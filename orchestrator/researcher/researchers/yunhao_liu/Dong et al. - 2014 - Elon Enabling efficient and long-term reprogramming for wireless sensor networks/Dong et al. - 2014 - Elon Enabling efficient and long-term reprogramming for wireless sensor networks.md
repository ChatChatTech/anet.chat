# Elon: Enabling Efficient and Long-Term Reprogramming for Wireless Sensor Networks

WEI DONG, Zhejiang University

YUNHAO LIU, Tsinghua University

CHUN CHEN, Zhejiang University

LIN GU, Hong Kong University of Science and Technology

XIAOFAN WU, Zhejiang University

We present a new mechanism called Elon for enabling efficient and long-term reprogramming in wireless sensor networks. Elon reduces the transferred code size significantly by introducing the concept of replaceable component. It avoids the cost of hardware reboot with a novel software reboot mechanism. Moreover, it significantly prolongs the reprogrammable lifetime (i.e., the time period during which the sensor nodes can be reprogrammed) by avoiding flash writes for TelosB nodes. Experimental results show that Elon transfers up to 120–389 times less information than Deluge, and 18–42 times less information than Stream. The software reboot mechanism that Elon applies reduces the rebooting cost by 50.4%–53.87% in terms of beacon packets, and 56.83% in terms of unsynchronized nodes. In addition, Elon prolongs the reprogrammable lifetime by a factor of 3.3.

Categories and Subject Descriptors: C.2.1 [Computer Communication Networks]: Network Architecture and Design—Distributed networks; D.4.7 [Operating Systems]: Organization and Design

General Terms: Design, Experimentation, Performance

Additional Key Words and Phrases: Wireless sensor network, reprogramming, component, reboot

# ACM Reference Format:

Wei Dong, Yunhao Liu, Chun Chen, Lin Gu, and Xiaofan Wu. 2014. Elon: Enabling efficient and long-term reprogramming for wireless sensor networks. ACM Trans. Embedd. Comput. Syst. 13, 4, Article 77 (February 2014), 27 pages.

DOI: http://dx.doi.org/10.1145/2560017

# 1. INTRODUCTION

Wireless sensor networks (WSNs) have been studied for a wide range of applications, such as ecological surveillance [He et al. 2004], habitat monitoring [Szewczyk et al. 2004], infrastructure protection [Szewczyk et al. 2004], etc. For a variety of reasons, such as upgrading node software, correcting software bugs, and patching security holes, WSN application code often needs to be updated after the deployment. Physically collecting deployed nodes, however, is either very difficult or infeasible in many

This work is supported by the National Science Foundation of China Grants No. 61202402, No. 61070155, the NSFC Major Program under grant 61190110, the NSFC Distinguished Young Scholars Program under grant 61125202, the Fundamental Research Funds for the Central Universities (2012QNA5007), and the Research Fund for the Doctoral Program of Higher Education of China (20120101120179).

Authors’ addresses: W. Dong, C. Chen, and X. Wu, College of Computer Science, Zhejiang University; email: {dongw, chenc, wuxiaofan}@zju.edu.cn; Y. Liu, School of Software and TNLIST, Tsinghua University; email: yunhao@greenorbs.com; L. Gu, Department of Computer Science and Engineering, Hong Kong University of Science and Technology; email: lingu@cse.ust.hk.

Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies show this notice on the first page or initial screen of a display along with the full citation. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, to republish, to post on servers, to redistribute to lists, or to use any component of this work in other works requires prior specific permission and/or a fee. Permissions may be requested from Publications Dept., ACM, Inc., 2 Penn Plaza, Suite 701, New York, NY 10121-0701 USA, fax +1 (212) 869-0481, or permissions@acm.org.

-c 2014 ACM 1539-9087/2014/02-ART77 \$15.00

DOI: http://dx.doi.org/10.1145/2560017

large-scale WSN systems. Enabling sensor nodes to be reprogrammable over the air is a crucial technique to address such challenges [Wang et al. 2006]. There are several key factors that affect the reprogramming efficiency and reprogrammable lifetime (we define the reprogrammable lifetime as the time period during which the sensor nodes can be reprogrammed) of a WSN, including the transferred code size, the loading cost, and the reprogramming voltage requirement.

First, the transferred code size greatly impacts the transmission overhead. To make a WSN reprogrammable, Deluge [Hui and Culler 2004] disseminates the entire program image, including the application code, the TinyOS kernel [Hill et al. 2000], and the reprogramming protocol. Hence, it must handle a large code size even for a simple application. For example, in the TinyOS 2.1 distribution [Hill et al. 2000], the Blink application with Deluge support consumes more than 35 KB code size. Such a code size results in a long transmission time and much energy consumption during dissemination. Stream [Panta et al. 2007] preinstalls the reprogramming protocol on the external flash. Consequently, for simple applications, it reduces the code size significantly. Specifically, for the Blink application in TinyOS 2.1, Stream needs approximately 9 KB transferred code size. Unfortunately, Stream is still far from sufficient for real-world and complex applications. For example, for the TestNetwork application in TinyOS 2.1, Stream needs more than 35 KB code size for reprogramming. This is because the TestNetwork application contains many TinyOS kernel services like CTP [Gnawali et al. 2009], Drip [Tolle and Culler 2005].

Second, the loading cost for executing the new code needs to be minimized. In particular, we should try to avoid full reboot for saving energy as well as to avoid dropping data. A system normally stores many state data such as routing tables [Gnawali et al. 2009], synchronization tables [Maroti et al. 2004], dissemination keys [Tolle and Culler´ 2005], etc. After rebooting, some nodes may take hours to fully come back online. For example, in a recent deployment on Reventador Volcano, reboots from a software error led to 3-day network outage, reducing mean node uptime from >90% to 69% [Chen et al. 2009; Werner-Allen et al. 2006].

Third, it is beneficial to avoid flash writes during reprogramming, as writing to flash requires a much higher voltage than the minimum operational voltage for the commonly used TelosB nodes. The MSP430F1611 microcontroller for the TelosB nodes can operate down to 1.8V [Polastre et al. 2005], while the minimum required voltage during a flash write or erase is 2.7V [Texas Instruments Inc.]. If the voltage falls below 2.7V during a write or erase, the result of the write or erase will be unpredictable [Texas Instruments Inc.]. As a result, based on study on the battery discharge curve [Lachenmann et al. 2007], network reprogramming has to be performed in the starting 23% duration of the entire network lifetime, significantly impairing the reprogrammability of existing reprogramming protocols that rely heavily on flash writes [Hui and Culler 2004; Panta et al. 2007; Marron et al. 2006; Panta and Bagchi 2009]. ´

To address these three key issues, we present Elon, a mechanism based on the TinyOS operating system [Hill et al. 2000]. Elon reduces the transmission overhead of both the TinyOS kernel services and the reprogramming protocol by defining replaceable component that needs to be frequently reprogrammed. Elon extends the nesC compiler to provide the boundary between replaceable component and the TinyOS kernel. The replaceable component is defined by replaceable code and replaceable data which are allowed to be declared by applications. Applications should also wire TinyOS kernel components which are mostly stable when the node software evolves. The intuition behind Elon’s design is that for real-world applications, the TinyOS kernel components are slowly changing while the application component is quickly changing. Therefore, by defining part of the application component as “replaceable,” we can reprogram the sensor node without the need of disseminating the TinyOS kernel which is typically the largest and most complex part of a program image. If kernel components need to be updated, Elon uses Deluge’s approach [Hui and Culler 2004] to update the entire code image. We can also use incremental reprogramming approaches by disseminating only the delta between two successive code versions. However, incremental reprogramming approaches [Panta and Bagchi 2009] involve more complexity in code rebuilding.

Elon trades off reprogramming flexibility for improved reprogramming performance: it needs modifications to existing application code to specify replaceable and system annotations, which limits flexibility about what can be replaced later on. Most existing approaches (e.g., Deluge) only need to bind a new component and allow any part of application code to be replaced. Elon’s approach suffices for most cases because the application behavior is mainly controlled by the application logic, which can be specified as replaceable. Therefore, we can “make the common case fast” when applying Elon in network reprogramming.

Elon allows applications to define “system” interfaces (via the “@system()” annotation) for accessing TinyOS kernel services (similar to syscalls in Unix-like systems [Kernighan and Pike 1984]). These interfaces define the boundary between the replaceable component and the TinyOS kernel. For downcalls (i.e., TinyOS commands) defined in the system interfaces, we relocate the references (i.e., command calls in the replaceable component) in the updated version to the corresponding addresses (i.e., command implementations in kernel components) in the base version. For upcalls (i.e., TinyOS events) defined in the system interfaces, we keep a system jump table to redirect the references (i.e., event calls/signals in kernel components) in the base version to the corresponding addresses (i.e., event handler implementations in the replaceable component) in the updated version.

By differentiating TinyOS kernel components from the replaceable component, Elon is able to reduce the transferred code size significantly. It also allows Elon to reboot a node in a fine-grained manner: Elon only reboots the replaceable component without losing TinyOS kernel data. Further, by placing the replaceable component on RAM (for Von Neumann architectures), it avoids flash writes, extending the reprogrammable lifetime significantly for the commonly used TelosB nodes.

We implement Elon on TinyOS 2.1 for TelosB nodes, and conduct comprehensive experiments to examine its performance. Evaluation results show that (i) Elon effectively reduces the transferred code size: it transfers up to 120–389 times less information than Deluge, 18–42 times less information than Stream, and 32%–51% less information than dynamic modules [Dunkels et al. 2006]. (ii) Elon significantly reduces the rebooting cost for core TinyOS components: for CTP [Gnawali et al. 2009] and Drip [Tolle and Culler 2005], it reduces the cost by 53.87% and 50.4%, respectively, in terms of beacon packets; for FTSP [Maroti et al. 2004], it reduces ´ the cost by 56.83% in terms of unsynchronized nodes. (iii) Elon extends the reprogrammable lifetime by a factor of 3.3 for TelosB nodes compared to existing reprogramming approaches. (iv) the overhead of Elon is acceptably small for real-world complex applications in terms of programmer cost, memory overhead, and execution overhead.

The contributions of this work are summarized as follows.

—We introduce the concept of replaceable component in reprogramming WSN. By applying it in Elon, we significantly reduce the transferred code size, improving the reprogramming performance in terms of dissemination time and transmission overhead.   
—We design a novel partial reboot mechanism to reduce the cost of full reboot, so that kernel data keeps persistent during the reprogramming process.

—We avoid flash operations for TelosB nodes [Polastre et al. 2005] which are based on the Von Neumann architecture. Elon not only improves reprogramming efficiency but also significantly prolongs the reprogrammable lifetime.   
—We implement Elon based on TinyOS 2.1, and evaluate its performance extensively. Results show that this design outperforms existing reprogramming approaches.

The rest of this article is structured as follows. Section 2 provides the necessary background. Section 3 presents the design details. Section 4 presents the evaluation results. Section 5 describes related work most pertinent to our work. Section 6 discusses limitations and our future work. Finally, Section 7 concludes this article.

# 2. BACKGROUND

Elon builds on top of the TinyOS operating system [Hill et al. 2000]. This section provides the necessary background on the mainstream reprogramming solutions for this system (Section 2.1), a real-world and complex application that motivates our design (Section 2.2), and core system components selected in our application (Section 2.3).

# 2.1. Deluge, Stream

Deluge [Hui and Culler 2004] is the mainstream reprogramming protocol distributed with TinyOS. Deluge enables complete system reprogramming, that is, the whole TinyOS-App image can be replaced by a new TinyOS-App image. In order to reprogram a network of sensor nodes for multiple times, the new TinyOS-App image must include the reprogramming protocol. Deluge stores the new code on the external flash during code dissemination. It uses a small bootloader, that is, TOSBoot, for loading the new code from the external flash onto the program flash. Finally, it forces a full reboot to execute the new code.

Stream [Panta et al. 2007] reduces the transferred code size by preinstalling the reprogramming protocol on the external flash as another code image (i.e., the reprogramming image). The application only needs to include a lightweight reprogramming support component which is responsible for rebooting to the reprogramming image when reprogramming is needed. After receiving the new application code, the reprogramming image reboots again to the new application code (the application image). Although Stream reduces the transferred code size significantly for simple applications, it is still insufficient for realworld and complex applications because the kernel components (such as CTP [Gnawali et al. 2009], Drip [Tolle and Culler 2005], FTSP [Maroti et al. 2004]) still need to be disseminated. Moreover, image switching with full ´ reboot degrades the reprogramming reliability because, according to our own experience, keeping a network in a consistent state (i.e., all nodes are in the reprogramming state or application state) is very difficult due to unreliable wireless links.

# 2.2. GreenOrbs

GreenOrbs [Mo et al. 2009] is a recently deployed wireless sensor network that aims at achieving long-term kilo-scale surveillance in the vast forest. In building such a complex system, the importance of network reprogramming cannot be emphasized too much: network reprogramming significantly reduces the manual efforts involved in traditional ways of collecting all nodes back, attaching to computers to burn new code, and redeploying all nodes in the fields.

The GreenOrbs uses TelosB nodes, and builds on top of the TinyOS operating system. The GreenOrbs program includes the CTP component [Gnawali et al. 2009] for collecting multiple types of sensor data, for instance, light, temperature, humidity, to a sink. To increase the flexibility, GreenOrbs includes the Drip component [Tolle and Culler 2005] for disseminating key system parameters, for instance, the duty cycle and transmission power settings. To achieve energy efficiency, GreenOrbs also includes the FTSP component [Maroti et al. 2004] for enabling synchronous low duty cycling. In ´ the current implementation, each node works three minutes every hour (i.e., 5% duty cycle). Existing mechanisms on TinyOS [Hui and Culler 2004; Panta et al. 2007] incur a large transferred code size for the GreenOrbs application, which is time-consuming and energy-inefficient to disseminate. For example, the entire GreenOrbs application consumes approximately 45KB, much larger than a single TinyOS packet with 29 bytes payload. Moreover, rebooting a node is costly, because after rebooting, a node loses all system states and needs to be awake until it is synchronized and fully functional again. Finally, the maximum voltage of the 2200mAh NiMH rechargeable battery that GreenOrbs currently uses is 2.8V. Because the energy consumption during the initial deployment can be quite large (all nodes must stay awake for synchronization before entering the working mode), the voltage of some nodes quickly falls below 2.7V, which makes most existing reprogramming mechanisms [Hui and Culler 2004; Panta et al. 2007; Marron et al. 2006; Panta and Bagchi 2009; Dunkels et al. 2006] useless during ´ the majority of the node lifetime.

# 2.3. CTP, Drip, FTSP

Most existing reprogramming mechanisms force a full reboot for executing the new code [Hui and Culler 2004; Panta et al. 2007; Marron et al. 2006; Panta and Bagchi ´ 2009]. However, reboot is not free. Computing systems maintain state to provide useful services. Rebooting a node clears this state and recovering this state can be costly for many important TinyOS kernel components [Chen et al. 2009].

CTP [Gnawali et al. 2009] is a collection tree protocol that collects data to a sink. A CTP node maintains two tables. The link estimation table stores the ETX estimate of each link. The routing table stores routing candidates and their corresponding path-ETX estimates to the sink. Rebooting a node causes a CTP node to lose information in these tables. Recovering this information is costly, either taking time to collect (for the link estimation table), or incurring a significant communication overhead for sending routing beacons (for the routing table) because the shared state has to be refreshed on the rebooting node at initialization time.

Drip [Tolle and Culler 2005] is a dissemination protocol for small data items. Drip stores the values of all data items in a RAM cache. Rebooting a Drip node causes a node to lose all values of the data items, which need to be collected again from other nodes, causing a significant increase of beacons after the reboot.

FTSP [Maroti et al. 2004] is a time synchronization protocol that establishes a global ´ time over the network. An FTSP node stores a table of sync beacons from other synchronized nodes to infer the relationship between its local time and the global time by linear regression. Rebooting a node clears this table, causing the rebooting node to remain temporally unsynchronized.

# 3. DESIGN

This section describes Elon’s design to address three reprogramming issues outlined in Section 1. Figure 1 illustrates Elon’s extensions to TinyOS. TinyOS kernel components should be included in the program of the base version for future use. For the base version, both kernel components and the replaceable component are programmed onto the program flash by the hardware in-system-programmer. A node works correctly after a reboot. For updated versions, only the replaceable component is generated and disseminated to each sensor node. When a node receives the new code, it uses a partial reboot mechanism to execute the new code.

Figure 2 shows Elon’s extensions to the nesC/GCC toolchain for TinyOS applications. The application and kernel components are in the nesC language. Applications can specify replaceable and system annotations. The modified nesC compiler processes these annotations and generates the C code (.c) along with a system jump table in assembly (.s). These source files (.c and .s) are further processed by the compiler (cc) and assembler (as) in the GCC toolchain. The output is comprised of a set of object files (.o). For the base version, we use a two-phase linking process to generate the executable

![](images/a2f11e501e6f4412db212ec4721ff6e5431b6676dde8e5685e84a6e477bfb2c0.jpg)



Fig. 1. Elon’s extensions to TinyOS. An application can specify replaceable component and TinyOS kernel components. System interfaces are boundaries between the replaceable component and TinyOS kernel components. The replaceable component calls system commands by address relocation. TinyOS kernel components signal system events by indirections via a system jump table.

![](images/e359ee15ba50585710d62e16fa5e5f13ae84fe55d9b497c2b3410e9502e24089.jpg)



Fig. 2. Elon’s extensions to the nesC/GCC toolchain. The process for generating the program of the base version is shown on the left, and the process for generating programs of the updated versions is shown on the right. Dashed boxes and arrows indicate additional steps for generating the base version. Gray boxes and arrows indicate additional steps for generating the updated versions.

ELF file. For updated versions, we have developed a tool (relocate.exe) to generate the relocated ELF file (for network reprogramming).

The next three sections detail Elon’s designs. Section 3.1 describes how Elon identifies and places the replaceable component. Section 3.2 describes how Elon identifies and implements system interfaces. Section 3.3 describes how Elon reboots a node to execute the code.

# 3.1. Replaceable Component

Applications need to define the replaceable component that needs to be frequently reprogrammed in the future. The replaceable component consists of the replaceable code, the replaceable data, and a system jump table. The replaceable code and replaceable data are declared by the application via the “@replaceable()” annotation. The system jump table is generated automatically by the modified nesC/GCC toolchain. Applications can specify the replaceable functions (code) and replaceable variables (data) separately. Applications can also specify an entire TinyOS component as replaceable. In this case, all variables and functions defined in this component default to replaceable unless they are explicitly specified as nonreplaceable. The following code shows the use of the annotation in detail.

```objectivec
module BlinkToCntLedsC {
    // ...
}
implementation {
    uint16_t counter @replaceable();
    void Boot.booted() @replaceable();
    void Timer.fired() @replaceable();
    // ...
} 
```

In the given example, the variable counter and the functions Boot.booted(), Timer.fired() are labelled as replaceable. Replaceable data and replaceable code are placed in separate sections, that is, .vdata for initialized replaceable data, .vbss for unintialized replaceable data, and .vtext for replaceable code. The existence of .vbss section helps reduce the transferred code size further because the initial values for the .vbss section do not need to be transferred (the values are known to be zero). The automatically generated system jump table is also placed in a separate section—the .jmptab section. We must provide the base addresses for these sections to the linker. Before we elaborate on the details of determining the base addresses, we first give an overview of the memory layout on TelosB nodes.

3.1.1. Memory Layout. The TelosB node has 10 KB data RAM (from address Ox1100 to address 0x38FF) and 48 KB internal program flash (from address 0x4000 to address 0xFFFF). The highest 32 bytes of code space (from address 0xFFE0 to address 0xFFFF) is reserved for storing the interrupt vectors.

The nesC compiler compiles the TinyOS nesC code to C code, which is further compiled and linked to an executable ELF by the GCC toolchain. The ELF file is used for linking and loading in traditional Unix-like systems. However, the standard ELF loader is usually missing for current sensor nodes. Therefore, the ELF file is further transformed to a simplified format, for instance, Intel hex (.ihex) or Motolora S Record (.srec). In the in-system-programming process, based on the ihex file or srec file, the hardware in-system-programmer writes necessary sections to the program flash, including the .text section (for the program code), the .data section (for initializing the .data section in RAM), and .vectors section (for interrupt vectors). When the code starts execution, it first executes an initializer (usually starts at address 0x4000) which is responsible for initializing the .data section and the .bss section in RAM. It then jumps to the main() function for further initialization, for instance, initializing the system stack, the registers, TinyOS components. Figure 3(a) illustrates the final memory layout after this process.

![](images/105daea7cb9da6f7b01362322e145fcb2e51cb9fd1bbf39491dd37c4333da2dc.jpg)



(（a）

![](images/4ac6127de2162a5cbf0f830a000ee5287f6b6a8143c098ae0c0a68490d9d6e05.jpg)



![](images/d42d86d63f8b1a54848946bddcf83074a927d723244962514715d562df712acf.jpg)



Fig. 3. Memory layout in RAM and the program flash. (a) memory layout for TinyOS. (b) memory layout for Elon after the first phase of linking. (c) memory layout for Elon after the two-phase linking process (the yellow boxes indicate the golden image).

3.1.2.Address Determination. Determining the base addresses of the .vdata，.vbss, .vtext, and .jmptab sections should satisfy two requirements. First, it should not conflict with other sections. Second, it should make efficient use of memory.

We place these sections as follows. First, the .vdata section and the .vbss section are placed in RAM. The .vdata section is directly after (in higher-address region than) the .bss section, and the .vbss section is directly after the .vdata section. Second, the .vtext section is placed in the program flash for the base version (serves as a golden image), and is placed in RAM for updated versions (in order to avoid flash writes during network reprogramming). For the base version, the .vtext section is directly after the .data section in the program flash. For updated versions, the .vtext section is directly after the .vbss section. Third, the .jmptab section is always placed in the start of RAM (i.e., 0x1100 for TelosB nodes) because the system jump table needs to be located at a fixed address, and it needs to be modifiable.

The base addresses of these sections should be specified to the linker prior to the linking stage. This means that in order to place the current section, we must obtain the sizes of all preceding sections before the linking stage (or after the compilation stage). However, the section sizes in the final executable file cannot be determined until the linking process is done. The reason is that the linker has to combine multiple object files to generate the final executable file [Levine 2000]. For example, the section sizes of .text, .data, and .bss cannot be determined after compilation if the application links additional external libraries. To address this issue, we adopt a two-phase linking process. We first specify nonconflict base addresses to the linker as follows:

$$
\mathrm{START} _ {\mathrm{vbss}} = \mathrm{END} _ {\mathrm{RAM}} - \mathrm{SIZE} _ {\mathrm{vbss}}
$$

$$
\mathrm{START} _ {\mathrm{.vdata}} = \mathrm{START} _ {\mathrm{.vbss}} - \mathrm{SIZE} _ {\mathrm{.vdata}}
$$

$$
\begin{array}{l} \text {START} _ {\mathrm{.vdata}} = \text {START} _ {\mathrm{.vbss}} - \text {SIZE} _ {\mathrm{.vdata}} \\ \text {START} _ {\mathrm{.jmptab}} = \text {END} _ {\text {flash}} - \text {SIZE} _ {\text {.vectors}} - \text {SIZE} _ {\text {.jmptab}} \end{array} \tag {1}
$$

$$
\mathrm{START} _ {\mathrm{.vtext}} = \mathrm{START} _ {\mathrm{.jmptab}} - \mathrm{SIZE} _ {\mathrm{.vtext+}. \mathrm{vdata}},
$$

where SIZE.vectors is a constant for a microcontroller (e.g., SIZE.vectors = 32 for MSP430F1611 used by TelosB nodes), and SIZE.vbss, SIZE.vdata, SIZE.jmptab, SIZE.vtext .vdata are all known after compilation because the corresponding sections are defined in a single compilation unit by prohibiting external libraries from being replaceable (note that the nesC compiler compiles all .nc files into a single C source file, app.c). Figure 3(b) illustrates the memory layout after this linking stage. After the first phase of linking, we obtain all the section sizes. Then we use it to determine the final base addresses.

$$
\begin{array}{l} \mathrm{START} _ {\text { .jmptab }} = \mathrm{START} _ {\mathrm{RAM}} \\ \mathrm{START} _ {\text { .data }} = \mathrm{START} _ {\text { .jmptab }} + \mathrm{SIZE} _ {\text { .jmptab }} \\ \mathrm{START} _ {\mathrm{.bss}} = \mathrm{START} _ {\mathrm{.data}} + \mathrm{SIZE} _ {\mathrm{.data}} \\ \mathrm{START} _ {\mathrm{.vdata}} = \mathrm{START} _ {\mathrm{.bss}} + \mathrm{SIZE} _ {\mathrm{.bss}} \\ \mathrm{START} _ {\mathrm{vbss}} = \mathrm{START} _ {\mathrm{vdata}} + \mathrm{SIZE} _ {\mathrm{vdata}} \tag {2} \\ \mathrm{START} _ {\text { .vtext }} ^ {\text { updated }} = \mathrm{START} _ {\text { .vbss }} + \mathrm{SIZE} _ {\text { .vbss }} \\ \mathrm{START} _ {\mathrm{.vtext}} ^ {\mathrm{golden}} = \mathrm{START} _ {\mathrm{Flash}} + \mathrm{SIZE} _ {\mathrm{.text+.data}} \\ \mathrm{START} _ {\mathrm{.jmptab}} ^ {\mathrm{golden}} = \mathrm{START} _ {\mathrm{.vtext}} ^ {\mathrm{golden}} + \mathrm{SIZE} _ {\mathrm{.vtext+}. \mathrm{vdata}} \\ \end{array}
$$

Figure 3(c) illustrates the final memory layout after this two-phase linking process. Note that, we reserve a golden image on the program flash for error recovery in the face of failure.

# 3.2. System Interface

System interfaces are the boundaries between the replaceable component and TinyOS kernel components. Applications need to customize the TinyOS kernel by wiring kernel components that will be used. The TinyOS kernel components will be installed onto the nodes for the first time and will not incur additional dissemination overhead when reprogramming the application component. Applications need to identify system interfaces, declared via the “@system()” annotation, for accessing kernel services. The following code shows the use of the annotation in detail.

```txt
module BlinkToCntLedsC {
    uses interface Boot @system();
    uses interface Timer<TMilli> @system();
    // ...
} 
```

In this example, both the Boot interface and the Timer<TMilli> interface are declared as system interfaces.

TinyOS interfaces contain commands (downcalls) and events (upcalls). For system interfaces, the commands are provided by the kernel components and represent the nonreplaceable part that does not need reprogramming; on the other hand, the events should be implemented by the application component and usually represent the replaceable part that needs reprogramming.

3.2.1. Modification to the nesC Compiler.We need to address issues in the nesC compilation process. The system commands and events should not be inlined because the caller part and callee part reside in different sections (i.e., the .text section and the .vtext section respectively). However, the current nesC compiler performs aggressive inlining for optimizing the execution efficiency. To address this issue, we modify the nesC compiler to make system commands and system events as “noninline.”   
3.2.2. Relocation and Indirection. For the program of the base version,the GCC toolchain relocates references to variables and functions correctly at link time. However, for any updated versions that will be reprogrammed onto the nodes through the network, changes in the source code make the address relocation incorrect. For system

commands, the GCC toolchain will relocate their addresses within the updated version. This is incorrect as we only reprogram the replaceable component of the updated version onto the nodes, references to system calls in the replaceable component should be relocated to corresponding addresses in the kernel components of the base version (that exist on the nodes). For example, it is possible that a system command Timer.startPeriodic() is located at 0x5000 in the base version while located at 0x5010 in the updated version. When generating an updated version, relocating references to 0x5010 by the GCC toolchain will be incorrect because 0x5000 is the actual address of the system call that is already programmed onto the nodes during the initial in-system-programming process. Also, for system events, it is often the case that their addresses in the updated version are different than the ones in the base version. Therefore, references to system events in the kernel component should point to corresponding addresses in the updated version. To address this issue, we adopt two approaches—relocation and indirection, for system commands and system events, respectively.

First, for system commands (also for the public kernel data), when generating the program of the updated version (i.e., the replaceable component), we relocate all references to system commands to the corresponding addresses in the base version. We develop a tool, relocate.exe, to do this kind of relocation. The following command shows the use of the tool in detail.

```batch
relocate.exe -d start_vdata -b start_vbss \
-t start_vtext -r main.exe main.o 
```

The base addresses for the .vdata, .vbss, and .vtext sections (i.e., start vdata, start vbss, start vtext) are determined by Eq. (2), main.exe is the executable file of the base version, and main.o is the object file of the updated version. The relocate.exe program parses the relocation entries in main.o and relocates the references in main.o to system commands implemented in main.exe. main.o is also the output file.

Second, for system events, we maintain a system jump table to redirect references in the base version to corresponding addresses in the updated version. The relocation technique for system commands described earlier does not apply here because we cannot modify the program code of the base version. For each system event that is replaceable, we allocate one entry in the system jump table. The following code shows the system jump table for the Boot system interface and the Timer<TMilli> system interface.

```powershell
br #BlinkToCntLedsC$Boot$booted
br #BlinkToCntLedsC$Timer$fired 
```

Invocation to these system events must be via the system jump table entries which redirect them to the actual implementations. When the addresses of system events change in the updated version, references in the base version do not change because the system jump table is placed at a fixed location in RAM (i.e., the starting address of RAM, described in Section 3.1). Instead, we modify the system jump table entries in RAM to reflect this change. The following command shows how to generate a correct system jump table for the updated version.

```batch
relocate.exe -t 1100 -r main.o jmptab.o 
```

We use relocate.exe again for relocating system jump table entries (jmptab.o) to the corresponding addresses in the program of the updated version (main.o). In the given command, 1100 (with hexadecimal base) denotes the starting address in RAM on

TelosB nodes. In this way, we retain access to system events which we are interested in in updated versions.

Some working details of relocate.exe are outlined as follows.

```txt
input: the ELF file needing relocation;
ref : the ELF file providing the symbol addresses.

parse input
for each rela in rela.vtext or rela.vdata or rela.jmptab in input {
    find corresponding sym
    if (sym locates in replaceable component) {
    relocate with the current version
    }
    else if (sym locates in kernel components) {
    // find corresponding symbol names
    if (sym.st_name == 0) { // if it is unnamed
    find named nsym that matches sym
    }
    getsymaddr_from_ref(symbol_name, ref)
    }
    use the symbol address to perform relocation
} 
```

The program takes two ELF files as inputs. The input file is the ELF file needing relocation and ref is the ELF file providing the symbol addresses. We first parse these two files for obtaining basic information such as locations of symbol tables and relocation tables. We then iterate all relocation entries in the replaceable component of the input file. For each relocation entry, we find the corresponding symbol entry. If the symbol locates in the replaceable component, we use symbol addresses in the input file for relocation. If the symbol locates in the kernel components, we use symbol addresses in the ref file for relocation. There is one practical issue worth mentioning. The relocation entry may refer to an unnamed symbol entry for relocation. There is no problem if the symbol locates in the replaceable component. However, if the symbol locates in kernel components, we need to obtain the corresponding symbol address in kernel components. For this purpose, we parse all symbol entries to find the named symbol entry for this relocation entry. Then we use the symbol name to find a matching symbol in the kernel components. Finally, when we obtain the symbol address, we perform actual relocation on the requested locations.

# 3.3. Reboot

There are two methods for programming a node with Elon, that is, in-systemprogramming, and network reprogramming. In the final stage of in-systemprogramming, the system executes a full reboot procedure. In the final stage of network reprogramming, we use a partial reboot mechanism in order to reduce the rebooting cost.

3.3.1. Full Reboot. In the final stage of in-system-programming, the system executes a full reboot procedure which is responsible for initialization for the data, system stack, the registers, TinyOS components, etc. Because Elon adds specific sections to the generated ELF file, we need to modify the default initializer generated by the GCC toolchain. By default, the reset interrupt service routine, \_reset\_vector initialize the .data and .bss sections, after which the main() function proceeds. The modified initialization procedure is as follows.

(1) Copy the default system jump table from the program flash to the start of RAM.   
(2) Initialize the .data section on RAM (i.e., copy the .data section from the program flash to RAM).   
(3) Initialize the .bss section on RAM to zero.   
(4) Initialize the .vdata section on RAM (i.e., copy the .vdata section from the program flash to RAM).   
(5) Initialize the .vbss section on RAM to zero.   
(6) Jump to the main() function which includes initialization of the system stack, the registers, and TinyOS components, etc.

Figure 3(c) shows the final memory layout after this procedure. There are two things that worth mentioning here. First, we program the replaceable component of the base version onto the program flash. This provides a golden image for error recovery in the face of failure. Second, we reduce the cost of copying the .vtext section to RAM by generating a default system jump table with entries pointing to corresponding locations in the program flash.

3.3.2. Partial Reboot. In the final stage of network reprogramming, we use a partial reboot mechanism in order to reduce the rebooting cost. The idea is similar to microreboot in general computing systems [Candea et al. 2004].

To avoid the use of external flash and make efficient use of RAM, we load the replaceable data and replaceable code onto RAM during code dissemination. A question in our design is whether the RAM can accommodate the replaceable code. Our experience in developing the GreenOrbs application demonstrate that it suffices for a large number of software changing scenarios. We will discuss this issue further in Section 6. Loading the new code on the fly will incur two problems. First, the current program will be corrupted. For example, the current program may handle a system Timer.fired() event periodically. During reprogramming, however, the implementation of Timer.fired() function could be partly rewritten. When this event is signaled, the system crashes. To address this issue, we rewrite all valid system jump table entries to point to a dummy event handler before reprogramming. Second, it may fail to receive a complete new program. To address this issue, we provide a rollback mechanism. We rollback to the golden image.

When we complete receiving and loading the replaceable data and replaceable code, we start a partial reboot procedure to restart the node. To summarize, Elon goes through the following steps for reprogramming a node.

(1) Write the system jump table entries to point to a default dummy event hander.   
(2) Receive data, and write replaceable data and replaceable code to RAM.   
(3) If the entire replaceable component is received correctly, go to step 5, else go to step 4.   
(4) Write the “golden” replaceable data to RAM. (the replaceable code will be located on the program flash for execution in the face of failure.)   
(5) Initialize the .vbss section on RAM to zero.   
(6) Write the system jump table: if the replaceable component is received correctly, write the newly received system jump table, otherwise write the “golden” default system jump table on the program flash.   
(7) Jump to the initialization procedure which includes initialization of the system stack, the registers, replaceable components, etc.

Elon uses two-levels of CRC checks to detect whether the update process is successful during the reception of the code update. The packet level CRC checks whether an incoming packet is correct. After receiving all packets comprising the updated code, Elon applies an image-level CRC to check whether the received code is correct.

Usually, network reprogramming employs an epidemic protocol like Deluge [Hui and Culler 2004] to ensure eventual consistency. A Deluge node periodically advertises the latest code version it owns. Neighboring nodes make requests to node that has the latest version. Eventually, all network nodes have the latest version of code. Hence, if a node is temporally disconnected during network reprogramming, it still can obtain the code update when it is connected later on. If the network happens to have different updated versions of a certain application and Elon does not instantly stop the running application for acquiring the latest code, the design of the new application needs to be compatible with the old versions to ensure correctness.

Compared to full reboot, the partial reboot procedure does not include initialization for the kernel data. This is important for keeping system states persistent across reboots.

It is worth noting that the application state may be discarded during the reboot. Whether the application state will be discarded depends on whether the corresponding variables are specified as replaceable or not. It should be noted that the “@replaceable” annotation is at the granularity of individual variables and individual functions, instead of a “component”.

(1) If variables are nonreplaceable, the state will be preserved across reboot. However, the space occupied by the variables cannot be released even if the variables are deleted in an updated version. (2) If variable are specified as replaceable, the state will not be preserved across reboot by default. If the sensor network application needs to preserve state despite a reboot, it is necessary to use an external mechanism that saves the application state to nonvolatile memory [Marron et al. 2006]. ´

# 4. EVALUATION

This section evaluates how Elon improves sensor network reprogramming efficiency (in terms of transferred code size and rebooting cost) and reprogrammable lifetime. We also evaluate the overhead Elon introduces. Section 4.1 describes the evaluation methodology. Section 4.2 shows evaluation results in terms of transferred code size. Section 4.5 shows evaluation results in terms of rebooting cost. Section 4.6 shows evaluation results in terms of reprogrammable lifetime. Finally, Section 4.7 shows Elon’s overhead in terms of programmer cost, memory overhead, and execution overhead, respectively.

# 4.1. Methodology

All experiments use TelosB nodes. To evaluate the performance of Elon, we consider the following software change scenarios for TinyOS applications.

(1) BlinkToCntLeds. We change the Blink application to the CntToLeds application. Blink is an application that toggles one LED periodically, and CntToLeds is an application that displays the lowest three bits of the counting sequence on the LEDs.   
(2) BlinkToCntRfm. We change the Blink application to the CntToLedsAndRfm application. CntToLedsAndRfm is an application that transmits the counting sequence over the radio and displays the lowest three bits of the counting sequence on the LEDs.   
(3) GreenOrbs. We consider a real-world software change scenario in the development of GreenOrbs. In the program of the base version, each node periodically reports sensor data to a collection sink by CTP; we want to reprogram an updated version in which each node additionally reports diagnostic packets to give more visibility into the system.

Table I. Comparison of transferred code size for Deluge, Stream, and Elon (in bytes). For the GreenOrbs application, Deluge cannot be used simply because the program size with Deluge support exceeds the maximum program size for TelosB nodes 

<table><tr><td></td><td>Deluge</td><td>Stream(lower bound)</td><td>Elon</td></tr><tr><td>BlinkToCntLeds</td><td>32008</td><td>2674</td><td>82</td></tr><tr><td>BlinkToCntRfm</td><td>32182</td><td>11608</td><td>266</td></tr><tr><td>GreenOrbs</td><td>&gt;48 KB</td><td>47640</td><td>2440</td></tr></table>

For network experiments, we use a testbed of 10 TelosB nodes in a linear structure. We set the transmission power level to 3 to emulate multihop transmissions. To get the statistics, we wrote two components, that is, RamLogC and ExtLogC, to log aggregated data in RAM, and to log system events in the external flash. In order to get the timing information, there is a sync node that periodically broadcasts sync beacons to synchronize all other nodes at the maximum transmission power. For synchronization, we use the packet-level time synchronization interface provided by TinyOS, which can achieve synchronization accuracy in less than 1 ms [Miklos Maroti and Janos Sallai]. After the experiments, we gather the data through one-hop wireless links.

# 4.2. Transferred Code Size

Table I shows the transferred code sizes for three reprogramming approaches, that is, Deluge [Hui and Culler 2004], Stream [Panta et al. 2007], and Elon, for the software change cases mentioned earlier. As the Stream code is not available for TinyOS 2.1, we use a lower bound for comparison (i.e., applications with Stream support do not wire the Stream support component). We can see that the code sizes for Deluge are very large because applications with Deluge support wire the DelugeC component which consumes a large fraction of code size. For the GreenOrbs application, Deluge cannot be used simply because the program size with Deluge support exceeds the maximum program size for TelosB nodes. For reprogramming simple applications, for instance, BlinkToCntLeds and BlinkToCntRfm, Stream reduces the code size significantly. This is because Stream does not include the reprogramming protocol. Instead, it preinstalls it on the external flash as another code image. However, for reprogramming complex applications, for instance, GreenOrbs, the transferred code size for Stream is still very large because a large number of kernel components (such as CTP, Drip, FTSP) are wired in the application and need to be transferred during reprogramming. Elon reduces the overhead of kernel components by identifying replaceable component. From the figures shown in Table I, we can see that Elon reduces the transferred code size significantly compared to Deluge and Stream: it transfers 120–389 times less information than Deluge, and 18–42 times less information than Stream.

# 4.3. Comparison to Dynamic Modules

Compared to dynamic modules, Elon does not incur the overhead of the relocation table, further reducing the dissemination cost. To investigate the overhead of metadata in dynamic modules, we use 11 benchmarks in SenSpire OS [Dong et al. 2011] as well as 5 benchmarks in FlexCup/TinyOS 2.1 [Marron et al. 2006]. ´

SenSpire OS is a micro embedded operating system for sensor networks. To achieve system predictability, it adopts two-phase interrupt servicing and predictable thread synchronization. To achieve programming flexibility, it employs a hybrid model for both event-driven programming and multithreaded programming. To retain efficiency, it employs stack sharing and modular design techniques.

![](images/aac5ac6d055f2d375e6746e0478d517514bb3ea1da2d9d56a220a0f41d045943.jpg)



Fig. 4. SELF module size breakdown.

SenSpire OS adopts a modular design architecture. A typical application needs to bind the following modules: (1) kernel which implements interrupt servicing and task scheduling; (2) mcu which implements device drivers on the MCU; (3) sensor which implements the sensing capability; (4) radio which implements the radio stack; (5) lib which implement common functions such as printing, CRC checks, etc.

SELF is an optimized module file format for SenSpire OS. It uses a series of techniques to reduce the module file size while retaining essential flexibility.

Figure 4 shows the application module sizes based on SenSpire OS. The application module is a single module decoupled from SenSpire OS kernel modules. The application modules need to invoke services in SenSpire OS kernel modules at run time. In Figure 4, modules kernel, mcu, sensor, radio, lib are treated as SenSpire OS kernel modules. We can see that the total sizes of these modules vary from 170 bytes to 918 bytes, depending on the complexity of the benchmark. The fractions of metadata vary from 0.32 to 0.51. Elon can avoid such overheads.

FlexCup is a modular code update mechanism based on TinyOS. Unlike traditional TinyOS that compiles the code into a single monolithic image, FlexCup exploits a new feature in the nesC compiler to compile TinyOS components into binary components that can be linked during run time. By this mechanism, FlexCup can update individual binary components instead of the entire code image. Compared to standard ELF, FlexCup employs several techniques to reduce the metadata overhead. First, symbols in the symbol and relocation tables are identified by a two-byte id instead of a humanreadable string. Second, the size of the relocation tables is compressed by combining entries with the same id. Figure 5 shows a comparison of FlexCup and Elon based on TinyOS 2.1. It is worth noting that FlexCup was originally developed based on TinyOS 1.x. We obtain the FlexCup module size by compiling the nesC components into binary components and applying the same reduction techniques described in the FlexCup paper [Marron et al. 2006]. We can see that FlexCup imposes an additional overhead. ´ Moreover, Elon does not require I/O operations on external flash for TelosB nodes while FlexCup requires extensive flash I/Os in order to perform node-side relocation.

# 4.4. Dissemination Time and Transmission Overhead

A small transferred code size translates to smaller dissemination time and smaller transmission overhead, which is important for energy-constrained sensor networks. To see the impact of the transferred code size on the dissemination time and the transmission overhead, we disseminate these applications through the Deluge protocol.

![](images/ffc992cd39d349410799707f3919191f7e729a0a893ca6ba5d90d32a9dc67f5e.jpg)



Fig. 5. A comparison of Elon and FlexCup.

![](images/0af148528e1bc01e4d757c5f6ce15840838ea36d0159ce326b1630b7571c34ed.jpg)



Fig. 6. Comparison of dissemination time (in seconds) for Deluge, Stream, and Elon.

As mentioned before, we obtain the timing information by packet-level synchronization provided in TinyOS, and we get the number of packet transmissions by use of the RamLogC component. Figure 6 compares the dissemination times of Deluge, Stream, and Elon. The result of GreenOrbs with Deluge support is not available because the program size exceeds the maximum program size for TelosB nodes, hence cannot be compiled correctly. As expected, Elon outperforms Deluge and Stream significantly, especially for complex applications with a large number of kernel components. For the two relatively simple applications, that is, BlinkToCntLeds and BlinkToCntRfm, Elon is 16.05–16.39 times faster than Deluge, and 2.2–4.87 times faster than Stream. For the complex GreenOrbs application, Elon is 8.82 times faster than Stream. This illustrates that replaceable component identification and isolation are very important for reprogramming real-world and complex applications. Figure 7 compares the total number of packets transmitted by all nodes in the network for Deluge, Stream, and Elon. Like dissemination time, Elon reduces the transmission overhead significantly compared to other approaches. As indicated by the GreenOrbs application, avoiding transmissions of kernel components in Elon results in a very large savings in the transmission overhead.

# 4.5. Rebooting Cost

The rebooting cost of Elon is low compared to existing reprogramming approaches. First, we eliminate the cost of flash I/O operations which incur extra energy consumption on current sensor nodes. For example, a flash I/O operation on TelosB nodes consume 5–12 mA, which is much larger than 0.5 mA energy consumption when the CPU is active. In Deluge, after a reboot, the TOSBoot copies the program code from the external flash to the program flash. Stream incurs even more flash I/O operations due to image switching. Elon does not have this overhead. Second, partial reboot is faster than full reboot because reinitialization of kernel data is not needed. Table II compares the full reboot time and the partial reboot time. We can see that Elon’s partial reboot mechanism is 5%–35% faster than the full reboot approach. Finally and most importantly, Elon does not lose kernel data caused by a full reboot. To see the impact of losing kernel data, we conduct experiments running typical TinyOS services, for instance, CTP [Gnawali et al. 2009], Drip [Tolle and Culler 2005], and FTSP [Maroti ´ et al. 2004].

![](images/2c6acc5ed87a69235a63698a17ca764912c135ff6089f2c17a202ca4bf288f74.jpg)



Fig. 7. Comparison of total number of packet transmissions for Deluge, Stream, and Elon.

Table II. Full Rebooting Time and Partial Rebooting Time for the Updated Applications (ms) 

<table><tr><td></td><td>TinyOS</td><td>Elon</td></tr><tr><td>BlinkToCntLeds</td><td>20.5</td><td>16.93</td></tr><tr><td>BlinkToCntRfm</td><td>23.3</td><td>17.25</td></tr><tr><td>GreenOrbs</td><td>87.6</td><td>83.2</td></tr></table>

For CTP [Gnawali et al. 2009], the cost of full reboots is the increase of routing beacons. Figure 8 shows the total accumulated number of beacons for the CTP protocol during a total of 2000 seconds. We compare the results when there are no-reboots, full reboots, and partial reboots. We use the RamLogC component for logging the accumulated number of beacons at each individual node. This information is transmitted to the sink by CTP. For no-reboots, the total number of beacons is 255; for full reboots, the total number of beacons increases to 594; for partial reboots, the number of beacons is 274. CTP uses a Trickle timer [Levis et al. 2004] to control the frequency of beaconing rate. When a node reboots, it will have a high frequency of beaconing rate in order to find new routes. Elon’s partial reboot mechanism keeps system states persistent across reboots. Compared to full reboots, Elon reduces the rebooting overhead by 53.87% in terms of beacon packets.

For Drip [Tolle and Culler 2005], the cost of full reboots is also the increase of beacon packets. Figure 9 shows the total accumulated number of beacons for the Drip protocol disseminating 32 keys during a total of 2000 seconds. We compare the results when there are no-reboots, full reboots, and partial reboots. Similarly, we use the RamLogC component for logging purpose. After the experiment, we collect the data individually for each node. As Drip also uses the Trickle timer [Levis et al. 2004] to control the beaconing rate, similar results can be obtained. For no-reboots, the total number of beacons is 2020; for full reboots, the total number of beacons increases to 4191; for partial reboots, the number of beacons is 2079. Compared to full reboots, Elon reduces the rebooting overhead by 50.4% in terms of beacon packets.

![](images/b6410085844fddec22f85b3e18b4c55be14dabe5ca9db8e4b600483943eb292f.jpg)



Fig. 8. Comparison of the total number of beacons in CTP for full reboots (three reboots), partial reboots, and no-reboots.

![](images/11b5ac370cadb6a6c22b6d015b5a5e0c1a74a53f290f44fd5bca21381d568c5a.jpg)



Fig. 9. Comparison of the total number of beacons in Drip for full reboots (three reboots), partial reboots, and no-reboots.

For FTSP [Maroti et al. 2004], the cost of full reboots is the decrease in the number ´ of synchronized nodes. Figure 10 shows the CDF of the number of synchronized nodes by querying the system periodically for a total of 600 times, when there are no-reboots, full reboots, and partial reboots. When there are reboots, we reboot the nodes every two minutes with a random startup time. Packet losses and other real-world variations cause a nonzero number of unsynchronized nodes even in the no-reboot case. Without reboots, there are approximately 74.52% synchronized nodes on average. With full reboots, there are approximately 35.05% synchronized node on average due to relatively high rebooting rate. With partial reboot, there are approximately 71.96% synchronized nodes on average. Compared to full reboot, Elon’s partial reboot mechanism reduces the rebooting overhead by 56.83% in terms of unsynchronized nodes.

![](images/680ca41feeb6fa40384a4a71acd1c5df43143da7bdff4908438bcb178dfd37be.jpg)



Fig. 10. CDF of synchronized nodes in FTSP when there are full reboots, partial reboots, and no-reboots.

# 4.6. Reprogrammable Lifetime

To investigate the reprogrammable lifetimes of different approaches, we deployed an indoor prototype system that runs the basic functionality of the GreenOrbs application. This version of program uses CTP to collect the voltage and other sensor data from multiple nodes. In this version, we do not include the FTSP component for fast implementation. To enable energy efficiency, we use the default low power listening (LPL) MAC in TinyOS. We use a 20 seconds data reporting rate and a 250ms sleep interval. A 250 ms sleep interval translates to 4.4% duty cycle when there is no traffic, with 11 ms check interval in the implementation of TinyOS. The actual duty cycle in our case should be much higher than 4.4% due to high data reporting rate (the LPL MAC waits for an additional duration of 100 ms when a packet is received). We successfully run the application for approximately 40 days.

Figure 11 shows the voltage readings for five typical nodes. We can see that the voltage decreases from 3V to 1.8V, during which the system operates correctly. This is because TelosB nodes have a minimum voltage of 1.8V for program execution [Polastre et al. 2005]. However, flash writes require a much higher voltage to ensure reliability. Specifically, flash writes on TelosB requires at least 2.7V as documented in the MSP430 users’ guide [Texas Instruments Inc.]. If the voltage falls below 2.7V during a write or erase, the result of the write or erase will be unpredictable [Texas Instruments Inc.]. This means that, in this application scenario, the reprogrammable lifetime is only 11 days for existing approaches that require flash writes (including Deluge [Hui and Culler 2004], Stream [Panta et al. 2007], FlexCup [Marron et al. 2006], etc). Elon ´ extends the reprogrammable lifetime to 37 days (or more), by a factor of 3.3.

# 4.7. Overhead

This section evaluates Elon’s overhead in term of programmer cost, memory overhead, and execution overhead, respectively.

4.7.1.Programmer Cost. First, Elon requires programmers to identify TinyOS kernel components in the base version. Table III compares the number of TinyOS kernel components for Deluge and Elon. We do not show the results for Stream as the results are similar to Deluge. For the software change scenario of BlinkToCntLeds, there is no increase. For the software change scenario of BlinkToCntRfm, the increase is 75%. This is because TinyOS kernel components (such as radio) are not used in the base version, but they will be used in the updated version. Therefore, they should be additionally wired in the application. For the software change scenario of GreenOrbs, however, no additional kernel components should be wired because the program of the base version already uses a large number of kernel components. This results indicate that for complex and well designed applications, the number of additional kernel components should be small because a lot of kernel components should be already used in the base version.

![](images/adea83c1a0df991ce22e390cd503550edf1958121e3dcae262b1bf48e2b8435e.jpg)



Fig. 11. Voltage readings for five typical nodes running the CTP protocol with default TinyOS LPL MAC.

Table III. Number of TinyOS Kernel Components in the Base Version 

<table><tr><td></td><td>Deluge</td><td>Elon</td><td>increase</td></tr><tr><td>BlinkToCntLeds</td><td>4</td><td>4</td><td>0%</td></tr><tr><td>BlinkToCntRfm</td><td>4</td><td>7</td><td>75%</td></tr><tr><td>GreenOrbs</td><td>25</td><td>25</td><td>0%</td></tr></table>

Second, Elon requires programmers to specify replaceable and system annotations. Depending on reprogramming needs, the number of annotations can be different. However, each annotation requires a simple @replaceable() and @system() code addition. Therefore, the cost of annotations is small.

When kernel components do not exist in the base version but are required by the updated version, we can fall back to the Deluge approach for reprogramming the entire software system.

4.7.2. Memory Overhead. We examine the Elon's memory overhead in terms of RAM consumption and program flash consumption, respectively. There are several factors that impact the Elon’s memory overhead. First, we place replaceable code on RAM, which increases RAM consumption and decreases program flash consumption. Second, we need to include the reprogramming support component, which increases program flash consumption. Third, we specify some TinyOS interfaces as “system”, which may increase program flash consumption (system commands and events are included in even if they are not referenced in the base version) or decrease program flash consumption (system functions are noninlined).

Table IV. RAM Consumption in Bytes for the Programs of the Base Version 

<table><tr><td></td><td>TinyOS</td><td>Elon</td><td>increase</td></tr><tr><td>BlinkToCntLeds</td><td>35</td><td>310</td><td>785.7%</td></tr><tr><td>BlinkToCntRfm</td><td>35</td><td>554</td><td>1482%</td></tr><tr><td>GreenOrbs</td><td>6326</td><td>7820</td><td>23.6%</td></tr></table>

Table V. RAM Consumption in Bytes for the Programs of the Updated Version 

<table><tr><td></td><td>TinyOS</td><td>Elon</td><td>increase</td></tr><tr><td>BlinkToCntLeds</td><td>37</td><td>384</td><td>937.8%</td></tr><tr><td>BlinkToCntRfm</td><td>320</td><td>796</td><td>148.7%</td></tr><tr><td>GreenOrbs</td><td>6426</td><td>8146</td><td>26.8%</td></tr></table>

Table VI. Program Flash Consumption in Bytes for the Programs of the Base Version 

<table><tr><td></td><td>TinyOS</td><td>Elon</td><td>increase</td></tr><tr><td>BlinkToCntLeds</td><td>2522</td><td>6836</td><td>171%</td></tr><tr><td>BlinkToCntRfm</td><td>2522</td><td>15820</td><td>527.2%</td></tr><tr><td>GreenOrbs</td><td>47414</td><td>47494</td><td>0.17%</td></tr></table>

Table IV shows the RAM consumption for the programs of the base version and Table V shows the RAM consumption for the programs of the updated version. For the two simple cases, that is, BlinkToCntLeds and BlinkToCntRfm, the relative increases in RAM consumption are quite large. However, the absolute values are sufficiently small compared to a total of 10 KB RAM on TelosB nodes. For the complex GreenOrbs case, the relative increase in RAM consumption drops to 23.6%–26.8%.

Table VI shows the program flash consumption for the programs of the base version and Table VII shows the program flash consumption for the programs of the updated version.

We can see that, for the two simple software change scenarios, that is, BlinkToCntLeds and BlinkToCntRfm, the increase is large because the reprogramming support component consumes a fixed code size of approximately 4 KB. However, for the complex case, that is, GreenOrbs, the increase is very small for the base version (0.17%), and is even negative for the updated version (−0.3%). The reason for the negative increase is because the updated replaceable component is placed in RAM, instead of in the program flash.

4.7.3. Execution Overhead. Elon slightly increases the execution overhead because of two reasons. First, the system annotation forces all system commands to be noninlined, hence there is an additional cost compared to the case when the functions can be inlined. Second, the system annotation forces all system events to be noninlined and redirected via a system jump table. This is an additional cost.

We use a Tektronix TDS3034C oscilloscope to measure the execution time of a TinyOS task. We instrument the TinySchedulerC component to provide such information. Table VIII shows the task execution times for the programs of the base version, and Table IX shows the task execution times for the programs of the updated version. We did not show the results for the GreenOrbs application because it involves a large number of TinyOS tasks which complicates the measurement. From the figures in Tables VIII and IX, we can see that the increase is small, especially for relative complex tasks.

Table VII. Program Flash Consumption in Bytes for the Programs of the Updated Version 

<table><tr><td></td><td>TinyOS</td><td>Elon</td><td>increase</td></tr><tr><td>BlinkToCntLeds</td><td>2642</td><td>6836</td><td>158.7%</td></tr><tr><td>BlinkToCntRfm</td><td>11576</td><td>15820</td><td>36.6%</td></tr><tr><td>GreenOrbs</td><td>47640</td><td>47494</td><td>-0.3%</td></tr></table>

Table VIII. Task Execution Times for the Programs of the Base Version (μs) 

<table><tr><td></td><td>Task</td><td>TinyOS</td><td>Elon</td><td>increase</td></tr><tr><td>BlinkToCntLeds</td><td>Timer.fired</td><td>273</td><td>296</td><td>8.4%</td></tr><tr><td>BlinkToCntRfm</td><td>Timer.fired</td><td>273</td><td>306</td><td>12.0%</td></tr></table>

Table IX. Task Execution Times for the Programs of the Updated Version (μs) 

<table><tr><td></td><td>Task</td><td>TinyOS</td><td>Elon</td><td>increase</td></tr><tr><td>BlinkToCntLeds</td><td>Timer.fired</td><td>308</td><td>323</td><td>4.8%</td></tr><tr><td rowspan="3">BlinkToCntRfm</td><td>Timer.fired</td><td>1640</td><td>1653</td><td>0.79%</td></tr><tr><td>sendDone</td><td>98.4</td><td>105</td><td>6.7%</td></tr><tr><td>receive</td><td>260</td><td>262</td><td>0.77%</td></tr></table>

To get further insights how Elon’s design impacts real-world complex applications, for instance, GreenOrbs, we measure the cost of an individual function (contains 5 nops) to analyze GreenOrbs’ execution overhead. Table X shows the execution cost of this function when it is inlined, it is noninlined, and it is noninline and indirected. We can see that, compared to an inlined function, the effect of function noninlining increases execution time by 2.5 μs; the effect of function noninlining and indirection increases the execution time by 4.5μs.

The most complex event handler in GreenOrbs involves 6 system calls (to system commands). Considering the cost of signaling the event handler, this incurs an additional cost of $6 \times 2 . 5 + 4 . 5 = 1 9 . 5 ~ \mu \mathrm { s }$ . This translates to at most $\begin{array} { r } { \frac { 1 9 . 5 } { 9 8 . 4 } = 0 . 2 } \end{array}$ increase in the execution time because 98.4 μs is the minimum task execution time we have so far measured.

We argue that this increase in execution time will not impact the energy efficiency of the GreenOrbs application. As mentioned earlier, the GreenOrbs application works 3 minutes every hour. Energy consumption per hour is thus $2 0 \mathrm { { m A } \times 1 \bar { 8 0 } s + 0 . 5 \mathrm { { m A } \times t , } }$ where 20mA is the energy consumption when radio is on, the 0.5 mA is the energy consumption when the CPU is active [Fonseca et al. 2008], t is the total execution time (t < 180s). With Elon, the energy consumption is $\leq 2 0 \mathrm { m A } \times 1 8 0 \mathrm { s } + 0 . 5 \mathrm { m A } \times 1 . 2 \mathrm { t }$ . Therefore, the energy consumption increases at most

$$
\frac {2 0 \mathrm{mA} \times 1 8 0 \mathrm{s} + 0 . 5 \mathrm{mA} \times 1 . 2 \times 1 8 0 \mathrm{s}}{2 0 \mathrm{mA} \times 1 8 0 \mathrm{s} + 0 . 5 \mathrm{mA} \times 1 8 0 \mathrm{s}} - 1 = 0. 0 3.
$$

Hence, the energy efficiency and lifetime of the sensor network will not be noticeably impacted.

# 5. RELATED WORK

Reprogramming wireless sensor networks has been an active research area in recent years [Wang et al. 2006; Hui and Culler 2004; Kulkarni and Wang 2005; Panta et al.

Table X. Execution times of an individual function containing 5 nop()s when it is inlined, it is noninlined, and it is noninlined and indirected (μs) 

<table><tr><td></td><td>execution time</td></tr><tr><td>5 nop()s inlined</td><td>10.5</td></tr><tr><td>5 nop()s noninlined</td><td>13</td></tr><tr><td>5 nop()s noninlined and indirected</td><td>15</td></tr></table>

2007; Naik et al. 2005; Huang and Setia 2008; Hou et al. 2008; Panta and Bagchi 2009]. Several systems, such as Mate [Levis and Culler 2002] and VM\* [Koshy and Pandey 2005b], provide virtual machines that run on resource-constrained sensor nodes. They allow for dissemination of a small code size because the virtual machine code is much more compact than the native code. However, the execution of virtual machine code is less efficient than native code if the program does intensive computation. Also, the virtual machine code is less expressive than native code.

TinyOS [Hill et al. 2000] is a widely used operating system for sensor networks. TinyOS does not support loadable modules. An application is compiled with TinyOS to form a single TinyOS-App image. Deluge [Hui and Culler 2004] provides reprogramming support for TinyOS applications. As sensor nodes need to be reprogrammed for multiple times, Deluge transfers the single TinyOS-App image along with the reprogramming protocol. After a node receives a new TinyOS-App image, the TinyOS bootloader (i.e., TOSBoot) copies the code from the external flash to the program flash, and it forces a reboot to execute the new code. Stream [Panta et al. 2007] reduces the transferred code size by preinstalling the reprogramming protocol on the external flash as another application image (i.e., the reprogramming image). During the reprogramming process, each node first reboots to the reprogramming image for retrieving the new application code. When the new application code is received, each node reboots again to the new application. Stream reduces the code size significantly for simple applications. However, it is still insufficient for real-world and complex applications which usually include a large number of kernel components. Moreover, Stream uses full reboots to switch between the reprogramming image and the application image. Therefore, it incurs the cost of full reboot and more importantly, according to our own experience, keeping a network in a consistent state (i.e., all nodes are in the reprogramming state or the application state) is very difficult because of unreliable wireless links.

The SOS [Han et al. 2005], Contiki [Dunkels et al. 2004, 2006], and the FlexCup extension [Marron et al. 2006] to TinyOS support loadable modules. In these systems, ´ individual modules can be loaded dynamically on the nodes. Specific challenges exist in these systems. First, they require disseminating symbol tables and relocation tables for linking and relocating. These may be quite large, typically 45% to 55% of the object file [Koshy and Pandey 2005a; Panta and Bagchi 2009]. Second, they make extensive use of flash. Therefore, they cannot reprogram a sensor network when the voltage of certain nodes falls below 2.7V (but above 1.8V) for the commonly used TelosB nodes [Texas Instruments Inc.], which limits the reprogrammable lifetime.

Incremental reprogramming [Jeong and Culler 2004; Koshy and Pandey 2005a; von Richenbash and Wattenhofer 2008; Panta and Bagchi 2009; Hu et al. 2009] is a technique to reduce the transferred code size by disseminating a program difference. Such research is complementary to our work. We can generate the incremental changes for the replaceable component to further reduce the code size. The work of compressing the program code [Tsiftes et al. 2008] and disseminating with network coding [Hagedorn et al. 2008; Rossi et al. 2010; Hou et al. 2008] is also complementary to our work. We can further use these techniques to reduce the transferred code size and the dissemination cost.

Reconfigurability can also be achieved by disseminating parameters understood by the program of the base version through Drip [Tolle and Culler 2005], Dip [Lin and Levis 2008], or DHV [Dang et al. 2009]. Although this approach is lightweight (e.g., the transferred code size is small, and it does not require a minimum voltage of 2.7V), it requires all parameters to be well defined in the base version, which is hard to design in the early stage of software developments. With this technique, the application logic cannot be modified when there are no corresponding parameters predefined in the base version. Elon is much more flexible: both the replaceable data and the replaceable code can be modified once they have been identified.

# 6. DISCUSSION

A basic observation to reduce the transferred code size is to disseminate what is needed, in other words, the application. Similar to the design concept of loadable modules, our approach identifies the replaceable component that needs to be reprogrammed. With this technique, common kernel components (that do not need to be reprogrammed) do not need to be disseminated. The traditional dynamic linking and loading technique [Levine 2000; Dunkels et al. 2006] for loadable modules is not appropriate for our scenario because of two reasons. First, it requires sophisticated OS support (e.g., the ELF loader) which is currently unavailable in TinyOS. Second, it incurs additional overhead, for instance, symbol tables and relocation tables. With a simplified design, we are able to provide a mechanism with minimal OS support and smaller transferred code size. We trade off less flexibility in the program layouts that can be slightly different on different sensor nodes. However, different program layouts can be easily avoided by programming the same binary code in the in-system-programming process.

For the Mica series node, our approach cannot prolong the reprogrammable lifetime because of two reasons. First, the Mica series node uses the Atmega128L microcontroller, which is based on the Harvard architecture. Therefore, the program code cannot be placed in data RAM for execution. Second, the minimum operational voltage is 2.7V (instead of 1.8V), that is, nodes die once the voltage falls below 2.7V. Another limitation of the Mica series node is that the RAM size is only 4KB. Our approach, however, is still useful by placing the replaceable code on the program flash. It is still effective in reducing the transferred code size, and, at the same time, avoiding the cost of full reboot.

The more recent Telos node uses a low-power MSP430F1611 microcontroller which is based on the Von Neumann architecture. The MSP430F1611 microcontroller can operate down to 1.8V. However, the minimum voltage during a flash write or erase operation is still 2.7V. If the voltage falls below 2.7V during a write or erase, the result of the write or erase will be unpredictable [Texas Instruments Inc.]. Therefore, it is beneficial to avoid flash writes during reprogramming so as to prolong the reprogrammable lifetime. Our approach avoids flash writes by placing replaceable component on RAM.

Today, even with many new offerings in microcontrollers, the MSP430F1611 remains a competitive choice for sensor platform design [Dutta et al. 2008]. Our design illustrates that avoiding flash writes is beneficial for low-power microcontrollers (that can operate down to 1.8V), because most low-power flash requires at least 2.5V–2.7V for writing or erasing, for instance, the program flash of MSP430F161x, ST M25P80 (external flash for the TelosB node) [STMicroelectronics Inc.], AT45DB041B (external flash for the MicaZ node) [Atmel Corporation], etc.

A question in our design is whether we can accommodate the replaceable code in RAM which is a precious resource for sensor nodes. Our experience in developing the GreenOrbs application using TelosB nodes demonstrates that it suffices for many software change scenarios for two reasons. First, the data RAM consumption is usually small for TinyOS applications (≤4 KB) partly because TinyOS was originally designed for Mica series nodes with 4 KB RAM. However, TelosB nodes have 10 KB RAM. Second, the total size of the replaceable components for well-designed applications is usually small (≈2 KB for the GreenOrbs application). If the size of the replaceable code does exceed the available RAM size, we can simply place it on the program flash. In this case, we require a higher voltage that ensures reliable flash writes.

TinyOS’s event-driven model has simplified the design of Elon’s partial reboot mechanism. First, TinyOS kernel does not keep application data. Second, TinyOS does not have blocking I/O operations [Hill et al. 2000; Nightingale et al. 2008]. Therefore, rebooting a node does not require hacking into the TinyOS kernel for preserving application data, cancelling blocking I/O operations, or halting threads. We do need to protect the system jump table to avoid jumping to corrupted memory locations during the reprogramming process.

Compared to complete system reprogramming [Hui and Culler 2004; Panta et al. 2007], Elon limits the reprogrammability to the replaceable component. It suffices for most cases because the application behavior is mainly controlled by the application logic, which can be specified as replaceable. On the other hand, compared to system parameters reconfiguration, we improve the reprogrammability because we allow updates to the native code.

The amount of code update depends on how many functions and variables are specified as replaceable. The replaceable annotation means that the corresponding functions or variables can be frequently changing. There can be nonreplaceable elements in the application component. If the entire application component is specified as replaceable, Elon update the entire application in the current implementation. It is possible to further optimize the performance by updating the actual changed parts by employing incremental reprogramming approaches. However, incremental approaches incur additional complexity in code rebuilding.

Ensuring a safe update to the program of the base version is an important issue that we have not covered thus far. In Elon’s current implementation, we have developed a simple version checking mechanism: it is not allowed to change the set of kernel components and system interfaces. In the future, we would like to develop a declarative language [Cao et al. 2008] for updating programs, which can avoid modifying the source code directly and can protect against occasional errors introduced by programmers.

# 7. CONCLUSION

This article presents a new mechanism called Elon for enabling efficient and long-term reprogramming in wireless sensor networks. Elon reduces the transferred code size significantly by introducing the concept of replaceable component. It avoids the cost of full reboot with a novel partial reboot mechanism. Moreover, it significantly prolongs the reprogrammable lifetime by avoiding flash writes for TelosB nodes. Experimental results show that Elon transfers up to 120–389 times less information than Deluge, and 18–42 times less information than Stream. The partial reboot mechanism that Elon applies reduces the rebooting cost by 50.4%–53.87% in terms of beacon packets, and 56.83% in terms of unsynchronized nodes. In addition, Elon prolongs the reprogrammable lifetime by a factor of 3.3. The overhead of Elon is acceptably small for real-world applications in terms of programmer cost, memory overhead, and execution overhead.

# ACKNOWLEDGMENTS

The authors would like to thank Gong Chen, Chao Huang for their help in Elon’s implementation and evaluation. We thank all members in the GreenOrbs project (http://www.greenorbs.org) for their contributions to this work.

# REFERENCES

Atmel Corporation. AT45DB041B Datasheet.

G. Candea, S. Kawamoto, Y. Fujiki, G. Friedman, and A. Fox. 2004. Microreboot: A technique for cheap recovery. In Proceedings of the USENIX Symposium on Operating Systems Design and Implementation.

Q. Cao, T. Abdelzaher, J. Stankovic, and L. Luo. 2008. Declarative Tracepoints: A programmable and application independent debugging system for wireless sensor networks. In Proceedings of the International Conference on Embedded Networked Sensor Systems.

Y. Chen, O. Gnawali, M. Kazandjieva, P. Levis, and J. Regehr. 2009. Surviving Sensor Network Software Faults. In Proceedings of the ACM Symposium on Operating Systems Principles.

T. Dang, N. Bulusu, W. Chi Feng, and S. Park. 2009. DHV: A code consistency maintenance protocol for multi-hop wireless sensor networks. In Proceedings of the European Conference on Wireless Sensor Networks.

W. Dong, C. Chen, X. Liu, Y. Liu, J. Bu, and K. Zheng. 2011. SenSpire OS: A predicatable, flexible, and efficient operating system for wireless sensor networks. IEEE Trans. Comput. 60, 12, 1788–1801.

A. Dunkels, N. Finne, J. Eriksson, and T. Voigt. 2006. Run-time dynamic linking for reprogramming wireless sensor networks. In Proceedings of the International Conference on Embedded Networked Sensor Systems.

A. Dunkels, B. Gronvall, and T. Voigt. 2004. Contiki: A lightweight and flexible operating system for tiny ¨ networked sensors. In Proceedings of the Workshop on Embedded Networked Sensors.

P. Dutta, J. Taneja, J. Jeong, X. Jiang, and D. Culler. 2008. A building block approach to sensornet systems. In Proceedings of the International Conference on Embedded Networked Sensor Systems.

R. Fonseca, P. Dutta, P. Levis, and I. Stoica. 2008. Quanto: Tracking energy in networked embedded systems. In Proceedings of the USENIX Symposium on Operating Systems Design and Implementation.

O. Gnawali, R. Fonseca, K. Jamieson, D. Moss, and P. Levis. 2009. Collection tree protocol. In Proceedings of the International Conference on Embedded Networked Sensor Systems.

A. Hagedorn, D. Starobinski, and A. Trachtenberg. 2008. Rateless deluge: Over-the-air programming of wireless sensor networks using random linear codes. In Proceedings of the International Symposium on Information Processing in Sensor Networks.

C.-C. Han, R. Kumar, R. Shea, E. Kohler, and M. Srivastava. 2005. A dynamic operating system for sensor nodes. In Proceedings of the International Conference on Mobile Systems, Applications and Services.

T. He, S. Krishnamurthy, J. A. Stankovic, T. A. L. Luo, R. Stoleru, T. Yan, L. Gu, and J. H. B. Krogh. 2004. Energy-efficient surveillance system using wireless sensor networks. In Proceedings of the International Conference on Mobile Systems, Applications and Services.

J. Hill, R. Szewcyk, A. Woo, D. Culler, S. Hollar, and K. Pister. 2000. System architecture directions for networked sensors. In Proceedings of the International Conference on Architectural Support for Programming Languages and Operating Systems.

I.-H. Hou, Y.-E. Tsai, T. F. Abdelzaher, and I. Gupta. 2008. AdapCode: Adaptive network coding for code updates in wireless sensor networks. In Proceedings of the Annual Joint Conference of the IEEE Computer and Communications Societies.

J. Hu, C. J. Xue, and Y. He. 2009. Reprogramming with Minimal Transferred Data on Wireless Sensor Network. In Proceedings of the IEEE Conference on Mobile, Ad Hoc and Sensor Systems.

L. Huang and S. Setia. 2008. CORD: Energy-efficient reliable bulk data dissemination in sensor networks. In Proceedings of the Annual Joint Conference of the IEEE Computer and Communications Societies.

J. W. Hui and D. Culler. 2004. The dynamic behavior of a data dissemination protocol for network programming at scale. In Proceedings of the International Conference on Embedded Networked Sensor Systems.

J. Jeong and D. Culler. 2004. Incremental network programming for wireless sensors. In Proceedings of the IEEE International Conference on Sensor and Ad Hoc Communications and Networks.

B. W. Kernighan and R. Pike. 1984. The Unix Programming Environment. Prentice Hall.

J. Koshy and R. Pandey. 2005a. Remote incremental linking for energy-efficient reprogramming of sensor networks. In Proceedings of the European Conference on Wireless Sensor Networks.

J. Koshy and R. Pandey. 2005b. VM\*: Synthesizing scalable runtime environments for sensor networks. In Proceedings of the International Conference on Embedded Networked Sensor Systems.

S. S. Kulkarni and L. Wang. 2005. MNP: Multihop network reprogramming service for sensor networks. In Proceedings of the IEEE International Conference on Distributed Computing Systems.

A. Lachenmann, P. J. Marron, D. Minder, and K. Rothermel. 2007. Meeting Lifetime Goals with Energy ´ Levels. In Proceedings of the International Conference on Embedded Networked Sensor Systems.

J. R. Levine. 2000. Linkers and Loaders. Morgan Kaufmann.   
P. Levis and D. Culler. 2002. Mate: A tiny virtual machine for sensor networks. In ´ Proceedings of the International Conference on Architectural Support for Programming Languages and Operating Systems.   
P. Levis, N. Patel, D. Culler, and S. Shenker. 2004. Trickle: A self-regulating algorithm for code propagation and maintenance in wireless sensor networks. In Proceedings of the ACM/USENIX Symposium on Networked Systems Design and Implementation.   
K. Lin and P. Levis. 2008. Data discovery and dissemination with DIP. In Proceedings of the International Symposium on Information Processing in Sensor Networks.   
M. Maroti, B. Kusy, G. Simon, and ´ A L´ edeczi. 2004. The flooding time synchronization protocol. In ´ Proceedings of the International Conference on Embedded Networked Sensor Systems.   
P. J. Marron, M. Gauger, A. Lachenmann, D. Minder, O. Saukh, and K. Rothermel. 2006. FlexCup: A flexible ´ and efficient code update mechanism for sensor networks. In Proceedings of the European Conference on Wireless Sensor Networks.   
M. Maroti and J. Sallai. TinyOS TEP133—Packet-level time synchronization.   
L. Mo, Y. He, Y. Liu, J. Zhao, S. Tang, X.-Y. Li, and G. Dai. 2009. Canopy closure estimates with GreenOrbs: Sustainable sensing in the forest. In Proceedings of the International Conference on Embedded Networked Sensor Systems.   
V. Naik, A. Arora, P. Sinha, and H. Zhang. 2005. Sprinkler: A reliable and energy efficient data dissemination service for wireless embedded devices. In Proceedings of the IEEE Real-Time Systems Symposium.   
E. B. Nightingale, K. Veeraraghavan, P. M. Chen, and J. Flinn. 2008. Rethink the sync. ACM Trans. Comput. Syst. 26, 3, 1–26.   
R. K. Panta and S. Bagchi. 2009. Hermes: Fast and energy efficient incremental code updates for wireless sensor networks. In Proceedings of the Annual Joint Conference of the IEEE Computer and Communications Societies.   
R. K. Panta, I. Khalil, and S. Bagchi. 2007. Stream: Low overhead wireless reprogramming for sensor networks. In Proceedings of the Annual Joint Conference of the IEEE Computer and Communications Societies.   
J. Polastre, R. Szewczyk, and D. Culler. 2005. Telos: Enabling ultra-low power wireless research. In Proceedings of the International Symposium on Information Processing in Sensor Networks.   
M. Rossi, N. Bui, G. Zanca, L. Stabellini, R. Crepaldi, and M. Zorzi. 2010. SYNAPSE : Code dissemination in wireless networks using fountain codes. IEEE Trans. Mob. Comput.   
STMicroelectronics Inc. ST M25P80 datasheet.   
R. Szewczyk, A. Mainwaring, J. Polastre, and J. A. D. Culler. 2004. An analysis of a large scale habitat monitoring application. In Proceedings of the International Conference on Embedded Networked Sensor Systems.   
Texas Instruments Inc. MSP430x1xx Family User’s Guide (Rev. F).   
G. Tolle and D. Culler. 2005. Design of an application-cooperative management system for wireless sensor networks. In Proceedings of the European Conference on Wireless Sensor Networks.   
N. Tsiftes, A. Dunkels, and T. Voigt. 2008. Efficient sensor network reprogramming through compression of executable modules. In Proceedings of the IEEE International Conference on Sensor and Ad Hoc Communications and Networks.   
P. Von Richenbash and R. Wattenhofer. 2008. Decoding code on a sensor node. In Proceedings of the IEEE International Conference on Distributed Computing in Sensor Systems.   
Q. Wang, Y. Zhu, and L. Cheng. 2006. Reprogramming wireless sensor networks: Challenges and approaches. IEEE Network Mag. 20, 3, 48–55.   
G. Werner-Allen, K. Lorincz, J. Johnson, J. Lees, and M. Welsh. 2006. Fidelity and yield in a volcano monitoring sensor networks. In Proceedings of the USENIX Symposium on Operating Systems Design and Implementation.

Received November 2011; revised June 2012; accepted October 2012