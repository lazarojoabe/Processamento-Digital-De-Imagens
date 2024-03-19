import cv2
import numpy as np
import os

def conta_proteina_por_nucleo(contornosNucleo, contornosProteina):
    qtdProteina_por_nucelo = []
    for contornosNucleo, contornosProteina in zip(contornosNucleo, contornosProteina):
        qtdProteina_por_nucelo[i] = contornosProteina[i]
    return qtdProteina_por_nucelo

def armazenar_pixels(contornos):
    pixels = []
    for contorno in contornos:
        for ponto in contorno:
            for coordenada in ponto:
                pixels.append(coordenada)
    return pixels

#acessando imagens contornadadas
pasta_origem = "imagens_sobrepostas"

pasta_destino = "nucleos_preenchidos"

#na pasta, há algumas imagens que podemos desconsidear em nossa análise, então utilzaremos somente as imagens de nosso interesse, que são essas
#abaixo:
imagens_validas = ["CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series009_z0_ch00.tif", "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series009_z0_ch02.tif",
                   "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series011_z0_ch00.tif", "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series011_z0_ch02.tif",
                   "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series027_z0_ch00.tif", "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series027_z0_ch02.tif"]
arq = os.listdir(pasta_origem)
j = 0
#lista para guardar cada nucleo
nucleos = [[]]
 
#lista para guardar a proteína do n-ésimo núcleo
proteinas = [[]]
for i in arq:
    if i in imagens_validas:
        caminho_origem = os.path.join(pasta_origem, i)
        img = cv2.imread(caminho_origem)
        # Converter a imagem para escala de cinza
        imagem_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
        # Aplicar o detector de bordas (por exemplo, Canny)
        bordas = cv2.Canny(imagem_gray, 100, 200)
 
        # Encontrar os contornos das bordas
        contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
        # Preencher os contornos com a cor verde
        imagem_preenchida = img.copy()
        cv2.drawContours(imagem_preenchida, contornos, -1, (0, 255, 0), thickness=cv2.FILLED)
 
        cv2.imwrite(os.path.join(pasta_destino, f"{i}"), imagem_preenchida)
        
        if(j % 2 == 0): #os índices pares das imagens válidas são os núcleos
            nucleos.append(contornos) 
        else:
            proteinas.append(contornos) #os índices ímpares das imagens válidas são as proteínas equivalentes ao último índice par
        j += 1
print(proteinas)