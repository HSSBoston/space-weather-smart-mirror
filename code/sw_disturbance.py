import pandas as pd
from PIL import Image, ImageDraw, ImageFont

imageFileName = "geomag-disturbance-panel.jpg"
font = ImageFont.truetype("pixelmix.ttf", 8)

columnNames = ["25", "24", "23", "22", "21", "20", "19", "18", "17", "0"]

def qFunc(x, a, b, c):
    return a * (x-b)**2 + c

def drawCurves(draw):
    df = pd.read_csv("monthly-ma.csv", names=columnNames, skiprows=1)
    print(df)
    
    currentCurve = [float(i) for i in df.loc[:, "25"].dropna().values.tolist()]
    indexList = [int(i) for i in df.loc[:, "0"].index.tolist()]
    print(currentCurve)
    print(indexList)

    param = [-0.00175581001, 72.1211268, 15.9693058]

    regCurve =[]
    for x in indexList:
        regCurve.append(param[0] * (x-param[1])**2 + param[2])
    print(regCurve)
    
    curveX = 0
    for i in range(64):
        regY = round(regCurve[curveX] * 2.5)
        draw.rectangle((i+7, 63-regY, i+7, 63-regY), fill=(255, 153, 0), outline=None)
        if curveX <= len(currentCurve):
            currentY = round(currentCurve[curveX] * 2.5)
            draw.rectangle((i+7, 63-currentY, i+7, 63-currentY), fill=(0, 0, 255), outline=None)
        curveX = curveX + 3
        if curveX >= len(indexList):
            break
                      


def getDisturbanceChangeImage():
    image = Image.new("RGB", (64, 64), (0, 0, 0))
    draw = ImageDraw.Draw(image)

#     draw.text((15,0), "Geomag", fill=(255, 255, 255), font=font)
    draw.text((0,0), "Disturbance", fill=(255, 255, 255), font=font)
    draw.text((9,8), "Progress", fill=(255, 255, 255), font=font)
    
    draw.rectangle((6, 18, 6, 62), fill=(112,128,144), outline=None)
    draw.rectangle((5, 19, 5, 19), fill=(112,128,144), outline=None)
    draw.rectangle((4, 20, 4, 20), fill=(112,128,144), outline=None)
    draw.rectangle((7, 19, 7, 19), fill=(112,128,144), outline=None)
#     draw.rectangle((8, 20, 8, 20), fill=(112,128,144), outline=None)

    draw.rectangle((6, 62, 63, 62), fill=(112,128,144), outline=None)
    draw.rectangle((62, 61, 62, 61), fill=(112,128,144), outline=None)
    draw.rectangle((61, 60, 61, 60), fill=(112,128,144), outline=None)
    draw.rectangle((62, 63, 62, 63), fill=(112,128,144), outline=None)

    draw.text((9,18), "Ap", fill=(112,128,144), font=font)
    draw.text((32,54), "t", fill=(112,128,144), font=font)
    
    drawCurves(draw)

    image.save(imageFileName)
    return image
