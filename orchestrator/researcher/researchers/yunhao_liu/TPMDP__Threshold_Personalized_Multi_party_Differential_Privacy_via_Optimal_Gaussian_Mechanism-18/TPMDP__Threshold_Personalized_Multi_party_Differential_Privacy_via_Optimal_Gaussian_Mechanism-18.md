# TPMDP: Threshold Personalized Multi-party Differential Privacy via Optimal Gaussian Mechanism

Jiandong Liu1, Lan Zhang1, Chaojie Lv1, Ting Yu2, Nikolaos M. Freris1, and Xiang-Yang Li1

1University of Science and Technology of China, Hefei, China

2Hamad Bin Khalifa University, Qatar

jdliu@mail.ustc.edu.cn, zhanglan@ustc.edu.cn, chjlv@mail.ustc.edu.cn, tyu@hbku.edu.qa,

nfr@ustc.edu.cn, xiangyangli@ustc.edu.cn

Abstract—In modern distributed computing applications, such as federated learning and AIoT systems, protecting privacy is crucial to prevent adversarial parties from colluding to steal others’ private information. However, guaranteeing the utility of computation outcomes while protecting all parties’ data privacy can be challenging, particularly when the parties’ privacy requirements are highly heterogeneous. In this paper, we propose a novel privacy framework for multi-party computation called Threshold Personalized Multi-party Differential Privacy (TPMDP), which addresses a limited number of semi-honest colluding adversaries. Our framework enables each party to have a personalized privacy budget. We design a multi-party Gaussian mechanism that is easy to implement and satisfies TPMDP, wherein each party perturbs the computation outcome in a secure multi-party computation protocol using Gaussian noise. To optimize the utility of the mechanism, we cast the utility loss minimization problem into a linear programming (LP) problem. We exploit the specific structure of this LP problem to compute the optimal solution after O(n) computations, where n is the number of parties, while a generic solver may require exponentially many computations. Extensive experiments demonstrate the benefits of our approach in terms of low utility loss and high efficiency compared to existing private mechanisms that do not consider personalized privacy requirements or collusion thresholds.

Index Terms—Differential privacy, secure multi-party computation, personalized privacy, distributed computing.

# I. INTRODUCTION

Collaborative computing, which involves multiple parties, has garnered significant attention in distributed systems like IoT and ad-hoc networks. This approach enables parties to obtain results with higher utility or accuracy based on more abundant datasets in tasks such as distributed computing [1], edge computing [2], and federated learning [3]. However, protecting privacy of the involved parties who contribute data in computing is crucial. For instance, in collaborative recommendations [4], multiple parties, such as video websites, banks, and online shops, contribute data to train an AI model to predict clients’ preferences. Each party holds a personalized privacy requirement, and the privacy requirement of banks, for example, can be more stringent than that of video websites.

Several solutions for (personalized) privacy-preserving collaborative computing have been proposed in the current literature [5]–[8] based on differential privacy (DP) [9]. These solutions aim to ensure the privacy of all parties by perturbing the outputs or inputs in collaborative computing. However, these methods can result in a prohibitively high noise level, which may significantly compromise the utility of the output. In this work, we propose a new personalized privacy framework for collaborative computing that offers higher utility.

To solve the problem of personalized private collaborative computing, we propose a new concept called threshold personalized multi-party differential privacy (TPMDP). TP-MDP draws on insights from both threshold secure multiparty computation (t-MPC) [10] and personalized differential privacy (PDP) [11]. t-MPC provides a collaborative computing framework that allows multiple parties to compute accurate results while ensuring that no collusion of t or fewer parties learns more than the outcome, where t is a predefined threshold value. In real-world applications, parties may be geographically isolated or have conflicting interests, which limits their ability to collude arbitrarily (e.g., distributed learning in Internet-of-Things (IoT) systems [12]). TPMDP ensures that all parties’ personalized DP requirements are met for all collusions of size up to a given threshold t.

The benefits of the TPMDP framework are demonstrated through the design of a highly effective and easy-to-implement multi-party Gaussian mechanism that satisfies TPMDP. In this mechanism, each participating party samples a Gaussian noise that adheres to all parties’ privacy requirements. Following this, all parties input their respective data and noise to a t-MPC protocol, which computes the query function perturbed by the noises contributed by all parties.

The utility of the multi-party Gaussian mechanism is optimized using an efficient parameter-choosing algorithm. We transform the problem of minimizing utility loss measured by the noise variance into a linear programming (LP) problem, which is characterized by numerous constraints that cannot be efficiently solved using a generic LP solver. To address this challenge, we leverage the structure of the LP problem and propose a method that yields the optimal solution with linear complexity O(n), where n represents the number of parties.

Our multi-party Gaussian mechanism offers notable theoretical advantages. In particular, compared to the threshold multi-party DP (TMDP) mechanism [5], where each party adds noise with uniform variance determined by their most stringent privacy requirement, our mechanism achieves superior utility, especially in scenarios where parties have heterogeneous privacy requirements and the collusion threshold is large. On the other hand, compared with the personalized local DP (PLDP) mechanism [7] without considering collusion thresholds, the advantage of the multi-party Gaussian mechanism is prominent when the threshold $t \le p n$ for a constant $p < 1$ as n increases.

For the LP problem of maximizing the multi-party Gaussian mechanism’s utility, we compare the efficiency of our solver with that of the state-of-the-art generic LP solver [13]. We find that the space and time complexity of the generic solver can be exponential in n. In contrast, our solver computes the optimal variance assignment with ${ \mathcal { O } } ( n )$ storage and running time.

We conduct experiments on synthetic and real-world datasets, which demonstrate that our TPMDP multi-party Gaussian mechanism outperforms both the TMDP and PLDP mechanisms in terms of utility. Moreover, we compare our mechanism with centralized (personalized) DP mechanisms where a trusted third party gathers data from all parties, computes the query function with additive noise, and then releases the results. It shows that our mechanism achieves utility comparable to centralized mechanisms when the honest parties comprise the majority $( \mathrm { i } . \mathrm { e } . , t < 0 . 5 n )$ .

Furthermore, we highlight the scalability advantages of our exact algorithm for solving the LP problem. Our method outperforms generic LP solvers and can efficiently handle many parties, making it a practical and scalable solution for multi-party privacy mechanisms.

# II. PRELIMINARIES

In this section, we introduce pertinent concepts from secure multi-party computation (MPC) and differential privacy (DP).

# A. Privacy of MPC

This paper focuses on MPC protocols with n semi-honest parties. Semi-honest parties follow the protocol but attempt to infer others’ private data through the messages they obtain during the protocol execution, denoted as their views.

Given an n-ary deterministic function $\begin{array} { r l } { f : } & { { } ( \{ 0 , 1 \} ^ { * } ) ^ { n } \to } \end{array}$ $( \{ 0 , 1 \} ^ { * } ) ^ { n }$ , we denote $f _ { A } ( { \pmb x } )$ as $\{ f _ { i } ( { \pmb x } ) \} _ { i \in A }$ , where $\textbf { \textit { x } } \triangleq$ $( x _ { 1 } , \ldots , x _ { n } ) , \ f _ { i } ( { \pmb x } )$ denotes the i-th element of $f ( { \pmb x } )$ , and $A \subset [ n ]$ is an adversarial group. Here, $\{ 0 , 1 \} ^ { * }$ denotes the space of binary strings with arbitrary length. The view of party $j \in [ n ]$ on the MPC protocol π with input x, denoted by ${ \mathscr V } _ { j } ^ { \pi } ( { \pmb x } )$ , is the vector consisting of all the messages that party j inputs and receives during the execution of π. The view of the adversarial group A is denoted as $\mathcal { V } _ { A } ^ { \pi } ( \pmb { x } ) \triangleq ( A , \{ \mathcal { V } _ { i } ^ { \pi } ( \pmb { x } ) \} _ { i \in A } )$ .

A protocol π privately computes f in the presence of any adversarial group A if A’s view $\mathcal { V } _ { A } ^ { \pi } ( { \pmb x } )$ can be essentially computed from the inputs and outputs available to A, such that computationally bounded or unbounded adversaries cannot distinguish it. The formal definitions of computational and statistical indistinguishability (denoted $\mathbf { b } \mathbf { y } \triangleq \mathrm { a n d } \triangleq$ , which provide privacy against computationally bounded and unbounded adversaries, respectively) can be found in [10]. We define the adversary structure  as the set of all considered adversarial groups A. We say that protocol π privately computes f if it privately computes f in the presence of A for all $A \in A .$

Definition 1 (Privacy of n-party MPC protocols for deterministic functions in semi-honest settings [10]). We say that an MPC protocol π computationally t-privately computes the deterministic function f if there exists a probabilistic polynomialtime algorithm  such that for $A \in \bar { \mathcal { A } } _ { t } \triangleq \{ A \subset [ n ] | | A | \leq t \}$ ,

$$
\left. \left\{\mathcal {S} (A, \left\{x _ {i} \right\} _ {i \in A}, f _ {A} (\boldsymbol {x})) \right\} _ {\boldsymbol {x} \in (\{0, 1 \} ^ {*}) ^ {n}} \stackrel {{c}} {{=}} \left\{\mathcal {V} _ {A} ^ {\pi} (\boldsymbol {x}) \right\} _ {\boldsymbol {x} \in (\{0, 1 \} ^ {*}) ^ {n}}. \right. \tag {1}
$$

Similarly, we say that π statistically t-privately computes $f ,$ if for every $A \in \mathcal A _ { t }$ , the left-hand and right-hand sides in $E q .$ . (1) are statistically indistinguishable.

In computationally private MPC, privacy is maintained even in unlimited collusions $( t = n - 1 )$ . On the other hand, in statistically private MPC, privacy is only guaranteed when the honest parties constitute a strict majority $\left( t < n / 2 \right)$ [10].

# B. DP and Gaussian Mechanism

In DP, our goal is to design a mechanism $M : \mathcal { X }  \mathcal { Y }$ that ensures the privacy of each record in an arbitrary collection $\mathbf { \boldsymbol { x } } \in \mathcal { X }$ . Here, X denotes the set of all possible input collections. We use the notation $x \simeq y$ to represent neighboring input collections x, $y \in { \mathcal { X } } , \operatorname { i . e . }$ , inputs that are either identical or differ by at most one element.

Definition 2 (Differential Privacy [9]). For $\epsilon \ge 0 , \delta \in [ 0 , 1 ] ,$ a randomized algorithm M is (ϵ, δ)-differentially private $i f f o r$ all $S \subset R a n g e ( M )$ and for all $\mathbf { { } } x , y \in { \mathcal { X } }$ such that $x \simeq y \mathrm { . }$

$$
\operatorname * {P r} [ M (\boldsymbol {x}) \in S ] \leq \exp (\epsilon) \operatorname * {P r} [ M (\boldsymbol {y}) \in S ] + \delta . \tag {2}
$$

Output perturbation is an important class of DP mechanisms. Let f be a query function. An output perturbation mechanism adds a noise vector X to f (x), i.e., $M ( { \pmb x } ) =$ $f ( { \pmb x } ) + { \boldsymbol { X } }$ . The Gaussian mechanism is a widely adopted output perturbation mechanism, where $X \sim \mathcal { N } ( 0 , \sigma ^ { 2 } I )$ , with I representing a d-dimensional identity matrix, where d is the dimension of $f ^ { \ast } \mathrm { \mathbf { s } }$ output. Balle et al. [14] proposed the analytical Gaussian mechanism that is tight for $( \epsilon , \delta ) \ / – \mathrm { D P }$ by selecting an appropriate $\sigma ^ { 2 }$ . For a function f with l2-sensitivity can compute with (1) c $\Delta _ { 2 } f \triangleq { \begin{array} { l } { { \underline { { \Delta } } } } \\ { { \overline { { \Delta } } } 2 { \mathrm { { J } } } } \end{array} } $ max $\sigma _ { ( \epsilon , \delta , \Delta _ { 2 } f ) } ^ { 2 }$ $\pmb { x } { \simeq } \pmb { y } \parallel f ( \pmb { x } ) - f ( \pmb { y } ) \parallel _ { 2 }$ − ∥2 using an efficient numerical alg. The Gaussian mechanism is and given ϵ and δ, one $( \epsilon , \delta ) \cdot$ differentially private if and only if σ2 ≥ σ2(ϵ,δ,∆2f). $\sigma ^ { 2 } \ge \sigma _ { ( \epsilon , \delta , \Delta _ { 2 } f ) } ^ { 2 }$ We use the notations Γ ≜ (ϵ, δ, ∆2f ) and σ2(ϵ,δ,∆ f) $\Gamma \triangleq ( \epsilon , \delta , \Delta _ { 2 } f )$ $\sigma _ { ( \epsilon , \delta , \Delta _ { 2 } f ) } ^ { 2 } \overset { \Delta } { = } \sigma _ { \Gamma } ^ { 2 }$ .

# III. PROBLEM FORMULATION

In this section, we formulate the definition of threshold personalized multi-party differential privacy (TPMDP).

# A. Computation and Privacy Threat Model

As shown in Fig. 1, the TPMDP system model involves a group of parties [n] who seek to privately compute a deterministic function $f ( x _ { 1 } , \ldots , x _ { n } )$ , where each party $i \in [ n ]$ holds an input $x _ { i } ~ \in ~ \{ 0 , 1 \} ^ { * }$ . We assume that the parties are semi-honest and that the maximum number of colluding adversaries is t.

![](images/1db75b3e66451cbb82d3376dacdab19db3ba93a1c5f9d7783bcb6579d644d8ae.jpg)



Fig. 1: The system model of TPMDP. The parties are assumed semi-honest, with the size of any adversarial group being limited to t. Each party i holds an input $x _ { i }$ and a privacy budget parameterized by $( \epsilon _ { i } , \delta _ { i } )$ . All parties execute the protocol Π and generate an output yi for each i. The privacy of each party’s input is preserved, ensuring that any adversarial group cannot obtain any information about $x _ { i }$ beyond $( \epsilon _ { i } , \delta _ { i } ) { \mathrm { - D P } }$ provided that party i is not part of that group.

To quantify the privacy requirements of each party i, we use the DP parameters $( \epsilon _ { i } , \delta _ { i } )$ for $i \in [ n ]$ . Specifically, in Definition 2, we take the function M as an arbitrary inference function and the input x or y as the messages that any adversary can obtain in a TPMDP protocol. We require that Eq. (2) holds for each i to ensure the privacy of party i. For convenience, we denote $\mathcal { E } \triangleq \{ ( \epsilon _ { i } , \delta _ { i } ) \} _ { i \in [ n ] }$ .

# B. Definition of TPMDP

TPMDP provides a metric for the privacy loss of a multiparty computation algorithm in case at most one $\mathrm { p a r t y } ^ { \bullet }$ input varies (denoted by neighboring inputs). The definition of neighboring inputs is provided in Definition 3. We define the colluding group’s refined view, as outlined in Definition 4, regarding what they can infer from the algorithm run. Finally, we summarize the definition of TPMDP in Definition 5.

Definition 3 (j-neighboring inputs). For $j \in [ n ]$ , two inputs $\pmb { x } \triangleq ( x _ { 1 } , \ldots , x _ { n } )$ and $\pmb { x } ^ { \prime } \triangleq ( x _ { 1 } ^ { \prime } , \ldots , x _ { n } ^ { \prime } )$ are j-neighboring if $x _ { i } = x _ { i } ^ { \prime } f o r i \neq j ;$ we use the notation x ${ \overset { j } { \simeq } } y .$ .

Definition 4 (Refined view). Let $\mathcal { V } _ { A } ^ { \Pi } ( { \pmb x } , { \pmb X } )$ be the viewed messages of group $A \subset [ n ]$ in a n-party computation protocol Π that computes a deterministic function given the input x and collection of randomization terms $\pmb { X } \in s u p p ( \mathcal { P } )$ . Here, P denotes the distribution of the collection of randomization terms, and supp(P) denotes the support of P. A tuple $\mathcal { R V } _ { A } ^ { \Pi } ( { \pmb x } , { \pmb X } )$ ) is called a computational refined view for $A \subset [ n ]$ if there exists a probabilistic polynomial-time algorithm S such that:

$$
\begin{array}{l} \left. \left\{\mathcal {S} (A, \mathcal {R V} _ {A} ^ {\Pi} (\boldsymbol {x}, \boldsymbol {X})) \right\} _ {\boldsymbol {x} \in (\{0, 1 \} ^ {*}) ^ {n}, \boldsymbol {X} \in s u p p (\mathcal {P})} \stackrel {{c}} {{=}} \right. \tag {3} \\ \left\{\mathcal {V} _ {A} ^ {\Pi} (\boldsymbol {x}, \boldsymbol {X}) \right\} _ {\boldsymbol {x} \in (\{0, 1 \} ^ {*}) ^ {n}, \boldsymbol {X} \in s u p p (\mathcal {P})}. \\ \end{array}
$$

If the left-hand and right-hand sides in Eq. (3) are statistically indistinguishable, $\mathcal { R V } _ { A } ^ { \Pi } ( { \pmb x } , { \pmb X } )$ is a statistical refined view.

Definition $\textbf { 5 } ( ( t , n , \mathcal { E } ) – \mathrm { T P M D P } )$ . A protocol Π satisfies computational $( t , n , \mathcal { E } ) – T P M D P$ if for $A \in \mathcal { A } _ { t } = \{ A \subset [ n ] \mid | A | \leq$ t}, there exists a computational refined view $\mathcal { R V } _ { A } ^ { \Pi } ( { \pmb x } , { \pmb X } )$ such that for all $j \in { \bar { A } } ,$ , for all $S \subset \{ \mathcal { R } \mathcal { V } _ { A } ^ { \Pi } ( { \pmb x } , { \pmb X } ) \}$ }x∈({0,1}∗)n,X∼P , and for all j-neighboring inputs x and ${ \pmb x } ^ { \prime } .$ :

$$
\operatorname * {P r} [ \mathcal {R V} _ {A} ^ {\Pi} (\boldsymbol {x}, \boldsymbol {X}) \in S ] \leq e ^ {\epsilon_ {j}} \operatorname * {P r} [ \mathcal {R V} _ {A} ^ {\Pi} (\boldsymbol {x} ^ {\prime}, \boldsymbol {X}) \in S ] + \delta_ {j}, \tag {4}
$$

where X denotes the collection of randomization terms in the protocol Π. When there exists a statistical refined view for each $A \in { \mathcal { A } } _ { t }$ satisfying Eq. (4), then we say the protocol Π satisfies statistical $( t , n , \mathcal { E } ) – T P M D P$

Definition 5 implies that, in a TPMDP mechanism, a set of adversaries $A \in \mathcal A _ { t }$ cannot distinguish with high certainty between the refined views for neighboring inputs. As the refined view computationally (statistically) covers the information in the running of the mechanism, we can ensure the privacy of all parties in the computational or statistical sense.

Comparisons with existing works: In comparison to existing definitions of multi-party DP in [5], [7], [15], our proposed definition is more comprehensive while remaining consistent with them. Specifically, when degenerating to the non-personalized setting (i.e., $( \epsilon _ { i } , \delta _ { i } ) \equiv ( \epsilon , \delta )$ for some $( \epsilon , \delta ) )$ , our definition of computational TPMDP is equivalent to the definition of computational multi-party DP (SIM-CDP) as presented in [15]. Additionally, by leveraging the post-processing property of DP [9], we can establish the consistency of our definition with TMDP in [5], which is solely based on the distribution of the view of parties when TPMDP degenerates to the non-personalized setting. Regarding the comparison with the definition for PLDP [7], it is a special case for statistical TPMDP with $t = n - 1$ .

# IV. MULTI-PARTY GAUSSIAN MECHANISM

We present an easy-to-implement multi-party Gaussian mechanism that is well-suited for TPMDP with different parameters $( t , n , \mathcal { E } )$ . We choose to use the Gaussian mechanism for several reasons: 1) Gaussian noise is prevalent and can be easily generated in both software and hardware [16], [17]; 2) Gaussian noise possesses the property that the sum of independent Gaussian noises is also Gaussian; and 3) Gaussian noise simplifies the analysis of mechanism utility, as the problem of minimizing utility loss measured by the overall noise variance can be cast into a linear programming (LP) problem. However, the LP problem for finding the optimal variances for the multi-party Gaussian mechanism includes an exponential number of constraints, making it computationally expensive to solve using the state-of-the-art generic LP solver [13], which requires storage and running time exponential in n. To address this challenge, we exploit the structure of the LP problem and develop an efficient solver that can solve the problem with ${ \mathcal { O } } ( n )$ storage and running time. The utility of our mechanism surpasses the current TMDP and PLDP mechanisms [5], [7].

# A. Algorithmic Description

Different from the general function $f ( \cdot ) ~ = ~ \{ f _ { i } ( \cdot ) \} _ { i \in [ n ] }$ considered in MPC, where the functions $f _ { i } ( \cdot ) , i \in [ n ]$ can be arbitrarily different, in the multi-party Gaussian mechanism, we consider a less general form of $f ,$ where $f _ { i } ( \cdot )$ is either equal to $F ( \cdot )$ or ⊥. Here, $F ( \cdot )$ represents an arbitrary function, and ⊥ is a symbol with no information. Thus, $f$ computes F and reveals the result to a subset of parties while outputting ⊥ to the others. This idea is similar to that adopted in MPC for defining protocols where the output is revealed only to a subset of parties. Note that there is no loss of generality since a general function can be composed of a finite number of such less general functions, which satisfies a TPMDP requirement (see the composition theorem in the full version [18]).

To simplify notation, we define the set of active users as $U ^ { + } = \{ i \in [ n ] | f _ { i } ( \pmb { x } ) = F ( \pmb { x } ) \}$ , where the non-active set is the complement of $U ^ { + }$ and is denoted by $U ^ { - }$ . Additionally, we define the active adversary structure $\mathcal { A } _ { t } ^ { + }$ as the set of adversarial sets containing at least one active user, that is, $\mathcal { A } _ { t } ^ { + } = \{ A \in \mathcal { A } _ { t } | A \cap U ^ { + } \bar { \neq } \emptyset \}$ .

The general algorithm of the multi-party Gaussian mechanism is presented in Alg. 1. This algorithm perturbs the query results by adding the sum of all parties’ Gaussian noises in an MPC protocol for $f .$

# Algorithm 1 Multi-party Gaussian mechanism

1: Input: $F ( \cdot ) , ( t , n , \mathcal { E } ) , \mathbf { \boldsymbol { x } } , U ^ { + }$   
2: Each party i computes a noise variance $\sigma _ { i } ^ { 2 }$   
3: Each party i generates $X _ { i } \sim \mathcal { N } ( 0 , \sigma _ { i } ^ { 2 } I )$   
4: All parties execute an MPC protocol π with inputs x, X and an output $\Pi _ { i } ( { \pmb x } , { \pmb X } ) = \ \mathsf { \bar { F } } ( { \pmb x } ) + \Sigma _ { j = 1 } ^ { n } X _ { j }$ to $i \in U ^ { + }$ and $\perp { \sf t o } \ i \in U ^ { - }$ , where Πi denotes the function w.r.t the i-th output of Π

The multi-party Gaussian mechanism will not result in significant communication overhead to the original MPC protocol since only n addition gates need to be included. For instance, if the traditional Shamir secret-sharing scheme [10] is employed, this can be accomplished in O(1) extra rounds with an ${ \mathcal { O } } ( n )$ additional message complexity to each party.

# B. Privacy Analysis and Optimization Objective

This section discusses the conditions under which the multiparty Gaussian mechanism satisfies TPMDP. To maximize the utility of the mechanism while ensuring TPMDP, we formulate a variance-minimization problem.

We introduce the concept of partial $\ell _ { 2 } { \mathrm { - s e n s i t i v i t y } } ,$ which measures the maximum difference in outcomes of a query function on neighboring inputs (cf. Definition 6). This sensitivity value is essential in determining the appropriate noise variance to ensure TPMDP.

Definition 6 (Partial ℓ2-sensitivity). Given a function $F : \cdot$ $( \{ 0 , 1 \} ^ { * } ) ^ { n } \to \mathbb { R } ^ { d }$ , the i-th partial $\ell _ { 2 } \cdot$ -sensitivity of F is

$$
\Delta_ {2, i} F = \max _ {x, y \in (\{0, 1 \} ^ {*}) ^ {n}, x \simeq y} \| F (x) - F (y) \| _ {2}.
$$

We demonstrate that the privacy guarantee of the multiparty Gaussian mechanism can be assessed by comparing partial sums of $\{ \sigma _ { i } ^ { 2 } \} _ { i \in [ n ] }$ and $\{ \sigma _ { \Gamma _ { i } } ^ { 2 } \} _ { i \in [ n ] }$ , where $\sigma _ { \Gamma _ { 3 } } ^ { 2 }$ denotes the sufficient noise variance for Gaussian mechanisms with parameters $\Gamma _ { i } \triangleq ( \epsilon _ { i } , \delta _ { i } , \Delta _ { 2 , i } F )$ . The theorem for the multiparty Gaussian mechanism is established as follows. We defer the proof of Theorem 1 to the full version [18].

Theorem 1. A multi-party Gaussian mechanism Π satisfies statistical $( t , n , \mathcal { E } )$ -TPMDP if the MPC protocol π in Alg. 1 is statistically τ -private where $\tau \geq t$ and σ satisfies

$$
\Sigma_ {i \in \bar {A} _ {j}} \sigma_ {i} ^ {2} \geq \sigma_ {\Gamma_ {j}} ^ {2}, \forall j \in [ n ], \forall A _ {j} \in \mathcal {A} _ {t} ^ {+} \cap \{A | j \in \bar {A}, | A | = t \}, \tag {5}
$$

where $\bar { A }$ denotes the complement of the set A. Π satisfies computational (t, n, E)-TPMDP if π is computationally $\tau \mathrm { - }$ private where $\tau \geq t$ and Eq. (5) holds.

The theory indicates that a specific multi-party Gaussian mechanism can satisfy a given TPMDP requirement with parameters $n , t ,$ and $\mathcal { E } .$ To optimize the utility of the multiparty Gaussian mechanism, we aim to minimize the additive noise variance while satisfying the TPMDP constraints given by Eq. (5). This involves finding each party’s variance $\sigma _ { i } ^ { 2 }$ by solving the following optimization problem:

$$
\min _ {\sigma = \left\{\sigma_ {i} \right\} _ {i = 1} ^ {n}} \Sigma_ {i = 1} ^ {n} \sigma_ {i} ^ {2} \tag {6}
$$

$$
\Sigma_ {i \in \bar {A} _ {j}} \sigma_ {i} ^ {2} \geq \sigma_ {\Gamma_ {j}} ^ {2},   \forall j \in [ n ], \forall A _ {j} \in \mathcal {A} _ {t} ^ {+} \cap \{A | j \in \bar {A}, | A | = t \}.
$$

The optimization problem described in Eq. (6) has noise variances $\sigma _ { i } ^ { 2 } , i \in [ n ]$ as decision variables. This indicates that the problem can be classified as a linear programming (LP) problem. For the sake of convenience, we define the objective function in Eq. (6) as $v _ { \sigma } .$ , such that $\textstyle v _ { \pmb { \sigma } } : = \sum _ { i = 1 } ^ { n } \sigma _ { i } ^ { 2 }$ .

# C. Utility-Maximizing Algorithm

In this section, we present an efficient method to obtain a utility-optimal multi-party Gaussian mechanism by solving the optimal noise variances in Eq. (6). Eq. (6) is an $\mathrm { L P }$ problem, which can be solved using a generic solver to obtain the optimal mechanism. The current state-of-the-art complexity of generic solvers for LP problems is $\widetilde { \mathcal { O } } ( ( n n z +$ $r a n k ^ { 2 } ) \sqrt { r a n k } \log \left( 1 / \epsilon \right) )$ [13], where nnz and rank refer to the number of non-zero entries and rank of the constraint matrix, respectively, and ϵ is the approximation parameter. The complexity of solving Eq. (6) is polynomial in n, with the order depending on t. This complexity limits the scalability of the multi-party Gaussian mechanism for large values of t. To overcome this limitation, we propose a method that solves Eq. (6) exactly, i.e., obtaining an exact solution in a finite number of iterations. Specifically, our method requires only ${ \mathcal { O } } ( n )$ computations. We provide a detailed comparison between the complexity of the generic LP solver and our method at the end of this subsection. Besides, the utility of our multi-party Gaussian mechanism, as measured by the noise variance, is superior to both TMDP and PLDP mechanisms [5], [7].

We present our results for two cases. First, we consider a special case where $U ^ { + } = \left[ n \right] ( \mathrm { i } . \mathrm { e } .$ , all parties are active), which implies $\mathcal { A } _ { t } ^ { + } = \mathcal { A } _ { t }$ . We then extend our results to the general case where $U ^ { + } \subset [ n ]$ . We exclude two trivial cases from our analysis, where $U ^ { + } = \varnothing$ and $t = 0$ , as in both cases, $\mathcal { A } _ { t } ^ { + } = \emptyset$ , which means that no noise is required. Therefore, we focus on $1 \leq | U ^ { + } | \leq n$ and $1 \leq t \leq n - 1$ in the subsequent analysis. The proofs for all results presented in this section can be found in the full version [18].

# 1) Case 1: $U ^ { + } = [ n ]$

Regarding Case 1, based on a dedicated analysis of the structure of the LP problem in Eq. (6), we discover that the optimal solution can be represented concisely. Specifically, the solution can be found as follows: 1) Each party computes sufficient variances for all parties’ DP requirements; 2) A uniform noise variance is assigned to the parties to satisfy the majority of the privacy requirements; 3) Additional noise variance is assigned to a party if the uniform noise variance is insufficient to meet his/her privacy requirement.

For ease of elaboration, we denote $\sigma _ { \Gamma _ { ( i ) } }$ as the i-th largest element in $\{ \sigma _ { \Gamma _ { j } } \} _ { j \in [ n ] }$ . The exact method for computing the optimal $\sigma _ { i } ^ { 2 } , \ i \in [ n ]$ for Eq. (6) in Case 1 is synopsized in Alg. 2. Specifically, after computing ξ in $\mathcal { O } ( 1 )$ steps, the computation of $\sigma _ { i } ^ { 2 }$ can be broken down into two parts. The first part involves finding the ξ-th largest element in $\{ { \sigma _ { \Gamma _ { j } } } \} _ { j \in [ n ] } ,$ which has a complexity of ${ \mathcal { O } } ( n )$ . The second part is a closedform expression with a complexity of $\mathcal { O } ( 1 )$ . Therefore, the overall complexity is ${ \mathcal { O } } ( n )$ .

Algorithm 2 Optimal parameter selection for multi-partyGaussian mechanism when $U ^ { + } = [ n ]$ 214号  
1: Input: $F$ , $(t,n,\mathcal{E})$ , $i$ 2: Output: Optimal $\sigma_i^2$ for party $i$ in Eq. (6)  
3: Compute $\sigma_{\Gamma_j}$ for $j\in [n]$ and $\xi = \min (\lfloor \frac{2n - t}{n - t}\rfloor ,t + 1)$ 4: Find the $\xi$ -th largest element in $\{\sigma_{\Gamma_j}\}_{j\in [n]}$ , $\sigma_{\Gamma_{(\xi)}}$ 5: Set $\sigma_i^2 = \frac{1}{n - t}\sigma_{\Gamma_{(\xi)}}^2$ if $\sigma_{\Gamma_i}\leq \sigma_{\Gamma_{(\xi)}}$ and $\sigma_i^2 = \sigma_{\Gamma_i}^2 -\frac{n - t - 1}{n - t}\sigma_{\Gamma_{(\xi)}}^2$ if $\sigma_{\Gamma_i} > \sigma_{\Gamma_{(\xi)}}$

Theorem 2. For Case 1, Alg. 2 outputs the optimal entries $\sigma _ { i } ^ { 2 } , \ i \in [ n ]$ Eq. (6)al overa, where ${ \mathcal { O } } ( n )$ $v _ { \pmb { \sigma } } = \Sigma _ { i = 1 } ^ { \xi - 1 } \sigma _ { \Gamma _ { ( i ) } } ^ { 2 } \dot { + }$ $\begin{array} { r } { \big ( \frac { 2 n - t } { n - t } - \xi \big ) \sigma _ { \Gamma _ { ( \xi ) } } ^ { 2 } , } \end{array}$ n−t $\begin{array} { r } { \xi = \operatorname* { m i n } \big ( \lfloor \frac { 2 n - t } { n - t } \rfloor , t + 1 \big ) } \end{array}$

Theorem 2 demonstrates that in the case where $U ^ { + } = [ n ]$ , each party can determine the optimal variance with a complexity of ${ \mathcal { O } } ( n )$ . The theorem further shows that when the threshold t is relatively small, i.e., $t \le p n$ for some constant $p < 1$ , the value of $\xi$ is bounded by $\mathcal { O } ( 1 )$ . In this scenario, the overall noise variance $v _ { \sigma }$ is $\mathcal { O } ( 1 )$ . However, if the threshold t is close to n $( { \bf e . g . } , n - t = \mathcal { O } ( 1 ) )$ , the value of $\xi$ scales as ${ \mathcal { O } } ( n )$ . Consequently, the overall noise variance is essentially the sum of required noise variances of a constant percentage of learners with more stringent privacy requirements.

# 2) Case 2: $U ^ { + } \subset [ n ]$

In this subsection, we extend our analysis to the general case where $U ^ { + } \subset [ n ]$ . We assume that $U ^ { + }$ has size $\eta + 1$ , where $0 \leq \eta \leq n - 1$ , and for convenience, we reparameterize $U ^ { + }$ as $\{ 1 ^ { + } , 2 ^ { + } , \dots , ( \eta + 1 ) ^ { + } \}$ and $U ^ { - } ~ \mathrm { a s } ~ \{ 1 ^ { - } , \dots , ( n - \eta - 1 ) ^ { - } \}$ . Let ${ \mathcal { E } } ^ { + }$ and ${ { \mathcal { E } } ^ { - } }$ be the sets of pairs $( \epsilon _ { i } , \delta _ { i } )$ for $i \in U ^ { + }$ and $i \in U ^ { - }$ , respectively, and let $\pmb { \sigma } ^ { + }$ and $\pmb { \sigma } ^ { - }$ be the sets of $\sigma _ { i }$ for $i \in U ^ { + }$ and $i \in U ^ { - }$ , respectively.

As before, we define σΓ + $\sigma _ { \Gamma _ { ( i ^ { + } ) } }$ and σΓ(i−) $\sigma _ { \Gamma _ { ( i ^ { - } ) } }$ as the i-th largest element in $\{ \sigma _ { \Gamma _ { j } } \} _ { j \in U ^ { + } }$ + and $\{ \sigma _ { \Gamma _ { j } } \} _ { j \in U ^ { - } }$ , respectively. The results are classified into four mutually exclusive subcases:

1) Subcase 1: $| U ^ { + } | \geq n - t + 1 ;$   
2) Subcase 2: $| U ^ { + } | = 1 ;$   
3) Subcase $\begin{array} { r } { \mathbf { 3 } \colon 2 \le | U ^ { + } | \le n - t } \end{array}$ and $n - t \left| U ^ { + } \right| \leq 0 ;$   
4) Subcase 4: $2 \leq | U ^ { + } | \leq n - t$ and $n - t | U ^ { + } | > 0 .$

These subcases cover all possibilities for $U ^ { + }$ and t.

Lemma 1. For Subcases 1 and 3, σ is optimal for Eq. (6) if it is optimal for Eq. (6) when replacing $\mathcal { A } _ { t } ^ { + }$ with $\boldsymbol { \mathcal { A } } _ { t } .$ .

According to Lemma 1, determining the optimal value of σ for Subcases 1 and 3 is equivalent to finding the optimal value of σ after substituting $\mathcal { A } _ { t } ^ { + }$ with $\boldsymbol { A } _ { t }$ . This task can be accomplished using Alg. 2.

Lemma 2. For Subcase 2, σ is optimal for Eq. (6) if:

1) when $t \ge 2 , \sigma _ { 1 ^ { + } } ^ { 2 } = 0$ and $\sigma ^ { - }$ is optimal for Eq. (6) with input $( t - 1 , \stackrel { \cdot } { n } - 1 , \mathcal { E } ^ { - } )$ and active set $U ^ { - } ;$   
2) when $\begin{array} { r } { \dot { t } = 1 , \sigma _ { 1 ^ { + } } ^ { 2 } = 0 , \acute { \sigma } _ { i } ^ { 2 } = \frac { 1 } { n - 1 } \sigma _ { \Gamma _ { ( 1 ^ { - } ) } } ^ { 2 } f o r i \in U ^ { - } . } \end{array}$

Lemma 3. For Subcase 4, let $\alpha = \operatorname* { m a x } \{ \sigma _ { \Gamma _ { ( 1 ^ { - } ) } } , \sigma _ { \Gamma _ { ( 2 ^ { + } ) } } \}$ and $\beta = \operatorname* { m a x } \{ \sigma _ { \Gamma _ { ( 1 ^ { + } ) } } , \sigma _ { \Gamma _ { ( 2 ^ { - } ) } } \}$ . Then σ is optimal for Eq. (6) if:

1) when $\begin{array} { r } { t = 1 \ o r \ \alpha \leq \beta , \ \sigma _ { i } ^ { 2 } = \frac { 1 } { n - \eta - t } \alpha ^ { 2 } \ f o r \ i \in U ^ { - } } \end{array}$ 1n−η−t α2 for i ∈ U −, and $\sigma _ { i } ^ { 2 } = \operatorname * { m a x } \{ 0 , \sigma _ { \Gamma _ { i } } ^ { 2 } - \alpha ^ { 2 } \} f o r \ i \stackrel { . . } { \in } \breve { U } ^ { + } ,$ ;   
2) when $t ~ \geq ~ 2 ~ a n d ~ \alpha ~ > ~ \beta , ~ \sigma _ { i } ~ = ~ 0 ~ i f ~ i ~ \in ~ U ^ { + } , ~ \sigma _ { i } ^ { 2 } ~ =$ ≥α2 n−η−t−1 $\begin{array} { r } { \alpha ^ { 2 } \ - \ \frac { n - \eta - t - 1 } { n - n - t } \beta ^ { 2 } \ i f \ i \ \in \ U ^ { - } } \end{array}$ and $\sigma _ { \Gamma _ { i } } ~ = ~ \sigma _ { \Gamma _ { ( 1 ^ { - } ) } } ,$ and σ 2i = n $\begin{array} { r } { \sigma _ { i } ^ { 2 } = \frac { 1 } { n - \eta - t } \bar { \beta } ^ { 2 } } \end{array}$ 1−η−t β2 otherwise.

Alg. 3 outlines the complete procedure for all four subcases. Within this algorithm, each learner identifies the subcase under which the parameter setting falls, then calculates the noise variance using the corresponding lemma described above. Like Alg. 2, the computational complexity of Alg. 3 is primarily determined by the process of finding $\sigma _ { \Gamma } .$ i for $i \in [ n ]$ and the ξ-th largest element for some $\xi \in [ n ]$ . Consequently, the complexity of Alg. 3 is ${ \mathcal { O } } ( n )$ .

Theorem 3. Alg. 3 outputs the optimal $\sigma _ { i } ^ { 2 } , i \in [ n ] f o r E q . ( 6 )$ . The computation takes ${ \mathcal { O } } ( n )$ steps. The optimal overall noise variance is

$$
v _ {\sigma} = \left\{ \begin{array}{l l} \Sigma_ {i = 1} ^ {\xi - 1} \sigma_ {\Gamma_ {(i)}} ^ {2} + \left(\frac {2 n - t}{n - t} - \xi\right) \sigma_ {\Gamma_ {(\xi)}} ^ {2}, & \text { Subcases   } 1 \& 3 \\ \Sigma_ {i = 1} ^ {\xi - 1} \sigma_ {\Gamma_ {(i ^ {-})}} ^ {2} + \left(\frac {2 n - t - 1}{n - t} - \xi\right) \sigma_ {\Gamma_ {(\xi^ {-})}} ^ {2}, & \text { Subcase   } 2 \\ \sigma_ {\Gamma_ {(1)}} ^ {2} + \frac {t - 1}{n - | U ^ {+} | - t + 1} \sigma_ {\Gamma_ {(2)}} ^ {2}, & \text { Subcase   } 4, \end{array} \right. \tag {7}
$$

where ξ = min $\textstyle ( { \bigl \lfloor } { \frac { 2 n - t } { n - t } } { \bigr \rfloor } , t + 1 )$ in Subcases 1 and 3, and $\xi =$ min $\textstyle { \big ( } { \big \lfloor } { \frac { 2 n - t - 1 } { n - t } } { \big \rfloor } , t { \big ) }$ n t in Subcase 2.

Theorem 3 demonstrates that each learner can achieve the optimal variance with a complexity of ${ \mathcal { O } } ( n )$ for the general case where $U ^ { + } \subset [ n ]$ . Regarding the overall noise variance $v _ { \sigma } ,$ , if the threshold $t \le p n$ for a constant $p \leq 1$ , similar to the case $U ^ { + } = \left[ n \right]$ , it holds that $v _ { \sigma } = \mathcal { O } ( 1 )$ for Subcases

Algorithm 3 Optimal parameter selection for multi-party Gaussian mechanism   
1: Input: $F$ , $(t,n,\mathcal{E})$ , $U^{+}$ , $i$ 2: Output: Optimal $\sigma_{i}^{2}$ for party $i$ in Eq. (6)
3: Compute $\sigma_{\Gamma_j}$ for $j\in [n]$ and $\xi = \min \left(\lfloor \frac{2n - t}{n - t}\rfloor ,t + 1\right)$ 4: Find the largest and 2-nd largest elements in $\{\sigma_{\Gamma_j}\}_{j\in U^{-}}$ , $\sigma_{\Gamma_{(1^-)}}$ and $\sigma_{\Gamma_{(2^-)}}$ 5: Find the largest and 2-nd largest element in $\{\sigma_{\Gamma_j}\}_{j\in U^{+}}$ , $\sigma_{\Gamma_{(1^+)}}$ and $\sigma_{\Gamma_{(2^+)}}$ 6: Set $\alpha = \max \{\sigma_{\Gamma_{(1^-)}},\sigma_{\Gamma_{(2^+)}}\}$ and $\beta = \max \{\sigma_{\Gamma_{(1^+)}},\sigma_{\Gamma_{(2^-)}}\}$ 7: switch (Subcase)
8: case Subcase 1, Subcase 3:
9:    Compute $\sigma_i^2$ using Alg. 2 with input $(F,(t,n,\mathcal{E}),i)$ 10:    Break
11: case Subcase 2:
12:    if $i\in U^{+}$ then
13:    Set $\sigma_i^2 = 0$ 14:    else if $t\geq 2$ then
15:    Compute $\sigma_i^2$ via Alg. 2 with $(F,(t - 1,n - 1,\mathcal{E}^{-}),i)$ 16:    else
17:    Set $\sigma_i^2 = \frac{1}{n - 1}\sigma_{\Gamma_{(1^-)}}^2$ 18:    end if
19:    Break
20: case Subcase 4:
21:    if $t = 1$ or $\alpha \leq \beta$ then
22:    if $i\in U^{+}$ then
23:    Set $\sigma_i^2 = \max \{0,\sigma_{\Gamma_i}^2 -\alpha^2\}$ 24:    else
25:    Set $\sigma_i^2 = \frac{1}{n - |U^+| - t + 1}\alpha^2$ 26:    end if
27:    else
28:    if $i\in U^{-}$ and $\sigma_{\Gamma_i} = \sigma_{\Gamma_{(1^-)}}$ then
29:    Set $\sigma_i^2 = \alpha^2 -\frac{n - |U^+| - t}{n - |U^+| - t + 1}\beta^2$ 30:    else if $i\in U^{-}$ then
31:    Set $\sigma_i^2 = \frac{1}{n - |U^+| - t + 1}\beta^2$ 32:    else
33:    Set $\sigma_i^2 = 0$ 34:    end if
35:    end if
36: end switch

1-4 when considering the dependence of n. However, when t is close to n $( { \bf e . g . } , n - t = \mathcal { O } ( 1 ) )$ , the parameter settings in Subcase 4 do not exist. In Subcases $1 { - } 3 , \xi = { \cal O } ( n )$ , and the overall noise variance essentially equals the sum of the required noise variances of a constant percentage of learners with more stringent privacy budgets.

Comparison with existing works: Table I summarizes the space and time complexity comparisons between Alg. 3 and a generic LP solver for Eq. (6). The results demonstrate that, when $t = p \cdot n$ for $p < 1$ , Alg. 3 reduces the space and time complexities of the generic solver from exponential to ${ \mathcal { O } } ( n )$ .

Regarding utility, the previous TMDP mechanism [5] did not consider personalized privacy requirements for each party. In a multi-party Gaussian mechanism satisfying TMDP, we replace each party $i \ ' s$ required noise variance $\sigma _ { \Gamma _ { i } } ^ { 2 }$ with the largest of their required noise variances $\sigma _ { \Gamma _ { ( 1 ) } } ^ { 2 }$ . Compared to our TPMDP multi-party Gaussian mechanism, the overall noise variance $v _ { \sigma }$ can be prohibitively large if the threshold value is close to n and all parties’ privacy requirements are heterogeneous. For example, if $\sigma _ { \Gamma _ { ( 2 ) } } \ll \sigma _ { \Gamma _ { ( 1 ) } }$ and $n - t = \mathcal { O } ( 1 )$ , it holds that vTPMDPσ /vTMDPσ ≤ O(1) · max{ 1n , σ $\begin{array} { r } { v _ { \sigma } ^ { \mathrm { T P M D P } } / v _ { \sigma } ^ { \mathrm { T M D P } } \leq \mathcal { O } ( 1 ) \cdot \operatorname* { m a x } \{ \frac { 1 } { n } , \frac { \sigma _ { \Gamma _ { ( 2 ) } } ^ { 2 } } { \sigma _ { \Gamma _ { ( 1 ) } } ^ { 2 } } \} \ll 1 } \end{array}$ σ2Γ(2) 2Γ (1) and for sufficiently large n in Subcases 1 and 3. Here, $v _ { \sigma } ^ { \mathrm { T M D P } }$ denote the optimal variance sums of TPMDP $v _ { \sigma } ^ { \mathrm { T P M D P } }$ vσ TPMDP and TMDP multi-party Gaussian mechanisms, respectively. Compared to the PLDP mechanism [19], our mechanism has a prominent advantage when $t \le p n$ . In this case, the overall noise variances of PLDP and our mechanisms scale as ${ \mathcal { O } } ( n )$ and O(1), respectively, provided that $\sigma _ { \Gamma _ { i } } ~ \in ~ [ C _ { 1 } , C _ { 2 } ]$ for $i \in [ n ]$ and $0 < C _ { 1 } < C _ { 2 }$ .

TABLE I: Complexity for generic LP solver and Alg. 3. $H ( p ) \ = \ p \log p + ( 1 - p ) \log ( 1 - p )$ is the entropy for $p < 1$ . The space complexity is evaluated using the size of codes and inputs the algorithm requires. The time complexity for the generic LP solver is from the result in [13] (i.e., $\widetilde { \mathcal { O } } ( ( n n z + r a n k ^ { 2 } ) \sqrt { r a n k } \log \left( 1 / \epsilon \right) )$ , where nnz and rank denote the number of non-zero entries and rank of the constraint matrix, and ϵ measures the suboptimality of the LP solver), after a plain application of Stirling’s formula. 

<table><tr><td></td><td>Space complexity</td><td>Time complexity</td></tr><tr><td>Generic solver $(t = C)$ </td><td> $\mathcal{O}(n^{C+2})$ </td><td> $\widetilde{\mathcal{O}}(n^{C+2.5})\log(1/\epsilon)$ </td></tr><tr><td>Generic solver $(t = p \cdot n)$ </td><td> $\mathcal{O}(n^{1.5}2^{H(p)n})$ </td><td> $\widetilde{\mathcal{O}}(n^{2}2^{nH(p)})\log(1/\epsilon)$ </td></tr><tr><td>Alg. 3</td><td> $\mathcal{O}(n)$ </td><td> $\mathcal{O}(n)$ </td></tr></table>

# V. EVALUATIONS BY EXPERIMENTS

This section assesses the utility and scalability of our multiparty Gaussian mechanism. Our findings demonstrate that our mechanism surpasses the heuristic non-threshold approach and the PLDP method in terms of utility and is even comparable to a centralized approach. Furthermore, our mechanism achieves better utility than the TMDP mechanism, particularly when the threshold value t approaches n or the proportion of conservative parties is relatively low. Additionally, our algorithm (Alg. 3) significantly outperforms the leading generic LP solver concerning running time and storage requirements.

# A. Utility Loss

Experimental setup: We evaluate the performance of our proposed mechanism by measuring the utility loss in two common query functions: count and linear regression. Count is a basic operation in complex data analytic tasks, while linear regression is a fundamental machine learning algorithm. We measure the utility loss of the mechanism using rooted mean squared error (RMSE). Additionally, we compare our proposed multi-party Gaussian mechanism (referred to as G in this section) with several baseline methods:

• non-thre: This baseline does not consider collusion thresholds. It is a special case of Alg. 3 when $t = n - 1$ .   
• TMDP [5]: This baseline does not consider personalized privacy budgets. Instead, each party’s privacy budget is replaced with the most stringent one. This approach is also a special case of Alg. 3.

![](images/2e068b29e69fd026e776f5e638876a329742c27759187558df5b192fede2430d.jpg)  
(a) Impact of ρ

![](images/2e286cbe00cbb9e0b2a36e6be7dc9d484fac08792cd9bcbb7824f5e461683273.jpg)



(b) Impact of fC

![](images/48b2d9153a2f49f701465bb62d823275c381e58c210be9abc0563ac65c6ef260.jpg)



(c) Impact of n

![](images/4cac6cc5a727b958ed8aaff52534d1600f36c67010c1c81e678b84c7069d0dfb.jpg)



(d) Impact of t   
Fig. 2: Utility loss for count. G is our proposed mechanism; MIN and non-thre are centralized and non-threshold baselines, respectively; Sample, PLDP, and TMDP stand for the Sample, randomized response, and TMDP mechanisms.

• MIN: This is a centralized baseline where a trusted third party gathers data from all parties, computes the query function with additive Gaussian noise, and then releases the results to the active parties.   
• Sample [11]: This state-of-the-art centralized PDP mechanism divides parties into stringent and non-stringent groups based on a predetermined budget $\epsilon ^ { ( t ) }$ . The data for parties with stringent privacy budgets are ignored with high probability, leading to a decrease in the required noise level. Following [11], we take $\begin{array} { r } { \epsilon ^ { ( t ) } = \frac { 1 } { n } \Sigma _ { i \in [ n ] } \epsilon _ { i } } \end{array}$ to achieve good accuracy results in various tasks.   
• PLDP [19]: We also include the PLDP mechanism as a baseline, which uses the randomized response for count and input perturbation for linear regression.   
• non-pri: For linear regression, we compare our mechanism with the non-private linear regression algorithm.

Datasets: We evaluate mechanisms for count on synthetic data. We sample a dataset with n binary values, with a default value of $n = 1 0 0 0$ . The density parameter $\rho ,$ which controls the fraction of 1’s in the dataset, is set to 0.15 by default. For linear regression, we use a real-world revenue dataset [20] that contains 5 features: the number of children, gender, age, educational level, and annual income for prediction. This dataset comprises 2.5 million records. For training, we use a default value of $n = 5 \times 1 0 ^ { 4 }$ data points, which are normalized to the range of [-1, 1] for each attribute. In each experiment, the data are distributed randomly among all parties.

Privacy budgets and thresholds: We adopt a methodology similar to [11] to randomly assign parties into three groups based on their privacy consideration. The groups are 1) conservative, comprising parties with high privacy consideration, 2) moderate, comprising parties with medium consideration, and 3) liberal, comprising parties with low consideration. We denote the fractions of conservative and moderate parties as $f _ { C }$ and $f _ { M }$ , respectively. The remaining fraction of liberal parties is represented by $f _ { L } \ = \ 1 - \ f _ { C } - f _ { M }$ . The default values for $f _ { C }$ and $f _ { M }$ are set to 0.54 and 0.37, respectively. We set the privacy budget parameters δi = 110n $\begin{array} { r } { \delta _ { i } = \frac { 1 } { 1 0 n } } \end{array}$ for $i \in [ n ]$ ], which is advised as a small multiple of $\begin{array} { l } { { \frac { 1 } { n } } ^ { \ } \ [ 1 6 ] } \end{array}$ . To select values for $\epsilon _ { i } , i \in [ n ]$ , we randomly choose values for parties in conservative and moderate groups from the intervals $[ \epsilon _ { C } , \epsilon _ { M } ]$ ] and $[ \epsilon _ { M } , \epsilon _ { L } ] .$ , respectively, while fixing $\epsilon _ { i } ~ = ~ \epsilon _ { L }$ for liberal parties. The values for $\epsilon _ { C } , \epsilon _ { M }$ , and $\epsilon _ { L }$ are 0.01, 0.2, and 1.0, respectively. In our experiments, we set the threshold parameter t to ⌊0.5n⌋ by default.

Results for count: Fig. 2 displays the utility of different mechanisms for count queries. To obtain these results, we randomly select $U ^ { + }$ from subsets of [n]. We repeat each mechanism for each configuration over 100 times and present the average results. Overall, when $t = \lfloor 0 . 5 n \rfloor$ , non-thre performs significantly worse than other mechanisms. G, TMDP, and MIN achieve similar utility in most cases. G performs better than TMDP when the fraction of conservative parties $f _ { c }$ is relatively small, or when the threshold value t is close to n.

1) Impact of data density: Fig. 2a shows that the utility loss of G, TMDP, MIN, non-thre, and PLDP remains constant when data density $\rho$ varies. The utility of G and TMDP is similar to MIN’s and much better than that of non-thre and PLDP. The utility loss of Sample increases linearly with $\rho .$ This can be explained by the fact that for smaller values of $\rho ,$ Sample discards mostly $0 ^ { \cdot } \mathrm { s } ,$ resulting in a minor loss of accuracy. For larger ρ, however, Sample ignores too many 1’s, leading to a larger count error.   
2) Impact of the fraction of conservative users: Fig. 2b demonstrates that $G$ outperforms TMDP when $f _ { C } ~ \le ~ 0 . 0 4$ . The utility of PLDP deteriorates sharply when $f _ { C } \geq 0 . 1$ . The centralized mechanism $M I N { \mathrm { : } }$ utility is similar to that of G and TMDP. Sample achieves the best utility since the additive noise is determined by $\epsilon ^ { ( t ) }$ , which is much larger than $\epsilon _ { C } .$ .   
3) Impact of the number of parties: Regarding the impact of n shown in Fig. 2c, MIN, G, and TMDP attain the lowest utility loss for $n \geq 5 0 0 0$ . Other mechanisms experience increasing utility loss as n increases. This is because, for Sample, the discarded data increase linearly with n, while for non-thre and PLDP, the noise variance increases linearly with $n .$   
4) Impact of the collusion threshold: Fig. 2d examines the impact of t and shows that except for G and TMDP, other mechanisms are not sensitive to changes in $t ,$ as only G and TMDP consider the collusion thresholds. The utility loss of G is similar to that of MIN for t < 700 and better than that of PLDP when $t < 9 0 0$ . Comparing G and TMDP, they have similar utility for $t \le 9 0 0$ . When $t > 9 0 0 .$ , G achieves significantly better utility than TMDP.

Results for linear regression: We employ the Functional mechanism proposed in [21] to perform linear regression, where we solve the weight of the linear regression loss function with its coefficients perturbed by the noises generated by our and the baseline Gaussian mechanisms. For each experiment, we conduct 20 runs of five-fold cross-validation.

In this study, we also investigate the impact of fC , n, and t on utility loss for different mechanisms. The results are presented in Fig. 3. Our evaluation reveals that non-thre and PLDP exhibit the largest utility loss. Sample achieves the closest utility to non-pri, which can be attributed to the smaller additive noise variance in Sample than the other three mechanisms. G and TMDP exhibit close performance to MIN in most cases. Additionally, G features better utility than TMDP when the fraction of conservative parties $f _ { c }$ is small, or when the threshold value t is close to n.

![](images/8355f874f3347455bb519a264264fd6260ed5fd6f0bdd946e7b2eef9a88c7505.jpg)



(a) Impact of fC

![](images/b599626a52a31e77b445235a8006dc842b139e3d178ef45b0046c51bd136d011.jpg)  
(b) Impact of n

![](images/bec3f402744962597201d58c467b13217cee746a8bceaf6d51e60d3d3a9a4501.jpg)  
(c) Impact of t   
Fig. 3: Utility loss of different mechanisms for linear regression

1) Impact of the fraction of conservative users: Our results in Fig. 3a reveal that the utility loss of G, non-thre, TMDP, and MIN increases with $f _ { C } .$ Comparing G and TMDP, we observe that G outperforms TMDP slightly for $f _ { C } \leq 0 . 0 1$ .

2) Impact of the number of parties: We observe, in Fig. 3b, that the utility loss for G, TMDP, and MIN roughly decreases as n increases since the increase in accuracy due to more training data exceeds the error caused by additive noise. However, the loss fluctuation of $G , T M D P ,$ and MIN around $n = 1 . 6 \times 1 0 ^ { 5 }$ occurs because the accuracy increase due to more training data does not dominate the noise when n is not sufficiently large. The utility of G, TMDP, and MIN converges to that of non-pri and Sample when $n \geq 9 \times 1 0 ^ { 5 }$ .

3) Impact of the collusion threshold: Fig. 3c demonstrates the impact of t. When $t \leq 2 5 0 0$ , the utility loss of G and TMDP is similar to that of MIN. As t increases, the utility of G and TMDP improves significantly and eventually reaches the maximum value when t approaches n 1. When t is close to $5 \times 1 0 ^ { 4 }$ , the utility of G surpasses that of TMDP.

# B. Scalability

In this study, we evaluate the efficiency of Alg. 3 by comparing it with Gurobi [22], one of the most efficient LP solvers. Fig. 4a presents a comparison of the space cost of Gurobi and our algorithm for varying values of n. We observe that the space requirement of Alg. 3 is insensitive to the change of n and t, and is significantly smaller than that of Gurobi for $n \geq 1 5$ . However, for Gurobi, the space complexity increases as t increases for varying values of n. Specifically, when $t \ : = \ : 0 . 5 n$ , the space complexity of Gurobi increases exponentially with n. Additionally, we analyze the execution time of Gurobi and Alg. 3 with varying values of $n ,$ as shown in Fig. 4b. Consistent with the space requirement analysis in Table I, the execution time of Gurobi increases as t increases for varying $n ,$ while Alg. 3 exhibits constant execution time for different t. As for the impact of $n ,$ we note that when $n \leq 1 2 .$ , the execution time for both Gurobi and Alg. 3 is less than 1 millisecond. However, for larger values of n, the execution time of Gurobi increases sharply (even exponentially for $t = 0 . 5 n )$ , while the execution time of Alg. 3 increases slowly with n. In summary, our results demonstrate that Alg. 3 outperforms Gurobi in terms of both space complexity and execution time for large values of $n ,$ especially when t is a constant factor of n.

![](images/cf0e7a514697a2f61e5637601a63fe9d483975bf408d9e764a9490ba00515d01.jpg)



(a) Space requirement

![](images/a83f0fabab21ff91a666a4462333d1ff4d6527d64c46e709f9d391d36b3f1b47.jpg)



(b) Execution time   
Fig. 4: Efficiency evaluation. The space requirement and execution time of Alg. 3 are independent of t.

# VI. RELATED WORK

Secure multi-party computation (MPC). MPC is a cryptographic technique that enables multiple parties to collaboratively compute a function while ensuring that no collusion of t parties can learn more than the outcome. The extensive literature on MPC provides a variety of protocols for computing a broad range of functions [10], [23], [24], and researchers have focused on reducing the computation and communication costs of MPC protocols [25], [26]. However, MPC has a drawback in that disclosing the exact function output may reveal a party’s private information, especially when some parties collude.

Differential privacy (DP). DP provides a methodology to protect individual input entries by introducing sufficient randomness to the input (input perturbation) or the computation outcome (output perturbation) [9]. Mironov et al. [15] and Jorgensen et al. [11] have respectively generalized DP to handle cases where the adversaries’ computation power is bounded and users’ privacy budgets are personalized. DP mechanisms provide a theoretical guarantee for protecting the private information contained in the output, albeit at the cost of sacrificing data utility due to the applied perturbation. To address this issue, researchers have developed a series of methods to find the optimal DP mechanism with respect to utility [14], [27], [28].

Multi-party differential privacy. Multi-party differential privacy aims to extend DP to accommodate the settings of multi-party computations. Dwork et al. [29] proposed a securely distributed noise generation protocol that enables the construction of multi-party DP mechanisms. Beimel et al. [5] provided a formal definition for threshold multi-party differential privacy (TMDP) and presented two methods for constructing TMDP mechanisms: one by combining MPC and

DP, and the other based on local DP (LDP). Combining MPC and DP typically results in better utility, and many privacypreserving computation systems with stringent utility requirements are constructed using this approach [6], [30], [31]. Recently, Tang et al. [32] proposed a multi-party personalized DP mechanism for marginal release by combining MPC with the Laplace DP mechanism. In contrast, the LDP methods are highly efficient at the expense of utility. Murakami et al. [7] introduced the notion of personalized LDP and optimized its utility. Researchers have proposed several personalized LDP mechanisms for machine learning [33] and statistics tasks [34]. Moreover, Cheu et al. [8] designed multi-party DP mechanisms using an anonymous channel called a shuffler, whose utility is strictly between LDP and centralized DP.

Despite the numerous contributions made in various aspects, there is a noticeable gap in designing multi-party DP mechanisms for the threshold model that allows for personalized privacy budgets while minimizing utility loss.

# VII. CONCLUSIONS

We present TPMDP, a novel general framework for achieving multi-party differential privacy. Our approach enables parties to privately compute a desired function in the presence of at most t colluding semi-honest adversaries while outputting the results to a specified subset. In this process, each party’s personalized privacy requirement is met. We propose an easyto-implement TPMDP mechanism that leverages the Gaussian mechanism. To minimize the overall variance of the Gaussian additive noise, we formulate the problem as an LP and provide an exact algorithm with linear complexity in the number of parties. Our experiments demonstrate the effectiveness of our approach in terms of low utility loss, storage requirements, and running time.

# ACKNOWLEDGMENTS

The research is partially supported by National Key R&D Program of China under Grant No. 2021ZD0110400, Innovation Program for Quantum Science and Technology 2021ZD0302900 and China National Natural Science Foundation with No. 62132018, “Pioneer” and “Leading Goose” R&D Program of Zhejiang, 2023C01029.

# REFERENCES

[1] N. Woolsey, X. Wang, R. Chen, and M. Ji, “FLCD: A flexible low complexity design of coded distributed computing,” IEEE Trans. Cloud Comput., vol. 11, no. 1, pp. 470–483, 2023.   
[2] C. Rublein, F. Mehmeti, M. Towers, S. Stein, and T. F. L. Porta, “Online resource allocation in edge computing using distributed bidding approaches,” in MASS. IEEE, 2021, pp. 225–233.   
[3] S. Paul, P. Sengupta, and S. Mishra, “Flaps: Federated learning and privately scaling,” in MASS. IEEE, 2020, pp. 13–19.   
[4] W. Lin, H. Leng, R. Dou, L. Qi, Z. Pan, and M. A. Rahman, “A federated collaborative recommendation model for privacy-preserving distributed recommender applications based on microservice framework,” J. Parallel Distributed Comput., vol. 174, pp. 70–80, 2023.   
[5] A. Beimel, K. Nissim, and E. Omri, “Distributed private data analysis: Simultaneously solving how and what,” in CRYPTO, 2008, pp. 451–468.   
[6] A. Acar, Z. B. Celik, H. Aksu, A. S. Uluagac, and P. McDaniel, “Achieving secure and differentially private computations in multiparty settings,” in PAC, 2017, pp. 49–59.

[7] T. Murakami and Y. Kawamoto, “Utility-optimized local differential privacy mechanisms for distribution estimation,” in USENIX Security Symposium, 2019, pp. 1877–1894.   
[8] A. Cheu, A. D. Smith, J. Ullman, D. Zeber, and M. Zhilyaev, “Distributed differential privacy via shuffling,” in EUROCRYPT, 2019, pp. 375–403.   
[9] C. Dwork, A. Roth et al., “The algorithmic foundations of differential privacy,” Foundations and Trends® in Theoretical Computer Science, vol. 9, no. 3–4, pp. 211–407, 2014.   
[10] O. Goldreich, Foundations of cryptography: volume 1,2, basic tools & basic applications. Cambridge University Press, 2007/2009.   
[11] Z. Jorgensen, T. Yu, and G. Cormode, “Conservative or liberal? personalized differential privacy,” in ICDE, 2015, pp. 1023–1034.   
[12] K. Jiang, H. Zhou, D. Zeng, and J. Wu, “Multi-agent reinforcement learning for cooperative edge caching in internet of vehicles,” in MASS. IEEE, 2020, pp. 455–463.   
[13] Y. T. Lee and A. Sidford, “Solving linear programs with sqrt(rank) linear system solves,” CoRR, vol. abs/1910.08033, 2019.   
[14] B. Balle and Y. X. Wang, “Improving the Gaussian mechanism for differential privacy: Analytical calibration and optimal denoising,” in ICML, vol. 80, 2018.   
[15] I. Mironov, O. Pandey, O. Reingold, and S. Vadhan, “Computational differential privacy,” in CRYPTO, 2009, pp. 126–142.   
[16] M. Abadi, A. Chu, I. Goodfellow, H. B. McMahan, I. Mironov, K. Talwar, and L. Zhang, “Deep learning with differential privacy,” in CCS, 2016, pp. 308–318.   
[17] R. Iyengar, J. P. Near, D. Song, O. Thakkar, A. Thakurta, and L. Wang, “Towards practical differentially private convex optimization,” in S&P, 2019, pp. 299–316.   
[18] J. Liu, L. Zhang, C. Lv, T. Yu, N. M. Freris, and X.-Y. Li, “TPMDP: Threshold personalized multi-party differential privacy via optimal gaussian mechanism,” CoRR, vol. abs/2305.11192, 2023.   
[19] P. Kairouz, S. Oh, and P. Viswanath, “Secure multi-party differential privacy,” in NIPS, 2015, pp. 2008–2016.   
[20] S. Ruggles, S. Flood, R. Goeken, J. Grover, E. Meyer, J. Pacas, and M. Sobek, “IPUMS USA: Version 9.0 [dataset]. 2019.”   
[21] J. Zhang, Z. Zhang, X. Xiao, Y. Yang, and M. Winslett, “Functional mechanism: regression analysis under differential privacy,” PVLDB, vol. 5, no. 11, pp. 1364–1375, 2012.   
[22] L. Gurobi Optimization, “Gurobi optimizer reference manual,” 2023.   
[23] A. C. C. Yao, “How to generate and exchange secrets,” in FOCS. IEEE Computer Society, 1986, pp. 162–167.   
[24] M. Ben-Or, S. Goldwasser, and A. Wigderson, “Completeness theorems for non-cryptographic fault-tolerant distributed computation,” in STOC, 1988, pp. 1–10.   
[25] Y. Ishai, J. Kilian, K. Nissim, and E. Petrank, “Extending oblivious transfers efficiently,” in CRYPTO, 2003, pp. 145–161.   
[26] D. Demmler, T. Schneider, and M. Zohner, “ABY–A framework for efficient mixed-protocol secure two-party computation.” in NDSS, 2015.   
[27] Q. Geng and P. Viswanath, “The optimal mechanism in differential privacy,” in ISIT, 2014, pp. 2371–2375.   
[28] Q. Geng and P. Viswanath, “Optimal noise adding mechanisms for approximate differential privacy,” IEEE Trans. Inf. Theory, vol. 62, no. 2, pp. 952–969, 2016.   
[29] C. Dwork, K. Kenthapadi, F. McSherry, I. Mironov, and M. Naor, “Our data, ourselves: Privacy via distributed noise generation,” in EUROCRYPT, 2006, pp. 486–503.   
[30] S. Goryczka, L. Xiong, and V. Sunderam, “Secure multiparty aggregation with differential privacy: A comparative study,” in EDBT/ICDT Workshops, 2013, pp. 155–163.   
[31] A. Papadimitriou, A. Narayan, and A. Haeberlen, “Dstress: Efficient differentially private computations on distributed data,” in EuroSys, 2017, pp. 560–574.   
[32] P. Tang, R. Chen, C. Jin, G. Liu, and S. Guo, “Marginal release under multi-party personalized differential privacy,” in ECML PKDD, vol. 13716. Springer, 2022, pp. 555–571.   
[33] X. Li, H. Yan, Z. Cheng, W. Sun, and H. Li, “Protecting regression models with personalized local differential privacy,” IEEE Trans. Dependable Secur. Comput., vol. 20, no. 2, pp. 960–974, 2023.   
[34] Z. Shen, Z. Xia, and P. Yu, “PLDP: personalized local differential privacy for multidimensional data aggregation,” Secur. Commun. Networks, vol. 2021, pp. 6 684 179:1–6 684 179:13, 2021.