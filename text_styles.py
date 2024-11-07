import sys
import os
import re


def colored_text(text, color):
	"""
	Args:
		test: <str>
		color: (r, g, b) | hex | ansi color
	"""
	# ANSI 색상 코드 정규 표현식 (RGB 또는 기본 ANSI 색상 코드)
	ansi_color_escape = re.compile(r'(\x1B\[38;2;\d+;\d+;\d+m|\x1B\[3\d+m)')

	# 기존 색상 코드 제거
	text = ansi_color_escape.sub('', text)
	
	ansi_colors = {
		"red": "255;0;0",
		"green": "0;255;0",
		"blue": "0;0;255",
		"yellow": "255;255;0",
		"cyan": "0;255;255",
		"magenta": "255;0;255",
		"white": "255;255;255",
		"black": "0;0;0"
	}
	if isinstance(color, tuple):  # RGB 튜플 경우
		r, g, b = color
		rgb_color_code = f"38;2;{r};{g};{b}"
	elif isinstance(color, str):  # 문자열 경우
		if color.startswith('#'):  # 헥스 색상 코드
			hex_color = color.lstrip('#')
			r = int(hex_color[0:2], 16)
			g = int(hex_color[2:4], 16)
			b = int(hex_color[4:6], 16)
			rgb_color_code = f"38;2;{r};{g};{b}"
		elif color in ansi_colors:  # ANSI 색상 이름
			rgb_color_code = f"38;2;{ansi_colors[color]}"
		else:
			raise ValueError("지원하지 않는 색상입니다.")
	else:
		raise TypeError("색상은 튜플 또는 문자열이어야 합니다.")

	# 색칠된 텍스트를 ANSI 이스케이프 코드와 함께 반환
	return f"\033[{rgb_color_code}m{text}\033[0m"

def bold_text(text):
	"""굵은 글씨로 변환"""
	return f"\033[1m{text}\033[0m"

def faint_text(text):
	"""흐릿한 글씨로 변환"""
	return f"\033[2m{text}\033[0m"

def underline_text(text):
	"""밑줄 있는 텍스트로 변환"""
	return f"\033[4m{text}\033[0m"

def invert_background(text, color=None):
	"""
	Args:
		text (str): 텍스트
		color (str | tuple, optional): 텍스트 색상 (기본값: None)
	Returns:
		str: 배경이 반전된 텍스트
	"""
	# 텍스트 색상이 주어지면 색상 변경
	if color:
		text = colored_text(text, color)

	# 배경 반전 (색상 반전)
	return f"\033[7m{text}\033[0m"

def remove_invert_background(text):
	"""
	Args:
		text (str): 텍스트

	Returns:
		str: 색상 반전이 해제된 텍스트
	"""
	# 색상 반전 ANSI 코드가 포함되어 있는지 확인
	if "\033[7m" in text:
		# 색상 반전 ANSI 코드 제거
		# 색상 반전 시작 코드와 종료 코드 제거
		text = re.sub(r'\033\[7m', '', text)  # 색상 반전 시작 코드 제거
		text = re.sub(r'\033\[0m', '', text)  # 기본 ANSI 종료 코드 제거
		
		return text
	else:
		# 색상 반전 ANSI 코드가 사용되지 않았다면 입력 텍스트 그대로 반환
		return text

def is_ansi_codes(text):
	"""
	Args:
		text (str): 검사할 텍스트
	Returns:
		bool: ANSI 코드가 포함되어 있으면 True, 아니면 False
	"""
	ansi_escape = re.compile(r'\x1B\[[0-?9;]*[mK]')
	return bool(ansi_escape.search(text))

def remove_ansi_codes(text):
	"""
	Args:
		text (str): ANSI 코드를 제거할 텍스트
	Returns:
		str: ANSI 코드가 제거된 텍스트
	"""
	ansi_escape = re.compile(r'\x1B\[[0-?9;]*[mK]')
	return ansi_escape.sub('', text)

# print("*")
# print("**")
# print("***")
# print("****")
# print("*****")
# print("				 |", end="\r")
# b = input("> ")
# a = 'apple'
# a = colored_text(a, "red")
# print(a)
# a = bold_text(a)
# print(a)
# a = colored_text(a, 'green')
# print(a)
# a = underline_text(a)
# print(a)
# s = invert_background(a)
# print(s)
# a = invert_background(a, 'blue')
# print(a)
# print(is_ansi_codes(a))
# a = remove_ansi_codes(a)
# print(a)


