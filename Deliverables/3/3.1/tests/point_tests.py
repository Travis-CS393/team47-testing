import unittest
import sys
sys.path.append('../src/')
from point import Point, str_to_point, get_raw

class TestPoint(unittest.TestCase):

	def test_basic_point(self):
		point = str_to_point("2-3")
		self.assertEqual(point.x, 1)
		self.assertEqual(point.y, 2)
	
	def test_big_point(self):
		point = str_to_point("20444-3095682")
		self.assertEqual(point.x, 20443)
		self.assertEqual(point.y, 3095681)
	
	def test_get_raw(self):
		point = str_to_point("3-1")
		self.assertEqual("3-1", get_raw((point.x, point.y)))
	
	def test_errors(self):
		self.assertRaisesAny(str_to_point, "random input")
		self.assertRaisesAny(str_to_point, "0-num")
		self.assertRaisesAny(str_to_point, "num-0")
		self.assertRaisesAny(str_to_point, "0-")
		self.assertRaisesAny(str_to_point, "-0")
		self.assertRaisesAny(str_to_point, "-")

	def assertRaisesAny(self, func, arg):
		with self.assertRaises(Exception):
			func(arg)

if __name__ == '__main__':
	unittest.main()