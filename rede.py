import re
import pytesseract
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random
import gradio as gr

# ============ 1. GERAR EXPRESSÃO ============

def gerar_expressao_aleatoria():
    operadores = ['+', '-', '*', '/']
    expr = f"{random.randint(1, 9)} {random.choice(operadores)} {random.randint(1, 9)}"
    if random.random() < 0.5:
        expr = f"{random.randint(1, 9)} {random.choice(operadores)} ({expr})"
    return expr

def gerar_imagem_sem_ruido(caminho='expressao_ocr.png'):
    expressao = gerar_expressao_aleatoria()
    largura, altura = 300, 100
    imagem = Image.new('RGB', (largura, altura), color='white')
    draw = ImageDraw.Draw(imagem)

    try:
        fonte = ImageFont.truetype("arial.ttf", 36)
    except:
        fonte = ImageFont.load_default()
    
    # Adicionar ruído à imagem
    pixels = imagem.load()  # Obtém acesso direto aos pixels da imagem
    for i in range(largura):
        for j in range(altura):
            # Adiciona ruído em um percentual de pixels
            if random.random() < 0.1:  # 10% dos pixels terão ruído
                # Gera um valor de cor aleatório (ruído)
                pixels[i, j] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    draw.text((10, 30), expressao, font=fonte, fill='black')
    imagem.save(caminho)
    return expressao, imagem

# ============ 2. OCR ============

def preprocessar_imagem(imagem):
    imagem = imagem.convert('L')
    imagem = imagem.point(lambda p: p > 200 and 255)
    imagem = imagem.filter(ImageFilter.MedianFilter(3))
    return imagem

def extrair_texto_ocr(caminho_imagem):
    imagem = Image.open(caminho_imagem)
    imagem = preprocessar_imagem(imagem)
    texto = pytesseract.image_to_string(imagem, config='--psm 6 --oem 3')
    return texto.strip()

# ============ 3. CORREÇÃO OCR ============

CORRECAO_OCR = {
    'O': '0', 'o': '0', 'l': '1', 'I': '1', '|': '1',
    'B': '8', 'S': '5', 's': '5', 'Z': '2', ' ': '',
    'a': '', 'e': '', 'n': '',
    '+': '+', '-': '-', '*': '*', '/': '/',
    '(': '(', ')': ')', '.': '.', ',': '', '=': '='
}

def corrigir_expressao(expressao):
    return ''.join(CORRECAO_OCR.get(c, c) for c in expressao)

# ============ 4. AVALIAÇÃO ============

def validar_expressao(expr):
    padrao = r'^[\d+\-*/().]+$'
    return re.fullmatch(padrao, expr) is not None

def avaliar_expressao(expr):
    try:
        return eval(expr)
    except Exception as e:
        return f"Erro ao avaliar: {e}"

# ============ 5. FUNÇÃO PRINCIPAL ============

def fluxo_gradio():
    caminho = 'expressao_ocr.png'
    expressao_original, imagem = gerar_imagem_sem_ruido(caminho)
    texto_ocr = extrair_texto_ocr(caminho)
    texto_corrigido = corrigir_expressao(texto_ocr)

    if validar_expressao(texto_corrigido):
        resultado = avaliar_expressao(texto_corrigido)
    else:
        resultado = "Expressão inválida mesmo após correção."

    return imagem, texto_ocr, texto_corrigido, str(resultado)

# ============ 6. INTERFACE GRADIO ============

interface = gr.Interface(
    fn=fluxo_gradio,
    inputs=[],
    outputs=[
        gr.Image(type="pil", label="Imagem com Expressão"),
        gr.Textbox(label="Texto Extraído pelo OCR"),
        gr.Textbox(label="Expressão Corrigida"),
        gr.Textbox(label="Resultado da Expressão")
    ],
    title="Leitor de Expressão com OCR",
    description="Clique no botão para gerar uma expressão aleatória, extrair com OCR e ver o resultado."
)

interface.launch()
