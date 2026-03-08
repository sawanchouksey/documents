# get array buffer information through buffer_info() method

import array

arr = array.array('i',[1,2,3,4,5,6])

print(arr.buffer_info()) #return (currentMemoryAddress, Lenght) of an array