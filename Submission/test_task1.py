import sys
from contextlib import contextmanager
import math
import unittest
from test_common import *
import task1

class TestTask1(TestCase):
  def test_init(self):
    with self.vis("empty init"):
      x = task1.HashTable()
    with self.vis("init with size and base"):
      z = task1.HashTable(800, 2398)

    ### MY TESTING ###
    with self.vis("init with size and no base"):
      z = task1.HashTable(table_capacity = 800)
    with self.vis("init with no size and base"):
      z = task1.HashTable(hash_base = 2398)
      
    assert self.check_okay("init")
    
  def test_hash(self):

    x = task1.HashTable(1024, 17)
    for (key, expect) in [("", 0),
                          ("abcdef", 389),
                          ("defabc", 309)]:
        with self.vis():
          self.assertEqual(x.hash(key), expect, msg=f"Unexpected hash with base 17 and key {key}.")

    ### MY TESTING ###

    # Check different variables for hash function
    x = task1.HashTable(64, 7)
    for (key, expect) in [("", 0), ("word", 50), ("test", 26)]:
        with self.vis():
          self.assertEqual(x.hash(key), expect, msg=f"Unexpected hash with base 17 and key {key}.")

    assert self.check_okay("hash")

  # The tests for __contains__ and __getitem__ use __setitem__, so we don't make any assumptions
  # about the underlying array representation. Remember to define your own tests for __setitem__
  # (and rehash)
  def test_contains(self):
    x = task1.HashTable(1024, 1)

    with self.vis():
      self.assertFalse("abcdef" in x, "False positive in __contains__ for empty table.")

    with self.vis("unexpected failure in setitem (1)"):
      x["abcdef"] = 18
      x["definitely a string"] = None
      x["abdcef"] = "abcdef"
    
    for key in ["abcdef", "definitely a string", "abdcef"]:
      with self.vis():
        self.assertTrue(key in x, "False negative in __contains__ for key {}".format(key))

    ### MY TESTING ###
    x = task1.HashTable()

    # Ensure keys aren't found in empty hash table
    for key in ["AB", "CD", "EF"]:
      with self.vis():
        self.assertFalse(key in x, "False positive in __contains__ for key {}".format(key))

    with self.vis("unexpected failure in setitem (2)"):
      x["three"] = 3
      x["five"] = 5
      x["seven"] = 7

    # Ensure correct keys are found
    for key in ["three", "five", "seven"]:
      with self.vis():
        self.assertTrue(key in x, "False negative in __contains__ for key {}".format(key))

    # Ensure capatilized keys are not found
    for key in ["Three", "Five", "Seven"]:
      with self.vis():
        self.assertFalse(key in x, "False positive in __contains__ for key {}".format(key))

    assert self.check_okay("contains")



  def test_getitem(self):
    x = task1.HashTable(1024, 1)

    with self.vis():
      with self.assertRaises(KeyError, msg="x[key] should raise KeyError for missing key."):
        elt = x["abcdef"]
      
    with self.vis("unexpected failure in setitem"):
      x["abcdef"] = 18
      x["definitely a string"] = None

    with self.vis():
      self.assertEqual(x["abcdef"], 18, msg = "Read after store failed.")

    x["abdcef"] = 22

    ### MY TESTING ###
    x = task1.HashTable()

    with self.vis("unexpected failure in setitem (2)"):
      x["three"] = 3
      x["five"] = 5
      x["seven"] = 7

    # Check values for each key are correct
    with self.vis():
      self.assertEqual(x["three"], 3, msg = "Read after store failed.")
      self.assertEqual(x["five"], 5, msg = "Read after store failed.")
      self.assertEqual(x["seven"], 7, msg = "Read after store failed.")


    assert self.check_okay("getitem")



  def test_rehash(self):

    ### MY TESTING ###
    x = task1.HashTable(4, 5)
    
    with self.vis("unexpected failure in setitem"):
      x["one"] = 1
      x["three"] = 3
      x["five"] = 5
      x["seven"] = 7

    with self.vis():
      self.assertTrue(len(x.table) == 4, msg = "Premature rehash")

    with self.vis("unexpected failure in setitem"):
      x["nine"] = 9

    with self.vis():
      # 4 * 2 = 8, next prime is 11
      self.assertTrue(len(x.table) == 11, msg = "Premature rehash")

    # Ensure values are correct after rehash
    with self.vis():
      self.assertEqual(x["one"], 1, msg = "Read after store failed.")
      self.assertEqual(x["three"], 3, msg = "Read after store failed.")
      self.assertEqual(x["five"], 5, msg = "Read after store failed.")
      self.assertEqual(x["seven"], 7, msg = "Read after store failed.")
      self.assertEqual(x["nine"], 9, msg = "Read after store failed.")

    assert self.check_okay("rehash")


if __name__ == '__main__':
  unittest.main()
