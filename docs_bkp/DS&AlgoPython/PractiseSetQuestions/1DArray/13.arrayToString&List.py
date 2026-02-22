# Convert array to string using tostring() method

import array

# Create a 1D array of integers
arr = array.array('i', [1, 2, 3, 4, 5])

# Convert the array to bytes
byte_string = arr.tobytes()
print("Byte String:", byte_string)

# Convert the byte string back to an array
# Note: You need to know the typecode ('i' for integers in this case)
new_arr = array.array('i')
new_arr.frombytes(byte_string)
print("Converted Array:", new_arr)

# Convert to list and print
print(new_arr.tolist())

