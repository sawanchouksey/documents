## Python Programming

### Python Scripting & Development

##### Q. Exception handling keywords?
- **try:** Code that might cause exception
- **catch:** Handle exception
- **else:** Execute if no exception
- **finally:** Execute regardless of exception

##### Q. What is *args in function?
Allows any number of arguments as tuple.
```python
def sum(*args):
    return sum(args)
```

##### Q. What is **kwargs in function?
Allows any number of keyword arguments as dictionary.
```python
def sum(**kwargs):
    return sum(kwargs.values())
```

##### Q. What is list comprehension?
Concise way to create lists:
```python
# Copy listA to listB with adding 1
listA = [1, 2, 3]
listB = [n + 1 for n in listA]

# With condition
l1 = ['sawan', 'muskan', 'srajan', 'vasu']
l2 = [name.upper() for name in l1 if len(name) > 5]
```

##### Q. Leap year conditions?
1. Divisible by 4
2. NOT divisible by 100 (except...)
3. OR divisible by 400

##### Q. Block scope in Python?
No block scope in Python - if/else/for/while blocks share scope with surrounding code.

##### Q. Output of print(734_529.678)?
734529.678 (underscores are ignored in numeric literals)

##### Q. Reverse string in Python?
```python
# Slicing
txt = "Hello World"[::-1]

# Loop
def reverse(s):
    str = ""
    for i in s:
        str = i + str
    return str
```

---

