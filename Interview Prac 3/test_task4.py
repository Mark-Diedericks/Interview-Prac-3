import sys
from contextlib import contextmanager
import math
import unittest
from test_common import *
import task4

# Check whether exactly used_cells are occupied.
def check_layout(hash_table, used_cells):
  for (index, cell) in enumerate(hash_table.table):
    if (cell is not None) != (index in used_cells):
      return False
  return True

class TestTask4(TestCase):
  def test_layout(self):
    with self.vis():
      t = task4.HashTable(128, 1)
      for key in ['ad', 'ac', 'bc']:
        t[key] = 1
      self.assertTrue(check_layout(t, { 68, 69, 70 }),
        msg = "Incorrect probe sequence.")

    with self.vis():
      t = task4.HashTable(128, 1)
      for key in ['ad', 'ac', 'ca']:
        t[key] = 1
      self.assertTrue(check_layout(t, { 68, 69, 72 }),
        msg = "Incorrect probe sequence.")

    assert self.check_okay("probe sequence")

  def test_statistics(self):
    with self.vis():
      t = task4.HashTable(128, 1) 
      for key in ['ad', 'ac', 'ca']:
          t[key] = 1
      self.assertEqual(t.statistics(), (1, 2, 2, 0),
        "Incorrect statistics.")

    with self.vis():
      t = task4.HashTable(128, 1) 
      for key in ['ac', 'ca', 'bb']:
          t[key] = 1
      self.assertEqual(t.statistics(), (2, 3, 2, 0),
        "Incorrect statistics.")

    assert self.check_okay("statistics")

  # Functionality tests are the same as Task 1.
  def test_contains(self):
    x = task4.HashTable(1024, 1)

    with self.vis():
      self.assertFalse("abcdef" in x, "False positive in __contains__ for empty table.")

    with self.vis("unexpected failure in setitem"):
      x["abcdef"] = 18
      x["definitely a string"] = None
      x["abdcef"] = "abcdef"
    
    for key in ["abcdef", "definitely a string", "abdcef"]:
      with self.vis():
        self.assertTrue(key in x, "False negative in __contains__ for key {}".format(key))

    assert self.check_okay("contains")

  def test_getitem(self):
    x = task4.HashTable(1024, 1)

    with self.vis():
      with self.assertRaises(KeyError, msg="x[key] should raise KeyError for missing key."):
        elt = x["abcdef"]
      
    with self.vis("unexpected failure in setitem"):
      x["abcdef"] = 18
      x["definitely a string"] = None

    with self.vis():
      self.assertEqual(x["abcdef"], 18, msg = "Read after store failed.")
    assert self.check_okay("getitem")

if __name__ == '__main__':
  unittest.main()
