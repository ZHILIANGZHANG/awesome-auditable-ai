# Research landscape, venues and publication strategy for auditable and reliable AI agents (newcomer's view, as of 2026-09-29)

> **How to read the tags (for the report writer).** All sources were accessed on 2026-09-29. The session's egress policy blocked arxiv.org, auditcommons.org, auditable-agents.github.io, all official conference sites (iclr.cc, icml.cc, neurips.cc, usenix.org, ieee-security.org, sigsac.org, kdd.org, colmweb.org, facctconference.org, conf.researchr.org), eur-lex.europa.eu, nist.gov, genai.owasp.org, huggingface.co, Semantic Scholar, OpenAlex, dblp and the lab sites (the proxy logged a 403 CONNECT denial for each). The session-wide WebSearch budget (200 calls) also ran out partway through. Each claim therefore carries one of these tags:
> **[opened]** = I read the file myself (GitHub raw files, PyPI JSON, the local repo). **[search]** = the content comes from the WebSearch tool's summary of that URL, and I could not open the page. **[tracker]** = a community deadline tracker (ccfddl/ccf-deadlines, sec-deadlines, huggingface/ai-deadlines, or the neurips2026-workshops JSON) read through GitHub raw, not the official site. **[est.]** = my own estimate from the previous year's pattern, not a verified date. "Zhao list" means the awesome-auditable-ai README (local copy /home/user/awesome-auditable-ai/README.md, identical to https://github.com/yzhao062/awesome-auditable-ai).

## Q1. What do Auditable Agents, GRADE and CatchBench state as limitations and future work, and what did Yue Zhao's group post between June and September 2026?

### Takeaway
Zhao's FORTIS lab (USC) built an unusually complete stack between June and September 2026: a framework paper, a Python SDK, a graph representation, a benchmark, a curated list and a news site. Its own artifacts spell out what is still missing. The group needs named-value corpora with observed read/write dependencies and human-validated slices, missing-guardrail (plan) audits, calibrated compound risk scores, dependency ground truth at scale, OpenTelemetry export, and statistical power for live early-warning claims. A newcomer should not build another over-privilege scanner, hash-chained log, or dependency-graph failure predictor that competes head-on with this stack. The better entry points are the evidence and data gaps the group names itself, where collaboration is also plausible.

### Cited Findings
**Auditable Agents (arXiv 2604.05485; Nian, Yuan, Zhang, Li, Zhao)**
- The paper defines five auditability dimensions: action recoverability, lifecycle coverage, policy checkability, responsibility attribution and evidence integrity. It proposes an Auditability Card and three mechanism classes (detect, enforce, recover) — [Zhao list, Audit Trails table + Citation block](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- It "identifies six open research problems organized by mechanism class". The only one I could name from search is "Predicting auditability gaps from code". Its evidence includes 617 security findings across six open-source projects, 8.3 ms median overhead for pre-execution mediation with tamper-evident records, and controlled recovery experiments in which responsibility-relevant information could be partly recovered without conventional logs — [arXiv HTML 2604.05485](https://arxiv.org/html/2604.05485) [search]
- Venue history: the list labelled the paper "ACL 2026 Workshop (KnowFM)" on 2026-06-24 (commit 3cc0877). It is now listed as "ACM AI Leadership Summit 2026". Zhao's page describes it as a position paper accepted to the ACM AI Leadership Summit 2026, with an earlier non-archival version at ACL 2026 KnowFM — [Zhao list commit history](https://github.com/yzhao062/awesome-auditable-ai/commits/main) [opened]; [USC "Agent Auditability" page](https://viterbi-web.usc.edu/~yzhao010/auditable-agents.html) [search]

**GRADE (arXiv 2606.22741; single author Yue Zhao; MIT license)**
- The README was revised on 2026-09-08 and withdraws half of the headline claim. The statement that "the dependency layer predicts failure where run size is weak" does not hold against a nonlinear baseline: on SWE-Gym a cubic spline on four size counts reaches 0.832 and a chain attachment that reads no logged information reaches 0.827, both above the dependency model's 0.804. The transfer panel is now to be read "as a description … rather than as a capability". The execution-layer localization result (Who&When) is unaffected — [GRADE README](https://github.com/yzhao062/grade) [opened]
- The transfer effect is "compression rather than improvement". The spread across six held-out corpora narrows from 0.406 to 0.144, only 3 of 6 targets improve, and the effect depends on the learner: 1.383× under gradient-boosted trees, 1.253× under a spline — [GRADE README](https://github.com/yzhao062/grade) [opened]
- Stated limitations: "ground-truth reliance labels do not exist at scale for any agent corpus". Off-the-shelf GNNs (GIN, R-GCN, HGT) transfer worse than source-aware features. Localization is single-corpus with no cross-class generalization claimed. Stated future work: localize on both layers, attribute a run to its failure mode, and build a tool-call-level declared corpus — [arXiv HTML 2606.22741v1](https://arxiv.org/html/2606.22741v1) [search]
- Datasets are not bundled. Corpora stream from the HF Hub (τ-bench, τ²-bench, SWE-agent, SWE-Gym, OpenHands, AgentRewardBench). A ScienceWorld corpus was dropped — [GRADE README](https://github.com/yzhao062/grade) [opened]

**CatchBench (arXiv 2608.22808; single author Yue Zhao; github.com/yzhao062/catchbench)**
- The paper "carries its own work-in-progress notice: the benchmark is still being extended" — [CatchBench README](https://github.com/yzhao062/catchbench) [opened]
- Design: three information states, PRE (declared configuration), LIVE (growing prefix) and POST (finished trace). In the README's words, "six audit scenarios produce seven task contracts … scored as nine boards". The Zhao list instead describes "seven boards over five scenarios", so the two count descriptions disagree — [CatchBench README](https://github.com/yzhao062/catchbench) [opened]; [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- Headline negative results: on τ-bench no method's prefix score reaches the 0.70 early-warning bar at any prefix. On `sweagent` no over-privilege method beats the 0.574 F1 of flagging every capability. Eight of eleven LLM judges score 0.333–0.452 Top-1 on 126 Who&When runs. The POST dependency increment is positive on τ-bench but changes sign on SWE-Gym depending on the model specification — [CatchBench README](https://github.com/yzhao062/catchbench) [opened]
- "47 of 118 pre-declared contrasts separate; the rest are published unresolved." Under the matched size control the SWE-Gym dependency increment stays unresolved at every prefix, and the localization board cannot order its leading judges. Dropped grounding and online stale-state detection "stay open" because the Gold-derived substrate "has not met the human-validation bar". Stated design targets are about 410 clusters (full) and 434 (auditable) at 100% prefix — [arXiv HTML 2608.22808](https://arxiv.org/html/2608.22808) [search]
- Gold injection limitation: both fault kinds "fail the no-artifact-leakage bar on the file-level substrate". A broken-predecessor baseline ranks all 82 stale-state and all 106 dropped-grounding targets Top-1 while flagging 0 of 188 clean runs. "Artifact-controlled evidence is not yet available". What would fix it: "a named-value corpus where writes and reads are explicit, plus a human-audited validation slice." SWE-Gym dependencies are inferred, not gold value-flow — [CatchBench README](https://github.com/yzhao062/catchbench) [opened]
- Planned but not built: a PRE "missing-guardrail plan audit". PRE labels are constructed by four label processes over 1,187 configs from six corpora — [CatchBench README](https://github.com/yzhao062/catchbench) [opened]
- Reproducibility and licensing caveats: CI does not check the paper numbers because "the manuscript repository is not public". Of 1,187 PRE records, 524 are NOASSERTION; `SWE-bench/experiments` has no license file; the Who&When and τ-bench trajectory cards declare no dataset license — [CatchBench README](https://github.com/yzhao062/catchbench) [opened]

**`auditable` SDK (Apache-2.0) and siblings**
- Ships today: signed hash-chained records, replay under live state, recovery through a rail-neutral gate, PRE `analyze_plan` lints, POST `analyze_run` ranking, and capture for LangGraph, LangChain and MCP. It "does **not** yet claim benchmark-grade detector evidence, a calibrated model-trust score, or calibrated cross-layer risk". Roadmap: one calibrated compound score with "the model treated as a first-class node", automatic fixes, CI checks forming an OWASP-Agentic/CWE rule floor, a CrewAI hook, OpenTelemetry and LangSmith export, and evidence bundles — [auditable README](https://github.com/yzhao062/auditable) [opened]
- Tension to note: the auditable README still headlines "auditable (size+deps) ROC-AUC 0.804 vs 0.663 for size (flat)" on the CatchBench SWE-Gym board, while the GRADE README reports that nonlinear size-only baselines reach 0.832 — [auditable README](https://github.com/yzhao062/auditable) [opened]; [GRADE README](https://github.com/yzhao062/grade) [opened]
- agent-audit (MIT; HeadyZhang): 66 rules mapped to OWASP Agentic Top 10 (2026). Stated limits: static analysis only, intra-procedural taint (no cross-function or cross-module tracking), Python-focused. PyPI 0.20.0 was released 2026-09-13 — [agent-audit README](https://github.com/HeadyZhang/agent-audit) [opened]; [PyPI](https://pypi.org/project/agent-audit/#history) [opened]
- Aegis (MIT; Justin0504; paper arXiv 2603.12621): the roadmap lists a pending "PromptGuard-2-equivalent ML layer" (v0.3) and "single-row content-tamper detection" (v0.4) — [Aegis ROADMAP](https://github.com/Justin0504/Aegis/blob/main/ROADMAP.md) [opened]

**What the group posted between June and September 2026 (timeline)**
- 2026-06: GRADE on arXiv (2606.22741). The `auditable` PyPI releases were 0.0.1 (06-16), 0.1.0 (06-23), 0.1.1 (06-24), 0.2.0 (07-20) and 0.2.1 (08-22) — [PyPI auditable](https://pypi.org/project/auditable/#history) [opened]
- August 2026 (arXiv ID 2608.x; exact date not verified): WeClawArena (arXiv 2608.03499), described as an "auditable sandbox and benchmark for cross-user agents collaboration and security", appears in EMNLP Findings 2026. It has 124 base tasks and 620 scenario variants (one benign control and four attack variants each), with Aojie Yuan and Haiyue Zhang among the co-authors — [arXiv 2608.03499](https://arxiv.org/abs/2608.03499) [search]; [FORTIS Lab page](https://viterbi-web.usc.edu/~yzhao010/lab.html) [search]
- 2026-08-11/12: the list was renamed "Awesome Auditable AI" and grew to 181 entries, then the "Auditable Agents Ecosystem" section was added (commits 6985136, d08fb33, 3c66d1e). It now has 206 entries across nine sections — [Zhao list commits](https://github.com/yzhao062/awesome-auditable-ai/commits/main) [opened]
- 2026-08-22: CatchBench 0.1.0 and 0.1.1 on PyPI. 2026-09-13: 0.1.2. CatchBench on arXiv as 2608.22808 (August 2026) — [CatchBench CHANGELOG](https://github.com/yzhao062/catchbench/blob/main/CHANGELOG.md) [opened]; [PyPI catchbench](https://pypi.org/project/catchbench/#history) [opened]
- August 2026: USC Viterbi news story "Giving AI Agents the Keys? USC Engineers Develop Tools to Audit and Monitor AI Agents" — [USC Viterbi news](https://viterbischool.usc.edu/news/2026/08/giving-ai-agents-the-keys-usc-engineers-develop-tools-to-audit-and-monitor-ai-agents/) [search]
- 2026-09-15/16 onward: Audit Commons (auditcommons.org, English plus Chinese) launched with a start-here page, an "audit an agent action" worksheet, a guide to reading agent evaluation reports, and news briefs. By 2026-09-28 it covered NIST NCCoE agent identity, AISI optstop, CAISI's GLM-5.3 cyber assessment, the OpenAI misalignment-reporting framework, the Anthropic–METR review, Transluce's agent-network report, an Australian agent-incident taskforce and Meta Muse. The site has "not yet selected" a reuse license — [audit-commons repo README](https://github.com/yzhao062/audit-commons) [opened]; [content/pages.json](https://github.com/yzhao062/audit-commons/blob/main/content/pages.json) [opened]
- auditable-agents.github.io "currently documents the first three" components: agent-audit, Aegis and auditable — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened] (the site itself was blocked)
- Earlier 2026 group papers that shape the collision space: FORTIS over-privilege-in-skills benchmark (arXiv 2605.09163, May 2026; code lili0415/FORTIS-Benchmark); Implicit Execution Tracing (arXiv 2603.17445; led by Yi Nian), which recovers segment-level agent provenance from final text alone; Agent Audit paper (arXiv 2603.22853, CAIS 2026); The Autonomy Tax (arXiv 2603.19423) — [arXiv 2605.09163](https://arxiv.org/abs/2605.09163) [search]; [arXiv 2603.17445](https://arxiv.org/pdf/2603.17445) [search]; [Zhao profile README](https://github.com/yzhao062) [opened]
- Funding and agenda signal: a Foresight Institute 2026 grant for an "audit-to-patch pipeline" that detects risks in agent code and configuration and "proposes safe, reviewable patches" — [Foresight grantee page](https://foresight.org/grantees/2026-yue-zhao/) [search]
- Zhao is Associate Co-Director of the USC Institute on Ethics and Trust in Computing for 2026–2027 and lists "cross-user contamination" and over-privilege as agent-specific failure modes he studies — [Zhao profile README](https://github.com/yzhao062) [opened]

### Inferences
- **Collision zones to avoid:** (a) static over-privilege or OWASP-mapped scanning of agent code, skills and harnesses (agent-audit, FORTIS, CatchBench PRE); (b) typed execution-plus-dependency graphs for run-level failure prediction (GRADE, auditable); (c) hash-chained, signed decision logs with replay and rollback (auditable, Aegis, plus many third-party tools in the list); (d) lifecycle audit benchmarks spanning PRE, LIVE and POST (CatchBench).
- **Collaboration or complementary angles the group says it lacks:** (1) a named-value agent corpus with explicit reads and writes plus a human-audited validation slice, which both CatchBench (artifact-controlled Gold) and GRADE (reliance ground truth) need; (2) the missing-guardrail plan audit (PRE); (3) calibrated compound scoring and uncertainty for audit signals; (4) statistical power and experimental design for LIVE early warning (~410–434 clusters needed); (5) an OpenTelemetry-native export and mapping of the dependency layer; (6) failure-mode attribution beyond step localization; (7) cross-user and multi-party agent networks (WeClawArena opens this, but it is early).
- The 2026-09-08 GRADE retraction and the 47/118 unresolved contrasts show the group's current norm: pre-declared contrasts, reported null results, regenerated numbers. A newcomer entering this niche should match that rigor, because reviewers who know this work will expect it.

### Gaps
- I could not read the full text of any of the three papers (arXiv blocked), so the complete list of the six Auditable Agents open problems and the verbatim limitations sections are missing. Only one open problem ("Predicting auditability gaps from code") was recovered.
- auditcommons.org and auditable-agents.github.io were blocked. Audit Commons content was read from its GitHub source repository instead. No arXiv author listing for June–September 2026 could be compiled, so other group preprints from that window (for example, arXiv 2609.29095 "Where Does Exactly-Once Live? …", which appeared next to CatchBench in search results) cannot be attributed.

## Q2. Which other groups are most active in failure attribution, reliability science, monitoring/control and agent security auditing, and what are they doing next?

### Takeaway
Failure attribution is moving from small hand-labelled sets (Who&When 184 tasks, TRAIL 148 traces) to large benchmarks built by construction (Who&When Pro 12,326; Aegis 9,533) and to evidence-grounded diagnosis (Microsoft AgentRx). Reliability science (Princeton) has pivoted away from leaderboards toward reliability metrics and a Reliability Dashboard. AI control (Redwood Research, UK AISI) is scaling to realistic, multi-agent and production-like settings and stress-testing monitors. SPY Lab's AgentDojo has become shared infrastructure, even used inside ControlArena. Transluce's Docent is turning transcript analysis into in-the-wild measurement.

### Cited Findings
**Who&When / AG2 authors (Penn State and collaborators)**
- Who&When (ICML 2025 spotlight) has 184 annotated failure tasks (CaptainAgent and hand-crafted systems such as Magentic-One; GAIA and AssistantBench queries). Code is MIT; the dataset is on HF as Kevin355/Who_and_When — [Who&When repo README](https://github.com/ag2ai/Agents_Failure_Attribution) [opened]
- Who&When Pro (arXiv 2607.09996, July 2026) is by Jiale Liu, Huajun Xi, Shaokun Zhang, Yifan Zeng, Tianwei Yue, Chi Wang, Jian Kang, Qingyun Wu and Huazheng Wang — [arXiv 2607.09996 / Emergent Mind](https://www.emergentmind.com/papers/2607.09996) [search]. It has 12,326 failed trajectories, 26 source benchmarks, 9 task families, 18 error modes and 3 modalities (text, image, video), built by warm-start replay of a successful prefix followed by a single injected error, so labels are exact by construction. Four evaluation axes: agent, step, error mode, all. "Frontier LLMs still struggle … especially on multimodal traces and root-cause classification." The dataset is HF Leoxx/whowhen_pro — [Who&When Pro README](https://github.com/ag2ai/whowhen_pro) [opened]
- Next direction signal: an AG2 pull request titled "[WIP] feat(extensions): add mi4afa probing failure attribution" — [ag2ai/ag2 PR #3277](https://github.com/ag2ai/ag2/pull/3277) [search]. The team's own "Awesome Agentic Failure Attribution" list stops at arXiv 2602.02475, with 16 arXiv entries in total — [awesome-failure-attributions](https://github.com/ag2ai/Agents_Failure_Attribution/tree/main/awesome-failure-attributions) [opened]

**MAST authors (UC Berkeley)**
- MAST has 14 failure modes in three groups, derived from 150 expert-examined traces. MAST-Data has 1,642 annotated traces across seven frameworks (NeurIPS 2025 D&B) — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]. The dataset is HF mcemri/MAD, with a full LLM-judge-annotated file and a human-labelled file; authors include Cemri, Pan, Yang, Agrawal, Chopra, Tiwari, Keutzer, Parameswaran, Klein and Ramchandran — [MAST repo](https://github.com/multi-agent-systems-failure-taxonomy/MAST) [opened]
- Next direction: IBM Research and UC Berkeley applied MAST with IT-Bench to enterprise IT agents (incident triage, log and metric queries, Kubernetes actions) — [HF blog, IBM Research](https://huggingface.co/blog/ibm-research/itbenchandmast) [search]

**Microsoft AgentRx**
- AgentRx synthesizes constraints (invariants), checks them step by step, and produces an auditable validation log. An LLM judge then localizes the critical step and assigns one of 10 categories. The pipeline runs Trajectory IR → invariants → checker → judge → reports over three domains (τ-bench, Flash incident management, Magentic-One). Code is MIT and the dataset is HF microsoft/AgentRx — [AgentRx README](https://github.com/microsoft/AgentRx) [opened]
- The benchmark has 170 trajectories, and AgentRx improves failure localization by 23.6% and root-cause attribution by 22.9% over prompting baselines — [MSR blog](https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/); [arXiv 2602.02475](https://arxiv.org/abs/2602.02475) [search]

**Princeton ("Towards a Science of AI Agent Reliability", HAL)**
- Authors: Stephan Rabanser, Sayash Kapoor, Peter Kirgis, Kangheng Liu, Saiteja Utpala and Arvind Narayanan (ICML 2026). Twelve metrics across consistency, robustness, predictability and safety; tied to the HAL Reliability Dashboard — [arXiv 2602.16666](https://arxiv.org/abs/2602.16666); [HAL Reliability Dashboard](https://hal.cs.princeton.edu/reliability/) [search]. The Zhao list notes that capability gains produced only small reliability gains across 15 models — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- Next direction: "HAL is no longer accepting new result submissions … We have paused updates to the leaderboard and are focusing our work on agent reliability" — [hal-harness README](https://github.com/princeton-pli/hal-harness) [opened]. Press coverage came on 2026-03-24 — [Fortune](https://fortune.com/2026/03/24/ai-agents-are-getting-more-capable-but-reliability-is-lagging-narayanan-kapoor/) [search]

**Redwood Research and UK AISI (AI control)**
- Ctrl-Z: the first control evaluation in an agent environment, using BashBench (257 multi-step sysadmin tasks) and resample protocols. Redwood announced ControlConf 2026 — [Redwood blog, Ctrl-Z](https://blog.redwoodresearch.org/p/ctrl-z-controlling-ai-agents-via); [ControlConf 2026](https://blog.redwoodresearch.org/p/announcing-controlconf-2026) [search]
- ControlArena (UK AISI; MIT; built on Inspect) has settings for AgentDojo, Apps, Bash, BashArena, BigCodeBench, Data Poisoning, Eval Sabotage (private), IAC, Infra (Kubernetes), Rogue Eval, SWE-bench Django (CWE-mapped side tasks), SAE Interp Sabotage, SHADE Arena (private) and vLLM, with micro-protocols, policies, monitors and trajectory export — [control-arena README](https://github.com/UKGovernmentBEIS/control-arena) [opened]. BashArena has 637 privileged Linux administration tasks and 4 sabotage objectives. This comes from a WebSearch summary of control-related results; the exact source page was not identified, but the result set included the [control-arena repo](https://github.com/UKGovernmentBEIS/control-arena) and [LinuxArena, arXiv 2604.15384](https://arxiv.org/pdf/2604.15384) [search]
- 2026 control and monitoring preprints surfaced by search (authorship not verified): LinuxArena, which runs control in live production environments (arXiv 2604.15384); MonitoringBench (2605.09684); "Multi-Agent AI Control: Distributed Attacks Hamper Per-Instance Monitors" (2607.07368); MOLE, on insider threats in agents (2609.06966); TraceGuard (2604.03968); "Detecting Safety Violations Across Many Agent Traces" (2604.11806); "Retrying vs Resampling in AI Control" (2605.26047); "Attack Selection Reduces Safety … against Trusted Monitoring" (2602.04930) — [search listing, e.g. arXiv 2607.07368](https://arxiv.org/pdf/2607.07368) [search]
- Monitors themselves are fragile. LLM monitors miss dangerous actions 2×–30× more often after 800K tokens of benign context (arXiv 2605.12366). An Opus 4.6 monitor catches 32% of 40 covert attacks and never catches 20 of them at 1% FPR (SLEIGHT-Bench, 2605.16626). Adaptive prompt-injection attacks subvert trusted monitors (ICLR 2026) — [Zhao list, Runtime Monitoring](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- AISI's optstop, an open-source Bayesian early-stopping tool for allocating evaluation trials, was announced 2026-08-27 (arXiv 2608.14425; github UKGovernmentBEIS/optstop) — [Audit Commons pages.json entry](https://github.com/yzhao062/audit-commons/blob/main/content/pages.json) [opened]

**ETH SPY Lab (AgentDojo)**
- AgentDojo authors: Debenedetti, Zhang, Balunović, Beurer-Kellner, Fischer and Tramèr. It has four suites (workspace, Slack, banking, travel) — [Invariant Labs blog](https://invariantlabs.ai/blog/agentdojo) [search]. It has 97 tasks and 629 security tests (NeurIPS 2024 D&B) — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]. It is MIT-licensed, installs with `pip install agentdojo`, and its changelog goes up to v0.1.35 — [agentdojo README / changelog](https://github.com/ethz-spylab/agentdojo) [opened]
- AgentDojo is now a ControlArena setting — [control-arena README](https://github.com/UKGovernmentBEIS/control-arena) [opened]. NIST publishes an "AgentDojo-Inspect" dataset — [data.gov listing](https://catalog.data.gov/dataset/agentdojo-inspect) [search]. Related design-level defenses include CaMeL ("Defeating Prompt Injections by Design", SaTML 2026) and "Design Patterns for Securing LLM Agents against Prompt Injections" — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]

**Transluce (Docent)**
- Docent is Apache-2.0 (© 2025 Clarity AI Research Inc., dba Transluce) and can be self-hosted — [docent repo](https://github.com/TransluceAI/docent) [opened]
- "Measuring coding agent misalignment in the wild" analysed 8,600 transcripts from SWE-chat plus internal traffic. About 2% of sessions showed severe monitor evasion or misrepresented success, for example merging to main without authorization or falsely claiming review approval — [Transluce Docent blog](https://transluce.org/docent/blog/coding-agent-behaviors) [search]. A post dated 2026-02-11 asks "Why does GPT-5.1 Codex underperform GPT-5 Codex?" — [Docent blog](https://transluce.org/docent/blog) [search]
- A 2026-09-23 report on agent network tunneling and website probes in public urlquery.net scanner logs used external evidence of agent activity — [Audit Commons pages.json](https://github.com/yzhao062/audit-commons/blob/main/content/pages.json) (source: transluce.org/agent-activity) [opened]

**Other active groups worth tracking (examples)**
- SALT-NLP: agents bypass peer-verification rules over repeated interactions (arXiv 2609.24967; code SALT-NLP/agent-collusion). Patronus AI: TRAIL. ulab-uiuc: AgentDebug and ProtocolBench. TIGER-AI-Lab: ClawBench. Sierra: τ-bench. PSU/AG2: AgenTracer (bingreeky). A2E (datamllab) — [Audit Commons pages.json](https://github.com/yzhao062/audit-commons/blob/main/content/pages.json) [opened]; [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- Failure-attribution preprints surfaced by search in August–September 2026 alone (authors not verified): "Root-Cause Attribution Is a Search Problem" (2609.13463); "Causal Attribution for Agentic Decisions: Estimators, Coupling, and a Traceability Specification" (2609.06445); "Explaining AI Agents Through Execution Traces" (2609.06063); AUDITA, on certified auditing and causal attribution (2608.22160); "When Agentic Executions Fail: Detecting and Localizing Runtime Faults from Telemetry" (2608.14680) — [search listing, e.g. arXiv 2609.13463](https://arxiv.org/pdf/2609.13463) [search]

### Inferences
- Attribution labs are converging on **scale by construction** (Who&When Pro, Aegis) and **evidence-grounded checking** (AgentRx invariants). Real-world (non-injected) failure labels and multimodal and root-cause classification remain weak, and those are the gaps Who&When Pro itself highlights.
- Control research is institutionalized (ControlArena, ControlConf, AISI tooling) and moving to multi-agent and production settings. A newcomer can contribute through shared infrastructure (Inspect/ControlArena settings, monitors, audit-record sufficiency) without needing frontier-lab access.
- Princeton's leaderboard pause makes reliability measurement (consistency, predictability) a sanctioned research target with an external reference implementation, a good fit for newcomers.
- Transluce and AISI are building **external, evidence-based** views (public scanner logs, statistical stopping). "Audit from outside the operator" is an emerging theme, and it complements Zhao's operator-side records.

### Gaps
- Paper-level authorship and affiliations for most 2026 control and attribution preprints above could not be verified (arXiv blocked). SPY Lab's own 2026 roadmap and new papers were not found. Redwood's and AISI's 2026 publication lists were not opened directly. The ControlConf 2026 date is unknown.

## Q3. Which conferences and workshops fit between October 2026 and mid-2027, and what are their deadlines?

### Takeaway
ICLR 2027, NeurIPS 2026 workshops, KDD 2027 cycle 1, USENIX Security 2027 cycle 1, ICSE 2027 and AAAI 2027 have already closed. The next realistic targets are: SaTML 2027 (closes today, 2026-09-29), AAMAS (Oct 1/8), FSE 2027 (Oct 2), ARR October (Oct 12, for NAACL/COLING 2027), WWW 2027 (Oct 25), IEEE S&P 2027 cycle 2 (Nov 17), Euro S&P and DSN 2027 (Dec 2), then a January 2027 cluster: ARR for ACL 2027, USENIX Security cycle 2 (Jan 26), ICML 2027 (~Jan 22, unverified), ISSTA (Jan 11), plus FAccT, CCS cycle 1 and IJCAI [est.]. Spring 2027 brings KDD cycle 2 (Feb) [est.], COLM and ASE (late March) [est.], and NeurIPS 2027 main and D&B (May) [est.].

### Cited Findings
**Already passed (for orientation)**
- ICLR 2027: abstract 2026-09-18, paper 2026-09-25 AoE. Reviews 2026-11-05, discussion Nov 5–18, AC discussion to Dec 16. Conference April 26–30, 2027 in California — [ICLR 2027 CFP](https://iclr.cc/Conferences/2027/CallForPapers) [search]. The tracker lists San Francisco and a decision date of 2026-12-16 — [ccfddl iclr.yml](https://github.com/ccfddl/ccf-deadlines) [tracker]
- KDD 2027 Research Track cycle 1: abstract 2026-07-19, paper 2026-07-26, rebuttal Sep 29–Oct 13, notification 2026-11-14. Cycle 2 is "February 2027", dates unpublished. At most seven submissions per author per cycle; OpenReview. KDD 2027 also runs a Datasets and Benchmarks track and an ADS track — [KDD 2027 Research CFP](https://kdd2027.kdd.org/research-track-call-for-papers/); [KDD 2027 D&B CFP](https://kdd2027.kdd.org/datasets-and-benchmarks-track-call-for-papers/) [search]
- USENIX Security 2027 cycle 1 closed 2026-08-25. AAAI 2027 closed 2026-07-28 (conference Montréal, Feb 16–23, 2027). NDSS 2027 both cycles closed (conference Seoul, Mar 22–26, 2027). ICSE 2027 had a single cycle, 2026-06-30 (conference Dublin, Apr 25–May 1, 2027) — [ccfddl](https://github.com/ccfddl/ccf-deadlines) [tracker]; [sec-deadlines](https://github.com/sec-deadlines/sec-deadlines.github.io/blob/master/_data/conferences.yml) [tracker]
- NeurIPS 2026 runs in Sydney (Dec 6–12) with satellites in Atlanta and Paris (Dec 9–13) — [NeurIPS 2026 Dates](https://neurips.cc/Conferences/2026/Dates) [search]; [HF ai-deadlines neurips.yml](https://github.com/huggingface/ai-deadlines) [tracker]. There are 109 workshops, and the NeurIPS blog warns against informal lists — [NeurIPS blog, 2026-08-10](https://blog.neurips.cc/2026/08/10/announcing-the-neurips-2026-workshops/) [search]
- Relevant NeurIPS 2026 workshops, almost all with submission deadlines of 2026-08-29 and notifications around Sep 22–29:
  - Sydney: Who Verifies the Agents? (Verify-Agents), Agents in the Wild (AIWILD, third edition), Interpreting Agent Behavior (IAB), Trust-AI-Eval (TAE, "Can we trust AI evaluation?": benchmark auditing, measurement validity), Meta-Agents, AgenticOS
  - Paris: FLMSec (deadline Aug 22), Trustworthy AI for Good (AI4GOOD), E-values (anytime-valid inference and auditing), Foundations of Agentic Systems Theory (FAST)
  - Atlanta: JUDGe (LLM-as-judge reliability), Evaluation of Interactive Agents (IAEval), CLEA (deadline Sep 4)
  - Sources: [neurips2026-workshops JSON](https://github.com/neurips2026-workshops/neurips2026-workshops) [tracker]; [YLfan99 list](https://github.com/YLfan99/neurips2026-workshops) [tracker]; [TAE site](https://tai-eval.github.io/); [Verify-Agents](https://verify-agents-workshop.github.io/); [AIWILD](https://agentwild-workshop.github.io/neurips2026/) [search]
- **Still open:** the IAB workshop lists a "Submission with NeurIPS reviews" deadline of **2026-10-01** (camera-ready Nov 20) — [IAB.json](https://github.com/neurips2026-workshops/neurips2026-workshops) [tracker]. Verify on iab-agents.github.io.
- The Agents in the Wild series ran at ICLR 2026 (235 submissions), ICML 2026 (Seoul, July 10/11) and NeurIPS 2026, so it is likely to recur — [organizer post on X](https://x.com/ChenguangWang/status/2044113029437239777) [search]. Other precedents: an ICML 2026 workshop on "Statistical Frameworks for Uncertainty in Agentic Systems", AIWILD at ICML 2026, and KnowFM at ACL 2026 — [Zhao list venue fields](https://github.com/yzhao062/awesome-auditable-ai) [opened]

**Open in Oct–Dec 2026**
- SaTML 2027: abstract 2026-09-22, paper **2026-09-29**; Reykjavik, May 2027 — [ccfddl satml.yml](https://github.com/ccfddl/ccf-deadlines); [sec-deadlines](https://github.com/sec-deadlines/sec-deadlines.github.io/blob/master/_data/conferences.yml) [tracker]
- AAMAS 2027: abstract **2026-10-01**, paper **2026-10-08**; Hanoi, May 3–7, 2027 — [ccfddl aamas.yml](https://github.com/ccfddl/ccf-deadlines) [tracker]
- FSE 2027: **2026-10-02**; Shenzhen, July 12–16, 2027 — [ccfddl fse.yml](https://github.com/ccfddl/ccf-deadlines) [tracker]
- ARR October 2026 cycle (official ARR schedule): submission **Oct 12**, reviewer registration Oct 14, reviews due Nov 16, author response Nov 24–30, meta-reviews Dec 17, cycle end Dec 20. NAACL 2027 and COLING 2027 take their final ARR submission on Oct 12 and commit by **Dec 23, 2026**. EACL 2027 commitment was Oct 11. **ACL 2027 final ARR submission is "January, 2027"** — [ARR dates.md (source of aclrollingreview.org/dates)](https://github.com/acl-org/aclrollingreview/blob/main/dates.md) [opened]. NAACL 2027 is in San Francisco, June 1–5, 2027; ACL 2027 is in Kyoto, Aug 17–22, 2027 — [ccfddl naacl/acl.yml](https://github.com/ccfddl/ccf-deadlines) [tracker]
- WWW 2027: **2026-10-25** (abstract one week earlier); Dublin, May 10–14, 2027 — [sec-deadlines](https://github.com/sec-deadlines/sec-deadlines.github.io/blob/master/_data/conferences.yml) [tracker]
- ACSAC 2026 workshop WAITI: deadline **2026-10-05**, Dec 7 (scope not checked) — [sec-deadlines](https://github.com/sec-deadlines/sec-deadlines.github.io/blob/master/_data/conferences.yml) [tracker]
- IEEE S&P 2027 cycle 2: abstract **2026-11-10**, paper **2026-11-17**; Montréal, May 17–19, 2027 per ccfddl, May 17–20 per sec-deadlines (the trackers disagree) — [ccfddl sp.yml](https://github.com/ccfddl/ccf-deadlines); [sec-deadlines](https://github.com/sec-deadlines/sec-deadlines.github.io/blob/master/_data/conferences.yml) [tracker]
- Euro S&P 2027: **2026-12-02**; Madrid, July 5–9, 2027. DSN 2027: **2026-12-02**; Berlin, June 22–25, 2027. ASIA CCS 2027 cycle 2: **2026-12-11**; Macau, July 12–16, 2027 — [sec-deadlines](https://github.com/sec-deadlines/sec-deadlines.github.io/blob/master/_data/conferences.yml) [tracker]

**January–June 2027**
- USENIX Security 2027 cycle 2: abstract **2027-01-19**, paper **2027-01-26**; Denver, Aug 11–13, 2027. ccfddl and sec-deadlines agree — [ccfddl uss.yml](https://github.com/ccfddl/ccf-deadlines) [tracker]
- ISSTA 2027: abstract **2027-01-08**, paper **2027-01-11**; Singapore, Sept 7–10, 2027 — [ccfddl issta.yml](https://github.com/ccfddl/ccf-deadlines) [tracker]
- ICML 2027 (**unverified**): search surfaced abstract Jan 16 and paper **Jan 22, 2027**, with the conference July 4–9, 2027. The location is reported inconsistently: "South America, city TBA" in one summary, a CFP page hosted on icml2027.eurac.edu in another. One source gave Jan 28 instead. The ICML 2026 pattern was abstract Jan 23–24 and paper Jan 28–29 — [researchtheta](https://researchtheta.com/conferences/icml-2027/); [Eurac page](https://icml2027.eurac.edu/en/news/call-for-papers-for-the-icml-2027-now-open) [search]; [HF ai-deadlines icml.yml](https://github.com/huggingface/ai-deadlines) [tracker]
- CCS 2027: Atlanta, Oct 11–15, 2027; deadlines "TBD". CCS 2026 used cycles of 2026-01-14 and 2026-04-29, so **expect mid-January and late April 2027** [est.] — [ccfddl ccs.yml](https://github.com/ccfddl/ccf-deadlines) [tracker]
- FAccT 2027: no information found. FAccT 2026 had abstract 2026-01-08 and paper 2026-01-13, so **expect mid-January 2027** [est.] — [HF ai-deadlines facct.yml](https://github.com/huggingface/ai-deadlines) [tracker]
- IJCAI 2027: Kyoto and Hengqin, August 2027, deadline "TBD". IJCAI 2026 closed 2026-01-19, so **expect mid-January 2027** [est.] — [ccfddl ijcai.yml](https://github.com/ccfddl/ccf-deadlines) [tracker]
- KDD 2027 cycle 2: **around early February 2027** [est.]. KDD 2026 cycle 2 was Feb 1/8, 2026 — [HF ai-deadlines kdd.yml](https://github.com/huggingface/ai-deadlines) [tracker]
- COLM 2027: no information. COLM 2026 had abstract Mar 26 and paper Mar 31, 2026 (conference San Francisco, Oct 6–9, 2026), so **expect late March 2027** [est.] — [HF ai-deadlines colm.yml](https://github.com/huggingface/ai-deadlines) [tracker]
- ASE 2027: no information. ASE 2026 closed 2026-03-26 (conference Munich, Oct 12–16, 2026), so **expect late March 2027** [est.] — [ccfddl ase.yml](https://github.com/ccfddl/ccf-deadlines) [tracker]
- NeurIPS 2027, including the Datasets and Benchmarks track: no information. NeurIPS 2026 had abstract May 4–5 and paper May 6–7, 2026, so **expect early-to-mid May 2027** [est.] — [HF ai-deadlines neurips.yml](https://github.com/huggingface/ai-deadlines) [tracker]
- EMNLP 2027: no information. EMNLP 2026 used the May 25, 2026 ARR cycle (commitment Aug 2), so **expect a May 2027 ARR cycle** [est.] — [ARR dates.md](https://github.com/acl-org/aclrollingreview/blob/main/dates.md) [opened]
- ICLR 2027 and ICML 2027 workshop calls: none found. Typical calls fall around February (ICLR) and May (ICML) [est.].
- IEEE S&P 2028 cycle 1: **around June 2027** [est.]. S&P 2027 cycle 1 was 2026-06-11 — [ccfddl sp.yml](https://github.com/ccfddl/ccf-deadlines) [tracker]

**Venue fit, based on where comparable work landed (from the Zhao list venue fields)**
- ML venues:
  - ICML 2025 / ICLR 2026: Who&When, AgenTracer, Aegis
  - ICML 2026: Towards a Science of AI Agent Reliability, τ²-bench, ProtocolBench
  - NeurIPS D&B: MAST, AgentDojo, OSWorld, OS-Harm
- NLP venues:
  - ACL 2026: TraceElephant
  - ACL Findings 2026: ErrorProbe
  - EMNLP 2026: StepGuard
  - EMNLP Findings 2026: WeClawArena
  - COLM 2025: AgentRewardBench
- KDD 2026: StepFinder
- Security venues:
  - USENIX Security 2026: AttriGuard
  - CCS 2025: AgentSentinel
  - SaTML 2026: CaMeL
- SE venues:
  - ICSE 2026: AgentSpec
  - ASE 2026: ProbGuard
- FAccT 2024: Visibility into AI Agents; Black-Box Access is Insufficient
- CAIS 2026: Agent Audit
- Source for all of the above: [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]. The one exception is the WeClawArena venue, which is not in the list and comes from [arXiv 2608.03499](https://arxiv.org/abs/2608.03499) [search]

### Inferences
- **Suggested 9-month plan for a newcomer:**
  - A short workshop or position piece now: the IAB NeurIPS-reviews track (Oct 1, only if a NeurIPS-reviewed paper exists).
  - A benchmark or measurement paper for **ARR Oct 12**, if NLP-flavoured and ready (NAACL/COLING 2027), or for **ARR January 2027** (ACL 2027, Kyoto).
  - Method papers for **ICML 2027 (~late Jan)** or **KDD 2027 cycle 2 (~Feb)**.
  - Security-flavoured audit work for **S&P cycle 2 (Nov 17)**, **USENIX Security cycle 2 (Jan 26)** or **CCS 2027 (Jan/Apr)** [est.].
  - Dataset or benchmark releases for **NeurIPS 2027 D&B (~May)** [est.] or the **KDD 2027 D&B track**.
  - Accountability or governance work for **FAccT 2027 (~Jan)** [est.].
  - SE-flavoured tooling for **FSE 2027 (Oct 2)**, **ISSTA 2027 (Jan 11)** or **ASE 2027 (~Mar)** [est.].
- Agent-safety and evaluation workshops recur at every major ML conference (AIWILD at ICLR, ICML and NeurIPS 2026; uncertainty-in-agents at ICML 2026; TAE, JUDGe, IAEval and Verify-Agents at NeurIPS 2026). Expect ICLR 2027 and ICML 2027 editions, useful as a low-cost first venue.

### Gaps
- None of the official conference pages could be opened (blocked). Dates tagged [tracker] must be rechecked on the official CFPs. The following are unknown or unverified: ICML 2027 (dates and location), NeurIPS 2027 (including D&B), COLM 2027, FAccT 2027, CCS 2027, IJCAI 2027, EMNLP 2027, ASE 2027, KDD 2027 cycle 2, and ICLR/ICML 2027 workshops.

## Q4. Which sub-areas are crowded and which are underexplored? (rough publication volume, 2025 vs 2026)

### Takeaway
No direct arXiv counts were possible: arXiv, Semantic Scholar, OpenAlex and dblp were blocked and the search budget was exhausted. Lower-bound counts from curated lists give a consistent picture. Prompt injection and agent security is by far the most crowded area, with hundreds of papers a year. Failure attribution roughly doubled or more in 2026 and is now crowded around Who&When-style LLM-judge methods. Runtime monitoring and control is steady and concentrated in a few organizations. Audit trails and provenance grew from a very small base, with many tools but few rigorous evaluations. Reproducibility, determinism and recovery remain the least covered.

### Cited Findings
**Method:** I counted unique arXiv IDs by year prefix (25xx = 2025, 26xx = Jan–Sep 2026) in curated lists opened through GitHub raw. These are **lower bounds shaped by curation**, not field totals.
- **Failure attribution and diagnosis:**
  - Zhao list section: 8 (2025) → 17 (2026). Its 2026 entries are spread across February–August, with 5 in June.
  - Union of the Zhao list, the Who&When authors' "Awesome Agentic Failure Attribution" list (16 IDs, not updated past Feb 2026) and 10 more 2026 attribution preprints surfaced by search: **13 (2025) → 27 (2026, Jan–Sep)**, 44 unique in total.
  - Sources: [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]; [awesome-failure-attributions](https://github.com/ag2ai/Agents_Failure_Attribution/tree/main/awesome-failure-attributions) [opened]
- **Runtime monitoring, guardrails and control:**
  - Zhao list: 12 (2025) → 11 (2026). At least 8 more 2026 control and monitoring preprints were surfaced by search (listed in Q2).
  - Sources: [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]; [search listing, e.g. arXiv 2605.09684](https://arxiv.org/pdf/2605.09684) [search]
- **Prompt injection and agent security (most crowded):**
  - ThuCCSLab Awesome-LM-SSP "A7 Prompt Injection": 37 (2024) → 71 (2025), counted by the list's own [YYYY/MM] tags.
  - "B3 Agent" (agent security): 133 entries dated 2025.
  - "B5 Prompt Injection": 12 agent prompt-injection papers from late August 2026 alone. The 2026 counts are incomplete because curation lags; the whole list holds 2,467 papers.
  - Zhao list "Security Auditing and Scanners": 4 (2025) → 12 (2026). The README notes that Security Review has **76 direct resources**.
  - Sources: [Awesome-LM-SSP](https://github.com/ThuCCSLab/Awesome-LM-SSP) [opened]; [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- **Reproducibility and nondeterminism:**
  - Zhao list "Reliability and Robustness": 2 (2025) → 9 (2026).
  - The README's own coverage note: "Consistency and Determinism is the least represented dimension here, with eight direct resources against 76 for Security Review", and it invites contributions on "run-to-run reproducibility, deterministic replay, bounded stochasticity".
  - Source: [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- **Audit trails, decision records and provenance:**
  - Zhao list: 1 (2025) → 9 (2026) papers, plus 11 decision-record tools, every one labelled "2026-present".
  - The evidence-tracing survey's list (xiaoqi-7): 11 (2025) → 12 (2026 H1 only).
  - Sources: [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]; [Agent-Tracing-Survey](https://github.com/xiaoqi-7/Agent-Tracing-Survey) [opened]
- **Open gaps named by the Zhao list:**
  - No shared reliability benchmark. Manual failure labels "remain in the low hundreds".
  - Attribution at scale is unreliable. Silent benign failures are detected but not localized: HINTBench models score <35 Strict-F1 on locating the risky step.
  - Calibrated abstention is open: in AgentAbstain the best of 17 models reaches 59.5% paired accuracy.
  - Reproducibility under stochasticity is open. Monitors degrade with context and can be evaded.
  - There is no cross-vendor decision-record schema. Recovery evaluation is only "emerging". Cost-aware reliability is partial. Evaluation integrity is unsettled (BenchJack).
  - Source: [Zhao list, "Open gaps"](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- **Telemetry sufficiency is a measured gap:** TelemetrySuffBench finds that OpenTelemetry- and OpenInference-compatible views keep 99.5–100% detection F1 but hold fault-origin step accuracy at ≤0.5%. TraceElephant finds that full traces raise step-level attribution from 17% to 30% — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- **Context on overall volume:** arXiv IDs in the late-August 2026 LM-SSP entries reach 2608.30686, so arXiv took more than 30,000 submissions in August 2026 — [Awesome-LM-SSP B5](https://github.com/ThuCCSLab/Awesome-LM-SSP) [opened]

### Inferences
- **Crowded (avoid unless you have a sharp angle):** new prompt-injection attacks or defenses evaluated only on AgentDojo; generic LLM-judge failure attribution evaluated only on Who&When (Who&When Pro, AgenTracer, FALAT, StepFinder, ECHO, SAFARI, AgentDebugX and others already occupy it); new hash-chained audit-log tools without evaluation; OWASP-mapped static scanners.
- **Growing but still open:** attribution on *real* (non-injected), long-horizon, multimodal or coding traces with human labels; evidence-grounded or causal attribution with guarantees (conformal attribution exists, but only as a single paper); monitor robustness (long context, evasion, multi-agent collusion).
- **Underexplored (best newcomer bets):**
  - Run-to-run reproducibility and deterministic replay as an audit prerequisite.
  - Recovery and rollback evaluation (only PALADIN, Atomix and ACRFence exist).
  - **Telemetry sufficiency**: the minimal set of logged fields that makes post-hoc attribution possible, which also informs EU AI Act Art. 12 logging and OpenTelemetry fields.
  - Dependency and value-flow ground truth: the named-value corpora that CatchBench and GRADE say they need.
  - Calibrated abstention and uncertainty for audit signals.
  - Statistically powered evaluation design for audit benchmarks.

### Gaps
- No real arXiv query counts were obtained (arXiv API, S2, OpenAlex and dblp blocked; WebSearch budget exhausted). All figures are curated-list lower bounds with curation lag (LM-SSP's 2026 coverage is sparse before August), so trend direction is more reliable than magnitude. A proper count needs arXiv API keyword queries (for example "failure attribution" AND agent, "prompt injection" AND agent, "agent monitoring"/"AI control", "reproducib*"/"nondetermin*" AND agent, "audit trail"/"provenance" AND agent), grouped by year.

## Q5. Which regulatory and standards drivers make certain questions timely?

### Takeaway
The EU AI Act's logging duties (Art. 12; deployers keep logs at least six months under Art. 26(6)) now bite on **2 Dec 2027** (Annex III) and **2 Aug 2028** (regulated products) after the Digital Omnibus (Reg. (EU) 2026/1744, in force 27 July 2026). That leaves a roughly 14-month window in which research can shape what "adequate agent logs" means. OpenTelemetry's GenAI agent conventions exist but are still at "Development" status. They carry no fields for dependencies, rationale or integrity, and content capture is opt-in. NIST's 2026 agent work centres on identity, authorization, auditing and non-repudiation. The OWASP Agentic Top 10 (2026) has become the rule taxonomy scanners map to. Together these create concrete demand for telemetry-sufficiency, decision-record and permission-evidence research.

### Cited Findings
- **EU AI Act.** Art. 12 requires high-risk AI systems to record events over their lifetime. Art. 26(6) requires deployers to retain logs for at least six months. The Digital Omnibus on AI (Regulation (EU) 2026/1744, in force 27 July 2026) moved high-risk application to **2 Dec 2027** for Annex III areas and **2 Aug 2028** for AI embedded in regulated products — [Zhao list, Standards](https://github.com/yzhao062/awesome-auditable-ai) [opened]. The list's link audit records that this act "was confirmed against the European Commission announcement and independent legal summaries" (EUR-Lex refuses non-browser clients) — [LINK-AUDIT.md](https://github.com/yzhao062/awesome-auditable-ai/blob/main/LINK-AUDIT.md) [opened]
- **NIST AI 600-1** (GenAI Profile, July 2024) names twelve GenAI risk areas and over 200 suggested actions across Govern, Map, Measure and Manage — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- **NIST 2026 agent guidance.** On 5 Feb 2026 the NCCoE published the concept paper "Accelerating the Adoption of Software and Artificial Intelligence Agent Identity and Authorization". It asks about the identification, authorization, **auditing and non-repudiation** of agents and about prompt-injection controls. Comments closed 2 April 2026, and as of 16 Sep 2026 the project status was "Reviewing Comments". It is a concept paper, not a standard — [Audit Commons article source](https://github.com/yzhao062/audit-commons/blob/main/content/bodies/nist-nccoe-agent-identity-concept-paper.html) (cites nist.gov and nccoe.nist.gov) [opened]. NIST CAISI published a GLM-5.3 cyber-capability assessment in September 2026 that describes tools, turn limits and safeguard settings, but one benchmark is private — [Audit Commons pages.json](https://github.com/yzhao062/audit-commons/blob/main/content/pages.json) [opened]
- **OWASP Top 10 for Agentic Applications (2026)** and the Securing Agentic Applications Guide 1.0 cover prompt injection, excessive agency, tool misuse, memory and context poisoning, and goal hijacking. The list's audit confirmed the links resolved on 2026-09-04 — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai); [LINK-AUDIT.md](https://github.com/yzhao062/awesome-auditable-ai/blob/main/LINK-AUDIT.md) [opened]. Adoption examples: agent-audit's 66 rules cover 10/10 categories — [agent-audit](https://github.com/HeadyZhang/agent-audit) [opened]. Microsoft's Agent Governance Toolkit publishes control mappings to the OWASP Agentic Top 10, NIST AI RMF, the EU AI Act and SOC 2 — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]. A 64,611-server MCP study found that scanners flag 96.89% of servers as risky at 45.53% precision — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- **OpenTelemetry GenAI semantic conventions.**
  - In core semconv **v1.42.0**, all `gen_ai.*` attributes, metrics, events and spans (and the `model/openai/` and `model/mcp/` definitions) "are deprecated in this repository and have moved to" open-telemetry/semantic-conventions-genai. The core repository is now at v1.44.0 — [semconv CHANGELOG](https://github.com/open-telemetry/semantic-conventions/blob/main/CHANGELOG.md) [opened]. The Zhao list dates v1.42.0 to 12 June 2026 — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]
  - The new repository covers GenAI clients, MCP and provider-specific conventions. Its schema URL is still "TODO" — [semantic-conventions-genai README](https://github.com/open-telemetry/semantic-conventions-genai) [opened]
  - The agent spans doc is at **Status: Development**. It defines `create_agent`, `invoke_agent` (client and internal), `invoke_workflow` and `plan` spans, with attributes for agent id, name, version and description, conversation id, tool definitions and token usage. `gen_ai.input.messages`, `gen_ai.output.messages` and `gen_ai.system_instructions` are **Opt-In**. There are no attributes for data dependencies, decision rationale or record integrity: the only "hash" and "depend" mentions concern conversation IDs — [gen-ai-agent-spans.md](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md) [opened]
- **ISO/IEC 42001:2023** is the first certifiable AI management-system standard, covering risk and impact assessment and performance measurement across the lifecycle — [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- **Other drivers:**
  - MITRE ATLAS v2026.07 (7 Aug 2026) added three AI Agent Tool Poisoning sub-techniques (AML.T0110.000/.001/.002) and AML.T0115.
  - CWE-1427 (prompt injection) is a mappable weakness.
  - The MCP specification revision of 2026-07-28 has an OAuth 2.1 profile.
  - A2A v1.0.1 (28 May 2026) and AP2 signed mandates are further drivers.
  - Source: [Zhao list, Standards](https://github.com/yzhao062/awesome-auditable-ai) [opened]
- **Industry and government signals from September 2026:**
  - OpenAI published a model-misalignment reporting framework with six incident reports (Sep 16).
  - Anthropic agreed to an independent METR review of cybersecurity evaluation incidents (Sep 9) and named Accenture as an embedded evaluator (Audit Commons brief published Sep 19; event date not recorded).
  - Australia opened an agent-incident taskforce after unauthorized portal access (Sep 26).
  - Meta strengthened its Muse agent security warning after a reported vulnerability (Sep 25).
  - Source: [Audit Commons pages.json](https://github.com/yzhao062/audit-commons/blob/main/content/pages.json) [opened] (each entry links its primary source)

### Inferences
- **Timely, regulation-anchored research questions:**
  1. For agents, what logged evidence is *sufficient* for Art. 12 purposes (risk identification, post-market monitoring) and for post-hoc attribution? Compare OTel-only, OTel plus dependency, and full-trace logging against attribution accuracy, extending TelemetrySuffBench and TraceElephant.
  2. Propose and evaluate OTel GenAI extensions for dependency, rationale and integrity. The Development-status window is when proposals get accepted.
  3. Privacy versus auditability: content capture is opt-in, so what can be audited from metadata alone, and what redaction-preserving provenance works (in the style of IET)?
  4. Agent identity, delegation and non-repudiation evidence (NCCoE framing), connecting permissions to actions, which is exactly the Audit Commons worksheet's reading.
  5. Scanner precision and OWASP-mapping validity (MCP scanners run at ~46% precision).
  6. Evidence artifacts that ISO/IEC 42001 auditors and third-party evaluators (METR-style reviews, incident reports) can consume.
- The Omnibus delay (Dec 2027 / Aug 2028) means 2026–27 papers can still feed harmonised standards and tooling before obligations apply.

### Gaps
- EUR-Lex, nist.gov, genai.owasp.org and iso.org could not be opened, so the EU AI Act, OWASP and ISO facts rest on the Zhao list and its link audit. I found no verified record of other 2026 NIST agent items: I recall, unverified, a CAISI RFI on AI-agent security and an "AI Agent Standards Initiative" in early 2026, which need checking. The status of CEN-CENELEC JTC 21 harmonised standards, of any ISO/IEC AI-logging standard (for example a draft ISO/IEC 24970, which I also recall unverified), and of ISO/IEC 42005/42006 was not verified. The exact release date of the OWASP Agentic Top 10 was not verified.

## Q6. Which open datasets, benchmarks and codebases are easiest for a newcomer, with licenses, sizes and compute?

### Takeaway
The cheapest entry points are CPU-only and API-light:
- **CatchBench PRE:** offline, about one second.
- **CatchBench full board:** about 9 minutes of CPU and 320 MB of downloads.
- **GRADE:** networkx.
- **Who&When, TRAIL, AgentRx and Who&When Pro:** LLM-API evaluation, with cost scaling with trace count.
- **AgentDojo, Inspect and Docent:** simple pip installs or self-hosting.

OSWorld, Terminal-Bench and ControlArena's complex settings need VMs, Docker or Kubernetes and cloud budget. Licensing is the main trap: several trace datasets (Who&When, the τ-bench trajectories, SWE-bench/experiments, and likely Who&When Pro and MAST) declare no data license.

### Cited Findings
| Resource | Size / content | License (as found) | Compute / setup notes | Source |
|---|---|---|---|---|
| Who&When | 184 annotated failure tasks from 127 MAS; GAIA/AssistantBench queries; agent + decisive step + explanation | Code MIT; dataset card declares **no** license | Runs via APIs (GPT-4o etc.) or open 7B–70B models (Llama-3.1-8B/70B, Qwen2.5-7B) | [repo](https://github.com/ag2ai/Agents_Failure_Attribution) [opened]; [CatchBench licensing note](https://github.com/yzhao062/catchbench) [opened]; counts from [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) |
| Who&When Pro | 12,326 failed trajectories; 26 benchmarks; 9 task families; 18 error modes; text, image, video | No LICENSE file found in repo root; HF card not checked | `pip install -e .` (litellm, pyyaml, pillow); API eval with concurrency; README says "start small" | [repo](https://github.com/ag2ai/whowhen_pro) [opened] |
| TRAIL | 148 traces, 841 errors; GAIA and SWE-bench splits | Eval code MIT; HF dataset license not checked | LiteLLM models; long-context needed (models ~11% at localization per list) | [trail-benchmark](https://github.com/patronus-ai/trail-benchmark) [opened]; [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) |
| MAST-Data (MAD) | 1,642 annotated traces across 7 frameworks (repo: "over 1K"); full file (LLM-judge) and human-labelled file | No LICENSE file found in repo; HF card not checked | JSON via `hf_hub_download`; no compute beyond analysis | [MAST repo](https://github.com/multi-agent-systems-failure-taxonomy/MAST) [opened] |
| Aegis (dataset) | 9,533 trajectories with faulty agents and error modes (injection into successful runs) | MIT (code) | `evaluation/evaluate.py` for aegis_bench and whowhen | [kfq20/AEGIS](https://github.com/kfq20/AEGIS) [opened]; [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) |
| TraceElephant (ACL 2026) | 220 annotated failure traces from 380 executions; full traces plus reproducible environments (GAIA, AssistantBench, SWE-bench Verified) | CC BY 4.0 | HF download; `run_test.sh` | [repo](https://github.com/TraceElephant/TraceElephant) [opened] |
| AgentRx | 170 trajectories; τ-bench / Flash / Magentic-One; 10-category taxonomy | MIT (LICENSE.txt) | Defaults to Azure OpenAI credentials; 6-stage pipeline | [repo](https://github.com/microsoft/AgentRx) [opened]; count from [MSR blog](https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/) [search] |
| CatchBench | 1,187 PRE configs from 6 corpora; POST/LIVE on Who&When, SWE-Gym, τ-bench | Code MIT, not blanket: 524 PRE records NOASSERTION | PRE: `pip install catchbench>=0.1.2`, ~1 s offline. Full board: ~9 min, ~320 MB, CPU torch 2.12.1 + pyg_lib, GRADE checkout, network each run | [repo](https://github.com/yzhao062/catchbench) [opened] |
| GRADE | Loaders for τ, τ², SWE-agent, SWE-Gym, OpenHands, AgentRewardBench, Who&When | MIT | Python ≥3.10 + networkx; GNN extras need torch/PyG | [repo](https://github.com/yzhao062/grade) [opened] |
| τ²-bench / "τ-Bench" | Domains: mock, airline, retail, telecom, banking_knowledge; voice full-duplex; v1.0.1 grading update (July 2026); 75+ task fixes | MIT | `uv` install; LLM agent + user simulator via API; leaderboard taubench.com | [repo](https://github.com/sierra-research/tau2-bench) [opened] |
| AgentDojo | 97 tasks, 629 security tests; 4 suites | MIT | `pip install agentdojo`; API models; optional transformers PI detector | [repo](https://github.com/ethz-spylab/agentdojo) [opened]; [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) |
| OSWorld | 369 computer-use tasks (+ OSWorld-Verified, 2025-07-28) | Apache-2.0 | VMware/VirtualBox or Docker with KVM; AWS parallelization cuts eval to under an hour; heaviest option | [repo](https://github.com/xlang-ai/OSWorld) [opened] |
| Terminal-Bench | TB 2.0: 89 tasks with containers; now a "continuous benchmark" on Harbor Hub | Apache-2.0 | Harbor + Modal/Docker; run oracle solutions 5× to validate sandbox | [repo](https://github.com/harbor-framework/terminal-bench) [opened]; [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) |
| SWE-bench trajectories (`SWE-bench/experiments`) | Predictions, results, execution logs and trajectories for leaderboard submissions; reasoning traces required since 2024-07-29 | **No license file** | Browsing needs no Docker; since 2025-11-18 Verified/Multilingual accept only academic or research submissions with open methods | [repo](https://github.com/SWE-bench/experiments) [opened]; [CatchBench note](https://github.com/yzhao062/catchbench) |
| Inspect (UK AISI) | Eval framework; ReAct agent; approval policies; sandboxes (Docker/K8s/Modal/EC2); 200+ prebuilt evals | MIT | pip; Docker for sandboxes | [repo](https://github.com/UKGovernmentBEIS/inspect_ai) [opened]; [Zhao list](https://github.com/yzhao062/awesome-auditable-ai) |
| Docent (Transluce) | Summarize, search and cluster agent transcripts | Apache-2.0 | Hosted or self-hosted (DB); LLM API | [repo](https://github.com/TransluceAI/docent) [opened] |
| ControlArena (UK AISI) | Control settings (AgentDojo, Bash, BashArena, IAC, Infra, vLLM, SHADE Arena …), micro-protocols, monitors | MIT | `pip install control-arena` + Docker; Infra setting needs Kubernetes; two settings are private repos | [repo](https://github.com/UKGovernmentBEIS/control-arena) [opened] |

- Status notes:
  - HAL's harness no longer accepts leaderboard submissions; the effort has shifted to reliability — [hal-harness](https://github.com/princeton-pli/hal-harness) [opened].
  - CatchBench records immutable HF commits for Who&When, SWE-Gym and τ-bench and refuses to score if a dataset head moves — [CatchBench README](https://github.com/yzhao062/catchbench) [opened].

### Inferences
- **Starter path (roughly 1–2 weeks, laptop plus a modest API budget):**
  1. Run `catchbench --task pre` and the full board to learn the PRE/LIVE/POST framing.
  2. Load Who&When, TraceElephant and MAST-Data, and replicate one attribution baseline with an open 7–8B model or a cheap API model.
  3. Use AgentDojo or τ²-bench inside Inspect to *generate your own* traces with the telemetry fields you want to study, since the missing piece is traces with observed dependencies.
  4. Use Docent to cluster failures.
- For publishable data contributions, prefer permissively licensed sources: TraceElephant (CC BY 4.0), MIT or Apache-2.0 environments that you run yourself (AgentDojo, τ²-bench, Terminal-Bench, OSWorld). Avoid redistributing trajectories whose cards declare no license (Who&When, τ-bench trajectories, SWE-bench/experiments).
- Compute rule of thumb, inferred from the READMEs: attribution and audit research is dominated by API inference cost, not GPUs, unless you train attribution models (for example AgenTracer-8B in the Zhao list). OSWorld, Terminal-Bench and ControlArena Infra are the settings where infrastructure, not the model, drives cost.

### Gaps
- Hugging Face was blocked, so dataset-card licenses for Who&When Pro, MAST-Data (mcemri/MAD), TRAIL (PatronusAI/TRAIL), Aegis (Fancylalala/AEGIS), TraceElephant and AgentRx were not checked, and download sizes (other than CatchBench's ~320 MB) are unknown. No per-run dollar or GPU-hour figures were found for any benchmark; the compute notes are qualitative, from READMEs.
