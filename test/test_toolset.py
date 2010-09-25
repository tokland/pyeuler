#!/usr/bin/python
import unittest

from pyeuler.toolset import *

class TestToolset(unittest.TestCase):
    def test_take(self):
        self.assertEqual(list(take(2, [1,2,3])), [1,2])
        self.assertEqual(list(take(0, [])), [])
        self.assertEqual(list(take(0, [1,2,3])), [])
        self.assertEqual(list(take(100, [1,2,3])), [1,2,3])
    
    def test_index(self):
        self.assertEqual(index(0, [1,2,3,4]), 1)
        self.assertEqual(index(3, [1,2,3,4]), 4)
        self.assertRaises(StopIteration, index, 0, [])
        self.assertRaises(StopIteration, index, 10, [1,2,3])

    def test_first(self):
        self.assertEqual(first(iter([1,2,3,4])), 1)
        self.assertRaises(StopIteration, first, iter([]))    

    def test_last(self):
        self.assertEqual(last(iter([1,2,3,4])), 4)
        self.assertRaises(TypeError, last, iter([]))    

    def test_take_every(self):
        self.assertEqual(list(take_every(1, [1,2,3,4])), [1,2,3,4])
        self.assertEqual(list(take_every(2, [1,2,3,4])), [1,3])
        self.assertEqual(list(take_every(10, [1,2,3,4])), [1])
        self.assertEqual(list(take_every(1, [])), [])

    def test_drop(self):
        self.assertEqual(list(drop(0, [1,2,3,4])), [1,2,3,4])
        self.assertEqual(list(drop(1, [1,2,3,4])), [2,3,4])
        self.assertEqual(list(drop(10, [1,2,3,4])), [])

    def test_ilen(self):
        self.assertEqual(ilen([]), 0)
        self.assertEqual(ilen([1, 2, 3]), 3)
        self.assertEqual(ilen(iter([1, 2, 3])), 3)
        
    def test_product(self):
        self.assertEqual(product([]), 1)
        self.assertEqual(product([2, 3]), 6)

    def test_flatten(self):
        self.assertEqual(flatten([]), [])
        self.assertEqual(flatten([[1,2,3], [4,5,6]]), [1,2,3,4,5,6])
        self.assertEqual(flatten([[1,2,3], [4,[5,6]]]), [1,2,3,4,[5,6]])

    def test_compact(self):
        self.assertEqual(list(compact([0, 1, "", None, [], (), "hello"])), [1, "hello"])
                
        
if __name__ == '__main__':
    unittest.main()
