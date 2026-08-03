# H2R: A Human-to-Robot Data Augmentation for Robot Pre-training from Videos

Guangrun Li<sup>1∗</sup>, Yaoxu Lyu<sup>1∗</sup>, Zhuoyang Liu<sup>1∗</sup>, Chengkai Hou<sup>1†</sup>, Jieyu Zhang<sup>2</sup>, Shanghang Zhang<sup>1</sup> <sup>B</sup>

<sup>1</sup>State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University; <sup>2</sup>University of Washington

\* Equal contribution, <sup>†</sup> Project lead, <sup>B</sup> Corresponding author

![[99_Attachments/papers/images/h2r/d5a4428a0c2a1af0042a29a5db5eaf73621b2e0dd03044a2e323bd4f9ab38048.jpg]]  
Fig. 1: Overview of H2R. H2R is a human-to-robot data augmentation pipeline designed to reduce the visual gap between egocentric human-hand videos and robot-centric observations used in downstream manipulation tasks. H2R augments egocentric human videos by replacing human hands with rendered robot arms, reducing the human-to-robot visual gap during visual pre-training. The resulting encoders improve policy learning across simulation benchmarks, real-world manipulation tasks, and demonstrate consistent performance improvements.

Abstract—Large-scale pre-training using egocentric human videos has proven effective for robot learning. However, the models pre-trained on such data can be suboptimal for robot learning due to the significant visual gap between human hands and those of different robots. To remedy this, we propose H2R, a humanto-robot data augmentation pipeline that converts egocentric human videos into robot-centric visual data. H2R estimates human hand pose from videos, retargets the motion to simulated robotic arms, removes human limbs via segmentation and inpainting, and composites rendered robot embodiments into the original frames with camera-aligned geometry. This process explicitly bridges the visual gap between human and robot embodiments during pretraining. We apply H2R to augment large-scale egocentric human video datasets such as Ego4D and SSv2. To verify the effectiveness of the augmentation pipeline, we introduce a CLIP-based imagetext similarity metric that quantitatively evaluates the semantic fidelity of robot-rendered frames to the original human actions. We evaluate H2R through comprehensive experiments in both simulation and real-world settings. In simulation, H2R consistently improves downstream success rates across four benchmark suites—Robomimic, RLBench, PushT, and CortexBench—yielding gains of 1.3%–10.2% across different visual encoders and policy learning methods. In real-world experiments, H2R improves performance on UR5 and dual-arm Franka/UR5 manipulation platforms, achieving 3.3%–23.3% success rate gains across gripperbased, dexterous, and bimanual tasks. We further demonstrate the potential of H2R in cross-embodiment generalization and its compatibility with vision–language–action models. These results indicate that H2R improves the generalization ability of robotic policies by mitigating the visual discrepancies between human and robot domains.

## I. INTRODUCTION

Pre-training generalizable visual representations is a central challenge in robotic manipulation. Recent advances in largescale pre-training in computer vision and language have significantly improved representation learning across domains [23, 37, 27, 17, 10, 1]. However, collecting large-scale robot demonstrations remains labor-intensive and costly [13, 29, 14], motivating the use of readily available egocentric human videos as an alternative source for robot pre-training.

Large-scale egocentric datasets such as Ego4D [20], Something-Something V2 [19], and EPIC-Kitchens [8] capture diverse human-object interactions and have been shown to support transferable visual representations for robotic manipulation. However, these datasets are inherently human-centric. The visual mismatch between human hands in egocentric videos and robotic embodiments at deployment time introduces a gap that is not explicitly addressed during pre-training, limiting representation transfer.

To mitigate this issue, we propose H2R (as shown in Figure 1), a simple data augmentation method that converts videos of Human hand operations into that of Robotic arm manipulation. H2R consists of two major procedures: the first part is to generate the robotic movements to imitate the human hand movements in a video, followed by the second stage that overlays the robotic movements onto the human hand’s movements in the video. Specifically, in the first part, we employ state-of-the-art 3D hand reconstruction model HaMeR [40] to accurately detect the position and posture of the human hand in egocentric videos. Then, we simulate the same robot state in simulators to obtain the mask of robot actions. In the second stage, we use the Segment Anything Model [30] to automatically separate human hand from background, and use the inpainting model LaMa [51] to fill the removed hand mask. After that, we align the camera intrinsic parameters of the images detected in HaMeR with those in the simulator, and then achieve pixel-level matching between the robotic arm images in the simulators and the human hand images in the egocentric video. Finally, we overlay the robotic arm images captured by the simulator’s camera onto the areas where the human hands are removed. Through such a process, H2R explicitly reduces the gap between human and robot hands by creating realistic robotic arm movements that visually mimic human hand actions. It allows the model to learn the taskspecific actions demonstrated by the human hand, but with robotic arm visual representations that are more suitable for robotic systems.

To evaluate the effectiveness of the H2R augmentation process, we introduce a CLIP-based [41] semantic similarity metric that measures how well the rendered robot frames preserve the original action semantics. This provides a lightweight and scalable proxy to assess the alignment quality between input human videos and robot-augmented outputs.

We further evaluate the effectiveness of H2R through a comprehensive set of experiments in both simulation and realworld settings. In simulation, we conduct imitation learning experiments on four benchmark suites—Robomimic [36], RLBench [24], PushT [7], and CortexBench [35]— using visual encoders pre-trained with MAE and R3M, and downstream policies trained under standard behavior cloning and diffusionbased policy learning frameworks. Across these benchmarks, pre-training with H2R consistently improves downstream success rates, with average gains ranging from 1.3% to 10.2% depending on the encoder and task suite.

In real-world experiments, we deploy H2R-enhanced visual encoders on multiple robotic platforms, including a UR5 arm with parallel grippers, a UR5 arm with a dexterous Leaphand, and dual-arm systems based on Franka and UR5e. Policies are trained using both Diffusion Policy [7] and ACT [57]. Across gripper-based, dexterous, and bimanual manipulation tasks, H2R yields consistent performance improvements in realworld success rates, with gains ranging from 3.3% to 23.3% across different encoder–policy combinations.

Beyond these primary evaluations, we conduct additional studies to characterize the generalization properties of H2R. These include experiments on pre-training with different egocentric datasets, cross-embodiment transfer where the augmentation embodiment differs from the downstream robot, robustness analyses under varying demonstration densities and lighting conditions, and integration with vision–language–action models through targeted fine-tuning. Collectively, these results demonstrate that explicitly reducing the human-to-robot visual gap during pre-training leads to robust and transferable improvements in downstream robotic manipulation performance.

## II. RELATED WORK

Robot Imitation Learning. Data-driven policy learning [31, 34, 53, 55, 7, 38] has enabled robots to autonomously perform tasks such as grasping, locomotion, and manipulation. Imitation learning [7, 56, 57, 36] trains policies from successful demonstrations, often supervised by behavior cloning [52, 15] objectives. ACT [57] addresses non-Markovian dynamics by fusing temporal sequences, while diffusion models [7, 56] are introduced to handle the inherent multimodality of robot motions.

Visual Encoder Pretraining for Robotics. Visual pretraining improves generalization of robotic policies across diverse tasks. Researchers have explored architectural designs [21, 11], training objectives [22, 5, 6], and dataset compositions [9, 33, 48, 47]. PVR-Control [39] shows that pretrained visual representations can outperform direct state-based policies. RPT [45] tokenizes observations to enable masked prediction pretraining. Methods like MVP [43] and R3M [37] utilize self-supervised objectives on videos to learn representations transferable to reinforcement learning. Voltron [27] demonstrates the use of MAE and contrastive learning for hierarchical robot control. Cross-Domain Visual Alignment. Bridging the domain gap between human and robot visual inputs remains a major challenge. WHIRL [2] matches task structure from thirdperson views, while RoVi-Aug [4] and Mirage [44] manipulate appearance via segmentation or image-space preprocessing. EgoMimic [28] removes hands and normalizes views to align egocentric perspectives.

![[99_Attachments/papers/images/h2r/8e29df95475be9c77a617dbfec61cf50ba2717a7b2b6aff7483df4968d0a0681.jpg]]  
Fig. 2: H2R Pipeline. The H2R pipeline includes three steps: (1) hand pose estimation, (2) retargeting to simulate robot arm movements, and (3) removal and inpainting of the human hand to create an augmented image with the robot arm, ensuring seamless integration.

## III. H2R: HUMAN-TO-ROBOT DATA AUGMENTATION

In this section, we present H2R, a human-to-robot data augmentation framework that converts egocentric human-hand videos into robot-centric visual observations. We detail the full augmentation pipeline, including (1)hand pose estimation, (2)retargeting, and (3)removal and inpainting, and further validate the quality of the generated data using a CLIP-based semantic consistency evaluation. An overview of the pipeline is shown in Figure 2.

## A. H2R Data Augmentation Pipeline

Step1: Hand Pose Estimation. To overlay the human hands in the egocentric image with different robots, we first need an efficient and accurate model to detect hand information. We adopt HaMeR [40], a state-of-the-art model for 3D hand detection and reconstruction, to accurately locate the hand in the image. This step outputs the position of the human hand, keypoints, and the intrinsic and extrinsic parameters of the camera. The hand position will be used in Step 3 (Removal and Inpainting) to segment the human hand, while the keypoints and camera parameters are used in Step 2 (Retargeting) to adjust the robot’s pose and camera position.

Step2: Retargeting. In this step, we simulate the robot arm to mirror the human hand’s movements detected in Step 1. Using the hand keypoints and camera parameters from Step 1, we calculate the joint angles of the robot arm.

We first build the robotic arm and its end-effectors, which are typically either grippers or dexterous hands. For dexterous hands, we estimate joint angles from hand keypoints predicted by HaMeR. Each finger joint angle is calculated using three consecutive keypoints along that finger. For grippers, we determine how open or closed they are based on the Euclidean distance between the corresponding fingertips. Since hand keypoints don’t capture the full arm pose (especially for joints unrelated to the hand), we manually set reasonable values for the remaining arm joints to complete a plausible robot configuration.

Next, we use the hand keypoints and camera parameters from HaMeR to adjust the camera pose in the simulator. Specifically, we define two coordinate systems: $C _ { H }$ , the coordinate system aligned with the human hand, and $C _ { S }$ , the coordinate system of the robotic arm in the simulator. By mapping the position of the camera in $C _ { H } \ { \mathrm { t o } } \ C _ { S }$ , we can ensure that the camera in the simulator shares the same perspective as the one captured in the real-world egocentric human image. The original camera position $W _ { \mathbf { c a m } _ { r e a l } }$ in the world frame is transformed to the aligned simulator position $W _ { \mathbf { c a m } _ { s i m } }$ using transformations from human hand $( _ { H } ^ { \mathbf { \bar { W } } } \mathbf { R } )$ and robot simulator $( \mathbf { \sp { W } R } )$ coordinate systems:

$$
{ } ^ { W } \mathbf { c a m } _ { s i m } = _ { S } ^ { W } \mathbf { R } _ { H } ^ { W } \mathbf { R } ^ { - 1 } { } ^ { W } \mathbf { c a m } _ { r e a l }\tag{1}
$$

Step3: Removal and Inpainting. After the robot pose is retargeted in Step 2, we proceed to remove the human hand from the image. We use the hand position and keypoints from Step 1 to segment out the human hand and arm regions using the Segment Anything Model (SAM) [30].

Then, to obtain clean backgrounds for inserting robotic arms, we apply LaMa [51], a powerful inpainting model, to fill in the removed hand-arm region. This yields clean RGB images without human limbs, providing a seamless background for inserting robotic arms in the subsequent steps.

Once both the arm segmentation from Step 2 and the inpainted image from Step 3 are available, we overlay the robot arm onto the inpainted image. We directly obtain the pixel coordinates of the human hand keypoints from Step 1. In parallel, the pixel coordinates of the robot endeffector links are computed in the simulator by projecting their 3D positions through the aligned camera using the known transformation matrices. By aligning the robot link positions with the corresponding human hand keypoints in pixel space, we ensure that the overlaid robot hand accurately matches the position and orientation of the original hand in the image, achieving precise pixel-level alignment.

## B. Data Quality Evaluation

We evaluate the visual plausibility and semantic consistency of H2R-augmented data using a vision–language similarity metric based on CLIP [42]. The evaluation procedure is illustrated in Figure 3, which also shows six representative pairs of original human frames and their corresponding H2Raugmented robot-centric images.

For each image, we associate a high-level verb–noun action description. Specifically, given an original human frame and its H2R-augmented counterpart, we construct two textual prompts describing the same action from different perspectives: a human-centric prompt (“A human is [action]”) and a robotcentric prompt (“A robotic arm is [action]”). Image–text cosine similarity is then computed using CLIP ViT-B/32 [42], measuring how well each image aligns with its corresponding semantic description.

To quantify data quality at scale, we randomly sample 1,000 image pairs from the pre-training dataset. For each pair, the action phrase is automatically generated using Qwen-2.5-VL [3]. We report the average CLIP similarity between original images and human-centric prompts, and between H2Raugmented images and robot-centric prompts.

The original human images achieve an average similarity score of 28.01, while H2R-augmented images reach 29.83. This result indicates that H2R consistently improves semantic alignment with robot-centric action descriptions. Overall, the CLIP-based evaluation provides a scalable measure of data quality, supporting the effectiveness of H2R in generating visually and semantically coherent training data for robotic visual pre-training.

## IV. EXPERIMENT

In this section, we conduct a comprehensive experimental evaluation of H2R. Experimental configurations are summarized in Table I. In simulation, we conduct imitation learning experiments across multiple benchmark suites, including studies on generalization across pre-training datasets, comparisons with robotic-data pre-training, and the effect of demonstration density. On real robots, we perform manipulation experiments across multiple platforms and task settings, together with studies on cross-embodiment transfer, compatibility with Vision-Language-Action models, component ablations, and robustness under lighting variations.

## A. Experimental Setup

Visual Representation Pre-training. We adopt the MAE [23, 53] and R3M [37] frameworks for visual encoder pre-training, both using a Vision Transformer (ViT-Base) [12] architecture. Pre-training is conducted on subsets of SSv2 (1M images) or Ego4D (117K clips).

For each framework, we consider two settings: pre-training on the original human video data and pre-training with additional H2R augmentation. H2R overlays robot embodiments onto human videos using three representative robot types: UR5 with Robotiq Gripper, UR5 with Leaphand, and Franka with Robotiq Gripper. Except for cross-embodiment experiments, the robot embodiment used for H2R augmentation is matched to the robot platform of the downstream task.

![[99_Attachments/papers/images/h2r/f48963e43da715b1276dbbd14f6bcbcdf478c1d46653ac8ed2bfefa2011feae6.jpg]]  
Fig. 3: Illustration of the CLIP-based quality evaluation. We evaluate augmentation quality by comparing CLIP image–text similarity under human-centric and robot-centric action prompts for original versus H2R-augmented images. The results show that H2R improves semantic alignment with robot-centric action descriptions, demonstrating the effectiveness of H2R in generating semantically coherent training data for robotic pre-training.

Simulation Benchmark. For each pre-training method, we evaluate the performance of pre-trained encoders in imitation learning. Specifically, we select a total of 10 simulation tasks in different environments, which are from Robomimic [36], RLBench [24], PushT [7] and CortexBench [35]. In particular, for Robomimic, we train the policies using the behavior cloning (BC) and evaluate them on tasks such as MoveCan, Square, and Lift, where the robot performs actions such as moving or lifting objects. For RLBench, we train the policies with Diffusion Policy and evaluate them on three manipulation tasks: Close Box, Close Laptop Lid and Toilet Seat Down. We use the PushT task in the Diffusion Policy evaluation framework, which evaluates a robot’s ability to push an object to a target location. We also use three MetaWorld tasks: Assembly, ButtonPress and Hammer from VC-1 Cortex benchmark for evaluation.

Real-world Setup. We evaluate the effectiveness of H2R across four real-world manipulation setups: (i) a UR5 arm equipped with a Robotiq Gripper [46], (ii) a UR5 arm equipped with a Leaphand end effector [49], (iii) a dualarm Franka Emika system with parallel grippers, and (iv) a dual-arm UR5e platform configured as a human-like bimanual manipulation setup. Across these platforms, we evaluate a diverse set of real-world manipulation tasks spanning gripperbased, dexterous, and bimanual manipulation; detailed task definitions are summarized in Table II.

TABLE I: Summary of Experimental Settings. This table outlines the hyperparameters, datasets, and configurations used for encoder pre-training, simulation benchmarks, and real-world robotic tasks.

<table><tr><td>Phase</td><td>Component</td><td>Framework</td><td>Key Configurations</td></tr><tr><td rowspan="4">Encoder Pretraining</td><td rowspan="2">Method</td><td>MAE</td><td>ViT-B, 800 epochs, batch size 128, learning rate  $4 \times 10^{-4}$ ,  $8 \times$ A800 GPUs.</td></tr><tr><td>R3M</td><td>ViT-B, 20K steps, batch size 256, learning rate  $1 \times 10^{-4}$ ,  $8 \times$ A800 GPUs.</td></tr><tr><td rowspan="2">Dataset</td><td>SSv2</td><td>~1M frames (subset), original vs. H2R-augmented.</td></tr><tr><td>Ego4D</td><td>117K clips subset (~1M frames), original vs. H2R-augmented.</td></tr><tr><td rowspan="6">Simulation Setup</td><td rowspan="4">Benchmark</td><td>Robomimic</td><td>200 epochs, 3 tasks.</td></tr><tr><td>RLBench</td><td>800 epochs, 3 tasks.</td></tr><tr><td>PushT</td><td>200 epochs, 1 task.</td></tr><tr><td>CortexBench</td><td>100 epochs, 3 tasks.</td></tr><tr><td rowspan="2">Policy</td><td>BC</td><td>3-layer MLP (Robomimic, CortexBench), default hyperparameters.</td></tr><tr><td>DP</td><td>Diffusion Policy (PushT, RLBench), default hyperparameters.</td></tr><tr><td rowspan="7">Real-world Setup</td><td rowspan="4">Scene</td><td>UR5-Gripper</td><td>3 tasks, keyboard-based teleoperation for collection, 1 camera, 30 demos.</td></tr><tr><td>UR5-Leaphand</td><td>3 tasks, vision-guided teleoperation for collection, 1 camera, 50 demos.</td></tr><tr><td>Dual-arm Franka</td><td>3 tasks, homogeneous-arm bilateral teleoperation for collection, 3 cameras, 300 demos.</td></tr><tr><td>Dual-arm UR5e</td><td>2 tasks, homogeneous-arm bilateral teleoperation for collection, 3 cameras, 300 demos.</td></tr><tr><td rowspan="3">Policy</td><td>DP</td><td>300 epochs (UR5-Gripper), 3000 epochs (UR5-Leaphand), 9000 epochs (dual-arm).</td></tr><tr><td>ACT</td><td>300 epochs (UR5-Gripper), 3000 epochs (UR5-Leaphand), 9000 epochs (dual-arm).</td></tr><tr><td>UVA</td><td>Default UVA configuration, 3000 epochs.</td></tr></table>

Demonstration data are collected through human teleoperation, with the collection interface adapted to the manipulation setting. Specifically, gripper-based tasks are collected using keyboard-based teleoperation, Leaphand tasks using visionguided teleoperation following the same setup as in Cord-ViP [16], and dual-arm tasks using homogeneous-arm bilateral teleoperation [54]. The number of demonstrations varies across setups and task categories, ranging from 30 to 300 episodes depending on task complexity, as summarized in Table I.

For policy training, we adopt Diffusion Policy (DP) [7] and ACT [57] as policy frameworks. We apply the pre-trained MAE and R3M visual encoders to downstream policy learning.

During evaluation, target objects are randomly initialized within predefined regions following a uniform distribution consistent with expert demonstrations. Each task is executed for 20 rollouts, and success rates are reported as the primary evaluation metric.

## B. Simulation Results

Performance on Simulation Benchmarks. Table III shows that visual encoders pre-trained with H2R consistently outperform those trained on the original SSv2 dataset across all evaluated simulation benchmarks for both MAE and R3M visual encoders. For Robomimic tasks, H2R leads to clear improvements for both encoders. MAE achieves a 10.2% increase in average success rate, while R3M improves by 6.3%. Notably, MAE observes a substantial 25.5% gain on the MoveCan task. Similar trends are observed on PushT, RLBench, and CortexBench, with consistent performance gains across the evaluated tasks for both MAE and R3M. These results demonstrate that H2R augmentation consistently enhances the effectiveness of visual representations learned from large-scale human video datasets for downstream imitation learning across diverse simulation environments.

Generalization Across Pre-training Datasets. We evaluate H2R using Ego4D to assess its generalization beyond SSv2. Specifically, we pre-train both MAE and R3M on an Ego4D subset of comparable scale to SSv2, following the same training protocol as in the previous experiments. Table IV reports the resulting imitation learning performance on the PushT task and RLBench benchmarks. On PushT, H2R leads to improvement for MAE (+2.2%) while preserving the same performance for R3M. On RLBench, H2R improves the average success rate for both encoders, with MAE increasing from 1.7% to 5.0% and R3M from 6.7% to 11.7%.

These results indicate that the benefits of H2R are not specific to SSv2, and can be consistently transferred to visual representations pre-trained on Ego4D, supporting the general applicability of H2R across different sources of large-scale human video data.

Pretraining on Robotic Datasets. We further compare H2R with visual representations pretrained directly on robotic datasets by including models pretrained on the DROID dataset [29], following the setting reported in the recent study [26]. All models use the R3M framework for pretraining, where R3M is pretrained on SSv2, R3M-DROID is pretrained on the DROID robotic dataset, and R3M-H2R is pretrained on the H2R-augmented SSv2 dataset. We evaluate all representations on the same Robomimic benchmarks. As shown in Table V, both robotic data pre-training and H2R augmentation lead to performance improvements over SSv2- only pre-training. However, R3M-H2R achieves the strongest overall results. Despite DROID being collected from real world robotic executions, H2R pre-training achieves stronger downstream manipulation performance, suggesting that humanto-robot visual augmentation offers an effective alternative to direct robotic data pretraining.

Effects of Demonstration Density. We observe relatively low success rates on RLBench under sparse, keypoint-based supervision, a setting commonly adopted in prior RLBench works to improve training efficiency [18, 25, 50]. This obser-

![[99_Attachments/papers/images/h2r/39cd601d4b54c0728c3b24934f631d3d74303384f7cea3ace2e9302937c1a94f.jpg]]

<table><tr><td>Embodiment</td><td>Task Name</td><td>Task Description</td></tr><tr><td rowspan="3">UR5-Gripper</td><td>PickCube</td><td>The robot grasps a cube and places it into a bowl.</td></tr><tr><td>Stack</td><td>The robot stacks a blue cube on top of a yellow cube.</td></tr><tr><td>CloseBox</td><td>The robot retrieves a cube from a box, places it into a bowl, and closes the box lid.</td></tr><tr><td rowspan="3">UR5-Leaphand</td><td>GraspChicken</td><td>The robot grasps a toy chicken and places it into a bowl.</td></tr><tr><td>StandCup</td><td>The robot grasps a fallen cup and places it upright on the table.</td></tr><tr><td>OpenBox</td><td>The robot opens an articulated box lid using the dexterous hand.</td></tr><tr><td rowspan="3">Dual-arm Franka</td><td>PlaceToy</td><td>The left arm grasps a toy from a pink box, and the right arm transfers it into a blue box.</td></tr><tr><td>SweepRubbish</td><td>The left arm sweeps trash into a dustpan held by the right arm.</td></tr><tr><td>WeighSauce</td><td>The left arm places a cup onto a scale, while the right arm performs a pouring motion with a bottle.</td></tr><tr><td rowspan="2">Dual-arm UR5e</td><td>PlaceBowl</td><td>The robot places a green bowl on top of a blue bowl.</td></tr><tr><td>StackBlocks</td><td>The robot stacks blocks in the order of red, yellow, and blue to form a single tower.</td></tr></table>

TABLE III: Simulation Benchmark Results. Success rates (%↑) across diverse imitation learning suites. Bold indicates the best performance within each group, and green/red denotes the performance gain/drop after applying H2R. All subsequent tables follow the same rule.

<table><tr><td rowspan="2">Method</td><td colspan="4">Robomimic</td><td>PushT</td><td colspan="4">RLBench</td><td colspan="4">CortexBench</td></tr><tr><td>MoveCan</td><td>Square</td><td>Lift</td><td>Avg.</td><td>PushT</td><td>CloseBox</td><td>CloseLaptopLid</td><td>ToiletSeatDown</td><td>Avg.</td><td>Assembly</td><td>ButtonPress</td><td>Hammer</td><td>Avg.</td></tr><tr><td>MAE (SSv2)</td><td>54.0</td><td>25.5</td><td>94.5</td><td>58.0</td><td>59.2</td><td>0.0</td><td>10.0</td><td>0.0</td><td>3.3</td><td>84.0</td><td>80.0</td><td>96.0</td><td>86.7</td></tr><tr><td>MAE (H2R)</td><td>79.5</td><td>29.5</td><td>95.5</td><td>68.2</td><td>64.5</td><td>5.0</td><td>15.0</td><td>20.0</td><td>13.3</td><td>88.0</td><td>88.0</td><td>100.0</td><td>92.0</td></tr><tr><td>Gain (Δ)</td><td>+25.5</td><td>+4.0</td><td>+1.0</td><td>+10.2</td><td>+5.3</td><td>+5.0</td><td>+5.0</td><td>+20.0</td><td>+10.0</td><td>+4.0</td><td>+8.0</td><td>+4.0</td><td>+5.3</td></tr><tr><td>R3M (SSv2)</td><td>59.5</td><td>20.5</td><td>85.0</td><td>55.0</td><td>15.0</td><td>0.0</td><td>20.0</td><td>10.0</td><td>10.0</td><td>76.0</td><td>56.0</td><td>88.0</td><td>73.3</td></tr><tr><td>R3M (H2R)</td><td>61.5</td><td>37.5</td><td>85.0</td><td>61.3</td><td>22.0</td><td>5.0</td><td>20.0</td><td>20.0</td><td>15.0</td><td>68.0</td><td>60.0</td><td>96.0</td><td>74.7</td></tr><tr><td>Gain (Δ)</td><td>+2.0</td><td>+17.0</td><td>0.0</td><td>+6.3</td><td>+7.0</td><td>+5.0</td><td>0.0</td><td>+10.0</td><td>+5.0</td><td>-8.0</td><td>+4.0</td><td>+8.0</td><td>+1.3</td></tr></table>

TABLE IV: Simulation Results with Ego4D Pre-training. Success rates (%↑) on PushT and RLBench when pre-training MAE/R3M on an Ego4D subset, comparing original vs. H2R-augmented pre-training.

<table><tr><td rowspan="2">Method</td><td>PushT</td><td colspan="4">RLBench</td></tr><tr><td>PushT</td><td>CloseBox</td><td>CloseLaptopLid</td><td>ToiletSeatDown</td><td>Avg.</td></tr><tr><td>MAE (Ego4D)</td><td>51.3</td><td>0.0</td><td>0.0</td><td>5.0</td><td>1.7</td></tr><tr><td>MAE (H2R)</td><td>53.5</td><td>10.0</td><td>5.0</td><td>0.0</td><td>5.0</td></tr><tr><td>Gain (Δ)</td><td>+2.2</td><td>+10.0</td><td>+5.0</td><td>-5.0</td><td>+3.3</td></tr><tr><td>R3M (Ego4D)</td><td>13.6</td><td>10.0</td><td>5.0</td><td>5.0</td><td>6.7</td></tr><tr><td>R3M (H2R)</td><td>13.6</td><td>15.0</td><td>5.0</td><td>15.0</td><td>11.7</td></tr><tr><td>Gain (Δ)</td><td>0.0</td><td>+5.0</td><td>0.0</td><td>+10.0</td><td>+5.0</td></tr></table>

vation motivates an additional study to examine whether the effectiveness of H2R depends on demonstration density, by comparing sparse and dense RLBench training under identical

TABLE V: Comparison to Robotic-data Pre-training. Robomimic success rates (%↑) for R3M pre-training on SSv2, robotic dataset (DROID), and H2R-augmented SSv2, highlighting H2R as an alternative to direct robotic-data pre-training.

<table><tr><td>Method</td><td>MoveCan</td><td>Square</td><td>Lift</td><td>Avg.</td></tr><tr><td>R3M</td><td>59.5</td><td>20.5</td><td>85.0</td><td>55.0</td></tr><tr><td>R3M-DROID</td><td>54.0</td><td>22.0</td><td>96.0</td><td>56.7</td></tr><tr><td>R3M-H2R</td><td>61.5</td><td>37.5</td><td>85.0</td><td>61.3</td></tr></table>

settings.

As shown in Table VII, increasing demonstration density substantially improves overall task performance (e.g., MAE

TABLE VI: Real-world Task Results. Success rates (%↑) on gripper, dexterous (Leaphand), and bimanual (Franka) tasks using DP and ACT policies with MAE/R3M visual encoders. Rows denote pre-training variants, and columns denote tasks. (a) DP Policy.

<table><tr><td rowspan="3">Policy</td><td rowspan="3">Method</td><td colspan="12">Tasks</td></tr><tr><td colspan="4">Gripper</td><td colspan="4">Leaphand</td><td colspan="4">Franka</td></tr><tr><td>PickCube</td><td>Stack</td><td>CloseBox</td><td>Avg.</td><td>GraspChicken</td><td>StandCup</td><td>OpenBox</td><td>Avg.</td><td>PlaceToy</td><td>SweepRubbish</td><td>WeighSauce</td><td>Avg.</td></tr><tr><td rowspan="6">DP</td><td>MAE (SSv2)</td><td>45.0</td><td>50.0</td><td>55.0</td><td>50.0</td><td>40.0</td><td>35.0</td><td>45.0</td><td>40.0</td><td>10.0</td><td>15.0</td><td>40.0</td><td>21.7</td></tr><tr><td>MAE (H2R)</td><td>65.0</td><td>55.0</td><td>50.0</td><td>56.7</td><td>55.0</td><td>60.0</td><td>65.0</td><td>60.0</td><td>15.0</td><td>15.0</td><td>45.0</td><td>25.0</td></tr><tr><td>Gain (Δ)</td><td>+20.0</td><td>+5.0</td><td>-5.0</td><td>+6.7</td><td>+15.0</td><td>+25.0</td><td>+20.0</td><td>+20.0</td><td>+5.0</td><td>0.0</td><td>+5.0</td><td>+3.3</td></tr><tr><td>R3M (SSv2)</td><td>40.0</td><td>55.0</td><td>45.0</td><td>46.7</td><td>10.0</td><td>20.0</td><td>40.0</td><td>23.3</td><td>10.0</td><td>20.0</td><td>20.0</td><td>17.7</td></tr><tr><td>R3M (H2R)</td><td>50.0</td><td>70.0</td><td>65.0</td><td>61.7</td><td>35.0</td><td>50.0</td><td>45.0</td><td>43.3</td><td>25.0</td><td>20.0</td><td>30.0</td><td>25.0</td></tr><tr><td>Gain (Δ)</td><td>+10.0</td><td>+15.0</td><td>+20.0</td><td>+15.0</td><td>+25.0</td><td>+30.0</td><td>+5.0</td><td>+20.0</td><td>+15.0</td><td>0.0</td><td>+10.0</td><td>+7.3</td></tr></table>

(b) ACT Policy.

<table><tr><td rowspan="3">Policy</td><td rowspan="3">Method</td><td colspan="12">Tasks</td></tr><tr><td colspan="4">Gripper</td><td colspan="4">Leaphand</td><td colspan="4">Franka</td></tr><tr><td>PickCube</td><td>Stack</td><td>CloseBox</td><td>Avg.</td><td>GraspChicken</td><td>StandCup</td><td>OpenBox</td><td>Avg.</td><td>PlaceToy</td><td>SweepRubbish</td><td>WeighSauce</td><td>Avg.</td></tr><tr><td rowspan="6">ACT</td><td>MAE (SSv2)</td><td>25.0</td><td>20.0</td><td>35.0</td><td>26.7</td><td>45.0</td><td>25.0</td><td>30.0</td><td>33.3</td><td>25.0</td><td>20.0</td><td>30.0</td><td>25.0</td></tr><tr><td>MAE (H2R)</td><td>30.0</td><td>35.0</td><td>40.0</td><td>35.0</td><td>50.0</td><td>50.0</td><td>40.0</td><td>46.7</td><td>40.0</td><td>35.0</td><td>35.0</td><td>36.7</td></tr><tr><td>Gain (Δ)</td><td>+5.0</td><td>+15.0</td><td>+5.0</td><td>+8.3</td><td>+5.0</td><td>+25.0</td><td>+10.0</td><td>+13.3</td><td>+15.0</td><td>+15.0</td><td>+5.0</td><td>+11.7</td></tr><tr><td>R3M(SSv2)</td><td>25.0</td><td>20.0</td><td>40.0</td><td>28.3</td><td>10.0</td><td>20.0</td><td>15.0</td><td>15.0</td><td>20.0</td><td>20.0</td><td>20.0</td><td>20.0</td></tr><tr><td>R3M (H2R)</td><td>30.0</td><td>40.0</td><td>50.0</td><td>40.0</td><td>35.0</td><td>60.0</td><td>20.0</td><td>38.3</td><td>30.0</td><td>20.0</td><td>25.0</td><td>25.0</td></tr><tr><td>Gain (Δ)</td><td>+5.0</td><td>+20.0</td><td>+10.0</td><td>+11.7</td><td>+25.0</td><td>+40.0</td><td>+5.0</td><td>+23.3</td><td>+10.0</td><td>0.0</td><td>+5.0</td><td>+5.0</td></tr></table>

TABLE VII: Effects of Demonstration Density. Success rates (%↑) under sparse vs. dense RLBench demonstrations, comparing MAE encoders pre-trained with and without H2R.

<table><tr><td>Data</td><td>Model</td><td>CloseBox</td><td>CloseLaptopLid</td><td>ToiletSeatDown</td><td>Avg.</td></tr><tr><td rowspan="3">Sparse data</td><td>MAE</td><td>0.0</td><td>10.0</td><td>0.0</td><td>3.3</td></tr><tr><td>MAE (H2R)</td><td>5.0</td><td>15.0</td><td>20.0</td><td>13.3</td></tr><tr><td>Gain (Δ)</td><td>+5.0</td><td>+5.0</td><td>+20.0</td><td>+10.0</td></tr><tr><td rowspan="3">Dense data</td><td>MAE</td><td>50.0</td><td>40.0</td><td>45.0</td><td>45.0</td></tr><tr><td>MAE (H2R)</td><td>60.0</td><td>45.0</td><td>60.0</td><td>55.0</td></tr><tr><td>Gain (Δ)</td><td>+10.0</td><td>+5.0</td><td>+15.0</td><td>+10.0</td></tr></table>

average success rate increases from 3.3% to 45.0%). More importantly, H2R consistently yields performance gains in both sparse and dense regimes. This result indicates that H2R is not tailored to a specific data density, but instead provides robust visual representations that remain effective across different demonstration settings.

## C. Real-world Results

Performance on Real-world Manipulation Tasks. In realworld experiments, we evaluate H2R on three categories of manipulation tasks-gripper, dexterous, and bimanual—using corresponding robotic platforms, including a UR5 equipped with a Robotiq gripper, a UR5 equipped with a Leaphand end effector, and a dual-arm Franka system. We adopt Diffusion Policy (DP) [7] and ACT [57] as policy frameworks, with visual encoders pre-trained using MAE and R3M. In this setting, the robot embodiment used for H2R augmentation during pretraining is identical to that used in downstream policy training and evaluation.

As shown in Table VI, H2R consistently improves real-world success rates across all task categories, encoders, and policies. Notably, the most pronounced gains are observed on Leaphand tasks, where H2R improves average performance by 20.0% (MAE, R3M) under DP, and by 13.3% (MAE) and 23.3% (R3M) under ACT. Gripper-based and dual-arm Franka tasks also benefit from H2R, with consistent improvements across both MAE and R3M. These results demonstrate that H2R effectively enhances real-world manipulation performance.

TABLE VIII: Real-world results with Ego4D pre-training. Success rates (%↑) on UR5-Leaphand tasks using ACT, comparing Ego4D pre-training with vs. without H2R augmentation.

<table><tr><td>Method</td><td>GraspChicken</td><td>StandCup</td><td>OpenBox</td><td>Avg.</td></tr><tr><td>MAE (Ego4D)</td><td>25.0</td><td>25.0</td><td>35.0</td><td>28.3</td></tr><tr><td>MAE (H2R)</td><td>35.0</td><td>50.0</td><td>45.0</td><td>43.3</td></tr><tr><td>Gain (Δ)</td><td>+10.0</td><td>+25.0</td><td>+10.0</td><td>+15.0</td></tr><tr><td>R3M (Ego4D)</td><td>15.0</td><td>20.0</td><td>30.0</td><td>21.7</td></tr><tr><td>R3M (H2R)</td><td>20.0</td><td>25.0</td><td>40.0</td><td>28.3</td></tr><tr><td>Gain (Δ)</td><td>+5.0</td><td>+5.0</td><td>+10.0</td><td>+6.7</td></tr></table>

Generalization Across Pre-training Datasets. To examine whether the effectiveness of H2R observed in simulation also extends to real-world settings, we further evaluate visual encoders pre-trained on Ego4D in real-world Leaphand manipulation tasks. Following the same pre-training protocol as in the simulation experiments, both MAE and R3M are trained on an Ego4D subset of comparable scale, with and without H2R augmentation, and deployed using the ACT policy.

Table VIII reports the success rates across three real-world Leaphand tasks. For MAE, applying H2R consistently improves performance on all tasks, increasing the average success rate from 28.3% to 43.3%. For R3M, H2R also yields consistent gains, with the average success rate improving from 21.7% to 28.3%.

These results are consistent with the trends observed in simulation and indicate that the benefits of H2R extend to real-world manipulation when visual encoders are pre-trained on Ego4D.

Cross-embodiment Generalization. We further evaluate the cross-embodiment generalization of H2R by applying H2Raugmented pre-training using a robot embodiment that differs from the one used in downstream policy training and evaluation. Specifically, we consider two augmentation settings during pre-training: UR5-based H2R and Franka-based H2R, while all downstream policies are trained and evaluated on UR5- Leaphand tasks.

As shown in Table IX, H2R continues to improve performance under embodiment mismatch for both MAE and R3M encoders, as well as for both DP and ACT policies. Using UR5-based H2R augmentation yields the strongest gains, with average success rates increasing by 20.0% (MAE) and 21.7% (R3M) under DP, and by 13.3% (MAE) and 23.3% (R3M) under ACT. When H2R is applied using Franka-based augmentation, performance improvements remain consistent but are generally smaller in magnitude.

TABLE IX: Cross-Embodiment Real-world Results. UR5-Leaphand task success rates (%↑) when the robot embodiment used for H2R augmentation during pre-training differs from the downstream embodiment (UR5-based vs. Franka-based augmentation). (a) DP Policy. (b) ACT Policy.

<table><tr><td>Policy</td><td>Method</td><td>GraspChicken</td><td>StandCup</td><td>OpenBox</td><td>Avg.</td></tr><tr><td rowspan="10">DP</td><td>MAE (SSv2)</td><td>40.0</td><td>35.0</td><td>45.0</td><td>40.0</td></tr><tr><td>MAE (H2R-UR5)</td><td>55.0</td><td>60.0</td><td>65.0</td><td>60.0</td></tr><tr><td>Gain (Δ)</td><td>+15.0</td><td>+25.0</td><td>+20.0</td><td>+20.0</td></tr><tr><td>MAE (H2R-Franka)</td><td>35.0</td><td>50.0</td><td>45.0</td><td>43.3</td></tr><tr><td>Gain (Δ)</td><td>-5.0</td><td>+15.0</td><td>0.0</td><td>+3.3</td></tr><tr><td>R3M (SSv2)</td><td>10.0</td><td>20.0</td><td>40.0</td><td>23.3</td></tr><tr><td>R3M(H2R-UR5)</td><td>35.0</td><td>50.0</td><td>45.0</td><td>43.3</td></tr><tr><td>Gain (Δ)</td><td>+25.0</td><td>+30.0</td><td>+5.0</td><td>+20.0</td></tr><tr><td>R3M(H2R-Franka)</td><td>20.0</td><td>30.0</td><td>45.0</td><td>31.7</td></tr><tr><td>Gain (Δ)</td><td>+10.0</td><td>+10.0</td><td>+5.0</td><td>+10.0</td></tr></table>

These results suggest that the effectiveness of H2R is not strictly limited to cases where the pre-training and downstream embodiments are identical. Within the evaluated settings, H2R remains beneficial even when the augmentation embodiment differs from that used in policy learning, indicating a certain degree of robustness to embodiment variation.

Synergy with Vision-Language-Action Models. A common paradigm in Vision-Language-Action (VLA) models is to initialize the visual backbone using encoders pre-trained on large-scale datasets (e.g., CLIP, VAEs). In this experiment, we investigate whether fine-tuning a pre-trained visual backbone on robot-oriented video data can enhance its suitability for robotic policy learning. Specifically, we fine-tune the pretrained VAE encoder and decoder used in the Unified Video Action Model(UVA) [32] separately on both the original SSv2 and the H2R-augmented datasets. The fine-tuned VAEs are subsequently frozen and integrated into the UVA framework for policy training on two distinct dual-arm UR5e robot tasks. The results shown in Table X demonstrate a clear performance trend in the different variants of the UVA model.

TABLE X: UVA with different visual backbones. Success rates (%↑) on dual-arm UR5e tasks when using UVA with original backbone, and with VAEs fine-tuned on SSv2 or H2R-augmented data.

<table><tr><td>Method</td><td>PlaceBowl</td><td>StackBlocks</td><td>Avg.</td></tr><tr><td>UVA</td><td>0.20</td><td>0.20</td><td>0.20</td></tr><tr><td>UVA (SSv2)</td><td>0.10</td><td>0.20</td><td>0.15</td></tr><tr><td>UVA (H2R)</td><td>0.40</td><td>0.30</td><td>0.35</td></tr></table>

Ablation Study. To evaluate the effectiveness of each component in H2R, we conduct ablation studies on two timeconsuming steps: (1) performing hand inpainting without overlaying a robotic arm (H2R w/o Overlay), and (2) overlaying the arm without precise alignment between the hand and the camera, instead using random pasting (H2R w/o Retarget). Table XI shows the necessity and effectiveness of each component in H2R. The first step leads to a significant drop in success rate due to the loss of critical human-object interaction pixels after inpainting. The second step fails to provide accurate motion cues for the model and introduces visual mismatches with real-world manipulation tasks.

<table><tr><td>Policy</td><td>Method</td><td>GraspChicken</td><td>StandCup</td><td>OpenBox</td><td>Avg.</td></tr><tr><td rowspan="10">ACT</td><td>MAE (SSv2)</td><td>45.0</td><td>25.0</td><td>30.0</td><td>33.3</td></tr><tr><td>MAE (H2R-UR5)</td><td>50.0</td><td>50.0</td><td>40.0</td><td>46.7</td></tr><tr><td>Gain (Δ)</td><td>+5.0</td><td>+25.0</td><td>+10.0</td><td>+13.3</td></tr><tr><td>MAE (H2R-Franka)</td><td>50.0</td><td>50.0</td><td>30.0</td><td>43.3</td></tr><tr><td>Gain (Δ)</td><td>+5.0</td><td>+25.0</td><td>0.0</td><td>+10.0</td></tr><tr><td>R3M (SSv2)</td><td>10.0</td><td>20.0</td><td>15.0</td><td>15.0</td></tr><tr><td>R3M (H2R-UR5)</td><td>35.0</td><td>60.0</td><td>20.0</td><td>38.3</td></tr><tr><td>Gain (Δ)</td><td>+25.0</td><td>+40.0</td><td>+5.0</td><td>+23.3</td></tr><tr><td>R3M (H2R-Franka)</td><td>40.0</td><td>25.0</td><td>5.0</td><td>23.3</td></tr><tr><td>Gain (Δ)</td><td>+30.0</td><td>+5.0</td><td>-10.0</td><td>+8.3</td></tr></table>

TABLE XI: Ablation Study. Ablation results by removing robot overlay (w/o Overlay) and camera-hand retargeting (w/o Retarget).

<table><tr><td>Policy</td><td>Method</td><td>GraspChicken</td><td>StandCup</td><td>OpenBox</td><td>Avg.</td></tr><tr><td rowspan="5">DP</td><td>H2R</td><td>55.0</td><td>60.0</td><td>65.0</td><td>60.0</td></tr><tr><td>H2R w/o Overlay</td><td>30.0</td><td>40.0</td><td>20.0</td><td>30.0</td></tr><tr><td>Gain (Δ)</td><td>-25.0</td><td>-20.0</td><td>-45.0</td><td>-30.0</td></tr><tr><td>H2R w/o Retarget</td><td>30.0</td><td>55.0</td><td>45.0</td><td>43.3</td></tr><tr><td>Gain (Δ)</td><td>-25.0</td><td>-5.0</td><td>-20.0</td><td>-16.7</td></tr><tr><td rowspan="5">ACT</td><td>H2R</td><td>50.0</td><td>50.0</td><td>40.0</td><td>46.7</td></tr><tr><td>H2R w/o Overlay</td><td>25.0</td><td>35.0</td><td>25.0</td><td>28.3</td></tr><tr><td>Gain (Δ)</td><td>-25.0</td><td>-15.0</td><td>-15.0</td><td>-18.3</td></tr><tr><td>H2R w/o Retarget</td><td>45.0</td><td>30.0</td><td>15.0</td><td>30.0</td></tr><tr><td>Gain (Δ)</td><td>-5.0</td><td>-20.0</td><td>-25.0</td><td>-16.7</td></tr></table>

TABLE XII: Generalization under Lighting Variations. Success rates (%↑) on UR5-Leaphand tasks under real-world lighting disturbances, comparing no augmentation, H2R, and H2R with lighting augmentation (H2R+LightAug).

<table><tr><td>Method</td><td>GraspChicken</td><td>StandCup</td><td>OpenBox</td><td>Avg.</td></tr><tr><td>MAE</td><td>10.0</td><td>20.0</td><td>5.0</td><td>11.7</td></tr><tr><td>MAE (H2R)</td><td>10.0</td><td>25.0</td><td>0.0</td><td>11.7</td></tr><tr><td>Gain (Δ)</td><td>0.0</td><td>+5.0</td><td>-5.0</td><td>0.0</td></tr><tr><td>MAE (H2R + LightAug)</td><td>20.0</td><td>40.0</td><td>25.0</td><td>28.3</td></tr><tr><td>Gain (Δ)</td><td>+10.0</td><td>+20.0</td><td>+20.0</td><td>+16.6</td></tr><tr><td>R3M</td><td>0.0</td><td>5.0</td><td>10.0</td><td>5.0</td></tr><tr><td>R3M (H2R)</td><td>0.0</td><td>15.0</td><td>10.0</td><td>8.3</td></tr><tr><td>Gain (Δ)</td><td>0.0</td><td>+10.0</td><td>0.0</td><td>+3.3</td></tr><tr><td>R3M (H2R + LightAug)</td><td>10.0</td><td>20.0</td><td>10.0</td><td>13.3</td></tr><tr><td>Gain (Δ)</td><td>+10.0</td><td>+15.0</td><td>0.0</td><td>+8.3</td></tr></table>

Robustness to Lighting Variations. To evaluate the generalization under varying lighting conditions, we introduce illumination disturbances during evaluation. Additionally, during training, we incorporate randomized lighting with varying directions and colors into the simulation environment for data augmentation. We compare three settings: no augmentation(MAE, R3M), H2R augmentation(H2R), and H2R with lighting disturbances(H2R+LightAug). As shown in Table XII, the model trained with H2R and lighting perturbations demonstrates significantly better generalization to real-world lighting variations than other baselines, highlighting the effectiveness of H2R in bridging the domain gap caused by lighting variations.

## V. CONCLUSION

We propose H2R, a data augmentation technique that bridges the visual gap between human hand demonstrations and robotic arm manipulations by replacing human hands in firstperson videos with robotic arm movements. Using 3D hand reconstruction and image inpainting models, H2R generates synthetic robotic arm manipulation sequences, making them more suitable for robot pre-training. Experiments across simulation benchmarks and real-world tasks demonstrate consistent improvements in success rates for encoders trained with various pre-training methods (e.g., MAE, R3M), highlighting the effectiveness and generalization of H2R. H2R enables efficient transfer of task knowledge from human demonstrations to robotic systems, reducing the reliance on costly robot-specific data collection.

## REFERENCES

[1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023.

[2] Shikhar Bahl, Abhinav Gupta, and Deepak Pathak. Human-to-robot imitation in the wild, 2022. URL https://arxiv.org/abs/2207.09450.

[3] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report, 2025. URL https://arxiv.org/abs/2502.13923.

[4] Lawrence Yunliang Chen, Chenfeng Xu, Karthik Dharmarajan, Muhammad Zubair Irshad, Richard Cheng, Kurt Keutzer, Masayoshi Tomizuka, Quan Vuong, and Ken Goldberg. Rovi-aug: Robot and viewpoint augmentation for cross-embodiment robot learning, 2024. URL https://arxiv.org/abs/2409.03403.

[5] Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton. A simple framework for contrastive learning of visual representations. arXiv preprint arXiv:2002.05709, 2020.

[6] Ting Chen, Simon Kornblith, Kevin Swersky, Mohammad Norouzi, and Geoffrey Hinton. Big self-supervised models are strong semi-supervised learners. arXiv preprint arXiv:2006.10029, 2020.

[7] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. arXiv preprint arXiv:2303.04137, 2023.

[8] Dima Damen, Hazel Doughty, Giovanni Maria Farinella, Sanja Fidler, Antonino Furnari, Evangelos Kazakos, Davide Moltisanti, Jonathan Munro, Toby Perrett, Will Price, et al. Scaling egocentric vision: The epic-kitchens dataset. In Proceedings of the European conference on computer vision (ECCV), pages 720–736, 2018.

[9] Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, and Li Fei-Fei. Imagenet: A large-scale hierarchical image database. In 2009 IEEE conference on computer vision and pattern recognition, pages 248–255. Ieee, 2009.

[10] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805, 2018.

[11] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby. An image is worth 16x16 words: Transformers for image recognition at scale. In 9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021. OpenReview.net, 2021. URL https://openreview.net/forum?id=YicbFdNTTy.

[12] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, et al. An image is worth 16x16 words: Transformers for image recognition at scale, 2021. URL https://arxiv.org/abs/2010.11929.

[13] Jiafei Duan, Yi Ru Wang, Mohit Shridhar, Dieter Fox, and Ranjay Krishna. Ar2-d2: Training a robot without a robot. In Conference on Robot Learning, pages 2838– 2848. PMLR, 2023.

[14] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Chenxi Wang, Junbo Wang, Haoyi Zhu, and Cewu Lu. Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot, 2023. URL https://arxiv.org/ abs/2307.00595.

[15] Pete Florence, Corey Lynch, Andy Zeng, Oscar Ramirez, Ayzaan Wahid, Laura Downs, Adrian Wong, Johnny Lee, Igor Mordatch, and Jonathan Tompson. Implicit behavioral cloning, 2021.

[16] Yankai Fu, Qiuxuan Feng, Ning Chen, Zichen Zhou, Mengzhen Liu, Mingdong Wu, Tianxing Chen, Shanyu Rong, Jiaming Liu, Hao Dong, et al. Cordvip: Correspondence-based visuomotor policy for dexterous manipulation in real-world. arXiv preprint arXiv:2502.08449, 2025.

[17] Samir Yitzhak Gadre, Gabriel Ilharco, Alex Fang, Jonathan Hayase, Georgios Smyrnis, Thao Nguyen, Ryan Marten, Mitchell Wortsman, Dhruba Ghosh, Jieyu Zhang, et al. Datacomp: In search of the next generation of multimodal datasets. Advances in Neural Information Processing Systems, 36, 2024.

[18] Ankit Goyal, Jie Xu, Yijie Guo, Valts Blukis, Yu-Wei Chao, and Dieter Fox. Rvt: Robotic view transformer for 3d object manipulation. In Conference on Robot Learning, pages 694–710. PMLR, 2023.

[19] Raghav Goyal, Samira Ebrahimi Kahou, Vincent Michalski, Joanna Materzynska, Susanne Westphal, Heuna Kim, Valentin Haenel, Ingo Fruend, Peter Yianilos, Moritz Mueller-Freitag, et al. The” something something” video database for learning and evaluating visual common sense. In Proceedings of the IEEE international conference on computer vision, pages 5842–5850, 2017.

[20] Kristen Grauman, Andrew Westbury, Eugene Byrne,

Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 18995– 19012, 2022.

[21] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), June 2016.

[22] Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollar, and Ross Girshick. Masked autoencoders are´ scalable vision learners. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 16000–16009, June 2022.

[23] Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollar, and Ross Girshick. Masked autoencoders are´ scalable vision learners. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 16000–16009, 2022.

[24] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J. Davison. Rlbench: The robot learning benchmark & learning environment. IEEE Robotics and Automation Letters, 2020.

[25] Yueru Jia, Jiaming Liu, Sixiang Chen, Chenyang Gu, Zhilue Wang, Longzan Luo, Lily Lee, Pengwei Wang, Zhongyuan Wang, Renrui Zhang, and Shanghang Zhang. Lift3d foundation policy: Lifting 2d large-scale pretrained models for robust 3d robotic manipulation, 2024. URL https://arxiv.org/abs/2411.18623.

[26] Guangqi Jiang, Yifei Sun, Tao Huang, Huanyu Li, Yongyuan Liang, and Huazhe Xu. Robots pre-train robots: Manipulation-centric robotic representation from largescale robot datasets, 2024. URL https://arxiv.org/abs/2410. 22325.

[27] Siddharth Karamcheti, Suraj Nair, Annie S. Chen, Thomas Kollar, Chelsea Finn, Dorsa Sadigh, and Percy Liang. Language-driven representation learning for robotics. In Robotics: Science and Systems (RSS), 2023.

[28] Simar Kareer, Dhruv Patel, Ryan Punamiya, Pranay Mathur, Shuo Cheng, Chen Wang, Judy Hoffman, and Danfei Xu. Egomimic: Scaling imitation learning via egocentric video, 2024. URL https://arxiv.org/abs/2410. 24221.

[29] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset, 2024. URL https://arxiv.org/abs/2403.12945.

[30] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Dollar,´ and Ross Girshick. Segment anything, 2023. URL https: //arxiv.org/abs/2304.02643.

[31] Sergey Levine, Peter Pastor, Alex Krizhevsky, Julian

Ibarz, and Deirdre Quillen. Learning hand-eye coordination for robotic grasping with deep learning and large-scale data collection. The International Journal of Robotics Research, 37(4-5):421–436, 2018. doi: 10.1177/0278364917710318.

[32] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model, 2025. URL https://arxiv.org/ abs/2503.00200.

[33] Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollar, and´ C. Lawrence Zitnick. Microsoft coco: Common objects in context. In David Fleet, Tomas Pajdla, Bernt Schiele, and Tinne Tuytelaars, editors, Computer Vision – ECCV 2014, pages 740–755, Cham, 2014. Springer International Publishing. ISBN 978-3-319-10602-1.

[34] Jianlan Luo, Charles Xu, Jeffrey Wu, and Sergey Levine. Precise and dexterous robotic manipulation via humanin-the-loop reinforcement learning, 2024.

[35] Arjun Majumdar, Karmesh Yadav, Sergio Arnaud, Yecheng Jason Ma, Claire Chen, Sneha Silwal, Aryan Jain, Vincent-Pierre Berges, Pieter Abbeel, Jitendra Malik, Dhruv Batra, Yixin Lin, Oleksandr Maksymets, Aravind Rajeswaran, and Franziska Meier. Where are we in the search for an artificial visual cortex for embodied intelligence?, 2024. URL https://arxiv.org/abs/2303.18240.

[36] Ajay Mandlekar, Danfei Xu, Josiah Wong, Soroush Nasiriany, Chen Wang, Rohun Kulkarni, Li Fei-Fei, Silvio Savarese, Yuke Zhu, and Roberto Mart´ın-Mart´ın. What matters in learning from offline human demonstrations for robot manipulation, 2021.

[37] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. arXiv preprint arXiv:2203.12601, 2022.

[38] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models, 2024. URL https://arxiv.org/abs/2310.08864.

[39] Simone Parisi, Aravind Rajeswaran, Senthil Purushwalkam, and Abhinav Gupta. The unsurprising effectiveness of pre-trained vision models for control. In Kamalika Chaudhuri, Stefanie Jegelka, Le Song, Csaba Szepesvari, Gang Niu, and Sivan Sabato, editors, Proceedings of the 39th International Conference on Machine Learning, volume 162 of Proceedings of Machine Learning Research, pages 17359–17371. PMLR, 17–23 Jul 2022. URL https://proceedings.mlr.press/v162/parisi22a.html.

[40] Georgios Pavlakos, Dandan Shan, Ilija Radosavovic, Angjoo Kanazawa, David Fouhey, and Jitendra Malik. Reconstructing hands in 3d with transformers, 2023. URL https://arxiv.org/abs/2312.05251.

[41] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language

supervision. In International conference on machine learning, pages 8748–8763. PMLR, 2021.

[42] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision, 2021. URL https://arxiv.org/abs/2103.00020.

[43] Ilija Radosavovic, Tete Xiao, Stephen James, Pieter Abbeel, Jitendra Malik, and Trevor Darrell. Real-world robot learning with masked visual pre-training, 2022.

[44] Ilija Radosavovic, Baifeng Shi, Letian Fu, Ken Goldberg, Trevor Darrell, and Jitendra Malik. Robot learning with sensorimotor pre-training. In 7th Annual Conference on Robot Learning, 2023. URL https://openreview.net/forum? id=3gh9hf3R6x.

[45] Ilija Radosavovic, Baifeng Shi, Letian Fu, Ken Goldberg, Trevor Darrell, and Jitendra Malik. Robot learning with sensorimotor pre-training. In Conference on Robot Learning, pages 683–693. PMLR, 2023.

[46] Robotiq Inc. Adaptive grippers. https://robotiq.com/ products/adaptive-grippers, 2025. Accessed: 2025-02-01.

[47] Christoph Schuhmann, Richard Vencu, Romain Beaumont, Robert Kaczmarczyk, Clayton Mullis, Aarush Katta, Theo Coombes, Jenia Jitsev, and Aran Komatsuzaki. Laion-400m: Open dataset of clip-filtered 400 million imagetext pairs. ArXiv, abs/2111.02114, 2021. URL https: //api.semanticscholar.org/CorpusID:241033103.

[48] Shuai Shao, Zeming Li, Tianyuan Zhang, Chao Peng, Gang Yu, Xiangyu Zhang, Jing Li, and Jian Sun. Objects365: A large-scale, high-quality dataset for object detection. In 2019 IEEE/CVF International Conference on Computer Vision (ICCV), pages 8429–8438, 2019. doi: 10.1109/ICCV.2019.00852.

[49] Kenneth Shaw, Ananye Agarwal, and Deepak Pathak. Leap hand: Low-cost, efficient, and anthropomorphic hand for robot learning, 2023. URL https://arxiv.org/abs/2309. 06440.

[50] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiver-actor: A multi-task transformer for robotic manipulation. In Conference on Robot Learning, pages 785–799. PMLR, 2023.

[51] Roman Suvorov, Elizaveta Logacheva, Anton Mashikhin, Anastasia Remizova, Arsenii Ashukha, Aleksei Silvestrov, Naejin Kong, Harshith Goka, Kiwoong Park, and Victor Lempitsky. Resolution-robust large mask inpainting with fourier convolutions, 2021. URL https://arxiv.org/abs/ 2109.07161.

[52] Faraz Torabi, Garrett Warnell, and Peter Stone. Behavioral cloning from observation. arXiv preprint arXiv:1805.01954, 2018.

[53] Tete Xiao, Ilija Radosavovic, Trevor Darrell, and Jitendra Malik. Masked visual pre-training for motor control. arXiv preprint arXiv:2203.06173, 2022.

[54] Zhiyuan Xu, Yinuo Zhao, Kun Wu, Ning Liu, Junjie Ji, Zhengping Che, Chi Harold Liu, and Jian Tang. Hacts: a human-as-copilot teleoperation system for robot learning,

2025. URL https://arxiv.org/abs/2503.24070.

[55] Jingyun Yang, Zi ang Cao, Congyue Deng, Rika Antonova, Shuran Song, and Jeannette Bohg. Equibot: Sim(3)- equivariant diffusion policy for generalizable and data efficient learning, 2024. URL https://arxiv.org/abs/2407. 01479.

[56] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In Proceedings of Robotics: Science and Systems (RSS), 2024.

[57] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. arXiv preprint arXiv:2304.13705, 2023.

## APPENDIX

## A. Details of Simulator Camera Position Alignment

We define two coordinate systems: $C _ { H }$ , the coordinate system aligned with the human hand, and $C _ { S }$ , the coordinate system of the robot arm in the simulator. We build the coordinate system ${ \cal W } _ { \mathbf { I } _ { H } }$ based on the hand keypoints:

$$
{ } ^ { W } \mathbf { I } _ { H } = \left\{ ^ { w } \mathbf { i } _ { H , x } , ^ { w } \mathbf { i } _ { H , y } , ^ { w } \mathbf { i } _ { H , z } \right\}\tag{2}
$$

Where $^ w \mathbf { i } _ { H , x } , ^ { w } \mathbf { i } _ { H , y } , ^ { w } \mathbf { i } _ { H , z }$ are unit vectors along the x-axes, y-axes and z-axes of the human hand coorinate system. With the keypoints get in HaMeR, we build the three axis of coordinates with the following functions:

$$
\begin{array}{r} ^ {w} \mathbf {i} _ {H, x} = ^ {w} \mathbf {i} _ {0, 9} \\ ^ {w} \mathbf {i} _ {H, y} = ^ {w} \mathbf {i} _ {0, 9} \times^ {w} \mathbf {i} _ {0, 1 3} \\ ^ {w} \mathbf {i} _ {H, z} = ^ {w} \mathbf {i} _ {H, x} \times^ {w} \mathbf {i} _ {H, y} \end{array}\tag{3}
$$

Where $w _ { \mathbf { i } _ { 0 , 9 } }$ and ${ w } _ { \mathbf { i } _ { 0 , 1 3 } }$ are unit vectors along the middle and ring fingers, respectively. In this notation, the first index (0) refers to the specific finger (middle or ring), and the second index (9 and 13) corresponds to the joint numbers along those fingers, as defined by the MANO model. Similarly, To construct the mapping from hand pose to robot arms, we need to get another coordinate system ${ } ^ { W } \mathbf { I } _ { S }$ in the simulator:

$$
{ } ^ { W } \mathbf { I } _ { S } = \{ ^ { w } \mathbf { i } _ { S , x } , ^ { w } \mathbf { i } _ { S , y } , ^ { w } \mathbf { i } _ { S , z } \}\tag{4}
$$

The method of determining the axis of coordinates is the same:

$$
\begin{array}{r} ^ {w} \mathbf {i} _ {S, x} = ^ {w} \mathbf {i} _ {0, 2} \\ ^ {w} \mathbf {i} _ {S, y} = ^ {w} \mathbf {i} _ {0, 2} \times^ {w} \mathbf {i} _ {0, 3} \\ ^ {w} \mathbf {i} _ {s, z} = ^ {w} \mathbf {i} _ {S, x} \times^ {w} \mathbf {i} _ {S, y} \end{array}\tag{5}
$$

Where $\mathbf { i } _ { 0 , 2 } , \mathbf { i } _ { 0 , 3 }$ are unit vectors along robot fingers that correspond to human middle and ring fingers and the index corresponds to the joint numbers defined by MANO. We build the following two coordinate transformation matrix to construct the mapping:

$$
\begin{array}{c} _ {H} ^ {W} \mathbf {R} = \left( \begin{array}{c c} ^ {W} \mathbf {I} _ {H} & \mathbf {k e y} _ {h u m a n} \\ \mathbf {O} & 1 \end{array} \right) \\ _ {S} ^ {W} \mathbf {R} = \left( \begin{array}{c c} ^ {W} \mathbf {I} _ {S} & \mathbf {k e y} _ {r o b o t} \\ \mathbf {O} & 1 \end{array} \right) \end{array}\tag{6}
$$

Where $\mathbf { k e y } _ { h u m a n } , \mathbf { k e y } _ { \mathbf { r o b o t } }$ are the positions of human wrist and robot wrist. After obtaining the two coordinate systems, we need to determine the position of the camera in the simulator $( ^ { W } \mathbf { c a m } _ { s i m } )$ and the position of the camera in the real world $( ^ { H } \mathbf { c a m } _ { R e a l } )$ , thus we can ensure we get the same pose of the human hand and robot arms

$$
\begin{array}{r} ^ {H} \mathbf {c a m} _ {R e a l} = _ {H} ^ {W} \mathbf {R} ^ {- 1} \times^ {W} \mathbf {c a m} _ {R e a l} \\ ^ {S} \mathbf {c a m} _ {s i m} = ^ {H} \mathbf {c a m} _ {R e a l} \\ ^ {W} \mathbf {c a m} _ {s i m} = _ {S} ^ {W} \mathbf {R} \times_ {H} ^ {W} \mathbf {R} ^ {- 1} \times^ {W} \mathbf {c a m} _ {R e a l} \end{array}\tag{7}
$$

## B. Additional Evaluation Details.

Figure 4 provides visualizations of the different simulation benchmarks, and Figure 5 illustrates the real-world experimental setup.

To better understand the limitations of our policy and the challenges encountered in real-world deployments, we present a qualitative analysis of failure cases from two representative tasks: a gripper-based task (Gripper-Stack) and a dexterous manipulation task (Gripper-StandCup). Figure 6 illustrates typical failure modes observed during execution.

In the Gripper-Stack task, we identify two major failure scenarios:

Case I: Grasp Failure Unnoticed. The robot arm fails to successfully grasp the blue cube. However, the policy proceeds as if the object had been grasped, moving toward the yellow cube and attempting to perform the stacking operation. This leads to a complete task failure.

Case II: Misaligned Placement. The robot successfully grasps the blue cube but fails to align it correctly on top of the yellow cube during the stacking phase, resulting in an unstable or failed placement.

In the Stand Cup task, similar issues emerge due to perception and control limitations:

Case I: Grasp Position Error. The Leaphand end-effector attempts to grasp the cup but fails to target the correct contact region. As a result, the cup slips out of the grasp during lifting, preventing task completion.

Case II: Insufficient Lifting Trajectory. Even when the grasp is successful, the lifting motion lacks sufficient amplitude or stability to fully stand the cup upright. The cup either tips over or fails to stand securely.

To enable fine-grained evaluation of policy performance and gain deeper insights into failure cases, we designed a task-specific evaluation rubric. Table XIV displays our rubric that the evaluator filled out when rolling out different policies. Take the DP policy as an example, the results in Table XIV demonstrate that H2R-augmented visual representation models not only improve overall success rates in real-world tasks, but also allow to accomplish more than half of the task consistently.

In addition to pre-training on the H2R data and raw data, we also applied a simple CutMix baseline to demonstrate the effectiveness of using the robotic arm to cover the human hand, which overlays a fixed set of specific images of robotic arms with grippers onto the original images, ensuring that the overlaid images cover the human hands as much as possible, without exceeding the detected bounding box. Our H2R is different from such baseline by employing robot hand construction to better match the pose of the hand and arm in the images. Based on the type of robotic arm used in CutMix, we categorize the augmented set into three types: CutMix1 represents the UR5 robotic arm, CutMix2 refers to the Franka robotic arm, and CutMix3 combines both the UR5 and Franka robotic arms.

From Table XIII, we observe that the encoder trained on H2R processed data shows consistent improvements across various tasks compared to the encoder trained on the original data,

![[99_Attachments/papers/images/h2r/f5278391f367a02829dabdabab2348b3d690d88532dbb358680eed748a94eb69.jpg]]  
Fig. 4: Simulation benchmark. We choose 3 tasks from the Robomimic, 3 tasks from the RLBench, and 3 tasks from the CortexBench, covering a range of robotic manipulation skills. We also include the PushT task, designed for the Diffusion Policy framework, as an additional benchmark to evaluate performance in a different task setup.

## UR5-Gripper

![[99_Attachments/papers/images/h2r/3b167b6d961063f95a99cc51fdd861635ee1425fce7111e2c07e5256ef8c1fcf.jpg]]

## UR5-Leaphand

![[99_Attachments/papers/images/h2r/f67d068b3c2f8ca54c0c219ee04408905ca4894e7a6e8019758f8472b5357c59.jpg]]

Dual-arm Franka  
![[99_Attachments/papers/images/h2r/f6702e8fc8283470f132329552524d48d20cd6ac148cc4defa22b1b35c47e94c.jpg]]

Dual-arm UR5  
![[99_Attachments/papers/images/h2r/b790a58c75f22fd3665989004573ad218615a2e4c7819547dc7e907e1c891198.jpg]]  
Fig. 5: Real-world Robot Setup. Illustration of different real-world experimental setup.

TABLE XIII: Robomimic Experiment result. We report the success rate (%) over IL-based tasks for MAE and R3M Robomimic.

<table><tr><td></td><td>MoveCan</td><td>Square</td><td>Lift</td><td>Average</td><td>PushT</td></tr><tr><td>MAE</td><td>54</td><td>25.5</td><td>94.5</td><td>58</td><td>59.2</td></tr><tr><td>MAE+CutMix1</td><td>72.0 (+18.0%)</td><td>30.0 (+4.5%)</td><td>95.0 (+0.5%)</td><td>65.7 (+7.7%)</td><td>37.5 (-21.7%)</td></tr><tr><td>MAE+CutMix2</td><td>58.0 (+4.0%)</td><td>36.0 (+10.5%)</td><td>90.0 (-4.5%)</td><td>61.3 (+3.3%)</td><td>40.0 (-19.2%)</td></tr><tr><td>MAE+CutMix3</td><td>78.0 (+24.0%)</td><td>32.0 (+9.3%)</td><td>92.0 (-2.5%)</td><td>67.3 (+2.7%)</td><td>42.0 (-17.2%)</td></tr><tr><td>MAE+H2R</td><td>79.5 (+25.5%)</td><td>29.5 (+4.0%)</td><td>95.5 (+1.0%)</td><td>68.2 (+10.2%)</td><td>64.5 (+5.3%)</td></tr><tr><td>R3M</td><td>59.5</td><td>20.5</td><td>85</td><td>55</td><td>15</td></tr><tr><td>R3M+CutMix1</td><td>69.5 (+10.0%)</td><td>30.0 (+9.5%)</td><td>91.0 (+6.0%)</td><td>63.5 (+8.5%)</td><td>19.0 (+4.0%)</td></tr><tr><td>R3M+CutMix2</td><td>66.0 (+6.5%)</td><td>26.0 (+5.5%)</td><td>83.0 (-2.0%)</td><td>58.3 (+3.3%)</td><td>17.0 (+2.0%)</td></tr><tr><td>R3M+CutMix3</td><td>68.0 (+8.5%)</td><td>26.0 (+5.5%)</td><td>84.0 (-1.0%)</td><td>59.3 (+4.3%)</td><td>14.0 (-1.0%)</td></tr><tr><td>R3M+H2R</td><td>61.5 (+2.0%)</td><td>37.5 (+17.0%)</td><td>85.0 (0.0%)</td><td>61.3 (+6.3%)</td><td>22.0 (+7.0%)</td></tr></table>

with the average success rate on all tasks ranging from 0.9% to 10.2%. Especially for the more challenging MoveCan task, it can improve the success rate by 25.5%. Additionally, while encoders trained on the relatively simple CutMix data show improvement on tasks in Robomimic, their performance in the PushT task remains slightly worse than the encoders trained on original data. These results demonstrate the effectiveness of using the robotic arm to cover the human hand in video data, as well as the effectiveness of H2R in imitation learning.

![[99_Attachments/papers/images/h2r/c2c392909979e6b29875c2e9aa27da379a290aab6822b4771448d9fae67f1470.jpg]]  
Fig. 6: Failure case visualizations: Stack and Stand Cup. We visualize real-world manipulation executions for two downstream tasks: Stack (top) and Stand Cup (bottom). These images provide qualitative insights into the performance and failure modes of the policy in real deployment, highlighting challenges such as object misalignment, perception noise, and grasp precision.

TABLE XIV: Task-specific sub-goal evaluation. To gain fine-grained insights into policy performance, we design a manual rubric covering key sub-goals for each manipulation task. Each cell reports the number of successful vs. unsuccessful attempts (Y/N) over 20 evaluation trials. Results show that models enhanced with H2R consistently accomplish more sub-goals across tasks compared to their baseline counterparts, demonstrating improved robustness in real-world execution. Bold numbers indicate better performance between paired models.

<table><tr><td>Task</td><td>Sub-goal</td><td>MAE(Y/N)</td><td>MAE+H2R(Y/N)</td><td>R3M(Y/N)</td><td>R3M+H2R(Y/N)</td></tr><tr><td rowspan="2">Gripper-PickCube</td><td>Overall success?</td><td>9/11</td><td>13/7</td><td>8/12</td><td>10/10</td></tr><tr><td>Pick up the cube?</td><td>14/6</td><td>15/5</td><td>11/9</td><td>13/7</td></tr><tr><td rowspan="2">Gripper-Stack</td><td>Overall success?</td><td>10/10</td><td>11/9</td><td>11/9</td><td>14/6</td></tr><tr><td>Pick up the cube?</td><td>13/7</td><td>16/4</td><td>13/7</td><td>17/3</td></tr><tr><td rowspan="3">Gripper-CloseBox</td><td>Overall success?</td><td>11/9</td><td>10/10</td><td>9/11</td><td>13/7</td></tr><tr><td>Place the cube in the bow?</td><td>12/8</td><td>14/6</td><td>12/8</td><td>15/5</td></tr><tr><td>Pick up the cube?</td><td>14/6</td><td>14/6</td><td>12/8</td><td>15/5</td></tr><tr><td rowspan="2">Leaphand-GraspChicken</td><td>Overall success?</td><td>8/12</td><td>11/9</td><td>2/18</td><td>7/13</td></tr><tr><td>Pick up the chicken?</td><td>13/7</td><td>14/6</td><td>3/17</td><td>10/10</td></tr><tr><td rowspan="2">Leaphand-StandCup</td><td>Overall success?</td><td>7/13</td><td>12/8</td><td>4/16</td><td>10/10</td></tr><tr><td>Pick up the cup?</td><td>12/8</td><td>18/2</td><td>12/8</td><td>15/5</td></tr><tr><td rowspan="2">Leaphand-OpenBox</td><td>Overall success?</td><td>9/11</td><td>13/7</td><td>8/12</td><td>9/11</td></tr><tr><td>Identify contact location?</td><td>14/6</td><td>16/4</td><td>10/10</td><td>10/10</td></tr></table>