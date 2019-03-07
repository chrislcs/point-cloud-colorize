mkdir /var/data/arnot/div_color/
python3 point-cloud-colorize/las_colorize.py -i /var/data/arnot/AHN/baarsjes.laz -o /var/data/arnot/div_color/c_10cn2_col.laz -V -d

mkdir /var/data/arnot/div_color/build/
mkdir /var/data/arnot/div_color/cesium/
echo 'colored';
entwine build -i /var/data/arnot/div_color/c_10cn2_col.laz -o /var/data/arnot/div_color/build/ -r EPSG:28992 EPSG:4978;
echo 'build';
entwine convert -i /var/data/arnot/div_color/build/ -o /var/data/arnot/div_color/cesium/;
echo 'converted to cesium';

