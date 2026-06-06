# ChromaCode: A Fully Imperceptible Screen-Camera Communication System

Kai Zhang, Yi Zhao, Student Member, IEEE, Chenshu Wu, Member, IEEE, Chaofan Yang, Kehong Huang, Chunyi Peng, Senior Member, IEEE, Yunhao Liu, Fellow, IEEE, and Zheng Yang, Senior Member, IEEE

Abstract—Hidden screen-camera communication techniques emerge as a new paradigm that embeds data imperceptibly into regular videos while remaining unobtrusive to human viewers. Three key goals on imperceptible, high rate, and reliable communication are desirable but conflicting, and existing solutions usually made a trade-off among them. In this paper, we present the design and implementation of CHROMACODE, a screen-camera communication system that achieves all three goals simultaneously. In our design, we consider for the first time color space for perceptually uniform lightness modifications. On this basis, we design an outcome-based adaptive embedding scheme, which adapts to both pixel lightness and regional texture. Last, we propose a concatenated code scheme for robust coding and devise multiple techniques to overcome various screen-camera channel errors. Our prototype and experiments demonstrate that CHROMACODE achieves remarkable raw throughputs of >700 kbps, data goodputs of 120 kbps with BER of 0.05, and with fully imperceptible flicker for viewing proved by user study, which significantly outperforms previous works.

Index Terms—Screen-camera communication, hidden visible communication, non-intrusive visible communication

# 1 INTRODUCTION

Every day, billions of videos are generated, broadcast, and watched over electronic visual displays such as phone or tablet screens, computer monitors, TVs, and electronic advertising boards. As digital marketing evolves, people continue to see trends favoring video, especially in the era of mobile Internet. According to Cisco’s forecast [1], video traffic is projected to grow fourfold from 2016 to 2021, contributing to 82% of all consumer Internet traffic by then, up from 73% in 2016. Today such videos displayed on various forms of screens are mainly for viewing only, but we look forward to an emerging paradigm of simultaneous viewing and communication with great demands to deliver additional information at the same time. This will allow movie audiences to refer to a website for more contents, TV programs to convey interactive information, and advertisers to provide extra details for an advertising video, all during watching.

If enabled, the new paradigm will reform various existing applications and foster new possibilities. For example, it may change the digital advertising industry. Although video advertising contributes a significant portion to video companies’ revenues, currently, it is reported that 65 per-

K. Zhang, Y. Zhao, C. Yang, K. Huang, Y. Liu and Z. Yang are with the School of Software, Tsinghua University, Beijing 100084, P. R. China. E-mail: nezharen1995@gmail.com, zhaoyi.yuan31@gmail.com, yangcf10@gmail.com, huangkh13@gmail.com, yunhao@greenorbs.com, hmilyyz@gmail.com   
C. Wu is with the Department of Electrical and Computer Engineering, University of Maryland, College Park, MD 20742, United States of America. E-mail: wucs32@gmail.com   
C. Peng is with the Department of Computer Science, Purdue University, West Lafayette, IN 47907, United States of America. E-mail: chunyi@purdue.edu   
Y. Liu is also with the Department of Computer Science and Engineering, Michigan State University, East Lansing, MI 48824, United States of America.

cent of people skip online video advertising [2]. Delivering advertising content (or even the advertisement video itself) by side information without tampering primary video itself will not only guarantee viewing experience but also enhance user interaction, a key to attract consumers’ attention according to a recent research [3]. Interactive TV programs and games will also be renovated, when users can perceive multi-dimensional contents for engagement with high throughput and low latency. It serves as an attractive way deliver additional information like Easter eggs for videos and movies and augment audience interaction during public activities and live shows. We also envision great potentials in content distribution within a group of users, especially when there is poor or no Internet (e.g., on underground subways or in developing areas). All these necessitate a fully-imperceptible, high-rate, and reliable screen-camera channel to deliver the new paradigm. Existing works, however, only realize one or two of the three goals [4], [5], [6], [7].

The proliferation of mobile devices equipped with highperformance cameras sheds light on this paradigm. A common real-life example towards this paradigm is Quick Response (QR) code [8]. QR code spatially occupies a small area in the corner of a screen, or temporally appears as a large image in the end of the primary video contents. However, embedding such visual patterns, either spatially or temporally, immediately creates a tension between the two goals of unobtrusive viewing and efficient communication. A spatially affixed QR code, though small, is still intrusive and results in low rate, and requires careful attention to scan it; temporally attached QR code is larger and thus easier to scan, however, users need to dedicatedly wait for additional frames after the primary video is finished.

Recent efforts [4], [5], [6], [7] attempt to enable hidden screen-camera communication by leveraging two facts: (1) Due to the flicker-fusion property of Human Vision

![](images/830245f14503d9853fb7e6149a6b7cad628c17728e06840bfdeed27b828ee1dd.jpg)



Fig. 1: A comparison of state-of-the-art works

System (HVS), human eyes cannot resolve light intensity fluctuations, but instead perceive the averaged luminance when it alternates beyond a certain frequency of about 40-50Hz in typical scenarios [9]. (2) Today, many off-theshelf displays support 120Hz or higher refresh rates, and commodity smartphone cameras can support mega-pixel resolution images at a high capture rate. The above two facts result in an opportunity to embed data into high frame rate primary videos unobtrusively. Leveraging these properties, InFrame++ [4] achieves high throughput though with noticeable flicker, while TextureCode [6] and HiLight [5] both ensure invisibility yet at the expense of throughput.

Albeit inspiring, previous works achieve their results due to different trade-offs required to overcome the challenges in imperceptible communication and suffer from several limitations. First, perceptible flicker still remains in practice. Second, the throughput remains low. Third, they cannot recognize the code reliably under distorted screencamera channel. Fig. 1 shows qualitative comparison of state-of-the-art works. None of previous studies achieve the three goals simultaneously. And among them, TextureCode [6] embeds in only partial frames while ImplicitCode [7] is applicable to only grayscale videos.

In this work, we aim to achieve all three goals on unobtrusive, high-rate, reliable screen-camera communication while retaining video watching experience to users. Our design and implementation of embedding data into video frames excel in three unique aspects. First, we consider for the first time color space for lightness changes (Specifically, I in HSI color space, L in HSL color space, Y in YUV color space, or $\hat { L ^ { * } }$ in CIE 1976 $L ^ { * } a ^ { * } b ^ { * }$ color space, etc). The key to relax the tension between screen-to-camera data communication and screen-to-eye vision channel lies in the distribution of color space. A uniform color space fits HVS better and can improve data frame hiding quality. Existing solutions, however, never explore along this direction but use common color spaces to embed bits. However, we tackle this problem fundamentally different from others. We explore the color space and make it right at the beginning with a uniform color space. As color is merely a subjective feeling of HVS, uniform color space allows better tolerance of complimentary lightness changes because, by definition, it is perceptually uniform. Particularly, we adopt CIE 1976 $L ^ { * } a ^ { * } b ^ { * }$ color space (a.k.a CIELAB or LAB) [10], along with CIEDE2000, the latest and most accurate color difference formula currently available [11], and thus believed to be the most human-eye-friendly among all.

The second is a full-frame adaptive embedding mechanism. Invisibility is usually guaranteed by using less space and applying smaller lightness changes. Yet to gain throughput, data should be embedded in as much space as possible with appropriate lightness changes for the full frame. Applying a fixed lightness change over all pixels, however, would frequently lead to too large perceivable color changes or too small undetectable color differences, due to a previously unnoticed fact that an identical lightness change to a pixel does not necessarily produce the same color differences, depending on the original lightness and surrounding texture. Different from previous works, we manipulate lightness adaptively for each pixel in an outcome color difference driven manner and account for both original lightness and texture, which reduces user-perceivable flicker to minimum while allows full-frame embedding for high rate transmission.

Third, we achieve reliable high-rate communication. Hidden screen-camera channel usually exhibits low signalto-noise ratio and thus suffers from significant random and burst errors. Previous works mainly focus on invisible embedding or high-rate transmission, but pay little attention to reliability, which is, though, of great importance for practical applications. To ensure reliable communication, we design a concatenated error correction code scheme consisting of Reed-Solomon code and convolutional code, providing high error-correcting capability. We further devise interleaving technology to deal with burst errors and propose techniques to eliminate channel distortions including Moire pattern, ´ projection distortions, rolling shutter effect, etc, which together yield highly reliable and efficient transmission.

We have implemented CHROMACODE on commodity monitors and camera-equipped smartphones and conducted extensive evaluation including user studies. CHRO-MACODE guarantees imperceptible flicker under various conditions, confirmed by a user study of 20 users. In the meanwhile, CHROMACODE yields remarkable raw throughput of 777 kbps and data goodput of 120 kbps, and a low bit error rate (BER) of 0.05, significantly outperforming previous works under the same conditions. Such a high throughput is critical for many applications. For example, although we can transmit a web link and let the users access further information via the Internet, it may cause bandwidth wastes and high delays in places like subway stations and crowded supermarkets with poor network conditions. More importantly, the sender may not want to upload the source videos to the public network for privacy concerns. We believe such achievements promisingly shape a practical technique for the emerging paradigm of simultaneous viewing and communication, which will become more appealing in the near future.

In summary, the main contributions are as follows:

We introduce for the first time uniform color space for unobtrusive data embedding. Different from all early works, we embed bits to pixels using the most accurate color difference formula CIEDE2000 in a perceptually uniform color space CIELAB.   
• We design a novel adaptive embedding scheme in an

outcome-based philosophy, which accounts for both pixel lightness and frame texture and ensures flicker invisibility over the full frame.

We achieve reliable data transmission by a concatenated code mechanism together with multiple techniques to handle screen-camera channel errors.   
We prototype a full system CHROMACODE and compare it with previous works via experimental evaluation. We demonstrate that CHROMACODE achieves remarkably higher throughputs and goodputs with significantly lower BER than previous arts, while guaranteeing better viewing experience.

In the following, we first provide an overview of CHRO-MACODE in §2. Then we introduce adaptive embedding in §3 and robust coding in §4. Implementation and experiments are presented in §5 and §6, respectively. We review the related works in §7 and conclude in §8.

# 2 CHROMACODE DESIGN

In this section, we first introduce the design goals for a reliable hidden screen-camera communication system and then present an overview of our novel design.

# 2.1 Design Goals

We aim to achieve the following goals in CHROMACODE.

1) Fully Unobtrusive. The screen-camera communication channel is visually hidden from users. Neither the embedded images monopolize any screen space (either spatially or temporally), nor the users perceive any flicker (over the full screen) when viewing the video.   
2) High Rate. High data rate enables transmission of large volume data and results in low latency, which is critical to practical real-time interaction applications. A high data rate should be achieved regardless of the video content. In particular, we aim at up to 100 kbps, allowing delivery of e.g., a 1kb URL within 10ms.   
3) Reliable. Previous works mainly focus on the compromise between unobtrusiveness and high rate transmission. In CHROMACODE, we further keep in mind robust communication with low bit error rates. A reliable communication channel is anticipated under various interferences such as rolling-shutter effects, Moire pattern, projection distortions, ´ screen-camera distances, etc.

All three goals enable side-channel to users and provide more possibility and flexibility for content providers. However, it is extremely challenging to simultaneously achieve the three conflicting goals. For example, reducing lightness changes for full unobtrusiveness may hurt reliable and highrate communication. In contrast, applying larger lightness changes enhances reliability but may lead to flicker.

# 2.2 Design Overview

Fig. 2 illustrates the overall workflow of CHROMACODE. CHROMACODE employs commodity screens as transceiver and off-the-shelf smartphones as receiver. The sender takes primary video together with secondary side information (referred as video and data respectively hereafter) as inputs. Data are first encoded by the concatenated error correction coding scheme, with Reed-Solomon code as outer code and convolutional code as inner code. The encoded data are then modulated as an imagery code, with frame preambles and some auxiliary visual patterns included. which is adaptively embedded into the primary video in a visually unobtrusive way, producing the ultimate output at the sender (displayed on the screen and streamed over the screen-camera channel).

![](images/3f783bb5fd57ed33f153dac7c51e0401c5e3b4a46d3cf1859164f115be524c16.jpg)



Fig. 2: CHROMACODE overall architecture

On the receiver side, a video clip is captured by camera. The receiver first extracts the embedded imagery code from the captured video frames by code detection. The extracted code is then demodulated and decoded, recovering the embedded bits. During the entire receiving procedure, users can normally watch the video, without feeling affected by the screen-camera transmission.

The core of CHROMACODE is to address two tensions: (1) unobtrusive and high-rate bit embedding, and (2) highrate and reliable communication. For the first one, we tackle it through spatially adaptive embedding in uniform color space (§3). For the second one, we address it by concatenated code and robust code detection (§4).

# 3 UNOBTRUSIVE BIT EMBEDDING

In this section, we discuss how to invisibly embed data frames, in the form of image codes as shown in Fig. 5, into normal videos without affecting the viewing experience. We first assume we already have the data frames (consisting 0 and 1 data bits as white and black cells) for embedding and leave its generation and modulation to next section.

# 3.1 Bits Embedding to Pixels

Inspired by previous works [4], we also embed data frames by altering the lightness of carrier video, exerting a series of time-variant high-frequency lightness changes that are imperceptible to human eyes yet detectable to cameras. Briefly, the carrier video is first multiplexed into a high frame rate of, e.g., 120 frames per second (fps). Each data frame is rendered by a pair of successive frames with contrary lightness changes ±∆L, i.e., increasing the pixel lightness of the first frame by a certain value and decreasing that of the subsequent frame by an identical amount (or in reverse). This results in two complementary frames that visually cancel out each other’s lightness changes thanks to the flicker fusion property of HVS. Yet in the meanwhile, they still can be captured by cameras with high capture rate, allowing extraction of the carried data bits.

Despite the intuitive philosophy, in practice however, various factors may cause flicker perception, such as frame rate, primary video contents, color space, etc. In the following, we present our novel design that enables fully imperceptible embedding, without degrading the transmission capability. Overall, we consider perceptual flicker regarding three factors: color space, pixel lightness, and texture complexity.

![](images/aca3620f7e70d84db489f45fffb398ea924034c1cc4c08fbf711da0fd6884567.jpg)



(a)

![](images/060fe7bae9e347831a68bf425063694709c818791d0abb6d8d89db2c381cccb6.jpg)



(b)

![](images/16d7e9ec408cf16e16abad59611730c895a49a889ff18165f0c553b9ebd933a5.jpg)



![](images/d25e912683ebd64c5808cdb0cff52dd4c45d1b00d71650578280599af139c1cb.jpg)



(d)

![](images/facae17c47cf79125db62abee375893f54c3d31999e6ebbef63bbe6510b49045.jpg)



Fig. 3: Perception diversity w.r.t. hue palettes in (a) HSL space and (b) LAB space w/ CIEDE2000, lightness palettes in (c) HSL space and (d) LAB space w/ CIEDE2000, and (e) texture complexity.1

# 3.2 Color Space Selection

As aforementioned, flicker-fusion property of human vision system underlies the possibility of hidden screen-camera communication. Such temporal flicker-fusion behavior is like a linear low-pass filter [12]. Most of previous works [4], [5], [6], [7] leverage this feature to achieve embedded communication by high-frequency lightness changes, directly modified in common color space like YUV or RGB. However, lightness is defined differently in different color spaces, and human-perceived lightness is linear with the defined lightness only in a perceptually uniform color space.

For example, when converting from RGB color space, HSI color space defines lightness as average of R, G, B values [13], while HSL color space defines it as average of maximum and minimum R, G, B values [14]. In addition, color is only a subjective feeling of our HVS to visible light, but not physical existence [15]. Hence how lightness and color are defined and tuned significantly affects visual perception and thus the data hiding quality. Consequently, we argue that it is primary to select an appropriate color space friendly to human eyes for data embedding in screencamera communication systems.

There are many color spaces designed with a lightness dimension, such as HSI, HSL, CIELAB, etc. In CHROMA-CODE, we target at a space that well suits human vision system, especially in lightness dimension. Such a color space should ensure perceptual uniformity, which means that under its lightness definition, increasing or decreasing the lightness by ∆L should result in about the same visual color differences. Only by such condition can the eye-perceived average lightness of continuous changes from $L + \Delta L$ to $L \stackrel { } { - } \Delta \bar { L }$ be exactly equal to $L ,$ thus guaranteeing the embedded video to be perceived the same as the original version with minimal color distortions.

Prior psycho-visual studies [16], [17] propose several uniform color spaces, where a change of the same amount in a color dimension produces a change of about the same visual importance. We experimentally validate such benefits of uniform color space. Fig. 3a and 3b depict the perceptual uniformity under HSL, a non-uniform color space, and CIELAB, a uniform color space respectively. In both cases, the original colors (middle of the each sector) are of the same saturation (100%) and lightness (50%), but are different in hue ranging from $0 ^ { \circ }$ to 300◦. For each original color, we increase and decrease the lightness (outer and inner sector) by the same amount $( \Delta L \overset { \cdot } { = } 4 \% )$ . As seen, given the same lightness changes, the resulted color differences are considerably more uniform in CIELAB space. For example, for quite some hue values (especially the green parts) in Fig. 3a, one can barely see a color difference with a lightness change of $+ \Delta L ,$ , which is, however, quite clear with −∆L. As comparison in Fig. 3b, the color changes are much more consistent, regardless of the hue values. Similar results are observed in Fig. 3c and 3d where we keep hue (120◦) and saturation (100%) unchanged and alter lightness dimension from 10% to 90%.

Therefore in CHROMACODE, we select CIELAB color space for lightness modification, which describes perceivable colors with three dimensions L∗ for lightness, $a ^ { * }$ for red/green color opponent and $b ^ { * }$ for yellow/blue color opponent. CIELAB is a representative uniform color space with the latest and most accurate color difference formula CIEDE2000 applicable [10], [11]. It can be converted easily from commonly used spaces like the RGB space. Concretely, we first convert each pixel in the original color space (e.g., RGB or YUV) into the CIELAB color space, modify its lightness, and then convert it back to the original color space for display. This conversion process is necessary because the required changing values in RGB color space cannot be decided without firstly counting for the lightness change in CIELAB color space. Precision losses between color space conversions affect perception little and can be ignored. The proposed approach applies to videos represented in different color spaces. By conversion to a uniform space, we are always able to modify lightness with guaranteed consistent color changes over complementary frames.

# 3.3 Spatially Adaptive Embedding

Intuitively, we can simply apply a uniform lightness change value to a whole video frame as done in [4], [6]. However, noticeable flicker still frequently remains under such modifications due to two reasons: First, lightness change is not equal to color difference. Depending on the specific original pixel lightness, an identical lightness change may produce different outcome color differences, which may be small enough to hide flicker at some pixels, but may be

1. Figure size and PDF compression may influence the perception. Refer to online examples for better viewing: https://walleve.github. io/ChromaCode/

![](images/5373ab4704ce104d6348e1733423f128c4041ae27a4cfd455b5f7d2486319d01.jpg)



Fig. 4: Contrast(i, j) calculation

considerable large and cause visible fluctuation at other pixels. Second, video contents upon which the data frame is embedded affect perceivable flicker. In particular, video regions with smooth texture are more sensitive where small color differences may also incur flicker. Thus applying a fixed lightness change value over a full video frame may lead to regional noticeable flicker.

These limitations motivate us to design an outcomebased spatially adaptive embedding scheme for lightness modifications, targeting at ultimate outcome of color difference and accounting for primary video contents.

# 3.3.1 Outcome-based Lightness Change Derivation

In contrast to lightness-change-driven principle adopted in previous works [4], [5], [6], we propose to design an outcome $( \mathrm { i . e . } ,$ , color difference) based lightness modification scheme. Specifically, rather than applying a certain lightness change and anticipating certain color difference as output, we first specify the desired color difference and then calculate the required lightness changes for the color difference.

Denote $\Delta E _ { 0 0 }$ as the expected color difference. To gain the best uniformity in eye perception, we calculate the color difference $\Delta E _ { 0 0 }$ of a pair of color values in CIELAB space using the CIEDE2000 formula, the most accurate color difference formula currently available suggested by CIE [11]:

$$
\Delta E _ {0 0} = \left[ \left(\frac {\Delta L ^ {\prime}}{k _ {L} S _ {L}}\right) ^ {2} + \left(\frac {\Delta C ^ {\prime}}{k _ {C} S _ {C}}\right) ^ {2} + \left(\frac {\Delta H ^ {\prime}}{k _ {H} S _ {H}}\right) ^ {2} + \frac {R _ {T} \Delta C ^ {\prime} \Delta H ^ {\prime}}{k _ {C} S _ {C} k _ {H} S _ {H}} \right] ^ {\frac {1}{2}}
$$

where $\Delta L ^ { \prime } , \ \Delta C ^ { \prime }$ and $\Delta H ^ { \prime }$ are corresponding lightness, chroma and hue differences, $S _ { L } , S _ { C } , \bar { S _ { H } }$ and $k _ { L } , k _ { C } , k _ { H }$ are respective weighting functions and parametric factors, and $R _ { T } ^ { \bar { } }$ is a rotation function. As we only modify $L ^ { * }$ and keep $a ^ { * }$ and $b ^ { * }$ unchanged, both $\Delta C ^ { \prime }$ and $\Delta H ^ { \prime }$ here equal 0. The above formula can be simplified as:

$$
\Delta E _ {0 0} = \frac {\Delta L ^ {\prime}}{k _ {L} S _ {L}}. \tag {1}
$$

Then the lightness change $\Delta L ^ { \prime }$ required to achieve color difference $\Delta E _ { 0 0 }$ can be derived as $\hat { \Delta } L ^ { \prime } = k _ { L } S _ { L } \Delta E _ { 0 0 }$ with $k _ { L } = 1$ recommended by CIE [11] and

$$
S _ {L} = 1 + \frac {0 . 0 1 5 (\bar {L} ^ {*} - 5 0) ^ {2}}{\sqrt {2 0 + (\bar {L} ^ {*} - 5 0) ^ {2}}}, \tag {2}
$$

where $\bar { L } ^ { * }$ denotes the average lightness value, which equals to the original lightness in CHROMACODE as we increase/decrease it by the same amount. Then for a specific pixel at position $( i , j )$ of a video frame, the lightness change for a color difference of $\Delta E _ { 0 0 }$ is:

$$
\Delta L _ {1} ^ {*} (i, j) = k _ {L} \left[ 1 + \frac {0 . 0 1 5 (L ^ {*} (i , j) - 5 0) ^ {2}}{\sqrt {2 0 + (L ^ {*} (i , j) - 5 0) ^ {2}}} \right] \Delta E _ {0 0}, \tag {3}
$$

where $L ^ { * } ( i , j )$ is the original pixel lightness. As long as an appropriate color difference $\bar { \Delta E } _ { 0 0 }$ is specified, we can have the required lightness change value $\bar { \Delta L _ { 1 } ^ { * } ( i , j ) }$ .

Eqn. 3 indicates that the required lightness change value $\Delta L _ { 1 } ^ { * }$ for a specific color difference $\Delta E _ { 0 0 }$ depends on the original lightness $L ^ { * }$ and that the same lightness change value based on different original lightness will output different color differences, demonstrating insufficiency of conventional lightness modification approaches without considering original pixel lightness. Previous researches [18] suggest that $\Delta \bar { E } _ { 0 0 }$ should be below 6.0. We evaluate impact of $\Delta E _ { 0 0 }$ on flicker invisibility in §6.2 and give its recommended values.

# 3.3.2 Texture-based Lightness Change Adaptation

Prior research has demonstrated that video texture affects perceptual lightness changes [19]. In particular, as depicted in Fig. 3e, according to our experimental measurements, smooth regions usually expose noticeable flicker more easily while textured regions help hide flicker. Hence adjusting $\Delta L _ { 1 } ^ { * } ( i , j )$ in Eqn. 3 by accounting for regional texture complexity will further relieve noticeable flicker especially in less textured regions. Yet different from TextureCode [6] that only selects some parts of a video frame for embedding and directly discards other regions, our method seeks for appropriate lightness changes over the whole frame, retaining its full capability for transmission.

We adopt gray level co-occurrence matrix [20], a typical method for image texture measures, for this purpose. For a co-occurrence matrix $C ,$ each element $C ( i , j )$ indicates the frequency within a set of image values (i.e., gray level) that value i co-occurs with value $j$ in certain spatial relationship called displacement vector. Based on gray level cooccurrence matrix, different metrics have been defined to reflect texture complexity more precisely, such as energy, entropy, contrast, etc [21]. Here we use and compute contrast as follows.

We apply a $9 \times 9$ pixel sliding window to a video frame and generate regional gray level co-occurrence matrix, using $L ^ { * }$ of pixels in this region to represent the gray level. As shown in Fig. $^ { 4 , }$ let $\bar { C } o n t r a s t ( i , j )$ be the calculated contrast from the gray level co-occurrence matrix $M ( i , j )$ generated under a $\mathsf { \bar { y } } \times \mathsf { 9 }$ region centered at pixel $( i , j )$ with displacement vector $d = ( 1 , 0 )$ . Denote $S ( i , \bar { j } )$ as the amount of valid pixels covered by the sliding window. For most circumstances $S ( i , j ) = \mathbb { 9 } \times \mathbb { 9 } = 8 1$ , except when part of the sliding window moves out of the bound of a video frame so that $S ( i , j )$ will be smaller. Then we have the normalized texture complexity near pixel (i, j) as:

$$
\operatorname{Texture} (i, j) = \frac {\operatorname{Contrast} (i , j)}{S (i , j)}. \tag {4}
$$

A larger $T e x t u r e ( i , j )$ indicates more complicated texture near pixel $( i , j )$ . Suppose the maximum $\overset { \cdot } { T } e x t u r e ( i , j )$

![](images/f5dce7b39fd350ff5fddba3651157dd663139c23d878e71d6ff9ea0ea5d5506f.jpg)



Fig. 5: Data frame

over a whole video frame is T extureM ax. We define a lightness scaling ratio α as:

$$
\alpha (i, j) = \frac {\text { Texture } (i , j)}{\text { TextureMax }} \times (1 - k) + k. \tag {5}
$$

This maps T exture $( i , j )$ to $\alpha ( i , j ) \in [ k , 1 ]$ , where k is the minimal scaling factor and can be set to a certain value. Then we refine the ultimate lightness modification amount $\Delta L _ { 2 } ^ { * }$ as:

$$
\Delta L _ {2} ^ {*} (i, j) = \Delta L _ {1} ^ {*} (i, j) \times \alpha (i, j). \tag {6}
$$

As seen, $\Delta L _ { 2 } ^ { * }$ is scaled down from $\Delta L _ { 1 } ^ { * }$ in smooth regions with smaller $T e x t u r e ( i , j )$ .

We then use $\Delta L _ { 2 } ^ { * } ( i , j )$ as lightness modification amount for complementary pixels at position $( i , j )$ . For one pair of pixels at position $( i , j )$ in two complementary frames, we apply a respective lightness change of $\pm \Delta L _ { 2 } ^ { * } ( i , j )$ to them to embed information bit $\mathbf { \zeta } ^ { \prime } 1 ^ { \prime }$ and apply $\mp \Delta L _ { 2 } ^ { * } ( i , j )$ for bit $' 0 ^ { \prime }$ . By doing this, we successfully embed the data frames intended from streaming into the primary video frames, without impairing the viewing quality for display.

# 4 RELIABLE DATA TRANSMISSION

Data transmission is achieved by decoding the slight lightness changes of received video captured through the screento-camera channel. Besides the primary video contents, various factors may lead to channel errors, such as projection distortions, blurring, Moire patterns, rolling shutter ´ effects, etc. In this section, we present how to overcome these challenges and address the tension between high rate and reliable communication over the noisy screen-to-camera channel.

# 4.1 Encoding and Modulation

# 4.1.1 Data Segmentation

A single data frame (image code as in Fig. 5) can hold only limited amount of data bits. Thus streaming data need to be segmented into different segments, each containing K bytes for one data frame. We design the segment header as simple as possible to reduce the amount of non-data bits. As shown in Fig. 7a, the segment header contains 3 bytes, the first two for segment sequence number and the last for checksum. The checksum is simply computed as the XOR sum of all data bytes and the two sequence number bytes (as shown in Fig. 6). Assume there are N bytes of data to be streamed, and the maximum segment size is K bytes, we divide the data steam into $\begin{array} { r } { G = \lceil \frac { N } { K - 3 } \rceil } \end{array}$ segment.

![](images/8dfea3b49e3082497934db67d7b1333d809badbb53679b94d1997ebc03b6f8af.jpg)



Fig. 6: Checksum computation

Besides the three bytes, a payload length field is also needed to allow different code sizes. The payload length field is marked by a variable length of $L \stackrel { - } { = } \dot { 1 } \sim 4$ bytes, depending on segment length K (Fig. 7b). Here we use a variable length in purpose of remaining as more capacity for data bits as possible.

Supposing the capacity of a single data frame is $C ,$ we can derive the required L for the largest payload length and thus determine the largest group length $\dot { K } = C - \overset { \sim } { L }$ . The capacity is determined by data frame size. In this work, we define 40 different sizes of data frame, allowing for various requirements of code capacity. For each data frame size $C _ { k } ,$ the data frame covers 12k bits in width, and $1 2 k \times 9 / 1 6$ bits in height, where $k \in [ 1 , 4 0 ]$ .

# 4.1.2 Concatenated Error Correction Coding

Visible light communication uses systematic code like BCH code and Reed-Solomon (RS) code [4], [22] to deal with channel errors. Despite its stable error-correcting capability, RS code requires deterministic input for hard-decision decoding, while the captured video lightness varies continuously. Therefore, the performance may degrade due to channel distortions.

In ChromaCode, we apply a concatenated error correction code that employs RS code as outer code and convolutional code as inner code, which is commonly used in radio communications [23]. Convolutional code does not require each bit’s binary values, but uses their distance to $' 0 ^ { \prime }$ or ‘1’. This concatenated code works well in screencamera communication since it combines the advantages of RS code and convolutional code. As shown in Fig. 8, we divide the input data into multiple units and apply RS coding (outer code) to each unit. Then we merge the units and pass them to the convolutional encoder (inner code). By concatenated encoding, the receiver can not only benefit soft decision decoding from convolutional code, but also enjoy high error-correcting capability of RS code.

# 4.1.3 Interleaving and Data Frame Assembling

Finally the encoded data is rendered as an imagery code for embedding. Fig. 5 illustrates the overall structure of our imagery design for a data frame. It involves three types of basic elements, i.e., cell, the basic operation unit comprised by several pixels for one bit, block made from multiple neighboring cells, and line, a specially featured block formed by a column or row of cells. Structurally, the code consists of three different parts as follows.

![](images/b740ea15cf932d904934061187d450ac476bfca2d37a6a828c1f1c75d9a78c5d.jpg)



(a) Segment header

![](images/d866d6c2e2dfd0fbb018e4830108b11ef813ce86d88d9f3753420e943736de59.jpg)



(b) Payload length   
Fig. 7: Data segment header structure

![](images/54e909ae4a112ed3535ec4308e4ed1f515e874154d257ba189a4630f507b125c.jpg)



Fig. 8: Concatenated Error Correction Code

(1) Code Borders. The outmost fringe of the data frame is comprised by a rectangle with black edges. Next to it is a rectangle consisting of four intermediate black-and-white featured lines with one cell width. Together with another 3 horizontal and 3 vertical such lines crossing the rectangle, they partition the whole frame into 16 blocks (i.e., data blocks). These featured code borders are intended for code detection and localization, as well as data block recognition. The specially designed black-and-white patterns are also preserved for handling rolling shutter effects (§4.2.1) and lightness normalization (§4.2.2).

(2) Code Preamble Blocks. Inside the black-and-white borders are filled by a round of repeated square blocks (4×4 cells) intended for code preamble information. Particularly, as shown in Fig. 9, code preamble information include 2 bits for segment sequence number (the last two bits of segment sequence number after segmentation, remained for handling rolling shutter effects as will be detailed below), 2 bits for RS code error correction level and 1 bit for convolutional code error correction level. We apply BCH coding to generate 10 parity bits for these 5 bit information, occupying 15 bits in total. The remaining 1 bit in the code preamble block is used as the checksum for the abovementioned 15 bits. In addition to the strong error-correcting code, we further repeat the 16-cell block for many times in the data frame (Fig. 5) to ensure successful delivery of the code preamble information, which is critical to decoding at the receiver side.

(3) Data Blocks. All the remaining space except for the above two parts are used for rendering the encoded data bits. Since screen-camera channel may suffer from burst errors due to rolling shutter effects and primary video contents, which means some continuous areas encounter errors. Burst errors will degrade the error-correcting capability of both RS code and convolutional code. To alleviate it, we borrow interleaving technique from radio communication to disperse potential burst errors such that error correction code can deal with them as random errors. To apply interleaving, we partition the data space of a data frame into 16 equally sized blocks, each containing a certain number of cells determined by the specific code capacity. The blocks are filled with the encoded data bits in an iterative columnby-column manner, with black representing 1 and white representing 0. Specifically, we place the first 16 bits of the encoded data bits at the first left-top pixel of each data block respectively, in the order as indicated by Fig. 5. We

repeat this procedure for all data bits, while during each iteration, we shift the pixel position to the next on the right (or the left first of the next row if current row is fulfilled). When all encoded data bits are rendered, an imagery code is produced as the data frame.

The data frame is then invisibly modulated onto the primary video frames for transmission by adaptive embedding, as stated above in Section 3. The resulting video is then displayed on the screen, delivering to users as normal video yet to cameras as embedded frames.

# 4.2 Demodulation and Decoding

Here we discuss data decoding and demodulation assuming that embedded video frames are available and code positions in the frames are detected, and postpone how to extract embedded frames from the captured video and detect code positions to next section.

# 4.2.1 Demodulation

When code positions are recognized, the data frame can be obtained by subtraction over two complementary video frames in lightness dimension. Note that CHROMACODE supports dynamic primary video contents. Even for dynamically changing video frames, we notice that the adjacent frames are mostly similar, allowing our subtraction mechanism to work. As a pair of complementary frames possess the same video content, only positive and negative lightness values remain after subtraction, which reflects the received data frame. Ideally, if the channel is perfect, this received data frame will be exactly the same with what was embedded at the sender side. However, significant biases exist as the captured video has undergone various channel distortions including imprecise code positions, rolling shutter effects and so on. In this subsection, we present how to precisely recognize the code and deal with rolling shutter effects.

Code Recognition. The first step of demodulation is to recognize code capacity, which determines the size (width and height in pixels) of a cell. We also need to resolve the code positions as precisely as possible, especially when code boundary detection (§5) causes potential errors. We achieve precise code positioning and recognition jointly by looking into the four featured black-and-white border lines as shown in Fig. 5.

Recall that we have defined 40 ranks of code capacity, with a gap of 12 cells in width between adjacent ranks.

![](images/bc04e9666278ee26ebd66362899cb2a6275d4c960f9926ec220d87f9da16f5a4.jpg)



Fig. 9: Code preamble blocks

Each rank is specified with a fixed aspect ratio of 16:9. Hence we can simply vote among the 40 candidate patterns by evaluating how each of them agrees with the captured patterns. For each of the four lines, denote $g _ { 1 } , g _ { 2 } , . . . , g _ { N }$ as the extracted lightness values of the N pixels it covers. Supposing the line should contain K cells under a specific code capacity, we can calculate a corresponding similarity S as:

$$
S _ {K} = \frac {1}{N} \left| \sum_ {i = 1} ^ {N} g _ {i} (- 1) ^ {\left\lfloor \frac {(i - 1) K}{N} \right\rfloor} \right| \tag {7}
$$

Exceptions are for left and right vertical lines, for which the lightness may be reversed due to rolling shutter effect. Suppose the rolling shutter happened at the jth pixel, then the true similarity $\bar { S } _ { K }$ should be revised as:

$$
S _ {K} = \frac {1}{N} \left| \sum_ {i = 1} ^ {j - 1} g _ {i} (- 1) ^ {\left\lfloor \frac {(i - 1) K}{N} \right\rfloor} - \sum_ {i = j} ^ {N} g _ {i} (- 1) ^ {\left\lfloor \frac {(i - 1) K}{N} \right\rfloor} \right| \tag {8}
$$

Since we do not know the true j at this moment (next subsection will present how to infer the exact j), we choose $j \in [ 1 , N ]$ that maximizes $S _ { K }$ in Eqn. 8.

We sum up the $S _ { K }$ from all four lines and compare the sums for every possible code capacity. The code capacity that yields the largest similarity is then selected. As adjacent capacity ranks are 12 cells apart, we can find the correct code capacity confidently.

Once we have the code capacity information, the cell size in pixels as well as the data block positions are also known. Then we compute the lightness of each cell as the averaged value over all pixels within the cell, which will be used for soft-decision decoding in §4.2.2 after eliminating the impacts of rolling shutter effect.

Rolling Shutter Effect Correction. When recording a picture or a video frame, modern cameras don’t capture a snapshot of the entire scene instantly at one time, but instead scan the scene line-by-line horizontally, which is the well-known rolling shutter effect [24]. As a result, the pixels of different rows in one image are actually captured at different time instants. In CHROMACODE, cameras capture video frames at the same frame rate as video displays on screen. Therefore, one frame captured by the camera may in fact come from two successive video frames played on the screen, with one dimmed horizontal line dividing them, as shown in Fig. 10. Upper the line is the previous frame while lower the line is the subsequent frame. This will lead to reversed lightness difference when taking the subtraction of two frames. In addition, the line itself is dimmed, leading to burst errors around it.

![](images/63b05f64bd98f72be2eda53571c1fb2584fef4c63c4184bf1f9a2714acfb74fd.jpg)



Fig. 10: Rolling shutter effect

Albeit we have employed interleaving technique in the encoding scheme to alleviate unpredictable burst errors, we particularly correct rolling shutter effect before decoding. Recall Section 4.1.3, we have designed 5 specially featured vertical black-and-white lines in our code (See Fig. 5). We can identify where the rolling shutter exactly happened by examining from where the sequenced black and white cells are inverted. To detect that position, we can simply reuse the similarity formula in Eqn. $^ { 8 , }$ while we denote $g _ { 1 } , g _ { 2 } , . . . , g _ { n }$ as the average lightness of each cell and n as the number of cells contained in each line. The calculated similarity $S _ { j }$ will reach its maximum when j is the exact cell where rolling shutter happened, because for any other $j$ there will always be some mismatches between the captured lightness and the predefined black and white sequence. Therefore, the position of rolling shutter is estimated as $\hat { j } = a r g m a x _ { j } S _ { j }$ . Each of the 5 vertical featured lines can output an estimate of the position. We then interpolate among the 5 estimates to derive the ultimate position, and revert the lightness change values below that position. By doing so, the impacts of rolling shutter effects are corrected.

# 4.2.2 Decoding

Normalization. After demodulation, we have the received data frame with corrected lightness for each cell. Ideally, each positive lightness value shall represent bit $\mathbf { \zeta } ^ { \prime } 1 ^ { \prime }$ while negative represents bit $' 0 ^ { \prime }$ (or vice verse). In practice, however, due to screen-camera channel distortions, there may be significant lightness offsets, making this simple strategy infeasible. To combat lightness distortions, we normalize the subtracted lightness values to [0, 1] and employ softdecision decoding to leverage their tendency to bit $\mathbf { \zeta } ^ { \prime } 1 ^ { \prime }$ or $' 0 ^ { \prime }$ .

Again we take the featured black-and-white lines as references for lightness normalization over the data frame. Particularly, we use the median lightness of all black and white blocks on these featured lines as reference values for bit 1 and $0 ,$ denoted as $R _ { 1 }$ and $R _ { 0 }$ respectively. Denote the lightness of the data cell centered at $( i , j )$ as $\Delta L ( i , j )$ . Then we normalize $\Delta L ( i , j )$ to $\Delta L ^ { \prime } ( i , j )$ by:

$$
\Delta L ^ {\prime} (i, j) = \left\{ \begin{array}{l l} 1 & v > 1 \\ v & 0 \leq v \leq 1 \\ 0 & v <   0 \end{array} \right. \tag {9}
$$

TABLE 1: Representative primary video clips and tags used in the experiments 

<table><tr><td></td><td>Zootopia (Z) [25]</td><td>Football (F) [26]</td><td>GTA V (G) [26]</td><td>Minecraft (M) [26]</td><td>Town (T) [26]</td></tr><tr><td></td><td><img src="images/92213f495cb8cb1107239ea7dd85a2af73a6278272ad435f40f3eb9704da55f6.jpg"/></td><td><img src="images/6ead0513bc4fdac918ada01662ca95f19c679d53917939698c59638adf099181.jpg"/></td><td><img src="images/2c92ff415ff52975a04dccd54b876c06ac7865cb5f7a8652e479333c8916c83b.jpg"/></td><td><img src="images/d5e0824787c7fac0dfd3eefa3e9258bbc83ffaddb70704eb89036e1f830cd48c.jpg"/></td><td><img src="images/c6bb895d2bf88588f9871aac10e6dba6fbe347bd5ab53533e4fa2f7b38c4b66f.jpg"/></td></tr><tr><td>Texture</td><td>Plain</td><td>Textured</td><td>Textured</td><td>Textured</td><td>Plain&amp;Textured</td></tr><tr><td>Switching</td><td>Gradual</td><td>Gradual&amp;Sharp</td><td>Sharp</td><td>Gradual</td><td>Gradual</td></tr><tr><td>Luminance</td><td>Bright</td><td>Bright</td><td>Dark</td><td>Bright</td><td>Dark</td></tr><tr><td>Quality</td><td>SD</td><td>SD</td><td>HD</td><td>HD</td><td>SD</td></tr></table>

$$
v = \frac {\Delta L (i , j) - R _ {0}}{R _ {1} - R _ {0}} \tag {10}
$$

By Eqn. 9, we map each cell’s lightness to a value within [0, 1], which is sufficient for our soft-decision coding scheme, without the need to force them to binary values of 1 or 0.

Convolutional Decoding and RS Decoding. We read normalized lightness of each data cell in the same order as interleaving during encoding process, leading to a sequence of data values between [0, 1]. Then we identify the preamble blocks and extract code preambles including segment sequence number, RS code and convolutional code correction levels. With the data sequence and code preamble information, decoding basically works in two steps: First, we decode the inner convolutional code with Viterbi decoding algorithm [27], which, in brief, seeks for a Viterbi path of most likely sequence in terms of certain distance metric. This step takes advantages of its soft-decision decoding property, which calculates code distances from the normalized lightness values to 1 or 0 but not quantize them by a hard threshold of, e.g., 0.5. After that, we conduct RS decoding upon the decoded output of convolutional decoding, and finally obtain the original segmented data.

Segment Combination. Finally, all decoded data segments are fused together according to their segment sequence numbers to recover the entire data bits.

# 5 IMPLEMENTATIONS

We have developed data frame embedding program on computers as the sender, as well as Android application on smartphones as the receiver. To embed codes in normal video at sender, we use FFmpeg [28] tool to duplicate primary video frames to 120fps as well as compress the modulated video frames into the final ready-to-transmit video. We use MediaCodec [29] from Android API for hardware video decoding at receiver. We do image processing with Qt [30] at the sender and OpenCV [31] at the receiver. 2 In the following, we discuss some implementation details that address several practical challenges.

When compressing frames into H.264 video with FFmpeg, one parameter is used to control the compressed video quality, namely constant rate factor (CRF). CRF can be assigned a value from 0 to 51. The smaller the CRF, the better the video quality and the larger the video size [32]. Low video quality will exacerbate viewing experience, especially when certain codes are embedded. Therefore, it is

2. All our implementation and the following evaluation programs and data are available upon request.

a compromise between video size and watching experience, as evaluated in §6.

Smoothing Transitional Frames. While the proposed spatially adaptive embedding scheme gracefully renders data frame imperceptibly, Flickers may be potentially observed when data frames switch. This is because successive frames carrying two different data frames do not complement with each other in lightness changes. To overcome this, we follow InFrame++ [4] to smooth the transition by decreasing the lightness change value for transitional frames.

Data Frame Localization. Unlike InFrame++ [4] that uses visible locators and invisible alignment patterns around data frame borders for code block localization, which affects video watching experience and shrinks precious code embedding spaces, we perform full-screen data frame embedding. The code borders are the same as the video borders, and also the same as the monitor inner border (we assume the common case that video is playing at full-screen mode). Thus we can perform code localization by detecting the screen border, without any extra visible locators or patterns. There are already mature techniques for screen border detection. In CHROMACODE, we combine Canny algorithm [33] and Hough transform [34] for this purpose.

Handling Channel Distortions. We also overcome several screen-to-camera channel distortions that may cause burst errors and noises for data transmission.

1) Projection Distortions. Geometric distortion is a unique challenge of screen-camera channel, which is due to the unparallel camera plane and screen plane, i.e., an angle exists between them. Therefore the boundary of captured video frames are not regular rectangles but distorted quadrilaterals. CHROMACODE addresses this issue by recovering the distorted frames via projection transformation under homogeneous coordinates [35].

2) Moir´e Pattern. Images taken from an electronic display with a digital camera may exhibit Moire patterns because ´ both electronic screens and digital cameras display or capture images by line-by-line scanning [36]. Moire patterns ´ will blur the captured frames and act as noises to screencamera channel, preventing precise code block recognition. Fortunately, as Moire patterns usually occur at relatively ´ high frequency [37], they can be eliminated by low-pass filtering. In CHROMACODE, we apply Gaussian smoothing to the received frames to attenuate high-frequency components, which is demonstrated to effectively overcome Moire´ patterns.

![](images/7d4c5aaf6af9d56896296d7c93dd862f90614b9732bd97d5cd4f6af8b9716aa3.jpg)



Fig. 11: Impact of video sources

![](images/300181ec7979cf64125ae8390e94407b34f5a34c2205f9880ed28c7a520d2ca6.jpg)



Fig. 12: Impact of color space

# 6 EXPERIMENT EVALUATION

# 6.1 Experimental Methodology

Our evaluation contains two major parts, a user study that evaluates the user perceived data hiding quality and a data transmission benchmark that demonstrates the throughput and BER under various conditions. For both evaluation, we implemented two related schemes, InFrame++ [4] and TextureCode [6], for comparison.

Experiment Settings. We use a DELL XPS 8900-R17N8 desktop as the sender for video generation and playing, which has a GeForce GTX 745 graphic card that supports hardware video acceleration for efficient 120fps video playing and an AOC AGON AG271QX 27 inch monitor that supports 120Hz refresh rate. The screen resolution is fixed to 1920×1080. By default the receiver is run as an App on a Nexus 6P smartphone. Note that the camera frame rate is not necessarily the same as the screen refresh rate. Any camera that supports a capture rate equal to or higher than the screen refresh rate can work as the receiver.

Video Selection. We select a group of videos as primary videos for experiments. A key consideration is to find a set of representative videos with various characteristics, e.g., incorporating both plain and textured frames, involving both sharply and slowly switching scenes, containing both dark and bright scenarios, and covering both high definition (HD) and standard definition (SD). Accordingly, we choose 10 different videos for experiments. Table 1 shows screenshots of 5 representative video clips and their characteristics. Resolutions of HD videos are all 1920×1080, while those of SD videos are relatively lower. Besides, CHROMACODE supports 4K video as long as sufficient 120 fps 4K video playing is supported by the graphic card.

Comparative Approaches. As we do not have access to the source codes of InFrame++ and TextureCode, we make our own implementations according to their paper. TextureCode uses YUV color space for lightness modification. InFrame++ authors did not clarify what color space they use. However, as their sender is mainly implemented in GPU, we speculate it uses YUV color space as well since GPUs commonly use YUV color space. TextureCode

![](images/607f8a737150212173ba607186caa972605fb15664a2f7144d5c3d06af25b545.jpg)



Fig. 13: Impact of $\Delta E _ { 0 0 }$

additionally faces a major issue that code positions are unknown to receiver, for which they simply assume that the receiver already has the knowledge from the sender. In our implementation, we follow the same settings for TextureCode.

User Study. Since it is very difficult to quantify the invisibility using an objective technical metric, we perform user surveys for evaluation, as many previous works do [4], [5], [6]. We invited 20 participants with 8 females and 12 males ageing in range of 20 to 40 with healthy vision conditions to watch 67 experimental videos under various conditions and assess on the data hiding quality according to their watching experience. They are asked to score the perceived flicker level by 5 grades from 1 to 5, where 5 indicates completely imperceptible, 3 means slightly perceptible but not affecting much the watching experience, and 1 indicates severely affected watching experience. To reduce score bias among different users, we provide sample videos of score 1 to 5 for their references. Users are told to watch the videos normally as they usually do. They are not required to remain static during watching.

The experiment videos are displayed to users in a fixed, previously randomized order. As some of our selected primary videos are of low quality, they may have very obvious flickers or pixel block borders even without any data embedded. For participants’ convenience of no need to distinguish whether flickers in test videos are caused by embedded data or by low quality of the primary video itself, and to eliminate the interferences of the diversity of primary video qualities on the flicker level and avoid psychological implications, we mix primary videos with their embedded versions for user assessment and then calculate the relative score of each video as score = score embedded/score origin×5, where score origin and score embedded indicate the respective scores users gave on the video before and after embedding. If score > 5 (which means score embedded > score origin), we let score = 5. if score < 1, we let score = 1.

Data Transmission. We conduct experiments to evaluate the throughput and BER and study the impacts of various factors and environment conditions. We use three metrics. 1) Data goodput (goodput or G Data hereafter): the effective throughput of correctly decoded data bits, which is the ultimate goal for data communication; 2) Raw throughput (throughput or T Raw hereafter): throughput accounting for all received bits, which is, albeit not achievable in practice due to errors, useful for indicating the upper bound of potential throughput; 3) Bit error rate (BER): the number of error bits divided by total received data amount.

![](images/47800543c564ee59dd9bd509f36c1ee76b9c4820f36ba29a495b27842dffced4.jpg)



![](images/a39ba52cc1685e8c05b067a0328b76a50b4259a777e27fbbb34f4e3eeae5315c.jpg)



Fig. 14: Impacts of k

![](images/8c0addae59694b1352a312188a9ced171071e05f6427bba7b0195a863e0544e2.jpg)



![](images/32e5ce0e5983856af6f2217df698a84b545965196110c1738ce7d660b742ec13.jpg)



Fig. 15: Impact of CRF

![](images/033f1f3d1d8deedc5c5670460805fdd83060a65f5391b6abcd07a41dce734580.jpg)



![](images/e0daaa3c9684ce96f041fa52406c873b50a7fc1475dba11de71a895fa07a26b8.jpg)



Fig. 16: Impact of data cell size

![](images/7cc21c403362fe04e012752dbdd6c91e52bb303b13a71000d24650207c795792.jpg)



![](images/c5d5e3ac7825b5aa3e663a726836ba259cf198569f361cd8ca42b0ae9fafe8ed.jpg)



Fig. 17: Impact of distance

# 6.2 CHROMACODE Performance

By default, we set $\Delta E _ { 0 0 } = 2 . 0 , k = 0 . 5 , C R F = 1 2 ,$ data cell size as 10×9, convolution code error correction level as (3, 1, 5), RS code error correction level as (30, 11), and test at typical watching/recording distance 50 cm. Under default settings, CHROMACODE achieves remarkable throughput of 777 kbps and goodput of 120 kbps, with a BER of 0.05. Note that the ultimate goodput is much smaller than the raw throughput. This is because the concatenated code occupies a significant portion of channel capacity for parity bits, which can be changed by using different error correction levels.

In the following, we examine the impacts of some individual parameters by varying each of them while leaving others unchanged as the default values. For all boxplots in Fig. 11-17 and Fig. 21, black lines are medians, red dots are means, and green dots are outliers.

Video sources. We first evaluate the results on different source videos in Fig. 11. Different videos exhibit considerably diverse performance due to their disparate properties in terms of texture, luminance, quality, etc (See Table 1). In short, videos achieving higher data hiding quality usually lead to low throughput and high BER. For example, both GTA V and Minecraft video clips, two HD videos with highly textured contents, yield the highest data hiding quality with mean score of nearly 5, but also the lowest throughput. The other two videos Zootopia and Town produce the contrary results. This is natural because when flicker is imperceptible to users, it also becomes difficult for cameras. We test with 5 additional highly textured videos [26]. The raw throughputs range from 312 to 621 kbps, goodputs range from 5 to 56 kbps, and BERs range from 0.09 to 0.12. These results prove that good performance remains over various videos with diverse properties. In the following, we choose Zootopia as the default video for parameter study. The results using other videos can be similarly inferred.

Color space. We compare bits embedding in LAB color space and three non-uniform color space, i.e., YUV, HSL, HSI, all with a lightness dimension. As shown in Fig. 12, thanks to the perceptual uniform color differences, CIELAB color space yields significantly better invisibility than the other color spaces, without downgrading the data transmission performance (the best data rate and BER are obtained by LAB color space).

Color difference $\Delta E _ { 0 0 } .$ Fig. 13 shows the impacts of $\Delta E _ { 0 0 } .$ . As seen, as $\Delta E _ { 0 0 }$ increases from 1.5 to 3.5, both raw throughputs and goodputs increase, from 734 kbps to 846 kbps and from 94 kbps to 151 kbps respectively, while BER decreases from 0.07 to 0.03. The data hiding quality consistently remains at a graceful level (mean and median scores above 3) regarding different $\Delta E _ { 0 0 } ,$ , although it slightly drops to be observable in several cases when $\Delta E _ { 0 0 }$ is as large as 3.5. We believe that $\Delta E _ { 0 0 } \in [ 2 . 0 , 3 . 0 ]$ is a good compromise for both invisibility and transmission performance.

Scaling factor k. Fig. 14 presents the performance impacts of scaling factor k in Eqn. 5 for lightness adaptation. As expected, smaller k (which means smaller changes in smooth regions) results in less flicker, although the differences are marginal. However, transmission is more sensitive to k. As k decreases from 0.7 to 0.3, the BER increases significantly from 0.04 to 0.09, while goodput degrades from 138 kbps to 59 kbps. Considering the lightness changes even in smooth regions should be significant enough for capture, we suggest a safe range of k ∈ [0.4, 0.7].

Data cell size. We examine the performance under different data cell sizes, which are changed at the sender side and automatically recognized by the receiver. As shown in Fig. 16, both throughputs and BER increase with smaller data cell size within one frame. This is intuitive since, smaller data cells mean more data blocks that convey more bits within a single frame while at the same time increase the probability of bit errors. Specifically, the overall goodput increases from 28 kbps to 137 kbps when cell size decreases from 26×17 to 8 × 7, while suddenly drops to 58 kbps when data cell size further decreases to $6 \times 6 .$ . The drop is due to too small data cells to be correctly recognized at the receiver.

Constant rate factor CRF . We observe that lossy video compression (with large CRF ) will lead to poor invisibility. As shown in Fig. 15, when CRF increases from 8 to 24 and the compressed video quality accordingly degrades, data hiding quality scores decrease significantly and go below 3 when CRF exceeds 20. In the meanwhile, larger CRF also resulted in decreased throughput and increased BER. Therefore, CRF should be no more than 20 in practice to ensure unobtrusiveness and good throughput.

![](images/28b9c1df6747cb02cd59bf5e8147a8774af2fc11cb85a5d3dddda1dc1d45096b.jpg)



Fig. 18: Impact of error correction level

![](images/398d43a6636729395fb3f7d5ba6659dfeea502dc1b334455f38b387c623c478c.jpg)



Fig. 19: Impact of ambient luminance

IEEE TRANSACTIONS ON MOBILE COMPUTING   
![](images/56382ce018fe10b0ca7c483fe5f67229a5bc0937d6b21661311340e847719a4f.jpg)



Fig. 20: Impact of recording angle

TABLE 2: Energy consumption (W) 

<table><tr><td></td><td>Nexus 6P</td><td>Pixel 2</td></tr><tr><td>Video recording</td><td>0.05</td><td>4.11</td></tr><tr><td>Screen border detection</td><td>0.62</td><td>1.11</td></tr><tr><td>Demodulation and decoding</td><td>0.76</td><td>1.38</td></tr></table>

TABLE 3: Encoding/Decoding speed (fps) 

<table><tr><td></td><td>PC</td><td>Nexus 6P</td><td>Pixel 2</td></tr><tr><td>Encoding and Modulation</td><td>6.5</td><td>-</td><td>-</td></tr><tr><td>Screen border detection</td><td>-</td><td>3.8</td><td>8.0</td></tr><tr><td>Demodulation and decoding</td><td>-</td><td>0.6</td><td>2.2</td></tr></table>

Watching and recording distance. Fig. 17 illustrates the performance at various watching and recording disances. Evidently, the data hiding quality improves over larger watching distances. When watching from a distance of 180 cm, all participants give the highest invisibility scores for all videos. However, the flicker becomes challenging to be captured by cameras as well when it is too far to be seen by eyes. When recording distances increase from 60 cm to 180 cm, both throughputs and goodputs degrade from 697 kbps to 112 kbps and 56 kbps to 0.47 kbps respectively, while BERs increase from 0.09 to 0.12. Larger data cell sizes will improve performance over long distances. For example, a throughput of 309 kbps can be achieved at 180 cm when using a data cell of 14×12.

Error correction level. Both RS code and convolutional code have variable input/output radios (error-correcting capability). we denote error correction level of convolutional code as (N, K, L), and that of RS code as (N, K), with N being output symbol rate, K being input data rate, and L being constraint length. In ChromaCode, we design four ratios for RS code including (30, 6), (30, 11), (30, 17), (30, 20), and two for convolutional code including (2, 1, 8) as well as (3, 1, 5), resulting in 8 different error-correcting levels. We evaluate the impacts of 4 out of our 8 different error correction levels and depict the results in Fig. 18, where we plot both the BERs after convolutional decoding (BER Conv) and after RS decoding (BER RS). We make two observations. First, concatenated code achieves lower BERs than any individual code scheme. Second, higher error

![](images/ead80ddf4c3a54164751ccdfc4ae10a6ec54c603d1068ed582b7d0b8e467bc83.jpg)



Fig. 21: User bias

correction levels of convolutional code or RS code lead to lower BERs, yet the latter’s impacts are far more marginal than the former. However, higher error correction level also means lower data throughput, as parity bits occupy more space. As a trade-off, we by default recommend the error correction levels of convolutional code as (3, 1, 5) and RS code as (30, 11).

Ambient luminance. Fig. 19 shows the performance impacts of ambient luminance. We test under ambient luminances ranging from 0 to 300 lux, with the screen luminance fixed to 300 lux. As ambient luminance increases, data goodput slightly decreases and BER increases since more interference is resulted from higher ambient luminance. However, the impacts of ambient luminance on data rates and error rates are negligible.

Recording angle. We carry out experiments to test the impacts of different recording angles. The recording angle here refers to horizontal angle between the camera and perpendicular bisector of the screen. As shown in Fig. 20, the performance degrades with larger recording angles. Raw throughputs decrease to 531 kbps at 15 degrees and 365 kbps at 25 degrees. Data goodputs between 15 to 25 degrees are about 40 kbps and BERs are about 0.10. The performance degradation is not only owing to projection distortion, but also due to larger distances from the camera to the outermost side of screen due to the angle.

Hardware diversity. We compare the performance on Pixel 2 smartphone. The raw throughput, goodput, and BER, under default settings, are 632 kbps, 55 kbps, and 0.09 respectively, which is slightly worse than Nexus 6P (recall the first paragraph in this Section). Such hardware diversity may arise from differences in camera quality and drivers that automatically control focusing and exposure time when recording video.

Hand motions. Hand motions during video recording will introduce extra distortions and potentially degrade performance. We test the performance in practical use cases when the receiver is held by user hand. The default performance achieved in raw throughput, data goodput, and BER are 627 kbps, 70 kbps and 0.09 respectively, which are slightly worse compared with fixed cameras.

![](images/cf2dafbd5a163793df468fdb51e373e3c1140be24a935b83a020596b99bbe208.jpg)



Fig. 22: Comparative study

Energy consumption. Table 2 shows energy consumption at the receiver implemented on Nexus 6P and Pixel 2 smartphones respectively. While CHROMACODE consumes more overall energy on Pixel 2 than Nexus 6P, we make two futher observations: 1) Demodulation and decoding module consumes more energy than screen border detection module. 2) The power consumption for video recording varies violently on different devices, depending on the specific smartphone OS and camera hardware capability.

Encoding/Decoding speed. We evaluate the encoding and decoding speed of CHROMACODE. The sender is a DELL XPS 8900-R17N8 PC equipped with 8×3.40 Ghz CPU, DDR4 RAM and 7200 rpm HDD. The receiver is run on Nexus 6P with 4×1.55 GHz & 4×2.0 GHz CPU as well as Pixel 2 with 4×2.35 GHz & 4×1.9 GHz CPU. By the time of writing our implementation of CHROMACODE mainly uses CPUs for computing and has not performed GPU optimization. The experiment results are summarized in Table 3. At the receiver the demodulation and decoding speed is lower than that of screen border detection. Decoding speed on the more powerful Pixel 2 is faster than that on Nexus 6P. However, neither encoding nor decoding speeds have supported real-time capability now, which is remained for our future works. Briefly, there might be several ways to achieve real-time communication: First, the encoding could be done offline. Second, the calculation of Eqn. 3 could be implemented in a table look-up way to save computation. It may be feasible to accelerate by decoding on only a subset of pixels and applying the results to the nearby pixels. GPU implementation and light coding mechanism are also under consideration.

User bias. From Fig. 21 we learn user bias on their scores given to the invisibility of CHROMACODE. The low scores below 2 are mainly given to two videos with CRF = 20 and $C R F ~ = ~ 2 4 ~ $ , whose compression qualities are very low and thus flickers are more obtrusive. Excluding these two videos, all mean and median scores given by our 20 volunteers are higher than 3. Different users may have quite large bias in flicker perception. For example, volunteer #1 and volunteer #5 tend to give more scores of 5, while volunteer #15 mostly gives scores of 3.75, indicating that volunteer #15 is more sensitive to video distortions.

Finally, we would like to point out that, despite of CHROMACODE’s significant improvements, the achieved BER is somewhat still high compared to typical radio or acoustic communications (typically under $\mathrm { i } 0 ^ { - 3 } )$ . Screencamera channel is a very noisy channel that may suffer from rolling shutter effect, Moire pattern, etc. Moreover, in ´ hidden screen-camera communication, we only make tiny modifications to videos to ensure invisibility. All these raise significant challenges in efficient decoding, which remains room for future enhancements.

# 6.3 Comparative Study

We compare the performance of CHROMACODE with two state-of-the-art approaches, namely, InFrame++ [4] and TextureCode [6]. Similar to CHROMACODE, both InFrame++ and TextureCode achieve different throughputs under different settings. For a fair comparison, we compare the invisibility and BER when they reach at equivalent throughputs. We adapt the data cell sizes of each system so that a specific throughput is obtained, and measure the corresponding invisibility scores and BER. Other parameters such as watching distances are kept identical for all systems.

The experimental results on 3 primary videos (Z, G, and T) are demonstrated in Fig. 22. As seen, although Texture-Code retains graceful invisibility consistently, the throughputs it can achieve are considerably low, ranging from 1 kbps to only 95 kbps, yet the BERs are fairly high. This is because TextureCode does not embed in plain regions, and does not use error correction codes. As comparison, both InFrame++ and CHROMACODE yield throughputs up to 500 kbps, while CHROMACODE further reaches about 1360 kbps, nearly 3× over InFrame++. In addition, when producing equivalent throughputs from about 120 kbps to 540 kbps, CHROMACODE consistently outperforms InFrame++ by achieving significantly higher invisibility scores and lower BERs. The throughput gain over InFrame++ is mainly because that CHROMACODE embeds 1 bit using 1 cell, while InFrame++ uses multiple cells. The BER gain is obtained from CHROMACODE’s concatenated error correction coding and interleaving techniques. In a nutshell, CHROMACODE outperforms both InFrame++ and TextureCode with remarkably better flicker invisibility, higher throughputs and lower BERs.

We would like to point out that our evaluation results seem different from what was reported by TextureCode [6], which claims to reach equivalent or higher goodputs than InFrame++. This is because TextureCode uses a data frame rate of 60 fps for evaluation, while InFrame++ uses only 15 fps. In other words, in TextureCode one data frame is repeated within 2 video frames, while in InFrame++ it is repeated over 8 frames. In our comparison, we use 60 fps data frame rate for all.

# 7 RELATED WORKS

Color Space. Many color spaces have been defined and used in computer systems such as CIE1931 RGB and CIE1931 XYZ space [38]. These color spaces, however, are not perceptually uniform [39]. To overcome this, CIE later introduced uniform color spaces, e.g., CIE 1976 L∗a∗b∗ and CIE 1976 L∗u∗v∗ [10], [40]. However, the uniform color space is still not perfectly perceptual uniform. Decades of efforts are made by CIE to improve color difference calculation, from CIE76 to CMC(1:c) [41] to CIE94 [42] and finally CIE presented and recommended CIEDE2000, the most accurate color difference formula currently available [43], which is the exact formula used in CHROMACODE.

VLC over Screen-Camera Links. VLC grows as an increasingly hot topic [44], [45], [46]. Originated from one dimensional barcode, imagery codes like QR code [8] have been widely used for screen-camera communication nowadays. Recently, dynamic code becomes popular, which renders a sequence of images for streaming. PixNet [47] is the first-of-its-kind system that enables data streaming between LCD screens and cameras. COBRA [48] designs a novel colorful code for phone-to-phone communication. LightSync [49] enhances the coding scheme of COBRA and achieves higher rate. RDCode [22] contributes a robust dynamic code design with multi-level error correction schemes. Rain-Bar+ [50] designs an robust online high-goodput VLC system, which has realtime feedback. ARTcode [51] aims to produce visual codes that encode data in the form of human-readable images. These works focus on efficient transmission over dedicated screen-camera links. On the contrary, CHROMACODE aims at invisible communication with screen-camera link as a side channel.

Hidden Screen-Camera Communication. Hidden communication conveys information via a side visual [4] or acoustic [52], [53] channel. InFrame [12] and its extended version InFrame++ [4] pioneer the research area of unobtrusive screen-camera communication. They are the first to propose complementary frames to leverage flicker fusion property of HVS. However, as argued by a later work TextureCode [6], flicker still remains noticeable in InFrame++. TextureCode [6] improves invisibility by adaptive embedding based on video texture, but it only embeds data in textured regions and discards the others, which leads to degraded throughputs and changing uncertain code locations. Instead of lightness, HiLight [5] changes real-time accessible transparency in RGB color space and enables any-scene communication. Yet HiLight transmits bits by translucency changes at different frequencies, which largely limits its achievable throughputs. ImplicitCode [7] combines InFrame and HiLight to achieve better balance between invisibility and throughputs, which is, however, applicable to only grayscale carrier videos. Uber-in-Light [54] encodes data as complementary intensity changes over RGB channels and enables hidden communication for any screen and camera. Differently, CHROMACODE excels in its adaptive embedding in uniform color space, which is beyond the consideration of all existing works, robust coding scheme, and comprehensive system implementations.

# 8 CONCLUSION

We present CHROMACODE, a system that achieves all three goals on unobtrusive, high-rate, reliable screen-camera communication. We consider for the first time perceptually uniform color space and design a novel adaptive embedding scheme that accounts for both pixel lightness and texture. To achieve reliability, we employ concatenated error correction code together with a set of techniques overcoming multiple screen-camera channel distortions. We prototype CHROMA-CODE and evaluated it by experiments. The results demonstrate its superior performance over previous schemes in terms of invisibility, throughput and BER. CHROMACODE is a promising step in a line of work towards the emerging simultaneous viewing and communication paradigm. It is on the way of changing video advertising industry by the new paradigm of advertisement placement for online video, TV, movie, outdoor electronic billboard, etc. Not only that, we anticipate even more imaginary spaces for novel applications.

# ACKNOWLEDGMENTS

We sincerely thank the anonymous shepherd and reviewers for their helpful comments and advices. We appreciate all 20 participants in our user study. This work is supported in part by the National Key Research Plan under grant No. 2016YFC0700100, NSFC under grant 61522110, 61332004, 61672319 and 61632008.

# REFERENCES

[1] Cisco, “Cisco visual networking index: Forecast and methodology, 2016-2021,” 2017. [Online]. Available: https://www.cisco.com/c/ en/us/solutions/collateral/service-provider/visual-networkingindex-vni/complete-white-paper-c11-481360.pdf   
[2] I. M. Lab. (2017) Media trial report: Magna and ipg media lab turbocharge skippable pre-roll campaign.   
[3] The interactive effect: A key to surviving in the attention economy of a mobile-first world. [Online]. Available: https://medium. com/ipg-media-lab/the-interactive-effect-a-key-to-surviving-inthe-attention-economy-of-a-mobile-first-world-dcd8ace76ab1   
[4] A. Wang, Z. Li, C. Peng, G. Shen, G. Fang, and B. Zeng, “Inframe++: Achieve simultaneous screen-human viewing and hidden screen-camera communication,” in Proceedings of the 13th Annual International Conference on Mobile Systems, Applications, and Services, ser. MobiSys ’15. New York, NY, USA: ACM, 2015, pp. 181–195. [Online]. Available: http://doi.acm.org/10.1145/ 2742647.2742652   
[5] T. Li, C. An, X. Xiao, A. T. Campbell, and X. Zhou, “Real-time screen-camera communication behind any scene,” in Proceedings of the 13th Annual International Conference on Mobile Systems, Applications, and Services, ser. MobiSys ’15. New York, NY, USA: ACM, 2015, pp. 197–211. [Online]. Available: http://doi.acm.org/10.1145/2742647.2742667   
[6] V. Nguyen, Y. Tang, A. Ashok, M. Gruteser, K. Dana, W. Hu, E. Wengrowski, and N. Mandayam, “High-rate flicker-free screencamera communication with spatially adaptive embedding,” in The 35th Annual IEEE International Conference on Computer Communications, ser. INFOCOM ’16, 2016, pp. 1–9.   
[7] S. Shi, L. Chen, W. Hu, and M. Gruteser, “Reading between lines: High-rate, non-intrusive visual codes within regular videos via implicitcode,” in Proceedings of the 2015 ACM International Joint Conference on Pervasive and Ubiquitous Computing, ser. UbiComp ’15. New York, NY, USA: ACM, 2015, pp. 157–168. [Online]. Available: http://doi.acm.org/10.1145/2750858.2805824   
[8] Information technology - Automatic identification and data capture techniques - QR Code 2005 bar code symbology specification, IEC ISO 18 004, 2016.   
[9] G. S. Brindley, J. J. Du Croz, and W. A. H. Rushton, “The flicker fusion frequency of the blue-sensitive mechanism of colour vision,” The Journal of Physiology, vol. 183, no. 2, pp. 497–500, 1966. [Online]. Available: http://dx.doi.org/10.1113/ jphysiol.1966.sp007879   
[10] Colorimetry – Part 4: CIE 1976 L∗a∗b∗ Colour space, CIE ISO 11 664- 4, 2008.   
[11] Colorimetry – Part 6: CIEDE2000 Colour-Difference Formula, CIE ISO 11 664-6, 2013.   
[12] A. Wang, C. Peng, O. Zhang, G. Shen, and B. Zeng, “Inframe: Multiflexing full-frame visible communication channel for humans and devices,” in Proceedings of the 13th ACM Workshop on Hot Topics in Networks, ser. HotNets ’14. New York, NY, USA: ACM, 2014, pp. 23:1–23:7. [Online]. Available: http://doi.acm.org/10.1145/2670518.2673867

[13] A. Hanbury, “Constructing cylindrical coordinate colour spaces,” Pattern Recognition Letters, vol. 29, no. 4, pp. 494 – 500, 2008. [Online]. Available: http://www.sciencedirect.com/ science/article/pii/S0167865507003601   
[14] G. H. Joblove and D. Greenberg, “Color spaces for computer graphics,” in Proceedings of the 5th Annual Conference on Computer Graphics and Interactive Techniques, ser. SIGGRAPH ’78. New York, NY, USA: ACM, 1978, pp. 20–25. [Online]. Available: http://doi.acm.org/10.1145/800248.807362   
[15] A. Roorda and D. R. Williams, “The arrangement of the three cone classes in the living human eye,” Nature, pp. 520–522, 1999.   
[16] R. G. Kuehni, Historical Development of Color Space and Color Difference Formulas. John Wiley & Sons, Inc., 2003, pp. 204–270. [Online]. Available: http://dx.doi.org/10.1002/0471432261.ch6   
[17] D. J. Fleet and D. J. Heeger, “Embedding invisible information in color images,” in Proceedings of International Conference on Image Processing, ser. ICIP ’97, vol. 1, 1997, pp. 532–535 vol.1.   
[18] H. X. Liu, B. Wu, Y. Liu, M. Huang, and Y. F. Xu, “A discussion on printing color difference tolerance by ciede2000 color difference formula,” in Advances in Printing and Packaging Technologies, ser. Applied Mechanics and Materials, vol. 262. Trans Tech Publications, 2 2013, pp. 96–99.   
[19] C. Chubb, G. Sperling, and J. A. Solomon, “Texture interactions determine perceived contrast,” in Proceedings of the National Academy of Sciences of the United States of America, ser. PNAS ’89, 1989, pp. 9631–9635.   
[20] G. Stockman and L. G. Shapiro, Computer Vision, 1st ed. Upper Saddle River, NJ, USA: Prentice Hall PTR, 2001.   
[21] R. M. Haralick, K. Shanmugam, and I. Dinstein, “Textural features for image classification,” IEEE Transactions on Systems, Man, and Cybernetics, vol. SMC-3, no. 6, pp. 610–621, 1973.   
[22] A. Wang, S. Ma, C. Hu, J. Huai, C. Peng, and G. Shen, “Enhancing reliability to boost the throughput over screen-camera links,” in Proceedings of the 20th Annual International Conference on Mobile Computing and Networking, ser. MobiCom ’14. New York, NY, USA: ACM, 2014, pp. 41–52. [Online]. Available: http://doi.acm.org/10.1145/2639108.2639135   
[23] A. Ghosh, D. R. Wolter, J. G. Andrews, and R. Chen, “Broadband wireless access with wimax/802.16: current performance benchmarks and future potential,” IEEE Communications Magazine, vol. 43, pp. 129–136, 2005.   
[24] M. Meingast, C. Geyer, and S. Sastry, “Geometric models of rolling-shutter cameras,” CoRR, vol. abs/cs/0503076, 2005. [Online]. Available: http://arxiv.org/abs/cs/0503076   
[25] Zootopia — disney movies. [Online]. Available: http://movies. disney.com/zootopia   
[26] Xiph.org :: Derf’s test media collection. [Online]. Available: https://media.xiph.org/video/derf/   
[27] A. J. VITERBI, Error Bounds for Convolutional Codes and an Asymptotically Optimum Decoding Algorithm. Co-Published with Indian Institute of Science (IISc), Bangalore, India, 2011, pp. 41–50. [Online]. Available: http://www.worldscientific.com/doi/ abs/10.1142/9789814287517 0004   
[28] Ffmpeg. [Online]. Available: https://ffmpeg.org/   
[29] Mediacodec — android developers. [Online]. Available: https:// developer.android.com/reference/android/media/MediaCodec   
[30] Qt — cross-platform software development for embedded & desktop. [Online]. Available: https://www.qt.io/   
[31] Opencv library. [Online]. Available: https://opencv.org/   
[32] Encode/h.264-ffmpeg. [Online]. Available: https://trac.ffmpeg. org/wiki/Encode/H.264   
[33] J. Canny, “A computational approach to edge detection,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. PAMI-8, no. 6, pp. 679–698, 1986.   
[34] P. V. C. Hough, “Machine Analysis of Bubble Chamber Pictures,” Conf. Proc., vol. C590914, pp. 554–558, 1959.   
[35] H. Coxeter, Introduction to geometry, ser. Wiley classics library. Wiley, 1969. [Online]. Available: https://books.google.com/ books?id=c0ld-crynsIC   
[36] Moire´ pattern. [Online]. Available: https://en.wikipedia.org/ wiki/Moir\ pattern   
[37] Z. Wei, J. Wang, H. Nichol, S. Wiebe, and D. Chapman, “A median-gaussian filtering framework for moire pattern noise ´ removal from x-ray microscopy image,” Micron, vol. 43, no. 2, pp. 170 – 176, 2012. [Online]. Available: http://www.sciencedirect. com/science/article/pii/S0968432811001181

[38] H. S. Fairman, M. H. Brill, and H. Hemmendinger, “How the cie 1931 color-matching functions were derived from wright-guild data,” Color Research & Application, vol. 22, no. 1, pp. 11–23, 1997. [Online]. Available: http://dx.doi.org/10.1002/(SICI)1520- 6378(199702)22:1h11::AID-COL4i3.0.CO;2-7   
[39] D. L. MacAdam, “Visual sensitivities to color differences in daylight∗,” J. Opt. Soc. Am., vol. 32, no. 5, pp. 247– 274, 1942. [Online]. Available: http://www.osapublishing.org/ abstract.cfm?URI=josa-32-5-247   
[40] Colorimetry – Part 5: CIE 1976 L∗u∗v∗ Colour space and u’, v’ uniform chromaticity scale diagram, CIE ISO 11 664-5, 2009.   
[41] M. R. Luo and B. Rigg, “Uniform colour space based on the cmc(l:c) colour-difference formula,” Journal of the Society of Dyers and Colourists, vol. 102, no. 5-6, pp. 164–171, 1986. [Online]. Available: http://dx.doi.org/10.1111/j.1478-4408.1986.tb01069.x   
[42] R. McDonald and K. J. Smith, “Cie94-a new colour-difference formula\*,” Journal of the Society of Dyers and Colourists, vol. 111, no. 12, pp. 376–379, 1995. [Online]. Available: http://dx.doi.org/10.1111/j.1478-4408.1995.tb01688.x   
[43] “Publications briefly mentioned: Cie 142-2001, improvement to industrial colour-difference evaluation,” Color Research & Application, vol. 27, no. 1, pp. 61–61, 2002. [Online]. Available: http://dx.doi.org/10.1002/col.10020   
[44] J. Zhang, C. Zhang, X. Zhang, and S. Banerjee, “Towards a visible light network architecture for continuous communication and localization,” in Proceedings of the 3rd Workshop on Visible Light Communication Systems, ser. VLCS ’16. New York, NY, USA: ACM, 2016, pp. 49–54. [Online]. Available: http://doi.acm.org/10.1145/2981548.2981556   
[45] S. Naribole, S. Chen, E. Heng, and E. Knightly, “Lira: A wlan architecture for visible light communication with a wi-fi uplink,” in 2017 14th Annual IEEE International Conference on Sensing, Communication, and Networking, ser. SECON ’17, June 2017, pp. 1–9.   
[46] Z. Tian, K. Wright, and X. Zhou, “The darklight rises: Visible light communication in the dark,” in Proceedings of the 22Nd Annual International Conference on Mobile Computing and Networking, ser. MobiCom ’16. New York, NY, USA: ACM, 2016, pp. 2–15. [Online]. Available: http://doi.acm.org/10.1145/2973750.2973772   
[47] S. D. Perli, N. Ahmed, and D. Katabi, “Pixnet: Lcd-camera pairs as communication links,” in Proceedings of the Annual Conference on Applications, Technologies, Architectures, and Protocols for Computer Communications, ser. SIGCOMM ’10. New York, NY, USA: ACM, 2010, pp. 451–452. [Online]. Available: http://doi.acm.org/10.1145/1851182.1851258   
[48] T. Hao, R. Zhou, and G. Xing, “Cobra: Color barcode streaming for smartphone systems,” in Proceedings of the 10th International Conference on Mobile Systems, Applications, and Services, ser. MobiSys ’12. New York, NY, USA: ACM, 2012, pp. 85–98. [Online]. Available: http://doi.acm.org/10.1145/2307636.2307645   
[49] W. Hu, H. Gu, and Q. Pu, “Lightsync: Unsynchronized visual communication over screen-camera links,” in Proceedings of the 19th Annual International Conference on Mobile Computing and Networking, ser. MobiCom ’13. New York, NY, USA: ACM, 2013, pp. 15–26. [Online]. Available: http://doi.acm.org/10.1145/ 2500423.2500437   
[50] M. Zhou, Q. Wang, T. Lei, Z. Wang, and K. Ren, “Enabling online robust barcode-based visible light communication with realtime feedback,” IEEE Transactions on Wireless Communications, vol. 17, no. 12, pp. 8063–8076, Dec 2018.   
[51] Z. Yang, Y. Bao, C. Luo, X. Zhao, S. Zhu, C. Peng, Y. Liu, and X. Wang, “Artcode: Preserve art and code in any image,” in Proceedings of the 2016 ACM International Joint Conference on Pervasive and Ubiquitous Computing, ser. UbiComp ’16. New York, NY, USA: ACM, 2016, pp. 904–915. [Online]. Available: http://doi.acm.org/10.1145/2971648.2971733   
[52] Q. Wang, K. Ren, M. Zhou, T. Lei, D. Koutsonikolas, and L. Su, “Messages behind the sound: Real-time hidden acoustic signal capture with smartphones,” in Proceedings of the 22Nd Annual International Conference on Mobile Computing and Networking, ser. MobiCom ’16. New York, NY, USA: ACM, 2016, pp. 29–41. [Online]. Available: http://doi.acm.org/10.1145/2973750.2973765   
[53] M. Zhou, Q. Wang, K. Ren, D. Koutsonikolas, L. Su, and Y. Chen, “Dolphin: Real-time hidden acoustic signal capture with smartphones,” IEEE Transactions on Mobile Computing, vol. 18, no. 3, pp. 560–573, March 2019.   
[54] M. Izz, Z. Li, H. Liu, Y. Chen, and F. Li, “Uber-in-light: Unobtrusive visible light communication leveraging complementary

color channel,” in The 35th Annual IEEE International Conference on Computer Communications, ser. INFOCOM ’16, April 2016, pp. 1–9.

![](images/2fe3a8240b8f90d95f48713cbbbb199c07e21837a3df170fafa1a115e8dbeb5c.jpg)



Kai Zhang received the BE degree from the School of Software, Tsinghua University, in 2016. He is currently working toward the MS degree in software engineering in the School of Software, Tsinghua University. He is a member of the Tsinghua National Lab for Information Science and Technology. His research interests include visible light communication and blockchain.

![](images/d9725a340adb34a5fe2b1e304c70d9bdf37ea9455037dd64b96a30fb3b82edb2.jpg)



Yi Zhao received the BE degree from the School of Software, Tsinghua University, in 2017. He is now a PhD student in the School of Software, Tsinghua University. He is a member of the Tsinghua National Lab for Information Science and Technology. His research interests include Internet of Things, mobile computing and urban computing. He is a student member of the IEEE.

![](images/7075f9d4e1971f7a5d8fd0b72739d8c879da9d63f81ad88d70aa2e18c82539c1.jpg)



Chenshu Wu received the BE degree from the School of Software, and the PhD degree in computer science, both from the Tsinghua University, in 2010 and 2015, respectively. He is currently in the Department of Electrical and Computer Engineering, University of Maryland, College Park. His research interests include wireless networks and mobile computing. He is a member of the IEEE and ACM.

![](images/88c4780a18bbc19ddaf299fad4580679ea94829c8dd0fedbc4c2eb6d81f6aed7.jpg)



Chaofan Yang received the BE degree and the MS degree, both from the School of Software, Tsinghua University, in 2014 and 2017, respectively. He is currently working in Microsoft as a software engineer. His research interests include wireless sensing and wireless video transmission.

![](images/ca309e7fcbf14064a9531a35e31c5438571633edf4bbb715331b0cc8f002016b.jpg)



Kehong Huang received the BE degree from the School of Software, Tsinghua University, in 2018. He is currently working toward the Master degree in the School of Software, Tsinghua University. He is a member of the Tsinghua National Lab for Information Science and Technology. His research interests include AI and mobile computing. He is a student member of the ACM.

![](images/33dd0ad0d0bec0d83b0f4c9c7165f623d0101de8b8b72e37e2f23eee496f6e25.jpg)



Chunyi Peng received the PhD degree in Computer Science from the University of California, Los Angeles in 2013. She now works as an Assistant Professor in the Department of Computer Science at Purdue University. Her research interests focus on mobile networks, mobile sensing systems, wireless networking, and network security. She is a senior member of the IEEE.

![](images/c98c7f6a1c1db3b81d2e5dbc35214d13325eac8e545356fc63b64377e61839d2.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, the MS and PhD degrees in computer science and engineering from Michigan State University, in 1995, 2003, and 2004, respectively. He is now MSU Foundation Professor and Chairperson of Department of Computer Science and Engineering, Michigan State University, and holds Chang Jiang Chair Professorship at Tsinghua University. His research interests include wireless sensor network, peer-to-peer computing, and perva-

sive computing. He is a fellow of the IEEE.

![](images/d5ee07a470be93a12c5144eb3ca4976cbd60f75105a5a3cab2332449b95b2e3e.jpg)



Zheng Yang received the BE degree in computer science from the Tsinghua University, and the PhD degree in computer science from the Hong Kong University of Science and Technology, in 2006 and 2010, respectively. He is currently an Associate Professor with the Tsinghua University. His main research interests include wireless ad-hoc/sensor networks and mobile computing. He is a senior member of the IEEE.