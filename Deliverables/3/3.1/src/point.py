class Point:
   def __init__(self, x, y):
      self.x, self.y = x, y

def str_to_point(s):
   try:
      x_str, y_str = s.split("-")
      x, y = int(x_str) - 1, int(y_str) - 1
      return Point(x, y)
   except:
      raise Exception("invalid string input for point")

def get_raw(tupl):
   x, y = tupl
   return "{}-{}".format(x + 1, y + 1)