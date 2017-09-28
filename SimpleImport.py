'''
用于在分享扩展中导入 py 文件到 Pythonista

请先在 Pythonista 的设置中将该脚本设为分享扩展启动选择项之一

By Nicked

https://t.me/nicked
'''

import appex, console, shutil
from os import path


file = 'avi,wmv,mpeg,mp4,mov,mkv,flv,f4v,m4v,rmvb,rm,3gp,dat,ts,mts,vob,m3u8,mp3,aac,wav,wma,cda,flav,m4a,mid,mka,mp2,mpa,mpc,ape,ogg,ra,wv,ac3,dts,jpg,bmp,gif,mif,miff,png,tif,tiff,svg,wmf,jpe,jpeg,pic,webp,txt,md,log,doc,csv,xls,ppt,docx,xlsx,pptx,wps,wpt,dot,rtf,dps,dpt,pot,pps,et,ett,xlt,py,js,html,htm,php,xml,bin,img,iso,mds,nrg,zip,rar,7z,jar,cab,tar,tar.gz,tar.tgz,gz,tgz'
# 文件保存路径
save_dir = path.expanduser('~/Documents')

def simple_import():
	if appex.is_running_extension():
		get_path = appex.get_file_path()
		file_name = path.basename(get_path)
		dstpath = path.join(save_dir, file_name)
		file_pure_name = path.splitext(file_name)[0]
		file_ext = path.splitext(file_name)[-1]
		if file_ext.split('.')[-1] in file:
			new_file_name = ''
			number = 1
			while(path.exists(dstpath)):
				new_file_name = file_pure_name + str(number) + file_ext
				dstpath = path.join(save_dir, new_file_name)
				number += 1
			if new_file_name:
				try:
					while True:
						newname = console.input_alert('文件名已存在', '重命名如下？',new_file_name,'确认', hide_cancel_button=False)
						if not path.exists(path.join(save_dir, newname)):
							break
				except:
					exit()
			else:
				try:
					newname = console.input_alert('确认', '文件名',file_name,'确认', hide_cancel_button=False)
					if path.exists(path.join(save_dir, newname)):
							console.hud_alert('有重名文件，导入失败！', 'error',2)
							exit()
				except:
					exit()
			dstpath = path.join(save_dir, newname)
			try:
				shutil.copy(get_path, dstpath)
				console.hud_alert('导入成功！','',1)
			except Exception as eer:
				print(eer)
				console.hud_alert('导入失败！','error',1)
		else:
			console.hud_alert('格式不支持无法导入', 'error', 2)
	else:
		console.hud_alert('请在分享扩展中打开本脚本','error',2)

if __name__ == '__main__':
	simple_import()
