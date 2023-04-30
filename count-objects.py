from PIL import Image
import copy
import random
import sys

sys.setrecursionlimit(1000000)


def count_objects(image_path, case=0):
    # Open the image file
    img = Image.open(image_path)

    # Get the pixel data as a list of lists
    pixels = list(img.getdata())
    width, height = img.size
    img_input = [pixels[i * width:(i + 1) * width] for i in range(height)]

    # Segment the holes in the image
    img_holes = get_holes(img_input, width, height)

    # Fill the holes in the image
    img_filled = fill_holes(img_input, img_holes, width, height)

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
                    img_input, img_filled, width, height), distinction=str(case) + "-" + str(count))
                if has_hole:
                    has_holes += 1

    # Print the results
    print('Total de objetos: ', count, '\nObjetos sem furos: ', count - has_holes,
          '\nObjetos com furos: ', has_holes, '\n')


def flood_fill(pixels, holes, width, height, x, y):
    # Base case: pixel is outside image bounds or is already white
    if x < 0 or y < 0 or x >= width or y >= height or pixels[y][x] == 255:
        return False

    # Mark the pixel as white
    pixels[y][x] = 255

    # If the pixel is a hole, mark the object as having a hole
    has_hole = False

    # Check if the pixel is a hole in the image with only holes
    if holes[y][x] == 0:
        has_hole = True

    # Recursively flood fill surrounding 8 pixels and checks for holes
    has_hole = flood_fill(pixels, holes, width, height, x - 1, y - 1) or has_hole
    has_hole = flood_fill(pixels, holes, width, height, x, y - 1) or has_hole
    has_hole = flood_fill(pixels, holes, width, height, x + 1, y - 1) or has_hole
    
    has_hole = flood_fill(pixels, holes, width, height, x + 1, y) or has_hole
    has_hole = flood_fill(pixels, holes, width, height, x - 1, y) or has_hole
    
    has_hole = flood_fill(pixels, holes, width, height, x - 1, y + 1) or has_hole
    has_hole = flood_fill(pixels, holes, width, height, x, y + 1) or has_hole
    has_hole = flood_fill(pixels, holes, width, height, x + 1, y + 1) or has_hole

    return has_hole


def flood_fill_background(pixels, width, height, x, y):
    # Base case: pixel is outside image bounds or is already white
    if x < 0 or y < 0 or x >= width or y >= height or pixels[y][x] == 0:
        return

    # Mark the pixel as white
    pixels[y][x] = 0

    # Recursively flood fill surrounding pixels
    flood_fill_background(pixels, width, height, x + 1, y)
    flood_fill_background(pixels, width, height, x - 1, y)
    flood_fill_background(pixels, width, height, x, y + 1)
    flood_fill_background(pixels, width, height, x, y - 1)


def get_holes(pixels, width, height):
    copy_pixels = copy.deepcopy(pixels)
    flood_fill_background(copy_pixels, width, height, 0, 0)
    invert_colors(copy_pixels, width, height)
    return copy_pixels


def invert_colors(pixels, width, height):
    for y in range(height):
        for x in range(width):
            if pixels[y][x] == 0:
                pixels[y][x] = 255
            elif pixels[y][x] == 255:
                pixels[y][x] = 0


def fill_holes(objects, holes, width, height):
    c_objects = copy.deepcopy(objects)
    c_holes = copy.deepcopy(holes)
    for y in range(height):
        for x in range(width):
            if c_holes[y][x] == 0 or c_objects[y][x] == 0:
                c_objects[y][x] = 0
    return c_objects


def add_padding(input_pixels):
    pixels = copy.deepcopy(input_pixels)
    rows = len(pixels)
    cols = len(pixels[0])
    new_rows = rows + 4
    new_cols = cols + 4
    new_pixels = [[0 for j in range(new_cols)] for i in range(new_rows)]

    # Set the values of the new rows to 255
    for i in range(2):
        for j in range(new_cols):
            new_pixels[i][j] = 255
        for j in range(new_cols - 2, new_cols):
            new_pixels[new_rows - i - 1][j] = 255

    # Set the values of the new columns to 255
    for i in range(2, new_rows - 2):
        for j in range(2):
            new_pixels[i][j] = 255
        for j in range(new_cols - 2, new_cols):
            new_pixels[i][j] = 255

    # Copy the values from the original matrix
    for i in range(rows):
        for j in range(cols):
            new_pixels[i+2][j+2] = pixels[i][j]

    return new_pixels


def get_diff(pixels, new_pixels, width, height):
    c_pixels = copy.deepcopy(pixels)
    c_new_pixels = copy.deepcopy(new_pixels)

    for y in range(height):
        for x in range(width):
            if c_pixels[y][x] == 0 and c_new_pixels[y][x] == 255:
                c_pixels[y][x] = 128

    return c_pixels


def saveImage(width, height, image, distinction=''):
    img_name = str(distinction) + 'imagem' + \
        str(random.randint(0, 10000)) + '.pgm'
    type_img = 'P2' + '\n'
    size = str(width) + ' ' + str(height) + '\n'
    header = [type_img, size, '255\n']

    file_img = open(img_name, 'w')

    # Escreve o cabeçalho
    for content in header:
        file_img.write(content)

    for i in range(height):

        for j in range(width):
            pixel = str(image[i][j]) + '\n'
            file_img.write(pixel)

    file_img.close()


print('--------------- CASE 1 ---------------')
count_objects('C:/Users/Jorge/Desktop/projeto-pi/teste.pbm', 1)
print('--------------- CASE 2 ---------------')
count_objects('C:/Users/Jorge/Desktop/projeto-pi/teste1.pbm', 2)
