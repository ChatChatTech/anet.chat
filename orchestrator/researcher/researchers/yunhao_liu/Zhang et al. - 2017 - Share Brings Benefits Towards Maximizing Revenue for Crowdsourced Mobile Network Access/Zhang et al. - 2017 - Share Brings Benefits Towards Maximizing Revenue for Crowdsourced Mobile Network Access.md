# Share Brings Benefits: Towards Maximizing Revenue for Crowdsourced Mobile Network Access

Yi Zhang $^{*}$ $^{\dagger}$ , Yuan He $^{\dagger}$ , Jiliang Wang $^{\dagger}$ , Yanrong Kang $^{*}$ , Daibo Liu $^{\ddagger}$ , Bo Li $^{*}$ and Yunhao Liu $^{\dagger}$

\*Department of Computer Science and Engineering, Hong Kong University of Science and Technology

$^{\dagger}$ School of Software and TNLIST, Tsinghua University

$^{\ddagger}$ University of Electronic Science and Technology of China

Email: {yzhangbh,ykangaa,bli}@cse.ust.hk, {heyuan,jiliangwang,yunhao}@tsinghua.edu.cn, dbliu.sky@gmail.com

Abstract—Crowdsourced mobile network access (CMNA), in which mobile users can share their Internet access with others, is a promising paradigm for addressing users' increasing needs for ubiquitous connectivity and alleviating cellular network congestion. In this paper, we study the operator-assisted CMNA model, in which a mobile virtual network operator (MVNO) incentivizes its subscribers to operate as mobile WiFi hotspots (hosts) through reimbursement and gets revenue from the relayed traffic. Despite of the promising performance, practical strategies for MVNO and hosts have not been studied yet. Existing works usually assume both MVNO and hosts can obtain complete information, and ignore the accompanied overhead in backhaul and privacy threats to users. Such assumptions are unrealistic in practice. To address this issue, we first systematically characterize the revenue loss for both MVNO and hosts with incomplete market information. Based on the analysis, we propose a novel partial cooperation strategy (PCS) to enable appropriate information exchange between MVNO and hosts with little overhead. With adaptive reimbursement and subtle information control, our PCS efficiently improves MVNO's revenue at equilibrium, and also satisfies the hosts' rationality. Through extensive evaluation on data from the real world, we demonstrate our PCS can improve MVNO's revenue by 23% at equilibrium, compared with the results without PCS.

# I. INTRODUCTION

Due to the fast development of communication techniques and mobile applications, cellular networks are entering the epoch of data explosion [1]. Though billions of dollars has been invested on infrastructure update, the capacity of cellular infrastructures such as base stations, is still inadequate to hold all users' communication needs, especially when the number of mobile users is continuously increasing. In this context, crowdsourced mobile network access (CMNA) [2], where mobile users can share their Internet access with others, offers a low cost solution to alleviate network congestion and satisfy users' communication needs.

In this paper, we consider a prominent commercial CMNA model, the operator-assisted CMNA model $[3]$ , $[4]$ . In this model, a mobile virtual network operator (MVNO) incentivizes its subscribers to operate as mobile WiFi hotspots through reimbursement and gets revenue from the relayed traffic. Unlike traditional mobile network operators (MNOs), MVNO is a special wireless service provider. On one hand, it does not own radio spectrum and/or wireless network infrastructure, but leases these resources from MNOs at wholesale prices. On the other hand, it benefits from providing services to its own subscribers at retailing prices. As illustrated in Fig.1, the MVNO buys the data resource from an MNO and charges its subscriber, marked with red, a fee for data usage. The uniqueness of the model is that MVNO allows its subscriber to operate as a WiFi AP, or MiFi (called host). The host can provide network access to other mobile users (called clients), who are not MVNO's subscribers but within the vicinity. When providing WiFi access to clients, the host only shares its cellular connection of the device and does not pay for the clients' data. To incentivize hosts to share their network access, MVNO will return some revenue to hosts, e.g., reimbursing hosts some free data quota for the traffic they relay [4].

![](images/5bfc2a4cd155ff0501b9a5fddcb02f26ebe90412177f36c82596369383c4d650.jpg)



Fig. 1: The CMNA model. MVNO incentivizes its subscriber, marked with red, to provide WiFi connections and gets revenue from the relayed traffic.

In a nutshell, the operator-assisted CMNA model mentioned above innovates a revolutionary network access paradigm. First, operators including both MNO and MVNO can benefit from this model. For MNO, the network congestion can be significantly decreased $[5]$ , which leads to lower infrastructure maintenance and update cost $[6]$ . MVNO can also attract data traffic from clients and dynamically extend its active customer group. Second, clients can also use the network more efficiently in terms of energy or data fee $[3]$ , $[7]$ . Third, the hosts also have incentives to participate in the market since they can receive some revenue, e.g., free data quota or monetary revenue, according to their contributions. They only need to pay for the data they actually consume, while not for the data they forward, which will be paid by clients themselves. This simplifies the economic interactions between the hosts and clients and thus, facilitates the adoption of this model in practice.

Different from existing models of MNOs, the core participants in the operator-assisted CMNA model, i.e. MVNO and hosts, can dynamically adjust their strategies, i.e. reimbursement (MVNO) and whether to provide relay services (hosts), based on their own needs. Those features lead to an interactive marketing scenario and make it difficult for MVNO and hosts to determine the optimal strategies in practice. Most of the previous studies assume each participant can obtain complete market information to determine the optimal strategy $[2]$ – $[4]$ , $[8]$ , $[9]$ . However, this assumption is often impractical in the real world. First, it requires significant modifications in backhaul, e.g., adding independent Gateway GPRS Support Node (GGSN) to filter the packets. Second, sharing information with third parties, e.g., MVNOs, may also leak users' privacy and thus, cannot be afforded by MNOs. Given information asymmetry between MVNO and host, it would be hard to maximize their benefits simultaneously. This issue, however, is ignored in previous studies. Further, the strategies of MVNO and hosts are mutually impacted. None of existing studies have considered the dynamic interactions between MVNO and hosts and thus, cannot provide the optimal strategies for them.

To address those issues, we aim at designing a practical mechanism to maximize MVNO's revenue, while also satisfying the hosts' rationality. In practice, such a design faces several challenges. First, the information asymmetry makes it difficult to determine the accurate revenue for both MVNO and hosts. On one hand, the unknown strategies of hosts and other information, e.g., the covered clients, prevent MVNO from determining the accurate revenue. On the other hand, a host is also difficult to determine its optimal strategy because it is affected by the (unknown) contending hosts, clients and MVNO's reimbursement. Second, the behaviors of MVNO and hosts impact each other and change dynamically, which make the revenue evolution sophisticated to analyze.

In order to tackle those challenges, we adopt a game-theoretic analysis and model the interactions between MVNO and hosts as a two-stage Bayesian game. Through systematical characterization, we demonstrate that MVNO's revenue suffers a loss due to information asymmetry and thus, can be further improved. Following the analysis, we introduce a novel partial cooperation strategy (PCS). In PCS, the core participants, i.e. MVNO and hosts, can exchange some useful information to improve their strategies. By subtle control, the exchanged information promotes the system to equilibrium and the participants' privacy is also preserved. Accordingly, the MVNO's revenue is shown to be higher than that without PCS. Compared with traditional strategies [2], [4], [8], [10], our PCS does not require complete information of all participants, and incurs much less overhead in achieving system equilibrium. Moreover, our model, PCS and equilibrium analysis capture a variety of practical issues, including dynamic personal preference of hosts to provide relay services, the energy consumption patterns of hosts and the potential contention between hosts. This is of paramount importance for the expansion of this commercial model in the future.

To summarize, our contributions are highlighted as follows:

\- We introduce a practical framework for the operator-assisted CMNA model and characterize the equilibrium strategies for MVNO and hosts with information asymmetry. To the best of our knowledge, this is the first work to address such a practical yet important issue in the operator-assisted CMNA model.

\- We show that the equilibrium strategy with information asymmetry may lead to the suboptimal revenue. Hence, we design a partial cooperation strategy (PCS) for MVNO and hosts to optimize their strategies. By appropriate information exchange, the revenue for MVNO can be efficiently improved, while the hosts' rationality is also satisfied.

\- We perform extensive evaluation on real data traces. The results demonstrate PCS can efficiently improve MVNO's

revenue by 23% under different conditions, compared with the results without PCS.

The rest of the paper is organized as follows: we first discuss related work in Section 2. Then we present the system models and problem definitions in Section 3. Then we analyze the equilibrium strategies for MVNO and hosts with information asymmetry and demonstrate its drawbacks in Section 4. Following the analysis, we propose our PCS mechanism and corresponding equilibrium strategies in Section 5. We present the evaluation in Section 6 and conclude our work in Section 7.

# II. RELATED WORK

Crowdsourced mobile network access, or user-provided connectivity, enables more flexible and ubiquitous Internet access among mobile users and is becoming a hotspot in the research community. In this section, we first introduce current organizations of CMNA model and then, discuss related issues about its incentive design.

Organization of CMNA. In current CMNA models, there are two organizations: multi-hop and two-hop. A representative instance of the former model is the OpenGarden Project $^{1}$ , where each user (device) may act as a client node (consuming data), a relay node (relaying data to other nodes), or a gateway node (connecting the mesh overlay with the Internet through a WiFi or a cellular connection). However, the routing protocol is hard to design for such a dynamic network, which limits its applications. On the other hand, two-hop CMNA model is more lightweight and practical. In this model, a mobile user can directly connect to cellular network or through the relay services provided by others. This setting simplifies the routing decisions of users, which is adopted in our analysis.

Incentives of CMNA. Several studies [2], [4], [8], [11]–[14] have been conducted in designing incentives of CMNA model. Lu et al. [8] focus on the crowdsourced mobile data offloading scenario and propose the novel concept of perceived valuation to achieve precise valuation. Manshaei et al. [3] study the dynamics of CMNA model by using a simple analytical model. They show that the subscription fee, link quality and the user preferences are important impacting factors for the evolution of CMNA model. Iosifidis et al. [2] design a virtual currency system for user cooperation in CMNA model. Gao et al. [4] design a hybrid pricing strategy for users based on complete system information. However, those works either incur heavy economic interactions between users or set impractical assumptions, such as requiring all information about each participant [2], [4]. In following, we will propose a practical cooperation strategy in the CMNA model and demonstrate its advantage through systematical characterization.

# III. MODELS AND DEFINITIONS

# A. System models

We consider an operator-assisted CMNA model in an area S, which consists of one mobile virtual network operator (MVNO), a set of hosts (MVNO subscribers), and a set of clients (alien subscribers). For hosts, their data usage is directly charged by MVNO. While for clients, their data usage is charged by MVNO only if they access the Internet through hosts' relay services. In our model, we use the pricing scheme from a practical commercial model $^{2}$ , where the price charged by MVNO is the same with that through cellular networks, i.e. MVNO charges no extra fee on clients, considering the fairness of the market. We assume a client can connect to any host within its vicinity. A brief summary of notations is listed in Table.I.

TABLE I: Notations 

<table><tr><td>Parameter</td><td>Description</td></tr><tr><td> $T$ </td><td>The slotted time model</td></tr><tr><td> $\lambda_{h}(i)$ </td><td>The density of hosts in i-th slot</td></tr><tr><td> $\lambda_{c}(i)$ </td><td>The density of clients in i-th slot</td></tr><tr><td> $p_{0}$ </td><td>The wholesale price per byte</td></tr><tr><td> $p$ </td><td>The retailing price per byte</td></tr><tr><td> $\theta_{i}(t)$ </td><td>The reimbursement for host  $i$  at slot  $t$ </td></tr><tr><td> $g_{i}$ </td><td>The weight of host  $i$  on energy consumption</td></tr><tr><td> $D(t)$ </td><td>The total relayed traffic from clients</td></tr><tr><td> $N_{i}^{r}(t)$ </td><td>The number of mobile users within  $r$ </td></tr><tr><td> $d(t)$ </td><td>The cellular link capacity of a host</td></tr><tr><td> $x_{i}(t)$ </td><td>The communication needs of client  $i$ </td></tr><tr><td> $e_{t}$ </td><td>The per-byte transmission energy cost</td></tr><tr><td> $e_{0}$ </td><td>The per-slot basic energy cost of a host</td></tr><tr><td> $J_{M}$ </td><td>The revenue function for the MVNO</td></tr><tr><td> $J_{i}$ </td><td>The revenue function for host  $i$ </td></tr><tr><td> $\Phi_{A}(x)$ </td><td>The probability of PPP at  $x$  with mean  $A$ </td></tr><tr><td> $B(n,p)$ </td><td>Binomial distribution at  $n$  with parameter  $p$ </td></tr></table>

We consider a slotted time model $T = \{1, 2, \ldots\}$ and a periodic mobility model [15] for hosts and clients. Namely, each host and client remain stationary within one slot but may move to another location in the next slot. Under this condition, MVNO updates the reimbursement plan in every slot. Without loss of generality, we denote $N_{h}(t)$ as the number of hosts, which is only known by MVNO. According to the measurements in [8], the distribution of mobile users can be characterized by a Poisson Point Process (PPP) $\Phi$ . We use $\lambda_{h}(t)$ and $\lambda_{c}(t)$ to denote the mean density for hosts and clients. We should note that our analysis can also be applied to other distributions.

# B. The MVNO model

The MVNO pays the MNO, e.g., AT&T, at a price $p_{0}$ per byte. On the other hand, the MVNO charges its hosts and clients at a retailing price p per byte. We should note that other dynamic pricing strategies, e.g., time-dependent pricing policy [6], can also be applied in our model.

The MVNO offers some free data quota to the hosts, as the reimbursement for their engagement in CMNA. Without loss of generality, we denote $\theta_{i}(t)$ as the reimbursement plan for host $i$ , such that he gets $\theta_{i}(t) \cdot x$ free data quota if he relays $x$ bytes from clients.

The main extra revenue for MVNO is from clients. If we denote $D_{i}(t)$ as the amount of relayed traffic from host $i$ , then MVNO's revenue $J_{M}(t)$ can be calculated as:

$$
J _ {M} (t) = \underbrace {p \cdot \sum_ {i} D _ {i} (t)} _ {\text { income }} - \underbrace {\sum_ {i} \left(1 + \theta_ {i} (t)\right) \cdot D _ {i} (t) \cdot p _ {0}} _ {\text { cost }} \tag {1}
$$

$^{2}$ https://yourkarma.com/

![](images/02c0abf7dd8c3e57013cc5a27de4602db752e663bbeaf8050a4d07e30df3af0b.jpg)



Fig. 2: Illustration of the host model.

# C. The host model

We consider a prominent host model shown in Fig.2. On one hand, host's MiFi provides WiFi relay service to clients and itself through an independent cellular link to the base stations. On the other hand, the host can also connect to the Internet through the cellular link of his phone. Given sufficient works in mobile data offloading [16]–[18], we consider host's own network requirement can be always satisfied and will not affect the relay service of its MiFi under this condition.

Then we specify the model parameters for the host model. We denote r as the radius of WiFi communication range for each host. Based on the definition, we denote $N_{i}^{r}(t)$ and $N_{i}^{2r}(t)$ as the number of mobile users (including hosts and clients) within r and 2r, which can be obtained through neighbor discovery or other modern techniques. For analytical tractability, we consider each host within 2r can contend for clients in $N_{i}^{r}(t)$ .

Based on the aforementioned assumptions, the revenue of host i depends on his choice: whether to provide relay service. Accordingly, it can be represented as a 0-1 strategy set: we use $\Theta_{i}(t) \in \{0,1\}$ to denote this strategy set, where $\Theta_{i}(t) = 1$ means he chooses to provide relay service, while $\Theta_{i}(t) = 0$ otherwise. In comparison with previous hybrid setting, the 0-1 strategy setting copes with the fact that the offloaded traffic is often not known by hosts. In addition, it also incurs less overhead for hosts to subscribe to MVNO. Those features make it more feasible to be implemented in practice.

1. Providing relay service. Under this choice, the impact comes from two parts: the income of the free data quota provided by MVNO (positive), and extra cost in providing relay services (negative). For positive revenue, the monetary benefit is calculated as $p \cdot \theta_{i}(t) \cdot x$ , where the amount of relayed traffic is x and the reimbursement plan is $\theta_{i}(t)$ . For negative revenue, we focus on the extra energy cost in providing relay service through his mobile AP.

We use the linear energy consumption model in [7] in which the energy consumption of relaying $x$ bytes in one slot is $e_t \cdot x + e_0$ , where $e_0$ denotes the basic energy consumption and $e_t$ denotes per-byte transmission cost in providing relay service. Notice that different hosts may hold different weight on the same amount of energy consumption. Considering this diversity, we denote $g_i$ as host $i$ 's weight on energy consumption [2], [4]. Without loss of generality, we assume each $g_i$ is drawn from $[g, \overline{g}]$ according to an atomless, right-continuous cumulative distribution function $F$ [10].

If the amount of relayed traffic for host $i$ at $t$ is $D_{i}(t)$ , the

revenue $J_{i}(\Theta_{i}(t))$ can be expressed as follows:

$$
J _ {i} (\Theta (t)) = \underbrace {p \cdot \theta_ {i} (t) \cdot D _ {i} (t)} _ {\text { income }} - \underbrace {g _ {i} \cdot \left(e _ {t} \cdot D _ {i} (t) + e _ {0}\right)} _ {\text { cost }} \tag {2}
$$

Note that the cellular link capacity of mobile AP for each host is also limited. We denote the limitation as $d(t)$ in slot t. Accordingly, $D_{i}(t)$ should satisfy: $D_{i}(t) \leq d(t)$ . In addition, the capacity $d(t)$ may vary over different time slots. For example, when the cellular network is heavily loaded (e.g., in a densely populated area), the capacity for each host may be small. If a host receives too many connection requests, some (random) requests will be denied.

2. Not providing relay service. Under this choice, host i obtains no free data quota and incurs no extra cost. Accordingly, we set $J_{i}(\Theta_{i}(t)) = 0$ under this condition.

# D. The client model

In time slot $t$ , we consider each client $i$ has $x_{i}(t)$ communication needs, depending on the Apps it uses [19]. Following the previous setting, we use a Poisson distribution to denote $x_{i}(t)$ with parameter $\mu$ .

Since the power consumption of cellular connections is usually higher than that of WiFi connections [4], each client will first try to connect to a host for more energy efficient network access at the start of each slot. If the client's connection request is satisfied, $x_{i}(t)$ bytes will be transmitted through WiFi connection and charged by MVNO with price $p$ . Otherwise, e.g., the connection request is denied by a host, the MVNO cannot charge the client.

# E. Problem definition

Our objective is to design an incentive mechanism, such that (1) the expected revenue function $J_{M}(t)$ is maximized at equilibrium and, (2) individual rationality is satisfied, i.e. the expected revenue function of any host i is nonnegative if it chooses to provide relay service. Considering the information asymmetry between hosts and MVNO, we model the interaction between hosts and MVNO as a two-stage Bayesian game: at stage I, MVNO determines the reimbursement plan for each host. Accordingly, each host determine its strategy at stage II based on its reimbursement. In order to characterize the game equilibriums, we resort to backward induction [20]. Namely, we first determine the equilibrium strategy for each host at stage II. Then we derive the optimal reimbursement plan of MVNO at stage I.

# IV. EQUILIBRIUM ANALYSIS WITH INFORMATION ASYMMETRY

First, we analyze the equilibrium strategies with information asymmetry, which exists in current operator-assisted CMNA models [3], [4]. In such a scenario, MVNO offers a homogeneous reimbursement $\theta(t) = \theta_{i}(t)$ to each host i. For convenience of illustration, we denote $J_{M}^{o}(t)$ as MVNO's revenue in this scenario. As aforementioned, we first characterize the equilibrium strategies for hosts. Then we derive the optimal reimbursement $\theta(t)$ for MVNO.

A. Stage II: equilibrium analysis for hosts

Characterizing the equilibrium strategies for a host involves expressing his revenue expectation when he chooses to provide relay service. Without loss of generality, we focus on the strategy of host i in time slot t. Based on the model descriptions in Section.II, we can know that $J_{i}(\Theta_{i}(t))$ is not only affected by reimbursement plan $\theta_{i}(t) = \theta(t)$ (directly), but also by the strategies of other hosts (indirectly). For example, its relayed traffic may be decreased with more contending hosts in $N_{i}^{2r}(t)$ .

However, prior knowledge about other hosts' strategies are usually unknown because each host $i$ preserves some private information, i.e. $g_{i}$ . This fact, together with undetermined number of contending hosts, motivate us to model the interactions among hosts at stage II as a Bayesian Game (BG). Accordingly, we can define the game equilibrium as follows:

Definition 4.1: A strategy profile $\Theta^{*}$ is a Bayesian Nash Equilibrium if $\forall \Theta_{i}(t)^{*} \in \Theta(t)^{*}$ , the following inequality holds:

$$
\mathbb {E} [ J _ {i} (\Theta_ {i} (t) ^ {*} | \Theta_ {- i} (t) ^ {*}) ] \geq \mathbb {E} [ J _ {i} (\Theta_ {i} (t) | \Theta_ {- i} (t) ^ {*}) ], \forall \Theta_ {i} (t) \tag {3}
$$

where $\Theta_{-i}(t)^{*} \triangleq \Theta^{*} / \Theta_{i}(t)^{*}$ .

Then, we have the following theorem:

Theorem 4.1: There exists a pure Bayesian Nash equilibrium at Stage II.

In the sequel, we use “equilibrium” to denote Bayesian Nash equilibrium. Also, we focus on the symmetric equilibrium in which all hosts take the same strategic function $^{3}$ at equilibrium.

Since $\mathbb{E}[J_{i}(\Theta_{i}(t))] = 0$ when $\Theta_{i}(t) = 0$ , analyzing the equilibrium is equivalent to checking the value of $\mathbb{E}[J_{i}(\Theta_{i}(t))]$ when $\Theta_{i}(t) = 1$ . Obviously, when $\mathbb{E}[J_{i}(\Theta_{i}(t))] > 0$ , the condition of equilibrium is obtained given Definition.4.1. Since the revenue function $J_{i}(t)$ monotonously decreases with $g_{i}$ , we can then use Maximize A Posterior (MAP) to determine the equilibrium: if “providing relay service” is the optimal strategy for host i, then other contending hosts with smaller $g_{i}$ should take the same action. Accordingly, we have:

Theorem 4.2: (Equilibrium condition) Without information exchange, the equilibrium strategy for host $i\Theta_{i}(t)^{*}$ equals to 1 only if $g_{i}$ satisfies the following equation:

$$
g _ {i} <   \frac {p \cdot \theta (t) \cdot \mathbb {E} _ {h} [ D _ {i} (t) ]}{e _ {t} \cdot \mathbb {E} _ {h} [ D _ {i} (t) ] + e _ {0}} \tag {4}
$$

$\mathbb{E}_h[D_i(t)]$ denotes the expected relayed traffic from host $i$ 's view, i.e.:

$$
\begin{array}{l} \mathbb {E} _ {h} [ D _ {i} (t) ] = \sum_ {n _ {h} = 0} ^ {N _ {i} ^ {2 r} (t)} \Phi_ {4 \pi r ^ {2} \lambda_ {h} (t)} (n _ {h} + 1) \sum_ {n = 0} ^ {n _ {h}} B (n, F (g _ {i})) \times \\ \left[ e ^ {- \frac {\mu \left(4 N _ {i} ^ {T} (t) - n _ {h}\right)}{4 n + 4}} + d (t) + \mathcal {Q} _ {t} \left(\frac {\mu \left(4 N _ {i} ^ {r} (t) - n _ {h}\right)}{4 n + 4}\right) \right] \tag {5} \\ \end{array}
$$

in which $\mathcal{Q}_{t}(\cdot)$ is a polynome on regularized gamma function $Q(d(t), m\mu)$ : $\mathcal{Q}_{t}(m) = m\mu Q(d(t), m\mu) - d(t)Q(d(t) + 1, m\mu)$ .

Algorithm 1: Maximizing MVNO's revenue with information asymmetry   
Input: The number of clients $\lambda_c(t)$ , the number of hosts $\lambda_h(t)$ ;
Output: Reimbursement $\theta(t)^*$ ;

1 Initialization:
2 $\theta(t)_0 = \frac{p}{p_0} - 1$ ; // Set the initial reimbursement
3 $\Delta\theta_1 = \frac{\xi + \eta}{1 + \eta}$ ; // Set the initial stepsize
4 $\mathbb{E}[J_M^o(t)]_0 = 0$ ;

5 Loop:
6 $i = 2$ ;

7 while TRUE do
8 $\theta(t)_i = \theta(t)_{i-1} - \Delta\theta_i$ ;
9 $\mathbb{E}[D(t)] = \text{Eq.7}$ ;
10 $\mathbb{E}[J_M^o(t)]_i = (1 - \theta(t)_i) \cdot (p - p_0) \cdot \mathbb{E}[D(t)]$ ;
11    if $\mathbb{E}[J_M^o(t)]_i \neq \mathbb{E}[J_M^o(t)]_{i-1}$ then
12 $\Delta\theta_i = \frac{\xi + \eta}{i + \eta} \cdot \frac{|\mathbb{E}[J_M^o(t)]_i - \mathbb{E}[J_M^o(t)]_{i-1}|}{\mathbb{E}[J_M^o(t)]_i - \mathbb{E}[J_M^o(t)]_{i-1}}$ ;
13    else
14    Return $\theta(t)^* = \theta(t)_i$ ;
15 $i = i + 1$ ;

# B. Stage I: equilibrium analysis for MVNO

At stage I, we consider the scenario where each host takes its equilibrium strategy. Under this condition, MVNO determines its optimal reimbursement $\theta(t)$ such that the expectation of its revenue is maximized, i.e.

$$
\max \quad \mathbb {E} [ J _ {M} ^ {o} (t) ] \quad s. t. \quad \theta (t) > 0 \tag {6}
$$

Then we can readily have the following lemma:

Lemma 4.1: Given the equilibrium condition at stage II, there exists a unique $\theta(t)$ such that $\mathbb{E}[J_M^o (\theta (t))]$ is maximized at stage I.

In order to derive the optimal $\theta(t)$ , the key is to obtain $\mathbb{E}[D(t)]$ . Following the analysis in previous subsection, $\mathbb{E}[D(t)]$ can be calculated using the following equation:

$$
\begin{array}{l} \mathbb {E} [ D (t) ] = \sum_ {i} \mathbb {E} _ {M} [ D _ {i} (t) ] \tag {7} \\ = F (g _ {\theta}) \cdot N _ {h} (t) \cdot \mathbb {E} _ {M} [ D _ {i} (t) ] \\ \end{array}
$$

where $F(g_{\theta})$ denotes the probability that host $i$ provides relay service and $\mathbb{E}_M[D_i(t)]$ denotes the expected relayed traffic of a host from MVNO's view:

$$
\begin{array}{l} \mathbb {E} _ {M} \left[ D _ {i} (t) \right] = \sum_ {n _ {h} = 0} ^ {N _ {h} (t)} \Phi_ {4 \pi r ^ {2} \lambda_ {h} (t)} \left(n _ {h} + 1\right) \sum_ {n = 0} ^ {n _ {h}} B (n, F (g _ {\theta})) \times \\ [ e ^ {- \frac {\mu \pi r ^ {2} \lambda_ {c} (t)}{n + 1}} + d (t) + \mathcal {Q} _ {t} (\frac {\mu \pi r ^ {2} \lambda_ {c} (t)}{n + 1}) ] \\ \end{array}
$$

and $g_{\theta}$ denotes the corresponding equilibrium weight, i.e.

$$
g _ {\theta} = \frac {p \cdot \theta (t) \cdot \mathbb {E} _ {M} [ D _ {i} (t) ]}{e _ {t} \cdot \mathbb {E} _ {M} [ D _ {i} (t) ] + e _ {0}} \tag {8}
$$

Given the form of $\mathbb{E}_{M}[D_{i}(t)]$ , it may be difficult to derive the optimal $\theta(t)$ by differentiation. However, we notice that $J_{M}^{o}(\theta(t))$ is concave based on Lemma.4.1. Hence, we propose a gradient descent search algorithm to derive the optimal $\theta(t)$ , whose details are illustrated in Algorithm.1. Typically, we set the starting reimbursement as $\theta(t)_{0} = \frac{p}{p_{0}} - 1$ and decrease

$\theta(t)_0$ progressively until $J_M^o (\theta (t))$ cannot be maximized, based on diminishing stepsize $\Delta \theta_{i}$ :

$$
\Delta \theta_ {i} = \frac {\xi + \eta}{i + \eta}, \quad 0 <   \eta <   \xi \leq 1, i = 1, 2, \dots \tag {9}
$$

where $i$ denotes $i$ -th round and $\xi$ and $\eta$ are two controlling parameters.

Lemma 4.2: The result of Algorithm.1 converges to the optimal MVNO's revenue at equilibrium.

Remark: In this section, we demonstrate the equilibrium strategies for both MVNO and hosts based on probabilistic analysis. However, we should notice that the equilibrium with information asymmetry can be further improved. Considering some impacting factors are not known by MVNO and hosts, e.g., $N_{r}^{2r}(t)$ to MVNO and the number of contending hosts $n_{i}^{h}$ to each host i, the estimation in the expected amount of relayed traffic is not accurate for both MVNO and hosts. For each host i, it has to consider all possible numbers of contending hosts to guarantee $J_{i}(\Theta_{i}(t)) > 0$ when $\Theta_{i}(t) = 1$ , while the actual number of contending hosts is unique in a single slot. The inaccurate estimation may lead to $\Theta_{i}(t) = 0$ when there are few contending hosts or $\Theta_{i}(t) = 1$ when the number of contending hosts is large. Both conditions lead to the revenue loss for a host. On the other hand, MVNO's reimbursement $\theta(t)$ may not match the actual needs of different hosts given biased estimation. Given the diverse user distributions between different hosts, i.e. $N_{i}^{r}(t)$ , the equilibrium reimbursement $\theta_{i}(t)$ for each host is usually different. Accordingly, the reimbursement $\theta(t)$ may not be adequate to recruit hosts with large $N_{i}^{r}(t)$ , while exceeding the equilibrium reimbursement of those with smaller $N_{i}^{r}(t)$ . This decreases the potential clients and affects the extension of MVNO's service. Thus, the revenue loss from clients, as well as marginal aspects like advertising, also exist in this scenario.

# V. DESIGN AND ANALYSIS OF partial cooperation strategy (PCS)

To improve the equilibrium strategies with information asymmetry, the key is to eliminate the bias in estimating the expected amount of relayed traffic. In order to achieve this goal, we introduce a partial cooperation strategy (PCS) to enable appropriate information exchange between MVNO and hosts, as the means to improve their estimation accuracy. The workflow of PCS is shown in Fig.3.

# A. Design of PCS

In PCS, MVNO and hosts exchange some statistical information with each other at the start of each slot:

- Hosts to MVNO: each host $i$ reports $\{N_i^r(t), N_i^{2r}(t)\}$ and its location to MVNO. By gathering those information, MVNO can determine how many clients exist within a host's vicinity so that it can tune the reimbursement accordingly.   
- MVNO to hosts: MVNO responds the exact number of contending hosts $n_i^h$ in $N_i^{2r}(t)$ to each host $i$ . For host $i$ , $n_i^h$ will be used to determine whether to provide relay services.

Notice that under this condition, the information exchange is asymmetric: the location of a host is not broadcast by MVNO. Therefore, each host's privacy can be well preserved. In addition, the truthfulness of hosts, i.e. reporting true $N_{i}^{r}(t)$

![](images/20b10c987244a9c1af2af5ec5607aa96ed43a0bc01e74c0599449cdae00cb403.jpg)



Fig. 3: The design of PCS mechanism. Each host i reports its neighbors $N_{i}^{r}(t)$ , $N_{i}^{2r}(t)$ and its location to MVNO, while MVNO responds the number of potential contending hosts $n_{i}^{h}$ to each host i.

and $N_{i}^{2r}(t)$ , can also be guaranteed. Based on KS test, MVNO can examine whether the amount of relayed traffic follows the Poisson distribution with the mean $(N_{i}^{r}(t)-n_{i}^{h})\mu$ , where $N_{i}^{r}(t)-n_{i}^{h}$ is the number of in-vicinity clients. If the result is “reject”, MVNO can eliminate the participation of the host. Moreover, the communication overhead is also negligible to hosts since only several numbers are exchanged with MVNO. Hence, those features imply it is practical in the real world.

# B. Analysis of PCS

Similar to the previous section, we utilize backward induction to characterize the equilibriums in this scenario.

1) Stage II: equilibrium analysis for hosts: In this scenario, host $i$ can obtain the exact number of other hosts within $2r$ . Then we have the following theorem:

Theorem 5.1: (Equilibrium condition) With PCS, the equilibrium strategy for host $i \Theta_{i}(t)^{*}$ equals to 1 only if $g_{i}$ satisfies the following equation:

$$
g _ {i} <   \frac {p \cdot \theta_ {i} (t) \cdot \mathbb {E} _ {h} [ D _ {i} (t) ]}{e _ {t} \cdot \mathbb {E} _ {h} [ D _ {i} (t) ] + e _ {0}} \tag {10}
$$

$\mathbb{E}_h[D_i(t)]$ denotes the expected amount of relayed traffic, i.e.:

$$
\mathbb {E} _ {h} [ D _ {i} (t) ] = \sum_ {n = 0} ^ {n _ {i} ^ {h}} B (n, F (g _ {i})) \times
$$

$$
[ e ^ {- \frac {\mu (4 N _ {i} ^ {r} (t) - n)}{4 n + 4}} + d (t) + \mathcal {Q} _ {t} (\frac {\mu (4 N _ {i} ^ {r} (t) - n)}{4 n + 4}) ]
$$

in which $\mathcal{Q}_t(\cdot)$ follows the definition in Theorem.4.2.

2) Stage I: equilibrium analysis for MVNO: For the ease of distinction, we denote $J_{M}^{e}(t)$ as MVNO's revenue in this scenario. Since MVNO can obtain the accurate number of invicinity clients for each host, our goal is to determine the reimbursement array $\theta$ for each host i such that:

$$
\max \mathbb {E} [ J _ {M} ^ {e} (t) ] = (p - p _ {0}) \cdot \sum_ {i} \mathbb {E} [ D _ {i} (t) ] - \sum_ {i} \theta_ {i} (t) \cdot \mathbb {E} [ D _ {i} (t) ] \cdot p _ {0}
$$

$$
s. t. \quad \theta_ {i} (t) \text {   is   optimal, } \quad \forall \theta_ {i} (t) \in \theta \tag {11}
$$

Without loss of generality, we denote $\mathbb{E}[g]$ as the weight expectation, then the optimal $\theta_{i}(t)$ can be calculated as follows:

$$
\theta_ {i} (t) = \frac {\mathbb {E} [ g ] \cdot (e _ {t} \cdot \mathbb {E} _ {M} [ D _ {i} (t) ] + e _ {0})}{p \cdot \mathbb {E} _ {M} [ D _ {i} (t) ]} \tag {12}
$$

In the scenario, MVNO can obtain accurate distribution of hosts and clients based on PCS. Hence, we have: $\mathbb{E}_{M}[D_{i}(t)] = \mathbb{E}_{h}[D_{i}(t)]$ .

Based on the traffic pattern of clients mentioned in Section.II, the expected amount of traffic increases when more clients are covered. Then, solving Eq.11 is equivalent to: finding the set of hosts with minimum cost such that all clients are covered, given the capacity constraint $d(t)$ . Then we have the following theorem:

Theorem 5.2: Maximizing MVNO's revenue (Eq.11) is NP-complete.

Considering this feature of the problem, we propose a heuristic algorithm towards maximizing the expectation of MVNO's revenue, whose details are illustrated in Algorithm.2. Basically, our algorithm consists of three phases:

1) Phase 1: finding the primary host set. We resort to the cost-effectiveness updating algorithm in [21] to determine the primary host set to cover C. Namely, we select the host with the minimum cost of covering one client in each loop, until all clients are covered or all hosts are checked. Under this condition, the capacity constraint is not considered.   
2) Phase 2: calculating the uncovered client set. With respect to the step 1, we simulate the host selection of clients in $s_i$ for each host $i$ , given the capacity constraint $d(t)$ . We repeat this step for $n$ rounds and determine the expected uncovered clients for each host $i$ , i.e. $\mathbb{E}[\overline{\mathcal{C}_i}]$ . By default, we considered a client is uncovered if the probability of unsuccessful connection is larger than 0.5.   
3) Phase 3: updating the primary host set. If there exist uncovered clients and unselected hosts, we return to the phase 1 and repeat the process, until the traffic from all clients can be relayed or $\mathbb{E}[J_M^e (t)]$ cannot be increased.

After finishing those three phases, Algorithm.2 outputs the array $\theta$ to guide MVNO's reimbursement on different hosts. Since all the operations in Algorithm.2 can be done offline, MVNO can thus quickly tune its reimbursement for each host dynamically under different conditions, without the need for trials. Moreover, the algorithm is also scalable on different MVNO's requirements. For example, different MVNOs can apply different host selection models to generate $s_{i}$ for each host i and different possibility thresholds to determine $E[\overline{C_{i}}]$ . In addition, they can also apply different simulation rounds n to control the result accuracy.

Remark: By introducing PCS, the bias in the traffic estimation for MVNO and hosts can be eliminated. The accurate estimation has positive impacts on both MVNO and hosts. On one hand, the expectation of relayed traffic can be determined more accurately for each host i, since the number of contending hosts in $N_{i}^{2r}(t)$ is known. Hence, it can tune the strategy more precisely according to the reimbursement $\theta_{i}(t)$ . On the other hand, MVNO can also estimate the expected amount of traffic provided by each host more accurately. This enables it to personalize the reimbursement $\theta_{i}(t)$ based on the client distribution of each host. For example, it can focus on reimbursing hosts with high client densities to obtain high revenue, while saving monetary cost on hosts with low client densities. Therefore, the overall revenue $\mathbb{E}[J_{M}^{e}(t)]$ at equilibrium can be further improved.

In addition, we should notice that our PCS does not affect normal interactions between hosts and MVNO. First, no location information is exchanged between hosts. This preserves the privacy of hosts and provides incentives for them to participate in the PCS. Second, the weight information is not leaked to neither MVNO nor other hosts. Accordingly, the fairness of the market is still guaranteed such that no one can get extra revenue based on others' information. Therefore, those features indicate our PCS is practical in the operator-assisted CMNA model.

![](images/208b5c84fbf13bdaf1a5050be51b28a929ca66eb1fe5da09b131e7abdbbbecfe.jpg)



(a) Test on RealityMining dataset

![](images/ca979bfd46a484bb4dcff38628e3a18a4b0c1e7f00c87c79faa2a5bb1f862553.jpg)



(b) Test on NCSU Mobility dataset

![](images/9da9372400cb73abdfe188a8560a975987ba576c60b153a83f106a772715e72f.jpg)



(c) Test on LifeMap dataset   
Fig. 4: The per-slot MVNO's average revenue of three mechanisms on three datasets.

Algorithm 2: Maximizing MVNO's revenue with PCS   
Input: Client set of each host $i$ $s_i$ , cost of each host $i$ $c_i$ , client set $\mathcal{C}$ ;
Output: Reimbursement array $\theta = \{\theta_1(t), ..., \theta_k(t)\}$ ;

1 Phase 1: finding the primary host set
2 $S = \theta = \emptyset$ ;
3 while $|S| \neq |\mathcal{C}|$ or not all hosts have been checked do
4 Calculate the cost effectiveness $\alpha_i = \frac{c_i}{|S/s_i|}$ for each host $i$ ;
5 $s_i = \{s_i | i = \arg \min_i \{\alpha_i\}\}$ ;
6 if $\theta_i < \frac{p}{p_0} - 1$ then
7 Update $S = S \cup s_i$ ;
8 Update $\theta = \theta \cup \theta_i(t)$ ;

9 Phase 2: calculating the uncovered client set
10 while repeating for n rounds do
11 Calculating $\overline{\mathcal{C}_i}$ for each host $i$ given capacity $d(t)$ ;

12 Update the remaining client set as $\mathcal{C} = \mathcal{C} - \bigcup \mathbb{E}[\overline{\mathcal{C}_i}]$ ;

13 Phase 3: Updating the primary host set
14 while $\mathcal{C} > 0$ and there exist hosts that can cover $\mathcal{C}$ do
15 Repeat Phase 1&2 with $\mathcal{C}$ ;

16 Return $\theta$ ;

# VI. EVALUATION

We consider a practical system setup based on real traces and demonstrate the comparison experiments in certain representative scenarios. The system parameters follows related experimental studies $[7]$ , $[22]$ .

# A. Experimental setup

Our experiments are built on four datasets:

- RealityMining [23]. The dataset contains the location data of 100 subjects at a MIT building over the course of the 2004-2005 academic year.   
- NCSU Mobility [24]. The dataset contains the mobility traces of 35 people in NCSU over one hour.   
- LifeMap [25]. The dataset contains the mobility data of 12 people over four months at Yonsei University in Seoul.   
- One-week trace from eight base stations located in a major city. The trace records the information of link quality, user density, conversations, application usage and

data transmission for about 1000 users with over one million sessions. We use this dataset to set parameters for hosts and clients under different conditions.

In the experiments, the default slot length is set to 1min. We denote every person in the first three datasets as a potential host and generate clients within its vicinity according to the user distribution of the fourth dataset. The default coverage radius r of a host is set to 30 meters, and its link capacity is set to 30MB/min according to the fourth dataset. While for each client, we use a Poisson distribution to characterize its communication needs in terms of KBytes, whose expectation $\mu$ is 2000KB according to the forth dataset. We adopt the linear energy consumption model in [7] for each host, whose parameters are derived from [2], [22], i.e. $e_{t} = 3.2J/MB$ and $e_{0} = 20J$ . By default, we use a uniform distribution to denote $F(g_{i})$ on $[10^{-4}, 5 \times 10^{-4}]$ . We consider each client can perform perfect CSMA control and there exists a perfect scheduling protocol on each host, such that the communication need of a client can be satisfied if it does not exceed the host's link capacity.

In addition, we should note that the data usage price, which affects MVNO's revenue, depends on the country. In a recent study, ITU reports an average price of 0.021\$/Mbit in US, 0.006\$/Mbit in China, and 0.002\$/Mbit in UK [26]. According to these findings, we set the prices p = 0.003\$/Mbit and $p_{0} = 0.001$ \$/Mbit by default.

In the first three datasets, we conduct comparison experiments of three mechanisms: heterogeneous reimbursement (PCS), homogeneous reimbursement (w/o PCS) and the optimal reimbursement. Each test will be repeated 50 times to eliminate the random error.

# B. Results

1) MVNO's revenue and reimbursement: First, we compare the per-slot MVNO's average revenue of three mechanisms. As shown in Fig.4, our PCS improves the per-slot MVNO's average revenue by $23\%$ , compared with that of w/o PCS. In addition, we also notice that the gap between PCS and the optimal revenue is only around $10\%$ . The main reason is that by introducing PCS, the accurate number of other contending hosts within vicinity can be known by each host, while the potential revenue provided by a host can also be estimated by MVNO. Therefore, MVNO and hosts can determine their strategies more accurately. On the other hand, we also notice that the gap between PCS and w/o PCS varies a lot in different datasets. In RealityMining and LifeMap datasets, the average gap between PCS and w/o PCS is $29.1\%$ while in NCSU

![](images/28db53a5437734a9c266d88c7cafaf75d301439be0c6fad530346415718b99ff.jpg)



(a) Test on RealityMining dataset

![](images/10e6b8e6ae866df95506d9da642fcdc7d1631eb01cae93be108811307d18d7fb.jpg)



(b) Test on NCSU Mobility dataset

![](images/48f0296221f549946caee4d450a1dc74dbadfd5dba2906c8e30d05d45f8a2c32.jpg)



(c) Test on LifeMap dataset

Fig. 5: Comparison of reimbursement ratio $\theta(t)$ between w/o PCS, PCS and optimal (avg). The error bar of PCS depicts the reimbursement range for different hosts.   
![](images/4e069a7d7d6f0d6fe299f9d9c01e4241d84a576062a5faadc588c6cc9793365e.jpg)



Fig. 6: The number of (average) contending hosts with different host density.

![](images/fe4149e3d0bb2f267d285078b58ed9264e0dd1cbca18445bfac41ee9ac0ec7cc.jpg)



Fig. 7: The per-slot MVNO's revenue (PCS) under different client density.

![](images/19758db4019835feb485d139acec2743d5bc0ceb5a6c65458b3d231be5c1de93.jpg)



Fig. 8: The per-slot MVNO's revenue (PCS) under different hosts' capacity.

Mobility dataset, the gap is only 7.2%. To analyze the reason behind this phenomenon, we plot the number of (average) contending hosts in three datasets in Fig.6. As illustrated, we notice the number in the NCSU Mobility dataset is much higher than those in other two datasets. The high density of hosts indicates similar client distributions between them. As a result, the revenue provided by PCS is close to that of w/o PCS.

Further, we evaluate the reimbursement plan $\theta(t)$ in those datasets. First, as shown in Fig.5, our PCS mechanism reduces MVNO's reimbursement plan $\theta(t)$ by 14.1% in average. By designing reimbursement plans according to the reported information, the diversity of hosts is considered and thus, brings more revenue to MVNO while still providing incentives to hosts in this model. Similar to the previous experiments, we also notice that our PCS performs better when there are fewer contending hosts. For example, the reduce of $\theta(t)$ in RealityMining dataset can be as much as 20.2%, while the reduce in NCSU Mobility dataset is only about 4-5%. In addition, we also notice even in crowded environment, maximum $\theta(t)$ is only about 0.05. Given the difference between retailing price and wholesale price mentioned before, this indicates a 20x potential return since MVNO only needs to contribute around 5% of his budget for attracting more clients. Clearly, this result supports the application of this model and provides straightforward instructions of setting reimbursement plan for MVNOs. To the best of our knowledge, this is the first quantification on the impacts of reimbursement plans of this model.

2) Impacts from hosts and clients: In this subsection, we examine the impacts of the density of clients on per-slot MVNO's revenue (provided by PCS). As shown in Fig.7, we notice that MVNO's revenue is generally increased. By increasing the maximum number of in-vicinity clients from 5 to 25, MVNO's revenue is increased by 3.72(2.9x) in the RealityMining dataset, 0.51(1.9x) in the NCSU Mobility dataset, and 0.45(2.7x) in the LifeMap dataset. In addition, we also notice that the increasing trend in the RealityMining and LifeMap dataset is slowed down when the number exceeds 15. This is because in those two datasets, the clients within a host's vicinity usually meet only one host, since the number of contending hosts is near zero in those two datasets (Fig.6). As a result, when the expected number of in-vicinity clients exceeds the serving capacity of a host, i.e., 15, more connection requests are likely to be declined, which slows down the increasing trend. However, this phenomenon is not observed in the NCSU Mobility dataset, since a client usually meets more than 1 hosts. In a word, the results imply the relation between MVNO's revenue and client density is not as simple as linear. Other factors, like the distribution of hosts, also have an important impact on MVNO's revenue.

In addition, we also examine the impacts of hosts' capacity on MVNO's revenue. We set the portion of hosts as 1 and vary their capacity from 10MB to 30MB per slot. As shown in Fig.8, we notice that MVNO's revenue is increased by 3.27(3.3x) in the RealityMining dataset, 0.55(1.8x) in the NCSU Mobility dataset, and 0.25(1.7x) in the LifeMap dataset when the link capacity increases from 10MB to 30MB. The results imply that focusing on recruiting the host with good link quality can offer higher revenue to MVNO, which matches the analysis of equilibrium improvement of PCS.

3) Impacts on cells: Last but not the least, we also analyze the network load change with our PCS in those three datasets. According to [5], the cellular network load is usually affected by the total amount of traffic and the number of concurrent connections. In our scenario, the total amount of traffic remains unchanged since a client will turn to cellular networks if his connection request is declined by a host. As a result, the number of concurrent connections becomes the main impacting factor, which forms our focus. First we examine the impacts of host density on the network load change. As shown in Fig.9a, we observe a sharp decrease of the network load in all those three datasets. The network load is decreased by 50% percent when 50% hosts in RealityMining dataset, 30% hosts in NCSU dataset, and 70% hosts in LifeMap dataset, provide relay services. Second, we also examine the impacts of host capacity on network load change, which is shown in Fig.9b. By varying from 10MB to 30MB, we observe a decrease of 49% in RealityMining dataset, 63% in NCSU Mobility dataset, and 54% in LifeMap dataset. Since the infrastructure maintenance and update takes a large portion of monetary cost on MNOs, our results indicate allowing operator-assisted CMNA model (PCS) can efficiently decrease the network load and thus, save the monetary cost on MNOs, which is worthy of popularization.

![](images/93c6e5fc1c66e1701a981104feeb4e49d77dac6075e0d9728f0b662e373094f2.jpg)



(a) Under different host density

![](images/0f257da789aa7e205db767958e181e7443f86baabe9328529c0efb9c72c50d22.jpg)



(b) Under different host capacity   
Fig. 9: Network load decrease analysis (PCS).

4) Summary: In words, the experimental results show that our PCS coordinates MVNO's adaptive reimbursement with hosts' environments and thus, improves MVNO's revenue at equilibrium. Additionally, our quantitative analysis in reimbursement demonstrates MVNO can get significant revenue back by contributing a small portion ( $\sim5\%$ ) of his budget. This result supports the application of this model, and provides easy-to-use instructions in setting reimbursement. Last but not the least, the results on cells indicate that CMNA model with our PCS could be an effective supplement to modern mobile networks for decreasing network load.

# VII. CONCLUSION

The operator-assisted CMNA model innovates a revolutionary paradigm for mobile Internet access, whose market has not yet been fully exploited. To facilitate its application in the real world, we analyze the equilibrium strategies of two core participants, i.e. MVNO and hosts, in current model and demonstrate its deficiency under information asymmetry. Based on the analysis, we propose a partial cooperation strategy (PCS) to enable appropriate information exchange for optimizing the equilibrium strategies for both MVNO and hosts. The extensive trace-driven numerical studies demonstrate MVNO's revenue can be improved by 23% in average, compared with the revenue without PCS.

# VIII. ACKNOWLEDGEMENTS

The research was support in part by grants from NSFC under grant 61572277, 61532012, a grant from NSFC-RGC (China-HK) under the contract 61361166009, National Natural Science Fund for Excellent Young Scientist No. 61422207, RGC under the contracts 615613, 16211715, C7036-15G (CRF), and a grant from NSF (China) under the contract U1301253.

# REFERENCES

[1] “Vni mobile forecast highlights, 2014 to 2019,” Cisco, Tech. Rep., 2014.   
[2] G. Iosifidis, L. Gao, J. Huang, and L. Tassiulas, “Enabling crowdsourced mobile internet access,” in Proceedings of IEEE INFOCOM, 2014, pp. 451–459.   
[3] M. H. Manshaei, J. Freudiger, M. Félegyházi, P. Marbach, and J.-P. Hubaux, “On wireless social community networks,” in Proceedings of IEEE INFOCOM, 2008, pp. 1552–1560.   
[4] L. Gao, G. Iosifidis, J. Huang, and L. Tassiulas, “Hybrid data pricing for network-assisted user-provided connectivity,” in Proceedings of IEEE INFOCOM, 2014, pp. 682–690.   
[5] M. Z. Shafiq, L. Ji, A. X. Liu, J. Pang, S. Venkataraman, and J. Wang, "A first look at cellular network performance during crowded events," in Proceedings of ACM SIGMETRICS, vol. 41, no. 1, 2013, pp. 17-28.   
[6] S. Ha, S. Sen, C. Joe-Wong, Y. Im, and M. Chiang, “Tube: time-dependent pricing for mobile data,” ACM SIGCOMM Computer Communication Review, vol. 42, no. 4, pp. 247–258, 2012.   
[7] J. Huang, F. Qian, A. Gerber, Z. M. Mao, S. Sen, and O. Spatscheck, "A close examination of performance and power characteristics of 4g lte networks," in Proceedings of ACM MobiSys, 2012, pp. 225–238.   
[8] Z. Lu, P. Sinha, and R. Srikant, “Easybid: Enabling cellular offloading via small players,” in Proceedings of IEEE INFOCOM, 2014, pp. 691–699.   
[9] J. Musacchio and J. Walrand, “Wifi access point pricing as a dynamic game,” IEEE/ACM Transactions on Networking (TON), vol. 14, no. 2, pp. 289–301, 2006.   
[10] T. Luo, H.-P. Tan, and L. Xia, “Profit-maximizing incentive for participatory sensing,” in Proceedings of IEEE INFOCOM, 2014, pp. 127–135.   
[11] J. Li, R. Bhattacharyya, S. Paul, and S. Shakkottai, “Incentivizing sharing in realtime d2d streaming networks: A mean field game perspective,” IEEE/ACM Transactions on Networking, pp. 2119–2127, 2016.   
[12] Q. Ma, L. Gao, Y.-F. Liu, and J. Huang, “A game-theoretic analysis of user behaviors in crowdsourced wireless community networks,” arXiv preprint arXiv:1503.01539, 2015.   
[13] R. Chakravorty, S. Agarwal, S. Banerjee, and I. Pratt, “A mobile bazaar for wide-area wireless services,” Wireless Networks, vol. 13, no. 6, pp. 757–777, 2007.   
[14] T. Yu, Z. Zhou, D. Zhang, X. Wang, Y. Liu, and S. Lu, “Indapson: An incentive data plan sharing system based on self-organizing network,” in Proceedings of IEEE INFOCOM, 2014, pp. 1545–1553.   
[15] M. C. Gonzalez, C. A. Hidalgo, and A.-L. Barabasi, “Understanding individual human mobility patterns,” Nature, vol. 453, no. 7196, pp. 779–782, 2008.   
[16] Y. Zhang, J. Wang, Y. He, X. Ji, Y. Kang, D. Liu, and B. Li, "Furion: Towards energy-efficient wifi offloading under link dynamics," in Proceedings of IEEE SECON, 2016, pp. 1-9.   
[17] Y. Zhang, J. Wang, Y. He, Y. Kang, B. Li, and Y. Liu, “Q-offload: Quality aware wifi offloading with link dynamics,” in Proceedings of IEEE RTSS, 2015, pp. 239–248.   
[18] M. V. Barbera, S. Kosta, A. Mei, and J. Stefa, “To offload or not to offload? the bandwidth and energy costs of mobile cloud computing,” in Proceedings of IEEE INFOCOM, 2013, pp. 1285–1293.   
[19] Y. Zhang, Y. He, X. Wu, Y. Liu, and W. He, "Netmaster: Taming energy devourers on smartphones," in Proceedings of IEEE ICPP, 2014, pp. 301-310.   
[20] D. Fudenberg and J. Tirole, “Game theory mit press,” Cambridge, MA, p. 86, 1991.   
[21] V. Chvatal, “A greedy heuristic for the set-covering problem,” Mathematics of operations research, vol. 4, no. 3, pp. 233–235, 1979.   
[22] N. Ding, D. Wagner, X. Chen, Y. C. Hu, and A. Rice, “Characterizing and modeling the impact of wireless signal strength on smartphone battery drain,” in Proceedings of ACM SIGMETRICS, 2013, pp. 29–40.   
[23] A. Pentland, N. Eagle, and D. Lazer, “Inferring social network structure using mobile phone data,” Proceedings of the National Academy of Sciences (PNAS), vol. 106, no. 36, pp. 15 274–15 278, 2009.   
[24] I. Rhee, M. Shin, S. Hong, K. Lee, S. Kim, and S. Chong, “CRAW-DAD data set ncsu/mobilitymodels (v. 2009-07-23),” Downloaded from http://crawdad.org/ncsu/mobilitymodels/, Jul. 2009.   
[25] Y. Chon, E. Talipov, H. Shin, and H. Cha, “CRAWDAD data set yonsei/lifemap (v. 2012-01-03),” Downloaded from http://crawdad.org/yonsei/lifemap/, Jan. 2012.   
[26] “Measuring the information society,” International Telecommunication Union (ITU), Tech. Rep., 2013.