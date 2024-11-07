import console_iotools as io
import text_styles as style

class ConsoleUi:
	def __init__(self):
		pass

	def update(self):
		pass
		# select된곳 확인 (input 진행중이였다면, InputObj가 상세한 커서 추척)
		# 오브젝트들 업데이트 진행
		# 모든 업데이트 종료후 select복원

class UiObject:
	def __init__(self, loc=(0, 0), size=None, selectable=False, need_update=True):
		self.x, self.y = loc
		self.size = size
		self.selectable = selectable
		self.selected = False
		self.need_update = need_update
		self.updated = not need_update
		self.parent = None
		self.childes = []

	def draw(self, parent_loc=(0, 0)):
		pass

	def hadle_input(self, key):
		pass

	def select_toggle(self): # self.selectable == True 인 경우만 작성
		self.selected = not self.selected

class StrObj(UiObject):
	def __init__(self, text, loc=(0, 0), size=None, selectable=False, need_update=True):
		super().__init__(loc, size, selectable, need_update)
		self.text = text

	def draw(self, parent_loc=(0, 0), draw_size=None):
		x, y = parent_loc
		x += self.x
		y += self.y
		if self.size:
			end = (x + self.size[0], y + self.size[1])
		else:
			if draw_size:
				end = (x + draw_size[0], y + draw_size[1])
			else:
				end = (x + len(self.text), y + 1)
		end[0] = min(self.parent.draw_area['end'][0], end[0])
		end[1] = min(self.parent.draw_area['end'][1], end[1])
		io.area_clear((x, y), end)
		io.area_print(self.text, (x, y), end)
		self.updated = True

class TextObj(StrObj):
	def __init__(self, text, loc=(0, 0), size=None, need_update=True):
		super().__init__(text, loc, size, False, need_update)
		
class LinkObj(StrObj):
	def __init__(self, text, link, loc=(0, 0), size=None, need_update=True, target=None):
		super().__init__(text, loc, size, True, need_update)
		self.link = link
		self.target = target

	def select_toggle(self):
		if self.selected:
			self.text = style.remove_invert_background(self.text)
		else:
			self.text = style.invert_background(self.text)
		self.updated = False
		super().select_toggle()
		
	def hadle_input(self, key):
		if key == 'ENTER':
			pass
			# ContainerObj 작성후 작성

class ContainerObj(UiObject):
	def __init__(self, loc=(0, 0), size=None, selectable=False, need_update=True, border=[1, 1, 1, 1]):
		"""
		Args:
			size: (width, height)
			border: [1, 1, 1, 1], 1 or 0의 list 각각 top right bottom left
		"""
		if size is None:
			ValueError('ContainerObj는 size가 정의되어야 합니다.')
		super().__init__(loc, size, selectable, need_update)
		self.size = size
		self.border = border
		self.draw_area = {'start':None, 'end':None}

	def draw(self, parent_loc=(0, 0), draw_size=None, draw_border=False):
		start = (parent_loc[0] + self.x, parent_loc[1] + self.y)
		if self.size:
			draw_size = self.size
		end = (start[0] + draw_size[0], start[1] + draw_size[1])
		self.draw_area['start'] = (start[0]+self.border[3], start[1]+self.border[0])
		self.draw_area['end'] = (end[0]-self.border[2], end-self.border[1])
		if draw_border:
			if self.border[0]: # top
				tmp = f'┌{"─" * (draw_size[0]-2)}┐'
				io.area_print(tmp, start, (start[0]+draw_size[0], start[1]+1))
			if self.border[1]: # right
				tmp = '┐\n'
				for _ in range(draw_size[1]-2):
					tmp += '│\n'
				tmp += '┘'
				io.area_print(tmp, (end[0]-1, start[1]), end)
			if self.border[2]: # bottom
				tmp = f'└{"─" * (draw_size[0]-2)}┘'
				io.area_print(tmp, (start[0], end[1]-1), end)
			if self.border[3]: # left
				tmp = '┌\n'
				for _ in range(draw_size[1]-2):
					tmp += '│\n'
				tmp += '└'
				io.area_print(tmp, start, (start[0]+1, end[1]))
		for child in self.childes:
			if not child.updated:
				child.draw(parent_loc=start, draw_size=None)


