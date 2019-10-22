import sys
from contextlib import contextmanager
import math
import unittest
from test_common import *
import task5

# Check whether exactly used_cells are occupied.
def check_layout(hash_table, used_cells):
  for (index, cell) in enumerate(hash_table.table):
    if (cell is not None) != (index in used_cells):
      return False
  return True

class TestTask5(TestCase):
  def test_layout(self):
    with self.vis():
      t = task5.HashTable(128, 1)
      for key in ['ad', 'da']:
        t[key] = 1
      self.assertTrue(check_layout(t, { 69 }),
        msg = "Incorrect chaining layout.")
      
    with self.vis():
      t = task5.HashTable(128, 1)
      for key in ['ad', 'ac' ]:
        t[key] = 1
      self.assertTrue(check_layout(t, { 68, 69 }),
        msg = "Incorrect chaining layout.")

    ### MY TESTING ###
    
    # Check three consecutive collisions of same hash
    with self.vis():
      t = task4.HashTable(128, 1)
      for key in ['ad', 'ac', 'da', 'ca']:
        t[key] = 1
      self.assertTrue(check_layout(t, { 68, 69 }),
        msg = "Incorrect probe sequence.")


    # Check collision with different hash value
    with self.vis():
      t = task4.HashTable(128, 1)
      for key in ['ad', 'ac', 'ca', 'ab', 'ba']:
        t[key] = 1
      self.assertTrue(check_layout(t, { 67, 68, 69 }),
        msg = "Incorrect probe sequence.")

      self.check_okay('layout')

  def test_statistics(self):
    with self.vis():
      t = task5.HashTable(128, 1) 
      for key in ['ad', 'ac', 'ca']:
          t[key] = 1
      self.assertEqual(t.statistics(),
        (1, 1, 1, 0),
        "Incorrect statistics count.")

    with self.vis():
      t = task5.HashTable(128, 1) 
      for key in ['ac', 'bb', 'ca']:
          t[key] = 1
      self.assertEqual(t.statistics(), (2, 3, 2, 0),
        "Incorrect collision count.")

    ### MY TESTING ###
    x = task5.HashTable(1024, 1)

    # Test collisiions, 3 colliding with original 1
    with self.vis("testing statistics"):
      for key in ["abcdef", "defabc", "fedbac", "defcab"]:
        x[key] = 1
      stats = x.statistics()
      self.assertEqual(stats, (3, 6, 3, 0), "incorrect statistics")

    # Setting first existing key should be a collision, in the BST
    # this is due to the BST invariants and string comparison used
    with self.vis("testing statistics"):
      x['abcdef'] = 1
      stats = x.statistics()
      self.assertEqual(stats, (4, 6, 3, 0), "incorrect statistics, setting existing value")
    assert self.check_okay("statistics")


   # Functionality tests are again the same as task 1.
  def test_contains(self):
    x = task5.HashTable(1024, 1)

    with self.vis():
      self.assertFalse("abcdef" in x, "False positive in __contains__ for empty table.")

    with self.vis("unexpected failure in setitem"):
      x["abcdef"] = 18
      x["definitely a string"] = None
      x["abdcef"] = "abcdef"
    
    for key in ["abcdef", "definitely a string", "abdcef"]:
      with self.vis():
        self.assertTrue(key in x, "False negative in __contains__ for key {}".format(key))

    ### MY TESTING ###
    x = task5.HashTable()

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
    x = task5.HashTable(1024, 1)

    with self.vis():
      with self.assertRaises(KeyError, msg="x[key] should raise KeyError for missing key."):
        elt = x["abcdef"]
      
    with self.vis("unexpected failure in setitem"):
      x["abcdef"] = 18
      x["definitely a string"] = None

    with self.vis():
      self.assertEqual(x["abcdef"], 18, msg = "Read after store failed.")

    ### MY TESTING ###
    x = task5.HashTable()

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

if __name__ == '__main__':
  unittest.main()
