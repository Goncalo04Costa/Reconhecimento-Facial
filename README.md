# Reconhecimento Facial com DeepFace, OpenCV e SQL Server

Este projeto realiza **reconhecimento facial** em tempo real utilizando a webcam, comparando as faces com uma base de dados de pessoas, e exibindo informações como **nome**, **idade estimada** e **emoção dominante**.

## 🧠 Tecnologias Utilizadas

- [DeepFace](https://github.com/serengil/deepface) - Framework para análise facial (reconhecimento, idade, emoção, etc)
- [OpenCV](https://opencv.org/) - Captura de vídeo e processamento de imagem
- [pyodbc](https://github.com/mkleehammer/pyodbc) - Conexão com base de dados SQL Server
- SQL Server - Armazena nomes e caminhos das imagens das pessoas conhecidas

## 💡 Funcionalidades

- Captura vídeo em tempo real via webcam
- Analisa rostos detectados e exibe:
  - Nome da pessoa (se reconhecida)
  - Idade estimada
  - Emoção dominante
- Emoções representadas por cor na moldura da face
- Comparação de embeddings faciais com a base de dados
- Suporte a múltiplas imagens no banco de dados

## 📸 Base de Dados

A Base de dados deve conter uma tabela `Pessoas` com os seguintes campos:

| Nome       | CaminhoFoto                   |
|------------|-------------------------------|
| nome 1     | C:\\Imagens\\nome1.jpg        |
| nome 2     | C:\\Imagens\\nome2.jpg        |


Esta é apenas uma primeira versão do projeto, melhorias em breve


Gonçalo Costa

