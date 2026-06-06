# Palantír: Towards Efficient Super Resolution for Ultra-high-definition Live Streaming

Xinqi Jin1†, Zhui Zhu2†, Xikai Sun2, Fan Dang3, Jiangchuan Liu4, Jingao Xu5, Kebin Liu3, Xinlei Chen6,7,8, and Yunhao Liu2,3

1School of Software, Tsinghua University 2Department of Automation, Tsinghua University 3Global Innovation Exchange, Tsinghua University 4School of Computing Science, Simon Fraser University 5School of Computer Science, Carnegie Mellon University 6Shenzhen International Graduate School, Tsinghua University 7Pengcheng Laboratory, China 8RISC-V International Open Source Laboratory, China {jinxq21,z-zhu22,sxk23}@mails.tsinghua.edu.cn,dangfan@tsinghua.edu.cn, jcliu@sfu.ca,jingaox@andrew.cmu.edu,kebinliu2021@tsinghua.edu.cn, chen.xinlei@sz.tsinghua.edu.cn,yunhao@tsinghua.edu.cn

# ABSTRACT

Neural enhancement through super-resolution (SR) deep neural networks (DNNs) opens up new possibilities for ultrahigh-definition (UHD) live streaming over existing encoding and networking infrastructure. Yet, the heavy SR DNN inference overhead leads to severe deployment challenges. To reduce the overhead, existing systems propose to apply DNNbased SR only on carefully selected anchor frames while upscaling non-anchor frames via the lightweight reusing-based SR approach. However, frame-level scheduling is coarsegrained and fails to deliver optimal efficiency. In this work, we propose Palantír, the first neural-enhanced UHD live streaming system with fine-grained patch-level scheduling. Two novel techniques are incorporated into Palantír to select the most beneficial anchor patches and support latencysensitive UHD live streaming applications. Firstly, under the guidance of our pioneering and theoretical analysis, Palantír constructs a directed acyclic graph (DAG) for lightweight yet accurate SR quality estimation under any possible anchor patch set. Secondly, to further optimize the scheduling latency, Palantír improves parallelizability by refactoring the computation subprocedure of the estimation process into a sparse matrix-matrix multiplication operation.

The evaluation results suggest that Palantír incurs a negligible scheduling latency accounting for less than 5.7% of the end-to-end latency requirement. When compared to the naive method of applying DNN-based SR on all the frames, Palantír can reduce the SR DNN inference overhead by 20 times (or 60 times) while preserving 54.0-82.6% (or 32.8-64.0%) of the quality gain. When compared to the state-of-the-art real-time frame-level scheduling strategy, Palantír can reduce the SR DNN inference overhead by 80.1% at most (and 38.4% on average) without sacrificing the video quality.

# 1 INTRODUCTION

UHD videos such as 4K and 8K videos are expected to form a huge market worth more than \$1 trillion in the following few years [18]. More and more UHD live-streaming applications are deployed to revolutionize many aspects of our society. For example, the UHD live streaming of major sports events such as the Olympics [24, 25] creates unprecedentedly immersive experiences for audiences. Besides, with the real-time UHD video from inspection and surveillance cameras, human operators can have a precise understanding of the spot and remotely take immediate actions to prevent emergent accidents [13, 17].

However, the bitrates of the encoded UHD videos are significantly larger than videos of lower resolutions and pose great challenges to existing network infrastructure. Specifically, the bitrates of 4K videos can be as large as 45Mbps [21], while the worldwide average uplink bandwidth of mobile broadband networks is only 11.07 Mbps [34]. A common solution to this problem is using dedicated hardware encoders [8, 25, 28], which can encode the UHD video more efficiently and provide much lower bitrates. However, hardware encoders are very expensive and typically cost hundreds to thousands of dollars. Using fixed broadband networks for the uplink is an alternative solution, but it inevitably affects mobility and prohibits applications such as drone-based inspection [17, 37].

Recently, neural enhancement has been proposed [11, 42, 44] and deployed [14, 27, 32, 45] to improve video streaming. It can potentially boost the broad deployment of UHD live streaming by allowing the streaming source to stream only a low-bitrate low-resolution (LR) video over the bandwidthlimited uplink and using a super-resolution (SR) deep neural network (DNN) to upscale the LR stream to its SR counterpart later. However, as detailed in Sec. 2.1, SR DNN inference incurs heavy computation overhead and deployment challenges. Therefore, many research efforts have been aimed at optimizing the overhead. NEMO [42] and NeuroScaler [44] achieve this by categorizing frames into anchor frames and non-anchor frames: only anchor frames undergo computation-intensive DNN-based SR, while non-anchor frames are reconstructed via reusing the SR results of reference frames. The most beneficial anchor frames are carefully selected so that a large quality gain is achieved with a small anchor frame set. Nevertheless, these systems still fail to reduce the overhead optimally due to their coarse scheduling granularity and consequently insufficient utilization of videos’ temporal redundancy. For example, a beneficial anchor frame may still contain some existing objects that can be well reconstructed by reusing-based SR.

In this paper, we propose Palantír, the first patch-level neural-enhanced UHD live streaming system. Palantír aims to further optimize the computation overhead via fine-grained scheduling, i.e., selecting the appropriate type — anchor or non-anchor — for each patch (part of a single frame). Palantír is centered around two primary goals. The first is to accurately pinpoint the most beneficial anchor patches so that a smaller overhead can be achieved without sacrificing the quality gains. The second is to minimize the scheduling latency to better support latency-sensitive applications such as public surveillance [16, 23], interactive shows [38], and remote drone operation [17, 37]. As introduced next, Palantír integrates a theory-guided DAG-based quality estimation method and a parallelism scheme to meet the two goals.

DAG-based quality estimation for patch-level scheduling (Sec. 4). Quality measurement for anchor selection violates the second goal due to the heavy measurement overhead. Although some quality estimation strategies are proposed in NEMO and NeuroScaler for efficient selection, they are originally designed for other scenarios and can hardly be adapted to meet our two goals. Tens of seconds are spent in NEMO for anchor frame selection in a video segment of a few seconds. Extending the strategy to the patch level incurs even larger latency. NeuroScaler uses a real-time yet inaccurate estimation method, and it mainly compensates for the inaccuracy by prioritizing certain frame types. The underlying insight is that certain frame types have large degrees of reference. Our preliminary experiments (detailed in Sec. 4.1) validate the insight - the common language effect size [31] reaches 97.4% (close to the best case of 100%) between prioritized frame types and normal frames. However, the metric is as low as 58.9% (close to the worst case of 50%) between different sub-frame units of encoded videos, so type-based prioritization is unhelpful in patch-level scheduling.

In this paper, we propose to solve the estimation problem from a novel and theoretical perspective. We systematically analyze the SR error (which is inversely related to the quality gains) accumulation process in neural enhancement for the first time (Sec. 4.2). Incorporated with a few reasonable assumptions, the analysis suggests a lightweight DAG structure for quick and accurate simulation of the process. The SR error incurred by any anchor patch set can be simulated based on the DAG. Effective approximations are further proposed to easily construct the DAG without contradicting modern codecs and decoder softwares (Sec. 4.3).

Parallelized scheduling (Sec. 5). We find that the DAG structure is highly irregular due to the complex reference relationship among patches, making it difficult to achieve the concurrent attainment of correctness and parallelism (Sec. 5.1). Yet, our measurement reveals that a sequential implementation of DAG-based estimation achieves the first goal but is still distant from the second goal.

We get out of the dilemma by utilizing the inherent characteristics of the DAG structure. Specifically, we find that due to the acyclic reference relationship among frames, there exist no bi-directional edges between two groups of patches corresponding to two frames. Therefore, we group patch nodes by their belonging frames and introduce both intra-set and inter-set parallelism to refactor the per-group computation process into a highly parallelizable sparse matrix-matrix multiplication (SpMM) operation. Such optimization reduces the latency by more than 200 times without changing the scheduling result and simultaneously meets the two goals (Sec. 5.2).

The key contributions of the paper include:

• Palantír is the first to enable efficient SR enhancement for UHD live streaming via fine-grained scheduling.   
• Palantír can effectively identify the most beneficial anchor patches by DAG-based quality estimations. The DAG modeling is based on our pioneering, systematic, and formalized analysis of SR error propagation.   
• By utilizing the inherent characteristics of the DAG structure, Palantír can be optimized via parallelism to further reduce the DAG-based anchor selection latency by more than 200 times while not affecting the selection results.   
• We conduct extensive evaluations to demonstrate that Palantír significantly reduces the overhead of neural enhancement and incurs a negligible latency.

The rest of the paper is structured as follows. Sec. 2 reviews preliminary knowledge. An overview of Palantír is outlined in Sec. 3. We detail our theory-guided DAG-based estimation method in Sec. 4 and the latency optimization strategy for estimation-based scheduling in Sec. 5. We evaluate Palantír in Sec. 6. A discussion on limitations and future work is conducted in Sec. 7. Related work is reviewed in Sec. 8 and the paper is concluded in Sec. 9.

# 2 BACKGROUND

# 2.1 Primer on SR Streaming

SR DNNs typically incorporate convolution layers and modules specially designed for upscaling (e.g., deconvolution [15], pixel shuffle [36], etc). We refer readers to [10] for further details of the SR DNNs.

Currently, there are two common deployment models for SR enhancement. One is to execute the SR DNN inference on the mobile streaming clients [14, 27, 32, 45], and the other is to execute the SR DNN on a cloud server so that a lot of audience for the same video can benefit from the onetime server-side enhancement [44]. Yet, SR DNNs are of high computation complexity and lead to severe deployment challenges in both deployment models. In the first model, the battery of mobile clients can be easily drained. Consequently, Microsoft Edge VSR disables its SR feature when the device is not being charged [32]. As for the second model, the heavy inference overhead appears in the form of the high monetary cost of using cloud servers (estimated to be at least \$1.690 per hour per 4K stream [44]). Lowering the overhead is essential to a broader application of SR enhancement.

# 2.2 Reusing-based SR

To enable low-cost SR enhancement, researchers have built the NEMO [42] system, where an SR-enhanced decoder is adopted to reduce the cost by using video temporal redundancy. In the SR decoder, video frames are categorically divided: anchor frames are upscaled via DNN-based SR, while non-anchor frames are quickly upscaled via reusing-based SR. To appreciate the intricacies of reusing, a basic understanding of video codecs is essential. Video coding predominantly encodes a block through inter coding; it identifies a similar reference block from a prior frame and only stores the subtle difference or residual between the two blocks. A reference index is retained in the coded video to identify the frame containing the reference block or the reference frame, while a motion vector is stored to represent the potential spatial offset between the current and reference blocks (owing to object movements or camera shifts). To decode an inter-coded block $b _ { i n t e r } ^ { i } \left( i . e . , \pmb { \Theta } \right.$ in Fig. 1), the decoder first parses the reference index to determine its reference frame (➊) from the decoded frame buffer and then parses the motion vector (➋) to determine its reference block $b _ { i n t e r } ^ { i } . r e f$ (➌). The reference block is added to the decoded residual

![](images/c7a6ef0f6ef3421b4f45cd3a919c2be05be7e8a165140ddb820e2b69fe6c50d4.jpg)



Figure 1: Video decoding pipeline.

![](images/7419e43588254a7f33b970730aab9ebafece830bb6fd72a7a72a7759fba79302.jpg)



Figure 2: SR-integrated decoder overview.

$b _ { i n t e r } ^ { i } . r e s \left( \pmb { \odot } \right)$ . This can be formally expressed as

$$
b _ {i n t e r} ^ {i} = b _ {i n t e r} ^ {i}. r e f + b _ {i n t e r} ^ {i}. r e s. \tag {1}
$$

An alternative to inter-coding is intra-coding, which, while similar, leverages spatial redundancy and encodes an intracoded block $b _ { i n t r a } ^ { i }$ by storing the intra-frame residual. We refer the readers to the technical specifications [22] for further details. Note that patches are not the same as encoding blocks in this paper: (1) blocks can have different sizes, while the sizes of all patches are the same to ease fine-grained scheduling; (2) a block is either intra-coded or inter-coded, while a patch is either an anchor or non-anchor. We leave selecting anchor patches of different shapes for future work.

The SR decoder in NEMO [42] is developed based on the open-source Google libvpx VP9 decoder [5]. As shown in Fig. 2, the SR decoder first decodes a frame into its LR version by referring to decoded frames in the LR buffer (➊) and can insert it into the LR buffer for future frames (➋), just as a standard decoder. Along with the LR video, a cache profile is also downloaded, each bit of which indicates whether a frame is an anchor or non-anchor. If the current frame is an anchor, the LR version will be fed into the SR DNN to obtain the SR version (➌), which may be inserted into the SR buffer for future reuse (➍). Otherwise, the SR version is obtained via reusing-based SR (➎). The reusing-based SR uses a process similar to that in Fig. 1 to decode every intercoded block $b _ { i n t e r } ^ { i }$ to its SR version, except that the motion vector is scaled (e.g., by 4 times, when the LR and SR frames are 240p and 960p, respectively), the residual is upscaled by bilinear interpolation to match the resolution of the superresoluted block $( b _ { i n t e r } ^ { i } . S R )$ , and the same reference index is used to fetch cached frames from the SR buffer rather than the LR buffer. We can formulate the process as

![](images/7fcd3eb00a629f634462af5096a9359299e4e8e7d8279b49c9ae0aacee8b41a7.jpg)



Figure 3: Palantír overview.

$$
b _ {i n t e r} ^ {i}. S R = b _ {i n t e r} ^ {i}. r e f. S R + i n t e r p (b _ {i n t e r} ^ {i}. r e s, s c a l e), \tag {2}
$$

where ?????????? is the ratio of the width of the SR video to that of the LR video. We also rewrite Eq. (1) as

$$
b _ {i n t e r} ^ {i}. L R = b _ {i n t e r} ^ {i}. r e f. L R + b _ {i n t e r} ^ {i}. r e s \tag {3}
$$

to distinguish between the LR and SR version of the same block in the SR decoder. As for any intra-coded block $b _ { i n t r a } ^ { i }$ in the non-anchor frame, it is upscaled by applying bilinear interpolation on its decoded LR version, i.e.,

$$
b _ {i n t r a} ^ {i}. S R = \text { interp } (b _ {i n t r a} ^ {i}. L R, \text { scale }). \tag {4}
$$

After upscaling every block to their SR versions, the SR version of the non-anchor frame may be inserted into the SR buffer for future reuse (➏). More details are available in [42]. Based on the open-source SR decoder in NEMO, we develop a fine-grained SR decoder, where a larger cache profile indicates the type (i.e., anchor or non-anchor) of every patch, and, based on their types, patches are upscaled via either DNN-based or reusing-based SR.

# 2.3 Estimation-based Anchor Selection

Assuming that the DNN model is well suited for the video, selecting all patches as anchors naturally results in the best quality but also leads to the highest overhead. Similarly, the number of anchor frames is limited in NEMO and NeuroScaler to reduce the cost. These two systems thus greedily select the anchor frame that yields the highest quality until some budget or goal is met. As measuring the video quality for greedy search is too time-consuming, NEMO and NeuroScaler approximate the video qualities with estimation values. In NEMO, a heavy initial measurement phase (reported to take nearly one minute for a video segment of 4 seconds [42]) is required before conducting any estimation. Extending the strategy to patch-level scheduling can even further slow down the measurement phase. Since the strategy in NEMO fails to support live streaming due to its low anchor selection throughput, we do not use it as a baseline in our paper. Alternatively, we choose to use the strategy introduced in NeuroScaler [44] as our baseline.

# 3 SYSTEM OVERVIEW

Scope. We aim to support UHD live streaming via SR enhancement. As video frames are highly redundant, we propose to apply DNN-based SR only on carefully chosen anchor patches while upscaling non-anchor patches via the lightweight reusing-based SR mechanism. This optimization is essential to improve the practicality of SR enhancement, considering the effect of SR inference on the battery life of mobile clients and the monetary costs of cloud-based SR inference.

Design goals. First, Palantír aims to pinpoint the most beneficial anchor patches, so that it can use a small anchor patch set to reduce the DNN inference cost while achieving a large quality gain. Second, Palantír should complete the finegrained scheduling as quickly as possible, considering the stringent latency requirements in many video applications [9, 16, 20, 37].

Workflow. The workflow of Palantír is shown in Fig. 3. Considering the limited uplink bandwidth [34] and the high bitrate of the original high-resolution (HR) video [21], the streamer only uploads the downsampled LR video to the media server. The server generates an SR error DAG (Sec. 4.3) for every LR video segment whose time duration equals the pre-defined scheduling interval. The quality of the corresponding SR segment under any possible anchor patch set can be quickly estimated using the constructed DAG, and beneficial anchor patches are greedily searched via DAG-based quality estimation. Two novel parallelism strategies are used to further accelerate the searching process without changing its results (Sec. 5). A cache profile is then created, every bit of which indicates whether a patch in the LR segment is an anchor or non-anchor. In the existence of a powerful cloud server [44], both the LR segment and its corresponding cache profile are streamed to the server and then processed by the SR decoder on the server. Or, alternatively, the SR decoder can be executed in the streaming client to perform cache profile-guided SR enhancement.

Deployment Scenario. Palantír is designed for UHD live streaming but also supports videos of lower resolutions and video-on-demand services. Our initial prototype is tailored for the VP9 codec, considering the engineering complexities involved in transitioning to other codecs. However, the system is not restricted to VP9-specific functionalities and should be adaptable to a range of other codecs.

# 4 DAG-BASED QUALITY ESTIMATION

We first identify the problems with existing quality estimation methods. To design a fine-grained and lightweight estimation method, we give a pioneering analysis of the SR error propagation process. Based on our analysis, we propose DAG-based error propagation modeling and quality estimation. We use reasonable approximations to easily determine the values of static attributes in the DAG.

# 4.1 Problems with Existing Methods

A natural way to estimate the video quality under a given anchor patch set is to extend the methods used in NEMO or NeuroScaler. The strategy in NEMO is based on the observation that the quality gain of a frame is mostly determined by the most relevant anchor frame. NEMO first enumerates every anchor frame set consisting of a single frame ?? and measures the quality (denoted as ???? (?? |?? )) of every frame ?? under every enumerated single anchor frame set |?? |. Then, NEMO estimates the quality under any anchor frame set AP as $F Q ( i | A P ) \approx m a x _ { f \in A P } F Q ( i | f )$ . Capitalized on the heuristics, NEMO requires a heavy measurement phase in nature and incurs a high latency (reported to be 59.6 seconds for a video segment of 4 seconds [42]) not suitable for live streaming. The scheme can be easily extended to the patch-level granularity by firstly conducting measurements for all single anchor patch sets, but the latency of initial measurements can be further increased.

In contrast, the method in NeuroScaler [44] is much more efficient. It models the super-resolution error propagation process as a linked list, where each node corresponds to a frame and each pair of consecutive frames is linked. The SR error of an anchor frame is assumed to be 0, while the error of a non-anchor frame equals that of its preceding frame node plus the residual between the two frames. An anchor set that leads to a lower sum of the errors over all frame nodes is regarded as leading to higher video quality.

However, such a modeling is too simplified and ignores the effect of the degree of reference. In fact, each frame can have at most three reference frames in VP9 [22], and its SR error directly depends on the error of every reference frame rather than that of a single preceding frame. Conversely, some types of frames (i.e., keyframes and alternative reference frames in the VP9 codec [22]) may be referred to by many subsequent frames (rather than a single subsequent frame, as modeled by NeuroScaler). To compensate for over-simplified modeling, NeuroScaler gives priorities to keyframes and alternative reference frames: a normal frame may be selected as the anchor only if all the keyframes and alternative reference frames (AltRefs) have been selected as anchors. Yet, transferring the linked list-based modeling and the heuristic mitigation strategy to our context faces several challenges:

![](images/fbd0f5f2b66cc1ba0c38b0d9b92f8492f545d217e0daeb8db663086a378e77cd.jpg)



Figure 4: The distribution of degrees of reference for different types of frames and MBs.

• First, a patch can refer to a huge number of preceding patches, so it will be even more unreasonable if we model the SR error propagation process as multiple independent linked lists of patch nodes for fine-grained scheduling. Denoting the number of rows in the patch grid as ???? and the number of columns in the patch grid as ????, and considering that each frame may refer to at most three frames in VP9 [22], a patch in a VP9-coded video can refer to 3 · ???? · ???? patches at most.

• Second, we argue that the types of sub-frame encoding units such as macroblocks (MBs) do not implicitly imply their degrees of reference. Here we conduct a preliminary experiment on the 480p version of the first benchmark video used in the evaluation part (Sec. 6) to support our argument. We separately measure the distribution of degrees of reference among different types of frames and macroblocks (including prioritized frame types, unprioritized normal frames, intra-coded MBs, and inter-coded MBs). The degree of reference for a given frame (or MB) is quantitatively defined as $\frac { n u m \_ r e f e r e n c e s } { r e s o l u t i o n }$ , where ??????\_???? ?? ?????????????? denotes the number of pixels that refer to the given frame (or MB) for inter coding and ???????????????????? denotes the number of pixels in the given frame (or MB). As shown in Fig. 4, the degrees of references for keyframes and AltRefs are significantly greater than those of normal frames, while the distribution range of degrees of references for intra-coded MBs is similar to that for inter-coded MBs. We further use the common language effect size (CLES) [31] to quantize the results. The CLES is defined as the probability that a value randomly sampled from one distribution will be greater than that from another distribution. The CLES reaches 97.4% (close to the best case of 100%) between prioritized frame types and normal frames but is as low as 58.9% (close to the worst case of 50%) between different MB types. Therefore, type-based prioritization is helpful in frame-level scheduling but hardly applies to patch-level scheduling.

# 4.2 Understanding SR Error Propagation

We next give an analysis of the SR error propagation process, which lays the foundation for our DAG-based quality estimation.

• Case #1: non-anchor patches.

Analysis: every non-anchor patch ?? may consist of multiple inter-coded blocks $( b _ { i n t e r } ^ { 1 } , . . . , b _ { i n t e r } ^ { n 1 } )$ and intra-coded blocks $( b _ { i n t r a } ^ { 1 } , . . . , b _ { i n t r a } ^ { n 2 } )$ . For analysis purposes, we split those blocks spanning multiple patches into multiple subblocks, each within a single patch. The SR error of ?? is:

?? .??????????

$$
= \left| \left| P. S R - P. H R \right| \right| _ {2} ^ {2} \tag {5}
$$

$$
= \sum_ {i = 1} ^ {n 1} | | b _ {i n t e r} ^ {i}. S R - b _ {i n t e r} ^ {i}. H R | | _ {2} ^ {2} + \sum_ {i = 1} ^ {n 2} | | b _ {i n t r a} ^ {i}. S R - b _ {i n t r a} ^ {i}. H R | | _ {2} ^ {2}
$$

$$
= \sum_ {i = 1} ^ {n 1} b _ {i n t e r.} ^ {i}. e r r o r + \sum_ {i = 1} ^ {n 2} b _ {i n t r a.} ^ {i}. e r r o r.
$$

Example (see Fig. 5): $P _ { n } ^ { 1 , 1 }$ .?????????? equals the sum of $b _ { i n t e r } ^ { i 1 } .$ ?????????? , ????2?????? $b _ { i n t r a } ^ { i 2 }$ .?????????? , and the errors of many other blocks within $P _ { n } ^ { 1 , 1 }$ (not marked due to the limited space).

Conclusion #1: the SR error of a non-anchor patch is the sum of the SR errors of all inter-coded and intra-coded blocks within the patch.

Analysis: According to the equation (2), we can further write the SR error of an inter-coded block $b _ { i n t e r } ^ { i }$ ?? ?????????? as

$$
\begin{array}{l} b _ {\text { inter }} ^ {i}. \text { error } \tag {6} \\ = | | b _ {i n t e r} ^ {i}. r e f. S R + i n t e r p (b _ {i n t e r} ^ {i}. r e s, s c a l e) - b _ {i n t e r} ^ {i}. H R | | _ {2} ^ {2} \\ \approx b _ {i n t e r.} ^ {i}. r e s. c o m p l e x i t y + b _ {i n t e r.} ^ {i}. r e f. e r r o r, \\ \end{array}
$$

where

$$
\begin{array}{l} b _ {i n t e r} ^ {i}. \text { res.complexity } \tag {7} \\ = | | i n t e r p (b _ {i n t e r} ^ {i}. r e s, s c a l e) - (b _ {i n t e r} ^ {i}. H R - b _ {i n t e r} ^ {i}. r e f. H R) | | _ {2} ^ {2} \\ = | | i n t e r p (b _ {i n t e r} ^ {i}. L R - b _ {i n t e r} ^ {i}. r e f. L R, s c a l e) - (b _ {i n t e r} ^ {i}. H R \\ - b _ {i n t e r. r e f. H R)} ^ {i} | | _ {2} ^ {2} \\ = \left\| \text { interp } (i n t e r p (b _ {i n t e r} ^ {i}. H R - b _ {i n t e r} ^ {i}. r e f. H R, s c a l e ^ {- 1}), s c a l e) \right. \\ - \left(b _ {i n t e r} ^ {i}. H R - b _ {i n t e r} ^ {i}. r e f. H R\right) | | _ {2} ^ {2} \\ \end{array}
$$

and

$$
\begin{array}{l} b _ {i n t e r} ^ {i}. r e f. e r r o r \tag {8} \\ = | | b _ {i n t e r} ^ {i}. r e f. S R - b _ {i n t e r} ^ {i}. r e f. H R | | _ {2} ^ {2}. \\ \end{array}
$$

Here, $b _ { i n t e r } ^ { i }$ .??????.???????????????????? relates to the texture com-?? ?? plexity of the HR residual $( i . e . , b _ { i n t e r } ^ { i } . H R - b _ { i n t e r } ^ { i } . r e f . H R )$ since a HR residual with more complex texture details will experience a more significant deviation after the process

![](images/3209675a8709b4ddce1f499b1c0fe9babc491eb5fb2834d51a6578b806648c2a.jpg)



$F _ { n - 1 }$

![](images/6233baf6d3db039fe0b13f30cd254b7185856361b3a19827520c4062bd6b5290.jpg)



$F _ { n }$   
Figure 5: An example of SR error propagation.

of downscaling and re-upsampling, i.e., ???????????? (???????????? (·, ?????????? −1), ??????????).

Similarly, according to the equation (4), we have

$$
b _ {i n t r a} ^ {i}. e r r o r = b _ {i n t r a} ^ {i}. c o m p l e x i t y, \tag {9}
$$

where

$$
\begin{array}{l} b _ {i n t r a} ^ {i}. \text { complexity } \tag {10} \\ = | | i n t e r p (b _ {i n t r a} ^ {i}. L R, s c a l e) - b _ {i n t r a} ^ {i}. H R | | _ {2} ^ {2} \\ = | | \text { interp } (i n t e r p (b _ {i n t r a} ^ {i}. H R, s c a l e ^ {- 1}), s c a l e) \\ - b _ {i n t r a} ^ {i}. H R | | _ {2} ^ {2} \\ \end{array}
$$

relates to the texture complexity of the HR content $( i . e . ,$ $b _ { i n t r a } ^ { i } . H R )$ .

Example (see Fig. 5): for $b _ { i n t e r } ^ { i 1 }$ in the frame $F _ { n }$ (see Fig. 5), its SR error equals $b _ { i n t e r } ^ { i 1 } .$ ????1?????????? .?????? .???????????????????? +????1???????? ?? .???? ?? .?????????? , where $b _ { i n t e r } ^ { i 1 } . r e f$ is its reference block in $F _ { n - 1 } ,$ a reference frame of $F _ { n } ; \mathrm { f o r } b _ { i n t r a } ^ { i 2 } ;$ ????2?????????? , its SR error equals ????2?????? $b _ { i n t r a } ^ { i 2 }$ .????????????????????.

Conclusion #2: the SR error of an inter-coded block depends on both the texture complexity of its HR residual and the SR error of its reference block; while the SR error of an intra-coded block depends on the texture complexity of its HR content.

Analysis: combining the equation (5), (6), and (9), we have

$$
P. e r r o r \approx P. T C + P. A E, \tag {11}
$$

where

$$
\begin{array}{l} P. T C = \sum_ {i = 1} ^ {n 1} b _ {\text { inter }} ^ {i}. \text { res.complexity } \tag {12} \\ + \sum_ {i = 1} ^ {n 2} b _ {i n t r a. c o m p l e x i t y} ^ {i} \\ \end{array}
$$

indicates the texture complexity of the HR content or the HR residual, and

$$
P. A E = \sum_ {i = 1} ^ {n 1} b _ {\text { inter }} ^ {i}. \text { ref.error } \tag {13}
$$

is the accumulated error from depending blocks.

To reformulate the equation (13) and simplify the SR error accumulation process along patches, we make the following assumption:

Assumption #1: the per-pixel SR error within a patch is uniform - every pixel in the same patch shares exactly the same amount of error. $\mathbf { o r } ,$ formally speaking, we assume that

$$
p. e r r o r = | | p. S R - p. H R | | _ {2} ^ {2} = \frac {P . e r r o r}{\text { patch\_size }} \tag {14}
$$

holds for every pixel ?? in some patch ??.

Denoting the set of reference patches of ?? as $P ^ { 1 } , . . . , P ^ { n 3 }$ and according to the Assumption #1, we can reformulate the equation (13) as

$$
\begin{array}{l} P. A E = \sum_ {i = 1} ^ {n 1} b _ {\text { inter }} ^ {i}. \text { ref.error } \tag {15} \\ = \sum_ {i = 1} ^ {n 1} \sum_ {p \in b _ {i n t e r} ^ {i}. r e f} p. e r r o r \\ = \sum_ {i = 1} ^ {n 3} W ^ {i} \cdot P ^ {i}. e r r o r, \\ \end{array}
$$

where the weight coefficient $W ^ { i }$ indicates the ratio of the number of referenced pixels in $P ^ { i }$ to the patch size.

Example (see Fig. 5): for convenience, we assume that $b _ { i n t e r } ^ { i 1 }$ is the only inter-coded block in , , $P _ { n } ^ { 1 , 1 }$ . The weight between intersectof the pa $P _ { n } ^ { 1 , 1 }$ and regiosize; ?? 1 1 $P _ { n - 1 } ^ { 1 , 1 }$ 1 equatween arly, t f the.105 and $b _ { i n t e r } ^ { i 1 } . r e f$ $P _ { n - 1 } ^ { 1 , 1 }$ $P _ { n } ^ { 1 , 1 }$ ?? 1,2 $P _ { n - 1 } ^ { 1 , 2 }$ ?? −1 equals 0.323. According to the equation (11) and (15), ?? 1,1?? $P _ { n } ^ { 1 , 1 }$ .?????????? can be approximated as $P _ { n } ^ { 1 , 1 } . T C + 0 . 1 0 5$ · ?? 1,1 ??−1.?????????? + 0.323 · ?? 1,2??−1 $P _ { n - 1 } ^ { 1 , 1 } . e r r o r + 0 . 3 2 3 \cdot P _ { n - 1 } ^ { 1 , 2 } . e r r o r$ .?????????? .

From the equation (11), (12), and (15) we can make the final conclusion:

Conclusion #3: under the Assumption #1, the SR error of a non-anchor patch equals the weighted sum of the SR errors of its depending patches plus the texture complexities of its inter-coded HR residuals and its intra-coded HR contents.

• Case #2: anchor patches. Since it is common to train or fine-tune the SR DNNs to match the current video content in neural-enhanced streaming [11, 29, 44], we make the following assumption:

Assumption #2: the SR errors of anchor patches are always 0.

# 4.3 DAG Construction

According to the Conclusion #3, the SR error of a nonanchor patch is the weighted sum of those of its depending patches plus its texture complexity. A patch ?? may depend on another patch $P ^ { i }$ for inter-coding only if the frame containing $P ^ { i }$ is a reference frame of the frame containing the patch ??. Since the reference relationship among frames is directed and acyclic, the SR error propagation process among patches is also directed and acyclic. Therefore, we propose to use a directed acyclic graph (DAG) to represent the SR error origination and propagation process among patches, where every node corresponds to a patch and every edge indicates an inter-coding reference relationship. A static weight attribute is associated with every edge to reflect the degree of reference, corresponding to $\dot { W } ^ { i }$ in the equation (15). Three attributes are associated with each patch node ??:

• The static ?? .???? attribute represents the texture complexity (defined in the equation (12)) of ??.   
• The $P . i s _ { _ - }$ \_??????ℎ???? attribute indicates whether the patch node is an anchor or non-anchor under a given anchor patch set.   
• The P.error attribute represents the SR error. When P.is\_anchor equals 1, P.error equals 0 (according to the Assumption #2); otherwise, P.error equals the weighted sum of the ?????????? attributes of the predecessor nodes plus ?? .???? (according to the Conclusion #3).

Problem formulation. We aim to set the appropriate values for the is\_anchor attributes of all nodes to trade off the estimated quality and the inference overhead. The quality is estimated $\mathsf { a s } - \sum _ { P }$ ?? .?????????? . The inference overhead is affected by the number of anchor patches (i.e., Í?? ?? .????\_??????ℎ???? ).

Determining static attributes. At first glance of the last two lines of (7) (or (10)), we need data only from the HR video to compute the block-level texture complexities and then aggregate the block-level results to obtain the static ?? .???? attribute according to (12). Consequently, it seems that we only need to feed the HR video to the decoder and slightly modify the decoder to fulfill the computation of ?? .????. However, we identify two challenges of this method, with the former one applicable to all codecs and the latter one specific to codecs supporting invisible frames (e.g., VP8, VP9, and AV1). First, the encoding process for the HR video and that for the LR video are independent. Considering an inter-coded block $b _ { i n t e r } ^ { i }$ ?? ?????? in the LR video and its corresponding block $b _ { i n t e r } ^ { i } . H R$ in the HR video, the two blocks may share different reference indices or irrelevant motion vectors due to the independent encoding processes. Feeding the HR video to the decoder, the decoder can only obtain $b _ { i n t e r } ^ { i } . H R . r e f$ , the reference block of $b _ { i n t e r } ^ { i }$ .???? in the HR video, rather than $b _ { i n t e r } ^ { i } . r e f . H R$ , the block in the HR video that corresponds to $b _ { i n t e r } ^ { i } . r e f$ in the LR video. Yet, feeding both the LR video and the HR video to the decoder contradicts the conventional functionalities and structures of existing decoders. Second, codecs like VP8, VP9, and AV1 use invisible frames to achieve an effect similar to bi-directional prediction in H.26X codecs. As the encoding processes for the LR and HR video are independent, an invisible frame may not have a corresponding invisible frame in the HR video.

![](images/dc29fd130571c51ffdda18edbb0ae12bd694b36b3fa9b4e7ac914fc2145161fa.jpg)



Figure 6: Determining the value of the static TC attribute.

To sidestep the two challenges, we propose to approximate the complexity of an inter-coded residual via

$$
b _ {\text { inter }} ^ {i}. \text { res.complexity } \tag {16}
$$

$$
= | | i n t e r p (b _ {i n t e r} ^ {i}. r e s, s c a l e) - (b _ {i n t e r} ^ {i}. H R - b _ {i n t e r} ^ {i}. r e f. H R) | | _ {2} ^ {2}
$$

$$
\approx | | i n t e r p (i n t e r p (b _ {i n t e r} ^ {i}. r e s, 0. 5), 2) - b _ {i n t e r} ^ {i}. r e s | | _ {2} ^ {2}
$$

and approximate the complexity of an intra-coded block via

$$
b _ {\text { intra }} ^ {i}. \text { complexity } \tag {17}
$$

$$
= | | i n t e r p (b _ {i n t r a} ^ {i}. L R, s c a l e) - b _ {i n t r a} ^ {i}. H R | | _ {2} ^ {2}
$$

$$
\approx | | i n t e r p (i n t e r p (b _ {i n t r a} ^ {i}. L R, 0. 5), 2) - b _ {i n t r a} ^ {i}. L R | | _ {2} ^ {2}
$$

We base our approximation on the following observation: if some content (i.e., ?????????????? . $( i . e . , b _ { i n t r a } ^ { i } . H R )$ or some residual $( i . e . ,$ $b _ { i n t e r } ^ { i } . H R - b _ { i n t e r } ^ { i } . r e f . H R )$ ?? ?????????? is of high texture complexity, its?? ?? downsampled version $( i . e . , b _ { i n t r a } ^ { i } . L R$ or $b _ { i n t e r } ^ { i } . r e s )$ also tends to have high texture complexity.

With the above approximations, we can determine the P.TC attribute by only resorting to data in the LR video. We slightly modify the decoder to fulfill the computation process. The workflow is shown in Fig. 6. While decoding a coded block $b ^ { i } \left( \pmb { \mathbb { \bullet } } \right)$ , it computes either the complexity of its content or its residual, based on its coding type, and then adds the value to ?? .???? (➏), where ?? is the patch containing the block. In the case of intra-coding $( \pmb { \Theta } ) , b _ { i n t r a } ^ { i }$ .???????????????????? (➌) is computed from the decoded $b _ { i n t r a } ^ { i } . L R .$ , following the equation (17). In the case of inter-coding $( \pmb { \Theta } ) , b _ { i n t e r } ^ { i }$ .??????.???????????????????? (➎) is computed from the parsed $b _ { i n t e r } ^ { i } . r e s$ ?????????????? .??????, following the equation (16).

# 5 PARALLEL SEARCHING

# 5.1 Performance Analysis

We employ a greedy searching algorithm to iteratively select anchor patches based on the estimated quality. We refer to the sequential implementation of this method as the vanilla Palantír. Specifically, the estimation processes for different anchor patch sets are executed sequentially, and the error attributes for different patch nodes under a given anchor patch set are also computed sequentially. As demonstrated later in Sec. 6, the vanilla Palantír meets the first goal but fails the second goal.

![](images/da15d8f6b50d0707a5113a664b438c34816b54bba594ea517107e6cad44494d1.jpg)



Figure 7: A case study of quality estimation, with ???? · ???? = 15 and $F _ { 0 }$ being a reference frame of $F _ { 1 }$ . Sub-graphs are marked with different numbers and colors.

To improve the scheduling latency, an intuitive method is to introduce parallelism into the DAG-based estimation process. However, the complex reference relationship among patches leads to a highly irregular DAG structure, making it challenging to simultaneously guarantee correctness, parallelism, and data locality of computation. We conduct a case study to demonstrate this. For simplicity, we use only the first two frames of an LR segment to construct an SR error DAG (shown in Fig. 7) and identify two challenges.

• First, to ensure the correctness of quality estimation, the error attribute of any non-anchor node can be computed only after the error attributes of all its predecessor nodes are computed. The process can be parallelized by processing different nodes in different threads, only if there exists no directed path from one node processed in some thread to another node processed in another thread; otherwise, the correctness requirement may be violated. As shown in Fig. 7, we can divide the DAG into nine disconnected sub-graphs and process different sub-graphs in different threads. However, each sub-graph is rather small due to the sparse connections among patches, making it challenging to effectively utilize the SIMD features of modern CPUs.

• Second, while configuring data used by an individual thread to ensure memory locality is fairly straightforward, the scenario becomes more complex when multiple threads access data from various sub-graphs. It requires an intricate thread-synchronization mechanism to maintain memory locality throughout the execution of multiple threads.

# 5.2 Parallelism Solution

We propose a novel strategy to enable parallel searching in Palantír. The parallelized Palantír can generate the same anchor patch set as the vanilla Palantír as its parallelism mechanism does not hurt the correctness of the computation. As demonstrated later in Sec. 6.3 and 6.4, the parallelized Palantír improves the DAG-based selection latency by more than 200 times and meets the two design goals simultaneously.

For clarity, we continue with the above case study in Sec. 5.1 to introduce our parallelism mechanism. As shown in Fig. 7, edges always start from some patch in $F _ { 0 }$ and point to some patch in $F _ { 1 }$ . There exist neither edges along the opposite direction nor edges connecting patches within the same frame. We will utilize this phenomenon to optimize Palantír via both intra-set and inter-set parallelism. Note that the observed phenomenon is not accidental: edges indicate inter-frame coding references, and the coding reference relationship among frames is directed and acyclic in most codecs. Therefore, our optimization should be applicable to many codecs.

Intra-set parallelism. Based on the above phenomenon, we can follow the frame decoding order to enumerate the DAG for quality estimation, i.e., firstly compute the error attributes for the nodes in $F _ { 0 }$ and then deal with the nodes in $F _ { 1 }$ . The TC attributes of nodes in $F _ { 0 }$ (or $F _ { 1 } )$ can be denoted as a vector $T C _ { 0 }$ (or ????1). Similarly, we use the notation $E r r o r _ { i }$ for the error attributes and $I s _ { \scriptscriptstyle - }$ \_??????ℎ?????? for the is\_anchor attributes $( i = 0 , 1 )$ . The weight attributes of the edges can be denoted by a sparse ?? ??????ℎ?? matrix. Note that the ?? ??????ℎ?? matrix is sparse since each patch in $F _ { 1 }$ only refers to a limited set of patches in $F _ { 0 }$ due to the temporal locality of videos. The computation process can be formalized as ???????? $r _ { 0 } = T C _ { 0 } \circ$ ????\_??????ℎ?? $r _ { 0 }$ and $E r r o r _ { 1 } = \left( T C _ { 1 } + \right.$ ?? ??????ℎ?? · ??????????0) ◦????\_??????ℎ????1, where ◦ indicates the elementwise multiplication and ?? ??????ℎ?? · ??????????0 is a parallelizable sparse matrix-vector multiplication (SpMV) operation. Although the concurrent attainment of correctness, parallelism, and data locality for SpMV operations are also challenging, SpMV itself is a common operation in many application files and thus attracts many research and engineering efforts [19, 30, 41]. Consequently, parallelized SpMV can be simply achieved by using a mainstream matrix-related computation package such as PyTorch.

Inter-set parallelism. Batching is widely used to improve DNN inference throughput [7] due to the effect of the data dimension on parallelism opportunities [6, 33]. Therefore, we execute the quality estimation under several searched anchor sets in parallel by adding a batch dimension to both ???????????? and ????\_??????ℎ??????. The same ?? ??????ℎ?? matrix and ?????? vectors are shared among different samples in the batch. With the inter-set parallelism, the SpMV operations are converted into the sparse matrix-matrix (SpMM) operations, which are also well studied and supported for parallel implementation.

# 6 EVALUATION

We evaluate Palantír by answering three questions:

• Does Palantír achieve the first design goal of selecting a beneficial anchor patch set and improving the efficiency of neural-enhanced UHD live streaming?

• Does Palantír achieve the second design goal of incurring a negligible latency overhead for UHD live streaming?   
• How does each component of Palantír contribute to its overall performance?

# 6.1 Experimental Setup

Implementation. We develop our decoder based on the open-source SR decoder in NEMO [42]. We incorporate two novel modes into the decoder. The first is to obtain the data required for graph construction (as introduced in Sec. 4.3). The second is to take both an LR video and a corresponding cache profile as input, and then upscale patches by either SR DNNs or reusing-based SR based on the cache profile. The source code is available at https://palantir-sr.github.io.

Hardware. We use a server with a 16-core AMD Ryzen processor as our media server, where graph construction and anchor selection are performed. The scheduling latency is measured on the server. We use a Xiaomi 12S smartphone, which was announced in July 2022 and equipped with the Qualcomm Snapdragon 8+ Gen 1 Mobile Platform, to measure the energy efficiency when running SR DNN inference on mobile receiver devices.

Video. We download six popular 4k@30fps videos from YouTube. To demonstrate the universality of Palantír, the videos contain six distinct categories, including makeup review, computer gaming, skit, shopping, car review, and unboxing. We use FFmpeg (v3.4) [4] to transcode the HR video into the 480p (854 × 480) LR version in real time. We follow encoding guidelines to set the bitrate to 1800 kbps, the encoding speed to 5 [2], and the group of pictures (GoP) to 60 frames (i.e., 2 seconds) [40]. We use the -auto-alt-ref option in FFmpeg to enable the alternative reference frame feature required by the anchor selection algorithm in NeuroScaler. Unless noted otherwise, We use the first five minutes of each video in our evaluation.

SR DNN. We adopt the DNN model of NAS [43]. We empirically set the number of residual blocks to 8 and the number of filters to 48. The DNN upscales the resolution of the LR video by 4 times. As the feasibility of online training for live streaming has been demonstrated [29], we train the DNN model for each benchmark video. When comparing the performance of different methods on the same video, the same DNN model is used for fairness.

Anchor patch size. We use a patch size of 170 × 160 to compensate for energy efficiency and latency. Consequently, each LR frame consists of 15 patches.

Baselines. We use three baselines in this part. The first is the Per-frame baseline, which applies DNN-based SR on all the frames. The second is the NeuroScaler baseline, which uses the algorithm in NeuroScaler [44] to select the anchor frame set. The third is the Key+Uniform baseline, which selects all the patches in the keyframe and equally spaced patches in the remaining frames as anchor patches.

![](images/2836b47330e38d0fae1bfdbb6c356b5e2447e73235fd51223df8fd1f79f28de9.jpg)



(a) Setting: ?? = 1.

![](images/04fb6694fb4ff27ab0cd9c832b93e5c7de882a148187343adf080f4af0f7462f.jpg)



(b) Setting: ?? = 2.

![](images/7d696f4592ba46c732a53c4a681899fa47c09970ca9102e3b6fdea70b21fa7d7.jpg)



(c) Setting: ?? = 3.   
Figure 8: A comparison of anchor effectiveness.

Scheduling interval. Unless otherwise noted, we use a scheduling interval equal to the GoP (i.e., 2 seconds).

Parallelism. The parallelized Palantír and the vanilla Palantír are two different implementations of the same selection method and lead to the same anchor patch set, so the results in Sec. 6.2 apply to both implementations. The latency results in Sec. 6.3 are obtained using the parallelized Palantír. Finally, the two implementations are compared in Sec. 6.4.

# 6.2 Anchor Effectiveness

Quality Gain. We compute the peak-signal-to-noise-ration (PSNR) between the SR video and the original HR video to quantify the effectiveness of an anchor set. To make a fair comparison, we keep the total sizes of the anchor regions the same, i.e., compare the quality gain under the ??-ary anchor frame set selected by the NeuroScaler baseline with that under the (15 · ??)-ary anchor patch set selected by Palantír or the Key+Uniform baseline. The only exception here is the Per-frame baseline, where all the frames are always treated as anchors and the size of the anchor regions is thus always larger than other methods. Furthermore, we empirically limit ?? to not be greater than 3 since: (1) ?? = 3 can deliver quality gains that are comparable to the setting of applying DNNbased SR on all frames; (2) further increasing the value of ?? leads to a limited benefit yet a significant overhead.

![](images/b91225c4cd0d4861f81c71454f5db24ea9d80a2c8030c45a0f4ee1b3c461498a.jpg)



(a) Setting: 1 anchor frame / 15 anchor patches.

![](images/d36f64950d375723f1b153e5ae96b8ddb7ddbd90bf3ca914308b7efe2f577bdc.jpg)



(b) Setting: 2 anchor frames / 30 anchor patches.

![](images/c9640424cb29737861379154b17f845f5fd2b2f9697f8e2ccc891c0a8b49a963.jpg)



(c) Setting: 3 anchor frames / 45 anchor patches.   
Figure 9: A comparison of energy overhead.

The results are shown in Fig. 8, from which we have three observations: (1) Palantír consistently outperforms the NeuroScaler baseline and the Key+Uniform baseline with its ability to identify beneficial patches. Palantír boosts the quality gain of neural enhancement by 3.7 times at most and 1.4 times on average than the NeuroScaler baseline, or by 3.7 times at most and 1.7 times on average than the Key+Uniform baseline. (2) The fine-grained scheduling-based Key+Uniform baseline even falls behind the coarse-grained schedulingbased NeuroScaler baseline, so the effect of fine-grained scheduling heavily depends on the anchor selection method. (3) Palantír reduces the SR DNN inference overhead by 20 times with ?? = 3 (or 60 times with ?? = 1) while compared to the Per-frame baseline. With such a remarkable overhead reduction, Palantír still preserves 54.0-82.6% (or 32.8-64.0%) of the quality gain of the Per-frame baseline.

Energy Efficiency. We now examine how the anchor efficiency of Palantír transfers to energy efficiency when running the SR decoder on mobile devices. We enable the developer mode on the Xiaomi 12S smartphone and record the average current over a specified period using the built-in power monitor software. The detailed energy consumption measurement method is presented in § A.1.

![](images/822071290180d726f3bf8942a2359de30ee7a020a17ee7cb85b5e5c3c8d535a2.jpg)  
Figure 10: The ratio of the monetary cost of Palantír to that of the NeuroScaler baseline.

For each anchor frame set ???? selected by the NeuroScaler baseline, we find the minimal anchor patch set ???? which is selected by Palantír and achieves an equivalent or higher PSNR than ???? . We compare the energy overhead under ???? with that under ????. As shown in Fig. 9, Palantír reduces the energy overhead over all cases. The reduction ratio is 38.1% at most and 22.4% on average.

Monetary cost reduction. We now present how Palantír reduces the monetary cost when running the SR decoder on cloud servers. We use the same method as measuring energy efficiency to find the corresponding ???? for every ????. The monetary cost is estimated to be linear to the DNN computation complexity under the cache profile (???? or ????), and the keras-flops package [1] is used to measure the computation complexity. The ratio of the monetary cost incurred by Palantír to that incurred by the NeuroScaler baseline is presented in Fig. 10. Compared to NeuroScaler, Palantír reduces the monetary cost by 80.1% at most and 38.4% on average.

# 6.3 Scheduling Latency

End-to-end (E2E) latency is an important metric in live stream ing [9, 16, 20, 37]. To ensure that the live streaming latency can be lower than the GoP, modern streaming standards such as CMAF [26] allow a chunk (which can be part of a GoP) to be immediately packaged (i.e., chunked packaging [12]) and delivered $( i . e . ,$ chunked delivery [12]) when ready. Here we denote the chunk length as ?? frames and assume the scheduling interval of Palantír to be equal to ?? for simplicity. As shown in Fig. 11, the streamer contributes new video frames at a constant rate. Every new chunk of ?? frames is contributed per time duration of $\begin{array} { r } { L _ { 1 } = \frac { n } { f r a m e \_ r a t e } } \end{array}$ . In traditional streaming pipeline without neural enhancement, the new chunk can be immediately packaged and delivered at $t _ { 1 }$ . However, two additional latency sources are presented in Palantír, i.e., the DAG construction latency $L _ { 2 }$ and the DAG-based anchor selection $L _ { 3 }$ . We evaluate whether $L _ { 2 } + L _ { 3 }$ is small enough to well support latency-sensitive UHD applications.

We first examine the value of $L _ { 2 } .$ . Note that we can directly feed a newly contributed frame to the decoder (working in the first mode introduced in Sec. 6.1) for DAG construction, so $L _ { 2 }$ should be equal to the processing latency of the last frame in the scheduling interval if the decoder runs above

![](images/98bc6dcd7335cb6ab776606a82232c7f903bb511d75e8f78749cc92da2a48d0c.jpg)



Figure 11: The timeline of Palantír. The numbers within the blocks represent the frame indices.

![](images/cb853d6c4133732e5cefda72456ba06e93f76491078da485d00c38a37af2a771.jpg)



Figure 12: Per-frame latency of decoding for DAG construction during a GoP.

30fps. As shown in Fig. 12, the measured per-frame decoding latency for DAG construction is indeed always below 33 ms, so we estimate $L _ { 2 }$ to be the average of the measured per-frame decoding latencies in Fig. 12, i.e., 7.2ms.

The DAG-based anchor selection latency $L _ { 3 }$ depends heavily on the scheduling interval and the number of selected anchor patches per scheduling interval. For ULL UHD live streaming applications [37] requiring an E2E latency below 200ms, we set the scheduling interval to be 66.67ms (i.e., 2 frames in the 30-fps evaluation videos). As for LL live streaming applications [9, 16, 20] whose E2E latency requirements range from 2 seconds to 10 seconds, we consider five different settings (with the latency requirement being 2s, 4s, 6s, 8s, and 10s, respectively) and set the scheduling interval to be one-fifth of the latency requirement under each setting. As illustrated in Sec. 6.2, using only 5% of all the patches as anchor patches can lead to large quality gains, so we set the ratio of searched anchor patches to be 5% for latency measurement. Under the above settings, the relationship between the overall scheduling latency $L _ { 2 } + L _ { 3 }$ (with $L _ { 2 }$ fixed to 7.2ms) and the E2E latency requirement is measured and plotted in Fig. 13. In all the settings of LL UHD live streaming, the overall streaming latency is less than 2.5% of the E2E latency requirement. As for the case of ULL live streaming, the scheduling latency is 11.3ms and accounts for about 5.7% of the E2E latency requirement.

# 6.4 Ablation Study

SR error DAG. The key to selecting a beneficial anchor patch set is our DAG-based modeling. We use a theoretical analysis to determine the values of the static weight attributes of the edges and the static TC attributes of patch nodes (see Sec. 4.2 and 4.3) . To quantify the importance of setting appropriate values, we evaluate with the makeup review video and compare Palantír with two variants. In the first variant (Palantír w/o weight), the only predecessor node of the patch node $P _ { n } ^ { i , j }$ (located at the ??-th row and ?? -th column of the patch grid of the ??-th frame) is $P _ { n - 1 } ^ { i , j }$ ??−1 and the weight of the edge connecting them equals 1. However, the TC attributes in the first variant are kept the same as in Palantír. Note that the first variant resembles the NeuroSclaer baseline when the patch size equals the frame resolution. In the second variant (Palantír w/o TC), the weight attributes are kept the same as in Palantír, but the TC attributes of all nodes are set to 1. As shown in Fig. 14(a), Palantír consistently outperforms the two variants.

图 Overall Scheduling LatencyE2E Latency Requirement   
![](images/cd67d7ca6f0c7459eae6a613a52718c600ec36396c606ca734d173f40d893439.jpg)



Figure 13: The relationship between the overall scheduling latency and the E2E latency requirement.

![](images/6622113a211517a3c91bb27f09a755530432d45c0bcf85326b065cbaad253cf6.jpg)



(a) Analysis on the DAG’s (b) Analysis on the paralattributes. lelism mechanisms.   
Figure 14: Ablation study.

Parallel Searching. We have introduced intra-set and inter-set parallelism (see Sec. 5) to speed up the quality estimation process in our greedy searching algorithm. We measure the DAG-based anchor selection latency (i.e., ??3) under three different settings: (1) the vanilla Palantír- nodes in the original DAG are processed serially for estimation; (2) the partially optimized Palantír setting - only the intra-set parallelism is enabled; (3) the optimized Palantír- both the two parallelism mechanisms are enabled. The relationship between the number of anchor patches per scheduling interval and the DAG-based selection latency $L _ { 3 }$ is shown in Fig. 14(b). The optimized Palantír consistently speeds up selection by above 200 times than the vanilla Palantír.

# 7 LIMITATIONS AND FUTURE WORK

Exploring a smaller patch size. A natural method to further improve the efficiency of neural enhancement is to use a smaller patch size. However, this method leads to a larger DAG and increases the latency of anchor selection. Potential remedies may be pruning the constructed DAG.

# 8 RELATED WORK

Model Compression. Model compression has been utilized in many video super-resolution systems such as OmniLive [35] and Microsoft Edge VSR [32]. Considering the heavy energy overhead of SR DNNs, it is reasonable to integrate both model compression and resuing-based SR to build a practical system.

# 9 CONCLUSION

In this work, we propose Palantír, the first neural-enhanced UHD live streaming system with fine-grained patch-level scheduling. Palantír seeks to improve efficiency via reasonable scheduling while minimizing the scheduling latency to better support live streaming. Based on our pioneering and theoretical analysis, Palantír adopts DAG-based quality estimation to select a beneficial anchor patch set with low computation cost. The per-frame computation sub-procedure of the estimation method is further refactored to facilitate parallelization and acceleration and significantly decrease the scheduling latency. The evaluation findings indicate that Palantír effectively optimizes the efficiency of neural enhancement and fits the latency requirement of UHD live streaming.

# A APPENDIX

# A.1 Energy Measurement

Here we explain how we measure the energy overhead under a given anchor set. We use the Android Debug Bridge (adb) over Wi-Fi [3] to execute the decoder in the smartphone’s shell. We do not use adb over USB as connecting the smartphone to an external computer via USB automatically charges the smartphone battery and affects the measured current value. Our setting adheres mostly to the guidelines in [39] for reproducibility, except that the Wi-Fi module is turned on for adb. To remove the impact of the display screen, native daemons, and Wi-Fi interfaces in our measurements, we first record the average current $C _ { 1 }$ before the decoder is executed and then record the average current $C _ { 2 }$ during the execution of the decoder. We also record the duration of decoding, ?? , and compute the energy overhead of neuralenhanced decoding as $\left( C _ { 2 } - C _ { 1 } \right) \times T$ .

# REFERENCES

[1] [n. d.]. keras-flops · pypi. https://pypi.org/project/keras-flops/, last accessed on Jun. 26, 2024.   
[2] 2023. Live encoding with VP9 using FFmpeg. https://developers.goo gle.com/media/vp9/live-encoding, last accessed on Mar. 15, 2024.   
[3] 2024. Android Debug Bridge (adb) | Android Studio. https://developer. android.com/tools/adb#connect-to-a-device-over-wi-fi, last accessed on Mar. 15, 2024.   
[4] 2024. FFmpeg. https://ffmpeg.org/, last accessed on Mar. 15, 2024.   
[5] 2024. webm/libvpx - Git at Google. https://chromium.googlesource. com/webm/libvpx, last accessed on Mar. 15, 2024.   
[6] Martín Abadi, Paul Barham, Jianmin Chen, Zhifeng Chen, Andy Davis, Jeffrey Dean, Matthieu Devin, Sanjay Ghemawat, Geoffrey Irving, Michael Isard, Manjunath Kudlur, Josh Levenberg, Rajat Monga, Sherry Moore, Derek G. Murray, Benoit Steiner, Paul Tucker, Vijay Vasudevan, Pete Warden, Martin Wicke, Yuan Yu, and Xiaoqiang Zheng. 2016. TensorFlow: A System for Large-Scale Machine Learning. In 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16). USENIX Association, Savannah, GA, 265–283.   
[7] Ahsan Ali, Riccardo Pinciroli, Feng Yan, and Evgenia Smirni. 2020. BATCH: Machine Learning Inference Serving on Serverless Platforms with Adaptive Batching. In SC20: International Conference for High Performance Computing, Networking, Storage and Analysis. 1–15.   
[8] Amazon Web Services. [n. d.]. AWS Elemental Link. https://aws.amaz on.com/elemental-link/, last accessed on Jun. 26, 2024.   
[9] Amazon Web Services, Inc. [n. d.]. Video Latency in Live Streaming. https://aws.amazon.com/media/tech/video-latency-in-live-streamin g, last accessed on Jun. 26, 2024.   
[10] Saeed Anwar, Salman Khan, and Nick Barnes. 2020. A Deep Journey into Super-Resolution: A Survey. ACM Comput. Surv. 53, 3, Article 60 (may 2020), 34 pages. https://doi.org/10.1145/3390462   
[11] Duin Baek, Mallesham Dasari, Samir R. Das, and Jihoon Ryoo. 2021. DcSR: Practical Video Quality Enhancement Using Data-Centric Super Resolution. In Proceedings of the 17th International Conference on Emerging Networking EXperiments and Technologies (Virtual Event, Germany) (CoNEXT ’21). Association for Computing Machinery, New York, NY, USA, 336–343.   
[12] Abdelhak Bentaleb, May Lim, Mehmet N. Akcay, Ali C. Begen, Sarra Hammoudi, and Roger Zimmermann. 2023. Toward One-Second La tency: Evolution of Live Media Streaming. (2023). arXiv preprint arXiv:2310.03256.   
[13] Coastal Safety Group. 2021. Beach Cameras and Image Analytics——Coastal Safety Group. https://coastalsaf etygroup.com.a u/news/beach-cameras-and-image-analytics, last accessed on Jun. 26, 2024.   
[14] CommsEase. 2022. AI Super-Resolution. https://doc.commsease.com/ en/nertc/guide/zYzMjc0NTA?platform=android, last accessed on Jun. 26, 2024.   
[15] Chao Dong, Chen Change Loy, and Xiaoou Tang. 2016. Accelerating the Super-Resolution Convolutional Neural Network. In Computer Vision – ECCV 2016, Bastian Leibe, Jiri Matas, Nicu Sebe, and Max Welling (Eds.). Springer International Publishing, Cham, 391–407.   
[16] Field Test Asia Pte. Ltd. [n. d.]. GB/T 28181-2022 English PDF (GBT28181-2022). https://www.chinesestandard.us/products/ GBT28181-2022, last accessed on Jun. 26, 2024.   
[17] Flyability. 2024. Ultimate Guide to Wind Turbine Inspection Techniques. https://www.flyability.com/blog/wind-turbine-inspection, last accessed on Jun. 26, 2024.   
[18] Global Market Insights Inc. 2024. 4K Technology Market, Share & Analysis Report, 2024-2032. https://www.gminsights.com/industryanalysis/4k-technology-market, last accessed on Jun. 26, 2024.

[19] Constantino Gómez, Filippo Mantovani, Erich Focht, and Marc Casas. 2021. Efficiently running SpMV on long vector architectures. In Proceedings of the 26th ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming (Virtual Event, Republic of Korea) (PPoPP ’21). Association for Computing Machinery, New York, NY, USA, 292–303. https://doi.org/10.1145/3437801.3441592   
[20] Google. [n. d.]. Live streaming latency - YouTube Help. https: //support.google.com/youtube/answer/7444635?hl=en, last accessed on Jun. 26, 2024.   
[21] Google. 2024. YouTube recommended upload encoding settings. https: //support.google.com/youtube/answer/1722171?hl=en, last accessed on Jun. 26, 2024.   
[22] Adrian Grange, Peter de Rivaz, and Jonathan Hunt. 2016. VP9 Bitstream & Decoding Process Specification v0.6. https://storage.googleapis.com /downloads.webmproject.org/docs/vp9/vp9-bitstream-specificationv0.6-20160331-draf t.pdf, last accessed on Mar. 15, 2024.   
[23] Peter Hermann. [n. d.]. D.C. police ’Real-Time Crime Center’ launches with live video monitoring. The Washington Post ([n. d.]). https: //www.washingtonpost.com/dc-md-va/2024/04/08/crime-center-dcpolice-video/   
[24] International Olympic Committee. 2022. Beijing 2022 set to be the most immersive Olympic Winter Games yet. https://olympics.com /ioc/news/beijing-2022-set- to-be- the-most-immersive-olympicwinter-games-yet, last accessed on Jun. 26, 2024.   
[25] International Olympic Committee. 2024. Intel unveils AI-Platform Innovation for Paris 2024. https://olympics.com/ioc/news/intelunveils-ai-platform-innovation-for-paris-2024, last accessed on Jun. 26, 2024.   
[26] ISOIEC JTC 1SC 29. [n. d.]. ISOIEC 23000-19:2024 — Multimedia application format (MPEG-A) — Part 19: Common media application format (CMAF) for segmented media. https://www.iso.org/standard/85623.h tml, last accessed on Jun. 26, 2024.   
[27] JDT Developer. 2022. The practice and application of video superresolution technology. https://developer.jdcloud.com/en/article/2267, last accessed on Jun. 26, 2024.   
[28] Kiloview Electronics Co., Ltd. [n. d.]. Kiloview E3 - Kiloview. https: //www.kiloview.com/en/kiloview-e3/, last accessed on Jun. 26, 2024.   
[29] Jaehong Kim, Youngmok Jung, Hyunho Yeo, Juncheol Ye, and Dongsu Han. 2020. Neural-Enhanced Live Streaming: Improving Live Video Ingest via Online Learning. In Proceedings of the Annual Conference of the ACM Special Interest Group on Data Communication on the Applications, Technologies, Architectures, and Protocols for Computer Communication (Virtual Event, USA) (SIGCOMM ’20). Association for Computing Machinery, New York, NY, USA, 107–125. https://doi.org/10.1145/3387514.3405856   
[30] Kenli Li, Wangdong Yang, and Keqin Li. 2015. Performance Analysis and Optimization for SpMV on GPU Using Probabilistic Modeling. IEEE Transactions on Parallel and Distributed Systems 26, 1 (2015), 196–205. https://doi.org/10.1109/TPDS.2014.2308221   
[31] K. O. McGraw and S. P. Wong. 1992. A common language effect size statistic. Psychological Bulletin 111, 2 (1992), 361–365. https: //doi.org/10.1037/0033-2909.111.2.361   
[32] Microsoft Edge Team. 2023. Video super resolution in Microsoft Edge. https://blogs.windows.com/msedgedev/2023/03/08/video-superresolution-in-microsof t-edge/, last accessed on Jun. 26, 2024.   
[33] Graham Neubig, Yoav Goldberg, and Chris Dyer. 2017. On-the-fly Operation Batching in Dynamic Computation Graphs. In Advances in Neural Information Processing Systems, I. Guyon, U. Von Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett (Eds.), Vol. 30. Curran Associates, Inc.   
[34] Ookla, LLC. 2024. Speedtest Global Index - Internet Speed around the world. https://www.speedtest.net/global-index, last accessed on Jun.

26, 2024.

[35] Seonghoon Park, Yeonwoo Cho, Hyungchol Jun, Jeho Lee, and Hojung Cha. 2023. OmniLive: Super-Resolution Enhanced 360° Video Live Streaming for Mobile Devices. In Proceedings of the 21st Annual International Conference on Mobile Systems, Applications and Services (Helsinki, Finland) (MobiSys ’23). Association for Computing Machinery, New York, NY, USA, 261–274.   
[36] Wenzhe Shi, Jose Caballero, Ferenc Huszár, Johannes Totz, Andrew P. Aitken, Rob Bishop, Daniel Rueckert, and Zehan Wang. 2016. Real-Time Single Image and Video Super-Resolution Using an Efficient Sub-Pixel Convolutional Neural Network. In 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 1874–1883.   
[37] Soliton Systems. [n. d.]. Beyond Line of Sight Drones with Ultra Low Latency. https://www.solitonsystems.com/low-latency-video/remoteoperation/beyond-line-of -sight-command-and-control-of -drones, last accessed on Jun. 26, 2024.   
[38] Statista. [n. d.]. Distribution of worldwide YouTube viewing time as of 2nd quarter 2021, by device. https://www.statista.com/statistics/11 73543/youtube-viewing-time-share-device/, last accessed on Sept. 9, 2023.   
[39] Xiaolong Tu, Anik Mallik, Dawei Chen, Kyungtae Han, Onur Altintas, Haoxin Wang, and Jiang Xie. 2023. Unveiling Energy Efficiency in Deep Learning: Measurement, Prediction, and Scoring across Edge Devices Xiaolong. In Proceedings of the 8th ACM/IEEE Symposium on Edge Computing (Wilmington, DE, USA) (SEC ’23). Association for Computing Machinery, New York, NY, USA, 15 pages. arXiv preprint arXiv:2310.18329.

[40] Twitch. 2024. Broadcast Guidelines. https://help.twitch.tv/s/article/b roadcast-guidelines?language=en\_US, last accessed on Mar. 15, 2024.   
[41] Guoqing Xiao, Kenli Li, Yuedan Chen, Wangquan He, Albert Y. Zomaya, and Tao Li. 2021. CASpMV: A Customized and Accelerative SpMV Framework for the Sunway TaihuLight. IEEE Transactions on Parallel and Distributed Systems 32, 1 (2021), 131–146. https://doi.org/10.1109/ TPDS.2019.2907537   
[42] Hyunho Yeo, Chan Ju Chong, Youngmok Jung, Juncheol Ye, and Dongsu Han. 2020. NEMO: Enabling Neural-Enhanced Video Streaming on Commodity Mobile Devices. In Proceedings of the 26th Annual International Conference on Mobile Computing and Networking (London, United Kingdom) (MobiCom ’20). Association for Computing Machinery, New York, NY, USA, Article 28, 14 pages.   
[43] Hyunho Yeo, Youngmok Jung, Jaehong Kim, Jinwoo Shin, and Dongsu Han. 2018. Neural adaptive content-aware internet video delivery. In 13th {USENIX} Symposium on Operating Systems Design and Implementation ({OSDI} 18). 645–661.   
[44] Hyunho Yeo, Hwijoon Lim, Jaehong Kim, Youngmok Jung, Juncheol Ye, and Dongsu Han. 2022. NeuroScaler: Neural Video Enhancement at Scale. In Proceedings of the ACM SIGCOMM 2022 Conference (Amsterdam, Netherlands) (SIGCOMM ’22). Association for Computing Machinery, New York, NY, USA, 795–811.   
[45] ZEGOCLOUD. [n. d.]. ZegoExpressEngine. https://docs.zegocloud.c om/article/api?doc=express\_video\_sdk\_API\~java\_android\~class\~Zeg oExpressEngine#set-play-streams-alignment-property, last accessed on Jun. 26, 2024.