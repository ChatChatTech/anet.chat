# Predicting functional elements and variants effects in non-coding regions based on deep learning

Yunhao Liu1 , Shaoliang Peng1,2,4,5\*, Wenjie Shu3\*,, Bin Jiang1 , Chao Yang1 , Kun Xie1

1 College of Computer Science and Electronic Engineering, Hunan University, China

2 National Supercomputing Centre in Changsha, Hunan University, China

3 Department of Biotechnology, Beijing Institute of Radiation Medicine, China

4 School of Computer Science, National University of Defense Technology, China

5 Peng Cheng Lab, Shenzhen, China

Corresponding Authors: slpeng@hnu.edu.cn, wenjieshu@gmail.com

Abstract—Accurate recognition and annotation of the important functional elements in the genome is an important prerequisite to understand the coding mode of complex regulatory networks in the one-dimensional genome .Despite rapid advances in sequencing and recognition technologies, accurately calling non-coding variant effects from large-scale sequence reads remains challenging.Here we present a deep neural network-based algorithmic framework, DeepMSA, which directly learns a regulatory sequence code from large-scale chromatin-profiling data,enabling to evaluate chromatin effects caused by SNP(single nucleotide polymorphism).

Keywords-non-coding functional elements,convolution neural network learning,variant effects prediction

# I. INTRODUCTION

With the advance of gene sequence research，More and more studies have shown that non-coding regions play a complex role in the transcription stage, and further proved that non-coding genomic variation would also have a great impact on human disease and traits. In recent years, large scientific projects such as Encyclopedia of DNA Elements (ENCODE), modENCODE and Roadmap epigenomics projects[1, 2]provide massive public data related to the identification and annotation of DNA elements. With the booming of next-generation sequencing and the development of bioinformatics, a comprehensive analysis of functional DNA elements in the human genome is possible. However, the current calculation method of predictive regulatory sequence information is mainly to extract the features in the sequence with convolution operation. This method not only fails to effectively extract the global features but also performs well in the prediction of specific several chromatin features. When the feature space is extended, the accuracy will decrease.

An extensible quantitative model that can accurately predict the general annotation such as transcription factor binding sites (TFBS) and DNase Ⅰ digital genomic footprinting (DGF) is the key to this challenge. Although it has a good performance for several special chrome factors including TF binding and histone marks, they show substantially less estimative power while the number of features has been increased. Moreover, multiple sources of evidence indicate that in vivo TF binding depends upon sequence beyond traditionally defined motifs[3]. For example, TF binding can be influenced by cofactor binding sequences, chromatin accessibility and structural flexibility of binding-site DNA[4].DNase I-hypersensitive sites (DHSs) and non-coding RNA related annotation are expected to have even more complex underlying mechanisms involving multiple chromatin proteins[5].DNaseI footprinting enables visualization of regulatory factor occupancy on DNA in vivo at nucleotide resolution and has been widely applied to delineate the fine structure of cis-regulatory regions[6]. Therefore, a flexible and extensible quantitative model that can effectively modularize these complex features is the solution to predict chromatin features accurately from the sequence. Those predictions may then be used to estimate the functional effects of non-coding variants after that.

In order to cope with this fundamental problem, here we propose DeepMSA(deep learning multichannel based sequence analyzer),a convolution neural network-based algorithmic framework for predicting non-coding variant effect. We first constructed a large scale feature space consisting of nine features, including TF binding, DHS, Histone marks, DGF, segementation, genomic evolutionary rate profiling(GERP), identifying topologically associating domains(TADs), short RNA and long RNA profiles. We then compiled a diverse compendium of genome-wide chromatin profiles from the Encyclopedia of DNA Elements (ENCODE) and Roadmap Epigenomics projects[1, 2] to train the model. We also used mice data to verify the model's general ability .

# II. MATERIALS AND METHODS

# A. Datasets and preprocessing

The training data were obtained by combining ENCODE data as the main body and Roadmap Epigenomics data as the supplement.

In order to prepare our model input,we have selected three main features in the feature system(TF binding,DHS and histone marks). We then divided the genes into 200bp segments. Each segment overlapped more than half of the 200-bp with the location corresponding to the main feature set would be kept , otherwise abandoned. We focused on the processed collection with at least one key feature region event, resulting in 28% of the whole genome (857,143,200bp of sequences), which contains training, testing, and validation set for evaluating model performance. (The evaluation of mutation sites will not be limited to this region.)

Each 200bp fragment will be supplemented with 400-bp contextual information before and after, and then mapped to the human GRCh37 reference genome to obtain a 1000-bp base sequence. The 1000-bp DNA sequence is then encoded as a 1000 ×4 matrix in a one-hot coding format.(A is going to be coded as [1,0,0,0],G is going to be coded as[0,1,0,0], C is going to be coded as[0,0,1,0], T is going to be coded as[0,0,0,1].) The final encoded matrix will be paired with 2584 dimensional vectors in the eigenspace of the corresponding position.

Training, test and validation data sets are divided based on chromosomes. Regions of chromosomes 7, 8 and 9 were removed from the set.Chromosome 7 was used for verification while chromosome 8 and chromosome 9 were used to test the prediction effect of the model, and the rest were used for model training. We select the area under the receiver operating characteristic curve(ROC) to evaluate the effect of our model on the test set. The predicted probability for each sequence is computed as the average of the probability predictions for the forward and complementary sequence pairs.

The GRCh37/hg19 genome assembly was used for all analyses in this study.

# B. Model design

Our model is inspired by the structure of the convolutional neural network. Convolutional neural network is a typical multi-layer neural network, and each layer consists of a number of computational units called neurons. Each element is essentially multiplying the input matrix by the parameter matrix to get the output matrix. The output matrix calculated by all neurons in a layer together constitutes the extracted features of the layer.

The deep convolutional network model features sequential alternating convolution and pooling layers that extract sequence features at different spatial scales, followed by one fully connected layer that integrates information from the full-length sequence and a sigmoid output layer that computes probability output for each individual chromatin factor feature. Each layer of the deep convolutional network executes a linear transformation of the output from the previous layer by multiplying a weight matrix, followed by a nonlinear transformation. The weight matrix is learned during training to minimize predictive errors[7].

Considering the shape of the input matrix and the particularity of genetic information, in order to improve efficiency and extract features effectively, we have made some changes to the convolutional network model, as shown in Figure 1. We first divided the convolution kernel into two categories, one being normal convolution kernel and the other being half-volume convolution kernel. Formally, let $\ b X \in \ b R ^ { \mathrm { c \times h } \times \mathrm { w } }$ denote the input feature tensor of a convolutional layer, where h and w represent the height and width of the input and c denote the channels. We then explicitly divided X along the channel dimension into $\mathbf { X } = \{ \mathrm { X } ^ { \mathrm { o } } , \mathrm { X } ^ { \mathrm { R } } \}$ , where $\mathbf { X } ^ { 0 } ~ ( ~ \mathbf { X } ^ { 0 } \in \mathbf { R } ^ { ( 1 - \alpha ) \mathrm { c } \times \mathrm { h } \times \mathrm { w } }$ )denote original size convolution kernel and R X ${ \bf \Xi } ( { \bf \Lambda } { \bf X } ^ { \mathrm { R } } \in {  { \sf R } } ^ { \alpha \mathbf { c } \times \frac { \ln } { 2 } \times \frac { \bf w } { 2 } }$ wh )denote the convolution kernel with reduced volume by a parameter $\alpha \ ( \alpha \in [ 0 , 1 ] )$ . Next, we use the pure self-attention mechanism instead of convolution to extract features. Formally, let ${ \mathrm { Y } } ^ { \mathrm { o . . } \mathrm { o } }$ and ${ \mathrm { Y } } ^ { \mathrm { R } \to \mathrm { R } }$ represent the original tensor and reduced tensor feature extraction steps. Then the operation of extracting features with convolution can be expressed as:

$$
\mathbf {Y} = \mathbf {W} ^ {\mathrm{T}} \mathbf {X}
$$

The feature extraction operation of pure auto attention mechanism can be expressed as[8]:

$$
\mathrm{Y} ^ {\mathrm{O} \rightarrow \mathrm{O}} = \text { soft } \max (\frac {X ^ {O} X ^ {O ^ {T}}}{\sqrt {w}}) X ^ {O}
$$

Finally, pooling and upsampling are used to realize the interaction between the original convolution kernel and the feature extracted by the reduced convolution kernel, so as to enhance the effect of information updating. The calculation of original information update can be expressed as:

$$
\begin{array}{l} \mathrm{Y} ^ {\mathrm{O}} = \mathrm{Y} ^ {\mathrm{O} \rightarrow \mathrm{O}} + \mathrm{Y} ^ {\mathrm{R} \rightarrow \mathrm{O}} \\ = \sigma \left(\frac {X ^ {\mathrm{O}} X ^ {\mathrm{O} ^ {\mathrm{T}}}}{\sqrt {\mathrm{w}}}\right) X ^ {\mathrm{O}} + u p s a m p l i n g \left(\mathrm{W} ^ {\mathrm{R} \rightarrow O} ^ {\mathrm{T}} X ^ {\mathrm{R}}\right) \\ \end{array}
$$

Where  represents the activation function, upsampling( · ) denotes an up-sampling operation to fill the · Matrix with adjacent elements. The result of information interaction is achieved by mapping the samples from the feature map extracted by the reduced volume convolution kernel to the original space. The corresponding reduced volume feature space update event can be represented as:

![](images/5e509ba935fda1b61675069862a2167d37859b349855d9f6604934a1ecabb079.jpg)



Figure 1. Feature extraction method of rmulti-channel layer.

$$
\begin{array}{l} \mathbf {Y} ^ {\mathrm{R}} = \mathbf {Y} ^ {R \rightarrow R} + \mathbf {Y} ^ {O \rightarrow R} \\ = \sigma (\frac {X ^ {\mathrm{R}} X ^ {R ^ {T}}}{\sqrt {w}}) X ^ {\mathrm{R}} + \mathrm{W} ^ {\mathrm{O} \rightarrow \mathrm{R} ^ {\mathrm{T}}} p o o l (X ^ {\mathrm{O}}) \\ \end{array}
$$

Where $\sigma$ represents the activation function, pool( · ) denote Maximum pooling operation. The result of the information exchange is achieved by pooling the feature map and reducing the feature space.More details are shown in Figure 1.

The basic layer types in our model consist of multichannel layers, pooling layers, and fully connected layer. A multichannel layer gets output by convolution operation with a specified number of convolution kernels and self-attention operation.and all outputs are then transformed by activation function(We have chosen ReLU in is study, which would keep values above 0 and sets values below 0 to 0).In the first multichannel layer, the reduced volume input will be obtained byusing convolution mapping and pooling(the original layer input is the input before the convolution). The convolution kernel in attention operation can be regarded as a global position weight matrix(GPWM), and attention manipulation is equivalent to counting GPWM scores. Accordingly, each kernel in the mapping operation can be treated as a local position weight matrix(LPWM), and convolution operation is equivalent to computing the LPWM scores with a moving window with step size 1 on the sequence. In higher-level multichannel layers, each kernel is either GPWM or LPWM over the output of the previous layer.

A pooling layer extracts the maximum element value in the window to reduce the size of the output graph, thus allowing the next multichannel layer to perform feature extraction on a larger space. On the top of the last multichannel layer, we add a full connected layer that can integrate information from the full length of 1,000 bp. Finally, we use the sigmoid layer to predict each chromatin characteristic probability value, and use the sigmoid function to map the probability value to 0\~1.

DeepMSA combined three sub-models to predict the 2584-dimensional feature space. The first model contains three multichannel layers with 320,640and 960 kernels andthe second contains two multichannel layers with 360 and 640 kernels. Whilethe third contains four multichannel layers with 320,480,720 and 1280 kernels. Higher-level multichannel layers in each model receive the fused information of the previous layer and are capable of representing more complex patterns than the lower layers.Three models make predictions for each of the 815 chromatin features(690 TF binding features,125 DHS features),1222chromatin features(1222 histone features) and 546 chromatin features(24 GERP features,64 DGF features,416 RNA features,6 segmentation features,36 TAD features), respectively. Then the three prediction results are spliced together to obtain the prediction results of the feature space. Notably, all the predictors in the output layer share the same set of input from the input layer, which allows the size of the eigenspace applicable to arbitrary scaling while allowing sharing predictive sequence features across chromatin feature predictors.The overall structure of the model is shown in Figure 2.

# C. Model training

To improve the performance of the model, we minimize the target function. It is defined as the sum of negative log likelihood (NLL) and regularization terms for controlling overfitting. Specifically,

$$
\text { target } = N L L + \lambda_ {1} \| W \| _ {2} ^ {2} + \lambda_ {2} \| H ^ {- 1} \| _ {1}
$$

![](images/5648b3d63ffeb9ea51d770c4758740c87469db2d248f4f09003aa117e6dba780.jpg)



Figure 2. Overall model architecture diagram.

$$
\mathrm{NLL} = - \sum_ {s} \sum_ {t} \log (Y _ {t} ^ {s} f _ {t} (X ^ {s}) + (1 - Y _ {t} ^ {s}) (1 - f _ {t} (X ^ {s})))
$$

wheres indicates the index of training samples and t indicates the index of chromatin features. $Y _ { t } ^ { s }$ indicates 0,1 neural networks. L2 regularization term 2W 2 i $\left\| \boldsymbol W \right\| _ { 2 } ^ { 2 }$ s defined to be the sum of squares of all the weight matrix entries. $\left. H ^ { - 1 } \right. _ { 1 }$ is defined to be the L1 norm of all the output values of the last layer (fully connected layer) before the output layer. Additionally, the optimization is subjected to regularization constraints that for any layer m and neuron n, $\left. \ b { W } _ { \mathrm { m } } ^ { n } \right. _ { 2 } \leq \lambda _ { 3 } _ { \mathrm { o r } }$ 3  or the L2 norm of weights for any neuron must not be larger than a specified value.

The momentum stochastic gradient descent method is used to minimize the objective function, and the derivative of all parameters of the model is calculated and the corresponding parameters are adjusted by the standard backpropagation algorithm. During training, we will also adopt dropout mechanism to set the corresponding proportion of random neurons value in the multichannel layer to 0 to further prevent model overfitting and improve model generalization ability.

Our implementation utilizes the Tensorflow1.4r library (https://github.com/tensorflow/tensorflow) and Keras library (https://github.com/keras-team/keras). Tesla V100 GPU was used for training the model.

# D. SNP effects for evaluating sequence features

In order to detect the influence of SNPs on sequence feature information, we collected public data sets of published papers(cancer[9, 10] and depression[11]). We first label for samples, chromatin feature t. $f _ { t } ( X ^ { s } )$ represents the predicted probability output of the model for chromatin feature t given input $X _ { s }$ . We used a combination of multiple regularization techniques typical for training deep

removed the mutant fragments that did not belong to the non-coding region, and then selected the fragments that contained only a single base deletion or substitution within 200bp to splice 400bp before and after to form 1000bp fragments. The effect of a base substitution on a specific feature space score(FSS) can be defined as follow:

$$
\mathrm{FSS} = \sum_ {i = 1} ^ {n} (\log_ {2} (\frac {P _ {i}}{1 - P _ {i}}) - \log_ {2} (\frac {P _ {i} ^ {\prime}}{1 - P _ {i} ^ {\prime}}))
$$

Where P represents the probability predicted for the original sequence and P’ represents the probability predicted for the mutated sequence.The symbol i represents the index in the eigenspace.DeepMSA's capabilities are fully utilized by representing the distance between two sequences in the feature space.

# III. RESULTS

We selected an area under the receiver operator characteristic curve(AUROC) as the main indicator to evaluate the performance of the model, which is a most commonly used metric in classification task.Meanwhile, we also choose the area under the precision-recall curve (AUPRC) as additional metrics to suited to the problems with imbalanced classes.After training our model with the same data set with the existing two models, we compared the characteristic space of our model and the characteristic space system of mice respectively, and the results showed that DeepMSA had great advantages in both the overall precision and the single precision.

![](images/9e12ddaace84e9e4f7f9f389d236cf6dc05d42c72d42d21bf1bf8314276bdb90.jpg)



Figure 3. The prediction accuracy of the three models in feature space.

# A. Prediction on human characteristic space

We train and evaluated performance of different models on a same data set,where training, test and validation data sets are divided based on chromosomes. Regions of chromosomes 7, 8 and 9 were removed from the set.Chromosome 7 was used for verification while chromosome 8 and chromosome 9 were used to test the prediction effect of the model,and the rest were used for model training. The predicted probability for each sequence is computed as the average of the probability predictions for the forward and complementary sequence pairs.There are two models we constructed to predict chromatin effect,including a traditional machine learning model gkmSVM and a deep learning models DeepSEA.Figure 1 Table 1 shows the performance of different models in feature space.It can be seen from Figure 1 that both the deep learning model and the machine learning model are sensitive to the features that account for the majority of the data, instead of paying attention to the relatively small but equally important feature information.In terms of overall accuracy, our model still has good performance.From the results in Table 1, where S stands for threshold and S=0.5 represents the AUC value of the model when the threshold value is 0.5

TABLE I MODELSPERFORMANCE 

<table><tr><td>Model</td><td>S=0.5</td><td>S=0.7</td><td>AUPRC</td></tr><tr><td>gkmSVM</td><td>0.9027</td><td>0.8462</td><td>0.4581</td></tr><tr><td>DeepSEA</td><td>0.9403</td><td>0.8687</td><td>0.4773</td></tr><tr><td>DeepMSA</td><td>0.9517</td><td>0.9101</td><td>0.4963</td></tr></table>

we noticed that when the threshold boundary of judgment was improved, compared with similar models, our model could still maintain high accuracy.This is enough to prove that the multi-channel feature extraction model has a higher threshold tolerance than the single-channel feature extraction model.

# B. Prediction on chromatin effect

We further assessed the FSS score,which has discussed in the method section, using the model's predictive precision.We randomly selected 5,000 pieces of data from more than half of the segments in which the functional components were positive.Then we calculate the effect of central sequence single base mutation on the apparent feature spatial system.What we've observed is that those mutations that cause more changes in the number of functional components are more likely to cause disease.For example,it appears higher score on locus SNP rs4784227 with C-to-T alteration, which can lead to breast cancer[12].For an SNP associated with childhood leukemia on rs12142375[13], the model predicted that the alteration of T to C creates a binding site for GATA1.For an isolated pancreatic agenesis mutation[14], we predicted the deleterious effect to FOXA2 binding with A-to-G alteration.

# C. Prediction on mice gene

To verify the universality of our model, we trained three deep learning models including DeepSMA with a mouse data set[15]which contains the epigenome taken from various types of somatic cells.

![](images/9d038620fb785425af01b3cfdaf6a451b1acde58e02cf35d4e9f9e25aa7a4099.jpg)



Figure 4. ROC renderings on mouse datasets.

As can be seen from the results shown in the figure1. First of all, we can see that compared with DeepSEA model, DeppSEA model with attention mechanism has some improvement in effect. Comparing the effects of the three models, we can find that found the AUROC score can be increased by 3% after applying the attention and multi‐ channel mechanism.

# IV. CONCLUSION

Existing functional element recognition models tend to focus on predicting specific apparent features, and the increasing size of the feature space will lead to a decrease in the performance of existing models.And one of the preconditions for understanding disease is to predict the complete apparent signature.Our model chooses to use the strategy of combining ATTENTION and frequency division to predict the large‐scale feature space, and the performance of the model is also obtained from multiple human epigenetic data such as ECONDE and Roadmap epigenomics projects.In addition, we also verified that our model has better mobility than similar models on the epigenetic data of mice.

# ACKNOWLEDGMENT

This work was supported by National Key R&D Program of China 2017YFB0202602, 2018YFC0910405, 2017YFC1311003, 2016YFC1302500, 2016YFB0200400, 2017YFB0202104; NSFC Grants U19A2067, 61772543, U1435222, 61625202, 61272056; The Funds of Peng Cheng Lab, State Key Laboratory of Chemo/Biosensing and Chemometrics; the Fundamental Research Funds for the Central Universities, and Guangdong Provincial Department of Science and Technology under grant No. 2016B090918122.

# REFERENCES

[1] E. P. Consortium, "An integrated encyclopedia of DNA elements in the human genome," Nature, vol. 489, no. 7414, pp. 57-74, 2012.   
[2] A. Kundaje et al., "Integrative analysis of 111 reference human epigenomes," Nature, vol. 518, no. 7539, pp. 317-330, 2015.   
[3] J. Zhou and O. G. Troyanskaya, "Predicting effects of noncoding variants with deep learning-based sequence model," Nat Methods, vol. 12, no. 10, pp. 931-4, Oct 2015.   
[4] M. Slattery, T. Zhou, L. Yang, A. C. D. Machado, R. Gordân, and R. Rohs, "Absence of a simple code: how transcription factors read the genome," Trends in biochemical sciences, vol. 39, no. 9, pp. 381-399, 2014.   
[5] D. Benveniste, H.-J. Sonntag, G. Sanguinetti, and D. Sproul, "Transcription factor binding predicts histone modifications in human cell lines," Proceedings of the National Academy of Sciences, vol. 111, no. 37, pp. 13367-13372, 2014.   
[6] E. C. Strauss and S. H. Orkin, "In vivo protein-DNA interactions at hypersensitive site 3 of the human beta-globin locus control region," Proceedings of the National Academy of Sciences, vol. 89, no. 13, pp. 5809-5813, 1992.   
[7] A. Galicia, R. Talavera-Llames, A. Troncoso, I. Koprinska, and F. Martínez-Álvarez, "Multi-step forecasting for big data time series based on ensemble learning," Knowledge-Based Systems, vol. 163, pp. 830-841, 2019.   
[8] A. Vaswani et al., "Attention is all you need," in Advances in neural information processing systems, 2017, pp. 5998-6008.   
[9] R. Cowper-Sal et al., "Breast cancer risk–associated SNPs modulate the affinity of chromatin for FOXA1 and alter gene expression," Nature genetics, vol. 44, no. 11, pp. 1191-1198, 2012.   
[10] T. Filippini et al., "Association between outdoor air pollution and childhood leukemia: a systematic review and dose–response metaanalysis," Environmental health perspectives, vol. 127, no. 4, p. 046002, 2019.   
[11] M. N. Weedon et al., "Recessive mutations in a distal PTF1A enhancer cause isolated pancreatic agenesis," Nature genetics, vol. 46, no. 1, pp. 61-64, 2014.   
[12] A. G. Waks and E. P. Winer, "Breast cancer treatment: a review," Jama, vol. 321, no. 3, pp. 288-300, 2019.   
[13] S. H. Lai, G. Zervoudakis, J. Chou, M. E. Gurney, and K. M. Quesnelle, "PDE4 subtypes in cancer," Oncogene, pp. 1-12, 2020.   
[14] C. Y. Chia et al., "GATA6 cooperates with EOMES/SMAD2/3 to deploy the gene regulatory network governing human definitive endoderm and pancreas formation," Stem cell reports, vol. 12, no. 1, pp. 57-70, 2019.   
[15] C. Liu et al., "An ATAC-seq atlas of chromatin accessibility in mouse tissues," Scientific data, vol. 6, no. 1, pp. 1-10, 2019.