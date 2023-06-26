import ftplib, requests
from analyze_cycle25_length import getProgressInCycle
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

imageFileName = "geomag-current-panel.jpg"

noaaFtpHost = "ftp.swpc.noaa.gov"
port = 21
user = passwd = "anonymous"
noaaGeomagDir = "pub/lists/geomag/"
kIndexFileName = "AK.txt"
noaaAlertsUrl = "https://services.swpc.noaa.gov/products/alerts.json"

noaaScaleColors = [(0,255,0),(254,237,0),(254,192,0),(254,150,0),(237,0,0),(178,0,0)]
font = ImageFont.truetype("pixelmix.ttf", 8)
fontDoubleSize = ImageFont.truetype("pixelmix.ttf", 16)

def getCurrentDate():
    daysOfWeek = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dt = datetime.now()
    yr = dt.year % 2000    
    if dt.month // 10 == 0:
        mo = "0" + str(dt.month)
    else:
        mo = str(dt.month)
    if dt.day // 10 == 0:
        day = "0" + str(dt.day)
    else:
        day = str(dt.day)
    dow = daysOfWeek[dt.weekday()]
    return (str(yr), mo, day, dow)

def kp2NoaaScaleStormLevel(kp):
    if float(kp) <= 4.33:
        noaaScaleKp = 0
        stormLevel = "No storm"
    elif float(kp) >=4.67 and float(kp) <= 5.33:
        noaaScaleKp = 1
        stormLevel = "Minor"
    elif float(kp) >=5.67 and float(kp) <= 6.33:
        noaaScaleKp = 2
        stormLevel = "Moderate"
    elif float(kp) >=6.67 and float(kp) <= 7.33:
        noaaScaleKp = 3
        stormLevel = "Strong"
    elif float(kp) >=7.67 and float(kp) <= 8.67:
        noaaScaleKp = 4
        stormLevel = "Severe"
    elif float(kp) >=9.0:
        noaaScaleKp = 5
        stormLevel = "Extreme"
    return noaaScaleKp, stormLevel

def getKandNoaaScale():
    kp = noaaScaleKp = 0
    planetaryKs = []

    with ftplib.FTP() as ftp:
        try:
            ftp.connect(noaaFtpHost, port)
            ftp.login(user, passwd)
            ftp.cwd(noaaGeomagDir)
            with open(kIndexFileName, "wb") as f:
                ftp.retrbinary("RETR " + kIndexFileName, f.write)
        except ftplib.all_errors as e:
            print("FTP error: ", e)
    
    with open(kIndexFileName) as f:
        lines = f.readlines()
    
    for line in lines:
        if line.startswith("Planetary"):
            planetaryKs = planetaryKs + line.split()[3:]
    try:
        planetaryK = planetaryKs[ planetaryKs.index("-1.00") - 1 ]
        print("Kp: ", planetaryK)
        kp = float(planetaryK)
    except ValueError:
        print("Kp not found. Using Kp=0.")
    
    noaaScaleKp, stormLevel = kp2NoaaScaleStormLevel(kp)
    print("Kp NOAA scale", noaaScaleKp, stormLevel)
    return kp, noaaScaleKp, stormLevel

def drawCurrentDate(draw):
    yr, mon, day, dow = getCurrentDate()
    draw.text((0, 0), mon + "/" +day + "/" + yr, fill=(255, 255, 255), font=font)
    draw.text((47, 0), dow, fill=(255, 255, 255), font=font)

def drawCurrentKp(draw):
    kp, noaaScaleKp, stormLevel = getKandNoaaScale()
    draw.rectangle((0, 10, 13, 27), fill=noaaScaleColors[noaaScaleKp], outline=None)
    
    draw.text((2, 10), str(noaaScaleKp), fill=(61,61,61), font=fontDoubleSize)
    draw.text((16, 10), stormLevel, fill=noaaScaleColors[noaaScaleKp], font=font)
    draw.text((16, 18), "Kp: "+str(kp), fill=(255, 255, 255), font=font)

def downloadJasonData(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to download data:", response.status_code, response.text)
        return None

def drawProgress(draw):
    progressInCycle = getProgressInCycle()
    draw.text((16, 28), str(progressInCycle) + "% done", fill=(255, 255, 255), font=font)
    
def drawAlerts(draw):
    yr, mo, day, dow = getCurrentDate()
    today = mo + "-" + day
#     print(today)
    draw.text((9, 39), "Warnings", fill=(255, 255, 0), font=font)
    
#     draw.text((0, 36), "Warning:", fill=noaaScaleColors[1], font=font)
#     draw.text((0, 44), "Kp5 G1 minor", fill=noaaScaleColors[1], font=font)    
#     draw.text((0, 52), "storm today:", fill=noaaScaleColors[1], font=font)    
        
#     alerts = ["K04W", "K04A","K05W", "K05A","K06W", "K06A","K07W", "K07A","K08W", "K08A","K09W", "K09A"]
    alerts = ["K04W", "K05W", "K06W", "K07W", "K08W", "K09W"]
    currentAlerts = []
    responseList = downloadJasonData(noaaAlertsUrl)
    for alertDict in responseList:
        if alertDict["product_id"] in alerts and today in alertDict["issue_datetime"]:
            currentAlerts.append(alertDict["product_id"])
#             print(alertDict)
    print(len(currentAlerts), "alerts")
    if len(currentAlerts) == 0:
        draw.text((0, 47), "N/A", fill=noaaScaleColors[0], font=font)
    else:
        currentAlerts.sort(reverse=True)
        print(currentAlerts)
        kpInWarning = currentAlerts[0][2]
        noaaScale, stormLevel = kp2NoaaScaleStormLevel(kpInWarning)
        draw.text((0, 47), "Kp" + kpInWarning, fill=(255, 255, 255), font=font)
        draw.text((15, 47), " G" + str(noaaScale), noaaScaleColors[noaaScale], font=font)
        draw.text((35, 47), "storm", fill=(255, 255, 255), font=font)
        draw.text((14, 47+8), stormLevel, fill=noaaScaleColors[noaaScale], font=font)
#         for i in range(len(currentAlerts)):
#             draw.text((0, 44+i*8), currentAlerts[i], fill=(255, 255, 255), font=font)
    return True

def getCurrentGeoMagDataImage():
    image = Image.new("RGB", (64, 64), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    drawCurrentDate(draw)
    drawCurrentKp(draw)
    drawProgress(draw)
    qrRequired = drawAlerts(draw)
    image.save(imageFileName)
    if qrRequired:
        return image, True
    else:
        return image, False

    
