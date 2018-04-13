# encoding:utf-8
__author__ = 'APLK'
'''
 你有一个目录，装了很多照片，把它们的尺寸变成都不大于 iPhone5 分辨率的大小。
'''
from PIL import Image
import os
desDirs='E:/期权二期文档/调整的UI'
saveDirs='E:/期权二期文档/调整的UI/temp'
if not os.path.isdir(saveDirs):
    os.mkdir(saveDirs)
    print(saveDirs)
for file in os.listdir(desDirs):
    picPath = desDirs+"/"+file
    print(picPath+',file='+file.split('.')[0])
    if os.path.isfile(picPath):
        with Image.open(picPath) as img:
            width,height=img.size
            n = width / 1366 if (width / 1366) >= (height / 640) else height / 640
            img.thumbnail((width / n, height / n))
            img.save(saveDirs+'/'+file.split('.')[0]+'.png','png')
