import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join


sets = ['train', 'test', 'val']
classes = ['missing_hole', 'mouse_bite', 'open_circuit', 'short', 'spur', 'spurious_copper']

# 進行歸一化操作
def convert(size, box):         # size:(原圖w,原圖h) , box:(xmin,xmax,ymin,ymax)
    dw = 1./size[0]             # 1/w
    dh = 1./size[1]             # 1/h
    x = (box[0] + box[1])/2.0   # 物體在圖中的中心點x座標
    y = (box[2] + box[3])/2.0   # 物體在圖中的中心點y座標
    w = box[1] - box[0]         # 物體實際畫素寬度
    h = box[3] - box[2]         # 物體實際畫素高度
    x = x*dw                    # 物體中心點x的座標比(相當於 x/原圖w)
    w = w*dw                    # 物體寬度的寬度比(相當於 w/原圖w)
    y = y*dh                    # 物體中心點y的座標比(相當於 y/原圖h)
    h = h*dh                    # 物體寬度的寬度比(相當於 h/原圖h)
    return (x, y, w, h)         # 返回 相對於原圖的物體中心點的x座標比,y座標比,寬度比,高度比,取值範圍[0-1]


def convert_annotation(image_id):
    in_file = open('data/Annotations/%s.xml' % (image_id), encoding='utf-8')
    out_file = open('data/labels/%s.txt' % (image_id), 'w', encoding='utf-8')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')

    if size != None:
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            
            if cls not in classes or int(difficult) == 1:
                continue

            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            print(image_id, cls, b)

            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()
print(wd)

for image_set in sets:
    if not os.path.exists('data/labels/'):
        os.makedirs('data/labels/')

    image_ids = open('data/ImageSets/%s.txt' % (image_set)).read().strip().split()
    list_file = open('data/%s.txt' % (image_set), 'w')

    for image_id in image_ids:
        list_file.write('data/images/%s.jpg\n' % (image_id))
        convert_annotation(image_id)

    list_file.close()