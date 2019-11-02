import sys
import json
sys.path.append('../../3/3.1/src/')
from stone import StoneEnum

def format_score(score):
   return {"W":score[StoneEnum.WHITE], "B":score[StoneEnum.BLACK]}

def format_pretty_json(objects):
   joined = ',\n  '.join(json.JSONEncoder().encode(obj) for obj in objects)
   return "[\n  {}\n]".format(joined)