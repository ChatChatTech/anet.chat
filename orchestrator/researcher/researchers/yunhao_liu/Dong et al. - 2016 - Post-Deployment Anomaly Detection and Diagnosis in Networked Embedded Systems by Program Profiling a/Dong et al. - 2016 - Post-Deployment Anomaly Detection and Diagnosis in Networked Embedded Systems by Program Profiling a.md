# Post-Deployment Anomaly Detection and Diagnosis in Networked Embedded Systems by Program Profiling and Symptom Mining

Wei Dong, Member, IEEE, Luyao Luo, Chun Chen, Member, IEEE, Jiajun Bu, Member, IEEE, Xue Liu, Member, IEEE, Yunhao Liu, Fellow, IEEE

Abstract—Detecting and diagnosing anomalies in networked embedded systems like sensor networks is a very difficult task, due to the variable workloads and severe resource constraints. In this paper, we focus on how to aid bug diagnosis after the system has been deployed. We notice that most node-level debugging tools can provide detailed program information inside the node but fail to detect when and where a problem occurs in the network. On the other hand, most network-level diagnosis tools can effectively detect a problem from the network but fail to narrow down the problem within the node because they lack detailed program information. To close the gap, we propose D2, a new method for post-deployment anomaly detection and diagnosis in networked embedded systems by combining program profiling and symptom mining. D2 employs binary instrumentation to perform lightweight function count profiling. Based on the statistics, D2 uses PCA (Principal Component Analysis) based approach for automatically detecting network anomalies. Compared with previous methods, D2 is able to point programmers closer to the most likely causes by a novel approach combining statistical tests and program call graph analysis. We implement our method based on TinyOS 2.1.1 and evaluate its effectiveness by case studies in the development of a working sensor network. Results show that our method can aid programmers to diagnose problems quickly in real-world sensor network systems, and at the same time, incurs an acceptable overhead to the running system.

Index Terms—Networked embedded systems; sensor networks; diagnosis; program profiling; symptom mining

# 1 INTRODUCTION

Detecting and diagnosing anomalies in networked embedded systems like sensor networks is a very difficult task, due to the variable workloads and severe resource constraints. Many real-world deployments exemplify such difficulties.

LOFAR-agro is a sensor network consisting of about 100 nodes for precision agriculture in the Netherlands during the year 2004-2005 [1]. The software components include (1) TMAC, an adaptive low-duty-cycle MAC protocol, (2) MintRoute [2], a multihop routing protocol, (3) Deluge [3], a wireless reprogramming protocol, and (4) the LOFAR-agro application. The developers encounter numerous problems during the deployment. They observe that the system exhibits low data rate due to the malfunction of TMAC. Detailed diagnosis requires a more than thorough understanding of the TinyOS structure and its components. The concrete causes are thus left unclear due to tight project schedules.

GreenOrbs is a large-scale sensor network system consisting of over 300 nodes for forestry applications starting from the year 2009 [4]. The initial software components include (1) CTP [5], a multihop routing protocol, (2) FTSP [6], a global time synchronization protocol, and (3) the GreenOrbs application. During the deployment in the Zhejiang Forestry

• W. Dong, L. Luo, C. Chen, J. Bu are with the College of Computer Science, Zhejiang University, China. E-mail: dongw@zju.edu.cn.   
• X. Liu is with School of Computer Science, McGill University, Canada. Email: xueliu@cs.mcgill.ca   
• Y. Liu is MOE Key Lab for Information System Security, School of Software, TNLIST, Tsinghua University, China. Email: yunhao@greenorbs.com

University’s woodland, we often observe that some nodes frequently lose synchronization with the rest of the network. After many rounds of careful detections involving both code reviews and testbed experiments, we eventually find out the causes. First, the TinyOS clock driver would occasionally return bogus local timestamps. Second, FTSP does not check the validity of the timestamps.

These experiences show us the importance of problem detection and diagnosis as well as their practical challenges in real-world systems. There are numerous methods to aid problem diagnosis in the literature, such as static verification [7], [8], interactive debugging [9], [10], tracing and logging [11], [12], [13], network-level diagnosis [14], [15], [16], etc. In this paper, we focus on functional problems after the system is deployed. Simulation and testbed environments are inevitably different from real deployments. Some problems can only manifest themselves after deployments. Functional problems should be detected and diagnosed in time since their occurrences at some nodes usually suppress their normal work.

We notice that most node-level debugging tools can provide detailed program information inside the node but may fail to detect when and where a problem occurs in the network. On the other hand, most network-level diagnosis tools can effectively detect a problem from the network but may fail to narrow down the problem within the node because they lack detailed program information. A simple combination of the above two will cause large overhead. Moreover, some errors detected by network-level tools may not be reproducible and thus cannot be easily diagnosed by the node-level tools.

To close the gap, we propose D2, a post-deployment anomaly detection and diagnosis method by combining program profiling and symptom mining. Today’s embedded sensor software has a low visibility in exposing detailed execution behaviors. As opposed to previous instrumentation methods which either incur a large overhead [11] or demand special hardware [12], we employ binary instrumentation to perform lightweight function count profiling. The statistics at the function level provide us fine-grained information for detailed reasoning. Unlike previous methods which require application programmers’ efforts for providing specific network metrics [17], our method treats the program as a black box, thus is scalable for a wide range of applications. Based on the statistics, we employ PCA (Principal Component Analysis) based approach for automatically detecting network problems. Previous network-level diagnosis methods only detect network problems at the node level or link level [15], [18], D2 is able to point programmers closer to the most likely causes by a novel approach combining statistical tests and program call graph analysis.

It is worth noting some of the most important features in D2.

• D2 does not require efforts from the developers. The source code does not need to be modified and no libraries need to be linked into the executable file. Therefore, it is easily scalable to a wide range of applications.   
• D2 does not affect program execution unless the sink node issues a profiling request. D2 can be installed or uninstalled easily at the runtime so that we can use it when needed and stop it otherwise.   
• D2 uses lightweight function count profiling. Counterbased profiling incurs less overhead than event-based profiling.   
• Despite lightweight, D2 provides function-level information. Note that functions for sensor networks are typically very short. Hence function counts for sensor network applications carry more execution information than those for PCs.   
• D2 automates the process of problem identification and causal reasoning. The diagnosis report provides detailed information for problem solving.   
• Although we currently implement D2 based on TinyOS, its design principles can also be applied to other OSes since binary instrumentation within D2 operates at the binary level.

We evaluate D2’s effectiveness by case studies in real-world sensor network applications. Results show that our method incurs an acceptable overhead and can aid programmers to diagnose real-world problems quickly.

We specialize in detecting and diagnosing functional problems after deployment, which leads to two important design considerations. First, the tool should be lightweight so that normal operations are not severely affected. Second, the profiling of function executions is needed for fine-grained diagnosis inside the node.

It is also important to mention the limitations of our tool. First, in order to correctly detect an anomaly, system data (i.e., program profile) about the anomaly needs to be collected since D2 relies on the collected system data for problem detection

Table 1: Comparison of various existing tools 

<table><tr><td colspan="2">Tools</td><td>Post-deployment diagnosis ability</td><td>Automatic detection</td><td>Code-level diagnosis</td></tr><tr><td rowspan="4">Pre-deployment tools</td><td>T-Check</td><td>✕</td><td>√</td><td>√</td></tr><tr><td>KleeNet</td><td>✕</td><td>√</td><td>√</td></tr><tr><td>T-Morph</td><td>✕</td><td>✕</td><td>√</td></tr><tr><td>Semtomist</td><td>✕</td><td>√</td><td>√</td></tr><tr><td rowspan="3">Debugging tools</td><td>Clairvoyant</td><td>√</td><td>✕</td><td>√</td></tr><tr><td>NodeMD</td><td>√</td><td>✕</td><td>√</td></tr><tr><td>DT</td><td>√</td><td>✕</td><td>√</td></tr><tr><td rowspan="5">Logging and tracing tools</td><td>EnviroLog</td><td>√</td><td>✕</td><td>√</td></tr><tr><td>DustMiner</td><td>✕</td><td>√</td><td>√</td></tr><tr><td>TinyTracer</td><td>✕</td><td>✕</td><td>√</td></tr><tr><td>LIS</td><td>√</td><td>✕</td><td>√</td></tr><tr><td>Aveksha</td><td>✕</td><td>✕</td><td>√</td></tr><tr><td rowspan="5">Network-level diagnosis tools</td><td>Sympathy</td><td>√</td><td>√</td><td>✕</td></tr><tr><td>PAD</td><td>√</td><td>√</td><td>✕</td></tr><tr><td>AD</td><td>√</td><td>√</td><td>✕</td></tr><tr><td>TinyD2</td><td>√</td><td>√</td><td>✕</td></tr><tr><td>LD2</td><td>√</td><td>√</td><td>✕</td></tr><tr><td>This paper</td><td>D2</td><td>√</td><td>√</td><td>√</td></tr></table>

and diagnosis. If a non-producible anomaly happens before D2 is turned on, this anomaly is left undetected. Second, D2’s function count profiling approach, albeit lightweight, loses other detailed function execution information, e.g., the return value of each function. D2 can be extended to incorporate more advanced profiling methods such as call site profiling with return values [19], at the cost of large profiling overhead. Third, D2 cannot detect concurrency problems due to improper interleavings of functions. Detecting such bugs requires detailed function-level logging to track the order of function executions using tools such as TinyTracer [11] or LIS [20], [21].

The contributions of this work are summarized as follows.

• We propose a new method for post-deployment anomaly detection and diagnosis in networked embedded systems by combining program profiling and symptom mining.   
• We propose a novel approach combining statistical tests and program call graph analysis to point programmers closer to the most likely causes inside the node.   
• We implement our method and demonstrate its effectiveness using case studies from real sensor network applications.

The rest of this paper is structured as follows. Section 2 describes the related work. Section 3 provides the preliminaries. Section 4 presents the design principles. Section 5 describes D2’s extensions. Section 6 shows the evaluation results, and finally, Section 7 concludes this paper and gives directions of future work.

# 2 RELATED WORK

There are numerous research works related to anomaly detection and diagnosis. Table 1 summarizes diagnosis tools for networked embedded systems. We classify existing works into four main categories: pre-deployment tools, debugging tools, logging and tracing, network-level diagnosis.

These diagnosis tools provide the following features:

• Post-deployment diagnosis ability. For post-deployment diagnosis, the tool should incur small runtime overhead. Moreover, it should be installed or uninstalled easily at the runtime so that we can use it when needed and stop it otherwise. All the mentioned pre-deployment tools lack post-deployment diagnosis ability since they require finegrained information that is only affordable by simulators (e.g., Sentomist [22], T-Morph [23]). Some of the tools (e.g., DustMiner [24] and LIS [20]) cannot be uninstalled easily: once installed, they affect the program’s execution and incur runtime overhead to the system.   
• Automatic detection. Automatic anomaly detection is very important. Most debugging and logging tools (except DustMiner [24]) lack automatic detection ability. Instead, they require developers’ experiences to record or probe the most appropriate program information.   
• Code-level diagnosis. Code-level diagnosis is very useful for developers. In particular, descriptive diagnosis reports are desired to fix the program problems. All the mentioned network-level diagnosis tools can only pinpoint the problematic nodes or links.

Table 1 shows that none of these tools achieve all these features simultaneously.

Pre-deployment tools. T-Check [7] is a tool that uses random walks and explicit state model checking to find safety and liveness errors in sensor network applications running on TinyOS. T-Check is based on the TOSSIM simulator and thus loses the ability to detect and diagnose real-world sensor network software. KleeNet [8] uses symbolic analysis to generate test cases for sensor network code. T-Morph [23] is a novel tool to mine, visualize, and verify the execution patterns of TinyOS applications. T-Morph abstracts the dynamic execution process of a TinyOS application into simple, structured application behavior models, which well reflect how the static source codes are executed. Sentomist [22] uses the number of executed instructions during interrupt handling intervals to find transient bugs.

Both T-Morph and Sentomist are based on Avrora [25]—an instruction level simulator for the mica platform. Such detailed information can only be acquired in simulations and is not affordable in real-world sensor network deployments. Unlike Sentomist, D2 further generates diagnosis reports to facilitate problem diagnosis.

Debugging tools. Clairvoyant [9] is a comprehensive source-level debugger for wireless embedded networks. With Clairvoyant, a developer can execute GDB-like commands to interactively debug the sensor nodes. NodeMD [26] is designed to diagnose node-level faults in sensor network applications. It focuses on catching software faults before they completely disable the remote sensor node, so that the user can be provided with diagnostic information to troubleshoot the root cause. Declarative Tracepoint (DT) [10] integrates benefits of previous debugging techniques and uses a SQL-based language interface for debugging.

Although these tools facilitate fixing the already-seen bugs, they cannot automatically identify such bugs.

Logging and tracing. EnviroLog [27] aims to improve repeatability of experimental testing of distributed event-driven applications, based on the observation that the system state can change depending on the event sequence and timing. EnviroLog provides an event recording and replay service that captures and replays events with the help of the nonvolatile flash. DustMiner [24] identifies bugs in sensor network software by checking discriminative log patterns. Sundaram et al. propose TinyTracer, an efficient intra-procedural and interprocedural control-flow tracing algorithm that generates the traces of all interleaving concurrent events [11]. AVEKSHA [12] is a hardware-software approach for tracing events in a non-intrusive manner. LIS (Log Instrumentation Specification) [20], [21] performs insertion of low overhead logging calls into a system. At the heart of LIS are the three scoping declarations (i.e., global, local, point) that direct the assignment of the token identifier that is logged by the system. By separating the local and point scope from the global scope, LIS can significantly reduce the number of bits required to log a given token.

Compared with some approaches with manual logging, D2 uses automatic function count profiling. Although it is possible that manual logging can detect finer-grained program problems (e.g., concurrency problems) by logging important events or variables, it highly depends on developers’ experiences. For the Internet or high-performance distributed systems, the logging information is typically available [28]. However, for most sensor network software, the logging information is usually unavailable since it is often not a good idea for detailed logging which incurs a large runtime overhead. D2’s counter-based profiling can be more efficient than LIS’s eventbased profiling and we will make a quantitative comparison in Section 6.

Network-level diagnosis. Sympathy [14] collects multiple network metrics and uses a decision tree to localize the failures. PAD [15] uses lightweight network monitoring and Bayesian network based analysis to infer network failures and their causes. Agnostic Diagnosis [17] also collects multiple network metrics and uses anomaly detection on the correlation graph to discover silent failures. TinyD2 [16] uses the concept of self-diagnosis in which each sensor can join the fault decision process. TinyD2 [16] plants a finite state machine into each sensor node, enabling them to accordingly change the diagnosis state. LD2 [18] is a in-network diagnosis approach which conducts the diagnosis process in a local area. LD2 achieves diagnosis decision through distributed evidence fusion operations.

Although these tools can automatically narrow down the problem to the node level or link level, they cannot localize the problem inside the node, e.g., the program code. Moreover, they demand manual efforts to write customized node-level diagnosis engine or additional codes for obtaining network metrics.

# 3 PRELIMINARIES

This section introduces the necessary techniques. The trampoline technique is used in the binary instrumentation phase in order to perform the actual profiling task without significantly modifying the original code. One-class SVM (Support Vector

![](images/b51564c761f99c4f351dac179bff277ef20e010460e24ac380c17b9b2ab18336.jpg)



Fig. 1: D2 overview.

Machine) and PCA (Principal Component Analysis) are two well-known methods for anomaly detection. D2 uses PCA for anomaly detection.

The trampoline technique. In embedded systems, trampolines are short snippets of code that start up other snippets of code. A trampoline is inserted into the target binary, such that the target execution is rerouted to the patch, before it returns for execution of the original code [29]. In our case, we use the trampoline technique to redirect the control to a target function which performs the actual profiling tasks.

SVM, one-class SVM and PCA. SVM is a statistical method that infers how two classes of points are different from each other. Given a set of labeled data points, the algorithm can find a hyperplane that best separates a set of unlabeled data points into the two different classes. The hyperplane is considered as the boundary of the two classes.

When it is used for anomaly detection, what we have is a set of unlabeled ones. A trick is therefore to assume that all input samples belong to one class, i.e., the normal class, which however contains some misclassified ones. Also consider that there is a virtual outlier class, which naturally contains the origin in a d-dimensional space and some samples that are misclassified to the normal class. We can then apply SVM to find a boundary to separate these two classes. Such a variant of SVM is called one-class SVM [22].

PCA is a way of identifying patterns in data, and expressing the data in such a way as to highlight their similarities and differences. PCA is a powerful tool for analyzing data of high dimension and has been applied in many areas. PCA captures patterns in high-dimensional data by automatically choosing a set of principal components (i.e., coordinates). When it is used for anomaly detection, we consider the principal components form the normal subspace. The distance from a data point to the normal subspace can be used for anomaly detection. A simple heuristic is that the farther it is away from the normal subspace, the more suspicious it is as an outlier. The runtime overhead of PCA is linear with the number of feature vectors and thus can scale to large data.

Both one-class SVM and PCA can model the majority characteristics of a set of unclassified samples and determine whether a sample is an outlier. D2 uses PCA for anomaly detection. We will explain PCA is a more suitable choice in our case in Section 4.3.

# 4 DESIGN

Figure 1 shows an overview of D2. The sink node can issue a request to notify a subnet of nodes to transition into profiling mode. Once requested, the D2 module on the sensor node employs binary instrumentation to perform function count profiling. Snapshots of the profiles are either transferred to the sink for real-time analysis or stored on the sensor nodes’ external flash for later analysis.

![](images/4ee978f0a28ca1967cd72a550e6da26b61a6f27f4d892ce73428321bdcf3b191.jpg)



Fig. 2: RAM layout on TelosB nodes.

The D2 module at the PC side performs analysis on the collected profiles. First, D2 performs PCA-based anomaly detection to identify when and where potential problems occur in the network. Second, D2 tries to narrow down the problem to function level by considering statistical divergence of functions or function ratios between normal profiles and abnormal profiles. The diagnosis report lists a set of suspicious functions or function ratios. The result is further refined by their causal relationships which are obtained by inspecting the function call graph of the program.

# 4.1 Binary instrumentation

The D2 module on the sensor node is responsible for instrumenting the program binary to perform function count profiling. The D2 module employs binary instrumentation technique which inserts additional code and data into the executable, modifying the runtime behaviors to perform the needed task [30]. In addition, D2 maintains necessary information to undo the profiling task.

Function count profiling needs to find the start of each function. The D2 module performs a simple disassembly of the program, discovering every function block by examining the destination of every call instruction in the code. This approach will not reveal functions that are called only by function pointers. However, such functions are not common in TinyOS, and if they must be profiled then the symbol table generated from a compiler can be loaded.

Function count profiling also requires a set of counters to be allocated in order to count the number of each function’s executions. The RAM on current sensor nodes are divided into three sections as shown in the left part in Figure 2. The program’s initialized data, .data, is allocated at the start of the RAM. The program’s uninitialized data, .bss, is allocated following the .data. The program’s execution stack grows from the bottom of the RAM. D2 tries to allocate these counters after the .bss section so that the program’s data would not be corrupted and the stack space can be maximized. On PCs, it is easy to find out the end of .bss by looking at the value of end bss in the ELF file [31], indicating the end of the .bss section. On the sensor nodes, however, only the raw binary file is stored and detailed metadata information is lacking. D2 finds out the end of .bss by examining the initialization procedure whose program logic is common for almost all applications. D2 obtains the end of .bss section by examining the corresponding constants encoded in the instructions. D2 allocates 4 bytes for each function counter. For a complex application like GreenOrbs with about 280 functions, the overall RAM overhead is 1,120 bytes. This is acceptable compared with a total of 10KB RAM on TelosB nodes.

![](images/c86a751eb97885030b9244dc1fd0159516919265b54a08f701f215dbada34a1c.jpg)



Fig. 3: The trampoline technique.

D2 uses the trampoline technique to replace the instruction block at the start of each function by a call instruction so as to direct the control to the trampoline which performs the actual profiling.

Figure 3 shows the basic idea of the trampoline technique. We explain each step in the instrumentation process as follows.

1) At the start of each function, we replace the original instructions to a call instruction which directs the control to the corresponding trampoline. A call instruction may replace one or two instructions as the instructions are of variable lengths. The replaced instructions are “mirrored” at the corresponding trampoline and meant to be executed after function count profiling is finished.   
2) The call instruction directs the function’s control to its trampoline. The trampoline first saves the context by saving values of registers that will be used by the trampoline. This is achieved by pushing the values onto the stack.   
3) The trampoline executes the profiling logic. First, the corresponding function counter is incremented. Second, a checking procedure is executed. The main task of the checking procedure is to check whether it is the right time to take a snapshot of the function counters by transferring them to the sink or storing them on the local external flash.   
4) The context is restored by poping values from the stack to corresponding registers.   
5) The mirrored instructions in the original function are executed. It is worth mentioning that if we have to replace relative instructions, we cannot simply mirror the instructions at a different location. Instead, we should translate the instructions to use the absolute address.   
6) The control is finally transferred to the function.

We have mentioned that a checking procedure needs to be invoked in order to take snapshots of the function counters. These snapshots are used to create features over a time window for problem detection. For traditional PC software, snapshots may not be needed [19] because the execution of most PC software (such as latex, gcc) finishes in a short time. On the other hand, sensor software is executed for a long duration. Program features over a relatively short time window will enable problem detection at a fine-grained time granularity.

![](images/74eb2996fa5da2a342ead27ec26376532ce2f8b5e88e40bbd20d910e6e84d13c.jpg)



Fig. 4: An illustrative example for problem detection.

A key problem is how to determine when we should take snapshots. A naive approach would take snapshots at a predetermined time window. This approach will cause extra overhead if no activities happen during the time window. It is not uncommon that sensor nodes perform tasks periodically and infrequently. Hence, it is important to reduce the snapshot overhead when sensor node remains in the sleep state.

To address this issue, D2 adaptively takes snapshots. The checking procedure checks a total function counter (which counts the total number of function executions) at the current time as well as at the last snapshot. If it detects that the difference of the current total function counter and the total function counter at the last snapshot exceeds a threshold, e.g., 5000, it takes snapshots of the function counters by either transferring snapshots to the sink or saving snapshots to the external flash.

We note that the setting of this threshold has a tradeoff. On one hand, if the threshold is too large, the time granularity may not be fine-grained enough for detecting transient problems. On the other hand, if the threshold is too small, the snapshot overhead will be large. The threshold can also be dynamically reconfigured using a data dissemination protocol such as Drip [32] or DIP [33].

# 4.2 Problem detection

The D2 module on the PC is responsible for detecting the problems. D2 retrieves the snapshots by either wireless communications or serial connections.

Suppose there are N nodes in the network and each node has m time windows, D2 eventually gets N × m snapshots. Each snapshot is actually a function count vector f. There are n elements in the vector where n is the total number of functions in the program. Each element corresponds to a function and the value of the element is how many times this function is executed in the time window.

Figure 4 shows an illustrative example. There are two nodes and each node has three time windows (W1–W3). There are six function count vectors in this example. In time window W1 at node 1 (i.e., the first vector), the elements record the function execution counter during the time window. For example, the first vector shows that the functions, send(), receive(), sense(), and blink() execute 20, 30, 20, 30 times respectively in time window W1.

In our anomaly detection problem, we would like to detect which nodes exhibit abnormal behaviors at which time windows. More specifically, we would like to automatically detect anomalies among the given function count vectors. For the example shown in Figure 4, the second vector may be identified as an anomaly since the ratio of send() and receive() is much smaller than those in most other vectors.

A key assumption of our approach is that a problem makes a sensor node deviate from the normal, and thus outliers are good indicators of potential problems. During normal executions the relative frequency of two function counts in a time window usually stays the same. For example, the ratio between functions send() and receive() in the CTP component [5] is usually very stable during normal executions, but changes significantly when a problem occurs. The actual count does not matter (as it depends on workloads), but the ratio among different function counts matters.

We would like to “find needle from the haystack”, i.e., detect anomalies from all the diagnostic data. We adopt the Principal Component Analysis $( \mathrm { P C A } )$ approach. PCA is able to capture the essence of correlation in the data. Figure 4 illustrates an example using two dimensions in our data, i.e., function counts of send() and receive(). We see that most data resides in the straight line of $S _ { n } .$ The axis $S _ { n }$ captures the strong correlation between the two dimensions. Therefore, data points far from $S _ { n } , { \mathrm { e . g . } }$ , B and C, show unusual correlation, and thus are considered as anomalies. Point C represents that the number of send() is much smaller than the number of receive(), indicating that the node may experience an overflow in the receiving queue. Point B represents that the number of receive() is much smaller than the number of send(), indicating that the node may experience a high number of retransmissions. On the other hand, data point A, though far from other points, is close to $S _ { n } ,$ and thus is considered as normal. Point A represents cases in which both send() and receive() are executed frequently, indicating that the node has a large workload during that time window.

It is important to note that the problematic function can be easily identified for some simple cases. But problem detection becomes much more difficult for complex cases. For example, when the correlation of a pair of functions changes from high to low, or when additional system information (e.g., timing of I/O operations) are considered. PCA can not only work for simple cases but also for complex cases, making our approach easily extensible. It is also important to contrast PCA with one-class SVM for anomaly detection. For a similar set of data points, we apply one-class SVM and Figure 6 shows the detection results with the gray scales representing the distances to the hyperplane (the darker the color, the farther away from the hyperplane). We can see that PCA identifies B and C as anomalies while SVM identifies B, C, D, E as anomalies (if the threshold is set near the outmost boundary). In reality, data points D and E may represent normal conditions where the node experiences heavy workload for forwarding data packets. Therefore, we consider PCA as a more suitable choice in our case.

Like [28], we use the distance from a data point to the normal subspace $S _ { n }$ to determine whether f is an anomaly. The Squared Prediction Error $\mathbf { S P E } = | | \mathbf { f } _ { a } | | ^ { 2 }$ where $\mathbf { f } _ { a } = ( \mathbf { I } - \mathbf { P } \mathbf { P } ^ { T } ) \mathbf { f }$ is the projection of f onto the abnormal subspace $S _ { a } ,$ and $\mathbf { P } =$ $\left[ \mathbf { p } _ { 1 } , \mathbf { p } _ { 2 } , . . . , \mathbf { p } _ { k } \right]$ where $\mathbf { p } _ { 1 } , \mathbf { p } _ { 2 } , . . . , \mathbf { p } _ { k }$ are the principal components. We use a threshold of $Q _ { \alpha }$ to detect whether a data point is abnormal:

![](images/e25256c53341cc26a0e03f908197630b53c085b600bc17256d4a5f324b37c0b3.jpg)

Fig. 5: PCA anomaly detection. $S _ { n }$ indicates the normal subspace and $S _ { a }$ indicates the abnormal subspace. f represents the feature vector. $f _ { a }$ is the projection of f onto the abnormal subspace $S _ { a } .$ . SPE (Squared Prediction Error) is the squared length of $f _ { a }$ . Points B and C are identified as anomalies.   
![](images/27a1bdaa4b9df407bfecbed8ed33f7beb8d7e06536b924aa7798ea6aad6c542c.jpg)



Fig. 6: Anomaly detection using one-class SVM. The gray scales represent the distances to the hyperplane.

$$
\mathbf {S P E} = \left| \left| \mathbf {f} _ {a} \right| \right| ^ {2} > Q _ {\alpha} \tag {1}
$$

where $Q _ { \alpha }$ denotes the Q statistic (a well known test statistic for the SPE residual function [34]) at the 1 − α confidence level. The choice of the confidence parameter α for anomaly detection has been studied in previous work [35]. We choose $\alpha = 0 . 0 0 1$ as in previous work [28].

# 4.3 Problem diagnosis

Now we have detected abnormal function count vectors. We still lack detailed information why the anomaly occurs. For the example shown in Figure 4, the second vector may be detected as an anomaly. But we still do not know which specific functions contribute to this abnormal behavior. For a practical system with hundreds of functions, it is very useful to narrow down to the problematic functions.

Generally, given an anomaly and a set of normal profiles, we would like to examine each individual dimension and the ratios between two dimensions to see whether they are significantly different from the normal data. For example, we have detected that a node exhibits abnormal behaviors with its feature vector [11,100,22,38] in which each element corresponds to each function execution counter. We have also determined that the normal feature vector should be [10±2,60±50,20±3,30±4] where each element encodes both a mean value and a standard deviation. We would like to determine which function or a pair of functions are abnormal from the normal data. Considering that a program may contain hundreds of different functions in practice, it is useful to narrow down to the problematic functions for bug fixing. For this particular case, we can detect that the last function is abnormal since its execution counter far exceeds the normal data while the first three function counters are all within the normal range. D2 not only detects single abnormal function, but also abnormal function execution ratios. It performs such detections in a n2 matrix with each element corresponding to a ratio for a pair of functions.

We perform t-tests [36] to compare n function counts and n2 ratios between the detected anomaly and the normal data points. If the t-test rejects the null hypothesis, we conclude that the corresponding function count or ratio is able to distinguish the two classes. We use Welsh’s t-test and use a critical value of $p < 0 . 0 5$ to reject the null hypothesis and assess significance.

The magnitude of the t-statistic indicates the difference between the two classes. A larger t-statistic can be due to a larger difference in the means and/or smaller variance in the two classes. The sign of the t-statistic indicates which class has a bigger mean [37].

At this time, we can return a list of suspicious functions or ratios between two functions ranked by their statistical significance. The result can further be refined by considering the call/post relationship between functions. For example, we have ranked functions A, B, C at the top. Without their relationships, we need to manually check the correctness of all these functions. Clearly, a diagnosis report showing both statistical difference as well as the call/post relationships can greatly help further diagnosis.

We define elements in the diagnosis report as follows.

• A node represents a suspicious function or a suspicious ratio between two functions.   
• The size of the node indicates the statistical difference from the normal data.   
• There is a directed edge from node A to node B if functions in node A are predecessors of functions in node B in the call/post graph.   
• If some suspicious functions share common ancestors, we also show the nearest common ancestor and the corresponding call/post relationship to facilitate problem reasoning.

Figures 9–12 show examples of diagnosis reports. In the example diagnosis report shown in Fig. 12, we see that three function counts decrease rapidly at the problematic node. All these functions are related to the CTP sending logic. This localizes the bug to the corresponding component. The decrease of these function counters implies that the problematic node stops invoking sendMessage() due to some reasons in the radio stack. This gives programmers further guidance on how to diagnose the bug by inspecting the sending-related functions in the corresponding component.

We obtain the call/post graph of the program by parsing the ELF file on the PC. The call relationship is parsed by examining the call instructions and the corresponding target addresses in the code section. As mentioned earlier, call with pointers is a rare condition in TinyOS.

The post relationship is obtained by a more complicated way in the code section. The execution model of TinyOS consists of interrupts and tasks. Interrupts execute at a higher priority and can preempt the execution of tasks. Tasks execute at a lower priority and are scheduled in a FIFO manner. Interrupts are used to handle time sensitive operations which are usually very short. Tasks can be posted in the interrupts or other tasks to continue the processing a complex logical task. In TinyOS, the postTask function is used to post a task to the FIFO task queue. The runTask function is used to schedule the execution of queued tasks when the TinyOS task scheduler gains the CPU. We use the following procedure to obtain the post relationship. First, the task ID is found by inspecting calls to TinyOS postTask. Second, the functions corresponding to the actual task is found by inspecting the switch...case table in the runTask function with the task ID.

# 5 EXTENSION

We have described how D2 can detect and diagnosis anomalies exhibited in the function count vectors. In some circumstances, it is important to consider the timing information of program executions. For example, Distalyzer [37] extracts two features from a large amount of log data in distributed systems. The event feature summarizes the timing of system events while the state feature summarizes the values of a set of state variables.

A native approach to extend D2 is to additionally record the execution time of a function in the binary instrumentation process. However, we find that the execution time of a function in TinyOS is not informative enough. This is because I/O operations (e.g., send a packet, read a sensor data, write to the external flash, etc) are heavily used in event-driven systems like TinyOS, and, the I/O waiting time cannot captured in the function execution time since I/O operations in TinyOS are in split phase.

We extend D2’s binary instrumentation process to record the waiting time of the split-phase I/O operations, e.g., the time interval between send() and sendDone(), or, read() and readDone(). Therefore, the snapshots also include the average I/O waiting time of the split-phase I/O operations. Hence, we can additionally get I/O timing vector I which records I/O operation’s average waiting time. The PCA anomaly detection process detects anomalies based on both feature vectors f (function count) and I (I/O timing). By this approach, we can not only detect statistical anomalies exhibited in function counts but also anomalies exhibited in I/O waiting times.

Table 2: The number of principal components in the feature data. n is the dimension of the feature vector f and k is the number of principal components. 

<table><tr><td>Benchmarks</td><td>n</td><td>k</td></tr><tr><td>TestNetwork</td><td>257</td><td>10</td></tr><tr><td>Oscilloscope</td><td>212</td><td>14</td></tr><tr><td>TestDip</td><td>148</td><td>13</td></tr><tr><td>TestDissemination</td><td>135</td><td>9</td></tr><tr><td>Deluge-Blink</td><td>265</td><td>7</td></tr></table>

The above extension can potentially detect more system problems, especially those related to timing. However, it also introduces additional overhead to the runtime system. Therefore, we provide an option to turn on D2’s capability in detecting timing problems. In D2’s basic version, only function counts are collected. In D2’s extended version, additional I/O timing information is collected.

# 6 EVALUATION

In this section, we present an evaluation of D2. Section 6.1 introduces the evaluation setup as well as the benchmarks we use. Section 6.2 evaluates D2’s overhead on the TelosB nodes including RAM overhead, program flash overhead, external flash overhead, and the CPU slowdown. Section 6.3 describes case studies in real sensor network applications.

# 6.1 Benchmarks

In order to evaluate the overhead of D2 on real sensor nodes, we investigate five typical benchmarks on TelosB nodes with 8MHz MSP430f1611 processor, 128KB program size, 10KB memory size, 1MB external flash size, and 250Kbps CC2420 radio.

All five benchmarks are in the TinyOS 2.1.1 distribution.

• TestNetwork: TestNetworkC uses the basic networking layers, CTP (collection) and Drip (dissemination).   
• Oscilloscope: Oscilloscope is a simple data collection demo. It periodically samples the default sensor and broadcasts a message over the radio every 10 readings.   
• TestDip: TestNetworkC exercises the basic dissemination protocol DIP.   
• TestDissemination: TestDissemination exercises the basic dissemination protocol Drip.   
• Deluge-Blink: Deluge-Blink is the simple Blink application with the Deluge reprogramming support.

Table 2 shows the number of principal components for the five benchmarks We see a small number of dimensions can essentially capture large variance in the original data, indicating that the dimensions are highly correlated.

# 6.2 Overhead

This section evaluates the overhead of D2’s basic version on the TelosB nodes, including RAM overhead, program flash overhead, external flash overhead, and CPU slowdown.

Table 3: RAM overhead (bytes) 

<table><tr><td>Benchmarks</td><td># of func</td><td>Overhead</td></tr><tr><td>TestNetwork</td><td>257</td><td>1032</td></tr><tr><td>Oscilloscope</td><td>212</td><td>852</td></tr><tr><td>TestDip</td><td>148</td><td>596</td></tr><tr><td>TestDissemination</td><td>135</td><td>544</td></tr><tr><td>Deluge-Blink</td><td>265</td><td>1064</td></tr></table>

![](images/b2d399f3f2ffe4ddbf7bf12f08ab1fc8809f62904dbb77ac9e8a6a485d002250.jpg)



Fig. 7: RAM consumption of TinyOS applications.

# 6.2.1 RAM

D2 requires a set of function counters to be allocated on RAM to track the number of each function’s executions. The RAM overhead is proportional to the number of functions to be tracked. We currently use 4 bytes for each counter. Besides, we need 4 additional bytes to track the total count of all function executions.

Table 3 shows the RAM overhead for five benchmark applications based on TinyOS 2.1.1. We can see that the RAM overhead varies from 544 bytes to 1064 bytes.

To see whether this RAM overhead is acceptable, we measure the RAM consumptions of the five benchmarks in Figure 7 (the statistics for GreenOrbs are similar to the TestNetwork application). The TinyOS applications consume 391–4386 bytes while the stacks1 consume 464–674 bytes. Since TinyOS employs static memory allocation (i.e., the remaining memory space will not be used by the OS and the applications), D2’s memory consumptions can well fit into the remaining memory space.

# 6.2.2 Program flash

D2 increases program flash size in two ways. First, the D2 module which performs binary instrumentation takes about 6.8kB program memory. Second, after instrumentation, the original program increases because of the trampoline overhead for each function.

The first overhead is a constant for all benchmarks. For all the benchmarks investigated in this paper, we can fit the D2 module on the program flash. When the original application code size is large, we can perform further optimizations by dynamic loading, i.e., storing the D2 module on the external flash and loading onto the program memory by another smaller bootloader when needed. After D2 performs binary instrumentation, the node switches to the instrumented application code. In this way, the memory overhead of D2 module has no impact on the application.

![](images/cb8e110ca546fdb0da01cf628f8ceaf1bdde50b5b46dd030a847cccf78da9eaa.jpg)



Fig. 8: Program flash overhead

Table 4: Increase of program size when function inlining is prohibited 

<table><tr><td>Benchmarks</td><td>Default</td><td>non-inlining</td><td>inc. rate</td></tr><tr><td>TestNetwork</td><td>33.102</td><td>35.576</td><td>7.47%</td></tr><tr><td>Oscilloscope</td><td>17.450</td><td>18.860</td><td>8.08%</td></tr><tr><td>TestDip</td><td>17.154</td><td>18.582</td><td>8.32%</td></tr><tr><td>TestDissemination</td><td>14.826</td><td>16.278</td><td>9.79%</td></tr><tr><td>Deluge-Blink</td><td>32.866</td><td>35.208</td><td>7.13%</td></tr></table>

The second overhead depends on the complexity of each benchmark. Figure 8 shows the original program size, the constant overhead of D2, and the trampoline overhead for five benchmarks. The trampoline overhead after instrumentation depends on the number of functions in the compiled code.

Function inlining is a common technique for optimizing program performance. However, it can hinder localizing to the correct function in D2. To strike a reasonable balance, we would require large functions non-inlined so that bugs can be traced to the corresponding function. Table 3 shows the increase of program size when we prohibit inlining of functions exceeding 200 bytes. We can see that the increase is below 10% compared with the default case with aggressive function inlining.

# 6.2.3 External flash

Usually, D2 needs to store snapshots of function counts onto the external flash for later analysis. The snapshots can also be directly sent to the sink node for real-time analysis. The snapshot overhead depends on how frequently D2 takes snapshots.

Tables 5 show the snapshot overhead for five benchmark applications for 30 minutes when the threshold φ (for the total function counter) is set at 5000. We also compare the overhead of D2’s counter-based profiling with LIS’s eventbased profiling [20], [21]. We can see that D2 results in 39– 220 reduction.

Finally, it is important to examine the energy overhead on the external flash. According to our previous study,

• the current when reading from external flash is $I _ { \mathrm { r e a d } } =$ 5mA,

Table 5: External flash overhead for 30 minutes (bytes) with φ=5000. 

<table><tr><td>Benchmarks</td><td> $\phi=5000$ </td><td> $\frac{LIS}{D2}$ </td></tr><tr><td>TestNetwork</td><td>15934</td><td>220.5</td></tr><tr><td>Oscilloscope</td><td>68688</td><td>56.55</td></tr><tr><td>TestDip</td><td>19536</td><td>81.15</td></tr><tr><td>TestDissemination</td><td>13230</td><td>77.7</td></tr><tr><td>Deluge-Blink</td><td>14310</td><td>39.6</td></tr></table>

Table 6: Additional energy consumption due to storing snapshots on external flash (mAs) 

<table><tr><td>Benchmarks</td><td>Without D2</td><td>Additional cost</td><td>inc. rate</td></tr><tr><td>TestNetwork</td><td>981.00</td><td>15.74</td><td>1.60%</td></tr><tr><td>Oscilloscope</td><td>2185.67</td><td>67.86</td><td>3.10%</td></tr><tr><td>TestDip</td><td>1118.34</td><td>19.3</td><td>1.73%</td></tr><tr><td>TestDissemination</td><td>627.84</td><td>13.07</td><td>2.08%</td></tr><tr><td>Deluge-Blink</td><td>965.30</td><td>14.13</td><td>1.46%</td></tr></table>

Table 7: Comparison of CPU utilizations 

<table><tr><td>Benchmarks</td><td>Without D2</td><td>With D2(ai)</td><td>With D2(pi)</td></tr><tr><td>TestNetwork</td><td>2.16%</td><td>2.50%</td><td>2.78%</td></tr><tr><td>Oscilloscope</td><td>4.82%</td><td>5.57%</td><td>6.21%</td></tr><tr><td>TestDip</td><td>2.47%</td><td>2.85%</td><td>3.18%</td></tr><tr><td>TestDissemination</td><td>1.40%</td><td>1.60%</td><td>1.79%</td></tr><tr><td>Deluge-Blink</td><td>2.13%</td><td>2.46%</td><td>2.73 %</td></tr></table>

• the current when writing to external flash is $I _ { \mathrm { w r i t e } } = 1 2 \mathrm { m A }$ .   
• the time for reading one byte from the external flash is $T _ { \mathrm { r e a d } } = 0 . 0 4 5 \mathrm { m s } .$ .   
• the time for writing one byte to the external flash is $T _ { \mathrm { w r i t e } }$ $= 0 . 0 5 9 \mathrm { m s } .$

Considering the per-byte energy consumption of logging on the external flash as well as reading from the flash for later collection, we can get: $W _ { \mathrm { b y t e } } = I _ { \mathrm { r e a d } } T _ { \mathrm { r e a d } } + I _ { \mathrm { w r i t e } } T _ { \mathrm { w r i t e } }$ . Table 6 shows the energy consumption for the five benchmarks lasting for 30 minutes (with $\phi = 5 0 0 0 )$ . We also show the relative increase compared with the original application. We can see that the relative increase is small.

# 6.2.4 CPU utilization

D2 slightly degrades program’s execution because of the overhead in the trampolines. Table 7 compares the CPU utilizations of the original program (without D2) and the instrumented program (with D2). We further differentiate two cases: 1) D2(ai), D2’s default case with aggressive inlining, and 2) D2(pi), prohibiting the inlining of functions exceeding 200 bytes. We can see that the increase of CPU utilization is small. This will not affect the network performance as most sensor network applications are not CPU-intensive.

Nevertheless, D2 may still introduce Heisenbugs due to binary instrumentation. We try to minimize the impact by minimizing D2’s run-time overhead. The degradation can be eliminated if additional hardware is employed. For example, if the AVEKSHA hardware [12] is employed, the extra CPU attaching to the JTAG will be interrupted at the start of each function and thus can execute the trampoline in parallel to the main CPU, eliminating the execution overhead of trampolines.

# 6.2.5 Comparison with other approaches

![](images/16f61cd54e071f202f166d96d477c46d1608f6d8ecfe2219fe8a64cbae811eac.jpg)



Fig. 9: Diagnosis report for case 1. The size of a node represents the statistical significance. The upward arrow inside the node indicates a statistical increase. The arrow connecting two nodes represents a call/post relationship.

Table 8: Comparison of D2 and LIS [20]. 

<table><tr><td>Tools</td><td>CPU inc.</td><td>RAM (bytes)</td><td>trace size (kB)</td></tr><tr><td>D2</td><td>15%</td><td>852</td><td>68</td></tr><tr><td>LIS [20]</td><td>21%</td><td>450</td><td>3842</td></tr></table>

We compare the overhead of D2 with LIS [20]—an eventbased profiling method using the Oscilloscope benchmark. Table 8 shows the results. (1) CPU utilization. D2 increases the CPU utilization by 15% compared with the uninstrumented program. According to [11], LIS increases by CPU utilization by 21%. (2) RAM overhead. D2 consumes more memory than LIS due to its allocation of function counters. Note that we can further optimize D2’s memory consumption by allocating 2 bytes (instead of 4 bytes) for each function counter, as long as the function counter does not overflow during the maximum possible time window. (3) Size of diagnostic data (external flash overhead). D2 consumes significantly less overhead than LIS: LIS’s trace size is 56 times larger than the snapshot overhead of D2.

# 6.3 Case studies

Our goal in these studies is to demonstrate that D2 can be applied in existing sensor network applications and can simplify the complex process of detecting and diagnosing sensor network problems.

# 6.3.1 Case 1: flash broken

Application scenario. We test our GreenOrbs application program in an indoor testbed consisting of 50 TelosB nodes for 30 minutes. The GreenOrbs application basically reads the sensor data and delivers the data to the sink with a period of 1 minute. Each packet transmission and reception events are recorded on the external flash for later analysis.

Symptom. We find a symptom that two nodes did not record any events in their external flash until we finish the experiment and attempt to retrieve the recorded events.

D2 setup and findings. In the next experiment, we turned on the D2 functionality for this application. The D2 profiles are collected through serial ports. We use 10 snapshots from each node to apply D2’s analysis approach.

D2 indeed detects that two nodes exhibit abnormal patterns. D2 can not only detect the problem in the network but also simplify the process of further diagnosis. Figure 9 depicts the diagnosis report generated by D2. We can see that four functions are frequently executed in abnormal nodes. Function runTask() invokes releaseAndRequest() which again invokes release() and request().

From the prefixes of these functions, we can easily guess that the STM25P component might be in error: the STM25P component repeatedly makes requests to acquire the SPI resource. Considering that these two nodes did not record any events in the external flash, we highly suspect that their external flash is broken and the buggy code does not take this condition into account.

Looking into the two files related to STM25P (i.e., Stm25pSpiP.nc and Stm25pSectorP.nc), we confirm our guess by finding that the powerUp() function would always return SUCCESS regardless of the status of the hardware (i.e., signature). The STM25P datasheet [38] indicates that the powering up succeeds only when the signature equals to 0x13.

Code fix. We fix the bug by checking the signature in the powerUp() function. If it does not succeed, we simply prevent the code from repeatedly acquiring the SPI resource.

Discussion. We note that this is a new bug which has not been previously reported as far as we know. We hope the bug will be fixed in the next release of TinyOS.

It is true that programmers can be alerted by examining the return value of write/read. However, this particular programmer had ignored the return value of a critical function in this case. D2 can detect the problem and narrow down the problem with a relatively small overhead in an automatic manner.

# 6.3.2 Case 2: TYMO routing protocol

Application scenario. We use 50 TelosB nodes in an indoor testbed. The application uses the TYMO routing protocol. TYMO is a TinyOS-based implementation of the DYMO routing protocol [39]—a successor of the AODV routing protocol [40]. In [23], authors reported a bug in the recent TYMO routing protocol in the TinyOS distribution. We apply D2 to a similar case to see whether D2 can also localize the bug. Sink node (node 50) is used to collect data. All other nodes (nodes 0, ... 48) are reporting packets to the sink via one hop wireless. The experiment lasts for 30 minutes.

Symptom. The sink node misses all packets from node 0.

D2 setup and findings. We turned on the D2 functionality and collected all the profiles for later analysis.

D2 generates the diagnosis report as shown in Figure 10. We can see that at node 0 the function getPayload() is called frequently while function getRoute() is called infrequently (compared with the normal behavior). Both functions are called in the selectRoute() function.

We look into the source code and find that the execution flow at node 0 diverges from the normal execution flow in which a node tries to get a forwarding route and transmit the packet. Node 0 simply finds that the packet is for itself (the function isForMe(msg) returns true), causing the abnormal function executions in Fig. 10.

![](images/bb6431d6e17c9ac7f258e2a7fc8400b64b331cd64a0e7c2fe6ba758d0c86d55b.jpg)



Fig. 10: Diagnosis report for case 2. The size of a node represents the statistical significance. The upward arrow inside the node indicates a statistical increase. The arrow connecting two nodes represents a call/post relationship. The function selectRoute function (top) does not exhibits statistical difference in this case.

After more careful code reviews, we find that the real root cause is that the destination field is set too late: the destination field of msg is not set before calling selectRoute(). The function selectRoute() invokes isForMe() before msg is properly initialized. If the current node is 0, the function isForMe() will return true as the uninitialized fields in msg happen to be 0. So node 0 will not transmit any data. We can see that D2 can also localize the bug for this case.

Code fix. We fix the code by setting the destination field before calling selectRoute().

# 6.3.3 Case 3: CTP queue overflow

Application scenario. We deploy 50 TelosB nodes in the woodland of Zhejiang Forestry University. The nodes run the actual GreenOrbs application for one week.

Symptom. We have indeed detected a number of problems. In particular, nodes near the sink are more likely to experience heavier packet losses.

D2 setup and findings. We turned on the D2 functionality and collected all the profiles for later analysis. After distinguishing the anomaly points, we apply D2’s diagnosis method.

Figure 11 depicts the diagnosis report generated by D2. In this case, D2 finds that each individual function count does not exhibit much statistical difference. However, some ratios between functions exhibit large statistical difference. For example, the ratio between receive() and send() decreases in a few snapshots. D2 will automatically detect anomalies in function ratios when it finds each individual function count is normal.

This finding clearly indicates that the corresponding node during that time window experiences transient overflow so that the number of receive() and send() diverges. Looking into the code, we indeed find that the default CTP implementation does not turn on the congestion control mechanism.

![](images/80350ca8ba43b23ec91a498388936bfb265b034bfc3067c2663275c0f62768fd.jpg)



Fig. 11: Diagnosis report for case 3. The size of a node represents the statistical significance of the ratio. The downward arrow indicates a statistical decrease. A solid arrow connecting two nodes indicates that there is a call/post relationship between the functions in the numerator while a blank arrow connecting two nodes indicates that there is a call/post relationship between functions in the denominator.

Code fix. We implement a simple congestion control mechanism as follows. First, we set the ECN bit to notify neighbors when the current queue size exceeds the maximum allowable size. Second, after receiving packets with the ECN bit turned on, the current node will avoid selecting the congested node. More advanced congestion control mechanisms can be adopted. However, we find that this simple mechanism addresses this problem fairly well in practice.

Discussion. The PCA approach used by D2 can automatically find correlations among multiple dimensions. D2 can detect anomalies violating the correlations. For problem diagnosis, D2 will first check the function counts to pinpoint abnormal functions. If the function counts are normal, it will proceed to check the ratios of function counts to pinpoint which ratios are abnormal.

This case study gives us the following implications. First, some problems can be caused by the joint effects of code imperfections as well as the topology and traffic in real systems. Hence, a method that can be applied in a realworld deployed system is important to capture such problems. Second, sensor network exhibits variable workload. Simple analysis on each individual dimension may not be able to reveal some problems. We find PCA is suitable because it can capture the essence of the correlations between multiple dimensions.

# 6.3.4 Case 4: FTSP+CTP in TinyOS 2.1.0

Application scenario. We use 24 TelosB nodes in our indoor testbed for one hour. The application uses the CTP protocol to collect sensor data at a rate of 5 minutes. It also uses the FTSP protocol for global time synchronization.

Symptom. After 10 minutes, several nodes stop delivering data to the sink node.

![](images/baa14ca5d12ac84844353c5708cf845d1a36f09fb833e7c5e84273f7917b3ab2.jpg)



Fig. 12: Diagnosis report for case 4.

D2 setup and findings. We repeat the experiments, and turn on the D2 functionality and collect all the profiles for later analysis. D2 generates the diagnosis report as shown in Figure 12. We can see that at node 6 three function counts decrease rapidly. All these functions are related to the CTP sending logic. This implies that node 6 stops invoking sendMessage() due to some reasons in the radio stack.

We look into the source code and find that the most likely reason is due to the busy flag sendBusy in the CTP components. Normally, sendBusy will be reset to FALSE in the sendDone() event. However, when CTP works together with FTSP, it is possible that the invocation to the MAClayer send fails after sendBusy is set to TRUE. This, in turn, causes the sendDone() event never happen. Hence the CTP protocol hangs. It is correct when CTP is the sole protocol in the application because the invocation to the MAC-layer send always succeeds. However, multiple protocols with different purposes may co-exist in a sensor to fulfil different tasks. Hence, uncoordinated resource contention among different protocols may be transiently triggered and the system eventually fails [22]. This bug has been extensively discussed in the TinyOS mailing list.

Code fix. We fix the code by examining the return value of MAC-layer send(), and post the send() task in a retransmission timer until it succeeds.

# 6.3.5 Case 5: CTP in high-data-rate applications

Application scenario. We use 50 TelosB nodes in our indoor testbed for one hour. The application uses the CTP protocol to collect sensor data. We change the data transmission period from 10s to 1s.

Symptom. We find that at data transmission period of 10s, the sink can collect the sensor data. However, the sink receives no data when the transmission period is changed to 1s.

D2 setup and findings. We repeat the experiment, and turn on the D2 functionality. In particular, we use D2’s extended version to also collect the timing information of TinyOS split-phase I/Os. We suspect that there are problems in the radio transmission components. From Figure 13, we find that the I/O waiting times of two operations significantly deviate from the normal. One is the send() to sendDone() time interval in the CtpForwardingEngine component. The other is the ACK waiting time which is the time interval from the packet is actually transmitted (an SFD interrupt will be generated) to the corresponding ACK is received (another SDF interrupt corresponding to the ACK will be generated). Figure 13 shows that the I/O waiting times of these two I/O operations with varying transmission periods. We can see that at 10s transmission period, the two I/O waiting times are kept small. However, both I/O waiting times significantly increase when the transmission period decreases (i.e., at a higher data rate). The large increase of ACK time (from 3ms to 20ms) clearly suggests an unexpected scenario from the perspective of developers: the TinyOS link layer will retransmit the packet after an ACK timeout of 1/128 ≈ 7.8ms. If the ACK is returned at a later time, the link layer will repeatedly retransmit the packet, making the CTP protocol to hang eventually. The increase of ACK time is due to the fact that TinyOS uses software ACK by default [41]. Software ACKs can be interrupted and delayed by other radio activities.

![](images/7a83f8cd9da389b7e494e5a94962177f958444be274ef6126547ac353e89f0c0.jpg)



Fig. 13: I/O waiting time (ms) of two I/O operations with varying transmission periods.

Code fix. We fix the problem by turning on the CC2420 HW ACKNOWLEDGEMENTS flag to inform TinyOS to use the hardware ACKs instead of software ACKs.

# 6.3.6 Comparative study

We also perform a comparative study on both one-class SVM (used by Sentomist) and PCA (used by D2) for the four case studies described earlier (Section 6.3.1–6.3.4). We use two metrics for comparison: the overhead and the effectiveness. The overhead of SVM and PCA is the time taken by these approaches to detect an anomaly. The detection algorithm is run on a PC with a dual-core 2.3GHz CPU and 4GB RAM. Table 9 compares the execution times of SVM and PCA on the PCs. We can see that PCA runs slightly faster than SVM.

The end-to-end metric for evaluating the effectiveness of a diagnosis approach is the amount of developer time required to diagnose each bug. However, this metric highly depends on the expertise of the developer as well as his familiarity to different code components. We choose detection accuracy as an effectiveness metric since problem diagnosis will be more efficient if the anomalies are more accurately detected in the first place.

We manually inject bugs so that we can compare our result with the ground truth. In each case study, we perform oneclass SVM and PCA on 250 data points with 10 known anomalies produced by the buggy program code. Table 10 shows detection accuracy which is defined as the ratio of the number of real anomalies among the 10 top ranked anomalies produced by two approaches. We also show the false positive ratio (FP) and false negative ratio (FN). We can see that PCA has a better accuracy than one-class SVM, especially for the third case.

Table 9: Execution time (ms) of SVM and PCA. 

<table><tr><td>Cases</td><td>SVM</td><td>PCA</td></tr><tr><td>Flash broken</td><td>19.20</td><td>12.42</td></tr><tr><td>TYMO</td><td>19.92</td><td>17.66</td></tr><tr><td>CTP-overflow</td><td>23.01</td><td>20.78</td></tr><tr><td>CTP+FTSP</td><td>26.91</td><td>21.83</td></tr></table>

Table 10: Detection accuracy of SVM and PCA. 

<table><tr><td>Cases</td><td>SVM (FP/FN)</td><td>PCA (FP/FN)</td></tr><tr><td>Flash broken</td><td>100% (0%/0%)</td><td>100% (0%/0%)</td></tr><tr><td>TYMO</td><td>90% (10%/10%)</td><td>100% (0%/0%)</td></tr><tr><td>CTP-overflow</td><td>50% (50%/50%)</td><td>90% (10%/10%)</td></tr><tr><td>CTP+FTSP</td><td>90% (10%/10%)</td><td>90% (10%/10%)</td></tr></table>

We believe that the injected bugs in the case studies are representative since the injected bugs are the ones we have actually encountered during the development of GreenOrbs, a real-world sensor network system. It is worth noting that D2 can also detect non-reproducible anomalies as long as the program profile about the anomaly has been collected. Whether D2 can detect the anomaly depends on whether D2 has collected the program profile about the anomaly, instead of whether the anomaly is reproducible or non-reproducible.

# 7 CONCLUSION

In this paper, we propose a method towards automated postdeployment diagnosis in networked embedded systems by combining program profiling and symptom mining. As opposed to previous instrumentation methods which either incur a large overhead or demand special hardware, we employ binary instrumentation to perform lightweight function count profiling. The statistics at the function level provide us finegrained information for detailed reasoning. Unlike previous methods which require application programmers’ efforts for providing specific network metrics, our method treats the program as a black box, thus is scalable for a wide range of applications. Based on the statistics, we employ PCAbased approach for automatically detecting network problems. Previous network-level diagnosis methods only detect network problems at the node level or link level, D2 is able to point programmers closer to the most likely causes by a novel approach combining statistical tests and program call graph analysis.

We implement our method based on TinyOS 2.1.1 and evaluate its effectiveness by case studies in the development of GreenOrbs. Results show that our method can aid programmers to diagnose problems quickly in real-world sensor network systems, and at the same time, incurs an acceptable overhead to the running system.

# ACKNOWLEDGEMENT

This work is supported by the National Science Foundation of China Grants No. 61472360.

# REFERENCES

[1] K. Langendoen, A. Baggio, and O. Visser, “Murphy Loves Potatoes: Experiences from a Pilot Sensor Network Deployment in Precision Agriculture,” in Proc. of the International Workshop on Parallel and Distributed Real-Time Systems (WPDRTS), 2006.   
[2] A. Woo, T. Tong, and D. Culler, “Taming the Underlying Challenges of Reliable Multihop Routing in Sensor Networks,” in Proc. of ACM SenSys, 2003.   
[3] J. W. Hui and D. Culler, “The dynamic behavior of a data dissemination protocol for network programming at scale,” in Proc. of ACM SenSys, 2004.   
[4] Y. Liu, Y. He, M. Li, J. Wang, K. Liu, L. Mo, W. Dong, Z. Yang, M. Xi, and J. Zhao, “Does Wireless Sensor Network Scale? A Measurement Study on GreenOrbs,” in Proc. of IEEE INFOCOM, 2011.   
[5] O. Gnawali, R. Fonseca, K. Jamieson, D. Moss, and P. Levis, “Collection Tree Protocol,” in Proc. of ACM SenSys, 2009.   
[6] M. Maroti, B. Kusy, G. Simon, and ´ A. L ´ edeczi, “The Flooding Time ´ Synchronization Protocol,” in Proc. of ACM SenSys, 2004.   
[7] P. Li and J. Regehr, “T-Check: Bug Finding for Sensor Networks,” in Proc. of ACM/IEEE IPSN, 2010.   
[8] R. Sasnauskas, O. Landsiedel, M. H. Alizai, C. Weise, S. Kowalewski, and K. Wehrle, “KleeNet: Discovering Insidious Interaction Bugs in Wireless Sensor Networks Before Deployment,” in Proc. of ACM/IEEE IPSN, 2010.   
[9] J. Yang, M. L. Soffa, L. Selava, and K. Whitehouse, “Clairvoyant: A comprehensive source-level debugger for wireless sensor networks,” in Proc. of ACM SenSys, 2007.   
[10] Q. Cao, T. Abdelzaher, J. Stankovic, and L. Luo, “Declarative Tracepoints: A Programmable and Application Independent Debugging System for Wireless Sensor Networks,” in Proc. of ACM SenSys, 2008.   
[11] V. SUNDARAM, P. EUGSTER, X. ZHANG, and V. ADDANKI, “Diagnostic Tracing for Wireless Sensor Networks,” ACM Transactions on Sensor Networks, vol. 9, no. 4, pp. 38:1–38:41, 2013.   
[12] M. Tancreti, M. Hossain, S. Bagchi, and V. Raghunathan, “Aveksha: A Hardware-Software Approach for Non-intrusive Tracing and Profiling of Wireless Embedded Systems,” in Proc. of ACM SenSys, 2011.   
[13] R. Sauter, O. Saukh, O. Frietsch, and P. J. Marron, “TinyLTS: Efficient ´ Network-Wide Logging and Tracing System for TinyOS,” in Proc. of IEEE INFOCOM, 2011.   
[14] N. Ramanathan, K. Chang, L. Girod, R. Kapur, E. Kohler, and D. Estrin, “Sympathy for the sensor network debugger,” in Proc. of ACM SenSys, 2005.   
[15] Y. Liu, K. Liu, and M. Li, “Passive Diagnosis for Wireless Sensor Networks,” IEEE/ACM Transactions on Networking, vol. 18, no. 4, pp. 1132–1144, 2010.   
[16] K. Liu, Q. Ma, X. Zhao, and Y. Liu, “Self-Diagnosis for Large Scale Wireless Sensor Networks,” in Proc. of IEEE INFOCOM, 2011.   
[17] X. Miao, K. Liu, Y. He, Y. Liu, and D. Papadias, “Agnostic Diagnosis: Discovering Silent Failures in Wireless Sensor Networks,” in Proc. of IEEE INFOCOM, 2011.   
[18] Q. Ma, K. Liu, X. Miao, and Y. Liu, “Sherlock is Around: Detecting Network Failures with Local Evidence Fusion,” in Proc. of IEEE INFOCOM, 2012.   
[19] J. Ha, C. J. Rossbach, J. V. David, I. Roy, H. E. Ramadan, D. E. Porter, D. L. Chen, and E. Witchel, “Improved Error Reporting for Software that Uses Black-Box Components,” in Proc. of ACM PLDI, 2007.   
[20] Y. C. R. Shea and M. B. Srivastava, “LIS is More: Improved Diagnostic Logging in Sensor Networks with Log Instrumentation Specifications ((TR-UCLA-NESL-200906-01)),” UCLA, Tech. Rep., 2009.   
[21] R. Shea, M. B. Srivastava, and Y. Cho, “Scoped identifiers for efficient bit aligned logging,” in Design, Automation, and Test in Europe, 2010, pp. 1450–1455.   
[22] Y. Zhou, X. Chen, M. R. Lyu, and J. Liu, “Sentomist: Unveiling Transient Sensor Network Bugs via Symptom Mining,” in Proc. of IEEE ICDCS, 2010.   
[23] ——, “T-Morph: Revealing Buggy Behaviors of TinyOS Applications via Rule Mining and Visualization,” in Proc. of SIGSOFT 2012/FSE 20, 2012.

[24] M. Khan, H. K. Le, H. Ahmadi, and T. Abdelzaher, “DustMiner: Troubleshooting Interactive Complexity Bugs in Sensor Networks,” in Proc. of ACM SenSys, 2008.   
[25] B. L. Titzer and et al., “Avrora: Scalable Sensor Network Simulation With Precise Timing,” in Proc. of ACM/IEEE IPSN, 2005.   
[26] V. Krunic, E. Trumpler, and R. Han, “NodeMD: Diagnosing node-level faults in remote wireless sensor,” in Proc. of ACM MobiSys, 2007.   
[27] L. Luo, T. He, G. Zhou, L. Gu, T. F. Abdelzaher, and J. A. Stankovic, “Achieving repeatability of asynchronous events in wireless sensor networks with EnviroLog,” in Proc. of IEEE INFOCOM, 2006.   
[28] W. Xu, L. Huang, A. Fox, D. Patterson, and M. I. Jordan, “Detecting Large-Scale System Problems by Mining Console Logs,” in Proc. of ACM SOSP, 2009.   
[29] J. M. Link, “Trampolines for embedded systems: Minimizing interrupt handlers latency,” in [Online]. Available: http://www.drdobbs.com/embedded-systems/trampolines-forembeddedsystems/184404772.   
[30] M. Ekman and H. Thane, “Dynamic Patching of Embedded Software,” in Proc. of IEEE RTAS, 2007.   
[31] T. Committee, “Tool interface standard (TIS) executable and linking format (ELF) specification,” 1995.   
[32] G. Tolle and D. Culler, “Design of an Application-Cooperative Management System for Wireless Sensor Networks,” in Proc. of EWSN, 2005.   
[33] K. Lin and P. Levis, “Data Discovery and Dissemination with DIP,” in Proceedings of ACM/IEEE IPSN, 2008.   
[34] J. E. Jsackson and G. S. Mudholkar, “Control procedures for residuals associated with principal component analysis,” Technometrics, vol. 21, no. 3, pp. 341–349, 1979.   
[35] A. Lakhina, M. Crovella, and C. Diot, “Diagnosing network-wide traffic anomalies,” in Proc. of ACM SIGCOMM, 2004.   
[36] W. T. V. S. A. Teukolsky and B. P. Flannery, “Numerical Recipes in C: The Art of Scientific Computing,” in Cambridge University Press, 1992.   
[37] K. Nagaraj, C. Killian, and J. Neville, “Structured Comparative Analysis of System Logs to Diagnose Performance Problems,” in Proc. of USENIX NSDI, 2012.   
[38] M25P80 datasheet, STMicroelectronics, 2004.   
[39] R. Thouvenin, “Implementing and evaluating the dynamic manet ondemand protocol in wireless sensor networks,” in Master Thesis, University of Aarhus, 2007.   
[40] C. Perkins, E. Belding-Royer, and S. Das, “Ad-hoc On-Demand Distance Vector Routing,” in Proc. of IEEE workshop on mobile computing systems and applications, 1993.   
[41] P. Levis, D. Gay, V. Handziski, J.-H. Hauer, B. Greenstein, M. Turon, J. Hui, K. Klues, C. Sharp, R. Szewczyk, J. Polastre, P. Buonadonna, L. Nachman, G. Tolle, D. Culler, , and A. Wolisz, “T2: A Second Generation OS for Embedded Sensor Networks,” Technical Univ. Berlin, Tech. Rep., 2005.

![](images/9e479adb9a620f2297020e58c43681d23366f076351ea8f001acdad4a34a3aa8.jpg)



Luyao Luo received his B.Eng. degree from Central South University in 2015. He is currently a graduate student in Zhejiang University, China. His research interests include networked embedded systems and system diagnosis.

![](images/cdb855ada1ab552c02a4c3c4dbb5c04773d73cab28b7f746a6b726393411f492.jpg)



Chun Chen received his Bachelor of Mathematics degree from Xiamen University, China, in 1981, and his M.S. and Ph.D. degrees in Computer Science from Zhejiang University, China, in 1984 and 1990 respectively. He is a professor in College of Computer Science, and the Director of Institute of Computer Software at Zhejiang University. His research interests include embedded system, image processing, computer vision, and CAD/CAM.

![](images/f9f023eb7cb3ff580d0458b3bf5d2be376e968453387e4bc849910ae88adf9d3.jpg)



Jiajun Bu received the B.S. and Ph.D. degrees in Computer Science from Zhejiang University, China, in 1995 and 2000, respectively. He is a professor in College of Computer Science and the deputy dean of School of Software Technology at Zhejiang University. His research interests include embedded system, mobile multimedia, and data mining. He is a member of the IEEE and the ACM.

![](images/80062e88918f75bb74345cfc151bf91c3ed4a7c59f65f4cda79f1071944448ab.jpg)



and software reliability.

Xue Liu is an Associate Professor and William Dawson Scholar in the School of Computer Science, McGill University, Montreal, QC, Canada. He received his Ph.D. in Computer Science from the University of Illinois at Urbana-Champaign in 2006. He received his B.S. degree in Mathematics and M.S. degree in Automatic Control both from Tsinghua University, China. His research interests are in computer networks and communications, smart grid, realtime and embedded systems, cyber-physical systems, data centers,

![](images/cd7dab18e38df37d53853092c9cba91f4faa19de8bc3482a09d52a114b1e2dd3.jpg)



Wei Dong received his BS and Ph.D. degrees from the College of Computer Science at Zhejiang University in 2005 and 2011, respectively. He is currently an associate professor in the College of Computer Science in Zhejiang University. His research interests include sensor networks, wireless and mobile computing, and network measurement. He is a member of the IEEE.

![](images/72a4e216fef9a55eba0710cddca9f7b74843390fef23f981ba4aa738ab6a53ae.jpg)



Yunhao Liu received the B.S. degree in automation from Tsinghua University, Beijing, China, in 1995, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing,MI, USA, in 2003 and 2004, respectively. He is a Professor, Dean of the School of Software, and a member of the Tsinghua National Lab for Information Science and Technology, Tsinghua University. Prof. Liu is serving as the Chair of ACM China Council.