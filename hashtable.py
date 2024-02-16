#Creating the hash table
#Source: W-1_ChainingHashTable_zyBooks_Key-Value.py
class hashtable:
    def __init__(self, initialcapacity=40):
        self.table = []
        for i in range(initialcapacity):
            self.table.append([])

    #Inserts a new item into the hash table and will update an item in the list already
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #update key if it is already in the bucket
        for kv in bucket_list:
            #print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True
        #if not in the bucket, insert item to the end of the list    
        key_value = [key, item]
        bucket_list.append(key_value)
        return True
    #Searches the hash table for an item with the matching key
    #Will return the item if founcd, or None if not found
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #print(bucket_list)
        #search key in bucket
        for kv in bucket_list:
            #print(key_value)
            if kv[0] == key:
                return kv[1]  #value
        return None 
        
    #Removes an item with matching key from the hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #removes the item if it is present
        if key in bucket_list:
            bucket_list.remove(key)
