import os 
import appex
import console

def folder_size(folder_path):
	#size = sum(os.path.getsize(f) for f in os.listdir(folder_path) if os.path.isfile(f))
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(folder_path):
		total_size += sum(os.path.getsize(os.path.join(dirpath, name)) for name in filenames)
#		for f in filenames:
#			fp = os.path.join(dirpath, f)
#			total_size += os.path.getsize(fp)
	return total_size

def actualSize(total_size):
	if total_size / 1024 >= 1024:
		total_size = str(round(total_size / 1024 / 1024, 2)) + ' MB'
	else:
		total_size = str(round(total_size / 1024, 1)) + ' KB'
	return total_size
	
def capacitySize(total_size):
	if total_size / 1000 >= 1000:
		total_size = str(round(total_size / 1000 / 1000, 2)) + ' MB'
	else:
		total_size = str(round(total_size / 1000, 1)) + ' KB'
	return total_size

def get_size():
	if appex.is_running_extension():
		path = appex.get_file_path()
		if not os.path.exists(path):
			raise Exception('文件路径不存在')
		if os.path.isfile(path):
			size = os.path.getsize(path)
		else:
			size = folder_size(path)
		console.clear()
		console.set_color(0.3,0.3,1)
		console.set_font('Menlo',20)
		print('文件名称: ' + path.split('/')[-1])	
		print('文件大小: ' + actualSize(size))
		print('占用空间: ' + capacitySize(size))
	else:
		console.hud_alert('请在分享扩展中打开本脚本', 'error', 2)
if __name__ == '__main__':
	get_size()
