---
title: "2604.25907"
---

# How Fast Should a Model Commit to Supervision? Training Reasoning Models on the Tsallis Loss Continuum

Chu-Cheng Lin Eugene Ie

{kitsing,eugeneie}@google.com

# Abstract

Adapting reasoning models to new tasks during post-training with only output-level supervision stalls under reinforcement learning from verifiable rewards (RLVR) when the initial success probability $p _{0}$ is small. Using the Tsallis $q$ -logarithm, we define a loss family $J _{Q}$ that interpolates between RLVR (at $q { =} 0$ , the exploitation pole) and the log-marginal-likelihood over latent trajectories (at $q { =} 1$ , the densityestimation pole). All members share the same per-example gradient direction, differing only by a scalar amplification $P _{\theta} ^{- q}$ that reweights each instance independently of the learning rate. This amplification is the mechanism that addresses cold-start stalling: under gradient flow, the exploitation pole requires $\Omega ( 1 / _{p _{ 0}} )$ time to escape cold start, while the density-estimation pole escapes in $\Theta \big ( \log ( 1 / p _{0} ) \big )$ ; intermediate $q$ trades escape speed against noise memorization. Because $P _{\theta}$ is intractable, we derive two Monte Carlo estimators from the two factorizations of the gradient: Gradient-Amplified RL (GARL) samples from the prior and amplifies the RL gradient, and Posterior-Attenuated Fine-Tuning (PAFT) importance-resamples from the posterior and runs standard SFT. Both have bias $\dot{O} \big ( q / \dot{M} P _{\theta} ^{q + 1} \big )$ ; GARL has lower variance, PAFT has semantically coherent gradients. On FinQA, HotPotQA, and MuSiQue, GARL at $q { =} 0 . 7 5$ substantially mitigates cold-start stalling, escaping cold start where GRPO fails entirely. In warm start, GARL at low $q$ dominates FinQA where training is stable; on HotPotQA and MuSiQue, GARL destabilizes during training, and PAFT at $q { =} 0 . 7 5$ provides stable gradients (best overall on HotPotQA at $4 7 . 9 \mathrm{ \ m a j} \ @ 1 6 .$ , $+ 1 4 . 4$ over GRPO).

# 1 Introduction

Language models reason most effectively when they generate latent computational trajectories — chains of thought, proof sketches, search traces — before producing an answer [Lin et al., 2021, Merrill and Sabharwal, 2024]. Reinforcement learning from verifiable rewards (RLVR) [DeepSeek-AI, 2025, Shao et al., 2024] is commonly used to learn such reasoning models, where the latent rationales are action sequences for reaching correct answers. With supervision only at the output level, RLVR can be prohibitively slow at cold start, when the initial model is too unaligned to make progress. Rao–Blackwellized rewards [Zhou et al., 2026] ensure non-zero reward (and thus non-zero gradients) for all trajectories, but as we show, this reduces gradient variance without addressing the escape-speed bottleneck. Even when RLVR succeeds, it is mode-seeking, and the reasoning capability boundary can narrow as training proceeds [Yue et al., 2025], limiting sample diversity and self-consistency decoding [Wang et al., 2023]. Instruction engineering supplies enough structure for SFT and RL to progress [Ouyang et al., 2022, DeepSeek-AI, 2025, Chu et al., 2025], but the recipe depends on task-specific prompts, and naive SFT on weak annotations risks memorizing label errors

![[99_Attachments/papers/images/tsallis-loss-continuum/99fbc2e100f586ed6cb23f29b40ea97dfa5ea3480b63be747e23f7f44bffb56e.jpg]]  
Figure 1: The $J _{Q}$ loss family is a continuum between exploitation $( q = 0$ ) and density estimation $( q = 1 )$ ) losses (poles at either end of the axis below); correspondingly, commitment is the induced gradient amplification $( P _{\theta} ^{- q}$ ; top arrow). High $q$ resolves ambiguity (fast cold-start escape) but also memorizes noise; low $q$ resolves noise (robust filtering) but cannot escape cold start. $p _{0}$ denotes initial success probability; convergence results assume bounded score (Section 5).

[Zhang and Sabuncu, 2018]. The two failure modes — cold-start stagnation and noise memorization — pull in opposite directions, and a unifying theoretical account has been lacking.

We provide such an account, built around a per-instance gradient amplification that directly addresses the cold-start stalling problem. Let $P _{\pmb{ \theta}} = p _{\pmb{ \theta}} ( \mathbf{y} ^{*} \ | \ \mathbf{x} ^{*} )$ denote the model’s conditional success probability. We show that exploitation and density estimation behaviors arise as two endpoints (or poles) of a one-parameter loss continuum $J _{Q}$ derived from this quantity, under the Tsallis $q$ - logarithm [Tsallis, 1988]: the exploitation pole $J _{0} \overset{ \cdot} { =} \mathbb{E} [ 1 - P _{\theta} ]$ (maximization of expected accuracy, equivalent to RLVR under exact-match reward1) and the density-estimation pole $\bar{J _{1}} = \mathbb{E} [ - \log P _{\pmb{ \theta}} ]$ (maximization of log-marginal-likelihood over latent trajectories). All members share the same per-example gradient direction, differing only by a scalar amplification $P _{\theta} ^{- q}$ (Figure 1): $q$ , which we denote as commitment, amplifies the pull on low- ${ \mathbf{}} \cdot P _{\theta}$ (unfamiliar) examples relative to high- $P _{\theta}$ (familiar) ones. Since the learning rate sets one global step size for all examples, no global learning rate can exactly reproduce this per-instance reweighting. This amplification is precisely what is absent from RLVR’s success-probability dynamics, and is the mechanism that addresses cold-start stalling.

Commitment is thus the training-time analog of the inference-time exploration-exploitation tradeoff studied in RL [Lee et al., 2018, Nachum et al., 2018]: low $q$ concentrates on what the model already knows, high $q$ pushes toward unfamiliar supervision. High commitment $( q \to 1 ) ,$ ) resolves ambiguity — escaping cold start in $\Theta \big ( \log \big ( 1 / p _{0} \big ) \big )$ time (Theorem 5.2) — but memorizes noise, since the model fits the training distribution exactly, including errors [Zhang and Sabuncu, 2018]. Low commitment $( q \to 0 )$ ) resolves noise — the bounded loss and escort tempering filter corrupted labels (Proposition C.2) — but escape slows to $\Omega ( 1 / _{p _{ 0}} )$ (Theorem 5.1). Intermediate $q$ balances this tradeoff between ambiguity resolution and noise resistance.

Because $P _{\pmb{ \theta}}$ is intractable, practical optimization requires Monte Carlo estimation. The gradient admits two factorizations — through the RL and FT endpoints (Figure 2) — each of which extends a classical estimator at its endpoint to the full continuum. The two resulting methods are complementary: one uses all $M$ sampled rationales but mixes in contributions that may contradict the answer; the other approximately samples from the posterior over rationales that agree with the answer and runs standard fine-tuning on them, trading statistical efficiency for semantically coherent gradients. Both have the same bias; the choice is dictated by the training regime.

![[99_Attachments/papers/images/tsallis-loss-continuum/fd5235b385a4bb8afbf8ff111c745e96bfb5dd6efec1f509b79720fe5bb1084d.jpg]]  
Figure 2: Two estimators from one gradient identity. The $J _{Q}$ gradient factors through either the RL endpoint $\nabla _{\boldsymbol{ \theta}} \ell _{0}$ (yielding GARL) or the FT endpoint $\nabla _{\boldsymbol{ \theta}} \ell _{1} $ (yielding PAFT). Both have the same bias $O ( { q} / { M P _{\theta} ^{q + 1}} )$ . GARL conditionally Rao–Blackwellizes PAFT (with respect to the resampling randomness): it has lower variance but mixes bad rationales into the gradient, while PAFT excludes them via posterior sampling at the cost of resampling noise. GARL recovers RB-REINFORCE $( q { =} 0 )$ ) and IWAE $( q { =} 1 )$ ; PAFT recovers EM $\scriptstyle q = 1 )$ . The choice is regime-dependent: GARL at large $q$ for cold-start escape; in warm start, GARL at low $q$ when training is stable, PAFT at $q { =} 0 . 7 5$ when GARL collapses (Section 7).

Overview of contributions. Figures 1 and 2 visualize the loss continuum and the gradient duality; our contributions follow from the $P _{\theta} ^{- q}$ amplification factor (Proposition 4.1).

1. The $J _{Q}$ loss family (Sections 3 to 5). $J _{Q}$ interpolates between a bounded, noise-robust loss at $\dot{\boldsymbol{ q}} = 0$ and an unbounded, mode-covering loss at $q = 1$ , with minimizers given by the escort distribution $\theta _{j} ^{*} \propto \alpha _{j} ^{1 / q}$ (Theorem 3.1) — a training-time analog of inference temperature — and a dispersion penalty that encourages uniform success across training examples (Proposition B.1). All members share the same gradient direction, differing only by $P _{\theta} ^{- q}$ , which controls cold-start escape speed: the exploitation pole cannot escape faster than $\mathrm{ \Delta} \mathrm{ \ddot{\Omega}} \Omega ( { 1} / { r _{p}} _{0} )$ (Theorem 5.1), while the density-estimation pole escapes in $\Theta ( \log ( 1 / p _{0} ) )$ (Theorem 5.2).   
2. Two gradient estimators: GARL and PAFT (Section 6). The gradient admits two factorizations — via the RL endpoint $( P _{\theta} ^{- q} \nabla _{\theta} \ell _{0} )$ and the FT endpoint $( P _{\pmb{ \theta}} ^{1 - q} \nabla _{\pmb{ \theta}} \ell _{1} )$ — each yielding a practical Monte Carlo estimator. Gradient-Amplified RL (GARL) samples trajectories from the prior and amplifies the RL gradient, generalizing RB-REINFORCE $[ q { =} 0$ ; Zhou et al., 2026] and the IWAE gradient estimator $[ q { =} 1$ ; Burda et al., 2015]. Posterior-Attenuated Fine-Tuning (PAFT) approximately samples from the posterior $p _{\pmb{ \theta}} ( \mathbf{z} \mid \mathbf{x} ^{*} , \mathbf{y} ^{*} )$ over rationales that agree with the answer and runs standard fine-tuning on them, generalizing the E-step of EM $[ q { =} 1$ ; Dempster et al., 1977, Phan et al., 2023]. Both have the same bias $O ( q / M P _{\theta} ^{q + 1} )$ ; GARL has lower variance, PAFT produces semantically coherent gradients. GARL is essential at cold start (posterior sampling yields no trajectories); in warm start, GARL at low $q$ works when training is stable (FinQA), but destabilizes on HotPotQA and MuSiQue. PAFT does not collapse on any benchmark we tested, at the cost of slower per-step learning (Section 7).   
3. Empirical validation (Section 7). On three reasoning benchmarks (FinQA, HotPotQA, MuSiQue) with strict (exact-match) training rewards, GARL at intermediate $q$ escapes cold start where GRPO fails entirely. At warm start, the best stable method at each benchmark improves maj $\ @ 1 6$ over GRPO by $+ 6 . 6$ to $+ 1 4 . 4$ points: GARL at $q { =} 0 . 2 5$ leads on FinQA (38.7 vs. 26.9) where training is stable; PAFT at $q { =} 0 . 7 5$ is best on HotPotQA (47.9 vs. 33.5) where GARL collapses at all tested $q$ , and on MuSiQue (22.4 vs. 15.8) where GARL’s higher peak does not survive training.

# 2 Setup and Background

We consider supervised conditional generation with latent reasoning trajectories. Let $\mathbf{\Theta} \Theta \subseteq \mathbb{R} ^{d}$ be the parameter space of an autoregressive language model $p _{\theta}$ with alphabet $\Sigma$ . Inputs come from a

task distribution we do not model. We train on a supervised dataset $\mathcal{D}$ of input-output pairs $\left( \mathbf{x} ^{*} , \mathbf{y} ^{*} \right)$ where $\mathbf{x} ^{*} \in \mathcal{X} \subseteq \Sigma ^{*}$ and $\mathbf{y} ^{*} \in \mathcal{V} \subseteq \Sigma ^{*}$ .

Generative story. Given input $\mathbf{x}$ , the model samples an unannotated latent rationale $\mathbf{z} \in \mathcal{Z} \subseteq \Sigma ^{*}$ from $p _{\pmb{ \theta}} ( \cdot \mid \mathbf{x} )$ , then generates an output $\hat{\mathbf{ y}} \sim p _{\pmb{ \theta}} ( \cdot \ | \ \mathbf{x} , \mathbf{z} )$ . This defines the joint $p _{\pmb{ \theta}} ( \mathbf{z} , \mathbf{y} \mid \mathbf{x} ) =$ $p _{\pmb{ \theta}} ( \mathbf{z} \mid \mathbf{x} ) p _{\pmb{ \theta}} ( \mathbf{y} \mid \mathbf{x} , \mathbf{z} )$ and the induced marginal $\begin{array} { r} { p _{\pmb{ \theta}} ( \mathbf{y} \mid \mathbf{x} ) = \sum _{\mathbf{z} \in \mathcal{Z}} p _{\pmb{ \theta}} ( \mathbf{z} , \mathbf{y} \mid \mathbf{x} )} \end{array}$ . 2

The latent $\mathbf{z}$ may represent a chain of thought [Wei et al., 2022], proof trace, search trajectory, program, or other internal computational object. We treat $\mathbf{z}$ as an operational latent: with supervision only at the output level, the latent trajectory mediates the output distribution.

Success probability and endpoint losses. For each supervised example $\left( \mathbf{x} ^{*} , \mathbf{y} ^{*} \right)$ , the central quantity is the success probability $P _{\pmb{ \theta}} \triangleq p _{\pmb{ \theta}} ( \mathbf{y} ^{*} \mid \mathbf{x} ^{*} )$ . From this we define two endpoint losses: the exploitation loss $J _{0} ( \pmb{ \theta} ) \ \triangleq \ \mathbb{E} _{( \mathbf{x} ^{*} , \mathbf{y} ^{*} ) \sim \mathcal{D}} [ 1 - P _{\pmb{ \theta}} ]$ and the density-estimation loss $J _{1} ( \pmb{ \theta} ) \ \triangleq$ $\mathbb{E} ( \mathbf{x} ^{*} , \mathbf{y} ^{*} ) { \sim} \mathcal{D} \left[ - \log P _{\theta} \right]$ . Both are minimized at 0 when $P _{\theta} = 1$ , but transform $P _{\theta}$ into optimization signal differently. Under exact-match supervision $( R ( \hat{\mathbf{ y}} , \mathbf{y} ^{*} ) = \mathbb{I} ( \hat{\mathbf{ y}} = \mathbf{y} ^{*} ) )$ , $J _{0}$ equals 1 minus the expected reward (Proposition A.1), so minimizing $J _{0}$ is equivalent to maximizing expected reward.3

The $J _{Q}$ family. We interpolate using the Tsallis $q$ -logarithm [Tsallis, 1988]:

$$
\log_{q} (u) = \frac{u ^{1 - q} - 1}{1 - q}, \quad 0 <   u \leq 1, \tag{1}
$$

with $\begin{array} { r } { \log _{1} ( u ) \triangleq \operatorname* { l i m } _{q \to 1} \log _{q} ( u ) = \log u } \end{array}$ . We define the loss family

$$
J _{Q} (\boldsymbol{\theta}, q) = \underset{(\mathbf{x} ^{*}, \mathbf{y} ^{*}) \sim \mathcal{D}} {\mathbb{E}} [ - \log_{q} (P _{\boldsymbol{\theta}}) ], \tag{2}
$$

or equivalently

$$
J _{Q} (\boldsymbol{\theta}, q) = \underset{(\mathbf{x} ^{*}, \mathbf{y} ^{*}) \sim \mathcal{D}} {\mathbb{E}} \left[ - \log_{q} \left(\sum_{\mathbf{z} \in \mathcal{Z}} p _{\boldsymbol{\theta}} \left(\mathbf{z}, \mathbf{y} ^{*} \mid \mathbf{x} ^{*}\right)\right) \right].
$$

It recovers the endpoints: $J _{Q} ( \pmb { \theta } , 0 ) = J _{0} ( \pmb { \theta } )$ and $J _{Q} ( \pmb { \theta } , 1 ) = J _{1} ( \pmb { \theta } )$ .

# 3 Loss Landscape of the $J _{Q}$ Continuum

For a fixed supervised example $\left( \mathbf{x} ^{*} , \mathbf{y} ^{*} \right)$ , define the per-example $q$ -loss

$$
\ell_{q} \left(\boldsymbol{\theta}; \mathbf{x} ^{*}, \mathbf{y} ^{*}\right) \triangleq - \log_{q} P _{\boldsymbol{\theta}} = \frac{1 - P _{\boldsymbol{\theta}} ^{1 - q}}{1 - q}, \tag{3}
$$

so that $J _{Q} ( \pmb { \theta } , q ) = \mathbb{E} _{( \mathbf{x} ^{*} , \mathbf{y} ^{*} ) \sim \mathcal{D} } [ \ell _{q} ( \pmb { \theta } ; \mathbf{x} ^{*} , \mathbf{y} ^{*} ) ]$ . At $q = 0$ this gives $\ell _{0} = 1 - P _{\theta}$ (bounded in $[0, 1] .$ ); at $q = 1$ it gives $\ell _{1} = - \log P _{\theta}$ (unbounded as $P _{\theta} \to 0$ ). The parameter $q$ shapes the loss landscape in four ways:

• Dataset-level coverage: $q > 0$ penalizes non-uniform success across training examples (dispersion penalty).   
• Prediction-level coverage: the minimizer is the escort distribution $\theta _{j} ^{*} \propto \alpha _{j} ^{1 / q}$ , interpolating from mode-seeking $( q \to 0 )$ ) to mode-covering $( q = 1 )$ ).   
• Propriety: $q = 1$ is the unique strictly proper scoring rule in the family; $q < 1$ introduces controlled mode-seeking bias.   
• Robustness: at $q \ < \ 1$ the loss is bounded and the escort tempering concentrates the minimizer away from corrupted labels; at $q = 1$ the model fits noise exactly.

We develop the first two below; formal statements for all four are in Section B.

# 3.1 Dataset-level coverage: the dispersion penalty

Let $\begin{array} { r } { \bar{P} \triangleq \mathbb{E} _{( \mathbf{x} ^{*} , \mathbf{y} ^{*} ) \sim \mathcal{D} } [ P _{\pmb { \theta} } ] } \end{array}$ denote the mean success probability. The exploitation loss $J _{0} = 1 - \bar{P}$ depends only on $\bar{P}$ and is indifferent to how success is distributed across examples. For $q > 0 , - \log _{q}$ is strictly convex, so Jensen’s inequality gives $J _{Q} \geq - \log _{q} ( \bar{P} )$ : the loss penalizes non-uniform success. To second order, the excess loss scales as $\begin{array} { r } { \frac { q } { 2 } \bar{P} ^{- q - 1} \dot{\mathbf { V} } \mathbf{a r} _{\mathcal{D} } ( P _{\pmb { \theta} } ) } \end{array}$ , with the penalty coefficient monotonically increasing in $q$ .

# 3.2 Prediction-level coverage: the escort minimizer

At the prediction level, $q$ controls whether the model’s output distribution matches the data or concentrates on the mode. Consider a categorical model with a single input $\mathbf{x} ^{*}$ , outputs $\{ v _{1} , \dotsc , v _{N} \}$ model $p _{\pmb { \theta} } ( v _{j} \mid \mathbf{x} ^{*} ) = \theta _{j} \in \Delta _{N}$ , and empirical frequencies $\alpha _{j} > 0$ with $\textstyle \sum _{j} { \alpha _{j} } = 1$ .

The escort distribution [Beck and Schögl, 1993] of order $\beta$ of a distribution $\alpha$ is $\alpha _{j} ^{\beta} / \Sigma _{k} \alpha _{k} ^{\beta}$ ; setting $\beta = { ^ 1 } / q$ gives the data distribution tempered at temperature $q$ .

Theorem 3.1. [Minimizers of $J _{Q}$ in the categorical model] For $q \in ( 0 , 1 ]$ , the unique minimizer of $\begin{array} { r } { J _{Q} ( \pmb { \theta } , q ) = \sum _{j} \alpha _{j} ( - \log _{q} \theta _{j} ) } \end{array}$ over $\Delta _{N}$ is the escort distribution of order $1 / q$ :

$$
\theta_{j} ^{*} (q) = \frac{\alpha_{j} ^{1 / q}}{\sum_{k = 1} ^{N} \alpha_{k} ^{1 / q}}, \quad j = 1, \dots , N. \tag{4}
$$

For $q = 0$ , the objective is linear and minimized at any vertex $e _{j}$ with $j \in \mathrm { a r g m a x } _{k} \alpha _{k}$

Proof sketch. For $q > 0$ , strict convexity ensures uniqueness. Lagrange multipliers give $\alpha _{j} \theta _{j} ^{- q} = \mu$ for all $j$ , yielding $\theta _{j} \propto \alpha _{j} ^{1 / q}$ . □

The escort distribution interpolates continuously from full coverage $( q = 1 \colon \theta ^{*} = \alpha )$ $( q = 1$ to pure mode seeking $( q \to 0 ; \theta ^{*}$ concentrates on the most frequent output). In particular, $q = 1$ is the unique strictly proper scoring rule in the $J _{Q}$ family (Corollary B.3).

# 4 Gradient Geometry of $J _{Q}$

All members of $J _{Q}$ share the same per-example gradient direction. The gradient factors through either the RL endpoint $\nabla _{\pmb { \theta} } \ell _{0}$ or the FT endpoint $\nabla _{\boldsymbol { \theta} } \ell _{1}$ , motivating the two Monte Carlo estimators of Section 6.

Proposition 4.1 (Gradient geometry and dual factorization). For any fixed supervised example $\left( \mathbf{x} ^{*} , \mathbf{y} ^{*} \right)$ with $P _{\theta} > 0$ and any $q \in [0, 1]$ ,

$$
\nabla_{\boldsymbol{\theta}} \ell_{q} \left(\boldsymbol{\theta}; \mathbf{x} ^{*}, \mathbf{y} ^{*}\right) = \underbrace{P _{\boldsymbol{\theta}} ^{- q}} _{\text{amplify}} \nabla_{\boldsymbol{\theta}} \ell_{0} \left(\boldsymbol{\theta}; \mathbf{x} ^{*}, \mathbf{y} ^{*}\right) = \underbrace{P _{\boldsymbol{\theta}} ^{1 - q}} _{\text{attenuate}} \nabla_{\boldsymbol{\theta}} \ell_{1} \left(\boldsymbol{\theta}; \mathbf{x} ^{*}, \mathbf{y} ^{*}\right). \tag{5}
$$

rule and , the sec $\begin{array} { r } { \frac { d } { d u } \log _{q} ( u ) = u ^{- q} \colon \nabla _{\theta} \ell _{q} = - P _{\theta} ^{- q} \nabla _{\theta} P _{\theta} = P _{\theta} ^{- q} \nabla _{\theta} \ell _{0} } \end{array}$ . Since $\nabla _{\pmb { \theta} } \ell _{0} =$ $- \nabla _{\pmb { \theta} } P _{\pmb { \theta} } = P _{\pmb { \theta} } \nabla _{\pmb { \theta} } \ell _{1}$

The scalar rescales either the RL endpoint gradient (by $P _{\theta} ^{- q} \in [ 1 , \infty )$ , amplification) or the FT endpoint gradient (by $P _{\theta} ^{1 - q} \in [0, 1]$ , attenuation). Setting $q = 0$ recovers $\nabla \ell _{0}$ (no amplification); $q = 1$ recovers $\nabla \ell _{1}$ (no attenuation).

The scalar $P _{\pmb { \theta} } ^{- q}$ controls both cold-start escape speed $( \dot{p} = p ^{2 - q} \| s \| ^{2}$ , yielding the $\Omega ( 1 / _{p _ { 0} } )$ versus $\Theta ( \log ( 1 / { p _{0} } ) )$ separation of Section 5) and finite-sample estimator bias (larger $q$ increases the $O ( q / ( M P _{\theta} ^{q + 1} ) )$ ) bias of Section 6). Each factorization motivates a Monte Carlo estimator: the RL factorization yields GARL (prior sampling with amplification; Section 6.1), the FT factorization yields PAFT (posterior sampling with attenuation; Section 6.2).

# 5 Commitment Dynamics under Gradient Flow

Under gradient flow, escape from a cold start $( p _{0} = P _{\pmb { \theta} ( 0 ) } \ll 1 )$ ) takes $\Omega ( 1 / _{p _ { 0} } )$ time at the exploitation pole $( q { = } 0 )$ but only $\Theta \big ( \log \big ( 1 / p _{0} \big ) \big )$ at the density-estimation pole $\scriptstyle ( q = 1 )$ ). This exponential separation in $1 / p _{0}$ is governed by the amplification factor $P _{\theta} ^{- q}$ and the dynamics $\dot{p} = p ^{2 - q} \lVert s ( \pmb { \theta } ) \rVert ^{2}$ . Our analysis is stylized: it tracks single-example success probability under continuous-time gradient flow, isolating the role of the amplification factor rather than fully modeling multi-example LM optimization.

# 5.1 Dynamics of the success probability

We study gradient flow, the continuous-time limit of gradient descent, in which parameters evolve as $\dot{\pmb { \theta} } = - \nabla _{\pmb { \theta} } \ell ( \pmb { \theta } )$ [Su et al., 2016]. This removes step-size effects and yields closed-form rates that capture the qualitative behavior of discrete optimization. The results below require no convexity: ${ \dot{p} } \geq 0$ always (Equation (6)), so $p$ is monotone along the flow.

Fix a single example’s $q$ -loss $\ell _{q} ( \pmb \theta ) = - \log _{q} ( P _{\pmb \theta} )$ , $\pmb \theta \in \mathbb{R} ^{d}$ . Let $p ( t ) \triangleq P _{\pmb { \theta} ( t ) }$ denote the success probability along the flow, with time derivative ${ \dot{p} } \triangleq d p / d t$ . We combine $\dot{p} ( t ) = \nabla _{\pmb { \theta} } P _{\pmb { \theta} ( t ) } \cdot \dot{\pmb { \theta} } ( t )$ (chain rule), and $\begin{array} { r } { \Dot { \pmb { \theta } } ( t ) = - \nabla _{\pmb { \theta} } \ell _{q} ( \pmb { \theta } ( t ) ) = P _{\pmb { \theta} ( t ) } ^{- q} \nabla _{\pmb { \theta} } P _{\pmb { \theta} ( t ) } } \end{array}$ (the second equality uses Proposition 4.1, which gives $\nabla _{\pmb { \theta} } \ell _{q} = - P _{\pmb { \theta} } ^{- q} \nabla _{\pmb { \theta} } P _{\pmb { \theta} } )$ . Substituting and writing $\nabla _{\pmb \theta} P _{\pmb \theta ( t )} = P _{\pmb \theta ( t )} \nabla _{\pmb \theta} \log P _{\pmb \theta ( t )}$ with score $s ( \pmb { \theta } ) \triangleq \nabla _{\pmb { \theta} } \log P _{\pmb { \theta} }$ ,

$$
\dot{p} = \nabla_{\boldsymbol{\theta}} P _{\boldsymbol{\theta} (t)} \cdot \dot{\boldsymbol{\theta}} (t) = \nabla_{\boldsymbol{\theta}} P _{\boldsymbol{\theta} (t)} \cdot \left(P _{\boldsymbol{\theta} (t)} ^{- q} \nabla_{\boldsymbol{\theta}} P _{\boldsymbol{\theta} (t)}\right) = P _{\boldsymbol{\theta} (t)} ^{- q} \| \nabla_{\boldsymbol{\theta}} P _{\boldsymbol{\theta} (t)} \| ^{2} = p ^{2 - q} \| s (\boldsymbol{\theta} (t)) \| ^{2}. \tag{6}
$$

The entire effect of $q$ on convergence speed is captured by the exponent $2 - q$ on $p$ ; the factor $\| s ( \pmb \theta ) \| ^{2}$ depends on the architecture but not on $q$ .

# 5.2 Cold-start escape rates

Let $p _{0} \triangleq p ( 0 ) \ll 1$ . With $\| s \|$ approximately constant, Equation (6) implies that the escape time to a target $\delta$ is $\begin{array} { r } { T \sim \int _{p _ { 0} } ^{\delta} u ^{- ( 2 - q )} d u } \end{array}$ , and the exponent $2 - q$ controls its growth as $p _{0} \to 0$ : at $q = 0$ the integrand is $u ^{- 2}$ and $T$ diverges as $1 / p _{0}$ ; at $q = 1$ the integrand is $u ^{- 1}$ and $T$ diverges only as $\log ( 1 / p _{0} )$ (equivalently, $p ( t ) = p _{0} \bar{e} ^{t}$ under ${ \dot{p} } = p$ ). We formalize this separation in two results.4 The first requires only an upper bound on the score norm and establishes that the exploitation pole is provably slow. The second adds a lower bound and shows the density-estimation pole is provably fast, giving tight $\Theta ( \cdot )$ rates across the continuum.

Theorem 5.1. [Exploitation is provably slow] Let $\pmb \theta \in \mathbb{R} ^{d}$ parameterize any differentiable model. Consider gradient flow on $\ell _{q} ( \pmb { \theta } ) = - \log _{q} ( P _{\pmb { \theta} } )$ , starting from $p _{0} = P _{\pmb { \theta} ( 0 ) } \in ( 0 , 1 / 2 ]$ with fixed target $\delta \in ( 0 , 1 / 2 ]$ . Suppose only that $\left\| s ( \pmb \theta ( t ) ) \right\| \leq C$ throughout the trajectory. Then as $p _{0} \to 0$ :

$$
T _{q} (p _{0}, \delta) = \Omega \left(\frac{p _{0} ^{- (1 - q)}}{1 - q}\right) f o r q \in [ 0, 1),
$$

$$
T _{1} (p _{0}, \delta) = \Omega \left(\log \frac{1}{p _{0}}\right).
$$

In particular, the exploitation pole cannot escape cold start faster than $\Omega ( 1 / _{p _ { 0} } )$

Proof sketch. From $\dot{p} = p ^{2 - q} \lVert s \rVert ^{2} \leq C ^{2} p ^{2 - q}$ , the success probability grows no faster than $C ^{2} p ^{2 - q}$ . Integrating: Tq ≥ 1C2 R δp $\begin{array} { r } { T _{q} \geq \frac { 1 } { C ^{2} } \int _{p _ { 0} } ^{\delta} u ^{- ( 2 - q )} d u } \end{array}$ , which evaluates to $\Omega \big ( p _{0} ^{- ( 1 - q )} / ( 1 - q ) \big )$ . □

The upper bound $\| s \| \leq C$ holds for any autoregressive softmax model with bounded parameterto-logit Jacobian: the per-trajectory score $\begin{array} { r } { \nabla _{\theta} \log p ( \mathbf{z} , \mathbf{y} ^{*} \mid \mathbf{x} ^{*} ) = \sum _{t} ( e _{y _ { t} } - p _{t} ) ^{\top} \nabla _{\theta} z _{t} } \end{array}$ combines bounded softmax residuals with the Jacobian $\nabla _{\pmb { \theta} } z _{t}$ , and $s$ is a posterior expectation of these, so $\| s \|$ is bounded whenever the weights are bounded and activations Lipschitz. No matter how favorable the

architecture, the exploitation pole requires escape time at least linear in $1 / p _{0}$ — a prediction Section 7 confirms: $q = 0$ fails to escape cold start in practice.

Theorem 5.2. [Tight cold-start escape rates] Under the same setup as Theorem 5.1, suppose additionally that $\lVert \bar{s} ( \pmb \theta ( t ) ) \rVert \geq c > 0$ throughout the trajectory. Then:

1. General $q \in [ 0 , 1 )$ :

$$
T _{q} (p _{0}, \delta) = \Theta \left(\frac{p _{0} ^{- (1 - q)}}{1 - q}\right) a s p _{0} \rightarrow 0.
$$

2. Density-estimation pole $\displaystyle q = 1 .$ ):

$$
T _{1} (p _{0}, \delta) = \Theta \left(\log \frac{1}{p _{0}}\right) a s p _{0} \to 0.
$$

3. Speedup ratio: for any $q < q ^{\prime}$ with $q ^{\prime} \leq 1$ ,

$$
\frac{T _{q} (p _{0} , \delta)}{T _{q ^{\prime}} (p _{0} , \delta)} \to \infty a s p _{0} \to 0.
$$

Proof sketch. The lower bound on $\| s \|$ gives $\dot{p} \ge c ^{2} p ^{2 - q}$ , yielding the matching upper bound $\begin{array} { r } { T _{q} \le \frac { 1 } { c ^{2} } \int _{p _ { 0} } ^{\delta} u ^{- ( 2 - q )} d u . } \end{array}$ . Combined with Theorem 5.1, this gives the $\Theta ( \cdot )$ bounds. □

Robustness of the separation. The upper bound $\| s \| \leq C$ alone is enough for Theorem 5.1’s $\Omega ( \cdot )$ time bound; the additional lower bound $\| s \| \geq c$ is used only to promote this to the matching $\Theta ( \cdot )$ in Theorem 5.2. The $q$ -dependent separation itself comes from the assumption-free factor $p ^{{ \bar{2} } - q }$ in Equation (6), so the ordering across poles survives even where $\| s \| \geq c$ fails — at a critical point, for instance, every $q$ stalls equally. Section C.1 works out exact escape times for a sigmoid model.

Why momentum-based optimization cannot substitute for $q$ . The parameter $q$ controls perinstance commitment: how much to prioritize hard instances relative to easy ones. This is orthogonal to the global step size set by the learning rate. Momentum-based adaptive optimizers such as Adam [Kingma and Ba, 2014] adjust per-parameter step sizes aggregated across examples, but cannot compensate for per-example reweighting. The scalars $P _{\theta} ^{- q}$ (for GARL) and $P _{\theta} ^{1 - q}$ (for PAFT) are thus preserved under both minibatch SGD and Adam, and the cold-start separation persists in practice.

Noise fitting is symmetric. The same machinery gives a dual result for label noise: for example, in the binary categorical model with symmetric label-flip rate $\epsilon$ , the time to grow noise contamination $\tilde{p} = 1 - p _{\pmb { \theta} } ( c \mid \mathbf{x} ^{*} )$ to target level $\eta$ scales as $T _{q} ^{\mathrm { n o \bar{i} s e } } ( \eta ) = \Theta ( \eta ^{q + 1} / ( \bar{( q} + 1 ) \epsilon ) )$ , with speedup ratio $T _{q} / T _{q ^ { \prime} } = \Theta ( \eta ^{- ( q ^ { \prime} - q ) } )$ for $q < q ^{\prime}$ (Proposition C.2). The speedup ratio matches the cold-start speedup $\Theta ( p _{0} ^{- ( q ^ { \prime} - q ) } )$ exactly in form: the same amplification $P _{\theta} ^{- q}$ accelerates commitment to clean and corrupted supervision alike, with matching exponents in $p _{0}$ and $\eta$ . High commitment thus compresses both timescales — the time to resolve ambiguity and the time to memorize noise.

SFT-then-RL asymmetry. The cold-start escape and noise fitting results explain the familiar SFT-then-RL pipeline [Ouyang et al., 2022, DeepSeek-AI, 2025, Chu et al., 2025]. SFT on annotated (input, CoT, answer) triples is the $q = 1$ pole with a degenerate proposal (marginalization collapses onto the supervised CoT), so it escapes in $\Theta ( \log ( 1 / p _{0} ) )$ via $P _{\theta} ^{- 1}$ amplification; RL $( q = 0 )$ ) pays the full $\Theta ( 1 / \bar{p _{0} } )$ cost. Switching to RL after SFT then halts commitment to noisy annotations: $q = 1$ memorizes noise fastest $( T _{1} ^{\mathrm { n o i s e} } = \Theta ( \eta ^{2} / \epsilon ) )$ ) while $q = 0$ does not memorize at all $( \mathrm { l i m } _{q \to 0 ^ { +} } T _{q} ^{\mathrm { n o i s e} } ( \eta ) = \infty$ for any $\eta > 0$ ; Proposition C.2). The $J _{Q}$ continuum replaces this hard switch with a smooth interpolation.

# 6 Gradient Estimators for $J _{Q}$

The marginal $\begin{array} { r } { P _{\pmb { \theta} } = \sum _{\mathbf z \in \mathcal Z} p _{\pmb { \theta} } ( \mathbf z , \mathbf y ^{*} \mid \mathbf x ^{*} ) } \end{array}$ in $\nabla _{\pmb { \theta} } J _{Q}$ is intractable, so we estimate the gradient by Monte Carlo. The dual factorization (Proposition 4.1) yields two natural estimators:

• GARL (Section 6.1): sample from the prior $p _{\pmb { \theta} } ( \mathbf{z} \mid \mathbf{x} ^{*} )$ , estimate $\nabla _{\pmb { \theta} } \ell _{0}$ and $P _{\theta}$ from the same samples, amplify by $\bar{( w _{M} ) } ^{- q}$ .   
• PAFT (Section 6.2): approximately sample from the posterior $p _{\pmb { \theta} } ( \mathbf{z} \mid \mathbf{x} ^{*} , \mathbf{y} ^{*} )$ , estimate $\nabla _{\pmb { \theta} } \ell _{1}$ via teacher forcing, attenuate by $( \bar{w} _{M} ) ^{1 - q}$ .

Drop-in compute cost. Both estimators are drop-in replacements for RB-REINFORCE/RLOO at the same rollout budget. GARL replaces the scalar 1 in RB-RLOO with $( \bar{w} _{M} ) ^{- q}$ , reusing the $M$ prior samples and per-token log-probabilities RB-RLOO already computes [Zhou et al., 2026]; the only added work is the scalar $\bar{( w _{M} ) } ^{- q}$ and the leave-one-out baseline in Equation (12), both $O ( M )$ in compute. PAFT adds one categorical resample over the $M$ prior weights, followed by teacher forcing on $K$ resampled trajectories whose tokens have already been generated. Neither requires forward passes beyond what RL training already does. In our experiments (Section 7), GRPO, GARL, and PAFT all use $M = 3 2$ rollouts per prompt at training time.

# 6.1 GARL: Gradient-Amplified RL

# 6.1.1 A plug-in Monte Carlo estimator

Fix a supervised example $\left( \mathbf{x} ^{*} , \mathbf{y} ^{*} \right)$ and draw $M$ i.i.d. latent trajectories $\mathbf{z} ^{( 1 )} , \ldots , \mathbf{z} ^{( M )} \sim p _{\pmb { \theta} } ( \cdot \mid \mathbf{x} ^{*} )$ Define the per-sample likelihood weight and gradient contribution:

$$
w _{m} \triangleq p _{\boldsymbol{\theta}} \left(\mathbf{y} ^{*} \mid \mathbf{x} ^{*}, \mathbf{z} ^{(m)}\right), \quad g _{m} \triangleq - w _{m} \nabla_{\boldsymbol{\theta}} \log p _{\boldsymbol{\theta}} \left(\mathbf{z} ^{(m)}, \mathbf{y} ^{*} \mid \mathbf{x} ^{*}\right), \tag{7}
$$

with empirical means $\begin{array} { r } { \bar{w} _{M} \triangleq \frac { 1 } { M } \sum _{m} w _{m} } \end{array}$ and $\begin{array} { r } { \bar{g} _{M} \triangleq \frac { 1 } { M } \sum _{m} g _{m} \quad } \end{array}$ . By the log-trick,

$$
\mathbb{E} \left[ \bar{w} _{M} \right] = P _{\boldsymbol{\theta}}, \quad \mathbb{E} \left[ \bar{g} _{M} \right] = - \sum_{\mathbf{z}} \nabla_{\boldsymbol{\theta}} p _{\boldsymbol{\theta}} \left(\mathbf{z}, \mathbf{y} ^{*} \mid \mathbf{x} ^{*}\right) = - \nabla_{\boldsymbol{\theta}} P _{\boldsymbol{\theta}} = \nabla_{\boldsymbol{\theta}} \ell_{0}. \tag{8}
$$

Plugging these into the RL factorization of Proposition 4.1 yields the plug-in estimator

$$
\widehat{\nabla_{\boldsymbol{\theta}} \ell_{q}} (q, \boldsymbol{\theta}; \mathbf{x} ^{*}, \mathbf{y} ^{*}, M) \triangleq \frac{\bar{g} _{M}}{(\bar{w} _{M}) ^{q}}. \tag{9}
$$

The dataset-level estimator of $\nabla _{\pmb { \theta} } J _{Q}$ averages Equation (9) over a minibatch: GARL amplifies the RL gradient $\hat{g} _{M}$ by the plug-in estimate $( \bar{w} _{M} ) ^{- q}$ of $P _{\theta} ^{- q}$ . At the endpoints, GARL recovers RB-REINFORCE $[ q { = } 0$ ; Zhou et al., 2026] and the IWAE gradient estimator $[ q { = } 1$ ; Burda et al., 2015]; see Section D.2.

Effective reward. The effective reward ${ w _{m} } / ( \bar{w} _{M} ) ^{q}$ has a maximum value of $M ^{q}$ , and varies along with $q$ ; we divide by $M ^{q}$ to normalize it to [0, 1] (Section D). We use the maximum effective reward across samples to monitor training dynamics (Figure 3). The $1 / M ^{q}$ factor in Algorithms 1 and 2 is an implementation choice equivalent to a $q$ -dependent learning-rate rescaling; the mathematical estimators of Equations (12) and (14) target $\nabla _{\theta} \ell _{q}$ directly without it.

# 6.1.2 Consistency and finite-sample bias

Equation (9) is a ratio estimator: it reuses the same samples in numerator and denominator, so it is biased at finite $M$ even though $\bar{w} _{M}$ and $\hat{g} _{M}$ are individually unbiased.5

Theorem 6.1. [Consistency and bias expansion] Fix a supervised example $\left( \mathbf{x} ^{*} , \mathbf{y} ^{*} \right)$ and assume:

1. $P _{\theta} > 0$   
$2 . \mathbb{E} [ \| g _{m} \| ^{2} ] < \infty .$   
3. $w _{m} \geq \epsilon a . s .$ . for some $\epsilon > 0$ .

Then for any fixed $q \in [0, 1]$ ,

$$
\widehat{\nabla_{\boldsymbol{\theta}} \ell_{q}} (q, \boldsymbol{\theta}; \mathbf{x} ^{*}, \mathbf{y} ^{*}, M) \xrightarrow [ M \rightarrow \infty ]{a . s .} \nabla_{\boldsymbol{\theta}} \ell_{q} (\boldsymbol{\theta}, q; \mathbf{x} ^{*}, \mathbf{y} ^{*}). \tag{10}
$$

Moreover, for fixed $P _{\theta} > 0$ and $q \in [0, 1]$ , the bias satisfies

$$
\mathbb{E} \left[ \widehat{\nabla_{\boldsymbol{\theta}} \ell_{q}} \right] - \nabla_{\boldsymbol{\theta}} \ell_{q} = O \left(\frac{q}{M P _{\boldsymbol{\theta}} ^{q + 1}}\right) \quad a s M \rightarrow \infty . \tag{11}
$$

At $q = 0$ the factor $q$ in the numerator makes the bias vanish exactly for all $M$ : the estimator reduces to the unbiased sample mean $\hat{g} _{M}$ (Equation (8)). The explicit leading-order coefficient is in Section D.

Proof sketch. Assumption 1 ensures continuity of $f ( a , b ) = b a ^{- q}$ at $( P _{\pmb { \theta} } , \nabla \ell _{0} )$ ; consistency then follows from the SLLN. For the bias, since $f$ is linear in $b$ , write $f ( \bar{w} _{M} , \bar{g} _{M} ) = \bar{g} _{M} \cdot h ( \bar{w} _{M} )$ where $h ( a ) = a ^{- q}$ . Expanding $h$ around $P _{\theta}$ and separating $\bar{g} _{M} = \mu _{g} + ( \bar{g} _{M} - \mu _{g} )$ yields the ${ \cal O } ( ^{1} / M )$ bias from $\mathbf{V a r} ( w _{m} )$ and $\mathbf{C o v} ( g _{m} , w _{m} )$ . The remainder is $O ( M ^{- 2} )$ : on the high-probability event $\{ \bar{w} _{M} \geq P _{\theta} / 2 \}$ (exponential concentration via $w _{m} \in [0, 1] )$ , the derivatives of the scalar function $h$ are bounded and Assumption 2 controls the higher-order terms; Assumption 3 gives $\bar{w} _{M} ^{- q} \leq \epsilon ^{- q}$ everywhere, making the complementary event’s contribution $O ( \epsilon ^{- q} e ^{- c M} )$ . □

The $O ( 1 / M )$ rate is standard for ratio estimators; the $J _{Q}$ -specific feature is the joint dependence on $q$ and $P _{\pmb { \theta} }$ . The bias grows with $q$ (vanishing at $q = 0$ ) and explodes as $P _{\pmb { \theta} }  0$ with $P _{\pmb { \theta} } ^{- ( q + 1 )}$ scaling: the same amplification that enables fast cold-start escape (Theorems 5.1 and 5.2) degrades estimator quality. This predicts intermediate $q$ outperforms both endpoints in practice — confirmed in Section 7. The expansion is a fixed- $P _{\theta}$ , large- $M$ asymptotic; in the cold-start regime where $P _{\theta}$ is small and $M$ is bounded by compute, it identifies the direction of finite-sample degradation rather than providing a uniform bound.

# 6.1.3 Variance reduction for GARL

The GARL estimator (9) decomposes into a score-function term (for the sampled z) and a pathwise term (for the fixed $\mathbf{y} ^{*}$ ); only the score-function term admits baselines. Following Kool et al. [2019], we center the score-function coefficient with a leave-one-out control variate using w¯¬m $\begin{array} { r } { \bar{w} _{\neg m} \triangleq \frac { 1 } { M - 1 } \sum _{j \neq m} w _{j} } \end{array}$ , yielding the RLOO estimator (derivation in Section D.1):

$$
\widehat{\nabla_{\boldsymbol{\theta}} \ell_{q}} ^{\mathrm{R L O O}} = \frac{1}{M} \sum_{m = 1} ^{M} \left[ - \underbrace{\left(\frac{w _{m}}{(\bar{w} _{M}) ^{q}} - (\bar{w} _{\neg m}) ^{1 - q}\right)} _{\text{centeredweight}} \cdot \nabla_{\boldsymbol{\theta}} \log p _{\boldsymbol{\theta}} \left(\mathbf{z} ^{(m)} \mid \mathbf{x} ^{*}\right) - \frac{\nabla_{\boldsymbol{\theta}} w _{m}}{(\bar{w} _{M}) ^{q}} \right]. \tag{12}
$$

Proposition 6.2 (RLOO bias preservation). Under the assumptions of Theorem 6.1, $\mathbb{E} [ \widehat { \nabla _{\pmb { \theta} } \ell _{q} } ^{\mathrm { R L O O} } ] =$ 一 $\mathbb{E} [ \widehat { \nabla _{\theta} \ell _{q} } ^{\mathrm { p l u g - i n} } ]$ , so the RLOO estimator inherits the bias of Equation (11).

Algorithm 1 summarizes the complete estimator. At $q = 0$ it recovers the Rao–Blackwellized RLOO estimator [Zhou et al., 2026]; at $q = 1$ the centered weight becomes $w _{m} / \bar{w} _{M} - 1$ , a self-normalizing baseline (details in Section D.1).

# 6.2 PAFT: Posterior-Attenuated Fine-Tuning

GARL estimates the $J _{Q}$ gradient via the RL factorization: sample rationales from the prior $p _{\pmb { \theta} } ( \mathbf{z} \mid \mathbf{x} ^{*} )$ , then amplify by $P _{\theta} ^{- q}$ — sometimes massively, especially on hard instances. The FT factorization (Equation (5)) suggests an alternative: instead of sampling from the prior and amplifying, (approximately) sample from the posterior $p _{\pmb { \theta} } ( \mathbf{z} \mid \mathbf{x} ^{*} , \mathbf{y} ^{*} )$ — where rationales already agree with the answer — and attenuate by $P _{\theta} ^{1 - q} \in [0, 1]$ .

Algorithm 1 GARL: per-example $J _{Q}$ gradient with RLOO control variate   
Require: Example $(\mathbf{x}^{*},\mathbf{y}^{*})$ , interpolation parameter $q\in [0, 1]$ , number of latent samples M 1: Sample latent trajectories $\mathbf{z}^{(1)},\ldots ,\mathbf{z}^{(M)}\sim p_{\theta}(\cdot \mid \mathbf{x}^{*})$ 2: for $m = 1,\dots ,M$ do   
3: $w_{m}\gets p_{\theta}(\mathbf{y}^{*}\mid \mathbf{x}^{*},\mathbf{z}^{(m)})$ $\triangleright$ likelihood weight   
4: $\nabla_{\pmb{\theta}}w_{m}\leftarrow \nabla_{\pmb{\theta}}p_{\pmb{\theta}}(\mathbf{y}^{*}\mid \mathbf{x}^{*},\mathbf{z}^{(m)})$ $\triangleright$ pathwise gradient of output likelihood   
5: end for   
6: $\bar{w}_M\gets \frac{1}{M}\sum_{m = 1}^M w_m$ $\triangleright$ batch mean (estimates $P_{\theta}$ )   
7: for $m = 1,\dots ,M$ do   
8: $\bar{w}_{\neg m}\gets \frac{1}{M - 1}\sum_{j\neq m}w_j$ $\triangleright$ leave-one-out mean   
9: $c_{m}\gets \frac{w_{m}}{(\bar{w}_{M})^{q}} -(\bar{w}_{\neg m})^{1 - q}$ $\triangleright$ centered weight (RLOO baseline)   
10: $\hat{g}_m\gets -c_m\nabla_\pmb{\theta}\log p_\pmb{\theta}(\mathbf{z}^{(m)}\mid \mathbf{x}^*) - \frac{\nabla_\pmb{\theta}w_m}{(\bar{w}_M)^q}$ $\triangleright$ score-function + pathwise terms   
11: end for   
12: return $\hat{g}\gets \frac{1}{M^q}\cdot \frac{1}{M}\sum_{m = 1}^M\hat{g}_m$ $\triangleright$ per-example gradient estimate, normalized by $M^q$

# 6.2.1 Posterior form of the gradient

Expanding $\nabla _{\pmb { \theta} } \ell _{1} = - \nabla _{\pmb { \theta} } \log P _{\pmb { \theta} }$ as a posterior expectation:

$$
\nabla_{\boldsymbol{\theta}} \ell_{q} = - P _{\boldsymbol{\theta}} ^{1 - q} \cdot \underset{\mathbf{z} \sim p _{\boldsymbol{\theta}} (\mathbf{z} | \mathbf{x} ^{*}, \mathbf{y} ^{*})} {\mathbb{E}} \left[ \nabla_{\boldsymbol{\theta}} \log p _{\boldsymbol{\theta}} \left(\mathbf{z}, \mathbf{y} ^{*} \mid \mathbf{x} ^{*}\right) \right]. \tag{13}
$$

Each sample gradient is standard SFT (teacher forcing) on a semantically coherent (input, rationale, answer) triple: the rationale is posterior-weighted toward agreement with $\mathbf{y} ^{*}$ .

Approximate posterior sampling. Equation (13) requires samples from the posterior $p _{\pmb { \theta} } ( \mathbf{z} \mid$ $\mathbf{x} ^{*} , \mathbf{y} ^{*} )$ , which is intractable for autoregressive models where $\mathbf{z}$ precedes y. The framework permits many approximate posterior samplers (learned proposals, MCMC, infilling models); here we use importance resampling [IR; Rubin and Rubin, 1988] because it reuses GARL’s prior sample pool and $w _{m}$ weights with minimal additional compute: resample $K$ trajectories with replacement, with probability proportional to $w _{m}$ . IR guarantees exactly $K$ resampled trajectories regardless of how small the individual $w _{m}$ values are.

The PAFT estimator. Let $\mathbf{z} ^{( 1 )} , \ldots , \mathbf{z} ^{( K )}$ denote the resampled trajectories. The PAFT gradient estimate is

$$
\hat{\nabla} _{\mathrm{P A F T}} = - \left(\bar{w} _{M}\right) ^{1 - q} \cdot \frac{1}{K} \sum_{k = 1} ^{K} \nabla_{\boldsymbol{\theta}} \log p _{\boldsymbol{\theta}} \left(\mathbf{z} ^{(k)}, \mathbf{y} ^{*} \mid \mathbf{x} ^{*}\right). \tag{14}
$$

At $q = 1$ , the instance weight vanishes $( P _{\theta} ^{1 - 1} = 1 ) $ ) and PAFT recovers the E-step of EM [Dempster et al., 1977, Phan et al., 2023]; see Section D.2 for all endpoint reductions.

# 6.2.2 Bias and variance

Conditional on the prior pool $\{ ( \mathbf{z} ^{( m )} , w _{m} ) \} _{m = 1} ^{M}$ , $( \bar{w} _{M} ) ^{1 - q}$ is deterministic and the IR average of $f _{m} = \nabla _{\pmb { \theta} } \log p _{\pmb { \theta} } ( \mathbf{z} ^{( m )} , \mathbf{y} ^{*} \mid \mathbf{x} ^{*} )$ has conditional mean $\sum _{m} ( w _{m} / \sum _{j} w _{j} ) f _{m} = - \bar{g} _{M} / \bar{w} _{M}$ (using $g _{m} = - w _{m} f _{m} )$ . Hence

$$
\mathbb{E} [ \hat{\nabla} _{\mathrm{P A F T}} | \mathrm{p o o l} ] = - (\bar{w} _{M}) ^{1 - q} \cdot \left(- \bar{g} _{M} / \bar{w} _{M}\right) = \frac{\bar{g} _{M}}{(\bar{w} _{M}) ^{q}} = \hat{\nabla} _{\mathrm{G A R L}}.
$$

Taking outer expectations gives an exact identity $\mathbb{E} [ \hat{\nabla} _{\mathrm { P A F T} } ] = \mathbb{E} [ \hat{\nabla} _{\mathrm { G A R L} } ]$ at every finite $M$ , so PAFT has the same $O ( { q } / { M P _{\theta} ^{q + 1} } )$ bias as GARL (Theorem 6.1) even though the plug-in $( \bar{w} _{M} ) ^{1 - q}$ is individually biased (Jensen). The plug-in bias is exactly canceled by the covariance between $( \bar{w} _{M} ) ^{1 - q}$ and the IR average: the Rao–Blackwellization identity fixes the total, so components cannot be analyzed in isolation. By the law of total variance, GARL has strictly lower variance than PAFT (Propositions D.3 and D.4).

Yet PAFT can produce better training dynamics. GARL’s lower variance comes from mixing bad rationales into the gradient with small weights; PAFT excludes them before the gradient is formed.

Algorithm 2 PAFT: per-example $J _{Q}$ gradient via importance resampling   
Require: Example $(\mathbf{x}^{*},\mathbf{y}^{*})$ , interpolation parameter $q\in [0, 1]$ , prior samples $M$ , resampled trajectories $K$ 1: Sample latent trajectories $\mathbf{z}^{(1)},\ldots ,\mathbf{z}^{(M)}\sim p_{\theta}(\cdot \mid \mathbf{x}^{*})$ 2: for $m = 1,\dots ,M$ do   
3: $w_{m}\gets p_{\theta}(\mathbf{y}^{*}\mid \mathbf{x}^{*},\mathbf{z}^{(m)})$ $\triangleright$ likelihood weight (same as GARL)   
4: end for   
5: $\bar{w}_M\leftarrow \frac{1}{M}\sum_{m = 1}^M w_m$ $\triangleright$ batch mean (estimates $P_{\theta}$ 6: Resample indices $r_1,\ldots ,r_K\sim$ Categorical $(w_{1} / \sum_{j}w_{j},\dots,w_{M} / \sum_{j}w_{j})$ 7: $\hat{g}\gets -\frac{(\bar{w}_M)^{1 - q}}{M^qK}\sum_{k = 1}^{K}\nabla_\theta \log p_\theta (\mathbf{z}^{(r_k)},\mathbf{y}^*\mid \mathbf{x}^*)$ attenuated SFT on coherent rationales, normalized by $M^q$ 8: return $\hat{g}$ $\triangleright$ per-example gradient estimate, normalized by $M^q$

The resampling noise is structured — preserving the semantic coherence of the FT endpoint — so PAFT is more stable at warm start despite its higher variance (Section 7). Unlike GARL’s rewardtimes-score structure, the PAFT gradient is a plain posterior expectation of the complete-data score, with no reward coefficient to center; variance reduction comes from the posterior sampling itself, which excludes bad rationales before they reach the gradient.

# 7 Empirical Validation

We validate the theoretical predictions and empirical effectiveness of GARL and PAFT on subsets of three reasoning datasets — FinQA [Chen et al., 2021], HotPotQA [Yang et al., 2018], and MuSiQue [Trivedi et al., 2022] — using post-trained Qwen 3 0.6B [Yang et al., 2025] under both cold-start and warm-start conditions.

# 7.1 Experimental setup

Warm-start scenario. Task inputs are natural-language prompts with standard task descriptions and answer-formatting instructions. The un-adapted model can occasionally produce correct answers (Section 7.3), so reward is not sparse.

Cold-start scenario. We use linearized problem inputs and outputs as $\left( \mathbf{x} ^{*} , \mathbf{y} ^{*} \right)$ pairs with no task description and no answer-formatting instructions. The model must discover both how to solve the problem and how to format the answer; initial success probability $P _{\theta}$ is very low.

Datasets. We sample subsets from the official splits of FinQA, HotPotQA, and MuSiQue. FinQA: train $n = 6 1 4 5$ , validation $n = 8 7 2$ , test $n = 1 1 3 2$ . HotPotQA: train $n = 9 0 6 7$ , validation $n = 3 4 2$ , test $n = 3 4 3$ . MuSiQue: train $n = 9 9 8 5$ , validation $n = 5 7 9$ , test $n = 4 4 5$ . Exact-match training rewards are computed against the gold answer string; evaluation uses substring match (Section 7).

Methods and compute budget. All methods — GRPO, GARL, and PAFT — use the same rollout budget of $M = 3 2$ latent trajectories per prompt during training and 16 samples per prompt at evaluation, so head-to-head comparisons are fair in compute. GARL (Algorithm 1) uses the RLOO variance reduction (Equation (12)); PAFT (Algorithm 2) importance-resamples $K = M$ trajectories from the same pool. We evaluate fixed values of $q \in \{ 0 , 0 . 2 5 , 0 . 5 , 0 . 7 5 , 1 . \bar{0} \}$ .

Rationale budget. We enforce a per-rationale token budget by forcing the model to decode the thinking-end token (</think> for our Qwen experiments) once the allocated thinking budget is exhausted [Muennighoff et al., 2025]. The budget varies by dataset: FinQA uses $4 \mathbf{k} - 1 2 8$ tokens, HotPotQA 3k − 128, and MuSiQue $2 \mathrm { k } - 1 2 8$ , where the 128-token offset reserves space for the answer.

Evaluation. Training uses exact-match rewards (Section 2). Evaluation uses relaxed substring match — $\hat{\mathbf { y} }$ is correct if $\mathbf{y} ^{*}$ appears as a substring of $\hat{\mathbf { y} }$ — so rationale tokens around the answer do not penalize the model. We report pass@1 (p@1; single-sample accuracy), pass ${ \ @ k }$ ( $\mathbf{\nabla} [ \mathsf { p } \ @ k$ ; best-of- $k$ ,

Table 1: Cold-start GARL results on FinQA. GARL with $q \leq 0 . 5$ fails entirely; only $q \geq 0 . 7 5$ escapes.   

<table><tr><td>Method</td><td>p@1</td><td>p@16</td><td>m@16</td></tr><tr><td>GRPO</td><td>0</td><td>0</td><td>0</td></tr><tr><td>q = 0 (RB-RLOO)</td><td>0</td><td>0</td><td>0</td></tr><tr><td>q = 0.25</td><td>0</td><td>0</td><td>0</td></tr><tr><td>q = 0.5</td><td>0</td><td>0</td><td>0</td></tr><tr><td>q = 0.75</td><td>30.5</td><td>61.1</td><td>38.3</td></tr><tr><td>q = 1</td><td>21.9</td><td>58.7</td><td>33.5</td></tr></table>

Table 2: Cold-start GARL (no prompts) vs. warm-start GRPO (prompted). All methods use exactmatch rewards during training. In our setting, GARL at $q { = } 0 . 7 5$ matches or exceeds GRPO on every metric across all three benchmarks (a confounded comparison: see body discussion).   

<table><tr><td>Dataset</td><td>Method</td><td>p@1</td><td>p@16</td><td>m@16</td></tr><tr><td rowspan="3">FinQA</td><td>GRPO</td><td>18.9</td><td>48.4</td><td>26.9</td></tr><tr><td>q=0.75</td><td>30.5</td><td>61.1</td><td>38.3</td></tr><tr><td>q=1</td><td>21.9</td><td>58.7</td><td>33.5</td></tr><tr><td rowspan="3">HotPotQA</td><td>GRPO</td><td>29.1</td><td>55.1</td><td>33.5</td></tr><tr><td>q=0.75</td><td>53.5</td><td>74.1</td><td>57.2</td></tr><tr><td>q=1</td><td>48.7</td><td>75.5</td><td>56.6</td></tr><tr><td rowspan="3">MuSiQue</td><td>GRPO</td><td>13.6</td><td>37.3</td><td>15.8</td></tr><tr><td>q=0.75</td><td>26.8</td><td>58.9</td><td>34.8</td></tr><tr><td>q=1</td><td>21.6</td><td>58.1</td><td>32.5</td></tr></table>

rewards coverage), and $\mathtt { m a j @ k }$ $\left( \mathtt { m } \ @ k \right.$ ; majority vote over $k$ samples [Wang et al., 2023], rewards diverse correct trajectories). Reported test numbers are taken from the checkpoint with highest validation $\mathtt { m a j @ 1 6 }$ . 6

# 7.2 Cold-start results: the escape-time separation

Cold start tests whether commitment speed, controlled by $P _{\theta} ^{- q}$ , determines escape from a sparsereward regime (Theorem 5.2).

Cold-start escape requires large $q$ . GRPO, Rao–Blackwellized RLOO $( q = 0$ ), and all $q \leq 0 . 5$ fail entirely — zero accuracy across all metrics. Rao–Blackwellization replaces the binary reward $\mathbb{I} ( \hat{\mathbf { y} } = \mathbf{y} ^{*} )$ with its conditional expectation $w _{m} = p \pmb { \theta } ( \mathbf{y} ^{*} \mid \mathbf{x} ^{*} , \mathbf{z} ^{( m )} )$ [Zhou et al., 2026], reducing variance but not helping escape: the underlying gradient remains $\nabla _{\pmb { \theta} } \ell _{0} = - \nabla _{\pmb { \theta} } P _{\pmb { \theta} }$ with dynamics ${ \dot{p} } = p ^{2} \| s \| ^{2}$ and no amplification $P _{\theta} ^{- q} = 1$ at $q = 0$ ; Figure 3). These results suggest that in our setting the cold-start bottleneck is primarily gradient amplification rather than gradient variance. The sharp transition at $q = 0 . 7 5$ matches Theorem 5.1: the lower bound $\Omega ( p _{0} ^{- ( 1 - q )} )$ grows rapidly as $q$ decreases, so for a fixed training budget there is a critical $q$ below which escape fails.

The density-estimation pole escapes but overshoots. $q = 1$ successfully escapes cold start on all three benchmarks (Table 2), confirming Theorem 5.2. However, $q = 0 . 7 5$ achieves higher pass@1 and $\mathtt { m a j @ 1 6 }$ on every benchmark. The pass@16 picture is more nuanced: $q = 1$ achieves higher pass@16 than $q = 0 . 7 5$ on HotPotQA (75.5 vs. 74.1), consistent with its stronger mode-covering behavior producing more diverse reasoning paths. But this diversity does not translate to higher $\mathtt { m a j @ 1 6 }$ , because the trajectories are trained with noisier gradients. This is exactly the escape-vs-bias tradeoff predicted by Theorem 6.1: $q = 1$ ’s stronger amplification enables faster escape but produces noisier gradient estimates, while $q = 0 . 7 5$ strikes a better balance.

Cold-start GARL is competitive with prompted GRPO. Table 2 compares cold-start GARL at $q \in \{ 0 . 7 5 , 1 \}$ (no task-specific prompts) against warm-start GRPO (with prompts) across all three benchmarks; all methods use exact-match training rewards. In our setting, GARL at $q = 0 . 7 5$ matches

Figure 3: Cold-start training dynamics on FinQA: maximum amplified advantage $c _{m} / M ^{q}$ vs. training step, where $c _{m} = w _{m} / ( \bar{w} _{M} ) ^{\bar{q} } - ( \bar{w} _{\lnot m} ) ^{1 - q}$ is the centered weight from Equation (12) (normalized to $[0, 1]$ by dividing by $M ^{q}$ ; cf. effective-reward bound in Section D). $q = 1$ escapes immediately, $q = 0 . 7 5$ escapes sharply around step 35, and $q \leq 0 . 5$ remain flat — qualitatively consistent with the predicted ordering $( \Theta ( \log ( 1 / p _{0} ) )$ at $q = 1$ , $\Theta ( p _{0} ^{- ( 1 - q )} )$ for $q < 1$ , with $\Omega ( p _{0} ^{- ( 1 - q )} )$ exceeding the training budget at small $q$ ). We do not claim measured slopes validate the asymptotic rates. Despite its fast escape, $q = 1$ achieves lower test accuracy than $q = 0 . 7 5$ (Table 1), consistent with the $O ( { q } / { M P _{\theta} ^{q + 1} } )$ ratio-estimator bias of Theorem 6.1 degrading gradient quality.

or exceeds prompted GRPO on every metric across all three benchmarks $( + 1 1 . 6 ~ \mathsf { p } \ @ 1 $ on FinQA, $+ 2 4 . 4$ on HotPotQA, $+ 1 3 . 2$ on MuSiQue), and GARL at $q = 1$ exceeds GRPO on coverage metrics $( \mathtt { p } \ @ 1 6 , \mathtt { m } \ @ 1 6 )$ while underperforming on $\mathtt { p @ 1 }$ . We treat this as a hypothesis-generating observation rather than evidence that prompts are unnecessary: cold- and warm-start runs differ in more than prompts (input formatting, output constraints, target distribution), and isolating the prompt factor requires a controlled ablation we leave to future work.

# 7.3 Warm-start results across three benchmarks

Warm start tests whether GARL and PAFT still help when $P _{\theta}$ is not negligible and standard RL already makes progress. Table 3 reports warm-start maj@16 across all three benchmarks.

Cold-start without instructions beats warm-start with them. The base model with task-specific prompts but no training performs weakly $( 1 2 . 6 / 2 2 . 2 / 8 . 9 \mathrm { \ m a j } \mathbb{\otimes} 1 6 $ ; first row of Table 3), confirming that these tasks require adaptation. Every trained method in Tables 2 and 3 improves over this base. More striking: cold-start GARL at $q = 0 . 7 5$ without any task-specific prompts matches or beats

Table 3: Warm-start $\mathtt { m a j @ 1 6 }$ across three benchmarks (exact-match training rewards; evaluation uses substring match). Base $=$ un-adapted Qwen 3 0.6B evaluated with the same prompted inputs as the trained methods. GARL at $q = 0$ recovers RB-RLOO [Zhou et al., 2026]. GARL entries for MuSiQue and HotPotQA are peak-before-collapse (validation accuracy collapses to zero before end of training; see Section 7.3); only FinQA GARL and all PAFT entries are steady-state. Best steady-state result per benchmark in bold: GARL at $q { = } 0 . 2 5$ on FinQA, PAFT at $q { = } 0 . 7 5$ on HotPotQA and MuSiQue. The best stable method beats GRPO by $+ 6 . 6$ to $+ 1 4 . 4$ points.   

<table><tr><td>Method</td><td>FinQA</td><td>HotPotQA</td><td>MuSiQue</td></tr><tr><td>Base (no training, prompted)</td><td>12.6</td><td>22.2</td><td>8.9</td></tr><tr><td>GRPO</td><td>26.9</td><td>33.5</td><td>15.8</td></tr><tr><td>GARL (q = 0, RB-RLOO)</td><td>38.3</td><td>21.6</td><td>9.1</td></tr><tr><td>GARL (q = 0.25)</td><td>38.7</td><td>22.9</td><td>24.3</td></tr><tr><td>GARL (q = 0.75)</td><td>37.6</td><td>46.8</td><td>19.7</td></tr><tr><td>PAFT (q = 0.25)</td><td>26.6</td><td>47.0</td><td>9.0</td></tr><tr><td>PAFT (q = 0.75)</td><td>28.6</td><td>47.9</td><td>22.4</td></tr></table>

the best stable warm-start maj@16 on every benchmark — FinQA 38.3 vs. 38.7 (tie with warm-start GARL at $q = 0 . 2 5 )$ ), HotPotQA 57.2 vs. 47.9 $\left( + 9 . 3 \right)$ , MuSiQue 34.8 vs. 22.4 $\left( + 1 2 . 4 \right)$ .

The swing from base-with-prompts to cold-start GARL is $+ 2 5 . 7$ to $+ 3 5 . 0$ points with no prompt engineering whatsoever. Instructions and answer-formatting supervision are not merely unnecessary under strong commitment; one interpretation is that the added prompt structure may constrain the learned policy toward narrower reasoning patterns. A controlled ablation isolating the prompt factor from other cold-start/warm-start differences is left to future work. With high- $q$ amplification, the model discovers task structure directly from input-output pairs.

Rao–Blackwellized rewards alone are insufficient. GARL at $q ~ = ~ 0$ recovers the Rao– Blackwellized REINFORCE estimator of Zhou et al. [2026] with leave-one-out baseline (RB-RLOO). It beats GRPO on FinQA $( + 1 1 . 4 ~ \mathrm { m } \mathbb{Q} 1 6 )$ ) but underperforms on HotPotQA (−11.9) and MuSiQue $( - 6 . 7 )$ : replacing the binary reward with $w _{m} = \bar{p _{\pmb \theta} } ( \mathbf{y} ^{*} \mid \mathbf{x} ^{*} , \mathbf{z} )$ does not generalize across warmstart tasks. Raising $q$ lifts peak accuracy on the unstable benchmarks (GARL $q = 0 . 7 5$ : HotPotQA $2 1 . 6  4 6 . 8$ peak; MuSiQue $9 . 1  1 9 . 7$ peak; FinQA is roughly flat across $q \in [ 0 , 0 . 7 5 ] ,$ ), but peaks do not survive training on HotPotQA or MuSiQue (next paragraphs).

Low $q$ wins on FinQA. On FinQA, GARL is stable throughout training at all tested $q$ , so the cost of high $q$ — estimator bias $O ( { q } / { M P _{\theta} ^{q + 1} } )$ (Theorem 6.1) and noise memorization (Proposition C.2), both driven by $P _{\theta} ^{- q}$ — outweighs its amplification benefit, and lower-bias estimators extract more signal per step. GARL at $q = 0 . 2 5$ posts the best FinQA maj@16 (38.7, $+ 1 1 . 8$ over GRPO). On MuSiQue and HotPotQA, GARL’s warm-start training collapses (next paragraphs), so this low- $q$ advantage cannot be realized without training-dynamics instability.

GARL destabilizes on HotPotQA; PAFT is stable. GARL destabilizes on HotPotQA warm-start at every tested $q$ : validation accuracy peaks early and collapses to zero before the end of training $( q = 0 . 2$ : peak 41.1 at step 100, zero by step 150; $q = 0 . 2 5$ : peak 22.9 at step 50, zero by step 100; $q = 0 . 7 5$ : peak 46.8 at step 50, zero by step 100). HotPotQA exhibits broader instability — GRPO also degrades, peaking at ${ \sim } 3 7 . 4 $ around step 100 and declining steadily to ${ \sim } 5 . 0$ by end of training — but GARL’s collapse is qualitatively different: a sharp drop to literal zero rather than a gradual decline. PAFT shows neither pattern, reaching $\mathbf{4 7 . 9 \ m a j} \ @ 1 6$ $+ 1 4 . 4$ over GRPO) and remaining stable. Figure 4 compares GARL and PAFT validation curves at matched $q = 0 . 2 5$ . We do not have a verified mechanism for the GARL-specific zero-collapse: candidate explanations include pathwise-term corruption (the GARL gradient updates $p _{\pmb { \theta} } ( \mathbf{y} ^{*} \mid \mathbf{x} ^{*} , \mathbf{z} )$ on every sampled $\mathbf{z}$ , including incoherent ones, while PAFT only updates on resampled coherent rationales) and HotPotQA-specific overfitting (also visible in GRPO), and disentangling them would require a pathwise-zeroed ablation and additional diagnostics. The practical implication holds regardless: PAFT is the stable choice on benchmarks where GARL collapses.

Figure 4: Warm-start validation $\mathtt { m a j @ 1 6 }$ on HotPotQA at $q = 0 . 2 5$ : GARL peaks at step 50 (30.6) and collapses to zero by step 100; PAFT remains stable throughout training and reaches 53.6. At fixed $q$ , the contrast isolates the estimator (prior-sampled, all- $M$ vs. posterior-resampled).

PAFT at low $q$ is slow, not collapsed. PAFT at $q = 0 . 2 5$ underperforms on MuSiQue (9.0 vs. 15.8), but validation accuracy is still rising at the end of training rather than dropping: the attenuation factor $P _{\theta} ^{1 - q} = P _{\theta} ^{0 . 7 5}$ heavily down-weights hard instances, so learning is slow but not unstable. This differsom GARL’s warm-start collapse on HotPotQA and MuSiQue (validation drops to zero). The GARL-vs-PAFT trade-off is therefore speed vs. stability: PAFT gives up gradient signal per step but avoids the destabilization observed in GARL on HotPotQA and MuSiQue. Raising $q$ to 0.75 recovers speed for PAFT without compromising stability, delivering best-overall HotPotQA (47.9) and the honest MuSiQue recommendation (22.4 steady-state vs. GARL’s 24.3 peak-before-collapse).

# 7.4 Discussion

GARL and PAFT trade speed against stability. Across regimes: cold start requires GARL’s amplification (PAFT is undefined when $P _{\pmb { \theta} } \approx 0$ ); warm start admits both. Within warm start: GARL delivers higher per-step signal but destabilizes during training on HotPotQA and MuSiQue (collapse to zero), where HotPotQA also exhibits broader instability visible in GRPO’s gradual decline. PAFT does not collapse on any benchmark tested, at the cost of lower per-step signal $P _{\theta} ^{1 - q}$ attenuation plus posterior-resampling variance). On these benchmarks, the practical decision is stable-vs-not rather than high- $q$ -vs-low- $q$ : use GARL at low $q$ where it is stable (FinQA); use PAFT at $q \geq 0 . 7 5$ where GARL collapses (HotPotQA, MuSiQue). The mechanism behind GARL’s zero-collapse is unverified; pathwise-term corruption and dataset-specific overfitting are both candidates that future ablations could disentangle.

Practical recommendation: GARL at large $q$ for cold-start escape; in warm start, use GARL at low $q$ if training is stable (FinQA), and PAFT at $q \geq 0 . 7 5$ otherwise (HotPotQA, MuSiQue). PAFT also acts as an automatic curriculum: early on, only the easiest rationales pass the importance resampling

filter; as $P _{\theta}$ grows, more rationales become coherent enough to be selected, broadening the training distribution without an explicit schedule.

# 8 Related Work

$q$ -logarithmic losses. The Tsallis $q$ -logarithm originates in non-extensive statistical mechanics [Tsallis, 1988]. Ferrari and Yang [2010] introduced the maximum $L _{q}$ -likelihood estimator (MLqE), which replaces log with $\log _{q}$ in the log-likelihood and is equivalent to reweighting the score by $f ( X ; \theta ) ^{1 - q}$ . For sample-size-dependent $q _{n} \to 1$ , MLqE is asymptotically normal around $\theta _{0}$ ; for fixed $q < 1$ , finite-sample MSE can fall below MLE’s at the cost of bias toward a surrogate parameter $\theta _{0} / q$ . The PAFT gradient Equation (13) is the marginal-likelihood analog of this weighted score. Extending the $q$ -log to deep classification, Zhang and Sabuncu [2018] proposed generalized cross-entropy for noisy labels (the same loss family under a different parameterization), observing that bounded loss at $q < 1$ prevents gradient domination by mislabeled samples. Our escort minimizer analysis (Theorem 3.1) gives a precise mechanism: the tempering $\tilde{\alpha} _{j} ^{{ 1 / q} }$ concentrates the minimizer on the clean mode. Concurrently, Wang et al. [2026] apply the deformed-log family at the token level for SFT, deriving a gate-times-error gradient structure; their token-level gate $p ^{\alpha}$ is the single-token specialization of our example-level $P _{\theta} ^{- q}$ , but their $p$ is an exact softmax probability whereas our $P _{\pmb { \theta} }$ is an intractable marginal over latent trajectories.

Training-time exploration-exploitation. Tsallis entropy has been used as a policy regularizer in RL [Lee et al., 2018, Nachum et al., 2018], providing inference-time exploration through sparse action distributions. Our use of the Tsallis $q$ -logarithm in the loss function provides a different kind of control: training-time exploration-exploitation. The escort minimizer $\theta _{j} ^{*} \propto \alpha _{j} ^{1 / q}$ (Theorem 3.1) is a training-time analog of inference temperature that permanently shapes what the model learns, and the $P _{\theta} ^{- q}$ factor automatically explores more on instances the model finds surprising — a per-instance effect not achievable by tuning the learning rate or inference temperature alone.

Information-theoretic context. Escort distributions were studied by Beck and Schögl [1993]. Rényi variational inference [Li and Turner, 2016] provides a complementary continuum that tightens the ELBO toward exact log-marginal-likelihood; our $J _{Q}$ family approaches the same target from the exploitation side, with $- \log P _{\theta}$ as their shared meeting point. The RL-as-inference connection [Levine, 2018, Norouzi et al., 2016, Guu et al., 2017] views MLE and RL as distinct frameworks; our contribution is embedding them as endpoints of a single continuously parameterized family.

Latent-variable training for reasoning. On the RL side, RLVR and GRPO [DeepSeek-AI, 2025, Shao et al., 2024] optimize expected reward with policy gradients. On the latent-variable side, STaR [Zelikman et al., 2022] bootstraps reasoning by generating and filtering rationales, while TRICE [Phan et al., 2023] maximizes marginal log-likelihood via MCMC-EM. Our framework subsumes these as endpoints: RLVR corresponds to $q = 0$ and marginal log-likelihood training to $q = 1$ . PAFT at $q = 1$ recovers the EM E-step underlying TRICE, and STaR’s rejection-sampling strategy can be viewed as a hard-acceptance variant of PAFT’s importance resampling (Section D.2).

Concurrent RL-to-ML interpolations. MaxRL [Tajwar et al., 2026] defines another RL-to-ML continuum by truncating the Maclaurin expansion of $\log p$ at order $T$ . Their estimator is unbiased for the truncated objective $J ^{( T )}$ (itself a biased approximation of $\log { P _{\theta} } .$ ), while GARL targets the true $q$ -loss with $O ( 1 / M )$ estimator bias (Theorem 6.1). A key distinction is cold-start behavior: the MaxRL estimator is exactly zero when no sample succeeds $( K { = } 0 )$ ), while GARL always has nonzero gradient since $w _{m} > 0$ . MaxRL and PAFT share the principle of training on successful trajectories; in the limit $T \to \infty$ and $q = 1$ , both average posterior-sampled gradients, differing only in hard (MaxRL) vs. soft (PAFT) acceptance.

Gradient estimators for marginal likelihoods. The IWAE estimator [Burda et al., 2015] that GARL recovers at $q { = } 1$ has a well-known failure mode: Rainforth et al. [2018] showed that as $M$ grows, the signal-to-noise ratio of the inference-network gradient shrinks, motivating doubly reparameterized variants [Roeder et al., 2017, Tucker et al., 2019]. Our bias expansion $O ( { q } / { M P _{\theta} ^{q + 1} } )$ exposes a related phenomenon along the $J _{Q}$ continuum: the same amplification that enables cold-start

escape degrades estimator quality, and intermediate $q$ balances the two — a prediction confirmed in Section 7.

Rao–Blackwellization and verifier-free training. Zhou et al. [2026] propose VeriFree, which uses $p _{\pmb { \theta} } ( \mathbf{y} ^{*} \ \mid \ \mathbf{x} ^{*} , \mathbf{z} )$ directly as the reward signal. This is the RB-REINFORCE estimator that GARL recovers at $q = 0$ (Section 6.1). While Rao–Blackwellization reduces gradient variance, our experimental results in Section 7 show it does not address the cold-start escape bottleneck: the gradient remains $\nabla _{\pmb { \theta} } \ell _{0} = - \nabla _{\pmb { \theta} } P _{\pmb { \theta} }$ regardless of Rao–Blackwellization, and the dynamics ${ \dot{p} } = p ^{2} \| s \| ^{2}$ receive no amplification at $q = 0$ (Figure 3). Both GARL and PAFT are verifier-free throughout the $J _{Q}$ continuum.

RLVR capability boundaries and reward hacking. Yue et al. [2025] showed that RLVR improves sampling efficiency but rarely elicits new reasoning patterns, and the capability boundary narrows during training. Our framework gives a direct mechanism: this narrowing is the mode-seeking behavior predicted by the escort distribution at $q = 0$ (Corollary B.2). Related, sustained GRPO training with exact-match rewards often collapses via reward hacking, where models exploit verifier formatting rather than reasoning. The $J _{Q}$ continuum exposes $q$ as a principled control for mode concentration, and PAFT as an empirically more stable alternative to GARL during warm-start training (Section 7).

# 9 Conclusion and Future Work

We introduced a Tsallis loss continuum $J _{Q}$ that unifies RLVR-style exploitation and marginallikelihood training via a single parameter $q$ controlling commitment to unfamiliar supervision. The per-instance amplification $P _{\theta} ^{- q}$ is the mechanism that addresses the cold-start stalling problem: GARL at large $q$ escapes cold start where GRPO fails, and the $\Omega ( 1 / _{p _ { 0} } )$ lower bound for RLVR-style training is bypassed by moving $q$ away from the exploitation pole. The gradient admits a dual factorization through the RL and FT endpoints (Proposition 4.1), yielding two complementary estimators: GARL (prior-sampling amplification) and PAFT (posterior-sampling attenuation). High commitment $( q \to 1 )$ ) resolves ambiguity but memorizes noise; low commitment $( q \to 0$ ) resolves noise but cannot escape cold start. Within warm start, GARL destabilizes on HotPotQA and MuSiQue while PAFT remains stable across all benchmarks tested.

Limitations and future work. Experiments in this work use a single model scale (Qwen 3 0.6B), three benchmarks, and fixed values of $q$ . The cold-start escape theorems and bias expansion are scale-agnostic, but the GARL collapse / PAFT stability finding has been verified only at this scale; replication at bigger model scales is important. Our convergence analysis is stylized: single-example, gradient flow, bounded score (Theorems 5.1 and 5.2). Our framework assumes exact-match supervision (Section 2); extension to general rewards is open.

# References

Christian Beck and Friedrich Schögl. Thermodynamics of Chaotic Systems: An Introduction. Cambridge Nonlinear Science Series. Cambridge University Press, 1993.   
Yuri Burda, Roger Baker Grosse, and Ruslan Salakhutdinov. Importance weighted autoencoders. volume abs/1509.00519, 2015. URL https://api.semanticscholar.org/CorpusID: 11383178.   
Zhiyu Chen, Wenhu Chen, Charese Smiley, Sameena Shah, Iana Borova, Dylan Langdon, Reema Moussa, Matt Beane, Ting-Hao Huang, Bryan Routledge, and William Yang Wang. FinQA: A dataset of numerical reasoning over financial data. In Marie-Francine Moens, Xuanjing Huang, Lucia Specia, and Scott Wen-tau Yih, editors, Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pages 3697–3711, Online and Punta Cana, Dominican Republic, November 2021. Association for Computational Linguistics. doi: 10.18653/v1/2021. emnlp-main.300. URL https://aclanthology.org/2021.emnlp-main.300/.

Tianzhe Chu, Yuexiang Zhai, Jihan Yang, Shengbang Tong, Saining Xie, Dale Schuurmans, Quoc V Le, Sergey Levine, and Yi Ma. SFT memorizes, RL generalizes: A comparative study of foundation model post-training. 2025. URL https://openreview.net/forum?id=dYur3yabMj.   
DeepSeek-AI. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. 2025. URL https://arxiv.org/abs/2501.12948.   
AP Dempster, NM Laird, and DB Rubin. Maximum likelihood from incomplete data via the EM algorithm. Journal of the Royal Statistical Society. Series B (Methodological), pages 1–38, 1977.   
Davide Ferrari and Yuhong Yang. Maximum $L _{q}$ -likelihood estimation. The Annals of Statistics, 38 (2):753–783, 2010.   
Kelvin Guu, Panupong Pasupat, Evan Liu, and Percy Liang. From language to programs: Bridging reinforcement learning and maximum marginal likelihood. In Regina Barzilay and Min-Yen Kan, editors, Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1051–1062, Vancouver, Canada, July 2017. Association for Computational Linguistics. doi: 10.18653/v1/P17-1097. URL https://aclanthology.org/ P17-1097/.   
Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization. volume abs/1412.6980, 2014. URL https://api.semanticscholar.org/CorpusID:6628106.   
Wouter Kool, Herke van Hoof, and Max Welling. Buy 4 REINFORCE samples, get a baseline for free! 2019. URL https://openreview.net/forum?id=r1lgTGL5DE.   
Kyungjae Lee, Sungjoon Choi, and Songhwai Oh. Sparse markov decision processes with causal sparse tsallis entropy regularization for reinforcement learning. IEEE Robotics and Automation Letters, 3(3):1466–1473, 2018. doi: 10.1109/LRA.2018.2800085.   
Sergey Levine. Reinforcement learning and control as probabilistic inference: Tutorial and review. ArXiv, abs/1805.00909, 2018. URL https://api.semanticscholar.org/CorpusID: 19077536.   
Yingzhen Li and Richard E Turner. Rényi divergence variational inference. In D. Lee, M. Sugiyama, U. Luxburg, I. Guyon, and R. Garnett, editors, Advances in Neural Information Processing Systems, volume 29. Curran Associates, Inc., 2016. URL https://proceedings.neurips.cc/paper_ files/paper/2016/file/7750ca3559e5b8e1f44210283368fc16-Paper.pdf.   
Chu-Cheng Lin, Aaron Jaech, Xin Li, Matthew R. Gormley, and Jason Eisner. Limitations of autoregressive models and their alternatives. In Kristina Toutanova, Anna Rumshisky, Luke Zettlemoyer, Dilek Hakkani-Tur, Iz Beltagy, Steven Bethard, Ryan Cotterell, Tanmoy Chakraborty, and Yichao Zhou, editors, Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 5147–5173, Online, June 2021. Association for Computational Linguistics. doi: 10.18653/v1/2021.naacl-main. 405. URL https://aclanthology.org/2021.naacl-main.405/.   
William Merrill and Ashish Sabharwal. The expressive power of transformers with chain of thought. In The Twelfth International Conference on Learning Representations, 2024. URL https:// openreview.net/forum?id=NjNGlPh8Wh.   
Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi, Luke Zettlemoyer, Percy Liang, Emmanuel Candès, and Tatsunori Hashimoto. s1: Simple test-time scaling, 2025. URL https://arxiv.org/abs/2501.19393.   
Ofir Nachum, Yinlam Chow, and Mohammad Ghavamzadeh. Path consistency learning in tsallis entropy regularized mdps. ArXiv, abs/1802.03501, 2018. URL https://api.semanticscholar. org/CorpusID:3653343.   
Mohammad Norouzi, Samy Bengio, Zhifeng Chen, Navdeep Jaitly, Mike Schuster, Yonghui Wu, and Dale Schuurmans. Reward augmented maximum likelihood for neural structured prediction. In Proceedings of the 30th International Conference on Neural Information Processing Systems, NIPS’16, page 1731–1739, Red Hook, NY, USA, 2016. Curran Associates Inc. ISBN 9781510838819.

Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke E. Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Francis Christiano, Jan Leike, and Ryan J. Lowe. Training language models to follow instructions with human feedback. ArXiv, abs/2203.02155, 2022. URL https://api.semanticscholar.org/CorpusID:246426909.   
Du Phan, Matthew D. Hoffman, David Dohan, Sholto Douglas, Tuan Anh Le, Aaron Parisi, Pavel Sountsov, Charles Sutton, Sharad Vikram, and Rif A. Saurous. Training chain-of-thought via latentvariable inference. In Proceedings of the 37th International Conference on Neural Information Processing Systems, NIPS ’23, Red Hook, NY, USA, 2023. Curran Associates Inc.   
Tom Rainforth, Adam R. Kosiorek, Tuan Anh Le, Chris J. Maddison, Maximilian Igl, Frank Wood, and Yee Whye Teh. Tighter variational bounds are not necessarily better. In International Conference on Machine Learning (ICML), pages 4277–4285, 2018.   
Geoffrey Roeder, Yuhuai Wu, and David K. Duvenaud. Sticking the landing: Simple, lower-variance gradient estimators for variational inference. In Advances in Neural Information Processing Systems (NeurIPS), 2017.   
Db Rubin and Db Rubin. Using the sir algorithm to simulate posterior distributions. 1988. URL https://api.semanticscholar.org/CorpusID:115305396.   
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, Y.K. Li, Y. Wu, and Daya Guo. DeepSeekMath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.   
Weijie Su, Stephen Boyd, and Emmanuel J. Candès. A differential equation for modeling nesterov’s accelerated gradient method: theory and insights. J. Mach. Learn. Res., 17(1):5312–5354, January 2016. ISSN 1532-4435.   
Fahim Tajwar, Guanning Zeng, Yueer Zhou, Yuda Song, Daman Arora, Yiding Jiang, Jeff Schneider, Ruslan Salakhutdinov, Haiwen Feng, and Andrea Zanette. Maximum likelihood reinforcement learning. 2026. URL https://arxiv.org/abs/2602.02710.   
Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. MuSiQue: Multihop questions via single-hop question composition. Transactions of the Association for Computational Linguistics, 2022.   
Constantino Tsallis. Possible generalization of boltzmann-gibbs statistics. Journal of Statistical Physics, 52:479–487, 1988. URL https://api.semanticscholar.org/CorpusID: 16385640.   
George Tucker, Dieterich Lawson, Shixiang Gu, and Chris J. Maddison. Doubly reparameterized gradient estimators for Monte Carlo objectives. In International Conference on Learning Representations (ICLR), 2019.   
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. In The Eleventh International Conference on Learning Representations, 2023. URL https://openreview.net/forum?id $\equiv$ 1PL1NIMMrw.   
Zecheng Wang, Deyuan Liu, Chunshan Li, Yupeng Zhang, Zhengyun Zhao, Dianhui Chu, Bingning Wang, and Dianbo Sui. Gradients must earn their influence: Unifying sft with generalized entropic objectives, 2026. URL https://arxiv.org/abs/2602.11424.   
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In Proceedings of the 36th International Conference on Neural Information Processing Systems, NIPS ’22, Red Hook, NY, USA, 2022. Curran Associates Inc. ISBN 9781713871088.   
Ronald J. Williams. Simple statistical gradient-following algorithms for connectionist reinforcement learning. Mach. Learn., 8(3–4):229–256, May 1992. ISSN 0885-6125. doi: 10.1007/BF00992696. URL https://doi.org/10.1007/BF00992696.

An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao Ge, Haoran Wei, Huan Lin, Jialong Tang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jing Zhou, Jingren Zhou, Junyang Lin, Kai Dang, Keqin Bao, Kexin Yang, Le Yu, Lianghao Deng, Mei Li, Mingfeng Xue, Mingze Li, Pei Zhang, Peng Wang, Qin Zhu, Rui Men, Ruize Gao, Shixuan Liu, Shuang Luo, Tianhao Li, Tianyi Tang, Wenbiao Yin, Xingzhang Ren, Xinyu Wang, Xinyu Zhang, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yinger Zhang, Yu Wan, Yuqiong Liu, Zekun Wang, Zeyu Cui, Zhenru Zhang, Zhipeng Zhou, and Zihan Qiu. Qwen3 technical report, 2025. URL https://arxiv.org/abs/2505.09388.   
Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. HotpotQA: A dataset for diverse, explainable multi-hop question answering. In Conference on Empirical Methods in Natural Language Processing (EMNLP), 2018.   
Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Yang Yue, Shiji Song, and Gao Huang. Does reinforcement learning really incentivize reasoning capacity in LLMs beyond the base model? In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025. URL https://openreview.net/forum?id=4OsgYD7em5.   
Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D. Goodman. Star: self-taught reasoner bootstrapping reasoning with reasoning. In Proceedings of the 36th International Conference on Neural Information Processing Systems, NIPS ’22, Red Hook, NY, USA, 2022. Curran Associates Inc. ISBN 9781713871088.   
Zhilu Zhang and Mert R. Sabuncu. Generalized cross entropy loss for training deep neural networks with noisy labels. In Proceedings of the 32nd International Conference on Neural Information Processing Systems, NIPS’18, page 8792–8802, Red Hook, NY, USA, 2018. Curran Associates Inc.   
Xiangxin Zhou, Zichen Liu, Anya Sims, Haonan Wang, Tianyu Pang, Chongxuan Li, Liang Wang, Min Lin, and Chao Du. Reinforcing general reasoning without verifiers. In The Fourteenth International Conference on Learning Representations, 2026. URL https://openreview.net/ forum?id=nnwvwge40d.

# A Proofs for Section 2: Setup and Background

Proposition A.1 (RLVR connection). Under the conditional model of Section 2 and exact-match reward $R ( \hat{\mathbf { y} } , \mathbf{y} ^{*} ) = \mathbb{I} ( \hat{\mathbf { y} } = \mathbf{y} ^{*} )$ , the expected reward equals $\mathbb{E} _{\boldsymbol { D} } [ P _{\boldsymbol { \theta} } ]$ ; consequently $J _{0} ( \pmb { \theta } ) = 1 -$ $\mathbb{E} _{\mathcal{D} } [ P _{\theta} ]$ , and minimizing $J _{0}$ is equivalent to maximizing expected reward.

Proof. For a fixed example $\left( \mathbf{x} ^{*} , \mathbf{y} ^{*} \right)$

$$
\begin{array}{l} \mathop{\mathbb{E}}_{\substack{\mathbf{z}\sim p_{\boldsymbol{\theta}}(\cdot |\mathbf{x}^{*}),\\ \hat{\mathbf{y}}\sim p_{\boldsymbol{\theta}}(\cdot |\mathbf{x}^{*},\mathbf{z})}}[R(\hat{\mathbf{y}},\mathbf{y}^{*})] \\ = \sum_{\substack{\mathbf{z}\in \mathcal{Z},\\ \mathbf{y}\in \mathcal{Y}}}\left[p_{\boldsymbol{\theta}}(\mathbf{z}  |  \mathbf{x}^{*})\right. \\ \left. \cdot p _{\boldsymbol{\theta}} (\mathbf{y} \mid \mathbf{x} ^{*}, \mathbf{z}) \mathbb{I} (\mathbf{y} = \mathbf{y} ^{*}) \right]. \\ \end{array}
$$

The indicator picks out the correct output, giving

$$
\begin{array}{l} \underset{ \begin{array}{c} \mathbf{z} \sim p _{\boldsymbol{\theta}} (\cdot | \mathbf{x} ^{*}), \\ \hat{\mathbf{y}} \sim p _{\boldsymbol{\theta}} (\cdot | \mathbf{x} ^{*}, \mathbf{z}) \end{array}} {\mathbb{E}} [ R (\hat{\mathbf{y}}, \mathbf{y} ^{*}) ] = \sum_{\mathbf{z} \in \mathcal{Z}} p _{\boldsymbol{\theta}} (\mathbf{z} \mid \mathbf{x} ^{*}) p _{\boldsymbol{\theta}} (\mathbf{y} ^{*} \mid \mathbf{x} ^{*}, \mathbf{z}) \\ = P _{\theta}. \\ \end{array}
$$

Taking an expectation over training examples from $\mathcal{D}$ , we have

$$
\underset{ \begin{array}{c} (\mathbf{x} ^{*}, \mathbf{y} ^{*}) \sim \mathcal{D} \\ \mathbf{z} \sim p _{\boldsymbol{\theta}} (\cdot | \mathbf{x} ^{*}), \\ \hat{\mathbf{y}} \sim p _{\boldsymbol{\theta}} (\cdot | \mathbf{x} ^{*}, \mathbf{z}) \end{array}} {\mathbb{E}} [ R (\hat{\mathbf{y}}, \mathbf{y} ^{*}) ] = \underset{ \begin{array}{c} (\mathbf{x} ^{*}, \mathbf{y} ^{*}) \sim \mathcal{D} \\ \mathbf{z} \sim p _{\boldsymbol{\theta}} (\cdot | \mathbf{x} ^{*}, \mathbf{z}) \end{array}} {\mathbb{E}} [ P _{\boldsymbol{\theta}} ].
$$

# B Proofs for Section 3: Loss Landscape

Proposition B.1 (Dispersion penalty). For $q > 0$ , $J _{Q} ( \theta , q ) \geq - \log _{q} ( \bar{P} )$ , with equality if and only if $P _{\pmb { \theta} }$ is constant across all examples in $\mathcal{D}$ .

Proof. For $q > 0$ , the function $\begin{array} { r } { h _{q} ( u ) = - \log _{q} ( u ) = \frac { 1 - u ^{1 - q} } { 1 - q } } \end{array}$ is strictly convex on $( 0 , 1 ]$ , since $h _{q} ^{\prime \prime} ( u ) = q u ^{- q - 1} > 0 .$ . Applying Jensen’s inequality:

$$
\begin{array}{l} J _{Q} (\boldsymbol{\theta}, q) = \underset{(\mathbf{x} ^{*}, \mathbf{y} ^{*}) \sim \mathcal{D}} {\mathbb{E}} \left[ h _{q} (P _{\boldsymbol{\theta}}) \right] \\ \geq h_{q}\Bigl(\underset{(\mathbf{x}^{*},\mathbf{y}^{*})\sim \mathcal{D}}{\mathbb{E}}[P_{\boldsymbol{\theta}}]\Bigr) = -\log_{q}(\bar{P}), \\ \end{array}
$$

with equality iff $P _{\theta}$ is constant across all examples.

Theorem 3.1. [Minimizers of $J _{Q}$ in the categorical model] For $q \in ( 0 , 1 ]$ , the unique minimizer of $\begin{array} { r } { J _{Q} ( \pmb { \theta } , q ) = \sum _{j} \alpha _{j} ( - \log _{q} \theta _{j} ) } \end{array}$ over $\Delta _{N}$ is the escort distribution of order $1 / q$ :

$$
\theta_{j} ^{*} (q) = \frac{\alpha_{j} ^{1 / q}}{\sum_{k = 1} ^{N} \alpha_{k} ^{1 / q}}, \quad j = 1, \dots , N. \tag{4}
$$

For $q = 0$ , the objective is linear and minimized at any vertex $e _{j}$ with $j \in \mathrm { a r g m a x } _{k} \alpha _{k}$

Proof. Case $q \in ( 0 , 1 ]$ . Since $h _{q}$ is strictly convex for $q > 0$ , the objective is strictly convex on the interior of $\Delta _{N}$ , and the minimizer is unique. Since all $\alpha _{j} > 0$ , the minimizer lies in the interior (any boundary point has infinite loss for $q = 1$ and suboptimal loss for $q < 1 \AA$ ), so we can use Lagrange multipliers for the equality constraint $\textstyle \sum _{j} \theta _{j} = 1$ :

$$
- \alpha_{j} \theta_{j} ^{- q} - \lambda = 0 \quad \Longrightarrow \quad \alpha_{j} \theta_{j} ^{- q} = \mu \quad \text{forall} j,
$$

where $\mu \triangleq - \lambda > 0$ . Solving: $\theta _{j} = ( \alpha _{j} / \mu ) ^{1 / q}$ . The constraint $\textstyle \sum _{j} \theta _{j} = 1$ yields $\begin{array} { r } { \mu ^{1 / q} = \sum _{k} \alpha _{k} ^{1 / q} } \end{array}$ giving Equation (4).

Case $q = 0$ . The objective $\begin{array} { r } { J _{Q} ( \theta , 0 ) = 1 - \sum _{j} \alpha _{j} \theta _{j} } \end{array}$ is linear, minimized at any vertex $e _{j}$ with $j \in$ $j \in \mathrm { a r g m a x } _{k} \alpha _{k}$ . □

Corollary B.2 (Endpoint behavior and monotone sharpening). Under the categorical model:

1. Density-estimation pole $( q = 1$ ): $\theta _{j} ^{*} ( 1 ) = \alpha _{j}$ . The model exactly recovers the data distribution.   
2. Exploitation pole $( q \to 0 ^{+} ,$ ): assuming a unique mode $j ^{*} = \mathrm { a r g m a x } _{k} \alpha _{k}$ , $\theta _{j} ^{*} ( q ) \to \mathbb{I} ( j =$ $j ^{*}$ ). The model concentrates all mass on the most frequent output.   
3. Monotone sharpening: for $0 < q ^{\prime} < q \leq 1$ and $\alpha _{j} > \alpha _{k}$ , $\theta _{j} ^{\ast} ( q ^{\prime} ) / \theta _{k} ^{\ast} ( q ^{\prime} ) > \theta _{j} ^{\ast} ( q ) / \theta _{k} ^{\ast} ( q )$ .

Proof. Part (1): $^ 1 / q = 1$ . Part (2): $( \alpha _{j} / \alpha _{j ^ { *} } ) ^{1 / q}  0$ for $j \neq j ^{*}$ . Part (3): $\theta _{j} ^{*} / \theta _{k} ^{*} = ( \alpha _{j} / \alpha _{k} ) ^{1 / q}$ , increasing in $1 / q$ . □

Corollary B.3 (Propriety). The Tsallis $q$ -logarithmic scoring rule is strictly proper if and only if $q = 1$ .

Proof. By Theorem 3.1, the maximizer of $\mathbb{E} _{y \sim \alpha} [ \log _{q} ( \theta _{y} ) ]$ is $\theta _{j} ^{*} \propto \alpha _{j} ^{1 / q}$ , which equals $\alpha$ iff $q = 1$ For $q \in ( 0 , 1 )$ the true distribution $\alpha$ is not even a maximizer (the rule is not proper at all), let alone the unique one. □

The robustness counterpart under label noise — both static (where the escort minimizer concentrates) and dynamic (how fast the model gets there) — is deferred to Section C.5, after the gradient-flow machinery of Section 5.

# C Proofs for Section 5: Commitment Dynamics under Gradient Flow

# C.1 Warm-up: exact analysis on the sigmoid model

Before proving the general results, we work through the scalar sigmoid model $P ( \theta ) = \sigma ( \theta ) =$ $( 1 + e ^{- \theta} ) ^{- 1}$ as a warm-up. This model admits exact closed-form escape times that validate the $\Theta ( \cdot )$ bounds in Theorem 5.2.

Under gradient flow on $\ell _{q} ( \theta ) = - \log _{q} ( \sigma ( \theta ) )$ , the parameter evolves as $\dot{\theta} = P ( \theta ) ^{- q} P ^{\prime} ( \theta )$ . Since $P ^{\prime} ( \theta ) = P ( \theta ) ( 1 - P ( \theta ) )$ , the chain rule gives:

$$
\dot{p} = \left[ P ^{\prime} (\theta) \right] ^{2} P (\theta) ^{- q} = p ^{2 - q} (1 - p) ^{2}.
$$

This is a special case of the general dynamics (Equation (6)) with score norm $\| s ( \theta ) \| ^{2} = ( 1 - p ) ^{2}$ , which satisfies $\| s \| ^{2} \in [ ( 1 - \mathit { \bar{\delta} } ) ^{2} , 1 ]$ on $p \in [ p _{0} , \delta ]$ — confirming the bounded score assumption.

The separable ODE gives the exact escape time:

$$
T _{q} \left(p _{0}, \delta\right) = \int_{p _{0}} ^{\delta} \frac{d u}{u ^{2 - q} (1 - u) ^{2}}. \tag{15}
$$

We evaluate this integral using a dominant/remainder decomposition. Write $( 1 - u ) ^{- 2} = 1 + r ( u )$ where $\begin{array} { r } { r ( u ) = \frac { 2 u - u ^{2} } { ( 1 - u ) ^{2} } } \end{array}$ (1−u)2 . On $u \in [ 0 , \delta ]$ with $\delta \le 1 / 2$ , we have $0 \leq r ( u ) \leq 8 u$ . Substituting and distributing:

$$
T _{q} (p _{0}, \delta) = \underbrace{\int_{p _{0}} ^{\delta} \frac{d u}{u ^{2 - q}}} _{\text{dominant}} + \underbrace{\int_{p _{0}} ^{\delta} \frac{r (u)}{u ^{2 - q}} d u} _{\text{remainder}}.
$$

Case q ∈ (0, 1). The dominant integral evaluates to p0 $q \in \mathsf { \Gamma } ( 0 , 1 )$ $\begin{array} { r } { \frac { p _{0} ^{- ( 1 - q )} - \delta ^{- ( 1 - q )} } { 1 - q } = \frac { p _{0} ^{- ( 1 - q )} } { 1 - q } ( 1 + o ( 1 ) ) \ } \end{array}$ 1−q . The remainder satisfies $\begin{array} { r } { 0 \leq \int r ( u ) u ^{- ( 2 - q )} d u \leq 8 \int u ^{q - 1} d u = \frac { 8 \dot{\delta} ^{q} } { q } } \end{array}$ 8δqq , a constant. So the remainder is negligible and $\begin{array} { r } { T _{q} = \frac { p _{0} ^{- ( 1 - q )} } { 1 - q } ( 1 + o ( 1 ) ) } \end{array}$ .

Case $q = 0$ . The dominant integral gives $\scriptstyle { \frac { 1 } { p _{0} } } ( 1 + o ( 1 ) )$ . The remainder is $O ( \log ( 1 / p _{0} ) )$ , still negligible compared to $1 / p _{0}$ . So $\begin{array} { r } { T _{0} = \frac { 1 } { p _{0} } ( 1 + o ( 1 \dot{)} ) } \end{array}$ .

Case $q = 1$ . The dominant integral is $\log ( 1 / p _{0} ) + \log \delta .$ . The remainder satisfies $\begin{array} { r } { \int r ( u ) u ^{- 1} d u \le } \end{array}$ $8 ( \delta - p _{0} ) = { \cal O } ( 1 )$ . So $T _{1} = \log ( 1 / p _{0} ) ( 1 + o ( 1 ) )$ .

Note that the sigmoid model yields exact $1 + o ( 1 )$ asymptotics (not just $\Theta ( \cdot ) \big .$ ) because $\| s \| ^{2} = $ $( 1 - p ) ^{2} \to 1$ as $p  0$ , so the score norm converges to a known constant. This is stronger than the general theorem, which only assumes bounded score norms.

# C.2 Proof of Theorem 5.1: Exploitation is provably slow

Theorem 5.1. [Exploitation is provably slow] Let $\pmb \theta \in \mathbb{R} ^{d}$ parameterize any differentiable model. Consider gradient flow on $\ell _{q} ( \pmb { \theta } ) = - \log _{q} ( P _{\pmb { \theta} } )$ , starting from $p _{0} = P _{\pmb { \theta} ( 0 ) } \in ( 0 , 1 / 2 ]$ with fixed target $\delta \in ( 0 , 1 / 2 ]$ . Suppose only that $\left\| s ( \pmb \theta ( t ) ) \right\| \leq C$ throughout the trajectory. Then as $p _{0} \to 0$ :

$$
T _{q} (p _{0}, \delta) = \Omega \left(\frac{p _{0} ^{- (1 - q)}}{1 - q}\right) f o r q \in [ 0, 1),
$$

$$
T _{1} (p _{0}, \delta) = \Omega \left(\log \frac{1}{p _{0}}\right).
$$

In particular, the exploitation pole cannot escape cold start faster than $\Omega ( 1 / _{p _ { 0} } )$

Proof. From Equation (6), $\dot{p} = p ^{2 - q} \lVert s ( \pmb { \theta } ) \rVert ^{2} \leq C ^{2} p ^{2 - q}$ . By the ODE comparison principle (since $u \mapsto u ^{2 - q}$ is nondecreasing on $( 0 , 1 ] ) , p ( t ) \ \leq \ p ^{*} ( t )$ $( 0 , 1 ] )$ where $p ^{*}$ solves $\hat{p} ^{*} = \hat{C} ^{2} ( p ^{*} ) ^{2 - q}$ with $p ^{*} ( 0 ) = p _{0}$ . So $p$ reaches $\delta$ no sooner than $p ^{*}$ :

$$
T _{q} \geq \frac{1}{C ^{2}} \int_{p _{0}} ^{\delta} \frac{d u}{u ^{2 - q}}.
$$

For q ∈ [0, 1), the integral evaluates to p0 $q ~ \in ~ [ 0 , 1 )$ $\begin{array} { r l r } { \frac { p _{0} ^{- ( 1 - q )} - \delta ^{- ( 1 - q )} } { 1 - q } } & { { } = } & { \frac { p _{0} ^{- ( 1 - q )} } { 1 - q } ( 1 + o ( 1 ) ) } \end{array}$ −(1−q)−δ−(1−q) 1−q p−(1−q)0 , giving $T _{q} ~ =$ $\Omega ( p _{0} ^{- ( 1 - q )} / ( 1 - q ) )$ .

For $q = 1$ , the integral is $\log ( \delta / p _{0} ) = \log ( 1 / p _{0} ) ( 1 + o ( 1 ) )$ , giving $T _{1} = \Omega ( \log ( 1 / p _{0} ) )$ .

# C.3 Proof of Theorem 5.2: Tight cold-start escape rates

Theorem 5.2. [Tight cold-start escape rates] Under the same setup as Theorem 5.1, suppose additionally that $\| s ( \pmb \theta ( t ) ) \| \geq c > 0$ throughout the trajectory. Then:

1. General $q \in [ 0 , 1 )$

$$
T _{q} (p _{0}, \delta) = \Theta \left(\frac{p _{0} ^{- (1 - q)}}{1 - q}\right) a s p _{0} \rightarrow 0.
$$

2. Density-estimation pole $\displaystyle q = 1 ,$ ):

$$
T _{1} (p _{0}, \delta) = \Theta \left(\log \frac{1}{p _{0}}\right) \quad a s p _{0} \rightarrow 0.
$$

3. Speedup ratio: for any $q < q ^{\prime}$ with $q ^{\prime} \leq 1$ ,

$$
\begin{array}{c} \frac{T _{q} (p _{0} , \delta)}{T _{q ^{\prime}} (p _{0} , \delta)} \to \infty \quad a s p _{0} \to 0. \end{array}
$$

Proof. The lower bound on time $( \Omega )$ follows from Theorem 5.1. For the upper bound, the additional assumption $\| s \| \geq c > 0$ gives $\dot{p} \ge c ^{2} p ^{2 - q}$ ; by the ODE comparison principle, $p ( t ) \geq p _{*} ( t )$ where $p _{*}$ solves $\dot{p} _{*} = \ddot{c} ^{2} ( p _{*} ) ^{2 - q}$ , so $p$ reaches $\delta$ no later than $p _{*}$ :

$$
T _{q} \leq \frac{1}{c ^{2}} \int_{p _{0}} ^{\delta} \frac{d u}{u ^{2 - q}}.
$$

This integral evaluates to $\frac { p _{0} ^{- ( 1 - q )} } { 1 - q } \big ( 1 + o ( 1 ) \big )$ for $q \in [ 0 , 1 )$ and $\log ( 1 / p _{0} ) ( 1 + o ( 1 ) )$ for $q = 1$ Combined with the lower bound, $T _{q} = \Theta ( p _{0} ^{- ( 1 - q )} / ( 1 - q ) )$ for $q < 1$ and $T _{1} = \Theta ( \log ( 1 / p _{0} ) )$ .

Speedup ratio. For $q < q ^{\prime} < 1 \colon T _{q} / T _{q ^ { \prime} } = \Theta ( p _{0} ^{- ( q ^ { \prime} - q ) } ) \to \infty$ . For $q < 1$ and $q ^{\prime} = 1 \colon T _{q} / T _{1} =$ $\Theta ( p _{0} ^{- ( 1 - q )} / \log ( 1 / p _{0} ) ) \to \infty$ .

# C.4 Near-optimality convergence (supplementary result)

Proposition C.1 (Near-optimality convergence is $q$ -independent). Suppose that near optimality, $\| s (  { \bar{\theta} } ) \| ^{2}$ depends on $\pmb \theta$ only through $P _{\pmb { \theta} }$ (i.e., $\lVert s ( \pmb \theta ) \rVert ^{2} = h ( \bar{P} _{\pmb \theta} )$ for some function $h$ ). Then for $\epsilon _{0} \ll 1$ and $\epsilon _{1} < \epsilon _{0}$ , the time to improve from $P _{\theta} = 1 - \epsilon _{0}$ to $P _{\theta} = 1 - \epsilon _{1}$ satisfies

$$
T _{q} \left(1 - \epsilon_{0}, 1 - \epsilon_{1}\right) = T _{q ^{\prime}} \left(1 - \epsilon_{0}, 1 - \epsilon_{1}\right) \left(1 + O \left(\epsilon_{0}\right)\right)
$$

for all $q , q ^{\prime} \in [0, 1]$ . That is, the convergence time is the same for all members of the $J _{Q}$ family up to a correction that vanishes as $\epsilon _{0}  0$ .

Proof. Write $\epsilon = 1 - p$ with $\epsilon \ll 1$ . From Equation (6), $\dot{\epsilon} = - ( 1 - \epsilon ) ^{2 - q} \| s ( \pmb { \theta } ) \| ^{2} < 0$ . Since $\epsilon$ decreases over time, the convergence time from $\epsilon _{\mathrm { 0} }$ to $\epsilon _{1}$ is:

$$
T _{q} = \int_{\epsilon_{1}} ^{\epsilon_{0}} \frac{d \epsilon}{(1 - \epsilon) ^{2 - q} \| s (\boldsymbol{\theta}) \| ^{2}}.
$$

For any $q , q ^{\prime} \in [0, 1]$ , the integrands of $T _{q}$ and $T _{q ^ { \prime} }$ differ by the factor $( 1 - \epsilon ) ^{q - q ^ { \prime} }$ . We bound this factor on $\epsilon \in [ \epsilon _{1} , \epsilon _{0} ]$ with $\epsilon _{0} \ll 1$ . Using the Taylor expansion $\log ( 1 - \epsilon ) = - \epsilon - \epsilon ^{2} / 2 - \cdot \cdot \cdot$ :

$$
\begin{array}{l} \log (1 - \epsilon) ^{q - q ^{\prime}} = (q - q ^{\prime}) \log (1 - \epsilon) \\ = \left(q - q ^{\prime}\right) \left(- \epsilon - \frac{\epsilon^{2}}{2} - \dots\right). \\ \end{array}
$$

Since $| q - q ^{\prime} | \leq 1$ :

$$
\left| \log (1 - \epsilon) ^{q - q ^{\prime}} \right| \leq \epsilon + \frac{\epsilon^{2}}{2} + \dots = O (\epsilon).
$$

Exponentiating and using $e ^{x} = 1 + x + O ( x ^{2} ) = 1 + O ( \epsilon )$ for $x = O ( \epsilon )$ , we get $( 1 { - } \epsilon ) ^{q - q ^ { \prime} } = 1 { + } O ( \epsilon )$ . Since $\epsilon \leq \epsilon _{0}$ on $[ \epsilon _{1} , \epsilon _{0} ]$ , the integrands of $T _{q}$ and $T _{q ^ { \prime} }$ differ by a multiplicative $1 + O ( \epsilon _{0} )$ factor, giving $T _{q} / T _{q ^ { \prime} } = 1 + O ( \epsilon _{0} )$ . □

# C.5 Noise-fitting rate under symmetric label noise

The cold-start escape rates (Theorems 5.1 and 5.2) measure how fast the model commits to correct supervision under the $J _{Q}$ amplification $P _{\theta} ^{- q}$ . The symmetric question is how fast the model commits to incorrect supervision: the same amplification drives both, giving the following dynamical formulation of robustness under label noise.

Noise-contamination setup. We work with a two-label categorical model, chosen to expose the mechanism in the simplest possible setting. For a single input $\mathbf{x} ^{*}$ , the model predicts one of two labels $\{ c , k \}$ with probabilities $p _{\pmb { \theta} } ( c \mid \mathbf{x} ^{*} ) = p$ and $p _{\pmb { \theta} } ( k | \mathbf{x} ^{*} ) = 1 - p$ , where $p$ is a differentiable function of $\pmb \theta \in \mathbb{R} ^{d}$ . The target label is corrupted: with probability $1 - \epsilon$ it equals the clean value $c$ , and with probability $\epsilon \in ( 0 , 1 / 2 )$ it flips to the noise value $k$ , giving $\tilde{\alpha} = ( 1 - \epsilon , \epsilon )$ . The restriction to two labels is cosmetic: in the $N$ -label categorical model with symmetric noise $\tilde{\alpha} = ( 1 - \epsilon ) \alpha + \epsilon \cdot \mathrm { U n i f }$ , conditioning on the two-subset $\{ j ^{*} , k \}$ containing the clean mode $j ^{*}$ and any fixed wrong label $k$ reduces to this binary setting.

Let $p ( t ) \ = \ p _{\pmb { \theta} } ( c \ | \ \mathbf{x} ^{*} )$ denote the clean-mode probability under gradient flow on $J _{Q} ( \pmb { \theta } ) =$ $\mathbb{E} _{y \sim \tilde{\alpha} } [ \ell _{q} ( p _{\pmb { \theta} } ( y \mid \mathbf{x} ^{*} ) ) ]$ , and let $\tilde{p} ( t ) = 1 - p ( t )$ denote the noise contamination. As in Section C, we assume bounded score: $c _{*} \leq \| s ( \pmb \theta ( t ) ) \| \leq C$ where $s \triangleq \nabla _{\pmb { \theta} } \log _{\ b { p} }$ is the score of the clean-mode probability (the analog of $\nabla _{\boldsymbol { \theta} } \log P _{\boldsymbol { \theta} }$ in Section 5).

The escort asymptote. Differentiating $J ( p ) = ( 1 - \epsilon ) \ell _{q} ( p ) + \epsilon \ell _{q} ( 1 - p )$ gives $J ^{\prime} ( p ) = - ( 1 -$ $\epsilon ) p ^{- q} + \epsilon \tilde{p} ^{- q}$ . Gradient flow on a scalar parameterization of $p$ yields

$$
\dot{\tilde{p}} = - \dot{p} = \left[ \epsilon \tilde{p} ^{- q} - (1 - \epsilon) (1 - \tilde{p}) ^{- q} \right] p ^{2} \| s \| ^{2}. \tag{16}
$$

For $q > 0$ , the dynamics have a unique stable equilibrium at

$$
\tilde{p} _{*} (q) \triangleq (\epsilon / (1 - \epsilon)) ^{1 / q} (1 + o (1)) \quad \text{as} \epsilon \rightarrow 0, \tag{17}
$$

obtained by solving $J ^{\prime} ( p ) = 0$ . This equilibrium coincides with the static escort minimizer from Theorem 3.1 applied to $\tilde{\alpha}$ : at $q = 1$ , $\tilde{p} _{*} ( 1 ) = \epsilon$ (the model fits observed noise exactly); as $q \to 0$ , $\tilde{p} _{*} ( q ) \to 0$ (the model concentrates on the clean mode, paralleling Corollary B.2). The escort is both where $J _{Q}$ is minimized (static) and where gradient flow converges (dynamic).

The noise-to-clean ratio $\epsilon \tilde{p} ^{- q} / [ ( 1 - \epsilon ) ( 1 - \tilde{p} ) ^{- q} ]$ is monotone decreasing in $\tilde{p}$ on $( 0 , 1 )$ : it diverges as $\tilde{p}  0$ (noise term dominates near the clean mode), equals 1 at $\tilde{p} = \tilde{p} _{*} ( q )$ (equilibrium), and vanishes as $\tilde{p}  1$ . So for $\tilde{p} \ll \tilde{p} _{*} ( q )$ — the regime of small noise contamination — the noise term in Equation (16) dominates by an arbitrarily large factor. This drives the asymptotic scaling.

Proposition C.2 (Noise-fitting rate). Fix $q \in ( 0 , 1 ]$ . Under the setup above, starting from $\tilde{p} ( 0 ) = 0 ^{+}$ , the time $T _{q} ^{\mathrm { n o i s e} } ( \eta )$ to reach noise contamination level $\tilde{p} ( T _{q} ^{\mathrm { n o i s e} } ) = \eta$ satisfies, for $\eta$ below the stable equilibrium (i.e. $\eta \ll \tilde{p} _{*} ( q )$ ; in particular as $\eta  0$ ):

$$
T _{q} ^{\text{noise}} (\eta) = \Theta \left(\frac{\eta^{q + 1}}{(q + 1) \epsilon}\right). \tag{18}
$$

The speedup ratio for $0 < q < q ^{\prime} \leq 1$ diverges: $T _{q} ^{\mathrm { n o i s e} } ( \eta ) / T _{q ^ { \prime} } ^{\mathrm { n o i s e} } ( \eta ) = \Theta ( \eta ^{- ( q ^ { \prime} - q ) } ) \to \infty$ as $\eta  0$ . At $q = 0$ , adopting the convention $\tilde{p} ^{0} \equiv 1$ , the dynamics Equation (16) reduce to $\dot{\tilde { p} } = - ( 1 - 2 \epsilon ) p ^{2} \| s \| ^{2} < 0$ everywhere (for $\epsilon < 1 / 2$ ), so $\tilde{p}$ decreases from $\tilde{p} ( 0 ) = 0 ^{+}$ and never reaches any $\eta > 0 ; T _{0} ^{\mathrm { n o i s e} } ( \eta ) = \infty$ .

Proof. By the noise-to-clean monotonicity established above, for any $K > 1$ there exists $\tilde{p} _{K} ( q ) =$ $K ^{- 1 / q} \tilde{p} _{*} ( q ) ( 1 + o ( 1 ) )$ such that for $\tilde{p} \le \tilde{p} _{K}$ , the noise term in Equation (16) exceeds $K$ times the clean term. Combined with $p = 1 - \tilde{p} \to 1$ as $\tilde{p} \to 0$ :

$$
\dot{\tilde{p}} \in \left[ \left(1 - \frac{1}{K}\right) \epsilon c _{*} ^{2} \tilde{p} ^{- q} \left(1 + o (1)\right), \epsilon C ^{2} \tilde{p} ^{- q} \right].
$$

Fix any $K > 1$ (e.g., $K = 2$ ). Separating variables, $\tilde{p} ^{q} d \tilde{p} = \Theta ( \epsilon ) d t$ integrates to $\tilde{p} ^{q + 1} / ( q + 1 ) =$ $\Theta ( \epsilon t )$ , giving $T _{q} ^{\mathrm { n o i s e} } ( \eta ) = \Theta ( \eta ^{\dot{q} + 1 } / ( ( \bar{q} + 1 ) \epsilon ) )$ for all $\eta \le \tilde{p} _{K} ( q )$ ; taking $\eta  0$ removes the constraint on $K$ . For the speedup ratio, $T _{q} / T _{q ^ { \prime} } = [ \eta ^{q + 1} / ( q + 1 ) ] / [ \eta ^{q ^ { \prime} + 1 } / ( q ^{\prime} + 1 ) ] = \Theta ( \eta ^{- ( q ^ { \prime} - q ) } ) .$ which diverges as $\eta  0$ for $q < q ^{\prime}$ . □

Structural parallel with cold-start escape. Theorem 5.2 gives $T _{q} ^{\mathrm { e s c a p e} } ( p _{0} ) = \Theta ( p _{0} ^{- ( 1 - q )} / ( 1 -$ $q )$ ) for $q \ < \ 1$ with speedup ratio $T _{q} / T _{q ^ { \prime} } = \Theta ( p _{0} ^{- ( q ^ { \prime} - q ) } )$ . Proposition C.2 gives $T _{q} ^{\mathrm { n o i s e} } ( \eta ) =$ $\Theta ( \eta ^{q + 1} / ( ( q + 1 ) \epsilon ) )$ with matching speedup ratio $\Theta ( \eta ^{- ( q ^ { \prime} - q ) } )$ . The exponents in $p _{0}$ (cold start) and $\eta$ (noise) differ by a constant shift, but the $q$ -dependence of the speedup ratio is identical in form: the same $P _{\theta} ^{- q}$ amplification accelerates commitment to all supervision, clean or corrupted. Static mode-seeking (Corollary B.2) is recovered as the $t \to \infty$ limit of Equation (16): $\tilde{p} ( t ) \to \tilde{p} _{*} ( q ) \to 0$ as $q \to 0$ .

# D Proofs for Section 6: Monte Carlo Estimators

Theorem 6.1. [Consistency and bias expansion] Fix a supervised example $\left( \mathbf{x} ^{*} , \mathbf{y} ^{*} \right)$ and assume:

1. $P _{\theta} > 0$

2. $\mathbb{E} [ \| g _{m} \| ^{2} ] < \infty$   
3. $w _{m} \geq \epsilon a . s .$ . for some $\epsilon > 0$ .

Then for any fixed $q \in [0, 1]$ ,

$$
\widehat{\nabla_{\boldsymbol{\theta}} \ell_{q}} (q, \boldsymbol{\theta}; \mathbf{x} ^{*}, \mathbf{y} ^{*}, M) \xrightarrow [ M \rightarrow \infty ]{a . s .} \nabla_{\boldsymbol{\theta}} \ell_{q} (\boldsymbol{\theta}, q; \mathbf{x} ^{*}, \mathbf{y} ^{*}). \tag{10}
$$

Moreover, for fixed $P _{\theta} > 0$ and $q \in [0, 1]$ , the bias satisfies

$$
\mathbb{E} \left[ \widehat{\nabla_{\boldsymbol{\theta}} \ell_{q}} \right] - \nabla_{\boldsymbol{\theta}} \ell_{q} = O \left(\frac{q}{M P _{\boldsymbol{\theta}} ^{q + 1}}\right) \quad a s M \rightarrow \infty . \tag{11}
$$

Proof. We write

$$
\mu_{w} \triangleq \mathbb{E} \left[ w _{m} \right] = P _{\boldsymbol{\theta}}, \quad \mu_{g} \triangleq \mathbb{E} \left[ g _{m} \right] = \nabla_{\boldsymbol{\theta}} \ell_{0} \left(\boldsymbol{\theta}; \mathbf{x} ^{*}, \mathbf{y} ^{*}\right).
$$

Define the smooth map

$$
f (a, b) \triangleq b a ^{- q},
$$

for $a > 0$ . Then

$$
\widehat{\nabla_{\boldsymbol{\theta}} \ell_{q}} (q, \boldsymbol{\theta}; \mathbf{x} ^{*}, \mathbf{y} ^{*}, M) = f (\bar{w} _{M}, \bar{g} _{M}),
$$

while the target gradient is

$$
\nabla_{\boldsymbol{\theta}} \ell_{q} (\boldsymbol{\theta}, q; \mathbf{x} ^{*}, \mathbf{y} ^{*}) = f (\mu_{w}, \mu_{g}) = \mu_{g} \mu_{w} ^{- q}.
$$

The almost sure convergence in Equation (10) follows from the Strong Law of Large Numbers, since $\bar{w} _{M} \to \mu _{w}$ and $\bar{g} _{M} \ \to \ \mu _{g}$ almost surely, and since $f$ is continuous at $( \mu _{w} , \mu _{g} )$ because $\mu _{w} = P _{\pmb { \theta} } > 0$ .

For the bias expansion, we exploit the linearity of $f$ in its second argument: $f ( a , b ) = b a ^{- q}$ , so

$$
\begin{array}{l} f \left(\bar{w} _{M}, \bar{g} _{M}\right) = \bar{g} _{M} \cdot h \left(\bar{w} _{M}\right) \\ = \underbrace{\mu_{g} h (\bar{w} _{M})} _{\text{firstpice}} + \underbrace{(\bar{g} _{M} - \mu_{g}) h (\bar{w} _{M})} _{\text{secondpice}}, \\ \end{array}
$$

where $h ( a ) \triangleq a ^{- q}$ is a scalar function whose derivatives $h ^{( k )} ( a ) = ( - q ) ( - q - 1 ) \cdot \cdot \cdot ( - q - k +$ $1 ) a ^{- ( q + k )}$ depend only on $a$ .

First piece. Expand $h ( \bar{w} _{M} )$ to third order around $\mu _{w}$ , with $h ^{\prime} ( a ) = - q a ^{- q - 1}$ , $h ^{\prime \prime} ( a ) = q ( q +$ $1 ) a ^{- q - 2}$ , $h ^{\prime \prime \prime} ( a ) \bar{=} - q ( q + 1 ) ( q + 2 ) a ^{- q - 3}$ :

$$
\begin{array}{l} h(\bar{w}_{M}) = \underbrace{h(\mu_{w})}_{\mathbb{E}[\cdot ] = \mu_{w}^{-q}} + \underbrace{h^{\prime}(\mu_{w})(\bar{w}_{M} - \mu_{w})}_{\mathbb{E}[\cdot ] = 0} + \underbrace{\frac{1}{2}h^{\prime\prime}(\mu_{w})(\bar{w}_{M} - \mu_{w})^{2}}_{\mathbb{E}[\cdot ] = \frac{q(q + 1)}{2M}\mu_{w}^{-q - 2}\mathbf{Var}(w_{m})} \\ + \underbrace{\frac{1}{6} h ^{\prime \prime \prime} (\mu_{w}) (\bar{w} _{M} - \mu_{w}) ^{3}} _{\mathbb{E} [ \cdot ] = O (M ^{- 2}) \text{via} \kappa_{3} / M ^{2}} + \underbrace{R _{M} ^{(1)}} _{\text{4 t h - o r d e r}}. \\ \end{array}
$$

Therefore:

$$
\begin{array}{l} \mu_{g} \mathbb{E} [ h (\bar{w} _{M}) ] = \mu_{g} \mu_{w} ^{- q} + \frac{q (q + 1)}{2 M} \mu_{g} \mu_{w} ^{- q - 2} \mathbf{V a r} (w _{m}) \\ + O (M ^{- 2}) + \mu_{g} \mathbb{E} \left[ R _{M} ^{(1)} \right]. \\ \end{array}
$$

Second piece. The factor $( \bar{g} _{M} - \mu _{g} ) = O _{p} ( M ^{- 1 / 2} )$ , so a second-order expansion of $h ( \bar{w} _{M} )$ suffices. Multiplying $\left( \bar{g} _{M} - \mu _{g} \right)$ by each term of the expansion and taking expectations:

$$
\begin{array}{l} \mathbb{E} \left[ \left(\bar{g} _{M} - \mu_{g}\right) h \left(\bar{w} _{M}\right) \right] \\ = \underbrace{h (\mu_{w})   \mathbb{E} [ \bar{g} _{M} - \mu_{g} ]} _{= 0} + \underbrace{h ^{\prime} (\mu_{w})   \mathbb{E} [ (\bar{g} _{M} - \mu_{g}) (\bar{w} _{M} - \mu_{w}) ]} _{= - \frac{q}{M} \mu_{w} ^{- q - 1} \mathbf{C o v} (g _{m}, w _{m})} \\ + \underbrace{\frac{1}{2} h ^{\prime \prime} (\mu_{w})   \mathbb{E} [ (\bar{g} _{M} - \mu_{g}) (\bar{w} _{M} - \mu_{w}) ^{2} ]} _{= O (M ^{- 2}) \text{v i a i . i d . e x p a n s i o n}} + \underbrace{\mathbb{E} [ R _{M} ^{(2)} ]} _{\text{3 r d - o r d e r r e m a i n d e r}} \\ \end{array}
$$

For the cross moment, expand $\begin{array} { r } { \mathbb{E} [ ( \bar{g} _{M} - \mu _{g} ) ( \bar{w} _{M} - \mu _{w} ) ^{2} ] = M ^{- 3} \sum _{i , j , k} \mathbb{E} [ ( g _{i} - \mu _{g} ) ( w _{j} - \mu _{w} ) ( w _{k} - } \end{array}$ $\mu _{w} ) ]$ . By independence, the only nonzero index pattern is $i = j = k$ (all others vanish because $\mathbb{E} [ \stackrel { \cdot \cdot } { g _{i} } - \mu _{g} ] = 0$ or $\mathbb{E} [ w _{j} - \mu _{w} ] = 0 \mathrm { , }$ ). The $M$ surviving terms give $\mathbb{E} [ ( g _{m} - \mu _{g} ) ( w _{m} - \mu _{w} ) ^{2} ] / M ^{2} =$ $O ( M ^{- 2} )$ , since $| ( w _{m} - \mu _{w} ) ^{2} | \le 1$ and $\mathbb{E} [ \left. g _{m} \right. ] < \infty$ (Assumption 2). The remainder has the form R(2)M $R _{M} ^{( 2 )} = ( \bar{g} _{M} - \mu _{g} ) \cdot O ( | \bar{w} _{M} - \mu _{w} | ^{3} )$ .

Combining. Adding the two pieces and substituting $\mu _{w} = P _{\pmb { \theta} } , \mu _{g} = \nabla _{\pmb { \theta} } \ell _{0} , \nabla _{\pmb { \theta} } \ell _{1} = \nabla _{\pmb { \theta} } \ell _{0} / P _{\pmb { \theta} }$ $\mu _{w} = P _{\theta}$ $\mu _{g} = \nabla _{\pmb { \theta} } \ell _{0}$

$$
\begin{array}{l} \mathbb{E} \left[ \widehat{\nabla_{\boldsymbol{\theta}} \ell_{q}} (q, \boldsymbol{\theta}; \mathbf{x} ^{*}, \mathbf{y} ^{*}, M) \right] = \nabla_{\boldsymbol{\theta}} \ell_{q} (\boldsymbol{\theta}, q; \mathbf{x} ^{*}, \mathbf{y} ^{*}) \\ + \frac{q}{M P _{\boldsymbol{\theta}} ^{q + 1}} \\ \left[ \frac{q + 1}{2} \nabla_{\boldsymbol{\theta}} \ell_{1} \left(\boldsymbol{\theta}; \mathbf{x} ^{*}, \mathbf{y} ^{*}\right) \mathbf{V a r} \left(w _{m}\right) - \mathbf{C o v} \left(g _{m}, w _{m}\right) \right] \\ + \mathbb{E} [ R _{M} ], \\ \end{array}
$$

where RM = µgR(1)M $R _{M} = \mu _{g} R _{M} ^{( 1 )} + R _{M} ^{( 2 )}$ + R (2)M . +

Remainder bound. Write $\begin{array} { r } { \mathbb{E} [ R _{M} ] = \mathbb{E} [ R _{M} \cdot \mathbf{1} _{A} ] + \mathbb{E} [ R _{M} \cdot \mathbf{1} _{A ^ { c} } ] } \end{array}$ where $A = \{ \bar{w} _{M} \geq P _{\theta} / 2 \}$

On $A$ . The derivatives of $h$ are bounded on $\{ a \ge P _{\pmb { \theta} } / 2 \}$ : $| h ^{( k )} ( a ) | \le C _{k}$

For $R _{M} ^{( 1 )}$ (the fourth-order scalar remainder), the integral form gives $| R _{M} ^{( 1 )} | \leq C _{4} | \bar{w} _{M} - \mu _{w} | ^{4}$ on $A$ Since wm $\in [0, 1] , \mathbb{E} \big [ | \bar{w} _{M} - \mu _{w} | ^{4} \big ] = O ( M ^{- 2} )$ , so $\mathbb{E} [ | R _{M} ^{( 1 )} | \cdot { \mathbf{1} } _{A} ] = O ( M ^{- 2} )$ .

For $R _{M} ^{( 2 )} \ = \ ( \bar{g} _{M} - \mu _{g} ) \cdot O ( | \bar{w} _{M} - \mu _{w} | ^{3} )$ on $A$ (the third-order remainder from the second piece), Cauchy–Schwarz gives $\mathbb{E} \big [ | R _{M} ^{( 2 )} | \cdot \mathbf{1} _{A} \big ] \leq C _{3} \sqrt { \mathbb{E} \big [ \| \bar{g} _{M} - \mu _{g} \| ^{2} \big ] } \sqrt { \mathbb{E} \big [ ( \bar{w} _{M} - \mu _{w} ) ^{6} \big ] } =$ $O ( M ^{- 1 / 2} ) O ( M ^{- 3 / 2} ) = O ( M ^{- 2} )$ , using Assumption 2 and the boundedness of $w _{m}$ .

On $A ^{c}$ . Assumption 3 gives $\bar{w} _{M} \ge \epsilon > 0$ , so $| h ( \bar{w} _{M} ) | \leq \epsilon ^{- q}$ everywhere and $| f ( \bar{w} _{M} , \bar{g} _{M} ) | \leq$ $\epsilon ^{- q} \lVert \bar{g} _{M} \rVert$ . Therefore $| R _{M} | \leq | f ( \bar{w} _{M} , \bar{g} _{M} ) | + | T _{M} | \leq C \epsilon ^{- q} \left( 1 + \| \bar{g} _{M} \| \right)$ , where $T _{M}$ collects the (bounded) Taylor terms. Again by Cauchy–Schwarz,

$$
\mathbb{E} \left[ \left| R _{M} \right| \cdot \mathbf{1} _{A ^{c}} \right] \leq C \epsilon^{- q} \sqrt{\mathbb{E} \left[ (1 + \| \bar{g} _{M} \|) ^{2} \right]} \sqrt{P \left(A ^{c}\right)}.
$$

The first factor is $O ( 1 )$ by Assumption 2. For the second, since $w _{m} \in [0, 1]$ are i.i.d. with mean $P _{\theta}$ , Hoeffding’s inequality with $t = P _{\theta} / 2$ gives $P ( A ^{c} ) = P ( \bar{w} _{M} - P _{\pm} \leq - \bar{P} _{\theta} / 2 ) \leq \exp ( - M P _{\theta} ^{2} / 2 )$ Thus $\mathbb{E} [ | R _{M} | \cdot { \bf 1 } _{A ^ { c} } ]$ decays faster than any polynomial in $M$ .

Combining: $\mathbb{E} [ R _{M} ] = O ( M ^{- 2} )$ , yielding Equation (11).

# D.1 RLOO control variate derivation

We derive the RLOO estimator (12) from the plug-in estimator (9). Using the chain rule, $g _{m}$ from (7) decomposes into a score-function term and a pathwise term:

$$
g _{m} = - w _{m} \nabla_{\boldsymbol{\theta}} \log p _{\boldsymbol{\theta}} \left(\mathbf{z} ^{(m)} \mid \mathbf{x} ^{*}\right) - \nabla_{\boldsymbol{\theta}} w _{m}. \tag{19}
$$

Substituting into the plug-in estimator isolates the score-function component:

$$
\widehat{\nabla_{\boldsymbol{\theta}} \ell_{q}} ^{\text{p l u g - i n}} = \frac{1}{M} \sum_{m = 1} ^{M} \left[ \frac{- w _{m}}{(\bar{w} _{M}) ^{q}} \nabla_{\boldsymbol{\theta}} \log p _{\boldsymbol{\theta}} \left(\mathbf{z} ^{(m)} \mid \mathbf{x} ^{*}\right) - \frac{\nabla_{\boldsymbol{\theta}} w _{m}}{(\bar{w} _{M}) ^{q}} \right]. \tag{20}
$$

Since $\mathbb{E} [ \nabla _{\pmb { \theta} } \log p _{\pmb { \theta} } ( \mathbf{z} ^{( m )} \mid \mathbf{x} ^{*} ) ] = 0$ , we can subtract any baseline from the score-function coefficient $- w _{m} / ( \bar{w} _{M} ) ^{q}$ without changing the expected value, provided the baseline does not depend on $\mathbf{z} ^{( m )}$ .

We use a leave-one-out approximation. Let $\begin{array} { r } { \bar{w} _{\neg m} = \frac { 1 } { M - 1 } \sum _{j \neq m} w _{j} } \end{array}$ . Replacing $w _{m}$ with $\bar{w} _{\neg m}$ in the coefficient, the batch mean collapses to $\bar{w} _{\neg m}$ , giving a surrogate coefficient of $- ( \bar{w} _{\neg m} ) ^{1 - q}$ . Subtracting this baseline yields the RLOO estimator (12).

Endpoint recovery. At $q = 0$ , the centered weight evaluates to $w _{m} - \bar{w} _{\lnot m}$ , and the score-function term becomes $- ( w _{m} - \bar{w} _{- m} ) \nabla _{\pmb { \theta} } \log p _{\pmb { \theta} } ( \mathbf{z} ^{( m )} \mid \mathbf{x} ^{*} )$ , exactly recovering the REINFORCE leaveone-out (RLOO) estimator standard in RLVR. At $q = 1$ , the centered weight is $w _{m} / \bar{w} _{M} - 1$ ; since $\begin{array} { r } { \sum _{m = 1} ^{M} ( w _{m} / \bar{w} _{M} - 1 ) = 0 } \end{array}$ , this acts as a self-normalizing baseline that strictly centers the importance weights across the batch.

Proposition D.1 (RLOO bias preservation, restated). Under the assumptions of Theorem 6.1, the RLOO estimator (12) satisfies the same bias expansion as the plug-in estimator (9).

Proof. The RLOO estimator (12) differs from the plug-in estimator (20) by subtracting $( \bar{w} _{\neg m} ) ^{1 - q}$ from the score-function coefficient $w _{m} / ( \bar{w} _{M} ) ^{q}$ for each sample $m$ . Denoting $\begin{array} { r } { s _{m} = \nabla _{\pmb { \theta} } \log p _{\pmb { \theta} } ( \mathbf{z} ^{( m )} \mid \mathbf{\tau} } \end{array}$ $\mathbf{x} ^{*} ,$ ), the difference in expectations is

$$
\Delta = \frac{1}{M} \sum_{m = 1} ^{M} \mathbb{E} [ (\bar{w} _{\neg m}) ^{1 - q} s _{m} ].
$$

Since $\begin{array} { r } { \bar{w} _{\neg m} = \frac { 1 } { M - 1 } \sum _{j \neq m} w _{j} } \end{array}$ is a function of $\{ \mathbf{z} ^{( j )} \} _{j \neq m}$ only, and $s _{m} = \nabla _{\pmb \theta} \log p _{\pmb \theta} \big ( \mathbf z ^{( m )} \ | \ \mathbf x ^{*} \big )$ is a function of $\mathbf{z} ^{( m )}$ only, the independence of the i.i.d. samples gives

$$
\mathbb{E} \big [ (\bar{w} _{\neg m}) ^{1 - q} s _{m} \big ] = \mathbb{E} \big [ (\bar{w} _{\neg m}) ^{1 - q} \big ] \cdot \underbrace{\mathbb{E} [ s _{m} ]} _{= 0} = 0,
$$

where $\begin{array} { r } { \mathbb{E} [ s _{m} ] = \mathbb{E} _{\mathbf{z} \sim p _{\theta} } [ \nabla _{\theta} \log p _{\theta} ( \mathbf{z} \mid \mathbf{x} ^{*} ) ] = 0 } \end{array}$ is the standard score-function identity. Therefore $\Delta = 0$ and the two estimators have identical expectations for every $M$ . □

# D.2 Endpoint recovery

Proposition D.2 (Endpoint recovery for GARL and PAFT). Fix a supervised example $\left( \mathbf{x} ^{*} , \mathbf{y} ^{*} \right)$ with $P _{\theta} > 0$ .

1. GARL at $q = 0$ recovers Rao–Blackwellized REINFORCE [Williams, 1992, Zhou et al., 2026]:

$$
\left. \widehat{\nabla_{\boldsymbol{\theta}} \ell_{q}} \right| _{q = 0} = \bar{g} _{M} = \frac{1}{M} \sum_{m = 1} ^{M} \left(- w _{m} \nabla_{\boldsymbol{\theta}} \log p _{\boldsymbol{\theta}} \left(\mathbf{z} ^{(m)}, \mathbf{y} ^{*} \mid \mathbf{x} ^{*}\right)\right),
$$

which is unbiased for $\nabla _{\boldsymbol { \theta} } \ell _{0}$ by Equation (8). Each $g _{m}$ marginalizes out the output y given $\mathbf{z} ^{( m )}$ analytically via $w _{m} = p _{\pmb \theta} ( \mathbf y ^{*} \mid \mathbf x ^{*} , \mathbf z ^{( m )} )$ , rather than relying on a sampled output and binary reward.

2. GARL at $q = 1$ recovers the IWAE gradient estimator [Burda et al., 2015], a self-normalized importance sampling (SNIS) estimator for $\nabla _{\boldsymbol { \theta} } \log P _{\boldsymbol { \theta} }$ :

$$
\left. \widehat{\nabla_{\boldsymbol{\theta}} \ell_{q}} \right| _{q = 1} = \frac{\bar{g} _{M}}{\bar{w} _{M}} = \frac{\sum_{m} w _{m} \left(- \nabla_{\boldsymbol{\theta}} \log p _{\boldsymbol{\theta}} (\mathbf{z} ^{(m)} , \mathbf{y} ^{*} \mid \mathbf{x} ^{*})\right)}{\sum_{m} w _{m}}.
$$

3. PAFT at $q = 0$ reduces to posterior-resampled SFT scaled by $P _{\pmb { \theta} }$ :

$$
\left. \hat{\nabla} _{\mathrm{P A F T}} \right| _{q = 0} = - \bar{w} _{M} \cdot \frac{1}{K} \sum_{k = 1} ^{K} \nabla_{\boldsymbol{\theta}} \log p _{\boldsymbol{\theta}} (\mathbf{z} ^{(r _{k})}, \mathbf{y} ^{*} \mid \mathbf{x} ^{*}).
$$

The factor $\bar{w} _{M} \approx P _{\theta}$ downweights hard instances so aggressively that this endpoint is overly conservative in practice. Unlike the other three endpoints, it does not correspond to a standard method.

4. PAFT at $q = 1$ recovers the E-step of EM [Dempster et al., 1977] / TRICE [Phan et al., 2023]:

$$
\left. \hat{\nabla} _{\mathrm{P A F T}} \right| _{q = 1} = - \frac{1}{K} \sum_{k = 1} ^{K} \nabla_{\boldsymbol{\theta}} \log p _{\boldsymbol{\theta}} \left(\mathbf{z} ^{\left(r _{k}\right)}, \mathbf{y} ^{*} \mid \mathbf{x} ^{*}\right).
$$

The instance weight $( \bar{w} _{M} ) ^{1 - 1} = 1$ vanishes: all instances contribute equally, and the gradient is uniform SFT on approximate posterior samples.

Proof. Each case follows by substituting $q = 0$ or $q = 1$ into the GARL estimator (9) or PAFT estimator (14) and simplifying $( \bar{w} _{M} ) ^{0} = \bar{1}$ . □

# D.3 PAFT bias and variance

Proposition D.3 (PAFT has the same bias as GARL). Under the assumptions of Theorem 6.1, $\mathbb{E} [ \hat{\nabla} _{\mathrm { P A F T} } ] = \mathbb{E} [ \hat{\nabla} _{\mathrm { G A R L} } ] .$ for all M . In particular, the PAFT estimator has the same $O ( { q } / { M P _{\theta} ^{q + 1} } )$ bias as in Equation (11).

Proof. Conditional on the prior samples $\mathrm { p o o l } = \{ ( { \mathbf{z} } ^{( m )} , w _{m} ) \} _{m = 1} ^{M}$ , the factor $( \bar{w} _{M} ) ^{1 - q}$ is deterministic. The importance-resampled average satisfies

$$
\mathbb{E} \left[ \frac{1}{K} \sum_{k = 1} ^{K} f (\mathbf{z} ^{(r _{k})}) \Bigg | \text{pool} \right] = \sum_{m = 1} ^{M} \frac{w _{m}}{\sum_{j} w _{j}} f (\mathbf{z} ^{(m)}) = \hat{\mu} _{\text{SNIS}},
$$

where $f ( \mathbf{z} ) = \nabla _{\pmb { \theta} } \log p _{\pmb { \theta} } ( \mathbf{z} , \mathbf{y} ^{*} \mid \mathbf{x} ^{*} )$ . Therefore

$$
\begin{array}{l} \mathbb{E} [ \hat{\nabla} _{\mathrm{P A F T}} | \mathrm{p o o l} ] = - (\bar{w} _{M}) ^{1 - q} \cdot \hat{\mu} _{\mathrm{S N I S}} \\ = - \left(\bar{w} _{M}\right) ^{1 - q}. \frac{\sum_{m} w _{m} f _{m}}{M \bar{w} _{M}} \\ = \frac{1}{(\bar{w} _{M}) ^{q}} \cdot \frac{1}{M} \sum_{m} (- w _{m} f _{m}) \\ = \frac{\bar{g} _{M}}{(\bar{w} _{M}) ^{q}} = \hat{\nabla} _{\mathrm{G A R L}}. \\ \end{array}
$$

Taking outer expectations by the tower property: $\mathbb{E} [ \hat{\nabla} _{\mathrm { P A F T} } ] = \mathbb{E} [ \hat{\nabla} _{\mathrm { G A R L} } ]$ .

Proposition D.4 (GARL has strictly lower variance than PAFT). Under the same setup, $\mathbf{V a r} ( \hat{\nabla} _{\mathrm { P A F T} } ) \geq \mathbf{V a r} ( \hat{\nabla} _{\mathrm { G A R L} } )$ , with equality only when $\mathbf{V} \mathbf{a r} ( \hat{\nabla} _{\mathrm { P A F T} } \mid \mathrm { p o o l } ) = 0$ almost surely.

Proof. By Proposition D.3, $\mathbb{E} [ \hat{\nabla} _{\mathrm { P A F T} } \mid \mathrm { p o o l } ] = \hat{\nabla} _{\mathrm { G A R L} }$ . The law of total variance gives

$$
\begin{array}{l} \mathbf{V a r} (\hat{\nabla} _{\mathrm{P A F T}}) = \mathbf{V a r} \left(\mathbb{E} [ \hat{\nabla} _{\mathrm{P A F T}} | \text{pool} ]\right) + \mathbb{E} \left[ \mathbf{V a r} (\hat{\nabla} _{\mathrm{P A F T}} | \text{pool}) \right] \\ = \mathbf{V a r} (\hat{\nabla} _{\mathrm{G A R L}}) + \underbrace{\mathbb{E} \left[ \mathbf{V a r} (\hat{\nabla} _{\mathrm{P A F T}} \mid \text{pool}) \right]} _{\geq 0}, \\ \end{array}
$$

with equality iff $\mathbf{V a r} ( \hat{\nabla} _{\mathrm { P A F T} } \mid \mathrm { p o o l } ) \ = \ 0$ a.s. This holds when, for each pool realization, all resampled trajectories produce the same gradient — e.g., when a single trajectory dominates the importance weights. In the non-degenerate case, the inequality is strict. □