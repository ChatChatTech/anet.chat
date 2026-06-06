# Reliable Response Delivery in Peer-to-Peer Systems

Xiaomei Liu $^{1}$ , Yunhao Liu $^{2}$ , Li Xiao $^{1}$

$^{1}$ Department of Computer Science and Engineering, Michigan State University, USA $^{2}$ Department of Computer Science, Hong Kong University of Science & Technology, Hong Kong liuxiaom@cse.msu.edu, liu@cs.ust.hk, lxiao@cse.msu.edu

# Abstract

Unstructured peer-to-peer (P2P) system is the prevalent model in today's P2P system. In such systems, a response is sent along the same path that carried the incoming query message. To guarantee the anonymity of the requestor, no requestor information is included in the query message and each node in the query incoming path only knows its immediate neighbors who sent the query request to it. This mechanism introduces response loss when any one node or connection in the path fails, which is a general case in the P2P system due to its dynamic nature. In this paper, we aim at addressing the response loss problem and present three techniques to alleviate this problem: redundant response delivery (RRD) scheme as a proactive approach, adaptive response delivery (ARD) scheme as a reactive approach, and extended adaptive response delivery to render ARD to function in an unstructured P2P system with limited or no flooding based search mechanism. With limited traffic overhead, all three techniques reduces response loss rate by more than 65% and they are all fully distributed.

# 1. Introduction

Aimed at efficient utilization of Internet edge resources, peer-to-peer file sharing systems have received much attention since the emergence of Napster. P2P systems can be divided into two different categories[9]: structured, and unstructured. Although a structured P2P system greatly reduces the overhead of file locating, its weakness in partial/keyword search and additional DHT table maintenance cost impedes its application in the real world. The overwhelmed web traffic contributed by peer-to-peer system which makes it as a leading consumer of Internet bandwidth almost all comes from unstructured P2P system[14]. Our research focuses on the unstructured P2P system.

In unstructured P2P systems, such as Gnutella [2] and KaZaA [3], files are randomly distributed among peers. There is no connection between file placement and network topology. File locating is generally concluded based on the flooding search mechanism: each source peer makes duplicate copies of a query it receives and broadcasts to all its directly connected neighbors except the one that delivered the incoming message in each forwarding step. The duplication process only terminated when the TTL value of the query reduces to zero or a satisfying result has been found. This flooding mechanism is widely adopted in unstructured P2P systems due to its simplicity and robustness of node failure. Another benefit of the flooding search mechanism is that it provides anonymity for the query requestor: no information of query requestor is included in the query request message and the peers who received the request only know the query message id and the neighbors who sent this message to it. To reduce the search traffic in the system, the response delivery process in the unstructured P2P system does not adopt a flooding mechanism. If a peer receives a query message and can satisfy this query, it will send a response along the same path the query came from: each peer on the path sends a response to the first neighbor who sent the incoming query to it.

The unstructured P2P system is a highly oscillating system. Peer membership is ad-hoc and dynamic due to the lack of a dedicated and centralized authority in the system. Although a flooding-based search mechanism is robust in node failure, the response message will be lost if any node on the response path fails. One may argue that loss of some response messages is not a big issue since multiple responses may be found for one query. However, our simulations show that 35% of the responses are lost in a P2P system, which is not a negligible loss. In existing P2P systems, the most popular search method is keyword search and that means search results will not be exactly what a user wants most of the time. More search results for a query provide more chances for a user to find what he/she really needs. Also, it is obvious that all network resources used to find the response are also wasted when a response is lost.

To reduce the response loss rate and utilize network resources more efficiently, we present three techniques, reversed redundant response delivery (RRD), adaptive response delivery (ARD), and extended adaptive response delivery (e-ARD), all three of which handle the response loss problem regardless of node failure or node departure. In RRD, the responder proactively sends back duplicate copies of the same response via different paths to avoid response loss. In ARD, peers in a response path automatically choose alternative paths in case of node failure or departure. The e-ARD extends the ARD mechanism to avoid response loss in P2P systems with limited or no broadcasting searching mechanisms. Among the three schemes, RRD makes least modification to current P2P systems and returns responses faster than ARD on average. ARD outperforms of RRD in both effectiveness and traffic overhead. The e-ARD performs best among the three in almost all aspects. However, it requires more modification for existing systems than the other two techniques and may also add extra overhead to the system.

The remainder of the paper is organized as follows. Section 2 overviews the related work of this research. Section 3 describes proposed response returning techniques. Simulation methodology and performance evaluation are presented in Section 4 and 5. Finally, we conclude our work in Section 6.

# 2. Related work

Authors in [5] also noticed the response loss problem and expected the optimization technique they proposed may make the case worse. They proposed to stop forwarding the query earlier than to stop forwarding the response, or to set a time threshold and re-issue the query when it can not be satisfied within the time limit. However, both techniques cannot help for the response loss problem caused by the inherent P2P system oscillation. The first technique needs the cooperation of each peer and thus only helps to make up the response loss caused by their proposed technique of adjusting overlay topology. The second technique may reduce the unnecessary query re-issuing traffic in the case of slow response, but it provides no benefit in reducing traffic and potential extra response delay caused by the lost responses. We also noticed the problem during our work in [8] and we realize that, with more optimization techniques being used to limit the query traffic, this problem will become more serious. This also motivates us to further investigate this problem.

Research has been done to provide fault tolerance in structured P2P systems[17, 18]. However, their target is different from ours in that fault tolerance needs to be provided in the whole search process in a structured P2P system, while in our case, we only need to provide fault tolerance to the response message. We expect no modifications in query request process and thus our technique can be seamlessly combined with existing query mechanism or most of the proposed search optimization mechanisms which focus on query request process. In addition, in structured P2P systems, a node is tightly controlled and node information can be used to construct fault tolerance strategies. However, in unstructured P2P systems, the only information a peer has is on itself and its neighbors.

Message delivery in an ad hoc network may also fail due to node motion. However, routing mechanisms used in an ad hoc network [7, 10, 11] cannot be used to solve the problem in P2P systems. In an ad hoc network the source node and destination node know each other, while in a P2P system there is the requirement of anonymity during the query process. In addition, the delivery algorithm in an ad hoc network generally adopts broadcasting in a wireless network, which should be avoided in the response delivery process. To the best of our knowledge, no effective solution has been proposed to deal with the response loss problem incurred by the unstructured P2P system itself.

# 3. Response delivery optimization

Before presenting our techniques of response delivery optimization, we would like to define forwarding neighbor and primary forwarding neighbor first. During the query process, if a neighbor of peer p forwards a copy of this query message to p, then this neighbor is p's forwarding neighbor. Among all the forwarding neighbors of p, the first one that forwards the copy of this query to p is called primary forwarding neighbor. In existing P2P system, p always sends back responses to its primary forwarding neighbor. All of our three techniques are based on the observation that the amount of forwarding neighbors of a peer in a flooding based query mechanism is more than one in most of the cases. However, the third mechanism presented of e-ARD also takes the case that only one forwarding neighbor is available during the query process.

![](images/7431e3b9290dc1494b4b76bbc9ae77ffaeb7c6302aa400868ad171ced002653d.jpg)



Fig 1 Response loss problem in P2P system

# 3.1. Response loss problem

The P2P system is a highly resilience system in that peers come and go frequently. Even when the peers keep alive in a system, they may adjust their connections with a high frequency. Previous studies show that a peer's lifetime varies from less than 10 minutes in FastTrack [13] to 60 minutes in Gnutella and Napster [15]. Uptime of logical connections is obviously even shorter than individual peers, from 1 minute or less to 24 minutes [12]. In addition, many new techniques trying to improve the performance of P2P system also require peers to adjust their connections to find better neighbors or achieve optimized overlay topologies[5, 8]. This further increases the dynamic nature of P2P systems.

To reduce the response traffic, responses will be sent back to requestor along the query incoming path instead of flooding. In addition, to keep requestor's anonymity, no requestor information is included in the request/response message. Peers on the response path only depend on the local knowledge of their primary forwarding neighbor to route the response. Thus, the response message will be thrown away if the primary forwarding neighbor fails. For example, in Fig. 1, peer S issues a query and peer T has a response for the query. The response is sent back along the incoming query path A→B→C→D. If any one of A, B, C or D leaves after it forwards the query, or any connection in any two of these node changes, a response loss occurs. In this case, network resources for both response return and original query propagation are wasted.

# 3.2. Redundant response delivery (RRD)

Making a backup copy of vulnerable/critical components of the system is a common technology to improve the system's fault tolerance. The redundant response delivery (RRD) scheme also tries to alleviate the response loss problem via backup paths in case of path failure. However, the success of using backup paths is based on whether such paths are available, i.e. whether the same query message can be forwarded to the same node from more than one path. This is intuitively true for a flooding query delivery system in a highly connected network. It is also attested to by the result of our simulation: without any extra specification of the query transfer, except flooding, and network topology kept consistent with those of the real world, RRD does significantly reduce response loss rate. One issue about RRD deserving mention is that it is totally different from a flooding/broadcast delivery system: in RRD scheme, only responder issues responses to multiple selected neighbors, each other node in the path still forwards the response to its primary forwarding neighbor. In this sense, RRD is more like the k-walker mechanism discussed in [9].

We illustrate RRD here with an example. Fig. 1 supposes that peer S floods a query, and peer T has a response for the query. According to Gnutella 0.6 protocol [2], if peer A is T's primary forwarding neighbor, T will send back the response via A and discard the same query message from other forwarding neighbors, such as G, M and F. The path for T to send back a response to S is A→B→C→D. If any of the peers on the path fails or leaves, the response will be lost. Instead of returning a response through one path, the RRD scheme adds one or more redundant response paths. For the same example, in addition to sending a response back immediately to A, T also selects one of the other forwarding neighbors (F, G, or M) as back up neighbors with redundancy probability γ, which is determined by the number of extra paths the system needs and the number of forwarding neighbors, and sends a response back through each of the selected neighbors. All other peers will drop response messages with the same message ID previously received. With the traffic overhead of redundant response delivery, RRD can effectively improve the response success rate in a dynamic P2P environment.

The deployment of RRD completely relies on the local information of a node. It creates very limited computation overhead for responder in choosing multiple neighbors to send back the responses. But it creates extra network traffic overhead, which is proportional to the number of redundant paths. However, the response traffic along one path is very limited, in order of O(1) and restricted by the maximum TTL, which is suggested as 7 in [2]. The extra response traffic along redundant paths is also limited and still in order of O(1), restricted by maximum TTL and $\gamma$ . On the other side, the improvement of response return rate with few extra paths is already very impressive. In our simulation, with average node degree of 6 and $\gamma = 0.2$ , the response loss rate can be reduced by $65\%$ .

# 3.3. Adaptive response delivery (ARD)

In the adaptive response delivery (ARD) scheme, each peer keeps a forwarding neighbor list for each query message within a certain period of time. The format of each item in the forwarding neighbor list is <Message ID, Forwarding Neighbor>. The primary forwarding neighbor of this peer will not be recorded in its forwarding neighbor list.

The basic idea of ARD is as follows. If a peer in a response path finds that the next hop cannot be reached, he will check his forwarding neighbor list to see if other neighbors also forwarded the same query message to him. If so, he will select in the list the first to arrive and reroute the response to this forwarding neighbor. Otherwise, he will send a failure message with the query message ID and the information about his neighbors who cannot be reached to his previous hop who will try to reroute the response. Gnutella 0.6 protocol [2] suggests that the TTL of a response should be set to at least the hops value of the responding query plus 2. ARD needs to set a much larger TTL in order to route the response back to the initiator.

Take Fig. 2 as an example for ARD. Peer A issues a query that is flooded to many peers. Peer P receives the query and finds that he has a response for the query. Assume the query path with the primary forwarding neighbor for P is A→B→F→P. We consider the case that B fails or leaves after it forwarded the query to F. When F receives a response from P and tries to send the response to B, F will find that he cannot reach B. With ARD, F will first check his forwarding neighbor list for this query and select in the list the first to arrive. Here, F chooses G as his new forwarding neighbor. When G receives the response, he again finds that B is non-reachable and picks E to return the response. Peer E will eventually send the response back to A via C or D depending on which one first forwards the query message to E. Another case is that both B and G leave. Peer F will inform his previous hop, P, that he cannot deliver the response through all his forwarding neighbors, i.e. B and G. Peer P will pick H to reroute the response.

We need to discuss the update frequency of the forwarding neighbor list. Update frequency is $1/T_{wait}$ if we define $T_{wait}$ as the average lifetime of a forwarding neighbor record in the forwarding list. A forwarding neighbor record will be removed from the list if $T_{wait}$ expires. Thus it is important to select the right value of $T_{wait}$ . If $T_{wait}$ is set too small, a forwarding neighbor record may be removed before the response is sent back to this peer. If $T_{wait}$ is set too large, the overhead for each peer to keep the forwarding neighbor lists will be very high. The value of $T_{wait}$ is related to the average response time that is defined as the time difference from when a responder sends a response to when the initiator receives the response.

We will show that ARD, a simple resilient forwarding technique, is able to increase response success rate with low traffic cost, especially when many peers fail in a system. Compared with RRD, the additional traffic overhead in ARD is small because ARD only reroutes a response if necessary. Our simulation shows that the traffic caused by the adaptive delivery algorithm is close to that of the original response.

One may also concern that adaptive response delivery (ARD) will perform poorly in the case that only a few or none of the peers have multiple forwarding neighbors. However, like we mentioned in the case of RRD, this is rare in the unstructured P2P system and even when this case happens, a peer can return the response to the node that delivered the response to it, which can provide a second chance to reroute the response message to other peers.

# 3.4. Extended adaptive response delivery (e-ARD)

Both RRD and ARD will not be effective in the case that there is only one forwarding neighbor available for a peer. Although this situation rarely happens in most of flooding-based P2P systems, it may happen in a higher frequency with the adoption of new techniques removing unnecessary node connection.

We extended ARD technique to be effective even in this case. In e-ARD mechanism, an IP address used for adaptive response delivery is appended in each query message. When the next hop neighbor in the response transfer path fails, in addition to forwarding the response to an alternative neighbor, the peer can also forward the response to the node with this IP address. One important issue that cannot be ignored here is that we must keep the requestor's anonymity during the process. Thus, we cannot simply append the requestor's address in the query message. In e-ARD, we achieve the requestor's anonymity by introducing the backup response delivery agent (bRDA).

![](images/4acdab2c33bf56982d7489f917cb2cfca01be60062ac91f5474ab857e4317447.jpg)



Fig 2 Adaptive response routing

3.4.1 Backup response delivery agent (bRDA). In the e-ARD scheme, we define type II query request/response messages by adding a new field of bRDA address based on query request and response message specified in Gnutella 0.6 [2]. During the query process, type II request/response messages will be issued.

When a requestor makes a query request, it will put its own address in the field of bRDA Address of the request message with a wrap probability $\alpha$ and broadcast it to all its neighbors. The peer who received the query will decide with a wrapping probability of $\alpha$ whether it will replace the bRDA address in the query message with its own IP address. We call the node that decided to append its own IP address to the query message the backup response delivery agent (bRDA). When a bRDA appends its own IP address in the query message, it also stores the old bRDA address in the query message in its forwarding neighbor list. In e-ARD, each entry in the forwarding neighbor list is extended to <message ID, pre-bRDA address, forwarding neighbor 1, forwarding neighbor2, etc>. For the node which is not the bRDA, the pre-bRDA address of the related record is NULL. A responder will copy the bRDA address of the received query to its response message. During the response delivery process, a node will check its neighbor list and see if it is the bRDA of the related message. If it is, it will remove the IP address in the response message and append the previous bRDA address stored in its forwarding neighbor list in the response message.

3.4.2. Wrapping probability $\alpha$ . It is important to take a proper value of wrapping probability. If it is too big, most of the nodes in the query-incoming path will become bRDA. This will consume too much of local resources and reduce the response return efficiency. An extreme case is to set $\alpha$ as 1. This reduces e-ARD to ARD. On the other side, if $\alpha$ is too small, then one can always consider the backup path address in the query message is the address of requestor and thus can not guarantee the anonymity of the requestor. Here we recommend taking $\alpha$ from 0.35 to 0.7. We compute the value of $\alpha$ based on the following equation:

$$
\alpha = 0. 3 5 + \omega \times (1 - \frac {c}{\phi (T _ {o n}) + c}) \quad \text { where } \quad \omega = 0. 4, \mathrm{c} \text { is   a }
$$

constant decided by the application, and $T_{on}$ is the peer's on line time. Both c and $\phi(T_{on})$ will affect the increase trend of $\alpha$ . In our simulation we take $\phi(T_{on}) = T_{on}\log(T_{on} + 1)$ . If we assume there are k hops for a query to be satisfied and f is the probability of the bRDA address being changed at least once by any of the nodes on the whole query path, then $f = 1 - (1 - \alpha)^{k-1}$ . Thus we can see that even when all nodes in the query path take the value of $\alpha$ as base probability 0.35 and in a case that query path length is only as short as three hops, f will be 0.578 which means there is still a fairly big chance for the bRDA address to be changed.

3.4.3. Extended adaptive response delivery. When a node receiving the response message finds that its primary forwarding neighbor for this response message fails, three cases may happen: (i) there are other neighbors available in its forwarding neighbor list, then the node will choose one of them according to the ARD to forward the response; (ii) There are no other forwarding neighbors available for this response. The node will build a UDP connection to a bRDA with the appended bRDA address. (iii) bRDA itself is failed or behind a firewall and the UDP connection to bRDA cannot be built. Then the node will inform its previous hop node and ask it to choose other node to forward the response message as in ARD. At the same time, a backup response delivery agent will always need to replace the bRDA address in the response message with the one it stored.

Fig. 3 illustrates the effect of the bRDA in response routing of the e-ARD scheme. Peer P and K are the primary forwarding neighbors of peer O and N respectively which fail during the response return process. In Fig. 3.a and 3.b, O is on the query incoming path. Thus, no matter if O is a bRDA or not, it always sends a response to a bRDA (here is A) which is also on the query incoming path. In Fig. 3.c and 3.d, O sends a response to its forwarding neighbor N which is not on the original query incoming path. In Fig. 3.c, N is not a bRDA itself and thus it still sends a response to agent A whose address is appended in the response message. The response message is rerouted to the original query incoming path since the bRDA address appended in the response message is the address of the agent who is in the original query incoming path. In Fig. 3.d, N itself is bRDA. It changes the bRDA address field according to the bRDA address stored in its forwarding neighbor list and sends a response message to M accordingly. The response message did not reroute to the original query incoming path although the appended bRDA address in the message is the address of an agent who is in the original query incoming path. However, we see that the length of response path is reduced in all cases due to the bRDA.

TABLE I: TYPE II REQUEST MESSAGE 

<table><tr><td></td><td colspan="2">Minimum Speed</td><td colspan="2">bRDA Address</td><td colspan="2">Search criteria</td><td>Extension blocks</td></tr><tr><td>Byte Offset</td><td>0</td><td>1</td><td>2</td><td>5</td><td>6</td><td>end with 0x00</td><td>Optional</td></tr></table>

TABLE II: TYPE II RESPONSE MESSAGE 

<table><tr><td></td><td>Number of Hits</td><td colspan="2">Port</td><td colspan="2">Responder Address</td><td colspan="2">Speed</td><td colspan="2">bRDA Address</td><td>Result Set</td></tr><tr><td>Byte Offset</td><td>0</td><td>1</td><td>2</td><td>3</td><td>6</td><td>7</td><td>10</td><td>11</td><td>14</td><td>15 -</td></tr></table>

The e-ARD can be used in P2P systems adopting a DFS based search mechanism or other non-flooding based search technique such as k-walker. Forwarding responses to a bRDA in e-ARD will reduce the number of hops in response return process and further cut both response time and traffic cost. This will partly pay for the overhead of creating a UDP connection.

# 4. Simulation methodology

We use a large-scale network simulation to evaluate the performance of our techniques. The network topology in the simulation should be consistent with the real P2P network to accurately evaluate the performance of the proposed mechanism. The study in [15] shows that P2P overlay topologies follow the small world and power law properties, and topologies generated using the AS Model have such properties. BRITE [1] is one of the topology generation tools that provide the option to generate topologies based on the AS Model. Using BRITE, we generated 4 logical topologies with 2000, 3000, 5000 and 8,000 nodes within the same area. To check networks with different connectivity, we varied the average number of neighbors of each node from 4 to 10.

Observations shown in [6] pointed out that the object popularity distribution in a P2P system does not follow a Zipf distribution like WWW objects mentioned in [4]. We simulate the flooding search process via executing Bread First Search based algorithm from a specific node. As for the query dispatch frequency, we set every node in the system to issue 0.3 queries per minute on average, which is calculated from the observation data shown in [16], i.e., 12,805 unique IP addresses issued 1,146,782 queries in 5 hours.

Based on generated P2P network topologies, we simulated the joining and leaving behavior of peers via turning on/off logical peers. The peer lifetime is generated according to the distribution observed in [15]. The lifetime is decreased by one after passing each second and a peer will leave in the next second when its lifetime reaches zero. During each second, there are a number of peers leaving the system. To keep the power law property during node leaving and joining processes, we then randomly pick up (turn on) the same number of peers from the network to join the overlay system. For each peer, a maximum-neighborconnection is pre-defined following power law. Each peer is required to keep the number of his neighbor connections no greater than his maximum-neighborconnection during the simulation.

We have done simulations based on P2P network size of 2000, 3,000, 5,000 and 8,000. The results from networks with different sizes are consistent, which confirms our techniques are scalable. Here we show the simulation results from a network size of 8,000. Although this size is still small compared with real P2P systems of millions of nodes, it is closer to the reality than the other simulations with smaller network sizes. We take 10 minutes as the default peer life time if not specified. During the computation of the wrapping probability of $\alpha$ , we take $c = 70$ and $\phi(T_{on}) = T_{on}\log(T_{on} + 1)$ such that $\alpha$ is increased from 0.35 to about 0.70 in our simulation period of 60 minutes.

![](images/a34890bdd256d8e7fffd8088d5d76959d44dd871552b667ac7fde7ef01aacbb8.jpg)  
Fig. 3 extended Adaptive Response Delivery, effect of backup response delivery agent

# 5. Performance evaluation

We present the simulation results about our techniques in this section. We first show the performance of all three techniques in a Gnutella like context environment and then we will check e-ARD in an environment with DFS search mechanism.

Fig. 4 compares response return rates of a Gnutella-like system, RRD scheme, ARD scheme, and e-ARD scheme under different peer uptimes ranging from 10 minutes to 60 minutes. Response return rate is defined as follows:

all response found for query – responses lost in backward path

all responses found for the query

The query frequency for each node is 0.3 queries per minute. We deploy the simulations for a 60 minutes period, collecting the data every 20 seconds, and repeat the process multiple times. The average response return rate is based on these collected data. We can see from Fig. 4 that Gnutella-like systems suffer from 35% response loss when the average peer uptime is 10 minutes. The RRD, ARD, e-ARD can increase response return rate by up to about 35%, 47%, 51% respectively, compared with Gnutella-like systems. The performance of the e-ARD scheme is better but close to ARD and both of them achieve near perfect response success rate. We also investigated the relationship between response return rates and the average number of response neighbors per node $^{1}$ in Fig. 5. We can see that the return rate increases as the average number of neighbors increases in a Gnutella-like system, but the response return rate of ARD is not sensitive to the average number of neighbors because of its near optimal performance.

The response traffic cost is the traffic of sending a response message from a responder to a query initiator. We compute response traffic cost as a function of consumed network bandwidth and other related expenses. In Fig. 6, we compare the average response traffic cost of four different response delivery schemes. For the RRD scheme in our simulation, only one additional path is selected for returning a duplicated response. Compared with a Gnutella-like system, the RRD scheme incurs a 102% increase in traffic cost. ARD only increases the response traffic cost by about 9% and e-ARD creates even less extra traffic at 6%.

Fig. 7 shows the average response time, the time from when a query is issued by a requestor to when the response is received by the requestor, of the four response schemes. As we expected, the average response time of both the RRD and ARD schemes are close to Gnutella-like systems. The response time in RRD is only 2% higher than that of Gnutella-like systems, while ARD is about 4% higher than that of Gnutella-like system.

To show how e-ARD performs in a system not adopting a flooding search algorithm, we deploy DFS search in our simulator and compare the response return rate in such a system with and without e-ARD. Fig. 8 shows the impact of e-ARD in response return rate, and Fig. 9 shows the response time of the system without flooding. We can see that e-ARD improves the response return rate up to 60% and, at the same time, needs less time to return a response back to the requestor.

# 6. Conclusion

Unstructured P2P system is a highly dynamic system in that average peer life time is from 10 to 60 minutes and average logical connection between peers is from 1 to 24 minutes. This leads to a response loss problem, with up to 35% of the responses being lost along their return path.

To remedy the response loss problem, we present and evaluate in this paper three techniques: RRD, ARD, and e-ARD. Compared to current response return mechanisms, all these techniques reduce response loss rate with limited extra cost regarding to the whole query process. Compared with RRD, ARD achieves better performance with higher response return rate and less response traffic cost. However, RRD needs least modification of the current response return mechanism to implement and can send responses back to the requestor faster than ARD on average. The e-ARD extends ARD and can even be used in unstructured P2P systems using a limited or non-flooding search mechanism. However, introduction of bRDA will add some complexity of the implementation of e-ARD. Although the average response time in ARD is longer than both RRD and Gnutella-like scheme, it is very close to the other two schemes (a difference of 4%). any central control. We will further investigate the effect of the ARD algorithm in the case of logical link breakage, and attempt to combine it with other optimization algorithms, such as P2P network topology adaptation.

![](images/d2db255cf4c7554f742f7b434f68a15d4e0818da7f4748f335bc6631d63872a3.jpg)



Fig. 4 Response return rate vs. peer life time

![](images/d2564a9abec765dd9200097efc942d06728142fd67a2987a803dc31ea99458ea.jpg)



Fig. 5 Response return rate under different network topologies (ARD)

![](images/1b56273555ace12bbd44cba2291c234e4e43f088e42bdecd797c89363d39ee9c.jpg)



Fig. 6 Response traffic cost vs. peer life time

![](images/11372e59a4b05fa63b61ba1e14c0f276ceadc0055d9c45701eb23c9ca43c6139.jpg)



Fig. 7 Response time vs. average peer life time

![](images/2fdf27c06dbcca10269cfbba9ccb4a0322acfc35239aa290ba9b369614e941ea.jpg)



Fig. 8 Response return rate with and without e-ARD

![](images/b5c80aff019aa307d0ba1d7efd095b51c807ed47bee3906166d6a58a2cbd2c04.jpg)



Fig. 9 Response time with and without e-ARD (DFS)

# 7. References:

[1] BRITE", http://www.cs.bu.edu/brite/   
[2] The Gnutella protocol specification 0.6", http://rfc-gnutella.sourceforge.net   
[3] KaZaA", http://www.kazaa.com   
[4] V. Almeida, A. Bestavros, M. Crovella, and A. d. Olivera, "Characterizing Reference Locality in the WWW," in Proceedings of the IEEE Conference on Parallel and Distributed Information Systems (PDIS), 1996.   
[5] Y. Chawathe, S. Ratnasamy, L. Breslau, N. Lanham, and S. Shenker, "Making Gnutella-like P2P Systems Scalable," in Proceedings of SIGCOMM, 2003.   
[6] K. P. Gummadi, R. J. Dunn, S. Saroiu, S. D. Gribble, H. M. Levy, and J. Zahorjan, "Measurement, Modeling, and Analysis of a Peer-to-Peer File-Shareing Workload," in Proceedings of 19th ACM Symposium on Operating Systems Principles (SOSP'03), 2003.   
[7] D. B. Johnson and D. A. Maltz, "Dynamic Source Routing in Ad Hoc Wireless Networking," in Proceedings of Mobile Computing, 1996.   
[8] Y. Liu, X. Liu, L. Xiao, L. Ni, and X. Zhang, "Location-Aware Topology Matching in Unstructured P2P Systems," in Proceedings of INFOCOM, 2004.   
[9] Q. Lv, P. Cao, E. Cohen, K. Li, and S. Shenker, "Search and replication in unstructured peer-to-peer networks," in Proceedings of ACM International Conference on Supercomputing, 2002.

[10] V. Park and M. Corson, "Temporally-ordered Routing Algorithm (TORA) Version 1: Functional Specification," in IETF Internet draft (draft-ietf-tora-spec-04.txt), 2001.   
[11] C. E. Perkins and E. M. Royer, "Ad-hoc On-demand Distance Vector Routing," in Proceedings of MILCOM, 1997.   
[12] C. Rohrs, "Query Routing for the Gnutella Network", http://rfc-gnutella.sourceforge.net   
[13] S. Sen and J. Wang, "Analyzing Peer-to-peer Traffic Across Large Networks," in Proceedings of ACM SIGCOMM Internet Measurement Workshop, 2002.   
[14] S. Saroiu, K. Gummadi, R. Dunn, S. Gribble, and H. Levy, "An Analysis of Internet Content Delivery Systems," in Proceedings of OSDI, 2002.   
[15] S. Saroiu, P. Gummadi, and S. Gribble, "A Measurement Study of Peer-to-Peer File Sharing Systems," in Proceedings of Multimedia Computing and Networking (MMCN), 2002.   
[16] K. Sripanidkulchai, "The popularity of Gnutella queries and its implications on scalability", http://www2.cs.cmu.edu/\~kunwadee/research/p2p/gnutella.html   
[17] S. Wang, D. Xuan, and W. Zhao, "On Resilience of Structured Peer-to-Peer Systems," in Proceedings of GLOBECOM, 2003.   
[18] B. Y. Zhao, L. Huang, J. Stribling, S. C. Rhea, A. D. Joseph, and J. D. Kubiatowicz, "Tapestry: An infrastructure for fault-resilient wide-area location and routing," IEEE Journal on Selected Areas in Communications, 2001.