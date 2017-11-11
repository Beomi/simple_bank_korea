from PIL import Image
from PIL import ImageChops
from selenium import webdriver

import math, operator
from functools import reduce
import re
import os

from ..libcheck.phantomjs_checker import TMP_DIR

CURRENT_PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_keypad_img(PHANTOM_PATH, LOG_PATH=os.path.devnull):
    area_hash_list = []
    area_pattern = re.compile("'(\w+)'")
    driver = webdriver.PhantomJS(executable_path=PHANTOM_PATH, service_log_path=LOG_PATH)
    driver.set_window_size('1920', '1080')
    driver.implicitly_wait(10)
    driver.get('https://obank.kbstar.com/quics?page=C025255&cc=b028364:b028702&QSL=F')
    if driver.get_cookie('JSESSIONID'):
        JSESSIONID = driver.get_cookie('JSESSIONID').get('value')
    else:
        JSESSIONID = ''
        print('no JSESSIONID')
    if driver.get_cookie('QSID'):
        QSID = driver.get_cookie('QSID').get('value')
    else:
        QSID = ''
        print('no QSID')
    KEYPAD_USEYN = driver.find_element_by_css_selector('input[id*="KEYPAD_USEYN"]').get_attribute('value')
    quics_img = driver.find_element_by_css_selector('img[src*="quics"]')
    area_list = driver.find_elements_by_css_selector('map > area')

    for area in area_list:
        re_matched = area_pattern.findall(area.get_attribute('onmousedown'))
        if re_matched:
            area_hash_list.append(re_matched[0])

    img_url = quics_img.get_attribute('src')
    keymap = quics_img.get_attribute('usemap').replace('#divKeypad', '')[:-3]
    driver.get(img_url)
    driver.save_screenshot(os.path.join(TMP_DIR, 'tmp', 'screenshot.png'))
    screenshot = Image.open(os.path.join(TMP_DIR, 'tmp', 'screenshot.png'))
    real = screenshot.crop(box=(0, 0, 205, 336))
    real.save(os.path.join(TMP_DIR, 'tmp', 'real.png'))
    driver.quit()

    # Get list
    num_sequence = _get_keypad_num_list()

    PW_DIGITS = {}
    # FIXED
    PW_DIGITS['1'] = area_hash_list[0]
    PW_DIGITS['2'] = area_hash_list[1]
    PW_DIGITS['3'] = area_hash_list[2]
    PW_DIGITS['4'] = area_hash_list[3]
    PW_DIGITS['6'] = area_hash_list[5]

    # Floating..
    for idx, num in enumerate(num_sequence):
        if idx == 0:
            PW_DIGITS[str(num)] = area_hash_list[4]
        elif idx == 1:
            PW_DIGITS[str(num)] = area_hash_list[6]
        elif idx == 2:
            PW_DIGITS[str(num)] = area_hash_list[7]
        elif idx == 3:
            PW_DIGITS[str(num)] = area_hash_list[8]
        elif idx == 4:
            PW_DIGITS[str(num)] = area_hash_list[9]

    return {
        'JSESSIONID': JSESSIONID,
        'QSID': QSID,
        'KEYMAP': keymap,
        'PW_DIGITS': PW_DIGITS,
        'KEYPAD_USEYN': KEYPAD_USEYN
    }


def rmsdiff(im1, im2):
    h = ImageChops.difference(im1, im2).histogram()
    return math.sqrt(reduce(operator.add,
                            map(lambda h, i: h * (i ** 2), h, range(256))
                            ) / (float(im1.size[0]) * im1.size[1]))


def _get_keypad_num_list():
    # 57x57 box
    img = Image.open(os.path.join(TMP_DIR, 'tmp', 'real.png'))
    box_5th = Image.open(os.path.join(CURRENT_PACKAGE_DIR, 'assets', '5.png'))
    box_7th = Image.open(os.path.join(CURRENT_PACKAGE_DIR, 'assets', '7.png'))
    box_8th = Image.open(os.path.join(CURRENT_PACKAGE_DIR, 'assets', '8.png'))
    box_9th = Image.open(os.path.join(CURRENT_PACKAGE_DIR, 'assets', '9.png'))
    box_0th = Image.open(os.path.join(CURRENT_PACKAGE_DIR, 'assets', '0.png'))

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
        crop.save(os.path.join(TMP_DIR, 'tmp', 'tmp_{}.png'.format(idx)))
        tmp_img = Image.open(os.path.join(TMP_DIR, 'tmp', 'tmp_{}.png'.format(idx)))
        for key, box in box_dict.items():
            try:
                diff = rmsdiff(tmp_img, box)
                if diff < 13:
                    keypad_num_list += [key]
            except Exception as e:
                print(e)

    return keypad_num_list


if __name__ == '__main__':
    print(get_keypad_img('phantomjs'))  # PATH to phantomjs
    print(_get_keypad_num_list())
