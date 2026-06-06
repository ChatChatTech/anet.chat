# Efficient Object-grained Video Inpainting with Personalized Recovery and Permission Control

Haikuo Yu∗, Jiahui Hou∗, Lan Zhang∗, Suyuan Liu∗, Xiang-Yang Li∗

∗School of Computer Science and Technology, University of Science and Technology of China

yhk7786@mail.ustc.edu.cn, jhhou@ustc.edu.cn, zhanglan@ustc.edu.cn, lsysue@mail.ustc.edu.cn, xiangyangli@ustc.edu.cn

Abstract—Online video-centric service is an emerging application paradigm that enables users to access personalized video services using public equipment. However, it also brings many privacy and security issues, since the online videos might be accessed by different users. To protect the video content privacy against untrusted recipients, we need to take fine-grained control of access permissions to video content. The same video content might be accessible to certain recipients while being restricted to others. Traditional methods generate and encode multiple redacted versions of the same video, leading to substantial increases in storage, processing, and communication costs, which is difficult in adapting to the demands of the ubiquitous multimedia era. Enabling cost-effective, personalized, and fine-grained access control for video content presents a significant challenge.

Video inpainting methods have gained popularity for their notable ability to remove objects with plausible pixels. In this work, we introduce the Object-grained Video Inpainting (OVI) framework for personalized access control – objects in videos are accessible only to authorized users and are visually coherently blocked for all others. OVI is efficient irrespective of user count. We implement the prototype and evaluate its performance via security study, reconstruction effectiveness, and efficiency. The experimental results show that OVI speeds up video sharing and reduces communication savings by a Θ(n) factor over the baselines when there are n different accessing groups.

Index Terms—Video Inpainting, Fine-Grained Video Privacy

# I. INTRODUCTION

In recent years, video-centric systems have been rapidly developed and become prevalent in numerous fields such as elderly care, traffic surveillance, and school safeguarding [16], [32]. These systems typically comprise a set of video sources and numerous video recipients, each having specific tasks. As videos contain a wide variety of semantic information with different sensitivity levels for various utilities, a major security concern is preventing the leakage of irrelevant information to unauthorized recipients.

Existing systems assign access rights by video files. For example, in a nursing home, the surveillance system captures videos across the board, but different users have access to different cameras, e.g., Alice’s family has access to video files from Alice’s room and common areas. This coarsegrained approach performs poorly in both security and usability. First, Alice’s family can see Bob in the public area – undermining Bob’s security; meanwhile, there is no way to see Alice when she is in Bob’s room – undermining Alice’s usability. That is, for various recipients of a video, the factors deemed private or useful within an identical video frame might be object-grained and personalized. Therefore, finer-grained access control mechanisms on video content are essential during the video-sharing process, which cannot be satisfactorily addressed through control granularity at the level of video files or a singular, simplistic perturbation on specific video content. When sharing a video stream with n recipients, each has a personalized block list of objects. It is hard to find a common region as the protection target to fulfill all recipients’ needs [23]. Thus, we aim to control each recipient’s objectgrained access. Each recipient accesses objects according to their authorities, with the videos they receive maintaining overall visual coherence.

![](images/7a92ee35d1b070168193e8b2ae137263ee0cd65ae3717297c569fef306267fb6.jpg)



Fig. 1. OVI performs object removal on the input video once and shares the same inpainted video with multiple recipients. Different recipients reconstruct the different hidden objects within their own authority.

We utilize the idea of video inpainting [12], [25] to realize the object-grained access control. Video inpainting is a video editing technique of filling in missing pixels in a video with plausible values. It has demonstrated promising outcomes to protect video privacy [8], [18]. Given a video and masks that annotate the segmentation of private objects in each frame, state-of-the-art video inpainting methods refer to the regions of objects in masks as the missing pixels and can effectively remove the objects from videos. Unlike blurring or pixelation, inpainting methods preserve the visual coherence and the quality of the whole frame.

We propose an Object-grained Video Inpainting (OVI) mechanism with personalized recovery and permission control generalized to existing inpainting methods. In OVI, a trusted video server performs inpainting-based object removal only once on all sensitive objects in video streams. Subsequently, multiple recipients can retrieve customized and object-grained video results from the same inpainted video stream based on their access authorities (Fig. 1).

The design of OVI aims to achieve the following objectives altogether: First, we seek to ensure the visual effectiveness of object removal and reconstruction. It forms the foundation of our approach to object-grained access control while maintaining utility and visual fidelity. Then we aim to ensure that recipients are unable to reconstruct unauthorized objects. This objective builds a permission control mechanism and guarantees the security of our method. Lastly, our framework aims for efficiency by requiring only one inpainting process and one encoding process to cater to multiple recipients’ needs and the one-time processing time is comparable to typical inpainting methods.

Challenges. To achieve these objectives, our method has to achieve a balance between security and usability, which brings two major challenges. 1) Conventional inpainting methodologies treat the regions of objects as ’missing pixels’, thereby executing pixel completion to achieve effective object removal. However, according to the theory of video steganography [1], the generated pixels lack the original object information, which compromises the reconstruction quality, thereby impacting the usability of the reconstructed objects. Conversely, retaining information of the original objects can detract from the efficacy of object removal. The inherent conflict between effectively removing and reconstructing objects poses a challenge. 2) Striking a balance between the efficiency of access control and the object-level granularity presents a formidable challenge. We aspire to tailor the visible objects for each recipient based on their specific access permission, while other objects remain completely irrecoverable. The temporal cost of access control should remain independent of the number of recipients. However, performing inpainting on each block list of objects individually, then encoding and delivering each uniquely processed video to the respective target recipients, will result in n distinct versions of the same video. When the n is large, this approach leads to significant computing, storage, and communication costs.

To address these challenges, We first design a RecMap Generator within the traditional inpainting process to effectively avoid the trade-off between object removal and reconstruction performance. The RecMap Generator extracts deep feature maps from the original frames. The feature maps, in conjunction with the inpainting results, serve as inputs to a Reconstructor dedicated to reconstructing objects. By meticulously crafting a joint training objective for both the RecMap Generator and the Reconstructor, the feature map (hereafter referred to as the ”map”) is capable of controlling the reconstruction outcomes at a pixel-level granularity. Additionally, we propose a pixel-grained function encryption method for both the map and mask. We transmit the encrypted maps to users in a way compliant with video transmission protocols. This method guarantees that users can only access and reconstruct the authorized objects, thereby facilitating object-grained access control and bolstering privacy protection in video streams.

In summary, our work makes the following contributions.

• To the best of our knowledge, this is the first semantic object-grained access control framework for videos based on video inpainting. We simultaneously set and

implement different object-level access permissions for various recipients of the same video stream.

• We devise a RecMap generation method within the inpainting process that enhances the effectiveness of inpainting and object-grained reconstruction simultaneously. We also propose an efficient functional encryption method on feature maps and masks, ensuring secure reconstruction only for authorized objects.

• We implement an OVI prototype and conduct comprehensive experiments to demonstrate the effectiveness of inpainting, reconstruction, and privacy enhancement. We also evaluate the real-time performance on different devices to showcase its efficiency.

# II. RELATED WORK

# A. Video Inpainting

Video inpainting methods [12], [29], [30], [33] can be used to remove the privacy-sensitive region of images by filling the target region with estimated pixel values without leaving traces. While these methods have achieved excellent visual results, they are not efficient in achieving multiple access control requirements simultaneously, as they all generate pixels of each frame and then perform video encoding to generate one version of inpainted videos. So those methods always require n rounds of video encoding to meet n privacy needs. We also note that some latest image inpainting work [13], [17] using the diffusion model are generally aimed at the effect of diverse inpainting results, which is not required for objectremoving tasks. Generative video content does not impinge upon the access control of the original video content, so diverse inpainting is beyond the scope of our work.

# B. Video Access Control

Video access control methods block the information of video content. From the perspective of granularity, we categorize existing methods into frame-level and object-level.

For frame-level, Existing cryptography-based research employs an all-or-nothing control strategy for video frames. Some studies [2], [7] propose secure and reliable video-sharing schemes based on blockchain technology. In [27], Attribute-Based Encryption (ABE) is used for distributing video data based on users’ attributes. Some deep learning-based methods show advantages both in visual quality and usability. The work [28] develops a generative neural network to generate image perturbations on whole images to preserve privacy in image recognition applications. Wu et al. [23] propose a cycle-GAN framework to hide and reconstruct the details of the whole frame. Frame-grained methods exhibit a relatively coarse granularity of control. Obfuscation of the whole frame inevitably impacts the visual quality and usability of objects that do not require protection.

Some research focuses on the object-level access control of videos. Jin et al. [10] provide a privacy-protection architecture to minimize outgoing data before sending videos to external cloud servers, which supports object-level databaselike queries. The work [5] develops a tile-based storage management system that splits video frames into independently queryable tiles for different video queries. Those object-level approaches segment videos into square blocks for distribution to various users. Our work, in contrast, involves distributing a single, complete video frame preserving visual coherence, and enabling each user to perform object-level reconstruction. Additionally, there exist deep learning-based methodologies that are dedicated to safeguarding particular objects. For instance, face de-identification methods [4], [24] focus on face protection. Similar to inpainting works, these approaches are not amenable to access control applications due to their irreversible nature of obfuscation.

# III. DESIGN OVERVIEW

In this section, we first elaborate on the system model, threats, and design objectives. We then present the OVI design at a high level, with respect to the objectives. More design technique details are explained in the following section.

# A. System and Threats Model

In a video-sharing scenario with access control, we consider two entities: the users receiving videos and the entity responsible for desensitizing the video and delivering it to the users, which we refer to as the video server.

Video server. The entity desensitizing the video can be the owner of the video or a cloud/edge server responsible for processing the original video. In our system, this entity uses inpainting techniques to control the access of objects, then encodes the inpainted frames into a video stream for transmission. We assume the video server is trusted and honest. We also assume that this entity already knows which objects in the video need to be removed and the access strategy of these objects.

User. Users receiving inpainted videos can only reconstruct the removed objects based on their access permissions. Users may have the motivation to infer the removed video content. Therefore, we assume users may potentially be attackers with the goal of accessing video content beyond their access authorities. From the perspective of attackers, to reconstruct the unauthorized objects, their possible ways are to (a) try to obtain the original feature maps of the objects. (b) try to reconstruct the unauthorized objects without knowing the feature maps and masks. We note that the attacker may use prior knowledge or life experience to infer some object information only from the inpainted videos. For instance, users might speculate the presence of a car in the inpainted frame (Fig.2a) or infer the existence of a person on the chair (Fig. 2b). This case is beyond our consideration. However, We ensure that the information the attacker guesses or infers cannot help the reconstruction of original objects.

Trusted authority: A trusted party is introduced solely for the purposes of verifying users’ identities and access permissions, as well as distributing security keys. This entity is typically fulfilled by an auditor or a notary public.

![](images/d3d230f3f5bb1592166679a614838731a300e42124b95a9ca94450ac1f9bda54.jpg)  
original frame

![](images/f4c55c3148337e73f6f72fb976a82db2c744c50c2e5910e7825e9e9bbf714133.jpg)  
inpainted frame

![](images/2385efdd142ed12098b963938fafe647dd2b7e394fe54fa681b0689ede0ed763.jpg)  
original frame

![](images/6c178eb62b08f918679bcd9f4ae8d6d76e59c9460ae313d763f7aeb370dde925.jpg)  
inpainted frame   
Fig. 2. Two examples that users may guess the pixel location of removed objects. In those cases, the information of pixel location that users guess cannot help the reconstruction.

# B. Design Objectives and Overview

1) Design Objectives: We further elaborate on the design objectives of OVI introduced in the introduction section.   
O1: Effectiveness of inpainting. The inpainting results of the proposed method should achieve state-of-the-art object removal performance.   
O2: Ability of object-grained reconstruction. The proposed method must guarantee the effective reconstruction of authorized objects while simultaneously preserving the pixel regions of unauthorized objects.   
O3: Object-grained access control. Each object’s accessibility within every frame must be explicitly determined and controlled. The proposed mechanism should not only manage user permissions for each object meticulously but also safeguard against unauthorized access and reconstruction.   
O4: Efficiency. On the server side, the time overhead of the method should remain consistent and not vary with the number of users. Specifically, the method should execute the inpainting process only once for a given video, regardless of the number of access control requirements. The additional time overhead due to access control should be minimal in comparison to the inpainting process. On the user side, the framework should ensure that reconstruction can be efficiently executed in realtime, even with limited computing resources.   
2) Design Overview: The core idea of OVI lies in removing objects by inpainting on the server side and performing objectgrained reconstruction with permissions on the user side.

There are five components of OVI (Fig. 3), Inpaintor and Reconstructor are deep networks used to perform inpainting and object-grained reconstruction, respectively. The RecMap Generator is a compact deep neural network designed to generate a feature map containing depth information necessary for the Reconstructor to accurately reconstruct regions. Map & Mask Encryptor and Decryptor are used to control access to objects efficiently by functional encrypting feature maps and masks. Map & Mask Encryptor encrypts the mask and the maps one time and users with different access permissions can decrypt different regions of the maps and masks by the Decryptor. The Inpaintor, Reconstructor, and RecMap Generator are involved in the training and inference stages, Map & Mask Encryptor and Decryptor are only involved in the inference stage.

Following the existing inpainting work, we assume each video frame has a corresponding segmentation mask. We use a video V containing T video frames $\{ v _ { t } \in \mathbb { N } ^ { H \times W \times 3 } | t =$

![](images/d831c453caebf3081256f683a19482fc24251bca0fe022385231e111991fe435.jpg)



Fig. 3. Inference workflow of OVI. RecMap Generator, Inpaintor, Map & Mask Encryptor, and Decryptor are system components. The server side on the left performs inpainting on video frames and encryption on feature maps and masks. On the user side, The Decryptor decrypts the region of authorized maps and masks and reconstructs the corresponding objects.

![](images/d8eb2fc5add45dda307112908cf060c69f28514bb170f817af9b14ba71b9baab.jpg)



Fig. 4. The training workflow of OVI. RecMap Generator, Inpaintor, and Reconstructor are involved in the workflow. The Inpaintor is frozen during training.

$1 , 2 , . . . , T \}$ and their corresponding masks $\begin{array} { c c c } { { M } } & { { = } } & { { \{ m _ { t } \in } }  \end{array}$ $\mathbb { N } ^ { H \times W } | t = 1 , 2 , . . . , T \}$ as an example to illustrate the training and inference process of OVI. In the training stage (Fig. 4), we input the whole video V and M into the Inpaintor to remove the objects annotated by M and acquire the inpainted frames $\{ v _ { t } ^ { \prime } \in \stackrel { \cdot } { \mathbb { N } } ^ { H \times W \times 3 } | t = \dot { 1 } , 2 , . . . , T \}$ . Then, the $R e c M a p$ Generator takes each $v _ { t }$ as input and outputs a map $k _ { t } ,$ , an integer $H \times W \times 1$ matrix with values ranging from 0 to 255. For each frame, we randomly select objects from the mask $m _ { t }$ to create a new mask $m _ { t } ^ { \prime }$ , which includes only the segmented selected objects. We then compute $k _ { t } ^ { \prime } = k _ { t } \cdot m _ { t } ^ { \prime }$ to preserve the values in $k _ { t }$ that correspond to the regions of the selected objects. We input $k _ { t } ^ { \prime } , m _ { t } ^ { \prime } ,$ , and $ { \boldsymbol { v } } _ { t } ^ { \prime }$ into the Reconstructor. Our training objective is to reconstruct the non-zero pixel regions of $m _ { t } ^ { \prime }$ as faithfully and realistically as possible while leaving the other regions of $ { \boldsymbol { v } } _ { t } ^ { \prime }$ unchanged, thereby achieving the goals of effective object-grained reconstruction (O2). To ensure that the Inpaintor remains exclusively focused on the task of object removal, it is trained in isolation, unaffected by the objectives of joint training. The reconstruction effectiveness is achieved through joint training of the RecMap Generator and the Reconstructor. Consequently, our framework is compatible with a variety of existing state-of-the-art inpainting methods, thereby fulfilling O1.

In the inference stage (Fig. 3), the server deploys the Inpaintor, the RecMap Generator, and the Encryptor, while the Reconstructor and the Decryptor is deployed on the user side. The server takes the original videos $\{ v _ { t } \}$ and the masks $\{ m _ { t } \}$ as the input of the Inpaintor and the RecMap Generator to generate the inpainted frames $\left\{ v _ { t } ^ { \prime } \right\}$ and $\{ k _ { t } \}$ . We manage the access permissions for objects across multiple users by enabling different users to obtain distinct pixel regions of maps and masks. To obviate the necessity of distributing diverse maps and masks to each user, we propose a functional encryption strategy. The server uses the Encryptor to encrypt each $k _ { t }$ and $m _ { t }$ one time to acquire $e n c ( m _ { t } )$ and $e n c ( k _ { t } )$ . The $e n c ( m _ { t } )$ and $e n c ( k _ { t } )$ are still integer matrix ranging from 0 to 255. Then, the server combines $\left\{ v _ { t } ^ { \prime } \right\}$ as the RGB channels and $\{ e n c ( k _ { t } ) | t = 1 , 2 , . . . , T \}$ as the alpha channels to form RGBA images. The RGBA images are then encoded into video streams S. S and $\{ e n c ( m _ { t } ) \}$ are sent to users. Upon receiving S, each user $j$ decodes S to obtain $\{ e n c ( k _ { t } ) \}$ and $\{ v _ { t } ^ { \prime } \}$ . Decryptor takes $\{ e n c ( k _ { t } ) \}$ and $\{ e n c ( m _ { t } ) \}$ as input to acquire $d e c ( e n c ( m _ { t } ) , j )$ and $d e c ( e n c ( k _ { t } ) , j )$ , which retrieves the pixel regions of the objects within authorized access of user $j .$ The $\{ d e c ( e n c ( m _ { t } ) , j ) \}$ , $\{ d e c ( e n c ( k _ { t } ) , j ) \}$ , and $\{ v _ { t } ^ { \prime } \}$ are then inputted into the Reconstructor. The Reconstructor reconstructs the objects that user $j$ can access, while the remaining objects are still removed. Combining the functional map&mask encryption with the object-grained reconstruction effectiveness of the Reconstructor, we can achieve objectgrained access control. (O3).

Throughout the entire inference process, regardless of the number of users or different privacy requirements, the server only performs one inpainting and one encryption. Also, the model of Reconstructor on the user side is lightweight, and the introduced time overhead for reconstruction is minimal, allowing real-time processing. Thereby, OVI achieves efficiency for the entire system (O4).

# IV. KEY DESIGNS

In this section, we first introduce the design of OVI networks, then we present the details of how to perform functional encryption and sharing of the maps and the masks.

# A. Effectiveness of Inpainting and Reconstruction

OVI ensures the effectiveness of inpainting and object-level reconstruction by two designs: the RecMap Generator and the object-grained training objectives. First, we introduce our design purposes for the RecMap Generator.

First, we design the RecMap Generator to avoid the tradeoff between the effectiveness of inpainting and reconstruction. Existing inpainting methods have been highly successful in seamlessly removing objects from images. However, OVI has the additional target of preserving the ability to reconstruct the inpainted objects. This means that the inpainting results should not only remove the object without leaving visual traces as much as possible but also retain the necessary visual information of objects for subsequent reconstruction. Achieving both objectives poses a semantic conflict, as they entail contradictory goals. To navigate the trade-off between inpainting and reconstruction effectiveness, we assign the Inpaintor the sole task of completing the pixels of removed objects. Conversely, the RecMap Generator is tasked with conveying object information. The Inpaintor views the regions of removed objects as missing pixels, whereas the RecMap Generator processes original frames to generate a feature map that encapsulates deep information about the removed objects. The Inpaintor is trained independently, while the feature map created by the RecMap Generator is integral to the training of the Reconstructor. Through joint training of the RecMap Generator and Reconstructor, both models learn to reconstruct objects cohesively and uniquely match each other. The necessary information for reconstruction is transmitted solely through the feature map, which is encrypted to ensure security. By doing so, we enable both excellent inpainting and reconstruction results without compromising on either aspect.

Secondly, the RecMap Generator is designed to ensure the security of access control on removed objects, even when users guess their pixel location. As we discussed in the threat model, users may deduce the approximate object segmentation in the inpainted video frames based on their prior knowledge or by identifying unnatural regions in the frames, as shown in $\mathrm { F i g } . 2 .$ . To ensure the security of access control, we do not solely rely on the Inpaintor to achieve satisfactory inpainting results for all objects in all video frames. The security of OVI is robust to the case that the inpainting model sometimes has imperfect effects. Regardless of whether the inpainting performance is good or not, users cannot reconstruct original objects as long as the corresponding regions of maps are encrypted. So, by employing the RecMap Generator and encrypting the maps, even if users can deduce the accurate segmentation of the inpainted objects, OVI can prevent them from restoring the original objects without permission and decryption.

# B. Training objectives.

Now we discuss the joint training for the RecMap Generator and Reconstructor to enable the Reconstructor to effectively and selectively restore specific objects.

First, we fix the width and height of the original video to be w and $h ,$ respectively. The RecMap Generator adopts Resnet [6] as its backbone and generates $w \times h \times 1$ maps. The Reconstructor uses Unet [15] as its backbone and generates $w \times h \times 3$ reconstructed frames. In our evaluations, we set $w = 2 5 6$ and $h = 2 5 6$ .

For each frame $v _ { t }$ , we input $v _ { t }$ and mask $m _ { t }$ into Inpaintor to generate the inpainted frame $\boldsymbol { v } _ { t } ^ { \prime } .$ The RecMap Generator takes the binarize t $v _ { t }$ as th mask nput to geto obtain ate the map , $k _ { t }$ . Then we $m _ { t }$ $m _ { t } ^ { b }$

$$
m _ {t} ^ {b} [ x, y ] = \left\{ \begin{array}{l l} 1 & m _ {t} [ x, y ] > 0 \\ 0 & m _ {t} [ x, y ] = 0 \end{array} , \right. \tag {1}
$$

where $x$ and $y$ denote the horizontal and vertical pixel coordinates of $m _ { t } .$ , respectively. Then, we perform an element-wise multiplication between $k _ { i }$ and $m _ { t } ^ { b }$ to only retain the values of the inpainted regions, denoted as $k _ { t } ^ { \prime } = k _ { i } \odot m _ { t } ^ { b }$ . We concatenate $m _ { t } ^ { b } , k _ { t } ^ { \prime } ,$ and $ { \boldsymbol { v } } _ { t } ^ { \prime }$ to form the input of the Reconstructor, resulting in the output $o _ { t } ^ { 1 }$ during training

$$
o _ {t} ^ {1} = \operatorname{Rec} \left(m _ {t} ^ {b} | | k _ {t} ^ {\prime} | | v _ {t} ^ {\prime}\right), \tag {2}
$$

where $R e c$ denotes the inference process of the Reconstructor. We calculate the $L _ { 1 }$ loss between $o _ { t } ^ { 1 }$ and $v _ { t }$ to minimize the pixel-level differences between them. Additionally, we compute the perceptual loss (PL) [11] using a pre-trained VGG model between $o _ { t } ^ { 1 }$ and $v _ { t }$ to reduce the discrepancies in the deep features of them. The Eq. 3 yields our cycle loss $\mathrm { l o s s } _ { \mathrm { c y c } }$ from original frames to reconstructed frames, which focuses on reconstructing all objects in the frames.

$$
\mathrm{loss} _ {\text {cyc}} = \lambda_ {1} L _ {1} \left(o _ {t} ^ {1}, v _ {t}\right) + \lambda_ {2} P L \left(o _ {t} ^ {1}, v _ {t}\right), \tag {3}
$$

where $\lambda _ { 1 }$ and $\lambda _ { 2 }$ denote the weights assigned to the two types of losses, respectively.

Masks delineate the regions to be reconstructed by the Reconstructor. Our aim is for the Reconstructor to concentrate only on the non-zero areas of masks. To reinforce this, we create a zero-filled mask $m _ { t } ^ { z e r o }$ and concatenate it with $k _ { t } ^ { \prime }$ and $ { \boldsymbol { v } } _ { t } ^ { \prime }$ to generate the second input for the Reconstructor, yielding the second output in the training process as

$$
o _ {t} ^ {2} = \operatorname{Rec} (m _ {t} ^ {\text { zero }} | | k _ {t} ^ {\prime} | | v _ {t} ^ {\prime}). \tag {4}
$$

Similarly, we produce a one-filled mask $m _ { t } ^ { o n e }$ and obtain the third output

$$
o _ {t} ^ {3} = \operatorname{Rec} (m _ {t} ^ {\text { one }} | | k _ {t} ^ {\prime} | | v _ {t} ^ {\prime}). \tag {5}
$$

We then calculate the $L _ { 1 }$ loss between $o _ { t } ^ { 2 }$ and the inpainted frame $v _ { t } ^ { \prime } ,$ , and the $L _ { 1 }$ loss between $o _ { t } ^ { 3 }$ and the original frame $v _ { t } .$ ,

$$
\text { loss } _ {\text { zero }} = L _ {1} (o _ {t} ^ {2}, v _ {t} ^ {\prime}), \text { loss } _ {\text { one }} = L _ {1} (o _ {t} ^ {3}, v _ {t}). \tag {6}
$$

The $\mathrm { l o s s } _ { \mathrm { z e r o } }$ ensures that the Reconstructor is confined to reconstructing only the non-zero mask regions. Despite $m _ { t } ^ { o n e }$ being entirely filled with $1 , k _ { t } ^ { \prime }$ is non-zero solely within the object region. The $\mathrm { l o s s } _ { \mathrm { o n e } }$ not only enhances the comprehensiveness of the training loss concerning masks but also indicates that the reconstruction is affected by both the mask and the map, underscoring the necessity of both elements.

The losses discussed previously are all at the frame level, suitable for reconstructing all objects within a frame. In convolutional neural networks, such as Unet or Resnet, the local features of the input have a significant impact on the entire output. Hence, using only these frame-level losses for training the Reconstructor might result in the region corresponding to a single object in the masks and keys having a disproportionate effect on the reconstruction of all objects. To mitigate this, we introduce an object-grained loss, designed to prevent the partial regions of masks and maps from excessively influencing the reconstruction of the entire set of objects.

As depicted in Fig. 4, during each training epoch, we randomly select objects from each mask $m _ { t }$ to create a new mask $m _ { t } ^ { \prime }$ . This new mask $m _ { t } ^ { \prime }$ retains the pixel regions of the selected objects while setting other pixel regions to 0. At least one object is selected to differentiate $m _ { t } ^ { \prime }$ from $m _ { t } ^ { z e r o }$ . We then binarize $m _ { t } ^ { \prime }$ to obtain $m _ { t } ^ { b ^ { \prime } }$ and compute the element-wise tmultiplication between $m _ { t } ^ { b ^ { \prime } }$ t and $k _ { t } ,$ denoted as $k _ { t } ^ { ^ { \prime \prime } } = k _ { t } \cdot m _ { t } ^ { b ^ { \prime } }$ . Subsequently, we concatenate $m _ { t } ^ { \check { b } ^ { \prime } } , \ k _ { t } ^ { \prime \prime }$ , and $ { \boldsymbol { v } } _ { t } ^ { \prime }$ to form the fourth input for the Reconstructor, generating the fourth output as

$$
o _ {t} ^ {4} = \operatorname{Rec} (m _ {t} ^ {b ^ {\prime}} | | k _ {t} ^ {^ {\prime \prime}} | | v _ {t} ^ {\prime}). \tag {7}
$$

For regions where $m _ { t } ^ { b ^ { \prime } } > 0$ , we calculate the $L _ { 1 }$ loss between $o _ { t } ^ { 4 }$ and $v _ { t }$ . For regions where $m _ { t } ^ { b ^ { \prime } } = 0 .$ , we calculate the $L _ { 1 }$ loss between $o _ { t } ^ { 4 }$ and $v _ { t } ^ { \prime } .$ . We also use $\begin{array} { r } { \epsilon _ { 1 } ~ = ~ \frac { \sum m _ { t } ^ { b ^ { \prime } } } { w \times h } } \end{array}$ and $\epsilon _ { 2 } ~ = ~ { \frac { \sum \left( 1 - m _ { t } ^ { b ^ { \prime } } \right) } { w \times h } }$ as the normalization factors to ensure a balance in the number of pixels between the non-zero and zero regions. The objective of ${ \mathrm { l o s s } } _ { \mathrm { p a r t } }$ is to quantify the discrepancies between $o _ { t } ^ { 4 }$ and the corresponding ground truth $( v _ { t } \ \mathrm { o r } \ v _ { t } ^ { \prime } )$ in their respective regions, given by

$$
\begin{array}{l} \mathrm{loss} _ {\mathrm{part}} = \epsilon_ {1} L _ {1} (m _ {t} ^ {b ^ {\prime}} o _ {t} ^ {4}, m _ {t} ^ {b ^ {\prime}} v _ {t}) \\ + \epsilon_ {2} L _ {1} \left(\left(1 - m _ {t} ^ {b ^ {\prime}}\right) o _ {t} ^ {4}, \left(1 - m _ {t} ^ {b ^ {\prime}}\right) v _ {t} ^ {\prime}\right). \tag {8} \\ \end{array}
$$

Finally, the overall objective of our training process is to minimize

$$
\text { loss } _ {\text { all }} = \text { loss } _ {\text { cyc }} + \lambda_ {3} \text { loss } _ {\text { zero }} + \lambda_ {4} \text { loss } _ {\text { one }} + \lambda_ {5} \text { loss } _ {\text { part }}, \tag {9}
$$

where $\lambda _ { 3 } , \lambda _ { 4 }$ and $\lambda _ { 5 }$ are the weight of $\mathrm { l o s s } _ { \mathrm { z e r o } }$ , lossone and ${ \mathrm { l o s s } } _ { \mathrm { p a r t } }$ . In our experiments, we set $\lambda _ { 2 } = 1$ and $\lambda _ { 1 , 3 , 4 , 5 } = 5 0 0$ to strike a balance between the magnitudes of perceptual loss and $L _ { 1 }$ loss.

# C. Functional Encryption of Maps and Masks

From our network design, Users can reconstruct the pixel regions of objects if and only if users can obtain the corresponding regions of mask and map. The mask informs users about the areas to be reconstructed, while the map enables the Reconstructor to accurately reconstruct the non-zero regions in the mask. We design a functional encryption strategy where the server performs encryption on masks and maps one time, and different users can decrypt and obtain the authorized regions of the mask while other regions remain encrypted.

We assume videos contains c objects $\{ e _ { i } , i \in [ 1 , c ] \}$ requiring inpainting and we denote the background as $e _ { 0 }$ . In the preprocessing stage prior to video processing, we generate a $s e e d _ { i }$ randomly and uniformly for each $e _ { i }$ . We use each seedi as the nonces of PRNG to generate a $h \times w$ matrix $R _ { i }$ containing random integers ranging from 0 to 255. We note that the mask $m _ { t }$ of frame $v _ { t }$ labels pixel region of each $e _ { i } , i \in [ 0 , c ]$ using pixel value $p _ { i } \ ( p _ { 0 } = 0 )$ . The details of the encryption process (Fig. 5) are as follows. We first generate the binarized mask $m _ { i , t } ^ { b }$ t for each $e _ { i }$ in $v _ { t } .$ .

$$
m _ {i, t} ^ {b} [ x, y ] = \left\{ \begin{array}{c c} 1 & m _ {t} [ x, y ] = p _ {i}, \\ 0 & \text { others }. \end{array} \right. \tag {10}
$$

![](images/3b0e99a89df107afd5f9cbfa21fb8e0fe36de88837011651b8046b11ee7565c9.jpg)



Fig. 5. An example of functional encryption on a mask and a map. each object is encrypted by a unique seed, the seeds are distributed to users with permission.

For each $e _ { i } ,$ , we calculate the XOR value $X m _ { i }$ between $R _ { i }$ and $m _ { t }$ and the XOR value $X k _ { i }$ between $R _ { i }$ and $k _ { t }$ . Then we combine all the $X m _ { i }$ and $X k _ { i }$ according to the region of $e _ { i }$ and $m _ { i , i } ^ { b }$ t to acquire the encrypted mask $e n c ( m _ { t } )$ and the encrypted map $e n c ( k _ { t } )$ , given by

$$
e n c \left(m _ {t}\right) = \sum_ {i = 0} ^ {c} m _ {i, t} ^ {b} \cdot \left(R _ {i} \oplus m _ {t}\right), \tag {11}
$$

$$
e n c (k _ {t}) = \sum_ {i = 0} ^ {c} m _ {i, t} ^ {b} \cdot (R _ {i} \oplus k _ {t}),
$$

where · denotes dot product operation and ⊕ denotes the dot XOR operation.

![](images/809f4ae87029074b872ba6e41037e26c5b6053a324ab2f6ef6e44e4f77b8f1c4.jpg)



Fig. 6. An example of functional decryption of a mask and a map of different users. User 1 and user 2 decrypt the different regions of the map and mask.

To decrypt $e n c ( m _ { t } )$ and $e n c ( k _ { t } )$ , users initially utilize the seeds as nonces for a Pseudo-Random Number Generator (PRNG) to generate $h \times w$ matrices. Considering $s e e d _ { i }$ as an example, the user applies XOR operation to $R _ { i }$ and $e n c ( m _ { t } )$ to obtain

$$
R _ {i, t} = R _ {i} \oplus e n c (m _ {t}). \tag {12}
$$

Only the pixel region of $e _ { i }$ is decrypted to $p _ { i }$ while pixels in other regions remain random. It is necessary to denoise $R _ { i , t }$ since random pixels may inadvertently contain $p _ { i }$ . First, we apply the Sobel operator to compute the horizontal and vertical gradients of $R _ { i , t }$ . Since the pixels in the $e _ { i }$ regions are the same, gradients in these non-edge areas are zero. Conversely, other regions with random pixel values have very low probabilities of having 0 gradients. Therefore, we first extract the regions with gradients 0. To further diminish residual noise, we perform one iteration of erosion. To compensate for the loss caused by erosion and non-zero gradients of the edge region, we perform two iterations of dilation and obtain a pixel region $R _ { i , t } ^ { \prime }$ closely approximating $e _ { i } . \ R _ { i , t } ^ { \prime }$ is then binarized to generate $R _ { i , t } ^ { b ^ { \prime } }$ . Next, we calculate $R _ { i , t } ^ { b ^ { \prime } } \cdot ( R _ { i } \oplus e n c ( k _ { t } ) )$ to decrypt the map within the $e _ { i }$ region.

![](images/f257bd766d3f8456edd323562545eb7ff01879d5f0de03b75f6fbaccea4fcade.jpg)  
Inpainted frame

![](images/f4fe84ac3499e76706c796a931cd38fae488336e8e9400ea17eee3e3bcfb62bf.jpg)  
Authorized recovery

![](images/1934379f011f8abea551be5c7dbbb8173b824e9304e4fcfea46c8262b3664407.jpg)  
Attack case 1

![](images/a35acf9ff17f1a74164cc677ef51207ccbe0bcc5e124bf2ed11d0e74a197e310.jpg)  
Attack case 2

![](images/44d0595449897d0ca81c7f59cce26d8e5cc4dc7d27f80d633eb8c36f066eb6d9.jpg)  
Inpainted frame

![](images/9e46ade082ff3fd7d342fe60ce91a1afa37d981e168987255e0e5acc60b89e60.jpg)  
Authorized recovery

![](images/32875d55148ef78ca52eca5499fbe77629420843c1d310434ef05d1c86a46432.jpg)  
Attack case1

![](images/f51fc7ffe016a524de7f44c2a447d04acdee5bf314e0b29ee9a486a9bef1a44a.jpg)  
Attack case 2

![](images/a7a67feb327c7475f76839c427be233ef71bed65759028c77bd9fed00ed0aa51.jpg)  
Inpainted frame

![](images/ad6bf04580bd098014e423fabaa362bcdb5c0a3de2f4cb31d8cdc85d50e9b26e.jpg)  
Authorized recovery

![](images/0558855043158d6e2c8ca1d2e6f85c758e46cec7554d02b853fbac7af0584ace.jpg)  
Attack case 1

![](images/7e1f8cd8e08523e36d5570eb7e38b21a496ed4c660246792adeaa131beda9500.jpg)  
Attack case 2

![](images/8386b107f1c0ef47da20244f73c136a7a84aed098824756174c0dedcd20898c1.jpg)  
Inpainted frame

![](images/7c2c6f76ec985b7589c6da9a0ed980c969495db98aa55be1fe1800648768268b.jpg)  
Authorized recovery

![](images/efdc4fe5d15157bb6a2329353ef26027c132ef7ab18a85c756003b75917cf07f.jpg)  
Attack case 1

![](images/bc35b144d5bcbf24d6a961e149093ff8c8c7939e656c7c36743df9f8d94b62df.jpg)  
Attack case 2   
Fig. 7. Visual comparison examples of authorized reconstructed frames, frames reconstructed by attack case 1 and attack case 2.

Finally, we address the management of seeds associated with objects. For the reconstruction of a given object $e _ { i } ,$ users must obtain the corresponding seedi. Therefore, it is imperative that distinct seeds are accessible to different users based on their permission. The distribution of seeds constitutes a pre-processing step that can be effectively addressed by existing key management systems. In this paper, we use ciphertext-policy attribute-based encryption (CP-ABE) [3] as an exemplar to succinctly illustrate this process. CP-ABE describes users’ identities as an attribute set over the attribute universe of the system and forms access policies by combining attribute values through Boolean operations and thresholds. We assume that a trusted authority is aware of the access policy for each object. During the pre-processing phase, this entity generates a unique seedi for each $e _ { i } , i ~ \in ~ [ 0 , c ]$ and sends it to the server. Subsequently, the trusted authority integrates the access policy $\mathbb { A } _ { i }$ of object $e _ { i } , i \in [ 1 , c ]$ into the ciphertext $A B E _ { e n c } ( s e e d _ { i } )$ and send it to users. To decrypt $A B E _ { e n c } ( s e e d _ { i } )$ , users’ attribute sets must satisfy the attached $\mathbb { A } _ { i }$ . We note that $s e e d _ { 0 }$ is not distributed to users, as the inpainted frames already include the original background. Also, possession of seed0 enables users to decrypt and observe the outlines of all inpainted objects, which could potentially cause privacy leakage.

# V. SECURITY ANALYSIS

Given our threats model, we analyze the security of access control of OVI from two perspectives: 1) attempt to acquire keys to decrypt feature maps and masks and 2) attempt to reconstruct the hidden objects without the feature maps.

Attack 1. Is it possible for the adversary to obtain maps for the objects without permission?

In our implementation of the access control process, we utilize the computationally secure CP-ABE method [21] to manage our seeds and the AES-CTR [9] as PRNG to encrypt feature maps by XOR. These cryptography techniques are proven to be robust against computational attacks.

Based on this assumption, we consider the adversary’s computational capabilities to be limited, preventing them from acquiring a seed when they lack proper access. Furthermore, the encrypted maps and masks are combined using several random matrices generated through XOR operations with random bitmaps, as shown in Eq. 11. As a result, attackers are unable to obtain the corresponding masks and maps without the required permission to access the seeds.

Attack 2. Is it possible for the adversary to reconstruct the inpainted objects without true masks and maps?

Although we encrypt the masks, an adversary might still infer a mask from the inpainted frames (Fig. 2). Consequently, we analyze the feasibility of unauthorized object reconstruction under the assumption of a worst-case scenario, where the adversary accurately infers the exact mask. We categorize the attack methods into two cases: using the existing Reconstructor model and training a new $R e c o n s t r u c t o r \mathrm { { a d v } }$ model. In the case 1, the attacker requires a map to serve as input for the existing Reconstructor. We Assume that the keys have not been compromised, and the adversary is unable to decrypt the encrypted maps without authorization. Therefore, we substitute the original map with three alternative strategies: using all-zero maps, all-one maps, and randomly generated maps. The effectiveness of these three substitutions is similar. Fig. 7 illustrates examples of these failed attempts.

In the case 2, an adversary may train a new $R e c o n s t r u c t o r _ { \mathrm { a d v } }$ and aim to directly reconstruct the original frames using the inpainted frames and true masks. However, as previous research [1] has highlighted, without access to the hidden object information, the attacker cannot accurately reconstruct the concealed information. Since the attacker does not have access to the original frames and the generated maps, their trained network performs poorly on the test dataset. We conduct the experiment that allows the attacker to train a $R e c o n s t r u c t o r \mathrm { { a d v } }$ using the same network and training objectives with our Reconstructor. The $R e c o n s t r u c t o r _ { \mathrm { a d v } }$ takes inpainted frames and masks as inputs without the map to generate the original frames. Fig. 7 shows examples of reversals attempted by $R e c o n s t r u c t o r \mathrm { { a d v } }$ . The results demonstrate that the adversary fails to reconstruct the removed object.

Furthermore, we provide a quantitative analysis by comparing the two attack cases and normally authorized reconstruction based on the PSNR [22] and SSIM [20] metrics.

We use two state-of-the-art inpainting methods [12], [29] as our Inpaintor 1 and Inpaintor 2. Fig. 8 and Fig. 9 show the significant differences between the two attack methods and normally authorized reconstruction, which clearly demonstrates that OVI is capable of resisting both attack cases.

![](images/c50e95cffba0a1bb05b26fd1b0fb8683109a0db81bba2a2984279353d36ce1e8.jpg)



Fig. 8. PSNR comparison between normally authorized reconstruction and two attacks.

![](images/bf6d4dc9ade114f3d1a69c90b09c6c7cc45d9fbdc63192eed50c2dd79cc375d0.jpg)



Fig. 9. SSIM comparison between normally authorized reconstruction and two attacks.

# VI. EVALUATION

Our evaluation starts with measuring the real-time performance of OVI on both the server and the user side. We then conduct experiments to discover the effectiveness and robustness of object-grained reconstruction in different settings.

# A. Settings

Our video server runs on Linux with two NVIDIA GTX 3090 GPUs with 24 GB of memory. The server uses the RGBA encoding method provided in [23]. We use two kinds of devices as users’ devices, Device 1 runs on Windows 10 with eight Intel Cores i5-11500 (2.70GHz) and one NVIDIA GTX 3060 GPU with 12 GB of memory; Device 2 is Jetson Nano (Quad-Core ARM Cortex-A57 MPCore CPU and NVIDIA Pascal GPU with 256 CUDA cores).

Dataset. We evaluate OVI on two video object segmentation datasets, YouTube-VOS [26] and DAVIS [14]. Both datasets contain object-segmentation masks for each frame. YouTube-VOS and DAVIS consist of 4453 and 150 video clips, respectively. We train the RecMap Generator and Reconstructor on the YouTube-VOS and evaluate the models on the DAVIS.

Metrics. We choose PSNR, SSIM, VFID [19] and LPIPS [31] to evaluate the reconstruction performance of OVI. Specifically, PSNR and SSIM are frequently used to assess the distortion of videos. VFID and LPIPS measure the perceptual similarity between two input videos.

# B. Real-Time Performance

Baseline methods. To achieve the effect where each user receives a unique inpainting video as attained by OVI, we use two existing video sharing methods as baselines for comparing the time expenditure. In both methods, we employ the the-state-of-art techniques [29] for the inpainting process of objects in videos. The baseline 1 performs inpainting for each user according to their access permissions. This process results in n inpainting operations, n encoding processes, and n video copies. The baseline 2 method entails inpainting all objects in each frame first. Then, for each user, specific pixel regions of objects are selected and pasted onto the inpainted frames. Finally, these frames are encoded into the stream and transmitted to the user. This process results in 1 inpainting operations, n encoding processes, and n video copies.

We first compare the average FPS of OVI with the two baseline methods using the same encoder and device (Fig. 10). As the number of privacy needs increases, the FPS of OVI remains the same, while the average running time of the two baseline methods increases linearly and the FPS decreases inversely. We note that although the running time of baseline 2 is close to OVI, the communication and the storage overhead are $\Theta ( n )$ times OVI. This is because, despite baseline 2 only performing inpainting once, it still requires encoding for n different video versions, with the encoding and streaming processes being repeated n times.

![](images/93149c7cae5e233f6e4139118ebbc44055ad7975e51c1b9b0914b14f1d68090d.jpg)



Fig. 10. The inpainting FPS of OVI and baseline methods on the server side vs. the number of users with different privacy needs.

![](images/8ffdfe1872285cf6f4db6b14308afba16099dca3b8f4065dee503bb6eca4025e.jpg)



Fig. 11. Additional time overhead introduced by OVI: map & mask encryption and map generation vs. the number of objects per frame.

Compared to a single run of traditional inpainting methods, running OVI once introduces additional computational overhead introduced by map generation and mask&map encryption. We now demonstrate that this increased overhead is acceptable. The runtime for generating maps is consistent across video content, averaging 5.90 ms per frame. However, the time required for encrypting maps and masks increases linearly with the number of objects. Fig. 11 illustrates that the runtime for encryption escalates from 0.85 ms to 1.54 ms as the element count rises from one to eight, which negligibly affects the overall temporal overhead. On average, the additional time overhead constitutes merely 6.6% of the runtime of the original inpainting process.

![](images/1d81b6f5e56fb1fde4e84f4909773b6666bf689be52a5c053dbab5f134bda17a.jpg)



Fig. 12. Fps of decryption in two kinds of devices.

![](images/93c6fa6ed5711a406ebfaea424dbd92dddd4fe50d98295ceb4ffeabdf202cc03.jpg)



Fig. 13. Fps of reconstruction in two kinds of devices.

We now demonstrate the real-time performance of models of different sizes running on different users’ devices. We use $C F _ { u }$ and $C F _ { r }$ to represent the number of convolutional filters in the Unet (Reconstructor) and Resnet (RecMap Generator) layers, respectively. Larger values of $C F _ { u }$ and $C F _ { r }$ lead to higher computational demands on the networks. Fig. 12 and Fig. 13 present the average time overhead for decryption and reconstruction. When the $C F _ { u } ~ = ~ 2 4 .$ , the frame rate of reconstruction reaches 101 fps on a PC and 32 fps on a Jetson Nano, minimally impacting the real-time performance and enabling smooth and secure object reconstruction at the user end.

![](images/9febff6692e6a2d31362323d4f977818cdcbf196dc584dbf3b689bd377aa74c9.jpg)

![](images/d12a2bbd35e709ff6584aacff4d7d04eebe4293e5efd037629fb001f089aba44.jpg)

![](images/12f551598ac3de7b83743dfa464fbdc3c69c1e19578f5619a60e61420cec624c.jpg)

![](images/c6a5a89ebb4c7bf8f52520ccb09b654b63e7e2a142c8c69e70ecc3cbe63b5d92.jpg)

![](images/9ea6f45e0b2c102d231538889c128953a77dc90c63cdc80cbe8ce49fd48b7c34.jpg)  
Original frame

![](images/63563bad6a65b8fe862ffa240cb39a2c5efee7349a8c60ea93525cc9ecc3e7ab.jpg)  
Inpainted frame

![](images/7f2ac0be0c43c60e67e1b1c393fc2ae8ff4696113b624c23ca0491bcc891d4d9.jpg)  
User 1 reconstruction

![](images/6622540be4e789eff350599e343ead338f809ab91be20f8438957f36137fe605.jpg)  
User 2 reconstruction

![](images/18ceb7bb520282bfa6b011e0095fe41933675c85201e9bd1020a4c92d7d33771.jpg)

![](images/b8f7c5e2c47b2833442fda0c8f6244cb1b9d7bae0f60bf24c9df76ed30e5cde7.jpg)

![](images/46d7c57e461305cd8c6a798c41803de9a7a7d3a9fa719ccb6df2277562c16fa9.jpg)

![](images/877075b3e891ae082671634d32a2593bae9af0526879394cab4b6f438df941b9.jpg)

![](images/15a41995153309032df03abd01f04d67bdf44fb8184cff328f7e3bd4cc8a72be.jpg)  
Original frame

![](images/f185fa183e7b95060a0a89150981df54b4319a2779099d51bab11876040ae732.jpg)  
Inpainted frame

![](images/52660db8196b99e59c4258c22df46099baa514c1400b4b18bdf36a6afef1b960.jpg)  
User 1 reconstruction

![](images/e66912c2929499ea99c2622be0e48e3d9c79b17f8728da9fdb396627811e1071.jpg)  
User 2 reconstruction   
Fig. 14. Qualitative results of original frames, the inpainted frames, and two reconstruction results with different access permissions.

To sum up, OVI speeds up the encoding efficiency $\Theta ( n ) \times$ to the baseline methods to satisfy multiple privacy needs on the server side and save the communication and the storage overhead from Θ(n) to Θ(1). Also, OVI introduces an additional O(1) extra time overhead on the user side, which does not hinder the real-time performance of decoding.

# C. Reconstruction Performance

Qualitative results. Fig. 14 shows the qualitative results of object removal and two different reconstructions. This demonstrates our Reconstructor can reconstruct faithful results within access while other objects remain inpainted.

Quantitative results. We first consider the case of reconstructing all inpainted objects and use the frame-grained work [23] as the baseline method. Tab. I illustrates both Inpaintor 1 and Inpaintor 2 show similar and higher performance across all four metrics compared to the baseline method.

TABLE I FOUR METRICS ON THE CASE RECONSTRUCTING ALL INPAINTED OBJECTS. 

<table><tr><td></td><td>PSNR</td><td>SSIM</td><td>VFID</td><td>LPIPS</td></tr><tr><td>Inpaintor 1</td><td>33.467</td><td>0.963</td><td>0.133</td><td>0.027</td></tr><tr><td>Inpaintor 2</td><td>33.611</td><td>0.959</td><td>0.100</td><td>0.021</td></tr><tr><td>baseline</td><td>26.931</td><td>0.870</td><td>0.194</td><td>0.131</td></tr></table>

We also evaluate the impact of different parameter numbers for the Reconstructor and RecMap Generator on the reconstruction results. As shown in Fig. 15, the Reconstructor’s performance remains at a good level when $C F _ { u } \ge 2 4 $ , and the size of the RecMap Generator has a small impact on the reconstruction results. Unless otherwise specified, we default to using $C F _ { u } = 2 4$ and $C F _ { r } = 2 4$ in evaluations.

Next, we consider cases where only partial objects are reconstructed. For each video in the dataset, we randomly generate non-empty block lists of objects for users. We compare the reconstructed object’s pixel regions with the original frames in terms of PSNR and SSIM (VFID and LPIPS require the entire frame as input). Then, we compare the pixel regions of unauthorized objects generated by the Reconstructor with the inpainted frame, as shown in Tab II.

![](images/7951f25051a8dbacb9167e731904e715982014f3fb0b87be1b2c9768523f00ad.jpg)



(a) CFu vs. PNSR & SSIM

![](images/89e6498418b1ddbccabb481c6a92d363672025c81a6eb44206e73a0bf59c7973.jpg)



(b) CFu vs. VFID & LSIPS

![](images/febcf53490a0ab7a4a0d239c76980c81fea34fc1fe51d3b4fa082ccb14c74863.jpg)



(c) CFr vs. PNSR & SSIM

![](images/538f51641f6bb11021e0b9bc47380eb8ef12ae19455b3d14607556d0af7e370e.jpg)



(d) CFr vs. VFID & LSIPS   
Fig. 15. Impact of different parameter sizes for the Reconstructor and RecMap Generator on the reconstruction results.

TABLE II PSNR AND SSIM ON RECONSTRUCTING AUTHORIZED OBJECTS AND HIDING UNAUTHORIZED OBJECTS. 

<table><tr><td></td><td>Inpaintor</td><td>PSNR</td><td>SSIM</td></tr><tr><td>authorized objects</td><td>1</td><td>29.807</td><td>0.908</td></tr><tr><td>reconstruction</td><td>2</td><td>29.946</td><td>0.908</td></tr><tr><td>unauthorized</td><td>1</td><td>29.460</td><td>0.912</td></tr><tr><td>objects hiding</td><td>2</td><td>29.466</td><td>0.898</td></tr></table>

Robustness to Mask Shapes: The shape of masks may be slightly modified in the decryption process. We demonstrate that as long as the feature map is correct, OVI is robust to various mask shapes. We use dilated masks $( m a s k _ { d } )$ and bounding boxes of original masks (maskb) to perform object reconstruction with different masks. The results (Tab. III) show consistent object reconstruction and preservation of pixels outside the object regions.

TABLE III FOUR METRICS ON THE RECONSTRUCTION RESULTS WITH DIFFERENT MASKS. 

<table><tr><td></td><td>PSNR</td><td>SSIM</td><td>VFID</td><td>LPIPS</td></tr><tr><td> $mask_{d}$ </td><td>30.778</td><td>0.929</td><td>0.192</td><td>0.041</td></tr><tr><td> $mask_{b}$ </td><td>30.691</td><td>0.928</td><td>0.205</td><td>0.042</td></tr></table>

# VII. DISCUSSION AND CONCLUSION

OVI has two limitations that can be improved in the future. First, we do not theoretically guarantee that no attack is able to reverse inpainting, we plan to to enhance the theoretical security by deep learning interpretability. Second, OVI’s effectiveness is predicated on accurate object segmentation, which depends on either current segmentation methods or manual annotation to obtain precise masks.

OVI is a fine-grained video access control framework that effectively meets different object removal needs by performing inpainting only once. This approach significantly reduces the overhead associated with communication and storage, scaling it down from Θ(n) to Θ(1). We believe that OVI offers a practical and efficient solution for video access control.

# ACKNOWLEDGEMENT

The research is partially supported by National Key R&D Program of China under Grant No. 2021ZD0110400, Innovation Program for Quantum Science and Technology 2021ZD0302900, China National Natural Science Foundation with No. 62132018, 62231015, U23A20308, “Pioneer” and “Leading Goose” R&D Program of Zhejiang, 2023C01029, and 2023C01143.

# REFERENCES

[1] M. Abadi and D. G. Andersen, “Learning to protect communications with adversarial neural cryptography,” CoRR, vol. abs/1610.06918, 2016.   
[2] F. Ahmed, L. Wei et al., “Toward fine-grained access control and privacy protection for video sharing in media convergence environment,” Int. J. Intell. Syst., vol. 37, no. 5, pp. 3025–3049, 2022.   
[3] J. Bethencourt, A. Sahai, and B. Waters, “Ciphertext-policy attributebased encryption,” in 2007 IEEE Symposium on Security and Privacy (SP ’07), 2007, pp. 321–334.   
[4] E. Chatzikyriakidis, C. Papaioannidis, and I. Pitas, “Adversarial face de-identification,” in 2019 IEEE International conference on image processing (ICIP). IEEE, 2019, pp. 684–688.   
[5] M. Daum, B. Haynes et al., “Tasm: A tile-based storage manager for video analytics,” in 2021 IEEE 37th International Conference on Data Engineering (ICDE). IEEE, 2021, pp. 1775–1786.   
[6] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in IEEE CVPR, 2016, pp. 770–778.   
[7] Q. He, B. Jiang et al., “Bps-vss: A blockchain-based publish/subscribe video surveillance system with fine grained access control,” in International Conference on Blockchain and Trustworthy Systems. Springer, 2020, pp. 255–268.   
[8] S. Himmi, O. Ilter et al., “Don’t share my face: Privacy preserving inpainting for visual localization,” in IEEE/RSJ International Conference on Intelligent Robots and Systems, IROS 2022, Kyoto, Japan, October 23-27, 2022, 2022, pp. 12 506–12 511.   
[9] H. Isa, I. Bahari et al., “Aes: Current security and efficiency analysis of its alternatives,” in 2011 7th International Conference on Information Assurance and Security (IAS). IEEE, 2011, pp. 267–274.   
[10] H. Jin, G. Liu, D. Hwang, S. Kumar, Y. Agarwal, and J. I. Hong, “Peekaboo: A hub-based approach to enable transparency in data processing within smart homes,” in 2022 IEEE Symposium on Security and Privacy (SP). IEEE, 2022, pp. 303–320.

[11] A. B. L. Larsen, S. K. Sønderby et al., “Autoencoding beyond pixels using a learned similarity metric,” in International conference on machine learning. PMLR, 2016, pp. 1558–1566.   
[12] Z. Li, C. Lu et al., “Towards an end-to-end framework for flow-guided video inpainting,” in IEEE CVPR, New Orleans, LA, USA, June 18-24, 2022, 2022, pp. 17 541–17 550.   
[13] A. Lugmayr, M. Danelljan et al., “Repaint: Inpainting using denoising diffusion probabilistic models,” in IEEE CVPR, New Orleans, LA, USA, June 18-24, 2022, pp. 11 451–11 461.   
[14] F. Perazzi, J. Pont-Tuset et al., “A benchmark dataset and evaluation methodology for video object segmentation,” in IEEE CVPR 2016, Las Vegas, NV, USA, June 27-30, 2016, 2016, pp. 724–732.   
[15] O. Ronneberger, P. Fischer, and T. Brox, “U-net: Convolutional networks for biomedical image segmentation,” in Medical Image Computing and Computer-Assisted Intervention–MICCAI 2015: 18th International Conference, Proceedings. Springer, 2015, pp. 234–241.   
[16] M. Sabra, A. Maiti, and M. Jadliwala, “Zoom on the keystrokes: Exploiting video calls for keystroke inference attacks,” in NDSS, virtually, February 21-25, 2021. The Internet Society, 2021.   
[17] C. Saharia, W. Chan et al., “Palette: Image-to-image diffusion models,” in ACM SIGGRAPH, Vancouver, BC, Canada, August 7 - 11, 2022, 2022, pp. 15:1–15:10.   
[18] E. Upenik, P. Akyazi et al., “Inpainting in omnidirectional images for privacy protection,” in IEEE ICASSP 2019, Brighton, United Kingdom, May 12-17, 2019, 2019, pp. 2487–2491.   
[19] T. Wang, M. Liu et al., “Video-to-video synthesis,” in NeurIPS, December 3-8, 2018, Montreal, Canada ´ , 2018, pp. 1152–1164.   
[20] Z. Wang, A. C. Bovik et al., “Image quality assessment: from error visibility to structural similarity,” IEEE Trans. Image Process., vol. 13, no. 4, pp. 600–612, 2004.   
[21] B. Waters, “Ciphertext-policy attribute-based encryption: An expressive, efficient, and provably secure realization,” in 14th International Conference on Practice and Theory in Public Key Cryptography, ser. Lecture Notes in Computer Science, vol. 6571, 2011, pp. 53–70.   
[22] S. Winkler and P. Mohandas, “The evolution of video quality measurement: From psnr to hybrid metrics,” IEEE transactions on Broadcasting, vol. 54, no. 3, pp. 660–668, 2008.   
[23] H. Wu, X. Tian et al., “PECAM: privacy-enhanced video streaming and analytics via securely-reversible transformation,” in ACM MobiCom, New Orleans, Louisiana, USA, October 25-29, 2021, pp. 229–241.   
[24] Y. Wu, F. Yang, Y. Xu, and H. Ling, “Privacy-protective-gan for privacy preserving face de-identification,” Journal of Computer Science and Technology, vol. 34, no. 1, pp. 47–60, 2019.   
[25] H. Xiang, Q. Zou et al., “Deep learning for image inpainting: A survey,” Pattern Recognit., vol. 134, p. 109046, 2023.   
[26] N. Xu, L. Yang et al., “Youtube-vos: Sequence-to-sequence video object segmentation,” in Springer ECCV, Munich, Germany, September 8-14, 2018, Proceedings, Part V, ser. Lecture Notes in Computer Science, vol. 11209, 2018, pp. 603–619.   
[27] K. Yang, Z. Liu et al., “Time-domain attribute-based access control for cloud-based video content sharing: A cryptographic approach,” IEEE Transactions on Multimedia, vol. 18, no. 5, pp. 940–950, 2016.   
[28] M. Ye, Z. Tang et al., “Visual privacy protection in mobile image recognition using protective perturbation,” in Proceedings of the 13th ACM Multimedia Systems Conference, 2022, pp. 164–176.   
[29] K. Zhang et al., “Flow-guided transformer for video inpainting,” in Springer ECCV, Tel Aviv, Israel, October 23-27, ser. Lecture Notes in Computer Science, vol. 13678, 2022, pp. 74–90.   
[30] K. Zhang, J. Fu, and D. Liu, “Inertia-guided flow completion and style fusion for video inpainting,” in IEEE CVPR, New Orleans, LA, USA, June 18-24, 2022, pp. 5972–5981.   
[31] R. Zhang, P. Isola et al., “The unreasonable effectiveness of deep features as a perceptual metric,” in IEEE CVPR, Salt Lake City, UT, USA, June 18-22, 2018, 2018, pp. 586–595.   
[32] W. Zhou, Y. Jia et al., “Discovering and understanding the security hazards in the interactions between iot devices, mobile apps, and clouds on smart home platforms,” in 28th USENIX security symposium (USENIX security), 2019, pp. 1133–1150.   
[33] X. Zou, L. Yang et al., “Progressive temporal feature alignment network for video inpainting,” in IEEE CVPR, virtual, June 19-25, 2021, pp. 16 448–16 457.