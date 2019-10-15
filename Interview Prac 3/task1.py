"""
List based implementation of HashTable

@author         Mark Diedericks 30572738
@since          15/10/2019
@modified       15/10/2019
"""

class HashTable:
    PRIMES = [3, 7, 11, 17, 23, 29, 37, 47, 59, 71, 89, 107, 131, 163, 197, 239, 293, 353, 431, 521, 631, 761,
            919, 1103, 1327, 1597, 1931, 2333, 2801, 3371, 4049, 4861, 5839, 7013, 8419, 10103, 12143, 14591,
            17519, 21023, 25229, 30313, 36353, 43627, 52361, 62851, 75521, 90523, 108631, 130363, 156437,
            187751, 225307, 270371, 324449, 389357, 467237, 560689, 672827, 807403, 968897, 1162687, 1395263,
            1674319, 2009191, 2411033, 2893249, 3471899, 4166287, 4999559, 5999471, 7199369]

    def __init__(self, table_capacity = 1103, hash_base = 31): 
        """
        Instantiates a new instance of the HashTable class with a specified capacity and base.

        @param          table_capacity: the capacity of the hash table
        @param          hash_base: the base used in the hash funciton
        @return         None
        @complexity     O(1) for both best and worst case.
        @postcondition  A list of size table_capacity is created for the instance, populated with None
        """
        self.table = [None] * table_capacity
        self.base = hash_base
        self.count = 0
  
    def __getitem__(self, key):

        # Get starting index and table size
        i = self.hash(key)
        n = len(self.table)

        # Circularly loop until we either find the element or nothing 
        for j in range(n):
            k = (i + j) % n

            # Stop searching if we reach an empty slot
            if self.table[k] is None:
                break

            # Check if the element is the desired one
            if self.table[k][0] == key:
                return self.table[k][1]

        # Key wasn't found
        raise KeyError('Key does not exist in table.')

    def __setitem__(self, key, item):
        # Get starting index and table size
        i = self.hash(key)
        n = len(self.table)

        # Circularly loop until we either find the element or nothing 
        for j in range(n):
            k = (i + j) % n

            # Stop searching if we reach an empty slot, just insert element
            if self.table[k] is None:
                self.table[k] = (key, item)
                self.count += 1
                return

            # Check if the element is the desired one
            if self.table[k][0] == key:
                self.table[k][1] = item
                return

        # Key wasn't found nor an empty slot for it, rehash and insert
        rehash()
        self[key] = item

    def __contains__(self, key):

        # Get starting index and table size
        i = self.hash(key)
        n = len(self.table)

        # Circularly loop until we either find the element or nothing 
        for j in range(n):
            k = (i + j) % n

            # Stop searching if we reach an empty slot
            if self.table[k] is None:
                return False

            # Check if the element is the desired one
            if self.table[k][0] == key:
                return True

        # Key wasn't found
        return False

    def hash(self, key):

        val = 0
        # Hash key, power = self.base, divisor = len(self.table)
        for i in range(len(key)):
            val = (val*self.base + ord(key[i])) % len(self.table)

        return val


    def rehash(self):

        # Calculate new size
        capacity = get_size(len(self.table))

        tbl_old = self.table
        self.table = [None] * capacity

        # Iterate over old table and insert the key-value pairs into new table
        for pair in range(tbl_old):
            # Table was not full, warn
            if pair is None:
                print('WARN: Rehashing non-full table.')
                continue

            # Add the pair to the new table
            self[pair[0]] = pair[1]


    def get_size(self, capacity):
        
        # Our target value is double the capacity
        target = capacity * 2

        lo = 0
        hi = len(HashTable.PRIMES)

        # Binary search PRIMES for our target value
        while hi > lo:
            mid = (lo + hi) // 2
            val = HashTable.PRIMES[mid]

            if val == target:
                return val

            if val > target:
                hi = mid
            elif val < target:
                lo = mid+1

        # No exact match was found, our index is where we would expect the value to be,
        # this mid will be the location of the prime we want
        mid = (lo + hi) // 2
        if mid < len(HashTable.PRIMES):
            return HashTable.PRIMES[mid]

        # No value is large enough, raise ValueError
        raise ValueError('No prime large enough for capacity; {}.'.format(capacity))