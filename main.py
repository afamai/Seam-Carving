from skimage import io
import numpy as np
import glob
import re
import click
import seam_carving as sc
import time
import random

@click.command()
@click.option("-i", "--input", type=click.File('rb'), required=True, help="The input file.")
@click.option("-o", "--output", type=click.Path(), default="result{:04}.jpg", help="The output file.", show_default=True)
@click.option("-w", "--width", type=int, help="The resulting width to resize the image to.")
@click.option("-h", "--height", type=int, help="The resulting height to resize the image to.")
def cli(input, output, width, height):
    image = io.imread(input)
    image = image.astype(np.int_)
    h, w, _ = image.shape

    if width:
        dx = width - w
        if dx < 0:
            image = sc.remove_seams(image, abs(dx))
        elif dx > 0:
            image = sc.add_seams(image, dx)

    if height:
        image = np.rot90(image)
        dy = height - h
        if dy < 0:
            image = sc.remove_seams(image, abs(dy))
        elif dy > 0:
            image = sc.add_seams(image, dy)
        image = np.rot90(image, k=-1)
    image = image.astype(np.uint8)
    # Find all result images in current directory
    results = glob.glob("result*.jpg") 
    idx = 0
    if results:
        # Get the largest index
        idx = int(re.search(r'\d+', results[-1]).group())
    
    io.imsave(output.format(idx+1), image)