import json
from point import get_raw
from stone import Stone

# Formats from game object representation to raw python representation

# Fix naming since format board takes in a matr of len 3 for board history
def format_one_board(matr):
	return [[matr[i][j].get_raw() for i in range(len(matr))] for j in range(len(matr))]

def format_board(matr):
	if (len(matr) == 1):
		try:
			return [[[matr[0][i][j].get_raw() for i in range(len(matr[0]))] for j in range(len(matr[0]))]]
		except (IndexError, AttributeError) as e:
			return matr

	elif (len(matr) == 2):
		try:
			return [[[matr[0][i][j].get_raw() for i in range(len(matr[0]))] for j in range(len(matr[0]))], [[matr[1][i][j].get_raw() for i in range(len(matr[1]))] for j in range(len(matr[1]))]]
		except (IndexError, AttributeError) as e:
			return matr

	elif (len(matr) == 3):
		try:
			return [[[matr[0][i][j].get_raw() for i in range(len(matr[0]))] for j in range(len(matr[0]))], [[matr[1][i][j].get_raw() for i in range(len(matr[1]))] for j in range(len(matr[1]))], [[matr[2][i][j].get_raw() for i in range(len(matr[2]))] for j in range(len(matr[2]))]]
		except (IndexError, AttributeError) as e:
			return matr

	else:
		raise Exception("Board history can have length from 1 to 3.")

def format_board_if_valid(inpt):
	if isinstance(inpt, str):
		return inpt
	return format_board(inpt)

def format_points(pts_set):
	return sorted([get_raw(tupl) for tupl in list(pts_set)])

def format_pretty_json(objects):
	joined = ',\n  '.join(json.JSONEncoder().encode(obj) for obj in objects)
	return "[\n  {}\n]".format(joined).replace('"],', '"],\n  ').replace("  \n", "")

	