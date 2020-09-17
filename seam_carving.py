import click
import matplotlib.pyplot as plt
from skimage import filters, color, io
import numpy as np
import time
import glob
import re
import multiprocessing as mp

def compute_scoring_matrix(image):
    # computer the energy image using gradient magnitude
    matrix = filters.sobel(color.rgb2gray(image))

    r, c = matrix.shape
    for i in range(1, r):
        for j in range(c):
            if j == 0:
                matrix[i, j] += min(matrix[i-1, j], matrix[i-1, j+1])
            elif j == c-1:
                matrix[i, j] += min(matrix[i-1, j-1], matrix[i-1, j])
            else:
                matrix[i, j] += min(matrix[i-1, j-1], matrix[i-1, j], matrix[i-1, j+1])

    return matrix

def minimum_seam(matrix):
    r, c = matrix.shape
    # mask = np.ones((r, c), dtype=np.bool)
    mask = []
    for i in reversed(range(r)):
        if i == r-1:
            j = np.argmin(matrix[-1])
        else:
            if j == 0:
                j += np.argmin(matrix[i, j:j+2])
            else:
                j += np.argmin(matrix[i, j-1:j+2]) - 1
        # mask[i, j] = False
        mask.append(i * c + j)
    return mask

def remove_seams(image, amount):
    img = image.copy()
    for _ in range(amount):
        score_matrix = compute_scoring_matrix(img)
        mask = minimum_seam(score_matrix)

        # remove seam from image
        r, c, _ = img.shape
        # img = img[mask].reshape((r, c-1, 3))
        img = np.delete(img.reshape((r*c, 3)), mask, axis=0).reshape((r, c-1, 3))
    
    return img

@click.command()
@click.option("-i", "--input", type=click.File('rb'), required=True, help="The input file.")
@click.option("-o", "--output", type=click.Path(), default="result{:04}.jpg", help="The output file.", show_default=True)
@click.option("-w", "--width", type=int, help="The resulting width to resize the image to.")
@click.option("-h", "--height", type=int, help="The resulting height to resize the image to.")
def cli(input, output, width, height):
    image = io.imread(input)
    h, w, _ = image.shape

    if width:
        dx = width - w
        if dx < 0:
            image = remove_seams(image, abs(dx))

    

    if height:
        image = np.rot90(image)
        dy = height - h
        if dy < 0:
            image = remove_seams(image, abs(dy))
        image = np.rot90(image, k=-1)

    # Find all result images in current directory
    results = glob.glob("result*.jpg") 
    idx = 0
    if results:
        # Get the largest index
        idx = int(re.search(r'\d+', results[-1]).group())
    
    io.imsave(output.format(idx+1), image)