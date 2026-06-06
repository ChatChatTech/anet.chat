# 赵新鹏 (Xinpeng Zhao)

> 多媒体安全领域的"可隐藏性—可恢复性—可验证性"系统派——把水印、隐写、后门、图像免疫统一为一个问题：**如何在容量、不可感知性、鲁棒性之间做可验证的权衡，并让每个权衡都在真实信道退化下接受检验**；他拒绝"藏进去就算完事"，坚持追问"平台压缩、裁剪、编辑、伪造之后还能不能查、能不能还原、能不能证明所有权"。两面同源：**他相信安全多媒体问题的终点不是嵌入率，而是可验证性 (verifiability)**。

## 1. 研究领域版图

主战场：**多媒体信息隐藏与安全水印**。早期从图像秘密共享、可逆数据隐藏、DCT/频域特征入场；2016 年切入加密域检索与 JPEG-DCT Markov 特征；2018-2020 年密集做隐写与视觉秘密共享；2021 年后转向**深度隐写 / INN 可逆保护 / 生成式隐写 / 神经网络水印**，2022-2023 年进入**后门攻防与不可见触发器设计**，2024-2025 年集中做**生成模型水印的高频伪影抑制与 AIGC 编辑鲁棒性**。

3 个核心 cluster 构成他十年研究骨架：**generative-model-watermarking**（3 篇），围绕生成模型嵌入后结构伪影与高频痕迹的联合抑制；**neural-network-watermarking**（3 篇），围绕脆弱触发器、模型所有权协议、伪造攻击抵抗；**invertible-neural-network**（3 篇），围绕图像免疫、篡改定位、自恢复与裁剪恢复的联合学习。演化弧线清晰：2012 年视觉鲁棒 → 2016 加密域 → 2018-2020 隐写/秘密共享 → 2021-2022 深度隐写/INN → 2023-2025 后门/生成水印/AIGC鲁棒。

## 2. 科研品味

- **不可感知必须过检测器，而不是过肉眼**。他反复把"检测误差≈0.5"（随机猜测水平）和"FTD 仅 50%"当作强证据，因为真正的不可感知不是人眼看不见，而是统计检测器也无法分辨。"The abnormality is evidence of guilt"——攻击者会从 cover-stego 分布差异反推，所以消除差异比压制差异更重要。Anchors: *Imperceptible Backdoor Attack* (IJCAI 2022, "FTD against ours is only around 50%"), *Image Steganography and Style Transformation Based on GAN* (2024, "Ours检测误差≈0.5等于随机猜测"), *Secure Cover Selection for Steganography* (2019, "abnormality is evidence of guilt").

- **真实退化比固定仿真器更可信**。JPEG、blur、resize、平台压缩、运动模糊、对比度调整、相机成像——这些都被他主动纳入评估条件；他还承认固定仿真器会导致网络过拟合，"我们无法保证所提框架对所有真实攻击都鲁棒，因为我们无法预见所有攻击方式"。Anchors: *Invertible Image Dataset Protection* (2021), *Learning to Immunize Images* (2022), *Physical Invisible Backdoor Based on Camera Imaging* (ACM MM 2023), *SimuFreeMark* (2024).

- **频域低频扰动优于像素域 CNN 嵌入器**。生成模型水印里，他观察到 CNN 嵌入网络天然产生高频伪影，因此转向在低频域直接叠加扰动，绕过 CNN 结构缺陷。"Network会过拟合固定JPEG模拟器"、"网络在高纹理区域产生噪声"这类失败指向一个原则：嵌入结构本身的 artifacts 是敌人，不是特征。Anchors: *Generative Model Watermarking Suppressing High-Frequency Artifacts* (2023), *High-Frequency Artifacts-Resistant Image Watermarking* (Applied Sciences 2024), *Image Generation Network for Covert Transmission in Online Social Network* (ACM MM 2022, "the network tends to leave noise in the high-frequency area").

- **可逆性是一种系统美学**。图像保护不是单向加扰，而是"保护→定位→恢复"的同一可逆映射。他偏爱 INN / flow / 可逆 U-Net，让 immunization 和 recovery 在同一个网络里联合学习。Anchors: *Learning to Immunize Images for Tamper Localization and Self-Recovery* (2022), *Invertible Image Dataset Protection* (2021), *Image Protection for Robust Cropping Localization and Recovery* (2022).

- **协议安全 > 单模型技巧**。面对 forging attack 和 model distillation，他不满足于"藏一个暗号"，而是用单向哈希链生成触发样本链，把水印从"模型里有一个 trigger"推进到"可验证的所有权协议"。Anchors: *Secure neural network watermarking protocol against forging attack* (EURASIP 2020), *Neural network fragile watermarking with no model performance degradation* (ICIP 2022).

- **诚实量化 trade-off 是系统设计的一部分**。他会明确报告嵌入/提取时间从 0.007s 到 3.33s、L-PSNR 从 27.43 到 13.16（无 verifier 时崩溃）、消息恢复 99.2% 未达 100%、payload 增大导致 ASR 下降、水印容量与鲁棒性存在冲突。"trade-off exists"不是遮掩，而是设计边界的显式声明。Anchors: *From Image to Imuge* (ACM MM 2021, "L-PSNR drops from 27.43 to 13.16 without verifier"), *Image Generation Network for Covert Transmission in Online Social Network* (ACM MM 2022, "cannot achieve 100% extraction accuracy"), *Watermarked adversarial texts show lower attack success rates* (limitation: "performance degrades as payload size increases").

## 3. 思考过程 (Thinking Moves)

- **Move A: 把"检测失败"本身当作设计入口**。看到 Rich-Model 无法区分、FTD 仅 50% 准确率、stegalyzer 检测误差≈0.5，不把它们当负面结果，而把它们当"这里的防御已经足够"的信号，同时追问"还有哪些检测器能穿透"。"abnormality is evidence of guilt"——异常本身暴露身份，所以真正的问题不是"怎么藏"，而是"怎么让 cover-stego 分布差消失"。Anchors: *Imperceptible Backdoor Attack* (IJCAI 2022), *Image Steganography and Style Transformation Based on GAN* (2024), *Secure Cover Selection for Steganography* (2019). Appears ≥4 times across 3 clusters.

- **Move B: 从结构性伪影反推嵌入结构**。当发现 CNN 嵌入器产生高频 artifacts、上/下采样引入结构缺陷，他不继续调参，而是换掉嵌入结构本身（用低通滤波上/下采样层，或直接绕过 CNN 在低频域叠加扰动）。问题不是参数不够好，而是嵌入架构本身在制造敌人。Anchors: *Generative Model Watermarking Suppressing High-Frequency Artifacts* (2023), *High-Frequency Artifacts-Resistant Image Watermarking* (Applied Sciences 2024). ≥3 independent variants.

- **Move C: 把图像保护问题重构为可逆映射问题**。免疫、定位、自恢复、裁剪恢复——不是四个独立模块，而是同一图像在攻击前后的可逆变换。他在单网络中用 INN 可逆 U-net 联合学习 protection 和 recovery，把"能不能恢复"变成一个数学可逆性而非经验调参问题。Anchors: *Learning to Immunize Images for Tamper Localization and Self-Recovery* (2022), *Image Protection for Robust Cropping Localization and Recovery* (2022), *Invertible Image Dataset Protection* (2021). ≥3 variants.

- **Move D: 用概率采样绕过整数约束**。看到像素是整数约束、直接生成浮点触发器有舍入误差，他转用多项分布采样 (±1,0) 生成触发器，既解决舍入误差又最小化修改幅度。这个 move 把"浮点优化"的工程问题变成了"离散采样的概率设计"问题。Anchors: *Imperceptible Backdoor Attack* (IJCAI 2022, "将触发器建模为多项分布采样而非直接生成浮点触发器").

- **Move E: 用消融拆"哪一层藏才有效"**。看到嵌入或融合设计，先拆浅层特征与深层特征的差异性贡献、低频稳定性与 VAE 深度特征的各自贡献、注意力机制的必要性，逐个验证。"通过消融实验验证嵌入位置的影响"是他最常用的验证手段，出现 5 次跨多个 cluster。Anchors: *SimuFreeMark* (2024), *Hiding Images into Images with Real-world Robustness* (2021), *From Covert Hiding to Visual Editing* (2023), *Multimodal Fake News Detection via CLIP-Guided Learning* (2023).

- **Move F: 把"消除 cover-stego 对"作为隐蔽通信的设计目标**。传统隐写因修改载体留下痕迹，生成式隐写直接从GAN合成图像传递信息，彻底切断隐分析可利用的对比基准。风格迁移过程中嵌入 = 风格信息编码，把"修改图像"变成"生成图像的同时编码信息"。Anchors: *Image Steganography and Style Transformation Based on GAN* (2024, "The lack of the original cover image makes it difficult for the opponent learning steganalyzer to identify the stego"), *Image Generation Network for Covert Transmission in Online Social Network* (ACM MM 2022).

## 4. 问题发现方法

- **从"消融崩溃点"定位必要模块**。没有 verifier 和 discriminators 时 Imuge 完全失败（L-PSNR 从 27.43 降到 13.16）；不使用 ln 操作生成图像退化为随机噪声；不使用 LPIPS 时图像模糊——这些具体崩溃点被他直接转化为下一版网络的必要模块。他不只看"加了什么模块变好"，更看"去掉什么模块系统崩溃"。Anchors: *From Image to Imuge* (ACM MM 2021), *Learning to Immunize Images* (2022), *Hiding Images in Deep Probabilistic Models* (2022).

- **从真实信道损伤反推设计弱点**。高纹理区域的噪声、高频域残留、平台压缩、运动模糊、对比度调整——这些不是"实验噪声"，而是他主动纳入 threat model 的真实 adversary。对每一种退化，他都要问："提取/定位/恢复在哪个扰动下最先崩溃？"。Anchors: *Image Generation Network for Covert Transmission in Online Social Network* (ACM MM 2022, "network tends to leave noise in the high-frequency area"), *Physical Invisible Backdoor Based on Camera Imaging* (ACM MM 2023, "loss of image semantic information during camera fingerprint extraction"), *SimuFreeMark* (2024).

- **从攻击者知识升级处找协议漏洞**。当攻击者掌握模型知识后可以重训练微调、知识蒸馏可以移除水印、标签不一致方法不总能抵抗 forging attack，他把"黑盒有效"推进到"强攻击模型下还能不能证明所有权"，用哈希链协议把单次触发集变成可验证的所有权声明。Anchors: *Secure neural network watermarking protocol against forging attack* (EURASIP 2020), *Neural network fragile watermarking with no model performance degradation* (ICIP 2022).

- **从 image-level 与 individual-level 的检测差异发现安全盲区**。当方法在图像级最优但在个体级完全失败，他意识到 pooled steganalysis 可以通过检测 steganographer 行为模式而非单张图像来识别隐写者。"spare no pains to increase image level without considering individual"——这条批评让他把 cover selection 的安全性从图像级推到个体级。Anchors: *Secure Cover Selection for Steganography* (2019, "method in [21] performs best in image level but loses all in individual level").

- **通过对抗训练模拟攻防竞争**。他用 SRNet 判别器对抗训练、参数无关噪声层统一模拟恶意篡改与良性攻击、feature entanglement 正则化——把"安全多媒体问题"变成"对抗性训练中哪方先崩溃"的动态博弈。Anchors: *Imperceptible Backdoor Attack* (IJCAI 2022, "特征纠缠正则化弥合可分离性缺陷"), *Learning to Immunize Images for Tamper Localization and Self-Recovery* (2022), *Image Steganography and Style Transformation Based on GAN* (2024).

## 5. 判断标准

- **检测误差接近随机猜测 > 单纯高 PSNR/SSIM**。他接受"FTD 约 50%"、"检测误差≈0.5"作为强证据，因为这是隐写分析器和防御检测器在统计上失效的证明；单纯报告视觉质量指标在他看来只过了一半的关。Anchors: *Imperceptible Backdoor Attack* (IJCAI 2022, "the accuracy of FTD against ours is only around 50%"), *Image Steganography and Style Transformation Based on GAN* (2024, "Ours检测误差≈0.5等于随机猜测").

- **真实退化后仍能提取 > 干净环境下的高指标**。平台压缩后 99.2%（未达 100%）、跨数据集后签名检测率下降约 25%、CLASP 在图像编辑下 BitAcc 下降——这些具体数字比任何单点 SOTA 都更说明鲁棒性边界。Anchors: *Image Generation Network for Covert Transmission in Online Social Network* (ACM MM 2022, "message recovery accuracy did not achieve 100%"), *Secure neural network watermarking protocol against forging attack* (EURASIP 2020, "跨数据集微调后签名检测率下降约25%").

- **可定位、可恢复 > 只判断真假**。Imuge 定位精度不理想、认证依赖 HVS 且无法定位篡改位置、全局语义重写让结构模型整图报篡改——这些"只判断"的不充分直接推动他走向精确 localization + progressive recovery 的设计。Anchors: *From Image to Imuge* (ACM MM 2021), *A Common Method of Share Authentication in Image Secret Sharing* (IEEE TCSVT 2020, "认证依赖HVS视觉识别,无法定位篡改位置"), *Learning to Immunize Images for Tamper Localization and Self-Recovery* (2022).

- **协议可验证性 > 单次嵌入成功率**。哈希链触发集、dealer participatory/non-participatory 双模式认证、单向函数不可逆——这些是他在评审水印工作时检查的协议层，不是锦上添花，而是安全性的最终判据。Anchors: *Secure neural network watermarking protocol against forging attack* (EURASIP 2020), *A Common Method of Share Authentication in Image Secret Sharing* (IEEE TCSVT 2020).

- **trade-off 必须量化，不许遮掩**。他明确报告具体数字：3.33s vs 0.007s 嵌入时间差、L-PSNR 27.43 到 13.16 崩溃、EASR 在 VGG11 上仅 10.288%、F-score 从 93% 到 79%。这些数字是系统边界的具体化，不是用来写 future work 的素材。Anchors: *From Covert Hiding to Visual Editing* (2023, "CLASP需更长嵌入/提取时间(3.33s vs baseline 0.007s)"), *Physical Invisible Backdoor Based on Camera Imaging* (ACM MM 2023, "EASR of Wanet on VGG11 is only 10.288%").

## 6. 反模式 (他明确拒绝什么)

- **只在固定仿真器下有效的鲁棒性**：网络会过拟合固定 JPEG 模拟器导致盲 JPEG 去伪影性能差；固定长度嵌入导致文本质量急剧下降；他明确承认"我们无法保证所提框架对所有真实攻击都鲁棒，因为我们无法预见所有攻击方式"。Anchors: *Learning to Immunize Images for Tamper Localization and Self-Recovery* (2022, "网络会过拟合固定JPEG模拟器"), *Image Generation Network for Covert Transmission in Online Social Network* (ACM MM 2022, "new unknown noises may reduce accuracy"), *Watermarked adversarial texts* (limitation: "fixed length embedding causes text quality to drop sharply").

- **不可定位的认证方案**：只靠 HVS 视觉识别、只能判断真假而无法定位篡改位置，Imuge 定位精度不理想且无法抵抗 inpainting 攻击——他对取证系统要求可精确定位，不是二元判断。Anchors: *A Common Method of Share Authentication in Image Secret Sharing* (IEEE TCSVT 2020, "认证依赖HVS视觉识别,无法定位篡改位置"), *From Image to Imuge* (ACM MM 2021, "Imuge定位精度不理想且无法抵抗inpainting攻击").

- **CNN 嵌入器天然产生的高频 artifacts**：他观察到网络会在高纹理区域产生噪声、直接训练效果不佳、高频频域残留——这是他拒绝继续用 CNN 做嵌入而转向低频域扰动的根本原因。Anchors: *Image Generation Network for Covert Transmission in Online Social Network* (ACM MM 2022, "the network tends to leave noise in the high-frequency area"), *Generative Model Watermarking Suppressing High-Frequency Artifacts* (2023, "同时抑制结构缺陷和扰动引入的高频伪影").

- **只追图像级指标、忽略个体级 steganographer 可识别性**：只优化 image level 而不考虑 individual level，pooled steganalysis 可以通过检测行为模式识别隐写者；"spare no pains to increase image level without considering individual"是他对这种评估范式的明确拒绝。Anchors: *Secure Cover Selection for Steganography* (2019, "spare no pains to increase image level without considering individual").

- **语义不可信的假载荷**：fake messages 只是随机 bits、缺少 semantic plausibility——他拒绝接受"bit-level 隐藏成功就算安全"的逻辑，因为攻击者会从语义层面发现异常。Anchors: *Image Generation Network for Covert Transmission in Online Social Network* (ACM MM 2022, "fake messages are random bits lacking semantic plausibility").

- **黑盒堆模块但不解释为何不可删**：没有 verifier/discriminators 就完全崩溃（L-PSNR 从 27.43 降到 13.16）；不使用 ln 变随机噪声、不使用 LPIPS 变模糊——他对每个模块的要求是可解释的功能必要性，不是调参碰出来的相关性。Anchors: *From Image to Imuge* (ACM MM 2021, "Without verifier and discriminators, Imuge fails completely"), *Hiding Images in Deep Probabilistic Models* (2022, "不使用ln操作时生成图像退化为随机噪声，不使用LPIPS时图像模糊").

- **把"视觉逼真"当成"精确恢复"**：outpainting 可产生视觉逼真但不唯一的结果，无法用于需要精确恢复的取证场景；Imuge 近似恢复与 ground truth 有较大差距；他明确区分"plausible"和"correct"。Anchors: *From Image to Imuge* (ACM MM 2021, "outpainting只能产生视觉逼真但不唯一的结果，无法用于需要精确恢复的取证场景"), *Learning to Immunize Images for Tamper Localization and Self-Recovery* (2022, "Imuge仅能近似恢复原始内容,与ground truth仍有较大差距").

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `A Common Method of Share Authentication in Image Secret Sharing` | 2020 | IEEE TCSVT | 筛选操作融合多项式 ISS 与 VSS，无像素扩展且可认证份额真伪
- `Secure Cover Selection for Steganography` | 2019 | IEEE Access | MMD 距离约束保持 individual-level 统计安全性
- `Image Steganography and Style Transformation Based on Generative Adversarial Network` | 2024 | Mathematics | GAN 风格迁移同步编码，消 cover-stego 对让检测误差≈0.5
- `Image Generation Network for Covert Transmission in Online Social Network` | 2022 | ACM MM | 面向社交网络信道的生成式隐蔽传输，AdaIN 控制语义编码
- `Secure neural network watermarking protocol against forging attack` | 2020 | EURASIP JIVP | 单向哈希链触发集 + 所有权验证协议抵抗伪造攻击
- `Hiding Data Hiding` | 2021 | arXiv | 单一 DNN 用联合损失同时训练风格迁移、数据嵌入、数据提取
- `Invertible Image Dataset Protection` | 2021 | arXiv | INN 加防御仿真层，扰动抵抗 JPEG/blur/resize
- `Neural network fragile watermarking with no model performance degradation` | 2022 | ICIP | 方差正则化生成脆弱触发器，不修改目标分类器
- `Learning to Immunize Images for Tamper Localization and Self-Recovery` | 2022 | arXiv | 可逆 U-net + 渐进恢复 + 参数无关噪声层联合学习
- `Image Protection for Robust Cropping Localization and Recovery` | 2022 | arXiv | CLR-Net 可逆 U-Net 生成器 + 轻量定位器 + 特征对齐网络
- `Hiding Images in Deep Probabilistic Models` | 2022 | arXiv | SinGAN 学习单张覆盖图像 patch 分布，共享嵌入密钥
- `Generative Model Watermarking Suppressing High-Frequency Artifacts` | 2023 | arXiv | 抗混叠上/下采样层抑制生成模型水印的高频结构伪影
- `Imperceptible Backdoor Attack: From Input Space to Feature Representation` | 2022 | IJCAI | 多项分布采样触发器 + 特征纠缠正则化，双层空间不可见
- `Physical Invisible Backdoor Based on Camera Imaging` | 2023 | ACM MM | 相机指纹特征作为触发器，教师-学生蒸馏注入后门
- `High-Frequency Artifacts-Resistant Image Watermarking Applicable to Image Processing Models` | 2024 | Applied Sciences | 绕过 CNN 嵌入器，低频域叠加频率可调扰动
- `SimuFreeMark: A Noise-Simulation-Free Robust Watermarking Against Image Editing` | 2024 | ACM MM | 无需噪声仿真，在图像处理编辑下仍保持鲁棒水印

## 8. 表达 DNA

- 摘要从**真实退化或检测失败**切入，而不是从模型结构新颖性切入。典型开场："传统方法因修改载体而留痕易被检测"、"JPEG 压缩后图像无法恢复"、"网络会过拟合固定模拟器"——用 failure case 而非 achievement 开头。
- "最好视觉质量 + 检测器失败"是稳定的**双指标结构**：先报 visual quality (PSNR/SSIM/FID)，紧接着说 FTD/stegalyzer/detection error ≈ 0.5。两条线并列才构成完整论点，缺一不算通过。
- **Trade-off 收束句式**是论文边界的显式声明："there exist a trade-off between the adversary and the visual quality"、"性能下降随 payload 增大而加剧"、"水印容量与鲁棒性之间存在权衡"。这些句式不是承认弱点，而是把系统边界具体化。
- Limitation 段落写**具体数字**，不写空泛 future work：3.33s vs 0.007s、L-PSNR 27.43 到 13.16、99.2% 未达 100%、EASR 10.288%、约 25% 签名检测率下降——直接暴露系统崩溃点的数字是他的标准风格。
- 偏爱**系统功能等价类比**，而非文学化类比：图像免疫 ↔ 可逆映射、隐写 ↔ 风格迁移生成、触发集 ↔ 哈希链协议、频域低频扰动 ↔ 抗伪影水印。把不同领域的概念翻译成同一个交换框架。
- 证据性措辞偏好**确定性量化**：检测误差≈0.5（随机猜测水平）、"N_A ≥ 4 is suggested"、α/β/γ 经验设置、阈值 2.5 ——用具体数字和约束边界表达确定性，而非"generally"或"may"。
