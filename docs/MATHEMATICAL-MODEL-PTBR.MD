## Modelo Matemático

O modelo matemático do `pycube-rotation` é baseado inteiramente em **projeções** utilizando multiplicações matriciais. Como um cubo possui 3 dimensões, precisamos "achatá-lo", ou seja, projetar todas as coordenadas $x$ e $y$ para um $z$ fixo. Dessa maneira, é possível representar o cubo 3-d como um desenho 2-d na tela (utilizando a biblioteca `pygame`).

As projeções são realizadas respeitando um modelo de câmeras *pinhole*, baseado na presença de um anteparo de coordeanda $z$ fixa (distância focal) que recebe as projeções dos pontos, que sempre passam pela origem (o pinhole), simulando o comportamento de raios de luz em câmeras.

O processo de transformação pode ser dividido em algumas etapas.

<br/>

### 1. Projeção

Para os cálculos, podemos, em um primeiro momento, pensar separadamente: primeiro, projetamos as coordeandas $x$ em um $z$ fixo, trabalhando com pares $(x_i, z_i)$, para o z de projeção $z_p = -d$ (distância focal precisa ser multiplicada por $-1$, pois ela é absoluta e o "anteparo" se encontra atrás do pinhole, a origem). Então, podemos pensar no mesmo processo para as coordenadas $y$, com pares $(y_i, z_i)$. 

Esse processo é possível pois, realizando semelhanças entre os triângulos formados nos planos (feito no próximo passo), é possível constatar que as coordeandas de projeção, $x_p$ e $y_p$, não são dependentes entre si, e são apenas influenciadas pela coordenada $z$ original ($z_0$) e a distância focal $d$.

#### 1.1. Semelhança de Triângulos

Ao formarmos triângulos retângulos conectando os pontos $(x_0, z_0)$ e $(x_p, z_p)$ a origem (usaremos pares $(x, z)$ como exemplo, mas o mesmo se aplica para $(y_0, z_0)$), formamos dois triângulos semelhantes, os quais, portanto, possuem a seguinte proporção entre seus catetos:

$$  
\frac{x_0}{z_0} = \frac{x_p}{z_p}
$$

Substituindo $z_p = -d$ e isolando $y_p$:

$$
\frac{x_0}{z_0} = -\frac{x_p}{d}  
$$

$$
x_p = -\frac{d * x_0}{z_0}
$$

No entanto, como queremos utilizar multiplicações matriciais aplicadas as coordenadas originais para realizar os cálculos que resultam nas coordenadas de projeção, utilizamos de um artifício matemático: reescrever $x_0$ em função de $x_p$ e $w_p$, o último sendo um fator em função de $z_0$ e $d$ e poderá, então, ser representado na nossa matriz de transformação:

$$
x_0 = -\frac{x_p * z_0}{d}
$$

$$
w_p = -\frac{z_0}{d}
$$

$$
\therefore x_0 = x_p * w_p
$$

Assim, podemos representar a nossa transformação das coordenadas $(x_0, z_0)$ para $(x_p, z_p)$:

$$
\begin{bmatrix}
1 & 0 & 0\\
0 & 0 & -d \\
0 & \frac{-1}{d} & 0
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

#### 1.2. Unindo $x$ e $y$

Agora, realizando o processo para as coordeandas $x_p$ e $y_p$ separadamente, percebemos que o fator chave na transformação é o mesmo: $w_p$. Portanto, podemos juntar as duas transformações e descrevê-las com apenas uma multiplicação matricial que gera todas as coordenadas de projeção com a matriz &P&:

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

Dessa maneira, a matriz de transformação no código é sempre calculada da mesma maneira, de acordo com o valor de $d$ inputado no sistema.

<br/>

### 2. Construção do cubo

Com a capacidade de montar as matrizes de projeção, precisamos imaginar a construção da matriz que representará os vértices do cubo e como ela será transformada antes de realizar o processo.

Primeiro, facilitando o processamento, o cubo é inicialmente construído ao redor da origem $(0, 0, 0)$, com arestas de tamanho 1. A matriz das suas coordenadas precisa de 4 linhas: uma para as coordenadas $x$, uma para as $y$, uma para as $z$ e uma de apenas 1's (para podermos multiplicar pela matriz $P$ que depende da dimensão extra $w$):

$$
C = \begin{bmatrix}
x_0 & x_1 & ... & x_n\\
y_0 & y_1 & ... & y_n \\
z_0 & z_1 & ... & z_n \\
1 & 1 & ... & 1
\end{bmatrix}
$$

Com essa matriz em mãos, podemos pré-multiplicá-la pela matriz de projeção $P$ para obter as coordenadas que serão mostradas para o usuário.

<br/>

### 3. Rotação

No entanto, antes de realizarmos a projeção de 3-d para 2-d, precisamos realizar as rotações no nosso sistema tridimensional. Para isso, geramos matrizes específicas para as rotações ao redor de cada eixo separadamente, $R_x$, $R_y$ e $R_z$:

$$
R_x = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & \cos(\theta) & -\sin(\theta) & 0 \\
0 & \sin(\theta) & \cos(\theta) & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\hspace{0.5in}
R_y = \begin{bmatrix}
\cos(\theta) & 0 & \sin(\theta) & 0 \\
0 & 1 & 0 & 0 \\
-\sin(\theta) & 0 & \cos(\theta) & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\hspace{0.5in}
R_z = \begin{bmatrix}
\cos(\theta) & - \sin(\theta) & 0 & 0 \\
\sin(\theta) & \cos(\theta) & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

*OBS:* $\theta$ *representa o ângulo da rotação, que no programa é separado para cada eixo.*

Vale ressaltar que cada ângulo é incrementado em 1° por ciclo (na rotação automática). Além disso, apenas podemos realizar diretamente as rotações pois o cubo está centrado estratégicamente na origem, e as matrizes de transformação sempre atuam centradas na origem, $(0, 0, 0)$

As aplicando na matriz de cubo $C$:

$$
C = R_z R_y R_x C
$$

Após essa ação, é preciso transladar a coordenada $z$, pois $z = 0$ é reservado para o pinhole, e não seria possível realizar a projeção. Foi arbitrariamente escolhido um incremento de 5 para todas os pontos.

Agora, podemos realizar nossa projeção utilizando $P$:

$$
C_p = PC
$$

<br/>

### 4. Construção das Coordenadas

Com a matriz projetada $C_p$ em mãos, precisamos tomar cuidado: ainda não possuimos as coordenadas $(x_p, y_p)$, pois a nossa matriz possui apenas $x_p * w_p$ e $y_p * w_p$, como indicado abaixo:

$$
C_p = \begin{bmatrix}
x^{0}_p * w^{0}_p & x^{1}_p * w^{1}_p & ... & x^{7}_p * w^{7}_p\\
y^{0}_p * w^{0}_p & y^{1}_p * w^{1}_p & ... & y^{7}_p * w^{7}_p \\
z_p & z_p & ... & z_p \\
w^{0}_p & w^{1}_p & ... & w^{7}_p
\end{bmatrix}
$$

Portanto, precisamos dividir todas as linhas da nossa matriz pela última linha (com os valores de $w_p$), "normalizando-a" e obtendo as coordenadas $x_p$ e $y_p$.

Agora, podemos extrair apenas o que nos interessa, os pares $(x, y)$ de interesse das duas primeiras linhas, e adicionar coordenadas homogêneas para realizarmos as translações necessárias nos próximos passos, obtendo uma matriz $8x3$ (8 vértices e 3 coordenadas para cada):

$$
C_p = \begin{bmatrix}
x^{0}_p & x^{1}_p & ... & x^{7}_p \\
y^{0}_p & y^{1}_p & ... & y^{7}_p \\
1 & 1 & ... & 1
\end{bmatrix}
$$

No entanto, o nosso cubo ainda é muito pequeno para ser observado na tela e está centrado na origem no sistema de coordenadas. Portanto, vamos aplicar uma matriz de expansão $E$ que multiplica as coordenadas por `400` e uma matriz de translação $T$ que movimenta a matriz para o centro da tela ($W$ é a *width* da tela e $L$ o *length*):

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

Por fim, para termos as coordenadas de cada ponto, podemos transpor a matriz, de modo que cada linha correspode às coordenadas de um vértice.

*OBS: vale ressaltar que é realizada uma validação para evitar glitches. Ao alterar a distância focal* $d$, *é possível que algumas coordenadas acabem sendo negativas. Portanto, caso isso ocorra, o ponto não é desenhado na tela.*

<br/>

### 5. Variando a distância focal

É importante realizar algumas observações sobre a distância focal e o seu funcionamento no modelo matemático. 

A distância focal representa a distância entre o *pinhole* (origem) e o nosso "anteparo", isto é, a coordenada $z$ fixa na qual queremos os nossos pontos projetados. Portanto, ela é absoluta, sempre positiva. Por decisão de implementação, decidimos que todos os pontos do cubo estarão em $z$ positivos, e, portanto, devem ser projetados em um $z$ negativo. 

Dessa maneira, ao calcular a matriz de projeção, sempre calculamos $z_p = -d$, o que causa o sinal de negativo aparecer no cálculo das matrizes. Além disso, para evitar *glitches*, foi feita uma validação que impede que a distância focal se torne negativa, o que causaria que $z_p > 0$ e impediria a projeção passar pelo pinhole.