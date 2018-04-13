#encoding:utf-8
__author__='APLK'

from PIL import Image,ImageDraw,ImageFont
def drawNum(num):
    im = Image.open('E:\python_demo\hello\\answer\\0000.png')
    width,height = im.size
    x=width*0.9
    y=height*0.03
    font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 25)
    draw = ImageDraw.Draw(im)
    draw.ellipse((x-9,y,x+21,y+30),fill=(255,25,55))
    draw.text((x,y),str(num),fill=(255,255,255),font=font)
    im.save('E:\python_demo\hello\\answer\\0000-1.png','png')

drawNum(5)

