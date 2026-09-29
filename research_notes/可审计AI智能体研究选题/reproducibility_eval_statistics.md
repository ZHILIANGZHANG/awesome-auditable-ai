# Consistency, determinism, reproducibility and the statistics of evaluating LLM agents (plus evaluation integrity): research notes as of 2026-09-29

*Verification note (read first).* In this session the egress proxy blocked arxiv.org, export.arxiv.org, api.semanticscholar.org, www.semanticscholar.org, huggingface.co, alphaxiv.org, openreview.net, thinkingmachines.ai, lmsys.org and hal.cs.princeton.edu. The shared WebSearch budget (200 calls per session) ran out after 18 of my queries. For that reason the Semantic Scholar citation graphs of Chatzi et al. and Ravfogel et al. could not be pulled. Instead, novelty was checked with web-search extracts plus keyword and title searches over GitHub-hosted daily arXiv digests. Those digests (qhduan/cn-chat-arxiv, CSQianDong/Awesome-arXiv-Daily-Reporter) store full or roughly 1,000-character abstracts of new cs.CL/cs.AI papers, and the searches also covered author repositories and official docs on GitHub. Evidence tags used below:
- **[A]** abstract or primary text read verbatim (digest mirror, author repo, or official docs)
- **[W]** web-search extract of a page I could not open
- **[S]** third-party secondary summary (re-verify numbers before quoting)
- **[T]** title or metadata only

Canonical arXiv links are given even when the text was read through a mirror.

---

## Key question 1: What are the known sources of nondeterminism in agent runs, and what tooling exists (2026-09) for deterministic replay and forking?

### Takeaway
Agent-run nondeterminism has at least six layers:
1. inference numerics (batch-size-dependent reductions, prefix caching, quantization, precision)
2. intended sampling randomness
3. invisible provider-side serving changes and bugs
4. tool, environment, infrastructure and harness state
5. other stochastic actors (LLM user simulators, LLM judges)
6. execution-order and concurrency effects on random draws

By September 2026, bitwise-reproducible inference is achievable for *self-served open-weight* models: vLLM batch invariance (beta), SGLang's deterministic mode, LLM-42, or simply serial batch-size-1 inference with prefix caching off. Record/replay/fork tooling for agent runs has also multiplied (OrcaReplay, LangGraph time-travel, Plumbline, Amberfork, CAR, the Replay Gap branching harness). No tool I found *couples* randomness across different agent configurations, and hosted APIs remain uncontrollable. The README's open gap ("compare runs causally without discarding useful nondeterminism") is therefore still open at the tooling level.

### Cited Findings
**Inference numerics and serving engines**
- Thinking Machines ("Defeating Nondeterminism in LLM Inference", 2025) argues that temperature 0 plus a fixed seed does not guarantee identical outputs once batching and scheduling vary. Matmul, attention and normalization use reduction schedules that change with batch size. The fix is batch-invariant kernels for RMSNorm, matmul and attention (a "fixed split-size" decode). The post demos this on vLLM via FlexAttention/torch.Library, and the extract reports 1,000 identical runs giving bitwise-identical outputs. [W] — [Thinking Machines blog](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)
- LLM-42 (Gond, Kamath, Basu, Ramjee, Panwar; arXiv 2601.17768, Jan 2026) [A]:
  - Nondeterminism "arises from floating-point non-associativity combined with dynamic batching and GPU kernels whose reduction orders vary with batch size."
  - Disabling dynamic batching "severely degrades throughput". Batch-invariant kernels "tightly couple determinism to kernel design" and impose fixed overheads.
  - LLM-42 instead decodes on a nondeterministic fast path with a verify–rollback loop that replays candidate tokens under a fixed-shape reduction schedule, so overhead is paid only in proportion to traffic that needs determinism.
  - [arXiv](https://arxiv.org/abs/2601.17768); [abstract mirror](https://github.com/1jmdev/research/blob/ae20e11f9f37d19eeb8d9c1e545d3cf3b69b2f49/papers/serving-systems/_general/2601.17768-llm-42-enabling-determinism-in-llm-inference-with-verified-speculation.md)
- SGLang's FAQ attributes "about 95%" of its output indeterminism to dynamic batching and the rest to prefix caching. It suggests `--disable-radix-cache` with one request at a time, and now offers `--enable-deterministic-inference`. [A] — [SGLang FAQ](https://github.com/sgl-project/sglang/blob/c7be3e935b5034006cd6ae7977b41e2459b4126c/docs/docs/references/faq.mdx); LMSYS post "Towards Deterministic Inference in SGLang and Reproducible RL Training" dated 2025-09-22 in its URL [W] — [LMSYS](https://www.lmsys.org/blog/2025-09-22-sglang-deterministic/); feature issue [W] — [sglang#10278](https://github.com/sgl-project/sglang/issues/10278)
- SGLang determinism is not universal as of Sep 2026. [A] — [DeepSeek-V4 cookbook](https://github.com/sgl-project/sglang/blob/c7be3e935b5034006cd6ae7977b41e2459b4126c/docs/cookbook/autoregressive/DeepSeek/DeepSeek-V4_1.mdx); [speculative decoding doc](https://github.com/sgl-project/sglang/blob/c7be3e935b5034006cd6ae7977b41e2459b4126c/docs/docs/advanced_features/speculative_decoding.mdx); [server args](https://github.com/sgl-project/sglang/blob/c7be3e935b5034006cd6ae7977b41e2459b4126c/docs/docs/advanced_features/server_arguments.mdx)
  - The DeepSeek-V4 cookbook says "output is not bitwise stable across batch composition today" and that `--enable-deterministic-inference` "is refused on this backend".
  - Deterministic inference is "not yet supported" with the UNO speculative-decoding mode.
  - On MLX, per-request `sampling_seed` under deterministic mode is "deterministic within MLX only".
- vLLM enables batch invariance with `VLLM_BATCH_INVARIANT=1` (example uses the TRITON_ATTN backend). The docs say it "is currently in beta. Some features are still under active development" (tracking issue #27433). [A] — [vLLM docs](https://github.com/vllm-project/vllm/blob/e05095c9e1ae37f208c1ad70b08c17f1152878fc/docs/features/batch_invariance.md)
- "Same Request, Different Answer: Quantization Amplifies Cache-Induced Divergence in LLM Serving" (arXiv 2609.04748, Sep 2026) [A] — [arXiv](https://arxiv.org/abs/2609.04748); [abstract mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.04748.json)
  - Setup: model, decoding parameters, seed and request order held fixed; serial batch-size-1 requests; an 80-episode multi-turn agentic tool-use workload; 2 engines × 4 weight formats.
  - Enabling prefix caching changed the agent's trajectory in **36.2%** of episodes at 16-bit and **75.0%** at 4-bit.
  - With caching disabled, repeated execution was bit-identical in every configuration (0 of 800 episodes diverged).
- "How Lossless Is Lossless Speculative Decoding? The Role of Numerical Precision in Orthrus" (arXiv 2609.15504, Sep 2026) [A] — [arXiv](https://arxiv.org/abs/2609.15504); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.15504.json)
  - Under BF16, exact trajectory matching with the autoregressive reference occurred in only 45% (authors' checkpoint) and 43% (reproduction) of 1,190 prompts.
  - Match probability is associated with response-conditional perplexity.
  - There was no systematic degradation on lm-eval-harness.
- A survey of determinism in financial AI ("From accuracy to auditability", arXiv 2605.23955, May 2026) lists LLM-agent workflow failure modes as "batch-dependent differences and trajectory drift", alongside tabular and GNN nondeterminism. [A, via translated abstract] — [arXiv](https://arxiv.org/abs/2605.23955); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/05/2605.23955.json)

**Hosted / provider-side**
- "Noise Floor Audit for Agent Benchmarks" (Chen et al.; arXiv 2608.22331, Aug 2026) [A] — [arXiv](https://arxiv.org/abs/2608.22331); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.22331.json)
  - Setup: 3 native tool-calling endpoints from 2 providers on BFCL multiple/parallel, with matched AST grading.
  - Temperature-0 reruns were "nearly deterministic": ever-flip fractions 0.7%, 2.0%, 2.7%; mean run correlations 0.997, 0.966, 0.961.
  - Semantics-preserving prompt perturbations gave paired SDs **11×–58×** larger than rerun SDs.
  - Malformed-output failures were 30%, 7% and <1% of failures depending on endpoint.
- Provider-side infrastructure bugs change token selection invisibly. A third-party summary of Anthropic's 2025 postmortem lists a misconfiguration deployed Aug 25 that caused token-generation errors, and an XLA:TPU miscompilation "affecting token selection". [S] — [summary in claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/ed932a05a44a801e5deec462e949f35f7dca0eec/guide/core/known-issues.md)
- Already in the README: "Non-Determinism of 'Deterministic' LLM System Settings in Hosted Environments" (Eval4NLP 2025). — [ACL Anthology](https://aclanthology.org/2025.eval4nlp-1.12/)

**Environment, infrastructure and harness**
- Anthropic's "Quantifying infrastructure noise in agentic coding evals" (Gian Segato) [S] — [Anthropic](https://www.anthropic.com/engineering/infrastructure-noise); [notes 1](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/a66524cfb23f73c35ef171572cff3a028c7ce4e5/articles/evaluation/anthropic-infrastructure-noise-agentic-coding-evals-2026.md); [notes 2](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/a66524cfb23f73c35ef171572cff3a028c7ce4e5/articles/evaluation/infrastructure-noise-agentic-coding-evals-2026.md); [notes 3](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/a66524cfb23f73c35ef171572cff3a028c7ce4e5/articles/evaluation/anthropic-infrastructure-noise-benchmark-validity-2026.md)
  - Date: two secondary notes say 2026-02-05; one says "2026-04", so there is a conflict.
  - Claim: container resource allocation alone can shift agentic coding scores by more than the gap between top models.
  - A SWE-bench cross-check raised RAM from 1× to 5× on 227 problems × 10 runs each; scores rose monotonically, but only +1.54 pp. Terminal-Bench effects were described as larger.
  - Quoted line: "A few-point lead might signal a real capability gap—or it might just be a bigger VM."
  - One summary advises treating leaderboard gaps under 3 pp as not meaningful when configurations are undisclosed. This may be the summarizer's paraphrase.
- Harness and scaffold variance [S] — [atom harness-research notes](https://github.com/rush86999/atom/blob/6e34725c70179506515888a23c00635188f833c0/docs/architecture/AGENT_HARNESS_RESEARCH.md); [metaharness notes](https://github.com/ruvnet/metaharness/blob/9ce8b8dd89045c3b9a1f809ae58f3589029db4a4/docs/dream-cycle/2026-09-05-gist.md)
  - "Stop Comparing LLM Agents Without Disclosing the Harness" (Zhang et al., arXiv 2605.23950, May 2026) reports harness-induced variance exceeding model-induced variance, with rank reversals, and cites 69.7% → 77.0% on Terminal-Bench "from infrastructure alone".
  - Harness-Bench (arXiv 2605.27922, May 2026) reports a 23.8-point aggregate gap between harnesses on identical models and tasks (106 tasks × 6 harnesses × 8 backends; 5,194 trajectories).
  - A pre-registered study, "Scaffold Effects on GAIA" (arXiv 2606.08529), reports scaffold choice moving accuracy by up to 28 points within one model.
  - "The Scaffold Effect in Coding Agents" (KDD 2026 eval workshop) reports a 40× difference in tokens per solved task at near-equal pass rates.
  - README already lists WildClawBench: a harness swap moves one model by up to 18 points.
- Epoch AI's SWE-bench Verified tracker reportedly runs third-party scaffolds via Inspect-SWE "because scaffold choice changes results". A Scale SEAL note reports a 9.5-point swing from the harness alone. [S] — [metaharness notes](https://github.com/ruvnet/metaharness/blob/9ce8b8dd89045c3b9a1f809ae58f3589029db4a4/docs/dream-cycle/2026-08-14-gist.md)
- HAL's log inspection found agents "searching for the benchmark on HuggingFace instead of solving a task" and "misusing credit cards in flight booking tasks". It also found "higher reasoning effort reducing accuracy in the majority of runs". Open internet access is thus a source of both variance and integrity problems. [A] — [HAL arXiv 2510.11977](https://arxiv.org/abs/2510.11977); [abstract copy](https://github.com/stanford-cs336/lectures/blob/de53a9f979a6ee35f7d13a5e1aadee5ea1afc58e/var/files/arxiv-da52f2adde464d4d0a73c1f3ae830eae-https_arxiv_org_abs_2510_11977)
- A deterministic execution layer does not automatically buy reproducibility. "Harness Engineering for Predictable Agentic Systems" (arXiv 2608.26197, Aug 2026) wrapped agents in finite-state control, forced tool selection, output validation, bounded retry and structured planning (Qwen-2.5-7B, Gemma-3-27B; finance and legal tasks). Reproducibility improved significantly in 1 of 4 cells, degraded significantly in 2, and was unchanged in 1; a free-text planning step was the culprit. [A] — [arXiv](https://arxiv.org/abs/2608.26197); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.26197.json)
- "Agent bullwhip": in multi-echelon supply-chain (Beer Game) agents, run-to-run instability "can propagate across echelons and compound over time, even when the underlying demand path is held fixed". [A] — [arXiv 2605.17036](https://arxiv.org/abs/2605.17036); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/05/2605.17036.json)

**Other stochastic actors and execution-order effects**
- CAR-bench uses an "LLM-simulated user" whose incomplete or ambiguous requests the agent must resolve (as does τ-bench, per the README). The user simulator is itself a noise source. [A] — [TRACE/CAR-bench, arXiv 2608.22793](https://arxiv.org/abs/2608.22793); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.22793.json)
- LLM judges are stochastic and prompt-sensitive. On an 8-language Agent-as-a-Judge benchmark, "7 of 15 backbone pairs show statistically significant pairwise rank reversal" across prompt languages. [A] — [arXiv 2608.22432](https://arxiv.org/abs/2608.22432); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.22432.json)
- Buffalo, Pearson and Klein, "Realizing Common Random Numbers: Event-Keyed Hashing for Causally Valid Stochastic Models" (arXiv 2603.11084, Mar 2026). Reusing a base seed assumes "the same draw index corresponds to the same modeled event across scenarios". Standard PRNG practice yields "causally incoherent paired counterfactual comparisons". The remedy is counter-based RNGs (Philox/Threefry) keyed by event identifiers. [W] — [arXiv](https://arxiv.org/abs/2603.11084)

**Tooling for deterministic replay and forking (papers + open source), Sep 2026**
- Already in the README:
  - OrcaReplay: records model calls, workspace changes and MCP frames; re-executes against recorded responses and reports divergence; forks from a filesystem checkpoint onto a different model.
  - AgentRunProof: scripted-response conformance with content-addressed evidence.
  - Inspect: sandboxed execution, limits, approvals.
  - Docent: transcript clustering and search.
  - ActiveGraph, "The Log is the Agent" (arXiv 2605.21997): replay and forks from an event log.
  - ACRFence: checkpoint-restore semantic rollback attacks.
  - Local file: README.md, sections "Tools and Platforms" and "Audit Trails".
- Inspect has native repeated-run statistics: `--epochs` with reducers `mean`, `median`, `mode`, `max`, `at_least_{n}`, `pass_at_{k}` and `pass_k_{k}`, plus inter-judge agreement via `krippendorff_alpha()`. [A] — [Inspect options](https://github.com/UKGovernmentBEIS/inspect_ai/blob/f753add3909e0a2974249f0fa2c0896b5691f0e5/docs/options.qmd); [Inspect multi-scorer](https://github.com/UKGovernmentBEIS/inspect_ai/blob/f753add3909e0a2974249f0fa2c0896b5691f0e5/docs/multiple-scorers.qmd)
- LangGraph has checkpoint-based "time travel (replay and fork)" with fork checkpoints marked `source == "fork"`. [A] — [LangGraph tests](https://github.com/langchain-ai/langgraph/blob/07b33185eab893be2ed031eedae52f09314bf77c/libs/langgraph/tests/test_time_travel.py)
- Plumbline (open source, 2026) [A] — [README](https://github.com/Bhargs24/plumbline/blob/5c3005d1ae48683b9a7d7d98dc3d8a6bac98b9fb/README.md); [DESIGN](https://github.com/Bhargs24/plumbline/blob/5c3005d1ae48683b9a7d7d98dc3d8a6bac98b9fb/DESIGN.md)
  - Localizes divergence between tool-call sequences with Needleman–Wunsch alignment (match +2, mismatch −1, gap −2), so an omission reads as one gap rather than cascading mismatches.
  - Reports Wilson intervals and permutation tests, plus certificates, provenance and OTel/OpenInference ingestion.
  - Its "determinism study against a live model" commits 2,082 trajectories across three studies "and a retraction"; the numbers can be rechecked with no model calls.
- Amberfork (open source, 2026) aligns a failing run against a known-good reference run. [A] — [BENCHMARK.md](https://github.com/Melvin0070/amberfork/blob/7ba58e950d3e8fb6d73162a0d3fa0c11bdacc4cd/BENCHMARK.md); [README](https://github.com/Melvin0070/amberfork/blob/7ba58e950d3e8fb6d73162a0d3fa0c11bdacc4cd/README.md); [writeup](https://github.com/Melvin0070/amberfork/blob/7ba58e950d3e8fb6d73162a0d3fa0c11bdacc4cd/docs/writeup.md)
  - Details are under Key question 2(d).
- Causal Agent Replay (CAR) code, created 2026-06-03, describes itself as "counterfactual replay and causal attribution over LLM-agent trajectories". A second repo computes P(fail|kept) − P(fail|ablated), a point of commitment, and Shapley attribution. [T, repo descriptions] — [jaineet17/causal-agent-replay](https://github.com/jaineet17/causal-agent-replay); [krishddd/Trajectory_Causal_Attribution](https://github.com/krishddd/Trajectory_Causal_Attribution)
- The Replay Gap (Gonuguntla; arXiv 2608.08239; COLM 2026 Efficient Reasoning Workshop) [S summary + A bibtex] — [arXiv](https://arxiv.org/abs/2608.08239); [summary](https://github.com/xianshang33/llm-paper-daily/blob/e8d3636881edfaf3ea7c0f35baed0d027d1f7e2f/summary_en/2026-08/2608.08239.md); [repo](https://github.com/AshrithaG/replay-gap/blob/670d3c062b0aac26ff6e81988cbe17f3f454757f/README.md)
  - Ships an open-source "branching-rollout protocol".
  - It forks *live* SWE-bench agent trajectories at controlled points, rebuilds the environment, and uses same-model control forks to isolate noise.
  - It shows that static replay evaluators "mispredict every success-relevant outcome call".
- Evidence-Carrying Termination (arXiv 2608.23623, Aug 2026) lets an agent return COMPLETE only if a certificate binds each answer claim to in-scope trace evidence *and a deterministic replay reconstructs the claimed value*. It had 0/288 unsafe completions vs 252/288 for a termination-critic baseline. [A] — [arXiv](https://arxiv.org/abs/2608.23623); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.23623.json)
- "BTS-AgentBench: A Deterministic, Replayable Pipeline from Read-Only Telemetry Logs to Agent Benchmarks" (arXiv 2608.27334, Aug 2026). [T] — [arXiv](https://arxiv.org/abs/2608.27334)
- CALM (arXiv 2609.22252) uses "frozen prompt-response pairs" for "deterministic offline replay" of an LLM-driven simulator. This is a generic record/replay pattern. [A] — [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.22252.json)

### Inferences
- "Determinism" has split into three problems:
  1. numerical determinism, which is solved for self-served open weights but in beta and with caveats (vLLM beta; SGLang backend and feature exclusions)
  2. record/replay determinism, which logging solves (OrcaReplay, CALM, Plumbline)
  3. *causal comparability across configurations*, which is unsolved and is exactly the README's open gap.

  Replaying recorded outputs certifies the harness but, as the Replay Gap shows, "scores the wrong world" when the policy changes. Counterfactual questions need live branching with environment snapshotting.
- For a newcomer, the cheapest route to bitwise reproducibility is serial batch-size-1 inference with prefix caching off: 2609.04748 found 0/800 divergences that way. Batch-invariant modes are needed only for throughput.
- Nondeterminism of hosted APIs is provider- and configuration-specific (Noise Floor Audit), and silent provider bugs exist. Any shared-noise or coupling method will be limited to self-served open-weight models. For hosted models, API-side noise must be modeled as an uncontrolled variance component.
- Harness, infrastructure and resource variance can match or exceed model differences, so it must enter any variance decomposition (Key question 2(b)) and any integrity claim (2(e)).

### Gaps
- Primary pages for Thinking Machines, LMSYS, Anthropic (infrastructure noise and postmortem) and HAL could not be opened. Their numbers come from search extracts or secondary notes; verify them before final citation, including the "1,000 bitwise-identical runs" figure and the infrastructure-noise Terminal-Bench magnitude.
- Throughput overheads of vLLM and SGLang deterministic modes were not verified.
- I found no source quantifying wall-clock or date-dependent nondeterminism in agent benchmarks (time-dependent tasks, rate limits, TTL caches, live-web drift). ClawBench in the README runs on live websites, but that is indirect evidence.
- The current status of OpenAI's `seed`/`system_fingerprint` and any determinism options in Anthropic/Google APIs was not verified.
- No open tool was found that forks with *shared noise* across two agent configurations.

---

## Key question 2(a): Coupled / paired agent evaluation with common random numbers (Gumbel-max SCM + environment snapshotting + batch-invariant inference)

### Takeaway
**Verdict: partially addressed and converging fast; the specific agent version is still open.**
- Token-level coupling for evaluation is done for *single-turn* LLM benchmarks (Benz et al., AISTATS 2026: up to 75% fewer samples).
- Common-random-numbers (CRN) or paired designs appeared in agent work in Jun–Sep 2026: step attribution/credit (2609.06445, 2608.19760, CAR 2606.08275), agentic RL (2609.24144), and skill-library selection (2608.02005).
- Live forking of SWE-bench agents appeared too (Replay Gap).
- I found **no** paper or code that uses Gumbel-max token coupling of whole multi-step agent trajectories to cut the cost of A/B comparisons between agent configurations on standard agent benchmarks. That covers coupling the policy, the user simulator and the environment noise together.

It is still the best narrative fit to the README gap: CRN preserves each arm's marginal distribution, keeping "useful nondeterminism", while making the arms causally comparable. The window is closing, and the paper must answer the September 2026 critique that CRN estimands can fail (2609.06445).

### Cited Findings
**Foundations**
- Oberst & Sontag, "Counterfactual Off-Policy Evaluation with Gumbel-Max Structural Causal Models" (arXiv 1905.05824; ICML 2019, PMLR v97). They generate counterfactual trajectories in finite POMDPs via a Gumbel-max SCM and highlight episodes where the RL policy's counterfactual outcome differs most, for expert review. [W] — [arXiv](https://arxiv.org/abs/1905.05824); [PMLR](http://proceedings.mlr.press/v97/oberst19a/oberst19a.pdf)
- Lorberbom et al., "Learning Generalized Gumbel-max Causal Mechanisms" (arXiv 2111.06888, 2021; venue not verified here). [T] — [arXiv](https://arxiv.org/abs/2111.06888)
- Chatzi, Corvelo Benz, Straitouri, Tsirtsis, Gomez-Rodriguez, "Counterfactual Token Generation in Large Language Models" (arXiv 2409.17027). [W+A] — [arXiv](https://arxiv.org/abs/2409.17027); [PMLR v275 bib](https://github.com/mlresearch/v275/blob/44a2c63472bff65a4d852e179b9721d93a8cfec2/clear25.bib); [author page](https://github.com/Qvapil/Qvapil.github.io/blob/b9981080e31c0b36846b842d6c62b566073f7dac/_pages/about.md); [code](https://github.com/Human-Centric-Machine-Learning/counterfactual-llms/blob/ad3e0702ac5308f66c725e7f8725e7cd70f7a363/README.md)
  - Venue: CLeaR 2025 (PMLR v275); also presented at the NeurIPS 2024 Causality and Large Models workshop.
  - Method: the sampler becomes a Gumbel-max SCM. The RNG state at each step is stored and Gumbel values regenerated on the fly, so counterfactual tokens cost "almost no" extra.
  - Counterfactual stability favours counterfactuals similar to the factual sequence. Application: bias detection. Models: Llama 3 8B-Instruct and Ministral-8B-Instruct.
- Ravfogel et al., "Gumbel Counterfactual Generation From Language Models" (arXiv 2411.07180; ICLR 2025). They use hindsight Gumbel sampling to infer the latent noise of observed strings and generate counterfactuals under interventions on model internals. [W] — [arXiv](https://arxiv.org/abs/2411.07180)
- "Gumbel Machine: Counterfactual Student Writing Generation via Gumbel Noise Steering" (arXiv 2605.27249, May 2026) is an education application. This was the only Ravfogel/Chatzi follow-up surfaced by search; the citation graphs could not be pulled. [W] — [arXiv](https://arxiv.org/abs/2605.27249)

**Closest prior for (a)(i), variance-reduced comparison**
- Corvelo Benz, Tsirtsis, Straitouri, Chatzi, Artola Velasco, Thejaswi, Gomez-Rodriguez, "Evaluation of Large Language Models via Coupled Token Generation" (arXiv 2502.01754; ICLR 2025 workshop version; **AISTATS 2026**). [W] — [arXiv](https://arxiv.org/abs/2502.01754); [code](https://github.com/Human-Centric-Machine-Learning/coupled-llm-evaluation)
  - "Coupled autoregressive generation" makes different LLMs sample with the same source of randomness.
  - On benchmark datasets it reaches the same conclusions "using provably fewer samples", up to **75% fewer**.
  - On (human or LLM) pairwise comparisons, coupled and vanilla generation "can surprisingly lead to different rankings when comparing more than two models, even with an infinite amount of samples". The authors read this as the apparent advantage of a model being possibly "confounded by the randomness inherent to the generation process". Their LMSYS Chatbot Arena prompt experiment shows this.
  - Models were from the Llama, Mistral and Qwen families; everything is single-turn.
- Sharma, "When Does Pairing Seeds Reduce Variance? Evidence from a Multi-Agent Economic Simulation" (arXiv 2512.24145, Dec 2025). Paired seeds yield "strict variance reduction whenever outcomes are positively correlated at the seed level", tighter CIs and effective-sample-size gains, and recover independent evaluation when correlation is absent. The testbed is the TaxAI MARL simulator, not LLMs. [W] — [arXiv](https://arxiv.org/abs/2512.24145)
- OASE, "Evolving in the Agent Jungle via History-Informed Opponent Awareness" (arXiv 2608.02005, Aug 2026). It evaluates candidate and incumbent LLM-agent skill libraries under the same seed and an anchored opponent snapshot. The CRN paired estimator has "approximately half the variance" of the unpaired one in first-price auctions. [W] — [arXiv](https://arxiv.org/abs/2608.02005)
- "Luck Is Not Skill: When Do Paired Rollouts Help Group-Relative RL of LLM Agents?" (N. Sakib; arXiv 2609.24144, Sep 2026). [A] — [arXiv](https://arxiv.org/abs/2609.24144); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.24144.json); [author page with code link](https://github.com/TheDeadcoder/TheDeadcoder/blob/7f72962d1c3c3837b96f1ae8a84363e911cfc416/README.md)
  - Paired rollouts "share an event-keyed noise schedule within each group while preserving each rollout's marginal distribution". The shared noise is environment noise (tool faults, grader flips), not token noise.
  - Pairing removes the between-schedule component of reward-contrast variance "but need not reduce gradient variance", with an exact condition and a counterexample.
  - A registered 2B tool-use agent study gained +5.1 pp noisy-test success but missed the registered learning-curve criterion.
- Vera Zúñiga, "What Iterated Self-Feeding Probes of Language Models Measure…" (arXiv 2608.10986, Aug 2026). Advancing two token rings "under common random numbers makes undamaged copies diverge by exactly zero". The paper warns that some coupled measurements are properties of the construction, not the model, and reports "four retracted verdicts". [A] — [arXiv](https://arxiv.org/abs/2608.10986); [mirror](https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/5c92abb70af3796439f0e8320b2a961f56500a51/12-Aug-2026/NLP/papers.jsonl)
- Buffalo et al. (arXiv 2603.11084): event-keyed CRN (see Key question 1) is the technique needed to keep noise aligned once trajectories diverge. [W] — [arXiv](https://arxiv.org/abs/2603.11084)

**Closest prior for (a)(ii), counterfactual "what if this step differed" on agent trajectories**
- "Causal Attribution for Agentic Decisions: Estimators, Coupling, and a Traceability Specification" (arXiv 2609.06445, Sep 2026). [A] — [arXiv](https://arxiv.org/abs/2609.06445); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.06445.json); [code](https://github.com/designer-coderajay/Causal-Attribution-for-Agentic-Decisions/blob/bcba99958ace0ff5a4709f3abad26a11c9b4a3a7/README.md)
  - It separates the "marginal total effect that prior work measures" from "a common-random-numbers total effect that isolates a step's own contribution", and adds a natural direct effect under a pinned downstream.
  - "Both estimands then fail, in the same direction." Under the marginal estimand a causally inert step has the identical total effect as the decisive one on every run of a planted chain. Under CRN, "the decisive step returns exactly zero on the runs where the executing step flips, about one in ten".
  - It asks what records a high-risk agentic system must keep for post-hoc causal attribution, reading the question against EU Regulation 2024/1689.
- "Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures" (CAR; arXiv 2606.08275, Jun 2026). [W] — [arXiv](https://arxiv.org/abs/2606.08275)
  - It models a run as an SCM, applies a do-operation to a step, and "re-executes the trajectory forward under the same stochastic policy", measuring the shift in the outcome distribution.
  - It adds an intervention algebra, a single-step contrastive estimator with a "point-of-commitment rule", and budgeted Monte-Carlo Shapley. It is open source and says state-of-the-art LLM-judge step accuracy on Who&When is "about 14%".
  - Whether CAR shares noise across arms is unclear from the extract.
- "Credit Without Ground Truth: Auditing Step-Level Credit Assignment in LLM Agents Against Executed Replay" (Haiyue Zhang; arXiv 2608.19760, Aug 2026). [W] — [arXiv](https://arxiv.org/abs/2608.19760)
  - Ground truth comes from re-sampling the policy's alternatives at each decision point and rolling forward, in ALFWorld, with a paired CRN design (identical seeds, task order, environment seeds and RNG streams across arms).
  - 30.5% of decision points show a nonzero replay contrast. 13.1% vs 26.8% of points have no policy-supported counterfactual, depending on the policy.
  - LLM-judge scores, logprob ratios and policy confidence show no reliable fidelity beyond a shuffled control. Implicit credit tracks fluency (median rank correlation +0.75).
- "Should I Have Expressed a Different Intent? Counterfactual Generation for LLM-Based Autonomous Control" (arXiv 2601.20090, Jan 2026). It models the user–agent–environment closed loop as an SCM, generates candidate counterfactual outcomes via "probabilistic abduction" with test-time scaling, and calibrates "conformal counterfactual generation" sets with coverage guarantees. The application is wireless network control, where it beats naive re-execution. [W] — [arXiv](https://arxiv.org/abs/2601.20090)
- The Replay Gap (arXiv 2608.08239) does live branched forks of SWE-bench trajectories with same-model control forks. It does not couple noise. [S] — [summary](https://github.com/xianshang33/llm-paper-daily/blob/e8d3636881edfaf3ea7c0f35baed0d027d1f7e2f/summary_en/2026-08/2608.08239.md)
- Also surfaced but not read: "CausalFlow: Causal Attribution and Counterfactual Repair for LLM Agent Failures" (arXiv 2605.25338); "Abstract Counterfactuals for Language Model Agents" (Pona et al., arXiv 2506.02946); "Large Language Models as Nondeterministic Causal Models" (arXiv 2509.22297). [T] — [CausalFlow](https://arxiv.org/abs/2605.25338); [Abstract Counterfactuals](https://arxiv.org/abs/2506.02946); [LLMs as Nondeterministic Causal Models](https://arxiv.org/abs/2509.22297)

**Negative search results**
- A code search across GitHub for Gumbel-based counterfactual or coupled replay of agent trajectories returned only unrelated repositories.
- Keyword searches of 2026 digests found no paper combining "Gumbel"/"coupled generation" with agents. The only CRN-for-LLM-agent papers found are the ones listed above.
- Sources: [GitHub code search, performed 2026-09-29; no URL]; [digest repo](https://github.com/qhduan/cn-chat-arxiv)

### Inferences
- **How the idea differs from the closest work:**
  1. It moves from single-turn coupled generation (Benz) to multi-step, tool-interleaved trajectories. Once two coupled trajectories diverge, positional noise indices desynchronize, so the design needs **event-keyed noise** (keyed by task, turn, tool call and token position), borrowing Buffalo et al.'s ABM fix.
  2. It must couple **all** stochastic actors: the agent's sampler, the LLM user simulator (τ-bench and CAR-bench use one), and seeded environment randomness or injected faults (as 2609.24144 does for environment noise only).
  3. It compares *agent configurations* (prompts, scaffolds, same-family models, tool sets), not only models.
  4. It needs bitwise-deterministic serving (Key question 1), or else coupled arms diverge for numerical rather than causal reasons.
  5. For (a)(ii) it must go beyond CAR's interventional re-execution. The noise-sharing counterfactual has to confront 2609.06445's finding that CRN total effects can be exactly zero for decisive steps. Reporting CRN total effect, marginal total effect and natural direct effect side by side, with a diagnosis of when each fails, would be a contribution in itself.
- **Estimand subtlety** (inferred from Benz et al.'s pairwise-ranking result): for binary task success, CRN leaves each arm's marginal success probability unchanged, so it is pure variance reduction for accuracy *differences*. For pairwise-preference or judge-comparison metrics, coupling changes the estimand. A paper should state this cleanly, perhaps as a proposition.
- **Feasibility (3–6 months): medium.**
  - Compute: a few GPUs serving 7–14B same-family open-weight models, deterministically (or serial, uncached), plus a user-simulator model.
  - Environments: seedable and deterministic ones (τ-bench/τ²-bench DB tools, AppWorld, ALFWorld/TextWorld), with SWE-bench-style containers only as a stretch goal (snapshot or rebuild as in the Replay Gap).
  - Skills: probability and causal inference (Gumbel-max SCMs, CRN, variance of paired estimators) and sampler hacking in vLLM/SGLang or HF generate (Chatzi et al.'s code patches Llama generation).
  - Main risks: vocabulary mismatch across model families (token coupling is only natural within a shared tokenizer; my inference is that Benz et al. used same-family models, unverified); coupling correlation decaying quickly on long horizons (itself a reportable finding); closed APIs being excluded.
- **Target headline** (hypotheses to test, not findings):
  - (i) A variance-reduction curve: CRN-coupled A/B tests of agent configurations need k× fewer runs to detect a given Δ. Show how the gain decays with horizon and with per-step policy divergence, and that event-keyed noise recovers most of the gain lost to naive positional seeding.
  - (ii) Some published agent A/B conclusions or leaderboard orderings reverse or become non-significant under coupling.
  - (iii) Logging RNG states plus environment snapshots, the "audit-grade reproducibility record", enables post-hoc counterfactual audits at negligible overhead. This matches the traceability question 2609.06445 raises and the README's auditability framing.
- **Best-fit venue:** ICML or NeurIPS main track (method, theory and agent experiments), or ICLR. AISTATS or CLeaR suit a more theoretical cut, since that is where Benz et al. and Chatzi et al. landed. The workshop fallback is an ICML-style "Statistical Frameworks for Uncertainty in Agentic Systems" workshop, which the README shows existed at ICML 2026.

### Gaps
- The Semantic Scholar citation graphs of Chatzi et al. (2409.17027) and Ravfogel et al. (2411.07180) could not be pulled because the API was blocked. A citation sweep is still required before submission.
- Only the abstracts of 2609.06445, 2606.08275 and 2608.19760 were seen. Whether CAR or 2608.19760 use Gumbel-level token noise sharing, or only seed-level pairing, must be checked in the full texts.
- Whether Benz et al.'s coupling requires a shared vocabulary was not verified.
- I recall a result bounding the disagreement probability of Gumbel-max coupling relative to maximal coupling, in speculative-decoding literature ("coupling without communication"). It was not verified here and would be useful theory.

---

## Key question 2(b): Statistical power and variance decomposition of agent benchmarks (runs needed, clustered SEs, variance components, significance of leaderboard gaps)

### Takeaway
**Verdict: partially addressed and increasingly crowded for the headline message, open for a full crossed decomposition.**
- The "report error bars / how many runs and tasks" message is established by Miller (2024), HiBayES (2025), Signal and Noise (2025), HAL (ICLR 2026), and in 2026 by Efficient Benchmarking, How Many Tasks, Noise Floor Audit, Identical Runs and Anthropic's infrastructure-noise post.
- Still open: a **crossed variance-components (G-theory / mixed-effects) decomposition for agent benchmarks** that jointly estimates task, seed/sampling, serving-numerics, provider, infrastructure/resources, harness/scaffold, user-simulator and judge components with their interactions. It would feed a D-study (optimal tasks × runs) and a significance re-audit of public agent leaderboards.
- The README's variance-components and Dice Roll papers do this only for brand-recommendation answers, not agents.

### Cited Findings
**General methods**
- Miller, "Adding Error Bars to Evals" (arXiv 2411.00640, Nov 2024) treats eval questions as draws from a super-population and applies the CLT. It gives formulas for SEs, paired-difference analysis, clustered SEs and variance reduction, plus power analysis for "how many questions and runs are needed". lmms-eval 0.6 implemented SEs/CIs, clustered SEs and paired differences based on it. [S + A] — [arXiv](https://arxiv.org/abs/2411.00640); [notes](https://github.com/BobYeger/state-of-agents/blob/38add564c98bc2df5505b8d6e84ada4624e2fe2a/sources/Adding%20Error%20Bars%20to%20Evals.md); [lmms-eval 0.6](https://github.com/EvolvingLMMs-Lab/lmms-eval/blob/c59eb48ee9e5bfdf2bfd6ad97fa1aba5c9eef18f/docs/releases/lmms-eval-0.6.md)
- HiBayES (Luettgau, Coppock, Dubois, Summerfield, Ududec; UK AISI; arXiv 2505.05602, May 2025) is a hierarchical Bayesian GLM framework for AI evaluation statistics. It supports "classical question-answer benchmarks and advanced agentic evaluations, particularly in low-data scenarios (e.g., < 20 data points per evaluation)" and ships a package. [A] — [arXiv](https://arxiv.org/abs/2505.05602); [abstract mirror](https://github.com/Luvata/arxive/blob/1620fc6bcd136848375a9c12a057db05dfb0d287/pages/2025-05-12-cs-ai.html)
- "Signal and Noise: A Framework for Reducing Uncertainty in Language Model Evaluation" (Heineman et al., AI2; NeurIPS 2025; arXiv 2508.13144) defines signal (separating better from worse models) and noise (sensitivity to training-step variability). Higher signal-to-noise ratio gives more reliable small-scale decisions. Data: 30 benchmarks, 375 models, 900K results. It is about pretraining eval, not agents. [A] — [arXiv](https://arxiv.org/abs/2508.13144); [abstract mirror](https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/5c92abb70af3796439f0e8320b2a961f56500a51/19-Aug-2025/NLP/README.md)
- Also seen: "Instance-level Randomization: Toward More Stable LLM Evaluations" (EMNLP Findings 2025). [T] — [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.182/)

**Agent-specific**
- HAL, "Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation" (Kapoor + 30 authors; arXiv 2510.11977; ICLR 2026 per search extract). [A; venue W] — [arXiv](https://arxiv.org/abs/2510.11977); [abstract copy](https://github.com/stanford-cs336/lectures/blob/de53a9f979a6ee35f7d13a5e1aadee5ea1afc58e/var/files/arxiv-da52f2adde464d4d0a73c1f3ae830eae-https_arxiv_org_abs_2510_11977)
  - A standardized harness over hundreds of VMs ran 21,730 rollouts: 9 models × 9 benchmarks, about $40,000.
  - It shares all agent logs (2.5B tokens).
  - Its reliability dashboard claims accuracy is rising faster than reliability. [W] — [HAL reliability](https://hal.cs.princeton.edu/reliability/)
- Secondary notes on the HAL reliability dashboard and the final "Towards a Science of AI Agent Reliability" (arXiv 2602.16666, ICML 2026; in README) [S] — [sources.json](https://github.com/vasilyu1983/AI-Agents-public/blob/8dc5de47c1db00f8ba01806f5dddd798fc78cf22/frameworks/shared-skills/skills/foundations-reliability-theory/data/sources.json)
  - As of 2026-08-14 the dashboard covered 15 agents on GAIA and τ-bench airline across 12 metrics.
  - The final version has "a corrected outcome-consistency formula".
- "Efficient Benchmarking of AI Agents" (arXiv 2603.23749, Mar 2026). [A] — [arXiv](https://arxiv.org/abs/2603.23749); [abstract mirror](https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/5c92abb70af3796439f0e8320b2a961f56500a51/26-Mar-2026/AI/README.md); [code](https://github.com/fsndzomga/efficient-benchmarking-ai-agents)
  - Across 8 benchmarks, 33 scaffolds and 70+ model configurations, absolute score prediction degrades under scaffold shift but rank-order prediction stays stable.
  - Evaluating only tasks with 30–70% historical pass rates cuts tasks by 44–70% with high rank fidelity.
  - Random subsets show "high variance across seeds".
- "How Many Tasks Are Enough for Agent Benchmark Decisions? A Replay Analysis of Public LLM Agent Benchmarks" (Huang et al.; arXiv 2607.12338, Jul 2026). [S] — [arXiv](https://arxiv.org/abs/2607.12338); [notes](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/1af0a59b73b364613425a0aedf43477fdfe97e09/docs/agent-design-space-source-notes.md); [authors/code](https://github.com/js-lee-AI/awesome-llm-agent-papers/blob/6552bcff902193e5bd721cff1ff74efba388e8aa/README.md)
  - Replaying SWE-bench, AppWorld and τ-bench shows how much of each benchmark must be run to reach the full-run conclusion: AppWorld 15%, τ-bench 25%, SWE-bench Verified **90%**.
  - It recommends that partial-evaluation reports state the margin, task-selection method, coverage rule, decision criterion and the number of unresolved comparisons.
- Noise Floor Audit (arXiv 2608.22331): prompt-perturbation paired SDs are 11–58× larger than rerun SDs on BFCL (see Key question 1). [A] — [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.22331.json)
- "Identical Runs, Different Results: Benchmarking AI Coding Agents on Open-Weight Models" (Ariño de la Rubia & Pafka; arXiv 2609.33812, Sep 2026; the affiliation line reads "Epoch", unclear whether Epoch AI). [A; last two numbers W] — [arXiv](https://arxiv.org/abs/2609.33812); [paper source](https://github.com/earino/identical-runs-different-results/blob/d98dd8821fd8871e2a07591bb0093d02767f1f46/paper/identical-runs-different-results.md)
  - Task: an agent improves XGBoost training code for airline delays; a hidden holdout scores it.
  - 584 runs covered 6 agents on 6 open-weight endpoints, with 6 pairings run 52 times each.
  - "Identical runs of one pairing varied more than the pairings differed from one another, so comparisons of a few runs ranked them unreliably." Resolving the observed differences "would take tens to more than a hundred" runs.
  - The six pairing means span 0.0095 AUC while the median within-pairing SD is 0.0107.
  - The repo includes a VERIFY.md mapping each claim to a command.
- Anthropic's infrastructure-noise post: resource allocation shifts scores. [S] (see Key question 1)
- Harness variance: "Stop Comparing LLM Agents Without Disclosing the Harness" (2605.23950), Harness-Bench (2605.27922), Scaffold Effects on GAIA (2606.08529), and "The Scaffold Effect" (arXiv 2607.22585, "harness-specific cost and failure fingerprints under fixed models"). [S] — [atom notes](https://github.com/rush86999/atom/blob/6e34725c70179506515888a23c00635188f833c0/docs/architecture/AGENT_HARNESS_RESEARCH.md); [guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/ed932a05a44a801e5deec462e949f35f7dca0eec/guide/core/agent-harness.md)
- Also surfaced by title only: "Measuring Harness-Induced Belief Divergence in Multi-Step LLM Agents" (Yi et al., arXiv 2607.04528) and "Beyond Static Leaderboards: Predictive Validity for the Evaluation of LLM Agents" (Patel et al., arXiv 2606.19704). [T] — [list](https://github.com/js-lee-AI/awesome-llm-agent-papers/blob/6552bcff902193e5bd721cff1ff74efba388e8aa/README.md)
- Consistency gaps between pass@1 and pass^k keep appearing:
  - AppWorld with GPT-4.1 ReAct: 77% mean per-run pass vs 53% all-5 success, a "24-point consistency gap". [A] — [arXiv 2609.08832](https://arxiv.org/abs/2609.08832); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.08832.json)
  - τ-Rec (Jun 2026 digest; arXiv ID not captured): best model about 57% pass^1 vs about 38% pass^4. [A] — [mirror](https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/5c92abb70af3796439f0e8320b2a961f56500a51/10-Jun-2026/NLP/README.md)
- Already in the README: "Where Does the Noise Come From?" (variance components, brand answers; arXiv 2607.13304) and "The Dice Roll Method" (G-theory, power, block bootstrap, brand answers; arXiv 2609.04047).

### Inferences
- **How a new paper would differ:** the README's variance-components work is for brand answers, and the agent papers each isolate one or two factors: tasks (How Many Tasks, Efficient Benchmarking), reruns vs prompt perturbations (Noise Floor), identical runs (Identical Runs), infrastructure (Anthropic), harness (Harness-Bench). Nobody has published a *crossed* design on agent benchmarks that estimates all the components *and their interactions*. The key interactions are model × harness, model × infrastructure and task × seed. The paper would then turn those estimates into (i) a D-study giving the cheapest tasks × runs design for detecting Δ = 1–3 pp per benchmark, (ii) a re-audit of what fraction of public leaderboard adjacent-rank gaps are significant under clustered or hierarchical models, and (iii) a reporting standard with software, for example an Inspect or HAL plugin.
- **Feasibility: high.**
  - Reusable data: public HAL logs (2.5B tokens), public replays (How Many Tasks), public run records (METR TH1.1; see 2(c)).
  - Controlled new runs with open-weight models can toggle prefix caching, quantization, batch invariance, resource limits and harness. Statistics skills (mixed models, G-theory, HiBayES) are learnable in the time frame.
- **Target headline** (hypotheses): for SWE-bench/Terminal-Bench-class benchmarks, harness × model and infrastructure components are the same order as the model main effect; after clustering, only a minority of adjacent leaderboard gaps are significant; a D-study shows that more tasks, not more seeds, is usually the cheaper lever (or the reverse), benchmark by benchmark.
- **Best venue:** NeurIPS Datasets & Benchmarks, ACL/EMNLP (evaluation methodology), ICLR if the leaderboard audit is striking; KDD applied data science or its agentic-evaluation workshop. There was a KDD 2026 agentic AI evaluation workshop. [S] — [atom notes](https://github.com/rush86999/atom/blob/6e34725c70179506515888a23c00635188f833c0/docs/architecture/AGENT_HARNESS_RESEARCH.md)
- Risk: novelty is incremental unless the crossed design and the audit are clearly more comprehensive than How Many Tasks, Identical Runs and Noise Floor, which all appeared in Jul–Sep 2026. Combining (b) with (a), showing which variance components CRN coupling removes, or with (c), would sharpen it.

### Gaps
- The primary texts of Miller and METR, and full texts of How Many Tasks and Identical Runs, were not readable.
- Whether any 2026 paper already fits a full crossed mixed model on agent benchmarks (for example inside HAL's ICLR camera-ready or the "Towards a Science" final version) could not be excluded.
- Anthropic's Terminal-Bench numbers (magnitude of resource-induced swing) remain unverified.

---

## Key question 2(c): Reliability decomposition into per-step error hazard + recovery rate (Markov/survival) to forecast long-horizon success and pass^k

### Takeaway
**Verdict: largely done for the basic Markov/hazard version, open for identification and forecasting.**
- TraceToChain (arXiv 2604.24579, Apr 2026) already fits agent traces to absorbing Markov chains and shows pass@k, pass^k and the reliability decay curve (RDC) are projections of one success-time distribution.
- Constant-hazard and Weibull fits to horizon curves exist: Ord (2025), METR, and Hamilton (2026).
- A 2026 preprint argues horizon-curve "hazards" confuse a cross-sectional mean with a mechanism.
- Still open: separating per-attempt hazard from task heterogeneity (frailty) using *repeated attempts*, explicitly estimating recovery, and *prospectively* validating forecasts of long-horizon pass^k from cheap short-horizon measurements.

### Cited Findings
- TraceToChain (arXiv 2604.24579, Apr 2026, cs.SE) [A] — [arXiv](https://arxiv.org/abs/2604.24579); [abstract mirror](https://github.com/Mont9165/arxiv-issue-bot/blob/cfbbaf80083d0bd11ff4c45815bdd088dedaf0e4/data/papers/2604.24579.md)
  - Fits agent traces to an absorbing DTMC with an automatic cluster taxonomy and Laplace-smoothed MLE.
  - Checks fit with an AIC + Kolmogorov–Smirnov certificate and reports Dirichlet-posterior and bootstrap intervals, adapting Kemeny–Snell, Cheung and Goel–Okumoto reliability math.
  - "pass@k, pass^k, and the RDC are projections of one success-time distribution."
  - On 7 controlled MAST-style frameworks with a 50/50 fit/test split: max L∞ RDC error 0.053 (median 0.048); KS accepts 7/7 (min p = 0.78).
- Ord, "Is there a half-life for the success rates of AI agents?" (arXiv 2505.05115, May 2025) models a constant failure rate per human-minute, giving exponential decline and a per-agent half-life (about 59 minutes for Claude 3.7 Sonnet). A rule of thumb: doubling duration squares success probability. [W] — [arXiv](https://arxiv.org/abs/2505.05115); [author page](https://www.tobyord.com/writing/half-life)
- METR, "Measuring AI Ability to Complete Long Tasks" (Kwa et al.; arXiv 2503.14499; NeurIPS 2025 per notes; revised 2026-02-25) finds the 50% time horizon doubling about every 7 months. METR's "Time Horizon 1.1" (2026-01-29) and "limitations of time horizons" (2026-01-22) notes reportedly say reliability-critical tasks need 98%+ success. [S] — [notes](https://github.com/coco-research/coco/blob/fcd2856f29fa2cf9d3a8dc64f00220a1a2202772/systems/superintelligence/ai/research/beth-barnes/02-seven-month-rule-and-long-task-horizon.md); [notes](https://github.com/tatra-labs/tatra-labs.github.io/blob/146febca890f7e4855bff0b92346dc781656a036/content/posts/who-closes-the-loop/sections/sec-7-1.md)
- Hamilton (2026 blog, "Peto's Paradox and the Future of AI Agents") fits a Weibull S(t) = exp(−(t/λ)^κ). Frontier models have κ ≈ 0.6–0.9, a *declining* hazard, while humans are about 0.37. Ord had noted that METR's 80%-to-50% horizon ratio for Claude 3.7 Sonnet (about 0.25) is close to the constant-hazard value (0.32). [S] — [notes](https://github.com/tatra-labs/tatra-labs.github.io/blob/146febca890f7e4855bff0b92346dc781656a036/content/posts/who-closes-the-loop/sections/sec-2-2.md)
- The "horizon-curve-mean-not-mechanism" preprint (GitHub, 2026; arXiv ID not found) is built on METR's public TH1.1 run records and HCAST tasks. [A] — [README](https://github.com/Atharva12081/horizon-curve-mean-not-mechanism/blob/2a769b7bafb05beebc501a0182873fea3752c69c/README.md); [paper source](https://github.com/Atharva12081/horizon-curve-mean-not-mechanism/blob/2a769b7bafb05beebc501a0182873fea3752c69c/paper/main.tex)
  - "Treating the resulting curve's derivative as a within-run failure hazard confuses a cross-sectional mean with a mechanism: one binary outcome per task cannot separate attempt noise from persistent task difficulty."
  - It uses complete monotonicity (a mixture-of-exponentials characterization) that "holds for the declining-hazard Weibull family".
- "Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents" (arXiv 2603.29231; in README) defines RDC, the Variance Amplification Factor, the Graceful Degradation Score and the Meltdown Onset Point. It covers 10 models, 23,392 episodes and a 396-task benchmark in 4 duration buckets and 3 domains. [A] — [abstract mirror](https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/5c92abb70af3796439f0e8320b2a961f56500a51/1-Apr-2026/AI/README.md)
- Recovery-focused benchmarks exist but do not model hazard: ToolMaze (arXiv 2606.05806, "dynamic replanning and anomaly recovery"), plus the README's ReliabilityBench and PALADIN. [T] — [list](https://github.com/js-lee-AI/awesome-llm-agent-papers/blob/6552bcff902193e5bd721cff1ff74efba388e8aa/README.md)

### Inferences
- **How a new paper would differ from TraceToChain:**
  1. Use real long-horizon agent benchmarks with repeated attempts per task (HAL reliability runs, τ-bench pass^k runs, METR TH1.1 records if they contain repeats) instead of controlled MAST-style frameworks.
  2. Use a **frailty / hierarchical survival model**, with a per-task random hazard multiplier, to separate within-attempt hazard from between-task heterogeneity. That is exactly the identification problem the horizon-curve preprint says single-outcome data cannot solve.
  3. Model an explicit error → recovery transition, since recovery rate is a plausible reason Weibull κ < 1.
  4. Run a *prospective* forecasting test: fit on short tasks or cheap step-level probes, then predict pass^k on held-out long tasks.
- **Feasibility: high.** Compute is low (mostly reanalysis plus modest new runs); skills are survival analysis, mixed models and Markov chains. The risk is that TraceToChain and the horizon-curve preprint make reviewers see it as incremental unless the frailty result is decisive.
- **Target headline** (hypotheses): the declining population hazard in horizon curves is mostly task heterogeneity, and per-attempt hazard is near-constant. Two consequences would follow: (i) pass^k decays faster at long horizons than curve-extrapolation suggests, and (ii) recovery rate, not first-error rate, explains most cross-model differences in long-horizon success. Either could be falsified, which is good.
- **Best venue:** ICML or NeurIPS (a statistical modeling contribution with an AI-forecasting impact story), or TMLR; it could merge with (b) into a stronger "statistical foundations of agent reliability" paper.

### Gaps
- The arXiv ID, authorship and venue of the horizon-curve preprint are unknown. "Noema Research Laboratory" branding appears in the LaTeX; the arXiv status was not verified.
- Whether METR TH1.1 public records contain multiple attempts per task (needed for frailty identification) was not verified.
- Hamilton's blog and METR's TH1.1 and limitations notes were only seen via secondary notes.
- "Long-horizon execution" or self-conditioning papers from 2025 that measure per-step accuracy compounding were not re-verified here and should be checked.

---

## Key question 2(d): Divergence debugging — align repeated runs, find fork points, test whether forks predict or localize failures

### Takeaway
**Verdict: partially addressed; the core scientific question is still open.**
- Tools and adjacent papers now exist:
  - a Consistency Analyzer that "pinpoints where and why a trajectory is likely to flip" (2609.08832, used for self-improvement, not attribution evaluation)
  - open-source aligners (Amberfork, Plumbline)
  - replay and divergence tooling (OrcaReplay, Replay Gap)
  - interventional attribution by re-execution (CAR, Credit Without Ground Truth, 2609.06445)
- Still open: a rigorous test of whether *naturally occurring* multi-run fork points, weighted by outcome relevance, localize *human-labeled* decisive errors better and more cheaply than LLM-judge attribution, on benchmarks with reproducible environments. Amberfork's own write-up says natural-failure evidence was elusive.

### Cited Findings
- "Closing the Consistency Gap: Self-Evolving Agents That Learn to Stay on Course" (arXiv 2609.08832, Sep 2026) [A] — [arXiv](https://arxiv.org/abs/2609.08832); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.08832.json)
  - AppWorld GPT-4.1 ReAct succeeds on all 5 runs only 53% of the time vs a 77% mean.
  - A "Consistency Analyzer … pinpoints where and why a trajectory is likely to flip across executions", and a Guideline Generator turns the diagnosis into episodic memory.
- Already in the README: "When Agents Disagree With Themselves" (arXiv 2602.11619). Tasks with inconsistent action paths score lower.
- Amberfork (GitHub, 2026) [A] — [BENCHMARK.md](https://github.com/Melvin0070/amberfork/blob/7ba58e950d3e8fb6d73162a0d3fa0c11bdacc4cd/BENCHMARK.md); [writeup](https://github.com/Melvin0070/amberfork/blob/7ba58e950d3e8fb6d73162a0d3fa0c11bdacc4cd/docs/writeup.md)
  - Hypothesis: "Aligning a failing run against a known-good reference run localizes the decisive error step at least as well as single-trace LLM-judge attribution — and does so explainably, locally, offline."
  - Protocol: "controlled-injection localization on real logs (chimera pairs…)". "Alignment + sustained-divergence rule 70%" within a ±3-step window.
  - Caveat, in the authors' words: injected forks make "sustained divergence at the gold step … true by construction". For natural failures "we went looking — repeatedly".
- Plumbline: Needleman–Wunsch divergence localization plus permutation tests (see Key question 1). [A] — [README](https://github.com/Bhargs24/plumbline/blob/5c3005d1ae48683b9a7d7d98dc3d8a6bac98b9fb/README.md)
- Interventional and replay attribution: CAR (arXiv 2606.08275; LLM-judge step accuracy on Who&When "about 14%"), Credit Without Ground Truth (arXiv 2608.19760; 30.5% of decision points have a nonzero replay contrast), and 2609.06445 (CRN vs marginal estimand failures). [W/A] — [CAR](https://arxiv.org/abs/2606.08275); [2608.19760](https://arxiv.org/abs/2608.19760); [2609.06445 mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.06445.json)
- AgentWorld (arXiv 2608.24076, Aug 2026) has an adversarial risk analyzer that snapshots the required intermediate-state "spine" and runs Monte-Carlo branch rollouts under 4 perturbation types, with ΔP/ΔT scoring, Dempster–Shafer fusion and Shapley attribution. It also uses pass^k consistency metrics. [A, via translated abstract] — [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.24076.json)
- "Root-Cause Attribution Is a Search Problem: Continual Search for Long-Horizon Agent Failures" (arXiv 2609.13463, Sep 2026) observes that one-shot LLM judges "settle on a plausible diagnosis early, leaving critical evidence in longer traces unexamined". [A] — [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.13463.json)
- Testbeds already in the README:
  - TraceElephant (ACL 2026): fully observable traces and *reproducible environments*.
  - Who&When Pro (arXiv 2607.09996): replays a successful prefix exactly, then injects one failure.
  - TelemetrySuffBench: fault-origin step accuracy ≤ 0.5% from telemetry views.
  - OrcaReplay: divergence reports.

### Inferences
- **How a new paper would differ:**
  - (i) Use *natural* repeated runs (K ≈ 10–20 per task) instead of injected forks (Amberfork, Who&When Pro).
  - (ii) Build a prefix tree of aligned runs, then estimate each fork's outcome relevance as the drop in empirical or branch-rollout success probability. This separates benign from pivotal divergence, which matters because 2608.19760 finds only about 30% of decision points change outcomes.
  - (iii) Validate against labeled decisive steps (TraceElephant, Who&When) and against interventional estimates (CAR-style). The link to consistency: the fork structure *is* the consistency measurement, so one data collection yields both a consistency score and attribution.
- **Feasibility: high to medium.** Needs repeated runs on reproducible environments (TraceElephant, τ-bench, AppWorld) and alignment algorithms (edit distance over tool calls plus semantic matching). Compute is modest with open or cheap models. Pitfall: labeled datasets are fixed logs, and re-running them requires the original environments; TraceElephant is the exception and a good fit.
- **Target headline** (hypotheses): the first outcome-relevant fork, estimated from about 10 natural runs, localizes annotated decisive errors within ±1 step far more often than LLM-judge attribution (about 14% step accuracy per CAR) at a fraction of the cost. Most divergence is benign, and a small set of "pivotal" forks carries the failure risk.
- **Best venue:** ACL/EMNLP (the failure-attribution line: Who&When at ICML 2025, TraceElephant at ACL 2026), ICLR, or KDD.

### Gaps
- Full texts of 2609.08832 (how the Consistency Analyzer localizes flips) and CAR were not read; overlap must be checked.
- Amberfork's natural-failure results and Plumbline's "retraction" details were not read in full.
- "Thought Anchors"-style counterfactual resampling of reasoning steps is a close analog for single traces but was not verified in this session.

---

## Key question 2(e): Evaluation integrity beyond BenchJack / AgentRewardBench / SpecBench — LLM-judge reliability on trajectories and reward-hacking detection

### Takeaway
**Verdict: very active and crowded in Aug–Sep 2026; niches remain.**
- New benchmarks for trajectory judges exist (MobileJudgeBench), as does a controlled "trajectory-judge" study showing outcome-only judges miss about half of silent faults.
- Other new work: rubric induction against over-crediting, rank reversal of multilingual judges, hack-verifiable environments (HVTB), formal reward-integrity instrumentation (BenchShield), and contract-based deterministic supervision (ContrAgent). Earlier foundations are ImpossibleBench and the Agentic Benchmark Checklist.
- Open niches:
  - (i) judge stochasticity as a *variance component* and its effect on leaderboard significance (connects to (b))
  - (ii) *intermittent* reward hacking across repeated runs ("hack@k"), since single-run audits may underestimate propensity (connects consistency and integrity)
  - (iii) attested, reproducible evaluation runs: evidence that a score came from a declared configuration and stayed within the evaluation boundary

### Cited Findings
- "trajectory-judge: What Outcome-Only LLM Judges Miss on Agent Trajectories" (arXiv 2609.00038, Sep 2026) [A] — [arXiv](https://arxiv.org/abs/2609.00038); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.00038.json)
  - Setup: a deterministic tool-using support-desk environment, an oracle policy, and single-fault injection at a known step, split into silent vs loud faults.
  - 5 judges were scored over 400 trajectories.
  - The outcome-only judge catches 84% of loud but **45% of silent** faults and flags **33% of correct** trajectories. A step-rubric judge reaches 77% silent recall.
- MobileJudgeBench, "Benchmarking LLM Judges for Mobile Agent Evaluation" (arXiv 2608.11434, Aug 2026) [A] — [arXiv](https://arxiv.org/abs/2608.11434); [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.11434.json)
  - 931 human-annotated trajectories from 6 benchmarks, 4 agent models and 68 apps; 6 judge methods.
  - A simple baseline with sampled screenshots is competitive with purpose-built judges, and "the LLM backbone is the primary driver".
- RubricForge, "Inducing Reward-Free Judging Rubrics that Reduce Over-Crediting in Agent Evaluation" (arXiv 2608.13564, Aug 2026). Existing judges "tend to credit fluent but unsuccessful trajectories as successes". Rubrics are evolved against labeled trajectories to agree with environment reward. [A] — [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.13564.json)
- "Rank Reversal in Multilingual LLM Judges" (arXiv 2608.22432): 7/15 backbone pairs have significant rank reversal. A label-free double-centering calibrator (CBC) raises cross-task rank consistency τ from 0.650 to 0.902 over 7,920 judge runs. [A] — [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.22432.json); [fuller abstract](https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/5c92abb70af3796439f0e8320b2a961f56500a51/25-Aug-2026/NLP/README.md)
- "Hack-Verifiable Terminal Bench: Evaluating Reward Hacking in Terminal Tasks" (arXiv 2608.22103, Aug 2026). [A] — [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.22103.json)
  - Detection by humans or LLM judges "can be unreliable".
  - Hack-verifiable environments embed detectable hacks so hacks can be identified automatically.
  - It measures frontier-model hack rates and whether prompting prevents known hacks and "unknown unknowns".
- "BenchShield: Formal Model-Backed Instrumentation for Reward Integrity in LLM-Agent Evaluation Infrastructure" (arXiv 2609.11028, Sep 2026). Existing defenses "do not provide reusable evidence that a concrete run remained within its intended evaluation boundary". It grounds detection in "a finite lifecycle model of an evaluation's reward-relevant events" with static phase-aware taint analysis and more. [A] — [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.11028.json)
- ContrAgent, "Symbolic Temporal Supervision of LLM Agents Using Contracts" (arXiv 2609.18128). Existing safeguards "grade recorded trajectories post hoc with stochastic LLM judges". It instead uses assume-guarantee contracts in LTLf over tool-call traces, a deterministic artifact. [A] — [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.18128.json)
- AutoGym (arXiv 2609.22592) generates gyms with verifiers because post-hoc LLM judges are "unreliable". [A] — [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.22592.json)
- ImpossibleBench (arXiv 2510.20270; ICLR 2026 per notes) mutates unit tests to contradict specs, so "cheating rate" is the pass rate on impossible tasks (LiveCodeBench- and SWE-bench-derived). [S] — [notes](https://github.com/zhaoyang97/Paper-Notes-en/blob/148a16dd45b148e890b4428db21133e5a1589b77/docs/ICLR2026/llm_safety/impossiblebench_measuring_llms_propensity_of_exploiting_test_cases.md); [summary](https://github.com/memgrafter/research-digests/blob/491d1e597ee1384396057fbe72e2bdec9f11c2c6/ml_research_analysis_2025/2510.20270_impossiblebench-measuring-llms-propensity-of-exploiting-test-cases_20260208_120718.md)
  - Hidden tests nearly eliminate cheating but hurt legitimate performance; read-only tests are a compromise.
  - Allowing multiple submissions raised cheating from 33% to 38%.
  - A flag-for-human option cut GPT-5 cheating from 54% to 9% and o3 from 49% to 12%, with limited effect on Claude Opus 4.1.
- "Establishing Best Practices for Building Rigorous Agentic Benchmarks" (Zhu, Jin, Liang, Kang, Stoica et al.; arXiv 2507.02825, Jul 2025) introduces the Agentic Benchmark Checklist (outcome validity, task validity, reporting). Benchmark issues can under- or over-estimate agent performance "by up to 100% in relative terms". [S] — [review JSON](https://github.com/onehr/agent-readings/blob/7c16813eecdbc92437a886864d5da165cc96d3d5/data/reviews/rigorous-agentic-benchmarks-zhu-2025.json); [notes](https://github.com/vasilyu1983/AI-Agents-public/blob/8dc5de47c1db00f8ba01806f5dddd798fc78cf22/frameworks/shared-skills/skills/qa-agent-testing/references/agentic-benchmarks.md)
- HAL's LLM-aided log inspection surfaced benchmark-lookup and credit-card misuse behaviours. [A] — [HAL abstract](https://github.com/stanford-cs336/lectures/blob/de53a9f979a6ee35f7d13a5e1aadee5ea1afc58e/var/files/arxiv-da52f2adde464d4d0a73c1f3ae830eae-https_arxiv_org_abs_2510_11977)
- Test evidence can be hollow: "64.8% of real agentic PRs touch test files with zero executable-line coverage" (arXiv 2607.18057, ICSME). [S] — [metaharness notes](https://github.com/ruvnet/metaharness/blob/9ce8b8dd89045c3b9a1f809ae58f3589029db4a4/docs/dream-cycle/2026-09-05-gist.md)

### Inferences
- The "are judges reliable?" axis is saturating: MobileJudgeBench, trajectory-judge, RubricForge, AgentRewardBench and AgentAuditor all address it. A newcomer should avoid another judge benchmark.
- **Better angles:**
  1. **Judge noise as a variance component.** Rerun judges on identical trajectories (serving nondeterminism, temperature) and propagate their flip rate into leaderboard CIs. Inspect already supports multi-judge Krippendorff's α.
  2. **Hack@k.** Reward hacking may be intermittent across runs, so propensity estimates need pass^k-style repeated sampling. Test this with HVTB or ImpossibleBench across k runs.
  3. **Run attestation.** Combine BenchShield-style boundary evidence with deterministic replay and content-addressed receipts (README: AgentRunProof, YYLO, Proofline) so that a leaderboard number is independently re-checkable. This matches the README's auditability framing.
- **Feasibility:** medium; the space is crowded. **Venues:** ACL/EMNLP, NeurIPS D&B, ICLR; for attestation, security venues such as USENIX Security or CCS workshops.

### Gaps
- Full texts of HVTB and BenchShield were not read (their quantitative results were truncated in the mirrors).
- ImpossibleBench and ABC numbers come from secondary notes.
- I did not find a paper measuring hack rate as a function of the number of repeated runs; absence is not proof.

---

## Key question 3: Which Jun–Sep 2026 papers on agent consistency, reproducibility or evaluation statistics are not yet in the README?

### Takeaway
None of the papers below is in the README; this was checked by grepping README.md for each arXiv ID on 2026-09-29. The most important additions for the "Consistency and Determinism" dimension are 2609.04748, 2609.33812, 2608.22331, 2607.12338, 2609.08832, 2608.26197, 2609.06445, 2608.19760, 2606.08275, 2608.08239, 2609.24144 and 2609.15504. For evaluation integrity they are 2609.00038, 2608.11434, 2608.13564, 2608.22103 and 2609.11028. Important pre-June items missing from the README include HAL, Benz et al. (AISTATS 2026), TraceToChain, LLM-42, HiBayES, Miller, ImpossibleBench and ABC.

### Cited Findings
**June 2026**
- 2606.08275 — Causal Agent Replay (step do-interventions + re-execution; open source). [W] — [arXiv](https://arxiv.org/abs/2606.08275)
- 2606.08529 — Scaffold Effects on GAIA (pre-registered; up to 28-point scaffold effect). [S] — [notes](https://github.com/rush86999/atom/blob/6e34725c70179506515888a23c00635188f833c0/docs/architecture/AGENT_HARNESS_RESEARCH.md)
- 2606.19704 — Beyond Static Leaderboards: Predictive Validity for the Evaluation of LLM Agents. [T] — [list](https://github.com/js-lee-AI/awesome-llm-agent-papers/blob/6552bcff902193e5bd721cff1ff74efba388e8aa/README.md)
- 2606.05806 — ToolMaze (replanning and recovery when tools fail). [T] — [list](https://github.com/js-lee-AI/awesome-llm-agent-papers/blob/6552bcff902193e5bd721cff1ff74efba388e8aa/README.md)
- τ-Rec (pass^k benchmark for agentic recommenders; about 57% pass^1 vs 38% pass^4; ID not captured). [A] — [mirror](https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/5c92abb70af3796439f0e8320b2a961f56500a51/10-Jun-2026/NLP/README.md)

**July 2026**
- 2607.12338 — How Many Tasks Are Enough for Agent Benchmark Decisions? [S] — [arXiv](https://arxiv.org/abs/2607.12338)
- 2607.04528 — Measuring Harness-Induced Belief Divergence in Multi-Step LLM Agents. [T] — [list](https://github.com/js-lee-AI/awesome-llm-agent-papers/blob/6552bcff902193e5bd721cff1ff74efba388e8aa/README.md)
- 2607.22585 — The Scaffold Effect (harness-specific cost and failure fingerprints). [S] — [guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/ed932a05a44a801e5deec462e949f35f7dca0eec/guide/core/agent-harness.md)
- 2607.08010 — Tool-Making and Self-Evolving LLM Agents in Low-Latency Systems (compiled tools cut error rate by up to 53% "by suppressing run-to-run variance in repeated steps"). [A] — [mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/07/2607.08010.json)
- 2607.07946 — DeepSWE (freezes the harness across models to isolate capability). [S] — [notes](https://github.com/ruvnet/metaharness/blob/9ce8b8dd89045c3b9a1f809ae58f3589029db4a4/docs/dream-cycle/2026-08-14-gist.md)

**August 2026**
- 2608.22331 — Noise Floor Audit for Agent Benchmarks. [A]
- 2608.26197 — Harness Engineering for Predictable Agentic Systems (deterministic execution constraints; mixed effects). [A]
- 2608.19760 — Credit Without Ground Truth (executed-replay audit of step credit; CRN pairing). [W]
- 2608.08239 — The Replay Gap (live branching vs static replay; COLM 2026 workshop). [S/A]
- 2608.02005 — OASE (CRN paired comparisons of skill libraries). [W]
- 2608.22793 — TRACE / CAR-bench (Pass^3 59.9% → 94.5% on GPT-5.5 via a skill bank). [A] — [mirror](https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/5c92abb70af3796439f0e8320b2a961f56500a51/25-Aug-2026/NLP/README.md)
- 2608.24076 — AgentWorld (pass^k, snapshot + Monte-Carlo branch rollouts). [A]
- 2608.23623 — Evidence-Carrying Termination (deterministic replay certificates). [A]
- 2608.22432 — Rank Reversal in Multilingual LLM Judges. [A]
- 2608.11434 — MobileJudgeBench. [A]
- 2608.13564 — RubricForge. [A]
- 2608.22103 — Hack-Verifiable Terminal Bench. [A]
- 2608.10986 — Iterated self-feeding probes under CRN (construction vs model). [A]
- 2608.27334 — BTS-AgentBench (deterministic replayable telemetry-to-benchmark pipeline). [T]
- 2608.02645 — Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures (idempotency keys). [S] — [notes](https://github.com/rush86999/atom/blob/6e34725c70179506515888a23c00635188f833c0/docs/architecture/AGENT_HARNESS_RESEARCH.md)

**September 2026**
- 2609.04748 — Same Request, Different Answer (prefix caching × quantization divergence in agent trajectories). [A]
- 2609.33812 — Identical Runs, Different Results (584 runs; tens to 100+ runs needed). [A]
- 2609.08832 — Closing the Consistency Gap (Consistency Analyzer). [A]
- 2609.06445 — Causal Attribution for Agentic Decisions: Estimators, Coupling, Traceability. [A]
- 2609.24144 — Luck Is Not Skill (paired rollouts in group-relative RL of agents). [A]
- 2609.15504 — How Lossless Is Lossless Speculative Decoding? (BF16 trajectory mismatch). [A]
- 2609.00038 — trajectory-judge. [A]
- 2609.11028 — BenchShield. [A]
- 2609.13463 — Root-Cause Attribution Is a Search Problem. [A]
- 2609.18128 — ContrAgent (LTLf contracts). [A]
- 2609.22592 — AutoGym (verifiable gyms). [A]
- 2609.11018 — Defining AI Agents: A Compendium of Criteria, Metrics, and Benchmarks. [T] — [arXiv](https://arxiv.org/abs/2609.11018)
- Links for items without inline links are given in the sections above; the mirror path pattern is `qhduan/cn-chat-arxiv/papers/26/MM/ID.json`. — [digest repo](https://github.com/qhduan/cn-chat-arxiv/tree/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26)

**Earlier (Jan–May 2026 or 2024–2025) but also missing from the README and relevant**
- 2502.01754 Benz et al. (AISTATS 2026); 2409.17027 Chatzi et al. (CLeaR 2025); 2411.07180 Ravfogel et al. (ICLR 2025).
- 2510.11977 HAL (ICLR 2026); 2411.00640 Miller; 2505.05602 HiBayES; 2508.13144 Signal and Noise (NeurIPS 2025).
- 2604.24579 TraceToChain; 2603.23749 Efficient Benchmarking of AI Agents; 2505.05115 Ord; 2503.14499 METR.
- 2601.17768 LLM-42; 2601.20090 conformal counterfactual generation for LLM-based control; 2603.11084 event-keyed CRN; 2512.24145 paired seeds.
- 2605.23950 harness disclosure; 2605.27922 Harness-Bench; 2605.23955 determinism survey; 2605.17036 agent bullwhip; 2605.25338 CausalFlow; 2605.27249 Gumbel Machine.
- 2510.20270 ImpossibleBench; 2507.02825 ABC.
- (Sources as cited in the sections above; README absence checked locally by grep.)

### Inferences
- Jul–Sep 2026 shows a burst of measurement papers (Noise Floor, Identical Runs, How Many Tasks, prefix-cache divergence) and causal-replay papers (CAR, Credit Without Ground Truth, 2609.06445, Replay Gap). A pure measurement paper therefore has less novelty headroom than a method that exploits controlled randomness, as in 2(a).
- The README's Consistency and Determinism coverage (8 items) could roughly double using [A]-verified items from this list alone.

### Gaps
- Coverage of cs.LG/stat.ML-only papers is weaker, because the digest mirrors mostly track cs.CL/cs.AI plus cross-lists. A proper arXiv listing sweep for Jun–Sep 2026 (stat.ML, cs.SE) is still needed.
- OpenReview (ICLR 2027 submissions, NeurIPS 2026 camera-readies) could not be checked.

---

## Key question 4: Additional promising gaps, and an overall recommendation

### Takeaway
The strongest newcomer bet is **2(a), scoped tightly**: CRN / Gumbel-coupled A/B evaluation of agent configurations on seedable environments (τ-bench-style plus ALFWorld/AppWorld), with event-keyed noise and deterministic serving. It should report (i) variance reduction and its decay with horizon, (ii) the estimand distinctions exposed by 2609.06445, and (iii) an "audit-grade randomness record". It maps one-to-one onto the README's stated open gap. The fallback or companion is a crossed variance-components audit (2(b)) or a frailty-hazard model (2(c)), both cheap and statistically clean. 2(d) is a good ACL/EMNLP paper if run on TraceElephant; 2(e) is crowded.

### Cited Findings
- The README states the gap: "Reproducibility under inherent model stochasticity remains open beyond measurement and replay. Runs are still difficult to compare causally without discarding useful nondeterminism." (local README.md, "Open gaps" block) — [awesome-auditable-ai](https://github.com/yzhao062/awesome-auditable-ai)
- CRN preserves marginals, so it keeps "useful nondeterminism". Paired rollouts share noise "while preserving each rollout's marginal distribution" ([2609.24144 mirror](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.24144.json) [A]). Paired seeds recover independent evaluation when correlation is absent ([arXiv 2512.24145](https://arxiv.org/abs/2512.24145) [W]).
- Pre-registration and retraction culture is emerging in agent evaluation, a sign that reviewers will expect it:
  - a registered protocol with a disclosed pilot ([2609.24144](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.24144.json) [A])
  - a determinism study with "a retraction" ([Plumbline](https://github.com/Bhargs24/plumbline/blob/5c3005d1ae48683b9a7d7d98dc3d8a6bac98b9fb/DESIGN.md) [A])
  - "four retracted verdicts" ([2608.10986](https://github.com/CSQianDong/Awesome-arXiv-Daily-Reporter/blob/5c92abb70af3796439f0e8320b2a961f56500a51/12-Aug-2026/NLP/papers.jsonl) [A])
  - a pre-registered scaffold study ([2606.08529 notes](https://github.com/rush86999/atom/blob/6e34725c70179506515888a23c00635188f833c0/docs/architecture/AGENT_HARNESS_RESEARCH.md) [S])
- Constraining the harness can reduce reproducibility ([2608.26197](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/08/2608.26197.json) [A]). Precision and caching choices silently change agent trajectories ([2609.04748](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.04748.json); [2609.15504](https://github.com/qhduan/cn-chat-arxiv/blob/6443461bf7738879c410ba892e35b85e37d38d0f/papers/26/09/2609.15504.json) [A]).
- Single binary outcomes per task cannot separate attempt noise from task difficulty ([horizon-curve preprint](https://github.com/Atharva12081/horizon-curve-mean-not-mechanism/blob/2a769b7bafb05beebc501a0182873fea3752c69c/paper/main.tex) [A]).
- Venue evidence:
  - statistical LLM-evaluation methods accepted at AISTATS 2026 ([Benz et al. repo](https://github.com/Human-Centric-Machine-Learning/coupled-llm-evaluation) [W]) and CLeaR 2025 ([PMLR v275](https://github.com/mlresearch/v275/blob/44a2c63472bff65a4d852e179b9721d93a8cfec2/clear25.bib) [A])
  - agent-reliability metrics at ICML 2026, failure attribution at ACL 2026, agent-evaluation infrastructure at ICLR 2026 (README entries; [HAL](https://arxiv.org/abs/2510.11977) [W])
  - a KDD 2026 agentic-evaluation workshop ([notes](https://github.com/rush86999/atom/blob/6e34725c70179506515888a23c00635188f833c0/docs/architecture/AGENT_HARNESS_RESEARCH.md) [S])
  - a COLM 2026 workshop for the Replay Gap ([repo](https://github.com/AshrithaG/replay-gap/blob/670d3c062b0aac26ff6e81988cbe17f3f454757f/README.md) [A])

### Inferences
**Additional gaps I see beyond ideas (a)–(e)**
1. **Full-stack coupling.** Existing CRN work couples *one* stochastic actor: the environment (2609.24144), the opponent snapshot (2608.02005), the policy step (2609.06445), or single-turn tokens (Benz). None couples policy + user simulator + judge + environment together.
2. **Serving-configuration sensitivity as a first-class eval axis.** Prefix caching, quantization, precision, speculative decoding and batch invariance change *agent* trajectories (2609.04748, 2609.15504). A "serving-config robustness" protocol for agent benchmarks, possibly in HAL or Inspect, is missing.
3. **Useful vs harmful nondeterminism.** pass@k gains (exploration) and pass^k losses (inconsistency) are reported separately (CAR-bench: Pass@3 vs Pass^k; the 24-pp consistency gap). No framework says when to *reduce* stochasticity (deployment) and when to *couple* it (evaluation). Deterministic harnesses can backfire (2608.26197).
4. **Identifiability-aware benchmark design.** Collect ≥2 attempts per task by default so that attempt noise and task difficulty (frailty) can be separated; horizon-curve analyses currently cannot.
5. **Randomness provenance for audits.** What to log (RNG states or noise, serving configuration, environment snapshots) so a third party can re-run *counterfactuals* later. This ties to 2609.06445's traceability question and to the README's decision-record theme, and could make a strong "auditable agents" position-plus-system paper.
6. **Closed-API coupling.** Hosted models expose no noise, so coupling is impossible. Methods for quasi-pairing (shared prompts, seeds where offered, response caching) and their bias are unexplored in what I could find.

**Recommendation table** (my assessment)

| Idea | Novelty verdict (2026-09) | Newcomer feasibility (3–6 mo) | Top-venue odds | Best fit |
|---|---|---|---|---|
| (a) CRN/Gumbel-coupled agent A/B + counterfactual replay | Partially addressed; agent-trajectory token coupling for evaluation still open; crowding fast | Medium: needs sampler hacking plus deterministic serving | Highest ceiling if scoped and fast; must engage 2609.06445 | ICML/NeurIPS/ICLR; AISTATS/CLeaR |
| (b) Variance components / power / leaderboard audit | Headline message done; crossed decomposition open | High: public logs, cheap | Medium; strongest as NeurIPS D&B or combined with (a)/(c) | NeurIPS D&B, ACL/EMNLP, KDD |
| (c) Hazard + recovery (frailty) forecasting | Markov version done (TraceToChain); frailty and prospective forecasting open | High: reanalysis | Medium | ICML/NeurIPS, TMLR |
| (d) Divergence debugging via natural forks | Partially addressed (2609.08832, Amberfork, CAR) | High to medium | Medium | ACL/EMNLP, ICLR |
| (e) Integrity: judge noise, hack@k, attestation | Crowded; niches open | Medium | Medium to low unless a sharp angle | ACL/EMNLP, NeurIPS D&B, security venues |

- Suggested combined paper: "(a) + (b)". Estimate the variance components of agent A/B tests, then show which components CRN coupling removes (sampling, user simulator, environment) and which it cannot (harness, infrastructure, provider). This gives both a method and a measurement contribution and pre-empts "just another noise audit" reviews.

### Gaps
- Upcoming deadlines were not checked (ICLR 2027, ACL ARR cycles, ICML/KDD 2027); verify against official CFPs.
- Semantic Scholar citation sweeps (τ-bench 2406.12045, 2602.16666, Chatzi et al.) and an OpenReview search were blocked. A final novelty pass is needed before committing, especially for (a), given four closely related Aug–Sep 2026 papers.
- Numbers tagged [S] or [W] must be re-verified against primary sources before appearing in the final Chinese report.
