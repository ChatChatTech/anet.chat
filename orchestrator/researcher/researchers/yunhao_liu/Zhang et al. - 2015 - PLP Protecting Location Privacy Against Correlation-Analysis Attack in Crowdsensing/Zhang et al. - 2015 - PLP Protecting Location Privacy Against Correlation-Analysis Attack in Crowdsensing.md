# PLP: Protecting Location Privacy against Correlation-Analysis Attack in Crowdsensing

Shanfeng Zhang1,2, Qiang Ma2, Tong Zhu2, Kebin Liu2, Lan Zhang2, Wenbo He3, Yunhao Liu2

1 Department of Computer Science and Engineering, Hong Kong University of Science and Technology

2 School of Software and TNList, Tsinghua University, Beijing, China

3 School of Computer Science, McGill University, Canada

{shanfeng, maq, tong, kebin, lan, wenbo, yunhao}@greenorbs.com

Abstract—Crowdsensing applications require individuals to share local and personal sensing data with others to produce valuable knowledge and services. Meanwhile, it has raised concerns especially for location privacy. Users may wish to prevent privacy leak and publish as many non-sensitive contexts as possible. Simply suppressing sensitive contexts is vulnerable to the adversaries exploiting spatio-temporal correlations in users’ behavior. In this work, we present PLP, a crowdsensing scheme which preserves privacy while maximizes the amount of data collection by filtering a user’s context stream. PLP leverages a conditional random field to model the spatio-temporal correlations among the contexts, and proposes a speed-up algorithm to learn the weaknesses in the correlations. Even if the adversaries are strong enough to know the filtering system and the weaknesses, PLP can still provably preserves privacy, with little computational cost for online operations. PLP is evaluated and validated over two real-world smartphone context traces of 34 users. The experimental results show that PLP efficiently protects privacy without sacrificing much utility.

# I. INTRODUCTION

In recent years, the phenomenal growth of various sensors on smartphones demonstrates that crowdsensing has high payoff potential to obtain fine-grained measurements, compute community statistics, and construct global view of measurements. Crowdsensing can increase the scale and scope of measurements in a way that may otherwise not be supported. Consequently, a wide range of applications such as public health [1], public safety [2], and traffic monitoring [3, 4], have been developed. However, in crowdsensing applications, a user may not want to share the sensing data which may reveal his/her private information such as locations. Anonymous users can still be re-identified with the uploaded data [5–7]. With the privacy concerns, users may hesitate to participate in the sensing task. In this case, it raises difficulties for the server to collect high quality data. Hence, there exists a tradeoff between the privacy of individual data and the utility gained by mining the data.

In this paper, we investigate the techniques to enhance location privacy in crowdsensing, and explain our techniques in a specific scenario, where we build a Received Signal Strength (RSS) map in an indoor area using the data collected from mobile phone users. These users report their locations and the measured RSS values to the server continuously. This process is also called site survey for indoor localization [8, 9]. In this scenario, a user can define some locations as sensitive. For example, Alice does not want others to know that she is in Bob’s office. Our objective is to prevent an adversary from inferring a user’s sensitive locations based on the reported data, meanwhile the server is able to generate an accurate RSS map in the indoor area with fine granularity.

![](images/8bf3ff3994b752211f4a7100791b50d3a3d1015db392699b2e79b1af6b4f55aa.jpg)



(a) HMM can model: given the current position C of the user, the next position will be one of {B, D, E, F }.

![](images/597e7ffab79b972a71f5fbcda2978ce901566225c25bca9784a4026f877e07b6.jpg)



(b) CRF can model: given A B ! C , the next position will probably be F , otherwise the shorter path A ! D ! E is preferred.   
Fig. 1. HMM cannot perfectly describe the spatio-temporal correlations.

The main challenge to address the trade-off between privacy and utility in crowdsensing comes from: 1) temporal correlations among the locations reported in contiguous time slots by an individual user; 2) spatial correlations among locations in a real map topology; 3) data correlations among the RSS values collected in nearby locations (e.g. similar and continues RSS values in a corridor). These correlations can be employed by an adversary to infer location information of individual users.

A large body of existing approaches [10, 11] aim to protect location privacy when users publish location streams, but little of them are effective against strong adversaries knowing spatio-temporal correlations. The authors in [12] show that an attacker may correlate locations from multiple timestamps to accurately pinpoint the user’s sensitive positions. They hide the temporal correlations by postponing some of the reports. Their system, however, is vulnerable to attacks with spatial correlations (e.g., a shorter path is usually preferred). The authors in [13] model temporal correlations with Hidden Markov Model (HMM), then evaluate the sensitivity of locations based on the correlations with private locations, therefore, preserve privacy by suppressing sensitive locations with high probability.

However, HMM has severe limitations in representing human activities [9]. First of all, HMM is incapable of capturing long-range or transitive dependencies of the observations due to its strict conditional independence assumption. For instance, in our scenario, the RSS values at two contiguous locations have data correlation: the values are similar when they are recorded in a corridor without obstruction, different when they are recorded around a corner. Secondly, spatial correlations can be considered to infer the sensitive information. Fig. 1 shows an example why HMM cannot perfectly describe the spatiotemporal correlations. Let us assume that F is a sensitive location. Given a current position C of the user (shown in Fig. 1(a)), HMM can infer that B, D, E and $F$ may be the next position. Given a path $A  B  C$ (shown in Fig. 1(b)), the next position will probably be $F ,$ otherwise the shorter path $A  D  E$ is preferred. Such spatio-temporal correlations between locations cannot be flexibly modeled by a HMM.

Based on these observations, we realize that the adversaries may have more knowledge than temporal correlations modeled by a HMM. For the users, the suppression strategy must be designed on a model, which can flexibly and accurately describes the spatio-temporal correlations and data correlations.

In this paper, we propose PLP, which models the potential correlations in a Conditional Random Field (CRF), and preserves privacy by filtering a user’s context stream. PLP does not assume conditional independence between the reported data, and incorporates long-range dependencies among locations and reported sensing data. PLP suppresses sensing data at all sensitive locations and reports data with a certain probability at insensitive locations. The suppression probability depends on the spatio-temporal and data correlations. By learning the CRF model, we learn potential correlations and find a proper suppression probability to protect the the location privacy. We design a novel estimation algorithm to speed up learning the model, and prove monotonicity property of suppression strategies, which helps to search the optimal strategy that maximizes utility while preserves predefined privacy requirements. To sum up, the key advantages of PLP are:

1. Effectiveness. PLP can preserve privacy even if the adversary is strong enough to know our suppression strategies and the correlations among location data. With PLP, we can not only model the various known correlations, but also have the potential to model the correlations that may be discovered in the future.   
2. Efficiency. PLP incurs little computational cost for online operation. With a novel speed-up estimation algorithm and searching algorithm, the offline training process is done in 40 minutes, which is short enough to be finished when a user is charging his/her phone.   
3. Data utilization. Unlike perturbation based approaches, PLP reports accurate crowdsensing data, and aims to maximize the number of collect data while protects privacy.

We evaluate the performance of PLP with two real-world data sets. The experimental results show that PLP efficiently defends against strong adversaries without sacrificing much utility.

The rest of the paper is organized as follows. In Section II, we formally define our problem, and give necessary background on CRF, the attack model and the metrics. Details about modeling the CRF, novel learning algorithm and optimal algorithm to find the best suppression strategy are presented in Section III. Evaluation results are shown in Section IV. We present related work in Section V, and Section VI concludes this work.

TABLE I SUMMARY OF SYMBOLS 

<table><tr><td> $\mathcal{L}$ </td><td>set of all locations of a user</td></tr><tr><td> $d_{j}$ </td><td>a sensing report</td></tr><tr><td> $l_{j}$ </td><td>an entry in  $\mathcal{L}$ </td></tr><tr><td> $\vec{S}$ </td><td>sensitive locations defined by a user</td></tr><tr><td> $\vec{D}$ </td><td>a sequence of sensing data</td></tr><tr><td> $\vec{O}$ </td><td>a sequence of reported data</td></tr><tr><td> $\vec{L}$ </td><td>a sequence of locations</td></tr><tr><td> $\mathcal{P}$ </td><td>a suppression strategy</td></tr><tr><td> $f_{k}(\vec{L})$ </td><td>a feature function modeling temporal correlations</td></tr><tr><td> $h_{k}(\vec{L},\vec{O})$ </td><td>a feature function modeling spatial correlations</td></tr><tr><td> $r_{k}(\vec{L},\vec{O})$ </td><td>a feature function modeling data correlations</td></tr><tr><td> $g_{k}(L_{t},O_{t})$ </td><td>a feature function modeling suppression strategy</td></tr></table>

# II. PRELIMINARIES

In this section, we introduce our privacy preserving crowdsensing system. We also give a brief introduction of CRF, present the attack model and the metrics to measure privacy and utility.

# A. Privacy Preserving Crowdsensing System

There are three major players in our paper: a crowdsensing server, users, and adversaries. We consider the site survey application scenario in [9]: the crowdsensing server aims to build a RSS fingerprint database by gathering information from a large group of user; the users upload location information in a large building by our privacy preserving crowdsensing system PLP. Each entry in the database includes a RSS fingerprint and its corresponding location.

We use $\mathcal { L }$ to denote the set of locations $l _ { j }$ that a user may go to, $l _ { j }$ and $d _ { j }$ to denote a location and a sensing report. The sensing data $d _ { j }$ includes information about RSS fingerprint. The user need to define a profile of private positions $S =$ $\{ s _ { 1 } , s _ { 2 } , \cdots , s _ { S } \}$ , where $s _ { j } \in { \mathcal { L } }$ . Driven by benefits, the user uploads site survey data in ${ \mathcal { L } } - S ,$ and meanwhile needs to protect private locations defined in S.

Suppose a user reports a data sequence $\begin{array} { r l } { \vec { D } } & { { } = } \end{array}$ $\{ D _ { 1 } , \bar { D } _ { 2 } , \cdot \cdot \cdot , D _ { T } \}$ at a fixed rate, positions of these data are denoted as $\vec { L } = \{ L _ { 1 } , L _ { 2 } , \cdots , L _ { T } \}$ . Please note that each $D _ { t }$ includes the information of $L _ { t } .$ . To preserve privacy and maximize utility at the same time, PLP suppresses each data $D _ { j }$ with a certain probability. We use $\vec { O } = \{ O _ { 1 } , O _ { 2 } , \cdots , O _ { T } \}$ to denote the reported data after filtering, where Ot = empty if privacy-related data $D _ { t }$ is suppressed; otherwise $O _ { t } = D _ { t }$ . The crowdsensing server uses the precise location information $O _ { t } = D _ { t }$ to construct the fingerprint database.

# B. CRFs

Conditional Random Fields (CRFs) [14] are undirected graphs that encode a conditional probability distribution. Consider a CRF with $\vec { O } = \{ O _ { 1 } , O _ { 2 } , \cdot \cdot \cdot , O _ { n } \}$ as observed states, and $\vec { L } = \{ L _ { 1 } , L _ { 2 } , \cdots , \bar { L } _ { n } \}$ as hidden states. A CRF models the conditional probability $P r ( \vec { L } | \vec { O } )$ as:

$$
P r [ \vec {L} | \vec {O} ] = \frac {1}{Z (\vec {O})} \prod_ {c \in \mathcal {C}} \Phi (\overrightarrow {L _ {c}}, \overrightarrow {O _ {c}}), \tag {1}
$$

where $Z ( \vec { O } )$ is the normalizing function:

$$
Z (\vec {O}) = \sum_ {\vec {L}} \prod_ {c \in \mathcal {C}} \Phi (\overrightarrow {L _ {c}}, \overrightarrow {O _ {c}}), \tag {2}
$$

$\mathcal { C }$ is the set of cliques in the graph representation of the CRF model,   is a factor function defined on the cliques to model the correlations among the nodes in a clique, and is usually written in the form of the factorization of a set of feature functions $f _ { k }$ :

$$
\Phi (\overrightarrow {L _ {c}}, \overrightarrow {O _ {c}}) = e x p \left(\sum_ {k} \lambda_ {k} f _ {k} (\overrightarrow {L _ {c}}, \overrightarrow {O _ {c}})\right), \tag {3}
$$

where $\lambda _ { k }$ is the feature parameter of feature function $f _ { k } .$ .

CRF can flexibly and accurately describe the spatiotemporal correlations. Both HMMs and CRFs can be used to find the hidden sequence (e.g. L\~ ) from the observation sequence (e.g. O\~ ). For simplicity to model the joint probability $P r ( \vec { L } , \vec { O } )$ , HMM assumes that all the observed states are conditionally independent given the hidden states, which is not true in our scenario. For example, if a sensitive place is suppressed, nearby places will be suppressed with high probability to protect the sensitive one. By modeling the conditional probability $P r ( \vec { L } | \vec { O } )$ , CRFs can model long-range dependences between the hidden states and observations without making the inference problem intractable.

# C. Attack Model

We consider strong adversaries, who can obtain information of the suppression system, spatio-temporal knowledge and all the sensing data (i.e. $\vec { \cal O } \ = \ \{ { \cal O } _ { 1 } , { \cal O } _ { 2 } , \cdot \cdot \cdot , { \cal O } _ { T } \} )$ ) of a user. With a conditional random field to model the spatio-temporal correlations, the adversary tries to reveal whether the user is at a private location at time $t _ { \underline { { \cdot } } }$ The posterior belief of a location sequence $\vec { L }$ based on O\~ is computed by Equ. 1. We will show in Section IV that such a strong adversary can disclose sensitive location information with reports from existing privacy preserving systems such as MaskSensitive and MaskIt [13].

# D. Definition of Privacy and Utility

We use metrics in [13] to evaluate the privacy degree and utility of a report $\vec { O } = \{ O _ { 1 } , O _ { 2 } , \cdot \cdot \cdot , O _ { T } \}$ .

Algorithm 1 Suppression Strategy of PLP   
Input: Site survey data $\vec{D}$ , Suppression strategy P
Output: Report data $\vec{O}$

1: for t = 0 to $T$ do   
2: Get location id j, s.t. $l _ { j } = D _ { t }$ .location   
3: Get suppression probability $p _ { j }$   
4: Set Ot = empty with probability $p _ { j }$   
$O _ { t } = D _ { t }$ with probability $1 - p _ { j }$

![](images/24c674d6c683abcb6557598dfc0f6584ae043f400c471ae82efecfac72f5f744.jpg)



Temporal Correlations   
(a)

![](images/ab69becb197f38ccaae9aa067a012cf862bbc2d96086669d82fe151ba741376a.jpg)



Spatial Correlations

![](images/954e76b7754be43ee974db2cf09b3169118d1bc720d4fc6658ef0f287c6142c6.jpg)



Data Correlations

(d)   
![](images/4e806a71075e7f358a60f747fd43f776f0611a8e9619e2c1b0f3b8932de94317.jpg)



Suppression Strategy

![](images/3a9bfe014f5b305dfcb0c81933533ed0b765ba73baeed2b97f95b42d7d9cd94a.jpg)



Fig. 2. Factor graphs of correlations and suppression strategy.

1) Privacy Metric: Consider a user reporting a sequence of site survey data ${ \vec { O } } .$ The private locations are S. We say the reporting data preserves privacy, if it doesn’t change adversary’s guess on the user’s probability of being at private locations by  . Informally, $\vec { O }$ preserves     privacy if for any time t, and for any private location $s _ { j } \in S _ { \cdot }$ , the posterior belief about the user being at $s _ { j }$ at t is required to be close to the prior belief:

$$
P r [ L _ {t} = s _ {j} | \vec {O} ] - P r [ L _ {t} = s _ {j} ] \leq \delta , \tag {4}
$$

where   is a privacy parameter to model the difficulty in guessing privacies. The smaller   is, the more difficult for an adversary to reveal privacy.

2) Utility Metric: Consider a user reports ${ \vec { O } } .$ On the server side, a non-empty report $O _ { i }$ can be used to update the RSS fingerprint database. The utility of $\vec { O }$ is defined as a ratio of non-empty items:

$$
u t i l i t y (\vec {O}) = \left| \{t | O _ {t} \neq e m p t y \} \right| / T, \tag {5}
$$

where T is the number of items in ${ \vec { O } } .$

# III. ENHANCING PRIVACY WITH CRF

This section details the PLP system based on a CRF. We first give an overview of the model, followed by definition of proper feature functions. We then propose a novel estimation algorithm to speed up learning feature weights, and seek to find the optimal suppression strategy based on monotonicity properties.

# A. Overview

On the user side, we formulate the reporting problem as a decision problem. We assign a suppression probability $P _ { t }$ for each sensing data $D _ { t } .$ . PLP outputs empty with a probability $P _ { t }$ and output $D _ { t }$ with a probability $1 - P _ { t }$ . Algo. 1 describes details about this process. We denote a suppression strategy by a set of suppression probabilities $\mathcal { P } = \{ p _ { 1 } , p _ { 2 } , \cdot \cdot \cdot \} . ~ p _ { j }$ is the suppression probability when the user is at $l _ { j } .$ . We aim to find a suppression strategy $\mathcal { P }$ that preserves privacy and maximizes utility at the same time.

We model the potential correlations and suppression strategy in the CRF model. With properly assigned suppression strategies, PLP can achieve $\delta - p r i v a c y$ .

Correlations. Given a report ${ \vec { O } } ,$ the adversary tries to infer locations $\vec { L }$ with correlations modeled by a CRF. Based on Equ. 1, the probability of the adversary to guess the location sequence $\vec { L }$ given $\vec { O }$ is:

$$
\begin{array}{l} P r [ \vec {L} | \vec {O} ] = \frac {1}{Z (\vec {O})} e x p \left\{\sum_ {t = 1} ^ {T} \left(\sum_ {k = 1} ^ {K _ {1}} \lambda_ {k} f _ {k} (\vec {L}) \right. \right. \\ \left. \left. + \sum_ {k = 1} ^ {K _ {2}} \beta_ {k} h _ {k} (\vec {L}, \vec {O}) + \sum_ {k = 1} ^ {K _ {3}} \gamma_ {k} r _ {k} (\vec {L}, \vec {O})\right) \right\}, \\ \end{array}
$$

where $\vec { L } \subset \mathcal { L }$ is a location sequence; $f _ { k } ( \vec { L } )$ models the potential temporal correlations among any set of locations in $\mathcal { L }$ (Fig. 2(a)), for example, the probability of next position to be F given previous path is $A  B  C$ in Fig. 1 b; $h _ { k } ( \vec { L } , \vec { O } )$ defines the spatial correlations among a set of coherent locations and corresponding reports (Fig. 2(b)), for example, data in the locations near a privacy locations may probably be suppressed; $r _ { k } ( \vec { L } , \vec { O } )$ models the feature dependencies (Fig. 2(c)); $K _ { 1 }$ , $K _ { 2 } , \ K _ { 3 }$ is the number of corresponding feature functions. In our application, data dependencies are the correlations among RSS data. We will discuss the proper definition of these three feature functions and the algorithm to train the feature parameters $( \left\{ \lambda _ { k } , \beta _ { k } , \gamma _ { k } \right\} )$ in next Section III-C. Note that we can further define more feature functions to model other potential correlations of crowdsensing data and location information, such that we can protect against attacks based on these potential correlations.

Suppression strategy. We then model the suppression strategy  in the CRF by defining a set of feature functions $g _ { k _ { 1 } } ( L _ { t } , O _ { t } )$ and $g _ { k _ { 2 } } ( L _ { t } , O _ { t } )$ :

$$
g _ {k _ {1}} (L _ {t}, O _ {t}) = \delta (L _ {t} = l _ {j}, O _ {t} = e), \tag {7}
$$

$$
g _ {k _ {2}} (L _ {t}, O _ {t}) = \delta (L _ {t} = l _ {j}, O _ {t} = D _ {t}), \tag {8}
$$

where $\delta ( w )$ is an indicator function which equals 1 if the condition w holds and 0 otherwise. Feature parameters are the log likelihood based on the suppression strategy P:

$$
\theta_ {k _ {1}} = \log p _ {j}, \quad \theta_ {k _ {2}} = \log (1 - p _ {j}). \tag {9}
$$

We use a set of feature functions $\left\{ g _ { k } \right\}$ to denote $\{ g _ { k _ { 1 } } \}$ and $\left\{ g _ { k _ { 2 } } \right\}$ . The CRF model can be written as:

$$
\begin{array}{l} P r [ \vec {L} | \vec {O} ] = \frac {1}{Z (\vec {O})} e x p \left\{\sum_ {t = 1} ^ {T} \left(\sum_ {k = 1} ^ {K _ {1}} \lambda_ {k} f _ {k} (\vec {L}) + \sum_ {k = 1} ^ {K _ {2}} \beta_ {k} h _ {k} (\vec {L}, \vec {O}) \right. \right. \\ \left. \left. + \sum_ {k = 1} ^ {K _ {3}} \gamma_ {k} r _ {k} (\vec {L}, \vec {O}) + \sum_ {k = 1} ^ {K _ {4}} \theta_ {k} g _ {k} \left(L _ {t}, O _ {t}\right)\right) \right\}, \tag {10} \\ \end{array}
$$

![](images/7ba59099b58a002192353f8fafac18e03c24d960c2e73f46a53bf29568899d79.jpg)



Fig. 3. Given S as a sensitive location, A is highly spatial correlated with S because paths passing B will probably pass through S, while C is less correlated because paths passing C can also go to D.

where $Z ( \vec { O } )$ is normalizing function as in Equ. 2:

$$
\begin{array}{l} Z (\vec {O}) = \sum_ {L} e x p \left\{\sum_ {t = 1} ^ {T} \left(\sum_ {k = 1} ^ {K _ {1}} \lambda_ {k} f _ {k} (\vec {L}) + \sum_ {k = 1} ^ {K _ {2}} \beta_ {k} h _ {k} (\vec {L}, \vec {O}) \right. \right. \\ \left. \left. + \sum_ {k = 1} ^ {K _ {3}} \gamma_ {k} r _ {k} (\vec {L}, \vec {O}) + \sum_ {k = 1} ^ {K _ {4}} \theta_ {k} g _ {k} \left(L _ {t}, O _ {t}\right)\right) \right\}. \tag {11} \\ \end{array}
$$

We now show how to check whether a suppression strategy $\mathcal { P }$ is privacy-preserving. Note that a different suppression strategy $\mathcal { P }$ can influence $P r [ \vec { L } | \vec { O } ]$ , which is the probability of the adversary to disclose $\vec { L }$ given ${ \vec { O } } .$ The posterior probability in Equ. 4 can now be computed by:

$$
P r [ L _ {t} = s _ {j} | \vec {O} ] = \sum_ {\vec {L}: L _ {t} = s _ {j}} P r [ \vec {L} | \vec {O} ]. \tag {12}
$$

We say a suppression strategy $\mathcal { P }$ meets    privacy, if for any possible reported data $\vec { O } , \vec { O }$ preserves $\delta - p r$ ivacy. Algorithm 2 describes details to check a suppression strategy.

utility of a suppression strategy is defined as the expectation of report data:

$$
\begin{array}{l} u t i l i t y (\mathcal {P}) = \sum_ {\vec {\mathcal {O}}} P r [ \vec {\mathcal {O}} ] \times u t i l i t y (\vec {\mathcal {O}}) \\ = \sum_ {\vec {O}} P r [ \vec {O} ] \left| \{t \mid O _ {t} \neq e m p t y \} \right| / T. \tag {13} \\ \end{array}
$$

# Algorithm 2 CheckPrivacy

Input: Suppression strategy ${ \mathcal { P } } ,$ Privacy profile S, Floorplan topology $\mathcal { G }$

Output: Whether $\mathcal { P }$ satisfies     P rivacy

1: Initialize $\mathcal { G }$ to find possible path set: $P a t h = \{ \vec { L } \}$ and output sequence set $\bar { \mathcal { O } } = \{ \vec { O } \}$

2: for $s _ { j } \in S$ do

3: for $t = 0$ to $T$ do

4: caculate $P r [ L _ { t } = s _ { j } ]$

5: for $\vec { O } \in \mathcal { O }$ do

6: for $\vec { L } \in P a t h$ and $\vec { L }$ is possible to output $\vec { O }$ do

7: if ${ \cal L } _ { t } = = s _ { j }$ then

8: $P r [ L _ { t } = { \bf \ddot { \it s } } _ { j } | \vec { O } ] + = P r [ \vec { L } | \vec { O } ]$

9: if $P r [ L _ { t } = s _ { j } | \vec { O } ] - P r [ L _ { t } = s _ { j } ] > \delta$ then

10: return $^ { * } \delta - P r$ rivacy not satisfied”

11: return    P rivacy satisfied

We will show algorithms to find an optimal suppression approach P that preserves   privacy and maximizes $u t i l i t y ( \mathcal { P } )$ 号 in Sec. III-D.

# B. CRF Model for PLP

In this part, we will introduce details of the feature functions used to model the spatio-temporal correlations and data correlations.

Temporal Correlation Analysis. We use $f _ { k } ( \vec { L } )$ to model the temporal transitions between locations. For instance, in Fig. 1, the transition to $L _ { t } = F$ given $L _ { t - 1 } = C , L _ { t - 2 } = B$ and $L _ { t - 3 } = A$ is modeled by a feature function $f _ { k } { \mathrm { : } }$ :

$$
f _ {k} (\vec {L}) = \delta (L _ {t - 3} = A, L _ {t - 2} = B, L _ {t - 1} = C, L _ {t} = F). \tag {14}
$$

The feature parameter $\lambda _ { k }$ is the transition weight, representing the frequency a transition occur $( { \bf e . g . } \ \lambda _ { k } \ = \ l o g P r [ L _ { t } \ =$ $F | L _ { t - 3 } = A , L _ { t - 2 } = B , L _ { t - 1 } = C ] )$ .

Similarly, we define a feature function $f _ { k } ( L _ { 1 } , L _ { 2 } , \cdots , L _ { t } )$ to model the dependency of any t locations: $( l _ { 1 } , l _ { 2 } , \cdots , l _ { t } )$ . For simplicity, we consider temporal transition dependencies among at most three locations in this work, even though we can add temporal correlations among locations of any number. That is, for any three locations: $l _ { i } , l _ { j } , l _ { k } .$ , the transition from $l _ { i } , l _ { j }$ to $l _ { k }$ can be modeled by a feature function:

$$
\begin{array}{l} \begin{array}{l} f _ {k} \left(L _ {t - 2}, L _ {t - 1}, L _ {t}\right) \\ f (L _ {t - 2}, L _ {t - 1}, L _ {t}) \end{array} \tag {15} \\ = \delta (L _ {t - 2} = l _ {i}, L _ {t - 1} = l _ {j}, L _ {t} = l _ {k}). \\ \end{array}
$$

We will show how to train the feature in the next subsection.

Spatial Correlation Analysis. We use $h _ { k } ( \vec { L } , \vec { O } )$ to model spatial correlations. For instance, in Fig. 3, B is highly correlated with S. If the user walks from A to B, he will probably go to S. So B should also be suppressed to protect S. On the other hand, if the user walks from A to C, he can choose to go to S or D. So we don’t need to suppress C with high probability. In conclusion, if we know the user goes to B, we will also know that the user goes to S. For this example, we define a spatial feature function:

$$
\begin{array}{l} h _ {k} (L _ {t}, L _ {t - 1}, O _ {t}, O _ {t - 1}) \\ \begin{array}{l} \text {   } \\ = \delta (L _ {t} = S, L _ {t - 1} = C, O _ {t} = e, O _ {t - 1} = e), \end{array} \tag {16} \\ \end{array}
$$

In general cases, we need to model correlation between a set of private locations $S ^ { \prime } \subset S$ and any location set $L \subset { \mathcal { L } } .$ . In other words, if we know $L ,$ the user may probably go to $S ^ { \prime }$ . For simplicity, we consider correlations between one sensitive location and one correlated location in our application. We define a spatial feature function as:

$$
h _ {k} (L _ {t}, L _ {t - t ^ {\prime}}, O _ {t}, O _ {t - t ^ {\prime}})
$$

$$
\begin{array}{l} t _ {k} \left(L _ {t}, L _ {t - t ^ {\prime}}, O _ {t}, O _ {t - t ^ {\prime}}\right) \\ = \delta \left(L _ {t} = s _ {j}, L _ {t - t ^ {\prime}} = l _ {j}, O _ {t} = e, O _ {t - t ^ {\prime}} = e\right) \end{array} \tag {17}
$$

The feature parameter $\beta _ { k }$ is trained to model the degree of correlations. For example, in Fig. 3, correlation between S and B has a larger feature parameter, while correlation between S and C has a smaller feature parameter. We will show detailed training process latter.

Data Correlation Analysis. The term $r _ { k } ( \vec { L } , \vec { O } )$ is used to model data correlations, namely RSS correlations in our

![](images/38e7808efb9f2e256a4f78a125e782366cd06e1e72d98fc4cefb1c6312c1061a.jpg)



Fig. 4. If the user walks a direct path to an AP, the RSS values will gradually increase. On the other hand, if the user makes a turning around the corner, the RSS values will decrease dramatically.

application. As illustrated in Fig. 4, the RSS value increases gradually when walking a direct path towards an AP. In contrast, the RSS value decreases dramatically when the user takes a turn. To model such a correlation, we define feature functions:

$$
\begin{array}{l} r _ {k _ {1}} \left(L _ {t}, L _ {t - 1}, O _ {t}, O _ {t - 1}\right) = \delta \left(\operatorname{dir} \left(L _ {t}, L _ {t - 1}\right) = a h e a d\right) \tag {18} \\ \times \delta (d i s (O _ {t}. r s s, O _ {t - 1}. r s s) <   = R) \\ \end{array}
$$

$$
r _ {k _ {2}} \left(L _ {t}, L _ {t - 1}, O _ {t}, O _ {t - 1}\right) = \delta \left(\operatorname{dir} \left(L _ {t}, L _ {t - 1}\right) = \text {turn}\right) \tag {19}
$$

$$
\times \delta (d i s (O _ {t}. r s s, O _ {t - 1}. r s s) > R)
$$

where $d i r ( L _ { t } , L _ { t - 1 } ) =$ ahead if the user does not take a turning from $L _ { t }$ to $L _ { t - 1 }$ , direction $\begin{array} { l } { ( y _ { t } , y _ { t - 1 } ) } & { = } \end{array}$ turn otherwise, $d i s ( O _ { t } . r s s , O _ { t - 1 } . r s s )$ is a function to compute the distance of the RSS readings, R is set according to stability of RSS values. We follow [9] to define the RSS distance function di as Euclidean distance between two RSS fingerprints.

# C. Speed-up Parameter Estimation in CRFs

The goal of parameter estimation is to determine the weights $\left\{ \lambda _ { k } , \beta _ { k } , \gamma _ { k } \right\}$ of the feature functions given a training data set $\{ \overrightarrow { D ^ { i ( j ) } } , \overrightarrow { L ^ { i ( j ) } } \}$ . We first show how to efficiently train the weights for spatial and RSS feature functions based on log likelihood, and then the temporal ones.

For spatial correlations, we need to learn $\beta _ { k }$ for each function concerning any sensitive location $s _ { j } ~ \in ~ S$ and any $l _ { j } \in { \mathcal { L } } .$ . We set  k = log $P r ( L _ { t } = s _ { j } | L _ { t - t ^ { \prime } } = l _ { j } )$ . In other words, if a location has a stronger correlation with a private location, it will be more likely to be suppressed. Because such spatial correlations usually occurs between nearby locations, we consider $t ^ { \prime } \leq 3$ .

For RSS data correlations, we first show how to train the iven .rss, $L _ { t } ^ { i ( j ) } , L _ { t - 1 } ^ { i ( j ) }$ and corresponding RSS datay $L _ { t } ^ { i ( j ) } . r s s , L _ { t - 1 } ^ { i ( j ) }$ Lt

$$
\begin{array}{l} R = \arg \max _ {R} \sum_ {j} \sum_ {t = 1} ^ {T} \left\{r _ {k _ {1}} (L _ {t} ^ {i (j)}, L _ {t - 1} ^ {i (j)}, L _ {t} ^ {i (j)}. r s s, L _ {t - 1} ^ {i (j)}. r s s) \right. \\ \left. + r _ {k _ {2}} \left(L _ {t} ^ {i (j)}, L _ {t - 1} ^ {i (j)}, L _ {t} ^ {i (j)}. r s s, L _ {t - 1} ^ {i (j)}. r s s\right) \right\}, \tag {20} \\ \end{array}
$$

where $r _ { k _ { 1 } }$ and $r _ { k _ { 2 } }$ are defined in Equ. 18 and Equ. 19. Then we get feature parameters $\gamma _ { k _ { 1 } }$ and $\gamma _ { k _ { 2 } } .$ :

$$
\gamma_ {k _ {1}} = \log (R - d i s (x _ {t}. r s s, x _ {t - 1}. r s s)) / R; \tag {21}
$$

$$
\gamma_ {k _ {2}} = \log (d i s (x _ {t}. r s s, x _ {t - 1}. r s s) - R) / R. \tag {22}
$$

Note that the greater RSS value varies, the more likely a user will take a turn, and vice versa.

Now we consider the temporal correlations. Remember that we train a CRF for each suppression strategy and then check whether the suppression strategy leaks privacy. Given a particular suppression strategy ${ \mathcal { P } } _ { \mathrm { { i } } }$ , we can set $\{ \theta _ { k } \}$ by Equ. 7 and Equ. 8. Parameters $\left\{ \lambda _ { k } \right\}$ for the temporal features are estimated discriminatively to maximize the conditional loglikelihood of training data:

$$
l (\lambda) = \sum_ {j} \log P r [ \overrightarrow {L ^ {i (j)}} | \overrightarrow {O ^ {i (j)}} ], \tag {23}
$$

where $P r [ \overrightarrow { L ^ { i ( j ) } } | \overrightarrow { O ^ { i ( j ) } } ]$ is defined as Equ. 10 with feature functions defined in Equ. 7,8,15,17,18,19. The derivative of the log-likelihood l( ) with respect to $\lambda _ { k }$ is:

$$
\frac {\partial l (\lambda)}{\partial \lambda_ {k}} = \sum_ {j = 1} ^ {N} \sum_ {t = 1} ^ {T} f _ {k} (L _ {t} ^ {i (j)}, L _ {t - 1} ^ {i (j)}, L _ {t - 2} ^ {i (j)}) \tag {24}
$$

$$
- \sum_ {j = 1} ^ {N} \sum_ {t = 1} ^ {T} \sum_ {l, l ^ {\prime}, l ^ {\prime \prime}} f _ {k} (l, l ^ {\prime}, l ^ {\prime \prime}) P r (l, l ^ {\prime}, l ^ {\prime \prime} | \overrightarrow {O ^ {i (j)}})
$$

The first term is the expected value of $f _ { k }$ under the empirical distribution $\widetilde { P r } ( \vec { L } , \vec { O } )$ . The second term, which arises from the derivative of log $Z ( \vec { O } )$ , is the expectation of $f _ { k }$ under the model distribution $P r ( \vec { L } | \vec { O } ) \widetilde { p } ( \vec { O } )$ . So when the gradient is zero, these two expectations are equal. Because the function l(✓) is concave[15], it can be efficiently maximized by secondorder techniques such as conjugate gradient and L-BFGS. We use L-BFGS with a regularization to train the model.

# D. Speed-up Suppression Strategy Learning

After training the feature parameters for a particular suppression strategy P, we can check whether the strategy meets $\delta - p r i v a c y$ . To choose the best suppression strategy that meets    privacy and maximizes $u t i l i t y$ , we need to iterate all possible . Algorithm 3 shows such a process. This approach is not practical. Even discretizing the probability space [0,1]

Algorithm 3 Find best suppression strategy   
Input: Training data set $\{\overrightarrow{D^{i(j)}},\overrightarrow{L^{i(j)}}\}$ , Privacy profile: S
Output: Optimal suppression strategy: $P^{*}$ 1: Get a floor plan topology G

2: foreach suppression strategy P do

3: Train parameters $\{\lambda_{k},\beta_{k},\alpha_{k},\theta_{k}\}$ for CRF according to $\{\overrightarrow{D^{i(j)}},\overrightarrow{L^{i(j)}}\}$ ;

4: if CheckPrivacy(P,S,G) then

5: u = utility(P);

6: update maxUtility and $P^{*}$ ;

![](images/e5b41f1bd4959e2945fc67dd64ff9975da8fc754f7f0fb91b946e209ad2815de.jpg)



Fig. 5. Floor plan of experiment in the office building

into $\{ 0 , 1 / d , 2 / d , . . . , 1 \}$ , there are still $d ^ { n T }$ strategies need to be checked.

We speed up the search process with a monotonicity property of the suppression strategy. A strategy $\mathcal { P } _ { k }$ dominates $\mathcal { P } _ { j }$ if each probability in $\mathcal { P } _ { k }$ is equal or larger than the one in $\mathcal { P } _ { j } .$ . $\mathcal { P }$ is said to have monotonicity property, if $\mathcal { P } _ { k }$ dominating $\mathcal { P } _ { j }$ preserves $\delta - p r i v a c y$ , given $\mathcal { P } _ { j }$ preserves $\delta - p r i v a c y .$ If we can prove the monotonicity property of ${ \mathcal P } ,$ we can adopt efficient search algorithms to search for the optimal strategy. We prove the monotonicity property in Appendix and use the greedy approach of Mondrian [16] by starting with $\mathcal { P } = 1 , 1 , \cdots , 1$ and gradually reducing the suppression probability until further reducing violates privacy demand.

# IV. EXPERIMENTS

In this section, we analyze the performance of PLP and compare it with MaskSensitive and MaskIt [13] using two read-world context traces:

• The first one contains daily activities of 30 employees for a month, in an office building covering about 1600 $m ^ { 2 }$ , as shown in Fig. 5. The data set contains attributes including location information, RSS values, accelerometer readings and magnetic field data. These data are recorded every 30 seconds with a total length of 7200 minutes.   
The second data set is recorded on a floor of an academic building in a university, also covering over 1600 $m ^ { 2 }$ , as shown in Fig. 6.. The trace contains 16,498 records in 600 traces by 4 users. Recorded attributes are accurate locations, RSS reading and accelerometer data.

Our evaluation centers around three key questions: 1. Is PLP efficient enough to work in practice? 2. Is PLP more secure than former work? 3. How much utility will we sacrifice for an user-specified privacy guarantee?

In this section, we first state the experimental methodology and analyze the evaluation results to answer the aforementioned three key questions.

# A. Experimental Methodology

We first pre-process the user data by mapping user trajectories to the possible locations as shown in Fig. 5 and Fig. 6. For each user, potential correlations are trained on the first half of his/her traces to build a CRF. With such a model and a set of predefined sensitive locations, PLP filters the sensing data and reports privacy-preserving information based on the second half of the trace. The privacy parameter   is set by users in real application. We set   to 0.1 in our evaluation, unless otherwise stated. And the system is said to protect privacy if Equ. 4 is satisfied. An attack model described in Section II-C, is implemented to reveal the sensitive contexts from the reports of PLP.

![](images/ee702a5feedcb6c02760175d22d5696c92f34b56fbe3c48f15d8106bc2688e94.jpg)



Fig. 6. Floor plan of experiment in the academic building

![](images/2dc5ffd9361c67355f4de531cda1956c097fabbbffecedc76cc773286ffd2ca0.jpg)



Fig. 7. MaskSensitive and MaskIt can be attacked with the model considered in CRF, while CRF is secure with respect to attack models in MaskSensitive and MaskIt

We implement a prototype of PLP on a PC with 2.3GHz CPU and 8GB memory. To evaluate the overhead on a smartphone, we conduct experiments on an iPhone 5.

# B. Performance Evaluation

Efficiency. We evaluate the efficiency of PLP by comparing it with $3 ^ { r d }$ -order Markov Chain, 2nd-order Markov Chain and MaskIt[13] that uses 1st-order order Markov Chain. Table II shows the average time to train the models, and in-practical running time. It takes 38 minutes on average for training, while training a $3 ^ { r d } .$ -order Markov Chain takes much more time (4.1 hours). We believe the data correlations, and the set of private locations will not change much in a day. PLP is trained when the user is charging his/her phone about once a day. As charging normally takes a few hours, our speed-up training algorithm is fast enough to work in practice. PLP is also practical to offer real-time responses, because it takes less than 1ms to make a suppression decision on a phone. Note that we can extend ELP to large scale scenarios. In that case, each

TABLE II COMPARISON OF AVERAGE PROCESSING TIMES 

<table><tr><td></td><td>MaskIt</td><td> $2^{nd}$  MC</td><td> $3^{rd}$  MC</td><td>PLP</td></tr><tr><td>initial</td><td>18min</td><td>39min</td><td>4.1h</td><td>38min</td></tr><tr><td>workInPractise</td><td>128ms</td><td>134ms</td><td>259ms</td><td>1ms</td></tr></table>

![](images/d72a7de945d5a0b0fa3d56eeedaeb03427cf6078bb9b281ca2363e661a9813a5.jpg)



Fig. 11. Privacy-Utility trade-off with different percentage of sensitive locations

node may represent an area, such that the total nodes in the CRF model will not change much.

Privacy guarantee. PLP is secure against different adversaries, while other privacy-preserving systems [13] are vulnerable to the attack model in our work. Consider a user defines 20% of total location information as sensitive. On the one hand, let the user report crowdsensing data by existing privacy-preserving systems, i.e. MaskSensitive and MaskIt [13], and be attacked by our attack model. MaskSensitive is a naive approach that only suppresses sensitive information, while MaskIt uses a HMM to model the correlations.

We show that our proposed attack model can disclose about 68% of sensitive information from the report by MaskSensitive (13% of all data in Fig. 7). Our attack model can also disclose about 31% of sensitive information from the report by MaskIt (7% of all data in Fig. 7). Thus we show that the attack model we considered is more powerful than [13]. On the other hand, we let the user report with PLP and attack with the method proposed in MaskIt. In Fig. 7, we show the attack model considered in MaskIt cannot disclose information from the report by PLP.

But how much utility will PLP sacrifice? We can see in Fig. 7, MaskIt uploads 63% of crowdsensing data while PLP uploads 63%. So PLP sacrifice little utility compared with MaskIt to guarantee that all privacy of the user will not be disclosed with a stronger attacker.

Privacy-Utility trade-off. The crowdsensing system will gain less utility if users want more privacy. How much utility will we sacrifice for an user-specified privacy guarantee? We conduct experiments to show the trade-off between the utility and the privacy degree.

By varying the privacy degree   from 0.05 to 0.3 and percentage of private information from 10% to 40%, we evaluate the trade-off between utility and privacy level. Fig. 8 and Fig. 9 shows the average utility of users by setting different sensitive locations. We can see that it is more difficult to suppress private information at corridors because they are highly correlated with a large number of other locations. On the contrary, it is easier to protect private information at a user’s own office. This is because offices are only correlated with a few locations, and the prior probability for the user to be in personal office is high. The floor plan (Fig. 6) shows that the traces in the second data set do not have office rooms

![](images/a8d2afcb4b7cf971daef0457cd7ddd1b251a23b10d34d98c00141d54edca1c11.jpg)



Fig. 8. Utility vs. privacy in office building with different sensitive locations

![](images/26c93e6d080a2287b9449677d97a125bdd21ca7de58b18e6eee3442bfa6a93af.jpg)



Fig. 9. Utility vs. privacy in academic building with different sensitive locations

![](images/fe77334ad5376ca8e52c1655c0925e5b1444bf9a5affbaaf9f5d99661a08d351.jpg)



Fig. 10. Utility vs. privacy with different map topology

for individual users.

Fig. 10 compares the average utility of users in the office building and the academic building. The complicated topology in the office building makes it easier to hide private locations. Thus the utility of users in office building is higher than users in the academic building. We can also see that PLP can gain an average utility of more than 0.6 in a simple topology environment by setting $\delta = 0 . 1$ , while average utility gain can reach 0.7 in the office building. We also evaluate the tradeoff between utility and the percentage of sensitive locations. We can see in Fig. 11 that utility is guaranteed above 60% in both data sets if the user defines less than 20% of locations as privacy. The performance of the crowdsensing system is poor when the defined private locations are greater than 40%.

# V. RELATED WORK

Crowdsensing. Many recent studies develop crowdsensing platforms for location based mobile computing applications. SurroundSence [17] utilizes sensors on smartphones to collect identifiable fingerprints signals for logical localization. Escort [18] obtains cues from social encounters and leverages an audio beacon infrastructure to guide a user to a desired person. WILL [9] and LifS [8] design an indoor localization technique leveraging user mobility and WiFi infrastructure while avoiding site survey. Although people enjoy these location based crowdsensing applications, privacy concerns undermine their will to participate.

Location privacy. Many efforts have been made to preserve privacy while releasing a user’s location. There are four main classes of solutions: perturbation, k-anonymity, secure multiparty computation (SMC) and homomorphic encryption. The first class [19, 20], which adds independent noise to sensing data, are proven to be inadequate, if an adversary uses filtering techniques [20, 21] to reconstruct the distribution of the original data. The second class, anonymity-based approaches [5, 6], hide the sensing data among a set of possible values. For example, for location data, a user reports a region instead of exact location to the server. However, such coarse location information may degrade the data utility. What’s more, in crowdsensing, location data are frequently updated. This dynamic behavior introduces huge overhead to keep the data k-anonymous. The third class, SMC techniques [22, 23], rely on a joint computation among a set of involved peers. This will incur a high communication or computation overhead when participant population is large. The fourth class aggregates data based on homomorphic encryption[11, 24], which allows a user to perform data aggregation on individual data without knowing the data. However, to interpret the final aggregation, a server needs to know which users reported data, which is not always desirable.

The above mentioned techniques do not consider strong adversaries knowing the system and spatio-temporal correlations, while the following are several studies aim to protect against analyze of temporal correlations [12, 13, 25]. [12] considers an adversary knowing the maximum velocity of users. If locations are continuously reported, an attacker can correlate locations from multiple timestamps to accurately pinpoint the user position. They propose spatial and temporal cloaking approaches to hind the correlations. This work is vulnerable to attacks from the adversaries leveraging spatial correlations (e.g., a shorter path is usually preferred). [25] considers how to suppress events in a stream to reduce the disclosure of sensitive patterns while maximizing the detection of nonsensitive patterns. They protect against adversaries knowing temporal correlations among nearby or overlapping events, but not against adversaries also knowing the system and other correlations.

The work that is closest to us is MaskIt [13] and CQue [26]. MaskIt seeks to leverage a Markov Chain to model the temporal correlations. The system evaluates the sensitivity of locations based on the correlation with sensitive locations. A location with higher sensitivity should be suppressed with a higher probability and vice versa. However, dependencies not modeled in HMM may be revealed to the adversaries to help inferring privacies (e.g. Fig. 1). CQue [26] also use a generative model Dynamic Bayesian Network to model the temporal correlations. These generative models all make conditional independent assumption among the observations, which may be used by the adversaries to disclose privacy.

To the best of our knowledge, PLP is the first work that protects privacy against strong adversaries knowing the system and any leakage of potential spatio-temporal correlations among location data in crowdsensing.

# VI. CONCLUSION

In this work, we study the problem of privacy-preserving location stream report. PLP employs a conditional random field to model potential spatio-temporal correlations between sensitive and nonsensitive contexts, and report sensing data with a probability based on the correlations with private locations. We present a learning algorithm to study the feature weights in CRF and an algorithm to find the best report strategy that maximizes the utility, while protects against strong adversaries knowing our system and potential spatiotemporal correlations. Our experiment on real-world traces demonstrates that PLP is effective to achieve privacy without sacrificing much utility, and is efficient to offer real-time response. Admittedly, the adversary can always build an even better model in principle that is able to reveal sensitive information. The defender can never say with certainty that all attacks are covered, in the endless competition between adversaries and defenders continues.

# VII. ACKNOWLEDGEMENTS

The authors thank the anonymous reviewers for their valuable feedbacks. This research is supported in part by NSFC under Grant No. 61472219, 61472218, 61402338, and NSFC Distinguished Young Scholars Program under Grant No. 61125202.

# REFERENCES

[1] J. Corburn, “Confronting the challenges in reconnecting urban planning and public health,” American journal of public health, vol. 94, no. 4, pp. 541–546, 2004.   
[2] S. Shah, F. Bao, C.-T. Lu, and I.-R. Chen, “Crowdsafe: crowd sourcing of crime incidents and safe routing on mobile devices,” in Proceedings of ACM GIS, 2011.   
[3] Y. Zheng, L. Zhang, X. Xie, and W.-Y. Ma, “Mining interesting locations and travel sequences from GPS trajectories,” in Proceedings of ACM WWW, 2009.   
[4] P. Zhou, Y. Zheng, and M. Li, “How long to wait?: predicting bus arrival time with mobile phone based participatory sensing,” in Proceedings of ACM MobiSys, 2012.   
[5] L. Sweeney, “k-anonymity: A model for protecting privacy,” International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, 2002.   
[6] M. Gruteser and D. Grunwald, “Anonymous Usage of Location-Based Services Through Spatial and Temporal Cloaking,” in Proceedings of ACM MobiSys, 2003.   
[7] B. Wang, B. Li, and H. Li, “Gmatch: Secure and privacypreserving group matching in social networks,” in Proceedings of IEEE GLOBECOM, 2012.   
[8] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: wireless indoor localization with little human intervention,” in Proceedings of ACM MobiCom, 2012.   
[9] C. Wu, Z. Yang, Y. Liu, and W. Xi, “WILL: Wireless Indoor Localization Without Site Survey,” in Proceedings of IEEE INFOCOM, 2012.   
[10] L. Zhang, X. Li, Y. Liu, and T. Jung, “Verifiable Private Multi-party Computation: Ranging and Ranking ,” in Proceedings of IEEE INFOCOM, 2013.   
[11] Q. Li and G. Cao, “Efficient and privacy-preserving data aggregation in mobile sensing,” in Proceedings of IEEE ICNP, 2012.   
[12] G. Ghinita, M. L. Damiani, C. Silvestri, and E. Bertino, “Preventing velocity-based linkage attacks in locationaware applications,” in Proceedings of ACM GIS, 2009.

[13] M. Gotz, S. Nath, and J. Gehrke, “MaskIt: Privately ¨ Releasing User Context Streams for Personalized Mobile Applications ,” in Proceedings of ACM SIGMOD, 2012.   
[14] J. Lafferty, A. McCallum, and F. Pereira, “Conditional random fields: Probabilistic models for segmenting and labeling sequence data,” in Proceedings of IEEE ICML, 2001.   
[15] C. Sutton and A. McCallum, “An Introduction to Conditional Random Fields for Relational Learning,” Introduction to statistical relational learning, 2007.   
[16] K. LeFevre, D. J. DeWitt, and R. Ramakrishnan, “Mondrian multidimensional k-anonymity,” in Proceedings of IEEE ICDE, 2006.   
[17] M. Azizyan, I. Constandache, and R. R. Choudhury, “SurroundSense: mobile phone localization via ambience fingerprinting,” in Proceedings of ACM MobiCom, 2009.   
[18] I. Constandache, X. Bao, M. Azizyan, and R. R. Choudhury, “Did you see Bob?: human localization using mobile phones,” in Proceedings of ACM MobiCom, 2010.   
[19] H. Ahmadi, N. Pham, R. Ganti, T. Abdelzaher, S. Nath, and J. Han, “Privacy-aware regression modeling of participatory sensing data,” in Proceedings of ACM Sensys, 2010.   
[20] Z. Huang, W. Du, and B. Chen, “Deriving private information from randomized data,” in Proceedings of ACM SIGMOD, 2005.   
[21] M. Li, S. Yu, N. Cao, and W. Lou, “Privacy-preserving distributed profile matching in proximity-based mobile social networks,” IEEE Transactions on Wireless Communications, vol. 12, no. 5, pp. 2024–2033, 2013.   
[22] C. Rottondi, G. Verticale, and A. Capone, “Privacypreserving smart metering with multiple data consumers,” Computer Networks, vol. 57, no. 7, pp. 1699– 1713, 2013.   
[23] R. Cramer, I. Damgard, and S. Dziembowski, “On the ˚ complexity of verifiable secret sharing and multiparty computation,” in Proceedings of ACM STOC, 2000.   
[24] E. Shi, T. Chan, E. G. Rieffel, R. Chow, and D. Song, “Privacy-Preserving Aggregation of Time-Series Data.” in Proceedings of ISOC NDSS, 2011.   
[25] D. Wang, Y. He, E. Rundensteiner, and J. F. Naughton, “Utility-maximizing event stream suppression,” in Proceedings of ACM SIGMOD, 2013.   
[26] A. Parate, M.-C. Chiu, D. Ganesan, and B. M. Marlin, “Leveraging graphical models to improve accuracy and reduce privacy risks of mobile sensing,” in Proceedings of ACM MobiSys, 2013.