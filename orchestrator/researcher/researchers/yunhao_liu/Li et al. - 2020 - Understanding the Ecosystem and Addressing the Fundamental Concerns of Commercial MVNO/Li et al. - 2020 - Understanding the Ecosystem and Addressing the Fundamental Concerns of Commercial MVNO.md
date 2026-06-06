# Understanding the Ecosystem and Addressing the Fundamental Concerns of Commercial MVNO

Yang Li , Jianwei Zheng, Zhenhua Li , Member, IEEE, ACM, Yunhao Liu, Fellow, IEEE, ACM, Feng Qian, Sen Bai, Yao Liu , Member, IEEE, and Xianlong Xin

Abstract— Recent years have witnessed the rapid growth of mobile virtual network operators (MVNOs), which operate on top of existing cellular infrastructures of base carriers, while offering cheaper or more flexible data plans compared to those of the base carriers. In this paper, we present a two-year measurement study towards understanding various fundamental aspects of today’s MVNO ecosystem, including its architecture, customers, performance, economics, and the complex interplay with the base carrier. Our study focuses on a large commercial MVNO with one million customers, operating atop a nation-wide base carrier. Our measurements clarify several key concerns raised by MVNO customers, such as inaccurate billing and potential performance discrimination with the base carrier. We also leverage big data analytics, statistical modeling, and machine learning to address the MVNO’s key concerns with regard to data usage prediction, data plan reselling, customer churn mitigation, and billing delay reduction. Our proposed techniques can help achieve higher revenues and improved services for commercial MVNOs.

Index Terms— Mobile virtual network operator (MVNO), mobile network operator (MNO), base carrier, MVNO ecosystem.

# I. INTRODUCTION

ROPELLED by increasing market demands, mobile virtual network operators (MVNOs) have quickly gained popularity and commercial success in recent years [1]. The global MVNO market revenue has reached \$60.5 billion in 2018 [2], and the number of MVNOs worldwide has exceeded 1000 [3]. MVNOs operate on top of existing cellular infrastructures of base carriers, while offering cheaper or more flexible data and voice/SMS plans compared to those of the base carriers. Also, MVNOs can enhance the utilization of base carriers’ infrastructures, as well as promote the competition in the telecommunication market and prevent potential monopoly to some extent. Further, MVNOs are expected to

Manuscript received July 21, 2019; revised December 24, 2019 and March 12, 2020; accepted March 13, 2020; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor C. F. Chiasserini. This work was supported in part by the National Key Research and Development Program of China under Grant 2018YFB1004700, in part by NSFC under Grant 61822205, Grant 61632020, Grant 61632013, and Grant 61702298, and in part by the BNRist. (Corresponding author: Zhenhua Li.)

Yang Li, Jianwei Zheng, Zhenhua Li, and Sen Bai are with the School of Software, Tsinghua University, Beijing 100084, China (e-mail: lizhenhua1983@tsinghua.edu.cn).

Yunhao Liu is with the School of Software, Tsinghua University, Beijing 100084, China, and also with the Department of Computer Science and Engineering, Michigan State University, East Lansing, MI 48824 USA.

Feng Qian is with the Department of Computer Science and Engineering, University of Minnesota, Minneapolis, MN 55455 USA (e-mail: fengqian@umn.edu).

Yao Liu is with the Department of Computer Science, Binghamton University, Binghamton, NY 13902 USA (e-mail: yaoliu@binghamton.edu).

Xianlong Xin is with Xiaomi Technology Company Ltd., Beijing 100085, China (e-mail: andynjux@163.com).

Digital Object Identifier 10.1109/TNET.2020.2981514

![](images/1cf3d5c837946d5f4b2582e5d2c7c82a3487b62070cb9877489b2e98ff26714d.jpg)



Fig. 1. Architectural overview of a typical light MVNO’s ecosystem.

play a critical role in the 5G era: MVNOs that obtain sliced radio access network resources from base carriers would act as a forerunner in network slicing, a crucial technology of 5G [4].

Despite the unprecedented growth of MVNOs, end customers are still subject to manifold concerns when switching to MVNOs. For example, severe overcharge problems have been reported with regard to MVNO users [5]. Also, some base carriers may deliver MVNO users’ data with lower priorities, leading to inferior performance experienced by MVNO customers [6]–[8]. All above concerns may impede the reputation of MVNOs and hinder their development.

Due to the few studies in public literature, the community lacks a thorough understanding of the MVNO ecosystem, including its architecture, performance, economics, customers, and the complex interplay between an MVNO and its base carrier. In this paper, we present a nearly two-year measurement study towards understanding above aspects. Our study focuses on Xiaomi Mobile [9] (V-Mobile for short), a large commercial MVNO in China. It has about one million (M) users and fully operates on top of China Telecom (B-Mobile for short), a nationwide base carrier in China which has over 300M users. V-Mobile is a representative light MVNO (§II), the most popular type of MVNOs that fully rely on the base carrier’s cellular infrastructure [1], while having the capability of designing their own data plans independently of the base carriers. In other words, V-Mobile resells data plans purchased from B-Mobile to its users. In order to attract customers while gaining profits, V-Mobile has to (1) strategically design its own data plans, and (2) judiciously purchase data plans from B-Mobile to fulfill the data plans selected by V-Mobile customers, based on estimating their monthly data usages.

Studying the MVNO ecosystem is challenging, as it involves multiple stakeholders (customers, the MVNO, and the base carrier) that incur complex interplay, as well as components not present in traditional MNOs (Mobile Network Operators) such as data plan reselling. As illustrated in Figure 1, a typical light MVNO like V-Mobile runs four main businesses: data/text services, data plan reselling, customer care, and billing. Data and SMS text transmission are the basic services a MVNO provides to its customers via its base carrier. With reliable basic services, the MVNO can then make its profit mostly by reselling data plans. Further, customer care is crucial to stable profitability. In addition, billing is needed to track each customer’s payments and the MVNO’s earnings, which also facilitates profit optimization and exception handling.

According to the operation experiences of V-Mobile, running the above businesses is confronted with four core pain points that are also summarized in Figure 1. First, it is critical to guarantee the network performance of data/text services [7], which is also an indispensable part of customer care. Second, for data plan reselling, accurate data usage prediction on a monthly basis is the primary yet challenging target [10]. Third, since an enterprise usually needs to pay much more when attempting to recruit new customers than to retain existing ones [11], customer churn needs to be effectively mitigated with moderate overhead. Finally, customer feedback indicates that inaccuracy and latency are the major issues of billing.

To enable large-scale measurement, we collaborate with V-Mobile and collect five datasets (§II) which include customers’ demographics, selected data plans, monthly data usages, traffic characteristics, network performance, billing events, and so forth. Jointly examining these datasets helps reveal a comprehensive landscape of the MVNO ecosystem as follows.

• Data Plan & Usage Characterization (§IV-A). We begin with customers’ data plan selection and data consumption. V-Mobile users are found to be sensitive to prices – almost half of them prefer the data plan with the lowest cost per GB (\$2.84/GB). Also, their demographics are different from those of an MNO: significantly more female (58.3%) than male (41.7%), and dominated by users younger than 30. Besides, V-Mobile users considerably under-utilize their data plans, e.g., 23% users have little data usage (<50 MB) in at least 25% of their billed months, and their actual data usage is weakly correlated with their subscribed data plans. The above findings suggest that V-Mobile users’ data plan selection is oftentimes economically suboptimal, which is a key reason why operating an MVNO can be profitable.

• Network Performance Characterization (§IV-B). We collect TCP performance statistics from ∼600 geographically distributed V-Mobile and B-Mobile customers’ mobile devices for 30 days. By analyzing this data, we find no noticeable performance difference between B-Mobile and V-Mobile. This is distinct from previous reports where MVNO users suffer from performance degradations compared to the base carrier’s users [6]–[8]. Our results indicate that the performance degradation reported by prior studies is very likely a (man-manipulated) policy-level result by the base carrier rather than a technical necessity.

• Monthly Data Usage Prediction (§V-A.1) plays a critical role in the operation of an MVNO. We formulate it into a time series forecasting problem, and strategically apply off-the-shelf machine learning (ML) algorithms. We employ robust statistical methods such as Grubb’s Test [12] and neighbor mean interpolation [13] to complement the ML approaches. The synergy among above efforts leads to an average prediction accuracy of 93.3%. In addition to data usage prediction on a per-user basis, we holistically examine the entire user base through uncertainty modeling, which establishes a global statistical distribution for the prediction accuracy. Doing so facilitates the prediction for new users with insufficient training samples.

• Data Reselling Optimization (§V-A.2). Leveraging our data usage prediction technique, we develop a framework to optimize V-Mobile’s reselling profit, i.e., intelligently selecting the data plans to be purchased from B-Mobile in order to maximize the overall profit for V-Mobile. When applied to the active users in our dataset, our ML-based technique increases V-Mobile’s profit rate by 25.7% compared to its current approach. Applying the uncertainty modeling further improves the profit rate by 27.3% – an overall improvement of 60% brought by our approach.

Customer Churn Profiling & Mitigation (§V-B). Customer churn refers to when a customer cancels or “drops out” her subscribed service. Its mitigation is extremely important for both base carriers and in particular MVNOs like V-Mobile. We mine our dataset to reveal key factors that indicate a user’s forthcoming service cancellation. We then use them to proactively predict customers’ churn also with off-the-shelf ML algorithms. Additionally, we employ an under-sampling [14] based method called One-Sided Selection [15] to mitigate the negative impact caused by imbalanced positive and negative samples in our dataset. Eventually, we manage to achieve both high precision (96.3%) and recall (97.8%), and our solution can even be adjusted to effectively detect phone fraud.

Tackling Inaccurate Billing (§V-C). We systematically investigate V-Mobile users’ complaints on billing issues, e.g., their unexpectedly high monthly charges. We find that most billing issues are caused by the excessive propagation delay of the control-plane billing state update reports (SURs). The overall delay often reaches several minutes, leading to billing inconsistency between B-Mobile and V-Mobile. We propose a simple yet effective approach to mitigate this problem by aggregating multiple SURs each reporting a small data usage and employing a dedicated SUR transmission line from B-Mobile to V-Mobile. We assisted V-Mobile in actually deploying our solution, which significantly reduced the average SUR delivery latency (from B-Mobile to V-Mobile) from two minutes to less than one second on V-Mobile’s production system.

To our knowledge, this is so far the most comprehensive study of commercial MVNO. Our high-level contributions are multifold. From an end user’s perspective, our study demystifies the MVNO ecosystem, and clarifies several key concerns raised by customers. From an MVNO’s perspective, we leverage big data analytics, statistical modeling, and machine learning to optimize an MVNO’s key businesses such as data usage prediction, data plan reselling, and customer churn mitigation. In addition, we summarize the high-level lessons we have learned in §VII to benefit relevant researchers and practitioners. Our study also exposes to the community new research topics, with intra-disciplinary nature, in the context of MVNO and its interplay with the base carrier.

# II. BACKGROUND

A base carrier typically owns a legal license to exclusively use certain frequencies of the radio spectrum in a country. This can often lead to market monopoly, service degradation, or under-utilization of radio resources. To address these problems, numerous MVNOs have emerged in recent years. An MVNO fully or partially leverages one or multiple base carriers’ licensed radio spectrum and facilities. According to their degrees of dependence on base carriers, today’s MVNOs can be classified into three categories [1]: skinny, light, and thick MVNOs. Skinny and light MVNOs do not have their own radio infrastructures; skinny MVNOs are mainly devoted to marketing and sales, and are thus also known as “branded resellers,” while light MVNOs further have the ability to design specialized data plans independently of the base carriers. In contrast, thick MVNOs have their own infrastructures (including the core networks and the radio access networks) to exert more control over their offerings, which however are not permitted in many countries such as China. Among the three categories, light MVNOs (e.g., our studied V-Mobile) are the most common and are permitted in most countries [1].

![](images/bccc576e36c7d736622f893de10e09f4b192065b8ca1d34f00c9bb55176342c7.jpg)



Fig. 2. Interactions among V-Mobile, its customers, and B-Mobile.

# A. Data Plan Reselling

V-Mobile resells data plans purchased from B-Mobile to its users. However, it does not have a wholesale (discounted) price from B-Mobile, nor is it allowed to buy a single data plan from B-Mobile to serve multiple users. Therefore, in order to attract customers while gaining profits, V-Mobile has to strategically design its own data plans. Specifically, let $P _ { V }$ be a data plan that V-Mobile offers its customers; let $P _ { B }$ be the same plan offered by B-Mobile; let $P _ { V } ^ { \prime }$ be the corresponding plan that V-Mobile purchases from B-Mobile to fulfill $P _ { V }$ . Ideally, $P _ { V }$ needs to be cheaper than $P _ { B }$ , otherwise customers have no incentives to switch to V-Mobile; $P _ { V } ^ { \prime }$ should be inferior to (and thus cheaper than) $P _ { V }$ , otherwise operating V-Mobile is not profitable. Consider a concrete example. B-Mobile has a monthly plan of “\$7.23 for 2 GB plus \$0.01/MB overdraft” $( P _ { B } )$ . To attract customers, V-Mobile lowers the price by offering “\$7.09 for 2 GB plus \$0.01/MB overdraft” $( P _ { V } )$ . To fulfill $P _ { V }$ , V-Mobile can purchase from B-Mobile an inferior plan of “\$5.78 for 1 GB plus \$0.01/MB overdraft” $( P _ { V } ^ { \prime } )$ . The assumption here is that, despite having a 2 GB data plan, many users’ actual monthly usages are much lower. In this example, the reselling is profitable if a V-Mobile user’s monthly usage is lower than 1000 + (7.09-5.78) / 0.01 = 1131 MB. This example also illustrates the importance for V-Mobile to accurately predict a user’s monthly data usage.

# B. Billing

As the base carrier of V-Mobile, B-Mobile has hundreds of millions of customers and over a million base stations (BSes) across the country. Since V-Mobile is a light MVNO, all its SIM cards are issued by B-Mobile while possessing special phone numbers (MSISDN) that can be identified as MVNO numbers. Therefore, all the data traffic, voice calls, and SMS messages of V-Mobile users are delivered by the radio infrastructure of B-Mobile. Moreover, since V-Mobile establishes its own data plans, it needs to handle customers’ billing, which is processed at the accounting center (AC), by itself. In order for V-Mobile to generate bills in an accurate and timely fashion, the SURs, which contain users’ up-to-date data usage

TABLE I DIFFERENT DATASETS USED IN THIS PAPER AND THEIR ATTRIBUTES. 

<table><tr><td>Dataset</td><td>Attribute</td></tr><tr><td>BBSDataset</td><td>user_name, post_content</td></tr><tr><td>UserDataset(Jan. 2016 – Oct. 2017)</td><td>user_id, gender, birthday, date_join, date_drop, churn_status</td></tr><tr><td>MonthlyDataset(Jan. 2016 – Oct. 2017)</td><td>user_id, data_plan, data_usage, payment, account_balance</td></tr><tr><td>PerfDataset</td><td>rtt, flow_duration, retransmission_rate, down_flow_rate, up_flow_rate</td></tr><tr><td>SURDataset</td><td>type, timestamp, device_id, data_usage</td></tr></table>

information, need to be properly delivered to V-Mobile’s AC. This can be achieved in two ways. The major way is shown in the upper branch in Figure 2: V-Mobile and B-Mobile establish a control-plane channel between their ACs, allowing B-Mobile to forward V-Mobile users’ SURs, which we call B-Mobile-SURs, to V-Mobile. In B-Mobile, B-Mobile-SURs are gathered and propagated by its base stations. Another way of delivering SURs is illustrated in the bottom branch in Figure 2. V-Mobile customers can optionally install an app developed by V-Mobile. When the app is running, it keeps monitoring the client device’s data usage and uploading SURs, which we call App-SURs, directly to V-Mobile’s AC.

# III. MEASUREMENT DATA COLLECTION

To enable our large-scale measurement of a typical MVNO, we collect multiple datasets from various sources. The datasets and their attributes are listed in Table I. Correlating these datasets focusing on different aspects (including user profile, data usage, network performance, etc.) helps reveal a complete landscape of the MVNO ecosystem.

(1) BBSDataset. V-Mobile maintains a BBS (Bulletin Board System) website from which we gathered ∼12,000 posts from the BBS users, who belong to either the current or prospective users of V-Mobile. We then manually examine all the posts to understand the users’ concerns. Detailed analysis of the posts can be accessed in our early version [16].   
(2) UserDataset. We obtain from V-Mobile a database containing each user’s basic information, including the gender, birthday, the date of joining V-Mobile, and the date of canceling the service (for dropout users). Our dataset was captured in Oct. 2017, involving a total of 908,548 users since Jan. 2016. In this “snapshot,” 168,853 users terminated their contracts with V-Mobile and thus are excluded. In the remainder of this paper, unless otherwise noted, we apply our analysis to the 0.74M (≈ 908, 548 − 168, 853) active users.   
(3) MonthlyDataset. The AC of V-Mobile archives every user’s monthly data plan, data usage, payment, and account balance information. They provide an essential data source for profiling, modeling, and predicting each user’s monthly data usage (§IV-A and §V-A.1) The data are also used for optimizing the data reselling profit of V-Mobile (§V-A.2), as well as customer churn profiling and mitigation (§V-B). This dataset covers 22 billed months, from Jan. 2016 to Oct. 2017.   
(4) PerfDataset. A challenge we face is to monitor V-Mobile users’ network performance. We take a crowd-sourcing-based approach where we invite users of both V-Mobile and B-Mobile to voluntarily participate in a data collection campaign by installing an app developed by V-Mobile and turning on the “sampling performance” option for a whole month. The app passively measures key performance metrics such as RTT and throughput of

![](images/c9652de48c70c9e3d3e505e7953cb8ee170b53342fee8d9e0df899e1ddbf6acb.jpg)



Fig. 3. Comparison of popular light MVNOs’ payment modes and monthly data plans. Each bar’s bottom line and top line correspond to the MVNO’s cheapest and priciest plans. A line inside the bar represents an available plan.

users’ traffic. The collected statistics are securely uploaded to a remote server when users’ devices are idle, and no actual content payload was collected or uploaded. Overall, 342 V-Mobile users and 250 B-Mobile users from 269 cities in the country (China) voluntarily participated in our study for 30 days, forming a decently large dataset consisting of 1 TB TCP flows’ statistics.

(5) SURDataset. Recall from §II (Figure 2) that there are two types of SURs: B-Mobile-SURs and App-SURs. An SUR consists of a timestamp, a device ID, and the user’s data usage in bytes. We collect both types of SURs at V-Mobile’s AC, and use these data to investigate the billing issues in §V-C.

To make clear the potential generality of our measurement study, we further conduct a survey of popular light MVNOs in Europe, Asia-Pacific, and North America in three aspects:

• From their official websites: Suning, Snail, Mineo, Sakura, Giffgaff, Freenet, and so on, as well as from the statistics of BestMVNO, we observe that all these MVNOs run similar businesses such as data plan pricing/reselling, customer care, and billing.   
• In detail, we compare their payment modes and monthly data plans in Figure 3. As shown, most light MVNOs support “Pre-paid” mode, and high-volume (> 10 GB) data plans are much less provided than small- or mid-volume (< 10 GB) data plans. In other words, data plans of other light MVNOs are also similar with those of V-Mobile. As a matter of fact, even for skinny and full MVNOs, their data plans are similar to those of light MVNOs [17].   
• The problems observed in our datasets, regarding data usage prediction, customer churn, and inaccurate billing, are also hot research topics of other MVNOs [6]–[8], [18], [19].   
As a result, our study methodology and findings should be mostly applicable to other MVNOs, especially light MVNOs.

# IV. DATA USAGE & NETWORK PERFORMANCE PROFILING

In this section, we first profile V-Mobile customers’ data usage with UserDataset & MonthlyDataset (§IV-A), and then analyze PerfDataset to compare the network performance and traffic characteristics of V-Mobile and B-Mobile (§IV-B).

# A. Data Usage Characterization

We perform our characterization for V-Mobile customers in three aspects: data plan selection, actual data usages, and the relationship between them. We also compare V-Mobile with B-Mobile to unravel their differences.

TABLE II V-MOBILE’S DESIGNED DATA PLANS AND THEIR PERCENTAGE OF USERS 

<table><tr><td>Monthly Data</td><td>Subscription Fee</td><td>Overdraft</td><td>% of Users</td></tr><tr><td>1 GB</td><td>$5.64</td><td>$0.01/MB</td><td>35.79%</td></tr><tr><td>2 GB</td><td>$7.09</td><td>$0.01/MB</td><td>10.52%</td></tr><tr><td>3 GB</td><td>$8.53</td><td>$0.01/MB</td><td>47.37%</td></tr><tr><td>4 GB</td><td>$12.87</td><td>$0.01/MB</td><td>6.32%</td></tr></table>

TABLE III B-MOBILE’S DATA PLANS (SELECTED) 

<table><tr><td>Monthly Data</td><td>Subscription Fee</td><td>Overdraft Fee</td></tr><tr><td>500 MB</td><td>$3.62</td><td>$0.01/MB</td></tr><tr><td>1 GB</td><td>$5.78</td><td>$0.01/MB</td></tr><tr><td>2 GB</td><td>$7.23</td><td>$0.01/MB</td></tr><tr><td>3 GB</td><td>$8.68</td><td>$0.01/MB</td></tr><tr><td>4 GB</td><td>$13.01</td><td>$0.01/MB</td></tr><tr><td>6 GB</td><td>$27.47</td><td>$0.01/MB</td></tr></table>

![](images/6b6cb333203621b410a7e110a47b9abed2b3c043dc07d291a13a65a64fd392b0.jpg)



Fig. 4. Distributions of V-Mobile users’ monthly data usage with respect to each data plan.

![](images/558fe1111c6c9c869c20aeddc3c7ad352e89bf9aee95d886a5ae010418bb5675.jpg)



Fig. 5. Distribution of V-Mobile active users’ monthly data usage.

1) Data Plan Selection: V-Mobile makes its data plans cheaper than those (counterparts) of B-Mobile to attract customers. Table II and Table III compare the specific data plans offered by both carriers. Table II also shows the percentage of users subscribing to each of the V-Mobile’s data plans. As shown, V-Mobile users are price conscious: the 3 GB data plan attracts the most (47.37%) users for its lowest cost per GB (\$2.84/GB), followed by the 1 GB plan that has the lowest subscription cost. In contrast, the 4 GB plan has the fewest (6.32%) users, very likely because of its highest subscription cost as well as a large subscription cost increase from 3 GB to 4 GB.

We also make several interesting observations regarding V-Mobile users’ demographics, which is presented in our early version [16].

Actual Data Usage. Figure 5 plots the distribution of V-Mobile users’ monthly data usage across all of their billed months. It ranges between 0 and 6,018 MB with a mean (median) being 1,743 MB (1,950 MB). The tail indicates that overdraft may indeed occur in a non-trivial fraction of billed months, this brings potential obstacles for MVNOs towards making profits (§II). More specifically, Figure 4 shows V-Mobile users’ monthly data usages with respect to each data plan. We observe that most (93%) customers’ monthly data usages are below the data caps of their purchased plans, and those who use little to no data prefer the 1 GB plan. Besides, 27.7% customers have not used up half of their purchased data plans, indicating that V-Mobile still has considerable profitability through data reselling.

![](images/7860389c426f8c19d7d7e6c55ceaa8af56f5ad83f114b7fa6dcd18a88c6f805f.jpg)



Fig. 6. Distribution of V-Mobile active users’ presence ratios.

![](images/c03f611e8af864dd86a4e4fd5216e4a5e561f0145f67392ce280449b0a03ea1a.jpg)



Fig. 7. Difference between users’ selected data plans and actual data usage.   
![](images/67735045e079320ab7d21f034402cb82afa0161ab9d9592d8e04a2fe3631a79f.jpg)



Fig. 8. Average data usage, under-utilized bytes, and overdraft for each data plan.

More surprisingly, we see the other extreme for about 20% of the billed months in which a user consumes little data – we call this the intermittent presences of some users. Suppose a user has been a V-Mobile customer for n full months while she barely used her data plan in m out of n months. We empirically define a “bare usage” as consuming no more than 50 MB of data in a month with only full months being considered. We then compute the presence ratio of the customer as $( n \mathrm { ~ - ~ } m ) / n$ to quantify how often she uses the V-Mobile service. Figure 6 plots the presence ratio distribution across users whose lifetimes are at least one full month. As shown, the presence ratio ranges from 0.05 to 1 and averages at 0.82. Such low presence ratios are often from users who hold more than one SIM cards and use V-Mobile as a backup that is used infrequently. These users can bring high profits if V-Mobile can accurately predict their non-presence.

Data Plan vs. Actual Usage. To better understand the relationship between users’ selected data plan and monthly actual usage, we profile their difference in Figure 7 across all billed months, where a positive value indicates under-utilizing the data plan, and a negative value corresponds to overdraft. Figure 8 further shows the statistics of actually consumed, under-utilized, and overdraft bytes for each type of data plan. As shown, customers typically under-utilize their data plans (in 82.59% of all billed months). An average user under-utilizes her data plan by as much as 893 MB. This indicates that most users are pretty conservative with their data usage.

# B. Network Performance and Traffic Characteristics

We now analyze PerfDataset, collected from about 600 V-Mobile and B-Mobile users via an Android app. Once the “sampling performance” option is turned on, the app leverages libpcap to passively monitor the client device’s traffic (only the TCP/IP headers) and compute several key performance metrics: (1) TCP handshake RTT, (2) TCP flow size, i.e., the total number of payload bytes within a flow, (3) TCP flow duration, i.e., the time span between the first and last packet of a flow, (4) TCP flow rate, i.e., the ratio between flow size and duration, with uplink and downlink measured separately, and (5) TCP uplink packet retransmission rate, i.e., the ratio between retransmitted uplink data packets and the total number of uplink data packets within a flow (note that we are unable to measure the downlink retransmission rate).

Compared to prior characterizations of cellular network performance (e.g., 3GTest in 2009 [20], 4GTest in 2011 [21], SpeedTest in 2011 [22], and an LTE study in 2012 [23]), our study focuses on both MVNO and MNO, and provides more up-to-date statistics that can benefit other work on synthetic cellular traffic generation and cellular performance modeling. Our measurement results are shown in Figure 9’s eight subplots. Each CDF in subplots (a) to (f) is across all eligible TCP flows; subplots (g) and (h) show the monthly maximum flow rates across all users’ billed months, to reveal the maximum capacity offered by today’s cellular networks.

From BBSDataset we learn that many V-Mobile users have concerns that B-Mobile may potentially deliver their traffic at a lower priority. Surprisingly, our results in all plots of Figure 9 disprove this: statistically, there is no noticeable performance difference between V-Mobile and B-Mobile, in all eight metrics. Since we collect the samples from a small number of users, we further use the paired-samples T-test [24] to compare their performances. The T-test result is a confidence (p-value) between 0 and 1. We accept the hypothesis that their mean values are equal if the p-value is larger than α, a threshold typically set to 0.05. As listed in Figure 9, all the values of p are much bigger than 0.05. Therefore, even considering the impact of small samples, we still find no significant difference between their performances. We ascribe this to the non-discriminatory packet routing policy of B-Mobile in delivering V-Mobile users’ data. In contrast, several previous reports [6]–[8] noted that the users of certain MVNOs had suffered from performance degradations compared to the base carriers’ users. Our measurements indicate that such a performance degradation is very likely a (man-manipulated) policy-level result rather than a technical necessity.

We also compare our results with an LTE measurement study in 2012 [23] when LTE just made its debut. We do not distinguish between V-Mobile and B-Mobile due to their similar performance. Subplots (a)(b) show that the vast majority of flows are small and short. Nevertheless, the long tails indicate that a small fraction of “heavy-hitter” flows can be very large. The flow sizes are statistically larger than those reported by [23] where the median flow size is less than 5KB, likely due to the larger content sizes today. In subplot (c), the 25th, 50th, and 75th percentiles of the TCP handshake RTTs are 30.3ms, 48.6ms, and 68.2ms, considerably lower than those reported by [23] (the median around 70ms), possibly attributed to the infrastructural improvement of the LTE RAN (radio access network) over the past years. In subplot (d), the uplink retransmission rate is typically low, with the 25th, 50th, and 75th percentiles being 0.03%, 0.06%, and 0.36%.

![](images/c728bb1d74b2288e8709b33359768d56260250c285212dcd5d928c52f870b23d.jpg)



(a) p = 0.8798

![](images/aaef57ce6bcf9d5f563f691a05c37e3547e66c8de4ff769be596ea515e8fadca.jpg)



(b) p = 0.8436

![](images/c3298cf16c849bca8092c7bf33d6bebbc89f8389ca51976e5be256d794b9ba7f.jpg)



(c) p = 0.9042

![](images/b1f08a5517dc7cd99b29d0b2b8957a16e2e4276f7f26ec9323e72cc91c0d7f7d.jpg)



(d) p = 0.9698

![](images/0a83b78f61d6186123d4a9287b15a8cc36121856d4f8a5c6ed497034071e2998.jpg)



(e) p = 0.9327

![](images/dd139f56421fd2675fa6ce90bd7666e12f2899bef2608f3725f1b0bb5fee2c82.jpg)



(f) p = 0.9506

![](images/0dfe709b61ee701769bfd36201c448f11ae55b88e8b639880d1a02414cafb45f.jpg)



(g) p = 0.9142

![](images/0e9c6032074059a3143bc7d6285dc2f60e95c4eaf1853a108a432f5e93d3ec4e.jpg)



(h) p = 0.8949   
Fig. 9. Network performance and traffic characteristics of crowd-sourced V-Mobile and B-Mobile users. The p-values of the T-test are also shown.

# V. ADDRESSING THE CORE PAIN POINTS OF MVNO

As illustrated in Figure 1, a typical light MVNO is subject to four core pain points. Given that network performance is not an issue in V-Mobile (cf. §IV-B), the real pain points we have to address include data usage prediction, customer churn, and billing inaccuracy and latency. In this section, we first introduce how an MVNO can optimize the data reselling profit via appropriate data usage prediction (§V-A), and then extract key features and adopt ML algorithms to predict customer churn (§V-B), and finally analyze BBSDataset to understand and partially address the billing issues (§V-C).

# A. Data Usage Prediction and Data Reselling Optimization

In this part, we first describe the challenges and solutions for large-scale monthly data usage prediction, and then detail how an MVNO can leverage it to optimize the reselling profit.

1) Data Usage Prediction and Modeling: Data usage prediction is a typical time series forecasting problem, which utilizes a model to predict a variable’s future value(s) based on its previously observed values. In our work, for each user we have a time series $X \ = \ \{ X _ { 1 } , X _ { 2 } , . . . , X _ { n } \}$ where $X _ { i }$ is the user’s data usage in the i-th month, and our objective is to predict $X _ { n + 1 }$ . The prediction of each user is independently performed. For a given user, we define the prediction accuracy as:

$$
\text { Accuracy } = 1 - \frac {\left| \text { predicted\_usage } - \text { actual\_usage } \right|}{\max (\text { predicted\_usage,   actual\_usage })}. \tag {1}
$$

In the literature, while there exist many studies on (typically short-term) traffic volume prediction [25], [26], few studies specifically focus on long-term, large-scale cellular data usage prediction with limited historical data [27]. For short-term traffic volume prediction, Alarcon-Aquino and Barria proposed a multi-resolution finite-impulse-response (FIR) neural-network-based learning algorithm to predict traffic in 10 seconds with rich historical data [25]; Xiang et al. combined the covariation orthogonal and artificial neural network to predict traffic in 50 seconds [26]. However, because of the serious over-fitting,1 such models are not suitable for our long-term (three-month) data usage prediction with

1For short-term traffic volume prediction, the data collection is usually quite fine-grained (e.g., at the level of several seconds) and thus building a complex neural network model with plenty of parameters that fits the traffic curve accurately is possible. But for long-term prediction, fine-grained data can hardly be acquired due to the large overhead of data collection and storage; thus, training complex models with limited data will incur serious over-fitting. limited historical data, due to the generally short lifetime and intermittent presence of customers. For long-term traffic prediction, Shu et al. used seasonal ARIMA (Auto Regression Integrated Moving Average) to predict the GSM traffic load in 301 days [27]. However, ARIMA is limited by its natural tendency to concentrate on the mean value of historical series data, which is not what we exactly want in our scenario (i.e., per-month data usage). Given these concerns, we develop our own approach.

Methodology. We apply mainstream ML techniques for a user’s monthly data usage prediction, including SVR (Support Vector Regression [28]), RBFNN (Radial Basis Function Neural Network [29]), BPNN (Back Propagation Neural Network [30]), and ULR (Unary Linear Regression [31]). Each user is trained and tested separately. We empirically select the algorithms’ parameters as follows. As for SVR, it uses the RBF (Radial Basis Function) kernel with the kernel parameter of 0.01 and regularization parameter of 100. As for RBFNN, we set the spread of radial basis function to 0.1 and the number of neurons which are added between displays to 100. Meanwhile, we limit the maximum number of neurons to 400. BPNN uses “tansig” and “purelin” for hidden layers and output layers. The maximum number of iterations is set to 100.

Another decision we need to make is to determine n, the window length of the time series X. It poses a tradeoff: a large n reduces the number of valid training samples and may cause potential overfitting, while a small n makes the training data less expressive. We test different values of n and empirically choose n = 3 to balance the above tradeoff.

Furthermore, to filter out outliers and avoid potential overfitting, we utilize a data augmentation method called Grubbs’ Test [12], which is found to be more robust compared to simple k-means clustering used in our early version [16]. In Grubbs’ Test, outliers in a dataset are selected to be samples whose deviation from the average value (μ) exceeds the standard deviation (s) by over twice. For a group of m customers with data usages $\{ X _ { 1 } , X _ { 2 } , \cdots , X _ { m } \}$ , we first calculate two statistics:

$$
\mu = \frac {\sum_ {i = 1} ^ {m} X _ {i}}{m}, \quad s = \sqrt {\frac {\sum_ {i = 1} ^ {m} (X _ {i} - \mu)}{m - 1}}. \tag {2}
$$

Then, we use μ and s to calculate the Grubbs test statistic:

$$
G _ {i} = \frac {\left| X _ {i} - \mu \right|}{s}, \tag {3}
$$

which reflects the extent of a sample’s “anomaly”. Next, we use a hyperparameter α and the number of samples (m) to look up (in Grubbs’ critical value table) the outlier detection threshold $T \geq 2 , { \mathrm { I f } } \ G _ { i } > T , X _ { i }$ is determined as an outlier. Here α denotes the significance level of the statistical test and is empirically selected from {0.10, 0.05, 0.01}. Usually a smaller α corresponds to a larger ${ \dot { T } } ,$ , implying that the detected outliers are more significant but fewer in quantity.

![](images/d851ca63b91a0a644e44f20d62d2e829db55a183ad4fec1e175cc96b8abbd1f3.jpg)



Fig. 10. Average prediction accuracy of different machine learning techniques.

TABLE IV PREDICTION ACCURACY OF SVR-RBF, ENHANCED WITH GRUBBS’ TEST AND VARIOUS MAINSTREAM INTERPOLATION METHODS 

<table><tr><td>Interpolation Method</td><td>Accuracy (α = 0.10)</td><td>Accuracy (α = 0.05)</td><td>Accuracy (α = 0.01)</td></tr><tr><td>Neighbor Mean</td><td>93.26%</td><td>93.30%</td><td>93.25%</td></tr><tr><td>Median</td><td>92.93%</td><td>92.75%</td><td>92.72%</td></tr><tr><td>Nearest</td><td>89.94%</td><td>89.44%</td><td>88.49%</td></tr><tr><td>Polynomial</td><td>90.55%</td><td>90.76%</td><td>89.98%</td></tr><tr><td>Cubic</td><td>90.45%</td><td>90.16%</td><td>89.09%</td></tr></table>

After removing the above outliers, we apply interpolation to obtain an analytical representation of the discrete samples. We consider several mainstream one-dimensional data interpolation techniques, including neighbor mean interpolation [13], median interpolation [32], nearest interpolation [33], polynomial interpolation [34], and cubic interpolation [35].

Results. For each user whose lifetime is l months, since we pick $\ n \ = \ 3 .$ , we use $\{ s _ { 1 } , s _ { 2 } , s _ { 3 } \quad \longrightarrow \quad s _ { 4 } \} , \ldots ,$ $\left\{ s _ { l - 3 } , s _ { l - 2 } , s _ { l - 1 } \ - \ldots \right\}$ to train a model, where $s _ { i }$ is the data usage of the i-th month obtained from MonthlyDataset, using each of the aforementioned ML algorithms $( ^ { 6 6 }  ^ { 5 }$ separates the features and label). In the prediction phase, we employ the model to predict $s _ { l + 1 }$ based on $\{ s _ { l - 2 } , s _ { l - 1 } , s _ { l } \}$ . To evaluate our approach, we compute the prediction accuracy, defined in Equation (1), for each user, and compare the average accuracy of the five ML algorithms in Figure 10. In fact, V-Mobile itself adopts a quite simple method to predict each user’s monthly data usage by calculating the average value in previous months. This does not work well: the prediction accuracy is merely 68.67%. In comparison, our method achieves an average prediction accuracy of 93.3%. Table IV shows the prediction accuracy for different interpolation methods and α values for Grubbs’ Test, using SVR with RBF kernel. As shown, using neighbor mean interpolation with $\alpha =$ 0.05 yields the best accuracy of 93.3% (accordingly, the outlier detection threshold $T = 2 . 4 0 9 )$ ). Also note that in our prior version [16], using k-means clustering for outlier removal can only achieve a prediction accuracy of up to 86.75% (also using SVR with RBF kernel).

Additionally, we observe that users with a longer lifetime tend to exhibit a higher prediction accuracy because more historical data is available. This is illustrated in Figure 11, which plots the average prediction accuracy for users with different lifetime (using SVR with RBF kernel with Grubbs’ Test and neighbor mean interpolation).

Despite the overall good results, Figure 10 indicates the high variation in prediction accuracy across individual users. In particular, for users with a short lifetime, their data usage prediction is inherently difficult due to a lack of training samples. This motivates us to further holistically examine the entire user base by performing statistical uncertainty modeling (detailed in our early version [16]), which establishes statistical distributions for the prediction accuracy. As to be shown in §V-A.2, the uncertainty modeling helps users with insufficient training data; it also provides a building block for deriving a generic cost-aware optimization framework.

![](images/226d00839f5d47b102b44c5dad02c96240c5f26b3735335b739693961539eece.jpg)



Fig. 11. Average prediction accuracy increases with the lifetime of users.

![](images/f02aee4a83a2dc15627626f25e86cddba7c9eecdc54ec08b05b26cb66b83721e.jpg)



Fig. 12. The random variable $k ^ { \prime } / k$ follows a normal distribution.

2) Data Reselling Optimization: Since a V-Mobile user often does not use up her subscribed data plan $P _ { V } ,$ so V-Mobile can purchase an inferior plan, $P _ { V } ^ { \prime } \{$ , from B-Mobile to fulfill $P _ { V }$ , and utilize the price difference to make profits. Our goal here is to make the selection of $P _ { V } ^ { \prime }$ more intelligent to increase the profit for V-Mobile, transparently to its users.

Our data usage prediction may not be accurate for a specific user, so we are unable to guarantee that every individual user’s reselling profit is maximized. Instead, we aim at maximizing the expected data reselling profit across all $\mathrm { u s e r s } . ^ { 2 }$ Let there be a group of m customers with their predicted data usage $\{ k _ { 1 } , k _ { 2 } , \cdots , k _ { m } \}$ , and a collection of the base carrier’s data plans $\{ P _ { 1 } , P _ { 2 } , \cdots , P _ { n } \}$ . Consider a given user $j$ whose predicted usage is $k _ { j }$ . Let ${ p } _ { i } ( k _ { j } )$ be the expected expense, which includes the monthly subscription fee and the overdraft cost, that V-Mobile pays B-Mobile if V-Mobile selects $P _ { i }$ as the underlying plan to fulfill this user’s subscription. Thus, the minimum total expense that V-Mobile pays B-Mobile is:

$$
\sum_ {j = 1} ^ {m} \min _ {1 \leq i \leq n} \{p _ {i} (k _ {j}) \}. \tag {4}
$$

To calculate Equation (4), we need to first calculate $p _ { i } ( k _ { j } )$ :

$$
p _ {i} (k _ {j}) = \int_ {0} ^ {+ \infty} f (x) g (x) d x, \tag {5}
$$

where $x$ is the independent variable of the customer’s data usage, $g ( x )$ is the probability density function of the user’s actual data usage derived through uncertainty modeling, and

2 In theory, it is possible to improve the overall reselling profit by meticulously dividing the customers into multiple groups and separately devising their optimization strategies. This method, however, is rather ad hoc and datadependent, making the long-term suitability hard to ensure. It also significantly increases the complexity of algorithm design and parameter tuning, but the practical reward may not be able to make up for the increased workload.

$f ( x )$ is the payment function of x under data plan $P _ { i } .$ . For example, f(x) for “\$3.62 for 500 MB plus \$0.01/MB overdraft” is defined as $f ( x ) = 3 . 6 2$ for $0 \leq x \leq 5 0 0$ , and $\textstyle f ( x ) = { \frac { x } { 1 0 0 } } - 1 . 3 8$ for $x > 5 0 0 .$ .

Based on our modeling results in $\begin{array} { r } { \ S ^ { \mathrm { V } - \mathrm { A } . 1 , \ \frac { k _ { j } ^ { \prime } } { k _ { i } } } } \end{array}$ follows a certain distribution. Assume we use SVR-RBF or ULR whose prediction results follow a normal distribution $N ( 1 , \sigma ^ { 2 } )$ . In this case, the maximum likelihood estimation $\hat { \sigma } ^ { 2 }$ is:

$$
\hat {\sigma^ {2}} = \frac {1}{m} \sum_ {j = 1} ^ {m} \left(\frac {k _ {j} {} ^ {\prime}}{k _ {j}}\right) ^ {2} - 1. \tag {6}
$$

From the historical data of V-Mobile, we calculate σˆ to be 0.04 for SVR-RBF and 0.22 for ULR.

To calculate Equation (5), we first rewrite it as a sum of two integrations $\begin{array} { r } { \hat { \int _ { 0 } ^ { S } { f ( x ) g ( x ) d x } } + \int _ { S } ^ { \infty } { f ( x ) g ( x ) d x } } \end{array}$ , where S is the data plan size (e.g., 500 MB in the above example), due to the piecewise nature of f (x). We then apply the rectangle method [36] to numerically calculate each integration.

Evaluation. To assess the effectiveness of the above method, we apply it to the historical usage data of V-Mobile users between January 2016 and October 2017 (obtained from the MonthlyDataset), to optimize the reselling profit for the billing cycle of November 2017. The key evaluation metric, profit rate (PR), is defined as $P R = ( m _ { 1 } - m _ { 2 } ) / m _ { 2 }$ where m1 is the total expense that customers pay V-Mobile, and $m _ { 2 }$ is the cost that V-Mobile pays B-Mobile. A higher PR is always preferred by V-Mobile. Note that a PR may be negative. We compare four optimization methods as follows:

• The Current Approach employed by V-Mobile, learned by us based on our communication with the company, works as follows: in each month, V-Mobile estimates each user’s usage in the next month simply by calculating the arithmetic mean of all historical months’ usage. V-Mobile then purchases the cheapest data plan (with the overdraft cost taken into account) from B-Mobile based on this rough usage estimation. We apply this method to our data and calculate the overall PR to be 3.5%.   
• Machine Learning Only. For each customer, V-Mobile employs machine learning (SVR-RBF with Grubbs’ Test and neighbor mean interpolation, see §V-A.1) to predict next month’s data usage, and then determines the data plan to be purchased from B-Mobile accordingly. This approach yields an overall PR of 4.4%.   
• Machine Learning with Uncertainty Estimation. We apply the full method in §V-A.1 and §V-A.2 that combines the machine learning (SVR-RBF) and statistical uncertainty estimation. This approach leads to an overall PR of 5.6%, which is 60.0% higher than V-Mobile’s current approach and 27.3% higher than the ML-only approach. We find that the significant increase of PR is attributed to better selections of B-Mobile’s data plans for customers with a short lifetime. For such customers with insufficient training samples, per-user machine learning is oftentimes ineffective. Instead, the cross-user prediction accuracy modeling (§V-A.1) can provide a more reasonable estimation of the expected expense $( p _ { i } ( k _ { j } ) )$ based on the “big data.”   
• The Optimum. To estimate the upper bound of the profit that V-Mobile can make, we use the ground-truth data, i.e., customers’ actual data usage in Nov. 2017, to compute the optimal data plan selection. This leads to a PR of 6.2%, only 10.7% higher than our achieved PR of 5.6%.

![](images/75e10ac1b34e46b0b77fe0a1adaa1727826c2934c81692e008efe34628f54b66.jpg)



Fig. 13. Top features ranked by the Spearman’s rank correlation coefficient.

# B. Customer Churn Profiling and Mitigation

Customer churn refers to when a customer ceases her relationship with a company (in our case, canceling her cellular service or dropout). Its mitigation is extremely important for both base carriers and MVNOs because of the high expense that a carrier needs to pay to recruit new customers.

Correlation Analysis. We seek answers to the following key question: which properties (features) of customers are good indicators of their forthcoming service cancellation? Understanding this is a key prerequisite of performing effective churn management in order to retain customers. We take a data-driven approach to address this problem. Specifically, we first compile a set of 12 features that cover a wide range of properties of users’ personal, data usage, and performance. Obtained from UserDataset and MonthlyDataset, the 12 features are listed as follows: gender, age, lifetime, data plan, monthly data usage, monthly expense, monthly uplink bytes, monthly downlink bytes, roaming events, account balance, state update performance (§V-C), and device type. For each of a user’s billed months, we generate a vector containing the 12 features, and obtain a binary label representing the churn state (whether the user has canceled her service) in the next month. To further enrich the feature set, we extend the features with numerical values by computing statistical functions such as mean(), median(), stdev(), and mean\_diff() (mean of the first order difference) over the user’s past months.

We next study the correlation between each of the features and the label (the churn state of the next month) across all customers’ billed months. We compute the Spearman’s rank correlation coefficient [37], a robust, nonparametric measure of the dependency between the rankings of two statistical variables. The coefficient ranges between −1.0 (negative correlation) and +1.0 (positive correlation). We include both the active and dropout users (about 1 million in total) in this study. Figure 13 lists the top 8 features that have the strongest correlations with the customer churn. We make several observations as detailed below. To help quantify our findings, we define a metric called Dropout Contribution (DC), which is the percentage of dropout users with certain properties (e.g., having a specific lifetime range) among all dropout users. DC is calculated by examining each user’s features associated with the month in which she dropped out. More detailed analysis of customer churn is presented in our early version [16].

Customer Churn Prediction. Jointly leveraging the above identified features, we consider proactively predicting the customer churn. Customer churn prediction has been widely studied in prior work [19], [38], [39]. Nath and Behara applied Naive Bayes to predict customer churn with 50,000 customers’ data, achieving a high precision of 95.33% but a low recall of 59.89% [19]. Hung et al. used Decision Tree to develop customer churn prediction models with

TABLE V CUSTOMER CHURN PREDICTION RESULTS 

<table><tr><td>ML Model</td><td>Precision</td><td>Recall</td><td>F1 score</td></tr><tr><td>Naive Bayes</td><td>76.72%</td><td>50.54%</td><td>0.61</td></tr><tr><td>RBF Neural Network</td><td>81.52%</td><td>91.85%</td><td>0.86</td></tr><tr><td>SVM</td><td>78.79%</td><td>96.89%</td><td>0.87</td></tr><tr><td>Logistic Regression</td><td>92.38%</td><td>85.02%</td><td>0.89</td></tr><tr><td>Decision Tree</td><td>94.45%</td><td>94.10%</td><td>0.94</td></tr><tr><td>Random Forest (RF)</td><td>95.52%</td><td>94.45%</td><td>0.95</td></tr><tr><td>RF with One-Sided Selection</td><td>96.29%</td><td>97.81%</td><td>0.97</td></tr></table>

22,000 customers’ data, gaining high precision (96.21%) and recall (94.55%) [38]. However, as shown in Table V, after applying Decision Tree to our dataset, the precision and recall are lower than those of Random Forest. Tsai and Lu applied back-propagation artificial neural networks (ANNs) to 51,306 customers’ data for churn prediction; the accuracy was 94.32% but the precision and recall were rather imbalanced [39], which resembles the case of RBF Neural Network in Table V.

Compared with the previous work, we perform more comprehensive experiments with a much larger dataset (739,695 customers). We apply mainstream off-the-shelf ML algorithms (Naive Bayes, SVM, Logistic Regression, RBF Neural Network, Decision Tree, and Random Forest) to the 8-dimensional feature vectors (Figure 13), attempting to derive the most suitable algorithm for customer churn prediction. Details of configuring the ML algorithms are omitted for brevity. Unlike the data usage prediction where we build a per-user model, here we construct a single model for all users’ monthly records, to capture the common behaviors regarding service cancellation among V-Mobile customers.

We evaluate the prediction accuracy using 10-fold cross validation based on users. In each fold, we train a model using the monthly records from 90% of the users, and use the trained model to predict the records of the remaining 10% users. The results shown in Table V indicate that the random forest model achieves fine precision (95.52%) and F1 score (0.95), as well a high recall rate (94.45%). On one hand, for the 4.48% of customers who are mispredicted but in fact do not have the tendency to drop out, they will not be negatively affected (but might instead be positively encouraged) by V-Mobile’s actions of retaining customers. On the other hand, we wish to further improve the recall rate, as for the 5.55% dropout customers who are missed by our prediction, failing to retain them will bring considerable financial losses to V-Mobile. Note that recruiting a new customer is much more expensive than retaining an existing customer [11].

In order to increase the recall rate (using Random Forest), we adopt an under-sampling [14] based method called One-Sided Selection (OSS) [15]. This is motivated by our observation that negatives (non-dropouts) are significantly more than positives (dropout users) in our case – the imbalance between positives and negatives could considerably degrade the accuracy of our prediction model [40]. OSS addresses this issue by discarding a portion of negative samples that are borderline or redundant. Here borderline samples lie close to the boundary between the positive and negative regions in classification; they are unreliable because even little noise incurred by a feature can move the sample to the other side of the decision surface. Redundant samples can be substituted by other samples in the dataset, so removing them can better balance positives and negatives.

OSS leverages Tomek links [41] to detect borderline samples. Given two samples x and y (with different churn labels) each having 8 features $\{ x _ { 1 } , x _ { 2 } , \cdot \cdot \cdot , x _ { 8 } \}$ and $\{ y _ { 1 } , y _ { 2 } , \cdots , y _ { 8 } \}$ , the Euclidean distance between x and y, denoted as $\delta ( x , y )$ , is calculated by: $\delta ( x , y ) = \sqrt { \textstyle \sum _ { i = 1 } ^ { 8 } ( x _ { i } - y _ { i } ) ^ { 2 } }$ . The pair $( x , y )$ is called a Tomek link if no sample z exists so that $\delta ( x , z ) <$ $\delta ( x , y )$ or $\delta ( y , z ) \ < \ \delta ( y , x )$ . Then, samples participating in Tomek links are taken as borderline samples.

OSS also constructs a consistent subset C of the training set S to reduce redundant samples [15]. A set $N \subseteq M$ is consistent with M if the 1-nearest-neighbor classifier trained with the samples in N can correctly classify the samples in M . Initially, C contains all the positives in S plus one randomly selected negative sample in S. Then, OSS trains a prediction model using the samples in C and the 1-nearest-neighbor classifier [42], classifies S with the model, and compares the classification results with ground truth. The correctly classified negatives are considered redundant as they can be substituted by the randomly selected negative in C. Finally, OSS moves all the misclassified samples in S to C and removes the borderline negative samples from C, thus generating the new training set.

For a dataset of n samples with k features, the time complexity of OSS is $O ( k n )$ , which is quite small in our case: $n = 7 3 9 , 6 9 5$ and $k = 8$ . Enhanced by OSS, Random Forest achieves an essentially higher recall of 97.81%; meanwhile, the precision is increased to 96.29% and the F1 score is increased to 0.97. The recall rate and precision are both improved, because OSS effectively reduces false negatives that lie on the boundary between positive and negative regions. Such false negatives are turned into true positives with little increase of false positives.

# C. Inaccurate Billing and Delayed Billing State Update

Recall from §II that based on our analysis of the BBSDataset, we find more than 40% of the posts in the V-Mobile BBS concern inaccurate billing or delayed billing state notifications. These problems, if occur, are highly undesired because handling a billing issue requires considerable manual efforts from the customer service team, and problematic billing may also endanger the reputation of an MVNO.

1) Understanding Inaccurate Billing: We manually examine the posts involving billing complaints in the BBSDataset, and identify two issues:

Issue 1. Termination of service despite a positive account balance. A user suddenly loses her access to the cellular data service. Meanwhile, however, she still observes a positive account balance from the V-Mobile’s app or website.

Issue 2. Unexpectedly high monthly charge experienced by customers. A user receives a monthly bill that substantially exceeds her expected cost. Typically, the user believes she has not yet used up her monthly data plan but the received bill charges more than the data plan subscription cost.

In addition, we learn from V-Mobile that their internal billing sometimes also experiences inconsistencies:

Issue 3. Unexpectedly high charge experienced by V-Mobile. V-Mobile notices that for certain customers, the bill that it receives from B-Mobile appears to be higher than what it should be charged, based on its own data usage records of these customers. This does not affect V-Mobile customers’ bills, but causes V-Mobile to lose profit.

![](images/2456717907e83ce7e9b53533c2cbef738397647d302deaa04355812714b83267.jpg)



Fig. 14. B-Mobile-SUR propagation delay in B-Mobile $( D _ { B } )$ .   
![](images/698db465fa179989880512845a9f3a59e7c8747c9ae20f7b872a84e7f3b53cc3.jpg)



Fig. 15. Inter-AC B-Mobile-SUR propagation delay $( D _ { V } ) _ { \ }$

A few studies exist with respect to inaccurate billing in the telecommunication industry [43]–[45]. Daily Mail reported that up to 20M Americans using their end devices were over-charged by 7%-14% [43]. Peng et al. took an in-depth look at the issue of inaccurate billing in 3G data access [44], and found the root cause to be billing message loss. Li et al. noted that the over-/under-billing in 4G/5G cellular edge could come from billing data loss, selfish charging, or both [45]. In the scenario of V-Mobile, however, there is no message loss or selfish charging according to our measurements (so that all data usages are recorded in B-Mobile-SUR and the records in both V-Mobile and B-Mobile are consistent with customers’ actual data usages). We thus infer that B-Mobile does not have the billing message loss issue revealed in [44].

To dig out the root causes of the above issues, we carefully analyze the SURDataset. Our basic analysis methodology is to correlate the two types of SURs. For App-SURs, their delivery takes place in almost real time (typically less than 1 second), so their reception time can be largely regarded as a “ground-truth” of the time when the data is actually consumed. However, App-SURs are only used for troubleshooting purposes due to their low user coverage and the possibility of being tampered/spoofed. In contrast, B-Mobile-SURs are used for the actual billing. However, their delivery may experience high delays. To quantify that, as shown in Figure 2, we use $D _ { B }$ to denote the B-Mobile-SUR propagation delay within B-Mobile, and use $D _ { V }$ to denote the delivery latency from B-Mobile to V-Mobile. We can first calculate $D _ { B } + D _ { V }$ by taking the reception difference between a B-Mobile-SUR and its corresponding App-SUR, and then calculate $D _ { V }$ as a delta between the timestamp field in the B-Mobile-SUR (denoting the time when it leaves B-Mobile’s AC) and its reception time at V-Mobile’s AC. $D _ { B }$ can thus be derived as $( D _ { B } + D _ { V } ) - D _ { V }$ .

Figure 14 and Figure 15 plot the distributions of $D _ { B }$ and $D _ { V }$ respectively. As shown, $D _ { B }$ ranges from several seconds to 2.3 hours, and averages at nearly 16 minutes. $D _ { V }$ ranges from 1 second to 4.3 minutes, with an average of around 2 minutes. We will explain why they are high in §V-C.2.

Given the above finding, we can explain the root causes of the three aforementioned issues (Issue 1 to 3). For Issue 1, we find that the user-perceived account balance, despite being positive, was typically quite low when the user could not access the cellular service. In fact, at the time when the cellular service was terminated by the B-Mobile, the user’s account balance had indeed decreased to zero or negative at B-Mobile’s AC. However, the B-Mobile-SUR had not yet been propagated to V-Mobile’s AC due to the high delay of $D _ { V }$ . Such a billing inconsistency is a unique issue in an MVNO.

For Issue 2, we find that in most cases the user actually had not used up her data plan of the current month. However, at the end of the previous month, due to the high propagation delay $( D _ { B } + D _ { V } )$ , a small portion of the B-Mobile-SURs arrived late at V-Mobile’s $\mathrm { A C } ,$ so V-Mobile was not able to add them to the previous month’s bill. Instead, they were then added to the current month’s bill, making it look unreasonable.

For Issue 3, we owe it to the excessive inter-AC delay $( D _ { V } )$ . Specifically, after a V-Mobile user switches to a different data plan, the subscription is not always delivered from V-Mobile’s AC to B-Mobile’s AC in real time when the inter-AC channel is congested. As a result, before the new data plan actually takes effect at B-Mobile, the user’s subscription will experience inconsistency between V-Mobile and B-Mobile. This inconsistency will be reflected on the next bill that B-Mobile sends to V-Mobile.

2) Reducing Billing State Update Delay: §V-C.1 reveals that the high B-Mobile-SUR propagation delay causes almost all users’ complains on inaccurate billing, as well as the billing inconsistency experienced by V-Mobile. A high $D _ { B }$ is attributed to several reasons including (1) the low priority of the SUR traffic compared to that of the data traffic, so that SURs are only transferred when a base station is idle, (2) the large volume of the SUR traffic contributed by over a million base stations of B-Mobile, (3) the SURs’ multi-hop uploading paradigm where they are typically relayed by multiple base stations, and (4) the complex billing rules incurring high computational overheads at B-Mobile’s AC. Regarding $D _ { V }$ , its delay is mostly caused by the congestion over the inter-AC channel, as the SUR traffic’s high throughput often exceeds the bandwidth of the inter-AC channel, which is realized using commodity wired broadband connectivity over the (also congestion-prone) public Internet.

Several approaches at various protocol layers can be developed to reduce the B-Mobile-SUR propagation delay. They range from simply improving the physical layer infrastructure (e.g., upgrading the inter-AC link) to sophisticated scheduling algorithms that accelerate the control-plane data delivery. We next demonstrate that a simple strategy of aggregating SURs can effectively reduce the bandwidth utilization and thus the congestion incurred by the excessive number of B-Mobile-SURs, leading to reduced latency of B-Mobile-SUR delivery. Moreover, given that the bandwidth of the leased dedicated line between the ACs of B-Mobile and V-Mobile is rather expensive (much more expensive than residential bandwidth), we can also save the bandwidth costs by aggregating the traffic of SURs. Since we have no data or control over B-Mobile, we apply the method to reduce $D _ { V } ;$ but the high-level concept can also be employed to optimize $D _ { B }$ .

To motivate our approach, we make two observations. First, the data usage reported by each SUR is typically small. Figure 16 plots the distribution of the data usage reported by all B-Mobile-SURs we collected. As shown, it ranges from several bytes to up to 30 MB, with an average size of only 69 KB. Second, users typically do not need to know the precise data usage $( e . g .$ , at the granularity of a byte or a kilobyte).

![](images/ccc9f0e92c0b5c48f6aa64909a0a01f9c3a285968b432f21096ab248eac5a285.jpg)



Fig. 16. Distribution of reported data usage in a B-Mobile-SUR.

![](images/9577ce8765fe6aee50ae1dd081ee82915b7d0a4f3b81d393449146bbb6f1b51a.jpg)



Fig. 17. Impact of B-Mobile-SUR aggregation on bandwidth utilization over the inter-AC channel.

Given the above observations, we propose to aggregate (at B-Mobile’s AC) a user’s multiple B-Mobile-SURs containing small data usage reports into a single B-Mobile-SUR that carries a data usage of at least $A g g$ bytes. In this way, the traffic volume over the inter-AC channel can be dramatically reduced. Under the specific inter-AC channel setup of V-Mobile, this can lead to a much lower $D _ { V }$ by suppressing the network congestion over the inter-AC channel. The $A g g$ parameter incurs a tradeoff between the inter-AC traffic volume and the precision of real-time data usage statistics. We set $A g g \ =$ 1 MB because on V-Mobile’s app and website, users’ up-todate data usage is displayed in the unit of a megabyte.

To quantify how the above scheme helps reduce the inter-AC traffic, we conduct a “what-if” analysis. We select a typical week (the first week of 06/2017) and plot the inter-AC traffic throughput in the top curve in Figure 17. We observe a peak throughput of 20+ Mbps, as well as a clear diurnal pattern. We then conduct a trade-driven simulation to study the throughput reduction if our aggregation scheme is deployed. Considering the situation when users seldom use data for a long time t, our aggregation algorithm would lead to an unacceptably long billing state update delay. In order to bound this delay, we have a safeguard mechanism that employs a temporal threshold (100 seconds). When t exceeds the threshold and there are not sufficient data aggregated yet, the state update report will be instantly sent to the AC of V-Mobile. As shown in the bottom curve, performing B-Mobile-SUR aggregation reduces the peak throughput to around 5Mbps.

Finally, we assisted V-Mobile in actually deploying our aggregation scheme by modifying the agent software that V-Mobile installs at B-Mobile’s AC for forwarding B-Mobile-SURs over the inter-AC channel. After the deployment, the inter-AC channel congestion was almost fully eliminated, and the 99-percentile of $D _ { V }$ was reduced to less than one second.

# VI. RELATED WORK

MVNO Measurements. Only a limited number of studies exist on commercial MVNOs. In 2014, Zarinni et al. conducted a first study (based on their claim) of MVNO performance using controlled experiments, and noticed performance-wise differential treatments between some MVNOs and their base carriers [6]. Concretely, they studied the performance of three applications (voice service, web access, and video streaming) in two popular MVNO families in America. Each MVNO family includes three MVNOs and a major carrier. They found that some MVNOs have performance degradation and that two MVNO families do have some essential differences. Also in 2014, Vallina-Rodriguez et al. studied the relationship between many MVNOs and their base carriers, and pinpointed several potential issues for light and thick MVNOs [1]. In 2016, Schmitt et al. noted that a packet may traverse a longer network path in an MVNO network than in the base carrier’s network [7]. Our study differs from theirs in several aspects: the study scale, the examined topics, and the findings.

Cellular Network Performance. Several large-scale measurements have been conducted to understand the cellular network performance [20]–[23]. Huang et al. employed a crowd-sourcing approach to measure 3G network performance on smartphones [20]. They also conducted an in-depth study of the LTE performance using datasets obtained from a cellular ISP [23]. Sommers and Barford compared cellular and WiFi performance using crowd-sourced data in diverse environments [22]. Our study in §IV-B focuses on an MVNO and its base carrier, and provides more up-to-date performance statistics; we also compare our results with [23].

Traffic Prediction and MVNO Economics. A plethora of work on network traffic prediction, such as [25], [46], has been proposed. However as shown in §V-A.1, they are not suited to our long-term, large-scale data usage prediction with limited historical data, so we develop our own approach. Researchers have also conducted analytical modeling and formulation on MVNO economics, such as market sharing between MVNOs and MNOs [47] and leveraging users’ feedback for pricing [18]. Compared to these theoretical studies, our reselling optimization takes a more practical and intuitive approach based on statistical modeling and machine learning. We also evaluate its effectiveness using real MVNO customers’ data.

Customer Churn Mitigation. Customer churn mitigation is critical, as acquiring a new user costs 5–6 times more than retaining an existing user [11]. In fact, the issue has been studied in not only telecom services but also other industries such as insurance [48], news media [49], and banking [50]. Various techniques have been put forward to predict dropout users, including decision trees, support vector machine, neural networks, and ensembles of multiple techniques. We instead consider churn mitigation in the context of MVNO, which has a unique business model and customer-churn characteristics.

# VII. LESSONS LEARNED

To benefit future researches around the MVNO ecosystem, we share our experiences gained in this study.

There exist gaps (pricing, plan type, customer service) between MNOs and their customers, and MVNOs help reduce them, leading to win-win results. Observed from the businesses of V-Mobile and B-Mobile, there exist gaps between MNOs and their customers in three aspects. First, data plans of MNOs are likely to be expensive due to the monopoly of MNOs, which stems from two factors: (1) government policies, and (2) MNOs not allowing customers to shift from one operator to another without changing phone numbers. Second, oftentimes there is a mismatch between the actual data usage of many MNO customers and their data plans because the data plan options of MNOs are very limited. Third, due to MNOs’ monopoly, their customer services are oftentimes not fully up to expectations. Compared to MNOs, MVNOs bring improvement in all the above aspects. First, MVNOs can provide customers with more customized data plans at lower prices through accurate data usage prediction while making profits. Since light MVNOs do not need to deploy and maintain physical infrastructures, they can focus more on improving customer service quality. Furthermore, MVNOs can gain customers that MNOs miss; at the same time MNOs can also obtain revenues indirectly from these missed customers by cooperating with MVNOs [51], leading to a win-win situation.

The development status of full MVNOs in open markets is not as good as expected, especially in terms of network performance and MNO relationship. In §IV-B, our measurement results show that there is no noticeable performance difference between V-Mobile and B-Mobile. However, existing literature [6], [7] noted that full MVNOs appeared to offer inferior performance compared to their base carriers in the U.S. Actually, there exists competition between full MVNOs and MNOs in open markets [52]. Although full MVNOs have their own infrastructures, they also partially rely on their base carriers’ radio base stations [1]. Considering above facts, we can possibly attribute the performance degradation of full MVNOs to two reasons: (1) the performance, reliability, and scalability of their own network infrastructures may not be as good as those of the base carriers’ given full MVNOs’ short history compared to MNOs; (2) additional handovers need to be performed between the infrastructures of full MVNOs and their base carriers. That being said, we suggest that full MVNOs in open markets should focus on not only the network performance of their own infrastructures but also their relationship with the base carriers from both the technical and policy perspectives. Note that in China, the full MVNO market is not yet open due to government policies; only light MVNOs exist and the agreements between light MVNOs and their base carriers tend to be mutually beneficial [53].

Basic statistical methods can effectively mitigate the errors or biases in machine learning-based prediction. In the early version of this study [16], we adopted k-means clustering to filter out outliers in MonthlyDataset and achieved an prediction accuracy of 86.75%. We observed that prediction inaccuracy was oftentimes due to missed outliers and missing samples in MonthlyDataset. To improve this, in our follow-up experiments reported in this paper, we find that basic statistical methods (e.g., Grubbs’ Test with neighbor mean interpolation) can effectively detect outliers and fill in missing samples, eventually increasing the accuracy to 93.3%. Furthermore, in customer churn prediction, we also discover that One-Sided Selection [15] can mitigate the biases caused by the class imbalance problem and increase the recall to 97.81%. These illustrate that customers’ monthly data usages and churn dynamics are roughly in line with specific statistical distributions, which can hint customer behaviour modeling. We believe the same principle is potentially applicable to predicting other key metrics in the cellular ecosystem.

High control-plane signaling load can be effectively reduced through strategically batching delay-tolerant control messages. In §V-C.1, we uncover the root cause of inaccurate billing to be the high billing delay. Reducing the billing delay is challenging, due to the sophisticated billing logic and complex agreements between MVNOs and their base carriers. Our scheme, which has been deployed at V-Mobile, adds the mechanism of SUR aggregation to the agent software that V-Mobile installs at B-Mobile’s AC. Despite such a simple method, the result is encouragingly satisfactory: it successfully reduces 99% of $D _ { V }$ (the delivery latency from B-Mobile to V-Mobile) to less than 1 second. The results indicate the importance of optimizing the cellular-control plane, as well as the effectiveness of batching delay-tolerant control messages in reducing the signaling load.

Our prediction approach for customer churn is also suited to phone fraud detection after moderate adjustments. In §V-B, we describe the prediction approach for customer churn, including feature engineering, correlation analysis, class imbalanced sampling, and the classification algorithm. By leveraging the approach, we successfully achieve a high recall of 97.81% and a fine precision of 96.29%. Moreover, we discover that this approach can also be applied to fraud detection for V-Mobile after moderate modifications. Since MVNOs have no physical stores, the SIM cards can only be authenticated online where most information needed for authentications (e.g., names and citizen ID numbers) may be stolen or forged. Therefore, fraud detection for MVNOs is more important compared to that for traditional carriers.

When applying the prediction approach in §V-B to fraud detection, we extract 16 more features for each customer:

1) total number of outgoing calls,   
2) total number of incoming calls,   
3) avg. number of outgoing calls per day,   
4) number of phone numbers in outgoing calls,   
5) number of phone numbers in incoming calls,   
6) avg. duration of outgoing calls,   
7) proportion of outgoing calls during work hours,   
8) proportion of outgoing calls at night,   
9) avg. interval between consecutive outgoing calls,   
10) ratio of the 1st feature over the 4th feature,   
11) number of days with outgoing calls,   
12) interval between first bill time and activation time,   
13) number of involved BSes for outgoing calls,   
14) number of involved BSes for incoming calls,   
15) usage ration of the most involved BS for outgoing calls,   
16) usage ration of the most involved BS for incoming calls, according to our literature review, statistic calculation, and domain knowledge. The 1st–8th features have been widely used and proved to be effective by existing studies of fraud detection [54], [55]. The 9th–12th features are extracted based on statistic correlation analysis – they are the top 4 features ranked by Spearman’s correlation coefficient. The 13th–16th features stem from our domain knowledge: different from legitimate users whose phone calls typically involve a number of geo-distributed BSes, scammers usually make plenty of calls at the same location and thus the number of involved BSes should be quite small while the usage ration of the most involved BS should be pretty high.

We focus on optimizing precision rather than recall by increasing the confidence threshold of admitting scammer samples, since misclassifying legitimate users as scammers will lead to customer complaints, customer churn, and loss of reputation. By adopting the adjusted approach, we achieve a high precision of 99.31% as well as a satisfactory recall of 97% on about 1 million customers. The ground truth was obtained via public reporting (www.12321.cn) and manual tagging by V-Mobile customers. Given this promising result, we believe our prediction framework can be possibly applied to detect other malicious activities in the MVNO industry and other relevant domains.

# VIII. CONCLUDING REMARKS

We conduct an in-depth investigation of V-Mobile, a large and representative light MVNO with 1 million customers. Our findings shed light on various topics that are of the interests of the stakeholders: MVNO customers, the MVNO carrier, and the base carrier. At a high level, our study delivers several take-away messages. First, MVNOs can leverage the unique demographics and usage patterns of their customers to promote and improve their services. Second, AI and big data can significantly boost the revenue and service quality for MVNOs. Third, the cross-layer and cross-entity interactions, in particular those between an MVNO and its base carrier, need to be better handled. We hope our study can benefit both the MVNO industry and research community in the future.

# ACKNOWLEDGMENT

The authors thank Ao Xiao, Junjie Hou, Congzhi Ku, and Xiaoyu Piao for their help in data collection and analysis.

# REFERENCES

[1] N. Vallina-Rodriguez, S. Sundaresan, C. Kreibich, N. Weaver, and V. Paxson, “Beyond the radio: Illuminating the higher layers of mobile networks,” in Proc. ACM MobiSys, 2015, pp. 375–387.   
[2] Size of the Global MVNO Market From 2012 to 2022. Accessed: Jun. 1, 2018. [Online]. Available: https://www.statista.com/statistics/ 671623/global-mvno-market-size/   
[3] Report: Number of MVNOs Exceeds 1, 000 Globally. Accessed: Jun. 1, 2018. [Online]. Available: https://www.fiercewireless.com/europe/ report-number-mvnos-exceeds-1-000-globally   
[4] A. Nakao et al., “End-to-end network slicing for 5G mobile networks,” J. Inf. Process., vol. 25, pp. 153–163, Jan. 2017.   
[5] MVNOs: Phone Companies Without the Equipment. Accessed: Jun. 1, 2018. [Online]. Available: https://www.theglobeandmail.com/ technology/mvnos-phone-companies-without-the-equipment/ article729367/   
[6] F. Zarinni, A. Chakraborty, V. Sekar, S. R. Das, and P. Gill, “A first look at performance in mobile virtual network operators,” in Proc. Conf. Internet Meas. Conf. (IMC), 2014, pp. 165–172.   
[7] P. Schmitt, M. Vigil, and E. Belding, “A study of MVNO data paths and performance,” in Proc. PAM, 2016, pp. 83–94.   
[8] T. Oshiba, “Accurate available bandwidth estimation robust against traffic differentiation in operational MVNO networks,” in Proc. IEEE Symp. Comput. Commun. (ISCC), Jun. 2018, pp. 00694–00700.   
[9] Xiaomi Mobile. Accessed: Jun. 1, 2018. [Online]. Available: https://www.mi.com/mimobile/   
[10] B. W. Kim and S. H. Seol, “Economic analysis of the introduction of the MVNO system and its major implications for optimal policy decisions in Korea,” Telecommun. Policy, vol. 31, no. 5, pp. 290–304, Jun. 2007.   
[11] A. D. Athanassopoulos, “Customer satisfaction cues to support market segmentation and explain switching behavior,” J. Bus. Res., vol. 47, no. 3, pp. 191–207, Mar. 2000.   
[12] G. L. Tietjen and R. H. Moore, “Some Grubbs-type statistics for the detection of several outliers,” Technometrics, vol. 14, no. 3, pp. 583–597, Aug. 1972.   
[13] M. S. Floater, “Mean value coordinates,” Comput. Aided Geometric Des., vol. 20, no. 1, pp. 19–27, Mar. 2003.   
[14] C. Drummond et al., “C4. 5, class imbalance, and cost sensitivity: Why under-sampling beats over-sampling,” in Proc. Workshop Learn. Imbalanced Datasets II, 2003, pp. 1–8.

[15] M. Kubat et al., “Addressing the curse of imbalanced training sets: Onesided selection,” in Proc. ICML, 1997, pp. 1–8.   
[16] A. Xiao et al., “An in-depth study of commercial MVNO: Measurement and optimization,” in Proc. ACM MobiSys, 2019, pp. 457–468.   
[17] TCCRocks. Accessed: Jul. 18, 2019. [Online]. Available: https://www.tccrocks.com/the-verizon-plan/   
[18] C. Meidanis, I. Stiakogiannakis, and M. Papadopouli, “Pricing for mobile virtual network operators: The contribution of u-map,” in Proc. IEEE Int. Symp. Dyn. Spectr. Access Netw. (DYSPAN), Apr. 2014, pp. 133–136.   
[19] S. V. Nath and R. S. Behara, “Customer churn analysis in the wireless industry: A data mining approach,” in Proc. Annu. Meeting Decis. Sci. Inst., vol. 561, Nov. 2003, pp. 505–510.   
[20] J. Huang, Q. Xu, B. Tiwana, Z. M. Mao, M. Zhang, and P. Bahl, “Anatomizing application performance differences on smartphones,” in Proc. 8th Int. Conf. Mobile Syst., Appl., Services (MobiSys), 2010, pp. 165–178.   
[21] J. Huang, F. Qian, A. Gerber, Z. M. Mao, S. Sen, and O. Spatscheck, “A close examination of performance and power characteristics of 4G LTE networks,” in Proc. 10th Int. Conf. Mobile Syst., Appl., Services (MobiSys), 2012, pp. 225–238.   
[22] J. Sommers and P. Barford, “Cell vs. WiFi: On the performance of metro area mobile connections,” in Proc. ACM IMC, 2012, pp. 301–314.   
[23] J. Huang et al., “An in-depth study of LTE: Effect of network protocol and application behavior on performance,” ACM SIGCOMM Comput. Commun. Rev., vol. 43, no. 4, pp. 363–374, 2013.   
[24] H. Hsu and P. Lachenbruch, “Paired T-test,” in Wiley Encyclopedia of Clinical Trials. Hoboken, NJ, USA: Wiley, 2007, pp. 1–3. [Online]. Available: https://onlinelibrary.wiley.com/   
[25] V. Alarcon-Aquino and J. A. Barria, “Multiresolution FIR neuralnetwork-based learning algorithm applied to network traffic prediction,” IEEE Trans. Syst., Man Cybern., C (Appl. Rev.), vol. 36, no. 2, pp. 208–220, Mar. 2006.   
[26] L. Xiang, X.-H. Ge, C. Liu, L. Shu, and C.-X. Wang, “A new hybrid network traffic prediction method,” in Proc. IEEE Global Telecommun. Conf. (GLOBECOM), Dec. 2010, pp. 1–5.   
[27] Y. Shu, “Wireless traffic modeling and prediction using seasonal ARIMA models,” IEICE Trans. Commun., vol. 88, no. 10, pp. 3992–3999, Oct. 2005.   
[28] H. Drucker, C. Burges, L. Kaufman, A. Smola, and V. Vapnik, “Support vector regression machines,” in Proc. NIPS, 1997, pp. 155–161.   
[29] D. Broomhead and D. Lowe, “Radial basis functions, multi-variable functional interpolation and adaptive networks,” Roy. Signals Radar Establishment, Malvern, U.K., Tech. Rep. 4148, 1988. [Online]. Available: https://apps.dtic.mil/dtic/tr/fulltext/u2/a196234.pdf   
[30] D. E. Rumelhart, G. E. Hinton, and R. J. Williams, “Learning representations by back-propagating errors,” Nature, vol. 323, no. 6088, pp. 533–536, Oct. 1986.   
[31] H. Bourennane, D. King, and A. Couturier, “Comparison of kriging with external drift and simple linear regression for predicting soil horizon thickness with different sample densities,” Geoderma, vol. 97, nos. 3–4, pp. 255–271, Sep. 2000.   
[32] D. L. Donoho and T. P. Y. Yu, “Nonlinear pyramid transforms based on median-interpolation,” SIAM J. Math. Anal., vol. 31, no. 5, pp. 1030–1061, Jan. 2000.   
[33] N. Jiang and L. Wang, “Quantum image scaling using nearest neighbor interpolation,” Quantum Inf. Process., vol. 14, no. 5, pp. 1559–1571, May 2015.   
[34] M. Gasca and T. Sauer, “Polynomial interpolation in several variables,” Adv. Comput. Math., vol. 12, no. 4, p. 377, 2000.   
[35] F. N. Fritsch and R. E. Carlson, “Monotone piecewise cubic interpolation,” SIAM J. Numer. Anal., vol. 17, no. 2, pp. 238–246, Apr. 1980.   
[36] P. J. Davis and P. Rabinowitz, Methods of Numerical Integration. New York, NY, USA: Academic, 1984, pp. 51–198.   
[37] Y. Dodge, Spearman Rank Correlation Coefficient. New York, NY, USA: Springer, 2008, pp. 502–505, doi: 10.1007/978-0-387-32833-1\_379.   
[38] S.-Y. Hung, D. C. Yen, and H.-Y. Wang, “Applying data mining to telecom churn management,” Expert Syst. Appl., vol. 31, no. 3, pp. 515–524, Oct. 2006.   
[39] C.-F. Tsai and Y.-H. Lu, “Customer churn prediction by hybrid neural networks,” Expert Syst. Appl., vol. 36, no. 10, pp. 12547–12553, Dec. 2009.   
[40] R. Akbani, S. Kwek, and N. Japkowicz, “Applying support vector machines to imbalanced datasets,” in Proc. ECML, 2004, pp. 39–50.   
[41] D. Devi, S. K. Biswas, and B. Purkayastha, “Redundancy-driven modified tomek-link based undersampling: A solution to class imbalance,” Pattern Recognit. Lett., vol. 93, pp. 3–12, Jul. 2017.

[42] Q. P. He and J. Wang, “Fault detection using the k-Nearest neighbor rule for semiconductor manufacturing processes,” IEEE Trans. Semicond. Manuf., vol. 20, no. 4, pp. 345–354, Nov. 2007.   
[43] Dailymail Report. Accessed: Jul. 18, 2019. [Online]. Available: https:// www.dailymail.co.uk/sciencetech/article-1388796/Up-20-million-Americans-systematically-overcharged-AT-T-data-usage.html   
[44] C. Peng, G.-H. Tu, C.-Y. Li, and S. Lu, “Can we pay for what we get in 3G data access?” in Proc. 18th Annu. Int. Conf. Mobile Comput. Netw. (Mobicom), 2012.   
[45] Y. Li, K.-H. Kim, C. Vlachou, and J. Xie, “Bridging the data charging gap in the cellular edge,” in Proc. ACM Special Interest Group Data Commun. (SIGCOMM), 2019, pp. 15–28.   
[46] H. Peyravi and R. Sehgal, “Link modeling and delay analysis in networks with disruptive links,” ACM Trans. Sensor Netw., vol. 13, no. 4, pp. 1–25, Sep. 2017.   
[47] M. Debbah, L. Echabbi, and C. Hamlaoui, “Market share analysis between MNO and MVNO under brand appeal based segmentation,” in Proc. 6th Int. Conf. Netw. Games, Control Optim. (NetGCooP), Nov. 2012.   
[48] K. Morik and H. Köpcke, “Analysing customer churn in insurance data– a case study,” in Proc. Eur. Conf. Princ. Data Mining Knowl. Discovery, 2004, pp. 325–336.   
[49] K. Coussement and D. Van den Poel, “Churn prediction in subscription services: An application of support vector machines while comparing two parameter-selection techniques,” Expert Syst. Appl., vol. 34, no. 1, pp. 313–327, Jan. 2008.   
[50] D. Popovic and B. Baši´c, “Churn prediction model in retail banking using fuzzy C-means algorithm,” Informatica, vol. 33, no. 2, pp. 243–247, 2009.   
[51] Yozzo. Accessed: Jul. 18, 2019. [Online]. Available: http://www.yozzo. com/mvno-wiki/mvno-benefits-for-mno   
[52] AEI Report. Accessed: Jul. 18, 2019. [Online]. Available: https://www. aei.org/technology-and-innovation/mobile-virtual-network-operatorsand-competition-in-mobile-markets-lessons-from-canada/   
[53] Qianzhan Report. Accessed: Jul. 18, 2019. [Online]. Available: https://bg.qianzhan.com/report/detail/458/180514-94c96d4b.html   
[54] R. Alves et al., “Discovering telecom fraud situations through mining anomalous behavior patterns,” in Proc. DMBA Workshop, 12th ACM SIGKDD, 2006, pp. 1–6.   
[55] S. Subudhi and S. Panigrahi, “Quarter-sphere support vector machine for fraud detection in mobile telecommunication networks,” Procedia Comput. Sci., vol. 48, pp. 353–359, May 2015.

![](images/1ff31bad83c79162872fb0e6287b1e40099ebc365a35e1dceae3409d3973e4be.jpg)



Yang Li received the B.S. degree from the School of Software, Tsinghua University, in 2018, where he is currently pursuing the M.E. degree with the School of Software. His research areas mainly include big data analysis, machine learning, cloud computing/storage, and network measurement.

![](images/0288e19ebcfe55745cd4159f39ffcf901b693e6cc87525a7f7c44a1d62149658.jpg)



Zhenhua Li (Member, IEEE) received the B.S. and M.S. degrees from Nanjing University in 2005 and 2008, respectively, and the Ph.D. degree from Peking University in 2013, all in computer science and technology. He is currently an Associate Professor with the School of Software, Tsinghua University. His research areas cover cloud computing/storage/download, big data analysis, content distribution, and mobile Internet. He is a member of the ACM.

![](images/8814fc37b44b053bb4ad3c11428faff29ef7a3f21991cde228ba5b81b1b64640.jpg)



Yunhao Liu (Fellow, IEEE) received the B.S. degree from Automation Department, Tsinghua University, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University. He is currently an MSU Foundation Professor and the Chairperson of the Department of Computer Science and Engineering, Michigan State University. His research interests include sensor network and the IoT, localization, RFID, distributed systems, and cloud computing. He is a Fellow of the ACM.

![](images/847b9964c1996345bbe1edff1654b6d43c97e3ca3724b25687d387d02499b796.jpg)



Feng Qian received the B.S. degree from Shanghai Jiao Tong University and the Ph.D. degree from the University of Michigan. He worked at AT&T Labs and Indiana University. He is currently an Assistant Professor with the Computer Science and Engineering Department, University of Minnesota–Twin Cities (UMN). His research interests cover mobile systems, AR/VR, mobile networking (including 5G), wearable computing, real-world system measurements, and system security.

![](images/b2ef2884d0f94f2b5fab4186564276faf641bcf502063addddce65f09a260b81.jpg)



Sen Bai received the B.S. degree from the School of Software Engineering, Huazhong University of Science and Technology, China, in 2008, and the M.S. degree from the Department of Computer Science, Jilin University, China, in 2013, where he received the Ph.D. degree in 2016. From 2017 to 2019, he was a Post-Doctoral Researcher with the School of Software, Tsinghua University. His research interests are in the area of wireless ad hoc networks and intelligent transportation systems.

![](images/03b48c969a133a643386a969445ff70e905c5b2f08988440135e670bb93c51ac.jpg)



Yao Liu (Member, IEEE) received the B.S. degree in computer science from Nanjing University and the Ph.D. degree in computer science from George Mason University. She is currently an Assistant Professor with the Department of Computer Science, Binghamton University. Her research areas include Internet mobile streaming, multimedia computing, Internet measurement and content delivery, and cloud computing.

![](images/9e7fba9a09f78a54abb8ab9d40ee09f630cb08e1be6c8cd9efd28a6e632851db.jpg)



Jianwei Zheng received the B.S. degree from the School of Electronics Engineering and Computer Science, Peking University, in 2019. He is currently pursuing the Ph.D. degree with the School of Software, Tsinghua University. His research areas mainly include big data analysis, network measurement, and cloud computing.

![](images/42b0cf0ac835b60f309ed755f1b9488982be7afdab61926883812629394874e0.jpg)



Xianlong Xin received the B.S. and M.S. degrees in computer science and technology from Nanjing University in 2007 and 2010, respectively. He is a Senior Manager of software engineering with Xiaomi Technology Company, Ltd. He is an expert at the IoT and big data computing.