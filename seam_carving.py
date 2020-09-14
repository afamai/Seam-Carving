import click
import matplotlib.pyplot as plt
from skimage import data, filters, color

@click.command()
def cli():
    click.echo("hello world")
    img = data.brick()
    img = data.stereo_motorcycle()[0]
    gradient = filters.sobel(img)

    fig, axes = plt.subplots(1, 2)
    ax = axes.ravel()
    ax[0].imshow(img, cmap="gray")
    ax[1].imshow(gradient, cmap="gray")
    plt.show()