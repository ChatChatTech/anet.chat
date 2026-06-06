# Noisy Data Collection Towards Diversity Maximization

Xiang Xiao∗, Lan Zhang∗, Xiang-Yang Li∗

∗School of Computer Science and Technology

University of Science and Technology of China

Abstract—In the big data era, we can take advantages of the big data by machine learning, knowledge discovery and so on. A dataset with good quality can promote the performance of the aforementioned applies. The dataset quality can be assessed from many aspects, for example, completeness, consistency, diversity, etc. In this paper, we will investigate diversity-driven data collection. Most previous works focused on the data collection only consider the accurate data without any noise. However, from the surveys and experiments, we find out that the data generally has noise with a certain probability distribution. Based on this discovery, we take account of the distribution of the data noise in the data space. We construct a comprehensive model to calculate the probability density distribution (abbreviated to PDF) of the distance between two noisy data points. Using the mainstream diversity metric, i.e., the average distance, we propose a more time-saving data collection method compared to the existing generic greedy algorithm.

# I. INTRODUCTION

In recent years, we have entered the big data era. According to a report [10] from IBM Marketing Cloud, 90% of the data on Internet has been created since 2016 and 2.5 quintillion bytes of data is created every day. Meanwhile, we can make a profit from the big data. By taking advantage of the data mining and machine learning techniques, we can get the inherent information of the big data and apply it to the recommendation system [18] and so on.

A dataset of good quality is needed for aforementioned applies. The dataset quality can be measured from three different aspects [21], the amount, the matching degree and the diversity. We mainly focus on the diversity of the collected data. Many works have proposed that diversity is very important to the dataset construction [15] [4]. In crowdsourcing, the diversity of opinion is important to form a wise crowd [15]. In a recommendation system, diversity is also important because no one wants to see a list of similar recommendations [4]. There are many works related to the diversity maximizing in collecting dataset [17]. Many of them ignore the data noise. However, it is inevitable that uncertainty and noise widely exist in the datasets [1]. There are many sources of data noise: (1) Data generation stage. For example, the GPS signal is very poor in the downtown area with only about 50% having errors less than 10 meters [3]. (2) Data storage and transmission stage. (3) Data publication stage. In data publication, to protect the privacy of the data from individuals, some noise will be added to the data to protect the privacy of individuals, e.g., in differential privacy scenario [7].

We mainly focus on the diversity of the collected uncertain data. Some previous works [12] focused on the data quality, which has a certain relation with the data noise. Those works focus on data purchase and don’t investigate the concrete noise formulation. Different from them, we figure out that the noise of the raw data has a certain PDF generally. Based on the noise PDF, we can calculate the PDF of the distance of two data points. Thus, we take account of the diversity-driven uncertain data collection problem. We propose an acceleration method to collect diversified uncertain data with cardinality constraints.

There are two main challenges in noisy data collection. (1) How to efficiently calculate the PDF of the distance between two noisy data points? Many previous works use the sampling method to get this PDF [13]. They take many samples of the noise of the two data points and calculate the point distance of every sample pair. Then they get the distance histogram and fit the PDF curve approximately. However, this method needs a large number of samples thus is very time-consuming. (2) How to efficiently and accurately measure the diversity of a largescale dataset? Nowadays, it is common that there are millions of data pieces in one dataset. We use the average distance of a dataset as the diversity metric. Previous methods, such as the greedy selection algorithm or the local search algorithm are time-consuming when the data amount is large. Thus, an efficient solution with a good tradeoff between efficiency and accuracy is desired.

The contributions of this paper are summarized as follows:

• We propose a novel framework for diversity-driven uncertain data collection. An efficient method to calculate the PDF of the noisy data distance is also designed.   
• We propose an acceleration method for data collection that use the average distance as the diversity metrics. We calculate the average distance between a data point and a dataset by random sampling. By adjusting the sample amount, we can well balance the calculation efficiency and accuracy.   
To validate the efficiency of our model, we conduct extensive experiments on the synthetic dataset (with 40,000 images in total) based on ImageNet. According to the experiment results, our method can collect dataset with diversity near the generic greedy algorithm while the time consumption is less by several orders of magnitude.

The rest of this paper is organized as follows. In section II, we describe the noise form and the diversity metrics. Then we introduce our solutions to accelerate traditional diversitydriven data collection methods in section III. The performance evaluations are reported in Section IV. We review the related works in section V and conclude our work in section VI.

# II. PRELIMINARY AND PROBLEM FORMULATION

# A. Noise Form

First of all, we should determine the PDF formulation of the data noise. We surveyed the sensor data as the representative 1-dimension data and GPS data for the 2-dimension data. [19] shows that the 1-dimension sensor data follows the normal distribution. [5] [14] research the noise of the GPS data and model the GPS noise as the zero-mean normal distribution. Based on them, for the high-dimension data, we adopt the attributelevel uncertainty model proposed in [13]. In that model, every dimension of a data point is following an independent probability distribution function. Also, we find that the noise on every dimension approximately obeys the normal distribution and the mean is zero (see section IV). Suppose the noise for d-dimension data is $\mathbf { n } = \left( n _ { 1 } , n _ { 2 } , \cdots , n _ { d } \right)$ , the standard = (deviation on every dimension is ${ \pmb \sigma } = ( \sigma _ { 1 } , \sigma _ { 2 } , \cdots , \sigma _ { n } )$ , we = (can summarize the PDF of the noise as follows

$$
f (\mathbf {n}) = \frac {1}{(2 \pi) ^ {d / 2} \prod_ {i = 1} ^ {d} \sigma_ {i}} \exp (- \sum_ {i = 1} ^ {d} \frac {n _ {i} ^ {2}}{2 \sigma_ {i} ^ {2}}) \tag {1}
$$

# B. Diversity Formulations

Previous works [11] have proposed different diversity metrics and this paper is focused on the metric of average distance.Intuitively, when the distances in a dataset are mostly large, the similarity between two data point is mostly small. So we can conclude that the diversity of the dataset is high (see the S-model in [17]). The diversity metric has many formulations. One popular metrics is the average distance of the dataset. We denoted it as $d i v _ { a } ( D )$ for a dataset $D = ( d _ { 1 } , d _ { 2 } , \cdots , d _ { n } )$ ( ). The definition is as follows:

$$
d i v _ {a} (D) = \frac {1}{| D | (| D | - 1)} \sum_ {d _ {i}, d _ {j} \in D \land i \neq j} d i s t (d _ {i}, d _ {j})
$$

When the data has noise, the aforementioned formulations can be adopted as the diversity metric in which the pair-wise distance should be replaced by its expectation.

# III. SELECTION ALGORITHM

We describe the total design of the noisy data collection method in this section. We want to maximize the diversity given a cardinality constraint on the dataset size. First, we introduce the method to calculate the PDF of the distance of two noisy data. Next, we illustrate how to use random sampling to accelerate the collection process which can be applied to the greedy algorithm [6] and the local search algorithm [11].

# A. Probability Distribution Of Distance

When using the average distance metric, a basic problem is how to calculate the distance between the two noisy data points. Some works [13] take some samples of the two points and fit the PDF of the distance approximately. This method takes a lot of time on sampling, distance calculation and curve fitting. However, for the noise form mentioned in Section II, we can obtain the approximation PDF faster. The problem can be formulated as follows. Given two d-dimension vectors $\mathbf { x } _ { 1 } , \ \mathbf { x } _ { 2 } .$ , with the mean and standard variation vector of $\mathbf { x } _ { i }$ being $\pmb { \mu } _ { i } = ( \mu _ { i , 1 } , \mu _ { i , 2 } , \cdots , \mu _ { i , d } ) , \pmb { \sigma } _ { i } = ( \sigma _ { i , 1 } , \sigma _ { i , 2 } , \cdots , \sigma _ { i , d } ) .$ , = (how can we get the PDF of $d i s t ( \mathbf { x } _ { i } , \mathbf { x } _ { j } ) \} $ We denote $\mathbf { x } =$ $( x _ { 1 } , x _ { 2 } , \cdot \cdot \cdot , x _ { d } ) = \mathbf { x } _ { 1 } - \mathbf { x } _ { 2 }$ ( ) =, and its mean and variation vector (are $\pmb { \mu } = ( \mu _ { 1 } , \mu _ { 2 } , \cdots , \mu _ { d } )$ and $\pmb { \sigma } ^ { 2 } = ( \sigma _ { 1 } ^ { 2 } , \sigma _ { 2 } ^ { 2 } , \cdot \cdot \cdot , \sigma _ { d } ^ { 2 } )$ . As = ( ) = ( )for the two points, the values at the same dimension are independent with each other, so we can get that

$$
\boldsymbol {\mu} = \left(\mu_ {1, 1} - \mu_ {2, 1}, \mu_ {1, 2} - \mu_ {2, 2}, \dots , \mu_ {1, d} - \mu_ {2, d}\right)
$$

$$
\pmb {\sigma} ^ {2} = (\sigma_ {1, 1} ^ {2} + \sigma_ {2, 1} ^ {2}, \sigma_ {1, 2} ^ {2} + \sigma_ {2, 2} ^ {2}, \dots , \sigma_ {1, d} ^ {2} + \sigma_ {2, d} ^ {2})
$$

The distance of $\mathbf { x } _ { 1 } , \mathbf { x } _ { 2 }$ is $\begin{array} { r } { d i s t ( \mathbf { x } _ { 1 } , \mathbf { x } _ { 2 } ) = | \mathbf { x } | = \sqrt { \sum _ { i = 1 } ^ { d } x _ { i } ^ { 2 } } } \end{array}$ i= i . As $x _ { i } \sim N ( \mu _ { i } , \sigma _ { i } ^ { 2 } )$ , we denote $\begin{array} { r } { Q = d i s t ^ { 2 } ( \mathbf { x } _ { 1 } , \mathbf { x } _ { 2 } ) \stackrel { \cdot } { = } \sum _ { i = 1 } ^ { d } x _ { i } ^ { 2 } } \end{array}$ ( ) = ( ) =and Q is the sum of independent normal variants. According to the definition of $\chi ^ { 2 }$ -distribution, Q obeys the $\chi ^ { 2 }$ -distribution. The mean and the variation of $Q$ are

$$
\mu_ {Q} = \sum_ {i = 1} ^ {d} E (x _ {i} ^ {2}) = \sum_ {i = 1} ^ {d} (\mu_ {i} ^ {2} + \sigma_ {i} ^ {2})
$$

$$
\sigma_ {Q} ^ {2} = E [ Q ^ {2} ] - E ^ {2} [ Q ] = \sum_ {i = 1} ^ {d} (2 \sigma_ {i} ^ {4} + 4 \sigma_ {i} ^ {2} \mu_ {i} ^ {2})
$$

The proof of these two equations are as follows.

Proof As the variation of $x _ { i } , V ( x _ { i } ) = E ( x _ { i } ^ { 2 } ) - E ^ { 2 } ( x _ { i } )$ , we have $E ( x _ { i } ^ { 2 } ) = V ( x _ { i } ) + E ^ { 2 } ( x _ { i } )$ ( ), thus $\begin{array} { r } { \mu _ { Q } = \sum _ { i = 1 } ^ { d } ( \mu _ { i } ^ { 2 } + \sigma _ { i } ^ { 2 } ) } \end{array}$ . ( ) = ( ) +The variation of Q, i.e., $\sigma _ { Q } ^ { 2 } = E ( Q ^ { 2 } ) - \dot { E } ^ { 2 } ( \overline { { Q } } )$ ( +. We have

$$
\begin{array}{l} \sigma_ {Q} ^ {2} = E [ (\sum_ {i = 1} ^ {d} x _ {i} ^ {2}) ^ {2} ] - [ \sum_ {i = 1} ^ {d} E (x _ {i} ^ {2}) ] 2 \\ = E \left(\sum_ {i = 1} ^ {d} \sum_ {j = 1} ^ {d} x _ {i} ^ {2} x _ {j} ^ {2}\right) - \sum_ {i = 1} ^ {d} \sum_ {j = 1} ^ {d} E \left(x _ {i} ^ {2}\right) E \left(x _ {j} ^ {2}\right) \\ = \sum_ {i = 1} ^ {d} [ E (x _ {i} ^ {4}) - E ^ {2} (x _ {i} ^ {2}) ] \\ \end{array}
$$

As for the $E ( x _ { i } ^ { 4 } )$ , we have

$$
\begin{array}{l} E (x _ {i} ^ {4}) = \int_ {- \infty} ^ {+ \infty} x ^ {4} \frac {1}{\sqrt {2 \pi} \sigma_ {i}} e ^ {(} - \frac {(x - \mu_ {i}) ^ {2}}{2 \sigma_ {i} ^ {2}}) d x \\ = 3 \sigma_ {i} ^ {4} + 6 \sigma_ {i} ^ {2} \mu_ {i} ^ {2} + \mu_ {i} ^ {4} \\ \end{array}
$$

Thus we can get

$$
\begin{array}{l} \sigma_ {Q} ^ {2} = \sum_ {i = 1} ^ {d} [ (3 \sigma_ {i} ^ {4} + 6 \sigma_ {i} ^ {2} \mu_ {i} ^ {2} + \mu_ {i} ^ {4}) - (\mu_ {i} ^ {2} + \sigma_ {i} ^ {2}) ^ {2} ] \\ = \sum_ {i = 1} ^ {d} (2 \sigma_ {i} ^ {4} + 4 \sigma_ {i} ^ {2} \mu_ {i} ^ {2}) \\ \end{array}
$$

As the dimension d is high, Q can be approximately treated as a normal distribution with its original mean and variation. Thus we have $d i s t ^ { 2 } ( { \bf x } _ { 1 } , { \bf x } _ { 2 } ) \sim N ( \mu _ { Q } , \sigma _ { O } ^ { 2 } )$ .

( )At last, we also find that $d i s t ( \mathbf { x } _ { 1 } , \mathbf { x } _ { 2 } )$ obeys a normal ( )distribution approximately. Consequently, we want to get the mean and standard deviation of $d i s t ( \mathbf { x } _ { 1 } , \mathbf { x } _ { 2 } )$ , denoted as $\mu _ { D }$ and $\sigma _ { D }$ (. We randomly select 10000 $\left( \mathbf { x } _ { 1 } , \mathbf { x } _ { 2 } \right)$ pairs. We use ( )sampling and curve fitting to get the mean and standard deviation of the distances as their $\mu _ { D }$ and $\sigma _ { D }$ . Then we calculate $\mu _ { Q }$ and $\sigma _ { Q }$ . We execute linear regression between $\mu _ { Q }$ with $\mu _ { D } ^ { 2 }$ , and $\mu _ { Q } / \sigma _ { Q }$ with $\mu _ { D } / \sigma _ { D }$ . Finally, we find the relations as belows

$$
\mu_ {D} = \sqrt {\mu_ {Q}}
$$

$$
\frac {\mu_ {D}}{\sigma_ {D}} = 2 \frac {\mu_ {Q}}{\sigma_ {Q}}
$$

# B. Average Distance

As we get the mean of the distance, we can use the distance mean to solve the average distance maximization problem. The problem is that given a dataset $D = ( x _ { 1 } , x _ { 2 } , \cdot \cdot \cdot , x _ { n } )$ , and the = (selection budget k, we aim to find a subset $S \subset D$ )and $| S | = k$ =so that maximize the average distance in S. There are some methods to solve this problem, such as the generic greedy algorithm [6] and the local search algorithm. We denote the selected dataset as $S ^ { \prime }$ . In the generic greedy algorithm, as Alg. 1 of [6], in each iteration we should find

$$
i = \arg \max _ {i} \sum_ {x _ {j} \in S ^ {\prime}} d i s t (x _ {i}, x _ {j})
$$

The local search algorithm is Alg. 2 in [11]. In each iteration, it will find a data pair $x _ { i } \in D \backslash S ^ { \prime }$ and $x _ { j } \in S ^ { \prime }$ and so that

$$
d i v (S ^ {\prime} \backslash \{x _ {j} \} \cup \{x _ {i} \}) \geq d i v (S ^ {\prime}) (1 + \frac {\epsilon}{n})
$$

Then $x _ { i }$ and $x _ { j }$ will be swapped.

In both of the two problems, a critical process is to calculate the average distance between a point x and a subset $S ,$ , which is denoted as $\begin{array} { r } { d i s t ( x , S ) = \bar { \sum _ { x _ { i } \in S } d i s t ( x , x _ { j } ) } / | S | } \end{array}$ . In the greedy algorithm, we calculate $d i s \dot { t } ( x _ { i } , S ^ { \prime } )$ . In the local search algorithm,

$$
d i v (S ^ {\prime} \backslash \{x _ {j} \} \cup \{x _ {i} \}) = \frac {2}{k (k - 1)} [ \frac {k (k - 1)}{2} \times d i v (S ^ {\prime})
$$

$$
- (k - 1) \text { dist } (x _ {j}, S ^ {\prime} \backslash \{x _ {j} \}) + (k - 1) \text { dist } (x _ {i}, S ^ {\prime} \backslash \{x _ {j} \}) ]
$$

$$
= d i v (S ^ {\prime}) + \frac {2}{k} (d i s t (x _ {i}, S ^ {\prime} \backslash \{x _ {j} \}) - d i s t (x _ {j}, S ^ {\prime} \backslash \{x _ {j} \}))
$$

This method needs to traverse all the points to calculate the accurate average distance. When the subset has a large size, for example, $k = \Theta ( n )$ , it will be time-consuming. So = Θ( )we want to find a rapid method that calculates $d i s t ( x , S )$ . A ( )method is that we sample some points S from S then we calculate $\boldsymbol { d i s t } ( \boldsymbol { x } , \bar { \boldsymbol { S } } )$ as $d i s t ( x , S )$ . According to Hoeffding’s ( ) ( )inequality [9], we can balance the sample number and the accuracy of the average distance.

Lemma 1 (Hoeffding’s inequality) $I f x _ { 1 } , x _ { 2 } , \cdots , x _ { n }$ are independent, and $\forall i \ = \ 1 , 2 , \cdot \cdot \cdot , n , \ x _ { i } \ \in \ [ a _ { i } , b _ { i } ] .$ , we denote $\mu = E ( \textstyle \sum _ { i = 1 } ^ { n } x _ { i } / n )$ = 1, then

$$
P r \{\left| \frac {\sum_ {i = 1} ^ {n} x _ {i}}{n} - \mu \right| \geq t \} \leq 2 e ^ {- 2 n ^ {2} t ^ {2} / \sum_ {i = 1} ^ {n} (a _ {i} - b _ {i}) ^ {2}}
$$

We can randomly sample m points $x _ { 1 } , x _ { 2 } , \cdots , x _ { m }$ with replacement from S and calculate 1m mi=1 $S$ $\begin{array} { r } { \frac { 1 } { m } \sum _ { i = 1 } ^ { m } d i s t ( x _ { i } , x ) } \end{array}$ dist xi, x ≈ $d i s t ( x , S )$ . At first, we should prove that

$$
E (\frac {1}{m} \sum_ {i = 1} ^ {m} d i s t (x _ {i}, x)) = d i s t (x, S)
$$

Proof

$$
E (\frac {1}{m} \sum_ {i = 1} ^ {m} d i s t (x _ {i}, x)) = \frac {1}{m} \sum_ {i = 1} ^ {m} E (d i s t (x _ {i}, x))
$$

As every sample is uniformly sampled from $S ,$ with the probability $1 / | S | ,$ , for $i ~ = ~ 1 , 2 , \cdots , m$ , $E ( d i s t ( x _ { i } , x ) ) \ =$ $\textstyle \sum _ { x _ { j } \in S } d i s t ( x _ { j } , { \dot { x } } ) / | S |$ = 1 2. We have

$$
\begin{array}{l} E (\frac {1}{m} \sum_ {i = 1} ^ {m} d i s t (x _ {i}, x)) = \frac {1}{m} \sum_ {i = 1} ^ {m} \sum_ {x _ {j} \in S} \frac {1}{| S |} d i s t (x _ {j}, x) \\ = \frac {1}{m} \sum_ {i = 1} ^ {m} d i s t (x, S) \\ = d i s t (x, S) \\ \end{array}
$$

Consequently, we can use the average distance to the samples to approximately calculate the average distance to the original dataset. By adjusting the sample amount, we can balance the time consumption and the accuracy of the average distance according to the Hoeffding’s inequality. Also, we use the random sampling to select a subset from $D \backslash S ^ { \prime }$ , find the point with maximum average distance to $S ^ { \prime }$ in the subset and add the point to $S ^ { \prime }$ . Suppose that in every iteration, we sample $k _ { 2 }$ data points from $D \backslash S ^ { \prime } .$ , and for every point in them, we sample $k _ { 1 }$ data points to calculate the average distance and finally find the maximal to add to $S ^ { \prime } .$ , we can get the time complexity as

$$
O (\sum_ {i = 1} ^ {k} \min \{n - i, k _ {2} \} \times \min \{i, k _ {1} \}) = O (k k _ {1} k _ {2})
$$

The traditional greedy algorithm has the time complexity $O ( n k ^ { 2 } )$ . Thus we can choose $k _ { 1 }$ and $k _ { 2 }$ properly and reduce the time consumption.

# IV. PERFORMANCE EVALUATION

# A. Noise Formulation

In this subsection, we show the noise distribution extracted from the popular dataset, ImageNet. [21] uses the 1000- dimension features of the images from the fc8 layer to calculate the diversity of the dataset. In every category, the objects are of the same kind. The center of the features in the same category is denoted as the accurate data point for the category. Given a feature $\textit { f } = \ ( f _ { 1 } , f _ { 2 } , \cdot \cdot \cdot , f _ { d } )$ and its center $c =$ $( c _ { 1 } , c _ { 2 } , \cdots , c _ { d } )$ = ( ), the difference between $f$ =and c can be treated ( )as the noise of $f , { \mathrm { i . e . , ~ } } n = \left( f _ { 1 } - c _ { 1 } , f _ { 2 } - c _ { 2 } , \cdots , f _ { d } - c _ { d } \right)$ , where $n _ { i } = f _ { i } - c _ { i }$ = (. We get the histogram of $n _ { i }$ )on every =dimension and find out the proper approximate PDF. We randomly choose 25 categories from the ImageNet, containing

39270 images totally, and get the noise for every image. For every dimension, we count the distribution of the noise. We get the standard deviation (denoted as std) of the noise as the std of the normal distribution on that dimension. We randomly select two dimensions and draw the real distribution and the corresponding normal distribution, as in Fig. 1.

![](images/b7e441877d125e83a77254b4b5fd627e3f43b769f11f0febe0432198b20278c8.jpg)



(a) 400th dimension

![](images/88eb3db74b6ee07f004c6f2e888f9efed39ca37bd00d422a8344dfd4cde8f64a.jpg)



(b) 600th dimension   
Fig. 1: The real and approximate distribution of the noise on two dimensions

The mean and std of the normal distribution is those of the real noise. It is shown that the normal distribution can approximate the real distribution well. Nevertheless, the pdf curve is similar to the Laplace distribution, too. Thus we compare the Laplace and normal distribution. The parameter $\mu$ and λ in the Laplace distribution, $\begin{array} { r } { f ( x ) ~ = ~ \frac { \hat { 1 } } { 2 \lambda } e ^ { - \frac { | x - \mu | } { \lambda } } } \end{array}$ |x−μ| , ( ) =can be calculated from the mean and std of the real noise. Fig. 2a shows the real noise distribution and the approximate normal and Laplace distribution on a certain dimension. We calculate the average difference of the probability density between the real distribution and the approximate distribution on every dimension and getting the result in Fig. 2b. In fact, on the range of the noise − , , the average difference of [ 20 20]the normal distribution is less than the Laplace distribution. Thus we set the normal distribution to be the approximate distribution.

![](images/08366d3ad98919ae0183598271949db5283543d622f75662e16b66775e88deb1.jpg)



(a) real and approximate distribution(b) the difference of normal and Laplace

![](images/b122849ee7e4a7ff0d9b6d0d570e6a17f6c29bbef3494e656eaeb2a8682be41b.jpg)



Fig. 2: The comparison of normal and Laplace distribution

Next, we use linear regression to verify the relations between $\mu _ { D } , \sigma _ { D }$ and $\mu _ { Q } , \sigma _ { Q }$ , i.e., $\mu _ { D } = { \sqrt { \mu _ { Q } } }$ and $\begin{array} { r } { { \frac { \mu _ { D } } { \sigma _ { D } } } = 2 { \frac { \mu _ { Q } } { \sigma _ { Q } } } } \end{array}$ μQ . =The results can be found in Fig. 3 and Tab. I.

TABLE I: The results of linear regression 

<table><tr><td>equation</td><td>slope</td><td>intersect</td><td>r-value</td></tr><tr><td> $\mu_{D} = k \cdot \sqrt{\mu_{Q}} + b$ </td><td>1.000029</td><td>-0.023670</td><td>0.999999</td></tr><tr><td> $\frac{\mu_{D}}{\sigma_{D}} = k \cdot \frac{\mu_{Q}}{\sigma_{Q}} + b$ </td><td>1.998378</td><td>0.043880</td><td>0.996434</td></tr></table>

![](images/f830201efafa0435b98d32c7e40536f0817464c6f1f6843bdae2606492b32184.jpg)



(a) relation between μD and $\sqrt { \mu _ { Q } }$

![](images/c49ea3761155ad72cc388d7ec17a331175f3551d832c7efbfc4aadd951c7d0b6.jpg)



(b) relation between $\frac { \mu _ { D } } { \sigma _ { D } }$ and $\frac { \mu _ { Q } } { \sigma _ { Q } }$ σQ   
Fig. 3: The relations of $\mu D , \sigma _ { D }$ and $\mu _ { Q } , \sigma _ { Q }$

# B. Average Distance

In this subsection, we show the experiment results, including the average distance and the time consumption of our method and the generic greedy method. There are four factors affecting the results, the data amount of the dataset D, the cardinality constraint $\boldsymbol { k } , \boldsymbol { k } _ { 1 }$ and $k _ { 1 }$ . First is the relationship between the size of sampling and the average distance. With the increase of $k _ { 1 }$ and $k _ { 2 } ,$ the average distance between a point and a dataset is more accurate and the selected maximum is more nearly the real maximum. Fig. 4 shows the average distance of the collected data when the $k _ { 1 }$ and $k _ { 2 }$ changes. With $k _ { 1 }$ and $k _ { 2 }$ increasing, the average distance converged to that of the generic greedy method result. When the $k _ { 1 }$ and $k _ { 2 }$ reach 500, the average distance is approximately the same as the result of the generic greedy method. Thus, we fix $k _ { 1 } = k _ { 2 } = 5 0 0$ as the sample number.

![](images/bc89426e51a267fc001bf7224884d22fef17c5ce5787ae62485f541c11f6200b.jpg)



Fig. 4: The change of the average distance when $k _ { 1 }$ and $k _ { 2 }$ change

From the aforementioned image dataset, we select D with the size of 5000, 10000, 15000, 20000, 25000, and set k as 2500, 5000, 10000, 15000. For the selected D, we sample the noise of every data point several times and calculate the mean of the average distance. With the change of these two factors, we figure out the impact on the average distance and the time consumption. From Fig. 5, we can find that the result of the sampling method can compare with the generic greedy method. They are both better than the random selection.

![](images/1fa0783898bf205b70d51eafbe794b537d890748dc4e166ab21e9e5522ad8c06.jpg)



(a) k = 2500

![](images/760b412c5ca7903ef980859a1ee46e3ee0c8200f66247c43d53ddaa0a160487d.jpg)



(b) k = 5000   
Fig. 5: The average distance when the data amount changes

The time consumption comparison is shown in Fig. 6. We can see that compared with the generic greedy method, the sampling method is several orders of magnitude faster.

![](images/37033f6f51df66a0e3079107dc94c04a9b6f48f83e395a660ae847c061c86b6d.jpg)



(a) sample method

![](images/c5bee8a202ee45f89728fd28240ef8ba37757acb35509a7deae77d514f286471.jpg)



(b) generic greedy method   
Fig. 6: The time consumption of the sample and generic greedy method

# V. RELATED WORK

Data collection is an essential step in the construction of datasets. According to the machine learning theories, the high diversity of the training datasets can promote the generality of the learned model. Thus, many works take researches on the diversity of the collected data in many fields, such as crowdsourcing [17], information retrieval [2] and so on. Many methods are proposed to collect dataset with large diversity. The greedy method [17] is a method with a constant approximation ratio as the diversity metric is submodular. Some heuristic methods, such as neighborhood method [8] and the interchange method [20], have good performance in experiments.

Many papers conduct researches on accurate date. However, most data are produced with noise in reality. [1] models the uncertain data as computational geometry problems and calculate the probability of being the nearest neighbor of a given point. [16] is from the database and information retrieval aspect and constructs a data structure to facilitate uncertain data queries. [13] proposes new methods to find k nearest neighbors. We take advantages of the uncertainty models in [13] and research in the dataset diversity problem.

# VI. CONCLUSION

We propose an method to calculate the PDF of the distance between two noisy data points in high-dimension space when the noise obeys the normal distribution. This method is more time-saving in contrast to sampling and curve fitting. We also propose a sampling method to accelerate the general greedy algorithm. Our experiments validate the efficiency of our methods compared with previous methods. The collected dataset diversity of our method is near to that of the general greedy algorithm. Future works can focus on other distance metrics, for example, the minimum distance or other diversity metrics such as entropy and coverage.

# ACKNOWLEDGMENTS

This work is supported by the National Key R&D Program of China 2017YFB1003003, NSF China under Grants No. 61822209, 61751211, 61572281, 61520106007, and the Fundamental Research Funds for the Central Universities.

# REFERENCES

[1] P. K. Agarwal, B. Aronov, S. Har-Peled, J. M. Phillips, K. Yi, and W. Zhang, “Nearest-neighbor searching under uncertainty ii,” ACM Transactions on Algorithms (TALG), vol. 13, no. 1, p. 3, 2016.   
[2] R. Agrawal, S. Gollapudi, A. Halverson, and S. Ieong, “Diversifying search results,” in ACM WSDM, 2009. ACM, 2009, pp. 5–14.   
[3] C. Bo, X.-Y. Li, T. Jung, X. Mao, Y. Tao, and L. Yao, “Smartloc: Push the limit of the inertial sensor based metropolitan localization using smartphone,” in ACM Mobicom, 2013.   
[4] J. Carbonell and J. Goldstein, “The use of mmr, diversity-based reranking for reordering documents and producing summaries,” in ACM SIGIR, 1998.   
[5] F. V. Diggelen, “System design & test-gnss accuracy-lies, damn lies, and statistics-this update to a seminal article first published here in 1998 explains how statistical methods can create many different,” GPS world, 2007.   
[6] M. Drosou, H. Jagadish, E. Pitoura, and J. Stoyanovich, “Diversity in big data: A review,” Big data, 2017.   
[7] C. Dwork, A. Roth et al., “The algorithmic foundations of differential privacy,” Foundations and Trends in Theoretical Computer Science, 2014.   
[8] E. Erkut, Y. Ulk ¨ usal, and O. Yenicerio ¨ glu, “A comparison of p-dispersion ˘ heuristics,” Computers & operations research, 1994.   
[9] W. Hoeffding, “Probability inequalities for sums of bounded random variables,” in The Collected Works of Wassily Hoeffding. Springer, 1994, pp. 409–426.   
[10] IBM, “10 key marketing trends for 2017 and ideas for exceeding customer expectations,” 2017. [Online]. Available: https://www-01.ibm. com/common/ssi/cgi-bin/ssialias?htmlfid=WRL12345USEN   
[11] P. Indyk, S. Mahabadi, M. Mahdian, and V. S. Mirrokni, “Composable core-sets for diversity and coverage maximization,” in ACM PODS, 2014.   
[12] H. Jin, L. Su, D. Chen, K. Nahrstedt, and J. Xu, “Quality of information aware incentive mechanisms for mobile crowd sensing systems,” in ACM MobiHoc, 2015.   
[13] J. Liu and H. Deng, “Outlier detection on uncertain data based on local information,” Knowledge-Based Systems, 2013.   
[14] P. Newson and J. Krumm, “Hidden markov map matching through noise and sparseness,” in ACM SIGSPATIAL, 2009.   
[15] J. Surowiecki, M. P. Silverman et al., “The wisdom of crowds,” American Journal of Physics, 2007.   
[16] Y. Tao, R. Cheng, X. Xiao, W. K. Ngai, B. Kao, and S. Prabhakar, “Indexing multi-dimensional uncertain data with arbitrary probability density functions,” in VLDB, 2015.   
[17] T. Wu, L. Chen, P. Hui, C. J. Zhang, and W. Li, “Hear the whole story: Towards the diversity of opinion in crowdsourcing markets,” Proceedings of the VLDB Endowment, vol. 8, no. 5, pp. 485–496, 2015.   
[18] X. Wu, X. Zhu, G.-Q. Wu, and W. Ding, “Data mining with big data,” IEEE TKDE, 2013.   
[19] L. Xiao, S. Boyd, and S. Lall, “A scheme for robust distributed sensor fusion based on average consensus,” in IEEE IPSN, 2005.   
[20] C. Yu, L. Lakshmanan, and S. Amer-Yahia, “It takes variety to make a world: diversification in recommender systems,” in ACM EDBT, 2009.   
[21] L. Zhang, Y. Li, X. Xiao, X.-Y. Li, J. Wang, A. Zhou, and Q. Li, “Crowdbuy: Privacy-friendly image dataset purchasing via crowdsourcing,” in IEEE INFOCOM 2018.