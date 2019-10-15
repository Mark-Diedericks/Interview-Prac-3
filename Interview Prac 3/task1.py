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

        self.collisions = 0
        self.probe_len = 0
        self.probe_max = 0
        self.rehashes = 0

    def __len__(self):
        """
        Will return the count of key-value pairs in the hash table

        @return         The count of key-value pairs
        @complexity     O(1) for both best and worst case
        """
        return self.count
  
    def __getitem__(self, key):
        """
        Will attempt to get the value associoated with the given key

        @param          key: The key to search for and get it's value
        @return         The value of associated with the given key
        @raises         KeyError: key does not exist in the hash table
        @complexity     O(m) for best case - no probing. O(n + m) for worst case - linear probing. Where n is self.count and m is key length
        @postcondition  The value for the key will be returned if the key exists within the hash table
        """

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
        """
        Will set value of existing key-value pair, insert new key-value pair if not existent within dictionary. 
        Will also rehash the hash table if it is full, inserting the key-value pair afterwards.

        @param          key: The key of the key value pair, hashed to find index
        @param          item: The value associated with the key
        @return         None
        @complexity     O(m) for best case - at hash index. O(nm) for worst case - rehash. Where n is self.count and m is (average) key length
        @postcondition  The hash table will contain the the item at for the given key
        """

        # Get starting index and table size
        i = self.hash(key)
        n = len(self.table)

        # If a pair is where this is meant to be, we have a collision
        # If that pair has the same key we are setting, not inserting
        # thus it cannot count as a collision.
        if self.table[i] is not None and self.table[i][0] != key:
            self.collisions += 1

        # Circularly loop until we either find the element or nothing 
        for j in range(n):
            k = (i + j) % n

            # Stop searching if we reach an empty slot, just insert element
            if self.table[k] is None:
                self.table[k] = (key, item)
                self.count += 1

                # We're adding a new pair, so consider probe length
                self.probe_len += j
                if j > self.probe_max:
                    self.probe_max = j

                return

            # Check if the element is the desired one
            if self.table[k][0] == key:
                self.table[k] = (key, item)

                # We're not adding a new pair, so disregard probe length
                return

        # Key wasn't found nor an empty slot for it, rehash and insert
        self.rehash()
        self[key] = item

    def __contains__(self, key):
        """
        Determines whether or not the hash table contains a specified key

        @param          key: the key to search for
        @return         Whether or not the key exists within the hash table
        @complexity     O(m) for best case - no probing. O(n + m) for worst case - linear probing. Where n is self.count and m is key length
        """

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
        """
        Will return an integer hash of the inputted key

        @param          key: the key which will be hashed
        @return         The integer hash value of the specified key
        @complexity     O(n) for both best and worst case, where n is the length of the key
        """

        val = 0
        # Hash key, power = self.base, divisor = len(self.table)
        for i in range(len(key)):
            val = (val*self.base + ord(key[i])) % len(self.table)

        return val


    def rehash(self):
        """
        Will change capacity of the hash table to the next highest prime above the double of its
        original capacity.

        @param          None
        @return         None
        @complexity     O(mn) best case - no collisions inserting. O(mn^2) for worst case - maximum collisions inserting. Where m is (average) key length and n is self.count
        @postcondition  The hash table will contain the same key-value pairs however will have a capacity of double rounded up to the nearest prime in PRIMES.
        """

        # Calculate new size
        capacity = self.get_size(len(self.table))

        # Increment rehash counter, reset collisions and probes
        self.rehashes += 1
        self.collisions = 0
        self.probe_len = 0
        self.probe_max = 0

        tbl_old = self.table
        self.table = [None] * capacity

        # Iterate over old table and insert the key-value pairs into new table
        for pair in tbl_old:
            # Table was not full, skip empty pair
            if pair is None:
                continue

            # Add the pair to the new table
            self[pair[0]] = pair[1]


    def get_size(self, capacity):
        """
        Will get the closest, looking up, number prime to double the inputted capacity.

        @param          capacity: the original capacity to be doubled and rounded up to nearest prime
        @return         Closest prime above double the capacity
        @raises         ValueError: when no value in PRIMES is greater than or equal to double the capacity
        @complexity     O(log n) for both best and worst case, where n is the length of PRIMES
        """
        
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


    def statistics(self):
        """
        Returns a tuple of hash table statistics

        @param          None
        @return         (# of collisions, total probe length, maximum probe length, # of rehashes)
        @complexity     O(1) for both best and worst case
        """

        return (self.collisions, self.probe_len, self.probe_max, self.rehashes)