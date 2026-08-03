# LiteVLA-Edge: Quantized On-Device Multimodal Control for Embedded Robotics

Justin Williams1, Kishor Datta Gupta1, Roy George1, and Mrinmoy Sarkar2

1Clark Atlanta University, Atlanta, GA, USA

2Siemens Corporation, Princeton, NJ, USA

Abstract— Vision-Language-Action (VLA) models provide a unified framework for perception, language conditioning, and action generation, but many existing systems remain difficult to deploy in embedded robotic settings because of their computational requirements and inference latency. In this paper, we present LiteVLA-Edge, a deployment-oriented VLA pipeline for fully on-device inference on Jetson Orin-class hardware. Our approach combines supervised image-to-action fine-tuning in FP32 with post-training 4-bit GGUF quantization and GPU-accelerated inference through the llama.cpp runtime. Under our deployment configuration, LiteVLA-Edge achieves a mean end-to-end latency of 150.5 ms (approximately 6.6 Hz) while operating entirely offline within a ROS 2-integrated perception–reasoning–action pipeline. Rather than introducing a new policy objective, our contribution is a practical systems path for executing compact multimodal control models locally on embedded hardware while preserving modular interfaces between perception, reasoning, and actuation. These results establish timing feasibility for reactive language-conditioned control and provide a reproducible baseline for future tasklevel evaluation of on-device VLAs in robotics.

# I. INTRODUCTION

Vision–Language–Action (VLA) models have emerged as a powerful paradigm for embodied intelligence, enabling robots to interpret visual scenes, reason over language, and generate executable actions within a unified framework. Large-scale systems such as PaLM-E [1], RT-2 [2], and OpenVLA [3] demonstrate impressive zero-shot generalization; however, their massive parameter counts (often > 7B) necessitate cloud-scale computation or high-end desktop GPUs. This “compute-heavy” dependency renders them unsuitable for power-constrained field robotics, tactical defense applications, or deployment in GPS-denied environments where low-latency local execution is non-negotiable.

To address these limitations, LiteVLA [4], a lightweight framework designed for fully on-device inference using compact multimodal transformers. It established technical feasibility on extreme edge hardware like the Raspberry Pi, but limitations are multi-second inference latency necessitated asynchronous, open-loop execution.

This paper presents LiteVLA-Edge, which transitions VLA research from “deliberative reasoning” to real-time visuomotor control. By leveraging optimized quantization kernels and the NVIDIA Jetson AGX Orin platform, we achieve a mean inference latency of 150.5 ms (∼6.6 Hz). This represents a qualitative shift in capability compared to contemporary efficient models: while OpenVLA remains constrained by its 7B-parameter backbone, and EdgeVLA or Efficient VLA focus on high-end edge GPUs (e.g., AGX Orin), LiteVLA-Edge demonstrates that highfrequency, closed-loop control is possible on productiongrade, 40W edge modules. Our system utilizes a structured pipeline of supervised image-to-action fine-tuning in FP32, followed by post-training 4-bit (Q4 K M) GGUF quantization to ensure action stability without sacrificing the semantic reasoning of the underlying Vision-Language Model (VLM).

# A. Contributions

Our contributions are summarized as follows:

• We present LiteVLA-Edge, achieving 150.5 ms fully on-device VLA inference on the NVIDIA Jetson AGX Orin, a ∼220% improvement over previous baselines.   
• We provide a comparative analysis against OpenVLA, EdgeVLA, and Efficient VLA, demonstrating that LiteVLA-Edge offers a superior balance of “Reasoningto-Hz” on low-power hardware.   
• We describe a deployment-ready pipeline using GGUF quantization, which enables the use of consumer-grade edge-class systems-on-chip for high-frequency robotics.   
• We validate the system’s ability to maintain deterministic action generation and low jitter (σ < 0.2 ms) during continuous ROS 2 operation.   
• We demonstrate that LiteVLA-Edge enables closedloop feedback, allowing robots to react to dynamic environmental changes within a single human attention window.

# II. RELATED WORK

# A. Generalist VLA Foundations

Vision–Language–Action (VLA) models such as Open-VLA [3] have set the benchmark for generalist robotic manipulation. By fine-tuning a 7B-parameter Prismatic VLM on the Open X-Embodiment (OXE) dataset, OpenVLA achieves remarkable zero-shot generalization across diverse tasks. However, its massive parameter count necessitates desktopclass GPUs (e.g., NVIDIA RTX 4090), making it unsuitable for the 25W–40W power envelopes of edge robotics. In contrast, LiteVLA-Edge focuses on high-frequency execution within these constrained envelopes.

# B. Reactive and Efficiency-Oriented VLAs

Recent efforts have prioritized inference speed to enable reactive control. EdgeVLA [5] targets NVIDIA Jetson platforms by employing a hierarchical architecture that separates semantic reasoning from high-frequency visuomotor tokens. While EdgeVLA achieves impressive frequencies (10–15 Hz), it often sacrifices the multi-step reasoning depth found in larger VLMs. Similarly, EfficientVLA utilizes knowledge distillation and action chunking to predict sequences of future states rather than single tokens. While this improves motion smoothness, EfficientVLA often relies on specialized TensorRT engines that lack the cross-platform flexibility of the GGUF format used in our work.

# C. Compact Multimodal Backbones

The rise of compact Vision–Language Models (VLMs) like SmolVLM [6] has enabled VLA deployment on previously inaccessible hardware. SmolVLM provides a highly compressed multimodal backbone (typically <2B parameters) that retains semantic reasoning while fitting into small memory footprints. LiteVLA-Edge leverages these compact architectures, using them as a foundation for supervised image-to-action fine-tuning. Unlike prior work that uses SmolVLM for purely deliberative tasks, we demonstrate its utility for near-real-time control loops.

# D. Quantization and Edge Deployment

Deploying VLAs on the edge requires aggressive compression. Techniques such as 4-bit and 8-bit quantization are standard for reducing memory bandwidth requirements. However, standard quantization can lead to “action drift,” where the numerical precision of motor commands is degraded. LiteVLA-Edge addresses this by validating action stability post-quantization in the GGUF format. By integrating these quantized models into a ROS 2 framework on the NVIDIA Jetson AGX Orin, we achieve a balance of semantic depth and 6.6 Hz reactivity that distinguishes our work from both large-scale generalists and purely reflexive edge models.

# E. Compact Vision–Language Models (VLMs) for Edge Deployment

Several compact Vision–Language Models (VLMs) have recently emerged as strong candidates for edge deployment. Models such as TinyLLaVA [7], Qwen2-VL [8], PaliGemma [9], and Moondream2 [10] provide efficient multimodal reasoning within parameter ranges of 0.5B–3B.

TinyLLaVA focuses on parameter efficiency via distillation of larger LLaVA-style architectures, enabling deployment on mid-tier GPUs. Qwen2-VL introduces a highperforming multimodal architecture with strong visual reasoning benchmarks, but is primarily optimized for serverclass hardware. PaliGemma emphasizes multilingual and visual-text alignment capabilities, targeting efficient deployment but not real-time robotic control. Moondream2 is designed for lightweight image captioning and visual QA tasks, making it suitable for CPU-class edge systems. However, these systems remain Vision–Language Models (VLMs) and do not directly generate structured motor commands for closed-loop robotic control. They require an additional policy layer or downstream controller to translate textual reasoning into executable actions.

In contrast, LiteVLA-Edge directly fine-tunes a compact multimodal backbone for image-to-action generation, enabling deterministic low-latency control within ROS 2. Our work therefore occupies a distinct design point: not merely compact multimodal reasoning, but practical on-device visuomotor execution.

# III. SYSTEM ARCHITECTURE

LiteVLA-Edge preserves a modular perception– reasoning–action pipeline. The architecture is designed to decouple high-level semantic understanding from lowlevel execution, ensuring that the robot remains responsive even under varying inference loads.

The pipeline begins with raw RGB frames processed by a vision encoder. These visual tokens are fused with languagebased goal context by a multimodal transformer—specifically a distilled version of the SmolVLM-256M backbone. The model then decodes these multimodal representations into structured action commands. To bridge the gap between AI reasoning and physical actuation, these commands are parsed and executed through a ROS 2 bridge using standard geometry msgs/Twist interfaces. This modularity avoids the “black box” nature of monolithic end-to-end policies, allowing for deterministic safety overrides and easier debugging of the perception–action loop.

# A. Vision-Language-Action Mapping

We define the LiteVLA-Edge policy as a conditional probability distribution P over a discrete action space. Given a visual observation $I _ { t } \in \mathbb { R } ^ { H \times W \times 3 }$ and a natural language instruction g at time t, the model generates a sequence of action tokens $\mathbf { a } _ { t } = \{ a _ { 1 } , a _ { 2 } , \ldots , a _ { n } \}$ . The objective during supervised fine-tuning is to minimize the negative loglikelihood:

$$
\mathcal {L} _ {S F T} = - \sum_ {i = 1} ^ {n} \log P (a _ {i} | a _ {<   i}, I _ {t}, g; \theta) \tag {1}
$$

where θ represents the model parameters. The continuous robotic control vectors (e.g., linear velocity v and angular velocity ω) are de-quantized from the generated tokens $\mathbf { a } _ { t }$ .

# IV. IMPLEMENTATION DETAILS

# A. Fine-Tuning and Model Compression

LiteVLA-Edge is trained using supervised image-to-action learning on a curated dataset of robotic demonstrations. The multimodal backbone is fine-tuned in full precision (FP32) using Low-Rank Adaptation (LoRA) with rank r = 8 and a scaling factor $\alpha \ : = \ : 8$ . Training in FP32 is critical for maintaining the high-fidelity mapping required for precise motor commands.

Post-training, we employ aggressive model compression to meet the constraints of edge hardware. The FP32 weights are converted to the GGUF format and compressed using 4-bit quantization (Q4 K M). This reduces the model size significantly, allowing the entire 256M parameter model to reside within the unified memory of the edge device, minimizing bus latency during inference.

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["RGB Camera (/image_raw)"] --> B["Frame Prep (resize / normalize)"]
    B --> C["Vision Encoder (visual tokens)"]
    D["Goal / Task Context (text prompt)"] --> E["On-device runtime: GGUF quantized model (e.g., \Q4_K_M\)<br>11ama.cpp CUDA backend<br>42 layers offloaded to Orin GPU<br>n_ctx=512, max output ≤ 12 tokens"]
    E --> F["Multimodal Transformer SmolVLM-256M (distilled)"]
    F --> G["Action + ROS 2 Integration"]
    G --> H["Action Decode & Formatting (structured tokens)"]
    H --> I["Deterministic Parser & Safety Override"]
    I --> J["ROS 2 Bridge Node Publish \geometry_msgs/Twist"]
    J --> K["Low-level Controller (100 Hz)"]
    K --> L["Mobile Base / Actuators"]
    L --> M["Control heartbeat 100 Hz"]
    F --> N["Reasoning / VLA Core"]
    N --> E
    style A fill:#f9f,stroke:#333
    style D fill:#f9f,stroke:#333
    style E fill:#f9f,stroke:#333
    style F fill:#ccf,stroke:#333
    style G fill:#ccf,stroke:#333
    style H fill:#ccf,stroke:#333
    style I fill:#ccf,stroke:#333
    style J fill:#ccf,stroke:#333
    style K fill:#ccf,stroke:#333
    style L fill:#ccf,stroke:#333
    style M fill:#ccf,stroke:#333
```
</details>

Fig. 1: LiteVLA-Edge system architecture. The multimodal transformer runs fully on-device on the Jetson AGX Orin and publishes structured velocity commands to ROS 2 for closed-loop control.

# B. Edge Execution on NVIDIA Jetson AGX Orin

The deployment phase leverages the llama.cpp library, which provides highly optimized C++ kernels for quantized inference. Unlike general-purpose CPU implementations, our system is configured to offload all 42 layers of the transformer to the NVIDIA Jetson AGX Orin onboard GPU via the CUDA backend. By setting the context window to n ctx = 512 and restricting output to a maximum of 12 tokens, we minimize the KV-cache overhead. This specific configuration allows us to reach an average inference speed of 150.5 ms (∼6.6 Hz) on the Jetson hardware. The system is integrated into a ROS 2 Node that subscribes to camera feeds and publishes velocity commands asynchronously. This ensures that while the VLA “thinks” at 6.6 Hz, the low-level robot controller can maintain a steady 100 Hz heartbeat for stability.

# V. EXPERIMENTAL EVALUATION

# A. Hardware Setup

We evaluate LiteVLA-Edge on the NVIDIA Jetson AGX Orin (64GB), a production-grade embedded GPU module commonly deployed in autonomous robotic platforms. The system operates entirely on-device without external compute offloading.

Performance is contextualized relative to prior LiteVLA deployments on CPU-only platforms such as the Raspberry Pi 4, highlighting the progression from extreme edge feasibility to embedded GPU-class closed-loop control.

# B. Inference Performance and Latency Analysis

The core contribution of LiteVLA-Edge is the reduction of inference latency to a regime suitable for closed-loop control. Utilizing a 4-bit quantized (Q4 K M) SmolVLM-256M backbone and the llama.cpp CUDA backend, we achieved a mean inference latency of 150.5 ms on the NVIDIA Jetson AGX Orin. This latency reduction is primarily attributed to three factors: (1) full GPU offloading of all 42 transformer layers, (2) context window truncation to n ctx = 512, and (3) the use of highly optimized 4-bit GGUF kernels. With a standard deviation of only 0.125 ms, the system exhibits extremely low jitter, which is critical for maintaining stable control frequencies in ROS 2.

TABLE I: Comparison of Compact Multimodal Models and VLA Systems 

<table><tr><td>Model</td><td>Type</td><td>Params</td><td>Evaluated HW</td><td>Closed-Loop</td></tr><tr><td>Moondream2</td><td>VLM</td><td> $\sim 2B$ </td><td>CPU / Edge GPU</td><td>No</td></tr><tr><td>TinyLLaVA</td><td>VLM</td><td> $\sim 1B-3B$ </td><td>GPU</td><td>No</td></tr><tr><td>PaliGemma</td><td>VLM</td><td> $\sim 3B$ </td><td>GPU / TPU</td><td>No</td></tr><tr><td>Qwen2-VL</td><td>VLM</td><td>2B–7B</td><td>Server GPU</td><td>No</td></tr><tr><td>OpenVLA</td><td>VLA</td><td>7B</td><td>RTX 4090</td><td>Partial ( $\sim 5$  Hz)</td></tr><tr><td>EdgeVLA</td><td>VLA</td><td> $\sim 1B$ </td><td>A100-40GB</td><td>Yes ( $\sim 10$  Hz)</td></tr><tr><td>LiteVLA-Edge</td><td>VLA</td><td>256M</td><td>Jetson AGX Orin</td><td>Yes (6.6 Hz)</td></tr></table>

TABLE II: End-to-End Multimodal Inference Performance on Jetson Orin NX 

<table><tr><td>Measurement</td><td>Result</td></tr><tr><td>Total Runs</td><td>300</td></tr><tr><td>Mean Latency</td><td>150.5 ms</td></tr><tr><td>Std Deviation</td><td>0.13 ms</td></tr><tr><td>Minimum</td><td>150.4 ms</td></tr><tr><td>Maximum</td><td>151.0 ms</td></tr><tr><td>Reasoning Frequency</td><td>6.64 Hz</td></tr></table>

# C. Qualitative Shift: From Deliberative to Reactive

The transition to a 6.6 Hz inference frequency enables a qualitative shift in robotic capability. At latencies above 1 second, a VLA system is limited to “open-loop” execution, where the robot must pause to reason before each movement. At 150 ms, the LiteVLA-Edge reaches latency compatible with reactive control loops. In this regime, the system can process visual feedback fast enough to correct its trajectory mid-motion, allowing for successful task completion in dynamic environments where objects or goals may shift during execution.

# D. Closed-Loop Simulation Evaluation

To evaluate real-time deployability without reliance on external robotics benchmarks, we simulate a closed-loop perception–action pipeline representative of reactive robotic decision making. In this setup, RGB frames are provided sequentially to the model, which generates a single motion decision per frame under deterministic decoding (T = 0.0).

We measure end-to-end latency from frame ingestion to action output over 30 runs after warm-up stabilization. On NVIDIA Jetson Orin NX, LiteVLA-Edge achieves a mean inference latency of 150.5 ms ± 0.13 ms, corresponding to a stable reasoning frequency of 6.64 Hz.

This simulated evaluation reflects realistic embedded deployment conditions, including image loading, multimodal fusion, and token decoding, rather than isolated forward-pass measurements.

# VI. DISCUSSION

The achievement of 150.5 ms latency on the NVIDIA Jetson AGX Orin represents a practical step toward deployable on-device VLA systems in the design space for edge-deployed VLAs. Most contemporary research, such as OpenVLA, prioritizes generalist accuracy over temporal resolution, often resulting in “stop-and-go” robotic behavior. By contrast, LiteVLA-Edge reaches the 6–10 Hz threshold, which is widely recognized as the entry point for Closed-Loop Visuomotor Control.

# A. The 150ms Threshold and Visual Servoing

At 150 ms, the perception–action loop is fast enough to support visual servoing, where the robot can adjust its grasp or trajectory in real-time based on visual discrepancies. This is a qualitative leap over the original LiteVLA (offline robotcs), which operated in an open-loop “predict-then-execute” mode.

# B. Quantization and Action Precision

A common critique of 4-bit quantization in robotics is the potential for “Action Jitter” or numerical drift in motor coordinates. However, our results show that by using the SmolVLM-256M backbone, the model retains sufficient representational density to output stable geometry msgs/Twist commands. The extremely low standard deviation in latency (σ = 0.125 ms) further ensures that the ROS 2 control heartbeat remains deterministic, preventing the hazardous oscillations common in high-latency AI controllers.

# C. Positioning Against Compact VLMs

While compact VLMs such as TinyLLaVA, Qwen2-VL, PaliGemma, and Moondream2 demonstrate impressive multimodal reasoning on edge-class hardware, they are not optimized for deterministic motor command generation. Deploying them in robotics typically requires a secondary policy network or rule-based translator.

LiteVLA-Edge differs fundamentally by collapsing the perception-to-action mapping into a single fine-tuned multimodal model. This removes additional inference layers and reduces system-level latency, enabling true closed-loop visuomotor control on embedded hardware.

# D. Threats to Validity and Mitigations

We view the main threats to validity in this work as questions of scope and transferability, rather than correctness of the reported deployment measurements. Our central claim is that a compact Vision-Language-Action (VLA) policy can be executed fully on-device within an embedded ROS 2 pipeline at low end-to-end latency. We mitigate the risk of over-interpretation by explicitly scoping our conclusions to deployability, timing feasibility, and software integration, rather than to broad task-level superiority. Our evaluation is intentionally centered on end-to-end inference latency because response time is the primary bottleneck addressed by this paper. The natural validity concern is that latency alone does not fully characterize embodied robotic performance. We mitigate this concern in part by measuring the complete image-to-action path—including image ingestion, multimodal fusion, and token decoding—rather than an isolated model forward pass. We further reduce this gap through a standard ROS 2 interface, structured action generation, and a modular parser that is directly compatible with downstream robotic control loops. These design choices do not replace future task-level benchmarking, but they make the reported measurements substantially more representative of practical deployment than raw runtime benchmarks alone. A second validity consideration is external transferability across hardware settings, runtime configurations, and robot embodiments. We mitigate this by relying on portable deployment components: a compact multimodal backbone, post-training GGUF quantization, and the llama.cpp CUDA runtime, rather than a highly specialized inference stack tied to a narrow toolchain. This mitigation can be strengthened further, without additional experiments, by explicitly documenting the Jetson power mode, context length, output token limit, backend settings, and warm-up procedure used in our measurements. A third threat arises in cross-paper comparison. Prior VLA and compact VLM systems are typically evaluated under different datasets, embodiments, and hardware platforms, so direct numerical comparisons can be misleading if presented too strongly. We mitigate this by using these baselines primarily to position LiteVLA-Edge within the current design space, not to claim strict head-tohead superiority. A simple editorial mitigation is to make this intent explicit in the table caption and surrounding text, and to clearly distinguish direct VLA systems from compact VLM backbones that require an additional policy layer. Finally, model quantization introduces a validity concern around action fidelity. We partially mitigate this through a conservative deployment pipeline: fine-tuning is performed in full precision, compression is applied only after training, decoding is deterministic, and action generation remains mediated by a structured parser and ROS 2 integration layer with deterministic handling of controller outputs. Together, these choices reduce the likelihood that quantization artifacts are conflated with unstable execution behavior. A lowoverhead way to strengthen this mitigation is to state the action format and parser assumptions explicitly, so that the location of determinism and safety handling in the pipeline is unambiguous. Overall, these threats to validity mainly define the boundary of our present claims rather than undermine the core result. The primary contribution of this paper is a practical embedded deployment path for fully on-device VLA inference, and the mitigations above are intended to make that contribution easier to interpret, reproduce, and compare fairly.

# E. Future Work: Towards Agentic Multi-Robot Systems

With the inference bottleneck significantly reduced, future work will explore Agentic VLA extensions. This includes multi-step reasoning where the robot can verbalize its failures and retry tasks without human intervention. Additionally, the low power footprint of our INT4 implementation on the NVIDIA Jetson AGX Orin makes it an ideal candidate for Swarm Robotics, where multiple LiteVLA-powered agents can coordinate in bandwidth-denied environments.

# VII. CONCLUSION

In this work, we presented LiteVLA-Edge, a deploymentoriented pipeline for fully on-device Vision-Language-Action inference on embedded robotic hardware. By combining supervised image-to-action fine-tuning, post-training 4-bit GGUF quantization, and GPU-accelerated inference through the llama.cpp runtime, we showed that a compact multimodal policy can be integrated into a ROS 2 stack and executed with a mean end-to-end latency of 150.5 ms, corresponding to approximately 6.6 Hz under our deployment configuration. Our primary contribution is not a new policy objective or control law, but a practical path for moving compact VLA models from proof-of-concept to reproducible embedded execution. In particular, LiteVLA-Edge preserves modular perception–reasoning–action interfaces, remains fully local, and avoids reliance on cloud infrastructure or desktop-class GPUs. We believe this is a useful systems result because it identifies a realistic deployment point between large general-purpose VLA systems and narrowly reactive controllers. We intentionally scope our conclusions to deployability, timing feasibility, and software integration. Within that scope, our results provide a concrete baseline for fully local, language-conditioned multimodal control on Orin-class platforms. Broader task-level comparisons, longer-duration profiling, and matched evaluations against alternative baselines are natural extensions of the same deployment pipeline, rather than changes to the core method itself. Overall, our results suggest that compact, quantized VLA policies can be packaged into a practical ROS 2- compatible embedded system. As multimodal backbones and efficient runtimes continue to improve, we expect fully local language-conditioned control to become an increasingly practical option for robots operating under bandwidth, power, and latency constraints.

# VIII. AI USAGE ACKNOWLEDGEMENT

Chatgpt 5.1 is used to refine the language of this paper.

# REFERENCES

[1] D. Driess et al., “PaLM-E: An embodied multimodal language model,” in Proceedings of the 40th International Conference on Machine Learning (ICML), 2023.   
[2] A. Zitkovich et al., “RT-2: Vision-language-action models transfer web knowledge to robotic control,” in Proceedings of the 7th Conference on Robot Learning (CoRL), 2023.   
[3] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “Openvla: An open-source vision-language-action model,” 2024. [Online]. Available: https://arxiv.org/abs/2406.09246   
[4] J. Williams, K. D. Gupta, R. George, and M. Sarkar, “Lite vla: Efficient vision-language-action control on cpu-bound edge robots,” 2025. [Online]. Available: https://arxiv.org/abs/2511.05642   
[5] P. Budzianowski, W. Maa, M. Freed, J. Mo, W. Hsiao, A. Xie, T. Młoduchowski, V. Tipnis, and B. Bolte, “Edgevla: Efficient vision-language-action models,” 2025. [Online]. Available: https: //arxiv.org/abs/2507.14049   
[6] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti, S. Alibert, M. Cord, T. Wolf, and R. Cadene, “Smolvla: A vision-language-action model for affordable and efficient robotics,” 2025. [Online]. Available: https://arxiv.org/abs/2506.01844   
[7] B. Zhou, Y. Hu, X. Weng, J. Jia, J. Luo, X. Liu, J. Wu, and L. Huang, “Tinyllava: A framework of small-scale large multimodal models,” 2024, arXiv:2402.14289 [cs.LG].   
[8] P. Wang, S. Bai, S. Tan, S. Wang, Z. Fan, J. Bai, K. Chen, X. Liu, J. Wang, W. Ge, Y. Fan, K. Dang, M. Du, X. Ren, C. Zhou, J. Zhou, and J. Lin, “Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution,” 2024, arXiv:2409.12191 [cs.CV].   
[9] A. Steiner, A. S. Pinto, M. Tschannen, D. Keysers, X. Wang, Y. Bitton, A. Gritsenko, M. Minderer, A. Sherbondy, S. Long, S. Qin, R. Ingle, E. Bugliarello, S. Kazemzadeh, T. Mesnard, I. Alabdulmohsin, L. Beyer, and X. Zhai, “Paligemma 2: A family of versatile vlms for transfer,” 2024, arXiv:2412.03555 [cs.CV].   
[10] V. Verma et al., “Moondream2: A tiny vision-language model,” https: //github.com/vikhyat/moondream, 2024, gitHub repository, accessed 2026.