import cv2
import numpy as np
 
# Carregar a imagem
imagem = cv2.imread("C:\Users\lazaro\Documents\OneDrive - Universidade Federal de Uberlândia\IC\Processamento-Digital-De-Imagens\CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series009_z0_ch00.tif")
 
# Converter a imagem para escala de cinza
imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
 
# Aplicar o detector de bordas (por exemplo, Canny)
bordas = cv2.Canny(imagem_gray, 100, 200)
 
# Encontrar os contornos das bordas
contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
# Preencher os contornos com a cor verde
imagem_preenchida = imagem.copy()
cv2.drawContours(imagem_preenchida, contornos, -1, (0, 255, 0), thickness=cv2.FILLED)
 
# Exibir a imagem original e a imagem com as bordas preenchidas
cv2.imshow('Imagem Original', imagem)
cv2.imshow('Imagem Preenchida', imagem_preenchida)
for i in range(len(contornos)):
    print(len(contornos[i]))
cv2.waitKey(0)
cv2.destroyAllWindows()