# Almost Optimal Dynamically-Ordered Multi-Channel Accessing for Cognitive Networks

Bowen Li∗, Panlong Yang∗, Xiang-Yang Li†, Shaojie Tang†, Yunhao Liu‡, Qihui Wu∗

∗ Institute of Communication Engineering, PLAUST

† Department of Computer Science, Illinois Institute of Technology

‡ Department of Computer Science and Engineering, TsingHua University

Abstract—For cognitive wireless networks, one challenge is that the status of the channels’ availability and quality is difficult to predict and quantify. Numerous learning based online channel sensing and accessing strategies have been proposed to address such challenge. In this work, we propose a novel channel sensing and accessing strategy that carefully balances the channel statistics exploration and multichannel diversity exploitation. Unlike traditional MAB-based approaches, in our scheme, a secondary cognitive radio user will sequentially sense the status of multiple channels in a carefully designed ordering. We formulate the online sequential channel sensing and accessing problem as a sequencing multi-armed bandit problem, and propose a novel policy whose regret is in optimal logarithmic rate in time and polynomial in the number of channels. We conducted extensive simulations to compare the performance of our method with traditional MAB-based approach. Our simulation results show that our scheme improves the throughput by more than 30% and speed up the learning process by more than 100%.

# I. INTRODUCTION

In cognitive radio networks, user is regulated to perform spectrum sensing before it transmits over a channel, so as to protect primary user’s communication [1]. Due to hardware limitations, cognitive user can only sense a small portion of the spectrum band at a time1. Thus, properly arranging sensing and accessing policy is critical for improving system throughput as well as reducing access delay. A major challenge in achieving optimal opportunistic channel accessing is the difficulty of predicting the channel status and quality accurately. Online learning schemes, due to the adaptivity and efficiency inherently for dynamic wireless network, have received much attention [2].

Assuming cognitive user could only sense/access one channel at each time slot, existing online channel sensing and accessing solutions often model the learning process as a multi-armed bandit (MAB) problem [3]. Although the one channel per slot scheme is somehow reasonable in periodical and synchronized spectrum sensing system, it fails to exploit instantaneous opportunities among channels, i.e. multichannel diversity. Such diversity is widespread in dynamic spectrum access system, since the available channels are commonly more than users could use, e.g., with half of the US population having more than 20 TV channels available for white-space communication at a time [4]. Meanwhile, compared with the duration of an access time slot, the channel sensing time is typically very short, e.g., the sensing time is about 10ms, and the access duration is typically about 2s in TV band [5].

Motivated by these facts, we investigate the online channel sensing and accessing schemes, where cognitive user is allowed to sense multiple channels sequentially during each time slot. Our objective is to optimize the total throughput achieved during system lifetime by carefully selecting the sequence of channels to be sensed in each time slot. In this way, both long-term statistics and short-term diversity among different licensed channels can be jointly explored and exploited. Note that in our model, the number of channels being sensed in each time slot is a random variable, while for all the previous work applying MAB in dynamic spectrum access [6]–[8], the number of channels sensed in each time slot is a fixed constant, typically one. This distinguishing feature makes the traditional MAB models cannot be used to solve our problem directly.

In this work, we formulate the problem on learning the optimal channel sensing order in a stochastic setting as a new bandit problem, which we referred as a sequencing multiarmed bandit problem (SMAB). In this formulation, we map each sensing order (i.e. a sequence of channels) to an arm. The throughput reward of choosing an arm in a slot is linearly proportional to the remaining transmission time. Observe that the number of arms using this simple mapping is exponential, i.e., it is O N K where N is the total number of channels ( )and K is the maximum number of channels user could sense in one time slot. This complexity brings the first challenge in devising an efficient online learning policy, as traditional MAB solutions [9], [10] would result in exponential throughput loss with the increasing number of channels. Moreover, the rewards from different arms are no longer independent in our model, because multiple channels (up to K channels) could be sensed in one time slot. Consequently, previous results under the assumption of independent arms are no longer applicable to our model, which is the second challenge in analyzing the performance of our scheme.

The main contributions of our paper are as follows. Firstly, we apply the classic UCB1 algorithm [10] to handle the online sequential sensing/accessing problem and analyze the regret value, where the regret is the difference between the expected reward gained by a genie-based optimal choice (i.e., always using the optimal sequential sensing order derived with full channel statistics), and the reward obtained by a given policy. We show that both regret and storage overhead are exponentially increasing with the number of channels N . We then propose an improved policy that we refer to as UCB1 with virtual sampling (UCB-VS) by considering the dependencies between arms, which significantly improves the convergence of the learning process. Finally, we develop a novel algorithm for such sequencing multi-armed bandit problem, called sequencing confidence bound (SCB). We show that the regret is not only logarithmic in time (i.e., orderoptimal rate) but also polynomial in the number of channels. Meanwhile, the storage overhead is reduced from $O ( N ^ { K } )$ to $O ( N )$ .

( )The rest of the paper is organized as follows. We present our system model and problem formulation in Section II. Our novel online sequential channel sensing and accessing policy is presented in Section III. Extensive simulation results are reported in Section IV. We conclude our work in Section V.

# II. SYSTEM MODEL AND PROBLEM FORMULATION

Consider a cognitive radio network with potential channel set $\Omega = \{ 1 , 2 , \ldots , N \}$ . Each cognitive user is operated in Ω = 1 2constant access time (CAT) mode, i.e., user would have a constant duration $T$ once it obtains a communication chance. We denote the duration of each communication chance as a time slot. Denote $a _ { i } ( j ) \in \{ 0 , 1 \}$ as the availability of channel i in the $j ^ { t h }$ ( )slot, where $a _ { i } ( j )$ 1 indicates the primary user ( ) = 0is transmitting over channel i in the $j ^ { t h }$ slot, and $a _ { i } ( j ) = 1$ , ( ) = 1vice versa. We assume channel state is stable during slot time, and independently changes across slots, since the interval time between adjacent communication chances is relatively long in multi-user networks (as discussed in [11]). We consider that the channel idle probability $\theta _ { i } \in [ 0 , 1 ] \ : ( i \in \Omega )$ is not known to [0 1] Ωuser at the beginning, but can be available through learning. For denotation convenience, we sort the channel according to idle probability, where $\theta _ { [ 1 ] } \geq \theta _ { [ 2 ] } \geq . . . \geq \theta _ { [ N ] }$ .

[1] [2] [ ]At each slot, user senses the channels sequentially according to a given sensing order, until it arrives at an idle channel, and transmits over this channel during the remainder of the time slot with data rate R. Each channel sensing is denoted as a step in a slot, which costs a constant time $\tau _ { s } .$ . We denote as the set of all possible sensing orders. Each element in $\Psi ,$ that is $\vec { \psi _ { m } } : = ( s _ { 1 } ^ { m } , s _ { 2 } ^ { m } , \ldots , s _ { K } ^ { m } )$ , is a permutation of the $K$ := (channels, where $K$ 2 )is the maximum number of steps in each decision slot, and $s _ { k } ^ { m }$ denotes the ID of $k ^ { t h }$ channel in $\vec { \psi _ { m } }$ . Correspondingly, K $\begin{array} { r } { \left( N , \lfloor \frac { T } { \tau _ { s } } \rfloor \right) } \end{array}$ (· is rounddown function), and $| \Psi | = M = \left( \begin{array} { c } { { \dot { N } } } \\ { { K } } \end{array} \right)$ K . When the user stops at step k (i.e, $a _ { s _ { k } } = 1$ in current slot), it could obtain = 1an immediate data transmission reward $R \left( T - k \tau _ { s } \right)$ .

We define the deterministic policy $\pi ( j )$ )at each time, mapping from the observation history $\mathcal { F } _ { j - 1 }$ )to a sequence of channels $\vec { \psi } ( j )$ for the $j ^ { t h }$ 1time slot. The problem is how to ( )make sequential decision on sensing order selection among multiple choices, offering stochastic rewards with unknown distribution. Our main goal is to devise a learning policy maximizing the accumulated throughput, i.e.,

$$
\max \lim _ {L \to \infty} \sum_ {j = 1} ^ {L} \mu_ {\pi (j)}
$$

where $\mu$ is the expected reward in one slot time according to an order $\vec { \psi } .$ . Let $\begin{array} { r } { \alpha = \frac { \tau _ { s } } { T } } \end{array}$ . The expected per-slot reward when choosing order $\vec { \psi _ { m } }$ is given by

$$
\mu_ {m} = E \left[ r _ {\vec {\psi} _ {m}} \right] = \sum_ {k = 1} ^ {K} \left\{(1 - k \alpha) \theta_ {s _ {k} ^ {m}} \prod_ {\kappa = 1} ^ {k - 1} \left(1 - \theta_ {s _ {\kappa} ^ {m}}\right) \right\} \tag {1}
$$

Here, rψm $r _ { \vec { \psi } _ { m } }$ is the normalized immediate reward obtained using order $\vec { \psi _ { m } }$ . Without special emphasis, the rewards we talked about are normalized. To obtain the actual throughput, the reward should be scaled by constant factor $R T$ .

Since maximizing accumulated throughput is equivalent to minimizing the regret, we can get

$$
\min \lim _ {L \to \infty} \rho_ {\pi} (L) = L \mu^ {*} - \sum_ {j = 1} ^ {L} \mu_ {\pi (j)} \tag {2}
$$

where $\rho _ { \pi } \left( L \right)$ is the regret after L slots, which is the difference ( )between the reward with optimal sensing order (obtained by a genie) and the reward achieved by the given policy. $\mu ^ { * } =$ $\operatorname* { m a x } _ { m } \left\{ \mu _ { m } \right\}$ =is the expected per slot reward in optimal sensing maxorder.

# III. ALMOST OPTIMAL ONLINE SEQUENTIAL SENSING AND ACCESSING

In this section, we first propose two intuitive methods to construct sensing order selection strategy. The first one directly applies UCB1 [10], and the second one is UCB1 with virtual sampling (UCB1-VS), which is an improved version of UCB1 by exploring the dependency among arms. We analyze the performance of such intuitive methods. Both storage overhead and regret are exponentially increasing with the number of channels $N$ . We then develop a novel algorithm for such SMAB problem, i.e. sequencing confidence bound (SCB), which needs only O N in storage overhead. Moreover, we ( )prove that the regret of SCB is O N K  L , which is in ( log )polynomial order of N and strictly in logarithmic order of time slots.

# A. Solutions Based on UCB1

1) Intuitive UCB1 Algorithm: An intuitive approach to solve the sequencing multi-armed bandit problem is to use the UCB1 policy proposed by Auer et al. [10]. In supporting sensing order selection, two variables are used for each candidate order $\vec { \psi } _ { m } ~ ( 1 \leq m \leq M ) \colon \hat { \mu } _ { m } ( j )$ is the averaged value of 1 ˆ ( )all the obtained rewards of sensing/accessing with order $\vec { \psi _ { m } }$ up to slot $j ,$ and $n _ { m } ( j )$ is the number of times that $\vec { \psi _ { m } }$ has (been chosen up to slot $j .$ . They are both initialized to zero and updated according to the following rules:

$$
\hat {\mu} _ {m} (j) = \left\{ \begin{array}{l l} \frac {\hat {\mu} _ {m} (j - 1) n _ {m} (j - 1) + r _ {m} (j)}{n _ {m} (j - 1) + 1}, & \vec {\psi} _ {m} \text {   is   selected } \\ \hat {\mu} _ {m} (j - 1), & \text { else } \end{array} \right. \tag {3}
$$

UCB1 algorithm   
1: Initialize: $j = 0$ ; for all $1 \leq m \leq M$ : $\hat{\mu}_m = 0$ , $n_m = 0$ 2: for $j = 1$ to $M$ do
3: Sequentially sensing/accessing with order $\vec{\psi}_j$ in $j^{th}$ slot
4: Update $\hat{\mu}_j$ , $n_j$ using Equ. (3)-(4) respectively
5: end for
6: for $j = M + 1$ to $L$ do
7: Sequentially sensing/accessing with order $\vec{\psi}_m$ that maximizes $\hat{\mu}_m + \sqrt{\frac{2\log j}{n_m}}$ in $j^{th}$ slot
8: Update $\hat{\mu}_m$ , $n_m$ using Equ. (3)-(4) respectively
9: end for   
Fig. 1. UCB1 algorithm description

$$
n _ {m} (j) = \left\{ \begin{array}{l l} n _ {m} (j - 1) + 1, & \vec {\psi} _ {m} \text {   is   selected } \\ n _ {m} (j - 1), & \text { else } \end{array} \right. \tag {4}
$$

Then, the intuitive policy can be described as: at the very beginning, choose each sensing order only once. After that, select the order $\vec { \psi _ { m } }$ that maximizes $\begin{array} { r } { \hat { \mu } _ { m } + \sqrt { \frac { 2 \log j } { n _ { m } } } } \end{array}$ 2 log j . The nm ˆ +description of such policy is presented in Fig.1.

The regret of the UCB1 policy is bounded according to the following theorem.

Theorem 1: The expected regret of sequential sensing/accessing under policy UCB1 is at most

$$
\left[ 8 \sum_ {m: \mu_ {m} <   \mu^ {*}} \left(\frac {\log L}{\Lambda_ {m}}\right) \right] + \left(1 + \frac {\pi^ {2}}{3}\right) \left(\sum_ {m: \mu_ {m} <   \mu^ {*}} \Lambda_ {m}\right) \tag {5}
$$

where $\Lambda _ { m } = \mu ^ { * } - \mu _ { m }$

Λ =Proof: See ( [10], Theorem 1).

According to Equ. (5), we conclude that the regret under UCB1 policy is upper bounded in the order $O ( M \log L )$ . As $M = \left( \begin{array} { l } { { N } } \\ { { K } } \end{array} \right) K ! .$ , it can be rewritten as $O ( N ^ { K } \log L )$ . Intuitively, although the UCB1 policy achieves zero-regret (i.e., $\begin{array} { r } { . } { L \to \infty } \frac { \rho _ { \pi } ( \tilde { L } ) } { L } = 0 )  \end{array}$ ρπ(L)L ), it performs poorly in the sequencing lim = 0multi-armed bandit problem, especially when the number of channels is large.

2) Improved UCB1-VS Algorithm: As the reward in our sequencing multi-armed bandit problem is order-related, the orders with identical sub-sequence would result in similar rewards. This basic finding provides us an important hint that we could improve learning efficiency by exploring dependency among arms, e.g., obtaining information about multiple arms by playing a single arm.

The UCB1-VS is developed from UCB1, where only the update process is revised with Virtual Sampling. Specifically, suppose that a user selects an order $\vec { \psi _ { m } } = ( s _ { 1 } ^ { m } , s _ { 2 } ^ { m } , \ldots , s _ { K } ^ { m } )$ s m in a slot and finds that channel $s _ { k } ^ { m }$ = ( 1is idle, then:

• Update statistics of all the sensing order starting with $s _ { 1 } ^ { m } , s _ { 2 } ^ { m } , \ldots , s _ { k } ^ { m }$ m, sm , . . , using reward $1 - k \alpha ;$   
1 2 1• Update statistics of all the sensing order starting with $s _ { k } ^ { m }$ using reward $1 - \alpha$ .

Moreover, in the special case that $K = N \ ( { \mathrm { i . e . , } }$ , user is capable =of sensing all channels in a slot time) and all channels are sensed to be busy, we can conclude that all sensing orders would lead to zero reward in this slot.

Clearly, with virtual sampling, the learning process could be greatly accelerated while the zero-regret property still holds. As analytical result of the precise regret by this UCB1-VS scheme is hard to achieve, we evaluate its performance via extensive simulations in Sec. IV.

# B. A Novel Algorithm for Sequencing Bandit Problem

Although the UCB1 based solutions achieve optimal logarithmic regret over time, they are exponentially increasing with the number of channels. Moreover, as the choices are made according to order-specific statistics, the required storage overhead for supporting decision-making is also exponentially growing with the number of channels. Consequently, when the number of channels for dynamic accessing is large, e.g., more than 50 in the TV band [5], the order-specific methods result in poor performance in regret and unacceptable storage overhead. In this subsection, we propose a novel learning policy for sequencing channel sensing and accessing, in which decisions are made according to channel-related statistics. As a result, the storage overhead is linear with the number of channels. We also proved that the regret of our proposed algorithm is in polynomial order of channels.

1) Algorithm Description: In decision-making process, the channel statistics are learnt by recording and updating the following two variables: $\widehat { \theta } _ { i } ( j )$ and $n _ { i } ^ { s } ( j )$ , where $\widehat { \theta } _ { i } ( j )$ and $n _ { i } ^ { s } ( j )$ ( ) ( ) ( )is the statistic value of idle probability and the times ( )having been sensed for channel i till slot j respectively. They are initialized to zero and updated as follows:

$$
\hat {\theta} _ {i} (j) = \left\{ \begin{array}{l l} \frac {\hat {\theta} _ {i} (j - 1) n _ {i} (j - 1) + a _ {i} ^ {j}}{n _ {i} (j - 1) + 1}, & \text { if   channel } i \text { is   sensed } \\ \hat {\theta} _ {i} (j - 1), & \text { else } \end{array} \right. \tag {6}
$$

$$
n _ {i} ^ {s} (j) = \left\{ \begin{array}{l l} n _ {i} ^ {s} (j - 1) + 1, & \text { if   channel } i \text { is   sensed } \\ n _ {i} ^ {s} (j - 1), & \text { else } \end{array} \right. \tag {7}
$$

Then, the SCB learning policy can be described as follows. Firstly, user will sequentially sense channels until all channels are visited at least once. After that, in time slot j, the user will choose the sensing order $\vec { \psi _ { m } }$ with the maximum $S C B _ { m } ( j )$ , where $S C B _ { m } ( j )$ is defined by

$$
S C B _ {m} (j) = \sum_ {k = 1} ^ {K} \left\{(1 - k \alpha) \theta_ {s _ {k} ^ {m}} ^ {u} (j) \prod_ {\kappa = 1} ^ {k - 1} \theta_ {s _ {\kappa} ^ {m}} ^ {u} (j) \right\} \tag {8}
$$

Here $\begin{array} { r } { \theta _ { i } ^ { u } ( j ) = \hat { \theta } _ { i } ( j ) + \sqrt { \frac { 2 \log j } { n _ { i } ^ { s } ( j ) } } } \end{array}$ 21ogj is the upper confidence bound ( )of the idle probability on channel i up to slot j. The detailed SCB algorithm is presented in Fig.2.

Note that to achieve i $\begin{array} { r } { \vec { \psi } = \arg \operatorname* { m a x } _ { \vec { \psi } _ { m } \in \Psi } S C B _ { m } ( j ) } \end{array}$ is really simpleel sequence with descending order of current channel upper confidence bound $\theta _ { i } ^ { u } ( j )$ will achieve maximum SCB.

SCB algorithm   
1: Initialize: for all $1 \leq i \leq N$ : $\hat{\theta}_{i} = 0$ , $n_{i}^{s} = 0$ ; $S_{0} = \{1, 2, \ldots, N\}$ ; l = 1, k = 1;
2: while $S \neq \emptyset$ do
3:    Sense random channel $i \in S_{0}$ 4:    Update $\hat{\theta}_{i}$ , $n_{i}^{s}$ accordingly
5: $k = k + 1$ , $S_{0} = S_{0} \setminus \{i\}$ 6:    if $a_{i}^{l} = 1$ then
7: $l = l + 1$ , k = 1; access the idle channel
8:    else if $k = K + 1$ then
9: $l = l + 1$ , k = 1; wait for next slot
10:    end if
11: end while
12: for j = l to L do
13:    Sequentially sensing/accessing with $\vec{\psi}$ where $\vec{\psi} = \arg\max_{\vec{\psi}_{m} \in \Psi} SCB_{m}(j)$ 14:    Update $\hat{\theta}_{i}$ , $n_{i}^{s}$ accordingly
15: end for   
Fig. 2. SCB algorithm description

2) Analysis of Regret: Traditionally, the regret of a policy is upper-bounded by the number of times each sub-optimal arm being played. Summing over all sub-optimal arms can get the upper bound. However, our proposed approach requires more finely analysis, since it focuses on the basic elements of each arm (i.e. the sub-sequences in each sensing order). Actually, we analyze the number of times each sub-optimal channel being sensed in each step, and sum up this expectation over all channels and then over all steps. Our analysis provides an upper bound polynomial to N and logarithmic to time. We present our analytical result in the following theorem.

Theorem 2: The expected regret of sequential sensing/accessing under the SCB policy is at most

$$
\Phi (L) K \left[ N - \frac {K + 1}{2} - \frac {\alpha (K + 1) (3 N - 2 K - 1)}{6} \right]
$$

where $\begin{array} { r c l } { { \Phi ( L ) } } & { { = } } & { { \frac { 8 \log L } { \Delta _ { m i n } } + \Bigl ( 1 + \frac { \pi ^ { 2 } } { 3 } \Bigr ) \Delta _ { m a x } , } } \end{array}$ and $\Delta _ { m i n }$ 8 logmin $\begin{array} { r } { \operatorname* { m i n } _ { i , j } | \theta _ { i } - \theta _ { j } | ( i \neq j ) , \Delta _ { m a x } = \operatorname* { m a x } _ { i , j } | \theta _ { i } - \theta _ { j } | . } \end{array}$

in = Δ = maxThe detailed proof of this theorem is omitted here due to page limitation. As $N \geq K$ and $K \geq 1$ , we conclude 1that N − K −  ≥ . Thus, the right part of regret 3expression $\begin{array} { r } { N - \frac { K + 1 } { 2 } - \frac { \overline { { \alpha ( K + 1 ) ( 3 \dot { N } - 2 K - 1 ) } } ^ { 2 } } { 6 } < \dot { N } } \end{array}$ . As a result, 2 6our policy achieves with a regret upper bounded in the order of O N K  L , which is in polynomial order to number of ( log )channels and strictly in logarithmic order to time.

# IV. SIMULATIONS AND PERFORMANCE ANALYSIS

In this section, we evaluate and analyze the performance of the proposed online sequential channel sensing and accessing algorithms via simulations.

![](images/bbf64ce7aa84c4d858e4a6611b9d8b024c0b1e4b31208505254114b4e684e677.jpg)



Fig. 3. Learning progress analysis

Eight policies are running under the same environment for performance comparison, where UCB1, UCB1-VS, and SCB are our proposed sequential online learning policies, Single Index is an order-optimal one channel per slot online learning policy which is first presented by Lai et al in [6]. Randomized Single Channel chooses one random channel for sensing/accessing at each slot, and Optimal Single Channel is a genie-based policy that user always senses/accesses the channel with highest idle probability in each slot. Correspondingly, user would sequentially sense/access with a randomly chosen sensing order at each slot under Randomized Sequence, and would always use the optimal sensing order for sequential sensing/accessing under Optimal Sequence.

We derive the normalized throughput as a function of slot index in Fig.3. The results we are averaged from 1500 rounds of independent experiments, where each lasts 6000 time slots. Our experiment setting is as follows. The idle probabilities of independent channels are randomly generated in range ,  for each round. Then, the states of channels (i.e. idle [0 1]or busy) in each slot are generated independently according to the idle probability vector of current experiment round. Here, $N = 3$ and the normalized sensing cost $\alpha = 0 . 2$ . It = 3 = 0 2clearly shows that: 1) all the policies that exploit diversity $( \mathrm { i . e . , }$ , sequential sensing/accessing) outperform the policy in the scheme of “one channel per slot”, e.g., even Randomized Sequence outperforms Optimal Single Channel that always using the optimal channel; 2) all the learning policies converge to the optimal solution under either sequential sensing scheme or one channel per slot scheme; and 3) our proposed SCB policy outperforms all other three online policies in both expected throughput and learning speed.

In Fig.4, we further compare the performance of the learning policies with different N . Comparing the results in the case that $N = 3 \ ( \mathrm { i . e . }$ ., the left part) with that in the case $N = 5$ = 3 = 5(i.e., the right part), we obtain following observations. Firstly, as the number of channels increases, user could obtain more throughput gain through learning. This is because the potential opportunity increases with the number of channels. Moreover, the curves clearly show that, the learning speed of orderspecific algorithms (UCB1 and UCB1-VS) would sharply decreased as N increases, meanwhile, the UCB1-VS greatly accelerate the learning progress over traditional UCB1. These conform to the analysis we stated in Section.III.

![](images/a34ce46442e3201ae8f9750d762887a22dd8be31e937ca06a259fcb8c727e996.jpg)  
Fig. 4. Throughput reward with different N

Finally, in Fig. 5, we study the impact of channel idle probability on the efficiency of learning policies. In this part, $N \ = \ 5$ and $\alpha ~ = ~ 0 . 1$ . Two parameters, i.e., θ and $\delta ,$ are = 5 = 0 1used to control the generation of channel idle probability, where channel idle probabilities are randomly generated in the range $\bigl \lceil \bar { \theta } - \delta , \bar { \theta } + \bar { \delta } , \bigr \rceil$ at the beginning of each round. We +compare our proposed SCB policy with existing MAB-based online policy Single Index [6] in both normalized throughput and learning speed. It clearly shows in upper part of Fig. 5 that SCB outperforms Single Index in all cases by exploiting instantaneous diversity among channels. Meanwhile, the throughput gain decreases as $\bar { \theta }$ and δ increases. This indicates that our scheme would benefit more in the spectrum scarcity scenario, e.g., it shows nearly two times throughput over Single Index) when $\bar { \theta } = 0 . 3$ . The averaged throughput = 0 3gain over all the considered scenarios is more than . 30%Further, we study the learning speed of these two policies in the lower part of this figure. We denote the number of slots user experienced before achieving “σ-learning-progress” $( 0 < \sigma < 1 )$ as $t _ { \sigma } ,$ and use it to quantify the learning speed of 0 1the online learning policies. Specifically, $t _ { \sigma } ^ { s c b }$ and t sin.indexσ are defined as $\begin{array} { r } { t _ { \sigma } ^ { s c b } \doteq \operatorname* { m i n } _ { j } \left\{ \frac { \dot { E _ { { \left[ r _ { s c b } \left( j \right) - r _ { s e q . r a n d . } \left( j \right) \right] } } } } { E \left[ r _ { s e q . o p t . } \left( j \right) - r _ { s e q . r a n d . } \left( j \right) \right] } = \sigma \right\} } \end{array}$ and $\begin{array} { r } { t _ { \sigma } ^ { s i n . i n d e x } \doteq \operatorname* { m i n } _ { j } \left\{ \frac { E [ r _ { s i n . i n d e x } ( j ) - r _ { s i n . r a n d . } ( j ) ] } { E [ r _ { s i n . o p t . } ( j ) - r _ { s i n . r a n d . } ( j ) ] } = \sigma \right\} } \end{array}$ respec-[ ( )tively. We choose a typical value of σ, i.e. $\sigma = 0 . 9$ , to evaluate = 0 9the learning speed. It is clearly shown that SCB scheme greatly reduced the time cost for achieving  learning progress, e.g., less than half even when $\bar { \theta } \ : = \ : 0 . 7$ %, which means that = 0 7SCB accelerates the learning process by more than . 100%The results also show that the learning speeds of the two policies are strictly increasing with $\delta ,$ where δ characterizes the deviation of channel statistics. Meanwhile, the learning speed of SCB is increasing with $\theta ,$ perhaps due to the fact that less channels would be observed in a slot when θ increases.

# V. CONCLUSION

In this work, we investigated online learning of optimal sequential channel sensing and accessing. We first introduced the classic UCB1 algorithm in solving our problem. We concluded that using this classic algorithm, both the storage and regret are exponentially increasing with the number of channels. Then, an improved algorithm, i.e. UCB1-VS, was presented, which accelerated learning process by exploring dependency between orders. Finally, we proposed the SCB algorithm with storage overhead linear to the number of channels, and the regret in O N K  L .

![](images/4097196dac490446f8b97e46748d1b71742ae800b39560aa5c284fa0ce810827.jpg)



Fig. 5. Impact of idle probability

# ACKNOWLEDGMENT

The research of authors is partially supported by NSF CNS-0832120, NSF CNS-1035894, NSF of China under Grant No. 60932002, 61003277, 61170216, 61172062, 973 Program of China under grant No. 2009CB320400, 2010CB328100, 2010CB334707, 2011CB302705, Tsinghua National Laboratory for Information Science and Technology (TNList), program for Zhejiang Provincial Key Innovative Research Team, and program for Zhejiang Provincial Overseas High-Level Talents (One-hundred Talents Program). Jiangsu NSF (Grant No. BK2010102).

# REFERENCES

[1] C. Wang, X.-Y. Li, S. Tang, and C. Jiang, “Multicast capacity scaling laws for multihop cognitive networks,” in IEEE Transactions on Mobile Computing, Sep. 2011, pp. 262–271.   
[2] P. Xu, X.-Y. Li, S. Tang, and J. Zhao, “Efficient and strategyproof spectrum allocations in multichannel wireless networks,” IEEE Trans. Computers, vol. 60, no. 4, pp. 580–593, 2011.   
[3] A. Mahajan and D. Teneketzis, “Multi-armed bandit problems,” 2009.   
[4] M. Mishra and A. Sahai, “How much white space is there?” EECS Department, University of California, Berkeley, Tech. Rep. UCB/EECS-2009-3, Jan. 2009.   
[5] “IEEE 802.22-2011(TM) standard for cognitive wireless regional area networks (RAN) for operation in TV bands.” [Online]. Available: http://www.ieee802.org/22/   
[6] L. Lai, H. E. Gamal, H. Jiang, and H. V. Poor, “Cognitive medium access: Exploration, exploitation and competition,” CoRR, vol. abs/0710.1385, 2007.   
[7] K. Liu and Q. Zhao, “Distributed learning in multi-armed bandit with multiple players,” IEEE Transactions on Signal Processing, pp. 5667– 5681, 2010.   
[8] C. Tekin and M. Liu, “Online learning in opportunistic spectrum access: A restless bandit approach,” in INFOCOM, 2011.   
[9] T. L. Lai and H. Robbins, “Asymptotically efficient adaptive allocation rules,” Advances in Applied Mathematics, vol. 6, no. 1, pp. 4–22, 1985.   
[10] P. Auer, N. Cesa-Bianchi, and P. Fischer, “Finite-time analysis of the multiarmed bandit problem,” Mach. Learn., vol. 47, pp. 235–256, May 2002.   
[11] Y. Liu, Y. He, M. Li, J. Wang, K. Liu, L. Mo, W. Dong, Z. Yang, M. Xi, J. Zhao, and X.-Y. Li, “Does wireless sensor network scale? a measurement study on greenorbs,” in INFOCOM, 2011, pp. 873–881.