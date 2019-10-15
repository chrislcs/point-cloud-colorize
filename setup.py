import setuptools

setuptools.setup(
    name="point-cloud-colorize",
    version="0.0.3",
    author="Chris Lucas, Arno Timmer, Rein van 't Veer",
    author_email="chris.lucas@geodan.nl, arno.timmer@geodan.nl, rein@geodan.nl",
    description="Point cloud colorization library",
    long_description="Colorizes point cloud .las or .laz files using aerial photography",
    long_description_content_type="text/markdown",
    url="https://github.com/Geodan/point-cloud-colorize",
    packages=['point_cloud_colorize'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Windows",
    ],
    install_requires=[],
)
