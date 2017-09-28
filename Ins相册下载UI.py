#coding: utf-8
import re, json, time, requests, ui, clipboard, console, os, sys
from os import makedirs, path
from math import ceil
from multiprocessing.dummy import Pool
r = requests.Session()
heads = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
'Referer': 'https://www.instagram.com/' }
r.headers.update(heads)

def clip_check():
	if clipboard.get().startswith('http') and 'instagram' in clipboard.get():
		ui.delay(get_user_info,1)
		return clipboard.get()
	else:
		return '剪贴板内容非Ins地址！'

@ui.in_background	
def get_user_info():
	global user_name, full_name, user_id, user_img, user_followed, user_postcount, user_img_data
	user_name = clipboard.get().split('/')[-1]
	url = 'https://www.instagram.com/'+user_name
	try:
		html = r.get(url).text
	except Exception as e:
		view.username.text = '无法连接！请刷新重试！'
		view.status.text = str(e)
		exit()
	html_json_str = re.findall("(?<=window\.\_sharedData\s=\s).+?(?=\;\<\/script\>)",html)[0]
	html_json = json.loads(html_json_str)['entry_data']['ProfilePage'][0]['user']
	full_name = html_json['full_name'] or user_name
	user_id = html_json['id']
	user_img = html_json['profile_pic_url_hd']
	user_followed = html_json['followed_by']['count']
	user_postcount = html_json['media']['count']
	view.userinfo.text = '帖子:{} 关注者:{:.1f}千'.format(user_postcount,user_followed/1000)
	view.username.text = full_name
	user_img_data = r.get(user_img).content
	view.userimg.image = ui.Image.from_data(user_img_data)
	view.downbutton.enabled = True

def make_download_dir():
	dir = path.join(path.expanduser('~/Documents/instagram'),user_name)
	if not path.isdir(dir):
		makedirs(dir)
	return dir
	
def get_media_code():
	global after_id, media_code
	url = 'https://www.instagram.com/graphql/query/'
	query_var = {'id':user_id, 'first':500, 'after':after_id}
	query_params = {'query_id':'17888483320059182', 'variables': json.dumps(query_var)}
	try:
		res = r.get(url, params=query_params)
	except:
		return False
	try:
		res_json = json.loads(res.text)['data']['user']['edge_owner_to_timeline_media']
		code =  [ i['node']['shortcode'] for i in res_json['edges'] ]
		media_code.extend(code)
		view.status.text = '正在发起请求...\n完成{}  |  剩余{}'.format(len(media_code),user_postcount-len(media_code))
		after_id = res_json['page_info']['end_cursor']
	except:
		return False
	return True

def get_media_url(code):
	global image_url, video_url, media_code
	url = 'https://www.instagram.com/p/{}/?__a=1'.format(code)
	try:
		res = r.get(url).text
	except:
		return False
	try:
		res_json = json.loads(res)['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
		image = [ i['node']['display_url'] for i in res_json if not i['node']['is_video'] ]
		video = [ i['node']['video_url'] for i in res_json if i['node']['is_video'] ]
		image_url.extend(image)
		video_url.extend(video)
	except:
		try:
			res_json = json.loads(res)['graphql']['shortcode_media']
			if res_json['is_video']:
				video_url.append(res_json['video_url'])
			else:
				image_url.append(res_json['display_url'])
		except:
			return False
	media_code.remove(code)
	view.status.text = '正在抓取下载地址...\n已抓取到{}张图片和{}个视频'.format(len(image_url),len(video_url))

def download(item):
	global down_count, down_size, image_url, video_url
	try:
		data = r.get(item,timeout=10).content
	except:
		return False
	down_count += 1
	if down_mode == 'image':
		file_path = '{}/{}-{}.jpg'.format(down_dir,user_name,down_count)
		with open(file_path,'wb') as file:
			file.write(data)
		image_url.remove(item)
		if down_count%20 == 0:
			view.userimg.image = ui.Image.named(file_path)
			
	elif down_mode == 'video':
		file_path = '{}/{}-{}.mp4'.format(down_dir,user_name,down_count)
		with open(file_path,'wb') as file:
			file.write(data)
		video_url.remove(item)
		view.userimg.image = ui.Image.from_data(user_img_data)
		
	down_size += path.getsize(file_path)/1000000
	speed = down_size/(time.time()-start_time)
	view.status.text = '正在下载...\n平均速度:{:.1f}M/S\n已下:{} | 剩余: {}'.format(speed,down_count,len(image_url)+len(video_url))

@ui.in_background
def downbutton_tapped(sender):
	global after_id, image_url, video_url, media_code, down_dir, down_count, down_mode, start_time, down_size
	view.downbutton.enabled = False
	console.set_idle_timer_disabled(True)
	view.status.text = '正在与Instagram服务器通讯...'
	query_num = ceil(user_postcount/500)
	query_count = 0
	after_id = ''
	image_url = []
	video_url = []
	media_code = []
	view.status.text = '向服务器请求ShortCode...'
	while query_count < query_num:
		if not get_media_code():
			time.sleep(3)
		else:
			query_count += 1
	view.status.text = '获取ShortCode完成！'
	time.sleep(1)
	view.status.text = '遍历贴文抓取下载地址...'
	while media_code:
		pool = Pool(40)
		pool.map(get_media_url,media_code)
		pool.close()
		pool.join()
	view.status.text = '下载地址抓取完成！'
	time.sleep(1)
	view.status.text = '准备下载...'
	down_dir = make_download_dir()
	down_count = 0
	down_size = 0
	start_time = time.time()
	while image_url:
		down_mode = 'image'
		pool = Pool(30)
		pool.map(download,image_url)
		pool.close()
		pool.join()
	while view.videobutton.value and video_url:
		down_mode = 'video'
		pool = Pool(30)
		pool.map(download,video_url)
		pool.close()
		pool.join()
	console.set_idle_timer_disabled(False)
	view.downbutton.enabled = True
	end_time = time.time()
	view.status.text = '下载完成!耗时{:.0f}秒，平均{:.1f}M/S。\n共下载{}项,总大小{:.1f}MB。\n保存在目录instagram/{}内。'.format(end_time-start_time,down_size/(end_time-start_time),down_count,down_size,user_name)


class RootView (ui.View):
	
	def __init__(self):
		self.bg_color = '#ffffff'
		self.name = 'Ins相册批量下载'
		self.tint_color = 'white'
		
		self.refresh = ui.ButtonItem()
		self.refresh.title = '刷新剪贴板'
		self.refresh.action = self.refresh_tapped
		self.right_button_items = [self.refresh]
		
		self.clipview = ui.Label()
		self.clipview.frame = (0,0,w,40)
		self.clipview.number_of_lines = 2
		self.clipview.alignment = ui.ALIGN_CENTER
		self.clipview.text = clip_check()

		self.username = ui.Label()
		self.username.frame = (0,40,w,40)
		self.username.font = ('<System-Bold>',22)
		self.username.alignment = ui.ALIGN_CENTER
		self.username.number_of_lines = 2
		self.username.text_color = '#d600b7'
		self.username.text = '等待获取用户信息...'
		
		self.userinfo = ui.Label()
		self.userinfo.frame = (0,85,w,40)
		self.userinfo.font = ('<System>',18)
		self.userinfo.alignment = ui.ALIGN_CENTER
		self.userinfo.text_color = '#5c5c5c'
		self.userinfo.text =  '帖子：0 关注者：0'
						
		self.userimg = ui.ImageView()
		self.userimg.frame = ((w-220)/2,140,220,220)
		self.userimg.image = ui.Image.named('iob:load_d_256')
		self.userimg.border_width = 1
		self.userimg.border_color = '#aab0b0'
		
		self.videobutton = ui.Switch()
		self.videobutton.frame = (210,395,50,40)
		self.videobutton.tint_color = 'red'
		self.videobutton.value = False
		self.videobutton_title = ui.Label()
		self.videobutton_title.alignment = ui.ALIGN_CENTER
		self.videobutton_title.frame = ((w-180)/2,390,100,40)
		self.videobutton_title.font = ('<System>',20)
		self.videobutton_title.text = '下载视频'
		
		self.downbutton = ui.Button()
		self.downbutton.frame = ((w-180)/2,450,180,40)
		self.downbutton.border_width = 1.2
		self.downbutton.border_color = '#b1b1b1'
		self.downbutton.font = ('<System-Bold>',20)
		self.downbutton.title = '下载'
		self.downbutton.tint_color = 'white'
		self.downbutton.bg_color = '#1e8173'
		self.downbutton.corner_radius = 10
		self.downbutton.enabled = False
		self.downbutton.action = downbutton_tapped
		
		self.status = ui.Label()
		self.status.frame = (0,495,w,100)
		self.status.alignment = ui.ALIGN_CENTER
		self.status.number_of_lines = 0
		self.status.font = ('<System-Bold>',18)
		
		self.add_subview(self.clipview)
		self.add_subview(self.username)
		self.add_subview(self.userinfo)
		self.add_subview(self.downbutton)
		self.add_subview(self.videobutton)
		self.add_subview(self.videobutton_title)
		self.add_subview(self.status)
		self.add_subview(self.userimg)
	
	def refresh_tapped(self,sender):
		self.clipview.text = clip_check()
	
	def will_close(self):
		console.set_idle_timer_disabled(False)
	
w,h = ui.get_screen_size()
view = RootView()
view.present(title_bar_color='#1e8173',title_color='white')
		
		
