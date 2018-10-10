# point-cloud-colorize

Colors a point cloud using a WMS.

This python script adds color to a LAS/LAZ file using a WMS service.

(Default: PDOK 2016 aerial imagery).

## Installation

Install python3 (with numpy, matplotlib, requests and owslib libraries) and [PDAL](https://www.pdal.io/) (with LASzip).

### Windows

The easiest way to install these packages on windows is with [OSGeo4W](https://trac.osgeo.org/osgeo4w/) or [conda](https://conda.io/).

#### OSGeo4W

Download the OSGeo4W installer. Run and choose `advanced install` and select at least the following packages: `pdal`, `laszip`, `python3-core`, `python3-numpy`, `python3-matplotlib`, `python3-requests`, `python3-owslib`.

#### Conda

Download and install [Anaconda](https://www.anaconda.com/download/) or [Miniconda](https://conda.io/miniconda.html). Open the `Anaconda Prompt`. Run the following commands:

```
conda install requests
conda install numpy
conda install matplotlib
conda install owslib
conda install -c conda-forge pdal
conda install -c conda-forge python-pdal
```

## Usage

### Windows

#### OSGeo4W

Open an OSGeo4W shell and run `py3_env.bat` located in the `bin` folder in your OSGeo4W installation folder. Run the following command:

```
python las_colorize.py -h
```

To see the help.

#### Conda

Open an Anaconda Prompt. Run the following command:

```
python las_colorize.py -h
```

To see the help.

## Example

```
python las_colorize.py -i C_25DN2.las -o C_25DN2_color.las
```
