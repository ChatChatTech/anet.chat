# Incentives for Mobile Crowd Sensing: A Survey

Xinglin Zhang, Student Member, IEEE, Zheng Yang, Member, IEEE, Wei Sun, Student Member, IEEE, Yunhao Liu, Fellow, IEEE, Shaohua Tang, Member, IEEE, Kai Xing, Member, IEEE, and Xufei Mao, Member, IEEE,

Abstract—Recent years have witnessed the fast proliferation of mobile devices (e.g., smartphones and wearable devices) in people’s lives. In addition, these devices possess powerful computation and communication capabilities, and are equipped with various built-in functional sensors. The large quantity and advanced functionalities of mobile devices have created a new interface between human beings and environments. Many mobile crowd sensing applications have thus been designed, which recruit normal users to contribute their resources for sensing tasks. To guarantee good performance of such applications, it’s essential to recruit sufficient participants. Thus, how to effectively and efficiently motivate normal users draws growing attention in the research community.

This paper surveys diverse strategies that are proposed in the literature to provide incentives for stimulating users to participate in mobile crowd sensing applications. The incentives are divided into three categories: entertainment, service, and money. Entertainment means that sensing tasks are turned into playable games in order to attract participants. Incentives of service exchanging are inspired by the principle of mutual benefits. Monetary incentives give participants payments for their contributions. We describe literature works of each type comprehensively and summarize them in a compact form. Further challenges and promising future directions concerning incentive mechanism design are also discussed.

Index Terms—Crowd Sensing, Incentive Mechanisms, Reverse Auction

# I. INTRODUCTION

The market of hand-held mobile devices (e.g., smartphones and wearable devices) is proliferating rapidly in recent years. These devices possess powerful computation and communication capabilities, and are equipped with various functional built-in sensors. Along with users round-the-clock, mobile devices have become an important information interface between users and environments. These advances have enabled and stimulated the development of mobile sensing technologies [1–5], among which mobile crowd sensing catches more and more attention owing to its capability of completing complex social and geographical sensing applications.

X. Zhang and S. Tang are with the School of Computer Science and Engineering, South China University of Technology, Guangzhou, P.R. China. X. Zhang was also a research associate at School of Software, Tsinghua University during this study. E-mail: zhxlinse@gmail.com, shtang@ieee.org.   
Z. Yang, Y. Liu, and X. Mao are with the School of Software and TNLIST, Tsinghua University, Beijing, P. R. China. E-mail: yang@greenorbs.com, yunhao@greenorbs.com, xufei.mao@gmail.com.   
W. Sun is with the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong. E-mail: sunw1989@gmail.com.   
K. Xing is with the School of Computer Science and Technology, and the Suzhou Institute for Advanced Study, University of Science and Techonology of China, China. E-mail: kxing@ustc.edu.cn.

Mobile crowd sensing [3] requires large amounts of participants (e.g., normal smartphone users) to sense the surrounding environment via rich built-in sensors of mobile devices, including accelerometer, gyroscope, compass, microphone, camera, GPS, and wireless network interfaces. These sensors are able to record various information about the participants (e.g., mobilities and locations) and the environment (e.g., images and sounds). By fusing and analyzing the multidimensional information, it is possible to facilitate the development of health caring, environment monitoring, traffic monitoring, social behavior monitoring, etc. In this sense, mobile crowd sensing provides a new perspective of our life and society. Pioneer sensing systems include NoiseTube [6] for noise monitoring, SignalGuru [7] and VTrack [8] for traffic monitoring, CityExplorer [9], SmartTrace [10], Sensorly [11] for 3G/WiFi discovery, and LiFS [12] and TrMCD [13] for indoor localization. We refer interested readers to a thorough survey of such mobile sensing systems in [2].

The power of the aforementioned sensing systems relies heavily on the quantity of participants. However, ordinary individuals are reluctant to participate and share their sensing capabilities due to the lack of sufficient incentives. Indeed, participating in the sensing systems may incur costs and risks. For example, when a smartphone user participate in a sensor data collection task, it is inevitable that the task consumes multiple resources of the smartphone, including computation, communication, and energy. In addition, the collected data usually contains location information, which makes the users who are sensitive to privacy feel uncomfortable. Therefore, it is conceivable that ordinary individuals will not participate in sensing tasks, unless they are sufficiently motivated.

In this survey, we review effective incentives that motivate normal users with mobile devices to participate in crowd sensing tasks from three categories: entertainment, service, and money. Most incentives adopted in current works fit in one of these categories. Each type of the incentives emphasizes some aspects of user needs, such as enjoyment, comfort, fulfillment, and making a profit. The brief descriptions of the three incentive categories are as follows:

• To make entertainment an incentive, crowd sensing tasks are turned into sensing games, such that users can contribute computation or sensing abilities of their mobile devices when they play these games. This paradigm makes users feel enjoyable when they perform tasks, but it has to guarantee that the designed sensing games are interesting enough.   
• The rationality of taking service as an incentive roots in the mutual-benefit principle. Service consumers are also service providers. In other words, if a user wants

to benefit from the service provided by the system, she also has to contribute to the system.

• The last category is based on monetary incentives. In this case, the system has to pay a certain amount of money to motivate potential participants, such that the participants can use their resources, usually smartphone sensors, to complete the distributed tasks.

The three types of incentives possess different properties. The design of entertainment and service incentives depends on specific sensing tasks heavily, which restricts applicable areas of such incentives. On the contrary, monetary incentives are mostly designed for a general framework, which can be applied to diverse sensing tasks. In this survey, we organize the three types of incentives according to their own structural characteristics and present representative works for each type.

Note that incentive mechanisms are also studied in other networking problems [14–16]. However, all of these works are tailored to meet the unique characteristics of the problems under study. Thus they cannot be applied to mobile crowd sensing problems as stated in this work.

We highlight the contributions of this paper as follows:

• To the best of our knowledge, this is the first survey concerning various incentives and corresponding mechanisms for mobile crowd sensing, which we believe is complementary to several surveys of mobile sensing systems [1–5].   
• Existing works on incentives of mobile crowd sensing systems are collected and studied. We have classified the incentives into three categories: entertainment, service, and money. Each category is organized and illustrated according to its unique structure.   
• The important characteristics of incentive methods are summarized and compared in the form of tables with respect to each category.   
• Some possible future directions of incentive mechanisms are proposed and analyzed.

The rest of the paper is organized as follows: Section II explores how mobile sensing games help collect diverse sensed data. The principle and representative applications of service incentives are given in Section III. Section IV presents multiple monetary incentive mechanisms and their properties. Finally, Section V discusses some possible future directions and Section VI draws the conclusion.

# II. ENTERTAINMENT AS INCENTIVES

The incentives of entertainment in mobile sensing tasks are inspired by location-based mobile games [17, 18], which focus on enriching game players’ experience by incorporating various devices with sensing capabilities. In this section, we discuss three sensing contexts and corresponding representative games for motivating people.

# A. Network Infrastructure

Gathering data about localization and communication networks are important for some location-based services. For example, knowing where good network connections are available can be helpful for mobile TV service providers. Therefore, researchers are interested in designing location-based games that can reveal network infrastructures. The key challenge of such games is that, given a predefined game area, players should investigate as many spots as possible inside the area, such that the signal map of the network can be built accurately.

Barkhuus et al. [19] design a mobile game Treasure to build WiFi coverage maps of a given game area. Players carry mobile devices with GPS and WiFi. They need to pick up virtual coins scattered over the game area and then upload the coins to a server to gain game points. Better network connections give larger probabilities of uploading the collected coins successfully. Therefore players are motivated to find areas with stronger WiFi coverage. Bell et al. [20] also study WiFi coverage of a specific area. They design a location-based game called Feeding Yoshi, where teams of players are asked to search for open and close WiFi hotspots. In the game, open hotspots are virtual fruits, while close hotspots are virtual pets called Yoshis. To earn more points, players need to find more fruits and feed them to Yoshis. These searching activities implicitly reveal the WiFi information around the game area.

Considering the coverage of GSM cells, Broll and Benford [21] design a game named Tycoon, where players compete with each other to gain the largest amount of credits by buying virtual objects (e.g., buildings) in a predefined game area. Each GSM cell in the game area is virtually mapped to either a producer or a consumer in the game. Players collect resources from producers and exchange for the virtual objects from consumers to earn credits. This interaction process generates cell-id and GPS traces that can be used to evaluate the spatial coverage of a GSM cell. Similarly, Drozd et al. [22] develop the game Hitchers, where a player is required to expose virtual hitchers (i.e., hitch hikers) in her current GSM cell. Each hitcher has a specific destination and can be picked up and carried away by other players. In this manner, hitchers travel across the city and record a large amount of trajectories that can be used to build GSM cell-id maps.

Despite the various game characters and elements, the location-based games we discuss above share a simple game principle: giving users game points as a reward for revealing the network coverage map of an area. The popularity and effectiveness of this principle suggests its wide applicability in designing games to gather information about networks.

# B. Geographic Data

Geographic data is a kind of sensed data that can be automatically recorded by embedded sensors of mobile devices, such as sounds and GPS traces in a specific region. The location-based games for geographic data are usually transformed from traditional card games or outdoor exercises. We first introduce several representative games, and then discuss the design principles.

GeoTicTacToe [23] is a location-based variant of the traditional game Tic Tac Toe. In Tic Tac Toe, two players, X and O, try to place marks X or O in the game board. The one who first successfully places three X’s or O’s in a row/column/diagonal wins the game. The same rule applies to GeoTicTacToe, except for the turn-taking restriction. The game board now is the interesting sensing area. Each board position is assigned with a coordinate. The players have to move to a board position to place X-token or O-token and the time it takes to move from one point to another depends on the distance and the speed of each player. The balance of reasoning and sportive elements needs to be well handled in this situation to assure a fair and interesting game.

TABLE I SENSING GAMES 

<table><tr><td>Authors</td><td>Ref</td><td>Game</td><td>Sensing Task</td><td>Technology/Sensor</td><td>Collected Data</td></tr><tr><td>Barkhuus et al.</td><td>[19]</td><td>Treasure</td><td>study WiFi coverage of specific areas</td><td>WiFi, GPS</td><td>maps with signal strength</td></tr><tr><td>Bell et al.</td><td>[20]</td><td>Feeding Yoshi</td><td>study WiFi coverage of specific areas</td><td>WiFi</td><td>manually annotated maps</td></tr><tr><td>Broll and Benford</td><td>[21]</td><td>Tycoon</td><td>evaluate the coverage of GSM cells</td><td>GSM, GPS</td><td>travel trajectories with cell-ids and GPS readings</td></tr><tr><td>Drozd et al.</td><td>[22]</td><td>Hitchers</td><td>evaluate the coverage of GSM cells</td><td>GSM</td><td>travel trajectories with cell-ids</td></tr><tr><td>Schlieder et al.</td><td>[23]</td><td>GeoTicTacToe</td><td>collect GPS traces (and other sensor readings) for predefined areas</td><td>GPS, other sensors</td><td>GPS traces (and other sensor readings)</td></tr><tr><td>Schlieder et al.</td><td>[24, 25]</td><td>CityPoker</td><td>collect GPS traces (and other sensor readings) for predefined areas</td><td>GPS, other sensors</td><td>GPS traces (and other sensor readings)</td></tr><tr><td>Jordan et al.</td><td>[26]</td><td>Ostereiersuche</td><td>identify structural landmarks</td><td>GPS</td><td>GPS traces</td></tr><tr><td>Matyas et al.</td><td>[9]</td><td>CityExplorer</td><td>produce geospatial data for location-based service</td><td>GPS, camera</td><td>GPS traces, photos, manual annotations</td></tr><tr><td>Han et al.</td><td>[27]</td><td>BudBurst Mobile</td><td>facilitate climate change education and data collection</td><td>accelerometer, GPS, compass</td><td>GPS traces, manual annotations</td></tr><tr><td>Bell et al.</td><td>[28]</td><td>EyeSpy</td><td>produce information about recognizable and findable locations</td><td>WiFi, camera</td><td>WiFi fingerprints, photos, manual annotations</td></tr></table>

CityPoker [24, 25] is a variant of the card game Poker. The game is played by two teams (players) and starts by assigning a poker hand of five cards to each team. The team then tries to improve their poker hand by changing cards at predefined geographical locations (caches) scattered over the game area. There are two cards in each cache, with which the team can only exchange one card. The game ends under two conditions: (1) every team has finished card exchanging at every cache; (2) time limit is met. The winner of the game is the team with the best poker hand. Contrary to normal poker, CityPoker is a full information game, where it eliminates most of the chance element. Each team knows the card distribution on the game area and has to wisely plan next moves against the opponent.

Ostereiersuche [26] is a location-based mobile game inspired by a popular German tradition, according to which families go for a walk and kids look for colorfully painted eggs hidden by the Easter bunny. Game players follow navigational hints to search for virtual hidden eggs with coupons in the physical game area. Each player earns a chance to win a prize in a lottery by collecting three different coupons. Consequent actions of collecting eggs provide the movement trajectory of a player. Combining numerous trajectories can reveal the structure of space and reason about salient spatial elements.

In summary, a common principle of these games is that players move frequently and contribute large amounts of trajectories in game areas. As smartphones are equipped with various sensors, the trajectories can contain rich information such as GPS traces, accelerometer readings and noise records. These trajectories can then be used for diverse crowd sensing tasks. Another principle is to balance the sportive and reasoning elements of the game. As users are usually required to travel a long distance in the game, the game design should reduce the influence of speed differences among users. Otherwise, fast users may easily dominate the game, which makes the game less attractive.

# C. Geographic Knowledge

Geographic knowledge is a collection of data that users explicitly generate for a physical location. Intuitive examples of geographic knowledge include classifications of points of interest, ratings of a restaurant, and opening times of a museum.

CityExplorer [9] is designed based on the idea of the award winning board game Carcassonne designed by Klaus-Jurgen ¨ Wrede. The primary way for a player to win in CityExplorer is to set as many markers as possible in a citywide game area. The game area is divided into non-overlapping squares or segments, where the setting of markers is allowed. The player who holds the majority of markers in such a segment claims the domination of it and will get credits. As the game is designed to collect geospatial data, the setting of a marker includes: (1) take photos of the location where you put a marker at; (2) record the location name; (3) approach the location closely enough; (4) select the correct category for that location.

Project BudBurst [29] is an online participatory sensing network. The goals of the project are facilitating climate change education and engaging participants in the climate change data collection, based on the timing of leafing, flowering, and fruiting of plants. The Budburst Mobile app for Android aims initially at making data collection by participants in Project BudBurst easier and more convenient. Han et al. [27] investigate adding game components to BudBurst Mobile to motivate individuals to engage more in the project. The game components include two approaches for players to earn points: (1) use local plant lists and the interactive map to initiate plant observations; (2) find a plant at the published location, take a photo and keep a note of the observation.

In EyeSpy [28], players make use of photos or texts to tag geographic locations. Other players then locate these places with tags and confirm them to earn points for themselves. As a result, EyeSpy produces a collection of recognisable and findable geographic information in the form of photos and text tags. Large numbers of such tags are then used to support navigation tasks.

The above games share a key property of active content generation for a specific location. Generally, these games do not emphasize on participating and competing in a synchronized time period. Instead, they make use of players’ casual short time slots to generate data. This design principle holds the advantage that users only generate data when they would like to play the game, which helps to sustain the playability of the game.

In summary, the characteristics of sensing games are listed in TABLE I.

# III. SERVICE AS INCENTIVES

For some mobile crowd sensing systems, a participant (e.g., a smartphone user) may have two roles concurrently: a contributor and a consumer. Traffic monitoring is a typical example. A participant acts as a contributor when she travels on a bus or car if she collects traffic data (e.g., GPS traces) to a service provider via networks such as WiFi, GPRS, and 3G. The service provider then processes the data crowdsourced from a large amount of users and provides a real-time traffic information service, such as querying on traffic jams and bus crowdedness. In such sensing applications, in order to attract more users to contribute sensed data such that the system can provide services of good quality, the service provider will usually grant a participant some service quota, which determines how much service that user can receive. In essence, this strategy is an exchange of contribution and consumption for each participant.

Luo and Tham [30] design two incentive schemes under this framework: Incentive with Demand Fairness (IDF) and Iterative Tank Filling (ITF). The system consists of a service provider and N smartphone users. Assume that the time is slotted. In each slot, user i is assigned a quadruple $< \psi _ { i } , c _ { i } , Q _ { i } , q _ { i } >$ , where $\psi _ { i }$ represents the user’s contribution level within that slot, ci denotes the cost of the user, $Q _ { i }$ is the user’s service demand for consumption in the next slot, and $q _ { i }$ is the service quota that is granted by the service provider, which is the upper bound of service that the user can actually consume in the next slot. The service provider offers a total amount $Q _ { t o t }$ of service quota to all users and associates $Q _ { t o t }$ with the quality of service (QoS) Ψ of the system. The higher Ψ is, the higher $Q _ { t o t }$ is. The problem is thus to assign an amount $Q _ { t o t }$ of service quota to N users with respect to user quadruples under two cases, IDF and ITF.

In IDF, the objective is to assure fairness of each user in consuming the service. Intuitively, a larger $\psi _ { i }$ will lead to a larger $q _ { i }$ assigned to user i. Taking the demand $Q _ { i }$ and the total service quota restriction $Q _ { t o t }$ into consideration, the quota distribution scheme is as follows: sort the users in descending order of $\psi _ { \underline { { i } } }$ , and increase each $q _ { i }$ in this order at the rate of $Q _ { i } \psi _ { i } / \sum _ { l = 1 } ^ { N }$ Qlψl until reaching $Q _ { i }$ . Therefore, the user with the largest ψi will get the maximal $q _ { i } / Q _ { i }$ i first.

![](images/431b115573d027717d98e0ec7009727894c2ade350c26036e423bcce4ef57ddd.jpg)



Fig. 1. The transaction process of TruCentive protocol [32]

In ITF, the objective is to maximize social welfare from the system’s perspective, i.e., the aggregate user utility is maximized. The objective function is defined as $\begin{array} { r } { S = \dot { \sum } _ { i = 1 } ^ { N } { \psi _ { i } u _ { i } } . } \end{array}$ N , where $u _ { i }$ is user i’s utility. In optimizing this objective, the user with larger $\psi _ { i }$ will be of higher preference. The utility function should be monotonically increasing with diminishing return property as suggested in [31]. Typically, the problem would be converted to a nonlinear programming problem.

IDF and ITF can serve as general approaches for service exchange systems. The theoretical results guarantee their good performance in optimizing the objective functions. Yet in the problem formulation, how to quantify the user quadruples is not investigated, making the solutions less attractive for practical applications. Considering this, other research works concentrate on specific application scenarios.

Hoh et al. [32] design an incentive scheme, named Tru-Centive, for crowdsourced parking information systems. In the crowdsourced parking system, contributors are drivers who provide parking availability information and consumers are drivers who utilize the crowdsourced parking information to search for parking spots. Contributors report information about when and where a parking spot is available or soonto-be available, called PA messages. The crowdsouced system gathers PA messages and then distributes the messages to the drivers near the location to help them find available spots.

How to trade PA messages is the core functionality of TruCentive. Credits are used as the incentive for each PA message exchanged among contributors and consumers. Typically, a PA message contains the following information: GPS coordinate of the parking spot, identifier of the parking spot, and identification of the contributor’s vehicle. The work flow of the TruCentive trading scheme is shown in Fig 1.

The challenges for TruCentive are two folds: how to ensure consumers being honest and how to ensure profitability for the service provider. For the first challenge, the authors design a game theoretical scheme which guarantees that consumers can only maximize their gain by telling the truth. The key idea is that a consumer can resell the spot after she successfully parks at a traded spot if she tells the truth. Thus TruCentive sets the reward parameters to ensure that the expected gain of reselling a spot is higher than the expected gain of telling lies. To guarantee that the service provider is profitable, TruCentive makes sure that the benefit of the provider is larger than the cost under several mathematical constraints.

![](images/141a5a2fbf37c40b9dd5eacbeed1ef526f5749d6ab9c2d7949686277df41f247.jpg)



Fig. 2. Group-level credit database

Lan et al. [33, 34] discuss another scenario where crowdsourced mobile surveillance is considered. They propose a virtual-credit-based protocol for data collection in mobile surveillance. The protocol demands strict fair exchange of sensor data uploads for virtual credits. Without paying credits, a participant cannot download data directly from the server or indirectly from other participants. Also, participants cannot obtain credits for uploads they did not perform. Therefore, participants are motivated to earn credits by uploading sensor data or share their bandwidth with other participants.

In the simple form of utilizing mobile phone users, Gupta et al. [35] make use of SMS as a tool to crowdsource in developing regions. They propose a platform called mClerk, which can send and receive tasks via SMS. Also, mClerk can send small images and thus can distribute graphical tasks. mClerk enables image-based tasks to be distributed to lowincome workers by using a protocol that can send small bitmapped images via ordinary SMS messages. Then it is used to digitize local-language text. Typically, mClerk starts by scanning paper documents, then it segments documents into word images, and sends each image via SMS to users’ phones. To motivate users’ participation, mClerk will give service quota to the users who finish each task correctly. The quota that can later be consumed by users is usually in the form of airtime (in chunks of minimum recharge amount) provided by mobile network operators. This simple service exchange scheme is effective in drawing users’ participation.

Researchers also find the service exchange principle useful in other areas. In LiveCompare [36], participants use their phone cameras to take pictures of product price tags. By submitting a price data point, the user can receive pricing information for the product at nearby grocery stores. In DietSense [37], participants take pictures of what they eat and share it within a community to compare eating habits. The commonality of all these application-based incentive mechanisms is that they focus on easy deployment in the real-world systems. The tight coupling between mechanisms and system properties limits the generalization ability of these mechanisms. Furthermore, the system utility of such mechanisms is not maximized in most cases.

Different from the previous individual-level incentives of service exchanging, some research works investigate incentives from a group-level view. The basic idea, as elaborated in [38], is inspired by the incentives of blood donation in real life. Every blood donor can benefit herself and her linear relatives if they need blood for clinic use. Thus, a donor is motivated not only by her own utility, but also by her relatives’ utilities. This group-level incentive has been proven effective in practice.

The concept of group-level incentive means that, mobile users can be organized as a virtual group according to their relations, such as relatives, spouse, classmates, and friends. In the hope of drawing more users on collecting sensor data, the platform gives credits as reward to all members in a group once there is at least one member who makes contribution (Fig. 2). Cheng et al. [38] design a group-level incentive schemes in wireless sensor networks (WSN). Typically, in WSN, data collection is a great challenge as sensor energy is a bottleneck for small sensing devices, which are used to measure, monitor and transmit data in the physical world. By adopting the idea of sharing benefit among group members, smartphone users are motivated to participate in data collection when some group members need the service.

In general, if we view each group as a single super entity, the strategies for individual-level incentives of service exchange can be applied. The difficulty mainly comes from the implementation of information sharing and management among group members.

As a brief summary, we list the properties of sensing tasks with service incentives in TABLE II.

# IV. MONEY AS INCENTIVES

Paying for sensed data in crowd sensing tasks is the most intuitive incentive, as it has made sensed data become goods in a free market. Any user who would like to make some money can sell her sensed data for crowd sensing tasks. In this section, we first review the effectiveness of monetary incentives, and then introduce different incentive mechanisms designed for negotiation between the task requester and the participants.

# A. The Effectiveness of Monetary Incentives

Monetary incentives have been used in many e-commerce scenarios. Rivest and Shamir [39] initially try to measure web content usage through users by paying a certain amount of money based on page visits to a site. With the prevalence of online music and applications, payment schemes are also introduced to these fields [40]. Monetary incentives are applied to Amazon Mechanical Turk (MTurk) for task fulfillment [41], where requesters post tasks that are easy for humans to accomplish, but difficult for computers. Workers undertake tasks in order to get some payments. Mason and Watts [42] show that increasing the amount of payments in MTurk can help completing tasks faster. In the case of participatory sensing, although it shares some similarities with MTurk (e.g., the requestor only distributes small tasks to users), the data collection paradigm of mobile crowd sensing is quite different as users collect data and complete sensing tasks during their daily routines. Thus it is necessary to investigate how well monetary incentives can work in mobile crowd sensing scenarios.

TABLE II SENSING TASKS WITH SERVICE INCENTIVES 

<table><tr><td>Authors</td><td>Ref</td><td>Type of Sensor</td><td>Sensing Service Description</td></tr><tr><td>Luo and Tham</td><td>[30]</td><td>general</td><td>provides two general incentive mechanisms: one considers user fairness and the other pursues social welfare maximization</td></tr><tr><td>Hoh et al.</td><td>[32]</td><td>GPS</td><td>provides available parking information (when and where) to drivers</td></tr><tr><td>Lan et al.</td><td>[33, 34]</td><td>video camera</td><td>provides mobile surveillance videos and data forwarding service</td></tr><tr><td>Gupta et al.</td><td>[35]</td><td>none</td><td>digitizes local-language text</td></tr><tr><td>Deng and Cox</td><td>[36]</td><td>camera</td><td>provides product price sharing service</td></tr><tr><td>Reddy et al.</td><td>[37]</td><td>camera, GPS, microphone</td><td>provides eating habit comparison and suggestion service</td></tr><tr><td>Cheng et al.</td><td>[38]</td><td>general</td><td>collects different types of data in wireless sensor networks</td></tr></table>

TABLE III PAYMENT SCHEMES 

<table><tr><td>Scheme</td><td>Description</td></tr><tr><td>MACRO</td><td>lump sum payment (50 dollars)</td></tr><tr><td>MEDIUM $_{\mu}$ </td><td>medium payment (20 cents per valid submission)</td></tr><tr><td>HIGH $_{\mu}$ </td><td>high payment (50 cents per valid submission)</td></tr><tr><td>LOW $_{\mu}$ </td><td>low payment (5 cents per valid submission)</td></tr><tr><td>COMPETE $_{\mu}$ </td><td>competition-based payment (ranging from 1 to 22 cents per valid submission)</td></tr></table>

Musthag et al. [43] design a study to investigate the effectiveness of monetary incentives. Specifically, the study is designed to collect physiological, psychological, and behavioral measures of stress from people by asking them to answer questions and submit sensed data from their wearable sensors. The authors compare three different payment schemes:

• UNIFORM. Participants are paid a fixed amount of 4 cents for each completed question.   
• VARIABLE. Participants are paid a variable amount in the range 2 to 12 cents per question. The amount changes with questionnaire according to some distribution.   
• HIDDEN. This scheme is the same as VARIABLE, except that participants are not told the amount of each question until they complete an entire questionnaire.

The result of the study shows that VARIABLE incentive scheme can reduce 50% of the cost than UNIFORM incentive scheme to achieve the same performance. HIDDEN incentive payment scheme is the least effective one among the three schemes.

Reddy et al. [44] also investigate how different payment schemes affect user participation. The designed task is to learn about recycling practices at a university. Participants need to take photos of the contents in waste bins distributed across the campus. They can optionally tag the images to describe the contents. Participants are rewarded each time they take a sample. In the study, 55 users are recruited and they are randomly divided into five incentive groups as shown in Table III.

Note that the total budget for all payment schemes is capped at 50 dollars per participant. The study results show that, in terms of participation level, $\mathrm { C O M P E T E } _ { \mu }$ is the most successful scheme. However, the user participation rates vary greatly. MACRO is the least successful scheme considering participation rate. Also, COMPE $\mathrm { { \bf { E } } } _ { \mu }$ performs the best considering the spatial and temporal coverage provided by participants.

Usually, mobile sensing applications would reveal privacy information of users, such as locations. Thus it is natural to consider the problem of evaluating the price of user privacy, i.e., at what price a user will be willing to expose her privacy. If the payment is lower than the privacy price, the system may fail to recruit enough users to perform tasks.

Danezis et al. [45] infer the price at which volunteers would be willing to expose their locations for a period time by using tools in experimental economics and psychology. The authors carry out a seal-bid second-price auction and invite volunteers to participate in a fictitious study that needs the location information from their phones. The application asks the volunteers to bid a price they require for revealing their positions. The work flow of the auction is as follows: volunteers are asked to offer a bidding price; then auctioneer expects to invite n people with the lowest bidding prices, and pay them an amount equivalent to the lowest price of the bidder who is not chosen. The auction structure can motivate users to reveal their true values attached to their location privacy. In the study conducted among computer science students at the University of Cambridge, the results show that a median bid of 10 pounds is needed for location privacy. If the study has commercial interests, the median bid raises by 10 pounds. This result can be considered a lower bound on the location privacy as students are with few responsibilities and in a tolerant environment.

The above investigations on monetary incentives demonstrate a common fact: users have different payment expectations for the same sensing task and they would like to involve in determining the payment. For example, HIDDEN scheme gives different payments for different users, yet it performs worse than UNIFORM scheme. This is because users have no idea how much money they can get for completing the sensing task. On the contrary, $\mathrm { C O M P E T E } _ { \mu }$ and auctions perform well, as users know how much they can get if they decide to participate in these schemes. In the following subsections, we discuss two kinds of such effective schemes.

# B. Monetary Incentives Based on Auctions

An auction-based mechanism is originally a process of buying and selling goods by negotiating the monetary prices [46].

![](images/cd4566e40a3289aeda5e3d0ab4838ded4d38a8c34b93e95dc6160c6bcf96de26.jpg)



Fig. 3. Reverse auction system [53]

Given the various forms of auction-based approaches, they have been widely applied to monetary bidding scenarios, such as spectrum allocation [47], P2P networks [48], routing [49], and resource allocation in grids [50]. Auction-based approaches are also studied in a few non-monetary scenarios, such as target tracking in wireless sensor networks [51] and robot coordination [52]. In the context of mobile crowd sensing, auction-based approaches are investigated in the original form, i.e., monetary mechanisms, and a growing number of elaborate mechanisms are proposed. Specifically, a kind of auction, called reverse auction, is adopted to model the negotiation process in crowd sensing. The basic structure of the reverse auction system is shown in Fig 3. The system involves two participating roles: a platform that distributes sensing tasks and the mobile phone users who constitute potential labor force. The objective is to design a task assignment and payment negotiation scheme, which ensures that both the platform and users are satisfied, i.e., their utility functions are maximized.

The platform initiates one round of task distribution by sending task descriptions. A set of n users are assumed to be interested in the sensing tasks after receiving the requests. If users participate in sensing tasks, they will consume multiple resources, including computation, communication, and energy. Thus it is rational for a user to expect certain profit based on her cost and sensing plan (e.g., sensing time). A participating user then submits a bidding profile (including a bidding price and a sensing plan) to the platform. After collecting all bidding profiles from the n users, the platform selects a subset of them and determines the payments for them. Finally, the selected users perform the assigned tasks and upload the sensed data to the platform.

Lee and Hoh [54] design a Reverse Auction-based Dynamic Price incentive mechanism with virtual participation credit (RADP-VPC) that aims at minimizing and stabilizing the platform cost while maintaining the participation level, which is obtained by keeping price competition and user retention. As the name of the mechanism implies, there are two functional components: RADP and VPC.

RADP makes use of the sealed bid reverse auction [55] to select m winners out of n bidders who want to sell their sensed data. Lee and Hoh consider the situation where the auction is conducted in multiple rounds. In each round r, bidder i bids at price $b _ { i } ^ { r }$ , which is lower bounded by her true cost $c _ { i } .$ . The platform selects $m$ bidders with lowest bids and purchases their data. The widely adopted utility function of user i in round r is defined as follows [56]:

$$
u _ {i} (b _ {i} ^ {r}) = (h _ {i} (b _ {i} ^ {r}) - c _ {i}) \cdot g _ {i} (b _ {i} ^ {r}), \tag {1}
$$

where $h _ { i } ( b _ { i } ^ { r } )$ and $g _ { i } ( b _ { i } ^ { r } )$ are the received rewards and winning probability, respectively. Rational users always consider a tradeoff between the winning probability $g _ { i } ( b _ { i } ^ { r } )$ and the expected gain $h _ { i } ( b _ { i } ^ { r } ) - c _ { i }$ . Therefore, bidders will adjust their bidding behaviors adaptively: if a bidder loses in the current round, she will decrease her bidding price such that she can raise the winning probability; on the contrary, a bidder will increase her bidding price when she wins in the current round.

The above mechanism encounters the problem of incentive cost explosion. A user who loses in the current round with higher true valuation will think that she is not possible to win, as her true valuation is higher than other users’ true valuations. Thus, the loser has no incentive to participate in the next round. On the other hand, a user who wins the current round will think that she can still increase the bidding price in order to raise her expected utility. Hence, when the number of remaining users falls below a certain point, the incentive cost of the platform will explode. To prevent such incentive cost explosion, the authors add virtual participation credit (VPC) to the mechanism. Specifically, a user i who loses in the current round r, and participate in the next round r + 1 will receive a VPC $v _ { i } ^ { r + 1 }$ as a reward:

$$
v _ {i} ^ {r + 1} = \left\{ \begin{array}{c l} v _ {i} ^ {r} + \alpha , & \text { if   user   } i \text {   loses   in   round   } r, \\ 0, & \text { otherwise. } \end{array} \right. \tag {2}
$$

VPC is used for decreasing a user’s bid price, thus her winning probability in the next round will increase. To be clear, We differentiate two bid prices: actual bid $b _ { i } ^ { r }$ and competition bid $b _ { i } ^ { r ^ { * } }$ , which are related by the equation:

$$
b _ {i} ^ {r ^ {*}} = b _ {i} ^ {r} - v _ {i} ^ {r}. \tag {3}
$$

By introducing VPC to RADP, the platform is able to maintain price competition and prevent incentive cost explosion.

Jaimes et al. [57] consider the mechanism design based on user locations and platform budgets. The authors propose that, for sensing tasks, it is insufficient to select only users with the lowest costs in every round. It is also important to consider the locations of users, the coverage, and the budget constraint. Thus they combine RADP with Recruitment mechanism (RADP-VPC-RC) [54] and the Greedy Budgeted Maximum Coverage (GBMC) [58] to create a new Greedy Incentive Algorithm (GIA).

To deal with the coverage problem, GIA uses the geometric disk model:

$$
f (d (i, j)) = \left\{ \begin{array}{l l} 1, & \text { if } d (i, j) \leq R, \\ 0, & \text { otherwise }, \end{array} \right. \tag {4}
$$

where $d ( i , j )$ represents the Euclidean distance between user i and user $j ,$ and $R$ is the coverage of a mobile phone sensor.

Taking the coverage and budget into consideration, the problem can be stated as follows. Given a set U of n users, a collection $\{ S _ { i } \} , i = 1 , 2 , . . . , n$ of subsets of U (with $S _ { i }$ denoting the set of users that are covered by user i), and a budget L, find a subset $S \subseteq U ,$ , such that the total incentive cost of users in S is bounded by $L ,$ and the total number of users covered by S is maximized. This budgeted maximum coverage problem is solved by GIA, which includes three steps: (1) select the set $S _ { i }$ that maximizes the marginal coverage increment per unit cost, and add $S _ { i }$ to the candidate set G; (2) select the set $S _ { j }$ that maximizes the marginal coverage increment, and add $S _ { j }$ to the candidate set $G ^ { \prime } ; ( 3 )$ return the best of the two candidates as the final result. Although the implementation of GIA is restricted to maximizing the coverage of disk models, the key idea of GIA is more general and may be adapted to other objective functions, such as submodular functions.

Yang et al. [59] consider the essential property of truthfulness in incentive mechanisms, and design a reverse auctionbased incentive mechanism that is computationally efficient, individually rational, profitable and truthful:

• Computational efficiency: An incentive mechanism is computationally efficient if it has a polynomial time complexity.   
• Individual rationality: A user will get nonnegative utility upon completing the sensing task.   
• Profitability: The platform will get nonnegative utility at the end of the sensing task.   
• Truthfulness: A mechanism is truthful, or incentive compatible, if a bidder cannot improve her utility by submitting a bidding price deviating from her true value in spite of others’ bidding prices.

The authors model the problem as follows: the platform has a set $\Gamma = \{ \tau _ { 1 } , . . . , \tau _ { m } \}$ of sensing tasks in the users’ selection list. Each $\tau _ { i } \in \Gamma$ is of value $v _ { i } > 0$ to the platform. Each user i can select a subset of tasks $\Gamma _ { i } \subseteq \Gamma$ and has a cost $c _ { i }$ associated with the selected tasks. User i can submit a biding profile $( \Gamma _ { i } , b _ { i } )$ to the platform, where $b _ { i }$ is user i’s bidding price. The platform selects a subset $S$ of all bidding users and determines a payment $p _ { i }$ for each winning user i. The utility of user i is

$$
u _ {i} = \left\{ \begin{array}{c l} p _ {i} - c _ {i}, & \text { if } i \in S, \\ 0, & \text { otherwise. } \end{array} \right. \tag {5}
$$

The utility of the platform is

$$
u _ {0} = v (S) - \sum_ {i \in S} p _ {i}, \tag {6}
$$

where $\begin{array} { r } { { v } ( S ) = \sum _ { \tau _ { j } \in \cup _ { i \in S } \tau _ { i } } { v } _ { j } } \end{array}$

It is obvious that in order to maximize $u _ { 0 } ( S )$ , we have $p _ { i } = b _ { i }$ . Thus the platform utility becomes:

$$
u _ {0} = v (S) - \sum_ {i \in S} b _ {i}, \tag {7}
$$

which can be proved to be a submodular function that has constant-factor approximation algorithms for maximization [60].

The proposed truthful incentive mechanism, named MSening Auction, consists of two phases:

• Winner selection: Users are sorted according to the difference of their marginal values and bids. The set of winners are $S = \{ 1 , 2 , . . . , L \}$ , where $L \leq n$ is the largest index guaranteeing that $v _ { L } \geq b _ { L }$ .   
• Payment determination: To compute the payment $p _ { i }$ for each winner $i \in S ,$ , we sort the users in $U \backslash \{ i \}$ according to the difference of their marginal values and bids. For each position $j$ in this sorting, we compute the maximum price that user i can bid given that she can still be selected instead of the user at the $j \mathrm { - t h }$ position of the sorting. In the end, $p _ { i }$ is set to the maximum of all computed prices.

Subramanian et al. [61] adopt the same bidding framework. They improve the platform utility compared with MSensing by designing a mechanism named SMART. Specifically, SMART takes the output set S of MSensing and conducts user examination through retain, remove and replace operations. As such, SMART refines the set of selected users and guarantees that the final utility is at least as large as that of MSensing.

The reverse auction-based mechanisms we discussed so far focus on motivating normal users to participate in the sensing tasks. Yet they cannot take into account the differences of users. For example, some users may be willing to spend more time or efforts in sensing than others do, whereas some users may be malicious in order to benefit themselves. Therefore, when designing incentive mechanisms, it is also necessary to consider the discrepancies among users.

Recently, Krontiris and Albers [62] propose a Multi-Attribute Auctions (MAA) to consider both incentives of users and multiple attributes of sensed data. MAA is an extension of the traditional reverse auction. The traditional reverse auction only considers the negotiated price between buyers (service providers) and sellers (smartphone users). On the contrary, MAA considers buyer’s preferences for an item besides the price. The system can express its preferences in the form of a utility function, which represents the key characteristic of multi-attribute auctions [55]. The utility function takes each bid, including a monetary bid and multiple quality dimensions, as input, and calculates a utility score. Mathematically, the bid can be expressed by an k-dimensional vector ${ \boldsymbol x } = ( x _ { 1 } , . . . , x _ { k } )$ . Assume that the utility function u(x) is additive, and each attribute $x _ { i }$ has a weight $w _ { i }$ , then the overall utility of a bid is:

$$
u (x) = \sum_ {i = 1} ^ {k} w _ {i} u (x _ {i}), \tag {8}
$$

where $\textstyle \sum _ { i = 1 } ^ { k } w _ { i } = 1$ . For n submitted bids, the system thus can determine the winning bid:

$$
\arg \max _ {x ^ {j}} u (x ^ {j}), 1 \leq j \leq n, \tag {9}
$$

where $x ^ { j }$ represents the j-th bid.

Given the framework of MAA, Krontiris and Albers suggest a list of candidate attributes: price, location accuracy, user credibility, sensing time, etc. They use the Quality of Context framework [67] to derive attribute selection. Although MAA provides a good vision of combining multi-attributes of users in the incentive mechanism, users receive a heavy burden of selecting attributes and tuning the corresponding weights, which actually decreases the incentives of participation in the first place.

TABLE IV MONETARY INCENTIVE MECHANISMS 

<table><tr><td>Authors</td><td>Ref</td><td>Mechanism</td><td>Platform Objective</td><td>Payment Scheme</td><td>Property</td></tr><tr><td>Musthag et al.</td><td>[43]</td><td>posted price</td><td>verify monetary incentive</td><td>uniform, variable, hidden</td><td>none</td></tr><tr><td>Reddy et al.</td><td>[44]</td><td>posted price</td><td>verify monetary incentive</td><td>fixed, ranking based</td><td>none</td></tr><tr><td>Danezis et al.</td><td>[45]</td><td>seal-bid auction</td><td>verify monetary incentive</td><td>lowest losing bid</td><td>truthful</td></tr><tr><td>Lee and Hoh</td><td>[54]</td><td>reverse auction</td><td>minimize and stabilize platform cost</td><td>equal to bids</td><td>prevent users from dropping out of sensing tasks</td></tr><tr><td>Jaimes et al.</td><td>[57]</td><td>reverse auction</td><td>maximize coverage within budget</td><td>equal to bids</td><td>consider spatial coverage of selected users</td></tr><tr><td>Yang et al.</td><td>[59]</td><td>reverse auction</td><td>maximize utility</td><td>threshold payment</td><td>profitable, individual rational, truthful</td></tr><tr><td>Subramanian et al.</td><td>[61]</td><td>reverse auction</td><td>maximize utility</td><td>threshold payment</td><td>profitable, individual rational, truthful</td></tr><tr><td>Krontiris and Albers</td><td>[62]</td><td>multi-attributive auction</td><td>maximize overall utility with multi-attributes</td><td>equal to bids</td><td>multi-attribute evaluation of users</td></tr><tr><td>Duan et al.</td><td>[63]</td><td>Stackelberg game</td><td>recruit enough users</td><td>equal share of the total reward</td><td>analysis of Nash equilibrium</td></tr><tr><td>Yang et al.</td><td>[59]</td><td>Stackelberg game</td><td>maximize utility</td><td>proportional share of the total reward</td><td>unique Nash equilibrium</td></tr><tr><td>Zhao et al..</td><td>[64]</td><td>online reverse auction</td><td>maximize utility within budget</td><td>threshold payment</td><td>individual rational, truthful, competitive</td></tr><tr><td>Koutsopoulos</td><td>[65]</td><td>reverse auction</td><td>minimize cost given quality constraint</td><td>threshold payment</td><td>individual rational, truthful</td></tr><tr><td>Singla and Kause</td><td>[66]</td><td>reverse auction</td><td>maximize utility within budget</td><td>threshold payment</td><td>privacy protected, individual rational, truthful, competitive</td></tr><tr><td>Zhang et al..</td><td>[53]</td><td>online reverse auction</td><td>maximize the difference of utility and cost</td><td>threshold payment</td><td>individual rational, truthful, competitive</td></tr></table>

Koutsopoulos [65] considers a simpler setting, where the users have only one attribute: quality of collected data. In this case, users only need to submit their bids and participation levels as other reverse auction-based incentive mechanisms. For each user i, the platform maintains and continuously updates an empirical quality indicator $q _ { i }$ , which quantifies the relevance or usefulness of the sensed data provided by user i in the past. This can be evaluated by the average deviation of submitted data from the result of the aggregation of all users’ sensed data.

# C. Monetary Incentives Based on Stackelberg Game

Stackelberg game [68] is a game where one player (leader) has dominant influence over other players (followers). Typically, the game has two stages: (1) the leader moves first; (2) the followers move. This game has been utilized in the domain of sensing applications since the task distribution framework holds the similar behavior.

Duan et al.. [63] make use of the Stackelberg game to design a threshold revenue model for service providers. Specifically, consider a set of $N = \{ 1 , 2 , . . . , n \}$ smartphone users who are interested in participating, with the total number n being publicly known. Each user i has a cost $c _ { i }$ for participating. If the service provider recruits at least $n _ { 0 }$ smartphone users for sensed data collection, it can receive a revenue of $V .$ The system and the users interact through a two-stage process similar to that of Stackelberg game.

• The system announces a pair $( R , n _ { 0 } )$ , where R is the total reward and $n _ { 0 }$ is the threshold number of required participants.   
• Each user decides whether to accept the task or not.

Assume that in the second stage, there are n users willing to participate, a participated user i’s payoff is:

$$
\left(\frac {R}{n} - c _ {i}\right) \cdot 1 _ {(n \geq n _ {0})}, \tag {10}
$$

where $1 _ { A }$ is the indicator function, with value being 1 when the condition A is satisfied and 0 otherwise. That is, if the system recruits a sufficient number of users, the recruited user i incurs a cost $c _ { i }$ and receives a reward $R / n$ . In this model, the profit of the system is:

$$
(V - R) \cdot 1 _ {(n \geq n _ {0})}. \tag {11}
$$

As illustrated above, the sensing task now is organized as a two-stage Stackelberg game, which can be analyzed by backward induction. Let us first consider the second stage, where users make decisions based on the observed value of the total reward R and the threshold number $n _ { 0 }$ . It is considered as reaching a Nash equilibrium (NE) if no user can improve her payoff by unilaterally deviating her current strategy. This equilibrium leads to a task success probability $P ( n \geq n _ { 0 } ; R )$ . Note that there may be multiple Nash equilibria here. Then we consider the first stage, where the system selects the value of R to maximize its expected profit $( V - R ) \cdot P ( n \geq n _ { 0 } ; R )$ . This two-stage analysis guarantees an equilibrium of the whole sensing task distribution.

Yang et al.. [59] also modeled the proposed platform-centric incentive mechanism as a StackelBerg game. In the platformcentric model, there is one sensing task and the platform announces a total reward R. The sensing plan of user i is represented by the number of time units $t _ { i }$ she is willing to spend on the sensing task. The cost of user i is $\kappa _ { i } t _ { i } ,$ , with $\kappa _ { i }$ meaning the unit cost. The utility of user i is:

$$
u _ {i} = \frac {t _ {i}}{\sum_ {j \in U} t _ {j}} R - t _ {i} \kappa_ {i}. \tag {12}
$$

The utility of the platform is:

$$
u _ {0} = \lambda \log (1 + \sum_ {i \in U} \log (1 + t _ {i})) - R, \tag {13}
$$

where the two log terms reflect the diminishing return and λ is a system parameter. The NE of the model is derived through backward induction and is proved to be unique. Therefore, the model can be solved by numerical methods.

The Stackelberg game can produce solutions with theoretical guarantees. However, the shortage is that the costs of all users or their probability distributions are assumed to be known. This limits the applicability of Stackelberg game-based mechanisms because users may keep their costs private in the real world.

TABLE IV gives a summarization of monetary incentive mechanisms.

# V. FUTURE DIRECTIONS

Incentive mechanism design is in its infancy in the field of mobile crowd sensing. Much work remains to be done in order to guarantee sufficient participation for the rapidly proliferating sensing applications. Among the three types of incentives, entertainment and service are more applicationdependent because they require domain knowledge. On the contrary, monetary incentive is suitable for general sensing applications and hence attracts more attention recently. In this section, we discuss possible future directions considering incentive mechanisms, with an emphasis on monetary ones.

# A. Entertainment-based Incentives

For incentives of entertainment, we have shown that the existing sensing games share several structural design principles that can accommodate various types of mobile crowd sensing tasks. With the development of wireless technologies and pervasive sensing units (e.g. [69, 70]), as well as the emergence of new sensing task categories, sensing games may be adapted considering the following aspects.

1) Hybrid networks: Existing sensing games make use of a specific kind of wireless networks (e.g., GSM, 3G, or WiFi) to transmit collected sensed data. The network capability hence is not fully utilized when several networks exist. Specifically, network offloading techniques [71], which migrate mobile data traffic from cellular networks to WiFi access points, provide the opportunity to enable new sensing games with wide area coverage and heavy traffic load, such as games with video streaming in metropolitan areas, where cellular networks cover the whole game area and WiFi access points boost data transmission.

2) Integrating equipments: Smartphones are prevalent in designing mobile sensing games in the literature. With the new trends of wearable devices, such as smartwatches, smart wristbands, and smartglasses, another promising direction is to integrate smartphones with these devices to enrich the gaming experience of participants. Smartwatches and smart wristbands can better capture the physical movements of players than smartphones, while smartglasses are capable of creating fascinating virtual world to make sensing games

more attractive. Therefore, if sensing task requestors can use smartphones to coordinate various wearable devices, they may work out diverse games appealing to a great number of users.

3) Heterogeneous sensing systems: As stated in Section II, giving game points as reward is effective in location check-in tasks [19–22]. These sensing tasks are homogeneous, where the contribution of each user is easy to evaluate and the corresponding game point distribution is straightforward. In the emerging social sensing systems, such as MediaQ [72], the heterogeneous sensing tasks are also based on location checkins. Therefore, an intuitive solution for user incentives in social sensing systems is to introduce game points. However, the game point distribution scheme in the homogeneous system may not be used directly. The challenge is that it becomes difficult to assign points to tasks such that enough players are motivated, as tasks in social sensing systems require different sensors, and their difficulty levels vary greatly for different users. New effective game point distribution schemes are required to motivate users to complete as many tasks as possible under these constraints.

# B. Service-based Incentives

For incentives of service, researchers have studied mechanisms from two aspects: developing general abstract models to analyze theoretic properties, and designing applicationspecific mechanisms for easy deployment. We discuss possible directions that can enhance existing results.

1) Dynamic models: Existing abstract models, such as IDF and ITF [30], assume that the full knowledge of users in the service system is known a priori. Specifically, they include the total number of users as a parameter for resource allocation. Yet in real applications, users exhibit dynamic actions in the system. They may join the system asynchronously and have diverse levels of service demand at different places. The parameters such as the total number of users change frequently. These dynamic properties make the static models impractical. Therefore, we believe that designing dynamic models with theoretic guarantees is critical for enhancing the availability and applicability of the abstract models.

2) Group-level models: Intuitively, group-level incentives are more powerful in motivating users than individual-level incentives, as each user in a group makes contribution not only for herself, but also for the other members in the same group. Yet existing mechanisms have not take into account the situation that users may also lose incentives to contribute, because they know that other members will share their service quotas. This phenomenon is similar to the free riding in P2P networks [73], where users tend to consume the resource without contribution. We believe the it is desirable to make group-level mechanisms robust against such behaviors before applying them to various applications.

# C. Monetary Incentives

Monetary incentive mechanisms emphasize efficient negotiation between the system and users. Researchers mostly take advantage of auctions to design mechanisms. We envision a few research directions for auction-based incentive mechanisms in the following paragraph.

![](images/d3173cb42c6703b70e7ba1db297781febfc2866fb61aaa1e426a90e6ebb7c72f.jpg)



Fig. 4. Online reverse auction [53]

1) Online mechanism design: Existing monetary systems mostly assume static settings, i.e., when the interaction between a platform and users starts, a sufficient number of users must be available such that the strategies can be applied. Even in the recurrent format of auction-based methods, it is assumed that for a certain period of time, the platform can see a sufficient number of bids. This setting is referred to as offline setting here, and we deem online setting as a more practical setting, where the users’ bids do not have to be synchronized. Unlike the batched and synchronised manner in the offline setting, the interactive process in the online setting is sequential and asynchronous. The key difference is that the decision of the platform is made one by one upon each user’s arrival, and each user leaves immediately after one round of interaction with the platform. The interaction of the platform and the users in online setting is shown in Fig. 4. Recently, Some researchers [53, 64] investigate this online setting based on an offline budget feasible mechanism, which provides a starting point for online mechanisms. We believe more research work will be conducted in this direction.

2) Task assignment: Most existing mobile crowd sensing systems are designed to collect sensed data for specific applications, such as traffic monitoring and pollution monitoring, where users only need to keep their smartphone sensors on for data collection. Recently, another crowd sensing paradigm, called spatial crowdsourcing [74], is receiving increasing interests. In this paradigm, users need to actively answer spatial queries by going to specific locations. Therefore, designing effective incentive mechanisms for spatial crowdsourcing systems proposes a new challenge: the mechanism not only needs to select users, but also needs to assign appropriate tasks to the selected users. We believe that, with the development of spatial crowdsourcing, many incentive mechanisms can be investigated accordingly.

3) Quality control: Though some pioneer works, as discussed in Subsection IV-B, have been proposed to consider

user quality in mobile crowd sensing, the resultant mechanisms have some flaws. The main concern is that these mechanisms require the platform to maintain the whole population of users’ information, such as reputation or quality indicator, which may be inefficient or even untenable. In fact, the quality we care is the final quality of sensed data aggregation for a platform. Hence, it is possible to achieve good quality of experience for a platform without user information logs. One possible direction is to follow the methods adopted by Internet crowdsourcing tasks [75, 76], where statistical tools are applied to get data summarization of high quality.

4) Privacy tradeoff: To some extent, monetary payment to a participant compensates for her privacy leak, such as location and behavior pattern. The private information makes the participant vulnerable to malicious attack. Therefore, protecting participants’ privacy is of great concern even though participants are compensated. A key character of mobile crowd sensing tasks is location dependance. Existing incentive mechanisms largely ignore the privacy protection of participants. What’s worse, under most current incentive mechanisms, users who participate in the bidding process directly reveal their locations, resulting in that the users who lose in the bidding process get no compensation at all for their privacy revelation. Considering this, Singla and Kause [66] propose an mechanism that only requires users to submit their bidding with obscure locations. After the bidding process, only the winning users are needed to reveal their true locations when submitting sensed data. In this setting, the platform utility is sacrificed, as in user selection phase, the platform do not have the accurate locations for users and cannot evaluate the accurate utility of each user. We believe that more research works are needed for designing efficient incentive mechanisms with privacy protection.

# VI. CONCLUSION

In this survey, we review three types of incentives that have been applied in mobile crowd sensing systems: entertainment, service, and money. Entertainment-based methods try to motivate normal participants by turning certain sensing tasks into games, such that participants can experience enjoyment while they are contributing to the sensing systems. Integrating sensing tasks and games depends heavily on the structure of the games, which results in a limited applicability. Incentives of service are in the form of exchanging personal contribution and system service. Typically, this kind of incentive can be widely applied in the public service systems, such as air pollution monitoring, noise monitoring, and traffic monitoring. Monetary incentive mechanisms provide participants the most intuitive incentives. Once participants make contributions for the sensing tasks, they can receive some money as reward. In this paradigm, large amounts of participants’ spare time can be utilized and the sensing tasks themselves do not need to possess properties like enjoyment or comfort of service. In other words, monetary mechanisms are more general than the mechanisms of entertainment and service since the latter two classes of mechanisms must be implemented in an applicationspecific way.

In conclusion, incentives play an essential role in mobile crowd sensing systems, as they feed the system on sufficient number of participants such that the sensing systems can actually work. Incentives appear in different forms and each form has its well-suited contexts. With the rapidly proliferating mobile crowd sensing applications, the development of effective and efficient incentive mechanisms is a new and vibrant field and will continue to flourish.

# ACKNOWLEDGMENT

This work is supported in part by the NSFC Major Program under grant 61190110, NSFC under grant 61171067, 61332004, 61361166009, 61272426, and the NSFC Distinguished Young Scholars Program under grant 61125202. S. Tang’s work is partially supported by the NSFC under grant U1135004 and 61170080, and 973 Program under grant 2014CB360501.

# REFERENCES

[1] N. Lane, E. Miluzzo, H. Lu, D. Peebles, T. Choudhury, and A. Campbell, “A survey of mobile phone sensing,” IEEE Communications Magazine, vol. 48, no. 9, pp. 140– 150, 2010.   
[2] M. Y. A. Wazir Zada Khan, Yang Xiang and Q. Arshad, “Mobile phone sensing systems: A survey,” IEEE Communications Surveys & Tutorials, vol. 15, no. 1, 2013.   
[3] R. K. Ganti, F. Ye, and H. Lei, “Mobile crowdsensing: Current state and future challenges,” IEEE Communications Magazine, vol. 49, no. 11, pp. 32–39, 2011.   
[4] G. Chatzimilioudis, A. Konstantinidis, C. Laoudias, and D. Zeinalipour-Yazti, “Crowdsourcing with smartphones,” IEEE Internet Computing, 2012.   
[5] A. Campbell, S. Eisenman, N. Lane, E. Miluzzo, R. Peterson, H. Lu, X. Zheng, M. Musolesi, K. Fodor, and G. Ahn, “The rise of people-centric sensing,” IEEE Internet Computing, vol. 12, no. 4, pp. 12–21, 2008.   
[6] N. Maisonneuve, M. Stevens, M. Niessen, and L. Steels, “Noisetube: Measuring and mapping noise pollution with mobile phones,” Information Technologies in Environmental Engineering, pp. 215–228, 2009.   
[7] E. Koukoumidis, L. Peh, and M. Martonosi, “Signalguru: leveraging mobile phones for collaborative traffic signal schedule advisory,” in Proceedings of ACM MobiSys, 2011.   
[8] A. Thiagarajan, L. Ravindranath, K. LaCurts, S. Madden, H. Balakrishnan, S. Toledo, and J. Eriksson, “Vtrack: accurate, energy-aware road traffic delay estimation using mobile phones,” in Proceedings of ACM SenSys, 2009.   
[9] S. Matyas, C. Matyas, C. Schlieder, P. Kiefer, H. Mitarai, and M. Kamata, “Designing location-based mobile games with a purpose: collecting geospatial data with cityexplorer,” in Proceedings of ACM ACE, 2008.   
[10] C. Costa, C. Laoudias, D. Zeinalipour-Yazti, and D. Gunopulos, “Smarttrace: Finding similar trajectories in smartphone networks without disclosing the traces,” in Proceedings of IEEE ICDE, 2011.   
[11] “Sensorly.” http://www.sensorly.com.   
[12] C. Wu, Z. Yang, and Y. Liu, “Smartphones based crowdsourcing for indoor localization,” IEEE Transactions on Mobile Computing, vol. 14, no. 2, pp. 444–457, 2015.

[13] X. Zhang, Z. Yang, C. Wu, W. Sun, Y. Liu, and K. Xing, “Robust trajectory estimation for crowdsourcing-based mobile applications,” IEEE Transactions on Parallel and Distributed Systems, vol. 25, no. 7, pp. 1876–1885, 2014.   
[14] R. Ma, S. Lee, J. Lui, and D. Yau, “An incentive mechanism for p2p networks,” in Proceedings of IEEE ICDCS, 2004.   
[15] S. Zhong, L. Li, Y. Liu, and Y. Yang, “On designing incentive-compatible routing and forwarding protocols in wireless ad-hoc networks,” Wireless Networks, vol. 13, no. 6, pp. 799–816, 2007.   
[16] L. Gao, Y. Xu, and X. Wang, “Map: Multiauctioneer progressive auction for dynamic spectrum access,” IEEE Transactions on Mobile Computing, vol. 10, no. 8, pp. 1144–1161, 2011.   
[17] C. Magerkurth, A. D. Cheok, R. L. Mandryk, and T. Nilsen, “Pervasive games: bringing computer entertainment back to the real world,” ACM Computers in Entertainment, vol. 3, no. 3, pp. 4–4, 2005.   
[18] N. M. Avouris and N. Yiannoutsou, “A review of mobile location-based games for learning across physical and virtual spaces,” Journal of Universal Computer Science, vol. 18, no. 15, pp. 2120–2142, 2012.   
[19] L. Barkhuus, M. Chalmers, P. Tennent, M. Hall, M. Bell, S. Sherwood, and B. Brown, “Picking pockets on the lawn: the development of tactics and strategies in a mobile game,” in Proceedings of ACM UbiComp, 2005.   
[20] M. Bell, M. Chalmers, L. Barkhuus, M. Hall, S. Sherwood, P. Tennent, B. Brown, D. Rowland, S. Benford, M. Capra, et al., “Interweaving mobile games with everyday life,” in Proceedings of ACM CHI, 2006.   
[21] Seamful Design for location-based mobile games, 2005.   
[22] A. Drozd, S. Benford, N. Tandavanitj, M. Wright, and A. Chamberlain, “Hitchers: designing for cellular positioning,” in Proceedings of ACM Ubicomp, 2006.   
[23] C. Schlieder, P. Kiefer, and S. Matyas, “Geogames: Designing location-based games from classic board games,” IEEE Intelligent Systems, vol. 21, no. 5, pp. 40–46, 2006.   
[24] C. Schlieder, “Representing the meaning of spatial behavior by spatially grounded intentional systems,” GeoSpatial Semantics, pp. 30–44, 2005.   
[25] P. Kiefer, S. Matyas, and C. Schlieder, “Playing locationbased games on geographically distributed game board,” in Proceedings of PerGames, 2007.   
[26] K. O. Jordan, I. Sheptykin, B. Gruter, and H.-R. Vatter- ¨ rott, “Identification of structural landmarks in a park using movement data collected in a location-based game,” in Proceedings of ACM SIGSPATIAL COMP, 2013.   
[27] K. Han, E. Graham, D. Vassallo, and D. Estrin, “Enhancing motivation in a mobile participatory sensing project through gaming,” in Proceedings of IEEE PAS-SAT/SocialCom, 2011.   
[28] M. Bell, S. Reeves, B. Brown, S. Sherwood, D. MacMillan, J. Ferguson, and M. Chalmers, “Eyespy: supporting navigation through play,” in Proceedings of ACM CHI, 2009.   
[29] http://budburst.org/.   
[30] T. Luo and C. Tham, “Fairness and social welfare in

incentivizing participatory sensing,” in Proceedings of IEEE SECON, 2012.   
[31] R. T. Ma, S. Lee, J. Lui, and D. K. Yau, “Incentive and service differentiation in p2p networks: a game theoretic approach,” IEEE/ACM Transactions on Networking, vol. 14, no. 5, pp. 978–991, 2006.   
[32] B. Hoh, T. Yan, D. Ganesan, K. Tracton, T. Iwuchukwu, and J. Lee, “Trucentive: A game-theoretic incentive platform for trustworthy mobile crowdsourcing parking services,” in Proceedings of IEEE ITSC, 2012.   
[33] K. Lan, C. Chou, and H. Wang, “An incentive-based framework for vehicle-based mobile sensing,” Procedia Computer Science, vol. 10, pp. 1152–1157, 2012.   
[34] C.-M. Chou, K.-c. Lan, and C.-F. Yang, “Using virtual credits to provide incentives for vehicle communication,” in Proceedings of IEEE ITST, 2012.   
[35] A. Gupta, W. Thies, E. Cutrell, and R. Balakrishnan, “mclerk: enabling mobile crowdsourcing in developing regions,” in Proceedings of ACM CHI, 2012.   
[36] L. Deng and L. P. Cox, “Livecompare: grocery bargain hunting through participatory sensing,” in Proceedings of ACM HotMobile, 2009.   
[37] S. Reddy, A. Parker, J. Hyman, J. Burke, D. Estrin, and M. Hansen, “Image browsing, processing, and clustering for participatory sensing: lessons from a dietsense prototype,” in Proceedings of ACM EmNets, 2007.   
[38] L. Cheng, C. Chen, J. Ma, and Y. Chen, “A group-level incentive scheme for data collection in wireless sensor networks,” in Proceedings of IEEE CCNC, 2009.   
[39] R. Rivest and A. Shamir, “Payword and micromint: Two simple micropayment schemes,” in Security Protocols, 1997.   
[40] D. Geer, “E-micropayments sweat the small stuff,” IEEE Computer, vol. 37, no. 8, pp. 19–22, 2004.   
[41] Amazon, “Mturk,” March 2010. http://mturk.com.   
[42] W. Mason and D. Watts, “Financial incentives and the performance of crowds,” in Proceedings of ACM SIGKD-D HCOMP, 2009.   
[43] M. Musthag, A. Raij, D. Ganesan, S. Kumar, and S. Shiffman, “Exploring micro-incentive strategies for participant compensation in high-burden studies,” in Proceedings of ACM Ubicomp, 2011.   
[44] S. Reddy, D. Estrin, M. Hansen, and M. Srivastava, “Examining micro-payments for participatory sensing data collections,” in Proceedings of ACM Ubicomp, 2010.   
[45] G. Danezis, S. Lewis, and R. Anderson, “How much is location privacy worth,” in Poceedings of WEIS, 2005.   
[46] V. Krishna, Auction theory. Academic press, 2009.   
[47] J. Jia, Q. Zhang, Q. Zhang, and M. Liu, “Revenue generation for truthful spectrum auction in dynamic spectrum access,” in Proceedings of ACM MobiHoc, 2009.   
[48] C. Wu, B. Li, and Z. Li, “Dynamic bandwidth auctions in multioverlay p2p streaming with network coding,” IEEE Transactions on Parallel and Distributed Systems, vol. 19, no. 6, pp. 806–820, 2008.   
[49] X. Su, S. Chan, and G. Peng, “Auction in multipath multi-hop routing.,” IEEE Communications Letters, vol. 13, no. 2, pp. 154–156, 2009.

[50] D. Grosu and A. Das, “Auction-based resource allocation protocols in grids,” in Proceedings of IASTED PDCS, 2004.   
[51] J. Zheng, M. Z. A. Bhuiyan, S. Liang, X. Xing, and G. Wang, “Auction-based adaptive sensor activation algorithm for target tracking in wireless sensor networks,” Future Generation Computer Systems, vol. 39, pp. 88 – 99, 2014.   
[52] B. P. Gerkey and M. J. Mataric, “Sold!: Auction methods for multirobot coordination,” IEEE Transactions on Robotics and Automation, vol. 18, no. 5, pp. 758–768, 2002.   
[53] X. Zhang, Z. Yang, Z. Zhou, H. Cai, L. Chen, and X. Li, “Free market of crowdsourcing: Incentive mechanism design for mobile sensing,” IEEE Transactions on Parallel and Distributed Systems, vol. 25, no. 12, pp. 3190–3200, 2014.   
[54] J. S. Lee and B. Hoh, “Dynamic pricing incentive for participatory sensing,” Pervasive and Mobile Computing, vol. 6, no. 6, pp. 693–708, 2010.   
[55] M. Bichler, The Future of e-Markets: Multidimensional Market Mechanism. Cambridge University Press, 2001.   
[56] J. Lee and B. Szymanski, “Auctions as a dynamic pricing mechanism for e-services,” Service Enterprise Integration, pp. 131–156, 2007.   
[57] L. Jaimes, I. Vergara-Laurens, and M. Labrador, “A location-based incentive mechanism for participatory sensing systems with budget constraints,” in Proceedings of IEEE PerCom, 2012.   
[58] S. Khullera, A. Mossb, and J. Naor, “The budgeted maximum coverage problem,” Information Processing Letters, vol. 70, pp. 39–45, 1999.   
[59] D. Yang, G. Xue, X. Fang, and J. Tang, “Crowdsourcing to smartphones: incentive mechanism design for mobile phone sensing,” in Proceedings of ACM MobiCom, 2012.   
[60] U. Feige, V. Mirrokni, and J. Vondrak, “Maximizing non-monotone submodular functions,” SIAM Journal on Computing, vol. 40, no. 4, pp. 1133–1153, 2011.   
[61] A. Subramanian, G. S. Kanth, and R. Vaze, “Offline and online incentive mechanism design for smart-phone crowd-sourcing,” arXiv preprint arXiv:1310.1746, 2013.   
[62] I. Krontiris and A. Albers, “Monetary incentives in participatory sensing using multi-attributive auctions,” International Journal of Parallel, Emergent and Distributed Systems, vol. 27, no. 4, pp. 317–336, 2012.   
[63] L. Duan, T. Kubo, K. Sugiyama, J. Huang, T. Hasegawa, and J. Walrand, “Incentive mechanisms for smartphone collaboration in data acquisition and distributed computing,” in Proceedings of IEEE INFOCOM, 2012.   
[64] D. Zhao, X.-Y. Li, and H. Ma, “How to crowdsource tasks truthfully without sacrificing utility: Online incentive mechanisms with budget constraint,” in Proceedings of IEEE INFOCOM, 2014.   
[65] I. Koutsopoulos, “Optimal incentive-driven design of participatory sensing systems,” in Proceedings of IEEE INFOCOM, 2013.   
[66] A. Singla and A. Krause, “Incentives for privacy tradeoff in community sensing,” in Proceedings of AAAI HCOM-

P, 2013.   
[67] T. Buchholz, A. Kupper, and M. Schiffers, “Quality of ¨ context: What it is and why we need it,” in Proceedings of the workshop of HPOVUA, 2003.   
[68] D. Fudenberg and J. Tirole, “Game theory,” 1991.   
[69] J. Han, C. Qian, P. Yang, D. Ma, Z. Jiang, W. Xi, and J. Zhao, “Geneprint: Generic and accurate physical-layer identification for uhf rfid tags,” IEEE/ACM Transactions on Networking, accepted to appear.   
[70] Z. Zhou, C. Wu, Z. Yang, and Y. Liu, “Sensorless sensing with wifi,” Tsinghua Science and Technology, vol. 20, no. 1, pp. 1–6, 2015.   
[71] S. Dimatteo, P. Hui, B. Han, and V. O. Li, “Cellular traffic offloading through wifi networks,” in Proceedings of IEEE MASS, 2011.   
[72] S. H. Kim, Y. Lu, G. Constantinou, C. Shahabi, G. Wang, and R. Zimmermann, “Mediaq: Mobile multimedia management system,” in Proceedings of ACM MMSys, 2014.   
[73] M. Feldman, C. Papadimitriou, J. Chuang, and I. Stoica, “Free-riding and whitewashing in peer-to-peer systems,” IEEE Journal on Selected Areas in Communications, vol. 24, no. 5, pp. 1010–1019, 2006.   
[74] L. Kazemi and C. Shahabi, “Geocrowd: enabling query answering with spatial crowdsourcing,” in Proceedings of ACM SIGSPATIAL GIS, 2012.   
[75] Y. Baba and H. Kashima, “Statistical quality estimation for general crowdsourcing tasks,” in Proceedings of ACM SIGKDD, 2013.   
[76] S. Oyama, Y. Baba, Y. Sakurai, and H. Kashima, “Accurate integration of crowdsourced labels using workers’ self-reported confidence scores.,” in Proceedings of IJ-CAI, 2013.

![](images/9e5b4bb5d66aa59eb8009f77bcd6c7901f3b70a4ca3b22d2eb41c187b7f34099.jpg)



Xinglin Zhang received a B.E. degree in School of Software from Sun Yat-sen University in 2010 and a Ph.D. degree in the Department of Computer Science and Engineering from Hong Kong University of Science and Technology in 2014. He is currently with the South China University of Technology. His research interests include wireless ad-hoc/sensor networks, mobile computing and crowdsourcing. He is a student member of the IEEE and the ACM.

![](images/617e80cf85ead519b7e24cee7d5e66224884ecc34e650af1ad7625bad832aca0.jpg)



Zheng Yang received a B.E. degree in computer science from Tsinghua University in 2006 and a Ph.D. degree in computer science from Hong Kong University of Science and Technology in 2010. He is currently a faculty member of Tsinghua University. His main research interests include wireless adhoc/sensor networks and mobile computing. He is a member of the IEEE and the ACM.

![](images/a703554988188ed5ea4780d33ec7889d2cc849ecebf4e51212fbd2da229a012d.jpg)



Wei Sun received his B.E. degree in the School of Computer Science and Technology from University of Science and Technology of China in 2011. He is now a Ph.D. student in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include wireless sensor networks and pervasive computing. He is a student member of the IEEE and the ACM.

![](images/119d272ff8c97fda31f50786f71558057d737bc1272b4df7551195591041c7cb.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is now a professor at Tsinghua University. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. He is a fellow of the IEEE.

![](images/851a54062ac1439d43270017e897a3711b40dbb0421780428e731443389a0799.jpg)



Shaohua Tang received the B.Sc. and M.Sc. Degrees in applied mathematics, and the Ph.D. Degree in communication and information system all from the South China University of Technology, in 1991, 1994, and 1998, respectively. He has been a full professor with the School of Computer Science and Engineering, South China University of Technology since 2004. His current research interests include information security, networking, and information processing. He is a member of the IEEE.

![](images/8c4006e3d0bca97ab2c1656bd53bb9af70be7ccb5472efa938ca88e5cc80a6bc.jpg)



Kai Xing is an Associate Professor at the School of Computer Science and Technology, The University of Science and Technology of China. He received his M.S. and Ph.D. degree in Computer Science from The George Washington University in 2006 and 2009, respectively. His current research interests include cyber physical networking systems, wireless networks, mobile computing, in-network information processing, and network security. He is a member of the IEEE and the ACM.

![](images/bc37d561dde132e719da38fa48ef43ecac9254965922404b7b19e4fcac18f169.jpg)



Xufei Mao received the Ph.D. degree in Computer Science from Illinois Institute of Technology, Chicago in 2010. He received the MS degree (2003) in Computer Science and the Bachelor degree (1999) in Computer Science at Northeastern University and Shenyang University of Technology respectively. He is currently an Assistant Research Professor in the School of Software, Tsinghua University. His research interests span wireless ad hoc networks, wireless mesh networks and wireless sensor networks.