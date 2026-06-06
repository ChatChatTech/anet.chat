# Cardinality Estimation for Large-scale RFID Systems

Chen Qian, Hoilun Ngan, and Yunhao Liu

Department of Computer Science and Engineering

Hong Kong University of Science and Technology

{cqian, cpeglun, liu}@cse.ust.hk

Abstract—Counting or estimating the number of tags is crucial for large-scale RFID systems. The use of multiple readers was recently proposed to improve the efficiency and effectiveness in reading RFID tags. Due to the long processing time, tag identification based counting schemes are often impractical, especially when tags are attached to moving objects. The existing estimation based schemes, on the other hand, suffer from the multiple-reading problem. To address this issue, we propose the Lottery Frame (LoF) scheme, a replicate-insensitive estimation protocol, that is able to eliminate multiple-readings. We show the high accuracy, short processing time and low overhead of the proposed LoF scheme through analysis and simulations.

# I. INTRODUCTION

Radio Frequency Identification (RFID) technology [1] has been widely used for many applications, such as localization [2] [3] and objects tracking [4], activity monitoring [5], and access control and security [6]. An RFID system typically consists of three components: readers, tags and the middleware software [7]. RFID readers with antennas are devices used to read or write data to RFID tags. RFID tags are labeled in designated objects where each tag has a small size of memory to store its unique ID as well as other information.

Counting the number of tags in a given region is one of the most important tasks in large-scale RFID systems. Intuitively, we can identify all tags in the region [8] and then compute the cardinality. As many tags may respond to a reader simultaneously, the collision among tags becomes a critical factor affecting the reading accuracy. Many anti-collision schemes have been proposed [9] [10] [11] [12] [13], falling into two categories: Slotted ALOHA schemes [11] and Tree-based or Binary Splitting schemes [12] [13]. The most significant shortcoming of such schemes is the long processing latency. As analyzed in [13], using tree-based schemes to identify 3000 tags will need over 1000 seconds. For slotted ALOHA schemes, the time is even longer [9]. Hence, existing schemes based on the identification of individual tags are impractical for large-scale RFID systems, especially when tags are attached to mobile objects. In this case, a tag may leave the reader’s range before being identified.

![](images/7cd2d7037bd6b4e996cd2d8652bdf166630c87001fe180f2a84d255d063ae064.jpg)



Fig. 1. An example of multi-reader RFID systems

In order to address the long latency issue, estimation schemes without identification are proposed [14] [15]. Most, if not all, of those approaches are designed for a single reader. Due to the terrain and limited interrogation region of readers, however, large-scale RFID deployments often need multiple readers [16], in which several readers are placed to cover the entire region of interest. Multi-reader RFID systems, being efficient and effective, suffer from the so-called multiple-reading problem. As illustrated in Fig. 1, a number of tags stay in the overlapping interrogation region and respond to multiple readers simultaneously. Let $r _ { 1 } , r _ { 2 } , . . . , r _ { m }$ denote the readings of m readers. Some tags are counted by multiple readers. To estimate the total number of tags, the existing schemes can be generalized to use either $\mathbf { M A X } ( r _ { 1 } , r _ { 2 } , . . . , r _ { m } )$ or $\mathbf { S U M } ( r _ { 1 } , r _ { 2 } , . . . , r _ { m } )$ 1 2as the estimator. For example, in ( 1 2 )Fig. 1, existing schemes report either the MAX, which is 5, or the SUM, 15, while the actual number of tags is 10.

Moreover, most of previous estimation schemes use dynamic incremental slotted ALOHA frames [14] [15]. They modify their frame size based on the feedback from readers. Consequently, many communication rounds are needed to finalize an optimal length of the frame, which is linearly proportional to the size of the tag set. For example, to estimate thousands of tags, readers should create frames with hundreds of slots [14]. Thus, the processing time will be extremely long in large-scale RFID systems.

In this work, we propose the Lottery Frame (LoF) protocol, a non-identification based scheme to estimate the cardinality of tags. The advantages of LoF include: (1) replicate-insensitive with a high accuracy; (2) good scalability with short processing time and light communication overhead; and (3) no need of anti-collision schemes. The design can be easily implemented in current RFID systems without particular assumptions about the number and placement of readers and tags.

The rest of this paper is organized as follows. In Section II, we describe the replicate-insensitive estimation problem. Section III presents our basic ideas, and Section IV describes the detailed protocol design. We present the performance evaluation in Section V. We discuss related work in Section VI and conclude this work in Section VII.

# II. PROBLEM DESCRIPTION

In order to improve coverage, many RFID systems deploy multiple readers with overlapping interrogation regions [16], so as to guarantee that most tags are able to access at least one reader, even when the wireless links are unreliable and dynamically changing. Suppose there are n tags in a certain region and m readers can fully cover that region. The estimation results of readers are $r _ { 1 } , r _ { 2 } , . . . , r _ { m }$ . Obviously, we have

$$
M A X (r _ {1}, r _ {2},..., r _ {m}) \leq n \leq S U M (r _ {1}, r _ {2},..., r _ {m}) \tag {1}
$$

By employing the existing estimators like USE and UPE [14], each reader can obtain an estimation result of the tags in its vicinity. Nevertheless, it is only possible to compute $\mathbf { M A X } ( r _ { 1 } , r _ { 2 } , . . . , r _ { m } )$ and $\mathbf { S U M } ( r _ { 1 } , r _ { 2 } , . . . , r _ { m } )$ ( 1 2 ) ( 1 2 )to estimate the entire cardinality. In some cases, these two values are feasible estimators of n. For instance, if the target area is so small that each reader is able to cover the whole area, the MAX estimator is very close to n. Also, if the readers are deployed sparsely and the overlapping regions are rare, the SUM estimator is also acceptable. The problem in SUM estimator is that tags in the overlapping regions are read by multiple readers so that they are counted for multiple times. In other words, SUM estimator contains replicate information. The replicates make SUM larger than the exact value of n like the case shown in Fig. 1.

There are mainly two types of multiple-reading. The type in the example of Fig. 1 is called spatial multiplereading, which means each tag is possibly recorded by multiple readers. The other type observed by us is called temporal multiple-reading, in which a tag is counted by the same reader for multiple times. For example, in Intelligent Transportation Systems (ITS) [17], a car passing by a reader twice will be recorded as two vehicles in the database. Temporal multiple-reading also happens in signal-reader context. In this work, we only consider spatial multiple-reading. Temporal multiple-reading can be analyzed similarly.

Besides accuracy, other important metrics of RFID tag estimation algorithms include processing time and communication overhead, as fast speed is the major motivation of using estimation schemes to replace identification algorithms.

In following parts, we will introduce our replicateinsensitive estimation scheme LoF, which eliminates the replicates by hashing and OR operation. Furthermore, it remarkably saves the processing time and communication overhead compared with previous estimation schemes. In the design of LoF, we assume the entire region of interest is covered by multiple readers. We also assume every tag in that region can access at least one reader. Besides, each tag stores a number of hash values. The removal of these assumptions has impact on the accuracy of the result, but does not overthrow its correctness. There are no further assumptions about the number and placement of readers or tags.

# III. BASIC PRINCIPLES FOR LOF ALGORITHM

In slotted ALOHA identification schemes, the reader creates an ALOHA frame with several time slots, and then add the frame length (number of time slots) into the interrogation message sent to tags nearby. Each tag randomly picks a time slot to transmit back. Since only the tags that transmit to slots without collision can be recognized, the reader has to keep sending requests until each tag is identified at least once.

Due to the possible collisions, the identification process needs more than one transmission round. Nevertheless, the collision information can help to estimate the cardinality, even though most tags are not identified. For example, if the frame length is 10, and 8 slots are idle (with no response), it is likely that the number of tags is no more than 3. Conversely, if nine of them are collision slots, the cardinality is mostly much larger. This is the basic idea of our design, called Linear Probabilistic Estimation (LPE), which shares some features with Linear Probabilistic Counting [18].

Suppose each reader $r _ { j }$ construct an ALOHA frame $F _ { j }$ with l time slots, and then broadcast the length l to probe tags nearby. When a tag $t _ { i }$ receives the probe message, it applies a particular hash function $H ( k e y )$ to its ID i. The hash values of $H ( k e y )$ ( )are uniformly ( )distributed and range from 0 to h. After obtaining the result $H ( i ) , t _ { i }$ normalizes $H ( i )$ to $[ 0 , l - 1 ]$ and denotes ( ) ( ) [0 1]the normalized value as k. Then it picks the kth slot in the frame to respond.

Consider a reader $r _ { j }$ keeping a bitmap $B M _ { j }$ , where the bit $B M _ { j } [ k ]$ is corresponding to the time slot k in $F _ { j } ,$ , where $k = 0 , 1 , 2 . . .$ . If the reader $r _ { j }$ hears no response = 0 1 2(idle) in the time slot $k ,$ it sets $B M _ { j } [ k ]$ as 0. Obviously, if the reader hears one tag’s response or multiple responses (collision), the bit $B M _ { j } [ k ]$ will be set as 1. Let $V _ { 0 }$ denote [ ]the number of bits with value $0 ,$ and $V _ { 1 }$ 0denote the 1number of bits with value 1. In single-reader scenarios, supposing the tag number is n and the frame length is l, we have the following result.

Lemma 3.1: If n, l are very large, the expectation of $V _ { 0 }$ and $V _ { 1 }$ follow

$$
E (V _ {0}) = l e ^ {- n / l} \tag {2}
$$

$$
E (V _ {1}) = l (1 - e ^ {- n / l}) \tag {3}
$$

Proof: For the kth bit in the bitmap, it will become 0 as if no tags respond in the time slot k. We know that every tag has $1 / l$ probability to respond to the time slot k. Therefore,

$$
P r (B M [ k ] = 0) = (1 - \frac {1}{l}) ^ {n} = e ^ {- n / l}
$$

Hence we obtain,

$$
E (V _ {0}) = \sum_ {k = 0} ^ {l - 1} P r (B M [ k ] = 0) = l e ^ {- n / l}
$$

Since $V _ { 0 } + V _ { 1 } = l ,$ ,

$$
E (V _ {1}) = l - E (V _ {0}) = l \left(1 - e ^ {- n / l}\right)
$$

□

Replacing n and $E ( V _ { 0 } )$ by their representations in ( 0)terms of observed variables n and $V _ { 0 }$ , we get,

˜ 0Estimator 1. n is an estimator of the tag number $n ,$ where

$$
\tilde {n} = - l \ln (V _ {0} / l) \tag {4}
$$

![](images/eaa1331cada110b945395db8d6b6a7fdbaabdc9a7e78da35f6bcdb85e35de3f7.jpg)  
Fig. 2. Examples of LPE

Figure 2(a) gives an example of Estimator 1 in singlereader scenarios. Every tag hashes itself to a time slot of a frame with size $l = 8 .$ . After hearing the whole frame, = 8the reader knows that two slots are with no transmission, three slots are with one transmission and the other three slots are with collision. Therefore, $V _ { 0 } = 2$ and $V _ { 1 } = 6$ . We may estimate the number of tags based on formula (4).

$$
\tilde {n} = - l \log (V _ {0} / l) = - 8 \times \log (2 / 8) = 1 1. 0 9 0 4
$$

The estimated value of the tag number is 11.0904, which is very close to the exact number 11.

The property of hashing is suitable for eliminating replications, since the datum with the same value will have the same hash value. Applying this estimator to multi-reader RFID systems, each of the readers does not compute $V _ { 0 } , \ V _ { 1 }$ individually, instead, a reader reports 0 1its bitmap to the central server. When receiving bitmaps from all readers, the server applies logical OR to those bitmaps and obtain a merged bitmap. Then the server calculates the estimator n referring to the merged bitmap. ˜An example of this process in multi-reader RFID systems is illustrated in Fig. 2(b).

We claim that Estimator 1 is a replicate-insensitive estimation scheme in multi-reader scenarios and prove the correctness as follows.

Lemma 3.2: Suppose two tag sets $S _ { 1 }$ and $S _ { 2 }$ are in the vicinities of two readers $r _ { 1 }$ and $r _ { 2 }$ 1 2respectively. $S _ { 1 }$ and $S _ { 2 }$ 1share common members, i.e., $\left| S _ { 1 } \cap S _ { 2 } \right| > 0 .$ 1. The 2 1 2 0estimator of the merged bitmap equals to the estimation result of tag set $S _ { 1 } \cup S _ { 2 }$ .

1 2Proof: Suppose the bitmaps generated by r and r are BM and $B M _ { 2 }$ 1 2. The server obtain a third bitmap $B M _ { 3 } = B M _ { 1 }$ 2OR BM .We further assume there was a 3 = 1 2super RFID reader which can cover the tag set $S _ { 1 } \cup S _ { 2 } ,$ and the bitmap of it is $B M _ { S }$ 1 2. In order to prove Lemma 2, we have to show that $B M _ { 3 } = B M _ { S }$ .

For any bit $B M _ { 3 } [ k ]$ in $B M _ { 3 }$ =,

$$
\begin{array}{l} B M _ {3} [ k ] = 1 \iff B M _ {1} [ k ] = 1 \vee B M _ {2} [ k ] = 1 \\ \Longleftrightarrow \exists t _ {i} \in S _ {1}, H (i) = k \\ \forall \exists t _ {i} \in S _ {2}, H (i) = k \\ \Longleftrightarrow \exists t _ {i} \in S _ {1} \cap S _ {2}, H (i) = k \\ \Longleftrightarrow B M _ {S} [ k ] = 1 \\ \end{array}
$$

Similarly, $B M _ { 3 } [ k ] = 0 \Longleftrightarrow B M _ { S } [ k ] = 0$ . Therefore, $B M _ { 3 } = B M _ { S }$ holds.

3 =We further have,

Lemma 3.3: Suppose tag sets $S _ { 1 } , S _ { 2 } , . . . , S _ { m }$ are in the vicinities of m readers $r _ { 1 } , r _ { 2 } , . . . , r _ { m }$ 2respectively. They 1 2share common members. The estimator n of the merged ˜bitmap equals to the estimation result of tag set $S _ { 1 } \cup$ $S _ { 2 } \cup \ldots \cup S _ { m }$ .

2The proof of Lemma 3.3 is similar to that of Lemma 3.2.

Theorem 3.4: Estimator 1 is a replicate-insensitive estimation in multi-reader scenarios.

Proof: As stated by Lemma 3.3, the estimator n equals to the estimation of tag set $S _ { 1 } \cup S _ { 2 } \cup \ldots \cup S _ { m }$ . Since every ID in tag set $S _ { 1 } \cup S _ { 2 } \cup \ldots \cup S _ { m }$ is distinct, 1 2Estimator 1 eliminates all the replicates. □

Before the idea can be implemented, however, some issues must be addressed. Note that the assumption we give for $H ( k e y )$ to be uniformly distributed does not ( )always hold in real circumstances. Since normally the hash values will have an uneven distribution depending on the tag set under estimation. Therefore, we provide the standard error for Estimator 1 by theoretical analysis. Here the standard error means the standard deviation of the ratio $\tilde { n } / n$ .

From Lemma 3.1, we know that

$$
E (V _ {0}) = l e ^ {- n / l}
$$

Hence,

$$
V a r (V _ {0}) = E \left(V _ {0} ^ {2}\right) - E \left(V _ {1} ^ {2}\right) = l e ^ {- n / l} \left(1 - (1 + n / l) e ^ {- n / l}\right)
$$

Then we obtain the standard error,

$$
S t d (\tilde {n} / n) = \sqrt {V a r (\tilde {n} / n)} = \frac {\sqrt {m} (e ^ {- n / l} - n / l - 1) ^ {1 / 2}}{n}
$$

Table I provides the frame length l needed for estimation the number of tags with a standard error less than 10%.

TABLE I FRAME LENGTH NEEDED FOR STANDARD ERROR OF 10% 

<table><tr><td>N</td><td>100</td><td>500</td><td>1000</td><td>5000</td><td>10000</td><td>50000</td></tr><tr><td>Frame Length</td><td>80</td><td>172</td><td>268</td><td>948</td><td>1709</td><td>6909</td></tr></table>

As shown in Table I, the optimal frame length increases with the cardinality of tag set. As the total number of tags is unknown, the length will be initially set to be a small value. If the readers realize that too many collisions happen in the frame, they should extend the frame, e.g., double the length, then retransmit. Such process has to repeat in order to get an optimal frame size for estimation. The same problem happens in existing estimation algorithms such as USE and UPE [14]. As analyzed by the authors, to get an accurate estimation of 500 tags by UPE, the length of frame needed is 180. Using USE, the number even increases to about one thousand. Both of retransmissions and the large frame size enlarge the processing time and communication overhead.

In our design, LoF employs the hash functions with geometric distribution rather than uniform distribution. Taking the advantage of this kind of hash functions, LoF has fixed and short frame length so as to reduce the latency and communication overhead in finalizing an optimal frame length.

# IV. THE DESIGN OF LOF ALGORITHM

In this section, we provide our replicate-insensitive estimation algorithm Lottery Frame (LoF), which combines LPE with geometric distribution, thus saving the processing time and communication overhead compared with USE, UPE and LPE.

# A. Geometric Distribution and GD Galton Board

By modifying the famous statistical device Galton Board [20], we build a machine Geometric Distribution Galton Board (GD-Galton Board) to simulate the geometric distribution. For easy to understand, let us see the example in Fig. 3(a), where we drop balls into Galton board. Each time when a ball hits one of the nails, it can bounce right or left with 50% probability respectively. If the number of balls is sufficiently large, the heights of the ball heaps will approximately be a normal distribution. If we revise the structure of the device as shown in Fig. 3(b), by hitting a nail, a ball has 50% probability to drop into the right side slot, and 50% probability to bounce left. As a result, if the number of balls is sufficiently large, the heights of the ball heaps will follow geometric distribution, i.e., $1 / 2 ^ { t }$ of the balls are in the tth slot. 1 2Imagine the ball heaps as a bitmap, we can point out three parts: the suffix of ones, the prefix of zeros and the fringe consists zeros and ones. Statistically, more balls drop, more left the fringe will be. Therefore, the position of fringe can be used to estimate the number of balls.

![](images/e74226a651c3f61ac7ecea8eecfc91fb33a520bb5fcf71b7b4d7e397c1d3dabe.jpg)  
Fig. 3. Galton Board and GD-Galton Board

# B. The General Protocol

In the rules of lotteries, it is very easy for a player to win a small prize, while winning a higher class of prize needs really good luck. Good lucks are rare, so we are able to estimate the number of tickets a player bought based on the prizes he wins. Suppose a lottery has several classes of prizes. If the player wins quite a lot different high classes of prizes, we can guess that he bought a great number of tickets.

Inspired by such life experiences, we design our replicate-insensitive estimation algorithm LoF. We design a lottery-style game using GD-Galton board. Every RFID tag can be considered as a lottery ticket, and the ticket number is the tag ID. To determine which kind of prize the ticket wins, the tag drops a ball into GD-Galton board. The more left slot the ball stands in, the higher prize it wins. Here the GD-Galton board actually plays the role as a geometric distribution hash function $H ( )$ . We estimate the cardinality based on the position of fringe in GD-Galton board.

![](images/1e0097b51b1b6930009ec0abc3f67653cf55a761e47d0ae59bc0b215e04a4c6d.jpg)  
Fig. 4. Pseudocode of LoF

1) Tag: When probed by a reader in the estimation process, the tag applies the hash function to its ID and responds in a time slots according to the result, i.e., the prize it wins. The simplest hash function with geometric distribution is,

H ID the position of least-significant (right-most) ( ) =bit of zero in binary representation of ID

For example, H =0 and H =2. Apparently, 50% of the IDs are hashed to slot 0, because the least-significant bit (bit 0) has 50% probability to be zero. Also, it can be easily proved that $1 / 2 ^ { t }$ of the IDs are hashed to the slot t .

1To make the implementation convenient, we just write the value H ID onto the tags in production. The ( )penalty is only a little extra memory to store H ID ( )as the string of H ID is much shorter than that of ID. ( )Since LoF may use multiple hash functions to increase the accuracy as we will discuss in the next part, a tag using LoF has to attach multiple values in its memory, and selects one of them upon the request of the reader. Finally, tags respond readers by a short message without any identifiable information.

The distributed LoF algorithm for tags is formally described in Fig. 4(a).

2) Reader: In LoF, readers use a slotted ALOHA model. Each reader also generates a bitmap at each round of communication. The positions of the bitmap correspond to time slots of the ALOHA frame. After hearing the tag responses, every reader should report its bitmap to a specific server. For LoF, readers should know the number of hash functions used, but the length of frame is fixed. We illustrate our distributed algorithm for readers in Fig. 4(b).

3) Server: We should expect, if there are n tags, approximately $n / 2$ of the responses are in time slot 0, approximately $n / 4$ of the responses are in time slot 1and $1 / 2 ^ { t }$ 4of the responses are in time slot $t - 1$ . Thus, by 1 2 1merging the bitmaps by OR operation, the kth bit in bitmap $B M [ k ]$ will be zero if $k \gg l o g _ { 2 } n$ , or be one if $k \ll l o g _ { 2 } n$ [ ] 2. The fringe consists zeros and ones for the k 2whose value is near $l o g _ { 2 } n$ .

2By modifying a theorem suggested by Flajolet and Martin [19], we have the following Lemma which offers a relationship between the position of fringe in bitmap BM and the total number of tags n.

Lemma 4.1: Suppose R is the right most zero in BM, i.e. ${ \cal R } = \mathrm { m i n } \{ i | B M [ i ] = 0 \}$ . The expected value of R =satisfies

$$
E (R) = \log_ {2} (\varphi n) + P (\log_ {2} n) + o (1) \tag {5}
$$

where the constant $\varphi ~ = ~ 0 . 7 7 5 3 5 1 . . .$ . and $P ( u )$ is a = 0 775351 ( )periodic and continuous functions of u with period 1 and amplitude bounded by $1 0 ^ { - 5 }$ .

10Lemma 4.1 was proven in [19]. Omitting the term $P ( \log _ { 2 } n ) + o ( 1 )$ , and replacing n and $E ( R )$ by their (log2 ) + (1) ( )representations in terms of observed variables n and $R ,$ we obtain,

Estimator 2. n is an estimator of the tag number $n ,$ where

$$
\tilde {n} = 1 / \varphi \times 2 ^ {R} = 1. 2 8 9 7 \times 2 ^ {R} \tag {6}
$$

Formula (6) also justifies the statement we suggested that the fringe consists zeros and ones for the bit k whose value is near $\log _ { 2 } n$ . Moreover, since tags use log2hash function to select time slots for responding, the LoF algorithm is also replicate-insensitive in multi-reader RFID systems.

Theorem 4.2: LoF is a replicate-insensitive estimation in multi-reader scenarios.

The proof is same as that of Theorem 3.4.

The following theorem shows that using geometric distribution hash functions, LoF has the advantage of fixed and short frame length.

Theorem 4.3: A frame with N slots is sufficient log2for the estimation algorithm using geometric distribution hash functions, where N is the number of all the same series tags in production.

Proof: Clearly, the number of tags currently under estimation follows $n < N$ . We know that $1 / 2 ^ { t }$ of the n tags response to the time slot t − . Let $t = \log _ { 2 } N$ . We have,

$$
n \times \frac {1}{2 ^ {\log_ {2} N}} <   n \times \frac {1}{2 ^ {\log_ {2} n}} = 1
$$

which implies the time slot $\log _ { 2 } N - 1$ has no responses, and those slots for which $t > \log _ { 2 } N$ are also empty. Therefore, $\log _ { 2 } N$ slots are sufficient for LoF estimation.

![](images/60893bc28bba5095e8f2af7b792f3298e48ac7ff9244e5698be25ea5de3f885e.jpg)

Suppose there are totally 50000 tags produced. According to Theorem 3, we only have to fix the length of ALOHA frames as $\log _ { 2 } 5 0 0 0 0 = 1 5 . 6 0$ . Compared log2 50000 = 15 60with hundreds and thousands time slots needed for USE, UPE and Estimator 1, LoF evidently saves the processing time. Moreover, there is no constraint of operation range for LoF. Using frames with fixed length of 16, LoF can estimate the number of tags up to 50000. Hence, LoF is highly scalable.

# C. Multiple Hash Functions

Based on the analysis in [19], we may also derive the standard deviation of the geometric distributed bitmap counting as the following theorem.

Theorem 4.4: Suppose R is the position of the right most zero in BM . The standard deviation of R satisfies

$$
\sigma_ {n} ^ {2} = \sigma_ {\infty} ^ {2} + Q (\log_ {2} n) + o (1) \tag {7}
$$

where the constant $\sigma = 1 . 1 2 1 3 . . .$ . and $Q ( u )$ is a periodic functions of u with mean value 0 and period 1.

An error with approximately 1.12 bit might be acceptable for some applications, e.g., to realize the size of the tag set for tag identification. It is however too high for many other applications. Luckily, the estimator used in LoF algorithm is an unbiased estimator. In that sense, if we make several independent estimations and compute the average result, the standard deviation will be significantly reduced. In LoF algorithm, we can employ a set of m independent hash functions. The readers should generate m bitmaps by all of the hash functions. Then LoF has m bitmaps and compute m positions of the right most zero $R _ { 1 } , R _ { 2 } , . . . , R _ { m }$ . Consider the average value

$$
\bar {R} = (R _ {1} + R _ {2} + \ldots + R _ {m}) / m
$$

The variable $\bar { R }$ has the expectation and standard deviation that satisfy

$$
E (\bar {R}) \approx \log_ {2} (\varphi n), \sigma (\bar {R}) \approx \sigma_ {\infty} / \sqrt {m}
$$

Therefore, the improved estimator is

$$
\tilde {n} = 1. 2 8 9 7 \times 2 ^ {R} = 1. 2 8 9 7 \times 2 ^ {\sum_ {i} R _ {i} / m} \tag {8}
$$

Table II lists the standard error in terms of the number of independent hash functions.

TABLE II STANDARD ERROR FOR MULTIPLE HASH FUNCTIONS 

<table><tr><td>M</td><td>1</td><td>2</td><td>4</td><td>8</td><td>16</td><td>32</td><td>128</td></tr><tr><td>Std Error</td><td>117%</td><td>73%</td><td>47%</td><td>32%</td><td>20%</td><td>15%</td><td>7%</td></tr></table>

# D. Comparison with other Methods

We summarize LoF in applicability, processing time, communication overhead, space and computation complexity. In multi-reader scenarios, LoF can support replication-insensitive estimation. Assume the number of readers is constant. According to Theorem 4.3, for each communication round the length of slotted ALOHA frame is O n . Employing multiple hash functions, the communication round will be a constant number based on the accuracy desired. Consequently for the entire LoF algorithm using multiple hash functions, the processing time is also O n . Readers and the server only have to store bitmaps with the same length as frames. Thus the space cost is also O n . The (log )complexity for computing the final result is O n , (log )because LoF should scan each bitmap to find the right most zero. For the fairness of comparison, we multiply the number of hash functions, k, to each value. Table III compares LoF with other four RFID tag counting approaches: identification (Iden), USE, UPE [14] and LPE.

TABLE III COMPARISON OF COUNTING/ESTIMATION SCHEMES 

<table><tr><td></td><td>Repli.-insen.</td><td>Frame Length</td><td>Process Time</td><td>Space</td><td>Comp.</td></tr><tr><td>Iden</td><td>YES</td><td> $O(n)$ </td><td> $O(n^{2})$ </td><td> $O(n \log n)$ </td><td> $O(n \log n)$ </td></tr><tr><td>USE</td><td>NO</td><td> $O(n)$ </td><td> $O(n \log n)$ </td><td> $O(n)$ </td><td> $O(n)$ </td></tr><tr><td>UPE</td><td>NO</td><td> $O(n)/p$ </td><td> $O(n \log n)$ </td><td> $O(n)$ </td><td> $O(n)$ </td></tr><tr><td>LPE</td><td>YES</td><td> $O(n)$ </td><td> $O(n \log n)$ </td><td> $O(n)$ </td><td> $O(n)$ </td></tr><tr><td>LoF</td><td>YES</td><td> $O(k \log n)$ </td><td> $O(k \log n)$ </td><td> $O(k \log n)$ </td><td> $O(k \log n)$ </td></tr></table>

# V. PERFORMANCE EVALUATION

In this section, LoF is evaluated through comprehensive simulations. First we describe the simulation setup, and address the schemes and performance metrics we evaluate. We then provide the simulation results for both single-reader and multi-reader scenarios.

# A. Simulation Methodologies and Performance Metrics

In our simulator, the interrogation range of each reader is set to be circular with the same radius. We assume that there is no transmission loss between tags and readers. Readers are capable to detect if there is idle, single reply or collision in any frame slot. In case there are multiple readers, at most one reader is operating at any time. Each tag is engineered to have globally unique IDs and a set of pre-computed 32-bit hash values. In LoF, they are able to pick the right hash values for frame slot selection.

We compare the estimation schemes in two scenarios: single-reader environment and multi-reader environment. For the single-reader environment, we contrast LoF with UPE, the main strategy in [14]. UPE does not support estimation in multi-reader environments, so we compare LoF with the two statistical values, MAX and SUM. Each reading in MAX and SUM is generated by UPE. Since the accuracy of LoF increases by adding more hash functions, we also evaluate the LoF protocol for different number of hash functions in both scenarios. Table IV shows the setup of our simulator. The simulation takes 100 runs with the same parameters, and we report the average.

TABLE IV SIMULATION SETUP 

<table><tr><td></td><td>Single-reader</td><td>Multi-reader</td></tr><tr><td>Schemes evaluated</td><td>LoF and UPE</td><td>LoF, MAX and SUM</td></tr><tr><td>Metrics</td><td>accuracy and latency</td><td>accuracy and latency</td></tr><tr><td>Tag size</td><td>50-50000</td><td>5000 and 50000</td></tr><tr><td>Number of readers</td><td>1</td><td>4</td></tr><tr><td>Terrain</td><td>N/A</td><td>100 x 150 rectangular</td></tr><tr><td>Interrogation range</td><td>infinite</td><td>50-70</td></tr><tr><td>Repeating times</td><td>100</td><td>100</td></tr></table>

The estimation accuracy is illustrated in terms of error and normalized variance. Suppose the actual cardinality is n and the estimated value is n. Error and normalized variance are defined as

$$
E r r o r = \frac {| \tilde {n} - n |}{n}
$$

$$
N o r V a r = \frac {1}{1 0 0} \sum {\frac {| \tilde {n} - n |}{n}}
$$

Ideally, the error should be 0. The closer the error to 0, the better the estimation is.

Another metric we concern is latency. Tag cardinality estimation requires several transmission rounds among readers and tags. For each round, readers take a number of time slots according to frame length. We abstract the estimation time as the total number of frame slots of the whole process.

![](images/9eb6a3da689e174020b968e789a2c716733bc2e79cd50dfda2a5be3e7c83e9dd.jpg)



Fig. 5: Accuracy Comparison in Single-reader Context   
![](images/8e770fa179313b10b9ab2e6e2ee4ad6750035938daa13330a8a241858f23d563.jpg)



Fig. 7: Normalized Standard Deviation for LoF with Multiple Hashes   
![](images/c1512ea00b8941a7f026cde7ac3f063daec19941c8bad6da969b6942baca7353.jpg)



Fig. 9: Accuracy Comparison in Multi-reader Context (5000 tags)

# B. Single-reader Scenario

Figure 5 plots the estimation accuracy of LoF and PUE. With more hash functions used in cardinality estimation, the error reduces. Employing 16 hash functions, the error is down to less than 0.04, i.e. 4% deviation from the actual cardinality. The change of actual tag size has no significant effect to LoF. In other words, the same frame length is suitable for a wide range of tag size. For UPE, the error is always greater than 0.80.

![](images/d795a3ffd42a5c5bbaf1e25e24d31d8cb94ea351ffb64fbd6cb5641e00060dd8.jpg)



Fig. 6: Standard Deviation for LoF with Multiple Hashes   
![](images/6dfe1ced05bd7295ba61dd4e65bbe961e81f7124e7a5ebfb43e02562691c657c.jpg)



Fig. 8: Simulation Model

![](images/a3e76c254f142fcad6b0725fbf212b47d98bb0fa7ac8b44c038573fc2f2bf5df.jpg)



Fig. 10: Accuracy Comparison in Multi-reader Context (50000 tags)

We are also interested in the accuracy distribution in each simulation. Figure 6 and 7 show the standard deviation and normalized standard deviation of estimation accuracy of LoF. When more hash functions are used in the estimation, the standard deviation of the estimation drops. Employing 16 hash functions, the normalized standard deviation is not more than 0.30. The number of tags affects little on the variation as illustrated in Fig. 7.

LoF employs fixed frame length. Therefore, independent on the actual tag cardinality, the total number of time slots required is equal to the frame length multiplied by the number of hash functions, i.e., m in our simulation as shown in Table V. On the other hand, Table VI shows that the frame slot requirement of UPE depends on the actual tag cardinality, which is relatively long. Besides, without prior knowledge of the approximate cardinality order, UPE suffers from huge expense in finalizing an optimal length.

TABLE V REQUIRED TIME SLOT NUMBER FOR LOF 

<table><tr><td>Number of Hashes</td><td>1</td><td>2</td><td>4</td><td>8</td><td>16</td><td>32</td></tr><tr><td>Time Slots</td><td>32</td><td>64</td><td>128</td><td>256</td><td>512</td><td>1024</td></tr></table>

TABLE VI REQUIRED TIME SLOT NUMBER FOR UPE

<table><tr><td>Number of Tags</td><td>50</td><td>500</td><td>5000</td><td>10000</td><td>30000</td><td>50000</td></tr><tr><td>Time Slots</td><td>62</td><td>461</td><td>3215</td><td>4570</td><td>11045</td><td>23291</td></tr></table>

Compared with UPE, LoF provides tunable estimation accuracy with expense on estimation time and frame slots requirements. Also, users are capable to predict the number of time slots required.

# C. Multi-reader scenario

We then consider multiple readers which have overlapping interrogation regions. Different number of tags (5000 and 50000) is randomly distributed in a 100 units x 150 units rectangular terrain. The terrain is covered by four readers which are located near the corners. The reading range is varying between 50 and 70 units. The simulation model is shown in Fig. 8.

Figure 9 and 10 provide the accuracy of LoF, MAX and SUM in multi-reader environment, where each reading in MAX and SUM is generated by UPE. They indicate that MAX and SUM estimators perform poorly in cardinality estimation no matter which single reader algorithm is used. These estimations are affected by multiple factors including but not limited to the number of readers, the interrogation range and reader deployment. Estimations by MAX are usually well-below the actual cardinality while those by SUM are always multiple times of the actual number of tags. As shown in Fig. 9, when the interrogation range grows, the error of MAX becomes lower and SUM goes further beyond accurate, because longer interrogation range will cause more overlapping areas. The cardinality estimation from merged bitmaps of every LoF reader provides the highest accuracy. When only 16 hash functions are used, the estimation error is already less than 4%. The estimation error is within 2% when 64 hash functions are used. Comparing Fig. 9 and Fig. 10, we again find that the number of tags has no significant impact on accuracy of LoF.

TABLE VII REQUIRED TIME SLOT NUMBER FOR LOF 

<table><tr><td>Number of hashes</td><td>1</td><td>4</td><td>16</td><td>32</td><td>64</td></tr><tr><td>Time Slots</td><td>128</td><td>512</td><td>2048</td><td>4096</td><td>8192</td></tr></table>

TABLE VIII REQUIRED TIME SLOT NUMBER FOR UPE 

<table><tr><td></td><td colspan="3">5000 tags</td><td colspan="3">50000 tags</td></tr><tr><td>Range</td><td>50</td><td>60</td><td>70</td><td>50</td><td>60</td><td>70</td></tr><tr><td>Time Slots</td><td>3600</td><td>3600</td><td>3630</td><td>33291</td><td>50370</td><td>71250</td></tr></table>

Table VII and Table VIII show the frame slot requirements for LoF and PUE scheme. The results are similar to the single reader case.

# VI. RELATED WORK

To improve the coverage in large-scale RFID systems, multiple readers are often deployed in the region of interest. In a recent work [16], the author analyzed three types of collisions in multi-reader environment: tag-tag collision, reader-tag collision and reader-reader collision. The work focuses on mitigating reader-tag and readerreader collisions. In our work, the term collision only refers to tag-tag collision. We assume no collisions in the other two types.

The existing RFID identification algorithms can be classified into two main categories based on which anti-collision scheme they use. The first type of RFID identification algorithms uses Aloha-based anti-collision schemes [11]. By employing such schemes, the reader creates a frame with a certain number of time slots, and then adds the frame length into the interrogation message sent to tags nearby. Each tag who receives the message randomly picks a time slot to transmit back. Since collisions in a same slot possibly happen and only the tags which transmit to slots without collision can be recognized, the reader has to keep sending requests until each of the tags is identified at least once. The other type of identification algorithms perform anti-collision by Tree-based or Binary Splitting schemes [12] [13]. Using Tree-based schemes, in each round, reader splits the set of tags into two subsets and labeled them by binary numbers. The reader repeats such process until each subset has only one tag. Thus the reader is able to identify all tags. The common drawback of these two types is the relatively long identification time.

To speed-up the identification protocols, Floerkemeier [15] suggests estimating the cardinality of tags based on the number of idle slots in current frame. A Bayesian probability estimation is used to maximize throughput. The most recent RFID tag estimation algorithms Unified Simple Estimator (USE) and Unified Probabilistic Estimator (UPE) are proposed by Kodialam and Nandagopal [14]. In USE, the authors proposed three estimators and analyzed their operating range and accuracy. Moreover, UPE employs the probabilistic framed ALOHA protocol to further mitigate the limitation that the operating range of a frame is dependent on the frame size. Nevertheless, as analyzed in section III-B, such a limitation still exists. Besides, USE and UPE are vulnerable to multiple-reading because they support no schemes that can eliminate the replicate information.

# VII. CONCLUSIONS

Counting the number of tags is a crucial task in large-scale RFID systems. In this work, we propose LoF, a replicate-insensitive estimation protocol that can eliminate multiple-readings. Our theoretical analysis and simulation results show that LoF can achieve accurate estimation in both single-reader and multi-reader environments, and significantly reduce the counting latency and communication overhead. We are also planning to explore more practical issues in multi-reader RFID systems, such as efficient identification, object tracking, as well as authentication. Indeed, this design can be easily extended to other fields, e.g., wireless sensor networks.

# VIII. ACKNOWLEDGEMENT

This work is supported in part by the Hong Kong RGC grants HKUST6183/06E, HKUST6169/07E, and HKBU 1/05C, the National High Technology Research and Development Program of China (863 Program) under grant No. 2007AA01Z180, the National Basic Research Program of China (973 Program) under grant No. 2006CB303000, NSFC Key Project grant No. 60533110, and the HKUST Nansha Research Fund NRC06/07.EG01.

# REFERENCES

[1] K. Finkenzeller, RFID Handbook: Radio-Frequency Identification Fundamentals and Applications. John Wiley & Sons, 2000.   
[2] L. M. Ni, Y. Liu, Y. C. Lau, and A. Patil, “LANDMARC: Indoor Location Sensing Using Active RFID,” in Proceeding of the first IEEE International Conference in Pervasive Computing and Communications (PerCom), 2003.

[3] A. Ranganathan, J. Al-Muhtadi, S. Chetan, R. Campbell, and M. D. Mickunas, “MiddleWhere: A Middleware for Location Awareness in Ubiquitous Computing Applications, in Proceeding of the 5th International Middleware Conference (Middleware), 2004.   
[4] D. Zhang, J. Ma, Q. Chen, and L. M. Ni, “An RF-based System for Tracking Transceiver-free Objects,” in Proceeding of the Fifth IEEE International Conference in Pervasive Computing and Communications (PerCom), 2007.   
[5] Y. Liu, L. Chen, J. Pei, Q. Chen, and Y. Zhao, “Mining Frequent Trajectory Patterns for Activity Monitoring Using Radio Frequency Tag Arrays,” in Proceeding of the Fifth IEEE International Conference in Pervasive Computing and Communications (PerCom), 2007.   
[6] G. Avoine and P. Oechslin, “A Scalable and Provably Secure Hash-Based RFID Protocol,” in Proceeding of PerCom Workshops, 2005.   
[7] R. Want, “An Introduction to RFID Technology,” IEEE Pervasive Computing, vol. 5, pp. 25- 33, 2005.   
[8] I. Chlamtac, C. Petrioli, and J. Redi, “Energy-conserving access protocols for identification networks,” IEEE/ACM Transactions on Networking (TON), vol. 7, pp. 51-59, 1999.   
[9] J. Lee, T. Kwon, Y. Choi, S. K. Das, and K.-a. Kim, “Analysis of RFID anti-collision algorithms using smart antennas,” in Proceeding of the 2nd International Conference on Embedded Networked Sensor Systems (SenSys), 2004.   
[10] V. Namboodiri and L. Gao, “Energy-Aware Tag Anti-Collision Protocols for RFID Systems,” in Proceeding of the Fifth IEEE International Conference in Pervasive Computing and Communications (PerCom), 2007.   
[11] L. G. Roberts, “Aloha Packet System with and without Slots and Capture,” ACM SIGCOMM Computer Communication Review, vol. 5, pp. 28-42, 1975.   
[12] J. I. Capetanakis, “Tree algorithms for packet broadcast channels,” IEEE Trans. on Information Theory, vol. IT-25, pp. 505- 515, 1979.   
[13] J. Myung and W. Lee, “Adaptive Splitting Protocols for RFID Tag Collision Arbitration,” in Proceeding of International Symposium on Mobile Ad Hoc Networking and Computing (Mobi-Hoc), 2006.   
[14] M. Kodialam and T. Nandagopal, “Fast and Reliable Estimation Schemes in RFID Systems,” in Proceeding of the Twelfth Annual International Conference on Mobile Computing and Networking (Mobicom), 2006.   
[15] C. Floerkemeier, “Transmission control scheme for fast RFID object identification,” in Proceeding of PerCom Workshops, 2006.   
[16] Z. Zhou, H. Gupta, S. R. Das, and X. Zhu, “Slotted Scheduled Tag Access in Multi-Reader RFID Systems,” in Proceeding of the fifteenth IEEE International Conference on Network Protocols (ICNP), 2007.   
[17] A. D. Joseph, A. R. Beresford, J. Bacon, et al, “Intelligent Transportation Systems,” IEEE Pervasive Computing, vol. 5, pp. 63-67, 2006.   
[18] K.-Y. Whang, B. T. Vander-Zanden, and H. M. Taylor, “A Linear-Time Probabilistic Counting Algorithm for Database Applications,” ACM Transactions on Database Systems, vol. 15, pp. 208-229, 1990.   
[19] P. Flajolet and G. N. Martin, “Probabilistic Counting Algorithms for Data Base Applications,” Journal of Computer and System Science, vol. 31, 1985.   
[20] V. V. Kozlov and M. Y. Mitrofanova, “Galton Board,” Regular Chaotic Dynamics, vol. 8, pp. 431-439, 2002.