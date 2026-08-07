# Ego2Robot: Scalable Robot Data Synthesis from Egocentric Human Data

Ye Wang<sup>1,2,∗</sup>, Pei Lin<sup>2,3,4,∗</sup>, Xiong-Hui Chen<sup>2,∗</sup>, Haoqi Yuan<sup>2</sup>, Zhixuan Liang<sup>2</sup>, Yiyang Huang<sup>2</sup>, Anzhe Chen<sup>2</sup>, Zixing Lei<sup>2</sup>, Jie Zhang<sup>2</sup>, Tao Zhang<sup>1</sup>, Haoyang Li<sup>2</sup>, Tong Zhang<sup>2</sup>, Chenxi Xiao<sup>3</sup>, Ziyuan Jiao<sup>4,5</sup>, Qin Jin<sup>1,†</sup>

<sup>1</sup>AIM3 Lab, Renmin University of China <sup>2</sup>Qwen Team, Alibaba Inc.

<sup>3</sup>ShanghaiTech University <sup>4</sup>Beijing Institute for General Artificial Intelligence (BIGAI)

<sup>5</sup>Beijing University of Aeronautics and Astronautics

<sup>∗</sup>Equal contribution <sup>†</sup>Corresponding author

Abstract: Learning generalizable robot manipulation policies requires large-scale and diverse demonstration data. Egocentric human manipulation videos offer rich scene and task diversity, and prior work has shown that retargeting and rendering such videos into robot-format data can yield effective per-task policies at small scale. However, whether this approach can provide pretraining benefits for visionlanguage-action models at scale remains unexplored. We present Ego2Robot, a scalable pipeline that converts egocentric human manipulation videos into robot training data through action retargeting, robot-arm visual synthesis, and multilevel quality curation. Ego2Robot supports both curated datasets and in-the-wild videos, producing 18,561 hours of robot training data spanning 15 robot morphologies, making it the largest ego-to-robot dataset to date. To evaluate generalization, we extend RoboTwin2.0 with disentangled perturbation axes covering visual appearance, scene layout, embodiment morphology, and task semantics. Experiments show that joint pretraining on Ego2Robot-synthesized and robot data consistently improves out-of-distribution generalization across multiple perturbation types, with benefits validated on real-robot deployment. Project page: https://www-ye.github.io/ego2robot\_blog/

Keywords: Robot Data Synthesis, Egocentric Data, Generalization Evaluation

## 1 Introduction

Recent vision-language-action (VLA) models [1, 2, 3, 4, 5] have demonstrated impressive progress in robot manipulation through large-scale robot demonstration pretraining. However, the generalization ability of these systems remains fundamentally constrained by the scale and diversity of available robot data. Despite major efforts such as Open X-Embodiment [6], DROID [7], and AgibotWorld [8], collecting robot demonstrations remains expensive, labor-intensive, and limited by hardware availability, teleoperation cost, and restricted interaction diversity [9, 10, 11].

Egocentric human videos offer a compelling alternative. Compared with robot teleoperation, human hand interactions can be collected at massive scale across diverse objects, environments, and task variations [12, 13]. These videos capture rich manipulation priors that are difficult to obtain with robots alone. However, directly converting egocentric videos into robot training data remains challenging due to the substantial gap between human and robot embodiments. One promising direction is to retarget hand motions to robot kinematics and visually replace human arms with rendered robot embodiments, which has shown strong per-task results at small scale [14, 15]. Whether large-scale ego2robot-synthesized data can serve as effective pretraining data for robot policies, particularly for improving out-of-distribution generalization, remains largely unexplored.

In this work, we investigate ego-to-robot synthesis as a scalable paradigm for robot policy pretraining. Our key hypothesis is that, despite embodiment differences, egocentric manipulation videos contain transferable interaction regularities that can complement robot data if properly aligned. Based on this observation, we propose Ego2Robot, an end-to-end pipeline that converts egocentric human manipulation data into embodiment-specific robot training data through action alignment, visual alignment, and multi-level quality curation (Figure 1). The pipeline supports both annotated ego datasets and pure ego videos, and processes approximately 1,940 hours of egocentric video from four diverse sources across 15 robot morphologies, producing 18,561 hours of effective robot training data, to the best of our knowledge the largest ego-to-robot dataset to date.

![](../../99_Attachments/papers/images/ego2robot/88ed1db513f12ca26b55b578bdf69026fbe890036fc661513d4481c1bd73f65e.jpg)  
Figure 1: Ego2Robot pipeline. Converting egocentric video into 18,561h robot training data across 15 morphologies through action alignment, visual alignment, and quality curation.

To evaluate whether ego2robot-synthesized data improves robot generalization, we further introduce a disentangled evaluation protocol built on RoboTwin2.0 [16]. Unlike prior evaluations that aggregate multiple distribution shifts into a single score, our protocol decouples perturbations across four axes: visual appearance, scene layout, embodiment morphology, and task semantics. This enables fine-grained analysis of where pretraining with a combination of robot and ego2robot-synthesized data provides benefits and whether the gains arise from visual robustness, embodiment transfer, or semantic generalization. Extensive experiments show that ego2robot-synthesized data consistently improves out-of-distribution performance and provides complementary value to robot data. In particular, the gains are most pronounced under visual, embodiment, and semantic perturbations, suggesting that large-scale ego2robot-synthesized data primarily improves invariance and crossdistribution robustness rather than merely increasing trajectory coverage.

Our contributions are as follows: (1) We propose Ego2Robot, a complete ego-to-robot synthesis pipeline with action alignment, visual alignment, and multi-level quality curation, supporting 15 robot morphologies. (2) We construct the largest ego-to-robot dataset to date, containing 18,561 hours of synthesized robot training data generated from diverse egocentric video sources. (3) We introduce a disentangled generalization benchmark that separates visual, scene, embodiment, and semantic perturbations for fine-grained evaluation of robot policy robustness. (4) We demonstrate that combining ego2robot-synthesized data with pure robot data improves generalization performance, particularly under out-of-distribution shifts.

## 2 Related Work

Robot Data Scaling and Learning from Human Data Scaling robot demonstration data is central to generalizable manipulation. Large-scale robot datasets [6, 7, 8] and portable collection systems [10, 11, 9, 17, 18] have expanded available demonstrations, but diversity remains constrained by collection cost and hardware scalability. Human manipulation videos provide a broader alternative, motivating work on visual pretraining [19, 20, 21], reward learning [22], motion priors [23], and point tracking [24, 25], though these methods still rely on robot data to bridge embodiment gaps.

More direct approaches leverage human data for robot policy learning. One line of work co-trains on egocentric or human video alongside robot data [15, 26, 27, 28, 29], while another converts human demonstrations into robot-format data through retargeting and rendering [14, 30] or embodiment masking [15]. However, the retarget-and-render approach has only been studied at limited scale or for individual tasks. Our work scales it to 18,561 hours across 15 robot morphologies and systematically evaluates its benefit for VLA pretraining and out-of-distribution generalization.

Data Augmentation for Robot Learning Data augmentation expands training diversity without additional robot collection. Simulation-based methods [31, 32] generate synthetic demonstrations in digital twins, while cross-embodiment methods including RoviAug [33], Mirage [34] and OXE-AugE [35] bridge robot-to-robot visual gaps through inpainting and image editing. Unlike these approaches, our work extends augmentation to the substantially larger ego-to-robot domain gap, leveraging egocentric human videos to synthesize training data for 15 robot morphologies and sys tematically evaluating generalization across multiple perturbation axes.

Benchmarks for Robot Generalization Existing manipulation benchmarks such as RoboTwin [36, 16], LIBERO [37], CALVIN [38], RLBench [39], and SIMPLER [40] evaluate policy generalization under bundled perturbations, making it difficult to attribute failures to specific factors. ManiSkill2/3 [41, 42] and RoboCasa [32] support multiple robot configurations but lack standardized cross-embodiment evaluation. Recent decomposed benchmarks, including Colosseum [43], LIBERO-Plus [44], and LIBERO-PRO [45], separate perturbation axes and show that VLA models degrade substantially under individual shifts, but remain limited to single-arm settings. RoboTwin 2.0 [16] and EBench [46] evaluate dual-arm manipulation yet still primarily report bundled results. We extend RoboTwin2.0 with independent perturbation axes spanning visual appearance, scene layout, embodiment, and task semantics, while jointly supporting dual-arm and cross-embodiment evaluation.

## 3 Ego2Robot Pipeline

Given egocentric videos depicting human hand manipulation, our pipeline produces embodimentspecific robot training data through three stages: action alignment, visual alignment, and quality curation (Figure 1). Action alignment converts hand poses into robot end-effector trajectories via retargeting and temporal smoothing. Visual alignment replaces human arms with rendered robot arms through arm segmentation, hand removal, robot base pose search with IK solving, and depthaware rendering. Quality curation then filters samples at the trajectory, frame, and episode levels. The pipeline supports two input paths: Path A accepts ego datasets with existing hand pose annotations, while Path B processes unannotated videos by first estimating hand poses via WiLoR [47, 48] per-frame reconstruction and DynHaMR [49] temporal optimization. For long videos, we adopt Qwen3.5 [50] to segment continuous recordings into discrete subtasks with natural language descriptions. After hand pose estimation, both paths share a unified pipeline that generates training data for any of 15 supported robot morphologies in parallel.

1. Action Alignment The action alignment stage converts hand poses into parallel-gripper endeffector trajectories through retargeting and temporal smoothing.

Hand-to-Gripper Retargeting. For each frame with a detected hand, we extract a compact gripper representation from the 21 hand keypoints. We define a virtual fingertip as a weighted blend of the index and middle finger tips:

$$
\mathbf {p} _ {\mathrm{vf}} = 0. 7 \cdot \mathbf {p} _ {\mathrm{index}} + 0. 3 \cdot \mathbf {p} _ {\mathrm{middle}}\tag{1}
$$

The tool center point (TCP) and gripper opening width are:

$$
\mathbf {p} _ {\mathrm{tcp}} = \frac {\mathbf {p} _ {\mathrm{thumb}} + \mathbf {p} _ {\mathrm{vf}}}{2}, \quad w = \| \mathbf {p} _ {\mathrm{thumb}} - \mathbf {p} _ {\mathrm{vf}} \|\tag{2}
$$

The grasp orientation is a right-handed orthonormal frame $\mathbf { R } \ = \ [ \mathbf { x } \textbf { y z } ]$ . The grasp axis z lies along the jaw line (thumb tip to virtual fingertip); together with the wrist-to-fingertip direction $\mathbf { d } =$ $\mathbf { p } _ { \mathrm { v f } } - \mathbf { p } _ { \mathrm { w r i s t } }$ it spans the jaw plane, whose normal is the gripper-normal axis ${ \bf y } ;$ the approach axis x completes the frame:

$$
\mathbf {z} = \frac {s (\mathbf {p} _ {\mathrm{thumb}} - \mathbf {p} _ {\mathrm{vf}})}{w}, \quad \mathbf {y} = \frac {\mathbf {z} \times \mathbf {d}}{\| \mathbf {z} \times \mathbf {d} \|}, \quad \mathbf {x} = \mathbf {y} \times \mathbf {z}\tag{3}
$$

where $s ~ = ~ + 1$ for the right hand and $s ~ = ~ - 1$ for the left hand, so that z points consistently regardless of handedness and both hands map to the same gripper frame. The three axes are: $\mathbf { x } -$ approach direction, $\mathbf { y } - \mathrm { g r i p p e r }$ normal (perpendicular to the jaw plane), z – grasp axis (along the jaw line).

Temporal Smoothing. Per-frame hand detection introduces high-frequency noise. We apply Savitzky-Golay filtering to positions and widths, and Gaussian-weighted SLERP to orientations, producing smooth trajectories while preserving motion structure.

Action Speed Alignment. Egocentric hand manipulation exhibits significantly higher action speeds than robot teleoperation data. To align the speed distributions, we apply per-source frame subsampling during training: ANT and EgoDex are downsampled to 60% of their original frame rate (∼1.7× slower), EgoVerse to 45% $( \sim 2 . 2 \times$ slower), and ViTRA to 25% (∼4× slower).

2. Visual Alignment Visual alignment transforms ego video from depicting human hands to showing a robot arm operating in the same scene.

Arm Segmentation. We employ SAM 3 [51] to segment human arm regions in each frame, providing temporally consistent masks across frames.

Hand Removal. With the arm masks, ProPainter [52] performs temporally consistent video inpainting to remove the human arms and reconstruct the background.

Robot Base Pose Search. A fundamental challenge in converting ego videos to robot data is determining the robot base placement. Unlike robot-to-robot transfer where a source base position is available, egocentric hand trajectories are embodiment-free: there is no physical robot base to reference. We must find a base pose $\mathbf { T } _ { \mathrm { b a s e } } = ( \mathbf { t } , \mathbf { R } ) \in S E ( 3 )$ such that the retargeted trajectory remains kinematically feasible for the target robot morphology.

We formulate this as an optimization over base placements. Given a trajectory of $N$ target endeffector poses $\{ \mathbf { T } _ { i } ^ { \mathrm { e e } } \} _ { i = 1 } ^ { N }$ and a robot with maximum reach $r _ { \mathrm { m a x } }$ , we seek:

$$
\mathbf {T} _ {\text { base }} ^ {*} = \arg \max _ {\mathbf {T} _ {\text { base }}} \frac {1}{| \mathcal {K} |} \sum_ {k \in \mathcal {K}} \nVdash \left[ \mathrm{IK} (\mathbf {T} _ {\text { base }} ^ {- 1} \mathbf {T} _ {k} ^ {\mathrm{ee}}) \text {   is   feasible } \right]\tag{4}
$$

where ${ \mathcal { K } } \subset \{ 1 , \ldots , N \}$ is a set of representative keyframes selected to cover the spatial extremes of the trajectory (positions with maximum displacement or orientation change), and $\operatorname { I K } ( \cdot )$ denotes an inverse kinematics solver in MuJoCo [53, 54]. Candidate base placements are generated via grid search around the trajectory centroid, constrained by the per-morphology kinematic reach $r _ { \mathrm { m a x } }$ . Each candidate is validated by solving IK at all keyframes, and the placement with the highest feasibility rate is selected. This search is performed independently for each of the 15 robot morphologies, as different arm lengths and joint configurations require different base placements for the same trajectory.

Inverse Kinematics and Rendering. Given the optimized base placement, IK is solved frame-byframe in MuJoCo. The robot is rendered from the original camera viewpoint.

Depth-Aware Compositing. The robot is rendered from the camera viewpoint and composited into the inpainted scene using depth ordering:

$$
I _ {\text { final }} (u, v) = \left\{ \begin{array}{l l} I _ {\text { robot }} (u, v) & \text { if } D _ {\text { robot }} (u, v) <   D _ {\text { scene }} (u, v) \land M _ {\text { robot }} (u, v) = 1 \\ I _ {\text { inpaint }} (u, v) & \text { otherwise } \end{array} \right.\tag{5}
$$

![](../../99_Attachments/papers/images/ego2robot/e955fe178d6da4464b1ee8508ffe8c6027a27ea1d9a78cf9722e4a05e60092d0.jpg)  
Figure 2: Evaluation framework. Four generalization dimensions with 12 evaluation settings. Dashed borders: settings decoupled from bundled randomization for independent testing. Solid borders: newly introduced evaluation axes. Gray border: external benchmark (EBench).

where $D _ { \mathrm { s c e n e } }$ is obtained from depth sensors or estimated via monocular depth. This process is applied independently for each of 15 robot morphologies (Panda, UR5e, ARX-L5, xArm7, Sawyer, Kinova Gen3, IIWA, Jaco, FR3, UR10e, ViperX, WidowX, Piper, YAM, Aloha-Agilex), generating parallel training streams from each ego video.

3. Quality Curation We apply three-level quality filtering. L1 (Pipeline-internal): frames with IK failures, self-collisions, action outliers, or insufficient workspace coverage are flagged during processing. L2 (Statistical): trajectories with extreme action values, sudden discontinuities, or excessive invalid frame ratios are removed. L3 (VLM Consistency): a vision-language model [50] audits synthesized videos for semantic consistency between rendered robot actions and original manipulation intents.

We apply the pipeline to four egocentric sources: ANT (7h, our in-house pick-and-place dataset with hand pose annotations), EgoDex [12] (732h), ViTRA [29] (249h), and EgoVerse [13] (954h), totaling ∼1,940 hours of annotated ego data. Because egocentric hand manipulation moves considerably faster than robot teleoperation, we subsample frames per source during training to match the robot speed distribution: ANT and EgoDex to 60% of their original frame rate (∼1.7× slower), EgoVerse to 45% (∼2.2× slower), and ViTRA to 25% (∼4× slower).

After processing across 15 robot morphologies and quality curation, this yields 18,561 hours of synthetic robot training data. Each sample consists of a robot-composited video frame, the corresponding camera-frame EEF action, camera parameters, and a text instruction. Because egocentric videos are captured with diverse, unknown camera placements, a world-frame action representation would require per-video calibration and produce incompatible action spaces across sources. Camera-frame relative EEF actions express end-effector displacements in the observer’s coordinate frame, naturally unifying data from different camera setups and robot morphologies.

## 4 Evaluation Framework

Understanding which generalization dimensions benefit from ego2robot-synthesized data—and which are limited by domain gaps—requires evaluation granularity that existing benchmarks do not provide. Current protocols such as RoboTwin 2.0 [16] apply multiple perturbation factors simultaneously, producing a single aggregate OOD metric that conflates visual, spatial, embodiment, and semantic shifts.

We extend RoboTwin 2.0 with 11 independent perturbation settings and camera-frame relative EEF support, and complement it with EBench [46], which provides 7 precision tabletop tasks in Isaac Sim with a higher-mounted head camera closer to the egocentric perspective. The extension covers four generalization dimensions as shown in Figure 2:

(1) Visual Appearance—independent control of background texture, lighting, and robot color. Background and lighting are decoupled from the original bundled randomization for isolated testing. Robot color applies random hue shifts to all robot links, testing visual invariance to embodiment appearance changes not seen during training. (2) Scene Layout—table height variation (±4cm), distractor objects, and camera viewpoint offset (±5cm), all decoupled for independent evaluation. These spatial perturbations probe robustness to physical arrangement changes common in real-world deployment. (3) Embodiment—replacing the default Aloha-Agilex with UR5-WSG, ARX-X5, and Franka Panda for zero-shot cross-embodiment evaluation, with initial end-effector poses aligned via IK to ensure consistent starting conditions. This tests whether the camera-frame action representation generalizes across morphologically distinct robots without embodiment-specific fine-tuning. (4) Task Semantics—50 tasks evaluated with object instances unseen during that task’s training, and 505 paraphrased natural language instructions that rephrase commands in colloquial form. This probes generalization to novel object appearances and robustness to linguistic variation. This decomposition enables precise attribution of generalization gains to specific perturbation types. Further details are provided in the Appendix.

## 5 Experiments

## 5.1 Experimental Setup

Model Architecture. We adopt a VLA architecture with Qwen3.5-4B as the vision-language backbone and a Diffusion Transformer (DiT) action head. The model predicts 32-step action chunks in camera-frame relative end-effector representation with 8 diffusion steps.

Training Protocol. All pretraining runs use identical hyperparameters: 8 GPUs, batch size 12/GPU, learning rate 1e-5 → 1e-6 with cosine decay, bf16, 200K steps. Since all configurations train for the same number of steps with the same batch size, each setting processes an identical number of training samples (∼19.2M frames), ensuring fair comparison regardless of dataset size. Finetuning loads pretrained weights with ColorJitter augmentation for 50K steps.

Pretraining Data. We compare four configurations: (i) robot-only (DROID [7] + AgibotWorld [8] + InternData [55], ∼6,565h), and (ii–iv) Ego2Robot-synthesized data (abbreviated Ego2R) mixed with robot data at 1:3, 3:1, and 1:1 ratios. Finetuning and Evaluation. All models are finetuned on RoboTwin’s 50 clean-setting tasks (50 demonstrations per task) and evaluated under each perturbation setting with 50 episodes per task. EBench models are finetuned separately on its training set. For real-robot evaluation, we test on an ARX ACone platform across 5 long-horizon manipulation tasks. More details are provided in the Appendix.

## 5.2 Main Results

Table 1 shows the success rates of models pretrained with different mixing ratios of Ego2Robot data and real-robot data. Table 2 further compares these models on the extended benchmark, where the test conditions are decomposed along three dimensions: visual appearance, scene, and embodiment. From these results, we draw the following conclusions:

Co-training improves OOD generalization. Ego2R+Robot (1:1) leads in five of seven columns, reaching 53.5% on RoboTwin Randomized (+2.6 over robot-only) while maintaining 68.1% on Clean. The 1:3 ratio yields marginal gains, whereas 3:1 and 1:1 produce substantial improvements.

Visual appearance benefits most. Table 2 shows that 1:1 improves on all three visual factors: background (+4) and lighting (+8) from the scene diversity in egocentric videos, and robot color (+6) from multi-morphology rendering across 15 configurations.

Table 1: Main results. Success rates (%) on RoboTwin2.0 and EBench. Green = gain >5% vs. Robot-only.

<table><tr><td rowspan="2">Pretraining</td><td colspan="2">RoboTwin</td><td colspan="4">Per-Dimension (RoboTwin)</td><td>EBench</td></tr><tr><td>Clean</td><td>Rand</td><td>Visual</td><td>Scene</td><td>Embody</td><td>Task</td><td>Avg</td></tr><tr><td>Robot-only</td><td>62.2</td><td>50.9</td><td>61.4</td><td>52.9</td><td>23.8</td><td>46.2</td><td>39.6</td></tr><tr><td rowspan="2">Ego2R+Robot (1:3)</td><td>61.4</td><td>51.0</td><td>61.2</td><td>52.5</td><td>21.9</td><td>49.5</td><td>47.4</td></tr><tr><td>-0.8</td><td>+0.1</td><td>-0.2</td><td>-0.4</td><td>-1.9</td><td>+3.3</td><td>+7.8</td></tr><tr><td rowspan="2">Ego2R+Robot (3:1)</td><td>64.1</td><td>49.2</td><td>62.7</td><td>54.3</td><td>28.2</td><td>51.6</td><td>51.7</td></tr><tr><td>+1.9</td><td>-1.7</td><td>+1.3</td><td>+1.4</td><td>+4.4</td><td>+5.4</td><td>+12.1</td></tr><tr><td rowspan="2">Ego2R+Robot (1:1)</td><td>68.1</td><td>53.5</td><td>67.3</td><td>56.9</td><td>27.2</td><td>54.1</td><td>49.8</td></tr><tr><td>+5.9</td><td>+2.6</td><td>+5.9</td><td>+4.0</td><td>+3.4</td><td>+7.9</td><td>+10.2</td></tr></table>

Table 2: Per-perturbation breakdown. Change vs. Robot-only. Green = gain >5%.

<table><tr><td rowspan="2">Pretraining</td><td colspan="3">Visual</td><td colspan="3">Scene</td><td colspan="3">Embodiment</td><td colspan="2">Task</td></tr><tr><td>BG</td><td>Light</td><td>Color</td><td>Height</td><td>Clutter</td><td>Camera</td><td>ARX</td><td>UR5</td><td>Franka</td><td>Obj</td><td>Lang</td></tr><tr><td>Robot-only</td><td>66.6</td><td>58.2</td><td>59.4</td><td>60.1</td><td>48.3</td><td>50.4</td><td>44.1</td><td>20.2</td><td>7.0</td><td>29.3</td><td>63.1</td></tr><tr><td rowspan="2">Ego2R+Robot (1:3)</td><td>65.0</td><td>58.3</td><td>60.3</td><td>58.6</td><td>49.3</td><td>49.6</td><td>43.7</td><td>17.6</td><td>4.5</td><td>36.8</td><td>62.2</td></tr><tr><td>-1.6</td><td>+0.1</td><td>+0.9</td><td>-1.5</td><td>+1.0</td><td>-0.8</td><td>-0.4</td><td>-2.6</td><td>-2.5</td><td>+7.5</td><td>-0.9</td></tr><tr><td rowspan="2">Ego2R+Robot (3:1)</td><td>65.5</td><td>60.9</td><td>61.8</td><td>62.0</td><td>49.2</td><td>51.6</td><td>47.6</td><td>31.4</td><td>5.6</td><td>40.0</td><td>63.1</td></tr><tr><td>-1.1</td><td>+2.7</td><td>+2.4</td><td>+1.9</td><td>+0.9</td><td>+1.2</td><td>+3.5</td><td>+11.2</td><td>-1.4</td><td>+10.7</td><td>+0.0</td></tr><tr><td rowspan="2">Ego2R+Robot (1:1)</td><td>70.3</td><td>65.8</td><td>65.8</td><td>62.4</td><td>52.0</td><td>56.3</td><td>51.2</td><td>25.0</td><td>5.3</td><td>39.6</td><td>68.5</td></tr><tr><td>+3.7</td><td>+7.6</td><td>+6.4</td><td>+2.3</td><td>+3.7</td><td>+5.9</td><td>+7.1</td><td>+4.8</td><td>-1.7</td><td>+10.3</td><td>+5.4</td></tr></table>

Scene layout shows moderate gains. Camera offset robustness improves by +6 at 1:1, as egocentric videos naturally exhibit diverse head poses and viewpoints.

Embodiment transfer benefits from multi-morphology data. ARX improves from 44 to 51 (1:1), and UR5 peaks at 31 (3:1), directly benefiting from exposure to 15 morphologies during pretraining. Franka remains below 7%, reflecting its large kinematic gap from the training embodiment.

Task semantics improve consistently. Unseen object generalization improves from 29% to 40% (+11 at 3:1) due to diverse object interactions in egocentric video. Paraphrased instruction robustness reaches 69% at 1:1, benefiting from broader instruction diversity.

EBench confirms gains under higher viewpoint. EBench’s higher-mounted camera is closer to the egocentric perspective. The 3:1 ratio achieves the best EBench score (51.7, +12.1 over robot-only), suggesting co-training benefits are amplified when the viewpoint bias partially matches.

## 5.3 Ablation Studies

Figure 3 isolates the pipeline’s contribution using ego-only pretraining (without any robot data).

Pipeline alignment is essential. Raw ego co-training achieves only 28.1% on RoboTwin Randomized. Processing through our pipeline (Ego2R with a single morphology) improves this to 31.7%, a +3.6 gain that validates the visual and action alignment stages.

More morphologies help. Increasing from 1 to 15 morphologies steadily improves performance (31.7→33.5). Adding raw ego data alongside the

![](../../99_Attachments/papers/images/ego2robot/bfa5e46a3c71d1f03c650e60d5dabde4eb97e06d66df4d0ec6934400abf6e1c7.jpg)  
Figure 3: Pipeline value and embodiment scaling. Success rate on RoboTwin Randomized.

![](../../99_Attachments/papers/images/ego2robot/0d17938829d35d3800f16b6c7e8a650369f02263040452c06d5e7be345161f96.jpg)  
Figure 4: Real robot results. Success rates (%) on five tasks on the ARX ACone platform.

![](../../99_Attachments/papers/images/ego2robot/0f6dc92baceb7e28eea534e3d394312a8cc5935a22717b0f9208b131917d5e17.jpg)  
Figure 5: Real robot rollouts. Key frames from five evaluation tasks on the ARX ACone platform.

15-morphology Ego2R data yields a

further jump to 37.3%—the raw ego data effectively acts as a 16th “morphology” with slightly different visual appearance and action distribution, further enriching the pretraining diversity.

## 5.4 Real Robot Experiments

We evaluate on an ARX ACone platform across five long-horizon tasks (Figure 5): putting fruits into a basket, putting blocks into a drawer, folding a towel, sweeping trash into a bin, and inserting a screw. For each task, we collect 20 teleoperated demonstrations. Additionally, we record egocentric play videos of hand manipulation (approximately 7 minutes per scene) and process them through our Ego2Robot pipeline to generate ACone-specific synthetic demonstrations. We compare three configurations (Figure 4): Robot-only uses robot-only pretraining and finetunes on teleoperated demonstrations; Mix uses Ego2R+Robot (1:1) pretraining with the same demonstrations; Mix + Ego2R Play finetunes on teleoperated demonstrations mixed 1:1 with the pipeline-converted egoplay (Ego2R) data.

Mix + Ego2R Play achieves the best results across all five tasks, with the largest gains on Put Blocks (+14 over Robot-only) and Insert Screw (+13), demonstrating that casually recorded egocentric videos can be converted into effective training signal via our pipeline. Mix pretraining alone already improves over Robot-only, and Ego2R Play data provides further consistent gains.

## 6 Limitations

Our work has several limitations that point to future research directions. First, retargeting maps hand poses to parallel-jaw grippers, discarding fine-grained finger articulation. Extending to dexterous multi-finger hands could broaden the range of transferable skills. Second, visual alignment relies on inpainting and depth-aware compositing, which may introduce artifacts under heavy occlusion or complex lighting. Improving rendering fidelity, e.g., with generative models, could further reduce the visual domain gap. Finally, our evaluation is limited to the task scope of RoboTwin2.0 [16]. Extending to broader tasks and embodiment configurations would strengthen generality.

## 7 Conclusion

We presented Ego2Robot, a scalable pipeline that converts egocentric hand manipulation videos into robot training data across 15 morphologies. The disentangled evaluation we constructed reveals that ego2robot-synthesized data complements robot data, with gains most pronounced under visual, embodiment, and semantic perturbations. On real robots, combining ego2robot-synthesized data with a small number of demonstrations enables effective multi-task deployment. We hope this work encourages leveraging the vast supply of human manipulation video for scalable robot learning.

## References

[1] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In Conference on Robot Learning, pages 2165–2183. PMLR, 2023.

[2] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. Openvla: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246, 2024.

[3] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, et al. pi 0: A vision-language-action flow model for general robot control. arXiv preprint arXiv:2410.24164, 2024.

[4] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, et al. pi {0.5}: a vision-language-action model with open-world generalization. arXiv preprint arXiv:2504.16054, 2025.

[5] J. Bjorck, F. Castaneda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, ˜ S. Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. arXiv preprint arXiv:2503.14734, 2025.

[6] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In 2024 IEEE International Conference on Robotics and Automation (ICRA), pages 6892–6903. IEEE, 2024.

[7] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. arXiv preprint arXiv:2403.12945, 2024.

[8] Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Hu, X. Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. arXiv preprint arXiv:2503.06669, 2025.

[9] C. Chi, Z. Xu, C. Pan, E. Cousineau, B. Burchfiel, S. Feng, R. Tedrake, and S. Song. Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots. arXiv preprint arXiv:2402.10329, 2024.

[10] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn. Learning fine-grained bimanual manipulation with low-cost hardware. arXiv preprint arXiv:2304.13705, 2023.

[11] P. Wu, Y. Shentu, Z. Yi, X. Lin, and P. Abbeel. Gello: A general, low-cost, and intuitive teleoperation framework for robot manipulators. In 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 12156–12163. IEEE, 2024.

[12] R. Hoque, P. Huang, D. J. Yoon, M. Sivapurapu, and J. Zhang. Egodex: Learning dexterous manipulation from large-scale egocentric video. arXiv preprint arXiv:2505.11709, 2025.

[13] R. Punamiya, S. Kareer, Z. Liu, J. Citron, R.-Z. Qiu, X. Cai, A. Gavryushin, J. Chen, D. Liconti, L. Y. Zhu, et al. Egoverse: An egocentric human dataset for robot learning from around the world. arXiv preprint arXiv:2604.07607, 2026.

[14] M. Lepert, J. Fang, and J. Bohg. Phantom: Training robots without robots using only human videos. In Conference on Robot Learning, pages 4545–4565. PMLR, 2025.

[15] S. Kareer, D. Patel, R. Punamiya, P. Mathur, S. Cheng, C. Wang, J. Hoffman, and D. Xu. Egomimic: Scaling imitation learning via egocentric video. In 2025 IEEE International Conference on Robotics and Automation (ICRA), pages 13226–13233. IEEE, 2025.

[16] T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Z. Li, Q. Liang, X. Lin, Y. Ge, Z. Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. arXiv preprint arXiv:2506.18088, 2025.

[17] N. M. M. Shafiullah, A. Rai, H. Etukuru, Y. Liu, I. Misra, S. Chintala, and L. Pinto. On bringing robots home. arXiv preprint arXiv:2311.16098, 2023.

[18] L. Pei, H. Yuzhe, L. Wanlin, X. Chenxi, and J. Ziyuan. Dexmove: Learning tactile-guided non-prehensile manipulation with dexterous hands. In The Fourteenth International Conference on Learning Representations, 2026. URL https://openreview.net/forum?id= dT3ZciXvNX.

[19] S. Nair, A. Rajeswaran, V. Kumar, C. Finn, and A. Gupta. R3m: A universal visual representation for robot manipulation. arXiv preprint arXiv:2203.12601, 2022.

[20] I. Radosavovic, T. Xiao, S. James, P. Abbeel, J. Malik, and T. Darrell. Real-world robot learning with masked visual pre-training. In Conference on Robot Learning, pages 416–426. PMLR, 2023.

[21] Y. J. Ma, S. Sodhani, D. Jayaraman, O. Bastani, V. Kumar, and A. Zhang. Vip: Towards universal visual reward and representation via value-implicit pre-training. arXiv preprint arXiv:2210.00030, 2022.

[22] A. S. Chen, S. Nair, and C. Finn. Learning generalizable robotic reward functions from” inthe-wild” human videos. arXiv preprint arXiv:2103.16817, 2021.

[23] C. Wang, L. Fan, J. Sun, R. Zhang, L. Fei-Fei, D. Xu, Y. Zhu, and A. Anandkumar. Mimicplay: Long-horizon imitation learning by watching human play. arXiv preprint arXiv:2302.12422, 2023.

[24] M. Xu, Z. Xu, Y. Xu, C. Chi, G. Wetzstein, M. Veloso, and S. Song. Flow as the cross-domain manipulation interface. arXiv preprint arXiv:2407.15208, 2024.

[25] J. Ren, P. Sundaresan, D. Sadigh, S. Choudhury, and J. Bohg. Motion tracks: A unified representation for human-robot transfer in few-shot imitation learning. In 2025 IEEE International Conference on Robotics and Automation (ICRA), pages 8802–8810. IEEE, 2025.

[26] R. Zheng, D. Niu, Y. Xie, J. Wang, M. Xu, Y. Jiang, F. Castaneda, F. Hu, Y. L. Tan, L. Fu, et al.˜ Egoscale: Scaling dexterous manipulation with diverse egocentric human data. arXiv preprint arXiv:2602.16710, 2026.

[27] H. Luo, Y. Feng, W. Zhang, S. Zheng, Y. Wang, H. Yuan, J. Liu, C. Xu, Q. Jin, and Z. Lu. Being-h0: vision-language-action pretraining from large-scale human videos. arXiv preprint arXiv:2507.15597, 2025.

[28] H. Luo, Y. Wang, W. Zhang, S. Zheng, Z. Xi, C. Xu, H. Xu, H. Yuan, C. Zhang, Y. Wang, et al. Being-h0. 5: Scaling human-centric robot learning for cross-embodiment generalization. arXiv preprint arXiv:2601.12993, 2026.

[29] Q. Li, Y. Deng, Y. Liang, L. Luo, L. Zhou, C. Yao, L. Zeng, Z. Feng, H. Liang, S. Xu, et al. Scalable vision-language-action model pretraining for robotic manipulation with real-life human activity videos. arXiv preprint arXiv:2510.21571, 2025.

[30] T. Zhang, S. Xia, Y. Wang, and Q. Jin. Easymimic: A low-cost framework for robot imitation learning from human videos. arXiv preprint arXiv:2602.11464, 2026.

[31] A. Mandlekar, S. Nasiriany, B. Wen, I. Akinola, Y. Narang, L. Fan, Y. Zhu, and D. Fox. Mimicgen: A data generation system for scalable robot learning using human demonstrations. arXiv preprint arXiv:2310.17596, 2023.

[32] S. Nasiriany, A. Maddukuri, L. Zhang, A. Parikh, A. Lo, A. Joshi, A. Mandlekar, and Y. Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. arXiv preprint arXiv:2406.02523, 2024.

[33] L. Y. Chen, C. Xu, K. Dharmarajan, M. Z. Irshad, R. Cheng, K. Keutzer, M. Tomizuka, Q. Vuong, and K. Goldberg. Rovi-aug: Robot and viewpoint augmentation for crossembodiment robot learning. arXiv preprint arXiv:2409.03403, 2024.

[34] L. Y. Chen, K. Hari, K. Dharmarajan, C. Xu, Q. Vuong, and K. Goldberg. Mirage: Crossembodiment zero-shot policy transfer with cross-painting. arXiv preprint arXiv:2402.19249, 2024.

[35] G. Ji, H. Polavaram, L. Y. Chen, S. Bajamahal, Z. Ma, S. Adebola, C. Xu, and K. Goldberg. Oxe-auge: A large-scale robot augmentation of oxe for scaling cross-embodiment policy learning. arXiv preprint arXiv:2512.13100, 2025.

[36] Y. Mu, T. Chen, Z. Chen, S. Peng, Z. Lan, Z. Gao, Z. Liang, Q. Yu, Y. Zou, M. Xu, et al. Robotwin: Dual-arm robot benchmark with generative digital twins. In Proceedings of the computer vision and pattern recognition conference, pages 27649–27660, 2025.

[37] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. Advances in Neural Information Processing Systems, 36:44776–44791, 2023.

[38] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. IEEE Robotics and Automation Letters, 7(3):7327–7334, 2022.

[39] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison. Rlbench: The robot learning benchmark & learning environment. IEEE Robotics and Automation Letters, 5(2):3019–3026, 2020.

[40] X. Li, K. Hsu, J. Gu, K. Pertsch, O. Mees, H. R. Walke, C. Fu, I. Lunawat, I. Sieh, S. Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. arXiv preprint arXiv:2405.05941, 2024.

[41] J. Gu, F. Xiang, X. Li, Z. Ling, X. Liu, T. Mu, Y. Tang, S. Tao, X. Wei, Y. Yao, et al. Maniskill2: A unified benchmark for generalizable manipulation skills. arXiv preprint arXiv:2302.04659, 2023.

[42] S. Tao, F. Xiang, A. Shukla, Y. Qin, X. Hinrichsen, X. Yuan, C. Bao, X. Lin, Y. Liu, T.-k. Chan, et al. Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai. arXiv preprint arXiv:2410.00425, 2024.

[43] W. Pumacay, I. Singh, J. Duan, R. Krishna, J. Thomason, and D. Fox. The colosseum: A benchmark for evaluating generalization for robotic manipulation. arXiv preprint arXiv:2402.08191, 2024.

[44] S. Fei, S. Wang, J. Shi, Z. Dai, J. Cai, P. Qian, L. Ji, X. He, S. Zhang, Z. Fei, et al. Libero-plus: In-depth robustness analysis of vision-language-action models. arXiv preprint arXiv:2510.13626, 2025.

[45] X. Zhou, Y. Xu, G. Tie, Y. Chen, G. Zhang, D. Chu, P. Zhou, and L. Sun. Libero-pro: Towards robust and fair evaluation of vision-language-action models beyond memorization. arXiv preprint arXiv:2510.03827, 2025.

[46] S. A. Laboratory. Ebench: Elemental mobile manipulation benchmark, 2026. URL https: //internrobotics.github.io/EBench-doc/. Preprint coming soon.

[47] R. A. Potamias, J. Zhang, J. Deng, and S. Zafeiriou. Wilor: End-to-end 3d hand localization and reconstruction in-the-wild. In Proceedings ofthe Computer Vision and Pattern Recognition Conference, pages 12242–12254, 2025.

[48] C. Si, Y. Liu, B. Ai, J. Xie, R. A. Potamias, C. Zheng, and H. Su. Anyhand: A large-scale synthetic dataset for rgb (-d) hand pose estimation. arXiv preprint arXiv:2603.25726, 2026.

[49] Z. Yu, S. Zafeiriou, and T. Birdal. Dyn-hamr: Recovering 4d interacting hand motion from a dynamic camera. In Proceedings ofthe Computer Vision and Pattern Recognition Conference, pages 27716–27726, 2025.

[50] Q. Team. Qwen3. 5: Accelerating productivity with native multimodal agents, february 2026. URL https://qwen. ai/blog.

[51] N. Carion, L. Gustafson, Y.-T. Hu, S. Debnath, R. Hu, D. Suris, C. Ryali, K. V. Alwala, H. Khedr, A. Huang, et al. Sam 3: Segment anything with concepts. arXiv preprint arXiv:2511.16719, 2025.

[52] S. Zhou, C. Li, K. C. Chan, and C. C. Loy. Propainter: Improving propagation and transformer for video inpainting. In Proceedings of the IEEE/CVF international conference on computer vision, pages 10477–10486, 2023.

[53] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In 2012 IEEE/RSJ international conference on intelligent robots and systems, pages 5026–5033. IEEE, 2012.

[54] K. Zakka. Mink: Python inverse kinematics based on MuJoCo, Feb. 2026. URL https: //github.com/kevinzakka/mink.

[55] Y. Tian, Y. Yang, Y. Xie, Z. Cai, X. Shi, N. Gao, H. Liu, X. Jiang, Z. Qiu, F. Yuan, et al. Interndata-a1: Pioneering high-fidelity synthetic data for pre-training generalist policy. arXiv preprint arXiv:2511.16651, 2025.

## Ego2Robot Appendix

A Ego2Robot Pipeline Details 14  
B Evaluation Framework Details 17  
C Model Architecture Details 19  
D Training Details 19  
E Real Robot Experiment Details 20  
F Additional Experimental Results 21

## A Ego2Robot Pipeline Details

## A.1 Hand Pose Estimation (Path B).

Per-Frame Reconstruction. WiLoR [47] performs per-frame hand detection and regresses MANO parameters $( \theta , \beta , \mathbf { t } )$ , yielding 21 keypoints $\{ \mathbf { p } _ { j } \} _ { j = 0 } ^ { 2 0 }$ and a hand mesh per frame. Detections are filtered by a SAM 3-generated hand mask: frames where more than 80% of projected keypoints fall outside the mask are discarded.

Cross-Frame Association. WiLoR uses a YOLO-based hand detector that outputs bounding boxes and initial left/right labels. To build temporally consistent tracks, the frame with the highest combined left+right detection score serves as the seed. From the seed, we propagate bidirectionally: at each frame, each new detection is assigned to the hand whose previous wrist position is nearest in image space $( \ell _ { 2 }$ distance). When multiple detections compete for the same hand, the highestscoring one is kept. After association, a jump filter removes frames where the 3D wrist velocity exceeds max(4 × median velocity, 0.003 m/frame), indicating misdetections.

Temporal Optimization. DynHaMR [49] refines the tracks by jointly optimizing MANO pose and shape parameters across the full sequence, minimizing:

$$
\mathcal {L} _ {\mathrm{dyn}} = \mathcal {L} _ {\mathrm{data}} + \lambda_ {\text { smooth }} \mathcal {L} _ {\text { smooth }} + \lambda_ {\text { bio }} \mathcal {L} _ {\text { bio }}\tag{6}
$$

where ${ \mathcal { L } } _ { \mathrm { d a t a } }$ enforces consistency with per-frame WiLoR estimates, ${ \mathcal { L } } _ { \mathrm { s m o o t h } }$ penalizes acceleration in wrist position and finger joint angles, and $\mathcal { L } _ { \mathrm { b i o } }$ enforces biomechanical joint limits. The depth of reconstructed hands is constrained to [0.05, 0.4] m from the camera.

Gap Handling. When hand detections are missing for consecutive frames, we apply gap-specific interpolation. Large gaps (>10 frames) are filled with the robot’s home configuration, with smooth blending transitions at the gap boundaries. The blend length is $n = \mathrm { m a x } ( 5 , \mathrm { m i n } ( 9 0 , \lceil 0 . 6 n _ { \mathrm { p o s } } \ +$ $\left. . 4 n _ { \mathrm { r o t } } \right] ) .$ ) frames, where $n _ { \mathrm { p o s } } ~ = ~ \Delta p / 3 . 2 5$ mm and $n _ { \mathrm { r o t } } ~ = ~ \Delta \theta / 1 . 0 8 ^ { \circ }$ are the number of frames needed at fixed blend speeds to cover the displacement. Small gaps (≤10 frames) use linear position interpolation + SLERP.

## A.2 Subtask Segmentation (Path B).

For long continuous recordings, we pre-split videos at 60-second boundaries. Each clip is sent to a VLM (Qwen3.5 [50]) along with the following prompt template:

```txt
You are watching a first-person manipulation video ( {duration}s). Task: " {task_desc}" Segment this video by complete task goals. Each subtask should be
```

```txt
an independent, complete objective.
Write a SHORT English action instruction (5--12 words) for each subtask.
Output ONLY a JSON array: [{"description":..., "start_time":..., "end_time":...}, ...]
```

The VLM returns subtask boundaries and natural language descriptions that serve as training instructions.

## A.3 Action Alignment Details.

Handedness Sign. The sign s in the grasp-axis definition (Equation 3) is determined by the hand’s left/right identity: $s = + 1$ for the right hand and s = −1 for the left hand, so that the grasp axis z points consistently regardless of handedness and both hands map to the same gripper frame. The wrist-to-fingertip vector $\mathbf { d } = \mathbf { p } _ { \mathrm { v f } } - \mathbf { p } _ { \mathrm { w r i s t } }$ that forms the gripper-normal axis y is taken directly from the MANO keypoints.

Degenerate Orientation. When the thumb tip and virtual fingertip nearly coincide (gripper width $w < 0 . 0 1 \mathrm { m } )$ , the grasp orientation degenerates; we freeze it to the last valid estimate. The same fallback is applied when z and d are nearly parallel $( \| \mathbf { z } \times \mathbf { d } \| \approx 0 )$

Velocity Filtering. Per-frame detection jumps are removed by a velocity filter. For position velocity $v _ { t } = \| \mathbf p _ { t } - \mathbf p _ { t - 1 } \|$ , the threshold is:

$$
\tau_ {t} = \max \left(5 \cdot \operatorname{median} \left(\left\{v _ {s} \right\} _ {s}\right), 0. 9 / \mathrm{fps}\right)\tag{7}
$$

An analogous threshold with floor 10.0/fps rad/frame is used for rotational velocity. Frames exceeding τ<sub>t</sub> are replaced by interpolation from neighbors. The procedure is iterated for 2 rounds.

Temporal Smoothing. Position and gripper width: Savitzky-Golay filter, window min(21, n), polynomial order min(3, window−1). Orientation: Gaussian-weighted SLERP, σ=10 frames, kernel size 21. Adjacent quaternions are hemisphere-corrected $( q _ { t } \to - q _ { t }$ when $q _ { t } \cdot q _ { t - 1 } < 0 )$ before interpolation.

## A.4 Visual Alignment Details.

Arm Segmentation. SAM 3 [51] uses the text prompt “person” with the middle frame as prompt anchor for temporal propagation. Long videos are processed in 400-frame chunks with 50-frame overlap; masks in overlap regions are merged via bitwise-OR. Post-processing: (i) $\mathrm { { g a p s } \leq 3 }$ frames are filled by interpolating neighboring masks; (ii) frames with mask area $< 5 0 \%$ of the local median (window 11) are replaced by the nearest valid mask; (iii) morphological close with 5×5 elliptical kernel.

Hand Removal. ProPainter [52] runs at fp16 with neighbor length = 10, ref $s \mathrm { t r i d e } = 1 0$ , subvideo length = 80, mask dilation = 4, RAFT iterations = 20.

Base Pose Search. The optimization objective is defined in Equation 4. Here we detail the candidate generation and scoring. Candidates are generated in the camera coordinate frame with offsets scaled by reach r:

• Lateral (left-right): $r \times \{ 0 . 3 , 0 . 4 , 0 . 5 , 0 . 6 , 0 . 8 , 1 . 0 , 1 . 2 \}$ (7 levels, sign-flipped per arm)

• Forward-backward: r × {−0.1, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9} (7 levels)

• Vertical: r × {0.4, 0.2, 0.0, −0.2, −0.4} (5 levels)

• Orientation: pitch $\{ 3 0 ^ { \circ } , 4 5 ^ { \circ } , 6 0 ^ { \circ } \} \times \operatorname { y a w } \left\{ - 4 5 ^ { \circ } , - 2 0 ^ { \circ } , 0 ^ { \circ } , 2 0 ^ { \circ } , 4 5 ^ { \circ } \right\} \times \operatorname { r o l l } \left\{ - 1 5 ^ { \circ } , 0 ^ { \circ } , 1 5 ^ { \circ } \right\}$

Candidates with camera distance $< 0 . 2 0 \mathrm { m }$ , or with trajectory points beyond 0.9r from base or closer than 0.08 m to base, are discarded. Surviving candidates are scored by:

$$
S = \operatorname{FR} \left(\mathbf {T} _ {\text { base }}\right) - 5. 0 \cdot | \bar {\rho} - 0. 6 5 |\tag{8}
$$

where FR is the IK feasibility rate over up to 20 keyframes (using the mink IK solver, quadprog backend, 100 iterations, $1 0 ^ { - 5 }$ threshold). The second term is a reach penalty: $\begin{array} { r }  \bar { \rho } = \frac { 1 } { | \mathcal { K } | } \sum _ { k } \bar { \| \mathbf { T } _ { \mathrm { b a s e } } ^ { - 1 } \mathbf { p } _ { k } ^ { \mathrm { e e } } \| / r } \end{array}$ is the average end-effector distance from the base normalized by the kinematic reach r, and the penalty is minimized when $\bar { \rho } = 0 . 6 5$ , encouraging the robot to operate at 65% of its maximum reach to retain kinematic margin for manipulation. We independently screen the top-5 candidates per arm, then jointly verify all 25 left–right combinations to select the final base placement.

Depth-Aware Compositing. The main text (Equation 5) presents a unified depth-ordering rule. In practice, we separate the robot into arm body and gripper regions using MuJoCo’s per-geom segmentation masks. The arm body mask (robot mask=1 ∧ gripper mask=0) is always composited onto the inpainted scene, since the arm is positioned between the camera and the workspace and is never occluded by scene objects. The gripper mask (gripper mask=1) undergoes per-pixel depth comparison: a gripper pixel at $( u , v )$ is hidden when the scene depth $D _ { \mathrm { s c e n e } } ( u , v ) < D _ { \mathrm { s i m } } ( u , v )$ and the pixel is not within the dilated hand mask region, where $D _ { \mathrm { s c e n e } }$ is estimated by Depth Anything V3 and $D _ { \mathrm { s i m } }$ is rendered by MuJoCo. The hand mask is dilated with a 5×5 kernel (1 iteration) before compositing to prevent revealing inpainted boundaries along the original arm contour. The final overlay is:

$$
\begin{array}{c} I _ {\text {out}} (u, v) = \left\{ \begin{array}{l l} I _ {\text {sim}} (u, v) & \text {if} (u, v) \in M _ {\text {arm}} \cup M _ {\text {gripper\_vis}} \\ I _ {\text {inpaint}} (u, v) & \text {otherwise} \end{array} \right. \\ \text {where} M _ {\text {gripper\_vis}} = M _ {\text {gripper}} \setminus \{(u, v): D _ {\text {scene}} <   D _ {\text {sim}} \wedge (u, v) \notin M _ {\text {hand}} \}. \end{array}\tag{9}
$$

## A.5 Quality Curation Details.

L1 (Pipeline-internal). A frame is valid when: (i) hand detected, (ii) IK tracking error $< 0 . 0 5  { \mathrm { m } }$ (iii) rendered robot visible (>0 pixels), (iv) no self-collision (MuJoCo contact check). Additional invalidation: bimanual cross-arm contacts > 1 or robot mask > 70% of image area.

Stability Erosion. Short valid runs $( < \lfloor 0 . 3 \times \mathrm { f p s } \rfloor$ frames) sandwiched between invalid regions are eroded to invalid.

L2 (Statistical). Two post-hoc statistical filters are applied: (i) Q1/Q99 filter: for each action dimension, per-dataset Q1 and Q99 statistics are computed (excluding previously invalidated frames). Frames falling outside $[ \mathrm { Q 1 } - 3 ( \mathrm { Q 9 9 - Q 1 } ) , \mathrm { Q 9 9 + 3 } ( \mathrm { Q 9 9 - Q 1 } ) ]$ are flagged. (ii) Sudden-change filter: for each step, residual, acceleration, and jerk are computed on state/action trajectories. Steps exceeding per-dimension thresholds (computed from the dataset’s distribution) are flagged. After both filters, episodes whose total invalid frame ratio exceeds 60% are discarded entirely.

L3 (VLM Consistency). A VLM (Qwen3.5) audits each synthesized video for semantic consistency. The video is sampled at 4 fps and sent along with the subtask description. The prompt is:

```txt
You are evaluating whether a manipulation video matches its text description.
This is a ROBOT manipulation dataset. "Hand" refers to the robot's gripper/end-effector.
Many tasks use FAKE or SIMULATED objects as stand-ins for real objects. This is EXPECTED.
Task Description: {description}
Determine if the robot's actions match the described task.
Flag MAJOR MISMATCHES: wrong action type, wrong object category, wrong target location, or failed execution.
Be tolerant of: fake/toy objects, minor appearance variations, small spatial deviations, different grasping approaches.
Respond in JSON: {"is_consistent": true/false, "confidence": 0.0-1.0, "reasoning": "..."}
```

Episodes judged inconsistent are discarded.

## A.6 Color Randomization.

Each rendered robot undergoes deterministic color randomization in HSV space: $H \sim U ( 0 , 1 )$ $S \sim U ( 0 . 3 , 1 ) , V \sim U ( 0 . 4 , 1 )$ , applied uniformly across all links.

Table 3: Supported robot morphologies.

<table><tr><td>Robot</td><td>DOF</td><td>Gripper (mm)</td><td>Reach (m)</td></tr><tr><td>Panda</td><td>7</td><td>0–80</td><td>1.272</td></tr><tr><td>Kinova Gen3</td><td>7</td><td>0–85</td><td>1.337</td></tr><tr><td>IIWA</td><td>7</td><td>0–85</td><td>1.411</td></tr><tr><td>Sawyer</td><td>7</td><td>14–79</td><td>1.420</td></tr><tr><td>FR3</td><td>7</td><td>0–80</td><td>1.272</td></tr><tr><td>xArm7</td><td>7</td><td>0–85</td><td>1.290</td></tr><tr><td>UR5e</td><td>6</td><td>0–85</td><td>1.236</td></tr><tr><td>UR10e</td><td>6</td><td>0–85</td><td>1.627</td></tr><tr><td>Jaco</td><td>6</td><td>0–125</td><td>1.200</td></tr><tr><td>ViperX</td><td>6</td><td>15–87</td><td>0.911</td></tr><tr><td>WidowX</td><td>6</td><td>11–55</td><td>0.787</td></tr><tr><td>ARX-L5</td><td>6</td><td>0–88</td><td>0.855</td></tr><tr><td>Piper</td><td>6</td><td>0–70</td><td>0.883</td></tr><tr><td>YAM</td><td>6</td><td>4–75</td><td>0.866</td></tr><tr><td>Aloha-Agilex</td><td>6</td><td>7–102</td><td>0.853</td></tr></table>

![](../../99_Attachments/papers/images/ego2robot/ddaa595614ef1cc5de81f7e83e3df67617a0007fcb7252d16ab19d1bc9010839.jpg)  
Figure 6: 15 supported robot morphologies. 3D models of all 15 robots.

## A.7 Supported Robot Morphologies.

Table 3 lists the 15 morphologies. Figure 6 shows the 3D models of all 15 robots.

## B Evaluation Framework Details

## B.1 Perturbation Parameters.

Randomized (standard OOD). The original RoboTwin 2.0 setting simultaneously applies background texture replacement, lighting randomization, table height offset, and clutter. We decouple these into independent axes below, and additionally introduce Camera Offset, Robot Color, Paraphrased Instructions, and Unseen Objects as new evaluation dimensions.

Visual Appearance: Background. Table and floor textures replaced with randomly sampled textures from a library. Lighting. Light positions and intensities randomized. Robot Color. Uniform hue shift from [0<sup>◦</sup>, 360<sup>◦</sup>) applied to all robot links.

Scene Layout: Table Height. Vertical offset ±4 cm. Clutter. 3–5 distractor objects with random poses. Camera Offset. Head camera displaced up to 5 cm per axis.

Task Semantics: Paraphrased Instructions. 505 colloquially rephrased commands (human + LLM generated). Unseen Objects. 50 new tasks with object instances not present in the finetuning demonstrations (same category, different appearance/geometry), spanning seven manipulation families:

• Move-to-pad/pot (10): move bottle pad, move cup pad, move bowl pad, move cup pot, move bottle pot, move mug pot, move apple pot, move seal pot, move pillbottle pot, move bowl pot

• Place-in-basket (11): place soap basket, place mug basket, place perfume basket, place teabox basket, place toycar basket, place apple basket, place bottle basket, place cup basket, place coffeebox basket, place saucecan basket, place hamburg basket

• Place-on-stand (4): place cup stand, place mug stand, place bottle stand, place apple stand

• Place-on-scale (3): place bottle scale, place cup scale, place mug scale

• Put-in-cabinet (3): put apple cabinet, put seal cabinet, put bowl cabinet

• Bimanual place-A-to-B (12): place cup left bottle, place mug right apple, place bottle left cup, place seal right mug, place mug left cup, place apple left mug, place bottle right apple, place seal left cup, place mug left bottle, place apple right cup, place cup right seal, place bottle left apple

• Move-away (7): move cup away, move bottle away, move apple away, move mug away, move seal away, move bowl away, move pillbottle away

Embodiment: Cross-Embodiment Transfer. The default embodiment is Aloha-Agilex, loaded as a single dual-arm URDF. For zero-shot cross-embodiment evaluation, we replace it with ARX-X5, UR5-WSG, or Franka Panda. Each alternative embodiment is loaded as two independent single-arm URDFs positioned symmetrically about the workspace center, with inter-arm base distances of 0.6 m (ARX-X5), 0.59 m (UR5-WSG), and 0.65 m (Franka) to accommodate different arm lengths. Initial EEF poses are aligned via IK, and all three camera extrinsics (head camera + two wrist cameras) are aligned across embodiments to ensure consistent starting conditions in the camera-frame action space.

## B.2 Task List.

The 50 tasks: adjust bottle, beat block hammer, blocks ranking rgb, blocks ranking size, click alarmclock, click bell, dump bin bigbin, grab roller, handover block, handover mic, hanging mug, lift pot, move can pot, move pillbottle pad, move playingcard away, move stapler pad, open laptop, open microwave, pick diverse bottles, pick dual bottles, place a2b left, place a2b right, place bread basket, place bread skillet, place burgerfries, place can basket, place cans plasticbox, place container plate, place dual shoes, place empty cup, place fan, place mouse pad, place object basket, place object scale, place object stand, place phone stand, place shoe, press stapler, put bottles dustbin, put object cabinet, rotate qrcode, scan object, shake bottle, shake bottle horizontally, stack blocks three, stack blocks two, stack bowls three, stack bowls two, stamp seal, turn switch.

Step limits per task range from 400 (e.g., click bell, adjust bottle) to 1700 (put bottles dustbin), with most tasks at 400. Complex multi-step tasks use higher limits: open microwave 1500, blocks ranking 1200, stack blocks three 1200, stack bowls 900–1200, hanging mug 900, stack blocks two / handover block 800, place cans plasticbox 800. New/unseen tasks default to 1000 steps.

## B.3 Protocol.

50 episodes/task, binary success. Aggregates: Visual = mean(BG, Light, Robot Color); Scene = mean(Height, Clutter, Camera); Embodiment = mean(ARX, UR5, Franka); Task = mean(Obj, Lang).

## B.4 EBench Table Top.

EBench [46] provides 7 table-top tasks in Isaac Sim: collect coffee beans, flip cup & collect cookies, frame against pen holder, install gear, peg in hole, put glass in glass box, tighten nut. Camera is higher than RoboTwin, closer to the egocentric perspective.

## C Model Architecture Details

The Qwen3.5-4B vision-language backbone processes multi-view RGB images (2–3 views per timestep) and a structured text prompt, producing a sequence of hidden states $\mathbf { H } \in \mathbb { R } ^ { L \times d }$ that jointly encode visual and linguistic information. Camera intrinsics $\mathbf { K } \in \mathbb { R } ^ { 3 \times 3 }$ and extrinsics $\mathbf { T } _ { w c } \in S E ( 3 )$ are injected into the visual features via mRoPE positional encodings, enabling the model to reason about the 3D spatial relationship between the camera and the scene. The DiT action head conditions on H through cross-attention: a context generator compresses H into conditioning features C using 8 learnable query tokens, and the DiT layers attend to C when predicting 32-step action chunks via flow matching (8 training / 4 inference steps).

## C.1 Structured Prompt.

The text input follows a two-field format:

embodiment: {type}\_{model}

instruction: {task description}

embodiment encodes data source and robot model: robot aloha (real robot), h2r arx (Ego2R with ARX), human ego (raw ego). Dropped to “None” with 15% probability during training. instruction is never dropped.

## C.2 Camera-Frame Relative EEF.

Each action step is 7-dim: 3D position delta $\Delta \mathbf { p }$ , 3D rotation delta $\Delta \omega$ (rotation vector), 1D gripper. Given the EEF-to-camera transformation $\mathbf { T } _ { c e } = \mathbf { T } _ { w c } ^ { - 1 } \mathbf { T } _ { w e }$ with rotation component $\mathbf { R } _ { c e } ,$ base-frame deltas are transformed:

$$
\Delta \mathbf {p} _ {c c} = \mathbf {R} _ {c e} \Delta \mathbf {p} _ {e e}, \quad \Delta \mathbf {R} _ {c c} = \mathbf {R} _ {c e} \Delta \mathbf {R} _ {e e} \mathbf {R} _ {c e} ^ {\top}\tag{10}
$$

This naturally unifies data from different camera setups and robot morphologies without explicit extrinsic calibration, as described in Section 3.

## C.3 Flow Matching.

Given clean actions ${ \bf a } _ { 0 }$ and noise $\epsilon \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } )$ , the noised sample at $t \in [ 0 , 1 ]$

$$
\mathbf {a} _ {t} = (1 - t) \mathbf {a} _ {0} + t \boldsymbol {\epsilon}\tag{11}
$$

Training objective:

$$
\mathcal {L} = \mathbb {E} _ {t, \mathbf {a} _ {0}, \epsilon} \left\| \mathbf {v} _ {\theta} (\mathbf {a} _ {t}, t, \mathbf {c}) - (\epsilon - \mathbf {a} _ {0}) \right\| ^ {2}\tag{12}
$$

where c is the visual-language conditioning. Inference uses 4 Euler steps $( \Delta t { = } 1 / 4 )$

## D Training Details

## D.1 Pretraining.

8×A100 GPUs, batch 12/GPU, backbone lr $1 0 ^ { - 5 } \substack {  } 1 0 ^ { - 6 }$ cosine (5K warmup), action head lr 10× $( 1 0 ^ { - 4 } {  } 1 0 ^ { - 5 } )$ , AdamW $( \beta _ { 1 } { = } 0 . 9 , \beta _ { 2 } { = } 0 . 9 5 )$ , bf16, ZeRO-1, 200K steps (∼19.2M frames), 8 diffusion steps/forward. No image augmentation.

## D.2 Pretraining Data.

Robot data comprises three sources: DROID [7] (∼511 h) provides real-world teleoperated demonstrations across diverse objects and scenes with a Franka arm. AgibotWorld [8] (∼2,404 h) is a large-scale real teleoperation dataset covering 180 manipulation tasks on humanoid platforms. InternData [55] (∼3,650 h) provides simulation-generated demonstrations across Franka, humanoid, and Aloha embodiments. Together these total ∼6,565 h. Ego2R data is derived from four egocentric sources (ANT 7 h, EgoDex 732 h, ViTRA 249 h, EgoVerse 954 h, totaling ∼1,940 h before processing) rendered across 15 morphologies, yielding 18,561 h after pipeline processing and quality curation. The mixing ratios (1:3, 3:1, 1:1 Ego2R-to-Robot) are implemented via per-source sampling weights; all configurations process the same total number of frames. Figure 7 shows the per-source sampling weights used within each group.

![](../../99_Attachments/papers/images/ego2robot/c106a864ce9a3a9dca9deeab0d3833b4dca2e61664983bb1845b56e5f637851b.jpg)

![](../../99_Attachments/papers/images/ego2robot/9f1521e775f2ab29975d992f3a2b473ac1af536986eac8d8cd60fed4783b281b.jpg)  
Figure 7: Pretraining data composition. Slices show per-source sampling weights (training mix); panel titles give the total data volume. (a) Robot (∼6,565 h). (b) Ego2R (∼18,561 h).

## D.3 Finetuning.

All finetuning runs load pretrained weights. 8×A100 GPUs, batch 12/GPU, backbone lr $1 0 ^ { - 5 } \substack {  } 1 0 ^ { - 6 }$ cosine (5K warmup), action head lr $1 0 \times ( 1 0 ^ { - 4 } {  } 1 0 ^ { - 5 } )$ , AdamW $( \beta _ { 1 } { = } 0 . 9 , \beta _ { 2 } { = } 0 . 9 5 )$ bf16, ZeRO-2, ColorJitter, 8 diffusion steps/forward.

RoboTwin Clean. 50 tasks × 50 demos (2,500 episodes), 50K steps, chunk 20, replan every 16.

EBench Table Top. 7 table-top tasks × 400 demos (2,800 episodes), 50K steps, chunk 32.

Real robot. See Section E for data details. 1:1 teleop-to-Ego2R mixing ratio, 50K steps, chunk 32.

## D.4 Ablation Configurations.

The ablation (Figure 3) uses only ego-sourced data (raw ego or Ego2R) for pretraining, excluding real robot data, to isolate the pipeline’s contribution:

• Raw ego (∼1,940 h): egocentric video after pipeline quality filtering but without robot rendering.

• Ego2R, 1 morphology (∼1,237 h): pipeline-processed, ARX-L5 only.

• Ego2R, 5 morphologies (∼6,187 h): Aloha-Agilex, ARX-L5, FR3, ViperX, xArm7.

• Ego2R, 10 morphologies (∼12,374 h): Aloha-Agilex, ARX-L5, FR3, IIWA, Jaco, Piper, UR5e, ViperX, YAM, xArm7.

• Ego2R, 15 morphologies (∼18,561 h): all 15.

• Ego2R (15) + Raw ego (∼20,501 h): 15-morphology Ego2R plus raw egocentric data.

All ablation models are pretrained on the specified ego-sourced data only (no real robot data), then finetuned on RoboTwin Clean.

## E Real Robot Experiment Details

## E.1 Platform and Tasks.

ARX ACone dual-arm (6-DOF/arm, parallel gripper, head + two wrist RGB cameras, 15 Hz control, Replan every 32 steps).

• Put Fruits (3 steps): place 3 fruits into a basket.

![](../../99_Attachments/papers/images/ego2robot/20a5dc5f791c5fc1cab42f232bb06f70e8ff00d87deba0660ab2c0b7f1e98728.jpg)  
Figure 8: Ego play → Ego2R synthesis on real-world scenes. Top: original egocentric human manipulation. Bottom: Ego2R pipeline output with ACone robot overlay.

Table 4: Real robot scoring.

<table><tr><td>Task</td><td>Step 1</td><td>Step 2</td><td>Step 3</td><td>Step 4</td></tr><tr><td>Put Fruits</td><td>33.3</td><td>33.3</td><td>33.3</td><td>—</td></tr><tr><td>Put Blocks</td><td>25</td><td>25</td><td>25</td><td>25</td></tr><tr><td>Fold Towel</td><td>50</td><td>50</td><td>—</td><td>—</td></tr><tr><td>Sweep Trash</td><td>25</td><td>25</td><td>25</td><td>25</td></tr><tr><td>Insert Screw</td><td>25</td><td>25</td><td>25</td><td>25</td></tr></table>

• Put Blocks (4 steps): open drawer, place 2 blocks, close drawer.

• Fold Towel (2 steps): two sequential folds.

• Sweep Trash (4 steps): pick broom, sweep, dump, return broom.

• Insert Screw (4 steps): bimanual handover and insertion of 2 screws.

## E.2 Data.

20 teleop demos per task (100 total) + ∼35 min ego play video across 5 scenes. Ego play processed via Path B (WiLoR, DynHaMR, Qwen3.5, Ego2R) to generate 675 ACone synthetic episodes. Teleop and Ego2R data are mixed at a 1:1 ratio during finetuning.

## E.3 Ego Play to Ego2R Visualization.

Figure 8 shows representative frames from the ego play data and corresponding Ego2R synthesis. The top row shows the original egocentric human manipulation; the bottom row shows the pipeline output with the robot (ACone) overlaid onto the inpainted scene.

## E.4 Scoring.

Sub-step partial scoring (Table 4), 100 points per task, 20 trials.

## F Additional Experimental Results

## F.1 Comparison with Pi0.5.

Pi0.5 [4] is evaluated under the same RoboTwin EEF settings (OpenPI framework, camera-frame relative EEF). Pi0.5 uses a different backbone and pretraining data. Figure 9 reports results. Ego2R+Robot (1:1) outperforms the Robot-only baseline across nearly all settings.

![](../../99_Attachments/papers/images/ego2robot/85136799b4b3f8a05945c3f4c0efb5193ea9edf7b67e25f8e005c385af6904f3.jpg)  
Figure 9: Comparison with Pi0.5 across RoboTwin settings.

## F.2 Per-Task Results.

Table 5 reports per-task success rates on all 50 RoboTwin tasks under Clean and Randomized settings for five models: Pi0.5 and four of our models.

Table 5: Per-task results on RoboTwin including Pi0.5 (success rate %).

<table><tr><td rowspan="2">Task</td><td colspan="2">Pi0.5</td><td colspan="2">Robot-only</td><td colspan="2">Ego2R (1:3)</td><td colspan="2">Ego2R (3:1)</td><td colspan="2">Ego2R (1:1)</td></tr><tr><td>Clean</td><td>Rand</td><td>Clean</td><td>Rand</td><td>Clean</td><td>Rand</td><td>Clean</td><td>Rand</td><td>Clean</td><td>Rand</td></tr><tr><td>adjust_bottle</td><td>62.0</td><td>18.0</td><td>94.0</td><td>77.0</td><td>92.0</td><td>79.0</td><td>100.0</td><td>72.0</td><td>89.0</td><td>91.0</td></tr><tr><td>beat_block_hammer</td><td>48.0</td><td>16.0</td><td>63.0</td><td>27.0</td><td>64.0</td><td>56.0</td><td>57.0</td><td>18.0</td><td>65.0</td><td>71.0</td></tr><tr><td>blocks_ranking_rgb</td><td>74.0</td><td>16.0</td><td>56.0</td><td>60.0</td><td>64.0</td><td>63.0</td><td>49.0</td><td>43.0</td><td>78.0</td><td>60.0</td></tr><tr><td>blocks_ranking_size</td><td>32.0</td><td>0.0</td><td>30.0</td><td>22.0</td><td>46.0</td><td>21.0</td><td>43.0</td><td>7.0</td><td>52.0</td><td>16.0</td></tr><tr><td>click_alarmclock</td><td>44.0</td><td>56.0</td><td>96.0</td><td>93.0</td><td>100.0</td><td>87.0</td><td>100.0</td><td>85.0</td><td>100.0</td><td>100.0</td></tr><tr><td>click_bell</td><td>32.0</td><td>40.0</td><td>100.0</td><td>95.0</td><td>100.0</td><td>94.0</td><td>100.0</td><td>93.0</td><td>100.0</td><td>100.0</td></tr><tr><td>dump_bin_bigbin</td><td>72.0</td><td>70.0</td><td>54.0</td><td>73.0</td><td>72.0</td><td>69.0</td><td>81.0</td><td>76.0</td><td>86.0</td><td>72.0</td></tr><tr><td>grab_roller</td><td>94.0</td><td>46.0</td><td>98.0</td><td>71.0</td><td>68.0</td><td>48.0</td><td>91.0</td><td>64.0</td><td>89.0</td><td>63.0</td></tr><tr><td>handover_block</td><td>16.0</td><td>0.0</td><td>5.0</td><td>2.0</td><td>18.0</td><td>4.0</td><td>39.0</td><td>9.0</td><td>36.0</td><td>9.0</td></tr><tr><td>handover_mic</td><td>26.0</td><td>4.0</td><td>69.0</td><td>13.0</td><td>86.0</td><td>34.0</td><td>83.0</td><td>17.0</td><td>97.0</td><td>23.0</td></tr><tr><td>hanging_mug</td><td>10.0</td><td>4.0</td><td>14.0</td><td>16.0</td><td>14.0</td><td>9.0</td><td>12.0</td><td>9.0</td><td>10.0</td><td>10.0</td></tr><tr><td>lift_pot</td><td>8.0</td><td>2.0</td><td>93.0</td><td>28.0</td><td>84.0</td><td>14.0</td><td>95.0</td><td>44.0</td><td>93.0</td><td>44.0</td></tr><tr><td>move_can_pot</td><td>28.0</td><td>0.0</td><td>47.0</td><td>50.0</td><td>30.0</td><td>40.0</td><td>42.0</td><td>85.0</td><td>47.0</td><td>65.0</td></tr><tr><td>move_pillbottle_pad</td><td>60.0</td><td>44.0</td><td>63.0</td><td>60.0</td><td>68.0</td><td>69.0</td><td>41.0</td><td>67.0</td><td>74.0</td><td>82.0</td></tr><tr><td>move_playingcard_away</td><td>90.0</td><td>52.0</td><td>74.0</td><td>58.0</td><td>88.0</td><td>92.0</td><td>88.0</td><td>42.0</td><td>92.0</td><td>63.0</td></tr><tr><td>move_stapler_pad</td><td>22.0</td><td>6.0</td><td>23.0</td><td>19.0</td><td>34.0</td><td>21.0</td><td>30.0</td><td>13.0</td><td>43.0</td><td>31.0</td></tr><tr><td>open_laptop</td><td>68.0</td><td>20.0</td><td>77.0</td><td>61.0</td><td>74.0</td><td>56.0</td><td>64.0</td><td>46.0</td><td>75.0</td><td>58.0</td></tr><tr><td>open_microwave</td><td>26.0</td><td>8.0</td><td>77.0</td><td>59.0</td><td>42.0</td><td>29.0</td><td>37.0</td><td>32.0</td><td>50.0</td><td>25.0</td></tr><tr><td>pick_diverse_bottles</td><td>56.0</td><td>18.0</td><td>60.0</td><td>37.0</td><td>58.0</td><td>53.0</td><td>71.0</td><td>50.0</td><td>70.0</td><td>50.0</td></tr><tr><td>pick_dual_bottles</td><td>82.0</td><td>14.0</td><td>91.0</td><td>59.0</td><td>80.0</td><td>77.0</td><td>83.0</td><td>55.0</td><td>97.0</td><td>54.0</td></tr><tr><td>place_a2b_left</td><td>60.0</td><td>10.0</td><td>40.0</td><td>55.0</td><td>58.0</td><td>42.0</td><td>54.0</td><td>48.0</td><td>73.0</td><td>44.0</td></tr><tr><td>place_a2b_right</td><td>58.0</td><td>14.0</td><td>42.0</td><td>49.0</td><td>52.0</td><td>41.0</td><td>53.0</td><td>51.0</td><td>64.0</td><td>53.0</td></tr><tr><td>place_bread_basket</td><td>68.0</td><td>44.0</td><td>75.0</td><td>55.0</td><td>72.0</td><td>64.0</td><td>76.0</td><td>59.0</td><td>79.0</td><td>62.0</td></tr><tr><td>place_bread_skillet</td><td>86.0</td><td>46.0</td><td>76.0</td><td>41.0</td><td>76.0</td><td>50.0</td><td>80.0</td><td>61.0</td><td>87.0</td><td>53.0</td></tr><tr><td>place_burger_fries</td><td>90.0</td><td>78.0</td><td>96.0</td><td>83.0</td><td>98.0</td><td>81.0</td><td>97.0</td><td>88.0</td><td>96.0</td><td>88.0</td></tr><tr><td>place_can_basket</td><td>40.0</td><td>0.0</td><td>49.0</td><td>25.0</td><td>38.0</td><td>9.0</td><td>34.0</td><td>15.0</td><td>34.0</td><td>16.0</td></tr><tr><td>place_cans_plasticbox</td><td>94.0</td><td>74.0</td><td>90.0</td><td>68.0</td><td>54.0</td><td>68.0</td><td>97.0</td><td>59.0</td><td>70.0</td><td>59.0</td></tr><tr><td>place_container_plate</td><td>96.0</td><td>58.0</td><td>86.0</td><td>76.0</td><td>92.0</td><td>79.0</td><td>93.0</td><td>73.0</td><td>93.0</td><td>81.0</td></tr><tr><td>place_dual_shoes</td><td>54.0</td><td>12.0</td><td>50.0</td><td>30.0</td><td>34.0</td><td>27.0</td><td>35.0</td><td>17.0</td><td>35.0</td><td>19.0</td></tr><tr><td>place_empty_cup</td><td>74.0</td><td>56.0</td><td>73.0</td><td>74.0</td><td>86.0</td><td>83.0</td><td>88.0</td><td>78.0</td><td>88.0</td><td>66.0</td></tr><tr><td>place_fan</td><td>36.0</td><td>30.0</td><td>48.0</td><td>54.0</td><td>48.0</td><td>24.0</td><td>41.0</td><td>50.0</td><td>39.0</td><td>46.0</td></tr><tr><td>place_mouse_pad</td><td>18.0</td><td>0.0</td><td>41.0</td><td>34.0</td><td>22.0</td><td>36.0</td><td>30.0</td><td>25.0</td><td>29.0</td><td>33.0</td></tr><tr><td>place_object_basket</td><td>24.0</td><td>4.0</td><td>65.0</td><td>50.0</td><td>76.0</td><td>28.0</td><td>77.0</td><td>51.0</td><td>69.0</td><td>48.0</td></tr><tr><td>place_object_scale</td><td>58.0</td><td>44.0</td><td>38.0</td><td>46.0</td><td>40.0</td><td>33.0</td><td>52.0</td><td>45.0</td><td>40.0</td><td>47.0</td></tr><tr><td>place_object_stand</td><td>94.0</td><td>40.0</td><td>70.0</td><td>75.0</td><td>80.0</td><td>77.0</td><td>87.0</td><td>71.0</td><td>82.0</td><td>82.0</td></tr><tr><td>place_phone_stand</td><td>40.0</td><td>4.0</td><td>65.0</td><td>49.0</td><td>48.0</td><td>63.0</td><td>70.0</td><td>61.0</td><td>75.0</td><td>45.0</td></tr><tr><td>place_shoe</td><td>64.0</td><td>24.0</td><td>84.0</td><td>84.0</td><td>78.0</td><td>84.0</td><td>63.0</td><td>58.0</td><td>75.0</td><td>76.0</td></tr><tr><td>press_stapler</td><td>42.0</td><td>32.0</td><td>86.0</td><td>71.0</td><td>82.0</td><td>62.0</td><td>76.0</td><td>70.0</td><td>83.0</td><td>62.0</td></tr><tr><td>put_bottles_dustbin</td><td>14.0</td><td>2.0</td><td>25.0</td><td>20.0</td><td>42.0</td><td>32.0</td><td>41.0</td><td>19.0</td><td>50.0</td><td>39.0</td></tr><tr><td>put_object_cabinet</td><td>22.0</td><td>0.0</td><td>41.0</td><td>20.0</td><td>30.0</td><td>19.0</td><td>39.0</td><td>36.0</td><td>43.0</td><td>29.0</td></tr><tr><td>rotate_qrcode</td><td>50.0</td><td>2.0</td><td>31.0</td><td>17.0</td><td>54.0</td><td>16.0</td><td>54.0</td><td>36.0</td><td>69.0</td><td>37.0</td></tr><tr><td>scan_object</td><td>62.0</td><td>38.0</td><td>62.0</td><td>37.0</td><td>66.0</td><td>46.0</td><td>66.0</td><td>46.0</td><td>56.0</td><td>33.0</td></tr><tr><td>shake_bottle</td><td>96.0</td><td>72.0</td><td>91.0</td><td>75.0</td><td>88.0</td><td>89.0</td><td>99.0</td><td>75.0</td><td>96.0</td><td>87.0</td></tr><tr><td>shake_bottle_horizontally</td><td>98.0</td><td>74.0</td><td>98.0</td><td>81.0</td><td>84.0</td><td>87.0</td><td>99.0</td><td>84.0</td><td>97.0</td><td>92.0</td></tr><tr><td>stack_blocks_three</td><td>68.0</td><td>16.0</td><td>14.0</td><td>23.0</td><td>14.0</td><td>28.0</td><td>10.0</td><td>13.0</td><td>28.0</td><td>23.0</td></tr><tr><td>stack_blocks_two</td><td>80.0</td><td>56.0</td><td>75.0</td><td>70.0</td><td>82.0</td><td>75.0</td><td>77.0</td><td>56.0</td><td>95.0</td><td>61.0</td></tr><tr><td>stack_bowls_three</td><td>38.0</td><td>36.0</td><td>50.0</td><td>41.0</td><td>40.0</td><td>43.0</td><td>48.0</td><td>50.0</td><td>47.0</td><td>45.0</td></tr><tr><td>stack_bowls_two</td><td>82.0</td><td>44.0</td><td>76.0</td><td>78.0</td><td>66.0</td><td>73.0</td><td>73.0</td><td>67.0</td><td>72.0</td><td>72.0</td></tr><tr><td>stamp_seal</td><td>32.0</td><td>2.0</td><td>35.0</td><td>42.0</td><td>46.0</td><td>30.0</td><td>34.0</td><td>30.0</td><td>44.0</td><td>42.0</td></tr><tr><td>turn_switch</td><td>56.0</td><td>40.0</td><td>55.0</td><td>42.0</td><td>40.0</td><td>42.0</td><td>53.0</td><td>41.0</td><td>50.0</td><td>48.0</td></tr><tr><td>Average</td><td>54.9</td><td>27.7</td><td>62.2</td><td>50.9</td><td>61.4</td><td>51.0</td><td>64.1</td><td>49.2</td><td>68.1</td><td>53.5</td></tr></table>