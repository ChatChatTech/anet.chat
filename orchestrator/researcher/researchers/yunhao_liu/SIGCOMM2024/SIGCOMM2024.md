# #484 SCX: Stateless KV-Cache Encoding for Cloud-Scale Confidential Transformer Serving

![](images/803820021a7c48a7c79268e0829bfe634c0a5e7ec5871a80aac116667e95cccf.jpg)

![](images/ade91ae51239af1580e4d96cc5ce7c084df687d17bd555acea64af0c1c06875c.jpg)

Your submissions

(All)

Search

# √ Email notification

Select to receive email on updates to reviews and comments.

# ▼ PC conflicts

Guoliang Xing

# Shepherd

Kevin Hsieh

# Review #484A

Review #484B

Review #484C

Review #484D

Comments

# Accepted

![](images/4f7c9f68bd1511909032ca76b2f2fd623809f24a0438cc57633fff9efc79a4f2.jpg)

Final version (1.1MB) Ⓤ Jul 31, 2025, 2:05:17 AM PDT · ↙ a2994ba1

![](images/5c0309b4543a6ae63ffafded4007aff2f55e538b92db3e510ebcb2803dee172d.jpg)

Submission version

# ▼ Abstract

Transformer models have revolutionized fields like natural language processing and computer vision but face privacy concerns in sensitive applications such as medical diagnostics. Existing confidential serving methods, including cryptography-based, memory isolation-based, and access control-based, offer trade-offs between privacy and efficiency but often struggle with high latency or hardware dependencies. This work proposes stateless KV-cache encoding (SCX), a novel framework that encodes the intermediate key-value cache during Transformer inference using user-controlled keys. SCX ensures that the cloud can neither recover the input nor independently complete the next token prediction, effectively preserving privacy. By introducing efficient encoding and decoding schemes, SCX addresses communication complexity and attack vulnerabilities while ensuring zero loss of inference quality. Experiments on large Transformer models demonstrate that SCX achieves lower latency (e.g., 36ms for LLaMA-7B), outperforming state-of-the-art cryptography and memory isolation methods by orders of magnitude. Moreover, SCX can complementarily work with advanced KV-cache management techniques to further enhance KV-cache communication efficiency by 85%, marking a significant step toward practical, privacy-preserving large Transformer serving.

# ▼ Authors (anonymous)

Mu Yuan (The Chinese University of Hong Kong)
<ym0813@mail.ustc.edu.cn>

Lan Zhang (University of Science and Technology of China) <zhanglan@ustc.edu.cn>

Liekang Zeng (The Chinese University of Hong Kong)
<lkzeng@cuhk.edu.hk>

Siyang Jiang (The Chinese University of Hong Kong)
<syjiang@ie.cuhk.edu.hk>

Bufang Yang (The Chinese University of Hong Kong)
<bfyang@link.cuhk.edu.hk>

Di Duan (The Chinese University of Hong Kong)
<duandiacademic@gmail.com>

Guoliang Xing (The Chinese University of Hong Kong)
<glxing@ie.cuhk.edu.hk>

# ▶ Topics and options

▶ ACM keywords, ACM Computing Classification, and Source files