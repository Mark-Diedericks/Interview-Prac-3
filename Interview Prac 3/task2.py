"""
HashTable based functions and timings

@author         Mark Diedericks 30572738
@since          15/10/2019
@modified       15/10/2019
"""

import timeit
import task1

def load_dictionary(hash_table, filename, time_limit = None):
    """
    Will load a file and add each line as a key to hash_table with a value of 1
    
    @param          hash_table: the hash_table where lines will be added to
    @param          filename: name of the file to load
    @param          time_limit: how long the funciton operates before timing out, if none the function wont time out
    @return         None
    @complexity     O(mn) for both best and worst case. Where m is cost of hash table setitem and n is the number of lines
    @postcondition  The hash table will contain all unique lines in the file as keys with values of 1
    """

    # Save beginning time
    start = timeit.default_timer()

    # Open the file, read each line, add word to hash table with value of 1
    with open(filename, 'r', encoding='utf-8') as f:
        for word in f:
            hash_table[word] = 1

            # If we've reached our time limit, break the operation
            if time_limit is not None and timeit.default_timer() - start >= time_limit:
                raise Exception('Time limit exceeded.')

    # Ensure file is closed
    if not f.closed:
        raise IOError('File is not closed.')

def load_dictionary_time(hash_base, table_size, filename, max_time):
    """
    Will load a file and add each line as a key to hash_table with a value of 1, returning count of words and the time taken
    
    @param          hash_base: the base of the hash table
    @param          table_size: the capacity of the hash table
    @param          filename: name of the file to load
    @param          max_time: how long load_dictionary operates before timing out, if none the function wont time out
    @return         (count of words, time taken)   Time taken will be None if load_dictionary timed-out
    @complexity     O(n) for both best and worst case. Where n is cost of load_dictionary
    """
    
    # Create a hash table
    tbl = task1.HashTable(table_size, hash_base)
    
    # Save beginning time
    start = timeit.default_timer()

    try:
        # Load the file into hash table
        load_dictionary(tbl, filename, max_time)
    except:
        pass

    words = len(tbl)

    # Elapsed time
    elapsed = timeit.default_timer() - start
    time = elapsed if elapsed <= max_time else None

    return (words, time)


def table_load_dictionary_time(max_time):
    """
    Will execute load_dictionary_time on a combination of files, sizes and bases. Saving the data, along with timing and words
    to a file.
    
    @param          max_time: how long load_dictionary operates before timing out, if none the function wont time out
    @return         None
    @complexity     O(nm) for both best and worst case. Where n is cost of load_dictionary and m is the number of size-base-file combinations
    @postcondition  A file, 'output_task2.csv', will contain the filename, tale, base, words and time data for each combination.
    """

    TABLE_BASE = [1, 27183, 250726]
    TABLE_SIZE = [250727, 402221, 1000081]
    FILE_NAMES = ["english_small.txt", "english_large.txt", "french.txt"]

    start = timeit.default_timer()

    # Get output file handle
    f = open("output_task2.csv", 'w+', encoding="UTF-8")

    # Create headers
    f.write('File Name,Table Size,Table Base,Words,Time\n')

    # Loop through each combination
    for file in FILE_NAMES:
        for size in TABLE_SIZE:
            for base in TABLE_BASE:

                # Run combination
                res = load_dictionary_time(base, size, file, max_time)

                words = res[0]
                time = res[1] if res[1] is not None else "TIMEOUT"

                # Print results to file
                print('{0}, {1}, {2}, {3}'.format(file, size, base, timeit.default_timer() -  start))
                f.write('{0},{1},{2},{3},{4}\n'.format(file, size, base, words, time))

    # Close file
    f.close()

    # Ensure file is closed
    if not f.closed:
        raise IOError('File is not closed.')
    
if __name__ == '__main__':
    table_load_dictionary_time(120)