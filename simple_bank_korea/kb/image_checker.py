from PIL import Image
from PIL import ImageChops

img = Image.open('quics.gif')

# 57x57 box
box_5th = Image.open('assets/5.png')
box_7th = Image.open('assets/7.png')
box_8th = Image.open('assets/8.png')
box_9th = Image.open('assets/9.png')
box_0th = Image.open('assets/8.png')

box_list = [box_5th, box_7th, box_8th, box_9th, box_0th]


# 57x57 box
crop_5th = img.crop(box=(74, 99, 131, 156)) # 7

crop_7th = img.crop(box=(16, 157, 73, 214)) #.save('5.png')

crop_8th = img.crop(box=(74, 157, 131, 214)) #.save('9.png')

crop_9th = img.crop(box=(132, 157, 189, 214)) #.save('0.png')

crop_0th = img.crop(box=(74, 215, 131, 272)) #.save('8.png')

crop_list = [crop_5th, crop_7th, crop_8th, crop_9th, crop_0th]

for crop in crop_list:
    for box in box_list:
        tmp = crop.save('tmp.png')
        tmp_img = Image.open('tmp.png')
        print(ImageChops.difference(tmp_img, box))
        # if ImageChops.difference(tmp_img, box):
        #     print('wow1')
        #     print(tmp_img, box)
        #
        # else:
        #     pass
        #     #print(tmp_img, box)
