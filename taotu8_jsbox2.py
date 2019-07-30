import sys
import appex
import clipboard
#from multiprocessing.dummy import Pool as ThreadPool
import os
import requests
import time
import webbrowser
import console
from multiprocessing.pool import ThreadPool
def url_response(url):
	
	img_name = url.split('/')[-1]
	path = folder_path + '/' + img_name
	r = requests.get(url, timeout=7,stream = True)
	with open(path, 'wb') as f:
		for ch in r:
			f.write(ch)
if __name__ == '__main__':
	# 初始化
	console.clear()
	folder_name = sys.argv[1]
	IMGList = sys.argv[2].split(',')
	doc_path = os.path.join(os.path.expanduser('/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/Downloads'),'TaoTu8_Images')
	folder_path = os.path.join(doc_path, folder_name)
	if os.path.isdir(folder_path):
		pass
	else:
		os.makedirs(folder_path)
	start = time.time()
	len = len(IMGList)
	ThreadPool(len).imap_unordered(url_response, IMGList)

	print(f"Time to download: {time.time() - start}")
	print('图片数量:'+str(len))
	time.sleep(1)
	webbrowser.open('jsbox://')


