---
layout: default
title: Documentation
---

# Mathematical Model

The mathematical model of `pycube-rotation` is entirely based on **projections** using matrix multiplications. Since a cube has 3 dimensions, we need to "flatten" it, i.e., project all $x$ and $y$ coordinates to a fixed $z$. This way, it is possible to represent the 3D cube as a 2D drawing on the screen (using the `pygame` library).

The projections are carried out according to a *pinhole* camera model, based on the presence of a fixed $z$ coordinate plane (focal length) that receives the projection of the points, which always pass through the origin (the pinhole), simulating the behavior of light rays in cameras.

The transformation process can be divided into several steps.

<br/>

## 1. Projection

For the calculations, we can initially think separately: first, we project the $x$ coordinates to a fixed $z$, working with pairs $(x_i, z_i)$, for the projection $z_p = -d$ (the focal length needs to be multiplied by $-1$, since it is absolute and the "screen" is located behind the pinhole, the origin). Then, we can apply the same process for the $y$ coordinates, with pairs $(y_i, z_i)$.

This process is possible because, by analyzing the similarity of the triangles formed in the planes (done in the next step), we can see that the projection coordinates $x_p$ and $y_p$ are not dependent on each other, and are only influenced by the original $z$ coordinate ($z_0$) and the focal length $d$.

### 1.1. Triangle Similarity

By forming right triangles connecting the points $(x_0, z_0)$ and $(x_p, z_p)$ to the origin (we use pairs $(x, z)$ as an example, but the same applies to $(y_0, z_0)$), we form two similar triangles, which therefore have the following proportion between their sides:

$$  
\frac{x_0}{z_0} = \frac{x_p}{z_p}
$$

Substituting $z_p = -d$ and isolating $x_p$:

$$
\frac{x_0}{z_0} = -\frac{x_p}{d}  
$$

$$
x_p = -\frac{d * x_0}{z_0}
$$

However, since we want to use matrix multiplications applied to the original coordinates to obtain the projection coordinates, we use a mathematical trick: rewrite $x_0$ in terms of $x_p$ and $w_p$, the latter being a factor depending on $z_0$ and $d$, which can then be represented in our transformation matrix:

$$
x_0 = -\frac{x_p * z_0}{d}
$$

$$
w_p = -\frac{z_0}{d}
$$

$$
	\therefore x_0 = x_p * w_p
$$

Thus, we can represent our transformation from coordinates $(x_0, z_0)$ to $(x_p, z_p)$ as:

$$
\begin{bmatrix}
1 & 0 & 0\\
0 & 0 & -d \\
0 & rac{-1}{d} & 0
\end{bmatrix}
\begin{bmatrix}
x_0 \\
z_0 \\
1
\end{bmatrix} = 
\begin{bmatrix}
x_p * w_p \\
z_p \\
w_p
\end{bmatrix}
$$

### 1.2. Combining $x$ and $y$

Now, applying the process for both $x_p$ and $y_p$ separately, we notice that the key factor in the transformation is the same: $w_p$. Therefore, we can combine the two transformations and describe them with a single matrix multiplication that generates all projection coordinates with matrix $P$:

$$
P = \begin{bmatrix}
1 & 0 & 0 & 0\\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & -d \\
0 & 0 & \frac{-1}{d} & 0
\end{bmatrix}
$$

$$
\begin{bmatrix}
x_p * w_p \\
y_p * w_p\\
z_p \\
w_p
\end{bmatrix} = P
\begin{bmatrix}
x_0 \\
y_0 \\
z_0 \\
1
\end{bmatrix}
$$

This way, the transformation matrix in the code is always calculated in the same way, depending on the value of $d$ input into the system.

<br/>

## 2. Cube Construction

With the ability to build projection matrices, we need to consider how to construct the matrix representing the cube's vertices and how it will be transformed before applying the projection.

First, to simplify processing, the cube is initially built around the origin $(0, 0, 0)$, with edges of length 1. The coordinate matrix requires 4 rows: one for the $x$ coordinates, one for $y$, one for $z$, and one of all 1’s (so we can multiply by matrix $P$ which depends on the extra $w$ dimension):

$$
C = \begin{bmatrix}
x_0 & x_1 & ... & x_n\\
y_0 & y_1 & ... & y_n \\
z_0 & z_1 & ... & z_n \\
1 & 1 & ... & 1
\end{bmatrix}
$$

With this matrix, we can pre-multiply it by the projection matrix $P$ to obtain the coordinates displayed to the user.

<br/>

## 3. Rotation

However, before projecting from 3D to 2D, we need to rotate our system in 3D space. For this, we generate specific matrices for rotations around each axis separately, $R_x$, $R_y$, and $R_z$:

$$
R_x = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & \cos(	heta) & -\sin(	heta) & 0 \\
0 & \sin(	heta) & \cos(	heta) & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\hspace{0.5in}
R_y = \begin{bmatrix}
\cos(	heta) & 0 & \sin(	heta) & 0 \\
0 & 1 & 0 & 0 \\
-\sin(	heta) & 0 & \cos(	heta) & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\hspace{0.5in}
R_z = \begin{bmatrix}
\cos(	heta) & - \sin(	heta) & 0 & 0 \\
\sin(	heta) & \cos(	heta) & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

*Note:* $	heta$ *represents the rotation angle, which in the program is separated for each axis.*

It is worth noting that each angle is incremented by 1° per cycle (in automatic rotation). Furthermore, we can apply rotations directly because the cube is strategically centered at the origin, and transformation matrices always act centered at the origin $(0, 0, 0)$.

Applying them to the cube matrix $C$:

$$
C = R_z R_y R_x C
$$

After this, it is necessary to translate the $z$ coordinate, since $z = 0$ is reserved for the pinhole, and projection would not be possible. An arbitrary increment of 5 is chosen for all points.

Now, we can apply our projection using $P$:

$$
C_p = PC
$$

<br/>

## 4. Coordinate Construction

With the projected matrix $C_p$ in hand, we need to be careful: we do not yet have the $(x_p, y_p)$ coordinates, since our matrix only contains $x_p * w_p$ and $y_p * w_p$, as shown below:

$$
C_p = \begin{bmatrix}
x^{0}_p * w^{0}_p & x^{1}_p * w^{1}_p & ... & x^{7}_p * w^{7}_p\\
y^{0}_p * w^{0}_p & y^{1}_p * w^{1}_p & ... & y^{7}_p * w^{7}_p \\
z_p & z_p & ... & z_p \\
w^{0}_p & w^{1}_p & ... & w^{7}_p
\end{bmatrix}
$$

Therefore, we must divide all rows of our matrix by the last row (with $w_p$ values), "normalizing" it and obtaining the $x_p$ and $y_p$ coordinates.

Now, we can extract only what we need, the $(x, y)$ pairs of interest from the first two rows, and add homogeneous coordinates to perform the necessary translations in the next steps, obtaining an $8x3$ matrix (8 vertices and 3 coordinates each):

$$
C_p = \begin{bmatrix}
x^{0}_p & x^{1}_p & ... & x^{7}_p \\
y^{0}_p & y^{1}_p & ... & y^{7}_p \\
1 & 1 & ... & 1
\end{bmatrix}
$$

However, our cube is still too small to be observed on the screen and is centered at the coordinate system origin. Therefore, we apply a scaling matrix $E$ that multiplies the coordinates by `400` and a translation matrix $T$ that moves the matrix to the screen center ($W$ is the screen *width* and $L$ the *length*):

$$
E = \begin{bmatrix}
400 & 0 & 0\\
0 & 400 & 0\\
0 & 0 & 1
\end{bmatrix},
\hspace{0.5in}
T = \begin{bmatrix}
1 & 0 & (W/2)\\
0 & 1 & (L/2)\\
0 & 0 & 1
\end{bmatrix}
$$  

$$
C_p = T E C_p
$$

Finally, to obtain the coordinates of each point, we can transpose the matrix so that each row corresponds to the coordinates of one vertex.

*Note: a validation is performed to avoid glitches. When changing the focal length $d$, some coordinates may become negative. In this case, the point is not drawn on the screen.*

<br/>

## 5. Varying the Focal Length

It is important to make some remarks about the focal length and its role in the mathematical model.

The focal length represents the distance between the *pinhole* (origin) and our "screen", i.e., the fixed $z$ coordinate where we want to project our points. Therefore, it is absolute, always positive. For implementation purposes, we decided that all cube points are at positive $z$, and therefore must be projected onto a negative $z$.

Thus, when calculating the projection matrix, we always set $z_p = -d$, which causes the negative sign to appear in the matrix calculations. Furthermore, to avoid *glitches*, a validation prevents the focal length from becoming negative, which would cause $z_p > 0$ and make it impossible for the projection to pass through the pinhole.