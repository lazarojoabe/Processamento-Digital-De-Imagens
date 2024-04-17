import os

# Caminho para a pasta contendo as imagens
pasta_imagens = "Larvas desafiadas_04_04_2014"

# Inicializa listas vazias para armazenar os nomes dos arquivos de núcleos e proteínas
nucleos = []
proteinas = []

# Percorre todos os arquivos na pasta
for nome_do_arquivo in os.listdir(pasta_imagens):
    # Verifica se o arquivo é uma imagem e termina com _ch00.tif (núcleos)
    if nome_do_arquivo.endswith('_ch00.tif'):
        nucleos.append(nome_do_arquivo)
    # Verifica se o arquivo é uma imagem e termina com _ch02.tif (proteínas)
    elif nome_do_arquivo.endswith('_ch02.tif'):
        proteinas.append(nome_do_arquivo)

# Imprime as listas de núcleos e proteínas
print("Núcleos:", nucleos)
print("Proteínas:", proteinas)
