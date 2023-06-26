from analyze_gscale_days_cycle25 import getStormDays
from PIL import Image, ImageDraw, ImageFont

imageFileName = "storm-days-panel.jpg"
noaaScaleColors = [(0,255,0),(254,237,0),(254,192,0),(254,150,0),(237,0,0),(178,0,0)]
font = ImageFont.truetype("pixelmix.ttf", 8)


def getStormDaysImage():
    image = Image.new("RGB", (64, 64), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    stormDaysSummary = getStormDays()
    
    draw.text((3,0), "Storm Days", fill=(255, 255, 255), font=font)
    draw.text((17,8), "Stats", fill=(255, 255, 255), font=font)
    
    for i in range(5):
        stormDays = stormDaysSummary[i+1][0]
        stormDaysMean = stormDaysSummary[i+1][1]
        stormDayPercent = round(100 * stormDays/stormDaysMean)
        stormDaysMean = round(stormDaysMean)
        draw.text((0,20+9*i), "G"+str(i+1), fill=noaaScaleColors[i+1], font=font)
        draw.text((14,20+9*i), str(stormDays) + "/" + str(stormDaysMean), fill=(255, 255, 255), font=font)
        if stormDayPercent // 10 == 1:
            draw.text((63-15,20+9*i), str(stormDayPercent) + "%", fill=(0, 0, 255), font=font)
        elif stormDayPercent // 10 == 0:
            draw.text((63-10,20+9*i), str(stormDayPercent) + "%", fill=(0, 0, 255), font=font)
    
    image.save(imageFileName)
    return image
    
    