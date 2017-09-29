# -*- coding: utf-8 -*-
#!python2
from multiprocessing.dummy import Pool as ThreadPool
import os
import requests
import re
import time
import sys
import console
import appex
from bs4 import BeautifulSoup


def config_url(url):
    url = re.findall('.*\d{5}\/', url)[0]
    hs = requests.get(url)
    hs.encoding = 'utf-8'
    soup = BeautifulSoup(hs.text)
    pattern_zhang = u'\d{2,3}张'
    pattern_name = '(?<=<h1 id="htilte">).*(?=</h1>)'
    img_zhang = re.findall(pattern_zhang, hs.text)[0]
    img_num = int(img_zhang[0:-1])
    print(hs.text)
    #folder_name = re.findall(pattern_name, hs.text)[0]
    folder_name = soup.h1.string
    print(folder_name)
    doc_path = os.path.join(os.path.expanduser('~/Documents/Downloads'),'Zngirls_Images')
    folder_path = os.path.join(doc_path, folder_name)
    pattern_url = '(?<=gallery)\/\d{5}\/\d{5}\/(?=s)'
    match_url = re.findall(pattern_url, hs.text)[0]
    url_head = 'https://t1.onvshen.com:85/gallery' + match_url + 's/'
    img_url = []
    img_url.append(url_head + '0.jpg')
    for i in range(1, img_num):
        if i <= 9:
            img_url.append(url_head + '00' + str(i) + '.jpg')
        elif i <= 99:
            img_url.append(url_head + '0' + str(i) + '.jpg')
        else:
            img_url.append(url_head + str(i) + '.jpg')
    config = {'img_num': img_num, 'img_url':img_url,'folder_name': folder_name,'folder_path': folder_path}
    return config


def folder_size(folder_path):
    #size = sum(os.path.getsize(f) for f in os.listdir(folder_path) if os.path.isfile(f))
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    if total_size // 1024 >= 1024:
        total_size = str(round(total_size // 1024 // 1024, 1)) + 'MB'
    else:
        total_size = str(total_size // 1024) + 'KB'
    return total_size



def download_img(url):
    global down_count, dp_count, img_num
    down_count = down_count + 1
    dp_count = dp_count + 1
    console.set_color(.2,.8,.2)
    dp = '□' * 10
    status = '下载中'
    if dp_count > 9:
        dp_count = 0
    if down_count == img_num:
        console.set_color(1,0,.8)
        dp_count = 10
        status = '完成!'
    dp = dp.replace('□', '■', dp_count)
    sys.stdout.write('\r' + status + dp +
                     '(' + str(down_count) + '/' + str(img_num) + ')')
    sys.stdout.flush()
    header = {'Referer': 'https://www.nvshens.com'}
    img_data = requests.get(url, headers=header, timeout=10).content
    img_name = url.split('/')[-1]
    with open(folder_path + '/' + img_name, 'wb') as handler:
        handler.write(img_data)


if __name__ == '__main__':
    # 初始化设置
    global folder_path
    down_count = 0
    dp_count = 0
    config = {}
    url = appex.get_url()
    # url = 'https://www.nvshens.com/g/22377/10.html'
    config = config_url(url)
    # 生成的存储图像路径，map 的函数接受一个参数，故用了全局参数作为存图路径
    folder_name = config['folder_name']
    img_num = config['img_num']
    download_url_list = config['img_url']
    folder_path = config['folder_path']
    if os.path.isdir(folder_path):
        pass
    else:
        os.makedirs(folder_path)
    # 下载图像
    console.clear()
    console.set_color(1,0,.8)
    console.set_font('Menlo',17)
    t1 = int(time.time())
    pool2 = ThreadPool(20)
    pool2.map(download_img, download_url_list)
    pool2.close()
    pool2.join()
    t2 = int(time.time())
    total_size = folder_size(folder_path)
    print('\n共计下载图片: ' + str(img_num) + '张\n耗时: ' + str(t2 - t1) +
          '秒。\n文件夹大小:' + total_size + '\n文件默认保存在桌面:' + folder_name)
    file_list = []
    for i in range(0, img_num):
	    file_name = download_url_list[i].split('/')[-1]
	    file_list.append(os.path.join(folder_path,file_name))
    console.quicklook(file_list)
    exit()
