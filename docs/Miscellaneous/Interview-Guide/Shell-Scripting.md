## Shell Scripting

### Bash & Shell Programming

##### Q. Find length of string variable?
```bash
${#string}
```

##### Q. Convert string to substring?
```bash
string="abcdef"
echo "${string:1}"      # bcdef
echo "${string:4}"      # ef
echo "${string:0:3}"    # abc
echo "${string:3:3}"    # def
echo "${string: -1}"    # f
```

##### Q. Set default value for variable?
```bash
name=${name:-'default_value'}
```

##### Q. Check if user passed value?
```bash
#!/bin/bash
: ${1:?"Please provide a variable value"}
echo "You provided: $1"
```

##### Q. Script output examples?
```bash
# Script 1
#!/bin/bash
echo ${0}  # script name
echo ${1}  # first argument
echo ${2}  # second argument

./test.sh test 20
# Output: test.sh, test, 20

# Script 2
#!/bin/bash
echo $#    # number of arguments
echo $@    # all arguments (separate)
echo $*    # all arguments (combined)

./test.sh sawan 20 21 34
# Output: 4, sawan 20 21 34, sawan 20 21 34

# Script 3
#!/bin/bash
pwd="sawan"
echo ${pwd}  # variable value
echo $(pwd)  # command output
echo `pwd`   # command output

# Output: sawan, /current/directory, /current/directory

# Script 4 - readonly
#!/bin/bash
pwd="sawan"
echo ${pwd}  # sawan
pwd="test"
echo ${pwd}  # test
readonly pwd
pwd="chouksey"  # Error: readonly variable
echo ${pwd}  # test
```

---

