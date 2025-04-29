# 🧠 OCR de Expressões Matemáticas com Gradio

Este projeto demonstra o uso de **OCR (Reconhecimento Óptico de Caracteres)** com a biblioteca `pytesseract` para identificar expressões matemáticas escritas em imagens. Utilizando uma interface interativa com **Gradio**, o sistema permite gerar expressões aleatórias, exibi-las em imagem, extrair o conteúdo com OCR, corrigir possíveis erros e avaliar o resultado final.

Além disso, o sistema realiza **validação estrutural das expressões utilizando conceitos de Gramática Livre de Contexto (GLC)**, garantindo que apenas expressões válidas sintaticamente sejam avaliadas.

---

## ⚙️ Funcionalidades

- Geração de uma **expressão matemática aleatória**.
- Criação de uma **imagem contendo essa expressão** (com ou sem ruído).
- Extração da expressão contida na imagem utilizando **OCR** com `pytesseract`.
- Correção de possíveis erros cometidos pelo OCR.
- Validação da expressão por meio de análise léxica.
- Avaliação da expressão com retorno do resultado final.
- Interface gráfica via **Gradio** com um botão interativo para iniciar o processo.

---

## 🖥️ Demonstração da Interface

A interface conta com:

- ✅ Um botão: **"Criar Expressão"**
- 🖼️ Uma imagem exibindo a expressão
- 🧠 O texto extraído e corrigido
- 🧮 O resultado da expressão avaliada

---

## 📦 Bibliotecas Necessárias

Antes de executar o projeto, certifique-se de instalar as seguintes dependências:

```bash
pip install gradio pillow pytesseract numpy

Cetifique-se de ter o tesseract instalado e inserido nas variáveis de ambiente.
