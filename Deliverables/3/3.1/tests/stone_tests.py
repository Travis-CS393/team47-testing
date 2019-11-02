import unittest
import sys
sys.path.append('../src')
from stone import Stone, StoneEnum

class TestStone(unittest.TestCase):

	def test_stone_basics(self):
		self.assertEqual(StoneEnum(StoneEnum.WHITE), Stone("W").get_type())
		self.assertEqual(StoneEnum(StoneEnum.BLACK), Stone("B").get_type())
		self.assertEqual(None, Stone(" ").get_type())
	
	def test_get_raw(self):
		stone = Stone("W")
		self.assertEqual("W", stone.get_raw())
	
	def test_stone_raises(self):
		with self.assertRaises(Exception):
			Stone("random_input")

if __name__ == '__main__':
	unittest.main()