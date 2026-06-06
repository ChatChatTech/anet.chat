# TagScreen: Synchronizing Social Televisions Through Hidden Sound Markers

Qiongzheng Lin $^{*}$ $^{\dagger}$ , Lei Yang $^{\dagger}$ , Yunhao Liu $^{*}$ ,

\* School of Software and TNLIST, Tsinghua University, China

$^{\dagger}$ Department of Computing, The Hong Kong Polytechnic University, Hong Kong {lin, young}@tagsys.org, yunhao@greenorbs.com

Abstract—Millions of people nowadays share their television (TV) experience with other people through social media like Twitter or Facebook with mobile devices. It is generally believed that TV has been repurposed for social networks, called as social television. A key functionality of social television is that it allows the viewers to interchange their comments through mobile devices, thus creating the impression of watching TV like alongside a group of friends. To do so, mobile devices have to be aware of the current media context (identifier and progress) of what the TV is playing, known as synchronizing context from TVs to mobile devices. Unfortunately, most legacy systems are not able to track the playing progresses or need to upgrade TV devices. To address the issue, we design a purely software-based solution, called as TagScreen, which inserts a series of hidden sound markers into the audio of the content. TagScreen supports long-range or multipath-resistant synchronization at second-level, being independent of device diversity over severely frequency-selective acoustic channels. We implement TagScreen by using COTS TVs and mobile devices. The system has been extensively tested on 150 movies and 150 TV series across five different environments. Results show that TagScreen has a mean recognition accuracy of 98% up to 35m, and a mean tracking accuracy of 97%.

# I. INTRODUCTION

Television (TV), the most pervasive medium ever invented, creates a shared and common experience that connect people with each other in an extended society. As people are leading more widely diverse lives and doing more manifold activities, TV can provide a common point or reference, a kind of ‘social glue’ that bonds strangers and acquaintances. Nowadays many people share their TV experiences with other viewers on social networks like Twitter and Facebook by using smart phones and tablets. The TV is being repurposed for social networks, known as social television, which was named one of the 10 most important emerging technologies by the MIT Technology Review in 2010 [1].

The key functionality of social television is to create the impression of watching TV like alongside a group of friends. It can provide a shared media context for conversations on the contents that they have enjoyed, despite neither at the same time nor at the same place. For example, Alice watched a movie and posted her comment at 5'13" (i.e. the playing progress). The comment tagged with the media context (content identifier and playing progress), is posted to the social network. When Bob watches the same movie later, the comment posted by Alice is displayed to Bob at the same progress (5'13"), making Bob feel as if he was watching the movie together with Alice.

![](images/450e6d8828d01ea3cedb375fab0bf1531ea48f511d0cfe1a648f65ff71a6f791.jpg)



Fig. 1: System architecture of TagScreen. Its crucial task is to synchronize media context from TV to mobile devices.

With the proliferation of smart phones and tablets, the mobile devices become a major ‘second screen’ for social televisions. The people could read extra information behind the movie or interact with their friends in the social networks. The most crucial task of such ‘instant interaction’ is to let the mobile devices be aware of the media context, known as synchronizing the media context from TVs to mobile devices. Apparently, inferring context through TV program does not work due to unknown of channel information, not mentioned for VOD (video on demand). A common industrial solution is to upgrade devices to smart TVs or topsets (like Apple TV), which can regularly broadcast contexts over WiFi or Bluetooth. Obviously, it is not compatible with the legacy TV devices. The third method $[2]$ , $[3]$ is based on audio signature. It records a short audio clip as content signature and sends it to backend server for content recognition. Such method has many limitations. For example, any noise from the crowd or juicer machine may pollute the signature. What is worse, the background music in a movie always repeats at different time slots, making the recognition only at the level of identifier recognition instead of fine-grained progress tracking $[4]$ .

In this paper, we design a new social television system, TagScreen, for supporting long-range, real-time and backwards-compatible context synchronization from TVs to mobile devices through acoustic channels. TagScreen inserts a series of inaudible sound markers (i.e. sound markers) into content audios. These markers are naturally broadcasted when the host contents are being played. The user's mobile device can receive and identify these sound markers with their microphone. To better understand the concept of TagScreen, we provide a brief overview of how TagScreen works in high-level in Fig. 1. Specifically, the content provider (like CNN or BBC) inserts media context into the content audio second by second before the content was released. Meanwhile it also registers the content ID in a centralized server which stores the extra information of the content. After recognizing the context, the mobile devices post (or pull) the comments on the basis of currently resolved media context to (or from) social networks when the user is viewing the content.

A key advantage of TagScreen over conventional social television systems is that it is a purely software-based solution, which is backwards compatible to legacy TVs and mobile devices. TagScreen can run on many mobile devices, such as smart phone, tablet, or even a TV remoter, as long as they have a microphone. Our design only leverages an essential component of TV set, speaker, to convey the media context, although a TV set itself is unaware of this. The second advantage of TagScreen is that it is action-aware. The viewer usually performs actions, such as pausing, stopping, fast-forwarding, changing channel, when viewing contents. Since the media context contains progress information, TagScreen can synchronously show comments as TV plays, even suffering from unpredictable viewing actions. Meanwhile, TagScreen also incidentally provides fundamental action data for viewing behavior mining.

Developing such a practical system out of the basic principle, however, entails substantial challenges. First, the embedded sound markers must stay unobtrusive to users. They should be inaudible from users and do not interfere with any content that the user is listening from the loudspeaker. Second, the playing scenes are very diverse. The content may be played in a quiet living room, noisy shopping mall like LED advisement screen, or in a severely multipath-suffered car like FM radio. Thus, the long-distance and multipath-resistant synchronization is necessary. Third, the signal processing must be real-time and energy-saving. The received audio signal arrives in a shifted version at mobile devices due to the propagation delay. It requires an energy-consuming convolution to extract the sound markers from recorded samples, which is apparently unfordable for the smart devices with very limited power budget.

Our empirical studies (referring to Section III) suggest that the best candidate carrier frequencies should be above 18kHz, which is unobtrusive to users as well as non-destructive to content audio. Actually, the essential technique of TagScreen is on acoustic communication that carries information over sound signals. Our studies also show that the frequency selectivity becomes the most fatal factor affecting the communications due to scene diversity and multipath effect. To deal with this issue, TagScreen carries the sound markers over a group of linear frequencies (i.e. chirp at 18kHz\~20kHz) instead of a single frequency. We also design an efficient algorithm called as quick synchronization for markers decoding, reducing the computations from $O(n^{2})$ to $O(n)$ for energy saving. It exploits the sparse nature of the synchronization problem, where only the correct alignment between the received audio clip and the known preamble code causes their cross-correlation to spike (Details are elaborated in Section IV.).

Summary of results. We build a prototype implementation of TagScreen and evaluate it over 150 movies and 150 TV series, leading to the following findings:

- Across 5 different environments, TagScreen has a mean recognition accuracy of $98\%$ , offering $5 \times$ than audio signature based schemes used in WeChat [2] or SampleSumo [3].   
- TagScreen extends the communication range up to $35m$ at maximum given average sound volume compared to the few meters of the previous work.   
- Providing real-time tracking of playing progress (which, to best of our knowledge, is never studied before), TagScreen has a mean synchronization delay of 1.6 seconds.   
- TagScreen reduces the time cost of convolution on mobile devices by $6.5 \times$ against the cross-correlation methods. It consumes as much power as playing 'Fruit Ninja', $2 \times$ lower than Google Maps.

Contributions. First, we design and implement a new software-based social television system that is able to synchronize the media context from TVs to mobile devices through acoustic channels. Second, we propose to embed the hidden sound markers in the media at carefully selected frequencies, so as to thrive the challenges of acoustic communications. Third, we introduce quick synchronization to recognition algorithm, reducing computations to a nearly linear time and input number $10\times$ off.

# II. OVERVIEW

TagScreen is a real-time social television system, which allows viewers to post and pull comments from social networks with their mobile devices, based on the current TV context. Although we present the system in the context of traditional television, TagScreen's technique can be applied to a variety of video-sharing websites, such as YouTube, Netflix, Hulu, etc.

# A. Motivation & Scope

Social TV attempts to make the television experience more participatory. It goes a step further and lets viewers interact with other TV viewers watching in different homes. This social overlay on TV is a natural part of the Internet converging with TV. The design of TagScreen involves two kinds of third-party entities, content provider and social network. We believe that there is a strong motivation for them to support social television, because the cooperation is win-win. Media that has a high discussion rate on social networks usually draws more attention and attracts more viewers, while comments on viewing experiences lead to more discussions on social networks thus more visiting traffic.

In terms of the human's reaction delay and change frequency of movie plots, we think the synchronization at second level is sufficient for our system and that the delay (i.e. few milliseconds) resulted from the propagation from the TV to mobile device is ignorable.

![](images/381f9d387bf2b1befd8fcda1f90984fdda49d5d4d899f19c53be3989f9af81e4.jpg)



(a) Spectrum of ambient noise

![](images/c8e9c3333b5094f7f21305fbb97b310ab753b8385e4bb1b8838b68263accf7ef.jpg)



(b) Frequency selectivity

![](images/b42b12b1f1ef48d56d264a1762a88dde2e324445774ae6907efff74a015c90ab.jpg)



(c) Multipath (echo) effect   
Fig. 2: Marking content. (a) The frequency band between 18kHz to 20kHz is chosen in terms of ambient noise, content audio and human hearing system. (b) The frequency selectivity over different TVs. (c) The multipath effect takes impacts on the acoustic channel.

# B. Solution

To synchronize the media context between TVs and smart devices, at high level TagScreen has two crucial components distributed in the domains of content provider and viewers' mobile devices respectively. These two components are:

- Marking Content: Content provider inserts the media contexts including content ID and progress into the content audio second by second, using the technique in Section III.   
- Synchronizing Playing: TagScreen leverages the mobile devices to recognize context and track playing progress with the energy-efficient signal processing algorithm proposed in Section IV.

The next few sections will elaborate the above two issues, and provide the technical details.

# III. MARKING CONTENT

This section introduces the design of sound marker, which must be inaudible and reliable. The design is highly dependent on the characteristic of the acoustic communications. Thus, we first present it from three key perspectives: carrier, modulation, and encoding.

# A. Marker Carrier

The frequency selection is a fundamental issue of the marker design. The chosen frequency must be inaudible to human hearing system, tolerant to ambient noise and nondestructive to contents. Most mobile devices today support an acoustic sampling rate of up to 44KHz, indicating a maximum operating frequency of 22KHz. However, their microphone components are dedicated to human speeches, and some smart devices can hardly record signals over 21kHz [5]. Thus, our candidate frequencies are below 20kHz.

Considering noise. A key requirement of sound marker is that it must operate indoors where the ambient acoustic noise may impose significant interference. To study such interference, we collected ambient sound samples in an isolate and silent room as noise floor. Next, we sampled sounds in a very noisy restaurant during busy hours, using iPhone 6. Note that the samples are recorded by an App developed by us instead of iPhone's built-in recorder, because the latter eliminates the high-frequency noise to enhance human voice. Fig. 2(a) shows the frequency distribution of the ratio of ambient sound energy to the noise floor, where the blue line indicates the noise distribution at the restaurant. As shown in the figure, the ambient noise above the noise floor is totally below 9kHz. Human voice rarely exceeds 1kHz, but the metal devices, like juicer or blender, in the restaurant contribute a lot to the higher frequency. Conducting the same experiment in living room, shopping mall, supermarket, even noisy railway station, we obtain the similar conclusion that the available band is between 10kHz \~ 20kHz in terms of the ambient noise.

Considering inaudibility. Last, we consider the hearing of human beings so that we can design inaudible sound markers. Evaluating the maximum audible frequency of human ears in theory and practice, we have the similar results as shown in [5] that the sound over 18kHz is claimed to be mostly inaudible in typical environments.

On the basis of the above observations, we conclude that the perfect frequency band is between $18\mathrm{kHz} \sim 20\mathrm{kHz}$ , which is resistant to ambient acoustic noise, barely involved in content, and inaudible for human ears. Certainly, this band can be recognized by most of today's mobile devices.

# B. Marker Modulation

The second aspect of the marker design is how to modulate the context on the selected frequency? One of the notorious issues in wireless communications is the frequency selectivity, which refers to the selective attenuation of certain frequencies in the transmitting signal, due to device diversity and multipath effect. Next, we consider the frequency selectivity over acoustic channels.

TV diversity. The sound is generated by the mechanical components (e.g. vibrating membranes) so that the speaker may not faithfully produce tones of specific frequencies. We measure the frequency responses of various TV devices. In the experiment, an iPhone 6 is chosen as a reference microphone to record the test sound broadcasted from 5 different kinds of speakers (3 TVs and 2 stereo speakers) respectively. The phone is placed in front of speakers with 1m distance. The audio volume is kept at an average level. The test sound is a 50-second sine signal sweeping from 30 to 22 kHz. Fig. 2(b) shows the frequency response of the recorded audios. An ideal frequency response should be a line at 0dB parallel to the x-axis, implying that all frequencies experience the same overall attenuation from speaker to microphone. As a result, the response below 14kHz behaves as desired, but serve frequency selectivity appears in our chosen band (18kHz\~20kHz), in which the signal attenuation varies over devices. Because as main home entertainment, TVs enhance the audio system for human hearing but weaken the 'noise' at other frequencies.

![](images/8c510b2b673b4701d0a54f1f4f78f2fb011b7ad112d2dd71afb1146a13390420.jpg)



Fig. 3: The structure of sound marker. The sound marker contains a long up-chirp (90ms) for preamble, 36 short chirps (36 × 20 = 720ms) for payload, 8 short chirps (8 × 20 = 160ms) for CRC, and 30ms blank for guard interval.

Multipath effect. Multipath (i.e. echo in acoustics) is the propagation phenomenon that several copies of transmitted signals through different paths are superposed. These copied signals with the same frequency but different time delays induce constructive or destructive interference at the receiver, leading to frequency selectivity. To characterize this interference, we measure the received acoustic power different environments using the same pair of speaker and microphone. Fig. 2(c) depicts the frequency response in bedroom, lounge, elevator, and car. Being similar to the above observations, we find that the multipath effect also leads to severe frequency selectivity. In fact, the selectivity in acoustic channel is more serious than that in electromagnetic channel due to longer wavelength.

To deal with the frequency selectivity, TagScreen adopts a group of linear frequencies (called as chirp) between 18kHz\~20kHz instead of a single tone. The practices have shown that the chirp has very excellent capability of resolving multipath propagation [6]. Based on linear increase or decrease of the frequency over time, the chirp can be categorized into two types: up-chirp and down-chirp. Formally, suppose $f_{1}$ and $f_{2}$ are the starting and ending frequency, then the time-domain function for the up-chirp and down-chirp can be expressed as $\sin\left(2\pi(f_{1}t\pm\frac{v}{2}t^{2})\right)$ , where $0\leq t\leq T$ , and v is the rate of frequency increase (or decrease), defined as $v=\frac{f_{2}-f_{1}}{T}$ and T is the time it takes to sweep from $f_{1}$ to $f_{2}$ . In practice, we fix $f_{1}=18kHz$ and $f_{2}=20kHz$ , but use two different sweeping time: 20ms and 90ms. In this way, we have four chirps: short up-chirp (i.e. T=20ms), short down-chirp (i.e. T=20ms), long up-chirp (i.e. T=90ms), and long down-chirp (i.e. T=90ms). Actually, we only use the first three chirps to represent the preamble, the symbol '0' and the symbol '1'. More details are introduced later.

# C. Marker Encoding

Finally, we design the structure of sound marker, i.e. encoding. The structure of a sound marker is shown in Fig. 3. It contains a long up-chirp (90ms) for preamble, 36 short chirps (36 × 20 = 720ms) for payload, 8 short chirps (8×20 = 160ms) for CRC, and 30ms blank for guard interval. Each marker totally occupies 1 second.

![](images/8074d9cddc90e85f4f45c9061890cfb48b69e482fe815c6407c34963bf452820.jpg)



(a) Frequencies over time

![](images/91117560c7f226775749f41ccccb247194181d120a7d7b48d9031523a3b839eb.jpg)



(b) Sound marker   
Fig. 4: Encoding example. (a) The collected audio clips over 5 seconds. (b) The corresponding frequency distribution over time. (c) Zooming into the first sound marker.

Preamble. As beginning of a sound marker, the preamble will be used for marker synchronization. We set its interval to 90ms because with regard to 44.1 kHz sampling rate, the mobile device can sample $0.09 \times 44.1 = 3,969$ points, which is at most close to $2^{12} = 4,096$ . (i.e. FFT requires the length of input sequence to be integral power of 2.)

Payload. In TagScreen, the payload contains the media context, content identifier and playing progress. We assign 22 symbols for identifiers and 14 symbols for progress. Usually, a movie or TV show lasts less than 5 hours. Thus 14 symbols ( $2^{14}/3600 = 5.5$ hours) is enough to decode the entire playing progress. For extra-long movie (playing time > 5.5 hours), we can use multiple identifiers to logically divide it into multiple parts and starts over. Totally, the sound marker can totally represent 1.1 billion minutes of contents.

Fig. 4 shows an example of how to insert sound markers to the movie ‘The Avengers 2’. We randomly record 5-second audio clip, and show its frequency using Short Time Fourier Transform to show its spectrum in Fig. 4(a). From the figure, we can see that power mainly distributes in two frequency bands. The original content audio lies in the band of 0 \~ 5kHz while our sound markers are in the band of 18 \~ 20kHz. There are 5 entire sound markers shown in total in the figure because the content is marked on second level. Finally, we zoom in to see the first sound marker, as shown in Fig. 4(b). Clearly, we can observe three segments. A long up-chirp at the beginning, as marker’s preamble, is followed by the segment of playing time composed of 22 short chirps. There are 29 short chirps for identifier. 8 short chirps for CRC in the end of the marker.

# IV. SYNCHRONIZING PLAYING

The media context, wrapped within the payload of sound marker, is broadcasted when the content is played. After receiving the sound clip, the smart devices start to decode the context. This section presents how TagScreen synchronizes the sound markers and decodes payload inside the marker.

# A. Formalizing Synchronization Problem

The received audio signal arrives in a shifted version at mobile devices due to the propagation delay, thereby we don't know when the marker starts at inside the recorded audio clip. The first task of TagScreen is to synchronize (or align) sound markers. The traditional synchronization correlates the received clip with the known preamble code in the time domain. Since the correlation is equivalent to time-reserved convolution, the correct synchronization corresponds to the one that maximizes the convolution. The synchronization problem can be formally defined as follows.

![](images/269df77310003c52e7e8896cd4d0a322cf94d1385be35bc61bf13990ccdffc67.jpg)



Fig. 5: The procedure for FFT-based alignment. The algorithm multiplies the FFT of recorded audio with the FFT of the preamble, and then takes the IFFT of the resulting. The IFFT spikes at the correct time shift for the alignment.

Definition 1: Given a sequence of received sound clip, $x = [x_{0}, x_{1}, \cdots, x_{n-1}]$ , and the time-reversed preamble code $p = [p_{n-1}, p_{n-1}, \cdots, p_{0}]$ , find the time shift $\tau$ that maximizes the correlation between x and p, i.e., computing:

$$
\tau = \operatorname{argmax} \mathbf {p} \otimes \mathbf {x} \tag {1}
$$

where $\otimes$ is a circular convolution, and $0 \leq \tau \leq n$ .

Computing this convolution needs performing n correlations, each of which has size of n, thus the total complexity equals $O(n^{2})$ . However, the convolution in time domain is equivalent to element-by-element multiplication in the frequency domain. By fully utilizing the advantage of FFT, the calculation can be re-defined as follows:

$$
\tau = \operatorname{argmax} \mathcal {F} ^ {- 1} (\mathcal {F} (\mathbf {p}) \times \mathcal {F} (\mathbf {x})) \tag {2}
$$

where $\mathcal{F}(\cdot)$ is the FFT and $F^{-1}$ is the inverse FFT, and $\times$ denotes the element-by-element multiplication. In this way, with the benefit of FFT, which has a computational complexity of $O(n\log(n))$ , the totally complexity of the synchronization process is reduced to $O(n\log(n))$ . In practice, the Eqn. 2 can be performed as follows, as shown in Fig. 5. First, the system takes the FFT of the received sound clip x and the preamble code p. Second, it multiplies the outputs of two transformed results. Third, it performs the inverse FFT on the resulting signal. This three-step process is mathematically equivalent to convolving the clip with the preamble code. As a result, the final output will spike at the correct shift that synchronizes the preamble with the received clip.

Challenge: Although FFT significantly reduce the synchronization complexity, it is still a heavy burden for mobile device to perform twice n-point FFTs and once n-point IFFT very second, i.e. sound markers are embedded at second-level. In terms of the sampling rate of 44.1 kHz, the total number of FFT and IFFT input for a 4-hour movie equals $4 \times 3$ , $600 \times 3 \times 44100 \times \log(44100) = 2.9393 \times 10^{10}$ audio points. Apparently, such hug computations (29 billions) will quickly use up the smart device's battery.

# B. Revisiting Fourier Transform

We observe that the final correlation result spikes in the time domain, as shown in the Step#3 of Fig. 5, thereby the result is actually very sparse. Recent work in signal processing has shown that if the signal is very sparse, the computations could be optimized to a linear time [7]–[9]. To this end, let us firstly revisit a basic property of the Fourier transform:

Lemma 1: Folding a signal in the time domain is equivalent to subsampling it in the frequency domain, and vice versa.

The proof of Lemma 1 can refer to [7] and be formally explained as follows. Let x be a discrete time signal, and X be its representation in frequency domain, i.e. $\mathbf{X} = \mathcal{F}(\mathbf{x})$ . Let $\hat{x}$ be the folded version of x and defined as follows:

$$
\widehat {\mathbf {x}} [ i ] = \sum_ {j = 0} ^ {n / w - 1} \mathbf {x} [ i + j w ] \tag {3}
$$

where w is the size of the folding window, $w = 1, 2, \ldots, n - 1$ and $i = 0, 1, \ldots, w$ . On the other hand, let $\widehat{X}$ be FFT of $\widehat{x}$ (i.e. $\widehat{X}$ is the frequency representation of the folded version.). Then, the relationship between $\widehat{X}$ and X is described as follows:

$$
\widehat {\mathbf {X}} [ f ] = \mathbf {X} [ f \cdot \frac {n}{w} ] \tag {4}
$$

for $f = 0,1,\ldots ,w - 1$ . Namely, $\widehat{\mathbf{X}}$ is a subsampled version of $\mathbf{X}$ .

To visually understand this lemma, we show an example in Fig. 6. With respect to w = 5, the original 10-point signal in the top left is folded to 5-point signal in the top right by adding the x[1,2,3,4,5] to x[6,7,8,9,10] respectively, i.e. $\widehat{x}[1,2,\ldots,5] = x[1,2,\ldots,5] + x[6,7,\ldots,10]$ . In the Fourier domain, the FFT of the folded signal is a subsampled version of the FFT of the original signal, i.e.

![](images/d6a07885c3c327c9d8dc60ddab09ae5eea6a28ca45a39c9494cb2ec476bff0fc.jpg)



Fig. 6: The relationship between folding and subsampling. Folding a signal in the time domain is equivalent to subsampling it in the frequency domain, and vice versa.

the samples of $\widehat{X}[1,2,\ldots,5]$ correspond to the samples of $X[1\times2,2\times2,\ldots,5\times2]$ where n/w=2. Inversely, given a subsampled $\widehat{X}$ , we could get a folded version $\widehat{x}$ .

# C. Quick Synchronization

Since the result of the final synchronization process has a single major spike at the correct shift, as shown in Fig. 5 the output of IFFT is very sparse in the time domain. Even folding the final time-domain result in some extent, the correct shift can be still distinguished. Inspired by Lemma 1, we design an efficient synchronization algorithm, called as quick synchronization, making efforts to reduce the input by one order of magnitude.

Instead of performing a full n-point FFT, we firstly fold the received audio clip x and preamble code p with a window size w, and then perform w-point FFT on the folded signals. Correspondingly, the inputs are changed from x and p to $\widehat{x}$ and $\widehat{p}$ . Similar to the example shown in Fig. 6, the results of FFTs on folded-version signals induce subsampled-version representation in frequency domain, thereby the outputs of the two w-pint FFT become to $\widehat{X}$ and $\widehat{P}$ . In Step#2, we perform the element-by-element multiplication on the results of the last step, i.e. $\widehat{X} \times \widehat{P}$ . Here, our trick is that it is straightforward to prove the following Lemma.

Lemma 2: Subsampling the multiplication of two signals equals to multiplying their corresponding subsampled versions. Namely,

$$
\widehat {\mathbf {P}} \times \widehat {\mathbf {X}} = \widehat {\mathbf {P} \times \mathbf {X}} \tag {5}
$$

$$
\begin{array}{c} \text {Proof:} \widehat {\mathbf {P}} [ f ] \times \widehat {\mathbf {X}} [ f ] = \mathbf {P} [ f \cdot \frac {n}{w} ] \times \mathbf {X} [ f \cdot \frac {n}{w} ] = (\mathbf {P} \times \mathbf {X}) [ f \cdot \\ \frac {n}{w} ] = (\widehat {\mathbf {P} \times \mathbf {X}}) [ f ]. \text {Thus,} \widehat {\mathbf {P}} \times \widehat {\mathbf {X}} = \widehat {\mathbf {P} \times \mathbf {X}}. \end{array}
$$

Then, the input of Step #3 is changed to $\widehat{P \times X}$ (i.e. $\widehat{P} \times \widehat{X}$ ). The most interesting thing happens. The last step performs IFFT on a subsampled version of $P \times X$ , what does the result mean? Reviewing Fig. 6 and Lemma 1, performing IFFT on a subsampled signal in frequency domain results in a folded version of the signal in time domain. Thus, the result of the convolution changes from $p \otimes x$ to a folded version $\widehat{p \otimes x}$ . Furthermore, the folded fashion is exactly as same as performed in the first step. As aforementioned, even folding the final time-domain result, the correct shift can be still distinguished because the spike is very sparse, i.e. majority of the folding results are still at low level. Folding can be considered as a kind of 'hashing' that n original points are hashed into w buckets. Since there is only one correlation spike in the result of IFFT, the magnitude of the bucket it hashed to will be significantly larger than that of other buckets where only noise samples are hashed to. In other words, the other buckets cannot include the correct time shift, thereby the time shifts in these buckets can be totally excluded. In this way, we can quickly find n/w candidate time shifts which are hashed into the spiked bucket. To further identify the real time shift, we can correlate the initial signal x with the preamble p using each of those n/w candidates. Finally, the shift that produces the maximum correlation is the right one.

![](images/d3f1766745531a0f8dddca283997ef4db9eb48e6a2a615bc59a3126c36636bdc.jpg)



(a) Original synchronization

![](images/6e84456d9cdd8559614b871eb5229217721b3292e2fb31e4e4b420302078f72e.jpg)



(b) Quick synchronization   
Fig. 7: Comparisons of two synchronization algorithms.

Algorithm: Finally, we put all pieces together and sketch the whole algorithms as follows.

- Input: The input of TagScreen is a recorded audio samples x with a pre-defined folding window $w = n / \log n$ .   
- Step 1: TagScreen folds the recorded $n$ -point samples $\mathbf{x}$ into $w$ -point $\widehat{\mathbf{x}}$ , as described in Eqn 3.   
- Step 2: TagScreen performs a $w$ -point FFT on the folded samples $\widehat{\mathbf{x}}$ and outputs $\widehat{\mathbf{X}}$ . Note that we can compute $\widehat{\mathbf{P}}$ in advance because preamble code remains unchanged.

\- Step 3: TagScreen calculates the multiplication of $\widehat{\mathbf{X}} \times \widehat{\mathbf{P}}$ and performs the IFFT on it. Since the input of this IFFT was subsampled, its output is folded in the time domain. Specifically, each of the $w$ buckets at the output of this step is equivalent to the sum of $n/w$ aliased time samples.

\- Step 4: TagScreen identifies the bucket with the maximum magnitude among the $w$ buckets, and further obtains $n / w$ candidate time shifts hashed into the chosen bucket. TagScreen correlates the initial audio samples $\mathbf{x}$ with the preamble $\mathbf{p}$ using each of those $n / w$ candidates. The correct time shift is the one that produces the maximum correlation.

Analysis: Let us analyze the computation complexity of quick synchronization. The folding in the first Step takes $O(n)$ . The second step performs a FFT which takes $O(w \log(w))$ . The third step performs w multiplications as well as $O(w \log(w))$ for IFFT. Finally, it performs n/w correlations to find the correct time shift. When we adopt $w = n / \log(n)$ , the length of preamble is less than w and $w \log(w)$ is less than n. Thus, the total running time of Step 4 equals $O(n)$ only. With the sampling rate of 44.1 kHz, the number of FFT (or IFFT) input is reduced from 65, 536 to 4, 096, offering $10 \times$ off.

Fig. 7 shows the correlation results of original and quick synchronization. Notice that the results could be positive or negative with different time shifts while the absolute magnitude will be considered. The original synchronization has 65,536 results while quick synchronization has 4,096 results because of the folding operation.

# D. Decoding Payload

The media contexts are wrapped within sound marker. After finding the markers in the clip (i.e. markers are synchronized.), the next task is to decode and correct media context. Since the symbols in the payload are regularly encoded with constant length and in predefined order, convolution is not necessary. TagScreen determines each symbol as the one with maximum amplitude by matching each symbol separated from the payload with short up-chirp or down-chirp.

Content identifier. The content identifier remains unchanged if the content isn't changed. If the current sound marker is too weak or suddenly interfered, TagScreen can repeat decoding on subsequent sound markers and sum up the output to average the noise. Since the spike corresponding to identifier symbols is the same in each run, it becomes more prominent. In contrast, noise exhibits random and hence they tend to be eliminated while accumulating multiple recorded sound markers. TagScreen also leverages this approach to quickly detect whether the identifier is correctly decoded rather than CRC for shortening its processing time.

Playing progress. The playing progress is used for querying comments or time-stamping posted comments. It also has another important usage of determining viewers' actions. During the course of watching, the viewer may perform unpredictable actions (e.g. pause, forward, backward, change content) at any time. The progress can be predicable if the content is normally played, which is leveraged to check users' actions. Specifically, if decoded playing progress does not equal to the predicated, user actions must be performed. Then the content ID as well as the progress are re-decoded. An extra benefit of progress tracking is to provide fundamental data for deep mining on the viewers' behaviors, which is never offered by previous work.

CRC validation. A CRC code appended to each payload is also decoded to validate whether the payload is correctly received or decoded.

# V. IMPLEMENTATION

TagScreen is a pure software based solution. It consists of three main components in domains of content provider, viewer's mobile device and social networks respectively.

Marking content. We developed a software tool using C# language for marking content. This tool firstly produces an independent marker audio that contains a sequence of sound markers, corresponding to a given content. It then merges this marker audio with the audio in the left (or right) channel of the content. Utilizing this tool, we totally marked 150 movies and 150 TVs top-ranked in IMDb. These contents are tested using one iPad, one TCL TV, two models of Sony TVs, and two sets of home stereos.

Tracking playing. We developed a third party Android (OS: v4.4) APP with ionic framework to track playing. The app uses CKFFT [10] implementation internally to compute the Fourier transform of quick synchronization. CKFFT is a library designed for iOS and Android native development, optimized for ARM devices. The app is tested on two types of smart phones (Xiaomi Redmi 2 and Sony Xperia Z2) and two types of pads (HUAWEI S8-701W and Mi Pad). These mobile devices belong to low-end machines equipped with average CPUs and microphones.

Backend Server. Our backend server is implemented using NodeJS (v4.0) with Express (v4.10). We employ MongoDB (v3.0) as our database to record the 14-bit content identifier and content information (such as movie name, cast list, etc). We also develop a simple social service to receive or query viewers' comments.

# VI. MICROBENCHMARK

We evaluate the various functions of TagScreen with regard to five different locations, living room, restaurant, car, square, and railway station, compared with conventional methods. By default, we employ the Xiaomi Redmi 2 (100 US\$) to conduct most experiments.

# A. Recognition

First, we present the recognition accuracy under five different environments including living room, restaurant, Car, Square and Railway station. We also evaluated other two industrial implementations, WeChat [2] and SampleSumo [3], as baseline. We kept the smart phone at the same place and tuned the volume of speaker to the same level while evaluating different methods. The experiments are repeated over 100 measurements. The recognition accuracy is defined as the ratio of successful recognitions to the total count of measurements. Fig. 8 plots the final recognition accuracy.

WeChat: WeChat is the most popular mobile instant messaging App in China. As of August 2014, WeChat has 438 million active users. WeChat has an important internal function that it can recognize TV content using smart phone's speaker based on the audio signature. It can achieve a recognition accuracy of $98\%$ in a quiet living room. However, the accuracy quickly reduces to $63\%$ , $22\%$ and $16\%$ in a noisy restaurant, square and railway station, suffering from the higher interference from ambient noise. What is worse, the accuracy decreases to $14\%$ because of the severe multipath effect despite in a car where is as quiet as a living room. In addition, we found WeChat takes 40 seconds on average to output results because it needs to record and upload sufficient samples to cloud for analysis.

SampleSumo: SampleSumo is another industrial product providing sound recognition for game control. It runs at personal computer instead of mobile devices, and requires to extract the audio signals in advance. Being similar to WeChat,

![](images/555769beac1689200c3c5e4c786a327a0a4159f787bc81d41f081859809dd042.jpg)



Fig. 8: Recognition accuracy

![](images/707a8c2acdad44786643098a50f3b31189125492dec9d64cf3ce0e27b3569307.jpg)



Fig. 9: Tracking accuracy

![](images/fba3ae0afee84d9e1c576e8ee153af993c3ee0daa5fd435a08d0ec4e70af75ad.jpg)



Fig. 10: Tracking delay

![](images/563c097afd5e74b5ff065b0cd2742f54ab26493e65d37a97f636d199e3f83fca.jpg)



Fig. 11: Impact of distance

![](images/6ee2f523e73a0f1b6c9a8f46dbff296fad1b190ad3904024c710e10dd37e46f2.jpg)



Fig. 12: Power consumption

![](images/654c5b5ca796e2bcde3a3ff6b913bb51b410e5797218f8d2257782ee9efba7a6.jpg)



Fig. 13: Running time

SampleSumo has a recognition accuracy of 95% in a quiet living room, but worse performance in other four places.

TagScreen: Our method has a recognition accuracy of 99%, 98%, 97%, 98% and 98% in the five different places, outperforming WeChat by 1.6×, 4.4×, 4.4× and 9.8× in four kinds of noisy environments. In terms of the recognition time, both SampleSumo and TagScreen output results within 2 seconds. These significant improvements are achieved for two reasons. First, we carefully choose an ideal frequency band carrying sound markers, which are far from the ambient noises. That is the reason why TagScreen appears to be independent on its environment. Second, chirp signal is widely used for radar applications due to its great abilities on anti-multipath and anti-frequency-selectivity. This is the main reason that TagScreen still works well in a very small space.

# B. Tracking progress

Second, we investigate the TagScreen's quality of progress tracking. We discuss the tracking performance in two aspects, accuracy and delay. We develop a mini player to randomly simulate viewers' actions, like stopping, pausing, rewinding or fast-forwarding the content. The time points are automatically recorded in log as ground truth when the actions are performed.

Tracking accuracy. Fig. 9 presents the experimental results of tracking accuracy, which is evaluated using two metrics, True Positive Rate (TPR) and False Positive Rate (FPR). The TPR indicates the ratio of correctly tracked actions to the total number of actions that are really performed. It can be observed that TagScreen can correctly detect 97% actions at the first time. Even so, the missed 3% can be still detected after a few seconds. We placed the smart phone at a fixed place and did not perform any actions to produce FPR. The FPR is the ratio of mistakenly tracked actions to the total number of detections. Since we employ the progress to determine the occurrence of actions, the smart phone performs detection every second. From the figure, we can see that TagScreen has a FPR of 2.7%. To further reduce the FPR, we can merge the tracking results of two consecutive sound markers for determination.

Tracking delay. By comparing ground truth with history of actions identified by TagScreen, we compute the time that TagScreen takes to successfully re-track the playing progress. Fig. 10 shows response delays as a function of distance. TagScreen's 90th percentiles are 1.76s, 1.9s, 2.37s and 2.73s at the distances of 5m, 10m, 15m and 20m. Note that one second delay is unavoidable because we need to collect a new whole sound marker, which takes 0.97s. It is clear that longer distance has larger delay because there is an extra delay due to sound propagation. For example, the distance of 20m introduces about extra 0.05s delay. In terms of human's reaction delay, these two second delays hardly cause influences on users' viewing experiences.

# C. Communication distance

Third, to verify the maximum transmission range, we deploy Transwin A920 speaker at our large office with 25m width and 50m length. Thinkpad laptop plays content through the speaker, where the volumes of laptop and speaker are set to 60% and 100% respectively. Fig. 11 presents the accuracy of recognition. As illustrated in the figure, TagScreen can recognize more than 97% contents within 35m, showing that TagScreen supports long-distance synchronization. The low accuracy (< 90%) at longer distance is resulted from weak volume of recording. Increasing the audio output level can further increase the range.

# D. Power consumption

Fourth, to guarantee the real-time progress tracking, TagScreen has to continuously turn on the microphone to record the raw audio clips. One concern is its power consumption. We employ Trepn Power Profiler, which is an on-target power and performance profiling application developed by Qualcomm, to measure the power consumption of TagScreen as well as other 7 popular Apps. During the measurements, all background Apps are shut down. Fig. 12 shows the power comparisons over 40 seconds. Totally, the power consumption of TagScreen is higher than that of two basic Apps (locking or unlock screen), but lower than the other 5 Apps, even less than the consumption used for browsing web pages using Safari. Notice that the top 3 energy-consuming Apps are screen- and GPU-intensive, implying that most of the power consumed in mobile device is used for lighting screen or rendering scenes instead of recording audio. This experiment shows that the power consumption is not a performance bottleneck.

# E. Running time

Last, we introduce two mechanisms, sparse FFT and preamble tuning, to reduce running time of decoding sound markers. We employ Traceview, a debug tool provided by Android platform, to check the running time taken on full FFT, sparse FFT and preamble tuning. The running time was measured under three cases labeled 'free', 'average' and 'busy', indicating how busy CPU is. The results are shown in Fig. 13. We note that the running time taken by FFT, SFFT and Tuning are $15ms$ , $2.3ms$ and $0.8ms$ . SFFT and tuning reduce the time by $6.5\times$ and $18.75\times$ respectively, offering significant improvements. Tuning is more effective but limited to the cases with slight movements or cases even without actions.

# VII. RELATED WORK

This section reviews prior work on social television and acoustic communications.

Social television: The social dimension of TV has been explored [11]–[14] many years ago. [12] presents twelve sociability heuristics for social television. [13] implements a social television system which allows people interact in synchronous or asynchronous television-viewing situations. [11] studies how people interact in front of a TV set. [14] reviews the state-of-the-arts on social television's two directions, social aspects and user interaction. This work focuses on the social aspect of the system, while our work offers the fundamental synchronization framework to support advanced applications.

Acoustic communication: The acoustic communication has been studied in [5], [6], [15]–[17]. [16] achieves a data rate at 5.5 kbps in an audible mode using multiple tones, or 1.4 kbps at an inaudible mode. [5] attempts to insert hidden information into audios. This system needs to conduct the full FFT to demodulate the hidden information, taking 6.5× time. To save energy, it processes the audio signal every 3 minutes, therefore, it cannot track playing progress in real time. [6] reviews acoustic communication as a wireless technology for short and long distance communication. [15], [17] implement secure acoustics-based NFC systems that use the microphones and speakers on mobile phones. These systems work in a very short range.

Acoustic sensing: [18], [19] study indoor localization with acoustic signals. [20] identify environment with acoustics. [21] can sense driver phone use with acoustic ranging through car speakers. Dia [22] achieves autodirective audio capturing through a synchronized smart phone array.

# VIII. CONCLUSION

In this work, we present TagScreen for synchronization of social television to second-level. A key innovation is to insert hidden sound markers for real-time playing tracking. TagScreen can extend the communication range to dozens of meters while maintaining a high recognition accuracy.

# ACKNOWLEDGEMENT

This study is supported in part by NSF China Grant No. 61572282 and NSFC/RGC Joint Research Scheme No. 61361166009.

# REFERENCES

[1] “MIT Technology Review on Social TV,” http://www2.technologyreview.com/article/418541/tr10-social-tv/.   
[2] “Wechat,” http://www.wechat.com/en/.   
[3] “Samplesumo,” https://samplesumo.com/.   
[4] P. Cano, E. Batlle, H. Mayer, and H. Neuschmied, “Robust sound modelling for song identification in broadcast audio,” in Audio Engineering Society Convention 112. Audio Engineering Society, 2002.   
[5] H. Lee, T. H. Kim, J. W. Choi, and S. Choi, “Chirp signal-based aerial acoustic communication for smart devices,” in Proc. of IEEE INFOCOM, 2015.   
[6] A. Madhavapeddy, R. Sharp, D. Scott, and A. Tse, “Audio networking: the forgotten wireless technology,” Pervasive Computing, IEEE, vol. 4, no. 3, pp. 55–60, 2005.   
[7] H. Hassanieh, P. Indyk, D. Katabi, and E. Price, “Simple and practical algorithm for sparse fourier transform,” in Proc. of ACM-SIAM symposium on Discrete Algorithms, 2012.   
[8] H. Hassanieh, F. Adib, D. Katabi, and P. Indyk, “Faster gps via the sparse fourier transform,” in Proc. of MobiCom, 2012.   
[9] H. Hassanieh, L. Shi, O. Abari, E. Hamed, and D. Katabi, “Ghz-wide sensing and decoding using the sparse fourier transform,” in Proc. of IEEE INFOCOM, 2014.   
[10] “Cricket fft,” http://www.crickettechnology.com/ckfft.   
[11] N. Ducheneaut, R. J. Moore, L. Oehlberg, J. D. Thornton, and E. Nickell, "Social tv: Designing for distributed, sociable television viewing," Intl. Journal of Human–Computer Interaction, 2008.   
[12] D. Geerts and D. De Grooff, “Supporting the social uses of television: sociability heuristics for social tv,” in Proc. of ACM SIGCHI, 2009.   
[13] M. Nathan, C. Harrison, S. Yarosh, L. Terveen, L. Stead, and B. Amento, "Collaboratv: making television viewing social again," in Proc. of ACM international conference on Designing interactive user experiences for TV and video, 2008.   
[14] P. Cesar, K. Chorianopoulos, and J. F. Jensen, “Social television and user interaction,” Computers in Entertainment (CIE), vol. 6, no. 1, p. 4, 2008.   
[15] R. Nandakumar, K. K. Chintalapudi, V. Padmanabhan, and R. Venkatesan, “Dhwani: secure peer-to-peer acoustic nfc,” in ACM SIGCOMM CCR, vol. 43, no. 4, 2013, pp. 63–74.   
[16] V. Gerasimov and W. Bender, “Things that talk: using sound for device-to-device and device-to-human communication,” IBM Systems Journal, vol. 39, no. 3.4, pp. 530–546, 2000.   
[17] B. Zhang, Q. Zhan, S. Chen, M. Li, K. Ren, C. Wang, and D. Ma, “: Enabling keyless secure acoustic communication for smartphones,” Internet of Things Journal, vol. 1, no. 1, pp. 33–45, 2014.   
[18] J. Qiu, D. Chu, X. Meng, and T. Moscibroda, “On the feasibility of real-time phone-to-phone 3d localization,” in Proc. of ACM Sensys, 2011.   
[19] W. Huang, Y. Xiong, X.-Y. Li, H. Lin, X. Mao, P. Yang, and Y. Liu, "Shake and walk: Acoustic direction finding and fine-grained indoor localization using smartphones," in Proc. of IEEE INFOCOM, 2014.   
[20] S. P. Tarzia, P. A. Dinda, R. P. Dick, and G. Memik, “Indoor localization without infrastructure using the acoustic background spectrum,” in Proc. of ACM MobiSys, 2011.   
[21] J. Yang, S. Sidhom, G. Chandrasekaran, T. Vu, H. Liu, N. Cecan, Y. Chen, M. Gruteser, and R. P. Martin, “Sensing driver phone use with acoustic ranging through car speakers,” TMC, vol. 11, no. 9, pp. 1426–1440, 2012.   
[22] S. Sur, T. Wei, and X. Zhang, “Autodirective audio capturing through a synchronized smartphone array,” in Proc. of ACM Mobisys, 2014.