import os
import unittest

from point_cloud_colorize.las_colorize import process_files_parallel, process_files


class TestColorizePointcloud(unittest.TestCase):
    def test_unparrallel_processing(self) -> None:
        with self.subTest('It fails if the colorizing fails'):
            input_laz = 'test.laz'
            output_laz = 'test_out.laz'

            process_files(input_path=input_laz,
                          output_path=output_laz,
                          las_srs='EPSG:28992',
                          wms_url='https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?',
                          wms_layer='Actueel_ortho25',
                          wms_srs='EPSG:28992',
                          wms_version='1.3.0',
                          wms_format='image/png',
                          wms_pixel_size=0.25,
                          wms_max_image_size=1000,
                          verbose=False)

    def test_parrallel_processing(self) -> None:
        with self.subTest('It fails if the colorizing fails'):
            input_laz = 'test.laz'
            output_laz = 'test_out_dir'

            process_files_parallel(input=input_laz,
                                   output=output_laz,
                                   las_srs='EPSG:28992',
                                   wms_url='https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?',
                                   wms_layer='Actueel_ortho25',
                                   wms_srs='EPSG:28992',
                                   wms_version='1.3.0',
                                   wms_format='image/png',
                                   wms_pixel_size=0.25,
                                   wms_max_image_size=1000,
                                   verbose=False)

if __name__ == '__main__':
    unittest.main()
