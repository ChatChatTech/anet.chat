# Cloak of Invisibility: Privacy-Friendly Photo Capturing and Sharing System

Lan Zhang , Member, IEEE, Xiang-Yang Li , Fellow, IEEE, Kebin Liu, Member, IEEE, Cihang Liu , Member, IEEE, Xuan Ding, Member, IEEE, and Yunhao Liu, Fellow, IEEE

Abstract—The wide adoption of smart devices with onboard cameras facilitates photo capturing and sharing, but greatly increases people’s concern on privacy infringement. Here, we seek a solution to respect the privacy of persons being photographed in a smarter way that they can be automatically erased from photos captured by smart devices according to their intention. To make this work, we need to address three challenges: 1) how to enable users explicitly express their intentions without wearing any visible specialized tag, and 2) how to associate the intentions with persons in captured photos accurately and efficiently. Furthermore, 3) the association process itself should not cause portrait information leakage and should be accomplished in a privacy-preserving way. In this work, we design, develop, and evaluate a system, called COIN (Cloak Of INvisibility), that enables a user to flexibly express her privacy requirement and empowers the photo service provider (or image taker) to exert the privacy protection policy. Leveraging the visual distinguishability of people in the field-of-view and the dimension-order-independent property of vector similarity measurement, COIN achieves high accuracy and low overhead. We implement a prototype system, and our evaluation results on both the trace-driven and real-life experiments confirm the feasibility and efficiency of our system.

Index Terms—Photo capturing and sharing, portraiture privacy, privacy protection, smart camera

# 1 INTRODUCTION

NOWADAYS, smart devices with onboard cameras e.g., smart phones and glasses [37], are pervasive in our daily lives. Current smart devices can capture and even share photos anytime anywhere without informing the parties in the photo, e.g., lifeloggers’ wearable cameras, thus raising many concerns on people’s privacy infringement [12]. InfoTrends conservatively forecasted that 1.2 trillion photos will be taken in 2017, approximately 85.0 percent of which will be taken using mobile devices. We conducted an online survey with 224 volunteers, among whom 89.7 percent mostly take photos with their mobile phones. Secretive photographing without clear warning beforehand is privacy violation. Even worse, if the secretively taken photos which contain information beyond what users want to reveal are shared on Internet, it will make users extremely susceptible to various attacks. More than 80 percent of our respondents would like to use new techniques (e.g., installing a privacy

friendly camera app) to respect others’ and their own privacy.

To protect people’s portrait privacy from unwilling photo-taking and publication, many photo service providers or users have taken actions in different ways. For example, some Glass wearers whip their device off in inappropriate situations, such as in gym locker rooms or work meetings; some business bans smart glasses inside their buildings to respect customers’ privacy; and the Glass manufacturer (e.g., Google) does not allow developers to create applications that take photo silently. Those methods, however, are broad-brush and blunt which can significantly hurt the applications of smart devices. Therefore, it is appealing to consider how one might build a system which respects people’s portrait privacy while guaranteeing a comfortable usage of smart glasses/cameras.

Instead of discarding the smart glasses/cameras due to privacy concerns, in this work, we seek a solution for reaching an ultimate goal of privacy-aware Glass/camera, operating transparently to end users [39]. Our solution will let end users to express their privacy requirements and glasses/cameras or photo service providers will exert the privacy protection mechanisms. When taking a photo/ video, the smart device will detect who (in the picture/ video) requested privacy protection, and then remove them from the image automatically. Our protocol can also improve the social augment application by automatically tagging a user in a photo when he/she expresses an interest to share his/her information with surrounding people.

To implement such a privacy-aware camera, we need to address several critical challenges. First, we should enable the user efficiently and flexibly to express his/her intention/ requirements conveniently. Some methods require the user to wear visible specialized tag (e.g., QR code [3]), which is inaesthetic and inconvenient. In this work, we propose a method to encode the user’s portrait feature in the request and transmit it using wireless devices. Then, the second challenge is that we should accurately and efficiently associate each privacy-seeking user with an image region in the photo taken by another user (the photographer ). Furthermore, the association process itself should not cause portrait information leakage and should be accomplished in a privacy-preserving way. Face recognition [23], [31] is widely used to identify people in photos, but in practice it suffers when there is a lack of a clear front view of faces due to the camera’s view angle and distance. Sophisticated but complicated matching schemes may cause high overhead and long delay. The matching problem itself is difficult due to the accuracy and efficiency requirements, let alone completing matching process in a private and non-interactive manner with untrusted server. Matching a user’s privacy-expression with a possible people in a photo can be reduced to some sort of vector matching. Many private vector matching protocols use multi-party computation techniques, which require frequent interactions among participants. Most existing private vector matching methods (in both multi-party computation and outsourced manner) use homomorphic encryption [15], [26] or garble circuit [26], and cause high computation cost for both client and cloud. The third challenge is that the privacy-friendly Glass/camera should be transparent to all users and minimize extra overhead to mobile devices. An ad hoc approach may lead to requirements for “always-on” neighbour discovery, frequent information exchanging as well as complex image matching computation on user devices. To reduce the overhead of users, our protocol will outsource most of these tasks to cloud with a well-designed strategy to prevent privacy leakage to untrusted cloud and other users.

The main contributions of this work are as follows:

To the best of our knowledge, we are the first to present a portrait privacy preserving photo capturing and sharing system. which enables a user to express his/her privacy requirement and empowers the smart devices to exert the protection. We comprehensively analyze the privacy issues during the photo capturing and sharing and define three types of threats. With our approach, people who do not want to be captured in photo will be automatically erased from the photo and verification of the removal is also supported in case the photographer ignores the request.   
For accurate and efficient matching between people’s privacy intentions and people in the photo, we design a graph-based portrait profile and a robust matching algorithm. The graph representation of portrait is sufficiently distinguishable and better-formed for storage and matching than the image. Moreover, our matching mechanism is resistant to pose changes of people and camera, and also compatible for the future development of vision feature description.   
We propose a novel highly efficient encryption-free privacy-preserving vector distance protocol in a non-

![](images/d2f974960348e84ce15dde75db15b10c5f50ff2c2268f5a5aa1841716a9d1ade.jpg)



Fig. 1. Example application scenario of COIN: in the photo, the tagged person is labeled and the invisible person is erased.

interactive manner with untrusted server. Based on our observation, the dimension-order-independent property of distance between vectors, we enable the distance computation on transformed vectors other than cypher blocks, which significantly reduces the computation complexity and communication cost than existing cryptosystem based solutions. With our protocol, most computation tasks are transferred from smart devices to the cloud in a privacy-preserving way, meanwhile the interaction cost is significantly saved.

We design and implement a prototype system and verify the effectiveness of our scheme by extensive experiments as well as case studies.

# 2 MOTIVATION AND PRIVACY REQUIREMENTS

# 2.1 Motivation

In this work we seek a solution to respect the privacy of persons being photographed in a smarter way. As an example shown in Fig. 1, when someone uses his smart Glass to take a photo, people in the field of view (FOV) should be notified (or the photographer should know the privacy protection intentions of people in FOV). Then persons who are unwilling to be photographed, e.g. Neighbor 1, should have a convenient way to specify their privacy intentions, and thus be automatically erased from the photo. We refer to them as invisible users. Users who would like to make friends with the photographer, e.g., Neighbor 2, can be automatically tagged on the photo and share information. We refer to them as tagged users. The photographer just takes other people into the photo as usual. The system can motivate the photographer in two aspects: (1) when respecting other invisible users’ privacy, his/her privacy can also be protected by others; (2) the system supports tagging people automatically, which could be helpful and fun in many scenarios (e.g., social applications). Photo sharing services can benefit from this system by attracting more users who would like to be invisible or tagged in photos. Besides, after one time setting the solution should be transparent to all users and avoid incurring high overhead to their smart devices. Finally, the portrait privacy protection strategy should be well designed and avoid further leakage of any type of private information.

# 2.2 Threats to Portrait Privacy

People may be photographed nearly anytime anywhere without their consent. For example, one cannot notice that a Glass is taking a photo of him/her. Photos contain rich information, including people’s appearance, location, activities, etc.. There are many mature techniques to detect and recognize the objects (e.g., faces and pedestrians) within the photos [20], [31]. Many image analysis techniques, e.g., [20] and [31] can possibly be used to automatically mine sensitive information from photos. Facing massive cameras and image analysis techniques [20], [31], people’s portrait privacy is badly in need of protection. In this work, we focus on protecting users’ portrait information. Here, a portrait not only includes the user’s face but also his/her body, since clothes and accessories could also reveal identification information. We consider three types of threats to portrait privacy, which expose sensitive information to different extend.

Visual portrait privacy. The most intuitive way to violate a user’s portrait privacy is to capture and publish (e.g., through photo sharing systems) a photo containing his/her visible portrait. Simply blurring all faces in images, e.g., [29] and Google Street View, will disable the normal photographing function. In our protocol COIN we propose to match the people in the photo to their privacy protection intentions, and erase only people that should be invisible. There are several critical steps in designing a privacy respecting phototaking and sharing system, including, but are not limited to, 1) privacy expression by potential users in the photo, and 2) privacy respecting mechanism for the photographer. As we will discuss in detail in Section 3, a user expresses his/her privacy requirement by encoding his/her portrait, which clearly cannot be transmitted in its original form (otherwise his/her portrait privacy is broken by himself/herself). Receiving such privacy expression, the photographer need to perform matching to find the correct person to erase. So, we need to provide privacy protections in all these operations.

Portrait feature privacy. This type of threats occur inside some image services, e.g. image matching or face recognition. These services don’t use visible images directly, but take feature vectors of image as the descriptor, e.g., Eigenfaces [31] and color histogram. But users can also be identified by features of portrait image. For example, face images can be reconstructed from face vectors [8]. During the process, the leakage of portrait features also violates users’ privacy.

Inference privacy. Even if an image system hides original images and other information such as their feature vectors, an adversary with a collection of images (an image dictionary) can infer the hidden content using the similarity measurement function of the system. Hence, we should prevent adversaries from obtaining the similarity measuring results to enhance the privacy protection.

There are also other types of user privacy should be respected, e.g. location privacy. A lot of methods have been proposed to provide privacy-preserving location services [17], [21], [33]. COIN leverages existing solutions to protect other user privacy since it is not the focus of this study.

# 2.3 Adversary Model

Our approach defends a user’s portrait privacy against both untrusted cloud server and malicious users. For the cloud, we apply the widely used “honest-but-curious” assumption. The cloud server will follow the protocol, but might conduct extra work to harvest portrait images of invisible people, reconstruct invisible portraits using feature vectors or infer the invisible content using image dictionary. This is a justifiable assumption because deviating from the protocol will lead to poor user experience, thus could cause revenue loss of the service provider. Also, we assume that the cloud won’t collude with any client to conduct an attack. A malicious user could participate in harvesting other users’ portrait information by eavesdropping their communication with the cloud. All users except the photographer should be prevented from obtaining the portrait information of invisible users. Although the photographer already owns the photo of invisible people, he/she may misbehave to preserve the invisible people who should be erased and publish the photo through Internet. So, we also need a verification scheme against dishonest photographers.

# 2.4 Design Goals

We design our system to achieve both the privacy goal and system efficiency goal.

Privacy Goal. COIN is designed to protect invisible users’ visual portrait privacy, portrait feature privacy and inference privacy from participants, the cloud and outsiders. It requires the system to accurately match users’ requests with people in the photo in a privacy-preserving manner.

Efficiency Goal. To lease the burden of mobile participants, our protocol COIN is designed to let the powerful cloud conduct most computation in the non-interactive way as well as reduce the computation and communication cost as much as possible.

Facing critical challenges introduced in Section 1, to achieve this vision, a set of techniques are designed to realize robust portrait matching and efficient privacy preserving outsourced computing which will be discussed in following sections.

# 3 SYSTEM DESIGN OVERVIEW

Facing critical challenges introduced in Introduction. we design our system to achieve both the privacy and system efficiency goals. We first present our baseline system design without privacy-preserving computing. With our graph-based portrait matching algorithm, the baseline approach COIN is effective to protect users’ visual portrait privacy by accurately matching invisible people in photos and erasing them automatically. COIN is sufficient when the server is trusted and the communication channel is secure. But in practice, there is a risk of exposing portrait features to untrusted cloud and other participants. Furthermore, we propose an efficient privacy-preserving outsourced vector distance protocol, based on which an advanced approach COIN++ provides portrait feature privacy and inference privacy protection with little extra overhead for the client. In this section, we will sketch our system architecture.

![](images/cd9463c059b320213541923fffe24ca49c0aa352b325dcf7a7631e423e5c9640.jpg)



Fig. 2. Baseline system architecture (COIN).

# 3.1 Overview of Baseline System COIN

There are three parties involved in our system: the photographer, who takes the photo; the neighbors, who could be in the FOV of the photographer (as presented in Fig. 1); the cloud, who takes charge of location, communication and computation services. As we have discussed, some neighbors want their portrait privacy to be protect and thus are not willing to be photographed. Our goal is to remove the unwilling people from the photo before it is kept and shared. The architecture and workflow of our baseline system are illustrated in Fig. 2, which includes the following major components that are deployed on photographer, neighbors and cloud separately.

The Self Portrait Profile Generation component, located at the neighbor side, creates personal portrait profile of the user. The user will encode his/her portrait profile to express his/her privacy requirement.   
The FOV Portrait Profiles Generation component deployed on the photographer extracts portrait profiles of people from the taken photo.   
The Proximity Service on cloud helps to detect users in proximity that may appear in photographer’s FOV. This component can reduce the computation cost of cloud and communication cost of end users. For users’ location privacy, we use existing privacypreserving location services, e.g., [21].   
The Matching Service on cloud conducts portrait profile matching tasks to determine people that should be erased from the photo.   
The Privacy Concealing component, located on photographer, erases invisible people from the photo automatically before uploading.   
The Verification Service runs on cloud side to take charge of verifying the removal of invisible people, in case there are dishonest photographers.

We would like to take a typical photographing process as an example to describe the functionality of each component and the system workflow. Each user creates his/her personal portrait profile using the Self Portrait Profile Generation component and encode his/her portrait profile to express his/her privacy requirement, e.g., he/she can choose his/ her status from “invisible me” (or “tag me”) in the mobile phone app to make himself/herself an invisible (or tagged) user. Besides portrait profile, each user can also specify locations he/she wants to protect his/her privacy, e.g., he/she can set a hospital as a private location and a photo captured at this hospital should remove him/her from it. In our design, a set of vision feature vectors are extracted from subregions of a portrait image. Both face and body features are extracted, in case that there may be a lack of clear front view of face. We design a graph structure to encode the extracted vision features (feature vectors are properties of nodes) and use the graph as the portrait profile, as the examples in Fig. 4. Different types of graph nodes own different types of feature vectors, e.g., face feature vector for Node No.5, color and texture vectors for Node No.6. A label is associated with each node to indicate its type. The selected featured should be invariant to scaling, rotation, and partially invariant to change in illumination and camera viewpoint. As the evolving of computer vision techniques, new features can conveniently be introduced to our system. Compared with uploading the original image, the feature graph shows a low risk on privacy leakage without lose of matching functionality, and are much more efficient for both computation and communication. Besides, the graph representation is highly robust against pose changes of people and cameras. For each invisible user, his/her self portrait profile is generated once and for all until he/she updates it. While the face features of a user remains the same, the user could change his/her outfits. The face and upper body portrait profile could be automatically updated when the user takes a selfie or while he/she uses the phone with the frontal camera facing himself/herself. He/she can also obtain the whole body image with the help of a mirror or a friend. In our advanced approach, transformed version of portrait graph are used to improve privacy protection, and we convert the people matching problem to graph matching problem.

Triggered by a photo shooting action, the Proximity Service on cloud will automatically start to check if there are invisible people in the FOV of the photographer or any users, whose current location is unavailable, have predefined this place as their private location. If any, the cloud will record the status and inform them and start the next step. Proximity service can be realized easily using existing location service and onboard compass. For example, Wi-Fi based localization can achieve 1-2 meter level accuracy [22]. It is not always convenient to recognize an accurate FOV, which needs parameters and the current orientation of the camera. In practice, the cloud could efficiently search invisible neighbors (located within a certain distance) of the photographer and take them as potential people appearing in the photo. With limited number of potential matched invisible users, our system can achieve high matching accuracy and low overhead.

In the next step, after being informed by cloud, invisible neighbors upload their self portrait profiles to cloud (this could be done in advance to reduce the delay or in case they may not have Internet connection sometimes). Meanwhile, the photographer detects all people in the photo and extracts their portrait profiles with the FOV Portrait Profiles Generation component, which works similarly to self portrait profile generation. These profiles will be uploaded to cloud as well. Then the Matching Service will match portrait profiles of invisible users to portrait profiles from the photo and determine people that should be erased from the photo. The graph matching algorithm will be discussed in detail in the following section. The matched results will be sent to photographer, and then the Privacy Concealing component will erase the corresponding image regions of invisible people from the photo automatically by blurring or other more sophisticated techniques, like image inpainting [7], [16], to maximize the aesthetics. We show an example of removing invisible people from photo in Fig. 5. For the inpainting, we use the code from Criminisi’s work [7]. Specially, if the photographer doesn’t have Internet connection when he/she ia taking photos, he/she can record the photo taking place and conduct the matching and concealing processes whenever he/she connects to the Internet. After the removal, the photographer can store or share the photo using the cloud service. Note that, based on the personal specification, the whole procedure works the same way for tagged users and the “erase” operation can be alternated to “tag” to augment many social applications.

![](images/d562b8e7cd63054f3ad2540c7965857b023e2ee1b8361f9dfbced935f464b8a1.jpg)



Fig. 3. Advanced system architecture (COIN++).

In case there are dishonest photographers who ignore the request or don’t complete the removal, COIN supports verification of removal. All invisible users’ portrait profiles have been uploaded to the cloud in the previous stage. Once the photo is shared through Internet, the Verification Service will check the photo as follows the cloud first conducts a people detection on the photo and extracts all portrait profiles; then the cloud matches these profiles with the cached profiles of invisible neighbors, if there is a matching, it can tell that the photographer didn’t follow the protocol. The verification process can be completed alone by the cloud without any interaction with users.

# 3.2 Overview of Advanced System COIN++

The baseline protocol protects the visual privacy of people’s portraits, but exposes users’ portrait profile (i.e. feature vectors) to the cloud and even the eavesdroppers. With some feature vectors an adversary could have a chance to match them with existing photos or even reconstruct the photo. In the advanced approach, we retain the visual portrait privacy protection and improve the system to protect users’ portrait feature privacy and inference privacy. In other words, the graph based profile matching scheme should be conducted in a privacy-preserving manner. The core of the portrait profile matching algorithm is to measure the distance between vision feature vectors. We cannot directly adopt existing privacy-preserving vector distance protocols based on homomorphic encryption [15], [26] and garbled circuit [26] due to their large computation and communication cost. In our system we propose a highly efficient outsourced vector distance protocol (see Section Privacy Enhanced System). As shown in the red blocks in Fig. 3, based on our observation, the dimension-order-independent property of distance between vectors, we propose a well designed scrambling scheme and combine it with locality sensitive hash. With our design, all invisible neighbors can secretly transform their vectors in a distance preserving way. Then the cloud can measure vector distances using the transformed vectors and match transformed portrait graph with the same algorithm as in the baseline system. Our scheme protects invisible users’ portrait profiles (from both himself/herself and the photographer) with little extra cost on the client side. But, it saves computation cost for the cloud, because the distance computation of high-dimensional real number vectors is converted to distance of low-dimensional binary hash code.

![](images/14178bd27a7b711b2d4d98db3cf71b95827fa4fb66ff4ba77160384bc90a6332.jpg)



Fig. 4. Portrait graph representation.

The architecture of the advance system is presented in Fig. 3, except vector transformation and verification, other components are the same as that in the baseline system. Here, the verification is more challenging, because the cloud only knows the transformed portrait graphs of invisible users. Without knowing the secret transformation, the cloud cannot compare them with portrait graphs extracted from the uploaded photo directly. When an invisible user needs to check if his/her portrait has been removed, he/she need to start a verification and participate in the process as follows: the cloud sends all extracted feature vectors in a random order to the invisible user. Note that, these feature vectors are supposed to belong to preserved visible people if the photographer is honest. And the invisible user transforms them in the same way as his/her self feature vectors and sends the results transformed vectors to the cloud. Then the cloud can compare preserved people in the photo and invisible neighbors using transformed portrait graphs, and detect the dishonest photographer.

# 4 PORTRAIT PROFILE GENERATION AND MATCHING

# 4.1 Portrait Profile Generation

In this work, we design a distinguishable graph representation of portrait. Compared with the original pixel image, portrait graph extracts components of the portrait and describes their connectivity, hence it is more robust to changes of the person’s pose and the camera’s view angle. Portrait graph is also more efficient for storage, transmission and matching, and shows a lower risk on privacy leakage. After applying people detection on a photo [20], [32], we obtain portrait images (including both people faces and bodies) from the photo as shown in the first subfigure of Fig. 4. Then portrait image can be segmented into adjacent regions by different colors and textures [1], [10]. Given one portrait image, a graph $G = ( V , E )$ can be constructed, where V is a set of nodes representing segmented regions and E are edges connecting any two regions that share a boundary. Figs. 4 and 7 illustrate some examples of our graph representations for portraits.

![](images/fc76aa0430da55841a5448d821a6180a656c93f3176f1ed5de69a92bb2c40375.jpg)



Fig. 5. Example of automatic privacy concealing (erase invisible people from photos) by image inpainting [7] or blur.

Foreground Extraction. Now we have obtained the graph structure of a portrait image, However, some regions/nodes could be the background, which could deteriorate the matching correctness and efficiency. Then we measure each node’s confidence of being a part of the person, and remove the node with low confidence to eliminate the background. Basically, the confidence is obtained by fusing evidences using Dempster Shafer theory (DST) [28]. Two types of evidences are used. The first cue is the border weight (BW) of a region, which describes the extend that the region shares its boundary with the border of the portrait image.

$$
B W = \frac {\text { length } (\text { region   boundary } \cap \text { window   border })}{\text { length } (\text { window   border })}. \tag {1}
$$

Border weight gives an evidence that a region doesn’t belong to the entity with a probability interval BW; 1 . The ½ other cue is the center weight (CW), which describes the distance from the mass center of a region to the center of the portrait image.

$$
C W = 1 - \frac {\text { distance } (\text { region   center,   window   center })}{\max (\text { distance } (\text { region   center,   window   center }))}. \tag {2}
$$

Center weight gives an evidence that a region belongs to the entity with a probability interval CW; 1 . Combing two ½ probability intervals by DST produces the confidence of this region. Fig. 4 shows examples of foreground extraction and portrait graph generation, which provide more accurate graph representation of people portrait. The result of foreground extraction can also be employed by the privacy concealing component as the accurate erase area to achieve better looking removal, as shown in Fig. 5.

Node Properties. Segmentation not only yields the portrait graph structure, but also results in relatively consistent color and texture for each region. For each region of portrait, vision feature vectors, e.g., face feature vector (e.g., eigenfaces vector [31]), color histogram and texture vector, are extracted as property of the corresponding node. For the node of human face, (e.g., Node No.5 in Fig. 4), face feature vector, e.g., eigenfaces [31], can be extracted. For body nodes, we can use feature vectors invariant to scaling, rotation and partially invariant to change in illumination and camera viewpoint, for example, color and texture. For each feature, various description vectors have been designed. We will give more details about node properties in the implementation section.

# 4.2 Portrait Graph Matching Scheme

To achieve accurate and efficient portrait graph matching, there are several challenging issues should be addressed with low computation cost: graph structure of the same person varies due to changing illumination condition and viewpoint; incomplete graphs could be produced due to occlusion; portrait profile could still contain some noisy nodes from background. As a result, the matching algorithm should be elastic to node/edge division, aggregation, insertion and deletion, and robust to noise nodes. Existing graph matching methods usually have application-oriented specifications [13], [14], [34], e.g., assumptions about node numbers, graph structure and pre-knowledge of correspondences, making them difficult to be directly applied in this work. To meet the critical requirements of portrait profile matching, we design a voting based strategy in which both the node similarity and graph structure are considered.

Let graph $G ^ { x } = ( V ^ { x } , E ^ { x } )$ denote portrait profile X (say ¼ ð Þproduced by a user) and $G ^ { y } = ( \bar { V ^ { y } } , E ^ { y } )$ denote portrait ¼ ð Þprofile Y (say produced by a photographer). Here $V ^ { x } =$ $\{ v _ { 1 } ^ { x } , v _ { 2 } ^ { x } , . . . , v _ { p } ^ { x } \}$ and $V ^ { y } = \{ v _ { 1 } ^ { y } , \mathbf { \bar { { v } } _ { 2 } ^ { y } , . . . , \mathbf { \bar { { v } } _ { q } ^ { y } } } \}$ ¼. Each node owns some f g ¼ f gfeature vectors as its property. In order to improve matching accuracy as well as speed up the computation process, we add a label to each node according to the result of face detection, which describes its type, for example, human face or human body. Only nodes of the same type can be matched. The similarity between two nodes of different types is zero. As human face is a strong feature to identify a person, our matching scheme will first consider the matching between nodes labeled with “human face” (e.g., Node No.5 in Fig. 4), then invoke an integrated graph matching. In this way, our method provides more accurate and robust matching than existing face recognition based methods.

Initialization. Let the similarity between nodes $v _ { i } ^ { x }$ and $v _ { j } ^ { y }$ be $\mathbf { S } ( v _ { i } ^ { x } , v _ { i } ^ { y } )$ , which can be obtained through measuring the ð Þdistances between feature vectors of two graph nodes. Note that, if $v _ { i } ^ { x }$ and $v _ { i } ^ { y }$ have different type labels, $\bar { \mathbf { S } ( \ b { v } _ { i } ^ { x } , \ b { v } _ { i } ^ { y } ) }$ is set to ð Þzero. In the next section, we will discuss the details of privacy preserving vector distance computation. During the matching process, a matrix M with p rows and $q$ columns is built. Each entry $M _ { i j } = \{ f _ { i j } , n _ { i j } , c _ { i j } \}$ of the matrix is a triple where $f _ { i j }$ ¼ f gis a boolean flag indicating whether node $v _ { j } ^ { y }$ is a possible match for node $v _ { i } ^ { x } , n _ { i j }$ caches the one-hop neighbor match information and $c _ { i j }$ is a counter. Details of these parameters will be presented in the following parts. A match is represented as an assignment for all $\{ { \bar { f } } _ { i j } \}$ , where there is at most one $f _ { i j }$ f gequaling TRUE for every column j. $\operatorname { A l l } \left\{ f _ { i j } \right\}$ are initiated to TRUE.

f gAfter the initialization, our graph matching scheme consists of three stages.

Stage 1. We eliminate wrong matches based on the similarities of node pairs. If ${ \bf S } ( v _ { i } ^ { x } , v _ { i } ^ { y } )$ is above a pre-specified threshold $\xi _ { s } ,$ ð Þthe corresponding flag $f _ { i j }$ is set to TRUE, otherwise, we eliminate this match by setting $f _ { i j }$ to FALSE. Note that, a node in $V ^ { x }$ does not necessarily have a possible match in $V ^ { y } ,$ thus there can be rows with all FALSE flags.

![](images/1393de98893ab1af8d554d8209b5d969a08b195d7030486ac651ec6ff1db98bb.jpg)



(a)

![](images/be1a3281be01f2e4a53885ba3e21c022820e94dcae55671d50c994579d82e595.jpg)  
(b)

![](images/1032d5db9ea8d1636058ad6eb79c26bcdff4ea2db054ad1d75f2bb39522a68fa.jpg)



(c)   
Fig. 6. Example of portrait profile matching.

After this stage, all node pairs with TRUE flags are considered as candidate matches.

Stage 2. We explore the one-hop neighbor matching for each candidate match. For each candidate match $( v _ { i } ^ { x } , v _ { j } ^ { y } )$ , the neighbor sets of $v _ { i } ^ { x }$ and $v _ { j } ^ { y }$ are denoted as $N E ( v _ { i } ^ { x } )$ and $N E ( v _ { j } ^ { y } )$ . We find the most likely mapping from $N E ( v _ { i } ^ { x } )$ to $N E ( v _ { i } ^ { y } )$ ð Þ. To achieve this, we first look for potential matches ð Þin matrix M for each node in $N E ( v _ { i } ^ { x } )$ . We then connect each node in $N E ( v _ { i } ^ { x } )$ ð Þwith its matched nodes in $N E ( v _ { j } ^ { y } )$ with ð Þ ð Þundirected edges, as shown in Fig. 6b. Nodes in both sets as well as the edges form a bipartite graph and the problem can be transformed to find a maximum match on the bipartite graph. To address this problem, we apply the Hungary algorithm [18] which outputs a mapping from $N E ( v _ { i } ^ { x } )$ to $N \bar { E } ( v _ { j } ^ { y } )$ ð. As mentioned above, the mapping is denoted as $n _ { i j } .$ .

$$
n _ {i j} (v _ {a} ^ {x}) = \left\{ \begin{array}{l l} v _ {b} ^ {y} & \text {if} v _ {a} ^ {x} \text {matches} v _ {b} ^ {y} \\ \Phi & \text {if there is no match in} N E (v _ {j} ^ {y}) \text {for} v _ {a} ^ {x} \end{array} \right.
$$

where $v _ { a } ^ { x } \in N E ( v _ { i } ^ { x } )$ and $v _ { b } ^ { y } \in N E ( v _ { i } ^ { y } )$ .

2 ð Þ 2 ð ÞStage 3. We choose at most one assignment for each node in $V ^ { x }$ by a voting based scheme. For each candidate match $( v _ { i } ^ { x } , v _ { j } ^ { y } )$ , we build two trees rooted at $v _ { i } ^ { x }$ and $v _ { j } ^ { y }$ on graph $G _ { x }$ and $G _ { y }$ respectively. The two trees are traced in parallel on two graphs with the BFS method. Here we restrict the tree growth to the constraint that, once a node $v _ { k } ^ { x }$ on $G _ { x }$ and its matched node $v _ { g } ^ { y }$ are appended to the trees, the neighbors of $v _ { k } ^ { x }$ which have not been included can be added to the tree only if they have matched nodes in $N E ( v _ { g } ^ { y } )$ according the recorded mapping $n _ { k g } .$ ð Þ. When two trees have grown to the maximum size, we get a possible match for the subgraphs. In this approach, we propose a voting scheme to determine the best match. That is, for each candidate match $( v _ { k } ^ { x } , v _ { q } ^ { y } )$ on the two trees, we increase the counter value of $c _ { k g }$ Þin entry $M _ { k g } .$ . After trees of all candidate matches $( v _ { i } ^ { x } , v _ { j } ^ { y } )$ voted, we check the $c _ { i j }$ in each entry $M _ { i j }$ ð Þand retain the largest one for each column. Then matrix M indicates a most likely match of $G ^ { x }$ and $G ^ { y }$ and the similarity between the two portrait profiles are calculated by integrating similarities of all matched nodes and edges.

$$
\mathbf {S} (G ^ {x}, G ^ {y}) = \frac {\sum_ {f _ {i j} = \mathrm{TRUE}} \mathbf {S} (v _ {i} ^ {x} , v _ {j} ^ {y})}{\parallel V ^ {x} \parallel + \parallel V ^ {y} \parallel} + \frac {\sum_ {e _ {a b} \in E ^ {x}} \sum_ {e _ {c d} \in E ^ {y}} \delta (e _ {a b} , e _ {c d})}{\parallel E ^ {x} \parallel + \parallel E ^ {y} \parallel}
$$

where

$$
\delta (e _ {a b}, e _ {c d}) = \left\{ \begin{array}{l l} 1 & \text { if } f _ {a c} = T R U E \& f _ {b d} = T R U E \\ 0 & \text { otherwise. } \end{array} \right.
$$

# 5 PRIVACY ENHANCED SYSTEM

We enhance our system to protect users’ portrait feature privacy and inference privacy by conducting the portrait graph matching in an outsourced and privacy-preserving manner, whose core is measuring the Euclidean distance between feature vectors privately and efficiently. As one of the main contributions, we propose a novel highly efficient encryption-free privacy-preserving vector distance protocol in a non-interactive manner against untrusted server. We gain the chance by observing that the distance between two vectors is independent to their dimension order, since the vector distance is measured in a dimension-wise way. Based on the observation, we propose to transform the original vectors to randomly ordered vectors in a distance preserving way, and keep the transformation a secret to adversaries. This design enables us to measure distance on transformed vectors as on original vectors (which means light-weight computation), but the adversary cannot obtain the original vectors nor compute the distance between the transformed vectors and vectors from a dictionary to infer the original ones.

Let the distance function of two vectors $\mathbf { x } =$ $( \mathbf { x } _ { 1 } , \mathbf { x } _ { 2 } , \cdot \cdot \cdot ) , \mathbf { y } = ( \mathbf { y } _ { 1 } , \mathbf { y } _ { 2 } , \cdot \cdot \cdot ) \in \mathbf { V }$ be ${ \mathsf { d } } ( \mathbf { x } , \mathbf { y } )$ ¼. As shown in ð   Þ ¼ ð   Þ 2 ð ÞFig. 3, we design the transformation with two main building blocks: Profile Scrambling and Locality Sensitive Hash $( L { \bar { S } } H )$ . The profile scrambling module works based on our observation that vector distances are dimension-orderindependent, that is when we randomly change the dimension order of both x and y consistently to obtain scrambled $\mathbf { x } ^ { \prime }$ and ${ \bf y ^ { \prime } } ,$ we have $\mathsf { d } ( \mathbf { x } , \mathbf { y } ) \equiv \dot { \mathsf { d } } ( \mathbf { x } ^ { \prime } , \mathbf { y } ^ { \prime } )$ . Once the ð Þ  ð Þscrambling order is kept secret, the original vectors are protected and a dictionary based inference is prevented. In case there may be some dimension-dependent characteristics of vision feature vectors, e.g., in the color histogram the dimensions representing red component usually have large values, we employ the LSH module to transform the scrambled feature vectors into another lowdimensional vector space. LSH hides the scrambled feature vectors from all parties and makes the statistic analysis on scrambled vectors infeasible, meanwhile it also preserves the distance among vectors. Besides, lowerdimension vectors reduce the cost for vector distance computation and vector transmission. Moreover, changing the dimension order of x randomly to $\mathbf { x } ^ { \prime }$ makes their hashes totally different, because there is a random distance between them. Hence, the vector scrambling works like a random salt, which strengths the security property of LSH and makes the dictionary attack against LSH infeasible. Combining vector scrambling and LSH, we protect feature vectors of invisible users from untrusted cloud and other parties, and outsource most computation to the cloud in a secure and noninteractive manner.

Before we present our privacy-preserving vector distance protocol, we first introduce the LSH based vector distance measurement as a preliminary. The key insight behind LSH is that it is possible to construct hash functions such that close vectors will have the same hash value with higher probability than vectors that are far apart. Different LSH functions are designed for various distance metrics, e.g., Euclidean distance, Hamming distance, cosine distance. In our system, we use the commonly used Euclidean distance $\begin{array} { r } { \mathsf { d } _ { E } ( \mathbf { x } , \mathbf { y } ) = \sqrt { \sum _ { i } ( \mathbf { x } _ { i } - \mathbf { y } _ { i } ) ^ { 2 } } } \end{array}$ . Particularly, for high-dimenð Þ ¼ ð sional vector space $\mathbf { V } = R ^ { D }$ with Euclidean distance, an ¼LSH function is defined as follows [9]:

$$
\mathbf {H} (\mathbf {x}) = <   h _ {1} (\mathbf {x}), h _ {2} (\mathbf {x}), \dots , h _ {m} (\mathbf {x}) > \tag {3}
$$

$$
h _ {i} (\mathbf {x}) = \left\{ \begin{array}{l l} 1 & \text { if } \frac {\mathbf {a} \cdot \mathbf {x}}{W} \geq 1, i = 1, 2, \dots , m \\ 0 & \text { otherwise }, \end{array} \right. \tag {4}
$$

where $\mathbf { a } \in R ^ { D }$ is a random vector with each dimension 2chosen independently from the standard Gaussian distribution $N ( 0 , \bar { 1 } )$ . Here each $h _ { i }$ is an atomic LSH function, ð Þand the LSH function H generates a hash vector of the input vector by concatenating m scalar atomic hash values. The window size W and m control the distance range that the mapping is sensitive to. In the advance system, the cloud determines the hashing function H and publishes it to all participants. According to the definition of LSH, the differences between hash vectors indicate the distance between original vectors. In this work we apply the Hamming distance between hash vectors to approximate the distance between original vectors. Our experimental results show that the Hamming distance between hash vectors is nearly monotonic to distance measurement between original vectors.

# 5.1 Outsourced Privacy-Preserving Distance Computing

As illustrated in Fig. 3, to outsource portrait matching to could in the privacy-preserving manner, each participant should transform his/her vectors by first scrambling the their dimension order and then conducting LSH on the scrambled vectors. Portrait graph with transformed vectors are uploaded to cloud for portrait matching. Here, we assume that each user shares a secure communication channel with the cloud. Then the transformed vectors are protected from other participants. In a specific round of photographing, to preserve distance between transformed vectors, the challenge is that all participants (photographer and invisible neighbors) must scramble their feature vectors in a consistent order individually and secretly. We refer to the scramble order as scramble code SC. To achieve the same SC, all participants first need to generate a same random seed R secretly. The multi-user agreement protocol requires that the untrusted cloud cannot learn the random seed and the scramble code, although it controls all communications between users.

# 5.1.1 Random Number Exchange

There are many well-designed group key agreement protocols [6], [19], but most of them require multiple communication rounds among participants, which could cause long delay. Utilizing the honest-but-curious cloud and secure communication channels between the cloud and users, we adapt the practical distributed group key agreement protocol proposed in [6] to achieve round optimum and efficient random number agreement. Let $\bar { U _ { 1 } } , \dots , U _ { n }$ be a dynamic subset of all users who want to generate a common random number and our protocol is presented in Algorithm 1. With this protocol, the photographer and his/her invisible neighbors can obtain the same random number, while the cloud learns nothing about the random number.

# Algorithm 1. Random Number Agreement

# System Initialization:

Cloud generates and publishes system parameters: 1) a large prime number $p = \Theta ( 2 ^ { c N } ) ,$ , a constant $c \geq 1 ,$ $q = \Theta ( \bar { 2 } ^ { N } )$ and $g \in Z _ { p }$ ¼of order $q = \Theta ( 2 ^ { N } )$ .

¼ ð ÞEach user $U _ { i }$ 2 ¼ ð Þgenerates his private parameter $a _ { i } \in Z _ { q }$ and public parameter $b _ { i } = g ^ { a _ { i } }$ mod p and sends $b _ { i }$ 2to the cloud.

Cloud checks that $b _ { i } ^ { q } \equiv 1$ mod p for all $i = 1 , \ldots , n .$

# Runtime:

1: Cloud arranges n users’ indices in a cycle and sends $b _ { i - 1 }$ and $b _ { i + 1 }$ to each $U _ { i } , i = 1 , \ldots , n .$   
2: Each $U _ { i } , i = 1 , \ldots , n$ ¼computes $c _ { i }$ and sends it to cloud

$$
c _ {i} = (b _ {i + 1} / b _ {i - 1}) ^ {a _ {i}} \bmod p. \tag {5}
$$

3: Cloud sends $c _ { 1 } , \cdots , c _ { n }$ to each $U _ { i } , i = 1 , \ldots , n .$

4: Each $U _ { i } , i = 1 , \ldots , n$ ¼computes the random number

$$
R _ {i} = (b _ {i - 1}) ^ {n a _ {i}} \cdot c _ {i} ^ {n - 1} \cdot c _ {i + 1} ^ {n - 2} \dots c _ {i - 2} \bmod p. \tag {6}
$$

Although each user generates Ri individually, all $R _ { i }$ equal to the same random number

$$
R = g ^ {a _ {1} a _ {2} + a _ {2} a _ {3} + \dots + a _ {n} a _ {1}} \bmod p. \tag {7}
$$

# 5.1.2 Scramble Code Generation

After obtaining consistent random seed R, each participant generates the scramble code using Algorithm 2, and rearranges the dimension order of each feature vector according to the scramble code.

# Algorithm 2. Scramble Code Generation

Input: Vector dimension $N ;$ Random number $R ;$ Sorted set ${ \cal S } = \{ 1 , 2 , \ldots , N \} ;$

¼ f gOutput: Scrambled dimension sequence $\mathbf { S C } ;$

1: for $k = N - 1 ; k > = 0 ; k - { \bar { - } }$ do   
2: $i = R / k ! ;$   
3: $\mathbf { S C } [ N - k ] = S [ i ] ;$   
4: ½   ¼ ½ Remove S i from $S ;$   
5: $R = R$ ½ mod k!;   
¼6: end for   
7: return SC;

As illustrated in Fig. 3, after scrambling feature vectors, the photographer and invisible neighbors apply LSH to scrambled vectors to get transformed vectors for current round. The cloud can simply use the transformed vectors to compute distance and conduct the same graph matching algorithm as in the basic scheme. While the membership doesn’t change, the random number remains the same. In this case, the photographer can use the same random number to generate transformed vectors for new photos, and all invisible neighbors do not need any recalculation. When the membership changes, the cloud can insert/remove users into/from the existing ring of Algorithm 1 to update the random number for a new round. Note that, in this case, most users do not need to recalculate the Step 2 in Algorithm 1. Based on our evaluation, the runtime of random generation is usually only 0.014s, which is negligible for human movement. Once the random number is updated, the system achieves randomized transformation outputs for the same feature vector in different rounds.

![](images/83a859982cfcbcd7b8f811f62af84a47a8332034ad2e8658de1fae460ef829c1.jpg)



Fig. 7. Sample portrait images and their portrait profile, including the original image, detected foreground, and portrait profile graph. (The faces are blurred for the purpose of anonymity.)

# 6 IMPLEMENTATION AND EVALUATION

We implement prototype systems of both variants COIN and COIN++ . To support automatic people detection, we implement the most popular face detection [32] and pedestrian detection [20] algorithm based on OpenCV. To generate portrait graph, Many segmentation methods exist in the computer vision field [1], [10]. In our prototype, we adopt JSeg [10] for image segmentation, because it achieves good results with acceptable computation cost. The color threshold of JSeg is set to 100 and the merge threshold is set to 0.6, which work fine in all evaluations. Leveraging the library of MPEG-7, a 48-byte eigenfaces vector [31] is extracted as the property of a node labeled with “face”, and a 64-byte color histogram vector and a 20-byte texture vector (edge histogram with 4 blocks and 5 orientations) are extracted as the property of other nodes. Eigenface is a very popular face feature vector due to its high efficiency, but it can be affected by lighting, scale and rotation. Note that, COIN is compatible with any other vector-based feature descriptors, more advanced descriptors can also be adopted. Obtaining the matching results, invisible people are removed from the photo by blurring and inpainting [7], as shown in Fig. 5. Except the image processing, all other building blocks are realized using Java, including portrait graph matching, LSH, random number agreement, vector scrambling and the messaging module. The client side is developed as an app on Android platform for case study. A user starts this app by inputting his/her portrait profile via selfieing, and chooses his/her status from “invisible me”, “tag me” or “do nothing”. A photographer can use this app to capture photos, which processes images according to the matching results.

# 6.1 Case Study and Experiment Setup

To test the practicality and efficiency of COIN the evaluation is conducted in a crowded real-life scenario: a networking workshop with more than 50 attendees in a 200 $m ^ { 2 }$ meeting hall. 10 volunteers (4 female and 6 male) acted as invisible users and also photographers. Within one day, the volunteers took photos freely and our system recorded the cost and photos. After the experiment, we got 208 photos. 1326 pedestrians are detected which belong to 42 individuals (7 female and 35 male), but only 412 faces are detected. The reason is that, pedestrian detection is much more robust from different view points, but face detection requires the frontal face of people. It implies that a whole body detection and description (e.g., our graph model) is more robust to changes of people’s pose and the camera’s view angle. Fig. 7 shows some sample pedestrian images and their portrait graphs extracted by our system. In our evaluations, we do not consider those people in photo who cannot be detected by our prototype, since they are usually very small or occluded badly. Besides, the detection rate could be improved with more sophisticated people detection algorithm, which is out of the scope of this work. For evaluation only, we manually labeled all captured people as the ground truth.

![](images/4dad8b10618ddda753739b9e83e01b0ade26cfb1abeecbd6f45b6dfac3d26f68.jpg)



Fig. 8. Portrait similarity variances.

Experiment Setting. In the experiments, we use three types of phones as clients: HTC G10 (1024 Hz CPU and 768 M RAM), HTC G23 (1536 Hz CPU and 1G RAM) and HTC New One (1741 Hz CPU and 2G RAM). One laptop is used as the cloud: ThinkPad X1 with i7 2.7 GHz CPU and 4 GB RAM. Before experiments, we need to decide the parameter $\xi _ { s }$ of the matching methods, which is the threshold to eliminate unmatched nodes in Stage 1. We conduct pair-wise portrait graph matchings on the dataset with different settings of $\xi _ { s } .$ . When $\xi _ { s }$ increases from 0 to 0.5, average matching time for a pair of portrait graphs is cut down by 30 percent, with little hurt to the similarity measurement. But while $\xi _ { s }$ continues to increase, it eliminates more and more true match pairs. As a result, we set $\xi _ { s } = 0 . 5$ in ¼our experiments. We also need to determine the parameter of the LSH algorithm. The accuracy of distance measurement using LSH increases with bigger m (longer hash code) and smaller W (smaller window). According to the analysis in [9] and the statistics of our dataset, we set the W to 3 and m to 128, then the hashed vector is 128 bit. For the random number generation, N is set to 512, which provides sufficient protection for the random number agreement protocol.

# 6.2 Matching Accuracy

Here we investigate the most important metric, the portrait matching accuracy, which determines the correctness of invisible people removal and visible people tagging.

We start by examining the consistency and distinguishability of user’s portrait graph by self-similarity (similarity between the same entity’s portrait graphs) and cross-similarity (similarity between different entities’ portrait graphs). In this evaluation, we remove the face property since it is highly distinctive but cannot always be obtained. Fig. 8 presents the evaluation results using the dataset. The upper blue line stands for mean self-similarity for each entity, and the lower red line is mean cross-similarity between this entity and all other entities. We notice that, generally portrait graph has a good consistency, i.e., high self-similarity and small variance. And the obvious gap between self-similarity and cross-similarity shows a good distinguishability, which also shows that our graph representation is highly robust for pose changes of people and cameras. Hence, in most cases, portrait graph can provide accurate matching without face features, which also implies better privacy protection.

![](images/c91c4ff8d0195194c868d2cf634ced8fd406f0bb261744e8fff059451eb70231.jpg)



Fig. 9. FP and FN in basic scheme.

Then, we evaluate the matching correctness by analyzing all possible combinations using the dataset. A false negative (FN) happens when a user A is invisible, but not removed from the photo due to a match score lower than threshold $\theta _ { s } . \mathrm { ~ A ~ }$ false positive (FP) happens when user A is invisible, but another visible user C is removed due to a higher match score than both the threshold and A’s score. In COIN, matching is conducted on portrait graph with plain feature vectors. Fig. 9 illustrates the percentage of FN and FP changing with different threshold $\theta _ { s }$ . We can see that, though smaller $\theta _ { s }$ causes higher false positive, the false positive rate remains smaller than 2.5 percent. It proves that, our portrait graphs achieve robust matching results, that is if there is an invisible user in the photo, we hardly remove a wrong person from the photo. However, false negative rate increases significantly with $\theta _ { s \prime }$ because larger $\theta _ { s }$ will exclude invisible users’ portrait graph with low match scores. By selecting the threshold $\theta _ { s } = 0 . 5 ,$ , ¼COIN achieves 0.5 percent false negative (99.5 percent recall) and 2.1 percent false positive (97.9 percent precision) without using any face property. With face property, the false negative decreases to about 0.1 percent and false positive is less than 1 percent. If we use deep learning techniques for highly accurate face recognition, e.g., DeepFace [30], we can achieve 0.1 percent false negative whole about 0.5 percent false positive. In COIN++, feature vectors are transformed by scrambling and LSH. While the scrambling retains the accurate distance between vectors, LSH could cause some accuracy loss. Will the transformation reduce the matching accuracy? With appropriate parameters m  128 and $W = 3 ,$ COIN++ achieves comparable accu-¼ ¼racy with COIN, as shown in Fig. 10. When $\theta _ { s } = 0 . 5 ,$ , the ¼false negative is about 0.7 percent (99.3 percent recall) and the false positive is about 2.9 percent (97.1 percent precision) without any face property. In summary, both variants support accurate matching and our vector transformation achieves good portrait feature privacy protection with little accuracy loss.

![](images/933178e3a214322377c43df3bac11459a7a6ce15534818a98952f27dbaf074a9.jpg)



Fig. 10. FP and FN in advanced scheme.

# 6.3 Micro Benchmark

# 6.3.1 Communication Cost

In COIN, each face node takes 48B and every other node takes 84B. The size of the portrait graph depends on the node number k. For most applications, $k \leq 1 0$ is sufficient, so the communication cost for each portrait is 0.82 KB. In COIN++, after encoding, each vector is hashed to 128 bits, which reduces the size of a portrait to 0.15 KB. Protocol COIN++ requires extra communication for random number agreement, which is only about 0.19 KB. COIN costs each participant less than 1 KB data transmission to enable portrait privacy protection. The cost for a photographer depends on the people number in the captured photo, but in most cases (with less than 10 people in photo), less than 10 KB overhead is incurred, which is much less than a photo. The transmission delay for each participant is less than 1ms and for each photographer is less than 3 ms with 4G networking. In general, COIN achieves much smaller transmitted data size and better privacy protection than transmitting the image itself.

# 6.3.2 Computation Cost

In COIN, the computation cost is composed of portrait graph generation on the client side, and portrait matching on the cloud. COIN++ costs extra computation for random number agreement and vector transformation by scrambling and LSH. The runtime is only about 3 ms to transform ten 64-dimension feature vectors. The major computation delay is caused by image processing. For a participant, it only needs to be executed once for the profile setup; for a photographer, it needs to be executed for every captured photo. The runtime of portrait detection and segmentation depends on the resolution and complexity of the photo, but the detection and segmentation results are not sensitive to scaling. Hence, in our prototype all images are scaled to about 240,000 pixels. For the photographer, on average it takes about 0.4 s to conduct face and pedestrian detection. Given a portrait image/subimage, the processing time of segmentation and feature extraction increases with the image complexity, i.e. region number after segmentation. On average, there are 28.2 regions of each portrait, and it takes about 2.6 s to process one image. Figs. 11 and 12 give the CDF of image segmentation and graph generation for three different phones.

Compared with the image processing, the runtime of graph generation and matching is nearly negligible. On the client side, only extra 0.014 s runtime is required for random number generation in COIN++. On the cloud side, the time needed to match a pair of portrait graph is only about 0.04 s in COIN and decreases to 0.01 s in COIN++ due to the hashed feature vector. The cloud also needs 0.9 s to generate system parameters for random number generation. The millisecond-level portrait graph transmission delay is negligible too. So the total computation delays for both variants are about 3 s on the client and 1 s on the cloud, which results a 4s system computation delay.

![](images/4f4fa9519760a31399c6a1e205e900ed2a0f4a6dff13ad43b48c264ef86bcb30.jpg)



Fig. 11. CDF of segmentation run time.

Now we’ve learned the magnitude of the time cost for each component, the overall delay also depends on the number of co-located invisible neighbors. With more active peers sending privacy requests, the matching cost will increase, but compared to the image processing cost, the matching cost on the cloud side is still quite small. Besides, the power consumption caused by our protocol (secondlevel computation) is much smaller than that caused by photo capturing itself.

# 6.4 Case Evaluation

We conduct the case based evaluation in the aforementioned experiments. Overall, the false negative rate is about 1.4 percent (98.6 percent recall) and the false positive rate is 0.9 percent (99.1 percent precision). Further, we go through all failure cases, and here we give more detailed analysis about them. Most false positive cases happen when there are no invisible users in the photos, thus wrong persons are removed. Specifically, due to the absent of any true match users, the false positive rate raises to 4.9 percent (95.1 percent precision), and the threshold 0.5 is not high enough to exclude all false matches. There are also some false positive cases caused by similar clothes of the invisible user and the incorrectly removed user. Most false negative cases happen when the invisible users are sheltered by objects or other people, which results in small match scores. And the average time for successful invisible people removal is about 4 seconds.

# 6.5 Compare with Alternative Solution

We propose an outsourced privacy preserving distance computation method using vector scrambling and LSH. For comparison purpose, we also realize private Euclidean distance computation using a partial homomorphic encryption (Pallier encryption) in the SMC manner (e.g., the method used in [15]). Using the same computer and test images, the Pallier-based method takes about 0.5 s for feature vector encryption and 1.8 s for portrait matching between a pair of feature vectors. But with our approach, the transformation cost is negligible and the matching cost is only 0.01 s. Besides, our method requires no interaction during the matching process. The comparison shows the a significant efficiency of our system.

![](images/150343ba5011f8ece98f53f9e6cf264d320601b2a7a96c7904ee1a25bbef7502.jpg)



Fig. 12. CDF of graph generation run time.

# 7 RELATED WORK

Ubiquitous availability of smart devices with onboard cameras has resulted in photos being captured and shared online at an unprecedented scale. It is important to respect people’s portrait privacy and protect them from unwilling photo-taking and publication. Some actions have been taken in industry and business areas, e.g., forbidding silent photo taking or camera usage in inappropriate situations, which are broadbrush and blunt. There are very few existing work addressing this issue in academic area. The most related work to ours is [3], which requires users to wear visible specialized tags (e.g., QR code) to express their requirements and blurs faces in photos accordingly. There are a few limitations of [3]: first, visible tags on cloth are inaesthetic and inconvenient; second, it considers only face as private information, but a portrait not only includes the user’s face but also his/ her body, since clothes and accessories could also reveal identification information; third, it assumes a trusted server and transmits each user’s portrait image in its original form (visible form), which could cause privacy leakage to untrusted servers and eavesdroppers; besides, without verification mechanism, a photographer can simply ignore the request. In this work, we seek a solution to protect people’s portrait privacy in a non-intrusive way while guaranteeing a comfortable usage of smart glasses/cameras. The whole protection process should be conducted in a privacy-preserving manner even with untrusted server. Also verification of the protection should be supported in case the photographer ignores the request. Our work are related to existing research in the following aspects.

Image Privacy Protection. A number of approaches have been designed to protect image privacy. There is a trivial solution to protect image content. Blacking out private contents, e.g. human faces, thwarts any possible violation of owners’ privacy. For example, systems like Blinkering Surveillance [27] use computer vision methods to hide sensitive contents from video frame, and [40] conceals persons in circumstantial video image. Newton et al. [25] introduces an algorithm to protect the face privacy of individuals in video by blurring faces. GigaSight [29] blacks out sensitive information from video frames. But in a photographing scenario, the challenge is how to match people’s privacy requests with people in the photo. Face recognition is an alternative way to solve the matching problem. Many face descriptors are proposed for face recognition, e.g. Eigenfaces [31] and Fisherfaces [2]. Eigenface method is expected to suffer under variation in lighting direction. Fisherfaces [2] is a method based on Fishers Linear Discriminant, which produces well separated classes in a low-dimensional subspace. To use face recognition approaches, it requires the people to face to cameras. Besides, during the information exchange process, face descriptors could be leaked to adversaries. There are some work providing privacy-preserving face recognition, by which a client can privately search for a specific face image in the image database. Erkin et al. [11] leverages homomorphic encryption to recognize a face in a database of M faces. It requires O log M rounds and is computationð Þally expensive. Sadeghi et al. [26] improves the scheme with cryptographic building blocks combing homomorphic encryption with garbled circuits, requiring only O 1 ð Þrounds with smaller communication and computation cost. Zhang et al. [35], [36] enable outsourced content-based image search against untrusted servers. Those methods provide privacy protection to the requested images as well as the outcome of the matching algorithm, but the computation overhead is large.

Graph Matching. Graph matching techniques are related to the people matching in our approach. Graph matching methods have been applied in many tasks such as face recognition [34], fingerprint identification [14] and others [13]. The recent work [13] proposes a matching scheme which leverages partially known correspondences as anchors. Their application-oriented specifications, e.g., assumptions about node numbers, graph structure and pre-knowledge of correspondences, make them difficult to be applied in this work.

Secret Exchange. Diffie-Hellman key exchange is a well known protocol proposed to distribute a session key between two parties through an untrusted channel. Over the years, several papers have attempted to extend the wellknown Diffie-Hellman key exchange to the multi-party setting [5]. Dynamic group Diffie-Hellman protocols for authenticated key exchange are designed to work in a scenario where a group of parties want to join and leave the multicast group at any given time [4].

Privacy-Preserving Vector Distance Computation. A key step for privacy-preserving photo capturing is matching users in the photo with users who request privacy protection. The matching process can be considered as a sort of distance computation between vectors. For the random perturbation-based algorithms, the original data distributions can be reconstructed with some fair degree of accuracy, but mutual Euclidean distances between individual data points are not preserved. To achieve privacy preserving match, many existing protocols use multi-party computation (SMC) [15], [26] or garble circuit [26] to compute Euclidean distance between vectors. They, however usually require frequent online interactions among data owners. Moreover, their large computation cost and ciphertext size make them unsuitable for mobile applications. Zhang et al. [38] designs a light weight symmetric encryption based vector matching protocol, but it cannot be adopted for distance computation. Mukherjee et al. [24] proposes an approach using Fourierrelated transforms to hide accurate data values and to approximately preserve Euclidean distances among them. It works well for some data mining purpose on large datasets, but the transformation is public and deterministic and it cannot prevent malicious user from dictionary attack. Instead, we propose a novel highly efficient encryption-free privacy-preserving vector distance protocol in a non-interactive manner with untrusted server.

# 8 DISCUSSION AND CONCLUSION

In this work, we present a new approach COIN to protect users’ portrait privacy during photo taking and sharing. With our system, users that are unwilling to be photographed will be automatically erased from the pictures in a lightweight and privacy-preserving way. To achieve this goal, we propose the integrated system framework, a portrait graph matching scheme to match people in photos and an encryption-free privacy-preserving vector distance computation method. We have fully implemented our protocol, and thoroughly evaluated the protection performance and the overhead of the system. Our work is a first step towards privacy-preserving photo capturing and sharing. There are still plenty of room for improvement, and also many open problems to solve. First, the accuracy and efficiency of our method is highly dependent on the performance of people detection and image segmentation methods. With the remarkable development of deep learning techniques in the computer vision area, more accurate and faster solutions can be adopted to facilitate our system. Second, our system may be vulnerable to malicious attacks like denial-of-service (DOS) attack. If many malicious “invisible” users upload fake portrait graphs to the cloud, it could cause higher false positive rate and large overhead to valid users. Besides, in our future work, we will further explore how to efficiently protect users’ portrait privacy in a captured video clips and how to effectively encourage people to use privacy-friendly camera apps.

# ACKNOWLEDGMENTS

This work is supported by the National Key R&D Program of China 2017YFB1003000, NSF China under Grants No. 61822209, 61502271, 61625205, 61572281, 61472218, 61520106007, 61751211, NSF CNS 1526638, the Fundamental Research Funds for the Central Universities WK2150110009, and the Key Research Program of Frontier Sciences, CAS, No.QYZDY-SSW-JSC002.

# REFERENCES

[1] P. Arbelaez, M. Maire, C. Fowlkes, and J. Malik, “Contour detection and hierarchical image segmentation,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 33, no. 5, pp. 898–916, May 2011.   
[2] P. N. Belhumeur, J. P. Hespanha, and D. J. Kriegman, “Eigenfaces vs. fisherfaces: Recognition using class specific linear projection,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 19, no. 7, pp. 711–720, Jul. 1997.   
[3] C. Bo, G. Shen, J. Liu, X.-Y. Li, Y. Zhang, and F. Zhao, “Privacy. tag: Privacy concern expressed and respected,” in Proc. 12th ACM Conf. Embedded Netw. Sensor Syst., 2014, pp. 163–176.   
[4] E. Bresson, O. Chevassut, and D. Pointcheval, “Provably authenticated group diffie-hellman key exchangethe dynamic case,” in Proc. 7th Int. Conf. Theory Appl. Cryptology Inf. Secur.: Adv. Cryptology, 2001, pp. 290–309.   
[5] E. Bresson, O. Chevassut, and D. Pointcheval, “Group diffiehellman key exchange secure against dictionary attacks,” in Proc. Int. Conf. Theory Appl. Cryptology Inf. Secur., 2002, pp. 497–514.

[6] M. Burmester and Y. Desmedt, “A secure and efficient conference key distribution system,” in Proc. Workshop Theory Appl. Cryptographic Tech., 1994, pp. 275–286.   
[7] A. Criminisi, P. P-erez, and K. Toyama, “Region filling and object removal by exemplar-based image inpainting,” IEEE Trans. Image Process., vol. 13, no. 9, pp. 1200–1212, Sep. 2004.   
[8] M. Daneshi and J. Guo, “Image reconstruction based on local feature descriptors,” Dept. Elect. Eng., Stanford Univ., Stanford, CA, USA, Tech. Rep., 2011.   
[9] M. Datar, N. Immorlica, P. Indyk, and V. S. Mirrokni, “Localitysensitive hashing scheme based on p-stable distributions,” in Proc. 20th Annu. Symp. Comput. Geometry, 2004, pp. 253–262.   
[10] Y. Deng and B. Manjunath, “Unsupervised segmentation of colortexture regions in images and video,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 23, no. 8, pp. 800–810, Aug. 2001.   
[11] Z. Erkin, M. Franz, J. Guajardo, S. Katzenbeisser, I. Lagendijk, and T. Toft, “Privacy-preserving face recognition,” in Proc. Int. Symp. Privacy Enhancing Technol. Symp., 2009, pp. 235–253.   
[12] R. Hoyle, R. Templeman, S. Armes, D. Anthony, D. Crandall, and A. Kapadia, “Privacy behaviors of lifeloggers using wearable cameras,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., 2014, pp. 571–582.   
[13] N. Hu, R. M. Rustamov, and L. Guibas, “Graph matching with anchor nodes: A learning approach,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2013, pp. 2906–2913.   
[14] D. Isenor and S. G. Zaky, “Fingerprint identification using graph matching,” Pattern Recognit., vol. 19, no. 2, pp. 113–122, 1986.   
[15] J. Katz, A. Sahai, and B. Waters, “Predicate encryption supporting disjunctions, polynomial equations, and inner products,” in Proc. Theory Appl. Cryptographic Tech. 27th Annu. Int. Conf. Adv. Cryptology, 2008, pp. 146–162.   
[16] N. Komodakis, “Image completion using global optimization,” in Proc. IEEE Comput. Soc. Conf. Comput. Vis. Pattern Recognit., 2006, pp. 442–452.   
[17] L. Shangguan, Z. Yang, A. X. Liu, Z. Zhou, and Y. Liu, “STPP: Spatial-temporal phase profiling-based method for relative RFID tag localization,” IEEE/ACM Trans. Netw., vol. 25, no. 1, pp. 596– 609, Feb. 2017.   
[18] H. W. Kuhn, “The hungarian method for the assignment problem,” Naval Res. Logistics Quart., vol. 2, no. 1/2, pp. 83–97, 1955.   
[19] P. P. Lee, J. C. Lui, and D. K. Yau, “Distributed collaborative key agreement and authentication protocols for dynamic peer groups,” IEEE/ACM Trans. Netw., vol. 14, no. 2, pp. 263–276, Apr. 2006.   
[20] B. Leibe, E. Seemann, and B. Schiele, “Pedestrian detection in crowded scenes,” in Proc. IEEE Comput. Soc. Conf. Comput. Vis. Pattern Recognit., 2005, pp. 878–885.   
[21] X.-Y. Li and T. Jung, “Search me if you can: Privacy-preserving location query service,” in Proc. IEEE INFOCOM, 2013, pp. 2760– 2768.   
[22] H. Liu, Y. Gan, J. Yang, S. Sidhom, Y. Wang, Y. Chen, and F. Ye, “Push the limit of wifi based localization for smartphones,” in Proc. 18th Annu. Int. Conf. Mobile Comput. Netw., 2012, pp. 305–316.   
[23] J. Luo, Y. Ma, E. Takikawa, S. Lao, M. Kawade, and B.-L. Lu, “Person-specific sift features for face recognition,” IEEE Int. Conf. Acoust. Speech Signal Process., 2007, pp. II-593–II-596.   
[24] S. Mukherjee, Z. Chen, and A. Gangopadhyay, “A privacypreserving technique for Euclidean distance-based mining algorithms using fourier-related transforms,” VLDB J., vol. 15, no. 4, pp. 293–315, 2006.   
[25] E. M. Newton, L. Sweeney, and B. Malin, “Preserving privacy by de-identifying face images,” IEEE Trans. Knowl. Data Eng., vol. 17, no. 2, pp. 232–243, Feb. 2005.   
[26] A.-R. Sadeghi, T. Schneider, and I. Wehrenberg, “Efficient privacy-preserving face recognition,” in Proc. 12th Int. Conf. Inf. Secur. Cryptology, 2010, pp. 229–244.   
[27] A. Senior, S. Pankanti, A. Hampapur, L. Brown, Y.-L. Tian, A. Ekin, J. Connell, C. F. Shu, and M. Lu, “Enabling video privacy through computer vision,” IEEE Secur. Privacy 3, no. 3, pp. 50–57, 2005.   
[28] G. Shafer, A Mathematical Theory of Evidence, vol. 1. Princeton, NJ, USA: Princeton Univ. Press, 1976.   
[29] P. Simoens, Y. Xiao, P. Pillai, Z. Chen, K. Ha, and M. Satyanarayanan, “Scalable crowd-sourcing of video from mobile devices,” Proc. 11th Annu. Int. Conf. Mobile Syst. Appl. Serv., 2013, pp. 139–152.   
[30] Y. Taigman, M. Yang, M. Ranzato, and L. Wolf, “Deepface: Closing the gap to human-level performance in face verification,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2014, pp. 1701– 1708.

[31] M. Turk and A. Pentland, “Eigenfaces for recognition,” J. Cognitive Neuroscience, vol. 3, no. 1, pp. 71–86, 1991.   
[32] P. Viola and M. J. Jones, “Robust real-time face detection,” Int. J. Comput. Vis., vol. 57, no. 2, pp. 137–154, 2004.   
[33] C. Wu, Z. Yang, and C. Xiao, “Automatic radio map adaptation for indoor localization using smartphones,” IEEE Trans. Mobile Comput., vol. 17, no. 3, pp. 517–528, Mar. 2018.   
[34] L. Wiskott, J.-M. Fellous, N. Kuiger, and C. Von Der Malsburg, “Face recognition by elastic bunch graph matching,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 19, no. 7, pp. 775–779, Jul. 1997.   
[35] L. Zhang, T. Jung, P. Feng, K. Liu, X.-Y. Li, and Y. Liu, “Pic: Enable large-scale privacy preserving content-based image search on cloud,” IEEE Trans. Parallel Distrib. Syst., vol. 28, no. 11, pp. 3258– 3271, Nov. 2017.   
[36] L. Zhang, T. Jung, C. Liu, X. Ding, X.-Y. Li, and Y. Liu, “Pop: Privacy-preserving outsourced photo sharing and searching for mobile devices,” in Proc. IEEE 35th Int. Conf. Distrib. Comput. Syst., 2015, pp. 308–317.   
[37] L. Zhang, X.-Y. Li, W. Huang, K. Liu, S. Zong, X. Jian, P. Feng, T. Jung, and Y. Liu, “It starts with igaze: Visual attention driven networking with smart glasses,” in Proc. ACM MobiCom, 2014, pp. 91–102.   
[38] L. Zhang, X.-Y. Li, K. Liu, T. Jung, and Y. Liu, “Message in a sealed bottle: Privacy preserving friending in mobile social networks,” IEEE Trans. Mobile Comput., vol. 14, no. 9, pp. 1888– 1902, Sep. 2015.   
[39] L. Zhang, K. Liu, X.-Y. Li, C. Liu, X. Ding, and Y. Liu, “Privacyfriendly photo capturing and sharing system,” Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., 2016, pp. 524–534.   
[40] W. Zhang, S.-C. S. Cheung, and M. Chen, “Hiding privacy information in video surveillance system,” in Proc. IEEE Int. Conf. Image Process., 2005, pp. II–868.

![](images/fa2768f656b4e22077327e30eed8268c6c4d57a5daa87e703f6d5a5d7f24e207.jpg)



Lan Zhang received the bachelor’s degree from the School of Software, Tsinghua University, China, in 2007 and the PhD degree from the Department of Computer Science and Technology, Tsinghua University, China, in 2014. She is currently a research professor with the School of Computer Science and Technology, University of Science and Technology of China. Her research interests include data trading, privacy protection, and mobile computing, etc. She is a member of the IEEE.

![](images/465328ae04ccf460876c64bf59cc3dbc59743b0ca74a5432dd1e4b831fd6dbb1.jpg)



Xiang-Yang Li received the bachelor’s degree from the Department of Computer Science and the bachelor’s degree from the Department of Business Management, Tsinghua University, China, both in 1995 and the MS and PhD degrees from the Department of Computer Science, University of Illinois at Urbana-Champaign, in 2000 and 2001, respectively. He is a full professor with the School of Computer Science and Technology, University of Science and Technology of China, Hefei, China. He was a full professor with the Illi-

nois Institute of Technology, Chicago. His research interests include wireless networking, mobile computing, security and privacy, and cyber physical systems. He is a fellow of the IEEE and an ACM Distinguished Scientist.

![](images/4cf7999b9e9141a78d4aaae1c3603802f771947c37041947997d6b8d8bad5edd.jpg)



Kebin Liu received the BS degree from the Department of Computer Science, Tongji University, in 2004, and the MS and PhD degrees from Shanghai Jiaotong University, in 2007 and 2010, respectively. He is currently an assistant researcher with the School of Software and TNLIST, Tsinghua University. His research interests include WSNs and distributed systems. He is a member of the IEEE.

![](images/2cca96cfb29ea0e8c57bd266041f986a1d8bfa1c9451ce2b9f1f7738d3d35872.jpg)



Cihang Liu received the bachelor’s degree from the School of Software, Tsinghua University, in 2014. He is working toward the PhD degree in the School of Software, Tsinghua University, China. His research interests include mobile computing and wireless communication. He is a member of the IEEE.

![](images/08af346603cbcab40846c6f820503157ee44f64ad71fbbfabeac0090c22e9b4b.jpg)



Yunhao Liu received the BS degree from the Automation Department, Tsinghua University, in 1995, and the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is a MSU foundation professor and chairperson of the Department of Computer Science and Engineering, Michigan State University. He also received the Tsinghua Chang Jiang Professorship. He is a fellow of the ACM and the IEEE, and an editor in chief of the ACM Transactions on Sensor Network.

![](images/c5e8a94d3d546331d0c19105878e9c9ffbdab637c84e3bde16a754e13b94f781.jpg)



Xuan Ding received the bachelor’s degree from the School of Software, Tsinghua University, China, in 2008 and the PhD degree from the department of Computer Science and Technology, Tsinghua University, China, in 2014. He is now a post doctor with the School of Software, Tsinghua University, China. His research interests include social networking privacy, privacy-aware computing, and data analysis, etc. He is a member of the IEEE.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.