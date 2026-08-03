---
title: "GS-Playground A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning 2604.25459"
---

# GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning

Yufei Jia1*, Heng Zhang2*, Ziheng Zhang3*, Junzhe ${ \mathbf{W}} { \mathbf{u}} ^{1 ^{ *}}$ , Mingrui $\mathrm{ Y u} ^{1 ^{ *}}$

Zifan Wang5, Dixuan Jiang6, Zheng $\mathrm{ L i} ^{5}$ , Chenyu $\mathrm{ C a o} ^{7}$ , Zhuoyuan ${ \mathrm{ Y u}} ^{3}$ , Xun Yang5, Haizhou $\mathrm{ G e ^{1}}$

Yuchi Zhang4, Jiayuan Zhang4, Zhenbiao Huang7, Tianle ${ \mathrm{ L i u}} ^{3}$ , Shenyu Chen8, Jiacheng Wang3, Bin $\mathrm{ X i e} ^{3}$

Xuran Yao4, Xiwa Deng2, Guangyu Wang1, Jinzhi Zhang1, Lei $\mathrm{ H a o} ^{9}$ , Zhixing Chen1, Yuxiang Chen10,

Anqi Wang4, Hongyun Tian3, Yiyi Yan4, Zhanxiang $\mathrm{ C a o ^{1 1}}$ , Yizhou Jiang1, Hanyang Shao4, Yue $\mathrm{ L i ^{4}}$ , Lu $\mathrm{ S h i ^{1}}$ , Bokui Chen1, Wei Sui12, Hanqing $\mathrm{ C u i} ^{2}$ , Yusen $\mathrm{ Q i n} ^{1 2}$ , Ruqi Huang1, Lei $\mathrm{ H a n} ^{4 \dagger}$ , Tiancai $\mathrm{ W a n g ^{3 \dagger}}$ , Guyue Zhou1†

1THU, 2Motphys, 3Dexmal, 4DISCOVER Robotics, 5HKUST(GZ), 6BIT,

7NUS, 8HITSZ, 9XJTU, $^{1 0} \mathrm{ N J U}$ , 11SJTU, $^{1 2} \mathrm{ D}$ -Robotics

*Equal contribution. †Advising. Correspondence to: Yufei Jia <jyf23@mails.tsinghua.edu.cn>.

Fig. 1: GS-Playground Overview. It integrates photorealistic 3D Gaussian Splatting with high-performance parallel physics, achieving over $1 0 ^{4}$ FPS at $6 4 0 \times 4 8 0$ resolution on a single GPU. We provide comprehensive sensor suites (Contact, Vision, LiDAR) and support a wide range of robotic embodiments and learning tasks, including locomotion, navigation, and manipulation.

Abstract—Embodied AI research is undergoing a shift toward vision-centric perceptual paradigms. While massively parallel simulators have catalyzed breakthroughs in proprioception-based locomotion, their potential remains largely untapped for visioninformed tasks due to the prohibitive computational overhead of large-scale photorealistic rendering. Furthermore, the creation of simulation-ready 3D assets heavily relies on labor-intensive manual modeling, while the significant sim-to-real physical gap hinders the transfer of contact-rich manipulation policies. To address these bottlenecks, we propose GS-Playground, a multimodal simulation framework designed to accelerate end-to-end perceptual learning. We develop a novel high-performance parallel physics engine, specifically designed to integrate with a batch 3D Gaussian Splatting (3DGS) rendering pipeline to ensure highfidelity synchronization. Our system achieves a breakthrough

throughput of $\mathbf{1 0 ^{4}}$ FPS at $\mathbf{6 4 0 \times 4 8 0}$ resolution, significantly lowering the barrier for large-scale visual RL. Additionally, we introduce an automated Real2Sim workflow that reconstructs photorealistic, physically consistent, and memory-efficient environments, streamlining the generation of complex simulationready scenes. Extensive experiments on locomotion, navigation, and manipulation demonstrate that GS-Playground effectively bridges the perceptual and physical gaps across diverse embodied tasks. Project homepage: https://gsplayground.github.io.

# I. INTRODUCTION

Vision serves as the most information-rich modality for robotic perception of the environment. Recently, significant progress has been made in learning policies for quasi-static

TABLE I: Comparison of physical and perceptual capabilities across parallel robotics simulators.   

<table><tr><td>Simulators</td><td>Physics Engine</td><td>Batch Physics</td><td>VRAM Usage</td><td>Integrated Batch IK</td><td>Batch Renderer</td><td>Batch Render Fidelity</td><td>3DGS Env. Num.</td><td>Dynamic 3DGS Scene</td><td>3DGS Render FPS</td><td>Startup Speed</td><td>Physics Cross Platform</td></tr><tr><td>MuJoCo/MJX [46]</td><td>Brax/MIX</td><td>CPU/GPU</td><td>★</td><td>×</td><td>Madrona</td><td>+</td><td>-</td><td>-</td><td>-</td><td>+</td><td>L</td></tr><tr><td>IsaacLab [39]</td><td>PhysX5</td><td>GPU</td><td>★★★★★</td><td>✓</td><td>omni.RTX</td><td>++</td><td>-</td><td>-</td><td>-</td><td>++</td><td>L</td></tr><tr><td>ManiSkill [45]</td><td>PhysX5</td><td>GPU</td><td>★★★</td><td>✓</td><td>Vulkan SBR</td><td>+</td><td>-</td><td>-</td><td>-</td><td>+++</td><td>W/L</td></tr><tr><td>Genesis [61]</td><td>Taichi</td><td>GPU</td><td>★</td><td>✓</td><td>Madrona</td><td>+</td><td>-</td><td>-</td><td>-</td><td>++</td><td>W/L/M</td></tr><tr><td>DISCOVERSE [19]</td><td>MuJoCo</td><td>-</td><td>-</td><td>×</td><td>-</td><td>+++</td><td>1 ~ 4</td><td>✓</td><td>~ 650</td><td>++</td><td>L</td></tr><tr><td>GSWorld [20]</td><td>PhysX5</td><td>-</td><td>-</td><td>×</td><td>-</td><td>+++</td><td>1</td><td>✓</td><td>-</td><td>++</td><td>L</td></tr><tr><td>GaussGym [11]</td><td>PhysX4</td><td>GPU</td><td>★</td><td>×</td><td>GSplat</td><td>+++</td><td>Up To 4096</td><td>×</td><td>-</td><td>++</td><td>L</td></tr><tr><td>GS-Playground</td><td>Self-Dev.</td><td>CPU/GPU</td><td>-</td><td>✓</td><td>BatchSplat</td><td>+++</td><td>Up To 4096</td><td>✓</td><td>~ 10k</td><td>++++</td><td>W/L/M</td></tr></table>

Note: 1. Batch Physics: Indicates supported hardware for batched simulation. 2. VRAM Usage: The number of $\cdot _{\star} \cdot$ indicates higher VRAM consumption. In headless mode, only physics simulation overhead is considered. 3. Batch Render Fidelity: The number of $\cdot _{+} \cdot$ represents higher visual fidelity. 4. 3DGS Render FPS: Tested on $6 4 0 \times 4 8 0$ resolution with an NVIDIA RTX 4090 GPU and an Intel i9-14900K CPU. 5. Startup Speed: More $\cdot _{+} \cdot$ means faster startup times. 6. Physics Cross Platform: W: Windows, L: Linux, M: macOS.

manipulation and navigation directly from real-world visual data [25, 62, 4, 56, 28, 51, 17]. However, tasks involving complex dynamics and contacts—such as locomotion and contactrich manipulation—require large-scale parallel simulation for effective reinforcement learning (RL). While current massively parallel simulators have revolutionized proprioception-based learning [34, 39, 55, 45, 61], they often struggle to reconcile visual fidelity with rendering efficiency, limiting the application of large-scale, vision-informed policy learning. We attribute this gap to two primary limitations:

• Prohibitive Rendering Overhead: Existing simulation pipelines face severe scalability bottlenecks when integrating high-resolution rendering. The exorbitant computational cost of photorealistic rendering creates intense resource contention with policy learning, frequently resulting in Out-of-Memory (OOM) failures. Consequently, these hardware constraints force a compromise between visual fidelity and simulation throughput, restricting the scale and efficacy of vision-based training.   
• Laborious Asset Synthesis: Constructing simulation assets that achieve both visual and physical high-fidelity remains a persistent challenge. While 3D reconstruction has advanced significantly, seamlessly converting these representations into “sim-ready” assets—those compatible with both high-frequency physics and memoryefficient rendering—remains difficult and laborious. This highlights the critical need for a pipeline capable of rapidly transforming individual real-world scenes into high-fidelity and consistent digital twins.

To bridge the gap, we introduce GS-Playground, a universal simulation framework harmonizing high-throughput physics simulation and high-fidelity visual rendering (Figure 1). Our platform maintains the precision and stability required for physics simulation while providing the rendering efficiency necessary for large-scale, vision-informed policy training and sim-to-real transfer. Our core contributions are as follows:

1) General-Purpose Embodied Simulation Platform: We develop a ground-up, cross-platform (Windows, Linux, and macOS) parallel physics engine that supports both GPU and CPU backends. This architecture provides high-fidelity physical dynamics and comprehensive sensor integration (including RGB cameras, LiDAR, and

force/contact sensors) across diverse robot embodiments (such as quadrupeds, humanoids, and manipulators). This platform facilitates a flexible development workflow from local prototyping to massively parallel training.

2) Memory-Efficient Batch 3DGS Rendering: To mitigate the memory bottlenecks in large-scale photorealistic simulation, we introduce a specialized point-pruning strategy optimized for rigid-body environments. This approach enables a memory-efficient rendering architecture capable of a breakthrough throughput of $\mathbf{1 0 ^{4}}$ FPS at $\mathbf{6 4 0 \times 4 8 0}$ resolution on a single GPU, significantly expanding the scale of vision-based reinforcement learning.   
3) Automated “Sim-Ready” Real2Sim Workflow: We present a targeted pipeline that streamlines the conversion of individual real-world scenes into functional digital twins, ensuring both visual realism and physical consistency. Our workflow significantly reduces the laborious manual effort usually required to create complex ”simready” assets, enabling the rapid population of diverse simulation environments.

We validate GS-Playground through a rigorous experimental regime. First, we demonstrate that our physics engine matches state-of-the-art simulators in accuracy and efficiency, with enhanced stability in specific contact-rich scenarios. Next, we confirm our rendering pipeline’s ability to provide high-fidelity feedback at unprecedented speeds. Finally, we benchmark the framework on a diverse suite of tasks—including quadrupedal locomotion, humanoid control, and robotic manipulation—across both state-based and visiondriven reinforcement learning. We summarize the key features of GS-Playground alongside other state-of-the-art simulators in Table I. We will release the framework and synthesized Bridge-GS dataset to empower the research community.

# II. RELATED WORK

# A. Massive Parallelism in Simulation

Massive parallel physical simulation has emerged as the indispensable infrastructure for efficient robot learning, particularly for locomotion and contact-rich manipulation [18, 27, 43, 35, 10, 64, 36, 49, 16, 50, 60, 6]. Milestone platforms such as Isaac Gym [34], Isaac Lab [39], and Genesis [61] have revolutionized the throughput of sample collection

by instantiating tens of thousands of parallel environments on GPUs. However, existing frameworks typically prioritize physical throughput over perceptual fidelity. Rendering architectures often diverge into two extremes: they either favor high sampling rates via streamlined rasterization (e.g., Madrona [42], ManiSkill3 [45]) or prioritize cinematic photorealism via computationally expensive ray-tracing (e.g., Isaac Lab [39]). The simultaneous achievement of massive parallel throughput with high-fidelity, photorealistic rendering remains a critical bottleneck for scaling vision-centric robot learning.

# B. Vision-Centric Robot Learning

Vision serves as the most information-rich modality for robotic perception. Recently, significant progress has been made in learning policies for quasi-static manipulation and navigation directly from real-world visual data, exemplified by Vision-Language-Action (VLA) models [25, 62, 4] and Vision-Language-Navigation (VLN) models [9, 5, 57, 58]. However, tasks involving complex dynamics and intermittent contacts rely heavily on simulation-based reinforcement learning (RL) to acquire skills in an unsupervised manner.

Early attempts to incorporate visual inputs into RL were often constrained by conventional, small-scale simulations [2, 37, 63], where low simulation throughput hindered the stable acquisition of complex skills. While recent advancements in massive parallel simulation have enabled sophisticated policy optimization for locomotion and dexterous manipulation, these frameworks primarily rely on proprioceptive states or point clouds due to the prohibitive computational overhead and limited fidelity of visual rendering [7, 30, 23, 53]. Furthermore, to mitigate the sim-to-real gap, recent attempts on vision-based RL methods often necessitate extensive visual randomization of textures, lighting, and backgrounds [17, 51]. This, however, imposes a substantial burden on GPU resources, significantly raising the computational threshold for research in visioninformed robot learning.

# C. Gaussian Splatting and Real-to-Sim Reconstruction

Building simulators highly consistent with the real world relies on high-quality visual rendering and precise physical modeling. Recently, Gaussian Splatting (3DGS) [24] has rapidly developed as an emerging scene reconstruction method, enabling photorealistic real-time rendering from arbitrary viewpoints. Its unique representation strikes a balance between visual fidelity and memory efficiency, making it particularly suitable for resource-constrained simulation environments. Recent research has significantly improved the capability to reconstruct renderable models from real scenes in terms of reconstruction paradigms [48, 38, 22], model efficiency [15, 12, 14], and generative Gaussian models [8, 31].

However, these methods generally struggle to directly meet the requirements of robotic simulators for sim-ready scenes. Existing works indicate that 3DGS-based rendering holds significant potential in robotics, enhancing sim-to-real transfer for vision-based policies [29, 13, 40], augmenting training datasets [3, 33, 54, 52], and supporting real-to-sim evaluation

pipelines [21, 1, 20, 59]. While GaussGym [11] pioneered the application of 3DGS in RL, our work extends this capability to contact-rich manipulation and larger-scale parallel throughput, providing a more versatile foundation for diverse visioninformed robot learning tasks.

# III. SYSTEM DESIGN

# A. System Overview

Figure 2 illustrates the architecture of GS-Playground, which comprises three core tiers: (1) a high-performance parallel physics engine supporting both GPU and CPU backends; (2) a memory-efficient batch 3DGS renderer optimized via point-pruning; and (3) an automated Real2Sim pipeline for rapid scene synthesis. These modules are seamlessly integrated with a multi-modal sensor suite to provide the high-throughput, photorealistic feedback necessary for visioncentric robot learning.

Data Flow. The simulation loop begins with the physics engine, which advances the world state using a velocity-impulse formulation. The updated rigid-body poses are synchronized with the Batch 3DGS Renderer through Rigid-Link Gaussian Kinematics (RLGK), enabling zero-overhead updates of visual clusters. The renderer produces photorealistic RGB images and depth maps, while the sensor suite provides LiDAR point clouds and high-dimensional contact data (including multi-point forces and torques). These modalities form the observation vector for end-to-end policy learning.

Asset Creation. Orthogonal to the loop, the Real2Sim Pipeline streamlines the conversion of individual real-world captures into simulation-ready assets. By performing automated segmentation, reconstruction, and sub-millimeter pose alignment, this pipeline populates the environment with physically consistent rigid-body twins.

Development Workflow. A key design principle is the flexibility of the development-to-training workflow. Our core physics engine is cross-platform (Windows, Linux, macOS), facilitating rapid local debugging and prototyping on various workstations. For large-scale training, the system leverages an optimized CUDA-based rendering pipeline on Linux, achieving a breakthrough throughput of $1 0 ^{4}$ FPS by utilizing specialized point-pruning to balance visual fidelity and memory consumption.

# B. Physics Solver Formulation

In robotic manipulation, the choice of constraint formulation directly impacts simulation fidelity. Optimization-centric solvers that rely on regularized soft contacts tend to produce visually smooth but physically ’spongy’ interactions, where heavy payloads may exhibit gradual drift due to residual forces. GS-Playground utilizes a velocity-impulse formulation in generalized coordinates and implements strict complementarity with explicit velocity clamping at the friction limits. This approach sacrifices the smoothness of the gradients in exchange for geometric precision, allowing for the simulation of rigid bodies that can maintain perfect static equilibrium and allows for high constraint stiffness and large simulation

"Real Image to Sim Physics" Asset Pipeline

Physics and Rendering Simulation Core

Applications   
Fig. 2: GS-Playground System Architecture. Left: an automated Image-to-Physics pipeline that constructs simulation-ready assets from RGB inputs via object segmentation, background inpainting, and 3DGS/mesh reconstruction. Middle: a physics and rendering simulation core with CPU/GPU physics backends, integrated sensor and LiDAR simulation, and batch-optimized 3DGS rendering with pruning and rigid-link kinematics. Right: downstream applications including manipulation, navigation, and large-scale parallel reinforcement learning.

time steps. This makes the engine particularly suitable for engineering applications where stability and exact constraint satisfaction are paramount.

The discretized dynamics equation for generalized coordinates $\mathbf{q} \in \mathbb{R} ^{n}$ and velocities $\mathbf{v} \in \mathbb{R} ^{n}$ over a time step $h$ is formulated as:

$$
\mathbf{M} (\mathbf{v} ^{+} - \mathbf{v}) = \mathbf{J} _{e} ^{T} \boldsymbol{\lambda} _{e} ^{+} + \mathbf{J} _{n} ^{T} \boldsymbol{\lambda} _{n} ^{+} + h (\boldsymbol{\tau} _{e x t} - \mathbf{c}) \tag{1}
$$

where M is the mass matrix, ${ \bf J } _{e}$ and ${ \bf J } _{n}$ are the Jacobians for equality and inequality constraints, respectively, and $\boldsymbol { \lambda }$ denotes the constraint impulses. The term c accounts for Coriolis and centrifugal forces. We incorporate soft constraints by defining an implicit impulse relation $\lambda ^{+} = f ( { \mathbf{u} } ^{+} ; { \mathbf{x} } , h )$ and linearizing it via a first-order Taylor expansion at the current velocity u:

$$
\boldsymbol{\lambda} ^{+} \approx f (\mathbf{u}) + \frac{\partial f}{\partial \mathbf{u}} \left(\mathbf{u} ^{+} - \mathbf{u}\right) \tag{2}
$$

By defining the positive definite compliance matrix ${ \textbf { C } } =$ $( - \frac { \partial f } { \partial \mathbf{u} } ) ^{- 1}$ and the bias term ${ \boldsymbol { \zeta } } = \mathbf{u} + \mathbf{C} f ( \mathbf{u} )$ , we obtain the standardized compliance form:

$$
\mathbf{u} ^{+} = - \mathbf{C} \boldsymbol{\lambda} ^{+} + \zeta \tag{3}
$$

By substituting this velocity relation into the constraint space and eliminating the equality constraints $\lambda _{e}$ via the Schur complement method, we obtain a reduced linear system for the inequality constraints $\lambda _{n}$ :

$$
\mathbf{u} _{n} ^{+} = \mathbf{A} \boldsymbol{\lambda} _{n} ^{+} + \mathbf{b} \tag{4}
$$

The system matrix A and the right-hand side vector $\mathbf{b}$ are explicitly given by:

$$
\mathbf{A} = \mathbf{J} _{n} \mathbf{M} ^{- 1} \mathbf{J} _{n} ^{T} - \mathbf{J} _{n} \mathbf{M} ^{- 1} \mathbf{J} _{e} ^{T} \left(\mathbf{W} _{e e} + \mathbf{C} _{e}\right) ^{- 1} \mathbf{J} _{e} \mathbf{M} ^{- 1} \mathbf{J} _{n} ^{T} \tag{5}
$$

$$
\mathbf{b} = \mathbf{J} _{n} \tilde{\mathbf{v}} + \mathbf{J} _{n} \mathbf{M} ^{- 1} \mathbf{J} _{e} ^{T} \left(\mathbf{W} _{e e} + \mathbf{C} _{e}\right) ^{- 1} \left(\boldsymbol{\zeta} _{e} - \mathbf{J} _{e} \tilde{\mathbf{v}}\right) \tag{6}
$$

where $\mathbf{W} _{e e} = \mathbf{J} _{e} \mathbf{M} ^{- 1} \mathbf{J} _{e} ^{T}$ is the effective inverse mass matrix of the equality constraints. The term $\left( \mathbf{W} _{e e} + \mathbf{C} _{e} \right)$ is guaranteed to be invertible as it is the sum of a positive semi-definite matrix and a positive definite matrix.

The solver resolves contact and friction as a Mixed Complementarity Problem (MCP). The impulse vector $\lambda _{n}$ comprises normal components $\lambda _{\perp}$ and frictional components $\lambda _{\parallel}$ . The solution must satisfy the bounds defined by the Coulomb friction model:

$$
\left\{ \begin{array}{l l} w _{i} \geq 0, & \text{if} \lambda_{i} ^{+} = l _{i} \\ w _{i} = 0, & \text{if} l _{i} <   \lambda_{i} ^{+} <   u _{i} \\ w _{i} \leq 0, & \text{if} \lambda_{i} ^{+} = u _{i} \end{array} \right. \tag{7}
$$

where $w _{i} = [ ( { \bf A } + { \bf C } _{n} ) \lambda _{n} ^{+} + ( { \bf b } - \zeta _{n} ) ] _{i}$ . For normal contact, the bounds are $[ 0 , \infty )$ ; for friction, the bounds are $[ - \mu \lambda _{\perp} ^{+} , \mu \lambda _{\perp} ^{+} ]$ . This formulation is solved efficiently using a Projected Gauss-Seidel (PGS) solver, ensuring stable friction behavior while accommodating both rigid and compliant contact interactions.

This framework demonstrates high extensibility. It supports various physical constraints, including MJCF-defined contact models (e.g., parameters solref, solimp), tendons, and actuators. Integrating a new constraint type simply requires defining its impulse-state relationship $\lambda ( \mathbf{x} , \mathbf{u} )$ and the corresponding Jacobian J. Additionally, to achieve real-time performance in large-scale scenarios with massive contacts, we implemented two key engineering optimizations:

1) Parallelization via Constraint Islands: Leveraging the spatial locality of physical interactions, we dynamically construct a constraint dependency graph at each time step. By analyzing the connectivity of the graph, the rigid body system is partitioned into disjoint sets of interacting bodies, termed “Constraint Islands.” Since the Linear Complementarity Problems (LCPs) for these islands are mathematically independent, they are dispatched to multi-core CPU threads for parallel solving, ensuring linear performance scaling with scene complexity.   
2) Warm-Starting with Temporal Coherence: We exploit the temporal coherence of physical processes by implementing a Contact Manifold Tracking system. This system persists contact constraints across simulation frames. Instead of initializing the Projected Gauss-Seidel (PGS) solver with zero vectors, we warm-start the solver using the converged impulses $\lambda _{t - 1}$ from

the previous frame as the initial guess $\lambda _{\mathrm { i n i t i a l} }$ . This strategy significantly accelerates convergence, typically reducing the required PGS iterations from over 50 to fewer than 10 for stable stacking tasks.

# C. Batch Renderer Optimization

Rendering thousands of high-fidelity 3DGS scenes simultaneously presents a significant memory challenge. To optimize memory usage while maintaining visual fidelity, we propose several key advancements as follows:

Efficient Pruning Strategy. We adopt a state-of-the-art efficient pruning strategy inspired by recent works [15, 12, 14], reducing the number of Gaussians by over $90 \%$ while maintaining a minimal Peak Signal-to-Noise Ratio (PSNR) drop of less than 0.05, virtually imperceptible to visuomotor policies. This reduction significantly lowers VRAM usage, while keeping the visual quality nearly unchanged. As a result, the strategy boosts the overall rendering speed and ensures model efficiency, making it well-suited for large-scale, highfidelity simulations.

Throughput Scaling. Our Batch-3DGS renderer is optimized for batch processing, enabling the simultaneous large-scale Gaussian rendering of multiple scenes. Built upon the efficient Gaussian rendering engine, we can render up to 2048 scenes at a resolution of $6 4 0 \times 4 8 0$ with a total throughput of up to 10,000 FPS. This scaling significantly improves throughput per unit compute, supporting large-batch training workflows.

Rigid-Link Gaussian Kinematics (RLGK). To ensure temporal consistency and eliminate visual artifacts in dynamic scenarios, we introduce Rigid-Link Gaussian Kinematics (RLGK), which binds clusters of 3D Gaussians to corresponding rigid bodies in the physics engine. This coupling ensures that visual representations move synchronously with their physical counterparts, enabling “zero-overhead” updates and artifact-free dynamic rendering during fast motion or contact events.

# D. “Image-to-Physics” Asset Pipeline

Users can create a set of simulation-ready assets from a single RGB image via our fully automated pipeline. The pipeline reconstructs 3D representations (3DGS/mesh) and estimates geometric and physical properties, enabling seamless integration with collision modeling and manipulation learning.

Objects Segmentation and Background Inpainting. We present an automated pipeline for object segmentation and background inpainting from a single RGB image. Objects are detected using Grounding DINO [32] and segmented with SAM1/SAM2 [26, 41] under a prompt-wise independent detection scheme, enabling explicit tracking of instance–label associations. To mitigate unreliable semantic similarity in open-vocabulary detection, we de-duplicate instances using visual criteria only: mask IoU for general redundancy and a dual-criterion rule based on mask inclusion and boundary overlap to correct over-segmentation. Instance selection is

TABLE II: Comparison of LiDAR simulation capabilities.   

<table><tr><td>LiDAR Sensor Feature</td><td>Ours</td><td>IsaacSim</td><td>Gazebo</td></tr><tr><td>Rotating LiDAR Support</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>Solid-State LiDAR Support</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>Non-repetitive scan LiDAR</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>Static Irregular Objects</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>Dynamic Irregular Objects</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>Self-Occlusion</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>3DGS Representation</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>Massively Parallel</td><td>✓</td><td>✓</td><td>×</td></tr></table>

prioritized by a composite confidence score combining detection and segmentation confidence. Occluded object regions are recovered through an iterative mask expansion process coupled with sequential inpainting. Objects are removed one at a time, and after each inpainting step, the scene is re-detected to identify newly exposed regions that are spatially adjacent and label-consistent with existing instances under a bounded area growth constraint. Background inpainting is performed sequentially using LaMa [44] to ensure stable reconstruction.

Assets Generation. For object-level assets, we apply SAM-3D [8] to the original RGB image together with the object mask $( M _{o b j} )$ to reconstruct its 3DGS and mesh, and to estimate its pose and scale. For scene-level assets, the inpainted background is processed by AnySplat [22] to generate the background 3DGS, depth map $( D _{b g} )$ , as well as the camera intrinsics and extrinsics. To align object- and scene-level assets, we first transform the object such that its rendered depth map $( D _{o b j} )$ aligns with the background depth $( D _{b g} )$ . The object is then scaled so that the area of its rendered mask matches the original object mask $( M _{o b j} )$ , measured by pixel occupancy. To reduce memory footprint for downstream robotic tasks, we apply Speedy- splat [14] for 3DGS pruning.

# E. User Interface and Ecosystem Design

GS-Playground provides a rich set of features including multi-modal sensing, seamless ecosystem compatibility, and cross-platform support to facilitate robot development.

Multi-modal Sensor Suite Beyond standard RGB and depth streams, we integrate a high-performance Batch-LiDAR module utilizing ray-casting to generate high-fidelity point clouds and heightmap scanning (Table II). Additionally, our platform provides detailed contact information equivalent to MuJoCo, including multi-point contact forces, torques, and decomposed normal/tangential components.

Ecosystem Compatibility and Cross-Platform Workflow. Prioritizing ”zero-friction” migration, our API is compatible with the MuJoCo MJCF format, enabling rapid project migration. The physics engine features a cross-platform architecture (Windows/Linux/macOS), allowing local prototyping and debugging before deploying large-scale parallel training on Linux GPU clusters using Batch-3DGS and CUDA-optimized perception modules.

# IV. RESULTS

We evaluate GS-Playground through a comprehensive benchmark suite spanning visual and geometric fidelity, physics stability, manipulation proficiency, and locomotion

TABLE III: Qualitative comparison of contact dynamics. The Newton’s Cradle case evaluates momentum transfer, while the Boston Dynamics Spot case validates base stability with a $1 0 ~ \mathrm { m s }$ timestep.   

<table><tr><td>Scenario</td><td>MuJoCo</td><td>IsaacSim</td><td>Ours</td></tr><tr><td>Newton&#x27;s Cradle (pre-impact)</td><td></td><td></td><td></td></tr><tr><td>Newton&#x27;s Cradle (post-impact)</td><td></td><td></td><td></td></tr><tr><td>Boston Spot (t=0s)</td><td></td><td></td><td></td></tr><tr><td>Boston Spot (t=2s)</td><td></td><td></td><td></td></tr></table>

capability. Our results demonstrate the platform’s superiority in photorealistic rendering, massive parallel physics stepping, and effective Sim2Real transfer for both vision-based and contact-rich tasks.

# A. Physics Stability and Solver Robustness

Multi-Scenario Benchmarking. We conduct a multiscenario stability study across multiple simulators to stress-test contact handling under challenging dynamics.

1) Hard Contact & Momentum Conservation: Using a Newton’s Cradle setup with identical initial perturbations across engines, we evaluate long-horizon momentum transfer and dissipation under hard contacts (Table III Top). GS-Playground preserves impact timing and swing amplitude with reduced energy bleed across repeated impacts, while MuJoCo exhibits stronger damping and phase drift.   
2) Large Time-step Stability: We evaluate base stability on a Boston Dynamics Spot model under physics-only stepping with a $1 0 \mathrm { m s }$ timestep, no control input, and identical initial pose (Table III Bottom). GS-Playground exhibits smaller base displacement and reduced drift over time, suggesting more stable contact resolution under large time steps.   
3) Complex Multi-Body Interactions: In a dense store shelf scenario with stacked objects, we evaluate static stability under complex multi-contact constraints. While GS-Playground consistently converges to stable equilibria, MuJoCo exhibits characteristic jitter and contact-induced drift—common artifacts in high-density contact graphs (Fig. 3).

Stability and Scalability in Complex Scenes. We evaluate the algorithmic robustness of GS-Playground against Mu-JoCo (CPU) and Genesis/MjWarp (GPU) in high-complexity single-environment scenarios. To vary scene complexity, we scale the number $( N )$ of 27-DoF humanoid agents within a single environment. All experiments were conducted on an AMD 9950x CPU and an NVIDIA RTX 5090 GPU. Results are shown in Fig. 4. As constraint density increases, GPUbased solvers suffers from severe performance degradation. At $N = 1 0$ , Genesis fails to reach convergence and exhibits

![[99_Attachments/papers/images/gs-playground/00b537fd4b0a81cc7e475dcb728e36e015a95a0a0c7712930bdfc75ee7e19f31.jpg]]  
Fig. 3: Physics stability under complex multi-body interactions. (a) The dense store shelf scenario; (b) Stability error across time steps, computed over all objects in the scene with identical initial placements. The error is defined as $\sqrt { \Delta p ^{2} + \Delta \theta ^{2} }$ , where $\Delta p$ is mean positional drift (m) and $\Delta \theta$ is mean orientation drift (rad).

Fig. 4: Performance Comparison on Complexity Scaling. Left: As the complexity (N, the number of humanoid robots) in a single environment increases, the FPS advantage of our framework becomes increasingly pronounced. Right: At a complexity of $N = 1 0$ , our framework maintains FPS advantage with large batch sizes, where Genesis fails to reach convergence.

numerical instability through Jacobian-related errors. When complexity reaches $N = 5 0$ , MjWarp’s throughput collapses to a mere 1.71 FPS. In contrast, GS-Playground (CPU) maintains a robust throughput of 1,015 FPS at $N = 5 0$ . This performance represents a $3 2 \times$ speedup over MuJoCo and a ${ \sim } 6 0 0 \times$ improvement over MjWarp. Note that GS-Playground also offers competitive GPU performance, with further gains expected as we are refining our GPU-specific kernel fusion and memory management strategies.

# B. Visual Fidelity and Efficiency

Visual 3DGS Compression. We measure the trade-off between memory footprint and visual quality, as summarized in Table IV. For full static scene reconstruction, we compare raw 3DGS reconstructions with our pruned version, retaining only about $30 \%$ of the Gaussians while preserving high PSNR and SSIM, along with competitive LPIPS performance. Additionally, for manipulated dynamic objects and the robot body, the number of points can be further reduced by up to $90 \%$ , enabling more aggressive memory compression without compromising the critical visual cues required for robotic perception.

Rendering Throughput Comparison. We evaluate the rendering throughput of GS-Playground against Isaac Sim’s ray-tracing renderer across three standard resolutions and multiple GPU architectures, including the NVIDIA RTX 4090, RTX 6000 Ada, and A100. As illustrated in Fig. 4, our

![[99_Attachments/papers/images/gs-playground/11afcf43e0e616cf9537813c89e5a08e8dc396c8cab13e1cfde784f97ff30088.jpg]]  
Fig. 5: Rendering throughput comparison between GS-Playground and Isaac Sim’s ray-tracing renderer across varying resolutions. While Isaac Sim relies on manual asset modeling and encounters Out-Of-Memory (OOM) exceptions at higher resolutions, GS-Playground leverages automated asset generation from real-world captures, achieving high-fidelity sim-ready assets with superior rendering throughput. Evaluations are conducted on three different GPU architectures: NVIDIA RTX 4090, RTX 6000 Ada Generation, and NVIDIA A100.

TABLE IV: Image Quality Metrics. Our model retains only $30 \%$ o f the original Gaussians with negligible degradation in visual fidelity of static scene reconstruction.   

<table><tr><td>Method</td><td># Gaussians ↓</td><td>PSNR ↑</td><td>SSIM ↑</td><td>LPIPS ↓</td></tr><tr><td>3DGS</td><td>100%</td><td>27.1503</td><td>0.8296</td><td>0.2238</td></tr><tr><td>Ours</td><td>30%</td><td>26.8658</td><td>0.8022</td><td>0.2840</td></tr></table>

Fig. 6: Visualization of rendering. The simulated renderings are nearly indistinguishable from real photographs indicating photorealistic fidelity. Our framework supports a broad range of tasks and evaluations, including diverse objects and scene configurations.

framework consistently outperforms the baseline, maintaining significantly higher FPS across all tested batch sizes. This performance advantage is particularly evident at higher resolutions, such as $1 2 8 0 \times 7 2 0$ , where Isaac Sim’s ray-tracing approach frequently encounters Out-Of-Memory (OOM) exceptions at larger batch sizes. In contrast, our Gaussian Splattingbased pipeline demonstrates superior memory efficiency and scalability, enabling high-throughput rendering of automated, sim-ready assets. These results validate that our framework provides a more robust and efficient solution for large-scale parallel visual simulation.

Qualitative Rendering Fidelity and Diversity. Fig. 6 presents a qualitative comparison between real and simulated renderings. The simulated renders exhibit a high degree of

Fig. 7: Wall-clock training efficiency for Unitree Go1 locomotion. (a) Flat terrain; (b) Rough terrain (stairs). “deci” denotes the decimation, which refers to the number of physical sub-steps per control step. Lower decimation typically increases throughput but may compromise physical fidelity.

visual consistency with real camera images, preserving critical geometric features and surface details. Moreover, the scenes depicted span a diverse set of object types, materials, and configurations, demonstrating that our simulation system maintains a high level of visual consistency across varied setups, making it suitable for diverse training and evaluation scenarios. All experiments were conducted on Bridge-v2 dataset[47], on a device equipped with an NVIDIA RTX 3090 GPU. Without 3DGS pruning, the pipeline processes a single image within 5 minutes end-to-end. Excluding model checkpoint loading time, segmentation and inpainting take about 25 s per scene, AnySplat completes within 8 s, and SAM3D processes each object mask within 10 s, demonstrating a fast and computationally efficient workflow. Compared to the Bridge-v2 dataset, the generated Bridge-GS dataset enriches each asset via our pipeline with scene- and object-level 3DGS representations, object-level meshes, object poses, and camera intrinsics and extrinsics.

# C. Physics-Intensive Locomotion Learning

Simulation Comparison. We benchmark our framework against IsaacLab using the Isaac-Velocity-Flat-Unitree-Go1-v0 and Isaac-Velocity-Rough-Unitree-Go1-v0 environments. All configurations are trained for an equivalent number of total steps. On flat terrain (Fig. 7a), while IsaacLab achieves higher

Fig. 8: Real-world deployment of policies trained in GS-Playground. We demonstrate robust Sim2Real transfer across diverse embodiments and modalities: (a) Quadrupedal Locomotion: Velocity tracking on Unitree Go2; (b) Humanoid Locomotion: 23-DoF balancing and walking on Unitree G1; (c) Visual Manipulation: End-to-end RGB-based grasping; (d) Visual Navigation: Real-time cone following on Unitree Go2 using raw RGB observations.

speed at low fidelity ( $d = 1$ , where $d$ denotes the decimation factor, or the number of physical sub-steps per control step), it fails to reach a competitive terminal reward. In contrast, our method with $d = 1$ achieves a terminal reward comparable to IsaacLab at $d = 4$ , while reaching convergence faster. This result demonstrates that our solver’s stability permits larger integration time steps without compromising physical fidelity or policy convergence. This stability advantage is even more apparent in complex environments like the stairs terrain (Fig. 7b). Here, our framework at $d = 1$ achieves higher rewards and faster convergence than the baseline at the same setting. Against the high-precision baseline $( d \ = \ 4 )$ ), our method remains faster in wall-clock time. These results show that our approach offers a clear dual advantage in stability and speed for complex, contact-rich tasks.

Sim2Real Deployment. We demonstrate the practical utility of GS-Playground by successfully deploying state-based locomotion policies onto a Unitree Go2 quadruped and a Unitree G1 humanoid (Fig. 8(a), (b)). The quadruped policy, utilizing simplified collision geometries and 1,024 parallel environments, reached convergence in 10 minutes of wallclock time. The humanoid policy, employing full-collision manifolds and 2,048 parallel environments, reached convergence in approximately 6 hours. These results demonstrate our framework’s efficiency in bridging the physics reality gap.

# D. Vision-Centric Navigation Learning

We demonstrate a vision-based navigation task on the Unitree Go2, where the robot is required to search for and reach a target traffic cone (Fig. 8(d)). The policy observes egocentric RGB images rendered by GS-Playground during training. To couple high-level visual decision making with stable legged control, we adopt a two-level hierarchical RL design. A highlevel policy encodes egocentric RGB observations and outputs

a compact navigation command (e.g., desired base motion command). A low-level policy takes the command together with proprioceptive states and produces joint-level control signals for the Go2. Both levels are trained with PPO in GS-Playground. After training in simulation, we directly deploy the learned policy on a real Go2, which successfully performs goal-directed navigation toward the cone using only onboard egocentric vision. These results validate that GS-Playground provides the high-fidelity visual feedback necessary for training vision-encoder policies capable of zeroshot real-world deployment.

# E. Vision-Centric Manipulation Learning

To evaluate the platform’s efficacy in bridging the visual Sim2Real gap, we conducted a block-grasping task using the Airbot Play robotic arm (Fig. 8c). The control policy is trained to map raw RGB observations and proprioceptive states directly to 6-DoF joint actions. Utilizing our Real2Sim pipeline, we reconstructed a high-fidelity digital twin that serves as a direct visual proxy for the real-world setup. To ensure the policy’s robustness against real-world variability, we incorporated domain randomization of camera poses and lighting conditions during the training phase. The resulting policy demonstrates remarkable generalization, achieving a $90 \%$ success rate during zero-shot real-world deployment. Notably, the evaluation was performed in a real-world scene that featured no specialized visual engineering or simplification, such as simplified backgrounds or controlled lighting. The robot demonstrates agile and stable grasping maneuvers, proving that the perceptual richness of 3D-Gaussian-based simulation allows agents to learn directly from complex, unsimplified visual cues.

# V. DISCUSSION

We plan to utilize GS-Playground to synthesize massivescale visual-informed data for VLA and VLN models, facilitating robust sim-to-real transfer. Additionally, by incorporating the real-to-sim workflows, we are constructing expansive, scalable environments for the rigorous verification and benchmarking of advanced robotic policies.

Despite its current performance, our framework has several limitations that provide opportunities for future research. Unlike ray tracing or standard rasterization-based renderers, 3D Gaussian Splatting struggles with handling randomized lighting and shadows. Our asset generation is currently dependent on the lighting conditions of the source images. While we achieve high fidelity, algorithmic relighting is needed to fully decouple object appearance from environmental lighting, which would further enhance generalization. Furthermore, the current Rigid-Link Gaussian Kinematics (RLGK) assumes rigid bodies. Representing deformable objects (cloth, fluids) or soft-body manipulation remains a challenge. We plan to integrate particle-based dynamics (like PBD or MPIM) with Gaussian splatting to address non-rigid interactions.

# VI. CONCLUSION

We introduce GS-Playground, a high-performance simulation platform that harmonizes a custom parallel physics engine with a memory-efficient batch 3D Gaussian Splatting (3DGS) renderer to bridge the gap between realism and efficiency. By utilizing a specialized point-pruning strategy, our framework achieves a breakthrough throughput of $1 0 ^{4}$ FPS while avoiding the heavy memory overhead of traditional neural rendering. An automated ”Image-to-Physics” pipeline streamlines the creation of simulation-ready digital twins, ensuring visual and physical consistency for complex tasks. Evaluations across quadrupedal, humanoid, and manipulation embodiments demonstrate that GS-Playground facilitates robust Sim2Real transfer by bridging the reality gap in both physical dynamics and visual perception. Ultimately, our fullstack engine provides a scalable, open-source pathway toward generalizable embodied AI.

# VII. ACKNOWLEDGMENTS

The authors gratefully acknowledge support from D-Robotics under Grant No. 20243000104. We thank the Mu-JoCo and MuJoCo Playground teams for making their codebases available to the community; their software and documentation provided valuable references and infrastructure support for this work.

# REFERENCES

[1] Jad Abou-Chakra, Lingfeng Sun, Krishan Rana, Brandon May, Karl Schmeckpeper, Maria Vittoria Minniti, and Laura Herlant. Real-is-sim: Bridging the sim-to-real gap with a dynamic digital twin for real-world robot policy evaluation. arXiv preprint arXiv:2504.03597, 2025.   
[2] Ilge Akkaya, Marcin Andrychowicz, Maciek Chociej, Mateusz Litwin, Bob McGrew, Arthur Petron, Alex Paino, Matthias Plappert, Glenn Powell, Raphael Ribas, et al. Solving rubik’s cube with a robot hand. arXiv preprint arXiv:1910.07113, 2019.   
[3] Leonardo Barcellona, Andrii Zadaianchuk, Davide Allegro, Samuele Papa, Stefano Ghidoni, and Efstratios Gavves. Dream to manipulate: Compositional world models empowering robot imitation learning with imagination. arXiv preprint arXiv:2412.14957, 2024.   
[4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. $\pi 0$ : A vision-language-action flow model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550. arXiv preprint ARXIV.2410.24164.   
[5] Wenzhe Cai, Jiaqi Peng, Yuqiang Yang, Yujian Zhang, Meng Wei, Hanqing Wang, Yilun Chen, Tai Wang, and Jiangmiao Pang. NavDP: Learning sim-to-real navigation diffusion policy with privileged information guidance. arXiv preprint arXiv:2501.04610, 2025.   
[6] Zhanxiang Cao, Yang Zhang, Buqing Nie, Huangxuan Lin, Haoyang Li, and Yue Gao. Learning motion skills

with adaptive assistive curriculum force in humanoid robots. arXiv preprint arXiv:2506.23125, 2025.   
[7] Tao Chen, Megha Tippur, Siyang Wu, Vikash Kumar, Edward Adelson, and Pulkit Agrawal. Visual dexterity: Inhand reorientation of novel and complex object shapes. Science Robotics, 8(84):eadc9244, 2023.   
[8] Xingyu Chen, Fu-Jen Chu, Pierre Gleize, Kevin J Liang, Alexander Sax, Hao Tang, Weiyao Wang, Michelle Guo, Thibaut Hardin, Xiang Li, et al. Sam 3d: 3dfy anything in images. arXiv preprint arXiv:2511.16624, 2025.   
[9] An-Chieh Cheng, Yandong Ji, Zhaojing Yang, Xueyan Zou, Jan Kautz, Erdem Biyik, Hongxu Yin, Sifei Liu, and Xiaolong Wang. Navila: Legged robot vision-languageaction model for navigation. In RSS, 2025.   
[10] Suyoung Choi, Gwanghyeon Ji, Jeongsoo Park, Hyeongjun Kim, Juhyeok Mun, Jeong Hyun Lee, and Jemin Hwangbo. Learning quadrupedal locomotion on deformable terrain. Science Robotics, 8(74):eade2256, 2023.   
[11] Alejandro Escontrela, Justin Kerr, Arthur Allshire, Jonas Frey, Rocky Duan, Carmelo Sferrazza, and Pieter Abbeel. Gaussgym: An open-source real-to-sim framework for learning locomotion from pixels. arXiv preprint arXiv:2510.15352, 2025.   
[12] Guangchi Fang and Bing Wang. Mini-splatting: Representing scenes with a constrained number of gaussians. In European Conference on Computer Vision, pages 165– 181. Springer, 2024.   
[13] Xiaoshen Han, Minghuan Liu, Yilun Chen, Junqiu Yu, Xiaoyang Lyu, Yang Tian, Bolun Wang, Weinan Zhang, and Jiangmiao Pang. $\mathrm { R e ^{3} }$ sim: Generating high-fidelity simulation data via 3d-photorealistic real-to-sim for robotic manipulation. arXiv preprint arXiv:2502.08645, 2025.   
[14] Alex Hanson, Allen Tu, Geng Lin, Vasu Singla, Matthias Zwicker, and Tom Goldstein. Speedy-splat: Fast 3d gaussian splatting with sparse pixels and sparse primitives. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 21537–21546, 2025.   
[15] Alex Hanson, Allen Tu, Vasu Singla, Mayuka Jayawardhana, Matthias Zwicker, and Tom Goldstein. Pup 3d-gs: Principled uncertainty pruning for 3d gaussian splatting. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 5949–5958, 2025.   
[16] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. arXiv preprint arXiv:2502.01143, 2025.   
[17] Tairan He, Zi Wang, Haoru Xue, Qingwei Ben, Zhengyi Luo, Wenli Xiao, Ye Yuan, Xingye Da, Fernando Castaneda, Shankar Sastry, et al. Viral: Visual sim-to-real ˜ at scale for humanoid loco-manipulation. arXiv preprint arXiv:2511.15200, 2025.   
[18] Jemin Hwangbo, Joonho Lee, Alexey Dosovitskiy, Dario

Bellicoso, Vassilios Tsounis, Vladlen Koltun, and Marco Hutter. Learning agile and dynamic motor skills for legged robots. Science Robotics, 4(26):eaau5872, 2019.   
[19] Yufei Jia, Guangyu Wang, Yuhang Dong, Junzhe Wu, Yupei Zeng, Haonan Lin, Zifan Wang, Haizhou Ge, Weibin Gu, Kairui Ding, et al. Discoverse: Efficient robot simulation in complex high-fidelity environments. arXiv preprint arXiv:2507.21981, 2025.   
[20] Guangqi Jiang, Haoran Chang, Ri-Zhao Qiu, Yutong Liang, Mazeyu Ji, Jiyue Zhu, Zhao Dong, Xueyan Zou, and Xiaolong Wang. Gsworld: Closed-loop photorealistic simulation suite for robotic manipulation. arXiv preprint arXiv:2510.20813, 2025.   
[21] Hanxiao Jiang, Hao-Yu Hsu, Kaifeng Zhang, Hsin-Ni Yu, Shenlong Wang, and Yunzhu Li. Phystwin: Physicsinformed reconstruction and simulation of deformable objects from videos. arXiv preprint arXiv:2503.17973, 2025.   
[22] Lihan Jiang, Yucheng Mao, Linning Xu, Tao Lu, Kerui Ren, Yichen Jin, Xudong Xu, Mulin Yu, Jiangmiao Pang, Feng Zhao, et al. Anysplat: Feed-forward 3d gaussian splatting from unconstrained views. ACM Transactions on Graphics (TOG), 44(6):1–16, 2025.   
[23] Yongpeng Jiang, Mingrui Yu, Chen Chen, Yongyi Jia, and Xiang Li. Robust in-hand reorientation with hierarchical rl-based motion primitives and model-based regrasping. IEEE Robotics and Automation Practice, 1: 12–17, 2025.   
[24] Bernhard Kerbl, Georgios Kopanas, Thomas Leimkuhler, ¨ and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. ACM Trans. Graph., 42(4):139– 1, 2023.   
[25] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246, 2024.   
[26] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Dollar, and Ross Girshick. Segment anything. ´ arXiv:2304.02643, 2023.   
[27] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra Malik. Rma: Rapid motor adaptation for legged robots. arXiv preprint arXiv:2107.04034, 2021.   
[28] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, et al. Simplevla-rl: Scaling vla training via reinforcement learning. arXiv preprint arXiv:2509.09674, 2025.   
[29] Xinhai Li, Jialin Li, Ziheng Zhang, Rui Zhang, Fan Jia, Tiancai Wang, Haoqiang Fan, Kuo-Kun Tseng, and Ruiping Wang. Robogsim: A real2sim2real robotic gaussian splatting simulator. arXiv preprint arXiv:2411.11839, 2024.   
[30] Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu,

Wei Liang, Yixin Zhu, and Siyuan Huang. CLONE: Closed-loop whole-body humanoid teleoperation for long-horizon tasks. In 9th Annual Conference on Robot Learning (CoRL), 2025.   
[31] Chenguo Lin, Panwang Pan, Bangbang Yang, Zeming Li, and Yadong Mu. Diffsplat: Repurposing image diffusion models for scalable gaussian splat generation. arXiv preprint arXiv:2501.16764, 2025.   
[32] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. arXiv preprint arXiv:2303.05499, 2023.   
[33] Haozhe Lou, Yurong Liu, Yike Pan, Yiran Geng, Jianteng Chen, Wenlong Ma, Chenglong Li, Lin Wang, Hengzhen Feng, Lu Shi, et al. Robo-gs: A physics consistent spatial-temporal model for robotic arm with hybrid representation. In 2025 IEEE International Conference on Robotics and Automation (ICRA), pages 15379–15386. IEEE, 2025.   
[34] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. arXiv preprint arXiv:2108.10470, 2021.   
[35] Gabriel B Margolis and Pulkit Agrawal. Walk these ways: Tuning robot control for generalization with multiplicity of behavior. In Conference on Robot Learning, pages 22–31. PMLR, 2023.   
[36] Gabriel B Margolis, Ge Yang, Kartik Paigwar, Tao Chen, and Pulkit Agrawal. Rapid locomotion via reinforcement learning. The International Journal of Robotics Research, 43(4):572–587, 2024.   
[37] Jan Matas, Stephen James, and Andrew J. Davison. Sim-to-real reinforcement learning for deformable object manipulation. In Conference on Robot Learning (CoRL), pages 734–743. PMLR, 2018.   
[38] Lars Mescheder, Wei Dong, Shiwei Li, Xuyang Bai, Marcel Santos, Peiyun Hu, Bruno Lecouat, Mingmin Zhen, AmaAG¸ l Delaunoy, Tian Fang, et al. Sharp ˜ monocular view synthesis in less than a second. arXiv preprint arXiv:2512.10685, 2025.   
[39] Mayank Mittal, Pascal Roth, James Tigue, Antoine Richard, Octi Zhang, Peter Du, Antonio Serrano-Munoz, ˜ Xinjie Yao, Rene Zurbr ´ ugg, Nikita Rudin, et al. Isaac ¨ lab: A gpu-accelerated simulation framework for multimodal robot learning. arXiv preprint arXiv:2511.04831, 2025.   
[40] M Nomaan Qureshi, Sparsh Garg, Francisco Yandun, David Held, George Kantor, and Abhisesh Silwal. Splatsim: Zero-shot sim2real transfer of rgb manipulation policies using gaussian splatting. In 2025 IEEE International Conference on Robotics and Automation (ICRA), pages 6502–6509. IEEE, 2025.   
[41] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Rong-

hang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Radle, Chloe Rolland, Laura Gustafson, Eric ¨ Mintun, Junting Pan, Kalyan Vasudev Alwala, Nicolas Carion, Chao-Yuan Wu, Ross Girshick, Piotr Dollar, and ´ Christoph Feichtenhofer. Sam 2: Segment anything in images and videos. arXiv preprint arXiv:2408.00714, 2024. URL https://arxiv.org/abs/2408.00714.   
[42] Brennan Shacklett, Luc Guy Rosenzweig, Zhiqiang Xie, Bidipta Sarkar, Andrew Szot, Erik Wijmans, Vladlen Koltun, Dhruv Batra, and Kayvon Fatahalian. An extensible, data-oriented architecture for high-performance, many-world simulation. ACM Transactions on Graphics (TOG), 42(4):1–13, 2023.   
[43] Jonah Siekmann, Kevin Green, John Warila, Alan Fern, and Jonathan Hurst. Blind bipedal stair traversal via sim-to-real reinforcement learning. arXiv preprint arXiv:2105.08328, 2021.   
[44] Roman Suvorov, Elizaveta Logacheva, Anton Mashikhin, Anastasia Remizova, Arsenii Ashukha, Aleksei Silvestrov, Naejin Kong, Harshith Goka, Kiwoong Park, and Victor Lempitsky. Resolution-robust large mask inpainting with fourier convolutions. arXiv preprint arXiv:2109.07161, 2021.   
[45] Stone Tao, Fanbo Xiang, Arth Shukla, Yuzhe Qin, Xander Hinrichsen, Xiaodi Yuan, Chen Bao, Xinsong Lin, Yulin Liu, Tse kai Chan, Yuan Gao, Xuanlin Li, Tongzhou Mu, Nan Xiao, Arnav Gurha, Viswesh Nagaswamy Rajesh, Yong Woo Choi, Yen-Ru Chen, Zhiao Huang, Roberto Calandra, Rui Chen, Shan Luo, and Hao Su. Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai. Robotics: Science and Systems, 2025.   
[46] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In 2012 IEEE/RSJ international conference on intelligent robots and systems, pages 5026–5033. IEEE, 2012.   
[47] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe Hansen-Estruch, Quan Vuong, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale. In Conference on Robot Learning (CoRL), 2023.   
[48] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. Vggt: Visual geometry grounded transformer. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 5294–5306, 2025.   
[49] Zifan Wang, Yufei Jia, Lu Shi, Haoyu Wang, Haizhou Zhao, Xueyang Li, Jinni Zhou, Jun Ma, and Guyue Zhou. Arm-constrained curriculum learning for locomanipulation of a wheel-legged robot. In 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 10770–10776. IEEE, 2024.   
[50] Zifan Wang, Teli Ma, Yufei Jia, Xun Yang, Jiaming Zhou, Wenlong Ouyang, Qiang Zhang, and Junwei Liang. Omni-perception: Omnidirectional collision avoidance

for legged locomotion in dynamic environments. arXiv preprint arXiv:2505.19214, 2025.   
[51] Haoru Xue, Tairan He, Zi Wang, Qingwei Ben, Wenli Xiao, Zhengyi Luo, Xingye Da, Fernando Castaneda, ˜ Guanya Shi, Shankar Sastry, et al. Opening the simto-real door for humanoid pixel-to-action policy transfer. arXiv preprint arXiv:2512.01061, 2025.   
[52] Sizhe Yang, Wenye Yu, Jia Zeng, Jun Lv, Kerui Ren, Cewu Lu, Dahua Lin, and Jiangmiao Pang. Novel demonstration generation with gaussian splatting enables robust one-shot manipulation. arXiv preprint arXiv:2504.13175, 2025.   
[53] Zhao-Heng Yin, Changhao Wang, Luis Pineda, Francois Hogan, Krishna Bodduluri, Akash Sharma, Patrick Lancaster, Ishita Prasad, Mrinal Kalakrishnan, Jitendra Malik, et al. DexterityGen: Foundation controller for unprecedented dexterity. In Proceedings of Robotics: Science and Systems (RSS), 2025.   
[54] Justin Yu, Letian Fu, Huang Huang, Karim El-Refai, Rares Andrei Ambrus, Richard Cheng, Muhammad Zubair Irshad, and Ken Goldberg. Real2render2real: Scaling robot data without dynamics simulation or robot hardware. arXiv preprint arXiv:2505.09601, 2025.   
[55] Kevin Zakka, Baruch Tabanpour, Qiayuan Liao, Mustafa Haiderbhai, Samuel Holt, Jing Yuan Luo, Arthur Allshire, Erik Frey, Koushil Sreenath, Lueder A Kahrs, et al. Mujoco playground. arXiv preprint arXiv:2502.08844, 2025.   
[56] Shaopeng Zhai, Qi Zhang, Tianyi Zhang, Fuxian Huang, Haoran Zhang, Ming Zhou, Shengzhe Zhang, Litao Liu, Sixu Lin, and Jiangmiao Pang. A vision-languageaction-critic model for robotic real-world reinforcement learning. arXiv preprint arXiv:2509.15937, 2025.   
[57] Jiazhao Zhang, Kunyu Wang, Shaoan Wang, Minghan Li, Haoran Liu, Songlin Wei, Zhongyuan Wang, Zhizheng Zhang, and He Wang. Uni-navid: A video-based visionlanguage-action model for unifying embodied navigation tasks. arXiv preprint arXiv:2412.06224, 2024.   
[58] Jiazhao Zhang, Anqi Li, Yunpeng Qi, Minghan Li, Jiahang Liu, Shaoan Wang, Haoran Liu, Gengze Zhou, Yuze Wu, Xingxing Li, et al. Embodied navigation foundation model. arXiv preprint arXiv:2509.12129, 2025.   
[59] Kaifeng Zhang, Shuo Sha, Hanxiao Jiang, Matthew Loper, Hyunjong Song, Guangyan Cai, Zhuo Xu, Xiaochen Hu, Changxi Zheng, and Yunzhu Li. Realto-sim robot policy evaluation with gaussian splatting simulation of soft-body interactions. arXiv preprint arXiv:2511.04665, 2025.   
[60] Yang Zhang, Zhanxiang Cao, Buqing Nie, Haoyang Li, Zhong Jiangwei, Qiao Sun, Xiaoyi Hu, Xiaokang Yang, and Yue Gao. Keep on going: Learning robust humanoid motion skills via selective adversarial training. arXiv preprint arXiv:2507.08303, 2025.   
[61] Xian Zhou, Yiling Qiao, Zhenjia Xu, TH Wang, Z Chen, J Zheng, Z Xiong, Y Wang, M Zhang, P Ma, et al. Genesis: A generative and universal physics engine for

robotics and beyond. arXiv preprint arXiv:2401.01454, 2024.   
[62] Zhongyi Zhou, Yichen Zhu, Junjie Wen, Chaomin Shen, and Yi Xu. Vision-language-action model with openworld embodied reasoning from pretrained knowledge. arXiv preprint arXiv:2505.21906, 2025.   
[63] Yuke Zhu, Josiah Wong, Ajay Mandlekar, Roberto Mart´ın-Mart´ın, Abhishek Joshi, Soroush Nasiriany, and Yifeng Zhu. robosuite: A modular simulation framework and benchmark for robot learning. arXiv preprint arXiv:2009.12293, 2020.   
[64] Ziwen Zhuang, Zipeng Fu, Jianren Wang, Christopher Atkeson, Soeren Schwertfeger, Chelsea Finn, and Hang Zhao. Robot parkour learning. arXiv preprint arXiv:2309.05665, 2023.

# Appendix

# TABLE OF CONTENTS

# Appendix A. Physics 13

A.1 Shaking Test . 13

# Appendix B. 3DGS Asset and Rendering 13

B.1 Assets Generation 13   
B.2 RLGK 14   
B.3 Consistency of Policy Performance between Simulation and Real World 15

# Appendix C. Locomotion 15

C.1 Environment Setup 15   
C.2 Training Details 16   
C.3 Specialized Perception . . 17

# Appendix D. Manipulation 18

D.1 Environment Setup 18   
D.2 Training Details 18   
D.3 Comparison with Other Simulators . 19

# Appendix E. Navigation 20

E.1 Task Definition 20   
E.2 Scene Reconstruction and Rendering . . 21   
E.3 Training Details 21

# Appendix F. MJCF Compatibility 21

F.1 Global Configuration 21   
F.2 Asset Management 22   
F.3 Scene Description 22   
F.4 Constraints and Equality 22   
F.5 Actuators and Sensors . 22   
F.6 Visuals and Defaults . 22

# APPENDIX A. PHYSICS

# A.1 Shaking Test

To evaluate the stability and robustness of frictional contacts under dynamic perturbations, we conducted a ”Shaking Test” using a Franka Panda arm. The robot grasps objects with different geometries—a cube, a ball, and a bottle—and executes aggressive random shaking motions. Each result aggregates 30 trials per object across three geometries. We compare the success rates of retaining the object across different physics engines at two simulation time steps: $d t = 0 . 0 0 2 s$ and $d t = 0 . 0 1 s$ .

As shown in Table V and Figure 9, GS-Playground demonstrates superior grasping robustness. The CPU backend achieves a $100 \%$ success rate (90/90) across all object types and time steps, attributed to our velocity-impulse formulation and strict complementarity constraints which effectively prevent numerical drift and slippage. In contrast, MuJoCo variants (Euler, Implicit, and Implicit+Noslip) struggle significantly with this task, often dropping the object due to insufficient friction retention under high accelerations. IsaacSim and Genesis show better performance but still experience failures (60/90 success). Our GPU backend also maintains high stability, validating the effectiveness of our parallel solver design.

# APPENDIX B. 3DGS ASSET AND RENDERING

# B.1 Assets Generation

Building upon the widely used Bridge-v2 dataset1, we introduce the Bridge-GS dataset, a large-scale collection of simulationready 3D assets generated via our automated pipeline. While the original Bridge-v2 dataset primarily consists of RGB images and robot trajectories, Bridge-GS significantly enriches this data by providing fully reconstructed scene-level and object-level

TABLE V: Grasping robustness under external disturbances. Success rates for a Franka Panda holding various geometries (cube, ball, bottle) under random shaking. A trial is successful if the object is retained for the entire evaluation horizon.   

<table><tr><td>Engine</td><td>dt=0.002s (success)</td><td>dt=0.01s (success)</td></tr><tr><td>MuJoCo (Euler)</td><td>0/90</td><td>0/90</td></tr><tr><td>MuJoCo (Implicit)</td><td>0/90</td><td>0/90</td></tr><tr><td>MuJoCo (Implicit+Noslip)</td><td>4/90</td><td>0/90</td></tr><tr><td>MJWarp</td><td>0/90</td><td>10/90</td></tr><tr><td>IsaacSim</td><td>60/90</td><td>60/90</td></tr><tr><td>Genesis</td><td>60/90</td><td>60/90</td></tr><tr><td>Ours (CPU)</td><td>90/90</td><td>90/90</td></tr><tr><td>Ours (GPU)</td><td>90/90</td><td>74/90</td></tr></table>

Fig. 9: Shaking Test Scene: A Franka Panda robot grasps various objects (a cube, a ball, and a bottle) while being subjected to random shaking motions. This setup is used to evaluate the grasping robustness of different simulation methods under dynamic perturbations.

3D Gaussian Splatting (3DGS) representations, along with object-level meshes, 6D object poses, and calibrated camera intrinsics and extrinsics.

Figure 10 illustrates samples from the Bridge-GS dataset. The dataset encapsulates diverse real-world scenes converted into digital twins, preserving visual fidelity while enabling physical interaction. Each column represents a distinct scene processed by our pipeline. The top row displays the original RGB images from the Bridge-v2 dataset. The subsequent rows show the intermediate and final outputs of our pipeline: the estimated depth maps used for geometry estimation, the instance segmentation masks identifying interactable objects, and the final composited 3DGS assets rendered in the simulation environment. This rich set of 3D annotations empowers researchers to train visuomotor policies in high-fidelity simulated replicas of real-world environments.

In addition to Bridge-v2, we further validate our pipeline using the InteriorGS dataset2. Although InteriorGS provides ground-truth 3DGS representations, we utilize it strictly as a source of diverse indoor RGB imagery. We render 2D snapshots from the scenes and feed them into our pipeline as raw input, without accessing the underlying 3D data. As shown in the bottom half of Figure 10, our pipeline successfully reconstructs these complex indoor environments into simulation-ready assets—recovering geometry, segmentation, and 3DGS representations purely from the rendered images. This demonstrates the pipeline’s robustness and its capability to generalize to a wide variety of indoor settings beyond the specific domain of Bridge-v2.

# B.2 RLGK

Rigid-Link Gaussian Kinematics (RLGK) is a mechanism designed to efficiently synchronize the state of millions of 3D Gaussians with the low-dimensional rigid body states derived from the physics engine. The core logic of RLGK is to map the update of high-dimensional visual representations to low-dimensional rigid body transformations, executing the synchronization process via massively parallelized vector operations on the GPU. Importantly, our implementation is optimized for batched environments, enabling the simultaneous simulation and rendering of $B$ parallel scenes (e.g., $B = 2 0 4 8 )$ using a single geometry template.

During the initialization phase, we upload a single ”template” of the scene’s Gaussians to GPU memory. We assign a rigid body index $k \in \{ 0 , \ldots , N _{b o d i e s} \}$ to each Gaussian $g _{i}$ and store the initial local configuration $\{ p _{l o c a l} ^{i} , q _{l o c a l} ^{i} \}$ relative to the body frame. At runtime, the physics engine outputs a batch of global poses $\mathbf{S} _{t} \in \mathbb{R} ^{B \times \bar{N _ { b o d i e s} } \times 7 }$ containing the state of every rigid body in every parallel environment. RLGK performs a batched gather operation to retrieve the transform for every Gaussian across all environments simultaneously. The new global state for the $j$ -th environment and $i$ -th Gaussian is computed via:

$$
p _{w o r l d} ^{(j, i)} = R \left(q _{k} ^{(j, t)}\right) p _{l o c a l} ^{i} + t _{k} ^{(j, t)} \tag{8}
$$

$$
q _{w o r l d} ^{(j, i)} = q _{k} ^{(j, t)} \otimes q _{l o c a l} ^{i} \tag{9}
$$

Fig. 10: Visual results of the asset generation pipeline on (top) Bridge-GS and (bottom) InteriorGS datasets. The rows display: (1) Original RGB images; (2) Estimated depth maps; (3) Instance segmentation masks; and (4) Reconstructed simulation-ready 3DGS assets.

This design allows for updating $B \times M$ points (where $M \approx 1 0 ^{6}$ ) in sub-milliseconds. By broadcasting the single template geometry $\{ p _{l o c a l} ^{i} \}$ across $B$ environments, we minimize memory bandwidth usage. The algorithmic description is provided in Algorithm 1.

# B.3 Consistency of Policy Performance between Simulation and Real World

We present the consistency analysis in Figure 11. We evaluated three representative imitation learning algorithms—ACT, Diffusion Policy (DP), and $\pi _{0}$ —across four diverse manipulation tasks: Push Mouse, Close Laptop, Pick Fruit, and Stack Cube. First, our experiments demonstrate a strong correlation (0.89) between simulation and real-world success rates, indicating that our simulation environment achieves high consistency with the physical world across different policy architectures and task scenarios. Second, as detailed in Section III-C, our efficient pruning strategy significantly reduces the number of Gaussians while maintaining high visual fidelity. The comparison between full and pruned 3DGS rendering shows that this reduction in point count has a negligible impact on the validation success rate of imitation learning policies. This confirms that our compression strategy effectively preserves the essential visual features required for policy learning while significantly lowering the method’s computational footprint.

# APPENDIX C. LOCOMOTION

# C.1 Environment Setup

In this task, we consider two environments: a Unitree Go2 quadruped environment and a Unitree G1 humanoid environment.

Algorithm 1 Batched Rigid-Link Gaussian Kinematics (RLGK)   
1: Input: Template Gaussians $\mathcal{G} = \{g_1,\dots ,g_M\}$ , Batch Size   
2: Pre-computation:   
3: for each Gaussian $g_i\in \mathcal{G}$ do   
4: Identify body index $k_{i}\in \{1,\ldots ,N_{bodies}\}$ 5: Store local pose: $p_{local}^{i},q_{local}^{i}$ 6: IndexMap[i] $\leftarrow$ ki   
7: end for   
8: Runtime Loop (at step t):   
9: Receive batch body states $\mathbf{S}_t\in \mathbb{R}^{B\times N_{bodies}\times 7}$ 10: Transfer $\mathbf{S}_t$ to GPU memory   
11: // Massive Parallel Update for $(B\times M)$ Gaussians   
12: $K\gets \mathbf{S}_t[:,IndexMap]$ 13: $\mathbf{P}_{world}\gets \mathrm{Transform}(\mathbf{P}_{local},K.p,K.q)$ 14: $\mathbf{Q}_{world}\gets K.q\otimes \mathbf{Q}_{local}$ 15: Update renderer buffers with batched state $\mathbf{P}_{world},\mathbf{Q}_{world}$

$\triangleright$ Gather: $(B,N_{bodies})\to (B,M)$ $\triangleright$ Broadcast $(1,M)$ to $(B,M)$

![[99_Attachments/papers/images/gs-playground/09de75c85fc4abb9359a86c2243bc0a6ce1c76a354ce7ca166828decbc7e4670.jpg]]  
Fig. 11: We compare the success rates of different policies in simulation and the real world on various tasks.

# C.2 Training Details

Observation and Action. We use a unified observation space for all environments:

• Gravity projected in body frame   
• Angular velocity   
• Joint positions   
• Joint velocities   
• Previous action   
• Velocity commands   
• Phase

The action space is defined as absolute joint position with a default offset:

$$
q _{t} = q _{d} + k _{a} a \tag{10}
$$

where $k _{a}$ is the action scale, $q _{d}$ is the default position and $a$ is the action. We employ a PD controller to map joint position to torque:

$$
\tau = k _{p} \left(q _{t} - q\right) - k _{d} \dot{q} \tag{11}
$$

Domain Randomization. For better sim-to-real transfer, we employ domain randomization by randomizing the following components:

• Sensor noise: We add Gaussian noise to the data from each sensor.   
• Physical parameters: Noise is introduced to physical quantities that are difficult to measure accurately, such as inertia and the center of mass, to enhance the robustness of the policy.

Reward Function. The training rewards are detailed in Table VI.

TABLE VI: Reward Functions for Locomotion Tasks   

<table><tr><td>Reward</td><td>Go2 Weight</td><td>G1 Weight</td><td>Expression</td></tr><tr><td>Joint torques</td><td>-1e-5</td><td>-1e-5</td><td>|τ|2</td></tr><tr><td>Dof pos limits</td><td>-1</td><td></td><td>|q| - qmax</td></tr><tr><td>Feet air time</td><td>1</td><td>2</td><td>(tair - threshold) * (1 - Qd)</td></tr><tr><td>Speed tracking</td><td>1</td><td>1</td><td>e-[(vcom-vd)/0.01 + (ωcom-ωd)/0.005]</td></tr><tr><td>Z-axis velocity</td><td>-2</td><td>-4</td><td>|vCoM,z|2</td></tr><tr><td>Action rate</td><td>-0.02</td><td>-0.01</td><td>|Δqlast - △q|2</td></tr><tr><td>Joint acc</td><td>-2.5e-7</td><td>-2.5e-7</td><td>|qlast-ˆ/△t|2</td></tr></table>

Network Architecture. We employ an asymmetric actor–critic setup, in which the policy network (actor) and the value network (critic) receive different observation inputs. The policy network is fed with the aforementioned observations, while the value network additionally receives uncorrupted versions of these signals and extra sensor readings such as contact forces, perturbation forces, and linear velocity. Both policy and value networks use a three-layer multilayer perceptron (MLP) with hidden sizes of 256, 128, and 64.

Training Curve. Learning curves for the G1 and Go2 Joystick tasks are shown in Figure 12 and Figure 13, respectively.

Fig. 12: Learning curves for the G1 Joystick task.

Fig. 13: Learning curves for the Go2 Joystick task.

# C.3 Specialized Perception

To enable robust locomotion across diverse terrains, we provide a suite of high-fidelity exteroceptive sensors compatible with various robot embodiments. As illustrated in Figure 14, these sensors can be flexibly configured to suit different tasks and morphologies.

Height Scan. The Height Scan sensor projects a grid of ray-casts downwards around the robot base to sample terrain elevation relative to the body frame. This local height map provides high-frequency terrain geometry information, essential for traversability analysis on rough terrain. In our benchmarks, we equip the Unitree Go2 quadruped with this sensor to facilitate adaptive gait generation on uneven surfaces.

LiDAR. The 3D LiDAR sensor performs omnidirectional or bounded ray-casting to generate a sparse point cloud of the environment. This modality is critical for obstacle detection, mapping, and navigation in cluttered spaces. We demonstrate its integration on the Unitree G1 humanoid for humanoid locomotion tasks.

Both sensors leverage our batched ray-casting engine to maintain high throughput during massive parallel training.

Fig. 14: Perception setups for locomotion tasks. Left: The Unitree Go2 robot utilizing a Height Scan sensor to perceive terrain geometry on rough terrain. Right: The Unitree G1 humanoid equipped with a LiDAR sensor for environmental awareness.

# APPENDIX D. MANIPULATION

# D.1 Environment Setup

The environment used is AIRBOT Play PickCube, as shown in Figure 15. The objective of this task is to control the robotic arm to grasp a cube placed on the table and lift it to a specified target position.

Fig. 15: The AIRBOT Play PickCube manipulation environment setup. The robot needs to grasp the green cube and lift it to the target position.

# D.2 Training Details

# Observation and Action.

• Observation Space

– Arm joint positions   
– Gripper position   
– Target position   
– Joint tracking error: the difference between the current control command and the robot’s current joint positions   
– Two input RGB images

• Action Space

– 6 DoF joint positions   
– 1 Gripper position

# Domain Randomization.

• Camera poses: We perform multi-camera domain randomization by perturbing each camera’s extrinsics independently for every parallel world. For each camera, we add a per-axis uniform translation offset in the range $\pm 0 . 0 2 \textrm { m }$ to the nominal camera position, and apply a small random rotation by sampling a random 3D axis and a rotation angle uniformly up to $5 ^{\circ}$ (axis–angle quaternion, then composed with the original orientation).   
• Box initial and target positions: At each reset, we randomize the initial 3D positions of both the box and the target by sampling a small uniform offset around their nominal location. The box is perturbed within $\pm 5 \ \mathrm { c m }$ in x, $\pm 1 0 \ \mathrm { c m }$ in y, and $\mathrm { 0 ~ c m }$ in z, while the target is perturbed within $\mathrm { 0 ~ c m }$ in x, $\pm 1 0 ~ \mathrm { c m }$ in y, and $3 { - } 8 ~ \mathrm { c m }$ upward in z (all relative to the same nominal reference).

# Reward Function.

TABLE VII: Reward Functions for PickCube Manipulation   

<table><tr><td>Reward</td><td>Weight</td><td>Expression</td></tr><tr><td>Gripper-Box Proximity</td><td>5.0</td><td>1 - tanh(5 ||pbox - pgrip ||)</td></tr><tr><td>Box-Target Tracking</td><td>5.0</td><td>(1 - tanh(5 ||ptgt - pbox ||)) Ireach</td></tr><tr><td>No Floor Collision</td><td>0.25</td><td>1 - Ifloor</td></tr><tr><td>No Box Collision</td><td>0.5</td><td>1 - Ihand-box</td></tr><tr><td>Gripper Closing</td><td>20.0</td><td>(1 - |ug - umin| / umax - umin) Ireach</td></tr><tr><td>Lifted (sparse)</td><td>8.0</td><td>I(pzbox &gt; pzbox,0 + 0.005) Ireach</td></tr><tr><td>Success (sparse)</td><td>10.0</td><td>I(||pbox - ptgt || &lt; ε)</td></tr></table>

Notation. $\mathbf{p} _{\mathrm { b o x} }$ is the box position, $\mathbf{p} _{\mathrm { t g t} }$ is the target (mocap) position, and $\mathbf{p} _{\mathrm { g r i p} }$ is the gripper site position. $p _{\mathrm { b o x} } ^{z}$ and $p _{\mathrm { b o x} , 0 } ^{z}$ denote the current and initial box height, respectively. $u _{g}$ is the gripper control command (last control dimension), with limits $u _{\mathrm { m i n} }$ and umax. I(·) is the indicator function. $\mathbb{I} _{\mathrm { r e a c h} } = \mathbb{I} ( \| \mathbf{p} _{\mathrm { b o x} } - \mathbf{p} _{\mathrm { g r i p} } \| < 0 . 0 1 5 )$ gates rewards that should only activate after the gripper reaches the box. $\mathbb{I} _{\mathrm { f l o o r} }$ and $\mathbb{I} _{\mathrm { h a n d - b o x} }$ indicate floor contact and hand–box collision as detected by contact sensors. ϵ is the success threshold (set to 0.01 in our experiments). The sparse bonuses ”Lifted” and ”Success” are applied in the vision setting. The episode reward is computed as $\begin{array} { r } { \mathrm { c l i p } ( \sum _{i} w _{i} r _{i} , - 1 0 ^{4} , 1 0 ^{4} ) } \end{array}$ .

Termination. The episode terminates when any of the following conditions becomes true: (i) the box goes out of bounds (any coordinate exceeds $1 . 0 \textrm { m }$ in magnitude, or the box drops below its initial height by more than $0 . 0 1 \mathrm { ~ m ~ }$ ), (ii) the simulation state becomes non-finite (any NaN in qpos or qvel), or (iii) the task is successful.

Network Architecture and Hyperparameters. We used the same vision PPO network as in Mujoco Playground, except that we modified the output features of the CNN encoders for both the actor and critic to 16. The training hyperparameters are shown in Table VIII.

TABLE VIII: PPO Hyperparameters for Manipulation   

<table><tr><td>Hyperparameter</td><td>Default Value</td></tr><tr><td>empirical_normalization</td><td>True</td></tr><tr><td>num_minibatches</td><td>8</td></tr><tr><td>discounting</td><td>0.97</td></tr><tr><td>learning_rate</td><td>1e-3</td></tr><tr><td>num_envs</td><td>2048</td></tr><tr><td>num_steps_per_env</td><td>40</td></tr><tr><td>value_loss coef</td><td>1.0</td></tr><tr><td>use_clipped_value_loss</td><td>True</td></tr><tr><td>clipparam</td><td>0.2</td></tr><tr><td>entropycoef</td><td>0.01</td></tr><tr><td>num_learning_epochs</td><td>4</td></tr><tr><td>schedule</td><td>adaptive</td></tr><tr><td>gamma</td><td>0.97</td></tr><tr><td>lam</td><td>0.95</td></tr><tr><td>desired_kl</td><td>0.01</td></tr><tr><td>max_grad_norm</td><td>1.0</td></tr></table>

# D.3 Comparison with Other Simulators

We conducted comparative experiments with other simulators, specifically Mujoco Playground, ManiSkill3, and Isaac Lab. All of these simulators support large-scale parallel rendering. All simulators employed the same image domain randomization

strategies, including variations in brightness, contrast and exposure. However, due to the difficulty in modeling simulation assets for the environment and the significant visual gap between simulation and reality, the success rate when deploying these policies in the real world was $0 \%$ .

Fig. 16: Render comparison. From left to right: Real World, Ours, Isaac Lab, ManiSkill3, and Mujoco.

We evaluated each policy over 20 trials. As shown in Table IX, our method achieved a success rate of $90 \%$ , being the only method capable of successful sim-to-real transfer.

TABLE IX: Sim-to-Real Success Rates across Different Simulators. Each method was evaluated over 20 trials.   

<table><tr><td>Simulator</td><td>Success Rate</td></tr><tr><td>Mujoco</td><td>0%</td></tr><tr><td>ManiSkill3</td><td>0%</td></tr><tr><td>Isaac Lab</td><td>0%</td></tr><tr><td>Ours</td><td>90%</td></tr></table>

Training Curve. In Figure 17 we report environment steps versus reward across 4 seeds on a single A100 GPU.

Fig. 17: Learning curves for the PickCube manipulation task.

# APPENDIX E. NAVIGATION

# E.1 Task Definition

We evaluate a simplified visual goal-seeking task in structured indoor scenes. The Unitree Go2 robot is required to locate and approach a red traffic cone based on egocentric RGB observations, within a time limit of $T _{\mathrm { m a x} } = 2 5$ seconds. The task is successful when the Euclidean distance between the robot’s base and the center of the target cone falls below a threshold $\epsilon = 0 . 3 5$ meters. The robot’s initial pose and the cone position are randomized at episode start (see Domain Randomization).

# E.2 Scene Reconstruction and Rendering

The simulation scene is captured with an RGB camera and reconstructed using the PGSR algorithm to obtain a 3D representation suitable for rendering. During training, RGB observations are rendered from the robot dog’s egocentric viewpoint (camera pose and intrinsics aligned with the Go2’s onboard camera) so that the policy receives first-person visual input consistent with real-world deployment.

# E.3 Training Details

Observation and Action Space. We use a hierarchical setup: a high-level navigation policy runs at $5 \mathrm { H z }$ and outputs velocity commands; a low-level locomotion controller runs at $5 0 \mathrm { H z }$ and maps commands plus proprioception to joint targets. The low-level controller is pre-trained with domain randomization and remains frozen during navigation training.

The observation space for the high-level policy is 228-dimensional: (1) Visual features (192 dimensions), i.e., image embeddings from a Vision Transformer (ViT) encoder; (2) Task command (3 dimensions), a one-hot vector indicating the target color—in this simplified task only the red cone is used; (3) Proprioception (33 dimensions), including base angular velocity, projected gravity, joint positions, joint velocities, and the previous action. The action space consists of 3 continuous velocity commands $\mathbf{v} _{\mathrm { c m d} } = ( v _{x} , v _{y} , \omega _{\mathrm { y a w} } )$ , squashed by a Tanh activation and scaled to the robot’s physical limits.

Policy Architecture. The high-level policy uses an asymmetric Actor-Critic structure. The Actor takes the observations above and incorporates a pre-trained ViT encoder (frozen during navigation training) to extract features from $2 2 4 \times 2 2 4$ RGB images, followed by an LSTM to aggregate temporal information. The Critic uses the same visual and proprioceptive inputs; implementation details follow the same asymmetric design as in the locomotion appendix. Both policy and value networks are optimized with PPO.

Reward Function. The reward function is given in Table X. It combines a sparse success bonus for reaching the goal with dense terms for goal distance reduction and heading alignment, plus regularization for action smoothness and velocity tracking.

TABLE X: Reward Function for High-Level Navigation Policy   

<table><tr><td>Reward Term</td><td>Expression / Description</td><td>Weight</td></tr><tr><td colspan="3">Task Rewards</td></tr><tr><td>Reach Goal</td><td>\(\mathbb{I}(d_{\text{target}} &lt; 0.35)\)</td><td>30.0</td></tr><tr><td>Goal Distance</td><td>\(d_{t-1}-d_t\) (towards target)</td><td>15.0</td></tr><tr><td>Goal Heading</td><td>\(\exp(-2(\Delta \psi/\pi)^2) \cdot \mathbb{I}(d &gt; 0.25)\)</td><td>3.0</td></tr><tr><td>Stand Still</td><td>Encourages stopping at goal</td><td>1.0</td></tr><tr><td colspan="3">Regularization</td></tr><tr><td>Action Smoothness</td><td>-\(\|\mathbf{a}\|^2\) (L2 norm)</td><td>-0.01</td></tr><tr><td>Velocity Tracking</td><td>\(\exp(-\|\mathbf{v}_{\text{cmd}} - \mathbf{v}_{\text{real}}\|^2/\sigma)\)</td><td>0.2</td></tr></table>

Domain Randomization. To improve sim-to-real transfer, we apply domain randomization during training: initial state—the robot’s initial position and yaw are randomly sampled within the feasible area, and the target cone position is randomized around predefined anchor points with additive noise; visual—random perturbations to camera extrinsics, and injection of image noise and motion blur; physical—random external pushes on the robot base and randomized link masses.

Training Hyperparameters. All experiments are run on a workstation with a single NVIDIA RTX 4090 GPU. We use GS-Playground with 48 parallel environments and train the high-level navigation policy with PPO for 10,000 iterations. The learning rate follows an adaptive schedule with initial value $1 . 0 \times 1 0 ^{- 3}$ , mini-batch size is 2, and the discount factor is $\gamma = 0 . 9 8$ . Further PPO and environment settings are consistent with the locomotion task where applicable.

# APPENDIX F. MJCF COMPATIBILITY

MJCF is a widely used format in the field of robotics simulation. GS-Playground provides extensive compatibility support for MJCF while maintaining its own simulation capabilities and features.

The details of current MJCF support status in GS-Playground are listed below:

# F.1 Global Configuration

GS-Playground fully supports critical global options such as timestep, gravity, and solver parameters (tolerance, iterations). Contact parameters including o_margin, o_solref, o_solimp, and o_friction are also supported, ensuring consistent physics behavior. We are planning to support additional environmental factors like wind and magnetic fields in future updates.

For the compiler configuration, essential attributes like autolimits, angle, eulerseq, and asset directories (meshdir, texturedir) are supported, allowing for seamless model compilation.

# F.2 Asset Management

GS-Playground supports a wide range of asset definitions:

• Mesh: Supports .stl, .obj, and .dae formats. Key attributes like file, vertex, scale, and refpos are supported.   
• Texture & Material: Supports 2d and skybox texture types, along with material properties such as reflectance, metallic, and roughness for realistic rendering.   
• Height Field: Supports hfield definitions for complex terrain generation.

# F.3 Scene Description

The core scene elements are well-supported to reconstruct complex robotic environments:

• Bodies & Joints: Supports body definitions with pos, orientation, and inertial properties. A comprehensive set of joint attributes is implemented, including stiffness, damping, frictionloss, armature, and limited ranges.   
• Geometries: Supports primitive types (plane, sphere, capsule, cylinder, box) and mesh geoms. Contact dynamics properties like solref, solimp, friction, and condim are fully compatible.   
• Lights & Cameras: Supports spot, directional, and point lights with shadow casting capabilities. Cameras can be configured with fovy, target, and tracking modes (fixed, track).

# F.4 Constraints and Equality

To model complex mechanical linkages, GS-Playground supports:

• Equality Constraints: connect, weld, and joint equality constraints are supported, allowing for loop closures and rigid attachments.   
• Tendons: Supports fixed tendons with length limits, stiffness, and damping properties.

# F.5 Actuators and Sensors

• Actuators: Supports motor, position, velocity, and general actuators. Control limits (ctrllimited, forcerange) and gain parameters (kp, kv, gear) are fully implemented.   
• Sensors: A rich suite of sensors is available, including accelerometer, velocimeter, jointpos, jointvel, and frame-based sensors (framepos, framequat, framelinvel, etc.), enabling comprehensive state observation.

# F.6 Visuals and Defaults

GS-Playground respects visual settings including global fog and lighting configurations. It also supports the default class system, allowing users to define hierarchical default properties for geom, joint, material, and other elements to streamline MJCF file structure.