# A Stern-based Collusion-Secure Software Watermarking Algorithm and Its Implementation

Jieqing Ai $^{1}$ , Xingming Sun $^{1,2}$ , Yunhao Liu $^{3}$ , Ingemar J. Cox $^{2}$ , Guang Sun $^{4}$ and Yi Luo $^{1}$

1. School of Computer and Communication, Hunan University, Changsha, China

2. UCL Adastral Park Campus, University College London, UK

3. Hong Kong University of Science & Technology

4. Hunan College of Finance & Economic, Changsha, China

dotrai@126.com, sunnudt@163.com

# Abstract

Stern algorithm is a robust static software watermarking scheme. It can resist many common attacks except collusive attacks. In this paper we propose an improved Stern algorithm, make it has the ability of resisting collusive attacks and simplify its implementation at the same time. Furthermore, we describe the implementation of our algorithm and the issues that arise when targeting MSIL. We then validated it by experiments against a variety of attacks.

# 1. Introduction

Using software watermarking technique to hide copyright information and track piracy is one of the important ways to protect software intellectual property [1]. Currently, watermarking algorithm is described as either being static or dynamic [2, 3, and 4]. Static watermarking algorithms only make use of the features of an application that are available at compile-time, such as the instruction sequence or the constant pool table in a Java application, to embed a watermark. On the other hand, a dynamic watermarking algorithm relies on information gathered during the execution of the application to both embed and recognize the watermark. Dynamic watermarking is more robust than static watermarking, but it can not resist from the simple subtract attacks. The advantage of static watermarking is easy to carry out, but it fails to resisting many attacks by semantics-preserving program transformations, including compilation, optimization, obfuscation, de-compilation, and dead-code removal, etc. For the limitation of static watermarking, Stern and Hachenz proposed a robust object watermarking [6], which was based on Cox's spread spectrum technique [7, 8]. The greatest difference from other software watermarking algorithms is that Stern algorithm does not treat the program as a serial or consequence of instructions, but as a statistical object. The idea is to spread the watermark over the entire application by a chosen instructions vector. It makes attacks difficult to locate where the watermark is embedded. It provides a high level of stealth and manner of resilience against attack.

The Stern algorithm has been implemented in SANDMARK framework [9], and the experiment shows it can resist many attacks, but it has following problems too:

1. Stern algorithm is not resilient to collusive attacks [9]. Because the algorithm does not protect the code book, which is the chosen instructions vector to present the watermark. Attacker can extrapolate the code book by comparing the applications with different watermark, and then disturb the instruction frequency in the application, so the watermark will be destructed.   
2. Hard to implement [6]. The Stern algorithm embeds watermark by modifying instruction frequencies, but when an instruction frequency is modified, the other instruction frequencies will be modified too, so a large scale of code will be modified to accomplish watermark embedding.   
In this paper, we proposed an improved Stern algorithm, make it has the ability of resisting collusive attack, our work includes:   
1. Make the Stern algorithm has the ability of resilience to collusive attacks by different code book strategy.   
2. Simplify the implementation by embedding watermark in different way.   
3. Implement the algorithm in MSIL.   
4. Compare the performance with Stern algorithm.

# 2. Our solution

Let P be a code, and $P_{w}$ be a watermarked code, W be the information inputted by users, watermark w is computed by a secure algorithm with W and key k, the length of w is n; Let $V=\left\{v_{0},v_{1},v_{2},\cdots,v_{n-1}\right\}$ be the chosen code book, while the $v_{i}$ is a single instruct or a instruct group; For each element i in V, we compute the number of occurrences $c_{i}$ of $v_{i}$ in the code P, and we form the occurrence vector $c=(c_{0},c_{1},c_{2},\cdots,c_{n-1})$ ; while the vector $d=(d_{0},d_{1},d_{2},\cdots,d_{n-1})$ is the number of occurrences of each instruction group in the code $P_{w}$ .

# 2.1. Watermark Embedding

1. Compute the number of occurrences of each element in code book V to form the vector c.   
2. Input secret key k and user information W, using a security pseudo-random number compute the watermark $w = (w_{0}, w_{1}, \cdots, w_{n-1})$ .   
3. Rearrange the order of elements in vector $c$ to form $c'$ by the secret key $k$ :

$$
c ^ {\prime} = \left(c _ {0} ^ {\prime}, c _ {1} ^ {\prime}, c _ {2} ^ {\prime}, \dots , c _ {n - 1} ^ {\prime}\right),
$$

And the $c'$ should be satisfied the following rule:

$$
\exists i, 0 \leq i <   n, c _ {i} ^ {\prime} \neq c _ {i}.
$$

4. Modify the code in such a way to make sure that the new extracted vector $b$ from watermarked application is equal to $c' + w$ , that is:

$$
b = (b _ {0}, b _ {1}, b _ {2}, \dots , b _ {n - 1}),
$$

$$
b _ {i} = w _ {i} + c _ {i} ^ {\prime}.
$$

Modifying the occurrences of the instruction groups is done in an iterative manner. A sophisticated modification is done to the code while preserving its correctness and the new occurrence vector is computed. If the new vector is closer to b, the process is continued, else the modification is refused.

# 2.2. Watermark Embedding

The Watermark Extraction algorithm compares the occurrence vector extracted from the original code with watermarked code. If they differ by approximately w we conclude that the watermark is present.

1. Set a detection threshold $\partial$ , $(0 < \partial < 1)$ .   
2. Compute the vector $d$ of the watermarked code $P_{w}$ by code book $V$ .   
3. Rearrange the order of elements in vector $d$ to form $d'$ by the secret key $k$ with the same way of embedding watermark.   
4. Compute the detected watermark $w'$ :

$$
w ^ {\prime} = d ^ {\prime} - c ^ {\prime}
$$

$$
w ^ {\prime} = (w _ {0} ^ {\prime}, w _ {1} ^ {\prime}, w _ {2} ^ {\prime}, \dots , w _ {n - 1} ^ {\prime}).
$$

5. Normalizing the watermark $w$ and the detected watermark $w'$ to unit magnitude:

$$
\tilde {w} = \frac {w}{| w |}
$$

$$
\tilde {w} ^ {\prime} = \frac {w ^ {\prime}}{| w ^ {\prime} |}
$$

6. Compute the similarity measure $z_{nc}$ between $\tilde{w}$ and $\tilde{w}^{\prime}$ :

$$
z _ {n c} = \frac {\sum_ {i = 1} ^ {n} \left(\tilde {w} _ {i} - \overline {{\tilde {w}}}\right) \left(\tilde {w} _ {i} ^ {\prime} - \overline {{\tilde {w} ^ {\prime}}}\right)}{\sqrt {\sum_ {i = 1} ^ {n} \left(\tilde {w} _ {i} - \overline {{\tilde {w}}}\right) ^ {2} \times \sum_ {i = 1} ^ {n} \left(\tilde {w} _ {i} ^ {\prime} - \overline {{\tilde {w} ^ {\prime}}}\right) ^ {2}}}
$$

If $z_{nc}$ is higher than $\partial$ then the algorithm outputs marked, else it outputs unmarked. In ideal situation, the result of $z_{nc}$ will be 1. According to experience in SANDMARK, if $z_{nc} \geq 0.9$ , it means marked; if $z_{nc} \leq 0.6$ , it means unmarked or the watermark is destructed; if $0.6 \leq z_{nc} \leq 0.9$ , it means the application may be marked.

# 3. Performance analysis

# 3.1. Date rate

The data rate $D_{c}$ of our watermarking algorithm essentially depends on the number of instruction groups defined in the code book V and the size of application P, that is $D_{c} = |V| \times |P|$ . Each vector instruction group encodes certain number of bits of watermark. Hence, the total number of bits that can be encoded depends on the number of vector instruction groups; and the smaller the application is, the smaller the data rate is.

# 3.2. Effect on code size

The algorithm modifies the number of occurrences of instruction groups in two ways, one is code substitution and the other is redundant instructions insertion. Code substitutions have a minimal impact on the size and performance of the target application. The reason is that for most substitutions the original and the substituted code segments are of the same or similar lengths. For this reason, it is important to try to construct as many code substitution patterns as possible. However, it is not always possible to create enough substitution patterns. The reason is that code substitutions have very strict limit. Let we have three instruction groups, that is A, B and C, A and C are members of code book V, B is a code segment of target application P, to substitute the instructions group B with A we must satisfy the following conditions:

a) For any instruction group $C, C \neq A$ , it must be satisfied:

$$
\forall C \in V, A \not \subset C a n d B \not \subset C;
$$

b) The instruction groups $A$ and $B$ is semantically equivalent.

The strict limit of code substitutions results in that the application which will be watermarked have not enough instruction groups to be substituted. On complex instruction set architectures (such as the X86 targeted in the implementation of the Stern algorithm $[7]$ ) this may be fairly easy since there are many possible code sequences with the same semantics. On a RISC machine or a virtual machine such as the CLR this is typically much harder since there are fewer instructions available. The way of code substitutes can not find enough semantically equivalent instruction groups when embedding huge data. For this reason it becomes important to construct redundant instructions to increase the occurrences of vector groups. Insert redundant instructions will certainly increase the size of application, if the size of code book V is n, the average length of each instruction group in V is d, the average number of times that each instruction group needs to be inserted is x, and the total number of inserted instructions will amount to $n \times d \times x$ . Further more, when using the Stern algorithm to modify the frequencies of instruction groups to embedding watermark, the other instruction groups frequencies will be modified too [9], this is very hard to close the goal to finishing embedding watermark and will modify a large scale of code. While in our solution, we just modify the number occurrence of instruction groups in the code, has no effect to other instruction groups and just needs to modify a small scale of code to finish embedding. So the table 1 shows that our solution has better performance in code size.

# 3.3. Effect on the consumption of time

The way of instruction substitutes has no effect on time consumption, because it does not increase the code size. While insert redundant instructions will certainly increase the running time. If the running time of a single instruction is t, the total instructions number of original code is N, the inserted number of instructions is S, the time consumption will be $(N+S)\times t$ , the increased scale of time is $[S/(N+S)]\times100\%$ , it means the bigger the N is, the less percentage of effect on time consumption is.

# 4. Implementation and Experiment

# 4.1. Implementation in MSIL

We must concern three problems when the scheme implemented in MSIL: a). how to form the code book V; b). how to rearrange the order of elements in vector c; c). how to substitute instructions and how to insert instructions.

# 4.1.1. How to form the code book V

In both our solution and the Stern algorithm, the code book V is assumed to be kept secret from the attacker, it contains information on which code substitutions and insertions are legal and how they affect the instruction group occurrences. The way of forming V determines the robustness against different classes of attacks. But the Stern algorithm just concerns the VECTOR EXTRACTION step without think about the circumstances of implementing. While we implement our solution based on MSIL instruction set, so the code book V must meet the following four conditions:

a) We choose the element of $V$ just in Base Instructions and Object Model Instructions. Because it's relatively ease to operate those instructions.   
b) Choose those instructions that can resist most normal attacks. For example the instructions 'ceq; brtrue.s'.   
c) Choose those instructions which outputted by the compiler frequently. For example the instructions 'ldstr; call void WriteLine ()'.   
d) The chosen instruction must be independent from each other. For example the instruction ‘add’ and ‘sub’ can not be chosen at the same time, if not, when replace the ‘add’ with ‘neg; sub’, that will reduce the number of occurrence of ‘add’ and the number of occurrence of ‘sub’ will be increased accordingly.

# 4.1.2. How to rearrange the elements of vector $\mathcal{C}$

Rearranging the order of elements in code book V can make our solution has the ability of resisting collusive attacks. The order of elements in V is determined by the secret key k. The secret key k determines where the instruction will be changed and when will be changed. We can rearrange the code book V by inputting different k each time. For example we can rearrange the order of elements in code book V in this way:

$$
c _ {i} ^ {\prime} = c _ {(i + k) \% n}.
$$

# 4.1.3. How to substitute instructions and how to insert instructions

There are two ways to modify the number of occurrence of instructions: Code substitution and insert nullified instructions. Whatever the way is, we must make sure that the stack's balance in the virtual machine. The stack must be empty when the code segment ends with instructions like “return” in CLR or JVM. When we substituting code or inserting code, the program can’t run correctly if the stack not in balance. For example, let $s_{0}$ be the start state of stack before inserting instructions, $G = (g_{0}, g_{1}, g_{2}, \cdots, g_{m-1})$ be the instructions about to be inserted, it must meet the following demands:

a) when inputting instruction $g_{i}, i \neq m - 1$ , the switch of states is:

$$
S _ {i} \xrightarrow {g _ {i}} S _ {i + 1}, \text {   and   } S _ {0} \neq S _ {i + 1},
$$

It makes our solution more resilient to code optimization.

b) When the inputted instruction is $g_{m-1}$ , the switch of states is:

$$
S _ {m - 1} \xrightarrow {g _ {m - 1}} S _ {0},
$$

It makes the state of stack return to original state and makes sure the application run in correct action.

# 4.2. The experiment and analysis

# 4.2.1. The experiment circumstance

Platform: Windows XP Professional, P4 2.66 GHz CPU, 512 MB RAM, .net framework 2.0, ILDASM.

We choose the most used application in SANDMARK to test our solution performance, as shown in the following table 1:

<table><tr><td rowspan="2"></td><td rowspan="2">Class</td><td colspan="3">Code Size (kb)</td></tr><tr><td>Before</td><td>After(Stern)</td><td>Our solution</td></tr><tr><td>XML Tree</td><td>27</td><td>61</td><td>64.7</td><td>62</td></tr><tr><td>Toy_1 .3</td><td>123</td><td>581</td><td>599</td><td>591</td></tr><tr><td>TTT</td><td>4</td><td>8</td><td>10.4</td><td>9.6</td></tr><tr><td>Spiro</td><td>24</td><td>69</td><td>81</td><td>80.4</td></tr><tr><td>Conzilla</td><td>586</td><td>1445</td><td>1590</td><td>1587</td></tr><tr><td>Cvt2 mae</td><td>28</td><td>311</td><td>331</td><td>318</td></tr></table>

Table 1: Test specimens and their features.

# 4.2.2. Experimental Results

In experiments, we compare the performance of our solution with the Stern algorithm in 7 different attacks, the result shows in the following figure 1. Set 1 be collusive attack, 2 be code reordering, 3 be additive and subtractive attack, 4 be code obfuscation, 5 be code recompile, 6 be code optimization, and 7 be code compress.

![](images/4caae7f95c01164d4cf9917a41e9f29fda1f55b0279b3549e280f545b0274166.jpg)



Figure 1: The performance comparison with threshold $\partial = 0.9$

# 4.2.3. Analysis of Results

In the SandMark framework, it use the same code book to embed watermark each time, which will be very easily to find out the key information of the code book by collusive attacks, and then the watermark will be easily destroyed. In our solution, we make the watermark has the ability of resisting collusive attacks by rearrange the order of elements in code book V, because attackers can hardly extrapolate the instructions of the rearranged code book V. If the size of V is n, the different order of rank achieved to n! and the difficulty of collusive attack will amount to n!.

Additive attacks have little infection on our solution. Additive attacks usually change the code size considerably and are generally has no effect. If the inserted code has the same or similar instruction static distribution with the watermarked application, which will be no infection on watermark extraction; if the attacker insert code in irregular way like randomly increases large scale of additive nullified instructions, the infection on watermark extraction is very little too. Because there are more than 200 kinds of MSIL instructions, if the code book V contains n kinds of single instruction and the attacker irregularly insert only one kind of instruction, we can calculate the infection on watermark extraction, which is just about $(n/200)\times100\%$ . The code book V not only contains single instruction but also multi-instructions groups, the possibility of change multi-instructions occurrences in code is less than the possibility of single instruction, so the way of inserting additive instructions has very little chance in destroying the watermark, not more than $(n/200)\times100\%$ .

The way of code rearrange attack has no infection on our solution, because our solution is based on instruction statistic distribution strategy like Stern algorithm. Decompiling and recompiling and optimizing the watermarked application can be a serious threat for Stern algorithm but not for us. This can be attributed to the type of instructions in the code book and decompiling can seriously change the code. Some of the substitution and embed/nullify groups are non-optimal to accommodate the required vector instruction groups. In our solution, we choose the instruction groups in a strict way that make sure those instruction groups can resilient to semantics-preserving program transformations. Code compressing has no infection on our solution, compressing may change the number of occurrences of instructions, but at the of the application's running time, the code will be decompressed. The decompressed code is the same with the watermarked code.

# 5. Conclusion

In this paper we proposed a collusion-secure software watermark algorithm and implemented in MSIL. We simplify the difficulty of realization of Stern algorithm, and our solution has the ability of resisting many attacks by semantics-preserving program transformations, including compilation, optimization, obfuscation, and dead-code removal, etc.

In future work, we can set a dynamic changing weight for each instruction that make it have the ability of auto-adapted, because different instruction has different infection under those attacks.

# 6. Acknowledgments

This paper is supported by the National Natural Science Foundation of China under Grant No.60573045, the National Research Foundation for the Doctoral Program of Higher Education of China No.20050532007, and National 973 Basic Research Program of China No.2006CB303000.

# 7. References

[1] J. Nagra, C. Thomborson and C. Collberg, "Software Watermarking: Protective Terminology", Australian Computer Science Conference, Australasian, 2002, pages 177-186.   
[2] C. Collberg and C. Thomborson, “Watermarking, tamper proofing and obfuscation tools for software protection”, IEEE Transactions on Software Engineering, 2002, pages 735-746.

[3] Li-he Zhang, Yi-xian Yang and Xin-xi Niu, “A survey on Software Watermarking”, Journal of Software, 2003, pages 268-277.   
[4] D. Curran, M. O. Cinneide and N. Hurley, "Dependency in software watermarking", Information and Communication Technologies: From Theory to Applications Conference, 2004, pages 569-570.   
[5] C. Collberg and C. Thomborson, “Software Watermarking: Models and Dynamic Embeddings”, In POPL’99, 26 $^{th}$ Annual SIGPLAN-SIGACT Symposium on Principles of Programming Languages, San Antonio, 1999, pages 311-324.   
[6] I. Cox, J. Kilian and F.T. Leighton et al, “A secure, robust watermark for multimedia”, Workshop on Information Hiding, Univ. of Cambridge, 1996, pages 175-190.   
[7] J. P. Stern, G. Hachez and F. Koeune et al, “Robust object watermarking: application to code”, In

Proceedings of the $5^{th}$ International Workshop on Information Hiding, 1999, Pages 368-378.   
[8] I. Cox, Matthew L. Miller and A. Jeffrey. Digital Watermarking, Publishing House of Electronics Industry, Perking. 2003.   
[9] T. Sahoo and C. Collberg. “Software Watermarking in the Frequency Domain: Implementation, Analysis, and Attack”, Journal of Computer Security, 2006, pages 721-755.   
[10] MSIL Instructions Specification, October 2000, www.ssw.uni-linz.ac.at/Teaching/Lectures/Sem/2001/Literatur/ILinstrset.doc.   
[11] C. Collberg, G.R. Myles and A. Huntwork, "SandMark — A tool for software protection research", IEEE Magazine of Security and Privacy, 2003, pages 40-49.