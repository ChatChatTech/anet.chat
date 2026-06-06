# Access Control Policy Negotiation for Remote Hot-deployed Grid Services

Wei Xue $^{1}$ , Jinpeng Huai $^{1}$ , Yunhao Liu $^{2}$

$^{1}$ Department of Computer Science and Technology, Beihang University, {xue, huaijp}@act.buaa.edu.cn

$^{2}$ Department of Computer Science, Hong Kong University of Science and Technology, liu@cs.ust.hk

# Abstract

Service grid is a widely distributed environment, where service deployers and containers may be located in different autonomous domains. In such cases, different from traditional scenarios such as J2EE applications, the access control policy should not be determined by a deployer or a container only. Existing grid application deployment solutions do not address this unique requirement. In this paper, we propose a general approach, namely CROWN.ST, an access control policy negotiation solution for remote hot-deployment of grid services in CROWN (China R&D Environment Over Wide-area Network). Based on an access control policy language derived from non-recursive stratified Datalog with constraints, we design the negotiation procedure and three types of meta-policies. We implement a CROWN.ST prototype and evaluate our design by comprehensive experiments.

Keywords: Grid Computing, Security, Trust, CROWN, Policy Negotiation, Implementation.

# 1. Introduction

Grid computing has been an attractive distributed computing paradigm over wide-area network, enabling resource sharing and collaborating across multiple domains[1, 2]. The research described in this paper is a part of a larger project named CROWN (China R&D Environment Over Wide-area Network)[3, 4], which aims to promote the utilization of valuable resources and cooperation of researchers nationwide and worldwide.

The CROWN project is started in late 2003 and sponsored by NSFC (National Natural Science Foundation of China). Several universities and institutes, such as Tsinghua University, Peking University, Computer Network Information Center of CAS (China Academy of Science) and Beihang University have joined CROWN as the initiating partners. Till March 2005, CROWN has gathered more than 0.7 Tflops computational resources, 10TB storage resources and many applications range from gene comparison to climate pattern prediction. Figure 1 illustrates its network topology.

CROWN, as a service grid, with heterogeneous resources wrapped as grid services, can be accessed using standardized protocol, such as Simple Object Access Protocol (SOAP). All the resources being wrapped are hidden from grid users.

For the convenience of developers and administrators of grid applications, we developed a service container to support the maintenance and management of grid services. Each service must be deployed into some target service container before it is accessible to users. We call the one which deploys a grid service as the deployer of the service.

As a grid is often a widely distributed environment, service deployers may be located far away from service containers. Hence, we developed a mechanism for remote and hot grid service deployment[3]. Due to the dynamic nature of grids, remote and hot service deployment is quite often in CROWN. In traditional scenarios such as J2EE application deployments, a deployer is absolutely trusted by an application server (after authentication and authorization) and can determine the security policy of the application by itself. In grid environments, the access control policy of a grid service cannot be determined by the deployer or the container only. Existing grid deployment solutions do not address such a unique requirement[5, 6].

![](images/9714a0c482076eae652be15929322f428952b47946257ca7076f3b832e1717e2.jpg)



Figure 1 Network Topology of CROWN

We propose a general approach, namely CROWN.ST, an access control policy negotiation solution for remote and hot-deployment of grid services. As non-recursive stratified Datalog with constraints is suitable to provide logical semantics for the core parts of the eXtensible Access Control Markup Language (XACML)[7], we propose an access control policy language based on it. We then design a negotiation procedure and meta-policies for the creation of proposals, conflict resolution, and policy validation during negotiations. Thus, deployers and containers are able to specify detailed strategies, automating the policy negotiation procedure and guaranteeing their own concerns are respected. We implement a CROWN.ST prototype and evaluate our design by comprehensive experiments. The preliminary results show that our approach is feasible and effective.

The rest of the paper is organized as follows. Section 2 describes the background and related works. Section 3 briefly introduces our access control policy language and related notions. Section 4 describes the policy negotiation procedure and meta-policies. Section 5 introduces the CROWN.ST prototype implementation. We analyze the complexity of the negotiation procedure in Section 6 and show the experimental results in Section 7. Section 8 concludes our work and presents future directions.

# 2. Background and Related Works

Remote deployment of applications has been investigated by researchers for a long time. Several popular fundamental software platforms, as well as those in the grid community, have remote deployment mechanisms built in[5, 6]. However, up to now, none of them takes access control policy negotiation into account.

# 2.1. Access Control

The remotely deployed grid service wraps raw resources supplied by the container and exposes higher level service interfaces to the end users. Normally, neither the deployer nor the container owns both the grid service and the raw resources. As a nature result, the access control policy for the grid service should be jointly determined by both parties, which is a unique requirement in grid systems, and is not supported by existing access control solutions for grid. For example, PRIMA[8] allows authoritative users to delegate fine-grained privileges to other subjects. The Community Authorization Service (CAS)[9] allows sites to delegate management of a subset of their policy space to the VO. Akenti[10] allows multiple stakeholders to create policy assertions. However, above solutions expect the resources have clear ownership and there exists unique source of authority that has the ultimate authority. They do not support policy negotiation. Beyond grid scenarios, some automatic approaches for security policy reconciliation or negotiation have been proposed. Patrick McDaniel et al identify an efficient algorithm for two-policy reconciliation and suggest efficient heuristics for the detection and resolution of intractable reconciliation[11]. But their target application scenarios are mainly secure group communications, and the policy language they proposed, i.e. Ismene, cannot depict detailed authorization policies. Furthermore, their reconciliation algorithm takes the conservative approach, which is essentially denials take precedence, to synthesize all access control policies and cannot choose different approaches dynamically. Oppositely, our language can be used to depict detailed policies, and meta-policies are used to select different combining algorithms and validation queries according to both parties' requirements.

H. Khurana and V. D. Gligor propose a formal state-transition model for access control policy negotiation[12]. They cast the negotiation problem as one of satisfying diverse coalition-member objectives and a specified set of negotiation constraints. Such a model is based solely on Role-Based Access Control (RBAC) model and does not provide automatic mechanisms for the negotiation. Vijay G. Bharadwaj et al propose a mathematical framework based on semiring-based CSPs (SCSPs) for automatic access control policy negotiation among autonomous domains[13]. But we think that the guidance provided by constraints is not enough to bring out practical solutions for automatic negotiation. We believe that agents for all parties should have prepared rules for negotiation in order to get concrete policies. Instead, we use rule-based meta-policies to determine the policy proposals, combining algorithms and validation queries in which different kinds of constraints can be expressed.

# 2.2. Policy Language

In this subsection, we briefly compare our access control policy language with those policy languages mentioned in literatures.

For every system with security concerns, it is critical to assure that the access control policies of a system are coherent and meet the requirements of stakeholders. So, many access control systems use formal languages or languages with formal semantics to specify their policies. Our access control policy language is based on non-recursive stratified Datalog with constraints and can be used to define the formal semantics of XACML, which is one of the design principles for the language.

Compared with other access control policy languages with logical foundation, the advantage of our language is twofold.

First, our language is non-monotonic. In another words, conclusions drawn before may become wrong when new facts are considered. Many popular trust management languages, such as RT (Role-based Trust-management) framework[14, 15], SD3 (Secure Dynamically Distribute Datalog)[16], and Binder[17], are monotonic, or have monotonic subset, such as Delegation Logic[18]. The hypothesis of monotonicity simplifies the distributed management of policies (through delegation, for example), while it fails to support explicit negation. However, explicit negation is necessary for resolving potential conflicts between proposals of the deployers and containers. Our design addressed this issue. Secondly, we propose to use constructive negation[19] as the operational model for negation when analyzing and validating policies as constraint logic programs. In this way, queries can get constructive answers even when meeting non-ground negative goals during the evaluation. If the negotiation fails, these answers can be returned to the negotiation partner as hints for the next round of negotiation.

# 3. Access Control Policy Language

In this section, we introduce the basic constructs of our access control policy language, which is designed based on the constraint logic programming paradigm. We refer readers to the surveys $[20, 21]$ for details about basic logical terms such as facts, rules, monotonic, stratification, non-recursive and constraints.

# 3.1. Notations

Our policy language is a multi-sorted logic language created from the following alphabet.

Constant Symbols: We regard the sets of subjects, resources, actions and environments as data types and separate them from basic data types such as integer and float. Accordingly, we use constant symbols begin with lowercase letter, such as sub\_1, res\_1, act\_1 and env\_1 to denote elements of these types respectively.

Variable Symbols: We use symbols in forms of Sub, Res, Act and Env as variable symbols ranging over the sets of subject, resources, actions and environments respectively. For simplicity, variable symbols ranging over basic data types are not classified accordingly in this paper. In the following, we refer to constant symbols and variable symbols of type X as “X terms”. For example, sub\_1 is a subject term.

Predicate Symbols: Three types of predicate symbols are considered.

(1) Primitive Constraint Predicate Symbols. Constraints are special relations upon terms of the corresponding constraint domain. A primitive constraint takes the form $r(t_{1},\ldots,t_{n})$ where r is an n-ary primitive constraint predicate symbol, and $t_{i}$ s are terms. A constraint is the conjunction of several primitive constraints.

(2) Built-in Predicate Symbols, including

Ternary predicate symbols, sub\_att, res\_att, act\_att and env\_att. They represent the attributes of subject, resource, action and environment respectively. To illustrate with sub\_att, the first argument is a subject term, and the second is a string term identifying an attribute, while the third is a term of some constraint domain.

4-ary predicate symbols, in the form of permit\_i, where i is a unique ordinal number used to stratify the resulting logic program. The first argument of permit\_i is a subject term, the second is a resource term, and the third is an action term, while the fourth is an environment term. The predicate permit\_i represents a positive authorization explicitly granted to or implicitly derived for the subject.

4-ary predicate symbols, in the form of deny\_i, where i and arguments are the same as permit\_i. The predicate deny\_i represents a negative authorization explicitly granted to or implicitly derived for the subject.

A 4-ary predicate symbol, permit, with the same arguments as permit\_i. The predicate permit represents the positive authorization explicitly granted to or implicitly derived for the subject finally.

A 4-ary predicate symbol, deny, with the same arguments as deny\_i. The predicate deny represents the negative authorization explicitly granted to or implicitly derived for the subject finally

# 3.2. Definition of Authorization Policies

According to the above access control policy language, an authorization policy is defined as follows.

Definition 3.1 An access control policy is a mapping of 4-tuples $(s,r,a,e)$ consisting of a subject, a resource, an action, and an environment, respectively to the set $\{permit,deny\}$ . The policy is specified as a program in non-recursive stratified Datalog with constraint which defines the predicates permit and deny. In following discussions, we will use usual terms such as atom, literal when define the logic rules that can be expressed in our access control policy language.

Definition 3.2 A subject attribute fact is a rule of the form: sub\_att(s,id,val) ← .

Where s is a subject term, id is a string term identifying an attribute, and val is the value of the attribute.

We define resource attribute facts, action attribute facts and environment attribute facts similarly. All of these facts are called attribute facts.

Attribute facts represent the authorization information related to subjects, resources, actions and environments. They maybe specified in the policy base beforehand, or gathered and specified by the access control system upon user accesses. To make it clearer, an example, E.A.1, is given in appendix.

Definition 3.3 A basic authorization rule is a rule of the form:

$$
\text { permit\_i } (s, r, a, e) \leftarrow L _ {1} \& \dots \& L _ {n}. \text {   or }
$$

$$
\text { deny\_i } (s, r, a, e) \leftarrow L _ {1} \& \dots \& L _ {n}.
$$

where s, r, a, e are subject term, resource term, action term and environment term respectively, and for each $0 < i \leq n$ , $L_{i}$ is either an attribute literal or a primitive constraint literal.

Basic authorization rules are specified by administrators explicitly, or, in our scenario, specified in the policy proposals proposed by the deployers and containers. Each of them represents a special kind of cases where the user access should be explicitly permitted or denied. An example, E.A.2, is given in appendix.

By means of different constraint domains and related complete theories, we can deal with subjects, resources, actions and environments with complex structures using the basic authorization rules. However, there may be conflicts among basic authorization rules. In order to express coherent policies with practical usage, we need the following composition rules.

Definition 3.4 A composition rule is of the form:

$$
\text { permit\_j } (s, r, a, e) \leftarrow L _ {1} \& \dots \& L _ {m}. \text {   or }
$$

$$
\text { deny\_j } (s, r, a, e) \leftarrow L _ {1} \& \dots \& L _ {m}. \text {   or }
$$

$$
\operatorname{permit} (s, r, a, e) \leftarrow L _ {1} \& \dots \& L _ {m}. \text {   or   }
$$

$$
\mathrm{deny} (s, r, a, e) \leftarrow L _ {1} \& \dots \& L _ {m}.
$$

where s, r, a, e are subject term, resource term, action term and environment term respectively, and for each $0<i\leq m$ , $L_{i}$ is either an attribute literal, a primitive constraint literal, a permit\_k (deny\_k) or a negative permit\_k (deny\_k) literal with lower ordinal number (k<j). permit (deny) should be regarded as permit\_k (deny\_k) with highest ordinal number.

Composition rules are used to derive authorizations from basic authorization rules and resolve possible conflicts among lower level rules. By means of composition rules, we can establish a tree of sets of authorization rules. The leaves of this tree are the sets consist of basic authorization rules and attribute facts. The root is a set of composition rules with permit and deny atoms as heads. Every non-leaf node of the tree is a set of composition rules with permit\_k and deny\_k atoms as heads. Thus, each sub-tree represents a consistent sub-policy of the whole authorization policy. This tree can be easily mapped to the hierarchy of policy set, policy, and rules defined in XACML. An example, E.A.3, is given in appendix.

By specifying an access control policy as a logic program in our language, you can depict the access control requirements of many real life applications. The evaluation of an access control policy can be implemented as the execution of corresponding logic program.

It's worthy of note that the authorization policy specified above should be transformed before analyzing or validating it as a constraint logic program. This is because of the constraint propagation and solving mechanism used by most constraint logic programming systems, which needs the constraint variables appear in the head of logic rules. The transformation procedure is quite straightforward. Firstly, you need to remove the subject, resource, action and environment variables from the head, and drop the attribute literals in the body of logic rules. Then you should insert appropriate constraint variables into the head literal and add appropriate constraint literals into the body. An example of transformation, E.A.4, is given in appendix.

It's easy to see that the transformation is not necessary if we only want to evaluate the policy against concrete attribute facts and get yes/no decision.

# 4. Negotiation Procedure & Meta-policies

In CROWN, service deployers and containers are often located in different security domains. As a result, before the access control policy negotiation for the remote hot-deployed a grid service will be considered, an appropriate trust relationship must be established, while the mechanism for trust establishment is out of this paper's discussion scope.

After trust establishment, as shown in Fig. 2, the negotiation procedure of access control policy takes place. WS-Security [22] is used to secure the communications between the two parties. We use dashed line for steps 7 and 8 in Fig. 2 because these two steps may be skipped.

![](images/4032bb124fb58315c72123c4b5513bc6ad9fba12aae6a30db8f64498069ab707.jpg)



Figure 2 Negotiation of Access Control Policy

During negotiation, the actions of both parties are controlled by meta-policies. CROWN.ST has three types of meta-policies as follows.

(1) Proposal making meta-policies are used to dynamically generate policy proposals. They are application-specific and mainly used on the container side. In order to accommodate diverse application requirements, we used rule-based language to specify this kind of meta-policies. Typically, they are specified in accordance with the service level agreements (SLAs) between the deployer and the container, or other collaboration agreements between them.   
(2) Combining algorithm selection meta-policies. We do not see any single combining algorithm suitable for resolving all possible conflicts in grid environments, so CROWN.ST employs meta-policies on the container side to dynamically select appropriate combining algorithms for synthesis of policy proposals. These meta-policies are also rule-based. The selection criteria in these rules are logical expressions defined for each candidate algorithms in terms of properties of the deployer, the service and the raw resources. Commonly used combining algorithms include deny-overrides, permit-overrides and explicit priority based algorithms.   
(3) Validity checking meta-policies are used to check the validity of temporary policies. They are rule-based too and specified in company with proposal

making meta-policies. Their evaluation results are logical queries consist of constraint literals and a permit or deny literal, and must be evaluated to true according to the temporary policy before the temporary policy is accepted. The queries with negative permit literal and negative deny literal correspond to the traditional safety and availability queries respectively. Besides authorization constraints such as separation of duties, the deployer could derive validity checking meta-policies from SLAs to take full advantage of the raw resources provided by the container.

To illustrate the negotiation procedure and meta-policies, we consider the following simple scenario. Alice has a grid service named servicel and want to provide it to her classmate Julius Hibbert. But Alice doesn't own enough resources to host the service herself. She finds a remote container which provides application hosting services and wants to deploy the service on it. The procedure she takes is the following:

Step 1. Alice generates its policy proposal, i.e. rule permit\_1 in E.A.2 which permits Julius Hibbert to access service1.   
Step 2. Alice submits the proposal to the negotiation service representing the container.   
Step 3. In this scenario, we suppose the container has established some SLA with Alice beforehand. The negotiation service authenticates Alice and generates its own policy proposal according to the SLA between them. The resulting proposal is the rule deny\_2 in E.A.2, which denies user access when CPU usage exceeds 50%. It's worthy to note that these two proposals concern different parts of the policy. While the deployer's proposal concerns who can access the grid service, the negotiation service's proposal concerns how much raw resources can be used by the grid service.   
Step 4. We suppose the negotiation service has two candidate combining algorithms in this scenario, permit-overrides and deny-overrides, which are provided for container owner and other remote users respectively. So, deny-overrides algorithm is selected for Alice. The resulting temporary policy is illustrated in E.A.3.   
Step 5. Because deny-overrides algorithm is selected, the validity checking on the container side could be omitted safely.   
Step 6. The negotiation service returns the temporary policy to the deployer.   
Step 7. The deployer checks the validity of the temporary policy and makes a decision, i.e., accept it and continue the deployment, or decline it and terminate the deployment. In this scenario, the validation queries are also generated according to the

SLA between Alice and the container in order to take full advantage of the raw resources provided by the container. The resulting query is

$$
C p u \_ u s a g e <   = 5 0,
$$

permit("service1", "Julius Hibbert", Cpu \_ usage). and is evaluated to true.

Step 8. The deployer submits its acceptance to the negotiation service and continues the real deployment.

# 5. CROWN.ST Prototype Implementation

To implement our access control policy language, we use an open source constraint logic programming system, YAP[23], as the underlying engine. Our current prototype only supports linear arithmetic constraints over rational number. Many authorization information used in grid environments (e.g., user identifier, time, storage space, cpu frequency) can be treated as rational numbers, so we could express real life policies over this constraint domain. For grid users' convenience, we implement a translation tool for translating access control policy specified with simplified XACML into constraint logic program written in our access control policy language.

Because current constraint logic programming systems lack support for general constructive negation (most implementations of constructive negation are specially designed for the Herbrand domain), we developed a tool for translating policies in our language to logically equivalent constraint logic program without negation, which will be evaluated using YAP. In this way, validation queries could get constructive answers even when validation fails. These answers may be used as hints for the negotiation partners to accelerate the next round of negotiation.

To implement meta-policies, we used a general, efficient and open source rule engine, Drools[24], which is based on Rete algorithm [25].

Besides above mentioned tools and libraries, we integrate the functionalities used in negotiation with other components of CROWN. On the deployer-side, we developed a GUI tool for negotiation, which prompts users for necessary decisions such as parameter choosing. The negotiation progress and temporary policy are visually shown to users. The user could use the translation and analysis function provided by the tool to translate and validate temp policies.

On the container-side, the functionalities used in negotiation are implemented as a standalone grid service, which is called negotiation service. We deploy this service in each CROWN node. Before deploying a service, the deployer is redirected to the negotiation service first. The negotiation service will generate a container side policy proposal and combine it with deployer's proposal, then validate the temporary policy and return validation result accordingly.

In order to reduce the cost spent on maintaining states for long-lived negotiations, the negotiation service signs and timestamps the temporary policy and then halts the negotiation procedure if the validation on the deployer-side is likely time consuming. The deployer can validate the temporary policy offline and then resume the remote deployment.

# 6. Complexity Analysis

Besides the cost of network transfer and message (de)serialization, the complexity of access control policy negotiation mainly comes from the evaluation and enforcement of meta-policies.

The three kinds of meta-policies are rule based, so their evaluations are tractable (particularly, the Drools engine can achieve linear complexity w.r.t. the meta-policy size after compilation). However, the validation queries derived from validation meta-policies must also be evaluated, which is intractable in general. Because that our policy language supports explicit negation, the independence of negated constraints property (INC)[26] does not hold on our constraint domains. Particularly, testing the satisfiability of a conjunction of constraints and negated constraints cannot be reduced to a series of tests involving a single negated constraint. As a result, the worst-case complexity of validation query evaluation is at least co-NP-hard w.r.t. the size of the temporary policy in general. Besides this, the cost of testing the satisfiability of each constraint may be not negligible. For example, the complexity of constraint solving over discrete finite domain is NP-hard in general. For our prototype, the complexity of solving linear arithmetic equations/inequations is polynomial w.r.t. the variable number and equaitons/inequations size, so its impact is relatively small.

Despite the high worst-case complexity mentioned above, the access control policy negotiations between grid service deployers and containers are not too complex according to our experience. Firstly, the basic authorization rules in these policies usually involve only few (for example, no more than 3) primitive constraints with few (no more than 3) variables, because the deployer and container owner usually concern with different authorization factors. For example, the deployers usually concern with the grid service user's identity and other properties. In contrast, the container owners usually concern with factors about the raw resources, such as CPU usage, storage size and network speed. Apparently, this will keep the explosion of sub-goals and the cost of constraint solving grow relatively slow when the rule number increase, as will also shown in Section 7.

Secondly, many safety properties can be achieved through careful proposal making and combination instead of temporary policy validation. For example, the container owner's meta-policies can choose deny-overrides combining algorithm or specify high priorities for deny rules in its proposal in order to assure the final policy will not abuse the raw resources.

Thirdly, the validity checking meta-policies used in real scenarios usually generate validation queries with quite a number of constraint literals, which could be used to reduce the search space of evaluation effectively.

# 7. Performance Evaluation

We successfully deploy CROWN.ST prototype in CROWN Grid environment. To evaluate its performance, we conduct a series of experiments. The negotiation service (with underlying container) is deployed on cluster nodes with Intel Xeon 2.8GHz CPU, 2G RAM, RedHat Linux EL3.0 and 100M bps Internet connection. On the deployer-side, we use a notebook with 1.6GHz CPU, 512M RAM, Debian Linux with kernel 2.6.8 and 100M bps Internet connection. To make sure the measurements are accurate, no other tasks are running on cluster nodes and the notebook, except the necessary CROWN middleware. If not explicitly specified otherwise, each experiment takes 10 run and we plot the average.

Concurrent thread numbers and the sizes of temporary policies are taken as parameters. The size of a temporary policy is further characterized using 4 parameters. (1) The number of primitive constraints in each basic authorization rule, denoted by PC in the following figures; (2) The size of a primitive constraint, i.e. the number of variables appearing in the primitive constraint, which is denoted by PCS; (3) The number of variables appear in the temporary policy, denoted by VAR; (4) The number of basic authorization rules appear in the temporary policy, denoted by R. We take the time used by the whole negotiation procedure as the evaluation metric, which excludes the time used for user interactions and digital encryption/decryption.

In our first experiment, we randomly generate four groups of test cases. Each group consists of 30 test cases generated with the same policy size parameters. We further separate the four groups into two subgroups according to PC and PCS (VAR is fixed in this experiment because its impact is relatively small). Figures 3 and 4 show the negotiation time used by these test cases. Each point represents the negotiation time used by one test case.

From these two figures, we can see that the negotiation time used by test cases with the same size parameters may differ significantly. This is because that the application-specific policy and query structures have an important impact on the negotiation time. As mentioned in Section 6, the worst-case complexity is at least co-NP hard, but not all cases are the worst cases. Contrarily, most cases are simple according to our experiences.

![](images/b17d63f90bf2289d63ce82d88ed7bcb7a96bdf0c7f16bfc926495a2ac3595012.jpg)  
Figure 3 Negotiation time for 60 randomly generated test cases with

$$
P C = 3, P C S = 3, V A R = 8
$$

![](images/a4359933382c6799473a8227931539f604225cca66f478b24b083b57f49db3cc.jpg)



![](images/285b0decf18db3aa205b5d4072fb6cbef7b82eedfe59cc2ac88f17ffba1713c6.jpg)



Figure 4 Negotiation time for 60 randomly generated test cases with

$$
P C = 5, P C S = 5, V A R = 8
$$

The peak value of 30 randomly generated test cases can be regarded as representing the worst-case. From these two figures we can see that the worst-case cost increases relatively slow against R when PC and PCS are relatively small, which are the cases for the most grid applications. As a result, we think the approach present in this paper can be used in real grid scenarios.

Figure 5 plots the average negotiation time against the number of concurrent requests. The policy size parameters of the test case is PC=5, PCS=3, VAR=8, R=8. As we can see in this figure, the average negotiation time increases linearly with the increasing number of concurrent requests.

![](images/7447e6dbaa06f4832966ee0c74b282c3b3eb43c4623a2658b89912ab8e8abc7e.jpg)



Figure 5 Negotiation time vs. the number of concurrent requests

# 8. Conclusions and Future Works

We propose a general approach for access control policy negotiation during remote hot-deployment of grid services, which is an important requirement for service grids like CROWN. We define an access control policy language based on non-recursive stratified Datalog with constraints for grid services. The language can be used to specify and analyze practical access control policies for real life applications. Based on this language, we design a negotiation procedure, which dynamically and automatically determine the final access control policy for the grid service being deployed.

We successfully implement a CROWN.ST prototype, which has been deployed in our CROWN Grid. We further evaluate CROWN.ST by comprehensive experiments. Due to the page limit, we only show some representative results in this paper.

CROWN is an actively ongoing project. Therefore, our solutions for secure, remote and hot deployment of grid services will be further extended and improved in future versions of CROWN. Future work will lead into several directions. First, we will improve the performance of the analyzing algorithm and extend CROWN.ST to support more constraint domains. Second, related topics such as the integration of trust negotiation, policy synthesis and service composition are going to be explored and implemented in CROWN. We believe these are the key technologies for better collaboration in service grids.

# References

[1] I. Foster and C. Kesselman, "Globus: A metacomputing infrastructure toolkit," Intl. Journal of Supercomputing Applications, vol. 11, pp. 115-129, 1997.   
[2] I. Foster, C. Kesselman, and S. Tuecke, "The Anatomy of the Grid: Enabling Scalable Virtual Organization," The International Journal of High Performance Computing Applications, 2001.   
[3] J. Huai, Y. Liu, X. Li, and C. Hu, "Early Experiences with CROWN Grid," Technical Report, School of Computer Science, Beihang University, 2005.   
[4] C. Hu, Y. Zhu, J. Huai, Y. Liu, and L. M. Ni, "Efficient Information Service Management Using Service Club in CROWN Grid," presented at IEEE International Conference on Services Computing, 2005.   
[5] F. Baude, D. Caromel, F. Huet, L. Mestre, and J. Vayssiere, "Interactive and Descriptor-based Deployment of Object-Oriented Grid Applications," presented at the 11th IEEE International Symposium on High Performance Distributed Computing, 2002.   
[6] W. Goscinski and D. Abramson, "Distributed Ant: A System to Support Application Deployment in the Grid," presented at the Fifth IEEE/ACM International Workshop on Grid Computing, 2004.   
[7] S. Godik and T. Moses, "eXtensible Access Control Markup Language Version 2.0, working draft 12," OASIS, June 25, 2004.   
[8] M. Lorch, D. Adams, D. Kafura, M. Koneni, A. Rathi, and S. Shah, "The PRIMA System for Privilege Management, Authorization and Enforcement in Grid Environments," presented at The 4th International Workshop on Grid Computing (Grid 2003), Phoenix, AR, USA, 2003.   
[9] L. Pearlman, V. Welch, I. Foster, C. Kesselman, and S. Tuecke, "A Community Authorization Service for Group Collaboration," presented at IEEE 3rd International Workshop on Policies for Distributed Systems and Networks, 2002.   
[10] M. R. Thompson and S. Mudumbai, "Certificate-based Authorization Policy in a PKI Environment," ACM Transactions on Information and System Security (TISSEC), vol. 6, pp. 566-588, 2003.   
[11] P. McDaniel and A. Prakash, "Methods and limitations of security policy reconciliation," presented at IEEE Symposium on Security and Privacy, 2002.   
[12] H. Khurana and V. D. Gligor, "A Model for Access Negotiations in Dynamic Coalitions," presented at the 13th IEEE International Workshops on Enabling Technologies: Infrastructure for Collaborative Enterprises (ICE'04), 2004.   
[13] V. G. Bharadwaj and J. S. Baras, "Towards Automated Negotiation of Access Control Policies," presented at IEEE

4th International Workshop on Policy for Distributed Systems and Networks, Lake Como, Italy, 2003.

[14] N. Li, J. C. Mitchell, and W. H. Winsborough, "Design of a role-based trust management framework," presented at the 2002 IEEE Symposium on Security and Privacy, 2002.

[15] N. Li and J. C. Mitchell, "Datalog with constraints: A foundation for trust management languages," presented at the 15th International Symposium on Practical Aspects of Declarative Languages, 2003.

[16] T. Jim, "SD3: A trust management system with certified evaluation," presented at 2001 IEEE Symposium on Security and Privacy, Oakland, California, USA, 2001.

[17] J. DeTreville, "Binder, a logic-based security language," presented at 2002 IEEE Symposium on Security and Privacy, Oakland, California, USA, 2002.

[18] N. Li, B. N. Grosof, and J. Feigenbaum, "Delegation Logic: A Logic-based Approach to Distributed Authorization," ACM Transactions on Information and System Security (TISSEC), vol. 6, pp. 128-171, 2003.

[19] P. J. Stuckey, "Negation and Constraint Logic Programming," Information and Computation, vol. 118, pp. 12-33, 1995.

[20] E. Dantsin, T. Eiter, G. Gottlob, and A. Voronkov, "Complexity and Expressive Power of Logic Programming," ACM Computing Surveys, vol. 33, pp. 374-425, 2001.

[21] J. Jaffar and M. J. Maher, "Constraint Logic Programming: A Survey," Journal of Logic Programming, vol. 19/20, pp. 503-581, 1994.

[22] B. Atkinson and G. Della-Libera, "Web Services Security Version 1.0," 2002.

[23] "The YAP Prolog System," http://www.ncc.up.pt/\~vsc/Yap/.

[24] N. A. Rupp, "The Logic of the Bottom Line: An Introduction to The Drools Project," http://www.theserverside.com/articles/article.tss?1=Drools, 2004.

[25] C. L. Forgy, "Rete: A fast algorithm for the many pattern/many object pattern match problem," Artificial Intelligence, vol. 19, pp. 17-37, 1982.

[26] M. J. Maher, "Adding Constraints to Logic-based Formalisms," in The Logic Programming Paradigm: a 25 Years Perspective, Artificial Intelligence Series, V. M. K.R.Apt, M. Truszczynski and D.S. Warren, Ed.: Springer-Verlag, 1999, pp. 313-331.

# Appendix

E.A.1 Consider the following attribute facts:

sub_att(sub_1,"subject-id", "Julius Hibbert") ← .  
env_att(env_1,"current-date", "2004-12-25") ← .

The first fact states that the subject identifier of sub\_1 is Julius Hibbert. This information may be gathered by the access control system after verifying the signature of the user on the requesting message. The second fact states that the current date is 2004-12- 25. This information may be gathered by the system from local time server.

E.A.2 Consider the following basic authorization rules:

permit_1(Sub, Res, Act, Env) ←
    res_att(Res, "resource-id", "service1"),
    sub_att(Sub, "subject-id", "Julius Hibbert").
deny_2(Sub, Res, Act, Env) ←
env_att(Env, "cpu-usage", X), X > 50.

The first rule states that the user Julius Hibbert can access service1 at any circumstance. The second rule states that nobody can access any service if the cpu-usage exceeds 50%.

E.A.3 There is a conflict between the two rules in example E.A.2, we can use the following composition rules to resolve it.

permit(Sub, Res, Act, Env) ←
    permit_1(Sub, Res, Act, Env),
    not deny_2(Sub, Res, Act, Env).
deny(Sub, Res, Act, Env) ←
    deny_2(Sub, Res, Act, Env).

These composition rules implement so called “denials take precedence” which is corresponding to the deny-overrides combining algorithm defined in XACML.

Many useful conflict resolution approaches based on explicit or implicit precedence can be implemented with our composition rules. Besides this, to assure the specification completeness of access control policy, we can further include some default authorization rules. For example, we can include the following default composition rule

deny(Sub, Res, Act, Env) ←
    not permit_1(Sub, Res, Act, Env).

to assure that “undefined” cases are regarded as “deny”.

E.A.4 The rules in example E.A.2 and E.A.3 can be transformed to the following rules before validating.

permit_1(Resource_id, Subject_id) ← Resource_id = "service1", Subject_id = "Julius Hibbert".
deny_2(Cpu_usage) ← Cpu_usage > 50.
permit(Resource_id, Subject_id, Cpu_usage) ← permit_1(Resource_id, Subject_id), not deny_2(Cpu_usage).
deny(Cpu_usage) ← deny_2(Cpu_usage).
deny(Resource_id, Subject_id) ← not permit_1(Resource_id, Subject_id).
resource_id, Subject_id, and Cpu_usage are constraint variables.