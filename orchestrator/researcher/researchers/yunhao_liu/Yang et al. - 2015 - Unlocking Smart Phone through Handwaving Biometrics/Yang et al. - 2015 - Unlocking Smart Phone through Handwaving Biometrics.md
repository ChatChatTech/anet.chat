# OpenSesame: Unlocking Smart Phone through Handwaving Biometrics

Lei Yang, Member, IEEE, Yi Guo, Member, IEEE, Xuan Ding, Member, IEEE, Silun Wang Jinsong Han, Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—Screen locking/unlocking is important for modern smart phones to avoid the unintentional operations and secure the personal stuff. Once the phone is locked, the user should take a specific action or provide some secret information to unlock the phone. The existing unlocking approaches can be categorized into four groups: motion, password, pattern, and fingerprint. Existing approaches do not support smart phones well due to the deficiency of security, high cost, and poor usability. We collect 200 users’ handwaving actions with their smart phones and discover an appealing observation: the waving pattern of a person is kind of unique, stable and distinguishable. In this paper, we propose OpenSesame, which employs the users’ waving patterns for locking/unlocking. The key feature of our system lies in using four fine-grained and statistic features of handwaving to verify users. Moreover, we utilize support vector machine (SVM) for accurate and fast classification. Our technique is robust compatible across different brands of smart phones, without the need of any specialized hardware. Results from comprehensive experiments show that the mean false positive rate of OpenSesame is around 15%, while the false negative rate is lower than 8%.

Index Terms—Smart Phone, Security, Privacy, Authentication, Accelerometer

# 1 INTRODUCTION

Nowadays, smart phones are no longer the devices that are only used to call or text others. They become prevalent with much more powerful functions. Acting as pocket PCs, smart phones can be used to deal with complicated tasks such as sending/receiving e-mails, shopping, mobile payment, etc.. Screen locker is a fundamental utility for smart phones to prevent the device from unauthorized use. For example, the Apple iPhones and Android phones can lock themselves automatically after being idle for a short time. It can protect the privacy of users as well as prevent unintentional operations.

Classical screen lockers have been proposed long time back. (1) The most widely used one is Slide-to-Unlock. The user can unlock his/her phone through sliding his finger across a defined trajectory. This method is too simple to protect user’s privacy. (2) PIN, the most common method used by traditional digital device, is always adopted on smart phones for unlocking smart phones. However, due to the relatively small screen and frequent unlocking request, it is inconvenient to set long and complex PIN on phones. For example, there are only four numbers allowed to be set as unlocking PIN in iPhone’s default setting. Such a short and simple PIN can often be easily guessed [1], [2]. (3) The user can pre-define a graphical password, like connecting at least 4 circles shown in the screen. Being similar to the PIN, simple graphic passwords are easy to be peeked and guessed, while the complex pattern may confuse the user and make inconvenience.

To enhance the security as well as the flexibility, many biometric authentication methods [3], [4] are introduced for screen lockers. The secrets of these methods cannot be easily spied and reproduced since they identify the user based on her natural features. The biometric measures are grouped into two main categories [5]: physiological biometrics and behavior biometrics.

Physiological biometrics leverage the physiological features of human beings to identify the user, including recognitions of face [6], voice [7], fingerprint [8], ear [6], and so on. However, we find that (i) performances of these solutions are heavily influenced by external factors. For example, the face acquirement by the camera is severely affected by the illumination, resulting in the failure to identify user at night. Similarly, it is hard to distinguish the the voice from the ambient interference in an extremely noisy environments, like subway or restaurant. Any authentication method must be adapted to all kinds of conditions. (ii) Unlocking operation is a very frequent operation, of which energy consumption should be carefully considered. It is well known that the camera is one of notorious energy killers [9] in smart phones. (iii) lack of required hardware on current mainstream smartphones, like fingerprint scanner.

The behavior biometrics is the other classification of biometric measure, which identify the user based on their behavior features, such as gesture [10], [11], typing behavior [6], [12], mouse movement [13], tapping behavior [14], or gait [15], However, these methods cannot either be adopted in smart phones or be suitable for unlocking smartphones. For example, in order to recognize the gait pattern, the user has to walk first or the smart phone to figure out whether he/she is valid [15]. It appears odd and inconvenient for users to perform the behavior as answering a phone call for the purpose of checking his/her emails [11]. (More discussions compared with these works are presented in Section 5).

In this paper, we observe that different users wave their smart phones produce distinct features. For example, some persons used to wave their smart phones drastically while some others like to wave in a gentle way. This makes the waving speed and frequency totally different among users. Also, the waving range and the way of wrist twisting are also different from user to user. These patterns derive from user’s physical features and habits. For example, the users with longer arms wave faster and wider than those with shorter arms. Some persons are accustomed to end their waving action with a wrist twisting while some others like to begin with a wrist twisting. Moreover, the gender, age, and occupation also greatly affect the feature of waving actions. On the other hand, we also observe that when a user waves his smart phone, he always shakes in a similar way. This is because, without intentional changes, a specific person tends to follow his habits once the habits are developed.

Based on above observations, we propose a handwaving biometric-based approach, called OpenSesame, to unlock the smart phone. Comparing with the existing methods, there are two major advantages of our approach. (i) It is difficult to forge. Using our approach, the authentication process is based on the features of the user’s habits and motions, which is much harder for unauthorized users to obtain. Even if the unauthorized user occasionally peeks at the user’s waving action, it is still difficult to simulate since there are still many distinct but invisible differences of waving actions. For example, users have different strength when waving or twisting. (ii) It is the simple and convenient. Our approach can free users from remembering a large number of passwords or complicated patterns for unlocking their phones, preserved the security and All the user needs to do is just naturally wave the phone for 1 or 2 seconds.

However, it is challenging to mine the unique patterns from the user’s handwaving action. First, we should choose appropriate sensors to monitor the user’s waving action. The sensor should be in low cost, easy for wide deployment, and energy-efficient. After careful comparison, we use the 3-axis accelerometer. Second, the main difficulty is to extract stable but unique features from the user’s waving action. We project the collected waving data into A-Space and then utilize four waving functions for feature extraction. Furthermore, we employ the support vector machine (SVM) for accurate and fast classification. We develop a prototype of handwaving unlocking system, termed as OpenSesame, and implement into three mainstreaming smart phones. We collect the handwaving traces from 200 volunteers using our app. After comprehensive experiments and tests, the result demonstrates that OpenSesame can accurately verify users via their handwaving with low latency.

The remainder of the paper is structured as follows. We characterize the handwaving with a large number of real users’ trace in Section 2. The system design is presented in Section 3 and the experiment results are evaluated in Section 4. We introduce the related work in Section 5. Finally, Section 6 concludes the paper.

# 2 WAVING CHARACTERIZATION

In this section, we introduce the sensor used for waving sensing, real trace collection, and analysis on the data.

# 2.1 Waving Sensing

For precisely characterizing user’s waving actions, selecting appropriate sensors is necessary. As the tremendous growth of MEMS technology, there are many powerful sensors equipped in our smart phone today, such as camera, microphone, proximity sensor, accelerometer, gyroscope, and magnetic sensor etc. In our system, the selected sensor should be able to depict the handwaving. In addition, it should be energy-efficient, stable, cheap, and compatible for wide deployment in most kinds of smart phones. Obviously, the first three sensors cannot capture the phone’s motion. The gyroscope sensor is attractive because it is designed for measuring or maintaining purpose, based on the principles of angular momentum. Unfortunately, this kind of sensor is not a standard equipment in most smart phones due to its high price. The magnetic sensor is usually used for compass, but it tends to be interfered by the mental objects under special environment, like inside the car or subway.

In our approach, we finally select the 3-axis accelerometer as our feature detecting sensor. The accelerometer allows smart phones to detect the motion performed on them. The accelerometer in smart phones measures the acceleration of the phone relative to freefall. A value of 1 indicates that the phone is experiencing 1 g of acceleration exerting on it. 1 g of acceleration is the gravity, which the phone experiences when it is stationary. The accelerometer measures the acceleration of the phone in three different axes: X, Y, and Z. Examples of the collected data are shown in Figure 1.

# 2.2 Data Collection

For investigating the uniqueness of handwaving, we collect the waving action data from 200 distinct smart phone users. For each specific user, he is asked to shake the smart phone for more than 10 seconds and repeat for three times. Note that there is no special restriction on user’s waving actions. He can shake the smart phone arbitrarily in each trail. Indeed, we aim at taking insight into the handwaving action but not the motion pattern.

The data is collected in two sampling modes: fast and normal modes. In the fast mode, the accelerometer samples every 10 to 20 milliseconds, corresponding to the acceleration value change rate. There are 100 users’ traces collected using this mode. In the normal mode, the sampling interval is 200 milliseconds and 100 users’ traces are sampled. Clearly, using normal sampling mode of accelerometer loses some data, but saves energy. We will compare these two modes in the evaluation section.

All the raw waving action are recorded as a sequence of tuples represented as $\left( x _ { t } , y _ { t } , z _ { t } \right)$ , where x, y, z donate the acceleration along the x-axis, y-axis and z-axis respectively, and t donates the time. As a result, we totally collect 600 files containing 389, 373 raw tuples.

![](images/94510942aba11aab92c92b75b2c119f79af24fe6360d6e10abda1635d48ae265.jpg)



(a) User 1 (Test 1)

![](images/1cf72efed42f1c019c33d3cf66ebdb71afbd94f045d2a111a258f7e36037ab07.jpg)



(b) User 1 (Test 2)

![](images/a1f23bc42a1bc4eba848cf79e5d00a31aae6e5ac0d762024da409466d99d0903.jpg)



(c) User 2

![](images/6964a4302fba1214d1aa07d1ca5b6ecb036523f4c628ffd27d5cdd556d6c4868.jpg)



(d) User 3

![](images/ca6c3b4239b07b86a82bcd4d0c9c20f2ddad427568bdd6e218794e7145a86efc.jpg)  
(e) User 4

Fig. 1: 3-D Acceleration Space   
![](images/396698710dc0b8ef6c76c939042a9be56b5a955a4b4db7fe65b60f6d96c2e5fa.jpg)



(a) S1

![](images/9282feae7e7000791fcac01ae419b8bbc08d9b99daa6a0b026637337b2bc861c.jpg)



(b) S2

![](images/5b50d532b4aa52d19f47adf1e06c7eb64f71cf958dc59c81e0336012089091fa.jpg)



(c) S3

![](images/cb30d60a2eccfe39d8c3e251f7373a4a1b2c53a24b5faa2684bba4787201c6ed.jpg)



(d) S4   
Fig. 2: Probability Density Functions with Variant Waving Functions

# 2.3 Waving Measurement

To show the uniqueness of handwaving in intuition, we display four users’ traces in Figure 1. The traces are illustrated in a 3-D acceleration space, short for A-Space, where the raw tuple $\left( x _ { t } , \ y _ { t } , \ z _ { t } \right)$ are connected in time order. Both the Figure 1(a) and Figure 1(b) are generated from two trails of a volunteer. We can see that the two shapes are very similar. The last three figures come from three distinct persons. Figure 1(c) is plot as a circle, Figure 1(d) resembles a river, while the shape in Figure 1(e) is in the shape of crescent. From these figures, we can observe that the handwaving biometrics are unique for a certain user. A given user presents very simple shape results on different trails. Moreover, different users have clearly different results.

The challenge here is how to measure the handwaving represented in A-Space. We should transform the A-Space representation into a parameterized and comparable feature vector. For this purpose, we define the waving function to measure the global geometric properties of the waving shapes, which is formally given by:

$$
f = S (\mathcal {A}) \tag {1}
$$

where ${ \mathcal { A } } = \{ ( x _ { t _ { 0 } } , y _ { t _ { 0 } } , z _ { t _ { 0 } } ) , ( x _ { t _ { 1 } } , y _ { t _ { 1 } } , z _ { t _ { 1 } } ) \cdot \cdot \cdot , ( x _ { t _ { n } } , y _ { t _ { n } } , z _ { t _ { n } } ) \}$ . A is a set of raw waving tuples collected during $t _ { 0 }$ and $t _ { n }$ . The waving function considers A as input and outputs a feature vector f. A good waving function should have the following properties:

• Efficiency: Since shape function will be performed in the smart phone, it should be simple enough to be fast and efficiently function.   
• Invariance: In most time, the smart phone is working in mobile environments. The waving function should be insensitive to the position or direction change of smart phones.

• Robustness: Although the waving data generated by one person is similar, there always exist many noises and the sampling time is variable. Hence, the waving function should be robust to noise, blur, cracks, and dust in the waving.

For meeting above four requirements, we propose four waving functions, $S _ { 1 } , S _ { 2 } , S _ { 3 } , S _ { 4 }$ , as follows:

• $\mathbf { S _ { 1 } }$ : The centroid C is computed first and then two random points A and B in the A-Space are chosen. The angle $\angle A C B$ among these three points are measured. The selection of random points is repeated for N times. At a result, N angles output and the corresponding PDF of these angles is reported as the feature vector.   
• $\mathbf { S _ { 2 } } \colon$ This waving function is similar to the $S _ { 1 }$ . The difference is that all of these three points are randomly selected. One angle among the three angles formed by these three points is recorded. As the result, the corresponding PDF of these angles is given for the feature vector.   
• S3: While both $S _ { 1 }$ and $S _ { 2 }$ concentrate on the angle parameter, the other two waving functions, $S _ { 3 }$ and $S _ { 4 }$ , focus on the distances among the points. $S _ { 3 }$ randomly selects N points and calculates the Euclidean distance between the centroid and these N selected points. Finally, the corresponding PDF of distances is calculated as the feature vector.   
• $\mathbf { S } _ { 4 } \colon$ Randomly selects N pair of points and calculates their Euclidean distance. The PDF of these distances is the feature vector.

The results of above four waving functions are demonstrated in Figure 2, with the input of four users’ waving data shown in Figure 1. From the figures, we can see that all four waving functions behave well. These four waving functions are chosen mostly for their simplicity and invariance. In particular, they are fast to compute, easy to understand, and simple to produce distributions. Despite their simplicity, we find these general purpose waving functions tare fairly distinguishable. They are robust because the probability that noises are selected is very low and hence their performance will not be affected. Third, these four functions are invariant to rotation and scaling because both the angle and distance is irrelevant to directions and positions of waving.

# 2.4 Waving Matching

Keeping in mind that our goal is to determine whether the screen should be unlocked according to a given waving action and the pre-defined one. We formalize the similarity of two waving actions by means of the distance between their feature vectors. Since the feature vectors are PDF of distributions, we divide the whole range of PDF into discrete bins and the average value is calculated regarding to each bin. As a result, the discretized PDF, $f = [ p _ { 1 } , p _ { 2 } , \cdot \cdot \cdot , p _ { n } ] .$ , is considered the feature vector where $p _ { i }$ denotes the probability of falling into the $i ^ { t h }$ bin.

Definition 1 (Similarity): Given two arbitrary feature vectors, $f _ { 1 } = [ p _ { 1 } , p _ { 2 } , \cdots , p _ { n } ]$ , and $f _ { 2 } = [ q _ { 1 } , q _ { 2 } , \cdots , q _ { n } ]$ , their similarity is defined as

$$
D (f _ {1}, f _ {2}) = \sum_ {i = 1} ^ {n} | p _ {i} - q _ {i} |
$$

where $D ( f _ { 1 } , f _ { 2 } ) \in [ 0 , 2 ]$ . The smaller similarity means two features are very close and vice versa.

We select 6 users randomly and each user conducts 3 trails. The waving function $S _ { 4 }$ is employed here to measure the handwaving. As a result, there are $3 \times 6 = 1 8$ features after using by $S _ { 4 }$ . Their similarity are plotted as a visualized similarity matrix in Figure 3. In the matrix, the darkness of each elements $( i , j )$ is proportional to the magnitude of the computed similarity between the $i ^ { t h }$ and $j ^ { t h }$ features. Darker elements represent better matches, while lighter elements indicate worse matches. The matrix is symmetric.

Definition 2 (Self-similarity): The self-similarity is the distance of two feature vectors extracted from two hand waving generated by a same user. Especially, if the two features come from a same waving instance, they are equal and their similarity equal zero.

Obviously, the elements lying in the diagonal line are the darkest because their distances equal 0. For each user, there are $3 \times 3 = 9$ elements for self-similarity measurement. From the figure, we can see that the self-similarity always maintains an acceptable darkness and is fully distinguishable from other users’ features.

# 3 OPENSESAME

In this section, we present our unlocking method for smart phone called OpenSesame.

![](images/2147b089260876484720c7568b2aec74a9a6d71f2f677bf46f4bd90b73e6f00c.jpg)



Fig. 3: Similarity Matrix for 6 distinct users with 3 trails

# 3.1 Overview

OpenSesame consists of four components: sensing, filter, fetcher, classifier, and matcher.

• Sensing: This component is straightforward used to record the user’s handwaving action data.   
• Filter: In practice, we find that there always exist some silent periods when no waving or very low level sensing data is detected. For better feature extraction, we use filter component to wipe out the silent periods.   
• Fetcher: The filtered raw tuples is feeded into fetcher component in which four waving functions are applied to fetch the waving features.   
• Classifier: To discriminate the authorized users and unauthorized users, the Support Vector Machine (SVM) is employed in our system for classification.   
• Matcher: In the last component, the extracted feature is used to determine whether it matches the pre-defined one.

# 3.2 Filter

Figure 4(a) shows 12 seconds of data acquisition. We find three special periods in which the waving values are too low to be detected. We can regard such periods as the silent periods. The silent periods may exist at the initial stage before the user shakes his smart phone, or in the final stage after the user stops his waving. The period may also be observed in the intermediate stage when an unexpected user’s pause occurs. Since the silent periods will seriously affect the accuracy of OpenSesame, we must filter those data captured during this periods. The $i ^ { t h }$ raw tuple with composed acceleration value $A _ { i }$ is wiped out if it satisfies the equation:

$$
\sum_ {x = i - b} ^ {i + b} (A _ {x} - \sum_ {y = i - b} ^ {i + b} \frac {A _ {y}}{2 b + 1}) ^ {2} <   \alpha , \tag {2}
$$

where b is called the tolerant static period, representing the amount of acceleration points used to determine the stability of an acceleration point. The α is the threshold to filter the silent points. Based on our algorithm, the filtered data is illustrated in Figure 4(b).

![](images/c0b6125beae236f0cf3b51f1a054462c2a0292bd5c7827d74fe451c209b53702.jpg)



(a) Before filtering   
![](images/56ca44ba973208ee72460ff1ee97870852de8d5b0d7e649a100cf498db14574f.jpg)



(b) After filtering   
Fig. 4: Comparing the features before and after filtering

# 3.3 Fetcher

After the filter component, we need to generate the feature vector of the user’s handwaving action. According to Section 2.3, the field set of the acceleration points can be treated as one single input of waving function, and the waving function can be applied to this input to generate the feature vector. However, using the field set as an input has two shortcomings. First, the amount of acceleration points in a field set is large, usually more than 1000. In order to generate a representative feature vector for the waving action data, an extremely large number of feature vectors are required. In this way, the system overhead is high and affects the normal operation of the smart phone. Second, to unlock the smart phone, the user is required to shake his smart phone for a period to generate same amount of waving data. However, it is inconvenient to ask the user to shake the smart phone for such a long time period to generate more than 1000 acceleration points for each time he wants to unlock his phone. Therefore, the amount of acceleration points selected as an input needs to be reduced.

According to our observation, the waving action of user always shows the property of repeating. In fact, the input waving action can be regarded as a series of small repeating waving actions which are very similar. Therefore, we can select a continuous sequence of acceleration points with a reasonable amount as an input to the waving function. Feature vectors can be generated from these small inputs with low data loss.

We generate the feature vectors as follows: we first select a window with size w, where w is much smaller than the size of the field set of data. From the field set of data, we select an acceleration point $P _ { k }$ and form the input with the subsequence of w continuous acceleration points $\left\{ { { P } _ { k } } , { { P } _ { k + 1 } } , { { P } _ { k + 2 } } , . . . , { { P } _ { k + w - 1 } } \right\}$ . Then we apply the waving function on this input and deliver the PDF of the feature vectors to describe the feature of the waving action.

# 3.4 Classifier

The feature classifier is designed to generate a standard to discriminate authorizeds user and unauthorized users with the feature vectors of the input waving action data. In OpenSesame, the support vector machine, SVM for short, is selected as the classifier. The SVM classifier is used to classify a group of linear-inseparable training tuples into two classes. Training tuples for SVM input is donated as $\{ \mathbf { v } , y \}$ , where v is the attribute vector used to describe the attributes of the training tuple, and $y$ is the label of the training tuple, which represents the actual class it belongs to. The basic idea of SVM is to transform these attribute vectors of training tuples into a higher dimensional space to make the training tuples linear-separable. Then the training tuples can be separated into two classes by a hyperplane. The SVM classifier classifies the training tuples based on this hyperplane, attempting to classify training tuples with same label into same class. Then a classification model is generated to describe the classification standard of a given tuple. Inputting an unclassified tuple into the SVM classifier using the generated classification model, the tuple can be predicted which class it most probably belongs to.

In OpenSesame, the label of the training tuple is either +1 or −1. When $y = + 1$ , the tuple is generated from the class of unauthorized users. On the contrary, $y = - 1$ means the tuple belongs to the authorized user’s class. The attribute vector v is generated from the feature vector we gain from Section 3.3. The attribute vector can be represented as $[ a _ { 1 } , a _ { 2 } , . . . , a _ { n } ] ^ { T }$ . Here, $a _ { i }$ is $i ^ { t h }$ property of the training tuple, which represents the $i ^ { t h }$ value in the feature vector. By injecting enough amount of training tuples into the SVM classifier, a classification model can be achieve to verify the authentication data of user.

# 3.5 Matcher

The matcher component is performed when the user activates the authentication interface of OpenSesame and wants to unlock the smart phone. The user shakes the smart phone to input his waving action as the authentication data. Feature vectors of the input waving action is generated and used to verify whether the user is the authorized user. If so, the access query is accepted and the smart phone is unlocked. If not, the access query is denied and the smart phone keeps locked.

The most important requirement is that the feature matching phase has to be processed within a short time period, say 1 or 2 seconds. The reason is that users always expect the unlocking process to be fast and convenient. If the feature matching time is long, the inconvenience overweighs the security of our approach and the users may decide to give up our system. To reduce the response time, two aspects need to be considered. The first issue is to reduce the amount of repetition when doing authentication. This can be achieved by reducing the false negative rate of authentication, which is going to be discussed in the experiment section. The second issue is to reduce the waving time in the matcher component. As we designed in the fetcher component, by using a small waving function input with window size w, the waving time can be reduced to the time period for collecting w acceleration points. Since w is much smaller than the size of the field set of acceleration points. Therefore, the waving time can be reduced to a tolerant range.

![](images/92101f8602810495e00c248bb54b0756b57c4ac31405e35188f0197da2ab1b4a.jpg)



(a) Screen locking

![](images/69673bc4f8ba2d6d6009c53deaf6e5dac0034dd90447cd3cec986b43fb9160bd.jpg)



(b) Access denied

![](images/eb525e77275d421d1c613396e67a6ede23b1ba72ee7fd1fb65ef7d7abdaaf464.jpg)



(c) Access accepted   
Fig. 5: The UI of OpenSesame

Normally, since the waving time is short, we assume that there is no pause in the middle of the waving action to reduce the complexity of filter. To detect the initial recordof the $i ^ { t h }$ ture pointpoint as $\begin{array} { r } { \sum _ { x = i - b } ^ { i } ( A _ { x } - \sum _ { y = i - b } ^ { i } { \frac { A _ { y } } { b + 1 } } ) ^ { 2 } } \end{array}$ tability. Once the real-time stability value is greater than the threshold, acceleration point $P _ { i }$ is set to be the initial point, and the waving action detection terminates when acceleration point sequence $\{ P _ { i } , P _ { i + 1 } , . . . , P _ { i + w } \}$ is recorded. Applying the same waving function to this sequence, we can generating the predict tuple with attribute vector $[ a _ { 1 } , a _ { 2 } , . . . , a _ { n } ] ^ { T }$ . By inputting this predict tuple into the SVM classifier with the classification model we delivered in classifier component, the SVM classifier decides which class the input tuple most likely belongs to. When the input tuple is classified into the authorized user set, the authentication is successfully done and the smart phone is unlocked. Otherwise, the smart phone requires another authentication try.

# 4 IMPLEMENTATION AND EVALUATION

In this section, we present the implementation of OpenSesame and evaluate its performance.

# 4.1 Implementation App

We implement OpenSesame in Android-based smart phones. The version of Android system is 2.3.3. the app is developed with Android-SDK using Java SE. Figure 5 shows the GUI of our app. With this app, the user’s handwaving data is collected and analyzed by the smart phone. Specifically, the interfaces shown in Figure 5(b) and Figure5(c) are used to notice whether the unlocking access is success or not. We use the open source library tool, LIBSVM [16], to perform the classification of SVM. LIBSVM is an integrated software for support vector classification. The version we used is LIBSVM-3.12. During our experiments, we use the default kernel function (Gaussian Radial Basis Function) and find the best setting of parameters Cost and γ for the kernel function via the cross-validation when generating the training model.

# 4.2 Metrics

We evaluate OpenSesame in terms of the authentication accuracy. The authentication accuracy is measured via the following metrics:

• False Negative Rate (FNR): The probability that an authorized user is treated as an unauthorized user. This rate is indeed the ratio of the number of incorrect authentications conducted by an authorized user to the number of his authentication attempts.   
• True Positive Rate (TPR): The probability that an authorized user is successfully verified. This rate derived from the ratio of correct authentication times of an authorized user to the number of his authentication attempts.   
• False Positive Rate (FPR): The probability that an unauthorized user is treated as an authorized user. This rate is obtained from the ratio of the incorrect authentication times of an unauthorized user to the number of his authentication attempts.

Note that FNR and TPR are related to the convenience of users when they use our system, where the authorized user can successfully unlock the smart phone by a single try. The FPR reflects the security of the OpenSesame, where the unauthorized user should be denied to unlock the smart phone.

# 4.3 Experiment Setup

For investigating the uniqueness of handwaving, we collect the waving action data from 200 distinct smart phone users. The subjects producing these datasets are randomly selected in different public places, including railway station, university library, and stadtpark. When collecting the waving action data, three smart phones from different brands are used. For collecting each specific users handwaving data, he is asked to act with the following instruction: The user first randomly selects one of the three smart phones we provided, and holds this smart phone, which is running our data collection app, in his accustomed way. Then he pushes the button of ‘start’ on the screen and begins to wave the smart phone until the hint sound is played by the smart phone. This waving process lasts for more than 10 seconds. The user repeats the above action for three times to terminate the data collection. Note that there is no special restriction on users waving actions. He can wave the smart phone arbitrarily in each trail. Indeed, we aim at taking insight into the handshaking action but not the motion pattern.

![](images/02634260d0652ecaaa908bc25c417a4e2c48f23ead8250644309c99739be811e.jpg)



(a) False Negative Rate   
![](images/5eb19cde9f6bb8ad2f5734b3e125b40c08c62528d96d5639342ae5a33c7a94a7.jpg)



(b) False Positive Rate   
Fig. 6: Impact of waving functions

![](images/ff618507ab855e2a82a07d7a4e9b0b12cc4efca62e0067713cd10c317033f359.jpg)



(a) False Negative Rate   
![](images/4600d412fdb1c4ff9a744fe66e12aa82fee1ac17bef97d76e6ed6727495d232b.jpg)



(b) False Positive Rate   
Fig. 7: Impact of windows size

Overall, 389,373 raw tuples are captured from 200 distinct users, with an average 1,947 raw tuples per user. Each user performs the handwaving for three trails while each trail persists 10 ∼ 20 seconds. For each user, the training data will be extracted from the first two trails, while the testing data will be retrieved from the last one. Therefore, there is no overlap between the training data and testing data. The classification is based on self and non-self discrimination. For a given user, the training data is composed of negative samples belonging to this user, and an equal number of positive ones from others.

# 4.4 Impact of Waving Functions

There are four waving functions to parameterize the A-Space representation of handwaving. In this experiment, we select 30 users’ handwaving and maintains the window size as 50 tuples. Figure 6 plots the FNR and FPR for the four waving functions. From the Figure 6(a), we observe that the average FNR using $S _ { 1 }$ and $S _ { 2 }$ are around 20% while the values are below 10% using $S _ { 3 }$ and $S _ { 4 } .$ . The similar observation is obtained on FPR, as shown in Figure 6(b). This shows that the distance-based waving functions perform better than the angle-based ones. We further focus on the distance-based waving functions. $S _ { 3 }$ and $S _ { 4 }$ have close FNRs and FPRs. However, the variance of $S _ { 4 }$ is smaller than that of $S _ { 3 }$ , which means $S _ { 4 }$ is more stable than $S _ { 3 }$ .

# 4.5 Impact of SVM

Window size is an important factor. For capturing enough windows, we require the users to shake their phones in a acceptable time period. A large window size will prolong the waving time period for unlocking and seriously affect user experiences. But a small window size will influence the identification accuracy. We change the windows size from 5 to 50 with the increment of 5 and employ $S _ { 4 }$ for testing. The result is shown in Figure 7. The average FNR decreases from 20% to 8% and the average FPR reduces from 42% to 18% as the window size increases. This shows that the larger window helps improve the accuracy. This is because that more raw tuples are extracted in a larger window and the user’s handwaving is better characterized.

The number of training tuples also affect the accuracy. As illustrated in Figure 7, FNR is approximately reduced by 50%, $i . e .$ from 15% to 8%, when window size is 50. This reduction is even obvious with small window size. On the other hand, the average FPR only reduces from 20% to 15% taking 5% off when window size is 50. This shows that FPR is less sensitive to the number of training tuples.

# 4.6 Impact of Sampling Rate

Accelerometer in smart phones has variant modes of sampling. With different sampling modes, the collection of data can be much different. In this experiment, we test the OpenSesame both in fast sampling mode and normal sampling mode. It can reach a very high 90% average accuracy in the fast sampling mode while the number is

![](images/743cb2fbd317558a0fa5be903754165ff785dda4d36e662eebcbb157ee87a5ab.jpg)



Fig. 8: Sampling mode

![](images/4e8e816254ca7cdef003b9e17ab1b819ff25b55f714e7e33f1e41f75e48cdf4a.jpg)



Fig. 9: User’s motion

55% with normal sampling mode. Losing part of waving data with low sampling rate is the major reason for the poor performance.

# 4.7 Impact of User Motion

As mentioned before, our approach should be insensitive to the user’s motions because the smart phone is mainly used in mobile environment. Clearly, the user motion will introduce many noises. In this experiment, we test the relationship between the speed of user’s motions and the accuracy. Five user’s motions are considered: stationary, walking slow, walking fast, running, and taking a vehicle. The result is shown in Figure 9. From the figure, we can see that as the speed growing from 0 m/s to 5 m/s, the FNR is steady around 11%, with a standard deviation of 2.0%. This indicates that the motion of users makes a very limited effect on our approach. Besides, the FPR is also invariant when the speed of user’s motion increases. The false positive rate is around 15% with a standard deviation of 2.5%. It can be further obtained from Figure 9 that, the FNR has an slightly increase, about 7%, when the speed of user increases from 0 m/s to 5 m/s. This can be understood because the faster motion will increase vibration in his smart phone leading to more noisy. However, these motion has very limited effect on the accuracy.

# 4.8 Impact of Phone Diversity

Nowadays, there are plenty of smart phone brands, such as iPhone, MOTO, SAMSUNG, HTC, etc. To promote the OpenSesame to smart phone users, one crucial issue is whether the OpenSesame can be well adapted to different brands of phones. The most effective factor on different smart phones is the type of accelerometer equipped. For different types of accelerometers, the level of sensitivity is different. Hence, the waving data collected is inequivalent.

![](images/a223a2f506ea58163809d17849d89598104ff9b8ad7ac8bbe3f802afeba1d578.jpg)



Fig. 10: Phone Brand

![](images/f9e7573472507edfdd23b7b95ddaedfdd279ab03b0656bb87be9cbf16af31a16.jpg)

![](images/5dd05c87965740b2561c70168ed52d95aaea730ee7c523ba8c4c12807c1362d8.jpg)

![](images/84ee49c6f0ca9674a4b94e5f91121eae1f2233e6fa8db923736988e3599b016b.jpg)

(a) A-Space representation   
![](images/a74fd0935c1f14de9d50ad86a8d819e33b7862940f9b17e915b9bf452a4176f2.jpg)



(b) Feature PDF via $S _ { 4 }$

![](images/38d0fac2748d0e6060895d1e92c4dc742b00dfd8b342735ee1024367c5d39695.jpg)



(c) CDFs of TPR   
Fig. 11: Impact of phone’s orientation

In this experiment, three different brands of phones are tested. For these three brands, the order from low to high based on the accelerometer is Phone A, Phone B, and Phone C. 40 sets of trials are tested on each smart phone and the FNR is reported in Figure 10. From the figure, we can see that the Phone C achieves the lowest FNR and Phone A has the worst value. That is because more sensitive accelerometer can collect more fine-grained data, which reflects more complete feature from waving actions. The average FNRs of three smart phone are below 10%, which is all acceptable in practice. Therefore, The OpenSesame can be well adapted to different brands of smart phones.

# 4.9 Impact of Smart Phone’s Orientation

Although the waving habit may be similar for an identical user, the postures of users when waving the smart phone can change the orientation of the phone. In this section, we evaluate OpenSesame with variant phone’s postures. In this experiment, three user’s postures are tested:

![](images/3f2172675b580aaeb52d3a47aaeb3a9b8ecab44f27436ca537cf88e3474a8aa5.jpg)



Fig. 12: Distances

• Standing: waving phone when standing on the ground. We consider the standing as a normal posture.   
• Lying: waving phone when lying on the bed. The waving orientation is rotated 90 degrees upward.   
• On-the-side: waving phone when sleeping on the user’s left side. The waving orientation is rotated 90 degrees to the left.

The results are shown in Figure 11. In the figures, we illustrate the A-Space representations of waving data by the three postures in Figure 11(a). Intuitively, these tree trails are similar, all like a shape of crescent, but having different orientation. Our approach should be insensitive to the rotation. We transform the waving from A-Space to feature PDF, shown in Figure 11(b), by means of waving function S4. As we expected, the difference of these three PDFs is very slight. In details, the distance between standing posture (the normal posture) and the lying posture/on-theside posture are 0.172 and 0.173, respectively. We believe these distances are small enough for the trails to be treated as coming from an identical user.

Furthermore, We conduct one trail in standing posture and store the corresponding result feature vector in our smart phone. Then we attempt to unlock the smart phone in the three postures. Each posture is repeated 30 trails. Finally, the CDF of accuracy is displayed in Figure 11(c). For the standing posture, 20% trails have an accurate rate lower than 90%, while 20% of lying posture and on-theside posture have accurate rate lower than 86% and 76%, respectively. Meanwhile, 20% lying postures and 45% onthe-side postures have their accurate rates higher than 90%. This experiment fully demonstrates that our approach is phone-orientation-insensitive.

# 4.10 Discrimination

We consider the OpenSesame’s capability of discrimination among different users. One user’s trace is selected and his similarity compared to other uses is calculated. The result is shown in Figure 12. From the figure, we can see that selfsimilarity is approximately bounded under 0.3, and 90% of the distances are lower than 0.25. Being different with the self-similarity, the distance between the given user and others is obvious. Only 8% of the distances are lower than 0.2, and about 20% of the distances are larger than 1.0.

![](images/c5260cf2de1f877e6ccae8560588d9b5a4896a6da30fe9d36fbcb616c5542baa.jpg)



(a) OpenSesame

![](images/f02acdb221a0a37f85d607752212dc96a3db247466437fc3515307c923e732f4.jpg)



(b) DTW   
Fig. 14: The normalized similarities under four cases using DTW and OpenSesame.

Hence, the discrimination of distinct users and recognition of identical users can be achieved.

Although the percentage of small distances between distinct users’ features is low, it may still affect the accuracy of the OpenSesame. It is necessary to find out the reason of the failure in discriminating the distinct users’ features. In Figure 13, three users’ A-Space representation are randomly selected. For each row, the top four similar users’ A-Space representations are listed. From these figures, we can find that the similar A-Space representations cause small distance of users’ features. For extremely close A-Space representations, such as the second figure in the first row, the distance is very small, e.g. 0.074. With higher dissimilarity of A-Space representations, for instance the last figure, the distance is larger, e.g. 0.147. Since the A-Space representation can reflect the waving action on the smart phone, we can draw the conclusion that for the users with similar habit of waving action, the probability of failure for the OpenSesame increases. Fortunately, referring to Figure 12, such kind of probability is low and OpenSesame therefore performs well as expected.

# 4.11 Comparison with DTW

The Dynamic Time Wrapping (DTW) is a well-established technique from speech processing, which is used to measure the similarity between two temporal sequences which may vary in time or speed. The advantage of DTW is that it can well deal with the misalign of points in the temporal sequences. DTW is only suitable for the case in which the user must wave his/her smart phone along a fixed, secrete and pre-defined movement. However, we pursue that the users are able to shake their phones in wider free movements in terms of their daily habits. In this situation, the DTW has following two major technical limitations compared with our shaking functions. First, the data acquired from the accelerator highly depends on the smart phone’s orientation. To maintain the similar shaking sequence for DTW identification, the users have to keep the same orientation as trained. Second, DTW cannot deal with the existence of noise, blur, cracks, and dust in the shaking data. Four kinds of waving functions we proposed are based on the statistics, being able to well address above issues.

![](images/96c7096a9810b20406f03bd7da86f5eb511de01db41b946469d3456280a0b2f4.jpg)



![](images/b76270efdd3f079a12e356f217789940b9672e72221168313be20da07b33c806.jpg)



(a) 0.074

![](images/79474256f0dfd473be8e18c84b20038c29f2ecaf30b354a0e46acfa9e5ce78ac.jpg)



(b) 0.114

![](images/175c97d8f5583a485fae1a1c08ecd4a982ea623aaedea80a0e0494529f5239c7.jpg)  
(c) 0.161

![](images/090cab704e63928ffe28567ea224ba613d37c738a4c6725aa57d95ae013353bc.jpg)



(d) 0.162

![](images/5a0eb6a67cccbaa8ad2dab4cf8503a62cc02f9d155b672fdaec2836350515ee5.jpg)



![](images/1e08b17eeec5d65fe61b934bf3c9d2f3611d32f4ebe79d634139757dd7783a64.jpg)



(a) 0.103

![](images/808a654e854bbe56b510a517dfe8207a83a9c33722dda2d5e7a5400383ef2bdf.jpg)



(b) 0.115

![](images/e4c0b6f22fb0d7aa000dca8b3815f50da1d6b34e62676d87b14f8fc4e730eb30.jpg)



(c) 0.117

![](images/07fafc4fb15e6cadde143a4440f6e957a64dc0534f9c815db6b0f20fd4cfe8ff.jpg)



(d) 0.120

![](images/269eb3d2c12adc0d993e20a10f4a9df3751d94aa64654508abd3f99e5b703c11.jpg)



![](images/b26ee2ef951201e0ac26a64aed1cd691bb281fc82dd59fc0ee04609ddf916f1c.jpg)



(a) 0.118

![](images/f71d102b42b2b58e3988b4b0e671a5046b1272d3852b1b95d7aec786392caf6a.jpg)  
(b) 0.128

![](images/2c8828d106022e53cac967969d5b6b4efb66f02a5d709aa0f38c398cd58a283c.jpg)



(c) 0.139

![](images/254650cf64d72b4f3a1d4c6f3b4297ef45b82f868796060727d521dea3f8df4a.jpg)



(d) 0.147   
Fig. 13: Top 4 Similar A-Space Points and the Distances to the Reference A-Space Points

To further compare the performance of DTW and OpenSesame, we let the user perform the following four trails:

• Case 1 (C1): The user waves his/her smart phones as trained.   
• Case 2 (C2): The user waves the smart phone as the mode he/she gets used to but not required as same as trained.   
• Case 3 (C3): The user waves his/her smart phone as trained but the orientation of smart phone is reversed.   
• Case 4 (C4): A second user attempts to wave the same smart phones as his habit.

The normalized similarities using DTW and waving functions are shown in Figure 14. We observe that (1) The normalized similarities from Case 1 to Case 3 are almost below 0.5, showing that whatever the user how to wave his/her phone, the self-similarities always maintain under an acceptable level. When changing user in Case 4, the similarity exceeds the threshold of 0.5, resulting a unlocking rejects. (2) When the user waves his/her smart phone not as trained, even just reversing the orientation, the normalized similarities are much higher than that of Case 1. In summary, the system can well distinguish different users whatever using OpenSesame or DTW. However, the DTW requires the user must wave his/her smart phones as trained.

# 4.12 Usability

We also conducted some filed trails using our prototype to evaluate the usability of our system. We invited about 10 college students who install our system and unlock their phones through OpenSesame. We measure the overall time they take to unlock the screen and ask for their feedback on our prototype. Different phone models are used in experiments, including HTC One, Xiaomi 2, Nexus 5, Huawei C8815 and Sony Xperia.

First, we collect the average and standard deviation of the time consumption for unlocking their smartphones. We see that it takes lower than 3 seconds by 6/10 users to unlock their smart phones. Compared with the slide-to-lock or PIN (taking about one second), the OpenSesame does not improve the unlocking. However, the savings come from (1) the simplified user interface as users do not need to take off the gloves for touch screen, or remember some complex passwords. (2) the security is also promoted in some extent.

Second, we ask the volunteers to fill the questionnaires in terms of learning curve, user-friendly, security and accessibility. The volunteer gives a score ranging from 1 to

![](images/306526af4860188dd105362f144bbbeebc8b9c2d61f50dde48719b53b647e14c.jpg)



Fig. 15: Time consumption

TABLE 1: Trial Experience 

<table><tr><td></td><td>Learning curve</td><td>User-friendly</td><td>Security</td><td>Accessibility</td></tr><tr><td>mean</td><td>1.2</td><td>4.8</td><td>3.6</td><td>4.8</td></tr><tr><td>stdev</td><td>0.5</td><td>1.5</td><td>1.1</td><td>1.3</td></tr></table>

5 for each item. The results are shown in Table 1. We can see that all the users indicate that our solution is very easy to use and intuitive, with almost no learning curve. This is the key value of OpenSesame, which we think is even more important than speed improvement. However, the user have a little concerns about the security. It is reasonable because each new technology has a process to be accepted. We believe that these concerns will gradually disappear as the OpenSesame is more widely accepted.

# 5 RELATED WORK

# 5.1 Accelerator based Authentication

A work parallel to ours is that Conti et al. propose to adopt the movement the user performs when answering a phone call to authenticate the user of a smartphone, which utilizes two kinds of components, accelerometer and orientation sensors, in smart phones [11]. Their work has following three major technical limitations compared to our work. First, their method in fact highly depends the phone’s trajectory, related to the phone’s movement parameters, such as the start position, end position, orientation and velocity. As long as the system learns the trajectory when the user picks up the phone from the pocket and moves to his/her ear, other trajectories, like the movement from the desktop to ear, will be rejected. On the contrary, our method concentrates on the human’s inherent characteristics, like the length arm and wrist size, among different users that leads to the waving differences. Thus, we don’t need the user to perform specific movements. Second, our four kinds of waving functions are designed to be invariant to the position or direction changes of smart phone. The user can wave the phones starting or ending at arbitrate positions. Importantly, our approach allows the existence of noise, blur, cracks, and dust in the shaking. Therefore, our approach provides much more freedom to user compared with theirs. Third, their method needs the orientation sensors, which are not fully supported by all smartphones, especially among low-grade mobile phones.

The second work parallel to ours is to identify users based on a secrete movement pattern measured by the accelerator sensor [17] and [18]. Liu et al. aims at identifying users based on a secrete movement pattern [17]. e.g. moving the phones as if to draw an ‘8’ in the air where ‘8’ is a secrete. Similarly, Okumura et al. asks the tester to grasp the device int the same way and shake it simple up and down in direction of y-axis 5 times continuously [18]. Being similar to the tranditional methods like PIN or password, an adversary might spy the movement, replay it, and get access to the phone and its data.

Importantly, above methods have not been evaluated their scheme in real word scenarios while ours are verified among 200 distinct users.

# 5.2 Touch based Authentication

These work [10], [19], [20] utilizes the unique interaction between user and the touch screen to identify the users. Sae-Bae et al. propose to use the timing of performing five-finger gestures on multi-touch capable of devices for authentication [10]. Luca et al. propose the timing of drawing the password on Antriod based touch screen phones for authentication [20]. Shahzed et al. propose to utilize the correlations among predefined ‘gestures’ i.e. touch trajectories for authentication. Their work requires users to use fingers to perform the gestures with the following two major limitations compared to our work [19]. First, their methods require users to use more than two fingers of a hand to perform the predefined gestures, which is very inconvenient on small touch screens of smart phones. Second, most of smart phones employ capacitive touch screens that only recognize the human’s finger without gloves. It is a wore experience to take off the gloves for answering a phone outside in winter. Our method, shaking the smart phone, behaves much more user friendly

# 5.3 Keystrokes based Authentication

These work proposes to identify users based on their typing behavior [12], [14], [21]. These methods mainly proposed for devices with physical keyboards and are inapplicable for smart phones. In addition, they have low accuracy because it is difficult to model typing behavior on touch screens because most people use the same finger for typing all keys on the keyboard displayed on the screen of smart phone.

# 5.4 Gait based Authentication

There are several methods [15], [22], [23] proposed to utilize the accelerator in smart phones to authenticate users based upon their gaits. Their accuracies are vulnerable to the types of surfaces such as grass, road, snow, wet surface, and slippery surface. They are also inapplicable for unlocking smart phone, in that it is infeasible to let user walk first to figure out whether she/he is the correct user or not, in order to recognize the user from his/her walking pattern.

# 6 CONCLUSION

In this paper, we propose a novel behavioral biometricbased authentication approach called OpenSesame for smart phone. We design four waving functions to fetch the unique pattern of user’s handwaving actions. By applying the SVM classifier, the smart phone can accurately verify the authorized user with the pattern of handwaving action. Experiment results based on 200 distinct users’ handwaving actions show that the OpenSesame reaches high level of security and robustness, and achieves good user’s experience.

# REFERENCES

[1] D. Florencio and C. Herley, “A large-scale study of web password habits,” in Proc. of ACM WWW, 2007.   
[2] J. Bonneau, “The science of guessing: analyzing an anonymized corpus of 70 million passwords,” in Proc. of IEEE Security and Privacy (SP), 2012.   
[3] H.-A. Park, J. W. Hong, J. H. Park, J. Zhan, and D. H. Lee, “Combined authentication-based multilevel access control in mobile application for dailylifeservice,” IEEE Transactions on Mobile Computing, 2010.   
[4] N. Ben-Asher, N. Kirschnick, H. Sieger, J. Meyer, A. Ben-Oved, and S. Moller, “On the need for different security methods on mobile ¨ phones,” in Proc. of ACM HCI, 2011.   
[5] R. V. Yampolskiy and V. Govindaraju, “Behavioural biometrics: a survey and classification,” International Journal of Biometrics, 2008.   
[6] A. H. Akkermans, T. A. Kevenaar, and D. W. Schobben, “Acoustic ear recognition for person identification,” in IEEE Workshop on Automatic Identification Advanced Technologies, 2005.   
[7] A. Jain, L. Hong, and Y. Kulkarni, “A multimodal biometric system using fingerprint, face and speech,” in Proc. of Audio-and Videobased Biometric Person Authentication, 1999.   
[8] P. J. Phillips, A. Martin, C. L. Wilson, and M. Przybocki, “An introduction evaluating biometric systems,” Computer, vol. 33, no. 2, pp. 56–63, 2000.   
[9] R. LiKamWa, B. Priyantha, M. Philipose, L. Zhong, and P. Bahl, “Energy characterization and optimization of image sensing toward continuous mobile vision,” in Proc. of ACM MobiSys, 2013.   
[10] N. Sae-Bae, K. Ahmed, K. Isbister, and N. Memon, “Biometric-rich gestures: a novel approach to authentication on multi-touch devices,” in Proc. of ACM CHI, 2012.   
[11] M. Conti, I. Zachia-Zlatea, and B. Crispo, “Mind how you answer me!: transparently authenticating the user of a smartphone when answering or placing a call,” in Proc. of ACM ASIACCS, 2011.   
[12] F. Monrose, M. K. Reiter, and S. Wetzel, “Password hardening based on keystroke dynamics,” International Journal of Information Security, 2002.   
[13] N. Zheng, A. Paloski, and H. Wang, “An efficient user verification system via mouse movements,” in Proc. of ACM CCS, 2011.   
[14] E. Miluzzo, A. Varshavsky, S. Balakrishnan, and R. R. Choudhury, “Tapprints: your finger taps have fingerprints,” in Proc. of ACM MobiSys, 2012.   
[15] D. Gafurov, K. Helkala, and T. Søndrol, “Biometric gait authentication using accelerometer sensor,” Journal of computers, vol. 1, no. 7, pp. 51–59, 2006.   
[16] C.-C. Chang and C.-J. Lin, “Libsvm: a library for support vector machines,” ACM Transactions on Intelligent Systems and Technology (TIST), vol. 2, no. 3, p. 27, 2011.   
[17] J. Liu, L. Zhong, J. Wickramasuriya, and V. Vasudevan, “User evaluation of lightweight user authentication with a single tri-axis accelerometer,” in Proc. of ACM MobiHCI, 2009.   
[18] F. Okumura, A. Kubota, Y. Hatori, K. Matsuo, M. Hashimoto, and A. Koike, “A study on biometric authentication based on arm sweep action with acceleration sensor,” in Proc. of IEEE ISPACS, 2006.   
[19] M. Shahzad, A. X. Liu, and A. Samuel, “Secure unlocking of mobile touch screen devices by simple gestures: You can see it but you can not do it,” in Proc. of ACM MobiCom, 2013.   
[20] A. De Luca, A. Hang, F. Brudy, C. Lindner, and H. Hussmann, “Touch me once and i know it’s you!: implicit authentication based on touch screen patterns,” in Proc. of ACM CHI, 2012.

[21] S. Zahid, M. Shahzad, S. A. Khayam, and M. Farooq, “Keystrokebased user identification on smart phones,” in Recent Advances in Intrusion Detection. Springer, 2009, pp. 224–243.   
[22] J. R. Kwapisz, G. M. Weiss, and S. A. Moore, “Cell phone-based biometric identification,” in Proc. of IEEE BTAS. IEEE, 2010, pp. 1–7.   
[23] J. Mantyjarvi, M. Lindholm, E. Vildjiounaite, S.-M. Makela, and H. Ailisto, “Identifying users of portable devices from gait pattern with accelerometers,” in Proc. of IEEE ICASSP, 2005.