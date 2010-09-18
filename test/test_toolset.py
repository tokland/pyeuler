#!/usr/bin/python
import unittest

from toolset import *

class TestToolset(unittest.TestCase):
    def test_take(self):
        self.assertEqual(list(take(2, [1,2,3])), [1,2])
        self.assertEqual(list(take(100, [1,2,3])), [1,2,3])
        self.assertEqual(list(take(0, [])), [])
        self.assertEqual(list(take(0, [1,2,3])), [])
    
    def test_index(self):
        self.assertEqual(index(0, [1,2,3,4]), 1)
        self.assertEqual(index(3, [1,2,3,4]), 4)
        self.assertRaises(StopIteration, index, 0, [])
        self.assertRaises(StopIteration, index, 10, [1,2,3])
        

if __name__ == '__main__':
    unittest.main()
