# Verifiable Private Multi-party Computation: Ranging and Ranking

Lan Zhang∗, Xiang-Yang Li,†, Yunhao Liu,‡§, Taeho Jung,†

∗ Department of Computer Science and Technology, TNList, Tsinghua University

† Department of Computer Science, Illinois Institute of Technology

‡ School of Software, Tsinghua University and MOE Key Lab for Information System Security

§ Department of Computer Science and Engineering, HKUST

Abstract—The existing work on distributed secure multi-party computation, e.g., set operations, dot product, ranking, focus on the privacy protection aspects, while the verifiability of user inputs and outcomes are neglected. Most of the existing works assume that the involved parties will follow the protocol honestly. In practice, a malicious adversary can easily forge his/her input values to achieve incorrect outcomes or simply lie about the computation results to cheat other parities. In this work, we focus on the problem of verifiable privacy preserving multiparty computation. We thoroughly analyze the attacks on existing privacy preserving multi-party computation approaches and design a series of protocols for dot product, ranging and ranking, which are proved to be privacy preserving and verifiable. We implement our protocols on laptops and mobile phones. The results show that our verifiable private computation protocols are efficient both in computation and communication.

Index Terms—Verifiability, Privacy, Multi-party Computation, Ranking, Ranging, Dot Product.

# I. INTRODUCTION

Privacy preserving multi-parity computation is widely used in different areas. For example, similarity calculation in social networks [8], private voting and auction [9], private data aggregation in sensor networks [6], [7], [12], [17], ranking [10] and oursourced computation [14], [19]. A trusted central server is a simple way to address this problem. The trusted central server will collect the private inputs of all parties, compute the result and disseminate the result to required parties through the secure communication channel. However the server may not always be accessible for all users due to the absence of Internet connection or server failure. Frequent communications with server will cause high expense and security vulnerability. Recently the cracking of databases of some famous online sites causes severe leakage of users’ privacy. As a result, many users may not want to reveal their private data even to a server, which also hinders the wide adoption of cloud computing. So there is a strong motivation to design distributed privacy preserving multi-party computation protocols. Note that theoretically, this has been addressed by Secure Multiparty Computation (SMC), which was first introduced in [15]. SMC enables parties to jointly compute a function over their individually held private inputs without any party learning information beyond what can be deduced from the result.

Although theoretically beautiful, generic SMC protocols are extremely expensive. Many successive work, like [3] and [8], provide practical solutions for private multi-parity computation (e.g. set intersection, dot product) based on homomorphic encryption and secret sharing. These existing approaches concentrate on the privacy protection, while the verifiability of user inputs and outcomes are neglected. The correctness of most protocols is based on the assumption that the involved parties will follow the protocol honestly. In practice a malicious adversary may simply forge his/her input value to produce an incorrect result or lie about the outcome of computation [2]. In this way, the malicious adversary can cheat other parties to accept the incorrect result and even compromise other parties’ privacy. For example, in a social networking system, an unverifiable private similarity calculation protocol may allow a malicious user to get others’s trust by inputting fake attributes or lying about similarity calculation results.

In this work, we focus on the important but neglected problem of verifiable private multi-party computation in an insecure environment without a long-term trustable server. The computation is conducted in a distributed manner, and a trusted server is only occasionally contacted to authenticate the inputs of users. Specifically, we discover two potential attacks on existing protocols for private multi-party computation. We then design verifiable private multi-party threshold-based ranging protocols and ranking protocols suitable for different applications. We prove that these protocols are privacy preserving and verifiable for both input and output values. We thoroughly analyze the performances of our protocols and evaluate them with implementations on laptops and mobile phones. Most of our protocols cost less than 0.5 second on both laptop and mobile phone. Our most expensive protocol (verifiable twoway ranging) takes only 2.56 seconds on laptop and 3.22 seconds on mobile phone, and the largest message size is 3.5 KB. The results show that our verifiable protocols are efficient in both computation and communication.

Paper Organization: The rest of the paper is organized as follows. We define our problem and present the adversary model in Section II. In Section III and Section IV, we respectively present our verifiable private multi-party computation protocols for threshold-based ranging and ranking. We report our analysis and evaluation results in Section V, review the related work in Section VI, and conclude the paper in Section VII.

TABLE I THE FAST VARIANT OF PAILLIER’S CRYPTOSYSTEM 

<table><tr><td>Choose two prime numbers p and q.</td></tr><tr><td>Public key:modulus n = pq and base g ∈ Zn2*</td></tr><tr><td>Private key:λ = LCM(p-1,q-1)</td></tr><tr><td>Encryption:c = E(m,r) = gm+nr mod n2</td></tr><tr><td>Decryption:m = D(c) = L(cλ mod n2/L(gλ mod n2) mod n, L(x) = x-1/n</td></tr><tr><td>Homomorphic:E(m1,r1)E(m2,r2) mod n2 = E(m1+m2,r1+r2) mod n2E(m1,r1)m2 mod n2 = E(m1m2,r1m2) mod n2</td></tr><tr><td>Self-blinding:D(E(m1,r1)) = E(m1,r1+r2)</td></tr></table>

# II. PROBLEM DEFINITION AND PRELIMINARY A. Verifiable Private Multi-party Computation

There are n parties $P = \{ P _ { 1 } , \ldots , P _ { n } \}$ , where each party $P _ { i }$ holds a private value $\mathrm { \Delta } v _ { i } . \mathrm { \Delta } n$ parties wish to compute $f ( v _ { i } , v _ { 2 } , \ldots , v _ { n } ) \ = \ ( y _ { 1 } , y _ { 2 } , \cdot \cdot \cdot , y _ { n } )$ by communicating among themselves, without giving away any information about their own values. We say a multi-party computation protocol is verifiable, if a malicious party cannot cheat other parties to accept an incorrect result. The verifiability of the computation result is usually neglected in existing protocols. In this work, we focus on the verifiable private computation which resists forged inputs and manipulation of computation results as well as preserves the privacy of input values.

# B. Homomorphic Encryption

Homomorphic encryption allows specific types of computations to be carried out on cipher text and obtains an encrypted result which is the cipher text of the computation result of the plain text. In this work, we use the fast variant of Paillier’s cryptosystem which is additively homomorphic as an example. The detail is presented in Table I.

Let the public key of the user $P _ { i }$ be $P k _ { i }$ and the private key be $S k _ { i }$ . We denote the encryption with $P _ { i } ^ { \cdot } \mathrm { s }$ public key as $\mathrm { E } _ { P k _ { i } } ( \cdot )$ , encryption with private key as $\operatorname { E } _ { S k _ { i } } ( . )$ . Similarly, $\mathrm { D } _ { P k _ { i } } ( \cdot )$ and $\mathrm { D } _ { S k _ { i } } ( \cdot )$ denote the decryption operations with $P _ { i } ^ { \cdot } \mathrm { { s } }$ keys. For simplicity, when no confusion caused, $\mathrm { E } _ { i }$ stands for $\mathrm { E } _ { P k _ { i } }$ and $\mathrm { D } _ { i }$ stands for $\mathrm { D } _ { S k }$ using the Paillier’s cryptosystem.

# C. Adversary Models

Many attacks are extensively studied in related private multi-party computation work, e.g. [3], [8]. Here, we discover two potential attacks (the compressive sensing based privacy reconstruction and fake signature) to the state-of-art private multi-party computation schemes, which haven’t been well studied yet.

1) Compressive Sensing Based Privacy Reconstruction: In social networks, considering a user’s attributes or relationship as a vector, private dot product is a typical way for profile matching and proximity calculation. However, a user’s vector can be reconstructed via multiple rounds of proximity computation. Let $\mathbf { v _ { k } }$ be the M-dimension private attribute vector of a user. Each dot product result gives one linear constraint on $\mathbf { v } _ { \mathbf { k } } .$ . In a traditional way as stated in [2], an adversary needs M linearly independent constraints to reconstruct the victim’s private vector $\mathbf { v _ { k } }$ . Indeed, $\mathbf { v _ { k } }$ is usually K-sparse (it has at most $K$ non-zeros) and K - M. Based on the research in the compressive sensing [1], an adversary can recover the K-sparse length-M user private vector $\mathbf { v _ { k } }$ from only $R \ge c K \log ( M / K ) \ll M$ dot-products, here c is a small constant.

So we suggest that, to achieve privacy preserving dot product in sparse-vector systems like social networks, a protection is needed to resist o(K log M ) queries from the same user or a collusive attack of a group of adversaries.

2) Fake Signature: Most existing work of SMC are based on homomorphic encryption systems. Encrypted private values are input, and a series of computation are conducted homomorphically on these encrypted values to generate the encryption of the computation result on these values. A few methods like [2] propose to use a signature of encrypted input from a trusted third party $P _ { T }$ to ensure the authenticity and consistency of the input value. However, we find that if the trusted third party $P _ { T }$ directly signs the encrypted value $\operatorname { E } _ { i } ( v _ { i } )$ and the digital signature generation system are homomorphic, the party $P _ { i }$ is able to generate a fake signature for value $k \cdot v _ { i }$ or $v _ { i } ^ { k }$ without contacting $P _ { T }$ . Here k is a constant picked by $P _ { i }$ . As a result, $P _ { i }$ can use $k \cdot v _ { i }$ as the input of a multi-party computation for arbitrary k,to cheat other parties to believe an incorrect conclusion.

So we suggest to avoid using homomorphic encryption to directly sign the encrypt value in private multi-party computation.

In the following part of this paper, we will focus on the verifiable private multi-parity computation resisting the adversaries of fake input and outcome, which are ignored by most existing work.

# 3) Fake Input and Fake Outcome:

Definition 1 (Fake Input Adversary): In the private multiparty computation, an adversary cheats by inputting an arbitrary value to deviate the result from its true value.

Definition 2 (Fake Outcome Adversary): In the private multi-party computation, a malicious party knowing the true result tells a wrong conclusion to trick other parties.

# D. Certificate

In this work, we suppose that there is a trusted third party $P _ { T }$ who is only involved to authenticate the input values of participants. So there is no requirement for long-term involvement by $P _ { T }$ . Each participant ${ \mathrm { \bar { \it P } } } _ { i }$ can contact $P _ { T }$ to authenticate his/her encrypted values. $P _ { T }$ signs the authenticated values and hands $P _ { i }$ his/her certificate consisting the following content and other information in a typical certificate:

$$
\mathbf {C} (P _ {i}, v _ {i}) = \langle \operatorname{Sig} (I D _ {i}), \mathrm{E} _ {P k _ {i}} (v _ {i}), \operatorname{Sig} (\mathrm{E} _ {P k _ {i}} (v _ {i})), P k _ {i}, P k _ {T} \rangle
$$

Note that the signature algorithm by the trusted authority is not homomorphic.

# Protocol 1: One-way Threshold-based Ranging Protocol

1) $P _ { 1 }$ sends $\operatorname { E } _ { 1 } ( \theta , r _ { 1 } )$ and the certificate ${ \bf C } ( P _ { 1 } , { \bf V } _ { 1 } )$ to $P _ { 2 }$ . E (Here certificate $\begin{array} { r l r } { \dot { \bf C } ( P _ { 1 } , { \bf V } _ { 1 } ) } & { { } = } & { \langle \mathrm { S i g } ( I D _ { 1 } ) , ~ \mathrm { E } _ { 1 } ( { \bf V } _ { 1 } , { \bf R } _ { 1 } ) } \end{array}$ , $\operatorname { S i g } ( \operatorname { E } _ { 1 } ( \mathbf { V } _ { 1 } , \mathbf { R } _ { 1 } ) ) , P \dot { k } _ { 1 } , P k _ { T } \dot { \mathbf { \gamma } }$ .   
2) $P _ { 2 }$ (E ( )) Trandomly picks a certificate $\mathbf { C } ( P _ { 2 } , \delta _ { 1 } \mathbf { V } _ { 2 } ) ,$ where $\begin{array} { r l r } { { \bf C } ( P _ { 2 } , \delta _ { 1 } { \bf V } _ { 2 } ) } & { { } \stackrel {  } { = } } & { \langle \mathrm { S i g } ( I D _ { 2 } ) , \quad \mathrm { E } _ { 2 } ( \delta _ { 1 } , r _ { 2 } ) , \quad \mathrm { E } _ { 2 } ( { \bf V } _ { 2 } , { \bf R } _ { 2 } ) } \end{array}$ , $\begin{array} { r } { \dot { \mathrm { E } _ { 2 } } ( \delta _ { 1 } \mathbf { V } _ { 2 } , \dot { \mathbf { R } _ { 2 } } ) , \qquad \mathrm { S i g } ( \bar { \mathrm { E } _ { 2 } } ( \delta _ { 1 } , r _ { 2 } ) ) } \end{array}$ E (, $\mathrm { S i g } \big ( \mathrm { E } _ { 2 } ( \delta _ { 1 } \dot { \bf V } _ { 2 } , { \bf R } _ { 2 } ) \big )$ , $P k _ { 1 } , P k _ { T } \rangle$ ) Sig(E ( )) Sig, and another arbitrary number $\delta _ { 2 } .$ ( )) For ranging Tcomputation, $P _ { 2 }$ computes

$$
\left\{ \begin{array}{l l} & e _ {1} = \mathrm{E} _ {1} (\delta_ {1} \mathbf {V} _ {1} \cdot \mathbf {V} _ {2} + \delta_ {2}, \delta_ {1} \mathbf {R} _ {1} \cdot \mathbf {V} _ {2} + r _ {2}), \\ & e _ {2} = \mathrm{E} _ {1} (\delta_ {1} \theta + \delta_ {2}, \delta_ {1} r _ {1} + r _ {2}) \end{array} \right.
$$

For verification purpose, $P _ { 2 }$ computes

$$
\left\{ \begin{array}{l l} & e _ {3} = \mathrm{E} _ {1} (\mathbf {R} _ {2} \cdot \mathbf {V} _ {1} + r _ {2}, \mathbf {R} _ {1} \cdot \mathbf {R} _ {2} + r _ {2}), \\ & e _ {4} = \mathrm{E} _ {1} (r _ {2} \theta + r _ {2}, r _ {1} r _ {2} + r _ {2}), \\ & e _ {5} = \mathrm{E} _ {2} (\delta_ {2}, r _ {2}), \end{array} \right.
$$

$P _ { 2 }$ sends $e _ { 1 } , e _ { 2 } , e _ { 3 } , e _ { 4 }$ to $e _ { 5 }$ and the certificate to $P _ { 1 \cdot }$

3) $P _ { 1 }$ compares $d _ { 1 } = \mathrm { D } _ { 1 } ( e _ { 1 } )$ and $d _ { 2 } = \mathrm { D } _ { 1 } ( e _ { 2 } )$ to determine the ranging result. $P _ { 1 }$ = D ( ) =verifies the value in $\mathbf { C } ( { \dot { P } } _ { 2 } , \mathbf { \dot { V } } _ { 2 } ) . { \mathbf { \nabla } } P _ { 1 }$ computes $d _ { 3 } { \bf \bar { \Psi } } = { \bf \bar { D } } _ { 1 } ( e _ { 3 } )$ and $d _ { 4 } ~ = ~ \mathrm { D } _ { 1 } ( e _ { 4 } )$ ( )to get the information of = D ( )random number, then $P _ { 1 }$ = D ( )computes and checks the equations:

$$
\left\{ \begin{array}{l l} & \mathrm{E} _ {2} (\delta_ {1} \mathbf {V} _ {1} \cdot \mathbf {V} _ {2} + \delta_ {2}, \mathbf {R} _ {2} \cdot \mathbf {V} _ {1} + r _ {2}) = \mathrm{E} _ {2} (d _ {1}, d _ {3}), \\ & \mathrm{E} _ {2} (\delta_ {1} \theta + \delta_ {2}, r _ {2} \theta + r _ {2}) = \mathrm{E} _ {2} (d _ {2}, d _ {4}). \end{array} \right.
$$

If they are not all true, P1 learns that $P _ { 2 }$ is cheating.

# III. VERIFIABLE THRESHOLD-BASED RANGING PROTOCOL

In this section, we present our two-party threshold-based ranging protocol which is the first privacy preserving ranging protocol supporting verifiability for both input and outcome.

First, we define the threshold-based ranging computation.

Definition 3 (Threshold-based Ranging): $P _ { 1 }$ holds private value $v _ { 1 }$ , and $P _ { 2 }$ holds private value $v _ { 2 }$ . There is a polynomial function $f ( v _ { 1 } , v _ { 2 } )$ and a threshold θ. Users $P _ { 1 }$ and $P _ { 2 }$ can only determine whether $f ( v _ { 1 } , v _ { 2 } ) > \theta$ or not.

In the verifiable private threshold-based ranging, only the 1-bit comparison result will be exposed to them. This computation can provide better privacy and be widely used in many applications, like [7], [12].

# A. Protocol Design

Our verifiable private threshold-based ranging computation is based on the following observation.

Theorem 1: Given a large integer n, two arbitrary positive numbers $\delta _ { 1 } , \delta _ { 2 } , ~ ( \delta _ { 1 } f ( v _ { 1 } , v _ { 2 } ) + \delta _ { 2 }$ mod $n ) ~ > ~ ( \delta _ { 1 } \theta + \delta _ { 2 }$ mod n) ⇔ $f ( v _ { 1 } , v _ { 2 } ) \ > \ \theta$ if $\delta _ { 1 } f ( v _ { 1 } , v _ { 2 } ) + \delta _ { 2 } \ \in \ [ 0 , n - 1 ]$ and $\delta _ { 1 } \theta + \delta _ { 2 } \in [ 0 , n - 1 ]$ .

Specifically, a party can choose $\delta _ { 1 } \leq \sqrt { n }$ and $\delta _ { 2 } \leq \sqrt { n } ,$ , if $f ( v _ { 1 } , v _ { 2 } ) \leq { \sqrt { n } } .$ .

1) One-way Protocol: We first consider the one-way situation that $P _ { 1 }$ wants to conduct the query, but $P _ { 2 }$ doesn’t need the result. Protocol 1 is the first verifiable private threshold-based ranging protocol. It uses a

# Protocol 2: Two-way Threshold-based Ranging Protocol

1) $P _ { 1 }$ sends $P _ { 2 }$ a randomly picked certificate $\mathbf { C } ( P _ { 1 } , \delta _ { 1 1 } \mathbf { V } _ { 1 } )$ .   
2) $P _ { 2 }$ computes $\operatorname { E } _ { 1 } ( \theta )$ by himself/herself.   
E ( )The rest of this step is same as Step 2 in Protocol 1, with the only difference that here we use $\delta _ { 2 1 }$ and $\delta _ { 2 2 }$ for $P _ { 2 } \mathrm { ^ { * } s }$ parameters.   
3) $P _ { 1 }$ compares $d _ { 1 } = \mathrm { D } _ { 1 } ( e _ { 1 } )$ and $d _ { 2 } = \mathrm { D } _ { 1 } ( e _ { 2 } )$ to determine the = D ( ) = D ( )ranging result, and verifies the result as in Step 3 in Protocol 1. If the verification fails, $P _ { 1 }$ learns that $P _ { 2 }$ is cheating and terminates the protocol. Otherwise, $P _ { 1 }$ computes

$$
\left\{ \begin{array}{l l} & m _ {1} = \mathrm{E} _ {2} (\delta_ {1 1} d _ {1} + \delta_ {1 2}), \\ & m _ {2} = \mathrm{E} _ {2} (\delta_ {1 1} d _ {2} + \delta_ {1 2}), \\ & m _ {3} = \mathrm{E} _ {1} (\delta_ {1 2}), \end{array} \right.
$$

and sends them to $P _ { 2 } .$ As in Protocol 1 the encrypted information for random numbers by $P k _ { 2 }$ are also sent to $P _ { 2 } .$ .

4) $P _ { 2 }$ can compare $d m _ { 1 } = \mathrm { D } _ { 2 } ( m _ { 1 } )$ and $d m _ { 2 } = \mathrm { D } _ { 2 } ( m _ { 2 } )$ to deter-=mine the ranging result. $P _ { 2 }$ ( ) = Dverifies the value in $\dot { \mathbf { C } } ( P _ { 1 } , \delta _ { 1 1 } \mathbf { V } _ { 1 } )$ , then $P _ { 2 }$ ( )decrypts the encrypted information of random number. $P _ { 2 }$ verifies the result if the following equations are true to determine if $P _ { 1 }$ cheating.

$$
\left\{ \begin{array}{l l} & \mathrm{E} _ {1} (\delta_ {1 1} \mathbf {V} _ {1} \cdot \delta_ {2 1} \mathbf {V} _ {2} + \delta_ {1 1} \delta_ {2 2} + \delta_ {1 2}) = \mathrm{E} _ {1} (d m _ {1}), \\ & \mathrm{E} _ {1} (\delta_ {1 1} \delta_ {2 1} \theta + \delta_ {1 1} \delta_ {2 2} + \delta_ {1 2}) = \mathrm{E} _ {1} (d m _ {2}). \end{array} \right.
$$

practical partial homomorphic encryption, the Paillier’s encryption. Each $P _ { i }$ needs to acquire a series of certificates $\begin{array} { r l r } { { \bf C } ( P _ { i } , \delta _ { k } v _ { i } ) } & { { } = } & { \langle \mathrm { S i g } ( I D _ { i } ) , \mathrm { E } _ { i } ( \delta _ { k } ) , \mathrm { E } _ { i } ( v _ { i } ) , \mathrm { E } _ { i } ( \delta _ { k } v _ { i } ) } \end{array}$ , $\mathrm { S i g } ( \mathrm { E } _ { i } ( \delta _ { k } ) )$ , Sig(Ei)(δkvi)), P ki, P kT 	, from a trusted authority $P _ { T }$ by giving $P _ { T }$ a set of random numbers $\{ \delta _ { k } \}$ chosen by $P _ { i }$ and $\mathrm { E } _ { P k _ { i } } ( v _ { i } )$ before the protocol launches. $P _ { i }$ can update the certificates once he/she can contact $P _ { T } .$ . Although the function $f ( v _ { 1 } , v _ { 2 } )$ in Protocol 1 can be any combination of addition and multiplication. $\mathrm { W . l . o . g . }$ ., we use the dot product $f ( \mathbf { V } _ { 1 } , \mathbf { V } _ { 2 } ) = \mathbf { V } _ { 1 } \cdot \mathbf { V } _ { 2 }$ of two private vectors as an example in the protocol statement. $\mathbf { R } _ { i } , r _ { i }$ are random vector and number chosen by $P _ { i }$ as the required input of the Paillier’s encryption.

2) Two-way Protocol: In the two-way situation, there is a common threshold $\theta . \ P _ { 1 }$ and $P _ { 2 }$ both need the verifiable result. A change is required to enable the two-way verifiable ranging. The values $\delta _ { 1 1 }$ and $\delta _ { 1 2 }$ are secretly chosen by $P _ { 1 }$ and $\delta _ { 2 1 }$ and $\delta _ { 2 2 }$ are secretly chosen by $P _ { 2 } . \mathrm { \ A }$ straightforward way is to repeat the Step 2 in the Protocol 1 to have $P _ { 1 }$ compute $\mathrm { E } _ { 2 } ( \delta _ { 1 1 } \mathbf { V } _ { 1 } \cdot \mathbf { V } 2 + \delta _ { 1 2 } )$ and $\mathrm { E } _ { 2 } ( \delta _ { 1 1 } \theta + \delta _ { 1 2 } )$ on the encrypted $\mathrm { E } _ { 2 } ( \mathbf { V } _ { 2 } )$ homomorphically. However, since $\mathbf { V } _ { 2 }$ could be a large vector, a simple extension will cost expensive computation. We design a more sophisticated solution and present Protocol 2 to reduce the computation cost. In the Step 3 of Protocol 2, we convert the homomorphic dot product computation on the ciphertext to a simple multiplication between two plain scalars which significantly simplifies the computation. According to our proof (omitted due to limited space), the input random number of Paillier’s encryption won’t affect the verifiability of the computation. For simplicity, we ignore the process of random numbers in the statement of Protocol 2 and the following protocols.

# Protocol 3: Participant Comparison Protocol

1) $P _ { 1 }$ sends certificate ${ \bf C } ( P _ { 1 } , v _ { 1 } )$ to $P _ { 2 }$ .   
2) $P _ { 2 }$ ( )randomly picks a certificate $\mathbf { C } ( P _ { 2 } , \delta _ { 1 } v _ { 2 } )$ and another arbitrary number $\bar { \delta } _ { 2 } . \ P _ { 2 }$ computes

$$
\left\{ \begin{array}{l l} & e _ {1} = \mathrm{E} _ {1} (\delta_ {1} v _ {1} + \delta_ {2}), \\ & e _ {2} = \mathrm{E} _ {1} (\delta_ {1} v _ {2} + \delta_ {2}), \\ & e _ {3} = \mathrm{E} _ {2} (\delta_ {2}), \end{array} \right.
$$

and sends them with the certificate and the encrypted information of random numbers by $P k _ { 1 }$ to $P _ { 1 }$ .

3) $P _ { 1 }$ compares $d _ { 1 } = \mathrm { D } _ { 1 } ( \dot { e _ { 1 } } )$ and $d _ { 2 } = \mathrm { D } _ { 1 } ( e _ { 2 } )$ to determine =the comparison result. $P _ { 1 }$ ) = D (verifies the value in $\dot { \bf C } ( P _ { 2 } , v _ { 2 } )$ , then ( )decrypts the information of random number and checks the following equations:

$$
\left\{ \begin{array}{l l} & \mathrm{E} _ {2} (\delta_ {1} v _ {1} + \delta_ {2}) = \mathrm{E} _ {2} (d _ {1}), \\ & \mathrm{E} _ {2} (\delta_ {1} v _ {2} + \delta_ {2}) = \mathrm{E} _ {2} (d _ {2}). \end{array} \right.
$$

If they are not all true, $P _ { 1 }$ learns that $P _ { 2 }$ is cheating.

# IV. VERIFIABLE RANKING PROTOCOL

Here we propose privacy-preserving verifiable ranking protocols in both participants model and aggregator model.

# A. Ranking Problem Definition

Definition 4 (Participant Ranking): A party $P _ { 1 }$ queries the rank of his own private value $v _ { 1 }$ among n parties’s private values $V = ( v _ { 1 } , v _ { 2 } , . . . . v _ { n } )$ . At the end, $P _ { 1 }$ only learns the ranking result $R ( P _ { 1 } , P )$ , which is an integer. Here $R ( P _ { 1 } , P ) =$ $K$ is $v _ { 1 }$ is the K-th smallest in $V .$ .

Definition 5 (Aggregator Ranking): An aggregator $P _ { a }$ wants to rank all n parties’s values $V = ( v _ { 1 } , v _ { 2 } , . . . . v _ { n } )$ . At the end, $P _ { a }$ only learns the ranking result $\langle I D _ { r 1 } , I D _ { r 2 } , . . . . I D _ { r n } \rangle$ where $I D _ { r i }$ is the ID of the user whose data is ranked i-th.

In both models, all participants’ values are kept private and only the initiator learns the result.

# B. Protocol Design

1) Participant Model: Comparison between two parties is the basic operation of participant ranking. First, we present our verifiable private comparison protocol (Protocol 3) between two participants. In the end of Protocol 3, $P _ { 1 }$ only learns the verifiable comparison result of $v _ { 1 }$ and $v _ { 2 } .$ , and $P _ { 2 }$ learns nothing. Based on the verifiable private comparison, $P _ { 1 }$ computes the rank $R ( P _ { 1 } , P )$ by comparing $v _ { 1 }$ with each party separately, and counting the values larger than $v _ { 1 }$ to conclude the rank $R ( P _ { 1 } , P )$ .

2) Aggregator Model: In the aggregator model, we first design the protocol to compare two parties’ private value for the aggregator $P _ { a }$ . It requires that, both $P _ { 1 }$ and $P _ { 2 } { } ^ { , }$ values are kept private and at the end of the protocol only the aggregator gets the verifiable comparison result. It is challenging when every party can eavesdrop all the communication. We present our design as Protocol 4.

By Protocol 4, the aggregator is able to get the verifiable comparison result between any pair of parties. Then we leverage the merge sort mechanism to design a parallel scheme

# Protocol 4: Aggregator Comparison Protocol

1) $P _ { a }$ launches the comparison by sending $P _ { 1 }$ and $P _ { 2 }$ his/her apublic key $P k _ { a }$ .   
2) $\bar { P } _ { 1 }$ arandomly picks a certificate $\mathbf { C } ( P _ { 1 } , \delta _ { 1 } v _ { 1 } )$ . P1 sends the certificate and $\begin{array} { r } { \dot { m } _ { 1 } = \operatorname { E } _ { 2 } ( \operatorname { E } _ { a } ( \delta _ { 1 } v _ { 1 } ) ) } \end{array}$ (to $P _ { 2 } .$   
3) $P _ { 2 }$ = E (Ea( )randomly picks a certificate $\dot { \bf C } ( P _ { 2 } , \delta _ { 2 } v _ { 2 } )$ . $P _ { 2 }$ sends the certificate and $\bar { m } _ { 2 } = \mathrm { E } _ { 1 } ( \mathrm { E } _ { a } ( \delta _ { 2 } v _ { 2 } ) )$ (to $P _ { 1 }$ .   
4) $P _ { 1 }$ = E (Everifies the value in $\dot { \bf C } ( P _ { 2 } , \dot { v } _ { 2 } )$ . P1 decrypts m2, then ( )computes the following value and sends them with key $P k _ { 1 }$ and the encrypted information of random numbers by ${ \dot { P } } k _ { a }$ to $P _ { a } \colon$

$$
\left\{ \begin{array}{l l} & e _ {1 1} = \mathrm{E} _ {a} (\delta_ {1} \delta_ {2} v _ {2}), \\ & e _ {1 2} = \mathrm{E} _ {a} (\mathrm{E} _ {2} (\delta_ {1} \delta_ {2} v _ {1})), \\ & e _ {1 3} = \mathrm{E} _ {a} (\mathrm{E} _ {2} (\delta_ {1} \delta_ {2} v _ {2})). \end{array} \right.
$$

Here $e _ { 1 2 }$ is calculated based on $\mathrm { E } _ { 2 } ( \delta _ { 2 } )$ in $\mathbf { C } ( P _ { 2 } , \delta _ { 2 } v _ { 2 } )$ and $e _ { 1 3 }$ is calculated based on $\mathrm { E } _ { 2 } \big ( \delta _ { 2 } v _ { 2 } \big )$ E (in $\dot { \bf C } ( P _ { 2 } , \delta _ { 2 } \dot { v } _ { 2 } )$ .

5) $P _ { 2 }$ E (verifies the value in ${ \bf C } ( P _ { 1 } , v _ { 1 } )$ (. $P _ { 2 }$ )decrypts $m _ { 1 }$ , then ( )computes the following value and sends them with key $P k _ { 2 }$ and the encrypted information of random numbers by $\dot { P } k _ { a }$ to $P _ { a } \colon$ :

$$
\left\{ \begin{array}{l l} & e _ {2 1} = \mathrm{E} _ {a} (\delta_ {1} \delta_ {2} v _ {1}), \\ & e _ {2 2} = \mathrm{E} _ {a} (\mathrm{E} _ {1} (\delta_ {1} \delta_ {2} v _ {2})), \\ & e _ {2 3} = \mathrm{E} _ {a} (\mathrm{E} _ {1} (\delta_ {1} \delta_ {2} v _ {1})). \end{array} \right.
$$

Here $e _ { 2 2 }$ is calculated based on $\mathrm { E } _ { 1 } ( \delta _ { 1 } )$ in $\mathbf { C } ( P _ { 1 } , \delta _ { 1 } v _ { 1 } )$ . e23 is calculated based on $\operatorname { E } _ { 1 } \left( \delta _ { 1 } v _ { 1 } \right)$ in $\mathbf { C } ( P _ { 1 } , \delta _ { 1 } v _ { 1 } )$ (.

6) $P _ { a }$ compares $d _ { 1 } = \mathrm { D } _ { a } ( \dot { e } _ { 1 1 } )$ )and $d _ { 2 } \doteq \mathrm { D } _ { a } ( e _ { 2 1 } )$ to determine the a = Da(comparison result. Then $P _ { a }$ = Da( )decrypts the information of random anumbers and checks the equations:

$$
\left\{ \begin{array}{l l} & \mathrm{E} _ {2} (d _ {1}) = \mathrm{D} _ {a} (e _ {1 3}), \mathrm{E} _ {1} (d _ {1}) = \mathrm{D} _ {a} (e _ {2 2}), \\ & \mathrm{E} _ {1} (d _ {2}) = \mathrm{D} _ {a} (e _ {2 3}), \mathrm{E} _ {2} (d _ {2}) = \mathrm{D} _ {a} (e _ {1 2}). \end{array} \right.
$$

If they are not all true, $P _ { a }$ learns that there’s a party cheating.

for ranking. Only $O ( \log n )$ rounds of comparisons will be launched by the aggregator. With the parallel steps 2) to 5) of Protocol 4, time complexity will be reduced compared to a serial scheme. Total O(n log n) comparisons are required in the worst case.

# V. ANALYSIS AND PERFORMANCE EVALUATION A. Protocol Analysis

Theorem 2: If the Paillier’s cryptosystem is semantically secure, Protocol 1 to 3 are privacy preserving.

Note that, in the Protocol 1, because the threshold θ is chosen by $P _ { 1 } , P _ { 1 }$ may launch a binary search by adjusting θ to narrow down the value range of $f ( v _ { 1 } , v _ { 2 } )$ . So we suggest that, a threshold may be given by the system or the query time should be limited.

Theorem 3: If the Paillier’s cryptosystem is semantically secure, the Protocol 4 is privacy preserving, when neither $P _ { 1 }$ nor $P _ { 2 }$ colludes with $P _ { a }$ even if the $P _ { 1 } , P _ { 2 }$ and $P _ { a }$ can eavesdrop all the communication.

However, if one of the party colludes with $P _ { a }$ , they can learn the value of the other party.

Theorem 4: Protocol 1 to 3 are verifiable: $P _ { 2 }$ cannot cheat $P _ { 1 }$ to accept an incorrect result, and vis versa.

TABLE II PERFORMANCE OF EACH PROTOCOL WITH REAL IMPLEMENTATION.M=30 

<table><tr><td rowspan="2">Protocol</td><td rowspan="2">Party</td><td colspan="2">Computation(s) (Verification)</td><td colspan="2">Computation(s) (All)</td><td colspan="2">Communication</td></tr><tr><td>Laptop</td><td>Phone</td><td>Laptop</td><td>Phone</td><td>(KB)</td><td>(Times)</td></tr><tr><td rowspan="2">1</td><td> $P_1$ </td><td>0.30</td><td>0.36</td><td>0.41</td><td>0.49</td><td>1.5</td><td>1</td></tr><tr><td> $P_2$ </td><td>no</td><td>no</td><td>2.05</td><td>2.72</td><td>3.25</td><td>1</td></tr><tr><td rowspan="2">2</td><td> $P_1$ </td><td>0.30</td><td>0.36</td><td>2.56</td><td>3.22</td><td>3.25</td><td>2</td></tr><tr><td> $P_2$ </td><td>0.30</td><td>0.37</td><td>2.35</td><td>3.09</td><td>3.25</td><td>1</td></tr><tr><td rowspan="2">3</td><td> $P_1$ </td><td>0.23</td><td>0.26</td><td>0.23</td><td>0.26</td><td>1.25</td><td>1</td></tr><tr><td> $P_2$ </td><td>no</td><td>no</td><td>0.12</td><td>0.14</td><td>3.25</td><td>1</td></tr><tr><td rowspan="3">4</td><td> $P_1$ </td><td>no</td><td>no</td><td>0.46</td><td>0.52</td><td>3.5</td><td>2</td></tr><tr><td> $P_2$ </td><td>no</td><td>no</td><td>0.46</td><td>0.52</td><td>3.5</td><td>2</td></tr><tr><td> $P_a$ </td><td>0.45</td><td>0.51</td><td>0.45</td><td>0.51</td><td>0.25</td><td>1</td></tr></table>

Theorem 5: Protocol 4 is unconditionally verifiable when at most one party cheats. And when both parties cheat individually without collaboration, $P _ { a }$ can verify the result with a quite high probability.

However, when $P _ { 1 }$ and $P _ { 2 }$ collude, they can cheat the aggregator to believe an incorrect result.

All the proof are omitted here due to the space limitation.

# B. Performance Evaluation

Our protocols are designed based on the fast variant of the Paillier’s cryptosystem, as in Table I. As in most implementations, we assume that n is 1024-bit, λ is 160-bit and the random number is 900-bit. We evaluate our protocols on both laptop and mobile phone. The laptop is Think Pad X1 with i7 2.7GHz CPU and 4GB RAM. The mobile phone is HTC G17 with 1228Hz CPU, and 1GB RAM. Table II presents the computation and communication cost of each protocol when the dimension of the vector is 30. The result shows that our protocols are practical in both laptop and mobile phones.

# VI. RELATED WORK

Secure multi-party computation (SMC) was initially introduced in [15]. One line of work on SMC is based on oblivious polynomial evaluation (OPE), e.g. [3], [8], [17]. Another line is based on oblivious pseudo random functions (OPRF), e.g. [5]. In all these approaches, both the input value and output result are not verifiable. The true result is only revealed to one party, who can cheat other parties by a forge result. Dong et al. [2] propose the fist scheme supporting verifiable private dot product between two parties.

There are some work leveraging Verifiable Secret Sharing (VSS) [13] to conduct multiparty computation of secret inputs when a majority of the players are honest, e.g. [11]. Secure computation based on VVS needs to share each secret input among n parties and requires at least t parties cooperate to produce the computation result. It results in high communication and computation cost.

Cloud computing enables the computational resource limited users to outsource their workload to the cloud. However, treating the cloud as an untrusted computing platform, privacy and verifiability are two of the main obstacles of its wide adoption. Recently, many work are dedicated to the privacyassured outsourced computing e.g. [14], [18] and cloud data access [19]. There are also some efforts on the verification of the outsourced computation result, e.g. [4].

# VII. CONCLUSION

In this paper, we analyze the potential attacks to the state-of-art secure multi-party computation schemes. Previous protocols focus on privacy protection, usually leaving the verifiability neglected. we propose the first verifiable privacy preserving protocols for threshold-based ranging and ranking in different situations, which can resist cheating on both input and outcome. We implement them on phones and laptops. The results show the efficiency of our protocols.

# ACKNOWLEDGMENT

The research is supported in part by National High-Tech R&D Program of China (863) under grant No. 2011AA010100, National Basic Research Program of China (973) under grant No. 2012CB316200 and the NSFC program under Grant No.61103187, No.61272426, No.61202359, No.61272429. The research of Xiang-Yang Li is partially supported by NSF CNS-0832120, NSF CNS-1035894, NSF ECCS-1247944, National Natural Science Foundation of China under Grant No. 61170216, No. 61228202, China 973 Program under Grant No.2011CB302705.

# REFERENCES

[1] BARANIUK, R. Compressive sensing [lecture notes]. Signal Processing Magazine, 2007, pp. 118–121.   
[2] DONG, W., DAVE, V., QIU, L., AND ZHANG, Y. Secure friend discovery in mobile social networks. INFOCOM, 2011.   
[3] FREEDMAN, M., NISSIM, K., AND PINKAS, B. Efficient private matching and set intersection. Advances in Cryptology-EUROCRYPT, 2004, pp. 1–19.   
[4] GENNARO, R., GENTRY, C., AND PARNO, B. Non-interactive verifiable computing: Outsourcing computation to untrusted workers. Advances in Cryptology–CRYPTO, 2010, pp 465–482.   
[5] HAZAY, C., AND LINDELL, Y. Efficient protocols for set intersection and pattern matching with security against malicious and covert adversaries. Theory of Cryptography, 2008, pp. 155–175.   
[6] XIANG-YANG LI, YAJUN WANG, AND YU WANG. Complexity of Data Collection, Aggregation, and Selection for Wireless Sensor Networks. IEEE Transactions on Computers, 2010, pp. 386–399.   
[7] HE, W., LIU, X., NGUYEN, H., NAHRSTEDT, K., AND ABDELZAHER, T. Pda: Privacy-preserving data aggregation in wireless sensor networks. INFOCOM , 2007.   
[8] LI, M., CAO, N., YU, S., AND LOU, W. Findu: Privacy-preserving personal profile matching in mobile social networks. INFOCOM, 2011.   
[9] PENG, K., BOYD, C., DAWSON, E., AND VISWANATHAN, K. Robust, privacy protecting and publicly verifiable sealed-bid auction. Information and Communications Security, 2002, pp. 147–159.   
[10] QI, Y., AND ATALLAH, M. Efficient privacy-preserving k-nearest neighbor search. ICDCS, 2008.   
[11] RABIN, T., AND BEN-OR, M. Verifiable secret sharing and multiparty protocols with honest majority. STOC, 1989.   
[12] SHENG, B., AND LI, Q. Verifiable privacy-preserving range query in two-tiered sensor networks. INFOCOM, 2008.   
[13] CHOR, B., GOLDWASSER, S., MICALI, S., AND AWERBUCH, B. Verifiable secret sharing and achieving simultaneity in the presence of faults. FOCS, 1985.   
[14] WANG, C., REN, K., YU, S., AND URS, K. Achieving usable and privacy-assured similarity search over outsourced cloud data. INFO-COM, 2012.   
[15] YAO, A. Protocols for secure computations. FOCS, 1982.   
[16] YE, Q., WANG, H., AND PIEPRZYK, J. Distributed private matching and set operations. Information Security Practice and Experience, 2008, pp. 347–360.   
[17] JUNG, T. AND MAO, X.F. AND LI, X.Y AND TANG, S.J. AND GONG, W. AND ZHANG, L. Privacy-preserving data aggregation without secure channel: multivariate polynomial evaluation. INFOCOM, 2013.   
[18] LI, X.Y. AND JUNG, T. Search me if you can: privacy-preserving location query service. INFOCOM, 2013.   
[19] JUNG, T. AND LI, X.Y AND WAN, Z. AND WAN, M. Privacy preserving cloud data access with multi-authorities. INFOCOM, 2013.