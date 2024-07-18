import ee
from ee_plugin import Map

image = ee.Image('USGS/SRTMGL1_003')
Map.addLayer(image, {'palette': ['blue', 'red'], 'min': 0, 'max': 5000}, 'dem', True)