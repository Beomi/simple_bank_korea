from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import math, operator
from functools import reduce
import shutil
import time
import re
from io import BytesIO


def get_keypad_img():
    area_hash_list = []
    area_pattern = re.compile("'(\w+)'")
    driver = webdriver.PhantomJS()
    driver.set_window_size('1920', '1080')
    try:
        driver.implicitly_wait(10)
        driver.get('https://bobank.kbstar.com/quics?page=C025255&cc=b028364:b028702&QSL=F#loading')
        quics_img = driver.find_element_by_css_selector('img[src*="quics"]')
        area_list = driver.find_elements_by_css_selector('map > area')

        for area in area_list:
            re_matched = area_pattern.findall(area.get_attribute('onmousedown'))
            if re_matched:
                area_hash_list.append(re_matched[0])

        img_url = quics_img.get_attribute('src')
        usemap = quics_img.get_attribute('usemap').replace('#divKeypad','')[:-3]
        print(img_url, usemap)
        driver.get(img_url)
        print(driver.save_screenshot('screenshot.png'))

        blank_img = Image.open('blank.gif')

        screenshot = Image.open('screenshot.png')
        bbox = screenshot.getbbox()
        print(bbox)
        screenshot.crop(box=(0,0,205,336)).save('real.png')
        # print(response.content)
        # Image.open(BytesIO(response.content)).save('quics.gif')
        driver.quit()
        return area_hash_list
    except Exception as e:
        driver.quit()
        print(e)


def rmsdiff(im1, im2):
    h = ImageChops.difference(im1, im2).histogram()
    return math.sqrt(reduce(operator.add,
                            map(lambda h, i: h * (i ** 2), h, range(256))
                            ) / (float(im1.size[0]) * im1.size[1]))


def get_keypad_num_list(img):
    # 57x57 box
    box_5th = Image.open('assets/5.png')
    box_7th = Image.open('assets/7.png')
    box_8th = Image.open('assets/8.png')
    box_9th = Image.open('assets/9.png')
    box_0th = Image.open('assets/0.png')

    box_dict = {
        5: box_5th,
        7: box_7th,
        8: box_8th,
        9: box_9th,
        0: box_0th,
    }

    # 57x57 box
    crop_5th = img.crop(box=(74, 99, 131, 156))
    crop_7th = img.crop(box=(16, 157, 73, 214))
    crop_8th = img.crop(box=(74, 157, 131, 214))
    crop_9th = img.crop(box=(132, 157, 189, 214))
    crop_0th = img.crop(box=(74, 215, 131, 272))

    crop_list = [crop_5th, crop_7th, crop_8th, crop_9th, crop_0th]

    keypad_num_list = []

    for idx, crop in enumerate(crop_list):
        tmp = crop.save('tmp_{}.png'.format(idx))
        tmp_img = Image.open('tmp_{}.png'.format(idx))
        for key, box in box_dict.items():
            diff = rmsdiff(tmp_img, box)
            if diff < 13:
                keypad_num_list += [key]
            else:
                print(diff)

    print(keypad_num_list)


if __name__ == '__main__':
    get_keypad_img()
    # get_keypad_num_list(
    #    img=Image.open('https://obank.kbstar.com/quics?asfilecode=523225&s=1267777411&keytype=3&dummy=4f9e919e9f3e'))
