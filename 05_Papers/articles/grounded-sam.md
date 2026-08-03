# Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks

International Digital Economy Academy (IDEA) & Community Code & Demo: https://github.com/IDEA-Research/Grounded-Segment-Anything

G-DINO: Open-Vocab. Det

SAM: Promptable Seg

Grounded SAM: Open-Vocab. Det & Seg

“There are two dogs playing with a stick on the beach”

“armchair, blanket, lamp, carpet, dog, floor, furniture, picture, pillow, plant, room”

![[99_Attachments/papers/images/grounded-sam/5d922a1b4b2f754598e5af1ceff700d50afa1c4cac9713a58e8e24a3cc4c9d46.jpg]]  
Grounded SAM + Stable-Diffusion: Highly Controllable Image Editing  
Grounded SAM + OSX: Promptable Human Motion Analysis

Figure 1: Grounded SAM can simultaneously detect and segment corresponding regions within images based on arbitrary text inputs provided by users. And it can seamlessly integrate with other Open-World models to accomplish more intricate visual tasks

## Abstract

We introduce Grounded SAM, which uses Grounding DINO [38] as an open-set object detector to combine with the segment anything model (SAM) [25]. This integration enables the detection and segmentation of any regions based on arbitrary text inputs and opens a door to connecting vari ous vision models. As shown in Fig. 1, a wide range of vision tasks can be achieved by using the versatile Grounded SAM pipeline. For example, an automatic annotation pipeline based solely on input images can be realized by incorporating models such as BLIP [31] and Recognize Anything [83]. Additionally, incorporating Stable-Diffusion [52] allows for controllable image editing, while the integration of OSX [33] facilitates promptable 3D human motion analysis. Grounded SAM also shows superior performance on open-vocabulary benchmarks, achieving 48.7 mean AP on SegInW (Segmentation in the wild) zero-shot benchmark with the combination of Grounding DINO-Base and SAM-Huge models.

## 1. Introduction

Visual perception and understanding tasks in open-world scenarios are crucial for the advancement of applications such as autonomous driving, robotic navigation, and intelligent security surveillance. These applications demand robust and versatile visual perception models capable of interpreting and interacting with open-world environments.

Currently, there are three primary methodologies to address the challenges in open-world visual perception. First, the Unified Model approach involves training models like UNINEXT [66] and OFA [59] on multiple datasets to support various vision tasks. This method also includes training large language models on different visual questionanswering datasets to unify tasks, like LLaVA [34], Instruct-BLIP [12], Qwen-VL [3] and other MLLMs [60, 40, 80]. However, a significant limitation of such an approach is its limited scope in data, especially in complex tasks like openset segmentation. Second, the LLM as Controller method attempts to bridge vision experts with language models. Examples include HuggingGPT [55], Visual ChatGPT [62], and LLaVA-Plus [35]. These approaches leverage the linguistic comprehension capabilities of large language models to direct various visual tasks. However, this method is heavily reliant on the functionalities and limitations of large language models. Third, the Ensemble Foundation Models approach seeks to accomplish open-world tasks in complex scenarios by collaboratively integrating expert models designed for specific contexts. This approach offers flexibility by combining the strengths of various specialized models.

Although there have been advances in addressing openworld tasks through these methodologies, a robust pipeline capable of supporting complex and fundamental open-world tasks such as open-set segmentation is still lacking in the market. Grounded SAM takes an innovative approach from the perspective of the Ensemble Foundation Models approach, pioneering the integration of open-set detector models, such as Grounding DINO [38], and promptable segmentation models like SAM [25]. It effectively tackles the open-set segmentation challenge by dividing it into two main components: open-set detection, and promptable segmentation. Based on this approach, Grounded SAM offers a powerful and comprehensive platform that further facilitates an efficient fusion of different expert models to tackle more intricate open-world tasks.

Building upon Grounded SAM as a foundation and leveraging its robust open-set segmentation capabilities, we can easily incorporating additional open-world mod els. For instance, when combined with Recognize Anything (RAM) [83], the RAM-Grounded-SAM model can automat ically identify and segment things or objects within images without the need for any textual input, thus facilitating automatic image annotation tasks. Similar automatic image annotation capabilities can also be achieved through integra tion with BLIP [31]. Furthermore, Grounded SAM, when coupled with the inpainting capability of Stable Diffusion, as exemplified by the Grounded-SAM-SD model, can execute highly precise image editing tasks. We will provide a more detailed discussion of Grounded SAM and its augmented capabilities through the incorporation of additional open-world models in Section 3.

## 2. Related Work

## 2.1. Task-specific Vision Models

In the field of computer vision, significant advancements have been made across a variety of tasks, including image recognition [47, 31, 18, 83, 17], generic object detection [49, 87, 43, 27, 77, 36, 19, 38, 51, 50, 20, 30], generic image segmentation [9, 8, 26, 29, 78, 88, 79, 25, 79, 16, 28], referring object detection and segmentation [41, 37, 86], object tracking [67, 84], image generation [75, 54, 48, 45, 23, 14, 52, 22, 82, 44], image editing [42, 1, 2, 53, 21], human-centric perception and under standing [72, 71, 73, 70, 69, 4, 33, 74], and human-centric motion generation [39, 6, 32, 61, 5]. However, despite these advancements, current models are mostly task-specific and usually fall short in addressing a broader range of tasks.

## 2.2. Unified Models

Unified models have been developed to address multi ple tasks. In the language field, Large language models (LLMs) such as GPT-3 [13], LaMDA [57], and PaLM [11] are examples of general-purpose unified models, which han dle language tasks through an auto-regressive and genera tive approach. Unlike language tasks that rely on a unified and structured token representation, vision tasks encompass many data formats, including pixel, spatial (e.g., box, key point), temporal, and others. Recent works have attempted to develop unified vision models from two perspectives to accommodate these diverse modalities. First, some models aim to unify various vision modalities into a single one. For instance, Pix2Seq [7] and OFA [59] attempt to merge spatial modalities such as box coordinates into language. Second, some models seek a unified model compatible with different modality outputs. UNINEXT [66] is an example that supports different instance-level task outputs. Although these unified vision models are advancing the progress of general intelligence, existing models can only handle a limited number of tasks and often fall short of task-specific models in performance.

## 2.3. Model Assembly with a Controller System

Orthogonal to our work, Visual ChatGPT [62] and HuggingGPT [55] propose to leverage LLMs to control different AI models for solving different tasks. Compared with these models, the foundation model assembling method does not employ an LLM as the controller, which makes the whole pipeline more efficient and flexible. We show that complex tasks can be decoupled, and step-by-step visual reasoning can be accomplished in a training-free model assembly manner.

## 3. Grounded SAM Playground

In this chapter, utilizing Grounded SAM as a foundation, we demonstrate our method of amalgamating expert models from various domains to facilitate the accomplishment of more comprehensive visual tasks.

## 3.1. Preliminary

We discuss the basic components of Grounded SAM and other domain expert models here.

Segment Anything Model (SAM) [25] is an open-world segmentation model that can "cut out" any object in any image with proper prompts, like points, boxes, or text. It has been trained on over 11 million images and 1.1 billion masks. Despite of its strong zero-shot performance, the model cannot identify the masked objects based an arbitrary text input and normally requires point or box prompts to run.

Grounding DINO [38] is an open-set object detector that can detect any objects with respect to an arbitrary free-form text prompt. The model was trained on over 10 million images, including detection data, visual grounding data, and image-text pairs. It has a strong zero-shot detection performance. However, the model needs text as inputs and can only detect boxes with corresponding phrases.

OSX [33] is the state-of-the-art model for expressive whole-body mesh recovery, which aims to estimate the 3D human body poses, hand gestures, and facial expressions jointly from monocular images. It needs first to detect human boxes, crop and resize the human boxes, and then conduct single-person mesh recovery.

BLIP [31] is a vision-language model that unifies visionlanguage understanding and generation tasks. We use the image caption model of BLIP in our experiments. The caption model can generate descriptions given any image. However, the model cannot perform object-level tasks, like detecting or segmenting objects.

Recognize Anything Model (RAM) [83] is a strong image tagging model that can recognize any common categories of high accuracy for an input image. However, RAM can only generate tags but cannot generate precise boxes and masks for the recognized categories.

Stable Diffusion [52] is an image generation model that samples images from the learned distribution of training data. Its most widely used application is generating images with text prompts. We use its inpainting variant in our experiment. Despite of its awesome generation results, the model cannot perform perception or understanding tasks.

ChatGPT & GPT-4 [15, 46] are large language models developed using the GPT (Generative Pre-trained Transformer) architecture, which is used for building conversational AI agents. It is trained on massive amounts of text data and can generate human-like responses to user input. The model can understand the context of the conversation and generate appropriate responses that are often indistinguishable from those of a human.

## 3.2. Grounded SAM: Open-Vocabulary Detection and Segmentation

It is highly challenging to determining masks in images corresponding to regions mentioned in any user-provided text and thereby enabling finer-grained image understanding tasks like open-set segmentation. This is primarily due to the limited availability of high-quality data for segmentation in the wild tasks, which presents a challenge for the model to accomplish precise open-set segmentation under conditions characterized by data scarcity. In contrast, open set detection tasks are more tractable, primarily due to the following two reasons. First, the annotation cost of detec tion data is relatively lower compared to segmentation tasks, enabling the collection of more higher-quality annotated data. Second, open-set detection only requires identifying the corresponding object coordinates on the images based on the given text without the need for precise pixel-level object masks. Similarly, the prediction of the correspond ing object mask, conditioned on a box and benefiting from the prior knowledge of the box’s location, is more efficient than directly predicting the region mask based on a text. This approach has been validated in previous works such as OpenSeeD [79], and the substantial issue of data scarcity can be largely addressed by utilizing the SAM-1B dataset developed in SAM [25].

Consequently, inspired by prior successful works such as Grounded Pre-training [81, 38] and SAM [25], we aim to address complex segmentation in the wild tasks by combining the strong open-set foundation models. Given an input image and a text prompt, we first employ Grounding DINO to generate precise boxes for objects or regions within the image by leveraging the textual information as condition. Subsequently, the annotated boxes obtained through Grounding DINO serve as the box prompts for SAM to generate precise mask annotations. By leveraging the capabilities of these two robust expert models, the open-set detection and segmentation tasks can be more effortlessly accomplished. As illustrated in Fig. 2, Grounded SAM can accurately detect and segment text based on user input in both conventional and long-tail scenarios.

![[99_Attachments/papers/images/grounded-sam/f28660ba8708e85407d9c360bd06046d7d188a7dce4e41772837856e8e16dc4a.jpg]]  
Figure 2: Grounded-SAM effectively detects and segments objects according to various user inputs. Its effectiveness is not limited to common cases but also includes long-tail object categories (like "Zale Horrida", and "Gazania Linearis", e.g.). Some of the demo images were sampled from the V3Det [58] dataset. We greatly appreciate their excellent work.

## 3.3. RAM-Grounded-SAM: Automatic Dense Image Annotation

The automatic image annotation system has numerous practical applications, such as enhancing the efficiency of manual annotation of data, reducing the cost of human annotation, or providing real-time scene annotation and understanding in autonomous driving to enhance driving safety. In the framework of Grounded SAM, it leverages the capabilities of Grounding DINO. Users have the flexibility to input arbitrary categories or captions, which are then automatically matched with entities within the images. Building upon this foundation, we can employ either an image-caption model (like BLIP [31] and Tag2Text [18]) or an image tagging model (like RAM [83]), using their output results (captions or tags) as inputs to Grounded SAM and generating precise box and mask for each instance. This enables the automatic labeling of an entire image, achieving an automated label ing system. As depicted in Fig. 3, RAM-Grounded-SAM exhibits the capability to automatically perform category prediction and provide dense annotations for input images across various scenarios. This significantly reduces the an notation cost and greatly enhances the flexibility of image annotation.

“Goggles. Jacket. Man. Showcase. Stand, Stool. Suit, Sunglasses. Display.”

“Boat. Bridge. Building. City. City view. River. Skyline. Skyscraper. Water.”

“Airliner. Plane. Boat, Cargo. Cargo ship. Container. Fly. Harbor. Sea.”

“Bend. Smartphone. Flower. Garden. Person. Rose. Sweatshirt. Woman.”

![[99_Attachments/papers/images/grounded-sam/7168c02013fe27338afc61e1dea3d021e1c2ca02071f35653cdf32c379e24bac.jpg]]  
Figure 3: RAM-Grounded-SAM combines the robust tagging capabilities of the RAM [83] with the open-set detection and segmentation abilities of Grounded SAM, which enables automatic dense image annotation with only image input (the demo images are sampled from the SA-1B [25] dataset).

## 3.4. Grounded-SAM-SD: Highly Accurate and Controllable Image Editing

By integrating the powerful text-to-image capability of image generation models with Grounded SAM, we can establish a comprehensive framework that enables the creation of a robust data synthesis factory, supporting fine-grained operations at the part-level, instance-level, and semantic-level. As shown in Fig. 4, users can obtain precise masks through interactive methods such as clicking or drawing bounding boxes within this pipeline. Moreover, users can leverage the capability of grounding, combined with text prompts, to automatically locate corresponding regions of interest. Building upon this foundation, with the additional capability of an image generation model, we can achieve highly precise and controlled image manipulation, including modifying the image representation, replacing objects, removing the corresponding regions, etc. In downstream scenarios where data scarcity arises, our system can generate new data, addressing the data requirements for the training of models.

## 3.5. Grounded-SAM-OSX: Promptable Human Motion Analysis

Previous expressive whole-body mesh recovery first detects all (instance-agnostic) human boxes and then conducts the single-person mesh recovery. In many real-world appli cations, we need to specify the target person to be detected and analyzed. However, existing human detectors can not distinguish different instances (e.g., specify to analyze "a person with pink clothes"), making fine-grained human motion analysis challenging. As shown in Fig. 5, we can integrate the Grounded SAM and OSX [33] models to achieve a novel promptable (instance-specific) whole-body human detection and mesh recovery, thereby realizing a promptable human motion analysis system. Specifically, given an image and a prompt to refer to a specific person, we first use Grounded SAM to generate a precise specific human box. Then, we use OSX to estimate an instance-specific human mesh to complete the process.

“A man with a sunglasses”

Grounded-SAM-SD: Highly Controllable Image Editing

![[99_Attachments/papers/images/grounded-sam/33a4bd7043b268d68c1c8940ef4b91013fc368d37b8493e88cf21c2c4f879402.jpg]]  
“concept art digital painting of an elven castle, inspired by lord of the rings, highly detailed, 8k”  
“Cat eye with galaxy in it, highly detailed, 8k”

Figure 4: Grounded-SAM-SD combines the open-set ability of Grounded SAM with inpainting  
![[99_Attachments/papers/images/grounded-sam/adae50f4eec90d5dbc7449a13839c18fd7793d6e0b816d6c74459a26a47ff063.jpg]]  
Figure 5: Grounded-SAM-OSX merges the text-promptable capability of Grounded SAM with the whole body mesh recovery ability of OSX [33], facilitating a precise human motion analysis system.

## 3.6. More Extensions for Grounded SAM

In addition to the aforementioned primary applications, Grounded SAM can further expand its scope of utilization by integrating more models. For instance, in the data labeling process, Grounded SAM can collaborate with the faster inference SAM models, such as FastSAM [85], MobileSAM [76],

Light-HQ-SAM [24], and EfficientSAM [63]. This collaboration can significantly reduce the overall inference time and expedite the labeling workflow. Grounded SAM can also leverage the HQ-SAM [24] model, which is capable of generating higher-quality masks, to enhance the quality of annotations. In the realm of image editing, Grounded SAM can also synergize with the newly proposed generative models such as Stable-Diffusion-XL [52] to achieve higherquality image editing. Furthermore, it can be integrated with models like LaMa [56] and PaintByExample [68] to achieve precise image erasure and customized image editing. Grounded SAM can also integrate with tracking models such as DEVA [10] to perform object tracking based on specific text prompts.

Table 1: Zero-shot benchmarking results of Grounded-SAM in SGinW. The best and second-best results are highlighted in bold and underlined, respectively. \* means the results were tested by the SAM-HQ [24] team. We are immensely thankful for their assistance in conducting these tests and highly appreciate their work.

<table><tr><td>Method</td><td>mean SGinW</td><td>Elephants</td><td>Hand-Metal</td><td>Watermelon</td><td>House-Parts</td><td>HouseHold-Items</td><td>Strawberry</td><td>Fruits</td><td>Nutterfly-Squirrel</td><td>Hand</td><td>Garbage</td><td>Chicken</td><td>Rail</td><td>Airplane-Parts</td><td>Brain-Tumor</td><td>Poles</td><td>Electric-Shaver</td><td>Bottles</td><td>Toolkits</td><td>Trash</td><td>Salmon-Fillet</td><td>Puppies</td><td>Tablets</td><td>Phones</td><td>Cows</td><td>Ginger-Garlic</td></tr><tr><td>X-Decoder-T [88]</td><td>22.6</td><td>65.6</td><td>22.4</td><td>16.2</td><td>5.5</td><td>50.6</td><td>41.6</td><td>66.5</td><td>62.1</td><td>0.6</td><td>28.7</td><td>12.0</td><td>0.7</td><td>10.5</td><td>1.1</td><td>3.6</td><td>1.2</td><td>19.0</td><td>9.5</td><td>19.3</td><td>15.0</td><td>48.9</td><td>15.2</td><td>29.9</td><td>12.0</td><td>7.9</td></tr><tr><td>X-Decoder-L-IN22K</td><td>26.6</td><td>63.9</td><td>20.3</td><td>13.5</td><td>4.9</td><td>50.5</td><td>74.4</td><td>79.1</td><td>58.8</td><td>0.0</td><td>24.3</td><td>3.5</td><td>1.3</td><td>12.3</td><td>0.5</td><td>13.4</td><td>18.8</td><td>43.2</td><td>14.6</td><td>20.1</td><td>12.3</td><td>57.3</td><td>6.9</td><td>43.4</td><td>12.3</td><td>15.6</td></tr><tr><td>X-Decoder-B</td><td>27.7</td><td>68.0</td><td>18.5</td><td>13.0</td><td>6.7</td><td>51.7</td><td>81.6</td><td>76.7</td><td>53.1</td><td>20.6</td><td>30.2</td><td>13.6</td><td>0.8</td><td>13.0</td><td>0.3</td><td>5.6</td><td>4.2</td><td>45.9</td><td>13.9</td><td>27.3</td><td>18.2</td><td>55.4</td><td>8.0</td><td>8.9</td><td>36.8</td><td>19.4</td></tr><tr><td>X-Decoder-L</td><td>32.2</td><td>66.0</td><td>42.1</td><td>13.8</td><td>7.0</td><td>53.0</td><td>67.1</td><td>79.2</td><td>68.4</td><td>75.9</td><td>33.0</td><td>8.6</td><td>2.3</td><td>13.1</td><td>2.2</td><td>20.1</td><td>7.5</td><td>42.1</td><td>9.9</td><td>22.3</td><td>19.0</td><td>59.0</td><td>22.5</td><td>15.6</td><td>44.9</td><td>11.6</td></tr><tr><td>OpenSeeD-L [79]</td><td>36.7</td><td>72.9</td><td>38.7</td><td>52.3</td><td>1.8</td><td>50.0</td><td>82.8</td><td>76.4</td><td>40.0</td><td>92.7</td><td>16.9</td><td>82.9</td><td>1.8</td><td>13.0</td><td>2.1</td><td>4.6</td><td>4.7</td><td>39.7</td><td>15.4</td><td>15.3</td><td>15.0</td><td>74.6</td><td>47.4</td><td>7.6</td><td>40.9</td><td>13.6</td></tr><tr><td>ODISE-L [64]</td><td>38.7</td><td>74.9</td><td>51.4</td><td>37.5</td><td>9.3</td><td>60.4</td><td>79.9</td><td>81.3</td><td>71.9</td><td>41.4</td><td>39.8</td><td>84.1</td><td>2.8</td><td>15.8</td><td>2.9</td><td>0.4</td><td>18.3</td><td>37.7</td><td>15.0</td><td>28.6</td><td>30.2</td><td>65.4</td><td>9.1</td><td>43.8</td><td>41.6</td><td>23.0</td></tr><tr><td>SAN-CLIP-ViT-L [65]</td><td>41.4</td><td>67.4</td><td>62.9</td><td>43.5</td><td>9.0</td><td>60.1</td><td>81.8</td><td>77.4</td><td>82.2</td><td>88.8</td><td>46.5</td><td>69.2</td><td>2.9</td><td>13.2</td><td>2.6</td><td>1.8</td><td>11.4</td><td>48.8</td><td>31.2</td><td>41.4</td><td>20.0</td><td>60.1</td><td>35.1</td><td>10.4</td><td>44.0</td><td>23.3</td></tr><tr><td>UNINEXT-H [66]</td><td>42.1</td><td>72.1</td><td>57.0</td><td>56.3</td><td>0.0</td><td>54.0</td><td>80.7</td><td>81.1</td><td>84.1</td><td>93.7</td><td>16.9</td><td>75.2</td><td>0.0</td><td>15.1</td><td>2.6</td><td>13.4</td><td>71.2</td><td>46.1</td><td>10.1</td><td>10.8</td><td>44.4</td><td>64.6</td><td>21.0</td><td>6.1</td><td>52.7</td><td>23.7</td></tr><tr><td>Grounded-HQ-SAM (B+H)* [24]</td><td>49.6</td><td>77.5</td><td>81.2</td><td>65.6</td><td>8.5</td><td>60.1</td><td>85.6</td><td>82.3</td><td>77.1</td><td>74.8</td><td>25.0</td><td>84.5</td><td>7.7</td><td>37.6</td><td>12.0</td><td>20.1</td><td>72.1</td><td>66.3</td><td>21.8</td><td>30.0</td><td>42.2</td><td>50.1</td><td>29.7</td><td>35.3</td><td>47.8</td><td>45.6</td></tr><tr><td>Grounded-SAM (B+H)*</td><td>48.7</td><td>77.9</td><td>81.2</td><td>64.2</td><td>8.4</td><td>60.1</td><td>83.5</td><td>82.3</td><td>71.3</td><td>70.0</td><td>24.0</td><td>84.5</td><td>8.7</td><td>37.2</td><td>11.9</td><td>23.3</td><td>71.7</td><td>65.4</td><td>20.8</td><td>30.0</td><td>32.9</td><td>50.1</td><td>29.8</td><td>35.4</td><td>47.5</td><td>45.8</td></tr><tr><td>Grounded-SAM (L+H)</td><td>46.0</td><td>78.6</td><td>75.2</td><td>61.5</td><td>7.2</td><td>35.0</td><td>82.5</td><td>86.9</td><td>70.9</td><td>90.7</td><td>28.2</td><td>84.6</td><td>7.2</td><td>38.4</td><td>10.2</td><td>17.4</td><td>59.7</td><td>43.7</td><td>26.9</td><td>22.4</td><td>27.1</td><td>63.2</td><td>38.6</td><td>3.4</td><td>49.4</td><td>40.0</td></tr></table>

## 4. Effectiveness of Grounded SAM

To validate the effectiveness of Grounded SAM, we evaluate its performance on the Segmentation in the Wild (SGinW) zero-shot benchmark, which comprises 25 zero-shot in-thewild datasets. As demonstrated in Table. 1, the combination of Grounding DINO Base and Large Model with SAM-Huge results in significant performance improvements in the zeroshot settings of SGinW, when compared to previously unified open-set segmentation models such as UNINEXT [66] and OpenSeeD [79]. By incorporating HQ-SAM [24], which is capable of generating masks of higher quality than SAM, Grounded-HQ-SAM achieves even further performance improvement on SGinW.

## 5. Conclusion and Prospects

The strengths of our proposed Grounded SAM and its extensions, which utilize the assembly of diverse expert models to accomplish various vision tasks, can be summarized as follows. First, the capability boundaries of the models can be seamlessly expanded by assembling various expert models. Previously, we could do n tasks with n models. Now, we can do up to 2<sup>n</sup> − 1 tasks with n expert models considering all possible model combinations. We can decouple a complex task into several sub-tasks that are solved by currently available expert models. Second, the model assembling pipeline is more explainable by decomposing a task into several subtasks. We can observe the output of each step to obtain the reasoning process of the final results. Finally, by combining various expert models, we can investigate new areas of research and applications, potentially leading to innovative results and technological advances.

Prospects: A significant prospect of our methodology entails establishing a closed loop between annotation data and model training. Through the combination of expert models, substantial annotation costs can be saved. Moreover, the inclusion of human annotators at different stages facilitates the filtering or fine-tuning of inaccurate model predictions, thereby enhancing the quality of model annotations. The annotated data is then continually utilized to further train and improve the model. Another potential application of our method is to combine with Large Language Models (LLMs). Given our assembled models can do almost any computer vision (CV) tasks with various input and output modalities, especially language, it becomes straightforward for LLMs to invoke our API via language prompts to effectively execute CV tasks. Last but not least, the model can be used to generate new datasets bridging any pairs of modalities, especially when combined with generation models.

## 6. Contributions and Acknowledgments

We would like to express our deepest gratitude to multiple persons from the research community for their substantial support in the Grounded SAM project. We have listed the main participating roles in the Grounded SAM Project below. Within each role, contributions are equal and are listed in a randomized order. Ordering within each role does not indicate the ordering of the contributions.

## Leads

Tianhe Ren, Co-Lead, Grounded SAM & Grounded-SAM-SD pipeline.

Shilong Liu, Co-Lead, Grounded SAM pipeline and online demo.

Ailing Zeng, Co-Lead, Grounded-SAM-OSX pipeline and demo.

Jin Ling, Co-Lead, Grounded-SAM-OSX pipeline and demo.

He Cao, Co-Lead, Grounded-SAM-SD pipeline and Interactive SAM Editing pipeline.

Kunchang Li, Co-Lead, BLIP-Grounded-SAM pipeline and ChatBot.

Jiayu Chen, Co-Lead, Grounded SAM modelscope demo support and code optimization.

Xinyu Huang, Co-Lead, RAM-Grounded-SAM demo support.

Feng Yan, Co-Lead, Grounded SAM with VISAM tracking demo.

Yukang Chen, Co-Lead, 3D-Box via Segment Anything.

## Core Contributors

Zhaoyang Zeng Hao Zhang Feng Li Jie Yang Hongyang Li Qing Jiang Chenxi Whitehouse Zhenxuan Wang Overall Technical Leads Lei Zhang

## References

[1] Omri Avrahami, Ohad Fried, and Dani Lischinski. Blended Latent Diffusion, Jun 2022. 2

[2] Omri Avrahami, Dani Lischinski, and Ohad Fried. Blended Diffusion for Text-driven Editing of Natural Images. In 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), Sep 2022. 2

[3] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou. Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond, 2023. 2

[4] Zhongang Cai, Wanqi Yin, Ailing Zeng, CHEN WEI, SUN Qingping, Yanjun Wang, Hui En Pang, Haiyi Mei, Mingyuan Zhang, Lei Zhang, et al. Smpler-x: Scaling up expressive

human pose and shape estimation. In Thirty-seventh Confer ence on Neural Information Processing Systems Datasets and Benchmarks Track, 2023. 2

[5] Junming Chen, Yunfei Liu, Jianan Wang, Ailing Zeng, Yu Li, and Qifeng Chen. Diffsheg: A diffusion-based approach for real-time speech-driven holistic 3d expression and gesture generation. arXiv preprint arXiv:2401.04747, 2024. 2

[6] Ling-Hao Chen, Jiawei Zhang, Yewen Li, Yiren Pang, Xi aobo Xia, and Tongliang Liu. HumanMAC: Masked Motion Completion for Human Motion Prediction. 2023. 2

[7] Ting Chen, Saurabh Saxena, Lala Li, David J Fleet, and Geoffrey Hinton. Pix2seq: A Language Modeling Framework for Object Detection. arXiv preprint arXiv:2109.10852, 2021. 2

[8] Bowen Cheng, Anwesa Choudhuri, Ishan Misra, Alexander Kirillov, Rohit Girdhar, and Alexander G. Schwing. Mask2Former for Video Instance Segmentation. 2022. 2

[9] Bowen Cheng, Alexander G. Schwing, and Alexander Kirillov. Per-Pixel Classification is Not All You Need for Semantic Segmentation. 2021. 2

[10] Ho Kei Cheng, Seoung Wug Oh, Brian Price, Alexander Schwing, and Joon-Young Lee. Tracking Anything with Decoupled Video Segmentation. In ICCV, 2023. 7

[11] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al. Palm: Scaling language modeling with pathways. arXiv preprint arXiv:2204.02311, 2022. 2

[12] Wenliang Dai, Junnan Li, Dongxu Li, Anthony Meng Huat Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale Fung, and Steven Hoi. InstructBLIP: Towards General-purpose Vision-Language Models with Instruction Tuning, 2023. 2

[13] Luciano Floridi and Massimo Chiriatti. GPT-3: Its nature, scope, limits, and consequences. Minds and Machines, 30:681–694, 2020. 2

[14] Oran Gafni, Adam Polyak, Oron Ashual, Shelly Sheynin, Devi Parikh, and Yaniv Taigman. Make-A-Scene: Scene Based Text-to-Image Generation with Human Priors. 2

[15] Roberto Gozalo-Brizuela and Eduardo C Garrido-Merchan. ChatGPT is not all you need. A State of the Art Review of large Generative AI models. arXiv preprint arXiv:2301.04655, 2023. 3

[16] Jie Hu, Linyan Huang, Tianhe Ren, Shengchuan Zhang, Ron grong Ji, and Liujuan Cao. You Only Segment Once: Towards Real-Time Panoptic Segmentation, 2023. 2

[17] Xinyu Huang, Yi-Jie Huang, Youcai Zhang, Weiwei Tian, Rui Feng, Yuejie Zhang, Yanchun Xie, Yaqian Li, and Lei Zhang. Open-Set Image Tagging with Multi-Grained Text Supervision, 2023. 2

[18] Xinyu Huang, Youcai Zhang, Jinyu Ma, Weiwei Tian, Rui Feng, Yuejie Zhang, Yaqian Li, Yandong Guo, and Lei Zhang. Tag2Text: Guiding Vision-Language Model via Image Tag ging, 2023. 2, 4

[19] Ding Jia, Yuhui Yuan, Haodi He, Xiaopei Wu, Haojun Yu, Weihong Lin, Lei Sun, Chao Zhang, and Han Hu. DETRs with Hybrid Matching. arXiv preprint arXiv:2207.13080, 2022. 2

[20] Qing Jiang, Feng Li, Tianhe Ren, Shilong Liu, Zhaoyang Zeng, Kent Yu, and Lei Zhang. T-Rex: Counting by Visual Prompting, 2023. 2

[21] Xuan Ju, Ailing Zeng, Yuxuan Bian, Shaoteng Liu, and Qiang Xu. Direct inversion: Boosting diffusion-based editing with 3 lines of code. arXiv preprint arXiv:2310.01506, 2023. 2

[22] Xuan Ju, Ailing Zeng, Chenchen Zhao, Jianan Wang, Lei Zhang, and Qiang Xu. HumanSD: A native skeleton-guided diffusion model for human image generation. 2023. 2

[23] Minguk Kang, Jun-Yan Zhu, Richard Zhang, Jaesik Park, Eli Shechtman, Sylvain Paris, Taesung Park, and Postech Postech. Scaling up GANs for Text-to-Image Synthesis. 2

[24] Lei Ke, Mingqiao Ye, Martin Danelljan, Yifan Liu, Yu-Wing Tai, Chi-Keung Tang, and Fisher Yu. Segment Anything in High Quality. arXiv:2306.01567, 2023. 6, 7

[25] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al. Segment Anything. arXiv preprint arXiv:2304.02643, 2023. 1, 2, 3, 5

[26] Feng Li, Qing Jiang, Hao Zhang, Tianhe Ren, Shilong Liu, Xueyan Zou, Huaizhe Xu, Hongyang Li, Chunyuan Li, Jianwei Yang, Lei Zhang, and Jianfeng Gao. Visual In-Context Prompting, 2023. 2

[27] Feng Li, Hao Zhang, Shilong Liu, Jian Guo, Lionel M Ni, and Lei Zhang. DN-DETR: Accelerate DETR Training by Introducing Query DeNoising. In Computer Vision and Pattern Recognition (CVPR), 2022. 2

[28] Feng Li, Hao Zhang, Peize Sun, Xueyan Zou, Shilong Liu, Jianwei Yang, Chunyuan Li, Lei Zhang, and Jianfeng Gao. Semantic-SAM: Segment and Recognize Anything at Any Granularity, 2023. 2

[29] Feng Li, Hao Zhang, Huaizhe xu, Shilong Liu, Lei Zhang, Lionel M. Ni, and Heung-Yeung Shum. Mask DINO: Towards A Unified Transformer-based Framework for Object Detection and Segmentation. In Proceedings of the IEEE conference on computer vision and pattern recognition, 2023. 2

[30] Hongyang Li, Hao Zhang, Zhaoyang Zeng, Shilong Liu, Feng Li, Tianhe Ren, and Lei Zhang. DFA3D: 3D Deformable Attention For 2D-to-3D Feature Lifting. In Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), pages 6684–6693, October 2023. 2

[31] Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation. In International Conference on Machine Learning, pages 12888– 12900. PMLR, 2022. 2, 3, 4

[32] Jing Lin, Ailing Zeng, Shunlin Lu, Yuanhao Cai, Ruimao Zhang, Haoqian Wang, and Lei Zhang. Motion-x: A largescale 3d expressive whole-body human motion dataset. In Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track, 2023. 2

[33] Jing Lin, Ailing Zeng, Haoqian Wang, Lei Zhang, and Yu Li. One-Stage 3D Whole-Body Mesh Recovery with Component Aware Transformer. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2023. 2, 3, 5, 6

[34] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual Instruction Tuning. arXiv preprint arXiv:2304.08485, 2023. 2

[35] Shilong Liu, Hao Cheng, Haotian Liu, Hao Zhang, Feng Li, Tianhe Ren, Xueyan Zou, Jianwei Yang, Hang Su, Jun Zhu, Lei Zhang, Jianfeng Gao, and Chunyuan Li. LLaVA-Plus: Learning to Use Tools for Creating Multimodal Agents, 2023. 2

[36] Shilong Liu, Feng Li, Hao Zhang, Xiao Yang, Xianbiao Qi, Hang Su, Jun Zhu, and Lei Zhang. DAB-DETR: Dynamic Anchor Boxes are Better Queries for DETR. In International Conference on Learning Representations, 2022. 2

[37] Shilong Liu, Yaoyuan Liang, Feng Li, Shijia Huang, Hao Zhang, Hang Su, Jun Zhu, and Lei Zhang. DQ-DETR: Dual Query Detection Transformer for Phrase Extraction and Grounding, 2022. 2

[38] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, et al. Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection. arXiv preprint arXiv:2303.05499, 2023. 1, 2, 3

[39] Shunlin Lu, Ling-Hao Chen, Ailing Zeng, Jing Lin, Ruimao Zhang, Lei Zhang, and Heung-Yeung Shum. Human-TOMATO: Text-aligned Whole-body Motion Generation. arXiv preprint arXiv:2310.12978, 2023. 2

[40] Gen Luo, Yiyi Zhou, Tianhe Ren, Shengxin Chen, Xiaoshuai Sun, and Rongrong Ji. Cheap and Quick: Efficient Vision-Language Instruction Tuning for Large Language Models, 2023. 2

[41] Gen Luo, Yiyi Zhou, Xiaoshuai Sun, Liujuan Cao, Chenglin Wu, Cheng Deng, and Rongrong Ji. Multi-task Collaborative Network for Joint Referring Expression Comprehension and Segmentation, 2020. 2

[42] Chenlin Meng, Yang Song, Jiaming Song, Jiajun Wu, Jun Yan Zhu, and Stefano Ermon. SDEdit: Image Synthesis and Editing with Stochastic Differential Equations, Aug 2021. 2

[43] Depu Meng, Xiaokang Chen, Zejia Fan, Gang Zeng, Houqiang Li, Yuhui Yuan, Lei Sun, and Jingdong Wang. Con ditional DETR for Fast Training Convergence. arXiv preprint arXiv:2108.06152, 2021. 2

[44] Chong Mou, Xintao Wang, Liangbin Xie, Jian Zhang, Zhon gang Qi, Ying Shan, and Xiaohu Qie. T2I-Adapter: Learning Adapters to Dig out More Controllable Ability for Text-to Image Diffusion Models, Feb 2023. 2

[45] Alex Nichol, Prafulla Dhariwal, Aditya Ramesh, Pranav Shyam, Pamela Mishkin, Bob McGrew, Ilya Sutskever, and Mark Chen. GLIDE: Towards Photorealistic Image Genera tion and Editing with Text-Guided Diffusion Models. 2

[46] OpenAI. GPT-4 Technical Report, 2023. 3

[47] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In International Conference on Machine Learning, pages 8748–8763. PMLR, 2021. 2

[48] Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu, and Mark Chen. Hierarchical Text-Conditional Image Gener ation with CLIP Latents. 2

[49] Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun. Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks. IEEE Transactions on Pattern Analysis and Machine Intelligence, 39(6):1137–1149, 2017. 2

[50] Tianhe Ren, Shilong Liu, Feng Li, Hao Zhang, Ailing Zeng, Jie Yang, Xingyu Liao, Ding Jia, Hongyang Li, He Cao, et al. detrex: Benchmarking Detection Transformers. arXiv preprint arXiv:2306.07265, 2023. 2

[51] Tianhe Ren, Jianwei Yang, Shilong Liu, Ailing Zeng, Feng Li, Hao Zhang, Hongyang Li, Zhaoyang Zeng, and Lei Zhang. A Strong and Reproducible Object Detector with Only Public Datasets, 2023. 2

[52] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. High-Resolution Image Synthesis with Latent Diffusion Models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 10684–10695, 2022. 2, 3, 7

[53] Nataniel Ruiz, Yuanzhen Li, Varun Jampani, Yael Pritch, Michael Rubinstein, and Kfir Aberman. DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation, Aug 2022. 2

[54] Chitwan Saharia, William Chan, Saurabh Saxena, Lala Li, Jay Whang, Emily Denton, Seyed Kamyar, Seyed Ghasemipour, Burcu Karagol, SSara Mahdavi, RaphaGontijo Lopes, Tim Salimans, Jonathan Ho, DavidJ Fleet, and Mohammad Norouzi. Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding. 2

[55] Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, and Yueting Zhuang. HuggingGPT: Solving ai tasks with chatgpt and its friends in huggingface. arXiv preprint arXiv:2303.17580, 2023. 2, 3

[56] Roman Suvorov, Elizaveta Logacheva, Anton Mashikhin, Anastasia Remizova, Arsenii Ashukha, Aleksei Silvestrov, Naejin Kong, Harshith Goka, Kiwoong Park, and Victor Lempitsky. Resolution-robust Large Mask Inpainting with Fourier Convolutions. arXiv preprint arXiv:2109.07161, 2021. 7

[57] Romal Thoppilan, Daniel De Freitas, Jamie Hall, Noam Shazeer, Apoorv Kulshreshtha, Heng-Tze Cheng, Alicia Jin, Taylor Bos, Leslie Baker, Yu Du, et al. Lamda: Language models for dialog applications. arXiv preprint arXiv:2201.08239, 2022. 2

[58] Jiaqi Wang, Pan Zhang, Tao Chu, Yuhang Cao, Yujie Zhou, Tong Wu, Bin Wang, Conghui He, and Dahua Lin. V3Det: Vast Vocabulary Visual Detection Dataset. arXiv preprint arXiv:2304.03752, 2023. 4

[59] Peng Wang, An Yang, Rui Men, Junyang Lin, Shuai Bai, Zhikang Li, Jianxin Ma, Chang Zhou, Jingren Zhou, and Hongxia Yang. OFA: Unifying Architectures, Tasks, and Modalities Through a Simple Sequence-to-Sequence Learning Framework. In ICML, 2022. 2

[60] Weihan Wang, Qingsong Lv, Wenmeng Yu, Wenyi Hong, Ji Qi, Yan Wang, Junhui Ji, Zhuoyi Yang, Lei Zhao, Xixuan Song, Jiazheng Xu, Bin Xu, Juanzi Li, Yuxiao Dong, Ming Ding, and Jie Tang. CogVLM: Visual Expert for Pretrained Language Models, 2023. 2

[61] Yinhuai Wang, Jing Lin, Ailing Zeng, Zhengyi Luo, Jian Zhang, and Lei Zhang. Physhoi: Physics-based imita-

tion of dynamic human-object interaction. arXiv preprint arXiv:2312.04393, 2023. 2

[62] Chenfei Wu, Shengming Yin, Weizhen Qi, Xiaodong Wang, Zecheng Tang, and Nan Duan. Visual ChatGPT: Talking, Drawing and Editing with Visual Foundation Models. arXiv preprint arXiv:2303.04671, 2023. 2, 3

[63] Yunyang Xiong, Bala Varadarajan, Lemeng Wu, Xiaoyu Xi ang, Fanyi Xiao, Chenchen Zhu, Xiaoliang Dai, Dilin Wang, Fei Sun, Forrest Iandola, et al. EfficientSAM: Leveraged Masked Image Pretraining for Efficient Segment Anything. arXiv preprint arXiv:2312.00863, 2023. 6

[64] Jiarui Xu, Sifei Liu, Arash Vahdat, Wonmin Byeon, Xiaolong Wang, and Shalini De Mello. Open-Vocabulary Panoptic Segmentation with Text-to-Image Diffusion Models. arXiv preprint arXiv:2303.04803, 2023. 7

[65] Mengde Xu, Zheng Zhang, Fangyun Wei, Han Hu, and Xiang Bai. Side Adapter Network for Open-Vocabulary Semantic Segmentation, 2023. 7

[66] Bin Yan, Yi Jiang, Jiannan Wu, Dong Wang, Zehuan Yuan, Ping Luo, and Huchuan Lu. Universal Instance Perception as Object Discovery and Retrieval. In CVPR, 2023. 2, 7

[67] Feng Yan, Weixin Luo, Yujie Zhong, Yiyang Gan, and Lin Ma. Bridging the Gap Between End-to-end and Non-End-to-end Multi-Object Tracking, 2023. 2

[68] Binxin Yang, Shuyang Gu, Bo Zhang, Ting Zhang, Xuejin Chen, Xiaoyan Sun, Dong Chen, and Fang Wen. Paint by Ex ample: Exemplar-based Image Editing with Diffusion Models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 18381–18391, 2023. 7

[69] Jie Yang, Bingliang Li, Fengyu Yang, Ailing Zeng, Lei Zhang, and Ruimao Zhang. Boosting human-object interaction de tection with text-to-image diffusion model. arXiv preprint arXiv:2305.12252, 2023. 2

[70] Jie Yang, Chaoqun Wang, Zhen Li, Junle Wang, and Ruimao Zhang. Semantic human parsing via scalable semantic transfer over multiple label domains. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 19424–19433, 2023. 2

[71] Jie Yang, Ailing Zeng, Feng Li, Shilong Liu, Ruimao Zhang, and Lei Zhang. Neural Interactive Keypoint Detection. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 15122–15132, 2023. 2

[72] Jie Yang, Ailing Zeng, Shilong Liu, Feng Li, Ruimao Zhang, and Lei Zhang. Explicit box detection unifies end-to-end multi-person pose estimation. In International Conference on Learning Representations, 2023. 2

[73] Jie Yang, Ailing Zeng, Ruimao Zhang, and Lei Zhang. Unipose: Detecting any keypoints. arXiv preprint arXiv:2310.08530, 2023. 2

[74] Zhendong Yang, Ailing Zeng, Chun Yuan, and Yu Li. Effective whole-body pose estimation with two-stages distillation. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 4210–4220, 2023. 2

[75] Michihiro Yasunaga, Armen Aghajanyan, Weijia Shi, Rich James, Jure Leskovec, Percy Liang, Mike Lewis, Luke Zettlemoyer, Wen-Tau Yih, and Memory Memory. Retrieval Augmented Multimodal Language Modeling. 2

[76] Chaoning Zhang, Dongshen Han, Yu Qiao, Jung Uk Kim, Sung-Ho Bae, Seungkyu Lee, and Choong Seon Hong. Faster Segment Anything: Towards Lightweight SAM for Mobile Applications. arXiv preprint arXiv:2306.14289, 2023. 6

[77] Hao Zhang, Feng Li, Shilong Liu, Lei Zhang, Hang Su, Jun Zhu, Lionel M. Ni, and Heung-Yeung Shum. DINO: DETR with Improved DeNoising Anchor Boxes for End-to-End Object Detection, 2022. 2

[78] Hao Zhang, Feng Li, Huaizhe Xu, Shijia Huang, Shilong Liu, Lionel M Ni, and Lei Zhang. MP-Former: Mask-Piloted Transformer for Image Segmentation. arXiv preprint arXiv:2303.07336, 2023. 2

[79] Hao Zhang, Feng Li, Xueyan Zou, Shilong Liu, Chunyuan Li, Jianfeng Gao, Jianwei Yang, and Lei Zhang. A Simple Framework for Open-Vocabulary Segmentation and Detection. arXiv preprint arXiv:2303.08131, 2023. 2, 3, 7

[80] Hao Zhang, Hongyang Li, Feng Li, Tianhe Ren, Xueyan Zou, Shilong Liu, Shijia Huang, Jianfeng Gao, Lei Zhang, Chunyuan Li, and Jianwei Yang. LLaVA-Grounding: Grounded Visual Chat with Large Multimodal Models, 2023. 2

[81] Haotian Zhang, Pengchuan Zhang, Xiaowei Hu, Yen-Chun Chen, Liunian Harold Li, Xiyang Dai, Lijuan Wang, Lu Yuan, Jenq-Neng Hwang, and Jianfeng Gao. GLIPv2: Unifying Localization and Vision-Language Understanding. arXiv preprint arXiv:2206.05836, 2022. 3

[82] Lvmin Zhang and Maneesh Agrawala. Adding Conditional Control to Text-to-Image Diffusion Models. 2

[83] Youcai Zhang, Xinyu Huang, Jinyu Ma, Zhaoyang Li, Zhaochuan Luo, Yanchun Xie, Yuzhuo Qin, Tong Luo, Yaqian Li, Shilong Liu, et al. Recognize Anything: A Strong Image Tagging Model. arXiv preprint arXiv:2306.03514, 2023. 2, 3, 4, 5

[84] Yifu Zhang, Peize Sun, Yi Jiang, Dongdong Yu, Fucheng Weng, Zehuan Yuan, Ping Luo, Wenyu Liu, and Xinggang Wang. ByteTrack: Multi-Object Tracking by Associating Every Detection Box. 2022. 2

[85] Xu Zhao, Wenchao Ding, Yongqi An, Yinglong Du, Tao Yu, Min Li, Ming Tang, and Jinqiao Wang. Fast Segment Anything, 2023. 6

[86] Chaoyang Zhu, Yiyi Zhou, Yunhang Shen, Gen Luo, Xingjia Pan, Mingbao Lin, Chao Chen, Liujuan Cao, Xiaoshuai Sun, and Rongrong Ji. SeqTR: A Simple Yet Universal Network for Visual Grounding, page 598–615. Springer Nature Switzerland, 2022. 2

[87] Xizhou Zhu, Weijie Su, Lewei Lu, Bin Li, Xiaogang Wang, and Jifeng Dai. Deformable DETR: Deformable Transformers for End-to-End Object Detection. In ICLR 2021: The Ninth International Conference on Learning Representations, 2021. 2

[88] Xueyan Zou\*, Zi-Yi Dou\*, Jianwei Yang\*, Zhe Gan, Linjie Li, Chunyuan Li, Xiyang Dai, Jianfeng Wang, Lu Yuan, Nanyun Peng, Lijuan Wang, Yong Jae Lee\*, and Jianfeng Gao\*. Generalized Decoding for Pixel, Image and Language. 2022. 2, 7