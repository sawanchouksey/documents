# Add item from list in array using fromlist() method

import array

arr = array.array('i',[0,1,2,3])

li = [9,0,8]

arr.fromlist(li)

print(arr)