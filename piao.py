import cv2
import numpy as np
import skimage.io as io
from skimage import data_dir
import os
import sys
#import fitz
# from reportlab.lib.pagesizes import portrait
# from reportlab.pdfgen import canvas
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
import pandas as pd

data = pd.read_csv('output.csv')
output_excle = pd.DataFrame(data)
png_str='./bills/*.png'


def img_reshape(img_ori):
    GrayImage = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
    ret, img_thresh = cv2.threshold(GrayImage, 250, 255, cv2.THRESH_BINARY)
    coords = np.column_stack(np.where(img_thresh < 255))
    coords = coords[:, ::-1]  # x, y互换
    min_rect = cv2.minAreaRect(coords)
    box = cv2.boxPoints(min_rect)
    box = np.int0(box)
    cv2.drawContours(img_thresh, [box], 0, [0, 255, 0], 1)
    box_x = [i[0] for i in box]
    box_y = [i[1] for i in box]
    area1 = img_ori[min(box_y):max(box_y), min(box_x):max(box_x)]  # y,x
    img = cv2.resize(area1, (1400, 900))
    return img

def img_div(img_ori):
    img = img_reshape(img_ori)
    # area1 = img[328:522,0:380] #名称
    # area2 = img[328:522,486:568] #单位
    # area3 = img[328:522,568:731] #数量
    area0 = img[328:578, :748]
    area1 = img[328:578, 750:]
    area2 = img[:170, 980:]
    img_vector = []
    img_vector.append(area0)
    img_vector.append(area1)
    img_vector.append(area2)
    return img_vector
    #cv2.namedWindow('ss',0)
    #cv2.imshow('ss', img)
    #cv2.imshow('area1', area1)
    #cv2.imshow('area2', area2)
    #cv2.waitKey(0)

def output_area2(result):
    #points=[]
    strs = []
    i = 0
    for line in result:
        #points.append(line[0][0])
        strs.append(list(line[1][0]))
        #print(line[0])
    #output_excle.
    #print(points)
    #print(strs)



coll = io.ImageCollection(png_str)
print(output_excle.head())
for i in range(len(coll)):
    img_vector = img_div(coll[i])
    cv2.imwrite('./bills_temp/area0.png',img_vector[0])
    cv2.imwrite('./bills_temp/area1.png',img_vector[1])
    cv2.imwrite('./bills_temp/area2.png',img_vector[2])
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    img_path = './bills_temp/area2.png'
    #result = ocr.ocr(img_path, cls=True)
    #output_area2(result)
    
#output_excel.to_excel('./result.xlsx')

#     cv2.imshow('area1', img_vector[0])
#     cv2.imshow('area2', img_vector[1])
#     cv2.waitKey(0)
#pdf2img()