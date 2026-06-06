# RPM: Local Differential Privacy based Inventory Forecasting

Lan Zhang

University of Science and Technology of China Hefei, China

zhanglan@ustc.edu.cn

Abstract—In the Cost-Per-Mille (CPM) advertising business scenario that adopts the guaranteed delivery model, ad publisher predicts the future available impressions inventory of each advertising placement under the constraints of each target audience based on the historical impressions data, so as to sell advertising resources reasonably. However, historical data threatens user and publisher privacy during the Sharing-Aggregation-Analysis procedure. In addition, internet companies that act as ad publishers are reluctant to release data constrained by laws and regulations, which creates Isolated Data Island. In order to realize privacy-preserving data sharing and publishing and improve data availability as much as possible to build inventory structure, we propose a novel Local Differential Privacy (LDP) method RPM to process user impressions logs and design a privacy-preserving inventory forecasting(PPIF) framework combining clustering and sampling in this work. LDP is a promising privacy standard. There is no need for trusted third parties to participate. Each user perturbs sensitive data locally and uploads the disturbed records. The real data does not leave the local area, providing the user with the privacy preserving effect of indistinguishable individuals. There is a trade-off between privacy protection and data availability. Under availability constraints, LDP is usually used in industry only for frequency and mean statistics operations. There is plenty of room for research in designing foundational LDP technologies to support more data-mining computing tasks such as clustering. The privacy-preserving effect of RPM is demonstrated by rigorous mathematical proof, and the simulation experiments prove that the inventory estimation results obtained by using RPM are more accurate than other existing LDP methods.

Keywords-local differential privacy, collecting user data, inventory forecast, clustring, sampling

# I. INTRODUCTION

With the widespread use of big data analysis technology, server records every imprint of the user’s operational information during the service period. Personal data uploaded by users for free is transformed into a potential commodity. In return, data collectors acting as server will provide quality services to users. At the same time, server will also perform data mining on the collected user data to increate greater value. Internet advertising helps free internet products and media providers find a means to monetize at scale, and it brings rich profits to the server. Many video advertisements have always adopted the CPM business model, which is different from the traditional web advertising Cost-Per-Download (CPD) model. This business model mainly uses a guaranteed delivery model, that is, selling the number of ad impressions

Cong Tang University of Science and Technology of China. Hefei, China tangcong@mail.ustc.edu.cn

![](images/c1cfb1f0a2282065cfbc7b373835556c0f903a4e114a03bc8315c4d3f81ff61c.jpg)



Fig. 1: Example of user log records and orders. $S _ { i j }$ represents the total amount of request of the i-th user and the j-th type PV, and $O _ { k }$ represents the quantity demanded of the k-th order. The dash line indicates an impression in the request is eligible to the connected order.

on a specific group of audience [1]. Estimate the available impressions (inventory) under any group orientation within a certain period of time (e.g., 1 day) in the future, so that server can sell advertising resources reasonably. Therefore, inventory forecasting is a widely used technique in computational advertising. Users enjoying media services regularly upload channel requests for a period of time to the server. One part of the record is user attributes, such as region or platform, and another part is related to behavior requests, such as the channel visited. Fig. 1 show the example, each user maintains a log record representing supply information locally every day. The server collects records for statistical analysis to devise order tactics. The data header attribute can be defined as a tuple, -id, region, platform, movie, cartoon. For example, an iPhone user from Shanghai watched two advertisements on a movie channel within a day, then the uploaded data is id, Shanghai, iP hone, 2, 0 .

Most apps require users to accept the privacy policy documents of access control and data record description proposed by the server before enjoying using the service. Most people directly agree to use the application by default, but personal information is uploaded to the service provider unwittingly. The uploaded data is not created by the users themselves, but naturally generated in a certain information service process. These data threaten the privacy of users. Data privacy is different from data security. Data security protects data from malicious insiders and external attackers, but data privacy controls how data is collected, shared, and used. In the periodic log uploaded by the user in the advertising scene, we denote the attributes that define the user (such as id, region, and platform) as UV attributes, and the attributes define the number of channel visits (such as movies, cartoons, etc.) as PV attributes. If users want to enjoy basic services, they have to provide UV information. We only conduct LDP on PV to protect privacy. If there is a privacy collection method that is acceptable to both users and the server, the server can further optimize the service quality under the premise of privacy protection and avoid unnecessary legal disputes.

Contributions. The main contributions of the paper are summarized as follows.

• A novel LDP algorithm. Many existing LDP researches have achieved perfect performances in frequency and mean(sum) estimation. Due to the large sample size, there is little difference in these methods in large-scale data setting. In addition, classical approaches are no longer applicable in complex computing tasks. In this paper, we propose a novel LDP basic method, RPM, which performs well under the clustering-sampling-summation computational task.   
• Privacy-Preserving inventory forecasting (PPIF) framework. The construction of reasonable inventory structure will directly affect the performance of advertising sales and delivery. RPM improves the privacy protection effect of the inventory forecasting subcomputation task. PPIF framework satisfies the purpose of the server to realize the basic business under the premise of protecting privacy.   
• Personalized privacy settings. Strong privacy protection processing means that the quality of the service enjoyed by users is low. Some users may prefer the quality of the service rather than their privacy. PPIF makes reasonable use of the disturbed data under different privacy budgets, which reduces the global error and accelerates the iteration speed.

Organization. The remainder of this paper is organized as follows. We review related works in Section II. Section III formulates the problem and provides essential background of LDP. Section IV introduces our proposed RPM algorithm and reviews the classical LDP algorithm for experiment comparison. Section V describes in detail the entire process of PPIF framework. Section VI demonstrates our experimental results. Section VII summarizes the whole paper.

# II. RELATED WORK

The concept of Differential Privacy(DP) was first proposed by Dwork. DP models all require a trusted server. Users upload raw data to the server’s database, and the server performs DP processing on database-based query results, which is mainly used to resist differential attacks. In the LDP scenario, the data processing occurs before the user uploads the data, the server receives only the disturbed version. A semi-honest model that does not require a trusted server is more realistic. The most classic LDP technique is the Random Response [2], which requires each user to respond to the original result with a certain probability, and finally the service side can still correct the approximate statistical results. Recently in the industry, Apple announced at the WWDC conference that Apple uses LDP to protect the privacy of IOS and MAC users, and it has been successfully deployed in multiple scenarios, such as collecting the frequency of users sending emoticons. Google also uses LDP technology to collect the behavior data of millions of users every day from the Chrome browser, called RAPPOR. Its core idea is to convert sensitive strings into bit strings through Bloom filters, and then perform Random Response processing for each bit. The successful application of LDP in the industry has attracted the attention of more researchers. Note that the above techniques are used to collect single-dimensional category attributes, but continuous numerical data in actual databases is more common. [3]–[8] are all studies of mean estimation. There are also some applications where LDP is combined with other technologies for more computing tasks. Ye et al. [9] combines Random Response and Harmony [6] method to propose a statistical method for key-value pairs. Sun et al. [10] performs random response processing for each bit on the output encoding result of [11] to calculate the distance between the original data, but the result is affected by the combination of encoding length and privacy budget, making the method less used in the actual scene. Wang et al. [7] combines their own PM method and [5] to propose the HM method, which is extended to multidimensional mean statistics, and finally the mean calculation is applied to stochastic gradient descent.

The estimation algorithm introduced in [1] is estimated based on the flow sheet. The result of inventory estimation and a specific algorithm are used to describe the combined inventory of multiple directional dimensions as accurately as possible. However, estimates based on combined dimensions are difficult to accurately reach the user granularity, and cannot support the transformation of sales to a more refined inventory structure. But if the user granularity is to be estimated, the time complexity will be tens of millions of times higher, and the result cannot be obtained in an acceptable time. In response to the above problems, a new inventory estimation system RAP based on user granularity is proposed in [12], which fully combines deep learning estimation models and sampling to reduce complexity. On this basis, we perform LDP processing on the input data to protect user privacy.

# III. PRELIMINARIES

This paper investigates the issue of the aggregator collects user data in the context of LDP and maximizes the availability of user data to obtain statistical models for data analysis on the premise of ensuring that user privacy is not compromised. Without loss of generality, suppose there are n users in total, and the local PV data for each user $u _ { i }$ is a d-dimensional vector $\langle v _ { i 1 } , v _ { i 2 } , \cdots , v _ { i d } \rangle$ . The data of each dimension can be numeric values or categories. Suppose the continuous domain of each numeric attribute is $[ - 1 , 1 ]$ . For ease of description, we let the one-dimensional user data denotes $v _ { i }$ .

In order to protect user privacy, the local differential privacy technology is used here. Each user $u _ { i }$ uses the randomized perturbation function $\boldsymbol { \mathcal { M } } ( \boldsymbol { \epsilon } , \boldsymbol { v _ { i } } )$ that meets the LDP property to process data locally and obtain output $v _ { i } ^ { * }$ , and then upload $v _ { i } ^ { * }$ to the aggregator. - is the privacy budget parameter, which controls the balance between privacy protection strength and data availability. The user real data does not leave the local during the whole process. The randomized perturbation function $\boldsymbol { \mathcal { M } } ( \boldsymbol { \epsilon } , \boldsymbol { v _ { i } } )$ satisfies --LDP, defined as follows:

Definition 1 (--Local Differential Privacy (LDP)): A randomized algorithm M satisfies --local differential privacy if and only if for any two input tuples v, v in the domain of M and for any output $v ^ { * }$ , we always have:

$$
\operatorname * {P r} (\mathcal {M} (v) = v ^ {*}) \leq \operatorname * {P r} (\mathcal {M} (v ^ {\prime}) = v ^ {*}) \cdot e ^ {\epsilon}. \tag {1}
$$

Unlike centralized DP, which needs an honest third party, the local DP requires a semi-honest third party. Intuitively --LDP means that two different inputs v, $v ^ { \prime }$ can both output the same output $v ^ { * }$ with different probabilities through the randomized function $\mathcal { M } .$ , The upper bound of the two probability ratios is $e ^ { \epsilon }$ . In other words, if the attacker only gets $v ^ { * }$ , and to a certain extent (controlled by -) cannot be sure whether the corresponding input is v or $v ^ { \prime } ,$ , which is also different from DP defined on neighbor datasets.

Inventory forecasting can be defined as the concept of given a set of directional labels to estimate the amount of inventory that will fit these directional tag combinations over a certain period of future time. Tencent advertising has made in-depth exploration in the field of contract advertising. The traditional approach [1] is to split the total inventory into a fine-grained inventory set, and any directional inventory is a subset of the fine-grained inventory set. But the sales delivery system is becoming more and more elaborative at present, and the traditional estimation based on the combination dimension is difficult to be accurate to the user granularity, which cannot support the more refined inventory structure. Zhang et al. [12] have designed a new inventory forecasting system based on user granularity: Request-level guaranteed Delivery Planning (RAP), which fully combines deep learning forecasting model and sampling to reduce system complexity and achieve better performance in more complex directional combination scenarios. RAP describes the demographics of the future by estimating the percentage of users per category.

Given the historical N -day user sets ${ \bf \bar { \Gamma } } D ^ { 1 } , D ^ { 2 } , \cdots , D ^ { N }$ , our goal is to predict the future M -day user sets $\bar { D ^ { \prime } } \bar { \bar { 1 } } \bar { + 1 } , \bar { D ^ { \prime } } \bar { \bar { N } } + 2 , \cdot \cdot \cdot \bar { \bar { \ } } D ^ { \prime } \bar { N } + M$ , which should minimize the loss function $L ( D ^ { \prime N + 1 } , \cdot \cdot \cdot , D ^ { \prime N + M } )$ . Although the total amount of exposure is large, the amount of exposure generated by a single user is very small. It’s difficult to find reasonable features to distinguish between the two different types of users. Moreover, it is not necessary to estimate the state of each user, only to ensure the accuracy of the total amount of exposure. RAP aggregates users according to UV type, and each category has a larger number of users after aggregation, which helps to improve model accuracy. For example, -Beijing, Android and -Shanghai, iP hone are two different UV aggregations, and each aggregation has a different category of users. RAP uses deep learning prediction model to guide sampling decision, making it more reasonable than naive random sampling method.

# IV. COLLECTING A SINGLE NUMERIC ATTRIBUTES

The study of single-dimensional numerical mean estimation is the cornerstone of all statistical model calculations. The core solutions of frequency estimation and multi-dimensional data collection are the deformation of single-dimensional methods. Therefore, this section focuses on the single-dimensional numerical mean estimation. Section IV-A proposes the ramppiecewice method for the PM method. Section IV-B proposes the staircase method with the minimum variance in the LDP scenario. Section IV-C reviews several existing methods and analyzes their differences.

# A. The Ramp-Piecewise Mechanism

In this section, we propose the Ramp-Piecewise Mechanism (RPM). Given sensitive data $v _ { i }$ to be processed and privacy parameters $\epsilon ,$ the randomized perturbation function $\mathcal { M }$ generates output $v ^ { * }$ . The range $[ l ( v _ { i } ) , r ( v _ { i } ) ]$ with high probability is not uniform sampling, but decreases from $v _ { i }$ to $l ( v _ { i } )$ and $r ( v _ { i } )$ successively. Intuitively, in order to keep the total probability as 1, the range of $\left[ C , l ( v _ { i } ) \right]$ ] and $[ r ( v _ { i } ) , C ]$ should be lengthened. In this way, the output range of the whole population will be enlarged, the variance will be enlarged, and the accuracy will be reduced.

$\mathbb { E } _ { \mathcal { M } } [ v _ { i } ^ { * } | v _ { i } ]$ denotes the expectation of the randomized versions $v _ { i } ^ { * }$ given input $v _ { i } . \ D A ( { \mathcal { M } } )$ denotes the availability of data for analysis using a randomized version, which is measured differently for different computing tasks. We are addicted to finding a randomized mechanism $\mathcal { M }$ that maximizes $D A ( { \mathcal { M } } )$ by solving the following constraint minimization problem:

$$
\max _ {\mathcal {M}} D A (\mathcal {M}),
$$

${ \mathrm { s . t . ~ E q . ~ } } ( 1 ) ,$ (2)

$$
\mathbb {P} _ {\mathcal {M}} [ v _ {i} ^ {*} \in \mathbb {V} ^ {*} | v _ {i} ] = 1,
$$

$$
\mathbb {E} _ {\mathcal {M}} [ v _ {i} ^ {*} | v _ {i} ] = v _ {i}.
$$

The three constraints respectively illustrate that the mechanism M satisfies LDP property, the area bounded by the probability density function and the coordinate axis is 1, and the mean estimate is unbiased where $\mathbb { V } ^ { * }$ is the range of randomized function $\mathcal { M }$ .

RPM takes as input a value $v _ { i } ~ \in ~ [ - 1 , 1 ]$ , and outputs a perturbed value $v _ { i } ^ { * } \in [ - C , C ]$ where $\begin{array} { r } { C = \frac { { \dot { e } } ^ { \epsilon } + 5 + 2 \sqrt { 6 + 3 e ^ { \epsilon } } } { e ^ { \epsilon } - 1 } } \end{array}$ e-+5+2√6+3e- . The probability density function of $v _ { i } ^ { * }$ as follows:

$$
p d f \left(v _ {i} ^ {*} = x \mid v _ {i}\right) = \left\{ \begin{array}{l l} \frac {p}{e ^ {\epsilon}}, & x \in [ - C, l \left(v _ {i}\right)) \cup (r \left(v _ {i}\right), C ] \\ k _ {1} x + b _ {1}, & x \in [ l \left(v _ {i}\right), v _ {i} ] \\ k _ {2} x + b _ {2}, & x \in \left(v _ {i}, r \left(v _ {i}\right) \right] \end{array} \right. \tag {3}
$$

![](images/ee87d062ceac2f6accba2ecde1c51a39d4ac95496be5c504b89b4bb2c577b92d.jpg)



(a) vi = −1

![](images/668029cd09b290f0ded2488aa574482e0656895982e092465d205d7216703ea4.jpg)



(b) vi = −0.4

![](images/79ee0e07ed3e04a3d5a755510e33f9f792d33d557b65323e4dc2159c0fc77105.jpg)



(c) vi = −1

![](images/8ac01e3ef31306aa385582a1860d02b603ce12aa7659ed0d0a1b9d0dc626b5db.jpg)



(d) vi = −0.4   
Fig. 2: The probability density function of RPM when $\epsilon = 1$ .

where

$$
l (v _ {i}) = \frac {3 v _ {i}}{p (1 - \frac {1}{e ^ {\epsilon}})} - \frac {C - 1}{2} - \frac {v _ {i}}{2},
$$

$$
r (v _ {i}) = l (v _ {i}) + C - 1, \tag {4}
$$

$$
p = \frac {6}{(1 - \frac {1}{e ^ {\epsilon}}) (C - 1) (C + 2)}
$$

Both $y = k _ { 1 } x + b _ { 1 }$ and $y = k _ { 2 } x + b _ { 2 }$ go through this point $( v _ { i } , p )$ . The two lines pass through point $( l ( v _ { i } ) , \frac { p } { \epsilon } )$ and point $( r ( v _ { i } ) , \frac { p } { \epsilon } )$ respectively. In addition, $\mathbb { E } ( v _ { i } ^ { * } ) = v _ { i }$ . By Equation 1, for any $v _ { i } , v _ { i } ^ { \prime } ,$ we have $\begin{array} { r } { \frac { p d f ( v ^ { * } | v _ { i } ) } { p d f ( v ^ { * } | v _ { i } ^ { \prime } ) } \le \frac { \bar { p } } { p / e ^ { \epsilon } } = e ^ { \epsilon } } \end{array}$ pp/e- = e-, which proves that RPM satisfies --LDP.

Similar to the method mentioned above, the second version selects random sampling near the input, with a decreasing probability of sampling far away from the input. RPM-flat takes as input a value $v _ { i } \in [ - 1 , 1 ]$ , and outputs a perturbed value $v _ { i } ^ { * } ~ \in ~ [ - C , C ]$ where $\begin{array} { l l l } { C } & { = } & { { \frac { 2 e ^ { \epsilon } + 1 + { \sqrt { 3 e ^ { 2 \epsilon } + 6 e ^ { \epsilon } } } } { e ^ { \epsilon } - 1 } } } \end{array}$ . The probability density function of $v _ { i } ^ { * }$ as follows:

$$
p d f (v _ {i} ^ {*} = x | v _ {i}) = \left\{ \begin{array}{l l} p, & x \in [ l (v _ {i}), r (v _ {i}) ] \\ k _ {1} x + b _ {1}, & x \in [ - C, l (v _ {i}) ] \\ k _ {2} x + b _ {2}, & x \in (r (v _ {i}), C ] \end{array} \right. \tag {5}
$$

where

$$
l (v _ {i}) = \frac {3 v _ {i}}{p (1 - \frac {1}{e ^ {\epsilon}}) (2 C - 1)} - \frac {C - 1}{2},
$$

$$
r (v _ {i}) = l (v _ {i}) + C - 1, \tag {6}
$$

$$
p = \frac {6}{(1 - \frac {1}{e ^ {\epsilon}}) (C + 1) (2 C - 1)}
$$

The two lines $y = k _ { 1 } x + b _ { 1 }$ and $y = k _ { 2 } x + b _ { 2 }$ pass through two points $( - C , \frac { p } { e ^ { \epsilon } } ) , ( l ( v _ { i } ) , p )$ and two points $( r ( v _ { i } ) , p ) , ( C , \frac { p } { e ^ { \epsilon } } )$ ) respectively. In addition, $\mathbb { E } ( v _ { i } ^ { * } ) = v _ { i }$ . By Equation 1, for any $v _ { i } , v _ { i } ^ { \prime } ,$ we have $\begin{array} { r } { \frac { p d f ( v ^ { * } | v _ { i } ) } { p d f ( v ^ { * } | v _ { i } ^ { \prime } ) } \le \frac { p } { p / e ^ { \epsilon } } = e ^ { \epsilon } } \end{array}$ p/e- = e-.

# B. The staircase method with the smallest variance

The $r ^ { * }$ in the staricase mechanism Geng et al. [4] give is obtained by the minimization cost function $V ( \mathcal P )$ . For the convenience of comparison, we also want to use the variance to measure the dispersion between the random variable and the original mean. We get the new $r ^ { \prime }$ by minimizing the variance of the staricase mechanism. Let $\ b \ = \ e ^ { - \epsilon }$ , we can compute $V a r ( \mathcal { P } _ { r } )$ via

$$
\begin{array}{l} \operatorname{Var} \left(\mathcal {P} _ {r}\right) = \int_ {x \in \mathbb {R}} x ^ {2} p d f (x) d x = 2 \int_ {0} ^ {+ \infty} x ^ {2} p d f (x) d x \\ = \Delta^ {2} [ \frac {1}{3} \frac {b + r ^ {3} (1 - b)}{b + r (1 - b)} + \frac {b}{1 - b} \frac {b + r ^ {2} (1 - b)}{b + r (1 - b)} + \frac {b (1 + b)}{(1 - b) ^ {2}} ]. \\ \end{array}
$$

Note that the term $\frac { b ( 1 + b ) } { ( 1 - b ) ^ { 2 } }$ is independent of $r .$ Define

$$
g (r) = \frac {1}{3} \frac {b + r ^ {3} (1 - b)}{b + r (1 - b)} + \frac {b}{1 - b} \frac {b + r ^ {2} (1 - b)}{b + r (1 - b)}. \tag {7}
$$

and thus to minimize $V ( \mathcal P _ { \nabla } )$ over $r \in [ 0 , 1 ]$ , we only need to minimize $g ( r )$ over $r \in [ 0 , 1 ]$ . The derivative of $g ( r )$ is

$$
g ^ {\prime} (r) = \frac {r ^ {3} \frac {2}{3} (1 - b) ^ {2} + r ^ {2} 2 b (1 - b) + r 6 b ^ {2} - b (1 - b) - 3 b ^ {2}}{(b + (1 - b) r) ^ {2}}.
$$

Set $g ^ { \prime } ( r ) = 0$ and we get $\begin{array} { r } { r = \sqrt [ 3 ] { \frac { b ^ { 2 } + b } { 2 } } \cdot \frac { 1 } { 1 - b } - \frac { b } { 1 - b } . } \end{array}$

# C. Existing Solutions

According to the difference of function output range, we divide LDP fundamental methods into the following four categories, and introduce the existing LDP methods in the following categories for experimental comparison.

Inject an unbounded range of noise. The Laplace Mechanism [3] is a classical method in DP scenarios, and it can also be applied to the LDP settings by following the following steps. Considering only the one-dimensional case, it is assumed that each user $u _ { i }$ has numerical data $v _ { i }$ locally, and the randomized function M is expressed in the Laplace mechanism as follows: $\begin{array} { r } { v _ { i } ^ { * } \ = \ \mathcal { M } ( v _ { i } , \epsilon ) \ = \ v _ { i } + L a p ( \frac { \Delta } { \epsilon } ) , } \end{array}$ , where $\Delta$ is the global sensitivity, $v _ { i } \in [ - 1 , 1 ]$ , since $\Delta = 2$ . $L a p ( \lambda )$ denotes a random variable that follows a Laplace distribution of scale $\lambda ,$ with the following probability density function: $\begin{array} { l } { { p d f ( x ) ~ = ~ \frac { 1 } { 2 \lambda } e x p ( - \frac { | x | } { \lambda } ) } } \end{array}$ . Once the aggregator has collected all the perturbation results uploaded by individuals, it can estimate the mean value $\textstyle { \frac { 1 } { n } } \sum _ { i = 1 } ^ { n } v _ { i } ^ { * }$ . Note that the noise injected into $t _ { i } ^ { * }$ has a mean value of 0, so this estimate $t _ { i } ^ { * }$ is unbiased. For any two input $v _ { 1 } , \ v _ { 2 } .$ , the noise generated by the Laplace mechanism is x1 and x2, respectively. pdf(x1)pdf(x2) $x _ { 1 }$ $x _ { 2 }$ $\begin{array} { r } { \frac { p d f ( x _ { 1 } ) } { p d f ( x _ { 2 } ) } \doteq } \end{array}$ $\begin{array} { r } { e x p ( \frac { | x _ { 2 } | - | x _ { 1 } | } { \lambda } ) = e x p ( \frac { \Delta } { \lambda } ) } \end{array}$ , let $\begin{array} { r } { \frac { \Delta } { \lambda } = \epsilon , } \end{array}$ , so it satisfies the --LDP. In addition, the variance in $t _ { i } ^ { * }$ is $\begin{array} { r } { \int _ { - \infty } ^ { + \infty } x ^ { 2 } p d f ( x ) d x = \frac { 8 } { \epsilon ^ { 2 } } } \end{array}$ .

Since the range of the injected noise x is infinite, the Laplace mechanism is put into the category of inject an infinite range of noise. For the same reason, Geng et al. [4] propose Staircase Mechanism, which can replace the Laplace mechanism. They show the staircase mechanism is the optimal noise adding mechanism in a universal context. Specifically, given $r \in [ 0 , 1 ]$ , define the noise distribution of the staircase shape with probability density function $p d f _ { r } ( x )$ defined as

$$
p d f _ {r} (x) = \left\{ \begin{array}{l l} e ^ {- k \epsilon} a (r) & | x | \in [ k \Delta , (k + r) \Delta) \\ e ^ {- (k + 1) \epsilon} a (r) & | x | \in [ (k + r) \Delta , (k + 1) \Delta) \end{array} \right. \tag {8}
$$

for $k \in \mathbb N$ , where $\Delta = 2 , a ( r )$ is the normalization factor to make $\begin{array} { r } { \int _ { - \infty } ^ { + \infty } p d f _ { r } ( x ) d x = 1 } \end{array}$ . Then the expression for $a ( r )$ is $\begin{array} { r } { a ( r ) \ = \ \frac { 1 - e ^ { - \epsilon } } { 4 \Delta ( r + e ^ { - \epsilon } ( 1 - r ) ) } } \end{array}$ . To minimize the expectation of amplitude, they have cost function $\mathcal { L } ( x ) = | x |$ . For a given probability distribution ${ \mathcal P } ,$ define $\begin{array} { r } { V ( \mathcal { P } ) = \int _ { x \in \mathbb { R } } \mathcal { L } ( x ) \mathcal { P } ( d x ) } \end{array}$ . ∈To minimize the expectation the amplitude of noise, the distribution has probability density function with $\begin{array} { r } { r ^ { * } = \frac { 1 } { 1 + e ^ { \frac { \epsilon } { 2 } } } . } \end{array}$ 1 +e -2 .

Map to two outputs that belongs to a bounded field. Duchi et al. [5] propose a method to perturb multidimensional numeric data. Specifically, give an individual data $v _ { i } \in [ - 1 , 1 ]$ , output $\begin{array} { r } { v _ { i } ^ { * } \ = \ \mathrm { \hat { A } } _ { 1 } \ = \ \frac { e ^ { \bar { \epsilon } } + \bar { 1 } } { e ^ { \epsilon } - 1 } } \end{array}$ and $\begin{array} { r } { v _ { i } ^ { * } ~ = ~ A _ { 2 } ~ = ~ - { \frac { e ^ { \epsilon } + \mathrm { \bar { 1 } } } { e ^ { \epsilon } - 1 } } } \end{array}$ with probability $\begin{array} { r } { P _ { 1 } = \frac { e ^ { \epsilon } - 1 } { 2 e ^ { \epsilon } + 2 } \cdot v _ { i } + \frac { 1 } { 2 } } \end{array}$ 2e-+2 and $\begin{array} { r } { P _ { 2 } = - \frac { e ^ { \epsilon } - 1 } { 2 e ^ { \epsilon } + 2 } \cdot v _ { i } + \frac { 1 } { 2 } } \end{array}$ e- 1 · vi + 12 , respectively. Once the aggregator has collected all the perturbation results uploaded by individuals, it can estimate the mean value 1 n $\textstyle { \frac { 1 } { n } } \sum _ { i = 1 } ^ { n } v _ { i } ^ { * }$ . Duchi et al. prove the $v _ { i } ^ { * }$ is an unbiased estimator. In addition, the variance of $v _ { i } ^ { * }$ is:

$$
\begin{array}{l} V a r [ v _ {i} ^ {*} ] = \mathbb {E} [ (v _ {i} ^ {*}) ^ {2} ] - (\mathbb {E} [ v _ {i} ^ {*} ]) ^ {2} \\ = \left(A _ {1}\right) ^ {2} \cdot P _ {1} + \left(A _ {2}\right) ^ {2} \cdot P _ {2} - v _ {i} ^ {2} \tag {9} \\ = (\frac {e ^ {\epsilon} + 1}{e ^ {\epsilon} - 1}) ^ {2} - v _ {i} ^ {2} \\ \end{array}
$$

Nguyen et al. [6] propose ˆ Harmony that map to two outputs that belongs to a finite field. The key idea of Harmony is to discretize a numerical value to a binary one and then perturb it using random response to satisfy --LDP. Specifically, given a individual data $v _ { i } \in [ - 1 , 1 ]$ , which is discretized to $v _ { i } ^ { \prime } =$ $1 \ \mathrm { o r \mathrm { ~ - 1 ~ } }$ with with probability $\begin{array} { r } { P _ { 1 } = \frac { 1 + v _ { i } } { 2 } } \end{array}$ or $\begin{array} { r } { { P _ { 2 } } \ = \ \frac { 1 - v _ { i } } { 2 } } \end{array}$ , 2 respectively. Then process $\boldsymbol { v } _ { i } ^ { \prime }$ by using random response, to keep $\boldsymbol { v } _ { i } ^ { \prime }$ the same or to flip it with probability $\begin{array} { r } { Q _ { 1 } = \frac { e ^ { \epsilon } } { 1 + e ^ { \epsilon } } } \end{array}$ e- or $\begin{array} { r } { Q _ { 2 } = \frac { 1 } { 1 + e ^ { \epsilon } } } \end{array}$ , respectively. The probability ratio of giving two different inputs $v _ { 1 }$ , v2 with the same output 1 is:

$$
\begin{array}{l} \frac {\operatorname * {P r} \left[ v _ {i} ^ {*} = 1 \mid v _ {i} = v _ {1} \right]}{\operatorname * {P r} \left[ v _ {i} ^ {*} = 1 \mid v _ {i} = v _ {2} \right]} = \frac {P _ {1} (v _ {1}) \cdot Q _ {1} (v _ {1}) + P _ {2} (v _ {1}) \cdot Q _ {2} (v _ {1})}{P _ {1} (v _ {2}) \cdot Q _ {1} (v _ {2}) + P _ {2} (v _ {2}) \cdot Q _ {2} (v _ {2})} \\ = \frac {e ^ {\epsilon} + 1 + v _ {1} (e ^ {\epsilon} - 1)}{e ^ {\epsilon} + 1 + v _ {2} (e ^ {\epsilon} - 1)} \\ \leq e ^ {\epsilon} \tag {10} \\ \end{array}
$$

we prove that the Harmont satisfy --LDP. In addition, the expectation of v∗i is vi $v _ { i } ^ { * }$ $v _ { i } \cdot \frac { e ^ { \epsilon } - 1 } { e ^ { \epsilon } + 1 }$ · e-−1e-+1 . We want to measure the dispersion between the random variable and the original mean, and different from the method mentioned above, the variance of the Harmony doesn’t express that, so we changed the expression for the variance $\begin{array} { r } { \dot { V a r ^ { * } } = ( \mathbb E ( v _ { i } ^ { * } ) - v _ { i } ) ^ { 2 } = \bar { 1 } + v _ { i } ^ { 2 } \cdot \frac { 3 - \hat { e } ^ { \epsilon } } { 1 + e ^ { \epsilon } } } \end{array}$ 1+e- .

Maps to an output that belongs to a bounded field. Ning Wang et al. [7] propose Piecewice Mechanism (PM) for collecting a numeric attribute. PM takes as input a value $v _ { i } ~ \in ~ [ - 1 , 1 ]$ , and output a perturbed value $v _ { i } ^ { * } \in [ - C , C ]$ . The probability density function of $v _ { i } ^ { * }$ is a piecewise constant function as follows:

$$
p d f (v _ {i} ^ {*} | v _ {i}) = \left\{ \begin{array}{l l} p & v _ {i} ^ {*} \in [ l (v _ {i}), r (v _ {i}) ], \\ \frac {p}{e ^ {\epsilon}} & v _ {i} ^ {*} \in [ - C, l (v _ {i})) \cup (r (v _ {i}), C ] \end{array} \right. \tag {11}
$$

where $\begin{array} { r } { l ( v _ { i } ) = \frac { C + 1 } { 2 } \cdot v _ { i } - \frac { C - 1 } { 2 } } \end{array}$ C+1 vi 2 and $r ( v _ { i } ) = l ( v _ { i } ) + C - 1$ . Specifically, when $v _ { i } = 1 , l ( v _ { i } ) = 1$ and $r ( v _ { i } ) = C .$ . From the area of probability density function is 1, we can get: $p ( C { - } 1 ) +$ $\begin{array} { r } { \frac { p } { e ^ { \epsilon } } ( C + 1 ) = 1 } \end{array}$ . One of the better properties is $\mathbb { E } ( v _ { i } ^ { * } ) = v _ { i }$ , we can get $\begin{array} { r } { ( C + 1 ) \frac { P } { e ^ { \epsilon } } \cdot \frac { 1 - C } { 2 } + ( C - 1 ) \mathbf { \hat { \boldsymbol { p } } } \cdot \frac { \hat { \mathbf { 1 } } + C } { 2 } = 1 } \end{array}$ . By considering the two formulas, comput $\begin{array} { r } { C = \frac { e ^ { \epsilon / 2 } + 1 } { e ^ { \epsilon / 2 } - 1 } } \end{array}$ e-/2 1 and $\begin{array} { r } { p = \frac { e ^ { \epsilon } - e ^ { \epsilon / 2 } } { 2 e ^ { \epsilon / 2 } + 2 } } \end{array}$ finally. Furthermore,

$$
\begin{array}{l} V a r [ v _ {i} ^ {*} ] = E [ (v _ {i} ^ {*}) ^ {2} ] - (E [ v _ {i} ^ {*} ]) ^ {2} \\ = \int_ {- C} ^ {l (v _ {i})} v _ {i} ^ {2} \frac {p}{e ^ {\epsilon}} d x + \int_ {l (v _ {i})} ^ {r (v _ {i})} p v _ {i} ^ {2} d x - v _ {i} ^ {2} + \int_ {r (v _ {i})} ^ {C} v _ {i} ^ {2} \frac {p}{e ^ {\epsilon}} d x \\ = \frac {e ^ {\epsilon / 2} + 3}{3 \left(e ^ {\epsilon / 2} - 1\right) ^ {2}} + \frac {v _ {i} ^ {2}}{e ^ {\epsilon / 2 - 1}} \tag {12} \\ \end{array}
$$

A combination of a specific encoding scheme and Random Response for distance prediction. The Bit Vectors (BV) [11] is supported by a theoretical foundation for encoding numerical values into an anonymization space. Initializes an s-length vector B for each input data v, the interval length t and the s random numbers from [l, r] are defined in detail. If the input v belongs to $[ r _ { i } - t , r _ { i } + t ]$ , the i-th bit will be set to 1, otherwise it remains unchanged. And after each of these bits have been processed this way, we get an updated B. Two inputs $v _ { 1 } , v _ { 2 }$ are processed to obtain $B _ { 1 } , B _ { 2 } ,$ , correspondingly. The relationship between the original $v _ { 1 } , v _ { 2 }$ can be estimated $\begin{array} { r } { | v _ { 1 } - v _ { 2 } | = \frac { d _ { H } * \bar { u } } { 2 s } } \end{array}$ with $| v _ { 1 } - v _ { 2 } | < 2 t$ , where $d _ { H }$ is the hamming distance between $B _ { 1 } , B _ { 2 }$ . The Randomized Bit Vector [10] added RR treatment for each bit of B on the basis of BV. Given Hamming distance $d _ { H }$ between embedded vector, the Euclidean distance between numerical values vales v1, v2 can be estimated by $\begin{array} { r } { d _ { E } ( v _ { 1 } , v _ { 2 } ) = \frac { u } { 2 s } \cdot ( \frac { e ^ { \epsilon } + 1 } { e ^ { \epsilon } - 1 } ) ^ { 2 } \cdot d _ { H } - \frac { u \dot { e } ^ { \epsilon } } { ( e ^ { \epsilon } - 1 ) ^ { 2 } } } \end{array}$ ue- .

# V. PRIVACY PRESERVING INVENTORY FORECAST

Non-privacy-preserving inventory forecasting framework RAP [12] first merges the user UV attributes, such as location, age, gender and other UV attributes. Such combinations are finite and easy to be implemented in engineering. After counting the number of users per day under each UV combination, the deep learning model can be used to estimate the number of users. PV dimension is used to classify the users under each combination. PV content dimension is chosen because the content dimension can reflect the user’s personal preference, and the variation of this preference is not large. For example, users whose exposure is concentrated in cartoon dimension can be considered to prefer cartoons in the future. Secondly, the content dimension of each user is constructed as a vector, and then unsupervised clustering is performed for all users over a period of time. At last, after obtaining the number of users and the proportion of each category of users under the combination, sampling can be conducted in the sampling pool to obtain the final estimated data.

![](images/9b949fc540e2d5c03a0ea51b8cbf7ff6b8148c266d79ecea59e55003f811dc67.jpg)



Fig. 3: System overview of PPIF

Algorithm 1: Privacy-Preserving Inventory Forecasting.   
input : History Log $< u_i, UV_i, RPM(PV_i, \epsilon_i), T>$ .
output: Future population structure $D'^M$ .

1 Estimate the future total population based on the historical UV information $P^M(UV)$ ;
2 Clustering users according to historical PV information:
for each $\epsilon_j$ do
3 Determine the number of cluster iterations $I_{\epsilon_j}$ ;
4 Initialize the clustering center $C_{\epsilon_j}$ using $C_{\epsilon_{j-1}}$ ;
5 Update $C_{\epsilon_j}$ ;
6 Get user categories using clustering model $< u_i, K_c>$ ;
7 Estimate the future distribution based on historical population categories $P^M(K_c|UV)$ ;
8 Samples from the historical user pool according to $P^M(K_c|UV) \times P^M(UV)$ ;
9 return $D'^M$

Fig. 3 is PPIF Framework overview. Alg. 1 describes the pseudo-code of PPIF. In PPIF, instead of uploading the real PV data to the server, the user uploads the perturbed PV data. The basic method of LDP introduced in Section IV is to process one-dimensional attributes, but PV data is a multi-dimensional attribute vector in reality. By the composition theorem [13], if $\epsilon _ { i }$ remains the same, the $\epsilon _ { i d }$ allocated to each dimension will decrease as the number of dimensions increases. If the calculation task of the scene is only sum or mean calculation, some dimensions can be randomly selected for LDP processing and uploaded, so that $\epsilon _ { i d }$ will be larger, and the result of the total sum or mean will be more accurate than the method of equalization. But instead of simply summing up in our PPIF scenario, we sample and sum by category. Uploading part of the dimensions sampled will seriously affect the clustering effect and further destroy the final summation result, so we adopt the equalization method in the PPIF scene.

The tensor D can be obtained by the server sorting the log file. As the magnitude of users is hundreds of millions, it is difficult to predict tensor D directly in engineering, but the problem can be simplified by the tensor decomposition. The server can count the number of historical users through all

the UV information. The perturbation of PV will not affect the prediction of the total number of future users, and the accurate tensor A can be obtained. The focus of our work is on the influence of LDP on clustering and summation, so there is little discussion on the use of deep learning for prediction in the algorithm. LDP achieves the purpose that the server cannot distinguish different users from UV by perturbing the PV data. However, forcing clustering on the perturbing data is contrary to the purpose of LDP, which is the main source of error. Optimization is needed to minimize error.

Each user values privacy differently, so the server collects user data processed by different privacy parameters $\epsilon _ { i } ,$ and gives priority to the data with high availability to get the coldboot clustering center $C _ { c d } .$ It guides the initialization direction of clustering for data with poor availability, which can reduce the number of iterations. In addition, as the center of the cluster, the mean value of the LDP is also used to reduce the error. The perturbed data will be output near the input value with a high probability in many LDP methods. Similarly, we use soft clustering to cluster users, which is different from the hard clustering scenario in which each user belongs to a unique category. Soft clustering outputs the probability of each user belonging to each category, corresponding tensor C, which conforms to the characteristics of LDP probability. We can estimate the future distribution based on historical population categories, which is the tensor B. Combined with the category proportion and the total number of users, the user groups that meet the conditions are sampled from the constructed user pool. This user group is final estimate of the future user structure, from which we can clearly understand the user’s UV and PV information, which can support other finegrained advertising operations. At this point, users’ privacy is protected by the LDP to the extent of -i, and the server builds a future user inventory structure based on the perturbed data.

# VI. EXPERIMENTS

We implement the proposed mechanisms and evaluate them on simulated synthetic and real datasets. In all the experiments, we run the test 100 times and report average results. Normalize all data to [ 1, 1]. Simulated datasets contains 1M tuples and 2 attributes. Each attribute value is generated from a Gaussian distribution and each tuple corresponds to a label representing the ordinal number of the cluster. The real dataset is extracted from the Tencent Advertising Algorithm Competition (TAAC), which contains 1396k user UV data, user behavior PV data and 735k advertising information. The dataset has no business meaning after desensitization. Firstly, we assume inventory orientation, so as to filter the user groups that meet the conditions. Secondly, the number of active users in a specific day is counted as the estimated number of users, and the total PV is regarded as the ground truth. The category distribution of the day is obtained by direct clustering under non-private scenes as the predicted distribution. After processing with different LDP methods and clustering, the sampling pool composed of the user groups of the previous three days was sampled and summed according to the distribution to compare with the real situation. All users with gender 2 and education level 5 were selected for the experiment to estimate the future inventory capacity of commodity type 1. The log from February 17 to 19, 2019 is selected as the historical sampling pool, and the future date to be estimated is February 20, 2019. When the number of clustering centers is 8, the clustering centers are relatively stable. LDP belongs to distributed computing in the real scenario. We process datasets uniformly to simulate the process of collecting user data, and the space-time cost does not need to be calculated. MAE and ARI were used to measure data availability and clustering, respectively. The experimental results illustrate the advantages of RPM method in the cluster-sample-summation task from the clustering effect and the overall effect respectively.

![](images/08a18518f83b7cb153339092c5ef8ce64b870fb257e407d1f268a0bd64b942b3.jpg)  
(a) Original

![](images/a836d44b92657a3864a309b949c12336e830d7ef6759af057a6cdd75c9876f97.jpg)  
(b) Laplace

![](images/ba2389c67f8d91dfec15a865ca325ccf7f4506ff3419481057b0381571c9aef1.jpg)  
(c) Staircase

![](images/9a68f1ea3a16041924813c88049ec66541693c97b64c516fecc5fdeeae36e8ba.jpg)  
(d) Harmony

![](images/fccf8f5bde23e287223f45f096ed084bd69fbcd0d4ad8844d1d3e302d2e2f22b.jpg)  
(e) Duchi

![](images/a34bdf304862cd9a6f2024c026564a9d7bfd8576a4ea10a154ca7104912f3004.jpg)  
(f) PM

![](images/cd333ae7c54b5835c0aab9b53c4c41ae5697872c3cdd177adb25601bf5f6c79e.jpg)  
(g) RPM   
Fig. 4: Density and distribution of 2d data in three classifications after LDP processing.

Mean Absolute Error (MAE) measures the overall absolute error between each methods outputs and the ground-truths, which is computed by averaging the absolute difference over all the entities. MAE was used in this work to measure data availability. MAE is calculated as: MAE = -ni=1|yi−xi|n . $\begin{array} { r } { \mathrm { M A E } = \frac { \sum _ { i = 1 } ^ { n } \left| y _ { i } - x _ { i } \right| } { n } } \end{array}$ n

Adjusted Rand Index (ARI) [14] is the corrected-for-chance version of the Rand index. ARI computes a similarity measure between two clusterings. When the ARI is close to 1, it means that the clustering effect is close to the real result, and when it is close to 0, it means random clustering. The original Adjusted Rand Index using the Permutation Model is: ARI = (RI $E x p e c t e d _ { R I } ) / ( m a x ( R I ) - E x p e c t e d _ { R I } )$ .

# A. Results on Summation

Fig. 5(b) demonstrates that in a separate summation calculation without clustering and sampling, the RPM method performs poorly when - is small, as the variance description shown in Fig. 5(a). The Laplace method leads to similar performance as Staircase method, and we ignored its results in subsequent experiments. The advantage of RPM does not lie in summation calculation. Subsequent experiments will illustrate the importance of clustering and make it perform well in the whole calculation task.

![](images/da3a245309fe704d387e5f10472ad30b323af73301f0e7324240f11e57cd3399.jpg)  
(a)

![](images/3f4a1f1d762da8ccc12f08c24968ba3ea9c62ef7a3f845fd2ba0785b80619932.jpg)



(b)   
Fig. 5: (a) Different approaches’ worst-case noise variances for versus the -. (b) The result accuracy for sum estimation.

![](images/fbfd010fbfc1bde140f7b900013e1d92b47f27b1a9b22268dfab79153e7ae7c5.jpg)



(a)

![](images/9cd113a72bd41ef64db61bda7514c81b552193829b9243f31a5e403ca95fe803.jpg)



(b)   
Fig. 6: (a) Different approaches’ ARI for versus the - on simulated dataset. (b) Different approaches’ ARI for versus the - on TAAC dataset.

# B. Results on Unsupervised Clustering

Fig. 4 illustrates the density and distribution of the 2- dimensional 3 classification data after LDP processing. It is obvious that Harmony and Duchi, two approaches with excellent performance in separate summation computing tasks, can not be applied to clustering tasks at all. These two methods offer inferior clustering results. Because each user is required to maintain a uniform sequence of random vertor, Randomized BV cannot be used in the actual scene. Fig. 6 shows the clustering effect of different methods on simulated dataset and TAAC dataset respectively. In the simulated dataset, it can be seen that when - is greater than 5.5, RPM method has the best performance among all methods. The reason why ARI on TAAC dataset is inferior to simulated dataset is that the number of dimensions of TAAC user data is much more than that of simulated data, and the total privacy budget of users is larger than that of users in simulated dataset. The clustering effect of RPM flat is equal to random clustering under any privacy budget, which means it has a deeper privacy protection effect. RPM flat can still be deployed to individual summation tasks, but it is not applicable to PPIF scenario that require high clustering results. The Laplace algorithm has similar summation performance to Staircase, but not as remarkable clustering performance as Staircase algorithm. We omit their results for brevity.

![](images/35e2b8d4e193058d6fa1f41a51307eaf687012e9a18b0ea3b8f8b5e51e37123d.jpg)



(a)

![](images/43a54bab7362705a3727e309ee379fa3c6dbca2743c7b1ae02f1cfddf3a7cdfb.jpg)



(b)   
Fig. 7: (a) Different approaches’ MAE for versus the - on simulated dataset. (b) Different approaches’ MAE for versus the - on TAAC dataset.

# C. Results on Inventory Forecast

Our goal is to obtain the future total inventory. Fig. 7 shows the overall effect of different methods on simulated dataset and TAAC dataset respectively. Since there is no real user category label in the TAAC dataset, the MAE in the non-private case is not close to 0. Fig. 7(b) only represents the estimated inventory of commodity type 1 for the population of gender 2 and education level 5 on February 20, 2019. Because we get a specific user structure from the sample pool, we can easily get inventory estimates for other commodity types, which is the fine-grained nature of the RAP. RPM performed better than other methods when - is larger. In practical scenarios, PM or RPM can be reasonably selected under different - conditions to obtain the global optimal effect.

# VII. CONCLUSION

In this work, we systematically propose RPM for the task of calculating inventory forecasting in the advertising business, and combine clustering and sampling to achieve a user-granular inventory estimation framework. In future work, there are more complex computing tasks that need to be supported by LDP, while meeting the requirements of users and server. The optimality of the LDP also needs to be explored. We plan to design (-, δ)-LDP method based the clustering summation computing task, which may provide higher records availability.

# ACKNOWLEDGMENTS

The research is supported by National Key R&D Program of China 2017YFB1003003, National Natural Science Foundation of China with No. 61822209, No. 61932016, No.61625205, No. 61520106007, and Tencent Holdings Ltd.

# REFERENCES

[1] X. Ma, L. Zhang, L. Xu, Z. Liu, G. Chen, Z. Xiao, Y. Wang, and Z. Wu, “Large-scale user visits understanding and forecasting with deep spatial-temporal tensor factorization framework,” in Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, KDD 2019, Anchorage, AK, USA, August 4-8, 2019, A. Teredesai, V. Kumar, Y. Li, R. Rosales, E. Terzi, and G. Karypis, Eds. ACM, 2019, pp. 2403–2411. [Online]. Available: https://doi.org/10.1145/3292500.3330728   
[2] S. L. Warner, “Randomized response: A survey technique for eliminating evasive answer bias,” Journal of the American Statistical Association, vol. 60, no. 309, pp. 63–66, 1965.   
[3] C. Dwork, F. McSherry, K. Nissim, and A. Smith, “Calibrating noise to sensitivity in private data analysis,” in Theory of Cryptography, S. Halevi and T. Rabin, Eds. Berlin, Heidelberg: Springer Berlin Heidelberg, 2006, pp. 265–284.   
[4] Q. Geng, P. Kairouz, S. Oh, and P. Viswanath, “The staircase mechanism in differential privacy,” J. Sel. Topics Signal Processing, vol. 9, no. 7, pp. 1176–1184, 2015. [Online]. Available: https://doi.org/10.1109/JSTSP.2015.2425831   
[5] J. C. Duchi, M. J. Wainwright, and M. I. Jordan, “Minimax optimal procedures for locally private estimation,” CoRR, vol. abs/1604.02390, 2016. [Online]. Available: http://arxiv.org/abs/1604.02390   
[6] T. T. Nguyen, X. Xiao, Y. Yang, S. C. Hui, H. Shin, and J. Shin, ˆ “Collecting and analyzing data from smart device users with local differential privacy,” CoRR, vol. abs/1606.05053, 2016. [Online]. Available: http://arxiv.org/abs/1606.05053   
[7] N. Wang, X. Xiao, Y. Yang, J. Zhao, S. C. Hui, H. Shin, J. Shin, and G. Yu, “Collecting and analyzing multidimensional data with local differential privacy,” in 35th IEEE International Conference on Data Engineering, ICDE 2019, Macao, China, April 8-11, 2019. IEEE, 2019, pp. 638–649. [Online]. Available: https://doi.org/10.1109/ICDE.2019.00063   
[8] Y. Zhao, J. Zhao, M. Yang, T. Wang, N. Wang, L. Lyu, D. Niyato, and K. Lam, “Local differential privacy based federated learning for internet of things,” CoRR, vol. abs/2004.08856, 2020. [Online]. Available: https://arxiv.org/abs/2004.08856   
[9] Q. Ye, H. Hu, X. Meng, and H. Zheng, “Privkv: Key-value data collection with local differential privacy,” in 2019 IEEE Symposium on Security and Privacy, SP 2019, San Francisco, CA, USA, May 19-23, 2019. IEEE, 2019, pp. 317–331. [Online]. Available: https://doi.org/10.1109/SP.2019.00018   
[10] L. Sun, L. Zhang, and X. Ye, “Randomized bit vector: Privacypreserving encoding mechanism,” in Proceedings of the 27th ACM International Conference on Information and Knowledge Management, ser. CIKM 18. New York, NY, USA: Association for Computing Machinery, 2018, p. 12631272. [Online]. Available: https://doi.org/10.1145/3269206.3271703   
[11] D. Karapiperis, A. Gkoulalas-Divanis, and V. S. Verykios, “Distance-aware encoding of numerical values for privacy-preserving record linkage,” in 33rd IEEE International Conference on Data Engineering, ICDE 2017, San Diego, CA, USA, April 19-22, 2017. IEEE Computer Society, 2017, pp. 135–138. [Online]. Available: https://doi.org/10.1109/ICDE.2017.58   
[12] H. Zhang, L. Zhang, L. Xu, X. Ma, Z. Wu, C. Tang, W. Xu, and Y. Yang, “A request-level guaranteed delivery advertising planning: Forecasting and allocation,” in KDD ’20: The 26th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, Virtual Event, CA, USA, August 23-27, 2020, R. Gupta, Y. Liu, J. Tang, and B. A. Prakash, Eds. ACM, 2020, pp. 2980–2988. [Online]. Available: https://dl.acm.org/doi/10.1145/3394486.3403348   
[13] C. Dwork and A. Roth, “The algorithmic foundations of differential privacy,” Foundations and Trends in Theoretical Computer Science, vol. 9, no. 3-4, pp. 211–407, 2014. [Online]. Available: https://doi.org/10.1561/0400000042   
[14] W. M. Rand, “Objective criteria for the evaluation of clustering methods,” Journal of the American Statistical Association, vol. 66, no. 336, pp. 846–850, 1971. [Online]. Available: https://www.tandfonline.com/doi/abs/10.1080/01621459.1971.10482356