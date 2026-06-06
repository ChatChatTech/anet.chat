# Arnetminer: expertise oriented search using social networks

Juanzi LI (\*) 1 , Jie TANG1 , Jing ZHANG1 , Qiong LUO2 , Yunhao LIU2 , Mingcai HONG1

1 Department of Computer Science and Technology, Tsinghua University, Beijing 100084, China 2 Department of Computer Science, The Hong Kong University of Science and Technology, Hong Kong, China

E Higher Education Press and Springer-Verlag 2008

Abstract Expertise Oriented Search (EOS) aims at providing comprehensive expertise analysis on data from distributed sources. It is useful in many application domains, for example, finding experts on a given topic, detecting the confliction of interest between researchers, and assigning reviewers to proposals. In this paper, we present the design and implementation of our expertise oriented search system, Arnetminer (http://www.arnetminer.net). Arnetminer has gathered and integrated information about a half-million computer science researchers from the Web, including their profiles and publications. Moreover, Arnetminer constructs a social network among these researchers through their co-authorship, and utilizes this network information as well as the individual profiles to facilitate expertise oriented search tasks. In particular, the co-authorship information is used both in ranking the expertise of individual researchers for a given topic and in searching for associations between researchers. We have conducted initial experiments on Arnetminer. Our results demonstrate that the proposed relevancy propagation expert finding method outperforms the method that only uses person local information, and the proposed twostage association search on a large-scale social network is order of magnitude faster than the baseline method.

Keywords social network, expertise search, association search

# 1 Introduction

This paper is concerned with the problem of expertise oriented search. This problem arises in many applications. For example, researchers often want to find experts on a certain topic and know more about these experts. Also, they may want to find the most influential papers on the topic, as well as the associations between some researchers. As another example, a funding agency constantly needs to query and search for experts on a certain topic, suitable reviewers for proposals and the relationships between project applicants and reviewers.

Expertise oriented search often requires retrieving largely unstructured raw data from multiple sources (e.g., home pages, conferences, DBLP, mailing lists), analyzing and mining semantic information from the data. These extraction and mining tasks pose several challenges. The first challenge is to extract and integrate data from heterogeneous sources. The second challenge is the effectiveness and scalability of searching and mining a large amount of data.

Driven by such applications and challenges, we have developed Arnetminer (http://www.arnetminer.net), an expertise oriented search system. Currently, Arnetminer contains the information of 448289 computer scientists, including their profiles and publications. This information is gathered from the Web and is integrated into a social network after cleaning and annotation. Based on this database, Arnetminer provides four main kinds of expertise oriented search services:

(1) searching for a given person’s information;   
(2) searching for publications;   
(3) searching for experts on a given topic;   
(4) searching for associations between two researchers.

The former two issues have been intensively studied in existing literature. The later two issues have not been sufficiently investigated previously and are the main focuses of our work.

Our approach to providing these services is to build a social network among the researchers through the coauthorship information in their publications. Specifically, each node in the network is a researcher’s profile including publications, and the edges are the co-authorships between researchers. To facilitate the search for experts on a given topic, we examine the local information (e.g., research interests, professional activities) of individual researchers as well as the co-authorship between researchers. Intuitively, the more publications researchers have (co-)authored relevant to a given topic, the more relevant their expertise is to the topic. Furthermore, the relevance of a researcher’s expertise to the topic is propagated to other researchers through coauthorships. Additionally, we have adopted the publicly available impact factor information about publication forums to help the relevance ranking [1]. Experimental results show that our proposed approach significantly outperforms the method that only uses the person local information.

In addition, to facilitate expert search, our co-author network supports searching associations between researchers. This association search is useful in many cases, for instance, examining relationships between a grant applicant and a proposed reviewer for possible conflict of interest [2], between two co-investigators on a grant proposal for the degree of collaboration, or between two proposed reviewers to control the degree of overlap [3]. Since this coauthor network contains millions of relationships between authors, we have developed an efficient two-phase search algorithm for this association search. The response time is usually within a few seconds. It is over a hundred times faster than the baseline methods.

The remainder of this paper is organized as follows. We review the related work in Section 2 and give the preliminaries and an overview of Arnetminer in Section 3. We present the construction of Arnetminer in Section 4 and the search mechanisms in Sections 5 and 6. We discuss our evaluation results in Section 7 and conclude the paper in Section 8.

# 2 Related work

This section introduces the related work on expertise oriented people search in social networks. We summarize it on four aspects. They are social networks, people search, expert search and association search in social networks.

# 2.1 Social networks

A social network enables people of common interests to publish their interests, get to know others and interact with people. Many social networks on the Web have been built, for example, tickle.com, friendster.com, myspace. com. According to a recent survey [4], 140 social networks have over 170 million members in total.

A semantic social network integrates multiple physical social networks and makes them interoperable. For example, The Friend of a Friend (FOAF) project creates a Web of machine-readable pages describing people and the relationships between people [5]. It has been adopted by many different social networking applications, such as FOAFRealm [6], FOAFnaut [7], and Flink [8].

Much research efforts have been made on the social network extraction. For instance, Ref. [9] presented an end-toend system that extracts a user’s social network and its members’ contact information from the user’s email inbox. Reference [10] developed a social network extraction system with a focus on relationship extraction and tracing. Flink [11] is a system for the extraction, aggregation and visualization of an online social network by using the Semantic Web technology. Other related work includes [12].

# 2.2 People search

Most of the current social networks provide people search. When a user types in keywords, the information about the people that matches the user requirement is returned. Examples are Friendster.com, Myspace.com and LinkedIn.com.

Reference [13] defined several search tasks related to people in a personal work space setting. The personal work space is the documents of an organization’s internal and external website, e-mail and database records. Searching for people in the personal work space includes three tasks, namely, expert finding, expert profiling and relationship finding.

Google Scholar can search diverse sources from a single point of entry, find papers of researchers and get the citation information of papers. CiteSeer is a digital library that focuses primarily on the literature in computer and information science. It provides detailed information about the citations of papers. These two search engines are powerful and are widely used by researchers.

Reference [8] presented a system describing the scientific work and social connectivity of Semantic Web researchers. It provides a browser for social networks, visualizes relationships between people and gives analysis results including Indegree, Closesness and Betweeness. Swoogle [14] is a search engine for Semantic Web documents, terms and data found on the Web. It employs a system of crawlers to discover RDF documents as well as HTML documents with embedded RDF content. POLYPHONE provides people search within a conference committee [12]. It can search for the person information, his/her related persons, and the shortest path between two persons. Other related work includes Libra [15], rexa [16] and DBlife [17].

# 2.3 Expert search

The task of expert finding is aimed at identifying persons with relevant expertise or experience for a given topic. Hawking points out that expert finding is one of the biggest challenges when dealing with information management [18]. Many research efforts have been made and mostly focused on expert finding on the Web or within an enterprise intranet.

Reference [19] and [20] aim at finding influential individuals and the evolution of co-authorship networks by analyzing the conference papers of SIGMOD and SIGIR respectively. Campbell [21] analyzed the link structure between authors and receivers of emails using a modified version of the Hyperlink-Induced Topic Search (HITS) algorithm to identify authorities. Other related work also includes [10,22–25].

Starting from 2005, the Text REtrieval Conference (TREC) has provided a common platform with the Enterprise Search Track for researchers to empirically assess their methods for expert finding. An overview is given by Ref. [26]. Fu et al [27] have developed a method called document reorganization to facilitate finding experts. Cao et al [28] propose a two-stage language model to the task.

# 2.4 Association search

Association search aims at finding the relationships between people. The ReferralWeb [10] system helps people search and explore social networks — the networks of friends, colleagues, and co-workers — that exist on the Web. They focus on expert recommendation rather than efficiently finding and ranking the associations. Balog and Rijke [13] propose to formulate three sub tasks in people association finding (also called relationship finding): connection finding, collaboration finding, and reputation analysis. They focus on finding direct associations between persons from the documents on the Web using information retrieval models. Adamic and Adar [29] have investigated the problem of association search in email networks. They tested how three properties (degree, position in the organizational hierarchy, and physical location) of the individuals in the social network can be used to improve the performance of association search.

Compared with the related work, this paper proposes the expertise oriented search. We formulize the services of expertise oriented search. We propose to accomplish it by building a social network from distributed sources automatically. To provide efficient and effective comprehensive expertise oriented search, we also propose the expert finding and association searching algorithms in a social network by using the information of person profile and the relationships between people. Finally, we implement a practical expertise oriented search system Arnetminer including 448289 computer scientists, with their profiles and publications based on the proposed methods.

# 3 Preliminaries and overview

In this section, we introduce the preliminaries of our work and describe the architecture overview of Arnetminer. Even though our system is developed for the computer science research area, it can be extended to handle social networks in other domains.

# 3.1 People and relationships

We describe a social network as a graph $G = ( V , E ) . \ V = \{ \nu _ { i } |$ $i = 1 , 2 , \cdots , \ N _ { \nu } \}$ is the set of persons, and $E = \{ ( \nu _ { i } , \nu _ { j } , e ^ { t } ) |$ $i , j \leqslant N _ { \nu } , i \neq j \}$ is the set of relations between persons. $N _ { \nu }$ is the number of people in a social network. $( \nu _ { i } , \nu _ { j } , e ^ { t } )$ represents a relationship between persons $\nu _ { i }$ and $\nu _ { j }$ with type $e ^ { t } ,$ and is written as $e _ { i j } ^ { t }$ in brief.

For a person $\nu _ { i } ,$ the schema of the person profile is shown in Table 1. It is represented based on FOAF [30].

Table 1 Schema of the person local information 

<table><tr><td>name</td><td>organization</td><td>expert_degree</td></tr><tr><td>title</td><td>depiction</td><td>phone_number</td></tr><tr><td>img</td><td>publications</td><td>fax_numbe</td></tr><tr><td>homepage</td><td>topic_interest</td><td>mbox</td></tr></table>

The only attribute in a person’s profile that is not in FOAF is expert\_degree. It is used to describe a person’s academic influence, which is a numeric number.

In Arnetminer, We use PLI(vi) to represent the profile information of person vi. PLI(vi) already contains some relationships, for example, the person-organization relationship (affiliation) and the person-research-interest relationship (interest\_topic). However, relationships in a social network are those between people. They are different from the general concept of a relationship in ontologies.

In a social network, there are many kinds of relationships such as ‘‘supervised\_by’’, ‘‘co-author’’, ‘‘colleague’’ and so on. Figure 1 illustrates a part of a social network. We use $P R I ( \nu _ { i } )$ to represent the relationships of person $\nu _ { i } .$

$$
\begin{array}{l} P R I (v _ {i}) = \left\{e _ {i j} ^ {t} | i \neq j, i, j \leqslant N _ {v}, e ^ {t} \text {   is   a   relationship   type } \right\} \tag {1} \\ \cup \left\{e _ {k i} ^ {t} | k \neq i, i, k \leqslant N _ {v}, e ^ {t} \text {   is   a   relationship   type } \right\} \\ \end{array}
$$

In Arnetminer, we use co-authorship as a type of relationship between people, and define foaf: knows for this relationship type.

# 3.2 Expertise oriented search services

We classify expertise oriented search services in a social network $G = ( V , E )$ into four types.

Person search Given a person’s name or given a person’s name and some constraints, it returns PLI(x) and $P R I ( x )$ for all x that satisfy the search condition.

The name can be the first name, last name or full name. The search conditions can be constraints on some attributes, for example, organization. A query ‘‘Jie Tang, org: Tsinghua’’ searches for the person with name ‘‘Jie Tang’’ and affiliation ‘‘Tsinghua’’. The search result is the person information about ‘‘Jie Tang’’ who works in Tsinghua University.

Expert finding Given a topic q, which is a sequence of words, it returns a ranked list including em persons with the most ‘expertise’. We use rel(v, q) to denote the relevance of person v to topic q. The expert list for topic q

![](images/17087be94edca2d9484f815e7f9a54048ba33fe87ef917fcc67baff46630186d.jpg)



Fig. 1 Example relationships in a social network

EPL(q) is defined as

$$
E P L (q) = \left\{v _ {i} \mid \max _ {e m} (r e l (v _ {i}, q)), \text {   for   } i = 1, 2,..., N _ {v} \right\}. \tag {2}
$$

Association search Given two persons’ names $\nu _ { i }$ and $\nu _ { j } ,$ it returns $s _ { n }$ paths of the lowest cost between $\nu _ { i }$ and vj in a social network.

$a s s o ( \nu _ { i } , \ \nu _ { j } ) = \{ ( p a t h _ { k } ( \nu _ { i } , \ \nu _ { j } ) , \ f ( p a t h _ { k } ( \nu _ { i } , \ \nu _ { j } ) ) ) \ | \ f ( p a t h _ { k } ( \nu _ { i } , $ $\begin{array} { r } { \nu _ { j } ) ) \lesssim f ( p a t h _ { k + I } ( \nu _ { i } , \nu _ { j } ) ) , k = 1 , 2 , . . . , s _ { n - 1 } \big \} _ { \nu } } \end{array}$ ,

where $p a t h _ { k } ( \nu _ { i } , \nu _ { j } ) = \nu _ { k 0 } \nu _ { k l } . . . \nu _ { k \nu }$ denotes a path of length v from $\nu _ { i } \quad \mathrm { t o } \quad \nu _ { j } , \quad \nu _ { k 0 } = \nu _ { i } , \quad \nu _ { k \nu } = \nu _ { j } ,$ and $\left( \nu _ { k i } , \nu _ { k ( i + 1 ) } , \right.$ $\mathbf { e } _ { k i , k ( i + 1 ) } ^ { t } ) \in E , f ( \mathbf { \theta } )$ is a cost function of a path. The lower the value f( ), the better the path.

When a name corresponds to multiple people, the system shows all people with the same name, and the user can select one for association search.

Publication search Given the keywords of interest, it returns all matched publications.

In publication search, the user inputs keywords, and the system returns the relevant publications. The system will provide downloadable links of the publications if possible. These online versions are also stored in our system and are provided to the user for preview.

# 3.3 System architecture

Figure 2 depicts our system architecture. In the following, we describe each component. Metadata definition this component defines the metadata for a social network. The metadata has been described in Section 3.1.

Social network (SN) construction for each person named x in a social network, this component constructs the person’s local information as well as relationship information from Web pages and online databases. We use Google to locate Web pages related to the person and then select the most relevant Web pages. Different information extraction methods are used to identify different kinds of information. We use DBLP as a main source for publication information. Finally, we integrate all of the information into the co-authorship social network.

SN Storage and management this component stores and manages the metadata and database of the social network. We use Jena [31] and SWARMS [32] as the infrastructure for social network storage and management.

Expertise oriented search as defined in Section 3.2, given a person’s name and optional constraints, person search returns the person information. Given a topic presented by a sequence of words, expert finding returns a name list of people with the most expertise in the topic. Given two persons’ names, association search returns the top association paths between two people.

User interface for person search, person’s PLI and PRI are displayed and corresponding links are given. For publication search, retrieved publications about topic q are listed with the detailed information such as co-authors, journal or conference name and publication pages. For expert finding, experts’ names with their links are presented. For association search, top association paths are displayed one by one in the descending order of path cost.

![](images/4393bd6f1cfb482331096ff67ce5fdda7a812b7c4a195f91d4a1b5f8067a5a54.jpg)



Fig. 2 Architecture of Arnetminer

Currently in our operation system, we also provide some other kinds of search such as hot topic search, survey paper search etc.

In the following, we focus on the construction of SN, expert search and association search, as they are three key issues in expertise oriented search using social networks. SN construction determines the accuracy of the presentation of person information in the social network. Expert finding needs to consider the relationships between people. Association search requires efficient algorithm to search for association paths in a large scale social network.

# 4 Social network construction

The construction of a social network is to create the person profile and then the co-author relationship. The latter can be done automatically by given the coauthor information. Therefore, the major problem in the construction of a social network is to identify and integrate the person profile information from distributed sources on the Web. In this section, we will describe the steps of constructing a social network in Arnetminer.

# 4.1 Data sources

Many sources on the Web can provide person information. They may be Web pages or online databases. In Arnetminer, we use Web pages, XML files of DBLP[33], and the publication ranking list provided by Citeseer [1].

(1) Web pages: Web pages include personal homepages, organization Web pages and community Web pages. From these pages, we extract the person information.   
(2) DBLP: We use DBLP as an important data source about publications of people. The DBLP server provides bibliographic information on major computer science journals and proceedings. DBLP provides dtd files to describe the metadata in its database and also provides XML files of the data (about 340 MB). Through DBLP, we can get the description of each paper.   
(3) Name list in DBLP: We parse the XML files of DBLP and extract author names and then produce an author name list in DBLP. We use people in this list as the nodes in the social network.   
(4) Estimated impact of conferences and journals provided by Citeseer [1]: Citeseer published a list of estimated impact of publication venues in computer science in May 2003. This list totally contains 1221 conferences and journals.

# 4.2 Locating related Web pages

Using Google to search for the Web pages containing a person’s information is the first step to locate Web pages related to the person. We use a person’s name as the keyword to search through Google.

In practice, some researchers have no homepages whereas the Web pages of the organizations and communities may contain the person information. Our preliminary experiments show that typical related Web pages can be personal homepages, publication pages from DBLP, and introductory Web pages about the person by an organization.

The first Web page Google returned may not be the page containing the information of person profile and also there may exist many Web pages to describe one person. In order to locate suitable Web pages containing the person profile, we use the top 20 returned pages as candidates. We analyzed Web pages returned by Google search engine and classify them into four types: DBLP search results, personal homepages created by the person whom we search for, the introductory Web pages for a person created by the organizations or communities that the person is associated with, and the others which do not contribute to the information of person profiles.

After locating Web pages that contain person information, we select high-quality pages from these candidate pages.

A SVM (Support Vector Machines) [34] based classification model is employed to identify whether or not a Web page is really ‘related’ to a person. A classifier is trained from a data set containing Web pages. We created the data set as follows. We randomly selected 2000 researchers from DBLP and used their names as queries in Google. We gathered the top 20 results from the Google results for each query (if the number of returned page exceeds 20). In total, we collected 37336 Web pages.

Then, human annotator conducted annotation on the data set. Specifically, 2720 Web pages are annotated as positive samples and the rest are negative samples.

We use SVM as the classification model to identify the relevant Web page. Features are defined in the SVM model. Due to space limitation, we omit the details of the feature definition. We carried out experiments to evaluate the performance of the classification based filtering method. Table 2 shows the five-fold cross validation results.

Table 2 Performance of locating Web page (%) 

<table><tr><td></td><td>precision</td><td>recall</td><td>F1-measure</td></tr><tr><td>filtering</td><td>93.55</td><td>91.84</td><td>92.69</td></tr></table>

# 4.3 Person information annotation

# 4.3.1 Web page annotation

Person information annotation is to annotate the Web pages with the information defined in Table 1 and generate the person profile in the social network. Because different kinds of information have different features in Web page, we use different semantic annotation methods for extraction [35,36]. We do not extract publication information from Web pages; instead, we use the publication information in DBLP.

Rule based semantic annotation is suitable for annotating the information that has template like structure. In Arnetminer, title, organization, homepage, phone number, fax phone number and email address are extracted using this method. The rules are learned from annotated example Web pages.

We also use classification based semantic annotation to annotate depiction and portrait (img) in person profiles. At first, we define some features for each type of person information to be annotated. We then use the training data to train the classification based semantic annotation model. The model is used to detect the start position and the end position for each type of the person information. Then we annotate the content between the start position and the end position. As for the classification models, we use SVMs. For example, in the identification of personal portrait, we use the surrounding text, image content features (e.g., whether or not one image contains a person face by face recognition), and image URL as features.

After these steps, we get the annotated result from Web pages. For each Web page, the annotated person information includes the person’s name, title, organization, homepage, phone number, fax phone number, email address, depiction, and portrait. If m, Web pages are regarded as the Web pages for different people, we have m groups of such annotated results.

# 4.3.2 DBLP annotation

In DBLP, person information is well formed with person name, coauthors and detailed publication information. We parse the XML files of DBLP and get the related information about person name, coauthors’ name and the detailed paper publication information. As can be seen from this step, in DBLP, name disambiguation problem is not tackled. When different people have the same name, their publications are recorded under one person name.

After the annotations of Web page and DBLP, we merge the person information extracted from Web pages with the person’s publication information to generate the profile of person. During the merging, we use heuristic rules to check whether the profiles and the publications are from the same person.

# 4.4 Constructing the social network in Arnetminer

We perform the steps presented in Sections 4.2 – 4.3 to extract person information using the name list extracted from DBLP. We use coauthorship to be the relationship between persons. In Arnetminer, we have gathered 448289 persons and 725655 publications have been gathered. Totally, there are 2413208 relationships between persons with 5.38 relationships for each person on average.

We generate the FOAF file for each person in the social network. Because the extracted information may have errors or be out of date, Arnetminer provides an interface to let users to edit and download the FOAF file. Generated FOAF files can be downloaded and parsed by a FOAF parser to interoperate with other systems.

In the construction of Arnetminer, there are still some problems to be further investigated to make the information in Arnetminer more accurate. They are name disambiguation, name normalization and the improvement of current information extraction methods, the integration with more sources so that Arnetminer can provide more and accurate social network information.

# 5 Expert search in Arnetminer

Most current expert finding systems use Web pages related to the persons. In Arnetminer, we study how to find experts in a social network. In particular, computing the relevance of person local information to a given topic q and using the social network structure to assist expert relevance calculation.

We propose a relevance propagation expert finding that takes into consideration of both person local information (e.g., person’s profile and person’s publications) and person network information (e.g., relationships between persons). It is a two stage expert finding process: (1) relevancy calculation using person local information to a topic and (2) relevancy improvement using relationships between people. The people with top highest topic relevancy values are selected to be the experts for topic $q .$ Thus, the expert finding task is transformed into the calculation of topic relevance for each person given topic $q .$

# 5.1 Relevancy of person local information

Let $q = \{ t _ { 1 } , t _ { 2 } , . . . , t _ { n } \} , t _ { i }$ is a word in topic q and n is the number of words in q. Given $P L I ( x )$ and $P R I ( x )$ , we exclude publications from $P L I ( x )$ , because publication information is important to topic relevancy calculation and have different calculation methods from other information in $P L I ( x )$ . Let $P u b ( x )$ denote the publication information of person x, and $P L I _ { - } A ( x )$ denote the person local information with publication information of person x removed. $P u b ( x ) = \{ p _ { 1 } , p _ { 2 } , . . . , p _ { m } \} , p _ { i }$ is a paper of person x and is presented by its URI. m is the number of papers of person x.

Virtual documents are used to present the person local information of person $x , m + 1$ documents $d ( P L I _ { - } A ( x ) )$ , $d ( p _ { 1 } ) , d ( p _ { 2 } ) , . . . , d ( p _ { m } )$ are constructed.

$$
d (P L I \_ A (x))
$$

$$
= \left\{(w _ {l i}, c o u _ {i}) \left| \begin{array}{l} w _ {l i} \text {   occurred   in   } P L I \_ A (x), \\ c o u _ {i} \text {   is   the   number   of   occurenes   of   } w _ {l i} \\ \text {   in   } P L I \_ A (x) \end{array} \right. \right\}, \tag {3}
$$

$$
d (p _ {i}) = \left\{\left(w _ {p i}, c o u _ {i}\right) \middle | \begin{array}{c} w _ {p i} \text {   occurred   in   paper   } p _ {i}, \\ c o u _ {i} \text {   is   the   number   of } \\ \text {   occurenes   of   } w _ {p i} \text {   in   } d (p _ {i}) \end{array} \right\}. \tag {4}
$$

We use words occurred in person’s title, organization, depiction and topic interest to construct $d ( P L I _ { - } A ( x ) )$ . We also link to the homepage of person x through the URL of person’s homepage, and add the words occurred in the person $x ^ { \prime } \mathrm { s }$ homepage to $d ( P L I _ { - } A ( x ) )$ . In $d ( p _ { i } )$ document construction, we view the content of paper $p _ { i }$ as a document.

$r e l \_ l ( x , \ q )$ stands for the relevancy of person local information to topic q. It is defined as:

$$
\begin{array}{l} r e l \_ l (x, q) = \lambda \times r e l (d (P L I \_ (x)), q) + (1 - \lambda) \\ \times \sum_ {i = 1} ^ {m} w (p _ {i}) r e l (d (p _ {i}), q). \tag {5} \\ \end{array}
$$

In Eq. (5), $r e l ( d ( P L I _ { - } ( x ) ) , q )$ denotes the relevancy of person $x ' s$ local information to topic q except for his publication information. $r e l ( d ( p _ { i } ) , q )$ denotes the relevancy of paper $p _ { i }$ to topic $q , ~ w ( p _ { k } )$ represents the impact factor of the publication $p _ { k } . \lambda$ is the weight and $\lambda = 0 . 5$ .

Now, topic relevancy calculation for person x is converted into the calculation of topic relevancy of documents. We use the probability of a topic $q$ for a given document d to represent the document relevancy to topic $q .$ That is $r e l ( d , p ) = p ( q | d )$ . Furthermore, we assume that the words in document d and query q are conditionally independent from each other. Then we can get:

$$
p (q | d) = \prod_ {i = 1} ^ {n} p (t _ {i} | d), p (t _ {i} | d) = \frac {\operatorname{cou} (t _ {i} , d)}{\operatorname{cou} (t _ {i})}, \tag {6}
$$

where, $c o u ( t _ { i } , d )$ is the frequency of word $t _ { i }$ in document d. $c o u ( t _ { i } )$ is the frequency of word t in all documents. We use Eq. (7) to deal with the problem of zero probability.

$$
p (t _ {i} | d) = \beta \times p (t _ {i} | d) + (1 - \beta) \times p (t _ {i}). \tag {7}
$$

# 5.2 Relevancy propagation

In relevancy propagation, we propagate the topic relevancy of one person to his/her related persons. We use Eq. (8) to propagate rel(x, q).

$$
\operatorname{rel} (x, q) ^ {i + 1} = \operatorname{rel} (x, q) ^ {i} + \sum_ {e \in P R I (x)} \operatorname{co} (e) \times \operatorname{rel} \left(x ^ {\prime}, q\right) ^ {i}. \tag {8}
$$

In Eq. (8), co(e) is the weight of edge $\boldsymbol { e } = ( x ^ { \prime } , x , e _ { x ^ { \prime } x } )$ in relevancy calculation. $x ^ { \prime }$ is the person which has relationships with person x. $c o ( e ) = \frac { c o u ( x ^ { \prime } , x , e ) } { c o u ( x ) }$ for edge $e = ( x ^ { \prime } , x ,$ , $e _ { x ^ { \prime } x } )$ . In Arnetminer, $c o u ( x ^ { \prime } , x , e )$ is the number of papers which persons x and $x ^ { \prime }$ co-authored and $c o u ( x )$ is the number of papers of person x.

$R e l \_ l ( x , q )$ is used as the initial value of rel(x, q), rel(x, $q ) ^ { 0 } = r e l \_ { 1 } ( x , q )$ . After each iteration process, we use Eq. (9) to normalize the topic relevance value.

$$
\operatorname{rel} (x, q) ^ {i + 1} = \frac {\operatorname{rel} (x , q) ^ {i + 1}}{\max _ {x ^ {\prime} \in V} \left(\operatorname{rel} (x ^ {\prime} , q) ^ {i + 1}\right)}. \tag {9}
$$

# 5.3 Expert finding with relevancy propagation

From the description of Sections 5.1 and 5.2, Fig. 3 summarizes our relevance propagation expert finding algorithm.

The termination conditions can be a predefined number of iterations or a threshold for rel(x, q).

# 6 Association search in Arnetminer

In association search, the main difficulty is the time efficiency of the algorithm. A social network usually contains hundreds of thousands of nodes and millions of edges, and the response time to a user’s association search should be within a few seconds.

<table><tr><td>Algorithm: expert finding with relevance propagation</td></tr><tr><td>Input: a topic q and a social network G = (V, E)</td></tr><tr><td>Output: a ranked list of persons with the most expertise</td></tr><tr><td>Step 1: Initialization of rel(x, q) 
for each person x ∈ V {
    Construct m+1 documents:
    d(PLI_A(x)), d(p₁), d(p₂), ..., d(pₘ)
    Calculate rel_l(x, q) using equation (5);
    rel(x, q) = rel_l(x, q)</td></tr><tr><td>}</td></tr><tr><td>Step 2: Relevance propagation 
do {
    for each x ∈ V {
        Update rel(x, q) using equation (8);
    }
    Normalize rel(x, q) using equation (9);
} while (the termination condition is not satisfied);</td></tr><tr><td>Step 3: Output top m persons with maximal rel(x, q)</td></tr></table>

Fig. 3 Relevancy propagation expert finding algorithm

We propose a two stage association search method for association task asso(s, t), in which s and t are person IDs in the social network. In the first stage, we use heap-Dijkstra algorithm to quickly find the shortest paths from all persons v [ $V - \{ t \}$ in the graph to t with a running time of $O ( ( m + n ) \log ( n ) )$ ) where m is number of edges and n is the number of nodes in the social network. In the second stage, we propose a algorithm to enumerate all association paths with a path length that is no longer than $( 1 + \beta ) L _ { \mathrm { m i n } } .$ $L _ { \mathrm { m i n } }$ is the length of the shortest path from s to t, and b is the predefined threshold. It is implemented using the depth first graph search algorithm.

# 6.1 Heap based shortest association finding

Let ${ e _ { i j } } ^ { t }$ be a relationship between vi and $\nu _ { j }$ with relationship type $e ^ { t }$ in social network $G = ( V , G )$ , we use $w ( e _ { i j } ^ { \ t } )$ t o indicate the cost from one person $\nu _ { i } ~ \mathrm { t o }$ another person $\nu _ { j }$ with respect to relationship $e ^ { t } .$ So far, there is only the co-author relationship in the social network, so we omit t in ${ e _ { i j } } ^ { t } .$ . We define $w ( e _ { i j } )$ as $w ( e _ { i j } ) = \exp ( \lambda \cdot o _ { i j } )$ , where $e _ { i j }$ denotes the co-authorship between persons $\nu _ { i }$ and $\nu _ { j } ; ~ o _ { i j }$ is the number of papers that vi and vj have coauthored; l is a user-defined factor (l 5 0.15).

We use the heap-Dijkstra algorithm to search for the shortest paths from all people except t in the social network to person t at first, and get $p a t h _ { 1 } ( \nu , t )$ with path cost $f ( p a t h _ { 1 } ( \nu , t ) )$ where v[ $V - \{ t \}$ . We difine f() as the accumulation of weight $w ( e _ { i j } )$ along the edges of $p a t h _ { 1 } ( \nu , \ t )$ . The algorithm is shown in Fig. 4.

path(v) records the shortest path from each v[ $V - \{ t \}$ to t, and d (v) records the cost of the path. After this process, we can get the shortest path $p a t h ( \nu ) \ ( p a t h _ { 1 } ( \nu , t ) )$ and $f ( \nu )$ $( f ( p a t h _ { 1 } ( \nu , t ) ) )$ for each v[ $V - \{ t \}$ .

# 6.2 Near-shortest association path finding

In this stage, we implement a straightforward $s - t$ association enumeration algorithm using the depth first graph search. The algorithm extends an $s - s ^ { \prime }$ association to t along the relationship $e = ( s ^ { \prime } , ~ u ^ { \prime } )$ if and only if $d ^ { \prime } ( s ^ { \prime } ) +$ $w ( e ) + f ( u ^ { \prime } ) < ( 1 + \beta ) L _ { \mathrm { m i n } } .$ , where $d ^ { \prime } ( s ^ { \prime } )$ is the cost of current $s - s ^ { \prime }$ association which is calculated during the process of the depth first graph search.

Whenever an association $p a t h ( s , \ t )$ is found using the above method, we calculate the cost of the association $f ( p a t h ( s , \ t ) )$ by accumulating the weights of all relationships included in the association path and adding the path with its cost to the association set.

In the depth first graph search, we restrict the length of an association to be less than a pre-defined threshold max\_length. We tentatively set it to be 7 in our experiments. This length restriction can reduce the computational cost. The same value is used in Milgram [37].

The search terminates when no more associations can be found. Then we rank all $p a t h _ { i } ( s , \ t )$ with the lowest f(pathi (s, t)) on the top.

# 7 Implementation and experiments

# 7.1 Arnetminer implementation

Referring to the Arnetminer framework described in Fig. 2, using the extraction and search algorithms described in Sections $4 { \cdot } 6 ,$ we implement an expertise oriented search system Arnetminer. We first generate a list of person names using DBLP, and then construct the social network. We use indexing technique in SWARMS [32] and Jena [31] to store and manage the data in the social network. And we provide a Web interface to perform expertise oriented search in Arnetminer. Also, we provide users an interactive environment to allow them to establish, modify and download the person information. The generated FOAF files can be reused and interoperated with other systems so that the person information can be shared across systems.

<table><tr><td>Algorithm: Heap Dijkstra algorithm</td></tr><tr><td>Input: Asso(s, t) and graph G = (V, E);</td></tr><tr><td>Output: find the shortest paths path1(v, t) from each node v ∈ V-{t} to node t</td></tr><tr><td>1. for each v ∈ V-{t} { path(v) ← φ, f(v) ← ∞; c(v) ← 0};</td></tr><tr><td>2. f(t)=0;</td></tr><tr><td>3. heap ← create a minimal heap;</td></tr><tr><td>4. insert t into heap;</td></tr><tr><td>5. while (heap is not empty){</td></tr><tr><td>6. v_min ← remove minimal node from heap;</td></tr><tr><td>7. c(v_min) ← 1;</td></tr><tr><td>8. E(v_min) ← all edges pointing to the node v_min;</td></tr><tr><td>9. foreach (e_min ∈ E(v_min)){</td></tr><tr><td>10. if( c(u) = 0 &amp;&amp; w(e_min) + f(v_min) &lt; d(u) ){</td></tr><tr><td>11. f(u) ← w(e_min) + f(v_min);</td></tr><tr><td>12. path(u) ← v_min;</td></tr><tr><td>13. if ( isinheap(u) ) {heap.moveUp(u);} else {heap.insert(u);}</td></tr><tr><td>14. }</td></tr><tr><td>15. }</td></tr><tr><td>16.}</td></tr></table>

Fig. 4 Heap-Dijkstra algorithm

In the person search, the average time of extracting a person information from the Web and DBLP varies from few seconds to half dozen seconds depending on the internet speed when the person’s information is not in Arnetminer. In expert search, the average search time is 7.8 seconds testing on expert finding tasks on 10 topics. In association search, the average search time for association finding in the network is less than 3 seconds.

# 7.2 Test data preparation

Among the four type searches, person search and publication search use metadata based keyword search which are widely used on the Web. We focus our evaluation on expert search and association search.

We have implemented the system in Java programming language with JDK 1.5.

All experiments were carried out on a Server running Windows2003 with two Dual-Core Intel Xeon processors (2.8 GHz) and 3-gigabyte memory. Run time does not include the time required to load the social network and the time to output the associations.

For expert search, standard data collection is difficult. How could we say that a person is an expert on a certain topic? It is usually subjective. In order to make our data sets commonly acceptable, we assume that an expert is often active in the committees of the top conferences and organizations in his/her related research topics. Therefore, we chose 5 topics and collected 5 lists of experts from the committees as the standard evaluation metrics. Table 3 shows the topics and the statistics of the experts. OA, SW, DM, IE and SVM are 5 test data sets. They are the abbreviation of Ontology Alignment, Semantic Web, Data Mining, Information Extraction and Support Vector Machine respectively. #Expert shows the number of experts we collected in each topic. The ‘source’ column means the website from which we obtain the expert list for a topic. These test sets can be found in website: http://keg.cs.tsinghua.edu.cn/project/ PSN/dataset.html.

Table 3 Expert lists on five research topics 

<table><tr><td>topic</td><td>#Expert</td><td>source</td></tr><tr><td>OA</td><td>57</td><td>PC Members of EON2003, OAEI2005&amp;2006, OM workshop2006</td></tr><tr><td>SW</td><td>412</td><td>PC Members of ISWC2001 — ISWC2006</td></tr><tr><td>DM</td><td>351</td><td>http://www.kmining.com/info_people.html</td></tr><tr><td>IE</td><td>91</td><td>http://www.isi.edu/infoagents/RISE/people.html</td></tr><tr><td>SVM</td><td>111</td><td>http://www.svms.org/people-frames.html</td></tr></table>

The test data used in association search are people pairs from our social network and five expert sets. The number of people pairs in each test set is 1 000. Data set Random contains the people pairs randomly selected from the social network. Two data sets SW\_P and DW\_P contain the people pairs from the same research topic of SW and DM. The last two data sets DM\_SW\_P and SW\_OA\_P contain the people pairs from two different research fields. For a people pair in DM\_SW\_P, one person is selected from experts for topic DM, and the other person is selected from experts for topic SW. Data set DM\_OA\_P is constructed in the same way as DM\_SW\_P. We use these five test data sets to evaluate the time performance for association search. We want to evaluate if our proposed method is efficient and if the time efficiency will be affected by the association paths between people from different researcher topics. We assume that people on different research topics will have longer association paths than people on the same research topic.

# 7.3 Expert finding evaluations

We use the expert finding evaluation methods provided in [5,26]. We define precision as the percentage of correctly found experts in the results. If the expert whom the algorithm finds is in the data set we collect, it is a right answer; otherwise, it is wrong. We use the ratio of the number of right answers to the number of experts in test set as precision. P@5 measures the precision in the top 5 returned experts for a topic, and P@10, P@20 are all calculated similarly. R-prec measures the precision after top R target experts are correctly found for a given topic. MAP is the mean of the precision scores obtained after each target expert is found, using zero as the precision for experts that are not correctly found. bpref focuses on the proportion of the wrongly identified experts.

We use EFB, EFL and EFF to denote the traditional IR based expert finding, local relevance calculation expert finding and relevancy propagation based expert finding respectively. In EFB, we first create a ‘document’ for each person by combining all his person local information (including publications) from the social network. Then given a topic, it queries the ‘document’ set to find which documents are most relevant to the topic. In EFL, we use Eq. (5) to perform expert finding and in EFF, we use the relevance propagation Eq 5. (5) and (8) to perform expert finding. Figure 6 shows the results of these three kinds of methods.

As can be seen from Table 4, our methods can achieve high performances 5 in most tasks.

(1) EFF significantly outperforms EFB. It means that our method is better than the conventional IR based expert finding method.   
(2) In almost all evaluations, EFF significantly outperforms EFL. It means that the relevancy propagation is effective for the expert finding task in a social network.

Table 4 Experimental results for 5 topics (%) 

<table><tr><td>topic</td><td>method</td><td>P@5</td><td>P@10</td><td>P@20</td><td>P@30</td><td>R-prec</td><td>MAP</td><td>bpref</td></tr><tr><td rowspan="3">OA</td><td>EF_B</td><td>0.00</td><td>0.00</td><td>15.00</td><td>16.67</td><td>11.11</td><td>2.50</td><td>8.53</td></tr><tr><td>EF_L</td><td>20.00</td><td>30.00</td><td>20.00</td><td>26.67</td><td>21.28</td><td>4.99</td><td>12.43</td></tr><tr><td>EF_F</td><td>60.00</td><td>50.00</td><td>30.00</td><td>23.33</td><td>16.67</td><td>6.17</td><td>11.60</td></tr><tr><td rowspan="3">SW</td><td>EF_B</td><td>0.00</td><td>0.00</td><td>0.00</td><td>0.00</td><td>5.65</td><td>0.22</td><td>1.90</td></tr><tr><td>EF_L</td><td>80.00</td><td>70.00</td><td>70.00</td><td>60.00</td><td>71.43</td><td>9.98</td><td>16.37</td></tr><tr><td>EF_F</td><td>80.00</td><td>90.00</td><td>95.00</td><td>76.67</td><td>90.91</td><td>12.52</td><td>18.02</td></tr><tr><td rowspan="3">DM</td><td>EF_B</td><td>0.00</td><td>0.00</td><td>0.00</td><td>0.00</td><td>0.80</td><td>0.02</td><td>0.60</td></tr><tr><td>EF_L</td><td>80.00</td><td>70.00</td><td>60.00</td><td>56.67</td><td>71.43</td><td>9.98</td><td>15.45</td></tr><tr><td>EF_F</td><td>80.00</td><td>80.00</td><td>80.00</td><td>70.00</td><td>83.33</td><td>11.38</td><td>16.84</td></tr><tr><td rowspan="3">IE</td><td>EF_B</td><td>0.00</td><td>0.00</td><td>5.00</td><td>3.33</td><td>2.72</td><td>0.38</td><td>0.89</td></tr><tr><td>EF_L</td><td>80.00</td><td>70.00</td><td>65.00</td><td>53.33</td><td>71.43</td><td>19.52</td><td>22.88</td></tr><tr><td>EF_F</td><td>100.00</td><td>90.00</td><td>55.00</td><td>53.33</td><td>90.91</td><td>20.11</td><td>22.63</td></tr><tr><td rowspan="3">SVM</td><td>EF_B</td><td>0.00</td><td>0.00</td><td>5.00</td><td>3.33</td><td>3.75</td><td>0.79</td><td>0.81</td></tr><tr><td>EF_L</td><td>40.00</td><td>20.00</td><td>15.00</td><td>13.33</td><td>3.91</td><td>2.80</td><td>6.07</td></tr><tr><td>EF_F</td><td>40.00</td><td>20.00</td><td>10.00</td><td>13.33</td><td>8.55</td><td>1.79</td><td>6.01</td></tr></table>

(3) EFL outperforms EFB. It means that the topic relevance calculation using Eq. (5) for person local information is more effective than the IR based expert finding. Our approach can achieve a high accuracy on most of the topics. In terms of P@5, for example, the precision range from 60.00% to 100% except for topic SVM.

# 7.4 Association search evaluation

We also evaluate our association search algorithm in Arnetminer. We use the average run time performance on test set to evaluate our method and compare it with other methods.

We compare our method named DeSt with the method of brute force enumeration method named BrSt. In BrSt, we directly conduct the depth-first graph search on the social network to find associations with the length which is less than the threshold max\_length. We also compare our method with another two-stage association search method named ToSt. In ToSt, in the first stage, it makes use of the conventional Dijkstra algorithm to find the shortest path, and in the second stage it uses the depthfirst graph search to find associations whose lengths are less than the threshold max\_length. The method in the second stage is similar to that in our proposed algorithm. Table 5 gives the test result of these three methods.

As can be seen from Table 5, our proposed method DeSt achieves a high time performance in all of the association search tasks. Our approach can find associations less than 3 seconds on most of the test sets. ToSt uses nearly more than four hundred times of our approach. The BrSt uses nearly 100 times of our approach. Also, we can see that the time performance on data set Random is the longest time among all tasks. It shows that two people on different research fields may have longer association paths and need to spend more time to search for their associations. The result of SW-OA\_P is less than 3 seconds because ontology alignment is a sub research topic in Semantic Web, so the researchers from these two fields should not have long association paths.

Table 5 Experimental results for association search (seconds) 

<table><tr><td>test set</td><td>method</td><td>total time</td><td>avg. time</td></tr><tr><td rowspan="3">Random</td><td>BrSt</td><td>669000</td><td>669.00</td></tr><tr><td>ToSt</td><td>1171702</td><td>1171.70</td></tr><tr><td>DeSt</td><td>3553</td><td>3.53</td></tr><tr><td rowspan="3">SW_P</td><td>BrSt</td><td>161050</td><td>161.50</td></tr><tr><td>ToSt</td><td>1129391</td><td>1129.39</td></tr><tr><td>DeSt</td><td>2752</td><td>2.75</td></tr><tr><td rowspan="3">DM_P</td><td>BrSt</td><td>16474</td><td>16.474</td></tr><tr><td>ToSt</td><td>1181133</td><td>1181.13</td></tr><tr><td>DeSt</td><td>2734</td><td>2.734</td></tr><tr><td rowspan="3">DM-SW_P</td><td>BrSt</td><td>969437</td><td>869.44</td></tr><tr><td>ToSt</td><td>1173969</td><td>1173.70</td></tr><tr><td>DeSt</td><td>3010</td><td>3.01</td></tr><tr><td rowspan="3">SW-OA_P</td><td>BrSt</td><td>373250</td><td>373.25</td></tr><tr><td>ToSt</td><td>1171182</td><td>1171.18</td></tr><tr><td>DeSt</td><td>2714</td><td>2.714</td></tr></table>

# 7.5 Arnetminer experiences

In the implementation of Arnetminer, we have following problems which need to be investigated in the future. For example:

Name disambiguation In Arnetminer, only heuristic rules are used, though these rules are effective, but we can not disambiguate the cases which fall out of the rules. In the future, we can also use and develop other statistical name disambiguation methods.

Other kinds of relationships In Arnetminer, we use the co-author relationship as the relationship in a social network. In the future, we will extract other relationships, for example, the relationship of co-organization and co-project etc.

FOAF file integration In the current system, we use the Google search API to locate the pages related to a person and use DBLP as another source to create the social network. FOAF is an important sources to get person description and more and more FOAF files are on the Web. We can further integrate FOAF files on the Web to get more information about a person.

# 8 Conclusions

In this paper, we present how to provide expertise oriented search through a social network. We introduce our experience on implementing an expertise oriented search (Arnetminer) system. By using data on the Web and public sources such as DBLP and Citeseer, we construct a social network. We then employ a relevancy propagation expert finding algorithm to find experts on given topics. We also propose a two stage association search algorithm to efficiently search for top association paths in the social network.

We implement Arnetminer and conduct comprehensive experiments to evaluate its performance. Current system is in the computer science research community. The framework of social network construction and the algorithms for person search, expert search, associate search and publication search, however, can be applied for people search in the social networks of other domains.

The system is in operation on the internet for about two years and receives accesses from about 1500 distinct users per month. Feedbacks from users and system logs indicate that users consider the system can really help people to find and share information in the academic community.

Acknowledgements This work was supported by the National Natural Science Foundation of China (Grant Nos. 90604025, 60703059).

# References

1. Citeseer. http://www.citeseer.nec.com   
2. Aleman-Meza B, Nagarajan M, Ramakrishnan C, et al. Semantic analytics on social networks: experiences in addressing the problem of conflict of interest detection. In: Proceedings of WWW’ 06. New York: ACM, 2006, 407–416   
3. Hettich S, Pazzani M J. Mining for proposal reviewers: lessons learned at the national science foundation. In: Proceedings of KDD’ 06. New York: ACM, 2006, 862–871   
4. Golbeck J. Web-based social networks: a survey and future directions. Technique Report   
5. Brickley D, Miller L. FOAF vocabulary specification. Namespace Document, http://xmlns.com/foaf/0.1/   
6. Kruk S R, Decker S. Semantic social collaborative filtering with FOAFRealm. In: Proceedings of the Semantic Desktop Workshop. Galway, Ireland, 2005   
7. Foafnaut. http://www.foafnaut.org/   
8. Flink. http://flink.semanticweb.org/   
9. Culotta A, Bekkerman R, McCallum A. Extracting social networks and contact information from email and the web. In: Proceedings of Email and Spam. AAAI 2004   
10. Kautz H, Selman B, Shah M. Combining social networks and collaborative filtering. Communications of the ACM, 1997, New York: ACM, 40(3): 63–65   
11. Mika P. Flink: Semantic Web technology for the extraction and analysis of social networks. Web Semantics: Science, Services and Agents on the World Wide Web, 2005, 3(2): 211–223   
12. Matsuo Y, Mori J, Hamasaki M. POLYPHONE: an advanced social network extraction system from the web. In: Proceedings of WWW’ 06. New York: ACM, 2006, 397–406   
13. Balog K, Rijke M d. Searching for people in the personal work space. In: Proceedings of International Workshop on Intelligent Information Access, 2006   
14. Ding L, Finin T, Joshi A, et al. Swoogle: a search and metadata engine for the semantic web. In: Proceedings of the International Conference on Information and Knowledge Mangement. New York: ACM, 2004, 652–659   
15. Libra. http://libra.msra.cn/   
16. Rexa. http://rexa.info/   
17. Doan A, Ramakrishnan R, Chen F, et al. Community information management. Data Enginneering, 2006, 29(1): 64–72   
18. Hawking D. Challenges in enterprise search. In: Proceedings of the 15th Australasian database conference. Australia: Australian Computer Society, Inc, 2004, 15–24   
19. Nascimento M A, Sander J, Pound J. Analysis of SIGMOD’s coauthorship graph. ACM SIGMOD Record, 2003, 32(3): 8–10   
20. Smeaton A F, Keogh G, Gurrin C, et al. Analysis of papers from twenty-five years of SIGIR conferences: what have we been doing for the last quarter of a century. ACM SIGIR Forum, 2002, 36(2): 39–43

21. Campbell C S, Maglio P P, Cozzi A, et al. Expertise identification using email communications. In: Proceedings of CIKM’ 03. New York: ACM, 2003, 528–531   
22. Schwartz M F, Wood D C M. Discovering shared interests using graph analysis. Communications of the ACM, 1993, 36(8): 78–89   
23. Foner L N. Yenta: a multi-agent, referral-based matchmaking system. In: Proceedings of First International Conference on Autonomous Agents. New York: ACM, 1997, 301–307   
24. Mattox D, Maybury M, Morey D. Enterprise expert and knowledge discovery. In: Proceedings of HCI. Mahwah: Lawrence Erlbaum Associates, Inc, 1999, 303–307   
25. Seid D Y, Kobsa A. Expert finding systems for organizations: problem and domain analysis and the demoir approach. Journal of Organizational Computing and Electronic Commerce, 2003, 13: 1–24   
26. Craswell N, Vries A P D, Soboroff I. Overview of the trec-2005 enterprise track. TREC 2005 Conference Notebook. 2005, 199–205   
27. Fu Y, Yu W, Li Y, et al. THUIR at trec 2005: enterprise track. In: Proceedings of TREC’ 05. 2005, 733–738

28. Cao Y, Liu J, Bao S, et al. Research on expert search at enterprise track of trec 2005. In: Proceedings of TREC’ 05. TREC, 2005   
29. Adamic L, Adar E. How to search a social network. Social Networks, 2005, 27: 187–203   
30. Foaf. http://xmlns.com/foaf/0.1/   
31. Carroll J J, Reynolds D, Dickinson I, et al. Jena: implementing the semantic web recommendations. In: Proceedings of WWW’ 04. New York: ACM, 2004, 74–83   
32. Liang B, Tang J, Li J. SWARMS: a tool for exploring domain knowledge. In: Proceedings of the Workshop of Contexts and Ontologies on the 20th International AAAI Conference. 2005, 120–123   
33. DBLP. http://www.informatik.uni-trier.de/,ley/db/   
34. Vapnik V. Statistical learning theory. New York: Springer Verlage, 1998   
35. Tang J, Li J, Lu H, et al. IASA: learning to annotate the semantic web. Journal of Data Semantics, 2005, 4: 110–145   
36. Tang J, Li H, Cao Y, et al. Email data cleaning. In: Proceedings of KDD’ 05. New York: ACM, 2005, 489–498   
37. Milgram S. The small world problem. Psychology Today, 1967, 2: 60–67