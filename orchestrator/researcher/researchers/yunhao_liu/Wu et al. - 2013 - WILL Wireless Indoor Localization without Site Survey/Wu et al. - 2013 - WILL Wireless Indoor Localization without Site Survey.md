# WILL: Wireless Indoor Localization without Site Survey

Chenshu Wu, Student Member, IEEE, Zheng Yang, Member, IEEE, Yunhao Liu, Senior Member, IEEE, and Wei Xi, Student Member, IEEE

Abstract—Indoor localization is of great importance for a range of pervasive applications, attracting many research efforts in the past two decades. Most radio-based solutions require a process of site survey, in which radio signatures are collected and stored for further comparison and matching. Site survey involves intensive costs on manpower and time. In this work, we study unexploited RF signal characteristics and leverage user motions to construct radio floor plan that is previously obtained by site survey. On this basis, we design WILL, an indoor localization approach based on off-the-shelf WiFi infrastructure and mobile phones. WILL is deployed in a real building covering over 1600 m2, and its deployment is easy and rapid since site survey is no longer needed. The experiment results show that WILL achieves competitive performance comparing with traditional approaches.

Index Terms—Wireless, indoor localization, fingerprint, site survey

# 1 INTRODUCTION

PERVASIVE and mobile systems for context-aware comput-ing are growing at a phenomenal rate. In most of today’s ing are growing at a phenomenal rate.In most of today's applications such as pervasive medicare, smart space, wireless sensor surveillance, mobile peer-to-peer computing, [1], [2] etc., location is one of the most essential contexts. In the literature of pervasive computing, wireless indoor localization has been extensively studied and many solutions are proposed to provide room-level localization services, such as locating a person or a printer in an office building.

A majority of previous localization approaches employ Received Signal Strength (RSS) as a metric for location determination. RSS fingerprints can be easily obtained for most off-the-shelf equipments, such as WiFi- or ZigBeecompatible devices. In these methods, localization is divided into two phases: training and serving. In the first phase, traditional methods involve a site survey process, in which engineers record the RSS fingerprints (e.g., WiFi signal strengths from multiple Access Points, APs) at every position of an interesting area and accordingly build a fingerprint database. Next in the serving phase, when a user sends a location query with its current RSS fingerprint, localization algorithms retrieve the fingerprint database and return the matched fingerprints as well as corresponding locations.

. C. Wu is with the Department of Computer Science and Technology, School of Software, TNLIST, Tsinghua University, Beijing, 100084, China. E-mail: wu@greenorbs.com.   
. Z. Yang and Y. Liu are with the School of Software, TNLIST, Tsinghua University, Beijing, 100084, China, and with the Hong Kong University of Science and Technology, Hong Kong. E-mail: yang@greenorbs.com, yunhao@greenorbs.com.   
. W. Xi is with the Department of Computer Science and Technology, School of Electronic and Information Engineering, Xi’an Jiaotong University, Xi’an, Shaanxi, 710049, China. E-mail: xiwei@greenorbs.com.

Manuscript received 13 Feb. 2012; revised 9 May 2012; accepted 29 May 2012; published online 6 June 2012.

Recommended for acceptance by J. Cao.

For information on obtaining reprints of this article, please send e-mail to: tpds@computer.org, and reference IEEECS Log Number TPDS-2012-02-0097. Digital Object Identifier no. 10.1109/TPDS.2012.179.

Although site survey is time consuming, labor intensive, and easily affected by environmental dynamics, it is inevitable for those RSS fingerprint matching-based approaches based on RSS fingerprint matching, since the fingerprint database is constructed based on on-site fingerprint collection.

To avoid site survey, researchers turn to characterizing wireless signal propagation. They aim to build accurate signal attenuation models and use RSS as an indication of signal propagating distance. Unfortunately, attenuation models perform poorly due to unpredictable signal propagation in complex and dynamic indoor environments, lacking technical potentials for practical uses.

The advance of wireless and embedded technology has fostered the flourish of smartphone market. Nowadays, mobile phones possess powerful computation and communication capability, and are equipped with different kinds of built-in sensors for various functions. Accompanying with users round-the-clock, mobile phones can be viewed as an increasingly important information interface between users and environments. These advances lay solid foundations of breakthrough technology for indoor localization.

On this basis, we reassess existing localization schemes and explore the possibility of using previously unavailable information for wireless indoor localization. Considering user movements, originally separated RSS fingerprints are connected under certain semantics. Similarly, studying the penetrating-wall effect of wireless signals is a good starting point for characterizing different rooms or functional areas. These observations motivate us to design rapidly deployed localization approaches without the laborious site survey process.

In this study, we propose WILL, a wireless indoor logical localization approach. By exploiting user motions from mobile phones, we successfully remove the site survey process of traditional approaches, while achieving competitive localization accuracy. The rationale behind WILL is that human motions can be applied to connect previously independent radio signatures under certain semantics. WILL requires no prior knowledge of AP locations, and users are not required for explicit participation to label measured data with corresponding locations, even in the training phase. In all, such features introduce new prospective techniques for indoor localization.

To validate this design, we deploy a prototype system and conduct extensive experiments in a middle-size academic building in Tsinghua University. Experiment results show that RSS-based indoor localization can achieve room-level location accuracy even without site survey. The average room localization accuracy, namely, accuracy of locating fingerprints to the rooms they are actually collected from, is over 80 percent, which is competitive to existing solutions.

The rest of the paper is organized as follows: We investigate the state of the art on indoor localization technology in Section 2. Section 3 presents our design overview. The generation of virtual rooms is studied in Section 4. In Section 5, the techniques of floor plan mapping, a key step of constructing the relation between virtual rooms and ground-truth floor plan without site survey, are discussed in detail. Section 6 summarizes the entire working process of WILL when it receives a location query. The prototype implementation and experiments are discussed in Section 7. We conclude the work in Section 8.

# 2 RELATED WORK

Location information is essential for a wide range of pervasive and mobile applications, such as wireless sensor networks, mobile social networks, location-based services, smart space, etc. [1], [2], [3]. In the literature of indoor localization, a well-known research direction, many techniques have been proposed in the past two decades. Generally, they fall into two categories: fingerprinting based and model based.

Fingerprinting-based techniques. A large body of indoor localization approaches adopt fingerprint matching as the basic scheme of location determination. The main idea is to fingerprint the surrounding signatures at every location in the areas of interests and then build a fingerprint database. The location is then estimated by mapping the measured fingerprints against the database. Researchers have striven to exploit different signatures of the existing devices or reduce the mapping effort. Most of these techniques utilize the RF signals. An early system using these techniques is RADAR [4]. Horus [5], improved upon RADAR, employs a stochastic description of the RSSlocation relationship and uses a maximum likelihood based method to estimate locations. OIL [6] structures an organic indoor localization system by using Voronoi regions for conveying uncertainty and employing a clustering method for identifying potentially erroneous user data. Varshavsky et al. [7] demonstrate that GSM signals from various towers can also be used for indoor localization. PlaceLab [8] uses radio beacons to localize mobile devices in the wild. ActiveCampus [9] project adopts similar techniques but assumes availability of AP locations. Some systems, such as LANDMARC [10], utilize RFID for indoor localization. Recently, SurroundSense [11] performs logical location estimation based on ambience features including sound, light, color, WiFi, and etc. And [12], [13], [14] utilizes FM Radio, acoustic background spectrum (ABS) and geomagnetism, respectively, as fingerprints for indoor location estimation. All these approaches require site survey over areas of interests to build fingerprint database. The considerable manual cost and efforts, in addition to the inflexibility to environment dynamics are the main drawbacks of fingerprint-based methods.

Model-based techniques. Another type of localization approaches use geometrical models to figure out locations. In those methods, locations are calculated rather than searched from known reference data. For example, the log-distance path loss (LDPL) model is used to estimate RF propagation distances according to the measured RSS values. These approaches trade the measurement efforts at the cost of decreasing localization accuracy due to the irregular signal propagation in indoor environment. Lim et al. [15] deploy WiFi sniffers at known locations to measure the RSS from various APs and then uses the LDPL model to construct RSS map. Ji et al. [16] also employ sniffers at known locations but uses a more sophisticated ray-tracing model. Madigan et al. [17] use a Bayesian hierarchical model to avoid the need of locations of the training points. However, they still depend on knowledge of the AP locations. To cut down the laborious measurement efforts and avoid the use of AP locations, EZ [18] models the physics constrains of wireless propagation with LPDL model and uses a genetic algorithm to solve them for localization. However, EZ still relies on occasionally available GPS information at the entrance or near a window. Besides, EZ involves in complex computation and the physical localization scheme might result in lot of misdetections of rooms.

Other than the RSS related model, other geometric models are also exploited for characterizing the relationship of signal transmitters and receivers. These systems include PinPoint [19] based on Time of Arrival (ToA), Cricket [20] based on Time Difference of Arrival (TDoA), and VOR [21] based on Angle of Arrival (AoA). Model-based techniques usually require the placement of additional infrastructure, modifications of off-the-shelf products, or knowledge of hardware configuration.

Different from previous work relying on infrastructure and propagation model, WILL adopts the fingerprinting technique but avoids site survey. WILL users are not involved in any work of data collection.

# 3 OVERVIEW

# 3.1 Unexploited Potential for Localization

WiFi technology has shown its great potentials for ubiquitous localization as it is available in a large amount of buildings through personal electronic devices like mobile phones and laptops.

By investigating the temporal and spatial characteristics of indoor RF propagation of WiFi signals, we discover some easily overlooked but dramatically useful characteristics. A key observation is that signals may encounter a considerable drop while passing through a wall (as shown in Fig. 1). As a result, RSS of a same AP can vary significantly in two rooms. People have been observing this wall-penetrating effect of radio signals when using wireless routers in everyday life.

![](images/a05d65c41a02bec85ae311df5ed7cb6cc91016960c334bc99a340e4fbfb9eaa5.jpg)



Fig. 1. Abrupt signal changes through a wall. AP1 is deployed in Room I and AP2 in an adjacent Room II.

Such characteristic, however, has not been fully exploited for positioning. As shown in Fig. 1, this variation of AP signal strength can be used to distinguish different rooms.

On the other hand, smartphones integrate various types of sensors such as accelerometer, magnetometer, gyroscope, etc., offering new opportunities to capture environment signatures and to detect user behaviors. WILL exploits accelerometers to obtain user movements, which will be further utilized to assist localization. Tri-axial accelerometers provide apparent evidence of human walking patterns [22]. As illustrated in Fig. 2, the acceleration variation for walking users is clearly different from those static. Amplitude of about 2 $\mathrm { m } / \mathrm { s } ^ { 2 }$ is caused by foot lifting and around $\mathrm { 3 \ m / s ^ { 2 } }$ by foot down. This signature is deeply explored in WILL to detect user motions and collect user traces.

WILL provides human localization service through locating mobile phones. Even though mobile phones can integrate sensors like compasses, cameras, microphones, gyroscopes, WILL uses only accelerometers since no human participation is involved for such sensors. Moreover, different from many previous work using accelerometers for step counting or displacement estimation [22], [23], WILL utilizes accelerometer sensors to explore reachability between different areas.

# 3.2 System Architecture

In this section, we present the overall vision of WILL, as shown in Fig. 3. The working process of WILL consists of two phases: training and serving. We describe high level architecture and present the details later.

![](images/b13ec970bf6450ff053de0c6a184586a1ca65ba226d3bb6e7d431aa74b4c8221.jpg)



Fig. 2. Acceleration signatures of 10 steps (each step marked with a cross).

![](images/914b0929ee19c85b82f3d3f4aa9d1a28beffe2982f4fd9e67ae3cdf0d263e84a.jpg)



Fig. 3. WILL architecture.

During the training phase (database construction), users in a building work with routine business while their mobile phones automatically measure WiFi signal strengths and record accelerometer readings. Raw data are collected in the fingerprint collection module on the mobile phone side. All raw fingerprints (not tagged with a known location) are preprocessed in fingerprint processing module and divided into two types: space-continuous and space-discontinuous, according to users’ motion states when the fingerprints are measured. Both types of fingerprints are classified into different virtual rooms, which are virtual containers of fingerprints with high similarity. A logical floor plan showing a view of relative location relationship (e.g., connectivity and reachability) between virtual rooms is then constructed by leveraging user trace information from the spacecontinuous data, which connect previously independent fingerprints. Afterwards, the logical floor plan is mapped to a given ground truth one by using a novel mapping method. By doing so, we associate the isolated fingerprints with physical rooms. Floor plan database stores these associated relationships.

In the serving phase, when a user sends a location query with his/her currently measured data using mobile phone, WILL server will response the user with the estimated location. The query may contain a variety of information, including WiFi measurements and sensory data. The localization engine consults the fingerprint database to localize the virtual room and then obtains the corresponding physical room from floor plan database. The location estimation and, if possible, the floor plan that the user currently locates at are sent back to the user. The querying data can be simultaneously used as collected fingerprints to update the databases.

# 4 VIRTUAL ROOM GENERATION

In this section, we define virtual room and describe how to extract distinct features of fingerprints from raw data. Afterwards, we classify fingerprints into a number of virtual rooms.

# 4.1 Fingerprint Collection

WILL users do not need to deliberately collect data even during the database building phase. They just work in offices, consume in shopping malls, or have a rest at coffee shops, walking or sitting. The information of WiFi signals and sensor readings is collected automatically by their cell phones. A regular record can be represented as $D _ { t } =$ $< F , A > ,$ , where F and A indicate the WiFi signal fingerprint and accelerometer value, respectively. Assuming totally n APs in the building, the WiFi signals fingerprint F can be represented as

$$
F = [ f _ {1}, f _ {2}, \dots , f _ {n} ], \tag {1}
$$

where $f _ { i }$ denotes the RSS value of the ith AP.

The motion state of users, walking or staying, is determined by accelerometer readings. Records of a walking user are integrated as an entire user trace $\mathcal { U } = < \bar { \mathcal { F } } , \mathcal { A } > ,$ , where $\mathcal { F }$ is a set of RSS fingerprints and A a set of acceleration values. Such records are called spacecontinuous as they are measured during user’s movements. For ease of presentation, we refer to continuous data as space-continuous data in this paper hereafter.

Theoretically, the traveling distance of a user can be derived from the continuous data which contain accelerometer readings by integrating acceleration twice with respect to time. However, due to the presence of noise in the sensor readings, error accumulates rapidly and can reach up to 100 meters after one minute of operation [22]. To avoid accumulation of measurement errors, most researchers adopt the individual step counts for estimating walking distance, just like a pedometer [23]. Different from previous work, in WILL, it is unnecessary to estimate displacement or accumulate step counts of mobile users. The continuous data are merely used to detect user mobility, i.e., to detect whether a user is mobile or static. We modify the local variance threshold method [23] to detect user footstep only, instead of step counts. The method is based on filtering the magnitude of acceleration followed by applying a threshold on the variance of acceleration over a sliding window. Note that a filter has been applied to smooth the raw sensor data because measurement errors as well as signal fluctuations exist. We omit the details here due to space limitation.

# 4.2 Fingerprint Processing

As can be seen from Fig. 1, the absolute RSS values of each individual AP vary widely over time (even at a fix location) while the difference relationship between them maintains. Consequently, it is inadequate to utilize absolute RSS values directly for location estimation like conventional work. In contrast, the difference relationship among different APs is exploited for fingerprint feature. In this work, we propose the RSS stacking difference, which means the cumulative difference between one AP and all other APs. RSS stacking difference embodies the RSS gap relations of the RSS fingerprint at a specific time and location and tends to be a relatively stable feature of radio signals than absolute RSS values.

Formally, given two fingerprints $F = [ f _ { 1 } , f _ { 2 } , \dots , f _ { n } ]$ and $F ^ { \prime } = [ f _ { 1 } ^ { \prime } , f _ { 2 } ^ { \prime } , \ldots , f _ { n } ^ { \prime } ] .$ , the dissimilarity (euclidean distance) between them using feature of RSS stacking difference can be calculated by the following formulae:

$$
\phi (F, F ^ {\prime}) = \sqrt {\sum_ {i = 1} ^ {n} \left(\omega (f _ {i}) - \omega (f _ {i} ^ {\prime})\right) ^ {2}} \tag {2}
$$

$$
\omega (f _ {i}) = \sum_ {j = 1} ^ {n} I (f _ {i} - f _ {j} > 0) (f _ {i} - f _ {j}), \tag {3}
$$

where I is an indicative function.

# 4.3 Virtual Rooms

Fingerprints are partitioned into different virtual rooms according to the values of RSS stacking difference. A virtual room is a virtual container which consists of the fingerprints with high similarity. Formally, if $\phi ( F _ { 1 } , F _ { 2 } ) < \xi , \ F _ { 1 }$ and $F _ { 2 }$ are treated to be in the same virtual room, where  is a dissimilarity threshold of the room.

Virtual rooms are generated by applying data mining approaches on fingerprints. We adopt several clustering techniques, including KMeans, FarthestFirst, EM, and FilteredCluster, which are implemented in WEKA, a popular classification and clustering tool. Among different techniques, KMeans demonstrates its high accuracy and efficiency for this application. Generally, the virtual room number (or the cluster number k) can be automatically set equal to the zone number in the physical floor plan in practice. Detailed results of performance comparison are shown in Fig. 8. After virtual room generated, each fingerprint is tagged with a virtual room label which it belongs to. In addition, each virtual room R is marked with a representative fingerprint F ½R- for fast location estimation (See Section 6). This representative fingerprint, along with the dissimilarity threshold , is dynamically determined and updated in the fingerprint database. In addition, both parameters are room specific, namely, each room has a distinct value for each parameter.

# 5 FLOOR PLAN CONSTRUCTION

Without site survey, the key challenge of localization is how to associate the fingerprints with their locations. In this section, we provide a matching based technique to find a mapping relation between logical floor plan of generated virtual rooms and the ground truth one, which then tells the correspondence of fingerprints and their measured locations.

# 5.1 Logical Floor Plan

Conventional work mostly focuses on a single location or a single room. The relationship of different rooms have not been sufficiently excavated. In WILL, traces of user’s motion indicate the reachability among virtual rooms, which is used to construct the logical floor plan of virtual rooms.

A logical floor plan is a diagram showing the view of the reachability among virtual rooms. It is formalized as an undirected graph $\overset { \vartriangle } { \boldsymbol { P } } = ( \boldsymbol { V } , \boldsymbol { E } )$ , namely, the logical graph, where each vertex v 2 V denotes a virtual room and an edge $( u , v ) \in E$ indicates that virtual room u and v are reachable from each other. We observed that user movements inside a building, from one room to another or through the corridors, might indicate the connectivity between rooms. Two rooms are referred to be connected in logical floor plan if and only if a user can walk seamlessly from one to the other without passing through any other room. For ease of understanding, we take an example in the ground truth floor plan (as shown in Fig. 4). If a user walks from room A to room B through a corridor segment

![](images/d3dd2ac0c51aa893a3c3e74a866cd697e54a3b7fe58182304a13f3526d5045e5.jpg)



Fig. 4. Examples of user traces through the building.

C, then it can be derived that C is reachable from both A and B, but A is not directly connected to B on only this condition. We assume that reachability is bidirectional, namely, if room A is reachable from room $\scriptstyle \mathrm { \mathrm { B } , }$ then B is also considered reachable from A.

A series of fingerprints can be collected during users’ movements. As fingerprints are labeled with virtual rooms, an entire trace may traverse different virtual rooms. In addition, the sequence of the virtual rooms being traversed can be obtained because the trace is time stamped and ordered.

Concretely, we consider a single user trace $\mathcal { U } = < \mathcal { F } , \mathcal { A } >$ where $\mathcal { F } = [ F _ { 1 } , F _ { 2 } , \ldots , F _ { m } ]$ and $\overset { \vartriangle } { \mathcal { A } } = [ A _ { 1 } , A _ { 2 } , \ldots , A _ { m } ]$ indicate a sequence of m fingerprints and acceleration readings collected during the user’s movement. Each $F _ { i }$ belongs to a virtual room $R _ { i } .$ Thus F corresponds to a series of virtual rooms $R = [ R _ { 1 } , R _ { 2 } , \ldots , R _ { m } ]$ . Accordingly, the reachability between virtual rooms can be obtained by following rule: if $R _ { i } \neq R _ { i + 1 } ,$ which means the user walks into virtual room $R _ { i + 1 }$ from $R _ { i } ,$ then $R _ { i }$ and $R _ { i + 1 }$ is marked to be reachable to each other. In other words, an edge $( R _ { i } , R _ { i + 1 } )$ is added to the logical floor plan P if $( R _ { i } , R _ { i + 1 } ) \notin E$ . Fusing a large amount of user traces together, the logical floor plan P is constructed.

There is a key problem about how to construct user traces when user behavior is unknown and unconstrained. User motions may be irregular, intermittent and convoluted, making it hard to select valuable and reliable traces from large quantity of raw measurements. Nonetheless, the more favored long-distance and relatively straight traces can be picked out basing on the distinctive sensor readings and WiFi signal features. We defer to the following two simple but effective principles for trace selection:

Traces with very few steps are dumped.   
Traces passing through less than two APs are abandoned.

The first principle ensures the user is walking, where the steps are approximately counted by the accelerometer readings along with the trace. The second implies the user’s location is changing, namely, the user is walking rather than shaking the phone or pacing back and forth in a small area. The second principle is according to the observation that RSS values are relatively similar at close locations but change dramatically with distant locations, especially when the locations are separated by walls or other obstructions. The number of APs passed by a trace is determined by the AP peaks appeared within the trace. An AP peak is an RSS value which is the maximum signal strength of this AP during a trace and is at least higher than a significance level, for instance, 2/3 of the maximum RSS value indicated in the database.

![](images/d199c6fe9016763c6e300fdd66606e6dcf1cec2c6176e8e58829ff5f4cef99ae.jpg)



Fig. 5. Floor plan of the building in Tsinghua University. APs with unknown locations are not marked.

# 5.2 Floor Plan Mapping

Logical floor plan needs to be mapped to the ground truth floor plan, which is available to the estate manager of a building who is also supposed to be the provider of location services in this building. For convenience, the ground truth floor plan is also referred to physical floor plan hereafter.

The physical floor plan is modeled with an undirected graph $\hat { \boldsymbol { P } } ^ { \prime } = ( \boldsymbol { V } ^ { \prime } , \boldsymbol { E } ^ { \prime } )$ , i.e., the physical graph, where each vertex $v \in V ^ { \prime }$ indicates a room (or a functional area) and each edge $( u , v ) \in E ^ { \prime }$ means the reachability of two rooms u and v. Under this scheme, the corridors are connected to most rooms while the adjacent rooms are not connected if no door exists between them. In the physical floor plan, a corridor can be divided into several segments, mainly according to the rooms’ corresponding areas in the corridor. Specifically, one corridor segment corresponding to a room is usually cut as an area, which then becomes a vertex in physical graph (as seen from Fig. 5). Hence, length of each segment is roughly in line with that of the largest room it connects. The modeled physical floor plan of our experiments is shown in Fig. 6, where the corridor is segmented into four parts. Given the logical floor plan $P = ( V , E )$ and the ground truth floor plan $\breve { P ^ { \prime } } = ( V ^ { \prime } , E ^ { \prime } )$ , we define the floor plan mapping as a function $p : V { \mapsto } V ^ { \prime }$ . In WILL, we set the numbers of virtual rooms to equal to or more than the number of physical areas, $\operatorname { i . e . , } | V | \leq | V ^ { \prime } |$ .

We propose a subsection mapping method (SSMM) which contains three stages: skeleton mapping, branch-knot mapping, and the correction. The virtual rooms with higher betweenness are in prior mapped in skeleton mapping while the rest are mapped using bipartite matching in branch-knot mapping. The initial mapping results are adjusted in the correction stage. Because of space limitation, we only present the brief framework here. For details of the mapping algorithm, readers are referred to [24] and [25].

Skeleton mapping. Betweenness centrality [26] is a measure of a vertex’s centrality within a graph. Vertices that occur on many shortest paths between other vertices have higher betweenness than those do not. As shown in Fig. 6, the vertices in the center (labeled C1, C2, C3, and C4) apparently have higher betweenness than others. Based on this observation, vertices which have the highest betweenness in P are mapped to those with highest betweenness in $P ^ { \prime }$ . Here, the mapping goal is to minimizing the total difference of betweenness for all matching pairs.

![](images/b1091c46d97f729f0900d4d3726da9c615b4339f681e5b4f0b0bfc0ca1830b69.jpg)



Fig. 6. Physical floor plan graph. Vertices with $" Z '$ denote rooms and $" C "$ denote corridor segments.

Branch-knot mapping. The rest of vertices in $P$ are mapped using the sum of shortest paths length as weights. In other words, for each vertex v in graph $P ,$ its weight $w ( v )$ equals to the sum of all shortest path lengths from v to all other vertices in $P ,$ namely, $\begin{array} { r } { w ( v ) = \sum _ { u \in P , u \neq v } d ( v , u ) } \end{array}$ where $d ( v , u )$ is the length of the shortest path from v to u. The weight of each vertex in $P ^ { \prime }$ is calculated in the same way. Then, the mapping goal is to minimize the total weight difference, say, $\begin{array} { r } { \dot { W ( p ) } = \sum _ { v \in V } | w ( v ) - w ( p ( v ) ) | } \end{array}$ .

We formalize the branch-knot mapping as a weighted minimum bipartite matching (WMBM) problem where every vertex in P is matched to another vertex in $P ^ { \prime } ,$ , resulting in a perfect matching. The WMBM problem is then performed using the Kuhn-Munkras (KM) [27] algorithm.

Combining the result of skeleton mapping and branchknot mapping, an original mapping is obtained. Figs. 10a and 10b show the result of skeleton mapping and branchknot mapping, respectively. Evident from Fig. 10, mapping errors could exist in the initial mapping result. We perform the correction stage of SSMM to fix some error mapping.

Correction. Redundant information in the initial mapping result is utilized for correction. By comparing the neighboring set of every skeleton vertex, error mapping can be figured out and corrected. The basic idea is: 1) if a pair of mapped skeleton vertices have very different neighboring sets, they tends to be an error link; 2) if two branch-knot vertices do not belong to a pair of mapped skeleton vertices, they are likely to be mistakenly mapped. Please refer to [25] for more detail algorithm descriptions. The corrected results of SSMM in our experiments are depicted in Fig. 10c.

# 6 LOCALIZATION USING WILL

We have constructed the fingerprint database and the floor plan database during the training phase of WILL. The association between these two databases is established as well. In this section, we present the entire working process of WILL when it receives location queries, which corresponds to the localization engine module in WILL system.

# 6.1 Localization

Recall Section 4, we mark each virtual room R with a representative fingerprint $F [ R ]$ after they are generated from the fingerprints. We use the mean value of all fingerprints in virtual room R as $F [ R ]$ . Formally, $F [ R ]$ can be calculated by the following formulas:

$$
F [ R ] = \frac {1}{| \mathcal {F} _ {R} |} \sum_ {F _ {i} \in \mathcal {F} _ {R}} F _ {i}, \tag {4}
$$

where $\mathcal { F } _ { R }$ is the set of fingerprints that belong to R

When one user visits a building where WILL is deployed, he/she queries WILL server for his/her current location with a record $D _ { t } = < F , A >$ , where t is the time stamp, F and A indicate WiFi signals and accelerometer values, respectively. The localization engine of WILL first determines the virtual room F belongs to, and then consults the floor plan database to obtain the mapped physical room, which is the response to be sent back to the user. $F$ is estimated to be in the virtual room which has the shortest distance to $F$ among all virtual rooms. Formally, F belongs to virtual room $R _ { i }$ if the dissimilarity of F and $\dot { F } [ R _ { i } ]$ satisfies

$$
\phi (F, F [ R _ {i} ]) = \min \{\phi (F, F [ R _ {j} ]), R _ {j} \in \mathcal {R} \}, \tag {5}
$$

and

$$
\phi (F, F [ R _ {i} ]) <   \xi , \tag {6}
$$

where - is the dissimilarity defined by (2), R is the set of all virtual rooms, and  denotes the dissimilarity threshold of rooms. Fingerprints beyond above two equations are treated as outliers and discarded. Assuming that virtual room $R _ { i }$ is mapped to a physical area $R _ { i } ^ { \prime } ,$ the user location is estimated as zone $R _ { i } ^ { \prime }$ and the result is sent back to the user with, if possible, the floor plan.

We design the localization engine as lightweight as possible for the purpose of better user experience on mobile phones and making WILL easily scalable.

# 6.2 Database Update

The floor plan and the fingerprint database should be updated over time to capture environment dynamics and to remedy fingerprint deviations as the data collected in the training phase of WILL might not roundly reflect the overall situation of the building. We execute two types of update operations in WILL: minor update and major update.

Minor update, being triggered frequently, deals with newly collected fingerprints. When user queries arrive, the attached fingerprints are not only used for localization, but also for updating virtual room features, including the representative fingerprints and dissimilarity thresholds.

Major update is carried out occasionally for a large amount of new data, resulting in large modifications in the previous database. For instance, if huge data are collected through a long-term running, especially when enough continuous data are included, the floor plan is refreshed using the updated logical floor plan.

# 7 EXPERIMENTS

# 7.1 Experimental Methodology

We developed the client of WILL on the increasingly popular Android OS. WiFi signals are recorded with the frequency of around twice per second when measuring. Accelerometers work in two frequencies: when detecting motions, they record sensory data with short intervals of 50 milliseconds; otherwise a relatively long interval of one second is adopted.

We implemented our prototype on two Google Nexus S phones, which support WiFi and contain accelerometer sensors. We deployed WILL system in one floor of an office building covering over 1600 $\mathrm { { m ^ { 2 } } }$ in Tsinghua University, which contains 16 offices, of which five are large rooms of 142 m2, seven are small ones with different sizes and the other four are inaccessible. The floor plan is shown in Fig. 5, where every physical zone is marked with a sequence number. Most rooms are installed with one or more APs while some have none. Totally, n ¼ 26 APs are installed in the floor, of which 20 are with known locations and are marked in Fig. 5. Note that the walls of the experimental building are constituted by only steel keels wrapped in two wooden clapboards instead of reinforced concrete, which reduces the walls’ shielding effects of wireless signals to a certain extent.

![](images/36ba8c1f6e182b488ab659207f47c930d2e018821e38d6cb31fe9cc17ed62fc5.jpg)



Fig. 7. Accuracy of virtual room generation using RSS stacking difference versus raw fingerprints.

Fig. 5 depicts the ground-truth floor plan, where the black triangles indicate physical functional zones and the edges show their connected relationships. In our evaluation, each physical room is modeled with a vertex while the corridor is divided into 4 segments. As a result, there are total 16 functional zones in the physical graph.

To evaluate WILL, we need the accurate room of each user when the location query is submitted. We require location samples, especially those close to the walls, to evaluate the localization performance. To obtain these location-labeled data, we set a data acquisition point every $4 \mathrm m ^ { 2 }$ and have some volunteers move around the space, stopping regularly to take 30 measurements and manually recording the ground truth locations. The data records for evaluation are extended to be $D _ { t } = < F , A , L >$ where L is an additional tuple, location. We collected 16,336 records (data set #1) on one phone and 14,271 records (data set #2) on another. All data are evenly collected from accessible areas in the floor.

Space-continuous data, say, the mobility data collected during user movements, consist of two parts in our experiments. One part are collected from real user traces, the other are generated from the discontinuous data. To collect continuous data, volunteers, as normal users with a mobile phone in hand, walk naturally in the building and collect traces and fingerprints during their natural movements. WILL records the accelerometer readings and picks up RSS values during moving with a, respectively, proper period. Totally, 30 real traces are extracted and additional 118 traces are generated from those location-labeled data. Different traces have various lengths and cover different areas of interests. Note that the generated traces are also realistic because the experimental data contain manually labeled accurate location information.

# 7.2 Performance

In this section, we evaluate WILL using data set #1 as training data for building databases and data set #2 as querying data to localize.

# 7.2.1 User Trace Detection

Though the users kept their mobile phones in hand when collecting continuous data in our experiments, we find that the rhythmic acceleration signatures in human walking patterns are evident no matter what postures the mobile phones are. As observed in the experiments, although the most remarkable acceleration variation caused by walking appears on different axes, the triaxial accelerometer captures rhythmic fluctuations finely whenever the mobile phone is placed horizontally in hand, sideways up, or vertically held. In addition, as WILL detects user mobility instead of user displacement or step counts, WILL avoids the accumulate error caused by noisy sensor measurements.

![](images/53c240e7f3747192f2677c67a408eacb67ebcbba7365aa53d2b609987acaef78.jpg)



Fig. 8. Assignment error with virtual room number (using KMeans).

# 7.2.2 Virtual Room Generation

For all virtual rooms, we mark each of them with the label of a physical zone where the largest portion of fingerprints within this virtual room are collected. The assignment error rate (AE) is used for evaluation of virtual room generation, which is referred to the percent of fingerprints tagged with those virtual rooms taking a physical zone label different from the zone where the fingerprints are actually collected.

As illustrated in Fig. 7, we notice that all clustering approaches can achieve a fairly good accuracy of over 80 percent on virtual rooms. Particularly, the KMeans approach can reach an accuracy of 93 percent when the virtual room number is set to 16 (equal to the physical functional zones number), which outperforms the best performance achieved by SurroundSense [11], a mobile phone localization system using many kinds of fingerprints relying on site survey. We are delighted even more that such improvement is made while fewer kinds of fingerprints (actually only WiFi here) are involved. The results benefit from the proposed feature of RSS stacking difference and the concept of virtual room. Fig. 7 further shows that partitional clustering approaches (KMeans) achieve better performance than others like density-based clustering (EM) and hierarchical clustering methods (FarthestFirst).

Both physical rooms and corridor segments can be partitioned well. Moreover, even two connected areas totally without APs installed in (e.g., two adjacent corridor zones) can also be distinguished by RSS data. As shown in Fig. 8, AE of partition on physical rooms is lower than 9 percent. As expected, partition on corridor segments is less accurate. Nevertheless, the error is smaller than 19 percent, which we think is acceptable as fingerprints in corridors are farraginous. Moreover, there are no walls or other obstructions between corridor segments, which enlarges the fingerprint similarities between different corridor segments.

It is also indicated that some virtual rooms may be indistinguishable. As illustrated in Fig. 9, when virtual room number increases, we observe that AE caused by some specific rooms always keep relatively large. On the other hand, the special building structure and materials of the building, as described above, add to the difficulty of distinguishing rooms, which results in larger AE. We believe WILL would work better in typical modern buildings with walls of reinforced cement.

![](images/75b295c01441221232666292ad4a1310eee5ba5062f922a2d67e97f4da77a353.jpg)



Fig. 9. Assignment error caused by different rooms. Rooms causing no AE are not indicated.

# 7.2.3 Localization Accuracy

The final localization accuracy is affected by two factors: the virtual room estimation accuracy and the floor plan mapping results. We present the mapping results and evaluate the ultimate localization performance using accuracy of virtual room localization (VRL) and physical room localization (PRL) in the following.

We use the virtual room results generated by KMeans with virtual room number of 16 for evaluation. The original results of the proposed SSMM on the logical and physical graphs are displayed in Figs. 10a and 10b. Some of the mapping errors are corrected in the correction stage of SSMM, as shown in Fig. 10c. There are two virtual rooms marked with the same physical room label and mapped to a same physical room. As a result, one room in the physical floor plan is not mapped with any virtual rooms. In other words, 15 out of 16 virtual rooms are correctly mapped while totally 14 out of 16 physical rooms are mapped.

We evaluate the location estimation accuracy based on the mapping result illustrated in Fig. 10c. To understand the localization accuracy of each room, we plot the cumulative distribution function (CDF) in Fig. 11. Seventy five percent of physical rooms can achieve localization accuracy of 80 percent or more. The median accuracies of VRL and PRL are 89 and 90 percent and the average accuracies of them are 81 and 86 percent, respectively. Such encouraging results show competitive performance of WILL comparing with traditional site survey-based methods.

![](images/c4a648ada181c10d0c212bd291b1628af0d63c374c64555d9a24ac2bf0748b75.jpg)



Fig. 11. CDF of per room accuracy.

# 7.2.4 Comparative Study

We compare WILL with some recent competitive techniques, specially, SurroundSense [11] and EZ [18] , in terms of complexity and accuracy. SurroundSense utilizes ambience features, including WiFi signals, accelerometer, camera sound, light, and even color, for indoor localization. It is a pervasive work exploring logical localization and opens new possibilities for indoor localization. SurroundSense achieves an encouraging average accuracy of 87 percent, which is almost the same as WILL. SurroundSense, however, relies on site survey and needs user-aware participation in localization, which makes it labor intensive and deployment expensive. Moreover, SurroundSense is inefficient in energy and computation cost as so many features are used.

EZ in [18] performs indoor physical localization with no pre-deployment efforts. EZ models the physical constraints of wireless propagation of all observations and uses a genetic algorithm to solve them. EZ yields a median localization error of 2 and 7 m, respectively, in a small and a large building. Nonetheless, EZ falls short of distinguishing physical rooms. In other words, the claimed median 7 m error of EZ might imply lot of misdetections of rooms, which is where WILL stands out. In addition, EZ relies on occasionally available GPS information at the entrance or near a window.

# 8 CONCLUSION

Previous indoor localization approaches mostly rely on laborintensive site survey over every location. In this paper, we presented WILL, an indoor logical localization approach without site survey or knowledge of AP locations and power settings. The main idea is to combine WiFi fingerprints with user movements. Fingerprints are partitioned into different virtual rooms and a logical floor plan is accordingly constructed. Localization is achieved by finding a matching between logical and ground-truth floor plan. We implement WILL in a typical office building and it achieves an average room-level accuracy of 86 percent, which is competitive to existing designs. We believe WILL demonstrates its advantage on low human cost, a long standing and universal will in wireless indoor localization. Future research in physical floor plan construction, sophisticated floor plan mapping as well as user behavior detection should make WILL a ubiquitous indoor positioning system.

![](images/6fa9acdba46d8e913a2ef84960e7a330bfe460541b9e42013878b148c4f92646.jpg)



(a) SSMM stage 1: skeleton mapping.

![](images/215207bfb2f9e90c3726185deda8a447ce26a8d5dc27cd12965b24fa9e69590c.jpg)



(b) SSMM stage 2: branch-knot mapping.

![](images/da1444dcfece6e811967aa18acb2708e4ed564fb8b83fc9dc3ad3e8d20ffa8a2.jpg)



(c) UItimate result of SSMM.   
Fig. 10. Floor plan mapping. Vertices colored the same indicate ground truth mapping pairs.

# ACKNOWLEDGMENTS

This work is supported in part by the NSFC Major Program under grant 61190110, NSFC under grant 61171067, 61133016, and 61272466, National High-Tech R&D Program of China (863) under grant No. 2011AA010100, National Basic Research Program of China (973) under grant No. 2012CB316200, and the NSFC Distinguished Young Scholars Program under Grant 61125202.

# REFERENCES

[1] X. Wang, L. Fu, and C. Hu, “Multicast Performance with Hierarchical Cooperation,” IEEE/ACM Trans. Networking, vol. 20, no. 3, pp. 917-930, June 2012.   
[2] Z. Yang, Y. Liu, and X.-Y. Li, “Beyond Trilateration: On the Localizability of Wireless Ad Hoc Networks,” IEEE/ACM Trans. Networking, vol. 18, no. 6, pp. 1806-1814, Dec. 2010.   
[3] B. Xiao, H. Chen, and S. Zhou, “Distributed Localization Using a Moving Beacon in Wireless Sensor Networks,” IEEE Trans. Parallel Distributed Systems, vol. 19, no. 5, pp. 587-600, May 2008.   
[4] P. Bahl and V.N. Padmanabhan, “RADAR: An In-Building RF-Based User Location and Tracking System,” Proc. IEEE INFOCOM, vol. 2, pp. 775-784, 2000.   
[5] M. Youssef and A. Agrawala, “The Horus WLAN Location Determination System,” Proc. Third Int’l Conf. Mobile Systems, Applications, and Services, pp. 205-218, 2005.   
[6] J. Park, B. Charrow, D. Curtis, J. Battat, E. Minkov, J. Hicks, S. Teller, and J. Ledlie, “Growing an Organic Indoor Location System,” Proc. Eighth Int’l Conf. Mobile Systems, Applications, and Services, pp. 271-284, 2010.   
[7] A. Varshavsky, E. de Lara, J. Hightower, A. LaMarca, and V. Otsason, “GSM Indoor Localization,” Proc. IEEE Fifth Ann. Conf. Pervasive Computing and Comm., vol. 3, no. 6, pp. 698-720, 2007.   
[8] A. LaMarca et al., “Place Lab: Device Positioning Using Radio Beacons in the Wild,” Proc. Third Int’l Conf. Pervasive Computing, pp. 301-306, 2005.   
[9] W.G. Griswold, P. Shanahan, S.W. Brown, R. Boyer, M. Ratto, R.B. Shapiro, and T.M. Truong, “ActiveCampus: Experiments in Community-Oriented Ubiquitous Computing,” Computer, vol. 37, no. 10, pp. 73-81, Oct. 2004.   
[10] L.M. Ni, Y. Liu, Y.C. Lau, and A.P. Patil, “LANDMARC: Indoor Location Sensing Using Active RFID,” Wireless Networks, vol. 10, no. 6, pp. 701-710, 2004.   
[11] M. Azizyan, I. Constandache, and R.R. Choudhury, “Surround-Sense: Mobile Phone Localization via Ambience Fingerprinting,” Proc. 15th Ann. Int’l Conf. Mobile Computing and Networking, pp. 261-272, 2009.   
[12] A. Matic, A. Papliatseyeu, V. Osmani, and O. Mayora-Ibarra, “Tuning to Your Position: FM Radio Based Indoor Localization with Spontaneous Recalibration,” Proc. IEEE Int’l Conf. Pervasive Computing and Comm. (PerCom), pp. 153-161, Apr. 2010.   
[13] S.P. Tarzia, P.A. Dinda, R.P. Dick, and G. Memik, “Indoor Localization without Infrastructure Using the Acoustic Background Spectrum,” Proc. Ninth Int’l Conf. Mobile Systems, Applications, and Services (MobiSys ’11), pp. 155-168, 2011.   
[14] J. Chung, M. Donahoe, C. Schmandt, I. Kim, P. Razavai, and M. Wiseman, “Indoor Location Sensing Using Geo-Magnetism,” Proc. Ninth Int’l Conf. Mobile Systems, Applications, and Services (MobiSys ’11), pp. 141-154, 2011.

[15] H. Lim, L.C. Kung, J.C. Hou, and H. Luo, “Zero-Configuration Indoor Localization over IEEE 802.11 Wireless Infrastructure,” Wireless Networks, vol. 16, no. 2, pp. 405-420, Feb. 2010.   
[16] Y. Ji, S. Biaz, S. Pandey, and P. Agrawal, “ARIADNE: A Dynamic Indoor Signal Map Construction and Localization System,” Proc. Fourth Int’l Conf. Mobile Systems, Applications and Services, pp. 151- 164, 2006.   
[17] D. Madigan, E. Einahrawy, R.P. Martin, W.H. Ju, P. Krishnan, and A.S. Krishnakumar, “Bayesian Indoor Positioning Systems,” Proc. IEEE CS INFOCOM, vol. 2, pp. 1217-1227, 2005.   
[18] K. Chintalapudi, A. Padmanabha Iyer, and V.N. Padmanabhan, “Indoor Localization without the Pain,” Proc. 16th Ann. Int’l Conf. Mobile Computing and Networking, pp. 173-184, 2010.   
[19] M. Youssef, A. Youssef, C. Rieger, U. Shankar, and A. Agrawala, “Pinpoint: An Asynchronous Time-Based Location Determination System,” Proc. Fourth Int’l Conf. Mobile Systems, Applications and Services, pp. 165-176, 2006.   
[20] N.B. Priyantha, A. Chakraborty, and H. Balakrishnan, “The Cricket Location-Support System,” Proc. Sixth Ann. Int’l Conf. Mobile Computing and Networking, pp. 32-43, 2000.   
[21] D. Niculescu and B. Nath, “VOR Base Stations for Indoor 802.11 Positioning,” Proc. 10th Ann. Int’l Conf. Mobile Computing and Networking, pp. 58-69, 2004.   
[22] O. Woodman and R. Harle, “Pedestrian Localisation for Indoor Environments,” Proc. 10th Int’l Conf. Ubiquitous Computing, pp. 114-123, 2008.   
[23] A. Jime´nez, F. Seco, C. Prieto, and J. Guevara, “A Comparison of Pedestrian Dead-Reckoning Algorithms Using a Low-Cost MEMS IMU,” Proc. IEEE Int’l Symp. Intelligent Signal Processing (WISP ’09), pp. 37-42, 2009.   
[24] C. Wu, Z. Yang, Y. Liu, and W. Xi, “Site-Survey-Free Wireless Localization Using Mobile Phones,” technical report, Hong Kong Univ. Science and Technology, 2011.   
[25] C. Wu, Z. Yang, Y. Liu, and W. Xi, “WILL: Wireless Indoor Localization without Site Survey,” Proc. IEEE INFOCOM ’12, pp. 64-72, Mar. 2012.   
[26] L.C. Freeman, “A Set of Measures of Centrality Based on Betweenness,” Sociometry, vol. 40, pp. 35-41, 1977.   
[27] J. Munkres, “Algorithms for the Assignment and Transportation Problems,” J. Soc. for Industrial and Applied Math., vol. 5, pp. 32-38, 1957.

![](images/7c870cbbcd054a0ac710f273c254fe3db5f0d527b0e0f5a66ad1973e0005a0a7.jpg)



Chenshu Wu received the BE degree from School of Software from Tsinghua University, Beijing, China, in 2010, and is currently working toward the PhD degree in the Department of Computer Science and Technology, Tsinghua University. His research interests include wireless ad-hoc/sensor networks and mobile computing. He is a student member of the IEEE and ACM.

![](images/7a6bec5e48032203a2c0849af1a87239d69bd9516a6e6cd08ee57ae0420c16ad.jpg)



Zheng Yang received the BE degree in computer science from Tsinghua University in 2006 and the PhD degree in computer science from Hong Kong University of Science and Technology in 2010. His main research interests include wireless ad hoc/sensor networks and mobile computing. He is a member of the IEEE and the ACM.

![](images/f8ab4f7a763a8f952af02112f6cc7281802b16364f68810046c3f7d20528cb6b.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is now an EMC chair professor at Tsinghua University, as well as a faculty member with the Hong Kong University of Science and Technology. His research interests include wireless sensor network, peer-to-peer computing, and pervasive

computing. He is a senior member of the IEEE.

![](images/12ff52fb1a31324217548164a98369ef77f32a6751f0e8351ca6daaede39439e.jpg)



Wei Xi received the BE degree from School of Computer Science and Technology from Xidian University, Xi’an, China, and is currently working toward the PhD degree of Xi’an Jiaotong University. His research interests include wireless sensor networks and mobile computing. He is a student member of the IEEE and ACM.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.