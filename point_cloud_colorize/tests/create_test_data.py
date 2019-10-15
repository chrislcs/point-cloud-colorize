import json
from typing import Tuple

import pdal
import wget


def crop_tile(bounds: Tuple[float, float, float, float] = (139703.2, 556571.8, 139717.1, 556581.8)) -> None:
    x_min, y_min, x_max, y_max = bounds
    pdal_pipeline = {
        "pipeline": [
            "09HN2.LAZ",
            {"type": "filters.crop", "bounds": f"([{x_min}, {y_min}], [{x_max}, {y_max}])"},
            {"type": "writers.las", "filename": "test.laz"}
        ]
    }
    pipeline = pdal.Pipeline(json.dumps(pdal_pipeline))
    pipeline.validate()
    pipeline.execute()


if __name__ == '__main__':
    url = 'https://geodata.nationaalgeoregister.nl/ahn3/extract/ahn3_laz/C_09HN2.LAZ'
    wget.download(url, '09HN2.LAZ')

    crop_tile()
