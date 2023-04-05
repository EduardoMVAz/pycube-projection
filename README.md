# Pycube Projection
## Linear Algebra project with matrix manipulation and 3D to 2D transformations.

Developers:

* João Lucas de Moraes Barros Cadorniga [JoaoLucasMBC](https://github.com/JoaoLucasMBC)  
* Eduardo Mendes Vaz [EduardoMVaz](https://github.com/EduardoMVAz)

This repository is a Linear Algebra based project with which we learned to translate 3D environments and images to a 2D plane.

---

![caso o GIF não funciona, o vídeo mp4 se encontra na raiz do repositório](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTU1NGY0MzgwMjI3NWRiNmFlNmI0NzUyZTFiNWVhYzI0ZTMzNDcwMSZjdD1n/Ek6m9HMFfEwYS0Cbua/giphy.gif)

---

## Como Instalar

Para utilizar o projeto <em>"Pycube Projection"</em>, você deve ter o Python instalado em seu computador e seguir os passos:

1. Clone o repositório na sua máquina na pasta de sua escolha. Utilize o comando:

`git clone https://github.com/JoaoLucasMBC/pycube-projection.git`

2. Utilizando o terminal / a IDE de sua escolha, crie uma *Virtual Env* de Python e a ative:

`python -m venv env`

`env/Scripts/Activate.ps1` (Windows)

3. Mude para a pasta do <em>"Pycube Projection"</em> e instale as bibliotecas requeridas:

`cd ./pycube-projection`

`pip install -r requirements.txt`

4. Após a instalação, rode o arquivo *main.py* pelo terminal para acionar o projeto:

`python main.py`

---

## Como Manipular o Cubo

A manipulação do cubo pode ser feita a partir de alguns comandos:
* `Q` e `T` - Esses dois botões acionam o modo de rotação automática: o cubo gira ao redor de todos os seus eixos, indefinidamente (com incremento de 1 grau por segundo). `Q` aciona o modo de rotação, e `T` interrompe. Enquanto o cubo está em modo rotação, apenas o comando `F` pode ser utilizado ao mesmo tempo, portanto, para manipular o cubo manualmente, interrompa o modo de rotação.
* `W, A, S, D, Z, X` - Esses comandos realizam a rotação manual do cubo. `W` e `S` os comandos para realizar a rotação do eixo X, `A` e `D` os comandos para a rotação do eixo Y, e `Z` e `X` para o eixo Z.
* `F` - Esse comando altera a distância focal `d` do cubo, dando um "zoom" nele. Pode ser usado independente do modo.

*OBS: como as teclas de rotação apenas incrementam o ângulo da matriz de rotação, vale ressaltar, que, por exemplo, caso o usuário rotacione em 180° o cubo no eixo x, a rotação no eixo y estará com os controles invertidos. Ou seja, é necessário prestar atenção ao combinar rotações, pois elas alteram a direção que os eixos apontam.*

---

## Modelo Matemático

O modelo matemático do `pycube-rotation` é baseado inteiramente em **projeções** utilizando multiplicações matriciais. Como um cubo possui 3 dimensões, precisamos "achatá-lo", ou seja, projetar todas as coordenadas $x$ e $y$ para um $z$ fixo. Dessa maneira, é possível representar o cubo 3-d como um desenho 2-d na tela (utilizando a biblioteca `pygame`).

As projeções são realizadas respeitando um modelo baseado em câmeras *pinhole*, baseado na presença de um anteparo de coordeanda $z$ fixa (distância focal) que recebe as projeções dos pontos, que sempre passam pela origem (o pinhole), simulando o comportamento de raios de luz em câmeras.

O processo de transformação pode ser dividido em algumas etapas.

### 1. Projeção

Para os cálculos, podemos pensar separadamente em um primeiro momento: primeiro projetamos as coordeandas $x$ em um $z$ fixo, trabalhando com pares $(x_i, z_i)$, para o z de projeção $z_p = -d$ (distância focal negativa pois se encontra atrás do pinhole, a origem). Então, podemos pensar no mesmo processo para as coordenadas $y$, com pares $(y_i, z_i)$. 

Podemos realizar esse processo pois, realizando semelhanças entre os triângulos formados nos planos (feito no próximo passo), é possível constatar que as coordeandas de projeção, $x_p$ e $y_p$, não são dependente entre si, e são apenas influenciadas pela coordenada $z$ original,$z_0$, e a distância focal $d$.

#### 1.1. Semelhança de Triângulos

Ao formarmos triângulos retângulos conectando os pontos $(x_0, z_0)$ e $(x_p, z_p)$ a origem (usaremos pares $(x, z)$ como exemplo, o mesmo se aplica para $(y, z)$), formamos dois triângulos semelhantes, os quais podemos fazer a seguinte proporção entre seus catetos:

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

No entanto, como queremos utilizar multiplicações matriciais aplicadas as coordenadas originais para realizar esses cálculos, utilizamos de um artifício: reescrever $x_0$ em função de $x_p$ e $w_p$, o último sendo um fator que agrupa $z_0$ e $d$ e poderá, então, ser representado na nossa matriz de transformação:

$$
x_0 = -\frac{x_p * z_0}{d}
$$

$$
w_p = -\frac{z_0}{d}
$$

$$
\therefore x_0 = x_p * w_p
$$

Assim, podemos representar a nossa transformação das coordenadas $(x_0, z_0)$ em $(x_p, z_p)$:

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

Agora, realizando o mesmo processo para as coordeandas $x_p$ e $y_p$ separadamente, percebemos que o fator chave na transformação é o mesmo $w_p$. Portanto, podemos juntar as duas transformações e descrever com uma multiplicação matricial que gera todas as coordenadas de projeção com a matriz &P&:

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

Dessa maneira, a matriz de transformação no código é sempre calculada dessa maneira, de acordo com o valor de $d$ inputado no sistema.

### 2. Construção do cubo

Com a capacidade de montar as matrizes de projeção, precisamos imaginar a construção da matriz que representará os vértices do cubo e como ela será transformada.

Primeiro, facilitando o processo, o cubo é inicialmente construído ao redor da origem $(0, 0, 0)$, com arestas de tamanho 1. A matriz das suas coordenadas precisa de 4 linhas: uma para as coordenadas $x$, uma para as $y$, uma para as $z$ e uma de apenas 1's (para fazer a matriz que depende da dimensão extra $w$):

$$
C = \begin{bmatrix}
x_0 & x_1 & ... & x_n\\
y_0 & y_1 & ... & y_n \\
z_0 & z_1 & ... & z_n \\
1 & 1 & ... & 1
\end{bmatrix}
$$

Com essa matriz, podemos pré-multiplicá-la pela matriz de projeção $P$ para obter as coordenadas que serão mostradas pelo usuário.

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

Vale ressaltar que cada ângulo é incrementado em 1° por ciclo (na rotação automática). Além disso, apenas podemos realizar diretamente as rotações pois o cubo está centrado estratégicamente na origem, e as matrizes de transformação sempre ocorrem ao redor do $(0, 0, 0)$

As aplicando na matriz de cubo $C$:

$$
C = R_z R_y R_x C
$$

Após essa ação, é preciso transladar a coordenada $z$, pois $z = 0$ é reservado para o pinhole, e não seria possível realizar a projeção. Foi arbitrariamente escolhido um incremento de 5 para todas os pontos.

Agora, podemos realizar nossa projeção utilizando $P$:

$$
C_p = PC
$$

### 4. Construção das Coordenadas

Com a matriz projetada $C_p$ em mãos, precisamos tomar cuidado: ainda não temos em mãos as coordenadas $(x_p, y_p)$, pois a nossa matriz possui apenas $x_p * w_p$ e $y_p * w_p$, como indicado abaixo:

$$
C_p = \begin{bmatrix}
x^{0}_p * w^{0}_p & x^{1}_p * w^{1}_p & ... & x^{7}_p * w^{7}_p\\
y^{0}_p * w^{0}_p & y^{1}_p * w^{1}_p & ... & y^{7}_p * w^{7}_p \\
z_p & z_p & ... & z_p \\
w^{0}_p & w^{1}_p & ... & w^{7}_p
\end{bmatrix}
$$

Portanto, precisamos dividir todas as linhas da nossa matriz pela última linha, "normalizando-a" e obtendo as coordenadas $x$ e $y$.

Agora, podemos extrair apenas o que nos interessa, os pares $(x, y)$ de interesse das duas primeiras linhas, e adicionar coordenadas homogêneas para realizarmos as translações necessárias nos próximos passos, obtendo uma matriz $8x3$ (8 vértices e 3 coordenadas para cada):

$$
C_p = \begin{bmatrix}
x^{0}_p & x^{1}_p & ... & x^{7}_p \\
y^{0}_p & y^{1}_p & ... & y^{7}_p \\
1 & 1 & ... & 1
\end{bmatrix}
$$

No entanto, o nosso cubo ainda é muito pequeno para ser observado na tela e está centrado na origem no sistema de coordenadas. Portanto, vamos aplicar uma matriz de expansão $E$ que multiplica as coordenadas por `400`, e uma matriz de translação $T$ que movimenta a matriz para o centro da tela ($W$ é a width da tela e $L$ o length):

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

### 5. Variando a distância focal

É importante realizar algumas observações sobre a distância focal
