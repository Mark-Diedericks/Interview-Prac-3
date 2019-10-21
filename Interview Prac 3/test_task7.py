import sys
from contextlib import contextmanager
import math
import unittest
from test_common import *
import task7

def as_int(values):
  return tuple(map(int, values))

class TestTask7(TestCase):
  def test_evaluate_frequency(self):
    with self.vis():
      freq = task7.Freq() 
      freq.add_file('words_simple.txt')
      comp = freq.evaluate_frequency('words_simple.txt')
      self.assertEqual(as_int(comp), (100, 0, 0, 0),
        msg = "Incorrect relative frequency (possibly rounding).")
      
    with self.vis():
      freq = task7.Freq()
      freq.add_file('words_simple.txt')
      # Words appearing multiple times in other_filename
      # should only be counted once.
      comp = freq.evaluate_frequency('words_dup.txt')
      self.assertEqual(as_int(comp), (40, 0, 0, 60),
        msg = "Incorrect handling of repeated words.")

    with self.vis():
      freq = task7.Freq()
      freq.add_file('words_simple.txt')
      with self.assertRaises(Exception, msg="Missing other_filename"):
        comp = freq.evaluate_frequency('some_missing_file.txt')

    self.assertTrue(self.check_okay("evaluate_frequency"))

if __name__ == '__main__':
  unittest.main()
