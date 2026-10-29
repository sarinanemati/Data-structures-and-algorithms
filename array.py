import ctypes

class DynamicArray:
    
    def __init__(self):
        self._n = int(0)                  
        self._capacity = int(1)           
        self._A = self._make_array(self._capacity)  

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        if not (0 <= k < self._n):
            raise IndexError('invalid index')
        return self._A[k]                    

    def append(self, obj):
        if self._n == self._capacity:        
            self._resize(2 * self._capacity) 
        self._A[self._n] = obj
        self._n += 1

    def insert(self, k, value):

        if not (0 <= k <= self._n):
            raise IndexError('invalid index')
        if self._n == self._capacity:        
            self._resize(2 * self._capacity) 
        for j in range(self._n, k, -1):      
            self._A[j] = self._A[j-1]
        self._A[k] = value                   
        self._n += 1

    def pop(self, k=None):
        if self._n == 0:
            raise IndexError('array is empty')
        if k is None:
            k = self._n - 1
        if not (0 <= k < self._n):
            raise IndexError('invalid index')
        
        value = self._A[k]
        for j in range(k, self._n - 1):      
            self._A[j] = self._A[j+1]
        self._n -= 1
        return value

    def remove(self, value):
        for k in range(self._n):
            if self._A[k] == value:         
                for j in range(k, self._n - 1): 
                    self._A[j] = self._A[j+1]
                self._A[self._n - 1] = None  
                self._n -= 1
                return
        raise ValueError('value not found')

    def _resize(self, c):
        b = self._make_array(c)              
        for k in range(self._n):
            b[k] = self._A[k]               
        self._A = b                         
        self._capacity = c

    def _make_array(self, c):
        return (c * ctypes.py_object)()

    def __str__(self):
        return str([self._A[i] for i in range(self._n)])


if __name__ == "__main__":
    print("1. Creating an empty dynamic array")
    arr = DynamicArray()
    print(f"Length: {len(arr)}, Initial Capacity: {arr._capacity}, Contents: {arr}\n")

    print("2. Testing append method")
    for val in [10, 20, 30, 40, 50]:
        arr.append(val)
        print(f"Appended {val} -> Length: {len(arr)}, Capacity: {arr._capacity}, Contents: {arr}")
    print()

    print("3. Testing insert method")
    print(f"Contents before insertion: {arr}")
    print(f"Inserted 99 at index 2 -> Contents: {arr}, New Length: {len(arr)}, Capacity: {arr._capacity}")
    print()

    print("4. Testing direct indexing")
    print(f"Element at index 0: {arr[0]}")
    print(f"Element at index 2 (newly inserted): {arr[2]}")
    print(f"Element at last index ({len(arr)-1}): {arr[len(arr)-1]}")
    print()

    print("5. Testing remove method")
    print(f"Contents before removing 30: {arr}")
    arr.remove(30)
    print(f"After removing 30 -> Contents: {arr}, Length: {len(arr)}")
    print()

    print("6. Testing pop method")
    popped_val = arr.pop(1) 
    print(f"Popped value from index 1: {popped_val}")
    print(f"Contents after pop: {arr}, Length: {len(arr)}, Current Capacity: {arr._capacity}")
