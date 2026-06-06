# QUIDS: Quality-Informed Incentive-Driven Multiagent Dispatching System for Mobile Crowdsensing

Nan Zhou , Zuxin Li , Fanhang Man, Xuecheng Chen , Susu Xu , Fan Dang , Senior Member, IEEE, Chaopeng Hong, Yunhao Liu , Fellow, IEEE, Xiao-Ping Zhang , Fellow, IEEE, and Xinlei Chen , Member, IEEE

Abstract—This article addresses the challenges of achieving optimal quality of information (QoI) in a nondedicated vehicular mobile crowdsensing (NVMCS) system, where vehicles not originally designed for sensing are leveraged to collect real-time data as they traverse urban environments. These challenges are exacerbated by the interrelated issues of sensing coverage, sensing reliability, and the inherently dynamic nature of participating vehicles. To tackle these challenges, we propose QUIDS, a quality-informed incentive-driven multiagent dispatching system, which ensures high sensing coverage and sensing reliability under budget constraints in NVMCS systems. QUIDS improves QoI by introducing a novel metric, aggregated sensing quality (ASQ), designed to quantitatively capture the concept of QoI by integrating both sensing coverage and sensing reliability. Moreover, we develop a mutually assisted belief-aware vehicle dispatching algorithm that estimates sensing reliability and allocates monetary incentives under uncertain vehicle conditions, thereby further improving ASQ. Evaluation using real-world data collected from a deployed NVMCS system in a metropolitan area demonstrates the effectiveness of QUIDS. The ASQ metric shows a 38% improvement over nondispatching scenarios and a 10% enhancement over state-of-the-art methods. In addition, QUIDS reduces reconstruction map errors by 39%–74% across various reconstruction algorithms, validating its efficacy in improving QoI within NVMCS systems. Addressing the often-overlooked issue of sensing reliability in existing studies, the QUIDS system leverages nondedicated vehicles and incorporates a quality-

Received 1 December 2025; accepted 26 December 2025. Date of publication 3 February 2026; date of current version 9 April 2026. This work was supported in part by the Natural Science Foundation of China under Grant 62371269, in part by Shenzhen Low-Altitude Airspace Strategic Program Portfolio under Grant Z25306110, in part by the Meituan Academy of Robotics Shenzhen, and in part by the Tsinghua Shenzhen International Graduate School-Shenzhen Pengrui Endowed Professorship Scheme of Shenzhen Pengrui Foundation. An earlier version of this paper was presented at the IEEE International Conference on Computer Communications (IEEE INFOCOM 2024) [DOI: 10.1109/INFOCOM52122.2024.10621374]. (Nan Zhou and Zuxin Li are co-first authors.) (Corresponding author: Xinlei Chen.)

Nan Zhou, Zuxin Li, Fanhang Man, Xuecheng Chen, Chaopeng Hong, Xiao-Ping Zhang, and Xinlei Chen are with the Shenzhen International Graduate School, Tsinghua University, Shenzhen 518071, China (e-mail: zhoun24@mails.tsinghua.edu.cn; lizx21@ mails.tsinghua.edu.cn; mfh21@mails.tsinghua.edu.cn; chenxc21@ mails.tsinghua.edu.cn; hongco@sz.tsinghua.edu.cn; xpzhang@ieee.org; chen.xinlei@sz.tsinghua.edu.cn).

Susu Xu is with the Department of Civil and System Engineering, Johns Hopkins University, Baltimore, MD 21218 USA (e-mail: sxu83@jhu.edu).

Fan Dang is with the School of Software Engineering, Beijing Jiaotong University, Beijing 100044, China (e-mail: dangfan@bjtu.edu.cn).

Yunhao Liu is with the School of Software and BNRist, Tsinghua University, Beijing 100084, China (e-mail: yunhao@greenorbs.com).

Digital Object Identifier 10.1109/JIOT.2026.3651903

informed, incentive-driven dispatching system to jointly optimize sensing coverage and sensing reliability. This enables low-cost, high-quality, and scalable urban environmental monitoring without the need for dedicated sensing infrastructure, and makes the system applicable to diverse smart-city scenarios such as traffic monitoring and environmental sensing.

Index Terms—Internet of Things, mobile crowdsensing, mobile sensing and applications, monetary incentive.

NOMENCLATURE 

<table><tr><td> $t \in \{1, \dots, T\}$ </td><td> $t$ th time slot for data collection.</td></tr><tr><td> $T$ </td><td>Number of time slots in one dispatch period.</td></tr><tr><td> $(x, y)$ </td><td>Grid coordinates  $(x \in \{1, \dots, M\}, y \in \{1, \dots, N\})$ .</td></tr><tr><td> $c \in \{1, \dots, C\}$ </td><td> $c$ th vehicle among  $C$  vehicles.</td></tr><tr><td> $I_c$ </td><td>Binary indicator for vehicle  $c$  dispatch status.</td></tr><tr><td> $R_c$ </td><td>All possible trajectories for vehicle  $c$ .</td></tr><tr><td> $r_c^k$ </td><td> $k$ th trajectory of vehicle  $c$ ,  $r_c^k \in R_c$ ,  $c \in \{0, \dots, C\}$ .</td></tr><tr><td> $\mathcal{O}_{c'}'$ </td><td>Historical trajectories of vehicle  $c'$ .</td></tr><tr><td> $D_c$ </td><td>Selected trajectory for vehicle  $c$  ( $M \times N \times T$  tensor).</td></tr><tr><td> $B$ </td><td>Budget for the dispatching system.</td></tr><tr><td> $a_c \in \{1, \dots, \mathcal{A}\}$ </td><td>Monetary incentive for sensor  $c$ .</td></tr><tr><td> $B_c$ </td><td>Total monetary incentive for all vehicles.</td></tr><tr><td> $w_c \in \{1, \dots, \mathcal{W}\}$ </td><td>Estimated sensing reliability for sensor  $c$ .</td></tr><tr><td> $\beta$ </td><td>Balance factor.</td></tr><tr><td> $m_c^{(x,y,t)}$ </td><td>Reading from sensor  $c$  at grid  $(x, y, t)$ .</td></tr><tr><td> $m_{(*)}^{(x,y,t)}$ </td><td>Aggregated result at grid  $(x, y, t)$ .</td></tr><tr><td> $b_c \in \{1, \dots, \mathcal{B}\}$ </td><td>Constant bias for sensor  $c$ .</td></tr><tr><td> $Q^{(x,y,t)}$ </td><td>Forecast task request distribution ( $M \times N \times T$  tensor).</td></tr></table>

# I. INTRODUCTION

N ONDEDICATED vehicular mobile crowdsensing(NVMCS) systems have emerged as a promising paradigm for collecting large volumes of spatiotemporal data [2]. Nondedicated vehicular sensing platforms, such as taxis, delivery drones [3], [4], and ride-sharing vehicles like Uber and Lyft, can collect data while navigating urban environments, offering cost-effective and easily maintainable solutions for NVMCS. By harnessing the collective sensing capabilities of these nondedicated vehicles, the NVMCS system supports a wide range of applications that enhance human life and inform decision-making processes, including public infrastructure management [5], traffic monitoring [6], and public policy formulation [7].

One of the key challenges in NVMCS systems is ensuring optimal quality of information (QoI), which depends on both sensing coverage and sensing reliability. Sensing coverage refers to the spatial and temporal extent of data collection, while sensing reliability pertains to the accuracy and consistency of sensor measurements. However, nondedicated vehicles, which prioritize fulfilling ride requests, often tend to concentrate in high-demand areas, leading to reduced sensing coverage in less populated or remote regions. In contrast, an effective NVMCS system typically requires comprehensive, city-wide data sampling to ensure sufficient spatio-temporal granularity for meaningful analysis. This imbalance in the spatial distribution of sensing resources diminishes overall sensing coverage, thereby undermining QoI. A seemingly straightforward solution is to dispatch vehicles to underserved areas, where sensing coverage is inadequate. However, this approach may result in a reduction in drivers’ earnings, as these areas typically experience fewer ride requests. Consequently, drivers may be reluctant to accept the proposed dispatch assignments, as they would be economically disadvantaged. To mitigate this issue, it is necessary to provide additional compensatory incentives that align the drivers’ economic motivations with the objectives of the sensing system. Moreover, the sensors deployed on nondedicated vehicles are inherently subject to various sources of uncertainty, which can introduce significant fluctuations in sensor readings. These fluctuations arise from multiple factors, including measurement inaccuracies, sensor degradation over time, and the absence of routine calibration. Such uncertainties can severely compromise the reliability and accuracy of the sensor data, which is critical for the overall performance of the NVMCS system.

In addition, the interplay between sensing coverage and sensing reliability often leads to a tradeoff. Specifically, evenly distributing sensors across the sensing area can improve coverage; however, this may reduce the number of sensors in each subregion, thereby increasing measurement uncertainties and diminishing reliability. Conversely, concentrating sensors in specific regions can enhance reliability by generating more data points, but this approach compromises coverage in other areas, resulting in data gaps and reduced spatial resolution. This inherent tradeoff between sensing coverage and sensing reliability presents significant challenges in achieving a balanced QoI, particularly in dynamic environments where sensor reliability is variable. These complexities further exacerbate the difficulty of ensuring high-quality data collection.

Existing solutions have made significant strides in enhancing the QoI in NVMCS systems. These solutions can be broadly categorized into two main approaches as follows.

1) Improving sensing coverage through vehicle dispatching, which includes various dispatching strategies such as dynamic programming [8], [9], and reinforcement learning [10]. However, these methods optimize only for sensing coverage and assume near-perfect sensor reliability. In reality, sensor reliability often exhibits significant uncertainty due to environmental interference and operational fluctuations. Neglecting sensing reliability may lead to unreliable data and misleading information.

2) Ensuring the sensing reliability of individual sensors, which focuses on improving sensor reliability using external References [11] or machine learning interpolation techniques [12] to enhance the performance of low-cost sensors. While these approaches are effective under certain conditions, they frequently assume the availability of specific sensor types or external calibration references, which can limit their applicability or make them prohibitively expensive in many real-world scenarios [13]. Moreover, they often fail to account for the monetary incentives required for vehicle dispatching, a crucial factor in ensuring the feasibility of the dispatching plan, especially considering the limited budgets typically available in practical applications.

The challenges of ensuring QoI in NVMCS systems can be summarized as follows.

C1) The inherent tradeoff between sensing coverage and sensing reliability. As discussed earlier, achieving an optimal balance between these two factors is critical; however, they often conflict, making simultaneous optimization difficult.   
C2) The difficulty of accurately estimating the sensing reliability of individual sensors. The continuous movement and varying locations of sensors, along with sensor drift and other uncertainties, complicate the assessment of the accuracy and consistency of their measurements.   
C3) The customization of an effective monetary incentive strategy. Limited incentive budgets and the willingness of vehicles to accept tasks under these financial constraints make the design of efficient incentive schemes particularly challenging. Therefore, in vehicle dispatching scenarios with constrained budgets, optimizing both sensing coverage and sensing reliability becomes increasingly complex and dynamic, thus hindering the improvement of QoI.   
To address these challenges, we propose QUIDS, a qualityinformed incentive-driven multiagent dispatching system, specifically designed to enable dynamic, sensing-driven dispatching for NVMCS tasks. Specifically, as follows.   
S1) To Tackle C1): We introduce a novel metric, aggregated sensing quality (ASQ), which effectively balances the tradeoff between sensing coverage and sensing reliability. Building on the insight that the sensing reliability of multiple lower quality sensors can be compensated by aggregating their readings, as outlined in [14], ASQ combines data from these sensors to produce a measure that approximates the performance of higher quality sensors.   
S2) To Tackle (C2&C3): We propose a mutually assisted belief-aware vehicle dispatching algorithm, grounded in the core principles of truth discovery, which integrates both sensing reliability and monetary incentives in guiding dispatch decisions. In this algorithm, the collaborative sensing reliability is derived from the aggregated data readings of multiple sensors, while monetary incentives are calculated based on ride requests originating from various destinations. Sensors

and vehicles are mutually assisted by exchanging information and resources, thereby enhancing both the reliability of the collected data and the operational efficiency of the dispatch process. Moreover, the dispatch process itself influences both the inference of sensing reliability and the computation of incentives, promoting adaptive and optimized data collection that improves the overall QoI. To evaluate the performance of our system, we deployed an NVMCS system involving 29 taxis over a two-month period to collect fine-grained air pollution data. The results demonstrate the effectiveness and potential of QUIDS in achieving optimal QoI in NVMCS scenarios.

To summarize, the main contributions of this article are as follows.

1) Propose a novel metric named ASQ to jointly optimize the inherent tradeoff between sensing coverage and sensing reliability, thereby enhancing the QoI.   
2) Design a mutually assisted belief-aware vehicle dispatching algorithm that enhances ASQ through real-time inference of sensing reliability.   
3) Design a monetary incentive mechanism, which incorporates human behavioral uncertainties into the modeling framework by introducing differentiated incentives, thereby effectively expanding the feasible region and solution space of the optimization problem.

The remainder of this article is organized as follows. In Section II, we formally define the coupled problem of sensing coverage and sensing reliability. Section III presents the proposed algorithmic framework in detail. In Section IV, we conduct a comprehensive performance evaluation of the proposed method. Section V discusses the generalizability and potential limitations of our approach. A review of related work is provided in Section VI. Finally, Section VII concludes the article.

# II. SYSTEM MODEL AND DEFINITION

We consider an NVMCS system that encounters challenges stemming from uneven sensing coverage and inconsistent sensing reliability. To address this issue, we present case studies (Section II-A), describe the system model and dispatching parameters (Section II-B), and detail how sensing reliability and sensing coverage are modeled as two key components of vehicular sensing performance (Section II-C), ultimately aiming to enhance QoI.

# A. Motivation Case Studies

In NVMCS systems, accurately measuring $O _ { 3 }$ levels is crucial for assessing air quality and identifying potential health risks. However, widely deployed low-cost $O _ { 3 }$ sensors often show substantial deviations from ground-truth measurements, as illustrated in Fig. 1(a). Such discrepancies compromise the reliability of the sensed data, thereby hindering informed decision-making. Furthermore, the lack of continuous calibration for sensors mounted on nondedicated vehicles introduces additional uncertainty regarding the accuracy of their readings, further complicating the data collection process.

To address these challenges, we explore the potential of data fusion techniques to enhance sensing reliability by compensating for the limitations of low-quality sensors through increased sensor density. Prior research [14] has shown that data fusion can significantly reduce the relative expanded uncertainty among multiple sensors with substantial deviations, as illustrated in Fig. 1(b). Building on this insight, the present study adopts a multistage approach to improve the reliability of sensor measurements in scenarios where reference monitoring data is unavailable. First, time-lagged and rolling statistical features are extracted to capture the temporal dynamics of sensor signals. Then, a random forest-based feature importance algorithm is applied to identify and retain the most informative features, thereby reducing the influence of noise and redundancy. Finally, machine learning models are employed to perform data fusion and reconstruction across multiple sensors, enabling the integration of complementary information from heterogeneous sources. This methodological framework is designed to enhance the stability of individual sensor outputs, expand spatial coverage, and improve the overall representativeness of the environmental data.

![](images/b71a47806d43c968bbbe796032e75a306ab84aab0abba582704f74d69b959c1c.jpg)



![](images/0d710b1781d702271086345175dd9df446f74edcad43cebe04d1edb06bbcdc28.jpg)



Fig. 1. Motivations for QUIDS. (a) Deviations and variations of lowcost sensors over time. (b) Data fusions for improving sensing reliability, reproduced from [14].   
![](images/a29fc3f08af88fc536e75c01e56ae2df05bf3b7f31eb5d73514988f444b91a92.jpg)



Fig. 2. This figure illustrates how dispatching NVMCS in uneven sensing reliability setups can improve QoI by making the coverage optimal.

# B. System Models

The proposed dispatching system aims to enhance the QoI by optimizing sensing coverage while ensuring sensing reliability. To this end, the platform selects optimal routes for taxis to improve the system’s sensing coverage (as illustrated in Fig. 2) and allocates financial incentives to drivers to promote acceptance of dispatch assignments. While many existing dispatching systems tend to overlook the importance of sensing reliability, integrating this factor constitutes a novel contribution of our approach. We argue that an optimized spatiotemporal distribution—characterized by both balanced sensing coverage and reliable sensor performance—provides an effective and scalable solution. This design offers valuable insights for a wide range of real-world applications [8], [15]. The key notations used throughout this article are summarized in Nomenclature.

To efficiently capture and analyze the geographical area of interest, we adopt a discrete spatiotemporal representation in the form of a grid with dimensions $M \times N$ . Each cell in the grid is indexed by its coordinates $( x , y )$ , where $x \in { 1 , \ldots , M }$ and $y \in { 1 , \ldots , N }$ , , . . . ,correspond to longitude and latitude, respectively. , . . . ,The temporal dimension is similarly discretized into time slots of fixed duration dt minutes, with $t \in { 1 , \dots , T }$ indexing each time slot.

Within this grid-based map, a total of C vehicles are unevenly distributed and indexed by $c = 1 , \ldots , C .$ . Each vehicle , . . . ,is equipped with sensors capable of automatically collecting environmental data at every time slot t. For each vehicle $^ { c , }$ a set of candidate trajectories is defined as $R _ { c } ,$ , consisting of K distinct routing options. Each trajectory is represented as a 3-D tensor $\mathbf { r } _ { c } ^ { k } \in \bar { \mathbb { R } } ^ { M \times N \times T }$ , which encodes the vehicle’s spatial occupancy over the entire sensing period T . The trajectory ultimately selected for vehicle c from its candidate set $R _ { c }$ is denoted by $D _ { c }$ .

The proposed dispatch operation focuses on selecting the optimal trajectory from the set of possible traces $r _ { c } ^ { k } \in \mathsf { \Gamma }$ $R _ { c } ,$ , thereby modifying the spatiotemporal distribution of the dispatched vehicle. Each vehicle, denoted as c, has a default trajectory represented by $r _ { c } ^ { 0 } .$ , which corresponds to the vehicle’s path without any dispatch intervention. The vehicle trajectory $R _ { c }$ is generated by a mobility predictor adapted from [16]. Instead of operating directly on the raw road network, this method constructs a time-dependent landmark graph by mining historical trajectory data, thereby effectively encapsulating the collective driving intelligence of the driver population. Its core innovation lies in the introduction of a variance-entropy clustering algorithm, which accurately quantifies the volatility and uncertainty of travel time. This enables probabilistic modeling of time-varying traffic patterns and significantly improves the accuracy of trajectory prediction. During the online computation phase, the system employs a two-stage routing strategy upon receiving a query: first, it searches the landmark graph for a sequence of landmarks to form a coarse route, and then refines this route within the actual road network to produce the final drivable path. The formula for generating candidate vehicle trajectories from historical data is as follows:

$$
R _ {c} = \text { MobilPred } \left(\sum_ {c ^ {\prime} = 1} ^ {C} \mathcal {O} _ {c ^ {\prime}} ^ {\prime}\right) \tag {1}
$$

where MobilPred is the mobility predictor, $\mathcal { O } _ { c ^ { \prime } } ^ { \prime } \in M \times N \times$ $T ^ { \prime }$ represents the known historical trajectory of vehicle $c ^ { \prime } , T ^ { \prime }$ denotes the historical observation time horizon, and the set of historical vehicles $C ^ { \prime }$ may differ from the vehicle c whose trajectory is to be predicted.

To determine whether the scheduler selects vehicle c and assigns it a route, we introduce an indicator variable $I _ { c } ,$ defined as follows:

$$
I _ {c} = \left\{D _ {c} = = r _ {c} ^ {k} \right\} \in \{0, 1 \}. \tag {2}
$$

Dispatching nondedicated vehicles may interfere with their primary missions and incur additional incentive costs. When the dispatcher decides to modify a vehicle’s trajectory $( I _ { c } = 1 )$ , a corresponding incentive $a _ { c }$ is provided as compensation. The proposed incentivization scheme allocates incentives to individual vehicle agents to ensure their willingness to undertake assigned tasks, while keeping the total incentive expenditure within a predefined budget constraint, denoted as B

$$
\sum_ {c = 1} ^ {C} a _ {c} \cdot I _ {c} \leq B. \tag {3}
$$

Related studies in this field have investigated various compensation models aimed at incentivizing participation while minimizing disruptions to users’ routine activities [2], [17]. In Section IV, we further examine the impact of user acceptability on the effectiveness of the proposed dispatching scheme.

# C. Problem Formulation

To balance sensing reliability and sensing coverage, we propose a novel objective function termed ASQ. The ASQ formulation is inspired by prior work in the sensing coverage domain [15], [18], where entropy is employed to quantify the spatial evenness of sensor distribution. We extend this concept by integrating sensing reliability into the model. Sensing reliability is derived from the truth discovery paradigm [19], which characterizes sensor trustworthiness through a reliability factor $w _ { c } .$ . A higher value of $w _ { c }$ indicates a more reliable sensor, with $w _ { c } = 1$ representing average reliability. This framework enables the identification of sensors producing more trustworthy data, as well as those that may require additional vehicle dispatching or redundant readings for compensation. The ASQ is formulated as follows:

$$
\phi_ {w} \left(\mathcal {W}, D _ {c}\right) = (1 - \beta) E \left(\mathcal {W}, D _ {c}\right) + \beta \log Q \left(\mathcal {W}, D _ {c}\right) \tag {4}
$$

where $\beta$ is a parameter that controls the relative importance of two sensing reliability-aware factors: coverage evenness and coverage rate.

The first term $E ( \mathcal { W } , D _ { c } )$ represents the spatial entropy of ,the sensed regions. Entropy, a classic measure of uncertainty in information theory, increases as sensor coverage becomes more evenly distributed, thereby promoting fair and efficient allocation of sensing resources [20]. The second term log $Q ( \mathcal { W } , D _ { c } )$ is a coverage-quality function weighted by ,sensing reliability. The logarithmic transformation compresses the dynamic range of $Q ( \mathcal { W } , D _ { c } )$ to match the scale of the ,entropy term, enhancing numerical stability and ensuring effective weighting. Moreover, the log function naturally captures diminishing returns in coverage improvement, preventing the algorithm from over-optimizing areas that already exhibit high coverage [21].

The entropy of the spatial distribution of sensed areas, denoted as $E ( \mathcal { W } , D _ { c } )$ , is computed as

$$
E \left(\mathcal {W}, D _ {c}\right) = - \sum_ {x, y, t, \mathcal {W}} P (x, y, t, \mathcal {W}) \log P (x, y, t, \mathcal {W}). \tag {5}
$$

The higher the entropy, the more evenly the sensors are distributed across the area, which results in better sensing coverage. We define $P ( x , y , t , \mathcal { W } )$ as the aggregated sum of , , ,variance factors within the trajectory, calculated as

$$
P (x, y, t, \mathcal {W}) = \frac {\sum_ {c = 1} ^ {C} w _ {c} D _ {c} (x , y , t)}{C T}. \tag {6}
$$

This equation defines the probability distribution of vehicle agents, where $D _ { c } ( x , y , t )$ indicates the presence of vehicle c at location $( x , y )$ , , and time t, and $w _ { c }$ denotes the weight ,associated with vehicle c. The sensing reliability, represented by $w _ { c } ,$ acts as a weighting factor that reflects the distribution of sensing trustworthiness across the spatiotemporal domain, thereby enabling the system to prioritize reliable coverage. The size of sensed areas, $Q ( \mathcal { W } , D _ { c } )$ , is calculated simply as

$$
Q (\mathcal {W}, D _ {c}) = \left| (x, y, t): P (x, y, t, \mathcal {W}) > \frac {1}{C T} \right| \tag {7}
$$

where Q(W Dc) represents the size of the sensed areas in the ,grid map where the net sensing reliability exceeds the average sensing reliability for a sensor.

The use of a weighted aggregate sum in (6) is motivated by its intuitive and generalizable ability to quantify sensing reliability. This formulation captures both the spatial evenness of sensor distributions and the individual reliability of each sensing agent. While the current model is designed to align with a weighted average data fusion approach, future work may investigate its integration with more advanced data fusion algorithms

$$
\max_{\substack{c = 1,\ldots ,C\\ k = 1,\ldots ,K}}\phi \left(\mathcal{W},D_{c}\right) = (1 - \beta)E\left(\mathcal{W},D_{c}\right) + \beta \log Q\left(\mathcal{W},D_{c}\right)
$$

$$
\text { subject   to } \left\{ \begin{array}{l} D _ {c} = r _ {c} ^ {k}, k \in \{1, 2, \dots , K \} \\ I _ {c} \in \{0, 1 \} \\ \sum_ {c = 1} ^ {C} a _ {c} \cdot I _ {c} \leq B. \end{array} \right. \tag {8}
$$

The objective function aims to maximize ASQ by balancing the entropy of sensor distributions and the extent of the sensed areas, both weighted by sensing reliability. In addition, the model incorporates physical mobility constraints related to vehicle scheduling, along with a budgetary constraint. This optimization problem is NP-hard, involving the combinatorial selection of discrete variables (Ic) and the continuous adjustment of reliability weights $( w _ { c } )$ . It features a nonlinear objective function $\phi _ { w }$ and a linear constraint $\sum a _ { c } \cdot I _ { c } \leq B$ .

φThe novelty of this formulation lies in its simultaneous integration of sensing reliability and sensing coverage as core components of vehicular sensing performance. By embedding both factors into a unified framework, the model enables the joint optimization of sensor deployment and measurement fidelity.

# III. ALGORITHM DESIGN

In this section, we present our proposed dispatching framework for improving QoI by optimizing ASQ. The algorithm consists of three key steps: online sensing reliability inference, monetary incentive mechanism, and mutually assisted beliefaware vehicle dispatching (shown in Fig. 3). The first step focuses on deriving the reliability of sensors operating within a common spatial domain (Section III-A). The second step quantifies the monetary incentives required for vehicle dispatching (Section III-B). The third step integrates the inferred sensing reliability with the calculated monetary incentives to inform the vehicle dispatching process (Section III-C). These steps form an iterative loop, where mutually assisted beliefaware vehicle dispatching also contributes to improvements in both online sensing reliability inference and monetary incentive mechanisms. Finally, we analyze the algorithm’s time complexity in Section III-D.

![](images/32718498b486f070abc0b2980625f554014156eb3e98fdd8952c1c539d1c0c5a.jpg)



Fig. 3. This figure shows our proposed algorithm’s framework.

# A. Online Sensing Reliability Inferring

In our framework, we adopt the concept of truth discovery [19] to model the sensing reliability of sensors using the reliability factor $w _ { c }$ . Truth discovery is a technique that infers the sensing reliability of sensors by comparing their measurements $m _ { c } ^ { ( x , y , t ) }$ with the inferred truth m(x,y,(∗) $m _ { ( * ) } ^ { ( x , y , t ) }$ , derived from other sensors in correlated sensing scenarios. However, in real-world sensing, different sensors often exhibit consistent deviations from the true value, leading to bias. This bias can significantly affect the data fusion results, particularly if all sensors dispatched to a single location share the same direction of bias, such as underestimating the true value. To address this challenge and account for systematic errors, we enhance the truth discovery approach by introducing a bias term $b _ { c }$ and reformulating the optimization function as follows:

$$
\begin{array}{l} \min _ {\mathcal {M}, \mathcal {W}, \mathcal {B}} f (\mathcal {M}, \mathcal {W}, \mathcal {B}) \\ = \sum_ {x, y, t} \left\{\sum_ {c = 1} ^ {C} w _ {c} \left\| m _ {(*)} ^ {(x, y, t)} - m _ {c} ^ {(x, y, t)} + b _ {c} \right\| ^ {2} \right\} \\ \end{array}
$$

$$
\text { s.t. } \quad \sum_ {c = 1} ^ {C} \exp (- w _ {c}) = 1, \sum_ {c = 1} ^ {C} b _ {c} = 0. \tag {9}
$$

In this optimization function, we aim to minimize the weighted sum of the differences between the inferred truth $m _ { ( * ) } ^ { ( x , y , t ) }$ m ,(∗) and the observed measurements $m _ { c } ^ { ( x , y , t ) }$ , while accounting for the bias terms $b _ { c }$ . The objective is to reduce the overall discrepancy between the aggregated truth and the bias-adjusted, reliability-weighted sensor readings. The first constraint limits the range of the weights to prevent them from becoming arbitrarily large or approaching negative infinity. The second constraint ensures that the bias terms do not dominate or nullify the influence of all sensor readings.

To infer sensing reliability, we formulate the optimization problem as described in (9). We adopt an approach similar to that of [19], employing Lagrange multipliers to solve the constrained optimization. The goal is to estimate the reliability values for each sensor accurately. By applying Lagrangian optimization, we derive the following equations:

$$
\mathcal {M}: m _ {(*)} ^ {(x, y, t)} = \frac {\sum_ {c = 1} ^ {C} w _ {c} \left(m _ {c} ^ {(x , y , t)} - b _ {c}\right)}{\sum_ {c = 1} ^ {C} w _ {c}} \tag {10}
$$

$$
\mathcal {W}: w _ {c} = - \log \frac {\sum_ {(x , y , t)} \left\| m _ {(*)} ^ {(x , y , t)} - m _ {c} ^ {(x , y , t)} + b _ {c} \right\| ^ {2}}{\sum_ {(x , y , t)} \sum_ {c ^ {\prime} = 1} ^ {C} \left\| m _ {(*)} ^ {(x , y , t)} - m _ {(c ^ {\prime})} ^ {(x , y , t)} + b _ {c ^ {\prime}} \right\| ^ {2}} \tag {11}
$$

$$
\mathcal {B}: b _ {c} = \frac {\sum_ {x , y , t} \left(m _ {c} ^ {(x , y , t)} - m _ {(*)} ^ {(x , y , t)}\right)}{\| r _ {c} (x , y , t) \neq 0 \|}. \tag {12}
$$

These equations facilitate the inference of sensing reliability values for individual sensors based on their measurements and the corresponding calculated weights.

Algorithm 1 Online Sensing Reliability Inference   
Input : sensing value of all sensors in a given time period $m_{c}^{(x,y,t)}$ , $c \in C$ , error bound $\epsilon$ , past outputs $(m_{(*)'}^{(x,y,t)}, w_{c}^{\prime}, b_{c}^{\prime})$ Output: updated data quality estimates $w_{c}$ , $b_{c}$ , and inferred truth $m_{(*)}^{(x,y,t)}$ 1 Split the sensors into clusters based on their location, so that $s_{(x,y,t)} = \{c \mid s_{c} = (x, y, t)\}$ ;

2 Initialization: Set Lagrangian factor $\lambda = 0$ ;

3 while error > $\epsilon$ do

4 $\lambda \leftarrow \lambda + \sum_{c \in s_{(x,y,t)}} (m_{(*)}^{(x,y,t)} - m_{c}^{(x,y,t)})^{2}$ ;

5    for $(x, y, t) \in (M, N, T)$ do

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

Algorithm 1 is designed to estimate the reliability factor $w _ { c }$ and constant bias $b _ { c }$ of each sensor in real-time, using the inferred truth ( $( m _ { ( * ) } ^ { ( x , y , t ) } )$ m(x,y,t)(∗) ) for all sensors over a given time period.

The algorithm takes as input the sensing values, error bound $\epsilon ,$ and previous outputs $( m _ { ( * ) ^ { \prime } } ^ { ( \bar { x } , y , t ) } , w _ { c } ^ { \prime } , b _ { c } ^ { \prime } )$ , and returns the updated data quality estimates $( w _ { c } , b _ { c } )$ , along with the updated inferred truth (m , ,(∗) $( m _ { ( * ) } ^ { ( x , \bar { y } , t ) } )$ (x y t)).

For each spatiotemporal cell (x y t), the algorithm iterates , ,over all sensors within the corresponding cluster $\boldsymbol { s } _ { ( x , y , t ) }$ to update their data quality estimates $( w _ { c }$ and $b _ { c } )$ . Equations (11) and (12) are employed to perform this update. Subsequently, the inferred truth is updated using (10), based on the newly updated data quality estimates. These equations incorporate past outputs $( \dot { m } _ { ( * ) ^ { \prime } } ^ { ( x , y , t ) } , w _ { c } ^ { \prime } , b _ { c } ^ { \prime } )$ as parameters in the summation, , ,effectively leveraging historical data to inform the update process.

The belief in the sensing reliability inference is naturally derived from (11). From this equation, we observe that the value of w can be expressed as w ∝ log $k \cdot d ( m _ { ( * ) } ^ { ( x , y , t ) } , m _ { c } ^ { ( x , y , t ) } - b _ { c } )$ (x,y,t) m(x,y,t) − b ), ,where k refers to the vehicles that participate in the measurement aggregation. Based on this, we define the belief of the estimate $\varepsilon _ { c }$ as follows:

$$
\varepsilon_ {c} = \log \left(\sum_ {\substack {i = 1 \\ i \neq c}} ^ {C} \sum_ {t = 1} ^ {T} \mathbf {r} _ {c} ^ {k} (t) \cdot \mathbf {r} _ {i} ^ {k} (t)\right). \tag{13}
$$

Here, $\mathbf { r } _ { c } ^ { k } ( t )$ is the kth trajectory of vehicle c. The product of the two tensors represents the overlap of the trajectories between all vehicles. By summing over all vehicles and time slots, we obtain the total number of vehicles that have an overlapping trajectory with vehicle $c .$ Taking the logarithm of this total yields the belief signal $\varepsilon _ { c }$ . If there is no overlap between another vehicle and c, the belief $\varepsilon _ { c }$ equals 0, indicating that εthe inferred sensing reliability for vehicle c is low.

# B. Monetary Incentive Calculating

We allocate incentives to the dispatched vehicles to ensure their willingness to perform the assigned tasks, while adhering to the budget constraints on total incentives. The utility of each vehicle is defined as its expected future returns. Given a potential scheduled trajectory $D _ { c } ^ { r }$ , the incentive $a _ { c }$ is designed to compensate for the utility loss incurred by the vehicle when accepting rather than rejecting $D _ { c } ^ { r } .$ . Since vehicles inherently seek to maximize their utility, this approach guarantees their acceptance of the proposed incentive.

The core of the incentive design lies in accounting for the probability of vehicle agents receiving new task requests at their destinations. Since the primary objective of vehicle agents is to identify potential customer requests, the likelihood of obtaining ride requests at the assigned destination plays a critical role in their decision to accept a dispatched task. Therefore, the key challenge in designing the incentive mechanism is to develop a dynamic and differentiated pricing strategy under a limited budget that accurately compensates drivers for the opportunity costs and risks associated with accepting certain tasks, particularly those directed to lowdemand areas. By doing so, the mechanism effectively enlarges the feasible region of the optimization model, transforming driver behavioral uncertainty into a tractable component of the solution space. This enables more flexible and efficient task assignment, ultimately maximizing both the system scheduling success rate and sensing coverage.

We adopt the model discussed in [22], which predicts the number of ride requests at various locations and times within the city based on historical task request data. This prediction enables the system to effectively match ride requests with available vehicles, allowing the deployment of more vehicles within the same budget, thereby enhancing the quality of sensing coverage.

Algorithm 2 Monetary Incentive Mechanism   
Input : estimated original trajectory of all vehicles $r_{c}^{0}$ , a potential dispatch trajectory $r_{c}^{k} \in R_{c}$ , ride request predict $Q^{(x,y,t)}$ , scheduling period T, $\{r_{min}, r_{max}\}$ Output: monetary incentive $a_{c}$ 1 Initialization: Set $a_{c} = r_{min}$ , t = 0;

2 for $t++ \leq T$ do

3 Calculate $Q_{c}^{0}$ by (15);

4 Calculate $Q_{c}^{r}$ by (16);

5 Calculate $a_{c}$ by (14);

6 end

Algorithm 2 is designed to calculate the incentives required for potential dispatch trajectories within a given period. Let $Q ^ { ( x , y , t ) } \in [ 0 , 1 ]$ denote the probability that a vehicle located ,at a specific spatial position (x y) at time t will receive at ,least one task request. This probability is approximated by the ratio of the number of task requests to the number of idle vehicle agents within the grid. If this ratio exceeds 1, the task request probability is capped at 1. Next, we define $r _ { \mathrm { m a x } }$ as the maximum monetary incentive typically accepted by the dispatch platform. Let the dispatching period be denoted as T , and define $r _ { u } = r _ { \operatorname* { m a x } } / T$ as the utility at each time point. In addition, for all vehicles, the incentive has a lower bound, $r _ { \mathrm { m i n } }$ , to ensure that the incentives provided are not negligible. Based on these considerations, we design the incentive $a _ { c }$ to encourage vehicle agent c to accept the potential assigned trajectory $D _ { c }$

$$
a _ {c} = \max \left(\min \left(r _ {\max}, r _ {\max} - r _ {u} \cdot \left(Q _ {c} ^ {r} - Q _ {c} ^ {0}\right)\right), r _ {\min}\right) \tag {14}
$$

$$
Q _ {c} ^ {0} = \sum_ {x, y} Q ^ {(x, y, t)} r _ {c} ^ {0} \tag {15}
$$

$$
Q _ {c} ^ {r} = \sum_ {x, y} Q ^ {(x, y, t)} D _ {c}. \tag {16}
$$

Here, $Q _ { c } ^ { 0 }$ represents the expected number of ride requests that vehicle c can receive during period T along its original trajectory $r _ { c } ^ { 0 } ,$ while $Q _ { c } ^ { r }$ represents the expected number of ride requests that c can receive during T along the trajectory $D _ { c }$ . The incentive $a _ { c }$ is constrained within the range $[ r _ { \operatorname* { m i n } } , r _ { \operatorname* { m a x } } ]$ . Based on the number of ride requests along the vehicle’s original trajectory, if the scheduled trajectory $D _ { c }$ enables vehicle agent c to discover more task requests, the increase in request probability is treated as an implicit incentive, with lower monetary compensation considered. Conversely, higher compensation is provided to ensure the vehicle is willing to accept the scheduled task.

Algorithm 3 Mutually Assisted Belief-Aware Vehicle Dispatching   
input : estimated original trajectory of all vehicles $r_{c}^{0}$ , possible trace set of vehicle $R_{c}$ ,
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
17 $c = c \rightarrow next;$ 18    end
19    Select ( $c', k'$ ) = arg max $_{c,k} V(r_{c}^{k*}, P)$ ;

20    if $k' > 0$ then
21 $D_{c} = r_{c}^{k*}$ ;

22    Update $S^{*} = \{I_{c}, D_{c}, B_{c}\}$ , $B_{c}$ and $\varepsilon_{c}$ ;

23    else
24 $I_{c'} = 0$ , $B_{c} = 0$ ;

25    end

26 end

# C. Mutually Assisted Belief-Aware Vehicle Dispatching

Algorithm 3 is designed to enhance the QoI by strategically dispatching vehicles to maximize the ASQ. In this framework, collaborative sensing reliability is inferred through the aggregation of data from multiple sensors operating within overlapping spatial regions, while monetary incentives are computed based on the predicted ride request densities at various destinations. By exchanging information and sharing resources, sensors and vehicles mutually assist one another, thereby improving both the reliability of the collected data and the operational efficiency of the dispatching process. Prior to initiating the scheduling procedure, the data request end provides the scheduling period T and the monetary budget B. Upon completion of the scheduling, the algorithm returns the improved vehicle coverage and updated belief to the data request end. During the scheduling period T , the total monetary incentives allocated must not exceed the available budget B.

In contrast to previous work [9], our approach explicitly accounts for sensing reliability and its inference, rather than assuming uniform reliability across all vehicles. We prioritize vehicles with overlapping trajectories, as they are more likely to provide accurate inferred sensing reliability. These vehicles are then dispatched to less populated areas, thereby enhancing both data collection and the reliability of the inferred sensing. To ensure that vehicles are willing to accept the scheduling, we offer incentive-based compensation, guaranteeing that their total earnings after dispatch are no less than those from executing their original trajectories.

Once the scheduling is accepted, dispatching is carried out to improve sensing coverage with respect to sensing reliability, employing a V value-based approach. This optimization enhances both overall data coverage and the quality of the collected information. The calculation of the V value is given by

$$
V _ {c} \left(r _ {c} ^ {k}, P\right) = - \frac {\sum_ {x , y , t} w _ {c} \cdot r _ {c} ^ {k} \cdot P (x , y , t , \mathcal {W})}{\sum_ {x , y , t} P (x , y , t , \mathcal {W})}. \tag {17}
$$

Here, $r _ { c } ^ { k }$ denotes either the selected trajectory of the current vehicle or the predicted trajectory generated by the mobility predictor. The term $w _ { c }$ represents the reliability factor, while $P ( x , y , t , \mathcal { W } )$ denotes the aggregated variance factor along the , , ,trajectory.

# D. Time Complexity Analysis

To analyze the complexity of our algorithm, we focus on the time complexity of each individual step. The initialization step has a time complexity of O(C), where C is the number of vehicles, since each vehicle needs to be initialized. The calculation step has a time complexity of $\mathcal { O } ( C T ^ { 4 } )$ , as we need to compute the sensing quality for each pair of vehicles. The trajectory size is estimated to have a complexity of $\mathcal { O } ( T ^ { 4 } )$ , based on the use of the Bellman–Ford algorithm for trajectory optimization. Therefore, the overall time complexity of our algorithm is O(CT 4).

# IV. EVALUATION

We present an evaluation of QUIDS through simulated dispatching and map reconstruction experiments using realworld data. The experimental setup uses data collected from a real-world deployment of the NVMCS system, combined with large-scale simulation-based scheduling to validate its performance (Section IV-A). We analyze how the ASQ varies with different factors and demonstrate the advantages of QUIDS over baseline approaches (Section IV-B). In addition, we assess the effectiveness of the ASQ metric by exploring its relationship with downstream tasks (Section IV-C). Finally, we validate the efficacy of our proposed dispatching algorithm through an ablation study (Section IV-D).

# A. Experiment Setup

1) Real-World Data Collection and Processing: We deployed mobile sensors in 29 taxis to collect data over a twomonth period in a large city, capturing environmental variables such as humidity, temperature, $O _ { 3 }$ , and particulate matter (see Fig. 4). Real-time GPS location data from the taxis, along with accurate sensor readings, were recorded every 3 s. The data underwent preprocessing, including outlier removal and imputation of missing values using a sliding window approach with a window size of 5 min.

![](images/2ae0378d1ad3f2632ac4bc5b0c5873859e77fef8f2bbc4ad6f225d8345f907cf.jpg)



Fig. 4. Sensor platform deployed in our taxi, features a GPS receiver, a gas prompt, and four slacks capable of sensing various physical factors across the city.

2) Simulation Environment Configuration: To replicate a real-world scenario, we selected a specific area with relatively dense vehicle trajectories, corresponding to a $1 5 \times 8 ~ -$ km grid in the city. The spatial resolution was set to 1 km, consistent with typical air pollution monitoring setups [23], [24]. The temporal resolution (i.e., time period dt) was set to 2 min, and the actuation period was set to 5T (10 min), representing the average time for a taxi to travel 4 km, thereby ensuring that air quality conditions remained stable during the dispatching simulations. Due to factors such as water bodies, nature reserves, or administrative borders, 42 grid cells were not covered by any mobile sensor and were marked as excluded areas, and thus excluded from the performance metric calculations.

3) Virtual Taxi Fleet Modeling: To simulate a large taxi fleet and analyze their trajectories, we utilized GPS data to extract the movement patterns of each vehicle. These trajectories reflect actual taxi movements without any incentivized dispatching. To expand the simulation to include 200 virtual taxis, we adjusted the mobility patterns and spatial distribution of the original trajectories, thereby enhancing coverage. This approach allowed us to assess the behavior and sensing coverage of a larger taxi fleet without the need for additional physical vehicles.

During the dispatching process, we set the monetary budget to B = U.S. 400, assumed zero mobility prediction error, and set the dispatch acceptance rate to 100%. Considering the city taxi flag-down fare of U.S. 2, we defined the cost parameters as $r _ { u } = \mathrm { U } . S$ . 2/min, with $r _ { \mathrm { m i n } } = \mathrm { U } . S . \ 2$ 2 and $r _ { \operatorname* { m a x } } = \mathrm { U } . S . ~ 2 0$ . The first six weeks of data were used to train the mobility prediction and ride request models, while the remaining data were reserved for testing the proposed method.

4) Large-Scale Sensing Simulations: To simulate low-cost sensors with controllable sensing errors, we focus on evaluating the $O _ { 3 }$ data from our dataset, as low-cost sensors for $O _ { 3 }$ typically exhibit considerable variability in measurement accuracy and reliability. Given the availability of multiple relevant datasets, we leverage publicly accessible calibration data to model this variability. Specifically, we extract error distributions from established low-cost $O _ { 3 }$ sensor calibration datasets [25], [26], which provide detailed characterizations of the error profiles across different sensor types. These error distributions are subsequently applied to our fine-grained sensing resulting maps, ensuring that the simulated sensor types are consistent with those deployed in real-world scenarios.

To generate realistic sensor readings, we introduce sensing errors based on the extracted error distributions. These errors are systematically incorporated into the ground truth values of the sensor grid, thereby simulating the impact of lowcost sensors on both measurement accuracy and precision. By modeling sensing errors in this manner, we can rigorously evaluate the performance of our dispatching system under realistic sensing conditions, thereby closely approximating the challenges encountered in real-world low-cost sensor deployments.

5) Baselines Methods for Comparison: Six baseline methods are adopted to evaluate the improvement in the ASQ metric achieved by QUIDS as follows.

1) No Actuation: This baseline refrains from any vehicle dispatch, serving as a passive reference to quantify the performance gain enabled by proactive scheduling.

2) Prediction-Based Actuation System: A predictive incentive system that anticipates vehicle trajectories and order demand to proactively optimize sensing coverage under a limited budget [8].

3) State-Aware Hybrid Incentive Program: A taxi dispatching scheme incorporating fine-grained vehicle state classification and a hybrid opportunity–participation incentive model to improve sensing diversity while aligning platform and driver interests [27].

4) Vehicle-Assisted Data Sensing Algorithm: A coalitional sensing framework based on Stackelberg game theory and Nash equilibrium optimization, designed to balance economic incentives and resource allocation across multiple operators and vehicles [28].

5) Vickrey–Clarke–Groves-Based Mobile Sensing Tasks: An enhanced auction mechanism integrating Vickrey–Clarke–Groves pricing with staggered scheduling and budget awareness to jointly guarantee passenger service quality and sensing task allocation [29].

6) Quality-Informed Multiagent Dispatching System (QUEST): A system jointly captures sensing coverage and reliability to handle uncertain, time-varying vehicle states [1].

7) Graph Convolutional Cooperative Multiagent Reinforcement Learning: A multiagent reinforcement learning approach using graph convolutional networks for distributed cooperative route planning, balancing passenger orders and sensing tasks [10].

6) Performance Metrics and Evaluation Protocol: We first utilize the ASQ metric, as defined in Section II-C, to evaluate the performance of various dispatching algorithms. To assess the real-world impact of ASQ and these dispatching strategies, we investigate their effects through a downstream task in mobile crowdsensing: map reconstruction. Map reconstruction involves generating a comprehensive representation of environmental data across a grid map, based on the measurements

collected by dispatched vehicles. For this task, we employ three distinct map reconstruction algorithms: linear interpolation, Gaussian process regression, and Bayesian Gaussian CANDECOMP/PARAFAC (BGCP) [30]. Each of these methods provides a different approach to filling in the gaps between sensor measurements, ensuring that the reconstructed map reflects the underlying environmental conditions as accurately as possible.

To evaluate the effectiveness of the map reconstruction process, we primarily use the reconstructed root-mean-square error (R-RMSE) metric. The R-RMSE quantifies the accuracy of the reconstructed map by comparing it to the ground truth. Lower R-RMSE values indicate better performance, meaning that the reconstructed map more closely aligns with the actual environmental conditions. This metric serves as a key indicator of the overall effectiveness of the dispatching strategies in terms of improving the quality and reliability of the reconstructed environmental maps.

# B. Evaluation for QUIDS

To evaluate the potential real-world impact of various dispatching algorithms, we introduce the error reduction rate (Err. Reduction), a metric that quantifies the maximum reduction in R-RMSE across all map reconstruction algorithms. This metric allows us to assess the improvements in map reconstruction accuracy achieved by each dispatching approach. Specifically, Err. Reduction represents the relative decrease in reconstruction error due to the deployment of the dispatching algorithm, with higher values indicating better algorithm performance.

Table I presents a comparative analysis of the performance of various dispatching algorithms in terms of the ASQ metric and downstream field reconstruction tasks. The experimental results demonstrate that QUIDS achieves the best performance across all evaluated aspects, including the ASQ score, the R-RMSE for three different field reconstruction algorithms, and the Err. Reduction. Specifically, QUIDS improves the ASQ metric by 38.02% compared to the no actuation (NA) method, and by 9.61%, 5.87%, 15.26%, 4.88%, and 6.48% relative to prediction-based actuation system (PAS), state-aware hybrid incentive program (SHIP), vehicle-assisted data sensing algorithm (VADS), Vickrey–Clarke–Groves-based mobile sensing task (VCG-MST), and graph convolutional cooperative multiagent reinforcement learning (GCC-MARL), respectively. In terms of Err. Reduction, QUIDS achieves a 75.4% reduction compared to NA, significantly outperforming the second-best method, SHIP, which attains a 58.67% reduction. These results fully demonstrate the effectiveness and superiority of the QUIDS algorithm among state-of-the-art solutions. Furthermore, the differences in R-RMSE and Err. Reductions across the algorithms reflect the inherent tradeoffs and advantages associated with enhancing sensing coverage and improving the accuracy of map reconstruction.

To further assess QUIDS under varying dispatching budgets, we plot ASQ against different budget levels in Fig. 5(a). Our proposed QUIDS consistently outperforms both baseline algorithms across all budget amounts. As the number of scheduled vehicles increases, QUIDS exhibits a more pronounced improvement compared to the PAS, achieving up to a 14.0% enhancement with a U.S. 200 budget. This improvement can be attributed to QUIDS’s ability to incorporate sensing reliability, thereby allowing for more effective allocation of the dispatching budget to maximize coverage. However, as the budget increases further, the advantage of QUIDS diminishes. This trend is expected, as the distribution of vehicles becomes increasingly dense, causing QUIDS to approach its performance ceiling when most vehicles are dispatched to already covered areas.

TABLE I PERFORMANCE BY DIFFERENT DISPATCHING AND RECONSTRUCTION ALGORITHMS 

<table><tr><td>Algorithm</td><td>NA</td><td>PAS</td><td>SHIP</td><td>VADS</td><td>VCG-MST</td><td>QUEST</td><td>GCC-MARL</td><td>QUIDS</td></tr><tr><td>ASQ</td><td>4.05</td><td>5.10</td><td>5.28</td><td>4.85</td><td>5.33</td><td>5.37</td><td>5.25</td><td>5.59</td></tr><tr><td>Linear R-RMSE ( $\mu g/m^3$ )</td><td>49.72</td><td>28.90</td><td>37.67</td><td>25.85</td><td>17.41</td><td>26.49</td><td>23.84</td><td>24.16</td></tr><tr><td>GPR R-RMSE ( $\mu g/m^3$ )</td><td>39.25</td><td>28.81</td><td>27.51</td><td>21.59</td><td>13.35</td><td>26.48</td><td>19.23</td><td>23.93</td></tr><tr><td>BGCP R-RMSE ( $\mu g/m^3$ )</td><td>26.24</td><td>12.24</td><td>20.03</td><td>13.09</td><td>8.13</td><td>9.27</td><td>11.56</td><td>6.45</td></tr><tr><td>Err. Reduction (%)</td><td>-</td><td>53.32</td><td>58.67</td><td>50.12</td><td>69.32</td><td>64.6</td><td>55.96</td><td>75.4</td></tr></table>

![](images/f8c3d53eb8be11dbb3026a3f64f993714bbf7dfc5821977457ab649f007e174a.jpg)



(a)

![](images/a17835b51cadb5a6f320453556c72a7ac12fb66e94420f7724c2e94acd357c02.jpg)



(b)

![](images/43bb16e01f5d456edbcb93c5ba660cf9c4c6b832b5cb017677f94edb7f28f622.jpg)



（c）

![](images/84199009a90c05e6bee775d8dd79f2d2b4607bc40ebd8d7de77dcb71b4665cc7.jpg)



(d)   
Fig. 5. Performance of QUIDS under different factors. (a) ASQ versus budget. (b) ASQ versus M. Pred. Error. (c) ASQ versus user acceptance. (d) ASQ versus error level.

We investigate the influence of mobility prediction errors on various dispatching algorithms by introducing random errors with varying degrees of Euclidean distance bias [31]. As shown in Fig. 5(b), QUIDS demonstrates robustness across different levels of mobility prediction accuracy. Although ASQ decreases with increasing prediction error, QUIDS consistently outperforms the benchmark methods in most scenarios.

In practice, some vehicles may decline incentives due to unforeseen circumstances, lack of awareness, or individual preferences. To evaluate the impact of user acceptance rates on QUIDS performance, we model the acceptance rate as the probability that each vehicle agent will accept a task after receiving the proposed incentive strategy. We conducted 1000 acceptance trials for each acceptance rate. Fig. 5(c) illustrates QUIDS’s performance across different time periods, with acceptance rates ranging from 60.0% to 100.0%. QUIDS consistently outperforms PAS, achieving higher ASQ scores and more effectively optimizing sensor coverage and reliability, even at lower acceptance rates.

To investigate the impact of varying degrees of sensing error on ASQ, we introduce controlled sensing errors by adding Gaussian noise, with the error level determined by the standard deviation. As illustrated in Fig. 5(d), the relationship between sensing error levels and ASQ is complex and algorithm-dependent. In certain cases, the ASQ value remains relatively stable or even slightly increases despite an increase in sensing error variance. This phenomenon occurs because ASQ primarily reflects the relative errors between different sensors, making it less sensitive to absolute changes in the sensing error.

Fig. 6 visualizes the dispatching outcomes based on ASQ. Both PAS and QUIDS dispatch vehicles from densely populated areas to sparsely populated regions. The overall sensing reliability is quantified using the mean absolute error over sensed area (S-MAE) over the sensed area. Notably, QUIDS demonstrates the lowest sensing error and the highest coverage among the evaluated algorithms, highlighting its effectiveness in balancing both sensing reliability and sensing coverage. Furthermore, an analysis of the spatial error distribution reveals that QUIDS significantly reduces errors in areas that are poorly covered by NA or PAS. This improvement can be attributed to QUIDS’s strategy of selecting vehicles with higher net sensing reliability, thereby generating more accurate and reliable data compared to NA or PAS.

# C. Evaluation for ASQ

Fig. 7 illustrates the relationship between ASQ and R-RMSE under varying experimental conditions, including different times, budgets, and algorithms. Each point represents a single round of simulation-based dispatching. This analysis underscores the critical role of ASQ in evaluating QoI for downstream tasks, particularly map reconstruction.

The experimental results reveal a clear negative correlation between ASQ and R-RMSE: higher ASQ scores generally correspond to lower R-RMSE values, indicating higher QoI during the map reconstruction process. This consistent association confirms that ASQ effectively quantifies the core concept of QoI and translates it into a measurable system-performance indicator. Although R-RMSE may vary at the same ASQ level due to differences in reconstruction algorithms and statistical fluctuations, this does not diminish ASQ’s function as a practical bridge between the qualitative notion of QoI and its quantitative assessment in system evaluation.

![](images/8f8e60218ce16a37436e2e5d25de729491099814cad862f76f85f3c8f022ff23.jpg)



Fig. 6. Sensing error after dispatching. Here, we zoomed in on a typical area affected by dispatching algorithms. QUIDS expanded the sensing coverage without the loss of sensing reliability.

![](images/90eb8f907acabcc69ef83c7c9707e79c0f9b6aa9073db181e206d53c9e32bd95.jpg)



Fig. 7. ASQ shows negative correlations with R-RMSE, among all different reconstruction algorithms.

TABLE II ABLATION STUDY 

<table><tr><td>Algorithm</td><td>QUIDS-NoRe</td><td>QUIDS-NoIn</td><td>QUIDS</td></tr><tr><td>ASQ</td><td>5.30</td><td>5.37</td><td>5.59</td></tr><tr><td>Linear RMSE ( $\mu g/m^{3}$ )</td><td>27.53</td><td>26.49</td><td>24.16</td></tr><tr><td>GPR RMSE ( $\mu g/m^{3}$ )</td><td>26.40</td><td>26.48</td><td>23.93</td></tr><tr><td>BGCP RMSE ( $\mu g/m^{3}$ )</td><td>10.58</td><td>9.27</td><td>6.45</td></tr><tr><td>Error Reduction (%)</td><td>59.7</td><td>64.6</td><td>75.4</td></tr></table>

# D. Ablation Study

We conducted an ablation study to assess the contributions of online sensing reliability inference and monetary incentive calculation to the overall performance of QUIDS. The configuration QUIDS-NoRe omits the sensing reliability inference, where all sensors are assigned a uniform reliability level. In contrast, QUIDS-NoIn excludes the monetary incentive calculation, resulting in identical incentives for all scheduled vehicles.

![](images/103b836b37d0770016000c89fccdda4cc94f917396346b0fcca0601a65a6a7dc.jpg)



![](images/18fc45afc7fa173b42586c520e33497df19d5a1637f50e8ab61f784a5b2e0472.jpg)



Fig. 8. These figures visualize the relations between the generated error and inferred reliability factor. QUIDS utilizes mutually assisted dispatching to acquire a more accurate inference. (a) Inferred w by QUIDS-NoRe. (b) Inferred w by QUIDS.

Table II presents the results of this ablation study. We observe that both QUIDS-NoRe and QUIDS-NoIn achieve higher ASQ values than the baselines shown in Table I; however, their performance still falls short of the full QUIDS configuration. This performance gap arises because QUIDS-NoRe does not accurately infer sensing reliability, which limits its ability to leverage optimal vehicle scheduling for error reduction. Similarly, QUIDS-NoIn fails to effectively allocate incentives, leading to a reduced number of vehicles available for scheduling. Both configurations highlight the critical importance of these two components within the QUIDS framework.

Fig. 8 illustrates the relationship between the inferred reliability factor w and the resulting sensing error across different regions. For this analysis, we selected three sectors with varying numbers of vehicle agents. In Fig. 8(a), we present the results of reliability inference using QUIDS-NoRe. While the inferred sensing reliability captures some aspects of the induced errors, the local aggregation of measurements introduces biases. These biases can cause well-performing sensors to receive lower w values due to discrepancies in the aggregated measurements. In contrast, Fig. 8(b) shows how mutually assisted dispatching enhances reliability inference. Despite minor deviations caused by inherent randomness, the results remain consistent, accurately classifying the sensing reliability of each sensor.

# V. DISCUSSIONS

We discussed the potential applications and future directions of QUIDS, while also highlighting its current limitations. Specifically, these include its generalizability to other NVMCS applications (Section V-A), the potential for improving its incentive model (Section V-B), and its dependence on accurate mobility predictions (Section V-C).

# A. Generalization to Other NVMCS Applications

Although QUIDS was originally developed for air pollution sensing, its underlying principles are generalizable to a wide range of NVMCS tasks. For instance, QUIDS can be adapted for applications such as wireless signal sensing, noise pollution mapping, and other environmental monitoring tasks. The system’s spatial granularity can be adjusted to meet the specific needs of these applications. However, since QUIDS’s reliability inference model is based on truth discovery, which assumes that the data originates from the same modality, it may face challenges in scenarios that require cross-modality data fusion for sensing reliability [32], [33]. To extend QUIDS for such cases, further design modifications would be necessary to integrate and harmonize data from different sensor modalities.

# B. Exploring Alternative Incentive Models

QUIDS currently uses a simple incentive model, but the introduction of alternative incentive strategies would not fundamentally disrupt its core contributions—modeling ASQ and implementing the mutually assisted dispatch framework. However, varying incentive patterns and scheduling methods could enhance the efficiency of vehicle dispatch and improve overall performance. For example, in cases where some vehicle agents accept tasks but do not adhere to the scheduled trajectories, two potential solutions could be explored: 1) excluding malicious agents from the dispatch pool and 2) adjusting the trajectory matrix to a probabilistic model for candidates deemed potentially noncompliant, allowing for more flexible task assignment while maintaining overall reliability.

# C. Reliance on Accurate Mobility Predictions

As demonstrated in our evaluation, the performance of QUIDS is highly sensitive to the accuracy of mobility predictions. Since the algorithm relies on accurate predictions of vehicle trajectories for effective dispatch, ensuring the accuracy of mobility models is crucial for the successful real-world application of QUIDS. To mitigate the impact of prediction errors, future work could explore techniques for improving mobility prediction, such as integrating real-time data or using more advanced machine learning models for trajectory forecasting. Moreover, robustness to varying degrees of prediction error could further enhance the practical applicability of QUIDS in dynamic environments.

# VI. RELATED WORK

In this section, we review the related work in three key areas: NVMCS (Section VI-A), sensing coverage (Section VI-B), and sensing reliability (Section VI-C).

# A. NVMCS System

NVMCS leverages nondedicated vehicles (e.g., taxis or private cars) for sensing purposes, improving both coverage and operational efficiency [34]. Previous research has explored various aspects of NVMCS, such as data volume [35], multiobjective tradeoffs [36], incentivization strategies [37], [38], and data utilization [23], [39], [40]. In particular, several representative approaches have been proposed in the domain of incentive strategies. For instance, the SHIP employs fine-grained vehicle state classification and an opportunity-participation hybrid incentive model to improve sensing diversity while aligning the interests of both platforms and drivers [27]. The VADS is a coalitional sensing framework based on Stackelberg game theory and Nash equilibrium optimization, designed to balance economic incentives and resource allocation across multiple operators and vehicles [28]. Finally, the VCG-MST mechanism integrates VCG pricing with staggered scheduling and budget awareness to simultaneously guarantee passenger service quality and effective sensing task allocation [29].

In contrast, our study specifically addresses the challenges of sensing reliability and coverage in NVMCS. Our findings complement and extend the existing body of NVMCS research, focusing on key issues that have been largely overlooked in previous works.

# B. Sensing Coverage

Ensuring comprehensive sensing coverage is a critical challenge in MCS systems. Researchers have proposed spatial–temporal scheduling approaches that consider energy efficiency or budget effectiveness when selecting NVMCS agents [41], [42], [43]. For example, Zhu et al. [18] addressed spatiotemporal redundancy when performing NVMCS tasks in urban areas using high-resolution maps. In addition, PAS first constructs two prediction models to estimate potential vehicle routes and passenger ride-hailing probabilities across urban areas, then introduces a prediction-based execution planning algorithm to select vehicles and assign routes [8]. iLOCuS remains exclusively concerned with the spatiotemporal distribution of sensed data and proposes a hierarchical iterative optimization algorithm to steer the data collected by vehicle agents toward a desired target distribution [9]. GCC-MARL develops a novel GCC-MARL framework to achieve distributed and cooperative routing decisions, assisting taxis in balancing order-serving and sensing tasks [10]. All these methods optimize only for sensing coverage, operating under the assumption of nearly perfect sensor reliability. In reality, however, sensor reliability tends to exhibit significant uncertainty due to environmental disturbances and operational fluctuations. By contrast, QUIDS proposes a new metric termed ASQ, which simultaneously captures both sensing coverage and reliability.

# C. Sensing Reliability

Mobile sensors are subject to environmental variations and external influences that complicate the task of ensuring reliable data collection [44]. Several methods have been proposed to address NVMCS sensing reliability, including comparing collected data with ground truth [45], [46], [47], calibrating sensors using external sources [11], [48], and leveraging machine learning models to improve sensor accuracy [12]. However, these methods face significant challenges in dynamic, NVMCS systems, where sensor types can vary, and ground truth references are often unavailable. Some approaches have tried to address these challenges by relying on historical data as pseudo-ground truth for static environments [49], [50]. In addition, Meng et al. [19] proposed truth discovery techniques for correlated sensors and regions. While these methods provide useful insights, they remain constrained by two major issues. 1) Uneven distribution of nondedicated vehicles: in areas with few vehicles, data coverage is sparse, resulting in unreliable sensing estimates and incomplete spatial coverage. 2) Failure to identify constant biases: existing methods primarily focus on detecting unreliable sensors but do not distinguish between dynamic errors and constant biases in sensor measurements. These limitations highlight the need for novel techniques capable of guiding dispatch decisions and enhancing the overall QoI in NVMCS systems.

# VII. CONCLUSION

To enhance the QoI in NVMCS systems, we propose QUIDS, a quality-informed incentive-driven multi-agent dispatching system. We model the paradoxical relationship between sensing reliability and sensing coverage as an optimization problem. Our framework infers sensor reliability and calculates monetary incentives to dispatch vehicles in NVMCS systems, aiming to maximize the ASQ metric and, consequently, achieve optimal QoI. City-scale simulations based on physical features demonstrate significantly lower error rates at high coverage levels, validating the effectiveness of our approach. This solution opens new research directions for NVMCS systems, including the modeling and optimization of sensing reliability and sensing coverage under conditions of limited incentives and uncertain environments.

# REFERENCES

[1] Z. Li et al., “QUEST: Quality-informed multi-agent dispatching system for optimal mobile crowdsensing,” in Proc. IEEE Conf. Comput. Commun. (IEEE INFOCOM), Milwaukee, WI, USA, May 2024, pp. 1811–1820.   
[2] Y. Liu, L. Kong, and G. Chen, “Data-oriented mobile crowdsensing: A comprehensive survey,” IEEE Commun. Surveys Tuts., vol. 21, no. 3, pp. 2849–2885, 3rd Quart., 2019.   
[3] C. Xiang et al., “Reusing delivery drones for urban crowdsensing,” IEEE Trans. Mobile Comput., vol. 22, no. 5, pp. 2972–2988, May 2023.   
[4] X. Chen et al., “DeliverSense: Efficient delivery drone scheduling for crowdsensing with deep reinforcement learning,” in Proc. ACM Int. Joint Conf. Pervasive a Comput., Sep. 2022, pp. 403–408.   
[5] A. Feltenstein and J. Ha, “An analysis of the optimal provision of public infrastructure: A computational model using Mexican data,” J. Develop. Econ., vol. 58, no. 1, pp. 219–230, 1999.   
[6] N. Buch, S. A. Velastin, and J. Orwell, “A review of computer vision techniques for the analysis of urban traffic,” IEEE Trans. Intell. Transp. Syst., vol. 12, no. 3, pp. 920–939, Sep. 2011.

[7] C. Fiandrino, F. Anjomshoa, B. Kantarci, D. Kliazovich, P. Bouvry, and J. N. Matthews, “Sociability-driven framework for data acquisition in mobile crowdsensing over fog computing platforms for smart cities,” IEEE Trans. Sustain. Comput., vol. 2, no. 4, pp. 345–358, Oct. 2017.   
[8] X. Chen et al., “PAS: Prediction-based actuation system for city-scale ridesharing vehicular mobile crowdsensing,” IEEE Internet Things J., vol. 7, no. 5, pp. 3719–3734, May 2020.   
[9] S. Xu, X. Chen, X. Pi, C. Joe-Wong, P. Zhang, and H. Y. Noh, “ILOCuS: Incentivizing vehicle mobility to optimize sensing distribution in crowd sensing,” IEEE Trans. Mobile Comput., vol. 19, no. 8, pp. 1831–1847, Aug. 2020.   
[10] R. Ding, Z. Yang, Y. Wei, H. Jin, and X. Wang, “Multi-agent reinforcement learning for urban crowd sensing with for-hire vehicles,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), May 2021, pp. 1–10.   
[11] Y. Cheng, X. He, Z. Zhou, and L. Thiele, “ICT: In-field calibration transfer for air quality sensor deployments,” Proc. ACM Interact., Mobile, Wearable Ubiquitous Technol., vol. 3, no. 1, pp. 1–19, Mar. 2019.   
[12] Y. Lin, W. Dong, and Y. Chen, “Calibrating low-cost sensors by a twophase learning approach for urban air quality measurement,” Proc. ACM Interact., Mobile, Wearable Ubiquitous Technol., vol. 2, no. 1, pp. 1–18, Mar. 2018.   
[13] F. C. Commission. (May 2021). Report To Congress on Usps Broadband Data Collection Feasibility Study. [Online]. Available: https://www.fcc.gov/sites/default/files/report-congress-usps-broadbanddata-collection-feasibility-05242021.pdf   
[14] T. Kassandros, E. Bagkis, and K. Karatzas, “Data fusion for the improvement of low-cost air quality sensors,” in Proc. Int. Tech. Meeting Air Pollut. Model. Appl.. Springer, 2021, pp. 175–180.   
[15] S. Ji, Y. Zheng, and T. Li, “Urban sensing based on human mobility,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., Sep. 2016, pp. 1040–1051.   
[16] J. Yuan et al., “T-drive: Driving directions based on taxi trajectories,” in Proc. 18th SIGSPATIAL Int. Conf. Adv. Geograph. Inf. Syst., 2010, pp. 99–108.   
[17] J. Liu, H. Shen, H. S. Narman, W. Chung, and Z. Lin, “A survey of mobile crowdsensing techniques: A critical component for the Internet of Things,” ACM Trans. Cyber-Phys. Syst., vol. 2, no. 3, pp. 1–26, 2018.   
[18] Q. Zhu, M. Y. S. Uddin, N. Venkatasubramanian, and C.-H. Hsu, “Spatiotemporal scheduling for crowd augmented urban sensing,” in Proc. IEEE Conf. Comput. Commun. (IEEE INFOCOM), Apr. 2018, pp. 1997–2005.   
[19] C. Meng et al., “Truth discovery on crowd sensing of correlated entities,” in Proc. 13th ACM Conf. Embedded Networked Sensor Syst., Nov. 2015, pp. 169–182.   
[20] T. Schreiber, “Measuring information transfer,” Phys. Rev. Lett., vol. 85, no. 2, pp. 461–464, Jul. 2000.   
[21] J. Napier, Mirifici Logarithmorum Canonis Descriptio. A. Hart, 1914.   
[22] A. Jauhri et al., “Space-time graph modeling of ride requests based on real-world data,” in Proc. AAAI Workshops, 2017.   
[23] X. Chen, X. Xu, X. Liu, H. Y. Noh, L. Zhang, and P. Zhang, “HAP: Finegrained dynamic air pollution map reconstruction by hybrid adaptive particle filter: Poster abstract,” in Proc. 14th ACM Conf. Embedded Netw. Sensor Syst. CD-ROM, Nov. 2016, pp. 336–337.   
[24] X. Chen et al., “PGA: Physics guided and adaptive approach for mobile fine-grained air pollution estimation,” in Proc. ACM Int. Joint Conf. Int. Symp. Pervasive Ubiquitous Comput. Wearable Comput., Oct. 2018, pp. 1321–1330.   
[25] J. M. Barcelo-Ordinas, P. Ferrer-Cid, J. Garcia-Vidal, M. Viana, and A. Ripoll, “H2020 project CAPTOR: Raw data collected by low-cost MOX ozone sensors in a real air pollution monitoring network,” Zenodo, H2020 Project CAPTOR, Mar. 2021, doi: 10.5281/zenodo.4570449.   
[26] O. Gonzalez, V. Barberan, and G. Camprodon, “Iscape low cost sensor development data,” iSCAPE, Dec. 2019, doi: 10.5281/zenodo.3570688.   
[27] H. Jiang, Y. Ren, J. Fang, Y. Yang, L. Xu, and H. Yu, “SHIP: A state-aware hybrid incentive program for urban crowd sensing with for-hire vehicles,” IEEE Trans. Intell. Transp. Syst., vol. 25, no. 3, pp. 3041–3053, Mar. 2024.   
[28] Z. Zhang, F. Zeng, and F. Tang, “Vehicle-assisted data sensing in vehicle edge metaverse: A game theory approach,” IEEE Trans. Veh. Technol., vol. 74, no. 4, pp. 5664–5675, Apr. 2025.   
[29] S. Liu, Q. Ge, K. Han, D. Fukuda, and T. Dantsuji, “Mechanism design for coordinating vehicle-based mobile sensing tasks within the ridehailing platform,” Transp. Res. C, Emerg. Technol., vol. 176, Jul. 2025, Art. no. 105151.

[30] X. Chen, Z. He, and L. Sun, “A Bayesian tensor decomposition approach for spatiotemporal traffic data imputation,” Transp. Res. C, Emerg. Technol., vol. 98, pp. 73–84, Jan. 2019.   
[31] W. Hu, X. Xiao, Z. Fu, D. Xie, T. Tan, and S. Maybank, “A system for learning statistical motion patterns,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 28, no. 9, pp. 1450–1464, Sep. 2006.   
[32] X. Chen, A. Purohit, C. R. Dominguez, S. Carpin, and P. Zhang, “DrunkWalk: Collaborative and adaptive planning for navigation of micro-aerial sensor swarms,” in Proc. 13th ACM Conf. Embedded Networked Sensor Syst., Nov. 2015, pp. 295–308.   
[33] H. Wang, Y. Liu, C. Zhao, J. He, W. Ding, and X. Chen, “CaliFormer: Leveraging unlabeled measurements to calibrate sensors with self-supervised learning,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput. ACM Int. Symp. Wearable Comput., Oct. 2023, pp. 743–748.   
[34] O. Rizwan, H. Rizwan, and M. Ejaz, “Development of an efficient system for vehicle accident warning,” in Proc. IEEE 9th Int. Conf. Emerg. Technol. (ICET), Dec. 2013, pp. 1–6.   
[35] S. M. A. Akber et al., “Data volume based data gathering in WSNs using mobile data collector,” in Proc. 22nd Int. Database Eng. Appl. Symp., Mar. 2018, pp. 199–207.   
[36] J. Sun, H. Jin, R. Ding, G. Fan, Y. Wei, and L. Su, “Multi-objective order dispatch for urban crowd sensing with for-hire vehicles,” in Proc. IEEE Conf. Comput. Commun. (IEEE INFOCOM), May 2023, pp. 1–10.   
[37] X. Zhang et al., “Incentives for mobile crowd sensing: A survey,” IEEE Commun. Surv. Tut., vol. 18, no. 1, pp. 54–67, 1st Quart., 2016.   
[38] E. Wang et al., “Distributed game-theoretical route navigation for vehicular crowdsensing,” in Proc. 50th Int. Conf. Parallel Process., Aug. 2021, pp. 1–11.   
[39] E. Wang, W. Liu, W. Liu, C. Xiang, B. Yang, and Y. Yang, “Spatiotemporal transformer for data inference and long prediction in sparse mobile CrowdSensing,” in Proc. IEEE Conf. Comput. Commun., May 2023, pp. 1–10.   
[40] X. Chen et al., “Adaptive hybrid model-enabled sensing system (HMSS) for mobile fine-grained air pollution estimation,” IEEE Trans. Mobile Comput., vol. 21, no. 6, pp. 1927–1944, Jun. 2022.   
[41] H. Ko, S. Pack, and V. C. M. Leung, “Coverage-guaranteed and energy-efficient participant selection strategy in mobile crowdsensing,” IEEE Internet Things J., vol. 6, no. 2, pp. 3202–3211, Apr. 2019.   
[42] X. Chen et al., “ASC: Actuation system for city-wide crowdsensing with ride-sharing vehicular platform,” in Proc. 4th Workshop Int. Sci. Smart City Operations Platforms Eng., Apr. 2019, pp. 19–24.   
[43] J. Ren, Y. Xu, Z. Li, C. Hong, X.-P. Zhang, and X. Chen, “Scheduling UAV swarm with attention-based graph reinforcement learning for ground-to-air heterogeneous data communication,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput. ACM Int. Symp. Wearable Comput., Oct. 2023, pp. 670–675.   
[44] M. Younis and K. Akkaya, “Strategies and techniques for node placement in wireless sensor networks: A survey,” Ad Hoc Netw., vol. 6, no. 4, pp. 621–655, Jun. 2008.   
[45] S. Zhang, H. Sheng, C. Li, J. Zhang, and Z. Xiong, “Robust depth estimation for light field via spinning parallelogram operator,” Comput. Vis. Image Understand., vol. 145, pp. 148–159, Apr. 2016.   
[46] H. Sheng, S. Zhang, X. Cao, Y. Fang, and Z. Xiong, “Geometric occlusion analysis in depth estimation using integral guided filter for light-field image,” IEEE Trans. Image Process., vol. 26, no. 12, pp. 5758–5771, Dec. 2017.   
[47] Y. Liu, X. Liu, F. Man, C. Wu, and X. Chen, “Fine-grained air pollution data enables smart living and efficient management,” in Proc. 20th ACM Conf. Embedded Networked Sensor Syst., Nov. 2022, pp. 768–769.   
[48] H. Wang, X. Chen, Y. Cheng, C. Wu, F. Dang, and X. Chen, “H-SwarmLoc: Efficient scheduling for localization of heterogeneous MAV swarm with deep reinforcement learning,” in Proc. 20th ACM Conf. Embedded Networked Sensor Syst., Nov. 2022, pp. 1148–1154.   
[49] D. Zhang, J. Huang, Y. Li, F. Zhang, C. Xu, and T. He, “Exploring human mobility with multi-source data at extremely large metropolitan scales,” in Proc. 20th Annu. Int. Conf. Mobile Comput. Netw., Sep. 2014, pp. 201–212.   
[50] J. Luo, Y. Hu, C. Yu, C. Hong, X.-P. Zhang, and X. Chen, “Field reconstruction-based non-rendezvous calibration for low cost mobile sensors,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput. ACM Int. Symp. Wearable Comput., Oct. 2023, pp. 688–693.

![](images/25465783b3a6b37dfb9bd9c23baf87f363cee8dd17507d7b889e7895544ab3ee.jpg)



Nan Zhou received the B.E. degree from the School of Telecommunications Engineering, Xidian University, Xi’an, China, in 2024. She is currently pursuing the master’s degree with the Tsinghua Shenzhen International Graduate School, Tsinghua University, Shenzhen, China.

Her research interests include world model, spatiotemporal dynamics, and mobile computing.

![](images/586b8ddfdebdd1a0f720cea68d7cd2c9c7f3f32e57a64af4e5b0558b680f389a.jpg)



Zuxin Li received the B.E. degree from Wuhan University, Wuhan, China, in 2021, and the M.S. degree from Tsinghua Shenzhen International Graduate School, Tsinghua University, Shenzhen, China, in 2024.

He is currently a Software Engineer with Kuaishou, Beijing, China. His research interests include mobile crowdsensing, path planning, and generative decision-making.

![](images/bb698f21b120125eca915ae2a5808f6a783b8b6490c1ba37cc20e335e0e007d2.jpg)



Fanhang Man received the B.S. degree from the University of California, San Diego, La Jolla, CA, USA, in 2021. He is currently pursuing the Ph.D. degree in data science and information technology with the Tsinghua Shenzhen International Graduate School, Tsinghua University, Shenzhen, China.

His research interests include machine learning, optimization, and large language models.

![](images/62c7458c67f95d632940d4714f0bb6a3213f31c799dce0e0f2948f8d5d94e6e8.jpg)



Xuecheng Chen received the B.E. degree from the Department of Intelligence Engineering, Sun Yat-sen University, Guangzhou, China, in 2021. He is currently pursuing the Ph.D. degree with the Tsinghua Shenzhen International Graduate School, Tsinghua University, Shenzhen, China.

His current research interests lie at the intersection of mobile computing, multirobot systems, and cyberphysical systems.

![](images/2a58894482f61729e7151cd59eb4c63a5f3703b30680ea2df3e4747ba25d03ec.jpg)



Susu Xu received the B.S. degree from Tsinghua University, Beijing, China, in 2014, and the M.S. and Ph.D. degrees from Carnegie Mellon University, Pittsburgh, PA, USA, in 2019.

She is currently an Assistant Professor with the Department of Civil and Systems Engineering, Johns Hopkins University, Baltimore, MD, USA. Her research focuses on mobile crowdsensing, spatiotemporal learning, and incentive mechanisms for urban systems and rapid disaster responses.

![](images/e18cccf9561e5a09b328aafa24357b146a43a23dcf7ce1611c750ceff5ed6a1d.jpg)



Fan Dang (Senior Member, IEEE) received the B.E. degree from the School of Software, Tsinghua University, Beijing, China, in 2013, where he is currently pursuing the Ph.D. degree.

His research interests include mobile computing and security.

![](images/d6950092c51bce0222312c3132a39e36917d5cf60c1f7643ab89cf3d1ba0bf15.jpg)



Chaopeng Hong received the B.E. and Ph.D. degrees from Tsinghua University, Shenzhen, China, in 2012 and 2017, respectively.

He is currently an Assistant Professor with the Tsinghua Shenzhen International Graduate School, Tsinghua University. His research interests lie in the coupled human-environment systems and sustainable systems analysis, including especially climate change, air quality, agriculture, energy, and water systems.

![](images/70651440d689af28ebf1ffb32a434c16a228965c55ebd7911e6d748cc8c8383a.jpg)



Xiao-Ping Zhang (Fellow, IEEE) received the B.S. and Ph.D. degrees in electronic engineering from Tsinghua University, Shenzhen, China, in 1992 and 1996, respectively, and the M.B.A. degree (Hons.) in finance, economics, and entrepreneurship from The University of Chicago Booth School of Business, Chicago, IL, USA, in 2008.

He was the Founding Dean of the Institute of Data and Information (iDI), Tsinghua Shenzhen International Graduate School (SIGS), Shenzhen, and the Chair Professor with the Tsinghua-Berkeley

Shenzhen Institute (TBSI), Shenzhen. He had been with the Department of Electrical, Computer, and Biomedical Engineering, Toronto Metropolitan University (formerly Ryerson University), Toronto, ON, Canada, as a Professor and the Director of the Communication and Signal Processing Applications Laboratory (CASPAL), Toronto, and was the Program Director of Graduate Studies. He is currently the Penrui Chair Professor with the Tsinghua SIGS, Tsinghua University. His research interests include sensor networks and IoT, machine learning/AI/robotics, statistical signal processing, image and multimedia content analysis, and applications in big data, finance, and marketing.

Dr. Zhang is a fellow of the Canadian Academy of Engineering and the Engineering Institute of Canada. He was an elected member of the ICME Steering Committee. He is a member of the Beta Gamma Sigma Honor Society. He is the General Co-Chair of the IEEE International Conference on Acoustics, Speech, and Signal Processing, 2021. He is the General Co-Chair of the 2017 GlobalSIP Symposium on Signal and Information Processing for Finance and Business and the 2019 GlobalSIP Symposium on Signal, Information Processing, and AI for Finance and Business. He is the General Chair of ICME2024 and BioCAS2023. He is the Editor-in-Chief of IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING. He was a Senior Area Editor of IEEE TRANSACTIONS ON IMAGE PROCESSING and IEEE TRANSACTIONS ON SIGNAL PROCESSING. He was an Associate Editor of IEEE TRANSACTIONS ON IMAGE PROCESSING, IEEE TRANSACTIONS ON MULTIMEDIA, IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS FOR VIDEO TECHNOLOGY, IEEE TRANSACTIONS ON SIGNAL PROCESSING, and IEEE SIGNAL PROCESSING LETTERS. He was selected as an IEEE Distinguished Lecturer by the IEEE Signal Processing Society and the IEEE Circuits and Systems Society. He is a registered Professional Engineer in Ontario, Canada.

![](images/e5b36e1e608b89b85716e5f92cc9469751f1ea1ffbfed0d59afc60bea3502ca2.jpg)



Yunhao Liu (Fellow, IEEE) received the B.E. degree from the Department of Automation, Tsinghua University, Beijing, China, in 1995, the M.A. degree from Beijing Foreign Studies University, Beijing, in 1997, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing, MI, USA, in 2003 and 2004, respectively.

He is currently a Professor with the Department of Automation and the Dean of the Global Innovation Exchange, Tsinghua University. His research

interests include the Internet of Things, wireless sensor networks, indoor localization, the industrial internet, and cloud computing. Dr. Liu is a fellow of CCF and ACM.

![](images/fafaa7aad88f0b88b23d6b8424e48da50da6f0af821ad673964c783b162014d9.jpg)



Xinlei Chen (Member, IEEE) received the B.E. and M.S. degrees in electronic engineering from Tsinghua University, Shenzhen, Guangdong, China, in 2009 and 2012, respectively, and the Ph.D. degree in electrical engineering from Carnegie Mellon University, Pittsburgh, PA, USA, in 2018.

He was a Post-Doctoral Research Associate with the Electrical Engineering Department, Carnegie Mellon University. He is currently an Associate Professor with the Tsinghua Shenzhen International Graduate School, Tsinghua University. His research

interests include the AIoT, artificial intelligence, pervasive computing, cyberphysical systems, robotics, urban sensing, brain–computer interface, and human–computer interface.