import sys
import os


def move_cursor(x, y):
	"""커서를 (y, x) 위치로 즉시 이동하는 함수."""
	sys.stdout.write(f"\033[{y};{x}H")  # 커서 이동
	sys.stdout.flush()  # 즉시 반영

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

# 환경 차이 있는 함수들
if os.name == 'nt':
	import msvcrt

	def getch():
		return	msvcrt.getch().decode('utf-8')

else: # Unix
	import tty
	import termios

	def getch():
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

