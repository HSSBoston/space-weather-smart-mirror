import requests, pandas as pd
from datetime import datetime
from sw_current import drawCurrentDate, getCurrentDate
from PIL import Image, ImageDraw, ImageFont

imageFileName = "geomag-forecast-panel.jpg"

noaaUrl = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"
noaaHistUrl = "https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt"
forecastFileName = "3-day-forecast.txt"
histFileName = "daily-geomagnetic-indices.txt"

noaaScaleColors = [(0,255,0),(254,237,0),(254,192,0),(254,150,0),(237,0,0),(178,0,0)]
font = ImageFont.truetype("pixelmix.ttf", 8)

def drawDays(draw):
    daysOfWeek = ["M", "T", "W", "T", "F", "S", "S"]
    today = datetime.now().weekday()
    dowId = today - 4
    for i in range(7):
        if dowId + i <= 6:
            if dowId + i == today:
                draw.text((12 + i*7, 56), daysOfWeek[dowId + i], fill=(0, 0, 255), font=font)
            else:
                draw.text((12 + i*7, 56), daysOfWeek[dowId + i], fill=(255, 255, 255), font=font)
        elif dowId + i >= 7:
            if dowId + i == today:
                draw.text((12 + i*7, 56), daysOfWeek[dowId + i - 7], fill=(0, 0, 255), font=font)
            else:
                draw.text((12 + i*7, 56), daysOfWeek[dowId + i - 7], fill=(255, 255, 255), font=font)

def downloadData(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to download data:", response.status_code, response.text)
        return None

def kpDecimal2kp(kpDecimal):
    if kpDecimal < 0.67:
        return 0
    if kpDecimal >= 0.67 and kpDecimal <= 1.33:
        return 1
    if kpDecimal >= 1.67 and kpDecimal <= 2.33:
        return 2
    if kpDecimal >= 2.67 and kpDecimal <= 3.33:
        return 3
    if kpDecimal >= 3.67 and kpDecimal <= 4.33:
        return 4
    if kpDecimal >= 4.67 and kpDecimal <= 5.33:
        return 5
    if kpDecimal >= 5.67 and kpDecimal <= 6.33:
        return 6
    if kpDecimal >= 6.67 and kpDecimal <= 7.33:
        return 7
    if kpDecimal >= 7.67 and kpDecimal <= 8.67:
        return 8
    if kpDecimal > 8.67:
        return 9

def kpDecimal2NoaaScale(kpDecimal):
    if kpDecimal <= 4.33:
        return 0
    elif kpDecimal >=4.67 and kpDecimal <= 5.33:
        return 1
    elif kpDecimal >=5.67 and kpDecimal <= 6.33:
        return 2
    elif kpDecimal >=6.67 and kpDecimal <= 7.33:
        return 3
    elif kpDecimal >=7.67 and kpDecimal <= 8.67:
        return 4
    elif kpDecimal >=9.0:
        return 5
        
def drawKp(draw):
    response = downloadData(noaaUrl)
    with open(forecastFileName, mode='w') as f:
        f.write(response)

    with open(forecastFileName) as f:
        lines = f.readlines()
        
    forecastData = [] 
    extracting = False
    for line in lines:
        line = line.replace("(G1)", "").replace("(G2)", "").replace("(G3)", "").replace("(G4)", "").replace("(G5)", "")
        if line.startswith("00-03UT"):
            extracting = True
        if extracting:
            forecastData.append(line.split()[1:])
        if line.startswith("21-00UT"):
            break
#     print(forecastData)
    
    df = pd.DataFrame(forecastData, columns=["today","tomorrow","2 days later"])
    kpToday = df.loc[:,"today"].max()
    kpTomorrow = df.loc[:,"tomorrow"].max()
    kp2daysLator = df.loc[:, "2 days later"].max()
    print(kpToday, kpTomorrow, kp2daysLator)
    
    response = downloadData(noaaHistUrl)
    with open(histFileName, mode='w') as f:
        f.write(response)

    with open(histFileName) as f:
        lines = f.readlines()
    
    histData = []
    extracting = False
    for line in lines:
        if extracting:
            histData.append(line.replace("\n", ""))
        if line.startswith("#  Date"):
            extracting = True

    del histData[len(histData)-1]
#     print(histData)
    histData.reverse()
#     print(histData)
    
    recent4days = []
    for i in range(4):
        recent4days.append( histData[i][65:] )
    recent4days.reverse()
    print(recent4days)
    
    historyData = []
    for dailyData in recent4days:
        historyData.append( max(list(map(float, dailyData.split()))) )
    print(historyData)

    kpData = historyData + [float(kpToday), float(kpTomorrow), float(kp2daysLator)]
    print(kpData)
    
    draw.text((0, 10), "Kp", fill=(255, 255, 255), font=font)
    for i in range(7):
        draw.text((12 + i*7, 10), str(kpDecimal2kp(kpData[i])),
                  fill=noaaScaleColors[kpDecimal2NoaaScale(kpData[i])], font=font)

    draw.text((0, 19), "G:", fill=(255, 255, 255), font=font)
    for i in range(7):
        noaaScale = kpDecimal2NoaaScale(kpDecimal2kp(kpData[i]))
        draw.text((12 + i*7, 19), str(noaaScale),
                  fill=noaaScaleColors[noaaScale], font=font)

    for i in range(7):
        kp = kpDecimal2kp(kpData[i])
        draw.rectangle((12 + i*7, 54 - kp*3, (12 + i*7)+5, 54),
                       fill=noaaScaleColors[kpDecimal2NoaaScale(kpData[i])], outline=None)
        

def getForecastDataImage():
    image = Image.new("RGB", (64, 64), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    drawCurrentDate(draw)
    drawDays(draw)
    drawKp(draw)

    image.save(imageFileName)
    return image


