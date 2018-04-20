# encoding:utf-8
'''
@author:lk

@time:2018/4/18 

@desc:

'''
import csv

import os
import urllib.request
import zipfile

from tqdm import tqdm

eg_link='http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize

desc='csv_data.zip'
#des进度条的前缀信息,例如:csv.zip: 9.75MB [00:38, 253kB/s]    表示csv.zip前缀
# unit最小单位
if not os.path.exists(desc) or not os.path.isfile(desc):
    with TqdmUpTo(unit='B', unit_scale=True, miniters=1,
              desc="csv.zip") as t:  # desc取最后一个元素作为文件名
        urllib.request.urlretrieve(eg_link, filename=desc,
                       reporthook=t.update_to, data=None)
urls=[]
# 将zip文件解压
if zipfile.is_zipfile(desc): #is_zipfile() 判断是否似zip文件
    f = zipfile.ZipFile(desc)
    files = f.namelist() #namelist() 返回zip压缩包中的所有文件
    print('files:', files)
    if files:
        with open(files[0], "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for _,url in reader:
                print(_,url)
                urls.append('http://'+url)
    f.close()

