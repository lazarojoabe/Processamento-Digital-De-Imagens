import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

def aplica_gauss_e_otsu(pastaOrigem, pastaDestino):
    arq = os.listdir(pastaOrigem)

    for i in arq:
        # Verificando se o que está sendo lido é uma imagem desejada
        caminho_origem = os.path.join(pastaOrigem, i)
        img = cv2.imread(caminho_origem, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Erro ao ler a imagem: {caminho_origem}")
        else:
            print(f"Imagem lida com sucesso: {caminho_origem}")

            gaussiana = cv2.GaussianBlur(img, (3, 3), 1)
            _, otsu = cv2.threshold(gaussiana, 175, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            cv2.imwrite(os.path.join(pastaDestino, f"{i}"), otsu)

def aplica_roberts(img):
    # Converte a imagem para escala de cinza, se necessário
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplica o operador Roberts
    roberts_x = cv2.filter2D(img_gray, cv2.CV_64F, np.array([[1, 0], [0, -1]]))
    roberts_y = cv2.filter2D(img_gray, cv2.CV_64F, np.array([[0, 1], [-1, 0]]))

    # Calcula a magnitude dos gradientes
    magnitude = cv2.magnitude(roberts_x, roberts_y)

    # Normaliza a magnitude para valores entre 0 e 255
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

    # Converte para o tipo uint8 e aplica uma operação de limiarização para obter uma imagem binária
    _, magnitude_bin = cv2.threshold(np.uint8(magnitude), 0, 255, cv2.THRESH_BINARY)

    return magnitude_bin

def contorna_bordas(img):
    roberts = aplica_roberts(img)
    contours, _ = cv2.findContours(roberts, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_contornada = cv2.drawContours(np.zeros_like(img), contours, -1, (0, 255, 0), 3) 
    return img_contornada

def sobrepoe_imagens(pastaLimiarizadas, pastaOriginais, pastaDestino):
    img_originais = os.listdir(pastaOriginais)
    img_limiarizadas = os.listdir(pastaLimiarizadas)

    for img in img_originais:
        if img in img_limiarizadas:
            img_original = cv2.imread(os.path.join(pastaOriginais, img))
            img_limiarizada = cv2.imread(os.path.join(pastaLimiarizadas, img))
            # Redimensiona a imagem limiarizada se necessário
            # if img_original.shape[:2] != img_limiarizada.shape[:2]:
            #     img_limiarizada = cv2.resize(img_limiarizada, (img_original.shape[1], img_original.shape[0]))

            img_contornada = contorna_bordas(img_limiarizada)

            # Sobrepõe as imagens
            newImg = cv2.addWeighted(img_original, 0.7, img_contornada, 0.3, 0)

            # Salva a imagem resultante na pasta de destino
            cv2.imwrite(os.path.join(pastaDestino, f"{img}"), newImg)

# pasta_origem_notebook = "C:/Users/lazar/OneDrive/Documentos/Iniciacao Cientifica/Processamento-Digital-De-Imagens/CgToll10B"
# pasta_destino_notebook = "C:/Users/lazar/OneDrive/Documentos/Iniciacao Cientifica/Processamento-Digital-De-Imagens/suavizacao_e_otsu"
# pasta_destino_contornadas_notebook = "C:/Users/lazar/OneDrive/Documentos/Iniciacao Cientifica/Processamento-Digital-De-Imagens/imagens_sobrepostas"

# pasta_destino_pc = "suavizacao_e_otsu"
# pasta_origem_pc = "CgToll10B"
# pasta_destino_contornadas_pc = "imagens_sobrepostas_pc"
#aplica_gauss_e_otsu(pasta_origem_notebook, pasta_destino_notebook)

#sobrepoe_imagens(pasta_destino_notebook, pasta_origem_notebook, pasta_destino_contornadas_notebook)
pasta_origem = "Larvas desafiadas_04_04_2014"
pasta_limiarizadas = "suavizacao_e_otsu_Larvas_desafiadas"
pasta_destino = "Larvas_desafiadas_sobrepostas"
aplica_gauss_e_otsu(pasta_origem, pasta_limiarizadas)

sobrepoe_imagens(pastaLimiarizadas= pasta_limiarizadas, pastaOriginais=pasta_origem, pastaDestino= pasta_destino)

