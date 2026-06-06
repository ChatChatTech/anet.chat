# Perceiving the Slightest Tag Motion beyond Localization

Lei Yang, Member, IEEE, Yi Guo, Student Member, IEEE, Tianci Liu, Student Member, IEEE and Cheng Wang, Member, IEEE Yunhao Liu, Fellow Member, IEEE

Abstract—Existing methods in RFID systems often employ presence or absence fashion to detect the tags’ motions, so they cannot meet motion detection requirement in many applications. Our recent observations suggest that the signal strength backscattered from the tag is hypersensitive to its position, inspiring us to perceive the tag motion through its radio signal strength changes. Motion perception is not trivial and challenged by weak stability of strength in that any other interference or noise may incur significant changes as well, resulting in high false positives. To tackle this issue, we propose to model the strength via the Mixture of Gaussian Model (MoG). The problem is thus converted to foreground segment in computer vision with the help of Strength Image, where the technique of MoG based background subtraction is employed. We then implement a prototype using commercial off-the-shelf products. The evaluation results show that the slightest tag motion (∼ 10cm) can be precisely perceived, and the accuracy is up to 92.34% while the false positive is suppressed under 0.5%.

Index Terms—RFID, Motion detection, Background substraction, Mixture of Gaussian Model

# 1 INTRODUCTION

A RFID readers and tags. Tags are attached to products for labeling, and usually have no battery supply so they have to be N RFID system typically consists of a large number of activated within the interrogation area of a reader. The reader interrogates the tags and collects their IDs via continuous RF waves, without the need of in sight or touch. In contrast to conventional identification technologies, like barcodes, RFID systems have many advantages, such as non-optical proximity, long transmission range, and quick identification.

The initial motivation of RFID is to automatically identify objects fast and conveniently, but its potential applications have been widely studied in recent years for areas. Two classical scenarios are presented as follows. Securing valuable objects. Museums and art galleries use RFID to track valuable artifacts, which is treated as a cost-efficient solution when the price of nowadays RFID tags can be as low as 1 USD per capita. A key requirement is that any movement of the tag (and thus the associated item) can be accurately captured, which might be as slight as centimeters. RFID leverages the RF signals as Mining customer’s behaviors. To stay competitive, a large number of data mining techniques have been introduced to help supermarket managers better understand consumers’ behaviors. Unfortunately, the techniques are generally confined to the consumers’ purchase data. The motion of the RFID tags on the products again implies rich behavioral information of the customer, e.g., taking the product from the shelf and returning it back. Again, precise and accurate detection of tag motion is of essential importance in this application. At first glance, there is not any connection between the above two scenarios. Actually, both focus on the surveillance of tag motions: the first needs an alert when valuable objects are moved; the second requires behavior records when the products are taken off the shelf.

To the best of our knowledge, few works have been studied on the surveillance of tag motion. Most previous works detect tag motion based on its absence or presence in ranges of different RFID readers, which gives very coarse granularity but cannot precisely detect slight tag motion at centimeter level. The recent RFID tag localization approaches [1]–[3] can work with better precision, but still at meter level which is not high enough. Besides, tag localization often incurs high deployment cost, including the deployment of numerous RFID readers and anchors.

In this study, we propose and design Frogeye, a system that exploits the signal strength changes of the backscattered from moving tags to provide a hypersensitive approach for tag motion perception. In theory, the power received by the reader which is backscattered from the tag, goes as the inverse fourth power of the distance in between. Such a characteristic makes the signal strength hypersensitive to tag positions. Our empirical studies validate the hypotheses, and reveal expected and encouraging results. Strength change based motion perception approach provides three obvious benefits: First, no additional devices are required because the radio signal strength is the most common parameter provided by the commercial off-the-shelf (COTS) readers. Second, there is no need for pre-deployed anchors or infrastructures. Third, open and welcoming surveillance can be offered without line of sight, which allows persons and objects to move between the reader and tags.

Motion perception at high accuracy is not trivial because the signal strength has weak stability in that arbitrary other interference or noise may incur significant changes. In detail, the thermal noise enables the signal strength to vibrate in a small range. Multipath enhances or weakened the strength. To address this issue, we utilize the Mixture of Gaussian (MoG) to model such weak stability. Our approach includes three steps. In the first step, a preprocessing is applied to divide the original reading stream into read frames. In the second step, the frame is projected into a strength image. An improved MoG based background subtraction (MoG-BS) method from computer vision is applied to detect the foreground pixels in the third step. We also design the mechanism to discover the moved tags through the detected foreground pixels.

Compared with the existing methods, Frogeye advances the perception in terms of sensitivity and stability. Our major contributions are summarized as follows.

• We conduct extensive statistical analysis of strength collected in a real-life office, showing that the strength are indeed hypersensitive to tags’ positions, but suffers from weak stability where the strength values are highly clustered in a small range due to thermal noise, and enhanced or weakened due to multi-path effect. We then present a MoG to accurately characterize the weak stability.   
• We propose Frogeye, to perceive the slight of tag motion. This approach takes a snapshot of tags’ positions through their backscattered strength every several read cycles, producing a sequence of strength frames. The MoG-BS is leveraged to detect any foreground pixels, namely moved tags in our scenario.   
• We implement the Frogeye using pure COTS RFID devices, ImpinJ R420 reader, and evaluate it at varying parameter choices. The evaluation results show that the slightest tag motion can be precisely perceived (∼ 10 cm on average), and the accuracy is up to 92.34% while the false positive is suppressed under 0.5%.

The remainder of the paper is structured as follows. We introduce and model the weak stability of signal strength in Section 2. The main design of Frogeye is presented in Section 3. The implementation and evaluation are given in Section 5. The related works about RFID system are overviewed in Section 6. Finally, Section 7 concludes this paper.

# 2 MODELING THE WEAK STABILITY

In this section, we introduce the theoretical background of the RFID technique and perform several empirical studies to model the weak stability of strength.

# 2.1 Intuition

Passive tags not equipped with batteries do not use a radio transmitter. Instead, they use modulation of the reflected power from the tags. Referring to [4], we can construct a mathematical statement of the power relationships using the Friis equation. Defining the gains of the reader’s and tag’s antenna $G _ { \mathrm { r e a d e r } } , G _ { \mathrm { t a g } } ,$ a backscatter transmission loss $T _ { b }$ , we can describe the power backscattered by the tag as:

$$
P _ {\mathrm{RX}, \text { reader }} = P _ {\mathrm{TX}, \text { reader }} G _ {\text { reader }} ^ {2} G _ {\text { tag }} ^ {2} \left(\frac {\lambda}{4 \pi d}\right) ^ {4} T _ {b} ^ {2}
$$

where λ is the wavelength and d is the distance between reader and tag. The above equation indicates that the power received by the reader and backscattered from the tag, goes as the inverse fourth power of the distance. In other words, the power backscattered by the tag is hypersensitive to the tag’s positions. This characteristic inspires and motivates us to perceive the tag motion by leveraging the changes in its signal strength. But the intuition becomes reality only when the backscattered strength behaves relatively stable. Namely, the strength backscattered from a stationary tag should remain unchanged.

![](images/97026ac3abad7a95a7a7b9ee7ba17064c04358c3d4f4fc665d8723f287082e01.jpg)



Fig. 1. Strength distribution over different distances. The figure shows that the strength is hypersensitive to the distance but exhibits weak stability.

We place a tag in front of the antenna in a quiet lab without any interference. The strength collected from different positions are shown in Fig. 1, where the d indicates the distance (cm) between the reader and tag. We observe that (1) the strength is indeed hypersensitive to the distance. The strength difference is very noticeable even if the two positions are very close (∼ 10cm). About the strength sensitivity, we further conduct evaluation in Section 5. (2) Unfortunately, the result is not as stable as expected, because the value occupies several units even when the tag remains in a same distance. We call this phenomenon weak stability.

In fact, it is still full of challenges to perceive the slightest tag motion despite the strength backscattered by the tag being hypersensitive to the motion, because the electronic component’s thermal vibration also brings changes. Especially when the strength is interfered, its changes are as significant as when the tag is moved. It is easy to mistakenly consider a stationary object moved. Aiming to distinguish these changes caused by real motion from the thermal vibration or interference, we next offer empirical insights into the weak stability and statistical methods to model them.

# 2.2 Modeling the Thermal Noise

As illustrated in Fig. 1, the strength of stationary tag does not always remain constant in the manner we expected. There is a range of vibration whatever effort we make to enable environment interference free. Actually, we think such vibration mainly comes from the thermal noise of the electronic components rather than the environment. Therefore, we model the strength using Gaussian distribution $N ( \mu , \sigma ^ { 2 } )$ ). We believe this model is reasonable because a lot of natured phenomena follows the Gaussian distribution, especially thermal noise from internal electronic components, which mainly contribute the vibration. Then the probability that target tag x has strength value $x _ { t }$ at time t is estimated as:

$$
\eta (x _ {t}) = \frac {1}{\sqrt {2 \pi | \sigma^ {2} |}} \exp \left(- \frac {(x _ {t} - \mu) ^ {T} (x _ {t} - \mu)}{2 | \sigma^ {2} |}\right)
$$

The Gaussian model depends on the tag position and features of the electronic components. The preview determines the center of vibration and the latter constrains its range. To verify the Gaussian model, we first use the Quantile-quantile plot (QQ plot) to visually display whether the X is from a Gaussian distribution (Gaussian model). If the distribution of X is normal, the plot will be linear compared with the ideal theoretical distribution. We use the interference-free trace from the first measurement. Fig. 2(a) plots collections from two different antennas. In the figure, the x-value of the point is the theoretical quantile and the y-value is the quantile of the data trace. The dashed line is the straight line connected by the first and third quartile calculated theoretically. If the traces follow the theoretical Gaussian distribution, their quantile is distributed around the dashed line. As we expect, the points in the figure are linear and very close to the theoretical line. Second, we employ Jarque-Bera Test (JB test) of 0.95 significance level to quantitatively evaluate the goodness-of-fit of the Gaussian model. The JB test is a widely adopted tool to test whether the sample data matches a Gaussian distribution. In detail, we can fit the Gaussian model by maximum likelihood estimation given a collected samples, $\{ x _ { 1 } , \cdots , , x _ { t } \}$ , as follows.

![](images/188dc58d2a12f8957eb864dbfb6269427e8de69c486403ad7b3a1ccba5622444.jpg)



(a) QQ Plot

![](images/848a4919b6aefa1168da39aeec44b4fe22c6bc72f3d170040ea67d6bf917a8c9.jpg)



(b) JB Test

![](images/97c869509b93aec2d393313d1f4d985d8f99b0ab16f7c8528b5847db78ee3e1b.jpg)



(c) Strength cloud   
Fig. 2. Modeling the strength values. (a) The QQ plot is used to visually display whether the strength value follows Gaussian model. If yes, the plot will be linear compared with the ideal theoretical distribution. (b) The Jarque-Bera test of 0.95 significance level is employed to quantitatively evaluate the goodness-of-fit of the Gaussian model. If points are clustered at the top and right-hand corner, then the fitness is good. (c)The strength is scattered in a polar coordinate in which the angle is randomly chosen and radius denotes its strength value.

$$
\mu \approx \bar {x} = \frac {1}{t} \sum_ {i = 1} ^ {t} x _ {i} \text { and } \sigma^ {2} \approx \frac {1}{t} \sum_ {i = 1} ^ {t} (x _ {i} - \bar {x}) ^ {2}
$$

Since the trace is recorded according to the time flow, we divide the whole time recorded into equal size windows. The JB test is then applied for each window to test the goodness-of-fit for the estimated Gaussian model. The pass rate is calculated every 100 windows. The test is performed on 100 tag traces. Fig. 2(b) illustrates the pass rate using the JB test. If points are clustered at the top and right-hand corner, then the fitness is good. We observe that the modelability of the strength using Gaussian model is rather convincing.

# 2.3 Modeling the Environment

In the second experiment, we bring an obstructed object when collecting the strength from the target stationary tag. We let one obstructed object (a person) walk through the intermediate region between the reader and target tag. In the experiment, a total of 13,797 strength values are recorded. Fig. 2(c) plots the tag’s ‘strength cloud’ in which the point is scattered using one strength value in a random direction. The point in the polar origin has the strongest strength. It is evident that: (1) being different from the case without the obstruction, the strength vibration does not concentrate on a sole level any more. Instead, there are three clear levels which correspond to three cloud layers in the figure. Clearly, the strength is enhanced or decayed by the person’s movement. (2) the thickness of each layer is equally likely. Essentially, the vibration ranges are very similar. This indicates that the thermal noise is still the leading factor contributing to the vibration whether the tag is interfered with or not.

These phenomenons can be explained by the multipath effect. There exist several paths for the backscattered signal propagating from tag to reader. The signal strength propagating through different paths varies a lot due to the path length. The reader prefers to resolve the strongest signal from all paths. Note that the strongest does not always come from the shortest path because two signal propagation may either cancel out or reinforce each other. When the interference object gets close to the tag, it may block some propagation paths and lead to the propagation jumping among the multiple paths, resulting in the strength migrates from one level to another.

From a long-term perspective, the strength exhibits multimodal characteristics where the distribution is likely composed of multiple Gaussian models. For example, Fig. 3(a) shows the strength changes in the above measurement over a short period of time (20s). Some of the time the strength regularly vibrates without obstruction while some of the time it may be weakened. Fig. 3(b) shows the fitted Gaussian curve for this tag’ strength. It is clear that the strength distribution is multi-modal containing more than one peak, so a single Gaussian model cannot exactly depict the truth. Actually, the multi-modal model is comprised of three single Gaussian models in the example, as shown in Fig. 3(c), 3(d), and 3(e). The final distribution can be considered as a weighted mixture of three, $G = w _ { 1 } G _ { 1 } + w _ { 2 } G _ { 2 } + w _ { 3 } G _ { 3 }$ . To cope with such a complicated scenario, the Mixture of Gaussian Model (MoG) based approach is employed here. We present a generalization to this approach. The strength is modeled by a mixture of K Gaussian models. The probability that the tag x has strength $x _ { t }$ at time t is estimated as:

$$
\begin{array}{l} \eta (x _ {t}) = \sum_ {i = 1} ^ {K} w _ {i} \eta_ {i} (x _ {t}, \mu_ {i}, \Sigma_ {i}) \\ { = } { \sum _ { i = 1 } ^ { K } \frac { w _ { i } } { ( 2 \pi ) ^ { - \frac { d } { 2 } } | \Sigma _ { i } | ^ { \frac { 1 } { 2 } } } \exp \left( \frac { 1 } { 2 } ( x _ { t } - \mu _ { i } ) ^ { T } \Sigma _ { i } ( x _ { t } - \mu _ { i } ) \right) } \\ \end{array}
$$

where $w _ { i }$ is the weight, $\mu _ { i }$ is the mean and d is the reader’s antenna number. $\Sigma _ { i }$ is the covariance for the $i ^ { t h }$ Gaussian model. Actually, the parameter $x _ { t }$ and $\mu _ { t }$ are vectors with d dimension, explained later in Section 3. Since the strengths are independently captured by d antennas, we set $\Sigma _ { i } = \sigma _ { i } ^ { 2 } \mathbf { I }$ where I is an identify matrix with d dimension. Then probability is reduced to

$$
\eta \left(x _ {t}\right) = \sum_ {k = 1} ^ {K} \prod_ {j = 1} ^ {d} \frac {w _ {k}}{\sqrt {2 \pi \sigma_ {j} ^ {2}}} \exp \left(- \frac {\left(x _ {t} - \mu_ {i}\right) ^ {2}}{2 \sigma_ {j} ^ {2}}\right) \tag {1}
$$

The K is determined by the potential number of propagation paths. Usually, from 3 to 10 are used according to our experience. We can see the weak stability of strength is actually mainly determined by the environment, e.g. the propagation paths, instead of the obstruction object. In theory, the peaks in MoG are as many as the potential propagation paths. Each Gaussian model in MoG corresponds a potential signal propagation and its weight is related to the time interval that the propagation takes effect in this path. Note that unlike the active communication, the backscattered signals from tag are too weak to penetrate the interference objects to generate a new vibration level. In addition, despite the interference object may create a new path to backscattered the signals, their effects are very limited on the MoG, as will be shown in Section 5. This fact motivates us to build the model through the history of strength and leverage the model to perceive tag motions.

![](images/25aa632b2b785ffff08f16d9b2a20a8eeaaaa16290db34fa5f4e2ca73528d8a7.jpg)



(a) Time serials

![](images/94dad179aa1b20083490f1e244202f3be18b8ed73e9c070bef3663e5901081ce.jpg)



(b) G

![](images/cf2915f6651f8e068b8811e55326ae88947d4a9585ef3f6fc1d8a4d614363c32.jpg)



(c) $G _ { 1 }$

![](images/879df28bdb3079f3bb2c6e6ed4b9738b5183c82011efdd916f37d41033ac7db1.jpg)



(d) $G _ { 2 }$

![](images/3e6e7468f9d92d729a0bc6d5d6e4216c7500bef29ccd4e7d2ddc75ba18ae3ceb.jpg)



(e) $G _ { 3 }$   
Fig. 3. The tag was captured for 20 seconds when a person randomly walked around the tag. (a) Strength values over 20 seconds. (b) Gaussian model fitted with the values over 20 seconds. (c) The model $G _ { 1 }$ fitted over [10s, 14s]. (d) The model $G _ { 2 }$ fitted over [4s, 8s]. (e) The model $G _ { 3 }$ fitted over [14s, 18s].

# 3 FROGEYE

In this section, we introduce the technique of MoG based background subtraction to perceive the tag motion via strength image. We call our approach Frogeye, because the natural construction of a frog retina enables its eyes to be hypersensitive to the moved objects but blind to static ones.

# 3.1 Overview

Our basic idea is to detect the ‘significant’ changes of the backscattered signal for perception of tag motion. There is a high probability that the tag moved when its strength changed significantly. The naive method is to compare the latest strength with the last one. If their difference exceeds a threshold, the motion is reported. However, the weak stability may trigger the significant changes as well. For example, the strength may migrate from one vibration level to another level far away when the original propagation path is blocked by the interference object. In this situation, the strength changes exhibit significant as the tag moves, giving rise to mistakenly determination, the false positive.

We find our problem is very similar to the foreground segmentation in computer vision, which is to segment the foreground pixels that “significantly differ” between the latest image of sequence and the previous images. To associate these two issues, we project the target tags into a strength image in which the strengthes of each tag are mapped to a row of pixels. The fact is that the values of these related pixels significantly change and these pixels become to foreground when the related tag moves. Therefore, as long as the foreground is detected, the moved tags are discovered. A lot of methods are proposed for foreground segmentation. We adopt the most popular one, MoG based background subtraction (MoG-BS), due to two reasons. First, MoG-BS well tackles illumination vibration and background motion. These two problems resemble our challenges incurred by the weak stability. Second, both strength and pixel value can be modeled using the MoG. In detail, the history of each a pixel is applied to build a MoG composing of K Gaussian models. When a new pixel value is captured, the value is compared with the built K models. If the value matches any one of the K models, the pixel is consider as background. Otherwise the foreground. After the foreground are segmented, we can easily reverse them to moved tags since the projection remains unchanged during the process.

![](images/2b28f7f9073004094811a10fb451c6047f1d06a4e1c2475e79ea128feabef60f.jpg)



Fig. 5. Definition of strength frame. The frame is a set of readings collected during m consecutive read cycles while each read cycle contains four antenna cycles.

# 3.2 System Architecture

Our goal is to determine whether the tag is really moved when its strength changes. Fig. 4 presents the overall algorithm flow of Frogeye. We describe the high level flow of information through its flow, and present the internal details later. Our approach contains three steps inputing strenght flow and outputing event flow. The reader repeatedly interrogates tags using multiple antennas and produces a stream of readings in its detection field. The first step is to split the original reading stream into many read cycles by time. Then the preprocessing aggregates m read cycles into a read frame. The read frame is the processing unit fed into the following steps. In the second step, a strength image is constructed using the readings in one read frame. In the third step, called motion perceiption, we model each pixel using MoG to determine whether the pixel belongs to the foreground. This component outputs a serials of labels that indicates each pixel is either a foreground or background. During the perceiption, we should model the background, detect the foreground, and reverse the foreground to tag motion. We observe a stationary tag may be wrongly determined as being in motion beucause of tag’s misread or neighbour obejcts’ movements. We call this kind of phenomenon as collateral motion. To address this issue, we propose the last step for motion refinement.

![](images/0c632600ef854c231ed9dcdc191f1f6c7f2ecf61be5eb7478bd25121b4291088.jpg)



Fig. 4. Flow chart of the algorithm. There are three steps with inputing strength flow and outputing event flow.

# 3.3 Preprocessing

The reader circularly scans the target space. The input of our system is a stream of readings. Before entring processing, we should split the strength flow into read frames. Fig. 5 illustrates the basic proesss units and their relationships. A commercial reader usually contains d antennas successively scheduled by a time division algorithm. Therefore each read cycle can be further divided into small parts denoted as antenna cycles. The reader uses each antenna to collect one set of readings from the target tags during an antenna cycle. If the tag is located within the overlapping region by multiple antennas, it will be collected many times. We define a higher kernel term, denoted as read frame. The read frame is a set of readings collected during m consecutive read cycles where m is a user specific parameter. The main task of preprocessing is to split the strength flow into a sequence of read frames.

# 3.4 Constructing Strength Image

After separating the frames from the strength flow, we project the readings in one read frame to a strength image. Suppose the reader monitors n tags, $\{ T _ { 1 } , T _ { 2 } , \cdots , T _ { n } \}$ , in the target space and all of them are known in advance. Then each read frame should contains $n \times m \times d$ readings. Note some tags may be beyond the range of some antenna. In this situation, the system creates a default reading for the tag, whose strength is set to the default value, e.g.- 90. We project a read frame of readings into a strength image I as follows:

![](images/6758fb7756db33a6d411b4b07b1a85e185f73fcc7b42e0a87b6a4676c1019460.jpg)



Fig. 6. Constructing the strength image. The readings in one frame are projected into a strength image. We consider each image produced by one antenna comes from different color channels. The final image is synthesized by these images of different colors.

$$
I = \left( \begin{array}{c c c c} x _ {1, 1} & x _ {1, 2} & \dots & x _ {1, m} \\ x _ {2, 1} & x _ {2, 2} & \dots & x _ {2, m} \\ \vdots & \vdots & \vdots & \vdots \\ x _ {n, 1} & x _ {n, 2} & \dots & x _ {n, m} \end{array} \right)
$$

In the image, each row is uniquely mapped to a same tag. The mapping fashion between the tags and rows is arbitrary as long as their mapping remains constant during the processing. Each column represents a read cycle. The whole image contains a total of m columns. Formally, given a strength image, the element $x _ { i , j }$ represents a reading strength from the $i ^ { t h }$ tag (Ti) collected in the $j ^ { t h }$ read cycle of the frame. Since the tag is read multiple times by d antennas in one read cycle, the $x _ { i , j }$ is indeed a vector. We consider them as the color values coming from different color channels (related to different antennas), such as red, green, blue, and alpha channels. Namely, $x _ { i , j }$ is a vector with d dimension. Actually, our approach is independent on the dimension of pixel. Even if there are more than four strengths captured, they will be fully considered. An example is shown in Fig. 6. There are 9 tags in the target space and three antennas are deployed. After a read frame, each antenna creates an image with $9 \times 8$ resolution $( m = 8 )$ . These three images are synthesized to a final image, which is going to be fed into the next step (foreground detection). Through image construction, the original reading stream eventually becomes a sequence of strength images, denoted as $\mathcal { T } = \{ I _ { 1 } , I _ { 2 } , \cdot \cdot \cdot , I _ { t } \}$ .

Why would we project the strength into an image? At the first glance, there is no connection between an optical image in computer vision and tag’s signal strength. Actually, we think the physical rationale behind them are similar. As shown in Fig. 7, (i) both of them focus on capturing the projections of objects. In optics, the light wave coming from the flashlight is reflected by the object and then captured by the camera. In our scenario, the wave becomes an electromagnetic wave. The wave is reflected by the tag and captured by the antenna. (ii) the optical image is an optical projection of the object while the backscattered strength can be considered as an electromagnetic projection of the tag. (iii) hence, the reader antenna can be considered a special ‘camera’ producing the tags’ imaging. The optical camera outputs optical images while the RFID antenna provides a strength image. (iv) when the objects are moved in the real target space, the pixels reflected from the objects significantly change in the images. The similar thing occurs in our scenario. The pixels reflected from the tags change when the tag moves. Therefore, we think the strength image represents a snapshot of current tags’ positions. Part of the images change when the tags move. (v), importantly, as we model the weak stability of tag’s strength, the pixel’ intensity can be modeled by the MoG as well.

![](images/aa34d636f5490d13eea1762183b2369d45db7e26f540a931bc6608d8ec533561.jpg)



Fig. 7. The physical rationale behind computer vision and RFID system.

# 3.5 Foreground Detection

Foreground detection from a sequence of images is a fundamental problem in computer vision, which has been well studied for many years [5]–[7]. Its goal is to segment the foreground pixels corresponding to moving objects, such as vehicles and humans, from the rest of an image, i.e. background. The foreground is the set of pixels that “significantly differ” between the latest image of the sequence and the previous images, given a set of images of the same scene taken at several different times.

Background subtraction is the most popular method for foreground segmentation, especially under those circumstances with a relatively dynamic background. It detects the foreground in an image by taking the difference between the current image and the reference background. The main idea behind it is to automatically generate and maintain a representation of the background that is then used to classify the pixels as background or foreground. The MoG-BS has been one of the most popular background subtraction techniques in the computer vision because of its robustness to subtle illumination changes and background motions. Here we employ and improve the MoG-BS from [8]. This algorithm is able to fast model the MoG using the training set and adaptively update the models during applying.

Modeling background with history: To make the problem more precise, we generally denote a sequence of strength images as $\mathcal { T } = \{ I _ { 1 } , I _ { 2 } , \cdot \cdot \cdot , I _ { t } \}$ . For any pixel I(x) in an image $I , x \in$ $\mathbb { R } ^ { l }$ and $\bar { I } ( \boldsymbol { x } ) \in \mathbb { R } ^ { d } , l$ is the dimension of the image. Typically, when $l = 1$ , the image is one dimension and can be represented as a vector. When $l = 2 .$ , the image is a matrix. Typically, $d = 1$ for a gray-scale image or $d = 3$ for RGB color images, but other values are allowed. At any time t, the history of a particular pixel x is

$$
\{x _ {1}, \dots , x _ {t} \} = \left\{I _ {i} (x,), 1 \leq i \leq t \right\}
$$

The history of such a pixel is applied to model the pixel values using the mixture of K Gaussian models. Initially, the K Gaussian models are given by an initial large variance $w _ { k }$ and low prior weight $\sigma _ { k }$ . These K Gaussian models are ordered by the criterion of $r _ { k } = w _ { k } / | \sigma _ { k } |$ . This order supposes that a background pixel corresponds to a high weight with a small variance because the background is more present than foreground. On the next frame, we have a new pixel value $x _ { t + 1 }$ . We say the Gaussian model is ‘matched’ i $\mathrm { f } \ x _ { t + 1 }$ is within λ× standard deviation of this Gaussian model. Here, we use the Mahalanobis distance to compare two vectors. Suppose the matched model $N ( \mu _ { k , t } , \sigma _ { k , t } ^ { 2 } )$ , the match rule is formulated as follows:

$$
(x _ {t + 1} - \mu_ {k, t}) ^ {T} \cdot (x _ {t + 1} - \mu_ {k, t}) <   \lambda^ {2} \cdot | \sigma_ {k, t} ^ {2} |
$$

Considering each pixel, there are two results:

Case 1: A match is found with one of the K Gaussian models, termed as $G _ { k } .$ . In this case, the pixel is classified as background.

Case 2: No match is found with any of the K Gaussian models. In this case, the pixel is classified as foreground.

According to the above results, the parameters of each model must be updated to make next foreground detection. Using the match result, two cases can occur such as in the foreground detection:

Case 1: A match is found with one of the K Gaussian models. For the matched model $G _ { k }$ , we increase its weight, adjust the mean closer to $x _ { t } ,$ , and decrease the variance as follows.

$$
w _ {k, t + 1} = (1 - \alpha) \times w _ {k, t} + \alpha
$$

where α is a learning rate.

$$
\mu_ {k, t + 1} = (1 - \gamma) \times \mu_ {k, t} + \gamma \times x _ {t + 1}
$$

$$
\sigma_ {k, t + 1} ^ {2} = (1 - \gamma) \times \sigma_ {k, t} ^ {2} + \gamma \times (x _ {t} - \mu_ {t + 1}) ^ {2}
$$

where $\gamma = \alpha \times \eta \left( x _ { t + 1 } \middle | \left( \mu _ { k } , \sigma _ { k } \right) \right)$ and $\eta ( \cdot )$ refers to Equation 1. For the unmatched models, we decrease their weights:

$$
w _ {i, t + 1} = (1 - \alpha) \times w _ {i, t}
$$

Case 2: No match is found with any of K Gaussian models. In this case, the model with least order is replaced by a new model with a mean equals to the new pixel value $x _ { t + 1 }$ , and initial large variance and low prior weight.

Foreground detection: Above algorithm is an adaptive process. In the training phase, we cloud set a bigger learning rate. The training phase ends when the K models become stable. In applying phase, we stop learning by setting the learning rate to zero. With regard to the dynamical situation in which the environment slightly changes, the smaller learning rate, e.g. 0.001, is allowed to let the system self-adaptively update. Especially it is able to accommodate the influence of the new few propagation paths produced by the interference objects. The foreground detection outputs a set of pixels labeling as foreground.

Reverse foreground to motion: Since we have a row of pixels mapping to one tag, the results of foreground detection are a mixture of background and foreground for each row. Suppose there are f pixels belonging to the foreground out of m values in a particular row. We define the probability of tag motion as $p = f / m$ . Therefore, the outputs of foreground detection for each read frame are reversely mapped to a vector:

![](images/2d0cdafb094aba367236cfa67a796ef1ef708cadd51f10a029a0c6acfcbae7cf.jpg)



Fig. 8. The collateral motion. The ground truth is shown in the first row where the target tag is indeed moved between the $1 3 ^ { t h }$ and 17th read frame but stays stationary in the left frames. However, due to the collateral motion, the target is mistakenly determined as moved in these frames plotted in black from the second row.

$$
\{<   T _ {1}, p _ {1} >, <   T _ {2}, p _ {2} >, \dots , <   T _ {n}, p _ {n} > \}
$$

where $T _ { i }$ is a reversely mapped tag and $p _ { i }$ denotes the probability that this tag moves. The simple method is to use majority voting to fuse the mixture in which the tag is determined moved only when $p \geq 0 . 5$ .

# 3.6 Motion Refinement

Consider two special scenarios. In the first scenario, the target tag may be temporarily and fully shielded by interference objects such that all potential signal’s propagation paths are blocked, incurring a missing reading. The default value created for the missing reading may be significantly different with the value captured last time. In the second scenario, the neighboring objects beside the target is moved. Its motion may involve the shaking of the target object. Both of the above scenarios introduce an incorrect determination. We call such a false motion the collateral motion. As illustrated in Fig. 8, the ground truth is shown in the first row where the target tag is indeed moved between the $1 3 ^ { t h }$ and $1 7 ^ { t h }$ read frame but stays stationary in the left frames. However, due to the collateral motion, the target is mistakenly determined as moved in these frames plotted in black from the second row. The collateral motion has an obvious common point that the motion is temporary and the tag eventually returns to the original position. To tolerate such unreliable collateral motions, we use the smoothing filter technique: a sliding window over the stream of motion events in the time window. Its goal is to reduce or eliminate involved motion within the time window. The window size is a crucial parameter such that it provides balance between tolerance and accuracy.

Bernoulli model: Consider a particular tag, we assume the output of motion detection for a particular tag in the current window is $W _ { t } = \{ p _ { ( t - w ) } , \cdots , p _ { t } \}$ where w is the window size and $p _ { t }$ is the motion probability outputted in the $t ^ { t h }$ read frame. We view each frame in the window as an independent Bernoulli trail, with success probability $p _ { t }$ about its motion status. Note that $p _ { i } ~ \in ~ W _ { t }$ is relatively homogeneous and thus we use the average empirical motion probability over the window to set the $p _ { t } ,$ namely,

$$
\tilde {p} = \frac {1}{w} \sum_ {i = 0} ^ {w} p _ {t - i}
$$

The number of moved frames, denoted as X, in the window is a random variable that follows a Binomial distribution, a sampling draw with parameters $( w , \tilde { p } )$ . From the standard probability theory, we can express the expectation and variance of X as $E [ X ] = w \times \tilde { p }$ and $V [ X ] = w \times \tilde { p } \times ( 1 - \tilde { p } )$ .

Adaptive smoothing algorithm: Based on the Bernoulli model, the probability that we mistakenly determine the tag as moved over w is exactly $( \tilde { p } ) ^ { w }$ . Setting this probability $( \tilde { p } ) ^ { w } \leq \delta$ and taking logs gives w l $\begin{array} { r } { \mathrm { n } ( \tilde { p } ) \leq \ln \delta . } \end{array}$ . Combining this with the inequality $- x \geq \ln ( 1 - x )$ for $x \in ( 0 , 1 )$ ), we see that it suffices to require $\begin{array} { r } { w \ge \frac { \ln ( \mathrm { i } / \delta ) } { 1 - \tilde { p } } } \end{array}$ ln(1/δ)1−p˜ . Thus, the size of the window must be ≥ d ln(1/δ) e $\begin{array} { r l } { \ge } & { { } \lceil \frac { \ln \left( 1 / \delta \right) } { 1 - \tilde { p } } \rceil } \end{array}$ to avoid the mistaken determination by involved motions with probability $\geq 1 - \delta$ . Namely,

$$
w _ {m i n} = \lceil \frac {\ln (1 / \delta)}{1 - \tilde {p}} \rceil \tag {2}
$$

where the parameter of δ indicates the confidence. When the window size w and motion probability $\tilde { p }$ is not too small, the model follows from a Chernoff bounds that the value of X should be within $2 \sqrt { V [ X ] }$ of its expectation with a probability close to 0.98. Based on such observations, we report a real motion event if the number of determined motions is less than the expected following condition:

$$
\left| X - w \tilde {p} \right| > 2 \sqrt {w \tilde {p} (1 - \tilde {p})} \tag {3}
$$

We design an adaptive algorithm to conduct the smoothing. The common algorithm Additive Increase but Multiplicative Decrease is adopted to adjust the window size. The window size is initialized to one for each tag and then adjusted dynamically according to the observed motion vector after the current window ends. In detail, if the size of a current window is smaller than the required minimized value based on Eqn. 2, we grow the size for the next window for this tag additively. If the size satisfies Inequality 3, we multiplicatively decrease it and a motion event is reported. The pseudocode is shown in Algorithm 1.

# 4 DISCUSSION

In this section, we discuss some issues that worth noting when deploying the system in practice.

# 4.1 Ambient Interference

In practice, the interferences may came from the ambience. For example, the strong sporadic interferes like mobile phones transmitting in the sam ISM band, may temperately enhance the RSS values or block the propagation of backscatter signals. Frogeye can deal with the ambient interference in three layers.

Algorithm 1 Adaptive motion smoothing   
Input: $W_{t} = p_{t-w}, \cdots, p_{t}$ /*current window*/
Input: $\delta$ /*the confidence for the tolerance*/
Input: $w_{t}$ /*the current window size*/
Output: $w_{t+1}$ /*the size for the next window*/ $w_{t+1} = 1$ $p_{t} = \frac{1}{w} \sum_{i=0}^{w} p_{t-i}$ $w_{min} = \left\lceil \frac{\ln(1-\delta)}{p_{t}} \right\rceil$ /*based on Equation 2*/
if $w_{t} < w_{min}$ then $w_{t+1} = \max\{\min\{w_{i} + 1, w_{min}\}, 1\}$ else if $w_{t}$ fulfills the Inequality 3 then $w_{t+1} = \max\{\min\{w_{t}/2, w_{min}\}, 1\}$ end if

First, there are about 50 channels available to avoid the frequency collision. We enable the reader random frequency hooping to avoid the enduringly interferences at one channel in the physical layer. Second, our algorithm is totally self-adaptive. It models the background with the latest RSS history, using the mixture of K Gaussian models. This characteristic allows our algorithm to resist the frequency interference in some extent. Most importantly, the ambient interference belongs to one of collateral motions. The motion would be refined and smoothed in the high level.

# 4.2 Walking speed

One of the benefits of using MoG to model the RSS changes is that the MoG is time-invariant and only cares about the strength distribution on frequency domain. As mentioned in Section 2.3, the strength distribution is multi-modal more than on peak due to the multi-path effect. Each propagation path contributes a Gaussian model. When the object gets close to the tag, it may block some propagation paths and lead to the propagation jumping to others, resulting the strength migrates from on model to another. Whatever the movement speed the user takes, it does not change the existed multipath and the learned MoG. Thus, the user’s walking speed does not take negative impacts on our approach.

# 4.3 Mobility Patterns

Each potential propagation path contributes a Gaussian model, while the propagation is determined by the environment instead of the moving objects. The signals are bounced off nearby objects, such as desks, tables, shelves, wall and so on. The K models remain unchanged as long as the environment is not changed and no matter how the users walks around the RFID systems. The user’s movements only affect the model orders, but does not create or eliminate any model during the monitoring phase. So the mobility patterns of users does not affect the models in monitoring phase. Considering the training phase, the system needs sufficient data to learn all of potential paths. It expects each path to be exposed by human movements. There is an implicit assumption that the samples collected in training phase and monitoring phase should be similar in nature and have internal connections. Thus, we need the mobility patterns of users collected for the training, should be adequately natural, such that they can reflects the user’s behaviors when monitoring. Of course, the system also dynamically creates a new model in order to adopt to the changed of environment. Even the models are not well learned during training, they can be gradually corrected in monitoring.

# 4.4 Variable Tag Population

In spite of constantly mapping between the tag and strength image, the process for each tag is totally independent. When dealing with the variable tag population, we can create an image with one row and m columns for each tag. In this way, the process does not be blocked when tag leaves or new tag enters.

# 4.5 Real-Time

Thanks for your comments. Yes, the real-time is an important metric when applying the algorithm in practice. The real-time depends on the scanning rate of reader. A modern COTS UHF reader usually supports 300 reads per second. Suppose there are 100 tags being monitored in the surveillance area, each tag can be read for about 3 times per second. In other words, the tag is read

![](images/5f29ef67d17e04662804e6fe1ac377e1b8f2d2dc7d1e63d05c01153f24c43a2a.jpg)



(a) Stationary scene

![](images/8d65c8f6138ce4288972209dae4bf5e9a415adf67c42c2f9363bb12e56065925.jpg)



(b) Mobile scene   
Fig. 9. Experiment setups in stationary and mobile scene. (a) 100 tags are attached on a white board in the office. Their positions remain unchanged. (b) Mobile trace are collected by attaching a tag on a mobile toy train.

every 300ms. A normal reader has a about 10m read range. If the users wants the tag motion not to be detected, he should take it using a speed of about 10m/300ms ≈ 33m/s. In practice, it is too fast to be fulfilled. Thus, our real-time can be guaranteed.

# 5 IMPLEMENTATION AND EVALUATION

In this section, we present the implementation and also conduct performance evaluation on the prototype.

# 5.1 Implementation

Our implementations are purely based on the COTS devices and standard communication protocol. In details,

Hardware: In our implementation, we employ R420 reader from ImpinJ. Total 100 tags with 4 kind of models are used. Four reader antennas polarized in horizontal direction are deployed in a line. The transmission power is adjusted at 30mW .

Software: We adopt Low Level Reader Protocol (LLRP) to communicate with the reader. This protocol was ratified by EPCglobal in April 2007. We adjust the configuration of reader to immediately report reading whenever tag is detected. The client code is implemented by Java language with help of Apache Math library.

Parameter choices: Frogeye comes with a number of different parameters. Four key parameters are employed as follows. Frame size is set to m = 10. The learning rate α is set to 0.1 for training phase but 0.001 when detecting. The number of Gaussian K is a user estimated parameter, which really depends on the environment. In experiment, we set K = 10 to adapt potential propagation paths. Note that it does not matter to use large K because the redundant models will be naturally ignored according to our algorithm. Since we use the ROC curve to measure the accuracy, the match threshold is considered as the operating parameter varying from 0.01 to 2.0.

# 5.2 Evaluation Methodology

In terms of the false positives, we deploy a white board on which 100 tags are attached, in the office, as shown in Fig. 9(a). There are 20 persons staying in the room. These persons, whose weights and heights vary in 60kg ∼ 90kg and 1.6m ∼ 1.8m, may interfere the signal strength when getting close to the board. We use four antennas continuously reading these tags for 24 hours. A total of 1, 130, 997 readings are collected. The traces collected in the first 6 hours are employed as the training set to model background models for each tag, and the left 18-hour traces are fed for testing the false positives. On the other hand, to measure the true positives, we attach tags on a toy train which moves along an oval track in a constant speed $\left( 0 . 7 m / s \right)$ . The track illustrated in Fig. 9(b) has a decimeter of 1m. We collect traces for 5 minutes as training set before the train takes movements. The number of true positive rate equals the number of perceived motions divided by the total read times when the tag moves.

Metrics: We express the perception accuracy by using the Receiver Operating Characteristic (ROC) curve. The vertical axis of the ROC curve is the true positive rate (TPR) which is the total number of perceived true positives divided by the number of real positives in ground truth. The horizontal axis of the ROC curve is the rate of false alarms, e.g. false positive rate (FPR), divided by the number of negative events in ground truth.

The metric of sensitivity is defined as the absolute the ratio of RSS difference to the distance of two positions, formulated as follows:

$$
\text { Sensitivity } = \frac {\left| R S S _ {A} - R S S _ {B} \right|}{\sqrt {(X _ {A} - X _ {B}) ^ {2} + (Y _ {A} - Y _ {B}) ^ {2}}}
$$

where $R S S _ { A }$ and $R S S _ { B }$ are the strength values respectively collected from position $A ( X _ { A } , Y _ { A } )$ and position $B ( X _ { B } , Y _ { B } )$ . The unit is $R S S / m$ , namely, the strength changes (RSS) in unit distance (m).

The minimum perception displacement (MPD) is used as the second metric to measure the system sensibility. MPD is the distance from the position where tag is trained to the one that the tag is firstly perceived in motion,

Baseline: For comparison, we also employ other three methods to perform the evaluation.

(1) Localization. There are many localization methods proposed in the literature. We use the most popular one in RFID system, LANDMARC [2]. Its basic idea is to calculate the weighted average of the four nearest tags’ locations. The weights are determined by the RSS values. (2) The minimum variance (MV). In this method, the latest 50 strengths are buffered to dynamically compute the current mean value. If the new strength deviates from the mean over than a threshold, the tag is determined in motion. (3) Frame differencing based subtraction (FD-BS). The simplest method used for foreground segmentation in computer vision. The foreground is determined if the continuous two frame image difference is greater than a threshold.

# 5.3 Perception Similarity

Intuitively, the individual differentiation may incur different interference impacts. Can we use the interference impacts from one object to model the others? To answer this question, we let four persons independently impose interference on the strength. These persons’ weights and heights are $P _ { 1 } ( 7 4 . 5 k g , 1 7 3 c m )$ , P2(58.5kg, 164cm), P3(64kg, 170cm), and $P _ { 4 } ( 6 9 k g , 1 7 1 c m )$ . Fig. 11(a) plots the fitted probability densities of strength interfered by these four persons. Visual inspection shows that the four curves nearly have the same shape. All of them can be modeled by two Gaussian models. The only difference is that the individual Gaussian model has different weights. As discussed in Section 2, the weight of every individual Gaussian model in MoG is highly related to the time interval that the model takes effect. In our algorithm, the weight only affects the matching order rather than the result. Our experiment fully shows the interference object takes very limited impacts on the models.

Fig. 11(b) plots seven-hour data containing 57, 603 × 4 readings for a stationary tag collected by four antennas. In the figure, four histograms represent the strength statistics respectively collected by the four antenna $A 1 \ \sim \ A 4 .$ The scatter matrix illustrates the strength results collected by any two antennas. From the figure, we observe that either the strength readings from one antenna or the combination from any two antennas are highly clustered. There are little points beyond the clusters. Although the four antennas are deployed in a line and very close (interval of ∼ 30cm for each other), the shape of cluster exhibits a little difference. This shows the strength distribution depends on the space relationship between reader antennas and tags. It further validates our hypothesis that the Gaussian model can depict the tags’ positions is reasonable.

# 5.4 Perception Sensitivity

To verify the sensibility, we change the distance between the antenna and tags from 30cm to 300cm. The strength results are plotted in Fig. 12(a). In total, the curve decreases as the distance increases and the slope of the curve equals 0.25 approximately, which well follows the theory (Note that the RSS is the logscale presentation of power). On the other hand, we also calculate the sensitivity of any two points out of 30 points in the curve. The CDF of the sensitivity results are shown in Fig. 12(b). We observe that 50% sensitivity achieves about 7RSS changes and about 10% cases have 13RSS above changes in the unit distance. Correspondingly, the received powers have $5 \times \sim 2 0 \times$ difference because of the following equation.

$$
\frac {P _ {A}}{P _ {B}} = 1 0 ^ {\frac {1}{1 0} (1 0 \log P _ {A} - 1 0 \log P _ {B})} = 1 0 ^ {\frac {1}{1 0} (R S S _ {A} - R S S _ {B})}
$$

Such differences are so noticeable that any commercial device is able to detect them.

Considering the toy train, we can calculate its read positions according to the read time and the train’s speed. Fig. 10(a) plots the tracked strength along the track. We can see that the strength changes in a rather wide range (∼ 15RSS) even when the neighboring positions are very close. We think the tag’s orientation also contributes a lot to these changes during the movement, because it is a well-known fact that the orientation seriously affects the strength. The tag’s orientation is defined by the angle between reader and tags. Note that the tag orientation does not influence our approach because the stationary tag does not change its orientation. By contrary, it may help motion perception when the tag moves with the orientation changes.

To measure the sensitivity without orientation’ influence, we keep the tag orientation unchanged and move the tag deviating from the trained position. Fig. 10(b) shows the MPD in various directions where the antennas locate in the north. We can see that (1) the MPDs in different direction are not the same. (2) The directions between $( - 6 0 ^ { \circ } \ \sim \ 6 0 ^ { \circ } )$ are the most sensitive in which the average MPD equals 6cm. This is because the tag in our experimental room is closer to the west wall. The more complex environment introduces more potential propagation paths of signal, requiring more Gaussian models to describe. Obviously, the sensitivity decreases when more models are used, because the real motion may be mistakenly determined as being interfered. (3) The average MPD is 10cm, which means the motion can be perceived by the system as long as the tag moves away by 10cm. The result is rather hypersensitive.

![](images/6679fa16dec635254892e2e22bbd9a68c2ee14e3355c3100624f57c54281e2df.jpg)



(a) Tracked strength

![](images/97dc6b8706832a4064d43966278a40abc7d8871349acd1bd205e1312055927e8.jpg)



(b) MPD

![](images/bc79a7a0d1fa5c6ff1300d1ca08d33bb018ba057c485500f6f4060414ac5d842.jpg)



(c) Accuracy

Fig. 10. Perception sensitivity and accuracy. (a) The strength values tracked by a mobile train. (b) The MPDs shown in different directions does not keep same. (c) The accuracy comparison through ROC curves among different methods.   
![](images/90ab663be8f6d82357ce284e96aa7e2c20ce22ce7914f423295663c7adae9b75.jpg)



(a) Interference similarity

![](images/0ca7c3dfe7cb86c639611f51cd0b7b7d73231b09c2ab3ebbb854547c9cf670e2.jpg)  
(b) The strength scatter matrix

![](images/cd2d4d0755ff86a7958d180cb4a464e089284b900ac7caab249faf0bc24e2253.jpg)



(a) Strength vs. distance

![](images/7480ab8eaa9763dbd01f645885f2c73557ff41251becd968508479c79457755f.jpg)



(b) CDF of sensitivity   
Fig. 11. Perception similarity. (a) The figure plots the probability densities of strength interfered by four persons. (b) The figure plots sevenhour data for a stationary tag collected by four antennas.   
Fig. 12. Perception sensitivity. (a) The strength distribution over the distance. (b) The CDF of sensitivity calculated over mobile traces.

# 5.5 Perception Accuracy

In this section, we apply the four methods to data traces and measure their perception accuracy. The ROC curves by these methods are plotted in Fig. 10(c). We can see that any of strength changes enabled methods has a better performance compared with localization. In detail, given a FPR of 0.5%, MoG-BS achieves 92.34% TPR while FD-BS and MV respectively have 75.6% and 3% FPR. The accuracy of MoG-BS is far better than two others. The MV uses several of the latest strength history to predict the tag motion. However, when the tag moves in a regular mode like the train, its changes is easy to be hidden by the latest history. So there are two obvious steps in the figure. In the first step, the threshold is too large to detect the motion, but the motion is suddenly detected when the threshold drops to a special value. Being different with MV, FD-BS only uses the last one history strength, hence its accuracy is higher than MV from the beginning because it has ability to resist the regular motion. However, there exists an attack against FD-BS in that it is possible to find a movement way enabling the same strength changes in any two adjacent read positions. In this situation, FD-BS fails to detect the motion. MoG-BS conquers the above weakness because it learns from the environment instead of the tag’s current status. As long as the environment is unchanged, its perception accuracy always remains in a high level. LANDMARC is the worst method behaving as a random coin because its localization accuracy is around 2m but our movement is confined in 1m.

# 5.6 Perception Parameters

We also consider other three factors that may take impacts on the accuracy.

Impact of antenna power: The antenna power is a key parameter which determines the reader interrogation range. Fig. 13(a) plots the ROC curves under different power levels. We can see that the curves nearly have no difference when the power is higher than 31.5dBm. Surprised, the level of 30.5dBm has a better performance. This can be understood that the higher antenna power gives much more energy to the tag. Therefore the tag has more choices of propagation paths required more Gaussian distributions to model. Thus the tag with higher power is vulnerable to false negatives. But because the environment is not changed, the possible paths is fully discovered when the power reaches a specific level. In this situation, the ROC does not change any more regardless of power changes.

Impact of frame size: Fig. 13(b) illustrates the impact of frame size. From the figure, we see the larger frame size behaves better performance because the motion probability is much more reliable. However, the larger frame size prolongs the perception time. The appropriate frame size should be adopted according to requirement in practice.

Impact of Antenna Number: Fig. 13(c) plots the ROC comparison using different number of antennas. The experiment using more antennas has a better performance. This is easily understood because much higher dimension of strength gives a much more comprehensive surveillance.

# 6 RELATED WORK

Fine-grained RFID localization is the most related topic to ours. These work can be classified into three categories.

RSS based methods: Early work on RFID localization is based on RSS. The reference tags are deployed at known positions in advance and used their RSS to locate the target tags [2], [9], [10]. Shangguan et al. [9] study on the problem of tag order under mobile environment. Sen et al. [11] offers a new localization algorithm using the PHY layer information. Liu et al. [10] propose a novel localization approach that utilizes the interference to position the target. This kind of method cannot be used in our scenario for two reasons. First, there may be no space to attach the reference tags. For example, the consumers often check the goods in the air. Second, passive tags’ RSSs are vulnerable to the tag orientation, which is totally unknown ahead.

![](images/2b65ea209adb68c3ce80d78d2eecc9dea36b462835b1d0464eb5d22ff7360137.jpg)



(a) Impact of power

![](images/f65b3755112250c7a007e97fa5ff66f4f250149e7fd2cb3de06470b39253c7ac.jpg)



(b) Impact of frame

![](images/283161fa8da8d249f0ca3e2554509d82ef0c3b6ada38823146d6d6624539a375.jpg)



(c) Impact of antenna   
Fig. 13. Impacts of perception parameters. (a) Impacts of power. (b) Impact of frame size. (c) Impact of the antenna number.

Proximity based methods: This kind of method identify the tag’s locations as same as the that of antenna that interrogates its [3], [12]–[14]. Zhu et al. propose a fault-tolerant localization approach for RFID reader [3]. Asadzadeb et al. [12] combine a group of tags to tackle with the orientation issue and track human’s motion patterns. Their method barely used for our scenarios because it only support horizontal and vertical movement where freedom movements are not allowed. [13] matches tag count percentage patterns under different signal attenuation levels to a database of tag count percentages, attenuations and distances from the base station reader. The disadvantage of these methods are the dependence of dense antenna to narrow the localization, which is infeasible in practice. In addition, the perception sensitivity of these method is determined by the interrogation range, which is normally around 10m.

Phase based methods: State-of-the-art systems use antenna arrays or synthetic aperture radar (SAR) to extract AoA of an RF signal and can achieve a location accuracy on the order of tens of centimeters [15]–[22]. PinIt [15] employs a moved antenna to measure the multipath profiles of reference tags at known positions and locates the target tag. The technique of PinIt is further applied in robot object manipulation [16]. The merit of PinIt is able to locate tag in NLOS environment. However, it needs to deploy dense reference tags in advance. [17] borrows the technique of SAR to generate the holographic localization of passive tags with a mobile reader, while [18] uses Inverse SAR to locate mobile tags. Both of these methods require RF propagation through the line-of-sight (LOS), which is hard to be fulfilled in practice, like in supermarket.

Detection of missing tags: The existing work [12], [23]– [27] utilize the presence-or-absence fashion to monitor the tag’s situation. Tan [23] et al. is the first to address this problem. In practice, it is necessary to report the missing ones without collecting all tags, because the later must stay in the range by default. Li [24] et al. further study the issue but propose a deterministic algorithm which reduces the time by 88.9% more. Luo [25] et al. consider the energy perspective for battery-powered active tags when detecting the missing tags. Zheng [26] et al. presents a physical layer missing tag identification scheme which effectively makes use of the lower layer information and dramatically improves operational efficiency. Gong [27] et al. propose a accurate approximation scheme for large-scale RFID cardinality estimation. As stated before, our work has a futher fine-grained surveillence on the target.

Fast identification: Anti-collision is another important topic in RFID area which aims to conduct the fast identification [28]– [35]. Chen [28] et al. address the problem of collecting information from sensor-augmented tags. They use multi-hash to spread the transmission slots. Xie et al. consider how to efficiently identify tags on the moving conveyor [29]. Jeffery [30] et al. design a statistical method to clean the uncertain tag readings. Yang [31] et al. and Tang [32] et al. discuss how to improve the throughput by avoiding the reader collision. Yang [33] et al. introduce the fast identification in anti-counterfeiting for a batch of rfid tags. Liu [34] et al. presents a new method to conduct adaptive continuous ccanning in large-scale RFID systems.

Polling query: Assuming all tag IDs in the range are known in advance, these papers [36]–[39] design protocols of polling queries to identify concerned tags with no need to collect them all. Shen et al. is one of the earliest works abandoning collecting all tags but designing polling query to the target tags whose categories are popular [36]. Qiao et al. propose tag-ordering polling protocol that can reduce per-tag energy consumption by more than an order of magnitude [37]. Gong et al. [38] present batch authentication by informative counting. Shahzad and Liu extend the study and propose a new scheme for estimating tag population size called ART [40] . Their method is based on the average run-length of ones in the bit string.

Foreground segmentation: Detecting regions of change in multiple images of the same scene taken at different times is of widespread interest in computer vision [5], [8]. The basic adaptive model is used in [5]. Chris and Grimson [8] discuss modeling each pixel as a mixture of Gaussians and using an online approximation to update the model.

# 7 CONCLUSION

Real-time object surveillance is an important task in RFID system. Existing methods in RFID systems often employ presence or absence fashion to detect the tags’ motions, so they cannot meet motion detection requirement in many applications. In this paper, we offer an innovate approach to explore the tag motion through its backscattered signal changes. We believe this is a step forward in the area of real-time monitoring using RFID technique.

# ACKNOWLEDGEMENT

The research of Yunhao Liu is supported by the NSF China Major Program No. 61190110.

# REFERENCES

[1] M. Bouet and A. L. dos Santos, “Rfid tags: Positioning principles and localization techniques,” in IFIP Wireless Days, 2008.   
[2] L. Ni, Y. Liu, Y. Lau, and A. Patil, “Landmarc: indoor location sensing using active rfid,” Wireless networks, vol. 10, no. 6, pp. 701–710, 2004.   
[3] W. Zhu, J. Cao, Y. Xu, L. Yang, and J. Kong, “Fault-tolerant rfid reader localization based on passive rfid tags,” in Proc. of IEEE INFOCOM, 2012.   
[4] D. Dobkin, The RF in RFID: passive UHF RFID in practice, 2008.   
[5] C. Wren, A. Azarbayejani, T. Darrell, and A. Pentland, “Pfinder: Realtime tracking of the human body ,” IEEE Transactions on Pattern Analysis and Machine Intelligence, 1997.   
[6] N. Friedman and S. Russell, “Image segmentation in video sequences: A probabilistic approach,” in Uncertainty in Artificial Intelligence, 1997.   
[7] W. Hu, T. Tan, L. Wang, and S. Maybank, “A survey on visual surveillance of object motion and behaviors,” IEEE Transactions on Systems, Man, and Cybernetics, 2004.   
[8] C. Stauffer and W. E. L. Grimson, “Adaptive background mixture models for real-time tracking,” in Proc. of IEEE CVPR, 1999.   
[9] L. Shangguan, Z. Li, Z. Yang, M. Li, and Y. Liu, “Otrack: Order tracking for luggage in mobile rfid systems,” in Proc. of IEEE INFOCOM, 2013.   
[10] Y. Liu, Y. Zhao, L. Chen, J. Pei, and J. Han, “Mining frequent trajectory patterns for activity monitoring using radio frequency tag arrays,” IEEE TPDS, vol. 23, no. 11, pp. 2138–2149, 2012.   
[11] S. Sen, B. Radunovic, R. R. Choudhury, and T. Minka, “Spot localization using phy layer information,” in Proc. of MobiSys, 2012.   
[12] P. Asadzadeh, L. Kulik, and E. Tanin, “Gesture recognition using rfid technology,” Personal and Ubiquitous Computing, vol. 16, no. 3, pp. 225–234, 2012.   
[13] P. Wilson, D. Prashanth, and H. Aghajan, “Utilizing rfid signaling scheme for localization of stationary objects and speed estimation of mobile objects,” in Proc. of IEEE RFID, 2007.   
[14] J. Han, C. Qian, D. Ma, X. Wang, J. Zhao, P. Zhang, W. Xi, and Z. Jiang, “Twins: Device-free object tracking using passive tags,” in Proc. of IEEE INFOCOM, 2013.   
[15] J. Wang and D. Katabi, “Dude, where’s my card?: Rfid positioning that works with multipath and non-line of sight,” in Proc. of ACM SIGCOMM, 2013.   
[16] J. Wang, F. Adib, R. Knepper, D. Katabi, and D. Rus, “Rf-compass: robot object manipulation using rfids,” in Proc. of ACM MobiCom, 2013.   
[17] R. Miesen, F. Kirsch, and M. Vossiek, “Holographic localization of passive uhf rfid transponders,” in Proc. of IEEE RFID, 2011.   
[18] A. Parr, R. Miesen, and M. Vossiek, “Inverse sar approach for localization of moving rfid tags,” in Proc. of IEEE RFID, 2013.   
[19] P. V. Nikitin, R. Martinez, S. Ramamurthy, H. Leland, G. Spiess, and K. Rao, “Phase based spatial identification of uhf rfid tags,” in Proc. of IEEE RFID, 2010.   
[20] T. Liu, L. Yang, Q. Lin, Y. Guo, and Y. Liu, “Anchor-free backscatter positioning for rfid tags with high accuracy,” in Proceedings of IEEE INFOCOM, 2014.   
[21] J. Wang, D. Vasisht, and D. Katabi, “Rf-idraw: virtual touch screen in the air using rf signals,” in Proc. of ACM SIGCOMM, 2014.   
[22] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu, “Tagoram: Realtime tracking of mobile rfid tags to high precision using cots devices,” in Proc. of ACM MobiCom, 2014.   
[23] C. C. Tan, B. Sheng, and Q. Li, “How to monitor for missing rfid tags,” in Proc. of IEEE ICDCS, 2008.   
[24] T. Li, S. Chen, and Y. Ling, “Identifying the missing tags in a large rfid system,” in Proc. of ACM MobiHoc, 2010.   
[25] W. Luo, S. Chen, T. Li, and S. Chen, “Efficient missing tag detection in rfid systems,” in Proc. of IEEE INFOCOM, 2011.   
[26] Y. Zheng and M. Li, “P-mti: Physical-layer missing tag identification via compressive sensing,” in Proc. of IEEE INFOCOM, 2013.   
[27] W. Gong, K. Liu, X. Miao, and H. Liu, “Arbitrarily accurate approximation scheme for large-scale rfid cardinality estimation,” in Proc. of IEEE INFOCOM, 2014.

[28] S. Chen, M. Zhang, and B. Xiao, “Efficient Information Collection Protocols for Sensor-augmented RFID Networks,” in Proc. of IEEE INFOCOM, 2011.   
[29] L. Xie, B. Sheng, C. C. Tan, H. Han, Q. Li, and D. Chen, “Efficient tag identification in mobile rfid systems’,” in Proc. of IEEE INFOCOM, 2010.   
[30] S. R. Jeffery, M. Garofalakis, and M. J. Franklin, “Adaptive cleaning for RFID data streams,” in VLDB, 2006.   
[31] L. Yang, Y. Qi, J. Han, W. Cheng, and Y. Liu, “Shelving interference and joint identification in large-scale rfid systems,” IEEE Transactions on Parallel and Distributed Systems, vol. PP, no. 99, pp. 1–1, 2013.   
[32] S. Tang, J. Yuan, X.-Y. Li, G. Chen, Y. Liu, and J. Zhao, “Raspberry: A stable reader activation scheduling protocol in multi-reader rfid systems,” in Proc. of IEEE ICNP, 2009.   
[33] L. Yang, J. Han, Y. Qi, and Y. Liu, “Identification-free batch authentication for rfid tags,” in Proc. of ICNP, 2010.   
[34] H. Liu, W. Gong, X. Miao, K. Liu, and W. He, “Towards adaptive continuous scanning in large-scale rfid systems,” in in Proc. of IEEE INFOCOM, 2014.   
[35] S. Qi, Y. Zheng, M. Li, L. Lu, and Y. Liu, “Collector: A secure rfidenabled batch recall protocol,” in Proc. of IEEE INFOCOM, 2014.   
[36] B. Sheng, C. Tan, Q. Li, and W. Mao, “Finding popular categories for RFID tags,” in Porc. of ACM MobiHoc, 2008.   
[37] Y. Qiao, S. Chen, T. Li, and S. Chen, “Energy-efficient polling protocols in RFID systems,” in Proc. of ACM MobiHoc, 2011.   
[38] W. Gong, K. Liu, X. Miao, Q. Ma, Z. Yang, and Y. Liu, “Informative counting: fine-grained batch authentication for large-scale rfid systems,” in Proc. of ACM MobiHoc, 2013.   
[39] J. Lim, S. Kim, H. Oh, and D. Kim, “A designated query protocol for serverless mobile rfid systems with reader and tag privacy,” Tsinghua Science and Technology, vol. 17, no. 5, pp. 521–536, 2012.   
[40] M. Shahzad and A. X. Liu, “Every bit counts: fast and scalable rfid estimation,” in Proc. of ACM Mobicom, 2012.

![](images/0424df7389e134bb083b420da7793778e1e42ef90c7a5babc496bb24c979371e.jpg)



Lei Yang respectively received the B.S. degree from the School of Software and Ph.D. degree from the Department of Computer Science and Engineering at Xi’an Jiaotong, Shaanxi, China. He is currently a postdoc fellow in the School of Software at Tsinghua University, Beijing, China. His research interests include RFID, pervasive computing, network security, and smart home. He is a member of the IEEE and ACM.

![](images/716a9828215d0193d860db2904595c072d715d8b1d5fd4cd2f68dceac7e6b7d4.jpg)



Yi Guo received his B.E. degree of Electrical and Computer Engineering from Shanghai Jiao Tong University, Shanghai, China, in 2011. He is currently a Ph.D. student in Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include radio frequency identification (RFID) and pervasive computing. He is a student member of the IEEE and the ACM.

![](images/00f06945b985c1120406c8b86f4108a96cf083e449331ed354e13b262318918f.jpg)

Tianci Liu received the BS degree from the School of Sofware at Tsinghua University, China, in 2012. He is now a third year PhD student of School of Software at Tsinghua University, China. His research interests include RFID and sensor network, mobile sensing and computing. He is a student member of IEEE and ACM.

![](images/a9f3b630297fc175558302004e8144a4784516183cf2881fd145b2e8ccebdd76.jpg)



Cheng Wang received his PhD degree in Department of Computer Science at Tongji University in 2011. Currently, he is a research professor of Computer Science at Tongji University. His research interests include wireless networking, mobile social networks, and cloud computing.

![](images/53a6c4ec550c62fc82ca559c99b5cd558fe85ba231aa3cddf1cf4ff342f9b33f.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, USA, in 2003 and 2004, respectively. He is now Cheung Kong Professor and Dean of School of Software at Tsinghua University, China. Yunhao is also a member of Tsinghua National Lab for Information Science and Technology. His research interests include RFID and sensor network, the Internet and Cloud Computing, and

distributed computing. Yunhao is IEEE Fellow.