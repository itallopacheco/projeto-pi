from PIL import Image
import random
import sys

sys.setrecursionlimit(10000)

def count_objects(image_path):
    # Open the image file
    img = Image.open(image_path)

    # Get the pixel data as a list of lists
    pixels = list(img.getdata())
    width, height = img.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    # Count the objects
    count = 0
    for y in range(height):
        for x in range(width):
            # If we find a black pixel, start a new object
            if pixels[y][x] == 0:
                count += 1
                # Flood fill the object with white
                flood_fill(pixels, width, height, x, y, count)

    saveImage(height,width,pixels)

    return count

def flood_fill(pixels, width, height, x, y, count):
    # Base case: pixel is outside image bounds or is already white
    if x < 0 or y < 0 or x >= width or y >= height or pixels[y][x] != 0:
        return

    # Mark the pixel as white
    pixels[y][x] = 255 - count * 20

    # Recursively flood fill surrounding pixels
    flood_fill(pixels, width, height, x + 1, y, count)
    flood_fill(pixels, width, height, x - 1, y, count)
    flood_fill(pixels, width, height, x, y + 1, count)
    flood_fill(pixels, width, height, x, y - 1, count)



def saveImage(width, height, image):
    img_name = "imagem" + str(random.randint(0, 10000)) + ".pgm"
    type_img = "P2" + "\n"
    size = str(width) + " " + str(height) + "\n"
    header = [type_img, size, "255\n"]

    file_img = open(img_name, 'w')

    # Escreve o cabeçalho
    for content in header:
        file_img.write(content)

    for i in range(height):

        for j in range(width):
            pixel = str(image[i][j]) + '\n'
            file_img.write(pixel)

    file_img.close()

print(count_objects('/home/itallo/Ufs/2022.2/PI/teste.pbm'))