import sys
sys.path.append('../../3/3.1/src/')
from point import Point, str_to_point
from constants import PASS

def format_input(string):
	if string == PASS:
		return "pass"
	else:
		return str_to_point(string)