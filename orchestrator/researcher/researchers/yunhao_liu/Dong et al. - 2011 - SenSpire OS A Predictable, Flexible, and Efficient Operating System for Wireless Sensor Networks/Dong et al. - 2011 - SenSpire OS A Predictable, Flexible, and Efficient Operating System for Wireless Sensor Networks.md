# SenSpire OS: A Predictable, Flexible, and Efficient Operating System for Wireless Sensor Networks

Wei Dong, Student Member, IEEE, Chun Chen, Member, IEEE, Xue Liu, Member, IEEE, Yunhao Liu, Senior Member, IEEE, Jiajun Bu, Member, IEEE, and Kougen Zheng

Abstract—The development of a modern sensor network is difficult because of the long-term unattended operation mode, diverse application requirements, and stringent resource constraints. To address these issues, we present SenSpire OS, a predictable, flexible, and efficient operating system for wireless sensor networks. We improve system predictability by two-phase interrupt servicing and predictable thread synchronization; we achieve system flexibility by providing a hybrid model for both event-driven programming and multithreaded programming; we retain system efficiency by employing stack sharing and modular design. Moreover, we have designed a three-layer networking stack and an object-oriented programming language (CSpire) to enhance system usability and programming convenience. Having implemented SenSpire OS on three most commonly used sensor node platforms, we evaluate its performance extensively. Results show that SenSpire OS ensures predictable system performance, provides a flexible hybrid model for application programming, and is efficient in resource utilization.

Index Terms—Wireless sensor networks, operating systems.

# 1 INTRODUCTION

Alarge number of small-sized, battery-powered sensor nodes that are limited in battery energy, CPU power, and typical Wireless Sensor Network (WSN) consists of a communication capability. Recently, WSN has witnessed an explosive growth in both academia and industry [1], attracting a great deal of research attention in the past few years. WSNs are envisioned to support a variety of applications, including military surveillance, habitat monitoring, and infrastructure protection, etc.

Being simple in terms of hardware, WSN applications are diverse and demanding. The infrastructural support for such applications in the form of operating systems (OS) is becoming increasingly important [2], [3], [4], [5], [6], [7], [8], [9]. The basic functionalities of an OS include resource abstractions for various hardware devices, interrupt management, task scheduling, concurrency control, and networking support. Numerous applications are built on top of the OS. A sensor network OS (hereafter, sensor OS for short) bridges the gap between the hardware simplicity and the application

. W. Dong, C. Chen, J. Bu, and K. Zheng are with the College of Computer Science, Yuquan Campus, Zhejiang University, Zheda Road 38, Hangzhou 310027, China. E-mail: {dongw, chenc, bjj, zkg}@zju.edu.cn.   
. X. Liu is with the School of Computer Science, McGill University, Montreal, Quebec H3A 2A7, Canada. E-mail: xueliu@cs.mcgill.ca.   
. Y. Liu is with the Tsinghua National Laboratory for Information Science and Technology (TNLIST), School of Software, Tsinghua University, and the Department of Computer Science, Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong. E-mail: liu@cse.ust.hk.

Manuscript received 22 Aug. 2009; revised 17 Feb. 2010; accepted 7 Aug. 2010; published online 25 Feb. 2011.

Recommended for acceptance by A. Zomaya.

For information on obtaining reprints of this article, please send e-mail to: tc@computer.org, and reference IEEECS Log Number TC-2009-08-0404.

Digital Object Identifier no. 10.1109/TC.2010.58.

complexity. It plays a central role in providing a flexible environment for building predictable and efficient services.

Over the years, we have seen various OSs emerging in the sensor network community [2], [3], [4], [5], [6], [7], [8], [9]. While they address various challenging issues by adopting different approaches in the design spectrum, two important issues, i.e., predictability assurance and programming flexibility, are still not well addressed.

Predictability. As sensor nodes are usually deployed in inaccessible areas, operating in an unattended manner for a long lifetime, system predictability is highly desirable. The OS should provide mechanisms to ensure the overall system performance. First, the OS should provide a level of separation between the OS and applications, e.g., the OS should remain responsive irrespective of the application behaviors. Second, the OS should provide a level of separation between different tasks, e.g., a critical task should not be blocked indefinitely by noncritical tasks or locks hold by a group of tasks.

Flexibility. Since WSN applications have diverse requirements, system flexibility to facilitate application programming is desirable. The OS should provide many choices to meet requirements of specific application scenarios and programmers’ preference. A hybrid model combining both event-driven programming and multithreaded programming is highly preferred. Specific challenges should be addressed to design a hybrid system while retaining predictability and efficiency at the same time.

Sensor nodes are usually equipped with low-power microcontrollers with stringent resource constraints. The OS should optimize CPU utilization and memory consumption for high efficiency. Moreover, as sensor nodes are usually deployed in hostile environment in a large scale, the OS should also support efficient network reprogramming [10] to allow updating the WSN software.

In this paper, we present the design principles of a new sensor OS, SenSpire OS, to address the above-mentioned issues in a systematic manner. First, SenSpire OS achieves system predictability by two-phase interrupt servicing, priority-based preemptive scheduling, and predictable thread synchronization. Second, SenSpire OS supports a flexible programming model that combines the benefits of both event-driven programming and multithreaded programming. Compared to existing approaches, the hybrid system of SenSpire OS is more flexible, and, at the same time ensures system predictability and efficiency. Third, SenSpire OS achieves system efficiency by employing stack sharing and static optimizations. Recently, SenSpire OS also supports an optimized dynamic loadable module format [11] for achieving energy efficiency when network reprogramming is performed.

The contributions of this work are highlighted as follows.

First, we introduce two-phase interrupt servicing and the priority ceiling protocol into the design of a sensor OS, and have illustrated that they are important for ensuring system predictability.

Second, SenSpire OS natively supports the hybrid model in the kernel scheduler, which advances the state-of-the-art hybrid models in three aspects. First, SenSpire OS allows decoupling of two subsystems (i.e., event-driven and multithreaded), hence is flexible in expressing and customizing different scheduling policies. Second, SenSpire OS supports event preemption, which is important for achieving system predictability in the event-driven subsystem. Third, Sen-Spire OS employs a novel differentiated kernel scheduling scheme to exploit stack sharing, hence can reduce the stack memory consumption.

Third, we have implemented SenSpire OS on three commonly used sensor node platforms, i.e., Mica2, MicaZ, and TelosB, with a small footprint. Moreover, we have designed an optimized dynamic loadable module format for network reprogramming. The proposed SELF module file format [11] is more flexible than MELF (which is for SOS [4]); and, it is much smaller than CELF [12] (which is for Contiki OS [3]).

Finally, we evaluate SenSpire OS’s performance extensively. We have also conducted quantitative comparisons with other representative sensor OSs to show our design advantages.

The rest of this paper is organized as follows: Section 2 presents the design of SenSpire OS. We describe the design principles from the perspective of system predictability (Section 2.1), flexibility (Section 2.2), efficiency (Section 2.3) as well as the networking abstraction (Section 2.4), and the programming language (Section 2.5). Section 3 introduces the implementation of SenSpire OS. Section 4 shows the evaluation results. Section 5 discusses related work. Finally, we conclude this paper and give future directions of work in Section 6.

# 2 DESIGN

This section presents the design of SenSpire OS. Fig. 1 gives an overview of SenSpire OS’s design principles.

Section 2.1 describes the two-phase interrupt servicing scheme and predictable thread synchronization primitives for achieving system predictability. Section 2.2 details the hybrid system design which provides a flexible model for both event-driven programming and multithreaded programming. Section 2.3 describes the stack sharing technique and the modular design approach for achieving system efficiency. In addition, to facilitate programming distributed sensor network applications, we have also designed a networking stack and a programming language called CSpire. Section 2.4 introduces the networking abstraction and Section 2.5 describes the CSpire language for application programming based on SenSpire OS.

![](images/7d88ad3b603ee3aac566197e1f9faf8aa11b46a77f4a762ff5b6aa0f27dd93be.jpg)



Fig. 1. An overview of SenSpire OS’s design principles.

# 2.1 Approaches for Predictability

Interrupt handling is very important for tiny embedded systems like sensor nodes [13]. Existing sensor OSs usually take a single-phase interrupt servicing scheme. For example, in TinyOS [2], interrupts are serviced by asynchronous code that is reachable from (i.e., called from) one Interrupt Service Routine (ISR) [14]. While the OS kernel disables the interrupts only for brief periods of time, it cannot prevent the applications from disabling interrupts, because this is the only possible way of synchronization between tasks (i.e., synchronous code in TinyOS) and interrupts (i.e., asynchronous code in TinyOS) [15]. Hence the interrupt latency can never be bounded without knowing application behaviors. SenSpire OS adopts a two-phase interrupt servicing scheme, so that the worst-case interrupt latency can be guaranteed.

Thread synchronization is an important issue in preemptive systems [16]. The design and implementation of synchronization primitives, however, are overlooked in existing sensor OSs, such as Contiki OS [3], Mantis OS [5]. Without a careful design, the synchronization of threads can lead to an indefinite period of priority inversion, during which a high priority thread waits indefinitely for the completion of low priority threads [16]. In order to address this issue, SenSpire OS adopts the priority ceiling protocol [16] to avoid unpredictable priority inversion and the formation of deadlocks.

# 2.1.1 Two-Phase Interrupt Servicing

We split interrupt servicing in SenSpire OS into two phases, i.e., the top half and the bottom half. The top half executes at interrupt time and is meant to be short enough to complete all necessary actions at the time of the interrupt. It performs sensitive and critical tasks with all interrupts disabled. In contrast, the bottom half can be deferred to a more suitable point in time to complete servicing of a prior interrupt. It allows top halves to preempt its execution by enabling interrupts.

![](images/072df0edd0439905d5639f09fa0de2e4ded796d4f69ebe1a665f0c30acbd16c7.jpg)



(a)

![](images/bb1753e32e355108a460587b43d02a7411b899f30727847d33105e7b747f308f.jpg)



(b)   
Fig. 2. The SenseTask application in TinyOS versus in SenSpire OS. (a) TinyOS. (b) SenSpire OS.

Fig. 2 shows the code snippets for the SenseTask application for both TinyOS-1.x and SenSpire OS (hereafter, we will use T1 to refer to TinyOS-1.x and T2 to refer to TinyOS-2.x when different TinyOS versions matter).

The code for SenSpire OS is written in CSpire, which will be introduced in Section 2.5. In CSpire, the bh keyword is used to indicate a bottom half while the task keyword is used to indicate a run-to-completion task (a run-to-completion task cannot block or self-suspend, e.g., TinyOS tasks are run-tocompletion). In the code for T1, the atomic keyword is used to protect the shared data by disabling global interrupts. Hence, within the atomic section, the OS is not responsive to any other interrupts. In contrast, in the code for SenSpire OS, the ADC completion event is notified in the context of a bottom half, and the critical primitive is used to protect the shared data. The critical primitive differs from the atomic primitive in that it only defers the execution of bottom halves. Hence top halves can still be serviced immediately once interrupts trigger. Note that the critical primitive is used to protect shared data between tasks and bottom halves. To protect shared data between bottom halves and top halves, we should use the atomic keyword (which disables all interrupts) instead. In this case, top halves cannot interrupt the execution of bottom halves. Interrupt latency depends on the length of time top halves execute and the rate of interrupts. In TinyOS, the interrupt latency also depends on the atomic section length because the atomic keyword disables all interrupts from execution. As the atomic keyword is exposed to application programmers, the application code does affect the interrupt latency. On the other hand, in SenSpire OS, the critical keyword disables bottom halves (but not top halves) and top halves can always be serviced irrespective of the critical section size. Hence, SenSpire OS achieves a more predictable interrupt latency.

# 2.1.2 Predictive Thread Synchronization

A number of recent sensor OSs [5], [6], [8], [17] support preemptive threading to ensure predictable system performance. Synchronization primitives are important to serialize the access to shared resources. The design and implementation of existing synchronization mechanisms are overlooked in prior preemptive threaded sensor OSs. In fact, a direct application of traditional synchronization primitives can lead to an indefinite period of priority inversion and a low level of schedulability [16].

![](images/8b9bc4b41d9cdcd2912063d5037164cdad4e8ce0647426d8a57a7f0cfd611591.jpg)



Fig. 3. Example of unpredictable periods of priority inversion.

We consider a similar example in [16] (shown in Fig. 3). $\tau _ { 1 } , \tau _ { 2 } ,$ and $\tau _ { 3 }$ are three threads arranged in descending order of priority with $\tau _ { 1 }$ having the highest priority. $\tau _ { 1 }$ and $\tau _ { 3 }$ share a data structure protected by a mutex. At time $t _ { 1 } ,$ -3 starts execution. At time $t _ { 2 } , \tau _ { 3 }$ locks the mutex and executes its critical section. During the execution of $\tau _ { 3 } ^ { \prime } \mathbf { s }$ critical section, $\tau _ { 1 }$ preempts $\tau _ { 3 }$ at time $t _ { 3 } .$ At time $t _ { 4 } , \tau _ { 1 }$ attempts to use the shared data. However, it blocks on the mutex hold by $\tau _ { 3 } .$ . At the same time, $\tau _ { 2 }$ starts execution till time $t _ { 5 } .$ In this example, we would expect that $\tau _ { 1 , }$ , being the highest priority thread, will be blocked no longer than the time for $\tau _ { 3 }$ to complete its execution in the critical section, i.e., $( t _ { 6 } - t _ { 5 } )$ . However, the duration of blocking is, in fact, $( t _ { 6 } - t _ { 5 } ) + ( t _ { 5 } - t _ { 4 } ) _ { . }$ , which is unpredictable because the execution time of $\tau _ { 2 } ( = t _ { 5 } - t _ { 4 } )$ and any other pending intermediate threads can be sufficiently long.

SenSpire OS hence adopts the priority ceiling protocol [16] to address this issue. It works as follows:

In SenSpire OS, each thread has a static priority and a dynamic priority.   
Each shared resource has a static priority ceiling, which equals to the highest static priority of the thread that uses it. Thanks to the CSpire language, we are able to obtain the priority ceiling by program code analysis.   
The dynamic priority of a thread equals the maximum of its static priority and priority ceiling of the shared resource it currently uses.   
A ready thread can preempt the current thread only when its static priority is higher than the dynamic priority of the current thread.

It is formally proved in [16] that the priority ceiling protocol reduces the worst-case blocking time to at most the duration of execution of a single critical section of a lower priority thread. In addition, it prevents the formation of deadlocks. In the example shown in Fig. 3, if the priority ceiling protocol is used, at time $t _ { 4 } , \tau _ { 3 }$ will continue because it has a higher dynamic priority than ${ \tau _ { 2 } } ^ { \prime } \mathbf { s }$ static priority.

# 2.2 Approaches for Flexibility

The debate between threads and events is a very old one [18], [19]. Event-driven systems have the benefits of high system responsiveness, high performance, and low resource consumption. On the other hand, multithreaded systems have the benefits of expressiveness and ease of use, e.g., application programmers can reason about the series of actions taken by a thread in the familiar way, leading to a natural programming style in which the control flow for a single thread is apparent [20].

As a hybrid model combines both event-driven programming and multithreaded programming, we therefore favor it to meet diverse application requirements. With a hybrid model, it means that the application programmer could design parts of the application using threads, where threads are the appropriate abstraction, and parts of the system using events, where they are more suitable [20]. It is flexible and gives the best of two worlds: the expressiveness of threads and customizability of events. While there exist a number of prior works on the design of hybrid models, SenSpire OS’s integral design goals distinguish its hybrid system design from existing works. The hybrid model of SenSpire OS has the following features.

Flexibility and customizability. Existing hybrid approaches, based on legacy codebase, make tight coupling of two subsystems, e.g., event-biased approaches require the existence of the event-driven subsystem while threadbiased approaches require the existence of multithreaded subsystem. By natively supporting hybrid scheduling in the kernel scheduler, SenSpire OS allows decoupling of two subsystems, hence is more flexible in expressing and customizing different scheduling policies.

Predictability and real-time performance. Existing approaches such as Protothreads [21], TinyThreads [22], do not support priority preemption. Other approaches, such as TinyMOS [23], only provide a limited number of priorities (e.g., limited to five in TinyMOS [5], [23]). SenSpire OS advances prior work by supporting programmer-assigned priority-based preemption, thus natively supporting longrunning computations without degrading system performance. Moreover, SenSpire OS supports event preemption, which is important to achieve predictability in the eventdriven subsystem. In addition, SenSpire OS employs the priority ceiling protocol to achieve predictable thread synchronization (Section 2.1).

Memory efficiency. Existing hybrid systems, such as TOSThreads [24], TinyMOS [23], based on legacy codebase, preclude aggressive resource optimizations in the implementation. In contrast, by natively supporting hybrid scheduling in the kernel scheduler, SenSpire OS is able to exploit stack sharing in order to reduce the stack memory consumption.

# 2.2.1 Hybrid System

Fig. 4 gives an overview of SenSpire OS’s hybrid system. In SenSpire OS, we classify tasks in two forms: event handler task (event for short) and thread task (thread for short). Events are handled by the event-driven subsystem and threads are handled by the multithreaded subsystem. Events are scheduled by Event Schedulers (ESs) which in turn are scheduled by the Kernel Scheduler (KS). SenSpire OS’s event-driven subsystem is different from TinyOS, in that we can support multiple preemption levels by the use of multiple ESs. Events in different ESs can preempt one another. In contrast, the TinyOS core has only one preemption level within the task context. Some critical system events (e.g., packet reception) are executed in the task context, sharing the same context as other noncritical tasks (e.g., compression). Therefore, a critical task can be interfered by the execution of other noncritical tasks ahead of it. The multithreaded subsystem consists of multiple threads which are directly scheduled by our KS along with ESs. It is different from Mantis OS, in that we do not employ time-sliced scheduling, instead, preemption occurs when a high priority thread (or ES) is ready or when the currently running thread calls a blocking I/O or gives up its CPU cycles voluntarily by calling sleep() or yield(). Hence the number of context switches can be reduced. In SenSpire OS, the event-driven subsystem takes a higher priority than the multithreaded subsystem because it is more suitable for time-sensitive operations.

![](images/e57a7f3843c35294fbad53c9d9c988a4a7ec7f8ac67e7ed10b95a82852cb0795.jpg)



Fig. 4. SenSpire OS’s hybrid system.

We have introduced the design of SenSpire OS’s thread synchronization primitives in Section 2.1.2. In the following section, we will describe SenSpire OS’s novel differentiated kernel scheduling scheme which implements the hybrid model while reduces memory consumption by stack sharing at the same time.

# 2.2.2 Differentiated Kernel Scheduling

SenSpire OS’s KS differentiates three execution contexts, i.e., ES, the primary thread (i.e., the system startup context, denoted as -0), and nonprimary threads (denoted as $\tau _ { 1 . . . n } )$ . As each ES represents a nonblocking context, they can share a common stack with one of the blocking context. In SenSpire OS, all ESs share a common stack with the primary thread. SenSpire OS’s stack sharing technique is inspired by TinyOS fibers [25], in which a system stack is shared between events and one thread. SenSpire OS extends it by supporting preemptive events and multiple threads. We will further discuss the issue of stack sharing in Section 2.3.1.

Context switches between ESs or between ES and the primary thread do not involve stack switching. Stack switching is only required when switching between threads or between ES and nonprimary threads. Note that we still need to switch the register files. Table 1 shows the actions taken by the KS.

Note that, events, being run-to-completion, are not allowed to block. This means that events cannot block on synchronization primitives such as mutexes. In order to achieve synchronization between events of different priorities, or events and threads, we need to manually check for the resource availability in the event, and need to repost the event if the resource is unavailable at the current time.

TABLE 1 Differentiated Kernel Scheduling 

<table><tr><td>current context</td><td>target context</td><td>switch registers</td><td>switch stacks</td></tr><tr><td>ES</td><td>ES</td><td>√</td><td>✗</td></tr><tr><td>ES</td><td> $\tau_0$ </td><td>√</td><td>✗</td></tr><tr><td>ES</td><td> $\tau_{1...n}$ </td><td>√</td><td>√</td></tr><tr><td> $\tau_0$ </td><td>ES</td><td>√</td><td>✗</td></tr><tr><td> $\tau_0$ </td><td> $\tau_{1...n}$ </td><td>√</td><td>√</td></tr><tr><td> $\tau_{1...n}$ </td><td> $\tau_{1...n}$ </td><td>√</td><td>√</td></tr><tr><td> $\tau_{1...n}$ </td><td> $\tau_0$ </td><td>√</td><td>√</td></tr><tr><td> $\tau_{1...n}$ </td><td>ES</td><td>√</td><td>√</td></tr></table>

means the KS takes the action when scheduling.  means the KS does not take the action when scheduling.

The KS employs preemptive scheduling in accordance with the priorities of ESs and threads. The priorities of ESs must be different while the priorities of threads can be the same. Within the same priority, the KS schedules threads in an FIFO manner. Each ES uses a nonpreemptive scheduling scheme. Within each ES, events share a common execution context and are scheduled by a certain nonpreemptive policy (e.g., FIFO, or nonpreemptive priority based). Hence, to execute an event, two levels of scheduling are involved: first, the KS schedules the corresponding ES (which the event is assigned to), then the ES schedules the event to run.

The scheduling system can be viewed as a hierarchy of execution contexts [26]. As shown in Fig. 5, the Kernel Scheduler schedules two ESs and two threads in a prioritypreemption manner. The ES-NPPS has the highest priority. Thus any event assigned to it can preempt other tasks. The scheduling policy is Non-Preemptive Priority Scheduling (NPPS). The ES-FIFO has an intermediate priority. Any event assigned to it can preempt threads, but not events assigned to ES-NPPS. It schedules events assigned to it in an FIFO manner. Two threads have the same lowest priority and can be preempted by any events in the system. They are scheduled by our KS in an FIFO manner.

# 2.2.3 Comparison with Prior Work

Fig. 6 compares SenSpire OS’s hybrid model with prior works in the sensor network community. In this figure, x-axis represents the thread phase while the y-axis represents the event phase. Early OSs, such as TinyOS (also SOS, Contiki OS core), only support nonpreemptive events. Protothreads [21], built on Contiki OS, supports thread-like

![](images/77095ea3957c479e40d3063aa6fac55d3876d1fd8e4d8ee845b65469d8d21074.jpg)



Fig. 5. An example scheduling hierarchy.

![](images/0fb261db4aa187ad39d4b5884657a06551d73576eec578bc7dbaec98aec1463a.jpg)



Fig. 6. Comparison of existing hybrid systems.

programming. However, it does not maintain threadindependent data, and does not allow preemption. TinyOS fibers [25], built on TinyOS, only supports one thread. TinyThreads [22], also built on TinyOS, implements a cooperative thread mechanism. In the cooperative thread model, a thread must explicitly yield the CPU to other runnable threads. The problem with cooperative threads is the correctness of the system depends on application code voluntarily yielding the CPU at specific intervals. If a thread does not relinquish the CPU for a long time, then other threads may be unable to make progress [24]. The same issue exists for event-driven systems. Therefore, TinyOS Preemptive Level Scheduler (PL) [27] supports preemptive events based on TinyOS, but it does not support thread-like programming. The Contiki preemptive library [3], and TOSThreads [24], support true preemptive multithreading on event-driven kernels; TinyMOS [23] supports events in a multithreaded kernel (Mantis OS). SenSpire OS advances these three works in three aspects. First, SenSpire OS supports preemption in both event-driven subsystem and multithreaded subsystem. Event preemption is important for ensuring system predictability in the event-driven subsystem. Second, SenSpire OS supports customizing different scheduling policies with the help of the CSpire language compiler (which will be further discussed in Section 4.5). Third, by directly supporting hybrid scheduling in the kernel scheduler, SenSpire OS is able to employ stack sharing for optimizing resource utilization (see Section 2.3.1).

# 2.3 Approaches for Efficiency

The design and implementation of a sensor OS should meet the resource constraints of sensor nodes. In most components of SenSpire OS, we adopt cost-effective design approaches (as opposed to approaches for traditional OSs). In particular, we employ stack sharing to reduce stack memory consumption in our scheduler design. In addition, the modular extension of SenSpire OS enables energy-efficient network reprogramming. We will introduce the stack sharing technique and the modular design approach in the following two sections, respectively.

# 2.3.1 Stack Sharing

The shared stack model not only can be applied to nonpreemptive systems, but also preemptive systems where tasks have run-to-completion semantics and do not suspend themselves [28].

In order to see why stack sharing can be applied to our hybrid system, we analyze the following conditions. First, all ESs can share a common stack because their execution is noninterleaved, i.e., if ESj begins execution between the start and finish of ESi (to make it possible, ESj must have a higher priority), then ESi is not allowed to resume execution until ESj has finished. Second, all ESs can share a common stack with one of the threads (primary thread). This is because each ES’s execution cannot be preempted by threads (as ES’s priority is higher than threads), and, once some ES preempts the execution of the primary thread, it must run to completion before the primary thread can be resumed.

In order to see the benefits our differentiated kernel scheduling (Section 2.2.2), we analyze the stack consumption of the scheduling hierarchy shown in Fig. 5 for prior approaches (without stack sharing) and SenSpire OS’s approach (with stack sharing). Without stack sharing, this scheduling hierarchy will occupy the following four stacks.

1. Stack for ES-NPPS; all tasks within ES-NPPS are nonpreemptive, hence share this common stack.   
2. Stack for ES-FIFO; all tasks within ES-FIFO are nonpreemptive, hence share this common stack.   
3. Stack for thread1 (the primary thread).   
4. Stack for thread2.

This is a relative costly scheme for implementing the hybrid model on resource constrained sensor nodes. In SenSpire OS, a common system stack is shared among ESs and the primary thread. Considering an additional stack for thread2, the system consumes two stacks, reducing two stacks compared to prior approaches.

# 2.3.2 Modular Design

Recently, SenSpire OS supports dynamic loadable modules to enable energy-efficient network reprogramming [11]. Early OSs, such as TinyOS, require full image replacement to reprogram a network of sensors [29]. This incurs a large amount of transmission overhead during code dissemination, which significantly impacts energy efficiency and the lifetime of a sensor network. A few differential-based approaches are designed for TinyOS [30]. The problem therein is that they require the program layout to be exactly the same on all sensor nodes. If sensor nodes are running different versions of their software, differential-based approaches do not scale [12]. SenSpire OS supports loadable modules. It uses an optimized module file format, SELF, for dissemination. The SELF loader within the OS is responsible for loading and executing a new module. Compared to existing modular OSs, such as SOS [4] and Contiki OS [3], [12], SenSpire OS’s modular design has two major advantages.

First, compared to Contiki’s CELF, SELF is even smaller. CELF only redefines long data types to short ones (e.g., from 32 bits to 16 bits, or 16 bits to 8 bits), hence still leads to a large amount of metadata overhead. SenSpire OS optimizes the module file format much further. For example, with the chained reference technique [11], [31], it reduces the number of relocation entries to the number of unique references, instead of the total number of references; with a system call jump table, it is able to prelink system calls to fixed addresses in the jump table slots. This prelinking technique significantly reduces the overhead of kernel symbols and their string representations.

Second, compared to SOS’s MELF, SELF is more flexible. MELF, being small in size, has several limitations. First, it uses Position Independent Code (PIC). Not all CPU architectures support PIC and even when supported, programs compiled to PIC typically are subject to size restrictions, e.g., 4 KB for the AVR microcontroller. SenSpire OS does not have this limitation by using relocatable code. Second, SOS module does not allow to define global variables because data relocation is not performed. SenSpire OS does not have this limitation.

# 2.4 Networking Abstraction

We have designed and implemented a three-layer networking stack to facilitate programming distributed sensor applications based on SenSpire OS. Different layers abstract different functionalities by different classes of WSN developers. 1) The radio layer provided by device driver developers. It implements device specific MAC protocols. 2) The unified resource layer provided by OS kernel developers. It virtualizes the radio hardware, scheduling concurrent requests [32]. On top of it, different applications can use the hardware radio without interfering each other. 3) The sensornet layer provided by network service developers. It implements neighborhood management and link estimations, which can be shared among different upper-layer networking routing protocols [33], [34].

# 2.5 Programming Language

We have developed a programming language, CSpire, for application programming based on SenSpire OS. CSpire partially supports object-oriented programming while tightly integrates with the OS kernel for compile-time verifications, optimizations, and customizations. We summarize CSpire’s features as follows:

Encapsulation. CSpire forces the application code be encapsulated in classes.   
Function polymorphism. CSpire allows a common name to be shared among multiple functions as long as their signatures are different. Note that CSpire does not allow dynamic polymorphism as it will incur a large runtime overhead.   
Object manipulation. CSpire supports invoking methods of an object. However, CSpire does not manage object lifetime.   
Support for the hybrid model. CSpire supports the keywords of task, thread, bh, etc., to simply programming on top of SenSpire OS’s hybrid model.   
Annotations. CSpire supports specifying annotations to objects, e.g., task[period=1000] denotes a periodic task with a one second period.   
Compile-time verification. CSpire verifies whether the application code conforms to the requirements of SenSpire OS. For example, blocking is not allowed in events (or bottom halves).   
Compile-time optimization and customization. CSpire is able to analyze application resource requirements and customize the OS kernel. Currently, CSpire supports for customization of the

![](images/e8e80becbc1b76ac6b839039c850bd17792e40cd51e4da4a8339d1e833a12274.jpg)



Fig. 7. SenSpire OS design overview.

scheduling hierarchy, e.g., the multithreaded system can be excluded if the application never uses. CSpire also supports stack size estimation by differentiating different execution contexts and analyzing at the assembly level.

# 3 IMPLEMENTATION

We have implemented SenSpire OS on three commonly deployed sensor node platforms—Mica2, MicaZ, and TelosB.

The SenSpire OS kernel is written in C. As shown in Fig. 7, The SenSpire OS mainly consists of the following components:

Hardware drivers. They are further classified into onchip device drivers (such as hardware timers, UART, and ADC) and off-chip device drivers (such as MTS300/MTS310 sensorboards, Chipcon CC1000/ CC2420 radios). We port parts of this code from SOS [4] and Mantis OS [5].   
Interrupt system. It contains the two-phase interrupt handling code.   
Task scheduling system. It implements the differentiated kernel scheduling algorithm and a set of synchronization primitives.   
Module manager. It extends SenSpire OS for handling modules. It is responsible for module placement, loading, and execution.   
Network protocols. They include the sensornet layer and illustrative network routing protocols such as the tree routing protocol [35].   
Programming environment. Applications based on SenSpire OS are written in CSpire, we expose SenSpire OS kernel services to application programmers via the CSpire native classes which are thin wrappers around their C implementations. We implement the CSpire compiler with JavaCC. It compiles user applications together with SenSpire OS native classes into C. Then it invokes the corresponding C cross-compiler (e.g., avr-gcc or msp-gcc) to compile the converted C code into the binary code.

The kernel scheduler is the core of SenSpire OS. The SenSpire OS kernel scheduler maintains a priority queue. As shown in Fig. 8, the kernel scheduler fetches the highest priority task from the queue. If there is no task in the queue, the kernel scheduler puts the CPU into the sleep state to save energy. Otherwise the kernel scheduler switches the register files. After that, the kernel scheduler switches the stack only when necessary (according to Table 1).

![](images/856e7970f9fa3b9c3125928b2d7117c1de784e71c71db5b423aa471e68071609.jpg)



Fig. 8. Pseudocode for the kernel scheduler.

# 4 EVALUATION

In this section, we evaluate the performance of SenSpire OS. Section 4.1 evaluates how SenSpire OS’s two-phase interrupt servicing scheme ensures a predictable interrupt latency. Section 4.2 examines the latency of bottom halves. Section 4.3 shows how SenSpire OS’s hybrid model provides a flexible environment to facilitate application programming. Section 4.4 illustrates how SenSpire OS’s preemptive kernel scheduling ensures system predictability and responsiveness in the face of long-running tasks. Section 4.5 shows that SenSpire OS’s scheduling hierarchy is flexible in customizing different scheduling policies. Section 4.6 evaluates the scheduler overhead. Section 4.7 evaluates the overall system efficiency, and finally, Section 4.8 examines how SenSpire OS’s modular design improves the reprogramming efficiency.

# 4.1 Interrupt Latency

We evaluate the interrupt latency for both TinyOS and SenSpire OS via a benchmark we called SenseRfm. It reads the ADC value every 50 ms while at the same time listens to the radio for incoming packets. In SenSpire OS, we write one benchmark with the bottom half mechanism and the other without the bottom half mechanism which is used to simulate the behaviors of T1. We have carried out evaluations for Mica2 using Avrora [36]. We have modified Avrora in order to gather the SPI interrupt latency distribution.

In this experiment, we would like to see how the SPI interrupt latency varies with the increase of critical sections in the processData task (see Fig. 2). As we have already shown, the critical section in T1 is enclosed in atomic{...} while the critical section in SenSpire OS is enclosed in critical{...}.

We vary the critical section in SenseRfm by increasing log2size (a constant in SenseRfm that controls the critical section size) from four to six. The corresponding clock cycles of the critical section varies from 80 to 500 cycles. We gather the SPI interrupt latency distribution (note that, the SPI interrupt will come at every 418 s on Mica2) and Figs. 9a, 9b, and 9c show the cumulative distribution function (CDF) of the SPI interrupt latency. The line marked “SenSpire OS” represents SenSpire OS with the bottom-half mechanism and the line marked “SenSpire-TOS” represents SenSpire OS without the bottom-half mechanism (which is used to simulate the behaviors of T1). As we can see from Figs. 9a, 9b, and 9c, the SPI interrupt latency in SenSpire OS has a much smaller worst-case latency than that of T1 and SenSpire-TOS. In addition, the worst-case interrupt latency for both T1 and SenSpire-TOS increases when the critical section increases. In contrast, SenSpire OS has a quite predictable interrupt latency distribution in all three cases. Such predictability is essential to achieve accurate time synchronization in sensor networks, as pointed out in [37]. By reducing interrupt latency from hundreds of s to a few s, we can improve the synchronization accuracy significantly.

![](images/872b49ee9b555f81f33c1bbd90e6bf38891edefe425f5a99a67536893cc7b3ab.jpg)



(a)

![](images/997f5b026caa083d5171599f5871ee6dc229bdf56e01f0e6297f8fb7937effb0.jpg)



(b)

![](images/c4fb7f3f7177cd4d1c61a016597f8dd939f2842d82c0ccb4f34e701d90622588.jpg)



（c）  
Fig. 9. SPI interrupt latency distribution. (a) log2size=4. (b) log2size=5. (c) log2size=6.

# 4.2 Bottom Half Latency

SenSpire OS’s predictable interrupt latency is achieved at the cost of putting deferrable interrupt handling code into the bottom half (e.g., in the SenseRfm benchmark for SenSpire OS, we put the ADC handling code in the bottom half). In this experiment, we would like to see how deferrable bottom halves can be under normal conditions (i.e., without considering interrupt nesting). We profile the ADC bottom half latency in the SenseRfm benchmark and compare it with the latencies of notification events in both T1 and T2. The results are depicted in Fig. 10.

As we can see from Fig. 10 that the ADC event notification latency of T1 is the smallest as it is in the interrupt execution environment (prefixed with the async keyword). T2 places the event notification in the task execution environment (without the async keyword and defaults to sync). The event notification latency is much larger, of which 103 clock cycles [38] are overheads of posting and executing a task. Bottom half latency in SenSpire OS is larger than T1 but smaller than T2.

![](images/ebffcc8726688bf54d82f173b94953f4dd4331a25fcc34ea4bd6b09087117567.jpg)



Fig. 10. Bottom half latency in SenSpire OS versus event notification latency in TinyOS.

As we can see from this experiment, top-half handler is suitable to place highly responsive code; task environment, on the other hand, has a relative higher response latency, especially when there are multiple tasks pending; bottomhalf handler provides a good place to handle slightly deferrable part of interrupt handling and is normally more responsive and predictable than a task.

# 4.3 Application Programming

SenSpire OS’s hybrid system design provides application programmers a flexible programming environment that supports both event-driven programming and multithreaded programming. Combined with the CSpire language, it facilitates application programming based on SenSpire OS.

Fig. 11 shows a typical sensor network application that illustrates the hybrid model can facilitate programming distributed sensor network applications. In this example, each sensor node samples the light sensor at an interval of one second. Every one hour, the sensor node transmits the last compressed data item to a sink node. After that, the sensor node starts compressing the current data (for sending out in the next working duration). The data compression logic is better expressed by a thread in which there may be many local variables. A thread can be preempted and it automatically preserves the values of these variables when it resumes. Event-based approach needs manual efforts in preserving state values during computation. When the node compresses the data, it still needs to responsive to radio events, e.g., it is still required to forward data for other nodes. In this case, using events for handling data forwarding is natural. If purely threading system were used, we must start a separate thread blocking on the radio event. If the number of events increases, the multithreaded approach does not scale.

```txt
import Led, Task, Timer, Sensor, Radio;

class SenseCompressionRfm {
    uint8_t data[BUFFER_SIZE];
    uint8_t compressedData[BUFFER_SIZE];
    uint8_t pkt[PKT_SIZE];

    void start() {
    Radio.begin_read(pkt, PKT_SIZE, radio_readDone)
    post timer_task;
    }
    task[@period=1000] timer_task() {
    Sensor.Light.begin_read(light_readDone);
    if (counter == 3600) {
    radio.begin_write(DEST_ADDR,
    /* lastCompressionBlock */);
    compression_thread.start();
    }
    }
    task light_readDone() {
    /* put the readings to data */
    }

    thread compression_thread() {
    /* compress the data */
    }
    task radio_readDone() {
    /* forward the packet for others */
    }
} 
```  
Fig. 11. Application programming based on SenSpire OS’s hybrid model.

![](images/76731536b2ef9334301c0dde6b4c425c1d418e89a702644530c0d7eccaaa8acb.jpg)



Fig. 12. Normalized throughput varied with computation time.

# 4.4 Advantages of Preemption

In the example shown in Fig. 11, SenSpire OS allows preemption so that during long-time compression, the system is still able to handle the radio events so that the data delivery performance of the network does not degrade.

In order to see how preemption ensures system performance, we proceed to perform an experiment in which one node (node A) reports data to a sink (node B) at a frequency of 50 Hz. Node A starts a long-time computing task at a frequency of 4 Hz. We would like to see how the computation time affects network throughput.

Fig. 12 shows the normalized throughput for the applications based on TinyOS and SenSpire OS. We can see that with the increase in computation time, the throughput decreases in TinyOS. With priority preemption, SenSpire OS is able to ensure network throughput irrespective of the computation time.

# 4.5 Customizability

SenSpire OS supports customizing its scheduling hierarchy for implementing different scheduling policies. We extend the work in [39] by a better support for multithreading. Fig. 13 shows the scheduling hierarchy for TinyOS [2], Mantis OS [5], SOS [4], and TinyOS Preemptive Level Scheduler [27], respectively. In TinyOS, the KS only schedules one FIFO-ES. In Mantis OS, the KS schedules threads of five priority levels. In SOS, the KS also schedules one ES. However, the ES schedules events of three priority levels in a nonpreemptive manner. In TinyOS Preemptive Level Scheduler, the KS schedules ESs of three preemptive priority levels. The intermediate priority ES supports three nonpreemptive priority levels. As we can see from the figure, SenSpire OS’s hybrid system is flexible in expressing and customizing different scheduling policies in existing sensor OSs.

![](images/4f82fcdad7ca0e5f08299f25e014a74c4315c03855c478ddc4749961c919e49c.jpg)  
Fig. 13. Customizability of SenSpire OS’s scheduling hierarchy. (a) TinyOS [2]. (b) Mantis OS [5]. (c) SOS [4]. (d) TinyOS preemptive level scheduler [27].

TABLE 2 Overhead of Starting a Task (in Clock Cycles) 

<table><tr><td>Operations</td><td>T1</td><td>Mantis</td><td>SenSpire</td></tr><tr><td>Posting an event task</td><td>42</td><td>N/A</td><td>90</td></tr><tr><td>Creating a thread task</td><td>N/A</td><td>2481</td><td>769</td></tr></table>

# 4.6 Scheduler Overhead

We next examine the scheduler overhead of SenSpire OS’s hybrid system. The scheduler imposes three kinds of overhead. The first is the cost of starting a task (posting an event task or creating a thread task in our case). The second is the cost of executing (or scheduling) a task. The third is the cost of checking that the task queue is empty and going back to sleep (this has to be done after every interrupt).

1. Overhead of starting a task. For an event task, starting a task is to post a task; for a thread task, starting a task is to create a task. We measure the clock cycles of each operation and the results are reported in Table 2. The post operation of T1 is 42 cycles while SenSpire OS has 90 cycles. The extra overhead lies in the fact that we make scheduling decisions in our post operation while TinyOS does not need to as priority preemption is not supported. When just the post operation is measured, SenSpire OS takes about 44 cycles which is very close to that of T1. Thread creation in SenSpire OS consumes 769 cycles, as opposed to 2,481 cycles in Mantis OS. The significant difference stems from the fact that Mantis OS uses a dynamic memory allocation which consumes about 1,655 cycles.   
2. Overhead of executing a task. In SenSpire OS, executing a task may involve context switching in KS depending on the current executing task and the task to be executed (hereafter, target task). It is worth noting that we evaluate the time to execute a task without considering the interference from other tasks. We measure the clock cycles of each operation and the results are reported in Table 3. When the current task is an event and the target task is another event in the same ES, SenSpire OS consumes more cycles than T1, because SenSpire OS takes a two-level event scheduling scheme (i.e., KS and ES). In SenSpire OS, ES scheduling is about 55 cycles which is close to T1; KS scheduling consumes about 67 cycles which is an extra overhead. Scheduling in all the other cases involves context switching, thus has a similar overhead as in Mantis OS.

TABLE 3 Overhead of Executing a Task (in Clock Cycles) 

<table><tr><td>current task</td><td>target task</td><td>T1</td><td>Mantis</td><td>SenSpire</td></tr><tr><td rowspan="3">Event</td><td>Event in the same ES</td><td>45</td><td>N/A</td><td>130</td></tr><tr><td>Event in a different ES</td><td>N/A</td><td>N/A</td><td>402</td></tr><tr><td>Thread</td><td>N/A</td><td>N/A</td><td>402</td></tr><tr><td rowspan="2">Thread</td><td>Event</td><td>N/A</td><td>N/A</td><td>407</td></tr><tr><td>Thread</td><td>N/A</td><td>447</td><td>420</td></tr></table>

TABLE 4 Checking Overhead (in Clock Cycles) and Percent of CPU Active Time 

<table><tr><td>OS version</td><td>checking overhead</td><td>% of active time</td></tr><tr><td>T1 (Optimized)</td><td>26</td><td>4.2%</td></tr><tr><td>SOS (Unoptimized)</td><td>76</td><td>7.4%</td></tr><tr><td>SOS (Optimized)</td><td>28</td><td>4.52%</td></tr><tr><td>SenSpire (Unoptimized)</td><td>36</td><td>5.8%</td></tr><tr><td>SenSpire (Optimized)</td><td>28</td><td>4.5%</td></tr></table>

3. Overhead of empty checking. For interrupt intensive applications, overhead of checking that task queue is empty is critical because that operation will be invoked whenever interrupt completes. We evaluate a blank program that merely listens for incoming packets on Mica2 (e.g., for Mica2, the SPI interrupt is triggered every 418 s) to examine the base overhead of CPU active time. We reported the results in Table 4, and compare them with results reported in [4]. We find that the original version of SenSpire OS costs about 5.8 percent of CPU active time while an optimized version can reduce it to 4.5 percent, comparable to that of TinyOS and SOS (optimized).

# 4.7 Overall System Performance

We have implemented a suite of benchmark applications on SenSpire OS. This section evaluates the overall performance of SenSpire OS with TinyOS (event-driven) and Mantis OS (multithreaded). The following sections examine the CPU utilization, memory consumption, and network performance, respectively.

1. CPU utilization. We examine CPU utilization for Mica2/MicaZ nodes using Avrora [36]. For benchmarks with radio communications, we only evaluate the sender. Table 5 shows the absolute values of CPU utilizations for 11 benchmarks based on TinyOS and SenSpire OS. Fig. 14 shows the CPU utilizations of SenSpire OS normalized to TinyOS for 11 benchmarks. The benchmarks are arranged roughly according to their implementation complexity. We can see that SenSpire OS’s CPU utilization is nearly as small as TinyOS, especially for relatively complex benchmarks. The normalized utilizations for the Blink benchmark and BlinkTask benchmark is relatively large because the absolute CPU utilizations are very low.

TABLE 5 CPU Utilization (Percent) of TinyOS and SenSpire OS 

<table><tr><td>benchmark</td><td>TinyOS</td><td>SenSpire OS</td></tr><tr><td>Blink</td><td>0.0273</td><td>0.0594</td></tr><tr><td>BlinkTask</td><td>0.0286</td><td>0.0648</td></tr><tr><td>CntToLeds</td><td>0.0582</td><td>0.0698</td></tr><tr><td>CntToRfm</td><td>5.8816</td><td>6.053</td></tr><tr><td>CntToLedsAndRfm</td><td>5.8876</td><td>6.065</td></tr><tr><td>Sense</td><td>0.0809</td><td>0.0893</td></tr><tr><td>SenseTask</td><td>0.0876</td><td>0.0985</td></tr><tr><td>SenseToLeds</td><td>0.1367</td><td>0.1446</td></tr><tr><td>SenseToRfm</td><td>5.9469</td><td>6.1836</td></tr><tr><td>Oscilloscope</td><td>0.3017</td><td>0.311</td></tr><tr><td>OscilloscopeRF</td><td>5.4983</td><td>5.9681</td></tr></table>

![](images/a0485ab1cb9d701c72676517b8587587813d81dfd029381f402141a69c2edf09.jpg)



Fig. 14. CPU utilization of SenSpire OS normalized to TinyOS.   
![](images/d2e8578af0ada725a68f8130ae406cd6f3bd18b661ed9b7724ee501ffe530cd3.jpg)



Fig. 15. CPU utilization comparison of SenSpire OS with Mantis OS and T2.

Fig. 15 shows the absolute CPU utilizations for another two benchmarks. The first benchmark, BlinkLed, is from Mantis OS, and the second benchmark, BlinkToRadio, is from T2. We can see that SenSpire OS has a lower CPU utilization than Mantis OS (the value normalized to Mantis OS is only 35 percent). In addition, SenSpire OS has a lower CPU utilization than T2 (the normalized value to T2 is 68 percent). One of the reasons we could identify is that T2 does CPU low power management and computes the lowest possible sleep mode whenever the system is idle, which consumes extra CPU cycles.

2. Memory consumption. We examine memory consumption for Mica2/MicaZ nodes in terms of RAM consumption (for data) and flash consumption (for code). Fig. 16 shows the RAM consumption for 11 benchmarks based on TinyOS and SenSpire OS. Overall, SenSpire OS’s RAM consumption is comparable to TinyOS. We have not shown RAM consumption of Mantis OS, because Mantis OS uses a dynamic memory allocation scheme so that the RAM consumption cannot be statically determined.

![](images/6f08036817df4f215b38a979dcf87e0d92de59f7b9562d88837e56e8a5c13b00.jpg)



Fig. 16. Data memory (RAM) consumption of TinyOS and SenSpire OS.

Fig. 17 shows the flash consumption for 11 benchmarks based on TinyOS and SenSpire OS. Similarly, SenSpire OS’s flash consumption is acceptably small.

Fig. 18 shows the flash consumption for two benchmarks, BlinkLed (from Mantis OS) and BlinkToRadio (from T2). We can see that SenSpire OS has a lower code size than Mantis OS. This is partially because we have done static optimizations in the CSpire compiler. SenSpire OS also has a lower code size than T2. Admittedly, the current SenSpire OS version still misses some kernel functionalities present in T2, e.g., low power management. We consider it a future directions of work for SenSpire OS.

# 4.8 Reprogramming Efficiency

The reprogramming energy efficiency depends on the transferred file size [40]. This section examines the transferred file size of SenSpire OS.

We compare the SELF with CELF which is an optimized module file format for Contiki OS. We implement the CELF approach (as described in [12]) for comparison. Fig. 19 shows the ratios of the CELF size divided by the SELF size for the 11 benchmarks based on SenSpire OS. We can see that SELF is much smaller than CELF. CELF is 1.6-2.5 times larger than SELF. This is because CELF only redefines long data types to short ones. SELF optimizes the file contents, and uses techniques of chained reference and prelinking to system calls to aggressively optimize the file size [11].

# 5 RELATED WORK

TinyOS [2], developed at UC Berkeley, is perhaps the earliest sensor OS in the literature. To enable a flexible architecture and a low resource consumption, TinyOS programming is based on components which are wired together to create a single application image at design-time. Component interactions happen at two directions, i.e., one component can use commands provided by another component; also, one

![](images/63f8b2dcbbbba8038a507e437a5b90e27a7367742d5c604fea0081b860873280.jpg)



Fig. 17. Program memory (program flash) consumption of TinyOS and SenSpire OS.

![](images/d9c6996557833e060d3d3b667bc5fa5e39e35f7eaec23c95bec75fad481ada92.jpg)



Fig. 18. Program code size comparison of SenSpire OS with Mantis OS and T2.

component can signal events to another component. The execution model of TinyOS consists of interrupts and tasks. Interrupts execute at a higher priority and can preempt the execution of tasks. Tasks execute at a lower priority and are scheduled in a FIFO manner. Tasks in TinyOS are written in a run-to-completion manner, and they cannot be preempted or self-suspended. For this reason, I/Os are done in splitphases, i.e., a request is issued before a signal invokes the start of the next task.

Contiki [3], developed at Swedish Institute of Computer Science, is a sensor OS that supports dynamically loadable modules [12]. Contiki supports multithreading via libraries to address the programming inconvenience of event-based programming (e.g., in TinyOS). Contiki also supports a lightweight threading mechanism, i.e., protothreads [21].

SOS [4], developed at the University of California, Los Angeles, also supports dynamically loadable modules. It adopts a module-based architecture which allows dynamically loading and unloading modules. The SOS execution model is only slightly more complex than TinyOS: SOS message handlers (similar to TinyOS tasks) are dispatched according to three different priorities, but preemption is not allowed between two message handlers.

Mantis OS [5], developed at Colorado University, implements a traditional preemptive time-sliced multithreading on sensor nodes. The Mantis kernel supports synchronous I/Os (as opposed to split-phase I/Os), and a set of concurrency control primitives, e.g., binary semaphores (mutex) and counting semaphores.

Nano-RK [6], developed at Carnegie Mellon University, implements a reservation-based real-time OS for WSNs. Nano-RK supports fixed-priority preemptive multitasking for guaranteeing that task deadlines are met. It also supports CPU and network bandwidth reservations, i.e., tasks can specify their resource demands and the OS provides timely, guaranteed and controlled access to CPU cycles and network packets.

RETOS [7], developed at Yonsei University, Korea, is designed to improve several aspects of prior work. It improves system resilience by supporting dual mode operation (i.e., kernel mode and user mode) as well as application code checking at design-time and runtime. It optimizes multithreading implementation [41] and provides support for POSIX 1003.1b real-time scheduling. It also supports loadable modules and provides multihop networking services.

![](images/be8b00dec936a6d7fc819ce04f1a8c0a88b8a9eca376b0b8792be1e940ac1e36.jpg)



Fig. 19. Reprogramming code size comparison of Contiki OS’s approach and SenSpire OS’s approach.

LiteOS [8], developed at the University of Illinois at Urbana Champaign, is designed to provide a traditional Unix-like environments for programming WSN applications. It includes: 1) a built-in hierarchical file system and a wireless shell for user interaction using Unix-like commands. 2) Kernel support for dynamic loading native execution of multithreaded applications. 3) An objectoriented programming language (LiteC++) that uses a subset of C++ as its syntax with class library support.

Pixie OS [9], developed at Harvard University, is designed to enables resource-aware programming. In Pixie, a sensor node has direct knowledge of available resources, such as energy, radio bandwidth, and storage space, and can control resource consumption at a fine granularity. The Pixie OS is based on a dataflow programming model based on the concept of resource tickets, a core abstraction for representing resource availability and reservations. By giving the system visibility and fine-grained control over resource management, a broad range of policies can be implemented.

Aside from the basic system implementations mentioned above, there is a large body of work devoted to improving OS capabilities in different dimensions, e.g., improving OS reliability (e.g., t-kernel [17], Harbor [42], and Neutron [43]), providing real-time support (e.g., FIT [39]), extending the programming model (e.g., protothreads [21], TOSThreads [24]), and providing reprogramming support (e.g., Deluge [29], Stream [40], and Elon [44]). For a more complete review in the areas of sensor OS design, refer to [45].

# 6 CONCLUSIONS AND FUTURE WORK

In this paper, we present SenSpire OS, a predictable, flexible, and efficient operating system for WSNs. We improve system predictability by two-phase interrupt servicing and predictable thread synchronization; we achieve system flexibility by providing a hybrid model for both event-driven programming and multithreaded programming; we retain system efficiency by employing stack sharing and modular design. In addition, we have designed a three-layer networking stack and an object-oriented programming language (CSpire) to enhance system usability and programming convenience. Having implemented SenSpire OS on three most commonly used sensor node platforms, we evaluate its performance extensively.

While we have shown that SenSpire OS is promising in providing a flexible environment for building predictable and efficient sensor network applications. There is much future work to consider. In particular, we would like to examine how SenSpire OS’s design principles will enhance the performance of large-scale complex WSN applications.

# ACKNOWLEDGMENTS

The authors would like to thank Fan Sun, Jie Chen, Zhengxing Zhuo, Zhenyuan Zhao, Shuopei Meng, Ming Xie, Xiaofan Wu, Gong Chen, and Guodong Teng in the development of SenSpire OS. The authors thank the anonymous reviewers for their insightful comments. This work is supported by the National Basic Research Program of China (973 Program) under Grant No. 2006CB303000, the National Science Foundation of China (Grant No. 61070155), the Program for New Century Excellent Talents in University (NCET-09-0685), and in part by an NSERC Discovery Grant under Grant No. 341823-07, NSERCStrategic Grant STPGP 364910-08, FQRNT 2010-NC-131844.

# REFERENCES

[1] I.F. Akyildiz, W. Su, Y. Sankarasubramaniam, and E. Cayirci, “Wireless Sensor Networks: A Survey,” Computer Networks, vol. 38, pp. 393-422, 2002.   
[2] TinyOS, http://www.tinyos.net,   
[3] A. Dunkels, B. Gro¨nvall, and T. Voigt, “Contiki—A Lightweight and Flexible Operating System for Tiny Networked Sensors,” Proc. 29th Ann. IEEE Int’l Conf. Local Computer Networks (LCN ’04), 2004.   
[4] C.-C. Han, R. Kumar, R. Shea, E. Kohler, and M. Srivastava, “A Dynamic Operating System for Sensor Nodes,” Proc. Third Int’l Conf. Mobile Systems, Applications, and Services (MobiSys), 2005.   
[5] S. Bhatti, J. Carlson, H. Dai, J. Deng, J. Rose, A. Sheth, B. Shucker, C. Gruenwald, A. Torgerson, and R. Han, “MANTIS OS: An Embedded Multithreaded Operating System for Wireless Micro Sensor Platforms,” J. Mobile Networks and Applications, vol. 10, pp. 563-579, 2005.   
[6] A. Eswaran, A. Rowe, and R. Rajkumar, “Nano-RK: An Energy-Aware Resource-Centric RTOS for Sensor Networks,” Proc. 26th IEEE Int’l Real-Time Systems Symp. (RTSS), 2005.   
[7] H. Cha, S. Choi, I. Jung, H. Kim, and H. Shin, “RETOS: Resilient, Expandable, and Threaded Operating System for Wireless Sensor Networks,” Proc. Sixth Int’l Conf. Information Processing in Sensor Networks (IPSN ’07), 2007.   
[8] Q. Cao, T.F. Adbelzaher, and J.A. Stankovic, “The LiteOS Operating System: Towards Unix-Like Abstractions for Wireless Sensor Networks,” Proc. Seventh Int’l Conf. Information Processing in Sensor Networks (IPSN ’08), 2008.   
[9] K. Lorincz, B. rong Chen, J. Waterman, G. Werner-Allen, and M. Welsh, “Resource Aware Programming in the Pixie OS,” Proc. Sixth ACM Conf. Embedded Network Sensor Systems (SenSys), 2008.   
[10] Q. Wang, Y. Zhu, and L. Cheng, “Reprogramming Wireless Sensor Networks: Challenges and Approaches,” IEEE Network Magazine, vol. 20, no. 3, pp. 48-55, May/June 2006.   
[11] W. Dong, C. Chen, X. Liu, J. Bu, and Y. Liu, “Dynamic Linking and Loading in Networked Embedded Systems,” Proc. IEEE Sixth Int’l Conf. Mobile Ad Hoc and Sensor Systems (MASS ’09), 2009.   
[12] A. Dunkels, N. Finne, J. Eriksson, and T. Voigt, “Runtime Dynamic Linking for Reprogramming Wireless Sensor Networks,” Proc. Fourth Int’l Conf. Embedded Networked Sensor Systems (SenSys ’06), 2006.   
[13] J. Regehr, “Safe and Structured Use of Interrupts in Real-Time and Embedded Softwares” Handbook of Real-Time and Embedded Systems, 2007.   
[14] D. Gay, P. Levis, R. von Behren, M. Welsh, E. Brewer, and D. Culler, “The nesC Language: A Holistic Approach to Networked Embedded Systems,” Proc. ACM Conf. Programming Language Design and Implementation (PLDI ’03), 2003.   
[15] L.E.L. del Foyo, P. Mejı´a-Alvarez, and D. de Niz, “Predictable Interrupt Management for Real Time Kernels over conventional PC Hardware,” Proc. 12th IEEE Real-Time and Embedded Technology and Applications Symp. (RTAS ’06), 2006.   
[16] L. Sha, R. Rajkumar, and J.P. Lehoczky, “Priority Inheritance Protocols: An Approach to Real-Time Synchronization,” IEEE Trans. Computers, vol. 39, no. 9, pp. 1175-1185, Sept. 1990.   
[17] L. Gu and J.A. Stankovic, “t-Kernel: Providing Reliable OS Support to Wireless Sensor Networks,” Proc. Fourth Int’l Conf. Embedded Networked Sensor Systems (SenSys ’06), 2006.

[18] R. von Behren, J. Condit, and E. Brewer, “Why Events are a Bad Idea for High-Concurrency Servers,” Proc. Ninth Conf. Hot Topics in Operating Systems (HOTOS ’03), citeseer.ist.psu.edu/ vonbehren03why.html, 2003.   
[19] J. Ousterhout, “Why Threads Are a Bad Idea (for Most Purposes) (Invited Talk),” http://www.softpanorama.org/People/ Ousterhout/Threads/index.shtml, 1996.   
[20] P. Li and S. Zdancewic, “Combining Events and Threads for Scalable Network Services Implementation and Evaluation of Monadic, Application-Level Concurrency Primitives,” Proc. ACM Conf. Programming Language Design and Implementation (PLDI ’07), 2007.   
[21] A. Dunkels, O. Schmidt, T. Voigt, and M. Ali, “Protothreads: Simplifying Event-Driven Programming of Memory-Constrained Embedded Systems,” Proc. Fourth Int’l Conf. Embedded Networked Sensor Systems (SenSys ’06), 2006.   
[22] W.P. McCartney and N. Sridhar, “Abstractions for Safe Concurrent Programming in Networked Embedded Systems,” Proc. Fourth Int’l Conf. Embedded Networked Sensor Systems (SenSys ’06), 2006.   
[23] E. Trumpler and R. Han, “A Systematic Framework for Evolving TinyOS,” Proc. Third Workshop Embedded Networked Sensors (EmNets), 2006.   
[24] K. Klues, C.-J.M. Liang, J. yeup Paek, R. Musaloiu-E, P. Levis, A. Terzis, and R. Govindan, “TOSThreads: Safe and Non-Invasive Preemption in TinyOS,” Proc. Seventh ACM Conf. Embedded Networked Sensor Systems (SenSys ’09), 2009.   
[25] M. Welsh and G. Mainland, “Programming Sensor Networks Using Abstract Regions,” Proc. USENIX First Conf. Symp. Networked Systems Design and Implementation (NSDI ’04), 2004.   
[26] J. Regehr, A. Reid, K. Webb, M. Parker, and J. Lepreau, “Evolving Real-Time Systems Using Hierarchical Scheduling and Concurrency Analysis,” Proc. 24th IEEE Real-Time Systems Symp. (RTSS ’03), 2003.   
[27] C. Duffy, U. Roedig, J. Herbert, and C.J. Sreenan, “Adding Preemption to TinyOS,” Proc. Fourth Workshop Embedded Networked Sensors (EmNets ’07), 2007.   
[28] K. Ha¨nninen, J. Ma¨ ki-Turja, M. Bohlin, J. Carlson, and M. Nolin, “Determining Maximum Stack Usage in Preemptive Shared Stack Systems,” Proc. 27th IEEE Int’l Real-Time Systems Symp. (RTSS ’06), 2006.   
[29] J.W. Hui and D. Culler, “The Dynamic Behavior of a Data Dissemination Protocol for Network Programming at Scale,” Proc. Second Int’l Conf. Embedded Networked Sensor Systems (SenSys ’04), 2004.   
[30] R.K. Panta and S. Bagchi, “Hermes: Fast and Energy Efficient Incremental Code Updates for Wireless Sensor Networks,” Proc. IEEE INFOCOM, 2009.   
[31] J.R. Levine, Linkers and Loaders. Morgan Kaufmann, 2000.   
[32] K. Klues, V. Handziski, C. Lu, A. Wolisz, D. Culler, D. Gay, and P. Levis, “Integrating Concurrency Control and Energy Management in Device Drivers,” Proc. 21st ACM SIGOPS Symp. Operating Systems Principles (SOSP), 2007.   
[33] J. Polastre, J. Hui, P. Levis, J. Zhao, D. Culler, S. Shenker, and I. Stoica, “A Unifying Link Abstraction for Wireless Sensor Networks,” Proc. Third Int’l Conf. Embedded Networked Sensor Systems (SenSys ’05), 2005.   
[34] J. Chen, W. Xu, S. He, Y. Sun, P. Thulasiramanz, and X. Shen, “Utility-Based Asynchronous Flow Control Algorithm for Wireless Sensor Networks,” IEEE J. Selected Areas in Comm., vol. 28, no. 7, pp. 1116-1126, Sept. 2010.   
[35] R. Fonseca, O. Gnawali, K. Jamieson, S. Kim, P. Levis, and A. Woo, “The Collection Tree Protocol (CTP), TinyOS Extension Proposals (TEP) 123,” Aug. 2006.   
[36] B.L. Titzer, D.K. Lee, and J. Palsberg, “Avrora: Scalable Sensor Network Simulation with Precise Timing,” Proc. Fourth Int’l Symp. Information Processing in Sensor Networks (IPSN), 2005.   
[37] M. Maro´ti, B. Kusy, G. Simon, and A. Le - ´deczi, “The Flooding Time Synchronization Protocol,” Proc. Second Int’l Conf. Embedded Networked Sensor Systems (SenSys ’04), 2004.   
[38] P. Levis, D. Gay, V. Handziski, J.-H. Hauer, B. Greenstein, M. Turon, J. Hui, K. Klues, C. Sharp, R. Szewczyk, J. Polastre, P. Buonadonna, L. Nachman, G. Tolle, D. Culler, and A. Wolisz, “T2: A Second Generation OS for Embedded Sensor Networks,” technical report, Technical Univ. Berlin, 2005.

[39] W. Dong, C. Chen, X. Liu, K. Zheng, R. Chu, and J. Bu, “FIT: A Flexible, Lightweight, and Real-Time Scheduling System for Wireless Sensor Platforms,” IEEE Trans. Parallel and Distributed Systems, vol. 21, no. 1, pp. 126-138, Jan. 2010.   
[40] R.K. Panta, I. Khalil, and S. Bagchi, “Stream: Low Overhead Wireless Reprogramming for Sensor Networks,” Proc. IEEE INFOCOM, 2007.   
[41] H. Kim and H. Cha, “Multithreading Optimization Techniques for Sensor Network Operating Systems,” Proc. Fourth European Conf. Wireless Sensor Networks (EWSN ’07), 2007.   
[42] R. Kumar, E. Kohler, and M. Srivastava, “Harbor: Software-Based Memory Protection for Sensor Nodes (Poster),” Proc. Sixth Int’l Conf. Information Processing in Sensor Networks (IPSN), 2007.   
[43] Y. Chen, O. Gnawali, M. Kazandjieva, P. Levis, and J. Regehr, “Surviving Sensor Network Software Faults,” Proc. ACM SIGOPS 22nd Symp. Operating Systems Principles (SOSP ’09), 2009.   
[44] W. Dong, Y. Liu, X. Wu, L. Gu, and C. Chen, “Elon: Enabling Efficient and Long-Term Reprogramming for Wireless Sensor Networks,” Proc. ACM Int’l Conf. Measurements and Modeling of Computer Systems (SIGMETRICS), 2010.   
[45] W. Dong, C. Chen, X. Liu, and J. Bu, “Providing OS Support for Wireless Sensor Networks: Challenges and Approaches,” IEEE Comm. Surveys and Tutorials, vol. 12, no. 4, pp. 519-530, Oct.-Dec. 2010.

![](images/8c5eb8144f896734c9f0ee2865d3c5b91a79cee22076f283a2a724c4f6deac7c.jpg)



Wei Dong received the BS and PhD degrees from the College of Computer Science, Zhejiang University, in 2005 and 2011, respectively. He is currently a post-doc fellow in the Department of Computer Science and Engineering of Hong Kong University of Science and Technology. His research interests include networked embedded systems and wireless sensor networks. He is a student member of the IEEE.

![](images/972c223a20e03b40d030f56b83fcf5756daf97c5e3ab4ea0eaf661623b45cf87.jpg)



Chun Chen received the bachelor of mathematics degree from Xiamen University, China, in 1981, and the MS and PhD degrees in computer science from Zhejiang University, China, in 1984 and 1990, respectively. He is a professor at the College of Computer Science, and the Director of Institute of Computer Software at Zhejiang University. His research interests include embedded system, image processing, computer vision, and CAD/CAM. He is a member of the IEEE.

![](images/3af593b9e8a814b37592d33a5823390ae362b6f76fa0b69d386cbce480ed48d0.jpg)



Xue Liu is an associate professor in the School of Computer Science at McGill University. He received his PhD in computer science from the University of Illinois at Urbana-Champaign in 2006. He received his BS degree in Mathematics and MS degree in Automatic Control both from Tsinghua University, China. He was the Samuel R. Thompson Associate Professor in the University of Nebraska-Lincoln in 2010. His research interests are in computer networks

and communications, smart grid, real-time and embedded systems, cyber-physical systems, data centers, and software reliability. His work has received the Year 2008 Best Paper Award from IEEE Transactions on Industrial Informatics, and the First Place Best Paper Award of the ACM Conference on Wireless Network Security (WiSec 2011). He is a member of the IEEE and the ACM.

![](images/b5ce1116353a1da6d37644e63901d62b5a2901e64dee5cbfbf8469500117c226.jpg)



Yunhao Liu received the BS degree from the Automation Department of Tsinghua University, China, in 1995, and the MA degree from Beijing Foreign Studies University, China, in 1997, and the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is a member of Tsinghua National Laboratory for Information Science and Technology, and the Director of Tsinghua National MOE Key Lab for Information

Security. He is also a faculty member at the Department of Computer Science and Engineering, the Hong Kong University of Science and Technology. He is a senior member of the IEEE, the IEEE Computer Society and the ACM Distinguished Speaker.

![](images/e2c580e0a260904de322ca81e548e1cd80fec27426f414a7256b5e5f254deba4.jpg)



Jiajun Bu received the BS and PhD degrees in computer science from Zhejiang University, China, in 1995 and 2000, respectively. He is a professor at the College of Computer Science and the deputy dean of the Department of Digital Media and Network Technology at Zhejiang University. His research interests include embedded system, mobile multimedia, and data mining. He is a member of the IEEE and the ACM.

![](images/25a7e33accd469181f127eec8dea49010a5063528da90aa9f7db5995efedbba6.jpg)



Kougen Zheng received the BSc degree from North-East Heavy Machinery Institute, in 1986, the PhD degree from the University of Warwick, United Kingdom, in 1992. He is currently a professor at the Computer Science College, Zhejiang University. His research interests include operating systems, computer networks, and artificial intelligence.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.