import cv2
import os

def conta_proteina_por_nucleo(contornosNucleo, contornosProteina):
    qtdProteina_por_nucleo = []
    for nucleo, proteina in zip(contornosNucleo, contornosProteina):
        qtd_proteina = len(proteina)  # Calcula a quantidade de proteína como o número de contornos de proteína correspondente
        qtdProteina_por_nucleo.append(qtd_proteina)
    return qtdProteina_por_nucleo

pasta_origem = "imagens_sobrepostas"
imagens_validas = ["CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series009_z0_ch00.tif",
                   "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series009_z0_ch02.tif",
                   "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series011_z0_ch00.tif",
                   "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series011_z0_ch02.tif",
                   "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series027_z0_ch00.tif",
                   "CgToll10B_RabbitTube546_ Dorsal647_03_06_2019.lif_Series027_z0_ch02.tif"]
pasta_destino = "nucleos_preenchidos"

arquivos = os.listdir(pasta_origem)
nucleos = []
proteinas = []
j = 0
for arquivo in arquivos:
    if arquivo in imagens_validas:
        caminho_origem = os.path.join(pasta_origem, arquivo)
        img = cv2.imread(caminho_origem)
        imagem_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bordas = cv2.Canny(imagem_gray, 100, 200)
        contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print("Printando os contornos: ", contornos)

        print("Intensidade de cada ponto: ", )
        imagem_preenchida = img.copy()
        cv2.drawContours(imagem_preenchida, contornos, -1, (0, 255, 0), thickness=cv2.FILLED)
        cv2.imwrite(os.path.join(pasta_destino, f"{arquivo}"), imagem_preenchida)
        
        #Como as imagens de núcelos estão salvas primeiro do que as imagens de proteínas e o contador j começa em 0, então sempre que j
        #for par será uma imagem de núcleo; caso seja ímpar, será uma imagem de proteína.
        if j % 2 == 0:
            nucleos.append(contornos)
        else:
            proteinas.append(contornos)
        j += 1
# Calcula a quantidade de proteína por núcleo para cada imagem válida
# for i in range(len(nucleos)):
#     qtd_proteina_por_nucleo = conta_proteina_por_nucleo(nucleos[i], proteinas[i])
#     print(f"Imagem {i+1} {imagens_validas[i]}:")
#     for j, qtd_proteina in enumerate(qtd_proteina_por_nucleo): #enumerate mapeia cada elemento da qtd de proteína com um índice
#         print(f"Núcleo {j+1}: {qtd_proteina} proteínas")


