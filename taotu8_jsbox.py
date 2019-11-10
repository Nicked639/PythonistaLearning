import console
import sys
import appex
#import clipboard
from multiprocessing.dummy import Pool as ThreadPool
import os
import requests
import time
import webbrowser

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
	down_count = 0
	dp_count = 0
	name = 0
	girl_name = sys.argv[1]
	folder_name = sys.argv[2]
	IMGList = sys.argv[3].split(',')
	doc_path = os.path.join(os.path.expanduser('/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/Downloads'),'TaoTu8_Images')
	girl_path= os.path.join(doc_path,girl_name)
	if not os.path.isdir(girl_path):
 		os.makedirs(girl_path)
	folder_path = os.path.join(girl_path,folder_name)
	if not os.path.isdir(folder_path):
 		os.makedirs(folder_path)
	download_url_list = IMGList
	img_num = len(download_url_list)
	# 下载图像
	console.set_color(1, 0, .8)
	console.set_font('Menlo', 17)
#	t1 = int(time.time())
	start = time.time()
	pool2 = ThreadPool(20)
	pool2.map(download_img, download_url_list)
	pool2.close()
	pool2.join()
#	t2 = int(time.time())

#	total_size = folder_size(folder_path)
#	print('\n'+folder_name+'\n共计下载图片: '+str(len(download_url_list))+'张\n耗时: '+str(t2-t1)+'秒。\n文件夹大小:'+total_size+'\n文件默认保存在根目录:'+folder_name)
	

	print('完成', time.time()-start)
	webbrowser.open('jsbox://')
