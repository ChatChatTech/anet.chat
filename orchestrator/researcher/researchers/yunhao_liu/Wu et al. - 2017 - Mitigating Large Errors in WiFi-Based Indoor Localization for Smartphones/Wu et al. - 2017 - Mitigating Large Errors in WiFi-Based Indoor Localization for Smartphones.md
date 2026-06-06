# Mitigating Large Errors in WiFi-based Indoor Localization for Smartphones

Chenshu Wu, Member, IEEE, Zheng Yang, Member, IEEE, Zimu Zhou, Member, IEEE, Yunhao Liu, Fellow, IEEE, and Mingyan Liu, Fellow, IEEE

Abstract—Although WiFi fingerprint-based indoor localization is attractive, its accuracy remains a primary challenge especially in mobile environments. Existing approaches either appeal to physical layer information or rely on extra wireless signals for high accuracy. In this paper, we revisit the RSS fingerprint-based localization scheme and reveal crucial observations that act as the root causes of localization errors, yet are surprisingly overlooked or not adequately addressed in previous works. Specifically, we recognize APs’ diverse discrimination for fingerprinting a specific location, observe the RSS inconsistency caused by signal fluctuations and human body blockages, and uncover the transitional fingerprint problem on commodity smartphones. Inspired by these insights, we devise a discrimination factor to quantify different APs’ discrimination, incorporate robust regression to tolerate outlier measurements, and reassemble different normal fingerprints to cope with transitional fingerprints. Integrating these techniques in a unified system, we propose DorFin, a novel scheme of fingerprint generation, representation, and matching, which yields remarkable accuracy without incurring extra cost. Extensive experiments in three campus buildings demonstrate that DorFin achieves a mean error of 2.5 meters and more importantly, decreases the 95th percentile error under 6.2 meters, both significantly outperforming existing approaches.

Index Terms—WiFi, fingerprints, smartphones, indoor localization

# 1 INTRODUCTION

HE proliferation of mobile computing has spurred extensive interests in location-based services, leading to an urgent need for fine-grained location. The past decade has witnessed the conceptualization and development of various wireless indoor localization techniques, including WiFi [1], [2], RFID [3], [4], acoustic signals [5], [6], ultrasound [7], [8], etc. Due to the wide deployment and availability of WiFi infrastructure, WiFi fingerprint-based indoor localization has become one of the most attractive localization techniques [9]–[14]. Roughly speaking, a fingerprintbased scheme consists of two stages: site survey and fingerprint matching. During site survey (a.k.a calibration or war-driving), received signal strengths (RSS) from multiple WiFi access points (APs) are recorded at known locations to construct a fingerprint database. To locate a user, localization algorithms match his RSS measurements against the pre-labeled records and estimate his location to be the one with the best-fitted fingerprint.

There is generally a tradeoff between accuracy, ubiquity, and cost in designing a pervasive indoor localization system. Accuracy has long been the primary

• C. Wu, Z. Yang and Y. Liu are with the School of Software and TNLIST, Tsinghua University. Email: {woo, yangzheng}@tsinghua.edu.cn, yunhao@greenorbs.com.   
• Zimu Zhou is with the the Computer Engineering and Networks Laboratory (TIK), ETH Zurich. E-mail: zimu.zhou@tik.ee.ethz.ch.   
• Mingyan Liu is with the Department of EECS, University of Michigan. E-mail: mingyan@eecs.umich.edu

challenge especially in mobile environments. Even schemes that have been reported to have very high accuracy in some instances, e.g., [2], [13], [15], can experience rapid performance degradation in realistic environments, with median error consistently above 5 meters [16]. In addition, there are always unacceptably large tail errors, e.g., 10∼20m or larger. Recent works [12], [16] found that large errors of prior works could range from 12 to around 40 meters. Mobility further deteriorates the performance especially for smartphone based methods. Efforts to gain high accuracy include to leverage physical layer information [17] and incorporate acoustic ranging [6], [12], among others. Despite of the notable improvements, these methods typically either rely on information unavailable on commodity smartphones, or resort to unrealistic cooperation among a dense crowd of peers, and WiFi fingerprinting is usually employed as a fundamental module [18]. Hence any improvement on WiFi fingerprinting itself is of great significance and is usually not conflict but complementary to enhancements by additional information [19]–[21]. In this paper, we investigate to mitigate large errors for WiFi fingerprinting and achieve accurate and robust localization, especially for mobile phones, without degrading the ubiquity or increasing the costs.

To investigate the root cause of limited localization accuracy, we conduct extensive experiments and uncover or revisit the following characteristics of WiFi fingerprint-based localization: 1) APs have different discriminatory capabilities to fingerprint a specific location since RSS changes are inversely proportional to the physical distance, subject to radio signal propagation laws. Intuitively, faraway APs may lead to large location estimation errors while close ones can help mitigate the location uncertainty. 2) Biased RSS measurements caused by signal fluctuation and human body blockage may present themselves as outliers in fingerprint matching. Human body blockage to smartphones can remove line-of-sight and weaken the received signal by up to 10dB, thus greatly exaggerating the discrepancies of fingerprints measured from the same location. 3) The real-time measured RSS values may be in fact outdated due to incomplete scan by hardware and software limitations of commodity wireless devices. In other words, latest reported RSS values could be cached duplicates of previous scans performed several seconds ago, as we call outdated RSS. Considering user mobility, the outdated RSSs could actually be measurements done at a previous location, which result in transitional fingerprint, i.e., a patchwork of the up-to-date RSSs of the current location and the cached RSSs of the past locations. In overlooking such farraginous information, previous works directly compare the transitional fingerprints with those collected at a single location, incurring frequent fingerprint mismatches. The above are key reasons behind location errors of fingerprint-based schemes, especially in mobile environments; yet surprisingly they have not been adequately addressed in existing works (in spite that some of them, e.g., AP quality and body blockage, have been noticed previously [22], [23]).

![](images/ad33fe50957fe2acd411c30f1c9be93804965c163e9c30f38a43d19257ba1b74.jpg)



Figure 1: Discrimination Diversity

![](images/ec86773c34f88cb5243773b9fd7adf1fd2c50db2f2ddddee4ef842e697dcfc25.jpg)



Figure 2: Fingerprint Inconsistency

![](images/ed482ae38386c89a4e8188f6447fd909fad15232c0a763de66d1069165447359.jpg)



Figure 3: Transitional fingerprints

With these observations in mind, we design DorFin (named after Discrimination diversity, Outdated RSS, and Fingerprint inconsistency), an accurate and robust fingerprint-based scheme that unleashes the true potential of WiFi-based localization for smartphone applications. DorFin includes three main components. First, we quantitatively differentiate distinct AP’s discriminatory ability w.r.t. a specific location. APs with stronger ability are emphasized with more weights in fingerprint matching, while others are de-emphasized. Second, noting fingerprint inconsistency, we apply a robust regression technique in fingerprint matching identify and mitigate those outlying RSS values, in the hope of ensuring accuracy under noisy measurements. Finally, we propose phantom fingerprints that incorporate multiple normal fingerprints in the fingerprint database to deal with the transitional fingerprints. Phantom fingerprints are assembled according to the specific geometrical constraints of outdated RSSs, which are derived by monitoring user mobility using smartphones’ built-in inertial sensors. Integrating these components, we design a uniform fingerprint similarity metric which further takes account of common AP ratio as a factor to mitigate erroneous matches of distant fingerprints.

To validate our design, we implement DorFin on commodity devices and conduct extensive experiments in three campus buildings. We also employ two classical [1], [2] and two latest [24], [25] approaches for comparison. Experimental results demonstrate competitive performance of DorFin even to solutions based on additional ranging techniques. In addition to the average accuracy of 2.5m, DorFin significantly reduces large location errors by limiting the 95 percentile errors in 6.2m, both outperforming all comparison approaches by at least 34% and 21%, respectively. Using only the most essential RSS, the proposed approach requires no extra hardware and is amendable to general fingerprint-based framework as well as mutually beneficial and complementary to existing or upcoming augmentations based on inertial sensors, acoustics, images or others [11], [12], [18]. We envision our approach as an important step towards accurate location estimation on smartphones with the prevalent WiFi infrastructure.

Our contributions are summarized as follows:

• We identify and mitigate several crucial problems that explain the root cause of location errors but have not been adequately studied.   
• We are the first to tackle the transitional fingerprint problem caused by incomplete scan and human mobility. In addition, to the best of our knowledge, DorFin is the first systematic attempt to integrate a suit of novel techniques in a unified solution. The proposed scheme achieves accurate and robust localization with only the prevalent RSS, requiring no additional hardware.   
• We implement a prototype system and conduct

real world experiments in multiple buildings using commodity devices. In addition to the remarkable performance, our method can be conveniently integrated in existing WiFi fingerprintbased localization systems.

The rest of the paper is organized as follows. Section 2 presents our preliminary measurements and basic observations. The method design is detailed in Section 3, followed with the experiments and performance evaluation in Section 4. We discuss the state-of-theart of indoor localization in Section 5 and conclude the paper in Section 6.

# 2 PRELIMINARY AND MEASUREMENTS

In this section, we review the classical RSS fingerprinting problem and investigate fundamental characteristics of radio fingerprints through real measurements. Our preliminary results show some crucial features, which, having been largely overlooked in the past, shed light on how to achieve high accuracy of fingerprint-based localization.

# 2.1 Problem Statement

The working process of a typical fingerprint-based localization scheme consists of two stages: site survey and fingerprint matching. During site survey, wireless fingerprints (i.e., the set of RSS values from multiple APs) are measured and recorded at every location of interests. A fingerprint database (a.k.a radio map) is accordingly constructed, in which the fingerprintlocation relationships are stored. To locate a user who sends a location query with his current RSS fingerprint, localization algorithms retrieve the fingerprint database and return the location of the matched fingerprint as the user’s location estimation.

Denote a fingerprint as $\pmb { f } = [ f _ { i } , i = 1 , \cdots , n ] ,$ , where $f _ { i }$ is the RSS value of the AP $A _ { i } \in { \mathcal { A } } ,$ the set of n detectable APs appearing in $f .$ . For two fingerprints $f$ and $f ^ { \prime } ,$ denote the RSS difference (RSD) vector as $\delta = [ \delta _ { i } , i = 1 , \cdot \cdot \cdot$ , p] where $\ddot { \delta } _ { i } = | f _ { i } - f _ { i } ^ { \prime } |$ indicates the RSD of AP $A _ { i } \in { \mathcal { A } } \cup { \mathcal { A } } ^ { \prime }$ in the two fingerprints and $p = | { \mathcal { A } } \cup { \mathcal { A } } ^ { \prime } |$ . Since the sample fingerprint $\bar { \pmb f }$ and query one $f ^ { \prime }$ do not necessarily contain identical sets of APs, we set $f _ { i } \left( f _ { i } ^ { \prime } \right)$ to -100, the default minimum RSS value, if $A _ { i } \notin \mathcal { A } \left( \mathcal { A } ^ { \prime } \right)$ . By doing this, we can always obtain an extended version of fingerprint that contains $p$ effective APs for a couple of any sample and query fingerprint. Let $\phi$ be the dissimilarity between $f$ and $f ^ { \prime } .$ , which, if measured by Euclidean distance, can be calculated as $\begin{array} { r } { \phi ( \pmb { f } , \pmb { f ^ { \prime } } ) \ = \ \| \pmb { \delta } \| \ = \ \sqrt { \sum _ { i = 1 } ^ { p } \delta _ { i } ^ { 2 } } } \end{array}$ . For all fingerprints stored in the fingerprint database ${ \mathcal { F } } ,$ the goal of fingerprint matching is to find the fingerprint ${ \bar { \pmb f } } ^ { * }$ that achieves the highest similarity with respect to the query fingerprint ${ \bar { f } } .$ . Formally,

$$
\boldsymbol {f} ^ {*} = \underset {\boldsymbol {f} _ {i} \in \mathcal {F}} {\arg \min} \phi (\boldsymbol {f}, \boldsymbol {f} _ {i}). \tag {1}
$$

Then the user’s location is estimated as the corresponding location $L ( f ^ { * } )$ of $f ^ { * }$ . Assumimg the true location of $f$ is $L ( f )$ , the location estimation error is given by $\varepsilon = \| L ( f ) - L ( f ^ { * } ) \|$ k.

# 2.2 Observations

Observation 1 (Discrimination Diversity) APs have diverse discrimination capability to fingerprint a specific location, subject to inherent constraints of radio signal propagation.

We term Discrimination capability as the ability of one AP to distinguish a specific location when including its RSS observations in the location’s fingerprint. Ideally, subject to the propagation law of wireless signals, RSS decays logarithmically with propagation distance $d .$ More formally, $R S S \propto - \log ( d )$ , indicating that $\begin{array} { r l } { \frac { \Delta R S S } { \Delta d } } & { { } \propto \ - \frac { 1 } { d } , } \end{array}$ − 1d , where ∆RSS denotes the RSS change and $\Delta d$ is the corresponding distance change. In other words, an identical ∆RSS can imply a smaller distance change $\Delta d$ at closer locations, or a larger ∆d at faraway positions. Figure 1 depicts the illustrative RSS spatial distribution of two APs. As seen, an RSS variance of 1dB in value corresponds to vastly different changes in physical distance, depending on the specific d. Specifically, faraway APs may contain larger uncertainties in location determination than closer APs. In a nutshell, distance changes indicated by RSS variances depend on the transmitter-receiver distance, leading to diverse discrimination capability across different locations.

Several previous works perform AP selection to deal with AP diversity. A subset of APs are chosen for location estimation using either specifically defined complex metrics or just RSS cutoff [23], [26]. As is pointed out in [27], AP selection is data dependent and thus the selected APs may not always be the most discriminative ones due to significant RSS fluctuations indoors. Hence selecting only a portion of APs and discarding the others may not be the best way to deal with the discrimination diversity, leaving a room for further improvements.

Observation 2 (Fingerprint Inconsistency) The majority of APs hold similar RSSs for fingerprints from the same/close locations while a small fraction may exhibit large differences due to environmental dynamics and human body blockages.

Location errors originate from unmatched fingerprints measured from the same/close locations. Our investigation on these fingerprints indicate that a majority of APs exhibit relatively stable RSSs even when these fingerprints are not matched. That is to say, the fingerprint dissimilarity (under certain metric such as Euclidean distance) is primarily produced by the drastically fluctuating RSSs of a small portion of APs, which is, however, obviously not caused by location changes, but probably stems from ambient dynamics and human body blockages [28], [29] especially in mobile environments.

![](images/561bd8eb1dd5ae9ba0320bdb8173464f16d4c62000dc8485208dbfce9880c6ec.jpg)



(a) Outdated rates over different APs

![](images/55d2a2db488ef4884ae7c55fb10e71474d7b6c231fe80b27f9c7cd018bf99f2a.jpg)



(b) Time delays of outdated RSS

![](images/183eaf9ca7f0c6c016ea5de03eccf01d36a393394f4a1c78c9597a36138a6aa7.jpg)



(c) Time delays in transitional fingerprints   
Figure 4: Outdated RSS phenomenon: The real-time reported RSSs in one fingerprint might be outdated due to incomplete scan.

As shown in Figure 2, signal strengths perceived by smartphones decrease significantly when the human body blocks the direct path of signal propagation, compared to when the user is facing the AP. These weakened RSS observations of blocked APs tend to deviate from the normal profiles, resulting in abnormal RSSs when compared with fingerprints measured during the training phase. Taking Figure 2 as an example, the normal RSS profile absent of body blockage is measured to be $\pmb { f } = [ - 4 0 , - 6 5 , - 5 0 ]$ ]. When a user is present and faces left, the right AP is blocked, resulting in a biased fingerprint $\pmb { f } _ { \mathrm { l e f t } } = [ - 4 0 , - 6 5 , - 6 5 ]$ (for simplicity, we assume RSSs of unblocked APs remain unchanged). When facing right, the line of sight of the left AP is blocked and its RSS is correspondingly weakened, creating a fingerprint $f _ { \mathrm { r i g h t } } =$ $[ - 5 2 , - 6 5 , - 5 0 ]$ ]. Then comparing $\pmb { f } _ { \mathrm { l e f t } }$ and $f _ { \mathrm { r i g h t } }$ with the normal f produces inconsistent RSD distributions $\delta _ { \mathrm { l e f t } } = [ 0 , 0 , 1 5 ]$ and $\delta _ { \mathrm { r i g h t } } = [ 1 2 , 0 , 0 ]$ , both generating abnormally larger fingerprint dissimilarity and ultimately leading to greater location uncertainty.

To tackle with such inconsistency, previous works typically collect orientation-dependent fingerprints for multiple directions [30], [31], but this requires high labour efforts while offers limited gains. Furthermore, the one-time constructed fingerprints are vulnerable to environmental changes, leading to degraded performance over time. Some recent solutions incorporate direction information in the fingerprint database [32] or resort to peer-assisted acoustic ranging among multiple phones [12], [33]. The former increases the costs of fingerprint constructions, while the latter relies on cooperation among multiple users, rendering it impractical. Probabilistic schemes [34], [35] have been designed to tolerate RSS variations by modeling the RSS distributions from sufficient number of samples. In contrast, we aim to identify and mitigate them.

Observation 3 (Transitional Fingerprint) The realtime reported RSS values might be outdated due to incomplete scanning results, caused by software and hardware restrictions.

The incomplete scan phenomenon is a widely existed yet surprisingly overlooked problem on offthe-shelf devices due to the wireless protocol and hardware capability limitations. Figure 3 illustrates a glance of scanning results from mobile devices running the Android OS. Commodity smartphones acquire WLAN information in a passive scanning mode by listening to periodic beacons from surrounding APs on all working channels. In this mode, the time a client stays on a channel is 100ms by default, which is specified by the 802.11 standard [36] and is equal to the default beacon interval. Consequently, the latency incurred in capturing the AP information for 2.4GHz WiFi is about 1,100ms since there are 11 available channels. In practice, it takes about 1∼1.5 seconds for mainstream Android OS to complete a scan with commodity smartphones. Due to beacon conflicts and channel collisions, the beacon interval of 100ms cannot be always guaranteed, potentially resulting in some missed APs during a scan. However, to maintain quality of service, these missed APs can still appear in the scanning results by duplicating information from last several scans a few seconds ago. As shown in Figure 4, a significant portion of APs experience high outdated rates, ranging from 2% to 25%. In particular, about 60% of the outdated RSSs bear an outdated delay of 1.4s, while around 20% and 15% has a delay of 2.7s and 4s, respectively. Translated into fingerprints, Figure 4c indicates that over 80% of fingerprints contain outdated RSSs, and for about 20% the maximum delay time exceeds 4s. Similar phenomenon is observed on various commodity devices including smartphones and pads such as Google Nexus S and Nexus 4, LG D820, and Samsung T210, and laptops such as Lenovo T430s and X1 Carbon.

If a user is stationary, such outdated RSS problem has little impact on location fingerprinting since the cached RSSs are also measured from the same position within a short period of time (less than a few seconds). In mobile environments, however, users may have moved several meters away between consecutive scans, resulting in a fingerprint comprised by RSS values that are actually observed at multiple locations, which we call transitional fingerprint. A transitional fingerprint is a patchwork of the up-todate RSSs of the current location and the cached RSSs of past locations. Previous works treat these spatially mixed fingerprints as normal ones and directly compare them to those stored in the fingerprint database, which are all collected at single locations. Obviously, matching fingerprints mixed from multiple locations to those from single positions may result in frequent fingerprint mismatches or even localization failures.

![](images/453826b6982d08e9a7a9faa35701e30344d91858d247d04a45542e7da3b43290.jpg)



Figure 5: System architecture

![](images/0c223daadff41e2b7060c23ae56c8979b3a81e580066e90327084f7ce71fefa7.jpg)



Figure 6: Phantom fingerprint

![](images/5472a691522cd0fe0df0fcbe80c73b44ae3993814395dc932c3ffaaf9bc7ba02.jpg)



Figure 7: Bequeathal locations

Note that the transitional fingerprint problem is very different from the conventionally denoted outof-date fingerprints, which refer to fingerprints that were collected a considerably long period of time ago [37]. The out-of-date fingerprints are typically the results of RSS variants due to environment dynamics and usually will be deprecated or adapted to date for localization [37]. The transitional fingerprint problem, however, is an intrinsic, environment-irrelevant issue subjected to prevalent WiFi and commercial hardware specifications in mobile contexts, which usually occurs within a short time period of a few seconds. To the best of our knowledge, this problem has not been noticed before. Previous solutions [38], [39] for mobile users utilize information from the past to come up with better disambiguation of candidate user locations, which potentially leverage physical constraints imposed by user movements and thus are completely different from and orthogonal to our consideration. More importantly, previous works treat the entire fingerprint as a basic unit and consider only the time domain. In contrast, we focus on each RSS component that composes the fingerprint, and investigate the spatial relationships between them caused by incomplete scan and user mobility.

Either having been noticed or not in the literature, the above-mentioned problems have not been adequately resolved. In this study, we reconsider the RSS fingerprinting scheme based on these significant observations to mitigate large location errors for smartphone localization.

# 3 DESIGN METHODOLOGY

By designing DorFin, we do not target at providing the most accurate solution for indoor localization among all existing techniques such as those based on RFID [4], PHY layer information [14], acoustic ranging [6], etc, but attempt to explore the true potential of pure WiFi fingerprint based localization scheme. DorFin is designed as an amendable technique that can be widely incorporated in various existing or upcoming WiFi-based solutions. Pursuing this goal, we do not resort to any extra information except for involving inertial sensing for mobility monitoring in DorFin. As illustrated in Figure 5, the proposed solution includes a phantom fingerprint assembling module, a robust regression procedure and a discriminatory policy, unified in a normal fingerprint matching scheme.

# 3.1 Phantom Fingerprints

An intuitive way to overcome transitional fingerprint problem is to recognize and discard the outdated entities before fingerprint matching. However, as indicated in Figure 4, a significant portion of APs bear outdated RSSs. Discarding all of them may degrade the performance of localization since larger number of APs can typically result in better accuracy [27], [32].

In contrast, one query fingerprint consisting of RSSs observed at multiple locations should be matched with fingerprints recombined by measurements from those locations, which, however, are not directly available in the fingerprint database. In this sense, one needs to assemble special fingerprints, i.e., combinations of fingerprints from multiple locations, for matching, as shown in Figure 6. These newly constructed fingerprints do not yet exist in the fingerprint database, and are referred to as phantom fingerprints.

For a fingerprint $\pmb { f } = [ f _ { i } , i = 1 , \cdots , n ] .$ , denote the encountered timestamp of each AP $A _ { i }$ in f by $t _ { i } .$ Recall Figure 3, the scanning delay is typically longer than 1 second by our measurements while the differences of all APs’ detected time in one fingerprint are usually small (indicated by the Time Synchronization Function timestamp provided by the Android OS). Hence, if the time difference between two APs in one fingerprint exceeds a certain value, e.g., 0.5s, then the earlier one is definitely outdated. In particular, for $\mathrm { A P } \ A _ { k } ,$ , the outdated duration $\Delta t _ { k }$ is computed by $\Delta t _ { k } = \operatorname* { m a x } _ { i = 1 , \cdots , n } t _ { i } - t _ { k }$ .

As illustrated in Figure $^ { 6 , }$ assume that $f _ { k }$ is actually the measurement of $A _ { k }$ at a previous location, called bequeathal location (BL), where a user was present $\Delta t _ { k }$ seconds ago. Further assume that the distance and direction from the BL to the user’s current location is $\ell _ { k }$ and $\theta _ { k } ,$ , respectively (we will describe how to compute $\ell _ { k }$ and $\bar { \theta } _ { k }$ shortly). Then when comparing $f$ with a candidate location, say, $L _ { z } ,$ instead of directly computing the dissimilarity between $f$ and $f _ { z } ,$ a sample fingerprint of $L _ { z } ,$ we match it against the phantom fingerprints ${ \pmb f } _ { i }$ z assembled from $f _ { z }$ and $f _ { B L ( z ) } ,$ fingerprint from the BL. Concretely, the RSS value $f _ { k }$ in $f$ is replaced by that of the same AP in $f _ { B L ( z ) }$ . Considering there would generally be temporal RSS samples from AP $A _ { k } ,$ we replace all its raw RSS observations with those from the BL and then accordingly regenerate a new version of fingerprint. In case of outdated RSSs from multiple APs, all of them are replaced according to their individual BLs, finally resulting in a precise phantom fingerprint ${ \pmb f } _ { z } .$ .

The distance offset \` and direction θ can be estimated by dead reckoning method using smartphone built-in inertial sensors like accelerometer, gyroscope, and compass [10], [11], [13]. Specifically, we adopt the method proposed in [40], which counts steps as accurately as up to 98%, regardless of the phone attitudes. The footsteps could then be converted to physical displacement by multiplying with the user’s step length, which can be automatically tracked [13]. The direction, on the other hand, is estimated using gyroscope and compass as [13]. In the following, we demonstrate that although dead-reckoning may not always be adequate for localization, it is sufficient for our purpose of estimating \` and θ. Note that we merely involve inertial sensing to monitor short distance movements, but do not resort to extra information such as a detailed digital floor plan that is required by previous works like Zee [13].

Due to noisy sensors and arbitrary human behavior, \` and θ cannot be 100% accurately computed. To cope with the erroneous estimations, we introduce an error range for each of them, denoted as $\Delta \ell$ and $\Delta \theta ,$ respectively, and demonstrate that the procedure of choosing BLs can tolerate these errors gracefully. Mathematically, as shown in Figure $^ { 7 , }$ potential BLs need to satisfy the condition that their distances and directions to the candidate location are bounded in $[ \ell - \Delta \ell , \ell + \Delta \ell ]$ and $\left[ \theta \mathrm { ~ - ~ } \Delta \theta , \theta \mathrm { ~ + ~ } \Delta \theta \right]$ , respectively. The size of the shaded area is $S = \bar { \Delta \theta } \big ( ( \ell + \Delta \ell ) ^ { 2 } \bar { - }$ $( \ell - \Delta \ell ) ^ { 2 } ) \big ) = 4 \Delta \theta \ell \Delta \ell .$ . Assuming a location sample density of 2m×2m and $\Delta \ell \leq 2$ meters, the minimal size $S _ { 0 }$ to cover two sample locations should be at least $4 \Delta \ell \mathrm { \ m } ^ { 2 }$ . Thus, if $\Delta \ell \leq 2$ meters and $\Delta \theta < 1 / \ell ,$ we have $S < S _ { 0 } .$ , which means the shaded area covers at most one sample location, i.e., there is only one candidate BL. In practice, the maximal value of the missing delay $\Delta t$ is less than 5s (APs not seen for more than 5s would no longer be reported until being detected again next time). Thus, assuming a normal walking speed of $1 . 2 \mathrm { m } / \mathrm { s } ,$ the distance offset can be at most $^ 6$ meters, resulting in a minimum value of $1 / \ell$ of $\frac { 1 } { 6 }$ . In other words, even though the distance and direction estimations are erroneous, we could identify a suspicious area and, with high probability, there is only one possible BL in the area, as long as the errors are in certain ranges $( \Delta \ell \leq 2$ meters and $\Delta \theta \ : < \ : \frac { 1 } { 6 } )$ . In case of multiple BLs (which is rare based on our measurements), the one closest to the center of the suspicious area (the shaded area shown in Figure 7) is selected. Phantom fingerprints are then constructed by combining fingerprints from the candidate location and those from the BLs, i.e., substituting the tuples corresponding to the outdated RSSs, as shown in Figure 6.

According to specific location sampling density, not all outdated RSSs need to be replaced. Only RSSs with distance offsets \` exceeding half of the unit length of sampling grids should be replaced. If \` is less than half of the sampling distance (including being equal to 0 which means static user), fingerprints are merely treated in the traditional way. Different from existing mobility-assisted approaches [11], [13], [39] that explore spatial mobility constraints, we solely utilize essential mobility hints to amend the transitional fingerprints. Hence DorFin can be further integrated with previous mobility-assisted techniques to achieve better performance.

# 3.2 Robust Fingerprinting

As we have observed, RSSs of one pair of fingerprints may contain outliers because of impaired measurements due to human body blockage. Since this is a primary cause of biased RSSs in mobile environments, only RSSs over a small portion of APs (that are blocked) may present outliers while most APs would remain consistent. Thus in this section, we propose to apply robust regression method on the inconsistent fingerprints, in the hope of bounding the influence of outlying measurements.

There are a large body of robust regression techniques, such as M -estimator, S-estimator, L-estimator, etc [41]. Among them, we choose the most widely adopted Least Median of Squares (LMS) [42] estimator due to its simplicity, effectiveness, and high breakdown point (0.5), which is demonstrated to yield sufficient results with efficient computation (as indicated in Section 4).

Given a query fingerprint $f _ { s } = [ f _ { s , i } , 1 \leq i \leq p ]$ and a sample fingerprint $\pmb { f } _ { t } = [ f _ { t , i } , 1 \leq i \leq p ]$ (suppose that both of them have been adjusted to be of $p$ RSS values as introduced in Section 2.1), we adopt a simple linear regression model as follows:

$$
y _ {i} = \alpha_ {1} x _ {i} + \alpha_ {2} + e _ {i}, i = 1, \dots , p, \tag {2}
$$

where the response variables y are given by $\mathbf { \Pi } _ { f _ { s } } ,$ while explanatory variables $\pmb { x } = \pmb { f } _ { t } . \pmb { e } = [ e _ { 1 } , \cdots , e _ { p } ]$ indicates the error term which is assumed to be normally distributed with zero mean and an unknown standard deviation σ.

As the AP number p is usually small, applying robust regression on insufficient observations does not always produce convincing statistical results. To obtain sufficient data for regression, we propose to compare the query fingerprint against all sample fingerprints corresponding to a candidate location, instead of a single averaged fingerprint. Specifically, for the candidate location $L \ = \ \bar { L ( \mathbf { \nabla } f _ { t } ) }$ with sample fingerprints $\mathcal { F } ^ { L } = \{ f _ { k } ^ { L } , k = 1 , \cdots , m \}$ , we simultaneously match $f _ { s }$ to all records in $\mathcal { F } ^ { L }$ . In doing so, we acquire mp observations, which can achieve the scale of hundreds since there are generally at least dozens of sample fingerprints for one location in the fingerprint database, and thus are sufficient for LMS regressiobecomes $\pmb { x } = [ \pmb { f } _ { 1 } ^ { L } , \cdot \cdot \cdot , \pmb { f } _ { m } ^ { L } ] _ { 1 \times m p } ^ { T }$ planatory variables x and correspondingly y is expanded as $\pmb { y } = [ \pmb { f } _ { s } , \cdot \cdot \cdot , \pmb { \dot { f } } _ { s } ] _ { 1 \times m p } ^ { T } .$ The regression model is thus rewritten as

$$
y _ {k, i} = \alpha_ {1} x _ {k, i} + \alpha_ {2} + e _ {k, i}, \tag {3}
$$

where $i = 1 , \cdots , p , k = 1 , \cdots , m _ { \scriptscriptstyle { \mathscr { M } } }$ , and $x _ { k , i }$ and $y _ { k , i }$ indicate the value of $f _ { i }$ in $\pmb { f } _ { k } ^ { L }$ and $\mathbf { \Pi } _ { f _ { s } , \ }$ respectively. Applying LMS to the data [x y] yields $\hat { \pmb { \alpha } } = [ \hat { \alpha } _ { 1 } , \hat { \alpha } _ { 2 } ]$ where the estimates $\hat { \alpha } _ { i }$ denote the regression coefficients. Multiplying x with these $\hat { \alpha } _ { i } ,$ we obtain the estimated values of $y _ { i }$ as

$$
\hat {y} _ {k, i} = \hat {\alpha} _ {1} x _ {k, i} + \hat {\alpha} _ {2}. \tag {4}
$$

The LMS estimator is given by minimizing the median of squares of residuals as follows:

$$
\min _ {\hat {\alpha}} \operatorname * {m e d} _ {i, k} (y _ {k, i} - \hat {y} _ {k, i}) ^ {2}. \tag {5}
$$

To determine whether a value $y _ { k , i }$ is an outlier among all elements in y, we compare the residual $\boldsymbol { r } _ { k , i } ~ = ~ y _ { k , i } - \hat { y } _ { k , i }$ to the scale estimate $\sigma ^ { * }$ defined by [41]. Then each $y _ { k , i }$ is adjusted to $\tilde { y } _ { k , i }$ as follows:

$$
\tilde {y} _ {k, i} = \left\{ \begin{array}{l l} y _ {k, i} & \text { if } | r _ {k, i} / \sigma^ {*} | \leq 2. 5 \\ \hat {y} _ {k, i} & \text { otherwise } \end{array} \right. \tag {6}
$$

where

$$
\begin{array}{l} \sigma^ {*} = \sqrt {\frac {\sum_ {k = 1} ^ {m} \sum_ {i = 1} ^ {p} w _ {k , i} r _ {k , i} ^ {2}}{\sum_ {k = 1} ^ {m} \sum_ {i = 1} ^ {p} w _ {k , i}}}, \\ w _ {k, i} = \left\{ \begin{array}{l l} 1 & \text { if } | r _ {k, i} / s ^ {0} | \leq 2. 5 \\ 0 & \text { otherwise } \end{array} \right., \\ s ^ {0} = 1. 4 8 2 6 * (1 + \frac {5}{n}) \sqrt {\mathrm{med} _ {k , i} r _ {k , i} ^ {2}}. \\ \end{array}
$$

The involved constant values are widely recognized factors that has been suggested by preliminary experience in the literature [41] and can generalize to difference scenarios. Accordingly, the RSS values of the query fingerprint $f _ { s }$ are regulated as $\begin{array} { r } { \tilde { f } _ { s , i } = \frac { 1 } { m } \sum _ { k } \tilde { y } _ { k , i } } \end{array}$ and the RSDs $\delta _ { s t }$ between $f _ { s }$ and $\scriptstyle f _ { t }$ are thus tuned as $\tilde { \delta } _ { s t , i } = | \tilde { f } _ { s , i } - f _ { t , i } |$ .

# 3.3 Discriminatory Policy

Given that APs have diverse discrimination capability to fingerprint a specific location, it is inappropriate, and also unnecessary, to match two fingerprints with all APs equally involved. More accurate location estimations can be achieved by relying more on the discriminative $\displaystyle { \mathrm { A P s } } ,$ and limiting the influence of those fluctuating and distant ones. Different from previous works that select a subset of APs for localization [23], [26], we attempt to appropriately assess and leverage each AP by seeking a discrimination metric that complies with physical constraints of signal propagation and simultaneously stays robust to RSS fluctuations.

To quantitatively differentiate each AP for a specific location, we define a discrimination factor according to the physical distance estimation between the $\mathrm { A P }$ and the mobile client using the widely adopted Log-Distance Path Loss (LDPL) model [43]:

$$
P _ {d} = P _ {d _ {0}} - 1 0 \gamma \lg (\frac {d}{d _ {0}}), \tag {7}
$$

where $P _ { d _ { 0 } }$ denotes the received power at a distance $d _ { 0 }$ (which usually takes the value of 1 meter), $\gamma$ is the path loss exponent, and $P _ { d }$ is the RSS in decibel measured at a distance of d (in meters). Generally, $P _ { d _ { 0 } }$ is a constant empirical value given the AP transmitting power. Although $\gamma$ can change between each pair of AP-client, there are a lot of works targeting at adaptively estimating its value [14], which is not within the scope of this paper. In the prototyped DorFin, we determine $P _ { d _ { 0 } }$ and $\gamma$ by empirical values and experimental measurements, as detailed in Section 4.

Deriving the distance to AP $A _ { i }$ from the LDPL model, we calculate its discrimination factor in fingerprint $f _ { u }$ to location $L _ { u }$ as follows:

$$
\rho_ {i} ^ {u} = \frac {1}{d _ {i} ^ {u}} = 1 0 ^ {\frac {f _ {u , i} - P _ {d _ {0}}}{1 0 \gamma}}, \tag {8}
$$

where $d _ { i } ^ { u }$ is the estimated distance between $A _ { i }$ and $L _ { u }$ . The rationale of using the reciprocal of physical distance lies in that it is consistent with the derivative of the LDPL equation, which indicates the RSS change $\Delta R S S \propto - \frac { 1 } { d }$ . More generally speaking, the basic rule is to emphasize closer APs with stronger RSSs.

While the exponential $\rho _ { i } ^ { u }$ effectively discriminates different $\mathrm { A P s , }$ it may also induce unnecessary matching errors in case of fluctuating RSSs, which may lead to significant distance estimation errors. Consider one of the APs in a fingerprint that fluctuates to a very large value (e.g., -45dBm). In this case, the effects of other representative APs, which could hold considerable RSSs (e.g., up to -60dBm) and are thus discriminative, may become negligible since they can only get inappreciable factors three or four times smaller than the fluctuating AP. Hence to cope with noisy RSSs, we additionally incorporate a sigmoid function to retain the effects of most discriminative APs. Mathematically, $\rho _ { i } ^ { u }$ is adjusted as follows:

$$
\rho_ {i} ^ {u} = \left\{ \begin{array}{l l} 1 0 ^ {\frac {f _ {u , i} - P _ {d _ {0}}}{1 0 \gamma}} & \text { if } f _ {u, i} \leq f _ {0} \\ \frac {1}{a} \left(1 + e ^ {- 2 \left(\frac {f _ {u , i} + 1 0 0}{1 0} - c\right)}\right) ^ {- 1} & \text { otherwise } \end{array} \right. \tag {9}
$$

where the watershed RSS value $f _ { 0 }$ can be a flexible empirical value, $\mathrm { e . g . , }$ -55dBm. Then the constant parameters a and c need to be determined based on the specific value of $\gamma$ such that $\rho _ { i } ^ { u }$ is continuous at $f _ { 0 }$ . When applying to different location systems, γ can be derived by empirical values and experimental measurements [14]. As shown in Section 4, empirical values based on real measurements yield grateful performance in practice, better than previous AP section policy [26]. $\mathbf { \bar { \rho } } _ { j } ^ { u }$ then serves as a differential weight which will be attached to the regressed RSD of $A _ { i }$ between $\mathbf { \nabla } f _ { u }$ and another fingerprint when computing their dissimilarity, as detailed in Section 3.4. Note that the discrimination factor will be normalized as $\textstyle \sum _ { k = 1 } ^ { n } \rho _ { k } ^ { u } = 1$ to keep the total power of a weighted fingerprint unchanged.

# 3.4 Localization

Integrating all of the above components in a unified solution, we define a new metric as follows for uniform fingerprint dissimilarity judgment.

$$
h (\boldsymbol {f} _ {s}, \boldsymbol {f} _ {t}) = \left(\sum_ {i = 1} ^ {p _ {s t}} (\rho_ {i} ^ {s t} \cdot \tilde {\delta} _ {s t, i}) ^ {2}\right) ^ {\frac {1}{2}}, \tag {10}
$$

where $p _ { s t } = | { \mathcal { A } } _ { s } \cup { \mathcal { A } } _ { t } |$ is the total number of distinctive APs in $f _ { s }$ and $\scriptstyle f _ { t } ,$ and $\rho _ { i } ^ { s t } = \operatorname* { m a x } \{ \rho _ { i } ^ { s } , \rho _ { i } ^ { t } \}$ denotes the discrimination capability of $\mathsf { A P } \ A _ { i }$ for matching $f _ { s }$ and $\scriptstyle f _ { t } ,$ which is calculated based on the regressed fingerprints. Note that the RSD $\tilde { \delta } _ { s t , i }$ could also be given by other suitable metrics such as a probability estimation. Realizing that fingerprints from closer locations share more common APs (or equivalently, fingerprints with very few common APs is unlikely to be from adjacent or same locations), the ultimate form of dissimilarity between two fingerprints $f _ { s }$ and $\pmb { f } _ { t }$ is expanded as follows:

$$
\phi (\boldsymbol {f} _ {s}, \boldsymbol {f} _ {t}) = h (\boldsymbol {f} _ {s}, \boldsymbol {f} _ {t}) \cdot \frac {p _ {s t}}{q _ {s t}}, \tag {11}
$$

where $q _ { s t } = | \mathcal { A } _ { s } \cap \mathcal { A } _ { t } |$ denotes the number of common APs in $f _ { s }$ and $\pmb { f } _ { t }$ . With the above metric, the dissimilarity of two fingerprints with fewer common discriminative APs will be amplified. In case of no common APs $( q _ { s t } ~ = ~ 0 )$ , the dissimilarity will go to infinity, which eradicates the mismatch of two completely irrelevant fingerprints.

# 4 EXPERIMENTS AND EVALUATION

# 4.1 Experimental Methodology

Data Collection. We develop an application for site survey and implement DorFin on Google Nexus S and Nexus 4 phones, which both run the mainstream Android OSs (with Android API level 16 and 17, respectively). The two models are equipped with different WiFi chipsets, the former with Broadcom BCM4329 and the later with Qualcomm Atheros WCN3660. We treat the two models equally and interchangeably for training and testing during evaluation and examine the integrated performance.

We conduct experiments in three campus buildings (denoted as Area #1, Area #2 and Area #3), as shown in Figure 8a, Figure 8b, and Figure 8c, respectively. We manually sample areas of interests in all buildings (corridors in Area #1 and #2, while corridors and rooms in Area #3). To construct the fingerprint database, we collect around 30 to 60 sample records at each location (which typically takes about 1 minute). In Area #1 and $\# 2 ,$ we collect RSS data by putting the phone on a portable desk. To get rid of human body effects, user does not present around the desk when the mobile phone is collecting data (but there are passengers passing through the corridors). A high sampling density of 1m×1m is used for extensive evaluation. Sparser data are then derived from these densely surveyed samples. In total, we obtain 90 locations in Area #1 and 83 sample locations in Area #2. In Area #3 where we sample the whole floor, we hold the phone in hand for collection. We use a sampling density of 2m×2m and survey 293 locations in total, for each we gather at least 60 RSS samples. 293 sample locations are gathered in Area #3. Note that the training data collection can be also done via crowdsourcing-based mechanisms [9], [11], [13]. However, we currently still conduct in manual manner in purpose of obtaining qualified and reliable ground truths for evaluation. Our future work includes building a real system that integrates automatic techniques for fingerprint collection and adaptation.

We consider both static and mobile cases for testing. For stationary cases, we collect query data by letting users record measurements at each location with their smartphones held in hand. For a mobile user, the smartphone measures RSSs while the user is walking at a constant speed along a designated path with predefined start and end points. Note that the individual walking speed varies from user to user and from trace to trace. To obtain the ground truth locations of fingerprint records along the moving trace, we compute user’s walking speed by dividing the path length to the total time, and accordingly interpolate between the start and end points to obtain the location corresponding to each measurement based on their timestamps. The data are all collected at different time (mostly from afternoon to the night) over two days. When collecting data, people are working routinely in their offices or labs and some will occasionally walking around and pass through the corridors. Users hold their phones in hand naturally with free styles during collection. In total, we collect static queries from around 200 locations in Area #1 and #2 and all 293 locations in Area #3. We gather over 20 mobile traces reported from different pathways.

![](images/71f9a794afa518c54e4ea0d26c2c94588fd5cc0c8926d1308f65c7595b6091b6.jpg)



(a) Area #1

![](images/c57894ed90879ef0a320ffe2ab97773307b9af87676a7989ef935491991fdf36.jpg)



(b) Area #2

![](images/98f68e40e0a396e6d3c710c5bb8e2ddc0963f024077da3955df345125d491d30.jpg)



(c) Area #3   
Figure 8: Experiment areas with sizes of around (a) $1 { , } 0 0 0 \mathrm { m } ^ { 2 } .$ , (b) 1,200 m2 and (c) 1,500 m2. APs deployed by the university are marked with stars. Locations of most APs are unknown.

Methods: We compare DorFin with two classical and two state-of-the-art schemes for fingerprint-based localization. Despite of numerous fingerprint-based approaches built upon RADAR and Horus, we still include them in purpose of confirming the performance improvements of DorFin over pure RSS fingerprintbased schemes.

• Enhanced RADAR (RADAR) [1]: RADAR is one of the most classical and widely adopted fingerprinting scheme, upon which a large body of algorithms are built [44]. We enhance RADAR by integrating the proposed common AP (CA) factor and using K-nearest neighbours for location estimation.   
• Enhanced Horus (Horus) [2]: A classical probabilistic algorithm that computes the probability distribution of the RSS values at each location as the fingerprint metric, and retrieves the targets of the maximum likelihood as estimated locations. Horus is also implemented with the CA factor and KNN scheme.   
• Temporally weighted KNN (TW-KNN) [24]: TW-KNN forms fingerprints with temporally weighted RSS by applying an iterative recursive weighted average filter on training RSS samples. Only a set of “important” APs are selected according to RSS values.   
• Kullback-Leibler Divergence (KLDiv) [25], [45]: A fingerprint-based localization scheme that utilizes the Kullback-Leibler divergence distance between two signal distributions as the similarity measure.

# 4.2 Performance Evaluation

# 4.2.1 Overall performance

Figure 9a illustrates the localization error distributions seen by DorFin in different areas. DorFin achieves mean accuracy of around 1.7m in both Area #1 and #2, while the mean error in the larger Area #3 appears to be higher, achieving 3.8m. Besides the promising average accuracy, DorFin significantly reduces large localization errors. In all experimental areas, DorFin decreases the 95th percentile errors to less than 7.0m.

To examine the performance in mobile scenarios, we test the proposed approach on the mobile traces and report the integrated results. As illustrated in Figure 9b, despite slight drop in accuracy compared to the static cases, DorFin maintains graceful performance in mobile cases, far superior to Horus and RADAR. Specifically, the average and 95th errors are about 3.0 meters and 8.5 meters, respectively. In comparison with RADAR and Horus, DorFin decreases both errors by nearly 50%. Even though the performance in mobile cases is not as good as static cases, the achieved accuracy remains comparable and promising. In addition, other complementary techniques such as path matching [9] can be integrated to further improve the accuracy for continuous localization.

Performance comparison. Integrating all results in Figure 9c, DorFin consistently surpasses comparison methods. Specifically, DorFin achieves an average accuracy of 2.5m and and 95th percentile accuracy of 6.2m. TW-KNN and Horus achieve the most comparable performance, with mean and 95th percentile errors of 3.8m, 3.9m and 8.0m and 7.8m, respectively. Among all approaches, RADAR yields the worst results with a mean error of 4.5m. KLDiv suffers from remarkable large errors, with 95th percentile error of 19.8m, although it achieves a slightly better median accuracy of 2.6m than DorFin. In addition, DorFin significantly mitigates the large errors by around 40%, limiting the max location errors within 10m, while all comparative methods produce max errors up to at least 16m.

Impact of training RSS samples. Due to the instability of RSS measurements, we are interested in whether and how the localization accuracy of DorFin would be affected by different sizes of training RSS samples for each location. Hence we tried DorFin with different number of training samples respectively and illustrate the results in Figure 9d. As seen, it yields only marginal differences in performance when using 20, 40, and 60 RSS samples for training. When shrinking the training sizes from 60 to 20 samples, the mean and 95th percentile errors merely increase by 2.4% and 6.4%. The results demonstrate the graceful robustness of DorFin to RSS variations.

![](images/cc6a25c422617191eb7a20d6f37bcdea504e1ca963700f99c413d19136329d7a.jpg)



(a) Accuracy in different areas

![](images/0c51dafae1891ee91a0d1f0b0abea518904eb2ba6343dbf2a5f7378ab1c1b9f9.jpg)



(b) Accuracy in mobile cases

![](images/8a606e1b2abfbf8efe813a38b0bd7c6105b3a2cd8f36d713bf6ebda8dfea6e4b.jpg)



(c) Accuracy comparison

![](images/7f4c2142bb685766b88eb5e676599d8e13019720def8ec28360c691121e08ba2.jpg)



(d) Impact of sample number

Figure 9: Accuracy of DorFin   
![](images/4c7ec86f0f1e49e90dc5d7202d4d2bb2070ddb707737a402a6c09e9bcb9481c2.jpg)



Figure 10: Effect sample density

![](images/88017260b0ca34b4bb27cc1e7e797fb2ff1c7ea379e2d208ff2719d4f511ba9f.jpg)



of Figure 11: Effects of individual modules

![](images/291d3504dae112e2714885bd7b2664f9c2452b2f3e63905ff090b95fb40d5bda.jpg)



Figure 12: Comparing DF with RSS-cutting method

![](images/7b14352b921bc2569867e534fe7bdb1b94007052926bb28daade702e756227c2.jpg)



Figure 13: Effect of PF (mobile scenarios)

Impact of sample density. As mentioned above, we sample the areas of interests with a density of 1m×1m, which is relatively high for practical operations. To examine the performance with sparser sample locations, we perform DorFin with training data of different sample densities (sample density is adjusted by sifting parts of the samples according to their locations). As shown in Figure 10, DorFin preserves excellent accuracy even with sample densities of 2m×2m and 3m×3m. Specifically, with density of 2m×2m, the mean and 95th percentile errors are still limited at 2.5m and 7.0m respectively, both better than those of Horus and RADAR with density of 1m×1m.

In conclusion, DorFin achieves remarkable performance in both stationary and mobile cases, with reasonable sample densities. To understand how each module of DorFin contributes to the integral accuracy, we next perform an analysis across different modules.

# 4.2.2 Effect of Individual Modules

We separately employ each module of DorFin, i.e., the discrimination factor (DF) module, the robust regression (RR) module, the common AP constraints (CA) module, and the phantom fingerprint (PF) module on the most basic nearest neighbor method (denoted as Basic) described in Section 2.1 and evaluate the individual performance.

Effect of DF. We evaluate the impact of DF by using a set of empirical parameters to calculate the discrimination factor. Specifically, the path loss exponent is set to a typical value of 3 in indoor environments while the referenced received power $P _ { d _ { 0 } }$ is determined as -40dB by some on-site measurements. The sigmoid function parameters a and c accordingly adopts the values of 4 and 4.3, respectively. As shown in Figure 11, DF limits the 95th percentile estimation error by about 40%, while the average error is 1.5m lower than the Basic scheme, which has mean and 95th percentile errors of 5m and 17.5m. By placing more weight on more discriminatory APs and limiting those of the others, DF achieves the improvement by ensuring the similarity between fingerprints of close locations. In addition, results from different buildings indicate that discrimination factors with uniform parameter settings can generate satisfactory results in different scenarios. Previous works employ RSS cutting method based on a simple threshold to select a subset of APs for localization. We also implement this scheme in our settings and compare its performance with DF. As shown in Figure 12, by exploiting potentials of all valuable APs, the proposed DF achieves better performance than the simple RSS cutting methods, no matter what thresholds are used.

Effect of RR. As shown in Figure 11, by employing RR over the Basic scheme, an average accuracy of 2.2m is achieved, with the corresponding 95th percentile accuracy of only 6m. Evidently, the advantages of RR are the most significant among all modules by reducing the mean and 95th percentile errors by about 56% and 65% compared with the Basic scheme, respectively. Such results on RR confirm our observation that fingerprint inconsistency counts as a major cause of localization errors of fingerprint-based methods especially for smartphones.

Effect of CA. Figure 11 also demonstrates that the CA module is simple yet effective. Incorporating the CA module with Basic scheme, the average and 95th percentile localization errors are reduced by about 27% and 40%, turning into 3.6m and 11.2m, respectively. Dissimilarity of fingerprints from faraway locations is largely enlarged by the common AP ratio, while that of fingerprints from close locations is hardly affected (since close locations share more common APs).

Effect of PF. To examine the effectiveness of phantom fingerprints in dealing with outdated RSS measurements, we compare the performance of the Basic method on mobile data with and without constructing phantom fingerprints. As depicted in Figure 13, the average and 95th percentile errors decrease from 3.9m and 10.4m to 2.4m and 6.9m respectively when the sample fingerprints are appropriately replaced with phantom fingerprints. With these results, it is of interests to examine to what extent the measured RSSs and further the entire fingerprints are outdated. As we observed, over 11% of RSS measurements are outdated in our experiment data. Furthermore, almost every fingerprint undergoes outdated RSSs. In particular, there frequently exist large offset distances ranging from 2m to 6m in most fingerprints. The effectiveness of the PF convincingly validates our observation that the transitional fingerprint problem can lead to location errors in mobile environments.

Building upon these components, DorFin produces promising accuracies that are competitive with those achieved by leveraging physical layer information [14], [17] or introducing extra ranging techniques [12], [33] (both with mean accuracy of about 1m∼3m). Without degrading the ubiquity nor increasing the costs, we believe the performance achieved by DorFin outperforms most of existing approaches and demonstrates promising potentials in serving as a practical scheme for worldwide deployment.

Considering potential RSS variations over longterm running, the radio map of some locations will change over time and lead to higher localization errors. Accounting this, self-calibration techniques for radio map updating [11], [37], [46], which tackle the RSS temporal variations to maintain an up-to-date database, could be incorporated for practical deployment and usage.

# 5 RELATED WORKS

In the literature of indoor localization, many techniques have been proposed in the past two decades. The state-of-the-art generally falls into two categories: fingerprint-based and ranging-based.

Fingerprint-based techniques. A large body of indoor localization approaches adopts fingerprint matching as the basic scheme for location estimation. Researchers have explored diverse signatures including WiFi [2], RFID [3], acoustic [5], etc. Among various signatures used, WiFi based scheme has been the most attractive.

Smartphones with various built-in sensors have been leveraged in fingerprint-based localization to reduce or eliminate site survey efforts. Examples include LiFS [9], unloc [11], Zee [13], Walkie-Markie [10], etc. They typically combine user mobility with extra information like digital floor plan [9], [13] or indoor landmarks [11] and usually can only handle mobile trajectories [10]. As these works mainly focus on easing the site survey in the training phase, DorFin is orthogonal to them in targeting at fingerprint matching of the online phase to improve localization accuracy. Nevertheless, DorFin is also compatible to crowdsourced fingerprint database constructed via these schemes.

Pursuing better accuracy, sophisticated probability models and advanced machine learning techniques have been employed [34], [35]. The study [16] validates a broad range of approaches in a realistic environments and reports that median errors of prior work are consistently greater than 5 meters and, counterintuitively, that simpler algorithms frequently outperform more sophisticated ones. Realizing that large errors always exist due to possibly faraway locations with similar WiFi signatures, authors in [12], [33] attempt to incorporate acoustic ranging in WiFi fingerprinting to limit the large tail errors. Although significant improvements are achieved, these approaches either rely on ranging among a dense crowd of users or require calibrating additional information. Recent works also explore new fingerprint features such as neighbour relative RSSs [47], neighbour RSS gradient [21] and RSS ratio over multiple antennas [48] for accurate and robust fingerprinting. To completely bypass the instability of RSS, physical layer Channel State Information (CSI) is recently introduced and achieves an accuracy of ∼1m [17], but at the cost of ubiquity degradation (since CSI is unavailable on most commodity smartphones).

To reduce computational complexity, d Different criteria for AP’s discriminatory ability such as InfoGain [23] and MaxMean [35] have been proposed to choose a subset of APs for localization. A more intuitive method called RSS cutoff, i.e., discarding RSS values below a specific threshold, is preferred in commercial products [26]. These methods conduct AP selection mainly to reduce the computational complexity. In contrast, we target at appropriately exploiting all available APs for more accurate fingerprint matching. Accounting for human body blockage, fingerprints are typically collected for multiple directions [30], which may increase labour efforts while offers limited gains. An elaborate model is designed in [31] to compensate for the signal attenuation of human body and thus generate orientation-independent fingerprints from measurements on just one orientation. In contrast to labour-intensive measurements or vulnerable models, we resort to exploit robust regression techniques to achieve effective robustness to RSS uncertainties.

Ranging-based techniques. These schemes calculate locations based on geometrical models rather than search for best-fitted signatures from pre-labeled reference database. The prevalent LDPL model, for instance, builds up a semi-statistical function between RSS values and RF propagation distances [15], [49]. These approaches trade measurement efforts for the cost of decreasing localization accuracy. EZ [49] employs a modeling method assuming no knowledge of physical layout or AP locations, and reports median error of 7 meters. Apart from RSS-based ranging, CSI is recently used to obtain for highly accurate distance and angle estimation [14]. Acoustic ranging is also employed for fine-grained indoor localization, such as Centour [33], Guoguo [6], etc.

Different from previous works that introduce additional information or extra signal sources for high accuracy, we identify the root causes of location errors in WiFi fingerprint-based localization for mobile devices. Specifically, we uncover and solved the transitional fingerprint problem, which has not been noticed in existing works. Aiming at a ubiquitous location service, we follow a typical RSS fingerprint-based scheme to design DorFin, which is thus amendable to integrate with existing approaches and can be easily incorporated in deployed systems with little efforts, making it a promising scheme in practical applications.

# 6 CONCLUSIONS

While WiFi fingerprint-based localization acts as the dominant scheme in indoor localization, the accuracy challenge remains a primary concern. In this paper, we identify several crucial causes of localization errors in fingerprint-based schemes. These observations then lead us to the design of a new WiFi fingerprinting scheme which successfully reduces the mean and 95th percentile location errors to 2.5 meters and 6.2 meters, without degrading ubiquity nor increasing the costs. Our approach marks a significant progress in RSS fingerprint-based indoor localization, especially for smartphones, and sheds lights on practical deployment in the real world.

# ACKNOWLEDGMENT

This work is supported in part by the NSFC under grant No. 61672319, 61522110, and 61632008.

# REFERENCES

[1] P. Bahl and V. N. Padmanabhan, “RADAR: an in-building RFbased user location and tracking system,” in Proceedings of IEEE INFOCOM, 2000.   
[2] M. Youssef and A. Agrawala, “The horus location determination system,” Wirel. Netw., vol. 14, no. 3, pp. 357–374, Jun. 2008.   
[3] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil, “LANDMARC: indoor location sensing using active RFID,” Wireless Networks, vol. 10, no. 6, pp. 701–710, 2004.   
[4] J. Wang and D. Katabi, “Dude, where’s my card? RFID positioning that works with multipath and non-line of sight,” in Proceedings of ACM SIGCOMM, 2013.

[5] S. P. Tarzia, P. A. Dinda, R. P. Dick, and G. Memik, “Indoor localization without infrastructure using the acoustic background spectrum,” in Proceedings of ACM MobiSys, 2011.   
[6] K. Liu, X. Liu, and X. Li, “Guoguo: Enabling fine-grained indoor localization via smartphone,” in Proceedings of ACM MobiSys, 2013.   
[7] N. B. Priyantha, A. Chakraborty, and H. Balakrishnan, “The cricket location-support system,” in Proceedings of ACM MobiCom, 2000.   
[8] P. Lazik and A. Rowe, “Indoor pseudo-ranging of mobile devices using ultrasonic chirps,” in Proceedings of ACM SenSys, 2012.   
[9] C. Wu, Z. Yang, and Y. Liu, “Smartphones based crowdsourcing for indoor localization,” Mobile Computing, IEEE Transactions on, vol. 14, no. 2, pp. 444–457, Feb 2015.   
[10] G. Shen, Z. Chen, P. Zhang, T. Moscibroda, and Y. Zhang, “Walkie-markie: indoor pathway mapping made easy,” in Proceedings of USENIX NSDI, 2013.   
[11] H. Wang, S. Sen, A. Elgohary, M. Farid, M. Youssef, and R. R. Choudhury, “No need to war-drive: unsupervised indoor localization,” in Proceedings of ACM MobiSys, 2012.   
[12] H. Liu, J. Yang, S. Sidhom, Y. Wang, Y. Chen, and F. Ye, “Accurate wifi based localization for smartphones using peer assistance,” Mobile Computing, IEEE Transactions on, vol. 13, no. 10, pp. 2199–2214, Oct 2014.   
[13] A. Rai, K. K. Chintalapudi, V. N. Padmanabhan, and R. Sen, “Zee: zero-effort crowdsourcing for indoor localization,” in Proceedings of ACM MobiCom, 2012.   
[14] S. Sen, J. Lee, K.-H. Kim, and C. Paul, “Avoiding multipath to revive inbuilding wifi localization,” in Proceedings of ACM MobiSys, 2013.   
[15] H. Lim, L. C. Kung, J. C. Hou, and H. Luo, “Zero-configuration indoor localization over IEEE 802.11 wireless infrastructure,” Wireless Networks, vol. 16, no. 2, pp. 405–420, 2010.   
[16] D. Turner, S. Savage, and A. C. Snoeren, “On the empirical performance of self-calibrating wifi location systems,” in Proceedings of IEEE Conference on Local Computer Networks (LCN), 2011.   
[17] S. Sen, B. Radunovic, R. R. Choudhury, and T. Minka, “You are facing the mona lisa: spot localization using PHY layer information,” in Proceedings of ACM MobiSys, 2012.   
[18] H. Xu, Z. Yang, Z. Zhou, L. Shangguan, K. Yi, and Y. Liu, “Enhancing wifi-based localization with visual clues,” in Proceedings of ACM UbiComp, 2015, pp. 963–974.   
[19] L. Li, G. Shen, C. Zhao, T. Moscibroda, J.-H. Lin, and F. Zhao, “Experiencing and Handling the Diversity in Data Density and Environmental Locality in an Indoor Positioning Service,” in Proceedings of ACM MobiCom, 2014.   
[20] S. He, T. Hu, and S.-H. G. Chan, “Contour-based trilateration for indoor fingerprinting localization,” in Proceedings of ACM SenSys, 2015.   
[21] Y. Shu, Y. Huang, J. Zhang, P. Cou, P. Cheng, J. Chen, and K. G. Shin, “Gradient-based fingerprinting for indoor localization and tracking,” IEEE Transactions on Industrial Electronics, vol. 63, no. 4, pp. 2424–2433, April 2016.   
[22] A. Haeberlen, E. Flannery, A. M. Ladd, A. Rudys, D. S. Wallach, and L. E. Kavraki, “Practical robust localization over large-scale 802.11 wireless networks,” in Proceedings of ACM MobiCom, 2004.   
[23] Y. Chen, Q. Yang, J. Yin, and X. Chai, “Power-efficient accesspoint selection for indoor location estimation,” Knowledge and Data Engineering, IEEE Transactions on, vol. 18, no. 7, pp. 877– 888, 2006.   
[24] P. Jiang, Y. Zhang, W. Fu, H. Liu, and X. Su, “Indoor mobile localization based on wi-fi fingerprints important access point,” International Journal of Distributed Sensor Networks, vol. 2015, p. 45, 2015.   
[25] P. Mirowski, D. Milioris, P. Whiting, and T. Kam Ho, “Probabilistic radio-frequency fingerprinting and localization on the run,” Bell Labs Technical Journal, vol. 18, no. 4, pp. 111–133, 2014.   
[26] I. Cisco Systems, “Wi-fi location-based services 4.1 design guide,” 2013.   
[27] S.-H. Fang and T.-N. Lin, “Principal component localization in indoor wlan environments,” Mobile Computing, IEEE Transactions on, vol. 11, no. 1, pp. 100–110, 2012.

[28] T. B. Welch, R. L. Musselman, B. A. Emessiene, P. D. Gift, D. K. Choudhury, D. N. Cassadine, and S. M. Yano, “The effects of the human body on uwb signal propagation in an indoor environment,” Selected Areas in Communications, IEEE Journal on, vol. 20, no. 9, pp. 1778–1782, 2002.   
[29] Z. Zhang, X. Zhou, W. Zhang, Y. Zhang, G. Wang, B. Y. Zhao, and H. Zheng, “I am the antenna: accurate outdoor AP location using smartphones,” in Proceedings of ACM MobiCom, 2011.   
[30] A. S. Paul and E. Wan, “Rssi-based indoor localization and tracking using sigma-point kalman smoothers,” Selected Topics in Signal Processing, IEEE Journal of, vol. 3, no. 5, pp. 860–873, 2009.   
[31] N. Fet, M. Handte, and P. J. Marron, “A model for wlan´ signal attenuation of the human body,” in Proceedings of ACM UbiComp, 2013.   
[32] W. Sun, J. Liu, C. Wu, Z. Yang, X. Zhang, and Y. Liu, “Moloc: on distinguishing fingerprint twins,” in Proceedings of IEEE ICDCS, 2013.   
[33] R. Nandakumar, K. K. Chintalapudi, and V. N. Padmanabhan, “Centaur: locating devices in an office environment,” in Proceedings of ACM MobiCom, 2012.   
[34] M. Youssef and A. Agrawala, “Handling samples correlation in the horus system,” in Proceedings of IEEE INFOCOM, 2004.   
[35] M. A. Youssef, A. Agrawala, and A. Udaya Shankar, “WLAN location determination via clustering and probability distributions,” in Proceedings of IEEE PerCom, 2003.   
[36] “IEEE 802.11, part11: Wireless LAN medium access control (MAC) and physical layer (PHY) specifications,” 2012.   
[37] J. Yin, Q. Yang, and L. Ni, “Learning adaptive temporal radio maps for signal-strength-based location estimation,” Mobile Computing, IEEE Transactions on, vol. 7, no. 7, pp. 869–883, 2008.   
[38] P. Bahl, V. N. Padmanabhan, and A. Balachandran, “Enhancements to the radar user location and tracking system,” Tech. Rep., 2000.   
[39] S. Hilsenbeck, D. Bobkov, G. Schroth, R. Huitl, and E. Steinbach, “Graph-based data fusion of pedometer and wifi measurements for mobile indoor positioning,” in Proceedings of ACM UbiComp, 2014, pp. 147–158.   
[40] C. Wu, Z. Yang, Y. Xu, Y. Zhao, and Y. Liu, “Human mobility enhances global positioning accuracy for mobile phone localization,” Parallel and Distributed Systems, IEEE Transactions on, vol. 26, no. 1, pp. 131–141, Jan 2015.   
[41] P. J. Rousseeuw and A. M. Leroy, Robust regression and outlier detection. Wiley, 2005.   
[42] P. J. Rousseeuw, “Least median of squares regression,” Journal of the American statistical association, vol. 79, no. 388, pp. 871– 880, 1984.   
[43] T. S. Rappaport et al., Wireless communications: principles and practice. Prentice Hall PTR New Jersey, 1996, vol. 2.   
[44] Z. Yang, C. Wu, Z. Zhou, X. Zhang, X. Wang, and Y. Liu, “Mobility increases localizability: A survey on wireless indoor localization using inertial sensors,” ACM Computing Surveys, vol. 47, no. 3, pp. 54:1–54:34, Apr. 2015.   
[45] P. Mirowski, H. Steck, P. Whiting, R. Palaniappan, M. Mac-Donald, and T. K. Ho, “Kl-divergence kernel regression for non-gaussian fingerprint based localization,” in Proceedings of IEEE IPIN, 2011, pp. 1–10.   
[46] C. Wu, Z. Yang, C. Xiao, C. Yang, Y. Liu, and M. Liu, “Static power of mobile devices: Self-updating radio maps for wireless indoor localization,” in Proceedings of IEEE INFOCOM, April 2015, pp. 2497–2505.   
[47] K. Lin, M. Chen, J. Deng, M. M. Hassan, and G. Fortino, “Enhanced fingerprinting and trajectory prediction for iot localization in smart buildings,” IEEE Transactions on Automation Science and Engineering, vol. 13, no. 3, pp. 1294–1307, July 2016.   
[48] W. Cheng, K. Tan, V. Omwando, J. Zhu, and P. Mohapatra, “Rss-ratio for enhancing performance of rss-based applications,” in Proceedings of IEEE INFOCOM, 2013.   
[49] K. Chintalapudi, A. Padmanabha Iyer, and V. N. Padmanabhan, “Indoor localization without the pain,” in Proceedings of ACM MobiCom, 2010.

![](images/59a0cc98dea906df4f453f93e70c1861d39b8b82bb19dbc85583b634c6525d06.jpg)



Chenshu Wu received his B.E. degree in School of Software in 2010 and Ph.D. degree in Department of Computer Science in 2015, both from Tsinghua University, Beijing, China. He is currently a Postdoc researcher in School of Software, Tsinghua University. His research interests include wireless networks and pervasive computing. He is a member of the IEEE and the ACM.

![](images/895864a52e69e968f56f36c4dfab81b2bfb0216368d5fcff4bc956b92030ec6d.jpg)



Zheng Yang received a B.E. degree in computer science from Tsinghua University in 2006 and a Ph.D. degree in computer science from Hong Kong University of Science and Technology in 2010. He is currently an associate professor in Tsinghua University. His main research interests include wireless ad-hoc/sensor networks and mobile computing. He is a member of the IEEE and the ACM.

![](images/8a939646895ebf4b62bbbb84a1dc34ad94b20c6e7a0cb20cfe03ae18a9dc242e.jpg)



Zimu Zhou is currently a postdoctoral researcher at the Computer Engineering and Networks Laboratory (TIK), ETH Zurich. He received his B.E. degree from the Department of Electronic Engineering, Tsinghua University in 2011 and Ph.D. degree from the Department of Computer Science and Engineering, the Hong Kong University of Science and Technology in 2015. He is a member of the IEEE.

![](images/6fa666f0d02e1a156a89275e6f7fffcbafa905da7e89b030c4c689e7a3153d38.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is now EMC Chair Professor at Tsinghua University. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. He is a Fellow of the ACM and the IEEE.

![](images/744914ac2f1855fbfabf19cc422eefc0dcdbdc19c67ee45fd5a03a80fb62c864.jpg)



Mingyan Liu received her Ph.D. Degree in electrical engineering from the University of Maryland, College Park, in 2000 and has since been with the Department of Electrical Engineering and Computer Science at the University of Michigan, Ann Arbor, where she is currently a Professor. Her research interests are in optimal resource allocation, performance modeling and analysis, and energy efficient design of wireless, ad hoc, and sensor networks. She is a Fellow of the IEEE.