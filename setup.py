from setuptools import setup

setup(
    name="seam-carving",
    version="0.1",
    py_modules=["seam_carving"],
    include_package_data=True,
    install_requires=["click", "scikit-image"],
    entry_points="""
        [console_scripts]
        seam_carving=seam_carving:cli
    """,
)