# point-cloud-colorize

Colors a point cloud using a WMS.

This python script adds color to a LAS/LAZ file using a WMS service.

(Default: PDOK aerial imagery)

## Installation

### Conda

Download and install [Anaconda](https://www.anaconda.com/download/) or [Miniconda](https://conda.io/miniconda.html). Open the `Anaconda Prompt`. Run the following command in the directory of this repository:

```
conda env create -f environment.yml
```

## Usage

### Conda

Open an Anaconda Prompt. Run the following command:

```
conda activate point-cloud-colorize
python las_colorize.py -h
```

To see the help.

## Example

```
python las_colorize.py -i C_25DN2.las -o C_25DN2_color.las
```
