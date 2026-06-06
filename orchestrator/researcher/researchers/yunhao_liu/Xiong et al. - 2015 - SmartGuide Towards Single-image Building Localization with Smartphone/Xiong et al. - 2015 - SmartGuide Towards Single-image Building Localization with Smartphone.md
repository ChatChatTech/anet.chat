# SmartGuide: Towards Single-image Building Localization with Smartphone

Xi Xiong

School of Software and TNList

Tsinghua University, China

xiongxi08@gmail.com

Yun Fei

Department of Computer

Science

Columbia University, New York

fyun@acm.org

Zheng Yang

School of Software and TNList

Tsinghua University, China

hmilyyz@gmail.com

Milos Stojmenovic

Department of Informatics and

Computing

Singidunum University, Serbia

mstojmenovic@singidun-

um.ac.rs

Longfei Shangguan

CSE, Hong Kong University of

Science and Technology

Hong Kong

lshangguan@cse.ust.hk

Yunhao Liu

School of Software and TNList

Tsinghua University, China

yunhao@greenorbs.com

# ABSTRACT

We introduce SmartGuide, a light-weighted and efficient approach to localize and recognize a distant unknown building. Our approach relies on shooting only a single photo of a target building via a smartphone and a local 2D Google map. SmartGuide first extracts a partial top view contour of a building from its side-view photo by applying vanishing point and the Manhattan World Assumption, and then fetches a candidate building set from a local 2D Google map based on smartphone’s GPS readings. Partial top view shape, orientation and distance relative to the camera are used as input parameters in a probability model, which adversely recognizes the best candidate building in the local map. Our model is developed based on kernel density estimation that helps reduce noise in the smartphone sensors, such as GPS readings and camera ray direction reported by noisy accelerometer and compass. Experimental results demonstrate that our approach recognizes buildings ranging from 20m to 520m and achieves 92.7% accuracy in downtown areas where the Manhattan World Assumption is applicable. In addition, the processing time is no more than 6 seconds for 87% of cases. Compared with existing building localization schemes, SmartGuide offers numerous advantages. Our method avoids taking multiple photos, intricate 3D reconstruction or any initial deployment cost of database construction, making it faster and less labor-intensive than existing solutions.

# Categories and Subject Descriptors

H.3.4 [Information Storage and Retrieval]: Systems and Software

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from Permissions@acm.org.

MobiHoc’15, June 22–25, 2015, Hangzhou, China.

Copyright 
c 2015 ACM 978-1-4503-3489-1/15/06 ...\$15.00.

http://dx.doi.org/10.1145/2746285.2746294.

# General Terms

Algorithms, Design, Experimentation, Performance, Ubiquitous Computing

# Keywords

Building Localization; Smartphone; Mobile Computing; Single Image

# 1. INTRODUCTION

In many cases, a mobile user may be interested in identifying and locating a remote building that appears in the viewfinder of his/her smartphone when s/he wants to know which building it is, how to arrive at the building, or what kinds of merchants (e.g., stores, restaurants, and companies) are located in the building. For instance, Bob is travelling in New York City, a metropolis famous for its grand architecture. Bob can easily recognize famous landmarks such as the Empire State Building or Freedom Tower. However, he also wants to know details about some attractive but less well-known buildings within his sight. These buildings of interest may be located in a distance very far from Bob, and Bob could resort to some non-technical solutions, such as asking local residents or searching a city map. However, such approaches have various disadvantages. The building information provided by local residents may be insufficient or inaccurate. Besides, the city map is sometimes unavailable or outdated. Moreover, Bob has to identify the specific building of interest from a massive crowd buildings in a city map, which can be troublesome or even annoying.

Object localization has recently received extensive research efforts in the community of mobile computing. Several approaches to this problem have been proposed. One solution is to take several pictures of the target object and calculate physical depth of the building from the camera [10, 21], which is sometimes cumbersome. For instance, OPS [10] requires a user to shoot an object from multiple distinct positions and reconstructs a 3D model of the object to estimate the distance between the user and the object. Nevertheless, it is more user-friendly for the user to take only a single photo to localize a target. However, a pre-available image database [14, 17, 23, 31], or prior knowledge of the target’s true size [20, 26] are often required. For example, a queried image is matched against the GPS-tagged image data to find its accurate GPS location, which requires a prepared tree-indexing database [31].

Nevertheless, there are some disadvantages existing in those solutions when it comes to building localization. Taking multiple photos of the target may be troublesome; constructing the spatial relationship between objects could introduce significant computational cost and corresponsive delay; deploying an indexed database of building photos is laborintensive; knowing the true size of the target building in advance can be impractical.

To address the problems mentioned above, we propose SmartGuide: a fast light-weighted single-image-based building localization system based on the Manhattan World Assumption. Our solution enables a user to localize and recognize a distant unknown building, using only one photo of a target building and a local 2D Google map, without any other prior knowledge. Compared with previous imagebased object detection and localization schemes, our solution avoids intricate 3D reconstruction and any initial deployment cost of database construction, which makes it much faster. It can also handle noisy sensor data because our probability model is based on kernel density estimation. Its processing time is no more than 6 seconds for 87% cases. While it is viable to adopt object localization method [10] to localize the target building, 30-60 seconds are required for 3D reconstruction. Additionally, experiments show our system can localize the farmost building at a distance of 520m, which is more than twice longer distance than other database-free methods [10, 21, 26].

The main point of this paper is to extract the partial top view contour of a targeted building from a single captured photo, and use a probability model to match it to a building in a local online maps (2D Google Maps in this paper) obtained by smartphone’s GPS. The 2D local map contains not only the top view of the target building but also other surrounding building top views. Thus, we shall find an optimal matching of partial top view contour in the local map along with the camera ray direction, which can be obtained by fusing sensor data of smartphone. Our system responds quickly using off-the-shelf smartphones.

This design leaves out the trouble of taking multiple photos of a building and the high computational cost caused by 3D reconstruction, as well as any initial deployment cost of database construction. Nevertheless, to implement it one must overcome several challenges. (1) Single image of a building provides some structural information but not enough details for us to reconstruct the partial top view of the building. Moreover, existing techniques on 3D reconstruction [5, 15, 18] cannot provide the acceptable performance in terms of accuracy and computational cost. (2) Even after we have acquired the building’s partial top view, there may exist many other buildings that own similar partial top view contours with the building of interest in the map. How to distinguish the targeted building from other similar buildings remains an important issue. (3) The smartphone sensors, such as GPS, accelerometer, compass, and gyroscope, are themselves noisy, which can further decrease the accuracy of recognition.

For the first issue, SmartGuide leverages the Manhattan World Assumption [3] and vanishing points to generate a partial top view using only a single photograph. The Manhattan World Assumption assumes that the majority of man-made buildings share a common characteristic: all edges of buildings and windows lie in three orthogonal directions. Utilizing this very reasonable assumption, we can extract the partial top view of a target building much more efficiently than by using 3D-based methods while still maintaining the required accuracy. The extracted partial top view contour not only shows a partial overlooked shape of the building, but also contains the building’s orientation relative to the camera. Different buildings do not only own different top view contour shapes, but also own different orientations and different distances from the camera (which can be calculated from the camera parameters and the real sizes of the buildings obtained from the map). Therefore, leveraging these features helps a lot in distinguishing the target building from other similar buildings, which solves the second issue. Lastly, we prepare a probability model based on kernel density estimation (KDE) [13] for the noisy sensor data.

We prototyped SmartGuide on Android smartphones, including LG Nexus 5, Samsung Galaxy Tab 10.1, and Samsung i9100, to collect building photos of different resolutions and qualities. Over fifty locations across four cities (Beijing, Wuxi, Hong Kong, and Shanghai) were evaluated in total. Under the Manhattan World Assumption, all photos are captured from the downtown area or universities where the shape of most buildings are constructed by straight line segments (see our examples below). The experimental results demonstrate that the systems can identify and locate buildings from 20m to 520m and achieve 92.7% identification accuracy in downtown areas where the Manhattan World Assumption is applicable. SmartGuide costs no more than 6 seconds for 87% cases and less than 9 seconds for all cases.

The key contributions of SmartGuide are summarized as follows.

1. Identified the possibility of localizing a remote building via top view feature matching. By analyzing top view features (shape, orientation and distance from camera) of the candidate buildings and the target building, we tried to localize the target building from a set of candidate buildings. Our method avoided taking multiple photos, intricate 3D reconstruction or any initial deployment of image databases.

2. Introduced a kernel-based probability model to deal with the smartphone’s sensor noises. We took a scrutiny on the sensor data, handled it with rigid mathematical models and demonstrated the efficiency of our model.

3. Implemented a prototype of our system with evaluation. We prototyped SmartGuide and evaluated its performance in various settings. We demonstrated that our system worked in nearly real-time on off-the-shelf smartphones while also preserving or improving accuracy.

The rest of the paper is organized as follows. Section 2 describes the system overview and Section 3 provides preliminary techniques used in our systems. In Section 4, we dive into the design details. The prototype implementation and performance are evaluated in Section 5. We review the related work in Section 6 and conclude this work in Section 7.

![](images/c543b485180d1cf03bc5e611d0aef28de7aac333e7edbec0eb5b120308f63faa.jpg)



Figure 1: The pipeline of our system. Directions of the arrows indicate the latter consumes result from the former

# 2. SYSTEM OVERVIEW

In this section, we introduce the basic components of SmartGuide and their work-flow. Fig. 1 portrays an overview of SmartGuide’s architecture.

Once the user captures a photo of a target building with a smartphone, SmartGuide records the GPS of the smartphone and calculates the camera ray direction at the same time. SmartGuide detects line segments and classifies these line segments into three orthogonal directions to estimate three vanishing points. According to the positions of three vanishing points, intrinsic camera parameters are calibrated to transform the coordinates of points in 2D photo into the 3D world space. After that, we extract the line segments on the top of the target building and project them onto the ground plane to get the partial top view of the target building.

Simultaneously, SmartGuide fetches a local map via online map services according to the GPS reading. The buildings in the local map compose a candidate building set which contains the target building, and their partial top views are also extracted. Since these buildings present different partial top view shapes, different orientations relative to camera, and different distances from the camera, we evaluate these three features of candidate buildings according to the partial top view, orientation, and size in photo of the target building. At last, we establish a probability model based on kernel density estimation (KDE), whose parameters are calculated according to the above three features, to identify the target building from a number of candidates.

# 3. PRELIMINARIES

We briefly review some techniques behind our system, and clarify their necessity for our purpose in this section.

Pinhole Camera: We use the classical Pinhole Camera model to simplify the process for acquiring the camera parameters [27]. In this model, 3D points in the real world and their projected points in the image plane construct an ideal pinhole camera, where its aperture is described as a point and no lenses are used for focusing light. In this way, we can ignore geometric distortions and unfocused blurring caused by lenses and finite sized apertures. In the pinhole camera model, all lines that are parallel in reality, such as edges of buildings and windows, are projected to a group of straight lines that converge to vanishing points in a image plane, which are crucial for us to extract the partial top view from a single image. Based on this model, we can achieve the focal length, the size and center of the image plane from the smartphone’s camera parameters, which are essential factors for building identification.

Manhattan World Assumption: Most man-made scenes follow the Manhattan World Assumption [3], where Cartesian coordinate system is used as a Manhattan grid. All lines in a photo image are assumed parallel to three directions. The lines in one direction are extrapolated to converge to a vanishing point. Accordingly, we can categorize all lines (corresponding to edges of buildings and windows) appearing in the image into three perpendicular directions. Hence the top view contour can be extracted from the categorized lines from a single image.

Kernel Density Estimation (KDE): Let $x _ { 1 } , x _ { 2 } , . . . , x _ { n }$ be independent and identically distributed samples drawn from some distribution with an unknown density function. We can estimate the unknown density function by kernel density estimation (KDE) as following [13]:

$$
\hat {f} (x, h) = \frac {1}{n h} \sum_ {i = 1} ^ {n} K _ {i} (\frac {x - x _ {i}}{h}). \tag {1}
$$

$K _ { i } \big ( \frac { x - x _ { i } } { h } \big )$ is the kernel function of the sample $x _ { i } ,$ a nonnegative function that integrates to one and has mean zero, where h is a smoothing parameter called bandwidth. Fundamentally, KDE is a data smoothing method used to infer data probability distribution based on finite data samples. Since the shooting position is unknown because of noisy GPS readings, the KDE is a powerful tool for us to estimate probability distribution of the shooting position given a finite set of candidate buildings in a 2D local map.

Hu’s Seven Moment Invariants: Moment theory is well established and widely applied in a number of digital image areas because image moments are important statistical properties of an image. The raw image moment is a weighted average of pixels’ intensities in the image, usually defined as

$$
M _ {i j} = \sum_ {x} \sum_ {y} x ^ {i} y ^ {j} I (x, y), \tag {2}
$$

where $I ( x , y )$ is the pixel intensity at $( x , y )$ .

Hu et al. [7] proved theoretically that an image can be summarized with seven functions that are various combinations of the raw moments $M _ { i j }$ . Furthermore, these seven functions are invariant under translation, scaling, as well as rotation, which makes them appropriate for comparing the similarity between different shapes [8].

# 4. SYSTEM DESIGN

SmartGuide consists of four components: (1) partial top view extraction from a single image, (2) candidate building set acquisition, (3) candidate building feature selection, (4) building identification. In this section, we detail the design challenges and implementations of each module.

![](images/33e5550d24e095dd2159ab2016d8a120062e13767c959f2d8e14b344991137ee.jpg)  
Figure 2: The intermediate results corresponding to each step of the pipeline: a) the captured image of a target building; b) the extracted line segments; c) the partial top view contour before angle adjusting; d) the final extracted partial top view contour; e) the local map provided by online maps service, whose center corresponds to GPS readings of smartphone; f) the colormapped probability model based on KDE, presenting the probability distribution of estimated shooting position; g) the corresponding 3D view of the probability model based on KDE.

# 4.1 Partial Top View Extraction from a Single Image

On online maps, buildings are typically drawn in line segments of their top views. Therefore, matching buildings can be converted to the matching building’s top view contours. However, in practice, users seldom take a photo from the top of a building, instead they take photos of the facades of a building. Hence, a critical problem is how to extract the top view contour from a side-view photo. We propose a novel approach in which one single image suffices to enable user-friendly and power-saving partial top view extraction on smartphones. These benefits come from the following observations in practical circumstances.

Vanishing Point Estimation: Since we are using the Manhattan World Assumption, we need to estimate the positions of three vanishing points before the contour extraction. Our method refers to a state-of-the-art technique proposed by Nieto and Salgado [11]. After obtaining three vanishing points, we group the input line segments based on their orientation towards three vanishing points. As a result, we can infer the geometrical relationships of these line segments. This is crucial for the following steps.

Estimation of the Smartphone Camera Parameters: We construct a camera matrix K that contains intrinsic and extrinsic camera parameters [5]. In this step we leave out skew parameters caused by the perspective transform.

Given the three vanishing points, we can compute a matrix Q, which equals $K K ^ { T ^ { * } }$ [12], thus K can be computed from the Cholesky factorization of Q. The matrix K transforms a point from world space to perspective space. Hence, K−1 helps us convert the coordinate system of every 2D line in the perspective image space into world space.

Generating Top View Line Segments: In the context of SmartGuide, we introduce a simple and fast method for the extraction of partial top view contour. The rationale behind is twofold. Firstly, if a line segment is on the top view of a building, it must also lie on the upper part of the photo. Secondly, based on the Manhattan World Assumption, we know if one segment has directions different from its neighbor segments, the angles between them can only be $\pi / 2 ~ \mathrm { o r } ~ - \pi / 2$ . Based on these observations we design the algorithm as follows:

1. Line segments are extracted from the photo with Line Segment Detector [24].   
2. From the top of image, we find the highest segment of the building, using the first vertex as the root of the following procedures.   
3. From the root we search for the segments next to it. For a vertex, we extract all the segments within its neighborhood. If the number of segments are below some expected threshold, we expand our searching

area. We then store the found segments into two bins according to their inclination to the vanishing points.

4. One or two new segments are created from the segments in the bins: the direction of a new segment is the averaged direction of the segments in one bin, and the length of that new segment is the maximal length of the segments in that bin.   
5. The created segments are linked to the root. For each created segment, we treat its far end as the new root; repeat from Step 3 until no new segments are found around the root.

After this step, a linked-list of line segments is built. Then we demonstrate how to construct the partial top view contour from these selected line segments.

Each vertex in the linked-list and its two segment neighbors (or one for the last vertex) construct a hinge. From the Manhattan World Assumption we know the angle of each hinge can be either $\pi / 2 \ : \mathrm { o r } \ : - \pi / 2 ,$ , or 0. We use the following function to determine the angle ωi of each hinge made from the i-th and i + 1-th segments (the current angle is denoted as \$i):

$$
\omega_ {i} = \left\{ \begin{array}{l l} \pi / 2 & \text { if } v _ {i} \neq v _ {i + 1}, | \varpi_ {i} - \pi / 2 | <   | \varpi_ {i} + \pi / 2 | \\ - \pi / 2 & \text { if } v _ {i} \neq v _ {i + 1}, | \varpi_ {i} - \pi / 2 | \geq | \varpi_ {i} + \pi / 2 |, \\ 0 & \text { if } v _ {i} = v _ {i + 1} \end{array} \right. \tag {3}
$$

where vi is the vanishing point to which the i-the segment points. For each hinge adjustment we calculate its corresponding rotation matrix Ri. Then we apply them onto each line segment, i.e., for the i-th segments, its rotation matrix is computed as $\textstyle \prod _ { k = 0 } ^ { i } R _ { k , k + 1 }$ .

# 4.2 Candidate Building Set Acquisition

SmartGuide relies on online map services for building identification. In this section, we explain in detail how Smart-Guide acquires a candidate set of buildings from the commercial map service.

Local Map fetching: Once a user takes a photo of a target building, it automatically triggers the GPS to acquire the world coordinate of the user. Based on the world coordinate, SmartGuide fetches a Google Map image (containing the candidate buildings) where the user lies in the center via standard Google map API. Fig. 2e gives a concrete example of a Google map image.

Candidate Building Top View Detection: After downloading the static Google map, the next step is to extract the top view contour of each building on this static map. Here we adopt a state-of-the-art method [22] to extract the borders of each building on the map. Since the contours of most buildings on the map are geometric polygons, it is thus unnecessary to store all the coordinates along each straight line. Therefore we further apply the Ramer-Douglas-Peucker (RDP) algorithm [9] to remove redundant coordinates along a straight line. After this process, each contour is represented by a vector of corner points, which are arranged counter clockwise.

# 4.3 Candidate Building Features Selection

It is understandable that every building possesses a unique top view contour, orientation relative to the camera ray direction, and distance from the camera. Therefore, after acquiring the candidate building set from the Google Map image, the next step is to match the targeting building to its actual location by comparing top view contours, orientation, and distance from the camera.

![](images/c29e3980c0a93c3e375a9d9e7136d7055d6361cc850e09769a48a2ca354d6f4c.jpg)



Figure 3: Only the part of building top view that faces the camera ray direction can be captured in photo.

Camera Direction Vector: In the standard sensor coordinate system of a smartphone, X and Y axes lie in the plane of the surface of the device and the Z axis points toward the outside of the screen face, so that the vector of camera ray direction is (0, 0, −1). To obtain the camera direction in the world coordinate system (where X axis is tangential to the ground pointing East and Y axis is tangential to the ground pointing toward the geomagnetic North Pole), we need to learn the rotation matrix between the two coordinate systems. The rotation matrix can be inferred by fusing accelerometer and magnetometer data from the smartphone, which are used to find the orientation relative to the vector of gravity and the vector of north direction respectively. Given the rotation matrix R:

$$
R = \left[ \begin{array}{l l l} r _ {0 0} & r _ {0 1} & r _ {0 2} \\ r _ {1 0} & r _ {1 1} & r _ {1 2} \\ r _ {2 0} & r _ {2 1} & r _ {2 2} \end{array} \right], \tag {4}
$$

The camera ray direction in world coordinate system is calculated by $R ( \mathrm { \bar { 0 , } } 0 , - 1 ) ^ { T } = ( - r _ { 0 2 } , - r _ { 1 2 } , - r _ { 2 2 } ) ^ { T }$ . Thus vector $\vec { D } = \left( - r _ { 0 2 } , - r _ { 1 2 } \right)$ represents the camera ray direction projected onto a horizontal plane, where the X axis points to the East and the Y axis points to the North.

Partial Top View Shape Feature Evaluation: We have extracted the partial top view of the target building and full top views of the candidate buildings in the previous sections. In order to evaluate candidate buildings’ top view shapes, we should extract the part of candidate buildings’ top view contours that are facing the camera ray direction. Fig. 3 illustrates such a case where the camera shoots the building from the front and only covers partial corner points $\left. \mathbf { p } _ { 4 } , \mathbf { p } _ { 5 } , \mathbf { p } _ { 6 } , \mathbf { p } _ { 7 } , \mathbf { p } _ { 8 } \right.$ .

For convenience we define the direction of our contour to be counter-clockwise. To detect the line segments that face the camera, we first determine whether a line segment is inward or outward by using the outer product between the camera ray direction D\~ with the line segment: if the outer product between them is negative, they are in the opposite direction, otherwise they are in the same direction. Hence if the line segment is facing the camera we know the outer product between it and the camera direction should be negative.

More intuitively, in a sequence of segments which faces the camera, every segment should face the camera. Therefore, the outer product of camera ray direction $\vec { D }$ with the sequence of segments should be all negative. For instance, $\vec { D } \times \mathbf { p } _ { 2 } \mathbf { p } _ { 3 } < 0$ but $\vec { D } \times \mathbf { p } _ { 3 } \mathbf { p } _ { 4 } > 0$ , thus contour $\left. \mathbf { p } _ { 2 } , \mathbf { p } _ { 3 } , \mathbf { p } _ { 4 } \right.$ i is not all facing to the camera.

However, one building can own several different visible partial contours that face the camera. For instance, visible corner points $\left. \mathbf { p } _ { 4 } , \mathbf { p } _ { 5 } , \mathbf { p } _ { 6 } , \mathbf { p } _ { 7 } , \mathbf { p } _ { 8 } \right.$ can form 6 different contours, namely $\langle \mathbf { p } _ { 4 } , \mathbf { p } _ { 5 } , \mathbf { p } _ { 6 } \rangle , \langle \mathbf { p } _ { 5 } , \mathbf { p } _ { 6 } , \mathbf { p } _ { 7 } \rangle , \langle \mathbf { p } _ { 6 } , \mathbf { p } _ { 7 } , \mathbf { p } _ { 8 } \rangle , \langle \mathbf { p } _ { 4 } , \mathbf { p } _ { 5 } $ , ${ \bf p } _ { 6 } , { \bf p } _ { 7 } \rangle , \ \langle { \bf p } _ { 5 } , { \bf p } _ { 6 } , { \bf p } _ { 7 } , { \bf p } _ { 8 } \rangle$ , and $\left. \mathbf { p } _ { 4 } , \mathbf { p } _ { 5 } , \mathbf { p } _ { 6 } , \mathbf { p } _ { 7 } , \mathbf { p } _ { 8 } \right.$ . Therefore, we need to find the one whose shape is the most similar with the partial top view contour extracted from photo.

Shape comparison should not be affected by translation, scaling and rotation, thus we adopt the aforementioned Hu’s seven moment invariants and an empirical formulae to compare two contour shapes as following:

$$
I (A, B) = \sum_ {i = 1 \dots 7} | m _ {i} ^ {A} - m _ {i} ^ {B} |, \tag {5}
$$

where

$$
m _ {i} ^ {A} = \operatorname{sign} (h _ {i} ^ {A}) \cdot \log h _ {i} ^ {A}, m _ {i} ^ {B} = \operatorname{sign} (h _ {i} ^ {B}) \cdot \log h _ {i} ^ {B}, \tag {6}
$$

and $h _ { i } ^ { A } , h _ { i } ^ { B }$ are the Hu moment invariants of contour A and B. The more similar A and B are, the smaller $I ( A , B )$ is.

To conclude, we compare the shapes of all partial visible contours with the partial top view contours extracted from the photo, and assume that the most similar one, which owns the smallest difference, as actual part that have been captured into the camera. The specific details are presented in Algorithm 1. In other words, for a candidate building contour $C _ { i } ,$ we can get the best matching partial contour ${ \tilde { C } } _ { i }$ in the photo and take its corresponding shape matching score as the candidate building shape score $s _ { i } .$ . The better they match with each other, the lower $s _ { i }$ is.

Input: a candidate building contour $C _ { i } = \langle \mathbf { p } _ { 1 } , \mathbf { p } _ { 2 } , . . . , \mathbf { p } _ { a _ { i } } \rangle$ , target building contour $C ,$ and camera ray direction $\vec { B }$   
Output: partial visible contour $\tilde{C}_i$ , $s_i$ float $s_i =$ MAXVALUE;
for $m = 1; m \leq a_i; m++$ do
    if $\overrightarrow{D} \times \overrightarrow{\mathbf{p}_m \mathbf{p}_{m+1}} > 0$ then
    | continue;
    end
    for $n = 2; n < a_i; n++$ do
    if $\overrightarrow{D} \times \overrightarrow{\mathbf{p}_{(m+n-1)\%a_i} \mathbf{p}_{(m+n)\%a_i}} > 0$ then
    | break;
    end
    let $temptC = \langle \mathbf{p}_m, \mathbf{p}_{m+1}, ..., \mathbf{p}_{(m+n)\%a_i} \rangle$ ;
    if $I(\tilde{C}_i, C) < s_i$ then
    | $s_i = I(\tilde{C}_i, C)$ ;
    | $\tilde{C}_i = temptC$ ;
    end
    end
end

return ${ \tilde { C } } _ { i } , s _ { i } ;$

Algorithm 1: extractPartialVisibleContour

Building Orientation Feature Evaluation: Different buildings also own different orientations relative to the camera ray direction. Based on the camera ray direction and the positions of three vanishing points, which correspond to three orthogonal directions, from the photo, we can calculate the target building orientation in world coordinates. In addition, we can get each candidate building orientation from the Google Map. Therefore the orientation error $\delta _ { i }$ between the i-th candidate building orientation and the target building orientation can be obtained.

Building Depth Feature: Given the camera parameters such as focal length $F$ and CCD width $W _ { c c d } ,$ physical building size $c _ { m }$ in meters computed from the map, and building size $c _ { p }$ in pixels in photo, we can estimate the averaged camera-to-building distance as following:

$$
d = \frac {F W _ {p}}{W _ {c c d}} \cdot \frac {c _ {m}}{c _ {p}}, \tag {7}
$$

where $W _ { p }$ is the width of the photo.

Therefore, given the location of candidate building on the map, the distance from camera to candidate building and the camera ray direction, we can infer the estimated shooting position (ESP) $\mathbf { e } _ { i }$ of i-th candidate building.

# 4.4 Building Identification

Probability Model based on KDE: From the previous steps, we have obtained the shape matching score $s _ { i } ,$ the building orientation error $\delta _ { i } ,$ and an estimated shooting position (ESP) $\mathbf { e } _ { i }$ for the i-th candidate building. Given shooting position o estimated by GPS, a naive method is directly taking the i-th candidate building which owns the smallest distance from $\mathbf { e } _ { i }$ to o as the target building. However, we know that o may not be accurate since there can be significant error in the GPS data. Moreover, since smartphone sensors are noisy, the camera ray direction inferred by accelerometer and magnetometer data also has random errors, which results in an inaccurate $\mathbf { e } _ { i }$ . In addition, the naive method does not take the shape matching score and the building orientation error into consideration. Hence, the result from this direct method can be problematic and unstable.

Since we do not know which building is captured in the photo, as well as the exact shooting position, we propose the probability distribution of the shooting position as the joint probability distribution of the probability distribution of all candidate buildings’ shooting positions and the probability distribution of the GPS coordinate. First, we model the distribution of the i-th candidate building’s shooting position as a normal distribution. The probability density function (PDF) at each pixel x is:

$$
f _ {i} (\mathbf {x}) = \frac {1}{\sqrt {2 \pi} \sigma_ {i}} e ^ {- \frac {\| \mathbf {x} - \mathbf {e} _ {i} \| ^ {2}}{2 \sigma_ {i} ^ {2}}}, \tag {8}
$$

where $\mathbf { e } _ { i }$ is the ESP of i-th candidate building, $\sigma _ { i }$ is the standard deviation of the ESP, and $\| \cdot \|$ is the 2-norm distance.

The $\sigma _ { i }$ depends on the shape matching score $s _ { i }$ and the candidate building’s orientation error $\delta _ { i }$ . We observe that the higher $s _ { i }$ is and the higher $\delta _ { i }$ is, the less possible the shooting position of i-th building concentrates on $\mathbf { e } _ { i }$ . Hence we model $\sigma _ { i }$ proportional to $s _ { i }$ . However, how to evaluate the candidate building’s orientation error δi remains another issue.

The candidate building’s orientation error $\delta _ { i }$ is introduced by two parts: the actual orientation deviation between i-th candidate building’s orientation and the target building’s orientation; the camera ray direction error caused by noisy smartphone’s sensor data. To evaluate camera ray direction error, we captured photos of different buildings at different locations, and recorded the computed camera ray directions multiple times. Compared with the true direction, we observe that the distribution of the camera ray direction error follows a homogeneous normal distribution. Hence we compute a score $\alpha _ { i }$ for the direction error as

![](images/221d6e986344a3c1b76f809c5d7f01f900dbb7134486b0b35d8f006515a5c21b.jpg)



Figure 4: Partial Top View Extraction

$$
\alpha_ {i} = e ^ {- \frac {\delta_ {i} ^ {2}}{\sigma^ {2} \delta}}, \tag {9}
$$

where $\sigma _ { \delta }$ is the standard deviation of camera ray direction. The less the orientation error $\delta _ { i }$ is, the higher the score $\alpha _ { i }$ is.

Therefore, we define $\sigma _ { i }$ is proportional to shape matching score $s _ { i }$ and inversely proportional to building orientation error score αi:

$$
\sigma_ {i} = \frac {\epsilon s _ {i}}{\alpha_ {i}}. \tag {10}
$$

where  is a constant scaling coefficient.

Since the probability distributions of every candidate building’s shooting position are mutually independent, the total probability density function (PDF) ˆf can be estimated by using kernel density estimation (KDE), as following:

$$
\hat {f} (\mathbf {x}) = \frac {1}{n} \sum_ {i} ^ {n} f _ {i} (\mathbf {x}) \tag {11}
$$

There is another issue we should take into consideration: we have the GPS of smartphone, however, the distribution of GPS location is not perfectly Gaussian since it is determined by the shape and acceleration of satellites, as well as the atmosphere turbulence. Fortunately, its error can be estimated and bounded by a Gaussian distribution [6, 16]. In this way, the final probability distribution of the shooting position is the joint distribution of 1) the distribution of all candidate buildings’ shooting positions, and 2) the distribution of GPS. Therefore, we modulate $\hat { f } ( \mathbf { x } )$ with a Gaussian distribution whose center is located at the captured GPS location:

$$
\begin{array}{l} \hat {f} _ {f i n a l} (\mathbf {x}) = \frac {1}{\sqrt {2 \pi} \epsilon_ {G}} e ^ {- \frac {\| \mathbf {x} - \mathbf {o} \| ^ {2}}{2 \epsilon_ {G} ^ {2}}} \hat {f} (\mathbf {x}) \\ = \frac {1}{n \sqrt {2 \pi} \epsilon_ {G}} e ^ {- \frac {\| \mathbf {x} - \mathbf {o} \| ^ {2}}{2 \epsilon_ {G} ^ {2}}} \sum_ {i} ^ {n} \frac {\alpha_ {i}}{\sqrt {2 \pi} s _ {i} \epsilon} e ^ {- \frac {\alpha_ {i} ^ {2} \| \mathbf {x} - \mathbf {e} _ {i} \| ^ {2}}{2 \epsilon_ {i} ^ {2} \epsilon^ {2}}}, \tag {12} \\ \end{array}
$$

with GPS’s standard deviation denoted as $\epsilon _ { G }$

According to Eqn. 12, we treat the location x which owns the highest ${ \hat { f } } _ { f i n a l } ( \mathbf { x } )$ as the most possible shooting position. Since we have obtained the shooting position and probability distribution of every candidate building’s shooting position, the candidate building, whose probability distribution of shooting position contributes most probability value in Eqn. 11, is identified as the target building in photo.

# 5. SYSTEM EVALUATION

In this section, we present the experimental evaluation of SmartGuide from several aspects. First, we will introduce its implementation details.

# 5.1 Implementation

All the functional components of SmartGuide are implemented on the Android platform (version 4.4). We evaluate its performance on an LG Nexus5 with a 2.3GHz CPU and 2GB RAM. Nearly 9k lines of Java implementation is involved in the functional structure (Fig. 1). We adopt OpenCV for Android SDK (version 2.4.9) [1] to implement the contour detection and calculate Hu’s invariant moments to match the top view shapes. Since we can expect the phone to be roughly static when the user is capturing photos, we use the immediate sensor output before the capturing to calculate the camera ray direction and GPS location.

To demonstrate the ubiquity of SmartGuide, over fifty locations across four cities (Beijing, Wuxi, Hong Kong, and Shanghai) were evaluated in total and the shooting distance spans from 20m to 520m. Moreover, we adopt various smartphones, including LG Nexus5, Samsung Galaxy Tab 10.1 and Samsung i9100, to collect building photos of different resolutions and qualities.

# 5.2 Evaluation

In the following, we first show the results of partial top view extraction with different buildings as input, and then verify the Gaussian distribution of the camera ray direction. Then we measure the overall identification accuracy and the time delay of SmartGuide.

Partial Top View Contour Extraction: Fig. 4 presents the results of partial top view extraction, whose inputs are four different buildings. The first three photos are captured in some downtown areas at a relatively remote distance ≈ 300 meters and the last photo is captured in a campus at close distance. For better presentation we also show their corresponding locations (marked by red rectangles) on the Google Map. The four buildings own different shapes and orientations (relative to the camera), which can be revealed in our results of partial top view extraction. Even though there are some trees or other buildings occluding the target building in the photo, our algorithm can still extract the correct partial top view contour of the building.

Camera Ray Direction PDF: To demonstrate that the probability distribution of the camera ray direction follows Gaussian distribution, we collected the camera ray direction data at different locations multiple times. The histogram of camera ray direction in Fig. 5 approximates the Gaussian distribution shape. Fig. 6 displays a quantile-quantile plot of the sample quantiles of camera ray direction versus theoretical quantiles from a normal distribution. If the distribution of camera ray direction is normal, the plot will be close to linear.

Accuracy of Building Identification: We tested Smart-Guide at more than 50 locations across four cities. The closest and the farmost buildings we can identify are 20m away and 520m away respectively. The farmost distance of previous works on object localization without leveraging prepared image database is no more than 250m [10, 21]. This distance range is caused by two reasons. First, if the distance is too short, it is hard to include a whole building into one photo, which hinders the partial top view extraction. Also it is usually unnecessary to identify a building which is very close to the user’s location. Next, the further the building, the less clear the photo is. When the image is blurry, the detection of line segments may be incorrect, which results in distorted top view extraction and exceptions in building identification.

The SmartGuide can achieve 92.7% accuracy in downtown areas where the Manhattan World Assumption is applicable. To evaluate SmartGuide’s performance with varied photo qualities, we downsample full-resolution photos to different levels of resolution. Fig. 7 shows the accuracy of identification suffers when the levels of resolution are below 640×480. Moreover, we compare the accuracy of SmartGuide with the method that does not apply our probability model based on KDE but only the i-th candidate building which owns the smallest distance from the estimated shooting position ei to the GPS measurement o as the target building. Fig. 7 demonstrates that the latter method performs much worse than SmartGuide.

In Fig. 8 we analyze SmartGuide’s accuracy based on different distances of the buildings from the shooting place. The target buildings within 100 meters are all correctly mapped. Two buildings within 100-300 meters and two buildings within 300-500 meters are wrongly identified. Thus we can infer that near buildings are more likely to be identified correctly than remote buildings due to their higher sharpness and smaller candidate building set.

Time Delay: We analyze the time cost of three functional components: partial top view extraction from a single photo, feature selection of candidate buildings and building identification. We leave out the time cost of candidate building set acquisition since Google Map API limits the maximal map size to be 30KB, so that we can download the local google map synchronously while extracting target building top view to reduce the time cost.The time cost of partial top view extraction is influenced by the photo resolution. Since using 640 × 480 resolution can achieve the same performance as higher resolution, thus we resize every photo into 640 × 480 for the evaluation.

In the building identification phase, we use an image with the same size as the map to represent the final PDF. For each pixel we fill it with a probability value according to its world-space location. A naive solution to compute ${ \hat { f } } _ { f i n a l } ( \mathbf { x } )$ is gathering the PDF values computed from each building for each location x on the map, which can be very inefficient. However, we notice the probability where x is far from $\mathbf { e } _ { i }$ is extremely low in practice. Hence we may approximate the result by ignoring the locations where $\| \mathbf { e } _ { i } - \mathbf { x } \| > r$ . In this way the performance can be largely improved since we only need to consider a small neighborhood around $\mathbf { e } _ { i }$ .

We ran SmartGuide 70 times and compare the time cost of different functional components in Fig. 9. It can be seen that the phase for partial top view extraction is the major factor influencing the total time consumption. The variation of the time cost for partial top view extraction is caused by the various line segment numbers detected in different photos. Besides, the time cost for feature selection is stable, and is small enough to be ignored. Furthermore, the time spent on location mapping is affected by the densities of buildings in the map. More buildings in a map take more time to calculate the probability distributions of candidate buildings’ shooting positions.

Fig. 10 presents the cumulative distribution function of total time cost. It takes at most 9 seconds for SmartGuide to calculate the target building location after taking the photo, and in 87% cases it takes no more than 6 seconds to get the result. By providing this interactivity, SmartGuide is rather efficient compared with the most relevant previous image-based localization method, which requires 30 ∼ 60 seconds [10].

# 6. RELATED WORK

In this section, we broadly review two categories of research directly related to our work.

Image based localization: Many recent works leverage computer vision techniques (e.g., STERO and SfM) for object localization [4, 17, 10, 23, 31]. Sattler et al. [17] proposed an 2D-3D matching method for object localization. Such method relies on multiple photos of the targeting object with various shooting angles. In [23], Laere et al. used SIFT features to match a query image against a set of reference images with known GPS coordinates. In [20, 26], the true size of the target is needed to localize the remote target. OPS [10] is the most relevant work to us. It requires a user to shoot an object from multiple distinct views and then uses SfM technique to reconstruct the 3D model of this object on the cloud end. After the 3D reconstruction, the distance between the user and this object will be returned to the user end, based on which the user could locate the geo-location of this object. Different from this method, SmartGuide requires the user to shoot the target only once and can immediately know its exact location and semantic information without a prepared image database or knowledge of the size of the target.

![](images/845eb212726b191450e0d540216d49e9eaca8437d3c1dd051162748d66519f51.jpg)



Figure 5: Camera Ray Direction PDF   
![](images/26f365b5e071c3179c509774fa501a6a897d84672befd50c7245ad87c9d53313.jpg)



Figure 6: QQ-plot

![](images/80f7266b4432990251e6a9a49a24a053bb1e287a17aecd19349b1a09210d28ad.jpg)



Figure 7: Accuracy of Building Identification

![](images/975d145c528164d4b0f8ebf6df992de361db8a51b3748f5d629a89539478fb19.jpg)



Figure 9: Time Cost of Func-Figure 8: Accuracy vs. Distancetional Components

![](images/90df6d02e9ad130a361a423d33444813027e11b5a57b208b90a070b742382ff5.jpg)



![](images/91f30e30d3a1faa5c42bcebc82c3d80680e1eb3ebe2ef48f60f9034fb4980258.jpg)



Figure 10: CDF of Time Cost

Smartphone based localization: Recent advances in embedding sensors of smarthpones open new research opportunities for pervasive localization services [2, 19, 25, 28, 29, 30]. WILL [28] designed an indoor localization technique which leverages user mobility and WiFi signal profiles for room-level human localization. UnLoc [25] proposed an sensor-fusion based localization technique which localizes/tracks the user’s location/trace while avoiding wardriving or fingerprints. Sen et al. [19] explored the frequency diversity of WiFi signals to characterize the fine-grained location of the user in an indoor environment. Escort [2] obtains cues from social encounters and leverages an audio beacon to guide the user to find a desired person. These systems mainly focus on how to identify the people’s location, with the help of existing infrastructure such as WiFi access points and GSM towers. While our work addresses localizing the remote building with a smartphone in quick and responsive manner, which tackles with another branch of localization issues.

View Extraction from Single Image: The methods that reconstruct a specific view from a single photo have been widely studied. A branch of these methods use deep learning. Markov random field, trained via supervised learning, is used to infer the 3D location and 3D orientation of every patch [18]. Another branch closer to our method use vanishing points, orthogonal structure and linear programming to reconstruct the 3D arrangement of lines extracted from a single image [15]. However, previous methods either require a large database for deep learning, or demand for high computational costs, which are not quite suitable in our scenario.

# 7. CONCLUSION

In this paper, we introduced SmartGuide, a fast system for accurate building localization with smartphones. We experimented on using a single image to locate the building in the map without any prior knowledge, which provided promising results for future research. It still has several limitations: it inherits the limitations of other works based on the Manhattan World Assumption, and for very complicated building structures, it can hardly recover the partial top view accurately, which can significantly decrease the efficiency of our algorithm. However, as 3D online maps services become increasingly mature, the height of a building also can be take into consideration to improve localization accuracy, which can be an attractive research direction.

# 8. ACKNOWLEDGEMENTS

We would like to thank the anonymous reviewers for providing valuable comments. This work is supported in part by the NSFC Major Program 61190110, NSFC under Grant 61171067, 61332004, 61303209, NSFC Distinguished Young Scholars Program under Grant 61125202, and Beijing Nova Program.

# 9. REFERENCES

[1] Developers Android. Opencv, 2014. http://opencv.org/platforms/android.html.   
[2] Ionut Constandache, Xuan Bao, Martin Azizyan, and Romit Roy Choudhury. Did you see bob?: human localization using mobile phones. In Proceedings of the MobiCom 2010, pages 149–160, 2010.   
[3] James M Coughlan and Alan L Yuille. Manhattan world: Compass direction from a single image by bayesian inference. In Proceedings of the ICCV 1999, volume 2, pages 941–947, 1999.   
[4] Gerald Friedland, Jaeyoung Choi, Howard Lei, and Adam Janin. Multimodal location estimation on flickr

videos. In Proceedings of SIGMM 2011, pages 23–28, 2011.   
[5] Richard Hartley and Andrew Zisserman. Multiple view geometry in computer vision. Cambridge university press, 2003.   
[6] Jeffrey Hightower and Gaetano Borriello. Location systems for ubiquitous computing. Computer, 34(8):57–66, 2001.   
[7] Ming-Kuei Hu. Visual pattern recognition by moment invariants. IRE Transactions on Information Theory, 8(2):179–187, 1962.   
[8] Zhihu Huang and Jinsong Leng. Analysis of hu’s moment invariants on image scaling and rotation. In Proceedings of the ICCET 2010, volume 7, pages V7–476, 2010.   
[9] David P Luebke. A developer’s survey of polygonal simplification algorithms. Computer Graphics and Applications, 21(3):24–35, 2001.   
[10] Justin Gregory Manweiler, Puneet Jain, and Romit Roy Choudhury. Satellites in our pockets: an object positioning system using smartphones. In Proceedings of the MobiSys 2012, pages 211–224, 2012.   
[11] Marcos Nieto and Luis Salgado. Non-linear optimization for robust estimation of vanishing points. In Proceedings of the ICIP 2010, pages 1885–1888, 2010.   
[12] Radu Orghidan, Joaquim Salvi, Mihaela Gordan, and Bogdan Orza. Camera calibration using two or three vanishing points. In Proceedings of the FedCSIS 2012, pages 123–130, 2012.   
[13] Emanuel Parzen. On estimation of a probability density function and mode. The annals of mathematical statistics, pages 1065–1076, 1962.   
[14] Arun Qamra and Edward Y Chang. Scalable landmark recognition using extent. Multimedia tools and Applications, 38(2):187–208, 2008.   
[15] Srikumar Ramalingam and Matthew Brand. Lifting 3d manhattan lines from a single image. In Proceedings of the ICCV 2013, pages 497–504, 2013.   
[16] Jason Rife, Sam Pullen, Boris Pervan, and Per Enge. Paired overbounding and application to gps augmentation. In Proceedings of the PLANS 2004, pages 439–446, 2004.   
[17] Torsten Sattler, Bastian Leibe, and Leif Kobbelt. Fast image-based localization using direct 2d-to-3d matching. In Proceedings of ICCV 2011, pages 667–674, 2011.   
[18] Ashutosh Saxena, Min Sun, and Andrew Y Ng. Make3d: Learning 3d scene structure from a single still image. IEEE Transactions on Pattern Analysis and Machine Intelligence, 31(5):824–840, 2009.   
[19] Souvik Sen, Romit Roy Choudhury, Bozidar Radunovic, and Tom Minka. Precise indoor localization using phy layer information. In Proceedings of the 10th ACM Workshop on Hot Topics in Networks, page 18, 2011.   
[20] Yi Shang, Wenjun Zeng, Dominic K Ho, Dan Wang, Qia Wang, Yue Wang, Tiancheng Zhuang, Aleksandre Lobzhanidze, and Liyang Rui. Nest: Networked smartphones for target localization. In Consumer

Communications and Networking Conference (CCNC), 2012 IEEE, pages 732–736. IEEE, 2012.   
[21] Longfei Shangguan, Zimu Zhou, Zheng Yang, Kebin Liu, Zhenjiang Li, Xibin Zhao, and Yunhao Liu. Towards accurate object localization with smartphones. IEEE Transactions on Parallel and Distributed Systems, 25(10):2731–2742, 2014.   
[22] Satoshi Suzuki et al. Topological structural analysis of digitized binary images by border following. Computer Vision, Graphics, and Image Processing, 30(1):32–46, 1985.   
[23] Olivier Van Laere, Steven Schockaert, and Bart Dhoedt. Finding locations of flickr resources using language models and similarity search. In Proceedings of the ICMR 2011, page 48, 2011.   
[24] R Grompone Von Gioi, Jeremie Jakubowicz, Jean-Michel Morel, and Gregory Randall. Lsd: A fast line segment detector with a false detection control. IEEE Transactions on Pattern Analysis and Machine Intelligence, 32(4):722–732, 2010.   
[25] He Wang, Souvik Sen, Ahmed Elgohary, Moustafa Farid, Moustafa Youssef, and Romit Roy Choudhury. No need to war-drive: unsupervised indoor localization. In Proceedings of the MobiSys 2012, pages 197–210, 2012.   
[26] Qia Wang, Alex Lobzhanidze, Suman Deb Roy, Wenjun Zeng, and Yi Shang. Positionit: an image-based remote target localization system on smartphones. In Proceedings of the 19th ACM international conference on Multimedia, pages 821–822. ACM, 2011.   
[27] Wikipedia. Pin hole camera model, 2008. http: //en.wikipedia.org/wiki/Pinhole\_camera\_model.   
[28] Chenshu Wu, Zheng Yang, Yunhao Liu, and Wei Xi. Will: Wireless indoor localization without site survey. IEEE Transactions on Parallel and Distributed Systems, 24(4):839–848, 2013.   
[29] Zheng Yang, Chenshu Wu, and Yunhao Liu. Locating in fingerprint space: wireless indoor localization with little human intervention. In Proceedings of the 18th annual international conference on Mobile computing and networking, pages 269–280. ACM, 2012.   
[30] Zheng Yang, Zimu Zhou, and Yunhao Liu. From rssi to csi: Indoor localization via channel response. ACM Computing Surveys (CSUR), 46(2):25, 2013.   
[31] Amir Roshan Zamir and Mubarak Shah. Accurate image localization based on google maps street view. In Computer Vision–ECCV 2010, pages 255–268. Springer, 2010.