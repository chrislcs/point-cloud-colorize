# -*- coding: utf-8 -*-
"""
Python3

@author: Chris Lucas
"""

from io import BytesIO
import json
import math
import numpy as np
import matplotlib.image as mpimg
import pyproj
from owslib.wms import WebMapService
from requests.exceptions import ReadTimeout


def request_image(bbox, size, wms_url, wms_layer, wms_srs,
                  wms_version, wms_format, retries):
    """
    Request an image from a WMS.

    Parameters
    ----------
    bbox : list of float
        The coordinates of the bounding box. [xmin, ymin, xmax, ymax]
    size : list of int
        The size of the image to be requested in pixels. [x, y]
    wms_url : str
        The url of the WMS service to use.
    wms_layer : str
        The layer of the WMS service to use.
    wms_srs : str
        The spatial reference system of the WMS data to request.
    wms_version : str
        The image format of the WMS data to request.
    wms_format : str
        The version number of the WMS service.
    retries : int
        Amount of times to retry retrieving an image from the WMS if it
        fails.

    Returns
    -------
    img : (MxNx3) array
        The RGB values of each pixel
    """
    for i in range(retries):
        try:
            wms = WebMapService(wms_url, version=wms_version)
            wms_img = wms.getmap(layers=[wms_layer],
                                 srs=wms_srs,
                                 bbox=bbox,
                                 size=size,
                                 format=wms_format,
                                 transparent=True)
            break
        except ReadTimeout as e:
            if i != retries-1:
                print("ReadTimeout, trying again..")
            else:
                raise e

    img = mpimg.imread(BytesIO(wms_img.read()), 0)

    return img


def image_size(bbox, pixel_size=0.25):
    """
    Compute the size of the image to be requested in pixels based on the
    bounding box and the pixel size.

    Parameters
    ----------
    bbox : list of float
        The coordinates of the bounding box. [xmin, ymin, xmax, ymax]
    pixel_size : float
        The desired pixel size of the requested image.

    Returns
    -------
    img_size : tuple of int
        The size of the image to be requested in pixels. (x, y)
    """
    dif_x = bbox[2] - bbox[0]
    dif_y = bbox[3] - bbox[1]
    aspect_ratio = dif_x / dif_y
    resolution = int(dif_x * (1/pixel_size))
    img_size = (resolution, int(resolution / aspect_ratio))

    return img_size


def retrieve_image(bbox, wms_url, wms_layer, wms_srs, wms_version,
                   wms_format, pixel_size, max_image_size, retries=10):
    """
    Retrieve the imagery from a WMS service for the given bounding box.

    Parameters
    ----------
    bbox : list of float
        The coordinates of the bounding box. [xmin, ymin, xmax, ymax]
    wms_url : str
        The url of the WMS service to use.
    wms_layer : str
        The layer of the WMS service to use.
    wms_srs : str
        The spatial reference system of the WMS data to request.
    wms_version : str
        The image format of the WMS data to request.
    wms_format : str
        The version number of the WMS service.
    pixel_size : float
        The desired pixel size of the requested image.
    max_image_size : int
        The maximum size (in pixels) of the largest side of the requested
        image.
    retries : int
        Amount of times to retry retrieving an image from the WMS if it
        fails.

    Returns
    -------
    img : (MxNx3) array
        The RGB values of each pixel
    """
    [xmin, ymin, xmax, ymax] = bbox

    x_range = xmax - xmin
    y_range = ymax - ymin
    longest_side = max([x_range, y_range])

    if (longest_side * (1/pixel_size) > max_image_size):
        length = max_image_size / (1/pixel_size)
        length_pixels = max_image_size

        rows = int(math.ceil((ymax-ymin)/length))
        cols = int(math.ceil((xmax-xmin)/length))

        img = np.zeros((length_pixels*rows, length_pixels*cols, 3))

        for col in range(cols):
            for row in range(rows):
                cell = [xmin+col*length, ymin+row*length,
                        xmin+(col+1)*length, ymin+(row+1)*length]

                img_part = request_image(cell, (length_pixels, length_pixels),
                                         wms_url, wms_layer, wms_srs,
                                         wms_version, wms_format, retries)

                img[((length_pixels*rows)-(row+1) *
                     length_pixels):(length_pixels*rows)-row*length_pixels,
                    col*length_pixels:(col+1)*length_pixels] = img_part

        img = img[(length_pixels*rows)-int(y_range*(1/pixel_size)):,
                  :int(round(x_range*(1/pixel_size)))]
    else:
        size = image_size(bbox)
        img = request_image(bbox, size, wms_url, wms_layer, wms_srs,
                            wms_version, wms_format, retries)

    return img


def las_colorize(ins, outs):
    """
    PDAL python function. Adds RGB information to a LAS file by downloading
    an orthophoto from a WMS service.

    Parameters
    ----------
    ins : PDAL input
    outs : PDAL output
    """
    X = ins['X']
    Y = ins['Y']

    [xmin, ymin, xmax, ymax] = [min(X), min(Y), max(X), max(Y)]

    if pdalargs['las_srs'] != pdalargs['wms_srs']:
        p1 = pyproj.Proj(init=pdalargs['las_srs'])
        p2 = pyproj.Proj(init=pdalargs['wms_srs'])
        [xmin, ymin] = pyproj.transform(p1, p2, xmin, ymin)
        [xmax, ymax] = pyproj.transform(p1, p2, xmax, ymax)

    bbox = [xmin, ymin, xmax, ymax]

    img = retrieve_image(bbox, pdalargs['wms_url'], pdalargs['wms_layer'],
                         pdalargs['wms_srs'], pdalargs['wms_version'],
                         pdalargs['wms_format'], float(pdalargs['wms_pixel_size']),
                         int(pdalargs['wms_max_image_size']))

    img_size = img.shape[:2]

    x_img = np.round(((X - xmin) / (xmax-xmin)) *
                     (img_size[1]-1)).astype(int)
    y_img = np.round(((ymax - Y) / (ymax-ymin)) *
                     (img_size[0]-1)).astype(int)

    rgb = img[y_img, x_img] * 255

    outs['Red'] = np.array(rgb[:, 0], dtype=np.uint16)
    outs['Green'] = np.array(rgb[:, 1], dtype=np.uint16)
    outs['Blue'] = np.array(rgb[:, 2], dtype=np.uint16)

    return True
