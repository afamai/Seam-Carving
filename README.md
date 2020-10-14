# Seam-Carving

This is a command-line interface (CLI) program that performs content aware image resizing using seam carving.
This project used the algorithm described in the following papers:
* [Seam Carving for Content-Aware Image Resizing](https://perso.crans.org/frenoy/matlab2012/seamcarving.pdf)

# Usage
#### Setting up Virtual Environment (Optional)
This step is optional and if you want to setup a virutal environment you can follow this [guide](https://docs.python-guide.org/dev/virtualenvs/) here

#### Building the code
Install required python libraries
```
$ pip install cython numpy .
```

Compile code for cython
```
$ python setup.py build_ext --inplace
```

#### Running the code
Using the `seam_carving` command you can now use seam carving to resize images.

```
$ seam_carving --help
Usage: seam_carving [OPTIONS]

Options:
  -i, --input FILENAME  The input file.  [required]
  -o, --output PATH     The output file.  [default: result{:04}.jpg]
  -w, --width INTEGER   The resulting width to resize the image to.
  -h, --height INTEGER  The resulting height to resize the image to.
  --help                Show this message and exit.
```
