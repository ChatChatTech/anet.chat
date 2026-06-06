# QUIDS: Quality-informed Incentive-driven Multi-agent Dispatching System for Mobile Crowdsensing

Nan Zhou, Zuxin Li, Fanhang Man, Xuecheng Chen, Susu Xu, Fan Dang, Chaopeng Hong, Yunhao Liu, Fellow, IEEE, Xiao-Ping Zhang, Fellow, IEEE, Xinlei Chen, Member, IEEE

Abstract—This paper addresses the challenges of achieving optimal Quality of Information (QoI) in non-dedicated vehicular mobile crowdsensing (NVMCS) system, where vehicles not originally designed for sensing are leveraged to collect realtime data as they traverse urban environments. These challenges are exacerbated by the interrelated issues of sensing coverage, sensing reliability, and the inherently dynamic nature of participating vehicles. To tackle these challenges, we propose QUIDS, a QUality-informed Incentive-driven multi-agent Dispatching System, which ensures high sensing coverage and sensing reliability under budget constraints in NVMCS systems. QUIDS improves QoI by introducing a novel metric, Aggregated Sensing Quality (ASQ), designed to quantitatively capture the concept of QoI by integrating both sensing coverage and sensing reliability. Moreover, we develop a Mutually Assisted Belief-aware Vehicle Dispatching algorithm that estimates sensing reliability and allocates monetary incentives under uncertain vehicle conditions, thereby further improving ASQ. Evaluation using real-world data collected from a deployed NVMCS system in a metropolitan area demonstrates the effectiveness of QUIDS. The ASQ metric shows a 38% improvement over non-dispatching scenarios and a 10% enhancement over state-of-the-art methods. Additionally, QUIDS reduces reconstruction map errors by 39–74% across various reconstruction algorithms, validating its efficacy in improving QoI within NVMCS systems. Addressing the often-overlooked issue of sensing reliability in existing studies, the QUIDS system leverages non-dedicated vehicles and incorporates a qualityinformed incentive-driven dispatching system to jointly optimize sensing coverage and sensing reliability. This enables low-cost, high-quality, and scalable urban environmental monitoring without the need for dedicated sensing infrastructure, and makes the

This paper was supported by Yunnan Forestry and Grassland Science and Technology Innovation Joint Special Project (grant NO. 202404CB090017), the Natural Science Foundation of China under Grant 62371269, National Key R&D program of China (2022YFC3300703), Guangdong Innovative and Entrepreneurial Research Team Program (2021ZT09L197), and Tsinghua Shenzhen International Graduate School Cross-disciplinary Research and Innovation Fund Research Plan (JC20220011) and Meituan Academy of Robotics Shenzhen.

A preliminary version of this article appeared in IEEE International Conference on Computer Communications (IEEE INFOCOM 2024) [1]

Nan Zhou, Zuxin Li, Fanhang Man, Xuecheng Chen are with Shenzhen International Graduate School, Tsinghua University, China. E-mail: {zhoun24, lizx21, mfh21, chenxc21}@mails.tsinghua.edu.cn

Susu Xv is with Department of Civil and System Engineering, Johns Hopkins University, United States of America. E-mail: sxu83@jhu.edu

Fan Dang and Yunhao Liu are with the School of Software and BNRist, Tsinghua University, Beijing 100084, China. Email: dangfan@tsinghua.edu.cn, yunhao@greenorbs.com

Chaopeng Hong and Xiao-Ping Zhang is with Shenzhen International Graduate School, Tsinghua University, Shenzhen, China. E-mail: {hongco, xiaoping.zhang}@sz.tsinghua.edu.cn

Xinlei Chen is with the Shenzhen International Graduate School, Tsinghua University, China. Email: chen.xinlei@sz.tsinghua.edu.cn

Nan Zhou and Zuxin Li are co-primary authors.

Corresponding authors: Xinlei Chen.

Manuscript submitted April 2025.

system applicable to diverse smart-city scenarios such as traffic monitoring and environmental sensing.

Index Terms—Internet of Things; Mobile sensing and applications; Mobile Crowdsensing; Monetary incentive

# I. INTRODUCTION

N ON-dedicated vehicular mobile crowdsensing (NVMCS)systems have emerged as a promising paradigm for systems have emerged as a promising paradigm for collecting large volumes of spatio-temporal data [2]. Nondedicated vehicular sensing platforms, such as taxis, delivery drones [3], [4], and ride-sharing vehicles like Uber and Lyft, can collect data while navigating urban environments, offering cost-effective and easily maintainable solutions for NVMCS. By harnessing the collective sensing capabilities of these non-dedicated vehicles, NVMCS system supports a wide range of applications that enhance human life and inform decision-making processes, including public infrastructure management [5], traffic monitoring [6], and public policy formulation [7].

One of the key challenges in NVMCS systems is ensuring optimal Quality of Information (QoI), which depends on both sensing coverage and sensing reliability. Sensing coverage refers to the spatial and temporal extent of data collection, while sensing reliability pertains to the accuracy and consistency of sensor measurements. However, non-dedicated vehicles, which prioritize fulfilling ride requests, often tend to concentrate in high-demand areas, leading to reduced sensing coverage in less populated or remote regions. In contrast, an effective NVMCS system typically requires comprehensive, city-wide data sampling to ensure sufficient spatio-temporal granularity for meaningful analysis. This imbalance in the spatial distribution of sensing resources diminishes overall sensing coverage, thereby undermining QoI. A seemingly straightforward solution is to dispatch vehicles to underserved areas, where sensing coverage is inadequate. However, this approach may result in a reduction in drivers’ earnings, as these areas typically experience fewer ride requests. Consequently, drivers may be reluctant to accept the proposed dispatch assignments, as they would be economically disadvantaged. To mitigate this issue, it is necessary to provide additional compensatory incentives that align the drivers’ economic motivations with the objectives of the sensing system. Moreover, the sensors deployed on non-dedicated vehicles are inherently subject to various sources of uncertainty, which can introduce significant fluctuations in sensor readings. These fluctuations arise from multiple factors, including measurement inaccuracies, sensor degradation over time, and the absence of routine calibration. Such uncertainties can severely compromise the reliability and accuracy of the sensor data, which is critical for the overall performance of the NVMCS system.

In addition, the interplay between sensing coverage and sensing reliability often leads to a trade-off. Specifically, evenly distributing sensors across the sensing area can improve coverage; however, this may reduce the number of sensors in each sub-region, thereby increasing measurement uncertainties and diminishing reliability. Conversely, concentrating sensors in specific regions can enhance reliability by generating more data points, but this approach compromises coverage in other areas, resulting in data gaps and reduced spatial resolution. This inherent trade-off between sensing coverage and sensing reliability presents significant challenges in achieving a balanced QoI, particularly in dynamic environments where sensor reliability is variable. These complexities further exacerbate the difficulty of ensuring high-quality data collection.

Existing solutions have made significant strides in enhancing the QoI in NVMCS systems. These solutions can be broadly categorized into two main approaches: (1) Improving sensing coverage through vehicle dispatching, which includes various dispatching strategies such as dynamic programming [8] [9], and reinforcement learning [10]. However, these methods optimize only for sensing coverage and assume near-perfect sensor reliability. In reality, sensor reliability often exhibits significant uncertainty due to environmental interference and operational fluctuations. Neglecting sensing reliability may lead to unreliable data and misleading information. (2) Ensuring the sensing reliability of individual sensors, which focuses on improving sensor reliability using external references [11] or machine learning interpolation techniques [12] to enhance the performance of low-cost sensors. While these approaches are effective under certain conditions, they frequently assume the availability of specific sensor types or external calibration references, which can limit their applicability or make them prohibitively expensive in many real-world scenarios [13]. Moreover, they often fail to account for the monetary incentives required for vehicle dispatching, a crucial factor in ensuring the feasibility of the dispatching plan, especially considering the limited budgets typically available in practical applications.

The challenges of ensuring QoI in NVMCS systems can be summarized as follows: (C1) The inherent trade-off between sensing coverage and sensing reliability. As discussed earlier, achieving an optimal balance between these two factors is critical; however, they often conflict, making simultaneous optimization difficult. (C2) The difficulty of accurately estimating the sensing reliability of individual sensors. The continuous movement and varying locations of sensors, along with sensor drift and other uncertainties, complicate the assessment of the accuracy and consistency of their measurements. (C3) The customization of an effective monetary incentive strategy. Limited incentive budgets and the willingness of vehicles to accept tasks under these financial constraints make the design of efficient incentive schemes particularly challenging. Therefore, in vehicle dispatching scenarios with constrained budgets, optimizing both sensing coverage and sensing reliability becomes increasingly complex and dynamic, thus hindering the improvement of QoI.

To address these challenges, we propose QUIDS, a QUalityinformed Incentive-driven multi-agent Dispatching System, specifically designed to enable dynamic, sensing-driven dispatching for NVMCS tasks. Specifically: (S1) To tackle (C1): We introduce a novel metric, Aggregated Sensing Quality (ASQ), which effectively balances the trade-off between sensing coverage and sensing reliability. Building on the insight that the sensing reliability of multiple lower-quality sensors can be compensated by aggregating their readings, as outlined in [14], ASQ combines data from these sensors to produce a measure that approximates the performance of higher-quality sensors. (S2) To tackle (C2&C3): We propose a Mutually Assisted Belief-aware Vehicle Dispatching algorithm, grounded in the core principles of truth discovery, which integrates both sensing reliability and monetary incentives in guiding dispatch decisions. In this algorithm, the collaborative sensing reliability is derived from the aggregated data readings of multiple sensors, while monetary incentives are calculated based on ride requests originating from various destinations. Sensors and vehicles are mutually assisted by exchanging information and resources, thereby enhancing both the reliability of the collected data and the operational efficiency of the dispatch process. Moreover, the dispatch process itself influences both the inference of sensing reliability and the computation of incentives, promoting adaptive and optimized data collection that improves the overall QoI. To evaluate the performance of our system, we deployed a NVMCS system involving 29 taxis over a two-month period to collect fine-grained air pollution data. The results demonstrate the effectiveness and potential of QUIDS in achieving optimal QoI in NVMCS scenarios.

To summarize, the main contributions of this paper are as follows:

• Propose a novel metric named Aggregated Sensing Quality (ASQ) to jointly optimize the inherent trade-off between sensing coverage and sensing reliability, thereby enhancing the Quality of Information (QoI);   
• Design a Mutually Assisted Belief-Aware Vehicle Dispatching Algorithm that enhances ASQ through real-time inference of sensing reliability;   
• Design a Monetary Incentive Mechanism, which incorporates human behavioral uncertainties into the modeling framework by introducing differentiated incentives, thereby effectively expanding the feasible region and solution space of the optimization problem.

The remainder of this paper is organized as follows. In Section II, we formally define the coupled problem of sensing coverage and sensing reliability. Section III presents the proposed algorithmic framework in detail. In Section IV, we conduct a comprehensive performance evaluation of the proposed method. Section V discusses the generalizability and potential limitations of our approach. A review of related work is provided in Section VI. Finally, Section VII concludes the paper.

![](images/7cc48ff0f20435304bda8befe8e5a230ff21d16af1adbb8eb001522d17d46417.jpg)



(a) Deviations and variations of lowcost sensors by time.

![](images/7fd9c7f8f6329e740c0edec083c3ca9c7dd8c9106311091236f7db730e96d984.jpg)



(b) Data fusions for improving sensing reliability, reproduced from [14].   
Fig. 1. Motivations for QUIDS.

# II. SYSTEM MODEL & DEFINITION

We consider a NVMCS system that encounters challenges stemming from uneven sensing coverage and inconsistent sensing reliability. To address this issue, we present case studies (Section II-A), describe the system model and dispatching parameters (Section II-B), and detail how sensing reliability and sensing coverage are modeled as two key components of vehicular sensing performance (Section II-C), ultimately aiming to enhance QoI.

# A. Motivation Case Studies

In NVMCS systems, accurately measuring $O _ { 3 }$ levels is crucial for assessing air quality and identifying potential health risks. However, widely deployed low-cost $O _ { 3 }$ sensors often show substantial deviations from ground-truth measurements, as illustrated in Fig. 1(a). Such discrepancies compromise the reliability of the sensed data, thereby hindering informed decision-making. Furthermore, the lack of continuous calibration for sensors mounted on non-dedicated vehicles introduces additional uncertainty regarding the accuracy of their readings, further complicating the data collection process.

To address these challenges, we explore the potential of data fusion techniques to enhance sensing reliability by compensating for the limitations of low-quality sensors through increased sensor density. Prior research [14] has shown that data fusion can significantly reduce the relative expanded uncertainty among multiple sensors with substantial deviations, as illustrated in Fig. 1(b). Building on this insight, the present study adopts a multi-stage approach to improve the reliability of sensor measurements in scenarios where reference monitoring data is unavailable. First, time-lagged and rolling statistical features are extracted to capture the temporal dynamics of sensor signals. Then, a Random Forest-based feature importance algorithm is applied to identify and retain the most informative features, thereby reducing the influence of noise and redundancy. Finally, machine learning models are employed to perform data fusion and reconstruction across multiple sensors, enabling the integration of complementary information from heterogeneous sources. This methodological framework is designed to enhance the stability of individual sensor outputs, expand spatial coverage, and improve the overall representativeness of the environmental data.

![](images/2668530b9cdbdf98223ed7299a6fa50bd08fca4c80cdb32655386cf300b423e1.jpg)



Fig. 2. This figure illustrates how dispatching non-dedicated vehicular Mobile Crowdsensing (NVMCS) in uneven sensing reliability setups can improve Quality of Information (QoI) by making the coverage optimal.

# B. System Models

The proposed dispatching system aims to enhance the Quality of Information (QoI) by optimizing sensing coverage while ensuring sensing reliability. To this end, the platform selects optimal routes for taxis to improve the system’s sensing coverage (as illustrated in Fig. 2) and allocates financial incentives to drivers to promote acceptance of dispatch assignments. While many existing dispatching systems tend to overlook the importance of sensing reliability, integrating this factor constitutes a novel contribution of our approach. We argue that an optimized spatiotemporal distribution—characterized by both balanced sensing coverage and reliable sensor performance—provides an effective and scalable solution. This design offers valuable insights for a wide range of real-world applications [8], [15]. The key notations used throughout this paper are summarized in Table I.

To efficiently capture and analyze the geographical area of interest, we adopt a discrete spatiotemporal representation in the form of a grid with dimensions $M \times N$ . Each cell in the grid is indexed by its coordinates $( x , y )$ , where $x \in { 1 , \ldots , M }$ and $y ~ \in ~ 1 , \ldots , N$ correspond to longitude and latitude, respectively. The temporal dimension is similarly discretized into time slots of fixed duration dt minutes, with $t \in { 1 , \dots , T }$ indexing each time slot.

Within this grid-based map, a total of C vehicles are unevenly distributed and indexed by $c = 1 , \ldots , C .$ . Each vehicle is equipped with sensors capable of automatically collecting environmental data at every time slot t. For each vehicle c, a set of candidate trajectories is defined as $\mathit { R } _ { c } ,$ consisting of K distinct routing options. Each trajectory is represented as a three-dimensional tensor rkc ∈ RM×N×T , $\mathbf { r } _ { c } ^ { k } \in \bar { \mathbb { R } } ^ { M \times N \times T } .$ which encodes the vehicle’s spatial occupancy over the entire sensing period T . The trajectory ultimately selected for vehicle c from its candidate set $R _ { c }$ is denoted by $D _ { c }$ .

The proposed dispatch operation focuses on selecting the optimal trajectory from the set of possible traces $r _ { c } ^ { k } \in R _ { c } ,$ , thereby modifying the spatiotemporal distribution of the dispatched vehicle. Each vehicle, denoted as $c ,$ has a default trajectory represented by $r _ { c } ^ { 0 } ,$ which corresponds to the vehicle’s path without any dispatch intervention. The vehicle trajectory $R _ { c }$ is generated by a mobility predictor adapted from [16]. Instead of operating directly on the raw road network, this method constructs a time-dependent landmark graph by mining historical trajectory data, thereby effectively encapsulating the collective driving intelligence of the driver population. Its core innovation lies in the introduction of a Variance-Entropy Clustering algorithm, which accurately quantifies the volatility and uncertainty of travel time. This enables probabilistic modeling of time-varying traffic patterns and significantly improves the accuracy of trajectory prediction. During the online computation phase, the system employs a two-stage routing strategy upon receiving a query: first, it searches the landmark graph for a sequence of landmarks to form a coarse route, and then refines this route within the actual road network to produce the final drivable path. The formula for generating candidate vehicle trajectories from historical data is as follows:

$$
R _ {c} = \text { MobilPred } (\sum_ {c ^ {\prime} = 1} ^ {C} \mathcal {O} _ {c ^ {\prime}} ^ {\prime}) \tag {1}
$$

where MobilPred is the mobility predictor, $\mathcal { O } _ { c ^ { \prime } } ^ { \prime } \in M \times N \times T ^ { \prime }$ represents the known historical trajectory of vehicle $c ^ { \prime } , T ^ { \prime }$ denotes the historical observation time horizon, and the set of historical vehicles $C ^ { \prime }$ may differ from the vehicle c whose trajectory is to be predicted.

To determine whether the scheduler selects vehicle c and assigns it a route, we introduce an indicator variable $I _ { c } ,$ defined as follows:

$$
I _ {c} = \left\{D _ {c} = = r _ {c} ^ {k} \right\} \in \{0, 1 \} \tag {2}
$$

Dispatching non-dedicated vehicles may interfere with their primary missions and incur additional incentive costs. When the dispatcher decides to modify a vehicle’s trajectory $( I _ { c } =$ 1), a corresponding incentive $a _ { c }$ is provided as compensation. The proposed incentivization scheme allocates incentives to individual vehicle agents to ensure their willingness to undertake assigned tasks, while keeping the total incentive expenditure within a predefined budget constraint, denoted as B.

$$
\sum_ {c = 1} ^ {C} a _ {c} \cdot I _ {c} \leq B \tag {3}
$$

Related studies in this field have investigated various compensation models aimed at incentivizing participation while minimizing disruptions to users’ routine activities [2], [17]. In the Section IV, we further examine the impact of user acceptability on the effectiveness of the proposed dispatching scheme.

# C. Problem Formulation

To balance sensing reliability and sensing coverage, we propose a novel objective function termed ASQ. The ASQ formulation is inspired by prior work in the sensing coverage domain [15], [18], where entropy is employed to quantify the spatial evenness of sensor distribution. We extend this concept by integrating sensing reliability into the model. Sensing reliability is derived from the truth discovery paradigm [19], which characterizes sensor trustworthiness through a reliability factor $w _ { c } . \mathrm { ~ A ~ }$ higher value of $w _ { c }$ indicates a more reliable sensor, with $w _ { c } = 1$ representing average reliability. This framework

TABLE I MAJOR NOTATIONS 

<table><tr><td>Symbol</td><td>Description</td></tr><tr><td> $t \in \{1, \dots, T\}$ </td><td> $t$ -th time slot for data collection</td></tr><tr><td> $T$ </td><td>Number of time slots in one dispatch period</td></tr><tr><td> $(x, y)$ </td><td>Grid coordinates  $(x \in \{1, \dots, M\}, y \in \{1, \dots, N\})$ </td></tr><tr><td> $c \in \{1, \dots, C\}$ </td><td>The  $c$ -th vehicle among  $C$  vehicles</td></tr><tr><td> $I_c$ </td><td>Binary indicator for vehicle  $c$  dispatch status</td></tr><tr><td> $R_c$ </td><td>All possible trajectories for vehicle  $c$ </td></tr><tr><td> $r_c^k$ </td><td>The  $k$ -th trajectory of vehicle  $c$ ,  $r_c^k \in R_c$ ,  $c \in \{0, \dots, C\}$ </td></tr><tr><td> $\mathcal{O}_{c'}'$ </td><td>The historical trajectories of vehicle  $c'$ </td></tr><tr><td> $D_c$ </td><td>Selected trajectory for vehicle  $c$  ( $M \times N \times T$  tensor)</td></tr><tr><td> $B$ </td><td>Budget for the dispatching system</td></tr><tr><td> $a_c \in \{1, \dots, \mathcal{A}\}$ </td><td>Monetary incentive for sensor  $c$ </td></tr><tr><td> $B_c$ </td><td>Total monetary incentive for all vehicles</td></tr><tr><td> $w_c \in \{1, \dots, \mathcal{W}\}$ </td><td>Estimated sensing reliability for sensor  $c$ </td></tr><tr><td> $\beta$ </td><td>Balance factor</td></tr><tr><td> $m_c^{(x,y,t)}$ </td><td>Reading from sensor  $c$  at grid  $(x, y, t)$ </td></tr><tr><td> $m_{(*)}^{(x,y,t)}$ </td><td>Aggregated result at grid  $(x, y, t)$ </td></tr><tr><td> $b_c \in \{1, \dots, \mathcal{B}\}$ </td><td>Constant bias for sensor  $c$ </td></tr><tr><td> $Q^{(x,y,t)}$ </td><td>Forecasted task request distribution ( $M \times N \times T$  tensor)</td></tr></table>

enables the identification of sensors producing more trustworthy data, as well as those that may require additional vehicle dispatching or redundant readings for compensation. The ASQ is formulated as follows:

$$
\phi_ {w} (\mathcal {W}, D _ {c}) = (1 - \beta) E (\mathcal {W}, D _ {c}) + \beta \log Q (\mathcal {W}, D _ {c}) \tag {4}
$$

where $\beta$ is a parameter that controls the relative importance of two sensing reliability-aware factors: coverage evenness and coverage rate.

The first term $E ( \mathcal { W } , D _ { c } )$ represents the spatial entropy of the sensed regions. Entropy, a classic measure of uncertainty in information theory, increases as sensor coverage becomes more evenly distributed, thereby promoting fair and efficient allocation of sensing resources [20]. The second term $l o g Q ( \mathcal { W } , D _ { c } )$ is a coverage-quality function weighted by sensing reliability. The logarithmic transformation compresses the dynamic range of $Q ( \mathcal { W } , D _ { c } )$ to match the scale of the entropy term, enhancing numerical stability and ensuring effective weighting. Moreover, the log function naturally captures diminishing returns in coverage improvement, preventing the algorithm from over-optimizing areas that already exhibit high coverage [21].

The entropy of the spatial distribution of sensed areas, denoted as $E ( \mathcal { W } , D _ { c } )$ , is computed as:

$$
E (\mathcal {W}, D _ {c}) = - \sum_ {x, y, t, \mathcal {W}} P (x, y, t, \mathcal {W}) \log P (x, y, t, \mathcal {W}) \tag {5}
$$

The higher the entropy, the more evenly the sensors are distributed across the area, which results in better sensing coverage. We define $P ( x , y , t , \mathcal { W } )$ as the aggregated sum of variance factors within the trajectory, calculated as:

$$
P (x, y, t, \mathcal {W}) = \frac {\sum_ {c = 1} ^ {C} w _ {c} D _ {c} (x , y , t)}{C T} \tag {6}
$$

This equation defines the probability distribution of vehicle agents, where $D _ { c } ( x , y , t )$ indicates the presence of vehicle c at location $( x , y )$ and time t, and $w _ { c }$ denotes the weight associated with vehicle $c .$ The sensing reliability, represented by $w _ { c } ,$ acts as a weighting factor that reflects the distribution of sensing trustworthiness across the spatiotemporal domain, thereby enabling the system to prioritize reliable coverage. The size of sensed areas, $Q ( \mathcal { W } , D _ { c } )$ , is calculated simply as:

$$
Q (\mathcal {W}, D _ {c}) = \left| (x, y, t): P (x, y, t, \mathcal {W}) > \frac {1}{C T} \right| \tag {7}
$$

where $Q ( \mathcal { W } , D _ { c } )$ represents the size of the sensed areas in the grid map where the net sensing reliability exceeds the average sensing reliability for a sensor.

The use of a weighted aggregate sum in Eq. (6) is motivated by its intuitive and generalizable ability to quantify sensing reliability. This formulation captures both the spatial evenness of sensor distributions and the individual reliability of each sensing agent. While the current model is designed to align with a weighted average data fusion approach, future work may investigate its integration with more advanced data fusion algorithms.

$$
\max_{\substack{c = 1,\dots ,C\\ k = 1,\dots ,K}}\phi (\mathcal{W},D_{c}) = (1 - \beta)E(\mathcal{W},D_{c}) + \beta \log Q(\mathcal{W},D_{c})
$$

$\mathrm { s u b j e c t ~ t o } \quad \left\{ \begin{array} { l l } { D _ { c } = r _ { c } ^ { k } , k \in \{ 1 , 2 , \ldots , K \} } \\ { I _ { c } \in \{ 0 , 1 \} } \\ { \sum _ { c = 1 } ^ { C } a _ { c } \cdot I _ { c } \leq B } \end{array} \right.$ (8)

The objective function aims to maximize ASQ by balancing the entropy of sensor distributions and the extent of the sensed areas, both weighted by sensing reliability. Additionally, the model incorporates physical mobility constraints related to vehicle scheduling, along with a budgetary constraint. This optimization problem is NP-hard, involving the combinatorial selection of discrete variables (Ic) and the continuous adjustment of reliability weights $( w _ { c } )$ . It features a nonlinear objective function $\phi _ { w }$ and a linear constraint $\sum a _ { c } \cdot I _ { c } \leq B$ .

The novelty of this formulation lies in its simultaneous integration of sensing reliability and sensing coverage as core components of vehicular sensing performance. By embedding both factors into a unified framework, the model enables the joint optimization of sensor deployment and measurement fidelity.

![](images/d2743860ff2efed47de5e19a7cd0d1b0d97f89ca0b8549555b33188459152411.jpg)



Fig. 3. This figure shows our proposed algorithm’s framework.

# III. ALGORITHM DESIGN

In this section, we present our proposed dispatching framework for improving QoI by optimizing ASQ. The algorithm consists of three key steps: Online Sensing Reliability Inference, Monetary Incentive Mechanism, and Mutually Assisted Belief-aware Vehicle Dispatching (shown in Fig. 3). The first step focuses on deriving the reliability of sensors operating within a common spatial domain (Section III-A). The second step quantifies the monetary incentives required for vehicle dispatching (Section III-B). The third step integrates the inferred sensing reliability with the calculated monetary incentives to inform the vehicle dispatching process (Section III-C). These steps form an iterative loop, where Mutually Assisted Belief-aware Vehicle Dispatching also contributes to improvements in both Online Sensing Reliability Inference and Monetary Incentive Mechanism. Finally, we analyze the algorithm’s time complexity in Section III-D.

# A. Online Sensing Reliability Inferring

In our framework, we adopt the concept of truth discovery [19] to model the sensing reliability of sensors using the reliability factor $w _ { c }$ . Truth discovery is a technique that infers the sensing reliability of sensors by comparing their measurements $m _ { c } ^ { ( x , y , t ) }$ with the inferred truth $m _ { ( * ) } ^ { ( x , \bar { y } , t ) }$ , derived from other sensors in correlated sensing scenarios. However, in real-world sensing, different sensors often exhibit consistent deviations from the true value, leading to bias. This bias can significantly affect the data fusion results, particularly if all sensors dispatched to a single location share the same direction of bias, such as underestimating the true value. To address this challenge and account for systematic errors, we enhance the truth discovery approach by introducing a bias term $b _ { c }$ and reformulating the optimization function as follows:

$$
\min _ {\mathcal {M}, \mathcal {W}, \mathcal {B}} f (\mathcal {M}, \mathcal {W}, \mathcal {B}) =
$$

$$
\sum_ {x, y, t} \{\sum_ {c = 1} ^ {C} w _ {c} \| m _ {(*)} ^ {(x, y, t)} - m _ {c} ^ {(x, y, t)} + b _ {c} \| ^ {2} \} \tag {9}
$$

$$
\text { s.t. } \quad \sum_ {c = 1} ^ {C} \exp (- w _ {c}) = 1, \sum_ {c = 1} ^ {C} b _ {c} = 0
$$

In this optimization function, we aim to minimize the weighted sum of the differences between the inferred truth m(∗) $m _ { ( * ) } ^ { ( x , y , t ) }$ and the observed measurements $m _ { c } ^ { ( x , y , t ) }$ (x,y,t)c , while accounting for the bias terms $b _ { c } .$ The objective is to reduce the overall discrepancy between the aggregated truth and the bias-adjusted, reliability-weighted sensor readings. The first constraint limits the range of the weights to prevent them from becoming arbitrarily large or approaching negative infinity. The second constraint ensures that the bias terms do not dominate or nullify the influence of all sensor readings.

To infer sensing reliability, we formulate the optimization problem as described in (9). We adopt an approach similar to that of [19], employing Lagrange multipliers to solve the constrained optimization. The goal is to estimate the reliability values for each sensor accurately. By applying Lagrangian optimization, we derive the following equations:

$$
\mathcal {M}: m _ {(*)} ^ {(x, y, t)} = \frac {\sum_ {c = 1} ^ {C} w _ {c} (m _ {c} ^ {(x , y , t)} - b _ {c})}{\sum_ {c = 1} ^ {C} w _ {c}} \tag {10}
$$

$$
\mathcal {W}: w _ {c} = - \log \frac {\sum_ {(x , y , t)} \| m _ {(*)} ^ {(x , y , t)} - m _ {c} ^ {(x , y , t)} + b _ {c} \| ^ {2}}{\sum_ {(x , y , t)} \sum_ {c ^ {\prime} = 1} ^ {C} \| m _ {(*)} ^ {(x , y , t)} - m _ {(c ^ {\prime})} ^ {(x , y , t)} + b _ {c ^ {\prime}} \| ^ {2}} \tag {11}
$$

$$
\mathcal {B}: b _ {c} = \frac {\sum_ {x , y , t} (m _ {c} ^ {(x , y , t)} - m _ {(*)} ^ {(x , y , t)})}{\| r _ {c} (x , y , t) \neq 0 \|} \tag {12}
$$

These equations facilitate the inference of sensing reliability values for individual sensors based on their measurements and the corresponding calculated weights.

Algorithm 1 is designed to estimate the reliability factor $w _ { c }$ and constant bias $b _ { c }$ of each sensor in real-time, using the inferred truth (m(x,y(∗) $( m _ { ( * ) } ^ { ( x , y , t ) } )$ ,t)) for all sensors over a given time period. The algorithm takes as input the sensing values, error bound ϵ, and previous outputs (m(x,y,(∗)′ $\epsilon ,$ $( \dot { m } _ { ( * ) ^ { \prime } } ^ { ( x , y , t ) } , w _ { c } ^ { \prime } , b _ { c } ^ { \prime } )$ , and returns the updated data quality estimates $( w _ { c } , \ b _ { c } )$ along with the updated inferred truth (m(∗) $\ c ( \dot { m } _ { ( * ) } ^ { ( x , y , t ) } )$ (x,y,t)).

For each spatiotemporal cell $( x , y , t )$ , the algorithm iterates over all sensors within the corresponding cluster $s _ { ( x , y , t ) }$ to update their data quality estimates $( w _ { c }$ and $b _ { c } )$ . (11) and (12) are employed to perform this update. Subsequently, the inferred truth is updated using (10), based on the newly updated data quality estimates. These equations incorporate past outputs $( \bar { m } _ { ( * ) ^ { \prime } } ^ { ( x , y , \bar { t } ) } , w _ { c } ^ { \prime } , b _ { c } ^ { \prime } )$ as parameters in the summation, effectively leveraging historical data to inform the update process.

The belief in the sensing reliability inference is naturally derived from (11). From this equation, we observe that the value of w can be expressed as w ∝ log k · d(m(x,y(∗) $k \cdot d ( m _ { ( * ) } ^ { ( x , y , t ) } , m _ { c } ^ { ( x , y , t ) } - b _ { c } )$ (x,y,t)c − bc),

Algorithm 1: Online Sensing Reliability Inference   
Input : sensing value of all sensors in a given time period $m_{c}^{(x,y,t)}$ , $c \in C$ , error bound $\epsilon$ , past outputs $(m_{(*)'}^{(x,y,t)}, w_{c'}', b_{c'}')$ Output: updated data quality estimates $w_{c}$ , $b_{c}$ , and inferred truth $m_{(*)}^{(x,y,t)}$ 1 Split the sensors into clusters based on their location, so that $s_{(x,y,t)} = \{c \mid s_{c} = (x,y,t)\}$ ;

2 Initialization: Set Lagrangian factor $\lambda = 0$ ;

3 while error > $\epsilon$ do

4 $\lambda \leftarrow \lambda + \sum_{c \in s_{(x,y,t)}} (m_{(*)}^{(x,y,t)} - m_{c}^{(x,y,t)})^{2}$ ;

5    for $(x,y,t) \in (M,N,T)$ do

6    for $c \in s_{(x,y,t)}$ do

7    Update $w_{c}$ using (11);

8    Update $b_{c}$ using (12);

9    end

10    Update $m_{(*)}^{(x,y,t)}$ using (10);

11    error $\leftarrow |m_{(*)}^{(x,y,t)} - m_{(*)'}^{(x,y,t)}|$ ;

12    if error $\leq \epsilon$ then

13    break;

14    end

15 $m_{(*)'}^{(x,y,t)} \leftarrow m_{(*)}^{(x,y,t)}$ ;

16    end

17 end

where k refers to the vehicles that participate in the measurement aggregation. Based on this, we define the belief of the estimate $\varepsilon _ { c }$ as follows:

$$
\varepsilon_ {c} = \log \left(\sum_ {\substack {i = 1 \\ i \neq c}} ^ {C} \sum_ {t = 1} ^ {T} \mathbf {r} _ {c} ^ {k} (t) \cdot \mathbf {r} _ {i} ^ {k} (t)\right) \tag{13}
$$

Here, $\mathbf { r } _ { c } ^ { k } ( t )$ is the k-th trajectory of vehicle $c .$ The product of the two tensors represents the overlap of the trajectories between all vehicles. By summing over all vehicles and time slots, we obtain the total number of vehicles that have an overlapping trajectory with vehicle c. Taking the logarithm of this total yields the belief signal $\varepsilon _ { c } .$ If there is no overlap between another vehicle and $c ,$ the belief $\varepsilon _ { c }$ equals 0, indicating that the inferred sensing reliability for vehicle c is low.

# B. Monetary Incentive Calculating

We allocate incentives to the dispatched vehicles to ensure their willingness to perform the assigned tasks, while adhering to the budget constraints on total incentives. The utility of each vehicle is defined as its expected future returns. Given a potential scheduled trajectory $D _ { c } ^ { r }$ , the incentive $a _ { c }$ is designed to compensate for the utility loss incurred by the vehicle when accepting rather than rejecting $D _ { c } ^ { r }$ . Since vehicles inherently seek to maximize their utility, this approach guarantees their acceptance of the proposed incentive.

The core of the incentive design lies in accounting for the probability of vehicle agents receiving new task requests at their destinations. Since the primary objective of vehicle agents is to identify potential customer requests, the likelihood of obtaining ride requests at the assigned destination plays a critical role in their decision to accept a dispatched task. Therefore, the key challenge in designing the incentive mechanism is to develop a dynamic and differentiated pricing strategy under a limited budget that accurately compensates drivers for the opportunity costs and risks associated with accepting certain tasks, particularly those directed to lowdemand areas. By doing so, the mechanism effectively enlarges the feasible region of the optimization model, transforming driver behavioral uncertainty into a tractable component of the solution space. This enables more flexible and efficient task assignment, ultimately maximizing both the system scheduling success rate and sensing coverage.

Algorithm 2: Monetary Incentive Mechanism   
Input: estimated original trajectory of all vehicles $r_c^0$ , a potential dispatch trajectory $r_c^k \in R_c$ , ride request predict $Q^{(x,y,t)}$ , scheduling period $T$ , $\{r_{min}, r_{max}\}$ Output: monetary incentive $a_c$ 1 Initialization: Set $a_c = r_{min}$ , $t = 0$ ;

2 for $t++ \leq T$ do

3 Calculate $Q_c^0$ by (15);

4 Calculate $Q_c^r$ by (16);

5 Calculate $a_c$ by (14);

6 end

We adopt the model discussed in [22], which predicts the number of ride requests at various locations and times within the city based on historical task request data. This prediction enables the system to effectively match ride requests with available vehicles, allowing the deployment of more vehicles within the same budget, thereby enhancing the quality of sensing coverage.

Algorithm 2 is designed to calculate the incentives required for potential dispatch trajectories within a given period. Let $Q ^ { ( x , \bar { y } , t ) } \in [ 0 , 1 ]$ denote the probability that a vehicle located at a specific spatial position $( x , y )$ at time t will receive at least one task request. This probability is approximated by the ratio of the number of task requests to the number of idle vehicle agents within the grid. If this ratio exceeds 1, the task request probability is capped at 1. Next, we define $r _ { m a x }$ as the maximum monetary incentive typically accepted by the dispatch platform. Let the dispatching period be denoted as $T ,$ , and define $r _ { u } = r _ { m a x } / T$ as the utility at each time point. Additionally, for all vehicles, the incentive has a lower bound, $r _ { m i n }$ , to ensure that the incentives provided are not negligible. Based on these considerations, we design the incentive $a _ { c }$ to encourage vehicle agent c to accept the potential assigned trajectory $D _ { c }$ :

$$
a _ {c} = \max \left(\min (r _ {\max}, r _ {\max} - r _ {u} \cdot (Q _ {c} ^ {r} - Q _ {c} ^ {0})), r _ {\min}\right) \tag {14}
$$

$$
Q _ {c} ^ {0} = \sum_ {x, y} Q ^ {(x, y, t)} r _ {c} ^ {0} \tag {15}
$$

Algorithm 3: Mutually Assisted Belief-aware Vehicle Dispatching   
Input : estimated original trajectory of all vehicles $r_{c}^{0}$ , possible trace set of vehicle $R_{c}$ ,
dispatching budget B, scheduling period T,
sensing reliability W, monetary incentive $a_{c}$ Output: an improved feasible solution $S^{*} = \{I_{c}, D_{c}, B_{c}\}$ 1 Initialize a feasible solution $S = \{I_{c}, r_{c}^{0}, B_{c}\}$ , set $S^{*} = S$ , t = 0, belief $\varepsilon$ through (13);

2 for $t \leq T$ do

3 $S = S^{*}$ , $B_{c} = 0$ ;

4    Calculate $P(x, y, t, W)$ by (6);

5 $C^{*} \leftarrow \{c \mid \varepsilon_{c} = \max(\varepsilon_{c})\}$ ;

6    for $c \in C^{*}$ do

7 $k^{*} = \max_{\varepsilon_{c}} \{\max_{r} V(r_{c}^{k}, P) \mid r_{c}^{k} \in R_{c}\}$ ;

8    if $k^{*}$ is the original trace then

9    Cancel c dispatching ;

10    end

11    if $B_{c} \leq B$ then

12    Dispatch vehicle c with trace $k^{*}$ ;

13 $B_{c} = B_{c} + a_{c}$ 14    else

15    continue ;

16    end

17 $c = c \rightarrow next$ ;

18    end

19    Select ( $c', k'$ ) = arg max $_{c,k} V(r_{c}^{k*}, P)$ ;

20    if $k' > 0$ then

21 $D_{c} = r_{c}^{k*}$ ;

22    Update $S^{*} = \{I_{c}, D_{c}, B_{c}\}$ , $B_{c}$ and $\varepsilon_{c}$ ;

23    else

24 $I_{c'} = 0$ , $B_{c} = 0$ ;

25    end

26 end

$$
Q _ {c} ^ {r} = \sum_ {x, y} Q ^ {(x, y, t)} D _ {c} \tag {16}
$$

Here, $Q _ { c } ^ { 0 }$ represents the expected number of ride requests that vehicle c can receive during period $T$ along its original trajectory $r _ { c } ^ { 0 } ,$ while $Q _ { c } ^ { r }$ represents the expected number of ride requests that c can receive during $T$ along the trajectory $D _ { c } .$ . The incentive $a _ { c }$ is constrained within the range $[ r _ { m i n } , r _ { m a x } ]$ . Based on the number of ride requests along the vehicle’s original trajectory, if the scheduled trajectory $D _ { c }$ enables vehicle agent c to discover more task requests, the increase in request probability is treated as an implicit incentive, with lower monetary compensation considered. Conversely, higher compensation is provided to ensure the vehicle is willing to accept the scheduled task.

# C. Mutually Assisted Belief-aware Vehicle Dispatching

Algorithm ?? is designed to enhance the QoI by strategically dispatching vehicles to maximize the ASQ. In this framework, collaborative sensing reliability is inferred through the aggregation of data from multiple sensors operating within overlapping spatial regions, while monetary incentives are computed based on the predicted ride request densities at various destinations. By exchanging information and sharing resources, sensors and vehicles mutually assist one another, thereby improving both the reliability of the collected data and the operational efficiency of the dispatching process. Prior to initiating the scheduling procedure, the Data Request End provides the scheduling period T and the monetary budget B. Upon completion of the scheduling, the algorithm returns the improved vehicle coverage and updated belief to the Data Request End. During the scheduling period T , the total monetary incentives allocated must not exceed the available budget B.

In contrast to previous work [9], our approach explicitly accounts for sensing reliability and its inference, rather than assuming uniform reliability across all vehicles. We prioritize vehicles with overlapping trajectories, as they are more likely to provide accurate inferred sensing reliability. These vehicles are then dispatched to less populated areas, thereby enhancing both data collection and the reliability of the inferred sensing. To ensure that vehicles are willing to accept the scheduling, we offer incentive-based compensation, guaranteeing that their total earnings after dispatch are no less than those from executing their original trajectories.

Once the scheduling is accepted, dispatching is carried out to improve sensing coverage with respect to sensing reliability, employing a V value-based approach. This optimization enhances both overall data coverage and the quality of the collected information. The calculation of the V value is given by:

$$
V _ {c} (r _ {c} ^ {k}, P) = - \frac {\sum_ {x , y , t} w _ {c} \cdot r _ {c} ^ {k} \cdot P (x , y , t , \mathcal {W})}{\sum_ {x , y , t} P (x , y , t , \mathcal {W})} \tag {17}
$$

Here, $r _ { c } ^ { k }$ denotes either the selected trajectory of the current vehicle or the predicted trajectory generated by the mobility predictor. The term $w _ { c }$ represents the reliability factor, while $P ( x , y , t , \mathcal { W } )$ denotes the aggregated variance factor along the trajectory.

# D. Time Complexity Analysis

To analyze the complexity of our algorithm, we focus on the time complexity of each individual step. The initialization step has a time complexity of $\mathcal { O } ( C )$ , where C is the number of vehicles, since each vehicle needs to be initialized. The calculation step has a time complexity of $\mathcal { O } ( C T ^ { 4 } )$ , as we need to compute the sensing quality for each pair of vehicles. The trajectory size is estimated to have a complexity of $\mathcal { O } ( T ^ { 4 } )$ , based on the use of the Bellman-Ford algorithm for trajectory optimization. Therefore, the overall time complexity of our algorithm is $\mathcal { O } ( C T ^ { 4 } )$ .

# IV. EVALUATION

We present an evaluation of QUIDS through simulated dispatching and map reconstruction experiments using realworld data. The experimental setup uses data collected from a real-world deployment of the NVMCS system, combined with large-scale simulation-based scheduling to validate its performance (Section IV-A). We analyze how the ASQ varies with different factors and demonstrate the advantages of QUIDS over baseline approaches (Section IV-B). Additionally, we assess the effectiveness of the ASQ metric by exploring its relationship with downstream tasks (Section IV-C). Finally, we validate the efficacy of our proposed dispatching algorithm through an ablation study (Section IV-D).

![](images/1121393fda28a6d41f179a2f4dc6d84b71e0630d08ef4f73e7602fb278d5d775.jpg)



Fig. 4. The sensor platform deployed in our taxi, features a GPS receiver, a gas prompt, and four slacks capable of sensing various physical factors across the city.

# A. Experiment Setup

1) Real-World Data Collection and Processing: We deployed mobile sensors in 29 taxis to collect data over a twomonth period in a large city, capturing environmental variables such as humidity, temperature, $O _ { 3 }$ , and particulate matter (see Fig. 4). Real-time GPS location data from the taxis, along with accurate sensor readings, were recorded every 3 seconds. The data underwent preprocessing, including outlier removal and imputation of missing values using a sliding window approach with a window size of 5 minutes.   
2) Simulation Environment Configuration: To replicate a real-world scenario, we selected a specific area with relatively dense vehicle trajectories, corresponding to a 15 km × 8 km grid in the city. The spatial resolution was set to 1 km, consistent with typical air pollution monitoring setups [23], [24]. The temporal resolution (i.e., time period dt) was set to 2 minutes, and the actuation period was set to 5T (10 minutes), representing the average time for a taxi to travel 4 km, thereby ensuring that air quality conditions remained stable during the dispatching simulations. Due to factors such as water bodies, nature reserves, or administrative borders, 42 grid cells were not covered by any mobile sensor and were marked as excluded areas, and thus excluded from the performance metric calculations.   
3) Virtual Taxi Fleet Modeling: To simulate a large taxi fleet and analyze their trajectories, we utilized GPS data to extract the movement patterns of each vehicle. These trajectories reflect actual taxi movements without any incentivized dispatching. To expand the simulation to include 200 virtual taxis, we adjusted the mobility patterns and spatial distribution of the original trajectories, thereby enhancing coverage. This approach allowed us to assess the behavior and sensing

![](images/4a4582b4cf31d9ed0daea243c304026acb27e45e10b29fed9fb01657f0c74ac1.jpg)



(a) ASQ vs. Budget

![](images/b195cff6c0af36ee1af3e77b2c1262baafc4728ef564dc9b1972c8becb7fe50c.jpg)



(b) ASQ vs. M. Pred. Error

![](images/23c0cf6298ead2a9e609ef712c641e3cae7742116460548ffc815e99d9cda29f.jpg)



(c) ASQ vs. User Acceptance

![](images/c92b1bef22d78ba3898bf2cdd78a2fb36502c6753b827a8b72582d067da7bc75.jpg)



(d) ASQ vs. Error Level

Fig. 5. The performance of QUIDS under different factors.   
![](images/79b48ddb6a604640b12d2a88ec0f753f489e1f204beada6a01076a4c37e9faf5.jpg)



![](images/2bd603d699ea72ea75f6003ac4804ebebd64f8b1d9631a298ca465634287ca49.jpg)



Fig. 6. Sensing error after dispatching. Here we zoomed in on a typical area affected by dispatching algorithms.QUIDS expanded the sensing coverage without the loss of sensing reliability.   
Fig. 7. ASQ shows negative correlations with R-RMSE, among all different reconstruction algorithms.

coverage of a larger taxi fleet without the need for additional physical vehicles.

During the dispatching process, we set the monetary budget to $B = 4 0 0 \mathrm { U S D } .$ , assumed zero mobility prediction error, and set the dispatch acceptance rate to 100%. Considering the city taxi flag-down fare of 2 USD, we defined the cost parameters as $r _ { u } = 2 \mathrm { { U S D / m i n } } .$ , with $r _ { \operatorname* { m i n } } = 2 \mathrm { U S D }$ and $r _ { \mathrm { m a x } } = 2 0 \mathrm { U S D }$ . The first six weeks of data were used to train the mobility prediction and ride request models, while the remaining data were reserved for testing the proposed method.

4) Large-Scale Sensing Simulations: To simulate low-cost sensors with controllable sensing errors, we focus on evaluating the $O _ { 3 }$ data from our dataset, as low-cost sensors for $O _ { 3 }$ typically exhibit considerable variability in measurement accuracy and reliability. Given the availability of multiple relevant datasets, we leverage publicly accessible calibration data to model this variability. Specifically, we extract error distributions from established low-cost $O _ { 3 }$ sensor calibration datasets [25], [26], which provide detailed characterizations of the error profiles across different sensor types. These error distributions are subsequently applied to our fine-grained sensing resulting maps, ensuring that the simulated sensor types are consistent with those deployed in real-world scenarios.

To generate realistic sensor readings, we introduce sensing errors based on the extracted error distributions. These errors are systematically incorporated into the ground truth values of the sensor grid, thereby simulating the impact of lowcost sensors on both measurement accuracy and precision. By modeling sensing errors in this manner, we can rigorously evaluate the performance of our dispatching system under realistic sensing conditions, thereby closely approximating the challenges encountered in real-world low-cost sensor deployments.

5) Baselines Methods for Comparison: Six baseline methods are adopted to evaluate the improvement in the ASQ metric achieved by QUIDS:

• No Actuation (NA): This baseline refrains from any vehicle dispatch, serving as a passive reference to quantify the performance gain enabled by proactive scheduling.   
• Prediction-Based Actuation System (PAS): A predictive incentive system that anticipates vehicle trajectories and order demand to proactively optimize sensing coverage under a limited budget [8].   
• State-Aware Hybrid Incentive Program (SHIP): A taxi dispatching scheme incorporating fine-grained vehicle state classification and a hybrid opportunity–participation incentive model to improve sensing diversity while aligning platform and driver interests [27].   
• Vehicle Assisted Data Sensing algorithm (VADS): A coalitional sensing framework based on Stackelberg game theory and Nash equilibrium optimization, designed to balance economic incentives and resource allocation across multiple operators and vehicles [28].   
• Vickrey–Clarke–Groves-based Mobile Sensing Tasks (VCG-MST): An enhanced auction mechanism integrating Vickrey–Clarke–Groves pricing with staggered scheduling and budget awareness to jointly guarantee passenger service quality and sensing task allocation [29].

• Quality-informed multi-agent dispatching system (QUEST): A system jointly captures sensing coverage and reliability to handle uncertain, time-varying vehicle states [1]. • Graph Convolutional Cooperative Multi-Agent Reinforcement Learning (GCC-MARL): A multi-agent reinforcement learning approach using graph convolutional networks for distributed cooperative route planning, balancing passenger orders and sensing tasks [30].

6) Performance Metrics and Evaluation Protocol: We first utilize the ASQ metric, as defined in Section II-C, to evaluate the performance of various dispatching algorithms. To assess the real-world impact of ASQ and these dispatching strategies, we investigate their effects through a downstream task in mobile crowdsensing: map reconstruction. Map reconstruction involves generating a comprehensive representation of environmental data across a grid map, based on the measurements collected by dispatched vehicles. For this task, we employ three distinct map reconstruction algorithms: Linear Interpolation, Gaussian Process Regression, and Bayesian Gaussian CANDECOMP/PARAFAC (BGCP) [31]. Each of these methods provides a different approach to filling in the gaps between sensor measurements, ensuring that the reconstructed map reflects the underlying environmental conditions as accurately as possible.

To evaluate the effectiveness of the map reconstruction process, we primarily use the Reconstructed Root Mean Square Error (R-RMSE) metric. The R-RMSE quantifies the accuracy of the reconstructed map by comparing it to the ground truth. Lower R-RMSE values indicate better performance, meaning that the reconstructed map more closely aligns with the actual environmental conditions. This metric serves as a key indicator of the overall effectiveness of the dispatching strategies in terms of improving the quality and reliability of the reconstructed environmental maps.

# B. Evaluation for QUIDS

To evaluate the potential real-world impact of various dispatching algorithms, we introduce the Error Reduction Rate (Err. Reduction), a metric that quantifies the maximum reduction in R-RMSE across all map reconstruction algorithms. This metric allows us to assess the improvements in map reconstruction accuracy achieved by each dispatching approach. Specifically, Err. Reduction represents the relative decrease in reconstruction error due to the deployment of the dispatching algorithm, with higher values indicating better algorithm performance.

Table II presents a comparative analysis of the performance of various dispatching algorithms in terms of the ASQ metric and downstream field reconstruction tasks. The experimental results demonstrate that QUIDS achieves the best performance across all evaluated aspects, including the ASQ score, the Reconstructed Root Mean Square Error (R-RMSE) for three different field reconstruction algorithms, and the Error Reduction Rate (Err. Reduction). Specifically, QUIDS improves the ASQ metric by 38.02% compared to the No Actuation (NA) method, and by 9.61%, 5.87%, 15.26%, 4.88%, and 6.48% relative to PAS, SHIP, VADS, VCG-MST, and GCC-MARL, respectively. In terms of Err. Reduction, QUIDS achieves a 75.4% reduction compared to NA, significantly outperforming the second-best method, SHIP, which attains a 58.67% reduction. These results fully demonstrate the effectiveness and superiority of the QUIDS algorithm among state-of-theart solutions. Furthermore, the differences in R-RMSE and error reduction rates across the algorithms reflect the inherent trade-offs and advantages associated with enhancing sensing coverage and improving the accuracy of map reconstruction.

To further assess QUIDS under varying dispatching budgets, we plot ASQ against different budget levels in Fig. 5(a). Our proposed QUIDS consistently outperforms both baseline algorithms across all budget amounts. As the number of scheduled vehicles increases, QUIDS exhibits a more pronounced improvement compared to the PAS, achieving up to a 14.0% enhancement with a 200 USD budget. This improvement can be attributed to QUIDS’s ability to incorporate sensing reliability, thereby allowing for more effective allocation of the dispatching budget to maximize coverage. However, as the budget increases further, the advantage of QUIDS diminishes. This trend is expected, as the distribution of vehicles becomes increasingly dense, causing QUIDS to approach its performance ceiling when most vehicles are dispatched to already covered areas.

We investigate the influence of mobility prediction errors on various dispatching algorithms by introducing random errors with varying degrees of Euclidean distance bias [32]. As shown in Fig. 5(b), QUIDS demonstrates robustness across different levels of mobility prediction accuracy. Although ASQ decreases with increasing prediction error, QUIDS consistently outperforms the benchmark methods in most scenarios.

In practice, some vehicles may decline incentives due to unforeseen circumstances, lack of awareness, or individual preferences. To evaluate the impact of user acceptance rates on QUIDS performance, we model the acceptance rate as the probability that each vehicle agent will accept a task after receiving the proposed incentive strategy. We conducted 1,000 acceptance trials for each acceptance rate. Fig. 5(c) illustrates QUIDS’s performance across different time periods, with acceptance rates ranging from 60.0% to 100.0%. QUIDS consistently outperforms PAS, achieving higher ASQ scores and more effectively optimizing sensor coverage and reliability, even at lower acceptance rates.

To investigate the impact of varying degrees of sensing error on ASQ, we introduce controlled sensing errors by adding Gaussian noise, with the error level determined by the standard deviation. As illustrated in Fig. 5(d), the relationship between sensing error levels and ASQ is complex and algorithm-dependent. In certain cases, the ASQ value remains relatively stable or even slightly increases despite an increase in sensing error variance. This phenomenon occurs because ASQ primarily reflects the relative errors between different sensors, making it less sensitive to absolute changes in the sensing error.

Fig. 6 visualizes the dispatching outcomes based on ASQ. Both PAS and QUIDS dispatch vehicles from densely populated areas to sparsely populated regions. The overall sensing reliability is quantified using the Mean Absolute Error over Sensed area (S-MAE) over the sensed area. Notably, QUIDS demonstrates the lowest sensing error and the highest coverage among the evaluated algorithms, highlighting its effectiveness in balancing both sensing reliability and sensing coverage. Furthermore, an analysis of the spatial error distribution reveals that QUIDS significantly reduces errors in areas that are poorly covered by NA or PAS. This improvement can be attributed to QUIDS’s strategy of selecting vehicles with higher net sensing reliability, thereby generating more accurate and reliable data compared to NA or PAS.

TABLE II PERFORMANCE BY DIFFERENT DISPATCHING AND RECONSTRUCTION ALGORITHMS 

<table><tr><td>Algorithm</td><td>NA</td><td>PAS</td><td>SHIP</td><td>VADS</td><td>VCG-MST</td><td>QUEST</td><td>GCC-MARL</td><td>QUIDS</td></tr><tr><td>ASQ</td><td>4.05</td><td>5.10</td><td>5.28</td><td>4.85</td><td>5.33</td><td>5.37</td><td>5.25</td><td>5.59</td></tr><tr><td>Linear R-RMSE ( $\mu g/m^3$ )</td><td>49.72</td><td>28.90</td><td>37.67</td><td>25.85</td><td>17.41</td><td>26.49</td><td>23.84</td><td>24.16</td></tr><tr><td>GPR R-RMSE ( $\mu g/m^3$ )</td><td>39.25</td><td>28.81</td><td>27.51</td><td>21.59</td><td>13.35</td><td>26.48</td><td>19.23</td><td>23.93</td></tr><tr><td>BGCP R-RMSE ( $\mu g/m^3$ )</td><td>26.24</td><td>12.24</td><td>20.03</td><td>13.09</td><td>8.13</td><td>9.27</td><td>11.56</td><td>6.45</td></tr><tr><td>Err. Reduction (%)</td><td>-</td><td>53.32</td><td>58.67</td><td>50.12</td><td>69.32</td><td>64.6</td><td>55.96</td><td>75.4</td></tr></table>

TABLE III ABLATION STUDY 

<table><tr><td>Algorithm</td><td>QUIDS-NoRe</td><td>QUIDS-NoIn</td><td>QUIDS</td></tr><tr><td>ASQ</td><td>5.30</td><td>5.37</td><td>5.59</td></tr><tr><td>Linear RMSE ( $\mu g/m^3$ )</td><td>27.53</td><td>26.49</td><td>24.16</td></tr><tr><td>GPR RMSE ( $\mu g/m^3$ )</td><td>26.40</td><td>26.48</td><td>23.93</td></tr><tr><td>BGCP RMSE ( $\mu g/m^3$ )</td><td>10.58</td><td>9.27</td><td>6.45</td></tr><tr><td>Error Reduction (%)</td><td>59.7</td><td>64.6</td><td>75.4</td></tr></table>

# C. Evaluation for ASQ

Fig. 7 illustrates the relationship between ASQ and R-RMSE under varying experimental conditions, including different times, budgets, and algorithms. Each point represents a single round of simulation-based dispatching. This analysis underscores the critical role of ASQ in evaluating QoI for downstream tasks, particularly map reconstruction.

The experimental results reveal a clear negative correlation between ASQ and R-RMSE: higher ASQ scores generally correspond to lower R-RMSE values, indicating higher QoI during the map reconstruction process. This consistent association confirms that ASQ effectively quantifies the core concept of QoI and translates it into a measurable system-performance indicator. Although R-RMSE may vary at the same ASQ level due to differences in reconstruction algorithms and statistical fluctuations, this does not diminish ASQ’s function as a practical bridge between the qualitative notion of QoI and its quantitative assessment in system evaluation.

# D. Ablation Study

We conducted an ablation study to assess the contributions of Online Sensing Reliability Inference and Monetary

![](images/790480c05ee22371885f9cd7f08878b3d05a1bceb1a70ce047c2ed39f54be70c.jpg)



(a) Inferred w by QUIDS-NoRe

![](images/c8ddef8af1777524be6cd6ac485e76ce0baefc160d15e2c5cf6e62aecbb17660.jpg)



(b) Inferred w by QUIDS   
Fig. 8. These figures visualize the relations between the generated error and inferred reliability factor. QUIDS utilizes mutually assisted dispatching to acquire a more accurate inference.

Incentive Calculation to the overall performance of QUIDS. The configuration QUIDS-NoRe omits the Sensing Reliability Inference, where all sensors are assigned a uniform reliability level. In contrast, QUIDS-NoIn excludes the Monetary Incentive Calculation, resulting in identical incentives for all scheduled vehicles.

Table III presents the results of this ablation study. We observe that both QUIDS-NoRe and QUIDS-NoIn achieve higher ASQ values than the baselines shown in Table II; however, their performance still falls short of the full QUIDS configuration. This performance gap arises because QUIDS-NoRe does not accurately infer sensing reliability, which limits its ability to leverage optimal vehicle scheduling for error reduction. Similarly, QUIDS-NoIn fails to effectively allocate incentives, leading to a reduced number of vehicles available for scheduling. Both configurations highlight the critical importance of these two components within the QUIDS framework.

Fig. 8 illustrates the relationship between the inferred reliability factor w and the resulting sensing error across different regions. For this analysis, we selected three sectors with varying numbers of vehicle agents. In Fig. 8(a), we present the results of reliability inference using QUIDS-NoRe. While the inferred sensing reliability captures some aspects of the induced errors, the local aggregation of measurements introduces biases. These biases can cause well-performing sensors to receive lower w values due to discrepancies in the aggregated measurements. In contrast, Fig. 8(b) shows how mutually assisted dispatching enhances reliability inference. Despite minor deviations caused by inherent randomness, the results remain consistent, accurately classifying the sensing reliability of each sensor.

# V. DISCUSSIONS

We discussed the potential applications and future directions of QUIDS, while also highlighting its current limitations. Specifically, these include its generalizability to other NVMCS applications (Section V-A), the potential for improving its incentive model (Section V-B), and its dependence on accurate mobility predictions (Section V-C).

# A. Generalization to Other NVMCS Applications

Although QUIDS was originally developed for air pollution sensing, its underlying principles are generalizable to a wide range of NVMCS tasks. For instance, QUIDS can be adapted for applications such as wireless signal sensing, noise pollution mapping, and other environmental monitoring tasks. The system’s spatial granularity can be adjusted to meet the specific needs of these applications. However, since QUIDS’s reliability inference model is based on truth discovery, which assumes that the data originates from the same modality, it may face challenges in scenarios that require cross-modality data fusion for sensing reliability [33], [34]. To extend QUIDS for such cases, further design modifications would be necessary to integrate and harmonize data from different sensor modalities.

# B. Exploring Alternative Incentive Models

QUIDS currently uses a simple incentive model, but the introduction of alternative incentive strategies would not fundamentally disrupt its core contributions—modeling ASQ and implementing the mutually assisted dispatch framework. However, varying incentive patterns and scheduling methods could enhance the efficiency of vehicle dispatch and improve overall performance. For example, in cases where some vehicle agents accept tasks but do not adhere to the scheduled trajectories, two potential solutions could be explored: (1) Excluding malicious agents from the dispatch pool, and (2) Adjusting the trajectory matrix to a probabilistic model for candidates deemed potentially non-compliant, allowing for more flexible task assignment while maintaining overall reliability.

# C. Reliance on Accurate Mobility Predictions

As demonstrated in our evaluation, the performance of QUIDS is highly sensitive to the accuracy of mobility predictions. Since the algorithm relies on accurate predictions of vehicle trajectories for effective dispatch, ensuring the accuracy of mobility models is crucial for the successful real-world application of QUIDS. To mitigate the impact of prediction errors, future work could explore techniques for improving mobility prediction, such as integrating realtime data or using more advanced machine learning models for trajectory forecasting. Moreover, robustness to varying degrees of prediction error could further enhance the practical applicability of QUIDS in dynamic environments.

# VI. RELATED WORK

In this section, we review the related work in three key areas: Non-dedicated Vehicular Mobile Crowdsensing (Section VI-A), Sensing Coverage (Section VI-B), and Sensing Reliability (Section VI-C).

# A. Non-dedicated Vehicular Mobile Crowdsensing System

NVMCS leverages non-dedicated vehicles (e.g., taxis or private cars) for sensing purposes, improving both coverage and operational efficiency [35]. Previous research has explored various aspects of NVMCS, such as data volume [36], multiobjective trade-offs [37], incentivization strategies [38], [39], and data utilization [23], [40], [41]. In particular, several representative approaches have been proposed in the domain of incentive strategies. For instance, the State-Aware Hybrid Incentive Program (SHIP) employs fine-grained vehicle state classification and an opportunity-participation hybrid incentive model to improve sensing diversity while aligning the interests of both platforms and drivers [27]. The Vehicle-Assisted Data Sensing algorithm (VADS) is a coalitional sensing framework based on Stackelberg game theory and Nash equilibrium optimization, designed to balance economic incentives and resource allocation across multiple operators and vehicles [28]. Lastly, the Vickrey–Clarke–Groves-based Mobile Sensing Task mechanism (VCG-MST) integrates VCG pricing with staggered scheduling and budget awareness to simultaneously guarantee passenger service quality and effective sensing task allocation [29].

In contrast, our study specifically addresses the challenges of sensing reliability and coverage in NVMCS. Our findings complement and extend the existing body of NVMCS research, focusing on key issues that have been largely overlooked in previous works.

# B. Sensing Coverage

Ensuring comprehensive sensing coverage is a critical challenge in MCS systems. Researchers have proposed spatialtemporal scheduling approaches that consider energy efficiency or budget effectiveness when selecting NVMCS agents [42]–[44]. For example, [18] addressed spatio-temporal redundancy when performing NVMCS tasks in urban areas using high-resolution maps. Additionally, PAS first constructs two prediction models to estimate potential vehicle routes and passenger ride-hailing probabilities across urban areas, then introduces a prediction-based execution planning algorithm to select vehicles and assign routes [8]. iLOCuS remains exclusively concerned with the spatiotemporal distribution of sensed data and proposes a hierarchical iterative optimization algorithm to steer the data collected by vehicle agents toward a desired target distribution [9]. GCC-MARL develops a novel graph convolutional cooperative multi-agent reinforcement learning framework to achieve distributed and cooperative routing decisions, assisting taxis in balancing order-serving and sensing tasks [10]. All these methods optimize only for sensing coverage, operating under the assumption of nearly perfect sensor reliability. In reality, however, sensor reliability tends to exhibit significant uncertainty due to environmental disturbances and operational fluctuations. By contrast, QUIDS proposes a new metric termed Aggregated Sensing Quality (ASQ), which simultaneously captures both sensing coverage and reliability.

# C. Sensing Reliability

Mobile sensors are subject to environmental variations and external influences that complicate the task of ensuring reliable data collection [45]. Several methods have been proposed to address NVMCS sensing reliability, including comparing collected data with ground truth [46]–[48], calibrating sensors using external sources [11], [49], and leveraging machine learning models to improve sensor accuracy [12]. However, these methods face significant challenges in dynamic, NVMCS systems, where sensor types can vary, and ground truth references are often unavailable. Some approaches have tried to address these challenges by relying on historical data as pseudo-ground truth for static environments [50], [51]. Additionally, [19] proposed truth discovery techniques for correlated sensors and regions. While these methods provide useful insights, they remain constrained by two major issues: (1) Uneven distribution of non-dedicated vehicles: in areas with few vehicles, data coverage is sparse, resulting in unreliable sensing estimates and incomplete spatial coverage. (2) Failure to identify constant biases: existing methods primarily focus on detecting unreliable sensors but do not distinguish between dynamic errors and constant biases in sensor measurements. These limitations highlight the need for novel techniques capable of guiding dispatch decisions and enhancing the overall QoI in NVMCS systems.

# VII. CONCLUSION

To enhance the QoI in NVMCS systems, we propose QUIDS, a QUality-informed Incentive-driven multi-agent Dispatching System. We model the paradoxical relationship between sensing reliability and sensing coverage as an optimization problem. Our framework infers sensor reliability and calculates monetary incentives to dispatch vehicles in NVMCS systems, aiming to maximize the ASQ metric and, consequently, achieve optimal QoI. City-scale simulations based on physical features demonstrate significantly lower error rates at high coverage levels, validating the effectiveness of our approach. This solution opens new research directions for NVMCS systems, including the modeling and optimization of sensing reliability and sensing coverage under conditions of limited incentives and uncertain environments.

# REFERENCES

[1] Z. Li, F. Man, X. Chen, S. Xu, F. Dang, X.-P. Zhang, and X. Chen, “Quest: Quality-informed multi-agent dispatching system for optimal mobile crowdsensing,” in IEEE INFOCOM 2024-IEEE Conference on Computer Communications. IEEE, 2024, pp. 1811–1820.   
[2] Y. Liu, L. Kong, and G. Chen, “Data-oriented mobile crowdsensing: A comprehensive survey,” IEEE Communications Surveys Tutorials, vol. 21, no. 3, pp. 2849–2885, 2019.   
[3] C. Xiang, Y. Zhou, H. Dai, Y. Qu, S. He, C. Chen, and P. Yang, “Reusing Delivery Drones for Urban Crowdsensing,” IEEE Transactions on Mobile Computing, pp. 1–1, 2021.   
[4] X. Chen, H. Wang, Z. Li, W. Ding, F. Dang, C. Wu, and X. Chen, “DeliverSense: Efficient delivery drone scheduling for crowdsensing with deep reinforcement learning,” in Adjunct Proceedings of the 2022 ACM Ubicomp & ACM ISWC, pp. 403–408.   
[5] A. Feltenstein and J. Ha, “An analysis of the optimal provision of public infrastructure: A computational model using mexican data,” Journal of Development Economics, vol. 58, no. 1, pp. 219–230, 1999.

[6] N. Buch, S. A. Velastin, and J. Orwell, “A review of computer vision techniques for the analysis of urban traffic,” IEEE Transactions on intelligent transportation systems, vol. 12, no. 3, pp. 920–939, 2011.   
[7] C. Fiandrino, F. Anjomshoa, B. Kantarci, D. Kliazovich, P. Bouvry, and J. N. Matthews, “Sociability-driven framework for data acquisition in mobile crowdsensing over fog computing platforms for smart cities,” IEEE Transactions on Sustainable Computing, vol. 2, no. 4, pp. 345– 358, 2017.   
[8] X. Chen, S. Xu, J. Han, H. Fu, X. Pi, C. Joe-Wong, Y. Li, L. Zhang, H. Y. Noh, and P. Zhang, “Pas: Prediction-based actuation system for city-scale ridesharing vehicular mobile crowdsensing,” IEEE Internet of Things Journal, vol. 7, no. 5, pp. 3719–3734, 2020.   
[9] S. Xu, X. Chen, X. Pi, C. Joe-Wong, P. Zhang, and H. Y. Noh, “ilocus: Incentivizing vehicle mobility to optimize sensing distribution in crowd sensing,” IEEE Transactions on Mobile Computing, vol. 19, no. 8, pp. 1831–1847, 2020.   
[10] R. Ding, Z. Yang, Y. Wei, H. Jin, and X. Wang, “Multi-agent reinforcement learning for urban crowd sensing with for-hire vehicles,” in IEEE INFOCOM 2021, 2021, pp. 1–10.   
[11] Y. Cheng, X. He, Z. Zhou, and L. Thiele, “ICT: In-field Calibration Transfer for Air Quality Sensor Deployments,” Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, vol. 3, no. 1, pp. 1–19, Mar. 2019.   
[12] Y. Lin, W. Dong, and Y. Chen, “Calibrating Low-Cost Sensors by a Two-Phase Learning Approach for Urban Air Quality Measurement,” Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, vol. 2, no. 1, pp. 18:1–18:18, Mar. 2018.   
[13] F. C. Commission, “Report to congress on usps broadband data collection feasibility study,” May 2021. [Online]. Available: https://www.fcc.gov/sites/default/files/ report-congress-usps-broadband-data-collection-feasibility-05242021. pdf   
[14] T. Kassandros, E. Bagkis, and K. Karatzas, “Data Fusion for the Improvement of Low-Cost Air Quality Sensors,” in Air Pollution Modeling and its Application XXVIII, C. Mensink and O. Jorba, Eds., Cham, 2022, pp. 175–180.   
[15] S. Ji, Y. Zheng, and T. Li, “Urban sensing based on human mobility,” in Proceedings of the 2016 ACM International Joint Conference on Pervasive and Ubiquitous Computing, ser. UbiComp ’16, New York, NY, USA, 2016, p. 1040–1051.   
[16] J. Yuan, Y. Zheng, C. Zhang, W. Xie, X. Xie, G. Sun, and Y. Huang, “Tdrive: Driving directions based on taxi trajectories,” in Proceedings of the 18th SIGSPATIAL International Conference on Advances in Geographic Information Systems, New York, NY, USA, 2010, p. 99–108.   
[17] J. Liu, H. Shen, H. S. Narman, W. Chung, and Z. Lin, “A survey of mobile crowdsensing techniques: A critical component for the internet of things,” vol. 2, no. 3, 2018.   
[18] Q. Zhu, M. Y. Sarwar Uddin, N. Venkatasubramanian, and C.-H. Hsu, “Spatiotemporal scheduling for crowd augmented urban sensing,” in IEEE INFOCOM 2018, 2018, pp. 1997–2005.   
[19] C. Meng, W. Jiang, Y. Li, J. Gao, L. Su, H. Ding, and Y. Cheng, “Truth discovery on crowd sensing of correlated entities,” Proceedings of the 13th ACM Conference on Embedded Networked Sensor Systems, 2015.   
[20] T. Schreiber, “Measuring information transfer,” Physical review letters, vol. 85, no. 2, p. 461, 2000.   
[21] J. Napier, Mirifici logarithmorum canonis descriptio. A. Hart, 1914.   
[22] A. Jauhri, B. Foo, J. Berclaz, C. C. Hu, R. Grzeszczuk, V. Parameswaran, and J. P. Shen, “Space-time graph modeling of ride requests based on real-world data,” in Workshops at the Thirty-First AAAI Conference on Artificial Intelligence, 2017.   
[23] X. Chen, X. Xu, X. Liu, H. Y. Noh, L. Zhang, and P. Zhang, “HAP: Finegrained dynamic air pollution map reconstruction by hybrid adaptive particle filter,” in Proceedings of the 14th ACM Conference on Embedded Network Sensor Systems, ser. SenSys ’16, pp. 336–337.   
[24] X. Chen, X. Xu, X. Liu, S. Pan, J. He, H. Y. Noh, L. Zhang, and P. Zhang, “PGA: Physics guided and adaptive approach for mobile fine-grained air pollution estimation,” in Proceedings of the 2018 ACM Ubicomp & ACM ISWC, pp. 1321–1330.   
[25] J. M. Barcelo-Ordinas, P. Ferrer-Cid, J. Garcia-Vidal, M. Viana, and A. Ripoll, “H2020 project CAPTOR: raw data collected by low- cost MOX ozone sensors in a real air pollution monitoring network,” Mar. 2021. [Online]. Available: https://doi.org/10.5281/zenodo.4570449   
[26] O. Gonzalez, V. Barberan, and G. Camprodon, “iscape low cost sensor development data,” Dec. 2019. [Online]. Available: https: //doi.org/10.5281/zenodo.3570688

[27] H. Jiang, Y. Ren, J. Fang, Y. Yang, L. Xu, and H. Yu, “Ship: A state-aware hybrid incentive program for urban crowd sensing with forhire vehicles,” IEEE Transactions on Intelligent Transportation Systems, vol. 25, no. 3, pp. 3041–3053, 2023.   
[28] Z. Zhang, F. Zeng, and F. Tang, “Vehicle-assisted data sensing in vehicle edge metaverse: A game theory approach,” IEEE Transactions on Vehicular Technology, 2024.   
[29] S. Liu, Q. Ge, K. Han, D. Fukuda, and T. Dantsuji, “Mechanism design for coordinating vehicle-based mobile sensing tasks within the ridehailing platform,” Transportation Research Part C: Emerging Technologies, vol. 176, p. 105151, 2025.   
[30] R. Ding, Z. Yang, Y. Wei, H. Jin, and X. Wang, “Multi-agent reinforcement learning for urban crowd sensing with for-hire vehicles,” in IEEE INFOCOM 2021-IEEE Conference on Computer Communications. IEEE, 2021, pp. 1–10.   
[31] X. Chen, Z. He, and L. Sun, “A bayesian tensor decomposition approach for spatiotemporal traffic data imputation,” Transportation Research Part C: Emerging Technologies, vol. 98, pp. 73–84, 2019.   
[32] W. Hu, X. Xiao, Z. Fu, D. Xie, T. Tan, and S. Maybank, “A system for learning statistical motion patterns,” vol. 28, no. 9, pp. 1450–1464.   
[33] X. Chen, A. Purohit, C. R. Dominguez, S. Carpin, and P. Zhang, “Drunk-Walk: Collaborative and adaptive planning for navigation of microaerial sensor swarms,” in Proceedings of the 13th ACM Conference on Embedded Networked Sensor Systems, ser. SenSys ’15, pp. 295–308.   
[34] H. Wang, Y. Liu, C. Zhao, J. He, W. Ding, and X. Chen, “CaliFormer: Leveraging unlabeled measurements to calibrate sensors with selfsupervised learning,” in Adjunct Proceedings of the 2023 ACM Ubicomp & ISWC, pp. 743–748.   
[35] O. Rizwan, H. Rizwan, and M. Ejaz, “Development of an efficient system for vehicle accident warning,” in 2013 IEEE 9th International Conference on Emerging Technologies (ICET). IEEE, 2013, pp. 1–6.   
[36] S. M. A. Akber, I. A. Khan, S. S. Muhammad, S. M. Mohsin, I. A. Khan, S. Shamshirband, and A. T. Chronopoulos, “Data volume based data gathering in WSNs using mobile data collector,” in Proceedings of the 22nd International Database Engineering & Applications Symposium, ser. IDEAS ’18, pp. 199–207.   
[37] J. Sun, H. Jin, R. Ding, G. Fan, Y. Wei, and L. Su, “Multi-objective order dispatch for urban crowd sensing with for-hire vehicles,” in IEEE INFOCOM 2023, pp. 1–10.   
[38] X. Zhang, Z. Yang, W. Sun, Y. Liu, S. Tang, K. Xing, and X. Mao, “Incentives for mobile crowd sensing: A survey,” IEEE Communications Surveys Tutorials, vol. 18, no. 1, pp. 54–67, 2016.   
[39] E. Wang, D. Luan, Y. Yang, Z. Wang, P. Dong, D. Li, W. Liu, and J. Wu, “Distributed game-theoretical route navigation for vehicular crowdsensing,” in Proceedings of the 50th International Conference on Parallel Processing, ser. ICPP ’21, pp. 1–11.   
[40] E. Wang, W. Liu, W. Liu, C. Xiang, B. Yang, and Y. Yang, “Spatiotemporal transformer for data inference and long prediction in sparse mobile CrowdSensing,” in IEEE INFOCOM 2023, pp. 1–10.   
[41] X. Chen, S. Xu, X. Liu, X. Xu, H. Y. Noh, L. Zhang, and P. Zhang, “Adaptive hybrid model-enabled sensing system (HMSS) for mobile fine-grained air pollution estimation,” vol. 21, no. 6, pp. 1927–1944.   
[42] H. Ko, S. Pack, and V. C. M. Leung, “Coverage-guaranteed and energyefficient participant selection strategy in mobile crowdsensing,” IEEE Internet of Things Journal, vol. 6, no. 2, pp. 3202–3211, 2019.   
[43] X. Chen, S. Xu, H. Fu, C. Joe-Wong, L. Zhang, H. Y. Noh, and P. Zhang, “ASC: actuation system for city-wide crowdsensing with ride-sharing vehicular platform,” in Proceedings of the Fourth Workshop on International Science of Smart City Operations and Platforms Engineering, ser. SCOPE ’19, pp. 19–24.   
[44] J. Ren, Y. Xu, Z. Li, C. Hong, X.-P. Zhang, and X. Chen, “Scheduling UAV swarm with attention-based graph reinforcement learning for ground-to-air heterogeneous data communication,” in Adjunct Proceedings of the 2023 ACM Ubicomp & ISWC, pp. 670–675.   
[45] M. Younis and K. Akkaya, “Strategies and techniques for node placement in wireless sensor networks: A survey,” Ad Hoc Networks, vol. 6, no. 4, pp. 621–655, 2008.   
[46] S. Zhang, H. Sheng, C. Li, J. Zhang, and Z. Xiong, “Robust depth estimation for light field via spinning parallelogram operator,” Computer Vision and Image Understanding, vol. 145, pp. 148–159, 2016.   
[47] H. Sheng, S. Zhang, X. Cao, Y. Fang, and Z. Xiong, “Geometric occlusion analysis in depth estimation using integral guided filter for light-field image,” IEEE Transactions on Image Processing, vol. 26, no. 12, pp. 5758–5771, 2017.   
[48] Y. Liu, X. Liu, F. Man, C. Wu, and X. Chen, “Fine-grained air pollution data enables smart living and efficient management,” in Proceedings of

the 20th ACM Conference on Embedded Networked Sensor Systems, ser. SenSys ’22, pp. 768–769.   
[49] H. Wang, X. Chen, Y. Cheng, C. Wu, F. Dang, and X. Chen, “H-SwarmLoc: Efficient scheduling for localization of heterogeneous MAV swarm with deep reinforcement learning,” in Proceedings of the 20th ACM Conference on Embedded Networked Sensor Systems, ser. SenSys ’22, pp. 1148–1154.   
[50] D. Zhang, J. Huang, Y. Li, F. Zhang, C. Xu, and T. He, “Exploring human mobility with multi-source data at extremely large metropolitan scales,” in Proceedings of the 20th annual international conference on Mobile computing and networking, 2014, pp. 201–212.   
[51] J. Luo, Y. Hu, C. Yu, C. Hong, X.-P. Zhang, and X. Chen, “Field reconstruction-based non-rendezvous calibration for low cost mobile sensors,” in Adjunct Proceedings of the 2023 ACM Ubicomp & ISWC, pp. 688–693.