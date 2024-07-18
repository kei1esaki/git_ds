import ee
from dateutil.parser import parse
ee.Initialize()
region=ee.Geometry.Rectangle([105.20,13.10,105.50,12.80])

def cloudMasking(image):
    qa = image.select('QA60')
    cloudBitMask = 1 << 10  
    cirrusBitMask = 1 << 11
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask).divide(10000)

def ImageExport(image,description,folder,region,scale):
    task = ee.batch.Export.image.toDrive(image=image,description=description,folder=folder,region=region,scale=scale)
    task.start()

Sentinel2 = ee.ImageCollection('COPERNICUS/S2').filterBounds(region).filterDate(parse('2015-01-01'),parse('2015-12-31')).map(cloudMasking).select(['B2','B3','B4','B8','B12'])
imageList = Sentinel2.toList(300) 
for i in range(imageList.size().getInfo()):
    image = ee.Image(imageList.get(i))
    ImageExport(image.reproject(crs='EPSG:4326',scale=10),image.get('system:index').getInfo(),'Cambodia',region['coordinates'][0],10)