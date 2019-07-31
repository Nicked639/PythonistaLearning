# -*- coding: utf-8 -*-
#!python2
from multiprocessing.dummy import Pool as ThreadPool
import os
import requests
import re
import time
import console
import sys
import appex
import clipboard
import webbrowser

def config_url(url):
	hs = requests.get(url)
	hs.encoding = 'utf-8'
	pattern_name = r'(?<=<title>).*(?=\-)'
	folder_name = re.findall(pattern_name, hs.text)[0]
	#print(folder_name)
	pattern_imagelist= r'lazysrc=[\s\S]*?(.*)(?=  onerror)'
	imagelist = re.findall(pattern_imagelist,hs.text)
	doc_path = os.path.join(os.path.expanduser('/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/Downloads'),'TaoTu8_Images')
	folder_path = os.path.join(doc_path, folder_name)
	config = {'folder_name':folder_name, 'folder_path':folder_path,'image_list':imagelist}
	return config


def folder_size(folder_path):
	# size = sum(os.path.getsize(f) for f in os.listdir(folder_path) if os.path.isfile(f))
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(folder_path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp)
	if total_size // 1024 >= 1024:
		total_size = str(round(total_size//1024//1024, 1))+'MB'
	else:
		total_size = str(total_size//1024) + 'KB'
	return total_size




def download_img(url):
	global down_count, dp_count, img_num, name
	down_count = down_count+1
	dp_count = dp_count+1
	console.set_color(.2, .8, .2)
	dp = '□' * 10
	status = '下载中'
	if dp_count > 9:
		dp_count = 0
	elif down_count == img_num:
		console.set_color(1, 0, .8)
		dp_count = 10
		status = '完成!'
		
	else:
		pass
	dp = dp.replace('□', '■', dp_count)
	sys.stdout.write('\r'+status+dp+'('+str(down_count)+'/'+str(img_num)+')')
	sys.stdout.flush()
	img_data = requests.get(url, timeout=7).content
	# img_name = str(name) + '.jpg'
	img_name = url.split('/')[-1]
	name += 1
	with open(folder_path + '/' + img_name, 'wb') as handler:
		handler.write(img_data)


if __name__ == '__main__':
	# 初始化
	console.clear()
	name = 0
	down_count = 0
	dp_count = 0
	url = appex.get_url()
	if len(sys.argv)>1:
		url = sys.argv[1]
	print('运行中...\n')
	config = config_url(url)

	# 生成图像存储路径, map 的函数接受一个参数，故用了全局参数作为存图路径
	folder_name = config['folder_name']
	folder_path = config['folder_path']
	image_list = config['image_list']
	if os.path.isdir(folder_path):
		pass
	else:
		os.makedirs(folder_path)
	download_url_list = image_list
	img_num = len(download_url_list)
	# 下载图像
	console.set_color(1, 0, .8)
	console.set_font('Menlo', 17)
	t1 = int(time.time())
	pool2 = ThreadPool(20)
	pool2.map(download_img, download_url_list)
	pool2.close()
	pool2.join()

	t2 = int(time.time())
	total_size = folder_size(folder_path)
	print('\n'+folder_name+'\n共计下载图片: '+str(len(download_url_list))+'张\n耗时: '+str(t2-t1)+'秒。\n文件夹大小:'+total_size+'\n文件默认保存在根目录:'+folder_name)

	# 预览下载内容
#	file_list = []
#	for i in range(0, img_num):
#		file_name = download_url_list[i].split('/')[-1]
#		file_list.append(os.path.join(folder_path, file_name))

	
	#webbrowser.open(url)

	sys.exit()
