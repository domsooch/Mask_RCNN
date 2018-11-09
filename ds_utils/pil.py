import os, sys, PIL, json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from base64 import b64encode, b64decode
import numpy as np
import cv2 as cv


def render_line_from_pointLst(image, pLst, fill=128):
    draw = ImageDraw.Draw(image)
    plen = len(pLst)
    for p in range(1, plen, 1):
        x,y = pLst[p]
        draw.line(pLst[p-1]+ pLst[p], fill=fill)
    draw.line(pLst[-1]+ pLst[0], fill=fill)
    

def PlotPoly(jipath):
    #Works with json files that have Image stored as base64 encrypted string
    ji = json.load(open(jipath))
    istr = ji['imageData']
    #HTML("<img src='data:image/png;base64,{0}'/>".format(istr))#Must be the last thing you do
    image_data = b64decode(istr)
    image = Image.open(BytesIO(image_data))
    print(jipath, image.size)
    for sh in ji['shapes']:
        render_line_from_pointLst(image, sh['points'], fill=128)
    return image

def count_pixels(img):
    x,y = img.size

def img_frombytes(data):
    size = data.shape[::-1]
    print(data.shape, 'data_size', size)
    databytes = np.packbits(data, axis=1)
    return Image.frombytes(mode='1', size=size, data=databytes)

def MaskToPointLst(m):
    contours, pntLst, x = cv.findContours(np.uint8(m), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_KCOS)#cv.CHAIN_APPROX_SIMPLE)
    return[list(p[0]) for p in pntLst[0]]
    
    
if __name__ == '__main__':
    train_ud = ms_udfix(r"C:\Users\Public\Segmentation\seg-countertops\annotationsWithImages\\")
    imgjson_files = [os.path.join(train_ud, pos_json) for pos_json in os.listdir(train_ud) if pos_json.endswith('.json')]
    print(train_ud)
    jipath = random.choice(imgjson_files)
    if 1:
        ipath = jipath.replace('.json', '.jpg')
        pil_im = Image.open(ipath)
        display(pil_im)
    PlotPoly(jipath)