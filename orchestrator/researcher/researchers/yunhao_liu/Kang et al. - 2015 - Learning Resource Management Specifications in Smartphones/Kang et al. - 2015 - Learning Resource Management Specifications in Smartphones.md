# Learning Resource Management Specifications in Smartphones

Yanrong Kang\*, Xin Miao†, Haoxiang Liu\*, Qiang Ma†, Kebin Liu† and Yunhao Liu†
\*Department of Computer Science and Engineering, Hong Kong University of Science and Technology
†School of Software and TNLIST, Tsinghua University
Email: {ykangaa, hliuab}@cse.ust.hk, {miao, maq, kebin, yunhao}@greenorbs.org

Abstract—Over the past few years we have observed a phenomenal growth of smartphones. Smartphones are equipped with various hardware and software resources such as Bluetooth, camera and gravity sensors. If these resources are not managed appropriately, it may cause severe problems such as battery drains and system crashes. However, the specifications of resource management are usually implicit. In this paper, we investigate the problem of mining resource management specifications from off-the-shelf apps. Our key insight is that if a set of operations to a resource are frequently performed in a specific order, it must contain the specifications of how to manage the resource. We design a tool named Automatic Resource Specification Miner (ARSM), to automatically extract resource management specifications in smartphones. In our experiments, ARSM can mine tens of rules from 100 top rated Android apps within six hours. Our work is orthogonal to existing studies on diagnosing smartphone apps. With the resource management specifications discovered, ARSM can help them pinpoint more bugs in apps.

Keywords-Mobile Computing; Smartphone Application; Programming Specification Mining;

# I. INTRODUCTION

Mobile computing with smartphones are becoming pervasive. Equipped with powerful hardware and software resources, smartphones are capable of providing a variety of services such as indoor/outdoor localization and social networking [1]–[3]. However, managing resources incorrectly can cause severe problems such as battery drains and system crashes. For example, an official release of Android Facebook app acquires a partial wakelock but does not release it. As a result, even if the screen is shut down by the user, the smartphone's CPU still keeps running in the background. With this app, the battery quickly drains in a few hours and thousands of users were affected [4].

Managing various resources on smartphone platforms is a non-trivial task. Firstly, although smartphone operating systems such as Android and iOS provide detailed APIs documentations, the resource management specifications are not explicitly defined. A developer may not be aware of all of them and misuse them in practice. Secondly, even an experienced developer cannot assure that all the resources are properly handled in a complex system.

The importance of resource management on smartphone platforms has not attracted much attention until recently. Only a few studies have been proposed to address this issue. eDoctor [5] identifies apps that can cause abnormal battery drain through monitoring the resources occupied by them. It can only assist ordinary users to identify energy anomalies, not capable of helping developers to understand its root causes and pinpoint bugs in source code. Pathak et al. studies no-sleep bugs caused by mishandling power control APIs (e.g., wakelocks) and proposes a automatic detection solution based on reaching definitions dataflow analysis in [6]. Jindal et al. uncovers sleep conflicts in smartphone device drivers and presented a runtime debugging system in [7]. These two approaches are restricted to specific kinds of bugs that are predefined.

```txt
public class WakefulIntentService extends IntentService
{ static WakeLock lockStatic = mgr.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK);
final protected void onHandleIntent(Intent intent) {
    try { // Acquire wakelock. Further operations are omitted.
    lockStatic .acquire ();}
    finally { // Release wakelock.
    lockStatic .release (); } }
} 
```  
Listing 1. Wakelock example.

In this paper, we study the problem of automatically discovering resource management rules via mining off-the-shelf apps. Using our method, we are able to learn resource management rules from the crowd and apply them to debug apps.

# A. Resource Management in Smartphones

Resource management in smartphones usually follow implicit programming patterns. Some of them are simple and well-known patterns such as a function pair of open and close: When writing a file, the open operation should always be followed by close. Otherwise, it may cause the file to be locked and further manipulations to this file will be prohibited.

Besides, resource management on smartphone platforms exhibits distinct specifications. In order to save energy, Android aggressively put its components (e.g., 3G radio and CPU) to an idle state shortly after they become inactive. If an app requires to keep several components running, it should explicitly notify the OS through acquiring an wakelock. For example, a partial wakelock instructs the OS not to put CPU to an idle state. And a full wakelock not only prevents the CPU and screen from sleeping, but also turns on the keyboard backlight. However, if the acquired wakelock is not released, the battery will drain quickly. Listing 1 demonstrates a code snippet adapted from an open source project [8]. In this example, the app acquires a partial wakelock and then starts to perform other tasks. In case of any exception during execution, it release the wakelock at the finally block. That is, the wakelock.acquire() → wakelock.release() pattern is faithfully followed.

```groovy
public class AudioRecorder extends Activity {
    private AudioRecord mAudioRecord; //an AudioRecord object
    private boolean inRecordMode = false; // recording state
    public void onCreate(Bundle savedInstanceState) { // Initialize AudioRecord object
    mAudioBufferSize = 2 * AudioRecord.getMinBufferSize(...);
    mAudioRecord = new AudioRecord(...);
    }
    public void onResume() { // Start a thread to record
    inRecordMode = true;
    Thread t = new Thread(new Runnable() {
    public void run() {
    getSamples(); // Process of recording
    });
    t.start();
    }
    protected void onPause() {
    inRecordMode = false; // Change inRecordMode to false to stop the recording thread
    }
    protected void onDestroy() {
    mAudioRecord.release(); // Release mAudioRecord
    }
    private void getSamples() { // Process of recording
    mAudioRecord.startRecording(); // Start recording
    while (inRecordMode) { // Keep on recording until inRecordMode is false
    int samplesRead = mAudioRecord.read(audioBuffer, 0, mAudioBufferSampleSize); // Read data from sensor
    }
    mAudioRecord.stop(); // Stop recording
    }
} 
```  
Listing 2. AudioRecorder example.

# B. Why Are Existing Tools Insufficient?

Although specification mining tools such as [9]–[11] are useful in mining desktop/server applications, none of them is able to discover resource management rules from smartphone apps. The reason is that apps are event-driven and their behaviors highly depend on interactions with users.

In specific, existing tools mainly fall into two categories, i.e., static analysis approaches and dynamic analysis approaches. Static analysis approaches rely on source code only to mine specifications. They do not require to actually execute the program but suffer from searching the large state space. However, on smartphone platforms, the event-driven nature exacerbate this problem. The enrollment of multiple events may cause the function invocations become more complex, thus leading to a larger state space. On the other hand, dynamic analysis approaches leverage user' execution traces to mine specifications. For smartphone apps, their execution traces can be gathered either from users directly or by simulating user behaviors. However, the former method needs to meet specific requirements such as the root priority, while the latter one is yet another challenge [12].

Listing 2 illustrates an example of Audiorecorder usage adapted from [13]. When this activity is created, its method onCreate() is called by the OS and an AudioRecord object mAudioRecord is created. Then method onResume() is invoked and it starts a thread to sampling audio data. If the user switches to another app, onPause() is called and the sampling procedure stops. When the user switches back, the OS invokes onResume again and sampling thread continues to run. Finally, when the user quits this app, the activity is destroyed, and audio resource is released.

From this example, we can observe that the specification of an audio resource (i.e., create() → startRecording() → read() → release()) is tightly coupled with the lifecycle of the activity. Since existing tools cannot perform life-cycle analysis or even inter-procedure analysis, they are unable to detect such patterns.

# C. Our Contributions

In this work, we present ARSM, a practical tool based on static analysis to mine resource management specifications in smartphones. Our contributions are:

- ARSM does not require the source code or execution traces of apps. Instead, it directly the installation files (i.e., apk files) directly.   
- We design a decision tree based approach to identify resource related classes in Android by analyzing the API documentation.   
- We propose an app analysis approach based on an intermediate language and graph data structures.   
- We model the specification mining problem as a frequent subgraph mining problem and successfully obtain specifications from off-the-shelf apps.

The rest of the paper is organized as follows: Section II presents the main design of ARSM. Section III describes its implementation. In section IV, ARSM is evaluated. In Section V, related work in this area is surveyed. And finally section VI concludes the paper.

# II. MAIN DESIGN

# A. Overview

We illustrate the overall design of ARSM in Figure 1. The basic idea of ARSM is to automatically mine resource management patterns from smartphone apps. It first has to parse app (e.g., apk files) and extract resource usage code from different applications. Then it uses frequent pattern mining method to find common resource usage patterns. However, before parsing apps, ARSM needs to know what code is related to resource management. For this purpose, we design an algorithm to automatically find resource related classes in Android. Then we use these resource related classes as seeds of the parsing process. During parsing process, ARSM collects the usage information of these seed classes and represents them with graphs. After embedding life cycle and analyzing inter-procedure information, ARSM gets a dataset of graphs. ARSM adopts closed frequent subgraph mining to attain frequent graphs. Finally it processes the resulting closed frequent subgraphs to derive usage patterns and uses them to detect violations as potential resource management defects.

![](images/e553dfcd4a5cb5fec80fb6aca6d04d8d0953e15349908a2ae341376b6189e48f.jpg)



Figure 1. ARSM Architecture

# B. Resource Identification

Resources on Android platform can be broadly classified into two categories: common resources such as thread, database, graphics that are the same on desktop/server platforms, and special resources such as WiFi, Bluetooth, camera and GPS that are unique. For some resources, such as WiFi, although desktop computers also have wireless network interface cards, the access to them heavily depends on the manufacturers and operating systems. JDK does not provide a standardized way of accessing them. In contrast, on smartphone platforms, Android can make sure that WiFi resources can be accessed in the same way across various manufacturers. Thus we put such resource in the second category.

Identifying the classes related to resource management is not easy. Android APIs contain more than 3000 classes/interfaces. Manually checking each of them is cumbersome. In this section, we design a decision tree based model to identify interesting classes.

1) Feature Extraction: The only input required is the Android API documentation, which can be easily downloaded from the Internet. We then parse the webpages using a XML parser, and extract three kinds of features for each class and interface.

The first kind of feature is Modifier Information. We use this information to distinguish interfaces from classes, as well as the classes that are abstract. We also use access control modifiers to filter non-public ones. In a word, we are only interested in public, non-abstract classes. The second kind of features is Package Structure Information. For all the classes, we analyze their package names and then test if the package names contains interesting keywords such as WiFi, NFC and Bluetooth. The intuition behind this feature is, a class in android.bluetooth package is much more likely to be a resource management related class than one in android.util package. The third kind of features is Member Information. We scan all the methods in a class, and want to find out how many of them matching case-insensitive patterns like: \*connect(), \*start(), \*dispose(), \*acquire(), \*release(), \*shutdown(), where \* stands for any number of characters. The fourth kind of features is Comment Information, which includes the comments of a class and its members.

2) Decision Tree Based Classification: After extracting all the features, we manually label 200 classes of them. We then train a decision tree model to classify Android classes into resource-related classes and non-resource-related classes. Finally, the classification output totally 441 resource-related classes, among which 36 are false positives.

# C. App Parsing

After obtaining resource management classes, ARSM scans app files and lists the invocations of their methods. Generally speaking, we would like to mine two kinds of information from method invocations:

- Correlation. Some methods often occur simultaneously, such as the write operation and flush operation of a file descriptor.   
- Temporal order. Method calls have orders. For example, before read contents from a socket, method init of the socket should be called.

Programs have many branching structures such as if/else and switch statement, and loop structures. In order to capture the wanted information in presence of branching structures, we employ directed cyclic graphs to represent the complicated relationship of methods invocations. The directed cyclic graphs are similar to ordinary control flow graphs but they only contain the method invocations that we are interested in. In this paper, we also call these graphs Complete Sequence Graphs (CSG). Each vertex in a CSG denotes a method invocation with a label indicating the invoked method. Similarly, each directed edge denotes the possible execution order between two statements. The definition of a CSG is as follows:

Definition 1. Given a control flow graph G with $V(G)$ denoting its vertices and $E(G)$ denoting its directed edges, and a set of selected vertices $S = \{v\}$ . The complete sequence graph is a graph C such that (1) $V(C) = S$ , (2) there exists a directed path from vertex u to v in C if and only if edge $(u, v)$ is in graph G.

In CSG, method invocations' correlation and temporal order are captured by directed edges between vertices. An edge from $u$ to $v$ means that there is a path in original code in which $u$ and $v$ appear together and $v$ appears after $u$ . No edge between $u$ and $v$ means that they never appear together in program's execution. A program's structure information is hidden in its CSG's topology. For example, cycles in CSG indicate loops in code.

ARSM parses apk files directly and uses Jimple code $[14]$ , an intermediate representation of Java programs to facilitate analysis. Then ARSM transfers Jimple code of apps into a set of CSGs. Each CSG in them represents a programming unit. A unit can be a method, an Activity class and a Service Class. The transformation process is accomplished in three steps. At first, ARSM builds a intra-procedural control flow graph of chosen statements called sifted control flow graph for each method in the application. Then complete sequence graph is constructed from the sifted control flow graph derived above. In the last step, we perform inter-procedural analysis and embed android components' lifecycle information.

ARSM divides statements into four categories, i.e., control statements $cs$ , intra-application method invocation statements $ims$ , seed method invocation statements $sms$ and no-target statements $ns$ . Control statements are branches statements except goto statement. Intra-application method invocation statements are statements which invoke methods from the app itself and seed method invocation statements invoke methods from seed classes. The rest statements are classified into no-target statements which we believe have no relevance with resource management. During parsing, $ns$ are straightly discarded, while $cs$ and $sms$ are processed to construct CSGs. Since $ims$ invoke intra-application methods, they are left for inter-procedural analysis.

In order to convert a control flow graph to a CSG, ARSM proposes an algorithm in Algorithm 1. We demonstrate the transformation with Figure 2 and Figure 3. Figure 2 is the control flow graph built from the sample code in Listing 3. In Figure 3a, all ns and cs vertices are removed and the edges between ims and sms are reserved. Edges between any pair of connected vertices are added and the final CSG in Figure 3b is constructed.

# D. Inter-Procedural and Life Cycle Analysis

1) Inter-Procedural Analysis: In the previous section, we build CSGs for each method to capture the usage of seed classes' methods. In this section, we perform interprocedural analysis with Android components' life cycle taken into account.

```txt
private void getSamples() { //Process of recording
    if (mAudioRecord == null) return;
    short [] audioBuffer = new short[mAudioBufferSampleSize];
    mAudioRecord.startRecording(); // Start recording
    int audioRecordingState = mAudioRecord.getRecordingState();
    if (audioRecordingState != AudioRecord.
    RECORDSTATE_RECORDING) {
    finish );
    }
    while (inRecordMode) {
    int samplesRead = mAudioRecord.read(audioBuffer, 0,
    mAudioBufferSampleSize); // Read samples from sensor
    }
    mAudioRecord.stop(); // Stop recording
} 
```  
Listing 3. Example code.

![](images/76af5f71f5ad632e91b83f72ebee8208215afd29cdfa1749244408da11aa1ed9.jpg)



Figure 2. Graph-based representation: Control Flow Graph.

![](images/693d2e4562ef4becea582b612de2c08a19c72c8e7308a46b17baa89ac8df1212.jpg)



![](images/87497e68a3dcdbc39dd6f43df81aa4c99b17997e45999a7d305149784fe4c912.jpg)



Figure 3. Graph-based representation: Sifted Control Graph and Complete Sequence Graph.

![](images/a927715f4d3bcc2301cf861721b5f01c14074e9b643f7460ae9a4190f9cbcd78.jpg)



![](images/5832fb5012055308cc04f876ef78a512ee57580244e33f39e147af96a2fdda88.jpg)



Figure 4. Lifecycle of activities and services.

Algorithm 1 CSG construction algorithm.   
Input: Control flow graph G
Output: Complete sequence graph $G'$ with only $ims(c)$ and $sms(c)$ statements
1: for each vertex v in G do
2: if v is cs or ns then
3: add edges from v's predecessors to v's successors
4: remove v
5: end if
6: end for

ARSM uses Dexpler [15] to construct call graph. From constructed call graph, each method invocation statement is linked with its target method. For method $m_{0}$ with its complete sequence graph $g_{0}$ , ARSM replaces all ims vertices $\{n_{i}\}$ in $g_{0}$ with their target methods' CSG $\{g_{i}\}$ . As in $g_{i}$ , CSG ims vertices may still exist, the replacement process can go for many rounds until all the ims vertices are replaced in $g_{0}$ . But this is time-consuming and increases the burden of data mining. And if a method is called by many other methods, its graph will appear in many graphs in the dataset and affects frequent pattern mining. To avoid bad influences, ARSM limits the number of rounds by maxDepth. After at most maxDepth rounds of replacement, inter-procedural analysis stops replacement and delete ims vertices. After this step, all ims vertices are either replaced or deleted and only sms vertices remain. The detailed process is described in Algorithm 2.

2) Life Cycle: Activities and services are two main components in Android. Activity acts like a web on PC and has interactions with users. Services, without a visual interface, are used to implement long-running background tasks or used as a rich communications API that can be called by other apps. Both of them share a system-defined life cycle mechanism. When their state are changed by users or by the operating system, OS notifies them by calling corresponding callback methods. For example, to start an activity, OS will invoke the following methods from this activity: onCreate(), onStart(), and onResume() in series. When the activity is obscured, methods onPause(), onStop() will be called. The callback methods' invoking sequence follows a system-defined order. This means that for activities and services, the execution order of their callback methods follows a predefined pattern.

We use these invocation patterns as priori knowledge to help us reveal resource usage patterns in event-driven systems. In specific, we manually construct a dummy method for each activity and service, based on their life cycle. This dummy method is composed of component's main lifecycle-relate callback methods. And its control flow graph follows the execution order of these methods defined by the Android platform. The template control flow graph of faked functions for activity and service in shown in Figure 4. After generating dummy methods, we build CSGs for the involved callback methods in the component. Then callback methods' CSGs are embedded into dummy method's CSG using Algorithm 2.

Algorithm 2 Inter-procedure analysis algorithm.   
Input: A set S of all project methods with corresponding complete sequence graph. $S=\{(m_{i}, g_{i})\}$ . A target method m.

Output: Complete sequence graph G for m with only sms(c) vertices
1: round = 0
2: G = a copy of $g_{m}$ 3: while (round < maxDepth) do
4:    for each ims vertex $v_{i}$ in G do
5:    get $v_{i}$ 's predecessors $\{b_{v,j}\}$ and successors $\{f_{v,k}\}$ 6:    get CSG of $v_{i}$ 's invoked method $g_{v_{i}}$ 7:    for each vertex $u_{i}$ in G do
8:    add edge from every node in $\{b_{v,k}\}$ to $u_{i}$ 9:    add edge from $u_{i}$ to every node in $\{f_{v,k}\}$ 10:    end for
11:    end for
12:    round = round + 1
13: end while
14: for each ims vertex $v_{i}$ in G do
15:    add edge from every node in $v_{i}$ 's predecessors $\{b_{v,k}\}$ to every node in $v_{i}$ 's successors $\{f_{v,k}\}$ 16:    remove $v_{i}$ from G
17: end for
18: return G

# E. Frequent Subgraph Mining

In this section, we reduce the mining problem into a closed frequent subgraph mining problem.

Frequent subgraph mining works on graphs with labeled edges and vertices. Let's denote a labeled graph by $g$ , its vertex set by $V(g)$ , edge set by $E(g)$ , and the label function by $l$ respectively. Correspondingly, the label of vertex $v$ is denoted as $l(v)$ , and edge e' label is denoted as $l(e)$ . A graph $g$ is a subgraph of $g'$ if and only if an subgraph isomorphism exists between $g$ and $g'$ . Graph $g'$ is also referred to as a supergraph of $g$ .

Definition 2. A subgraph isomorphism is an injective function $f$ from $V(g)$ to $V(g')$ , such that for any vertex $u$ in $V(g)$ , $u$ 's label in $g$ is equal to $f(u)$ 's label in $g'$ and for any edge $e = (u, v)$ in $E(g)$ , edge $(f(u), f(v))$ is in graph $g'$ and shares same label with $(u, v)$ in $g$ .

Given a graph dataset $D = g1, g2, ..., gn$ , support of a graph g (denoted as $support(g)$ ) is the number of graphs in which g is a subgraph. The frequent subgraph mining problem is given a threshold min\_support and a graph dataset D, finding all subgraphs whose support in D is at least min\_support. Closed subgraphs are subgraphs whose support is larger than the support of its any supergraphs. Using closed subgraph could help prune redundant sub-patterns with same support.

![](images/066defb8a9060509fbb8990665b5add0195ca81c6c6c122770d2197f99dfeeae.jpg)



(a) bytecode size (in KBs)

![](images/a034eec2c1086368ac4c4d646d581d87c40fe2404bd2bd91d785cce510183695.jpg)



(b) parsing time (in seconds)   
Figure 5. The distributions of bytecode size and parsing time of apps.

Finding closed frequent graph provides us convenience in identifying pattern violations in the graph dataset. Consider a situation in which graph g1 is a subgraph of g2 and both of them is closed frequent subgraph. That means that in some graphs g1 is presented while g2-g1 is absent. If such a case, with support of support(g1)-support(g2), is rare, it indicates that this may be a potential bug.

Using closed frequent subgraph mining enjoys several benefits: (1) Graphs retain both the correlation and spatial order information of code; (2) Graphs are more compact data structures than sequences. A single graph may contain several sequences. (3) Closed frequent subgraph greatly reduces the number of resulting patterns.

# III. IMPLEMENTATION

ARSM is written in Java and implemented on Android platforms. It takes apk files as main input and uses Dexpler to convert Android Dalvik Bytecode to Jimple code. Dexpler is a Soot [16] modification based on Dedexer [17]. Then ARSM parses the Jimple code. Complete sequence graphs of activities and services are firstly constructed using Lifecycle analysis with max depth maxDepth. Then for the remaining methods, ARSM selects those that are not called by methods inside this app and construct CSG for them with the same max depth maxDepth. With the dataset of CSGs, ARSM adopts algorithm gSpan [18] to mine closed frequent subgraphs. Finally, results are presented to the developers to prune extra edges generated during complete sequence graph construction and check the correctness.

# IV. EVALUATION

In experiments, we manually download 100 top rated apps from a popular Android market [19], including Facebook etc. The downloaded apps are in apk file format, each consisting of a bytecode file, a manifest file, several assets files, etc. Only bytecode files contain the information we need for mining. We analyze the size of bytecode file for each app, and depict the results in Figure 5a.

![](images/78cea563517acd0464896ff9ae52895db9a44706ef6a95632ff91951dca8dc8d.jpg)



(a) 20 projects

![](images/9f4c0d07cff2808426bf3872e6a845b4fe03c436131fb3d3bdd5ae8e04272de8.jpg)



(b) 100 projects   
Figure 6. Frequent pattern numbers varying number of projects and min\_support.

![](images/be0e2cd5c01633aa7fbb4228f757693507c1c6736daa567fed4f47949a3abb5d.jpg)



(a) Read from database

![](images/433280c2986af935219f3a4889a996b803eccffffa35a18759d04bb7c1952927.jpg)



(b) Write to database   
Figure 7. Database examples.

To evaluate efficiency of ARSM, we divide its running time into two parts. The first part is the time of parsing apps and generating graph datasets. The second part is the time of mining closed frequent subgraphs. In practice, the mining procedure can always be finished within a few seconds. So we ignore the mining time and evaluate the parsing time in 5. The maximal parsing time is within a few minutes.

Besides running time, we also observe the change of frequent patterns under various number of apps and min\_support values. First we randomly select 20 projects and vary min\_support from 20 to 80. As illustrated in Figure 6a, when min\_support is set to 20, there are as many as 50 closed frequent subgraphs. However, when its value becomes 80, the number of closed frequent subgraphs is 2. Similarly, in Figure 6b we can observe that with 100 apps, the number of frequent patterns also decrease drastically with min\_support.

In the following part of this section, we demonstrate the effectiveness of ARSM through case studies.

# A. Case Study I

First of all, ARSM is able to find specifications in the form of (Resource.acquire() → Resource.release()). In addition, it also captures the frequent behaviour after resource is acquired. For example, Figure 7 are two patterns with respect to SQL database usage in Android. They all include two statements SQLiteOpenHelper.<init>()

![](images/2872a01158b93a22d50bd133850b6fc0ee29306d5da86e05551566c616a0aaea.jpg)



Figure 8. MediaPlayer example.

and SQLiteOpenHelper.close(), which stand for the creation and closure of the database resource. However, between these two statements, the read operation invokes getReadbaleDatabase() method while the write operation calls getWritableDatabase() method. ARSM can distinguish these two patterns although they are very similar to each other.

# B. Case Study II

Figure 8 shows a pattern of MediaPlayer. After a MediaPlayer object is created, various methods can be invoked to set event listeners. As the order of these setOn\*\*\*Listener() methods being called has no predefined order, frequent sequence mining based approaches may treat them as different patterns. While in ARSM, we can represent the pattern using a single pattern, which is more compact. Also, if frequent itemset mining based approaches are applied, the results do not contain the temporal order information and little help can be provided to developers.

# C. Case Study III

The event-driven programming mechanism of mobile platforms renders static analysis more difficult since the execution order between event handlers is hard to tell. To address this issue, ARSM uses lifecycle analysis to reduce the large state space.

Figure 9a is a Camera related pattern revealed using life cycle analysis. It covers the whole process of using a camera, including opening, setting preview display, starting preview, stopping preview and finally releasing camera. In our experiment, without using life analysis, the derived patterns only contain partial information, as illustrated in Figure 9b. Obviously, they are only subgraphs of 9a. The reason is that the usage of camera is always accompanied with user interaction. And event-driven mechanism is implemented to respond to user behaviour. So the camera manipulation actions are distributed in many event-handler methods. Using static analysis without life cycle, only segments of the usage pattern can be captured.

# V. RELATED WORK

# A. Resource Management in Smartphones

Diagnosing resource leaking bugs on smartphone platforms has attracted much attention in recent years. Pathak et al. [6] made the first steps towards diagnosing no-sleep bugs that cause high energy consumptions. They found that many energy issues are due to inappropriate handling of wakelocks. To overcome it, they proposed a compile-time solution based on dataflow analysis techniques to detect missed resource-releasing API calls. Vekris et al. [20] further inspected no-sleep bugs using a inter-procedural data flow analysis framework. They defined a set of more precise wakelock related specifications. Liu et al. [21] studied the energy inefficiency problem caused by ineffective use of sensors and their data. They built a tool called GreenDroid to analyze sensory data utilization and report actionable information to developers to help locate root cause. Jindal et al. [7] uncovered sleep conflicts in smartphone device drivers and classified them into four types. Then they presented a runtime debugging system to avoid sleep conflicts. Our approach differs from these work in that they all target on predefined types of bugs, while our work is to take advantage of data mining techniques to automatically discover resource management specifications and then use the results to debug.

![](images/ce344a14a9ebb7df42475cc32dc338f65de155b4be7d0662c63f8d221481af54.jpg)



(a) With lifecycle analysis

![](images/25747231de019ac6faa0a4492a6afc5fd161aeb70656c05c6265463ca78459df.jpg)



(b) Without lifecycle analysis   
Figure 9. Camera example

# B. Energy Debugging in Smartphones

Abnormal energy consumption of smartphones is becoming a concern of millions of users. However, it is usually difficult for ordinary users to tell which app is draining the battery. Ma et al. [5] proposed eDoctor, which can help users diagnose abnormal battery drain issues by leveraging execution phases. Oliner et al. [22] developed a collaborative statistical tool named Carat to detect and diagnose energy bugs using information gathered from thousands of users. Tools such as ARO [23] and eprof [24] can also expose resource and energy inefficiency in mobile apps. Our work is complementary to theirs because they focus on helping ordinary users identifying buggy apps, while our objective is to assist developers to locate and avoid bugs that violate certain patterns.

# C. Specification Mining

Our work is also related to specification mining. PR-Miner [9] employs frequent pattern mining to extract implicit rules from large software code. It neglects temporal property of API calls and can only detect the co-occurrence of them. [10] proposes a static path generation approach to gather sequence information. However, the number of paths generated is usually exponential. In practice, it is computationally infeasible to enumerate all the paths, especially considering the event-driven characteristics of smartphone apps. [11] proposed an iterative mining approach to mining resource releasing specifications. MAPO [25] is a software repository mining framework that help developers learn API usage from open source repositories. However, MAPO only mines code fragments and ignores the control flow information of programs. These methods are not tailored for smartphone apps. As we illustrated previously, they may suffer from large search space or overlook specifications in apps.

# VI. CONCLUSION

We develop a static analysis tool ARSM to automatically extract resource management specifications from off-the-shelf apps. Using apk fils as input, ARSM is able to analyze the frequent usage patterns of resource related classes. By combining inter-procedural analysis and life cycle analysis, we tackle the problem of unknown methods invocation order caused by event-driven programming mechanism. Experiments shows that using life cycle analysis ARSM can generate more complete specifications. In addition, ARSM is very fast. It can parse an app in 122 seconds on average.

# ACKNOWLEDGMENT

This study is supported in part by NSF China Projects No. 61472211 and 61472219.

# REFERENCES

[1] C. Wu, Z. Yang, Y. Liu, and W. Xi, “Will: Wireless indoor localization without site survey,” in Proceedings of IEEE INFOCOM, 2012.   
[2] P. Zhou, Y. Zheng, Z. Li, M. Li, and G. Shen, “Iodetector: A generic service for indoor outdoor detection,” in Proceedings of ACM SenSys, 2012.   
[3] W. Wei, F. Xu, and Q. Li, “Mobishare: Flexible privacy-preserving location sharing in mobile online social networks,” in Proceedings of IEEE INFOCOM, 2012.   
[4] “Latest facebook update causing big battery drain,” http://http://phandroid.com/2010/08/05/latest-facebook-update-causing-big-battery-drain/.   
[5] X. Ma, P. Huang, X. Jin, P. Wang, S. Park, D. Shen, Y. Zhou, L. K. Saul, and G. M. Voelker, “edoctor: automatically diagnosing abnormal battery drain issues on smartphones,” in Proceedings of USENIX NSDI, 2013.   
[6] A. Pathak, A. Jindal, Y. C. Hu, and S. P. Midkiff, “What is keeping my phone awake?: characterizing and detecting no-sleep energy bugs in smartphone apps,” in Proceedings of ACM MobiSys, 2012.   
[7] A. Jindal, A. Pathak, Y. C. Hu, and S. Midkiff, “Hypnos: understanding and treating sleep conflicts in smartphones,” in Proceedings of ACM EuroSys, 2013.

[8] “An example of wakelock usage,” https://github.com/commonsguy/cwac-wakeful.   
[9] Z. Li and Y. Zhou, “Pr-miner: Automatically extracting implicit programming rules and detecting violations in large software code,” in Proceedings of ACM FSE, 2005.   
[10] M. Acharya, T. Xie, J. Pei, and J. Xu, “Mining api patterns as partial orders from source code: from usage scenarios to specifications,” in Proceedings of ACM FSE, 2007.   
[11] Q. Wu, G. Liang, Q. Wang, T. Xie, and H. Mei, “Iterative mining of resource-releasing specifications,” in Proceedings of IEEE/ACM ASE, 2011.   
[12] C. Hu and I. Neamtiu, “Automating gui testing for android applications,” in Proceedings of ACM International Workshop on Automation of Software Test, 2011.   
[13] “/an example code of audiorecord usage,” http://www.java2s.com/Code/Android/Media/AudioRecording.htm.   
[14] R. Vallee-Rai and L. J. Hendren, “Jimple: Simplifying java bytecode for analyses and transformations,” 1998.   
[15] A. Bartel, J. Klein, M. Monperrus, and Y. Le Traon, “Dexpler: Converting android dalvik bytecode to jimple for static analysis with soot,” in ACM Sigplan International Workshop on the State Of The Art in Java Program Analysis, 2012.   
[16] R. Vallée-Rai, P. Co, E. Gagnon, L. Hendren, P. Lam, and V. Sundaresan, “Soot: A java bytecode optimization framework,” in CASCON First Decade High Impact Papers, 2010.   
[17] “Dedexer,” http://dedexer.sourceforge.net.   
[18] X. Yan and J. Han, “Closegraph: mining closed frequent graph patterns,” in Proceedings of ACM SIGKDD, 2003.   
[19] “Apk downloading website,” http://apk.hiapk.com.   
[20] P. Vekris, R. Jhala, S. Lerner, and Y. Agarwal, “Towards verifying android apps for the absence of no-sleep energy bugs,” in Proceedings of USENIX HotPower, 2012.   
[21] Y. Liu, C. Xu, and S. Cheung, “Finding sensor related energy black holes in smartphone applications,” in Proceedings of IEEE PerCom, 2013.   
[22] A. Oliner, A. Padmanabha Iyer, I. Stoica, E. Lagerspetz, and S. Tarkoma, “Carat: Collaborative energy diagnosis for mobile devices,” EECS Department, University of California, Berkeley, Tech. Rep. UCB/EECS-2013-17, Mar 2013.   
[23] F. Qian, Z. Wang, A. Gerber, Z. Mao, S. Sen, and O. Spatscheck, “Profiling resource usage for mobile applications: a cross-layer approach,” in Proceedings of ACM MobiSys, 2011.   
[24] A. Pathak, Y. C. Hu, and M. Zhang, “Where is the energy spent inside my app?: fine grained energy accounting on smartphones with eprof,” in Proceedings of ACM MobiSys, 2012.   
[25] T. Xie and J. Pei, “Mapo: Mining api usages from open source repositories,” in Proceedings of ACM MSR, 2006.