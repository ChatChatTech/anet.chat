# OpenSesame: Unlocking Smart Phone through Handshaking Biometrics

Yi Guo∗, Lei Yang†, Xuan Ding‡, Jinsong Han†, Yunhao Liu‡

∗ CSE, Hong Kong University of Science and Technology, Hong Kong

† CS, Xi’an Jiaotong University, Xi’an, China

‡ School of Software, TNLIST, Tsinghua University, Beijing, China

Abstract—Screen locking/unlocking is important for modern smart phones to avoid the unintentional operations and secure the personal stuff. Once the phone is locked, the user should take a specific action or provide some secret information to unlock the phone. Existing approaches do not support smart phones well due to the deficiency of security, high cost, and poor usability. We collect 200 users’ handshaking actions with their smart phones and discover an appealing observation: the shaking pattern of a person is kind of unique, stable and distinguishable. In this paper, we propose OpenSesame, which employs the users’ shaking patterns for locking/unlocking. The key feature of our system lies in using four fine-grained and statistic features of handshaking to verify users. Moreover, we utilize support vector machine (SVM) for accurate classification. Results from comprehensive experiments show that our technique is robust compatible across different brands of smart phones, without the need of any specialized hardware.

Index Terms—Smart Phone, Security, Privacy, Authentication, Accelerameter

# I. INTRODUCTION

Nowadays, mobile phones are becoming prevalent with many powerful functions, such as sending/receiving e-mails, shopping, mobile payment, etc. Screen locker is a fundamental utility for smart phones to prevent the device from unauthorized use and to protect the privacy of users [1]–[3]. Existing approaches can be categorized into three groups: password [4], graphic pattern and physiological biometrics [5], [6]. Passwords and graphic patterns are of low security level, uneasy to remember, and inconvenient to input. Besides, physiological biometrics, such as fingerprint, needs extra component to be intergraded into the smart phone, which is costly to ordinary smart phones.

We observe that when different persons shake their smart phones, they present distinct features. The shaking speed, frequency, range and the way of wrist twisting are of great difference from person to person. These distinctions can reflect user’s physical features and habits, as long as their gender, age, occupation, etc. On the other hand, we also notice that when a person shakes his smart phone, he always shakes in a similar way. This is because, without intentional changes, a specific person tends to follow his habits once the habits are developed.

Based on above observations, we propose a handshaking biometric-based approach, called OpenSesame, to unlock the smart phone. Comparing with the existing methods, there are two major advantages of our approach. The first advantage is the difficulty to forge. Using our approach, the authentication process is based on the features of the user’s habits and motions, which is much harder for unauthorized users to obtain. Even if the unauthorized user occasionally peeks at the user’s shaking action, it is still difficult to simulate since there are still many distinct but invisible differences of shaking actions. For example, users have different strength when shaking or twisting. The second advantage is the simplicity and convenience. Our approach can free users from remembering a large number of passwords or complicated patterns for unlocking their phones. All the user needs to do is just naturally shake the phone for 1 or 2 seconds.

However, it is challenging to mine the unique patterns from the user’s handshaking action. First, we should choose appropriate sensors to monitor the user’s shaking action. The sensor should be in low cost, widely deployed, and energy-efficient. After careful comparison, we use the 3-axis accelerometer. Second, the main difficulty is to extract stable but unique features from the user’s shaking action. We project the collected shaking data into A-Space and then utilize four shaking functions for feature extraction.

The remainder of the paper is structured as follows. We characterize the handshaking with a large number of real users’ trace in Section II. The system design is presented in Section III and the experiment results are evaluated in Section IV. We introduce the related work in Section V. Finally, Section VI concludes the paper.

# II. SHAKING CHARACTERIZATION

In this section, we introduce the sensor used for shaking sensing, real trace collection, and analysis on the data.

# A. Shaking Sensing

For precisely characterizing user’s shaking actions, selecting appropriate sensors is necessary. As the tremendous growth of MEMS technology, there are many powerful sensors equipped in our smart phone today, such as camera, microphone, proximity sensor, accelerometer, gyroscope, and magnetic sensor etc. In our system, the selected sensor should be able to depict the handshaking. In addition, it should be energy-efficient, stable, cheap, and compatible for wide deployment in most kinds of smart phones.

In our approach, we finally select the 3-axis accelerometer as our feature detecting sensor. The accelerometer allows smart phones to detect the motion performed on them. The accelerometer in smart phones measures the acceleration of the phone relative to freefall. The accelerometer measures the acceleration of the phone in three different axes: X, Y, and Z. Examples of the collected data are shown in Figure 1.

# B. Data Collection

For investigating the uniqueness of handshaking, we collect the shaking action data from 200 distinct smart phone users. For each specific user, he is asked to shake the smart phone for more than 10 seconds and repeat for three times. Note that there is no special restriction on user’s shaking actions. He can shake the smart phone arbitrarily in each trail. Indeed, we aim at taking insight into the handshaking action but not the motion pattern. The data is collected in fast sampling mode. In the fast sampling mode, the accelerometer samples every 10 to 20 milliseconds, corresponding to the acceleration value change rate.

All the raw shaking action are recorded as a sequence of tuples represented as $\left( x _ { t } , ~ y _ { t } , ~ z _ { t } \right)$ , where x, $y , z$ donate the acceleration along the x-axis, y-axis and z-axis respectively, and t donates the time. As a result, we totally collect 600 files containing 389, 373 raw tuples.

# C. Shaking Measurement

To show the uniqueness of handshaking in intuition, we display four users’ traces in Figure 1. The traces are illustrated in a 3-D acceleration space, short for A-Space, where the raw tuple $\left( x _ { t } , ~ y _ { t } , ~ z _ { t } \right)$ are connected in time order. Both the Figure 1(a) and Figure 1(b) are generated from two trails of a volunteer. We can see that the two shapes are very similar. The last three figures come from three distinct persons. Figure 1(c) is plot as a circle, Figure 1(d) resembles a river, while the shape in Figure 1(e) is in the shape of crescent. From these figures, we can observe that the handshaking biometrics are unique for a certain user. A given user presents very simple shape results on different trails. Moreover, different users have clearly different results.

The challenge here is how to measure the handshaking represented in A-Space. We should transform the A-Space representation into a parameterized and comparable feature vector. For this purpose, we define the shaking function to measure the global geometric properties of the shaking shapes, which is formally given by:

$$
f = S \left(\bigcup (x _ {t}, y _ {t}, z _ {t})\right)
$$

The function considers the raw shaking tuples $\cup ( x _ { t } , y _ { t } , z _ { t } )$ as input and outputs a feature vector $f . \mathrm { A }$ good shaking function should have the following properties:

Efficiency: Since shape function will be performed in the smart phone, it should be simple enough to be fast and efficiently function.   
• Invariance: In most time, the smart phone is working in mobile environments. The shaking function should be insensitive to the position or direction change of smart phones.   
Robustness: Although the shaking data generated by one person is similar, there always exist many noises and the sampling time is variable. Hence, the shaking function

should be robust to noise, blur, cracks, and dust in the shaking.

For meeting above four requirements, we propose four shaking functions, $S _ { 1 } , S _ { 2 } , S _ { 3 } , \bar { S _ { 4 } }$ , as follows:

$\mathbf { S _ { 1 } }$ : The centroid C is computed first and then two random points A and B in the A-Space are chosen. The angle $\angle A C B$ among these three points are measured. The selection of random points is repeated for N times. At a result, N angles output and the corresponding PDF of these angles is reproted.   
· $\mathbf { S _ { 2 } }$ : This shaking function is similar to the $S _ { 1 }$ . The difference is that all of these three points are randomly selected. One angle among the three angles formed by these three points is recorded. As the result, the corresponding PDF of these angles is given.   
· $\mathbf { S _ { 3 } } \mathbf { : }$ : While both $S _ { 1 }$ and $S _ { 2 }$ concentrate on the angle parameter, the other two shaking functions, $S _ { 3 }$ and $S _ { 4 } ,$ focus on the distances among the points. $S _ { 3 }$ randomly selects N points and calculates the Euclidean distance between the centroid and these N selected points. Finally, the corresponding PDF of distances is calculated.   
· $\mathbf { S } _ { 4 } \mathbf { : }$ Randomly selects N pair of points and calculates their Euclidean distance. The PDF of these distances is the output.

The results of above four shaking functions are demonstrated in Figure 2, with the input of four users’ shaking data shown in Figure 1. From the figures, we can see that all four shaking functions behave well. These four shaking functions are chosen mostly for their simplicity and invariance. In particular, they are fast to compute, easy to understand, and simple to produce distributions. Despite their simplicity, we find these general purpose shaking functions tare fairly distinguishable. They are robust because the probability that noises are selected is very low and hence their performance will not be affected. Third, these four functions are invariant to rotation and scaling because both the angle and distance is irrelevant to directions and positions of shaking.

# D. Shaking Matching

Keeping in mind that our goal is to determine whether the screen should be unlocked according to a given shaking action and the pre-defined one. We formalize the similarity of two shaking actions by means of the distance between their PDFs. We define the distance between two PDFs as follows. The whole range of PDF is divided into discrete intervals, and the average value is calculated regarding to each interval. Assume two PDFs, the first is described as vector $f _ { 1 } ~ = ~ [ p _ { 1 } , p _ { 2 } , \cdot \cdot \cdot , p _ { n } ]$ , where $p _ { i }$ denotes the probability of falling into the $i ^ { t h }$ interval. The second is expressed similarly as $f _ { 2 } = [ q _ { 1 } , q _ { 2 } , \cdots , q _ { n } ]$ . The distance between the two PDFs is the accumulated as follows:

$$
D (f _ {1}, f _ {2}) = \sum_ {i = 1} ^ {n} | p _ {i} - q _ {i} |
$$

In Section IV, we can see that the self-similarity always maintains an acceptable value and is fully distinguishable from other users’ features.

![](images/e197146bc570d14765d14a7ed49d9e2bf9ee9b39cf83d280daf1a88d021be31e.jpg)



(a) User 1(Test 1)

![](images/72d6ff66fb7917c3623e3d8f1963fc99e51350b17a39a9851d6d2d15ffaaaad9.jpg)



(b) User 1(Test 2)

![](images/29569146509d59b6e71ce2476d06d1a1299bfcb0eb2b14ac5beb9b9f92a5942c.jpg)



(c) User 2

![](images/bbf6c3523e0f03f0f3c6b87e3bad51778e2e61165cd73431cd8495d62f2614b6.jpg)



(d) User 3

![](images/d81de723114626ed241107baae7b6833ff5f22bd164d2fa625384398e41809c2.jpg)  
(e) User 4

Fig. 1. 3-D Acceleration Space   
![](images/8aaaf4634c0f5f0350c1ad43205b25fcb64b830f466878c3a0ac650efac3c950.jpg)



(a) S1

![](images/48a6cc9929ba7b1957c65f19ed83fb11b0fcf192d7d03d2c75dbd2d92ee38571.jpg)



(b) S2

![](images/1c0f3e0a89182502a10c974500fba7bcf2507bc8460a8690deb0d2e8b451b204.jpg)



(c) S3

![](images/616db4d8ef41075489f430d9bb349b304e528a0ec5c31fca8f012aaf8b4828aa.jpg)



(d) S4   
Fig. 2. Probability Density Functions with Variant Shaking Functions

# III. OPENSESAME

In this section, we present our unlocking method for smart phone called OpenSesame.

# A. Overview

OpenSesame consists of four components: sensing, fetcher, classifier, and matcher.

• Sensing: This component is straightforward used to record the user’s handshaking action data.   
Fetcher: The raw tuples is feeded into fetcher component in which four shaking functions are applied to fetch the shaking features.   
Classifier: To discriminate the authorized users and unauthorized users, the Support Vector Machine (SVM) is employed in our system for classification.   
• Matcher: In the last component, the extracted feature is used to determine whether it matches the pre-defined one.

# B. Fetcher

According to Section II-C, the field set of the acceleration points can be treated as one single input of shaking function, and the shaking function can be applied to this input to generate the feature vector. However, using the field set as an input has two shortcomings. First, the amount of acceleration points in a field set is large, usually more than 1000. In order to generate a representative feature vector PDF for the shaking action data, an extremely large number of feature vectors are required. In this way, the system overhead is high and affects the normal operation of the smart phone. Second, to unlock the smart phone, the user is required to shake his smart phone for a period to generate same amount of shaking data. However, it is inconvenient to ask the user to shake the smart phone for such a long time period to generate more than 1000 acceleration points for each time he wants to unlock his phone. Therefore, the amount of acceleration points selected as an input needs to be reduced.

According to our observation, the shaking action of user always shows the property of repeating. In fact, the input shaking action can be regarded as a series of small repeating shaking actions which are very similar. Therefore, we can select a continuous sequence of acceleration points with a reasonable amount as an input to the shaking function. Feature vectors can be generated from these small inputs with low data loss.

We generate the feature vectors as follows: we first select a window with size w, where w is much smaller than the size of the field set of data. From the field set of data, we select an acceleration point $P _ { k }$ and form the input with the subsequence of w continuous acceleration points $\{ P _ { k } , P _ { k + 1 } , P _ { k + 2 } , . . . , P _ { k + w - 1 } \}$ . Then we apply the shaking function on this input and deliver the PDF of the feature vectors to describe the feature of the shaking action.

# C. Classifier

The feature classifier is designed to generate a standard to discriminate authorizeds user and unauthorized users with the feature vectors of the input shaking action data. In OpenSesame, the support vector machine, SVM for short, is selected as the classifier. The SVM classifier is used to classify a group of linear-inseparable training tuples into two classes. Training tuples for SVM input is donated as $\{ \mathbf { v } , y \}$ , where v is the attribute vector used to describe the attributes of the training tuple, and y is the label of the training tuple, which represents the actual class it belongs to. The basic idea of SVM is to transform these attribute vectors of training tuples into a higher dimensional space to make the training tuples linear-separable. Then the training tuples can be separated into two classes by a hyperplane. The SVM classifier classifies the training tuples based on this hyperplane, attempting to classify training tuples with same label into same class. Then a classification model is generated to describe the classification standard of a given tuple. Inputting an unclassified tuple into the SVM classifier using the generated classification model, the tuple can be predicted which class it most probably belongs to.

In OpenSesame, the label of the training tuple is either +1 or 1. When $y = + 1$ , the tuple is generated from the class of unauthorized users. On the contrary, $y = - 1$ means the tuple belongs to the authorized user’s class. The attribute vector v is generated from the PDF of the feature vector we gain from Section III-B. The attribute vector can be represented as $[ a _ { 1 } , a _ { 2 } , . . . , a _ { n } ] ^ { T }$ . Here, $a _ { i }$ is $i ^ { t h }$ property of the training tuple, which represents the $i ^ { t h }$ value in the feature vector PDF. By injecting enough amount of training tuples into the SVM classifier, a classification model can be achieve to verify the authentication data of user.

# D. Matcher

The matcher component is performed when the user activates the authentication interface of OpenSesame and wants to unlock the smart phone. The user shakes the smart phone for a short time period, say 1 or 2 seconds, to input his shaking action as the authentication data. Feature vectors of the input shaking action is generated and acceleration point sequence $\{ P _ { 1 } , P _ { 2 } , . . . , P _ { w } \}$ is recorded, where w is the window size in fetcher component. Applying the same shaking function to this sequence, we can generating the predict tuple with attribute vector $[ a _ { 1 } , a _ { 2 } , . . . , a _ { n } ] ^ { T }$ . By inputting this predict tuple into the SVM classifier with the classification model we delivered in classifier component, the SVM classifier decides which class the input tuple most likely belongs to. When the input tuple is classified into the authorized user set, the authentication is successfully done and the smart phone is unlocked. Otherwise, the smart phone requires another authentication try.

# IV. IMPLEMENTATION AND EVALUATION

In this section, we present the implementation of OpenSesame and evaluate its performance.

# A. Implementation App

We implement OpenSesame in Android-based smart phones. The version of Android system is 2.3.3. the app is developed with Android-SDK using Java SE. We use the open source library tool, LIBSVM [7], to perform the classification of SVM. LIBSVM is an integrated software for support vector classification. The version we used is LIBSVM-3.12. During our experiments, we use the default kernel function (Gaussian Radial Basis Function) and find the best setting of parameters Cost and $\gamma$ for the kernel function via the cross-validation when generating the training model.

# B. Metrics

We evaluate OpenSesame in terms of the authentication accuracy. The authentication accuracy is measured via the following metrics:

• False Negative Rate (FNR): The probability that an authorized user is treated as an unauthorized user.   
True Positive Rate (TPR): The probability that an authorized user is successfully verified.   
• False Positive Rate (FPR): The probability that an unauthorized user is treated as an authorized user.

![](images/9d205e71bbf913ca1656bebf594bc34287c4af6bf78e56a8df14e538938df989.jpg)



(a) False Negative Rate

![](images/2240e2a105daadf68e8bdbc44820b606e1c2bf730645e85e9bca09785e43167a.jpg)



(b) False Positive Rate   
Fig. 3. Impact of shaking functions

Note that FNR and TPR are related to the convenience of users when they use our system, where the authorized user can successfully unlock the smart phone by a single try. The FPR reflects the security of the OpenSesame, where the unauthorized user should be denied to unlock the smart phone.

# C. Experiment Setup

The data for experiments are collected in controllable environments where the users’ names are recorded. Overall, 389,373 raw tuples are captured from 200 distinct users, with an average 1,947 raw tuples per user. Each user performs the handshaking for three trails while each trail persists 10 20 seconds. For each user, the training data will be extracted from the first two trails, while the testing data will be retrieved from the last one. Therefore, there is no overlap between the training data and testing data. The classification is based on self and non-self discrimination. For a given user, the training data is composed of negative samples belonging to this user, and an equal number of positive ones from others.

# D. Impact of Shaking Functions

There are four shaking functions to parameterize the A-Space representation of handshaking. In this experiment, we select 30 users’ handshaking and maintains the window size as 50 tuples. Figure 3 plots the FNR and FPR for the four shaking functions. From the Figure 3(a), we observe that the average FNR using $S _ { 1 }$ and $S _ { 2 }$ are around 20% while the values are below 10% using $S _ { 3 }$ and $S _ { 4 } .$ . The similar observation is obtained on FPR, as shown in Figure 3(b). This shows that the distance-based shaking functions perform better than the angle-based ones. We further focus on the distance-based shaking functions. $S _ { 3 }$ and $S _ { 4 }$ have close FNRs and FPRs. However, the variance of $S _ { 4 }$ is smaller than that of $S _ { 3 }$ , which means $S _ { 4 }$ is more stable than $S _ { 3 }$ .

# E. Robustness

As mentioned before, our approach should be insensitive to the user’s motions because the smart phone is mainly used in mobile environment. In this experiment, we test the relationship between the speed of user’s motions and the accuracy. Five user’s motions are considered: stationary, walking slow, walking fast, running, and taking a vehicle. The result is shown in Figure 4. From the figure, we can see that as the speed growing from 0 m/s to 5 m/s, the FNR is steady around 11%, with a standard deviation of 2.0%. This indicates that the motion of users makes a very limited effect on our approach. Besides, the FPR is also invariant when the speed of user’s motion increases, which is around 15% with a standard deviation of 2.5%.

![](images/804348c673ef35f762492e0a126894676736cc896ad63ca8f546a05366fcd969.jpg)



Fig. 4. User’s motion

![](images/f9039ebd38879f325d5a14ccee9ae76a3f409d06a18f7b7c4d8c9024127e7b36.jpg)



Fig. 5. Phone’s orientation   
![](images/7f265f63a1101814a9dd9b854cfd2b8afe7a1068cb8960b2b7db4ce2c6775389.jpg)



Fig. 6. Distances

Although the shaking habit may be similar for an identical user, the postures of users when shaking the smart phone can change the orientation of the phone. In this section, we evaluate OpenSesame with variant phone’s postures. In this experiment, three user’s postures are tested: standing, lying on the back, and lying on the side. We conduct one trail in standing posture and store the corresponding result feature vector in our smart phone. Then we attempt to unlock the smart phone in the three postures. Each posture is repeated 30 trails and the CDF of accuracy is displayed in Figure 5. From this figure, 20% of lying-on-the-back posture and lyingon-the-side posture have accurate rate lower than 86% and 76%, respectively. Meanwhile, 20% lying-on-the-back posture and 45% lying-on-the-side posture have their accurate rates higher than 90%. This experiment fully demonstrates that our approach is phone-orientation-insensitive.

# F. Discrimination

In this section, we consider the OpenSesame’s capability of discrimination among different users. One user’s trace is selected and his similarity compared to other user is calculated. The result is shown in Figure 6. From the figure, we can see that self-similarity is approximately bounded under 0.3, and 90% of the distances are lower than 0.25. Being different with the self-similarity, the distance between the given user and others is obvious. Only 8% of the distances are lower than 0.2, and about 20% of the distances are larger than 1.0. Hence, the discrimination of distinct users and recognition of identical users can be achieved.

# V. RELATED WORK

Two major types of authentication methods are implemented on smart phones: knowledge-based authentication methods [8] (like PINs and graphical passwords) and biometric-based authentication methods [5], [6] (like fingerprint). Unlike the knowledge-based authentication, biometric-based authentication has the advantage of inimitability, which raises its security level. Moreover, biometric-based authentication does not need to remember a large amount of passwordsp, which provides more convenience [3].

Biometric-based approaches are classified as physiological and behavioral methods [5]. Physiological methods [9] employ the user’s unique physical characteristics as the authentication data. However, large memory usage, high processing latency, and external device requirement make these kinds of authentication approaches unrealistic to be widely deployed on smart phones. Behavioral methods use the patterns of user’s behavior as authentication data. When a user takes actions on the smart phone, like typing, the smart phone can detect the behavior and verify such behaviors to prestored data. Keystroke-based authentication [10] verifies the authorized user by analyzing the typing characteristics of the user. However, the performance of this method is strongly relying on the type of keyboards, especially for those smart phones with touch screens which can display the soft keyboard as the user wishes.

# VI. CONCLUSION

In this paper, we propose a novel behavioral biometricbased authentication approach called OpenSesame for smart phone. We design four shaking functions to fetch the unique pattern of user’s handshaking actions. By applying the SVM classifier, the smart phone can accurately verify the authorized user with the pattern of handshaking action. Experiment results based on 200 distinct users’ handshaking actions show that the OpenSesame reaches high level of security and robustness, and achieves good user’s experience.

# VII. ACKNOWLEDGEMENT

This work is supported in part by the National Basic Research Program of China (973) under grant No. 2011CB302705, NSFC under Project No. 61033015, the Fundamental Research Funds for the Central Universities of China, and NSFC Major Program under grant No. 61190110.

# REFERENCES

[1] A. D. Luca, A. Hang, F. Brudy, C. Lindner, and H. Hussmann, “Touch me once and i know it’s you!: implicit authentication based on touch screen patterns,” in Proc. of ACM CHI, 2012.   
[2] H. Park, J. W. Hong, J. H. Park, J. Zhan, and D. Lee, “Combined authentication-based multilevel access control in mobile application for dailylife service,” IEEE Transactions on Mobile Computing, 2010.   
[3] N. Ben-Asher, N. Kirschnick, H. Sieger, J. Meyer, A. Ben-Oved, and S. Moller, “On the need for different security methods on mobile phones,” in Proc. of ACM MobileHCI, 2011.   
[4] S. Chiasson, P. Oorschot, and R. Biddle, “A usability study and critique of two password managers,” in Proc. of USENIX Security Symposium, 2006.   
[5] R. V. Yampolskiy and V. Govindaraju, “Behavioural biometrics: a survey and classification,” Biometrics, 2008.   
[6] N. Zheng, A. Paloski, and H. Wang, “An efficient user veritification system via mouse movements,” in Proc. of ACM CCS, 2011.   
[7] C. Chang and C. Lin, “LIBSVM : a library for support vector machines,” ACM Transactions on Intelligent Systems and Technology, 2011.   
[8] N. L. Clarke and S. M. Furnell, “Authentication of users on mobile telephones: a survey of attitudes and practices,” Computers & Security, 2005.   
[9] W. Zhao, R. Chellappa, P. J. Phillips, and A. Rosenfeld, “Face recognition: a literature survey,” ACM Comput. Surv., 2003.   
[10] N. L. Clarke and S. M. Furnell, “Authenticating mobile phone users using keystroke analysis,” International Journal of Information Security, 2007.