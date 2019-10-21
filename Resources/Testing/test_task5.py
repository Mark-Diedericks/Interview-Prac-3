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
    assert self.check_okay("getitem")

if __name__ == '__main__':
  unittest.main()
