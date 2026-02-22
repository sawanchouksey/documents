# Slice an element from array by slice mechanism

import array

arr = array.array('i',[0,1,2,3,4,5])

# slice array into 3 element from 1..4 .
# 1=start index element included but not 4=last index element.

print(arr[1:4]) 

# slice from 2=specific index to all element

print(arr[2:])

# slice and print all element till 5=specific index

print(arr[:5])






