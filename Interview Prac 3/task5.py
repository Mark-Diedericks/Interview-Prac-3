"""
Separate Chaining Hash Table based functions, timings and statistics

@author         Mark Diedericks 30572738
@since          21/10/2019
@modified       21/10/2019
"""

import bst
from task1 import HashTable as HashTableLinear
from task3 import load_dictionary_statistics

class BinarySearchTree(bst.BinarySearchTree):
    def insert(self, key, value):
        """
        Will attempt to insert at a value with a given key

        @param          key: The key to search for and get it's value
        @return         The depth at which the key-value pair was inserted
        @complexity     O(log n) for both best and worst case, where n is the depth of the binary search tree
        @postcondition  The binary search tree will contain the given key-value par
        """
        if self.root is None:
            self.root = bst.BinaryTreeNode(key, value)
            return 0 # It was the root node, so depth of 0

        depth = 0 # Start at root, so depth of 0
        current_node = self.root
        while True:
          if key < current_node.key:
            depth += 1 # Increment depth at where the insert is
            if current_node.left is None:
              current_node.left = bst.BinaryTreeNode(key, value)
              break
            else:
              current_node = current_node.left
          elif key > current_node.key:
            depth += 1 # Increment depth at where the insert is
            if current_node.right is None:
              current_node.right = bst.BinaryTreeNode(key, value)
              break
            else:
              current_node = current_node.right
          else:
            assert current_node.key == key
            current_node.item = value
            break

        # Return set/insertion depth
        return depth

class HashTable(HashTableLinear):   
    ### Override only the methods which directly implement linear probing ###
    ### Implement separate chaining instead.                              ###
    
    def __getitem__(self, key):
        """
        Will attempt to get the value associoated with the given key

        @param          key: The key to search for and get it's value
        @return         The value of associated with the given key
        @raises         KeyError: key does not exist in the hash table
        @complexity     O(log n) for both best and worst case, where n is the length of the binary search tree,
        @precondition   The parameter key is of type string
        @postcondition  The value for the key will be returned if the key exists within the hash table
        """
        
        # assert preconditions
        assert isinstance(key, str)

        # Get starting index and table size
        i = self.hash(key)

        # If slot is not empty, attempt to find key
        # BinarySearchTree will raise KeyError if not found.
        if self.table[i] is not None:
            assert isinstance(self.table[i], BinarySearchTree)
            return self.table[i][key]

        # Key wasn't found
        raise KeyError('Key does not exist in table.')

    def __setitem__(self, key, item):
        """
        Will set value of existing key-value pair, insert new key-value pair if not existent within dictionary. 
        Will also rehash the hash table if it is full, inserting the key-value pair afterwards.

        @param          key: The key of the key value pair, hashed to find index
        @param          item: The value associated with the key
        @return         None
        @complexity     O(log n) for both best and worst case, where n is the length of the binary search tree,
        @precondition   The parameter key is of type string
        @postcondition  The hash table will contain the the item at for the given key
        """
        
        # assert preconditions
        assert isinstance(key, str)

        # Get starting index and table size
        i = self.hash(key)

        # If a pair is where this is meant to be, we have a collision
        # If that pair has the same key we are setting, not inserting
        # thus it cannot count as a collision.
        if self.table[i] is not None:
            self.collisions += 1
        else:
            self.table[i] = BinarySearchTree()
            
        assert isinstance(self.table[i], BinarySearchTree)

        # Insert/set and get probe length stat
        depth = self.table[i].insert(key, item)
        self.count += 1

        # We're adding a new pair, so consider probe length
        self.probe_len += depth
        if depth > self.probe_max:
            self.probe_max = depth

    def __contains__(self, key):
        """
        Determines whether or not the hash table contains a specified key

        @param          key: the key to search for
        @return         Whether or not the key exists within the hash table
        @complexity     O(1) for best case - no BST. O(log n) for  worst case, where n is the length of the binary search tree,
        @precondition   The parameter key is of type string
        """
        
        # assert preconditions
        assert isinstance(key, str)

        # Get starting index and table size
        i = self.hash(key)
        if self.table[i] is not None:
            assert isinstance(self.table[i], BinarySearchTree)
            return key in self.table[i]

        # Key wasn't found
        return False


def table_load_dictionary_statistics(max_time):
    """
    Will execute load_dictionary_time on a combination of files, sizes and bases. Saving the data, along with timing and words
    to a file. Uses separate chaining hash table..
    
    @param          max_time: how long load_dictionary operates before timing out, if none the function wont time out
    @return         None
    @complexity     O(nm) for both best and worst case. Where n is cost of load_dictionary and m is the number of size-base-file combinations
    @postcondition  A file, 'output_task5.csv', will contain the filename, table, base, words, collisions, probe length, max probe length 
                    and rehash count time data for each combination.
    """

    TABLE_BASE = [1, 27183, 250726]
    TABLE_SIZE = [250727, 402221, 1000081]
    FILE_NAMES = ["english_small.txt", "english_large.txt", "french.txt"]

    # Get output file handle
    f = open("output_task5.csv", 'w+', encoding="UTF-8")

    # Create headers
    f.write('File Name,Table Size,Table Base,Words,Time,Collisions,Probe Total,Probe Max, Rehashes\n')

    # Loop through each combination
    for file in FILE_NAMES:
        for size in TABLE_SIZE:
            for base in TABLE_BASE:
                # Run combination with quadratic probing hash table
                res = load_dictionary_statistics(base, size, file, max_time, HashTable(size, base))

                words = res[0]
                time = res[1] if res[1] is not None else "TIMEOUT"
                col = res[2]
                pro = res[3]
                promax = res[4]
                rehashes = res[5]

                # Print results to file
                f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'.format(file, size, base, words, time, col, pro, promax, rehashes))
                print('{0},{1},{2},{3},{4},{5},{6},{7},{8}'.format(file, size, base, words, time, col, pro, promax, rehashes))

    # Close file
    f.close()

    # Ensure file is closed
    if not f.closed:
        raise IOError('File is not closed.')


if __name__ == '__main__':
    table_load_dictionary_statistics(120)

