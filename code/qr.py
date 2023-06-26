import time, qrcode
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont

url = "https://www.ready.gov/space-weather"
imageFileName = "qr.jpg"

def getQrCodeImage():
    qrImg = qrcode.make(url)
    qrImg = qrImg.resize((64, 64), Image.NEAREST)
    qrImg = qrImg.convert("RGB")
    qrImg.save(imageFileName)
    return qrImg
