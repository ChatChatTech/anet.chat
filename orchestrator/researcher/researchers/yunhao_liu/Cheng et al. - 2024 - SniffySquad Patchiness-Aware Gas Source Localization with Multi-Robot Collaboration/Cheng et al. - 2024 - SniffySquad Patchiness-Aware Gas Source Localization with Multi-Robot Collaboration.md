# SniffySquad: Patchiness-Aware Gas Source Localization with Multi-Robot Collaboration

Yuhan Cheng∗, Xuecheng Chen∗, Yixuan Yang, Haoyang Wang, Jingao Xu, Chaopeng Hong, Xiao-Ping Zhang, Yunhao Liu, Xinlei Chen

Abstract—Gas source localization is pivotal for the rapid mitigation of gas leakage disasters, where mobile robots emerge as a promising solution. However, existing methods predominantly schedule robots’ movements based on reactive stimuli or simplified gas plume models. These approaches typically excel in idealized, simulated environments but fall short in real-world gas environments characterized by their patchy distribution. In this work, we introduce SniffySquad, a multi-robot olfactionbased system designed to address the inherent patchiness in gas source localization. SniffySquad incorporates a patchinessaware active sensing approach that enhances the quality of data collection and estimation. Moreover, it features an innovative collaborative role adaptation strategy to boost the efficiency of source-seeking endeavors. Extensive evaluations demonstrate that our system achieves an increase in the success rate by 20%+ and an improvement in path efficiency by 30%+, outperforming state-of-the-art gas source localization solutions.

Index Terms—gas source localization, mobile robot olfaction, collaborative robots, role adaptation

# I. INTRODUCTION

Rapid and accurate responses to gas leak incidents are essential for safeguarding human and environmental health, as leaked gases can rapidly create highly flammable or toxic conditions, posing significant risks of explosions and poisoning [1]–[3]. For instance, in the United States alone, 2,600 gas leakage incidents have been reported, with 328 resulting in explosions and 122 fatalities [4]. A key aspect of quick response requires localizing the gas source, which involves analyzing the concentration and distribution of the gas in the air to trace it back to its origin. With the knowledge

Manuscript submitted November 2024. (Corresponding author: Xinlei Chen.)

∗ indicates equal contribution.

Yuhan Cheng, Xuecheng Chen, and Haoyang Wang are with Shenzhen International Graduate School, Tsinghua University, Shenzhen, China (email: {cyh22, chenxc21, haoyang-22}@mails.tsinghua.edu.cn).

Yixuan Yang is with Electrical and Computer Engineering, Duke University, Durham, North Carolina, United States (email: yixuan.yang@duke.edu).

Jingao Xu is with School of Software, Tsinghua University, Beijing, China (email: xujingao13@gmail.com).

Chaopeng Hong is with Tsinghua Shenzhen International Graduate School, Tsinghua University, Shenzhen, China (email: hongcp@sz.tsinghua.edu.cn).

Xiao-Ping Zhang is with Shenzhen International Graduate School, Tsinghua University, Shenzhen, China, and also with RIOS Lab, Shenzhen, China (email: xpzhang@ieee.org).

Yunhao Liu is with Global Innovation Exchange, Tsinghua University, Beijing, China, and also with the Department of Automation, Tsinghua University, Beijing, China (email: yunhao@tsinghua.edu.cn).

Xinlei Chen is with Shenzhen International Graduate School, Tsinghua University, Shenzhen, China, and also with Pengcheng Laboratory, Shenzhen, Guangdong China, and RIOS Lab, Shenzhen, Guangdong, China (e-mail: chen.xinlei@sz.tsinghua.edu.cn).

![](images/daef3a155ef1fd44da97f55fe46ca62e2c446ff3c5e2a5e7502edd44955ae597.jpg)



![](images/d02c59de4ff9175f707219e26c3eba0a46863465aa675d2e6e9200863bc77b55.jpg)



Fig. 1. Mobile olfactory robots autonomously search for and navigate towards the source of gas leakage.

of source locations, subsequent mitigation operations, such as shutting off valves or sealing the leaks, can be conducted more logically, efficiently, and safely [5].

Conventional gas source localization (GSL) solutions fall into two categories: (i) human expert-based solutions assign human operators to engage in affected areas. These laborious and perilous activities not only increase the risk of misinterpretation but also imperil the safety of the operators [6]; and (ii) wireless sensor network (WSN)-based methods utilize preinstalled static sensors to detect the gas source by monitoring gas concentration readings [7]. However, this approach is constrained by spatial resolution limitations, particularly in environments with extensive and intricate pipeline networks that present numerous potential leakage points.

In this work, we aim to devise an effective strategy for collaboratively scheduling multiple olfactory robots to localize the gas source in real-world environments. Particularly, we utilize multiple robot’s activeness and collaborative capability to gather more information efficiently, enhancing the synergy between their sensing and scheduling abilities.

We take gas leakage in a factory with intricate pipelines as an example scenario, as shown in Fig. 1. Here, a fleet of robots equipped with gas concentration sensors and wind sensors are dispatched to search the surroundings and gather gas sensory data. By analyzing and interpreting the environmental conditions, the robots autonomously navigate to pinpoint the source of the gas leakage. However, translating this idea into a practical system is non-trivial and faces two challenges:

• The patchy nature of gas plumes confuses and traps the robots. The gas landscape is characterized by a patchy structure [8], [9], as evidenced by field measurements of gas concentration (see Fig. 2). As seen, gas plumes fragment into disjointed patches and form distinct and scattered areas. From the perspective of source-seeking robots, the concentration measured along the horizontal centerline exhibits pronounced fluctuations as the distance to the source increases, since gas patches are separated by regions where gas concentration is below detectable levels. This intermittent characteristic introduces uncertainty in determining the source direction when robots devise paths using noisy and local sensory data, ultimately leading to their entrapment within these patches and failure to complete GSL. Existing solutions, including bio-inspired [10], [11] and probabilistic model-based approaches [12], [13], either rely on local gas concentration gradient or oversimplified gas dispersion models, rendering them effective only in idealized scenarios with continuous gas concentration fields.

• Trade-off between source localization effectiveness and search efficiency for collaborative robots. Since gas distribution varies continuously over space and time, it is impossible to measure at every possible location all the time. Therefore, robots must strike a balance between two conflicting objectives within limited sampling: (i) identifying new potential gas source positions and (ii) excluding false positive source positions. Achieving these goals simultaneously complicates the localization of the true gas source efficiently and effectively. Specifically, the former goal necessitates extensive exploration and sampling of gas data, while the latter goal requires utilizing previously acquired information to reach and verify the estimated source position’s probability. Current multi-robot GSL solutions tend to exhibit either clustered or dispersed collaborative behaviors, thereby undermining the simultaneous achievement of both objectives [11], [14], [15].

Remark. As far as we are aware, previous works develop their operating principles ignoring the patchy nature of gas plumes, based on which they schedule agents without fully harnessing their versatility and collaborative capabilities at a system level.

To tackle the above challenge, we design and implement SniffySquad, a collaborative olfactory robot scheduling system for gas source localization. Benefiting from SniffySquad, a team of olfactory robots can adapt to field patchiness and dynamically adjust their movements accordingly, enabling efficient and effective emission source localization. In general, SniffySquad excels in the following two aspects.

• At the individual level, we propose a Patchiness-aware active sensing method, which refines the probabilistic source estimation by incorporating the patchy characteristic of gas in each robot’s moving strategy. Inspired by the principles of Langevin MCMC [16], we adjust robots’ gradient-based moving direction with a regulation term, allowing them to escape false positive source positions and thereby collect more informative sensing data.

• At the team level, we design a Potential-instructed collaborative roles adaptation strategy that further enhances the source-seeking efficiency by adjusting robots’ roles based on their spatial distribution and measurements in the past. Each robot in the team adopts either a fine-grained search role to

![](images/e7bfa1cc3dba4cc546d84722a74c778ae2d581a214376276363e448372f77383.jpg)



Fig. 2. Spatial characteristics of gas concentration. We conducted a proofof-concept experiment to check gas characteristics in our indoor testbed, with a gas emission device at $( x , y ) = ( 1 . 0 , 0 . 0 )$ and winds blowing along the x axis. The heatmap illustrates concentration values, representing the number of particles with a diameter >0.3um in 0.1L of air. The observed gas plume patches may mislead source-seeking robots into falsely identifying them as the actual gas emission source.

inspect spurious signals (i.e., exploiter) or a coarse-grained search role to discover potential new sources (i.e., explorer). These roles are adaptively adjusted based on the estimated probabilities of each robot’s proximity to the emission source, thereby parallelizing the exploration of the environment and exploitation of collected information in a flexible manner.

We evaluate the performance of SniffySquad and compare it with state-of-the-art baseline methods through experiments on a real-time multi-robot testbed (12 hours) and extensive physical feature-based simulations (750 runs). Experiment results show that our system outperforms all baselines, achieving a 20%+ success rate improvement and improving path efficiency by > 30%.

We summarize the contributions of this paper as follows:

• We propose SniffySquad, a collaborative multi-robot olfactory sensing system for accurate and efficient gas source localization, specifically designed to handle the patchy characteristics in real-world gas fields.   
• We introduce a patchiness-aware active sensing method that refines probabilistic source estimation by incorporating gas patchiness in each robot’s moving strategy. Building on this design, we further devise a potential-instructed collaborative roles adaptation strategy, which parallelizes the exploration of the environment and exploitation of collected information in an adaptive manner.   
• We develop a prototype system and evaluate SniffySquad through a real-world testbed and a physical-feature-based gas dispersion simulator. Extensive evaluation results show its effectiveness and superior performance.

The remainder of the paper is organized as follows. We first introduce the background, motivation, and related works in Section II. In Section III, we present preliminaries, followed by the system overview in Section IV. In Sections V and VI, we introduce the algorithm design, involving detailed descriptions of the patchiness-aware active sensing and potential-instructed collaborative roles adaptation. Section VII showcases the implementation and evaluation. Finally, Section VIII concludes the paper.

# II. BACKGROUND AND RELATED WORK

# A. Characteristics of Gas Concentration Distribution

Spatial characteristics of gas concentration in real-world are depicted in Fig. 2. The data are measured in our testbed, which will be introduced in Section VII-A. Fig. 2 shows that gas distribution exhibits patchiness, which is caused by turbulent atmosphere stretching and fragmenting plumes into disjointed patches spatially [8]. This characteristic may mislead sourceseeking robots into falsely identifying them as the actual gas emission source.

Note that characteristics of gas concentration distribution described by models commonly used in previous gas source localization (GSL) works differ significantly from those observed in practical environments. We first introduce the model that existing work relies on. To model the concentration of a substance flowing in a fluid, the transportation process is typically adopted, which is described by the partial differential convection-diffusion equation $\begin{array} { r } { \frac { \partial c } { \partial t } = \nabla \cdot \mathbf { u } c - \nabla \cdot \Gamma \nabla c + S } \end{array}$ . Here scalar c is the gas concentration, u is the velocity vector (u, v, w), ∇ and ∇· represents the gradient and the divergence of the c, and S is the source of a scalar. While this equation can be employed for numerical simulation in computational fluid dynamics (CFD), as highlighted in the preceding section, probabilistic gas source localization approaches necessitate an analytical model rather than a transportation process for numerical simulation. To this end, previous works [14], [17] solve a simplified transportation equation by assuming steadystate conditions and assuming no degradation, yielding the Gaussian plume model [18].

However, this oversimplified model can only be used to model gas concentration landscapes at microscopic scales, where molecular diffusion generates smooth changes in concentrations of chemicals [10]. In contrast, as shown in Fig. 2, at distances on the order of meters or larger, gas plumes are significantly dispersed, resulting in patchy and discontinuous plumes as macroscopic scales.

# B. Mobile Robot Olfaction-based Gas Source Localization

Current approaches can be categorized into two classes, which will be introduced first, reactive bio-inspired and probabilistic algorithms. Then multi-robot gas source localization methods are summarized, introducing how collaboration is incorporated.

1) Reactive bio-inspired GSL: Bio-inspired algorithms draw inspiration from the behavior of insects or rodents. They involve chemotaxis, anemotaxis, or combining both [10]. For chemotaxis, such strategies have the robot turn to the opposite direction if it experiences a declining odor concentration gradient along its trajectory. Chemotaxis fails when odor trails are broken, olfactory stimuli are sporadic, and consequently gradients are absent. Anemotaxis-driven navigation can be divided into surge (the robot moves upwind), casting, spiral, and zigzagging [11]. For casting, a robot in the plume moves upwind until it loses the plume, then it turns and moves crosswind until it hits odor packets again. When a robot loses the plume, it moves along a spiral or zig-zag to reacquire the plume. Bio-inspired methods are reactive in nature, making them susceptible to intermittent gas concentration signals caused by spurious gas patches.

2) Probabilistic gas source localization methods: According to models used for the environment’s representation, probabilistic gas source localization methods can be categorized into parametric and non-parametric algorithms [12].

• Parametric algorithms, which rely on an atmospheric transport and diffusion (ATD) model mapping each point in the environment to the expected gas concentration there, assume a finite set of parameters. In the context of GSL, the set of parameters is called source term, involving a combination of the position of the source, the release rate, the downwind direction and velocity, and 3-dimensional diffusion terms in different directions (x, y, and z). Prevalent plume models include the isotropic plume model [19] and the Gaussian plume model [20].

• Non-parametric algorithms. They model the spatial distribution of the gas plume rather than focus on terms parameterizing the gas source, thus can not be defined in terms of a finite set of parameters. These algorithms originate from the problem of gas distribution mapping (GDM). Popular algorithms include Kernel DM+V [21] (and its variants) and Gaussian Markov random fields (GMRF) based spatial modeling [13], [22].

Parametric methods are mostly computationally efficient and exhibit simple analytical forms. The simplicity of the plume model, on the other hand, ignores the stochasticity of gas emissions and the spatial nonuniformity of wind fields. It renders this type of algorithms idealistic. Moreover, these methods fail under the existence of multiple sources or the inclusion of walls and obstacles. The latter fact restrains the methods’ applicability to indoor places, such as factories. In contrast, non-parametric algorithms make less assumptions about the atmospheric environment and the gas source characteristics, hence are much more flexible to be applied in various scenerios. However, without much prior knowledge embedded in non-parametric algorithms, inference at areas that are previously unvisited are typically inaccurate. Moreover, the extensive parameter space poses computational challenges.

According to planning strategies used to seek the source, probabilistic GSL methods can be categorized into gradientbased and information-based algorithms.

• Gradient-based probabilistic GSL planners resemble the idea of chemotaxis but differ from it in the way they compute gradients. In chemotaxis, robots utilize merely measurements along its trajectory to identify whether the concentration is rising or declining. In probabilistic GSL algorithms, robots can leverage the probability model to calculate the direction, either analytically or numerically. For example in [23], particle filter biased random walk (BRW) modifies BRW [24] to utilize an analytical gradient computed from source term estimation results based on the Gaussian plume model.   
• Information-based GSL planners select actions to maximize the expected information gain (i.e., the uncertainty reduction). The algorithm can be implemented by optimizing upper confidence bound (UCB) [25], entropy such as mutual information [26], or Fisher information [27].

# C. Cooperative Gas Source Localization methods

An apparent way of increasing GSL efficiency and accuracy is by utilizing multiple robots as a team. Some directly extend single robot gas source localization algorithms by spanning the action space. Other methods, tailored for cooperative GSL, are listed here. (i) Particle Swarm Optimization (PSO)-based algorithms [15] are inspired by the bird flock searching for food. If an agent discovers a better pattern (potential food source), others adjust their movements to follow it. When robot teams adopt this strategy for GSL, they will have a tendency to move towards the same local optimium and are considered to lack cooperation [11]. (ii) Another type of approach [14] achieves cooperation by dispatching robots to investigate several likely source positions separately, so that they can either be ruled out or considered more thoroughly.

In summary, these multi-robot gas source localization methods induce either gathering or scattering behavior, so they lack efficiency in achieving both goals. Technically, each individual in the team acts similarly and are not assigned heterogeneous roles. In contrast, our work empowers team members to adopt different but complementary roles, enhancing individual diversity and overall synergy. This distinction highlights the advantage of a more strategic and versatile approach to team coordination.

# III. PRELIMINARIES

# A. Definitions

We denote gas source position and robot’s position at time t as $x _ { s }$ and $x ^ { ( i ) } ( t )$ , respectively. The total time spent for gas source localization is represented by final time step $t _ { f } .$ . The trajectory of a robot and its corresponding sensory measurements are denoted by $\mathbf { z } _ { 1 : t }$ and $\mathbf { x } _ { 1 : t }$ .

We express measurements at position x as $z ( x )$ . We denote measurement data as $z = ( z ^ { c } , z ^ { w } )$ , where gas concentration and airflow direction are denoted by c and $\mathbf { u } ~ = ~ ( u , v , w )$ , respectively. The system is only accessible to a belief $b ( t )$ incorporating sensory measurements $\mathbf { z } _ { \mathrm { 1 : } }$ :t along past trajectories $\mathbf { x } _ { 1 : t }$ due to partial observability. It follows the Bayesian estimation framework by continually updating the likelihood of each position being situated within the gas plume region based on incoming measurements z gathered from sensors equipped on the mobile robots. Mathematically, $p ( x | z _ { 1 : t } ) \propto$ $p ( x | z _ { 1 : t - 1 } ) p ( z _ { t } | x , z _ { 1 : t - 1 } )$ .

Important symbols used in the paper are listed in Table I.

# B. Problem Formulation

The goal of SniffySquad is to minimize the search time, defined as the duration from departure to a robot reaching the vicinity of a gas source. A search trial terminates when a robot’s position is within a predefined threshold of the gas source or the predefined time limit is reached. Mathematically, a successful search indicates that $\exists i \in \{ 1 , 2 , \ldots , M \}$ s.t. $\| x ^ { ( i ) } ( t _ { f } ) - x _ { s } \| ~ \le ~ d _ { \varepsilon }$ , where $d _ { \varepsilon }$ is the distance threshold. Therefore, the system objective can be formulated as:

$$
\begin{array}{l} \min _ {\mathbf {x} (t), \mathbf {u} (t)} t _ {f} \\ \begin{array}{l l} \text { s.t. } & b (t) = b e l (\mathbf {z} _ {1: t}, \mathbf {x} _ {1: t}), \end{array} \\ u ^ {(i)} (t) = g \left(x ^ {(i)} (t), x ^ {(- i)} (t), b (t)\right), \tag {1} \\ \dot {x} ^ {(i)} = f (x ^ {(i)}, u ^ {(i)}), \\ \mathbf {x} (t _ {0}) = \mathbf {x} _ {0}, \mathbf {x} (t _ {f}) = \mathbf {x} _ {f}, \\ x \in \mathcal {X}, u \in \mathcal {U}, t _ {f} > 0, \\ \end{array}
$$

The global gas source estimator is represented as $b e l ( \cdot )$ . The collaborative planner is denoted as $g ( \cdot )$ , which determines the movements of robot $i , u ^ { ( i ) } ( t )$ , according to the estimation results $b ( t )$ , its own position $\mathrm { c } ^ { ( i ) } ( t )$ , and other robots’ positions $x ^ { ( - i ) } ( t )$ . The control logic is denoted as $f ( \cdot )$ , describing the dynamics of specific robots.

# IV. SYSTEM OVERVIEW

In this part we describe the system model and interactions between various components. The design objective of our system is to schedule a team of autonomous mobile robots equipped with gas concentration sensors for gas source localization in atmospheric turbulence, achieving rapid and robust navigation towards the source of leakage. In this work, the system interacting with the underlying physical world is composed of M mobile robot nodes and an edge server. An overview of the system is shown in Fig. 3.

• On the Mobile layer, the mobile robot node consists of taskspecific sensors in the olfactory system, infrastructure for selflocalization (e.g., radio or visual sensors), and a patchinessaware active sensing module. First, it features task-specific sensors for the olfactory system, including a gas sensor to measure gas concentration and an anemometer to measure airflow direction. Second, the localization infrastructure utilizes an attached UWB tag to determine the robot’s position by measuring distances to pre-deployed UWB anchors. Finally, the patchiness-aware active sensing module (§V) takes highlevel plans (coordination) from the edge server as input, then outputs low-level control commands executed by motors.

• On the Edge layer, The edge server serves as the platform coordinating the robot team by maintaining a environmental map, estimating the gas source, and adapting team roles collaboratively. First, it maintains a global probability map associating each grid in the environment map with the probability of ’the gas source locates at that position’. The edge server fuses local measurements, including gas, wind, and location data, and continually updates the likelihood of each position being situated within the gas plume region based on incoming measurements. Second, the potential-instructed collaborative roles adaptation module (§VI) coordinate all robots’ behaviors and dispatches motion plans to mobile robot nodes.

Workflow. To summarize, robots in the system first take sensory measurements as inputs, including the gas concentration, wind speed and direction. The onboard measurements are filtered to update the probabilistic gas source estimation.

![](images/63f5f3c878358dc988498d8fa718b7563f1df8e429aa223fbfb0dc5a8f986679.jpg)



Fig. 3. System overview.

TABLE I LIST OF IMPORTANT NOTATIONS USED IN THE PAPER 

<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $M$ </td><td>Total number of robots</td></tr><tr><td> $x(t) \in \mathcal{X}$ </td><td>Position coordinates at time  $t$ </td></tr><tr><td> $\mathbf{x}$ </td><td>Positions of all  $M$  robots =  $[x^{(1)}, x^{(2)}, \ldots, x^{(M)}]^{T}$ </td></tr><tr><td> $x_{s}$ </td><td>Gas source position</td></tr><tr><td> $c$ </td><td>Gas concentration</td></tr><tr><td> $\mathbf{u}$ </td><td>Wind velocity vector =  $(u, v, w)$ </td></tr><tr><td> $z \in \mathcal{Z}$ </td><td>Sensory measurement collected from mobile robot nodes (consisting of gas concentration  $z^{c}$  and the wind vector  $z^{w}$ ) =  $(z^{c}, z^{w})$ </td></tr><tr><td> $t_{f}, t_{0}$ </td><td>Time of task termination and departure</td></tr><tr><td> $U(x)$ </td><td>Neighborhood of position  $x$ </td></tr><tr><td> $p(x)$ </td><td>Probability of the gas source being located at  $x$ </td></tr><tr><td> $\Phi : \mathcal{X} \to \mathbb{R}$ </td><td>Potential function</td></tr><tr><td> $\tau, \tau$ </td><td>Temperature parameter in Langevin diffusion; Temperatures of all  $M$  robots =  $[ \tau^{(1)}, \tau^{(2)}, \ldots, \tau^{(M)} ]^{T}$ </td></tr><tr><td> $a, s(i, j)$ </td><td>Swapping rate (i.e., role-exchange probability) between robot  $i$  and robot  $j$ </td></tr><tr><td> $\mu, \sigma$ </td><td>Deterministic and stochastic terms in the generic stochastic differential equation</td></tr><tr><td> $dB, \xi$ </td><td>Brownian motion in continuous and discrete time space</td></tr><tr><td> $\eta, h$ </td><td>Temporal and spatial discretization granularity</td></tr><tr><td> $\pi(\cdot)$ </td><td>Invariant distribution of MCMC sampling</td></tr></table>

Thereafter, based on the up-to-date potential function and current positions of robots in the team, the robots’ roles are reconfigured systematically if their potential of locating at the source mismatches with their roles. Finally, the robots choose their sensing directions according to the patchinessaware active sensing module. Subsequent contents delve into details of these components.

# V. PATCHINESS-AWARE ACTIVE SENSING

To tackle the patchy nature of gas plumes, we design a patchiness-aware active sensing method for individual robots to enable resilient gas source localization. The strategy is inspired by Markov chain Monte Carlo (MCMC) sampling based nonconvex learning. In this section, we first recast the GSL problem to MCMC sampling (Section V-A), then we describe the algorithm design that is tailored for olfactory mobile robots sensing actively in realistic plumes (Section V-B). At last, we introduce the probabilistic gas source estimation method, which constitutes sampling’s target distribution (Section V-C). Fig. 4 illustrates the workflow of the latter two sections.

# A. Recast GSL to MCMC Sampling

In this part, we first introduce a surrogate optimization via which the problem formulated in Eq. (1) can be solved. Regarding the patchy nature of gas plumes, the surrogate optimization is then reframed as MCMC sampling. At last, we describe the Langevin MCMC, based on which we design our algorithm tailored for mobile olfactory robots.

1) Surrogate optimization: Our task, gas source localization, involves identifying a position with the highest probability of locating the source of a gas emission. From this perspective, the objective of Eq. (1) can be realized by optimizing the likelihood of being the source location, with respect to position x. An efficient optimizing procedure leads to an efficient source seeking algorithm.

Specifically, instead of minimizing the terminating time $t _ { f }$ directly, we can optimize a surrogate function $\Phi ( { \boldsymbol { x } } ) : { \boldsymbol { \chi } }  \bar { \mathbb { R } } ,$ which assesses the likelihood of position x being the source location (position x with a small value of $\Phi ( x )$ has a high probability of being the source of gas leakage). Thus, the core task can be reinterpreted, leading to the formulation:

$$
\min _ {x \in \mathcal {X}} \Phi (x). \tag {2}
$$

We describe the probabilistic estimator and the design of potential $\Phi ( x )$ in Section V-C.

2) Optimization via sampling: In the context of GSL, however, the optimization task presents notable challenges attributable to two factors. First, the potential function exhibits multimodal characteristics and is far from convex due to the patchy gas plume. Second, the potential function available is noisy and stochastic [28]. Specifically, the robots rely on measurements obtained from onboard sensors, which are susceptible to noise and provide partial observations. Consequently, conventional algorithms suitable for convex objectives and methods taking deterministic movements can be trapped and/or misled.

To deal with the challenges posed by the nonconvex and stochastic nature of the potential function, reframing the optimization problem to an Markov chain Monte Carlo (MCMC) sampling problem [29] is one promising approach. Monte Carlo sampling has been shown to be a powerful method for nonconvex and multimodal optimization [16], [30], [31], as well as noises and randomness in the potential function [28]. Specifically, sampling can be faster than optimization for some nonconvex objectives [30]. Moreover, for noisy objectives whose randomness might arise from inherent function noise, MCMC sampling algorithms can be efficient by injecting the right amount of noise into each iterative update step, providing a means of coping with inherent noise. For instance, stochastic gradient descent methods [28] are designed to cope with such randomness.

A key step in MCMC sampling is constructing a Markov chain that has the desired probability distribution $\pi ( x )$ as its equilibrium distribution. Under this condition, one can draw samples from the intended distribution by recording states from the chain. Specifically, convergence to equilibrium means that the Markov chain ’forgets’ about its initial state and the sequence of states after convergence to distribution π(x).

![](images/f23c0baff376a1c8a7ee41812047efe0d9c7ef1c8b773e3fa56b8effce40e405.jpg)



Fig. 4. Illustration of the algorithm.

3) Langevin diffusion: To translate MCMC sampling methods to robot movement algorithms, we design the strategy based on Langevin diffusion MCMC. Now, we first introduce the generic diffusion MCMC, then introduce the Langevin diffusion.

Diffusioin MCMC sampling methods simulates a Markov chain using diffusion processes, a concept from statistical physics describing the movement of particles. A diffusion process is defined by a stochastic differential equation (SDE), whose general form can be expressed as:

$$
d x (t) = \mu (x (t)) d t + \sigma (x (t)) d B (t), \tag {3}
$$

where $x ( t )$ is the positions of the particle. This SDE consists of a deterministic drift term $\mu ( x ( t ) )$ and a stochastic term, which is proportional to the standard Brownian motion $d B ( t )$ and scaled by a factor $\sigma ( \boldsymbol { x } ( t ) )$ . The standard Brownian motion $\{ B ( t ) \} _ { t \geq 0 }$ is a stochastic process with properties (i) movement during any time interval $( s , t ) ( s < t ) , B ( t - s ) \doteq B ( t ) - B ( s )$ is a normal random variable, i.e., $B ( t - s ) \sim \mathcal { N } ( 0 , t - s )$ , and (ii) the increments of different time intervals are independent.

The Langevin dynamic, with respect to the potential function $\Phi ( x )$ , is a diffusion process exhibiting equilibrium behaviour. It is given by a stochastic differential equation:

$$
d x (t) = - \nabla \Phi (x (t)) d t + \sqrt {2 \tau} d B (t), \tag {4}
$$

where $\nabla \Phi ( { \boldsymbol x } ( t ) )$ is the gradient of the potential function at position $x ( t ) , \{ B ( t ) \} _ { t \geq 0 }$ is a standard Brownian motion and $\tau > 0$ is a parameter called temperature in statistical physics and thermodynamics. Notably, Eq. (4) is the stochastic version of gradient descent, differing in the incorporation of noise term, which is Gaussian with zero mean and a covariance determined by the temporal duration of the movement.

This random process $\{ x ( t ) \} _ { t \geq 0 }$ defined in Eq. (4) has a unique invariant distribution (a.k.a. the Boltzmann-Gibbs distribution) with density

$$
\pi_ {\tau} (x) = \frac {e ^ {- \Phi (x) / \tau}}{\int_ {\mathcal {X}} e ^ {- \Phi (x) / \tau} d x} = \frac {1}{Q} e ^ {- \Phi (x) / \tau}. \tag {5}
$$

Here the denominator Q is the normalization constant. With any initial distribution of $x ( t )$ , the limiting distribution of $X _ { t }$ converges to $\pi _ { \tau } ( x )$ by running the diffusion process. In other words, our solution is always expected to fall into the neighborhood of a global minimum of Φ(x) with high probability.

# B. Langevin Dynamics-driven Active Sensing Strategy

In this part, we describe the novel active sensing strategy for GSL with resiliency to patchy gas plume caused by atmospheric turbulence and noisy partial observations from robots.

As illuminated in the previous section, gas source search and localization can be recast to drawing samples from $\pi ( x ) = e ^ { - k \Phi ( x ) }$ , so that random samples drawn from $\pi ( x )$ are attracted to the peak in the distribution $\pi ( x )$ , i.e., the global minimum of $\Phi ( x )$ . This relationship is exemplified when $\pi ( x ) = \delta ( x ^ { * } )$ , where $x ^ { * } =$ arg min Φ(x), as $k  + \infty$ . In particular, the Dirac delta equilibrium distribution concentrates at $x ^ { * }$ (the global minimum of $\Phi ( x )$ and hence the position with the maximum likelihood of locating the source) and the chain ’forgets’ about initial position of the mobile robot.

We aim to develop an active sensing strategy for sourceseeking robots driven by Langevin dynamics. However, there is a gap between an algorithm tailored for robots and MCMC sampling due to the difference between particle dynamics and the mobile robots’ motion characteristics. Langevin diffusion is developed to describe the motion of particles (or the update of parameters of machine learning models) by defining a continuous-time stochastic process, thus Langevin MCMC can not be directly applied. To establish strategy suitable for robots determining their sensing direction, we first discretize the diffusion process and subsequently generate a sequence of positions for mobile robots to follow.

In the first step, we attain a discrete-time algorithm through the Finite Difference Method [32]. In detail, we first discretize the states over time from $\{ x ( t ) \} _ { t \in \mathbb { R } ^ { + } } \ \mathrm { t o } \ \left\{ x _ { k } \right\} _ { k \in \mathbb { Z } ^ { + } }$ , where $x _ { k } ~ = ~ x ( k \cdot \delta t )$ , and δt represents the discretization time step size. Then we apply the explicit, forward-time Euler scheme for temporal discretization, leading to the following formulation of the discrete stochastic differential equation:

$$
x _ {k + 1} = x _ {k} - \eta \cdot \nabla \Phi (x _ {k}) + \sqrt {2 \eta \tau} \cdot \xi_ {k}. \tag {6}
$$

Here the stepsize $\eta ~ > ~ 0$ is proportional to the temporal discretization granularity δt, τ is the temperature parameter, and $\{ \xi _ { k } \} _ { k \in \mathbb { Z } ^ { + } }$ signifies a sequence of standard normal random vectors. Eq. (6) describes how the robot’s sensing direction evolves overtime while incorporating randomness.

In the above equation, it requires calculating the gradient of the potential function at position x to generate a sequence of trajectory points. However, the function we designed in Section V-C is discrete and not differentiable. To address this, we adopt the central-difference approximation for spatial discretization:

$$
\nabla \Phi (x) \approx \left[ \frac {\Phi (x + h , y) - \Phi (x - h , y)}{2 h}, \quad \frac {\Phi (x , y + h) - \Phi (x , y - h)}{2 h} \right] ^ {T}.
$$

Additionally, following gradients might force the robot jump between distant positions when the slope of the potential function at current position is substantial. For robots’ path scheduling, we constrain the drift term to be below the robot’s maximal velocity.

# C. Probabilistic Gas Source Estimation

With the reframing of the GSL task as an MCMC sampling problem, a definition of the potential function $\Phi ( x )$ , as stated in Eq. (2) and in equilibrium distribution Eq. (5), is required. For every position $x \in \mathcal { X }$ in the environment, we estimate the probability that x is located within the gas plume region. This probability estimation is denoted as $p ( x )$ , and subsequently, we define the potential function as: $\Phi ( x ) \doteq - l o g ( p ( x ) )$ .

To obtain $p ( x )$ we employ a Bayesian estimation methodology, placing our method within the class of probabilistic GSL algorithms. Specifically, this estimator continually updates the likelihood of each position being situated within the gas plume region based on incoming measurements z gathered from sensors equipped on the mobile robots. Mathematically, $p ( x | z _ { 1 : t } ) \propto p ( x | z _ { 1 : t - 1 } ) p ( z _ { t } | x , z _ { 1 : t - 1 } )$ . In our scenario, the measurements $\boldsymbol { z } = ( z ^ { c } , z ^ { w } ) \in \mathcal { Z } = \mathbb { R } \times \mathbb { R } ^ { d }$ collected from the mobile robots consists of the gas concentration $z ^ { c }$ and the wind vector $z ^ { w }$ , acquired by chemical sensor and wind sensors (anemometers) respectively. To accommodate environments of arbitrary geometries, the area is discretized into a grid of equally-sized cells.

The update procedure upon receiving new measurements is implemented based on [33], involving two sequential steps. (1) Local estimation generation. The first step follows two intuitive and empirical rules: a) if the robot detects gas, the likelihood of neighboring grids within the upwind direction to localize within the gas plume is increased; b) If gas concentration is negligible or falls below a predefined threshold, grids directing to the position with previously recorded nonzero gas readings are attributed a higher likelihood of hosting gas. (2) Global estimation propagation. The first step generates estimations solely for $x \in U ( x ( t ) )$ , where $U ( { \boldsymbol x } ( t ) )$ denotes the neighborhood region around the robot’s current position $x ( t )$ , For the remaining areas $\{ x \in \mathcal { X } \backslash U ( x ( t ) ) \}$ }, their probabilities are updated in the second step by propagating information from $U ( { \boldsymbol x } ( t ) )$ to the entire environment X based on [33], conforming to the geometry of the area.

# VI. POTENTIAL-INSTRUCTED COLLABORATIVE ROLES ADAPTATION

In this part, we present how to coordinate a team of collaborative robots to enhance source-seeking efficiency, utilizing both external environmental cues and internal team dynamics. This strategy consists of two tightly-coupled modules: Heterogeneous Roles Assignment and Team Roles Adaptation. We present our algorithm in Algorithm 1.

# A. Heterogeneous Roles Assignment

The scattered, patchy nature of gas plumes and the multimodal nature of concentration distribution map require an GSL system with two capabilities, (i) discovering new potential source positions and (ii) distinguishing existing candidate positions. This gives rise to a trade-off between “global exploration” and “local exploitation” of the environment. To attain the advantages of both behaviors, we assign robots in the team with heterogeneous roles, named explorer and exploiter respectively. Robots acting as the former role are mainly responsible for objective (i) while the latter focus on objective (ii).

Algorithm 1: SniffySquad.   
Input: Robots' initial positions $x^{(0)}$ Output: $d_{\varepsilon}$ -approximate gas emission source position
while $\forall i \in \{1, 2, \ldots, M\}$ , $\|x^{(i)}(t_f) - x_s\| \geq d_{\varepsilon}$ do
    Collect environmental sensory measurements $z = (z^c, z^w)$ ;
    Update belief $b(x)$ , and potential $\Phi(x)$ accordingly;
    CollaborativeRolesAdaptation();
    for $i$ in $\{1, 2, \ldots, M\}$ do
    Assign a role $\tau^{(i)}$ to robot $i$ ;
    Move robot $i$ following $x_{k+1}^{(i)} = x_k^{(i)} - \eta \cdot \nabla \Phi(x_k^{(i)}) + \sqrt{2\eta\tau^{(i)}} \cdot \xi_k$ ;
    if $d(x_{k+1}^{(i)}, x_s) < d_{\varepsilon}$ then return;
    end
end

Function CollaborativeRolesAdaptation()
    for $i, j$ in $\{1, 2, \ldots, M\}$ do
    Calculate swapping rate $s(i, j) = a \cdot \exp(\min(0, (\frac{1}{\tau^{(i)}} - \frac{1}{\tau^{(j)}}) \cdot (\Phi(x^{(i)}) - \Phi(x^{(j)})))$ ;
    if random() $\leq s(i, j)$ then
    Robot $i$ and $j$ swap their roles (i.e., temperatures $\tau^{(i)}$ and $\tau^{(j)}$ );
    end
end

Considering this, we assign different roles to robots in a team. The role assignment can be implemented by regulating the temperature parameter τ in Eq. (4). Specifically, temperature τ in the motion dynamic plays a crucial part in regulating the behaviour of the robot. Robots assigned a low temperature carry out exploitative actions while those with high temperatures engage in exploratory actions. Mathematically, for a team with M robots, consider M Markov chains driven by Langevin diffusions:

$$
\mathrm{d} x ^ {(i)} (t) = - \nabla \Phi (x ^ {(i)} (t)) \mathrm{d} t + \sqrt {2 \tau^ {(i)} (t)} \mathrm{d} B ^ {(i)} (t), \tag {7}
$$

where $i \in \{ 1 , 2 , \ldots , M \}$ . The role of robot i is specified by its temperature $\tau ^ { ( i ) } ( t )$ , which governs the extent of exploring potential gas source positions and exploiting local information to distinguish spurious gas patches. When a robot is assigned a low temperature, its motion is governed by the gradient of the potential function, the robot tends to exploit the local information of the surrounding potential field. For a robot with a higher temperature, more randomness is injected into the motion, causing it to explore the environment more actively.

The role division module, following $\mathrm { E q . } \ ( 7 )$ , have a guarantee that robots are expected to concentrate around the global minima of the potential function $\Phi ( x )$ . Specifically, we denote the positions of M robots as $\mathbf { x } ~ = ~ \left\lceil x ^ { \top } \right\rceil , x ^ { ( 2 ) } , \bot \bot , x ^ { ( M ) } \Big \rceil ^ { T }$ , and their corresponding temperature parameters as $\begin{array} { r l } { \tau } & { { } = } \end{array}$ $\left[ \tau ^ { ( 1 ) } , \tau ^ { ( 2 ) } , \dots , \tau ^ { ( M ) } \right] ^ { T }$ . The invariant joint distribution [31] takes the form:

$$
\pi_ {\tau} (\mathbf {x}) \propto \exp \left(- \sum_ {i = 1} ^ {M} \frac {\Phi (x ^ {(i)})}{\tau^ {(i)}}\right). \tag {8}
$$

The marginal stationary distribution of the low temperature robot will be attracted to the peak of the potential function $\Phi ( x )$ .

# B. Team Roles Adaptation

This submodule adaptively adjusts team roles through role swapping, as illustrated in Fig. 4, based on the principles of replica exchange.

Optimizing the trade-off between localization effectiveness and search efficiency requires robots in the team to adjust their roles adaptively. One way to view this is through the lens of MCMC sampling. In Eq. (4), a high temperature fosters broader exploration across the global domain at the expense of reduced concentration around the minima, and vice versa. Therefore, the potential of using a fixed temperature is inherently limited. Alternatively, consider the gas source localization scenario. At an individual level, robots should exploit parsimoniously to avoid trapping in spurious patches and explore appropriately to escape from areas improbable to locate the source. From a team perspective, there should be some robots exploiting while others exploring.

In order to coordinate the team behavior systematically, we propose a role-swapping mechanism for team roles adaptation, incorporating replica exchange MCMC sampling [34]. When an exploiter i locates at a position that is less likely to correspond to the desired gas source compared to an explorer j, this pair of robots swaps their roles. Consequently, robot i transitions into an explorer so that it can turn to more promising areas and save time, while robot j transforms into an exploiter who slows down and focuses to avoid missing the source of interest.

Formally, this is achieved by swapping the temperatures between robots exhibiting different potential. Specifically, we consider a pair of random processes, denoted as robot i and $j ,$ from the set of M Langevin diffusions. The two robots swap temperatures with probability:

$$
s (i, j) = a \cdot \exp (\min (0, (\frac {1}{\tau^ {(i)}} - \frac {1}{\tau^ {(j)}}) \cdot (\Phi (x ^ {(i)}) - \Phi (x ^ {(j)}))). \tag {9}
$$

Here the constant $a \geq 0$ represents the swapping intensity. In this manner, robots occupying positions associated with smaller potential function values are inclined to be assigned a role of exploiter, specified by a lower temperature, and vice versa. To elucidate the exchange rule, let us assume, without loss of generality, that $0 ~ < ~ \tau ^ { ( i ) } ~ < ~ \tau ^ { ( j ) } ~ < ~ \infty$ and $a = 1$ . If $\Phi ( x ^ { ( i ) } ( t ) ) > \Phi ( x ^ { ( j ) } ( t ) )$ , then robot i swaps its temperature with robot $j ;$ otherwise, they swap with a probability $s ( i , j ) \in ( 0 , 1 )$ , which diminishes monotonically with respect to the difference between two objective values. For example, as $\Phi (  { \boldsymbol { { x } } } ^ { ( i ) } ) \ \to \ 0$ and $\Phi ( x ^ { ( j ) } ) ~  ~ + \infty$ , the swapping rate $s \to 0$ .

![](images/289a0f4522129df6b5560e5de41703ef0bf9fa979688ad5d199b64a8ef8ba172.jpg)



(a) Experimental testbed

![](images/4fe7874ed656e0d626fc7355e13886f6dd690ace28e682b507f15884a49ca2b7.jpg)



(b) Mobile robot   
Fig. 5. Experimental testbed of SniffySquad.

Under the specific swapping rule defined in Eq. (9), the algorithm exhibits an acceleration effect in concentrating around the global minima of $\Phi ( x )$ . This effect is theoretically analysed and demonstrated in [31]. Meanwhile, sampling in this manner still leads to the minimization of potential function and hence the identification of the most probable gas source location. This is because the equilibrium distribution of the replica exchange Langevin diffusion is also Eq. (8), the same as algorithms in which robots follow independent diffusion processes in Eq. (7).

# VII. IMPLEMENTATION AND EVALUATION

In this section, we evaluate the system’s performance from two aspects: source localization effectiveness and search efficiency. We first describe the settings of both physical and simulation experiments, as well as the metrics used in the evaluation (Section VII-A). We then compare overall performance of SniffySquad in both a testbed and simulation (Section VII-B). We also carry out experiments under different conditions to evaluate SniffySquad’s robustness to both external and internal factors (Section VII-C).

# A. Implementation and Setting

1) Field Experiment Setup: We first describe how we build an environment with gas, then mobile robots deployed in the testbed.

Gas environment. As illustrated in Fig. 5, we build a gas leakage testbed in a rectangular 15m × 10m laboratory environment. Since generating gas plumes for conducting field experiments requires strict safety and environmental considerations, we simulate the gas leakage scenario by adopting a smoke machine as the gas generator to release gas following previous work [23], [35], [36]. The primary component of the smoke fluid is ethylene glycol (EINECS No. 246-770-3). The behavior of such plumes mirrors that of numerous gas plumes in real-world application scenarios [37], [38]. We deploy a fan behind the gas generator to generate turbulent wind.

Multi-robot platform. We implement SniffySquad on commercial unmanned ground vehicles, as shown in Fig.5(b). Each robot is equipped with a particle matter sensor Plantower

![](images/b5c9f4b42003ee53b2d79789b50d50687e3fca444f960f6a680098d5e82f5e6f.jpg)



(a) Surge-Cast

![](images/e6b28f8410ac2dbeb0f372c812b2ebb93a4aed2fe20d0ce4d4fcd0b930c36520.jpg)



(b) Infotaxis

![](images/67e02aa74f8703c70cc3b6dae2c63363513e79a7dba8c87efcbd85f5c93c2bab.jpg)



(c) SniffySquad

![](images/b3522f371a2b3545e0f0dbfc23ea9522f7e4c835d6c05cb66673fd4bd7af661c.jpg)



(d) Distances to source over time   
Fig. 6. In an empty space (w/o walls and obstacles). (a)-(c) Illustration of trajectories generated by Surge-Cast, Infotaxis, and SniffySquad. The red rectangles indicate the trajectories that were misled by the gas patches. (d) The distance of the robot to the gas release source over time.

TABLE II OVERALL PERFORMANCE OF FIELD EXPERIMENT. 

<table><tr><td></td><td>Success Rate</td><td>Path Efficiency(%)</td></tr><tr><td>SniffySquad</td><td>5/6</td><td>90.0</td></tr><tr><td>Infotaxis</td><td>4/6</td><td>62.0</td></tr><tr><td>Surge-Cast</td><td>4/6</td><td>61.0</td></tr></table>

PMS5003T [39], which is capable of measuring concentration of particles with diameters less than 3 micrometers, expressed in units of micrograms per cubic meter $( \mu g / m ^ { 3 } )$ . When ethylene glycol is atomized, it forms aerosol particles. The particle matter sensor is utilized to detect these particles, allowing us to measure the concentration of ethylene glycol. Additionally, an ultrasonic anemometer has been integrated to provide data on wind direction and speed. To establish ground truth positions, a UWB localization device is integrated. Robot movement is guided by a PID controller. The onboard computer of the robot is a Raspberry Pi 4 Computer Model B with 8GB RAM, and the edge server is equipped with Intel(R) Core(TM) i7- 11700 of 2.50GHz main frequency and 16G RAM, running the Ubuntu 20.04.4 operating system. Mobile robots depart from the opposite side of the gas source, i.e., the right side of Fig.5(a).   
2) Simulation Setting: To simulate gas dispersion processes, we follow previous works [33] and build up the simulation environment based on two tools: (i) OpenFOAM [40], a computational fluid dynamics (CFD) simulator, is used to generate the wind flow vector field; (ii) GADEN [41], a 3-D gas dispersion simulator widely recognized and commonly used for robotic olfaction, is used to generate the gas concentration field. The gas simulation process involves two key steps: First, OpenFOAM models the flow of wind based on the environment geometry that is configured by a

TABLE III CONFIGURATION OF GAS DISPERSION PARAMETERS 

<table><tr><td>Symbol</td><td>Value</td><td>Description</td></tr><tr><td> $\mu$ </td><td>10 ppm</td><td>Gas conc. at filament center</td></tr><tr><td> $\sigma$ </td><td>10 cm</td><td>Initial std of filament</td></tr><tr><td> $\gamma$ </td><td>10  $cm^{2}/s$ </td><td>Growth ratio of  $\sigma$ </td></tr><tr><td>P, T</td><td>1 Atm, 298 Kelvins</td><td>Pressure and temperature</td></tr><tr><td> $\upsilon$ </td><td> $1.529 \times 10^{-5} m^{2}/s$ </td><td>Kinematic viscosity</td></tr><tr><td> $\rho$ </td><td> $1.196 kg/m^{3}$ </td><td>Air density</td></tr><tr><td>k</td><td> $3.75 \times 10^{-3} m^{2}/s^{2}$ </td><td>Turb. kinetic energy</td></tr><tr><td> $\varepsilon$ </td><td> $1.25 \times 10^{-2} m^{2}/s^{3}$ </td><td>Dissipation rate</td></tr></table>

![](images/8b3356a5deefe53fbddda957888b5118e545685618b39b9efdced84b597845ed.jpg)



(a) Success Rate

![](images/370b060586212188855e83853b174e8c5446bac691b9c4dbc7531c3d59aa6bf9.jpg)



(b) Path Efficiency   
Fig. 7. Overall performance of physical feature-based simulation experiments.

computer-aided design (CAD) model, and the specified flow inlets and outlets; Second, based on the wind flow data, GADEN takes the environment CAD model as input and obtains 3D gas distributions by implementing the filament gas dispersion theory [42]. The specific parameter configuration is listed in Table III. Our experiments include two representative scenarios in industrial factories: (i) empty spaces Fig. 11(a) and (ii) environments with rooms featuring walls and obstacles Fig. 11(b). To simulate robot’s dynamics, we implement a controller based on [43].

3) Comparative Methods: We compared SniffySquad with two related state-of-the-art (SOTA) methods including: (i) Surge-Cast [10], a SOTA reactive bio-inspired GSL algorithm. This algorithm involves two distinct motions patterns: when the robot identifies the plume concentration exceeding a predefined threshold, it engages in a ”surge”, i.e., moving upwind; otherwise, it executes a ”cast” maneuver perpendicular to the wind direction to re-establish contact with the plume; (ii) Infotaxis [33], a SOTA probabilistic source parameter estimation-based GSL algorithm. It’s an information-driven path planning algorithm, leveraging a probability map of the source position estimation and driving the robot’s movement toward the place with the highest information gain.   
4) Evaluation Metrics: We employ the following two metrics to evaluate the algorithms’ effectiveness and efficiency, respectively: (i) Success Rate (SR). It is determined by calculating the ratio of successful trials across all repeated experiments. A trial is deemed successful if mobile olfactory robots reach the vicinity of the actual ground truth position of the gas source within the predefined time limit and distance threshold $\varepsilon _ { s }$ . The threshold is set to 0.5m in the experiments. In practical application scenarios, the gas leakage source can be detected using onboard cameras as soon as it comes within a robot’s line-of-sight. (ii) Path Efficiency (PE). It is defined as $\frac { d _ { m i n } } { d }$ , where $d _ { m i n }$ is the shortest path distance from the robot’s starting point to the gas source, and d is the length of

![](images/423906b2aabb695433c7bf7f9c838225e5704b1351e598fb3950d27901c41c9a.jpg)



(a) Success Rate

![](images/f7bd11216f76b9faf2d0bc8d30e0ff914e9f0b1de9ed1ead26f19d78807115b7.jpg)



(b) Path Efficiency (Weak Source)

![](images/eaa84b2abf4ba37e4213ac8c347ab5ef2b14f7e19faaec5a616f7e4a7234b09b.jpg)



(c) Path Efficiency (Strong Source)

Fig. 8. Impact of gas emission intensity. (a) Success rate. (b)-(c) CDF of path efficiency under a weak and a strong source, respectively.   
![](images/e1dd3dd9931f53ac952e4afe5417c89c592c4a347edf827613f59579338a65ff.jpg)



(a) Success Rate

![](images/2cd1e152856e908825c1e01ca42b708cee30fc142728e7a4d0f34366d60826b2.jpg)



(b) Path Efficiency (Empty Space)

![](images/ce0c20667a19ed502f61c4f02bcd5f8b59681ccda27744bc436c6db2e4d73f0a.jpg)



(c) Path Efficiency (Structured Space)   
Fig. 9. Impact of environment geometry. (a) Success rate. (b)-(c) CDF of path efficiency under an empty and a structured space, respectively.

the robot’s travel trajectory driven by GSL approaches. This metric is only calculated for successful trials. Note that path efficiency is proportional to the time required for localizing the gas source, which aligns with the objective in Eq.1.

# B. Overall Performance

Table II illustrates overall performance evaluated in the testbed. A total of 6 experiments were conducted to compare the performance between Surge-Cast to Infotaxis and SniffySquad. In terms of both success rate and path efficiency, the performance of SniffySquad surpasses two SOTA baselines, Surge-Cast and Infotaxis. SniffySquad improves the path efficiency (i.e., decreases the trajectory lengths) by 32% and 32% compared to Surge-Cast and Infotaxis, respectively.

Fig. 7 evaluates overall performance of SniffySquad in physical feature-based simulations, using various numbers of robots. These experiments were carried out 50 times for each configuration. Across all scenarios involving robot counts ranging from one to three, it is evident that SniffySquad consistently attains the highest success rate, achieves the shortest search time for both an individual robot and robot teams, and generates the most efficient path. Specifically, SniffySquad achieves a success rate of 76% for a team of three robots, improving by 30% and 20% in comparison with Surge-Cast and Infotaxis, respectively. The search time and path efficiency are 148s and 0.67, reducing the total search time by 22.92% and 18.46%, shortening the trajectory length by 41.79% (from $2 . 5 6 d _ { m i n }$ to $1 . 4 9 d _ { m i n } )$ and 32.84% (from $2 . 2 2 d _ { m i n }$ to $1 . 4 9 d _ { m i n } )$ , respectively. This results from the resilience brought by the individual-level movement planning and the team-level roles adaptation algorithm, which enable robots to escape from false positive sources and parallelize the exploration of the environment and exploitation of collected information in a flexible manner. For all algorithms, success rates show an upward trend as the number of robots employed for gas source search and localization increases. Apparently, this is because the area is explored to a greater extent when more robots are working.

To further compare the performance of SniffySquad and baseline methods, we visualize the trajectories of all methods in Fig. 6 (a)-(c). It is demonstrated that SniffySquad produces smoother trajectories than baselines. Surge-Cast, a reactive method relying solely on current observations to make decisions, yields inefficient zig-zag paths and is the most susceptible to spatial and temporal gas concentration fluctuations (as shown in Fig. 2). Infotaxis, though incorporating a Bayesian gas source position estimator to filter the sensory measurements, suffers from trap in patchy areas. Fig. 6 (d) illustrates the nearest distance to the source within all robots over time. It’s verified that SniffySquad navigates towards the source the most efficiently and arrives at the source the most quickly. Surge-Cast takes 231 seconds and Infotaxis takes 187 seconds in total while SniffySquad takes only 145 seconds, indicating a decrease in search time by 37.23% and 22.46% in comparison to the two baselines, respectively. The acceleration effect produced by SniffySquad relative to previous methods in localizing the source attributes to the movement planning method that regulates the robots’ moving direction to enable escaping from gas patches, as well as the collaborative assignment and adaptation of team roles.

# C. System Robustness

We further experimentally evaluate SniffySquad with respect to various environmental conditions and key parameter settings in our system.

![](images/42b6150e28579a2f0fd27d8b978922aa25837eeb9d3b0f58b4e7c967a86196a5.jpg)



(a) Weak source

![](images/bd0b6e7315959f7825c4f9c6c9650b184e6be3b84613d0008a565f08905350e3.jpg)



(b) Strong source   
Fig. 10. Illustration of gas concentration fields under different emission intensities.

![](images/bc93bf6159d5e004bdf15e24599b8ce623eafb306863c730aad941effae25ee2.jpg)



(a) Empty Space

![](images/6b707adc4ccadca86bc3d95228359098d4853d7e5c37f431331dc2eeb4962a6c.jpg)



(b) Structured Space   
Fig. 11. Illustration of environment geometries.

1) Impact of Gas Emission Intensity: In real-world scenarios, SniffySquad should be capable of handling situations where different gas emission intensities are presented. Therefore, we investigate the performance of our system when handling different release rates of the gas source. Specifically, we select two representative gas release rates of 10 filaments per second and 30 filaments per second, which are denoted as a weak source and a strong source, respectively. As illustrated in Figs. 10(a) and 10(b), a snapshot of the field with the weak source shows a more discontinuous gas concentration field compared to that of the strong source, which indicates a higher difficulty for gas source localization.

We compare the performance of the proposed method and baselines under these two scenarios, as shown in Fig. 8. Firstly, across scenarios of a strong and a weak source, our method consistently achieves the highest success rate and the most efficient paths among all methods. This can be attributed to the patchy plume-resilient movement planning mechanism, as well as role adaptation based collaboration among robots in the team. Secondly, for all the methods, the success rate and path efficiency degrade as the gas emission intensity from strong turns to weak. This is because the olfactory stimulus in a field induced by the weaker source is sparser, confusing the robots more severely. Thirdly, it’s noteworthy that our approach’s advantage is especially significant under the weak gas source, validating its remarkable robustness to gas emission intensity. From the strong to weak source scenario, Surge-Cast and Infotaxis’ success rates decrease considerably by 12% and 20%, respectively, while their path efficiencies degrade significantly by 41% and 33%, respectively. In contrast, SniffySquad still maintains a success rate of above 89% and its path efficiency slightly reduces by only 13%. This is because of the integrated design of sensing and planning processes in our method, which allows the robot to escape from spurious gas patches and leads to more efficient localization.

![](images/d59122d8ced917e55ca449d49693171cdc759c347521afb28c987a984bbb6a58.jpg)



Fig. 12. Impact of initial distance to source.

![](images/eedc2227cb6c1ed4d8e2d1ec99016396b61b6bfdd17299649197efb72ec2529d.jpg)



Fig. 13. Impact of temperature parameter.

2) Impact of Geometry of the Environment: We evaluate the robustness of our approach in different environment geometries. As shown in Figs. 11(a) and 11(b), we evaluate all the methods in an empty space (without obstacles) and a structured space (with walls and rooms) to verify the benefits of our method. From Fig. 9, we can see that SniffySquad keeps outperforming the baseline method on both the success rate and path efficiency. Besides, although the structured space significantly increases the difficulty of GSL, our method maintains a success rate of more than 70% and an average path efficiency of around 0.6%. Note that Infotaxis shows a better performance than Surge-Cast in the empty space, but its performance degrades greatly when deployed in a more complex structured space. This indicates that SniffySquad avoids the oversimplified assumption of either the gas model or the environment, thus featuring the capability to handle complex environments with little performance degradation.

3) Impact of Initial Distance to the Source: We examine the impact of robots’ initial distances to the gas source on the task. The robots initiate their journey from five distinct positions, ranging from close to gradually increasing distances relative to the gas source. As shown in Fig. 12, when the initial distance is less than 70m, the success rate remains around 100% and the path efficiency decreases gradually as the initial distance grows. However, when it comes to a distance larger than 70m, we notice that the success rate quickly decreases. This is because the gas plume becomes more and more patchy as the distance increases (as illustrated in Fig. 2), inducing higher probability that the robots are entrapped or misled to a false source localization. We also note that even when the robots start searching at 90m away from the source, SniffySquad can still achieve an average search time of 148.1s for the successful trials.

4) Impact of Temperature Parameters: As clarified in Section VI, the temperature τ is a critical parameter in the system as it governs the role of a robot. To clarify the impact on the system performance with respect to values of temperature, all the robots are assigned an identical temperature across five orders of magnitude in the experiments. As illustrated in Fig. 13, the results of success rate and path efficiency exhibit different trends as the temperature rises. For the success rate, as the temperature increases, it shows an incline trend at first and reaches the maximum at the temperature of $1 0 ^ { - 1 }$ , and then declines gradually; for the path efficiency, its value gradually decreases as the temperature grows, especially when it rises over $1 0 ^ { - 1 }$ . This pattern echoes our previous analysis that either too exploitative movement (low temperature) or explorative movement (high temperature) fails to balance the trade-off of search efficiency and effectiveness. SniffySquad combines the advantages of both behaviors via the collaborative roleswitching method, making SniffySquad more superior to other approaches.

# VIII. CONCLUSION

This paper proposes SniffySquad, a multi-robot olfactionbased system for gas source localization. SniffySquad features two key designs from non-convex learning perspective to conquer the patchy characteristic of gas plumes and enable efficient and effective source localization by a collaborative strategy, as elaborated below. Specifically, we devise a patchy plume-resilient movement strategy inspired by Langevin diffusion approach. We then develop a collaborative strategy for multiple robots by assigning and adapting their planning preferences dynamically to balance the search efficiency and localization effectiveness of gas sources. We implement SniffySquad with multiple unmanned ground vehicles and conduct experiments in a real-world testbed. Results show that SniffySquad achieves a remarkable 20%+ success rate and 30%+ path efficiency improvement, respectively, outperforming state-of-the-art gas source localization solutions.

# REFERENCES

[1] X. Liu, X. Xu, X. Chen, E. Mai, H. Y. Noh, P. Zhang, and L. Zhang, “Individualized calibration of industrial-grade gas sensors in air quality sensing system,” in Proceedings of the 15th ACM Conference on Embedded Network Sensor Systems, 2017, pp. 1–2.   
[2] S. Pal, A. Ghosh, and V. Sethi, “Vehicle air pollution monitoring using iots,” in Proceedings of the 16th ACM conference on embedded networked sensor systems, 2018, pp. 400–401.   
[3] B. Maag, Z. Zhou, and L. Thiele, “W-air: Enabling personal air pollution monitoring on wearables,” Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, vol. 2, no. 1, pp. 1– 25, 2018.   
[4] X. Sun, J. Xiong, C. Feng, X. Li, J. Zhang, B. Li, D. Fang, and X. Chen, “Gastag: A gas sensing paradigm using graphene-based tags,” in Proceedings of the 30th Annual International Conference on Mobile Computing and Networking, 2024, pp. 342–356.   
[5] X. Liu, X. Chen, X. Xu, E. Mai, H. Y. Noh, P. Zhang, and L. Zhang, “Delay effect in mobile sensing system for urban air pollution monitoring,” in Proceedings of the 15th ACM Conference on Embedded Network Sensor Systems, 2017, pp. 1–2.

[6] G. McCarron, “Air pollution and human health hazards: a compilation of air toxins acknowledged by the gas industry in queensland’s darling downs,” International Journal of Environmental Studies, vol. 75, no. 1, pp. 171–185, 2018.   
[7] G. Manes, G. Collodi, L. Gelpi, R. Fusco, G. Ricci, A. Manes, and M. Passafiume, “Realtime gas emission monitoring at hazardous sites using a distributed point-source sensing infrastructure,” Sensors, vol. 16, no. 1, p. 121, 2016.   
[8] J. R. Bourne, M. N. Goodell, X. He, J. A. Steiner, and K. K. Leang, “Decentralized multi-agent information-theoretic control for target estimation and localization: finding gas leaks,” The International Journal of Robotics Research, vol. 39, no. 13, pp. 1525–1548, 2020.   
[9] M. Hutchinson, H. Oh, and W.-H. Chen, “Entrotaxis as a strategy for autonomous search and source reconstruction in turbulent conditions,” Information Fusion, vol. 42, pp. 179–189, 2018.   
[10] G. Reddy, V. N. Murthy, and M. Vergassola, “Olfactory sensing and navigation in turbulent environments,” Annual Review of Condensed Matter Physics, vol. 13, pp. 191–213, 2022.   
[11] X.-x. Chen and J. Huang, “Odor source localization algorithms on mobile robots: A review and future outlook,” Robotics and Autonomous Systems, vol. 112, pp. 123–136, 2019.   
[12] C. Rhodes, C. Liu, P. Westoby, and W.-H. Chen, “Autonomous search of an airborne release in urban environments using informed tree planning,” Autonomous Robots, vol. 47, no. 1, pp. 1–18, 2023.   
[13] C. Rhodes, C. Liu, and W.-H. Chen, “Informative path planning for gas distribution mapping in cluttered environments,” in 2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2020, pp. 6726–6732.   
[14] J. R. Bourne, E. R. Pardyjak, and K. K. Leang, “Coordinated Bayesian-Based Bioinspired Plume Source Term Estimation and Source Seeking for Mobile Robots,” IEEE Transactions on Robotics, vol. 35, no. 4, pp. 967–986, 2019.   
[15] B. P. Duisterhof, S. Li, J. Burgues, V. J. Reddi, and G. C. de Croon, ´ “Sniffy bug: A fully autonomous swarm of gas-seeking nano quadcopters in cluttered environments,” in 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2021, pp. 9099–9106.   
[16] W. Deng, G. Lin, and F. Liang, “A contour stochastic gradient langevin dynamics algorithm for simulations of multi-modal distributions,” Advances in neural information processing systems, vol. 33, pp. 15 725– 15 736, 2020.   
[17] A. Loisy and C. Eloy, “Searching for a source without gradients: how good is infotaxis and how to beat it,” Proceedings of the Royal Society A, vol. 478, no. 2262, p. 20220118, 2022.   
[18] E. Holzbecher and E. Holzbecher, “2d and 3d transport solutions (gaussian puffs and plumes),” Environmental modeling: using MATLAB, pp. 303–316, 2012.   
[19] M. Vergassola, E. Villermaux, and B. I. Shraiman, “‘infotaxis’ as a strategy for searching without gradients,” Nature, vol. 445, no. 7126, pp. 406–409, 2007.   
[20] C. Wang, T. Li, M. Q.-H. Meng, and C. De Silva, “Efficient mobile robot exploration with gaussian markov random fields in 3d environments,” in 2018 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2018, pp. 5015–5021.   
[21] A. J. Lilienthal, M. Reggente, M. Trincavelli, J. L. Blanco, and J. Gonzalez, “A statistical approach to gas distribution modelling with mobile robots-the kernel dm+ v algorithm,” in 2009 IEEE/RSJ International Conference on Intelligent Robots and Systems. IEEE, 2009, pp. 570– 576.   
[22] A. Gongora, J. Monroy, and J. Gonzalez-Jimenez, “Joint estimation of gas and wind maps for fast-response applications,” Applied Mathematical Modelling, vol. 87, pp. 655–674, 2020.   
[23] J. R. Bourne, E. R. Pardyjak, and K. K. Leang, “Coordinated bayesianbased bioinspired plume source term estimation and source seeking for mobile robots,” IEEE Transactions on Robotics, vol. 35, no. 4, pp. 967– 986, 2019.   
[24] L. Marques, U. Nunes, and A. T. de Almeida, “Olfaction-based mobile robot navigation,” Thin solid films, vol. 418, no. 1, pp. 51–58, 2002.   
[25] Y. Cao, Y. Wang, A. Vashisth, H. Fan, and G. A. Sartoretti, “Catnipp: Context-aware attention-based network for informative path planning,” in Conference on Robot Learning. PMLR, 2023, pp. 1928–1937.   
[26] H. Ma, T. Zhang, Y. Wu, F. du Pin Calmon, and N. Li, “Gaussian max-value entropy search for multi-agent bayesian optimization,” 2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 10 028–10 035, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:257482432

[27] T. Zhang, V. Qin, Y. Tang, and N. Li, “Distributed information-based source seeking,” IEEE Transactions on Robotics, vol. 39, pp. 4749–4767, 2022. [Online]. Available: https://api.semanticscholar.org/CorpusID: 252383539   
[28] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” arXiv preprint arXiv:1412.6980, 2014.   
[29] X. Cheng, The Interplay between Sampling and Optimization. University of California, Berkeley, 2020.   
[30] Y.-A. Ma, Y. Chen, C. Jin, N. Flammarion, and M. I. Jordan, “Sampling can be faster than optimization,” Proceedings of the National Academy of Sciences, vol. 116, no. 42, pp. 20 881–20 885, 2019.   
[31] Y. Chen, J. Chen, J. Dong, J. Peng, and Z. Wang, “Accelerating nonconvex learning via replica exchange langevin diffusion,” arXiv preprint arXiv:2007.01990, 2020.   
[32] J. C. Strikwerda, Finite difference schemes and partial differential equations. SIAM, 2004.   
[33] P. Ojeda, J. Monroy, and J. Gonzalez-Jimenez, “Information-driven gas source localization exploiting gas and wind local measurements for autonomous mobile robots,” IEEE Robotics and Automation Letters, vol. 6, no. 2, pp. 1320–1326, 2021.   
[34] D. J. Earl and M. W. Deem, “Parallel tempering: Theory, applications, and new perspectives,” Physical Chemistry Chemical Physics, vol. 7, no. 23, pp. 3910–3916, 2005.   
[35] M. Hutchinson, P. Ladosz, C. Liu, and W.-H. Chen, “Experimental assessment of plume mapping using point measurements from unmanned vehicles,” in 2019 International Conference on Robotics and Automation (ICRA). IEEE, 2019, pp. 7720–7726.   
[36] M. Hutchinson, C. Liu, and W.-H. Chen, “Information-based search for an atmospheric release using a mobile robot: Algorithm and experiments,” IEEE Transactions on Control Systems Technology, vol. 27, no. 6, pp. 2388–2402, 2018.   
[37] N. Kadakia, M. Demir, B. T. Michaelis, B. D. DeAngelis, M. A. Reidenbach, D. A. Clark, and T. Emonet, “Odour motion sensing enhances navigation of complex plumes,” Nature, vol. 611, no. 7937, pp. 754–761, 2022.   
[38] A. Francis, S. Li, C. Griffiths, and J. Sienz, “Gas source localization and mapping with mobile robots: A review,” Journal of Field Robotics, vol. 39, no. 8, pp. 1341–1373, 2022.   
[39] M. Levy Zamora, F. Xiong, D. Gentner, B. Kerkez, J. Kohrman-Glaser, and K. Koehler, “Field and laboratory evaluations of the lowcost plantower particulate matter sensor,” Environmental science & technology, vol. 53, no. 2, pp. 838–849, 2018.   
[40] H. Jasak, “Openfoam: Open source cfd in research and industry,” International Journal of Naval Architecture and Ocean Engineering, vol. 1, no. 2, pp. 89–94, 2009.   
[41] J. Monroy, V. Hernandez-Bennetts, H. Fan, A. Lilienthal, and J. Gonzalez-Jimenez, “Gaden: A 3d gas dispersion simulator for mobile robot olfaction in realistic environments,” Sensors, vol. 17, no. 7, p. 1479, 2017.   
[42] J. A. Farrell, J. Murlis, X. Long, W. Li, and R. T. Carde, “Filament- ´ based atmospheric dispersion model to achieve short time-scale structure of odor plumes,” Environmental fluid mechanics, vol. 2, pp. 143–169, 2002.   
[43] W. Chen, R. Khardon, and L. Liu, “Adaptive robotic information gathering via non-stationary gaussian processes,” The International Journal of Robotics Research, vol. 43, no. 4, pp. 405–436, 2024.