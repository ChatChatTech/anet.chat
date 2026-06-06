# Embracing Spatial Awareness For Reliable WiFi-based Indoor Location Systems

Jingao Xu\*, Zheng Yang\*, Hengjie Chen\*, Yunhao Liu\*†, Xiancun Zhou‡, Jianbo Li§, Nicholas Lane¶

\*Tsinghua University and BNRist, Beijing, China

$^{\dagger}$ Michigan State University

$^{\ddagger}$ West Anhui University, China

$^{§}$ Qingdao University, China

Bell Labs, United Kingdom(Great Britian)

Email: {xujingao13, hmilyyz, chenhengjie13, yunhaoliu}@gmail.com

zhouxcun@126.com, lijianbo@188.com, niclane@acm.org

Abstract—Indoor localization gains increasingly attentions in the era of Internet of Things. Among various technologies, WiFi-based systems that leverage Received Signal Strengths (RSSs) as location fingerprints become the mainstream solutions. However, RSS fingerprints suffer from critical drawbacks of spatial ambiguity and temporal instability that root in multipath effects and environmental dynamics, which degrade the performance of these systems and therefore impede their wide deployment in real world. Pioneering works overcome these limitations at the costs of ubiquity as they mostly resort to additional information or extra user constraints. In this paper, we present the design and implementation of ViViPlus, an indoor localization system purely based on WiFi fingerprints, which jointly mitigates spatial ambiguity and temporal instability and derives reliable performance without impairing the ubiquity. The key idea is to embrace the spatial awareness of RSS values in a novel form of RSS Spatial Gradient (RSG) matrix for enhanced WiFi fingerprints. We devise techniques for the representation, construction, and comparison of the proposed fingerprint form, and integrate them all in a practical system, which follows the classical fingerprinting framework and requires no more inputs than any previous RSS fingerprint based systems. Extensive experiments in different environments demonstrate that ViViPlus significantly improves the accuracy in both localization and tracking scenarios by about 30% to 50% compared with five state-of-the-art approaches.

# I. INTRODUCTION

Wireless indoor localization has attracted significant research interests from both academia and industrial sides due to the popularity of mobile and ubiquitous computing. Among various solutions based on technologies like RFID [1], [2], visual images [3], and inertial sensors [4], etc, WiFi-based localization systems have been widely studied and deployed as one of the most promising solution for ubiquitous indoor localization [5]–[12]. Built upon widely deployed WiFi infrastructure, WiFi-based localization systems usually employ the easily accessible Received Signal Strengths (RSSs) as location fingerprints. As a result, these systems are free of extra hardware or dedicated equipment, rendering them especially attractive for commercial and pervasive deployment. In addition to a number of start-up productions, RSS fingerprint based method has been incorporated in the positioning services of great companies like Google, Apple, Cisco, Huawei, and Baidu, etc.

Fingerprint-based approaches generally consist of two stages. In the first training phase, RSS fingerprints are collected with location labels by site survey to form a fingerprint database (a.k.a radio map). Then during the localization stage, a user is located by matching his/her fingerprint observation against the fingerprint database. Despite of extensive research, however, this technology has not yet stepped in the prime time for wide deployment. Leading companies like Google and Baidu only integrate indoor map services in sporadic areas like large malls, airports and museums. The primary hurdles are two-folds: expensive training efforts of site survey and unreliable accuracy. While the former has recently been efficiently addressed by crowdsourcing-based approaches [6], [8], [10], [13], [14], the unstable accuracy still remains a critical drawback to its widespread adoption [15].

Fingerprint based systems assume that RSS fingerprints are spatially unique and temporally stable for a specific location and thus could be leveraged as location fingerprints. Due to inherent wireless signal properties, however, RSS values suffer from severe uncertainty especially in complex indoor environments on account of multipath effects and environmental changes, which dramatically impair the spatial uniqueness and temporal stability. The resulted effects on RSS fingerprints are two folds: 1) spatial ambiguity: fingerprints from distinct locations may be similar and thus fingerprint mismatches would happen among distant locations; and (2) temporal instability: location fingerprints would vary over time, deviating from and therefore failed to match the initially collected ones. Spatial ambiguity is recognized as the root cause of large errors [3], [9] and may lead to large location errors of even up to ten meters [15]. Temporal instability further leads to gradually deteriorated performance over time [16]–[18]. In a nutshell, both of them degrade the performance of RSS fingerprinting and further prevent it from practical deployment.

Many pioneers have been addressing the above spatial and temporal shortcomings of RSS fingerprints. Major efforts usually overcome the spatial ambiguity by leveraging: 1) user mobility: Fingerprint ambiguity is reduced by user mobility, either by eliminating less likely candidates with inertial sensor hints [4], [19], or by constructing mobile forms of fingerprints that combine subsequent measurements along user movements [20]–[22]; 2) extra ranging: Eliminating spatial ambiguity by geometry constraints gathered from acoustic ranging [9] or spatial images [3]; Or 3) CSI: To avoid the drawbacks of RSS, some efforts are made to exploit physical layer information such as Channel State Information (CSI) for localization. Regarding temporal variations, periodic re-calibration should be applied to the fingerprint database, either by reconstruction or self-adaptation $[16]$ , $[17]$ , $[23]$ . Despite of the performance gains achieved, these methods also cause one or more of the following pains that hamper the superior ubiquity of fingerprint-based systems: 1) Require accurate user mobility, which is difficult to obtain by erroneous smartphone built-in sensors, and cannot locate a stationary user; 2) Impose constraints on user behaviors of moving and/or using smartphones; 3) Rely on intentional cooperation among multiple users; 4) Introduce extra information inputs beyond RSS measurements, such as digital floorplan, inertial data, images, etc, some of which are even not readily accessible from smartphones.

In this paper, we present the design and implementation of ViViPlus, an indoor localization system purely based on WiFi fingerprints, which jointly mitigates spatial ambiguity and temporal instability and derives reliable performance without the aforementioned limitations. The key intuition is to embrace the spatial awareness of RSS values for enhanced WiFi fingerprint representation. In particular, the spatial relationships among the RSSs of one AP at multiple neighbouring locations tend to be more robust than individual RSS values from one single location. In ViViPlus, we propose RSS Spatial Gradient (RSG) for fingerprinting, which depicts the RSS differences among a set of selected nearby locations. As a spatially relative form, RSG matrix can better mitigate the fingerprint ambiguity due to multipath fading, as well as temporal variations due to temporal dynamics like environmental changes, AP power adjustment, etc. For example, if one AP adjusts its transmission power, the RSS values observed at several selected adjacent locations would suffer identical or similar changes, keeping the corresponding RSG less affected or unaffected.

ViViPlus's design follows the classical fingerprinting framework and requires no more inputs than any previous RSS fingerprint based systems. Translating the intuitive idea into a practical system, three challenges reside. 1) How to represent an effective fingerprint form based on RSG? The key is to formulate a form that is compatible with traditional RSS fingerprint database. We define an RSG Matrix for each location. Each row in the matrix depict the RSG profile of one AP among several neighbouring locations. To obtain an optimal matrix, we carefully select a subset of neighbouring locations to form a reliable RSG profile. 2) How to construct such an RSG matrix based fingerprint for a single query? The construction of RSG matrix needs RSS observations from multiple locations. However, in typical scenarios, a user only reports one single measurement from one location (or at most a sequence of measurements along a path for a moving user). Our trick is to reuse the data of a current candidate location to construct a query RSG matrix. By doing this, the RSG matrix would be similar to the candidate's if they come from the same location, and largely deviate from each other if not. 3) How to efficiently compare and match RSG matrix based fingerprints for localization? Instead of comparing two matrices row-by-row, we conduct fingerprint comparison in a global way by extracting and matching the matrix features.

![](images/4405b732557413c7a235a6d41f0d7b63c6e33b1ccd7614fc143d2094b7b4b8e8.jpg)



Fig. 1. Overview of ViViPlus workflow

To evaluate ViViPlus, we conduct experiments in multiple different buildings. The results demonstrate that ViViPlus achieves reliable performance, with a mean accuracy of 2.47m and a 95th percentile accuracy of 5.41m, outperforming even the best among four comparative approaches by $>27\%$ and $>20\%$ , respectively. We also implement Particle Filter to enhance ViViPlus for mobile tracking, which yields an average and 95th percentile accuracy of 1.87m and 3.46m, significant outperforming three comparative systems. It is our vision to replace previous RSS fingerprints with RSG matrix for WiFi-based location systems in real-world deployment.

The core contributions are summarized as follows.

1) We explore spatial awareness of WiFi signals from the perspective of RSG for localization. RSG exploits the underlying spatial features of RSSs from nearby locations, which better mitigates the spatial ambiguity and temporal instability than the original RSS fingerprints.   
2) We propose RSG matrix to formulate a novel fingerprint form based on RSG features. Derived from pure RSS fingerprint database, RSG matrix is fully compatible with and requires no more information inputs than any existing fingerprint-based systems. We design algorithms to represent, construct, and compare the proposed RSG matrix for efficient localization.   
3) We implement ViViPlus on smartphones and conduct extensive experiments in different buildings with five different start-of-the-art approaches as comparison. The results demonstrate ViViPlus achieves remarkable performance gain without the pains of resorting to additional information or restrictions to users.

The rest of the paper is organized as follows. An overview is presented in Section II. We introduce RSG in Section III and present the ViViPlus design in Section IV. Evaluation is conducted in Section V. We review related works in Section VI and conclude this work in Section VII.

# II. OVERVIEW

# A. Classical Fingerprinting Framework

The mainstream of existing approaches employ RSS observations at one location as its fingerprints $[6]$ , $[8]$ , $[9]$ , $[14]$ . Such systems typically consist of two phases: In the first offline training phase, an RSS fingerprint database is constructed with locationally labelled fingerprints. In the online localization phase, location is determined by fingerprint matching.

![](images/eb803cf187b1b564cf77edcd6a78ae857fecef5be0d53a19ce04e1a5c96a2330.jpg)



![](images/22729e4a438b04e6be29fe3222e80024a7926bb351c2a85c1599f8395872081c.jpg)



![](images/36d1ddd2cda8dbf689ffd3129e1959de39aab373e3eb5a071aa9042640ca4778.jpg)



Fig. 2. Fingerprint spatial ambiguity and temporal instability: (a) Fingerprint distance matrix of 70 locations in a room. While most of the most similar fingerprints appear at the true location (on diagonal line), the top k most similar fingerprints may be far away. (b) Fingerprint distances of a specific location (6,2) to all other locations. (c) Re-collected fingerprint distance matrix against those used in (a). For many queries, a significant parts of the best matched locations are not the true locations.

Formally, the area of interests is sampled as a discrete location space $L = \{l_{1}, l_{2}, \cdots, l_{n}\}$ where n is the amount of sample locations. For each location $l_{i}$ with coordinates $(x_{i}, y_{i})$ , a corresponding fingerprint is denoted as $f_{i} = \{f_{i1}, f_{i2}, \cdots, f_{im}\}$ , $1 \leq j \leq m$ , where $f_{ij}$ denotes the RSS value (or the RSS distribution in probabilistic algorithms [5]) of the jth AP and m is the total number of APs in the targeted location space. All fingerprints form a fingerprint space $F = \{f_{1}, f_{2}, \cdots, f_{n}\}$ , corresponding to the location space L. The radio map consisted of $< l_{i}, f_{i}>$ terms is usually constructed either manually by site survey or automatically by crowdsourcing [6], [8]. Then location is estimated by retrieving the best matches of a query fingerprint against F.

# B. ViViPlus Overview

The design of ViViPlus follows the classical fingerprint framework, with no more inputs than any existing fingerprint-based systems. By doing this, we retain the elegant ubiquity of WiFi fingerprinting. ViViPlus contains three unique modules, i.e., RSG matrix database construction, query RSG matrix construction and RSG matrix matching, as illustrated in Figure 1.

An RSG matrix database is constructed during the offline phase based on top of a conventional RSS fingerprint database, with neither mobility nor other information requirements. The RSG matrix for one reference location is formed upon the RSS fingerprints from itself and its multiple neighbouring locations.

In the localization stage, a user reports a query RSS fingerprint in the identical form as classical RSS fingerprints. Due to lack of location information and thus no neighbouring locations, the query is then transformed into an RSG matrix depending on the information of a current candidate location. Specifically, when matching a user query $f_{Q}$ against a candidate reference location $l_{C}$ , we construct a RSG matrix $G_{Q(C)}$ tailored to this candidate location by reusing its RSG information (nearby locations and corresponding fingerprints). Therefore the query RSG matrix is customized for each candidate location. The ultimate location estimate of query $f_{Q}$ is then determined by the top k locations that output the largest similarity between their RSG matrices.

The proposed ViViPlus is computation efficient. The relatively complex RSG matrix construction is one-time effort during offline phase. During the online phase, the only extra computation costs compared to traditional RSS fingerprint-based approaches, lie in the RSG matrix construction for each comparison, which can be fortunately computed in constant time. For practicality, we also implement an AP selection procedure to include only good quality APs (scored by AP information entropy [24]) for localization. To further reduce the computation costs, in practice we do not need to try every reference location, but can efficiently shrink the search space by looking at common APs.

![](images/1620afd24fa9a7e23ca6c0ba239e7d608575d9ae2d87184d7749740bb901ce5e.jpg)



Fig. 3. RSS differences between neighbouring locations tend to be more stable than individual RSS values.

# III. SPATIAL AWARENESS OF RSS FINGERPRINTS

# A. Limitations of RSS Fingerprint

While spatial uniqueness and temporal stability are two fundamental assumptions of RSS fingerprinting, these two properties do not always hold in practice.

On one hand, multipath effects of wireless signals render similar RSSs over different locations of the same AP, resulting in the spatial ambiguity of RSS fingerprints, which means that fingerprints from distinct (and distant) locations may be similar to each other. Figure 2a shows the self-similarity matrix, using Euclidean distance, among each pair of fingerprints from 72 locations in a classroom. As seen, the most similar fingerprints for each query do not always appear at the true locations (on the diagonal line). In contrast, distant locations may possess more similar fingerprints. Taking location (6,2) as an example, we calculate the fingerprint similarity to all 70 locations in the room and depict the results in Figure 2b. The second most similar fingerprint appears at location (2, 3), which is about 4m away from the true location (note that the width and the length of the classroom are both only about 9m). Spatial ambiguity is recognized as the root causes of large location errors in WiFi localization [3], [9].

![](images/42a0684d4f20e1b3ddfdab2ba08842d0693a25309467ccdbd9b101f9ac574ad5.jpg)



Fig. 4. Illustration of RSG matrix (of the central green sample location)

On the other hand, RSS is known to be sensitive to uncertain environmental dynamics due to severe multipath effects in complex indoor environments $[5]$ , $[11]$ , $[16]$ . RSS variations may induce temporal instability, i.e., location fingerprints would vary over time, deviating from and therefore failed to match the initially collected ones. As shown in Figure 2c, we re-collected the fingerprints of all locations in the same room on a different day and calculate the similarity with those previously collected. Compared with Figure 2a, more locations cannot be correctly located using the newly collected fingerprints, which indicates that they have deviated from the original version due to temporal changes. As a result, temporal instability would gradually degrade the localization performance over time especially during long-term deployment.

In complex indoor environments, spatial ambiguity and temporal instability are even severe yet inevitable due to multipath fading and temporal dynamics. Consequently, they become the major obstacle behind the limited accuracy and reliability of WiFi localization based on RSS fingerprints.

# B. RSS Spatial Gradient

In contrast to previous WiFi fingerprinting that mainly employs RSS vectors as fingerprints, we propose RSG to explore and exploit spatial features of RSS fingerprints. The key insight is that certain spatial relationship among RSSs from multiple adjacent locations keeps relatively stable, although their individual RSS might be altered by signal distortions. As shown in Figure 3, RSS differences between two neighbouring locations are more stable than individual RSS values (with about $80\%$ improvement), regardless of the AP's signal strengths. Therefore, we can seek for a set of neighbouring locations to form a RSG matrix as more favorable fingerprints for our advantages of building more accurate and reliable fingerprinting scheme. Note that we do not assume that RSS observations are similar among neighbouring locations as we are exploring the stability of RSS differences among them. However, we neither require every pair of locations hold stable RSS differences. As will demonstrated in the following, we only need to select a subset of neighbouring locations that possess more stable RSS spatial relationships.

1) RSG Matrix Specification: An RSG matrix for a specific location depicts the RSS differences of every AP between itself and its neighbouring locations. Specifically, for a location $l_{i}$ , the RSG matrix is defined as:

![](images/0f46f1f471e2fb2972ea6aad9bce51af285b252af59dd5139c1dcf1a4a258efc.jpg)  
(a)

![](images/e8710e72a218dc95642ea30d2ae070e6e3198864dfb3921a98cfd57131e39433.jpg)



(b)

![](images/eb34e4f0fa639828dbf7e0d542b15f049454bc3ad8e75696362366372c51fbf1.jpg)



(c)

![](images/060e7cb420049d72f4d9b2c093b191c06455ea60ce8018e45584f087c95f47d0.jpg)  
(d)   
Fig. 5. Illustrations of RSG matrices at different locations: (a) Location (2,5). (b) Location (3,4). (c) Query RSG matrix from (2,5) generated upon the RSG matrix of candidate location (2,5), which is similar to (a). (d) Query RSG matrix from (2,5) built upon a different location (3,4), which is significantly different to (b).

$$
G _ {i} = \left(g _ {i 1} ^ {\rightarrow}, g _ {i 2} ^ {\rightarrow}, \dots , g _ {i m} ^ {\rightarrow}\right) ^ {\mathrm{T}}, \tag {1}
$$

where $m$ is the total number of APs that are selected for location $\pmb{l}_i$ . $g_{ik}^{\prime}$ is a series of RSS differences of AP $k$ between $\pmb{l}_i$ and its $2r + 1$ neighbouring locations, which is defined as:

$$
\vec {g _ {i k}} = \{<   d (\boldsymbol {l} _ {i}, \boldsymbol {l} _ {j}), \phi (f _ {i k}, f _ {j k}) >, i - r \leq j \leq i + r \}, \tag {2}
$$

where $\phi(f_{ik}, f_{jk})$ is the RSS difference of AP k between location $l_{i}$ and its neighbouring location $l_{j}$ (i.e., the respective kth item in their corresponding fingerprints $f_{i}$ and $f_{j}$ ). In the section, we simply calculate $\phi(f_{ik}, f_{jk}) = f_{ik} - f_{jk}$ and in Section IV-A2 we will present a discretized definition to enhance the robustness. $d(l_{i}, l_{j})$ denotes the physical distance between $l_{i}$ and $l_{j}$ . The $2r + 1$ neighbouring locations, i.e., $l_{i-1}$ to $l_{i-r}$ and $l_{i+1}$ to $l_{i+r}$ , are selected from the surrounding subspace of $l_{i}$ and ordered in physical distance to the current location $l_{i}$ . As a result, the RSG matrix $G_{i}$ for a reference location $l_{i}$ is a $m \times (2r + 1)$ matrix, where the $r + 1$ th column are all zeros (These will not necessarily be zeros when profiling a query fingerprint, as detailed later in Section IV). Figure 5a and Figure 5b shows two illustrative RSG matrices for two different locations respectively.

2) RSG Matrix Superiority: We qualitatively analyze the advantages of the proposed RSG matrix to traditional RSS fingerprints regarding temporal stability and spatial uniqueness.

First, RSG matrix exploits the spatially differential RSSs among a set of nearby locations, which turns out to be more stable against temporal dynamics than previous RSS fingerprints formed by absolute RSS values observed at a single location [16], [20], [21]. Specifically, let $f_{ik}^{1}$ and $f_{jk}^{1}$ denote the RSS values of $AP_{k}$ at two nearby location $l_{i}$ and $l_{j}$ at time $t_{1}$ ; $f_{ik}^{2}$ and $f_{jk}^{2}$ denote those measured at time $t_{2}$ . Accounting for that temporal dynamics in the environments would be similar to neighbouring locations, the RSS differences over time would also be likely similar, i.e., $|f_{ik}^{1} - f_{jk}^{1}| \approx |f_{ik}^{2} - f_{jk}^{2}|$ , while their respective RSS value changes $|f_{ik}^{1} - f_{ik}^{2}|$ and $|f_{jk}^{1} - f_{jk}^{2}|$ could be significantly large, as shown in Figure 3.

![](images/9d6ee1d9ef62fee8405755cb4b16d2a42b4058bbc4212d7dcb42218da4e91bfd.jpg)



(a)

![](images/b4b7f48bac2727c5ae8fe7e7ac3913efaa4de192125b0ffd75f41e6df2387586.jpg)



(b)

![](images/68c1f2c260e6d4c4c179633125ff0c67c054127694894aa879a1308d85af53f9.jpg)



(c)   
Fig. 6. RSG matrix mitigates spatial ambiguity and temporal instability: (a) Distance matrix of RSG matrix of a room. (b) RSG matrix distance for a specific location (6,2). (c) Distance matrix of RSG matrix of re-collected fingerprint against the previous data used in (a). In both (a) and (c), the best matched locations for each query almost always appear at close locations to the true locations (on the diagonal line and its two parallel lines).

Second, RSG matrix is also more distinctively in space. The reasons are two folds. 1) Different from traditional RSS fingerprints that rely on the measurements solely from one single location, RSG matrix synthesizes more information from multiple locations for location distinction and naturally possess better spatial resolution. 2) As will be depicted in Section IV, our novel scheme for RSG matrix generation and comparison further improve the spatial uniqueness. To be brief, the RSG matrix for a user query is constructed upon the fingerprints of a candidate reference location and its selected neighbours. Therefore, the query RSG matrices of an identical query vary upon different candidate locations. Hence, the constructed RSG matrix would be similar to the reference matrix if the query comes from the same location with the reference one (Figure 5a and Figure 5c); otherwise they will be significantly different (Figure 5b and Figure 5d). For two distant locations that suffer from spatial ambiguity under traditional RSS fingerprints, their RSG matrices would still be distinctive since they are unlikely to hold consistent gradients with the neighbouring fingerprints even their own fingerprints are similar to each other.

Figure 6 illustrate the advanced results for the same dataset as in Figure 2, yet using RSG matrix as fingerprints. Comparing Figure 2a with Figure 6a and Figure 2b with Figure 6b, the spatial ambiguity is clearly reduced by using RSG matrix. If we compare Figure 2c with Figure 6c, one can also observe that the performance is well retained regarding temporal dynamics. Specifically, in both Figure 6a and Figure 6c, the three best matched RSG matrices almost always appear at the three closest locations, as indicated the three diagonal lines in the figures (Note that the three lines are not closely together because we index the 70 locations in a $8m \times 9m$ room with a S-shaped snakelike manner).

# IV. ViViPlus DESIGN

In this section, we present the design and implementation of ViViPlus system that exploit RSG matrix as fingerprints.

# A. Realization of RSS Spatial Gradient

The RSG matrix for each reference location is built upon the original RSS fingerprint radio map. In this section, we first discuss how to form a good RSG matrix for each reference location. Then we consider discrete the RSG matrix to increase the robustness of our system. Finally, we present how to profile a query fingerprint based on a reference location's RSG.

Since an RSG matrix is basically a collection of the RSG of multiple APs (with each column corresponding one AP), we simply interpret on a single AP basic. The RSG matrix construction is then a repeat over multiple selected APs.

1) Profiling a Reference Location: For a reference location $l_{i}$ with an average fingerprint $f_{i} = \{f_{ik}, 1 \leq k \leq m\}$ , we consider all its neighbouring locations within r sample points. For each AP, our goal is to select c = 2r locations among them as the neighbours for RSG construction. Recalling that the key insight of RSG is to exploit stable spatial features, we achieve this by selecting a subset of locations that produce the most stable RSG for each AP.

Previously, we mention the representative fingerprint $f_{i}$ for a location $l_{i}$ as the averaged one. In practice, the fingerprint database generally stores all raw fingerprint measurements for each location [5], [25]. That is to say, there will be multiple RSS records of each AP for each location. Therefore, we leverage all available RSS observations to optimize the spatial stability in terms of RSG difference variances.

Specifically, for location $l_{i}$ , denote its averaged RSS for kth AP as $f_{ik}$ . Suppose there are p RSS records, i.e., $\{f_{jk}^{(x)}, 1 \leq x \leq p\}$ , for a location $l_{j}$ in its neighbouring set. We calculate every RSS difference $\phi(f_{ik}, f_{jk}^{(x)}), 1 \leq x \leq p$ and derive the corresponding variance. To guarantee sufficient space coverage of the selected neighbours, we increase the distance d step by step from 1 to r and select the two locations with the smallest RSS difference variances for each step. In practice, this policy is simply equivalent to an efficient operation of selecting the two locations with smallest RSS variances. By doing this, we obtain c = 2r neighbouring locations in total that cover physical distances from 1 to r sample points. For each selected location $l_{j}$ , we calculate the RSS difference as $\phi(f_{ik}, f_{jk}) = f_{ik} - f_{jk}$ , where $f_{jk} = \frac{1}{p} \sum_{t=1}^{p} f_{jk}^{(t)}$ . Afterwards, we generate the RSG for current location $l_{i}$ by dividing the selected neighbours into two parts with identical sizes and ordering them by physical distances to $l_{i}$ , resulting in the RSG profile $g_{ik}^{\rightarrow} = \{<d(l_{i}, l_{j}), \phi(f_{ik}, f_{jk}) >, i - r \leq j \leq i + r\}$ of the kth AP as in Figure 4. Repeating the above procedure for each AP in $f_{i}$ , we obtain the RSG matrix whose kth column corresponds to the RSG profile of the kth AP.

The above profiling procedure is similar to that in [25], which optimize the stability in terms of entire fingerprint similarity. Differently, ViViPlus considers spatial stability based on RSS gradient for the RSG matrix.

2) Discretization of RSG matrix: In practice, there might be uncertainties even we use the averaged RSS for calculation of RSS difference. To improve the robustness, we further discretize the RSG matrix. After discretization, each element of the RSG matrix reflects the strength relationship of the RSSs between the current location and its nearby locations, which is more stable and reliable than the absolute RSS difference.

As multiple RSS measurements from a specific AP over time typically follow a Gaussian distribution [5], [11], [24], we adopt the discretization method based on t-test as in [20]. t-test is a statistical hypothesis test that determines whether the null hypothesis (no difference between sample values) is to be rejected or accepted.

Let $R_{ik} = \{f_{ik}^{(x)}\}$ and $R_{jk} = \{f_{jk}^{(x)}\}, 1 \leq x \leq p$ denote two sets RSS samples from AP $k$ at location $l_i$ and $l_j$ . The mean and standard variance of $R_{ik}$ and $R_{jk}$ are denoted by $(\mu_{ik}, \sigma_{ik})$ and $(\mu_{jk}, \sigma_{jk})$ , respectively. Then we test the following two-side hypothesis:

$$
\left\{ \begin{array}{l l} H _ {0}: & \mu_ {i k} = \mu_ {j k} \\ H _ {1}: & \mu_ {i k} \neq \mu_ {j k} \end{array} \right. \tag {3}
$$

The $t$ -statistic can be calculated as

$$
t ^ {k} = \frac {\mu_ {i k} - \mu_ {j k}}{\sqrt {\frac {\sigma_ {i k} ^ {2}}{n} + \frac {\sigma_ {j k} ^ {2}}{n}}} \tag {4}
$$

Therefore, we can compute the cumulative distribution for t distribution at values in $t^{k}$ , and we set the signification level $\alpha = 0.1$ . The null hypothesis $H_{0}$ can be rejected with confidence(i.e. $\mu_{ik} \neq \mu_{jk}$ ) if a cumulative density is greater than $1 - \alpha$ , and accepted(i.e. $\mu_{ik} = \mu_{jk}$ ) otherwise.

Based on significance test, we compute the RSS gradient (i.e., the discrete RSS difference) $\phi(f_{ik}, f_{jk})$ as

$$
\phi (f _ {i k}, f _ {j k}) = \left\{ \begin{array}{l l} 1, & H _ {0} \text {   is   accepted } \\ 2, & H _ {0} \text {   is   rejected   and   } \mu_ {i k} \geq \mu_ {j k} \\ 0, & H _ {0} \text {   is   rejected   and   } \mu_ {i k} <   \mu_ {j k} \end{array} \right. \tag {5}
$$

The improvement by the discretized RSS gradient would be compared with the non-discrete RSS difference in the evaluation in Section V-B2.

3) Profiling a Query Fingerprint: In ViViPlus, a user queries his/her location by reporting an RSS fingerprint. We then construct an RSG matrix based on a single query fingerprint. The key intuition is to reuse the data in the RSG matrix database for reference locations to generate query RSG matrix. By doing this, a ViViPlus user is not required to report any mobility data, but only an RSS fingerprint as if he/she is using a conventional RSS fingerprint based system.

Consider that we are matching a query RSS fingerprint $f_{Q}$ against a candidate reference location $l_{C}$ . We then generate the query RSG matrix by substituting the query fingerprint as the representative fingerprint of $l_{C}$ . Specifically, suppose the $g\vec{C}k = \{ < d(\boldsymbol{l}_C, \boldsymbol{l}_j), \phi(f_{Ck}, f_{jk}) >, j \in N(\boldsymbol{l}_C) \}$ is the RSG for the $k$ th AP in the reference RSG matrix $G_C$ for the current location, where $N(\boldsymbol{l}_C)$ denotes the selected neighbours. The corresponding column in the query RSG matrix $G_Q$ is calculated as $g\vec{Q}k = \{ < d(\boldsymbol{l}_C, \boldsymbol{l}_j), \phi(f_{Qk}, f_{jk}) >, j \in N(\boldsymbol{l}_C) \}$ , where we replace $f_{Ck}$ in $g\vec{C}k$ and keep everything else (including $\boldsymbol{l}_C$ ) unchanged. Repeat this for all $m$ APs, we derive a query RSG matrix $G_Q = (g\vec{Q}_1, g\vec{Q}_2, \cdots, g\vec{Q}_m)^{\mathrm{T}}$ .

Generally, the resulted query RSG matrix will be similar to the reference one, if the query fingerprint is from the same or close location with $l_{C}$ . Otherwise, the two matrices would deviate from each other significantly because two different locations are unlikely to share consistent RSS spatial gradients over $N(l_{C})$ locations. This reference-data based query matrix generation is a unique design, which enables ViViPlus to deal with a single query fingerprint from one user without any additional information. The comparison between two RSG matrices for localization follows in the subsequent section.

# B. Localization with RSG Matrices

Different approaches can be used for RSG matrix comparison. We consider an eigenvector-based method and a SIFT-based method in ViViPlus.

1) Eigenvector-based Method: As the fingerprints involved in ViViPlus is in a matrix form, we intend to devise matrix features for fingerprint matching. Specifically, we exploit eigenvectors and eigenvalues, which are the most common and useful characteristics of a matrix that reflect the spatial feature and dimensionality of the specific matrix. Under this context, an RSG matrix G can also be expressed as a set of $\{<\lambda_{1},\mu_{1}>,<\lambda_{2},\mu_{2}>,\cdots,<\lambda_{m},\mu_{m}>\}$ where $\vec{\mu}_{1},\vec{\mu}_{2},\cdots,\vec{\mu}_{m}$ denotes the m eigenvectors under eigenvalues $\lambda_{1},\lambda_{2},\cdots,\lambda_{m}$ . We calculate a representative vector $\vec{v}$ as $\lambda_{1}\mu_{1}+\lambda_{2}\mu_{2}+\cdots+\lambda_{m}\mu_{m}$ for each RSG matrix $G_{i}$ for location $l_{i}$ . Then we only need to calculate the similarity of the representative vector $\vec{v}_{i}$ for localization. In this paper, we employ Euclidean Distance for this purpose.

2) SIFT-like Method: As shown in Figure 5, an RSG matrix can also be treated as an image with only one channel. Thus we can also apply developed computer vision techniques such as SIFT [26] for our matrix matching.

The computation complexity of eigenvector method is $O(\min(2r + 1, m)^{3})$ while that of the SIFT method is $O((m(2r + 1))^{3})$ , where $2r + 1$ denotes the number of nearby locations we selected and m is the AP number we use to construct RSG matrix. Section V presents the performance comparison of the above two methods. More enhancing technologies can be further incorporated to improve the ultimate performance, such as Particle Filter (PF).

# V. IMPLEMENTATIONS AND EVALUATION

# A. Experiment Methodology

1) Experimental Scenarios: We conduct our extensive experiments in four different buildings as shown in Figure 7. The four buildings have different environment conditions. In particular, the classroom building and company building are much crowded than the academic building and school office building. In addition, the fingerprints in different buildings are collected in different ways. In the company building, fingerprints are automatically collected and the ground truth locations are output by a UWB system. In the other buildings, we manually collect and label the fingerprints with a certain sample density. The data collection details in each building are summarized in Table I.

TABLE I
DATA COLLECTION IN DIFFERENT SCENARIOS 

<table><tr><td>#</td><td>Building type (Areas)</td><td>Size( $m^{2}$ )</td><td>Density</td><td>Devices</td><td>#Samples</td><td>#Loc</td><td>Duration</td></tr><tr><td>1</td><td>Academic (Public areas)</td><td>600</td><td> $1m \times 1m$ </td><td>Nexus 5/7, two Nexus 6p</td><td>23.4K</td><td>93</td><td>10h in 1 day</td></tr><tr><td>2</td><td>Office (Whole floor)</td><td>1,500</td><td> $2m \times 2m$ </td><td>Two Nexus S</td><td>27.2K</td><td>293</td><td>24h in 2 days</td></tr><tr><td>3</td><td>Classroom (Public areas)</td><td>3,360</td><td> $1.2m \times 1.2m$ </td><td>Nexus 7, two Nexus 6p</td><td>87.0K</td><td>460</td><td>12h in 1 day</td></tr><tr><td>4</td><td>Office (Two floors in company)</td><td>2,000</td><td> $1m \times 1m$ </td><td>HUAWEI P9, two HUAWEI Mate 8</td><td>65.0K</td><td>400</td><td>24h in 3 days</td></tr></table>

![](images/da52a692305104c0f338dff11c99bdb5b9ba7078e5525ba4dcfed73fb446a161.jpg)



(a) Office building

![](images/47c5980fbdc473459c705a80b81d4b2d241eda3cd062e7c73996a16538334fc3.jpg)



(b) Academic building

![](images/71db376bd0f5d0844b574b9f99150f1a799cf008ef213ee6659d3dcc7c67328c.jpg)  
(c) Classroom building

![](images/3641a3771419870ffc44ff968570e565795f0d8e6025b7d189cdc3d9b1b0f1e5.jpg)



(d) Company building

Fig. 7. Experimental areas   
![](images/95b9202b58573ff67fa163fd7929b670dcf9bff3b10417afe891bf74d0d19657.jpg)



Fig. 8. Three RSG similarity

![](images/3e566ce3870ded974aef75ad16ec368563406a6d81fdf6dea2989b499cbb6d54.jpg)



Fig. 9. Different RSG matrix

![](images/2e15abbe662992829ca7e8574e9bfa5ed7e95b4d131f572aaad2970f02c0f2e1.jpg)



Fig. 10. Different methods

2) Comparative Methods: To extensively evaluate the performance of ViViPlus, we additionally implement five different start-of-the-art approaches for comparison, which have been proposed to enhance the primary RSS fingerprinting. The five methods are: 1) Horus [5]: A classical probabilistic algorithm; 2) TW-KNN [27]: It applies an iterative recursive weighted average filter to form temporally weighted RSSs as fingerprints; 3) GIFT [20]: A binary metric of differential RSSs at two adjacent locations along a moving trace is exploited. As GIFT is designed for mobile traces, we combine queries from two adjacent locations as one for GIFT in the localization experiments and implement normal GIFT for tracking experiments; 4) ViVi [25]: A most related system that puts forward a similar concept of fingerprint spatial gradient. 5) Magicol [28]: A mobile tracking system using a Particle Filter to fuse traditional WiFi fingerprints and magnetic signals.

In our experiments, we compare our system ViViPlus with Horus, TW-KNN, GIFT(modified) and ViVi. We mainly aim to show the advantages of the proposed RSG over RSS fingerprints. Therefore we focus on the relative accuracy improvement rather than the absolute accuracy achieved by ViViPlus. Hence we mainly implement the core fingerprinting and matching components of the above systems. For example, we omit the clustering step for fast localization in Horus [5]. Then we apply identical preprocessing steps (e.g., AP selection) to all methods. The average location error and the 95th percentile error are adopted as major performance metrics for evaluation.

# B. Overall Performance

1) Different RSG Comparing Methods: We first explore the best RSG matrix comparing methods. We integrate the results of different phones from all experimental areas for evaluation. In addition to SIFT-like and eigenvector-based methods that leverage global feature of a matrix for matching (See Section IV-B), we further incorporate the methods in DorFin [29] and implement an additional method that compares RSG matrices row by row. As shown in Figure 8. Eigenvector-based method achieves the best accuracy, yielding an average accuracy of $2.5\mathrm{m}$ and a 95th error of $5.41\mathrm{m}$ . Although SIFT-like method performs better than eigenvector-based method regarding large errors, its average accuracy is $3.4\mathrm{m}$ which is $35.8\%$ worse than the latter. Considering SIFT is more computationally complex than calculating eigenvectors, we use eigenvector-based method for following evaluation. In addition, we use $r = 3$ and AP number of 15 by default.   
2) Absolute vs. Discrete RSG matrix: We evaluate the benefit of RSG matrix discretization. Evidently in Figure 9, RSG matrix discretization significantly improves the robustness of ViViPlus. While the 95th percentile errors are similar, the average accuracy is improved by $29.3\%$ , decreased from $3.54\mathrm{m}$ to $2.5\mathrm{m}$ by discretizing the RSG matrix.   
3) Performance Comparison: The performances of the proposed ViViPlus as well as the four state-of-the-art and comparative approaches are depicted in Figure 10. As seen, ViViPlus achieves the best performance among all. The average accuracy outperforms Horus by 48.3%, GIFT by 36.9%, TW-KNN by 35.2% and exceeds ViVi by 27.6%. The 95th percentile accuracy outperforms the four comparative approaches

![](images/50fe7232bd37de9ac8f2bdc6f53aeda8677187e70e106546d2ec90db82d73ff4.jpg)



Fig. 11. Different Areas

![](images/5d0581f0085ac86fdc65e7c0b5bf557ffa6b26921119711650b2a7e4d93a327c.jpg)



Fig. 12. Different Devices

![](images/ee7c6545b89f0c3061c0db0cf963d656efb13383a1273f2b2793452041c3ef4b.jpg)



Fig. 13. Impacts of $r$

![](images/af301ea439038a90d6345724c755c4baa1dfa54bedb404dbbea7e36164596c49.jpg)



Fig. 14. Impacts of AP number

by 37.4%, 30.8%, 31.8% and 20.5%, respectively. The results demonstrate ViViPlus achieves remarkable performance gains based on only RSS fingerprints without the pains introducing extra information or constraints. Further performance gains by additional information like sensor hints can easily be incorporated in ViViPlus. For example, we implement Particle Filter in ViViPlus and evaluate it for tracking in Section ??.

4) Performance with Different Conditions: To examine the robustness and practicability of ViViPlus, we invite three users to evaluate it in different buildings with different devices. As shown in Figure 11, ViViPlus achieves consistently delightful accuracy of 2.01m, 2.23m and 2.41m in academic building, office and classroom buildings that suffer from different crowd levels and wireless environments. Furthermore, Figure 12 shows that ViViPlus yields similar performance regardless the devices used. The average accuracies when using Nexus 6p, Nexus 5 and Nexus 7 pad are 1.96m, 2.25m and 2.43m respectively, while the fingerprint databases are not necessarily constructed using the same models of phones (see Table I).

# C. Impact of parameters

1) Impacts of neighbour number: In the above experiments, we use 6 neighbours (r = 3) to generate RSG matrices. Now we examine the impacts of r ranging from 2 to 5. As shown in Figure 13, when r increases from 2 to 3, the average location errors decrease from 3.84m to 2.5m. When r further increases to 5, however, the location errors increase to 2.96m (r = 4) and 3.35m (r = 5). The results indicate that the spatial stability among neighbouring RSSs only hold within a certain space range. Thus if using two distant neighbours (too large r), RSS observations from distant locations will also be involved, which will degrade the stableness of the RSG matrix.   
2) Impacts of AP Number: We also examine the impacts of AP numbers, which determine the size of the resulted RSG matrix. We evaluated the performance by randomly choosing 5, 15, 20, and all APs without filtering. As shown in Figure 14, ViViPlus achieves the best performance when using 15 APs. The average accuracy increases by 53.2%, 24% and 20.4% compared with using 5, 10 and all APs. Also note that the larger AP number we select, the higher system latency will be resulted. Thus in ViViPlus, we use 15 APs by default.

# D. System Latency

Thanks to efficient algorithm design and program optimization, ViViPlus enjoys a low system latency for real-time motion tracking. Specifically, the average computation time for each estimation is 0.6s, which demonstrates its capability for real-time applications. As comparison, GIFT uses 0.91s, Magicol uses 1.45s and Horus uses 0.71s for each estimation. To examine the running latency of the core localization algorithm, we randomly select 1000 individual user queries and integrate the running time. The average query delay of ViViPlus is 0.36s, which is similar to or faster than previous works, among which ViVi takes 0.33s, GIFT takes 0.71s and TW-KNN takes 0.87s.

# VI. RELATED WORKS

ViViPlus is closely related to a number of related works in the literature of indoor localization.

Using Extra Hints: Many works attempt to improve the accuracy of WiFi fingerprinting by leveraging additional information. Popular sensor hints include user mobility based on inertial sensing [4], [8], [10], [21], acoustic ranging [9], WiFi Direct ranging [30], image ranging [3], magnetism [28], etc. While remarkable gains can be achieved, these systems usually suffer from degradation of deployment ubiquity. They may require users to collect data intentionally (e.g., taking pictures) and behave carefully (e.g., monitoring movements), rely on cooperation among multiple users, and/or need access to extra modules like microphone or camera. In contrast, ViViPlus improves WiFi fingerprinting without any additional constraints on system inputs.

Physical Layer CSI: Recently, CSI has been leveraged for precise localization [31]–[34]. With higher resolution to multipath fading, CSI-based systems can yield decimeter-level accuracy [31], [32]. Some works also employ CSI for accurate passive localization and tracking [33], [34]. Despite of its high precision, CSI is not readily available on commercial smartphones and therefore these systems rely on customized hardware or specialized WiFi Network Interface Cards like Intel 5300, which largely limits the ubiquity for deployment.

Spatial Awareness: Some recent innovations also explore RSS spatial awareness for enhanced fingerprinting [7], [20], [35]. Walkie-Markie [7] is the first to explore RSS changing trends along pathways for floorplan construction. GIFT [20] defines a binary differential RSS, i.e., the difference of RSSs from two continuous locations, as a replacement of absolute RSSs to deal with signal variations. While these works inspire the design of ViViPlus, they rely on user movements and are only applicable to continuous tracking. RSS-Ratio [35] leverages differential RSS on two antennas on MIMO systems, which is not suitable on commodity smartphones. ViVi [25] is the most related work to ViViPlus. It employs fingerprint spatial gradient for better fingerprinting. Differently, ViViPlus explores RSS spatial gradient, which achieves better performance regarding spatial ambiguity and temporal instability.

# VII. CONCLUSION

In this paper, we present the design and implementation of ViViPlus, an indoor localization system purely based on WiFi fingerprints, which jointly mitigates spatial ambiguity and temporal instability and derives reliable performance without impairing the ubiquity. ViViPlus exploits the spatial awareness of RSS values by formulating an RSG matrix as enhanced WiFi fingerprints. We devise techniques for the representation, construction, and comparison of the proposed RSG matrix, and integrate ViViPlus as a fully practical system that requires no more inputs than any previous RSS fingerprint based systems. We conduct extensive experiments in different buildings and implement five different systems for comparison. The results demonstrate that ViViPlus significantly improves the accuracy in both localization and tracking scenarios by about 30% to 50% compared with the state-of-the-art approaches.

# ACKNOWLEDGMENT

This work is supported in part by the National Key Research Plan under grant No. 2016YFC0700100, NSFC under grant 61522110, 61332004, 61472098, 61572366, 61472057.

# REFERENCES

[1] J. Wang and D. Katabi, “Dude, where’s my card? RFID positioning that works with multipath and non-line of sight,” in ACM SIGCOMM, 2013.   
[2] L. Shangguan, Z. Yang, A. X. Liu, Z. Zhou, and Y. Liu, “Stpp: Spatial-temporal phase profiling-based method for relative rfid tag localization,” IEEE/ACM Transactions on Networking, 2017.   
[3] H. Xu, Z. Yang, Z. Zhou, L. Shangguan, K. Yi, and Y. Liu, “Enhancing wifi-based localization with visual clues,” in ACM UbiComp, 2015.   
[4] S. Hilsenbeck, D. Bobkov, G. Schroth, R. Huitl, and E. Steinbach, "Graph-based data fusion of pedometer and wifi measurements for mobile indoor positioning," in ACM UbiComp, 2014.   
[5] M. Youssef and A. Agrawala, “The horus location determination system,” Wireless Networks, vol. 14, no. 3, pp. 357–374, Jun. 2008.   
[6] Z. Yang, C. Wu, and Y. Liu, “Locating in Fingerprint Space: Wireless Indoor Localization with Little Human Intervention,” in ACM MobiCom, 2012.   
[7] G. Shen, Z. Chen, P. Zhang, T. Moscibroda, and Y. Zhang, “Walkie-Markie: indoor pathway mapping made easy,” in USENIX NSDI, 2013.   
[8] A. Rai, K. K. Chintalapudi, V. N. Padmanabhan, and R. Sen, “Zee: Zero-effort Crowdsourcing for Indoor Localization,” in ACM MobiCom, 2012.   
[9] H. Liu, Y. Gan, J. Yang, S. Sidhom, Y. Wang, Y. Chen, and F. Ye, "Push the limit of WiFi based localization for smartphones," in ACM MobiCom, 2012.   
[10] H. Wang, S. Sen, A. Elgohary, M. Farid, M. Youssef, and R. R. Choudhury, “No need to war-drive: unsupervised indoor localization,” in ACM MobiSys, 2012.   
[11] L. Li, G. Shen, C. Zhao, T. Moscibroda, J.-H. Lin, and F. Zhao, “Experiencing and Handling the Diversity in Data Density and Environmental Locality in an Indoor Positioning Service,” in ACM MobiCom, 2014.   
[12] Y. Xie, Z. Li, and M. Li, “Precise power delay profiling with commodity wi-fi,” IEEE Transactions on Mobile Computing, 2018.   
[13] C. Wu, Z. Yang, and Y. Liu, “Smartphones based crowdsourcing for indoor localization,” IEEE Transactions on Mobile Computing, 2015.   
[14] Z. Yang, C. Wu, Z. Zhou, X. Zhang, X. Wang, and Y. Liu, “Mobility increases localizability: A survey on wireless indoor localization using inertial sensors,” ACM Computing Surveys, vol. 47, no. 3, pp. 54:1–54:34, Apr. 2015.

[15] D. Lymberopoulos, J. Liu, X. Yang, R. R. Choudhury, V. Handziski, and S. Sen, “A realistic evaluation and comparison of indoor location technologies: Experiences and lessons learned,” in ACM/IEEE IPSN, 2015.   
[16] C. Wu, Z. Yang, C. Xiao, C. Yang, Y. Liu, and M. Liu, “Static power of mobile devices: Self-updating radio maps for wireless indoor localization,” in IEEE INFOCOM, April 2015.   
[17] S. He, W. Lin, and S.-H. G. Chan, “Indoor localization and automatic fingerprint update with altered ap signals,” IEEE Transactions on Mobile Computing, vol. 16, no. 7, pp. 1897–1910, 2017.   
[18] C. Wu, Z. Yang, and C. Xiao, “Automatic radio map adaptation for indoor localization using smartphones,” IEEE Transactions on Mobile Computing, 2018.   
[19] W. Sun, J. Liu, C. Wu, Z. Yang, X. Zhang, and Y. Liu, “MoLoc: on distinguishing fingerprint twins,” in IEEE ICDCS, 2013.   
[20] Y. Shū, Y. Huang, J. Zhang, P. Coué, P. Cheng, J. Chen, and K. G. Shin, "Gradient-based fingerprinting for indoor localization and tracking," IEEE Transactions on Industrial Electronics, vol. 63, no. 4, pp. 2424-2433, April 2016.   
[21] X. Ye, Y. Wang, W. Hu, L. Song, Z. Gu, and D. Li, “WarpMap: Accurate and Efficient Indoor Location by Dynamic Warping in Sequence-Type Radio-Map,” in IEEE SECON, 2016.   
[22] Z. Yin, C. Wu, Z. Yang, and Y. Liu, “Peer-to-peer indoor navigation using smartphones,” IEEE Journal on Selected Areas in Communications, 2017.   
[23] Y. Wen, X. Tian, X. Wang, and S. Lu, “Fundamental limits of rss fingerprinting based indoor localization,” in IEEE INFOCOM, 2015.   
[24] Y. Chen, Q. Yang, J. Yin, and X. Chai, “Power-efficient access-point selection for indoor location estimation,” Knowledge and Data Engineering, IEEE Transactions on, vol. 18, no. 7, pp. 877–888, 2006.   
[25] C. Wu, J. Xu, Z. Yang, N. D. Lane, and Z. Yin, “Gain without pain: Accurate wifi-based localization with fingerprint spatial gradient,” in ACM UbiComp, Sep 11-15 2017.   
[26] D. G. Lowe, “Distinctive image features from scale-invariant keypoints,” Int. J. Comput. Vision, vol. 60, no. 2, pp. 91–110, Nov. 2004.   
[27] D. Han, S. Jung, M. Lee, and G. Yoon, “Building a practical wi-fi-based indoor navigation system,” IEEE Pervasive Computing, vol. 13, no. 2, pp. 72–79, Apr 2014.   
[28] Y. Shu, C. Bo, G. Shen, C. Zhao, L. Li, and F. Zhao, “Magicol: Indoor Localization Using Pervasive Magnetic Field and Opportunistic WiFi Sensing,” IEEE Journal on Selected Areas in Communications, vol. 33, no. 7, pp. 1443–1457, July 2015.   
[29] C. Wu, Z. Yang, Z. Zhou, Y. Liu, and M. Liu, “Mitigating large errors in wifi-based indoor localization for smartphones,” IEEE Transactions on Vehicular Technology, vol. PP, no. 99, pp. 1–1, 2016.   
[30] J. Jun, Y. Gu, L. Cheng, B. Lu, J. Sun, T. Zhu, and J. Niu, “Social-loc: Improving indoor localization with social sensing,” in ACM SenSys, 2013.   
[31] M. Kotaru, K. Joshi, D. Bharadia, and S. Katti, “Spotfi:decimeter level localization using wifi,” in ACM SIGCOMM, 2015.   
[32] D. Vasisht, S. Kumar, and D. Katabi, “Decimeter-level localization with a single wifi access point,” in USENIX NSDI, 2016.   
[33] J. Wang, H. Jiang, J. Xiong, K. Jamieson, X. Chen, D. Fang, and B. Xie, “Lifs: Low human effort, device-free localization with fine-grained subcarrier information,” in ACM MobiCom, 2016.   
[34] X. Li, S. Li, D. Zhang, J. Xiong, Y. Wang, and H. Mei, “Dynamic-music: accurate device-free indoor localization,” in ACM UbiComp, 2016.   
[35] W. Cheng, K. Tan, V. Omwando, J. Zhu, and P. Mohapatra, “Rss-ratio for enhancing performance of rss-based applications,” in IEEE INFOCOM, 2013.