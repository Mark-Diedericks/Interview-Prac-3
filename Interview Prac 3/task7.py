"""
Linear Probing Hash Table based frequency analysis of text files, extended

@author         Mark Diedericks 30572738
@since          21/10/2019
@modified       21/10/2019
"""

from task1 import HashTable
from task6 import Freq as FreqBase

class Freq(FreqBase):
    def __init__(self):
        """
        Instantiates a new instance of the Freq class, loading in the default files

        @return         None
        @complexity     O(1) for both best and worst case.
        @postcondition  A hash table with a load factor of 0.5 is created as word_frequency and populated with words
                        and frequencies from the default files.
        """
        super().__init__()

    def evaluate_frequency(self, filename):
        """
        Will load a file and add each line as a key to hash_table with it's frequency as the value
        
        @param          filename: name of the file to load
        @return         Respective perctentage occurances of each rarity score for all words in the given file
        @complexity     O(n) for both best and worst case. Where n is the number of words
        @precondition   The file, filename, must exist
        """

        assert isinstance(filename, str)

        # Use a hash table to ensure only unique words are used
        word_table = HashTable(1000081, 27183)

        # Create rarity count array, from 0, 1, 2 and 3
        rarity_counts = [0] * 4

        # Open the file, read each line, add word to hash table with value of 1
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                # Get each individual word in the line
                words = line.replace('\n', '').split(' ')

                for w in words:
                    word = w.strip().lower() # Ensure no spaces are included in the word

                    # Skip word if we've already encountered it
                    if word in word_table:
                        continue

                    # Add word to word table to ensure it isn't done again
                    word_table[word] = 1

                    # Calculate the rarity score for the word and increment count for score
                    score = self.rarity(word)
                    rarity_counts[score] += 1

        # Ensure file is closed
        if not f.closed:
            raise IOError('File is not closed.')

        # Calculate total count
        total = 0
        for count in rarity_counts:
            total += count

        # Calculate percentages for each rarity
        percentages = [round(rarity_counts[i] / total * 100.0) for i in range(len(rarity_counts))]

        # Return percentages as tuple
        return tuple(percentages)


if __name__ == '__main__':
    # Evaluate percentage frequencies of 84-0.txt
    f = Freq()
    f.load_default_frequency()
    results = f.evaluate_frequency('Ebooks/84-0.txt')
    print(results)