import sys, unittest
sys.path.append('../src')
from stone import Stone, StoneEnum, get_other_type
from constants import EMPTY_STONE, BLACK_STONE, WHITE_STONE

class TestStone(unittest.TestCase):

	def test_stone_get_basics(self):
		self.assertEqual(StoneEnum(StoneEnum.WHITE), Stone(WHITE_STONE).get_type())
		self.assertEqual(StoneEnum(StoneEnum.BLACK), Stone(BLACK_STONE).get_type())
		self.assertEqual(None, Stone(EMPTY_STONE).get_type())

	def test_stone_set_basics(self):
		stone = Stone(EMPTY_STONE)
		stone.set_type(StoneEnum(StoneEnum.WHITE))
		self.assertEqual(StoneEnum(StoneEnum.WHITE), stone.get_type())
		stone.set_type(StoneEnum(StoneEnum.BLACK))
		self.assertEqual(StoneEnum(StoneEnum.BLACK), stone.get_type())
	
	def test_get_raw(self):
		stone = Stone(WHITE_STONE)
		self.assertEqual(WHITE_STONE, stone.get_raw())
	
	def test_stone_raises(self):
		with self.assertRaises(Exception):
			Stone("random_input")

	def test_get_other_type(self):
		self.assertEqual(StoneEnum.BLACK, get_other_type(StoneEnum.WHITE))
		self.assertEqual(StoneEnum.WHITE, get_other_type(StoneEnum.BLACK))

if __name__ == '__main__':
	unittest.main()