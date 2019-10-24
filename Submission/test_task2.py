import sys
from contextlib import contextmanager
import math
import unittest
from test_common import *
import task1
import task2

class TimedOutExn_(Exception):
  pass

class TestTask2(TestCase):
  def test_load(self):
    with self.vis():
      table = task1.HashTable()
      task2.load_dictionary(table, "words_simple.txt", 10)
      self.assertEqual(count_nonempty_buckets(table), 6)

    with self.vis():
      table = task1.HashTable()
      task2.load_dictionary(table, "words_empty.txt", 10)
      self.assertEqual(count_nonempty_buckets(table), 11, "Failed to handle empty line or whitespace.")

    ### MY TESTING ###
    
    # Test words of large file
    with self.vis():
      table = task1.HashTable(402221, 27183)
      task2.load_dictionary(table, "english_small.txt", 15)
      self.assertEqual(count_nonempty_buckets(table), 84097, "Failed to handle large file.")

    # Test words of larger file
    with self.vis():
      table = task1.HashTable(402221, 27183)
      task2.load_dictionary(table, "english_large.txt", 15)
      self.assertEqual(count_nonempty_buckets(table), 194433, "Failed to handle largest file.")

    # Test repeated words
    with self.vis():
      table = task1.HashTable(17, 3)
      task2.load_dictionary(table, "repeated.txt", 15)
      self.assertEqual(count_nonempty_buckets(table), 2, "Failed to handle repeated word(s).")


    self.assertTrue(self.check_okay("load_dictionary"))

  def test_load_timeout(self):
    with self.vis("load without max_time"):
      table = task1.HashTable()
      task2.load_dictionary(table, "words_simple.txt")

    with self.vis("failed to apply timeout"):
      table = task1.HashTable(100000, 1)
      with self.assertRaises(Exception, msg = "reading too many words should time out."):
        try:
          self.with_deadline(3, task2.load_dictionary, (table, "english_small.txt", 1))
        except TimedOutExn_:
          pass

    ### MY TESTING ###
    # Timeout on very large file with subpar table size and base
    with self.vis("failed to apply timeout (2)"):
      table = task1.HashTable(250727, 1)
      with self.assertRaises(Exception, msg = "reading too many words should time out."):
        try:
          self.with_deadline(11, task2.load_dictionary, (table, "english_large.txt", 10))
        except TimedOutExn_:
          pass

    self.assertTrue(self.check_okay("load_dictionary timeout"))

  def test_load_time(self):
    with self.vis("reporting words"):
      (words, time) = self.with_deadline(3, task2.load_dictionary_time, (31, 100, "words_simple.txt", 1))
      self.assertEqual(words, 6)

    ### MY TESTING ###
    # Large file
    with self.vis("reporting words"):
      (words, time) = self.with_deadline(1, task2.load_dictionary_time, (27183, 402221, "english_small.txt", 10))
      self.assertEqual(words, 84097)

    # Largest file
    with self.vis("reporting words"):
      (words, time) = self.with_deadline(1, task2.load_dictionary_time, (27183, 402221, "english_large.txt", 10))
      self.assertEqual(words, 194433)



    self.assertTrue(self.check_okay("load_dictionary time"))

if __name__ == '__main__':
  unittest.main()
