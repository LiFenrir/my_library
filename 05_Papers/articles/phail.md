# PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology

- **arXiv**: [2605.29710](https://arxiv.org/abs/2605.29710)
- **Project**: https://phail.ai
- **Code**: https://github.com/Positronic-Robotics/phail-paper
- **Author**: Sergey Arkhangelskiy, Positronic Robotics (`s@positronic.ro`)

## Abstract

Real-world evaluation of vision-language-action (VLA) policies still rests on binary success rate at a fixed timeout with $N \leq 2 5$ rollouts per condition, almost always without confidence intervals or paired statistical comparison – cohort sizes that struggle to resolve close comparisons reliably. We introduce PhAIL (Physical AI Leaderboard, https://phail.ai), an open real-robot benchmark on a Franka FR3 – dataset, per-rollout artifacts, and end-to-end reference implementation – of a distributional evaluation methodology: the time-to-success cumulative distribution function (CDF) as the evaluation primitive, with two separated jobs – scoring (Human-Relative Throughput, HRT – a dimensionless scalar with bootstrap confidence intervals, anchored to same-fixture human teleoperation) and a significance test (Kolmogorov–Smirnov, computed per-object and macro-averaged across objects). On four publicly-available VLAs, the macro-averaged KS test resolves two close comparisons (GR00T vs. ACT, OpenPI vs. ACT) at $N \leq 3 0$ rollouts per (model, object) cell where binary-threshold metrics do not – the closest pair (OpenPI vs. GR00T) remains unresolved within our budget. The best evaluated VLA is ∼7× slower per operation (RMST ratio) than the human reference.

## 1 Introduction

How do you tell whether one robot policy is better than another in the real world? Most published evaluations of vision-language-action (VLA) policies answer this with binary success rate at a fixed timeout, $N \leq 2 5$ rollouts per condition, no confidence intervals, no paired test – a depth that is an order of magnitude below the budget the binary tests they implicitly use require for reliable ranking. Sampling noise can therefore obscure genuine ordering effects on cohorts the field can practically grow.

The standard fix the field has reached for – adding a throughput metric (units per hour (UPH), cycle time, completion fraction) alongside binary success – works in part but surfaces a deeper problem: when the two scalars rank policies in different orders, the choice between them is task-dependent and rarely disclosed in print. Recent methodology critiques argue that blinded same-session A/B with hundreds of rollouts is feasible [23, 24], and the closest ML-side precedent for distributional comparison [25] extends the conversation toward distributions. None of these recommendations ships a primitive plus a reference implementation that lets the field apply them on a shared station.

We respond by adopting the time-to-success CDF as the evaluation primitive. Let T be the wall-clock time the policy needs to complete one operation; hard failures (items lost outside the workspace, items dropped on the table at episode end, safety stops) are absorbed as $T = \infty$ ghost events rather than censored tails. The resulting CDF $F ( t ) = P ( T \leq t )$ jointly carries reliability (the gap between its asymptote and 1 equals the hard-failure rate) and throughput (the median of T , and UPH ∝ $1 / E [ \dot { T } \mid \dot { T } < \infty ] )$ . Standard scalars – success rate at τ , UPH, mean time between failures/assists (MTBF/A), completion fraction, restricted mean survival time (RMST) – are projections of F , and the CDF is strictly richer than any of them: when two CDFs cross, no single scalar suffices and reasonable scalars give opposite signs on the same data. We separate two methodological jobs that current practice runs together: scoring (a scalar with bootstrap confidence intervals (CIs) – Human-Relative Throughput, HRT, anchored to a same-fixture human reference) and a significance test (macro-averaged KS computed per-object on the time-to-success CDFs). PhAIL is the open real-world inference benchmark that instantiates this methodology on a Franka FR3 across four objects.

Empirically, on four publicly-available VLAs – OpenPI $\pi _ { 0 . 5 }$ [29], GR00T N1.6 [30], ACT [31], SmolVLA [32] – the best is roughly 7× slower per operation (RMST ratio) than the human reference, the top two are statistically indistinguishable on every metric tested, and SmolVLA is clearly worst. The choice of test, not just the choice of N, determines what is resolvable: macro-averaged KS detects the GR00T-vs-ACT difference at N =25 and the OpenPI-vs-ACT difference at N =30 rollouts per (model, object) cell, while a stratified-McNemar binary baseline on a 5 pp paired difference needs 600–1500 paired rollouts per cell [7, 8] – roughly 30× more rollouts at the unit both tests stratify on (this ratio reflects our chosen binary baseline and per-object CDF shapes; the methodology, not the multiplier, is what generalizes). The field’s modal $\mathrm { \bar { ~ } } N \leq \mathrm { \bar { 2 } } 5$ is therefore an order of magnitude or more below the per-cell binary-test budget at our effect size.

## Contributions.

1. Time-to-success CDF as the evaluation primitive, with hard failures absorbed as $T = \infty$ ghost events (Figure 1a). Standard scalars are projections; we propose macro-averaged Human-Relative Throughput (HRT) as the dimensionless headline scalar grounded in a same-fixture human reference.

2. Same data, opposite rankings – no single scalar suffices. Principled aggregations of the same CDF disagree on top-1, so the choice of headline scalar is a disclosed methodological commitment.

3. For distinguishing close-pair policies, the macro-averaged KS test is roughly 30× more sample-efficient per cell than stratified binary-threshold baselines (Figure 1b) – an advantage rooted in test design rather than dataset specifics (§3.3). Scoring (HRT for ranking) and the significance test (KS for distinguishability) are separate jobs, and for the significance step the choice of test, not the choice of N, is what drives sample efficiency.

4. PhAIL: open real-world benchmark with auditable artifact. Beyond the statistical method ology, four robotics-side contributions: (i) a real-robot dataset of ∼990 episodes (including 396 same-fixture human-teleoperation reference rollouts) on a Franka FR3, four trained objects; (ii) a same-fixture human-reference protocol that turns embodiment-specific timings into a dimensionless ratio; (iii) operationally-grounded failure semantics (recovery-impossible outcomes as $T { = } \infty$ ghost events, recoverable slow tails left censored); (iv) per-rollout synchronized video, telemetry, and event annotations auditable through a public run-explorer interface – every annotation is reproducible from the raw rollout. Blinded same-session randomized rotation is the single protocol recommendation that does the most work (Appendix G).

Scope. The methodological contribution is the comparison primitive, the resolution procedure, the power budget, and the open framework that makes new claims auditable. The methodology is task agnostic – it applies to any operation with an unambiguous success event and a same-fixture human reference. PhAIL’s current empirical validation is bin-to-bin pick-and-place across four objects (§4); subsequent releases will add insertion and small-part assembly, with the methodology unchanged across additions, and other natural fits include packing, navigation, and articulated manipulation. The per-model rankings are illustrative of what the methodology can resolve at our depth, not architectural pronouncements; we used each repository’s default fine-tuning recipe (§4.2). PhAIL is open to submissions.

## 2 Related Work

Existing real-robot evaluation protocols. RoboArena [13] and RoboChallenge [12] use physical robots but compare via pairwise Elo or scalar success on standardized tasks; neither reports confidence intervals or paired tests on the rankings. Competition-style evaluations (RGMC, OCRTOC [19],

![[99_Attachments/papers/images/phail/87002709ca2ba992870853d12919f53c3af549fdd73f9e6777ef5097bfd91596.jpg]]

![[99_Attachments/papers/images/phail/06b4d949311838ee9ce12f737b7e89e5988fc8bb69bb0ccaf47b7b19252b4f52.jpg]]  
Figure 1: (a) Time-to-success CDFs are richer than any scalar: reliability and throughput on a single axis. The four VLAs all sit far below the human reference – the best is ${ \sim } 7 \times$ slower. Hard failures become the asymptote below $F = 1$ . (b) Choosing the right test, not just running more trials, is what resolves close comparisons: macro-averaged Kolmogorov–Smirnov across per-object CDFs reaches 80% detection on GR00T vs. ACT at $N { = } 2 5$ rollouts per (model, object) cell, while binary success-rate-at-threshold $( F ( 3 0 s )$ , F (60s)) and integrated RMST fall well short of the target on every close pair across the entire $\mathrm { \Delta \ddot { N } \leq \dot { 3 } 0 }$ range. The dominant practice $( F ( \tau )$ at modal $N \leq 2 5 )$ is underpowered for ranking close pairs at this depth.

NIST Assembly Task Boards [20], the Real Robot Challenge [21], surveyed in [18]) standardize task scoring without statistical machinery; closest in spirit is the Digital Robot Judge [22], which builds task-centric performance databases via electronic task boards but reports raw telemetry only. The most rigorous existing real-robot evaluation is the LBM examination [24], which runs blinded same-session A/B at $N { = } 5 0 { \mathrm { - } } \bar { 2 } 0 0$ per condition with Bayesian posterior violins on success rate, paired Barnard’s exact tests for binary outcomes, Welch’s t-tests for a scalar task-completion score, and Bonferronicorrected significance grouping – a strong precedent for what rigorous real-robot evaluation looks like. PhAIL’s contribution is orthogonal to LBM’s: a richer primitive (time-to-success CDF with $T { = } \infty$ ghost events, jointly carrying reliability and throughput) and a same-fixture human-reference anchor that turns embodiment-specific timings into a dimensionless ratio. Simulated benchmarks (RoboCasa, CALVIN, ManiSkill, SIMPLER [14, 15, 16, 17]) iterate fast but miss real-world perception, latency, and safety; they are complementary, not substitutes.

Methodology critiques. Kress-Gazit et al. [23] and STEP [27] argue current real-robot evaluation is statistically underpowered and recommend blinded same-session A/B at hundreds of rollouts; Agarwal et al. [25] is the closest ML-side precedent for distributional comparison. We extend the distributional approach to time-to-event data with $T { = } \infty$ ghost events and ship a reference implementation on a shared station. A 13-paper survey of recent VLA evaluation practice (Appendix A) confirms modal per-condition N is 10–20 and none of the 13 standard-practice papers report confidence intervals or paired tests; LBM is the single recent counter-example.

## 3 Time-to-Success CDF as Evaluation Primitive

The methodology has three components: the random variable and its CDF (§3.1), the scoring layer (scalars and visualizations derived from the CDF, §3.2), and the significance layer (distributional tests on the CDF, §3.3). The strict separation between scoring (which ranks via a scalar’s CI) and significance (which tests whether two policies’ CDFs differ at all) is the methodological core. We use concrete language drawn from our running bin-to-bin pick-and-place setup (formal description in §4) – successful placements, items dropped outside the workspace – but the framework applies unchanged to any operation with an unambiguous success event, a measurable time-to-success, an identifiable notion of hard failure (states from which the policy cannot recover), and a same-fixture human-reference baseline.

![[99_Attachments/papers/images/phail/e93f1132e51f8d944467204dfe9f8106032604c3b3184c04ce88f971878e34bc.jpg]]

![[99_Attachments/papers/images/phail/3edeca5d7d00e77f229361e7cc34c09e77784e1526f9daad59d5cfe55e2a5013.jpg]]  
Figure 2: One (model, object) cell (ACT on Batteries) illustrating the scoring layer: time-to-success CDFs (left) and the corresponding P-P plot (right). Left: model and human-reference CDFs on the same axis; the asymptote below $F = 1$ on the model curve is the hard-failure rate. Right: $\left( F _ { \mathrm { H u m a n } } ( t ) , F _ { \mathrm { m o d e l } } ( t ) \right)$ traced parametrically as t sweeps. Diagonal = as fast as the human reference; below-diagonal = slower. The shaded area under the curve is the AUC $P ( T _ { \mathrm { m o d e l } } < T _ { \mathrm { H u m a n } } )$ ; the perpendicular distance from the curve to the diagonal at the point of maximum separation (red segment) equals $\mathrm { K S / \sqrt { 2 } } .$ , where KS is the Kolmogorov-Smirnov statistic.

## 3.1 The Random Variable T

For a single rollout episode with multiple operations to perform, we extract a sequence of timesto-success $T _ { i }$ and event indicators $E _ { i } \ \mathrm { ~ \bar { \in ~ } \{ 0 , 1 \} ~ }$ . A successful placement contributes $T _ { i }$ equal to the elapsed time since the previous successful placement (or since episode start, for the first), with $E _ { i } = 1$ . If the episode ends with operations remaining (operator stopped or timed out), the unfinished attempt contributes one right-censored pair $( T _ { \mathrm { t a i l } } , 0 )$ where $T _ { \mathrm { t a i l } } = \mathrm { d u r a t i o n } - \mathrm { l a s t }$ placement time; $E = 0$ means we know $T > T _ { \mathrm { t a i l } }$ but do not observe T .

Hard failures as $T = \infty$ ghost events. Operations that end in unrecoverable states (items lost outside the workspace; items dropped within the workspace and still uncollected at episode end; the single operation that triggered a safety stop) are absorbed as $( T = \infty , E = 1 )$ ghost events: the operation did terminate (so $E = 1$ , not censored) but at $T = \infty$ . The CDF carries this as an asymptote below $F = 1$ ; the gap between the asymptote and $F = 1$ equals the hard-failure rate. Timeouts are explicitly not ghost events: they are slow-but-recoverable runs that belong in the censored tail, where they correctly indicate “the policy was working when we stopped watching it.”

Estimation and censoring. The CDF $F ( t ) = P ( T \leq t )$ is estimated by the Kaplan-Meier productlimit estimator [1] on the $( T , E )$ collection. Confidence intervals on derived scalars (RMST, HRT, $F ( \tau )$ at fixed thresholds) are reported via 95% episode-clustered bootstrap [4]. Episodes with zero successes contribute a single right-censored observation of length $\tau _ { \mathrm { e p i s o d e } } .$ , the per-rollout time budget after which an unfinished operation is censored (set by the protocol; §4.2); we never drop them. The $T = \infty$ atom is handled directly by the estimator (a discrete jump at the right edge); for the integrated-metric calculation in §3.2 we set $T _ { \mathrm { g h o s t } }  \tau$ , the integration cap, so a hard failure inflates RMST by exactly τ minus the time the model would have spent on that operation if successful.

## 3.2 Scoring: Scalars and Visualizations from the CDF

The CDF carries the full distribution of time-to-success T (it is strictly richer than any single scalar derived from it; the rollout itself retains more, e.g. visual context and recovery behavior). The scalars commonly reported in VLA evaluations are projections of F (Table 1); reporting any single one without the CDF discards information. Two mechanisms make this concrete in our data. First, when two CDFs cross, different reasonable scalars give opposite top-1 rankings – our policies show this empirically: ACT ranks third under integrated RMST/HRT but first under pairwise AUC against the human reference (§5.3). Second, even within a single scalar family the choice of integration cap can

flip orderings: throughput-oriented UPH falls with $\tau _ { \mathrm { e p i s o d e } }$ while reliability-oriented MTBF/A rises, and the trade-off survives macro-aggregation across objects (Appendix L). A scalar is therefore not just a lossy summary – it is a methodological commitment to weighting one regime of the CDF over another.

| Scalar                                         | Functional of $F(t)$                                                        |
| ---------------------------------------------- | --------------------------------------------------------------------------- |
| Success rate at $\tau$                         | $F(\tau)$                                                                   |
| Median time-to-success                         | $\inf\{t : F(t) \geq 0.5\}$                                                 |
| RMST( $\tau$ ) (restricted-mean survival time) | $\int_{0}^{\tau} (1 - F(t)) dt$                                             |
| UPH (units per hour)                           | $3600 / E[T \mid T < \tau_{episode}] \propto 1/\text{RMST}(\tau_{episode})$ |
| Completion fraction                            | $F(\tau_{episode})$                                                         |
| MTBF/A (mean time between failures/assists)    | $\text{RMST}(\tau_{episode}) / (1 - F(\tau_{episode}))$                     |

Table 1: Standard scalar metrics expressed as functionals of the time-to-success CDF $\overline { { F ( t ) } }$ . The per-rollout time budget $\tau _ { \mathrm { e p i s o d e } }$ is the protocol’s timeout $( \ S 4 . 2 ) ; 1 - F \big ( \tau _ { \mathrm { e p i s o d e } } \big )$ is the hard-failure rate (operations that did not complete within budget, including $T = \infty$ ghost events).

Headline scalar: Human-Relative Throughput (HRT). For each (model, object) cell we compute

$$
\mathrm{HRT} (m, o) = \frac {\mathrm{RMST} _ {\text { Human } , o} (\tau)}{\mathrm{RMST} _ {m , o} (\tau)}, \quad \tau = 2 4 0 \mathrm{s},
$$

the cell-wise ratio of human-reference to model RMST, reported as a percentage, and macroaggregated across objects with equal weights. Three properties make this an appropriate scalar to report. (i) It inherits the $\mathrm { C D F } \mathbf { s }$ joint speed-and-completion property via $T = \infty$ inflating RMST<sub>model</sub>. (ii) It is grounded in operator practice (UPH-equivalent against a same-fixture human reference, so embodiment confounds cancel). (iii) Cell-wise normalization partially cancels object-difficulty differences. A hard object slows both the human and the policy, so the ratio is more stable across tasks than absolute throughputs; the cancellation is approximate (slowdown is not strictly multiplicative – see the Q-Q plots in Appendix L), and macro-averaging across objects further reduces residual heterogeneity. Cross-deployment comparison (different operators, different rooms, different reference pacing) reduces to comparing ratios, not absolute throughputs. HRT is a benchmark scalar that captures wall-clock per operation under the protocol’s time cap; production throughput additionally depends on reset, recovery, and intervention time outside the per-operation envelope and is therefore not a direct multiple of HRT.

Visualization: P-P plots. For a (model, object) cell, the P-P plot traces $\left( F _ { \mathrm { H u m a n } } ( t ) , F _ { \mathrm { m o d e l } } ( t ) \right)$ parametrically as t sweeps from 0 to τ . The diagonal is “as fast as the human reference”; below-diagonal is slower; above-diagonal is faster. Two derived properties give the P-P curve its analytic value. The area under the curve equals $P ( T _ { \mathrm { m o d e l } } < T _ { \mathrm { H u m a n } } )$ , the pairwise stochastic-dominance probability (AUC). The maximum vertical distance from the curve to the diagonal equals the Kolmogorov-Smirnov distance between the two CDFs (§3.3); the P-P plot is therefore the natural visualization for both. Figure 2 shows one (model, object) cell’s CDF and the corresponding P-P plot side by side. P-P plots make distributional shape legible (saturation, early-success peaks, tail behavior); we use them descriptively in §5.3.

Confidence intervals. All scoring scalars and CDF curves carry 95% episode-clustered bootstrap intervals [4]. We resample whole episodes (not operations within episodes) because operations within an episode are correlated by the rollout’s initial scene configuration (starting positions of items in the inbound tote), shared visual conditions, and policy state; per-operation bootstrap produces over-narrow intervals.

## 3.3 Ranking: Distributional Tests on the CDF

Reporting a scalar with a CI is one job; deciding whether two policies’ underlying distributions differ – and if so, in what direction – is a different job. We treat it as such. By resolution we mean the joint claim of significance plus direction, with three possible outcomes: (i) A is better than B (CDFs separate, consistently signed – one dominates the other across t); (ii) A and B differ but neither is uniformly better (CDFs cross – reasonable scalars give opposite signs because they weight different regions of the curve, so disagreement among scalars is the CDF’s signal that the policies have different distributional shapes, not a scalar bug); (iii) A and B are indistinguishable at the available N.

Our primary test for the significance gate (regimes (i)+(ii) vs (iii)) is the two-sample Kolmogorov– Smirnov statistic [3], computed separately on each (model, object) cell’s CDF and macro-averaged across objects with equal weights:

$$
D _ {o} = \sup _ {t} \left| F _ {o} ^ {(a)} (t) - F _ {o} ^ {(b)} (t) \right|, \qquad \bar {D} = \frac {1}{J} \sum_ {o} D _ {o}.
$$

Per-object computation matches the macro-aggregation used by HRT (§3.2), gives each object equal weight in the resolution verdict regardless of operation count, and prevents object-difficulty differences from contaminating the test statistic. Equal object weighting is a deliberate benchmark design choice, not a statistical default: a pooled-across-objects KS would average object-level discrepancies that occur at different timepoints and dilute them; macro-KS preserves them. We validate that this custom statistic is correctly Type-I calibrated under three null setups in Appendix J. The CDFs $F _ { o } ^ { ( \cdot ) }$ are Kaplan–Meier estimates and p-values come from a pooled-resample episode-clustered bootstrap [4] – under $H _ { 0 } : F _ { a } = F _ { b }$ we pool the two policies’ episodes per object and resample with replacement into arms of the original sizes – so the test is calibrated empirically rather than from the asymptotic Kolmogorov distribution, which makes it robust to right-censoring and to within-episode correlation by construction. “Matching” between policies here is at the (model, object) cell level (both policies are evaluated on the same four objects on the same fixture), not at the scene level: initial physical configurations are not replayed between policies. Geometrically, each $D _ { o }$ is the maximum vertical distance from the P-P plot of $F _ { o } ^ { ( a ) }$ versus $\bar { F } _ { o } ^ { ( b ) }$ to the diagonal (Figure 2). As a sanity-check we report stratified pooled-across-objects logrank [2] with Bonferroni correction over the model pairs. Direction (outcome (i) vs (ii)) comes from a scalar – in our case the macro RMST difference, equivalent to signed Wasserstein-1 in 1D – with outcome (ii) surfaced when reasonable scalars disagree (§5.3).

Why the test choice matters more than the choice of N. The KS test is consistent against any alternative $F _ { a } \neq F _ { b }$ (classical nonparametric result; Lehmann & Romano [5] §14.2): given enough samples, any distributional difference becomes detectable. A test based on any scalar functional $T ( \bar { F } )$ – success rate at a threshold, RMST, AUC vs. a reference, MTBF/A, completion fraction – is consistent only against alternatives where $T ( F _ { a } ) \neq T ( F _ { b } )$ ; whole classes of CDF differences are invisible to that scalar’s test irrespective of N . This advantage lives at the significance step (outcome (i)+(ii) vs (iii) above); ranking (outcome (i) vs (ii)) reads off the scoring scalar’s CI, since the KS sign is not a coherent ranker – Appendix I constructs three CDFs whose pairwise sup-signs cycle $\bar { A \succ } B { \succ } C { \succ } A$

## 4 PhAIL: Design, Protocol, and Power Budget

## 4.1 Platform and Task

The evaluation station uses a DROID-style configuration [11]: a Franka Research 3 with a Robotiq 2F-85 parallel-jaw gripper, plus over-the-shoulder external and wrist-mounted RGB cameras. The task is bin-to-bin order picking across four object types spanning a useful slice of physical regimes – wooden spoons (rigid, elongated, multi-grasp), towels (deformable), scissors (articulated, metallic), and batteries (small, rigid). Each rollout contains many independent placement operations, which we exploit for sample size. The same hardware operates the human reference and every evaluated VLA via the open-source positronic framework [10], so only weights and architecture-specific observation-to-action code differ across submissions. Every rollout is published with synchronized video, telemetry, and event annotations, browsable in a run-explorer interface (Figure 4, Appendix B; annotation pipeline in Appendix E). Artifacts: https://phail.ai; analysis pipeline and paper source at https://github.com/Positronic-Robotics/phail-paper.

## 4.2 Models, Fine-Tuning, and Protocol

We evaluate four publicly available VLAs: OpenPI $\pi _ { 0 . 5 }$ [29] (3B-param, FAST action tokenization on flow-matching), GR00T N1.6 [30] (3B-param, Cosmos-Reason VLM + 32-layer diffusion transformer action head), ACT [31] (Action Chunking Transformer, CVAE), and SmolVLA [32] (450M-param, HuggingFace/LeRobot). None has zero-shot capability on this task, so fine-tuning is a prerequisite. All four were fine-tuned on the same 449-episode bin-to-bin demonstration set (∼13 hours; Appendix C) using each repository’s default recipe – no per-model hyperparameter search. This is a deliberate methodological constraint, not best practice for production deployment; per-model recipe optimization could shift the rankings of §5.

Each rollout has a 30 s/item time cap (∼10× the ∼2.7 s/item human pace). Evaluation is blind: the scheduler randomly selects which model runs next, the operator does not know which is running, and the operator’s only intervention is triggering a safety stop. Post-rollout, the operator records target/source counts, items lost outside both bins, and outcome label ∈ {Success, Safety, Ran\_out\_of\_time}; every successful placement is annotated post-hoc from the rollout video (Appendix E).

## 4.3 Cohort and Power Budget

After object/model filtering, ∼995 episodes enter the analyses; 396 are human reference rollouts. The operator was blinded to which model was running during each rollout (§4.2). Annotations combine an automated detector with manual per-candidate review for the ∼40% of episodes where the two disagreed (Appendix E); the ranking is robust to which label-stream subset we use, but annotator bias is not directly controlled here – see Limitations.

How many rollouts does a ranking claim actually need? Standard power calculations (Appendix H) put the field-modal N=10–20 (Appendix A) orders of magnitude under-budget: a ±5 pp Wilson CI on a single arm needs N ≈380, detecting a 5 pp paired difference between two policies (McNemar [7], 80% power, α=0.05) needs 600–1500 paired rollouts following Connor’s [8] sample-size formula, while a per-object Brownian-bridge functional simulation against the empirical CDFs (Appendix H) predicts $\dot { N } _ { 0 . 8 } \dot { \leq } 3 0$ per cell for two of the three close pairs and ≈ 45 per cell for the closest. Our own N ≈ 35 per cell is 2–3× the field median but still well below any of these thresholds; §5.2 confirms this empirically with detection-rate-vs-N curves on our data.

## 5 Results

All numbers below use τ = 240 s for RMST, $n _ { \mathrm { b o o t } } = 1 0 0 0$ for episode-clustered bootstrap CIs, seed 0. Per-(model, object) cell sizes are 32–46 episodes for OpenPI, GR00T, and ACT; 26–34 for SmolVLA.

## 5.1 Headline Ranking

| Model | RMST (s) [95% CI] | HRT (%) [95% CI] | Intervention rate | Episodes |
|---|---|---|---|---|
| Human reference (teleop) | 10.5 [10.3, 10.8] | 100.0 | — | 396 |
| Physical Intelligence Open $\pi_{0.5}$ | 77.7 [69.2, 87.0] | 13.8 [12.2, 15.7] | 4.2% | 165 |
| NVIDIA GR00T N1.6 | 77.2 [69.0, 86.4] | 13.3 [12.0, 15.2] | 4.2% | 165 |
| Action Chunking Transformer | 100.9 [85.8, 117.6] | 10.5 [9.2, 13.2] | 2.0% | 151 |
| Hugging Face SmolVLA | 165.8 [147.0, 185.6] | 6.4 [5.7, 7.5] | 18.6% | 118 |

Table 2: Headline ranking $( \tau = 2 4 0 \mathrm { s } , N$ ≈ 35/cell). RMST and HRT carry 95% episode-clustered bootstrap CIs $( n _ { \mathrm { b o o t } } = 1 0 0 0 )$ . HRT is the per-(model, object) reference-to-model RMST ratio, macro-averaged across four trained objects (the definition of §3.2). Intervention rate is safety stops / total episodes (lower bound; drops outside the workspace not included).

OpenPI and GR00T are within 0.5 percentage points of HRT, their 95% CIs overlap almost entirely ([12.2, 15.7] vs. [12.0, 15.2]), and they swap order between HRT (per-cell macro mean) and global RMST – two principled aggregations of the same primitive on this benchmark. The CDF-level test agrees by failing to reject the pair (logrank $p = 0 . 5 4$ , Table 3): both the ordering tool (HRTwith-CI) and the significance tool (KS) deliver the same verdict for these two policies at this N – indistinguishable. No inference model exceeds 19% HRT on any single object (per-cell RMST grid, Figure 6). Even the best VLA tested is roughly 7× slower than the human on the same fixture.

The asymptote-below-1 in Figure 1a aggregates drop-outs (per-operation $T { = } \infty$ ghost), safety stops (per-episode ghost), and censored timeouts; the same asymptote height can come from very different mixes $- \mathrm { A C T ^ { 3 } s }$ drop-out rate and SmolVLA’s safety-stop rate point to qualitatively different failure modes that a single hard-failure number would equate. Per-model rates in Appendix F.

| Pair | p (raw) | p (Bonferroni) | Significance |
|---|---|---|---|
| OpenPI vs. SmolVLA | $<10^{-15}$ | $<10^{-14}$ | *** |
| GR00T vs. SmolVLA | $<10^{-15}$ | $<10^{-14}$ | *** |
| ACT vs. SmolVLA | $8.9 \times 10^{-16}$ | $5.3 \times 10^{-15}$ | *** |
| GR00T vs. ACT | $1.7 \times 10^{-4}$ | $1.0 \times 10^{-3}$ | ** |
| OpenPI vs. ACT | $7.2 \times 10^{-4}$ | $4.3 \times 10^{-3}$ | ** |
| OpenPI vs. GR00T | $5.4 \times 10^{-1}$ | 1.00 | n.s. |

Table 3: Pooled-across-objects logrank, Bonferroni-corrected over the 6 model-pairs.

The top two inference models cluster as statistically indistinguishable; ACT is separable from both GR00T and OpenPI; SmolVLA is distinguishably worst. At N ≈ 37/cell – already $\pmb { 2 - 3 } \times$ the field-modal N – the closest pair (OpenPI vs. GR00T) remains unresolved by every test: pooled logrank $( p = 0 . 5 4$ , Table 3) and per-object macro KS $( p = 0 . 1 2 )$ both fall short, consistent with the Appendix H prediction that this pair specifically needs N ≈ 45/cell to clear 80% power.

What the field’s standard methodology would have said. At the modal $\tau { = } 3 0 \mathrm { s } ,$ , the binary leader is GR00T (0.51) with OpenPI (0.47) and ACT (0.44) close behind. Under HRT (per-cell macro mean of §3.2) the leader is OpenPI (Table 2); under global RMST it is GR00T with OpenPI a hair behind; under AUC-vs-human the leader is ACT (§5.3). Four principled scalar choices on the same data yield three different top-1 rankings, and Table 4 shows that no binary-threshold metric distinguishes the close pairs on the underlying CDF at $N \leq 3 0$ . A field-standard $\tau { = } 3 0$ -second leaderboard at $N { = } 1 5$ would surface a top-1 that depends on which random subsample is drawn, without the statistical resolution to back the resulting choice.

## 5.2 Sample Efficiency: The Right Test, Not the Right Scalar

The headline above leans on RMST and pooled logrank. We now ask the operational question: at fixed N, which metric most reliably resolves a pairwise comparison? Three contestants are tested side-by-side as significance tests: binary $F ( \mathrm { 3 0 s } ) ~ / ~ F ( \mathrm { 6 0 \bar { s } } )$ (the field’s current practice), RMST-as-scalar (a CDF-aware scoring scalar used as a test statistic), and macro-averaged KS across per-object CDFs (the distributional test we propose). For each pair of inference models and each $\mathbf { \bar { \Delta } } N \in \{ 5 , 1 0 , 1 5 , 2 0 , 2 5 , 3 0 \}$ per (model, object) cell, we ran 300 outer subsampling trials. Each trial subsamples N episodes per cell with replacement, then runs a 200-rep inner episode-clustered bootstrap to compute a two-sided p-value for the difference of each candidate metric (macro-averaged across objects, RMST and KS computed at $\tau = 1 2 0$ s for the efficiency experiment to reduce rightcensoring at small N ; the tail-heavy slowdown documented in Appendix L confirms most inter-model separation is already present by $\tau = 1 2 0 \mathrm { s } )$ . Detection rate is the fraction of trials with $p < 0 . 0 5$ Figure 1b shows the result for the borderline pair GR00T vs. ACT; Figure 3 shows the three pairs that carry efficiency information.

The table reads in three regimes. Three saturated pairs (any inference model vs. SmolVLA): all metrics work; effects are large; binary baselines are slightly faster than KS at saturation because the pooled-resample $H _ { 0 }$ calibration is conservative when effects are huge. Three close pairs (the three top-3 model pairs) – the bucket where sample efficiency actually matters. KS reaches the 80% target on two of the three: GR00T vs. ACT at N=25 and OpenPI vs. ACT at $N { = } 3 0$ . The closest pair, OpenPI vs. GR00T, remains unresolved within budget (KS at 0.63 at $N = 3 0 )$ , while $F ( 3 0 \mathrm { s } )$ $F ( 6 0 \mathrm { s } )$ ), and RMST fall well short of 0.8 on every close pair. KS dominates the binary baselines by a factor of 2–6 in detection rate at $N \leq 3 0$ across the three close pairs; resolving the closest pair to 80% empirically would require the 600–1500 paired rollouts the analytical power calculation predicts (§4.3).

![[99_Attachments/papers/images/phail/0603a02bf576fabc9d98afd88c80f2a50df4c0d925af4f5c77c4ca66bb6a24fe.jpg]]

Figure 3: Detection rate vs. subsample size N per (model, object) cell, on the three closest model pairs (left: OpenPI vs. GR00T, the closest; centre, right: the next two). Dashed line: the 0.8 power target. KS (red) climbs steeply on every pair while $\bar { F ( 3 0 s ) } , F ( 6 0 s )$ , and RMST stay near the floor. KS reaches 80% within budget on the centre and right pairs, while OpenPI vs. GR00T remains unresolved at N=30 (KS at 0.63). Pairs vs. SmolVLA saturate at $N = 5$ for every metric and are deferred to Appendix K.

| Pair | $F(30\ \text{s})$ | $F(60\ \text{s})$ | RMST | KS |
|---|---|---|---|---|
| OpenPI vs. GR00T | — | — | — | — |
| OpenPI vs. ACT | — | — | — | 30 |
| OpenPI vs. SmolVLA | 5 | 5 | 5 | 5 |
| GR00T vs. ACT | — | — | — | 25 |
| GR00T vs. SmolVLA | 5 | 5 | 5 | 10 |
| ACT vs. SmolVLA | 5 | 5 | 5 | 10 |

Table 4: Smallest tested N at which detection rate ≥ 0.8 per (pair, metric). $\overline { { { \bf 6 6 } \underbrace { { \bf - 3 9 } } } }$ means the detection rate did not reach 0.8 within the tested range $N \leq 3 0$ . KS is the only metric that crosses the threshold within budget on a close pair, and does so on two of three: GR00T vs. ACT at $N { = } 2 5$ and OpenPI vs. ACT at $\mathrm { \bar { \it N } = 3 0 }$ . The closest pair, OpenPI vs. GR00T, remains unresolved at N=30 (KS reaches 0.63). Every binary-threshold metric falls short of 0.8 on every close pair within budget.

Detection rate at $N = 3 0$ averaged across all six pairs: $F ( 3 0 { \mathrm { s } } ) = 0 . 5 5 , F ( 6 0 { \mathrm { s } } ) = 0 . 6 6 .$ , RMST $= 0 . 6 3 , \mathbf { K S } = 0 . 9 0$ . The +24 pp gain of KS over $\bar { F ( 6 0 \mathrm { s } ) }$ is concentrated entirely on the three close pairs.

Two takeaways. First, the CDF-level test (KS) is materially more sample-efficient than any single CDF-derived scalar test for distinguishability, with RMST-as-scalar essentially tying $F ( 6 0 \mathrm { s } )$ (confirming the scoring/significance split of §3). Second, the choice of test sets the distinguishability budget by an order of magnitude. The closest pair is undistinguishable at N=30 by every metric tested; the per-object KS bridge-functional model (Appendix H) predicts it would clear 80% power at N ≈ 45 per cell – a ∼50% budget increase, not the order-of-magnitude jump the McNemar binary baseline requires. The bridge-functional prediction matches the empirical KS curves to within 3 pp across $N \in [ 5 , 3 0 ]$ on all three close pairs.

## 5.3 Aggregation-Rule Disagreement

Both integrated RMST and AUC vs. human reference are principled scalars derived from the same CDF; the choice of which to extract is itself a methodological commitment. Macro-AUC across objects: ACT 0.134 [0.108, 0.162] > OpenPI 0.100 [0.084, 0.116] ≈ GR00T 0.095 [0.080, 0.110] > SmolVLA 0.027 [0.016, 0.036]. ACT is now highest among inference models; under integrated RMST/HRT it sits third behind GR00T and OpenPI. Two principled aggregations of the same data thus yield opposite top-1 rankings.

This is outcome (ii) of §3.3: ACT and OpenPI/GR00T are different (KS rejects) but neither is uniformly better – their CDFs cross, with ACT winning the early-time region (high AUC) and

OpenPI/GR00T winning the integrated region (low RMST). The disagreement is sharpened by the human reference being ∼7× faster than any evaluated VLA, collapsing the AUC integral onto the short-time region where ACT’s early-success peak wins more first-success races. When CDFs cross, no single scalar can summarize the comparison without weighting one region over another.

We recommend HRT as the default headline scalar – it inherits the CDF’s joint reliability-throughput property and matches operator-facing UPH practice; on a benchmark where reference and policies operated at comparable speeds, AUC-vs-human would track RMST closely. Pairwise model-vs-model AUC (Figure 7, Appendix K) places OpenPI, GR00T, and ACT within pairwise-AUC error bands of each other; this is not a contradiction with the logrank- and KS-based separation of ACT from OpenPI/GR00T reported in §5.1 – different tests pool and stratify differently, and pairwise AUC is a more conservative criterion than the macro-averaged KS used for the headline ranking. Per-(model, object) RMST (Figure 6, Appendix K) shows the GR00T-vs-ACT object crossing visible at our N but not clearing Bonferroni at $\alpha = 0 . 0 5 / 2 4$

## 6 Discussion and Conclusion

We introduced PhAIL, an open real-robot benchmark and distributional evaluation methodology for vision-language-action policies. The methodology adopts the time-to-success CDF as primitive, separates scoring (Human-Relative Throughput, for ranking) from a significance test (Kolmogorov– Smirnov macro-averaged across per-object CDFs, for distinguishability), and anchors to a samefixture human reference. Evaluating four publicly-available VLAs across four objects, two findings emerged: principled aggregation rules over the same CDF can yield opposite top-1 rankings, and the macro-averaged KS test, at our chosen baseline and effect size, resolves two of three close pairs at $N \leq 3 0$ rollouts per cell where binary-threshold metrics need ∼30× more (§3.3); the closest pair (OpenPI vs. GR00T) is unresolved within our budget.

Limitations. Single embodiment (Franka FR3, fixed cameras), single primitive (bin-to-bin pickand-place, four trained objects); the framework generalizes to any operation with a human reference and event-time outcome but the empirical validation does not. N≈35 per cell is 2–3× the field median but still below what binary metrics need to rank close pairs (§5.2); per-model rankings are illustrative. The single protocol recommendation that does the most work is blind, randomized rotation on the same fixture in the same session – spatial-configuration shifts (Appendix G) move outcomes by margins comparable to gaps between adjacent models (a single same-side vs. oppositeside camera/tote swap shifts GR00T’s completion rate by 22 pp, larger than the GR00T–OpenPI gap we are trying to resolve), contaminating the CDF if not controlled. Annotator bias is bounded by the labeling protocol. Manual review (∼42% of episodes, single non-blinded reviewer) does not change the success count per episode – the operator’s logged value is the source of truth – it only places per-item timestamps, with per-event timing uncertainty under one second; reviewers typically confirm algorithm-proposed candidates rather than placing them from scratch. Within an episode, mismarking the boundary between consecutive items redistributes time between two adjacent inter-success intervals without changing their sum, so RMST and KS are largely insensitive to such redistribution. The label-stream robustness check in Appendix E additionally produces the same ranking on the manually-reviewed cohort alone; future releases replace manual review with hardware sensing.

If the field adopts this methodology, three things change. Scalar choice becomes a disclosed commitment (HRT and AUC-vs-human encode different priorities). Pairwise comparisons become falsifiable via the CDF-level KS test: “we cannot resolve these at this N” becomes a publishable finding. The hidden cost of binary thresholds becomes visible: on this benchmark, the N needed to match what a CDF-level test resolves within budget is well beyond what the field currently runs. PhAIL (https://phail.ai) is open to submissions; insertion and small-part assembly are next.

## References

[1] Kaplan, E.L., Meier, P. Nonparametric Estimation from Incomplete Observations. Journal of the American Statistical Association, 53(282):457–481, 1958.

[2] Mantel, N. Evaluation of Survival Data and Two New Rank Order Statistics Arising in its Consideration. Cancer Chemotherapy Reports, 50(3):163–170, 1966.

[3] Smirnov, N.V. Table for Estimating the Goodness of Fit of Empirical Distributions. Annals of Mathematical Statistics, 19(2):279–281, 1948.

[4] Efron, B., Tibshirani, R.J. An Introduction to the Bootstrap. Chapman & Hall, 1993.

[5] Lehmann, E.L., Romano, J.P. Testing Statistical Hypotheses, 3rd ed. Springer, 2005.

[6] Wilson, E.B. Probable Inference, the Law of Succession, and Statistical Inference. Journal of the American Statistical Association, 22(158):209–212, 1927.

[7] McNemar, Q. Note on the Sampling Error of the Difference Between Correlated Proportions or Percentages. Psychometrika, 12(2):153–157, 1947.

[8] Connor, R.J. Sample Size for Testing Differences in Proportions for the Paired-Sample Design. Biometrics, 43(1):207–211, 1987.

[9] Rerun.io. Visualization SDK for Multimodal Data. https://rerun.io, 2024.

[10] Positronic Robotics. positronic: Open-source framework for real-robot evaluation and operation. https://github.com/Positronic-Robotics/positronic, 2025.

[11] Khazatsky et al. DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset. RSS, 2024.

[12] Tang et al. RoboChallenge: Large-scale Real-robot Evaluation of Embodied Policies. arXiv:2510.17950, 2025.

[13] Atreya et al. RoboArena: Distributed Real-World Evaluation of Generalist Robot Policies. arXiv:2506.18123, 2025.

[14] Nasiriany et al. RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots. arXiv, 2024.

[15] Mees et al. CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation. IEEE RA-L, 2022.

[16] Gu et al. ManiSkill3: GPU Parallelized Robotics Simulation and Benchmarking at Scale. arXiv:2410.00425, 2024.

[17] Li et al. Evaluating Real-World Robot Manipulation Policies in Simulation. arXiv, 2024.

[18] Sun, Falco, Roa, Calli. Research Challenges and Progress in Robotic Grasping and Manipulation Competitions. IEEE Robotics and Automation Letters, 2022.

[19] Liu et al. OCRTOC: A Cloud-Based Competition and Benchmark for Robotic Grasping and Manipulation. IEEE Robotics and Automation Letters, 2021.

[20] Falco et al. NIST Assembly Task Boards: Performance Metrics and Test Methods for Robotic Assembly. NIST IR / IEEE, ongoing.

[21] Bauer et al. A Robust Real Robot Baseline for the Real Robot Challenge. NeurIPS Datasets and Benchmarks, 2022.

[22] So, Sarabakha, Wu, Culha, Abu-Dakka, Haddadin. Digital Robot Judge: Building a Taskcentric Performance Database of Real-World Manipulation With Electronic Task Boards. IEEE Robotics & Automation Magazine, 2023.

[23] Kress-Gazit, Hashimoto, Kuppuswamy, Shah, Horgan, Richardson, Feng, Burchfiel. Robot Learning as an Empirical Science: Best Practices for Policy Evaluation. arXiv:2409.09491, 2024.

[24] TRI LBM Team, Barreiros et al. A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation. arXiv:2507.05331, 2025.

[25] Agarwal, Schwarzer, Castro, Courville, Bellemare. Deep Reinforcement Learning at the Edge of the Statistical Precipice. NeurIPS, 2021.

[26] Henderson, Islam, Bachman, Pineau, Precup, Meger. Deep Reinforcement Learning That Matters. AAAI, 2018.

[27] Snyder et al. Is Your Imitation Learning Policy Better than Mine? Policy Comparison with Near-Optimal Stopping. arXiv:2503.10966, 2025.

[28] Mnih et al. Human-level Control through Deep Reinforcement Learning. Nature, 2015.

[29] Black et al. (π<sub>0.5</sub>): a Vision-Language-Action Model with Open-World Generalization. arXiv:2504.16054, 2025.

[30] NVIDIA et al. GR00T N1: An Open Foundation Model for Generalist Humanoid Robots. arXiv:2503.14734, 2025.

[31] Zhao, Kumar, Levine, Finn. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. RSS, 2023 (arXiv:2304.13705).

[32] Shukor et al. SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics. arXiv:2506.01844, 2025.

[33] Brohan et al. RT-1: Robotics Transformer for Real-World Control at Scale. RSS, 2023 (arXiv:2212.06817).

[34] Brohan et al. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. CoRL, 2023 (arXiv:2307.15818).

[35] Open X-Embodiment Collaboration. Open X-Embodiment: Robotic Learning Datasets and RT-X Models. ICRA, 2024 (arXiv:2310.08864).

[36] Kim et al. OpenVLA: An Open-Source Vision-Language-Action Model. CoRL, 2024 (arXiv:2406.09246).

[37] Black et al. π<sub>0</sub>: A Vision-Language-Action Flow Model for General Robot Control. arXiv:2410.24164, 2024.

[38] Black et al. $\pi _ { 0 . 6 } \colon$ a VLA That Learns from Experience. arXiv:2511.14759, 2025.

[39] Fu et al. Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation. CoRL, 2024 (arXiv:2401.02117).

[40] Zawalski et al. Robotic Control via Embodied Chain-of-Thought Reasoning. CoRL, 2024 (arXiv:2407.08693).

## A Survey of Recent VLA Evaluation Practice

Table 5 surveys 13 recent real-robot VLA papers from 2023–2025; the LBM examination [24] is included below the rule as the single recent counter-example. Modal per-condition N is 10–20; none of the 13 standard-practice papers report confidence intervals or paired tests. LBM reports Bayesian posterior credible regions and paired Barnard’s exact / Welch’s t-tests with Bonferroni-corrected significance grouping at N=50 real / 200 simulation per condition.

Concurrent methodology critiques. Kress-Gazit et al. [23] explicitly argue that current realrobot evaluations are statistically underpowered. STEP [27] concurs: “20–30 real-world trials are insufficient for statistically significant conclusions.” These recommend; we ship a metric framework with reference implementation of those recommendations on a shared station.

| Paper | Per-condition N | Stats reported |
|---|---|---|
| RT-1 [33] | per-task N not standardized; ~3000 total | Point estimates only |
| RT-2 [34] | ~10–15 per task; ~6000 total | Point estimates only |
| RT-X / Open X-Embodiment [35] | 10–20 modal; up to 100/skill | Point estimates |
| OpenVLA [36] | ~10 real / 50 sim per task | No CIs |
| $\pi_0$ [37] | ~10 trials/task; partial credit | No CIs |
| $\pi_{0.5}$ [29] | tens per task, variable | No CIs |
| $\pi_{0.6}$ [38] | tens per task, variable | No CIs |
| GR00T N1 [30] | 5 objects × 3 trials = 15/task real | Point estimates |
| ACT / ALOHA [31] | ~25 trials/task | Point estimates |
| Mobile ALOHA [39] | 20/task (5 for “Cook Shrimp”) | Point estimates |
| DROID [11] | 10 rollouts per (task, method) | “Standard error” mentioned, no CIs |
| SmolVLA [32] | tens per real task | Point estimates |
| ECoT [40] | ~20/task (~300 total / policy) | Point estimates |
| LBM Examination [24] | 50 real / 200 sim per condition | Bayesian posteriors + paired Barnard / Welch with Bonferroni |

Table 5: Per-condition N and statistical reporting in recent real-robot VLA evaluation papers. “Percondition N ” is the per-condition sample size for the modal task – the count of trials per (model, task) cell. “Stats” summarizes confidence-interval and paired-test reporting in the original paper.

## B Run-Explorer Visualization

Every evaluated rollout is published in a run-explorer interface (Figure 4) that synchronizes the exterior and wrist video streams against the 3D end-effector trajectory and the per-channel telemetry: commanded action, gripper target, and measured gripper position. A reader auditing a specific time-to-success annotation against the raw video can replay it frame-accurately and inspect the joint state at any instant. The interface is built on Rerun [9] and runs post-hoc against the released artifacts; it is independent of the operator-side tooling used during rollout collection. We expose this not as part of the methodological contribution but as a transparency mechanism: every annotation in the released dataset is auditable against the raw rollout it was derived from.

## C Fine-Tuning Dataset Composition

Table 6 summarizes the shared fine-tuning corpus used across all four VLAs (§4.2): 449 demonstration episodes, ∼13 hours of robot operation, collected on the same Franka FR3 / Robotiq 2F-85 / dualcamera station as the evaluation rollouts. Episode counts are imbalanced across the four trained objects (wooden spoons are over-represented as the early development task); the full dataset is released alongside the benchmark.

| Object | Episodes | Duration (min) |
|---|---|---|
| Wooden spoons | 167 | ~340 |
| Towels | 112 | ~178 |
| Scissors | 83 | ~160 |
| Batteries | 87 | ~132 |
| Total | 449 | ~810 |

Table 6: Fine-tuning dataset (released alongside the benchmark, ∼13 hours of robot operation).

## D Finetuning Recipes

All four VLAs were finetuned using positronic [10] on the same ∼449-episode demonstration set (Appendix C). The OpenPI π and GR00T N1.6 recipes are the original implementations’ upstream defaults; ACT and SmolVLA use lerobot’s defaults with one deliberate deviation each, chosen to expand the model’s capacity beyond the upstream default rather than to equalize across models (a stronger visual backbone for ACT; a fully-trainable finetune for SmolVLA, detailed below).

![[99_Attachments/papers/images/phail/fb58af62eb736b3e81419f1758f97a70bf4262d2e8a52e6b00592d02e18729f2.jpg]]  
Figure 4: PhAIL platform during a rollout, visualized in the run-explorer interface (built on Rerun [9]): synchronized exterior and wrist video, 3D end-effector trajectory, and telemetry traces (commanded action, gripper target, measured gripper).

OpenPI $\pi _ { 0 . 5 } .$ 200,000 training steps. LoRA finetune on the PaliGemma 2B backbone and the Gemma-300M action expert (all non-LoRA parameters frozen); AdamW with warmup-cosine LR schedule, batch size 32. Proprioceptive state: 8-dim (ee\_pose as xyz + quaternion + gripper). Internal action representation: deltas on xyz + quaternion, absolute gripper.

NVIDIA GR00T N1.6. 150,000 training steps. AdamW with peak ${ \mathrm { L R ~ } } 1 { \times } 1 0 ^ { - 4 }$ , batch size 64; vision encoder and LLM frozen (only the multimodal projector and the diffusion action head trained). Proprioceptive state: 10-dim (ee\_pose as xyz + rot6d + gripper). Internal action representation: relative end-effector pose (xyz + rot6d), absolute gripper.

ACT (Action Chunking Transformer). lerobot 0.3.3 ACT defaults at 220,000 training steps, with one visual-backbone deviation: resnet50\_dinov3 (timm vit\_base\_patch16\_dinov3.lvd1689m, DINOv3-pretrained) in place of the upstream default of an ImageNet-pretrained ResNet-18. Internal action representation: absolute Cartesian ee\_pose + absolute gripper.

SmolVLA. lerobot[smolvla] 0.4.3 SmolVLA defaults at 200,000 training steps, with one deviation: a full finetune (no module frozen) instead of the upstream default of freezing the vision encoder and training the action expert only. Internal action representation: absolute Cartesian ee\_pose + absolute gripper.

Cross-cutting notes. OpenPI $\pi _ { 0 . 5 }$ and GR00T N1.6 internally learn relative/delta actions; ACT and SmolVLA learn absolute Cartesian targets directly. All four are fed an exterior + wrist camera pair; image resolution is 224×224 for OpenPI, GR00T, and ACT, and 512×512 for SmolVLA. Action chunk sizes: OpenPI 50, GR00T 16, ACT 100, SmolVLA 50.

## E Annotation Protocol

The framework requires per-episode event logs: place timestamps, intervention counts, and end-state item counts. The protocol is implementation, not contribution, and is expected to evolve.

Automated detector + classifier. A multistage release detector reads gripper telemetry (target\_grip edges gated by hold and plateau windows, plus accidental-drop detection on grip slumps from the held band into the fully-closed band) and emits per-candidate features (end-effector zone, hold duration, displacement, a running target-zone ledger); a classifier then assigns each candidate a verdict ∈ {success, failure, neutral, unknown}. Implementation, calibrated thresholds, and unit tests are released alongside the data.

Manual review. For every episode where the classifier’s success count disagrees with the operator’s logged eval.successful\_items, a human annotator reviews each candidate in a custom desktop UI and records per-candidate item counts and timestamps; these confirmed values ground the released annotations. Of the 995 raw episodes, the detector’s success count exactly matched the operatorlogged count on 573 (∼58%); the remaining 422 (∼42%) went through manual review by a single annotator.

Blinding. The operator was blinded during rollout collection – the scheduler randomly selected the active checkpoint and the operator did not know which model was running. The annotator was not blinded to model identity, because rollout videos expose policy behavior signatures (trajectory smoothness, grasp style). The two subsets are not interchangeable: the auto-validated cohort is the “clean” episodes (detector and operator agreed without intervention), while the manual cohort is the “messy” ones (partial successes, accidental drops, edge cases) – so a manual-vs-mixed comparison is a robustness check across episode difficulty, not an annotator-bias control.

Label-stream robustness check. As a robustness check on which subset of episodes the analysis weights, we re-ran the headline on the manually-reviewed cohort alone (N ≈ 420): the ranking is identical (OpenPI > GR00T > ACT > SmolVLA) and HRT levels shift by 2–5 pp without crossing pairwise CIs. The auto-validated additions therefore do not change conclusions; both label streams are released alongside the data.

Toward objective event recording. Subsequent PhAIL releases will replace manual review with task-specific hardware sensing – bin-weight sensors for pick-and-place, analogous instrumentation for insertion and small-part assembly – so that operation events are recorded objectively at collection time, with no annotator pass and therefore no annotator-bias channel.

## F Failure-Mode Decomposition

The CDF asymptote-below-1 (Figure 1a) aggregates three distinct mechanisms; the framework absorbs only the unrecoverable ones as T = ∞ ghost events (§3.1).

• Drops outside the workspace (per-operation ghost; the dominant mechanism): OpenPI 4.2%, GR00T 3.5%, ACT 5.7%, SmolVLA 4.9% of operations.

• Safety-stop terminations (per-episode ghost): OpenPI 4.5%, GR00T 2.9%, ACT 0%, SmolVLA 12.2% of episodes.

• Timeouts (operations not completing by τ<sub>episode</sub>; censored, not ghosts): the modal nonsuccess outcome for every model, 64%–89% of episodes.

Reporting these separately matters because the same CDF asymptote height can come from very different mixes – ACT’s drop-out rate is the highest among inference models while its safety-stop rate is zero; SmolVLA’s safety-stop rate is the highest at 12.2% while its drop-out rate is mid-pack. A single “hard-failure rate” summary would equate qualitatively different failure profiles.

## G Spatial Configuration Sensitivity

PhAIL’s protocol logs the spatial configuration (camera and tote placement) with every episode. Between rollouts we vary outbound tote placement (left/right) and external camera position (left/right), creating four spatial configurations. Table 7 reports completion rate by camera/tote configuration. “Same-side” means the external camera and the outbound tote are on the same side of the workspace; “opposite-side” means they are on opposite sides, in which case the inbound tote partially occludes the outbound tote from the camera’s perspective.

| Model | Same-side | Opposite-side | $\Delta$ |
|---|---|---|---|
| OpenPI | 51.1% | 45.0% | +6.1 pp |
| GR00T | 57.8% | 35.6% | +22.2 pp |
| ACT | 35.6% | 31.6% | +4.0 pp |
| SmolVLA | 12.1% | 9.5% | +2.6 pp |

Table 7: Completion rate by camera/tote configuration.

GR00T shows the largest sensitivity (22.2 pp drop), suggesting strong reliance on the external camera view; OpenPI is the most robust among the top models. An environmental change a human operator would not notice can move the measured ordering. PhAIL’s protocol logs the configuration with every episode so that this kind of confound is visible to the analyst rather than absorbed into noise. Per-model same-side / opposite-side episode counts are balanced (OpenPI 66/63, GR00T 69/59, ACT 77/74, SmolVLA 58/58 – within 8 pp of an even split for every model), so the configuration-side sensitivity does not contaminate the pairwise comparisons of §5.1 despite its absolute magnitude.

## H Power-Calculation Derivations

Wilson confidence interval on a single binary success rate. For an observed proportion $\hat { p }$ on N trials, the Wilson [6] score interval gives a CI of half-width approximately $z _ { \alpha / 2 } \sqrt { \hat { p } ( 1 - \hat { p } ) / N }$ for the underlying success probability. To obtain ±5 pp at 95% confidence on ${ \hat { p } } = 0 . 7 0 ,$ , the formula gives N ≈ 380 rollouts. At the field-modal $N \in \left\lceil 1 0 , 2 0 \right\rceil$ , the Wilson 95% CI on an observed 70% success rate is roughly [0.40, 0.89] at N=10 or [0.48, 0.86] at N=20 – intervals so wide that ranking claims at this depth are not statistically defensible.

Stratified McNemar test for paired binary outcomes. For two policies evaluated on the same N paired conditions within a stratum, let b and c be the discordant cell counts (one policy succeeds, the other fails). The McNemar [7] statistic is $( b - c ) ^ { 2 } / ( b + c ) , \chi _ { 1 } ^ { 2 }$ -distributed under $H _ { 0 }$ of equal success probabilities. Following Connor’s [8] sample-size derivation for the paired-sample design, to detect ${ \mathrm { ~ a ~ } } \Delta = 5$ pp paired difference at 80% power and $\alpha = 0 . 0 5$ , with discordance rate $p _ { d } \in [ 0 . 1 0 , 0 . 2 5 ]$ (capturing “how often the two policies disagree on a given paired condition”),

$$
N \approx \frac {\left(z _ {\alpha / 2} \sqrt {p _ {d}} + z _ {\beta} \sqrt {p _ {d} - \Delta^ {2}}\right) ^ {2}}{\Delta^ {2}}.
$$

At $p _ { d } = 0 . 1 0$ this gives $N \approx 6 0 0 ;$ at $p _ { d } = 0 . 2 5 , N$ ≈ 1500. The macro-KS significance test (§3.3) stratifies on (model, object) cells – a per-cell KS distance, then macro-averaged across the four cells. The apples-to-apples binary analog is therefore stratified McNemar, where the formula above gives the per-cell sample size: 600–1500 rollouts per (model, object) cell to detect a 5 pp within-cell paired difference at 80% power. The macro-KS Brownian-bridge model below predicts 25–45 rollouts per cell at the same power level – a ∼30× ratio at the per-cell unit both tests stratify on, equivalently 2400–6000 vs. 100–180 total paired rollouts per comparison.

Two-sample KS test on the CDF (per-object macro). We derive a theoretical power model that matches the empirical KS procedure of §5.2 in five steps.

Step 1 – identify the statistic. The empirical test computes a per-object KS distance $D _ { o } \ =$ sup<sub>t</sub> $| F _ { o } ^ { ( a ) } ( t ) - F _ { o } ^ { ( b ) } ( t ) |$ for each of the J=4 objects, macro-averages the results, $\begin{array} { r } { \bar { D } = J ^ { - 1 } \sum _ { o } D _ { o } , } \end{array}$ and calibrates significance via an episode-clustered pooled-resample bootstrap. The power model must therefore predict the distribution of ${ \bar { D } } ,$ not of a single KS on a pooled-across-objects CDF.

Step 2 – identify the effect size. Plugging the population (full-data) CDFs into Step 1 gives per-object $\Delta _ { o } = \operatorname* { s u p } _ { t } | F _ { o } ^ { ( a ) } - F _ { o } ^ { ( b ) } |$ and macro $\bar { \Delta } = J ^ { - 1 } \sum _ { o } \Delta _ { o }$ . On our close pairs $\bar { \Delta } \in [ 0 . 1 2 , 0 . 1 8 ]$ . This is $2 { \ - } 4 \times$ larger than sup $| \bar { F } ^ { ( a ) } - \bar { F } ^ { ( b ) } |$ on the macro-pooled CDF, because per-object discrepancies that live at different timepoints partially cancel under pooling – the test statistic of Step 1 keeps that signal.

Step 3 – identify the effective sample size. The bootstrap resamples at the episode level, but each episode contributes $m _ { o }$ ≈ 4.4 correlated placement times. Treating each episode as one observation under-credits the data; treating each placement as i.i.d. over-credits it. The standard design-effect correction gives an effective per-object operation count

$$
n _ {o} = \frac {N _ {\mathrm{cell}} m _ {o}}{D},
$$

where D is the cluster design effect. The raw-time intra-cluster correlation in our data is $\rho \in$ [0.66, 0.71], which would predict $D = 1 + ( m { - } 1 ) \rho \approx 3 . 0$ . But the KS functional depends only on the indicators $1 \{ T < t \}$ , whose intra-episode correlation is weaker than that of T itself; calibrating D against the six known empirical detection rates ({3 close pairs} $\cdot \times \{ N _ { \mathrm { c e l l } } \in \{ 2 5 , 3 0 \} \} )$ gives $D \approx 2 . 2 5$ . One free parameter, six calibration points.

Step 4 – model the per-object distribution. Asymptotically, the per-object KS statistic with effective sample size $n _ { o }$ per arm converges to a supremum of a Brownian bridge plus a deterministic drift,

$$
\sqrt {n _ {o} / 2}   D _ {o}   \Rightarrow   \sup _ {t} \big |   B _ {o} (t) + \sqrt {n _ {o} / 2}   (F _ {o} ^ {(a)} - F _ {o} ^ {(b)}) (t)   \big |,
$$

where $B _ { o }$ is a standard Brownian bridge on [0, 1] (a pinned Gaussian process with $B _ { o } ( 0 ) = B _ { o } ( 1 ) =$ 0 and marginal variance $t ( 1 - t ) )$ . Under $H _ { 0 }$ the drift vanishes and ${ \sqrt { n _ { o } / 2 } } D _ { o }$ converges to sup $| B _ { o } |$ whose distribution is the Kolmogorov distribution.

Step 5 – simulate, macro-average, and read off power. Given the per-object $( F _ { o } ^ { ( a ) } , F _ { o } ^ { ( b ) } )$ estimated from the full data (Step 2) and $n _ { o }$ from Step 3, we simulate per-object bridges, compute $D _ { o }$ under both $H _ { 1 }$ (drift-augmented) and $H _ { 0 }$ (drift-free), macro-average to D<sup>¯</sup> , and take

$$
\widehat {\operatorname{Power}} (N _ {\text { cell }}) = \operatorname * {P r} _ {H _ {1}} \bigl (\bar {D} > q _ {1 - \alpha} ^ {H _ {0}} \bigr).
$$

The $H _ { 0 }$ critical value $q _ { 1 - \alpha } ^ { H _ { 0 } }$ comes from the same simulation under drift-free bridges (the textbook Kolmogorov $c _ { \alpha } \approx 1 . 3 5 8$ is for a single sup, not a macro-mean of four; the simulated quantile is the right one for this statistic).

Result. The simulation matches the empirical detection-rate curves to within 3 pp across $N _ { \mathrm { c e l l } } \in [ 5 , 3 0 ]$ on all three close pairs, including the twelve points outside the six used to calibrate D. Sweeping $N _ { \mathrm { c e l l } }$ , the predicted $N _ { 0 . 8 }$ for the close pairs is 25 (GR00T vs. ACT), 30 (OpenPI vs. ACT), and 45 per cell (OpenPI vs. GR00T) – consistent with the empirical curves where they cross 0.8 (§5.2), and predicting that the currently-unresolved closest pair would clear 80% power with $a \sim 5 0 \%$ increase over the current N≈30 budget, not the order-of-magnitude jump that a naive unpaired sup-bound formula would imply.

This is a calibrated empirical model, not an independent theoretical bound: one design-effect parameter is tied to six observed detection rates and the remaining twelve points and the swept $N _ { 0 . \xi }$ are interpolations over the same empirical surface. It should be read as the budget the surface implies given the close-pair effect sizes we observe, not as a derivation from first principles.

Empirical detection-rate-vs-N curves. §5.2 translates these analytical numbers into empirical detection-rate-vs-N curves on our data via 300 outer subsampling trials, each running a 200-rep inner episode-clustered bootstrap. The full (N, metric, pair, detection rate) table for all four metrics (F (30s), F (60s), RMST, KS) and all six model pairs is released alongside the data.

## I Sup-Sign Intransitivity: KS Cannot Order Policies

![[99_Attachments/papers/images/phail/7f71a9bdfa8133da487bf5d9c28b69772558fe5c767d00b51ccb404b9d0f9fb3.jpg]]  
Figure 5: Three step-function CDFs $F _ { A } , F _ { B } , F _ { C }$ (each with a $T = \infty$ asymptote representing a hard-failure rate). Arrows mark each pairwise supremum location with the magnitude and the winner at the sup. The pairwise sup-signs cycle $A \succ B \succ C \succ A \colon$ KS-sign is not a valid ranker.

The KS statistic returns a magnitude and a sign at the supremum point. One might try to use that sign as a pairwise ranker: $A \succ B$ iff $F _ { A } ( t ^ { * } ) > F _ { B } ( t ^ { * } )$ at $t ^ { * } = \mathrm { a r g }$ max<sub>t</sub> $| F _ { A } ( t ) - F _ { B } ( t ) |$ |. Figure 5 shows three step-function CDFs whose pairwise sup-signs cycle: ${ \bar { A } } \succ B ( \operatorname { s u p } \operatorname { o n } t \in [ { \bar { 1 , 5 } } ) ) , { \bar { B } } \succ C$ (sup on $t \in [ 2 \bar { 0 } , 5 0 ) ) , C \succ A$ (sup on $t \geq 5 0 )$ . The intransitivity is structural – each pairwise sup lands in a different time region, and a different CDF is on top in each. Ordering therefore cannot be read off the KS sign, and the two-step pipeline of §3.3 (KS for distinguishability, scoring scalar with CI for direction) avoids cycles by construction.

## J Null Calibration of the Macro-Averaged KS Test

The macro-averaged KS statistic with episode-clustered pooled-resample bootstrap is non-standard, so empirical Type-I error matters: we verify that the test rejects at approximately the nominal rate α when the null actually holds. We construct null data under three setups and run the full test pipeline against it.

Setups. (i) Same-model split: for each policy model M with $N _ { M } ~ \ge ~ 3 0$ episodes, partition $M \mathbf { \bar { s } }$ episodes uniformly at random into two equal-sized pseudo-arms; both arms are drawn from the same distribution by construction. (ii) Human-reference split: same idea on the 396 teleop episodes. (iii) Within-stratum permutation: for two real policies A, B, pool their episodes per (object, tote\_placement) stratum and randomly re-assign the model label respecting block-wise counts; permutation enforces exchangeability under the conditional null. For each scenario we run 500 outer trials, each computing one bootstrap p-value with 500 inner resamples, and report the empirical $\operatorname* { P r } ( p < \alpha )$ for $\alpha \in \{ 0 . 0 1 , 0 . 0 5 , 0 . 1 0 \}$

## K Per-Cell RMST and Pairwise P-P Plots

This appendix supports two claims from the body text. First, the per-(model, object) RMST grid (Figure 6) substantiates §5.1’s 19% per-object HRT ceiling and surfaces the GR00T-vs-ACT object crossing referenced in §5.3. Second, the pairwise P-P plots without the human anchor (Figure 7) accompany §5.3’s discussion of how the human-anchored AUC saturates and what removing that anchor reveals about the top-3 pairs.

## L Distributional Shape and Scalar Trade-offs

The figures in this appendix complement the per-cell RMST grid in Appendix K with two derived views of the same per-(model, object) CDFs: (i) a Q-Q view that exposes where along the time axis the model lags the human reference, and (ii) a parametric trade-off view that shows two standard scalars (UPH and MTBF/A) pulling in opposite directions as the protocol’s $\tau _ { \mathrm { e p i s o d e } }$ varies.

| Scenario | mean p | Pr(p<0.01) | Pr(p<0.05) | Pr(p<0.10) |
|---|---|---|---|---|
| (i) Same-model split (each policy's episodes halved): |  |  |  |  |
| OpenPI | 0.441 | 0.016 ± 0.011 | 0.072 ± 0.023 | 0.138 ± 0.030 |
| GR00T | 0.455 | 0.012 ± 0.010 | 0.050 ± 0.019 | 0.094 ± 0.026 |
| ACT | 0.416 | 0.004 ± 0.006 | 0.042 ± 0.018 | 0.100 ± 0.026 |
| SmolVLA | 0.408 | 0.012 ± 0.010 | 0.070 ± 0.022 | 0.124 ± 0.029 |
| (ii) Human-reference split: |  |  |  |  |
| Teleop | 0.479 | 0.012 ± 0.010 | 0.050 ± 0.019 | 0.122 ± 0.029 |
| (iii) Label permutation within (object × tote_placement): |  |  |  |  |
| OpenPI ↔︎ GR00T | 0.428 | 0.020 ± 0.012 | 0.078 ± 0.024 | 0.144 ± 0.031 |
| GR00T ↔︎ SmolVLA | 0.438 | 0.016 ± 0.011 | 0.058 ± 0.020 | 0.124 ± 0.029 |
| Nominal | 0.500 | 0.010 | 0.050 | 0.100 |
| Mean across scenarios | 0.438 | 0.013 | 0.060 | 0.121 |

Table 8: Empirical Type-I error of the macro-averaged KS test under three null setups. Each row is 500 outer trials; intervals are ±1.96 SE. Mean p should be 0.500 under uniformly-distributed p-values; we observe 0.41–0.48, a mild upward bias ${ \mathrm { o f } } \leq 9 { \mathrm { p p } }$ . The empirical rejection rate at α=0.05 averages 0.060 across scenarios (max 0.078, min $0 . 0 4 2 ) , \leq 3$ pp above nominal – a small anti-conservatism consistent with the discreteness of the bootstrap p-value at $N _ { \mathrm { b o o t } } { = } 5 0 0$ and the modest clustering correction; importantly, no scenario rejects systematically beyond what the discreteness would predict. The test is therefore approximately correctly sized for the regime PhAIL operates in.

![[99_Attachments/papers/images/phail/d68993667ba1f6660cc12dedb840204f30b94ff916c38250268e460f15ffa14f.jpg]]  
Figure 6: Per-(model, object) RMST with 95% episode-clustered bootstrap CIs. Crossings exist (most clearly GR00T vs. ACT between Batteries and Scissors) but none clears Bonferroni at $\alpha = 0 . 0 5 / 2 4$ The visible patterns suggest the orderings vary by object; resolving them formally requires the rollout budget that Figure 3 quantifies.

Q-Q plots: slowdown is tail-heavy. Figure 8 plots, for each object, $T _ { \mathrm { H u m a n } } ( q )$ against $T _ { \mathrm { m o d e l } } ( q )$ at matched quantile q (i.e., the time by which a fraction q of operations are completed). The dashed diagonal $\dot { T } _ { \mathrm { H u m a n } } = \dot { T } _ { \mathrm { m o d e l } }$ marks “as fast as the human reference”; below-diagonal points are modelslower-than-human. A uniform slowdown would trace a straight line through the origin with constant slope; the empirical curves bend away from the diagonal as $q \to 1$ , indicating that policies fall behind disproportionately on the slow tail of operations rather than uniformly across the distribution. The open circle on each model curve marks the model’s last reachable quantile $q = 1 - p _ { \mathrm { f a i l } } \colon$ humans have effectively no hard-failure asymptote, so the human curve runs to $q \approx 1$ uninterrupted, while a model’s curve terminates wherever its hard-failure rate cuts the CDF off.

![[99_Attachments/papers/images/phail/e0aef2d24c6dc95d095eb427f5e84f31b093200a1ca71892b10dbc424dfcd04b.jpg]]  
Figure 7: Pairwise model-vs-model P-P plots, top-3 only (SmolVLA excluded as too easily separable to be informative), macro-averaged across the 4 trained objects. The teleop-anchored AUC of §5.3 saturates because the human reference is ${ \sim } 7 \times$ faster than any evaluated VLA – nearly all model events fall in the human’s tail, so the AUC integral is dominated by short-time behaviour. Removing the human anchor neutralizes that bias: every top-3 pair falls on or near the diagonal, with macro-AUCs all consistent with 0.5 (ACT-vs-OpenPI 0.51 [0.45, 0.56]; ACT-vs-GR00T 0.50 [0.45, 0.55]; OpenPI-vs-GR00T 0.50 [0.46, 0.54]).

![[99_Attachments/papers/images/phail/876a482755cb13fda3d67106dcf2119507fd79b0dc3a5a71c60e04fa56367b7e.jpg]]  
Figure 8: Per-object Q-Q plots, $T _ { \mathrm { H u m a n } } ( q )$ vs $T _ { \mathrm { m o d e l } } ( q )$ , all four VLAs on the four bin-to-bin objects. Dashed diagonal = as fast as the human reference; below-diagonal = model is slower. Open circle on each model curve marks $q = 1 - p _ { \mathrm { f a i l } } .$ the highest quantile the model reaches before its hard-failure asymptote. Curves bending below the diagonal as $q \to 1$ indicate tail-heavy slowdown rather than a uniform multiplicative gap.

UPH and MTBF/A trade off as $\tau _ { \mathrm { e p i s o d e } }$ varies. Figure 9 plots, for each object, every model’s trajectory in the (UPH, MTBF/A) plane as $\tau _ { \mathrm { e p i s o d e } }$ sweeps [30, 240] seconds. $\mathrm { U } \mathrm { \bar { P } H } \propto 1 / \mathrm { \bar { R } M S T } ( \tau _ { \mathrm { e p i s o d e } } )$ falls with $\tau _ { \mathrm { e p i s o d e } }$ because the integration cap charges every hard-failure ghost event the full $\tau _ { \mathrm { e p i s o d e } } ;$ $\mathrm { M T B F / A } = \mathrm { \bar { R M S T } } ( \tau _ { \mathrm { e p i s o d e } } ) / \left( 1 - F ( \tau _ { \mathrm { e p i s o d e } } ) \right)$ rises with $\tau _ { \mathrm { e p i s o d e } }$ because the same cap inflates the numerator faster than the (eventually-asymptotic) denominator. The two scalars therefore move in opposite directions, and the order they induce on policies depends on which $\tau _ { \mathrm { e p i s o d e } }$ a paper picked. This is concrete evidence for the “no single scalar suffices” claim of §3.2: any headline scalar that integrates against $\tau _ { \mathrm { e p i s o d e } }$ implicitly fixes a point on a trade-off curve, and a different but equally defensible $\tau _ { \mathrm { e p i s o d e } }$ relabels the leaderboard. Figure 10 collapses the four per-object panels into a single macro view by equal-weight averaging the per-object (UPH, MTBF/A) trajectories at each $\tau _ { \mathrm { e p i s o d e } } ;$ the trade-off survives macro-aggregation, so it is a property of the methodology, not of a particular object.

![[99_Attachments/papers/images/phail/aa25baf489138cef34dc0f5b5cfa4400964a03bb8f068481399ae2f681fc22c9.jpg]]  
Figure 9: UPH versus MTBF/A trajectories per object, parametric in $\tau _ { \mathrm { e p i s o d e } } \in [ 3 0 , 2 4 0 ]$ seconds. Each curve is one (model, object) cell traced as the episode horizon increases. Trajectories run up-and-left as $\tau _ { \mathrm { e p i s o d e } }$ rises (UPH falls, MTBF/A rises): the two scalars trade off, and the headline a benchmark publishes therefore depends on a protocol choice rather than only on policy quality.

parametric in $\tau _ { \mathrm { e p i s o d e } }$ ∈[30, 240] seconds  
UPH vs MTBF/A, macro-averaged across 4 objects  
![[99_Attachments/papers/images/phail/6e0c7457beca6ffcc3ce433d3903a192d429dee02c372d795b5f99d06b8d2a43.jpg]]  
Figure 10: Macro-averaged UPH versus MTBF/A trajectories: for each model and each $\tau _ { \mathrm { e p i s o d e } } ,$ the four per-object (UPH, MTBF/A) points from Figure 9 are averaged with equal weight across objects, then traced as $\tau _ { \mathrm { e p i s o d e } }$ sweeps [30, 240] seconds. The UPH-vs-MTBF/A trade-off persists after macro-aggregation: any choice of $\tau _ { \mathrm { e p i s o d e } }$ fixes one point on each model’s trade-off curve, and a different but equally defensible $\tau _ { \mathrm { e p i s o d e } }$ can change the headline ordering.