import click
import matplotlib.pyplot as plt
from skimage import data, filters, color, io
from scipy.ndimage import correlate
import numpy as np
import time


@click.command()
def cli():
    click.echo("hello world")
    img = io.imread("example02.jpg")
    original = img.copy()
    record = []
    start = time.time() 
    for n in range(100):
        energy = filters.sobel(color.rgb2gray(img))
        matrix = energy.copy()
        r, c = matrix.shape
        for i in range(1, r):
            for j in range(c):
                if (j == 0):
                    matrix[i, j] += min(matrix[i-1, j], matrix[i-1, j+1])
                elif (j == c-1):
                    matrix[i, j] += min(matrix[i-1, j-1], matrix[i-1, j])
                else:
                    matrix[i, j] += min(matrix[i-1, j-1], matrix[i-1, j], matrix[i-1, j+1])

        # remove seam
        seam = []
        for i in reversed(range(r)):
            if i == r-1:
                j = np.argmin(matrix[-1])
            else:
                if j == 0:
                    j += np.argmin(matrix[i, j:j+2])
                else:
                    j += np.argmin(matrix[i, j-1:j+2]) - 1

            seam.append(i * c + j)

        img = np.delete(img.reshape((r*c, 3)), seam, axis=0)
        img = img.reshape((r, c-1, 3))
        record.append(seam)
        print(str(n) + " seam complete")
    
    click.echo("Time taken: " + str(time.time() - start))

    seam_removed = img.reshape((-1,3))
    for seam in reversed(record):
        for idx in reversed(seam):
            seam_removed = np.insert(seam_removed, idx, [255,0,0], axis=0)

    seam_removed = seam_removed.reshape(original.shape)
                
    plt.imshow(img)
    plt.show()

    plt.imshow(seam_removed)
    plt.show()
    