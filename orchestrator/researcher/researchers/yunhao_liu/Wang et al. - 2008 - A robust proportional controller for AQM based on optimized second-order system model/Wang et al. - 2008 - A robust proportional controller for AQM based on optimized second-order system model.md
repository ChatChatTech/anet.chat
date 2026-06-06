# A robust proportional controller for AQM based on optimized second-order system model q

Jianxin Wang a,\*, Liang Rong a , Yunhao Liu b

a School of Information Science and Engineering, Central South University, Changsha 410083, LuShanNanLu No. 154, Changsha, HuNan 410083, China

b Department of Computer Science, HongKong University of Science and Technology, HongKong, China

# a r t i c l e i n f o

Article history:

Received 7 June 2007

Received in revised form 9 March 2008

Accepted 9 March 2008

Available online 22 March 2008

Keywords:

Active Queue Management

Optimized second-order system model

Packet loss ratio

# a b s t r a c t

Active Queue Management (AQM) is an effective mechanism to improve the performance of end-to-end congestion control. However, existing AQM schemes are sensitive to network traffic changes. In this paper, we propose a novel AQM algorithm based, for the first time, on the optimized second-order system model, called Adaptive Optimized Proportional Controller (AOPC). AOPC measures the latest packet loss ratio, and uses it as a complement to queue length in order to dynamically adjust packet drop probability. Through using TCP throughput model, AOPC is capable of detaching from the number of TCP sessions N and insensitive to various network conditions. The parameter tuning rule is in compliance with the optimized second-order system model which has a small overshoot and fast convergence speed. We comprehensively evaluate the performances of AOPC through extensive simulations using NS2 simulator, and contrast it with previous approaches such as REM, PI, PID, PIP, and LRED. Simulation results demonstrate that AOPC is more responsive to time-varying network conditions than other algorithms, and obtains the best tradeoff between utilization and delay.

\- 2008 Elsevier B.V. All rights reserved.

# 1. Introduction

Designing a scalable Active Queue Management (AQM) scheme to co-operate with TCP end-to-end congestion control has received much interest recently [1]. The TCP end-to-end congestion control scheme is effective in preventing congestion collapse, especially when most of the flows are responsive to packet loss in congested routers. Unresponsive flows, however, do not slow down their sending rates when the network becomes congested, and they indeed obtain more bandwidth, results in a longer time for the network to recover from congestion. Traditional end-to-end congestion control and drop-tail buffer management are insufficient to assure even minimal fairness, delay or loss guarantees, let alone providing quality of service support.

To mitigate such problems, AQM has been proposed at intermediate nodes to improve the end-to-end congestion control [1]. Generally, an Internet congestion control mechanism is comprised of two components. First, a flow control algorithm which runs in end hosts. During the congestion avoidance phase, TCP sources increase the congestion window size by one segment per round-trip time in the absence of congestion, and halve the congestion window size in response to a round-trip time with a congestion event,

which is known as Additive Increase and Multiplicative Decrease (AIMD). Second, the link management algorithm executed in intermediate routers. Internet routers trigger the packet dropping (or marking, if Explicit Congestion Notification (ECN) [2] is enabled) in advance when the onset of congestion is perceived, which is the basic idea of AQM. The design objectives of AQM are as follows. (1) reducing packet loss ratio at routers; (2) providing high throughput and low end-to-end delay and jitter; (3) being stable and responsive under dynamic network scenario; (4) being simple, efficient and scalable to deploy.

In existing AQM schemes, link congestion is estimated through queue length [3], traffic input rate [8,9], packet loss ratio [11,18], buffer overflow and emptiness [7], or a combination of these congestion indicators [10,12]. Queue length (or average queue length) is widely used in RED [3] and most of its variants [4–6], where packet drop probability is often linearly proportional to the queue length. Many studies have demonstrated that the performance of RED is inherent deficient in parameter settings. Floyd, the designer of RED, and other researchers have made great efforts to provide guidelines in parameter settings, such as gentle-RED [4], ARED [5], SRED [6] etc. Although these schemes work more effectively than RED under a wide range of traffic scenario, the major drawback is that their queue lengths oscillate largely under special network load and traffic conditions, resulting in low throughput and high queueing delay. BLUE [7] adjusts the marking (or dropping) probability based upon the buffer overflow and link idle events. The traffic input rate is also used in some AQM schemes such as

AVQ [8] to make the input rate match the link output rate. Many other schemes, such as REM [10] and RaQ [12], use both queue length and input rate to estimate congestion level. In [14], the fluid model of TCP behavior derived in [13] has been linearized by Hollot et al. and a second-order feedback control system was obtained thereafter. Subsequently, a Proportional-Integral (PI) controller [15] is designed to regulate the TCP/AQM interconnection system. The TCP/AQM interconnection system gives a framework for network researchers to design an AQM controller to regulate the system. Based on the system framework, Proportional-Integral-Derivative (PID) controller [16], PIP [17], and LRED [18], are proposed to eliminate the drawbacks in PI controller. These sophisticated controllers indeed enhance the performance in wide network scenarios; however, the connatural demerit of these controllers is that the control parameters are configured in particular network scenarios so that they lack of flexibility. The strong correlation between the control parameters and network parameters makes these controllers be prone to be unstable. The stability and convergence are two important issues which should be considered in the system design. Existing AQM controllers are sensitive to network load and obtain unsatisfactory stability and convergence under dynamic network environment, which motivate us to develop a robust controller with both stable control of queue evolution and fast convergence rate to the desire queue length under a variety of network scenarios.

The design is motivated by the following observation. The TCP throughput formula, which is derived from [19], can be useful in decoupling AQM design from the number of TCP sessions N. Based on the optimized second-order system model which has a small overshoot and fast convergence rate, together with the TCP throughput formula, we propose a robust AQM scheme, called Adaptive Optimized Proportional Controller (AOPC). AOPC periodically measures the packet loss ratio and uses it to compute a tuning factor of the control parameter. With this tuning factor, the AOPC tunes the control parameter adaptively, tracking the dynamic network load. Besides, AOPC applies the optimized second-order system model to ensure the satisfactory performance and guarantee the system stability. It has a better system closedloop performance over the approaches tuned by the classical Ziegler–Nichols rule. Through extensive simulations under various network configurations, we show that, compared to existing AQM schemes, such as REM, PI, PID, PIP, and LRED, AOPC scheme offers more stable control of queue length around the desired queue length, thus achieves higher link utilization. AOPC also has better responsiveness and robustness.

The remainder of this paper is organized as follows. In Section 2, we review the control system models. Section 3 presents the AOPC scheme and gives some guidelines for parameter settings. A performance analysis is also presented at the end of this section. We compare AOPC with REM, PI, PID, PIP and LRED through NS simulation in Section 4. We conclude this work in Section 5.

# 2. Control system model

In this section, we introduce the TCP/AQM interconnection system model, the optimized second-order system model, and the general properties of proportional AQM control.

# 2.1. TCP/AQM Interconnection system model

Transient behavior of networks with AQM routers supporting TCP flows was described by a couple of nonlinear ordinary differential equations [13]. These equations are linearized in [14] and the linear TCP/AQM interconnection system is depicted in Fig. 1, where $q _ { 0 }$ is the desired queue length, $G _ { 1 } ( s )$ is the AQM controller, $G _ { 2 } ( s )$ is the ‘‘plant” or TCP window-control and queue dynamics we try to control.

![](images/57df60cf63079d73a2b0bc441e8107989df15640c56aeae2594ceee303c8e1fc.jpg)



Fig. 1. Block diagram of TCP/AQM interconnection system.

The objective of the AQM controller is to regulate the queue length to the desired value $q _ { 0 }$ by marking (dropping) packets with a probability p as a function of measured queue length deviation between instantaneous and desired value. The transfer function of $G _ { 2 } ( s )$ is:

$$
G _ {2} (s) = \frac {K _ {m}}{(T _ {1} s + 1) (T _ {2} s + 1)}, \tag {1}
$$

where,

$$
K _ {m} = \frac {(R C) ^ {3}}{4 N ^ {2}}, \quad T _ {1} = \frac {R ^ {2} C}{2 N}, \quad T _ {2} = R. \tag {2}
$$

where, N is the number of active TCP sessions, R is the round trip time (RTT), and C is the link capacity.

By choosing different forms of $G _ { 1 } ( s )$ and employing different methods to determine the parameters of $G _ { 1 } ( s ) { \mathrm { . } }$ , we have different AQM algorithms (Controllers). The widely adopted controller is the general PID (Proportional-Integral-Differential) controller. Due to the modeling inaccuracies, as listed in [17], a parameter tuning structure is (1) to correct this simple plant or controlled object; and (2) insensitive to the drift of system parameters. In previous works, the control parameters of $G _ { 1 } ( s )$ are determined only based on some special network and traffic conditions. This paper proposes a self-tuning proportional controller that can determine the controller parameters dynamically.

# 2.2. Optimized second-order system model

Consider the closed-loop transfer function of the second-order system:

$$
G (s) = \frac {K}{\tau^ {2} s ^ {2} + 2 \zeta \tau s + 1}, \tag {3}
$$

where K is the static sensitivity, s is the time constant, and $\zeta$ is the damping factor. The magnitude–frequency characteristic $A ( \omega )$ and the phase–frequency characteristic uðxÞ are given by:

$$
A (\omega) = \frac {K}{\sqrt {(1 - \omega^ {2} \tau^ {2}) ^ {2}} + 4 \zeta^ {2} \omega^ {2} \tau^ {2}},
$$

$$
\varphi (\omega) = - \arctan \frac {2 \zeta \omega \tau}{1 - \omega^ {2} \tau^ {2}}.
$$

The damping factor f is vital to the performance of the second-order system [23]. When f is very small (close to zero) at $\omega \tau = 1$ , the value of $A ( \omega )$ is very large, which is called resonance. With the increasing of $\zeta ,$ the resonance peak descends. When $\zeta \geqslant 0 . 7 0 7$ , the resonance peak vanishes and $A ( \omega )$ is a decreasing function of x. In engineering, the second-order system is classified into under damping, critical damping, and over damping system corresponding ${ \bf t 0 } ~ \zeta < 1 , \zeta = 1$ , and $\zeta > 1$ . The second-order system is optimal when $\zeta = 0 . 7 0 7$ . For $0 < \zeta <$ 1, the closed-loop poles are a pair of complex conjugates $- \frac { \zeta } { \tau } \pm j \frac { \sqrt { 1 - \zeta ^ { 2 } } } { \tau }$ in the left-half s-plane, and the step response of the second-order system described by (3) is

$$
y (t) = K \left[ 1 - \frac {1}{\sqrt {1 - \zeta^ {2}}} e ^ {- \frac {\zeta t}{\tau}} \cdot \sin \left(\frac {\sqrt {1 - \zeta^ {2}}}{\tau} t + \arctan \frac {\sqrt {1 - \zeta^ {2}}}{\zeta}\right) \right]. \tag {4}
$$

When $t \to \infty , y ( t ) \to 1$ , the steady-state error $e _ { s s }$ goes to zero. Assume $K \leqslant 1$ is always satisfied in the proportional AQM control (In Section 2.3, we show this assumption is consistently valid). Let $y ( \infty ) = 1$ , then the steady-state error $e _ { s s }$ and the settling time $t _ { s }$ with admissible error set to be $2 \% ,$ , satisfied with $| y ( t _ { s } ) - y ( \infty ) | = 0 . 0 2 y ( \infty )$ , are obtained as follows:

$$
e _ {s s} = 1 - K, \tag {5}
$$

$$
t _ {s} = \frac {4 - \ln \sqrt {1 - \zeta^ {2}}}{\zeta} \tau . \tag {6}
$$

# 2.3. General properties of proportional AQM control

Let h denote the control parameter for a proportional AQM controller. The closed-loop transfer function of the TCP/AQM control system can be given by:

$$
G (s) = \frac {\theta K _ {m}}{T _ {1} T _ {2} s ^ {2} + (T _ {1} + T _ {2}) s + \theta K _ {m} + 1}
$$

$$
= \frac {K (\theta)}{\tau (\theta) ^ {2} s ^ {2} + 2 \zeta (\theta) \tau (\theta) s + 1}, \tag {7}
$$

where the static sensitivity $K ,$ time constant s, and damping factor f are calculated as functions of h as follows:

$$
K (\theta) = \frac {\theta K _ {m}}{\theta K _ {m} + 1}, \tag {8}
$$

$$
\tau (\theta) = \sqrt {\frac {T _ {1} T _ {2}}{\theta K _ {m} + 1}}, \tag {9}
$$

$$
\zeta (\theta) = \frac {T _ {1} + T _ {2}}{2} \sqrt {\frac {1}{(\theta K _ {m} + 1) T _ {1} T _ {2}}}. \tag {10}
$$

Assume the TCP/AQM interconnection system is an under damping system. We attempt to examine the monotonicity of steady-state error $e _ { s s }$ and settling time $t _ { s }$ as the control parameter h increases.

Lemma 1. The steady-state error $e _ { s s }$ of the TCP/AQM interconnection system is a decreasing function of h when using a proportional AQM controller.

Proof 1. The steady-state error calculated from (5) is a decreasing function of h if and only if the parameter K is a increasing function of h. From (8), since $K _ { m }$ is a positive parameter, obviously $K ( \theta ) < 1$ is always satisfied for all $\theta > 0$ and increases with h. Therefore, ess decreases as h increases. h

Lemma 2. The settling time $t _ { s }$ of the TCP/AQM interconnection system is a decreasing function of h when using a proportional AQM controller.

Proof 2. From (8)–(10), we have

$$
\theta K _ {m} + 1 = \frac {1}{1 - K}, \quad \frac {\tau \zeta}{T _ {1} + T _ {2}} = \frac {1}{2 (\theta K _ {m} + 1)} = \frac {1 - K}{2}.
$$

We write the derivative of function $t _ { s }$ about h as follows:

$$
\frac {\mathrm{d} t _ {s}}{\mathrm{d} \theta} = \frac {\partial t _ {s}}{\partial \tau} \frac {\mathrm{d} \tau}{\mathrm{d} \theta} + \frac {\partial t _ {s}}{\partial \zeta} \frac {\mathrm{d} \zeta}{\mathrm{d} \theta},
$$

where

$$
\frac {\partial t _ {s}}{\partial \tau} = \frac {4 - \ln \sqrt {1 - \zeta^ {2}}}{\zeta},
$$

$$
\frac {\mathrm{d} \tau}{\mathrm{d} \theta} = - \frac {T _ {1} T _ {2} K _ {m}}{2 (\theta K _ {m} + 1) \sqrt {T _ {1} T _ {2} (\theta K _ {m} + 1)}}
$$

$$
= - \frac {K _ {m} \tau^ {2} \zeta}{T _ {1} + T _ {2}} = - \frac {K _ {m} (1 - K)}{2} \tau ,
$$

$$
\frac {\partial t _ {s}}{\partial \zeta} = \left(\frac {\zeta^ {2} + (1 - \zeta^ {2}) \ln \sqrt {1 - \zeta^ {2}}}{(1 - \zeta^ {2}) \zeta^ {2}} - \frac {4}{\zeta^ {2}}\right) \tau ,
$$

$$
\frac {\mathrm{d} \zeta}{\mathrm{d} \theta} = - \frac {(T _ {1} + T _ {2}) K _ {m}}{4 (\theta K _ {m} + 1) \sqrt {T _ {1} T _ {2} (\theta K _ {m} + 1)}} = - \frac {K _ {m} \zeta (1 - K)}{2}.
$$

hence,

$$
\frac {\mathrm{d} t _ {s}}{\mathrm{d} \theta} = - \frac {K _ {m} [ \zeta^ {2} + 2 (1 - \zeta^ {2}) \ln \sqrt {1 - \zeta^ {2}} ] (1 - K)}{2 \zeta (1 - \zeta^ {2})} \tau
$$

From (8), we can see for all $\theta \in \mathbb { R } ^ { + } , K < 1$ is always satisfied. Since the system is an under damping system, that is $0 < \zeta < 1$ . If $\zeta ^ { 2 } + 2 ( 1 - \zeta ^ { 2 } ) \ln \sqrt { 1 - \zeta ^ { 2 } } > 0$ is valid, $\begin{array} { r } { \frac { \mathrm { d } t _ { s } } { \mathrm { d } \theta } < 0 } \end{array}$ will be satisfied. The proof for $\forall \zeta \in ( 0 , 1 ) , \zeta ^ { 2 } + 2 ( 1 - \zeta ^ { 2 } )$ ln $\sqrt { 1 - \zeta ^ { 2 } } > 0$ will be similar. Thus, $\begin{array} { r } { \frac { \mathrm { d } t _ { s } } { \mathrm { d } \theta } < 0 , } \end{array}$ and the function $t _ { s }$ is a decreasing function of h. h

# 3. The AOPC scheme

# 3.1. Overview of LRED scheme

The packet loss ratio and queue length are both used to estimate the degree of link congestion in LRED [18]. LRED periodically measures the packet loss ratio, which is then set as the desired stable packet drop probability $p _ { 0 } ,$ in the large time-scale, and updates packet drop probability in the small time-scale at each packet arrival. Thus, the packet drop probability is calculated as follows:

$$
p = \overline {{l (k)}} + \beta \sqrt {\overline {{l (k)}}} (q - q _ {0}), \tag {11}
$$

where b is a pre-configured positive constant, lðkÞ is the measured packet loss ratio at period k, $q _ { 0 }$ is the desired queue length. Let lðkÞ be the packet loss ratio in period k during the latest M measurement periods, then the measured packet loss ratio lðkÞ can be calculated as follows:

$$
\overline {{l (k)}} = m w * \overline {{l (k - 1)}} + (1 - m w) * l (k), \tag {12}
$$

where mw is the measured weight factor.

LRED is a typical proportional controller. The rationale of parameter setting behind LRED is to let the control parameter increases with the measured loss ratio. Thus, when $\overline { { l ( k ) } }$ is a bit large (or small), p will increase (or decrease) with a large (or small) slope so as to guarantee that the packet drop probability in small queue length is much smaller. For comparison of AOPC scheme, a stability condition for LRED is presented as follows.

Stability condition for LRED: Given network parameters $( \widehat { N } , \widehat { C } , \widehat { R } )$ , and assume that $\dot { \boldsymbol { \beta } }$ satisfies $\begin{array} { r } { \widehat { R } \omega + \arctan ( \frac { \omega } { K _ { 1 1 } } ) = \frac { \pi } { 2 } , \dot { \beta } > 0 } \end{array}$ , where x can be calculated as $\begin{array} { r } { \omega = \sqrt { \frac { 1 } { 2 } ( \sqrt { K _ { 1 1 } ^ { 4 } + 4 K _ { c } ^ { 2 } H _ { c } ^ { 2 } } - K _ { 1 1 } ^ { 2 } ) } } \end{array}$ , and $\begin{array} { r } { K _ { 1 1 } = \frac { 2 \widehat { N } } { \widehat { R } ^ { 2 } \widehat { C } } , } \end{array}$ $\begin{array} { r } { K _ { c } = \frac { \widehat { C } ^ { 2 } } { \eta N } , H _ { c } = \widehat { \beta } \sqrt { p _ { 0 } } } \end{array}$ in LRED. If

$$
\beta <   \hat {\beta} = \min \left(\dot {\beta}, \frac {\sqrt {2 \eta} (2 \hat {N}) ^ {4}}{\hat {R} ^ {3} \hat {C} ^ {3}}\right), \tag {13}
$$

then the TCP/LRED system remains stable for every value of $N \geqslant \widehat { N }$ and $R \leqslant { \widehat { R } }$ .

From the stability condition for LRED, we can see that the TCP/ LRED interconnection system has a strong relation with network variables (N, R) and the parameter tuning rule for LRED is not flexible enough since b is an implicit function of the network variables (N, R). However, the number of TCP sessions N and round trip time

R vary dynamically and remain unknowns. Moreover, even N and R are known a priori, the value of b is unable to be obtained through online computation for Internet routers since $\beta$ is not an explicit function of the network variables (N, R). Therefore, LRED is not scalable for a wide range of traffic conditions and impossible to be deployed in Internet routers. In order to circumvent the obstacle of parameter configuration and simplify the parameter tuning method, an estimation mechanism for network variables should be provided to capture the network dynamics.

# 3.2. AOPC description

The main goal of our work is to develop a simple AQM controller that can scale to Internet-like environments with significant heterogeneity in link capacities, end-to-end RTTs, route buffer sizes and variable traffic characteristics. By ‘‘simple” we mean an AQM controller does not require per-flow state information and low computation overhead in deployment. AQM schemes need to maintain closed-loop performance in face of varying network conditions. These conditions include variations in the number of TCP sessions N and TCP average round trip time R, and the introduction of shortlived flows into the queue. Due to the fact that (1) the lifetime of a TCP session remains unknown to a network router, (2) nonidentical TCP sessions have various lifetimes, and (3) the number of TCP sessions varies greatly, it is difficult to count the number of TCP sessions directly. Nevertheless, in the TCP/AQM interconnection system model, the system closed-loop performance has a strong relationship to these unknown network state variables.

The motivation behind AOPC is to detach the correlation between control parameters and the network state variables so as to provide an efficient and flexible mechanism for queue management. We employ proportional AQM control to calculate packet drop probability. AOPC measures packet loss ratio in a large time scale and updates packet drop probability in a small time scale upon each packet arrival. Different from LRED, AOPC tunes its control parameter adaptively according to the packet loss ratio measured in a large time scale to circumvent the drawbacks of LRED. The packet drop probability in AOPC is given by:

$$
p = \overline {{l (k)}} + \gamma (k) (q - q _ {0}), \tag {14}
$$

where, cðÞ is a variable parameter suitable to current network conditions, lðkÞ is the measured packet loss ratio, and the measurement method is the same as LRED as described in (12).

The TCP/AOPC interconnection control system is depicted in Fig. 2. AOPC has two components: (1) Network Load Estimator, which estimates the average number of TCP sessions at the end of the latest packet loss ratio measurement period so as to detach the correlation between the control parameter and the number of TCP sessions N; (2) Parameter Optimization Module, which optimizes the TCP/AOPC interconnection system based on the optimized second-order system model.

In order to acquire current network load information, AOPC estimates the number of TCP sessions N after packet loss ratio mea-

![](images/3f4690f818a4797d6f8e5ef7b0d8bbdc3992428a5d32ce822a039a1784fc9718.jpg)



Fig. 2. Block diagram of TCP/AOPC interconnection system.

sured at the end of each measurement period. The TCP flow number estimation is based on the TCP throughput formula [19], which takes the stable packet drop probability $p _ { 0 }$ as an input variable. The key assumption in the estimation is that the measured packet loss ratio $\overline { { l ( k ) } }$ can be used to approximate the stable packet drop probability $p _ { 0 } ,$ , that $\mathrm { i } s , \overline { { l ( k ) } } \approx p _ { 0 } .$ . Thus, the number of TCP sessions can be estimated when having the most recent measured packet loss ratio.

Apart from tuning controller parameters on-line to make system adaptable to network load changes by tracking current network load information, AOPC applies the the optimized second-order system model to ensure the efficiency and stability. This controller parameter tuning approach is known to work well for most single-input–single-output (SISO) linear system and results in better system closed-loop performance over those tuned by the classical Ziegler–Nichols rule.

# 3.2.1. Network load estimator

A single TCP flow, which experiences packet drop probability $p _ { 0 } ,$ attains the throughput roughly as follows [19]:

$$
x = \frac {1}{R} \sqrt {\frac {2}{3 p _ {0}}}, \tag {15}
$$

where R is the round trip time of the TCP flow.

Now consider a link shared by N flows. Let $y = \sum x _ { i } ( i = 1 , \dots , N )$ be the total sending rate. Suppose the link has the service rate (link capacity) C and the buffer is large enough to keep the link being fully utilized. Clearly the total sending rate is larger than the service rate, $i . \ e . \ y > C ,$ , so the drop probability $p _ { 0 }$ satisfies

$$
(1 - p _ {0}) y = C. \tag {16}
$$

Then, from (15) and (16), the drop probability $p _ { 0 }$ is the solution to

$$
\sum_ {i = 1} ^ {N} \frac {1}{R _ {i}} \sqrt {\frac {2}{3 p}} (1 - p) = C. \tag {17}
$$

Denoting

$$
\frac {1}{R _ {\mathrm{eq}}} = \frac {1}{N} \sum_ {i = 1} ^ {N} \frac {1}{R _ {i}}, \tag {18}
$$

where $R _ { \mathrm { e q } }$ is the harmonic mean of the individual round trip times of the flows. In [15], the $R _ { \mathrm { e q } }$ is interpreted as the equivalent round trip time of the flows, which can be viewed as equivalent to R in TCP/AQM model shown in Fig. 2. Then the system behaves in the mean as a system with N flows each having an identical equivalent round trip time $R _ { \mathrm { e q } } .$ .

From (17) and (18), we obtain

$$
N = R _ {\mathrm{eq}} C f (p _ {0}), \tag {19}
$$

where,

$$
f (p _ {0}) = \frac {\sqrt {3 p _ {0} / 2}}{1 - p _ {0}}, \tag {20}
$$

In $( 2 0 ) , f ( p _ { 0 } )$ is a tuning factor for calculating packet drop probability. According to previous assumption that the measured packet loss ratio lðkÞ can be used to approximate the stable packet drop probability $p _ { 0 } ,$ we rewrite (21) as follows:

$$
f (p _ {0}) = f \left(\overline {{l (k)}}\right) = \frac {\sqrt {3 \overline {{l (k)}} / 2}}{1 - \overline {{l (k)}}}. \tag {21}
$$

Eq. (19) illustrates that the number of TCP sessions N largely depends on the harmonic mean $R _ { \mathrm { e q } }$ of the RTTs yet not to individual RTTs. If the harmonic mean value $R _ { \mathrm { e q } }$ is a known variable and varies slightly around a stable value, we can estimate the number of TCP sessions N by ignoring the time variant property of $R _ { \mathrm { e q } } .$ Recent Internet measurements [20] report that roughly 75–90% of flows have RTTs less than 200 ms and the average RTT is distributed around 180 ms [21], suggesting an alternate way to improving TCP performance and AQM design.

# 3.2.2. Parameter optimization module

By approximating the stable packet drop probability $p _ { 0 }$ as the latest measured packet loss ratio lðkÞ, we obtain the following formulas from (2),(19),(21):

$$
K _ {m} = \frac {R _ {\mathrm{eq}} C}{4 f ^ {2} (\overline {{l (k)}})}, \quad T _ {1} = \frac {R _ {\mathrm{eq}}}{2 f (\overline {{l (k)}})}, \quad T _ {2} = R _ {\mathrm{eq}}. \tag {22}
$$

Thus, the TCP and queue dynamics transfer function $G _ { 2 } ( s )$ is greatly simplified. The rule for designing a stabilizing proportional controller to stabilize the TCP/AOPC interconnection system can be given in Theorem 1.

Theorem 1. Denoting $\gamma ( \cdot )$ to be the control parameter of AOPC. If

$$
\gamma (k) = \frac {f (\overline {{{l (k)}}}) [ 1 + 4 f ^ {2} (\overline {{{l (k)}}}) ]}{R _ {\mathrm{eq}} C}, \tag {23}
$$

then the linear feedback control system in Fig. 2 using $G _ { 1 } ( s ) = \gamma ( \cdot )$ is asymptotically stable and the system is an optimized system.

Proof 3. From (22), we can obtain

$$
\gamma = \frac {f (\overline {{{l (k)}}}) [ 1 + 4 f ^ {2} (\overline {{{l (k)}}}) ]}{R _ {\mathrm{eq}} C} = \frac {T _ {1} ^ {2} + T _ {2} ^ {2}}{2 K _ {m} T _ {1} T _ {2}}. \tag {24}
$$

Replacing h in (10) with c in (24), we obtain

$$
\zeta = \frac {T _ {1} + T _ {2}}{2} \sqrt {\frac {1}{(\gamma K _ {m} + 1) T _ {1} T _ {2}}} = 0. 7 0 7.
$$

According to the optimized second-order system model discussed in section II, when f ¼ 0:707, the system is an optimized second-order system, and it is asymptotically stable. So, TCP/AOPC interconnection system is asymptotically stable and the system is an optimized system. h

Compared to the stability condition for LRED, AOPC scheme maintains the closed-loop performance in face of varying network conditions. Meanwhile, AOPC simplifies the tuning method and makes it adaptable to dynamic networks. For AOPC implementation, we can track packet departure to obtain the link service rate C. From (20), we see that the harmonic mean of individual RTTs, $R _ { \mathrm { e q } } ,$ contributes a very small weight to the control parameter c. For example, assume the current measured packet loss ratio lðkÞ ¼ 0:01, the link capacity is 2500packets/s, when $R _ { \mathrm { e q } } = 0 . 2 s ,$ , the required AOPC parameter $\gamma$ is $2 . 6 2 5 \times 1 0 ^ { - 4 } ;$ while, when $R _ { \mathrm { e q } } = 0 . 1 5 s$ , the required AOPC parameter c is $3 . 5 \times 1 0 ^ { - 4 }$ . The example shows that even though $R _ { \mathrm { e q } }$ varies slightly in a range between 150 ms and 200 ms, the control parameter c is not obviously affected and can be treated as insensitive to RTT variation in real network condition.

# 3.3. Analysis of performance index

In this section, we discuss why AOPC obtains smaller steadystate error and faster convergence rate than LRED. Both AOPC and LRED are proportional controllers. We let $\theta _ { \mathsf { a } }$ and $\theta _ { \mathrm { l } }$ denote the control parameter for AOPC and LRED, respectively. Then,

$$
\theta_ {\mathrm{a}} = \gamma = \frac {f (\overline {{l (k)}}) [ 1 + 4 f ^ {2} (\overline {{l (k)}}) ]}{R _ {\mathrm{eq}} C}, \quad \text { and } \theta_ {1} = \beta \sqrt {\overline {{l (k)}}}.
$$

Ordinarily, the packet loss ratio is very small (close to zero), i. e. $\overline { { l ( k ) } } \ll 1$ .

Thus

$$
f (\overline {{l (k)}}) = \frac {\sqrt {3 \overline {{l (k)}} / 2}}{1 - \overline {{l (k)}}} \approx \sqrt {3 \overline {{l (k)}} / 2}.
$$

Then we obtain

$$
\frac {\theta_ {\mathrm{a}}}{\theta_ {1}} = \frac {\sqrt {\frac {3}{2}} (1 + 6 \overline {{I (k)}})}{\beta R _ {\mathrm{eq}} C}. \tag {25}
$$

Considering the following network conditions: $R _ { \mathrm { e q } } = 0 . 1 8 s ,$ C ¼ 2500packets/s, and $\overline { { l ( k ) } } = 0 . 0 1$ . According to [18], we have $\beta = 0 . 0 0 1$ . Substituting these values to (22), we obtain $\begin{array} { r }  \frac { \theta _ { \mathrm { a } } } { \theta _ { \mathrm { i } } } = 2 . 8 8 5 \ \end{array}$ , that is $\theta _ { \mathbf { a } } > \theta _ { \mathbf { l } }$ . Generally, in most network situations, $\theta _ { \mathsf { a } } > \mathsf { \dot { \theta } } _ { \mathsf { l } }$ is valid.

Suppose TCP/LRED remains an under damping system, we have following observations: (1) According to Lemma 1, the steady-state error, $e _ { s s } ,$ is a decreasing function of proportional parameter $\theta ,$ therefore AOPC obtains smaller steady-state error than LRED; and (2) According to Lemma 2, the settling time, $t _ { s } ,$ , is a decreasing function of proportional parameter h, which means that AOPC has a faster convergence rate than LRED.

Although proportional AQM controller always maintains non-zero steady-state error, this demerit can be overlooked in highly dynamic network scenarios as long as the error is sufficient small. Furthermore, a simple proportional controller can enhance the scalability of AQM algorithms and reduce the computational overhead. In our simulations below, we can observe that the performance of AOPC is never suffered by its small steady-state error.

# 4. Performance evaluation

To comprehensively evaluate the performance and the robustness of the proposed AOPC, we implement the AOPC scheme in NS2 [22] and conduct extensive simulations. Some representative AQM schemes, namely, REM [10], PI [15], PID [16], PIP [17], and LRED [18], are also simulated for the purpose of comparison. The settings of the parameters for various AQM schemes are based on their authors’ recommendations.

The dynamic behaviors of the selected AQM schemes are simulated under a variety of network topologies and traffic models. In particular, we consider the dumbbell network topology. Unless stated elsewhere, the congested link is configured with 10 Mbps, the round trip propagation delays are uniformly distributed over the range [60, 220]ms. We also consider the network topology with multiple bottleneck links as shown in Fig. 3, where each sender-receiver pair has TCP connections as cross traffic. In both scenarios, TCP Reno is used as the transport agent. Unless otherwise specified, the buffer size of each router is set to be 200 packets, and the desired queue length is set to be 50 packets. The total simulation last for 100 s.

# 4.1. Single bottleneck topology

# 4.1.1. Homogeneous traffic: long-lived FTP flows only

Experiment 1. Stability and responsiveness under sudden traffic load change scenario.

In this experiment, we investigate the stability and responsiveness of the AQM schemes under sudden traffic load change scenario. The number of FTP flows is 200 at the beginning and 200 additional FTP flows arrival at the link 50 s later. The queue evolutions are depicted in Fig. 4.

It can be seen that, PI is unable to regulate the queue length to the reference value throughout the simulation runtime. Note that REM and PID are not very robust with respect to such sudden traffic load change scenario, resulting in long time buffer overflows and heavy queue oscillations during 20–50 and 60–100 s. Besides, the queue evolution of REM bears much resemblance to that of PID, due to the fact that REM is in essence a PID-type controller. LRED is too aggressive, resulting in an empty buffer much of the time. AOPC has less overshoots and smaller queue oscillations. On the contrary, the queue lengths of PIP and LRED oscillate over a large range. As shown in Fig. 4, AOPC is robust against the variation of the number of connections and achieves shorter response time and better stability than other algorithms in the presence of sudden traffic change scenario.

![](images/23a13af3caf98694bbf9143040ec75185a3021b95d1803ecdd5ee1384052ff78.jpg)



Fig. 3. Multi-bottleneck topology with two sets of cross traffic.

![](images/50322c4a182edd67007b5fa6dbc82c5ccdf15d73bfddfb0421907a26a9595900.jpg)



(a) PI

![](images/b1fe09ba346f5409d821b4af598cc987e5dd16818a2460d4913e9c19dceb14ed.jpg)



(b) REM

![](images/953d90b20ca603709bfe8fa09f50034e3b8c676d1dedd2c96bebe8d5d6d8c4bf.jpg)



(c) PID

![](images/43e6d176ea3983884ec6095f345f8be6ae70d189113aae7869e06f533c7d5273.jpg)



(d) PIP

![](images/6ae0b499303098e53006d2982609d1c436cf79d7158748f4463696259be1927b.jpg)



(e) LRED

![](images/51a8e2e51186dff0152fb4498989fe7165c26e154724a92f6113b10fc984472d.jpg)



(f) AOPC   
Fig. 4. Experiment 1: evolution of the queue length under sudden traffic load change scenario.

Experiment 2. Convergence under various number of FTP flows.

We use the following Convergence criterion to compare the convergence properties of the AQM algorithms.

Convergence criterion: We assert an AQM algorithm converges to a stable point if and if only it satisfies all following conditions:

(1) the average queue length $A v e Q L e n ( t _ { 0 } , t _ { 0 } + \Delta t )$ during $[ t _ { 0 } , t _ { 0 } + \Delta t ]$ time interval must satisfy $\mid A \nu e Q L e n ( t _ { 0 } , t _ { 0 } -$ þ $\Delta t ) - q _ { 0 } \mid \leqslant \lambda * q _ { 0 } ,$ where Dt is a slot duration, and k is a constant which admits negligible queue deviation between real average queue length and reference queue length $q _ { 0 } ,$ ;

(2) the standard queue deviation $S t a n Q D e v ( t _ { 0 } , t _ { 0 } + \Delta t )$ Þ of $q _ { 0 }$ during $[ t _ { 0 } , t _ { 0 } + \Delta t ]$ time interval must satify $S t a n Q D e v ( t _ { 0 } , t _ { 0 } +$ þ $\Delta t ) \leqslant \mu \ast q _ { 0 }$ , where l is a constant which admits slight queue oscillation around reference queue length $q _ { 0 } ;$ ;   
(3) given any time $t > t _ { 0 } ,$ , condition 1 and 2 must be always satisfied simultaneously.

Thus, we assert the algorithm convergence to a stable point at time $t _ { 0 } + \Delta t / 2$ .

In the experiment, we vary the total number of FTP flows, N, from 300 to 1000 to imitate different congestion degrees. The value of k and $\mu$ set to 0.3 respectively, and the slot duration Dt set to 4 s. Using such an customized convergence criterion, the simulation results show that only AOPC is able to converge to a stable point at different congestion degrees while all other algorithms failed. Fig. 5 plots the convergence times of AOPC, the average queue length, and standard deviation of queue length of all algorithms except PI controller with various congestion degrees. Because PI causes buffer persistent overflows, which leads to large average queue length and small queue deviations. We do not consider its performance here. From the plot, we can conclude that the convergence rate of AOPC is almost independent to the value N. AOPC always converges to the stable point in less that 4 s. Note that the represent lines of PIP and AOPC overlap in the figure of average queue length. PIP obtains small value of average queue length and LRED may also satisfy condition 1 in the convergence criterion, however, both of them violate condition 2 due to their large queue oscillations.

![](images/ba82e549cfd1a6277e712594614d7b1e3725d826fcc1f68a59eae233c53153c0.jpg)



(a)

![](images/b68d53f4ddfacea6346aebc7be17c43c670096626e7e2a370e44f2b5168ab23b.jpg)



![](images/11df2e78b3497e7b47aa21910913fcf5812b62eb201898c79d204db1757141ae.jpg)



Fig. 5. Experiment 2: convergence under various number of FTP flows. (a) Convergence time of AOPC with k ¼ 0:3, l ¼ 0:3, Dt ¼ 4s. (b) Average queue length. (c) Standard deviation of instantaneous queue length.

Experiment 3. AQM performances as functions of round trip time.

In this experiment, we conduct a series of simulations to investigate the performance of the AQM schemes through varying the RTT from 20 to 200 s. We study the performance of queue deviation, link utilization, and packet loss ratio. Fig. 6 plots these metrics as functions of RTT for each AQM schemes except PI controller. From the figure, we observe that as RTT increases, REM and PID show gradually nice performances in respect of queue deviation and packet loss ratio. The queue deviation of AOPC keeps small as the RTT increases, which accounts for its persistent high link utilization. This confirms that small queue oscillations not only indicate low delay jitter but also a guarantee of high link utilization. An unattractive point is that the AOPC encounters a slightly larger proportional of packet losses than REM and PID. The queue deviations of PIP increase steeply as the RTT increases. On the contrary, LRED maintains a mild increment of queue deviations. However, as a result of the aggressiveness of packet drop behavior, LRED drains the queue for a long time of emptiness and hence falls a large stride in terms of link utilization when RTT is set to larger than 100 s.

Experiment 4. AQM performances as a function of link capacity.

In this experiment, we conduct a set of simulations to investigate the performance of the AQM schemes through varying the bottleneck link capacity from 10 to 90 Mbps. We study the performance of queue deviation, link utilization, and packet loss ratio. Fig. 7 plots these metrics as functions of link capacity for each AQM schemes except PI controller. From the figure, we observe that AOPC obtains the smallest queue deviation and satisfactory link utilization and packet loss ratio in all configured link capacities. Although REM and PID obtain slightly higher link utilizations when the link capacity is configured with 90 Mbps, their larger queue deviations mean more oscillatory in terms of queue evolution. The experiment illustrates that AOPC can scale to high speed links yet with stable control of queue evolution and satisfactory performance.

![](images/da50492d91cbc7775f79a8203068f81f29afa9545405e05c8cd00f12dbb3438b.jpg)



(a) Queue deviation

![](images/555c5ddaf0a2adb6974902edc673a4c648e288de77404fc3ade96777ab7269a1.jpg)



(b) Link utilization

![](images/756a85b7c48979efb416b8059645f5f860ed17c7fadf6209efb83f58bce5fdd5.jpg)



(c) Packet loss ratio   
Fig. 6. Experiment 3: queue deviation, link utilization, packet loss ratio as a function of round trip time for each AQM algorithm except PI.

![](images/c4a773043737d365f78bc061d979effab158a895714c66648f84e473bd6eeef3.jpg)



(a) Queue deviation

![](images/822079dbd61d4e4ded8707a48647be4c5ee15e2c5f306868bf71cd4113004365.jpg)



(b) Link utilization

![](images/58af3a50906d700ea5264e13c641f9eba6a7b987966c1d543b13eb80cd11382f.jpg)



(c) Packet loss ratio   
Fig. 7. Experiment 4: queue deviation, link utilization, packet loss ratio as a function of link capacity for each AQM algorithm except PI.

# 4.1.2. Heterogeneous traffic: hybrid flows

Experiment 5. Adding CBR flows, web traffic, and exponential ON/OFF UDP flows.

The unresponsive CBR flows, short-lived web traffic and ON/ OFF UDP flows can influence the control effect of AQM algorithms as the result of queue oscillation or unstable queue evolution. In this experiment, we use a mixture of FTP, CBR, exponential ON/OFF UDP flows, and web traffic to simulate a more realistic network scenario. The number of FTP flows and the number of CBR flows are 100 and 20, respectively. The inter-packet gap of a CBR flow is 0.08 s, and the total introduced CBR flows is approximately 1Mbps. we introduce 30 exponential ON/OFF UDP flows starting at 10 s and the inter-flow arrival time is exponentially distributed with a mean of 0.1 s. The durations of the ‘‘ON” and ‘‘OFF” states are exponentially distributed with a mean of 1 s. Also the introduced ON/OFF flows is approximately 1 Mbps. The web traffic is generated by ‘‘PagePool/Web-Traf” provided by NS2. The page pool attached to each of the congested link contains 5 servers and 5 clients. Each session transfers 1000 pages, such that the sessions never end in the lifetime of the simulation. Other parameters, like the inter-page waiting time, are presented in Table 1. Without any other traffic, the random web traffic utilizes about 1 Mbps.

Fig. 8 plots the queue evolution of the AQM schemes. We see that AOPC can robustly stabilize the queue length around 50 packets, while the queue length of PI keep the peak value for around 60 s. REM and PID require much longer time to decrease their queue size from the buffer top. The queue evolutions of PIP and LRED oscillate along with the dynamics of load levels. Despite AOPC is developed on TCP throughput model, it is close to the ideal performance under hybrid traffic conditions. The simulation results show that PIP, LRED and AOPC outperform REM, PI and PID in terms of responsiveness. Moreover, AOPC has a better queue stability than PIP or LRED. The queue length of AOPC also has a smaller oscillation.

# 4.2. Multiple bottlenecks topology

Experiment 6. Queue stability under multiple bottlenecks topology.

Using the multiple bottleneck network topology depicted in Fig. 9, we study the behavior of different AQM algorithms in the presence of cross traffic. We set 150 FTP flows with senders at the left hand side and receivers at the right hand side, with 60 FTP flows for each sender-receiver pair. We observe that the queue $R _ { 2 } - R _ { 3 }$ and $R _ { 4 } - R _ { 5 }$ exhibit similar trends. Queue R - R and $R _ { 5 } - R _ { 6 }$ are almost empty, indicating that these two links are not bottleneck links. Fig. 9 plots the queue R3 - R4 and $R _ { 4 } - R _ { 5 }$ .

AOPC significantly outperforms other AQM schemes, which are often sensitive to the network configurations such as TCP loads, presence of unresponsive flows, and cross traffic. In the multiple bottlenecks topological situation, PIP is prone to be unstable with continuous queue oscillation. Meanwhile, LRED suffers an aggressive packet drop behavior and makes the buffer empty for long periods, resulting in poor link utilization and continuous packet losses.

Previous simulations illustrate that stable queue evolutions and small queue oscillations do not only mean small queueing delay and jitters, but also high link utilizations. Note that the system convergence rates of other algorithms are deteriorated with higher loads, thus, the high link utilization are gained at the expense of more sluggish responsiveness, longer queueing delay, and larger delay jitter. On the contrary, our proposed AOPC can maintain a fast convergence rate and restrain queue oscillations under various traffic scenarios, achieving high link utilization and being well-suited as an AQM scheme.

Table 1 Parameter setting for PagePool/WebTraf in simulations 

<table><tr><td></td><td>Inter_Session</td><td>Inter_Page</td><td>Page_Size</td><td>Inter_Object</td><td>Object_Size</td></tr><tr><td>Average</td><td>5 s</td><td>4 s</td><td>10</td><td>0.01 s</td><td>10</td></tr><tr><td>Distribution</td><td>Exponential</td><td>Exponential</td><td>Constant</td><td>Exponential</td><td>Pareto II (shape = 1.2)</td></tr></table>

Note: Inter\_Session is the inter-session waiting time; Inter\_Page is the inter-page waiting time; Page\_Size is the number of objects in one page; Inter\_Object is the interobject waiting time; Object\_Size is the size of each object.

![](images/ae2452d737945245d2ad1a01493ec4a3545adc8bc13e55984c5a3d84d0c02ec7.jpg)



(a) PI

![](images/f27e9421f64911a5b756ab5eddc21295b98b867c46610c3e640236bdd60dd7a3.jpg)



(b) REM

![](images/149262a01ec365bb77421589f699d572d18f8e7237b9121b898689553ed2e36f.jpg)



(c) PID

![](images/96ed2140b6d9b4495399add4f53b36cc568595e7e29e963027c8b989f8e79390.jpg)



(d) PIP

![](images/292aefb5f893c0864ba4d11987a5941a05654334870cb1297616cf8625036228.jpg)



(e) LRED

![](images/609ab7cd488ffcd032e2e5fea954e01ae3f0a3a172ace842e00c1deb78579cfb.jpg)



(f) AOPC   
Fig. 8. Experiment 5: queue evolution under hybrid traffic scenario.

![](images/aa767a67e0208d80f03366876eb3b414d0b7e95ba0db8b196375800408e81b8c.jpg)



![](images/1057ef2c1f2f5d070553a4d06eb1df4bf4fa6d82b45c887300949ed0e12516aa.jpg)



(b) REM

![](images/abf987da44f83ca1fc408788031fbf26854be6677a06044bbab2c98ded48989b.jpg)



![](images/d231cebcc1b45b55cc66343172ee83e4fe77df01ab3bbc066c4c5649f57b94cd.jpg)



(d) PIP

![](images/08b062710f55f3eb74901c124fcb1c889355d1627e322f021eb4c57d29406a4b.jpg)



(e) LRED

![](images/e8198dfc2ba6d6b3a4b50ce95d5857663d1333b75262ccb5ed07c90032b201c5.jpg)



(f) AOPC   
Fig. 9. Experiment 6: queue evolution under multiple bottlenecks topology.

# 5. Conclusion

We propose a novel AQM scheme called AOPC. The AOPC scheme employs proportional AQM control to calculate packet drop probability. It measures packet loss ratio on a large time scale and updates packet drop probability on a small time scale upon each packet arrival. By introducing: (1) a network load estimator, which estimates TCP load based on the TCP throughput formula after packet loss ratio measured; and (2) a parameter optimization module, which optimizes the TCP/AOPC feedback control system based on the optimized second-order system model. AOPC detaches the correlation of control parameter from network load and alleviate the sensitivity to the system parameter variations. By using an optimized second-order system model, AOPC regulates the queue close to the desired length with small oscillations under widely varying traffic conditions.

The performance of AOPC is evaluated in simulations and compared with PI, REM, PID, PIP, and LRED. The performance analysis and simulation results show that AOPC is superior to existing AQM algorithms, including REM, PI, PID, PIP, and LRED. The major advantages of AOPC include (1) being stable and responsive in a sudden traffic load change scenario, or in the presence of unresponsive UDP flows and short-lived web traffic; (2) a fast convergence rate and small queue oscillations with respect to a large range of traffic scenarios, achieving a high link utilization; and (3) robustness and fast system response under multiple bottleneck link scenarios.

Our study on AOPC is admittedly in its early stages and there are several issues that need to be discussed in the future. There are several limitations: (1) the TCP throughput formula used to estimate network load produces uncertain estimation errors, especially in light load networks; (2) we ignore the feedback delay, which might be reasonable in small-delay LAN or MAN, but is definitely harmful to system stability; (3) different versions of TCP implementation, such as Reno, Vegas, etc, do coexist in the Internet and we should consider. Actually, the TCP/AQM model only describes the TCP Reno congestion control mechanism. Other unresponsive flows, for example, UDP flows and web traffic, should also be considered in the control system.

Recent technology trends indicate that the future Internet will have a large number of high-bandwidth links. With the transmission rate speeding up, the surge of interest of designing new transmission control protocols is increasingly active [24–26]. The research of TCP/AQM control system in high speed network is also a hot issue [27,28]. Therefore, it might be difficult, if not impossible, to employ an accurate model of network traffic and the queue dynamics with fixed parameters. An alternative way to address this issue could be regarding the controlled system as an uncertain system, and employing parameter identification approach to adjust the control laws, i.e., the packet drop behavior, accordingly.

# Acknowledgements

This work is supported by the National Natural Science Foundation of China (60673164), the Provincial Natural Science Foundation of Hunan (06JJ10009), the Specialized Research Fund for the Doctoral Program of Higher Education of China (20060533057), the National Basic Research 973 Program of China (2008CB317107), and the Program for New Century Excellent Talents in University (NCET-05-0683).

# References

[1] B. Braden, D. Clark, J. Crowcroft, B. Davie, S. Deering, D. Estrin, Recommendations on queue management and congestion avoidance in the Internet, IETF RFC 2309, 1998.   
[2] S. Floyd, TCP and explicit congestion notification, ACM Computer Communication Review 24 (1998) 10–23.   
[3] S. Floyd, V. Jacobson, Random early detection gateways for congestion avoidance, IEEE/ACM Transactions on Networking 1 (4) (1993) 397–413.   
[4] S. Floyd, Recommendations on using the gentle variant of RED, 2000. Available from: <http://www.aciri.org/floyd/gentle.html/>.   
[5] S. Floyd, R. Gummadi, S. Shenker, Adaptive RED: an algorithm for increasing the robustness of RED’s active queue management, 2001. Available from: http://www.icir.org/floyd/papers/adaptiveRed.pdf.   
[6] T. Ott, T. Lakshman, L. Wong, SRED: stabilized RED, in: Proceedings of IEEE INFOCOM, New York, March 1999, pp. 1346–1355.   
[7] W. Feng, D.D. Kandlur, D. Saha, D. Saha, The blue active queue management algorithms, IEEE/ACM Transactions on Networking 10 (4) (2002) 513–528.

[8] S. Kunniyur, R. Srikant, Analysis and design of an adaptive virtual queue (AVQ) algorithm for active queue management, in: Proceedings of ACM SIGCOMM, San Diego, 2001, pp. 123–134.   
[9] J. Aweya, M. Ouellette, Delfin Y. Montuno, K. Felske, Rate-based proportionalintegral control scheme for active queue management, International Journal of Network Management 16 (3) (2006).   
[10] S. Athuraliya, S. Low, V. Li, Q. Yin, REM: active queue management, IEEE Network Magazine 15 (2001) 48–53.   
[11] J. Hong, C. Joo, S. Bahk, Active queue management algorithm considering queue and load states, Elsevier Computer Communications 33 (4) (2007) 886– 892.   
[12] J. Sun, M. Zukerman, RaQ: a robust active queue management scheme based on rate and queue length, Elsevier Computer Communications 33 (8) (2007) 1731–1741.   
[13] V. Misra, W. Gong, D. Towsley, Fluid-based analysis of a network of AQM routers supporting TCP flows with an application to RED, in: Proceedings of ACM SIGCOMM, Stockholm, Sweden, 2000, pp. 151–160.   
[14] C. Hollot, V. Misra, D. Towsley, W. Gong, A control theoretic analysis of RED, in: Proceedings of IEEE INFOCOM, Anchorage, Alaska, 2001, pp. 1510– 1519.   
[15] C. Hollot, V. Misra, D. Towsley, W. Gong, On designing improved controllers for AQM routers supporting TCP flows, in: Proceedings of IEEE INFOCOM, Anchorage, Alaska, USA, 2001, pp. 1726–1734.   
[16] F. Ren, F. Wang, Y. Ren, X. Shan, PID controller for active queue management, Journal of Electronics and Information Technology (China), 25 (1) 2003.   
[17] H. Zhang, B. Liu, W. Dou, Design of a robust active queue management algorithm based on feedback compensation, in: Proceedings of ACM SIGCOMM, Kalsruhe, 2003, pp. 265–276.

[18] C. Wang, B. Li, Y. Thomas Hou, K. Sohraby, Y. Lin, LRED: a robust active queue management scheme based on packet loss ratio, in: Proceedings of IEEE INFOCOM, Hongkong, 2004, pp. 1–12.   
[19] J. Padhye, V. Firoiu, D. Towsley, J. Krusoe, Modeling TCP throughput: a simple model and its empirical validation, in: Proceedings of ACM SIGCOMM, Vancouver, August 1998, pp. 304–314.   
[20] H. Jiang, C. Dovrolis, Passive estimation of TCP round-trip times, ACM Computer Communications Review 32 (3) (2001) 75–88.   
[21] S. Shakkottai, R. Srikant, N. Brownlee, Andre Broido, The RTT distribution of TCP flows in the Internet and its impact on TCP-based flow control, 2004. Available from: <http://www.caida.org/outreach/papers/2004/tr-2004-02/tr-2004-02.pdf/>.   
[22] UCN/LBL/VINT, Network Simulator-NS2. Available from: <http://wwwmash.cs.berkeley.edu/ns/>.   
[23] Qi Wu, Automatic control theory, Tsinghua University Press, China, 1990. pp. 134–140.   
[24] D. Katabi, M. Handley, C. Rohrs, Congestion control for high bandwidth delay product networks, ACM SIGCOMM (2002).   
[25] C. Jin, D. Wei, S.H. Low, FAST TCP: motivation, architecture, algorithms, performance, in: IEEE INFOCOM, 2004.   
[26] Y. Zhang, D. Leonard, D. Loguinov, JetMax: scalable max–min congestion control for high-speed heterogeneous networks, in: IEEE INFOCOM, 2006.   
[27] F. Paganini, Z. Wang, Steven H. Low, John C. Doyle, A new TCP/AQM for stable operation in fast networks, in: Proceedings of IEEE INFOCOM 2003, San Francisco, USA, April 2003, pp. 96–105.   
[28] S. Liu, T. Basar, R. Srikant, Exponential-RED: a stabilizing AQM scheme for lowand high-speed TCP protocols, IEEE/ACM Transactions on Networking 13 (5) (2005).