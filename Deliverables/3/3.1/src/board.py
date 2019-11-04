from stone import StoneEnum, Stone, get_other_type
from point import Point
from constants import BOARD_DIM

class Board():

   ## Validators
   def valid_point(func):
      def wrapper(*args, **kwargs):
         for arg in args:
            if isinstance(arg, Point) and not args[0].point_valid(arg):
               raise Exception("Invalid point passed")
         return func(*args, **kwargs)
      return wrapper
   
   def valid_stone(func):
      def wrapper(*args, **kwargs):
         for arg in args:
            if not arg:
               raise Exception("Cannot call this funciton with the empty stone")
         return func(*args, **kwargs)
      return wrapper

   ## Constructor
   def __init__(self, board_matr, dim = BOARD_DIM):
      self.board_dim = dim
      self.board = board_matr
      self.points = {StoneEnum.WHITE: set(), StoneEnum.BLACK: set(), None: set()}
      for i in range(self.board_dim):
         for j in range(self.board_dim):
            self.points[self.get_type(Point(i, j))].add((i,j))

   def __setitem__(self, index, value):
      self.board[index] = value

   def __getitem__(self, index):
      return self.board[index]

   def __iter__(self):
      return iter(self.board)

   def __len__(self):
      return self.board_dim

   ## Public Methods
   @valid_point
   def occupied(self, point):
      return self.get_type(point) is not None

   @valid_point 
   @valid_stone
   def occupies(self, test_type, point):
      actual_type = self.get_type(point)
      return actual_type is test_type

   @valid_point
   @valid_stone
   def place_stone(self, stone_type, point):
      if self.occupied(point):
         return "This seat is taken!"
      else:
         self._update_stone(point, self.get_type(point), stone_type)
         return self.board

   @valid_point
   @valid_stone
   def place_and_update(self, stone_type, point):
      self.place_stone(stone_type, point)
      neighbors = self.get_neighbors(point)
      other_type = get_other_type(stone_type)
      for other_point in self._filter_neighbors_by_type(neighbors, other_type):
         if not self.reachable(other_point, None):
            self._remove_component(other_type, other_point)
      if not self.reachable(point, None):
         self._remove_component(stone_type, point)
         
      return self.board

   @valid_point
   @valid_stone
   def remove_stone(self, stone_type, point):
      if self.get_type(point) is not stone_type:
         return "I am just a board! I cannot remove what is not there!"
      else:
         self._update_stone(point, self.get_type(point), None)
         return self.board

   @valid_point
   def reachable(self, point, target_type):
      if self.get_type(point) == target_type:
         return True
      visited = [[False for i in range(self.board_dim)] for j in range(self.board_dim)]
      return self._reachable(point, target_type, visited)

   def get_points(self, stone_type):
      return self.points[stone_type]

   @valid_point
   def get_type(self, point):
      return self._get_stone(point).get_type()

   @valid_point
   def get_neighbors(self, point):
      x, y = point.x, point.y
      neighbors = [Point(x-1, y), Point(x+1,y), Point(x, y+1), Point(x, y-1)]
      return list(filter(self.point_valid, neighbors))
   
   @valid_point
   def get_liberties(self, point):
      component = set()
      liberties = set()
      self._get_liberties(point, component, liberties)
      return component, liberties

   def equal(self, board):
      for key in self.points:
         if self.points[key] != board.points[key]:
            return False
      return True
   
   def empty(self):
      return len(self.get_points(None)) == self.board_dim ** 2

   ## Private Methods
   def _get_stone(self, point):
      return self.board[point.x][point.y]

   def _filter_neighbors_by_visited(self, neighbors, visited):
      return list(filter(lambda point: not visited[point.x][point.y], neighbors))

   def _filter_neighbors_by_type(self, neighbors, stone_type):
      return list(filter(lambda point: self.get_type(point) == stone_type, neighbors))

   def _update_stone(self, point, old_type, new_type):
      self.points[old_type].remove((point.x, point.y))
      self.points[new_type].add((point.x, point.y))
      self._get_stone(point).set_type(new_type)

   def _reachable(self, point, target_type, visited):
      visited[point.x][point.y] = True
      neighbors = self.get_neighbors(point)
      valid_neighbors = self._filter_neighbors_by_visited(neighbors, visited)
      for adj_point in valid_neighbors:
         if self.get_type(adj_point) == target_type:
            return True
         if self.get_type(adj_point) == self.get_type(point) and \
            self._reachable(adj_point, target_type, visited):
            return True
      return False

   def _remove_component(self, stone_type, point):
      if self.get_type(point) == stone_type:
         self.remove_stone(stone_type, point)
         friends = self._filter_neighbors_by_type(self.get_neighbors(point), stone_type)
         for adj_point in friends:
            self._remove_component(stone_type, adj_point)

   def _get_liberties(self, point, component, liberties):
      component.add((point.x, point.y))
      neighbors = self.get_neighbors(point)
      empty_stones = self._filter_neighbors_by_type(neighbors, None)
      for empty_point in empty_stones:
         liberties.add((empty_point.x, empty_point.y))
      same_stones = self._filter_neighbors_by_type(neighbors, self.get_type(point))
      for same_point in same_stones:
         if (same_point.x, same_point.y) not in component:
            self._get_liberties(same_point, component, liberties)

   ## Board Related Point Functions
   def point_valid(self, point):
      return self.coord_valid(point.x) and self.coord_valid(point.y)

   def coord_valid(self, coord):
      return 0 <= coord and coord < self.board_dim