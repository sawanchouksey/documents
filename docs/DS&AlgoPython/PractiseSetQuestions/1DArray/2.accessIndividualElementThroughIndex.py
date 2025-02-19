# Access individual element through indexes

import array

arr = array.array('i',[1,4,5,0,7,6])

def accessElementThroughIndex(arr,index):
    if index >= len(arr):
        print(f"Element doesn't exist because index out of range")
    else:
        print(f"Element exist in {index} :", arr[index])

accessElementThroughIndex(arr,3)
