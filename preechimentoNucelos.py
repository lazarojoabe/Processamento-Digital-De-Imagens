import cv2
import matplotlib.pyplot as plt
import os

#acessando imagens contornadadas
pasta_origem = "CgToll10B"


#na pasta, há algumas imagens que podemos desconsidear em nossa análise, então utilzaremos somente as imagens de nosso interesse, que são essas
#abaixo:
imagens_validas = ["CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series009_z0_ch00.tif", "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series009_z0_ch02.tif",
                   "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series011_z0_ch00.tif", "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series011_z0_ch02.tif",
                   "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series027_z0_ch00.tif", "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series027_z0_ch02.tif"]
arq = os.listdir(pasta_origem)

for i in arq:
    if i in imagens_validas:
        caminho_origem = os.path.join(pasta_origem, i)
        img = cv2.imread(caminho_origem)

##TESTE PARA UMA IMAGEM INDIVIDUAL
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Função para segmentar uma bolinha na imagem usando flood fill e retornar sua área e a imagem preenchida
def segment_and_get_area(img, seed_point):
    # Converter a imagem para tons de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Inicializar a máscara de preenchimento
    mask = np.zeros((img.shape[0] + 2, img.shape[1] + 2), dtype=np.uint8)
    
    # Definir os limites de diferença de cor
    lo_diff = (10, 10, 10)
    up_diff = (10, 10, 10)
    
    # Realizar o preenchimento (flood fill)
    filled_img, mask, rect, area = cv2.floodFill(img.copy(), mask, seed_point, (255, 255, 255), lo_diff, up_diff)
    
    return area, filled_img

# Carregar a imagem original
img_original = cv2.imread("imagens_sobrepostas/CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series009_z0_ch00.tif")

# Converter a imagem para tons de cinza
img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

# Binarizar a imagem
_, img_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

# Encontrar contornos na imagem binarizada
contours, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterar sobre os contornos
for contour in contours:
    # Calcular o momento do contorno para encontrar o centro de massa
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        # Ponto de partida de preenchimento
        seed_point = (cX, cY)
        
        # Segmentar a bolinha usando flood fill e obter sua área e a imagem preenchida
        area, filled_img = segment_and_get_area(img_original, seed_point)
        
        # Exibir a área da bolinha
        print(f"Área da bolinha: {area} pixels")
        
        # Converter a imagem preenchida para RGB
        filled_img_rgb = cv2.cvtColor(filled_img, cv2.COLOR_BGR2RGB)
        
        # Exibir a imagem preenchida
        plt.imshow(filled_img_rgb)
        plt.axis('off')
        plt.show()
