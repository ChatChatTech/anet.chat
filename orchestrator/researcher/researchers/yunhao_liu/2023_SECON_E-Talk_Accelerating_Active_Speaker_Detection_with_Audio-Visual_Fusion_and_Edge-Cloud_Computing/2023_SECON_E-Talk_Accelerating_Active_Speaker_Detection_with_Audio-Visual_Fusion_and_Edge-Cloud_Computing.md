# E-Talk: Accelerating Active Speaker Detection with Audio-Visual Fusion and Edge-Cloud Computing

Xiaojing Yu, Lan Zhang, and Xiang-yang Li

Department of Computer Science, University of Science and Technology of China, Anhui, China

Deqing Alpha Innovation Institute, Zhejiang, China

Emails: yyxjing@gmail.com, {zhanglan, xiangyangli}@ustc.edu.cn

Abstract—Active Speaker Detection (ASD) aims to enhance communication and interaction in various scenarios, including meetings, group discussions, and security surveillance systems. The primary objective of ASD is to identify and label the position of the main active speaker. In large-scale surveillance systems, real-time ASD can pose network congestion issues due to the extensive video data uploaded from numerous cameras. To address this challenge, we propose a collaborative edgecloud solution called E-TALK for ASD. E-TALK leverages the simplicity of voiceprint comparison and processing, as opposed to analyzing video sequences. It utilizes voiceprint consistency as the criterion for determining if there has been a change in the active speaker. Our research focuses on evaluating the performance and computational costs of different voiceprint features and recognition models in speaker identification tasks. Additionally, E-TALK introduces a potential speaker tracking scheme for fixed-angle cameras, in conjunction with foreground extraction algorithms. Moreover, E-TALK incorporates a cloud-based highprecision facial ASD model, which utilizes historical information to determine the active speaker in real-time. We conducted experiments to evaluate the performance of our proposed solution in various scenarios and settings. The results demonstrate the effectiveness of the E-TALK approach in improving active speaker detection, highlighting its potential for practical application in surveillance systems.

Index Terms—active speaker detection, filtering, temporalitylevel stream

# I. INTRODUCTION

Active Speaker Detection (ASD) enhances communication and interaction in a variety of situations, such as meetings, group discussions, and security surveillance systems [1], [2]. ASD can be utilized to generate precise transcriptions of meetings by identifying individual speakers and annotating their corresponding speech segments, thereby simplifying the process of reviewing and analyzing the meeting’s content (Fig. 1). As high-quality microphones, cameras, and audio processing technologies become increasingly accessible, researchers have been investigating methods to identify and track active speakers in real-time. Early approaches primarily focused on audio features, such as voice pitch and energy, to detect speakers [3]. Subsequently, researchers integrated visual cues like lip movements and head poses to enhance accuracy [4]. The emergence of open-source datasets, such as AVA-Active Speaker [1], and advances in deep learning techniques, particularly Convolutional Neural Networks (CNNs) and Recurrent Neural Networks (RNNs) significantly improve the performance of ASD systems [5]. State-of-theart methods employ audio-visual models and capitalize on the interconnectedness between voice and facial modalities to bolster ASD accuracy and stability compared to audio or image-only alternatives [6].

![](images/07294078edcbf4e74725926654d603331fb5dc05eedf8988962ac02733a3ed18.jpg)



Fig. 1. An illustration of the interaction between participants in a seminar. The green bounding boxes represent current active speaker.

Modern surveillance cameras typically capture highresolution video streams (1080p or 4K) at high frame rates (e.g., 25 fps) to ensure smooth video and capture crucial details in fast-moving scenes [7]. A commonly employed computing paradigm nowadays involves the collection of data from edge devices, which is then centralized for processing in the cloud, leveraging its powerful computational capabilities [8]. In largescale surveillance systems with potentially hundreds or thousands of cameras operating simultaneously, the total amount of transmitted data increases, placing considerable strain on available bandwidth [9]. Uploading extensive video data from numerous cameras can congest the network, resulting in increased latency, packet loss, or even network failure, affecting not only the surveillance system but also other services sharing the same network infrastructure [10]. Although video compression techniques, such as H.265 or H.266/VVC [11], can reduce video stream sizes, they are still insufficient for mitigating bandwidth stress in large-scale systems. By performing certain processing tasks of ASD directly on cameras, the amount of data transmitted to cloud servers can be reduced, alleviating bandwidth stress and ensuring smooth surveillance system operation.

Nonetheless, optimizing ASD in surveillance systems using edge devices presents several challenges due to various factors. Firstly, capturing precise facial motion can be difficult when cameras are positioned more than five meters away from a person. Additionally, fixed-angle cameras often struggle to capture a person’s face frontally in different situations. Secondly, deploying complex methods on surveillance cameras is challenging due to limited computational resources, power constraints, and scalability issues. Many existing cameras lack necessary acceleration hardware units, such as GPUs, required for running deep models. Lastly, most current video frame filtering tasks are designed for scenarios where single-frame images can yield accurate judgments, such as counting people or vehicles [12]. Nonetheless, determining the active speaker requires a sequence of video frames, making it challenging to achieve accurate results using only a few sampled snapshots.

In the field of ASD, the position of the main active speaker is labeled at each timestamp. By acquiring the voiceprints of speakers in a scene over time, we can continuously track the position of a single speaker. When the positions of individuals remain relatively stable, comparing their voiceprints enables us to switch to the current speaker’s position. Based on these considerations, we propose E-TALK, a collaborative edge-cloud solution for active speaker detection. Utilizing the simplicity of comparing and processing voiceprints compared to analyzing video sequences, E-TALK leverages voiceprint consistency as the criterion for detecting changes in the active speaker. This research investigates the performance and computational costs of various voiceprint features and recognition models in speaker identification tasks. In conjunction with foreground extraction algorithms, E-TALK incorporates a potential speaker tracking scheme for fixed-angle cameras, allowing for continuous monitoring of the most likely active speakers. Additionally, E-TALK introduces an algorithm that utilizes a cloud-based high-precision facial ASD model to identify the active speaker in real-time using historical data. To evaluate the performance of E-TALK in different scenarios and settings, we conduct experiments that demonstrate the effectiveness of the proposed solution in enhancing active speaker detection. Our main contributions are summarized as the following:

• We introduce a novel edge-cloud cooperative ASD approach that utilizes voiceprint consistency as the primary criterion to simplify speaker detection, incorporating cloud-based high-precision facial recognition models for real-time active speaker identification while minimizing edge device computational resources.   
• We assess various voiceprint features and recognition models for performance and computational costs, enabling the selection of optimal features for the ASD process. Our proposed speaker tracking scheme for fixedangle cameras employs foreground extraction algorithms for continuous speaker tracking.   
• Comprehensive experiments on real-world surveillance videos demonstrate our method’s effectiveness, achieving a 91.88 mAP detection accuracy (a 30% improvement over state-of-the-art) and a 13.12 ms on-camera delay. Our cooperative filtering design saves 90% of frame transmission in computation overhead while maintaining a high detection accuracy of 0.855.

The rest of the paper is organized as follows. We introduce the motivation and related works in Sec. II. Then we summary the system overview in Sec. III. In Sec. IV and Sec. V, we discuss the effectiveness of audio-visual features and filters related to ASD accuracy and latency. Then we zoom in on the cooperation framework between on-device and server resources in Sec. VI. Evaluations and results with the state-ofthe-art solutions are given in Sec. VII. In Sec. VIII, we discuss the limitations of our work and the potential future directions.

# II. RELATED WORK

In this section, we investigate the resources of commodity cameras and the challenges of ASD based on live videos. We review related work on ASD and filtering techniques to gain a comprehensive understanding of this complex task.

# A. ASD based on Camera Resources

With the rapid development of computer vision, resourceequipped cameras have been widely deployed in residential buildings, commercial establishments, and educational institutions. The camera industry has broadened its scope by incorporating state-of-the-art technologies, such as CNNs, into camera products, enabling tasks like person and vehicle detection on the edge. However, due to the financial and logistical challenges of updating large-scale camera systems, a considerable resource gap still exists between state-of-theart and commonly deployed cameras [13]. To emphasize the generality of our method, we focus on low-cost cameras with modest resource constraints, such as embedded CPUs and small memories, instead of cameras with extra processing power like dedicated chips or GPUs. Traditional zero-resource cameras are not included in our design setting as they lack on-camera pre-processing capabilities. Adding peripheral edge computing nodes can turn them into intelligent devices.

Cameras are often installed in obscure corners of an area, making it less accessible and efficient to monitor an individual’s facial movements [14]. Additionally, built-in microphones may not support localization technologies that rely on acoustic sensing [15]. Furthermore, the audio quality of ondevice microphones can vary significantly due to background noise and different installation setups. These issues further complicate the task of providing accurate ASD predictions.

# B. Audio-Visual Active Speaker Detection

Audio-visual ASD jointly leverages audio and visual signals to assign a speech segment to its speaker. The availability of open-source datasets such as AVA-Active Speaker [1] and Voxconverse [16] has spurred research on ASD within the computer vision community. State-of-the-art ASD models [17], [18] typically have a three-part architecture: 1) video embedding, 2) audio embedding, and 3) cross ASD modeling. Researchers focus on the choice and design of audiovisual embedding models and the interconnectivity between audio and visual modalities to improve ASD accuracy and stability compared to their audio-only or image-only counterparts. Since facial movements often accompany speech, facial movement-based methods have shown promising results. TalkNet [6] achieves state-of-the-art performance with a 92.3% mAP in the AVA active speaker detection challenge. It employs sentence-level audio-visual information to explore audio-visual inter-modality interaction and synchronization.

Besides facial features, upper-body movements are considered effective cues for detecting potential speakers. Shahid et al. [19] propose S-VVAD for visual-voice activity detection. S-VVAD learns body motion cues related to speech activity by modeling motion directly without a skeleton detector. Despite that, body movement-based performance is less robust due to the weaker correlation between body motion and speaking activities compared to facial movements.

# C. On-Camera Video Filters

On-camera filters aim to mitigate computational overheads and network bottlenecks between cameras and servers by harnessing currently unused resources on the camera. Previous studies have designed low-cost and scalable video processing systems for edge and cloud environments [12]. Piyush et al. [20] introduce a dynamic micro-batch video windowing approach that supports complex event processing queries, striking a balance between edge resource costs and bandwidth savings. Authors in [13] investigate the performance of various low-level video features that extract frame differences for different filter tasks to reduce edge-to-cloud traffic. With suitable feature selection, they propose a lightweight machine learning technique and a cluster-based model for determining the threshold based on the correlation between the feature thresholds and query accuracy. However, existing lightweight video filtering technologies primarily concentrate on imagerelated tasks, such as object detection and vehicle counting.

Cutting-edge video sampling techniques for temporal action recognition focus on minimizing redundant information in video sequences while retaining discriminative features crucial for accurate action recognition. Existing works sample frames from both temporal redundancy [21] and spatial redundancy [22] perspectives, predominantly employing reinforcement learning and deep neural networks as foundational tools. These methods involve high computational complexity and demand significant processing power to perform real-time video analysis, making them unsuitable for deployment on edge cameras with limited resources.

# III. SYSTEM OVERVIEW

The system setting of E-Talk consists of the following components: i) A camera equipped with real-time video and audio recording capabilities is fixed in an area where multiple people can talk and move freely without any pre-defined patterns. ii) The camera transmits data to the server with a bandwidth stream limitation. The server utilizes the received data to detect active speakers. The ASD prediction results are stored and can be queried on the cloud server. iii) The server has the ability to transmit data to the camera in real-time subject to the same bandwidth limitations.

Fig. 2 illustrates the workflow of E-Talk, which operates through a series of steps involving live audio stream processing (Sec. IV), speaker tracking (Sec. V), key crop and audio feature generation, and server-side processing (Sec. VI) to achieve efficient and accurate active speaker detection:

![](images/51d6c19b32808dc7ec6ec68cb1f559d3298a8e59c1e74b9784b2489c7ff68246.jpg)



Fig. 2. Workflow of E-Talk

1) As the camera records the live audio stream, the voiceprint extractor continuously generates specified lowlevel audio features reflecting the identification of speakers. The voiceprint recognition function segments audios with dynamic profiles returned by the filter tuner.   
2) The speaker tracking module continuously tracks potential speakers in consecutive frames, generating bounding boxes around them. It then obtains the current speaker characteristics from the filter tuner.   
3) The filter generates key crops and corresponding audio features based on pre-defined filter rules and uploads them to the server.   
4) Upon receiving the date, the server runs the ASD pipeline to produce real-time predictions. The results are stored in datasets for subsequent filter adjustment. Meanwhile, the filter trainer adjusts the filter model and parameters based on real-time results and sends the adjustments back to the camera for implementation.

# A. ASD Problem Definition

Formally, the data available to the ASD pipeline at timestamp t is denoted as set $X _ { t } = \{ \langle v _ { 1 } , a _ { 1 } \rangle , \colon \colon , \langle v _ { t } , a _ { t } \rangle \}$ , where $v _ { t }$ contains body crops for visible people and $a _ { t }$ is the audio samples corresponding to the duration of $v _ { t }$ . The evaluation metric is the mean average precision (mAP) of correctly labeling the active speaker’s body track at $v _ { t }$ . The mAP is calculated by the average area under the Receiver Operating Characteristic curve (auROC) among classified classes [1]. The Intersection-Over-Union (IOU) threshold between predicted and true bounding boxes is 0.5. Remarkably, we use body crops instead of face crops that are used in previous ASD research. Since the skeleton detection model is quite reliable, we assume that the body detection method of the on-server ASD pipeline can obtain correct body crops corresponding to all potential visible speakers. Given the input data, the objective of ASD is to produce a vector $y _ { t } = \{ y _ { t , 1 } , y _ { t , 2 } , \cdot \cdot \cdot , y _ { t , k } \}$ , where $y _ { t , i } \in [ 0 , 1 ]$ is the confidence value that the i-th speaker is detected as speaking at timestamp t.

# B. Design Scope

The design objectives of the E-Talk system revolve around delivering optimal performance for ASD through a synergy of edge computing and server-side processing. To accomplish this, the system is tailored to meet the following requirements:

• ASD accuracy: A critical aspect of the E-Talk system is its accuracy in identifying active speakers. Our goal is to surpass the state-of-the-art performance in surveillance camera datasets.

• Latency: The latency consists of the computation latency and communication latency. Since the system configurations and the wireless network influence the communication cost, we mainly focus on optimizing the computation latency.   
• Filtering Rate: Since audio signals consume much less bandwidth than video frames, we use the frame filtering rate to represent the performance of bandwidth reduction. Filtering more frames can save resources and reduce communication latency, but it may also lead to a higher risk of incorrect detection. We aim to maximize the filtering rate while satisfying the above conditions.

# IV. VOICEPRINT SEGMENTATION

Voiceprints capture unique characteristics of individuals, enabling effective tracking of active speakers with greater accuracy than frame-based analysis. Voiceprint segmentation involves feature extraction and recognition. Given camera-side resource limitations, complex algorithms can cause delays. Therefore, the selection of features and recognition methods should consider real-time performance and accuracy.

# A. Audio Feature Extraction

Feature extraction aims to obtain relevant and discriminative information from raw audio signals that distinguishes between speakers and filters out background noise. We assess the Pearson correlation coefficient between popular audio features [23] and speaker identification alongside CPU computational latency. A larger absolute Pearson correlation coefficient value indicates a stronger correlation. Additionally, we evaluate the deep network voiceprint generation model ECAPA [24]. Test audios comprise ten speakers, lasting an hour; audio clips have a 5s window size and 1s step size. The results are shown in Table I. For multi-dimensional features like Melfrequency Cepstral coefficient (MFCC) and Chroma, we list the maximum value of a single dimension. Results reveal that deep network-based algorithms cannot operate in real-time on the camera. MFCC demonstrates the highest correlation, maintaining computational latency under 5ms, showcasing its effectiveness in vocal pattern recognition tasks. In our system, we employ a 13-dimension MFCC.

TABLE I PEARSON CORRELATION COEFFICIENT PER CANDIDATE RAW AUDIO FEATURE WITH CPU COMPUTATION TIME 

<table><tr><td>Audio Feature</td><td>Correlation Coefficient</td><td>Latency (ms)</td></tr><tr><td>Energy</td><td>0.022</td><td>0.23</td></tr><tr><td>Zero Crossing Rate</td><td>-0.018</td><td>0.44</td></tr><tr><td>Spectral Entropy</td><td>-0.234</td><td>2.43</td></tr><tr><td>Spectral Roll-off</td><td>-0.017</td><td>2.46</td></tr><tr><td>Spectral Spread</td><td>0.275</td><td>2.57</td></tr><tr><td>MFCC</td><td>0.576</td><td>4.69</td></tr><tr><td>Chroma</td><td>-0.231</td><td>14.71</td></tr><tr><td>ECAPA</td><td>0.591</td><td>223.75</td></tr></table>

# B. Speaker Recognition

Upon extracting features, they are used to train a classifier or recognition model to differentiate speakers. We compute the similarity or distance between the current voiceprint and the previously tracked voiceprints using measures like Euclidean distance, cosine similarity, DTW [25], or GMM likelihood scores [23]. GMMs are unsupervised statistical models often used in speaker recognition tasks due to their ability to model complex distributions.

We initialize and update GMMs through these steps:

1) The camera collects audio data and converts the audio stream into feature vectors. DNN voiceprint models label samples and differentiate speakers.   
2) GMMs for each speaker cluster are initialized with random parameters. We adopt Expectation-Maximization (EM) algorithm to update GMM parameters until convergence or a stopping criterion is met (max 50 iterations).   
3) When the DNN voiceprint model cannot provide a good estimate for the number of clusters due to environmental noise and the overlap of multiple voices, we apply the Bayesian Information Criterion (BIC) [26] to determine the optimal number.   
4) When the probability of sample occurrence for any GMM cluster is below a threshold, we add it to the training buffer. Once the buffer reaches the given value, it is uploaded to the cloud. The server divides existing weights by a factor larger than one (1.7 in our setting) and applies the EM algorithm to re-estimate GMM parameters.

When a new audio segment arrives, we use GMMs and a dynamic threshold to obtain speaker segments, merging short segments (with intervals less than 0.5s) to refine speaker boundaries and improve segmentation quality.

To label samples and distinguish speakers in the cloud, we use the state-of-the-art DNN embedding model, ECAPA [24]. ECAPA is a Time Delay Neural Network (TDNN)-based embedding extractor for speaker verification, built on the xvector architecture. Incorporating squeeze-and-excitation (SE) blocks and ResNet features, also used in the AVA detection model TalkNet [6], significantly enhances its performance over baseline designs. The resulting voiceprints exhibit a property wherein a dot product of two voiceprints closer to 1 indicates greater similarity between the speakers of the samples. Upon obtaining a voiceprint, we compare it with a past speaker’s voiceprint using a pre-defined threshold (=0.7) to determine if the current speaker matches the previous one, thereby segmenting an audio piece into sections corresponding to different speakers.

# V. FRAME FILTER

In this section, we present two frame filtering techniques. First, we minimize uploads caused by changes in the speaker’s position by tracking potential speakers. Second, we analyze speaker image changes to reduce uploads due to invalid images, such as instances when the speaker consistently faces away from the camera.

# A. Speaker Tracking

Visual Background Extractor (ViBe) [27] is a background subtraction algorithm employed for tracking people in video frames. The algorithm distinguishes moving objects (foreground) from the static background, facilitating people tracking in videos. We propose a lightweight speaker tracking method based on ViBe to generate bounding boxes of potential speakers in surveillance camera video frames.

To initialize the background model for each pixel in the first frame, we randomly select a set of background samples from its neighboring pixels (setting the minimum number to classify background pixels as 10, considering a video frequency less than 25Hz). For subsequent frames, we classify foreground and background pixels by comparing with its corresponding background samples, updating the background model by occasionally replacing random samples with the current pixel or neighboring pixels. Next, we apply morphological operations (e.g., dilation and erosion) to eliminate noise and fill gaps in the detected foreground. We then perform Connected Component Analysis (CCA) [28] on the binary foreground mask to group connected foreground pixels into distinct blobs and compute bounding boxes by identifying the minimum and maximum x and y coordinates in each component. Finally, we filter out small bounding boxes to remove false positives.

After uploading the bounding boxes and crops to the server, body detection models provide the aspect ratio of a person (adopting the 3D pose prediction model projected in [29] due to its low mean error per landmark). We assign a unique ID to each detected person initially. In later frames, we compare new bounding boxes with existing ones using IOU for matching. If a new bounding box does not match any existing ones, we assign a new unique ID to it. We apply a Kalman Filter [30] to improve tracking performance and handle occlusions and temporary disappearances.

The VIBE-based method is computationally efficient, consuming fewer resources for video frame processing compared to state-of-the-art tracking studies [31]. This suitability for edge device deployment results in lower latency.

# B. Image Filter

In real-world applications, determining if a person is speaking when their face is partially visible presents challenges. Performing speaker recognition tasks on edge nodes is difficult, requiring data upload to a server for detecting potential speakers. To address this, we analyze frame differences to assess the presence of valuable information in the current image. If the uploaded frame lacks sufficient information for analysis, it can be filtered out.

We assess the performance of various image features for face detection within the body bounding box. Table II displays the Pearson correlation coefficients for these features. Our results show that the Area feature provides the best correlation performance while maintaining acceptable latency. Consequently, we set a dynamic threshold for the minimum difference between valid frames. If the time difference between consecutive valid frames is below this threshold, we filter out these frames to reduce the upload frequency.

TABLE II PEARSON CORRELATION COEFFICIENT OF IMAGE FEATURES FOR FACE DETECTION. 

<table><tr><td>Image Feature</td><td>Correlation Coefficient</td><td>Latency (ms)</td></tr><tr><td>Pixel</td><td>-0.505</td><td>0.22</td></tr><tr><td>Area</td><td>-0.541</td><td>1.36</td></tr><tr><td>Edge</td><td>0.000</td><td>1.26</td></tr><tr><td>Corner</td><td>-0.160</td><td>2.85</td></tr><tr><td>Hist Correlation</td><td>0.030</td><td>1.15</td></tr><tr><td>Hist Chi-square</td><td>0.040</td><td>1.15</td></tr><tr><td>Hist Bhattacharyya</td><td>-0.269</td><td>1.14</td></tr><tr><td>Hist Intersection</td><td>0.508</td><td>1.15</td></tr></table>

# VI. E-TALK DESIGN

In this section, we discuss our approach to performing filtering. Firstly, we describe how to use facial DNN model recognition results and voiceprint segmentation for long-term observation to obtain ASD results. Next, we introduce our filtering workflow.

# A. ASD Pipeline

As TalkNet achieves state-of-the-art performance in the AVA active speaker detection challenge [6], we adopt it as our core detection model. Fig. 3 presents the architecture of TalkNet. It initially detects face crops using S3FD [32] to provide ground truth face tracking of speakers. Initially, the model detects face crops using S3FD [32], providing ground truth face tracking for speakers. Specifically, it learns the long-term representation of facial dynamics, denoted as $F _ { v } ,$ from a visual temporal embedding, primarily composed of a ResNet18-based enhancement network and a video temporal convolution block [33]. The audio signals are represented as 13-dimensional Mel-frequency cepstral coefficients (MFCCs). Subsequently, a 2D ResNet34 network with an SE attention module, as proposed in [34], is employed to learn the audio content representation, denoted as $F _ { a } .$ . TalkNet utilizes two cross-attention networks to learn temporal interactions, and a self-attention network serves as the classifier to distinguish between speaking and non-speaking statuses. Since the longterm sequence performance does not improve from 50 to 100 frames of video duration, we set the number of frames for each embedding at 50.

![](images/fb31099da366137365a47be0ec4c162f190c32e73f3997eeeac332f30ba8569c.jpg)



Fig. 3. Architecture of the Adopted AVA Detection Model (TalkNet [6])

The existing AVA model may not provide accurate recognition results because the camera might not capture a person’s face. Conversely, we observe that in most scenes, such as classrooms and conference rooms, the speaker is typically the same person. Considering the invariance of scenes under cameras, we can enhance performance by using long-term and short-term temporal correlation information for targeted tracking. Fig. 4 illustrates the execution workflow of our proposed ASD pipeline.

![](images/354b6744868f761a6997195cd16b5f74edff6813096fe3600bb653a57507217d.jpg)



Fig. 4. An Illustration of the ASD Pipeline

Given the input source $X _ { t } ,$ , we denote the body tracks as $B _ { t } = \{ B _ { 1 } , \cdot \cdot \cdot , B _ { k } \}$ , where $b _ { t , k } \in B _ { k }$ is the bounding box (we set $b _ { t , k } = N o n e$ when speaker k is undetectable in frame k). We set the face detection result of $b _ { t , k }$ is $f _ { t , k }$ , this is, $f _ { t , k } \in$ [0, 1]. The AVA detection model gives a speaking score of $b _ { t , k } .$ , denoted as $s _ { t , k } ,$ if and only if $f _ { t , k } = 1$ . The voiceprint segment process frames into partitions $V _ { i } ,$ i.e., $V \ = \ V _ { 1 } \cup V _ { 2 } \cup V _ { p } ,$ where $V = \{ 1 , 2 , . . . t \}$ . We have $V _ { i } \cap V _ { j } = \emptyset , \forall V _ { i } , V _ { j } \in \bar { V }$ and $i \neq j .$ . The system will store voiceprints of previously identified speakers with a high level of accuracy $( > 9 0 \% )$ . The recognition accuracy of voiceprint segment $V _ { t }$ compared to the voiceprint of speaker m is denoted as $s _ { t , m }$ .

Since we only get the exact predicted score when we detect the face in the body bounding box, we use contextual information to infer the $y _ { t }$ at the current moment t. The inference process of $y _ { t }$ operates within a voiceprint time window $V _ { p }$ that encompasses the current time t. It primarily takes into account whether the speaker’s face has been detected within this voiceprint window, whether the voiceprint of the user has been previously recorded, and the recognition score of matching for the user’s voiceprint.

The inference process is governed by two simple inference rules: 1) When the face of speaker m is detected within the voiceprint window $V _ { p } ,$ we set $y _ { t , m }$ according to the maximum score over $V _ { p } . ~ 2 )$ When the face of speaker m is not detected within the voiceprint window $V _ { p } ,$ two conditions are considered: If the voiceprint of the speaker has not been previously recorded, $y _ { t , m }$ is set to a default value c. If the voiceprint of the speaker has been recorded, $y _ { t , m }$ is determined based on the voiceprint matching degree $s _ { t , m }$ and the time of non-speaking interval $\tau _ { m }$ , i.e., $y _ { t , m } \gets s _ { t , m } - \theta _ { 1 } ( t - \tau _ { m } )$ .

Here, $\theta _ { 1 }$ and c are pre-defined parameters that represent the likelihood of speaking in an unknown state. $\theta _ { 1 }$ represents a scaling factor that adjusts the impact of the non-speaking interval, and c is the value indicating the possibility of speaking when the face of the speaker is not detected. They can be easily fitted through the face-mask analysis, i.e., masking a few face crops of speakers in the server and choose the optimal value when the ground truth of active speaker is known through the AVA detection model.

# B. Cooperative Workflow

Let’s introduce the specific workflow of the filter component, as outlined in Alg. 3. Using voiceprint recognition and speaker tracking, the system identifies the current speaker and tracks them (the system captures frames and truncates audio signals every 0.1 seconds). If the speaker is unidentified or position tracking is unavailable, the information is added to a buffer. The image filter module then assesses the buffer’s content before uploading meaningful information.

Algorithm 3: E-Talk Filter   
Input: Incoming audio and frame source src at camera
Output: current speaker prediction $b_{t}$ and $y_{t}$ 1 Fuction On-CameraFilter(src):
2 Initialize $Speaker_{c}$ from server;
3 while $\langle v_{t}, a_{t} \rangle \leftarrow \text{read}(src)$ do
4 $F_{a,t} \leftarrow MFCC(a_{t})$ ;
5 $Speaker_{t} \leftarrow VoiceprintRecognition(F_{a,t})$ ;
6 $b_{t} \leftarrow SpeakerTracking(v_{t})$ ;
7 if $Speaker_{t}$ is $Speaker_{c}$ and $b_{t,c} \neq None$ then
8 $y_{t} \leftarrow y_{c};$ 9 $b_{t} \leftarrow b_{t,c};$ 10 $F_{a} \leftarrow F_{a} \cup F_{a,t};$ 11 $v \leftarrow v \cup v_{t};$ 12 if ImageFilter(v) is True then
13 $y_{t}, b_{t} \leftarrow Server(F_{a}, v);$ 14 $F_{a}, v \leftarrow None;$ 15 Function Server( $F_{a}, v$ ):
16 $y_{t}, b_{t} \leftarrow LongTermEnsemble(Dataset, F_{a}, v);$ 17 Dataset $\leftarrow Dataset \cup y_{t}, b_{t};$ 18 return $y_{t}, b_{t};$

We first initialize the current speaker variable, Speakerc, from server. As the video and audio streams are continuously read from the source, we process each audio signal, ${ { a } _ { t } } ,$ by computing its MFCC features, $F _ { a , t } .$ . With these features, we utilize the Voiceprint Recognition module to identify the current speaker, Speakert. Subsequently, the Speaker Tracking module is employed to obtain the bounding box, $\begin{array} { r } { \pmb { b } _ { t } . } \end{array}$ , for each speaker present in the current frame, $v _ { t }$ . If the identified current speaker, Speakert, matches the previous speaker, $S p e a k e r _ { c } ,$ and the bounding box, $\boldsymbol { b } _ { t , c } ,$ is not None, we update the current label, $y _ { t } ,$ , and bounding box, $b _ { t } .$ , with the previous label, $y _ { c } ,$ , and bounding box, $\boldsymbol { b } _ { t , c } ,$ respectively. The audio features buffer, ${ \mathbf { } } F a .$ , and the video buffer, v. We apply the Image Filter module to the video buffer, $^ { v , }$ and if it returns True, the audio features buffer, $F _ { a } ,$ and the video buffer, $^ { v , }$ are sent to the server for processing. Upon receiving a response from the server, we obtain the current label, $y _ { t } .$ , and bounding box, $b _ { t } .$ . Then, we reset the audio features buffer, $\mathbf { \nabla } _ { F _ { a } . }$ , and the video buffer, v, to None. This process continues in a loop (repeating steps 4-14) until it is terminated.

# VII. EVALUATION

# A. Methodology

1) Dataset: We introduce the Classroom ASD Dataset, which consists of more than 600+ minutes of video collected from 6 different classrooms. The dataset includes recordings from traditional lecture-style classrooms and interactive classrooms, with half captured by front cameras (as in Fig.5(b)) and the other half by cameras at the back of classrooms (as in Fig. 5(a)). Each discussion video features at least 4 active speakers who speak for approximately equal amounts of time, with up to three speakers active simultaneously. All participants were aware of and consented to the filming. We recruit volunteers to manually annotate bounding boxes for the visible part of a speaker’s body when their head is visible, with a label granularity of 10 fps. The audio is down-sampled to 8 kHz. We use mAP to evaluate the ASD performance.

![](images/bb688bd4f8b078429e5cfa8d32506ef4cf46a83559f56f2837a856052d7e40ed.jpg)  
Fig. 5. An Illustration of Classroom ASD Dataset

The Columbia ASD dataset is a benchmark dataset for ASD [35]. It contains an 87-minute discussion video featuring 5 speakers who take turns speaking. Due to its limited size, the Columbia ASD dataset is only used as a test set. We use the F1-score as the evaluation metric.

2) Implementation: Server components ran on Ubuntu-16.04.1 with 12 CPU cores and 4 NVIDIA TITAN X (Pascal) GPUs. The camera-side E-Talk runs on Jetson TX2 (Dual-Core NVIDIA Denver 2 64-Bit + Quad-Core ARM Cortex-A57 MPCore CPU).

# B. Overall Performance

We compare E-Talk with uniform filtering, random filtering, and the baseline filtering framework Reducto [13]. The same ASD pipeline is employed on the server for all filter implementations. Previous works focused on single image frames, while the ASD task requires temporal information. To ensure fair comparison, all baselines upload a sequence of frames (length=5). For Reducto, we select Area as the lowlevel feature, similar to E-Talk.

![](images/8c0709e02a5b02d18712e96f10110c2148915baa728e115489faf2514a3e6c2c.jpg)



(a) Comparison of mAP

![](images/3336bc7d521ea7c3eb1d352a5a9a2bb44f78b08eab5eba5422521c3fb8869eff.jpg)



(b) Comparison of Latency   
Fig. 6. Comparison of Overall Performance

Fig. 6(a) summarizes the mAP of various filters. E-Talk achieves the best detection performance among filtering rates compared to our baseline filters. At a 90% filtering rate, E-Talk attains an ASD of 0.855, outperforming Reducto (mAP=0.672). Fig.6(b) reveals that E-Talk has higher latency due to speaker tracking and voiceprint segmentation.

# C. Performance of ASD Pipeline

We evaluate the mAP of different ASD pipelines without frame filtering, including TalkNet [6] and ASDNet [2]. TalkNet, the default AVA detection model, uses face tracks and MFCCs as visual and audio inputs. Table III lists the mAP and inference latencies of different ASD pipelines. E-Talk achieves the highest mAP with acceptable latency. Facial image-based DNN models struggle with accurate speaker detection due to invisible faces in most cases. TalkNet achieves a 0.922 mAP for video segments with visible speaker faces, but the average face detection rate when bodies are visible is only 41.69%.

TABLE III MAP AND INFERENCE LATENCY OF ASD PIPELINES. 

<table><tr><td>ASD pipeline</td><td>mAP (Classroom)</td><td>F1-score (Columbia)</td><td>Latency (ms)</td></tr><tr><td>TalkNet</td><td>0.6351</td><td>89.2</td><td>84.7</td></tr><tr><td>ASDNet</td><td>0.6179</td><td>96.2</td><td>68.0</td></tr><tr><td>S-VVAD</td><td>0.8770</td><td>94.0</td><td>37.3</td></tr><tr><td>E-Talk</td><td>0.9188</td><td>96.3</td><td>39.1</td></tr></table>

During the long-term integration process of the E-Talk ASD pipeline, there are two key parameters: c and $\theta _ { 1 }$ , Figure 7 illustrates the mAP values under different parameter settings. The optimal values of c and $\theta _ { 1 }$ are dependent on factors such as the distance between the camera and the speaker, as well as the loudness of the audio. The E-Talk system achieves the highest mAP when $c = - 1 . 1 5$ and $\theta _ { 1 } = 0 . 0 9$ .

![](images/f4715024ae283ebec80c7f87c482eca66da6608eb4a703a69f7fb38cc8fe03d5.jpg)



Fig. 7. Impact of Key Parameters in Long-term Ensemble Process

We examine the minimum data granularity required by the ASD pipeline to meet different accuracy requirements. In our setup, the original frame rate of the pictures is 25 Hz, i.e., the time interval between every two pictures is 0.04s. We test how different frame intervals affect ASD accuracy using facedetectable video clips in Columbia ASD dataset. Fig. 8(a) shows the relationship between frame draw granularity and ASD accuracy. At a 0.2s frame draw interval, the accuracy is 0.89an acceptable rate. To further enhance filtering efficiency, we can opt to draw frames at 0.2s intervals for the video streams uploaded to the server.

We also investigate the impact of different MFCC sampling intervals on ASD accuracy. Fig. 8(b) indicates that sampling MFCC features has a more significant influence than video frames. Accuracy drops to 0.80 with a 0.2s frame extraction interval. Since MFCC data takes up much less storage and bandwidth than images, we do not recommend further MFCC sampling.

![](images/b17420b44881e0efe0df136fa36ecba0c04284cfae4392d23293b231a6621230.jpg)



(a) Impact of Sampling on Frames

![](images/0a722e50cdb0d9f887fe8addb1f9f9073212b54bfcd060718bca4c5e95338908.jpg)



(b) Impact of Sampling on MFCCs   
Fig. 8. Impact of Sampling in ASD Pipeline

# D. Voiceprint Segment

We examine the performance of the voiceprint segment using GMMs as the voiceprint recognition method, focusing on the confidence threshold and input MFCC length. Fig. 9(a) displays the mAP and latency over various MFCC lengths with the optimal confidence threshold. E-Talk can achieve an accuracy of 0.9188 with an audio sample length of 1.8s. Fig. 9(b) presents the performance among different confidence values when the sample length is 1.8s.

![](images/4e6d5a193c8f2238801ddad59ef51b337636602c8015a21456acc1767ffec8e7.jpg)



(a) Impact of Audio Length

![](images/5a8c5bf85c009ef2faf6b793687f950a8341c5b75df1ea5bd37f49639f792a93.jpg)



(b) Impact of Confidence Threshold   
Fig. 9. Voiceprint Segment Performance

Table IV shows the performance of different regression methods for adjusting the voiceprint recognition threshold, focusing on Mean Squared Error (MSE), training latency, and prediction latency. From the results, it is evident that Support Vector Regression (SVR) outperforms other methods across all metrics, with the lowest MSE (=0.123) and relatively low training and prediction latencies (1.124 ms and 1.063 ms, respectively). Though Linear Regression has better latencies than SVR, its MSE is significantly higher (=0.160).

TABLE IV PERFORMANCE OF DIFFERENT REGRESSION METHODS 

<table><tr><td rowspan="2">Regression Method</td><td rowspan="2">MSE (video)</td><td colspan="2">Latency (ms)</td><td rowspan="2">MSE (audio)</td><td colspan="2">Latency (ms)</td></tr><tr><td>train</td><td>predict</td><td>train</td><td>predict</td></tr><tr><td>Linear</td><td>0.079</td><td>0.001</td><td>0.001</td><td>0.160</td><td>0.995</td><td>0.014</td></tr><tr><td>SVR</td><td>0.077</td><td>0.009</td><td>0.012</td><td>0.123</td><td>1.124</td><td>1.063</td></tr><tr><td>AdaBoosting</td><td>0.090</td><td>0.010</td><td>0.001</td><td>0.132</td><td>7.851</td><td>0.110</td></tr><tr><td>K-Neighbors</td><td>0.096</td><td>0.001</td><td>0.001</td><td>0.143</td><td>0.012</td><td>0.102</td></tr><tr><td>RandomForest</td><td>0.114</td><td>0.025</td><td>0.002</td><td>0.151</td><td>20.912</td><td>0.014</td></tr><tr><td>Bagging</td><td>0.117</td><td>0.015</td><td>0.001</td><td>0.152</td><td>10.236</td><td>0.258</td></tr><tr><td>DecisionTree</td><td>0.144</td><td>0.002</td><td>0.000</td><td>0.203</td><td>2.122</td><td>0.010</td></tr></table>

# E. Speaker Tracking

For speaker tracking, we use Multiple Object Tracking Accuracy (MOTA) as a performance metric, with higher values indicating better tracking performance, and average inference latency to measure processing time per sample, with lower values indicating faster execution. Table V shows that while E-Talk’s MOTA is slightly lower than TrackFormer [36] and CenterTrack [37] methods, it achieves the lowest inference latency of 35.4 milliseconds, suggesting E-Talk is an efficient and highly real-time speaker tracking method. TrackFormer and CenterTrack methods have higher MOTA but significantly longer inference latencies (235.1 ms and 156.5 ms, respectively). MHT DAM method [38] has a MOTA performance of 55.9, slightly lower than E-Talk, and an inference latency of 75.3 milliseconds, which is also higher than E-Talk.

TABLE V MOTA AND INFERENCE LATENCY OF SPEAKER TRACKING 

<table><tr><td>Tracking Method</td><td>MOTA</td><td>Latency (ms)</td></tr><tr><td>TrackFormer [36]</td><td>69.7</td><td>235.1</td></tr><tr><td>CenterTrack [37]</td><td>65.8</td><td>156.5</td></tr><tr><td>MHT DAM [38]</td><td>55.9</td><td>75.3</td></tr><tr><td>E-Talk</td><td>57.4</td><td>35.4</td></tr></table>

In frame filtering, a filter modulator is needed to generate a confidence threshold for determining speaker image changes. Table IV lists the performance of different regression methods, with the accuracy of filtering frames set to 100%. The results show that linear regression performs relatively well across all three metrics: it has the lowest MSE (=0.079) and the lowest training and prediction latencies. Although SVR has a slightly better performance in terms of MSE (=0.077) compared to linear regression, its training and prediction latencies are significantly higher than those of linear regression.

# VIII. CONCLUSION

In summary, we introduce an edge-cloud collaborative framework, E-Talk, for real-time active speaker detection under surveillance cameras. The E-Talk solution streamlines the process of active speaker detection by focusing on voiceprint consistency, evaluating voiceprint features and recognition models, employing foreground extraction for potential speaker tracking, and leveraging cloud-based facial recognition to accurately identify the active speaker in real-time. We collect a real-world video dataset for over 600 minutes to evaluate the ASD performance of E-Talk. The results show that E-Talk maintains a 0.855 mAP of ASD with a 90% frame filtering rate. We believe this framework is suitable for multi-modal tasks, providing a practical solution for real-time applications.

There are several possible directions for future work to enhance and expand the capabilities of E-Talk: 1) Improved noise reduction techniques: Investigate and incorporate advanced noise reduction algorithms to better handle real-world environments with various types and levels of background noise. 2) Multi-speaker detection: Extend the system to handle scenarios with multiple simultaneous active speakers, enabling it to accurately identify and track each speaker in more complex situations. 3) Scalability and optimization: Optimize the system to handle larger-scale deployments with numerous cameras and speakers while maintaining its performance and efficiency.

# ACKNOWLEDGMENT

The research is partially supported by National Key R&D Program of China under Grant 2021ZD0110400, Innovation Program for Quantum Science and Technology 2021ZD0302900, China National Natural Science Foundation with 62132018, “Pioneer” and “Leading Goose” R&D Program of Zhejiang 2023C01029, and the Fundamental Research Funds for the Central Universities WK2150110024.

# REFERENCES

[1] J. Roth, S. Chaudhuri, O. Klejch, R. Marvin, A. Gallagher, L. Kaver, S. Ramaswamy, A. Stopczynski, C. Schmid, Z. Xi et al., “Ava active speaker: An audio-visual dataset for active speaker detection,” in IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020, pp. 4492–4496.   
[2] O. Kop¨ ukl ¨ u, M. Taseska, and G. Rigoll, “How to design a three-stage ¨ architecture for audio-visual active speaker detection in the wild,” in Proceedings of the IEEE/CVF International Conference on Computer Vision, 2021, pp. 1193–1203.   
[3] F. Patrona, A. Iosifidis, A. Tefas, N. Nikolaidis, and I. Pitas, “Visual voice activity detection in the wild,” IEEE Transactions on Multimedia, vol. 18, no. 6, pp. 967–977, 2016.   
[4] J. S. Chung and A. Zisserman, “Out of time: automated lip sync in the wild,” in ACCV International Workshops, Taipei, Taiwan, November 20-24, 2016, Revised Selected Papers, Part II 13. Springer, 2016, pp. 251–263.   
[5] K. Grauman, A. Westbury, E. Byrne, Z. Chavis, A. Furnari, R. Girdhar, J. Hamburger, H. Jiang, M. Liu, X. Liu et al., “Ego4d: Around the world in 3,000 hours of egocentric video,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2022, pp. 18 995–19 012.   
[6] R. Tao, Z. Pan, R. K. Das, X. Qian, M. Z. Shou, and H. Li, “Is someone speaking? exploring long-term temporal features for audiovisual active speaker detection,” in Proceedings of the 29th ACM International Conference on Multimedia, 2021, pp. 3927–3935.   
[7] I. Team. (2018) Resolution usage statistics. [Online]. Available: https://ipvm.com/reports/resolution-2018   
[8] X. Yu, X.-Y. Li, J. Zhao, G. Shen, N. M. Freris, and L. Zhang, “Antigone: Accurate navigation path caching in dynamic road networks leveraging route apis,” in IEEE INFOCOM 2022 - IEEE Conference on Computer Communications, 2022, pp. 1599–1608.   
[9] C.-C. Lai, C.-K. Ting, and R.-S. Ko, “An effective genetic algorithm to improve wireless sensor network lifetime for large-scale surveillance applications,” in IEEE Congress on Evolutionary Computation, 2007, pp. 3531–3538.   
[10] A. Galanopoulos, J. A. Ayala-Romero, D. J. Leith, and G. Iosifidis, “Automl for video analytics with edge computing,” in IEEE Conference on Computer Communications, 2021, pp. 1–10.   
[11] T. Fu, H. Zhang, F. Mu, and H. Chen, “Fast cu partitioning algorithm for h. 266/vvc intra-frame coding,” in IEEE International conference on multimedia and expo (ICME), 2019, pp. 55–60.   
[12] R. Bhardwaj, Z. Xia, G. Ananthanarayanan, J. Jiang, Y. Shu, N. Karianakis, K. Hsieh, P. Bahl, and I. Stoica, “Ekya: Continuous learning of video analytics models on edge compute servers,” in 19th USENIX Symposium on Networked Systems Design and Implementation (NSDI), 2022, pp. 119–135.   
[13] Y. Li, A. Padmanabhan, P. Zhao, Y. Wang, G. H. Xu, and R. Netravali, “Reducto: On-camera filtering for resource-efficient real-time video analytics,” in Proceedings of the Annual conference of the ACM Special Interest Group on Data Communication on the applications, technologies, architectures, and protocols for computer communication, 2020, pp. 359–376.   
[14] A. F. Khalifa, E. Badr, and H. N. Elmahdy, “A survey on human detection surveillance systems for raspberry pi,” Image and Vision Computing, vol. 85, pp. 1–13, 2019.   
[15] J. Lian, J. Lou, L. Chen, and X. Yuan, “Echospot: Spotting your locations via acoustic sensing,” Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, vol. 5, no. 3, pp. 1–21, 2021.   
[16] J. S. Chung, J. Huh, A. Nagrani, T. Afouras, and A. Zisserman, “Spot the conversation: speaker diarisation in the wild,” arXiv preprint:2007.01216, 2020.

[17] H. Jiang, C. Murdock, and V. K. Ithapu, “Egocentric deep multichannel audio-visual active speaker localization,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2022, pp. 10 544–10 552.   
[18] J. L. Alcazar, F. Caba, L. Mai, F. Perazzi, J.-Y. Lee, P. Arbel ´ aez, ´ and B. Ghanem, “Active speakers in context,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2020, pp. 12 465–12 474.   
[19] M. Shahid, C. Beyan, and V. Murino, “S-vvad: visual voice activity detection by motion segmentation,” in Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, 2021, pp. 2332– 2341.   
[20] P. Yadav, D. Salwala, and E. Curry, “Vid-win: Fast video event matching with query-aware windowing at the edge for the internet of multimedia things,” IEEE Internet of Things Journal, vol. 8, no. 13, pp. 10 367– 10 389, 2021.   
[21] S. N. Gowda, M. Rohrbach, and L. Sevilla-Lara, “Smart frame selection for action recognition,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 35, no. 2, 2021, pp. 1451–1459.   
[22] Y. Wang, Y. Yue, Y. Lin, H. Jiang, Z. Lai, V. Kulikov, N. Orlov, H. Shi, and G. Huang, “Adafocus v2: End-to-end training of spatial dynamic networks for video recognition,” in 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2022, pp. 20 030– 20 040.   
[23] J. B. Ramgire and S. M. Jagdale, “A survey on speaker recognition with various feature extraction and classification techniques,” International Research Journal of Engineering and Technology, vol. 3, no. 04, pp. 709–712, 2016.   
[24] B. Desplanques, J. Thienpondt, and K. Demuynck, “Ecapa-tdnn: Emphasized channel attention, propagation and aggregation in tdnn based speaker verification,” arXiv preprint:2005.07143, 2020.   
[25] S. Salvador and P. Chan, “Toward accurate dynamic time warping in linear time and space,” Intelligent Data Analysis, vol. 11, no. 5, pp. 561–580, 2007.   
[26] S. I. Vrieze, “Model selection and psychological theory: a discussion of the differences between the akaike information criterion (aic) and the bayesian information criterion (bic).” Psychological methods, vol. 17, no. 2, p. 228, 2012.   
[27] O. Barnich and M. Van Droogenbroeck, “Vibe: a powerful random technique to estimate the background in video sequences,” in International Conference on Acoustics, Speech and Signal Processing. IEEE, 2009, pp. 945–948.   
[28] L. He, X. Ren, Q. Gao, X. Zhao, B. Yao, and Y. Chao, “The connectedcomponent labeling problem: A review of state-of-the-art algorithms,” Pattern Recognition, vol. 70, pp. 25–43, 2017.   
[29] D. Tome, C. Russell, and L. Agapito, “Lifting from the deep: Convolutional 3d pose estimation from a single image,” in The IEEE Conference on Computer Vision and Pattern Recognition (CVPR), July 2017.   
[30] G. Welch, G. Bishop et al., “An introduction to the kalman filter,” 1995.   
[31] X. Qian, A. Brutti, O. Lanz, M. Omologo, and A. Cavallaro, “Audiovisual tracking of concurrent speakers,” IEEE Transactions on Multimedia, vol. 24, pp. 942–954, 2021.   
[32] S. Zhang, X. Zhu, Z. Lei, H. Shi, X. Wang, and S. Z. Li, “S3fd: Single shot scale-invariant face detector,” in Proceedings of the IEEE international conference on computer vision, 2017, pp. 192–201.   
[33] T. Afouras, J. S. Chung, and A. Zisserman, “The conversation: Deep audio-visual speech enhancement,” arXiv preprint:1804.04121, 2018.   
[34] J. S. Chung, J. Huh, S. Mun, M. Lee, H. S. Heo, S. Choe, C. Ham, S. Jung, B.-J. Lee, and I. Han, “In defence of metric learning for speaker recognition,” arXiv preprint:2003.11982, 2020.   
[35] P. Chakravarty and T. Tuytelaars, “Cross-modal supervision for learning active speaker detection in video,” in European Conference on Computer Vision. Springer, 2016, pp. 285–301.   
[36] T. Meinhardt, A. Kirillov, L. Leal-Taixe, and C. Feichtenhofer, “Trackformer: Multi-object tracking with transformers,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2022, pp. 8844–8854.   
[37] X. Zhou, V. Koltun, and P. Krahenb ¨ uhl, “Tracking objects as points,” ¨ in Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part IV. Springer, 2020, pp. 474–490.   
[38] C. Kim, F. Li, A. Ciptadi, and J. M. Rehg, “Multiple hypothesis tracking revisited,” in Proceedings of the IEEE international conference on computer vision, 2015, pp. 4696–4704.