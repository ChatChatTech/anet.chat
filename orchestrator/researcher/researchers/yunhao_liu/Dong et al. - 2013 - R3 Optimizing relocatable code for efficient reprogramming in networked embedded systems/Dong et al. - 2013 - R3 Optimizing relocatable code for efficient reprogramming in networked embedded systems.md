# R3: Optimizing Relocatable Code for Efficient Reprogramming in Networked Embedded Systems

Wei Dong $^{\dagger}$ , Biyuan Mo $^{\dagger}$ , Chao Huang $^{\dagger}$ , Yunhao Liu $^{\ddagger\S}$ , and Chun Chen $^{\dagger}$ $^{\dagger}$ Zhejiang Key Lab of Service Robot, CS College, Zhejiang University; $^{\ddagger}$ TNLIST, School of Software, Tsinghua University; $^{\S}$ CS Department, HKUST {dongw, bobroute, huangchao88, chenc}@zju.edu.cn, yunhao@greenorbs.com

Abstract—We present a holistic reprogramming system called R3. R3 has two salient features. First, the binary differencing algorithm within R3 (R3diff) ensures an optimal result in terms of the delta size under a configurable cost measure. Second, the similarity preserving method within R3 (R3sim) optimizes the binary code format for achieving a large similarity with a small metadata overhead. Overall, R3 achieves the smallest delta size compared to other incremental approaches such as Rsync [11], RMTD [9], Zephyr/Hermes [17], [18], and R2 [2], e.g., 50%–99% reduction compared to Stream and about 20%–40% reduction compared to R2. R3's implementation on TelosB/TinyOS is lightweight and efficient. We release our code at http://code.google.com/p/r3-dongw.

# I. INTRODUCTION

Recent advances in microelectronic mechanical systems (MEMS) and wireless communication technologies have fostered the rapid development of networked embedded systems like wireless sensor networks. System software for these self-organizing systems often needs to be updated for a variety of reasons—fixing bugs, changing network functionality, tuning system parameters, etc. In our recent efforts in deploying a large-scale sensor network system—GreenOrbs during Dec, 2010–April, 2011, we regularly face the requirement of software upgrade. For example, our software version increases from version 158 to version 285 in the SVN repository. Although some modifications are intended for good readability and maintenance, we manually identify that at least 15 (i.e. 12%) of the updates are critical to system performance, including fixing link estimation bugs, adding additional metrics for diagnosis, etc.

The current software update technologies are often undersatisfactory. The serial programming approach does not scale well as it requires collecting all nodes back, attaching to computers to “burn” new codes, and redeploying all nodes into the field. Researchers have thus introduced wireless reprogramming techniques to enable each node to automatically update the software through wireless communications. The default wireless reprogramming approach—Deluge $[10]$ for TinyOS, however, has a large impact on the system performance as it often needs to transfer a large binary code. The huge amount of transmissions may quickly degrade system performance since radio transmission dominates the energy consumption on a sensor node $[6]$ , $[23]$ .

Many efforts have been made to improve the efficiency of wireless reprogramming, such as virtual machines $[13]$ , $[15]$ , modular designs $[3]$ , $[5]$ , $[8]$ , compression $[22]$ , incremental approaches [2], [9], [11], [17], [18], network encoding [1], [7], [20], etc. In this work, we consider the incremental approach to improve the reprogramming efficiency.

The rational behind incremental reprogramming is that the change to the software is often much smaller than the entire code in most software change cases. Hence, transferring only the changed part (which is encoded in a delta file) can significantly reduce the amount of transmissions. Regarding the delta file, there are two factors affecting its size.

(1) The differencing algorithm. It should generate a small delta file given two binary files. Existing binary differencing algorithms suffer from two limitations. First, they do not ensure an optimal result in terms of the delta file size. Second, some of them may incur a large overhead in terms of execution time and memory consumption, e.g. for the GreenOrbs programs, the RMTD algorithm $[9]$ has an execution time of about 60s and a memory consumption of 240MB. This makes the RMTD algorithm unsuitable for increasingly complex programs (e.g., programs for iMote2 nodes). We aim to propose an optimal differencing algorithm in terms of the delta file size with greatly improved runtime performance.

(2) The code generation mechanism should generate binaries with large similarity (between successive code versions) so that the differencing algorithm can benefit from the achieved similarity and the delta size can be further reduced. Existing methods achieve a limited similarity, and they may cause memory segmentations. Some of them may even have a large additional metadata overhead. We aim to propose an optimized binary code format that achieves a large similarity without causing memory segmentation or incurring a large metadata overhead.

We build a holistic reprogramming system called R3. R3 has two salient features. First, the binary differencing algorithm within R3 (R3diff) ensures an optimal result in terms of the delta size under a configurable cost measure. The time and space complexity of R3diff is $O(n^3)$ and $O(n)$ respectively. For all the benchmarks examined in this paper, the execution time varies from 0.01s to 0.29s, and the memory requirement varies from 50KB to 870KB, which significantly improves the runtime performance of RMTD proposed in [9]. Second, the similarity preserving method within R3 (R3sim) optimizes the binary code format for achieving a large similarity with a small metadata overhead. Overall, R3 achieves the smallest delta size compared to other incremental approaches such as Rsync [11], RMTD [9], Zephyr/Hermes [17], [18], and R2 [2]. R3's implementation on TelosB/TinyOS is lightweight and efficient.

The rest of this paper is structured as follows. Section II describes the background. Section III introduces the related work. Section IV presents the design details. Section V shows the evaluation results. Finally, Section VI concludes the paper and gives future research directions.

# II. BACKGROUND

# A. Incremental reprogramming

The key idea of incremental reprogramming is to transfer only the delta between the old code and the new code. Typically, the delta file size is much smaller than the entire new code size. Upon reception of the delta file, each node reconstructs the new code by patching the delta to the old code.

The delta file format usually encodes two kinds of commands. The ADD command inserts a byte sequence of a specified length. The COPY command copies a byte sequence from the old code to the new code. These two commands consume certain bytes to make them interpretable. Specifically, we use commands of the following forms (the subscript denotes the number of bytes consumed by each field):

$$
\mathrm{ADD} _ {1} <   \mathrm{n} > _ {2} <   \text { BYTE1 }.. \text { BYTEn } > _ {n}
$$

where $n$ is the number of added bytes. This command costs a total of $\alpha + n = 3 + n$ bytes.

$$
\text { COPY } _ {1} <   n > _ {2} <   \text { old\_addr } > _ {2}
$$

where n is the length of copied bytes, old\_addr is the start address in the old code. This command costs a total of $\beta = 5$ bytes. It is worth noting that the start address in the new code is not needed because the new code is reconstructed in sequential order.

To minimize the delta size, the differencing algorithm should take this encoding overhead into account.

# B. Relocatable code

Relocatable code is produced by the compiler, and in which all memory references in the code needing relocation are specially marked and can be relocated by the linker. Dynamic relocatable code can be relocated during load-time linking.

It is worth mentioning the concept of position independent code (PIC). PIC is a term for code that can run in any address space. This differs from relocatable code, which requires special processing by a link editor or program loader to make it suitable for execution at a given location. PIC uses other mechanisms like PC relative addressing instead of absolute addressing. PIC can effectively reduce the metadata overhead compared to relocatable code. Another benefit of PIC for PC software is that the code can be shared (and loaded into different virtual memory addresses) among different processes. The same benefit does not exist on motes without MMUs.

However, PIC needs compiler support. For example, on the MSP platform, no compiler is known to fully support PIC [4].

# III. RELATED WORKS

In this section, we briefly discuss various works in the field of wireless reprogramming.

# A. Native approach

Deluge [10] provides reprogramming support for TinyOS applications. As sensor nodes need to be reprogrammable for multiple times, Deluge transfers the single application image along with the reprogramming protocol. Stream [19] reduces the transferred code size by pre-installing the reprogramming protocol on the external flash as another application image (i.e., the reprogramming image).

# B. Loadable modules

The SOS [8], Contiki OS [4], [5], and the FlexCup extension [16] to TinyOS support loadable modules. In these systems, individual modules can be loaded dynamically on the nodes. Specific challenges exist in these systems. First, they require disseminating symbol tables and relocation tables for linking and relocating. These may be quite large, typically 45% to 55% of the object file [17]. Second, they make extensive use of the program flash.

Elon [3] addresses this issue by introducing the concept of replaceable component. In the network reprogramming process, only the replaceable component needs to be disseminated, greatly reducing the dissemination cost. Compared to other modular OSes such as Contiki OS and SOS, which enable reprogramming on a modular basis, Elon does not incur the overhead of relocation entries.

# C. Incremental approaches

Incremental reprogramming [2], [9], [11], [17], [18] is a technique to reduce the transferred code size by disseminating the delta file.

Jeong and Culler [11] modify the Rsync algorithm [21] for efficient incremental reprogramming for sensor nodes. Such a block-based algorithm, suitable for handling large files in computers, is inappropriate for energy-efficient reprogramming for micro embedded systems. The RMTD algorithm proposed in [9] is a byte-level differencing algorithm with $O(n^{3})$ time complexity and $O(n^{2})$ space complexity. It only ensures optimal results under $\alpha = 0$ . In practice, the large space requirement makes it unsuitable to scale to increasingly complex software programs (e.g. programs for iMote2 motes).

Koshy and Pandey [12] mitigate the effects of function shifts by using slop regions after each function in a program so that the function addresses do not change when each function grows within the slop region.

Zephyr [18] mitigates the effects of function shifts by using a function indirection table. Hermes [17] mitigates the effects of data shifts by first pinning variables to the same locations by source-level modifications, and then adopt two different approaches for handling data shifts.

R2 [2] unifies the approaches for handling function shifts and data shifts by using relocatable code. Memory addresses in the reference instructions are inflated with zeros for achieving large similarity between two codes. However, as illustrated in the R2 paper, the metadata occupies a large portion for complex software, and needs to be carefully compressed in a customized manner.

![](images/912f16bd207d4d2abcde492afeb72e807551cb124c222ce15997f9be3a568230.jpg)



Fig. 1: R3's overview

# IV. DESIGN

This section introduces R3's design. Figure 1 gives an overview of R3. R3's similarity preserving method, R3sim, augments the GCC compiler by generating code binaries with large similarity. R3's differencing algorithm, R3diff, takes the generated binary files as inputs, and generates a delta for dissemination. The dissemination protocol disseminates delta to all nodes. Upon reception of the delta file, the R3cons component on each node reconstructs the new binary code by patching the delta to the old binary code. Finally, R3's bootloader residing on each node, R3boot, loads the new binary code to the program flash and starts executing the new code.

# A. Similarity preserving method: R3sim

In R2, we propose a unified approach to handle shifts of functions, data variables, and interrupt service routines. R2 inflates reference addresses to zeros and appends a relocation entry for each reference instruction. Although R2 achieves a large similarity in the program code, it has a relatively large overhead in the relocation table (as illustrated in the R2 paper and analyzed in this section). This motivates us to devise an optimized code format that can preserve a large code similarity as R2 while incurs a low metadata overhead.

R2 reserves a relocation entry (offset, addr) for each reference instruction. The 2-byte offset field tells which memory address needs relocation while the 2-byte addr field tells the actual target address. There are two inefficiencies in R2's relocation table. First, each relocation entry contains an additional word (offset) in order to locate the address that needs relocation. Second, the number of relocation entries is proportional to the number of reference instructions (denoted as n), instead of the number of unique symbols (denoted as m).

The first factor contributes 1/2 metadata overhead while the second factor contributes nearly 1/3 metadata overhead since the number of unique symbols is approximately 1/3 of the number of reference instructions (as observed from the benchmarks we examined).

Nevertheless, the bytes in these factors encode useful information needed for relocation. There does exist a technique called chained reference (CR) [14] to encode the relocation entries in a more compact manner. The key idea of CR is trying to merge the relocation entries for the same symbol, because references to the same symbol in different locations of the program must point to the same target address. To achieve this goal, CR uses references to the same symbol in the program (which contain useless addresses before relocation) to create a linked list. Each relocation entry in the relocation table requires two values: an index to the symbol and a pointer to the first reference of that symbol (i.e., the header of the linked list). The loader performs relocation by traversing each linked list. By this technique, the size of the relocation table can be reduced from 4n to 4m.

The CR technique still suffers from two problems. First, each relocation entry still contains 2-byte offset for locating the first memory address that needs relocation. Second, more importantly, CR needs to inflate the references to appropriate pointers, which can decrease the code similarity.

We try to use another technique in R3sim. First, in order to make references to the same symbol unchanged, we must inflate the references in the instructions to the same value. In R2, we inflate all references to zeros while in R3 we make more efficient use of the 2 bytes, i.e., we inflate them to the symbol indices. A symbol index refers to a symbol entry which contains the actual symbol address. The same symbol has the same index in the old code and new code. This technique reduces the overhead from 4n to 4m while still preserves a large code similarity. Second, we do not use the 2-byte offset field to explicitly indicate which memory address needs relocation. Instead, we use a bitmap indicating which address needs relocation. On the MSP platform, relocation is performed on a 2-byte granularity with only one relocation type. The bit value of 1 indicates that the corresponding 2-byte code needs relocation while the value of 0 indicates that no relocation is required. This technique eliminates the overhead of the offset field while incurring the bitmap overhead of C/16≈6.2%C.

We can see that R3 preserves the similarity while can reduce the metadata overhead. R2's metadata overhead is 4n while R3's metadata overhead is 2m+C/16. We examine all benchmarks in this paper and find that n≈0.0864C and m≈0.0233C. Hence, R3 achieves approximately 0.24C reduction in the metadata overhead.

The workflow of the R3's similarity preserving method, R3sim, can be described as follows. First, the GCC compiler compiles the source code to a relocatable ELF. R3sim takes inputs of the relocatable ELF and the symbol table of the previous version to generate another ELF with similarity preserved. The old symbol table serves a reference for generating the new symbol table. R3sim will try to allocate the same index for the same symbol. When a symbol is deleted in the new version, R3 marks the entry as empty. When a symbol is added in the new version, R3 will try to use an empty slot before it allocates a new one. R3sim also generates a bitmap file and the new symbol table in binary forms. The generated ELF file is also converted to a binary file. All three files are combined to a single binary file which can be loaded for execution by

# R3boot.

We summarize R3's benefits over prior approaches:

- R3 keeps the merits of R2. R3 unifies the approach for handling function shifts and data shifts. It also nicely handle the shift of interrupt handlers. R3 preserves a large code similarity as R2.   
- R3 does not cause memory segmentation and makes efficient use of memory. While the indirection table of Zephyr requires additional program flash space, R3's symbol table does not occupy program flash space.   
- R3 effectively reduces R2's metadata overhead.   
- R3 does not require source-level modification as Hermes. Hermes requires accessing source files to keep similarity of data variables. However, most library files are provided in the form of relocatable binary instead of source files. R3 can be nicely integrated to this compilation model.

# B. Differencing algorithm: R3diff

R3diff takes the binary files of two successive versions, and generates a delta for dissemination. There are some design decisions for R3diff.

(1) R3diff should compare files at the smallest granularity of change. As most file changes are at the byte level, we devise R3diff to be byte-level. Comparing files at the smaller granularity, e.g. bit, will incur larger overhead because the storage requirement of bit-address will be larger than that of byte-address.

(2) However, the bitmap file generated by R3sim changes at the bit level. In this case, R3diff performs less effective without change. Although we can devise an additional bit-level comparison algorithm, we would like to reuse the code of byte-level R3diff. We keep the R3diff core unchanged by feeding it extended bitmap files (i.e. 1 bit in the original bitmap files is extended to 1 byte). Correspondingly, we need to set $\alpha' = 8 \times \alpha$ , $\beta' = 8 \times \beta$ in order to correctly reflect the encoding cost in bits. We then use an additional utility to compact the generated delta back to bit formats.

We now describe R3diff, the byte-level comparison algorithm which is optimal in terms of the delta size.

We define $opt_{i}$ as the minimum transferred delta size to construct the first i bytes of the new code. We can get (1) $opt_{0}=0$ . (2) $opt_{i}\geq opt_{i-1}$ , where $i\geq1$ . This inequality holds because if we can use $opt_{i}$ bytes to construct i bytes, we can also use these $opt_{i}$ bytes to construct i-1 bytes. Hence the smallest delta size used to construct i-1 bytes should be no smaller than $opt_{i}$ .

R3diff's major steps are described as follows.

(1) Generate footprints. We generate footprints (i.e. hash values) for every $p = \beta - \alpha + 1 = 3$ continuous bytes in the old code. The hash values are used to identify common segments (CS) in two code versions. Identifying CS smaller is not necessary because copying small number of bytes is not beneficial than adding them. For each hash location, we store an entry representing a length-p segment at a specified offset in the old code. For segments hashed to the same value, we use a linked list to store all entries. The storage requirement is thus $(nold - p + 1) \times sizeof(entry)$ where nold is the size of the old code.

(2) We compute $opt_{i}$ for $1 \leq i \leq n$ new where $n$ new is the size of the new code. Here $i$ denotes the number of constructed bytes in the new code. Hence $i - 1$ denotes the index of the last constructed byte.

(2.1) In order to compute $opt_{i}$ , we perform an operation, findk, on the last index (i-1). The findk function takes an index in the new code as input, and returns the smallest index in the new code, denoted as k, such that [k,i-1] matches a segment in the old code.

(2.2) In order to compute $opt_{i}$ , we introduce two additional notations, $opt_{i}^{A}$ and $opt_{i}^{C}$ . The former represents the minimum number of bytes to construct i bytes with ADD as the last command. The latter represents the minimum number of bytes to construct i bytes with COPY as the last command, or, equals to LARGE\_INTEGER if the last byte must be added. By definition, $opt_{i} = \min(opt_{i}^{A}, opt_{i}^{C})$ .

(2.3) Compute $opt_{i}^{A}$ and $opt_{i}^{C}$ as follows.

$$
o p t _ {i} ^ {A} = \min (o p t _ {i - 1} ^ {A} + 1, o p t _ {i - 1} ^ {C} + \alpha + 1) \tag {1}
$$

$$
o p t _ {i} ^ {C} = \left\{ \begin{array}{l} \text { LARGE\_INTEGER }, \text { if } k > i - 1 \\ o p t _ {k} + \beta , \text { otherwise } \end{array} \right. \tag {2}
$$

Note that the last byte cannot be copied when k>i-1.

We denote n=max(nold, nnew). The worst-case time complexity of the algorithm is $O(n^{3})$ , and the average time complexity of the algorithm is $O(n^{2})$ . The space complexity is $O(n)$ . It can be proved that the R3diff algorithm generates the smallest delta size for a given encoding cost of $\alpha$ and $\beta$ .

# V. EVALUATION

In this section, we evaluate the R3 reprogramming system. Section V-A describes the evaluation methodology. Section V-B presents a comparative study on the delta sizes generated by different approaches.

# A. Methodology

We evaluate R3 on TinyOS 2.1.1/TelosB. We select three software change cases from the TinyOS distribution as well as three software change cases in the development of our GreenOrbs application.

- Case 1: We change the Blink application from blinking the red led every 1 second to that blinking the red led every 2 seconds.   
- Case 2: We change the Blink application to CntToLeds which increments a counter every 1 second and displays the lowest three bits on the leds.   
- Case 3: We change the RadioCountToLeds application to RadioSenseToLeds.   
- Case 4: We consider the GreenOrbs application of SVN version 168. The base version performs sensing, transmissions, etc while the updated version disables sensing and enables local logging on the external flash.   
- Case 5: We consider the change case of GreenOrbs from version 182 to 183. The updated version fixes a link estimation bug in the 4bitle component.   
- Case 6: We consider the change case of GreenOrbs from version 306 to 314. The updated version provides another parameter for reconfiguration.

![](images/8ee2b59d592ba89c1ff59dd9b8b543eb8c1222422250099ef7ac1738c6ef23c3.jpg)



Fig. 2: Delta size comparison among six approaches

# B. Delta size

This section evaluates how similarity preserving methods impact delta size. When possible, we use these methods with R3diff which is proved to be optimal. It is worth noting that different methods may require slightly different differencing algorithms for improved performance. For example, Hermes requires additional metacommand to optimize the delta of the function indirection table; R2 requires a content-aware differencing algorithm to optimize the delta of the relocation table; and R3 requires a bit-level comparison algorithm to optimize the delta of bitmap files. In the evaluation, we take the above optimizations.

Figure 2 shows the transferred file sizes for various reprogramming approaches, including Stream, Zephyr, R2/R2c, and R3. Note that R2c is a variation of R2 with the chained reference technique described in Section IV-A. In Fig. 2, we also show the sizes of metadata. The notation “Table” refers to the indirection table for Zephyr, the relocation table for R2, and the symbol table for R3. The notation “bitmap” refers to the bitmap file in R3. We can see that R3 greatly reduces R2’s metadata overhead while preserves a high code similarity as R2, resulting in the smallest delta size.

# VI. CONCLUSION

We present a holistic reprogramming system called R3. The binary differencing algorithm within R3 (R3diff) ensures an optimal result in terms of the delta size under a configurable cost measure. The similarity preserving method within R3 (R3sim) optimizes the binary code format for large similarity with a small metadata overhead. Overall, R3 achieves the smallest delta size compared to other incremental approaches such as Rsync [11], RMTD [9], Zephyr/Hermes [17], [18], and R2 [2]. R3's implementation on TelosB/TinyOS is lightweight and efficient.

As a future work, we would like to port R3 to other embedded platforms and OSes.

# ACKNOWLEDGMENT

This work is supported in part by the National Science Foundation of China Grants No. 61202402, 61070155, and 61170213, the Fundamental Research Funds for the Central Universities (2012QNA5007), the Research Fund for the Doctoral Program of Higher Education of China (20120101120179), and NSFC Distinguished Young Scholars Program under Grant No. 61125202.

# REFERENCES

[1] W. Dong, C. Chen, X. Liu, J. Bu, and Y. Gao, “A Lightweight and Density-aware Reprogramming Protocol for Wireless Sensor Networks,” IEEE Trans on Mobile Computing, vol. 10, no. 10, pp. pp. 1403–1415, 2011.   
[2] W. Dong, Y. Liu, C. Chen, J. Bu, and C. Huang, "R2: Incremental Reprogramming using Relocatable Code in Networked Embedded Systems," in Proc. of IEEE INFOCOM, 2011.   
[3] W. Dong, Y. Liu, X. Wu, L. Gu, and C. Chen, “Elon: Enabling Efficient and Long-Term Reprogramming for Wireless Sensor Networks,” in Proc. of ACM SIGMETRICS, 2010.   
[4] A. Dunkels, N. Finne, J. Eriksson, and T. Voigt, “Run-Time Dynamic Linking for Reprogramming Wireless Sensor Networks,” in Proceedings of ACM SenSys, 2006.   
[5] A. Dunkels, B. Grönvall, and T. Voigt, “Contiki—a Lightweight and Flexible Operating System for Tiny Networked Sensors,” in Proc. of EmNets, 2004.   
[6] R. Fonseca, P. Dutta, P. Levis, and I. Stoica, “Quanto: Tracking Energy in Networked Embedded Systems,” in Proc. of USENIX OSDI, 2008.   
[7] A. Hagedorn, D. Starobinski, and A. Trachtenberg, “Rateless Deluge: Over-the-Air Programming of Wireless Sensor Networks using Random Linear Codes,” in Proc. of ACM/IEEE IPSN, 2008.   
[8] C.-C. Han, R. Kumar, R. Shea, E. Kohler, and M. Srivastava, “A Dynamic Operating System for Sensor Nodes,” in Proc. of ACM MobiSys, 2005.   
[9] J. Hu, C. J. Xue, and Y. He, “Reprogramming with Minimal Transferred Data on Wireless Sensor Network,” in Proc. of IEEE MASS, 2009.   
[10] J. W. Hui and D. Culler, “The dynamic behavior of a data dissemination protocol for network programming at scale,” in Proc. of ACM SenSys, 2004.   
[11] J. Jeong and D. Culler, “Incremental Network Programming for Wireless Sensors,” in Proc. of IEEE SECON, 2004.   
[12] J. Koshy and R. Pandey, “Remote Incremental Linking for Energy-Efficient Reprogramming of Sensor Networks,” in Proc. of EWSN, 2005.   
[13] ——, “VM\*: Synthesizing Scalable Runtime Environments for Sensor Networks,” in Proceedings of ACM SenSys, 2005.   
[14] J. R. Levine, Linkers and Loaders. Morgan Kaufmann, 2000.   
[15] P. Levis and D. Culler, “Maté: a tiny virtual machine for sensor networks,” in Proceedings of ACM ASPLOS, 2002.   
[16] P. J. Marrón, M. Gauger, A. Lachenmann, D. Minder, O. Saukh, and K. Rothermel, “FlexCup: A Flexible and Efficient Code Update Mechanism for Sensor Networks,” in Proceedings of EWSN, 2006.   
[17] R. K. Panta and S. Bagchi, “Hermes: Fast and Energy Efficient Incremental Code Updates for Wireless Sensor Networks,” in Proc. of IEEE INFOCOM, 2009.   
[18] R. K. Panta, S. Bagchi, and S. P. Midkiff, “Zephyr: Efficient Incremental Reprogramming of Sensor Nodes using Function Call Indirections and Difference Computation,” in Proc. of USENIX Annual Technical Conference, 2009.   
[19] R. K. Panta, I. Khalil, and S. Bagchi, “Stream: Low Overhead Wireless Reprogramming for Sensor Networks,” in Proc. of IEEE INFOCOM, 2007.   
[20] M. Rossi, N. Bui, G. Zanca, L. Stabellini, R. Crepaldi, and M. Zorzi, "SYNAPSE++: Code Dissemination in Wireless Sensor Networks Using Fountain Codes," IEEE Transactions on Mobile Computing, vol. 9, no. 12, pp. 1749–1765, 2010.   
[21] Rsync: http://samba.anu.edu.au/rsync/.   
[22] N. Tsiftes, A. Dunkels, and T. Voigt, “Efficient Sensor Network Reprogramming through Compression of Executable Modules,” in Proceedings of IEEE SECON, 2008.   
[23] Q. Wang, Y. Zhu, and L. Cheng, “Reprogramming Wireless Sensor Networks: Challenges and Approaches,” IEEE Network Magazine, vol. 20(3), pp. 48–55, 2006.