import os 
os.getcwd()
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS 

import webbrowser
import time
from selenium import webdriver

def get_exif(img):
    labeled = {}
    image = Image.open(img)
    image.verify()
    info = image._getexif()
    for (tag, val) in info.items():
        labeled[TAGS.get(tag, tag)] = val 
    return labeled  

exif = get_exif('IMG_5851.jpg')
print(exif)

def get_geotag(exif):
    if not exif: 
        raise ValueError("No EXIF metadata found.")
    geotagging = {}
    if 'GPSInfo' not in exif:
        raise ValueError("No EXIF geotagging found")
    else: 
        for (key, val) in GPSTAGS.items():
            if key in exif['GPSInfo']:
                geotagging[val] = exif['GPSInfo'][key]
    return geotagging 

tag = get_geotag(exif)

def get_decimal(dms, ref):
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0
    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds
    return round(degrees + minutes + seconds, 6)

def get_coordinates(tag):
    latitude = get_decimal(tag['GPSLatitude'], tag['GPSLatitudeRef'])
    longitude = get_decimal(tag['GPSLongitude'], tag['GPSLongitudeRef'])
    return (latitude, longitude)

coord= get_coordinates(tag)

def get_all(directory): 
    pass 

def web_search(coordinates):
    webbrowser.open('https://google.com/search?q='+str(coordinates))
    return None

# web_search(coord)

def make_mymap():
    # driver_path = r'/Users/brianha/Documents/WebDriver'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    driver = webdriver.Chrome(executable_path = DRIVER_BIN)  # Optional argument, if not specified will search path.
    driver.get('https://www.google.com/maps/d/u/0/?hl=en')
    time.sleep(2) # Let the user actually see something!
    # search_box = driver.find_element_by_name('q')
    # search_box.send_keys('ChromeDriver')
    # search_box.submit()
    time.sleep(5) # Let the user actually see something!
    driver.quit()
    return None

