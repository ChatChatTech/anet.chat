# An Improved Android Collusion Attack Detection Method Based on Program Slicing

Yunhao Liu $^{1,3}$ , Xiaohong Li $^{1,3(\text{☒})}$ , Zhiyong Feng $^{2}$ , and Jianye Hao $^{2}$

$^{1}$ School of Computer Science and Technology, Tianjin University, Tianjin 300350, China {yunhaoliu,xiaohongli}@tju.edu.cn

$^{2}$ School of Computer Software, Tianjin University, Tianjin 300350, China
{zyfeng,jianye.hao}@tju.edu.cn

$^{3}$ Tianjin Key Laboratory of Advanced Networking (TANK), School of Computer Science and Technology, Tianjin University, Tianjin 300350, China

Abstract. Android applications can leak sensitive information through collusion, which gives the smartphone users a great security risk. We propose an Android collusion attack detection method based on control flow and data flow analysis. This method gives analysis of data propagation between different applications firstly. And then, a multi-apps program slice model based on both data and control flow are given. Last, the privacy data leakage paths of multi-apps are computed by reaching-definition analysis. Meanwhile, the criterions of mobile device information leakage edge are redefined according to the correlation of mobile devices. Based on the above principle, we implemented an Android collusion attack sensitive information leakage detection tools called CollusionDetector. Case study is carried out for typical collusion attack scenarios and it can obtain better results than existing tools and methods. Experiments show that the analysis of control flow can more accurately find the path of privacy propagation, and more effectively to identify collusion attacks.

Keywords: Android Collusion Attack · Privacy leakage · Taint analysis · Program slicing

# 1 Introduction

Many privacy leak attacks are accomplished by multi-apps collaboration $[7,18]$ , and these kinds of attacks are called “Android Collusion Attack” $[25]$ . Different from traditional privacy leak attack which rely on single app, Android Collusion Attack often lunched by at least two apps, called source app and sink app. Source app often responsible for acquiring sensitive data and passing it to the sink app while the sink app sends the sensitive data out of the device. Each collusion app has different task and corresponding required permissions, this can easily circumvent those detection methods which focus on single app $[3,9,12]$ .

To address this problem, Android Collusion Attack $[1,26]$ are widely studied. A complete survey on those topics can be found in $[19]$ . In particular, Epicc $[18]$ and IccTA $[17]$ makes precisely static taint analysis on single app and it can find propagation of privacy cross apps with the help of ApkCombiner $[16]$ . Amandroid $[23]$ and SCanDroid $[11]$ can do static taint analysis for a group of app and detect the privacy leak caused by multi-apps.

Nevertheless, the propagation of sensitive information depends not only on the assignment between variables, but also on the control statements such as branch and loop. According to $[4]$ , most exist methods and tools ignore the detection of taint propagation based on control flow and this can cause some malicious app could not be found. Moreover, to prevent missing report, current approaches regard the privacy has leaked when they are sent out of an app. But actually, when sensitive information is sent out of an application does not mean it is certain to be sent out of the device. In other words, existing rules can cause false positives. Therefore, detecting Android Collusion Attack accurately and protecting the smartphone users' privacy data have become urgent needs.

In this paper, we design and build CollusionDetector – an improved detection framework for Android Collusion Attack. Static taint analysis method is adopted to build the taint propagation path between multi-apps and find the app group which can leak privacy. In order to solve the above problems, an improved taint checking algorithm both focus on control flow and data flow taint analysis is proposed. Meanwhile, Android APIs are re-classified to re-define the boundaries of sensitive information. For a set of Apk file to be detected, the interaction information between apps from resource and manifest files of apps are extracted. Together with each app's control flow graph, an inter-app control flow graph (IACFG) can be built. Last, privacy leakage and the collusion app groups can be detected by the improved taint analysis. CollusionDetector can detect the collusion attack which use the control flow to propagate sensitive information and improve the accuracy of detection.

Challenges also exist. The real-world applications may have complex business logic, which can lead to a large control flow graph. When building an inter-app control flow graph and perform taint analysis over it, the efficiency will be low. To this end, we extract suspicious paths from each Apk's control flow graph and build inter-app suspicious paths according to interaction information between apps before doing taint analysis. Suspicious path is a statement path in control flow graph which has the ability to send any information out of device whether the information is sensitive. Obviously, the size of inter-app suspicious paths is much smaller than IACFG and it narrowed the scope of our taint analysis.

To verify our approach, we implement three groups of Android Collusion Attack examples as test cases. Each group includes several Android apps that can collaborate to leak privacy and these three groups stands for different kinds of Android Collusion Attack. CollusionDetector perform analysis on test cases with other existing tool at the same time and our methods can detect all test cases successfully. Moreover, CollusionDetector is used to detect real-world privacy leak and the result is as good as other tools. These illustrate that our work has improvement on the detection of Android Collusion Attack.

The rest of the paper is organized as follow. Section 2 describe the attack scenario of Android Collusion Attack. Section 3 shows each step of our work. Case study and results are presented in Sect. 4 and the limitations of this work are presented in Sect. 5. We conclude the paper in Sect. 6.

# 2 Attack Scenario

According to the Android security report $[15]$ published by Nokia Threat Intelligence Laboratories in 2016, Android Collusion Attack is widely found in real-world Android apps. As Fig. 1 shows, the attacker repackage malicious code into an benign app's Apk. Because Android allow user to install app from any source, these repackaged apps are easily installed by users from some insecure third party sources. After the user install these collusion apps, malicious programs execute in the background, and the functionality of these apps do not appear abnormal, so it is hard for users to find that privacy information has been leaked.

![](images/d4129a7f10a9bc9d54d9a5ffe92dbe8a4b1f43e263d53e0ce2162796ddff498f.jpg)



Fig. 1. Android Collusion Attack in real-world

When collusion apps are installed on the device, they begin to work together to leak the user privacy. Figure 2 shows an example of two apps that cooperate to leak user privacy. First, ContactReader obtains the contacts information and send it to InfoSender. And then, InfoSender send these sensitive data to attackers server.

![](images/57eff2efa210a9a2144540189242c44a0facaadf9f10f67850965462f6789fb2.jpg)



Fig. 2. Mechanism of Android Collusion Attack

Actually, the above-mentioned attack scenario can be easily detect out by current approaches. To circumvent current approaches, attackers change the way of data propagation. Many prior works $[5,6,10,13,21]$ have mentioned the limitation of detecting control dependence attack and the threat of these attack is large. In $[4]$ , there are two types of control flow based data propagation, called Simple Encoding and File Length.

# 2.1 Simple Encoding

Simple Encoding is an effective way to spoof current taint checking mechanisms for Android app. In Fig. 3, ASCII\_Table is the string which contains all character in ASCII table and Tainted is the privacy data. Attackers often build a new string called unTainted to save the sensitive data. Secondly, they traverse each character (called taintedChar) in Tainted and compare taintedChar with every character in ASCII\_Table. And curValue is used to store the current character when traverse the ASCII\_Table. Lastly, if the two variables, taintedChar and curValue, are equal in this matching process, the curValue will be appended to unTainted.

![](images/2ab78f0107ffa6e944523eb3d12897f3c1aa6286c1d112e47d473429535f654d.jpg)



Fig. 3. If the values in curValue and taintedChar are equal, copy curValue to unTainted

Simple Encoding prevent direct assignments from Tainted to unTainted, thus unTainted will not regard as an tainted object according to current taint checking mechanisms. Figure 4 shows Simple Encoding can spoof these tradition mechanisms successfully and send the privacy out of device. The red variables and lines are taint propagation path detected by traditional taint checking mechanism.

# 2.2 File Length

Traditional taint checking mechanisms can be circumvented by File Length with ease. A file should be regarded as an untainted object only if there is no sensitive data is written into it. And the metadata of the file can store information such as length of file. In Fig. 5, attackers encode the taint data firstly, because file length can only store integer types of information. The sensitive data code is an integer and its value is N. Secondly, random data is written, one byte at the time, to a file until its size equals N. Last, attackers get the file length N and decode the number into a string.

![](images/ea6db2e61669de1e665e3f146b824abf5b3e663a632c88cae101e8404563e860.jpg)



Fig. 4. Current taint checking mechanisms track taints according to assignments

![](images/5f2f0a9bebe35fa8e6237e8d8c32b7d3970ed5a6ed78f888c9dd403c0a33c758.jpg)



Fig. 5. File length example

In this way, the file is not a tainted object and its size can be read as an untainted variable. As shown in Fig. 6, the sensitive data can circumvents traditional taint checking mechanism and successfully leaked by using File Length.

```txt
String Sensitive_data = source();
int Sensitive_data_code = Encode(Sensitive_data);
File file = new File();
for(int i = 0; i < Sensitive_data_code; ++i)
{
    writeOneByte(file);
}
int fileLength = file.length();
String Untainted_Sensitive_data = Decode(fileLength);
SendToRemoteServer(Untainted_Sensitive_data); 
```  
Fig. 6. Taint tracking is ended at the condition statement and privacy is leaked

Traditional taint checking mechanism neglect to analysis the control flow based taint propagation. This can cause huge security risks to the users' privacy. While one could extend the prior works to address this limitation, we use a different approach (outlined in Sect. 1) which we describe in more details in the following sections.

# 3 CollusionDetector

As Fig. 7 shows, CollusionDetector contains four phases. First, the control flow graph (CFG) for each Apk will be built and the IAC information will be extracted from each Apk's manifest file. On this basis, the suspicious paths for each Apk can be sliced out from corresponding CFG. In the third step, inter-app suspicious paths can be made up of several suspicious paths according to the IAC information in Phase 1. Last, the privacy propagation can be detected on inter-app suspicious paths by doing improved taint analysis thus the collusion apps can be found.

![](images/f39f33d41e886311b4065f0a52441df824f111650322c9579d9273adc18ea1f3.jpg)



Fig. 7. Overview of CollusionDetector

# 3.1 Analysing Each APK

According to the Phase 1 in Fig. 7, there are two tasks in this step, one is obtaining each input APK's CFG. Another task is parsing each APK's manifest file to find out the IAC information which determine the destination of data flow.

The CFG for each app can be obtained with the help of a static analysis framework for Android app, called FlowDroid. This framework can analyze Android app accurately and provides a series of API to allow user to obtain each Apk's CFG by programming. The IAC information need to be extracted by analysing AndroidManifest.xml. This file lists all components which an app owned and the configuration of these components. One of the configuration for components is Intent-Filter, which can determine the component can receive Intent objects with specific attribute. In addition, We need to extract the attribute values for each of the Intent objects being sent. As shown in Fig. 8, Attackers predefined same Action attribute values to ensure two collusion app can communicate.

![](images/1c40bda494a61636182a094ce84daddd5da53179a86f8f4bd50a1a281b7ce094.jpg)



Fig. 8. Inter-app communication with specific attribute value

An IAC information is defined as a 5-tuple $I = (\sigma, \alpha, \delta, \rho)$ and IAC information for an app set is a collection of I. For one IAC information, $\sigma$ stands for an app and $\alpha$ is the Action property of the Intent object to which the application is sent. If the app can not send any Intent object, the element $\alpha$ can be null. $\delta$ represents the property value of the Intent object that the application can receive and $\rho$ means which applications can receive Intent objects whose property value is $\alpha$ . If the app can not receive any Intent object, its $\delta$ can be null.

Algorithm 1. IAC Matching Algorithm   
Input : Initial collection: InfoSet $_{I}$ Output: Complete InfoSet $_{I}$ 1 some description;
2 Size ← The number of I in InfoSet $_{I}$ ;
3 for i = 0 to Size do
4    tmp $_{1}$ ← the ith element of InfoSet $_{I}$ ;
5    for j = i to Size do
6    tmp $_{2}$ ← the jth element of InfoSet $_{I}$ ;
7    if tmp $_{1}$ · α == tmp $_{2}$ · δ then
8    | tmp $_{2}$ · ρ ← tmp $_{1}$ · α;
9    end
10    end
11 end

To compute IAC information for an app set, we use $InfoSet_{I}$ to express all I for each app. In the initial state, the value of $\sigma$ , $\alpha$ and $\delta$ for each I should be determined because the analysis for every app. The last element $\rho$ should be calculate by Algorithm 1.

# 3.2 Computing Suspicious Paths

To reduce the scope of taint analysis, Suspicious Paths should be built firstly. It is a code execution path that can cause information leakage, whether or not the information is sensitive. In this step, static program slicing is used to obtain each Apk's suspicious paths. There has been a numbers of approaches about program slicing $[14,20,24]$ and computing dependency graph is used in this work. Next subsections describe the process of computing suspicious paths.

Slicing Criterion. To slice Suspicious Paths for each APK, the first challenge is to define slicing criterion. Suspicious Paths focus on sending data out an app, therefore, only those functions which can send information out should be defined as slicing criterion. In Android, there are many APIs can be points of interest such as sendBrocast(), sendTextMessage(), Log.i() and the objects or variables sent by them.

Computing Dependency Graph. In order to compute program slice, Data Dependency Graph (DDG) and Control Dependency Graph (CDG) are necessary. CDG can be built according to CFG easily. In a CFG, statements $a$ and $b$ has a control dependency if the outcome of $a$ determines whether $b$ should be executed or not. Meanwhile, Reaching-Definition analysis is used for the calculation of DDG. In a program, a variable's value depends on its definition and it can be used to define other variables. A definition of variable is defined as a two tuple, $Def = (S, V)$ . In $Def$ , $V$ is the variable and $S$ is the statement where $V$ is defined lately. During the execution of the program, the value of each variable may be change, new definitions can be generated, old definitions can be killed, and some definitions may remain unchanged. Therefore, we use collection $Gen_S$ to save the $Defs$ are newly created in statement $S$ . Meanwhile, collection $Kill_S$ is defined for storing the $Defs$ which are redefined. For each statement $S$ , there are two set, called $InSet_S$ and $OutSet_S$ , to describe the definitions of status before and after the execution of statement $S$ . Equation (1) shows that $InSet_S$ is the union set of definitions after execute all predecessors of $S$ , $pred[S]$ . While Eq. (2) shows that $OutSet_S$ adds the newly created definitions and delete the killed definitions after execute $S$ .

$$
I n S e t _ {S} = \bigcup_ {p \in p r e d [ S ]} O u t S e t _ {p} \tag {1}
$$

$$
O u t S e t _ {S} = G e n _ {S} \cup (I n S e t _ {S} - K i l l _ {S}) \tag {2}
$$

Reaching Definition Analysis is to compute each statement's InSet and OutSet, Algorithm 2 shows a worklist algorithm. The input of this algorithm is each Apk's CFG with all $InSet_S$ and $OutSet_S$ are initialized to empty. When Algorithm start running, it loads all statements $V$ into worklist and repeats the calculation shown by Eqs. (1) and (2), until $InSet_{S}$ and $OutSet_{S}$ for all elements are no longer changed. During the calculation, if the $OutSet_{S}$ is different from the old one after analyzed the statement S, it means that the InSet of successors of S (succ[S]) is change. Hence, the successors of S should be recalculated and succ[S] are send back to worklist again.

Algorithm 2. Reaching Definition Analysis WorkList Algorithm   
Input : control flow graph $G = (V, E)$ Output: $\forall S \in V, InSet_{S}$ 1 some description;
2 foreach S in V do
3 $InSet_{S} \leftarrow \emptyset;$ 4 $OutSet_{S} \leftarrow \emptyset;$ 5 end
6 WorkList $\leftarrow V;$ 7 while WorkList $\neq \emptyset$ do
8 $S \leftarrow$ Pop one basic block from WorkList;
9 $OldOutSet_{S} \leftarrow OutSet_{S};$ 10 $InSet_{S} \leftarrow \bigcup_{p \in pred[S]} OutSet_{p};$ 11 $OutSet_{S} = Gen_{S} \cup (InSet_{S} - Kill_{S});$ 12    if $OutSet_{S} \neq OldOutSet_{S}$ then
13 $WorkList \leftarrow WorkList \cup succ[S];$ 14    end
15 end

After getting the reaching definitions for each statement (e.g., $InSet_{S}$ ), which statements have data dependency relationship with slicing criterion is clear. Moreover, the data dependency graph (DDG) can be worked out and we can obtain the program slice by performing union operation on DDG and CDG.

# 3.3 Combination of Suspicious Paths

When we do inter-app static analysis, the cross app dataflow should be considered. In previous step, we obtain each APK's suspicious paths and these statements sequences are probably send data to another app. That is to say, suspicious belongs to different APKs can be combine.

In the first section, we get the connection points between dataflow through the analyze for AndroidManifest.xml and source files. Here, we combine cross app suspicious paths according to IAC information. Like the example in Sect. 3.1, Fig. 9 shows that two suspicious paths can be combined into an inter-app suspicious path.

![](images/7e67e942a73da08a394340eb430274f9e8546ab7346fbf4d9770325da02c8353.jpg)



Fig. 9. The Combination of Dataflow

# 3.4 Improved Inter-App Taint Analysis

This step consists doing taint analysis on inter-app suspicious paths. In other words, we need to determine whether these suspicious paths will leak sensitive information. Firstly, the source and sink functions should be ascertained. In this work, source is the method which can get the private data (e.g., getLatitude(), getDeviceId()) or receive information from other apps (e.g., getIntent()). Different from prior works, the definition of sink is the method which can send the sensitive information out of the device (e.g., sendTextMessage(), Log.i()). In most current approaches, the method which can send data out of an app is also regarded as sink. However, the privacy data is safe until it flow out of device.

Meanwhile, to address the problem in Sect. 2, we propose a new static taint checking mechanism for Android app. To be able to explain our taint propagation rules in detail we declare the following formalization descriptions and helper functions.

To describe the whole program, we use 2-tuple $P = < B, E >$ . $B$ is the set of all basic blocks in the program and $E$ is the edge between basic blocks. $B$ is defined as 3-tuple $B = < R, L, V >$ . $R$ is the variable in stack area and it can be a basic type variable or a reference of an object. $L$ is the memory location of object in heap area. $V$ is the value of variable.

Besides the descriptions above, there are several helper functions to ensure our precise model for program.

arrayElem(x) can determine whether a variable belongs to an array. The parameter x is the input variable and the return value will be true when x is an array's element.

source() returns sensitive data and the variable which is assigned by this function is tainted variable.

A tainted path T is defined for the basic blocks which contain tainted variables and at the beginning it holds that $T \leftarrow \emptyset$ . Tainted access paths are added to the set whenever the analysis reaches a call to a source, or when processing a statement that propagates an existing taint to a new memory location. Algorithm 3 shows the taint checking for each basic block in a program.

Algorithm 3. Improved Taint Analysis Algorithm   
Input : One BasicBlock, Current tainted variable set T
Output: Tainted variable set T

1 some description;
2 if BasicBlock is like Var_x = Var_y then
3    if ∀Var_y ∈ T then
4    | T ∪ {Var_x};
5    end
6    if Var_y ∉ T ∧ ¬arrayElem(Var_x then
7    | T \ {Var_x};
8    end
9    if x ∈ source() then
10    | T ∪ {Var_x};
11    end
12    if ∀Var_y ∈ T then
13    | T ∪ {Var_x};
14    end
15 end
16 if The type of BasicBlock is Var_x = new Object() then
17    if Var_x ∈ T|¬arrayElem(Var_x) then
18    | T \ {Var_x};
19    end
20 end
21 if The type of BasicBlock is branch structure then
22    if Var_y ∈ condition ∧ Var_y ∈ T then
23    | T ∪ {Var_x};
24    end
25 end

For an assignment basic block with the structure $Var_{x} = Var_{y}$ , we should consider that whether variable $Var_{x}$ is an element of an array first. To ensure the accuracy of analysis if any element in the array is tainted, the array is polluted. According to this rule, if $Var_{x}$ is a polluted variable, the array is tainted. Even if $Var_{x}$ is assigned a new ObjectLocation, as long as it belongs to the array, it must be contaminated.

Another case is the new basic block which creates a fresh object (e.g., $Var_{x} = new$ $Object()$ ), whether the $Var_{x}$ was tainted before, the variable $Var_{x}$ should be removed from T.

When the basic block is a branch structure like if(condition) then statements or loop(condition) do statements, the principle of this rule is that the variable $Var_{x}$ are tainted if its condition expression contains tainted variables.

According to the above algorithm, the implementation of taint analysis on inter-app suspicious paths by doing Reaching Definition analysis. The difference is that the point of interest is the source, because the inter-app suspicious paths have the ability to send any information out. When a variable defined by source() can reach the sink() and can be send by sink method, this path is a taint path.

# 4 Case Study

In this section, we firstly introduce the implementation of CollusionDetector and some examples of Android collusion attack. Then, we use our approach to analysis these attack examples to show the effectiveness of this work. Third, in order to show the improvement of this work in the Android collusion attack detection, we use three other different tools to detect the above attack examples and compare all results.

# 4.1 Implementation

There are already many outstanding static analysis tools for Android application, such as SCanDroid, FlowDroid and Amandroid. Although most of these tools are open source software, there is a lack of interface specification and programming guide. Only FlowDroid provides detailed develop guidance, therefore, our approach is implemented based on it. FlowDroid can be deployed in a development environment as several java projects and it provides us a lot of useful programming interfaces and a dataflow analysis framework. To prove the effectiveness of our approach, we implement several groups of Android Collusion Attack examples and these examples will be analyzed by CollusionDetector and other tools as test cases.

Implementation of CollusionDetector. Because we need programming interfaces offered by FlowDroid, the related FlowDroid projects should be imported into our IDE. We finished this work under the guidance of the Wiki of FlowDroid $[2]$ and build the programming framework successfully according to the guide book $[8]$ . The input of CollusionDetector is am APK file set and the output is:

- Whether there is collusion attack in the input APK file set?   
- If collusion attack exists, which apps are collaborated to leak privacy?   
- The conjunction point of each collusion group.   
- The control flow graph which can identify taint paths.

Implementation of Android Collusion Attack Example. We implement three groups of Android Collusion Attack examples, including one group of traditional collusion attack and two groups of collusion attack based on control flow (Simple Encoding and File Length). As shown in Table 1, the example of traditional collusion attack has two applications, one application called “ContactReader” is responsible for obtaining the contacts information which stored in the mobile phone and send them to another application. Another one called “InfoSender” is responsible for receiving contacts information and transmitting the information through the network to attackers remote server. The difference between examples of collusion attack based on control flow and traditional collusion attack is that they exploit the vulnerabilities of prior works to ensure the tainted data to be “washed up”.

Table 1. Different kinds of Android Collusion Attack examples 

<table><tr><td>Type</td><td>Name</td><td>Permission</td></tr><tr><td rowspan="2">Traditional collusion attack</td><td>ContactReader.apk</td><td>CONTACT_INFO</td></tr><tr><td>InfoSender.apk</td><td>INTERNET</td></tr><tr><td rowspan="2">Simple encoding</td><td>SEContactReader.apk</td><td>CONTACT_INFO</td></tr><tr><td>SEInfoSender.apk</td><td>INTERNET</td></tr><tr><td rowspan="2">File length</td><td>FLContactReader.apk</td><td>CONTACT_INFO</td></tr><tr><td>FLInfoSender.apk</td><td>INTERNET</td></tr></table>

# 4.2 Evaluation

After the implementation, we use CollusionDetector to analysis test cases to demonstrate the effectiveness of our approach. And then, in order to compare the results of different methods, we use four existing Android privacy leak detection methods and CollusionDetector to analyze the above three groups of test cases. Our evaluation addresses the following research questions:

RQ1. Can CollusionDetector find Android Collusion Attack?   
RQ2. How does CollusionDetector compare with existing tools?   
RQ3. Can CollusionDetector detect real-world leak?

All the experiments discussed in this subsection are performed on a Core i5 CPU running with Java8.

RQ1: Experimental Results on Test Cases. We use CollusionDetector to analysis three groups of test cases separately and the results of detection are shown in command line. If there exist collusion attack in the test case, we will map out the taint propagation path in the form of dot graph. FlowDroid provides programming interfaces which can draw dot graph according to control flow graph and we make further development to show taint path as dot graph.

RQ2: Comparison with Existing Tools. In this research question, we compare CollusionDetector with four existing tools: FlowDroid, IccTA and Scan-Droid. There are three issues we focus on:

- Can each tool or method find privacy leak in single app?   
- Can each tool or method find traditional collusion attack in Android?   
- Can each tool or method find File Length and Simple Encoding?

In Table 2, $\odot$ means that this tool can detect privacy leak in a test case and $\oplus$ has the opposite meaning. $\checkmark$ stands for the tool can detect the inter-app taint propagation and find out the collusion apps. We can find that FlowDroid and IccTA can not analysis multiple APK files. They can detect the privacy leak in single app without control flow based taint propagation successfully. Furthermore, IccTA can detect the taint propagation with Simple Encoding and File Length. ScanDroid can successfully find out the traditional collusion attack but it is failed in File Length and Simple Encoding.

Table 2. All methods and tools detection results 

<table><tr><td colspan="2">Test cases</td><td colspan="4">Methods</td></tr><tr><td>Type</td><td>Name</td><td>FlowDroid</td><td>IccTA</td><td>SCanDroid</td><td>Collusion- detector</td></tr><tr><td>Traditional android</td><td>ContactReader</td><td> $\odot$ </td><td> $\odot$ </td><td> $\odot$  √</td><td> $\odot$  √</td></tr><tr><td>collusion attack</td><td>InfoSender</td><td> $\odot$ </td><td> $\odot$ </td><td> $\odot$  √</td><td> $\odot$  √</td></tr><tr><td rowspan="2">Simple encoding</td><td>SEContactReader</td><td> $\otimes$ </td><td> $\odot$ </td><td> $\otimes$ </td><td> $\odot$  √</td></tr><tr><td>SEInfoSender</td><td> $\otimes$ </td><td> $\odot$ </td><td> $\otimes$ </td><td> $\odot$  √</td></tr><tr><td rowspan="2">File length</td><td>FLContactReader</td><td> $\otimes$ </td><td> $\odot$ </td><td> $\otimes$ </td><td> $\odot$  √</td></tr><tr><td>FLInfoSender</td><td> $\otimes$ </td><td> $\odot$ </td><td> $\otimes$ </td><td> $\odot$  √</td></tr></table>

According to the results, the reason why ScanDroid is failed in detect test case group “Simple Encoding” and “File Length” is same with FlowDroid: it can not detect the privacy leak in single app without control flow based taint propagation. We find a defect through the analysis of taint checking mechanism in FlowDroid: they only focus on taint propagation like $Y \leftarrow X_{tainted}$ but ignore the taint propagation based on control flow. Because it is difficult to analyze the source code for all existing tools, we hypothesized that SCanDroid use similar taint propagation rules as FlowDroid but IccTA use a different one. And that is why they can not track taint data propagate with Simple Encoding and File Length methods.

RQ3: Can CollusionDetector Detect Real-World Leak? We use CollusionDetector and tools which have been used in RQ3 to detect real-world leak. The test cases are apps which downloaded from Google Play and we found several apps have privacy leakage behavior.

In Table 3, the $\odot$ , $\otimes$ and has the same meaning in Table 2. According to the result, all methods can detect privacy leak except a failure caused by SCanDroid. Limited by the size of the app collection, none of the tools found the collusion app group based on control flow. While it still prove that CollusionDetector can detect privacy leak in real-world.

Table 3. My caption 

<table><tr><td>Test cases</td><td colspan="5">Methods and tools</td></tr><tr><td>Package name</td><td>FlowDroid</td><td>Epicc</td><td>IccTA</td><td>SCanDroid</td><td>Collusion-detector</td></tr><tr><td>com.zsdevapp.renyu</td><td> $\odot$ </td><td> $\odot$ </td><td> $\odot$ </td><td> $\odot$ </td><td> $\odot$ </td></tr><tr><td>com.y.lovefamily</td><td> $\odot$ </td><td> $\odot$ </td><td> $\odot$ </td><td> $\odot$ </td><td> $\odot$ </td></tr><tr><td>com.gotonyu.android.PhotoShare</td><td> $\odot$ </td><td> $\odot$  √</td><td> $\odot$  √</td><td> $\odot$ </td><td> $\odot$  √</td></tr><tr><td>com.liars.lineLearn</td><td> $\odot$ </td><td> $\odot$ </td><td> $\odot$ </td><td>⊗</td><td> $\odot$ </td></tr></table>

# 5 Limitations

At the moment, CollusionDetector resolves traditional collusion attack and two kinds of collusion attack depend on control flow. Currently, our approach still can not do taint analysis for native code, web applications (e.g., applications developed using PhoneGap $[22]$ ) and dynamic linking library in Android. Although CollusionDetector can avoid the false negative caused by control flow based taint propagation, however, we neglect the false positive cause by analyzing conditional statements. The principle of taint checking mechanism is simple and some complicated situations are overlooked.

# 6 Conclusion

It is proved that this method can detect the Android Collusion Attacks which contain the control flow based pollution, and we also use this method to detect the general privacy leakage applications. Compared with the detection accuracy of existing Android privacy leak detection methods, the result of the proposed method is approximately the same as them. It can be proved that this method can effectively detect the privacy leakage behavior of Android applications, and can also detect collusion attacks that have control flow based pollution. Limited by the size of the application set to be detected, we haven't found privacy leaks based on control flow. We will detect more real-world apps; Moreover, we are prepared to repackage malicious code which can leak privacy data based on control flow into some real-world apps, and then use our tools to detect them.

Acknowledgments. The authors are grateful to the anonymous reviews for their insightful comments, and that will have a great significance to our future work. This work is supported by Tianjin Key Laboratory of Advanced Networking (TANK), School of Computer Science and Technology, Tianjin University, Tianjin China300350. This work has partially been sponsored by the National Science Foundation of China (No. 61572349, 61272106).

# References

1. Davi, L., Dmitrienko, A., Sadeghi, A.-R., Winandy, M.: Privilege escalation attacks on android. In: Burmester, M., Tsudik, G., Magliveras, S., Ilić, I. (eds.) ISC 2010. LNCS, vol. 6531, pp. 346–360. Springer, Heidelberg (2011). doi:10.1007/978-3-642-18178-8\_30   
2. Arzt, S., Rasthofer, S., Fritz, C., Bodden, E., Bartel, A., Klein, J., Traon, Y.L., Octeau, D., Mcdaniel, P.: How to run flowdroid. https://github.com/secure-software-engineering/soot-inflow-android/wiki

3. Arzt, S., Rasthofer, S., Fritz, C., Bodden, E., Bartel, A., Klein, J., Traon, Y.L., Octeau, D., Mcdaniel, P.: Flowdroid: precise context, flow, field, object-sensitive and lifecycle-aware taint analysis for android apps. ACM Sigplan Not. 49(6), 259–269 (2014)   
4. Babil, G.S., Mehani, O., Boreli, R., Kaafar, M.A.: On the effectiveness of dynamic taint analysis for protecting against private information leaks on android-based devices. In: International Conference on Security and Cryptography, pp. 1–8 (2013)   
5. Cavallaro, L., Saxena, P., Sekar, R.: Anti-taint-analysis: practical evasion techniques against information flow based malware defense. Stony Brook University (2007)   
6. Cavallaro, L., Saxena, P., Sekar, R.: On the limits of information flow techniques for malware analysis and containment. In: Zamboni, D. (ed.) DIMVA 2008. LNCS, vol. 5137, pp. 143–163. Springer, Heidelberg (2008). doi:10.1007/978-3-540-70542-0\_8   
7. Chin, E., Felt, A.P., Greenwood, K., Wagner, D.: Analyzing inter-application communication in android. Plant Soil 269(1–2), 309–320 (2011)   
8. Einarsson, A., Nielsen, J.D.: A survivor's guide to java program analysis with soot. Notes from Department of Computer Science (2008)   
9. Enck, W., Ongtang, M., McDaniel, P.: On lightweight mobile phone application certification (2009)   
10. Enck, W., Gilbert, P., Chun, B.G., Cox, L.P., Jung, J., Mcdaniel, P., Sheth, A.N.: Taintdroid: an information-flow tracking system for realtime privacy monitoring on smartphones. In: USENIX Conference on Operating Systems Design and Implementation, pp. 99–106 (2010)   
11. Fuchs, A.P., Chaudhuri, A., Foster, J.S.: Scandroid: automated security certification of android applications (2009)   
12. Gibler, C., Crussell, J., Erickson, J., Chen, H.: AndroidLeaks: automatically detecting potential privacy leaks in android applications on a large scale. In: Katzenbeisser, S., Weippl, E., Camp, L.J., Volkamer, M., Reiter, M., Zhang, X. (eds.) Trust 2012. LNCS, vol. 7344, pp. 291–307. Springer, Heidelberg (2012). doi:10.1007/978-3-642-30921-2\_17   
13. Graa, M., Cuppens-Boulahia, N., Cuppens, F., Cavalli, A.: Detecting control flow in smartphones: combining static and dynamic analyses. In: Xiang, Y., Lopez, J., Kuo, C.-C.J., Zhou, W. (eds.) CSS 2012. LNCS, vol. 7672, pp. 33–47. Springer, Heidelberg (2012). doi:10.1007/978-3-642-35362-8\_4   
14. Horwitz, S., Reps, T., Binkley, D.: Interprocedural slicing using dependence graphs. In: ACM Sigplan 1988 Conference on Programming Language Design and Implementation, pp. 35–46 (1988)   
15. Nokia Threat Intelligence Laboratories: Nokia threat intelligence report. http://resources.alcatel-lucent.com/asset/200492   
16. Li, L., Bartel, A., Bissyandé, T.F., Klein, J., Traon, Y.L.: ApkCombiner: combining multiple android apps to support inter-app analysis. In: Federrath, H., Gollmann, D. (eds.) SEC 2015. IAICT, vol. 455, pp. 513–527. Springer, Cham (2015). doi:10.1007/978-3-319-18467-8\_34   
17. Li, L., Bartel, A., Klein, J., Traon, Y.L., Arzt, S., Rasthofer, S., Bodden, E., Octeau, D., Mcdaniel, P.: IccTA: detecting inter-component privacy leaks in android apps. In: IEEE/ACM IEEE International Conference on Software Engineering, pp. 280–291 (2015)   
18. Octeau, D., Mcdaniel, P., Jha, S., Bartel, A., Bodden, E., Klein, J., Traon, Y.L.: Effective inter-component communication mapping in android with epicc: an essential step towards holistic security analysis. In: USENIX Conference on Security, pp. 543–558 (2013)

19. Rashidi, B., Fung, C.: A survey of android security threats and defenses. J. Wirel. Mob. Netw. Ubiquitous Comput. Dependable Appl. 6, 3–35 (2015)   
20. Reps, T., Horwitz, S., Sagiv, M.: Precise interprocedural dataflow analysis via graph reachability. In: POPL 1995, vol. 167(96), pp. 49–61 (1995). Lecture Notes in Computer Science   
21. Schwartz, E.J., Avgerinos, T., Brumley, D.: All you ever wanted to know about dynamic taint analysis and forward symbolic execution (but might have been afraid to ask). In: Security and Privacy, pp. 317–331 (2010)   
22. Wargo, J.M.: Phonegap Essentials: Building Cross-platform Mobile Apps. Pearson Schweiz AG, Zug (2012)   
23. Wei, F., Roy, S., Ou, X., Robby.: Amandroid: a precise and general inter-component data flow analysis framework for security vetting of android apps. In: ACM SIGSAC Conference on Computer and Communications Security, pp. 1329–1341 (2014)   
24. Weiser, M.: Program slicing. In: International Conference on Software Engineering, pp. 439–449 (1981)   
25. Wu, L., Grace, M., Zhou, Y., Wu, C., Jiang, X.: The impact of vendor customizations on android security. In: ACM SIGSAC Conference on Computer and Communications Security, pp. 623–634 (2013)   
26. Xing, L., Pan, X., Wang, R., Yuan, K., Wang, X.F.: Upgrading your android, elevating my malware: privilege escalation through mobile OS updating. In: IEEE Symposium on Security and Privacy, pp. 393–408 (2014)