#coding: utf-8
import appex, requests, ui, re, clipboard

@ui.in_background
def origin_text ():
	if appex.is_running_extension():
		view.origin_text.text = appex.get_text() or requests.get(appex.get_url()).text
	elif clipboard.get().startswith('http'):
		if requests.head(clipboard.get()).headers.get('content-type') == 'text/html':
			view.origin_text.text = requests.get(clipboard.get()).text
		else:
			view.origin_text.text = clipboard.get()
	else:
		view.origin_text.text = clipboard.get()

def macth_text ():
	try:
		macth = re.findall(view.expression_input.text,view.origin_text.text,re.I)
		view.match_count.title = str(len(macth))
		return '\n'.join(macth) or '无结果'
	except:
		return '表达式错误！'
		

class ExpressionInputDelegate (object):
	
	def textfield_did_end_editing(self,textfield):
		if textfield.text:
			view.match_text.text = macth_text()

	def textfield_did_change(self,textfield):
		pass


class RootView (ui.View):
	
	def __init__ (self):
		self.bg_color = '#e9f1f1'
		self.name = '正则表达式测试'
		self.copy_button = ui.ButtonItem()
		self.copy_button.title = '复制表达式'
		self.copy_button.action = self.copy_button_tapped
		self.right_button_items = [self.copy_button]
		self.match_count = ui.ButtonItem()
		self.match_count.title = '0'
		self.match_count.tint_color = 'red'
		self.left_button_items = [self.match_count]
		
		self.expression_input = ui.TextField()
		self.expression_input.frame = (10,5,w-70,40)
		self.expression_input.border_width = 1
		self.expression_input.corner_radius = 6
		self.expression_input.clear_button_mode = 'always'
		self.expression_input.placeholder = '输入表达式'
		self.expression_input.delegate = ExpressionInputDelegate()
		
		self.match_button = ui.Button()
		self.match_button.image = ui.Image.named('iob:checkmark_circled_256')
		self.match_button.frame = (w-50,5,37,40)
		self.match_button.action = self.match_button_tapped
		self.match_button.tint_color = '#7cd359'
		
		self.origin_text = ui.TextView()
		self.origin_text.frame = (10,self.expression_input.y+self.expression_input.height+10,w-20,350)
		self.origin_text.bg_color = 'white'
		self.origin_text.border_width = 1
		self.origin_text.corner_radius = 6
		self.origin_text.number_of_lines = 0
		self.origin_text.font = ('<System>',16)
		
		
		self.match_text = ui.TextView()
		self.match_text.bg_color = 'white'
		self.match_text.border_width = 1
		self.match_text.corner_radius =  6
		self.match_text.font = ('<System>',16)
		self.match_text.editable = False
		self.add_subview(self.expression_input)
		self.add_subview(self.match_button)
		self.add_subview(self.origin_text)
		self.add_subview(self.match_text)
		
	def draw (self):
		self.match_text.frame = (10,self.origin_text.y+self.origin_text.height+10,w-20,h-self.origin_text.y-self.origin_text.height-85)
	
	def touch_begab (self,touch):
		pass
		
	def touch_moved (self,touch):
		y = touch.location[-1]
		if h-170 > y > 140:
			self.origin_text.height = y-self.origin_text.y
			self.set_needs_display()
	
	def match_button_tapped (self,sender):
		self.match_text.text = macth_text()
		
	def copy_button_tapped (self,sender):
		clipboard.set(self.expression_input.text)

w,h = ui.get_screen_size()
view = RootView()
view.present()
origin_text()
