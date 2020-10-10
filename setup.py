from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name="seam-carving",
    version="0.1",
    py_modules=["main"],
    ext_modules = cythonize("seam_carving.pyx"),
    include_package_data=True,
    install_requires=["click", "scikit-image", "cython"],
    include_dirs=[numpy.get_include()],
    entry_points="""
        [console_scripts]
        seam_carving=main:cli
    """,
)