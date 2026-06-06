# EyeLoc: Smartphone Vision Enabled Plug-n-play Indoor Localization in Large Shopping Malls

Manni Liu, Jialuo Du, Qing Zhou, Zhichao Cao, Member, IEEE and Yunhao Liu, Fellow, IEEE

# Abstract—

Indoor localization is becoming an emerging requirement in many large shopping malls. Existing indoor localization systems, however, require exhausted system bootstraps and calibration phases. The huge sunk cost usually hinders practical deployment of the indoor localization systems in large shopping malls. In contrast, we observe that floor-plan images of large shopping malls, which highlight the positions of many shops, are widely available in Google Maps, Gaode Maps, Baidu Maps, etc. According to several observed shops, people can localize themselves (called self-localization). However, due to the requirements of geometric sense and space transformation, not all people get used to this way. In this paper, we propose EyeLoc, which uses smartphone vision to enable accurate self-localization on a floor-plan image. EyeLoc addresses several challenges, including developing a ubiquitous smartphone vision system, extracting efficient vision clues and achieving robust measurement error mitigation. We implement EyeLoc in Android and evaluate its performance in emulated environment, two large shopping malls and a semi-outdoor large Outlets. The results show that the 90- percentile errors of localization and heading direction are 5.97 m and 20◦ in 70,000 m2 malls.

# I. INTRODUCTION

N OWADAYS, the physical layout of many large shoppingmalls is becoming more and more complex [1]. As malls is becoming more and more complex [1]. As there are many location-based activities (e.g., shopping, eating, watching movies) in large shopping malls, indoor localization is becoming an important service for people. Although outdoor localization (i.e., GPS) has been put into practice for many years, there is still no practical deployed indoor localization systems.

Many indoor localization systems rely on pre-collected information (e.g., Wi-Fi signals [2] [3] [4] [5] [6] [7], lamp positions [8] [9] [10], scene images [11] [12] [13] and magnetic fingerprints [14] [15]), called site survey, to construct a localizable map. In large shopping malls, the site survey usually incurs extensive bootstrap overhead which hinders corresponding approaches from widespread adoption. Even when the site survey is accomplished, the information needs to be timely updated and calibrated to ensure the accuracy. Moreover, some indoor localization systems [5] require custom hardware, which is not supported in commodity smartphones.

Our core question is can we set up a plug-and-play indoor localization system in large shopping malls with commodity smartphones? We notice a possible way by leveraging the widely available floor-plan images, which can be obtained from indoor map providers (e.g., Google Maps, Gaode Maps, Baidu Maps, etc.). Those floor-plan images contain positions of many shops, called Point of Interests (POI). POIs are used as visual hints when users try to manually localize themselves. This kind of nonautomatic self-localization usually requires users to have good geometric sense and the ability of space transformation. To reduce users’ mental work and provide realtime localization service, we refine the question as can users automatically obtain their positions on floor-plan images from their smartphones just like traditional outdoor localization systems such as Google Maps and Baidu Maps? In this sense, it is possible to achieve a plug-and-play indoor localization system by bridging this gap.

In this paper, we propose EyeLoc, a step towards plugand-play indoor localization in large shopping malls. The key idea of EyeLoc is to imitate human self-localization with smartphone vision. After obtaining a floor-plan image, EyeLoc uses scene text detection/recognition techniques to extract a set of POIs from the image. The recognized texts are used to identify different POIs and their corresponding text bounding boxes provide the approximate POI positions in the floor-plan coordinate system (called floor-plan space). Correspondingly in real space (called vision space), a user holds his/her smartphone and turns a 360◦ circle. The smartphone automatically shoots a series of images (called view image), which contain the surrounding POI signs. For those observed POIs, EyeLoc extracts their texts and geometric constraints in vision space, which are further used to match the user’s position in floorplan space.

Technically, EyeLoc develops several novel methods to address three challenges. First, there is a big difference between human vision system and smartphone vision system. Human vision system is a binocular system that supports estimating the direction and distance of an object. Most of the smartphones, however, only have one camera which is hard to achieve direction and distance measurements in a light-weight way with existing vision methods. We develop an accurate and ubiquitous monocular vision system which is available on most smartphones. We construct the constant geometric constraints of 3 observed POIs to enable position matching between floor-plan space and visual space. Second, to extract the directions of different POIs, text detection and recognition are necessary, but usually time-consuming. To reduce the processing time of POI extraction, an outlier image filtering method and a sparse image processing method are designed. Third, the measurement errors from motion sensors and floorplan images may incur inaccurate position matching, for which we design an error-resilient method.

We implement EyeLoc on Android smartphones and evaluate its performance in an office environment, two large shopping malls (7,500m2 and $1 0 , 0 0 0 \mathrm { m } ^ { 2 } )$ and a semi-outdoor large Outlets (70,000m2). The evaluation results show that the

90-percentile errors of localization and heading direction can achieve 5.97 m and 20◦. The contributions of this paper are as follows.

• We propose EyeLoc, a smartphone vision enabled plugand-play indoor localization in large shopping malls. No site survey nor periodical calibration of floor map is required.   
• We develop a ubiquitous smartphone vision system and corresponding geometric localization model. To guarantee the localization accuracy and processing efficiency, we propose countermeasures to address several practical challenges.   
• We implement EyeLoc on Android smartphones and evaluate its performance in an office environment and two large shopping malls. The evaluation results show that EyeLoc is effective in both localization accuracy and processing efficiency.

The rest of this paper is organized as follows. Section II introduces the overview of EyeLoc. Section III illustrates the detailed design of EyeLoc. Section IV and Section V show the details of EyeLoc implementation and evaluation, respectively. Section VI summarizes the related work. Finally, we conclude our work in Section VII.

# II. EYELOC OVERVIEW

Plug-and-play outdoor localization has been successfully achieved on smartphones with the help of GPS. Referring to the criteria of GPS-based outdoor localization, EyeLoc has two goals:

• Plug-and-play. EyeLoc should not assume any extra bootstrap cost (e.g., site survey, system calibration) in large shopping malls. Moreover, EyeLoc should not require users to own any prior knowledge or follow complex smartphone operations.   
• Efficient and robust. Facing computation-intensive image processing and various measurement errors from motion sensors and floor-plan images, EyeLoc should be able to accurately localize a user with short processing time.

To meet the first goal, EyeLoc is inspired by two observations. First, the indoor floor-plan images of shopping malls (e.g., shown in Fig. 1(a)) can be easily fetched from indoor map providers through Android and iOS APIs. The other observation is that people are used to turning around to observe surrounding POIs and localize themselves. After fetching the floor-plan images, EyeLoc enables the self-localization of the smartphone through absorbing data from the on-board motion sensors and camera. No bootstrap cost or user training is involved.

Fig. 1 is an example showing how EyeLoc works in a plugand-play manner. Alice is lost in a large shopping mall and she wants to go to H&M. As Alice opens EyeLoc on her smartphone, the corresponding floor-plan image is automatically fetched. She holds the smartphone and turns a 360◦ circle, during which the camera and motion sensors keep working. This operation is called circle shoot. With input data from the camera and motion sensors, EyeLoc extracts geometric information of surrounding POIs (e.g., GAP, UGG, MISS SIXTY, Calvin Klein). Meanwhile, EyeLoc uses text detection and recognition techniques to find the POI positions on the floor-plan image. Finally, EyeLoc projects Alice’s position and heading direction onto the floor-plan image.

![](images/9254e4f15a66dbd2b6148fa68af9042720873cf5e7d6ddac82cf00bb1fba93ae.jpg)



(a) Indoor Floor-plan Image

![](images/eba2319032e484edb1091a0ac42290f477b7eefe365a29d6cd4afea456a5ecd6.jpg)



(b) Circle Shoot   
Fig. 1. Illustration of an example of the EyeLoc innovation.

The involvement of image processing significantly increases the difficulty to meet the second goal. As Fig. 1 illustrates, EyeLoc depends on text detection and recognition techniques to extract POI signs from view images. Text detection and recognition for color images have been widely studied in the past decade, especially with deep learning models like convolutional neural networks. A few open-source models (e.g., OpenCV [16], Tesseract [17]) are also available on smartphones. Smartphones can also utilize cloud service from companies like Google, Baidu, etc. However, none of the two approaches can achieve real-time execution due to computation overhead on images or extra network delay. This contradiction demands us to design an efficient method to extract enough geometric information without incurring long processing latency. We have two intuitions for the method design. First, since the extracted POIs with error geometric information is useless even harmful for localization, we should not deal with those view images of low quality. Second, we observe that the view images are usually redundant for extracting the geometric information of an observed POI. Hopefully, we can only select a subset of those view images which contain equivalent geometric information of the observed shops as the whole set does for further processing.

On the other hand, various measurement errors are invertible and may lead to inaccurate localization. For example, as shown in Fig. 1(c), the text bounding boxes of the four observed shops may be not exactly aligned to that of the corresponding shop signs that appeared in vision space. To mitigate potential errors and achieve robust localization, our observation is that the spatial POI distribution is usually dense in large shopping malls, which means multiple POIs are available. Hopefully, we can use the redundant information to refine the estimated user position.

In comparison with human binocular vision system, EyeLoc develops a monocular vision system, which is accurate and ubiquitous for smartphones. EyeLoc enables user position matching between vision space and floor-plan space with constant geometric constraints of observed POIs. The system architecture of EyeLoc is shown in Fig. 2, including three parts as follows.

Raw Data Collection. The first part is to fetch floor-plan images from indoor map providers and collect raw information of view images from circle shoot. According to the coarse

![](images/f2dc5267625e44b9ea6ac292919ab8b80cef44d5eb75fc60fbeab92d9efa2d8a.jpg)



Fig. 2. Illustration of the system architecture of EyeLoc.

GPS localization, EyeLoc queries indoor map providers to obtain floor-plane images. During the circle shoot, Eyeloc uses the camera and motion sensors (e.g., compass, gyroscope, accelerometer) to continuously capture view images and corresponding motion attributes (e.g., camera facing direction, angle velocity). Section III-C shows the design details.

POI Extraction. Taking the information of view images and floor-plan images as input, the second part extracts geometric information of observed POIs in both vision space and floorplan space. Because text detection and recognition are timeconsuming, we need to extract enough geometric information while keeping the number of processed images as small as possible. EyeLoc filters out some view images which are blurred or have error motion attributes. Then EyeLoc develops a sparse image processing method to extract geometric information of all observed POIs from the rest of the images and keeps the number of processed images small. On the other hand, after extracting all POIs on the floor-plan image, EyeLoc obtains the positions of the observed POIs in floor-plan space by matching their names. The detailed design is illustrated in Section III-D.

Position Matching. With the geometric information of the observed POIs, EyeLoc now projects the user’s position and heading direction onto floor-plan space. The redundancy of the observed POIs is explored to mitigate unavoidable errors of geometric information in vision space and positions in floor-plan space. The observed POIs are grouped into tuples. Each POI tuple can be used to calculate the user’s position and heading direction with geometric constraints. The localization errors of different tuples are diverse with the same measurement errors. EyeLoc combines several inferred positions and the corresponding errors to vote the final user’s position and heading direction. The detailed design is shown in Section III-E.

# III. EYELOC DESIGN

To relieve humans of self-localization, EyeLoc achieves plug-and-play localization in large shopping malls. Due to the fundamental difference between the vision principle of humans and smartphones, we first establish the smartphone vision system and illustrate the geometric localization model. To further put EyeLoc into practice, we show the detailed design of three function components (shown in Fig. 2) step by step.

# A. Smartphone Vision System

We intend to define a ubiquitous smartphone vision system to fetch the geometric relationship between a smartphone and an observed POI. Human eyes form a binocular vision system, which enables us to estimate our distance and direction to an observed POI. Smartphone vision differs significantly from human vision. First, not all smartphones have been equipped with dual or triple cameras. It is hard to extract the distance and direction of an observed object from a monocular image except there is a preconfigured Structure from Motion (SfM) based model or learning based model. However, both of these two approaches require a large set of images for model training, which incurs the heavy burden of site survey. Second, humans have practiced a lot since childhood, so camera calibration [18] is a must to achieve accurate estimation. Since the parameters of camera calibration are not explicitly known for those smartphones, the complicated operation induces unacceptable difficulty to bootstrap this ability for common users. In EyeLoc, the question is can we estimate distance and direction as the geometric descriptor of an observed object through the monocular view images of circle shoot?

![](images/1065b0210808e7e306cc08a3ac645d5750b15e323f0daedb3584d47ae88e8181.jpg)



Fig. 3. Direction and distance measurement with circle shoot.

![](images/7e9526e3f246ff606084a61021af44a3fff2e33e8d34a9b7b334fd37b6cffb35.jpg)



(a) Influence of $\theta _ { 1 }$ and $\theta _ { 2 }$

![](images/b065ace3a88859c6a85d4c1493a91cc8ed3cf42e127cd36ebaf5232d6bc448b4.jpg)



(b) Influence of k   
Fig. 4. Illustration of distance error in terms of the error of $\theta _ { 2 }$ and k. (a) and (b) show the distance error under different $\theta _ { 2 }$ and k when other parameters are fixed.

It is confirmative that the direction information of a POI can be constructed with the monocular view images of circle shoot. We define the EyeLoc sightline of an object as the virtual line between the object and the user. For example, as shown in Fig. 3, given a POI P and a user H, the EyeLoc sightline is HP . O is the optical center of the camera lens and C is the center of the image plane. H, C and O are approximately kept on the same line all the time during circle shoot. When the user is facing P , HP coincides with $C O$ and its direction can be measured by smartphone motion sensors [19]. During circle shoot, however, the user’s facing direction is continuously changing. For example, $C _ { 1 } O _ { 1 }$ and $C _ { 2 } O _ { 2 }$ are not aligned with $H P .$ . The key observation is that when CO and $H P$ are aligned, $F$ that indicates the position of $P$ on a view image will coincide with $C .$ Otherwise, it will appear at the side of C as $F _ { 1 }$ and $F _ { 2 }$ show. As shown in Fig. 5(b), (c) and (d), when a user turns in clockwise during circle shoot (e.g., Fig. 5(a)), for shop “MOUSSY”, its text bounding box will appear from left to right in the view images. EyeLoc finds the view image (e.g., Fig. 5(c)) of which the text bounding box is at the center, then the direction of EyeLoc sightline can be estimated by motion sensor.

![](images/41c4b3c4ef431191222949db90ce198bb5d3983b944116459e3f7b982a896dfe.jpg)



Fig. 5. An example of the sightline change during circle shoot in physical space.

To enable distance estimation with monocular vision, it is possible to exploit the camera motion of circle shoot to imitate a binocular vision system. As shown in Fig. 3, the distance between the POI P and the user H is indicated as d. The distance between H and the optical center of smartphone camera lens $O _ { 1 }$ is $r .$ The focal length of the smartphone camera lens f is unknown for most smartphones. $\theta _ { 1 }$ indicates the intersection angle between line $H O _ { 1 }$ and EyeLoc sightline $H P .$ . Since $\triangle F _ { 1 } O _ { 1 } C _ { 1 }$ is similar to $\triangle P O _ { 1 } K _ { 1 }$ , we have the following equation:

$$
\frac {F _ {1} C _ {1}}{d \sin \theta_ {1}} = \frac {f}{d \cos \theta_ {1} - r} \tag {1}
$$

where $F _ { 1 } C _ { 1 }$ indicates the pixel offset between $F _ { 1 }$ and C1. Combining the same equation under another angle $\theta _ { 2 } ~ ( \theta _ { 1 } \neq$ $\theta _ { 2 } )$ , we can derive d as follow:

$$
d = r \frac {\sin \theta_ {1} - k \sin \theta_ {2}}{\cos \theta_ {2} \sin \theta_ {1} - k \cos \theta_ {1} \sin \theta_ {2}} \tag {2}
$$

where k equals the ratio between $F _ { 1 } C _ { 1 }$ and $F _ { 2 } C _ { 2 } . \mathrm { I f } \ \theta _ { 1 } , \theta _ { 2 } ,$ k and r are known, the distance d can be calculated. As the direction of $H P , H O _ { 1 }$ and $H O _ { 2 }$ can be obtained by motion sensors, $\theta _ { 1 }$ and $\theta _ { 2 }$ can be calculated. For a shop, we recognize the center of its text bounding box as $F _ { 1 }$ and $F _ { 2 }$ on a view image so that $F _ { 1 } C _ { 1 } , F _ { 2 } C _ { 2 }$ and k can be calculated. r can be roughly estimated according to human arm length. In this way, EyeLoc can estimate the distance of a POI without any prior knowledge of camera parameters in large shopping malls.

# Algorithm 1 Geometric Constraints Extraction Algorithm

Input: 3 POIs sorted as their appearance order; the directions of the corresponding EyeLoc sightline $\delta _ { 1 } , \delta _ { 2 } , \delta _ { 3 }$ in vision space.

Output: d12, $d _ { 2 3 } , d _ { 3 1 } , \theta _ { 1 2 } , \theta _ { 2 3 }$ and $\theta _ { 3 1 } .$

1: vector of POI1 EyeLoc sightline $v _ { 1 } = ( \sin \delta _ { 1 } , \cos \delta _ { 1 } ) .$   
2: vector of POI2 EyeLoc sightline $v _ { 2 } = ( \sin \delta _ { 2 } , \cos \delta _ { 2 } ) .$   
3: vector of POI3 EyeLoc sightline v3 = (sin δ3, cos $\delta _ { 3 } ) .$   
4: $d _ { 1 2 } = v _ { 1 } \times v _ { 2 } , d _ { 2 3 } = v _ { 2 } \times v _ { 3 }$ and $d _ { 3 1 } = v _ { 3 } \times v _ { 1 } .$   
5: $\theta _ { 1 2 } = ( \delta _ { 2 } - \delta _ { 1 } )$ mod $3 6 0 ^ { \circ } ; \theta _ { 2 3 } = \left( \delta _ { 3 } - \delta _ { 2 } \right)$ mod $3 6 0 ^ { \circ } ; \theta _ { 3 1 } =$ $\left( \delta _ { 1 } - \delta _ { 3 } \right)$ mod 360◦

Since the error of θ and k estimation is inevitable, we further conduct the error analysis. We assume r is 0.5m. Given $\theta _ { 1 } , \theta _ { 2 }$ and k are $2 4 ^ { \circ } , 1 2 ^ { \circ }$ and 2.11, d will be 5.48m. We change one parameter $( \mathbf { e . g . } , \theta _ { 1 } , \theta _ { 2 } , k )$ to calculate the distance error when other parameters are fixed. The results are shown in Fig. 4. Surprisingly, given the distance as 5.48m, the distance error is huge when $\theta _ { 1 } , \theta _ { 2 }$ and k have a small bias. The distance error is getting to $1 . 9 7 \mathrm { m } ,$ when $\theta _ { 1 }$ decreases from $2 4 ^ { \circ }$ to 23.9◦. Similarly, when $\theta _ { 2 }$ increases from $1 2 ^ { \circ }$ to $1 2 . 1 ^ { \circ }$ , the distance error increases from 0m to $2 . 6 8 \mathrm { m } . 0 . 1 ^ { \circ }$ error is common for the facing direction measurement with motion sensors. The same trend happens on $k .$ When k increases from 2.11 to 2.16, the distance error increases from 0m to 3.77m. Due to the limitation of image resolution, given that $F _ { 1 } C _ { 1 }$ is as large as 1000 pixels, 0.05 error of k means about no more than 50 pixels error of $\bar { F } _ { 2 } C _ { 2 }$ which is hard to achieve due to the relatively large estimation error of text bounding box. When $\theta _ { 1 }$ increases or ${ \dot { \theta } } _ { 2 }$ and k decreases a little, the situation is getting even worse. Hence, due to the limitation of motion sensor precision and image resolution, the potential huge error makes the distance estimation unpractical currently.

Overall, in our smartphone vision system, for a POI, we only use the direction of its EyeLoc sightline as the geometric descriptor to develop an error-controllable localization model (Section III-B). To accurately and efficiently trace the sightline of a smartphone, we further develop several countermeasures in Section III-D and Section III-E. We leave the accurate distance measurement using a monocular vision system as our future work.

# B. Geometric Localization Model

After we obtain the direction of the EyeLoc sightline of several POIs, the next question is how to construct constant geometric constraints, then figure out the user’s position and heading direction on the floor-plan image.

Let us show the constant geometric constraints through an example. As shown in Fig. 6(a), H is a user’s position. The user observes 3 POIs (e.g., POI1 Miss Sixty, POI2 UGG and $\mathrm { P O I _ { 3 } \ G A P ) }$ in their appearance oder and $N _ { v }$ indicates the north direction in vision space. As shown in Fig. 6(b), H also indicates the user’s position. 1, 2 and 3 represent the corresponding center of text bounding boxes of 3 observed POIs. Given the coordinate system X-Y of the floorplan image, $( x _ { 1 } , y _ { 1 } )$ , $( x _ { 2 } , y _ { 2 } )$ and $( x _ { 3 } , y _ { 3 } )$ are the corresponding coordinate of 1, 2 and $3 . \ : N _ { f }$ is the north direction in floor-plan space which aligns with $Y$ axis. In vision space, the directions of EyeLoc sightline $\bar { \delta } _ { 1 } , \delta _ { 2 }$ and $\delta _ { 3 }$ can be estimated. However, since $N _ { v }$ and $N _ { f }$ may not be aligned with each other, we cannot directly determine the coordinate of H with these directions in floor-plan space.

We have two constant geometric constraints in both vision and floor-plan spaces. The first is the rotation direction of circle shoot is constant. The 3 POIs will appear in the same order (e.g., $\mathrm { P O I _ { 1 } \to P O I _ { 2 } \to P O I _ { 3 } }$ and $1  2 \stackrel { - } {  } 3 )$ along the rotation direction. We use $d _ { 1 2 } , d _ { 2 3 }$ and $d _ { 3 1 }$ to indicate the rotation direction between each pair of adjacent POIs. The other is that, according to the similar triangles, $\angle \mathrm { P O I _ { 1 } } H \mathrm { P O I _ { 2 } } , \angle \mathrm { P O I _ { 2 } } H \mathrm { P O I _ { 3 } }$ and $\angle \mathrm { P O I _ { 3 } } \bar { H } \mathrm { P O I _ { 1 } }$ equal to $\angle 1 \bar { H 2 } , \angle 1 H 2$ and 6 1H2. The 3 intersection angles are indicated as $\theta _ { 1 2 } , \theta _ { 2 3 }$ and $\theta _ { 3 1 }$ . The rotation direction and the intersection angles between any two POIs sever the constant geometric constraints for both vision space and floor-plan space. Alg. 1 exhibits the details to

![](images/a627b160e1d6de1b5a757318d57b8777866200cabc0e5f03f781290b708732ca.jpg)



D'LUHFWLRQLQYLVLRQVSDFH

![](images/2a10abc78dc23e8cb6b4aad14c5c9e3ec099baa7de541c25883c36b282bd9c5a.jpg)



E'LUHFWLRQLQƊRRUSODQVSDFH

![](images/b90834d66c93589e827a18d4cd56ec1aa0b56ab9c35c4998e1456baa2366fcbb.jpg)



F3RVVLEOHORFDWLRQRQDQDUF   
Fig. 6. Illustration of the model used to localize a user’s position on floor-plan image with 3 observed POIs. (a) and (b) exhibit a constant geometric constraint in both vision space and floor-plan space. (c) shows the model to calculate the user’s location with the extracted geometric information.

# Algorithm 2 Arc Calculation Algorithm

Input: 2 POIs, $\overline { { \mathrm { P O I } _ { 1 } } }$ and $\overline { { \mathrm { P O I } _ { 2 } } } ,$ sorted as their appearance order; the rotation direction $d _ { 1 2 } ;$ the angle $\theta _ { 1 2 }$ between the directions of the corresponding EyeLoc sightline in vision space; the corresponding coordinates $( x _ { 1 } , y _ { 1 } )$ and $( x _ { 2 } , y _ { 2 } )$ in floor-plan space.

Output: The coordinate of circle center $( x _ { o } , y _ { o } ) ;$ ; the length of circle radius $R .$

1: pixel distance and slope of the chord $\bar { 1 2 }$ as $\begin{array} { r l } { d _ { 1 2 } } & { { } = } \end{array}$ $\hat { \sqrt { ( x _ { 1 } - x _ { 2 } ) ^ { 2 } + ( y _ { 1 } - y _ { 2 } ) ^ { 2 } } }$ and $\begin{array} { r } { k = \frac { x _ { 1 } - x _ { 2 } } { y _ { 1 } - y _ { 2 } } . } \end{array}$ .   
2: if $\theta _ { 1 2 }$ equals to 180◦ then   
3: H is on the segment between $\mathrm { P O I _ { 1 } }$ and POI2. $( x _ { o } , y _ { o } )$ and R are set as NULL.   
4: else if $\theta _ { 1 2 } > 1 8 0 ^ { \circ }$ then   
$\theta _ { 1 2 } = 3 6 0 ^ { \circ } - \theta _ { 1 2 } .$   
6: else if $\theta _ { 1 2 }$ equals to $9 0 ^ { \circ } .$ then   
7: (xo, yo) = ( x1+x2 , $( x _ { o } , y _ { o } ) \stackrel { \scriptscriptstyle } { = } ( { \textstyle \frac { x _ { 1 } + x _ { 2 } } { 2 } } , { \textstyle \frac { y _ { 1 } + y _ { 2 } } { 2 } } ) ; R = d _ { 1 2 } / 2$ 2 y1+y2 );R = d12/2   
8: else   
9: $\begin{array} { r c l } { R } & { = } & { \frac { d _ { 1 2 } } { 2 \sin \theta _ { 1 2 } } ; } \end{array}$ 2 sin θ12 two possible coordinates $( x _ { o 1 } , y _ { o 1 } )$ and $( x _ { o 2 } , y _ { o 2 } )$ of circle center are calculated by Equ. 5.   
10: set $( x _ { o } , y _ { o } )$ as $( x _ { o 1 } , y _ { o 1 } )$   
11: calculate the rotation direction $d _ { o 1 2 } = \mathrm { v e c t o r } ( x _ { o } - x _ { 1 } , y _ { o } -$ $y _ { 1 } ) \times \mathrm { v e c t o r } ( x _ { o } - x _ { 2 } , y _ { o } - y _ { 2 } )$   
12: $\textbf { f } d _ { 1 2 } \cdot d _ { o 1 2 } > 0 \oplus \theta _ { 1 2 } < 9 0 ^ { \circ }$ . then   
13: set $( x _ { o } , y _ { o } )$ as $( x _ { o 2 } , y _ { o 2 } )$   
14: end if   
15: end if

determine the $d _ { 1 2 } , d _ { 2 3 }$ , d931, θ12, θ23 and $\theta _ { 3 1 }$ given 3 POIs and their corresponding directions of EyeLoc sightline.

Given POI coordinates $( ( x _ { 1 } , y _ { 1 } ) , ( x _ { 2 } , y _ { 2 } ) , ( x _ { 3 } , y _ { 3 } ) )$ , rotation direction $( d _ { 1 2 } , \ d _ { 2 3 } , \ d _ { 3 1 } )$ and intersection angle $( \theta _ { 1 2 } , \ \theta _ { 2 3 } , \ \theta _ { 3 1 } )$ , we need a method to calculate the coordinate $( x _ { H } , y _ { H } )$ of the user’s position H in floor-plan space. As shown in Fig. 6(c), given the coordinates of two POIs $( \mathrm { e . g . , 1 , 2 } )$ , the rotation direction $d _ { 1 2 }$ and the intersection angle $\theta _ { 1 2 }$ , if $\theta _ { 1 2 }$ is 180◦, H is on the segment between 1 and 2. Otherwise, the possible position of H is on an arc that takes the segment $\vec { 1 2 }$ as the chord and $\theta _ { 1 2 }$ as the inscribed angle. The pixel distance between 1 and 2 is $l _ { 1 2 }$ which equals $\sqrt { ( x _ { 1 } - x _ { 2 } ) ^ { 2 } + ( y _ { 1 } - y _ { 2 } ) ^ { 2 } }$ . M is the middle point of the chord 12\~ and it’s coordinate (xM , yM ) equals $( { \frac { x _ { 1 } + x _ { 2 } } { 2 } } , { \frac { y _ { 1 } + y _ { 2 } } { 2 } } ) . \ O _ { 1 2 }$ is the center of the circle and R is the length of its radius. We use $( x _ { o } , y _ { o } )$ to indicate the coordinate of $O _ { 1 2 } .$ If $\theta _ { 1 2 }$ is $9 0 ^ { \circ }$ , $O _ { 1 2 }$ and M have the same coordinate. Otherwise, since 1 and 2 are on the circle, the chord $\bar { 1 2 }$ is perpendicular to $M O _ { 1 2 }$ and we have the following equation:

$$
\frac {x _ {1} - x _ {2}}{y _ {1} - y _ {2}} = - \frac {y _ {o} - y _ {M}}{x _ {o} - x _ {M}} = k \tag {3}
$$

where k is the slope of the chord $\bar { 1 2 } .$ Moreover, the central angle $\angle 1 O _ { 1 2 } 2$ is twice the corresponding inscribed angle which equals $1 8 0 ^ { \circ } - \theta _ { 1 2 }$ and $\angle 1 O _ { 1 2 } M$ is half the central angle $\angle 1 O _ { 1 2 } 2 .$ . Hence, $\angle 1 O _ { 1 2 } M = 1 8 0 ^ { \circ } - \theta _ { 1 2 }$ and $\begin{array} { r } { R = \frac { d _ { 1 2 } } { 2 \sin \theta _ { 1 2 } } } \end{array}$ . For the length of $O _ { 1 2 } M$ , 2 sin θ12 we have the following equation:

$$
\sqrt {(x _ {o} - x _ {M}) ^ {2} + (y _ {o} - y _ {M}) ^ {2}} = - \frac {l _ {1 2}}{2 \tan \theta_ {1 2}} \tag {4}
$$

Combining Equ. 3 and Equ. 4, we can obtain $( x _ { o } , y _ { o } )$ as follows:

$$
x _ {o} = x _ {M} \pm \frac {l _ {1 2}}{2 \tan \theta_ {1 2} \sqrt {1 + k ^ {2}}}; y _ {o} = y _ {M} \mp \frac {k l _ {1 2}}{2 \tan \theta_ {1 2} \sqrt {1 + k ^ {2}}} (5)
$$

Besides $O _ { 1 2 } ,$ , we obtain another false center of circle $O _ { 1 2 } ^ { \prime }$ which is symmetric with $O _ { 1 2 }$ by taking $\bar { 1 2 }$ as a mirror. To filter out the outlier ${ \dot { O } } _ { 1 2 } ^ { \prime } ,$ we further exploit the information of the rotation direction $d _ { 1 2 }$ and acute/obtuse angle $\theta _ { 1 2 }$ . If $\theta _ { 1 2 }$ is an acute angle, $O _ { 1 2 }$ is on the same side with H regarding segment 12\~ . Otherwise, $O _ { 1 2 }$ is on the opposite side with $H .$ . In this way, we can identify the unique coordinate of $O _ { 1 2 }$ . Algorithm 2 summarizes the detailed calculation of $O _ { 1 2 }$ and $R .$ Now, we know H is on an arc determined by $O _ { 1 2 }$ and R. Similarly, we can calculate another arc where H is on with $\mathrm { P O I _ { 2 } }$ , POI3 and $\theta _ { 2 3 }$ . We further calculate the intersections of these two arcs. One intersection is $\mathrm { P O I } _ { 2 } ,$ the other is the position of H.

In the angel-based geometric localization model, localization bias may be incurred by an unexpected situation: when H, POI1, POI2 and $\mathrm { P O I _ { 3 } }$ are on the same circle, we cannot localize H through the geometric constraints of the 3 POIs. This situation rarely happens in practice as shown in Section V. Moreover, we may be able to observe more than 3 POIs at large shopping malls. If the situation has happened, EyeLoc will popup a message to remind the user that he/she needs to walk several steps and relocalize himself/herself.

When the coordinate of $H$ is known, we can calculate the directions of HPOI1, $H \mathrm { P O I _ { 2 } }$ and $H \mathrm { P O I _ { 3 } }$ in floor-plan space. Then, with $\delta _ { 1 } , \delta _ { 2 }$ and $\delta _ { 3 } ,$ we can calculate the angle offset $\Delta _ { N }$ between the vision north $N _ { v }$ and floor-plan north $N _ { f } .$ Given any user’s heading direction $( \mathrm { e . g . }$ , camera facing direction) in vision space, we can infer his/her heading direction in floor-plan space. Overall, EyeLoc can calculate a user’s position and heading direction by observing no less than 3 POIs. More POIs can further improve the accuracy as introduced in Section III-E.

# C. Raw Data Collection

EyeLoc takes three data sources as input: view images captured by the camera, view image attributes measured by motion sensors and the floor-plan image fetched from indoor map providers. The camera and motion sensors work during the circle shoot, while the user is moving and the smartphone may be shaking slightly. To control the consequent measurement errors, as well as the processing latency and overhead, we conduct the raw data collection as follows:

1) View Images: Two system parameters are crucial to image shooting. One is the image resolution $I _ { r } .$ . The higher its value is, the text of more POIs can be accurately detected and recognized. However, the processing time also increases when $I _ { r }$ becomes high.

![](images/2cfcf70f7dc9b080597e9fed5de9676ade5e084219b213af6306bccb1def9bf2.jpg)



Fig. 7. Illustration of the camera facing direction δ measurement.

![](images/72b99224d4ca2309f461d7c14e11f320ad2ba1b817771c7e265e1fb8c659cde2.jpg)



Fig. 8. The influence of image blur on the accuracy of text detection.

![](images/eeda13e116b865f43ff19c9cf511e87aca4515b9ce6f7eb7bbb3af3675e3c397.jpg)



Fig. 9. The angle velocity measured by different combination of motion sensors.

Empirically, EyeLoc fixes $I _ { r }$ as 1536p during the circle shoot. The other parameter is the shooting frequency $f _ { s } ,$ , which means the interval between two adjacent view images is $\frac { 1 } { f _ { s } }$ . A high $f _ { s }$ ensures all surrounding POIs can be recorded when the rotation speed of a user is fast. Redundant view images also have a negative influence on processing time. EyeLoc selects a relatively high $\bar { f } _ { s }$ to guarantee the abundance of raw data. Later in Section III-D a smaller resolution $I _ { p }$ will be introduced for further image filtering and complement $I _ { r }$ and $f _ { s } .$ .

2) Motions Sensor Readings: In most cases, when a user operates circle shoot, the facing direction of the user and his/her smartphone camera is the same as illustrated in Fig. 7. We define the EyeLoc sightline of an object as the virtual line between the object and the user as shown in Fig. 7. The direction of a sightline δ is the angle between earth north and the projected direction $Z ^ { \prime }$ of the smartphone $Z$ axis, which is measured through the estimation of the camera facing direction.

We use the motion sensors $( \mathrm { e . g . }$ accelerometer, gyroscope and compass) to capture the camera facing direction. EyeLoc continuously samples the readings of the motion sensors. We collect the direction of gravity via the acceleration sensors along 3 smartphone axes $( { \mathrm { e . g . , ~ } } { \check { X } } \ , \ { \check { Y } }$ and $Z$ ), and determine the direction of north with compass sensors to calculate the direction of $Z$ in the earth coordinate system. As a result, the direction of $Z ^ { \prime }$ and δ are calculated correspondingly. To remove potential magnetic interference and bursty noise, EyeLoc adopts several methods [19] [20] to calibrate the camera facing the direction of each view image.

3) Floor-plan Image: Given the coarse GPS readings in a shopping mall, EyeLoc can fetch the floor-plan images of all floors in the shopping mall through APIs of indoor map providers. Each floor-plan image contains the skeleton and name of all POIs on that floor.

Overall, the raw data collection module outputs a series of view images, corresponding EyeLoc sightline directions and floor-plan images. However, the redundancy and measurement errors existing in raw data will incur computation inefficiency and localization error. Next, we introduce the methods to improve the efficiency and robustness.

# D. POI Extraction

For the floor-plan image, we use text detection/recognition techniques to collect POI signs and record their coordinates on the floorplan image as shown in Fig. 1(c). As for view images, our goal is to detect all available POI signs and determine corresponding sightlines. The angle formed by two EyeLoc sightlines is critical for position matching in Section III-E. The key issue is how to achieve real-time performance on smartphones.

1) View Image Outlier Filtering: During raw data collection, we obtain abundant view images and motion sensor readings. As the user is moving while the camera and motion sensors are working, some data contain errors that can significantly influence the localization result. Filtering out those data can also save the processing time.

![](images/c00583799691d6edd61d6e3963fbbac0ac506e3a1b572e7b9bb72bc867c11de9.jpg)



Fig. 10. Feature point matching in two different view images of the same POI.

![](images/337de359a21895a0bc013b838a9e08c8952919668141a2f4137a85dd071b4f8f.jpg)

![](images/209f32834e0040fce2db5684bdfafcc33af14fcb748ad7f173d2182bd2ef465f.jpg)  
(a)

![](images/29a2b67885955a0b03446b77fd3a4230dffe7193ed113ddb8b1d311964e770bb.jpg)

![](images/7d967b0a90a963c67601aae913585ea974da2bcaf1bd12b44a7f745c34152b7d.jpg)  
(b)

![](images/3e3bcbecd7d4863c4a706a5666048d67949bf048df15f7460c7359e2023356ee.jpg)

![](images/7890b2805fe02860435e1176be43d3f0023e20adacb595b61ccc3b683836d89c.jpg)  
(c)   
Fig. 11. Landmark identification and text bounding box

If a view image is blurred, we cannot detect any text at all. We treat blurred view images as outliers that should be filtered out. EyeLoc adopts Laplacian-based operator [21], which is a widely used function for focus measure, to define the degree of image blur. We randomly selected 1692 view images from the whole data set shot in two large shopping malls (Section V). We guarantee there is at least one POI sign in each of these view images. In Fig. 8, the black curve shows the Laplacian variances of these images are distributed from 0 to 400. The larger the variance ${ \mathrm { i s } } ,$ the less the image blur is, as shown in the comparison between the example view images with variance in the range [0,20] and [300,320]. In a view image, if the length of any recognized text string is more than 2, it is text-detectable. We further select 15 view images from each level of image blur to evaluate the probability of text detection under different levels of image blur. The red curve shows that the probability of text detection is higher than 80% when the Laplacian variance is larger than 80. Hopefully, we should filter out those view images whose Laplacian variance is less than 80 because it is hard to detect any text clues from it. Thus, we define a threshold $\Delta _ { L a p }$ (e.g., approximate 80) to determine whether a view image is blurred or not.

Moreover, the smartphone vibration around Y axis and Z axis can influence the position of a POI on view images. As a result, the estimation error of EyeLoc sightline may increase. The gyroscope outputs the angular velocity around 3 axes as $\omega _ { x } , \omega _ { y }$ and $\omega _ { z } ,$ then the total angular velocity is $\omega = \sqrt { \omega _ { x } ^ { 2 } + \omega _ { y } ^ { 2 } + \omega _ { z } ^ { 2 } } .$ On the other hand, we can also calculate the angular velocity $\omega ^ { \prime }$ given the $Z ^ { \prime }$ direction of two adjacent view images and the corresponding time interval. We conduct a circle shoot by setting $f _ { s }$ as 2Hz. During circle shoot, we manually vibrate the smartphone as a common user does when the picture ID is from 15 to 18 and from 26 to 30. As shown in Fig. 9, the angle velocity difference between ω and $\omega ^ { \prime }$ is close to zero as usual. However, smartphone vibration will obviously increase the difference. This observation indicates different motion sensors have different sensitivity for the vibration. Hence, EyeLoc sets a threshold $\Delta _ { \omega }$ and filters those view images when the angular velocity difference is larger than $\Delta _ { \omega }$ .

2) Text Filtering and Matching: In large shopping malls, text may appear or extract anywhere. It is possible to detect multiple text strings from a view image. Fig. 11 shows the case in the office environment. The top figures are RGB scene pictures and the bottom figures exhibit the red text bounding boxes on corresponding binary images. We can see that besides the desired text bounding box of “STARBUCK”, many redundant ones are also extracted from the textures of curtains, tables and switches. Moreover, in Fig. 11(a), only part of “STARBUCK” are recognized. Situations in shopping malls can be more complex since the name of a POI may appear at multiple places.

EyeLoc filters out the irrelevant and duplicate text bounding boxes through the following steps. First, given the minimum and maximum length of POI names extracted from floor-plan images, EyeLoc filters out the illegal text strings. Second, we group the rest of the text strings. Two text strings belong to the same group when the difference between them is smaller than a threshold $\Delta _ { t }$ . The difference between the two text strings is defined as the ratio between their Levenshtein Distance [22] and the maximum string length. Given the list of POI names extracted from floor-plan images, EyeLoc further removes those invalid groups whose text strings are not on the list (i.e., the similarity is smaller than $\Delta _ { t }$ in comparison with any POI name). Finally, in each valid group, EyeLoc combines the coordinates of all text bounding boxes to calculate the average value as the unique text bounding box position of the observed POI on the view image. In this way, EyeLoc identifies available POIs and corresponding positions of text bounding boxes on a view image.

3) Sparse Image Processing: After filtering the outliers of view images, for all observed POI, we need to exactly find the view images (e.g, Fig. 5(c)) where the corresponding text bounding boxes appear in the middle. The intuitive approach is to process all view images, but this will incur heavy networking and computation burden as the sampling frequency $f _ { s }$ is set high. Even worse, the desired view image may not be captured or blurred. Instead of processing every view image to extract the geometric information of all potential POIs, EyeLoc develops a sparse image processing approach to achieve the same goal. The key idea is after the position of a text bounding box is known from a view image (e.g., Fig. 5(b)), we can enable EyeLoc sightline estimation of a POI with one more view image which contains the same POI (e.g., Fig. 5(d)) by feature point matching. As shown in Fig. 10, given two view images $I _ { 1 }$ and $I _ { 2 } ,$ the text bounding box of $I _ { 1 }$ is extracted and it is $d _ { 1 }$ pixel from the middle line. Then, in $I _ { 2 } ,$ , we use ORB algorithm to extract the same feature points which fall into the text bounding box of $I _ { 1 }$ . Given a feature point, its coordinates on $I _ { 1 }$ and $I _ { 2 }$ are $( x _ { 1 } , y _ { 1 } )$ and $( x _ { 2 } , y _ { 2 } )$ . The pixel distance of the feature point is $\sqrt { ( x _ { 1 } - x _ { 2 } ) ^ { 2 } + ( y _ { 1 } - y _ { 2 } ) ^ { 2 } }$ . The average pixel distance of all feature points is indicated as $l _ { f }$ . Due to the approximate constant ratio between pixel distance and central angle, given their direction as $\delta _ { 1 }$ and $\delta _ { 2 } ,$ , we can calculate the direction δ of the POI EyeLoc sightline as following:

$$
\delta = \delta_ {1} + \frac {d _ {1}}{l _ {f}} (\delta_ {2} - \delta_ {1}) \tag {6}
$$

When we recognize the text bounding box of a POI from a view image, we use its adjacent images which probably contain the same POI to calculate the direction of POI EyeLoc sightline with Equ. 6.

![](images/a15e0f11002125a63a4ddf46204dc42bfc21613d827ad5463ef62dd6d6386e44.jpg)



(a) POI Error

![](images/e1d48e8d72b9179038ce2806b8b9b3480c230892a9bb396e35aefd929cf50ed6.jpg)



(b) Direction Error   
Fig. 12. The localization sensitivity regarding (a) POI error and (b) direction error.

To extract the geometric information of all observed POIs, the problem becomes to quickly target a view image for each observed POI. Given n view images $\left\{ I _ { 1 } , \mathbf { \bar { { I } } } _ { 2 } , . . . , I _ { n } \right\}$ , we set a step length $\Delta _ { s }$ and view images $\begin{array} { r } { \{ I _ { \Delta _ { s } } , \bar { I } _ { 2 \bar { \Delta _ { s } } } , . . . , \bar { I } _ { k \Delta _ { s } } \} ( k = \lfloor \frac { n } { \Delta _ { s } } \rfloor ) } \end{array}$ are selected for processing. Hopefully, if the minimum number of view images of a POI is larger than $\Delta _ { s }$ , EyeLoc cannot miss the view image of any observed POI. However, due to the possible failure of text recognition, we may miss some POIs so that no enough POIs are extracted. In this case, EyeLoc will exponentially reduce $\Delta _ { s }$ and reprocess the new view images until at least 3 POIs are extracted or all view images are processed. Overall, we can fetch enough available POIs and corresponding directions of EyeLoc sightline as soon as possible for later location matching. Next, we remove the potential estimation errors to achieve accurate location matching.

# E. Position Matching

According to the localization model in Section III-B, the user’s position can be localized with three observed POIs, called localization tuple. Fig. 12 shows the measured POI coordinates of a localization tuple $( \mathrm { e . g . , P O I _ { 1 } , P O I _ { 2 } , P O I _ { 3 } } )$ and the calculated user’s position H. The corresponding measured intersection angle $\theta _ { 1 2 } , \theta _ { 2 3 }$ and $\theta _ { 3 1 }$ are $1 2 0 ^ { \circ }$ . The POI text bounding boxes in the floor-plan image may not exactly align with that in physical space. Due to the POI coordinate errors, we assume the true POI positions may appear on a circle around it and the radius is $R _ { e } .$ . As shown in Fig. 12(a), when moving the POI1 around a circle with a radius of 3 pixels and keeping the positions of other POIs fixed, the calculated positions are shown as the green marks in the figure. Moreover, due to the possible errors from motion sensor and image processing, $\theta _ { 1 2 }$ may be inaccurately measured in comparison with the true intersection angle $\theta _ { 1 2 } ^ { \prime }$ as shown in Fig. 12(b). The same situation may happen for $\theta _ { 2 3 }$ and $\theta _ { 3 1 }$ . We assume the error of $\theta _ { 1 2 } , \theta _ { 2 3 }$ and $\theta _ { 3 1 }$ is in the range of $[ - \Delta _ { \theta } , \Delta _ { \theta } ]$ . For $\theta _ { 1 2 }$ , Fig. 12(b) shows the possible true positions shown as the green marks when $\Delta _ { \theta }$ is $1 0 ~ ^ { \circ } .$ . Regarding the errors of $P O I _ { 1 }$ and $\theta _ { 1 2 }$ , the maximum localization errors are indicated as $d _ { e }$ . The ratio between $d _ { e }$ and $R _ { e }$ or $\Delta _ { \theta }$ is further defined as the error sensitivity of a POI or an intersection angle. Given a localization tuple u, we define its localization error sensitivity les(u) as the sum of the error sensitivity of all three POIs and three intersection angles.

When k $\left( k \geq 3 \right)$ POIs are extracted, we have total $m = k ( k -$ $1 ) ( k - 2 ) / 6$ localization tuples indicated as $\{ u _ { 1 } , u _ { 2 } , . . . , u _ { m } \}$ . For the $i ^ { \mathit { t h } }$ tuple $u _ { i } .$ , its localization result and error sensitivity are indicated as $h _ { i }$ and $l e s ( u _ { i } )$ . The larger the $l e s ( u _ { i } )$ is, the more accurate the $h _ { i }$ is. Hence, EyeLoc sets the weight wi of localization result $h _ { i }$ as $1 / l e s ( u _ { i } )$ . Then, the final match location h is calculated as follows:

$$
h = \frac {\sum_ {i = 1} ^ {m} w _ {i} h _ {i}}{\sum_ {i = 1} ^ {m} w _ {i}} \tag {7}
$$

With h and k extracted POIs, EyeLoc can calculate the user’s heading direction according to the method in Section III-B.

# IV. IMPLEMENTATION

We implement EyeLoc as a mobile application in Android 7.0. Fig. 13 demonstrates the user interface (UI) of EyeLoc application when we conduct experiments in a shopping mall. As shown in Fig. 13(a), after a user opens EyeLoc application, the view captured by the camera appears on the smartphone screen. The view keeps refreshing with the circle shoot. A vertical white line appears in the center of the screen as the reference. Once a POI appears during the circle shoot, EyeLoc extracts its text string from the view image. If the text bounding boxes is aligned with the sightline of the smartphone camera, a green checkmark appears on the screen like Fig. 13(b). In this way, users can simply record POIs as many as possible. After the user finishes the circle shoot, EyeLoc exhibits the user’s position and heading direction on the floor-plan image as shown in Fig. 13(c). We discuss several system details and settings as follows.

![](images/4fe2c1584ab0b7c9c0ffa0a26e4268564040ad4890543afa16e746cbb951e6bd.jpg)



(a) An view image during the circle shoot

![](images/6c8a546d8241ce4ce75a314b5aef99be90b9f3a6f7fd490f5819f459c56818dc.jpg)



(b) POl extraction

![](images/91380fad00b63b8f0cc6566e3216e36df5c45bfeb8c370e04bb2afdccbeba8f5.jpg)



(c) Display the position and the heading direction on the floorplan image

Fig. 13. The UI of EyeLoc when running in a large shopping mall.   
![](images/c25f040bbca595a805c4a3180f0ef89a281b3ec31c828898ea296dd2843ec2f6.jpg)



(a) Different text recognition approaches

![](images/b3545fa2ba51df202f8ae1a7267a373b966b505e9cd8afb695e106aecbf05bcf.jpg)



(b) Different image resolution choices   
Fig. 14. The performance under different text recognition approaches and different image resolution choices

# A. Scene Text Detection and Recognition

Scene text detection and recognition techniques serve as a fundamental role in EyeLoc. We compare several existing techniques on Android smartphones in terms of recognition accuracy and processing time. Here, we adopt the same method in Section III-D2 to judge the similarity between two text strings. $\Delta _ { t }$ is set as 50%. We randomly select 100 images shot by a smartphone in two large shopping malls. Some of them are shot at daytime and the others are shot at night. Each image contains one shop sign which is manually labeled as the ground truth.

1) Local processing v.s. Cloud processing: According to different processing platforms, we can either perform the text detection and recognition processes locally on the smartphone, or remotely on cloud. The approaches of local processing include OpenCV [16] and Tesseract [17]. We choose Baidu Cloud as the platform for the typical cloud processing. LTE network, which is available in most shopping malls nowadays, is adopted to connect the smartphone with the cloud server.

Given the dataset of 100 images, the recognition accuracy and processing time are shown in Fig. 14(a). We can see that the text recognition accuracy of Baidu Cloud is 66%, which is much higher

TABLE I SUMMARY OF SYSTEM PARAMETERS 

<table><tr><td>Symbol</td><td>Description</td><td>Value</td></tr><tr><td> $I_p$ </td><td>The resolution of view image</td><td>1080p</td></tr><tr><td> $f_s$ </td><td>The sampling frequency of view image</td><td>2 Hz</td></tr><tr><td> $\Delta_{Lap}$ </td><td>The threshold of view image blur</td><td>80</td></tr><tr><td> $\Delta_\omega$ </td><td>The threshold of angle velocity difference</td><td> $10^\circ/s$ </td></tr><tr><td> $\Delta_t$ </td><td>The threshold of text string similarity</td><td>50%</td></tr><tr><td> $\Delta_s$ </td><td>The step length of sparse image processing</td><td>3</td></tr><tr><td> $\Delta_\theta$ </td><td>The error of intersection angle estimation</td><td> $10^\circ$ </td></tr><tr><td> $R_e$ </td><td>The error of extracted POI coordinates</td><td>20 pixels</td></tr></table>

than 12% of Tesseract and 2% of OpenCV. The text recognition accuracy of Tesseract and OpenCV is surprisingly low since it is challenging for the text classifiers and extreme region extraction to adapt to the complex lighting condition and text format of POI signs. The average processing time of Baidu Cloud is 2s which is a little higher than that of OpenCV, but much smaller than Tesseract. Due to the superior recognition accuracy and low processing time, we choose cloud processing instead of local processing.

2) The influence of image resolution: We further explore the performance of Baidu Cloud by using different image resolutions. We vary the resolution of the 100 images from 180p to 1538p. The performance is shown in Fig. 14(b). We can see that both text recognition accuracy and processing time increase with the increase of image resolution. When the image resolution is 720p, the text recognition accuracy and average processing time are 54% and 0.74s. In comparison, the text recognition accuracy and average processing time increase to 72% and 1.89s when the image resolution increases to 1536p. EyeLoc chooses $I _ { p }$ to keep the text recognition accuracy higher than 60%. Meanwhile, EyeLoc minimizes the expected time for successfully recognizing a POI which is the ratio between the average processing time and the recognition accuracy. Hence, we set $I _ { p }$ as 1080p. For outlier view image filtering, according to the observation of Fig. 8 and 9, we set $\Delta _ { L a p }$ and $\Delta _ { \omega }$ as 80 and $1 0 ^ { \circ } / s$ .

# B. Circle Shoot Operation

We set $f _ { s }$ as 2Hz, namely EyeLoc shoots 2 view images per second. The step length for sparse image processing $\Delta _ { s }$ is set to be 3. According to our empirical experience, 20% of view images are observed to be blurred (Fig. 8) and 37% of 1080p view images encounter text recognition failure (Fig. 14(b)), it is better to obtain at least 6 view images of a POI (e.g., 3s) to ensure the reliability and efficiency of POI extraction. That means if there are 5 POIs around a user, the circle shoot will take 15s at least.

# C. Floor-plan Images

EyeLoc generates high-resolution indoor floor-plan images from Gaode Maps. Since the font of POI texts on floor-plan images is in regular print format, the text recognition accuracy is close to 100%. The resolution of the floor-plan image is set to 2560×1440. Using the floor-plan image, however, the texts of different shops are often placed in the middle of the shops’ blocks, while the POIs captured by EyeLoc are shop signs which are often located on the entrances. The caused direction and coordinate errors can further lead to possible localization errors. To mitigate the influence of the floor-plan error, we refine the shop coordinates with fine-grained floor-plan data fetched from Gaode Maps. The floor plans are shape files containing several image layers, depicting shops, roadmaps, and doors. In our experiments we directly use the coordinates of the “doors” as the location of POIs (e.g., the blue circles in Fig. 18). The coordinates acquired this way are more accurate and it is beneficial to improve localization quality. Moreover, for error sensitivity estimation, we empirically set $\Delta _ { \theta }$ and $R _ { e }$ as 10◦ and 20 pixels. The threshold of text string similarity $\Delta _ { t }$ is set to be 50%.

Overall, Table I summarizes all system parameters of EyeLoc.

# V. EVALUATION

We evaluate EyeLoc with different smartphones (e.g., MI 5 and Huawei Mate 7) in an office environment1 and two large shopping malls2. The office environment is a 7m×9m office room. We print 6 shop signs such as NIKE on A4 papers, then hang them on the wall or curtains in clockwise order. The area of each floor in two large shopping malls is $7 { , } 5 0 0 ~ \mathrm { m } ^ { 2 }$ and $1 0 , 0 0 0 \mathrm { m } ^ { 2 }$ respectively. The area of the semi-outdoor Outlets is about 70,000 m2. The distance between adjacent shops and the width of corridors are much larger than office and shopping malls. We invited two volunteers (Male, 20-30 years old) to complete all the experiments both in daytime and at night. User 1 uses MI 5, User 2 uses Huawei Mate 7. The two users exhibit different habits as User 1 turns faster than User 2.

![](images/c7e604083fbbd21e897efc9d894252cc57f70c9fcc1dffd64fa2047dc5f7a2b7.jpg)



(a) The CDF of localization error i different environments.

![](images/b6d1d7139b8462ac5830f29142b1c3ea39d06941a3129832ef46df54303b8ab5.jpg)



(b) The CDF of facing direction error in different environments.

Fig. 15. The reliability of EyeLoc.   
![](images/ede21a51f3c6c1ccbbffb88bbe0673592c9a0a6c86fc4b9bc5419393cbeeba68.jpg)



(a) The influence of the number of observed POIs.

![](images/1f5d681dd553073e17337f8fe5d6286abda3b8fdfa2cce5de9d6bb12fe0ebba9.jpg)



(b) The influence of smartphone hardware.   
Fig. 16. Different influencing factors.

In the office environment, we uniformly split the office into 18 areas. Users stand at the center of each area to perform circle shoots. The ground truth is obtained through a laser rangefinder. In the two large shopping malls and the semi-outdoor Outlets, we mainly select the positions near entrances, elevators and bathrooms where users have high localization demands. For each of the 16 positions we evaluated, we also use the laser rangefinder to measure its ground truth. The minimum and maximum distances between the user and a POI are 2.26m and 37.4m in our experiments.

# A. The Accuracy of Localization and Heading Direction Estimation

We first discuss the reliability of EyeLoc. As shown in Fig. 15(a) and Fig. 15(b), in the two large shopping malls, the median errors of localization and heading direction are 2.6m and 10.5◦. The 90- percentile errors of localization and facing direction increase to 4m and 20◦. In the office environment, the 90-percentile errors of localization and facing direction are 1.1m and 8◦, which are much better than the performances in large shopping malls. There are two reasons. First, in the office environment, we can precisely measure the POI coordinates on the floor-plan images. However, the POI

coordinates suffer larger error due to the position mismatch between the text bounding boxes and the observed POI signs on the floorplan images obtained from indoor map providers. Moreover, in the office environment, usually we have only one POI in a view image. However, in large shopping malls, several signs of the same POI may appear in a view image, which will introduce error into the sightline estimation. Given the area as large as $7 { , } 5 0 0 \mathrm { m } ^ { 2 }$ and $1 0 { , } 0 0 0 \mathrm { m } ^ { 2 }$ , 4m and 20◦ is still relatively accurate for the most location-based services.

In 70,000 m2 semi-outdoor Outlets, the 90-percentile errors of localization and facing direction are 5.97m and 20◦. The error of facing direction is comparable with that in shopping malls. The localization error, however, is getting large. The reason is that the distance between user and POIs is larger in Outlets than that in shopping malls. A small estimation error of POI direction can lead to more position estimation errors. Hence, although the facing direction accuracy is similar, the localization error increases in a larger space.

1) The influence of the number of observed POIs: In position matching, EyeLoc utilizes the POI redundancy to mitigate the measurement errors of POI coordinates and EyeLoc sightlines. Fig. 16(a) shows the relationship between the number of observed POIs and the localization error. We can see the average localization error decreases as the number of observed POIs increases. Specifically, the localization error decreases by 33.7%/34.9% when the number of observed POIs increases from 3 to 4/5 in large shopping malls respectively. This indicates the error mitigation approaches are effective for improving the localization accuracy. Moreover, 5 or more POIs cannot provides more useful information for improving the localization accuracy rather than 4 POIs.

2) The influence of POI distribution: We evaluate the influence of POI distribution on the localization error. Fig. 17 shows the localization error distribution of 18 experiment positions given the positions of 6 POIs. The darker the color is, the higher the localization error is. We can see the localization error is getting higher when the distance between the user’s position and POIs is large. Moreover, the top left area is higher than its surrounding area, that is because it is close to the circle formed by several POIs. According to Section III-B, when the user’s position and POIs tend to be on the same circle, the accurate localization will be hard to achieve. Moreover, we give two experiment positions in shopping mall 1 (Fig. 18(a)) and shopping mall 2 (Fig. 18(b)). The white areas are roads and the yellow blocks are shops. The green points are the results of EyeLoc localization. The red points are the ground truths. The localization error of the position in shopping mall 1 is 1.56m, but that of the other one is 3.64m. From the POI distribution on the floor-plan images, we can see the large error in Fig. 18(b) is because the true position, GLORIA, AFU and MOFAN tend to on the same circle. In contrast, the position in Fig. 18 has more POIs which are close to it and uniformly distributed. Hence, the results suggest that the localization error is indeed related to the distribution of surrounding POIs, especially when the user’s position and observed POIs are on the same circle. However, the situation only happens twice among total 29 positions. If the situation happens, we will ask the user to walk a short distance and relocalize himself/herself again.

3) The influence of smartphone hardware: We further evaluate the localization error by using different smartphones at the same positions in large shopping malls. The results are shown in Fig. 16(b). We can see the average localization error is 2.66m for MI 5 and 2.51m for Huawei Mate 7. Since User 2 turns slower than User 1, the more redundant view images make the localization error variance of Huawei smartphone is smaller than MI 5. Overall, EyeLoc works well on both smartphones and does not depends on any smartphone specific hardware and parameters.

# B. Processing Efficiency

Another important metric is the processing time, which is from the end of circle shoot to the user’s position is shown on the screen. Since the view image processing dominates the overall processing time, we designed two approaches, namely, outlier image filtering and sparse image processing. We evaluate the processing time of three methods: “All” indicates we process all view images; “Filter” indicates we only process the view images after filtering the outliers. “Filter+Sparse” indicates we combine outlier filtering and sparse processing approaches. As shown in Fig. 20, we can see “Filter+Sparse” outperforms the other two methods and its median processing time is 18.2s which is 55.5% shorter than “All”. Moreover, the median processing time of “Filter” is 27.3s which is 36.2% shorter than “All”. That verifies both outlier filtering and sparse processing are effective to improve the processing efficiency. In the worst case, the processing time of “Filter+Sparse” is 37.4s. That means the user can obtain the localization result in no more than half a minute after circle shoot. Fig. 21 further shows the processing time on different smartphones.

![](images/100ae0d1e5254353aafb56c3a31409e6c9b0d7415e2a2b6373a1c2200aef8c54.jpg)



Fig. 17. The distribution of the localization error in office environment.

![](images/1b6f718ec75d3de9225ebe6c239cde18c0bdbefe2778150780dab43b14094cf3.jpg)



Fig. 18. Two experiment positions in two shopping malls.

<table><tr><td>Function Module</td><td>Energy Efficiency (W)</td></tr><tr><td>Image recording</td><td>1.94</td></tr><tr><td>Image processing</td><td>0.34</td></tr><tr><td>Location calculation</td><td>0.65</td></tr><tr><td>Total EyeLoc</td><td>2.17</td></tr></table>

Fig. 19. Energy efficiency of EyeLoc

# C. Energy Efficiency

We evaluate the energy efficiency of EyeLoc with Battery Historian [27], which is a tool to analyze battery consumption using Android “bugreport” files. We decompose EyeLoc to 3 function modules which are image recording, image processing and location calculation. To evaluate the energy efficiency of each function module, we set them in infinite loops and continuously run them for an hour. For each experiment, we charge MI 5 to 100% at the beginning. We also evaluate the total energy efficiency of EyeLoc with the same method. For each experiment, we repeat it 3 times and obtain the average value. The results are shown in Tab. 19. We can see that among different function modules, the energy cost of image recording is 1.94 W which is much higher than that of image processing (0.34 W) and location calculation (0.65 W). Hence, the network communication of image processing and computation of location calculations is much more energy-efficient than shooting images with the camera. In our implementation of EyeLoc, we use multi-thread to overlap image recording and processing. The circle shooting usually dominates the operation time of EyeLoc. As a result, the total energy efficiency of EyeLoc is 2.17 W which is mainly spent on imaging shooting.

# D. Localization Performance Comparison

To compare the localization performance, we implement Sextant [13] and evaluate its performance in the semi-outdoor Outlets. For each shop, we take 3 high-quality images to construct the visual clue and localization map. During evaluation, users are well trained

![](images/281264978e040201da99a6e684e3fd3557a0dfda88d2f39cac6772d083115086.jpg)



Fig. 20. The processing efficiency with outlier filtering and sparse processing.

![](images/976bbe90a0c17f6db31e3ca65119bfed6abeb0e789c8316899efdbe71729345d.jpg)



Fig. 21. The comparison of processing time on different smartphones.

and follow the rules of Sextant to shoot images. For example, users manually keep the POI in the middle of the image. The performance comparison is shown in Fig. 22. We can see the 90-percentile localization error of Sextant is 6.6m which is 10% higher than EyeLoc. The reason is that EyeLoc can automatically capture the angle of POI which is less accurate by using the user dependent method of Sextant. If users are not well trained, the localization error of Sextant could be increased since the increasing error of POI angle estimation.

# VI. RELATED WORK

In recent years, many works target on developing efficient indoor localization and positioning systems. However, most of them need some site surveying. Some of them even need custom hardware. According to different types of data sources, we divide existing works into four categories.

Wi-Fi Signal Many indoor localization methods are proposed based on Wi-Fi signals. One approach is fingerprinting-based. The Wi-Fi signal patterns serve as the fingerprint that represents every location. The system manager builds a fingerprint database in the target areas to initialize localization service. The user’s location is estimated by matching the measured fingerprint to database records. RADAR [28], Horus [29], Place Lab [30], PinLoc [31] and Smart2 [32] use site survey to construct the fingerprint database. LIFS [23] and Zee [33] further utilize crowdsourcing to alleviate the burden of labor-intensive site survey. A theoretical analysis around how good a performance the RSS fingerprinting can achieve is provided in [34].

The other approach is model-based. The basic principle is the relationship between the geometric structure from Wi-Fi access point (AP) to user’s location and the physical features of the received Wi-Fi signal can be modeled [35]. If the location of Wi-Fi AP is pre-known, the user’s location can be inferred. Based on the log-distance path loss (LDPL) model, EZ [36] uses the received signal strength (RSS) to estimate the signal propagation distance and combines several estimations of different APs to find the user’s location. SpinLoc [37] and Borealis [38] observe if a user faces an AP, the RSS is usually higher than the user turns his back on the AP. After making a full 360◦ turn, SpinLoc and Borealis extract the angle-of-arrival (AoA) of several APs to determine the user’s location. ArrayTrack [39] uses antenna array and Wi-Fi signal phase to obtain accurate AoA spectrum to calculate a user’s location. CUPID [40], SAIL [24], Chronos [5] and Ubicarse [41] further refine the distance and AoA measurement methods to achieve high localization precision or adapt to COST Wi-Fi AP. SpotFi [42] proposes a super-resolution AoA algorithm to extract AoAs from Channel State Information (CSI).

Visible Light In a typical visible light positioning (VLP) system, lamps (fluorescent and LED) are served as landmarks. After a light receiver (smartphone camera or photodiode) obtains several lamps’ location, the light receiver further measures the geometric structure from the observed lamps to find the user’s location. Luxapose [8] takes an image which contains several LEDs as input and fetches LEDs’ AoA to calculate the user’s location. According to inherent and common optical emission features of both LED and fluorescent, iLAMP [9] and Pulsar [43] identify a lamp’s location from a preconfigured database by feature matching. iLAMP further combines camera image and inertial sensors to infer user’s location. Pulsar utilizes a custom device to measure the lamp’s AoA, then determine user’s location.

![](images/4c013b6efa3442eec2c7096e601db02e9fb54243ecc2617d78d2f60c75ee84ac.jpg)



Fig. 22. The localization performance comparison between EyeLoc and Sextant in semi-outdoor Outlets.

<table><tr><td>Technology</td><td>Site Survey</td><td>Custom Hardware</td><td>Range (m2)</td><td>Localization Error (m)</td><td>Heading Error (°)</td></tr><tr><td>LIFS [23]</td><td>WiFi fingerprint</td><td></td><td>1,600</td><td>9</td><td>NA</td></tr><tr><td>SAIL [24]</td><td>WiFi AP location</td><td>√</td><td>2,800</td><td>2.3</td><td>NA</td></tr><tr><td>SmartLight [10]</td><td>Lamp modification</td><td>√</td><td>16</td><td>0.5</td><td>NA</td></tr><tr><td>iLAMP [9]</td><td>Lamp fingerprint</td><td></td><td>8</td><td>0.032</td><td>2.6</td></tr><tr><td>iMoon [25]</td><td>Environment image</td><td></td><td>1,100</td><td>2</td><td>6</td></tr><tr><td>Sextant [13]</td><td>Environment image</td><td></td><td>11,250/60,000</td><td>20</td><td>NA</td></tr><tr><td>FollowMe [26]</td><td>Geomagnetic fingerprint</td><td></td><td>2,000</td><td>2</td><td>NA</td></tr><tr><td>EyeLoc</td><td>FREE</td><td></td><td>7,500/10,000/70,000</td><td>5.97</td><td>20</td></tr></table>

Fig. 23. Summary of existing indoor localization systems

The other approach is to customize the lamp to establish a mapping function between the location of light receiver and the corresponding received light physical features. CELLI [44] develops a custom LED bulb which projects a large number of fine-grained light beams toward the service area. CELLI adopts a modulation method to encode the coordinate of a fine-grained cell into the corresponding light beam. Thus, the light receiver can obtain its location by visible light communication. SmartLight [10] uses LED array and a lens to form the light transmitter. On LED array, different LED lamps use different PWM frequencies. According to the frequencies of the received light, the coordinate of the observed LEDs circle can be inferred on LED array. The location of light receiver can be further calculated by optical geometric translation function of the lens.

Scene Image Using scene images containing landmark details and architectural features is also a popular direction. SLAM (Simultaneous Localization and Mapping) aims to output a map as well as the user’s real-time location. Both 2D and 3D positions are acceptable. We especially introduce SLAM with the camera as its main sensor in this paper. A single image and a floor plan is used as the input in [1] and the main technology is Markov random field. SfM (Structure from Motion) builds a 3D model from 2D images or video. Based on the 3D model, we can know the camera pose and shooting location given another image. iMoon [25] and Jigsaw [45] adopt SfM to construct indoor 3D model and enable localization services. Sextant [13] builds a geometrical model with static reference points and works for a lightweight site survey. All these papers need a collection of images for site survey, which EyeLoc avoids.

Others Magicol [14] and FollowMe [26] combine the geomagnetic field and user trajectory as the fingerprint to localize user’s location. With acoustic speakers as the landmarks, Swadloon [46] and Guoguo [47] use acoustic signal based geometric model and inertial sensors to localize user’s location. Shenlong Wang, etc. [1] utilize the floor-plan image and a scene image to localize a user in large shopping malls. Based on edge, text and layout features of a scene image, they use Markov random field model to infer the camera pose on the floor-plan image. However, they need to search through all possible positions which further incurs huge computation complexity. Hence, it is not practical on COTS smartphones.

To conclude, compared with these methods, as shown in Tab. 23, EyeLoc depends on neither pre-deployed infrastructure nor precollected information. Moreover, EyeLoc does not depend on any custom hardware and can be implemented as a smartphone application. EyeLoc can achieve the comparable accuracy of localization and heading direction in real large shopping malls which are much larger than the prototype deployment of the existing indoor localization systems.

# VII. CONCLUSION

In this paper, we propose EyeLoc, a plug-and-play localization system for large shopping malls without the burden of system bootstrap and calibration. EyeLoc enables the smartphone to imitate human self-localization behavior. After a user opens the EyeLoc application, he/she carries out the circle shoot and the smartphone continuously shoots view images meanwhile. After that, EyeLoc automatically projects the user’s position and heading direction on the floor-plan image. The evaluation results show that the 90-percentile accuracy of localization and heading direction is 5.97m and 20◦. Moreover, EyeLoc can be extended to other environments (e.g., office building, train station, airport) where floor-plan and indoor texts are available. We will extend EyeLoc to these environments in the future.

# ACKNOWLEDGEMENT

This study is supported in part by the National Science Foundation under Grant NSF 1919154, and the NSFC program under Grant 61772446 and 61872081.

# REFERENCES

[1] S. Wang, S. Fidler, and R. Urtasun, “Lost shopping! monocular localization in large indoor spaces,” in Proceedings of ICCV, 2015.   
[2] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil, “Landmarc: Indoor location sensing using active rfid,” Wireless Networks, vol. 10, no. 6, pp. 701– 710, 2004.   
[3] A. Haeberlen, E. Flannery, A. M. Ladd, A. Rudys, D. S. Wallach, and L. E. Kavraki, “Practical robust localization over large-scale 802.11 wireless networks,” in Proceedings of the 10th Annual International Conference on Mobile Computing and Networking, 2004.   
[4] H. Liu, Y. Gan, J. Yang, S. Sidhom, Y. Wang, Y. Chen, and F. Ye, “Push the limit of wifi based localization for smartphones,” in Proceedings of ACM MobiCom, 2012.   
[5] D. Vasisht, S. Kumar, and D. Katabi, “Decimeter-level localization with a single wifi access point.” in Proceedings of NSDI, 2016.   
[6] Z. Yang, L. Jian, C. Wu, and Y. Liu, “Beyond triangle inequality: Sifting noisy and outlier distance measurements for localization,” ACM Trans. Sen. Netw., vol. 9, no. 2, pp. 26:1–26:20, 2013.   
[7] J.-A. Francisco and R. P. Martin, “A method of characterizing radio signal space for wireless device localization,” Tsinghua Science and Technology, vol. 20, no. 4, pp. 385–408, 2015.   
[8] Y.-S. Kuo, P. Pannuto, K.-J. Hsiao, and P. Dutta, “Luxapose: Indoor positioning with mobile phones and visible light,” in Proceedings of ACM MobiCom, 2014.   
[9] S. Zhu and X. Zhang, “Enabling high-precision visible light localization in today’s buildings,” in Proceedings of ACM MobiSys, 2017.   
[10] S. Lin and T. He, “Smartlight: Light-weight 3d indoor localization using a single led lamp,” in Proceedings of ACM SenSys, 2017.   
[11] Q. Niu, M. Li, S. He, C. Gao, S. H. Gary Chan, and X. Luo, “Resourceefficient and automated image-based indoor localization,” ACM Trans. Sen. Netw., vol. 15, no. 2, pp. 19:1–19:31, 2019.   
[12] Y. Tian, R. Gao, K. Bian, F. Ye, T. Wang, Y. Wang, and X. Li, “Towards ubiquitous indoor localization service leveraging environmental physical features,” in proceedings of IEEE INFOCOM, 2014.   
[13] R. Gao, Y. Tian, F. Ye, G. Luo, K. Bian, Y. Wang, T. Wang, and X. Li, “Sextant: Towards ubiquitous indoor localization service by photo-taking of the environment,” IEEE Transactions on Mobile Computing, vol. 15, no. 2, pp. 460–474, 2016.   
[14] Y. Shu, C. Bo, G. Shen, C. Zhao, L. Li, and F. Zhao, “Magicol: Indoor localization using pervasive magnetic field and opportunistic wifi sensing,” IEEE Journal on Selected Areas in Communications, vol. 33, no. 7, pp. 1443–1457, 2015.   
[15] H. Wu, Z. Mo, J. Tan, S. He, and S.-H. G. Chan, “Efficient indoor localization based on geomagnetism,” ACM Trans. Sen. Netw., vol. 15, no. 4, pp. 42:1–42:25, 2019.

[16] G. Bradski and A. Kaehler, Learning OpenCV: Computer vision with the OpenCV library. ” O’Reilly Media, Inc.”, 2008.   
[17] R. Smith, “An overview of the tesseract ocr engine,” in Proceedings of ICDAR, 2007.   
[18] R. Jain, R. Kasturi, and B. G. Schunck, Machine Vision. McGraw-Hill, 1995.   
[19] P. Zhou, M. Li, and G. Shen, “Use it free: instantly knowing your phone attitude,” in Proceedings of ACM MobiCom, 2014.   
[20] N. Roy, H. Wang, and R. Roy Choudhury, “I am a smartphone and i can tell my user’s walking direction,” in Proceedings of ACM MobiSys, 2014.   
[21] S. Pertuz, D. Puig, and M. A. Garcia, “Analysis of focus measure operators for shape-from-focus,” Pattern Recognition, vol. 46, no. 5, pp. 1415–1432, 2013.   
[22] V. I. Levenshtein, “Binary codes capable of correcting deletions, insertions and reversals,” in Soviet Physics Doklady, 1966.   
[23] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: wireless indoor localization with little human intervention,” in Proceedings of ACM MobiCom, 2012.   
[24] A. T. Mariakakis, S. Sen, J. Lee, and K.-H. Kim, “Sail: Single access point-based indoor localization,” in Proceedings of ACM MobiSys, 2014.   
[25] J. Dong, Y. Xiao, M. Noreikis, Z. Ou, and A. Yla-J ¨ a¨aski, “imoon: Using ¨ smartphones for image-based indoor navigation,” in Proceedings of ACM Sensys, 2015.   
[26] Y. Shu, K. G. Shin, T. He, and J. Chen, “Last-mile navigation using smartphones,” in Proceedings of ACM MobiCom, 2015.   
[27] Google, “Battery historian,” https://github.com/google/battery-historian, 18-Aug-2020.   
[28] P. Bahl and V. N. Padmanabhan, “Radar: An in-building rf-based user location and tracking system,” in Proceedings of IEEE INFOCOM, 2000.   
[29] M. Youssef and A. Agrawala, “The horus wlan location determination system,” in Proceedings of ACM MobiSys, 2005.   
[30] Y.-C. Cheng, Y. Chawathe, A. LaMarca, and J. Krumm, “Accuracy characterization for metropolitan-scale wi-fi localization,” in Proceedings of ACM MobiSys, 2005.   
[31] S. Sen, B. Radunovic, R. R. Choudhury, and T. Minka, “You are facing the mona lisa: spot localization using phy layer information,” in Proceedings of ACM MobiSys, 2012.   
[32] I. Bisio, F. Lavagetto, A. Sciarrone, and S. Yiu, “A smart2 gaussian process approach for indoor localization with rssi fingerprints,” in 2017 IEEE International Conference on Communications (ICC), 2017.   
[33] A. Rai, K. K. Chintalapudi, V. N. Padmanabhan, and R. Sen, “Zee: zero-effort crowdsourcing for indoor localization,” in Proceedings of ACM MobiCom, 2012.   
[34] X. Tian, R. Shen, D. Liu, Y. Wen, and X. Wang, “Performance analysis of rss fingerprinting based indoor localization,” IEEE Transactions on Mobile Computing, vol. 16, no. 10, pp. 2847–2861, 2017.   
[35] P. Biswas, T.-C. Lian, T.-C. Wang, and Y. Ye, “Semidefinite programming based algorithms for sensor network localization,” ACM Transactions on Sensor Networks, vol. 2, no. 2, p. 188220, 2006.   
[36] K. Chintalapudi, A. Padmanabha Iyer, and V. N. Padmanabhan, “Indoor localization without the pain,” in Proceedings of ACM MobiCom, 2010.   
[37] S. Sen, R. R. Choudhury, and S. Nelakuditi, “Spinloc: Spin once to know your location,” in Proceedings of ACM HotMobile Workshop, 2012.   
[38] Z. Zhang, X. Zhou, W. Zhang, Y. Zhang, G. Wang, B. Y. Zhao, and H. Zheng, “I am the antenna: accurate outdoor ap location using smartphones,” in Proceedings of ACM MobiCom, 2011.   
[39] J. Xiong and K. Jamieson, “Arraytrack: A fine-grained indoor location system,” in Proceedings of NSDI, 2013.   
[40] S. Sen, J. Lee, K.-H. Kim, and P. Congdon, “Avoiding multipath to revive inbuilding wifi localization,” in Proceeding of ACM MobiSys, 2013.   
[41] S. Kumar, S. Gil, D. Katabi, and D. Rus, “Accurate indoor localization with zero start-up cost,” in Proceedings of ACM MobiCom, 2014.   
[42] M. Kotaru, K. Joshi, D. Bharadia, and S. Katti, “Spotfi: Decimeter level localization using wifi,” in Proceedings of the 2015 ACM Conference on Special Interest Group on Data Communication, 2015.   
[43] C. Zhang and X. Zhang, “Pulsar: Towards ubiquitous visible light localization,” in Proceedings of ACM MobiCom, 2017.   
[44] Y.-L. Wei, C.-J. Huang, H.-M. Tsai, and K. C.-J. Lin, “Celli: Indoor positioning using polarized sweeping light beams,” in Proceedings of ACM MobiSys, 2017.   
[45] R. Gao, M. Zhao, T. Ye, F. Ye, Y. Wang, K. Bian, T. Wang, and X. Li, “Jigsaw: Indoor floor plan reconstruction via mobile crowdsensing,” in Proceedings of ACM MobiCom, 2014.   
[46] W. Huang, Y. Xiong, X.-Y. Li, H. Lin, X. Mao, P. Yang, and Y. Liu, “Shake and walk: Acoustic direction finding and fine-grained indoor

localization using smartphones,” in Proceedings of IEEE INFOCOM, 2014. [47] K. Liu, X. Liu, and X. Li, “Guoguo: Enabling fine-grained indoor localization via smartphone,” in Proceeding of ACM MobiSys, 2013.

![](images/b4e4692498dd4b4d8697346ca622168c25721d2b9e2f2f7b63a05de6e22cd232.jpg)



Manni Liu received the BE degree in the Department of Mathematics and Applied Mathematics at Sun Yat-sen University. She is currently pursuing a Ph.D. degree in Computer Science and Engineering at Michigan State University. Her research interests include Internet of Things, mobile computing and indoor localization.

![](images/aefac9ef1794898b23461f1c583a6124a0303dd6a6842fbbeac5cd4445800aea.jpg)



Jialuo Du received the BE degree in Computer Science and Technology from Tsinghua University. He is currently pursuing a Ph.D. degree in School of Software from Tsinghua University. His research interests include Internet of Things and mobile computing.

![](images/f74c8917eba9edc6d168e6a2a84da016e41778cdf7f87e04c3b950d408e23e62.jpg)



Qing Zhou received the BE degree from Huazhong University of science and technology and ME degree from Tsinghua University. He is currently working for Alibaba in the industry.

![](images/58f63f39231f88debed9e70931d78c9f96ff0410623b2bd4fbb6c17ebdba26eb.jpg)



Zhichao Cao Zhichao Cao received the BE degree in the Department of Computer Science and Technology at Tsinghua University, and his Ph.D. degree in the Department of Computer Science and Engineering at Hong Kong University of Science and Technology. He worked as an assistant professor in the School of Software, Tsinghua University. He is currently with Department of Computer Science and Engineering, Michigan State University. His research interests include IoT system, mobile and edge computing. He is a member of the IEEE.

![](images/ff1729a9e4ef1f6f7918a7628de928db80560aaf54e761d118f8348b27c4aa85.jpg)



Yunhao Liu Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is with the Department of Computer Science and Engineering in Michigan State University, and holds the Chang Jiang professorship in Tsinghua University. He is a fellow of the IEEE and ACM.