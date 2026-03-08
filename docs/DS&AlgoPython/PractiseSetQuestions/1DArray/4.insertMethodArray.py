import array

arr = array.array('i',[1,2,5,7,8])

def inserElementArray(arr,index,element):
    arr.insert(index,element)
    print(arr)

inserElementArray(arr,0,9)