# Remove element from Array with the help of remove() method

import array

arr = array.array('i',[1,2,3,0])

def removeElementFromArray(arr,element):
    if element in arr:
        arr.remove(element)
        print(arr)
    else:
        print("element doesn't exist")

removeElementFromArray(arr,4)