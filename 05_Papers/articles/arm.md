---
title: "ARM Advantage Reward Modeling for Long Horizon Manipulation"
---

# ARM: Advantage Reward Modeling for Long-Horizon Manipulation

**Authors:** Yiming Mao1, Zixi Yu1,2, Weixin Mao1,†, Yinhao Li1, Qirui Hu1, Zihan Lan1, Minzhao Zhu1, Hua Chen1,3,∗

**Affiliations:** 1LimX Dynamics; 2Beijing University of Posts and Telecommunications; 3Zhejiang University

**Emails:** {aiming, nemo, waynemao, mason, ryan.hu, sober, mayer}@limxdynamics.com, huachen@intl.zju.edu.cn *

# Abstract

Long-horizon robotic manipulation remains challenging for reinforcement learning (RL) because sparse rewards provide limited guidance for credit assignment. Practical policy improvement thus relies on richer intermediate supervision, such as dense progress rewards, which are costly to obtain and ill-suited to non-monotonic behaviors such as backtracking and recovery. To address this, we propose Advantage Reward Modeling (ARM), a framework that shifts from hard-to-quantify absolute progress to estimating relative advantage. We introduce a cost-effective tri-state labeling strategy—Progressive, Regressive, and Stagnant— that reduces human cognitive overhead while ensuring high cross-annotator consistency. By training on these intuitive signals, ARM enables automated progress annotation for both complete demonstrations and fragmented DAggerstyle data. Integrating ARM into an offline RL pipeline allows for adaptive action-reward reweighting, effectively filtering suboptimal samples. Our approach achieves a $9 9 . 4 \%$ success rate on a challenging long-horizon towel-folding task, demonstrating improved stability and data efficiency over current VLA baselines with near-zero human intervention during policy training.

Project page: https://aiming1998.github.io/ ARM

# 1. Introduction

The rapid evolution of Vision-Language-Action (VLA) models [1, 2, 13, 15] has advanced general-purpose robotic manipulation. However, most existing VLA approaches rely heavily on imitation learning (IL) [26], which demands massive datasets and incurs considerable human labor and physical resources costs during large-scale data collection [3, 10, 14, 27, 35, 36]. Beyond data quantity, the in-

herent suboptimality and noise in human demonstrations, especially in complex, long-horizon tasks, often impede policy convergence. Reinforcement Learning (RL) [33] provides a promising alternative by enabling autonomous policy refinement beyond expert demonstrations [12, 18].

Nevertheless, effective RL in long-horizon manipulation hinges on informative reward signals. While sparse rewards (e.g., binary success indicators) are straightforward to specify, they struggle to yield effective learning signals, frequently leading to convergence difficulties in long-horizon manipulation tasks. Consequently, high-quality dense rewards or informative value functions are essential to provide continuous supervision and facilitate effective credit assignment.

Current frameworks [6, 12] attempt to leverage dense signals through advantage estimation or sample reweighting. However, they depend on high-precision progress reward models to mitigate the notorious credit assignment problem. This dependency constitutes a pervasive “Reward Engineering Bottleneck”, limiting both scalability and stability of VLA deployment in unstructured environments. Designing a cost-effective reward function that provides stable and high-frequency feedback remains a formidable challenge. In particular, existing evaluation paradigms predicated on absolute progress are limited by several critical bottlenecks [6, 12, 19, 23, 34, 37, 39]: First, Zeroshot VLMs suffer from considerable unreliability and prohibitive costs; they not only incur high inference overhead, but also yield low-precision annotations due to their lack of spatial-geometric grounding, which manifests as nonmonotonic oscillations in reward signals [6, 23, 32]. Second, current schemes exhibit quantization ambiguity in failure states. By predicating progress modeling on a strict monotonicity assumption and relying on simplistic video rewinding [6, 34, 39] to simulate regression, these methods fail to comprehensively characterize authentic, nonlinear operational errors. Moreover, the conventional reliance on coarse subtask partitions [6, 34] fails to capture the subtle intra-stage transitions essential for long-

![[99_Attachments/papers/images/arm/3d29758dc6bb752d7b804e40dd4121fd279578bfabb21a8fd096887137cf7476.jpg]]  
A. Advantage Reward Model(ARM)

![[99_Attachments/papers/images/arm/a74755f7e9129078ed4c825a49b6657d84cf28504012e509526a9c541142fe8a.jpg]]  
B. Global Progress Reconstruction

![[99_Attachments/papers/images/arm/5181f7f72dee705fbb20b091194c6a2d582ad6f173f237199a68a934e4496fcb.jpg]]  
C. Advantage-Weighted Behavior Cloning(AW-BC)   
Figure 1. Overview of our proposed framework. The system consists of three main components: (1) The Advantage Reward Model (ARM) with its MIMO-based Temporal Transformer, supervised by a lightweight tri-state labeling strategy; (2) An automated pipeline for global progress reconstruction; and (3) The Advantage-Weighted Behavior Cloning (AW-BC) algorithm, which optimizes the policy using length-invariant relative gains extracted from the reconstructed progress.

horizon tasks—such as critical recovery and corrective maneuvers [11]—ultimately yielding misaligned reward signals and erratic policy updates.

To address these challenges, we introduce Advantage Reward Modeling (ARM). Our core insight is that defining absolute progress necessitates ad-hoc, task-specific heuristics that are difficult to scale. In contrast, the relative advantage between states provides a more intuitive, concise, and task-agnostic primitive for annotation. While the recent work VLAC [38] also employs interval gain prediction, its methodology is predicated on the assumption of a positive correlation between task progress and time. By decoupling progress rewards from global temporal anchors, ARM naturally accommodates regressive behaviors and error recovery. Our core contributions are as follows:

• Tri-state Advantage Labeling Strategy: We introduce a labeling method based on three fundamental categories: Progressive, Regressive, and Stagnant. This scheme is task-agnostic, imposes low cognitive load, and is natively compatible with heterogeneous and fragmented datasets.   
• Advantage Reward Model (ARM): We develop a multimodal reward model that integrates temporal video sequences with robotic proprioceptive states to estimate the relative progress gain of trajectory segments. By anchoring these predictions with a task-completion head, ARM can automatically reconstruct globally consistent dense

progress trajectories from discrete tri-state labels.

• Advantage-Weighted Behavior Cloning (AW-BC): We extend the Reward-Aligned Behavior Cloning (RA-BC) paradigm [6] by incorporating adaptive scaling coefficients to ensure compatibility with fragmented DAgger data [31]. By leveraging predicted interval gains for advantage-aware reweighting, AW-BC effectively filters suboptimal samples and prioritizes high-value recovery trajectories. Empirically, our framework achieves a nearperfect success rate of $9 9 . 4 \%$ on the challenging, longhorizon towel-folding task, marking a notable advancement in VLA policy refinement.

# 2. Related Work

# 2.1. Reward for Manipulation

Traditional reinforcement learning (RL) relies heavily on manual reward shaping, which is often labor-intensive and task-specific. To mitigate this, inverse reinforcement learning (IRL) [25] and learning from human feedback (RLHF) [8] infer reward functions but suffer from identifiability and scalability issues, respectively.

Vision-language models (VLMs) such as VIP [21] and LIV [22] provide self-supervised goal-distance signals but lack the precision required for fine-grained, contact-rich manipulation. As noted in SARM [6], single-objective distance metrics fail to capture intermediate progress in

long-horizon tasks. A common limitation shared by methods such as GVL [23], ReWiND [39], SARM [6], and VIP [21] is their reliance on a strict monotonicity assumption, which equates task progress with chronological order. However, real-world offline demonstrations often contain mistakes, retries, and temporary regressions, leading to reward misspecification under temporal heuristics. Alternative approaches also present trade-offs: hop-based mechanisms such as Robo-Dopamine [34] sacrifice fine-grained action detail, while zero-shot VLM prompting [5, 7, 17] suffers from prediction noise, high latency, and inference cost. To address these issues, we introduce the Advantage Reward Model (ARM), which relaxes temporal monotonicity by evaluating relative progress against historical visual and proprioceptive states, enabling effective advantage estimation even under temporary trajectory deviations.

# 2.2. Reward-Aligned Behavior Cloning (RA-BC)

Learning from suboptimal demonstrations is a critical bottleneck for large-scale robot learning. To address this, the paradigm of Reweighted Behavior Cloning (BC) has been widely explored. Originating from classic baselines like Advantage-Weighted Regression (AWR) [28], Advantage-Weighted Actor-Critic (AWAC) [24], and Implicit Q-Learning (IQL) [16]—these approaches extract improved policies by applying advantage-based scalar weights to suppress suboptimal trajectories.

However, traditional weighting paradigms are limited by a critical bottleneck: they inherently rely on explicit environment rewards to fit global value functions, which are notoriously inaccessible in vision-based, real-world settings. To bypass this, recent methods like SARM [6] introduced the Reward-Aligned Behavior Cloning (RA-BC) framework, leveraging a stage-aware reward model instead of environment rewards. While effective at mitigating data quality issues, SARM trades the reward bottleneck for a new constraint: it heavily relies on prohibitive manual language annotations. In contrast, our proposed ARM eliminates the need for explicit reward engineering by extracting advantage signals purely through relative progress comparisons.

# 3. Method

# 3.1. Overview of ARM

As illustrated in Fig. 1, the proposed framework shifts the paradigm from absolute progress modeling to relative advantage estimation. The system comprises three synergistic components:

(A) Advantage Reward Model: A Multi-Input Multi-Output (MIMO) Temporal Transformer designed to capture fine-grained relative advantages from multimodal observations (Fig. 1A). The model is supervised by a lightweight

![[99_Attachments/papers/images/arm/d2355b87001367128eaec04fc6330e54c937e420b86bb76884e892124ebbd749.jpg]]  
Figure 2. Comparison between MISO and MIMO architectures. MISO stands for Multi-Input Single-Output, and MIMO stands for Multi-Input Multi-Output.

tri-state labeling scheme that categorizes state transitions into progressive, regressive, or stagnant states, providing a cost-effective and task-agnostic training signal.

(B) Global Progress Reconstruction: An automated pipeline that synthesizes the discrete interval gains predicted by ARM into coherent, globally consistent reward trajectories (Fig. 1B). This process effectively transforms local relative predictions into dense, high-fidelity progress signals suitable for downstream learning.   
(C) Policy Optimization via AW-BC: The AW-BC framework that integrates the reconstructed rewards for discriminative sample reweighting (Fig. 1C). By leveraging length-adaptive gains to prioritize high-value recovery behaviors and filter suboptimal segments, AW-BC facilitates stable offline RL-style policy refinement on noisy, heterogeneous datasets.

# 3.2. Advantage Reward Modeling

The Advantage Reward Model (ARM) is designed to resolve the perceptual ambiguities inherent in isolated frames by shifting the reward estimation paradigm from absolute progress regression to relative advantage classification. Unlike traditional “Multi-Input Single-Output” (MISO) models [6, 23] that collapse temporal context into a single scalar, ARM formulates reward estimation as a Multi-Input Multi-Output (MIMO) sequence learning problem (Fig. 2). This design allows the model to contextualize local observations within a short-term history, analogous to how humans review recent temporal context to disambiguate intent and action quality.

# 3.2.1. MIMO Transformer Architecture

We adopt the Transformer Sequential Aggregator from SARM [6] as our backbone, re-engineering it to support multi-frame causal reasoning and relative advantage estimation. ARM processes a sequence of historical observations within a causal window $\mathcal{W} _{t} = \{ o _{t - 4 k} , . . . , o _{t} \}$ in parallel. By restricting the receptive field to past frames, this window-based approach ensures that predictions are in-

formed by sufficient motion cues while maintaining realtime inference capabilities. Crucially, this causal formulation ensures seamless compatibility with both online and offline RL paradigms, as it facilitates instantaneous reward generation without any dependency on future trajectory segments.

Multimodal Fusion. For each timestep $i \in \mathcal{W} _{t}$ , ARM integrates three disparate signals: (i) CLIP-based [30] visual features $v _{i} ~ \in ~ \mathbb{R} ^{d _{ v _{ i s}}}$ , (ii) robot proprioceptive states $s _{i} \in$ $\mathbb{R} ^{d _{ s t a t e}}$ , and (iii) task instructions $g ~ \in ~ \mathbb{R} ^{d _{ l a n g}}$ . These inputs are projected into a unified $d$ -dimensional latent space to form a fused multimodal embedding $x _{i}$ , defined as:

$$
x _{i} = \operatorname{MLP} \left(v _{i}\right) + \operatorname{MLP} \left(s _{i}\right) + \operatorname{MLP} (g) \tag{1}
$$

The resulting sequence $\{ x _{i} \} _{i = t - 4 k} ^{t}$ is then processed by an 8-layer Transformer Encoder to yield temporally enriched latent representations $\{ h \}$ :

$$
\left\{h _{t - 4 k}, \dots , h _{t} \right\} = \text{Transformer} \left(\left\{x _{i} \right\} _{i = t - 4 k} ^{t}\right) \tag{2}
$$

where each $h _{i}$ encodes the historical evolution and kinematic state of the task at that specific moment.

Dual-Head Learning Objective. To balance sensitivity to local state transitions with the perception of global task goals, ARM is optimized via two synergistic output heads:

1. Multi-frame Advantage Classification: The interval head infers the advantage transitions $\Delta \hat{y}$ between consecutive hidden states $\left( { { h _{i} } , { h _{i + 1} } } \right)$ . This branch is optimized via a standard cross-entropy loss, denoted as ${ \mathcal{L} } _{\mathrm { i n t} }$ , which is supervised by the tri-state labels (detailed in Sec. 3.2.2). By reformulating reward estimation as a discrete classification task rather than continuous regression, the model exhibits significantly enhanced robustness against the non-linear noise and temporal stochasticity inherent in demonstrations.

2. Task Completion Prediction: To anchor relative advantage estimations to absolute task metrics, the completion head $C$ predicts the probability that the current observation $s _{t}$ constitutes a successful terminal state. This decoupled design not only facilitates the identification of successful task executions, but also extracts progress anchor points from the predictions. When jointly utilized with the Multi-frame Advantage Classification results, these anchor points enable highly consistent, dense progress reconstructions.

Moreover, since successful terminal frames are exceedingly rare within long-horizon continuous trajectories, this branch suffers from severe class imbalance. To effectively address this issue, we optimize the completion head using Focal Loss [20]:

$$
\mathcal{L} _{s u c c} = \operatorname{FocalLoss} \left(C _{t}, \mathbb{1} [ P _{t} \geq 1 - \epsilon ]\right) \tag{3}
$$

The total objective is defined as $\mathcal{L} _{A R M} = \lambda _{i n t} \mathcal{L} _{i n t} +$ $\lambda _{s u c c} \mathcal{L} _{s u c c}$ . This joint training enables the model to not only recover continuous progress curves but also accurately identify regressive behaviors and critical task completion moments.

# 3.2.2. Lightweight Tri-state Auto Labeling Strategy

Traditional reward engineering for robotic manipulation typically requires annotators to assign a normalized scalar value $P \in [0, 1]$ to each video frame. This continuous labeling process imposes a high cognitive load and is prone to inter-annotator inconsistency, as the definition of “progress” is often subjective. Such noise in supervision signals frequently leads to suboptimal policy convergence and substantial engineering overhead.

To address these issues, we redefine the annotation task as a tri-state categorical classification of relative advantage. As illustrated in Figure 3, for any observation pair $\left( { { s _{t} } , { s _{t + k} } } \right)$ , we define a progress-based advantage label $y \in$ $\{ - 1 , 0 , + 1 \}$ according to the following rules:

• $\mathbf{+ 1}$ (Progressing): The state effectively advances toward the task goal.   
• -1 (Regressing): The state deviates from the goal, encounters an error, or results in failure.   
• 0 (Stagnant): No substantial progress is made, corresponding to waiting or idle behavior.

By acquiring initial human annotations through this simplified paradigm, we can efficiently cold-start our model. Subsequently, the trained model is utilized to perform inference on vast amounts of unannotated trajectories, automatically generating large-scale pseudo-labeled data for further training.

# 3.3. Global Progress Reconstruction

As illustrated in Fig. 1B, leveraging the MIMO architecture enables ARM to decompose complete video demonstrations and systematically aggregate the resulting predictions to reconstruct a dense, full-sequence progress curve:

1. Parallel Inference Efficiency: While traditional sliding-window methods suffer from redundant computations on overlapping frames, the MIMO architecture predicts sequences directly within its context window. By leveraging video clipping, lengthy episodic trajectories are partitioned into independent, non-overlapping segments. These segments can be processed concurrently as parallel batches in a single forward pass, significantly accelerating the overall inference process.

2. Sequence Alignment and Padding: For terminal video segments that are shorter than the model’s specified window size, a tail-frame replication padding strategy is applied. During the final aggregation of the full episode, predictions corresponding to these synthetically padded regions are discarded to maintain temporal fidelity.

![[99_Attachments/papers/images/arm/a137d11a7c15a8c792198125314882646c2137f29ea9f515e41daf764e28be62.jpg]]  
Figure 3. Illustration of the tri-state labeling strategy applied to a demonstration episode.

3. Coherent Progress Generation: To generate the global dense progress curve $P _{t}$ , the system mathematically integrates the model-predicted relative state transitions $\Delta \hat{y}$ with the absolute task completion signal $C _{t}$ . Specifically, treating $C _{t}$ as the definitive progress anchor (e.g., $P _{T} = 1 . 0$ at task completion), the dense progress values for preceding frames are reconstructed via accumulation of $\Delta \hat{y}$ .

This pipeline elegantly transforms discrete, local relative predictions into a coherent and dense global progress signal, thereby providing consistent, high-quality supervision for subsequent policy learning.

# 3.4. Policy Optimization via AW-BC

Based on the dense progress signals reconstructed by ARM, we propose Advantage-Weighted Behavior Cloning (AW-BC). This framework prioritizes learning from highadvantage transitions while suppressing suboptimal behaviors through a statistically grounded reweighting mechanism, as illustrated in Fig. 1C.

# 3.4.1. Length-adaptive Gain Formulation

To mitigate the length bias inherent in heterogeneous demonstrations—where drastic variations in episode duration lead to inconsistent progress gradients (e.g., disproportionately steep slopes in shorter sequences)—we introduce an adaptive scaling mechanism. Such gradient volatility often induces instability and jitter in the learning dynamics, hindering smooth weight optimization. For an action chunk with horizon $H$ , the length-adaptive gain $\Delta G _{t}$ is formulated as:

$$
\Delta G _{t} = \left(P _{t + H} - P _{t}\right) \cdot \frac{L _{\text{seq}}}{\bar{L}} \tag{4}
$$

where $P _{t}$ denotes the progress value obtained via global progress reconstruction, $L _{\mathrm { s e q} }$ represents the total length of

the current episode, and $\bar{L}$ is the average episode length across the entire dataset. This normalization ensures that the derived advantage reflects the relative efficiency of a specific action sequence, effectively decoupling the reward signal from the absolute duration of the task.

# 3.4.2. Statistical Weighting and Objective

To convert raw gains into robust training weights, we employ a statistical normalization strategy based on the gain distribution of the current batch. Let $\mu$ and $\sigma$ be the mean and standard deviation of $\{ \Delta G _{i} \}$ . We define clipping bounds as $b _{l o w e r} = \mu - 2 \sigma$ and $b _{u p p e r} = \mu + 2 \sigma$ . The importance weight $\tilde{w} _{i}$ for each sample is computed as:

$$
\tilde{w} _{i} = \operatorname{clamp} \left(\frac{\Delta G _{i} - b _{\text{lower}}}{b _{\text{upper}} - b _{\text{lower}} + \epsilon}, 0, 1\right) \tag{5}
$$

This clamping mechanism effectively filters out regressive data (weights $ ~ 0$ ) while capping the influence of outliers. The final AW-BC objective is to minimize the weighted negative log-likelihood:

$$
\mathcal{L} _{A W - B C} (\theta) = \mathbb{E} _{(s, a) \sim \mathcal{D}} [ - \tilde{w} (s, a) \log \pi_{\theta} (a | s) ] \tag{6}
$$

# 3.4.3. Theoretical Connection to Offline RL

Our proposed formulation aligns with the principles of AWR [28]. Mathematically, this optimization problem can be viewed as maximizing the expected return of the policy under the constraint of remaining close to the behavior policy:

$$
\max _{\theta} \mathbb{E} _{(s, a) \sim \mathcal{D}} \left[ \tilde{w} (s, a) \log \pi_{\theta} (a | s) \right] \tag{7}
$$

Here, ARM functions as a learned Critic, providing the advantage estimate $\Delta G _{t}$ that guides the policy update. By prioritizing transitions with high relative advantage, our

method effectively performs offline policy improvement, extracting an optimal policy from suboptimal demonstrations without explicit online interaction.

# 4. Experiments

# 4.1. Experimental Setup

We evaluate our framework on a challenging, long-horizon bimanual towel-folding task. As illustrated in Fig. 4, a complete and successful demonstration requires a structured 8- stage procedure: (1) extracting exactly one towel from an unstructured, cluttered pile; (2) placing it onto the central tabletop; (3) flattening the towel to a planar initial state; (4) performing a bottom-to-up longitudinal fold; (5) executing a top-to-bottom longitudinal fold; (6) conducting a right-to-center lateral fold; (7) completing the sequence with a left-to-right lateral fold to form a compact rectangle; and (8) transporting and depositing the folded towel fully inside a target storage box on the left. A trial is considered successful only if a single towel is extracted, remains neatly folded, and is fully contained within the box boundaries within a 120-second limit.

![[99_Attachments/papers/images/arm/e47bf1c9c333366e83c4d05098c2fdc3cab437ceb365acdead35483fbe9af4e6.jpg]]  
Figure 4. Overview of the long-horizon towel-folding task. The sequence includes extracting a towel from clutter, placing and flattening it on the table, executing a precise multi-stage folding strategy, and transporting the folded towel into the target box.

Task and Hardware. Data was collected using an AgileX ALOHA [9] bimanual teleoperation system with randomized table heights for enhanced generalization. Detailed implementation details are in the Supplementary Materials.

Dataset Construction and Labeling. We curated a dataset $\mathcal{D} _{a l l}$ of 972 towel-folding episodes (20 hours total), comprising 809 expert demonstrations and 163 DAggeraugmented error-correction episodes. Unlike SARM [6], we retain all trajectories including slow episodes that contain important recovery patterns.

We evaluate three annotation paradigms: (i) VLMbased Labeling implemented in LeRobot [4], using Qwen3-VL [29] for temporal grounding of subtask boundaries; (ii) Manual Subtask Segmentation by human experts; and (iii) our proposed Tri-state Labeling.

Table 1. Quantitative Evaluation of Reward Models. All models are evaluated on a validation set of 50 trajectories. “MSE” measures the trajectory reconstruction fidelity against GT progress (normalized to [0, 1]). The bottom section reports the Success Identification Accuracy, assessing the Completion Head’s ability to correctly classify the final state of Standard (SE, 12 successful episodes), and Failure (FE, 12 failed episodes) trajectories. Best performances are highlighted in bold.

<table><tr><td>Metrics</td><td>SARM</td><td>ARM (Ours)</td></tr><tr><td>MSE ↓</td><td>0.0059</td><td>0.0014</td></tr><tr><td colspan="3">Success Identification Accuracy (%)</td></tr><tr><td>Standard (SE)</td><td>83.3 (10/12)</td><td>100.0 (12/12)</td></tr><tr><td>Failure (FE)</td><td>91.6 (11/12)</td><td>100.0 (12/12)</td></tr></table>

# 4.2. Reward Model Performance

To systematically evaluate the precision and robustness of our proposed reward models, we compare ARM and SARM [6] against the Ground Truth (GT). The evaluation metrics focus on two primary aspects: the numerical accuracy of progress estimation (MSE) and the categorical reliability of trajectory classification.

Quantitative Results. Table 1 summarizes the quantitative results. As expected, ARM demonstrates superior alignment with the GT signals across all evaluation criteria compared to SARM. Notably, ARM achieves a significantly lower MSE (0.0014 vs. 0.0059), representing a substantial improvement in the fidelity of dense progress estimation. Furthermore, ARM achieves perfect success rates in identifying Standard (SE) and Failure (FE) episodes, underscoring its robustness in diverse terminal scenarios.

![[99_Attachments/papers/images/arm/8ab91127c7ceb64390d668389d9bcbf6907ed97c08c3a5de3365962a66b63bfe.jpg]]  
Figure 5. Qualitative comparison of progress reconstruction. We visualize the progress curves of SARM and ARM against the GT for a representative episode. While SARM struggles with nonmonotonic behaviors, ARM reconstructs a smooth, high-fidelity curve that closely tracks the GT, even during regressive adjustments.

![[99_Attachments/papers/images/arm/d500a5cdd861d2d6663338596e452f6e878413ba0b5f7fe30f715bc887a4017c.jpg]]

![[99_Attachments/papers/images/arm/c670e037d9247dde9caca5434dcf4e25e299d41a317943bb50cbdd90afb63fb1.jpg]]  
Figure 6. Qualitative comparison of progress reconstruction. Our tri-state approach generates smoother, more consistent dense progress signals compared to the stepped curves of manual segmentation and VLM methods.

Qualitative Analysis. Fig. 5 visualizes the progress reconstruction differences between SARM and ARM. SARM produces stepped curves with abrupt transitions at subtask boundaries, failing to capture localized regressive movements. In contrast, ARM leverages relative advantage signals to generate smooth, dense progress curves that closely track the ground truth, even during non-monotonic robot adjustments.

# 4.3. Efficiency and Quality of Reward Labeling

A primary bottleneck in scaling reward-guided behavior cloning is the prohibitive cost of human annotation. To evaluate our framework, we conducted a controlled user study with five annotators comparing our Tri-state Advantage Labeling against the Subtask Segmentation protocol (visualized in Fig. 6). We evaluate the labeling process from two dimensions: throughput efficiency and reconstruction quality.

Labeling Throughput and Quality. As shown in Table 3, our tri-state protocol achieves significant efficiency gains. By simplifying annotation from precise temporal boundary localization to discrete classification, human annotators achieve 250 samples per 8-hour shift—a $2 . 5 \times$ speedup over the baseline (100 samples). This simplified formulation enables massive scaling: our Auto Tri-state pipeline processes $> 4 0 0$ , 000 samples per 8 hours, achieving $\mathbf{a} > 1 3 3 \times$ speedup over human baselines.

Beyond efficiency, our approach provides superior signal quality. As shown in Fig. 6, manual and VLM methods produce stepped progress curves with temporal misalignment, while our tri-state labeling $( + 1 , 0 , - 1 )$ yields smooth, dense progress curves when integrated with ARM’s anchor points.

# 4.4. MIMO Architecture Efficiency Analysis

To demonstrate the efficiency advantages of our proposed Multiple-Input Multiple-Output (MIMO) architecture, we conduct an ablation study comparing inference speeds across three distinct approaches: our ARM with MIMO design, traditional MISO VLM labeling using Qwen3-VL, and the baseline SARM model. The results, summarized in Table 4, highlight the substantial computational benefits achieved through our architectural design.

As demonstrated in Table 4, our ARM achieves an inference speed of 14.1 iterations per second (calculated as $2 . 8 2 \times 5$ for the 5-output MIMO configuration), representing a ${ 1 3 . 7 \times }$ speedup over VLM-based labeling (1.03 it/s) and a $\mathbf{3 . 6 \times}$ improvement over SARM (3.9 it/s). This substantial efficiency gain stems from the MIMO architecture’s ability to process multiple advantage predictions simultaneously within a single forward pass, eliminating the computational redundancy inherent in sequential processing approaches.

The efficiency advantage becomes particularly crucial during large-scale deployment, where the ARM model must process extensive trajectory datasets for reward signal generation. While traditional VLM approaches suffer from the overhead of processing each temporal segment independently, our MIMO design leverages shared feature representations to amortize computational costs across multiple outputs, making it highly scalable for real-world robotic learning applications.

# 4.5. Policy Performance Analysis

We evaluate the downstream manipulation performance by comparing three distinct policy configurations based on the GR00T-N1.5-3B [1]:

• (1) Baseline: Standard Behavior Cloning trained on the full dataset $\mathcal{D} _{a l l}$ .   
• (2) RA-BC (GR00T+SARM): Reward-Aligned Behavior Cloning [6] re-weighted by SARM progress signals.   
• (3) AW-BC $\mathbf{( G R 0 0 T + A R M}$ , Ours): Our proposed policy trained via Advantage-Weighted Behavior Cloning, utilizing the dense, relative advantage signals from ARM.

As summarized in Table 2, the Baseline suffers from a suboptimal success rate $( 6 2 . 1 \% )$ and lower operational efficiency. This is primarily due to the multi-modal noise and “sluggish” trajectories inherent in the full dataset, which typical BC fails to filter or prioritize. While RA-BC(GR00T+SARM) improves the success rate to $78 . 5 \%$ through subtask-based weighting, it remains constrained by the lack of fine-grained advantage estimation for errorcorrection behaviors.

Crucially, our framework achieves a near-perfect success rate of $9 9 . 4 \%$ . Beyond reliability, our policy demonstrates superior Task Throughput (32 episodes/hr), significantly outperforming the baselines. This indicates that the

Table 2. Quantitative Comparison of Downstream Policy Performance. We report the success rate, operational task throughput (episodes completed per hour), and folding precision (final edge alignment score; detailed annotation protocol provided in the Supplementary Material) on the long-horizon towel-folding task. Our proposed AW-BC (ARM) framework significantly outperforms both standard Behavior Cloning and prior reward-aware baselines across all metrics.   

<table><tr><td>Method</td><td>Success Rate (%)</td><td>Task Throughput (Episodes / hr)</td><td>Folding Precision (Score)</td></tr><tr><td>BC-Baseline (GR00T N1.5)</td><td>62.1</td><td>18</td><td>2.2</td></tr><tr><td>RA-BC (GR00T + SARM)</td><td>78.5</td><td>24</td><td>2.7</td></tr><tr><td>AW-BC (GR00T + ARM)</td><td>99.4</td><td>32</td><td>3.6</td></tr></table>

Table 3. Labeling Efficiency Comparison. Annotation throughput comparison between human and automated labeling protocols per 8-hour shift.   

<table><tr><td>Annotation Protocol</td><td>Rate (Samples/8h)</td></tr><tr><td>Human Baseline (Seg.)†</td><td>100</td></tr><tr><td>Human Tri-state (Ours)†</td><td>250</td></tr><tr><td>VLM (Qwen3-VL)‡</td><td>~ 3000</td></tr><tr><td>Auto Tri-state (Ours)‡</td><td>&gt; 400,000</td></tr></table>

† Per single human annotator.   
‡ Inference throughput on a single NVIDIA A100 GPU.

Table 4. MIMO Architecture Efficiency Comparison. We evaluate the inference throughput across different reward modeling approaches. ARM is evaluated with its MIMO design handling 5 parallel outputs per input, VLM labeling represents traditional single-input approaches, and SARM serves as the baseline. All measurements are conducted on a single NVIDIA A100 GPU under comparable conditions.   

<table><tr><td>Method</td><td>Architecture</td><td>Throughput (it/s)</td></tr><tr><td>Qwen3-VL</td><td>MISO</td><td>1.03</td></tr><tr><td>SARM Baseline</td><td>SISO</td><td>3.9</td></tr><tr><td>ARM (Ours)</td><td>MIMO</td><td>14.1</td></tr></table>

advantage-weighted objective effectively prioritizes highquality, decisive movements, resulting in more agile and purposeful trajectories. Furthermore, our method achieves the highest Folding Precision (3.6), as the dense reward signal provides finer supervision for the critical multi-stage alignment required in towel folding.

Ablation Study. To isolate the contributions of our key innovations, we evaluate three configurations through pairwise comparisons, as shown in Table 5.

The results reveal the impact of each component through direct comparisons.

Table 5. Ablation Study. We systematically evaluate the contributions of tri-state labeling and AW-BC training through three key configurations.   

<table><tr><td>Method</td><td>Task Seg.</td><td>Tri-state</td><td>RA-BC</td><td>AW-BC</td><td>Success Rate (%)</td></tr><tr><td>SARM</td><td>✓</td><td>-</td><td>✓</td><td>-</td><td>78.5</td></tr><tr><td>ARM</td><td>-</td><td>✓</td><td>✓</td><td>-</td><td>92.3</td></tr><tr><td>ARM</td><td>-</td><td>✓</td><td>-</td><td>✓</td><td>99.4</td></tr></table>

Tri-state vs. Task Segmentation: Comparing SARM with ARM (Tri-state $^ +$ RA-BC) shows tri-state labeling improves success rate from $78 . 5 \%$ to $9 2 . 3 \%$ $( + 1 3 . 8 \% )$ , demonstrating superior annotation quality and efficiency.

AW-BC vs. RA-BC: Comparing ARM (Tri-state + RA-BC) with ARM (Tri-state $^ +$ AW-BC) shows our advantageweighted training dramatically improves success rate from $9 2 . 3 \%$ to $9 9 . 4 \%$ $( + 7 . 1 \% )$ , highlighting the effectiveness of dense advantage signals.

Our complete ARM framework achieves $+ 2 0 . 9 \%$ improvement over SARM, demonstrating strong synergy between tri-state labeling and AW-BC training.

# 5. Conclusion

We propose Advantage Reward Model (ARM), a framework that addresses the reward engineering bottleneck in long-horizon robotic manipulation tasks. By modeling relative advantages, ARM overcomes inconsistency and high costs of traditional dense labeling. We introduce a tristate labeling strategy that reduces cognitive load for annotators while providing high-fidelity supervision signals and enabling automated labeling. In a challenging towelfolding task, ARM with Advantage-Weighted Behavior Cloning achieves a $9 9 . 4 \%$ success rate, outperforming existing Vision-Language-Action baselines. ARM provides a scalable and robust solution for training high-performance policies.

# References

[1] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. arXiv preprint arXiv:2503.14734, 2025. 1, 7   
[2] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. $\pi _{0}$ : A vision-languageaction flow model for general robot control. arXiv preprint arXiv:2410.24164, 2024. 1   
[3] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. arXiv preprint arXiv:2503.06669, 2025. 1   
[4] Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, Steven Palma, Pepijn Kooijmans, Michel Aractingi, Mustafa Shukor, Dana Aubakirova, Martino Russi, Francesco Capuano, Caroline Pascal, Jade Choghari, Jess Moss, and Thomas Wolf. Lerobot: State-ofthe-art machine learning for real-world robotics in pytorch. https://github.com/huggingface/lerobot, 2024. 6   
[5] Letian Chen, Nina Marie Moorman, and Matthew Craig Gombolay. ELEMENTAL: Interactive learning from demonstrations and vision-language models for reward design in robotics. In Forty-second International Conference on Machine Learning, 2025. 3   
[6] Qianzhong Chen, Justin Yu, Mac Schwager, Pieter Abbeel, Yide Shentu, and Philipp Wu. Sarm: Stage-aware reward modeling for long horizon robot manipulation, 2025. 1, 2, 3, 6, 7   
[7] Shirui Chen, Cole Harrison, Ying-Chun Lee, Angela Jin Yang, Zhongzheng Ren, Lillian J. Ratliff, Jiafei Duan, Dieter Fox, and Ranjay Krishna. Topreward: Token probabilities as hidden zero-shot rewards for robotics, 2026. 3   
[8] Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep reinforcement learning from human preferences. In Advances in Neural Information Processing Systems. Curran Associates, Inc., 2017. 2   
[9] Zipeng Fu, Tony Z Zhao, and Chelsea Finn. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. arXiv preprint arXiv:2401.02117, 2024. 6   
[10] Chengkai Hou et al. Robomind 2.0: A multimodal, bimanual mobile manipulation dataset for generalizable embodied intelligence. arXiv preprint arXiv:2512.24653, 2025. 1   
[11] Zheyuan Hu, Robyn Wu, Naveen Enock, Jasmine Li, Riya Kadakia, Zackory Erickson, and Aviral Kumar. Rac: Robot learning for long-horizon tasks by scaling recovery and correction. arXiv preprint arXiv:2509.07953, 2025. 2   
[12] Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, et al.

$\pi _{0 . 6} ^{*}$ : A VLA that learns from experience. arXiv preprint arXiv:2511.14759, 2025. 1   
[13] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. π0.5: a vision-language-action model with open-world generalization, 2025. 1   
[14] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. arXiv preprint arXiv:2403.12945, 2024. 1   
[15] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246, 2024. 1   
[16] Ilya Kostrikov, Ashvin Nair, and Sergey Levine. Offline reinforcement learning with implicit q-learning, 2021. 3   
[17] Tony Lee, Andrew Wagenmaker, Karl Pertsch, Percy Liang, Sergey Levine, and Chelsea Finn. Roboreward: Generalpurpose vision-language reward models for robotics, 2026. 3   
[18] Yunfei Li, Xiao Ma, Jiafeng Xu, Yu Cui, Zhongren Cui, Zhigang Han, Liqun Huang, Tao Kong, Yuxiao Liu, Hao Niu, et al. Gr-rl: Going dexterous and precise for long-horizon robotic manipulation. arXiv preprint arXiv:2512.01801, 2025. 1   
[19] Anthony Liang, Yigit Korkmaz, Jiahui Zhang, Minyoung Hwang, Abrar Anwar, Sidhant Kaushik, Aditya Shah, Alex S Huang, Luke Zettlemoyer, Dieter Fox, et al. Robometer: Scaling general-purpose robotic reward models via trajectory comparisons. arXiv preprint arXiv:2603.02115, 2026. 1   
[20] Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, and Piotr Dollár. Focal loss for dense object detection, 2018. 4   
[21] Yecheng Jason Ma, Shagun Sodhani, Dinesh Jayaraman, Osbert Bastani, Vikash Kumar, and Amy Zhang. Vip: Towards universal visual reward and representation via value-implicit pre-training. arXiv preprint arXiv:2210.00030, 2022. 2, 3   
[22] Yecheng Jason Ma, Vikash Kumar, Amy Zhang, Osbert Bastani, and Dinesh Jayaraman. Liv: Language-image representations and rewards for robotic control. In International Conference on Machine Learning, pages 23301–23320. PMLR, 2023. 2   
[23] Yecheng Jason Ma, Joey Hejna, Ayzaan Wahid, Chuyuan Fu, Dhruv Shah, Jacky Liang, Zhuo Xu, Sean Kirmani, Peng Xu, Danny Driess, Ted Xiao, Jonathan Tompson, Osbert Bastani, Dinesh Jayaraman, Wenhao Yu, Tingnan Zhang, Dorsa

Sadigh, and Fei Xia. Vision language models are in-context value learners, 2024. 1, 3   
[24] Ashvin Nair, Abhishek Gupta, Murtaza Dalal, and Sergey Levine. Awac: Accelerating online reinforcement learning with offline datasets, 2021. 3   
[25] Andrew Y. $\mathrm { N g }$ and Stuart J. Russell. Algorithms for inverse reinforcement learning. In Proceedings of the Seventeenth International Conference on Machine Learning, page 663–670, San Francisco, CA, USA, 2000. Morgan Kaufmann Publishers Inc. 2   
[26] Takayuki Osa, Joni Pajarinen, Gerhard Neumann, J. Andrew Bagnell, Pieter Abbeel, and Jan Peters. An algorithmic perspective on imitation learning. Foundations and Trends® in Robotics, 7(1–2):1–179, 2018. 1   
[27] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In 2024 IEEE International Conference on Robotics and Automation (ICRA), pages 6892–6903. IEEE, 2024. 1   
[28] Xue Bin Peng, Aviral Kumar, Grace Zhang, and Sergey Levine. Advantage-weighted regression: Simple and scalable off-policy reinforcement learning, 2019. 3, 5   
[29] QwenLM. Qwen3-vl. https : / / github . com / QwenLM/Qwen3-VL, 2025. GitHub repository, accessed 2025-11-09. 6   
[30] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision, 2021. 4   
[31] Stephane Ross, Geoffrey J. Gordon, and J. Andrew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning, 2011. 2   
[32] Sumedh Sontakke, Jesse Zhang, Séb Arnold, Karl Pertsch, Erdem Bıyık, Dorsa Sadigh, Chelsea Finn, and Laurent Itti. Roboclip: One demonstration is enough to learn robot policies. Advances in Neural Information Processing Systems, 36:55681–55693, 2023. 1   
[33] Richard S Sutton and Andrew G Barto. Reinforcement learning: An introduction. MIT press, second edition, 2018. 1   
[34] Huajie Tan, Sixiang Chen, Yijie Xu, Zixiao Wang, Yuheng Ji, Cheng Chi, Yaoxu Lyu, Zhongxia Zhao, Xiansheng Chen, Peterson Co, Shaoxuan Xie, Guocai Yao, Pengwei Wang, Zhongyuan Wang, and Shanghang Zhang. Robo-dopamine: General process reward modeling for high-precision robotic manipulation, 2025. 1, 3   
[35] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe Hansen-Estruch, Quan Vuong, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale, 2024. 1   
[36] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, et al. Robomind: Benchmark on multiembodiment intelligence normative data for robot manipulation. In Robotics: Science and Systems, 2025. 1

[37] Yanru Wu, Weiduo Yuan, Ang Qi, Vitor Guizilini, Jiageng Mao, and Yue Wang. Large reward models: Generalizable online robot reward generation with vision-language models, 2026. 1   
[38] Shaopeng Zhai, Qi Zhang, Tianyi Zhang, Fuxian Huang, Haoran Zhang, Ming Zhou, Shengzhe Zhang, Litao Liu, Sixu Lin, and Jiangmiao Pang. A vision-language-action-critic model for robotic real-world reinforcement learning. arXiv preprint arXiv:2509.15937, 2025. 2   
[39] Jiahui Zhang, Yusen Luo, Abrar Anwar, Sumedh Anand Sontakke, Joseph J Lim, Jesse Thomason, Erdem Biyik, and Jesse Zhang. Rewind: Language-guided rewards teach robot policies without new demonstrations, 2025. 1, 3

# Author Contributions

Yiming Mao is the primary architect of the ARM framework and spearheaded its development from the ground up. He designed the core algorithms, performed comprehensive hardware-software debugging. He conducted the entirety of the robotic manipulation experiments, managed the complete data engineering workflow, and drafted the original manuscript.

Zixi Yu contributed to manuscript drafting, prepared the technical illustrations and figures, and assisted in the replication of baseline methods.

Weixin Mao served as the Project Leader, providing overall supervision and strategic steering of the research direction. He played a key role in the intellectual refinement of the framework and critically revised the manuscript to ensure its technical and academic rigor.

Yinhao Li provided the initial software infrastructure and codebase.

Qirui Hu assisted with the maintenance and debugging of the robot hardware.

Zihan Lan contributed to the data parsing scripts.

Minzhao Zhu participated in technical discussions and provided general support.

Hua Chen provided administrative support and coordinated the research resources.

# A. VLM Prompting Details

For the towel-folding task, the subtask vocabulary is:

1. Extracting exactly one towel from an unstructured, cluttered pile;   
2. Placing it onto the central tabletop;   
3. Flattening the towel to a planar initial state;   
4. Performing a bottom-to-up longitudinal fold;   
5. Executing a top-to-bottom longitudinal fold;   
6. Conducting a right-to-center lateral fold;   
7. Completing the sequence with a left-to-right lateral fold to form a compact rectangle;   
8. Transporting and depositing the folded towel fully inside a target storage box on the left.

The effective prompt is:

# Role

You are a Robotics Vision System specializing in temporal action localization for robot manipulation. Your job is to segment a single demonstration video into distinct, non-overlapping atomic actions from a fixed label list.

# Label Set (Closed Vocabulary)

You must strictly identify the video segments using ONLY the provided

labels. Do not create new labels or modify existing ones.

The video shows execution of all actions in logical orders.

# Ground-Truth Semantics

Use visual state changes to define when an action starts and ends. Do NOT assume equal durations for the stages.

- An action starts at the first frame where the robot’s motion clearly initiates that action.   
- An action ends at the first frame where that specific action is visually completed and the manipulated object reaches a temporary, stable configuration.   
- Short pauses or ambiguous micro-motions should be assigned to the current action.

# Constraints

1. The full video from $" 0 0 : 0 0 "$ to the final timestamp must be covered without gaps.   
2. The end timestamp of one stage must equal the start timestamp of the next stage.   
3. Each stage appears exactly once and in logical order.   
4. Uniform or near-uniform segmentation should be avoided unless the video genuinely supports it.   
5. Timestamps must be in “MM:SS” format; the first stage starts at $" 0 0 : 0 0 "$ .

# Step 1 -- Textual Timeline

First, write a detailed textual timeline with approximate timestamps. For each stage, include its name, approximate start and end time, and the visual event that defines the boundary.

# Step 2 -- Structured Output

Then output only valid JSON consistent with the timeline above, using the exact labels and timestamps without adding extra keys.

In the implementation, this prompt is provided as a system instruction, while the user message contains the episode video and a short duration hint formatted as “Video is MM:SS (∼xx.xs). Follow instructions.” The resulting VLM output is parsed into stage names with start and end timestamps and then written into the dense subtask annotation fields of the dataset.

# B. Implementation Details

Our framework consists of two primary components: the Advantage Reward Model (ARM) and the Policy Model, both of which leverage high-capacity pre-trained backbones but are optimized for distinct objectives.

Reward Model (ARM) Training. ARM utilizes a pretrained CLIP ViT-B/32 as the vision-text encoder, followed by a Transformer-based Sequential Aggregator with a causal 5-frame window (sampled at 1Hz). The joint objective is defined as $\mathcal{L} _{\mathrm { A R M} } = \lambda _{\mathrm { i n t} } \mathcal{L} _{\mathrm { i n t} } + \lambda _{\mathrm { s u c c} } \mathcal{L} _{\mathrm { s u c c} }$ , where we employ Focal Loss for task completion and cross-entropy for tri-state interval classification. Complete hyperparameters are summarized in Table 6.

Policy Training (AW-BC). Based on the GR00T-N1.5 VLA foundation, our policy uses Advantage-Weighted Behavior Cloning where sample weights $w$ are derived from ARM-predicted gains $\Delta G _{t}$ . Training configurations are detailed in Table 7.

Table 6. ARM Training Hyperparameters. Complete hyperparameter settings for training the Advantage Reward Model.   

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Vision Encoder</td><td>CLIP ViT-B/32</td></tr><tr><td>Sequential Aggregator</td><td>5 frames (1Hz sampling)</td></tr><tr><td>Window</td><td></td></tr><tr><td>Training Epochs</td><td>2</td></tr><tr><td>Hardware Configuration</td><td>2 × NVIDIA A100 GPUs</td></tr><tr><td>Effective Batch Size</td><td>64</td></tr><tr><td colspan="2">Optimization Configuration</td></tr><tr><td>Optimizer</td><td>AdamW</td></tr><tr><td>Learning Rate (LR)</td><td>5 × 10-5</td></tr><tr><td>Weight Decay (WD)</td><td>10-3</td></tr><tr><td>LR Warmup Steps</td><td>1,000</td></tr><tr><td>LR Schedule</td><td>Cosine Decay</td></tr><tr><td>Mixed Precision</td><td>FP16</td></tr><tr><td colspan="2">Loss Function Configuration</td></tr><tr><td>Interval Loss Weight (λint)</td><td>1.0</td></tr><tr><td>Success Loss Weight (λsucc)</td><td>1.0</td></tr><tr><td>Focal Loss γ</td><td>2.0</td></tr><tr><td>Focal Loss α</td><td>2.0</td></tr><tr><td>Focal Loss ε</td><td>10-3</td></tr></table>

# C. ARM Inference Results

To evaluate the qualitative performance of our model, we visualize the ARM inference results on a held-out test trajectory, as shown in Fig. 7. The model is required to re-

Table 7. Policy Training Hyperparameters. Complete hyperparameter settings for Advantage-Weighted Behavior Cloning using the GR00T-N1.5 foundation model.   

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Foundation Model</td><td>GR00T-N1.5 (3B parameters)</td></tr><tr><td>Policy Head</td><td>Diffusion Transformer (DiT) Flow Matching</td></tr><tr><td>Action Dimension</td><td>14D bimanual actions</td></tr><tr><td>Action Horizon (H)</td><td>32</td></tr><tr><td>Camera Views</td><td>3 × 224 × 224 (head + wrists)</td></tr><tr><td>Training Epochs</td><td>7</td></tr><tr><td>Hardware Configuration</td><td>32 × NVIDIA A100 GPUs</td></tr><tr><td>Parallelization Strategy</td><td>FSDP (Fully Sharded Data Parallel)</td></tr><tr><td colspan="2">Optimization Configuration</td></tr><tr><td>Batch Size</td><td>256</td></tr><tr><td>Learning Rate</td><td>2 × 10-5(constant)</td></tr><tr><td>Mixed Precision</td><td>BF16</td></tr><tr><td>Gradient Clipping</td><td>1.0</td></tr><tr><td colspan="2">Advantage Weighting Configuration</td></tr><tr><td>Weight Clipping Range</td><td>[0, 1]</td></tr><tr><td>Positive Threshold</td><td>w=1</td></tr><tr><td>(ΔGt&gt;0.01)</td><td></td></tr><tr><td>Non-positive Threshold</td><td>w=0</td></tr><tr><td>(ΔGt≤0)</td><td></td></tr><tr><td colspan="2">Inference Configuration</td></tr><tr><td>Flow Matching Denoising</td><td>4</td></tr><tr><td>Steps</td><td></td></tr></table>

construct a dense progress signal for a long-horizon towelfolding sequence characterized by non-monotonic behaviors.

Tracking Regressive Behaviors. A critical observation in the inference results is ARM’s sensitivity to physical regressions. Between $t = 6 5 s$ and $t = 7 5 s$ , the robot performs a localized adjustment of the towel’s edge to prepare for the final fold. This action, while necessary, temporarily moves the state further from the target rectangular configuration.

As captured in the transition from $t ~ = ~ 6 9 \mathrm { s }$ $P _{\mathrm { p r e d} } =$ $8 6 . 1 5 \%$ ) to $t = 7 0 \mathrm { s }$ ( $P _{\mathrm { p r e d} } = 8 4 . 6 2 \% )$ , the Multi-frame Advantage head successfully identifies this trend, consistently predicting regressive signals ( $\Delta _{\mathrm { p r e d} } = - 1$ , as shown in the status text). This causes the reconstructed progress curve (blue line) to exhibit a precise downward “dip” that closely aligns with the ground truth (green line).

Figure 7. Visualization of ARM Inference Results. The left panels show the third-person view of the bimanual towel-folding task at $t = 6 9 s$ and $t = 7 0 s$ . The right panels display the corresponding progress curves: predicted progress $P _{p r e d}$ (blue) and ground truth $P _{g t}$ (green). ARM accurately captures the non-monotonic progress “dip” caused by a regressive adjustment, with the Multiframe Advantage head correctly outputting $\Delta _{\mathrm { p r e d} } = - 1$ .

High-Fidelity Signal Reconstruction. Despite the complexity of the 14-dimensional bimanual action space and the deformable nature of the towel, ARM maintains high temporal consistency throughout the inference process. The predicted curve is smooth and free from the cumulative drift or “stepped” artifacts common in subtask-based approaches. This high-fidelity inference result demonstrates that ARM can provide the downstream policy with accurate, real-time feedback, penalizing regressive movements and rewarding only those that effectively contribute to task completion.

# D. Real-World Implementation Details

Hardware Setup. The real-world data collection and policy deployment were conducted using an AgileX masterslave teleoperation system (illustrated in Fig. 8). The hardware platform utilizes a 6-Degree-of-Freedom (6-DoF) bimanual robot configuration.

Figure 8. Hardware setup for real-world experiments. The system features a 6-DoF bimanual robot configuration controlled via an AgileX master-slave teleoperation interface. It is equipped with a global base camera and two wrist-mounted cameras to capture comprehensive visual observations alongside the 14-dimensional proprioceptive data.

Observation and Action Space. To provide rich multimodal representations for both the ARM and downstream policies, the system integrates three distinct RGB camera perspectives: a High View to capture the global context of the workspace, alongside Left and Right Wrist Views for egocentric, contact-rich visual feedback. Furthermore, both the proprioceptive state and the action space are 14- dimensional, comprising the continuous joint positions and gripper states of the bimanual manipulators.

# E. Folding Precision Evaluation Protocol

We define a quantitative folding precision score ranging from 0 to 5 to evaluate the quality of towel folding results:

• 5 points: The folding task is fully completed, with a folding precision within $1 \mathrm { c m }$ .   
• 4 points: The folding task is fully completed, with a folding precision between 1 cm and $2 \mathrm { c m }$ .   
• 3 points: The folding task is fully completed, with a folding precision between 2 cm and $3 \mathrm { c m }$ .   
• 2 points: The towel is successfully flattened, but the final folding is not completed, though partial folding steps are finished.   
• 1 point: The towel is successfully flattened, but no valid folding steps are performed.   
• 0 points: No task steps are successfully completed.