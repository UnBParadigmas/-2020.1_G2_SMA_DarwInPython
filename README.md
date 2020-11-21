# DarwInPython

**Disciplina**: FGA0210 - PARADIGMAS DE PROGRAMAÇÃO - T03 <br>
**Nro do Grupo**: 02<br>
**Paradigma**: SMA<br>

## Alunos

| Matrícula  | Aluno                        |
| ---------- | ---------------------------- |
| 16/0124581 | Hugo Aragão de Oliveira      |
| 16/0123186 | Guilherme Guy de Andrade     |
| 16/0121612 | Gabriela Barrozo Guedes      |
| 15/0135521 | Leonardo dos S. S. Barreiros |

## Sobre

O projeto DarwInPython foi desenvolvido pelo corpo discente da disciplina de Paradigmas de Programação no ano de 2020 pela Universidade de Brasília. 

O projeto utiliza os Paradigmas Sistemas Multi-Agentes e Concorrentes para simular uma cadeia alimentar. Com ele é possivel ver as ações de Cenouras, Coelhos e Lobos em um campo, onde ocorrem as interações da cadeia alimentar (Coelhos comem Cenouras e Lobos caçam Coelhos). Também existe um mecanismo de reprodução entre animais de mesma espécie com base no nível de 'fome'.

## Screenshots

<!-- [Inicio do game](images/) -->
<!-- [Após interações](images/) -->

## Instalação

**Linguagens**: Python 3.7<br>
**Tecnologias**: Bibliotecas Pade e Pygame<br>

#### Instalação para rodar o programa sem Docker

Para executar o programa é necessário ter Python 3.7 instalado, assim como o Pip. Recomendamos a utilização de um `virtualenv`.

Para fazer as instalações das bibliotecas utilizadas rode o comando abaixo:

```sh
pip install -r requirements
```

## Uso

#### Rodando o programa com Docker

Para executar o programa utilizando Docker, rode os seguintes comandos:

```sh
// Permitir conexão com o servidor X da máquina (Ubuntu)
xhost +

// caso sucesso você verá:
$ access control disabled, clients can connect from any host

// a seguir execute
docker-compose up
```

**OBS.:** Essa forma de rodar com o docker funciona somente no **Ubuntu**.

#### Rodando o programa sem Docker

Para rodar o programa sem Docker, faça a instalação das bibliotecas utilizando o `pip`, e em seguida rode o comando:

```sh
pade create-pade-db
pade start-runtime --config_file config.json
```

## Vídeo

O Vídeo da apresentação está disponível abaixo:

[<img src="https://img.youtube.com/vi/Y3r-QRjGB8Q/maxresdefault.jpg">](https://youtu.be/Y3r-QRjGB8Q)

## Outros

Quaisquer outras informações sobre seu projeto podem ser descritas a seguir.

## Fontes

Caso utilize materiais de terceiros, referencie-os adequadamente.
