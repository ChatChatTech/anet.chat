# Hidden Markov based Truth Discovery for Multi-Agent Labeling

Shan-Yang Jiang

School of Data Science

University of Science and Technology of China

Hefei, China

yang12@mail.ustc.edu.cn

Lan Zhang

School of Computer Science and Technology

University of Science and Technology of China

Hefei, China

zhanglan@ustc.edu.cn

Abstract—In recent years, large-scale data labeling has become a huge demand and extremely challenging task. More and more machine learning and deep learning methods have been proposed to generate a variety of semantic labels for data, and used to provide data labeling service as a data labeling agent. However, even todays machine learning and deep learning model may also output a wrong label. So it is necessary to optimize the quality of the collected labeling results. Generally, there are many labeling models in the data labeling market, and each label agent has a different degree of reliability. Service buyers also need to integrate many label answers from different labels agents to get the final correct label truth.

In this article, we design a novel probabilistic graph based truth discovery algorithm to estimate the true label truth of the target task and the reliability of the label agent through the collected label answers. In particular, we build a novel expectation-maximization based iterative method for truth discovery to inference label truth and estimate label agent reliability. Finally, we conduct several experiments on a real-world dataset to testify the performance of our method.

Index Terms—label annotation, truth discovery, reliability estimation

# I. INTRODUCTION

Today's intelligent systems urgently need a large number of labeled data sets to build their own intelligent models. And the un-labeled datasets used to be completed by crowdsourcing human annotation, which cannot meet the requirement of fast evolution of current AI systems due to its diverse quality and time consuming characteristics. There are a lot of machine learning model and deep learning model based API agent service, such as MLaaS, BaiduAI [1], can provide richer and faster labeling capabilities. Consider building a smart image retrieval AI system, a requester may need annotate each image with a comprehensive collection of semantic labels. The requester can purchase a series of API agent service as a buyer on these agent platform, and use its to produce as many labels as possible to describe each image to improve the quality of search results.

Now, in order to extract rich labels, there are kinds of machine learning and deep learning model [2]–[4] which have been proposed to generate more and more semantic labels. At the same time, methods such as multi-label learning [5], [6] and multi-task learning [7], [8] are proposed, aiming to use a single model to obtain richer labeled labels. Some other work is devoted to the method design of accelerating model operation, such as model compression via parameter pruning & sharing [9], network architecture optimization [10] and adaptive model configuration [11]. The labeling platform releases these various labeling models to provide buyers with convenient and fast data labeling services in the form of label agent.

Although there are various annotation label agent available, buyers still have some difficulties in successfully completing data annotation. (1) The limited ability of a single label agent: One single label agent can usually only output part of labels based on certain aspects of the data. Thus, in many cases, e.g., image retrieval, and text sentiment analysis, it usually need a series labels to achieve a broad understanding of data. And, for these tasks, the more diverse labels collected, the better the services provided. (2) The diverse and unknown reliability of every label agent: Despite the efforts made by existing work to provide us with increasingly powerful label agent for various tasks, the output of the label agent is still not necessarily correct. Each label agent outputs its own classification result and its confidence. There may even be different label agent that output completely different results for the same task. (3) Large number of labeling tasks: Buyers usually have a large number of labeling tasks to complete. This means that the number of labeling results of labeling tasks obtained by buyers is even greater. This will bring huge data processing challenges to buyers after the completion of the collection of label results.

Usually, buyers labeling tasks have multiple labels that need to be labeled, such as multi label classification. Consider a text classification task, and the text may belong to politics, economy, culture, art, sports, etc. There may be a correlation between the classification categories, for example, political-related texts may also mention economic content. In the field of image classification, when a picture has a beach label, it means that the picture also has an outdoor scenery label. And the label agent outputs the labeling answer of each task's every label and its confidence level. A common method is to construct a set of labeled answers for each label by labeling agents, and then Majority Voting (MV), which selects the answer provided with the maximum confidence level as the truths. The immediate limitation here is this method does not take every label agents reliability into account, as every labeling agent has different labeling reliability. At the same time, this method ignores the nature of the latent correlation between labels.

Therefore, in this article, we propose a novel probabilistic graph model that considers the reliability of the labeling agent and the correlation between label truth to infer the true label value of the target task. First, we state that the accuracy is used to express the reliability of a labeled agent, and we assume that the probability that the output result of the labeled agent is correct obeys the Bernoulli distribution with its accuracy as a parameter. Next, we use Hidden Markov chains $[12]$ to build the correlation between label truth. The transition matrix in the Hidden Markov chain can just describe the probability of two labels co-occurring. Finally, according to the set of label answers that have been collected, the established probabilistic graph model is used to estimate the model parameters and infer the true value of the label.

To summarize, we make the following contributions:

- We identify a new data labeling scenario: the multi-agent labeling scenario, in smart API label market.   
- We establish a novel probabilistic model to describe the latent label correlation and the label answer generation process, propose truth discovery algorithm to jointly estimate the label truth and agent reliability.   
- We conduct several experiments on a real-world dataset to testify the performance of our method, and show that our method can achieve better result.

The rest of the paper is organized as follows. In Section II, we formulate the problem and present the overview of our design. We propose two methods: Truth Discovery without Label Correlation and Truth Discovery with Label Correlation in Section III. The experimental results are reported in Section IV. We review related work in Section V and conclude our work in Section VI.

# II. PROBLEM STATEMENT

In this section, we first describe our problem scenario, and then formally give the definition and symbolic representation of the problem.

# A. System Overview

A typical agent market contains two major parties: a service buyer, a set of agent which can provide label service. The buyer has a un-labeled task set, and agents can provide label service with a fix post price. We assume that, at the agent market scene, the buyer is in a push marketplace for annotation, that is buyer can ask for a label from a particular agent and are guaranteed to get the label answer. So buyer can select any agent to obtain its label answer for a task. Due to the task difference and diverse agent reliability, the collected label answer from these agents are normally noisy and imprecise. Considering the quality of label answer, the buyer faces two fundamental problems in agent market: how to calculate each task truth and how to evaluate each agent reliability?

# B. Agent Label Annotation

We denote the un-labeled dataset posted on the agent annotation market to obtain repeated noisy label answers by $T = \{ < x^{t}, y^{t} > \}_{t=1}^{T}$ , where each task $x^{t}$ associates with an unknown label truth set $y^{t}$ . Each $y^{t}$ consist of K labels, which is denoted by $y^{t} = [y_{1}^{t}, y_{2}^{t}, ..., y_{K}^{t}], y_{k}^{t} \in \{0, 1\}$ . Label truth value of the entire un-label dataset are denoted by $Y = \{y^{1}, y^{2}, ..., y^{T}\}$ . Thus, we can say " $y_{k}^{t}$ is the kth label of the task $x^{t}$ ".

There are totally W agents labeling the task set. All collected noisy label answers for each task $x^{t}$ form a matrix $\mathbf{A}^{t} = (a_{wk}^{t})_{W*K}$ , where $a_{wk}^{t}$ is the label answer by agent w for the kth label of task $x^{t}$ . If agent w does not provide any label answer for the kth label, we let $a_{wk}^{t} = \bot$ . We use $A_{*k}^{t}$ to denote the label answer set for the kth label, and $A_{w*}^{t}$ to denote the label answer set of agent w. All collected label answers of the entire task set are denoted by $A = \{A^{1}, A^{2}, ..., A^{T}\}$ .

This paper aims to solve the following two key issues in multi-label truth discovery problem in agent market:

Jointly estimate the label truth and the agent reliability. The primary function of a truth discovery algorithm is to estimate the label truth distribution Y for all tasks T from the obtained noisy label answer set A, and an excellent truth discovery algorithm should have high accuracy:

$$
A c c u r a c y = \frac {1}{T \cdot K} \sum_ {t = 1} ^ {T} \sum_ {k = 1} ^ {K} \mathbb {I} (\hat {y} _ {k} ^ {t} = y _ {k} ^ {t}) \tag {1}
$$

Here $\mathbb{I}$ is an indicator function, $\hat{\mathbf{y}}^t,\mathbf{y}^t\in \{0,1\}$ respectively are the estimated and the real label truth value. It outputs 1 when the estimated label truth equal to the real. Otherwise, it outputs 0. Meanwhile, estimation of each agent reliability is also an important function of the truth discovery algorithm. There are a lot of truth discovery for single-label. Can we jointly estimate the label truth distribution and the agent reliability considering for multi-label task?

Exploring and exploiting the latent label correlation. A simple and direct solution is to ignore the latent label correlation and treat the multi-label problem as multiple single-label problems. That is to say, directly on K different labels, run the truth discovery algorithm K times. However, for multi-label task, there perhaps exists latent correlation among the label truth. Generally speaking, people actually know the correlation between label truth, and they can use this correlation to infer the answer from a label with a known answer. However, the simple approach ignored this important factor. So is there an effective way to express the latent correlation between label truth and estimate label truth distribution considering latent label correlation?

# III. THE PROPOSED METHOD

In this section, we first present a general probabilistic graph model considers the task difficulty and the agent reliability to describe the label generation process without considering the latent label correlation. Then we give the expression of the latent label correlation, and we learn the model parameter with an EM algorithm combined with the probability graph model. Finally, we present our truth discovery algorithm.

TABLE I: Notations 

<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $\mathcal{T},\mathbf{T}$ </td><td>Target task dataset, the number of tasks</td></tr><tr><td> $\mathcal{W},\mathbf{W}$ </td><td>Label agent sets, the number of label agent</td></tr><tr><td> $x^{t},\mathbf{y}^{t}$ </td><td>Target task, target label sets</td></tr><tr><td> $K$ </td><td>Number of target labels</td></tr><tr><td> $\mathbf{A}^{t}$ </td><td>Label answer set for task  $x^{t}$ </td></tr><tr><td> $a_{wk}^{t}$ </td><td>Label answer for kth label of task  $x^{t}$  from agent w</td></tr><tr><td> $\theta^{t}$ </td><td>Task difficulty parameter for  $x^{t}$ </td></tr><tr><td> $\rho_{wk}$ </td><td>Agent reliability parameter for label agent w on kth label</td></tr><tr><td> $\mathcal{A}^{t},\mathcal{B}^{t},\pi^{t}$ </td><td>Hidden Markov Model parameters</td></tr></table>

# A. Label Generation Model

This subsection firstly model the generation process [13], [14] of the real label truth and the agent label answer of just one single-label based on the probabilistic graph model.

Generation of real label truth. We characterize the labeling difficulty of each task by $\theta^{t} = [\theta_{1}^{t}, \theta_{2}^{t}, ..., \theta_{K}^{t}]$ , $\theta_{k}^{t} \in [0, 1]$ . And we denote the all difficulty parameter vectors of totally T un-labeled tasks by a parameter set $\theta = \{\theta^{1}, \theta^{2}, ..., \theta^{T}\}$ . To be more precise, $\theta_{k}^{t}$ can be interpreted as the percentage of the agent labels the kth label as presence if a large number of noiseless (perfectly reliable) agents are asked for the labeling task. We can think that the result of a perfectly reliable agent is always correct, then we have: $\theta_{k}^{t} = P(y_{k}^{t} = 1)$ . So each true label is independently drawn from a Bernoulli distribution with parameter $\theta_{k}^{t}$ . That is, for the kth label of a task $x^{t}$ , we have:

$$
P (y _ {t} ^ {t} | \theta_ {k} ^ {t}) = (\theta_ {k} ^ {t}) ^ {\mathbb {I} (y _ {k} ^ {t} = 1)} (1 - \theta_ {k} ^ {t}) ^ {\mathbb {I} (y _ {k} ^ {t} = 0)} \tag {2}
$$

Generation of agent label answer. For ordinary binary classification tasks, the one-coin model is sufficient to express the reliability of each labeling agent. We use a parameter set of vector $\rho_{w} = [\rho_{w1}, \rho_{w2}, ..., \rho_{wK}]$ to denote the reliability of agent w with respect to K labels. And we denote the all reliability parameter vectors of totally W agents by a parameter set $\rho = \{\rho_{1}, \rho_{2}, ..., \rho_{W}\}$ . Each element $\rho_{wk}$ represent the probability of agent w correctly labeling the kth label, which derives $P(a_{wk}^{t} = 1|y_{k}^{t} = 1) = P(a_{wk}^{t} = 0|y_{k}^{t} = 0) = \rho_{wk}$ . That is, $a_{wk}^{t}$ conditioning on $y_{k}^{t}$ obeys a Bernoulli distribution with parameter $\rho_{wk}$ . Consider each task $x^{t}$ is independently annotated by W agents, the likelihood of $a_{wk}^{t}$ can be calculated as follow:

$$
\begin{array}{l} P \left(a _ {w k} ^ {t} = 1 \mid \theta_ {k} ^ {t}, \rho_ {w k}\right) = \theta_ {k} ^ {t} \cdot \rho_ {w k} + \left(1 - \theta_ {k} ^ {t}\right) \cdot \left(1 - \rho_ {w k}\right) \\ P \left(a _ {w k} ^ {t} = 0 \mid a _ {w k} ^ {t}\right) = a _ {w k} ^ {t} \cdot \left(1 - \rho_ {w k}\right) \end{array} \tag {3}
$$

$$
P (a _ {w k} ^ {t} = 0 | \theta_ {k} ^ {t}, \rho_ {w k}) = \theta_ {k} ^ {t} \cdot (1 - \rho_ {w k}) + (1 - \theta_ {k} ^ {t}) \cdot \rho_ {w k}
$$

# B. Truth Discovery without Label Correlation

In this subsection, we first present Label Independent Model for truth discovery without considering label correlation. The process of Label Independent Model contains two parameter sets: agent reliability parameter set $\rho$ and task difficulty

![](images/60080b49ad8cc384b45f1bd4907506fdc094a7aad33ce7e1eb67f90e42d8680d.jpg)



Fig. 1: Single-Label Probability Graph

parameter $\theta$ , we let $\Psi = (\rho, \theta)$ . The difficulty of each label is different for each task. So, we use the iterative EM algorithm to estimate the actual true label truth of each task in the absence of a true value.

Consider each task is individually labeled by every labeling agents, the likelihood of all collected noisy label answer set $A^{t}$ on the task $x^{t}$ can be calculated as follow:

$$
\begin{array}{l} l _ {x ^ {t}} (\boldsymbol {\rho}, \boldsymbol {\theta}) = P (\mathbf {A} ^ {t} | \mathbf {y} ^ {t}, \boldsymbol {\rho}, \boldsymbol {\theta}) \\ = \sum_ {\mathbf {y} ^ {t}} P (\mathbf {y} ^ {t} | \boldsymbol {\theta}) \cdot P (\mathbf {A} ^ {t} | \mathbf {y} ^ {t}, \boldsymbol {\rho}) \\ = \sum_ {\mathbf {y} ^ {t}} \prod_ {k = 1} ^ {K} P (y _ {k} ^ {t} | \theta_ {k} ^ {t}) \cdot \prod_ {w \in W ^ {t}} P (a _ {w k} ^ {t} | y _ {k} ^ {t}, \rho_ {w k}) \\ \end{array}
$$

Finally, the log-likelihood of all collected noisy label answer set A of the entire un-labeled dataset D is:

$$
L _ {\mathcal {D}} (\boldsymbol {\rho}, \boldsymbol {\theta}) = \sum_ {x ^ {t} \in \mathcal {D}} \ln l _ {x ^ {t}} (\boldsymbol {\rho}, \boldsymbol {\theta})
$$

Our optimization objective is to maximize the likelihoods of the collected label answer from agents $L_{\mathcal{D}}(\boldsymbol{\rho},\boldsymbol{\theta})$ , that is to update the parameters through the iterative EM algorithm.

E-step. With respect to the conditional distribution of Y given the observed noisy label answer A under the current estimates of parameters $\Psi^{old}$ , we calculate the expected value of the complete log-likelihood function, as follow:

$$
\begin{array}{l} \mathbf {Q} (\boldsymbol {\Psi}, \boldsymbol {\Psi} ^ {o l d}) = \mathbb {E} _ {\mathbf {Y} | \mathbf {A}, \boldsymbol {\Psi} ^ {o l d}} [ \ln P (\mathbf {A}, \mathbf {Y} | \boldsymbol {\Psi}) ] \\ = \sum_ {\boldsymbol {x} ^ {t} \in \mathcal {T}} \mathbb {E} _ {\mathbf {Y}} \left[ \ln P (\mathbf {A} ^ {t}, \mathbf {y} ^ {t} | \boldsymbol {\rho}, \boldsymbol {\theta}) \right] \\ = \sum_ {x ^ {t} \in \mathcal {T}} \mathbb {E} _ {\mathbf {Y}} \left[ \ln \left(P (\mathbf {A} ^ {t} | \mathbf {y} ^ {t}, \boldsymbol {\rho}) \cdot P (\mathbf {y} ^ {t} | \boldsymbol {\theta})\right) \right] \\ \end{array}
$$

Here, $P(\mathbf{y}^t|\boldsymbol{\theta})$ is a constant given a current estimation $\Psi$ . Thus, we only need to maximize:

$$
\mathbf {Q} (\boldsymbol {\Psi}, \boldsymbol {\Psi} ^ {o l d}) \propto \sum_ {x ^ {t} \in \mathcal {T}} \mathbb {E} _ {\mathbf {Y}} \left[ \ln P (\mathbf {A} ^ {t} | \mathbf {y} ^ {t}, \boldsymbol {\rho}) \right] \tag {4}
$$

Next, the posterior probability of the label truth value $y^{t}$ of each task $x^{t}$ can be calculated by Bayes' theorem as follows:

$$
\begin{array}{l} P (\mathbf {y} ^ {t} | \mathbf {A} ^ {t}, \boldsymbol {\Psi}) = \prod_ {k = 1} ^ {K} P (y _ {k} ^ {t} | \mathbf {A} ^ {t}, \boldsymbol {\Psi}) \\ \propto \prod_ {k = 1} ^ {K} p (y _ {k} ^ {t} | \theta_ {k} ^ {t}) \prod_ {w \in W ^ {t}} P (a _ {w k} ^ {t} | y _ {k} ^ {t}, \rho_ {w k}) \tag {5} \\ \end{array}
$$

Based on Equation 5, we can get the expected value of the posterior probability of each single label that will be used in M-step as follows:

$$
\mathbb {E} \left[ \mathbb {I} (y _ {k} ^ {t} = 1) \right] = \sum_ {k ^ {\prime} \in \{1, \dots , K \} \setminus k} P (y _ {k} ^ {t} = 1,... y _ {k ^ {\prime}} ^ {t}... | \mathbf {A}, \boldsymbol {\Psi}) \tag {6}
$$

M-step. We update the new parameter set $\Psi$ by maximizing the objective function Q formed as Eq.4 by $\Psi^{new} = \arg\max_{\Psi} \mathbf{Q}(\mathbf{\Psi}, \mathbf{\Psi}^{\mathrm{old}})$ . The parameters are updated as follow:

$$
\theta_ {k} ^ {t} = \mathbb {E} \left[ \mathbb {I} (y _ {k} ^ {t} = 1) \right] \tag {7}
$$

$$
\rho_ {w k} = \frac {\sum_ {x ^ {t} \in \mathcal {T}} \mathbb {I} (a _ {w k} ^ {t} = y) \mathbb {E} \left[ \mathbb {I} (y _ {k} ^ {t} = y) \right]}{\sum_ {x ^ {t} \in \mathcal {T}} \mathbb {I} (a _ {w k} ^ {t} \neq \bot)} \tag {8}
$$

After the EM algorithm converges, the final estimated true label truth of the task $x^{t}$ should be the multi-label label value with the largest posterior probability. That is:

$$
y _ {1} ^ {t}, \dots , y _ {K} ^ {t} = \arg \max P \left(y _ {1} ^ {t}, \dots , y _ {K} ^ {t} \mid \mathbf {A} ^ {t}, \boldsymbol {\theta}, \boldsymbol {\rho}\right) \tag {9}
$$

Algorithm 1: Truth Discovery without Label Correlation   
Input: Task set T, Agent set W, Label Answer set A
Output: Integrated Labels $y^{t}$ for each task $x^{t}$ 1 Initialize task difficult parameter $\theta_{k}^{t}$ for $x^{t} \in T$ , and agent reliability parameter $\rho_{wk}$ for $w \in W$ ;

2 while not converge do

3    // E step

4    for each task $x^{t} \in T$ do

5    Calculation expectation by Equation 6;

6    end

7    // M step

8    Update task difficulty parameter by Equation 7;

9    Update agent reliability parameter by Equation 8;

10 end

11 // convergence

12 for each task $x^{t} \in T$ do

13    Calculate the label truth by Equation 9;

14 end

15 return all task label truth $y^{t}$ .

![](images/b4ff85a5877e66e3ff308b1259ef4471332feb697e252fb2aad66d2a9c4206dc.jpg)



Fig. 2: HMM Probability Graph

# C. Truth Discovery with Label Correlation

This subsection presents Label Dependent Model, which models latent label correlation among single-label with the hidden Markov Model [12]. Finally, we give our truth discovery algorithm to estimate the model parameter, and infer the final label truth value.

Latent Label Correlation. Now, we give the definition of the latent correlation between two different labels: $f(y_k^{t'} | y_k^t)$ , inspired by [12], to quantify the latent correlation between $y_{k'}^t$ and $y_k^t$ as follows:

$$
f (y _ {k} ^ {t ^ {\prime}} | y _ {k} ^ {t}) = \frac {w e i g h t (y _ {k ^ {\prime}} ^ {t} , y _ {k} ^ {t})}{w e i g h t (y _ {*} ^ {t} , y _ {k} ^ {t})} \tag {10}
$$

where $k^{\prime} \neq k$ , and the $weight(y_{k^{\prime}}^{t}, y_{k}^{t})$ , denoting the degree of latent correlation between the label truth $y_{k}^{t}$ of the kth label and $y_{k^{\prime}}^{t}$ of another $k^{\prime}$ th label, which can be obtained by general knowledge background. For example, we can use the frequency of the two truth answer co-occurring in the collected answer set: $N(y_{k^{\prime}}^{t}, y_{k}^{t})$ to quantify the latent label correlation between two different truth of each pair of different labels.

Label Dependent Model. Given the output label answer $A^{t}$ from agents, we can calculate the latent correlation matrix $F^{t} = \{f(y_{k'}^{t} | y_{k}^{t})\}$ . The estimated truth value of each label is based on three factors: agent reliability, task difficulty, and latent label correlation among label truth value. We use hidden Markov model $\boldsymbol{\lambda}^{t} = (\mathcal{A}^{t}, \mathcal{B}^{t}, \pi^{t})$ to capture the latent correlation among label truth value for $x^{t}$ , and take every single-label truth $y_{k}^{t}$ as the hidden state of HMM; $\pi^{t}$ is the prior probability of which value being the truth of the first label for task $x^{t}$ ; $A^{t} = F^{t}$ is the state transition matrix in the hidden Markov Model; $\mathcal{B}^{t} = \{b_{y_{k}^{t}}(\mathbf{A}_{*k}^{t})\}$ is the collected label answers' generation probability matrix, and $b_{y_{k}^{t}}(\mathbf{A}_{*k}^{t})$ describing the relation between the collected label answer set $A_{*k}^{t}$ for kth label of task $x^{t}$ and the latent label truth value $y_{k}^{t}$ is defined as follows:

$$
\begin{array}{l} b _ {y _ {k} ^ {t}} (A _ {* k} ^ {t}) = P (\mathcal {A} _ {* k} ^ {t} | y _ {k} ^ {t}, \boldsymbol {\rho}, \boldsymbol {\theta}) \\ = \prod_ {w \in W _ {k} ^ {t}} P (a _ {w k} ^ {t} | y _ {k} ^ {t}, \rho_ {w k}, \theta_ {k} ^ {t}) \tag {11} \\ \end{array}
$$

For a task $x^{t}$ without the ground truth, the state transition matrix $A^{t}$ and the collected label answer's generation probability $B^{t}$ can be computed with two parameter set: $\rho$ and $\theta$ , and then the truth discovery problem can be transformed into the problem of searching the most possible multi-label label value of hidden states in the hidden Markov model $\lambda^{t}$ . In other words, after we have the hidden Markov Model $A^{t}$ and $\lambda^{t}$ , we just need to find the best state sequence that maximizing the posterior probability $P(\mathbf{y}^{t}|\boldsymbol{\lambda}^{t},\mathbf{A}^{t})$ as the estimated label truth value. This is a basic learning and predict problem in the HMM model. Thus we have :

$$
\begin{array}{l} \mathbf {y} ^ {t} = \arg \max _ {\mathbf {y} ^ {t}} P (\mathbf {y} ^ {t} | \boldsymbol {\lambda} ^ {t}, \mathbf {A} ^ {t}) \\ = \arg \max _ {\mathbf {y} ^ {t}} \pi^ {t} \prod_ {y _ {k} ^ {t} \in \mathbf {y} ^ {t}} b _ {y _ {k} ^ {t}} (A _ {* k} ^ {t}) f (y _ {k + 1} ^ {t} | y _ {k} ^ {t}). \\ \end{array}
$$

$$
P (\mathbf {y} ^ {t} | \boldsymbol {\lambda} ^ {t}, \mathbf {A} ^ {t}) = \pi^ {t} \prod_ {y _ {k} ^ {t} \in \mathbf {y} ^ {t}} b _ {y _ {k} ^ {t}} (A _ {* k} ^ {t}) f (y _ {k + 1} ^ {t} | y _ {k} ^ {t}).
$$

However, $\lambda^t$ has two unknown sets of parameters $\theta$ and $\rho$ , we also need to learn these two parameters. Here, we discuss parameter update of Label Dependent Model with the purpose of finding $\lambda^* = \arg \max_{\lambda^t} P(\mathbf{A}^t | \boldsymbol{\lambda}^t)$ . $\mathcal{A}^t$ can be directly obtained from general knowledge background, $\pi^t$ can be obtained by counting the answers of agents, and $\mathcal{B}^t$ is obtained with $b_{y_k^t}(\mathbf{A}_{*k}^t)$ which contains two parameter sets $(\theta, \rho)$ .

For a task $x_{t}$ without ground truth, we update the parameter set $(\boldsymbol{\theta},\boldsymbol{\rho})$ based on the EM algorithm. Before talking about the EM algorithm of the HMM model, we first need to define the forward process of the HMM model, we define:

$$
\alpha_ {k} (y _ {k} ^ {t}) = P (A _ {* 1} ^ {t}, A _ {* 2} ^ {t}, \dots , A _ {* k} ^ {t}, y _ {k} ^ {t} | \boldsymbol {\lambda})
$$

which is the probability of collecting the partial label answer $[A_{*1}^{t}, A_{*2}^{t}, ..., A_{*k}^{t}]$ , and ending up in the label value $y_{k}^{t}$ of the $k$ th label. Next, we recursively define the forward process as follows:

$$
\alpha_ {1} (y _ {1} ^ {t}) = \pi^ {t} \cdot b _ {y _ {1} ^ {t}} (\mathbf {A} _ {* 1} ^ {t})
$$

$$
\alpha_ {k} (y _ {k} ^ {t}) = \left[ \sum_ {y _ {k - 1} ^ {t} \in \{0, 1 \}} \alpha_ {k - 1} (y _ {k - 1} ^ {t}) f (y _ {k} ^ {t} | y _ {k - 1} ^ {t}) \right] \cdot b _ {y _ {k} ^ {t}} (\mathbf {A} _ {* k} ^ {t})
$$

$$
P (\mathbf {A} ^ {t} | \boldsymbol {\lambda} ^ {t}) = \sum_ {k = 1} ^ {K} \alpha_ {k} (\mathbf {y} ^ {t})
$$

Then we give the definition of the backward process of the HMM model:

$$
\beta_ {k} (y _ {k} ^ {t}) = P (A _ {* k + 1} ^ {t}, A _ {* k + 2} ^ {t},..., A _ {* K} ^ {t} | y _ {k} ^ {t}, \pmb {\lambda} ^ {t})
$$

which is the probability of collecting the partial label answer $\left[A_{*k+1}^{t}, A_{*k+2}^{t}, ..., A_{*K}^{t}\right]$ , and starting in the label value $y_{k}^{t}$ of the kth label. Also, we recursively define the backward process as follows:

$$
\beta_ {1} (y _ {1} ^ {t}) = 1
$$

$$
\beta_ {k} (y _ {k} ^ {t}) = \sum_ {y _ {k + 1} ^ {t} \in \{0, 1 \}} f (y _ {k + 1} ^ {t} | y _ {k} ^ {t}) \beta_ {k + 1} (y _ {k + 1} ^ {t}) b _ {y _ {k} ^ {t}} (\mathbf {A} _ {* k} ^ {t})
$$

$$
P (\mathbf {A} ^ {t} | \boldsymbol {\lambda} ^ {t}) = \sum_ {k = 1} ^ {K} \beta_ {k} (y _ {k} ^ {t}) \pi^ {t} b _ {y _ {1} ^ {t}} (A _ {* 1} ^ {t})
$$

According to the forward process and backward process of the defined HMM model, we get the generation probability of each label value of the task, which will be used in the EM algorithm:

$$
\begin{array}{l} P (y _ {k} ^ {t} | \mathbf {A} ^ {t}, \boldsymbol {\lambda} ^ {t}) = P (\mathbf {A} ^ {t} | \boldsymbol {\lambda} ^ {t}) P (\mathbf {A} ^ {t}, y _ {k} ^ {t} | \boldsymbol {\lambda}) \\ \propto P (\mathbf {A} ^ {t}, y _ {k} ^ {t} | \pmb {\lambda} ^ {t}) \\ = P (\mathbf {A} _ {* 1} ^ {t}... \mathbf {A} _ {* k} ^ {t}, y _ {k} ^ {t} | \boldsymbol {\lambda} ^ {t}) P (\mathbf {A} _ {* k + 1} ^ {t}... \mathbf {A} _ {* K} ^ {t} | y _ {k} ^ {t}, \boldsymbol {\lambda} ^ {t}) \\ = \alpha_ {k} (y _ {k} ^ {t}) \cdot \beta_ {k} (y _ {k} ^ {t}) \\ \end{array}
$$

E-step. Let $y^{t}$ is the label answer set of task $x^{t}$ . The posterior probability that $y^{t}$ is the correct answer of the task can be obtained:

$$
P (\mathbf {y} ^ {t} | \mathbf {A} ^ {t}, \boldsymbol {\lambda} ^ {t}) = \pi^ {t} \prod_ {k = 1} ^ {K} f (y _ {k + 1} ^ {t} | y _ {k} ^ {t}) b _ {y _ {k} ^ {t}} (\mathbf {A} _ {* k} ^ {t}) \tag {12}
$$

M-step. With respect to the conditional distribution of Y given the observed noisy label answer A under the current estimates of parameters $\lambda^{old}$ , we can calculate the expected value of the complete log-likelihood function, as follow:

$$
\begin{array}{l} \mathbf {Q} (\boldsymbol {\lambda} ^ {t}, \boldsymbol {\lambda} _ {o l d} ^ {t}) = \sum_ {\mathbf {y} \in \mathbf {Y} ^ {t}} \ln P (\mathbf {A} ^ {t}, \mathbf {y} ^ {t} | \boldsymbol {\lambda} ^ {t}) P (\mathbf {A} ^ {t}, \mathbf {y} ^ {t} | \boldsymbol {\lambda} _ {o l d} ^ {t}) \\ = \sum_ {\mathbf {y} ^ {t} \in \mathbf {Y} ^ {t}} \ln \pi^ {t} P (\mathbf {A} ^ {t}, \mathbf {y} ^ {t} | \boldsymbol {\lambda} _ {o l d} ^ {t}) + \\ \sum_ {\mathbf {y} ^ {t} \in \mathbf {Y} ^ {t}} \left[ \sum_ {k = 1} ^ {K} \ln f (y _ {k} ^ {t} | y _ {k - 1} ^ {t}) \right] P (\mathbf {A} ^ {t}, \mathbf {y} ^ {t} | \boldsymbol {\lambda} _ {o l d} ^ {t}) + \\ \sum_ {\mathbf {y} ^ {t} \in \mathbf {Y} ^ {t}} \left[ \sum_ {k = 1} ^ {K} \ln (b _ {y _ {k} ^ {t}} (\mathbf {A} _ {* k} ^ {t})) \right] P (\mathbf {A} ^ {t}, \mathbf {y} ^ {t} | \boldsymbol {\lambda} _ {o l d} ^ {t}) \\ \end{array}
$$

Then we can differentiate $\mathbf{Q}(\boldsymbol{\lambda}^{t},\boldsymbol{\lambda}_{old}^{t})$ function to get the gradients. Here, $\pi^{t}, P(\mathbf{A}^{t},\mathbf{y}^{t}|\boldsymbol{\lambda}_{old}^{t}), f(y_{k}^{t}|y_{k-1}^{t})$ are all known, only $b_{y_{k}^{t}}(\mathbf{A}_{*k}^{t})$ contains the unknown variable we want to estimate. So we have $\mathbf{Q}(\boldsymbol{\lambda}^{t},\boldsymbol{\lambda}_{old}^{t}) \propto \sum_{\mathbf{y}^{t} \in \mathbf{Y}^{t}} \left[ \sum_{k=1}^{K} \ln(b_{y_{k}^{t}}(\mathbf{A}_{*k}^{t})) \right] P(\mathbf{A}^{t},\mathbf{y}^{t}|\boldsymbol{\lambda}_{old}^{t})$ . According to Eq.11 which calculate parameter B, we can get know that the result of new Q-function is same as Eq.4. Finally, we could just update HMM parameter as follow:

$$
\theta_ {k} ^ {t} = \mathbb {E} \left[ \mathbb {I} (y _ {k} ^ {t} = 1) \right] \tag {13}
$$

$$
\rho_ {w k} = \frac {\sum_ {x ^ {t} \in \mathcal {T}} \mathbb {I} (a _ {w k} ^ {t} = y) \mathbb {E} \left[ \mathbb {I} (y _ {k} ^ {t} = y) \right]}{\sum_ {x ^ {t} \in \mathcal {T}} \mathbb {I} (a _ {w k} ^ {t} \neq \bot)} \tag {14}
$$

which is similar with the Label Independent Model.

After the EM algorithm converges, the final estimated true label truth of the task $x^{t}$ should be the multi-label label value with the largest posterior probability. That is:

$$
y _ {1} ^ {t}, \dots , y _ {K} ^ {t} = \arg \max P \left(y _ {1} ^ {t}, \dots , y _ {K} ^ {t} \mid \mathbf {A} ^ {t}, \boldsymbol {\lambda} ^ {t}\right) \tag {15}
$$

# D. Algorithm

The proposed method is conducted in three phases according to Algorithm 2: 1.label correlation estimation, 2.model parameter learning and 3.label truth calculation. In the label correlation estimation phase, we use the collected label results to estimate possible label relevance. In the model parameter learning phase, we use the proposed new probability graph model consider label truth latent correlation by Hidden Markov Model to jointly estimate task difficulty and agent reliability. At last, in the label truth calculation phase, we output the estimated label truth by Equation 15.

Algorithm 2: Truth Discovery with Label Correlation   
Input: Task set T, Agent set W, Label Answer set A
Output: Integrated Labels $y^{t}$ for each task $x^{t}$ 1 Initialize task difficult parameter $\theta_{k}^{t}$ for $x^{t} \in T$ , and agent reliability parameter $\rho_{wk}$ for $w \in W$ ;

2 Initialize label correlation matrix A from label answer set based on Equation 10;

3 while not converge do

4    // E step

5    for each task $x^{t} \in T$ do

6    Calculation expectation by Equation 12;

7    end

8    // M step

9    Update task difficulty parameter by Equation 13;

10    Update agent reliability parameter by Equation 14;

11 end

12 // convergence

13 for each task $x^{t} \in T$ do

14    Calculate the label truth by Equation 15;

15 end

16 return all task label truth $y^{t}$ .

# IV. EVALUATION

We implemented the proposed truth discovery algorithm and conducted an extensive set of experiments on a real-word image label tasks. In this part, we give the results of our proposed algorithm running on real data sets.

# A. Experimental Setup

1) Dataset: In our experiments, we conducted experiments on MS COCO 2020 datasets [15]. COCO is a large-scale object detection, segmentation, and captioning dataset, which has 330K images, 80 object categories, and more than 200K labeled categories. We select 1000 pictures and their labeled categories as the target tasks and the ground truth of our experiment. From this, we generated a multi-label labeling task. Next, we collected some popular trained image classification

models [16], and we have also trained some general models [17], [18] ourselves to generate agent label answer results for these labels. We also assume that we have ten optional labeling service sellers who have different labeling agents. Therefore, we randomly assign the collected label agents to these ten sellers, while ensuring that each seller can provide label agent services and no seller can annotate all target labels. So far, we have simulated and constructed a multi-agent annotation scene to obtain the buyer's annotation result data set.

2) Comparisons: To the best of our knowledge, there is the first truth discovery algorithm proposed for label annotation in agent market. Therefore, as for the evaluation, we choose the following three base truth discovery methods run for comparison:

- Major Voting(MV): This is a general method which selects the label answer provided with the maximum confidence level as the truth. The immediate limitation here is this method does not take the agent's reliability and the correlation between the label truth into account.   
- Truth Discovery without Label Correlation: This is a method which we describe in Section III-B. The immediate limitation here is this method does not take into account the correlation between the label truth. We call this method as "Independent".   
- Truth Discovery with Label Correlation: This is the method which we proposed in Section III-C of this paper. We call this method as "Dependent".   
3) Performance Metric: Our algorithm is to output the estimated value of the each label for each task, so we use the accuracy of the entire output label value as the evaluation metric of the algorithm experiment. And accuracy is formally defined as the ratio of correctly estimated labels:

$$
A c c u r a c y = \frac {1}{T \cdot K} \sum_ {t = 1} ^ {T} \sum_ {k = 1} ^ {K} \mathbb {I} (\hat {y} _ {k} ^ {t} = y _ {k} ^ {t})
$$

Then we also hope that the confidence of our estimated label truth is reliable enough, that is, the confidence of 0.9 for the same estimated label truth is better than 0.6.

# B. Performance of Truth Discovery Algorithm

In this section, we evaluate our truth discovery algorithm by conducting several experiments on MS COCO 2020 dataset with another two baseline method.

On the MS COCO data set, we collect different data set versions and repeat the experiment many times to obtain the results, as shown below. We first randomly select different numbers $K = 3,6,9$ of target labels to generate target labeling tasks. In each case of K, we also generate the target annotation data set multiple times, perform multiple repeat experiments, and finally take the average result of the multiple repeat experimental results. The experimental results are shown in the figure below. In different k situations, our truth discovery algorithm shows better performance. For the experimental result of accuracy, MV method has the worst result. After we consider the reliability of the agent, the accuracy is improved, which is the second method: Truth Discovery without Label Correlation. Then we further consider the correlation between label truth, the accuracy result become more accurate. Another experimental result is about the confidence of the estimated label truth. The experimental result shows that the MV method has the lowest confidence in the estimated label truth. That's because, without considering any external factors, simply taking the average value of the confidence of the output result of the labeling agent will be affected by inaccurate output, resulting in low confidence. After we consider the reliability of the agent and the correlation between the label truth, we can correct the output result of the labeling agent, so as to obtain a more confident and reliable estimated label truth.

![](images/05c368d39ab07e960d833f6170df8ccbafde3a53511436a385d90c87d7f642c4.jpg)



(a) accuracy on each task(K=3)

![](images/310f21f6ee42c6e8881f6c7e78120e6f65c88e16df40c79c81e44803e83d3b6a.jpg)



(b) confidence on each task(K=3)

![](images/cd939a81ce28f8bb8fe66888abdc98c3d0126079caa315ca1798da47e4a30e9a.jpg)



(c) accuracy on each task(K=6)

![](images/44483fc3ba53f6e6a57100fd0413e750fa8f55e2df07434c31eecd5f6668bc27.jpg)



(d) confidence on each task(K=6)

![](images/a4a3419f4542e6d50bf3051d0b4703d2bba2688114b28a18f309d6d3e50fdbf1.jpg)



(e) accuracy on each task(K=9)

![](images/a6bb4c9fbed056b1c3e38abcf350c3a24dec7a5bf92251ad26a437ed0401253d.jpg)



(f) confidence on each task(K=9)   
Fig. 3: Comparison results in accuracy and confidence under different K.

# V. RELATED WORK

Image Classification. Image classification is the most basic task in computer vision. From the simpler 10-class gray-scale image handwritten digit recognition task MNIST, to the larger 10-class Cifar10 and 100-class Cifar100 tasks, to the later ImageNet task, the image classification model is accompanied by the growth of the dataset, step by step up to today's level. Now, in a dataset with more than 10 million images and more than 20,000 categories like ImageNet, the capability of computer image classification model has surpassed that of human. From the late 1990s to the beginning of this century, SVM and K-nearest neighbors methods were used more. The LeNet network was born in 1994, and after many iterations, the LeNet5 [2] in 1998 was born, which is a widely known version. In 2012, AlexNet [3] was the first deep network in the true sense. Compared with the 5 layers of LeNet5, its number of layers has increased by 3, and the number of network parameters has also greatly increased. The input has also changed from 28 to 224. In 2015, ResNet [4] won the ILSVRC classification task championship. It exceeded the recognition level of humans with an error rate of $3.57\%$ , and created a new model record with a 152-layer network architecture. In addition, the classifications mentioned above are all single-label classification problems, that is, each picture corresponds to only one category, and many tasks are actually multi-label classification problems. For multi-label classification problems, there are usually two solutions, namely conversion to multiple single-label classification problems, or direct joint research. Han [5] proposed a collaborative embedding approach, which exploits the association between embedding features and annotations. Yang [6] designed a NNs which can learn to predict labels and exploit correlation among them simultaneously.

Truth Inference in Crowdsourcing. Crowdsourcing is another way to get labels for images. The crowdsourcing system assigns the images to human and gets redundant label answers. A fundamental problem in this system is Truth Inference, which decides how to effectively infer the truth. To address the problem, a common method is to construct a set of labeled answers for each label by labeling agents, and then Majority Voting (MV), which selects the answer provided with the maximum confidence level as the truths. The immediate limitation here is this method does not take every label agents reliability into account, as every labeling agent has different labeling reliability. The earliest Dawid & Skenes (DS) algorithm [19] use a confusion matrix to model the reliability of uncertain workers. Then, more and more methods [20]–[25], such as gradient descent based, Gibbs sampling based, variational inference based, were proposed to solve the truth inference problem in crowdsourcing systems. The problem solved by this article is similar to the truth inference problem in the crowdsourcing system, but has a fundamental difference. In a crowdsourcing system, people expressing the existence of an object can directly provide a label answer: 1; however, in the label agent scene, the agent expresses the possibility of an object's existence with a confidence index, which may be very high or very low. Confidence is a continuous value from 0 to 1, which contains more information than the 0/1 single-valued label answer in the crowdsourcing system. In addition, the level of people's labeling ability fluctuates greatly. For example, a student with excellent ability may also get a low score because of illness, and the general probability graph model cannot describe this characteristic. The performance of the trained convergent deep learning model is stable on most image, and the general probability graph model is sufficient to describe these label agents' reliability.

# VI. CONCLUSION

In this article, we define a new data labeling scenario: the multi-agent labeling scenario. And we solve the problem of truth discovery in multi-agent labeling scenario. We have established a new probability graph model taking into account the reliability of the agent and the correlation between the label truth. Next, a novel expectation-maximization based iterative method for truth discovery is designed to first estimate the truth, and then dynamically updates each agents reliability. Finally, we conduct several experiments on a real-world dataset to testify the performance of our method.

# ACKNOWLEDGMENT

The research is supported by National Key R&D Program of China 2017YFB1003003, National Natural Science Foundation of China with No. 61822209, No. 61932016, No.61625205, No. 61520106007.

# REFERENCES

[1] https://ai.baidu.com/   
[2] LeCun Y, Bottou L, Bengio Y, et al. Gradient-based learning applied to document recognition[J]. Proceedings of the IEEE, 1998, 86(11): 2278-2324.   
[3] Krizhevsky A, Sutskever I, Hinton G E. Imagenet classification with deep convolutional neural networks[J]. Advances in neural information processing systems, 2012, 25: 1097-1105.   
[4] He K, Zhang X, Ren S, et al. Deep residual learning for image recognition[C]//Proceedings of the IEEE conference on computer vision and pattern recognition. 2016: 770-778.   
[5] S. Han, J. Pool, J. Tran, and W. Dally. Learning both weights and connections for efficient neural network. In Advances in neural information processing systems, pages 11351143, 2015.   
[6] Y. Yang, Y.-F. Wu, D.-C. Zhan, Z.-B. Liu, and Y. Jiang. Complex object classification: A multi-modal multi-instance multi-label deep network with optimal transport. In Proceedings of the 24th ACM SIGKDD, pages 25942603. ACM, 2018.   
[7] L. Kaiser, A. N. Gomez, N. Shazeer, A. Vaswani, N. Parmar, L. Jones, and J. Uszkoreit. One model to learn them all. arXiv preprint arXiv:1706.05137, 2017.   
[8] J. Ma, Z. Zhao, X. Yi, J. Chen, L. Hong, and E. H. Chi. Modeling task relationships in multi-task learning with multi-gate mixture-of-experts. In Proceedings of the 24th ACM SIGKDD, pages 19301939. ACM, 2018.   
[9] W. Chen, J. Wilson, S. Tyree, K. Q. Weinberger, and Y. Chen. Compressing convolutional neural networks in the frequency domain. In Proceedings of the 22nd ACM SIGKDD, pages 14751484. ACM, 2016.   
[10] B. Wu, F. N. Iandola, P. H. Jin, and K. Keutzer. Squeezedet: Unified, small, low power fully convolutional neural networks for real-time object detection for autonomous driving. In CVPR Workshops, pages 446454, 2017.   
[11] J. Jiang, G. Ananthanarayanan, P. Bodik, S. Sen, and I. Stoica. Chameleon: scalable adaptation of video analytics. In Proceedings of the 2018 Conference of the ACM Special Interest Group on Data Communication, pages 253266. ACM, 2018.   
[12] Fang Y, Sun H, Li G, et al. Context-aware result inference in crowdsourcing[J]. Information Sciences, 2018, 460: 346-363.   
[13] Zhang J, Wu X. Multi-label inference for crowdsourcing[C]//Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery Data Mining. 2018: 2738-2747.   
[14] Li S Y, Jiang Y, Chawla N V, et al. Multi-label learning from crowds[J]. IEEE Transactions on Knowledge and Data Engineering, 2018, 31(7): 1369-1382.   
[15] T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dolla r, and C. L. Zitnick. Microsoft coco: Common objects in context. In European conference on computer vision, pages 740755. Springer, 2014.

[16] J.Redmonand A. Farhadi. Yolov 3: An incremental improvement. arXiv, 2018.   
[17] Ballester P, Araujo R. On the performance of GoogLeNet and AlexNet applied to sketches[C]//Proceedings of the AAAI Conference on Artificial Intelligence. 2016, 30(1).   
[18] Wu Z, Shen C, Van Den Hengel A. Wider or deeper: Revisiting the resnet model for visual recognition[J]. Pattern Recognition, 2019, 90: 119-133.   
[19] Alexander P Dawid and Allan M Skene. 1979. Maximum likelihood estimation of observer error-rates using the EM algorithm. Applied statistics 28, 1 (1979), 2028.   
[20] Vikas C Raykar, Shipeng Yu, Linda H Zhao, Gerardo Hermosillo Valadez, Charles Florin, Luca Bogoni, and Linda Moy. 2010. Learning from crowds. Journal of Machine Learning Research 11, Apr (2010), 12971322.   
[21] Matteo Venanzi, John Guiver, Gabriella Kazai, Pushmeet Kohli, and Milad Shok-ouhi. 2014. Community-based Bayesian aggregation models for crowdsourcing. In WWW. 155164.   
[22] Yuchen Zhang, Xi Chen, Denny Zhou, and Michael I Jordan. 2014. Spectral methods meet EM: A provably optimal algorithm for crowdsourcing. In NIPS. 12601268.   
[23] Gianluca Demartini, Djellel Eddine Difallah, and Philippe Cudr-Mauroux. 2012. ZenCrowd: Leveraging probabilistic reasoning and crowdsourcing techniques for large-scale entity linking. In WWW. 469478.   
[24] David R Karger, Sewoong Oh, and Devavrat Shah. 2011. Iterative learning for reliable crowdsourcing systems. In NIPS. 19531961.   
[25] Jacob Whitehill, Ting-fan Wu, Jacob Bergsma, Javier R Movellan, and Paul L Ruvolo. 2009. Whose vote should count more: Optimal integration of labels from labelers of unknown expertise. In NIPS. 20352043.