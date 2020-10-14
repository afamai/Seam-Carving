from skimage import io, transform, util
import matplotlib.pyplot as plt
import numpy as np
import glob
import re
import click
import seam_carving as sc
import time
import random

@click.command()
@click.option("-i", "--input", "input_", type=click.File('rb'), required=True, help="The input file.")
@click.option("-o", "--output", type=click.Path(), default="result{:04}.jpg", help="The output file.", show_default=True)
@click.option("--resize", nargs=2, type=int, help="Resizes image to a certain size.")
@click.option("--amplify", type=float, help="Amplifies the content of the image.")
#@click.option("--remove", type=click.File('rb'), help="Remove objects within the image by using a removal mask. Mask must be the same size of the image")
#@click.option("-m", "--mask", type=click.File())
def cli(input_, output, resize, amplify):
    image = io.imread(input_)
    if resize:
        width, height = resize
        h, w, _ = image.shape
        
        image = image.astype(np.int_)
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
    elif amplify:
        height, width, _ = image.shape
        h = round(height * amplify)
        w = round(width * amplify)
        image = transform.resize(image, (h, w), anti_aliasing=True)\
        
        image = util.img_as_ubyte(image).astype(np.int_)
        image = sc.remove_seams(image, w - width)
        image = np.rot90(image)
        image = sc.remove_seams(image, h - height)
        image = np.rot90(image, k=-1)
        image = image.astype(np.uint8)

    # Find all result images in current directory
    results = glob.glob("result*.jpg") 
    idx = 0
    if results:
        # Get the largest index
        idx = int(re.search(r'\d+', results[-1]).group())
    
    io.imsave(output.format(idx+1), image)