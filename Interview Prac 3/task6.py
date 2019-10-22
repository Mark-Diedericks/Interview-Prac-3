"""
Linear Probing Hash Table based frequency analysis of text files

@author         Mark Diedericks 30572738
@since          21/10/2019
@modified       21/10/2019
"""

from task1 import HashTable
import string

class Freq:
    def __init__(self):
        """
        Instantiates a new instance of the Freq class

        @return         None
        @complexity     O(1) for both best and worst case.
        @postcondition  A hash table with a load factor of 0.5 is created as word_frequency
        """
        self.word_frequency = HashTable(load_factor = 0.5)
        self.max_count = 0
  
    def add_file(self, filename):
        """
        Will load a file and add each word as a key to hash_table with it's frequency as the value
        
        @param          filename: name of the file to load
        @return         None
        @complexity     O(mn) for both best and worst case. Where m is cost of hash table setitem and n is the number of words
        @precondition   The file, filename, must exist
        @postcondition  word_frequency will contain all unique words in the file as keys with values of their frequency
        """
        assert isinstance(filename, str)
        tans = str.maketrans('', '', string.punctuation)

        # Open the file, read each line, add word to hash table with value of 1
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                # Skip blank lines
                if len(line.strip()) <= 0:
                    continue
                
                # Get each individual word in the line
                words = line.strip().replace('\n', '').split(' ')

                for w in words:
                    word = w.strip().lower().translate(trans) # Ensure no spaces or punctuation are included in the word

                    if not word in self.word_frequency:  # If word does not exist in hash table, add it as 1
                        self.word_frequency[word] = 0

                    # Set the new count
                    self.word_frequency[word] += 1

                    # Check if the new count should be the new max
                    if self.word_frequency[word] > self.max_count:
                        self.max_count = self.word_frequency[word];

        # Ensure file is closed
        if not f.closed:
            raise IOError('File is not closed.')

    def rarity(self, word):
        """
        Will return a rarity score for a given word based on the contents of the word_frequency hash table.
        
        @param          word: the word for which to calculate the rarity score
        @return         An integer rarity score in the range [0, 3]
        @complexity     O(n) for both best and worst case. Where m is cost of hash table getitem and contains (both should be the same)
        @precondition   The word is a string instance
        """
        assert isinstance(word, str)
        
        # Never observed word = score of 3
        if word not in self.word_frequency:
            return 3

        # Get frequency of word
        count = self.word_frequency[word]

        # Calculate score and return
        if count >= (self.max_count / 100.0):     # Appears at least max/100
            return 0
        elif count >= (self.max_count / 1000.0):  # Appears at least max/1000 but less than max/100
            return 1
        else:                                     # Appears less than max/1000
            return 2

    def load_default_frequency(self):
        """
        Will load a file and add each line as a key to hash_table with it's frequency as the value
        
        @param          filename: name of the file to load
        @return         None
        @complexity     O(mn) for both best and worst case. Where m is cost of hash table setitem and n is the number of lines
        @precondition   The file, filename, must exist
        @postcondition  word_frequency will contain all unique lines in the file as keys with values of their frequency
        """
        
        # Reset self, use large table size for many words
        self.word_frequency = HashTable(4999559, 52361, 0.5)
        self.max_count = 0

        # Load default files into hash table
        self.add_file('Ebooks/1342-0.txt')
        self.add_file('Ebooks/2600-0.txt')
        self.add_file('Ebooks/98-0.txt')


if __name__ == '__main__':
    f = Freq()
    f.load_default_frequency()