import cv2
import os

pasta_nucleos = "imagens_sobrepostas"
pasta_proteinas = "CgToll10B"
imagens_validas_nucleos = ["CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series009_z0_ch00.tif",
                            "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series011_z0_ch00.tif",
                            "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series027_z0_ch00.tif"]

imagens_validas_proteinas = ["CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series009_z0_ch02.tif",
                             "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series011_z0_ch02.tif",
                             "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series027_z0_ch02.tif"]

arquivos = os.listdir(pasta_nucleos)

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
            x, y = ponto[0]

            coordenadasX.append(x)
            coordenadasY.append(y)
    return coordenadasX, coordenadasY

for arquivo in arquivos:
    if arquivo in imagens_validas_nucleos:
        caminho_origem = os.path.join(pasta_nucleos, arquivo)
        img = cv2.imread(caminho_origem)
        nucleo_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bordas = cv2.Canny(nucleo_gray, 100, 200)
        contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Verificar se há uma imagem de proteína correspondente
        for imagem_proteina in imagens_validas_proteinas:
            if imagem_proteina == arquivo.replace("_z0_ch00.tif", "_z0_ch02.tif"):
                caminho_proteina = os.path.join(pasta_proteinas, imagem_proteina)
                img_proteina = cv2.imread(caminho_proteina)
                proteina_gray = cv2.cvtColor(img_proteina, cv2.COLOR_BGR2GRAY)
                coordenadasX, coordenadasY = obtem_coordenadas(contornos)
                #calculando a intensidade para cada x e y correspondente nas duas listas (coordenadasX e coordenadasY)
                intensidadesProteinas = [pesquisa_coordenadas(x, y, proteina_gray) for x, y in zip(coordenadasX, coordenadasY)]
                qtdMediaProteina = sum(intensidadesProteinas) / len(contornos)

                print(f"Valor médio de proteína na imagem {arquivo} é {qtdMediaProteina}")
