# Class to create the hash table
# Source code taken from WGU code: W-1_ChainingHashTable_zyBooks_Key-Value.py

class HashTable:
    def __init__(self, table_capacity=30):
        # Creates a list to hold table values in
        self.table = []
        # For every value that the table can hold append a value to it
        for count in range(table_capacity):
            self.table.append([])

    # Update an existing item in the list and add in a new item
    def insert(self, key, item):
        # The hash table will have key/values entered into it
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # If key is already in the bucket_list then update the key
        for temp_key in bucket_list:
            # Checking if the key will be updated
            if temp_key[0] == key:
                temp_key[1] = item
                return True
        # If key is not already in bucket_list then append it after the values already in it
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Look in the hash table for a key that's the same as the one being looked at
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
            # If key is found then return it
            if kv[0] == key:
                return kv[1]
        # Key is not found so nothing is returned
        return None

    # Function to remove a key if it's the same as the one in the hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # For every key in the bucket_list
        for kv in bucket_list:
            # If the key value matches then remove it
            if kv[0] == key:
                # Removing both the key and the item associated with it
                bucket_list.remove([kv[0], kv[1]])
                return


'''
***Extra Notes***
Refer to the heading about some of the code in the Hashtable.py class being taken from WGU created code, file
W-1_ChainingHashTable_zyBooks_Key-Value.py
'''
