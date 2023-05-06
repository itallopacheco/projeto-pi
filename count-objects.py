from PIL import Image
import copy
import sys
import time
import os
from os import walk
import shutil
from queue import Queue

sys.setrecursionlimit(1000000)

"""
    A funcao count_objects é a funcção principal.
    Após abrir a imagem e transformar em uma matriz de pixels, ela chama as funções

    add_padding: adiciona uma borda branca de 2 pixels em volta da imagem.
    get_holes: para ter uma imagem apenas com os buracos.
    fill_holes: para preencher os buracos e me dar uma imagem com os objetos completos.

    Após isso, ele percorre a imagem e chama a função flood_fill para preencher os objetos.
    A função flood_fill é recursiva e preenche os pixels ao redor do pixel atual.
    Ela também retorna se o objeto tem buracos ou não.
    Após isso chamamos get_diff para pegar a diferença entre a imagem original e a imagem preenchida.
    Essa diferença é salva em um arquivo .pgm.

    Após isso verificamos o retorno da função flood_fill (que indica se existem buracos naquele objeto ou nao)
    e incrementamos o contador de objetos.

    No final, chamamos a função print_results para imprimir os resultados.
    
"""
def count_objects(image_path, case=0):
    begin = time.perf_counter()

    # Open the image file
    img = Image.open(image_path)

    # Get the pixel data as a list of lists
    pixels = list(img.getdata())
    width, height = img.size
    img_input = [pixels[i * width:(i + 1) * width] for i in range(height)]

    img_input = add_padding(img_input)
    width += 4
    height += 4

    img_folder = os.path.join('resultados', case)
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    # Segment the holes in the image
    img_holes = get_holes(img_input, width, height)
    saveImage(width, height, img_holes, img_folder, 'holes')

    # Fill the holes in the image
    img_filled = fill_holes(img_input, img_holes, width, height)
    saveImage(width, height, img_filled, img_folder, 'filled')


    # Count the objects
    count = 0
    has_holes = 0
    for y in range(height):
        for x in range(width):
            # If we find a black pixel, start a new object
            if img_filled[y][x] == 0:
                count += 1
                # Flood fill the object with white
                has_hole = flood_fill(
                    img_filled, img_holes, width, height, x, y)
                saveImage(width, height, get_diff(
                    img_input, img_filled, width, height), img_folder, str(count))
                if has_hole:
                    has_holes += 1

    end = time.perf_counter()

    # Print the results
    print_results(end - begin, count, has_holes, case)

"""
    Funcao basica para imprimir os resultados.
"""
def print_results(time, count, has_holes, case):
    print(f'--------------- CASE {case} ---------------\nCaso {case} terminou em {time:0.1f} segundos\nTotal de objetos: {count}\nObjetos sem furos: {count - has_holes}\nObjetos com furos: {has_holes}\n')

    with open("./resultados.txt", "a") as arquivo:
        arquivo.write(
            f'--------------- CASE {case} ---------------\nCaso {case} terminou em {time:0.1f} segundos\nTotal de objetos: {count}\nObjetos sem furos: {count - has_holes}\nObjetos com furos: {has_holes}\n')

"""
    Essa funcao vai receber uma imagem com objetos, e uma imagem apenas com os buracos da img1.
    Ela vai preencher os pixeis de branco e vai verificar se o pixel atual é um buraco
    correspondente na imagem de buracos.

"""
def flood_fill(pixels, holes, width, height, x, y):
    # Cria uma fila e adiciona o pixel inicial
    q = Queue()
    q.put((x, y))

    has_hole = False

    # Enquanto a fila não estiver vazia
    while not q.empty():
        # Remove o primeiro elemento da fila
        x, y = q.get()

        # Caso Base: O pixel está fora dos limites da imagem ou já é branco
        if x < 0 or y < 0 or x >= width or y >= height or pixels[y][x] == 255:
            continue

        # Pintamos o pixel de branco
        pixels[y][x] = 255

        # Checa na imagem de buracos se o pixel atual é um buraco
        if holes[y][x] == 0:
            has_hole = True

        # Adiciona os pixels ao redor na fila
        q.put((x - 1, y - 1))
        q.put((x, y - 1))
        q.put((x + 1, y - 1))

        q.put((x + 1, y))
        q.put((x - 1, y))

        q.put((x - 1, y + 1))
        q.put((x, y + 1))
        q.put((x + 1, y + 1))

    return has_hole

"""
    Essa funcao vai preencher o fundo de uma imagem com a cor branca.
"""
def flood_fill_background(pixels, width, height, x, y):
    # Cria uma fila e adiciona o pixel inicial
    q = Queue()
    q.put((x, y))

    # Enquanto a fila não estiver vazia
    while not q.empty():
        # Remove o primeiro elemento da fila
        x, y = q.get()

        # Caso base: pixel está fora dos limites da imagem ou já é branco
        if x < 0 or y < 0 or x >= width or y >= height or pixels[y][x] == 0:
            continue

        # Marca o pixel como branco
        pixels[y][x] = 0

        # Adiciona os pixels ao redor na fila
        q.put((x + 1, y))
        q.put((x - 1, y))
        q.put((x, y + 1))
        q.put((x, y - 1))

def get_holes(pixels, width, height):
    copy_pixels = copy.deepcopy(pixels)
    flood_fill_background(copy_pixels, width, height, 0, 0)
    invert_colors(copy_pixels, width, height)
    return copy_pixels

"""
    Essa funcao vai inverter as cores de uma imagem.
"""
def invert_colors(pixels, width, height):
    for y in range(height):
        for x in range(width):
            if pixels[y][x] == 0:
                pixels[y][x] = 255
            elif pixels[y][x] == 255:
                pixels[y][x] = 0

"""
    Essa funcao vai preencher os buracos em uma imagem.
"""
def fill_holes(objects, holes, width, height):
    c_objects = copy.deepcopy(objects)
    c_holes = copy.deepcopy(holes)

    # Define a cor do pixel como 0 (preto) se o pixel for um buraco ou não fizer parte do objeto
    for y in range(height):
        for x in range(width):
            if c_holes[y][x] == 0 or c_objects[y][x] == 0:
                c_objects[y][x] = 0

    return c_objects


"""
    Essa função vai adicionar uma borda de 2 pixeis em volta da imagem.
    +2 na esquerda; +2 na direita; +2 em cima; +2 em baixo
"""
def add_padding(input_pixels):
    # As copias sao feitas para nao alterar a imagem original para fins de comparacao e auditoria 
    pixels = copy.deepcopy(input_pixels)
    rows = len(pixels)
    cols = len(pixels[0])
    new_rows = rows + 4
    new_cols = cols + 4
    new_pixels = [[255 for j in range(new_cols)] for i in range(new_rows)]

    # Copia os valores da matriz original para a nova matriz com margem de 2 pixels em cada borda
    for i in range(rows):
        for j in range(cols):
            new_pixels[i + 2][j + 2] = pixels[i][j]

    return new_pixels


"""
    Essa função vai obter a diferença entre duas imagens.
"""
def get_diff(pixels, new_pixels, width, height):
    c_pixels = copy.deepcopy(pixels)
    c_new_pixels = copy.deepcopy(new_pixels)

    # Os pixeis diferentes(que são 0 na imagem original e 255 na nova) são marcados com um valor de cinza
    for y in range(height):
        for x in range(width):
            if c_pixels[y][x] == 0 and c_new_pixels[y][x] == 255:
                c_pixels[y][x] = 128

    return c_pixels


"""
    Essa função vai salvar a imagem em um arquivo .pgm
    ela é usada para salvar as imagens que ilustram o processo 
    do reconhecimento dos objetos.
"""
def saveImage(width, height, image, folder_path, distinction=''):
    # Define o cabeçalho, nome e caminho do arquivo
    img_name = str(distinction) + '.pgm'
    type_img = 'P2' + '\n'
    size = str(width) + ' ' + str(height) + '\n'
    header = [type_img, size, '255\n']

    img_path = os.path.join(folder_path, img_name)
    file_img = open(img_path, 'w')

    # Escreve o cabeçalho
    for content in header:
        file_img.write(content)
    
    # Escreve os pixels
    for i in range(height):
        for j in range(width):
            pixel = str(image[i][j]) + '\n'
            file_img.write(pixel)

    file_img.close()


"""
    A função startTests é responsável por rodar todos os testes dentro da pasta /testes
    os resultados ficarão salvos na pasta /resultados, para cada teste será criada uma pasta 
    com o nome do arquivo de teste, dentro dessa pasta terão arquivos .pgm indicando o processo que 
    nos levou ao resultado final. 
"""
def start_tests():
    # Precisamos aumentar o limite de recursao para imagens maiores.
    sys.setrecursionlimit(1000000)

    # Busca todos os arquivos dentro da pasta /testes e verifica se ela está vazia.
    filenames = next(walk('./testes'), (None, None, []))[2]
    if filenames == []:
        print("No images found in the 'testes' folder")

    # Limpa os arquivos de resultados anteriores.
    open('./resultados.txt', 'w').close()

    # Chama a função count_objects para cada arquivo encontrado.
    for file in filenames:
        count_objects('./testes/' + file, file.split(".")[0])

    # Ao final de tudo pergunta se o usuário deseja apagar a pasta /resultados
    var = input("Deseja apagar a pasta 'resultados'? (s/n): ")
    if var == 's':
        shutil.rmtree('./resultados')
    elif var == 'n':
        input("Você pode encontrar os resultados na pasta 'resultados'")
    else:
        print("Opção inválida")


#Run the tests
start_tests()



"""

 # Open the image file
img = Image.open('testes/100x100.pbm')


# Get the pixel data as a list of lists
pixels = list(img.getdata())
width, height = img.size
img_input = [pixels[i * width:(i + 1) * width] for i in range(height)]

img_input = add_padding(img_input)
width += 4
height += 4

# Get the holes
img_holes = get_holes(img_input, width, height)
saveImage(width, height, img_holes, './resultados', 'holes')
# Fill the holes in original image
img_filled = fill_holes(img_input, img_holes, width, height)
saveImage(width, height, img_filled, './resultados', 'filled')

diff = get_diff(img_input, img_input, width, height)
saveImage(width, height, diff, './resultados', 'diff')

for y in range(height):
        for x in range(width):
            # If we find a black pixel, start a new object
            if img_filled[y][x] == 0:
                # Flood fill the object with white
                has_hole = flood_fill(img_filled, img_holes, width, height, x, y)
                # Save the image
                saveImage(width, height, img_filled, './resultados', 'filled')
                diff = get_diff(img_input, img_filled, width, height)
                saveImage(width, height, diff, './resultados', 'diff')
"""