# ShopMiner: Mining Customer Shopping Behavior in Physical Clothing Stores with COTS RFID Devices

Longfei Shangguan∗§, Zimu Zhou†§, Xiaolong Zheng∗, Lei Yang∗, Yunhao Liu∗, Jinsong Han‡ ∗Tsinghua IoT Center and School of Software, Tsinghua University †CSE Department, Hong Kong University of Science and Technology ‡School of Electronic and Information Engineering, Xi’an Jiaotong University Email: {longfei, xiaolong, young, yunhao}@greenorbs.com, zzhouad@cse.ust.hk, hanjinsong@mail.xjtu.edu.cn

# Abstract

Shopping behavior data are of great importance to understand the effectiveness of marketing and merchandising efforts. Online clothing stores are capable capturing customer shopping behavior by analyzing the click stream and customer shopping carts. Retailers with physical clothing stores, however, still lack effective methods to identify comprehensive shopping behaviors. In this paper, we show that backscatter signals of passive RFID tags can be exploited to detect and record how customers browse stores, which items of clothes they pay attention to, and which items of clothes they usually match with. The intuition is that the phase readings of tags attached on desired items will demonstrate distinct yet stable patterns in the time-series when customers look at, pick up or turn over desired items. We design ShopMiner, a framework that harnesses these unique spatial-temporal correlations of time-series phase readings to detect comprehensive shopping behaviors. We have implemented a prototype of ShopMiner with a COTS RFID reader and four antennas, and tested its effectiveness in two typical indoor environments. Empirical studies from twoweek shopping-like data show that ShopMiner could achieve high accuracy and efficiency in customer shopping behavior identification.

# Categories and Subject Descriptors

H.4 [Information Systems Applications]: Miscellaneous

# Keywords

Shopping behavior, RFID, Backscatter communication

# 1. INTRODUCTION

Shopping behavior analysis is of great importance to understand the effectiveness of marketing and merchandising efforts [2, 18]. With deep shopping behavior data, retailers

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from Permissions@acm.org.

SenSys’15, November 1–4, 2015, Seoul, South Korea..

© 2015 ACM. ISBN 978-1-4503-3631-4/15/11 ...\$15.00.

DOI: http://dx.doi.org/10.1145/2809695.2809710

§: co-primary author.

can capture customers’ flavors, test new arrivals, and adjust marketing strategy to optimize brand profitability. Mining customer shopping behavior in online stores is easily achievable by analyzing the click streams and customer shopping carts [3, 10, 11]. However, retailers with physical stores still lack effective methods to identify comprehensive customer behaviors. The only information readily available to retailers is the sales history, which fails to reflecting customer behaviors before they check out, like how customers browse the store, which products they show interest in, and what products they match against. Therefore, it is essential to explore new ways to capture customer behaviors in physical stores.

Previous efforts have exploited video cameras to monitor customer shopping behaviors in clothing stores [22, 23, 24]. However, such methods require densely deployed cameras to capture human actions, and complicated computer vision to recognize and analyze arm motions. Furthermore, videobased methods are susceptible to non-line-of-sight (NLOS) visual channels in crowded clothing stores where people frequently move around to pick up or try on clothes. Another brunch of methods tracks customer routes in stores, with the goal of mining hot zones and popular products [17, 31]. For example, the more people traverse along a route, the higher attentions the items around this route gain. Unfortunately, these approaches fail to provide high-fidelity information that is specifically relevant to shopping behaviors, like product browsing, pick-up actions and clothes trying-on.

RFIDs are emerging as an essential component of Cyber Physical Systems (CPS). Many well-known garment manufacturers (e.g., Abercrombie & Fitch, Calvin Klein, Decathlon) adopt passive RFIDs for sales tracking and anticounterfeiting [30]. We envision the adoption of RFIDs will sweep the clothing market in near future, and in this paper, we explore the feasibility of mining customer behavior in physical clothing stores with RFID devices. By carefully analyzing the customer shopping process in clothing stores (Section 2), we abstract three basic behavior mining functionalities essential to retailers: discovering popular category, identifying hot items and excavating correlated items.

• Popular category represents the clothes frequently viewed by customers.Since customers pay more views on items that meet their tastes, popular category data reveal customers’ flavor, hence providing valuable information to retailers’ trading strategy.

• Hot items are the clothes frequently picked up or turned over by customers. Hot items reveal whether customers show deeper interest in items after their first glance.   
• Correlated items are the clothes that are frequently matched with or tried on together, which can facilitate retailers to infer customer shopping habits and adopt bundle-selling strategies to boost profit.

These comprehensive shopping data reflect what items the customers browse, which items they show interest in, and which items they match with. By jointly analyzing these three kinds of shopping data with readily available sales history, the physical retailer can acquire much deeper business value. For example, popular items with little trying-on (i.e., not hot) may indicate the designs of these items are not run of the mill, while the hot item with unsatisfying sales volume may suggests an unacceptable price, which indicates sales promotion or discount should be taken.

In this paper, we present ShopMiner that enables customer shopping behavior sensing using commercial off-theshelf (COTS) RFID devices. The basic principle is that the phase readings of tags attached on desired items demonstrate distinct yet stable patterns when customers look at, pick up, turn over, or match desired items. These patterns are viable for an accurate shopping behavior mining service in clothing stores. Specifically, customers are likely to stand still for a while in front of attractive items, and hence block the wireless links between reader antennas and attractive items. Therefore, the phase reading of popular tags show a distinct pattern from those unpopular ones (i.e., not viewed by customers). Similarly, the phase reading of hot tags will change dramatically when customers pick them up or turn them over, e.g., observing pictures on the face/real side. The correlated items are brought together by one customer, thus experiencing a similar moving trail and temporal phase changes.

ShopMiner’s design harnesses these unique spatial-temporal phase reading correlations. The key techniques of ShopMiner are a novel foreground/background segmentation scheme for popular category detection, a robust statistical model for hot item identification, and a clustering algorithm for correlated items excavation. We implement ShopMiner on COTS RFID devices including an ImpinJ R420 reader, four Yeon antennas model YAP-100CP and a set of Alien UH-F passive tags. We test ShopMiner’s performance in two scenarios. Experimental results show that ShopMiner can detect popular items with a True Positive Rate (TPR) of 92%, identify hot items with an accuracy of 94% and 87% for pick-up and turn-over, respectively, and achieve over 85% accuracy for correlate item excavation in multiple users case.

Contributions. (1) ShopMiner is a unified sensing framework. Although some previous works have explored RFIDbased shopping behavior sensing [5, 16], none have incorporated the three key factors that are essential to retailers, i.e., what items the customers browse, which items they show interest in, and which items they match with. (2) As a long-term running system, ShopMiner considers both computational intensity and storage overhead. We design a hierarchical architecture and a set of efficient algorithms for multistage customer behavior detection. (3) We implement ShopMiner on COTS RFID devices, and conduct comprehensive experiments in two shopping-like scenarios. Empirical studies show that ShopMiner achieves over 90% TPR for customer behavior detection.

![](images/205d63095db5eb3cdd90c0740e346588a923611790cd930b9c85afab849bbc5f.jpg)



(a)

![](images/782642047c6c8b4ebf5877acbb3cdc7a44b2ac28a7b961a5c1614cc002ca5fc8.jpg)



(b)

![](images/e68a0a8d1b9ddba3f29258581b37ef2544a90aa1f7a8def0a470746500f9c267.jpg)



(c)

![](images/84050d057c818a28d6c717a33c5a3f47fe09387362e0f693a2739f482df83fb3.jpg)



(d)   
Figure 1: (a): hanging out and staying still in front of the interested item; (b), (c): browsing the interested item; (d): matching and trying items on in the fitting room;

Roadmap. The rest of paper is organized as follows. Section 2 presents the scope of ShopMiner. We present the detailed design of ShopMiner in Section 3 and the system implementation in Section 4. In Section 5, we interpret the experiment methodology, followed by detailed performance evaluation. Section 6 reviews related work, Section 7 discusses the limitations and we conclude in Section 8.

# 2. SCOPE

We envision ShopMiner can be deployed in clothing stores to monitor customer behaviors during shopping without body instrument. Figure 1 shows the typical shopping process in clothing stores before customers check out. It contains the following steps: browsing items and standing still in front of the attractive items; examining interested items by picking them up or turning them over; unsling desired items and trying them on in fitting rooms. These three steps contain comprehensive data and can help to optimize the retailer strategies. For example, by counting which items are mostly viewed by customers, the retailer could find those popular categories; by identifying and counting which items are picked up or turned over, the retailer could find those hot items; while by detecting which items are frequently picked up together or matched with, the retailer could find implicit correlation among clothes hence adopting tie-in promotion.

# 3. DESIGN

In this section, we elaborate on the design and the processing flow of ShopMiner. Throughout this paper we assume each piece of clothes is attached with a passive tag.

# 3.1 Discovering Popular Category

Popular items are the clothes frequently viewed by customers. The more times an item is viewed by customers, the higher attention it gains. Such information may serve as the baseline to examine the success of new products. In addition, it can also capture the flavor changing of customers and further help to optimize the product designing.

# 3.1.1 Shadowing effect of human body

We explore RF signal changes of multiple tag-to-antenna links to discover those popular categories. As Figure 2(a) shows, when a customer stands still in front of an item, his/her body naturally blocks the line-of-sight (LOS) link between the reader antenna and the focused item. Accordingly, the links that pass through the human body will, on average, experience higher shadowing losses [15].

![](images/e90f8e6004e2464fe7523c6052f06dab55452729df69ad0705b8fccb2f88ffe3.jpg)



![](images/2d15dc30ca42b20e2094746e203cebab54ad1e9301acfc401d8509db2a186b07.jpg)



Figure 2: Illustration of popular zone discovering

As an illustrative measurement, we deploy 48 backscatter links in an office environment. The link topology is shown in Figure 2(b). We use a commercial RFID reader ImpinJ R420 with three directional antennas as the power source and the receiver to interrogate RFIDs. The antenna is placed 3 meters away from the items and 1.2 meters above the floor. We conduct the following measurement. One volunteer hangs out along the trail 01, stands still for about 8s to browse item 04, and then leaves away. We collect the phase trend along each link and explore their temporal dynamics.

Figure 3 plots the phase measurements of four tags in this measurement study, namely tag 04, 05, 06 and 07. In accordance with our analysis, we find that during the first 4s, the phase patterns of these four tags maintain in a different yet stable level, indicating a relative steady link state. Within the period of 4s to 12s, the phase trend of tag 04 changes to another stable level, manifesting that a blocker stands still in front of tag 04 and blocks its LOS link. During the last 6 seconds, the phase patterns of tag 05, 06 and 07 change sequentially, indicating that a blocker leaves away and blocks these tags’ LOS paths sequentially. The measurement result shows that the body shadowing effect holds potential for non-invasive popular category discovery.

# 3.1.2 Noise statistics

The wireless propagation channel is affected by both the body shadowing and the ambient dynamics. As an example in Figure 2(a), people stand near the clothing rack will create a new signal propagation path, leading to multi-path effect. In multi-path environments, small changes of a few multipath components, even outside of the backscatter communication area can impact the measured phase.

To model the multi-path effect on the phase dynamics, we ask three volunteers to walk back and forth along trail 01 and 02 for 10min. Over 20,000 phase readings are recorded from 48 backscatter links. We randomly choose five tags and explore their temporal dynamics. As Figure 4 shows, the phase values fluctuate continuously and form a Gaussian-like distribution. We further test the distribution of the five tags’ phases against the standard Gaussian distribution. The linearity of the points on the Q-Q plot, as shown in Figure $5 ,$ demonstrates that the data are normally distributed.

In a nutshell, both the body shadowing and the multipath effect will introduce temporal phase dynamics. The phase dynamics exerted by the multipath effect is relatively slight and follows Gaussian distribution, whereas the phase value changes significantly when the LOS path is blocked.

# 3.1.3 Detection scheme

To capture the items in popular category (termed as popular items), we are inspired by the foreground detection problem in image processing. This problem aims to capture the foreground pixels that show significantly different values between contiguous image frames. In the context of Shop-Miner, we need to distinguish the popular items that show remarkable phase changing from the temporal phase trend. The similarity between the two problems motivate us to design a foreground detection based scheme for popular items discovery. Without loss of generality, time is partitioned into consecutive windows.

![](images/fec52c2046fe0eb6381c8c7b8dc0749fc15e146e847fb495fe0b6e39381a21b0.jpg)



Figure 3: Illustration of phase trends of four tags   
![](images/e9d17af107cf95d16fdb2c585432ebfd403cd963a374c78309ccac30f4384112.jpg)



Figure 4: phase value distribution of five tags

Composing phase frame: ShopMiner first splits the phase trend into multiple phase frames. Each frame contains m $\times \ d$ pixels. m is the number of tags in the reading zone and d is the frame length. The pixel value $\boldsymbol { r } _ { i , j }$ is the phase reading of the $i ^ { t h }$ tag (t ) collected within the $j ^ { t h }$ window $( w _ { j } )$ . Since each tag will be interrogated multiple times within one window, their average value is regarded as the phase measurement of this tag in this window. We vary parameter settings and set |w| and d to 0.02s and 50, which empirically balance computational efficiency and detection granularity.

Foreground detection: After splitting phase trend into frames, ShopMiner analyzes pixel values in each frame line-by-line. Pixel values that do not fit the background distribution are considered foreground. Notice that the phase distribution of each tag shows a distinct Gaussian-like distribution. Hence, we create m Gaussian models, each corresponding to one tag. ShopMiner then examines each pixel by comparing its value against the corresponding distribution. Specifically, given a pixel value $\begin{array} { r } { r _ { i , j } , } \end{array}$ let $N _ { i } ( \mu _ { i } , \sigma _ { i } ^ { 2 } )$ be the Gaussian model of tag i. ShopMiner formulates the following hypothesis test with $H _ { 0 }$ foreground and $H _ { 1 }$ background:

$$
\left\{ \begin{array}{l} H _ {0}: r _ {i, j} \notin \left(\mu_ {i} \pm \frac {\sigma_ {i}}{\sqrt {k _ {i}}} \cdot z _ {\alpha / 2}\right) \\ H _ {1}: r _ {i, j} \in \left(\mu_ {i} \pm \frac {\sigma_ {i}}{\sqrt {k _ {i}}} \cdot z _ {\alpha / 2}\right) \end{array} \right. \tag {1}
$$

where $0 < \alpha < 1$ , and $k _ { i }$ is the sample size. $\displaystyle \left( \mu _ { i } \pm \frac { \sigma _ { i } } { \sqrt { k _ { i } } } \cdot z _ { \alpha / 2 } \right)$ stands for the confidence region with the confidence level $( 1 - \alpha )$ . For example, $H _ { 1 }$ under $\alpha = 0 . 0 5$ indicates that the pixel $( i , j )$ is foreground with 95% probability.

![](images/cc8b3e1cb63c940c4d678e54cf838c85b27cf6edf75e9fff3e21844e1d9f35e3.jpg)



(a) tag 03

![](images/118c0af28599686c271d311ed0a9fdd37be3602150c72eb51327dcb6bbb482c5.jpg)



(b) tag 05

![](images/d463bfd663837c68849a7b9ecc4c88a5a0b481d0c234171916e7de6fc42a86f7.jpg)



(c) tag 08

![](images/e882766e27caad6c3c1b124554a26276d9826dadd46781225a20e2bef4466314.jpg)



(d) tag 09

![](images/6187d15d0b812bc9beb8ef1883bae9824cdade15b04716483ee22b48434d23b6.jpg)



(e) tag 13

Figure 5: QQ Plot of sample data versus standard normal   
![](images/6af3e08232945f715dd043a63055e00cda7c58550801671b6b55ae9871b9dd69.jpg)



(a)

![](images/b7c7a6c115aad9d3f85bbe2f02ce992f9f506ffac414f9b5139345fbb6b39a3d.jpg)



(b)

![](images/0db7e94a6be4e7fae74e3a1e7c7b22872e3a06bdd2896355b7f15aa7160ee7ab.jpg)



(c)

![](images/74e32266e9a5abe14f6038127bf8688aa37c5e54c2252caef83405f0ed4b8674.jpg)



(d)   
Figure 6: (a): the sketch of experiment field; (b): pick-up case; (c): turn-over case; (d): the phase trend before/after de-periodicity;

Detecting popular category: In one frame, if the majority part of pixels in row i are detected as foreground (i.e., >80%), then it is highly possible that all links between tag t and reader antennas are blocked by human body. To this end, ShopMiner formulates the following hypothesis test with H0 popular category items and H1 unpopular category items:

$$
\left\{ \begin{array}{l} H _ {0}: s _ {i} \geq \theta \\ H _ {1}: s _ {i} <   \theta \end{array} \right. \tag {2}
$$

where si is the number of consecutive frames that the tag ti’s links are blocked by human body. θ denotes a pre-defined threshold. The rationale behind this detection scheme is that since customers naturally stand still for a while in front of popular items, the LOS links between these tags and antennas will retain blocked for some time. Such a thresholdbased method prunes those tags whose LOS links are unintentionally blocked by customers. Since the threshold is primarily determined by the signal variations incurred by human blockage of the LOS path, it is mainly affected by the link distance and is robust to ambient factors e.g. shop sizes, layouts and reader placements. According to our experiments, within the effective range of RFID readers (around 6m), a fixed threshold yields satisfactory detection performance and a pre-trained threshold can scale to other shops without per-shop calibration.

Model training and updating: To precisely detect the foreground, it is essential to have an accurate Gaussian model for each tag. Initially, the parameters of m Gaussian models are computed when there are few or no customers in the shop (e.g., before the opening or after the closing). Then pixel values of the background parts are inserted into the model and the model parameters get updated. By doing so, the model parameters are updated continuously, and hence adapt to the temporal environment dynamics.

ShopMiner is immune to the spatial disorder of items. This is because each clothing item is associated with a unique RFID tag and ShopMiner can pinpoint which item of clothing is actually blocked by referring the tag ID.

# 3.2 Identifying Hot Items

Hot items are those with greater interests to customers. The traditional way to identify hot items, e.g. the sales history, only considers the purchased items as hot, and provides partial information for retailer strategy changing. ShopMiner identifies the hot items by exploiting the phase changing caused by customer behaviors. Specifically, it detects and counts the following customer actions:

(1): Turn-over action: A customer observes an interested item by turning it over from the side-view to the front-view.   
(2): Pick-up action: A customer takes a close look at an interested item by picking it up from the clothing rack.

These two actions indicate different levels of human interest on items, and hence should be identified separately. It is understandable that customers often turn over the attractive item at first glance, and pick it up for a close browsing when they show greater interest to this item. Hence in ShopMiner, we detect and identify these two actions separately.

# 3.2.1 Exploiting the similarity of pick-up and turnover for action detection

We assume that customers will pick up or turn over one interested item every time. Both the turn-over and the pickup actions will alter the item state from stationary to kinetic. Consequently, the kinetic item will experience fierce phase changing that naturally separates them apart from other stationary items. As an illustrative experiment, we place five items of clothes on a rack and ask one volunteer to mimic the customer. In the first experiment, the volunteer is required to pick up item 05, have a close browsing, and then put it back. In the second experiment, the volunteer is required to turn over item 05 to see its front-face, hold it for a while and then loose her grasp. The phase trends of the five items are shown in Figure 6(b) and Figure 6(c), respectively.

We first look at the pick-up action. As Figure 6(b) shows, initially the phase trends of these five tags all remain stable. When the volunteer picks up item 05 at $4 ^ { t h }$ second, the phase trend of this item jumps abruptly until the volunteer put it back at the $1 2 ^ { t h }$ second. Similarly, as shown in Figure 6(c), when the volunteer turns over the item 05 at the $4 ^ { t h }$ second, the phase trend of this tag changes significantly. The phase trend then keeps stable during the period of [4s, 8s], indicating that it is held steadily by the volunteer. As the volunteer looses her grasp, the item will rapidly recover to its original position, leading to a fierce phase changing. The measurement indicates that it is possible to detect pick-up and turn-over actions by observing the phase trend of tags. That is, identifying whether a period of phase changing occurs.

![](images/9bb8509af0d1494e6bf34ba54b6e6cdeec6a46c75b818d8acc980d6306195746.jpg)  
Figure 7: (a): the original phase trends; (b): after segmentation; (c): after de-periodicity; (d): after normalization;

# 3.2.2 Exploiting the dissimilarity of pick-up and turnover for action identification

In clothing stores, it is common to see that clothes are hung compactly to each other on the rack, with their sideviews facing to customers (Figure 1). Consequently, when the customer picks up one item to have a close browsing, the nearby items will be struck unintentionally, hence experiencing a slight shaking. As a result, the phase trends of these items will demonstrate a minor yet different variation tendency to the desired item (like tag 01, 02 ,03 and 04 in Figure 6(b)). In contrast, when the customer turns over one item (say item 05) to see its front face, the items around this item will be forced to turn over as well, hence experiencing a similar motion trail as item 05. As a result, the phase trends of these items will show a similar tendency to tag 05 (like tag 01, 02 ,03 and 04 in Figure 6(c)). Therefore, it is viable to distinguish turn-over and pick-up actions by jointly considering the phase trend of nearby tags, i.e., comparing the similarity of their phase trends.

# 3.2.3 Identification scheme

Based on above analysis, we first design a segmentationbased pick-up/turn-over detection scheme. This scheme exploits the similarity of pick-up and turn-over actions, and can accurately report the occurrence of these two actions. Then a peer-assisted identification scheme is put forward to further distinguish these two actions.

Segmentation-based detection: ShopMiner performs segmentation on the phase trend to detect whether a pickup or turn-over action occurs. Denote the phase trend as $\\\dot { S ^ { \mathbf { \eta } } } = \left( s _ { i } \right) \in R ^ { 1 \times N }$ , where N is the discrete time point. Within each window, we categorize phase values into multiple bins, and get the discrete probability distribution function (PDF) of phase values within each window. Given two consecutive windows $w _ { i }$ and $w _ { j }$ , let $P$ and Q be their PDFs. We computes the KL-divergence of these two PDFs as follows:

$$
D _ {K L} (P | | Q) = \sum_ {i} P (i) \cdot l n \frac {P (i)}{Q (i)} \tag {3}
$$

The KL-divergence describes the similarity of phase trends within two consecutive windows. We denote the period when there is a pick-up or turn-over action as motion period. The remaining period is denoted as silent period. Within the silent period, the phase value will maintain in a relative stable level. Hence the KL-divergence of two consecutive windows within the silent period should be small. In contrast, if at least one window is within the motion period, the PDF of these two windows should be significantly different, which leads to a large KL-divergence value. ShopMiner checks $D _ { K L } ( P | | Q )$ to detect whether the current window is within the silent period. After finding all windows within the silent interval, we can extract the motion interval accordingly. Consequently, a tag with a motion interval indicates a pick-up or turn-over action occurs.

Improving the granularity: the segmentation-based scheme can successfully detect the pick-up and turn-over actions due to its sensitivity to phase dynamics. However, since both the pick-up and turn-over actions will introduce phase turbulence to nearby items. The phase trend of these items may vary as well and hence will be detected by the segmentation-based scheme. To demonstrate this, we invite one volunteer to perform take-up and turn-over actions on the clothing rack for 200 times, and we find that the false alarm rate breaks 40%. To improve the detection granularity, we exploit the statistical feature of the phase trend. It contains two steps: de-periodicity and variance comparison.

De-periodicity: The phase value reported by the reader API is a periodic function ranging from 0 to 2π. As a result, when the phase value decreases to 0, it will jump to 2π, and then decreases as usual (Figure 6(d)). We term this abrupt phase changing phenomenon as a phase hop. In ShopMiner, we adopt the method in [16] to handle the phase hop problem. The general idea is to add or subtract 2π on the phase value when the phase hop occurs. The phase trend before/after de-periodicity is shown in Figure 6(d).

Variance comparison: Suppose m tags are detected in the segmentation step. For each tag i, we denote its phase samples within the motion period as $S _ { i } = ( s _ { j } ) \in R ^ { \bar { 1 } \times N _ { i } }$ . $N _ { i }$ is the length of the sample group, and may vary from tag to tag due to the multi-path self-interference [38] and random access principle of ALOHA protocol. We thus split each sample group into N frames. The frame length is set to 0.1s. Since multiple samples may locate within a frame, we computes their average (denoted as $s _ { j } ^ { \prime } )$ , and use it as the phase value of this frame. Then we compute the variance of $S _ { i }$ as follows:

$$
V a r (S _ {i}) = \frac {1}{N} \sum_ {j = 1} ^ {N} (s _ {j} ^ {\prime} - \mu) ^ {2} \tag {4}
$$

![](images/deb9c6fd227a3d087b34cbce89e545f8ef7b3c832cc09157d89316ad3f0ad53b.jpg)



(a)

![](images/2020d40c98aedbfb1436bdf9cb3f1fd16e8fd82675241f32a51b0b4a13bcc573.jpg)  
(b)

![](images/9d32ab9a88ed22c5087636aad971671f98158862ca0a1c7383642fa639fc81b7.jpg)



(c)

![](images/24a6ea477a2c9780306b9cd0f3a9e4c49896e4c853c89aead786b245f554a936.jpg)



(d)   
Figure 8: (a): the customer moving trail; (b): the phase trends of correlated items; (c): the phase trends of stationary tags nearby; (d): the phase trends of another group of correlated items;

After computing the variance of each tag, the one with the highest variance is denoted as the desired tag. The rationale is as follows: the motion of nearby items is indirectly driven by the human action. The driven power will be absorbed by clothes and diminishes rapidly as it prolongs. As a result, the desired item will experience much higher turbulence than the undesired ones, and hence show a larger variance.

Peer-assisted Identification: After finding out the desired tag, the next step is to distinguish the customer action, i.e., pick-up or turn-over. Recall that the phase trend of nearby tags would demonstrate a similar variation for turn-over, yet behave differently for pick-up. Hence we exploit this dissimilarity for action identification. Specifically, for each of the m phase trends, we zoom out the local dissimilarity of phase samples by normalizing this phase trend (Figure 7(d)). After the normalization, we splice these m phase trends consequently into a single phase trend, say $\mathbf { \bar { \cal S } } = ( s _ { j } ) \in { \cal R } ^ { 1 \times N }$ . Then autocorrelation is performed on S:

$$
\chi (m, \tau) = \frac {\sum_ {k = 0} ^ {k = \tau - 1} [ s _ {m + k} - \mu (m , \tau) ] [ s _ {m + k + \tau} - \mu (m + \tau , \tau) ]}{\tau \cdot \sigma (m , \tau) \cdot \sigma (m + \tau , \tau)} \tag {5}
$$

where $\mu ( k , \tau )$ and $\sigma ( k , \tau )$ are the mean and standard deviation of the phase samples $< s _ { k } , s _ { k + 1 } , . . . , s _ { k + \tau - 1 } >$ , respectively. In our case, τ equals to the number of data samples within the motion period, and is known a prior. Generally, the phase trend S, if connected by k similar phase trends, should behave like a periodic signal, hence demonstrating a higher auto-correlation value. Therefore, we can ascertain whether the motion period is caused by turn-over by checking the autocorrelation coefficient as follows:

• if $\chi ( m , \tau ) \geq \delta$ , then action = turn-over ;   
• if $\chi ( m , \tau ) < \delta ,$ then action = pick-up;

We test various thresholds over 1,000 experiments in our shopping-like scenario, and find a unified threshold δ = 0.65 optimal for our case. This threshold is impacted by the layout of shops as well as link distance, hence should be calibrated for different shops. Note that reordering the item, which occurs frequently in retail stores, does not impact the detection performance, since ShopMiner does not rely on any sequence or position information of items for pick-up/turnover detection.

# 3.3 Excavating Correlated Items

Our correlation analysis aims to find the items that are usually tried on together, e.g., dress shirt and tie are usually

![](images/c4ad34ea8656bfe2aa450be2debbb4ad8ad0690b08e4af593509a1f3c94f5e01.jpg)



Figure 9: sketch of clustering procedure

tie-in together, while people buying suit pants often consider about the dress shoes. Previous effort [5] proposed an RSS-based localization technique for correlated item discovery, based on an intuition that correlated items held by the same person should be in close proximity. However, after scrutinizing this method in real-world applications, we find that such a method is error-prone due to the following two reasons. On the one hand, items around the customer may also be in close proximity to the items in hand, and hence will be mistaken as correlated items. On the other hand, the ambient environment of clothing stores is fast-changing. Customers block/generate signal propagation paths dynamically, hence dampening the resolution of localization-based scheme.

# 3.3.1 Spatial-temporal correlation of signal features

ShopMiner explores the spatial-temporal correlation of phase trends to discover those correlated items. The observation is that correlated items, either in hand or in the shopping bag, follow a similar moving pattern with the customer, hence experiencing consistent temporal signal changing.

As an illustrative measurement, a customer is asked to carry four pieces of clothes in hand and walks to the fitting room. The walking trail is shown in Figure 8(a). Figure 8(b) illustrates the temporal phase trend of these four items. All these four phase trends demonstrate a similar temporal pattern. Specifically, when the volunteer rotates from a to b, because the distance between the tag and antenna first increases and then decreases, the phase trend thus shows a symmetric profile. As the customer walks to c, the phase trend changes repeatedly within [0, 2π) and finally maintains in a stable value when the customer reaches c and stays for a while. On the other hand, comparing Figure 8(b) with Figure 8(c) and Figure 8(d), the tags within different category have diverse temporal phase profiles, which naturally separate them apart. The measurement validates the feasibility of using phase trend similarity for correlated item discovery.

# 3.3.2 Clustering correlated items

Given a set of phase trends $\left( x _ { 1 } , x _ { 2 } , . . . , x _ { n } \right)$ , our goal is to partition the n phase trends into m (m is unknown a prior and $m \leq n )$ sets $\mathbf { S } = \{ S _ { 1 } , S _ { 2 } , . . . , S _ { m } \}$ , such that the withincluster sum of squares is minimized:

$$
\underset {\mathbf {S}} {\operatorname{argmin}} \sum_ {k = 1} ^ {m} \sum_ {i, j \in S _ {k}} \mathcal {T} (x _ {i}, x _ {j}) \tag {6}
$$

where $\mathcal { T } ( x _ { i } , x _ { j } )$ is the distance between $x _ { i }$ and $x _ { j }$ . To solve this optimization problem, we design a heuristic algorithm which iteratively partitions tags into different categories.

We give a toy example to explain this algorithm. Figure 9 shows a running case where ten tags need to be classified. In the first iteration, the algorithm randomly picks one tag as the pivot (e.g., tag 01 in the example), and computes the distance between its profile with the remaining. Tags that are with sufficiently close proximity with the pivot are clustered together. The algorithm then randomly chooses another pivot and repeats this process on the unclassified tags until the within-cluster sum of squares is minimized. Once the algorithm terminates, we achieve the corresponding tag set.

Distance metric ${ \mathcal { T } } ( x _ { i } , x _ { j } ) { \mathrm { : } }$ in designing the distance metric, we are facing two crucial issues: the first is the phase trend inconsistency, which means that phase trends are with different length due to the fragile backscatter links and multi-path effect. The second issue is the interrogation time inconsistency, which indicates the phase values are sampled in different time slots due to the random access character of ALOHA protocol. To address these issues, we use the Dynamic Time Warping (DTW) metric [33] to measure the distance of phase trends. This metric allows two time series that are similar but locally out of phase to align in a non-linear manner, hence naturally addressing both the phase profile inconsistency and interrogation time inconsistency.

Addressing phase scaling challenge: a practical challenge arises when we try to directly apply DTW to compare phase trends: phase scaling due to the different position of tags. The phase value is proportional to the tag-to-antenna distance, which may vary a little bit from tag to tag within the same category. As we can see from Figure 8(b), Vshapes within these four tags are the scaled version to each other. This scaling problem could degrade the performance of DTW. To address this challenge, we employ a variant of the DTW algorithm called Derivative Dynamic Time Warping (DDTW) [9], which exploits the same principle of DTW yet uses the derivative of phase values as the input data. D-DTW can overcome the phase value difference in the Y-axis by working with the derivatives of phases where only the slope of phase matters and not the absolute values.

# 4. IMPLEMENTATION

In this section, we present the details of system implementation, and address several deployment issues.

# 4.1 Methodology

Hardware: we build a prototype using COTS UHF R-FID devices. Each item of clothes is attached with an Alien passive RFID tag model AZ-9634. An ImpinJ reader R420 and several Yeon antennas model YAP-100CP work as the receiver to energize these passive tags and collect readings. The reader is connected to a local server via an Ethernet cable. To minimize the influence of network latency, we time-stamp each tag reading by the reader’s local clock.

![](images/57436264dfbe4d68a4dd50e74ab2e659914e03519ebf225addcdaedcf0d5b435.jpg)



Figure 10: Workflow of ShopMiner

Software: we implement the software component of our system in Java. Figure 10 shows the workflow of our Shop-Miner system. At the lowest level is the data collection module, which is integrated with the Octane SDK and continuously interrogates the nearby tags to capture the phase readings, at a rate about 340 readings per second. The tag readings are grouped according to the tag ID (96bit or 128bit identifier) and stored in the local database. Initially, the data processing module fetches out the phase reading, and feeds them into the popular category discovery module. After discovering the popular items, ShopMiner collects their tag IDs and performs pick-up/turn-over detection on these tags. ShopMiner finally clusters these hot items to excavate the correlated items. The software runs on a Lenovo PC with an Intel Core i7-4600U 2.10GHz CPU and 8GB RAM.

# 4.2 Deployment issues

One deployment issue is to minimize the population of items for correlation analysis. In a large garment store, everyday hundreds of items would be picked up or turned over frequently. While the majority part of these items will be placed back directly without any trying on [32]. Essentially, these items do not belong to any category of correlated items, and hence could be filtered out a prior. In ShopMiner, only the tags satisfying the following two conditions will be considered as candidates for correlation analysis: 1): this item has been picked up or turned over; 2): this item is sequentially identified by different RFID readers (indicating the item is in motion). Such heuristic prunes a large portion of uncorrelated items and boosts the efficiency of correlation analysis.

Another deployment issue is to minimize data storage. In our system, the RFID reader periodically interrogates tags. Hence the acquired data accumulates gradually. Figure 11 shows a snapshot of the data volume augmentation when the RFID reader monitors 5 items in front. The data volume increases linearly with the time and rapidly accumulates to over 10Mb at the end of the 30th second. Suppose the system monitors 100 items in a small clothing stores. Then each hour it will generate at least 24G volume of data, which is intolerable for practical deployment. To reduce the data storage overhead, ShopMiner runs the popular category discovery module and hot item identification module in a real-time manner. Only those hot items will be taken into account and their data will be stored in the database for offline correlation analysis. We call this process as early data pruning. As Figure 11 shows, after the early pruning, ShopMiner introduces significantly lower storage overhead, which accumulates to 0.2Mb at the end of the 30th second. From a long-term view, the data volume would accumulate to about 480Mb of a one-hour monitoring duration for 100 tags, which is negligible compared to one-hour raw data volume. We admit that for large-scale shops, tag populations would be high and hence the data volume would accumulate rapidly. For this case, we recommend to perform offline correlation analysis each hour and discard accumulated data after each round of data analysis.

![](images/9c3916a7d18b089bda5eccaa3e8d8cda94c6f2023b238c89901e77e7fa9ef147.jpg)



Figure 11: the snapshot of data storage in ShopMiner   
![](images/785f335f4cf8836aadf05907c0f79143a0df58f09f41adc95c2bd55217f9b151.jpg)



Figure 12: Deployment of the prototype in the office/home environment

# 5. EVALUATION

In this section, we introduce the experiment scenario and detail the system performance. We keep two places of decimal of the experimental result throughout the evaluation part.

# 5.1 Scenario

We evaluate the performance of ShopMiner in two typical indoor environments: (a) an office room of 26×14 m2 and (b) a twin-bedroom apartment of $1 3 \times 9 \ : m ^ { 2 }$ . The layouts of these two rooms are shown in Figure 12. The office environment mimics the large-scale shopping square (e.g., H&M, Zara, Abercrombie & Fitch, etc.). We recruit 10+ volunteers to mimic customers that browse commodities here. The apartment environment mimics little clothing stores (e.g., private clothing stores), where less than 5 customers are asked to hang out there. In each testing environment, we hang 20 pieces of clothes on a clothing rack. The clothing rack is with 2 meters long and 1.4 meters high. The space of adjacent clothes is about 5cm. It should be noticed that the shopping behaviors studied in this work are general motions that the customer will perform in all kinds of retail stores, hence our scheme could adapt to other types of display configurations such as supermarket, stationary store etc.. The location of the clothing rack is denoted as the dashed squires in Figure 12. To evaluate the robustness of ShopMiner, we also test its performance with different item-to-customer distance and different number of nearby customers (shown in Figure 13).

![](images/37bbd14c3017f6fbe6b92e7afb6a2c304a978213cb821c558495bc7c2b679319.jpg)



Figure 13: Illustration of testing scenarios: including three item-to-customer distance settings ((a), (b), (c)) and three different number of customer settings ((d), (e), (f))

# 5.2 Popular category discovery

We first examine the impact of different parameter settings on the performance of popular category discovery. Then we test the system performance with a focus on its detection granularity and robustness. Granularity represents the minimum number of items that ShopMiner can detect when the customer stand still in front of an interested item. Robustness reflects the ability to resist outer changes without a significant decline in granularity.

# 5.2.1 Parameter configuration

Impact of confidence level (1-α): The confidence level (Equation 1) plays a key role in popular category discovery, and cannot be configured arbitrarily. To explore a proper confidence level, we vary α from 0.01 to 0.2, and calculate the true positive rates (TPR) and true negative rates (T-NR) of ShopMiner. TPR represents the fraction of cases where ShopMiner correctly identifies body shadowing events among all body shadowing events. TNR represents the fraction of cases where ShopMiner correctly identifies non-body shadowing events among all non-body shadowing events. We plot the TPR and TNR under various confidence level settings in Figure 14. ShopMiner achieves balanced TPR and TNR over 91% using a confidence level of 0.86. We thus use this threshold in the following experiments.

Impact of threshold θ: We further investigate the influence of threshold θ (Equation 2) on the system performance. In practice, if θ is too large, then ShopMiner will mistaken the browsing event as non-browsing case. For example, one customer stands still for a short time to browse the interested item, and then leaves away. On the contrary, if θ is too small, then ShopMiner will mistaken a large portion of non-browsing events as browsing event. e.g., customer walks slowly around the cloth rack and unintentionally blocks the LOS path between clothes and the antenna. We define the TPR as the fraction of cases where ShopMiner correctly identifies browsing event among all body browsing events; and TNR is the fraction of cases where ShopMiner correctly identifies non-browsing event among all non-browsing events. Figure 15 plots the TPR and TNR under a range of threshold settings. ShopMiner achieves a balanced TPR and TNR of over 92% using a threshold of 12s. We will use this threshold in the subsequent evaluations.

![](images/510eaf96661a5bb6572396b3d226ade9843ac034231e53c5ba317feaa868c95d.jpg)



![](images/31ae59b8b08981ea210f7a58070a33e24991bab3746cf744d0784e9c0144c6f3.jpg)



![](images/f0650faa31058996b689da3ca0d876a1b8797bd84331422783853d42d7d7a00d.jpg)



Figure 15: Impact of threshold γ   
Figure 16: Impact of different number of antennas

Figure 14: Impact of confidence level   
![](images/655ffd7b2e3da31d5f61be0246d100bc69bbcb5f811a06328b121a39e9164c75.jpg)



![](images/c4f1e2010249faad65c1cd9d3df4aaab284e50497c94699ceedb870fe4aa17bd.jpg)



![](images/4cb042f5db58773b5db83e218e7d45f919424a0c6be545a1d86eac99b5e24c89.jpg)



Figure 17: Impact of item-to- Figure 18: Impact of multiple cuscustomer distance tomers   
Figure 19: ROC curve

# 5.2.2 Overall Performance

Granularity: We vary the number of reader antennas and observe the granularity changing. In this experiment, a customer browses clothes and stands still in front of the interested ones (i.e., popular category). The distance between the customer moving trail and the clothing rack is 0.3m. We repeat the experiment 50 times under each antenna setting. Figure 16 depicts the relationship between the number of antennas and the detection granularity. The detection granularity is about 6 pieces of clothes on average with only one reader antenna. With more antennas, the detection granularity improves significantly and finally achieves 3.2 pieces of clothing on average when the reader antenna added to 4. Although such granularity fails to precisely reveal the specific item that the customer is browsing, it can remarkably narrow down the scope of candidates. Furthermore, as items with the same style are often hung closely together, hence such granularity can guarantee that ShopMiner identifies those clustered popular category of clothes. Based on the experiment result, we use four antennas in the following experiments.

Robustness: We first vary the distance between the clothing item and the customer (termed as item-to-customer distance) d from 0.2m to 0.6m, and examine how this distance affect the detection granularity. The antenna is put 2 meters away from the clothing rack. Figure 17 shows the result. As this figure indicates, the detection granularity decreases moderately as we expand the distance between the item and the customer. Specifically, when the customer is with close proximity to clothing items, e.g., d = 0.2m or 0.3m, the detection granularity maintains in a similar and fine-grained level, with the granularity of 2.5 and 2.9 pieces of clothes on average. As we increase d to 0.6m, the detection granularity drops to about 5 pieces of clothes on average. This may be because the customer blocks more LOS paths between the undesired items and the antenna, hence leading to much coarser detection granularity.

We also test the granularity of ShopMiner in multiple customer cases. In this trail of experiments, we arrange different number of customers to browse clothes simultaneously. The distance between the clothing rack and the customer is set to 0.3m. Figure 18 shows the detection granularity changing when different number of customers browse clothes simultaneously. As expected, when there is only one customer, ShopMiner achieves a relative good result, with a detection granularity of 3.2 pieces of clothes on average. As more customers get enrolled, e.g., n = 3, the detection granularity drops slightly to 5.3 pieces of clothes on average. This may be because more people will naturally block more LOS paths and introduce much complex multi-path reflections.

Summary: from the experiment result we can see that ShopMiner can detect the popular item with a TPR of 92%. The detection granularity degrades slightly with the variation of tag-to-antenna distance and number of customers. Besides, the result also indicates that the granularity can be improved by deploying more reader antennas.

# 5.3 Hot item identification

We test the accuracy and robustness of the hot item identification scheme based on the following metric: TPR and

Table 1: Confusion matrix of action identification 

<table><tr><td rowspan="2">Ground-truth</td><td colspan="2">Predicted</td></tr><tr><td>Turn over</td><td>Pick up</td></tr><tr><td>Turn over</td><td>187</td><td>13</td></tr><tr><td>Pick up</td><td>9</td><td>191</td></tr></table>

![](images/c29d97d77848660b551918c79734ad0a1ce8993b4e81b3f684ded8b2a48dc24b.jpg)



Figure 20: Impact of multiple customers

FPR. TPR is defined as the proportion of cases where Shop-Miner successfully detects the pick-up and turn-over actions among all pick-up and turn-over actions performed by the customer. FPR is defined as the proportion of cases where ShopMiner mistakes other actions as pick-up or turn-over actions over all non-pick-up and non-turn-over actions.

Accuracy: In this trail of experiments, we ask a volunteer to randomly pick up or turn over different clothing items 20 times. Other customers hang out around the clothing rack to generate multi-path propagation interferences. The experiment is conducted 20 times in total in two testing scenarios by 10 different customers. The ground-truth is captured by a video camera. We summarize the detection result by plotting the Receiver Operating Characteristic (ROC) curves in Figure 19. As the result indicates, ShopMiner achieves a better detection accuracy in pick-up case than that in turnover case. Specifically, we can see that ShopMiner acquires a balanced detection accuracy of 94% with a FPR of 13% for the pick-up case, and that of 87% with a FPR of 16% for the turn-over case. The primary reason of this performance gap may be because the phase turbulence of the desired item is much more significant than that of nearby items (unintentionally stricken by the desired item) in pick-up case, whereas the phase turbulence of the desired one is relatively similar to other nearby items in turn-over case.

We further investigate the identification accuracy of Shop-Miner. The confusion matrix is shown in Table 1. Each row here denotes the actual activity performed by the volunteer and each column represents the activity recognized by Shop-Miner. Each element in the matrix corresponds to the fraction of actions in the row that were regarded as the activity in the column. As the result shows, ShopMiner achieves a true positive rate of 94% and 96% for turn-over and pick-up action, respectively. The turn-over action is misclassified as pick-up action with 7% probability, while the pick-up action is often misclassified as turn-over action with 5% probability. The result clearly demonstrates that the auto-correlation based detection scheme can successfully distinguish pick-up and turn-over actions with high accuracy.

Robustness: To quantify the robustness of the detection scheme, we test its performance in multi-person cases and plot the ROC curves in Figure 20. As the result indicates, with one customer, ShopMiner achieves a balanced detection accuracy of 92% with a FPR of 13%. The detection accuracy decreases slightly with more customers, yet ShopMiner still achieves an accuracy of 85% with a FPR of 22% with three customers. This is expected since multiple customers will introduce complex signal propagation environment, which further introduces phase disturbance to each item.

Table 2: Confusion matrix of action identification 

<table><tr><td rowspan="3">Ground-truth</td><td colspan="6">Predicted</td></tr><tr><td colspan="3">Turn over</td><td colspan="3">Pick up</td></tr><tr><td>1</td><td>2</td><td>3</td><td>1</td><td>2</td><td>3</td></tr><tr><td>Turn over</td><td>187</td><td>184</td><td>178</td><td>13</td><td>16</td><td>22</td></tr><tr><td>Pick up</td><td>9</td><td>10</td><td>13</td><td>191</td><td>190</td><td>187</td></tr></table>

We further investigate the multi-person impact on the identification accuracy. Table 2 shows the identification result. As the confusion matrix indicates, the misclassification rate rises moderately with the increase of customer population. Specifically, when there are two customers performing pick-up or turn-over actions in front of the same clothing rack, ShopMiner achieves preeminent performance, with an average misclassification rate of 8% and 5% for turn-over and pick-up, respectively. This index increases slightly for the three customer case, and finally peaks 11% and 7% for the four customer case. This may be because when multiple customers turn over clothes on the same clothing rack, the clothes nearby the desired ones will be pushed by multiple customers. As a result, their phase trends will change irregularly in some cases, hence degrading the identification performance. Nevertheless, ShopMiner still achieves 89% and 94% TPR, demonstrating its potential for real deployment.

Summary: the result shows that ShopMiner achieves an overall detection accuracy of 94% and 87% for pick-up and turn-over cases, respectively. The TPR of action identification is 96% and 94% for pick-up and turn-over actions, respectively. Besides, the result also indicates that ShopMiner is insensitive to the variation of customer populations.

# 5.4 Correlated item excavation

We evaluate the performance of our iterative correlation detection scheme using the metric Detection accuracy. The detection accuracy is defined as the proportion of cases where ShopMiner correctly identifies correlated items over all correlated items.

Accuracy: We examine the detection accuracy under different number of correlated items. In this trail of experiments, we arrange one customer to bring different number of correlated items and hang out around the reader’s reading zone. The experiment is conducted 200 times by 10 different customers. We then use different distance metric (DTW and DDTW) for correlated item detection. Figure 21 shows the detection accuracies. As is shown, the detection accuracies using different distance metrics both decrease slightly with the increase of the number of correlated items. Specifically, when there are few customers (e.g., 1 or 2), the detection accuracy of ShopMiner retains around 91% and 83% for the DDTW and DTW distance metrics, respectively. With more customers, the performance gap of ShopMiner under different distance metrics becomes more significant, and finally peaks at 10%. It manifests that DDTW metric significantly improves the detection accuracy.

![](images/4074580d9189ef489b6774308c88cf1e6b239e16dca1a0b26c8302b2218b585b.jpg)



![](images/c8c2d2aa9828940fe9c27070fb7cb8380a072fd7b001e2877d759fcdda688166.jpg)



![](images/6fe82734dbcade0406ad52a9022dc54e2937854c9078cbd7d9cbf665f65fc10d.jpg)



Figure 21: # of items vs. detection Figure 22: Impact of customer-to- Figure 23: Impact of customer accuracy antenna distance populations

Robustness: We investigate the impact of the customerto-antenna distance on the detection accuracy. As shown in Figure 22, the distance between the customer and the antenna has little impact on the detection accuracy. Specifically, when the customer stands close to the antenna, e.g., 0.5m or 1m away, the detection accuracy retains above 90%. The detection performance then degrades slightly to over 88% when the customer is 2m away from the antenna. Hence with the increase of the distance between the customer and the antenna, there is no significant performance degradation. This result shows that our correlation detection scheme is insensitive to the customer-to-antenna distance.

We further examine the impact of customer population on the detection accuracy. In this trail of experiment, we arrange different number of customers to walk around, with each customer bringing different number of clothes. As shown in Figure 23, ShopMiner achieves an overall accuracy of 92% when there are three customers. The detection accuracy then decreases slightly with more customers. However, ShopMiner still achieves an detection accuracy over 85% with 11 volunteers. This result shows that ShopMiner is robust to customer population changes.

Summary: Experimental result shows that ShopMiner achieves an overall detection accuracy of over 93% with one customer, and that of over 85% with six customers. The result also indicates that ShopMiner is insensitive to the number of customers and the antenna-to-customer distance.

# 6. RELATED WORKS

Offline shopping behavior mining: Despite the academic and commercial success in online shopping data acquisition, relative few efforts have been paid on the offline shopping data acquisition. You et al. [37] discussed the usage of mobile phones to monitor shopping time at physical stores. Hagan et al. [20] proposed a solution on offline customer behavior collection by mounting the data collection device in the shopping cart. Kanda et al. [7] designed a sensor network based shopping behavior analysis system in retail stores, with the goal of tracking and clustering consumer locations, and further inferring the hot items. These solutions fail to provide high-fidelity information on offline shopping behaviors, such as how customers browse stores, and what items they show interest.

Wearable sensor based activity recognition: It is natural to use wearable sensors for human activity recognition. JigSaw [19] continuously monitored and classified user activities and infers context like walking, cycling and running. Swimmaster [1] provided a fine-grained assessment of swimming by extracting swimming parameters such as velocity, arm strokes, body balance, and body rotation. Researchers also employed wearable sensors for other kinds of human activity detection, such as smoking [21] and sleeping [4, 6].

Some research also explored detecting offline shopping behaviors with smart devices. Lee et al. [12] presented a smartphone based customer shopping behavior modeling framework, which aims to examine the impact of six kind of human activities on customer behaviors. Rallapalli et al. [26] proposed a solution on tracking physical browsing by customers in retail stores using the inertial sensors on smart glasses. Sen et al. [27] explored the possibility of using smartphone sensing data to detect pre-defined shopping activities in physical retail stores. These works can provide certain customer activity recognition services. However, these schemes require each user to wear a special hardware, which is burdensome and may degrade the shopping experience.

WiFi-based posture recognition: Researchers also exploit WiFi signal changes for device-free human activity sensing. WiSee [25] leveraged wireless signals to enable human gesture recognitions. AllSee [8] provided a gesturerecognition scheme that can operate on battery-free wireless devices. WiHear [34] designed a novel signal processing technique to detect human speaking from WiFi signals. Eeyes [35] extracted the CSI information from 802.11 symbols for in-home human activity sensing, like washing, watching, brushing teeth. While these techniques relieve users from wearable sensors, they suffer from environment dynamics, and hence cannot be deployed in physical stores for customer behavior monitoring.

RFID-based human/object sensing: Previous research also explored the signal changes of RFID tags for human or object sensing. OTrack [28] exploited the spatial-temporal correlation of RSS signals to track the tag order in baggage sorting system. STPP [29] designed a phase profiling technique for the relative localization of rfid tags in 2D space. Togoram [36] tracked mobile RFID tags within centimeter level accuracy by using the SAR and hologram technique. Our work is inspired by the above works in phase based tag motion detection. However, our focus is on leveraging the phase pattern to infer customer behaviors, rather than capturing the tag’s position. CBID [5] and Tagbooth [16] are the most related works to ours. CBID [5] exploited the Doppler effect on human actions to detect customer behavior in shopping malls. Tagbooth [16] used the RSSI patterns to detect and identify the pick-up motions in physical retail stores. Our work differs from these two works in two aspects. On the one hand, our system incorporates three key factors that are essential to retailers, i.e., what items the customers browse, which items they show interest in, and which items they match with. In contrast, CBID and Tagbooth could only observe and detect pick-up motions and infer those correlated items. On the other hand, our system solely adopts the phase patterns to mining the customer shopping behavior, whereas CBID and Tagbooth mainly rely on RSSI and doppler shift for customer behavior identification.

# 7. DISCUSSION

This section talks about the practical deployment issues.

Distinguishing employee/customer: the current Shop-Miner prototype mostly aims at clothing stores in a selfservice/supermarket mode, where few employees are expected to continuously put products back in shelves and where customers are free to pick up and try on the items as wished. For retail stores with employees guiding customers or frequently putting products back in place, ShopMiner may experience severe interference since ShopMiner is unable to distinguish employees and customers via RF signals. A partial solution is to ask each employee to attach an RFID tag with special ID so that ShopMiner can simply discard the phase readings if the special ID is detected.

Deployment Cost for Full Coverage: mainstream commercial RFID readers can now support 4 antennas with each antenna effectively covering an area of 4m x 4m square. Hence the retailer can monitor nearly an area of nearly 602 with one reader, which costs less than 1000 USD. In addition, retailers are more interested in the shopping behaviors of some items (e.g. new products) than others (e.g. items on sale). Therefore, full radio coverage might be necessary only for certain important regions in the stores. According to our survey on a local clothing stores in Xi’an, another practical deployment concern comes from the placement of the readers, whether the four-antenna readers of relatively large size can be fixed on walls or ceilings without violating the decoration styles of the stores.

Impact of Crowded Stores: in our clothing store like evaluation, ShopMiner retains satisfactory performance (detection granularity of 5.3 pieces of items, hot item identification accuracy of 85%, and correlated item identification accuracy of 92%) when monitoring 3 customers browsing 1 rack simultaneously using 1 reader. According to our survey on two local clothing stores in Xi’an, it is sufficient to support 3-5 customers per rack most of the time, especially for those expecting pleasant user experience. In our clothing store like evaluation, ShopMiner retains satisfactory performance when monitoring 3 customers browsing one rack simultaneously. As customers standing still or walking in the shops close to the rack can partially alter the multipath propagations of the target customer, the phase profiles will experience slight fluctuations. Consequently, ShopMiner only mis-detects a customer when other customers occasionally block the LOS path of the target customer. However, since close presence of many customers can severely affect the RF signals and create complex multipath propagation environments of the targeted customer, the performance of ShopMiner can degrade dramatically in crowded stores, e.g. when it is Christmas sale.

Extending Beyond Clothing Stores: on one hand, the current ShopMiner prototype can be extended to some types of retail stores e.g. bookstores, where the items are of similar material, and are relatively tidily placed. On the other hand, RFID tags attached on metal products can experience severe radio interference, which can lead to failure of ShopMiner. It is also difficult to even attach an RFID tag on certain products, e.g. fruits. Hence the current version of ShopMiner may be inapplicable in computer stores and part of the grocery stores.

# 8. CONCLUSION

In this paper, we present the design, implementation and evaluation of ShopMiner, a RFID-based customer shopping behavior mining system works in physical clothing stores. By attaching each clothing item with a RFID tag, ShopMiner could “see” and detect how customers browse the stores, which category of items they show interest, and which items they match with. Such comprehensive shopping behavior data could benefit retailers in capturing customers’ flavors, testing new arrivals, and further optimizing their commercial strategies. We examine the accuracy and robustness of ShopMiner in various testing scenarios. The preliminary result shows that ShopMiner could achieve high accuracy and efficiency in customer shopping behavior identification, hence hold potential for practical deployment.

# 9. ACKNOWLEDGEMENT

We would like to thank the anonymous reviewers and our shepherd, Ms.Lama Nachman, for providing valuable comments. This work is supported in part by the NSFC Major Program 61190110, the national high technology research and development program of China (863 Program) under Grant No.2013AA014601, NSFC General Program NO.61572282 and No.61572396, Hong Kong RGC Grant HKUST16207714, and China Postdoctoral Science Foundation funded project under NO. 2015M570100.

# 10. REFERENCES

[1] M. B¨achlin, K. F¨orster, and G. Tr¨oster. Swimmaster: A wearable assistant for swimmer. In Proceedings of the 11th International Conference on Ubiquitous Computing, UbiComp ’09, pages 215–224, 2009.   
[2] D. R. Bell and J. M. Lattin. Shopping behavior and consumer preference for store price format: Why ”large basket” shoppers prefer edlp. Marketing Science, 17:66–88, 1998.   
[3] Y. H. Cho, J. K. Kim, and S. H. Kim. A personalized recommender system based on web usage mining and decision tree induction. Expert systems with Applications, 23(3):329–342, 2002.   
[4] W. Gu, Z. Yang, L. Shangguan, W. Sun, K. Jin, and Y. Liu. Intelligent sleep stage mining service with smartphones. In Proceedings of the 2014 ACM International Joint Conference on Pervasive and Ubiquitous Computing, UbiComp ’14, pages 649–660, 2014.   
[5] J. Han, H. Ding, C. Qian, D. Ma, W. Xi, Z. Wang, Z. Jiang, and L. Shangguan. Cbid: A customer behavior identification system using passive tags. In Proceedings of the 2014 IEEE 22Nd International Conference on Network Protocols, ICNP ’14, pages 47–58, 2014.   
[6] T. Hao, G. Xing, and G. Zhou. isleep: Unobtrusive sleep quality monitoring using smartphones. In

Proceedings of the 11th ACM Conference on Embedded Networked Sensor Systems, SenSys ’13, pages 4:1–4:14, 2013.   
[7] T. Kanda, D. F. Glas, M. Shiomi, H. Ishiguro, and N. Hagita. Who will be the customer?: A social robot that anticipates people’s behavior from their trajectories. In Proceedings of the 10th International Conference on Ubiquitous Computing, UbiComp ’08, pages 380–389, 2008.   
[8] B. Kellogg, V. Talla, and S. Gollakota. Bringing gesture recognition to all devices. In Proceedings of the 11th USENIX Conference on Networked Systems Design and Implementation, NSDI’14, pages 303–316, 2014.   
[9] E. J. Keogh and M. J. Pazzani. Derivative dynamic time warping. In SDM, pages 5–7, 2001.   
[10] R. Kohavi, N. J. Rothleder, and E. Simoudis. Emerging trends in business analytics. Communications of the ACM, 45:45–48, 2002.   
[11] J. Lee, M. Podlaseck, E. Schonberg, and R. Hoch. Visualization and analysis of clickstream data of online stores for understanding web merchandising. In Applications of Data Mining to Electronic Commerce, pages 59–84. 2001.   
[12] S. Lee, C. Min, C. Yoo, and J. Song. Understanding customer malling behavior in an urban shopping mall using smartphones. In Proceedings of the 2013 ACM Conference on Pervasive and Ubiquitous Computing Adjunct Publication, UbiComp ’13 Adjunct, 2013.   
[13] Z. Li, W. Chen, C. Li, M. Li, X.-Y. Li, and Y. Liu. Flight: Clock calibration using fluorescent lighting. In Proceedings of the 18th Annual International Conference on Mobile Computing and Networking, Mobicom ’12, 2012.   
[14] Z. Li, W. Du, Y. Zheng, M. Li, and D. Wu. From rateless to hopless. In Proceedings of the 16th ACM International Symposium on Mobile Ad Hoc Networking and Computing, MobiHoc ’15, 2015.   
[15] Z. Li, Y. Xie, M. Li, and K. Jamieson. Recitation: Rehearsing wireless packet reception in software. In Proceedings of the 21th Annual International Conference on Mobile Computing and Networking, Mobicom ’15, 2015.   
[16] T. Liu, L. Yang, X.-Y. Li, H. Huang, and Y. Liu. Tagbooth: Deep shopping data acquisition powered by rfid tags. In Proceedings IEEE Conference on Computer Communications, INFOCOM’15, 2015.   
[17] Y. Liu, Y. Zhao, L. Chen, J. Pei, and J. Han. Mining frequent trajectory patterns for activity monitoring using radio frequency tag arrays. IEEE Transactions on Parallel and Distributed Systems, 23(11):2138–2149, 2012.   
[18] G. L. Lohse, S. Bellman, and E. J. Johnson. Consumer buying behavior on the internet: Findings from panel data. Journal of interactive Marketing, 14:15–29, 2000.   
[19] H. Lu, J. Yang, Z. Liu, N. D. Lane, T. Choudhury, and A. T. Campbell. The jigsaw continuous sensing engine for mobile phone applications. In Proceedings of the 8th ACM Conference on Embedded Networked Sensor Systems, SenSys’10, pages 71–84, 2010.

[20] T. P. O’hagan and C. E. Lewis. Shopping cart mounted portable data collection device with tethered dataform reader, 1998. US Patent 5,821,513.   
[21] A. Parate, M.-C. Chiu, C. Chadowitz, D. Ganesan, and E. Kalogerakis. Risq: recognizing smoking gestures with inertial sensors on a wristband. In Proceedings of the 12th annual international conference on Mobile systems, applications, and services, MobiSys’14, pages 149–161, 2014.   
[22] E. M. Pereira, J. S. Cardoso, and R. Morla. Motion flow tracking in unconstrained videos for retail scenario. In Pattern Recognition and Image Analysis, pages 340–349. 2013.   
[23] M. Popa, A. K. Koc, L. J. Rothkrantz, C. Shan, and P. Wiggers. Kinect sensing of shopping related actions. In Constructing Ambient Intelligence, pages 91–100. 2012.   
[24] M. Popa, L. Rothkrantz, Z. Yang, P. Wiggers, R. Braspenning, and C. Shan. Analysis of shopping behavior based on surveillance system. In Proceedings of IEEE International Conference on Systems Man and Cybernetics, SMC’10, pages 2512–2519, 2010.   
[25] Q. Pu, S. Gupta, S. Gollakota, and S. Patel. Whole-home gesture recognition using wireless signals. In Proceedings of the 19th annual international conference on Mobile computing & networking, MobiCom’13, pages 27–38, 2013.   
[26] S. Rallapalli, A. Ganesan, K. Chintalapudi, V. N. Padmanabhan, and L. Qiu. Enabling physical analytics in retail stores using smart glasses. In Proceedings of the 20th Annual International Conference on Mobile Computing and Networking, MobiCom ’14, 2014.   
[27] S. Sen, D. Chakraborty, V. Subbaraju, D. Banerjee, A. Misra, N. Banerjee, and S. Mittal. Accommodating user diversity for in-store shopping behavior recognition. In Proceedings of the 2014 ACM International Symposium on Wearable Computers, ISWC ’14, 2014.   
[28] L. Shangguan, Z. Li, Z. Yang, M. Li, and Y. Liu. Otrack: Order tracking for luggage in mobile rfid systems. In Proceedings IEEE Conference on Computer Communications, INFOCOM’13, pages 3066–3074, 2013.   
[29] L. Shangguan, Z. Yang, A. X. Liu, Z. Zhou, and Y. Liu. Relative localization of rfid tags using spatial-temporal phase profiling. In 12th USENIX Symposium on Networked Systems Design and Implementation, NSDI’15, pages 251–263, 2015.   
[30] T. Staake, F. Thiesse, and E. Fleisch. Extending the epc network: the potential of rfid in anti-counterfeiting. In Proceedings of the 2005 ACM symposium on Applied computing, pages 1607–1612, 2005.   
[31] L.-A. Tang, Y. Zheng, J. Yuan, J. Han, A. Leung, C.-C. Hung, and W.-C. Peng. On discovery of traveling companions from streaming trajectories. In Proceedings of 28th International Conference on Data Engineering, ICDE’12, pages 186–197, 2012.   
[32] M. Uzan. Consumers online and offline shopping behavior. 2014.

[33] T. K. Vintsyuk. Speech discrimination by dynamic programming. Cybernetics and Systems Analysis, 4(1):52–57, 1968.   
[34] G. Wang, Y. Zou, Z. Zhou, K. Wu, and L. M. Ni. We can hear you with wi-fi! In Proceedings of the 20th annual international conference on Mobile computing and networking, MobiCom’14, pages 593–604, 2014.   
[35] Y. Wang, J. Liu, Y. Chen, M. Gruteser, J. Yang, and H. Liu. E-eyes: device-free location-oriented activity identification using fine-grained wifi signatures. In Proceedings of the 20th annual international conference on Mobile computing and networking, MobiCom’14, pages 617–628, 2014.

[36] L. Yang, Y. Chen, X.-Y. Li, C. Xiao, M. Li, and Y. Liu. Tagoram: real-time tracking of mobile rfid tags to high precision using cots devices. In Proceedings of the 20th annual international conference on Mobile computing and networking, MobiCom’14, pages 237–248, 2014.   
[37] C.-W. You, C.-C. Wei, Y.-L. Chen, H.-H. Chu, and M.-S. Chen. Using mobile phones to monitor shopping time at physical stores. Proceedings of IEEE Pervasive Computing, 10(2):37–43, 2011.   
[38] P. Zhang, J. Gummeson, and D. Ganesan. Blink: A high throughput link layer for backscatter communication. In Proceedings of the 10th international conference on Mobile systems, applications, and services, MobiSys’12, pages 99–112, 2012.