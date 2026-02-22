# check for number of occurence of an element using count() method

import array

arr = array.array('i',[0,1,2,1,4,5,1,1,9])

def occurenceElementCount(arr,element):
    print(f'occurence of element {element} in array is {arr.count(element)}')

occurenceElementCount(arr,1)
