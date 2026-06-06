# AdaShifter: An Online Data Annotation Framework Under Human-Machine Collaboration

Shanyang Jiang1,2 and Lan Zhang1,2(B)

1 School of Data Science, Hefei, China yang12@mail.ustc.edu.cn

2 University of Science and Technology of China, Hefei, China zhanglan@ustc.edu.cn

Abstract. A major barrier to deploying current smart models lies in their non-reliability to dynamic environments. Prediction models, although proficient in delivering accurate predictions for the fixed training data, cannot ensure robust performance in all novel environments. Nonetheless, conventional systems often rely on human experts to discern when to permit the system to autonomously handle tasks or when the human expert should provide an opinion? We propose a novel design AdaShifter: Adaptive Online Shifter via an online incremental learning process, in which the algorithm is an intermediary layer between prediction models and downstream human experts that aims to request human experts only when it is likely to be beneficial for their annotations. The results of a large-scale experiment show that our algorithm manages to request human experts at times of need and to significantly improve annotation compared to fixed, non-interactive, requesting approaches.

Keywords: Data annotation Bayesian process Mutual information

# 1 Introduction

In recent years, smart models have been increasingly utilized to supplement online annotation systems, particularly in domains like video abnormal detection [21], and video content moderation [10]. In current practical applications and relevant studies, the prevailing practice is that human experts frequently and actively provide modification suggestions for each prediction problem and model outcome. This work addresses a different but crucial question within the framework of human-in-the-loop annotation: when should human experts provide opinions? We explore whether it is possible to automatically identify situations where human experts are most helpful, i.e., whether human experts are more accurate than current prediction models, and whether such an approach of seeking human expert advice only when needed can indeed help models improve their annotations.

In this work, we assume that experts are anticipated to furnish accurate results. We posit this as a reasonable assumption that can be attainable in practical settings. We address the question of when to transition between prediction models and human experts. In this study, we delve into this problem from a theoretical standpoint and formulate an online algorithm that autonomously learns to optimally shift responsibilities among multiple agents. However, achieving this objective entails addressing two challenges:

Static Models and Dynamic Environment. In practical annotation systems, due to limited computational resources, the update frequency of annotation models cannot be too high, while the environment is constantly changing. Furthermore, for the overall annotation system, the current accuracy of the annotation model on the data generated in the current environment is also unknown.

Controllable Filtering Rate. In each downstream application, although human experts can actively intervene in the annotation process, the total workload budget that each human expert can adapt to and tolerate may vary. Hence, we aim for our algorithms to incorporate mechanisms enabling the adjustment of the workload shift for each agent during a specified period.

Based on that, we propose a novel design Adaptive Online Shifter (AdaShifter) via an online incremental learning process, in which the algorithm is an intermediary layer between prediction models and downstream human experts which aims to request human experts only when it is likely to be beneficial for their annotations. Specifically, our shifter module applies an online incremental learning process, a learned requesting policy that depends on the historical annotated data and adaptively requests human experts’ opinions only when it is likely to improve annotation performance:

– We first present the modified human-machine annotation process, and then define an adaptive online shifter that can decide whether to accept the results of the base prediction model or request advice from human experts for incoming samples.

– We adopt an online incremental learning approach based on historical annotated data, calculating both the prediction loss of the base model and the expected gain growth from human experts. We also analyze the online regret of our annotation framework.

We validated, through a series of annotation experiments with real-world data, that our online adaptive sample shifter consistently improves annotation accuracy compared to state-of-the-art methods. Moreover, on the NWPU-Campus dataset, even with only a portion of labeled data, its performance surpasses that of Bayesian active request methods.

# 2 Related Work

# 2.1 Model Labeling Under Human Assistance

Human annotations construct hybrid human-ML systems that synergize both strengths to enhance ML model performance [7]. The crowdsourcing works extensively employ human annotations for diverse tasks, including text processing [3], audio transcription [16], taxonomy creation [6], and social media analysis [12]. Research in active learning [19] illustrates that strategically sampling data points can reduce human workload, emphasizing the improvement of machine learning models rather than merely aiding raters. [8] have focused on ridge regression under human assistance and shown that a simple greedy algorithm can find a solution with nontrivial approximation guarantees. [9] demonstrated that, for support vector machines, it is possible to address the classification problem under human assistance using algorithms with approximation guarantees.

# 2.2 Model-Assisted Human Labeling

ML assistance, through predictions and explanations, has demonstrated enhanced efficiency in human labeling quality across various domains, such as video content moderation [5,15]. For example, in the work by [5], a model trained on past cross-community moderation decisions is utilized to assist Reddit human moderators in more effectively identifying violations. Interactive ML assistance, as used by [1], aids human annotators in generating adversarial examples to enhance a natural language question-answering model. In their work, [20] has initiated the development of automated decision support systems designed to improve performance with high probability without requiring human experts to understand the accuracy of each recommendation. In their exploration, [18] investigated a framework wherein the learning model has the option to defer to an expert or make a prediction. They proposed a novel surrogate loss through a reduction to multiclass cost-sensitive learning. Notably, the learned model is adapted to the underlying human expert to achieve improved performance compared to deploying the model or expert individually.

# 3 Problem Formulation

# 3.1 Initial Setting

In this work, we initially define online human-machine collaborative annotation as an online incremental learning problem, considering the arrival of data in realtime. Let Γ represent an exogenous distribution from which a streaming sequence of features $x _ { t }$ , where $t \in { 1 , . . . , T }$ , is drawn and indexed by time step. Meanwhile, we assume that we have sought access to a human expert $h _ { e x p }$ that may possess additional information beyond the base predictor to classify samples according to the target variable Y . So in our Annotator System, we consider three modules: a base inference predictor, a human expert, and an adaptive online data stream shifter.

We consider one base predictor $h _ { b a s e }$ trained on an initial static distribution $\{ \mathcal { X } , \mathcal { Y } \}$ , where $\mathcal { X }$ denotes the samples’ features and $\mathcal { V }$ denotes the target labels (e.g., possible class labels for classification tasks, possible values of the dependent variable for regression tasks). When we deploy the base predictor into a new dynamic environment with an input stream $\{ x _ { 1 } , . . . , x _ { T } \} \in \mathcal { X } ^ { \prime } , \{ \mathcal { X } ^ { \prime } , \mathcal { Y } ^ { \prime } \} \in \tau$ , we cannot assess the accuracy of the base model’s predictions at this moment, as the data distribution in the current environment differs from that of the initial training dataset.

So, our task is to determine, for each input sample $x _ { t }$ , whether it should be annotated by the base predictor: $\bar { y } _ { t } = \tilde { y } _ { t } = h _ { b a s e } ( x _ { t } )$ or to request the human expert: $\bar { y } _ { t } = \hat { y } _ { t } = h _ { e x p } ( x _ { t } )$ , in order to achieve the highest annotation accuracy for the final sample and label set. Formally, let $( X , Y ) = \{ ( x _ { t } , y _ { t } ) \} _ { t = 1 } ^ { T }$ represent $T$ pairs of samples $x _ { i }$ and their corresponding unknown class labels $y _ { i }$ . Let $\widetilde { D }$ represent the sample label set generated by the prediction model, and let $\widehat { D }$ represent the sample label set provided by human experts. Our goal is to maximize label accuracy $\textstyle \sum _ { t = 1 } ^ { T } \mathbb { I } [ y _ { t } = { \bar { y } } _ { t } ]$ by selecting a sample set to be annotated by the prediction model and a sample set to be labeled by human experts for the input sample data stream where $\bar { y } _ { t } = \{ \tilde { y } _ { t } , \hat { y } _ { t } \}$ .

# 3.2 Adaptive Online Shifter

Initially, given a human expert and a prediction model, at each time step $t \in$ $\{ 1 , . . . , T \}$ , our annotation system state is characterized by the current historical annotated data $d _ { t }$ , and a shifter module $s _ { t } \in \{ 0 , 1 \}$ , which determines to accept the base prediction model’s output $\tilde { y } _ { t }$ or request to the human expert $\hat { y } _ { t }$ . We start at a predefined initial labeled dataset $d _ { 0 } = \{ ( x _ { 0 } , y _ { 0 } ) \}$ . In the above, the switch value is given by a deterministic and time-varying shifter policy $s _ { t } = \pi _ { t } ( d _ { t } , s _ { t - 1 } )$ .

Annotation System with AdaShifter. Let $\begin{array} { r } { s : = \ ( h _ { b a s e } } \end{array}$ , AdaShifter, $h _ { e x p } )$ denote the adaptive online annotation system as a whole. Given a sample $x _ { t }$ from an online arrival data stream and its base prediction $\tilde { y } _ { t } = h _ { b a s e } ( x _ { t } )$ , the shifter module defines a policy distribution $s \left( \cdot | x _ { t } , \tilde { y } _ { t } \right)$ over the space of shifter $S : = \{ 0 , 1 \}$ , consisting of options accept $s = 0$ , or intervene and request the human expert $s = 1$ . Define the shifter module s induces the over-system policy as:

$$
h _ {\mathcal {S}} (\bar {y} | x, \tilde {y}) = \mathbb {E} _ {x \sim \rho \{X \}} [ \mathbb {I} [ s (x, \tilde {y}) = 0 ] (\bar {y} = \tilde {y}) + \mathbb {I} [ s (x, \tilde {y}) = 1 ] (\bar {y} = \hat {y}) ]. \quad (1)
$$

System Goal. Our objective diverges from traditional supervised learning as our primary focus is on the performance of the Adaptive Annotation System, rather than the classifier performance $h _ { b a s e }$ . Furthermore, annotation, learning, and evaluation are all conducted online in our approach. In general, we initially contemplate the corresponding supervised learning objective, which is primarily concerned with minimizing the generalization error of the model over the underlying data distribution, also known as the model risk:

$$
\mathcal {R} (h _ {\mathcal {S}}) := \mathbb {E} _ {x \sim \rho \{X \}} l (y, h _ {\mathcal {S}} (\bar {y} | x, \tilde {y})) \tag {2}
$$

Here, l represents a chosen loss function. Given a shifter policy s, the system risk in each round t is the expected error of the induced system policy, along with the upfront cost of shifter decisions:

$$
\mathcal {R} _ {t} (h _ {\mathcal {S}}) = \mathbb {E} _ {x \sim \rho \{X \}} [ \mathbb {I} _ {s (x _ {t}, \tilde {y} _ {t}) = 0} l (x _ {t}, y _ {t}, \tilde {y} _ {t}) + \mathbb {I} _ {s (x _ {t}, \hat {y} _ {t}) = 1} l (x _ {t}, y _ {t}, \hat {y} _ {t}) ]. \tag {3}
$$

Our objective is to devise an adaptive online shifter that determines when to intervene and solicit the human expert to minimize cumulative regret over a potentially unspecified horizon. At each time t, the shifter produces an action s indicating where the algorithm should be at time t as follow:

$$
\operatorname{Regret} \left(h _ {\mathcal {S}}\right) [ T ] := \sum_ {t = 0} ^ {T} \left(\mathcal {R} _ {t} \left(h _ {\mathcal {S}} ^ {*}\right) - \mathcal {R} _ {t} \left(h _ {\mathcal {S}}\right)\right), \tag {4}
$$

# 4 Selective to Request for Online Annotation

# 4.1 Adaptive Online Shifter Among Human and Models

Building on the preceding discussion, the determination to accept the sample labels from the prediction model or request re-annotation from human experts hinges on evaluating the reliability and diversity of the sample labels generated by the prediction model for the current input. At each timestep $t \in \{ 1 , . . . , T \}$ , we are presented with a lose function $l _ { t } ( x _ { t } , y _ { t } , \bar { y } _ { t } ; d _ { t - 1 } )$ where $\bar { y } _ { t } = \mathbb { I } _ { s = 0 } \left[ \bar { y } _ { t } = \tilde { y } _ { t } \right] +$ $\mathbb { I } _ { s = 1 } \left[ \bar { y } _ { t } = \hat { y } _ { t } \right]$ , and our task is to decide either $s = 0$ to stay at $d _ { t } = d _ { t - 1 }$ and obtain the expected gain $l _ { t } ( x _ { t } , y _ { t } , \tilde { y } _ { t } ; d _ { t } = d _ { t - 1 } )$ , or $s \ = \ 1$ to move to some other (possibly cheaper) state $d _ { t } = d _ { t - 1 } \cup ( x _ { t } , \hat { y } _ { t } )$ and obtain $l _ { t } ( x _ { t } , y _ { t } , \hat { y } _ { t } ; d _ { t } =$ $d _ { t - 1 } \cup ( x _ { t } , \hat { y } _ { t } ) ) + g ( d _ { t - 1 } , d _ { t } )$ , where $g ( d _ { t - 1 } , d _ { t } )$ is the gain of the transition between −states $d _ { t - 1 }$ and $d _ { t }$ − −. Given any base classifier policy $h _ { b a s e }$ and expert policy $h _ { e x p } ,$ the objective of our greedy shifter policy-AdaShifter $s _ { t }$ is to choose $s \in \{ 0 , 1 \}$ to minimize the immediate system risk incurred over time:

$$
s _ {t} \sim \arg \min _ {s \sim \mathcal {S}} \left[ l _ {t} (\bar {y} | x _ {t}; d _ {t}) + g (d _ {t - 1}, d _ {t}) \right]. \tag {5}
$$

# 4.2 Shifter Learning Algorithm

Accepting Prediction Models’ Results. One straightforward approach is to use the collected set of sample labels $d _ { t - 1 }$ provided by human experts (the ground truth) to estimate the reliability of the current prediction model’s results $( x _ { t } , \tilde { y } _ { t } )$ , i.e., by calculating the loss function size of the prediction model’s results on the ground truth set. This is precisely a way to assess the generalization performance of the prediction model by exploring the ground truth provided by human experts, which represents the true environment. The degree of reliability of the prediction model’s results can be formalized as:

$$
l (x _ {t}, \tilde {y} _ {t}) = l _ {t} (\tilde {y} _ {t} | x _ {t}; d _ {t} = d _ {t - 1}). \tag {6}
$$

Requesting to Human Expert. Concerning annotations supplied by human experts, we compute the expected gain for each request made to an expert from a probabilistic standpoint. Let’s denote the expected model risk as $\mathcal { R } ( d ) \ =$ $\mathbb { E } _ { \theta \sim p ( \cdot | d ) } \mathcal { R } ( h _ { \theta } )$ , note that the determining factor stems from its reliance on the current annotation data d, and θ is the gold parameter variable, which takes values from $\theta \in \Theta$ . This enables the discussion of the label generation process $h _ { \theta } ( y | x ) = p ( y | x , \theta )$ , the marginal distribution $p ( y | d , x ) = \mathbb { E } _ { \theta \sim p ( \cdot | d ) } p ( y | x , \theta )$ .

In the time-step t, if the AdaShifter selects   $s = 0$ , then $d _ { t } = d _ { t - 1 }$ , leading to $\mathscr { R } ( d _ { t } ) = \mathscr { R } ( d _ { t - 1 } )$ . However, when deliberating over choosing $s = 1$ , our objective is to quantify the potential expected gain in system risk by considering the introduction and online learning from the true label $\hat { y } _ { t }$ . Then, we can obtain a bounded generalization error . We introduce the definition of $^ { g , }$ , denoted as $g : v \mapsto g ( v ) = 2 b \left( e ^ { \theta _ { 0 } \left( { \frac { 1 } { e } } \left( v - 1 \right) \right) + 1 } - 1 \right)$ , ensuring that we now have:

$$
\begin{array}{l} \mathcal {R} (d _ {t - 1}) - \mathbb {E} _ {y _ {t} \sim p (\cdot | d _ {t - 1}, x _ {t})} [ \mathcal {R} (d _ {t} | d _ {t - 1}, x _ {t}, y _ {t}) ] \\ \leq 2 b \left(e ^ {\theta_ {0} \left(\frac {1}{e} \left(\mathbb {I} [ \theta ; y _ {t} \mid d _ {t - 1}, x _ {t} ] - 1\right)\right) + 1}\right). \tag {7} \\ \end{array}
$$

Given that g exhibits a monotonically increasing behavior, the above interpretation naturally transforms an information-theoretic criterion (the mutual information) into a decision-theoretic criterion (the expected improvement in posterior risk), aligning with our intended objective. Specifically, the input to function g broadens as follows:

$$
\mathbb {I} \left[ y _ {t}; \theta \mid d _ {t - 1}, x _ {t} \right] = \mathbb {H} \left[ y _ {t} \mid d _ {t - 1}, x _ {t} \right] - \mathbb {E} _ {\theta \sim p (\cdot | d _ {t - 1})} \mathbb {H} \left[ y _ {t} \mid x _ {t}, \theta \right], \tag {8}
$$

This expansion is interpreted as the anticipated reduction in uncertainty within the mode policy if $y _ { t } \sim p ( \cdot | d _ { t - 1 } , x _ { t } )$ is disclosed. This perspective bears similarity to entropy-based strategies in active learning, as discussed in [11]. Notably, upon deployment, $g _ { t } = g ( \mathbb { I } [ \theta ; y _ { t } | d _ { t - 1 } , x _ { t } ] )$ is initially large to make the expert requisition decision, resulting in our method emulating standard incremental learning.

# 5 Experiment

# 5.1 Simulation Experiments

Our first experiments primarily focus on testing two aspects of the properties of the AdaShifter algorithm across different datasets. We focus on the algorithm’s data annotation performance, comparing AdaShifter with existing methods to validate its effectiveness across varying parameters, including expert stochasticity and the number of input samples.

Datasets. We performed simulation experiments on various datasets. The synthetic data stream, referred to as “Gaussian” [17], was generated by randomly sampling data points from a 2D Gaussian function. The dataset named “Motion-Capture” [14] involves recognizing hand postures from continuous streams of data recorded by glove markers. In the “Alzheimer” dataset [2], our goal was to diagnose patients participating in the Alzheimer’s Disease Neuroimaging Initiative study early on. The aim is to determine their cognitive status, whether it falls within the normal range, shows mild impairment, or indicates a risk of dementia.

![](images/c761c52e618d8b0a633f66cab4233ca7493771339f3aeea160a77cc29e72edee.jpg)  
Fig. 1. System Regrets (above) and Mistakes (below).

Benchmarks. Our experimental design entails a comparison of the prediction performance of the system across four distinct experimental treatments. The comparative algorithms employed in our simulation experiments are as follows: No Advice: In this treatment, we initiated by collecting the output results solely from the base prediction model, establishing it as our minimal baseline. Random: This approach involves probabilistically deciding whether to accept the prediction model’s results or request input from human experts. Bayesian Active Request: Drawing inspiration from the methodology outlined in [11,13], the “Bayesian active request” treatment actively reduces entropy by soliciting input from human experts.

Experiment Setup. Every set of experiments consists of a sample label set from n = 2000 rounds of the data stream, with the exception of the synthetic Gaussian dataset where n = 500. These experiments are systematically repeated 10 times, each time employing different random seeds to ensure robustness and reliability in the results. Across all comparative algorithms, the underlying prediction model is implemented using Dirichlet-based Gaussian process classification and regression learning algorithms. To ensure statistical rigor and generalizability, the final performance metric results for each set of experiments are averaged across all 10 repeated trials.

Performance. In the context of repeated simulation experiments, the evaluation of the labeling system’s performance centers around the regret metric. Figure 1 above illustrates the results for all comparative algorithms, with AdaShifter consistently demonstrating lower cumulative regret. This observation indicates that the AdaShifter algorithm consistently performs well and exhibits superior decision-making throughout the experiments. As a secondary evaluation, we assess the mislabeling rate of the labeling system using a ground truth dataset. Figure 1 below showcases the experimental results for the mislabeling rate across all comparative algorithms, revealing that AdaShifter introduces a more effective learning capability. The lower mislabeling rate associated with AdaShifter suggests enhanced accuracy and reliability in the labeling system’s predictions compared to other algorithms under consideration.

![](images/854e4022ccb2b71e381d5ca0717b2b45fe447ff893a9e8cc8adccaf8c3f197b0.jpg)



(a) GaussianProcess+0.0

![](images/52e13776131348c8aad25d9d1056ce8c2f49a99328ef0f92872c0c7fd5d16cf4.jpg)



(b) GaussianProcess+0.1

![](images/b570441880c9c46d3b734212be453fbb1b06bc36ad9b7ab53b85db833dc9019a.jpg)



(c） GaussianProcess+0.2

![](images/bb95e160c7998ae067e32217e6553c3324f0394e4db0dacba01b13882d143379.jpg)



(d) GaussianProcess

![](images/bf8e7b5ce81aee883e77c4a7053c0d9822224b754b4439480f407a5218fc16b1.jpg)



(e) Motion Capture

![](images/ff52533c89cbc2c3a309d10fa6e8af3649ce400e3de9c784dfa48cc83183533e.jpg)



(f）Alzheimer  
Fig. 2. Expert stochasticity (above) and Sample number (below).

Hyper-parameter Analysis. In our investigation, we perform repeated simulation experiments to evaluate the effectiveness of the AdaShifter algorithm under different parameter settings in diverse scenarios. Firstly, we consider the variability in the reliability of labels provided by human experts, depending on the labeling tasks. This variability is simulated by introducing additional random noise into the sampled results from the Gaussian function. As depicted in Fig. 2 above, the performance of the AdaShifter algorithm is most pronounced at lower noise levels. However, its effectiveness diminishes as noise levels increase, indicating that our ability to estimate the reliability of the prediction model results becomes more entangled with noise. Furthermore, we explore the algorithm’s sensitivity to sample diversity by gradually increasing the number of actual samples. The labeling performance, illustrated in Fig. 2 below, demonstrates that the AdaShifter algorithm is responsive to changes in sample diversity. This observation emphasizes the importance of considering sample diversity when optimizing the AdaShifter algorithm for robust and reliable performance across a range of scenarios.

# 5.2 Real Cross-Dataset Annotation

Initially, we employ a Gaussian process-based method and a two-layer fully connected MLP network individually to train a vehicle detection model (1/0) on Dataset NWPUCampus [4]. Following that, we engage in collaboration with both base models and human experts to annotate the test set within Dataset NWPUCampus, AdaShifter’s result shows strong cross-dataset generalizability in Table 1. It means that: 1) Upon the collection of a new dataset, it becomes possible to utilize a universally pre-labeled classification model for the generation of labels; 2) In contrast to Bayesian active requests, where sample selection is closely tied to model re-training, our annotated instances function universally, not limited to the specific model employed for their selection.

Table 1. Accuracy on large-scale dataset NWPUCampus [4]. 

<table><tr><td>NWPUCampus-1K</td><td>Gaussian 0.20%</td><td>Gaussian 1%</td><td>MLP 0.20%</td><td>MLP 1%</td></tr><tr><td>Base</td><td>32.1</td><td>48.9</td><td>35.2</td><td>57.9</td></tr><tr><td>Random</td><td>47.4</td><td>52.8</td><td>43.6</td><td>59.0</td></tr><tr><td>Bayesian</td><td>39.5</td><td>50.9</td><td>47.5</td><td>62.2</td></tr><tr><td>AdaShifter(Ours)</td><td>41.2</td><td>53.2</td><td>49.3</td><td>63.6</td></tr></table>

# 6 Conclusion

In this article, we introduce an innovative approach for handling online data stream samples via online incremental learning, specifically through the development of an adaptive online data stream shifter algorithm Based on historical annotated data. This algorithm seamlessly transitions between the prediction model and human expert labeling, aiming to acquire more accurate annotated labels for enhanced data quality. Through a series of experiments, we demonstrate that our algorithm significantly improves the quality of labeled data.

Acknowledgements. Lan Zhang is the corresponding author. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016 “the Fundamental Research Funds for the Central Universities” WK2150110024.

# References

1. Bartolo, M., Thrush, T., Riedel, S., Stenetorp, P., Jia, R., Kiela, D.: Models in the loop: aiding crowdworkers with generative annotation assistants. arXiv preprint arXiv:2112.09062 (2021)   
2. Beckett, L.A., et al.: The Alzheimer’s disease neuroimaging initiative phase 2: increasing the length, breadth, and depth of our understanding. Alzheimer’s Dement. 11, 823–831 (2015)

3. Bernstein, M.S., et al.: Soylent: a word processor with a crowd inside. In: Proceedings of the 23nd Annual ACM Symposium on User Interface Software and Technology, pp. 313–322 (2010)   
4. Cao, C., Lu, Y., Wang, P., Zhang, Y.: A new comprehensive benchmark for semi-supervised video anomaly detection and anticipation. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (2023)   
5. Chandrasekharan, E., Gandhi, C., Mustelier, M.W., Gilbert, E.: Crossmod: a crosscommunity learning-based system to assist reddit moderators. Proc. ACM Hum.- Comput. Interact. 3(CSCW), 1–30 (2019)   
6. Chilton, L.B., Little, G., Edge, D., Weld, D.S., Landay, J.A.: Cascade: crowdsourcing taxonomy creation. In: Proceedings of the SIGCHI Conference on Human Factors in Computing Systems, pp. 1999–2008 (2013)   
7. De, A.: Invited tutorial: human assisted ML. In: Proceedings of the First International Conference on AI-ML Systems (2021)   
8. De, A., Koley, P., Ganguly, N., Gomez-Rodriguez, M.: Regression under human assistance. In: Proceedings of the AAAI Conference on Artificial Intelligence (2020)   
9. De, A., Okati, N., Zarezade, A., Rodriguez, M.G.: Classification under human assistance. In: Proceedings of the AAAI Conference on Artificial Intelligence (2021)   
10. Deodhar, M., Ma, X., Cai, Y., Koes, A., Beutel, A., Chen, J.: A human-ml collaboration framework for improving video content reviews. In: International Conference on Information and Knowledge Management (2022)   
11. DeSalvo, G., Gentile, C., Thune, T.S.: Online active learning with surrogate loss functions. In: Advances in Neural Information Processing Systems (2021)   
12. Founta, A., et al.: Large scale crowdsourcing and characterization of twitter abusive behavior. In: Proceedings of the International AAAI Conference on Web and Social Media, vol. 12 (2018)   
13. Gal, Y., Islam, R., Ghahramani, Z.: Deep Bayesian active learning with image data. In: International Conference on Machine Learning, pp. 1183–1192. PMLR (2017)   
14. Gardner, A., Kanno, J., Duncan, C.A., Selmic, R.: Measuring distance between unordered sets of different sizes. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (2014)   
15. Lai, V., et al.: Human-AI collaboration via conditional delegation: a case study of content moderation. In: Proceedings of the 2022 CHI Conference on Human Factors in Computing Systems, pp. 1–18 (2022)   
16. Lasecki, W., et al.: Real-time captioning by groups of non-experts. In: Proceedings of the 25th Annual ACM Symposium on User Interface Software and Technology, pp. 23–34 (2012)   
17. MacKay, D.J., et al.: Introduction to gaussian processes. NATO ASI Ser. F Comput. Syst. Sci. 168, 133–166 (1998)   
18. Mozannar, H., Sontag, D.: Consistent estimators for learning to defer to an expert. In: International Conference on Machine Learning (2020)   
19. Settles, B.: Active learning literature survey (2009)   
20. Straitouri, E., Wang, L., Okati, N., Rodriguez, M.G.: Improving expert predictions with conformal prediction (2023)   
21. Vu, H.: Deep abnormality detection in video data. In: IJCAI (2017)