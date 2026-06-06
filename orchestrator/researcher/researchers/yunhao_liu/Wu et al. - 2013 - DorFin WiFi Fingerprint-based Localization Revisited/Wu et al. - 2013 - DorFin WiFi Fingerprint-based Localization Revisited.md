# DorFin: WiFi Fingerprint-based Localization Revisited

Chenshu Wu∗, Zheng Yang∗, Zimu Zhou†, Yunhao Liu∗ and Mingyan Liu‡

∗School of Software and TNList, Tsinghua University

†CSE, Hong Kong University of Science & Technology

‡Department of EECS, University of Michigan

{wu, yang, zimuzhou, yunhao}@greenorbs.com, mingyan@eecs.umich.edu

Abstract—Although WiFi fingerprint-based indoor localization is attractive, its accuracy remains a primary challenge especially in mobile environments. Existing approaches either appeal to physical layer information or rely on extra wireless signals for high accuracy. In this paper, we revisit the RSS fingerprint-based localization scheme and reveal crucial observations that act as the root causes of localization errors, yet are surprisingly overlooked or even unseen in previous works. Specifically, we recognize APs’ diverse discrimination for fingerprinting a specific location, observe the RSS inconsistency caused by signal fluctuations and human body blockages, and uncover the RSS outdated problem on commodity smartphones. Inspired by these insights, we devise a discrimination factor to quantify different APs’ discrimination, incorporate robust regression to tolerate outlier measurements, and reassemble different fingerprints to cope with outdated RSSs. Combining these techniques in a unified solution, we propose DorFin, a novel scheme of fingerprint generation, representation, and matching, which yields remarkable accuracy without incurring extra cost. Extensive experiments demonstrate that DorFin achieves mean error of 2 meters and more importantly, bounds the 95th percentile error under 5.5 meters; these are about 56% and 69% lower, respectively, compared with the stateof-the-art schemes such as Horus and RADAR.

# I. INTRODUCTION

The proliferation of mobile computing has spurred extensive interests in location-based services, leading to an urgent need for fine-grained location. The past decade has witnessed the conceptualization and development of various wireless indoor localization techniques, including WiFi [1], [2], RFID [3], [4], acoustic signals [5], [6], ultrasound [7], [8], etc. Due to the wide deployment and availability of WiFi infrastructure, WiFi fingerprint-based indoor localization has become one of the most attractive localization techniques [9]–[14]. Roughly speaking, a fingerprint-based scheme consists of two stages: site survey and fingerprint matching. During site survey (a.k.a calibration or war-driving), received signal strengths (RSS) from multiple WiFi access points (APs) are recorded at known locations to construct a fingerprint database. To locate a user, localization algorithms match his RSS measurements against the pre-labeled records and estimate his location to be the one with the best-fitted fingerprint.

There is generally a tradeoff between accuracy, ubiquity, and cost in designing a pervasive indoor localization system. Accuracy has long been the primary challenge especially in mobile environments. Even schemes that have been reported to have very high accuracy in some instances, e.g., [2], [13], [15], can experience rapid performance degradation in realistic environments, with median error consistently above 5 meters [16]. In addition, there are always unacceptably large tail errors, e.g., 10∼20m or larger. Recent works [12], [16] found that large errors of prior works could range from 12 to around 40 meters. Mobility further deteriorates the performance especially for smartphone based methods. Efforts to gain high accuracy include to leverage physical layer information [17] and incorporate acoustic ranging [6], [12], among others. These methods typically either rely on information unavailable on commodity smartphones, or resort to unrealistic cooperation among a dense crowd of peers. In this paper, we revisit the WiFi fingerprinting localization framework and ask whether it is possible to achieve accurate and robust fingerprint-based localization, especially for mobile phones, without degrading the ubiquity or increasing the costs.

To investigate the root cause of limited localization accuracy, we conduct extensive experiments and uncover the following characteristics of WiFi fingerprint-based localization: 1) APs have different discriminatory capabilities to fingerprint a specific location since RSS changes are inversely proportional to the physical distance, subject to radio signal propagation laws. Intuitively, faraway APs may lead to large location estimation errors while close ones can help mitigate the location uncertainty. 2) Biased RSS measurements caused by signal fluctuation and human body blockage may present themselves as outliers in fingerprint matching. Human body blockage to smartphones can remove line-of-sight and weaken the received signal by up to 10dB, thus greatly exaggerating the discrepancies of fingerprints measured from the same location. 3) RSS measurements may be outdated due to hardware and software limitations of commodity wireless devices. In other words, latest reported RSS values could be duplicates of previous scans performed several seconds ago. Considering user mobility, the outdated RSS could in fact be measurements done at a previous location, resulting in outdated fingerprints consisting of RSS measurements from multiple locations. In overlooking such outdated information, previous works directly compare the outdated fingerprints with those collected at a single location, incurring frequent fingerprint mismatches. The above are key reasons behind location errors of fingerprint-based schemes, especially in mobile environments; yet surprisingly they have not been adequately addressed in existing works.

![](images/5b5961b03d5ca7e327e62cb351506fef7255aa31f2c79211ddd753c7fb98abf0.jpg)



Figure 1. Discrimination Diversity

![](images/07417b2d73622a30726237e44bdc14876b433c7932b20683fb7772ee31ef3fec.jpg)



Figure 2. Fingerprint Inconsistency

![](images/8f3d22ace14595bdc83111c583194c722f087ed2d16152e1457d60926e49daea.jpg)



Figure 3. Outdated fingerprints: A glance of scanning results from Android OS

With these observations in mind, we design DorFin (named after Discrimination diversity, Outdated RSSs, and Fingerprint inconsistency), a new fingerprint-based scheme for highly accurate localization. DorFin includes three main components. First, we quantitatively differentiate distinct AP’s discriminatory ability w.r.t. a specific location. APs with stronger ability are emphasized with more weights in fingerprint matching, while others are de-emphasized. Second, noting fingerprint inconsistency, we apply a robust regression technique in fingerprint matching, in the hope of bounding the impact of RSS outlier values and ensuring accuracy under noisy measurements. Finally, we propose phantom fingerprints that incorporate multiple fingerprints in the fingerprint database to deal with the outdated RSS values. Phantom fingerprints are assembled according to the spatial constraints of outdated RSSs, which are derived by monitoring user mobility using smartphones’ built-in inertial sensors. Integrating these components, we design a uniform fingerprint similarity metric which further takes account of common AP ratio as a factor to mitigate errouneous matches of distant fingerprints.

To validate our design, we implement DorFin on commodity devices and conduct extensive experiments in multiple buildings. Experimental results demonstrate competitive performance of DorFin to solutions based on physical layer information or on additional ranging techniques. In addition to the average accuracy of 2m, DorFin significantly reduces large location errors by limiting the 95 percentile errors in 5.5m, both outperforming the state-of-the-art schemes like Horus by 56% and 69%, respectively. Using only the most essential RSS and requiring no extra hardware, we believe our approach takes an important step forward to accurate location estimation on smartphones with the prevalent WiFi infrastructure.

Our contributions are summarized as follows:

• We uncover several crucial insights that explain the root cause of location errors but have not been adequately studied in existing literature.   
• We are the first to tackle the outdated RSS problem and the fingerprint inconsistency in WiFi fingerprint-based localization. We design an effective scheme for accurate and robust localization leveraging only the prevalent RSS, requiring no extra information or additional hardware.   
• We implement a prototype system and conduct real

world experiments in multiple buildings using commodity devices. In addition to the remarkable performance, our method can be conveniently integrated in existing WiFi fingerprint-based localization systems.

The rest of the paper is organized as follows. Section II presents our preliminary measurements and basic observations. The method design is detailed in Section III, followed with the experiments and performance evaluation in Section IV. We discuss the state-of-the-art of indoor localization in Section V and conclude the paper in Section VI.

# II. PRELIMINARY AND MEASUREMENTS

In this section, we review the classical RSS fingerprinting problem and investigate fundamental characteristics of radio fingerprints through real measurements. Our preliminary results show some crucial features, which, having been largely overlooked in the past, shed light on how to achieve high accuracy of fingerprint-based localization.

# A. Problem Statement

The working process of a typical fingerprint-based localization scheme consists of two stages: site survey and fingerprint matching. During site survey, wireless fingerprints (i.e., the set of RSS values from multiple APs) are measured and recorded at every location of interests. A fingerprint database (a.k.a radio map) is accordingly constructed, in which the fingerprint-location relationships are stored. To locate a user who sends a location query with his current RSS fingerprint, localization algorithms retrieve the fingerprint database and return the location of the matched fingerprint as the user’s location estimation.

Denote a fingerprint as $\pmb { f } = [ f _ { i } , i = 1 , \cdots , n ]$ , where $f _ { i }$ is the RSS value of the $\mathbf { A P } \ A _ { i } \in \mathcal { A } ,$ , the set of n detectable APs appearing in $f .$ For two fingerprints $f$ and $f ^ { \prime }$ , denote the RSS difference (RSD) vector as $\delta = [ \delta _ { i } , i = 1 , \cdots , p ]$ where $\delta _ { i } = | f _ { i } - f _ { i } ^ { \prime } |$ indicates the RSD of AP $A _ { i } \in { \mathcal { A } } \cup A ^ { \prime }$ in the two fingerprints and $p = | { \mathcal { A } } \cup { \mathcal { A } } ^ { \prime } |$ . Since $f$ and $f ^ { \prime }$ do not necessarily contain identical sets of APs, we set $f _ { i }$ $( f _ { i } ^ { \prime } )$ to -100, the default minimum RSS value, if $A _ { i } ~ \notin ~ { \mathcal { A } }$ (A0). Let $\phi$ be the dissimilarity between $f$ and $f ^ { \prime } ,$ which, if measured by Euclidean distance, can be calculated as $\begin{array} { r } { \phi ( \pmb { f } , \pmb { f ^ { \prime } } ) = \| \pmb { \delta } \| = \sqrt { \sum _ { i = 1 } ^ { p } \delta _ { i } ^ { 2 } } } \end{array}$ . For all fingerprints stored in the fingerprint database ${ \mathcal { F } } ,$ , the goal of fingerprint matching is to find the fingerprint $f ^ { * }$ that achieves the highest similarity with respect to the query fingerprint $f .$ Formally,

![](images/b3213c00776b52af8e174911381fe5532f72348f02a6106bb6414ebcbc965c08.jpg)



(a) Outdated rates over different APs

![](images/f52c88e94a022d7355e87ec82d270e9e91eac651d4cfd476adf72b86dd495245.jpg)



(b) Time delays of outdated RSSs

![](images/34e3c0d307ec8666ee29fe4e5b291db786f68be31c448c47f1a4409b29e2f44c.jpg)



(c) Time delays of outdated fingerprints   
Figure 4. Outdated RSS phenomenon: The reported RSSs in one fingerprint might be outdated.

$$
\boldsymbol {f} ^ {*} = \underset {\boldsymbol {f} _ {i} \in \mathcal {F}} {\arg \min} \phi (\boldsymbol {f}, \boldsymbol {f} _ {i}). \tag {1}
$$

Then the user’s location is estimated as the corresponding location $L ( f ^ { * } )$ of $f ^ { * }$ . Assumimg the true location of $f$ is $L ( f )$ , the location estimation error is given by $\varepsilon = \| L ( f ) - L ( f ^ { * } ) |$ .

# B. Observations

Observation 1 (Discrimination Diversity) APs have diverse discrimination capability to fingerprint a specific location, subject to inherent constraints of radio signal propagation.

Discrimination capability is referred to as the ability of one AP to distinguish a specific location when using its RSS observations as fingerprints. Ideally, subject to the propagation law of wireless signals, RSS decays logarithmically with propagation distance d. More formally, $R S S \propto - \log ( d )$ , indicating that $\frac { \Delta R S S } { \Delta d } \propto - \frac { 1 } { d }$ ∆d , where $\Delta R S S$ denotes the RSS change and $\Delta d$ is the corresponding distance change. In other words, an identical $\Delta R S S$ can imply a smaller distance change $\Delta d$ at closer locations, or a larger ∆d at faraway positions. As shown in Figure 1, RSS variance of 1dB in value corresponds to vastly different changes in physical distance, depending on the specific d. Hence, faraway APs may cause large errors in location estimation, while close ones can conversely mitigate the errors. In a nutshell, distance changes indicated by RSS variances depend on the transmitter-receiver distance, leading to diverse discrimination capability across different locations.

Observation 2 (Fingerprint Inconsistency) The majority of APs hold similar RSSs for fingerprints from the same/close locations while a small fraction may exhibit large differences due to environmental dynamics and human body blockages.

Location errors originate from unmatched fingerprints measured from the same/close locations. Our investigation on these fingerprints indicate that a majority of APs exhibit relatively stable RSSs even when these fingerprints are not matched. That is to say, the fingerprint dissimilarity (under certain metric such as Euclidean distance) is primarily produced by the drastically fluctuating RSSs of a small portion of APs, which is, however, obviously not caused by location changes, but probably stems from ambient dynamics and human body blocking effects [18], [19] especially in mobile environments.

As shown in Figure 2, signal strengths perceived by smartphones decrease significantly when the human body blocks the direct path of signal propagation, compared to when the user is facing the AP. These weakened RSS observations of blocked APs tend to deviate from the normal profiles, resulting in abnormal RSSs when compared with fingerprints measured during the training phase. Taking Figure 2 as an example, the normal RSS profile absent of body blockage is measured to be $\textbf { \textit { f } } = \ \left[ - 4 0 , - 6 5 , - 5 0 \right]$ . When a user is present and faces left, the right AP is blocked, resulting in a biased fingerprint $\pmb { f } _ { \mathrm { l e f t } } = [ - 4 0 , - 6 5 , - 6 5 ]$ (for simplicity, we assume RSSs of unblocked APs remain unchanged). When facing right, the line of sight of the left AP is blocked and its RSS is correspondingly weakened, creating a fingerprint ${ f _ { \mathrm { r i g h t } } = [ - 5 2 , - 6 5 , - 5 0 ] }$ . Then comparing $\pmb { f } _ { \mathrm { l e f t } }$ and $f _ { \mathrm { r i g h t } }$ with the normal f produces inconsistent RSD distributions $\delta _ { \mathrm { l e f t } } = [ 0 , 0 , 1 5 ]$ and $\delta _ { \mathrm { r i g h t } } = [ 1 2 , 0 , 0 ]$ , both generating abnormally larger fingerprint dissimilarity and ultimately leading to greater location uncertainty. Such inconsistency, however, has largely been overlooked in existing work but is ever-present especially for mobile users.

Observation 3 (Outdated Fingerprints) The measured RSS might be outdated due to incomplete scanning results, caused by software and hardware restrictions.

Commodity smartphones acquire WLAN information in a passive scanning mode by listening to periodic beacons from surrounding APs on all working channels. In this mode, the time a client stays on a channel is 100ms by default, which is specified by the 802.11 standard [20] and is equal to the default beacon interval. Consequently, the latency incurred in capturing the AP information for 2.4GHz WiFi is about 1,100ms since there are 11 available channels. In practice, it takes about 1∼1.5 seconds for mainstream Android OS to complete a scan with commodity smartphones. Due to beacon conflicts and channel collisions, the beacon interval of 100ms cannot be always guaranteed, potentially resulting in some missed APs during a scan. However, to maintain quality of service, these missed APs can still appear in the scanning results by duplicating information from last several scans a few seconds ago.

![](images/0a3e9101f1958a467a606b525c2c9efa3e96876085bf351834b82534503cfeec.jpg)



Figure 5. System architecture

![](images/513ca479362ce522e99fa3f8f58647f11513bf17415efbcf8f71955837801b8d.jpg)



Figure 6. Phantom fingerprint

![](images/3b5b6c48c462ec59b14e6e8ea1c1b58fe5cbc0afe0d324a0416a222965a953eb.jpg)



Figure 7. Bequeathal locations

As shown in Figure 4, a significant portion of APs experience high outdated rates, ranging from 2% to 25%. In particular, about 60% of the outdated RSSs bear an outdated delay of 1.4s, while around 20% and 15% has a delay of 2.7s and 4s, respectively. Translated into fingerprints, Figure 4c indicates that over 80% of fingerprints contain outdated RSSs, and for about 20% the maximum delay time exceeds 4s.

If a user is stationary, such outdated phenomenon has little impact on location fingerprinting since outdated RSSs are also measured from the same position. In mobile environments, however, users may have moved several meters away between consecutive scans, resulting in fingerprints comprised by RSS values that are actually observed at multiple locations, which we called outdated fingerprints. Previous works treat these outdated fingerprints as normal ones and compare them directly to those stored in the fingerprint DB, which are all collected at single locations. Obviously, matching fingerprints mixed from multiple locations to those from single positions may result in frequent fingerprint mismatches or even localization failures. In conclusion, serious outdated RSS measurements exist in WiFi-based location fingerprinting, and also contribute to location estimation error especially in a mobile environment.

In this study, we reconsider the RSS fingerprinting scheme based on these surprisingly overlooked observations. Specifically, we design DorFin, an accurate, robust, and practical indoor localization method which 1) quantitatively differentiates individual APs according to their location discrimination capability, 2) applies robust regression on inconsistent fingerprints, and 3) recombines phantom fingerprints to handle outdated RSS values in mobile environments. The following section details our design.

# III. DESIGN METHODOLOGY

As illustrated in Figure 5, the proposed solution includes a discriminatory policy, a phantom fingerprint assembling module, a robust regression procedure, and a normal fingerprint matching scheme.

# A. Discriminatory Policy

Given that APs have diverse discrimination capability to fingerprint a specific location, it is inappropriate, and also unnecessary, to match two fingerprints with all APs equally involved. More accurate location estimations can be achieved by relying on the more discriminative APs, and limiting or even eliminating the influence of those fluctuating and distant ones. Toward this goal, we attempt to seek a discrimination metric that complies with physical constraints of signal propagation and simultaneously stays robust to RSS fluctuations.

To quantitatively differentiate each AP for a specific location, we define a discrimination factor by estimating the physical distance between the AP and the mobile client using the following Log-Distance Path Loss (LDPL) model [21]:

$$
P _ {d} = P _ {d _ {0}} - 1 0 \gamma \log (\frac {d}{d _ {0}}), \tag {2}
$$

where $P _ { d _ { 0 } }$ denotes the received power at a distance $d _ { 0 }$ (which usually takes the value of one meter), γ is the path loss exponent, and $P _ { d }$ is the RSS in decibel measured at a distance of $d$ (in meters). Deriving the distance to AP $A _ { i }$ from the LDPL model, we calculate its discrimination factor in fingerprint $f _ { u }$ to location $L _ { u }$ as follows:

$$
\rho_ {i} ^ {u} = \frac {1}{d _ {i} ^ {u}} = 1 0 ^ {\frac {f _ {u , i} - P d _ {0}}{1 0 \gamma}}, \tag {3}
$$

where $d _ { i } ^ { u }$ is the estimated physical distance between $A _ { i }$ and $L _ { u }$ . The rationale of using the reciprocal of physical distance lies in that it is consistent with the derivative of the LDPL equation, which indicates the RSS change $\begin{array} { r } { \Delta R S S \propto - \frac { 1 } { d } } \end{array}$ .

While the exponential $\rho _ { i } ^ { u }$ effectively discriminates different APs, it may also induce unnecessary matching errors in case of fluctuating RSSs. Consider one of the APs in a fingerprint that fluctuates to a very large value (e.g., -45dBm). In this case, the effects of other representative APs, which could hold considerable RSSs (e.g., up to -60dBm) and are thus discriminative, may become negligible since they can only get inappreciable factors three or four times smaller than the fluctuating AP. Hence to cope with noisy RSSs, we additionally incorporate a sigmoid function to retain the effects of most discriminative APs. Mathematically, $\rho _ { i } ^ { u }$ is adjusted as follows:

$$
\rho_ {i} ^ {u} = \left\{ \begin{array}{l l} 1 0 ^ {\frac {f _ {u , i} - P _ {d _ {0}}}{1 0 \gamma}} & \text { if } f _ {u, i} \leq f _ {0} \\ \frac {1}{a} \left(1 + e ^ {- 2 \left(\frac {f _ {u , i} + 1 0 0}{1 0} - c\right)}\right) ^ {- 1} & \text { otherwise } \end{array} \right. \tag {4}
$$

where all constant parameters $f _ { 0 } ,$ , a watershed RSS value, a and c can be determined by general empirical values and measurements. Afterwards, the discrimination factor is normalized such that $\textstyle \sum _ { k = 1 } ^ { n _ { u } } \rho _ { k } ^ { u } \ = \ 1$ nu . The normalized $\rho _ { i } ^ { u }$ then serves as a differential weight which will be attached to the RSD of $A _ { i }$ between $f _ { u }$ and another fingerprint when computing their dissimilarity, as detailed in Section III-D.

# B. Phantom Fingerprints

As mentioned above, RSS of a specific AP reported in a query fingerprint may be outdated. If a user is stationary, this has little effect on fingerprint matching. In mobile environments, however, the outdated data may have been measured several seconds ago when the user was at another location. Subsequently, comparing fingerprint mixed with measurements from multiple locations with samples from one location can lead to false fingerprint matches.

Intuitively, a query fingerprint consisting of RSS features of different locations should be matched with fingerprints recombined by measurements from multiple locations, which, however, are not directly available in the fingerprint database. In this sense, one needs to assemble special fingerprints, i.e., combinations of fingerprints from multiple locations, for matching, as shown in Figure 6. These newly constructed fingerprints do not yet exist in the fingerprint database, and will be referred to as phantom fingerprints.

For a fingerprint $\textbf { \textit { f } } = \ [ f _ { i } , i \ = \ 1 , \cdot \cdot \ , n ]$ , denote the encountered timestamp of each $\mathsf { A P } \ A _ { i }$ in f by $t _ { i } .$ . Recall Figure 3, the scanning delay is typically longer than 1 second by our measurements while the differences of all APs’ detected time in one fingerprint are usually small (indicated by the Time Synchronization Function1 (TSF) timestamp). Hence, if the time difference between two APs in one fingerprint exceeds a certain length, e.g., 0.5s, then the earlier one is definitely outdated. In particular, for $\mathrm { A P } \ A _ { k } ,$ the outdated duration $\Delta t _ { k }$ is computed by $\Delta t _ { k } = \operatorname* { m a x } _ { i = 1 \cdots , n } t _ { i } - t _ { k }$ i=1,··· ,n .

As illustrated in Figure 6, assume that $f _ { k }$ is actually the measurement of $A _ { k }$ at a previous location, called bequeathal location (BL), where a user was present $\Delta t _ { k }$ seconds ago. Further assume that the distance and direction from the BL to the user’s current location is $\ell _ { k }$ and $\theta _ { k }$ , respectively (we will describe how to compute $\ell _ { k }$ and $\theta _ { k }$ shortly). Then when comparing $f$ with a candidate location, say, $L _ { z }$ , instead of directly computing the dissimilarity between $f$ and $f _ { z } ,$ , a sample fingerprint of $L _ { z }$ , we match it against the phantom fingerprints $\pmb { \mathscr { f } } _ { z }$ assembled from $f _ { z }$ and $f _ { B L ( z ) } $ , fingerprint from the BL. Concretely, the RSS value $f _ { k }$ in f is replaced by that of the same AP in $f _ { B L ( z ) }$ . In case of multiple outdated RSSs, all of them are replaced according to their individual BLs, finally resulting in a precise phantom fingerprint $\pmb { \mathscr { f } } _ { z }$ .

The distance offset \` and direction θ can be estimated by dead reckoning method using smartphone built-in inertial sensors like accelerometer, gyroscope, and compass [10], [11], [13], [22]. Specifically, we adopt the method proposed in [23], which counts steps as accurately as up to 98%. The footsteps could then be converted to physical displacement by multiplying with the user’s step length, which can be automatically tracked [13]. The direction, on the other hand, is estimated using gyroscope and compass as [13]. In the following, we demonstrate that although dead-reckoning may not be adequate for localization, it is sufficient for our purpose of estimating \` and θ.

Due to noisy sensors and arbitrary human behavior, \` and $\theta$ cannot be 100% accurately computed. To cope with the erroneous estimations, we introduce an error range for each of them, denoted as ∆\` and $\Delta \theta ,$ , respectively, and demonstrate that the procedure of choosing BLs can tolerate these errors gracefully. Mathematically, as shown in Figure 7, potential BLs need to satisfy the condition that their distances and directions to the candidate location are bounded in $[ \ell - \Delta \ell , \ell + \Delta \ell ]$ and $\lvert \theta - \Delta \theta , \theta + \Delta \theta \rvert$ , respectively. The size of the shaded area is $S = \Delta \theta \big ( ( \ell + \Delta \ell ) ^ { 2 } - ( \ell - \Delta \ell ) ^ { 2 } \big ) \big ) = 4 \Delta \theta \ell \Delta \ell .$ . Assuming a location sample density of 2m×2m and $\Delta \ell \leq 2$ meters, the minimal size $S _ { 0 }$ to cover two sample locations should be at least $4 \Delta \ell \mathrm { ~ m ^ { 2 } }$ . Thus, if $\Delta \ell \leq 2$ meters and $\Delta \theta < 1 / \ell ,$ we have $S < S _ { 0 }$ , which means the shaded area covers at most one sample location, i.e., there is only one candidate BL. In practice, the maximal value of the missing delay ∆t is less than 5s (APs not seen for more than 5s would no longer be reported until being detected again next time). Thus, assuming a normal walking speed of 1.2 m/s, the distance offset can be at most 6 meters, resulting in a minimum value of $1 / \ell$ of $\frac { 1 } { 6 } .$ . In other words, even though the distance and direction estimations are erroneous, we could identify a suspicious area and, with high probability, there is only one possible BL in the area, as long as the errors are in certain ranges $( \Delta \ell \leq 2$ meters and $\Delta \theta < \frac { 1 } { 6 } )$ . In case of multiple BLs (which is rare based on our measurements), the one closest to the center of the suspicious area (the shaded area shown in Figure 7) is selected. Phantom fingerprints are then constructed by fingerprints from the candidate location and those from the BLs.

According to specific location sampling density, not all outdated RSS values need to be updated. Only RSSs with distance offsets \` exceeding half of the unit length of sampling grids should be replaced. If \` is less than half of the sampling distance (including being equal to 0 which means static user), fingerprints are merely treated in the traditional way.

# C. Robust Fingerprinting

As we have observed, RSSs of one pair of fingerprints may contain outliers because of impaired measurements due to human body blockage. Since this is the primary cause of biased RSSs in mobile environments, only RSSs over a small portion of APs (that are blocked) may present outliers while most APs would remain consistent. Thus in this section, we propose to apply robust regression method on the inconsistent fingerprints, in the hope of bounding the influence of outlying measurements.

There are a large body of robust regression techniques, including M -estimator, S-estimator, L-estimator, etc [24]. Among them, we choose the most widely adopted Least Median of Squares (LMS) [25] estimator due to its simplicity, effectiveness, and high breakdown point (0.5).

![](images/a2e34fbca895b72fea7744f1417d73caa1d166e906235e9ac161bcf129e50636.jpg)



(a) Office building.

![](images/db31aa848c77034c9d1fbfedff4b5d35916f40c4f53cb2c75fdce8ce3127f9e8.jpg)



(b) Classroom building.   
Figure 8. Experiment buildings.

Given a query fingerprint $\pmb { f } _ { s } = [ f _ { s , i } , 1 \leq i \leq p ]$ and a sample fingerprint $\pmb { f } _ { t } = [ f _ { t , i } , 1 \leq i \leq p ]$ , we adopt a simple linear regression model as follows:

$$
y _ {i} = \theta_ {1} x _ {i} + \theta_ {2} + e _ {i}, i = 1, \dots , p, \tag {5}
$$

where the response variables y are given by $f _ { s } ,$ while $\mathbf { \vec { e } X \tilde { \mathbf { \theta } } }$ planatory variables $\pmb { x } = \pmb { f } _ { t } , \pmb { e } = [ e _ { 1 } , \cdot \cdot \cdot , e _ { p } ]$ indicates the error term which is assumed to be normally distributed with zero mean and an unknown standard deviation σ. As the AP number $p$ is usually small, applying robust regression on insufficient observations does not always produce convincing statistical results. To obtain sufficient data for regression, we propose to compare the query fingerprint against all sample fingerprints corresponding to a candidate location, instead of a single averaged fingerprint. Specifically, for the candidate location $L = L ( \pmb { f } _ { t } )$ with sample fingerprints $\mathcal { F } ^ { L } = \{ f _ { k } ^ { L } , k =$ $1 , \cdots , m \}$ , we simultaneously match $f _ { s }$ to all records in $\mathcal { F } ^ { L }$ . In doing so, we acquire mp observations, which can achieve the scale of hundreds since there are generally at least dozens of sample fingerprints for one location in the fingerprint database, and thus are sufficient for statistical regression like LMS estimator. In this case, the explanatory variables x expanded as becomes $\pmb { x } = [ \pmb { f } _ { 1 } ^ { L } , \cdot \cdot \cdot , \pmb { f } _ { m } ^ { L } ] _ { 1 \times m p } ^ { T }$ $\pmb { y } = [ \pmb { f } _ { s } , \cdot \cdot \cdot , \pmb { f } _ { s } ] _ { 1 \times m p } ^ { T }$ and correspondingly y is . The regression model is

$$
y _ {k, i} = \theta_ {1} x _ {k, i} + \theta_ {2} + e _ {k, i}, \tag {6}
$$

where $i = 1 , \cdots , p , k = 1 , \cdots , m$ , and $x _ { k , i }$ and $y _ { k , i }$ indicate the value of $f _ { i }$ in $\pmb { f } _ { k } ^ { L }$ and $f _ { s } ,$ respectively. Applying LMS to the data [x y] yields $\hat { { \pmb \theta } } = [ \hat { \theta } _ { 1 } , \hat { \theta } _ { 2 } ]$ where the estimates $\widehat { \theta } _ { i }$ denote the regression coefficients. Multiplying x with these ${ \hat { \theta } } _ { i } .$ , we obtain the estimated values of $y _ { i }$ as

$$
\hat {y} _ {k, i} = \hat {\theta} _ {1} x _ {k, i} + \hat {\theta} _ {2}. \tag {7}
$$

The LMS estimator is given by minimizing the median of squares of residuals as follows:

$$
\min _ {\hat {\boldsymbol {\theta}}} \operatorname * {m e d} _ {i, k} (y _ {k, i} - \hat {y} _ {k, i}) ^ {2}. \tag {8}
$$

To determine whether a value $y _ { k , i }$ is an outlier among all elements in y, we compare the residual $r _ { k , i } = y _ { k , i } - \hat { y } _ { k , i }$ i to the scale estimate $\sigma ^ { * }$ defined by [24]. Then each $y _ { k , i }$ is adjusted to $\tilde { y } _ { k , i }$ as follows:

$$
\tilde {y} _ {k, i} = \left\{ \begin{array}{l l} y _ {k, i} & \text { if } | r _ {k, i} / \sigma^ {*} | \leq 2. 5 \\ \hat {y} _ {k, i} & \text { otherwise } \end{array} \right. \tag {9}
$$

The boundary of 2.5 is an empirical value that has been suggested by preliminary experience in the literature [24]. Accordingly, the RSS values of the query fingerprint $f _ { s }$ are regulated as $\begin{array} { r } { \tilde { f } _ { s , i } = \frac { 1 } { m } \sum _ { k } \tilde { y } _ { k , i } } \end{array}$ and the RSDs $\delta _ { s t }$ between $f _ { s }$ and $\pmb { f } _ { t }$ are thus tuned as $\tilde { \delta } _ { s t , i } = | \tilde { f } _ { s , i } - f _ { t , i } |$ .

# D. Localization

Integrating all of the above components in a unified solution, we define a new metric as follows for uniform fingerprint dissimilarity judgment.

$$
h (\boldsymbol {f} _ {s}, \boldsymbol {f} _ {t}) = \left(\sum_ {i = 1} ^ {p _ {s t}} (\rho_ {i} ^ {s t} \cdot \tilde {\delta} _ {s t, i}) ^ {2}\right) ^ {\frac {1}{2}}, \tag {10}
$$

where $p _ { s t } = | { \mathcal { A } } _ { s } \cup { \mathcal { A } } _ { t } |$ | is the total number of distinctive APs in $f _ { s }$ and $\scriptstyle f _ { t } ,$ , and $\rho _ { i } ^ { s t } = \operatorname* { m a x } \{ \rho _ { i } ^ { s } , \rho _ { i } ^ { t } \}$ denotes the discrimination capability of $\mathsf { A P } \ A _ { i }$ for matching $f _ { s }$ and $\pmb { f } _ { t }$ . Note that the RSD $\tilde { \delta } _ { s t , i }$ could also be given by other suitable metrics such as a probability estimation. Realizing that fingerprints from closer locations share more common APs (or equivalently, fingerprints with very few common APs is unlikely to be from adjacent or same locations), the ultimate form of dissimilarity between two fingerprints $f _ { s }$ and $\mathbf { \Delta } f _ { t }$ is expanded as follows:

$$
\phi (\boldsymbol {f} _ {s}, \boldsymbol {f} _ {t}) = h (\boldsymbol {f} _ {s}, \boldsymbol {f} _ {t}) \cdot \frac {p _ {s t}}{q _ {s t}}, \tag {11}
$$

where $q _ { s t } = | \mathcal { A } _ { s } \cap \mathcal { A } _ { t } |$ denotes the number of common APs in $f _ { s }$ and $\pmb { f } _ { t } .$ . With the above dissimilarity metric, the dissimilarity of two fingerprints with fewer common discriminative APs will be amplified. In case of no common APs $( q _ { s t } = 0 )$ , the dissimilarity will go to infinity, which eradicates the mismatch of two completely irrelevant fingerprints.

# IV. EXPERIMENTS AND EVALUATION

# A. Experimental Methodology

We prototype DorFin on Google Nexus S and Nexus 4 phones which both run the mainstream Android OSs. We conduct the experiments in an office building and a classroom building on our campus, as shown in Figure 8a and Figure 8b, respectively. We manually sample areas of interests in both buildings and obtain a total of 83 sample locations in the classroom building and 90 locations in the office building. To construct the fingerprint database, we collect around 60 sample records at each location (which typically takes about 1 minute) by putting the phone on a portable desk. To obtain training data free of human body effects, no human is present around the desk when the mobile phone is collecting data. A high sampling density of 1m×1m is used in site survey for extensive evaluation. Sparser data are then derived from these densely surveyed samples.

![](images/138c8b272fc3f1d8f5d01444561f37e8052edadf63e865424745de74352a666d.jpg)



(a) Accuracy in office building

![](images/a424438e5bd630396c8a0bd743526c08bd54e9c056af06594cd728c2abdf6767.jpg)



(b) Accuracy in classroom building

![](images/a2a26714248d480ff5febb5fa98e67334088405a7a996ff7cab6f108f0324724.jpg)



(c) Accuracy in mobile environments   
Figure 9. Accuracy of DorFin

![](images/8b9604ac67d9334e823bd53412ee7deccc2cf5c241017eaf52f006b25c19dd20.jpg)



Figure 10. Effects of individual modules

![](images/8f1146ca461b75538b1b9facf771feea5c8c3380788ea723087b38897c58b8e4.jpg)



Figure 11. Effect of phantom fingerprints

![](images/d6c512a2dc74b765a6593afa9c04fb85490ae4d2687f8b0f10123e75f935b15d.jpg)



Figure 12. Effect of sample density

We consider both static and mobile cases for testing. For stationary cases, we collect query data by letting users record measurements at each location with their smartphones held in hand. For a mobile user, the smartphone measures wireless signals while the user is walking at a constant speed along a designated path with predefined start and end points. Note that the individual walking speed varies from user to user and from trace to trace. To obtain the ground truth locations of records along the moving trace, we compute user’s walking speed by dividing the path length to the total time, and accordingly interpolate between the start and end points to obtain the location corresponding to each measurement based on their timestamps. In total, we collect static queries from around 200 locations, and gather over 20 mobile traces reported from different pathways, covering major areas of both buildings.

A moving average filter is employed on the raw data to deal with noise. Location error between the ground truth and the estimated location (measured in Euclidean distance) is adopted for evaluation. In particular, we focus on the mean and 95th percentile localization errors. To compare the performance to popular approaches in the literature, we employ a deterministic scheme RADAR [1] and a probabilistic scheme Horus [2], two well-known methods of fingerprint-based localization. We choose RADAR and Horus for the purpose of confirming the performance improvements of DorFin on pure RSS fingerprintbased schemes. To provide fair comparison, identical training and testing data are fed to Horus, RADAR, as well as our proposed approach.

# B. Performance Evaluation

1) Overall performance: Figure 9 illustrates the localization error distributions seen by DorFin, Horus, and RADAR in different buildings and scenarios. DorFin achieves mean accuracy of around 1.5m and 2.6m in office and classroom buildings respectively, consistently and substantially outperforming Horus and RADAR. Besides the promising average accuracy, DorFin significantly reduces the maximum localization error. In both buildings, DorFin bounds the 95th percentile errors to only about 3.7m and 6.7m respectively, while Horus and RADAR both generate location estimation errors larger than 15 meters under identical settings. Integrating all results in both buildings, DorFin provides mean and 95th percentile errors of 2.0m and 5.5m, respectively. For comparison, the mean and 95th percentile errors of Horus are 4.4m and 17.9m while those of RADAR are 4.8m and 18m.

To examine the performance in mobile scenarios, we test the proposed approach on the mobile traces and report the integrated results. Examining across all mobile traces, we observe that the average walking speed is 1.0m/s, while the maximum and minimum speeds are 1.5m/s and 0.6m/s respectively, all within regular range of human walking speed. As illustrated in Figure 9c, despite slight drop in accuracy compared to the static cases, DorFin maintains graceful performance in mobile cases, far superior to Horus and RADAR. Specifically, the average and 95th errors are about 3.0 meters and 8.5 meters, respectively. In comparison with RADAR and Horus, DorFin decreases both errors by nearly 50%. Even though the performance in mobile cases is not as good as static cases, the achieved accuracy remains comparable and promising. In addition, other complementary techniques such as path matching [26] can be integrated to further improve the accuracy for continuous localization.

Impact of sample density. In the following, we further demonstrate that the suprior performance of DorFin is attributed to the proposed approach instead of dense samples. As mentioned above, we sample the areas of interests with a density of 1m×1m, which is relatively high for practical operations. To examine the performance with sparser sample locations, we perform DorFin with training data of different sample densities (sample density is adjusted by sifting parts of the samples according to their locations). As shown in Figure 12, DorFin preserves excellent accuracy even with sample densities of 2m×2m and 3m×3m. Specifically, with density of 2m×2m, the mean and 95th percentile errors are still limited at 2.5m and 7.0m respectively, both better than those of Horus and RADAR with density of 1m×1m.

In conclusion, DorFin achieves remarkable performance in both stationary and mobile cases, with reasonable sample densities. To understand how each module of DorFin contributes to the integral accuracy, we next perform an analysis across different modules.

2) Effect of Individual Modules: To provide a clear analysis, we separately employ each module of DorFin, i.e., the discrimination factor (DF) module, the robust regression (RR) module, the common AP constraints (CA) module, and the phantom fingerprint (PF) module on the most basic nearest neighbor method (denoted as Basic) described in Section II-A and evaluate the individual performance.

Effect of DF. We evaluate the impact of DF by using a set of empirical parameters to calculate the discrimination factor. Specifically, the path loss exponent is set to a typical value of 3 in indoor environments. The sigmoid function parameters a and c accordingly adopts the values of 4 and 4.3, respectively. As shown in Figure 10, DF limits the 95th percentile estimation error by about 40%, while the average error is 1.5m lower than the Basic scheme, which has mean and 95th percentile errors of 5m and 17.5m. By placing more weight on more discriminatory APs and limiting those of the others, DF achieves the improvement by ensuring the similarity between fingerprints of close locations. This feature is also illustrated in Figure 13b, which depicts the confusion matrix of fingerprint dissimilarity after employing the DF module (the confusion matrix of Basic scheme is shown in Figure 13a). In addition, results from two buildings indicate that discrimination factors with uniform parameter settings can generate satisfactory results in different scenarios.

Effect of RR. As shown in Figure 10, by employing RR over the Basic scheme, an average accuracy of 2.2m is achieved, with the corresponding 95th percentile accuracy of only 6m. Evidently, the advantages of RR are the most significant among all modules by reducing the mean and 95th percentile errors by about 56% and 65% compared with the Basic scheme, respectively. Figure 13d further depicts the corresponding dissimilarity matrix. Such results on RR confirm our observation that fingerprint inconsistency counts as a major cause of localization errors of fingerprint-based methods especially for smartphones.

Effect of CA. Figure 10 also demonstrates that the CA module is simple yet surprisingly effective. Incorporating the CA module with Basic scheme, the average and 95th percentile localization errors are reduced by about 50% and 60%, turning into 2.5m and 6.8, respectively. Figure 13c shows the confusion matrix after weighing the fingerprint similarity by the common AP ratio. Dissimilarity of fingerprints from faraway locations is largely enlarged by the common AP ratio, while that of fingerprints from close locations is hardly affected (since close locations share more common APs).

Effect of PF. To examine the effectiveness of phantom fingerprints in dealing with outdated RSS measurements, we compare the performance of the Basic method on mobile data with and without constructing phantom fingerprints. As depicted in Figure 11, the average and 95th percentile errors decrease from 3.9m and 10.4m to 2.4m and 6.9m respectively when the sample fingerprints are appropriately replaced with phantom fingerprints. With these results, it is of interests to examine to what extent the measured RSSs and further the entire fingerprints are outdated. As we observed, over 11% of RSS measurements are outdated in our experiment data. Furthermore, almost every fingerprint undergoes outdated RSSs. In particular, there always exist large outdated distances ranging from 2m to 6m in most fingerprints. The improvements gained by using PF validate quite convincingly our observation that the outdated RSS values can lead to location estimation errors in mobile environments.

Building on these components, DorFin produces promising accuracy levels even in mobile environments that are competitive with that achieved by leveraging physical layer information [14], [17] or introducing extra ranging techniques [12], [27] (both with mean accuracy of about 1m∼3m). Requiring no hardware modification, DorFin can enhance existing WiFi positioning systems.

# V. RELATED WORKS

In the literature of indoor localization, many techniques have been proposed in the past two decades. The state-of-theart generally falls into two categories: fingerprint-based and ranging-based.

Fingerprint-based techniques. A large body of indoor localization approaches adopts fingerprint matching as the basic scheme for location estimation. Researchers have explored diverse signatures including WiFi [2], RFID [3], FM radio [26], acoustic [5], magnetism [28], etc. Among various signatures used, WiFi based scheme has been the most attractive.

![](images/44d4ce0d50c5c1433b58267c4112827b5738b2a870d8658270daac0b32b5b959.jpg)



(a) Basic

![](images/949645a2ab4266f7342318805214d750ab6c0b796797a48b8d67f9b634ee107e.jpg)



(b) DF

![](images/c04d9652eccfce54e5ad593419e75f9407fb79dcaa1dfa2ca3040737cf7ce94a.jpg)



(c) CA

![](images/b47b0c4ff5124e27aa54b8cffc9c3874bf0384dc548eab943a3ea8fa2ae8e7a2.jpg)



(d) RR   
Figure 13. Confusion matrix of similarity between query fingerprints and training fingerprints from 90 locations

Smartphones with various built-in sensors have been leveraged in fingerprint-based localization to reduce or eliminate site survey efforts. Examples include LiFS [9], unloc [11], Zee [13], Walkie-Markie [10], etc. To provide better accuracy, sophisticated probability models and advanced machine learning techniques have been employed [29], [30]. The study [16] validates a broad range of approaches in a realistic environments and reports that median errors of prior work are consistently greater than 5 meters and, counter-intuitively, that simpler algorithms frequently outperform more sophisticated ones. Realizing that large errors always exist due to possibly faraway locations with similar WiFi signatures, authors in [12], [27] attempt to incorporate acoustic ranging in WiFi fingerprinting to limit the large tail errors. Although significant improvements are achieved, these approaches either rely on ranging among a dense crowd of users or require calibrating additional information. To completely bypass the instability of RSS, physical layer information, e.g., Channel State Information (CSI), is introduced and achieves an accuracy of ∼1m [17], but at the cost of ubiquity degradation (since CSI is unavailable on most commodity smartphones). To reduce computational complexity, different criteria for AP’s discriminatory ability such as InfoGain [31] and MaxMean [29] have been proposed to choose a subset of APs. However, they are only used for AP selection, instead of attaching to each AP for fingerprint matching.

Ranging-based techniques. These schemes calculate locations based on geometrical models rather than search for bestfitted signatures from pre-labeled reference database. The prevalent LDPL model, for instance, builds up a semi-statistical function between RSS values and RF propagation distances [15], [32]. These approaches trade measurement efforts for the cost of decreasing localization accuracy. EZ [32] employs a modeling method assuming no knowledge of physical layout or AP locations, and reports median error of 7 meters. Apart from RSS-based ranging, CSI is recently used to obtain for highly accurate distance and angle estimation [14]. Acoustic ranging is also employed for fine-grained indoor localization, such as Centour [27], Guoguo [6], etc.

Different from previous works that introduce additional information or extra signal sources for high accuracy, we identify the root causes of location errors in WiFi fingerprintbased localization for mobile devices, which have been largely overlooked in the literature. In addition, the proposed scheme achieves high accuracy with merely the prevalent RSS, thus is more amenable for practical applications.

# VI. CONCLUSIONS

While WiFi fingerprint-based localization acts as the dominant scheme in indoor localization, the accuracy challenge remains a primary concern. In this paper, we identify several crucial causes of localization errors in fingerprint-based schemes. These observations then lead us to the design of a new WiFi fingerprinting scheme which successfully reduces the mean and 95th percentile location errors to 2 meters and 5.5 meters, without degrading ubiquity nor increasing the costs. Our approach marks a significant progress in RSS fingerprintbased indoor localization, especially for smartphones, and sheds lights on practical deployment in the real world.

# REFERENCES

[1] P. Bahl and V. N. Padmanabhan, “RADAR: an in-building RF-based user location and tracking system,” in Proceedings of IEEE INFOCOM, 2000, pp. 775–784.   
[2] M. Youssef and A. Agrawala, “The horus WLAN location determination system,” in Proceedings of ACM MobiSys, 2005, pp. 205–218.   
[3] L. M. Ni, Y. Liu, Y. C. Lau, and A. P. Patil, “LANDMARC: indoor location sensing using active RFID,” Wireless Networks, vol. 10, no. 6, pp. 701–710, 2004.   
[4] J. Wang and D. Katabi, “Dude, where’s my card? RFID positioning that works with multipath and non-line of sight,” in Proceedings of ACM SIGCOMM, 2013.   
[5] S. P. Tarzia, P. A. Dinda, R. P. Dick, and G. Memik, “Indoor localization without infrastructure using the acoustic background spectrum,” in Proceedings of ACM MobiSys, 2011, pp. 155–168.   
[6] K. Liu, X. Liu, and X. Li, “Guoguo: Enabling fine-grained indoor localization via smartphone,” in Proceedings of ACM MobiSys, 2013.   
[7] N. B. Priyantha, A. Chakraborty, and H. Balakrishnan, “The cricket location-support system,” in Proceedings of ACM MobiCom, 2000, pp. 32–43.   
[8] P. Lazik and A. Rowe, “Indoor pseudo-ranging of mobile devices using ultrasonic chirps,” in Proceedings of ACM SenSys, 2012, pp. 99–112.   
[9] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: wireless indoor localization with little human intervention,” in Proceedings of ACM MobiCom, 2012, pp. 269–280.   
[10] G. Shen, Z. Chen, P. Zhang, T. Moscibroda, and Y. Zhang, “Walkiemarkie: indoor pathway mapping made easy,” in Proceedings of USENIX NSDI, 2013, pp. 85–98.   
[11] H. Wang, S. Sen, A. Elgohary, M. Farid, M. Youssef, and R. R. Choudhury, “No need to war-drive: unsupervised indoor localization,” in Proceedings of ACM MobiSys, 2012, pp. 197–210.   
[12] H. Liu, Y. Gan, J. Yang, S. Sidhom, Y. Wang, Y. Chen, and F. Ye, “Push the limit of WiFi based localization for smartphones,” in Proceedings of ACM MobiCom, 2012, pp. 305–316.

[13] A. Rai, K. K. Chintalapudi, V. N. Padmanabhan, and R. Sen, “Zee: zero-effort crowdsourcing for indoor localization,” in Proceedings of ACM MobiCom, 2012, pp. 293–304.   
[14] S. Sen, J. Lee, K.-H. Kim, and C. Paul, “Avoiding multipath to revive inbuilding wifi localization,” in Proceedings of ACM MobiSys, 2013.   
[15] H. Lim, L. C. Kung, J. C. Hou, and H. Luo, “Zero-configuration indoor localization over IEEE 802.11 wireless infrastructure,” Wireless Networks, vol. 16, no. 2, pp. 405–420, 2010.   
[16] D. Turner, S. Savage, and A. C. Snoeren, “On the empirical performance of self-calibrating wifi location systems,” in Proceedings of IEEE Conference on Local Computer Networks (LCN), 2011, pp. 76–84.   
[17] S. Sen, B. Radunovic, R. R. Choudhury, and T. Minka, “You are facing the mona lisa: spot localization using PHY layer information,” in Proceedings of ACM MobiSys, 2012, pp. 183–196.   
[18] T. B. Welch, R. L. Musselman, B. A. Emessiene, P. D. Gift, D. K. Choudhury, D. N. Cassadine, and S. M. Yano, “The effects of the human body on uwb signal propagation in an indoor environment,” Selected Areas in Communications, IEEE Journal on, vol. 20, no. 9, pp. 1778– 1782, 2002.   
[19] Z. Zhang, X. Zhou, W. Zhang, Y. Zhang, G. Wang, B. Y. Zhao, and H. Zheng, “I am the antenna: accurate outdoor AP location using smartphones,” in Proceedings of ACM MobiCom, 2011, pp. 109–120.   
[20] “IEEE 802.11, part11: Wireless LAN medium access control (MAC) and physical layer (PHY) specifications,” 2012.   
[21] T. S. Rappaport et al., Wireless communications: principles and practice. Prentice Hall PTR New Jersey, 1996, vol. 2.   
[22] I. Constandache, R. R. Choudhury, and I. Rhee, “Towards mobile phone localization without war-driving,” in Proceedings of IEEE INFOCOM, 2010, pp. 1–9.

[23] C. Wu, Z. Yang, Y. Zhao, and Y. Liu, “Footprints elicit the truth: Improving global positioning accuracy via local mobility,” in Proceedings of IEEE INFOCOM, 2013.   
[24] P. J. Rousseeuw and A. M. Leroy, Robust regression and outlier detection. Wiley, 2005.   
[25] P. J. Rousseeuw, “Least median of squares regression,” Journal of the American statistical association, vol. 79, no. 388, pp. 871–880, 1984.   
[26] S. Yoon, K. Lee, and I. Rhee, “FM-based indoor localization via automatic fingerprint DB construction and matching,” in Proceedings of ACM MobiSys, 2013, pp. 207–220.   
[27] R. Nandakumar, K. K. Chintalapudi, and V. N. Padmanabhan, “Centaur: locating devices in an office environment,” in Proceedings of ACM MobiCom, 2012, pp. 281–292.   
[28] J. Chung, M. Donahoe, C. Schmandt, I.-J. Kim, P. Razavai, and M. Wiseman, “Indoor location sensing using geo-magnetism,” in Proceedings of the ACM MobiSys, 2011, pp. 141–154.   
[29] M. A. Youssef, A. Agrawala, and A. Udaya Shankar, “WLAN location determination via clustering and probability distributions,” in Proceedings of IEEE PerCom, 2003, pp. 143–150.   
[30] M. Youssef and A. Agrawala, “Handling samples correlation in the horus system,” in Proceedings of IEEE INFOCOM, vol. 2, 2004, pp. 1023– 1031.   
[31] Y. Chen, Q. Yang, J. Yin, and X. Chai, “Power-efficient accesspoint selection for indoor location estimation,” Knowledge and Data Engineering, IEEE Transactions on, vol. 18, no. 7, pp. 877–888, 2006.   
[32] K. Chintalapudi, A. Padmanabha Iyer, and V. N. Padmanabhan, “Indoor localization without the pain,” in Proceedings of ACM MobiCom, 2010, pp. 173–184.