"""
Linear Probing Hash Table based frequency analysis of text files

@author         Mark Diedericks 30572738
@since          21/10/2019
@modified       21/10/2019
"""

from task1 import HashTable
class Freq:
    def __init__(self):
        self.word_frequency = HashTable()
        self.max_count = 0
  
    def add_file(self, filename):
        """
        Will load a file and add each line as a key to hash_table with it's frequency as the value
        
        @param          filename: name of the file to load
        @return         None
        @complexity     O(mn) for both best and worst case. Where m is cost of hash table setitem and n is the number of lines
        @precondition   The file, filename, must exist
        @postcondition  word_frequency will contain all unique lines in the file as keys with values of their frequency
        """

        # Open the file, read each line, add word to hash table with value of 1
        with open(filename, 'r', encoding='utf-8') as f:
            for word in f:
                if not word in self.word_frequency:  # If word does not exist in hash table, add it as 1
                    self.word_frequency[word] = 0

                # Set the new count
                count = self.word_frequency[word] + 1
                self.word_frequency[word] = count

                # Check if the new count should be the new max
                if count > self.max_count:
                    self.max_count = count;

        # Ensure file is closed
        if not f.closed:
            raise IOError('File is not closed.')

    def rarity(self, word):
        
        # Never observed word = score of 3
        if not word in self.word_frequency:
            return 3

        # Get frequency of word
        count = self.word_frequency[word]

        # Calculate score and return
        if count >= (max / 100.0):     # Appears at least max/100
            return 0
        elif count >= (max / 1000.0):  # Appears at least max/1000 but less than max/100
            return 1
        else:                          # Appears less than max/1000
            return 2


    def evaluate_frequency(self, other_filename):
        raise NotImplementedError
