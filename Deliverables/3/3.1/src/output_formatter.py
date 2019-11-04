import json
#from point import get_raw
from stone import Stone

def format_board(matr):
	"""
	print(matr)
	print(matr[0])
	return [[matr[i][j].get_raw() for i in range(len(matr))] for j in range(len(matr))]
	"""
	if (len(matr) == 1):
		return [[[matr[0][i][j].get_raw() for i in range(len(matr[0]))] for j in range(len(matr[0]))]]

	if (len(matr) == 2):
		return [[[matr[0][i][j].get_raw() for i in range(len(matr[0]))] for j in range(len(matr[0]))], [[matr[1][i][j].get_raw() for i in range(len(matr[1]))] for j in range(len(matr[1]))]]




def format_board_if_valid(inpt):
   if isinstance(inpt, str):
      return inpt
   return format_board(inpt)

def format_points(pts_set):
   return sorted([get_raw(tupl) for tupl in list(pts_set)])

def format_pretty_json(objects):
   joined = ',\n  '.join(json.JSONEncoder().encode(obj) for obj in objects)
   return "[\n  {}\n]".format(joined).replace('"],', '"],\n  ').replace("  \n", "")