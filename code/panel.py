import time, sys
from panel_util import setupPanelOptions
from sw_current import getCurrentGeoMagDataImage
from qr import getQrCodeImage
from sw_forecast import getForecastDataImage
from sw_storm_days import getStormDaysImage
from sw_disturbance import getDisturbanceChangeImage
from rgbmatrix import RGBMatrix
from PIL import Image, ImageDraw, ImageFont

options = setupPanelOptions()
matrix = RGBMatrix(options = options)

while True:
    try:
        image, qrRequired = getCurrentGeoMagDataImage()
        matrix.SetImage(image)
        time.sleep(2)
        # if qrRequired:
        #     image = getQrCodeImage()
        #     matrix.SetImage(image)
        image = getForecastDataImage()
        matrix.SetImage(image)
        time.sleep(2)
        image = getStormDaysImage()
        matrix.SetImage(image)
        time.sleep(2)
        image = getDisturbanceChangeImage()
        matrix.SetImage(image)
        time.sleep(2)
    except KeyboardInterrupt:
        break
    
while True:
    try:
        time.sleep(100)
    except KeyboardInterrupt:
        break
