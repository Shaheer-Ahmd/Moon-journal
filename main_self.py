from PIL import Image, ImageDraw, ImageFont
from os import listdir
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import math

@dataclass
class Moon:
    azimuth: float
    altitude: float
    phase_name: str
    phase: float
    image: Image

def azimuth_to_x(azimuth:float, width: int)->int:
    w = width
    azimuth_start = 60
    azimuth_end = 300
    delta_azimuth = azimuth_end - azimuth_start
    
    mR = w / ((math.radians(delta_azimuth))) 
    azimuth = azimuth - azimuth_start
    y = mR * math.radians(azimuth)
    # return int(m*azimuth + c)
    # print(f'x: {y} \n azimuth :{azimuth}')
    
    return int(y)

def altitude_to_y(altitude:float, height:int)->int:
    altitude_start = -10 #elevation of the horizon in the image
    altitude_end = 55 # highest elevation
    
    altitude = altitude - altitude_start
    mR =  0.6 * height / math.radians(altitude_end-altitude_start)
    c = 0.4 * height
    y = mR * math.radians(altitude)+ c
    y = height - y
    # return int(m*altitude + c)
    # print(f'y: {y} \n altitude :{altitude}')
    
    return int(y)

if __name__ == "__main__":
    landscape = Image.open('landscape.JPG')
    moon_data = pd.read_excel('moon_coordinates_good.xlsx')
    azimuth = moon_data['Azimuth']
    altitude = moon_data['Altitude']
    phase_name = moon_data['Phase name']
    phase = moon_data['Phase percentage']
    moon_images_dir = 'C:\\Users\\gamer\\Desktop\\LUMS\\Skardu Semester 2023\\Moon_journal\\mirai'
    i = 0
    for moon_image_name in listdir(moon_images_dir):
        moon = Moon(
            azimuth=azimuth[i],
            altitude=altitude[i],
            phase_name=phase_name[i],
            phase=phase[i],
            image=Image.open(moon_images_dir + '\\' + moon_image_name)
        )
        print(f'moon image:{moon_image_name}')
        x = azimuth_to_x(moon.azimuth, 6000)
        y = altitude_to_y(moon.altitude, 4000)
        moon.image = moon.image.resize((100, 100))
        landscape.paste(moon.image, (x-50, y-50, x+50, y+50))
        # beneath each image paste azimuth, altitude
        text = f'{moon.azimuth},{moon.altitude}\n{moon.phase_name}\n{moon.phase}'
        d = ImageDraw.Draw(landscape)
        font = ImageFont.truetype("arial.ttf", 40)
        text_seperation_y = 130
        text_seperation_x = 50
        #to make alternative descriptions appear on top and bottom
        if(i<13):
            if(i%2 != 0):
                d.text((x-text_seperation_x, y-250), text, fill=(255, 255, 255), font=font)
            else:
                d.text((x-text_seperation_x, y+text_seperation_y), text, fill=(255, 255, 255), font=font)    
        elif(i>20):
            d.text((int(x+0.7*text_seperation_x), y+int(0.8*text_seperation_y)), text, fill=(255, 255, 255), font=font)
        else:
            d.text((x-text_seperation_x, y+text_seperation_y), text, fill=(255, 255, 255), font=font)
        d.text((4300,100),"Description Format:\n  Azimuth, Altitude\n  Phase Name\n  Phase Percentage\nNote:\n  First Image is from 22:00 at 20/07/23\n  Each image is taken after 1 day 20m interval", fill=(255, 255, 255), font=ImageFont.truetype("arial.ttf", 80))
        i += 1
        
    current_datetime = datetime.now()
    landscape.save(f'landscape_{current_datetime.strftime("%Y-%m-%d_%H-%M-%S")}.jpeg')
