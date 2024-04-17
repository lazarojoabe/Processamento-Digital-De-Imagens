import cv2
import os
import shutil
import numpy as np
pasta_nucleos = "imagens_validas_nucleos"
pasta_proteinas = "imagens_validas_proteinas"

def filtraImagensNucleosValidas(pastaOrigem, pastaDestino):
    for nome_do_arquivo in os.listdir(pastaOrigem):
        # Verifica se o arquivo é uma imagem e termina com _ch00.tif (núcleos)
        if nome_do_arquivo.endswith('_ch00.tif'):
            # Constrói o caminho de origem e destino para o arquivo
            origem = os.path.join(pastaOrigem, nome_do_arquivo)
            destino = os.path.join(pastaDestino, nome_do_arquivo)
            shutil.copy(origem, destino)
filtraImagensNucleosValidas("Larvas_desafiadas_sobrepostas", "imagens_validas_nucleos")


def filtraImagensProteinasValidas(pastaOrigem, pastaDestino):
    for nome_do_arquivo in os.listdir(pastaOrigem):
        # Verifica se o arquivo é uma imagem e termina com _ch00.tif (núcleos)
        if nome_do_arquivo.endswith('_ch02.tif'):
            # Constrói o caminho de origem e destino para o arquivo
            origem = os.path.join(pastaOrigem, nome_do_arquivo)
            destino = os.path.join(pastaDestino, nome_do_arquivo)
            shutil.copy(origem, destino)
filtraImagensProteinasValidas("Larvas desafiadas_04_04_2014","imagens_validas_proteinas")
def pesquisa_coordenadas(coordX, coordY, imgProteina):
    valorPixel = imgProteina[coordX, coordY]
    return valorPixel

def obtem_coordenadas(contornos):
    coordenadasX = []
    coordenadasY = []
    for contorno in contornos:
        # Iterar sobre os pontos do contorno
        for ponto in contorno:
            # Obter as coordenadas x e y do ponto
            x, y = ponto[0] #ponto é uma lista de somente um item, então, para acessar os dados é necessário buscar
            #pelo índice do único elemento, que é o primeiro.
            coordenadasX.append(x)
            coordenadasY.append(y)
    return coordenadasX, coordenadasY
# img_nucleos = filtraImagensNucleosValidas("Larvas_desafiadas_sobrepostas")
# img_proteina = filtraImagensProteinasValidas("Larvas desafiadas_04_04_2014")
def calcular_media_intensidades(img_proteina, contornos):
    intensidades = []
    for contorno in contornos:
        # Calcula a máscara para o contorno atual
        mascara = np.zeros_like(img_proteina)
        cv2.drawContours(mascara, [contorno], -1, 255, -1)
        
        # Aplica a máscara à imagem da proteína para obter apenas os pixels dentro do contorno
        pixels_contorno = cv2.bitwise_and(img_proteina, mascara)
        
        # Calcula a média das intensidades dos pixels dentro do contorno
        intensidade_media = np.mean(pixels_contorno[pixels_contorno != 0])
        intensidades.append(intensidade_media)
    
    # Calcula a média geral das intensidades
    media_geral = np.mean(intensidades)
    return media_geral


arquivos = os.listdir(pasta_nucleos)
proteina = os.listdir(pasta_proteinas)
for arquivo in arquivos:
    caminho_origem = os.path.join(pasta_nucleos, arquivo)
    img = cv2.imread(caminho_origem)
    nucleo_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bordas = cv2.Canny(nucleo_gray, 100, 200)
    contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
    # Verificar se há uma imagem de proteína correspondente
    for imagem_proteina in proteina:
        #o que muda de uma imagem de núcleo para uma de proteína é o final; "z0_ch00.tif" é de núcleo
        #e "_z0_ch02.tif" é de proteína
        if imagem_proteina == arquivo.replace("_z0_ch00.tif", "_z0_ch02.tif"):
            caminho_proteina = os.path.join(pasta_proteinas, imagem_proteina)
            img_proteina = cv2.imread(caminho_proteina)
            proteina_gray = cv2.cvtColor(img_proteina, cv2.COLOR_BGR2GRAY)
            coordenadasX, coordenadasY = obtem_coordenadas(contornos)
        
            qtdMediaProteina = calcular_media_intensidades(proteina_gray, contornos)
            print(f"Valor médio de proteína na imagem {arquivo} é {qtdMediaProteina}")
            print(f"Valor médio de proteína na imagem {arquivo} é {qtdMediaProteina}")
