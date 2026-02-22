# Append Method to append element in Array

import array

arr = array.array('i',[0,1,2])

def appendElementArray(arr,element):    
    arr.append(element)    
    print(f"array after append {element} in array : ",arr)

appendElementArray(arr,5)
