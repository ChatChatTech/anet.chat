# TruGrid: A Self-sustaining Trustworthy Grid $^{‡}$

Yanmin Zhu $^{*}$ , Jinsong Han $^{*}$ , Yunhao Liu $^{*}$ , Lionel M. Ni $^{*}$ , Chunming Hu $^{+}$ and Jinpeng Huai $^{+}$

\* Department of Computer Science, Hong Kong University of Science & Technology, Hong Kong, China
{zhuym, jasonhan, liu, ni}@cs.ust.hk

$^{+}$ School of Computer Science
Beihang University,
Beijing, China
{hucm, huaijp}@act.buaa.edu.cn

# Abstract

In typical distributed environments, there are two parties: consumers and providers. Consumers have computational jobs while may lack of computational resources. Providers have relatively underutilized resources. With the rapid advancement in high-speed networks, how to enable the effective and secure interaction between consumers and providers has become increasingly important. Because of the distributed ownership of resources, however, it is a very challenging problem. We propose the TruGrid, a Self-sustaining Trustworthy Grid, to solve it. The TruGrid is a novel loosely connected grid system, which guarantees the incentive of every participant and therefore it is a self-sustaining system. We also identify two security challenges arising in the TruGrid, i.e., free-rider and boaster. The proposed trustworthiness management and the penalty model successfully overcome the challenges. Simulation results demonstrate that the TruGrid is a promising actuator to enable the interaction between autonomous consumers and providers.

Keywords: Grid, scheduling, incentive, P2P, security, trustworthiness, penalty

# 1. Introduction

In typical distributed environments, on one hand, some users (resource consumers) have computational jobs, but they may lack computational resources to execute their jobs. On the other hand, some resource owners (resource providers) have relatively underutilized resources. It should be noted that both consumer and provider that we talk about here refer to the possible roles. Any participant can be either a consumer or a provider or both. It is highly desirable for consumers to send jobs to providers for execution. To enable such an interaction, however, is particularly challenging. Both consumers and providers are autonomous and independent of each other, each having its own access policy, scheduling strategy, and optimization objective. The distributed ownership of resources greatly adds the difficulty.

A considerable research has been done on designing scheduling systems. However, these systems made impractical assumptions that providers are voluntary to provide computational resources and have the identical behavior in scheduling, which is not true in practice. Based on the impractical assumptions, those systems failed to enable the mentioned interaction between independent consumers and providers.

Conventional grid systems are usually organized hierarchically and require rigid security mechanisms. To achieve high security, however, always means put more restrictions and cost more expense. The consequence is that rigid grid systems are not flexible in practice. However, grid computing promises to provide high performance and efficiency. In contrast, peer-to-peer (P2P) systems are more loosely connected, in which every participant joins or leaves dynamically. P2P systems have been extremely attractive because of their unique capability to enable free and convenient file sharing among millions of individuals. Security level required by P2P systems is far lower than grid systems. To enable effective interaction between consumers and providers, neither traditional grid systems nor P2P systems can simply be applied. We want a distributed system that has the flexibility of P2P computing and meanwhile has the efficiency of grid computing.

We made great contributions in this paper as follows. We extend both grid computing and P2P computting, and propose the TruGrid, a Self-sustaining Trustworthy Grid, to enable the effective interaction between autonomous consumers and providers. The TruGrid is a novel loosely connected grid system, in which we introduce the economic trading model, and consumers and providers trade with each other. The incentive-based P2P scheduling is proposed to guarantee the incentive of every participant, and therefore the TruGrid is self-sustaining. We also identify two security challenges arising in the TruGrid, i.e., free-rider and boaster. In order to pay less, a consumer may intentionally claim shorter job length than the true job length, which causes the so-called free-rider problem. Similarly, to earn more profit, a provider may claim it could meet the deadline of a job but it actually cannot. We propose the trustworthiness management and the penalty model to secure our TruGrid.

The rest of the paper is organized as follows. Section 2 reviews the related work. In Section 3, we present our approach to building such a self-sustaining trustworthy grid in detail. To evaluate the performance of our approach, we present the simulation results in Section 4. Section 5 concludes the paper by summarizing the conclusion and the future work.

# 2. Related Work

In this section, we give an overview of related work Enterprise [1] is a market-like task scheduler for distributed computing environments. Each idle computer sends estimated task completion time as a bid to the client that initiates the task request. Then the client chooses the computer claiming the earliest completion time to execute the task. The scheduler is not practical for a grid environment in which resources are autonomous, because resource providers have no incentive to bid without benefits.

Spawn [2] is an open, market-based computational system that utilizes idle computational resource in a distributed network of heterogeneous computer workstations. When sellers initiate auctions, buyers bid for CPU slots with given funding. The auctions employed by Spawn are sealed-bid, second-price auctions. "Sealed" means that bidding agents cannot access information about other agents' bids, and "second-price" indicates that the amount paid by the winning agent is the amount offered by the next-highest competitive bidder. The objective of Spawn is the fairness of resource allocation: the number of CPU slots bought is proportional to the amount of funding, which is definitely not sufficient for a market-like grid system. Besides, the seller-initiated auction is suitable only for heavily loaded systems. In a lightly loaded system, the user-initiated auction is proved to outperform the server-initiated one [3].

Nimrod/G [4] is a resource management and scheduling system based on the parameter sweeping system Nimrod. It is built with the Globus toolkit and targets parameter sweeping applications. Nimrod/G comprises a centralized parameter engineer and dispatcher. Every client submits jobs to the parameter engineer and the engineer is responsible for parsing job parameters. The dispatcher distributes the independent subjobs over resources across the whole grid. Nimrod/G makes an attempt to incorporate the economic idea into scheduling. Resources are associated with prices and jobs are given budgets. But in the paper, the authors do not focus on the economic feature, and give no further explanation and implementation of their economic idea over Nimrod/G.

A bid trading mechanism $[5]$ is proposed for exchanging storage resources in P2P networks. A local site wishing to make a copy of a collection announces how much remote space is needed, and accepts bids for how much of its own space the local site must “pay” to acquire that remote space. It is flexible, but it shares the drawback of barter trading systems that only two peers having mutual interests are able to cooperate.

Our previous work [6] tries to build a computational market, which makes the first step to introduce the incentive concept in computational grids. Because of the lack of central control and security mechanisms, however, it is difficult to successfully build a self-sustaining system.

Security issues in P2P systems [7, 8] have been an active research subject. Ngan, et al. [9] proposed distributed architectures for fair sharing of storage resources which are against collusions among nodes. The EigenTrust reputation system is [10] proposed to reduce the number of downloads of inauthentic files in a peer-to-peer file-sharing network. EigenTrust computes for each peer a unique global trust value, based on the peer's history of uploads. By having peers use these global trust values to choose the peers from whom they download, the network is able to identify malicious peers and isolate them from the network.

# 3. Building a Self-sustaining Trustworthy Grid

The goal is to enable the effective interaction among participants. It implies that every participant should benefit from the participation. Taking advantage of the economic model, we consider interaction between consumers and providers as a kind of trading. We exploit E-currency as the media for trading. After a provider successfully completes a job for a consumer, the consumer will pay a certain amount of E-currency to the provider. Here secure transfer of payment is very important. However, how E-currency is managed and transferred between participants is beyond this paper, and therefore will not be discussed here.

# 3.1 Overview

To build a self-sustaining system, we must guarantee sufficient incentive for every participant. The respective incentives are as follows. For consumers, they want to get jobs done while paying as less as possible. For providers, they do want to earn as much as possible. But since the whole amount of the system profit is fixed, if one earns more, then the others earn less. Thus, from the perspective of the whole of the providers, we define the incentive for each provider as follows: the profit of each provider is proportional to the investment for its resources. For example, if provider A has invested for its resources ten times as much as provider B has, then the profit of A should roughly be ten times as much as that of B.

However, since prices of computational resources are changing constantly, it is hard to adapt direct investments as the metric. Instead, we choose computational capability to reflect relative investments, because we have the intuition that a more powerful computer usually means higher investment. The computational capability of any computer is estimated based on the SPEC [11] benchmark, and normalized to the standard platform. The capability of the standard platform is one, and in general, a greater capability means the computer is more powerful. Therefore, the incentive for each provider is that the profit earned is proportional to its capability.

To reach the aforementioned goal, we propose the TruGrid, which is a kind of system that is the middle in between traditional grids and P2P systems. As shown in Figure 1, a centralized unit, the Grid Regulator (GR), is introduced to regulate the operations in the TruGrid. It will not become the bottleneck of system performance, however, because it is only responsible for a limited amount of work. The GR maintains and dynamically adjusts two important things: 1. unit resource price for each provider; 2. trustworthiness for each consumer. Participants are organized into a P2P network. The detail will be explained later.

# 3.2 P2P Scheduling Infrastructure

In such a system, consumers and providers are loosely connected because of the common interest. We assume the availability of P2P network constructing approaches. How the P2P network is constructed and how the overlay can be optimized is out of this paper. Much work [12, 13] has been done for this.

![](images/4b0af873ab0a713f9697cb43528ffca38dc42340980a777d839be6eed6372408.jpg)



Figure 1: System overview

Based on the P2P scheduling infrastructure, the basic trading procedure is as follows:

Step 1: whenever a consumer has a job, it creates a job announcement, and sends it into the P2P network. The job announcement is then forwarded in the network and eventually most providers get it;

Step 2: after a provider gets a job announcement, it estimates whether it can meet the deadline requirement of the job based on the local job queue situation, and decides whether to compete for the job based on this consumer's trustworthiness available at the GR;

Step 3: after waiting for a certain period of time, the consumer may have several replied bids. The consumer selects the provider who charges the least and offers the job to it;

Step 4: an E-contract is signed as the payment certificate and also for solving any possible dispute;

Step 5: being offered the job, the provider inserts the job to the local job queue. If the queue is currently empty, then the job gets executed immediately. After the job is done, the result is sent back;

Step 6: finally, with the help of the E-contract, the payment is transferred at the GR.

Jobs here are computation-intensive and the execution of a job may last hours or even days. A job is characterized by deadline and job length. The job deadline is the time by which the job is required to be completed. The job length is the empirical execution time on a standard platform.

A provider may have many computers, so the provider capability is defined to be the sum of the capabilities of these computers. We assume every computer in a provider executes jobs sequentially, namely, it processes jobs one by one.

# 3.3 Incentive-based P2P Scheduling

Job scheduling in the TruGrid is carried out in a fully distributed fashion, which involves consumers, providers, and the GR. Both consumers and providers are autonomous, and they do decisions independently on their own will. We propose the incentive-based scheduling to guarantee sufficient incentive for each participant. The basic idea of the incentive-based algorithm is that the incentive for consumers is mainly achieved by the active competition among providers, and the incentive for providers is mainly achieved by the price adjusting algorithm.

To achieve fairness among providers, the GR is responsible for setting the unit resource price for each provider, which will be used in the resource trading. The unit resource price refers to the amount of E-currency required to pay for executing each unit length of job. Initially, the unit resource price for every provider is set to the same, which is selected by the GR. If these prices remain unchanged, however, it is extremely difficult to achieve the desired fairness. So we propose the dynamic price adjusting algorithm, with the basic idea that increasing its price can make a provider less competitive, and therefore decrease the profit earned by it, and vice versa.

The strength of the GR is that it has the global information of the grid. The GR is able to know the total jobs generated since every job announcement is broadcast throughout the network. Also, the GR has the knowledge of all providers in the TruGrid. Thus, the ideal profit allocating ratio can be computed as follows

$$
\delta_ {0} = \frac {\sum_ {j} l _ {j} \times p _ {j}}{\sum_ {i} p c _ {i}} \tag {1}
$$

Where $pc_{i}$ is the provider capability of the provider i, and $l_{j}$ and $p_{j}$ are the job length of job j and the unit resource price that the job is charged, respectively.

For each provider, the GR also computes its current profit allocating ratio

$$
\delta_ {i} = \frac {\sum_ {k} l _ {k} \times p _ {k}}{p c _ {i}} \tag {2}
$$

where k is the set of jobs offered to provider i. It is intuitive that if $\delta_{i}$ is less than $\delta_{0}$ , it shows that provider i earned less than is expected to get. Then, the unit resource price of this provider should be decreased so that it becomes more competitive while competing with other providers and therefore gets more job offers and hence earns more profit. Otherwise, it shows provider i earned more than is expected. Then its unit resource price should be increased.

After a consumer sends out a job announcement, it may get many bid replies who claim to meet the job deadline. Among these replies, the consumer will select the one who charges the least. To this end, the consume queries the GR and gets the price list of the providers that replied. Finally, the consumer offers the job to the one which charges the least.

# 3.4 Penalty Model

Different approaches to considering the pending job announcements shows different attitudes towards job competing. There are two extreme attitudes: aggressive and conservative. The aggressive attitude never considers pending job announcement and estimates deadline meeting only based on the current offered jobs. The aggressiveness will result in deadline missing, because it may happen that more than two jobs are offered to the provider, whose deadline meeting estimations are both based on the same local offered job queue. On the contrary, the conservative attitude takes every pending job announcement into account. There are tradeoffs between the aggressive and the conservative attitude. So far, we have implemented the aggressive attitude for its simplicity and good emulation of the real market competition.

Although the unit resource price of each provider is set by the GR, there is another type of problem with providers. In order to make more profit, the provider may boast, i.e., it may claim that it can meet a job's deadline but actually it cannot. The consequence is that the provider may miss the deadlines of some offered jobs.

Both above mentioned problems result in interest lost of consumers involved. To effectively protect the right of consumers, we propose the penalty model which enforces providers to keep promises as much as possible. According to the penalty model, a provider will be penalized if it misses the deadline of a job offered to it. The amount of penalty is proportional to the exceeding time. The more the deadline is exceeded, the more the provider is penalized.

# 3.5 Trustworthiness Management

The charge of a job is computed based on the job length. Therefore, consumers may be not honest when providing the job length information in order to pay less. For example, a consumer has a job with job length 20 hours, but it may claim that the job length is 5 hours. The consequence is that the provider who will be offered the job suffers. This is the so-called free-rider problem, which will lead to an unreliable system.

It is unique here, however, because the environment is a computational grid. We propose the dynamic trustworthiness management which is implemented at the GR to solve the dishonesty problem.

The GR maintains the trustworthiness record of every consumer. The trustworthiness tells how trustworthy a consumer is. With the help of trustworthiness, providers can make better decisions. For those consumers with bad trustworthiness, providers can choose not to do or to do fewer jobs from them. Trustworthiness of consumers should be computed and updated using the information provided by providers. And, to benefit from the trustworthiness management, providers are willing to cooperatively provide truthful observations of consumers to the GR. Based on the observed trustworthiness information from providers, the GR is able to maintain and dynamically update the trustworthiness for each consumer. We denote $\gamma_{i}$ as the trustworthiness of consumer i.

After a provider completes one job, it reports its observation on the trustworthiness of the consumer based on the processing of the job. Let $\beta$ be the observation for the job a.

$$
\beta_ {a} = \left\{ \begin{array}{l l} \frac {t _ {a} \times c _ {k} - j l _ {a}}{t _ {a} \times c _ {k}} & t _ {a} \times p c > j l _ {a} \\ 0 & t _ {a} \times p c <   = j l _ {a} \end{array} \right. \tag {3}
$$

Where $t_{a}$ is the actual processing time for job a, $c_{k}$ is the capability of the computer which executed the job in this provider, and $jl_{a}$ is the job length of job a claimed by the consumer. If the consumer provides the true job length, then the resulting $\beta$ is zero; otherwise, the more the consumer cheats, the greater the resulting $\beta$ is. But in any case, $\beta$ is less than one.

The GR maintains the trustworthiness for each provider. The perfect trustworthiness is zero. Initially, the $\gamma$ of every consumer is set to 0.5, preventing consumers with bad $\gamma$ from leaving the grid and joining again as a new consumer to get a new full $\gamma$ . Basically, to compute the current trustworthiness for each consumer, the GR takes average of observed trustworthiness reported by providers. Suppose that for consumer i, there are already n providers who reported observations. Then once receiving a new report for consumer i, the GR updates $\gamma$ of consumer i as follows.

$$
\gamma^ {\prime} = \frac {\mathrm{n} \times \gamma^ {0} + \beta}{n + 1} \tag {4}
$$

where $\gamma'$ and $\gamma^{0}$ are the new and old trustworthiness, respectively. A greater value means the corresponding provider is less trustworthy.

With the trustworthiness information, a provider can be cautious, in particular, in face of those consumers with poor trustworthiness. Based on the aggressive competing, we propose the following trustworthiness-aware job competing for providers. Whenever the GR receives a new job announcement, it decides whether providers should compete for it or not. The probability to compete is $pb=1-\gamma_{n}$ , where $\gamma_{n}$ is the trustworthiness of the consumer. After a provider gets a job announcement, it firstly consults the GR, and gets the indication. If the decision is not to compete, the provider simply drops this job announcement.

# 4. Simulation Results

To evaluate the performance of our proposed TruGrid, we design extensive simulation experiments.

# 4.1 Simulations Settings

Consumers are independently generating job requests. The arrival of jobs is modeled as a Poisson process. In our simulations, the length of jobs is uniformly distributed, and the deadline is set accordingly based on its job length. For each provider, the capability is normally distributed, because we have the observation that in a certain period, a kind of mainstream computes dominates the market.

In studying the performance of our algorithms, we compare it to the Bare System, which has implemented the incentive-based scheduling, but does not have the security mechanisms, i.e., trustworthiness management and penalty model. The comparisons hopefully allow us to gain the insight of the importance of security mechanisms to be implemented in such a loosely connected grid system.

# 4.2 Providers Results

The first experiment is designed to study the fairness achieved among providers. Before studying the fairness, we define the fairness scale to reflect the fairness expectation for each provider.

$$
\text { fairScale } _ {i} = \frac {\frac {\text { profit } _ {i}}{\sum_ {j} \text { profit } _ {j}}}{\frac {p c _ {i}}{\sum_ {j} p c _ {j}}}
$$

where $profit_{i}$ is the total profit earned by provider i. Ideally, for each provider, the fairness scale is one so that every provider gains sufficient incentive. To study the fairness achieved, we look at the standard deviation (SD) of the fairness scales of the providers.

As show in Figure 2, for both the TruGrid and the Bare System, the fairness is well achieved, because in both systems, the incentive-based scheduling is implemented. As noticed in the figure, the SD is far below 0.01 under any system load configuration.

![](images/b0b14e565a700b892cafb2c4939674b364b842800f52a0ec2817cc208716b524.jpg)



Figure 2: Fairness achieved among the providers

For providers, another concern is penalty. As a whole, the providers of course want to minimize the total penalty because eventually the penalty is distributed to each individual provider. We define the penalty ratio to be the ratio of the total penalty to the total ideal charge.

As illustrated by Figure 3, the TruGrid introduces very low penalty. When the system load is approaching the extreme load, i.e., one, the penalty ratio increases rapidly. It is apparent because at that time providers may miss many deadlines of jobs, and therefore are penalized much. As noticed in the figure, the Bare System introduces no penalty. It is obvious because in the Bare System, no penalty model is implemented. Therefore, by no chance a provider will be penalized.

# 4.3 Consumers Results

For consumers, what they concern most is whether their jobs can be successfully completed before deadlines. Since some consumers may be not honest when providing job length information so as to pay less, we have to distinguish consumers. For those trustworthy consumers, we try to minimize their deadline missing rate, while for those consumers with low trustworthiness, we try to identify them and consequently lower the quality of services for them.

We define the trustworthiness factor (tf) to describe how trustworthy a consumer is. For a consumer, its tf is the ratio of the aggregated fake job length claimed by the consumer to the aggregated true job length. For example, if a consumer always provides a fake job length which is 20% of the true length, its tf is 20%. The tf of fully trustworthy consumers equals to 100%.

![](images/c024642d0e27a4f38cb467f3d7c8f89fd4f94a8051c888dfa5bf24f75a47d9bc.jpg)



Figure 3: Penalty ratio of providers

In the following experiment, there are three categories of consumers, each having tf 20%, 60% and 100%, respectively. As shown in Figure 4, the TruGrid successfully distinguishes the consumers with different level of trustworthiness. In the TruGrid, consumers with a lower tf experience significantly worse quality of services, i.e., higher deadline missing rate. On the other hand, trustworthy consumers are guaranteed to receive good services. On the contrary, the Bare System fails to identify consumers with bad trustworthiness, and all consumers get the same services, which leads to the serious free rider problem.

![](images/ca61b2bab7612c1de1990edb2ea616370b879db71e713d788ddece776ea0ae77.jpg)



Figure 4: Deadline missing rate for individual consumer

Because of the absence of the penalty model, in the Bare System, providers are not afraid to cause deadline missing. Therefore, each provider just competes for jobs as many as possible, not considering its current workload. We design the following experiments to study the importance of the penalty model. Instead of looking at the deadline missing rate of individual consumer, we look at the aggregated deadline missing rate of the whole of consumers. Figure 5 shows that the

TruGrid significantly outperforms the Bare System. From the perspective of the whole, the consumers really benefit from the low deadline missing rate.

![](images/90884d7eb7ee0496618e89a4daad060c3452704dbf0c2225f720319712b2a0a4.jpg)



Figure 5: Deadline missing rate of the whole system

# 5. Conclusions

In this paper, we have proposed the TruGrid, a Self-sustaining Trustworthy Grid, to enable the effective interaction between consumers and providers in a loosely connected system. With the incentive-based scheduling, the TruGrid is a successful self-sustaining system, because the incentive of every participant is carefully guaranteed. The trustworthiness management allows the providers to identify untrustworthy consumers, and consequently behave negatively to these consumers. The penalty model forces providers to keep promises and therefore protects the right of consumers. In conclusion, the TruGrid is a promising actuator to enable the interaction between autonomous consumers and providers.

# References

[1] T. W. Malone, R. E. Fikes, K. R. Grant, and M. T. Howard, "Enterprise: A market-like task scheduler for distributed computing environments," in The Ecology of Computation, B. A. Huberman, Ed.: Amsterdam: north-Holland, 1988, pp. 177-205.   
[2] C. A. Waldspurger, T. Hogg, B. A. Huberman, J. O. kephart, and S. Stornetta, "Spawn: A distributed computational economy," IEEE Transactions

on Software Engineering, vol. 18, pp. 103-177, 1992.   
[3] D. L. Eager, E. D. Lazowska, and J. Zahorjan, "A comparison of receiver-initiated and sender-initiated adaptive load sharing," Performance Evalutaion, vol. 6, pp. 53-68, 1986.   
[4] R. Buyya, D. Abramson, and J. Giddy, "Nimrod/G: an architecture of a resource management and scheduling system in a global computational grid," presented at HPC Asia 2000, 2000.   
[5] B. F. Cooper and H. Garcia-Molina, "Bidding for storage space in a peer-to-peer data preservation system," presented at the 22nd International Conference on Distributed Computing Systems, Vienna, Austria, 2002.   
[6] Y. Zhu, L. Xiao, L. M. Ni, and Z. Xu, "Incentive-Based P2P Scheduling in Grid Computing," presented at International Conference on Grid and Cooperative Computing, Wuhan, China, 2004.   
[7] J. E. Bailes and G. F. Templeton, "Managing P2P security," Communications of the ACM, vol. 47, pp. 95-98, 2004.   
[8] E. Sit and R. Morris, "Security considerations for peerto -peer distributed hash tables," presented at the 1st International Workshop on Peer-to-Peer Systems (IPTPS '02), Cambridge, Massachusetts, 2002.   
[9] T.-W. J. Ngan, D. S. Wallach, and P. Druschel, "Enforcing fair sharing of peer-to-peer resources," presented at the 2nd International Workshop on Peer-to-Peer Systems (IPTPS '03), Berkeley, California, February, 2003.   
[10] S. D. Kamvar, M. T. Schlosser, and H. Garcia-Molina, "the EigenTrust Algorithm for Reputation Management in P2P Networks," presented at the Twelfth International World Wide Web Conference, 2003.   
[11] The Standard Performance Evaluation Corporation (SPEC) Home Page, http://www.specbench.org/, April, 2004   
[12] Z. Xu, C. Tang, and Z. Zhang, "Building topology-aware overlays using global soft-state," presented at 23th IEEE International Conference on Distributed Computing Systems, Providence, RI, United States, 2003.   
[13] Y. Liu, Z. Zhuang, L. Xiao, and L. M. Ni, "A distributed approach to solving overlay mismatching problem," presented at 24th International Conference on Distributed Computing Systems, Hachioji, Tokyo, Japan, 2004.