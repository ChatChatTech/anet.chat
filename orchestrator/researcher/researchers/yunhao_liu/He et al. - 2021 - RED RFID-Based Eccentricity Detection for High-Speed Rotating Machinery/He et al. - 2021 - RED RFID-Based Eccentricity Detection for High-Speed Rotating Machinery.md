Received November 20, 2015, accepted December 13, 2015, date of publication January 12, 2016, date of current version November 8, 2016.

Digital Object Identifier 10.1109/ACCESS.2016.2516949

# Fast Weighted Total Variation Regularization Algorithm for Blur Identification and Image Restoration

HAIYING LIU1,2, (Member, IEEE), JASON GU2,3, (Senior Member, IEEE), MAX Q.-H. MENG4, (Fellow, IEEE), AND WU-SHENG LU5, (Life Fellow, IEEE)

1School of Electrical Engineering and Automation, Qilu University of Technology, Jinan 250353, China

2Department of Electrical and Computer Engineering, Dalhousie University, Halifax, NS B3H 4R2, Canada

3School of Control Science and Engineering, Shandong University, Shandong 250061, China

4Department of Electronic Engineering, The Chinese University of Hong Kong, Hong Kong

5Department of Electrical and Computer Engineering, University of Victoria, Victoria, BC V8P 3W6, Canada

Corresponding author: J. Gu (jason.gu@dal.ca)

ABSTRACT Images obtained from unconstrained environments may be blurred by unknown kernels and affected due to noise. This paper presents a new total variation minimization-based method for blindly deblurring such images. Unlike the alternating optimization-based algorithms, the proposed algorithm adopts a joint estimation strategy to estimate the unknown blurring kernel and the unknown image in an iterative manner, where each iteration performs two separate image denoising subproblems that admit fast implementation. Experiments are performed on multiple synthetic, grayscale, and color images, and the results demonstrate that the proposed method is effective in blind deblurring.

INDEX TERMS Blind deconvolution, TV minimization, image denoising, image deblurring.

# I. INTRODUCTION

Classical image restoration algorithm is dedicated to estimating the true image assuming the knowledge of blur. Several methods solving these problems are available in the literature [1]–[9], including those based on total variation minimization which have been found especially effective. By contrast, blind deconvolution as an image restoration task tackles a much more challenging problem where both the image and the blurring mechanism are unknown. TVbased image restoration algorithms [10]–[33] have been examined in connection to this type of problem for the blind deconvolution. An approach that turns out to be particularly successful for blind deconvolution is proposed in [10] and improved in [11], [13], [15], [24], and [27] which is commonly known as the alternating optimization technique. The key idea of these aforementioned alternating optimization techniques is to fix one variable while optimize the other. Besides the relevant TVbased image restoration algorithms, there are many nonblind deconvolution algorithms. The algorithm based on Block Matching 3-D (BM3D) frames shows superiority with respect to the state of the art in the field [36]. Some researchers also developed an iterative graph-based framework for image restoration based on a new definition of the normalized graph Laplacian methods [34], [35] and their effectiveness for different restoration problems is proved.

The primary goal of this paper is to develop a new method for blind deconvolution of gray-scale as well as color images. Unlike the alternating-optimization based algorithm (which reduces the problem at hand to alternately performing two standard deblurring subproblems with known blurring kernels), the new method adopts a joint estimation strategy to synchronously estimate both the unknown kernel and unknown image. In this paper, we develop a new technique to optimize both unknowns together rather than fixing one and optimizing the other alternately. To deal with the technical challenges arising from this joint estimation approach, a new local framework was propose to carry out the joint estimation of the unknowns in an iterative manner. In this framework each iteration performs two separate image denoising subproblems which can be carried out efficiently using the techniques in [5] and [9]. Simulation results are presented to demonstrate that the proposed algorithm is capable of blindly deblurring images with considerably improved performance.

# II. BACKGROUND AND RELATED WORK

# A. IMAGE MODEL

We follow [2] to consider the basic image model

$$
\boldsymbol {A} \boldsymbol {u} + \boldsymbol {w} = \boldsymbol {u} _ {0} \tag {1}
$$

where A represents an affine map standing for a blurring operator, $\pmb { u } _ { 0 }$ denotes an observed noisy image of size $n _ { 1 } ~ \times ~ n _ { 2 }$ , and w is normally distributed additive noise. Assuming noise w is Gaussian white with independent and identically distributed components of zero mean and variance σ 2. The restoration problem here is to estimate (recover) image u and the blur operator A given the observation $\pmb { u } _ { 0 } .$ . We stress that because both the blurring operator A and image u are unknown, this is a blind deconvolution problem which makes model (1) nonlinear, thus technically this problem is more challenging than some deblurring problems encountered in reference papers [1]–[9].

# B. TV NORM OF GRAY-SCALE IMAGES

Let $\textbf { \textit { u } } \in  { R } ^ { n _ { 1 } \times n _ { 2 } }$ represent a digital gray-scale image. The isotropic total variation $( \| \pmb { u } \| _ { \mathrm { T V ^ { ( I ) } } } )$ of u is defined by

$$
\| \boldsymbol {u} \| _ {\mathrm{TV} ^ {(1)}} = \sum_ {i = 1} ^ {n _ {1}} \sum_ {j = 1} ^ {n _ {2}} \| \boldsymbol {D} _ {i, j} \boldsymbol {u} \| _ {2}, \quad \boldsymbol {D} _ {i, j} \boldsymbol {u} = \left[ \begin{array}{l} \boldsymbol {D} _ {i, j} ^ {(h)} \boldsymbol {u} \\ \boldsymbol {D} _ {i, j} ^ {(v)} \boldsymbol {u} \end{array} \right] \tag {2}
$$

where

$$
\boldsymbol {D} _ {i, j} ^ {(h)} \boldsymbol {u} = \left\{ \begin{array}{l l} u _ {i + 1, j} - u _ {i, j}, & i <   n _ {1}, \\ 0, & i = n _ {1} \end{array} \right.
$$

$$
\boldsymbol {D} _ {i, j} ^ {(v)} \boldsymbol {u} = \left\{ \begin{array}{l l} u _ {i, j + 1} - u _ {i, j}, & j <   n _ {2}, \\ 0, & j = n _ {1} \end{array} \right. \tag {3}
$$

# C. RELATED WORK

For blurred images with known blurring operator A, the image restoration problem can be treated by solving the unconstrained convex problem [2], [5], [6], [9]

$$
\underset {\boldsymbol {u}} {\text { minimize }} \quad \frac {1}{2} \| \boldsymbol {\mathcal {A}} \boldsymbol {u} - \boldsymbol {u} _ {0} \| _ {F} ^ {2} + \mu \| \boldsymbol {u} \| _ {\mathrm{TV} ^ {(I)}} \tag {4}
$$

where k · kF denotes Frobenius norm of matrix and $\mu > 0$ is regularization parameter that balances the trade-off between removing noise or small details.

For blurred images with an unknown blurring mechanism where the blurring operator A in model (1) is replaced by a convolutional kernel a, thus the model becomes

$$
\boldsymbol {a} * \boldsymbol {u} + \boldsymbol {w} = \boldsymbol {u} _ {0} \tag {5}
$$

The image blind deconvolution problem has been investigated by many researchers, of particular relevance to the method proposed here are the techniques developed in [13] where the blind deblurring problem is formulated as the optimization problem

$$
\min _ {\boldsymbol {u}, \boldsymbol {a}} F (\boldsymbol {u}, \boldsymbol {a}) = \frac {1}{2} \| \boldsymbol {a} * \boldsymbol {u} - \boldsymbol {u} _ {0} \| _ {2} ^ {2} + \beta_ {1} \| \boldsymbol {u} \| _ {\mathrm{BV}} ^ {2} + \beta_ {2} \| \boldsymbol {a} \| _ {\mathrm{BV}} ^ {2} \tag {6}
$$

where k·kBV is the bounded variation TV for image u and blur kernel a kukBV def =  R udivϕdx; $\boldsymbol { \varphi } = ( \varphi _ { 1 } , \varphi _ { 2 } , \cdot \cdot \cdot \varphi _ { N } \epsilon C _ { 0 } ^ { 1 } ( \Omega ) ^ { N } ) , \| \boldsymbol { \varphi } \| _ { L ^ { \infty } } ( \Omega ) \leq 1 \big \}$ denotes the boundary variational TV norm as defined in [13] for image u, and kakBV possess the same definition. Equation (6) is then solved by an alternating minimization strategy which starts by fixing kernel a to an initial estimate while minimizing functional $F ( { \pmb u } , { \pmb a } )$ with respect to u, then image u is fixed until the optimization result of $F ( { \pmb u } , { \pmb a } )$ is obtained with respect to a. The alternating procedure continues until both a and u converge, the convergence property of this algorithm is examined in [15].

# D. FAST GRADIENT-BASED ALGORITHMS FOR EQUATION (4)

To solve equation (4) with a known blurring operator A, there is an especially effective algorithm developed in [5], [9] based on a fast gradient projection (FGP) algorithm. In this algorithm, the objective function in (4) is expressed as $f ( { \pmb u } ) +$ g(u) where $\begin{array} { r } { f ( \pmb { u } ) \overset { - } { = } \frac { 1 } { 2 } \Vert \pmb { \mathcal { A } } \pmb { u } - \pmb { u } _ { 0 } \Vert _ { F } ^ { 2 } } \end{array}$ is convex and smooth while $g ( \pmb { u } ) = \mu \Vert \pmb { u } \Vert _ { \mathrm { T V } ^ { l } }$ is convex but nonsmooth. Let $\pmb { u } _ { k }$ be the image obtained in the kth iteration, the next iterative ${ \pmb u } _ { k + 1 }$ is generated by minimizing the proximal objective function which is quadratic and convex:

$$
Q _ {L} (\boldsymbol {u}, \boldsymbol {u} _ {k}) = f (\boldsymbol {u} _ {k}) + \langle (\boldsymbol {u}, \boldsymbol {u} _ {k}), \nabla f (\boldsymbol {u} _ {k}) \rangle + \frac {L}{2} \| \boldsymbol {u} - \boldsymbol {u} _ {k} \| _ {F} ^ {2} + g (\boldsymbol {u})
$$

${ \mathrm { s u b j e c t ~ t o : ~ } } u \in C = \{ \pmb { u } : b _ { l } \leq \pmb { u } _ { p , q } \leq b _ { u } \} .$ (7)

where $b _ { l }$ and $b _ { u }$ are lower and upper bounds to the image $( b _ { l } = 0$ and $b _ { u } = 2 5 5$ for 8-bit digital images), and L denotes the Lipschitz constant for $\nabla f ( \pmb { u } )$ , i.e., for any u and v,

$$
\left\| \boldsymbol {\mathcal {A}} ^ {\mathrm{T}} \boldsymbol {\mathcal {A}} (\boldsymbol {u} - \boldsymbol {v}) \right\| _ {F} \leq L \| \boldsymbol {u} - \boldsymbol {v} \| _ {F} \tag {8}
$$

Note that the first three terms on the right-hand side of (7) can be combined into a complete square term , hence the solution of the minimization problem, denoted by ${ \pmb u } _ { k + 1 } = P _ { L } ( { \pmb u } _ { k } )$ , can be expressed as

$$
P _ {L} (\boldsymbol {u} _ {k}) = \underset {\boldsymbol {u} \in C} {\operatorname{argmin}} \left\{\frac {L}{2} \| \boldsymbol {u} - (\boldsymbol {u} _ {k} - \frac {1}{L} \bigtriangledown h (\boldsymbol {u} _ {k})) \| _ {F} ^ {2} + \frac {\mu}{L} \| \boldsymbol {u} \| _ {\mathrm{TV}} \right\}
$$

$$
= \underset {\boldsymbol {u} \in C} {\operatorname{argmin}} \left\{\frac {L}{2} \| \boldsymbol {u} - \boldsymbol {b} _ {k} \| _ {F} ^ {2} + \frac {\mu}{L} \| \boldsymbol {u} \| _ {\mathrm{TV}} \right\} \tag {9}
$$

where

$$
\boldsymbol {b} _ {k} = \boldsymbol {u} _ {k} - \frac {1}{L} \boldsymbol {\mathcal {A}} ^ {\mathrm{T}} \boldsymbol {\mathcal {A}} (\boldsymbol {u} _ {k} - \boldsymbol {u} _ {0}) \tag {10}
$$

For implementation purposes, the Lipschitz constant L in (8) needs to be calculated. For the present case of f (u), (8) implies that

$$
L = \max _ {\| \boldsymbol {u} \| _ {F} = 1} \| \boldsymbol {\mathcal {A}} ^ {\mathrm{T}} \boldsymbol {\mathcal {A}} \boldsymbol {u} \| _ {F} \tag {11}
$$

In equation (9), ‘‘noisy’’ image is represented by bk and it can be updated using equation (10). In this way, the deblurring equation (4) can be solved by iteratively solving a sequence of denoising problem as specified in (9) and (10).

# III. NEW ALGORITHM BASED ON JOINT ESTIMATION OF KERNEL AND IMAGE

# A. THE SOLUTION METHOD AT A GLANCE

In this section, a novel algorithm is presented based on the TV-based formulation under the assumption that both a and u are unknown in the image model (5)

$$
\min _ {\boldsymbol {u}, \boldsymbol {a}} F (\boldsymbol {u}, \boldsymbol {a}) = \frac {1}{2} \| \boldsymbol {a} * \boldsymbol {u} - \boldsymbol {u} _ {0} \| _ {F} ^ {2} + \mu_ {1} \| \boldsymbol {u} \| _ {\mathrm{TV} ^ {(I)}} + \mu_ {2} \| \boldsymbol {a} \| _ {\mathrm{TV} ^ {(I)}} \tag {12}
$$

Traditional optimization approaches use alternating minimization where one of the unknowns is temporarily fixed while the other is being optimized, and the procedure continues in an alternating manner until both the kernel and image estimations converge. The difficulty encountered in a joint estimation method is that allowing both a and u to be unknown variables will make (5) nonlinear and destroy the convexity of function $F ( { \pmb u } , { \pmb a } )$ in (12). To deal with the aforementioned difficulty, we propose to work with (12) locally. Let $\pmb { u } _ { k }$ and $\pmb { a } _ { k }$ be the image and kernel obtained from the kth iteration, and we seek to find new estimates of the kernel and image in the form of $\pmb { u } = \pmb { u } _ { k } + \triangle \pmb { u }$ and $\pmb { a } = \pmb { a } _ { k } + \Delta \pmb { a }$ where the increments $\triangle \pmb { u }$ and $\triangle \pmb { a }$ denote small increments of $\pmb { u } _ { k }$ and $\pmb { a } _ { k }$ , respectively. Namely, $\triangle \pmb { u }$ and $\triangle \pmb { a }$ are matrices of the same size with $\pmb { u } _ { k }$ and $\pmb { a } _ { k }$ , whose elements are small in magnitude. With such constraints on $\triangle \pmb { u }$ and $\triangle \pmb { a } , \pmb { u } = \pmb { u } _ { k } + \triangle \pmb { u }$ and $\textbf { \em a } = \textbf { \em a } _ { k } + \Delta \textbf { \em a }$ will vary in a small vicinity of $\pmb { u } _ { k }$ and $\pmb { a } _ { k }$ , respectively. Under this assumption, we can write

$$
\begin{array}{l} \boldsymbol {a} * \boldsymbol {u} = (\boldsymbol {a} _ {k} + \triangle \boldsymbol {a}) (\boldsymbol {u} _ {k} + \triangle \boldsymbol {u}) \\ = \boldsymbol {a} _ {k} * \boldsymbol {u} _ {k} + \boldsymbol {a} _ {k} * \triangle \boldsymbol {u} + \triangle \boldsymbol {a} * \boldsymbol {u} _ {k} + \triangle \boldsymbol {a} * \triangle \boldsymbol {u} \\ = \left(\boldsymbol {a} _ {k} * \boldsymbol {u} _ {k} + \triangle \boldsymbol {a} * \boldsymbol {u} _ {k}\right) + \left(\boldsymbol {a} _ {k} * \triangle \boldsymbol {u} + \boldsymbol {a} _ {k} * \boldsymbol {u} _ {k}\right) \\ - \boldsymbol {a} _ {k} * \boldsymbol {u} _ {k} + \triangle \boldsymbol {a} * \triangle \boldsymbol {u} \\ = (\boldsymbol {a} _ {k} + \triangle \boldsymbol {a}) * \boldsymbol {u} _ {k} + (\triangle \boldsymbol {u} + \boldsymbol {u} _ {k}) * \boldsymbol {a} _ {k} \\ - \boldsymbol {a} _ {k} * \boldsymbol {u} _ {k} + \triangle \boldsymbol {a} * \triangle \boldsymbol {u} \\ = \boldsymbol {a} * \boldsymbol {u} _ {k} + \boldsymbol {u} * \boldsymbol {a} _ {k} - \boldsymbol {a} _ {k} * \boldsymbol {u} _ {k} + \triangle \boldsymbol {a} * \triangle \boldsymbol {u} \\ \approx \boldsymbol {a} * \boldsymbol {u} _ {k} + \boldsymbol {a} _ {k} * \boldsymbol {u} - \boldsymbol {a} _ {k} * \boldsymbol {u} _ {k} \tag {13} \\ \end{array}
$$

The above approximation for the last line of (13) is valid because both $\triangle \pmb { u }$ and $\triangle \pmb { a }$ are small, thus their product can be neglected. In this way, the equation (12) at hand can be simplified to

$$
\begin{array}{l} \min _ {\boldsymbol {u}, \boldsymbol {a}} F (\boldsymbol {u}, \boldsymbol {a}) = \frac {1}{2} \| \boldsymbol {a} * \boldsymbol {u} _ {k} + \boldsymbol {a} _ {k} * \boldsymbol {u} - \boldsymbol {f} _ {k} \| _ {F} ^ {2} \\ + \mu_ {1} \| \boldsymbol {u} \| _ {\mathrm{TV} ^ {(\mathrm{I})}} + \mu_ {2} \| \boldsymbol {a} \| _ {\mathrm{TV} ^ {(\mathrm{I})}} \tag {14} \\ \end{array}
$$

where $\pmb { f } _ { k } = \pmb { a } _ { k } * \pmb { u } _ { k } + \pmb { u } _ { 0 }$ . It is important to note that when both u and a are unknown, equation (14) still remains convex with respect to {u, a}.

For notation simplicity, we will denote $\textbf { \em x } = \{ \pmb { u } , \pmb { a } \}$ and define a linear operator $\pmb { A } _ { k }$ by $\pmb { \mathcal { A } } _ { k } \pmb { x } = \pmb { a } \ast \pmb { u } _ { k } + \pmb { a } _ { k }$ ∗u. Also, we denote $\| \pmb { x } \| _ { \mathrm { T V } , \mu } = \mu _ { 1 } \| \pmb { u } \| _ { \mathrm { T V } ^ { ( \mathrm { I } ) } } + \mu _ { 2 } \| \pmb { a } \| _ { \mathrm { T V } ^ { ( \mathrm { I } ) } }$ , the equation (14) now becomes

$$
\min _ {\boldsymbol {x}} F (\boldsymbol {x}) = \frac {1}{2} \| \boldsymbol {\mathcal {A}} _ {k} \boldsymbol {x} - \boldsymbol {f} _ {k} \| _ {F} ^ {2} + \| \boldsymbol {x} \| _ {\mathrm{TV} ^ {(I)}, \mu} \tag {15}
$$

and the minimization of $F ( \pmb { x } )$ in (15) is carried out subject to the following constrains:

$$
\sum_ {i = - m} ^ {m} \sum_ {j = - m} ^ {m} a _ {i, j} = 1 \tag {16a}
$$

$$
\boldsymbol {u} \geq 0, \boldsymbol {a} \geq 0 \tag {16b}
$$

$$
\left| \boldsymbol {u} _ {p, q} ^ {(k + 1)} - \boldsymbol {u} _ {p, q} ^ {(k)} \right| \leq \beta_ {1} \cdot I _ {\boldsymbol {u}} \tag {16c}
$$

$$
\left| \boldsymbol {a} _ {i, j} ^ {(k + 1)} - \boldsymbol {a} _ {i, j} ^ {(k)} \right| \leq \beta_ {2} \cdot I _ {\boldsymbol {a}} \tag {16d}
$$

$$
b _ {l} \leq \boldsymbol {u} _ {p, q} \leq b _ {u} \tag {16e}
$$

$$
\boldsymbol {a} _ {i, j} = \boldsymbol {a} _ {- i, - j}, \quad \text { for } 0 \leq i, j \leq m \tag {16f}
$$

where $\beta _ { 1 } \geq 0$ and $\beta _ { 2 } \geq 0$ are two small constants, $I _ { u } , I _ { a }$ are two defined unit matrices with the same size image u and kernel a. Constrains (16a) and (16f) impose normalization and symmetry conditions on the kernel; (16b) requires that both kernel and image are nonnegative; (16c) and (16d) ensure that the increments $\triangle \pmb { u }$ and $\triangle \pmb { a }$ are small in magnitude; and (16e) requires image u to be bounded.

By replacing $F ( { \pmb x } )$ in (15) with an approximate proximal objective function, the problem of minimizing $F ( { \pmb x } )$ in (15) is equivalent to separately minimizing two simplified objective functions based on the properties of the Frobnius norm as follows:

$$
\min _ {\boldsymbol {u}} F (\boldsymbol {u}) = \frac {1}{2} \| \boldsymbol {u} - \boldsymbol {b} _ {\boldsymbol {u} _ {k}} \| _ {F} ^ {2} + \frac {\mu_ {1}}{L} \| \boldsymbol {u} \| _ {\mathrm{TV} ^ {(I)}} \tag {17}
$$

and

$$
\min _ {\boldsymbol {a}} F (\boldsymbol {a}) = \frac {1}{2} \| \boldsymbol {a} - \boldsymbol {b} _ {\boldsymbol {a} _ {k}} \| _ {F} ^ {2} + \frac {\mu_ {2}}{L} \| \boldsymbol {a} \| _ {\mathrm{TV} ^ {(1)}} \tag {18}
$$

where $\pmb { b } _ { \pmb { u } _ { k } }$ and $\pmb { b } _ { \pmb { a } _ { k } }$ are known quantities in the kth iteration of the algorithm. The derivation details (leading to (17) and (18)) are given in Sec.III.B. Consequently, the blind deblurring problem at hand can be solved by iteratively performing two denoising subproblems:

$$
\min _ {\boldsymbol {u}} F (\boldsymbol {u}) = \frac {1}{2} \| \boldsymbol {u} - \boldsymbol {b} _ {\boldsymbol {u} _ {k}} \| _ {F} ^ {2} + \frac {\mu_ {1}}{L} \| \boldsymbol {u} \| _ {\mathrm{TV} ^ {(I)}} \tag {19a}
$$

$$
\text { subject   to }: \boldsymbol {u} \geq 0 \tag {19b}
$$

$$
\left| \boldsymbol {u} _ {p, q} ^ {(k + 1)} - \boldsymbol {u} _ {p, q} ^ {(k)} \right| \leq \beta_ {1} \cdot I _ {\boldsymbol {u}} \tag {19c}
$$

$$
b _ {l} \leq \boldsymbol {u} _ {p, q} \leq b _ {u} \tag {19d}
$$

where $1 \leq p \leq n _ { 1 } , 1 \leq q \leq n _ { 2 }$ and

$$
\min _ {\boldsymbol {a}} F (\boldsymbol {a}) = \frac {1}{2} \| \boldsymbol {a} - \boldsymbol {b} _ {\boldsymbol {a} _ {k}} \| _ {F} ^ {2} + \frac {\mu_ {2}}{L} \| \boldsymbol {a} \| _ {\mathrm{TV} ^ {(I)}} \tag {20a}
$$

$$
\text { subject   to }: \sum_ {i = - m} ^ {m} \sum_ {j = - m} ^ {m} a _ {i, j} = 1 \tag {20b}
$$

$$
\boldsymbol {a} \geq 0 \tag {20c}
$$

$$
\left| \boldsymbol {a} _ {i, j} ^ {(k + 1)} - \boldsymbol {a} _ {i, j} ^ {(k)} \right| \leq \beta_ {2} \cdot I _ {\boldsymbol {a}} \tag {20d}
$$

$$
\boldsymbol {a} _ {i, j} = \boldsymbol {a} _ {- i, - j} \tag {20e}
$$

where $0 \leq i , j \leq m$

Both equations (19) and (20) are standard image denoising problems to which fast algorithms such as those proposed in [5] and [9] are available.

# B. ANALYTICAL DETAILS OF THE PROPOSED ALGORITHM

Below we will provide analytical details of the three key issues involved in the proposed algorithm, namely symmetry property of the kernel, gradient of the first term of $F ( { \pmb x } )$ in (15) and derivation of equations (17) and (18).

# 1) SYMMETRY OF KERNEL a

For Gaussian lowpass blur, average blur and circularly averaging blur, the kernel matrix a is quadrantally symmetric (actually we assumed a specific symmetric structure for the kernel throughout the paper, but the proposed algorithms can absolutely extend to some other regular type of blur kernels), thus only its upper left part, denoted by a, should ebe considered as the designed variable because the rest of matrix a can be constructed using a as

$$
\boldsymbol {a} = \widetilde {\mathrm{I}} \tilde {\boldsymbol {a}} \widetilde {\mathrm{I}} ^ {\mathrm{T}} \tag {21}
$$

where a is assumed to be size $M \times M$ with $M = 2 m + 1$ .

$$
\widetilde {\mathrm{I}} = \mathrm{I} _ {m + 1} \widehat {\mathrm{I}} \tag {22}
$$

$\widehat { \mathrm { I } } = [ \mathrm { f l i p l r } ~ ( \mathrm { I } _ { m } ) 0 ]$ , fliplr $\left( \mathrm { I } _ { m } \right)$ is obtained by flipping identity matrix $\mathrm { I } _ { m }$ from left to right.

# 2) CALCULATE GRADIENT OF $\begin{array} { r } { h ( x ) = \frac 1 2 \| \mathcal { A } _ { k } x - f _ { k } \| _ { F } ^ { 2 } } \end{array}$

By the definitions of $\pmb { A } _ { k }$ and x (see Sec.III.A.), the adjoint of $\pmb { A } _ { k }$ , denoted by $\pmb { A } _ { k } ^ { \mathrm { T } }$ , can be found as follows (Assume v is a random image with the same size of u):

$$
\begin{array}{l} \langle \mathcal {A} _ {k} \boldsymbol {x}, \boldsymbol {v} \rangle = \left\langle \boldsymbol {a} * \boldsymbol {u} _ {k} + \boldsymbol {a} _ {k} * \boldsymbol {u}, \boldsymbol {v} \right\rangle \\ = \langle \boldsymbol {a} * \boldsymbol {u} _ {k}, \boldsymbol {v} \rangle + \langle \boldsymbol {a} _ {k} * \boldsymbol {u}, \boldsymbol {v} \rangle \\ = \langle \boldsymbol {a}, \hat {\boldsymbol {u}} _ {k} * \boldsymbol {v} \rangle + \langle \boldsymbol {u}, \hat {\boldsymbol {a}} _ {k} * \boldsymbol {v} \rangle \\ = \langle (\boldsymbol {u}, \boldsymbol {a}), \{\hat {\boldsymbol {a}} _ {k} * \boldsymbol {v}, \hat {\boldsymbol {u}} _ {k} * \boldsymbol {v} \} \rangle \\ = \langle \boldsymbol {x}, \boldsymbol {\mathcal {A}} _ {k} ^ {T} \boldsymbol {v} \rangle \tag {23} \\ \end{array}
$$

hence $\pmb { \mathcal { A } } _ { k } ^ { T } \pmb { \nu } = \{ \hat { \pmb { a } } _ { k } * \pmb { \nu } , \hat { \pmb { u } } _ { k } * \pmb { \nu } \}$ , where $\hat { \pmb { a } } _ { i , j } ^ { ( k ) } = \pmb { a } _ { - i , - j } ^ { ( k ) } , - m \leq$ aˆ i,j a −i,−j, −m ≤ $i , j \le m , \hat { \pmb { u } } _ { p , q } ^ { ( k ) } = \pmb { u } _ { - p , - q } ^ { ( k ) } , - m \le p \le n _ { 1 } , - m \le q \le n _ { 2 }$ , to obtain an expression of $\hat { \pmb u } _ { k }$ , we compute

$$
\begin{array}{l} \langle \boldsymbol {a} * \boldsymbol {u} _ {k}, \boldsymbol {v} \rangle = \sum_ {p = 1} ^ {n _ {1}} \sum_ {q = 1} ^ {n _ {2}} \left(\sum_ {i = - m} ^ {m} \sum_ {j = - m} ^ {m} \boldsymbol {a} _ {i, j} \boldsymbol {u} _ {p - i, q - j} ^ {(k)}\right) \cdot \boldsymbol {v} _ {p, q} \\ = \sum_ {i = - m} ^ {m} \sum_ {j = - m} ^ {m} \boldsymbol {a} _ {i, j} \left(\sum_ {p = 1} ^ {n _ {1}} \sum_ {q = 1} ^ {n _ {2}} \boldsymbol {u} _ {p - i, q - j} ^ {(k)} \cdot \boldsymbol {v} _ {p, q}\right) \\ = \langle \boldsymbol {a}, \hat {\boldsymbol {u}} _ {k} * \boldsymbol {v} \rangle \tag {24} \\ \end{array}
$$

Thus $\hat { \pmb { u } } _ { k } \ * \ \pmb { \nu }  &  = \ \sum _ { p = 1 } ^ { n _ { 1 } } \sum _ { q = 1 } ^ { n _ { 2 } } \pmb { u } _ { p - i , q - j } ^ { ( k ) } \ \cdot \ \pmb { \nu } _ { p , q }$ which implies $\hat { \pmb { u } } _ { p , q } ^ { ( k ) } = \pmb { u } _ { - p , - q } ^ { ( k ) } .$ uˆ p,q = u −p,−q.

To obtain an expression of $\hat { \pmb a } _ { k }$ , here we assume periodic boundary extension for image and then compute:

$$
\begin{array}{l} \langle \boldsymbol {a} _ {k} * \boldsymbol {u}, \boldsymbol {v} \rangle = \sum_ {p = 1} ^ {n _ {1}} \sum_ {q = 1} ^ {n _ {2}} \left(\sum_ {i = - m} ^ {m} \sum_ {j = - m} ^ {m} \boldsymbol {a} _ {i, j} ^ {(k)} \boldsymbol {u} _ {p - i, q - j}\right) \cdot \boldsymbol {v} _ {p, q} \\ = \sum_ {i = - m} ^ {m} \sum_ {j = - m} ^ {m} \boldsymbol {a} _ {- i, - j} ^ {(k)} \left(\sum_ {p = 1} ^ {n _ {1}} \sum_ {q = 1} ^ {n _ {2}} \boldsymbol {u} _ {p, q} \cdot \boldsymbol {v} _ {p - i, q - j}\right) \\ \end{array}
$$

$$
\begin{array}{l} \text { let } \quad p ^ {\prime} = p - i, q ^ {\prime} = q - j, \\ = \sum_ {i = - m} ^ {m} \sum_ {j = - m} ^ {m} \boldsymbol {a} _ {i, j} ^ {(k)} \left(\sum_ {p ^ {\prime} = 1 - i} ^ {n _ {1} - i} \sum_ {q ^ {\prime} = 1 - j} ^ {n _ {2} - j} \boldsymbol {u} _ {p ^ {\prime}, q ^ {\prime}} \cdot \boldsymbol {v} _ {p ^ {\prime} + i, q ^ {\prime} + j}\right) \\ \end{array}
$$

let a(k )−i0,−j0 $\begin{array} { r } { { \pmb a } _ { - i ^ { \prime } , - j ^ { \prime } } ^ { ( k ) } \triangleq \hat { { \pmb a } } _ { i , j } ^ { ( k ) } , i ^ { \prime } = i , j ^ { \prime } = j , } \end{array}$ aˆ (ki, , then

$$
\begin{array}{l} = \sum_ {i = - m} ^ {m} \sum_ {j = - m} ^ {m} \hat {\boldsymbol {a}} _ {i, j} ^ {(k)} \left(\sum_ {p = 1 + i} ^ {n _ {1} + i} \sum_ {q = 1 + j} ^ {n _ {2} + j} \boldsymbol {u} _ {p, q} \cdot \boldsymbol {v} _ {p - i, q - j}\right) \\ = \sum_ {p = 1} ^ {n _ {1}} \sum_ {q = 1} ^ {n _ {2}} \boldsymbol {u} _ {p, q} \left(\sum_ {i = - m} ^ {m} \sum_ {j = - m} ^ {m} \boldsymbol {a} _ {- i, - j} ^ {(k)} \cdot \boldsymbol {v} _ {p - i, q - j}\right) \\ = \langle \boldsymbol {u}, \hat {\boldsymbol {a}} _ {k} * \boldsymbol {v} \rangle \tag {25} \\ \end{array}
$$

which implies aˆ i,j $\hat { \pmb { a } } _ { i , j } ^ { ( k ) } = { \pmb { a } } _ { - i , - j } ^ { ( k ) } .$

Using the equations of (21), (22) and (23), the gradient of h(x) can be computed as following

$$
\nabla h (\boldsymbol {x}) = \left\{\hat {\boldsymbol {a}} _ {k} * \left(\boldsymbol {\mathcal {A}} _ {k} \boldsymbol {x} - \boldsymbol {f} _ {k}\right), \widetilde {\mathrm{I}} ^ {\mathrm{T}} \left[ \hat {\boldsymbol {u}} _ {k} * \left(\boldsymbol {\mathcal {A}} _ {k} \boldsymbol {x} - \boldsymbol {f} _ {k}\right) \right] \widetilde {\mathrm{I}} \right\} \tag {26}
$$

where variable x is redefined as $\pmb { x } = \{ \pmb { u } , \tilde { \pmb { a } } \}$ .

# 3) DERIVATION OF (17) AND (18)

Considering the minimization of the proximal objective function of F (x) in (15):

$$
Q (\boldsymbol {x}, \boldsymbol {x} _ {k}) = h (\boldsymbol {x} _ {k}) + \langle \boldsymbol {x} - \boldsymbol {x} _ {k}, \nabla h (\boldsymbol {x} _ {k}) \rangle + \frac {L}{2} \| \boldsymbol {x} - \boldsymbol {x} _ {k} \| _ {F} ^ {2} + \| \boldsymbol {x} \| _ {\mu , \mathrm{TV}} \tag {27}
$$

where L is a Lipschitz constant of 5h(x). It follows that up to a constant the first three terms on the right-hand side of (27) can be combined into a complete square term, i.e.,

$$
Q (\boldsymbol {x}, \boldsymbol {x} _ {k}) = \frac {L}{2} \| \boldsymbol {x} - (\boldsymbol {x} _ {k} - \frac {1}{L} \bigtriangledown h (\boldsymbol {x} _ {k})) \| _ {F} ^ {2} + \| \boldsymbol {x} \| _ {\mu , \mathrm{TV} ^ {(I)}} \tag {28}
$$

Let

$$
\boldsymbol {b} _ {k} = \boldsymbol {x} _ {k} - \frac {1}{L} \bigtriangledown h (\boldsymbol {x} _ {k}) \triangleq (\boldsymbol {b} _ {\tilde {\boldsymbol {a}} _ {k}}, \boldsymbol {b} _ {\boldsymbol {u} _ {k}}) \tag {29}
$$

then (27) can be written as

$$
\begin{array}{l} Q (\boldsymbol {x}, \boldsymbol {x} _ {k}) = \frac {1}{2} \| \boldsymbol {u} - \boldsymbol {b} _ {\boldsymbol {u} _ {k}} \| _ {F} ^ {2} + \frac {1}{2} \| \tilde {\boldsymbol {a}} - \boldsymbol {b} _ {\tilde {\boldsymbol {a}} _ {k}} \| _ {F} ^ {2} \\ + \frac {\mu_ {1}}{L} \| \boldsymbol {u} \| _ {\mu , \mathrm{TV}} + \frac {\mu_ {2}}{L} \| \tilde {\boldsymbol {a}} \| _ {\mu , \mathrm{TV}} \tag {30} \\ \end{array}
$$

Note that the first and third terms of (30) only depend on variable u, while the other two terms only depend on variable a˜. According to the properties of the Frobenius norm, the minimization of $Q ( { \pmb x } , { \pmb x } _ { k } )$ can be accomplished by two separate minimizations, namely

$$
\min _ {\boldsymbol {u}} \frac {1}{2} \| \boldsymbol {u} - \boldsymbol {b} _ {\boldsymbol {u} _ {k}} \| _ {F} ^ {2} + \frac {\mu_ {1}}{L} \| \boldsymbol {u} \| _ {\mathrm{TV} ^ {(I)}} \tag {31}
$$

which is identical to (17), and

$$
\min _ {\tilde {a}} \frac {1}{2} \| \tilde {a} - b _ {\tilde {a} _ {k}} \| _ {F} ^ {2} + \frac {\mu_ {2}}{L} \| \tilde {a} \| _ {\mathrm{TV} ^ {(I)}} \tag {32}
$$

which is a simplified version of (18) with a˜ replacing a in the light of symmetry property of a, as discussed earlier.

Based on the analysis and derivation what has been done in Sec III.A and Sec III.B, the proposed algorithm for blind deconvolution can be outlined as Algorithm 1.

# Algorithm 1 Implementation of the Proposed Algorithm

# Input:

Input image $\pmb { u } _ { 0 } .$ parameters m, $L , \delta , \mu _ { 1 } , \mu _ { 2 } , b _ { l } , b _ { u } , \beta _ { 1 }$ and $\beta _ { 2 } ,$ , and number of iterations $N ;$ set iteration counter $k = 0 ,$ , initial u to be $\pmb { u } _ { 0 } .$ , and initial a˜ to be the 2nd quadrant submatrix of the δ-matrix of size $( 2 m + 1 ) \times ( 2 m + 1 )$ .

# if k <N then

• Use (26) and (29) to compute and update $\pmb { b } _ { \tilde { \pmb { a } } _ { k } }$ and $\pmb { b } _ { \pmb { u } _ { k } }$   
• Solve problems (31) and (32) to get ${ \pmb u } _ { k }$ and $\tilde { \pmb { a } } _ { k }$ , respectively.   
• Set $k = k + 1$ . If k = N , output solution $\{ \pmb { u } _ { k } , \pmb { a } _ { k } \}$ and terminate, otherwise repeat the loop until the algorithm iteration proceeds to convergence.

# end if

# Output:

Optimal solution $\{ \pmb { u } _ { k } , \pmb { a } _ { k } \}$ .

# C. BLIND DEBLURRING OF COLOR IMAGES

A color image with the size of $n _ { 1 } \times n _ { 2 }$ is represented by $u =$ $\{ u ^ { ( r ) } , u ^ { ( g ) } , u ^ { ( \bar { b } ) } \}$ , where $u ^ { ( r ) } , u ^ { ( g ) }$ and $u ^ { ( b ) }$ are the components of u in red (R), green (G) and blue (B) channels, respectively. For color images, the model in (5) still remains valid where $a = \{ a ^ { ( r ) } , a ^ { ( g ) } , a ^ { ( b ) } \}$ and $w = \{ w ^ { ( r ) } , w ^ { ( g ) } , w ^ { ( b ) } \}$ , so model (5) is equivalent to three single-channel models

$$
a ^ {(\gamma)} * u ^ {(\gamma)} + w ^ {(\gamma)} = u _ {0} ^ {(\gamma)} \text {   for   } \gamma = r, g, b. \tag {33}
$$

Blind deblurring a color image is a problem of recovering image from observation $u _ { 0 } ~ = ~ \{ u _ { 0 } ^ { ( r ) } , u _ { 0 } ^ { ( g ) } , u _ { 0 } ^ { ( b ) } \}$ ) (b) , where the blurring kernel a is unknown. Based on equation (30), blind deblurring a color image can be accomplished by solving three convex problems

$$
\begin{array}{l} \min _ {u ^ {(\gamma)}, a ^ {(\gamma)}} F _ {\gamma} (u ^ {(\gamma)}, a ^ {(\gamma)}) = \frac {1}{2} \| a ^ {(\gamma)} * u ^ {(\gamma)} - u _ {0} ^ {(\gamma)} \| _ {F} ^ {2} + \mu_ {1} ^ {(\gamma)} \\ \left\| u ^ {(\gamma)} \right\| _ {\mathrm{TV} ^ {(I)}} + \mu_ {2} ^ {(\gamma)} \left\| a ^ {(\gamma)} \right\| _ {\mathrm{TV} ^ {(I)}} \tag {34} \\ \end{array}
$$

for $\gamma = r , g , b .$ . On problem (34) with (12), it’s quite clear that each problems in (34) is identical to a problem of blind deconvolution of an image, hence it can be solved by applying Algorithm 1.

# IV. PERFORMANCE EVALUATION

In this section, simulations are presented to illustrate the performance for our algorithm. The performance evaluation was carried out visually (i.e. subjectively) as well as numerically (i.e. objectively) from the improvement in peak-signal-tonoise ratio (PSNR) to structural similarity index measurement (SSIM). Besides these two evaluation standards, the computation efficiency was also studied. All simulations were performed on a Windows7 laptop PC with an Intel(R) Core(TM) i3-4010U Duo CPU P8700@1.70 GHz with 4.0 GB of RAM.

Performance of our algorithm was compared with the alternating optimization based method first developed in the late 1990’s and advanced in the early 2000’s [10], [11], [13]–[15] and the latest algorithm which is proposed in [14]. Algorithm [14] remains to be one of the best (if not the best) methods available for blind deconvolution of still images. $\mathbf { A } \mathbf { s }$ mentioned earlier, state of the art deblurring algorithms such as those in [5] and [9] have been proposed, however the methods in [5] and [9] assume known blurring kernels. In our simulations, algorithm [13] reduces the blind deconvolution problem into two standard (nonblind) deconvolution subproblems, and was carried out using the fast convex programming solver provided by [9] for efficient and accurate solution. In other words, our algorithm was compared with an algorithm that combines the best of the methods of [9] and [13]. For this reason, we shall call it $^ { 6 6 } [ 1 3 ] + [ 9 ] ^ { 5 }$ method in the rest of this section. The algorithm [33] solved blind deconvolution problem using the quadratic upper-bounded TV as the regularizer. The approximation cuts off the high frequency information and the alternate minimization step resulted in quality degradation and computation, but the performance of algorithm [14] is better than the aforementioned algorithms; it’s calculation of PSNR needs to extract some pixels from the edge of the image, and this will lead to some uncertainty to PSNR improvement, so we just made one comparison for gray-scale image Lena because of the uncertain result.

# A. BLIND DEBLURRING OF STANDARD GRAY-SCALE IMAGES

For visual examination, the proposed algorithm was applied to standard classic image Lena, which was degraded by original $9 \times 9$ Gaussian kernel with standard deviation δ, which is 4 and additive Gaussian white noise with standard deviation $\sigma \ = \ 1 0 ^ { - 3 }$ . The original, blurred, and deblurred images of Lena by the [13] + [9], [14] and the proposed methods are shown in Fig.1 (a), (b), (c), (d) and (e). The numerical values of bounds $\beta _ { 1 } , \beta _ { 2 }$ and regularization parameters $\mu _ { 1 } , \mu _ { 2 }$ were set to $( \beta _ { 1 } , \beta _ { 2 } , \mu _ { 1 } , \mu _ { 2 } ) = ( 2 \times 1 0 ^ { - 2 } , 5 \times 1 0 ^ { - 3 } , 6 \times 1 0 ^ { - 5 }$ , $3 ~ \times ~ 1 0 ^ { - 5 } )$ . It is observed that the PSNR has been improved from 23.4520 dB to 27.3840 dB, 28.1110 dB and 29.5081 dB via [13] + [9], [14] and the proposed method, respectively. The SSIM is improved from 0.6417 to 0.7656, 0.7654 and 0.8287. The approximate eclipse time for algorithm [13] + [9] is 51.8859s, [14] is 539.4359s and our algorithm is 38.3606s. The original and identified kernels of Gaussian are depicted in Fig.2.

![](images/d773709599ec77e26f3f30363f0b7482d065bb406623ac5ff83c3fb6b56fa66b.jpg)  
FIGURE 1. (a) Original image, (b) blurred image, (c) deblurred by [13] + [9] method $( \lambda _ { 1 } = 1 \times \mathsf { i } 0 ^ { - 4 } , \lambda _ { 2 } = 2 \times \mathsf { i } 0 ^ { - 4 } ) ,$ (d) deblurred by [14] and (e) deblurred by the proposed algorithm.

![](images/cd5c47cc5d5107d95080d8b0e44a3a1f20a8afc48a5e8c416e246ab9cd3158da.jpg)



![](images/07f08948186b62fa8a17b6a48c5171bb8c74f8a4761296a8c920bc8c01c35266.jpg)



FIGURE 2. (a) Original and (b) the identified Gaussian kernel using the proposed algorithm with the L2-error of 0.0008.

The proposed algorithm is extended to standard gray images Satellite and Cameraman $( 2 5 6 \quad \times \quad 2 5 6 ) .$ , Boat $( 5 1 2 \times 5 1 2 )$ with different kernels, where $9 \times 9$ Gaussian, $7 \times 7$ average lowpass and $9 \times 9$ circularly lowpass (also known as disk) blurs and additive Gaussian white noise with standard deviation $\sigma ~ = ~ 1 0 ^ { - 4 } .$ , $1 0 ^ { - 3 }$ and $1 0 ^ { - 4 }$ are imposed, respectively. The parameters were set as $\begin{array} { r l r } { ( \beta _ { 1 } , \beta _ { 2 } , \mu _ { 1 } , \mu _ { 2 } ) } & { { } = } & { ( 0 . 0 6 , 0 . 0 0 2 } \end{array}$ , $1 \times 1 0 ^ { - 4 } , 2 \times 1 0 ^ { - 5 } )$ for Satellite and Boat, and $( 0 . 0 5 , 0 . 0 0 4 , 1 \times 1 0 ^ { - 4 } , 2 \times 1 0 ^ { - 5 } )$ for Cameraman, respectively. The comparison results for Satellite are depicted in Fig.3, the SSIM, PSNR, identified kernel L2-error and the eclipsed time between our and [13] + [9] methods are listed in TABLE 1 and the other images compared results are shown in TABLE 2.

(a) Original image   
![](images/3266c6b3706d906f6801742219c0a7ea5041a0c41f4e423f959f91f6a584fac0.jpg)



(c)[13]+[9]   
![](images/043bedc433385e869a1d637cb072254ace88ea63f80f2660e62a90527946f539.jpg)



(b) Degraded image   
![](images/666f1134c964b796718ff31bfce475f330ef4ada8a3203ec1ecce04049f952ff.jpg)



(d) Our Algorithm   
![](images/c328cc4ad6ecec9eaf5ebbbd0e50e59d00e754e552e331040955734bcabab7b5.jpg)



FIGURE 3. (a) Original image, (b) blurred image, (c) deblurred by [13] + [9] method $( \lambda _ { 1 } = 3 \times 1 0 ^ { - 4 } , \lambda _ { 2 } = 1 \times 1 0 ^ { - 5 } ) .$ , (d) output of our algorithm.

TABLE 1. Performance comparison for gray image Satellite. 

<table><tr><td>MethodSatellite</td><td>[13] + [9]</td><td>Proposed Algorithm</td></tr><tr><td>SSIM</td><td>0.7595→0.9125</td><td>0.7595→0.9739</td></tr><tr><td>PSNR (dB)</td><td>21.4131→25.6472</td><td>21.4131→31.4932</td></tr><tr><td>Identified kernel L2 Error</td><td>0.0090</td><td>0.0033</td></tr><tr><td>Eclipse Time (s)</td><td>77.9242</td><td>48.9063</td></tr></table>

TABLE 2. Performance comparison of standard gray images. 

<table><tr><td rowspan="2">PSNR Blur(Images)</td><td rowspan="2">PSNR before</td><td colspan="2">PSNR after</td></tr><tr><td>[13] + [9]</td><td>Proposed Algorithm</td></tr><tr><td>Gaussian (Satellite)</td><td>21.4131</td><td>25.6472</td><td>31.3250</td></tr><tr><td>Average (Boat)</td><td>24.9657</td><td>28.0963</td><td>32.0029</td></tr><tr><td>Disk (Cameraman)</td><td>21.6917</td><td>22.8786</td><td>29.0434</td></tr><tr><td>E(t) (Satellite) (s)</td><td>\</td><td>77.9242</td><td>48.9063</td></tr><tr><td>E(t) (Boat) (s)</td><td>\</td><td>217.2793</td><td>127.9388</td></tr><tr><td>E(t) (Cameraman) (s)</td><td>\</td><td>16.4455</td><td>3.4942</td></tr></table>

![](images/6fbc443801c5987268d752ad87bd291c5d7e3026c86ca7edf7fc1d47770e35a8.jpg)



![](images/ea4b40f029b79332c319d9715c79990159d63f39b734a83cf442cf6813b6eb86.jpg)



![](images/3fd605be358dd29802388a72bde33dffe207ea4ab05e7ccbcf7eb916e61e64f4.jpg)



(f)

![](images/43b3a17eed076b88fff33420078dac43b08c38b59f309290e46109386e119f10.jpg)



FIGURE 4. Different natural gray-scale images. (a) Lifebuoy. (b) Axe. (c) Building. (d) Bird. (e) Flag. (f) Bridge.   
![](images/32d1e68aa352d80870bc0e5465cc57521f2e63299b9e61ab7e9fddf74eac15a7.jpg)



![](images/8ddb44f48e3400479405b68d4284cb1135035d3cd4fd3281ef002e1d0770cb86.jpg)



# B. BLIND DEBLURRING OF NATURAL GRAY-SCALE IMAGES

The natural images Lifebuoy, Axe, Fence, Bird, Flag, Building as depicted in Fig.4 were used to validate the efficiency of the proposed algorithm. The improvement of PSNR, SSIM and the regulated parameters for them are available in TABLE 3, respectively as compared with [13] + [9] method.

Lifebuoy (240 × 240) is degraded by $9 \times 9$ Gaussian blurs and additive Gaussian white noise with standard deviation $\sigma ~ = ~ 1 0 ^ { - 4 }$ . The bounds $\beta _ { 1 } , \beta _ { 2 }$ and regularization parameters $\mu _ { 1 } , \mu _ { 2 }$ were set to $( \beta _ { 1 } , \beta _ { 2 } , \mu _ { 1 } , \mu _ { 2 } ) ~ = ~ ( 0 . 0 6 , 0 . 0 0 2$ , $4 \times 1 0 ^ { - 4 } , 9 \times 1 0 ^ { - 4 } )$ and the compared simulation results are presented in Fig.5. The L2-error of identified kernels are 0.0046 and 0.0011 using [13] + [9] and our algorithm, respectively, and other parameters are presented in TABLE 3.

# C. BLIND DEBLURRING OF SYNTHETIC GRAY-SCALE IMAGES

Synthetic images, Art, $Z i g$ and Sun, with the same size of $2 4 0 \times 2 4 0$ in Fig.6 were introduced to test the effectiveness for the proposed algorithm. These three images are degraded by

TABLE 3. Blind deblurring of gray-scale standard images: performance comparison. 

<table><tr><td rowspan="2">Images (Kernel)</td><td colspan="4">Regulate Parameters of the proposed Algorithm</td><td rowspan="2">PSNR/SSIM before</td><td colspan="2">PSNR/SSIM after</td></tr><tr><td> $\beta_1$ </td><td> $\beta_2$ </td><td> $\mu_1$ </td><td> $\mu_2$ </td><td>[13] + [9]</td><td>Proposed Algorithm</td></tr><tr><td>Lifebuoy (gaussian)</td><td> $4 \times 10^{-4}$ </td><td> $9 \times 10^{-4}$ </td><td> $6 \times 10^{-2}$ </td><td> $2 \times 10^{-3}$ </td><td>25.9654/0.8272</td><td>30.4061/0.8837</td><td>33.7803/0.9173</td></tr><tr><td>Axe (gaussian)</td><td> $4 \times 10^{-4}$ </td><td> $9 \times 10^{-4}$ </td><td> $5 \times 10^{-2}$ </td><td> $2 \times 10^{-3}$ </td><td>24.9514/0.8510</td><td>31.2255/0.9302</td><td>38.6929/0.9783</td></tr><tr><td>Fence (average)</td><td> $8 \times 10^{-4}$ </td><td> $1 \times 10^{-4}$ </td><td> $1 \times 10^{-2}$ </td><td> $8 \times 10^{-4}$ </td><td>21.1648/0.7423</td><td>26.1194/0.8701</td><td>33.6950/0.9613</td></tr><tr><td>Bird (average)</td><td> $2 \times 10^{-4}$ </td><td> $1 \times 10^{-4}$ </td><td> $2 \times 10^{-2}$ </td><td> $4 \times 10^{-3}$ </td><td>26.9491/0.8839</td><td>30.9314/0.9386</td><td>35.4784/0.9753</td></tr><tr><td>Flag (disk)</td><td> $1 \times 10^{-4}$ </td><td> $2 \times 10^{-5}$ </td><td> $1 \times 10^{-2}$ </td><td> $4 \times 10^{-3}$ </td><td>22.2982/0.7511</td><td>23.7515/0.7705</td><td>29.1623/0.8293</td></tr><tr><td>Building (disk)</td><td> $1 \times 10^{-4}$ </td><td> $2 \times 10^{-4}$ </td><td> $6 \times 10^{-2}$ </td><td> $8 \times 10^{-3}$ </td><td>19.6731/0.4830</td><td>20.6847/0.5332</td><td>25.0840/0.7008</td></tr></table>

(a) Original image   
![](images/00582622cb26391145c9382447699aef4059ab121dd563bcd42c819b1139e485.jpg)



(c)[13]+[9]

(b) Degraded image   
![](images/cead8a8c82a84dabd65a30bbbfef02ffe10bb8ecf381023e8ce3ff317d604ad5.jpg)



(d) Our Algorithm

![](images/042ea2e0f09138ed1e76f397b3acaad47bd1e360ae788289667ee6882a387ce2.jpg)



![](images/db0a37402c1abd3986c19ff0066c23b83b64811d86f651a97f90fd68dbf05101.jpg)



FIGURE 5. (a) Original image, (b) blurred image, (c) deblurred by [13] + [9] method $( \lambda _ { 1 } = 3 \times 1 0 ^ { - 4 } , \lambda _ { 2 } = 1 \times 1 0 ^ { - 5 } ) .$ , (d) output of our algorithm.

![](images/ac8a262e7f45c0fa1637d581ec10afed72cb322ff88277092f7f3bed870e03c1.jpg)



(b)   
![](images/195856fbb0c03d3df3b0f9ae54a6181ef0cb1807efe81427b1f1e070a700c15d.jpg)



（c）  
![](images/2dc47a2857fe91fe1b0607b9cc8b4dbc739efca4a1f578eb615980a1dd5042ad.jpg)



FIGURE 6. Different synthetic gray-scale images. (a) Art. (b) Zig. (c) Sun.

$9 \times 9$ gaussian, average and disk blurs and additive Gaussian white noise with standard deviation $\sigma = 1 0 ^ { - 4 }$ , respectively.

The compared restoration results for the above synthetic image Art are illustrated in Fig.7 and the simulated results for $Z i g$ and Sun are presented in TABLE 4.

# D. BLIND DEBLURRING OF COLOR IMAGES

Our algorithm was also extended to standard and natural color images. The standard color Baboon and Lena images (256 × 256), and Barbara $( 5 1 2 \times 5 1 2 )$ , are imposed by 11 × 11 Gaussian, Average and Disk blurring

(a)   
![](images/9e4d2e80c24b5aea78298d4d6f558bf2b93840e880b3409396784939f1c1bc1d.jpg)



(b)   
![](images/d6f892c89cb9cb4be6649aa64a38e24ef992aba47b2a1581b1e65ab7d584f795.jpg)



（c）  
![](images/8a3394d74fdadfcb7b6a9098f29c7d419c92cf9d8793eb2e18d7036f193e828e.jpg)



(d)   
![](images/8d494d13bdcb1f05f8a1adf76cf75a90e7a3720cd44e4205962339ba7d5f06e5.jpg)



FIGURE 7. (a) Original image, (b) degraded image, (c) restored by [13] + [9] method $( \lambda _ { 1 } = 3 \times 1 0 ^ { - 4 } , \lambda _ { 2 } = 2 \times 1 0 ^ { - 5 } ) ,$ (d) restored by the proposed algorithm.

TABLE 4. Blind deblurring of synthetic gray-scale images: performance comparison. 

<table><tr><td rowspan="2">PSNR Blur</td><td rowspan="2">PSNR before</td><td colspan="2">PSNR after</td><td rowspan="2">SSIM before</td><td colspan="2">SSIM after</td></tr><tr><td>[13+9]</td><td>Proposed</td><td>[13+9]</td><td>Proposed</td></tr><tr><td>G (Art)</td><td>19.9641</td><td>31.7525</td><td>44.1826</td><td>0.7291</td><td>0.9713</td><td>0.9979</td></tr><tr><td>A (Zig)</td><td>14.2461</td><td>21.8093</td><td>26.4760</td><td>0.5310</td><td>0.7713</td><td>0.8838</td></tr><tr><td>D (Sun)</td><td>16.9608</td><td>19.0682</td><td>30.6138</td><td>0.6834</td><td>0.7599</td><td>0.9803</td></tr></table>

kernels and additive Gaussian white noise with $\sigma = 1 0 ^ { - 4 }$ The comparison results for Baboon are shown in Fig.8.

Three different profiles for L2-error of identified kernels are demonstrated in Fig.9 and three curves present their convergence trend as the iteration proceeds. The simulation results of the below three standard color images about PSNR, SSIM improvements are offered in Table 5 where the superiority of the proposed algorithm over the [13] + [9] method can easily be observed.

We also report some natural color images restoration results, such as Flag, Fence and Lifebuoy, all these three images with the same size of 240×240. As depicted in Fig.10, each is degraded by a $1 1 \times 1 1$ blurring kernel and additive Gaussian white noise with $\sigma = 1 0 ^ { - 4 }$ .

(a)   
![](images/4cabb973caf89c5ee933fd0adb5c6f5b3d35aa59c6b4040bdc2b74997474a5ba.jpg)



（c）

![](images/7349b187fdfae781776f644ae4273312595dffb2c28b0737b7cdcb603909177d.jpg)



![](images/ed5b315a6ce003f2031f488c3bfb5a5e2c35279ec5f4c93eed73183a16f8c751.jpg)



![](images/1898a7777aa7a89b882b916dfab67d977981655e46a4143b409bd82a8b91c1bf.jpg)



FIGURE 8. (a) Original image, (b) degraded image (PSNR = 16.3624 dB), (c) restored by [13] + [9] method (PSNR = 17.7732 dB, SSIM = 0.7149), (d) restored by the proposed algorithm (PSNR = 19.6816 dB, SSIM = 0.8177).

L2 error of indetified kernel   
![](images/5e3bf7a84dfe0d15677c5abd580b75bb978e5aee7f796ced18f0921fbfe74b2f.jpg)



FIGURE 9. Profiles for three channels about L2-Error of identified kernels.

TABLE 5. Performance comparison of standard color images. 

<table><tr><td rowspan="2">PSNR Blur</td><td rowspan="2">PSNR before</td><td colspan="2">PSNR after</td><td rowspan="2">SSIM before</td><td colspan="2">SSIM after</td></tr><tr><td>[13+9]</td><td>Proposed</td><td>[13+9]</td><td>Proposed</td></tr><tr><td>G (baboon)</td><td>16.3624</td><td>17.7732</td><td>19.6816</td><td>0.6386</td><td>0.7149</td><td>0.8177</td></tr><tr><td>A (barbara)</td><td>18.5496</td><td>20.3208</td><td>22.0008</td><td>0.7562</td><td>0.8068</td><td>0.8966</td></tr><tr><td>D (lena)</td><td>18.4232</td><td>19.2934</td><td>23.4277</td><td>0.9140</td><td>0.9196</td><td>0.9652</td></tr></table>

The original, blurred, and deblurred Fence images by the two algorithms are shown in Fig.11. The PSNR using our algorithm is improved from 15.5430 dB to 24.7198 dB, [13] + [9] just obtained 18.1674 dB. The other evaluation standard of SSIM can be increased from 0.6266 to 0.9007 offered by the proposed method, but [13] + [9] only achieved 0.6983.

(a)   
![](images/40fa4e4beedf561ffd2ad0d386d93b355ca28b72787d05164e5da60336e0a8e4.jpg)



(b)   
![](images/63ce0a785038efa2c57d17b8132467f259a3417ecec21fc8eb18aa6f910c9938.jpg)



（c）  
![](images/89c85031c8d0162cb1cc861f31d3197cce0d6c97382687c645eee4b1542937cb.jpg)



FIGURE 10. Different natural color images. (a) Flag. (b) Fence. (c) Lifebuoy.

(a)   
![](images/42e42c95d48de43e1730235da6475c95675db0a103b42d1b64ae8a583296979d.jpg)



（C）

(b)   
![](images/26a7922a159b3056dbfc2a1497dae8196cf41d48f4a23cde3f5034400567ab46.jpg)



(d)

![](images/140f8a95af8d4859e603dab0c1f7a4f1c274d5870177766f0858a858f115b89e.jpg)



![](images/2d7bc9d5ec0dd433d1dac7706474dfc9bc5af045cbdaf373b65db19499c543a5.jpg)



FIGURE 11. (a) Original image, (b) degraded image, (c) restored by [13] + [9] method, (d) restored by the proposed algorithm.

(a)   
![](images/d5d430776eeda10f59cfe8d71a678895a938cb84998cf7c1c73bc29bcaaf96a2.jpg)



(b)   
![](images/c347beed30beb9c4695ad0c63ef294489e3303a9fba74c1c49d8e998a9e54f43.jpg)



（c）  
![](images/e09f9461eca976fd50e0eaba1dccf0b9f55ba37fc612f71c02ab71868b18f94a.jpg)



FIGURE 12. Close-ups of selected sections for Fig.11 of the original image, restored by [13 + 9] and our algorithm. (a) Original. (b) [13] + [9]. (c) Our Algorithm.

Comparing the experimental results visually, it is noticed that the proposed algorithm tends to produce images with more detailed information of the textures than [13] + [9]. Except PSNR and SSIM, the detailed information for part of the original and the restored images using two different algorithms are also amplified and demonstrated in Fig.12.

The achievement of the proposed method and [13] + [9] in the aspect of PSNR, SSIM, L2-error of identified kernel and eclipsed time improvements for these three color natural images are given in Table 6. It is obvious the proposed algorithm performs better than [13] + [9] method in terms of the edge information protection.

TABLE 6. Blind deblurring of natural color Fence image performance comparison. 

<table><tr><td>Fence\Method</td><td>[13] + [9]</td><td>Proposed Algorithm</td></tr><tr><td>SSIM</td><td>0.6266→0.6983</td><td>0.6266→0.9007</td></tr><tr><td>PSNR</td><td>15.5430→18.1674</td><td>15.5430→24.7198</td></tr><tr><td>L2 Error-Red</td><td>0.0034</td><td>0.0021</td></tr><tr><td>L2 Error-Green</td><td>0.0034</td><td>0.0021</td></tr><tr><td>L2 Error-Blue</td><td>0.0034</td><td>0.0026</td></tr><tr><td>Eclipse Time</td><td>56.5200</td><td>33.3839</td></tr></table>

L2-Error identified kernel profiles   
![](images/4575e580b28aca2f0525945cd1a3d5a2ad9ccbb5e6463b8c7e125d1020677c40.jpg)



FIGURE 13. Profiles for three channels about L2-Error of identified kernels.

TABLE 7. Blind deblurring of natural color images performance comparison. 

<table><tr><td rowspan="2">PSNR Blur</td><td rowspan="2">PSNR before</td><td colspan="2">PSNR after</td><td rowspan="2">SSIM before</td><td colspan="2">SSIM after</td></tr><tr><td>[13+9]</td><td>Proposed</td><td>[13+9]</td><td>Proposed</td></tr><tr><td>G (fence)</td><td>15.5430</td><td>18.1674</td><td>24.7198</td><td>0.6266</td><td>0.6983</td><td>0.9007</td></tr><tr><td>A (flag)</td><td>15.7676</td><td>18.9462</td><td>26.4884</td><td>0.7720</td><td>0.8431</td><td>0.9653</td></tr><tr><td>D (lifebuoy)</td><td>20.0350</td><td>21.6604</td><td>26.5644</td><td>0.8907</td><td>0.9095</td><td>0.9521</td></tr></table>

The profile of identified kernel’s L2-error for natural image Fence depicted in Fig. 13 demonstrated the convergence as the iteration proceeded. These three different identified kernel profiles mean that the restored kernel will enormously approach to the original one as the kernel being optimized step by step and finally reach the optimal solutions.

For different natural color images Fence, Flag and Lifebuoy, the improvement of PSNR and SSIM are listed in TABLE 7 and from the comparison results, we can see that the proposed algorithm demonstrated a better performance than [13] + [9].

# V. CONCLUSION

This paper presents a novel fast weighted algorithm for blind deconvolution to remove unknown blur as well as random noise. This methodology can synchronously restore image and identify kernel in a way that cannot be achieved by other recent algorithms. The performance of the improved algorithm relative to well-established deblurring methods in the literature has been demonstrated by applying it to a variety of gray-scale standard, natural, synthetic images and color images. In the evaluation standard about PSNR, SSIM and convergence time improvement, the proposed algorithm achieved better results than other algorithms.

# REFERENCES

[1] L. I. Rudin, S. Osher, and E. Fatemi, ‘‘Nonlinear total variation based noise removal algorithms,’’ Phys. D, Nonlinear Phenomena, vol. 60, nos. 1–4, pp. 259–268, 1992.   
[2] L. I. Rudin and S. Osher, ‘‘Total variation based image restoration with free local constraints,’’ in Proc. IEEE Int. Conf. Image Process. (ICIP), vol. 1. Nov. 1994, pp. 31–35.   
[3] C. R. Vogel and M. E. Oman, ‘‘Fast, robust total variation-based reconstruction of noisy, blurred images,’’ IEEE Trans. Image Process., vol. 7, no. 6, pp. 813–824, Jul. 1998.   
[4] M. K. P. Ng, R. H. Chan, and W.-C. Tang, ‘‘A fast algorithm for deblurring models with Neumann boundary conditions,’’ SIAM J. Sci. Comput., vol. 21, no. 3, pp. 851–866, 1999.   
[5] A. Beck and M. Teboulle, ‘‘A fast iterative shrinkage-thresholding algorithm for linear inverse problems,’’ SIAM J. Imag. Sci., vol. 2, no. 1, pp. 183–202, 2009.   
[6] H.-Y. Liu, W.-S. Lu, and M. Q.-H. Meng, ‘‘De-blurring wireless capsule endoscopy images by total variation minimization,’’ in Proc. IEEE Pacific Rim Conf. Commun., Comput. Signal Process. (PacRim), Aug. 2011, pp. 102–106.   
[7] H.-Y. Liu, W.-S. Lu, C.-J. Zhang, and Q.-H. Meng, ‘‘Research and application for fast restoration of color images algorithm based on total variation framework,’’ Acta Metallurgica Sinica, vol. 35, no. 6, pp. 1–5 2012.   
[8] Z.-J. Bai, D. Cassani, M. Donatelli, and S. Serra-Capizzano, ‘‘A fast alternating minimization algorithm for total variation deblurring without boundary artifacts,’’ J. Math. Anal. Appl., vol. 415, no. 1, pp. 373–393, Jul. 2014.   
[9] A. Beck and M. Teboulle, ‘‘Fast gradient-based algorithms for constrained total variation image denoising and deblurring problems,’’ IEEE Trans. Image Process., vol. 18, no. 11, pp. 2419–2434, Nov. 2009.   
[10] Y.-L. You and M. Kaveh, ‘‘A regularization approach to joint blur identification and image restoration,’’ IEEE Trans. Image Process., vol. 5, no. 3, pp. 416–428, Mar. 1996.   
[11] Y.-L. You and M. Kaveh, ‘‘Blind image restoration by anisotropic regularization,’’ IEEE Trans. Image Process., vol. 8, no. 3, pp. 396–407, Mar. 1999.   
[12] L. He, A. Marquina, and S. J. Osher, ‘‘Blind deconvolution using TV regularization and Bregman iteration,’’ Int. J. Imag. Syst. Technol., vol. 15, no. 1, pp. 74–83, 2005.   
[13] T. F. Chan and C.-K. Wong, ‘‘Total variation blind deconvolution,’’ IEEE Trans. Image Process., vol. 7, no. 3, pp. 370–375, Mar. 1998.   
[14] M. S. C. Almeida and L. B. Almeida, ‘‘Blind and semi-blind deblurring of natural images,’’ IEEE Trans. Image Process., vol. 19, no. 1, pp. 36–52, Jan. 2010.   
[15] T. F. Chan and C. K. Wong, ‘‘Convergence of the alternating minimization algorithm for blind deconvolution,’’ Linear Algebra Appl., vol. 316, nos. 1–3, pp. 259–285, Sep. 2000.   
[16] P. Getreuer, ‘‘Total variation deconvolution using split Bregman,’’ Image Process. OnLine, vol. 2, no. 1, pp. 158–174, 2012.   
[17] K. Ohkoshi, T. Goto, S. Hirano, and M. Sakurai, ‘‘Blind image restoration based on total variation regularization of blurred images,’’ in Proc. IEEE 1st Global Conf. Consum. Electron., Jan. 2012, pp. 621–622.   
[18] C. He, C. Hu, W. Zhang, B. Shi, and X. Hu, ‘‘Fast total-variation image deconvolution with adaptive parameter estimation via split Bregman method,’’ Math. Problems Eng., vol. 2014, Feb. 2014, Art. ID 617026. [Online]. Available: http://dx.doi.org/10.1155/2014/617026   
[19] E. J. Candès, J. Romberg, and T. Tao, ‘‘Robust uncertainty principles: Exact signal reconstruction from highly incomplete frequency information,’ IEEE Trans. Inf. Theory, vol. 52, no. 2, pp. 489–509, Feb. 2006.

[20] L. Fan, C. J. Louis, J. Wu, and H. Shu, ‘‘A new fast algorithm for constrained four-directional total variation image denoising problem,’’ Math. Problems Eng., vol. 2015, 2015, Art. ID 815132. [Online]. Available: http://dx.doi.org/10.1155/2015/815132   
[21] M. F. Fahmy, G. M. A. Raheem, U. S. Mohammed, and O. F. Fahmy, ‘‘A new total variation based image denoising and deblurring technique,’’ in Proc. Eur. Conf., Jul. 2013, pp. 1669–1675.   
[22] Z. Zuo, T. Zhang, X. Lan, and L. Yan, ‘‘An adaptive non-local total variation blind deconvolution employing split Bregman iteration,’’ Circuits, Syst., Signal Process., vol. 32, no. 5, pp. 2407–2421, Oct. 2013.   
[23] A. Ahmed, B. Recht, and J. Romberg, ‘‘Blind deconvolution using convex programming,’’ IEEE Trans. Inf. Theory, vol. 60, no. 3, pp. 1711–1732, Mar. 2014.   
[24] K. Shao, Y. Zou, Y. Liu, C. Li, and B. Fu, ‘‘Based on total variation regularization iterative blind image restoration algorithm,’’ Sensors Transducers, vol. 167, no. 3, pp. 36–42, 2014.   
[25] D. Krishnan, J. Bruna, and R. Fergus, ‘‘Blind deconvolution with re-weighted sparsity promotion,’’ CoRR, pp. 1–16, 2013.   
[26] L. Yan, H. Fang, and S. Zhong, ‘‘Blind image deconvolution with spatially adaptive total variation regularization,’’ Opt. Lett., vol. 37, no. 14, pp. 2778–2780, 2012.   
[27] F. Sroubek and P. Milanfar, ‘‘Robust multichannel blind deconvolution via fast alternating minimization,’’ IEEE Trans. Image Process., vol. 21, no. 4, pp. 1687–1700, Apr. 2012.   
[28] G. Gong, H. Zhang, and M. Yao, ‘‘Construction model for total variation regularization parameter,’’ Opt. Exp., vol. 22, no. 9, pp. 10500–10508, 2014.   
[29] S. Tang, W. Gong, W. Li, and W. Wang, ‘‘Non-blind image deblurring method by local and nonlocal total variation models,’’ Signal Process., vol. 94, pp. 339–349, Jan. 2014.   
[30] F. Dong, H. Zhang, and D.-X. Kong, ‘‘Nonlocal total variation models for multiplicative noise removal using split Bregman iteration,’’ Math. Comput. Model., vol. 55, nos. 3–4, pp. 939–954, Feb. 2012.   
[31] P. Rodríguez, ‘‘Total variation regularization algorithms for images corrupted with different noise models: A review,’’ J. Elect. Comput. Eng., vol. 2013, Jun. 2013, Art. ID 217021. [Online]. Available: http://dx.doi.org/10.1155/2013/217021   
[32] D. Perrone and P. Favaro, ‘‘Total variation blind deconvolution: The devil is in the details,’’ in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., Jun. 2014, pp. 2909–2916.   
[33] M. R. Renu, S. Chaudhuri, and R. Velmurugan, ‘‘Convergence analysis of a quadratic upper bounded TV regularizer based blind deconvolution,’’ Signal Process., vol. 106, pp. 174–183, Jan. 2015.   
[34] A. Kheradmand and P. Milanfar, ‘‘A general framework for regularized, similarity-based image restoration,’’ IEEE Trans. Image Process., vol. 23, no. 12, pp. 5136–5151, Dec. 2014.   
[35] G. Peyré, S. Bougleux, and L. D. Cohen, ‘‘Non-local regularization of inverse problems,’’ Inverse Problems Imag., vol. 5, no. 2, pp. 511–530, 2011.   
[36] A. Danielyan, V. Katkovnik, and K. Egiazarian, ‘‘BM3D frames and variational image deblurring,’’ IEEE Trans. Image Process., vol. 21, no. 4, pp. 1715–1728, Apr. 2012.

![](images/f5af82962e90918ad4cdbd32361c2088420b631425e636020225dd71a6c3e13f.jpg)



HAIYING LIU received the M.Sc. and Ph.D. degrees from the School of Control Science and Engineering, Shandong University. She was a Visiting Student with the Department of Electrical and Computer Engineering, University of Victoria, Canada. She conducts research as a Post-Doctoral Fellow with the Department of Electrical and Computer Engineering, Dalhousie University, Canada. Her research interests are mainly in the field of pattern recognition, digital image processing and computer vision, adaptive fuzzy controller design, and stability analysis with application in mobile robots.

![](images/f606fbad551adb68eb72c8f9af38b32274107192a98328fd909205c18d64fdce.jpg)



JASON GU received the bachelor’s degree in electrical engineering and information science from the University of Science and Technology of China, in 1992, the master’s degree in biomedical engineering from Shanghai Jiao Tong University, in 1995, and the Ph.D. degree from the University of Alberta, Canada, in 2001. He is currently a Full Professor of Electrical and Computer Engineering with Dalhousie University, Canada. He is also a Cross-Appointed Professor with the School of Biomedical Engineering for his multidisciplinary research work. He has over 19 years of research and teaching experience and has authored over 240 conference papers and articles. His research areas include robotics, biomedical engineering, rehabilitation engineering, neural networks, and control. He is a fellow of the Engineering Institute of Canada. He has been the Associate Editor of the Journal of Control and Intelligent Systems, Transactions of the Canadian Society for Mechanical Engineering, Canada, the IEEE TRANSACTIONS ON MECHATRONICS, the International Journal of Robotics and Automation, Unmanned Systems, the Journal of Engineering and Emerging Technologies, and the IEEE ACCESS.

![](images/e9954a2a1bfa7be8ba441648732558889e0cc1db7a83eaf0d3b76dd41e6e896c.jpg)



MAX Q.-H. MENG (F’08) received the Ph.D. degree in electrical and computer engineering from the University of Victoria, Canada, in 1992, and the M.Sc. degree in automatic control from the Beijing Institute of Technology, Beijing, China, in 1988. He was a Professor with the Department of Electrical and Computer Engineering, University of Alberta, Canada, from 1994 to 2004. He is currently a Professor with the Department of Electronic Engineering,

The Chinese University of Hong Kong.

![](images/8043eaa31c5aee567111fddb94f266db06627d60d7272efdfa4708ce1f095f6e.jpg)



WU-SHENG LU (LF’12) received the M.S. degree in electrical engineering and the Ph.D. degree in control science from the University of Minnesota, Minneapolis, USA, in 1983 and 1984, respectively. He was a Post-Doctoral Fellow with the University of Victoria, Victoria, BC, Canada, in 1985, and a Visiting Assistant Professor with the University of Minnesota from 1986 to 1987. He joined the Electrical and Computer Engineering Department, University of Victoria, in 1987, as an Associate

Professor, where he has been a Professor since 1991. He has co-authored the book entitled 2-D Digital Filters and Practical Optimization: Algorithms and Engineering Applications with A. Antoniou. His current research interests include analysis and design of digital filters, digital signal and image processing with a focus on sparse signal processing, and methods and applications of convex optimization. He is a fellow of the Engineering Institute of Canada.