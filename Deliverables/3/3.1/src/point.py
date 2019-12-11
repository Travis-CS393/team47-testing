class Point:
   def __init__(self, x, y):
      """
      This class implements the Point class which describes 
      the coordinate position of a place on the Go Board
      """
      self.x, self.y = x, y

def str_to_point(s):
   try:
      x_str, y_str = s.split("-")
      x, y = int(x_str) - 1, int(y_str) - 1
      return Point(x, y)
   except:
      raise PointException("POINT: Invalid string input for point.")

def get_raw(tupl):
   x, y = tupl
   return "{}-{}".format(x + 1, y + 1)


class PointException(Exception):
   pass