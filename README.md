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
* `Q` e `T` - Esses dois botões acionam o modo de rotação automática: O cubo gira ao redor de todos os seus eixos, indefinidamente. `Q` aciona o modo de rotação, e `T` interrompe. Enquanto o cubo está em modo rotação, apenas o comando `F` pode ser utilizado ao mesmo tempo, portanto para manipular o cubo manualmente, interrompa o modo de rotação.
* `W, A, S, D, Z, X` - Esses comandos realizam a rotação manual do cubo, Sendo `W` e `S` os comandos para realizar a rotação do eixo X, `A` e `D` os comandos para a rotação do eixo Y, e `Z` e `X` para o eixo Z.
* `F` - Esse comando altera a distância focal `d` do cubo, dando um "zoom" nele. Pode ser usado independente do modo.
