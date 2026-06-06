# Blockchain for Data Science

Jiameng Liu

College of Computer Science and

Electronic Engineering,

Hunan University

Changsha 410082, China

meng84@hnu.edu.cn

Shaoliang Peng\*

College of Computer Science and

Electronic Engineering,

Hunan University

Changsha 410082, China

slpeng@hnu.edu.cn

Chengnian Long

Department of Automation,

Shanghai Jiao Tong University and the

Key Laboratory of System Control and

Information Processing

Shanghai 200240, China

longcn@sjtu.edu.cn

Lijun Wei

Department of Automation,

Shanghai Jiao Tong University

Shanghai 200240, China

sjtu\_weilijun@sjtu.edu.cn

Yunhao Liu

College of Computer Science and

Electronic Engineering,

Hunan University

Changsha 410082, China

yunhao\_liu@hnu.edu.cn

Zhihui Tian

The school of the Geo-Science &

Technology,

Zhengzhou University

Zhengzhou 450001, China

iezhtian@zzu.edu.cn

# ABSTRACT

Nowadays, the development of social information and network leads to the explosive growth of data. The increasing amount and diversity of data have also encouraged researchers to make business decisions by analyzing the big data generated. This has also caused the rapid development of the data science industry. However, there are still many challenges to be solved, especially data security and privacy. Data security and privacy threat permeate every link of data science industry chain, such as data production, collection, processing and sharing, and the causes of risk are complex and interwoven. Blockchain technology is highly praised and recognized for its decentralized infrastructure, anonymity, security and other characteristics. It will change the way we access and share information. We believe that blockchain technology can overcome some limitations in data science and promote the development of data science, but it may also bring some other problems. Therefore, it is necessary to explore the relationship between blockchain technology and data science. In this paper, we investigate the researches and applications of blockchain technology in the field of data science and give the potential advantages and challenges that blockchain technology may bring to data science.

# CCS Concepts

•Security and privacy ➝ Database and storage security • Information systems ➝ Data management systems ➝ Information integration

# Keywords

Blockchain; Data science; Big data analysis; Security; Privacy

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from Permissions@acm.org.

ICBCT'20, March 12–14, 2020, Hilo, HI, USA

© 2020 Association for Computing Machinery.

ACM ISBN 978-1-4503-7767-6/20/03…\$15.00

https://doi.org/10.1145/3390566.3391681

# 1. INTRODUCTION

We are now living in an era of data deluge. Data is growing at an amazing rate, and everyone is generating new data every second. “Data Science” refers to the art of turning data into decisionmaking and tradecraft. It is the integration of tools, technologies, and processes by which people and computers work together to turn data into knowledge discovery. Data science is proposed from big data and it is a discipline that makes data useful. The development of data science cannot be separated from big data. It includes the research methods and background of big data. The academic and business circles have started to focus on applied research based on the technology of big data. At present, the big data technology has been widely used in various industrial fields such as genomics, meteorology, finance, healthcare and so on [1].

Big data comes from a great variety of sources and generally has three types: structured, unstructured and semi-structured. Most big data are unstructured and semi-structured, which will bring difficulties to the use of data. Difficulties at different levels include data collection, storage, searching, sharing, analysis, management, and visualization, as well as data security and privacy. Specifically, there is a large amount of data from all walks of life, but they are isolated and need to be effectively correlated. Many industries make use of a small portion of big data for analysis because of the lack of storage infrastructure and the analysis techniques [2]. What's more, network security laws put forward more and more relevant requirements for security situational awareness, etc. In order to solve these problems, many technologies have been put forward and applied. Hadoop, Spark, MapReduce, SAS, and Rapid Miner offer flexibility, scalability, and good performance to improve the analytic process [3, 4]. SecSVA [5] allows secure storage, verification, and auditing of big data in the cloud environment. However, these technologies still have many deficiencies in data privacy protection and transparency. What other technology can help to solve these problems? Blockchain may have the potential to offer a solution, we think.

Data science and blockchain technology are in full swing. Some may think the two technologies are mutually exclusive. In fact, they are two complementary technologies. According to estimates by Neimeth [6], the blockchain ledger could be worth up to 20% of the total big data market by 2030, with annual revenue of up to \$100 billion. Like other emerging technologies, blockchain is gradually changing the way some industries operate. What will happen when these two technologies are applied simultaneously? To answer this question, it is necessary to better understand the differences and connections between blockchain and data science.

In this paper, the current challenges of data science and blockchain and the potential advantages of their combined use will be analyzed.

Our main contributions are:

1. Survey on data science, including big data technology and its open challenges.   
2. Investigation on blockchain and analyze its characteristics.   
3. Study of potential benefits, challenges and open issues of the convergence of blockchain and data science.

The rest of the paper is organized as follows. Section 2 introduces the blockchain technology and analyzes its main characteristics. In Section 3 the integration of data science and blockchain is addressed, analyzing the opportunities and challenges that this integration involves. Our conclusion is presented in Section 4.

# 2. BLOCKCHAIN

The popularity of Bitcoin makes people pay more and more attention to its underlying technique, blockchain. Compared with Bitcoin, the scope of blockchain is much larger. Blockchain is a distributed, immutable, transparent, secure and auditable ledger, which records all transactions executed and shares them among all participants. It is a decentralized solution without any third-party organization in the middle. Each transaction is validated by the consensus of the participants. The information of each completed transaction in the blockchain will be shared with all nodes. Once a transaction is recorded in the ledger, it can not be erased. This attribute makes the system more transparent than centralized transactions involving third parties [7]. In short, blockchain is a network technology. It can give users the opportunity to share information safely and realize point-to-point transactions without a middleman or central management system.

# 2.1 Blockchain Marchitecture

![](images/a6c0fff9b8af9c98479c78e82dbedcef6612fbf14181e20b9990b6fa4897eda9.jpg)



Figure 1. Block structure

The blockchain is a sequence of blocks, which holds a complete list of transaction records like conventional public ledger [8]. A block consists of the block header and the block body. Block header and the block body as shown in Figure 1. Block version indicates the validation rules that this block follows; Parent block hash refers to the hash value of the previous block, which is calculated using SHA256 (parent block header); Merkle tree root hash refers to the hash value of the Merkle tree root of the transactions in the block, which is also calculated by SHA256; Timestamp refers to the approximate time produced by the block, which is accurate to the UNIX timestamp of seconds; nBits refers to the current hashing target in a compact format; Nonce refers to the counter for Proof-of-Work algorithm. The block body is composed of a transaction counter and transactions. It is worth mentioning that the first block of the blockchain is called genesis block, which means it has no parent block [9]. Like this, each block contains the hash of the previous block header (except the genesis block). All the transactions will be saved in the blockchain. If a block is to be tampered with, the parent hash contained in the next block will not match the tampered value, so that this tampering behavior will be found.

# 2.2 Characteristics of Blockchain

The five basic characteristics of blockchain technology are as follows:

Decentralization: All parties of the blockchain have the right to access the entire database and its complete historical records. No single party controls data or information. Each party can directly verify the records of its trading partners without the need for a middleman.

Security: Blockchain can ensure that information is not tampered with. In the blockchain network, each person has a ledger. Each node will store all the data on this blockchain. Even if the node is damaged or attacked, it will not pose any threat to the ledger.

Anonymity and data privacy: Because the data exchange between the nodes of the blockchain follows a specific consensus protocol, the blockchain network does not need to be trusted and can exchange data based on addresses rather than personal identities. At the same time, the blockchain uses cryptography to ensure data privacy, even if the data is leaked, it cannot be parsed.

Smart contract: A smart contract is a computer program that executes automatically when certain conditions are met. The digital nature of the ledger means that blockchain transactions can be linked to computational logic and are inherently programmable. Therefore, users can set algorithms and rules that automatically trigger transactions between nodes.

Auditability: Since the blockchain stores all historical data with a timestamp after the genesis block through the block data structure, any data on the blockchain can be traced back to its origin through the blockchain structure. It improves the traceability and transparency of the data stored in the blockchain.

# 3. THE CONVERGENCE OF BLOCKCHAIN AND DATA SCIENCE

The value of data science lies in extracting valuable parts from data to produce data products. Due to the privacy, complexity, asymmetric supply and demand of data, the current data circulation has seriously restricted the development of data science in the society. The problems of data opening, sharing, and privacy protection are vital bottlenecks in the development of data science. Considering some characteristics of blockchains, such as transparency, security, auditability, and privacy can be complementary to data science, many start-ups, enterprises, and governments [10] are exploring their applications in the supply chain, electronic health records, voting, energy supply, ownership management, and protection of critical civilian infrastructure [11].

# 3.1 Benefits in the Convergence of Blockchain and Data Science

Although the technology of data science is developing, data risk control is not perfect, and there are still insufficient issues such as data silos, data low-quality, and data leakage. The underlying logic of blockchain is decentralization, openness, and transparency. Blockchain technology can solve the trust problem in the Internet environment, so as to promote the rapid development of big data and the digital economy. In this section, we will analyze some potential benefits of combining blockchain with data science.

# 3.1.1 Security and Privacy

Blockchain technology ensures data security and privacy through its decentralized system. Most of the data is stored in centralized servers, which can lead to leakage and loss of data. They are often targeted by cyber attackers. Blockchains decentralize control over data, making it a daunting task for cybercriminals to access and manipulate data on a massive scale. In addition, the transaction data on the blockchain, including the transaction address, amount, and transaction time, are all open and transparent, but the identity of the owner of the transaction address is anonymous. Through the encryption of blockchain technology, the user's identity and user data can be separated through the encryption algorithm.

The combination of blockchain and data science is most widely used in healthcare. The healthcare industry must ensure the security, privacy, and integrity of healthcare data. This is the demand for a sound and secure data management system [12]. After analysis, André Gonçalves et al. [13]found that data growth in healthcare will be faster than the rest of the digital universe. Azaria et al. introduced MedRec [14]. By taking advantages of blockchain, MedRec manages authentication, confidentiality, and accountability, which are crucial considerations when handling sensitive information. Since the blockchain can perform asymmetric encryption, it allows for differential privacy. In this way, patients can share clinical records without having to share sensitive data [15].

# 3.1.2 Credibility and Transparency

Using blockchain technology as an intermediary, data science can provide data analysis for demanders through the automatic execution process of smart contracts. It reduces human intervention and redundancy through smart contracts. Through scanning and accurate analysis of all data, the blockchain network is combined with the automatic execution of smart contracts, which is unfamiliar but trusted by many parties [16]. Xiaofeng Meng et al. [16] designed a closed-loop analytical architecture based on big data and blockchain in the medical and health industry to ensure the mutual trust of data and realize transaction endorsement. The combination of blockchain and data science can also improve the transparency of the industry. Damiano Di Francesco Maesa et al. [17] proposed a blockchain-based approach for the definition of auditable access control systems. Both the resource owner and the subject making the access request can easily detect inappropriate authorization or access denial, thanks to publicly auditable evidence of misconduct.

# 3.1.3 Data Analysis

In the era of big data, data security issues not only contain the personal privacy protection issues but also include the issue of data analysis which aims to predict the people's status and behavior [18]. The data stored in the blockchain is structured and complete, which contributes to further analysis. Fedak [19] asserted, blockchain not only makes big data even bigger but also contributes by making big data more secure and valuable, as blockchained big data is structured and ready for big data analytics. Zhuojie Huang [20] showed that blockchain can ensure trust and improve data integrity among different entities in the crossborder logistics network. Data scientists can use these realtime, traceable, better-integrated data for real-time analysis and optimization to achieve a global optimization model.

Through the distributed characteristics of blockchain, huge computing power can be obtained. Even in small organizations, data scientists can undertake a wide range of prediction and analysis tasks. These data scientists can use the computing power of thousands of computers connected to the blockchain network as cloud-based services to analyze data.

# 3.1.4 Data Sharing

The blockchain has solved the security problem of data sharing to a certain extent. Healthcare is a typical multi-center scenario, and no one institution has all the data. As a combination of distributed storage, point-to-point transmission, consensus mechanism, and encryption algorithms, blockchain provides a solution for data sharing. What the blockchain does is to break the data silos and give the data greater value. Blockchain technology can be used in the field of healthcare to achieve a delicate balance between privacy and the accessibility of electronic medical records [21]. QI Xia et al. proposed MeDShare [22]. This system addresses the issue of medical data sharing among medical big data custodians in a trustless environment. Aiqing Zhang [23] offered a blockchain-based secure and privacy-preserving PHI sharing (BSPP) scheme for diagnosis improvements in Electronic health systems. Simon Lebech Cichosz et al. [24] presented an approach for a blockchain-based platform for sharing Diabetes Health Care Data.

# 3.1.5 Protection of Data Sovereignty

At present, the use of most data is not controlled by its owners, because there is no reliable way to record how data is used and who records it. So there's almost no way to track or punish violators who use that data without limit [25]. Blockchain can further standardize the use of data and refine the scope of authorization, so as to protect the relevant rights and interests of data. Uchi Ugobame Uchibeke et al. [26] provided an architecture for access control management by using a decentralized security system based on the private and permissioned hyperledger blockchain. When users try to access data sets, the verify smart contracts or transactions verify that users have access to the data, thereby ensuring the rights of data. Chao Lin et al. [27] proposed the conceptual blockchain-based system (BSeIn) for remote mutual authentication with fine-grained access control. Only authorized participants can gain access to the original context of the request message. The whole request process is executed by interacting with the smart contract.

# 3.2 Challenges in the Convergence of Blockchain and Data Science

This section studies the main challenges to be addressed when applying blockchain technology to the data science domain. The birth time of blockchain is too short and the technical framework is not mature enough. Compared with most of the other technologies, blockchain is still in the "infant" stage. Although blockchain can bring many benefits to data management, there are still some noteworthy challenges. Some of the identified challenges are presented in this section.

# 3.2.1 Scalability

In data science, a lot of data needs to be processed and analyzed. Therefore, data storage must support high transaction throughput and high scalability. Scalability is defined as the ability of a system, network, or process to expand its potential by handling increasing workloads. Although blockchain brings many advantages that other technologies don't have, it is still exposed to the scalability issue, that prevents real-time trading [28]. The larger the size of the blockchain, the longer it will take to copy data to new nodes on the network. This affects new nodes or those that are back online and have not been updated for a long time. Algorithm level optimization can not solve the scalability problem of the large-scale decentralized system. Some schemes implemented under the chain are contrary to the idea of blockchain decentralization. Therefore, most of the leading blockchain projects above adopt a scalable method like sharding. However, these scalable methods will bring some security problems. Since participants cannot download and verify the history of the entire slice, they cannot be sure that the results they interact with have been written to the block. Therefore, we should continue to study the blockchain solution for data science and find a more complete solution.

# 3.2.2 Difficulty in Accurate Analysis

With the rapid development of the application of blockchain technology, the data scale will become larger and larger. The data fusion of blockchain in different business scenarios will further expand the data scale and richness. Although anonymity and privacy protection are the main characteristics of blockchain, it also makes it extremely difficult for researchers to obtain valuable information from blockchain data sets. The key and difficult point of on-chain data analysis is mining the relationship between accounts and addresses. The more anonymous the blockchain data set is, the more difficult it is for accurate marketing to individuals. Researchers can only get general rules from these data, but it is difficult to accurately predict the future behavior and results of individuals. The combination of blockchain and data science forms a very complex network. With the anonymity of blockchain, it is very difficult to mine the data on the chain in depth.

# 3.2.3 Consensus Upgrade

A consensus algorithm can be defined as a mechanism to make multiple participants in the network reach an agreement. Since the public blockchain does not rely on a central authority, the decentralized nodes need to reach an agreement on the validity of the transaction. This is the role of the consensus algorithm to ensure that all nodes comply with the protocol rules and that all transactions are conducted in a reliable way. When blockchain technology is applied to the field of data science, there must be multiple participants in the network. How to make these participants reach an agreement on one problem is a big problem. The most widely used consensus algorithms are POW and POS. There are other consensus algorithms that utilize the alternative implementation of POW and POS, as well as other hybrid implementations and some new consensus strategies [29], such as Ripple protocol consensus algorithm RPCA [30], Stellar Consensus Protocol (SCP) [31], Delegated Proof of Stake (DPOS) [32] and so on. Each industry will select and modify the consensus mechanism according to its own needs. However, participants and their big data environment are constantly changing, that is to say, there may be some changes in industry rules and their adjustments. After all parties of the blockchain have reached a consensus, how to upgrade the consensus with the changes in the environment is a very important issue. Especially after joining the incentive mechanism, how to persuade stakeholders to revise their opinions needs further research and discussion.

# 3.2.4 Intensified Competition

Data is undoubtedly the foundation of the information society. Each enterprise wants to collect as much data as possible to improve its competitiveness in the future [33]. With the dual support of the concepts of "blockchain" and "data science", more and more start-ups enter the blockchain and data science arena. At present, the profit route of big data companies can be summarized as "data-tools-services". Data acquisition is the first barrier to competition. In many areas, whether the data can be obtained or not determines the survival of the enterprise. However, in the blockchain industry, due to the characteristics of the technology itself, there is basically no threshold for big data companies to acquire data. That is, everyone can access the data on the blockchain. Breaking the data barrier means the reduction of data costs. In the future, more and more blockchain big data enterprises will appear, and the competition among enterprises will be more and more fierce. How to deal with data is the focus of competition, that is to say, who can provide more accurate and valuable content and tools are the key to win blockchain big data. However, for blockchain big data service companies, it is still early days, and there are still many things to be done.

# 4. CONCLUSIONS

Data science and blockchain technology can be combined to completely change the way we process and analyze data. The huge scale, diversity, and high growth rate of data and the rapid development of data applications have placed extremely high demands on the user amount, concurrency, and energy efficiency optimization of privacy protection service requests. In this paper, we first give an overview of data science, including big data technology and the threats it faces. Then we introduce blockchain technology, including blockchain architecture and some key features of blockchain. We also illustrate the potential benefits, challenges and open issues of blockchain and data science integration. While we embrace blockchain technology, we should strengthen the guidance and standardization of blockchain technology, pay attention to the research and analysis of data security risks, closely track development trends, and actively explore regulatory methods.

# 5. ACKNOWLEDGMENTS

This work was supported by National Key R&D Program of China 2017YFB0202602, 2018YFC0910405, 2017YFC1311003, 2016YFC1302500, 2016YFB0200400, 2017YFB0202104; NSFC Grants U19A2067, 61772543, U1435222, 61625202, 61272056; The Funds of Peng Cheng Lab, State Key Laboratory of Chemo/Biosensing and Chemometrics; the Fundamental Research Funds for the Central Universities, and Guangdong Provincial Department of Science and Technology under grant No. 2016B090918122.

# 6. REFERENCES

[1] Yin, S. and O. Kaynak, Big data for modern industry: challenges and trends [point of view]. Proceedings of the IEEE, 2015. 103(2): p. 143-146.   
[2] Katal, A., M. Wazid, and R. Goudar. Big data: issues, challenges, tools and good practices. in 2013 Sixth international conference on contemporary computing (IC3). 2013. IEEE.

[3] Tsai, C.-W., et al., Big data analytics: a survey. Journal of Big data, 2015. 2(1): p. 21.   
[4] Oussous, A., et al., Big Data technologies: A survey. Journal of King Saud University-Computer and Information Sciences, 2018. 30(4): p. 431-448.   
[5] Aujla, G.S., et al., SecSVA: secure storage, verification, and auditing of big data in the cloud environment. IEEE Communications Magazine, 2018. 56(1): p. 78-85.   
[6] Neimeth, C. What can be uncovered when big data meets the blockchain. JUN 29, 2017; Available from: https://www.infoworld.com/article/3203748/what-can-beuncovered-when-big-data-meets-the-blockchain.html.   
[7] Yli-Huumo, J., et al., Where is current research on blockchain technology?—a systematic review. PloS one, 2016. 11(10): p. e0163477.   
[8] Lee Kuo Chuen, D., Handbook of digital currency. 2015, Elsevier.   
[9] Zheng, Z., et al., Blockchain challenges and opportunities: A survey. International Journal of Web and Grid Services, 2018. 14(4): p. 352-375.   
[10] Walport, M., Distributed ledger technology: Beyond blockchain. UK Government Office for Science, 2016. 1.   
[11] Xu, X., et al. A taxonomy of blockchain-based systems for architecture design. in 2017 IEEE International Conference on Software Architecture (ICSA). 2017. IEEE.   
[12] Esposito, C., et al., Blockchain: A panacea for healthcare cloud-based data security and privacy? IEEE Cloud Computing, 2018. 5(1): p. 31-37.   
[13] Gonçalves, A., et al., Towards of a real-time big data architecture to intensive care. Procedia computer science, 2017. 113: p. 585-590.   
[14] Azaria, A., et al. Medrec: Using blockchain for medical data access and permission management. in 2016 2nd International Conference on Open and Big Data (OBD). 2016. IEEE.   
[15] Roman-Belmonte, J.M., H. De la Corte-Rodriguez, and E.C. Rodriguez-Merchan, How blockchain technology can change medicine. Postgraduate medicine, 2018. 130(4): p. 420-427.   
[16] Wang, X., et al. A Kind of Decision Model Research Based on Big Data and Blockchain in eHealth. in International Conference on Web Information Systems and Applications. 2018. Springer.   
[17] Maesa, D.D.F., P. Mori, and L. Ricci, A blockchain based approach for the definition of auditable Access Control systems. Computers & Security, 2019. 84: p. 93-119.   
[18] Zhang, D. Big data security and privacy protection. in 8th International Conference on Management and Computer Science (ICMCS 2018). 2018. Atlantis Press.

[19] Fedak, V., Blockchain and big data: The match made in heavens. Towards Data Science, 2018.   
[20] Huang, Z., From Data Science to Blockchain-Analytics in Cross-Border Logistics. 2019.   
[21] Dagher, G.G., et al., Ancile: Privacy-preserving framework for access control and interoperability of electronic health records using blockchain technology. Sustainable Cities and Society, 2018. 39: p. 283-297.   
[22] Xia, Q., et al., MeDShare: Trustless medical data sharing among cloud service providers via blockchain. IEEE Access, 2017. 5: p. 14757-14767.   
[23] Zhang, A. and X. Lin, Towards secure and privacypreserving data sharing in e-health systems via consortium blockchain. Journal of medical systems, 2018. 42(8): p. 140.   
[24] Cichosz, S.L., et al., How to use blockchain for diabetes health care data and access management: an operational concept. Journal of diabetes science and technology, 2019. 13(2): p. 248-253.   
[25] Lu, Q. and X. Xu, Adaptable blockchain-based systems: A case study for product traceability. IEEE Software, 2017. 34(6): p. 21-27.   
[26] Uchibeke, U.U., et al. Blockchain access control Ecosystem for Big Data security. in 2018 IEEE International Conference on Internet of Things (iThings) and IEEE Green Computing and Communications (GreenCom) and IEEE Cyber, Physical and Social Computing (CPSCom) and IEEE Smart Data (SmartData). 2018. IEEE.   
[27] Lin, C., et al., BSeIn: A blockchain-based secure mutual authentication with fine-grained access control system for industry 4.0. Journal of Network and Computer Applications, 2018. 116: p. 42-52.   
[28] Mengelkamp, E., et al., A blockchain-based smart grid: towards sustainable local energy markets. Computer Science-Research and Development, 2018. 33(1-2): p. 207-214.   
[29] Bach, L., B. Mihaljevic, and M. Zagar. Comparative analysis of blockchain consensus algorithms. in 2018 41st International Convention on Information and Communication Technology, Electronics and Microelectronics (MIPRO). 2018. IEEE.   
[30] Schwartz, D., N. Youngs, and A. Britto, The ripple protocol consensus algorithm. Ripple Labs Inc White Paper, 2014. 5: p. 8.   
[31] Mazieres, D., The stellar consensus protocol: A federated model for internet-level consensus. Stellar Development Foundation, 2015: p. 32.   
[32] Larimer, D., DPOS Consensus Algorithm—The Missing Whitepaper, Steemit, 2018.   
[33] Lecuyer, M., et al., Enhancing selectivity in big data. IEEE Security & Privacy, 2018. 16(1): p. 34-42.