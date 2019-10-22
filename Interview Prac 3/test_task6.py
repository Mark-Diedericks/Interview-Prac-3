import sys
from contextlib import contextmanager
import math
import unittest
from test_common import *
import task6

class TestTask6(TestCase):
  def test_addfile(self):
    with self.vis():
      freq = task6.Freq()
      freq.add_file('words_simple.txt')
      for word in ['this', 'dictionary', 'words']:
        self.assertEqual(freq.word_frequency[word], 1,
          "Incorrect frequency.")

    with self.vis():
      freq = task6.Freq()
      freq.add_file('words_dup.txt')
      for (word, count) in [('words', 3), ('and', 2)]:
        self.assertEqual(freq.word_frequency[word], count,
          "Incorrect frequency.")

    ### MY TESTING ###

    # Capitalization should not be considered??? Thus WORD = word???
    with self.vis():
      freq = task6.Freq()
      freq.add_file('repeated.txt')
      for (word, count) in [('word', 8)]:
        self.assertEqual(freq.word_frequency[word], count,
          "Incorrect frequency.")
    
    # Empty lines should not be considered
    with self.vis():
      freq = task6.Freq()
      freq.add_file('words_empty.txt')
      self.assertFalse('' in freq.word_frequency, "Frequency for empty words.")
    
     
    self.assertTrue(self.check_okay("addfile"))

  def test_rarity(self):
    with self.vis():
      freq = task6.Freq()
      freq.add_file('words_freq.txt')

      self.assertEqual(freq.rarity('a'), 0,
        "Incorrect rarity.")

    with self.vis():
      self.assertEqual(freq.rarity('fish'), 2,
        "Incorrect rarity.")

    ### MY TESTING ###

    # Ensure errors return 3 and commons return 0
    with self.vis():
      freq = task6.Freq()
      freq.add_file('repeated.txt')

      self.assertEqual(freq.rarity('a'), 3,
        "Incorrect rarity (Error).")
      self.assertEqual(freq.rarity('word'), 0,
        "Incorrect rarity (Common).")

    self.assertTrue(self.check_okay("rarity"))

if __name__ == '__main__':
  unittest.main()
