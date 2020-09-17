import click
import matplotlib.pyplot as plt
from skimage import data, filters, color, io
from scipy.ndimage import correlate
import numpy as np
import time

def compute_scoring_matrix(image):
    # computer the energy image using gradient magnitude
    matrix = filters.sobel(color.rgb2gray(image))

    r, c = matrix.shape
    for i in range(1, r):
        for j in range(c):
            if (j == 0):
                matrix[i, j] += min(matrix[i-1, j], matrix[i-1, j+1])
            elif (j == c-1):
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
def cli():
    image = io.imread("example01.jpg")
    start = time.time()
    im = remove_seams(image, 30)
    print("Time: " + str(time.time() - start))
    plt.imshow(im)
    plt.show()