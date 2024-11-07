import sys
import os


def console_size():
	"""현재 콘솔 화면의 크기를 가져오는 함수."""
	try:
		size = os.get_terminal_size()
		return size.lines, size.columns  # (행, 열) 형식으로 반환
	except OSError:
		# 터미널 크기를 가져올 수 없는 경우 기본값 반환
		return 24, 80  # 기본적으로 24행, 80열 반환
	
def clear_console(start=(0, 0), end=None):
	"""콘솔 화면의 특정 영역을 지우는 함수.
	Args:
		start: 지우기 시작할 (행, 열) 튜플 (기본값: (0, 0))
		end: 지우기 끝낼 (행, 열) 튜플 (기본값: None, 콘솔 화면의 끝으로 설정)
	"""
	# 전체 화면 지우기
	if (end is None) and (start == (0, 0)):
		os.system('cls' if os.name == 'nt' else 'clear')
	else:
		# end가 None이면 콘솔 화면의 끝으로 설정
		if end is None:
			end_row, end_col = console_size()
		else:
			end_row, end_col = end

		# 특정 영역만 지우기
		for row in range(start[0], end_row):
			if start[1] < end_col:
				print(f"\033[{row};{start[1]}H\033[{end_col - start[1]}X")  # 해당 행의 특정 열 

def area_print(text, start, end, line_strip=True):
	"""
	Args:
		text: <str>
		start: (x, y)
		end: (x, y)
	"""
	width = end[0] - start[0]
	height = end[1] - start[1]
	lines = []
	line = ''
	for c in text:
		if c == '\n':
			lines.append(line)
			line = ''
		elif len(line) >= width:
			lines.append(line)
			line = c
		else:
			line += c
	lines.append(line)
	line_numse = min(height, len(lines))
	for i in range(line_numse):
		move_cursor(start[0], start[1]+i)
		if line_strip:
			print(lines[i].strip(), end='')
		else:
			print(lines[i], end='')

def area_clear(start, end):
	width = end[0] - start[0]
	height = end[1] - start[1]
	for i in range(height):
		move_cursor(start[0], start[1]+i)
		print(' ' * width, end='')

# 환경 차이 있는 함수들
if os.name == 'nt':
	import msvcrt
	# from ctypes import windll, c_int, c_short, Structure, byref
	import colorama

	colorama.init()

	def getch():
		ch = msvcrt.getch()
		if ch == b'\xe0':  # 화살표 키 입력의 시작 바이트
			ch = msvcrt.getch()  # 다음 바이트를 읽어 화살표 키를 결정
			if ch == b'H':
				return 'UP'  # 위쪽 화살표
			elif ch == b'P':
				return 'DOWN'  # 아래쪽 화살표
			elif ch == b'K':
				return 'LEFT'  # 왼쪽 화살표
			elif ch == b'M':
				return 'RIGHT'  # 오른쪽 화살표
			elif ch == b'7':
				return 'HOME'  # 홈 키
			elif ch == b'8':
				return 'PAGE_UP'  # 페이지 업
			elif ch == b'9':
				return 'PAGE_DOWN'  # 페이지 다운
			elif ch == b'0':
				return 'END'  # 끝 키
		elif ch == b'\r':  # 엔터 키
			return 'ENTER'
		elif ch == b'\x08':  # 백스페이스
			return 'BACKSPACE'
		elif ch == b'\t':  # 탭
			return 'TAB'
		elif ch == b'\x1b':  # ESC 키
			return 'ESC'
		else:
			return ch.decode('utf-8')

	def move_cursor(x, y):
		# colorama.init()
		print(f"\033[{y+1};{x+1}H", end="")
		# colorama.deinit()


else:  # Unix
	import tty
	import termios

	def getch():
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)

			if ch == '\x1b':  # ANSI escape sequence의 시작
				next_char = sys.stdin.read(2)  # 다음 두 문자 읽기
				if next_char == '[A':
					return 'UP'  # 위쪽 화살표
				elif next_char == '[B':
					return 'DOWN'  # 아래쪽 화살표
				elif next_char == '[D':
					return 'LEFT'  # 왼쪽 화살표
				elif next_char == '[C':
					return 'RIGHT'  # 오른쪽 화살표
				elif next_char == '[H':
					return 'HOME'  # 홈 키
				elif next_char == '[5~':
					return 'PAGE_UP'  # 페이지 업
				elif next_char == '[6~':
					return 'PAGE_DOWN'  # 페이지 다운
				elif next_char == '[F':
					return 'END'  # 끝 키
				else:
					return ch  # 다른 ANSI 시퀀스
			elif ch == '\n':  # 엔터 키
				return 'ENTER'
			elif ch == '\x7f':  # 백스페이스
				return 'BACKSPACE'
			elif ch == '\t':  # 탭
				return 'TAB'
			elif ch == '\x1b':  # ESC 키
				return 'ESC'
			else:
				return ch
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

	def move_cursor(x, y):
		"""커서를 (y, x) 위치로 즉시 이동하는 함수."""
		sys.stdout.write(f"\033[{y+1};{x+1}H")  # 커서 이동
		sys.stdout.flush()  # 즉시 반영

