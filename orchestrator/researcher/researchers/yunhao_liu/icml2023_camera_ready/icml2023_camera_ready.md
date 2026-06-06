# Optimal Arms Identification with Knapsacks

Shaoang Li 1 Lan Zhang 1 Yingqi Yu 1 Xiang-Yang Li 1

# Abstract

Best Arm Identification (BAI) is a general online pure exploration framework to identify optimal decisions among candidates via sequential interactions. We pioneer the Optimal Arms identification with Knapsacks (OAK) problem, which extends the BAI setting to model the resource consumption. We present a novel OAK algorithm and prove the upper bound of our algorithm by exploring the relationship between selecting optimal actions and the structure of the feasible region. Our analysis introduces a new complexity measure, which builds a bridge between the OAK setting and bandits with knapsacks problem. We establish the instance-dependent lower bound for the OAK problem based on the new complexity measure. Our results show that the proposed algorithm achieves a near-optimal probability bound for the OAK problem. In addition, we demonstrate that our algorithm recovers or improves the state-of-the-art upper bounds for several special cases, including the simple OAK setting and some classical pure exploration problems.

# 1. Introduction

Multi-armed bandits exemplify the exploration-exploitation trade-off framework in online decision-making problems. The decision-maker selects arms (actions, options, decisions) sequentially and learns from the rewards to maximize the expected cumulative rewards over a number of trials. Many applications need to identify the best action over the candidates, and the rewards or loss during the exploration is ignored, which is defined as the best arm identification (BAI) problem (Audibert et al., 2010). For example, in a medical trial problem with m candidate ingredients and T patients that can be admitted to the medical trial (the exploration phase is limited by a fixed budget T ), the decision-maker 1University of Science and Technology of China, Hefei, China. Correspondence to: Lan Zhang <zhanglan@ustc.edu.cn>, Xiang-Yang Li <xiangyangli@ustc.edu.cn>.

Proceedings of the $\mathit { 4 0 } ^ { t h }$ International Conference on Machine Learning, Honolulu, Hawaii, USA. PMLR 202, 2023. Copyright 2023 by the author(s).

would like to identify the best ingredient to minimize harm to the patients or maximize the medical therapeutic effect. A series of efforts have been made to solve variants of BAI problems (Xu et al., 2020; Katz-Samuels & Jamieson, 2020; Zhang & Ong, 2021; Zhong et al., 2021).

The bandits with knapsacks (BwK) framework was introduced by (Badanidiyuru et al., 2013) to deal with a more general and realistic setting that takes the resource consumption into consideration. In the BwK setting, the optimal fixed distribution over arms may outperform the arm with the highest expected reward. The support of optimal distribution is composed of the arms with optimal ‘bang-per-buck,’ i.e., reward per unit of resource consumption, thus there are multiple ‘optimal arms’ (Badanidiyuru et al., 2013). Existing works focus on maximizing the accumulated reward under the resource constraints by finding the optimal fixed distribution (Badanidiyuru et al., 2013; Agrawal & Devanur, 2014).

In this paper, we consider a common situation in which the decision-maker needs to identify all optimal arms with the knapsack constraints, and define it as the optimal arms identification (OAK) problem. In the OAK setting, there exists a fixed set of arms and the hard constrained capacity for each resource; each arm is associated with an unknown reward distribution and an unknown consumption distribution. During the exploration, the decision-maker chooses an arm in each round and only observes a scalar-valued reward independently sampled from the reward distribution and a resource consumption vector independently sampled from the consumption distribution. Once one or more resource budget constraint is violated then the exploration stops. The decision-maker aims to maximize the probability of identifying all optimal arms with the resource knapsacks.

The OAK problem encompasses a wide range of applications due to the presence of resource constraints in pure exploration decision problems. For example, during the medical testing phase, the selection of ingredients may be constrained by the supply and monetary cost of each component, and the decision-maker would like to identify the ingredients that minimize harm to the patients or maximize the medical therapeutic effect. Similarly, the dynamic pricing problem involves sellers who face limited supply and aim to determine the optimal policy for maximizing expected revenue. In the dynamic procurement problem, algorithms are designed to purchase items or services while adhering to budgetary and other constraints.

The knowledge of optimal arms, which is not limited to pure exploration settings, is also valuable for addressing the associated regret minimization BwK problem. Previous work demonstrates that even with sufficient exploration about the optimal solution of LP to converge on an LP-perfect distribution while avoiding obviously suboptimal strategies, an√ $O ( \sqrt { T } )$ gap with the optimum remains necessary (Badanidiyuru et al., 2013). In contrast, subsequent studies present tighter regret upper bounds with the known optimal arms set (Flajolet & Jaillet, 2015; Li et al., 2021). For instance, (Li et al., 2021) prove the $O ( d ^ { 4 } / b ^ { 2 } )$ regret upper bound, omitting other problem-dependent parameters, which does not depend on T .

The OAK problem raises several challenges for designing and analyzing algorithms. One challenge is the unknown number of optimal arms, which necessitate that the algorithm explores the structure of the feasible region. Another one is to estimate the fixed optimal distribution, as with the BwK problem. The expected per-round reward is no longer a reliable estimate of the arm’s value. Each pull of any arm may influence the decision-maker’s estimated optimal distribution and lead to a different result. The algorithm needs to search over all possible distributions. And the large search space of possible distribution exacerbates the difficulty of the problem. This differs from the overwhelming majority of previous pure exploration bandits settings. Therefore, the design and analysis of algorithms require new technical tools for characterizing the complexity of the new exploration problem.

# 1.1. Our contributions

We pioneer the OAK setting under knapsacks constraints in this paper. First, we propose a BASEOAK learning algorithm based on the quarter reject/accept strategy. The analysis of our algorithm depends on our observation of the relationship between selecting optimal arms (point aspect) and the structure of the feasible domain (global aspect). We develop a new complexity measure based on this observation. Our analysis shows the ‘successive elimination-style’ algorithm places excessive emphasis on point aspect and veers widely from the optimal distribution.

Then, we develop a FULLOAK algorithm based on BASEOAK that strikes a balance between converging to the optimal distribution and exploring the optimality of arms. We upper bound the probability that the algorithm makes mistakes based on the new complexity measure. We establish the instance-dependent lower bound for the OAK problem. The analysis shows that FULLOAK is close to optimum - the lower bound matches the error probability in the exponential term up to a constant factor.

Last, We further investigate some special cases of OAK setting. We study the simple OAK setting for the case that influence from selections of different arms could be avoided. For the simple OAK problem, we present a near-optimal algorithm BASEOAK− based on BASEOAK. We demonstrate that BASEOAK− recovers or improves the state-of-the-art upper bounds for many classical pure exploration problems, including the BAI problem, top-K best arms identification problem, and multi-bandits best arms identification problem.

# 2. Problem Setup and Technical Preliminaries

In this paper, we use bold fonts to represent vectors and matrices. For a matrix C, we use $C _ { j , }$ · and $C _ { \cdot , i }$ to denote the j-th row vector and the i-th column vector, respectively. For a set X , we use $| \mathcal { X } |$ | to denote its cardinality.

# 2.1. Problem setup

We formally define the OAK problem below. Given T rounds, m arms and d types of resources being consumed, they are indexed by $[ T ] = 1 , 2 , \ldots , T , [ m ] = 1 , 2 , \ldots , m .$ , and $[ d ] \ = \ 1 , 2 , \ldots , d ,$ respectively. Each arm is associated with an unknown reward distribution and an unknown consumption distribution. In each round t, the algorithm plays an arm $i ( t ) \in [ m ]$ , then observes a scalarvalued reward $r ( t ) ~ \in ~ [ 0 , 1 ]$ and a resource consumption vector $\pmb { c } ( t ) \in [ 0 , 1 ] ^ { d }$ , which are independently sampled from the reward/consumption distribution. The jth component of $\mathbf { } c ( t )$ represents consumption of resource j. There are some fixed unknown reward expected vector $\pmb { \mu } = ( \mu _ { 1 } , \ldots , \mu _ { m } ) ^ { \top } \in [ 0 , 1 ] ^ { m }$ and consumption expected matrix $C = ( C _ { \cdot , 1 } , \dots , C _ { \cdot , m } ) \in [ 0 , 1 ] ^ { d \times m }$ such that $\mathbb { E } [ r ( t ) | i ( t ) ] = \mu _ { i ( t ) }$ and $\mathbb { E } [ { \pmb { c } } ( t ) | i ( t ) ] = \pmb { C } _ { \cdot , i ( t ) }$ .

We use B to denote the hard resource constraint vector. For each resource j, there is a pre-specified knapsack $B _ { j }$ representing the maximum amount constraint of consumption over all time horizons. Once one or more resource budget constraint is violated then the exploration stops. We say the constraints are uniform if $B _ { j } = B$ for all resource $j \in [ d ]$ . And any OAK instance can be reduced to one with uniform constraints $B = \mathrm { m i n } _ { j \in [ d ] } B _ { j }$ . For notation simplicity, we focus on the uniform OAK setting with knapsack B. Let $b = B / T$ denote the expected per-round resource constraint. Besides, we assume that the 1-st resource is the ‘time’ resource and each arm deterministically consumes 1 unit of it whenever it is picked. We assume the 1-st arm is the ‘null’ arm that can be played with no reward and only consumes the time resource. These assumptions are standard form in BwK literature (Badanidiyuru et al., 2013; Agrawal & Devanur, 2014; Li et al., 2021).

For a problem instance, we say one arm i is an optimal arm if it would be selected by the optimal dynamic policy in expectation. We give a more precise definition in the linear relaxation part below. The OAK algorithm aims to maximize the probability that correctly identifies all optimal arms with the fixed resource constraint. Formally, let $\mathcal { X } ^ { \ast }$ denote the index set of all optimal arms. The algorithm has to output an arm set ${ \mathcal { O } } \subseteq [ m ]$ ] once any constraint is violated (includes the time resource). The algorithm tries to maximize $\mathbb { P } [ \mathcal { O } = \mathcal { X } ^ { * } ]$ .

# 2.2. Linear relaxation

The OAK problem can be relaxed to the following linear program

$$
\max \quad \boldsymbol {\mu} ^ {\top} \boldsymbol {x},
$$

$\mathrm { s . t . } \quad C x \leq b ,$ (1)

$$
\boldsymbol {x} \geq 0.
$$

The x is the decision vector and $x _ { i }$ corresponds to the probability to select arm $i \in [ m ]$ . The LP (1) always has feasible solutions because of the existence of null arms. Let $\mathrm { O P T } _ { \mathrm { L P } }$ and $\mathbf { \nabla } _ { \mathbf { \mathcal { X } } } ^ { * }$ denote the optimal value and optimal solution of (1), respectively. One arm $i \in [ m ]$ is an optimal arm if the corresponding variable is basic variable in $\pmb { x } ^ { * }$ , i.e. $x _ { i } ^ { * } > 0$ .

Formally, let $\mathcal { X } ^ { \ast } ~ : = ~ \{ i | x _ { i } ^ { \ast } ~ > ~ 0 , i ~ \in ~ [ m ] \}$ and $\mathcal { X } ^ { \prime } : =$ $\{ i | x _ { i } ^ { * } = 0 , i \in [ m ] \}$ denote the index set of optimal basic variables and non-basic variables of $\mathbf { \boldsymbol { x } } ^ { * }$ , respectively. Then each arm $i \in \mathcal { X } ^ { * }$ is optimal arm and each arm $i \in \mathcal { X } ^ { \prime }$ is sub-optimal arm. Similarly, let $\mathcal { V } ^ { * } : = \{ j \vert b - ( \pmb { x } ^ { * } ) ^ { \top } \pmb { C } _ { j , \cdot } =$ $0 , j \in [ d ] \}$ and $\mathcal { V } ^ { \prime } : = \{ j | b - ( \pmb { x } ^ { * } ) ^ { \top } \pmb { C } _ { j , \cdot } > 0 , j \in [ d ] \}$ denote the index set of active constraints and non-active constrains of (1). Then each constraint $j \in \mathcal { V } ^ { * }$ is an active constraint and each constraint $j \in \mathcal { V } ^ { \prime }$ is a non-active constraint. Notice that we always have $| \mathcal { X } ^ { \ast } | = | \mathcal { Y } ^ { \ast } | \leq \operatorname* { m i n } \{ m , d \}$ .

Assumption 2.1. The LP (1) has a unique optimal solution. Moreover, the optimal solution is non-degenerate.

This assumption is a standard one in LP’s literature, and any LP can satisfy this assumption with an arbitrarily small perturbation (Megiddo & Chandrasekaran, 1989; Li et al., 2021). The dual problem of (1) is

$$
\min \quad \boldsymbol {b} ^ {\top} \boldsymbol {w},
$$

${ \mathrm { s . t . } } \quad C ^ { \top } { \pmb w } \geq { \pmb \mu } ,$ (2)

$$
\boldsymbol {w} \geq \mathbf {0}.
$$

Let $\boldsymbol { w } ^ { * }$ denote the optimal solution of it. Notice that for each non-active constraint $j \in \mathcal { V } ^ { \prime }$ , there is a non-basic variable $w _ { j } ^ { \ast } = 0$ .

Then we introduce the sub-optimality measure and optimality measure we use in this paper. To measure the suboptimality, we use the absolute value of reduced cost/profit $R _ { i } : = ( \pmb { w } ^ { * } ) ^ { \top } \pmb { C } . , _ { i } - \mu _ { i } , i \in [ m ]$ in LP literature and can be regarded as the cost/profit obtained for increasing a variable by a small amount. Notice that we have $R _ { i ^ { * } } = 0$ for each optimal arm $i ^ { * } \in \mathcal { X } ^ { * }$ and $R _ { i ^ { \prime } } > 0$ for each sub-optimal arm $i ^ { \prime } \in \mathcal { X } ^ { \prime }$ . To measure the optimality, consider the following linear program

$$
\max \boldsymbol {\mu} ^ {\top} \boldsymbol {x},
$$

$\mathrm { s . t . } \quad C x \leq b ,$ (3)

$$
\boldsymbol {x} \geq \mathbf {0}, x _ {i} = 0.
$$

Let $\mathrm { O P T } _ { \mathrm { L P } } ^ { - i }$ denote the optimal value of $\mathbf { i t } ,$ which adds a new constraint $x _ { i } = 0$ for one arm $i \in$ [m] compared with (1). Then define the value $G _ { i } : = \mathrm { O P T } _ { \mathrm { L P } } - \mathrm { O P T } _ { \mathrm { L P } } ^ { - i }$ , which shows the reward gap caused by one arm’s deletion. Under Assumption 2.1, we have $G _ { i ^ { \prime } } = 0$ for each sub-optimal arm $i ^ { \prime } \in \mathcal { X } ^ { \prime }$ and $G _ { i ^ { * } } > 0$ for each optimal arm $i ^ { * } \in \mathcal { X } ^ { * }$ .

# 3. BaseOAK Algorithm and Complexity Measure

This section introduces the intuition and specification of the BASEOAK algorithm (shown in Algorithm 1). We also introduce the new complexity measure. Based on this measure, we upper bound the probability that the algorithm makes mistakes.

# 3.1. BaseOAK algorithm

The algorithm splits the budget B evenly into $\lceil \log _ { 4 / 3 } m \rceil - 1$ phases and chooses the worst/best quarter of surviving arms to reject/accept at the end of each phase. An arm will be included in the final output if accepted during the time horizon, and an arm will be excluded if rejected at the end of one phase. The stop condition of BASEOAK is implied in the design of the number of phases and quarter elimination. They guarantee that BASEOAK does not exceed the budget $B$ and each arm is accepted or rejected before BASEOAK ends.

We describe the procedure of the algorithm below. The algorithm maintains three arm sets: the accept arm set $\boldsymbol { \mathcal { X } } _ { p } ^ { * }$ , the reject arm set $\mathcal { X } _ { p } ^ { \prime } ,$ and the active arm set $\mathcal { X } _ { p }$ . The accept/reject arm set includes all accepted/rejected arms before phase p, and the active arm set includes all remaining arms.

During phase $p ,$ the algorithm pulls all surviving arms $n ( p )$ times, where the definition of $n ( p )$ is given in Algorithm 1. Let $s ( p )$ denote the times of one surviving arm has been selected until the end of phase $\begin{array} { r } { p , { \mathrm { i . e . , } } s ( p ) = \sum _ { k = 0 } ^ { p } n ( k ) } \end{array}$ . Let $\bar { \pmb { \mu } } ( p )$ and $\bar { C } ( \boldsymbol { p } )$ denote the empirical mean estimator until the end of phase $p$ for $\pmb { \mu }$ and $C ,$ , respectively. Let $r _ { i } ( l )$ and $C _ { j , i } ( l )$ denote the reward and j-th resource consumption observed of the l-th pull for the arm i. Formally,

$$
\bar {\mu} _ {i} (p) = \frac {1}{s (p)} \sum_ {l = 1} ^ {s (p)} r _ {i} (l), \quad \bar {C} _ {j, i} (p) = \frac {1}{s (p)} \sum_ {l = 1} ^ {s (p)} C _ {j, i} (l).
$$

Algorithm 1 BaseOAK Algorithm (BASEOAK)   
```txt
Input: resource constraint B, number of arms m 
```

1: $\mathcal { X } _ { 0 }  [ m ] , \mathcal { X } _ { 0 } ^ { \prime }  \emptyset , \mathcal { X } _ { 0 } ^ { * }  \emptyset$   
2: for $p = 0 , \ldots , \lceil \log _ { 4 / 3 } m \rceil - 1$ do   
3: Pull each arm $i \in \ d { \mathcal { X } } _ { p } \cup \ d { \mathcal { X } } _ { p } ^ { * }$ for

$$
n (p) = \left\lfloor \frac {B}{| \mathcal {X} _ {p} \cup \mathcal {X} _ {p} ^ {*} | \lceil \log_ {4 / 3} m \rceil} \right\rfloor
$$

times

4: Compute the empirical estimator of $\bar { R } _ { i }$ and $\bar { G } _ { i }$ for each arm $i \in \mathcal { X } _ { p }$

5: if more non-basic variables in $\bar { \pmb { x } } ^ { * } ( p )$ then

6: $\mathcal X _ { p + 1 } ^ { \ast } \gets \mathcal X _ { p } ^ { \ast } \cup \big \{$ { the set of $\lceil \lvert \mathcal { X } _ { p } \rvert / 4 \rceil$ optimal arms in $\mathcal { X } _ { p }$ with the largest $\bar { G } _ { i } \}$

7: else

8: $\mathcal X _ { p + 1 } ^ { \prime }  \mathcal X _ { p } ^ { \prime } \cup \big \{$ { the set of $\lceil | \mathcal { X } _ { p } | / 4 \rceil$ sub-optimal arms in $\mathcal { X } _ { p }$ with the largest ${ { \bar { R } } _ { i } } \}$

10: $\mathscr X _ { p + 1 } \gets \mathscr X _ { 0 } \backslash ( \mathscr X _ { p + 1 } ^ { \prime } \cup \mathscr X _ { p + 1 } ^ { * } )$

11: end for

12: Output X ∗⌈log4/3 m⌉ $\mathcal { X } _ { \lceil \log _ { 4 / 3 } m \rceil } ^ { * }$

At the end of each phase p, with the empirical estimator $\bar { \pmb { \mu } } ( p )$ and $\bar { C } ( \boldsymbol { p } )$ , compute

$$
\max \quad \bar {\boldsymbol {\mu}} ^ {\top} \boldsymbol {x},
$$

$\mathrm { s . t . } \quad \bar { C } x \leq b ,$ (4)

$$
\boldsymbol {x} \geq \mathbf {0}.
$$

Let $\bar { \pmb { x } } ^ { * } ( p )$ denote the optimal solution of it. In the meantime, we compute the the empirical estimator of ${ \bar { R } } _ { i }$ and $\bar { G } _ { i }$ for each surviving $i \in \mathcal { X } _ { p } \cup \mathcal { X } _ { p } ^ { * }$ with $\bar { \pmb { \mu } } ( p )$ and $\bar { C } ( \boldsymbol { p } )$ .

If there are more non-basic variables (corresponding to the sub-optimal arms) in $\bar { \pmb { x } } ^ { * } ( p )$ , the algorithm chooses a quarter of arms with largest $\bar { R } _ { i }$ from the active arm set $\mathcal { X } _ { p }$ to reject and adds them into the reject arm set $\mathcal X _ { p + 1 } ^ { \prime }$ . Conversely, the algorithm chooses a quarter of arms with the largest $\bar { G } _ { i }$ from the active arm set $\mathcal { X } _ { p }$ to accept and adds them into the accept arm set $\boldsymbol { \mathcal { X } } _ { p + 1 } ^ { * }$ . Maybe there are some arms with the same $\bar { R } _ { i } / \bar { G } _ { i }$ such that it is difficult to decide which arm to reject/accept. We use a random strategy in this case, i.e., select a random arm to reject/accept until a quarter of the arms are eliminated. At the end of the last phase, the algorithm outputs all arms accepted during the whole time horizons.

The algorithm cannot be simplified to just eliminate and return the active set. It is important to maintain the active arm set and reject arm set simultaneously to make sure that each arm will be rejected/accepted only once during the game.

# 3.2. Complexity measure

We introduce the complexity measure used in our work. Let $\mathcal { D } = \{ x \in \mathbb { R } ^ { m } | C x \leq b , x \geq 0 \}$ denote the feasible domain of (1). Notice that D is a convex polyhedron. Let B denote the set of all vertexes (are also extreme points) of the convex polyhedron. We say $\textbf { \em x } \in \ \mathcal { D }$ is a vertex if $( \forall \lambda \in ( 0 , 1 ) , \pmb { u } , \pmb { v } \in \mathcal { D } ) [ \pmb { x } = \lambda \pmb { u } + ( 1 - \lambda ) \pmb { v } \Rightarrow \pmb { u } = \pmb { v } ]$ We use $\mathbf { \pmb { x } } _ { ( k ) }$ to denote the k-th optimal vertex, i.e.,

$$
\boldsymbol {\mu} ^ {\top} \boldsymbol {x} ^ {*} = \boldsymbol {\mu} ^ {\top} \boldsymbol {x} _ {(1)} \geq \boldsymbol {\mu} ^ {\top} \boldsymbol {x} _ {(2)} \dots
$$

$$
\geq \boldsymbol {\mu} ^ {\top} \boldsymbol {x} _ {(k)} \geq \dots \geq \boldsymbol {\mu} ^ {\top} \boldsymbol {x} _ {(| \mathcal {B} |)}.
$$

Under Assumption 2.1, the number of extreme points is no less than m. We define the vertex gap $\Delta _ { i }$ as

$$
\Delta_ {i} = \boldsymbol {\mu} ^ {\top} \boldsymbol {x} ^ {*} - \boldsymbol {\mu} ^ {\top} \boldsymbol {x} _ {(i)}, i \in [ m ].
$$

Our analysis relies on the following complexity measure:

$$
H := \max _ {i \neq 1} \frac {i}{\Delta_ {i} ^ {2}}, i \in [ m ],
$$

which is a generalization of the complexity measure for BAI. Note that the complexity measure captures the reduced cost of sub-optimal arm and the influence caused by that one of the optimal arm is not allowed to use simultaneously, and builds a bridge between point aspect (sub-optimality of arms) and global aspect (the feasible domain of latent structures of a problem instance, which could be induced from the BwK domain). We provide a formal description below.

Theorem 3.1. For any optimal arms identification or bandits with knapsack problem instance, we have $\begin{array} { r } { R _ { ( i ) } \geq \frac { \Delta _ { i + 1 } } { \sqrt { 2 } } } \end{array}$ and $G _ { ( i ) } \geq \Delta _ { i + 1 } .$ .

Proof Sketch. Let $d _ { q }$ denote the edge direction vector from $\pmb { x } ^ { * }$ leading to the adjacent extreme points $\pmb { x } ^ { ( q ) }$ corresponding to the increase of the sub-optimal variable $q \in \mathcal { X } ^ { \prime }$ . We use $\pmb { x } ^ { ( q ) }$ to denote the q-th optimal adjacent vertex, i.e. $\mu ^ { \top } \pmb { x } ^ { * } > \mu ^ { \top } \pmb { x } ^ { ( 1 ) } \geq . . . \geq \mu ^ { \top } \pmb { x } ^ { ( q ) } \geq . . . , q \in \mathcal { X } ^ { \prime }$ . We define the adjacent gap $\Delta ^ { ( q ) } : = \pmb { \mu } ^ { \top } \pmb { x } ^ { * } - \pmb { \mu } ^ { \top } \pmb { x } ^ { ( q ) } , q \in \pmb { \chi } ^ { \prime }$ . Then we consider the relationship between $\Delta ^ { ( q ) }$ and $R _ { ( q ) }$ . We rearrange $\mathbf { \Delta } \mathbf { w } ^ { * } = ( w _ { B } ^ { * } | w _ { N } ^ { * } ) ^ { \top }$ , where the basis vector $\pmb { w } _ { B } ^ { * } \in \mathbb { R } ^ { | \mathcal { V } ^ { * } | }$ includes all basic variables and the non-basis vector w $\mathbf { \Phi } _ { N } ^ { * } = ( 0 , \ldots , 0 ) ^ { \top }$ . Let $d _ { q i }$ denote the i-th element of dq. Define αq := mini∈X ∗ n −dqi $d _ { q }$ $\begin{array} { r } { \alpha _ { q } : = \operatorname* { m i n } _ { i \in \mathcal { X } ^ { * } } \left\{ \frac { \bar { \mathcal { x } } _ { i } ^ { * } } { - d _ { q i } } \right\} } \end{array}$ x ∗i We have

$$
\Delta^ {(q)} = - \alpha_ {q} \boldsymbol {\mu} ^ {\top} \boldsymbol {d} _ {q} = - \alpha_ {q} (\mu_ {q} - \left(\boldsymbol {w} _ {B} ^ {*}\right) ^ {\top} \boldsymbol {Q} _ {., q})
$$

$$
= - \alpha_ {q} (\mu_ {q} - \left(\pmb {w} ^ {*}\right) ^ {\top} \pmb {C} _ {., q}) = \alpha_ {q} R _ {(q)}
$$

From the geometry of linear programming, $\alpha _ { q }$ is the distance between the vertex $\mathbf { \boldsymbol { x } } ^ { * }$ and $\pmb { x } ^ { ( q ) }$ . And the distance of the polyhedron (i.e. the feasible domain of (1)) is not more than ${ \sqrt { 2 } }$ . From the definition of vertex gap and adjacent gap, we have $\Delta _ { q + 1 } \leq \Delta ^ { ( q ) }$ . Combine the two facts together, we obtain $\begin{array} { r } { R _ { ( i ) } \geq \frac { \Delta _ { i + 1 } } { \sqrt { 2 } } } \end{array}$ .

Then consider LP (3), notice that the feasible domain of (3) is a subset of D and the optimal extreme point of (3) is also a vertex of D. The feasible domain of (3) is nonempty because of the existence of the null arm. Under assumption 2.1, different LP (3) with different absent optimal arms have different vertex. Based on the definition of vertex gap, we could conclude that $G _ { ( i ) } \geq \Delta _ { i + 1 }$ .

The details of the proof are provided in Appendix A.

# 3.3. Theoretical result

Theorem 3.2. For the OAK problem, Algorithm 1 makes errors with probability at most

$$
O \left(m d \log m \cdot \exp \left(- \frac {b ^ {4} B}{9 0 H \max (| \mathcal {X} ^ {*} | , \log m)}\right)\right).
$$

Proof Sketch. Notice that the total pulls of BASEOAK is at most B and $c _ { i , j } ( t ) \leq 1$ for all arm i and resource $j$ during one round t, the algorithm will never exceed the consumption knapsack.

First, we argue that at the end of each phase, the optimal value of (4) is always close to $\mathrm { O P T } _ { \mathrm { L P } }$ . At the end of phase $p ,$ with probability at least 1 − 2md · exp $\left( - 2 \delta _ { p } ^ { 2 } s ( p ) \right) ,$ ), we have

$$
\bar {\boldsymbol {\mu}} ^ {\top} \bar {\boldsymbol {x}} ^ {*} (p) \geq \left(1 - \frac {\delta_ {p}}{b}\right) \mathrm{OPT} _ {\mathrm{LP}} - \delta_ {p},
$$

$$
\bar {\boldsymbol {\mu}} ^ {\top} \bar {\boldsymbol {x}} ^ {*} (p) \leq \left(1 + \frac {\delta_ {p}}{b}\right) \left(\mathrm{OPT} _ {\mathrm{LP}} - \Delta_ {2}\right) + \delta_ {p}.
$$

Then based on the analysis of the gap between the optimal solution of the dual form of (4) and $\ b { w } ^ { * }$ , we could bound the probability that $\bar { R } _ { i ^ { * } } ( p ) > \bar { R } _ { i ^ { \prime } } ( p )$ is at most

$$
2 m d \cdot \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} R _ {i ^ {\prime}}}{8}\right) ^ {2} s (p)\right).
$$

And the probability that $\bar { G } _ { i ^ { * } } ( p ) < \bar { G } _ { i ^ { \prime } } ( p )$ is at most

$$
2 m d \cdot \exp \left(- \frac {2 b ^ {2} G _ {i ^ {*}} ^ {2}}{9} s (p)\right).
$$

For all arms in $\mathcal { X } _ { p }$ , let $\mathcal { P } _ { p }$ and $\bar { \mathcal P } _ { p }$ denote the set of optimal arms for (1) and (4), $\mathcal { Q } _ { p }$ and $\bar { \mathcal { Q } } _ { p }$ denote the set of suboptimal arms for (1) and (4). Let $S _ { p } ^ { * }$ denote the $\frac { 1 } { 1 6 } | \mathcal { X } _ { p } |$ arms with smallest $G _ { i }$ and $S _ { p } ^ { \prime }$ denote the $\frac { 1 } { 1 6 } | \mathcal { X } _ { p } |$ | arms with largest $R _ { i }$ , respectively. Define

$$
\Phi_ {p} ^ {*} := \max _ {i \in \mathcal {P} _ {p} \backslash S _ {p} ^ {*}} \exp \left(- \frac {2 b ^ {2} G _ {i} ^ {2}}{9} s (p)\right),
$$

$$
\Phi_ {p} ^ {\prime} := \max _ {i \in \mathcal {Q} _ {p} \backslash S _ {p} ^ {\prime}} \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} R _ {i}}{8}\right) ^ {2} s (p)\right).
$$

Let us start with the case that $\bar { \mathcal { Q } } _ { p } > \bar { \mathcal { P } } _ { p }$ . Consider the number of arms in $\bar { \mathcal { Q } } _ { p } \cap ( \mathcal { P } _ { p } \backslash S _ { p } ^ { * } )$ , then

$$
\begin{array}{l} \mathbb {E} [ | \bar {\mathcal {Q}} _ {p} \cap (\mathcal {P} _ {p} \backslash S _ {p} ^ {*}) | ] = \sum_ {i \in \mathcal {P} _ {p} \backslash S _ {p} ^ {*}} \mathbb {P} [ \bar {G} _ {i} (p) <   \bar {G} _ {i ^ {\prime}} (p) ] \\ \leq \sum_ {i \in \mathcal {P} _ {p} \backslash S _ {p} ^ {*}} 2 m d \cdot \exp \left(- \frac {2 b ^ {2} G _ {i ^ {*}} ^ {2}}{9} s (p)\right) \\ \leq 2 m d \cdot | \mathcal {P} _ {p} \backslash S _ {p} ^ {*} | \cdot \Phi_ {p} ^ {*}. \\ \end{array}
$$

Then we apply Markov’s inequality

$$
\mathbb {P} [ | \bar {\mathcal {Q}} _ {p} \cap (\mathcal {P} _ {p} \backslash S _ {p} ^ {*}) | > \frac {1}{8} | \bar {\mathcal {Q}} _ {p} | ] \leq \frac {8 \mathbb {E} [ | \bar {\mathcal {Q}} _ {p} \cap (\mathcal {P} _ {p} \backslash S _ {p} ^ {*}) ]}{| \bar {\mathcal {Q}} _ {p} |}
$$

$$
\leq 1 6 m d \cdot \frac {| \mathcal {P} _ {p} \backslash S _ {p} ^ {*} |}{| \bar {\mathcal {Q}} _ {p} |} \Phi_ {p} ^ {*}.
$$

We could bound the cardinality of the set $\bar { \mathcal { Q } } _ { p } \cap \mathcal { Q } _ { p }$ with high probability.

$$
\mathbb {P} [ | \bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p} | > \frac {3}{4} | \bar {\mathcal {Q}} _ {p} | ] \geq 1 - 1 6 m d \cdot \frac {| \mathcal {P} _ {p} \backslash S _ {p} ^ {*} |}{| \bar {\mathcal {Q}} _ {p} |} \Phi_ {p} ^ {*}.
$$

Based on this event, let $i _ { p } ^ { * }$ denote the eliminated optimal arm in phase $p .$ Consider the the number of arms in $( \bar { \mathcal { Q } } _ { p } \cap$ $\mathcal { Q } _ { p } ) \backslash S _ { p } ^ { \prime }$ with larger $\bar { R } _ { x }$ than that of the eliminated optimal arm and let $N _ { p } ^ { \prime }$ denote it, then

$$
\begin{array}{l} \mathbb {E} [ N _ {p} ^ {\prime} ] = \sum_ {i \in (\bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p}) \setminus S _ {p} ^ {\prime}} \mathbb {P} [ \bar {R} _ {i _ {p} ^ {*}} (p) <   \bar {R} _ {i} (p) ] \\ \leq \sum_ {i \in (\bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p}) \setminus S _ {p} ^ {\prime}} 2 m d \cdot \exp \left(- \left(\frac {b \Delta_ {2}}{4 \sqrt {2}} + \frac {b ^ {2} R _ {i}}{4 \sqrt {2}}\right) ^ {2} s (p)\right) \\ \end{array}
$$

By applying Markov’s inequality, we obtain

$$
\mathbb {P} [ N _ {p} ^ {\prime} > \frac {1}{6} | \bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p} | ] \leq \frac {6 \mathbb {E} [ N _ {p} ^ {\prime} ]}{| \bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p} |}.
$$

We obtain that the probability that there is at least one eliminated optimal arms is at most

$$
3 2 m d \cdot \Phi_ {p} ^ {*} + 1 2 m d \cdot \Phi_ {p} ^ {\prime}.
$$

Similarly, the probability that at least one sub-optimal arm is added to $\mathcal { X } _ { p } ^ { \ast }$ is at most

$$
3 2 m d \cdot \Phi_ {p} ^ {\prime} + 1 2 m d \cdot \Phi_ {p} ^ {*}.
$$

Algorithm 2 FullOAK Algorithm (FULLOAK)   
Input: resource constraint B, number of arms m
1: Pull each arm once
2: while time horizon is less than T/3 and the consumption of any resource is less than B/3 do
3: for $t = 1, 2, \ldots, m$ do
4: Solve the linear program (5) and let $x_t$ denote the solution for it
5: Choose an arm to ‘pull’ as an independent sample from the distribution $x_t$ 6: end for
7: end while
8: Obtain the estimate of the optimal distribution $x_{T/3}$ .
9: $X_0 \leftarrow [m]$ , $X'_0 \leftarrow \emptyset$ , $X'_0 \leftarrow \emptyset$ 10: for $p = 0, \ldots, \lceil \log_{4/3} m \rceil - 1$ do
11: Pull each arm $i \in X_p$ for $n(p) = \left\lfloor \frac{B}{2|\mathcal{X}_p \cup \mathcal{X}_p^*| \lceil \log_{4/3} m \rceil} \right\rfloor$ times
12: Compute the empirical estimator of $\bar{R}_i$ and $\bar{G}_i$ for each arm $i \in X_p$ 13: if more non-basic variables in $\bar{x}^*(p)$ then
14: $X_{p+1}^* \leftarrow X_p^* \cup \{\text{the set of } \lceil |X_p|/4\rceil \text{ optimal arms in } X_p \text{ with the largest } \bar{G}_i\}$ 15: else
16: $X_{p+1}' \leftarrow X_p' \cup \{\text{the set of } \lceil |X_p|/4\rceil \text{ sub-optimal arms in } X_p \text{ with the largest } \bar{R}_i\}$ 17: end if
18: $X_{p+1} \leftarrow X_0 \backslash (X_{p+1}' \cup X_{p+1}^*)$ 19: end for
20: Output $X_{\lceil \log_{4/3} m \rceil}^*$

The pulls for each arm in $\mathcal { X } _ { p }$ before phase $t + 1$ satisfy

$$
\begin{array}{l} s (p) \geq \frac {B}{\log_ {4 / 3} m} \sum_ {k = 0} ^ {p} \frac {1}{| \mathcal {X} _ {p} + \mathcal {X} _ {p} ^ {*} |} \\ \geq \frac {B}{\log_ {4 / 3} m} \sum_ {k = 0} ^ {p} \min \left(\frac {2}{| \mathcal {X} _ {p} |}, \frac {2}{| \mathcal {X} _ {p} ^ {*} |}\right). \\ \end{array}
$$

Combine them together, we complete the proof. The details of the proof are provided in Appendix B.

# 4. FullOAK Algorithm and Lower Bound

This section develops an algorithm, called FULLOAK (shown in Algorithm 2), that solves the OAK problem based on some intuitions of BASEOAK. We provide the introduction, the main idea, and theoretical analysis of the algorithm. Moreover, we provide an instance-dependent lower bound for the OAK problem.

# 4.1. FullOAK algorithm

Notice that the theoretical analysis of BASEOAK show the dependence on $| { \mathcal { X } } ^ { * } |$ that the learning strategy makes mistakes for the $\mathrm { { O A K } }$ problem. The main reason is that an accurate estimator of the fixed optimal distribution suffices to guarantee algorithms with low error probability. However, BASEOAK does uniform exploration between all surviving arm during one phase, which veer widely from the optimal distribution. This also makes BASEOAK cannot delete any optimal arm during the game, so the exploration ability is limited:

$$
s (p) \leq \frac {2 B}{\log_ {4 / 3} m} \sum_ {k = 0} ^ {p} \frac {1}{| \mathcal {X} _ {p} \cup \mathcal {X} _ {p} ^ {*} |} \leq \frac {2 B}{| \mathcal {X} _ {p} ^ {*} |}.
$$

The dependence could be avoided if the algorithm obtains an accurate estimator before the reject/accept phase. Based on these analyses, we present the FULLOAK algorithm. There are two steps: the first step derived from the UCB family of algorithms and aims to converge the optimal solution of (1); the second step based on BASEOAK, the difference is that FULLOAK will delete all accept arms from the surviving arms set at the end of each phase. We provide the specification of the first step below.

Let $n _ { i } ( t )$ denote the number of pulls of arm i before round $t + 1$ . Let $\pmb { \mu } ^ { U } ( t )$ and $C ^ { L } ( t )$ denote the upper confidence bound reward vector and lower confidence bound consumption matrix until round t, respectively. Formally,

$$
\mu_ {i} ^ {U} (t) := \operatorname{proj} _ {[ 0, 1 ]} \left(\bar {\mu} _ {i} (t) + 2 f _ {r a d} \left(\bar {\mu} _ {i} (t), n _ {i} (t) + 1\right)\right),
$$

$$
C _ {j, i} ^ {L} (t) := \operatorname{proj} _ {[ 0, 1 ]} \left(\bar {C} _ {i, j} (t) - 2 f _ {\text { rad }} (\bar {C} _ {i, j} (t), n _ {i} (t) + 1)\right),
$$

where $p r o j _ { [ 0 , 1 ] }$ is a project function from real number to interval $[ 0 , 1 ]$ and $\begin{array} { r } { f _ { r a d } ( v , n ) = \sqrt { \frac { \gamma v } { n } } + \frac { \gamma } { n } , \gamma > 0 } \end{array}$ is a confidence radius function. Then after the selection of round t, consider the following linear program

$$
\begin{array}{l} \max \left(\boldsymbol {\mu} ^ {U} (t)\right) ^ {\top} \boldsymbol {x} \\ \text { s.t. } \quad C ^ {L} (t) x \leq (1 - \epsilon) b. \tag {5} \\ \boldsymbol {x} \geq \mathbf {0} \\ \end{array}
$$

The algorithm solves this linear program and selects arm according to the optimal solution of it for each round during the first step. Let $n _ { i } ( T / 3 )$ denote the pulls for arm i during the first phase. Then we obtain ${ \pmb x } _ { T / 3 }$ with

$$
(x _ {T / 3}) _ {i} = \frac {n _ {i} (T / 3)}{\sum_ {i} n _ {i} (T / 3)}.
$$

# 4.2. Theoretical result

The following theorem expresses the error bound for FUL-LOAK.

Theorem 4.1. For the OAK problem, with $\epsilon \quad = \quad$ $\begin{array} { r } { \sqrt { \frac { 3 \log ( m d T ) m } { B } } + \frac { 3 \log ( m d T ) m \log T } { B } } \end{array}$ , Algorithm 2 makes $e r \mathrm { - }$ rors with probability at most

$$
O \left(m d T \cdot \exp \left(- \frac {\alpha b ^ {2} B}{H \log m}\right)\right),
$$

where α is a constant.

Proof sketch. The upper confidence bound of the expected reward $\mu ^ { U } ( T / 3 )$ and lower confidence bound of the expected consumption $C ^ { L } ( T / 3 )$ satisfy the following properties:

(1) with probability at least $1 - 2 m d T \cdot \exp ( - \Omega ( \gamma ) )$ ,

$$
\begin{array}{l} \left| \left(\boldsymbol {\mu} ^ {U} (T / 3)\right) ^ {\top} \boldsymbol {x} _ {T / 3} - \mathrm{OPT} _ {\mathrm{LP}} \right| \\ \leq O \left(\sqrt {\frac {\gamma m \cdot \mathrm{OPT} _ {\mathrm{LP}}}{T}} + \frac {\gamma m d}{T} + \frac {\mathrm{OPT} _ {\mathrm{LP}}}{B} \sqrt {\frac {\gamma m d \cdot b}{T}}\right). \\ \end{array}
$$

(2) with probability at least 1 − 2mdT · exp(−Ω(γ)),

$$
\begin{array}{l} \sum_ {t = 1} ^ {T / 3} \left| \left(\boldsymbol {C} ^ {L} (t)\right) ^ {\top} \boldsymbol {x} _ {t} - \boldsymbol {c} _ {t} \right| \\ \leq \left(1 - O \left(\sqrt {\frac {\gamma m}{B}} + \frac {\gamma m \log T}{B}\right)\right) \frac {B \mathbf {1}}{3}. \\ \end{array}
$$

Notice that the consumption during the second step is at most $\begin{array} { l } { { \frac { B } { 2 } } } \end{array}$ , so the consumption of FULLOAK will less than $\frac { 5 B } { 6 }$ with high probability.

For the second step, at the end of phase $p ,$ for any optimal arm $i ^ { * } \in \mathcal { X } ^ { * }$ and any sub-optimal arm $i ^ { \prime } \in \mathcal { X } ^ { \prime }$ , the probability that $\bar { R } _ { i ^ { * } } ( p ) > \bar { R } _ { i ^ { \prime } } ( p )$ is at most

$$
2 m d \cdot \exp \left(- \alpha_ {1} \cdot b ^ {2} R _ {i ^ {\prime}} ^ {2} s (p)\right)
$$

for some constant $\alpha _ { 1 }$ . And the probability that $\bar { G } _ { i ^ { * } } ( p ) <$ < $\bar { G } _ { i ^ { \prime } } ( p )$ is at most

$$
2 m d \cdot \exp \left(- \frac {2 b ^ {2} G _ {i ^ {*}} ^ {2}}{9} s (p)\right).
$$

Similar to the proof of Theorem 3.2, we bound the probability that the algorithm makes mistakes by ignoring the $\frac { 1 } { 1 6 } | \mathcal { X } _ { p } |$ arms with the smallest $G _ { i }$ and the $\frac { 1 } { 1 6 } | \tilde { \mathcal { X } _ { p } } |$ arms with largest $R _ { i }$ of the active arms set, then we complete the proof. The details of the proof are provided in Appendix C. □

# 4.3. Lower bound

We provide an instance-dependent lower bound. Our analysis ensures that any bandit strategy nevertheless makes a mistake for some OAK problem instances. Our analysis also proves that our algorithm is near optimal - the lower bound matches the error probability in the exponential term up to a constant factor.

Theorem 4.2. For some OAK problem instances, consider any bandits algorithm that output an arm set ${ \mathcal { O } } \subseteq [ m ]$ ] at the end of the T -th round, it holds that

$$
\mathbb {P} (\mathcal {O} \neq \mathcal {X} ^ {*}) \geq \Omega \left(\exp \left(- \frac {\beta b ^ {2} B}{H \log m}\right)\right),
$$

where β is a constant.

Proof. We provide the core constructions below and give the detailed proof in Appendix D.

Let $( p _ { w } ) _ { 2 \le w \le W } \in [ 1 / 4 , 1 / 2 )$ be $( W - 1 )$ real numbers and let $p _ { 1 } = 1 / 2 .$ . And we define the quantities $l _ { w } : = 1 / 2 - p _ { w }$ Assume m is an exact multiple of W . Then we define

$$
\mu_ {i} := \frac {1}{2} - \frac {l _ {w}}{2 ^ {\lfloor (m - i) / W \rfloor}}, w = (i \bmod W), i \in [ m ].
$$

Let $\pi _ { i }$ denote the Bernoulli distribution of mean $\mu _ { i }$ and $\pi _ { i } ^ { \prime }$ denote the Bernoulli distribution of mean $1 - \mu _ { i }$ .

Consider W problem instances with time horizon T , m arms, d types of resources being consumed, and knapsack $b = W / m$ for each type of resource. To ease the reading, assume T is a power of 2, $W \geq \Omega ( { \sqrt { m } } )$ , and $d > m / W$ . Let w = (i mod W ), for the u-th problem instance, the i-th arm $\boldsymbol { x } _ { i } ^ { u }$ is associated with the reward distribution $\pi _ { i } ^ { u }$ ,

$$
\pi_ {i} ^ {u} := \pi_ {i} \mathbf {1} \{w \neq u \} + \pi_ {i} ^ {\prime} \mathbf {1} \{w = u \}, u \in [ W ], i \in [ m ].
$$

The consumption vector $\boldsymbol { c } _ { i } ^ { u }$ satisfies $( \pmb { c } _ { i } ^ { u } ) _ { 1 } \ = \ ( \pmb { c } _ { i } ^ { u } ) _ { d } \ =$ $( \boldsymbol { c } _ { i } ^ { u } ) _ { w } = 1$ , and $( \boldsymbol { c } _ { i } ^ { u } ) _ { j } = 0$ for all $j \neq 1 , j \neq w , j \neq d$ .

![](images/dad8c95773f7a107a40ef151c83d8a39665d1ed64cac6c11cd5d3144a7aaffbb.jpg)

# 5. Special Cases

In this section, we investigate some special cases of the OAK problem, including simple OAK problem and some classical pure exploration problems.

# 5.1. Simple OAK problem

The upper and lower bounds show the dependence on $| { \mathcal { X } } ^ { * } |$ that BASEOAK makes mistakes for the general OAK problem. The dependence could be avoided for some simple OAK problems. We say if the deletion of any optimal arm does not change $R _ { i }$ and $G _ { i }$ of any other arm, then the OAK problem is a simple OAK problem. We provide some examples of simple OAK problem in Sec. 5.2. For the simple OAK problem, we present BASEOAK− (Algorithm 3) based on BASEOAK: the algorithm eliminates the accepted arms from the active arm set at the end of each accept phase.

Theorem 5.1. For the simple OAK problem, Algorithm 3 makes errors with probability at most

$$
O \left(m ^ {2} \cdot \exp \left(- \frac {\kappa T}{H \log m}\right)\right),
$$

where κ is a constant.

![](images/33fcde0e504c432fad1c6282f03f9ec3f32590f2c3dd4cb9b8ed08ef5dafbed7.jpg)



(a) Time horizon T

![](images/243be61353edfa6b49641108cfb26dd35f088faa50ed123535f18f9ddc4c3f43.jpg)



(b) The gap ϵ

![](images/173b94b96d646d4382362bea0fd00bfc2d3360400e58edfc1df7dc0a3684c798.jpg)



(c) Per-round knapsack b   
Figure 1. Accuracy comparison in different environments.

We provide the specification of Algorithm 3 and the proof details of Theorem 5.1 in Appendix E.1.

# 5.2. Pure exploration problems

Example 5.2 (Best arm identification). The best arm identification problem can be modeled by the OAK problem with one resource (time resource) and one optimal arm. For the BAI problem, Algorithm 3 makes errors with probability at most

$$
O \left(\log m \cdot \exp \left(- \frac {\kappa T}{H \log m}\right)\right),
$$

where κ is a constant.

Notice that for the BAI problem, our complexity measure H is same as the complexity measure introduced in (Audibert et al., 2010). The result recovers the tight lower bound (Carpentier & Locatelli, 2016) up to a logarithmic factor and recovers the state-of-the-art upper bound in (Karnin et al., 2013). We provide the details of the proof in Appendix E.2.

Example 5.3 (TopK and MB problem). For any $K \in [ m ]$ , the TopK problem can be modeled by the simple OAK problem with $d = 2$ and $| { \mathcal { X } } ^ { * } | = K$ . The consumption vector for each arm is deterministic $( b , b / K ) ^ { \top }$ . Note that the number of optimal arms K is known to the learner. Let $\mathcal { P } = \{ \mathcal { X } ^ { ( 1 ) } , \ldots , \mathcal { X } ^ { ( K ) } \}$ be a partition of [m]. The MB problem with P can be modeled by the simple OAK problem with $d = K + 1$ and $| { \mathcal { X } } ^ { * } | = K$ . The deterministic consumption vector ${ C . , t o r }$ each arm $i \in \mathcal { X } ^ { ( k ) } , k \in [ K ]$ is deterministic with $( C _ { 1 , i } = b , C _ { k , i } = b / | \mathcal { X } ^ { ( k ) } | , C _ { j , i } = 0 ) [ j \neq 1 , j \neq k ]$ . Note that the number of optimal arms K and the partition P are known to the learner. For the TopK problem or the MB problem with K partitions, Algorithm 3 makes errors with probability at most

$$
O \left(m \cdot \exp \left(- \frac {\kappa T}{H \log m}\right)\right),
$$

where κ is a constant.

Notice that the multiplicative factor in Example 5.3 is $O ( m )$ while the previous upper bound is $O ( m ^ { 2 } )$ for the TopK and MB in the fixed budget setting (Bubeck et al., 2013; Chen et al., 2014). We provide the proof in Appendix E.2.

# 6. Numerical Evaluations

We consider a specific instance in which there are four arms $( m = 4 )$ , three types of resources $( d = 3 )$ , the expected per-round resource constraint of $0 < b \leq 1$ , and a parameter $0 < \epsilon \leq b .$ . The unknown reward vector is $\pmb { r } = ( 0 . 5 , 0 . 5 - \epsilon , 0 . 5 , 0 . 5 )$ , and the unknown expected resource consumption is represented by the matrix:

$$
\boldsymbol {C} = \left[ \begin{array}{c c c c} 0. 5 & 0. 5 & 0 & 0 \\ 0 & 0 & 0. 5 & 0. 5 + \epsilon \\ b & b & b & b \end{array} \right].
$$

We begin by considering the case where the knapsack $b = 0 . 2$ and the gap $\epsilon = 0 . 0 1$ . Among the available arms, the ones with indices 1 and 3 are optimal, while the rest are sub-optimal. To evaluate the performance of different algorithms, we compare the probability of outputting the index set containing all optimal arms. All results are the averages over 100 runs.

Note that the traditional regret minimization algorithms are not suitable for handling the OAK setting. This can be attributed to the fact that these algorithms rely on the ”optimism under uncertainty” principle and the associated confidence radius is often too large to explore the entire latent structure adequately. Consequently, the selection probability for “not too bad” arms remains high even when the game is ending. To compare our algorithms with traditional strategies, we propose a modification to the UcbBwK algorithm (Babaioff et al., 2015) that makes it more suitable for the OAK task. Specifically, we modify the algorithm to compute the LP based on the mean estimator after the last round and output optimal arms based on the solution. We refer to this new algorithm as ”MeanBwK.” The algorithm maintain a distribution $\mathcal { D } ^ { ( t ) }$ over arms to select arms during the times horizons, and we assume that the algorithms identify optimal arms based on the distribution of the last round, i.e., an arm i is considered optimal if and only if $\mathcal { D } _ { i } ^ { ( \tau ) } > 1 0 ^ { - 3 }$ , where τ is the index of the last round before the algorithms stop.

The results (accuracy) obtained in different environments are summarized in Figure 1. Figure 1(a) provide results for different time horizons. It is noteworthy that our algorithms outperform traditional algorithms due to their new designs tailored specifically for the OAK setting. To further evaluate the performance of our algorithms, we vary the value of ϵ while keeping $b = 0 . 2$ and $T = 2 \times 1 0 ^ { 4 }$ fixed, and present the results in Figure 1(b). Note that for smaller ϵ, algorithms are more susceptible to errors. We also investigate the impact of different values of b on the performance of our algorithms. We conduct experiments with $\epsilon = 0 . 0 1$ and $T = 2 \times 1 0 ^ { 4 }$ fixed, while also modifying the consumption to ensure that there are at least two optimal arms. The results of these experiments are presented in Figure 1(c). Based on the results, we observe that smaller values of b make it more challenging for the algorithms to identify all optimal arms, even with a longer time horizon, which is evident from the first line of the first table and the first line of the fourth table and is consistent with our theoretical analysis.

# 7. Related Work

# 7.1. Pure exploration problems

The best arm identification with the fixed budget setting was introduced by (Audibert et al., 2010). Subsequent work (Karnin et al., 2013; Carpentier & Locatelli, 2016; Chen et al., 2017c) establish the upper bound and lower bound of BAI, respectively. There are some extensions of BAI including top-K best arms identification (Kalyanakrishnan et al., 2012; Bubeck et al., 2013; Chen et al., 2017a;b; Reda´ et al., 2021; Zhou & Tian, 2022), θ-threshold arms identification (Locatelli et al., 2016; Mukherjee et al., 2017; Xu et al., 2020), ϵ-best arm identification (Kano et al., 2019; Katz-Samuels & Jamieson, 2020), multi-bandits best arms identification (Gabillon et al., 2011; Bubeck et al., 2013), and other variants (Abbasi-Yadkori et al., 2018; Rizk et al., 2021; Zhang & Ong, 2021; Zhong et al., 2021; Barrier et al., 2022; Wang et al., 2022). The Feasible Arms Identification (FAI) setting (Katz-Samuels & Scott, 2018; 2019) aims to identify all feasible (distribution have means belonging to the polyhedron) arms and top-K feasible arms, respectively, while the decision-maker aims to identify all optimal arms in the OAK problem. There are several fundamental differences between the OAK setting and the Feasible Arms Identification problem: (1) the expected reward vector µ is unknown for the OAK setting but known for the FAI setting; (2) the leaner has to consider infinite possible candidate distributions satisfy $C x \leq b$ (consumption matrix C is unknown) for the OAK setting while only needs to consider finite m distributions satisfy $\mathbf { \boldsymbol { x } } _ { i } \in \mathcal { D }$ (feasible domain D is known) for the FAI setting.

# 7.2. Bandits with knapsacks

Another line relevant to this paper is bandits with knapsacks. The regret minimization setting of stochastic BwK was first introduced and optimally solved in (Badanidiyuru et al., 2013) to encompass application domains the learner be limited by the resource constraints. Subsequent work provide a UCB-based algorithm for BwK problem (Agrawal & Devanur, 2014) and a ‘black-box reduction’ from bandits to BwK (Immorlica et al., 2019). They all achieve near-optimal worst-case regret. Some work (Flajolet & Jaillet, 2015; Sankararaman & Slivkins, 2021; Ren et al., 2021; Li et al., 2021) study the problem-dependent regret of BwK. There are some other versions of BwK including budgeted bandits (Tran-Thanh et al., 2010; 2012; Ding et al., 2013; Cayci et al., 2020; Das et al., 2022), contextual bandits with knapsacks (Badanidiyuru et al., 2014; Agrawal & Devanur, 2016; Agrawal et al., 2016; Sivakumar et al., 2022; Li & Stoltz, 2022), combinatorial semi-bandits with knapsacks (Sankararaman & Slivkins, 2018), adversarial bandits with knapsacks (Immorlica et al., 2019; Kesselheim & Singla, 2020; Castiglioni et al., 2022), other variants (Liu et al., 2022b;a; Kumar & Kleinberg, 2022), and applications (Badanidiyuru et al., 2012; Babaioff et al., 2015; Li et al., 2022). The regret minimization setting aims to trade off exploration and exploitation while the OAK setting is the pure-exploration framework. As a result, the two settings require different techniques for proving lower and upper bounds.

# 8. Conclusion

We consider the optimal arms identification with knapsacks problem, which extends the best arm identification by considering resource consumption. We present a novel, parameter-free algorithm that returns optimal arms with high probability. We propose a new complexity measure for the OAK problem, which builds a bridge between the OAK and BwK problem. We provide the error upper and lower bounds for the general OAK problem based on the new complexity measure. We further investigate some special cases and the results show that the proposed algorithm recovers or improves the state-of-the-art upper bounds for some classical pure exploration problems.

# Acknowledgments

The research is partially supported by National Key R&D Program of China under Grant No.2021ZD0110400, Innovation Program for Quantum Science and Technology 2021ZD0302900, China National Natural Science Foundation with No.62132018, No. 61932016, Pioneer and Leading Goose R&D Program of Zhejiang, 2023C01029, and the Fundamental Research Funds for the Central Universities WK2150110024.

# References

Abbasi-Yadkori, Y., Bartlett, P., Gabillon, V., Malek, A., and Valko, M. Best of both worlds: Stochastic & adversarial best-arm identification. In Conference on Learning Theory, pp. 918–949. PMLR, 2018.   
Agrawal, S. and Devanur, N. Linear contextual bandits with knapsacks. Advances in Neural Information Processing Systems, 29:3450–3458, 2016.   
Agrawal, S. and Devanur, N. R. Bandits with concave rewards and convex knapsacks. In Conference on Economics and Computation, pp. 989–1006. ACM, 2014.   
Agrawal, S., Devanur, N. R., and Li, L. An efficient algorithm for contextual bandits with knapsacks, and an extension to concave objectives. In Conference on Learning Theory, pp. 4–18. PMLR, 2016.   
Audibert, J.-Y., Bubeck, S., and Munos, R. Best arm identification in multi-armed bandits. In Conference on Learning Theory, pp. 41–53. Citeseer, 2010.   
Babaioff, M., Dughmi, S., Kleinberg, R. D., and Slivkins, A. Dynamic pricing with limited supply. ACM Trans. Economics and Comput., 3(1):4:1–4:26, 2015.   
Badanidiyuru, A., Kleinberg, R., and Singer, Y. Learning on a budget: posted price mechanisms for online procurement. In Proceedings of the 13th ACM Conference on Electronic Commerce, pp. 128–145. ACM, 2012.   
Badanidiyuru, A., Kleinberg, R., and Slivkins, A. Bandits with knapsacks. In Symposium on Foundations of Computer Science, pp. 207–216. IEEE, 2013.   
Badanidiyuru, A., Langford, J., and Slivkins, A. Resourceful contextual bandits. In Conference on Learning Theory, pp. 1109–1134. PMLR, 2014.   
Barrier, A., Garivier, A., and Kocak, T. A non-asymptotic ´ approach to best-arm identification for gaussian bandits. In International Conference on Artificial Intelligence and Statistics, volume 151, pp. 10078–10109. PMLR, 2022.   
Bubeck, S., Wang, T., and Viswanathan, N. Multiple identifications in multi-armed bandits. In International Conference on Machine Learning, pp. 258–265. PMLR, 2013.   
Carpentier, A. and Locatelli, A. Tight (lower) bounds for the fixed budget best arm identification bandit problem. In Conference on Learning Theory, pp. 590–604. PMLR, 2016.   
Castiglioni, M., Celli, A., and Kroer, C. Online learning with knapsacks: the best of both worlds. CoRR, abs/2202.13710, 2022.

Cayci, S., Eryilmaz, A., and Srikant, R. Budget-constrained bandits over general cost and reward distributions. In International Conference on Artificial Intelligence and Statistics, volume 108, pp. 4388–4398. PMLR, 2020.   
Chen, J., Chen, X., Zhang, Q., and Zhou, Y. Adaptive multiple-arm identification. In International Conference on Machine Learning, pp. 722–730. PMLR, 2017a.   
Chen, L., Li, J., and Qiao, M. Nearly instance optimal sample complexity bounds for top-k arm selection. In Artificial Intelligence and Statistics, pp. 101–110. PMLR, 2017b.   
Chen, L., Li, J., and Qiao, M. Towards instance optimal bounds for best arm identification. In Conference on Learning Theory, pp. 535–592. PMLR, 2017c.   
Chen, S., Lin, T., King, I., Lyu, M. R., and Chen, W. Combinatorial pure exploration of multi-armed bandits. In Advances in Neural Information Processing Systems, volume 27, pp. 379–387, 2014.   
Das, D., Jain, S., and Gujar, S. Budgeted combinatorial multi-armed bandits. In International Conference on Autonomous Agents and Multiagent Systems, pp. 345– 353, 2022.   
Ding, W., Qin, T., Zhang, X.-D., and Liu, T.-Y. Multiarmed bandit with budget constraint and variable costs. In Proceedings of the AAAI Conference on Artificial Intelligence, 2013.   
Flajolet, A. and Jaillet, P. Logarithmic regret bounds for bandits with knapsacks. arXiv preprint arXiv:1510.01800, 2015.   
Gabillon, V., Ghavamzadeh, M., Lazaric, A., and Bubeck, S. Multi-bandit best arm identification. Advances in Neural Information Processing Systems, 24, 2011.   
Immorlica, N., Sankararaman, K. A., Schapire, R., and Slivkins, A. Adversarial bandits with knapsacks. In Symposium on Foundations of Computer Science, pp. 202– 219. IEEE, 2019.   
Kalyanakrishnan, S., Tewari, A., Auer, P., and Stone, P. Pac subset selection in stochastic multi-armed bandits. In International Conference on Machine Learning, volume 12, pp. 655–662, 2012.   
Kano, H., Honda, J., Sakamaki, K., Matsuura, K., Nakamura, A., and Sugiyama, M. Good arm identification via bandit feedback. Machine Learning, 108(5):721–745, 2019.   
Karnin, Z., Koren, T., and Somekh, O. Almost optimal exploration in multi-armed bandits. In International Conference on Machine Learning, pp. 1238–1246. PMLR, 2013.

Katz-Samuels, J. and Jamieson, K. The true sample complexity of identifying good arms. In International Conference on Artificial Intelligence and Statistics, pp. 1781– 1791. PMLR, 2020.   
Katz-Samuels, J. and Scott, C. Feasible arm identification. In International Conference on Machine Learning, pp. 2535–2543. PMLR, 2018.   
Katz-Samuels, J. and Scott, C. Top feasible arm identification. In International Conference on Artificial Intelligence and Statistics, pp. 1593–1601. PMLR, 2019.   
Kesselheim, T. and Singla, S. Online learning with vector costs and bandits with knapsacks. In Conference on Learning Theory, pp. 2286–2305. PMLR, 2020.   
Kleinberg, R., Slivkins, A., and Upfal, E. Multi-armed bandits in metric spaces. In Dwork, C. (ed.), Symposium on Theory of Computing, pp. 681–690. ACM, 2008.   
Kumar, R. and Kleinberg, R. Non-monotonic resource utilization in the bandits with knapsacks problem. In Advances in Neural Information Processing Systems, 2022.   
Li, S., Zhang, L., and Li, X. Online pricing with limited supply and time-sensitive valuations. In IEEE Conference on Computer Communications, pp. 860–869. IEEE, 2022.   
Li, X., Sun, C., and Ye, Y. The symmetry between arms and knapsacks: A primal-dual approach for bandits with knapsacks. In International Conference on Machine Learning, pp. 6483–6492. PMLR, 2021.   
Li, Z. and Stoltz, G. Contextual bandits with knapsacks for a conversion model. In Advances in Neural Information Processing Systems, 2022.   
Liu, Q., Xu, W., Wang, S., and Fang, Z. Combinatorial bandits with linear constraints: Beyond knapsacks and fairness. In Advances in Neural Information Processing Systems, 2022a.   
Liu, S., Jiang, J., and Li, X. Non-stationary bandits with knapsacks. In Advances in Neural Information Processing Systems, 2022b.   
Locatelli, A., Gutzeit, M., and Carpentier, A. An optimal algorithm for the thresholding bandit problem. In International Conference on Machine Learning, pp. 1690–1698. PMLR, 2016.   
Megiddo, N. and Chandrasekaran, R. On the ε-perturbation method for avoiding degeneracy. Operations Research Letters, 8(6):305–308, 1989.   
Mukherjee, S., Naveen, K. P., Sudarsanam, N., and Ravindran, B. Thresholding bandits with augmented ucb. arXiv preprint arXiv:1704.02281, 2017.

Reda, C., Kaufmann, E., and Delahaye-Duriez, A. Top-m ´ identification for linear bandits. In International Conference on Artificial Intelligence and Statistics, volume 130, pp. 1108–1116. PMLR, 2021.   
Ren, W., Liu, J., and Shroff, N. B. On logarithmic regret for bandits with knapsacks. In Conference on Information Sciences and Systems, pp. 1–6. IEEE, 2021.   
Rizk, G., Thomas, A., Colin, I., Laraki, R., and Chevaleyre, Y. Best arm identification in graphical bilinear bandits. In International Conference on Machine Learning, pp. 9010–9019. PMLR, 2021.   
Sankararaman, K. A. and Slivkins, A. Combinatorial semibandits with knapsacks. In International Conference on Artificial Intelligence and Statistics, pp. 1760–1770. PMLR, 2018.   
Sankararaman, K. A. and Slivkins, A. Bandits with knapsacks beyond the worst case. Advances in Neural Information Processing Systems, 34, 2021.   
Sivakumar, V., Zuo, S., and Banerjee, A. Smoothed adversarial linear contextual bandits with knapsacks. In International Conference on Machine Learning, volume 162, pp. 20253–20277. PMLR, 2022.   
Tran-Thanh, L., Chapman, A., De Cote, E. M., Rogers, A., and Jennings, N. R. Epsilon–first policies for budget– limited multi-armed bandits. In Proceedings of the AAAI Conference on Artificial Intelligence, 2010.   
Tran-Thanh, L., Chapman, A., Rogers, A., and Jennings, N. Knapsack based optimal policies for budget–limited multi–armed bandits. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 26, pp. 1134–1140, 2012.   
Wang, Z., Wagenmaker, A. J., and Jamieson, K. G. Best arm identification with safety constraints. In International Conference on Artificial Intelligence and Statistics, volume 151 of Proceedings of Machine Learning Research, pp. 9114–9146. PMLR, 2022.   
Xu, Y., Chen, X., Singh, A., and Dubrawski, A. Thresholding bandit problem with both duels and pulls. In International Conference on Artificial Intelligence and Statistics, pp. 2591–2600. PMLR, 2020.   
Zhang, M. and Ong, C. S. Quantile bandits for best arms identification. In International Conference on Machine Learning, pp. 12513–12523. PMLR, 2021.   
Zhong, Z., Cheung, W. C., and Tan, V. Probabilistic sequential shrinking: A best arm identification algorithm for stochastic bandits with corruptions. In International Conference on Machine Learning, pp. 12772–12781. PMLR, 2021.

Zhou, R. and Tian, C. Approximate top-m arm identification with heterogeneous reward variances. In International Conference on Artificial Intelligence and Statistics, volume 151 of Proceedings of Machine Learning Research, pp. 7483–7504. PMLR, 2022.

# A. Analysis of Complexity Measure (Theorem 3.1)

After removing all non-active constraints of (1), we can get a standard form LP. Formally, base on the matrix $^ { C , }$ by arranging the $| { \mathcal { X } } ^ { * } |$ basic columns and $| \mathcal { V } ^ { * } |$ active rows next to each other, we obtain a $| \mathcal { V } ^ { * } | \times | \mathcal { X } ^ { * } |$ optimal basis matrix corresponding to $\pmb { x } ^ { * }$ and let P denote the basis matrix. Similarly, by arranging the $| { \mathcal { X } } ^ { \prime } |$ non-basic columns and $| \mathcal { V } ^ { * } |$ active rows next to each other, we obtain a $| \mathcal { V } ^ { * } | \times | \mathcal { X } ^ { \prime } |$ non-basis matrix and let $Q$ denote it. Then we could construct a matrix $A : = [ P | Q ]$ with $| { \mathcal { X } } ^ { * } |$ linearly independent columns (rows). We use $\boldsymbol { b } ^ { * }$ to denote the vector $( b , \dots , b ) ^ { \top } \in ( 0 , 1 ] ^ { | \mathcal { X } ^ { * } | }$ . Then the standard form LP is

$$
\begin{array}{l} \max \quad \boldsymbol {\mu} ^ {\top} \boldsymbol {x}, \tag {6} \\ \text { s.t. } \quad A x = b ^ {*}, x \geq 0. \\ \end{array}
$$

It is oblivious that (1) and (6) have same feasible domain D, optimal solution $\pmb { x } ^ { * }$ , and optimal value $\mathrm { O P T _ { L P } }$ . The dual problem of (6) is

$$
\min \quad (\boldsymbol {b} ^ {*}) ^ {\top} \boldsymbol {w},
$$

$$
\text { s.t. } \quad A ^ {\top} w \geq \mu , w \geq 0.
$$

And $\pmb { w } _ { B } ^ { * }$ is the optimal solution of it. We define a new $m \times m$ square matrix:

$$
M := \left[ \begin{array}{c c} P & Q \\ 0 & I \end{array} \right].
$$

We use I to denote the identity matrix. We also get the inverse of M :

$$
M ^ {- 1} := \left[ \begin{array}{c c} P ^ {- 1} & - P ^ {- 1} Q \\ 0 & I \end{array} \right].
$$

Define a m dimension vector

$$
\boldsymbol {d} _ {q} := (M ^ {- 1}) _ {., q}, q \in \mathcal {X} ^ {\prime}.
$$

Notice that $\pmb { x } ^ { * }$ is the optimal extreme point in D. Under the Assumption 2.1, there are $| { \mathcal { X } } ^ { \prime } |$ neighbors of $\mathbf { \boldsymbol { x } } ^ { * }$ . And $d _ { q }$ is the edge direction from $\mathbf { \boldsymbol { x } } ^ { * }$ leading to the adjacent extreme points $\pmb { x } ^ { ( q ) }$ corresponding to the increase of the sub-optimal variable $q \in \mathcal { X } ^ { \prime }$ . We use $\pmb { x } ^ { ( q ) }$ to denote the q-th optimal adjacent vertex, i.e.,

$$
\boldsymbol {\mu} ^ {\top} \boldsymbol {x} ^ {*} > \boldsymbol {\mu} ^ {\top} \boldsymbol {x} ^ {(1)} \geq \dots \geq \boldsymbol {\mu} ^ {\top} \boldsymbol {x} ^ {(q)} \geq \dots , q \in \mathcal {X} ^ {\prime}.
$$

We define the adjacent gap $\Delta ^ { ( q ) }$ as

$$
\Delta^ {(q)} = \boldsymbol {\mu} ^ {\top} \boldsymbol {x} ^ {*} - \boldsymbol {\mu} ^ {\top} \boldsymbol {x} ^ {(q)}, q \in \mathcal {X} ^ {\prime}.
$$

Then consider the relationship between $\Delta ^ { ( q ) }$ and $R _ { ( q ) }$ . Let $d _ { q i }$ denote the i-th element of $d _ { q }$ . Define

$$
\alpha_ {q} = \min _ {i \in \mathcal {X} ^ {*}} \left\{\frac {x _ {i} ^ {*}}{- d _ {q i}} \right\},
$$

we have

$$
\begin{array}{l} \Delta^ {(q)} = - \alpha_ {q} \pmb {\mu} ^ {\top} \pmb {d} _ {q} = - \alpha_ {q} (\mu_ {q} - (\pmb {w} _ {B} ^ {*}) ^ {\top} \pmb {Q} _ {., q}) \\ = - \alpha_ {q} (\mu_ {q} - \left(\boldsymbol {w} ^ {*}\right) ^ {\top} \boldsymbol {C} _ {., q}) = \alpha_ {q} R _ {(q)}. \\ \end{array}
$$

From the geometry of linear programming, $\alpha _ { q }$ is the distance between the vertex √ $\pmb { x } ^ { * }$ and $\pmb { x } ^ { ( q ) }$ . The distance of the polyhedron (i.e., the feasible domain of (1)) will be not more than $\sqrt { 2 }$ . From the definition of vertex gap and adjacent gap, we have $\Delta _ { q + 1 } \leq \Delta ^ { ( q ) }$ . Combine the two facts together, we obtain $\begin{array} { r } { R _ { ( i ) } \geq \frac { \Delta _ { i + 1 } } { \sqrt { 2 } } } \end{array}$

Then consider LP (3), notice that the feasible domain of (3) is a subset of D and the optimal extreme point of (3) is also a vertex of D. The feasible domain of (3) is nonempty because of the existence of null arms. Under Assumption 2.1, different LP (3) with different absent optimal arms have different vertex. Based on the definition of vertex gap, we could conclude that $G _ { ( i ) } \geq \Delta _ { i + 1 }$ .

# B. Analysis of Algorithm 1 (Theorem 3.2)

In this section, we analyze the probability bound of Algorithm 1 and prove Theorem 3.2.

# B.1. Main lemmas

Lemma B.1. At the end of phase p, for the optimal value of (4), if the algorithm makes no errors before the beginning of phase p, with probability at least 1 − 2md · exp $\left( - 2 \delta _ { p } ^ { 2 } s ( p ) \right) ,$ ), we have

$$
\bar {\boldsymbol {\mu}} ^ {\top} \bar {\boldsymbol {x}} ^ {*} (p) \geq \left(1 - \frac {\delta_ {p}}{b}\right) \mathrm{OPT} _ {\mathrm{LP}} - \delta_ {p}.
$$

Proof. According to the Hoeffding’s inequality, with probability at least $1 - 2 m d \cdot \exp \left( - 2 \delta _ { p } ^ { 2 } s ( p ) \right)$ , for all optimal arms $i ^ { * }$ and all active constraints $j ^ { * }$ in (1) and (4), we have

$$
\max (\mu_ {i ^ {*}} - \delta_ {p}, 0) \leq \bar {\mu} _ {i ^ {*}} (p) \leq \min (1, \mu_ {i ^ {*}} + \delta_ {p}),
$$

$$
\max (C _ {j ^ {*}, i ^ {*}} - \delta_ {p}, 0) \leq \bar {C} _ {j ^ {*}, i ^ {*}} (p) \leq \min (1, C _ {j ^ {*}, i ^ {*}} + \delta_ {p}).
$$

Under this event, consider the following linear program

$$
\begin{array}{l} \max \quad \boldsymbol {\mu} ^ {\top} \boldsymbol {x}, \\ \text { s.t. } \quad \boldsymbol {x} ^ {\top} \boldsymbol {C} _ {j, \cdot} ^ {\top} \leq b - \delta_ {p}, \forall j \in [ d ], \\ \boldsymbol {x} \geq 0. \\ \end{array}
$$

Let $\boldsymbol { x } ^ { * } ( \boldsymbol { b } ^ { L } )$ and $\mathrm { O P T } _ { \mathrm { L P } } (  { \boldsymbol { b } } ^ { L } )$ denote the optimal solution and optimal value of it, respectively. According to (Agrawal & Devanur, 2014), we have

$$
\mathrm{OPT} _ {\mathrm{LP}} \left(\boldsymbol {b} ^ {L}\right) \geq \left(1 - \frac {\delta_ {p}}{b}\right) \mathrm{OPT} _ {\mathrm{LP}}.
$$

Then we show that $\boldsymbol { x } ^ { * } ( \boldsymbol { b } ^ { L } )$ is also a feasible solution for $L P ( \bar { \mu } , \bar { C } )$ of phase p. Consider the j-th resource

$$
\begin{array}{l} \sum_ {i = 1} ^ {m} \bar {C} _ {j, i} x _ {i} ^ {*} (\boldsymbol {b} ^ {L}) \\ = \sum_ {i = 1} ^ {m} (\bar {C} _ {j, i} - C _ {j, i}) x _ {i} ^ {*} (\boldsymbol {b} ^ {L}) + \sum_ {i = 1} ^ {m} C _ {j, i} x _ {i} ^ {*} (\boldsymbol {b} ^ {L}) \\ \leq \max _ {i \in [ m ]} \left(\bar {C} _ {j, i} - C _ {j, i}\right) + (b - \delta_ {p}) \\ \leq b. \\ \end{array}
$$

With this feasibility, we have

$$
\begin{array}{l} \bar {\boldsymbol {\mu}} ^ {\top} \boldsymbol {x} ^ {*} (\boldsymbol {b} ^ {L}) \\ = \boldsymbol {\mu} ^ {\top} \boldsymbol {x} ^ {*} (\boldsymbol {b} ^ {L}) - \left(\boldsymbol {\mu} ^ {\top} \boldsymbol {x} ^ {*} (\boldsymbol {b} ^ {L}) - \bar {\boldsymbol {\mu}} ^ {\top} \boldsymbol {x} ^ {*} (\boldsymbol {b} ^ {L})\right) \\ \geq \mathrm{OPT} _ {\mathrm{LP}} (\boldsymbol {b} ^ {L}) - \left\| \boldsymbol {\mu} ^ {\top} - \bar {\boldsymbol {\mu}} ^ {\top} \right\| _ {\infty} \cdot \left\| \boldsymbol {x} ^ {*} (\boldsymbol {b} ^ {L}) \right\| _ {1} \\ \geq \left(1 - \frac {\delta_ {p}}{b}\right) \mathrm{OPT} _ {\mathrm{LP}} - \delta_ {p}. \\ \end{array}
$$

Then we get

$$
\bar {\boldsymbol {\mu}} ^ {\top} \bar {\boldsymbol {x}} ^ {*} (p) \geq \bar {\boldsymbol {\mu}} ^ {\top} \boldsymbol {x} ^ {*} (\boldsymbol {b} ^ {L}) \geq \left(1 - \frac {\delta_ {p}}{b}\right) \mathrm{OPT} _ {\mathrm{LP}} - \delta_ {p}.
$$

Lemma B.2. At the end of phase p, for the optimal value of (4), if one of optimal arms is not active in $\bar { \pmb { x } } ^ { * } ( p )$ , with probability at least $1 - 2 m d \cdot \exp \left( - 2 \delta _ { p } ^ { 2 } s ( p ) \right) ,$ ), we have

$$
\bar {\boldsymbol {\mu}} ^ {\top} \bar {\boldsymbol {x}} ^ {*} (p) \leq \left(1 + \frac {\delta_ {p}}{b}\right) \left(\mathrm{OPT} _ {\mathrm{LP}} - \Delta_ {2}\right) + \delta_ {p}.
$$

Proof. According to Theorem 3.1, for any arm $i \in [ m ]$ , we have

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {- i} \leq \mathrm{OPT} _ {\mathrm{LP}} - \Delta_ {2}. \tag {7}
$$

According to the Hoeffding’s inequality, with probability at least $1 - 2 m d \cdot \exp \left( - 2 \delta _ { p } ^ { 2 } s ( p ) \right)$ , for all optimal arms $i ^ { * }$ and all active constraints $j ^ { * }$ in (1) and (4), we have

$$
\max \left(\mu_ {i ^ {*}} - \delta_ {p}, 0\right) \leq \bar {\mu} _ {i ^ {*}} (p) \leq \min \left(1, \mu_ {i ^ {*}} + \delta_ {p}\right),
$$

$$
\max \left(C _ {j ^ {*}, i ^ {*}} - \delta_ {p}, 0\right) \leq \bar {C} _ {j ^ {*}, i ^ {*}} (p) \leq \min \left(1, C _ {j ^ {*}, i ^ {*}} + \delta_ {p}\right).
$$

Under this event, assume one of the optimal arm $i ^ { * } \in \mathcal { X } ^ { * }$ is eliminated in round t. Consider the following linear program

$$
\max \quad \boldsymbol {\mu} ^ {\top} \boldsymbol {x},
$$

$$
\text { s.t. } \quad \boldsymbol {x} ^ {\top} \boldsymbol {C} _ {j, \cdot} ^ {\top} \leq b + \delta_ {p}, \forall j \in [ d ], \tag {8}
$$

$$
\boldsymbol {x} \geq \mathbf {0}, x _ {i ^ {*}} = 0.
$$

Let ${ \pmb x } ^ { - i * } ( { \pmb b } ^ { U } )$ and $\mathrm { O P T } _ { \mathrm { L P } } ^ { i ^ { * } } ( \boldsymbol { b } ^ { U } )$ denote the optimal solution and optimal value of it, respectively. According to (Agrawal & Devanur, 2014), we have

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {i ^ {*}} \geq \frac {b}{b + \delta_ {p}} \mathrm{OPT} _ {\mathrm{LP}} ^ {i ^ {*}} (\boldsymbol {b} ^ {U}).
$$

Combine it with Theorem 3.1, we get

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {i ^ {*}} \left(\boldsymbol {b} ^ {U}\right) \leq \left(1 + \frac {\delta_ {p}}{b}\right) \left(\mathrm{OPT} _ {\mathrm{LP}} - \Delta_ {2}\right).
$$

Then we show that $\bar { \pmb { x } } ^ { * } ( p )$ is also a feasible solution for (8) of phase p. Consider the j-th resource

$$
\begin{array}{l} \sum_ {i = 1} ^ {m} C _ {j, i} \bar {x} _ {i} ^ {*} (p) \\ = \sum_ {i = 1} ^ {m} (C _ {j, i} - \bar {C} _ {j, i}) \bar {x} _ {i} ^ {*} (p) + \sum_ {i = 1} ^ {m} \bar {C} _ {j, i} \bar {x} _ {i} ^ {*} (p) \\ \leq \max _ {i \in [ m ]} \left(C _ {j, i} - \bar {C} _ {j, i}\right) + b \\ \leq b + \delta_ {p}. \\ \end{array}
$$

With this feasibility, we have

$$
\begin{array}{l} \bar {\boldsymbol {\mu}} ^ {\top} \bar {\boldsymbol {x}} ^ {*} (p) \\ = \boldsymbol {\mu} ^ {\top} \bar {\boldsymbol {x}} ^ {*} (p) + \left(\bar {\boldsymbol {\mu}} ^ {\top} \bar {\boldsymbol {x}} ^ {*} (p) - \boldsymbol {\mu} ^ {\top} \bar {\boldsymbol {x}} ^ {*} (p)\right) \\ \leq \mathrm{OPT} _ {\mathrm{LP}} ^ {i ^ {*}} (\boldsymbol {b} ^ {U}) + \left\| \bar {\boldsymbol {\mu}} ^ {\top} - \boldsymbol {\mu} ^ {\top} \right\| _ {\infty} \cdot \| \bar {\boldsymbol {x}} ^ {*} (p) \| _ {1} \\ \leq \left(1 + \frac {\delta_ {p}}{b}\right) \left(\mathrm{OPT} _ {\mathrm{LP}} - \Delta_ {2}\right) + \delta_ {p}. \\ \end{array}
$$

Then we complete the proof.

Lemma B.3. At the end of phase $p ,$ for any optimal arm $i ^ { * } \in \mathcal { X } ^ { * }$ and any active sub-optimal arm $i ^ { \prime } \in \mathcal { X } ^ { \prime } \cap \mathcal { X } _ { p } ,$ the probability that $\bar { R } _ { i ^ { * } } ( p ) > \bar { R } _ { i ^ { \prime } } ( p )$ is at most

$$
2 m d \cdot \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} R _ {i ^ {\prime}}}{8}\right) ^ {2} s (p)\right).
$$

Proof. Consider the dual form

$$
\begin{array}{l} \min \quad \boldsymbol {b} ^ {\top} \boldsymbol {w}, \\ \text { s.t. } \quad \bar {\boldsymbol {C}} ^ {\top} \boldsymbol {w} \geq \bar {\boldsymbol {\mu}}, \boldsymbol {w} \geq \mathbf {0}. \\ \end{array}
$$

Let $\bar { \pmb { w } } ^ { * } ( p )$ denote the optimal solution of it, according to Lemma B.1 and B.2, we have

$$
\left(1 - \frac {\delta_ {p}}{b}\right) \boldsymbol {b} ^ {\top} \boldsymbol {w} ^ {*} - \delta_ {p} \leq \boldsymbol {b} ^ {\top} \bar {\boldsymbol {w}} ^ {*} (p) \leq \left(1 + \frac {\delta_ {p}}{b}\right) \left(\boldsymbol {b} ^ {\top} \boldsymbol {w} ^ {*} - \Delta_ {2}\right) + \delta_ {p}.
$$

Then we get

$$
\sum_ {j = 1} ^ {d} \left(\bar {w} ^ {*} (p)\right) _ {j} - \sum_ {j = 1} ^ {d} w _ {j} ^ {*} \geq - \frac {\delta_ {p}}{b} \left(1 + \sum_ {j = 1} ^ {d} w _ {j} ^ {*}\right), \tag {9}
$$

$$
\sum_ {j = 1} ^ {d} \left(\bar {w} ^ {*} (p)\right) _ {j} - \sum_ {j = 1} ^ {d} w _ {j} ^ {*} \leq \frac {\delta_ {p}}{b} \left(\sum_ {j = 1} ^ {d} w _ {j} ^ {*} - \frac {\Delta_ {2}}{b}\right) + \frac {\delta_ {p} - \Delta_ {2}}{b}.
$$

Consider the $R _ { i }$ of $i ^ { * }$ and $i ^ { \prime }$

$$
R _ {i ^ {*}} = \left(\boldsymbol {w} ^ {*}\right) ^ {\top} \boldsymbol {C} _ {i ^ {*}} - \mu_ {i ^ {*}} \quad \leq 0,
$$

$$
\bar {R} _ {i ^ {*}} = \left(\bar {\boldsymbol {w}} ^ {*} (p)\right) ^ {\top} \bar {\boldsymbol {C}} _ {i ^ {*}} - \bar {\mu} _ {i ^ {*}} > 0, \tag {10}
$$

$$
\bar {R} _ {i ^ {\prime}} = \left(\bar {\boldsymbol {w}} ^ {*} (p)\right) ^ {\top} \bar {\boldsymbol {C}} _ {i ^ {\prime}} - \bar {\mu} _ {i ^ {\prime}} <   \bar {R} _ {i ^ {*}}.
$$

From (21) and (22), we have

$$
\begin{array}{l} \sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} \bar {C} _ {j, i ^ {*}} - \bar {\mu} _ {i ^ {*}} \\ \leq \sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} \left(C _ {j, i ^ {*}} + \delta_ {p}\right) - \left(\mu_ {i ^ {*}} - \delta_ {p}\right) \\ = \sum_ {j = 1} ^ {d} w _ {j} ^ {*} (C _ {j, i ^ {*}} + \delta_ {p}) - \left[ \sum_ {j = 1} ^ {d} w _ {j} ^ {*} (C _ {j, i ^ {*}} + \delta_ {p}) - \sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} (C _ {j, i ^ {*}} + \delta_ {p}) \right] - (\mu_ {i ^ {*}} - \delta_ {p}) \\ \leq \sum_ {j = 1} ^ {d} w _ {j} ^ {*} (C _ {j, i ^ {*}} + \delta_ {p}) + \frac {\delta_ {p}}{b} \left(\sum_ {j = 1} ^ {d} w _ {j} ^ {*} - \frac {\Delta_ {2}}{b}\right) + \frac {\delta_ {p} - \Delta_ {2}}{b} - (\mu_ {i ^ {*}} - \delta_ {p}) \\ \leq \left(\delta_ {p} + \frac {\delta_ {p}}{b}\right) \left(1 + \sum_ {j = 1} ^ {d} w _ {j} ^ {*}\right) - \frac {\Delta_ {2}}{b} - \frac {\delta_ {p} \Delta_ {2}}{b ^ {2}}. \\ \end{array}
$$

And

$$
\begin{array}{l} \sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} \bar {C} _ {j, i ^ {\prime}} - \bar {\mu} _ {i ^ {\prime}} \\ \geq \sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} (C _ {j, i ^ {\prime}} - \delta_ {p}) - (\mu_ {i ^ {\prime}} + \delta_ {p}) \\ = \sum_ {j = 1} ^ {d} w _ {j} ^ {*} (C _ {j, i ^ {\prime}} - \delta_ {p}) - \left[ \sum_ {j = 1} ^ {d} w _ {j} ^ {*} (C _ {j, i ^ {*}} - \delta_ {p}) - \sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} (C _ {j, i ^ {*}} - \delta_ {p}) \right] - (\mu_ {i ^ {\prime}} + \delta_ {p}) \\ \geq \sum_ {j = 1} ^ {d} w _ {j} ^ {*} (C _ {j, i ^ {\prime}} - \delta_ {p}) - \frac {\delta_ {p}}{b} \left(1 + \sum_ {j = 1} ^ {d} w _ {j} ^ {*}\right) - (\mu_ {i ^ {\prime}} + \delta_ {p}) \\ \geq R _ {i ^ {\prime}} - \left(\delta_ {p} + \frac {\delta_ {p}}{b}\right) \left(1 + \sum_ {j = 1} ^ {d} w _ {j} ^ {*}\right). \\ \end{array}
$$

According to the Strong duality theorem, we have

$$
\sum_ {j = 1} ^ {d} w _ {j} ^ {*} = \frac {1}{b} \sum_ {i = 1} ^ {m} \mu_ {i} x _ {i} ^ {*} = \frac {1}{b} \mathrm{OPT} _ {\mathrm{LP}} \leq \frac {1}{b}.
$$

From the Hoeffding’s inequality, Lemma B.1 and B.2, we have

$$
\begin{array}{l} \mathbb {P} [ \bar {R} _ {i ^ {*}} (p) > \bar {R} _ {i ^ {\prime}} (p) ] \\ \leq \mathbb {P} \left[ \frac {\Delta_ {2}}{b} + \frac {\delta_ {p} \Delta_ {2}}{b ^ {2}} + R _ {i ^ {\prime}} <   2 \left(\delta_ {p} + \frac {\delta_ {p}}{b}\right) \left(1 + \sum_ {j = 1} ^ {d} w _ {j} ^ {*}\right) \right] \\ \leq \mathbb {P} \left[ \frac {\Delta_ {2}}{b} + R _ {i ^ {\prime}} <   2 \delta_ {p} \left(1 + \frac {1}{b}\right) ^ {2} \right] \\ \leq 2 m d \cdot \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} R _ {i ^ {\prime}}}{8}\right) ^ {2} s (p)\right). \\ \end{array}
$$

Then we complete the proof.

![](images/052c256f21b0c289d177e3c67f8ae02c31d81939e5301c34d21050f13a2725f2.jpg)

Lemma B.4. During phase $p ,$ for any optimal arm $i ^ { * } \in \mathcal { X } ^ { * }$ and any active sub-optimal arm $i ^ { \prime } \in \mathcal { X } ^ { \prime } \cap \mathcal { X } _ { p } ,$ , the probability that $\bar { G } _ { i ^ { * } } ( p ) < \bar { G } _ { i ^ { \prime } } ( p )$ is at most

$$
2 m d \cdot \exp \left(- \frac {2 b ^ {2} G _ {i ^ {*}} ^ {2}}{9} s (p)\right).
$$

Proof. During phase $p ,$ for each arm $i \in [ m ]$ , consider the linear programming

$$
\begin{array}{l} \max \quad \bar {\boldsymbol {\mu}} ^ {\top} \boldsymbol {x}, \\ \text { s.t. } \quad \bar {C} x \leq b, \\ \boldsymbol {x} \geq \mathbf {0}, x _ {i} = 0. \\ \end{array}
$$

Let $\overline { { \mathrm { O P T } } } _ { \mathrm { L P } } ^ { - i }$ denote the optimal value of it. According to Lemma B.1 and the proof of Lemma B.2, with probability at least $1 - 2 | \bar { \mathcal { P } } _ { p } ^ { \mathrm { ~ \scriptsize ~ \stackrel { - } { \cup } ~ } } \mathcal { P } _ { p } \cup \mathcal { X } _ { p } ^ { * } | ^ { 2 } \cdot \exp \left( - 2 \delta _ { p } ^ { 2 } s ( p ) \right)$ , we have

$$
\begin{array}{l} \overline {{\mathrm{OPT}}} _ {\mathrm{LP}} ^ {- i ^ {\prime}} \geq \left(1 - \frac {\delta_ {p}}{b}\right) \mathrm{OPT} _ {\mathrm{LP}} - \delta_ {p}, \\ \overline {{\mathrm{OPT}}} _ {\mathrm{LP}} ^ {- i ^ {*}} \leq \left(1 + \frac {\delta_ {p}}{b}\right) \left(\mathrm{OPT} _ {\mathrm{LP}} - G _ {i *}\right) + \delta_ {p}. \\ \end{array}
$$

Then we have

$$
\begin{array}{l} \mathbb {P} [ \bar {G} _ {i *} (p) <   \bar {G} _ {i ^ {\prime}} (p) ] \\ \leq \mathbb {P} \left[ \left(1 + \frac {\delta_ {p}}{b}\right) \left(\mathrm{OPT} _ {\mathrm{LP}} - G _ {i ^ {*}}\right) + \delta_ {p} \geq \left(1 - \frac {\delta_ {p}}{b}\right) \mathrm{OPT} _ {\mathrm{LP}} - \delta_ {p} \right] \\ \leq \mathbb {P} \left[ \left(1 + \frac {2 (\mathrm{OPT} _ {\mathrm{LP}} - G _ {i ^ {*}})}{b}\right) \delta_ {p} \geq G _ {i ^ {*}} \right] \\ \leq 2 m d \cdot \exp \left(- \frac {2 b ^ {2} G _ {i ^ {*}} ^ {2}}{9} s (p)\right). \\ \end{array}
$$

# B.2. Proof of Theorem 3.2

For all arms in $\mathcal { X } _ { p }$ , let $\mathcal { P } _ { p }$ and $\bar { \mathcal P } _ { p }$ denote the set of optimal arms for (1) and $( 4 ) , \mathcal { Q } _ { p }$ and $\bar { \mathcal { Q } } _ { p }$ denote the set of sub-optimal arms for (1) and (4), respectively. Consider the first phase $p$ such that there is at least one eliminated optimal arm or one sub-optimal arm is added to $\boldsymbol { \mathcal { X } } _ { p } ^ { * }$ . Let $S _ { p } ^ { * }$ denote the $\frac { 1 } { 1 6 } | \mathcal { X } _ { p } |$ arms with smallest $G _ { i }$ and $S _ { p } ^ { \prime }$ denote the $\frac { 1 } { 1 6 } | \mathcal { X } _ { p } |$ arms with largest $R _ { i }$ , respectively. Define

$$
\begin{array}{l} \Phi_ {p} ^ {*} := \max _ {i \in \mathcal {P} _ {p} \backslash S _ {p} ^ {*}} \exp \left(- \frac {2 b ^ {2} G _ {i} ^ {2}}{9} s (p)\right), \\ \Phi_ {p} ^ {\prime} := \max _ {i \in \mathcal {Q} _ {p} \backslash S _ {p} ^ {\prime}} \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} R _ {i}}{8}\right) ^ {2} s (p)\right). \\ \end{array}
$$

Consider the case that $\bar { \mathcal { Q } } _ { p } > \bar { \mathcal { P } } _ { p }$ . Consider the number of arms in $\bar { \mathcal { Q } } _ { p } \cap ( \mathcal { P } _ { p } \backslash S _ { p } ^ { * } )$ , then

$$
\begin{array}{l} \mathbb {E} [ | \bar {\mathcal {Q}} _ {p} \cap (\mathcal {P} _ {p} \backslash S _ {p} ^ {*}) | ] = \sum_ {i \in \mathcal {P} _ {p} \backslash S _ {p} ^ {*}} \mathbb {P} [ \bar {G} _ {i} (p) <   \bar {G} _ {i ^ {\prime}} (p) ] \\ \leq \sum_ {i \in \mathcal {P} _ {p} \setminus S _ {p} ^ {*}} 2 m d \cdot \exp \left(- \frac {2 b ^ {2} G _ {i ^ {*}} ^ {2}}{9} s (p)\right) \\ \leq 2 m d \cdot | \mathcal {P} _ {p} \backslash S _ {p} ^ {*} | \cdot \Phi_ {p} ^ {*}. \\ \end{array}
$$

Then we apply Markov’s inequality

$$
\begin{array}{l} \mathbb {P} [ | \bar {\mathcal {Q}} _ {p} \cap (\mathcal {P} _ {p} \backslash S _ {p} ^ {*}) | > \frac {1}{8} | \bar {\mathcal {Q}} _ {p} | ] \\ \leq \frac {8 \mathbb {E} [ | \bar {\mathcal {Q}} _ {p} \cap (\mathcal {P} _ {p} \backslash S _ {p} ^ {*}) ]}{| \bar {\mathcal {Q}} _ {p} |} \tag {11} \\ \leq 1 6 m d \cdot \frac {| \mathcal {P} _ {p} \backslash S _ {p} ^ {*} |}{| \bar {\mathcal {Q}} _ {p} |} \Phi_ {p} ^ {*}. \\ \end{array}
$$

Then we have

$$
\mathbb {P} [ | \bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p} | > \frac {3}{4} | \bar {\mathcal {Q}} _ {p} | ] \geq 1 - 1 6 m d \cdot \frac {| \mathcal {P} _ {p} \backslash S _ {p} ^ {*} |}{| \bar {\mathcal {Q}} _ {p} |} \Phi_ {p} ^ {*}. \tag {12}
$$

Based on this event, let $i _ { p } ^ { * }$ denote the eliminated optimal arm in phase $p .$ Consider the the number of arms in $( \bar { \mathcal { Q } } _ { p } \cap \mathcal { Q } _ { p } ) \backslash S _ { p } ^ { \prime }$ with larger $\bar { R } _ { x }$ than that of the eliminated optimal arm and let $N _ { p } ^ { \prime }$ denote $\mathrm { i t , }$ then

$$
\begin{array}{l} \mathbb {E} [ N _ {p} ^ {\prime} ] = \sum_ {i \in (\bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p}) \setminus S _ {p} ^ {\prime}} \mathbb {P} [ \bar {R} _ {i _ {p} ^ {*}} (p) <   \bar {R} _ {i} (p) ] \\ \leq \sum_ {i \in (\bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p}) \setminus S _ {p} ^ {\prime}} 2 m d \cdot \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} R _ {i}}{8}\right) ^ {2} s (p)\right) \\ \leq 2 m d \cdot | (\bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p}) \backslash S _ {p} ^ {\prime} | \cdot \max _ {i \in (\bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p}) \backslash S _ {p} ^ {\prime}} \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} R _ {i}}{8}\right) ^ {2} s (p)\right). \\ \end{array}
$$

Then we apply Markov’s inequality

$$
\begin{array}{l} \mathbb {P} [ N _ {p} ^ {\prime} > \frac {1}{6} | \bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p} | ] \leq \frac {6 \mathbb {E} [ N _ {p} ^ {\prime} ]}{| \bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p} |} \\ \leq 1 2 m d \cdot \max _ {i \in (\bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p}) \setminus S _ {p} ^ {\prime}} \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} R _ {i}}{8}\right) ^ {2} s (p)\right). \\ \end{array}
$$

Then we obtain that the probability that there is at least one eliminated optimal arms is at most

$$
3 2 m d \cdot \Phi_ {p} ^ {*} + 1 2 m d \cdot \Phi_ {p} ^ {\prime}.
$$

Consider the case that $\bar { \mathcal { P } } _ { p } > \bar { \mathcal { Q } } _ { p }$ . Similarly, we have

$$
\begin{array}{l} \mathbb {P} [ | \bar {\mathcal {P}} _ {p} \cap (\mathcal {Q} _ {p} \backslash S _ {p} ^ {\prime}) | > \frac {1}{8} | \bar {\mathcal {P}} _ {p} | ] \\ \leq \frac {8 \mathbb {E} [ | \bar {\mathcal {P}} _ {p} \cap (\mathcal {Q} _ {p} \backslash S _ {p} ^ {\prime}) ]}{| \bar {\mathcal {P}} _ {p} |} \tag {13} \\ \leq 1 6 m d \cdot \frac {| \mathcal {Q} _ {p} \backslash S _ {p} ^ {\prime} |}{| \bar {\mathcal {P}} _ {p} |} \Phi_ {p} ^ {\prime}, \\ \end{array}
$$

and

$$
\mathbb {P} [ | \bar {\mathcal {P}} _ {p} \cap \mathcal {P} _ {p} | > \frac {3}{4} | \bar {\mathcal {P}} _ {p} | ] \geq 1 - 1 6 m d \cdot \frac {| \mathcal {Q} _ {p} \backslash S _ {p} ^ {\prime} |}{| \bar {\mathcal {P}} _ {p} |} \Phi_ {p} ^ {\prime}. \tag {14}
$$

Let $i _ { t } ^ { \prime }$ denote the added sub-optimal arm in phase $p .$ . Consider the the number of arms in $( \bar { \mathcal { P } } _ { p } \cap \mathcal { P } _ { p } ) \backslash S _ { p } ^ { * }$ with smaller $\hat { G } _ { x }$ than that of the sub-optimal arm $i ^ { \prime }$ and let $N _ { t } ^ { * }$ denote it, then

$$
\begin{array}{l} \mathbb {E} [ N _ {t} ^ {*} ] = \sum_ {i \in (\bar {\mathcal {P}} _ {p} \cap \mathcal {P} _ {p}) \setminus S _ {p} ^ {*}} \mathbb {P} [ \bar {G} _ {i} (p) <   \bar {G} _ {i ^ {\prime}} (p) ] \\ \leq \sum_ {i \in (\bar {\mathcal {P}} _ {p} \cap \mathcal {P} _ {p}) \setminus S _ {p} ^ {*}} 2 m d \cdot \exp \left(- \frac {2 b ^ {2} G _ {i} ^ {2}}{9} s (p)\right) \\ \leq 2 m d \cdot | \bar {\mathcal {P}} _ {p} \cap \mathcal {P} _ {p} | \cdot \max _ {i \in (\bar {\mathcal {P}} _ {p} \cap \mathcal {P} _ {p}) \setminus S _ {p} ^ {*}} \exp \left(- \frac {2 b ^ {2} G _ {i} ^ {2}}{9} s (p)\right). \\ \end{array}
$$

Then we apply Markov’s inequality

$$
\begin{array}{l} \mathbb {P} [ N _ {t} ^ {*} > \frac {1}{6} | \bar {\mathcal {P}} _ {p} \cap \mathcal {P} _ {p} | ] \\ \leq \frac {6 \mathbb {E} [ N _ {p} ^ {\prime} ]}{| \bar {\mathcal {P}} _ {p} \cap \mathcal {P} _ {p} |} \\ \leq 1 2 | \bar {\mathcal {P}} _ {p} \cup \mathcal {P} _ {p} \cup \mathcal {X} _ {p} ^ {*} | ^ {2} \cdot \max _ {i \in (\bar {\mathcal {P}} _ {p} \cap \mathcal {P} _ {p}) \setminus S _ {p} ^ {*}} \exp \left(- \frac {2 b ^ {2} G _ {i} ^ {2}}{9} s (p)\right). \\ \end{array}
$$

Then the probability that at least one sub-optimal arm is added to $\mathcal { X } _ { p } ^ { \ast }$ is at most

$$
3 2 m d \cdot \Phi_ {p} ^ {\prime} + 1 2 m d \cdot \Phi_ {p} ^ {*}.
$$

In conclude, the probability that the algorithm makes mistakes in round t is at most

$$
3 2 m d \cdot (\Phi_ {p} ^ {\prime} + \Phi_ {p} ^ {*}). \tag {15}
$$

Next, we analyse the algorithm to bound the probability of making mistakes over all rounds. Clearly, the algorithm does not exceed the budget B.

Consider the pulls for each arm in $\mathcal { X } _ { p }$ before phase $p + 1$

$$
\begin{array}{l} s (p) \geq \frac {B}{\log_ {4 / 3} m} \sum_ {k = 0} ^ {p} \frac {1}{| \mathcal {X} _ {p} + \mathcal {X} _ {p} ^ {*} |} \\ \geq \frac {B}{\log_ {4 / 3} m} \sum_ {k = 0} ^ {p} \min \left(\frac {2}{| \mathcal {X} _ {p} |}, \frac {2}{| \mathcal {X} _ {p} ^ {*} |}\right). \\ \end{array}
$$

Let $\begin{array} { r } { i _ { p } = \frac { m } { 1 6 } \left( \frac { 3 } { 4 } \right) ^ { p } } \end{array}$ , then we have

$$
\begin{array}{l} \Phi_ {p} ^ {*} = \max _ {i \in \mathcal {P} _ {p} \setminus S _ {p} ^ {*}} \exp \left(- \frac {2 b ^ {2} G _ {i} ^ {2}}{9} s (p)\right) \\ \leq \exp \left(- \frac {2 b ^ {2} \Delta_ {i _ {p}} ^ {2}}{9} s (p)\right) \\ \leq \exp \left(- \frac {4 b ^ {2} \Delta_ {i _ {p}} ^ {2}}{9} \frac {(p + 1) B}{| \mathcal {X} _ {p} ^ {*} | \log_ {4 / 3} m}\right) + \exp \left(- \frac {4 b ^ {2} \Delta_ {i _ {p}} ^ {2}}{9} \frac {B}{m \log_ {4 / 3} m} \left(\frac {4}{3}\right) ^ {t}\right) \tag {16} \\ = \exp \left(- \frac {4 b ^ {2} \Delta_ {i _ {p}} ^ {2}}{9 i _ {p}} \frac {i _ {p} (p + 1) B}{| \mathcal {X} _ {p} ^ {*} | \log_ {4 / 3} m}\right) + \exp \left(- \frac {4 b ^ {2} \Delta_ {i _ {p}} ^ {2}}{9 i _ {p}} \frac {B}{1 6 \log_ {4 / 3} m}\right) \\ \leq \exp \left(- \frac {4 b ^ {2}}{9 H} \frac {B}{| \mathcal {X} ^ {*} |}\right) + \exp \left(- \frac {4 b ^ {2}}{9 H} \frac {B}{1 6 \log_ {4 / 3} m}\right), \\ \end{array}
$$

and

$$
\begin{array}{l} \Phi_ {p} ^ {\prime} = \max _ {i \in \mathcal {Q} _ {p} \backslash S _ {p} ^ {\prime}} \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} R _ {i}}{8}\right) ^ {2} s (p)\right) \\ \leq \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} \Delta_ {i _ {p}}}{8 \sqrt {2}}\right) ^ {2} s (p)\right) (17) \\ \leq \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} \Delta_ {i _ {p}}}{8 \sqrt {2}}\right) ^ {2} \frac {(p + 1) B}{| \mathcal {X} _ {p} ^ {*} | \log_ {4 / 3} m}\right) + \exp \left(- 4 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} \Delta_ {i _ {p}}}{8 \sqrt {2}}\right) ^ {2} \frac {1}{i _ {p}} \frac {B}{1 6 \log_ {4 / 3} m}\right) (17) \\ \leq \exp \left(- \frac {4 b ^ {4}}{9 H} \frac {B}{| \mathcal {X} ^ {*} |}\right) + \exp \left(- \frac {4 b ^ {4}}{9 H} \frac {B}{1 6 \log_ {4 / 3} m}\right). \\ \end{array}
$$

Combine (15), (16), (17) together, we complete the proof of Theorem 3.2.

Last, we analyse the algorithm’s behavior. Consider the case that $\mathcal { Q } _ { p } > 2 \mathcal { P } _ { p }$ , according to (12) (which does not rely on $\bar { \mathcal Q } _ { p } > \bar { \mathcal P } _ { p } )$ , with probability at least $1 - 1 6 m d \cdot \frac { | \mathcal { P } _ { p } \backslash S _ { p } ^ { * } | } { | \bar { \mathcal { Q } } _ { p } | } \Phi _ { p } ^ { * } ,$ we have

$$
\begin{array}{l} | \bar {\mathcal {P}} _ {p} | = | \bar {\mathcal {P}} _ {p} \cap \mathcal {Q} _ {p} | + | \bar {\mathcal {P}} _ {p} \cap \mathcal {P} _ {p} | \\ = | \mathcal {Q} _ {p} | - | \bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p} | + | \mathcal {P} _ {p} | - | \bar {\mathcal {Q}} _ {p} \cap \mathcal {P} _ {p} | \\ <   \frac {3}{2} | \mathcal {Q} _ {p} | - | \bar {\mathcal {Q}} _ {p} | \\ \leq | \bar {\mathcal {Q}} _ {p} |. \\ \end{array}
$$

Similarly, consider the case that $\mathcal { P } _ { p } > 2 \mathcal { Q } _ { p }$ , according to (14), with probability at least $1 - 1 6 m d \cdot \frac { | \mathcal { Q } _ { p } \backslash S _ { p } ^ { \prime } | } { | \bar { \mathcal { P } } _ { p } | } \Phi _ { p } ^ { \prime } \mathrm { ~ , ~ }$ , we have

$$
| \bar {\mathcal {Q}} _ {p} | = | \bar {\mathcal {Q}} _ {p} \cap \mathcal {Q} _ {p} | + | \bar {\mathcal {Q}} _ {p} \cap \mathcal {P} _ {p} | <   \frac {3}{2} | \mathcal {P} _ {p} | - | \bar {\mathcal {P}} _ {p} | \leq | \bar {\mathcal {P}} _ {p} |.
$$

# C. Analysis of Algorithm 2

Our proof based on the following concentration inequality.

Lemma C.1 ((Kleinberg et al., 2008; Babaioff et al., 2015)). Consider some distribution with values in [0, 1], let v and v¯ be the expectation and average of n independent samples $x _ { 1 } , x _ { 2 } , \ldots , x _ { n }$ from this distribution, respectively. Then for each $\gamma > 0 ;$ ,

$$
\mathbb {P} [ | v - \bar {v} | \leq f _ {\text { rad }} (\bar {v}, n) \leq 3 f _ {\text { rad }} (v, n) ] \geq 1 - \exp (- \Omega (\gamma)), \tag {18}
$$

where $\begin{array} { r } { f _ { r a d } ( v , n ) = \sqrt { \frac { \gamma v } { n } } + \frac { \gamma } { n } } \end{array}$ . More generally, equation (18) holds $\begin{array} { r } { i f v = \frac { 1 } { n } \sum _ { t = 1 } ^ { n } \mathbb { E } [ x _ { t } | x _ { 1 } , \dots , x _ { t - 1 } ] } \end{array}$

We first prove the clean event that the upper confidence bound of the expected reward $\mu ^ { U } ( T / 3 )$ and lower confidence bound of the expected consumption $C ^ { L } ( T / 3 )$ )satisfy the following properties:

(1) with probability at least $1 - 2 m d T \cdot \exp ( - \Omega ( \gamma ) )$ ,

$$
\left| \left(\boldsymbol {\mu} ^ {U} (T / 3)\right) ^ {\top} \boldsymbol {x} _ {T / 3} - \mathrm{OPT} _ {\mathrm{LP}} \right| \leq O \left(\sqrt {\frac {\gamma m \cdot \mathrm{OPT} _ {\mathrm{LP}}}{T}} + \frac {\gamma m d}{T} + \frac {\mathrm{OPT} _ {\mathrm{LP}}}{B} \sqrt {\frac {\gamma m d \cdot b}{T}}\right).
$$

(2) with probability at least $1 - 2 m d T \cdot \exp ( - \Omega ( \gamma ) )$ ,

$$
\sum_ {t = 1} ^ {T / 3} \left| (\boldsymbol {C} ^ {L} (t)) ^ {\top} \boldsymbol {x} _ {t} - \boldsymbol {c} _ {t} \right| \leq \left(1 - O \left(\sqrt {\frac {\gamma m}{B}} + \frac {\gamma m \log T}{B}\right)\right) \frac {B \mathbf {1}}{3}.
$$

Let vˆ denote the empirical average of n samples, with probability at least $\begin{array} { r } { 1 - \exp ( - \Omega ( \gamma ) ) } \end{array}$ , we have

$$
\begin{array}{l} | \hat {v} - \bar {v} | \leq \frac {n}{n + 1} \cdot f _ {r a d} (\hat {v}, n) + \frac {\bar {v}}{n + 1} \\ \leq f _ {r a d} (\hat {v}, n + 1) + \frac {\bar {v}}{n + 1} \\ \leq 2 f _ {r a d} (\hat {v}, n + 1). \\ \end{array}
$$

By take a union bound, with probability $1 - m T \cdot \exp ( - \Omega ( \gamma ) )$ , we have

$$
\left| \frac {3}{T} \sum_ {t = 1} ^ {T / 3} (r (t) - \mu_ {i (t)}) \right| \leq O \left(f _ {\text {rad}} \left(\frac {3}{T} \sum_ {t = 1} ^ {T / 3} (\boldsymbol {\mu} ^ {U} (t)) _ {i (t)}, \frac {T}{3}\right)\right), \tag {19}
$$

$$
\left| \left(\boldsymbol {\mu} ^ {U} (T / 3)\right) ^ {\top} \boldsymbol {x} _ {T / 3} - \frac {3}{T} \sum_ {t = 1} ^ {T / 3} \left(\boldsymbol {\mu} ^ {U} (t)\right) _ {i (t)} \right| \leq O \left(f _ {r a d} \left(\frac {3}{T} \sum_ {t = 1} ^ {T / 3} \left(\boldsymbol {\mu} ^ {U} (t)\right) _ {i (t)}, \frac {T}{3}\right)\right).
$$

According to (Badanidiyuru et al., 2013), for any two vectors $\pmb { a } , \pmb { n } \in \mathbb { R } _ { + } ^ { m }$ , the following inequality always hold:

$$
\sum_ {i = 1} ^ {m} f _ {r a d} (a _ {i}, n _ {i}) n _ {i} \leq \sqrt {\gamma m (\boldsymbol {a} \cdot \boldsymbol {n})} + \gamma m
$$

Therefore,

$$
\begin{array}{l} \left| \sum_ {t = 1} ^ {T / 3} (\mu_ {i (t)} - (\boldsymbol {\mu} ^ {U} (t)) _ {i (t)}) \right| \leq O \left(\sum_ {t} f _ {r a d} (\mu_ {i (t)}, n _ {i (t)} (t) + 1)\right) \\ \leq O \left(\sum_ {i} (n _ {i (t)} (T / 3) + 1) f _ {r a d} (\mu_ {i (t)}, n _ {i (t)} (T / 3) + 1)\right) \\ \leq O \left(\sqrt {\gamma m \left(\sum_ {i} \mu_ {i} (n _ {i (t)} (T / 3) + 1)\right)} + \gamma m\right) \tag {20} \\ \leq O \left(\sqrt {\gamma m \left(\sum_ {t} \mu_ {i _ {t}}\right)} + \gamma m\right) \\ \leq O \left(\sqrt {\gamma m \left(\sum_ {t} (\boldsymbol {\mu} ^ {U} (t)) _ {i (t)}\right)} + \gamma m\right) \\ \end{array}
$$

Combine (19) and (20) together, we obtain

$$
\sqrt {\sum_ {t = 1} ^ {T / 3} \left(\boldsymbol {\mu} ^ {U} (t)\right) _ {i (t)}} \leq \sqrt {\sum_ {t = 1} ^ {T / 3} r (t)} + O (\sqrt {\gamma m}),
$$

and

$$
\left| \left(\boldsymbol {\mu} ^ {U} (T / 3)\right) ^ {\top} \boldsymbol {x} _ {T / 3} - \frac {3}{T} \sum_ {t = 1} ^ {T / 3} r (t) \right| \leq O \left(\sqrt {\gamma m (\sum_ {t} r (t))} + \gamma m\right).
$$

Similarly, we could also prove that with probability $1 - m d T \cdot \exp ( - \Omega ( \gamma ) )$ , we have

$$
\sum_ {t = 1} ^ {T / 3} \left| \left(\boldsymbol {C} ^ {L} (t)\right) ^ {\top} \boldsymbol {x} _ {t} - \boldsymbol {c} _ {t} \right| \leq O (\sqrt {\gamma m B} + \gamma m) \mathbf {1}.
$$

Combine (C) and (C) with the following inequality

$$
\frac {3}{T} \sum_ {t = 1} ^ {T / 3} r (t) \geq (1 - \epsilon) \mathrm{OPT} _ {\mathrm{LP}}
$$

and substituting the specification of ϵ and $\gamma = O ( \log ( m d T ) )$ , we obtain the desired inequalities. Notice that the consumption during the second step is at most $\begin{array} { l } { { \frac { B } { 2 } } } \end{array}$ , so the consumption of FULLOAK will less than $\frac { 5 B } { 6 }$ with high probability. Define

$$
\Psi := \left(\sqrt {\frac {\gamma m \cdot \mathrm{OPT} _ {\mathrm{LP}}}{T}} + \frac {\gamma m d}{T} + \frac {\mathrm{OPT} _ {\mathrm{LP}}}{B} \sqrt {\frac {\gamma m d \cdot b}{T}}\right).
$$

Then we prove the following lemma.

Lemma C.2. At the end of phase $p ,$ for any optimal arm $i ^ { * } \in \mathcal { X } ^ { * }$ and any sub-optimal arm $i ^ { \prime } \in \mathcal { X } ^ { \prime }$ , the probability that $\bar { R } _ { i ^ { * } } ( p ) > \bar { R } _ { i ^ { \prime } } ( p )$ is at most

$$
2 m d \cdot \exp \left(- \alpha_ {1} \cdot b ^ {2} R _ {i ^ {\prime}} ^ {2} s (p)\right).
$$

for some constant $\alpha _ { 1 }$

Proof. Consider the dual form

$\operatorname* { m i n } \textbf { \textit { b } } ^ { \top } \boldsymbol { w } ,$

$\mathrm { s . t . } \quad \bar { C } ^ { \top } \pmb { w } \geq \bar { \mu } , \pmb { w } \geq \mathbf { 0 } .$

Let $\bar { \pmb { w } } ^ { * } ( p )$ denote the optimal solution of $\mathrm { i t } ,$ we have

$$
\left| \boldsymbol {b} ^ {\top} \bar {\boldsymbol {w}} ^ {*} (p) - \boldsymbol {b} ^ {\top} \boldsymbol {w} \right| \leq O (\Psi).
$$

Then we get

$$
\sum_ {j = 1} ^ {d} \left(\bar {w} ^ {*} (p)\right) _ {j} - \sum_ {j = 1} ^ {d} w _ {j} ^ {*} \geq - \frac {1}{b} O (\Psi), \tag {21}
$$

$$
\sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} - \sum_ {j = 1} ^ {d} w _ {j} ^ {*} \leq \frac {1}{b} O (\Psi).
$$

Consider $R _ { i }$ of optimal arm $i ^ { * }$ and suboptimal $i ^ { \prime }$

$$
R _ {i ^ {*}} = \left(\boldsymbol {w} ^ {*}\right) ^ {\top} \boldsymbol {C} _ {i ^ {*}} - \mu_ {i ^ {*}} \quad \leq 0,
$$

$$
\bar {R} _ {i ^ {*}} = \left(\bar {\boldsymbol {w}} ^ {*} (p)\right) ^ {\top} \bar {\boldsymbol {C}} _ {i ^ {*}} - \bar {\mu} _ {i ^ {*}} > 0, \tag {22}
$$

$$
\bar {R} _ {i ^ {\prime}} = \left(\bar {\boldsymbol {w}} ^ {*} (p)\right) ^ {\top} \bar {\boldsymbol {C}} _ {i ^ {\prime}} - \bar {\mu} _ {i ^ {\prime}} <   \bar {R} _ {i ^ {*}}.
$$

From (21) and (22), we have

$$
\begin{array}{l} \sum_ {j = 1} ^ {d} \left(\bar {w} ^ {*} (p)\right) _ {j} \bar {C} _ {j, i ^ {*}} - \bar {\mu} _ {i ^ {*}} \\ \leq \sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} \left(C _ {j, i ^ {*}} + 3 f _ {r a d} (C _ {j, i ^ {*}}, s ^ {*} (p))\right) - (\mu_ {i ^ {*}} - 3 f _ {r a d} (\mu_ {i ^ {*}}, s ^ {*} (p))) \\ = \sum_ {j = 1} ^ {d} w _ {j} ^ {*} \left(C _ {j, i ^ {*}} + 3 f _ {\text {rad}} (C _ {j, i ^ {*}}, s ^ {*} (p))\right) - \left[ \sum_ {j = 1} ^ {d} w _ {j} ^ {*} \left(C _ {j, i ^ {*}} + 3 f _ {\text {rad}} (C _ {j, i ^ {*}}, s ^ {*} (p))\right) - \sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} \left(C _ {j, i ^ {*}} + 3 f _ {\text {rad}} (C _ {j, i ^ {*}}, s ^ {*} (p))\right) \right] \\ - \left(\mu_ {i ^ {*}} - 3 f _ {\text { rad }} (\mu_ {i ^ {*}}, s ^ {*} (p))\right) \\ \leq \sum_ {j = 1} ^ {d} w _ {j} ^ {*} (C _ {j, i ^ {*}} + 3 f _ {r a d} (C _ {j, i ^ {*}}, s ^ {*} (p))) + \frac {1}{b} O (\Psi) - (\mu_ {i ^ {*}} - 3 f _ {r a d} (\mu_ {i ^ {*}}, s ^ {*} (p))) \\ \leq 3 f _ {r a d} (C _ {j, i ^ {*}}, s ^ {*} (p)) \left(1 + \sum_ {j = 1} ^ {d} w _ {j} ^ {*}\right) + \frac {1}{b} O (\Psi). \\ \end{array}
$$

And

$$
\begin{array}{l} \sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} \bar {C} _ {j, i ^ {\prime}} - \bar {\mu} _ {i ^ {\prime}} \\ \geq \sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} (C _ {j, i ^ {\prime}} - 3 f _ {r a d} (C _ {j, i ^ {\prime}}, s ^ {\prime} (p))) - (\mu_ {i ^ {\prime}} + 3 f _ {r a d} (\mu_ {i ^ {\prime}}, s ^ {\prime} (p))) \\ = \sum_ {j = 1} ^ {d} w _ {j} ^ {*} (C _ {j, i ^ {\prime}} - 3 f _ {r a d} (C _ {j, i ^ {\prime}}, s ^ {\prime} (p))) - \left[ \sum_ {j = 1} ^ {d} w _ {j} ^ {*} \left(C _ {j, i ^ {*}} - 3 f _ {r a d} (C _ {j, i ^ {\prime}}, s ^ {\prime} (p))\right) - \sum_ {j = 1} ^ {d} (\bar {w} ^ {*} (p)) _ {j} \left(C _ {j, i ^ {*}} - 3 f _ {r a d} (C _ {j, i ^ {\prime}}, s ^ {\prime} (p))\right) \right] \\ - \left(\mu_ {i ^ {\prime}} + 3 f _ {r a d} (\mu_ {i ^ {\prime}}, s ^ {\prime} (p))\right) \\ \geq \sum_ {j = 1} ^ {d} w _ {j} ^ {*} (C _ {j, i ^ {\prime}} - 3 f _ {r a d} (C _ {j, i ^ {\prime}}, s ^ {\prime} (p))) - \frac {1}{b} O (\Psi) - (\mu_ {i ^ {\prime}} + 3 f _ {r a d} (\mu_ {i ^ {\prime}}, s ^ {\prime} (p))) \\ \geq R _ {i ^ {\prime}} - 3 f _ {r a d} (C _ {j, i ^ {\prime}}, s ^ {\prime} (p)) \left(1 + \sum_ {j = 1} ^ {d} w _ {j} ^ {*}\right) - \frac {1}{b} O (\Psi). \\ \end{array}
$$

According to the Strong duality theorem, we have

$$
\sum_ {j = 1} ^ {d} w _ {j} ^ {*} = \frac {1}{b} \sum_ {i = 1} ^ {m} \mu_ {i} x _ {i} ^ {*} = \frac {1}{b} \mathrm{OPT} _ {\mathrm{LP}} \leq \frac {1}{b}.
$$

Then we have

$$
\begin{array}{l} \mathbb {P} [ \bar {R} _ {i ^ {*}} (p) > \bar {R} _ {i ^ {\prime}} (p) ] \\ \leq \mathbb {P} \left[ R _ {i ^ {\prime}} <   3 \left(f _ {r a d} (C _ {j, i ^ {*}}, s ^ {*} (p)) + 3 f _ {r a d} (C _ {j, i ^ {\prime}}, s ^ {\prime} (p))\right) \left(1 + \frac {1}{b}\right) + \frac {1}{b} O (\Psi) \right] \\ \leq \mathbb {P} \left[ R _ {i ^ {\prime}} <   \frac {1}{b} O (\Psi + f _ {r a d} (1, s (p))) \right]. \\ \end{array}
$$

Notice that we have $f _ { r a d } ( 1 , s ( p ) ) = \Omega ( \Psi )$ . Combine them together, we complete the proof.

According to Lemma B.4, for any optimal arm $i ^ { * } \in \mathcal { X } ^ { * }$ and any active sub-optimal arm $i ^ { \prime } \in \mathcal { X } ^ { \prime } \cap \mathcal { X } _ { p }$ , the probability that

$\bar { G } _ { i ^ { * } } ( p ) < \bar { G } _ { i ^ { \prime } } ( p )$ is at most

$$
2 m d \cdot \exp \left(- \frac {2 b ^ {2} G _ {i ^ {*}} ^ {2}}{9} s (p)\right)
$$

during phase $p .$ Similar to the proof of Theorem 3.2, we bound the probability that the algorithm makes mistakes by ignoring the $\textstyle { \frac { 1 } { 1 6 } } | { \mathcal { X } } _ { p } |$ arms with the smallest $G _ { i }$ and the $\textstyle { \frac { 1 } { 1 6 } } | { \mathcal { X } } _ { p } |$ arms with largest $R _ { i }$ of the active arms set. For all arms in $\mathcal { X } _ { p } .$ , let $\mathcal { P } _ { p }$ and $\bar { \mathcal P } _ { p }$ denote the set of optimal arms for (1) and $( 4 ) , \mathcal { Q } _ { p }$ and $\bar { \mathcal { Q } } _ { p }$ denote the set of sub-optimal arms for (1) and (4). Let $S _ { p } ^ { * }$ denote the $\frac { 1 } { 1 6 } | \mathcal { X } _ { p } |$ arms with smallest $G _ { i }$ and $S _ { p } ^ { \prime }$ denote the $\frac { 1 } { 1 6 } | \mathcal { X } _ { p } |$ arms with largest $R _ { i } .$ , respectively. Define

$$
\begin{array}{l} \Phi_ {p} ^ {*} := \max _ {i \in \mathcal {P} _ {p} \backslash S _ {p} ^ {*}} \exp \left(- \frac {2 b ^ {2} G _ {i} ^ {2}}{9} s (p)\right), \\ \Phi_ {p} ^ {\prime} := \max _ {i \in \mathcal {Q} _ {p} \backslash S _ {p} ^ {\prime}} \exp \left(- \alpha_ {1} \cdot b ^ {2} R _ {i ^ {\prime}} ^ {2} s (p)\right). \\ \end{array}
$$

We obtain that the probability that there is at least one eliminated optimal arms is at most

$$
3 2 m d \cdot \Phi_ {p} ^ {*} + 1 2 m d \cdot \Phi_ {p} ^ {\prime}.
$$

Similarly, the probability that at least one sub-optimal arm is added to $\boldsymbol { \mathcal { X } } _ { p } ^ { * }$ is at most

$$
3 2 m d \cdot \Phi_ {p} ^ {\prime} + 1 2 m d \cdot \Phi_ {p} ^ {*}.
$$

Notice that FULLOAK will delete all accept arms from the surviving arms set at the end of each phase, the pulls for each arm in $\mathcal { X } _ { p }$ before phase $t + 1$ satisfy

$$
s (p) \geq \frac {B}{\log_ {4 / 3} m} \sum_ {k = 0} ^ {p} \frac {1}{| \mathcal {X} _ {p} |}
$$

Let $\begin{array} { r } { i _ { p } = \frac { m } { 1 6 } \left( \frac { 3 } { 4 } \right) ^ { p } } \end{array}$ , then we have

$$
\begin{array}{l} \Phi_ {p} ^ {*} = \max _ {i \in \mathcal {P} _ {p} \backslash S _ {p} ^ {*}} \exp \left(- \frac {2 b ^ {2} G _ {i} ^ {2}}{9} s (p)\right) \\ \leq \exp \left(- \frac {2 b ^ {2} \Delta_ {i _ {p}} ^ {2}}{9} s (p)\right) \\ \leq \exp \left(- \frac {4 b ^ {2} \Delta_ {\iota_ {p}} ^ {2}}{9} \frac {B}{m \log_ {4 / 3} m} \left(\frac {4}{3}\right) ^ {p}\right) \tag {23} \\ = \exp \left(- \frac {4 b ^ {2} \Delta_ {i _ {p}} ^ {2}}{9 i _ {p}} \frac {B}{1 6 \log_ {4 / 3} m}\right) \\ \leq \exp \left(- \frac {4 b ^ {2}}{9 H} \frac {B}{1 6 \log_ {4 / 3} m}\right) \\ \end{array}
$$

Similarly, we have

$$
\Phi_ {p} ^ {\prime} = \max _ {i \in \mathcal {Q} _ {p} \backslash S _ {p} ^ {\prime}} \exp \left(- \alpha_ {1} \cdot b ^ {2} R _ {i ^ {\prime}} ^ {2} s (p)\right) \leq \exp \left(- \frac {\alpha_ {2} b ^ {2} B}{H \log m}\right), \tag {24}
$$

where $\alpha _ { 2 }$ is a constant. Combine them together, we complete the proof.

The proof is similar to Lemma 7.4 in (Badanidiyuru et al., 2013) and the theoretical analysis in Appendix B.3 for the UCB algorithm for BwK (Agrawal & Devanur, 2014).

# D. Analysis of Lower Bound (Theorem 4.2)

Let $( p _ { w } ) _ { 2 \le w \le W } \in [ 1 / 4 , 1 / 2 )$ be $( W - 1 )$ real numbers and let $p _ { 1 } = 1 / 2$ . And we define the quantities $l _ { w } : = 1 / 2 - p _ { w }$ . Assume m is an exact multiple of W . Then we define

$$
\mu_ {i} := \frac {1}{2} - \frac {l _ {w}}{2 ^ {\lfloor (m - i) / W \rfloor}}, w = (i \bmod W), i \in [ m ].
$$

Let $\pi _ { i }$ denote the Bernoulli distribution of mean $\mu _ { i }$ and $\pi _ { i } ^ { \prime }$ denote the Bernoulli distribution of mean $1 - \mu _ { i }$

Consider W problem instances with time horizon T , m arms, d types of resources being consumed, and knapsack $b = W / m$ for each type of resource. To ease the reading, assume $T$ is a power of 2, $W \geq \Omega ( { \sqrt { m } } )$ , and $d > m / W$ . Let $w = ( i \mathrm { m o d } W )$ , for the u-th problem instance, the i-th arm $x _ { i } ^ { u }$ is associated with the reward distribution $\pi _ { i } ^ { u }$ ,

$$
\pi_ {i} ^ {u} := \pi_ {i} {\bf 1} \{w \neq u \} + \pi_ {i} ^ {\prime} {\bf 1} \{w = u \}, u \in [ W ], i \in [ m ].
$$

The consumption vector $\boldsymbol { c } _ { i } ^ { u }$ satisfies $( \pmb { c } _ { i } ^ { u } ) _ { 1 } = ( \pmb { c } _ { i } ^ { u } ) _ { d } = ( \pmb { c } _ { i } ^ { u } ) _ { w } = 1$ , and $( \boldsymbol { c } _ { i } ^ { u } ) _ { j } = 0$ for all $j \neq 1 , j \neq w , j \neq d .$ . Then there are $| \mathcal { X } ^ { * } | = m / W = 1 / b$ optimal arms and their indexes satisfy (i mod $W ) = u$ . For the hardness measure of the u-th problem instance H(u), we have

$$
H (u) = \max _ {i \in [ m ]} \frac {i}{\Delta_ {i , u} ^ {2}} \leq b \cdot 2 ^ {\frac {1}{b} + 1} \sum_ {w \neq u} (l _ {w} + l _ {u}) ^ {- 2},
$$

where $\Delta _ { i , u }$ is the vertex gap of the i-th arm for u-th instance.

Consider any algorithm A and let $( T _ { k } ) _ { 1 \leq k \leq | \mathcal { X } ^ { * } | }$ denote the number of samples by A on arms from index $( k - 1 ) \cdot W + 1$ to $k \cdot W$ . These quantities are random but satisfy $\begin{array} { r } { \sum _ { 1 \le k \le | \mathcal { X } ^ { * } | } T _ { k } = B } \end{array}$ . We have

$$
\begin{array}{l} \mathbb {P} (\mathcal {O} \neq \mathcal {X} ^ {*}) \geq \sum_ {i \in \mathcal {X} ^ {*}} \mathbb {P} (i \notin \mathcal {O}) \\ \geq \sum_ {1 \leq k \leq | \mathcal {X} ^ {*} |} \exp \left(- \frac {\beta_ {1} T _ {k}}{2 ^ {m - k} \cdot \log (W) \sum_ {w \neq u} (l _ {w} + l _ {u}) ^ {- 2}}\right) \\ \geq \exp \left(- \frac {\beta_ {2} b B}{2 ^ {\frac {1}{b} - 1} \log (W) \sum_ {w \neq u} (l _ {w} + l _ {u}) ^ {- 2}}\right) \\ \geq \exp \left(- \frac {\beta_ {2} b ^ {2} \cdot 2 ^ {\frac {1}{b} + 1} B}{2 ^ {\frac {1}{b} - 1} H (u) \log (W)}\right) \geq \exp \left(- \frac {2 \beta_ {2} b ^ {2} B}{H (u) \log m}\right), \\ \end{array}
$$

where $\beta _ { 1 } , \beta _ { 2 }$ are some constants. The second inequality comes from Theorem 2 of (Carpentier & Locatelli, 2016). Then we complete the proof.

# E. Analysis of Special Cases

# E.1. Simple OAK Problem

In this section, we provide the specification of $\mathrm { B A S E O A K ^ { - } }$ and prove Theorem 5.1.

The algorithm (shown in Algorithm 3) also splits the budget evenly into phases and chooses the worst/best quarter of surviving arms to reject/accept at the end of each phase. The difference is that the Algorithm 3 eliminates the accepted arms from the active arm set at the end of each accept phase.

We provide the proof of Theorem 5.1 below. Again, the probability that the algorithm makes mistakes in phase p is at most

$$
3 2 \left| \bar {\mathcal {P}} _ {p} \cup \mathcal {P} _ {p} \right| ^ {2} \cdot \left(\Phi_ {p} ^ {\prime} + \Phi_ {p} ^ {*}\right). \tag {25}
$$

And the algorithm does not exceed the budget $T .$ .

Consider the pulls for each arm in $\mathcal { X } _ { p }$ before phase $p + 1$

$$
s (p) \geq \frac {T}{\log_ {4 / 3} m} \sum_ {k = 0} ^ {p} \frac {1}{| \mathcal {X} _ {p} |}.
$$

Algorithm 3 BASEOAK−   
Input: rounds T, number of arms m
1: $X_{0} \leftarrow [m]$ , $X_{0}' \leftarrow \emptyset$ , $X_{0}^{*} \leftarrow \emptyset$ 2: for $p = 0, \ldots, \lceil \log_{4/3} m \rceil - 1$ do
3: Pull each arm $i \in X_{p}$ for $n(p) = \left\lfloor \frac{T}{|\mathcal{X}_{p}| \lceil \log_{4/3} m \rceil} \right\rfloor$ times
4: Compute the empirical estimator of the reduced gap $\bar{R}_{i}$ and deletion gap $\bar{G}_{i}$ for each arm $i \in X_{p}$ 5: if more non-basis variables in $\bar{x}^{*}(p)$ then
6: $X_{p+1}^{*} \leftarrow X_{p}^{*} \cup \{\text{the set of } \lceil |X_{p}|/4\rceil \text{ optimal arms in } X_{p} \text{ with the largest } \bar{G}_{i}\}$ 7: else
8: $X_{p+1}' \leftarrow X_{p}' \cup \{\text{the set of } \lceil |X_{p}|/4\rceil \text{ sub-optimal arms in } X_{p} \text{ with the largest } \bar{R}_{i}\}$ 9: end if
10: $X_{p+1} \leftarrow X_{0} \backslash (X_{p+1}' \cup X_{p+1}^{*})$ 11: end for
12: Output $X_{\lceil \log_{4/3} m \rceil}^{*}$

Let $\begin{array} { r } { i _ { p } = \frac { m } { 1 6 } \left( \frac { 3 } { 4 } \right) ^ { p } } \end{array}$ , then we have

$$
\begin{array}{l} \Phi_ {p} ^ {*} = \max _ {i \in \mathcal {P} _ {p} \backslash S _ {p} ^ {*}} \exp \left(- \frac {2 b ^ {2} G _ {i} ^ {2}}{9} s (p)\right) \\ \leq \exp \left(- \frac {2 b ^ {2} \Delta_ {i _ {p}} ^ {2}}{9} s (p)\right) \\ \leq \exp \left(- \frac {4 b ^ {2} \Delta_ {i _ {p}} ^ {2}}{9} \frac {T}{m \log_ {4 / 3} m} \left(\frac {4}{3}\right) ^ {p}\right) \tag {26} \\ = \exp \left(- \frac {4 b ^ {2} \Delta_ {i _ {p}} ^ {2}}{9 i _ {p}} \frac {T}{1 6 \log_ {4 / 3} m}\right) \\ \leq \exp \left(- \frac {4 b ^ {2}}{9 H} \frac {T}{1 6 \log_ {4 / 3} m}\right), \\ \end{array}
$$

and

$$
\begin{array}{l} \Phi_ {p} ^ {\prime} = \max _ {i \in \mathcal {Q} _ {p} \backslash S _ {p} ^ {\prime}} \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} R _ {i}}{8}\right) ^ {2} s (p)\right) \\ \leq \exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} \Delta_ {i _ {p}}}{8 \sqrt {2}}\right) ^ {2} s (p)\right) \tag {27} \\ \leq \exp \left(- 4 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} \Delta_ {i _ {p}}}{8 \sqrt {2}}\right) ^ {2} \frac {1}{i _ {p}} \frac {T}{1 6 \log_ {4 / 3} m}\right) \\ \leq \exp \left(- \frac {4 b ^ {4}}{9 H} \frac {T}{1 6 \log_ {4 / 3} m}\right). \\ \end{array}
$$

For all rounds t, we have $\begin{array} { r } { | \bar { \mathcal { P } } _ { p } \cup \mathcal { P } _ { p } | \leq \left( \frac { 3 } { 4 } \right) ^ { p } } \end{array}$ m. Combine (25), (26), (27) together, we complete the proof.

# E.2. Pure Exploration Problems

In this section, we prove the results in Example 5.2 and 5.3.

For the BAI problem, there is one optimal arm i∗. According to the proof of Lemma B.3, assume the optimal arm $i ^ { * }$ is not eliminated at the end of phase $p .$ For the optimal arm i∗ and any active sub-optimal arm $i ^ { \prime } \in \mathcal { X } ^ { \prime } \cap \mathcal { X } _ { p }$ , the probability that $\bar { R } _ { i ^ { * } } ( p ) > \bar { R } _ { i ^ { \prime } } ( p )$ is at most

$$
O \left(\exp \left(- 2 \left(\frac {b \Delta_ {2}}{8} + \frac {b ^ {2} R _ {i ^ {\prime}}}{8}\right) ^ {2} s (p)\right)\right).
$$

According to the proof of Theorem 3.2, the probability that the algorithm makes mistakes in round p is at most

$$
3 2 (\Phi_ {p} ^ {\prime} + \Phi_ {p} ^ {*}).
$$

By equation (26), (27), and a union bound, we complete the proof of the result in Example 5.2.

For the TopK and MB problem, due to the deterministic resource consumption, the probability that the algorithm makes mistakes in round p is at most

$$
3 2 | \bar {\mathcal {P}} _ {p} \cup \mathcal {P} _ {p} | \cdot (\Phi_ {p} ^ {\prime} + \Phi_ {p} ^ {*}).
$$

For all rounds p, we have $\begin{array} { r } { | \bar { \mathcal { P } } _ { p } \cup \mathcal { P } _ { p } | \leq \left( \frac { 3 } { 4 } \right) ^ { p } m } \end{array}$ . By equation (26), (27), and a union bound, we obtain the result in Example 5.3.