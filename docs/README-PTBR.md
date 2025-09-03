## Como Instalar

Para utilizar o projeto <em>"Pycube Projection"</em>, você deve ter o Python instalado em seu computador e seguir os passos:

1. Clone o repositório na sua máquina na pasta de sua escolha. Utilize o comando:

`git clone https://github.com/JoaoLucasMBC/pycube-projection.git`

2. Utilizando o terminal / a IDE de sua escolha, crie uma *Virtual Env* de Python e a ative:

- Using python environments:

        python -m venv <ENVIRONMENT-NAME>

        <ENVIRONMENT-NAME>/Scripts/Activate.ps1 (Windows)

        source <ENVIRONMENT-NAME>/bin/activate (Linux e MacOS)

- Using uv:

        uv venv <ENVIRONMENT-NAME> --python 3.13

        <ENVIRONMENT-NAME>/Scripts/activate (Windows)

        source <ENVIRONMENT-NAME>/bin/activate (Linux e MacOS)

3. Mude para a pasta do <em>"Pycube Projection"</em> e instale as bibliotecas requeridas:

`cd ./pycube-projection`

`pip install -r requirements.txt (venv)`

`uv pip install -r requirements.txt (uv)`

4. Após a instalação, rode o arquivo *main.py* pelo terminal para acionar o projeto:

`python src/main.py (Windows)`

`python3 src/main.py (Linux e MacOS)`

---

## Como Manipular o Cubo

A manipulação do cubo pode ser feita a partir de alguns comandos:
* `Q` e `T` - Esses dois botões acionam o modo de rotação automática: o cubo gira ao redor de todos os seus eixos, indefinidamente (com incremento de 1 grau por loop). `Q` aciona o modo de rotação, e `T` o interrompe. Enquanto o cubo está em modo rotação, apenas o comando `Mouse Scroll` pode ser utilizado simultaneamente, portanto, para manipular o cubo manualmente, interrompa o modo de rotação.
* `W, A, S, D, Z, X` - Esses comandos realizam a rotação manual do cubo. `W` e `S` os comandos para realizar a rotação do eixo $x$, `A` e `D` os comandos para a rotação do eixo $y$, e `Z` e `X` para o eixo $z$.
* `Mouse Scroll` - O scroll do mouse altera a distância focal `d` do cubo, dando um "zoom in" ou "zoom out" nele. O scroll para cima aumenta d, "zoom in", e o scroll para baixo diminui d, "zoom out". (Um mouse externo e um scroll de notebook são invertidos)

*OBS: como as teclas de rotação apenas incrementam o ângulo da matriz de rotação, vale ressaltar, que, por exemplo, caso o usuário rotacione em 180° o cubo no eixo x, a rotação no eixo y estará com os controles invertidos. Ou seja, é necessário prestar atenção ao combinar rotações, pois elas alteram a direção que os eixos apontam.*
