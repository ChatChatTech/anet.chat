# Design of a stabilizing AQM controller for large-delay networks based on internal model control q

Jianxin Wang a,\*, Liang Rong a , Yunhao Liu b

a School of Information Science and Engineering, Central South University, Changsha 410083, China b Department of Computer Science, Hong Kong University of Science and Technology, Hong Kong, China

Received 29 March 2007; received in revised form 9 December 2007; accepted 17 December 2007 Available online 31 December 2007

# Abstract

We focus on the problem of the stability of congestion control for networks with large round-trip communication delays. Nearly all the existing AQM schemes neglect the impact large communication delay has on system behavior, such as stability, robustness and convergence. The drastic queue oscillations in large delay networks of PI, REM and DC-AQM decrease link utilization and introduce avoidable delay jitter. To address this problem, we propose a robust IMC-PID congestion controller based on the internal model control principle to restrict the negative impact of the stability caused by large delay. Simulation results demonstrate that the integrated performance of our proposed scheme outperforms others as communication delay increases, and achieves high link utilization and small delay jitter.

\- 2007 Elsevier B.V. All rights reserved.

Keywords: Congestion control; Active queue management; Internal model control; Large-delay networks; Stability

# 1. Introduction

Congestion control in communication networks has become increasingly important due to the explosive expansion and the growth of traffic. From the control theory point of view, congestion control problems are complex and challenging due to their high-dimensional, nonlinear, and dynamic properties. In practical, individual sources have to select their transmission rates in a decentralized way with little information about the rest of the network.

Recent advances in mathematical modeling of congestion control have stimulated the research on theoretic analysis of the behavior, such as stability, robustness and fairness, of currently developed Internet congestion control protocols as well as the design of new protocols with higher performance [2–6]. One of the most important factors in the design of congestion control is its asymptotic stability, which is the capacity of the system to avoid oscillations in the steady-state and to properly respond to external perturbations caused by the arrival/departure of flows, variation in feedback, and other transient effects. Stability proofs for distributed congestion control become progressively more complicated as feedback delays are taken into account. However, most existing congestion controllers, such as RED [1], REM [7], PI [9], AOPC [10] and so on, neglect the impact on performance caused by large round-trip communication delay. Although DC-AQM [11] set its goal to tackle the delay stability issue in large-delay networks, the employed parameter tuning method, pade´ approximation, results in the large mismatch between plant and model. Simulation results in Section 2 illustrate these

q This paper is an extended version of our previous paper appeared in ICC 2007. This work is supported by the National Natural Science Foundation of China (60673164), the Provincial Natural Science Foundation of Hunan (06JJ10009), the Specialized Research Fund for the Doctoral Program of Higher Education of China (20060533057), and the Program for New Century Excellent Talents in University (NCET-05- 0683). \* Corresponding author. Tel.: +86 731 8830212; fax: +86 731 8876677. E-mail addresses: jxwang@mail.csu.edu.cn (J. Wang), csulrong@ gmail.com (L. Rong), liu@cs.ust.hk (Y. Liu).

controllers result in dramatic oscillations in large delay networks, which decrease the utilization of the bottleneck link and introduce the avoidable delay jitter.

The objective of this research is to propose a stabilizing congestion control system that maintains both stability and ideal transient performance under arbitrary feedback delays, especially in large round-trip communication delay scenarios. The proportional-integral-differential (PID) controller is widely adopted to regulate the network router buffer’s queue length. Some advanced PID controllers, designed using various methods like gain margin, phase margin [14], dominant pole placement [9], and linear quadratic regulators [15], are proposed to improve the stability and responsiveness of the TCP/AQM system. However, these proposals do not consider the delay stability issue [16,17]. Stability proofs for distributed congestion control become progressively more complicated as feedback delays are taken into account. We solve this problem by applying the principle of internal model compensation in control theory to restrict the negative impact on the queue stability caused by feedback delay. We call the new scheme IMC-PID congestion controller. Instead of using pade´ approximation to approximate the delay element [11], we apply the Taylor series expanding approach to reduce the plant/model mismatch. By choosing appropriate PID parameters, the IMC-PID controller can maintain stability with higher link utilization and smaller queue oscillation than that of other AQM controllers with arbitrary feedback delays.

The rest of the paper is organized as follows. In Section 2, we evaluate the negative impact of large delay on TCP/ AQM system performance. Section 3 makes an overview of the TCP/AQM control system and internal model control (IMC) principle. In Section 4, we develop a robust, stable IMC-PID congestion controller for large-delay networks and give some guidelines for parameter settings. The performance of IMC-PID is compared with that of REM, PI, and DC-AQM in Section 5. Finally, we conclude our research in Section 6.

# 2. Effect of large delay on TCP/AQM system performance

The dynamics of congestion control may be abstracted as a control loop with feedback delay. A fundamental characteristic of such system is that it becomes unstable for some large feedback delays. A fundamental principle from control theory states that a controller must react as quickly as the dynamics of the controlled signal; otherwise the controller will always lag behind the controlled system and will be ineffective. In the context of current proposals for congestion control, the controller is an AQM scheme. Most previous AQM schemes [1,7,9,10], which configure the parameters in the small-delay network scenarios, do not consider the effect of large feedback delay on TCP/AQM system performance. These design approaches cause the system oscillation in large feedback delay networks. Table 1 shows the round trip delays to different overseas websites from the host at Central South University in China. We can see that the maximum average RTT is larger than 1 s. However, Internet measurements report that roughly 75–90% of flows have RTTs less than 200 ms [20] and the average RTT is distributed around 180 ms [21]. Therefore, the RTTs between two overseas websites are on an average larger than that of a majority network flows.

Table 1 RTT statistical values 

<table><tr><td>URL</td><td>Minimum delay (ms)</td><td>Maximum delay (ms)</td><td>Average delay (ms)</td></tr><tr><td>www.ieee.org(61.200.81.134)</td><td>411</td><td>432</td><td>419</td></tr><tr><td>www.acm.org(63.118.7.16)</td><td>1101</td><td>1155</td><td>1131</td></tr><tr><td>www.yahoo.com(209.73.186.238)</td><td>347</td><td>355</td><td>352</td></tr><tr><td>www.mit.edu(18.7.22.83)</td><td>298</td><td>308</td><td>302</td></tr></table>

In order to investigate the performance of the existing typical AQM schemes, in particular, we select PI, REM and DC-AQM schemes to verify their stability in large delay networks. We conducted two sets of simulations under the dumbbell network topology scenario with average RTTs of 150 and 400 ms having uniformly distributed RTT ranges of [100, 200] ms and [200, 600] ms, respectively. In both cases, the buffer size is 300 packets, and the reference queue length is set to 150 packets in all

![](images/c6a1f6eb54ddc573734131e768fced146b65397b60526d04743341bf5754ab09.jpg)



Fig. 1. Queue evolution. The dotted lines and solid lines represent RTT = 150 and 400 ms, respectively. All of the three AQM schemes are prone to being unstable while increasing RTT.

Table 2 Link utilization and queue statistics 

<table><tr><td>Schemes</td><td colspan="2">PI</td><td colspan="2">REM</td><td colspan="2">DC-AQM</td><td colspan="2">IMC-PID</td></tr><tr><td>RTT (ms)</td><td>150</td><td>400</td><td>150</td><td>400</td><td>150</td><td>400</td><td>150</td><td>400</td></tr><tr><td>Link utilization</td><td>99.34%</td><td>97.27%</td><td>99.31%</td><td>91.14%</td><td>99.40%</td><td>95.50%</td><td>99.33%</td><td>97.30%</td></tr><tr><td>Average queue length (pkts)</td><td>162.42</td><td>150.80</td><td>154.22</td><td>102.67</td><td>157.25</td><td>32.98</td><td>175.88</td><td>149.72</td></tr><tr><td>Queue deviation (pkts)</td><td>44.23</td><td>63.89</td><td>45.16</td><td>112.26</td><td>28.16</td><td>30.81</td><td>46.52</td><td>42.16</td></tr></table>

AQM schemes, which accounts for 60 ms queueing delay in the congested router. The most congested link whose capacity is configured 15 Mbps are shared by 100 greedy and sustained FTP flows. The simulation scenario is also used in [11]; however, we replace homogeneous flows used in [11] with heterogeneous flows by configuring various RTT delays for all FTP flows. Fig. 1 demonstrates unstable dynamic behaviors of these AQM schemes in large-delay networks, though they can converge to steady-state fast in small-delay networks. The large queue oscillations of PI and REM indicate large delay jitter and/or low link utilization. DC-AQM does not converge to the reference queue length, though it is designed to compensate large delays. Table 2 summarizes the performance and statistical queue length for each scheme. As shown in Fig. 1 and Table 2, although PI keeps relative high link utilization, the queue is unstable and the queue deviation increases by 20 packets. The average queue length of DC-AQM shrinks to 30 packets, which leads to low link utilization. The queue deviation increases by 70 packets in REM, which is unfavorable to QoS requirement for real-time applications.

# 3. TCP/AQM control system and internal model control

In this section, we give a description of the TCP/AQM interconnection system model and the IMC based PID control.

# 3.1. TCP/AQM control system model

Nonlinear ordinary differential equations, which describe the transient behavior of networks with AQM routers supporting TCP flows, are developed in [2]. These equations are linearized in [8] and the linear TCP/AQM system model can be depicted as in Fig. 2, where $q _ { 0 }$ is the reference queue size. The action of an AQM controller is to mark (or drop) packets with probability p as a function of the measured difference between the real queue length q and the reference queue length $q _ { 0 } .$ . From Fig. 2, the plant transfer function, $P ( s ) = P _ { t c p } ( s ) P _ { q u e } ( s )$ , can be expressed in terms of network parameters yielding:

![](images/b3f8d7021046a21ed5e9f9d26745f0fb8be4fd39cc51ec246c362cfde8fa6210.jpg)



Fig. 2. TCP/AQM feedback control system model.

$$
P _ {t c p} (s) = \frac {\frac {R _ {0} C ^ {2}}{2 N ^ {2}}}{s + \frac {2 N}{R _ {0} ^ {2} C}}, \quad P _ {q u e} (s) = \frac {\frac {N}{R _ {0}}}{s + \frac {1}{R _ {0}}}, \tag {1}
$$

where $R _ { 0 }$ is round-trip time (RTT), N is the number of active TCP sessions, and C is link capacity (packets/s).

The plant dynamics, denoted by the transfer function $P ( s )$ , relates how this packet-marking probability dynamically affects the queue length. From (1) and Fig. 2 we have

$$
P (s) = \frac {K _ {m} \mathrm{e} ^ {- s R _ {0}}}{(T _ {1} s + 1) (T _ {2} s + 1)}, \tag {2}
$$

where, Km ¼ ðR0CÞ 3 , $\begin{array} { r } { K _ { m } = \frac { ( R _ { 0 } C ) ^ { 3 } } { 4 N ^ { 2 } } , T _ { 1 } = \frac { R _ { 0 } ^ { 2 } C } { 2 N } , T _ { 2 } = R _ { 0 } . } \end{array}$ 4N 2  T 1 ¼

# 3.2. Internal model control

The internal model control (IMC) was introduced by Garcia and Morari [12]. Using the IMC design procedure, controller complexity depends exclusively on two factors: the complexity of the model and the performance requirements stated by the designer. The control principle of IMC can be illustrated in Fig. 3, where $G _ { i } ( s )$ is the internal model controller, $G _ { c } ( s )$ the feedback controller, $G _ { p } ( s )$ the real plant, and $\widehat { G } _ { p } ( s )$ the inner model. Plant/model mismatch can be caused by model reduction (the representation of a high-order system by a low-order approximate model) or by system parameters which depend on the operating conditions. From Fig. 3, we can obtain the relationship between $G _ { i } ( s )$ and $G _ { c } ( s )$ as follows:

$$
G _ {i} (s) = \frac {G _ {c} (s)}{1 + G _ {c} (s) \widehat {G} _ {p} (s)}, \tag {3}
$$

$$
G _ {c} (s) = \frac {G _ {i} (s)}{1 - G _ {i} (s) \widehat {G} _ {p} (s)}. \tag {4}
$$

![](images/8deb09ce294bf0f5fb34c5d0d977f4fe846203d4b20d5388e236f8c887fe24d3.jpg)



Fig. 3. IMC and equivalent feedback control structure.

The control of large-delay system has been a major issue in control theory. The Smith predictor [13] is a widely used time-delay compensator; however, it is excessively sensitive to model mismatch. IMC surmounts this drawback of the Smith predictor, and enhances the robustness and the ability to resist disturbance. The IMC design procedure is very simple and straightforward and it can be divided into following two steps:

Step 1. Factor the model

$$
\widehat {G} _ {p} (s) = \widehat {G} _ {p ^ {+}} (s) \cdot \widehat {G} _ {p ^ {-}} (s) \tag {5}
$$

such that $\widehat { G } _ { p ^ { + } } ( s )$ contains all time delays and right-half plane (RHP) zeros; consequently $\widehat { G } _ { p ^ { - } } ( s )$ is stable and does not involve predictors.

Step 2. Define the IMC controller by

$$
G _ {i} (s) = \widehat {G} _ {p ^ {-}} ^ {- 1} (s) \cdot g (s), \tag {6}
$$

where $g ( s )$ is a low pass filter with

$$
g (s) = \frac {1}{(\varepsilon s + 1) ^ {\gamma}}, \tag {7}
$$

where e is an adjustable filter parameter which determines the speed of response, c is the order that must be selected such that $G _ { i } ( s )$ is proper, namely c must be equal to or greater than the order of $\widehat { G } _ { p ^ { - } } ^ { - 1 } ( s )$ . From (4), (6) and (7), we obtain

$$
G _ {c} (s) = \frac {\widehat {G} _ {p ^ {-}} ^ {- 1} (s)}{(\varepsilon s + 1) ^ {\gamma} - \widehat {G} _ {p ^ {+}} (s)}. \tag {8}
$$

# 4. Design of the IMC-PID congestion controller

# 4.1. IMC-PID parameter tuning guideline

The goal of this section is to show that the IMC design procedure leads naturally to PID-type controllers as a simple TCP/AQM congestion control model. For convenience, we first give the design guideline for IMC-PID controller as follows.

Theorem 1. Given a model $\widehat { G } _ { p } ( s ) = \widehat { G } _ { p ^ { + } } ( s ) \cdot \widehat { G } _ { p ^ { - } } ( s )$ such that $\widehat { G } _ { p ^ { + } } ( s )$ contains all time delays and RHP zeros; consequently $\widehat { G } _ { p ^ { - } } ( s )$ is stable and does not involve predictors.

Let $\begin{array} { r } { f ( s ) = \widehat { G } _ { p ^ { - } } ^ { - 1 } ( s ) / \frac { ( \varepsilon s + 1 ) ^ { \gamma } - \widehat { G } _ { p ^ { + } } ( s ) } { s } , I f \widehat { G } _ { p ^ { + } } ( 0 ) = 1 } \end{array}$ , then we can use the ideal PID controller $\begin{array} { r } { G _ { c } ( s ) = K _ { c } \Big ( 1 + \frac { 1 } { T _ { i } s } + T _ { d } s \Big ) } \end{array}$ to regulate the plant, and the PID control parameters are configured as follows:

$$
K _ {c} = f ^ {\prime} (0), \quad T _ {i} = \frac {f ^ {\prime} (0)}{f (0)}, \quad T _ {d} = \frac {f ^ {\prime \prime} (0)}{2 f ^ {\prime} (0)}, \tag {9}
$$

where $f ^ { \prime } ( 0 )$ and $f ^ { \prime \prime } ( 0 )$ are, respectively, the first- and secondorder derivatives of f(s) at $s = 0$ .

Proof. Recalling that the transfer function of the feedback controller $G _ { c } ( s )$ in $( 8 ) , \widehat { G } _ { p ^ { + } } ( 0 ) = 1$ makes the denominator polynomial of $G _ { c } ( s )$ being zero at $s = 0$ , which matches the condition of system control without steady-state error. Therefore, we can infer that $G _ { c } ( s )$ contains integral elements, and (8) can be denoted as $\begin{array} { r } { G _ { c } ( s ) \equiv { \frac { 1 } { s } } f ( s ) } \end{array}$ , where

$$
f (s) = \frac {\widehat {G} _ {p ^ {-}} ^ {- 1} (s)}{\frac {(\varepsilon s + 1) ^ {\gamma} - \widehat {G} _ {p ^ {+}} (s)}{s}}.
$$

Expanding f(s) according to the Taylor series, we obtain

$$
\begin{array}{l} G _ {c} (s) = \frac {1}{s} \left(f (0) + f ^ {\prime} (0) s + f ^ {\prime \prime} (0) s ^ {2} + \dots\right) \\ = K _ {c} \left(1 + \frac {1}{T _ {i} s} + T _ {d} s + \dots\right), \\ \end{array}
$$

where, $\begin{array} { r } { K _ { c } = f ^ { \prime } ( 0 ) , T _ { i } = \frac { f ^ { \prime } ( 0 ) } { f ( 0 ) } , T _ { d } = \frac { f ^ { \prime \prime } ( 0 ) } { 2 f ^ { \prime } ( 0 ) } , } \end{array}$ T d ¼ , and $K _ { c } , T _ { i } , T _ { d }$ correspond to PID control parameters. h

As given in Theorem 1, TCP/AQM system is a linear feedback system with delay. The stability of such a system can be regulated by the IMC-PID controller. Different from the former IMC-PID parameter tuning approach [11], which employs pade´ approximation for the delay element to yield a low-order approximate model, we apply the Taylor series in tuning IMC-PID parameters to reduce the plant/model mismatch caused by model reduction.

The control parameters are determined by the complicated function $f ( s )$ , and the calculation of its firstand second-order derivatives at $s = 0$ is given as follows.

Let $D ( s )$ denote the denominator polynomial of ${ \widehat { f } } ( s )$ , that is

$$
D (s) = \frac {(\varepsilon s + 1) ^ {\gamma} - \widehat {G} _ {p ^ {+}} (s)}{s}. \tag {10}
$$

Applying Taylor series to expand $D ( s )$ , we obtain

$$
D (0) = \gamma \varepsilon - \widehat {G} _ {p ^ {+}} ^ {\prime} (0), \tag {11}
$$

$$
D ^ {\prime} (0) = \frac {\gamma (\gamma - 1) \varepsilon^ {2} - \widehat {G} _ {p ^ {+}} ^ {\prime \prime} (0)}{2 !}, \tag {12}
$$

$$
D ^ {\prime \prime} (0) = \frac {\gamma (\gamma - 1) (\gamma - 2) \varepsilon^ {3} - \widehat {G} _ {p ^ {+}} ^ {\prime \prime \prime} (0)}{3 !}. \tag {13}
$$

According to (10)–(13), we can calculate function $f ( s )$ （2 and its first- and second-order derivatives at $s = 0$ :

$$
f (0) = \frac {1}{K _ {m} D (0)}, \tag {14}
$$

$$
f ^ {\prime} (0) = - \frac {\widehat {G} _ {p ^ {-}} ^ {\prime} (0) D (0) + K _ {m} D ^ {\prime} (0)}{\left(K _ {m} D (0)\right) ^ {2}}, \tag {15}
$$

$$
f ^ {\prime \prime} (0)
$$

$$
= f ^ {\prime} (0) \left(\frac {\widehat {G} _ {p ^ {-}} ^ {\prime \prime} (0) D (0) + 2 \widehat {G} _ {p ^ {-}} ^ {\prime} (0) D ^ {\prime} (0) + K _ {m} D ^ {\prime \prime} (0)}{\widehat {G} _ {p ^ {-}} ^ {\prime} (0) D (0) + K _ {m} D ^ {\prime} (0)} + \frac {2 f ^ {\prime} (0)}{f (0)}\right), \tag {16}
$$

where $K _ { m } = \widehat { G } _ { p ^ { - } } ( 0 )$ is the proportional amplification coefficient of the model.

# 4.2. Application to TCP/AQM control system

In this section, we describe the design of IMC-PID congestion controller according to Theorem 1 and the IMC design procedure. We assume the internal model for the IMC-PID congestion controller is

$$
\widehat {G} _ {p} (s) = P (s) = \frac {K _ {m} e ^ {- s R _ {0}}}{(T _ {1} s + 1) (T _ {2} s + 1)}. \tag {17}
$$

According to the IMC design procedure, $\widehat { G } _ { p } ( s )$ can be factored as

$$
\widehat {G} _ {p ^ {+}} (s) = e ^ {- s R _ {0}}, \quad \widehat {G} _ {p ^ {-}} (s) = \frac {K _ {m}}{(T _ {1} s + 1) (T _ {2} s + 1)}. \tag {18}
$$

Therefore,

$$
\widehat {G} _ {p ^ {-}} (0) = K _ {m}, \tag {19}
$$

$$
\widehat {G} _ {p ^ {-}} ^ {\prime} (0) = - K _ {m} (T _ {1} + T _ {2}), \tag {20}
$$

$$
\widehat {G} _ {p ^ {-}} ^ {\prime \prime} (0) = 2 K _ {m} (T _ {1} ^ {2} + T _ {2} ^ {2} + T _ {1} T _ {2}), \tag {21}
$$

$$
\widehat {G} _ {p ^ {+}} (0) = 1, \quad \widehat {G} _ {p ^ {+}} ^ {\prime} (0) = - R _ {0},
$$

$$
\widehat {G} _ {p ^ {+}} ^ {\prime \prime} (0) = R _ {0} ^ {2}, \quad \widehat {G} _ {p ^ {+}} ^ {\prime \prime \prime} (0) = - R _ {0} ^ {3}. \tag {22}
$$

We set $\gamma = 2$ in the low pass filter g(s) to guarantee the rationality of the IMC controller $G _ { i } ( s )$ . Substitute $\gamma = 2$ into (11)–(13), we obtain:

$$
D (0) = 2 \varepsilon + R _ {0}, \quad D ^ {\prime} (0) = \frac {2 \varepsilon^ {2} - R _ {0} ^ {2}}{2}, \quad D ^ {\prime \prime} (0) = \frac {R _ {0} ^ {3}}{6}.
$$

By substituting these expressions into (14)–(16), we can obtain the values of $f ( 0 ) , f ( 0 )$ and f00(0). Thus the controller parameters can be derived according to (9).

# 4.3. Implementation of IMC-PID congestion controller

Now, we have obtained an IMC-PID congestion controller which has the ability to restrict the negative impact on the system oscillations caused by large feedback delay. For a digital implementation, we need to convert the time-continuous system into time-discrete system by using a sample technique. Let T denotes the sample interval and the initial value of the drop probability is zero. In the kth sample interval, the arrival packet will be dropped with probability

$$
\begin{array}{l} p (k T) = p ((k - 1) T) + K _ {c} \left\{\left(1 + \frac {T}{T _ {i}} + \frac {T _ {d}}{T}\right) e (k T) \right. \\ \left. - \left(1 + \frac {2 T _ {d}}{T}\right) e ((k - 1) T) + \frac {T _ {d}}{T} e ((k - 2) T) \right\}, \tag {23} \\ \end{array}
$$

where $e ( k T ) = q ( k T ) - q _ { 0 } .$ .

In order to implement the controller, we need to determine the value of e and T. T is set approximately equal to the average RTT, in particular $T = 0 . 4 ~ \mathrm { s }$ . We conducted extensive simulations using MATLAB with different network parameters to investigate the impact of parameter e.

Results show that the system has only a small overshoot and small settling time when ${ \varepsilon = 0 . 3 – 0 . 5 R _ { 0 } }$ .

Consider a network scenario in which mean packet size = 500 bytes, $C = 3 7 5 0$ packet/s (or equivalently, 15 Mbps), $N = 6 0$ , and $R _ { 0 } = 0 . 4 0 ~ \mathrm { s } ,$ , choosing $\varepsilon = 0 . 5 R _ { 0 } .$ then the IMC-PID congestion controller can calculated as:

$$
G _ {c} (s) = 2. 9 0 6 7 \times 1 0 ^ {- 5} \left(1 + \frac {1}{5 . 4 5 s} + 0. 4 1 5 7 s\right). \tag {24}
$$

According to (23), the equation for updating the drop probability can be calculated as follows:

$$
\begin{array}{l} p (k T) = p ((k - 1) T) + 6. 1 4 1 1 1 \times 1 0 ^ {- 5} e (k T) \\ - 8. 9 4 8 8 9 \times 1 0 ^ {- 5} e ((k - 1) T) + 3. 2 1 1 1 1 \\ \times 1 0 ^ {- 5} e ((k - 2) T) \tag {25} \\ \end{array}
$$

# 5. Performance evaluation

In this section, we investigate the performance of IMC-PID congestion controller through NS [18] simulations. The dynamic behaviors of the previous AQM schemes are simulated under a variety of network topologies. In particular, we consider the classical dumbbell network topology. We also consider the network topology with multiple bottleneck links as shown in Fig. 4, where the maximum buffer of each router is also 300 packets, and each sender-receiver pair uses TCP connections as cross traffic. In both scenarios, TCP Reno is used as the transport agent.

# 5.1. Simple dumbbell topology network

# 5.1.1. Queue stability

For completeness, we continue using the simulation from Section 2 to investigate the stability of IMC-PID with average RTTs of 150 and 400 ms, respectively. The queue evolutions are plotted in Fig. 5 and the performances are tabulated in Table 2. Simulation results demonstrate that IMC-PID successfully restricts the negative impact on the queue stability caused by the large delay. Moreover, it gains a fast convergence rate when the average RTT is 400 ms. Compared with the results of other AQM schemes, IMC-PID obtains higher link utilization, relative better controls of queue length, and smaller queue deviations.

# 5.1.2. Packet drop behavior

The large queue oscillations generated in PI and REM and undesired queue evolution of DC-AQM probably result from the misbehaving controller output, i.e. packet drop probability. Inaccurate output control signal may lead to undesirable system behavior. In other words, smaller packet drop probability may cause undesired larger queue evolution, and vice versa. According to the wellknown TCP throughput formula [19], $C / N = \sqrt { 3 / 2 } /$ $( R _ { 0 } \sqrt { p _ { 0 } } )$ , the packet drop probability in steady state is around 0.6% in this experiment. Fig. 6 plots the packet drop probability of each AQM controller. Obviously, IMC-PID controller maintains more stable packet drop behavior, and other controllers yield dynamic outputs which result in the queue oscillations. The small packet drop probability of PI is the matter of the fact that the queue length of PI keep high for a longer time than that of other schemes. The largely dynamic packet drop probabilities of REM have caused the frequent queue oscillations. The undesired queue evolution of DC-AQM results from the large packet drop probability.

![](images/7e8b6992c0556cc0888e424a61305a7b055130c240e465b883481c16ecd7443d.jpg)



Fig. 4. Network topology with multiple bottleneck links and cross traffic. Each TCP connection shares link capacity with a pair of cross traffic at the congested link $\mathbf { R } _ { 2 }  – \mathbf { R } _ { 3 }$ and $\mathrm { R } _ { 4 } { \bf - R } _ { 5 }$ .

![](images/ff38eb837a327a50bfc00b903218f97095f1196ef0a0fbd77a7b1a6204c13071.jpg)



Fig. 5. Queue evolution of IMC-PID. The dotted line and solid line represent $\mathrm { R T T } = 1 5 0$ and 400 ms, respectively. IMC-PID obtains more stable queue controls than PI, REM, and DC-AQM.

# 5.1.3. Link utilization as a function of the average RTT

In order to study the effect on link utilization caused by various RTT, we vary RTT from 50 to 1000 ms with 20 segments. We repeat the experiment with different reference queue length being set to 25 packets and 150 packets respectively. After every experiment, we record the bottleneck link utilization and plot the results in Fig. 7. From the figure, we can observe that IMC-PID obtains roughly the same link utilization when RTTs are equal and its performance is hardly affected by the reference queue length. The DC-AQM achieves the similar property as IMC-PID, but its link utilizations decrease faster as the RTT growing up. However, this is not true for other controllers. The link utilizations of PI and REM decrease dramatically with large delay and small reference queue length.

![](images/38a58e9fd5dbdfa88879f948ac637c31555f2f91859ab352bbfe68b5bac28663.jpg)



Fig. 6. Packet drop probability of each AQM controller. Note that we use different scales on the drop Probability axis to display the plot for prettiness.

![](images/753b654b9508af41d98c5da60410336ca8b0bb0c0a735408f6bdaa9f6b1f53d5.jpg)



Fig. 7. Link utilization as a function of the average RTT. Each AQM scheme is verified with different reference queue length being set to 25 (represented by the dotted line) and 150 (represented by the solid line), respectively.

![](images/db96d5f3444241fce874d1b6377329c3f88010289988e9c50bcd74d130bd209c.jpg)



Fig. 8. Evolution of queue $\ \mathbf { R } _ { 2 } \mathbf { - R } _ { 3 } .$

# 5.2. Multiple bottleneck topology with cross traffic

Using the multiple bottleneck network topology depicted in Fig. 4, we study the behavior of different AQM algorithms in the presence of cross traffic. We set 120 FTP flows with senders at the left hand side and receivers at the right hand side, and 90 FTP flows with each cross sender–receiver pair. We collect the queue length for the AQM schemes of the congested routers. Simulation results show that queue $\mathbf { R } _ { 2 } \mathbf { - R } _ { 3 }$ and queue $\mathrm { R } _ { 4 } { \mathrm { - R } } _ { 5 }$ exhibit similar trends, so we do not plot the data of queue $\mathrm { R } _ { 4 } { \mathrm { - R } } _ { 5 }$ . Queue $\mathrm { R } _ { 3 ^ { - } } \mathrm { R } _ { 4 }$ is slightly congested and no packet losses are captured in this queue. Queue $\mathrm { R } _ { 1 } \mathrm { - R } _ { 2 }$ and queue $\mathrm { R } _ { 5 ^ { - } } \mathrm { R } _ { 6 }$ are almost empty, indicating that these two links are not bottleneck links. The instantaneous queues of $\mathbf { R } _ { 2 } \mathbf { - R } _ { 3 }$ for different AQMs are depicted in Fig. 8.

In Fig. 8, we can see that all the AQM schemes have noticeable oscillations in this case with multiple bottlenecks and cross traffic; yet IMC-PID controls the queue length significantly better than others. PI exhibits larger queue oscillation than IMC-PID. REM oscillates largely in the congested routers, and frequently causes buffer overflows and emptiness. The queue length of DC-AQM schemes is still frequently below the expected value (150 packets). IMC-PID regulates queue length around the expected value (150 packets) and obtains better control effect than other schemes.

# 6. Conclusion

In this paper, we proposed a congestion controller, called IMC-PID, to address the congestion control stability in large-delay networks. Existing AQM controllers yield unstable queue evolutions and result in low link utilizations and/or high delay jitters in networks with large communication delays. By adopting internal model control theory, the proposed IMC-PID controller is able to restrict the negative impact on queue stability caused by large delay. We conduct extensive simulations and comprehensively compare the performance of IMC-PID with previous works such as PI, REM, and DC-AQM. The results show that the IMC-PID outperforms others and maintains high link utilization as well as small queue deviation. As the controller parameters in this design are configured for particular networks, we are now generalizing IMC-PID so that it can be easily employed in real Internet. We can also extend this approach to the design of better Internet transport protocols combining with AQM to eliminate RTT bias and provide fair allocation of resources.

# References

[1] S. Floyd, V. Jacobson, Random early detection gateways for congestion avoidance, IEEE/ACM Transactions on Networking 1 (4) (1993) 397–413.   
[2] V. Misra, Wei-Bo Gong, Don Towsley. Fluid-based analysis of a network of AQM routers supporting TCP flows with an application to RED, in: Proceedings of ACM SIGCOMM, Stockholm, Sweden, August 2000, pp. 151–160.   
[3] F.P. Kelly, A. Maullo, D. Tan, Rate control for communication networks: Shadow prices, proportional fairness, and stability, Journal of the Operational Research Society 49 (1998) 237–252.   
[4] Srisankar Kunniyur, R. Srikant, End-to-end congestion control schemes: utility functions, random losses and ECN marks, IEEE/ ACM Transactions on Networking 11 (5) (2003) 689–702.   
[5] Yuping Tian, Stability analysis and design of the second-order congestion control for networks with heterogeneous delays, IEEE/ ACM Transactions on Networking 13 (5) (2005) 1082–1093.   
[6] Fernando Paganini, Zhikui Wang, John C. Doyle, Steven H. Low, Congestion control for high performance, stability, and fairness in general networks, IEEE/ACM Transactions on Networking 13 (1) (2005) 43–56.

[7] S. Athuraliya, S. Low, V. Li, REM: active queue management, IEEE Network Magazine 15 (2001) 48–53.   
[8] C. Hollot, V. Misra, D. Towsley, A control theoretic analysis of RED, in: Proceedings of IEEE INFOCOM, Anchorage, Alaska, April 2001, pp. 1510–1519.   
[9] C. Hollot, V. Misra, D. Towsley, On designing improved controllers for AQM routers supporting TCP flows, in: Proceedings of IEEE INFOCOM, Anchorage, Alaska, USA, April 2001, pp. 1726– 1734.   
[10] Jianxin Wang, Liang Rong. AOPC: an adaptive optimized proportional controller for AQM, in: Proceedings of IEEE ICPP, Columbus, Ohio, August 2006, pp. 164–174.   
[11] Fengyuan Ren, Chuang Lin, Bo Wei, Congestion control algorithm in large-delay networks, Computer Communications 27 (10) (2005) 485–493.   
[12] Carlos E. Garcia, Manfred Morari, Internal model control. 1. a unifying review and some new results, Industry and Engineering Chemical Process Design and Device 21 (1982) 308–323.   
[13] O.J.M. Smith, A controller to overcome dead time, ISA Journal 6 (2) (1959) 28–33.   
[14] Fengyuan Ren, Fubao Wang, Yong Ren, PID controller for active queue management, Journal of Electronics and Information Technology China 25 (1) (2003).   
[15] D. Agrawal, N.L. Da Fonseca, F. Granelli, Integrated ARM/AQM Mechanisms Based on PID Controllers, in: Proceedings of IEEE ICC, Seoul, Korea, May 2005, pp. 16–20.   
[16] R. Johari, D.K.H. Tan, End-to-end congestion control for the internet: delays and stability, IEEE/ACM Transactions on Networking 9 (6) (2001) 818–832.   
[17] Y. Zhang, S.-R. Kang, D. Loguinov, Delayed stability and performance of distributed congestion control, in: Proceedings of ACM SIGCOMM, Portland, Oregon, USA, August 2004.   
[18] UCN/LBL/VINT. Network simulator-ns2, http://www-mash.cs. berkeley.edu/ns.   
[19] J. Padhye, V. Firoiu, D. Towsley, J. Krusoe, Modeling TCP throughput: a simple model and its empirical validation, in: Proceedings of ACM SIGCOMM, Vancouver, August 1998, pp. 304–314.   
[20] H. Jiang, C. Dovrolis, Passive estimation of TCP round-trip times, ACM Computer Communications Review 32 (3) (2001) 75–88.   
[21] S. Shakkottai, R. Srikant, N. Brownlee, A. Broido, The RTT distribution of TCP flows in the Internet and its impact on TCP-based flow control, 2004, http://www.caida.org/outreach/papers/2004/tr-2004-02/tr-2004-02.pdf.