# Remove last and specific index element from an array

import array

arr = array.array('i',[1,2,3,6,7,8,0])

print(arr)

arr.pop()

print(arr)

arr.pop(3)

print(arr)
