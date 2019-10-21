"""
Quadratic Probing Hash Table based functions, timings and statistics

@author         Mark Diedericks 30572738
@since          21/10/2019
@modified       21/10/2019
"""

from task1 import HashTable as HashTableLinear
from task3 import load_dictionary_statistics

class HashTable(HashTableLinear):   
    ### Override only the methods which directly implement linear probing ###
    ### Implement quadratic probing instead.                              ###
    
    def probe_step(self, i):
        """
        Will return an integer step for the given index.

        @param          i: the index at which to calculate the step
        @return         The step, from the original hash index, which should be taken
        @complexity     O(1) for both best and worst case
        """
        return i**2;


def table_load_dictionary_statistics(max_time):
    """
    Will execute load_dictionary_time on a combination of files, sizes and bases. Saving the data, along with timing and words
    to a file. Uses quadratic probing hash table instead of a linear probing hash table.
    
    @param          max_time: how long load_dictionary operates before timing out, if none the function wont time out
    @return         None
    @complexity     O(nm) for both best and worst case. Where n is cost of load_dictionary and m is the number of size-base-file combinations
    @postcondition  A file, 'output_task4.csv', will contain the filename, table, base, words, collisions, probe length, max probe length 
                    and rehash count time data for each combination.
    """

    TABLE_BASE = [1, 27183, 250726]
    TABLE_SIZE = [250727, 402221, 1000081]
    FILE_NAMES = ["english_small.txt", "english_large.txt", "french.txt"]

    # Get output file handle
    f = open("output_task4.csv", 'w+', encoding="UTF-8")

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

    # Close file
    f.close()

    # Ensure file is closed
    if not f.closed:
        raise IOError('File is not closed.')


if __name__ == '__main__':
    table_load_dictionary_statistics(120)