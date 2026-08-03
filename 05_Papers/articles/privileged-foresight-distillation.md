---
title: "Privileged Foresight Distillation Zero-Cost Future Correction for World Action Models 2604.25859"
---

# PRIVILEGED FORESIGHT DISTILLATION: ZERO-COST FUTURE CORRECTION FOR WORLD ACTION MODELS

# Pengcheng Fang

The University of Southampton

# Hongli Chen

The University of Queensland

# Xiaohao Cai

The University of Southampton

April 29, 2026

# ABSTRACT

World action models jointly predict future video and action during training, raising an open question about what role the future-prediction branch actually plays. A recent finding shows that this branch can be removed at inference with little to no loss on common manipulation benchmarks, suggesting that future information may act merely as a regularizer on the shared visual backbone. We propose instead that joint training induces an action-conditioned correction that privileged future observations impose on action denoising, and that current-only policies capture this correction only partially. Making the account precise, we formulate privileged foresight as a residual in the action-denoising direction — the difference between what a model predicts given the true future and what it predicts given only the current frame — and introduce Privileged Foresight Distillation (PFD), which transfers this residual from a training-time teacher into a small adapter on a current-only student. The teacher and student share the same backbone and differ only in the attention mask over video tokens; future video is never generated at inference. Controlled experiments verify that this gain reflects a genuine future-conditioned correction rather than a side effect of capacity or regularization. Empirically, PFD achieves consistent improvements on LIBERO and RoboTwin manipulation benchmarks while preserving the current-only inference interface at negligible added latency. This view reframes the role of future information in world action models: not as a target to predict, nor as a regularizer to absorb, but as a compressible correction to be distilled.

# 1 Introduction

Joint prediction of future video and action is a central design pattern in world action models, motivated by the intuition that visual foresight during training helps an agent choose better actions. A recent finding challenges this premise: a model trained jointly with video prediction can be deployed without test-time future generation while matching or exceeding the predictive variant Yuan et al. [2026]. The result has been read as evidence that test-time future imagination is unnecessary — but it leaves a deeper question unanswered. If the future branch is not used at inference, what role does future information play during training, and is any of its action-specific content lost when the branch is removed?

Two readings of this finding are possible. On a regularizer reading, future video shapes the shared visual backbone but contributes nothing action-specific; the current-only policy captures everything useful, and there is nothing to recover. On a privileged-foresight reading, future video induces a structured correction on the action-denoising direction itself — a correction that joint training transfers only partially to the current-only path. The two readings are observationally similar in the existing literature, yet they imply opposite methodological prescriptions: the first directs effort toward stronger visual backbones, the second toward better mechanisms for transferring the privileged signal. We find that the first reading is incomplete. Simply exposing the current-only policy to more training capacity — naïve finetuning of the same backbone layers — fails to improve performance (Section 4.3), so the gap between what joint training can teach and what the current-only policy learns is not a capacity gap. The interesting signal, if it exists, must lie in a direction that pure supervision on the action target does not reach.

We locate this signal by asking what privileged access to the future would change in the action-denoising process. During training, we instantiate the same backbone as two parallel paths, identical except for the attention mask over

video tokens: a current-only student that sees only the current frame (matching the standard joint-training setup), and a privileged teacher that attends to the full future video. The teacher’s action-velocity prediction minus the student’s defines a foresight residual — the component of the denoising direction that becomes predictable once future information is available. Privileged Foresight Distillation (PFD) trains a small adapter on the student path to predict this residual from current-only context. The residual target is detached before use, so the inherited joint-training objective is not pulled away from the action target by a moving teacher signal. At inference, the teacher is discarded and the adapter augments the student’s prediction at each denoising step; the current-only inference interface is preserved exactly, with the foresight-induced correction restored through a residual head whose added latency is negligible (Section 4).

We design controlled experiments to interpret PFD’s gain, isolating it from confounds of capacity, regularization, and fine-tuning-budget reallocation. None of these alternatives accounts for the observed effect, supporting a specific reading of the transferred signal: privileged foresight is a future-conditioned correction that is not recovered by matched direct fine-tuning under the same budget, and a small adapter is sufficient to absorb it.

Contributions. We make the following contributions.

• A new perspective on future information. We propose that future information in world action models is best understood as an action-conditioned correction residual — a direction not recovered by matched direct fine-tuning under the same budget.   
• Privileged Foresight Distillation (PFD). We introduce a training-only teacher–student construction that makes this view operational: the teacher accesses real future during training, a small adapter distills the teacher-minus-student residual, and the adapter preserves the current-only inference interface with no future generation at test time.   
• Controlled evidence for the transferred signal. We design experiments that isolate PFD’s gain from confounds of capacity, auxiliary regularization, and budget reallocation between backbone fine-tuning and adapter capacity, supporting the reading of the foresight residual as a future-conditioned correction.   
• Empirical results. PFD achieves consistent improvements over the Fast-WAM backbone on LIBERO and RoboTwin, matching or exceeding methods that rely on embodied pretraining, with negligible inference overhead.

# 2 Related Work

World action models and future video. Recent robot policies combine video backbones with action heads, either by jointly predicting future frames and actions Wu et al. [2024], Cheang et al. [2024], Hu et al. [2025] or by conditioning actions on externally generated future videos Du et al. [2023], Black et al. [2024b]. In both settings, future materialization—as pixels or latent rollouts—is required at inference and often dominates computation. Fast current-only policies remove this test-time future generation with a single forward pass Yuan et al. [2026]. We ask whether action-relevant future information can still benefit such current-only policies, and in what form.

Uses of future information. Prior work mainly uses future information in two ways. Future-as-prediction explicitly generates future frames for action conditioning Du et al. [2023], Black et al. [2024b], while future-as-representation learns latent imagination rollouts for planning or representation learning Hafner et al. [2023], Schrittwieser et al. [2020], Hansen et al. [2024]. Both require future content to exist at test time in some form. In contrast, PFD uses future-as-correction: future video is available only during training, where it reveals what a current-only policy misses, and is distilled into a residual correction that is not reconstructed at inference.

Privileged information and adapter heads. PFD builds on asymmetric teacher–student learning with privileged information Vapnik and Vashist [2009], Chen et al. [2019], commonly used to transfer supervision from more informed teachers to constrained students. Here, teacher and student share the same backbone parameters and differ only in their attention mask over video tokens, removing architectural confounds. Moreover, PFD defines the adapter target as the teacher–student residual rather than replacing the student with full teacher imitation; a weak teacher-consistency term is used only to stabilize the corrected output, isolating the component attributable to future access. This residual is carried by a small action-stream adapter; unlike generic parameter-efficient adapters Hu et al. [2022], it is explicitly sized and trained to encode the foresight residual.

Top:Attention Mask Comparison (Why Teacher is Privileged)   
Student Mask (Fast-WAM,also used at inference)

Privileged Teacher Mask (Training Only)

(visible)

Right: Inference (Current frame only)

(no futureaccess)

SharedMoTBackbone

(video+actionexperts)

+studentmask

Teacher path

(training only)

Student path

&inference)

Teacher path

Adapterg

(ours; used in training

&inference)

Shared MoT Backbone

(same backbone weights)

Stopgrad

（detached from

gradient)

Figure 1: Privileged Foresight Distillation (PFD). Top: Student and privileged teacher paths differ only in their attention mask: the student action tokens attend to the current-frame video tokens and action tokens, matching the Fast-WAM current-only inference interface, whereas the teacher action tokens attend to all video tokens, including real future frames available only during training. Left: During training, the same MoT backbone is evaluated under both masks, yielding a live student prediction $v _{\mathrm{ b a s e}}$ and a stop-gradient privileged prediction $v _{\mathrm{ t e a c h e r}}$ . The detached residual target $r = \mathrm{ s g} ( v _{\mathrm{ t e a c h e r}} - v _{\mathrm{ b a s e}} )$ captures the action-denoising correction induced by future access. A small adapter $g _{\phi}$ takes the live $v _{\mathrm{ b a s e}}$ and predicts $\hat{\delta}$ to fit this residual, producing $v _{\mathrm{ f i n a l}} = v _{\mathrm{ b a s e}} + \hat{\delta}$ . Right: At inference, the teacher path and future video tokens are discarded. The model runs only the student mask and applies the adapter correction, preserving the current-only Fast-WAM interface with no test-time future generation and negligible adapter-only compute cost.

Discarded at inference

(not used)

# 3 Method

Privileged Foresight Distillation (PFD) is a training-time mechanism that operationalizes the future-as-correction view of $\ S 1$ : a privileged path with future access produces an action-side correction signal, and a small adapter on the current-only path absorbs it. Inference uses the current-only path and the adapter; the privileged path is not instantiated.

# 3.1 Preliminaries

Let $X = ( X _{1} , \ldots , X _{T} )$ denote a sequence of $T$ video frames with $X _{1}$ the current frame, and let $A$ denote the corresponding action chunk. Following Yuan et al. [2026], we adopt a Mixture-of-Transformers backbone with parameters $\theta$ , comprising a video expert and an action expert, with cross-stream information exchange controlled by a joint attention mask.

Both streams are trained with flow matching. We sample timesteps $\tau _{v} , \tau _{a} \in [0, 1]$ independently and draw independent Gaussian noise $\varepsilon _{v} , \varepsilon _{a}$ , yielding the corrupted inputs

$$
X _{\tau_{v}} = \left(1 - \tau_{v}\right) \varepsilon_{v} + \tau_{v} X, \quad A _{\tau_{a}} = \left(1 - \tau_{a}\right) \varepsilon_{a} + \tau_{a} A, \tag{1}
$$

with action-velocity target $v _{\mathrm { t a r g e t} } = A - \varepsilon _{a}$ . We write $u _{\mathrm { v i d e o} }$ for the video-velocity output and $u _{\mathrm { t a r g e t} } = X - \varepsilon _{v}$ for its target. We write

$$
v _{\mathrm{a c t}} \left(X _{\tau_{v}}, A _{\tau_{a}}, \tau_{v}, \tau_{a}; M\right)
$$

for the action-velocity output produced by the backbone when the joint self-attention is restricted by mask $M$ . The current-only forward used at inference adopts the student mask $M _{\mathrm { S} }$ , under which each action-token query attends to the current-frame video tokens $X _{1}$ and to the other action tokens:

$$
v _{\text{base}} = v _{\text{act}} \left(X _{\tau_{v}}, A _{\tau_{a}}, \tau_{v}, \tau_{a}; M _{\mathrm{S}}\right). \tag{2}
$$

Throughout the displayed equations we omit first-frame observation conditioning and the per-timestep scheduler weighting on the velocity outputs for clarity; both follow Yuan et al. [2026] and are applied identically to the student and teacher forwards introduced below.

# 3.2 A privileged forward via attention masking

PFD adds a second action forward, identical to (2) in every respect except for the attention mask:

$$
v _{\text{teacher}} = \operatorname{sg} \left[ v _{\text{act}} \left(X _{\tau_{v}}, A _{\tau_{a}}, \tau_{v}, \tau_{a}; M _{\mathrm{T}}\right) \right]. \tag{3}
$$

The teacher mask $M _{\mathrm { T} }$ allows each action-token query to attend to the full set of video tokens $X _{1} , \ldots , X _{T}$ , including future frames; $\operatorname{sg} ( \cdot )$ denotes the stop-gradient operator. The teacher and student forwards share the same parameters $\theta$ at every step — there is no exponential moving average, no frozen copy, and no distinct teacher network — and they consume the same noisy inputs $( X _{\tau _ { v} } , A _{\tau _ { a} } )$ generated from a single noise sample $\left( \varepsilon _{v} , \varepsilon _{a} \right)$ . The two forwards differ only in the attention mask over video tokens, which isolates the effect of future access: capacity, parameterization, optimizer state, and noise realization are held identical, so any difference between $v _{\mathrm { t e a c h e r} }$ and $v _{\mathrm { b a s e} }$ is attributable to the enlargement of the action queries’ attention support. The stop-gradient on (3) further removes the teacher from the optimization graph, so it contributes no parameter update of its own and serves only as a target source for the residual we now define. Because the two forwards share $\theta$ , the residual $v _{\mathrm { t e a c h e r} } - v _{\mathrm { b a s e} }$ is a model-dependent foresight-induced correction at the current parameter state and evolves during training.

# 3.3 The foresight residual and the residual adapter

Rather than have the student imitate $v _{\mathrm { t e a c h e r} }$ in full, PFD distills only the component that future access changes. We define the foresight residual as

$$
r := \operatorname{sg} \left(v _{\text{teacher}} - v _{\text{base}}\right); \tag{4}
$$

since $v _{\mathrm { t e a c h e r} }$ is already detached, this is equivalent to $r = v _{\mathrm { t e a c h e r} } - \mathrm { s g } ( v _{\mathrm { b a s e} } )$ . Targeting $r$ rather than $v _{\mathrm { t e a c h e r} }$ confines supervision to the component that future access changes at the current $\theta$ ; whenever the two masks induce identical predictions, the target is zero and no teacher signal enters the loss.

The residual is absorbed by a small residual adapter $g _{\varphi}$ placed at the output of the action expert and applied token-wise:

$$
\hat{\delta} = g _{\varphi} \left(v _{\text{base}}, \tau_{a}\right), \quad v _{\text{final}} = v _{\text{base}} + \hat{\delta}. \tag{5}
$$

First, the adapter consumes $v _{\mathrm { b a s e} }$ rather than $\operatorname{sg} ( v _{\mathrm { b a s e} } )$ ; only the residual target $r$ in (4) is detached. As we discuss in $\ S 3 . 4$ , this asymmetry is what allows residual supervision to influence the backbone subset $\theta ^{\prime}$ at all under partial fine-tuning, rather than reducing to a pure adapter-fitting problem on $\varphi$ . Second, the adapter’s output projection is zero-initialized, so $\hat{\delta} \equiv 0$ at the start of training and $v _{\mathrm { f i n a l} } = v _{\mathrm { b a s e} }$ identically; the corrected forward equals the standard Fast-WAM student forward at initialization, and any departure from it accumulates only as training drives $g _{\varphi}$ to fit $r$ .

# 3.4 Training objective and gradient routing

Let $\theta ^{\prime} \subseteq \theta$ denote the subset of backbone parameters that are permitted to update; the adapter parameters $\varphi$ always update. PFD trains $( \theta ^{\prime} , \varphi )$ against the inherited video flow-matching loss together with three action-side losses:

$$
\mathcal{L} _{\text{video}} = w _{v} \left(\tau_{v}\right) \left\| u _{\text{video}} - u _{\text{target}} \right\| ^{2}, \tag{6}
$$

$$
\mathcal{L} _{\mathrm{g t}} = w _{a} \left(\tau_{a}\right) \left\| v _{\text{final}} - v _{\text{target}} \right\| ^{2}, \tag{7}
$$

$$
\mathcal{L} _{\text{res}} = \left\| \hat{\delta} - r \right\| ^{2}, \tag{8}
$$

$$
\mathcal{L} _{\text{teacher}} = \left\| v _{\text{final}} - v _{\text{teacher}} \right\| ^{2}, \tag{9}
$$

where $w _{v} ( \cdot )$ and $w _{a} ( \cdot )$ are the per-timestep weighting schedules of Yuan et al. [2026]. The full PFD objective is

$$
\mathcal{L} = \lambda_{\text{video}} \mathcal{L} _{\text{video}} + \lambda_{\mathrm{g t}} \mathcal{L} _{\mathrm{g t}} + \lambda_{\text{res}} \mathcal{L} _{\text{res}} + \lambda_{\text{teacher}} \mathcal{L} _{\text{teacher}}, \tag{10}
$$

with non-negative scalar coefficients; the values used in all experiments are reported in $\ S 4 . 1$ .

Gradient routing. The teacher forward is fully stop-gradiented at (3) and contributes no update to $\theta$ . The residual target $r$ in (4) is also detached, which prevents ${ \mathcal{L} } _{\mathrm { r e s} }$ from being trivially reduced by moving its target instead of fitting it. However, because the adapter input in (5) is the live $v _{\mathrm { b a s e} }$ rather than $\mathrm { s g } ( v _{\mathrm { b a s e} } )$ , $\mathcal{L} _{\mathrm { r e s} }$ is not confined to updating $\varphi$ : under partial fine-tuning, gradient also flows from ${ \mathcal{L} } _{\mathrm { r e s} }$ through the dependence of $\hat{\delta}$ on $v _{\mathrm { b a s e} }$ and into $\theta ^{\prime}$ . Residual supervision therefore reshapes both the correction head and the backbone’s emitted current-only velocity, with the detached target ensuring that the reshaping pulls $v _{\mathrm { b a s e} }$ toward the privileged prediction rather than away from it.

$\mathcal{L} _{\mathrm { r e s} }$ versus $\mathcal{L} _{\mathrm { t e a c h e r} }$ . The two teacher-derived losses coincide in forward value but differ in gradient path. Substituting $v _{\mathrm { f i n a l} } = v _{\mathrm { b a s e} } + \hat{\delta}$ into (9) gives $\lVert \hat{\boldsymbol { \delta} } - ( \boldsymbol { v } _{\mathrm { t e a c h e r} } - \boldsymbol { v } _{\mathrm { b a s e} } ) \rVert ^{2}$ , which equals $\mathcal{L} _{\mathrm { r e s} }$ as a number. They diverge once gradients are computed: $\mathcal{L} _{\mathrm { r e s} }$ uses a fully detached residual target and routes gradient primarily through $g _{\varphi}$ , with a secondary path into $\theta ^{\prime}$ via the adapter’s dependence on $v _{\mathrm { b a s e} }$ ; $\mathcal{L} _{\mathrm { t e a c h e r} }$ keeps the live $v _{\mathrm { b a s e} }$ inside $v _{\mathrm { f i n a l} }$ on the prediction side and detaches only $v _{\mathrm { t e a c h e r} }$ , so its gradient pulls the current-only velocity itself toward the privileged prediction rather than routing through $g _{\varphi}$ . PFD retains both terms: ${ \mathcal{L} } _{\mathrm { r e s} }$ supervises the adapter through a detached target, while $\mathcal{L} _{\mathrm { t e a c h e r} }$ pulls $v _{\mathrm { b a s e} }$ toward $v _{\mathrm { t e a c h e r} }$ through the live prediction path.

PFD admits two regimes via the choice of $\theta ^{\prime}$ : adapter-only ( $\mathbf{\boldsymbol { \theta} } ^{\prime} = \boldsymbol { \mathcal{D} }$ , the backbone is frozen) and partial fine-tuning ( $\theta ^{\prime}$ unfreezes the last $K _{a}$ blocks of the action expert and the last $K _{v}$ blocks of the video expert); specific values and the default configuration are reported in $\ S 4 . 1$ .

# 3.5 Inference

At inference, PFD preserves the current-only denoising interface of Fast-WAM. At each flow-matching denoising step, the model computes the student velocity $v _{\mathrm { b a s e} }$ from (2) under the student mask $M _{\mathrm { S} }$ , applies the residual adapter, and uses

$$
v _{\text{final}} = v _{\text{base}} + g _{\varphi} \left(v _{\text{base}}, \tau_{a}\right)
$$

for the sampling update on $A _{\tau _ { a} }$ . The teacher mask $M _{\mathrm { T} }$ is never instantiated at inference, and the future video frames $X _{2} , \ldots , X _{T}$ are neither generated nor consumed. The only added cost relative to Fast-WAM is one forward pass through $g _{\varphi}$ per denoising step.

# 4 Experiments

# 4.1 Experimental setup

Benchmarks. We evaluate on LIBERO Liu et al. [2023] and RoboTwin 2.0 Chen et al. [2025], following Fast-WAM Yuan et al. [2026]. LIBERO contains four suites (Spatial, Object, Goal, Long); for each, we train one model on 500 demonstrations over 10 tasks and report success rate over 500 trials. RoboTwin 2.0 is a bimanual dual-arm benchmark; we use its multi-task setup with 2,500 clean-scene and 25,000 randomized-scene demonstrations across more than 50 tasks, reporting success over 100 trials per task in each condition.

Baselines. Our primary baseline is Fast-WAM in two forms: “Fast-WAM (released)” directly transcribes the numbers from Yuan et al. [2026], while “Fast-WAM (reproduced)” is re-trained with the released configuration, codebase, and schedule used by our PFD runs, and serves as the reference for reported gains. The reproduced numbers are slightly lower than the original report but follow consistent suite-level trends under a unified evaluation pipeline. For broader context, we also include published numbers for OpenVLA Kim et al. [2024], $\pi _{0}$ Black et al. [2024a], $\pi _{0 . 5}$ Physical Intelligence et al. [2025], Motus Bi et al. [2025], and LingBot-VA Li et al. [2026], taken verbatim from Yuan et al. [2026]. These five context baselines use embodied pretraining (“Emb. PT.”), whereas Fast-WAM and PFD use the Wan2.2-5B backbone without embodied pretraining.

Training. We train for 30 epochs on LIBERO and 15 on RoboTwin using 8 H100 GPUs, matching Fast-WAM’s batch size, schedule, and optimizer family. We use AdamW with cosine decay, weight decay 0.01, gradient clipping 1.0, and benchmark-specific learning rates following Fast-WAM defaults: $6 \times 1 0 ^{- 5}$ for LIBERO and $1 \times 1 0 ^{- 4}$ for RoboTwin. PFD adds only the privileged forward of $\ S 3 . 2$ , which shares backbone parameters and introduces one additional attention pass per step.

Inference. Following Fast-WAM, we use 10 flow-matching denoising steps with classifier-free guidance scale 1.0. At each step, PFD runs one student forward under $M _{\mathrm { S} }$ and applies the residual adapter, $v _{\mathrm { f i n a l} } = v _{\mathrm { b a s e} } + g _{\varphi} ( v _{\mathrm { b a s e} } , \tau _{a} )$ , as in $\ S 3 . 5$ . The teacher mask $M _{\mathrm { T} }$ is never instantiated at inference, and no future video frames are generated or consumed. End-to-end latency is reported in $\ S 4 . 4$ .

Implementation. All main results use the partial fine-tuning regime of $\ S 3 . 4$ , with trainable parameters $\theta ^{\prime} \cup \varphi$ . Here, $\theta ^{\prime}$ contains the last $K _{a}$ action-expert blocks and last $K _{v}$ video-expert blocks, each expert having 30 blocks, and $\varphi$ denotes

Table 1: LIBERO success rate $( \% )$ over 500 trials per suite. “Emb. PT.” indicates embodied pretraining; “(reproduced)” is re-trained under our codebase. Bold marks the rows and per-suite numbers where PFD (partial fine-tune) exceeds the reproduced Fast-WAM.   

<table><tr><td>Method</td><td>Emb. PT.</td><td>Spatial</td><td>Object</td><td>Goal</td><td>Long</td><td>Average</td></tr><tr><td>OpenVLA Kim et al. [2024]</td><td>✓</td><td>84.7</td><td>88.4</td><td>79.2</td><td>53.7</td><td>76.5</td></tr><tr><td>π0 Black et al. [2024a]</td><td>✓</td><td>96.8</td><td>98.8</td><td>95.8</td><td>85.2</td><td>94.1</td></tr><tr><td>π0.5 Physical Intelligence et al. [2025]</td><td>✓</td><td>98.8</td><td>98.2</td><td>98.0</td><td>92.4</td><td>96.9</td></tr><tr><td>Motus Bi et al. [2025]</td><td>✓</td><td>96.8</td><td>99.8</td><td>96.6</td><td>97.6</td><td>97.7</td></tr><tr><td>LingBot-VA Li et al. [2026]</td><td>✓</td><td>98.5</td><td>99.6</td><td>97.2</td><td>98.5</td><td>98.5</td></tr><tr><td>Fast-WAM (released) Yuan et al. [2026]</td><td>-</td><td>98.2</td><td>100.0</td><td>97.0</td><td>95.2</td><td>97.60</td></tr><tr><td>Fast-WAM (reproduced)</td><td>-</td><td>97.0</td><td>99.4</td><td>96.6</td><td>94.8</td><td>96.95</td></tr><tr><td>PFD (partial fine-tune, ours)</td><td>-</td><td>98.6</td><td>99.2</td><td>99.2</td><td>95.4</td><td>98.10</td></tr><tr><td>PFD (adapter-only, θ&#x27; = ∅)</td><td>-</td><td>97.2</td><td>98.8</td><td>96.6</td><td>93.8</td><td>96.60</td></tr></table>

Table 2: RoboTwin 2.0 success rate $( \% )$ over 100 trials per task. “Emb. PT.” indicates embodied pretraining; “from Wan2.2” is re-trained on our backbone without embodied pretraining.   

<table><tr><td>Method</td><td>Emb. PT.</td><td>Clean</td><td>Randomized</td><td>Average</td></tr><tr><td>π0Black et al. [2024a]</td><td>✓</td><td>65.92</td><td>58.40</td><td>62.2</td></tr><tr><td>π0.5Physical Intelligence et al. [2025]</td><td>✓</td><td>82.74</td><td>76.76</td><td>79.8</td></tr><tr><td>Motus Bi et al. [2025]</td><td>✓</td><td>88.66</td><td>87.02</td><td>87.8</td></tr><tr><td>Motus from Wan2.2</td><td>-</td><td>77.56</td><td>77.00</td><td>77.3</td></tr><tr><td>LingBot-VA Li et al. [2026]</td><td>✓</td><td>92.90</td><td>91.50</td><td>92.2</td></tr><tr><td>LingBot-VA from Wan2.2</td><td>-</td><td>80.60</td><td>-</td><td>80.6</td></tr><tr><td>Fast-WAM Yuan et al. [2026]</td><td>-</td><td>91.88</td><td>91.78</td><td>91.8</td></tr><tr><td>PFD (partial fine-tune, ours)</td><td>-</td><td>93.11</td><td>92.69</td><td>92.9</td></tr></table>

the adapter. We set $( K _{a} , K _{v} ) = ( 1 2 , 1 2 )$ for both benchmarks, unfreezing about $4 0 \%$ of blocks per expert. The adapter $g _{\varphi}$ is a three-layer SiLU MLP of width 512; it takes a linear projection of the live base-action velocity $v _{\mathrm { b a s e} }$ from (2) and a sinusoidal embedding of $\tau _{a}$ broadcast over tokens, with zero-initialized output projection. Loss weights are fixed for all PFD runs: $\lambda _{\mathrm { v i d e o} } = \lambda _{\mathrm { g t} } = 1 . 0$ , $\lambda _{\mathrm { r e s} } = 0 . 5$ , and $\lambda _{\mathrm { t e a c h e r} } = 0 . 1$ .

# 4.2 Main results

LIBERO. Table 1 reports per-suite success rates. PFD raises the LIBERO average from 96.95 for the reproduced Fast-WAM to 98.10, a gain of $+ 1 . 1 5$ on the four-suite mean. The per-suite breakdown is $+ 1 . 6$ on Spatial, $- 0 . 2$ on Object, $+ 2 . 6$ on Goal, and $+ 0 . 6$ on Long. PFD improves on three of the four suites; on Object, where both methods exceed $9 9 \%$ , the difference of 0.2 points is at the binomial standard-error scale of 500-trial evaluation. The gains are most pronounced on Goal, while Long also improves over the reproduced Fast-WAM baseline. Comparing against methods that use embodied pretraining, PFD surpasses Motus (97.7), $\pi _{0 . 5}$ (96.9), and $\pi _{0}$ (94.1), and trails LingBot-VA (98.5) by 0.40 — without invoking a separate embodied pretraining stage. Adapter-only PFD $\theta ^{\prime} = \varnothing ,$ ) reaches 96.60, competitive on Spatial, Object, and Goal but below the Fast-WAM baseline on Long; we therefore adopt partial fine-tuning as the default configuration and revisit the adapter-only regime as an ablation in $\ S 4 . 3$ .

RoboTwin 2.0. Table 2 reports clean-scene, randomized-scene, and average success rates. PFD reaches 93.11/92.69 on clean and randomized respectively, with an average of 92.9, improving over the Fast-WAM row by $+ 1 . 2 3$ on clean, $+ 0 . 9 1$ on randomized, and $+ 1 . 1 0$ on the average. PFD’s 92.9 also exceeds the strongest embodied-pretrain baseline (LingBot-VA at 92.2) by 0.7 despite using no embodied pretraining, and is the highest among all Wan2.2-based entries.

# 4.3 Isolating the foresight signal

The aggregate gain reported in $\ S 4 . 2$ is consistent with the privileged-foresight account but does not by itself rule out simpler explanations: extra trainable capacity in $\theta ^{\prime}$ , generic regularization from a second teacher forward, or a different allocation of the fine-tuning budget between backbone depth and adapter capacity. We design three controlled probes that share PFD’s training budget but each break exactly one ingredient of the foresight transfer, and verify whether breaking that ingredient erases the gain. We run probes on LIBERO; the four-suite split exposes capacity and

Table 3: LIBERO epistemic probes (success rate $\%$ ). The first three probes break, in turn, capacity, temporal correspondence, and the allocation of the fine-tuning budget between backbone depth and adapter width. The last two rows are supplementary ablations on the adapter regime and on fine-tune depth.   

<table><tr><td>Configuration</td><td>Spatial</td><td>Object</td><td>Goal</td><td>Long</td><td>Average</td></tr><tr><td>Fast-WAM (reproduced)</td><td>97.0</td><td>99.4</td><td>96.6</td><td>94.8</td><td>96.95</td></tr><tr><td>Pure finetune (θ&#x27;, no teacher)</td><td>96.4</td><td>99.2</td><td>96.4</td><td>94.8</td><td>96.70</td></tr><tr><td>Shuffled-future PFD</td><td>96.1</td><td>99.2</td><td>96.2</td><td>95.0</td><td>96.62</td></tr><tr><td>PFD, width 1024 at (Ka, Kv) = (12, 6)</td><td>97.9</td><td>99.8</td><td>97.2</td><td>94.5</td><td>97.36</td></tr><tr><td>PFD (default) (Ka, Kv) = (12, 12), W = 512</td><td>98.6</td><td>99.2</td><td>99.2</td><td>95.4</td><td>98.10</td></tr><tr><td>adapter-only (θ&#x27; = ∅)</td><td>97.2</td><td>98.8</td><td>96.6</td><td>93.8</td><td>96.60</td></tr><tr><td>fine-tune depth (Ka, Kv) = (6, 6)</td><td>97.9</td><td>99.7</td><td>97.3</td><td>94.7</td><td>97.40</td></tr></table>

correspondence dimensions independently of RoboTwin’s bimanual coordination, which we treat as an end-to-end test in $\ S 4 . 2$ . Numerical results are collected in Table 3 and visualized in Figure 2.

Matched-capacity control. The first probe, pure finetune, unfreezes the same backbone subset $\theta ^{\prime} = ( K _{a} , K _{v} ) =$ (12, 12) and trains against the action ground truth alone, with no teacher forward and no adapter. If the PFD gain were attributable to the additional trainable capacity that $\theta ^{\prime}$ exposes, this control would match or exceed PFD. It does not: pure finetune scores $9 6 . 4 / 9 9 . 2 / 9 6 . 4 / 9 4 . 8$ for an average of 96.70, which is $- 0 . 2 5$ below the reproduced Fast-WAM and $- 1 . 4 0$ below PFD. Unfreezing the same subset of layers under direct action supervision slightly hurts the current-only policy at this training budget. The signal that PFD transfers is therefore not accessible to direct supervision on the action target, even when the layers permitted to update are identical.

Shuffled-future control. The second probe, shuffled-future PFD, replaces the teacher’s future frames $X _{2} , \ldots , X _{T}$ at every training step with frames drawn from an unrelated trajectory in the same batch. The teacher mask $M _{\mathrm { T} }$ , the adapter, the loss weights, and the schedule are otherwise identical to the default PFD run. If the gain reflected auxiliary-loss regularization or the mere presence of a second supervisory target, destroying the temporal correspondence between $X _{1}$ and $X _{2 : T}$ should leave it largely intact, since the input statistics and loss magnitudes are preserved. Instead, shuffledfuture PFD scores $9 6 . 1 / 9 9 . { \overset { \cdot } { 2 } } / { \overset { \cdot } { 9 } } 6 . 2 / 9 5 . 0$ for an average of 96.62, which is $- 0 . 3 3$ below the reproduced Fast-WAM and $- 1 . 4 8$ below PFD. The transferred signal therefore depends on genuine current-to-future correspondence, not on incidental properties of the teacher forward.

Depth–width trade-off probe. The third probe asks whether reducing video-side fine-tuning depth while increasing residual-head width can substitute for the default full-depth PFD configuration. We double the adapter hidden width from 512 to 1024 and, to test a practical depth–width trade-off, halve the video-expert fine-tune depth from $K _{v} = 1 2$ to $K _{v} = 6$ (the action expert is held at $K _{a} = 1 2$ ). This redirects the freed compute from updating the deeper video stack into a wider correction head. The resulting configuration scores $9 7 . 9 / 9 9 . 8 / 9 7 . 2 / 9 4 . 5$ for an average of 97.36, which is $- 0 . 7 4$ below the default PFD at width 512. Redirecting fine-tuning budget from the video expert to a wider adapter therefore fails to recover the gain. We cannot rule out a clean adapter-width effect at fixed $( \bar{K _{a} } , K _{v} ) = ( 1 2 , 1 2 )$ and leave that question to future work.

Reading the probes together. Relative to the default PFD average of 98.10, the three probes land at deltas of −1.40 (matched-capacity), $- 1 . 4 8$ (shuffled-future), and $- 0 . 7 4$ (budget-reallocation). Two readings split cleanly. Ruled out: extra trainable capacity and auxiliary-loss regularization each erase the PFD gain when isolated, with the matchedcapacity row falling below the frozen baseline and the shuffled-future row matching it. Argued against, not ruled out: budget-reallocation closes only part of the gap, and the supplementary $K = 6$ row reported below scores similarly at 97.40 without any adapter widening, corroborating the reading that the residual gap from 97.40 to 98.10 tracks fine-tune depth on the video expert rather than adapter width. None of the three confounds reproduces the privileged-foresight residual $r$ in (4): $r$ is by construction the component of the action-velocity field that becomes available when the attention mask exposes future frames at the same parameters, and the alternatives examined here change capacity, target, or budget allocation while leaving that mask alone.

Fine-tune depth (supplementary). As a supplementary check, we ablate the depth of the trainable backbone subset by halving $K = K _{a} = K _{v}$ from 12 to 6 at the default adapter width of 512. This configuration scores 97.9/99.7/97.3/94.7 for an average of 97.40, which is $- 0 . 7 0$ below default PFD but $+ 0 . 4 5$ above the reproduced Fast-WAM. Its close correspondence to the budget-reallocation row at 97.36 indicates that at the half-depth setting the gap to default PFD is already determined by $K$ and is not closed by adapter widening. The teacher therefore contributes useful signal even at half depth, and additional fine-tune depth on the video expert continues to absorb it.

LIBERO Average Success Rate (%)   
Figure 2: LIBERO average success rate for the three primary probes, Fast-WAM (reproduced), and PFD (default). Breaking matched-capacity (Pure FT) or temporal-correspondence (Shuffled Future) drops accuracy below the Fast-WAM baseline (red); the budget-reallocation control — redirecting video-side fine-tuning budget to a wider adapter (Width 1024 at $K _{v} = 6$ ) — closes only part of the PFD gap (amber). The supplementary fine-tune-depth check $K = 6$ ) is shown for comparison and lands at the similar level.

# 4.4 Inference overhead

Table 4: End-to-end inference latency. Slowdown is reported relative to Fast-WAM   

<table><tr><td>Method</td><td>Test-time future</td><td>Latency (ms)</td><td>Slowdown</td></tr><tr><td>Fast-WAM-Joint</td><td>joint video+action denoising</td><td>580</td><td>3.05×</td></tr><tr><td>Fast-WAM-IDM</td><td>generate future, then IDM</td><td>810</td><td>4.26×</td></tr><tr><td>Fast-WAM</td><td>none (current-only)</td><td>190</td><td>1.00×</td></tr><tr><td>PFD (ours)</td><td>none (current-only) + adapter</td><td>192</td><td>1.01×</td></tr></table>

A central practical question for any future-aware policy is how much foresight costs at deployment time. World action models that materialize future video at inference — either by jointly denoising future frames and actions, or by generating a future clip and running an inverse-dynamics module (IDM) on top — pay a multiplicative latency penalty over a current-only forward, because future frames must be produced before any action chunk can be emitted. Yuan et al. [2026] report that these two designs run at 580 ms and 810 ms per inference on the Wan2.2-5B backbone, whereas removing test-time future generation altogether brings the same backbone down to 190 ms — a $3 . 1 \times$ to $4 . 3 \times$ speedup at no loss in success rate (Yuan et al., 2026, Fig. 4). PFD inherits this current-only inference interface verbatim; the only question for deployment is whether the adapter forward at each denoising step erodes that advantage.

It does not. Table 4 reports end-to-end latency on a single H100 averaged over 50 trials per configuration, under the 10 flow-matching denoising steps used throughout this paper. PFD runs at 192 ms, +2 ms over the 190 ms current-only Fast-WAM baseline ${ \sim } 1 \%$ overhead) and accordingly $3 . 0 \times$ to $4 . 2 \times$ faster than the imagine-then-execute alternatives. The added cost is fully attributable to one forward through the 1.2M-parameter MLP $g _{\varphi}$ at each denoising step $( \sim 0 . 0 2 \%$ of the Wan2.2-5B backbone). PFD never instantiates the teacher mask at inference and never generates future video frames, exactly as specified in $\ S 3 . 5$ ; the deployment profile of the current-only interface is preserved, and the foresight-induced correction is recovered without re-introducing the latency cost that motivated removing test-time future generation in the first place.

# 5 Conclusion

We revisited the role of future video in world action models once test-time imagination is removed, and argued that future is best understood not as a prediction target nor as a regularizer to absorb, but as a compressible correction to be distilled. Privileged Foresight Distillation operationalizes this view with a same-backbone teacher–student construction and a small output-side adapter that absorbs the foresight residual. Three epistemic probes — matched-capacity, shuffled-future, and budget-reallocation — attribute the gain to the foresight signal itself, and PFD improves over Fast-WAM on both LIBERO and RoboTwin at negligible added inference cost while preserving the current-only inference interface exactly.

Limitations. Two limitations are worth noting. First, the construction is deliberately simple: a single output-side MLP adapter, a full-horizon teacher mask, and a single backbone family. More expressive adapter designs — multiscale, gated, or cross-attentive — and richer teacher-mask schedules remain to be explored. Second, our claims are empirical: we observe that the foresight residual is absorbable by a small adapter and that capacity, regularization, and budget-reallocation alternatives do not account for the gain, but we do not provide a formal characterization of when the residual admits a low-capacity approximation. A theoretical account would tell us a priori which task families and backbones PFD should help.

# References

Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, and Jun Zhu. Motus: A unified latent action world model. arXiv preprint arXiv:2512.13030, 2025.   
Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. $\pi _{0}$ : A vision-language-action flow model for general robot control. arXiv preprint arXiv:2410.24164, 2024a.   
Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pre-trained image-editing diffusion models. In International Conference on Learning Representations (ICLR), 2024b. URL https://openreview.net/forum?id=c0chJTSbci.   
Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, Hanbo Zhang, and Minzhao Zhu. GR-2: A generative video-language-action model with web-scale knowledge for robot manipulation. arXiv preprint arXiv:2410.06158, 2024. URL https://arxiv.org/abs/2410.06158.   
Dian Chen, Brady Zhou, Vladlen Koltun, and Philipp Krähenbühl. Learning by cheating. In Conference on Robot Learning (CoRL), 2019. URL https://arxiv.org/abs/1912.12294.   
Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, Weiliang Deng, Yubin Guo, Tian Nian, Xuanbing Xie, Qiangyu Chen, Kailun Su, Tianling Xu, Guodong Liu, Mengkang Hu, Huan-ang Gao, Kaixuan Wang, Zhixuan Liang, Yusen Qin, Xiaokang Yang, Ping Luo, and Yao Mu. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. arXiv preprint arXiv:2506.18088, 2025.   
Yilun Du, Mengjiao Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Joshua B. Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. In Advances in Neural Information Processing Systems (NeurIPS), 2023. URL https://arxiv.org/abs/2302.00111.   
Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. arXiv preprint arXiv:2301.04104, 2023. URL https://arxiv.org/abs/2301.04104.   
Nicklas Hansen, Hao Su, and Xiaolong Wang. TD-MPC2: Scalable, robust world models for continuous control. In International Conference on Learning Representations (ICLR), 2024. URL https://arxiv.org/abs/2310. 16828.   
Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In International Conference on Learning Representations (ICLR), 2022. URL https://openreview.net/forum?id=nZeVKeeFYf9.   
Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. In International Conference on Machine Learning (ICML), 2025. URL https://arxiv.org/abs/2412.14803. Spotlight.

Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246, 2024.   
Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, Yujun Shen, and Yinghao Xu. Causal world modeling for robot control. arXiv preprint arXiv:2601.21998, 2026.   
Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. arXiv preprint arXiv:2306.03310, 2023.   
Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. $\pi _{0 . 5}$ : A vision-language-action model with open-world generalization. arXiv preprint arXiv:2504.16054, 2025.   
Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, Timothy Lillicrap, and David Silver. Mastering Atari, Go, chess and shogi by planning with a learned model. Nature, 588(7839):604–609, 2020. doi: 10.1038/s41586-020-03051-4.   
Vladimir Vapnik and Akshay Vashist. A new learning paradigm: Learning using privileged information. Neural Networks, 22(5–6):544–557, 2009. doi: 10.1016/j.neunet.2009.06.042.   
Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In International Conference on Learning Representations (ICLR), 2024. URL https://openreview.net/forum?id=NxoFmGgWC9.   
Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-WAM: Do world action models need test-time future imagination? arXiv preprint arXiv:2603.16666, 2026. URL https://arxiv.org/abs/2603.16666.