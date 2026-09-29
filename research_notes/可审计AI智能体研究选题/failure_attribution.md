# Failure Attribution and Diagnosis for LLM Agents and LLM Multi-Agent Systems: State of the Art (as of 2026-09-29) and Novelty Check of Candidate Ideas (a)–(f)

*Access note, which bears on how much to trust each item: arxiv.org, alphaxiv, Hugging Face, Semantic Scholar, OpenReview and ACL Anthology were blocked by this environment's egress proxy, and the session-wide WebSearch budget ran out after the first dozen queries. Paper content was therefore read through (i) full-text Markdown mirrors of arXiv papers hosted on GitHub (`ZhangCurosr/zhangcursor-papers-arxiv-*`), (ii) abstract mirrors on GitHub (`qhduan/cn-chat-arxiv` JSON, which truncates abstracts at about 1,000 characters, and `rxmna8502/vybe-intelligence-vault` notes, which keep the full abstract), (iii) third-party paper digests (`xianshang33/llm-paper-daily`, `CMander02/DailyAgentPapers`, `zhaoyang97/Paper-Notes-en`), (iv) the official GitHub READMEs of benchmarks and methods, and (v) a few WebSearch result summaries. Every claim cites the canonical arXiv/GitHub URL plus the mirror actually read. A claim marked "secondary" comes from a third-party synthesis, not from the paper itself.*

## Q1. Where does the sub-field stand: benchmarks, best reported numbers, dominant method families, known weaknesses?

### Takeaway
On Who&When, the best reported step-level accuracy without the ground-truth answer is **55.20%** on the Algorithm-Generated split (Adaptive Influence Graphs with Opus-5). On the Hand-Crafted split it is **29.31%**, a three-way tie between A2P, CHIEF and AIG that equals exactly 17 of 58 traces. The best agent-level accuracies without GT are 71.20% on AG (AIG) and 72.41% on HC (CHIEF); with GT, CHIEF reaches 76.80% on AG and 77.59% on HC. FAMAS reaches 41.38% HC step accuracy with GT, but it re-executes the system many times, so it is not a log-only method. Much of the AG progress since 2025 comes from stronger base models: plain "all-at-once" prompting with GPT-5.5 or Opus-5 already reaches 45–46%. On natural long-horizon benchmarks, exact root-step accuracy is still 13–34% (LongRCA, TRAJDEBUG, SearchAuditor), and on TRAIL-SWE joint location-and-category accuracy is about 1–2%. The synthetic Who&When Pro reaches 73.9% step accuracy on text, but error-mode macro-F1 stays at or below 22.2 (secondary source).

### Cited Findings

#### Who&When (184 failures: 126 Algorithm-Generated from CaptainAgent, 58 Hand-Crafted from Magentic-One)
- Split composition: 126 Algorithm-Generated and 58 Hand-Crafted cases — [A2P README](https://github.com/ResearAI/A2P). The original paper's best method reached 53.5% agent-level and 14.2% step-level accuracy — [awesome-auditable-ai README](https://github.com/yzhao062/awesome-auditable-ai); [Who&When arXiv 2505.00212](https://arxiv.org/abs/2505.00212) (ICML 2025).
- **Current SOTA table, as reported in Adaptive Influence Graphs (AIG), arXiv 2608.24361 (Aug 2026), Table 1, no ground-truth (GT) answer at inference.** Values are step / agent accuracy in %:
  - AG split:
    - AIG + Opus-5: 55.20 / 71.20
    - AIG + GPT-5.6-sol: 54.76 / 67.46
    - AIG + Sonnet-4: 53.97 / 67.46
    - AIG + DS-V3.2: 53.17 / 65.08
    - RAFFLES (Zhu et al., 2025) + Sonnet-4: 51.60 / –
    - A2P + GPT-4o: 47.50 / 65.40
    - All-at-once + Opus-5: 46.40 / 67.20
    - CHIEF + DS-V3.2: 45.60 / 68.80
    - CORRECT (Yu et al., 2025) + GPT-5: 38.10 / –
    - AgenTracer-8B: 37.30 / 63.73
    - CDC-MAS (Ma et al., 2025) + GPT-4o: 36.00 / 48.50
  - HC split:
    - A2P: 29.31 / 58.62
    - CHIEF + DS-V3.2: 29.31 / 72.41
    - AIG + Opus-5: 29.31 / 63.79
    - All-at-once + Opus-5: 22.41 / 50.00
    - RAFFLES + Sonnet-4: 22.41 / –
    - AgenTracer-8B: 20.68 / 63.82

  Sources: [arXiv 2608.24361](https://arxiv.org/abs/2608.24361), full text read via [GitHub mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-26/Adaptive-Influence-Graphs-for-Failure-Attribution-in-Multi-A_f997b0a8/full.md).
- **AIG Table 8, GT answer given.** Values are step / agent accuracy in %:
  - CHIEF + DS-V3.2: AG 52.00 / 76.80; HC 29.31 / 77.59
  - AgenTracer-8B: AG 42.86 / 69.62; HC 20.68 / 69.10
  - FAMAS + Qwen2.5-72B: AG 23.81 / 55.56; HC **41.38** / 62.07
  - AIG + Opus-5: AG 52.00 / 67.20; HC 27.59 / 62.07
  - AIG notes that "ground-truth access does not consistently help".

  Source: [AIG mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-26/Adaptive-Influence-Graphs-for-Failure-Attribution-in-Multi-A_f997b0a8/full.md).
- AIG's own claims:
  - It sets a new AG SOTA, beating the previous best (51.60%) by 3.6 points.
  - It beats CHIEF by 9.96 points in a matched comparison with Opus-5 and by 7.57 points with DS-V3.2.
  - Under relaxed tolerance it reaches 55.2% exact, 64.0% within ±1 step, 78.4% within ±2 and 84.0% within ±3.
  - On failures at step ≥5, Sonnet-4 rises from 10.8% (raw-log reading) to 40.5% (AIG).
  - The representation ladder alone (raw log → structured log → influence graph → agentic traversal) moves Opus-5 from 46.40% to 55.20%.

  Sources: [arXiv 2608.24361](https://arxiv.org/abs/2608.24361); [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-26/Adaptive-Influence-Graphs-for-Failure-Attribution-in-Multi-A_f997b0a8/full.md).
- A2P reports 47.46% step accuracy on AG and 29.31% on HC. Its baselines are all-at-once 16.67 / 12.07, step-by-step 27.78 / 18.97 and binary search 28.57 / 13.79. The repo defaults to `gpt-oss-120b`, whereas AIG lists A2P under GPT-4o, so which model produced A2P's headline number is uncertain. The A2P PDF is labelled "Discovered and authored by DeepScientist" (an AI-scientist system). Sources: [A2P README](https://github.com/ResearAI/A2P); [arXiv 2509.10401](https://arxiv.org/abs/2509.10401), via a WebSearch result listing.
- CHIEF ("From Flat Logs to Causal Graphs", arXiv 2602.23701, Feb 2026) uses DeepSeek-V3.2. Its HC agent accuracy is 77.59% with GT and 72.41% without, with 29.31% step accuracy. On AG it reaches 76.80% / 68.80% agent and 52.00% / 45.60% step. It beats 8 baselines, including GraphTracer (HC agent 74.91%), and uses 55,085 tokens per HC case versus far more for FAMAS, which has to replay repeatedly. Source: [DailyAgentPapers Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/02/27/from-flat-logs-to-causal-graphs-hierarchical-failure-attribution-for-llm-based-m.md); [arXiv 2602.23701](https://arxiv.org/abs/2602.23701).
- AgenTracer-8B (ICLR 2026), reported as with-GT / without-GT:
  - HC: agent 69.10 / 63.82; step 20.68 / 20.68.
  - AG: agent 69.62 / 63.73; step 42.86 / 37.30.
  - The model weights are not released.

  Sources: [Paper-Notes-en](https://github.com/zhaoyang97/Paper-Notes-en/blob/main/docs/ICLR2026/llm_agent/agentracer_who_is_inducing_failure_in_the_llm_agentic_systems.md); [AgenTracer README](https://github.com/bingreeky/AgenTracer).
- FALAT (arXiv 2606.00765) reports its best configurations at 46.0% step accuracy on AG and 29.1% on HC — [llm-paper-daily summary](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-05/2606.00765.md).
- FAMAS (arXiv 2509.13782; FSE 2026, published in PACMSE) is spectrum-based and requires repeated MAS executions. It reports 62.07% agent-level and 41.38% action-level accuracy on HC. Sources: a WebSearch summary of [arXiv 2509.13782](https://arxiv.org/abs/2509.13782) and the [FSE 2026 listing](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/205/Spectrum-based-Failure-Attribution-for-Multi-Agent-Systems), consistent with AIG Table 8.
- CatchBench scores the 126 AG runs (1,099 steps, of which 11% are faults):
  - GPT-5.5 all-at-once reaches Top-1 0.452, Top-3 0.667 and MRR 0.618.
  - Eleven LLM judges span 0.127–0.452 Top-1.
  - A position prior reaches 0.159 Top-1 against random 0.119.
  - The supervised execution-feature ranker (from GRADE) reaches 0.211.

  Source: [CatchBench README](https://github.com/yzhao062/catchbench).
- AgentDebugX's DeepDebug reaches 28.8% exact agent-and-step joint accuracy on Who&When with qwen3.5-9b, against 21.7% for the best single-pass baseline — [llm-paper-daily summary of arXiv 2607.18754](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-07/2607.18754.md).
- DCFA (EMNLP 2026) improves step-level accuracy by up to 8.27% over SOTA baselines across six LLMs — [WebSearch summary of arXiv 2609.04749](https://arxiv.org/abs/2609.04749); venue from the [DCFA repo](https://github.com/wzhSteve/DCFA).
- DUOTRACE (arXiv 2608.29646), a detect-then-attribute plug-in, adds 8.7% agent-level and 7.0% step-level accuracy across six LLM attribution baselines — [vybe abstract](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-29646.md).
- SAFARI (arXiv 2606.24626) beats SOTA by 20% on Who&When (1M-token budget) and by 19% on the TRAIL GAIA subset (25K budget). It keeps 0.58 precision when the fault lies 5× beyond the native context window — [vybe abstract](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2606-24626.md).
- DoVer (arXiv 2512.06749; listed in [MLNLP-World's ICLR 2026 paper list](https://github.com/MLNLP-World/Top-AI-Conferences-Paper-with-Code/blob/main/ICLR/2026/ICLR2026.md), per a code-search match whose page was not opened) found that two small prompt changes (step indices plus the annotators' guidance) lift GPT-4o's HC step accuracy, with GT and all-at-once, from 6% to 24% — [DoVer text as parsed in a GitHub file](https://github.com/geostigma-hj/on_policy_intervention/blob/main/chat_history/ChatGPT-DoVer_%E6%96%87%E7%AB%A0%E8%A7%A3%E8%AF%BB.md); [arXiv 2512.06749](https://arxiv.org/abs/2512.06749).
- CDC-MAS ("Automatic Failure Attribution and Critical Step Prediction Method for Multi-Agent Systems Based on Causal Inference", arXiv 2509.08682) reports up to 36.2% step-level accuracy on Who&When and TRAIL. Its generated optimizations raise task success by 22.4% on average — [HuggingArxivLLM digest](https://github.com/HuggingAGI/HuggingArxivLLM/blob/main/papers/2025%E5%B9%B409%E6%9C%88/2025%E5%B9%B409%E6%9C%8810%E6%97%A5/Automatic_Failure_Attribution_and_Critical_Step_Prediction_Method_for_Multi-Agent_Systems_Based_on_Causal_Inference.md).

#### TRAIL, TraceElephant, Who&When Pro and other benchmarks
- **TRAIL** (148 traces, 841 errors):
  - The original paper reports long-context models near 11% — [awesome README](https://github.com/yzhao062/awesome-auditable-ai).
  - EDGE's own measurement with Gemini-2.5-Pro:
    - TRAIL-GAIA: weighted-F1 33.51 → 42.13, location 35.68 → 30.15, joint 13.74 → 15.26.
    - TRAIL-SWE-Bench: F1 26.66 → 38.97, location 6.42 → 16.58, joint 1.35 → 2.01.
    - EDGE notes that "exact localization on long-context SWE-Bench remains difficult".

  Sources: [EDGE arXiv 2609.01360](https://arxiv.org/abs/2609.01360), via its [full-text mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-09-02/EDGE-Error-Dependency-Graph-Guided-Multi-Error-Attribution-i_42fcf3e6/full.md).
- **TraceElephant** (ACL 2026):
  - Data: 220 annotated failure traces from 380 executions of Captain-Agent, Magentic-One and SWE-Agent, on GAIA, AssistantBench and SWE-Bench Verified, with executable environments — [TraceElephant README](https://github.com/TraceElephant/TraceElephant).
  - Results, according to a digest of the paper (the two sources report slightly different figures, 16/17% and 28/30%):
    - The best configuration, a dynamic agentic attributor with full traces, reaches 33.3% step and 66.7% agent accuracy.
    - Output-only traces give 51% agent and 16% step accuracy.
    - Removing inputs lowers step accuracy from 28% to 18%.

  Sources: [DailyAgentPapers Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/04/24/seeing-the-whole-elephant-a-benchmark-for-failure-attribution-in-llm-based-multi.md); the awesome README reports 17% → 30% for the static-agentic setting.
- **Who&When Pro** (arXiv 2607.09996, 2026-07-10):
  - Design: 12,326 failed trajectories, 26 benchmarks, 3 modalities and 18 error modes. Each trajectory is built by warm-start replay of a successful prefix followed by one injected error.
  - Data availability: the "Full benchmark data release" item on the roadmap was still unchecked when the README was read.

  Sources: [whowhen_pro README](https://github.com/ag2ai/whowhen_pro); [vybe abstract](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-09996.md).
  - Headline numbers (**secondary**):
    - Best on text: step 73.9 (Qwen3.5-122B), agent 57.5, error-mode macro-F1 22.2 (GLM-5), all-three joint 25.3.
    - The human panel ratifies the pipeline's labels at 94.0 / 90.0 / 90.0 (Fleiss κ=0.73) and finds no clear decisive error in only 2.0% of traces.
    - Step accuracy falls from 94% on traces under 3K tokens to 50% on traces over 12K tokens.
    - Traces average 7.5 steps.
    - All-at-once beats step-by-step (63.2 vs 55.6).

  Sources: [howard86 synthesis](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx); consistent with the [agent-bisect prior-art log](https://github.com/kidus-der/agent-bisect/blob/main/docs/findings/landscape.md).
- **Natural long-horizon benchmarks**:
  - **LongRCA Bench** (arXiv 2608.15242): 1,140 human-annotated natural failed trajectories, "without injected errors" in v1. Reference roots precede completion by a median of 48 steps. The strongest of 5 baselines (DeepSeek-V4-Flash) reaches 13.2% exact root-step accuracy; RCTA reaches 24.1% root-step and 51.1% role accuracy. "Fewer than one quarter of reference roots are recovered exactly." Sources: [vybe v4 abstract](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-15242.md); [cn-chat-arxiv v1 abstract](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/08/2608.15242.json).
  - **TRAJDEBUG / TrajErrBench** (arXiv 2608.06346; EMNLP 2026 Findings): 486 manually annotated failures — 400 from τ²-Bench averaging 29.3 steps and 86 from SWE-Bench Pro averaging 119.7 steps. Across 7 benchmarks (869 trajectories) TRAJDEBUG reaches 34.11% macro accuracy against 25.69% for direct prompting, and beats AgentDebugger, CHIEF and AgentRx. Sources: [TrajDebug README](https://github.com/THU-KEG/TrajDebug); [Aug-2026 newsletter](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
  - **SearchAuditBench** (1,243 failures): the GPT-5.5 baseline reaches 26.6%, SearchAuditor 32.3% — [newsletter](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
  - **MegaRCA-Mix** (50 human-annotated long traces): Continual Search raises GPT-5.5's F1 from 0.349 to 0.498 — [vybe abstract of arXiv 2609.13463](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2609-13463.md).
  - **AgentChaosBench** (arXiv 2608.14680; 275 telemetry traces, 10 injected operational faults): top-1 fault-type accuracy is at most 24.8% (DeepSeek-v4-pro), joint type-and-location at most 22%, and a bypassed guardrail is nearly unsolved — [vybe abstract](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-14680.md).
  - **REFLECT** (arXiv 2606.09071) reports 76.3% exact-match localization on WTQ (137 failures), against 70.8% for the next-best Opus 4.6 all-at-once, on 4 benchmarks: WTQ, GAIA, BBM and SWE-bench — [Embodied-AI-Daily summary](https://github.com/luohongk/Embodied-AI-Daily/blob/main/summaries/2606.09071.md).

#### Dominant method families (with representative work)
1. **Prompted LLM judges** (all-at-once / step-by-step / binary search). This is the Who&When protocol family and remains a strong baseline once the model is a 2026 frontier model (CatchBench GPT-5.5 at 0.452; AIG's Opus-5 all-at-once at 46.40%) — [CatchBench](https://github.com/yzhao062/catchbench); [AIG mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-26/Adaptive-Influence-Graphs-for-Failure-Attribution-in-Multi-A_f997b0a8/full.md).
2. **Structured, causal-graph or counterfactual-prompting reasoning**: A2P (abduce–act–predict inside one prompt), CHIEF, DCFA, FALAT, AIG, EDGE and CDC-MAS — sources cited above.
3. **Agentic investigation and search** over long traces: SAFARI, Continual Search, RCTA, TRAJDEBUG, DeepDebug and CUADebugger — sources cited above.
4. **Trained attributors**:
   - AgenTracer-8B: GRPO on TracerTraj.
   - VerifyMAS: SFT verifier (NeurIPS 2026) — [repo](https://github.com/mala-lab/VerifyMAS).
   - AgentLocate: judge adapted by lightweight fine-tuning — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-07989.md).
   - AFANet: GNN, 70–300× faster — [llm-paper-daily](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-08/2608.18575.md).
   - ASCon — [repo](https://github.com/Shuyu-07/ASCon).
   - StepFinder (KDD 2026) — [repo](https://github.com/taiyu-zhu/StepFinder).
   - PolyGraph — [repo](https://github.com/NoWall-572/PolyGraph).
   - One-class neural CDE — in the README list.
5. **Replay and intervention-based methods**: FAMAS, DoVer, CAR, CausalFlow, REFLECT, MRFR/GCJR, SymTrace, EDGE's rollouts and AgenticRAG-FP — details under Q3(a).
6. **Detect-then-attribute and structural monitors**: DUOTRACE, Automata from Agent Traces, GRADE and CatchBench structural boards — sources under Q2.

#### Known weaknesses repeatedly reported
- **Length and context.** On Who&When Pro, step accuracy falls from 94% to 50% as traces grow, and step-by-step reading commits too early (secondary; [howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx)). SAFARI reports attention dilution ([vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2606-24626.md)). DCFA reports "contextual degradation" ([WebSearch summary of arXiv 2609.04749](https://arxiv.org/abs/2609.04749)).
- **Premature settling.** One-shot judges settle early on a plausible diagnosis — [Continual Search](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2609-13463.md).
- **Error propagation masks the root.** Local error counts dwarf decisive ones: failed trajectories average 7.62 local errors but only 1 decisive error — [newsletter on TRAJDEBUG](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
- **Coordination errors get mislabelled.** Planning, verification and coordination errors are absorbed into the "reasoning error" label, and giving the judge the gold answer degrades process diagnosis (Who&When Pro, secondary; [howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx)). AgenTracer's notes likewise say the ground truth "G can be misleading" ([Paper-Notes-en](https://github.com/zhaoyang97/Paper-Notes-en/blob/main/docs/ICLR2026/llm_agent/agentracer_who_is_inducing_failure_in_the_llm_agentic_systems.md)).
- **Label uncertainty.** See Q3(c): [DoVer](https://github.com/geostigma-hj/on_policy_intervention/blob/main/chat_history/ChatGPT-DoVer_%E6%96%87%E7%AB%A0%E8%A7%A3%E8%AF%BB.md); [MP-Bench](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/03/26/rethinking-failure-attribution-in-multi-agent-systems-a-multi-perspective-benchm.md).
- **Single-root-cause assumption.** Criticized by MP-Bench, EDGE and the CHIEF limitations — see Q4.

### Inferences
- Reported Who&When numbers are only loosely comparable. They differ in:
  - GT access versus none;
  - backbone model;
  - n (AIG uses n=125 for Opus-5 because of one content-filtered log);
  - exact versus tolerance scoring;
  - subset (CatchBench scores AG only).

  Reviewers now expect same-backbone baselines. AIG's +8.8 points over Opus-5 all-at-once is the right kind of evidence; "2.85× over GPT-4o-era baselines" is not.
- The HC split looks near a label-quality ceiling. Three different method families tie exactly at 17/58. DoVer shows that about half of HC's GAIA cases carry uncertain labels (Q3(c)). HC should not be used as the primary evidence in a new paper without cleaning or relabelling.
- Synthetic Who&When Pro (≈74% step accuracy) versus natural long-horizon sets (13–34%) is a gap of roughly 40–60 points. It is confounded by length, number of errors and domain, which motivates idea (b).

### Gaps
- No official leaderboard exists for Who&When, TraceElephant or TRAIL; the table above is assembled from papers' self-reports.
- Absolute numbers not captured:
  - DCFA and DUOTRACE: only relative gains are known.
  - AgentLocate and ECHO: unknown.
  - VerifyMAS on Who&When: only pair-level micro-F1.
  - TRAIL's original best per-model numbers: only the README's "near 11%".
- Who&When Pro's per-model table comes from two independent secondary syntheses and was not read in the primary PDF.
- The model behind A2P's headline number (gpt-oss-120b per the README versus GPT-4o per AIG) is unresolved.

## Q2. Which new (Jun–Sep 2026) attribution/diagnosis papers are NOT in the README list, and what do the six named papers actually contribute?

### Takeaway
Beyond the six named papers, about 30 relevant Jun–Sep 2026 items are missing from the README, plus about 7 important earlier ones. None of the arXiv IDs below appear in it; only A²E (2608.07346) and the AgentDebugX paper (2607.18754) do. The additions cluster into five threads, listed below. Several important pre-June items are also missing: DoVer (ICLR 2026), CHIEF, CDC-MAS, RAFFLES, VerifyMAS and IET.
1. Interventional and causal attribution: CAR, MRFR, REFLECT, CausalFlow, EDGE, Credit Without Ground Truth, Causal Attribution for Agentic Decisions, Zero-Replay Debugging, AgenticRAG-FP.
2. Long-horizon natural benchmarks: LongRCA, TrajErrBench, MegaRCA-Mix, ParaRecover, AgentChaosBench.
3. Attribution-to-repair loops: SymTrace/SymFail, MARS/StateMAS, real-time detection and repair, skill repair.
4. New Who&When methods: AIG, DCFA, DUOTRACE, AgentLocate, AFANet, ASCon, TRIAGE.
5. Structural audit and monitoring: Automata from Agent Traces, LEDGER, ClawTrack, How Do Agents Fail on AutoResearch.

### Cited Findings

#### The six papers named in the brief
- **A2P** (arXiv 2509.10401, Sep 2025; Westlake). A one-pass prompt scaffold with three stages: abduction of hidden causes, a minimal corrective "action" (do-intervention), and prediction of the next 3–5 turns. The counterfactual is simulated by the LLM, not executed. Results are 47.46% AG / 29.31% HC step accuracy. Sources: [A2P README](https://github.com/ResearAI/A2P); [WebSearch listing of arXiv 2509.10401](https://arxiv.org/abs/2509.10401).
- **Causal Agent Replay (CAR)** (arXiv 2606.08275, 2026-06-06; single author, Jaineet Shah).
  - It models an agent run as a structural causal model (SCM) and applies do-operations over agent steps.
  - It re-executes the trajectory forward under the same stochastic policy.
  - Its single-step contrastive estimator uses a "point-of-commitment" rule for the confound created by stochastic run-forward.
  - A budget-bounded Monte-Carlo Shapley estimator splits credit across interacting steps, and every effect comes with confidence intervals.
  - **Validation is on synthetic SCMs with planted ground truth only.** Shapley recovers 0.44, 0.45 and ≈0 (efficiency 0.909 versus the analytic 0.91).
  - Self-stated limits: it estimates only total effects (no direct/indirect split); common random numbers across branches are hard with LLMs; the judge-based outcome function adds noise; and it uses mock tools only.

  Sources: [DailyAgentPapers Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/06/06/causal-agent-replay-counterfactual-attribution-for-llm-agent-failures.md); [llm-paper-daily](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-06/2606.08275.md); [arXiv 2606.08275](https://arxiv.org/abs/2606.08275).
- **Localizing Emergent Failures / MRFR** (arXiv 2608.29228, v1 2026-08-29, v2 by 2026-09-10; Northeastern University, Aalborg and Zhejiang, per a WebSearch summary).
  - It formulates Minimal Repair Family Recovery: find all inclusion-minimal event sets whose counterfactual replay restores success, within a size bound.
  - The method, Graph-Constrained Joint Replay (GCJR), slices a dependency graph, builds singleton and pair candidates, and verifies them by paired replay.
  - On 90 in-scope cases from a 120-DAG controlled benchmark it reaches Family Exact Match 1.000 and cuts replay calls from 56.3 to 25.3 (−55.1%).
  - On a 24-case, four-agent LLM pilot it again reaches 1.000 and cuts model calls from 21.0 to 10.0.
  - "Single-event replay misses jointly necessary repairs."

  Source: [vybe v2 abstract](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-29228.md).
- **DCFA** (arXiv 2609.04749; EMNLP 2026). It is training-free and has two modules:
  - Global Causal-inspired Attribution, which builds a dependency graph over the trace;
  - Local Counterfactual-inspired Enhancement, which checks candidates with counterfactual-style reasoning.

  It defines the decisive error as "the earliest action whose correction can reverse system failure" and targets "shallow attribution" and "contextual degradation". It gains up to 8.27% step-level accuracy on Who&When across six LLMs. Sources: [cn-chat-arxiv abstract](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/09/2609.04749.json); [DCFA repo](https://github.com/wzhSteve/DCFA).
- **CatchBench** (arXiv 2608.22808, v3 by 2026-09-10; code at `yzhao062/catchbench`, the README maintainer's repository).
  - It asks one auditor's question in three information states: PRE (declared configuration before a run), LIVE (a growing trace prefix) and POST (the finished trace).
  - It has 7 task contracts and scores 72 entrants over 1,187 configurations and 1,162 runs.
  - "Most of the arena does not order": 56 of 138 registered contrasts separate in v3.
  - A trivial rule reaches perfect F1 on one configuration source.
  - The injected "Gold" substrate is rejected by the paper's own admissibility bar.
  - It concludes that "a benchmark number is therefore not interpretable until the process behind its labels is published and tested for the shortcut it may leave".

  Sources: [vybe abstract](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-22808.md); [README](https://github.com/yzhao062/catchbench).
- **FAMAS** ("Who is Introducing the Failure?", arXiv 2509.13782; FSE 2026). The first spectrum-based fault localization (SBFL) method for MAS. It replays the MAS repeatedly, abstracts the trajectories, and scores suspiciousness over agent-behaviour and action-behaviour factor groups. It reaches 62.07% agent-level and 41.38% action-level accuracy on HC. Sources: [WebSearch summary](https://arxiv.org/abs/2509.13782); [FSE page](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/205/Spectrum-based-Failure-Attribution-for-Multi-Agent-Systems); [ACM DOI 10.1145/3797113](https://dl.acm.org/doi/10.1145/3797113).

#### Additional papers not in the README (Jun–Sep 2026 unless dated otherwise)

*Methods on Who&When and related multi-agent benchmarks*
- **Adaptive Influence Graphs** (arXiv 2608.24361, 2026-08-26): the new AG SOTA at 55.20% — [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-26/Adaptive-Influence-Graphs-for-Failure-Attribution-in-Multi-A_f997b0a8/full.md).
- **DUOTRACE** ("Detect Before You Attribute", arXiv 2608.29646): VAE-based anomaly detection with a Tree-LSTM encoder, used as a plug-in filter — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-29646.md).
- **AgentLocate** ("Who Broke the System?", arXiv 2607.07989): a judge plus multi-perspective verifiers with confidence-aware aggregation and lightweight fine-tuning — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-07989.md).
- **AFANet** ("Beyond LLM-Based Reasoning: Lightweight GNNs for Agent Failure Attribution", arXiv 2608.18575): matches or beats Qwen-2.5-7B/14B SFT and GRPO attributors at 70–300× speed, with test-time adaptation for out-of-distribution data — [cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/08/2608.18575.json); [llm-paper-daily](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-08/2608.18575.md).
- **ASCon** (repo created Aug 2026): trained on Aegis-Bench and TracerTraj, tested on a Who&When "RootTest" — [repo](https://github.com/Shuyu-07/ASCon).
- **TRIAGE: Severity-Ranked Multi-Agent Failure Attribution** (AACL 2026): ranks steps by suspicion, structural impact and estimated repair uplift. Replay is *simulated* by a blinded LLM evaluator rather than executed. Evaluated on Who&When and TRAIL with any-hit@K and MRR — [repo](https://github.com/jimmywang585/triage-failure-attribution).
- **VerifyMAS** (arXiv 2605.17467, May 2026; NeurIPS 2026 per the repo): an error-first hypothesis-verification attributor with an SFT verifier. On Aegis-Bench it lifts Qwen2.5-7B's agent μF1 from 27.55 to 47.92; on Who&When, used as out-of-distribution data, pair-level μF1 only moves from 2.31 to 5.83 — [DailyAgentPapers Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/05/17/verifymas-hypothesis-verification-for-failure-attribution-in-llm-multi-agent-sys.md).
- **CHIEF** (arXiv 2602.23701, Feb 2026) — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/02/27/from-flat-logs-to-causal-graphs-hierarchical-failure-attribution-for-llm-based-m.md).
- **DoVer** (arXiv 2512.06749, Dec 2025, ICLR 2026) — [abstract copy](https://github.com/AlexsJones/research/blob/main/wiki/raw/articles/dover-2512.06749.md).
- **CDC-MAS** (arXiv 2509.08682) — [digest](https://github.com/HuggingAGI/HuggingArxivLLM/blob/main/papers/2025%E5%B9%B409%E6%9C%88/2025%E5%B9%B409%E6%9C%8810%E6%97%A5/Automatic_Failure_Attribution_and_Critical_Step_Prediction_Method_for_Multi-Agent_Systems_Based_on_Causal_Inference.md).
- **IET** ("When Only the Final Text Survives: Implicit Execution Tracing for Multi-Agent Attribution", arXiv 2603.17445, Mar 2026; the last author is listed as Yue Zhao, likely but not verified to be the README maintainer): keyed watermark signals let attribution work when logs are lost — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/03/18/when-only-the-final-text-survives-implicit-execution-tracing-for-multi-agent-att.md).

*Interventional, causal and multi-error attribution*
- **EDGE** (arXiv 2609.01360; Virginia Tech). A corpus-level error-dependency graph is screened and pruned, then its edges are validated by counterfactual rollout with tool outputs held fixed. Evaluated on TRAIL and MAST — [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-09-02/EDGE-Error-Dependency-Graph-Guided-Multi-Error-Attribution-i_42fcf3e6/full.md).
- **REFLECT: Intervention-Supported Error Attribution for Silent Failures** (arXiv 2606.09071). Diagnose, then run a prefix-preserving targeted replay with a faithfulness gate, then re-localize using the successful correction as contrastive evidence. Post-correction re-localization adds 10.6 points of exact match — [summary](https://github.com/luohongk/Embodied-AI-Daily/blob/main/summaries/2606.09071.md).
- **CausalFlow** (arXiv 2605.25338, May 2026; ICLR 2026 "Agents in the Wild" workshop per a third-party log).
  - It computes Causal Responsibility Scores by step-level counterfactual intervention and produces minimal repairs as (wrong step, corrected step) contrastive pairs.
  - Repair rates are 52.4% on GSM8K, 21.9% on SealQA-Hard and 44.5% on MedBrowseComp.
  - It is single-agent and sequential by design.

  Sources: [DailyAgentPapers Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/05/25/causalflow-causal-attribution-and-counterfactual-repair-for-llm-agent-failures.md); [agent-bisect log](https://github.com/kidus-der/agent-bisect/blob/main/docs/findings/landscape.md).
- **Credit Without Ground Truth: Auditing Step-Level Credit Assignment in LLM Agents Against Executed Replay** (arXiv 2608.19760; Heady Zhang, USC). Details under Q3(e) — [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-21/CREDIT-WITHOUT-GROUND-TRUTH-AUDITING-STEP-LEVEL-CREDIT-ASSIG_b49457bb/full.md).
- **Causal Attribution for Agentic Decisions: Estimators, Coupling, and a Traceability Specification** (arXiv 2609.06445, 2026-09-06). Details under Q3(a) — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2609-06445.md).
- **Knowledge-Based Zero-Replay Debugging of Multi-Agent LLM Traces** (arXiv 2606.14805). It predicts which events a replay oracle would mark high-effect, without replaying. Branch Recall@5 rises from 0.73 to 0.93 on held-out trace families (37 families) — [cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/06/2606.14805.json).
- **When Failures Propagate: Causal Failure Attribution in Agentic RAG (AgenticRAG-FP)** (arXiv 2608.20627). An interventional benchmark that injects a certified fault at a chosen hop and re-executes the rest of the trajectory. Coverage-based diagnosis identifies the injected hop 0.91 of the time at hop 1 and 0.00 at hops 2 and 3 (n=43/36/21) — [cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/08/2608.20627.json).

*Benchmarks and empirical studies*
- **LongRCA Bench** (2608.15242), **TRAJDEBUG/TrajErrBench** (2608.06346), **AgentChaosBench** (2608.14680) and MegaRCA-Mix inside **Continual Search** (2609.13463) — all cited under Q1.
- **ParaRecover** (arXiv 2609.12345): 10,626 instances for error localization and recovery in parallel tool use, with 14 error types — [cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/09/2609.12345.json).
- **Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures** (arXiv 2607.28802). 41 failure modes, each assigned to an edge between two components and to the side that should be repaired. The strongest judge reaches Cohen's κ=0.76 against human labels — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-28802.md).
- **How Do Agents Fail on AutoResearch** (arXiv 2608.14905): 800 trajectories and 45 failure patterns; 92.1% of failures are cognitive. An agent-as-judge reaches κ=0.75 against humans, versus 0.53 for a single LLM call — [newsletter](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
- **ClawTrack** (arXiv 2607.28037): 320 tasks; a per-turn process grader backed by 12,541 rubric items attributes success and failure to reasoning dimensions — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-28037.md).
- **Automata from Agent Traces: Failure and Next-Step Prediction** (arXiv 2608.23670). Finite-state machines of 7–43 states; failure-prediction AUROC up to 0.94; early stopping at 32% of progress with 85.9% precision and 95.5% recall — [newsletter](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
- **LEDGER: Claim-to-Evidence Trace Graphs for Auditing LLM Agents** (arXiv 2608.18398) — [newsletter](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
- **AgentAudit** (arXiv 2609.09875): full-lifecycle trust evaluation — [llm-paper-daily](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-09/2609.09875.md).
- **Towards Risk-free AI Agent Deployment** (arXiv 2608.16411): a position paper — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-16411.md).
- **MAS-ProVe** (arXiv 2602.03053, Feb 2026): process verification in multi-agent systems — [cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/02/2602.03053.json).

*Attribution → repair*
- **Repair or Resample? (SymTrace/SymFail)** (arXiv 2608.25920) — [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-27/Repair-or-Resample-Rethinking-Failure-Debugging-in-LLM-Multi_46acf179/full.md).
- **MARS / StateMAS** ("Autonomous Repair for Multi-Agent Systems via Monte-Carlo Tree Search", arXiv 2607.29055): 1,310 replayable failure trajectories; gains of 3.0–12.1 absolute points — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-29055.md).
- **Real-Time Detection and Repair of LLM Agent Failures** (arXiv 2608.02464): rolling back to the last fact-gathering step recovers 45% of failures versus 16% for a resampling control — [llm-paper-daily](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-08/2608.02464.md).
- **SkillAdaptor** (arXiv 2606.01311) — [summary](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-05/2606.01311.md).
- **RESKILL** (arXiv 2609.15684) — [cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/09/2609.15684.json).
- **Ecdysis** (arXiv 2609.11677): batch-level, cross-instance attribution that separates model faults from harness faults — [summary](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-09/2609.11677.md).

### Inferences
- Venue signal for 2026:
  - ICLR 2026: AgenTracer, Aegis and DoVer (plus the CausalFlow workshop paper).
  - ACL 2026: TraceElephant.
  - KDD 2026: StepFinder.
  - FSE 2026: FAMAS.
  - NeurIPS 2026: VerifyMAS.
  - EMNLP 2026: DCFA; TRAJDEBUG in Findings.
  - AACL 2026: TRIAGE.

  Top ML venues are taking benchmarks with a new supervision signal, or training recipes (AgenTracer, Aegis, VerifyMAS). Prompting pipelines on Who&When are mostly landing at *CL main, Findings or AACL. A newcomer's method-only paper on Who&When therefore faces saturated competition. Two to three new Who&When methods appeared per month in Aug–Sep 2026.
- The README maintainer's ecosystem is itself publishing on exactly these meta-questions:
  - CatchBench (label shortcuts) and GRADE (dependency records) are the maintainer's own repositories.
  - Credit Without Ground Truth (executed-replay audit) is by Heady Zhang at USC. The handle matches the `HeadyZhang/agent-audit` component in the README's ecosystem table; the affiliation is inferred, not verified.
  - IET has a "Yue Zhao" as last author.

  This is both a collaboration opportunity and a scooping risk for ideas (a), (c) and (e).

### Gaps
- Identified only through search listings or secondary pages, not opened:
  - "CausalLoss-Fin: Attributing Financial-Agent Loss to Decisions and Infrastructure Faults" (arXiv 2609.25960).
  - The survey "Beyond Individual Intelligence: Surveying Collaboration, Failure Attribution, and Self-Evolution in LLM-based Multi-Agent Systems" (arXiv 2605.14892).
  - "Interpreting Emergent Extreme Events in Multi-Agent Systems" (arXiv 2601.20538).
  - TRACE (arXiv 2607.13988) and "An Actionable Diagnosis of Multilingual, Multi-Agent Planning Failures" (arXiv 2608.03735), both seen only through the [howard86 synthesis](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx).
  - REFLECT's arXiv abstract page and RAFFLES/CORRECT/GraphTracer's arXiv IDs are unverified.
- GitHub code search indexes these mirrors only partially, so September 2026 coverage (especially after about 2026-09-20) is probably incomplete.

## Q3(a). Idea (a): Interventional (counterfactual) ground truth and a label-validity audit of existing benchmarks

### Takeaway
**Verdict: partially addressed.** The core definition is established: the decisive step is the earliest step whose correction flips failure to success, verified by replay (AgenTracer, DoVer, DCFA). Replay-based attribution methods now exist too: CAR, CausalFlow, REFLECT, MRFR/GCJR and EDGE. **Still open:**
1. A systematic, *execution-based* audit of human-labelled decisive steps on replayable natural benchmarks. DoVer did a *manual* re-annotation of 29 cases. An Aug-2026 review states that agreement between human labels and replay labels "has not been verified".
2. An empirical comparison of intervention semantics and estimands on real multi-agent traces: oracle correction versus policy resampling; marginal versus common-random-numbers (CRN) versus natural-direct-effect estimands.
3. Overdetermination and actual-causality formalisms (Halpern–Pearl, Chockler–Halpern degree of responsibility) on real traces. No agent-attribution paper found uses them explicitly.
4. Replay-budget-efficient labelling.

### Cited Findings
- **The decisive-error definition is already formalized and used as a label generator.** AgenTracer defines the decisive set as the steps whose correction by a DeepSeek-R1 "analyzer" (which sees feedback and the GT solution) flips the outcome, and takes the earliest one. Its D⁻ half of TracerTraj is labelled by this counterfactual replay; its D⁺ half comes from fault injection into successes. Its notes list as limitations the label quality being capped by R1, high replay cost, and the "single earliest decisive error" assumption. Source: [Paper-Notes-en](https://github.com/zhaoyang97/Paper-Notes-en/blob/main/docs/ICLR2026/llm_agent/agentracer_who_is_inducing_failure_in_the_llm_agentic_systems.md).
- **DoVer re-annotated Who&When manually and argues that single-step attribution is often ill-posed.**
  - It "revisit[s] evaluation on an existing benchmark". For the 29 GAIA cases in Who&When, "14 of 29 cases exhibit GT uncertainty", consistent with Who&When's reported annotator uncertainty of 15–30% and initial disagreement of about 20%.
  - Stratified results: on the 14 uncertain cases step accuracy is 24% (GPT-4o) and 7% (GPT-5); on the 15 certain cases it is 44% and 53%.
  - Sources of uncertainty: multiple plan–execute trials in one session (9/14); orchestrator-versus-sub-agent coordination ambiguity (5/14); no clear error at the GT step (7/14).
  - DoVer replaces the attribution-accuracy metric with intervention outcomes: it flips 18–28% of failed trials to success, reaches up to 16% milestone progress, and validates or refutes 30–60% of hypotheses.
  - It does not consider asynchronous executions.

  Sources: [DoVer text](https://github.com/geostigma-hj/on_policy_intervention/blob/main/chat_history/ChatGPT-DoVer_%E6%96%87%E7%AB%A0%E8%A7%A3%E8%AF%BB.md); [abstract copy](https://github.com/AlexsJones/research/blob/main/wiki/raw/articles/dover-2512.06749.md).
- **CAR** establishes SCM/do-replay, a point-of-commitment rule, Monte-Carlo Shapley and confidence intervals. It is validated **only on synthetic SCMs**, uses mock tools, and names CRN-across-branches and direct-versus-indirect effects as open — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/06/06/causal-agent-replay-counterfactual-attribution-for-llm-agent-failures.md).
- **MRFR/GCJR** handles joint necessity through minimal repair families, but only on a controlled 120-DAG benchmark and a 24-case pilot, bounded to singletons and pairs — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-29228.md).
- **Arxiv 2609.06445 shows estimand pitfalls.**
  - Under the marginal total effect "that prior work measures", a causally inert step has the *identical* total effect to the decisive step on every run of the planted chain.
  - Under common random numbers, the decisive step returns *exactly zero* on the roughly 1-in-10 runs where the executing step flips, even though its direct effect is 0.25.
  - The paper derives a coupling that keeps the direct effect estimable, with a closed form for its degradation. It shows that "mediated share" rankings can exceed one and misrank suppressed components.
  - Its live-pipeline experiment is only pre-registered, "because the live pipeline it requires was not available".
  - It adds a traceability specification motivated by the EU AI Act: Art. 86 has applied since 2026-08-02, while Art. 12 logging was deferred to 2027-12-02 by Regulation (EU) 2026/1744 (per the paper).

  Source: [vybe abstract](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2609-06445.md).
- **Credit Without Ground Truth** builds policy-conditional ground truth by executed replay in ALFWorld: re-sample the policy's own alternatives at each decision point and roll forward. Only 30.5% of defined decision points have a nonzero replay contrast. The share of points with no policy-supported counterfactual differs twofold between two similar policies (13.1% vs 26.8%) — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-19760.md).
- **The human-versus-interventional question is explicitly open.** The Aug-2026 failure-attribution newsletter, summarized: TRAJDEBUG (486 trajectories) and SearchAuditor (1,243) rely on manual annotation, while Credit Without Ground Truth uses executed counterfactuals. Annotation measures "the step humans think is decisive", resampling measures "the step that actually changes the outcome", and "whether the two agree has not been verified" — [newsletter (Japanese)](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
- **Replay infrastructure and its limits:**
  - SymTrace's replay of recorded prefixes raises per-execution failure reproduction from 67.97% to 80.78%, and consistent reproduction across three executions from 41.42% to 52.43%. Prefix exactness is 100%.
  - Live post-target execution still varies. For example, a Wikipedia API call returned HTTP 200 in the source execution but something different on replay.
  - Recorded tool results cannot recreate persistent side effects.

  Source: [SymTrace mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-27/Repair-or-Resample-Rethinking-Failure-Debugging-in-LLM-Multi_46acf179/full.md).
  - TraceElephant ships executable agent-system code that supports "trace replay from intermediate steps" — [README](https://github.com/TraceElephant/TraceElephant).
  - Who&When Pro warm-starts successful prefixes with a content-addressable tool cache (secondary; [howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx)).
  - AgentDebugX has a `rerun --start-event N` runner protocol — [README](https://github.com/AgentDebugX/AgentDebugX).
- **Post-hoc identifiability can vanish after the rest of the trajectory re-executes.** In AgenticRAG-FP, coverage-based diagnosis finds injected faults at hop 1 91% of the time but 0% at hops 2–3 — [cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/08/2608.20627.json).
- **Replay cost.** "Cost grows linearly with the number of candidate events". The Zero-Replay predictor lifts Branch Recall@5 from 0.73 to 0.93 at zero replay cost ([cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/06/2606.14805.json)). GCJR saves about 55% of replay calls ([vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-29228.md)). FAMAS consumes far more tokens than CHIEF because it replays repeatedly ([CHIEF Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/02/27/from-flat-logs-to-causal-graphs-hierarchical-failure-attribution-for-llm-based-m.md)).
- **Shapley credit across agents:**
  - CAR's Monte-Carlo Shapley is validated on synthetic SCMs only ([Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/06/06/causal-agent-replay-counterfactual-attribution-for-llm-agent-failures.md)).
  - CDC-MAS uses Shapley values for agent-level blame computed from logs, not replay ([digest](https://github.com/HuggingAGI/HuggingArxivLLM/blob/main/papers/2025%E5%B9%B409%E6%9C%88/2025%E5%B9%B409%E6%9C%8810%E6%97%A5/Automatic_Failure_Attribution_and_Critical_Step_Prediction_Method_for_Multi-Agent_Systems_Based_on_Causal_Inference.md)).
  - CommSCM (unpublished code release) attributes over communication edges via soft interventions ([repo](https://github.com/Ashar086/counterfactual-communication-attribution)).
- **Concurrent, unpublished GitHub projects to watch:**
  - [weirdo21371480/multi-agent-error-attribution](https://github.com/weirdo21371480/multi-agent-error-attribution): 362 natural Code traces, 100 failures, single and joint repair replay, and a "minimal joint repair set" rule. "Human-reviewed causal gold remains pending."
  - [kidus-der/agent-bisect](https://github.com/kidus-der/agent-bisect/blob/main/docs/findings/landscape.md): N-run treated/control replay with Newcombe confidence intervals, planted faults in τ²-bench.
  - [geostigma-hj/on_policy_intervention](https://github.com/geostigma-hj/on_policy_intervention): a judge versus a counterfactual-rollout oracle on ALFWorld.

### Inferences
- **Closest prior work:**
  - AgenTracer (arXiv 2509.03312, ICLR 2026): defines interventional labels.
  - DoVer (arXiv 2512.06749, ICLR 2026): manual label audit on 29 cases, intervention-based evaluation.
  - CAR (arXiv 2606.08275, June 2026): SCM plus Shapley, synthetic only.
  - MRFR (arXiv 2608.29228, Aug 2026): minimal repair families, synthetic plus pilot.
  - Credit Without Ground Truth (arXiv 2608.19760, Aug 2026): executed-replay ground truth, single-agent ALFWorld, audits credit signals rather than attribution labels.
  - Arxiv 2609.06445 (Sept 2026): estimand theory, no live data.
- **How idea (a) differs:** it would apply execution-based interventional labels to *existing human-labelled natural benchmarks*. Candidates are TraceElephant (220 traces, executable) and SymFail (536, with SymTrace replay; released per the paper). Partial replay is also possible for TrajErrBench's τ²-Bench portion. The study would report:
  1. P(success | fix human-labelled step) and P(success | fix other steps);
  2. the fraction of failures with ≥2 disjoint minimal repairs (overdetermination);
  3. the agreement rate between the human label and the earliest sufficient step;
  4. how the ranking of 10 or more published attributors changes when rescored against interventional labels (Kendall τ).

  Adding an explicit Halpern–Pearl/Chockler–Halpern degree-of-responsibility score, computed with CRN-coupled estimators, would give a formal contribution that the existing papers do not.
- **Feasibility in 3–6 months: medium.**
  - Data exists: TraceElephant's code and data on Hugging Face; SymFail's traces and graphs according to the paper.
  - Compute is mostly API calls. Example budget: 200 traces × about 6 candidate steps (the human label, top-3 LLM predictions, ±1 neighbours) × 2 intervention types (oracle fix, policy resample) × K=5 samples ≈ 12,000 partial reruns. That is roughly $0.5–3K with mid-tier APIs, or feasible on 2–4 GPUs with open models driving the agents.
  - Skills needed: running AG2, Magentic-One or SWE-agent in Docker; causal-inference basics; paired statistics (Wilson confidence intervals, McNemar, bootstrap).
  - Main risk: non-reproducibility. Even with exact prefixes only about 81% of failures reproduce, so every flip must be measured against a no-intervention replay control.
- **What would make it a strong paper (NeurIPS Datasets & Benchmarks, ICLR, or ACL/EMNLP):**
  - A measured statement of the form "only X% of human-annotated decisive steps in benchmark B are interventionally sufficient; Y% of failures are overdetermined; attributor rankings change (τ=Z)".
  - A released "interventionally verified" subset.
  - A cheap proxy (for example a Zero-Replay-style predictor or a judge-plus-replay budgeter) that recovers the interventional labels with 10× fewer replays.

### Gaps
- The DoVer full text was read from a parsed copy of the PDF. It could not be confirmed whether DoVer also intervened specifically at the human-labelled step to test its sufficiency.
- SymFail and StateMAS release status and licences were not checked on Hugging Face.
- Whether TraceElephant's environments reproduce the original failures at a usable rate is not reported in the pages read.

## Q3(b). Idea (b): The synthetic-vs-natural failure gap

### Takeaway
**Verdict: open as a controlled study; fragmentary evidence exists.** Benchmark-level contrasts are large: synthetic Who&When Pro reaches about 74% step accuracy, against 13–34% on natural long-horizon sets. Several papers report artifacts or poor transfer:
- CatchBench's injected substrate leaks its labels;
- VerifyMAS barely transfers from Aegis to Who&When;
- AgenticRAG-FP's injected hop becomes unidentifiable after re-execution.

What has not been found is a matched study (same tasks, agents and scaffolds) that compares injected with natural failures on transfer of trained attributors and on the statistical profile of decisive steps. An unpublished GitHub project is working toward exactly this.

### Cited Findings
- **Construction-artifact leakage in injected faults.** In CatchBench's "Gold" boards, a broken-predecessor baseline ranks all 82 stale-state and all 106 dropped-grounding injection targets Top-1 while flagging 0 of 188 clean runs, across five injection seeds. "Both fault kinds therefore fail the no-artifact-leakage bar." The README also notes that "injected faults may not represent natural failures" — [CatchBench README](https://github.com/yzhao062/catchbench).
- **Who&When Pro is admittedly the easy case (secondary).**
  - Every trace is one injected error into an otherwise known-good run, so a unique decisive step is guaranteed to exist. The accuracies are "best read as an upper bound on real post-mortem debugging".
  - Only 2.0% of traces have no clear decisive error, "a property of the construction".
  - Traces average 7.5 steps.
  - "Does attribution accuracy survive organic failures…?" is listed as an open question.

  Source: [howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx). The agent-bisect log likewise argues that the injected outlier "leaves detectable artifacts" ([log](https://github.com/kidus-der/agent-bisect/blob/main/docs/findings/landscape.md)).
- **Natural failures have a different profile.**
  - CLI coding-agent failures "are predominantly driven by epistemic errors, typically begin within the first few execution steps, and often remain hidden until recovery is no longer possible" (1,794 trajectories, 63,000+ steps) — [vybe on arXiv 2607.09510](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-09510.md).
  - Natural failed trajectories average 7.62 local errors with 1 decisive error — [newsletter on TRAJDEBUG](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
  - LongRCA (natural, no injection) sits at 13.2–24.1% — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-15242.md).
- **Transfer evidence.** VerifyMAS trains on Aegis-Bench and moves Qwen2.5-7B's agent μF1 there from 27.55 to 47.92. On Who&When, used as out-of-distribution data, pair-level μF1 moves only from 2.31 to 5.83 — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/05/17/verifymas-hypothesis-verification-for-failure-attribution-in-llm-multi-agent-sys.md). ASCon likewise trains on Aegis-Bench and TracerTraj and evaluates on a Who&When test split — [repo](https://github.com/Shuyu-07/ASCon). StepFinder trains on LLM-*regenerated* trajectories and evaluates on Who&When — [repo](https://github.com/taiyu-zhu/StepFinder).
- **Injected labels can become unrecoverable once the rest of the trajectory changes.** In AgenticRAG-FP diagnosis finds the injected hop 91% of the time at hop 1 and 0% at hops 2 and 3 — [cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/08/2608.20627.json).
- **Mixed datasets exist.** AgenTracer's TracerTraj combines counterfactual-replay labels on natural failures (D⁻) with injection labels (D⁺). The released data "is not exactly identical to the version reported in the paper" — [Paper-Notes-en](https://github.com/zhaoyang97/Paper-Notes-en/blob/main/docs/ICLR2026/llm_agent/agentracer_who_is_inducing_failure_in_the_llm_agentic_systems.md); [AgenTracer README](https://github.com/bingreeky/AgenTracer).
- **Organic failures with paired controls are possible.** In the multilingual planning-failure study (arXiv 2608.03735), the English run succeeds while the non-English run fails. This is a matched natural control rather than an injection (secondary; [howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx)).
- **A concurrent, unpublished GitHub project** is studying natural versus synthetic failures, multi-source attribution and Code→Web transfer of post-trained attributors. "Natural-data post-training and transfer results are not yet available" — [repo](https://github.com/weirdo21371480/multi-agent-error-attribution).

### Inferences
- **Closest work:**
  - Who&When Pro (arXiv 2607.09996, July 2026) and Aegis (arXiv 2509.14295, ICLR 2026): synthetic sources.
  - CatchBench (arXiv 2608.22808): the artifact-leakage test.
  - VerifyMAS (arXiv 2605.17467, NeurIPS 2026): Aegis→Who&When out-of-distribution results.
  - LongRCA (arXiv 2608.15242) and Failure as a Process (arXiv 2607.09510): natural profiles.
  - The unpublished weirdo21371480 project.
- **What would differ in idea (b):** a controlled 2×2 design (natural vs injected failures × in-distribution vs out-of-distribution attributor training) on the *same* agents and tasks, for example by collecting natural failures and injected failures from the same scaffolds on τ²-bench or GAIA. It would add:
  1. an "injection detectability" test, i.e. a classifier or heuristic that finds the injected step without understanding the task, generalizing CatchBench's broken-predecessor probe;
  2. distributional comparisons: position of the decisive step, number of errors, error-mode mix (planning, verification and coordination share), and trace length;
  3. transfer of AgenTracer-style and VerifyMAS-style trained attributors;
  4. an "injection recipe calibrated to natural statistics" that closes part of the gap.
- **Feasibility: high.** Most of the work is analysis on public data: Aegis on Hugging Face, Who&When, TRAIL (gated), TrajErrBench in its repo, SymFail per its paper, and Who&When Pro's harness (the full data release is still pending). LoRA fine-tuning of a 7–8B attributor needs 1–2 GPUs. Main risk: the unpublished project above may publish first.
- **Strong headline:** "Attributors trained on injected failures lose X points on matched natural failures; injected decisive steps are detectable by artifact-only probes with AUROC Y; natural decisive steps occur earlier and are Z× more often planning or verification errors." This fits ACL/EMNLP main, or NeurIPS Datasets & Benchmarks if a new matched corpus is released.

### Gaps
- No paper was found that reports a controlled natural-versus-injected comparison on identical tasks and agents. Given that the search was limited to GitHub mirrors, this is a "not found", not a proof of absence.
- Aegis's own cross-benchmark (Aegis→Who&When) numbers were not retrieved.

## Q3(c). Idea (c): Shortcut and annotation-artifact analysis of attribution benchmarks

### Takeaway
**Verdict: partially addressed; low novelty as a standalone paper.** Pieces already exist:
- CatchBench reports a position prior on Who&When AG (Top-1 0.159 vs random 0.119) and exposes construction shortcuts on its other boards.
- DoVer quantifies label uncertainty on Who&When HC.
- MP-Bench argues that "LLMs are bad at attribution" is largely an artifact of single-root-cause benchmark design.
- SymFail and Who&When Pro report inter-annotator statistics.
- A GitHub harness documents concrete Who&When file anomalies.

No systematic cross-benchmark heuristic suite was found. Such a suite would test role priors ("blame the orchestrator", last agent), "first error message or tool error" and position priors across Who&When, TRAIL, TraceElephant, Aegis, Who&When Pro, LongRCA and TrajErrBench, and would ship a cleaned "Verified" release. It is best combined with (a) or (b).

### Cited Findings
- **Position prior on Who&When AG** (126 runs, 1,099 steps): Top-1 0.159, Top-3 0.516, MRR 0.407, against random at 0.119 / 0.346 / 0.324. Two of eleven LLM judges (Mistral-Small at 0.135, Nova-Micro at 0.127) fall *below* the position prior — [CatchBench README](https://github.com/yzhao062/catchbench).
- **CatchBench construction shortcuts.** One rule ignores every name and permission and "flags each capability declared after the first"; it reaches perfect F1 on one of six configuration sources. The paper states: "A benchmark number is therefore not interpretable until the process behind its labels is published and tested for the shortcut it may leave" — [vybe abstract](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-22808.md). CatchBench also excludes Who&When HC because HC traces omit the per-step agent-name field in all 2,993 steps (versus 1,099 of 1,099 in AG) — [full-text mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-lg-001/blob/main/2026-08-25/CATCHBENCH-WHEN-CAN-AN-AGENT-FAILURE-BE-CAUGHT_d2548947/full.md).
- **Label uncertainty in Who&When** (DoVer): 14 of 29 GAIA cases are uncertain. Who&When itself reported 15–30% annotator uncertainty and about 20% initial disagreement. GPT-5 scores 7% on the uncertain cases and 53% on the certain ones — [DoVer text](https://github.com/geostigma-hj/on_policy_intervention/blob/main/chat_history/ChatGPT-DoVer_%E6%96%87%E7%AB%A0%E8%A7%A3%E8%AF%BB.md).
- **Who&When file anomalies** found by a replication harness (a pilot, not a paper):
  - 3 Hand-Crafted files point past the end of their trajectory (step 51 of 28, 8 of 5, 24 of 19);
  - 2 Algorithm-Generated files contain an empty-content step;
  - 3 + 3 files show agent/step mismatches.

  Source: [iamtaehyunpark/maej-uq README](https://github.com/iamtaehyunpark/maej-uq).
- **MP-Bench** (arXiv 2603.25001): LLMs' sampling disagreement mirrors experts' disagreement. Under multi-perspective nDCG, models beat random clearly (Claude-Sonnet-4.5 nDCG@5 of 0.5916; a cross-family ensemble reaches 0.8228). "Prior conclusions suggesting LLMs struggle with failure attribution are largely driven by limitations in existing benchmark designs" — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/03/26/rethinking-failure-attribution-in-multi-agent-systems-a-multi-perspective-benchm.md).
- **Inter-annotator agreement numbers now available:**
  - SymFail (3 independent annotators, 536 failures): exact failure-node agreement 73.88% for all three and 95.90% for at least two; the complete strict tuple agrees in only 39.18%; Fleiss κ is 0.622 for the primary category. The adjudicated final label is fully supported by all three initial annotators in only 34.89% of cases — [SymTrace mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-27/Repair-or-Resample-Rethinking-Failure-Debugging-in-LLM-Multi_46acf179/full.md).
  - Who&When Pro: human ratification κ=0.73 (secondary; [howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx)).
  - Model-or-Harness taxonomy: the judge reaches κ=0.76 against humans — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-28802.md).
- **Positional structure is exploited or acknowledged by methods.**
  - StepFinder includes an explicit "position bias term" in its model — [repo](https://github.com/taiyu-zhu/StepFinder).
  - GRADE's localization script claims "execution structure beats an early-fault prior" — [README](https://github.com/yzhao062/grade).
  - FALAT notes that single-pass judges suffer "positional bias and order sensitivity" — [summary](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-05/2606.00765.md).
  - AIG's gains concentrate on later failures (step ≥5) — [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-26/Adaptive-Influence-Graphs-for-Failure-Attribution-in-Multi-A_f997b0a8/full.md).
- **Tolerance-window metrics are already in use**: AIG's ±1/±2/±3 windows, FA4MAS's ±1–±5, Who&When Pro's Step@1 (secondary). Sources: [AIG mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-26/Adaptive-Influence-Graphs-for-Failure-Attribution-in-Multi-A_f997b0a8/full.md); [FA4MAS](https://github.com/SSonnyboy/FA4MAS).

### Inferences
- **Closest work:** CatchBench (arXiv 2608.22808), DoVer §3 (arXiv 2512.06749), MP-Bench (arXiv 2603.25001), the SymFail agreement analysis (arXiv 2608.25920) and the maej-uq pilot.
- **Remaining niche.** A "Who&When-Verified"-style release in the spirit of SWE-bench Verified or τ²-bench-verified would contain:
  - a heuristic panel covering position histograms per benchmark, first tool error, first message containing "error"/"fail", last agent, orchestrator blame and the most-frequent speaker;
  - per-benchmark "trivial-baseline ceilings";
  - a re-annotation with κ and item validity;
  - re-ranking of published methods on the cleaned subset.

  Idea (c) alone would likely land at a Findings or workshop venue. Combined with interventional relabelling (a) it becomes a main-track resource paper.
- **Feasibility: very high.** It takes 2–6 weeks with near-zero compute beyond re-running a few open-source attributors, and the data is public.
- **Strong headline:** "Trivial heuristics reach X% of SOTA on benchmark B. After removing invalid or ambiguous items, method rankings flip and reported gains shrink by Y points."

### Gaps
- The original Who&When per-annotator raw labels were not checked for release.
- It was not verified whether TRAIL or TraceElephant publish inter-annotator agreement.

## Q3(d). Idea (d): Attribution-to-repair utility

### Takeaway
**Verdict: partially addressed and very active.** DoVer (ICLR 2026) already argues for outcome-oriented evaluation. SymTrace shows that suspicious-node intervention (20.15%) beats both random-node and last-node intervention under the same budget and nearly triples task-level regeneration (6.90%). REFLECT shows that intervening at the wrong step collapses correction rates. Several systems report repair gains: AgentDebugX, TRAJDEBUG, MARS, the real-time repair paper and CausalFlow. One unpublished project localizes perfectly yet gains nothing end-to-end. **Not found:** a cross-method study that quantifies how well attribution accuracy (against human or interventional labels) predicts repair success under matched budgets with resampling controls, or a standardized utility metric adopted across methods.

### Cited Findings
- **DoVer**: "Rather than evaluating on attribution accuracy, we focus on measuring whether the system resolves the failure or makes quantifiable progress". It flips 18–28% of failures — [abstract copy](https://github.com/AlexsJones/research/blob/main/wiki/raw/articles/dover-2512.06749.md).
- **SymTrace/SymFail**:
  - Task-level regeneration repairs at most 6.90% of failures within three attempts.
  - Suspicious-Node Intervention repairs 20.15% with one intervention (2.92×).
  - It "substantially outperforms Random-Node Intervention and Last-Node Intervention under the same selective-replay budget".
  - The paper separates causal repair from stochastic resampling.

  Source: [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-27/Repair-or-Resample-Rethinking-Failure-Debugging-in-LLM-Multi_46acf179/full.md).
- **REFLECT**:
  - Injecting the correct repair hint yields a correction rate 42 points higher than no hint or a placebo hint.
  - Intervening at the wrong step lowers correction substantially.
  - Correction–localization coupling: explanation similarity differs by 0.25–0.29 between corrected and uncorrected trajectories, against ≤0.05 for ICS and Reflexion.

  Source: [summary](https://github.com/luohongk/Embodied-AI-Daily/blob/main/summaries/2606.09071.md).
- **Real-time detection and repair**: rolling back to the last fact-gathering step recovers 45% of failures versus 16% for a resampling control, lifting success from 52% to 73% — [summary](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-08/2608.02464.md).
- **AgentDebugX DeepDebug** repairs 13 of 73 failed GAIA tasks in one rerun, against 4–6 for three decoupled self-correction baselines, lifting accuracy from 55.8% to 63.6% — [summary](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-07/2607.18754.md).
- **TRAJDEBUG**: feeding its diagnosis back into a rerun raises success by 10.80% on average; transferring it as failure memory adds 5.70% — [newsletter](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
- **MARS/StateMAS** (1,310 replayable trajectories): MCTS repair with partial rollouts gains 3.0–12.1 absolute points. It describes DoVer as "the only existing work" on automated MAS repair — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-29055.md); [summary](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-07/2607.29055.md).
- **CausalFlow** repairs 52.4% (GSM8K), 21.9% (SealQA-Hard) and 44.5% (MedBrowseComp) of failures with minimal edits, and states that "causal attribution is necessary for reliable improvement" — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/05/25/causalflow-causal-attribution-and-counterfactual-repair-for-llm-agent-failures.md).
- **TRIAGE** (AACL 2026) ranks candidates partly by *estimated* repair uplift, R = 1 + max(0, patched − baseline), using simulated rather than executed replay — [repo](https://github.com/jimmywang585/triage-failure-attribution).
- **AgenTracer's attribution feedback** improves MetaGPT, MaAS and OWL by 4.8–14.2% — [Paper-Notes-en](https://github.com/zhaoyang97/Paper-Notes-en/blob/main/docs/ICLR2026/llm_agent/agentracer_who_is_inducing_failure_in_the_llm_agentic_systems.md).
- **Negative evidence (unpublished code release, CommSCM).** On SWE-bench Verified (n=100), its method recovers the injected gold communication edge in every instance (hit rate 1.00 versus 0.33 for a reward-only baseline). Yet "Resolve@1 does not improve" (0.02 versus 0.03–0.04), because failures move to patch synthesis — [repo](https://github.com/Ashar086/counterfactual-communication-attribution).
- **CUADebug** uses human annotations "to fix restart points" in controlled re-rollouts — [cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/08/2608.02643.json).
- **EDGE** leaves "evaluating such a [repair] loop faithfully [which] requires re-executing multi-agent systems at scale" to future work — [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-09-02/EDGE-Error-Dependency-Graph-Guided-Multi-Error-Attribution-i_42fcf3e6/full.md).

### Inferences
- **Closest work:** DoVer (arXiv 2512.06749, ICLR 2026), SymTrace (arXiv 2608.25920, Aug 2026), REFLECT (arXiv 2606.09071), MARS (arXiv 2607.29055) and AgentDebugX (arXiv 2607.18754).
- **What idea (d) would add:** a measurement study rather than yet another repair system. Take N published attributors and M repair operators (edit message, re-plan, resample from a step, rollback). Run each on replayable failures (SymFail, StateMAS, TraceElephant) with a resampling control, then report:
  1. the correlation, and its confidence interval, between per-trace attribution correctness and repair success;
  2. utility curves by distance from the labelled step: is "±1" as good as exact, and do earlier steps repair better?;
  3. cases where a "wrong" attribution repairs, i.e. overdetermined failures;
  4. a utility-based metric proposal ("repair@k from attributed step minus resample@k"), plus a leaderboard reordering.
- **Feasibility: medium.** Replay infrastructure exists: SymTrace, AgentDebugX's runner protocol, TraceElephant's code. Cost scales with attributors × repair operators × K; restricting to 150–300 traces and 5 attributors is tractable. Main risk: SymTrace or MARS authors may extend their own work in this direction.
- **Strong headline:** "Attribution accuracy explains only X% of the variance in repair success; ranking methods by repair utility reorders the leaderboard; about Y% of 'incorrect' attributions yield valid repairs."

### Gaps
- It is unknown whether StateMAS is publicly released, or whether SymTrace's replay bundles are released with the data.
- No paper reporting a Spearman/Kendall correlation between attribution accuracy and repair success was found.

## Q3(e). Idea (e): Process reward models and step verifiers as failure attributors

### Takeaway
**Verdict: partially addressed and converging quickly.** The PRM-to-attribution link has already been made:
- "Neglected Free Lunch" (arXiv 2606.26080) uses its implicit progress advantage for failure attribution on five benchmarks. The pages read did not say which ones.
- "Credit Without Ground Truth" (arXiv 2608.19760) audits LLM-judge scores, outcome-conditioned log-probability ratios (the implicit-PRM family) and policy confidence against executed-replay ground truth in ALFWorld. None beats its shuffled control.
- MAS-ProVe finds process verification inconsistent in multi-agent systems.
- ClawTrack uses a per-turn process grader for attribution.

**Still open:** explicit agent PRMs (for example AgentPRM) benchmarked on multi-agent attribution benchmarks (Who&When, TraceElephant, LongRCA, TrajErrBench) against both human and interventional labels, and at scales and environments beyond ALFWorld with 7–8B models.

### Cited Findings
- **Progress advantage** (arXiv 2606.26080): "log-probability ratio between the RL-trained policy and its reference policy exactly recovers the optimal advantage function". It is validated on "test-time scaling, uncertainty quantification, and failure attribution on five benchmarks and four model families" and "surpasses dedicated trained reward models" — [vybe abstract](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2606-26080.md); [summary](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-06/2606.26080.md).
- **Credit Without Ground Truth**:
  - Setting: ALFWorld; Qwen2.5-7B (50 trajectories) and Llama-3.1-8B (28, per the newsletter).
  - Finding: "none of the step-level credit signals we audit — LLM-judge scores, outcome-conditioned logprob ratios, or the policy's own confidence — shows reliable incremental fidelity beyond its own marginal-matched shuffled control".
  - Implicit credit "echoes the policy's fluency" (median rank correlation +0.75; +0.70 in a second family). Outcome conditioning adds no causal information (partial correlation −0.004).
  - A confidence-only router finds pivotal steps at chance level but cuts judge cost by 13.1% per turn.
  - Across 7 pre-registered training arms, none reliably beats the untrained policy; the differences are explained by "effective training dose". Its conclusion: "Comparisons of credit rules must match effective sample size, or they measure dose, not credit."
  - Limitations: a single environment, a single scale, offline LoRA, and no validated positive control for the training loop.

  Sources: [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-19760.md); [full-text mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-21/CREDIT-WITHOUT-GROUND-TRUTH-AUDITING-STEP-LEVEL-CREDIT-ASSIG_b49457bb/full.md); [newsletter](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
- **MAS-ProVe** (arXiv 2602.03053): a systematic study of LLM-as-judge, reward-model and PRM verification at agent and iteration granularity, over six multi-agent frameworks. "Process-level verification does not consistently impr[ove]" (the abstract is truncated there) — [cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/02/2602.03053.json).
- **ClawTrack** (arXiv 2607.28037): a Process Grader scores each turn on goal alignment, efficiency, information use and result verification. "Process scores effectively attribute success and failure to specific reasoning dimensions" — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-28037.md).
- **TRACE** (arXiv 2607.13988; secondary): scores each prefix by how predictable a *frozen reference model* finds the gold answer, and takes the decisive turn from adjacent differences. It needs the gold answer, which is unavailable when debugging in the wild — [howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx).
- **CausalFlow** produces validated (wrong step, corrected step) pairs "suitable for offline preference optimization or reward modeling", i.e. PRM training data derived from interventions — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/05/25/causalflow-causal-attribution-and-counterfactual-repair-for-llm-agent-failures.md).
- **AgentPRM** ("Process Reward Models for LLM Agents via Step-Wise Promise and Progress", arXiv 2511.08325) exists, according to GitHub digest listings (for example [PacemakerG/Agent-failure-diagnosis](https://github.com/PacemakerG/Agent-failure-diagnosis)). Its content was not opened.

### Inferences
- **Closest work:** arXiv 2606.26080 (June 2026), arXiv 2608.19760 (Aug 2026; Heady Zhang, USC, apparently in the README maintainer's ecosystem, not verified), MAS-ProVe (arXiv 2602.03053) and ClawTrack (arXiv 2607.28037).
- **What remains open:**
  1. A head-to-head benchmark of explicit agent PRMs, implicit PRMs or progress advantage, LLM judges and specialized attributors on *multi-agent* attribution benchmarks, scored against *both* human labels and interventional labels.
  2. Whether the negative result of Credit Without Ground Truth holds on long SWE or τ² trajectories and with larger policies. The newsletter flags this as "the next focus".
  3. Using PRMs as cheap first-stage filters that allocate a replay budget; this connects to Zero-Replay Debugging.
- **Feasibility: medium.**
  - Log-probability or implicit-PRM signals require open-weight RL-trained policies and their reference models (for example Qwen3-8B RL checkpoints). Scoring trajectories needs 1–4 A100/H100-class GPUs.
  - Explicit agent PRM checkpoints may not be public; this was not verified.
  - The agents behind Who&When (GPT-4o-based CaptainAgent and Magentic-One) are closed, so implicit-PRM log-probabilities cannot be computed on them. Only external scorer-style PRMs apply there.
- **Strong headline:** either a positive result ("a PRM's minimum-progress step matches interventional decisive steps at X% on long multi-agent traces at 1/100 of the judge cost") or a replicated negative one ("PRM credit tracks fluency, not causal responsibility, across N environments and model scales"). The negative version extends a result from the same USC ecosystem and so carries a higher scooping risk.

### Gaps
- Which "five benchmarks" arXiv 2606.26080 used for failure attribution (whether Who&When or TRAIL is among them) could not be read.
- No evidence was found either way on whether AgentPRM-style models have been scored on Who&When or TRAIL.

## Q3(f). Idea (f): Scaling attribution to long, branching, multi-agent traces

### Takeaway
**Verdict: largely addressed for long *linear* traces; crowded.** Bottlenecks the papers themselves name:
- attention dilution and context limits;
- premature settling on a diagnosis;
- sparse, distant evidence;
- many local errors against one decisive error;
- missing agent inputs in the logs;
- insufficient telemetry;
- dependencies across parallel branches.

Still open: asynchronous, branching or parallel multi-agent DAG traces (DoVer explicitly excludes asynchronous logs); streaming or online attribution (CatchBench LIVE shows no method clearing its threshold on τ-bench); and attribution across runs or a whole fleet.

### Cited Findings
- **SAFARI**: "attention dilution"; the method uses tools plus short-term memory and keeps 0.58 precision at 5× the context window — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2606-24626.md).
- **Continual Search**: one-shot judges "settle on a plausible diagnosis early"; evidence is "sparse, distributed across distant actions". Its new benchmark, MegaRCA-Mix, has 50 human-annotated long trials. "Lower-tier models can even surpass their higher-tier counterparts" — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2609-13463.md).
- **LongRCA**: roots precede completion by a median of 48 steps; 28.4% of trajectories have more than 100 subsequent steps; RCTA reaches 24.1% — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-15242.md).
- **TRAJDEBUG**: on the longest trajectories it stays above 20% while the best baseline falls to about 14%. Removing multi-granularity compression costs 21.02 points — [newsletter](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
- **SearchAuditor**: 73.1 messages and 65.1K tokens on average; 32.3% — [newsletter](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
- **Who&When Pro**: step accuracy is 94% under 3K tokens and 50% over 12K (secondary) — [howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx).
- **Missing context and inputs**: TraceElephant finds that removing inputs lowers step accuracy from 28% to 18% — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/04/24/seeing-the-whole-elephant-a-benchmark-for-failure-attribution-in-llm-based-multi.md). AIG notes that "Who&When exposes agent outputs but not the inputs each agent saw" — [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-26/Adaptive-Influence-Graphs-for-Failure-Attribution-in-Multi-A_f997b0a8/full.md).
- **Telemetry-only**: fault-origin step accuracy is at most 0.5% (TelemetrySuffBench, [README list](https://github.com/yzhao062/awesome-auditable-ai)). Joint type-and-location accuracy is at most 22% (AgentChaosBench, [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-14680.md)).
- **Parallel and branching structure**: ParaRecover targets "errors [that] may propagate across dependent branches" in parallel tool use (10,626 instances) — [cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/09/2609.12345.json). DoVer segments logs into plan–execute "trials" and states: "We do not consider logs from asynchronous agent executions" — [DoVer text](https://github.com/geostigma-hj/on_policy_intervention/blob/main/chat_history/ChatGPT-DoVer_%E6%96%87%E7%AB%A0%E8%A7%A3%E8%AF%BB.md).
- **Online and LIVE settings**: "On tau-bench, no reported method's point estimate reaches the 0.70 time-to-detection threshold" — [CatchBench README](https://github.com/yzhao062/catchbench). Automata from Agent Traces fires early stopping at 32% of progress (85.9% precision, 95.5% recall), but this is failure *prediction*, not attribution — [newsletter](https://github.com/masamasa59/ai-agent-papers/blob/main/newsletters/aug_2026/failure_attribution_trends.md).
- **Cross-instance attribution**: Ecdysis aggregates failures across instances to separate harness faults from model faults — [summary](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-09/2609.11677.md). EDGE builds a corpus-level dependency graph over error categories — [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-09-02/EDGE-Error-Dependency-Graph-Guided-Multi-Error-Attribution-i_42fcf3e6/full.md).

### Inferences
- **Closest work:** SAFARI (arXiv 2606.24626), Continual Search (arXiv 2609.13463), LongRCA (arXiv 2608.15242), TRAJDEBUG (arXiv 2608.06346), SearchAuditor (arXiv 2608.05212), AIG (arXiv 2608.24361), DCFA (arXiv 2609.04749) and DUOTRACE (arXiv 2608.29646).
- Another long-trace method would be incremental.
- **Defensible niches:**
  1. Asynchronous or parallel multi-agent DAG traces, where "earliest step" is ill-defined and needs a happens-before or causal order.
  2. Streaming attribution under a latency budget (LIVE).
  3. Fleet-level attribution across many runs (which component, prompt or tool version is responsible).
- **Feasibility for a newcomer: low to medium.** Each niche needs new data collection, for example async runs in LangGraph, CrewAI or A2A with timestamps and dependency edges.

### Gaps
- No benchmark specifically for asynchronous or parallel multi-agent attribution was found. ParaRecover works at the level of tool-use branches, not multi-agent systems.

## Q4. What open problems do the most recent papers themselves name?

### Takeaway
The recurring self-reported open problems are:
1. Single-root-cause labelling versus multi-error and overdetermined failures (CHIEF, TraceElephant, MP-Bench, EDGE, AgenTracer, REFLECT).
2. Evaluation on only one benchmark, and Who&When's missing inputs (AIG, CHIEF).
3. Replay cost and replay fidelity, including side effects and nondeterminism (AgenTracer, CAR, SymTrace).
4. Label construction and validity (CatchBench, DoVer, SymFail).
5. Evaluation of repair loops at scale (EDGE, MP-Bench, SymTrace).
6. Oracle-free verification and calibration (REFLECT, VerifyMAS).
7. Generalization beyond ALFWorld and small models (Credit Without Ground Truth).
8. Formal adequacy metrics and long-horizon root-cause attribution (Towards Risk-free AI Agent Deployment).

### Cited Findings
- **AIG**:
  - "whether the representation ladder transfers to other multi-agent frameworks and task distributions remains open";
  - Who&When lacks agent inputs;
  - it scores only a single annotated step, with no gold for intermediate graph structure;
  - it costs more tokens.

  Source: [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-26/Adaptive-Influence-Graphs-for-Failure-Attribution-in-Multi-A_f997b0a8/full.md).
- **CHIEF**: depends on the quality of its causal graph and virtual oracle (hallucinated edges); evaluated only on Who&When; assumes a single decisive root cause and does not handle cumulative small-deviation failures. Suggested future work includes "uncertainty modeling" — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/02/27/from-flat-logs-to-causal-graphs-hierarchical-failure-attribution-for-llm-based-m.md).
- **TraceElephant**: covers only three multi-agent architectures; assumes white-box full traces, so benchmarks with partial or noisy observations are needed; handles single-step attribution only. Suggested future work: counterfactual or Shapley decomposition across steps — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/04/24/seeing-the-whole-elephant-a-benchmark-for-failure-attribution-in-llm-based-multi.md).
- **MP-Bench**: needs probability or confidence weights across attributions; needs a diagnosis→repair closed loop; relies on LLM judges for evaluation — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/03/26/rethinking-failure-attribution-in-multi-agent-systems-a-multi-perspective-benchm.md).
- **VerifyMAS**: needs uncertainty and confidence calibration; its predefined taxonomy limits discovery of novel error types; cross-trajectory consistency is unused — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/05/17/verifymas-hypothesis-verification-for-failure-attribution-in-llm-multi-agent-sys.md).
- **CAR**: measures total effect only; CRN is hard in LLM settings; judge-based outcome noise; no real side-effecting tools; the budget–variance trade-off of Shapley estimation — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/06/06/causal-agent-replay-counterfactual-attribution-for-llm-agent-failures.md).
- **CausalFlow**: depends on the LLM proposing good interventions; replay cost; retrieval-driven failures cannot be fixed locally; structured logging lowered base accuracy (75.0% vs 88.1% on GSM8K); needs dependency annotations; extension to multi-agent systems — [Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/05/25/causalflow-causal-attribution-and-counterfactual-repair-for-llm-agent-failures.md).
- **EDGE**:
  - corpora with multi-error annotations are "scarce and have low per-category support";
  - its graph is category-level, not trace-level;
  - interventions hold tool outputs fixed;
  - MAST event annotations are not human-validated;
  - repair-loop evaluation "requires re-executing multi-agent systems at scale, which we leave to future work".

  Source: [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-09-02/EDGE-Error-Dependency-Graph-Guided-Multi-Error-Attribution-i_42fcf3e6/full.md).
- **CatchBench**:
  - "Dropped grounding remains open";
  - online stale-state detection is open;
  - the τ-bench warning bar is unresolved at 660 runs;
  - the Gold boards are "artifact-limited";
  - cross-vendor judge labels carry residual "label subjectivity";
  - its next release adds a human-audited validation slice with inter-rater agreement.

  Source: [full-text mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-lg-001/blob/main/2026-08-25/CATCHBENCH-WHEN-CAN-AN-AGENT-FAILURE-BE-CAUGHT_d2548947/full.md).
- **Credit Without Ground Truth**: single environment with a binary outcome; single-family, single-scale training; no validated positive control; the family-by-length interaction was "unmeasurable" and "inherited by future work" — [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-21/CREDIT-WITHOUT-GROUND-TRUTH-AUDITING-STEP-LEVEL-CREDIT-ASSIG_b49457bb/full.md).
- **SymTrace**: data covers benchmark tasks, not deployed systems; broader independent re-annotation is future work; persistent side effects cannot be replayed — [mirror](https://github.com/ZhangCurosr/zhangcursor-papers-arxiv-ai-001/blob/main/2026-08-27/Repair-or-Resample-Rethinking-Failure-Debugging-in-LLM-Multi_46acf179/full.md).
- **REFLECT**: weak on pure chain-of-thought traces; "single-step attribution may not apply in distributed or multi-round failures"; the proxy verifier is a bottleneck. Future work: oracle-free verification and replay for unstructured traces — [summary](https://github.com/luohongk/Embodied-AI-Daily/blob/main/summaries/2606.09071.md).
- **AgenTracer (per paper notes)**: labels capped by DeepSeek-R1; high replay cost; "single earliest decisive error assumption" — [Paper-Notes-en](https://github.com/zhaoyang97/Paper-Notes-en/blob/main/docs/ICLR2026/llm_agent/agentracer_who_is_inducing_failure_in_the_llm_agentic_systems.md).
- **Towards Risk-free AI Agent Deployment**: open problems are "formal adequacy metrics, root-cause attribution over long-horizon trajectories, and the reliability of self-evolving agents" — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-16411.md).
- **LongRCA**: "Even with RCTA, fewer than one quarter of reference roots are recovered exactly" — [vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2608-15242.md).
- **Who&When Pro (secondary)**:
  - accuracy on organic multi-cause failures is unmeasured;
  - human accuracy from scratch was never measured, because humans only *ratified* the supplied labels;
  - GPT-4.1 was chosen as the base agent because its reasoning is legible, and attribution depends on that legibility.

  Source: [howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx).

### Inferences
- The two most repeatedly named and least addressed problems:
  1. Ground truth for multi-cause and overdetermined natural failures (what should the label be?).
  2. Faithful repair-loop evaluation at scale.

  Both map onto ideas (a) and (d), which suggests a combined "interventional labels plus utility" paper hits the community's own stated gap.

### Gaps
- The limitations sections of DCFA, DUOTRACE, AgentLocate, LongRCA (full text) and Who&When Pro (primary) could not be read.

## Q5. Additional promising gaps (computer-use/embodied, telemetry-only, calibrated uncertainty, and others)

### Takeaway
Four gaps look promising and suit an "auditable agents" framing. They are ordered by fit for a newcomer.
1. **What must be logged for attribution to be possible?** Minimal sufficient trace schemas and legibility requirements. Telemetry-only attribution is near zero, full traces help markedly, and the EU AI Act makes this timely.
2. **Calibrated, set-valued attribution with abstention**, validated against interventional labels. Conformal and multi-perspective work exists, but nothing has been calibrated against execution-based labels.
3. **Coordination-aware attribution.** Planning, verification and coordination errors are systematically mislabelled as reasoning errors.
4. **Computer-use and embodied attribution.** CUADebug and Who&When Pro's multimodal splits are early; embodied or VLA attribution with physical replay is largely untouched.

### Cited Findings
- **Logging and legibility**:
  - Telemetry views keep 99.5–100% detection F1 while fault-origin step accuracy stays at or below 0.5% (TelemetrySuffBench, [README](https://github.com/yzhao062/awesome-auditable-ai)).
  - Full traces raise attribution accuracy by up to 76% ([TraceElephant Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/04/24/seeing-the-whole-elephant-a-benchmark-for-failure-attribution-in-llm-based-multi.md)).
  - Arxiv 2609.06445 contributes a traceability specification and notes the gap in the EU AI Act timeline (Art. 86 applies from 2026-08-02; Art. 12 logging deferred to 2027-12-02) ([vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2609-06445.md)).
  - GRADE grades dependency edges as observed, declared or inferred ([README](https://github.com/yzhao062/grade)).
  - IET recovers attribution when only the final text survives ([Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/03/18/when-only-the-final-text-survives-implicit-execution-tracing-for-multi-agent-att.md)).
  - Who&When Pro needs legible reasoning (secondary; [howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx)).
- **Calibration and uncertainty**:
  - Conformal Agent Error Attribution returns contiguous step sets with coverage guarantees ([README list, arXiv 2605.06788](https://github.com/yzhao062/awesome-auditable-ai)).
  - MP-Bench uses multi-perspective nDCG ([Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/03/26/rethinking-failure-attribution-in-multi-agent-systems-a-multi-perspective-benchm.md)).
  - CAR reports confidence intervals on every effect ([Q&A](https://github.com/CMander02/DailyAgentPapers/blob/main/data/2026/06/06/causal-agent-replay-counterfactual-attribution-for-llm-agent-failures.md)).
  - VerifyMAS and CHIEF name calibration and uncertainty as future work (see Q4).
  - A pilot harness models a "typed external uncertainty field" over Who&When steps ([maej-uq](https://github.com/iamtaehyunpark/maej-uq)).
- **Coordination errors mislabelled**: on multimodal traces, more than half of non-reasoning errors are absorbed into "reasoning error" (Who&When Pro, secondary; [howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx)). DoVer finds orchestrator-versus-sub-agent ambiguity in 5 of 14 uncertain cases ([DoVer text](https://github.com/geostigma-hj/on_policy_intervention/blob/main/chat_history/ChatGPT-DoVer_%E6%96%87%E7%AB%A0%E8%A7%A3%E8%AF%BB.md)). The Model-or-Harness taxonomy assigns faults to component edges and repair sides ([vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-28802.md)).
- **Computer-use and embodied**:
  - CUADebug: 204 OSWorld failures, a 30-subtype taxonomy, and joint subtype-and-step accuracy of 11.2% → 19.6% ([cn-chat-arxiv](https://github.com/qhduan/cn-chat-arxiv/blob/master/papers/26/08/2608.02643.json); [README list](https://github.com/yzhao062/awesome-auditable-ai)).
  - Who&When Pro (secondary): step accuracy is highest on text; error-mode classification rises from about 17% on text to about 37% on video ([howard86](https://github.com/howard86/howardism/blob/main/apps/blog/src/content/articles/automated-failure-attribution.mdx)).
  - The robotics paper BATON (arXiv 2608.16889) gets stage-level attribution *by construction* by exploring subtasks separately — [summary](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-08/2608.16889.md).
- **Attribution to components**: "Model or Harness?" argues outcome labels cause a "repair-assignment problem" ([vybe](https://github.com/rxmna8502/vybe-intelligence-vault/blob/main/ai/agents/arxiv-2607-28802.md)). Ecdysis separates model faults from harness faults across instances ([summary](https://github.com/xianshang33/llm-paper-daily/blob/main/summary_en/2026-09/2609.11677.md)).

### Inferences
- **Gap 1: "minimal sufficient logging for attribution".** This fits auditable AI best and is feasible for a newcomer. On TraceElephant (full traces) and SymFail (event graphs), systematically ablate trace fields: inputs, tool arguments, timestamps, dependency edges, reasoning text, OpenTelemetry/OpenInference-only views. Then measure (a) attribution accuracy and (b) interventional identifiability, and derive a schema with the minimal field set that preserves X% of attribution utility. The novelty over TelemetrySuffBench and TraceElephant would be a *field-level* sufficiency analysis grounded in interventional labels plus a proposed standard (OpenTelemetry semantic-convention extension). Cost is low.
- **Gap 2: calibrated set-valued attribution**, i.e. conformal sets calibrated against interventional rather than human labels, with abstention. It is novel if it combines (a) with the existing conformal work (arXiv 2605.06788). Medium feasibility.
- **Gap 4: embodied/VLA attribution** needs simulators and physical replay. It is high-risk for a 3–6-month newcomer project.

### Gaps
- No paper found evaluates attribution under summarized or encrypted reasoning traces. This is a potential gap, but Who&When Pro's statement about legibility is only secondary evidence.
- No embodied/VLA failure-attribution benchmark was found. The search could not reach arXiv listings directly, so this is not conclusive.
