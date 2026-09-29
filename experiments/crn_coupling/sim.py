#!/usr/bin/env python3
"""Toy check of common-random-number (CRN) coupling for multi-step agent A/B evaluation.

Question: when two agent configurations (say, two prompts) are compared by repeated runs,
how much does sharing the sampling noise between the two arms shrink the variance of the
estimated success-rate difference, and how must the shared noise be keyed so that the
coupling survives once the two trajectories diverge?

Toy agent. A task has K subgoals and a step budget T = 2K + 2. Each step attempts the current
subgoal: the policy picks one of m actions by Gumbel-max over its logits. Action 0 is correct
and completes the subgoal unless the environment fails (probability f). Actions 1..m-2 are
benign mistakes (the subgoal is retried). Action m-1 is irreversible and fails the episode.
Before each action the policy emits one or two "reasoning tokens" (two with probability
`verbosity`); they consume draws from the sampler's random stream but do not change outcomes.

Arms A and B share per-(task, subgoal) difficulty and distractor logits. Arm B adds `delta` to
the correct-action logit (a targeted improvement) and a fixed N(0, sigma^2) perturbation to
every logit (the broad side effects of, for example, a prompt edit).

Noise schemes:
  indep         independent noise for the two arms (the usual practice).
  same_seed     both arms read one sequential random stream per run, as when the same sampler
                seed is passed to both, and the environment is seeded per step.
  event         every draw is keyed by the decision it makes: (task, run, subgoal, attempt,
                action) for the policy and (task, run, subgoal, attempt) for the environment.
  event_policy  event-keyed policy noise, independent environment noise.

Every scheme leaves each arm's marginal distribution unchanged, so the estimate of the
success-rate difference stays unbiased; only its variance changes.
"""
import argparse
import json
import math
import time
from dataclasses import asdict, dataclass, replace

import numpy as np

U64 = np.uint64
Z_POWER = (1.959964 + 0.841621) ** 2  # two-sided alpha = 0.05, power = 0.8


def splitmix64(x):
    """SplitMix64 finalizer, vectorized over uint64 arrays."""
    with np.errstate(over="ignore"):
        z = x + U64(0x9E3779B97F4A7C15)
        z = (z ^ (z >> U64(30))) * U64(0xBF58476D1CE4E5B9)
        z = (z ^ (z >> U64(27))) * U64(0x94D049BB133111EB)
        return z ^ (z >> U64(31))


def mix(h, field):
    """Fold one non-negative integer key field into hash state h (a counter-based RNG)."""
    return splitmix64(h ^ np.asarray(field, dtype=np.int64).astype(U64))


def uniform(h):
    return ((h >> U64(11)).astype(np.float64) + 0.5) / 9007199254740992.0


def gumbel(h):
    return -np.log(-np.log(uniform(h)))


@dataclass(frozen=True)
class Params:
    K: int = 10                # subgoals per task (horizon)
    m: int = 5                 # actions: 0 correct, 1..m-2 benign mistakes, m-1 irreversible
    a0: float = 3.0            # base logit of the correct action
    tau: float = 1.0           # sd of per-(task, subgoal) difficulty
    distractor_sd: float = 0.5
    fatal_offset: float = -0.5
    f: float = 0.1             # environment (tool) failure probability per attempt
    delta: float = 0.3         # arm B: boost to the correct-action logit
    sigma: float = 0.0         # arm B: sd of a fixed perturbation added to every logit
    verbosity_a: float = 0.5   # P(two reasoning tokens before an action), arm A
    verbosity_b: float = 0.5   # same for arm B
    n_tasks: int = 100
    n_runs: int = 2000
    seed: int = 0


def build_logits(p):
    rng = np.random.default_rng(p.seed)
    N, K, m = p.n_tasks, p.K, p.m
    logits_a = rng.normal(0.0, p.distractor_sd, size=(N, K, m))
    logits_a[:, :, 0] = p.a0 - rng.normal(0.0, p.tau, size=(N, K))
    logits_a[:, :, m - 1] += p.fatal_offset
    logits_b = logits_a.copy()
    if p.sigma > 0:
        logits_b += rng.normal(0.0, p.sigma, size=(N, K, m))
    logits_b[:, :, 0] += p.delta
    return logits_a, logits_b


def run_arm(p, logits, arm, scheme, verbosity):
    """Simulate n_runs episodes of every task for one arm; return successes, shape (N, R)."""
    N, R, K, m = p.n_tasks, p.n_runs, p.K, p.m
    run_key = mix(mix(U64(0xA5A5A5A5 + p.seed), np.arange(N)[:, None]), np.arange(R)[None, :])
    own, shared = arm + 1, 0
    pol = mix(mix(run_key, 0), own if scheme == "indep" else shared)
    env = mix(mix(run_key, 1), own if scheme in ("indep", "event_policy") else shared)

    k = np.zeros((N, R), dtype=np.int64)       # current subgoal
    j = np.zeros((N, R), dtype=np.int64)       # attempt index on the current subgoal
    alive = np.ones((N, R), dtype=bool)
    cursor = np.zeros((N, R), dtype=np.int64)  # position in the shared stream (same_seed)
    rows = np.arange(N)[:, None]
    acts = np.arange(m)
    for t in range(2 * K + 2):
        active = alive & (k < K)
        if not active.any():
            break
        lg = logits[rows, np.minimum(k, K - 1)]
        if scheme == "same_seed":
            n_reason = 1 + (uniform(mix(pol, cursor)) < verbosity)
            start = cursor + 1 + n_reason                    # skip the reasoning-token draws
            g = gumbel(mix(pol[..., None], start[..., None] + acts))
            u = uniform(mix(env, t))
            cursor = np.where(active, start + m, cursor)
        elif scheme in ("event", "event_policy"):
            g = gumbel(mix(mix(mix(pol, k), j)[..., None], acts))
            u = uniform(mix(mix(env, k), j)) if scheme == "event" else uniform(mix(env, t))
        else:
            g = gumbel(mix(mix(pol, t)[..., None], acts))
            u = uniform(mix(env, t))
        action = np.argmax(lg + g, axis=-1)
        solved = active & (action == 0) & (u >= p.f)
        fatal = active & (action == m - 1)
        k += solved
        j = np.where(solved, 0, j + (active & ~solved & ~fatal))
        alive &= ~fatal
    return alive & (k == K)


def compare(p, scheme):
    la, lb = build_logits(p)
    sa = run_arm(p, la, 0, scheme, p.verbosity_a).astype(np.float64)
    sb = run_arm(p, lb, 1, scheme, p.verbosity_b).astype(np.float64)
    d = sb - sa
    R = p.n_runs
    var_paired = d.var(axis=1, ddof=1)                         # within-task Var(S_B - S_A)
    pa, pb = sa.mean(axis=1), sb.mean(axis=1)
    var_indep = (pa * (1 - pa) + pb * (1 - pb)) * R / (R - 1)  # the same arms run independently
    return {
        "scheme": scheme,
        "p_a": float(pa.mean()),
        "p_b": float(pb.mean()),
        "delta_hat": float(d.mean()),
        "se": float(math.sqrt(var_paired.mean() / (p.n_tasks * R))),
        "var_per_run": float(var_paired.mean()),
        "vrf": float(var_indep.mean() / var_paired.mean()),
        "reversal_rate": float((d < 0).mean()),
    }


def runs_for_power(var_per_run, delta):
    """Runs per arm (spread over the fixed task set) to detect delta at 80% power."""
    return math.ceil(Z_POWER * var_per_run / delta ** 2)


def sweep(base, label, key, values, schemes, **overrides):
    out = []
    for v in values:
        p = replace(base, **{key: v}, **overrides)
        rows = {s: compare(p, s) for s in schemes}
        if "same_seed" in schemes:
            rows["same_seed_verbose_b"] = compare(replace(p, verbosity_b=0.6), "same_seed")
        out.append({key: v, "rows": rows})
        print(f"[{label}] {key}={v} done", flush=True)
    return out


def fmt_table(sweep_rows, key, schemes, ref="event"):
    head = (f"| {key} | p_A | p_B | Δ̂ (event) | " + " | ".join(f"VRF {s}" for s in schemes)
            + " | runs/arm indep → event |")
    lines = [head, "|" + "---|" * (len(schemes) + 5)]
    for r in sweep_rows:
        rows, e = r["rows"], r["rows"][ref]
        indep_var = e["var_per_run"] * e["vrf"]
        runs = (f"{runs_for_power(indep_var, e['delta_hat']):,} → "
                f"{runs_for_power(e['var_per_run'], e['delta_hat']):,}")
        vrfs = " | ".join(f"{rows[s]['vrf']:.2f}" for s in schemes)
        lines.append(f"| {r[key]} | {e['p_a']:.3f} | {e['p_b']:.3f} | "
                     f"{e['delta_hat']:+.4f} ± {e['se']:.4f} | {vrfs} | {runs} |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", type=int, default=100)
    ap.add_argument("--runs", type=int, default=2000)
    ap.add_argument("--out", default="results.json")
    args = ap.parse_args()
    base = Params(n_tasks=args.tasks, n_runs=args.runs)
    t0 = time.time()
    all_schemes = ("indep", "same_seed", "event", "event_policy")
    res = {
        "params": asdict(base),
        "horizon": sweep(base, "horizon", "K", (1, 2, 5, 10, 20, 40), all_schemes),
        "distance": sweep(base, "distance", "sigma", (0.0, 0.1, 0.25, 0.5, 1.0),
                          ("same_seed", "event")),
        "effect": sweep(base, "effect", "delta", (0.05, 0.1, 0.3, 1.0), ("same_seed", "event")),
        "effect_broad": sweep(base, "effect_broad", "delta", (0.05, 0.1, 0.3, 1.0),
                              ("same_seed", "event"), sigma=0.25),
        "env": sweep(base, "env", "f", (0.0, 0.1, 0.3), ("same_seed", "event", "event_policy")),
    }
    res["seconds"] = round(time.time() - t0, 1)
    with open(args.out, "w") as fh:
        json.dump(res, fh, indent=2)

    cols = ("indep", "same_seed", "same_seed_verbose_b", "event", "event_policy")
    two = ("same_seed", "same_seed_verbose_b", "event")
    print("\n## Horizon (sigma=0, delta=0.3)\n" + fmt_table(res["horizon"], "K", cols))
    print("\n## Config distance (K=10, delta=0.3)\n" + fmt_table(res["distance"], "sigma", two))
    print("\n## Effect size, targeted change (K=10, sigma=0)\n" + fmt_table(res["effect"], "delta", two))
    print("\n## Effect size, broad change (K=10, sigma=0.25)\n"
          + fmt_table(res["effect_broad"], "delta", two))
    print("\n## Environment noise (K=10)\n"
          + fmt_table(res["env"], "f", ("same_seed", "event", "event_policy")))
    print("\n## Unbiasedness check: Δ̂ ± SE by scheme (horizon sweep)")
    for r in res["horizon"]:
        est = ", ".join(f"{s} {row['delta_hat']:+.4f}±{row['se']:.4f}" for s, row in r["rows"].items())
        print(f"- K={r['K']}: {est}")
    print("\n## Reversal rate P(S_B < S_A) under event coupling")
    for name in ("horizon", "distance", "effect", "effect_broad"):
        key = {"horizon": "K", "distance": "sigma"}.get(name, "delta")
        rates = ", ".join(f"{r[key]}: {r['rows']['event']['reversal_rate']:.4f}" for r in res[name])
        print(f"- {name}: {rates}")
    print(f"\nelapsed {res['seconds']} s")


if __name__ == "__main__":
    main()
