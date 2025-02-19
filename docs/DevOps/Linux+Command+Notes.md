### Linux Command List

### check and enable linux service for booting up on machine

```
sudo systemctl is-enabled nginx
sudo systemctl enable nginx
```

### Get the installed rpm package software

```
rpm -qa | grep nginx
```

###  Remove the installed rpm package software

```
sudo rpm -e nginx-module-xslt-1.24.0-1.amzn2.ngx.x86_64 nginx-1.24.0-1.amzn2.ngx.x86_64 nginx-module-image-filter-1.24.0-1.amzn2.ngx.x86_64 nginx-module-geoip-1.24.0-1.amzn2.ngx.x86_64 nginx-module-perl-1.24.0-1.amzn2.ngx.x86_64 nginx-debuginfo-1.24.0-1.amzn2.ngx.x86_64
```

### Memeory usage by process

```
pidstat -l -r|sort -k8nr|awk '{print $9 "   " $10 "   "$11}'|grep -v 0.[0-9][0-9]
```

### clear command history

```
history -c
```

### check 10 response time by command for specific website response

```
for in {1..10};
do
    curl -s -w "${time_total}\n" -o /dev/null
    https://google.com;
done
```

### Using Rsync to Sync with a Remote System with 'PUSH' operation

```
rsync -a ~/dir1 username@remote_host:destination_directory
```

### reverse sync remote to local with 'PULL' operation

```
rsync -a username@remote_host:/home/username/dir1 place_to_sync_on_local_machine
```

### X11 variable not set issue

export DISPLAY=<hostname_to_display_X11_graphics_to>:0.0
https://aws.amazon.com/blogs/compute/how-to-enable-x11-forwarding-from-red-hat-enterprise-linux-rhel-amazon-linux-suse-linux-ubuntu-server-to-support-gui-based-installations-from-amazon-ec2/

### Software Version check

```
#check nexus3 version
curl --include --silent http://HostUrl:Port/ | grep Server

#check svn version
svn --version

#mysql version
mysql -V

#docker version
docker --version

#influxdb version
influxd version

#telegraf version
telegraf --version

#nginx Version
nginx -V

#gitlab version
http://HostUrl:Port/help

#kubectl version
kubectl version

#minikube version
minikube version
```

### dockerimages removes with specific words

```
docker rmi -f $(docker images | grep wordstring grep dtc|awk {'print $3'})
```

### update *.xml file

```
sed -i 's|<level>.*</level>|<level>${LOG_LEVEL}</level>|g' os-admin-services-log4j2.xml
```

### execute remote shell script with ssh

```
sh '''
#!/bin/bash -xe
ssh T1046592@10.11.135.68 << 'ENDSSH'
cd /user/local/omnistore/baseproduct/Adeo_7th_S
mkdir bkp 
exit 0     
'ENDSSH'
'''
```

### properties upadte in .properties file

```
export oldapi=$(grep "apiUrl" web-app.properties)
export newapi=' "apiUrl": "http://10.11.142.231:8131/example-services/rest",'
sed -i "s|${oldapi}|${newapi}|g" web-app.properties
```

### properties upadte in .Js file

```
old_url=$(cat main.bundle.js | grep -Eo "(http|https)://[a-zA-Z0-9./?=_%:-]*" | grep Omnistore)
new_url="http://10.11.142.azure.com:9089/example-services/rest"
sed -i "s|${old_url}|${new_url}|g" main.bundle.js
```

### details about os logger user

```
uname -a
```

### Check logs for failed service symtemctl in linux

```
journalctl --no-pager -u serviceName
```

### kill running process on port

```
fuser -k port/tcp
```

### move file one folder to another with apttern matching

```
#!/bin/bash
SourceDirectory=/c/Users/sawan/Desktop/poc
DestinationDirectory=/c/Users/sawan/Desktop/adeo/
cd $SourceDirectory
find -iname '*Detexo*' -exec cp {} $DestinationDirectory \; 
```

### fileter docker images by word

```
docker images | grep -w app
```

### Font Issue in Linux

```
apt-get update; apt-get install -y fontconfig libfreetype6
```

### File Permission SSH configuration related

```
.ssh directory - 700
.pub file - 644
.id_rsa file- 600
authorized_key file- 600 
```

### replace string in multiple files

```
find ./ -type f -exec sed -i 's|redis.isPasswordEncrypted=false||g' {} \;
```

### extract value from json and store in file

```
cat deployment/workload-ext.json | jq ". | map(select(.name == \"$(BuildMS.NAME)\"))[]" > properties-ms.json 
echo "ms_name: $(BuildMS.NAME)" 
echo "properties-ms.json:" 
cat properties-ms.json 
```

### user details log file

```
cat /var/log/secure
```

### script for replace string URL with "string" in json properties file

```
export oldXRegisterID=$(grep "XRegisterId" XRegisterSet.json)
export newXRegisterID="\"XRegisterId\":\"${xid}\""
sed -i "s|${oldXRegisterID}|${newXRegisterID}|g" XRegisterSet.json
```

### Shell script operator annotations

##### A binary comparison operator compares two variables or quantities. Note that integer and string comparison use a different set of operators.

#### --integer comparison--

```
#is equal to
-eq
if [ "$a" -eq "$b" ]

#is not equal to
-ne
if [ "$a" -ne "$b" ]

#is greater than
-gt
if [ "$a" -gt "$b" ]

#is greater than or equal to
-ge
if [ "$a" -ge "$b" ]

#is less than
-lt
if [ "$a" -lt "$b" ]

#is less than or equal to
-le
if [ "$a" -le "$b" ]

#is less than (within double parentheses)
<
(("$a" < "$b"))

#is less than or equal to (within double parentheses)
<=
(("$a" <= "$b"))

#is greater than (within double parentheses)
>
(("$a" > "$b"))

#is greater than or equal to (within double parentheses)
>=
(("$a" >= "$b"))
```

#### --string comparison--

```
#is equal to
=
if [ "$a" = "$b" ]
#Caution    
#Note the whitespace framing the =.
if [ "$a"="$b" ] is not equivalent to the above.

#
==
if [ "$a" == "$b" ]
This is a synonym for =.
Note    
The == comparison operator behaves differently within a double-brackets test than within single brackets.
[[ $a == z* ]]   # True if $a starts with an "z" (pattern matching).
[[ $a == "z*" ]] # True if $a is equal to z* (literal matching).

[ $a == z* ]     # File globbing and word splitting take place.
[ "$a" == "z*" ] # True if $a is equal to z* (literal matching).

#is not equal to
!=
if [ "$a" != "$b" ]


#is less than, in ASCII alphabetical order
<
if [[ "$a" < "$b" ]]
if [ "$a" \< "$b" ]
Note that the "<" needs to be escaped within a [ ] construct.

#is greater than, in ASCII alphabetical order
>
if [[ "$a" > "$b" ]]
if [ "$a" \> "$b" ]
Note that the ">" needs to be escaped within a [ ] construct.

#string is null, that is, has zero length
-z
String=''   # Zero-length ("null") string variable.
if [ -z "$String" ]
then
  echo "\$String is null."
else
  echo "\$String is NOT null."
fi     # $String is null.

#string is not null.
-n
Caution    
The -n test requires that the string be quoted within the test brackets. Using an unquoted string with ! -z, or even just the unquoted string alone within test brackets (see Example 7-6) normally works, however, this is an unsafe practice. Always quote a tested string. [1]
```

### delete similar type of file

```
cd dir
find . -type f -iname \*.jar -delete
find . -type f -iname dockerimage.sh -delete
find . -type d -iname \completed -delete
```

### find and delete all folder with same name and their content

```
find . -path '*/ErrorFile/*' -delete   #delete content
find . -type d -iname \ErrorFile -delete  #delete folder
```

### Renaming similar type of extension files

```
#!/bin/bash
echo "Renaming Files.........."
for file in $(find . -name '*.properties-template')
do
  mv $file $(echo "$file" | sed -r 's|.properties-template|.properties|g')
done
```

### Error : execute "/bin/bash" resource temporarily unavailable in RHEL & no child process fork bumb

```
cd /etc/security/limits.d
vi 90-nproc.conf
-----------------------------------------------
*         soft     nproc        2050
root      soft     nproc       unlimited
-----------------------------------------------
```

### check sonarqube shell script for quality gate

```
QualityGate=$(curl -s http://localhost:9000/api/qualitygates/project_status?projectKey=com.example:omnistore-infra-build:infra-example)
result=$(echo $QualityGate | grep -o '"status":"[^"]*' | grep -o '[^"]*$'|head -1)

#!/bin/bash
if [ "result" == "OK" ]
then
        echo "abortPipeline: true"
else
        echo "abortPipeline: false"
fi
```

### check CPU usage seprate per CPU

```
Top-->press 1
```

### export varible by properties file

```
path ./filename.propertie
. ./build.properties
```

### run sh file from sourec command

```
source filename.sh
```

### diffrence between sh and source(.)

```
source (or . ) - runs inside current shell and changes its attribute/environment.

sh (or ./) - do fork and runs in a subshell and hence can't change attributes/environment.
```

### command >> /dev/null 2>&1 meaning?

> /dev/null - is a standard file that discards all you write to it, but reports that the write operation succeeded.
> 1 - is standard output 
> 2 - is standard error.
> 2>&1 redirects standard error to standard output. 
> &1 indicates file descriptor (standard output), otherwise (if you use just 1) you will redirect standard error to a file named 1. [any command] >>/dev/null 2>&1 redirects all standard error to standard output, and writes all of that to /dev/null.

### command to check recent command status code

```
echo $?
```

### stress test in ubuntu linux VM

```
sudo apt-get install stress/ yum install stress
stress --cpu 6(No of CPU)
```

### encrypty file with password

```
gpg -a --symmetric --cipher-algo AES256 sawan.txt
```

### decrypt the file

```
gpg -a --decrypt sawan.txt
```

### use multiple grep option by egrep

```
ps -ef|egrep -i "(tomcat|java)"
```

### to check uptime for server

```
uptime
```

### program to check version software installed or not

```
#!/bin/bash

#this will return descriptor value 0-1023 0=sucess , except 0 error code write in file /dev/null as descriptor value by 1>&2
vim --version 1>/dev/null 2>&1    

#check descriptor value for successfull result = 0
if [[ $? -eq 0 ]]
then
    echo "vim is already installed"
else
    echo "vim is not installed" 
fi
```

### find path oe env details from port no

```
pidnumber=$(lsof -t -i:port)
ps -ef | grep <pidnumber>
```

### delete all process with specific name by command

```
ps aux | grep chrome | awk ' { print $2 } ' | xargs kill -9
```

<mark>rpm cheat sheet</mark>

[Linux rpm command cheat sheet](http://www.cyberciti.biz/howto/question/linux/linux-rpm-cheat-sheet.php)

### add rpm repository in centos7

```
rpm -ivh http://repo.zabbix.com/zabbix/4.0/rhel/7/x86_64/zabbix-release-4.0-1.el7.noarch.rpm
```

### install software in centos/fedore/rhel

```
#Import the Microsoft repository key.
sudo rpm --import http://packages.microsoft.com/keys/microsoft.asc

#Create local azure-cli repository information.
echo -e "[azure-cli]
name=Azure CLI
baseurl=http://packages.microsoft.com/yumrepos/azure-cli
enabled=1
gpgcheck=1
gpgkey=http://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/azure-cli.repo

#install with or w/o gpgkey
yum install azure-cli --nogpgkey
```

<mark> encode decode password</mark>

https://www.base64encode.org/

104:sawanadmin@4<--->MTA0OlBvc2FkbWluQDQ=

### to delete directory recursively by specific name i.e '1.20.0-SNAPSHOTS'

```
find /tmp -type d -name '1.20.0-SNAPSHOTS' -prune -exec rm -rf {} +
```

<mark>linux command with their manuals</mark>

http://www.mediacollege.com/linux/command/linux-command.html
www.explainshell.com

### Nexus2 start

```
#expot java 8
export JAVA_HOME="/u0 1/106045/.sw/jdk1.8.0_112"
export PATH=$JAVA_HOME/bin:$PATH

#start nexus2
cd NEXUS_HOME/bin
sh nexus start
```

### Set Python Version default

    sudo update-alternatives --install /usr/bin/python(default python file for verion) python(language name) /usr/local/bin/python3.7(installed pyhton path) 1(priority)
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2 
    sudo update-alternatives --install /usr/bin/python python /usr/lib/python2.7 3
    sudo update-alternatives --config python

### remove sametype of directories in one command

```
error by terminal :
unable to execute /bin/rm: argument list too long
sudo find . -name "ng-*" -print0 | xargs -0 rm -rf
sudo find . -name "tomcat.*" -print0 | xargs -0 rm -rf
```

### This command shows the information about the users currently on the machine and their processes.

It is used to show who is logged on and what they are doing.

```
w
```

### remove everything except file/folder

```
rm -rf -v !("main.bundle.js|folder1")
```

### copy everything except few folder and files

```
rsync -avr --exclude='main.bundle.js|folder1' ../old-build/omnistore-bo/omnistore-bo-new/ .
```

### check command to file older than 6 month and size more than 1gb

```
find /path -mtime +180 -size +1G
```

### give folder name permission

```
chmod -Rf 770 */apache-tomcat-9.0.12
sudo chmod -x foldername
```

### check space used by directory

```
du -sch *
```

### for switch to root user

```
sudo su
```

### configure locales in linux-box

```
sudo dpkg-reconfigure locales
press <space-bar> for select locales time
```

### when /etc directory permission changed revert back in azure by Run Command option

```
sudo chown -R root:root /etc
sudo find /etc -type f -exec chmod 644 {} +
sudo find /etc -type d -exec chmod 755 {} +
sudo chmod 755 /etc/init.d/* /etc/rc.local /etc/network/* /etc/cron.*/*
sudo chmod 400 /etc/ssh/ssh*key
```

### check file permision in octal as well as letters

```
stat -c '%a %A' file/dierctory-name
```

### centos locale

```
localectl set-locale LANG=en_GB.utf8
```

### locale status

```
localectl status
```

### replace propertie file inside the jar

```
jar -uf jarname.jar application.properties
jar -uf <war_name>\WEB-INF\lib\  <jar_name>
```

### create user

```
useradd [options] username
useradd sawan
```

### create password for user

```
sudo -i
passwd <username>
passwd T1046592
```

### create group and add user to group

```
sudo groupadd <groupname>
sudo groupadd editorial
sudo usermod -a -G <groupname> <username>
sudo usermod -a -G editorial olivia
```

### add user to sudo access in centos

```
usermod -aG wheel <username>
usermod -aG wheel 106045
```

### change password never expire

```
chage -m 0 -M 99999 -I -1 -E -1 <username>
chage -m 0 -M 99999 -I -1 -E -1 T1046592
#-m 0 will set the minimum number of days between password change to 0
#-M 99999 will set the maximum number of days between password change to 99999
#-I -1 (number minus one) will set the “Password inactive” to never
#-E -1 (number minus one) will set “Account expires” to never
```

### to check the sudo access

```
sudo whoami
o/p for sudo acess:root
```

### scheduled task at linux by crontab by passing cron expression with task in crontab file.

```
usage:  crontab [-u user] file
        crontab [ -u user ] [ -i ] { -e | -l | -r }
        -e      (edit user's crontab)
        -l      (list user's crontab)
        -r      (delete user's crontab)
        -i      (prompt before deleting user's crontab)
```

### start/stop/restart cron service in rhel

```
service crond start/stop/restart
/etc/init.d/crond start/stop/restart
systemctl start/stop/restart crond.service
```

### which users are already a member of a group

```
grep <groupname> /etc/group
grep editorial /etc/group
```

### give user permission to acces the directory

```
setfacl -R -m u:<username>:rwx <directory-name>
setfacl -R -m u:hduser:rwx /data/omnistore/sawan-poc/order-microservice
```

### To check Tomcat running path

```
ps -ef | grep catalina/tomcat
```

### change password in linux

```
passwd
```

### delete swap file from VIM editor

```
find . -type f -name "*.sw[klmnop]" -delete
```

### You can also create multiple nested folders by adding the -p option

```
mkdir -p parents directory folder/inside folder directory name
```

### You can use the .. special path to indicate the parent folder

```
cd .. #back to the home folder
```

### You can also use absolute paths, which start from the root folder /

```
cd /path
```

### Whenever you feel lost in the filesystem, call the pwd command to know where you are

```
pwd
```

### we’ll use the more generic rm command which deletes files and folders, using the -rf options

```
rm -rf folder/directory
```

### delete multiple folders at once

```
rmdir folder1,folder2(dir or folder should be empty)
```

### List the names of the files in the current directory along with the permissions, date, time and size

```
ll
```

### List the names of the files in the current directory

```
ls
```

### List the names of the files in the current directory along with the permissions, date, time and size

```
ls -al /directory or path
```

### You can create an empty file using the touch command

```
touch filename
```

### You can copy a file using the cp command

```
cp file name another file
```

### Linux command for copying files and directories. The syntax is as follows

```
cp -avr /dir1 /dir2/
cp -avr /home/vivek/letters /usb/backup
```

### get privateip of vm

```
hostname -i
```

### delete same name directory from folder

```
find . -name apm -type d -print0|xargs -0 rm -r --
```

### In its simplest usage, cat prints a file’s content to the standard output

```
cat file
```

### using the output redirection operator > you can concatenate the content of multiple files into a new file

```
cat file1 file2 > file3
```

### Using >> you can append the content of multiple files into a new file, creating it if it does not exist

```
cat file1 file2 >> file3
```

### write content in file

```
cat >> file name(press enter) 
content(press ctrl+d)
```

### check the memory usage by Pid

```
pmap pidno
```

### run command interval

```
watch -n <sec in digit> <command>
watch -n 10 ls- l (every 10 second refresh result)
```

### find size of directory in linux

```
du -sh <directoryName>
du -sh /pilot-setup
```

### The find command can be used to find files or folders matching a particular search pattern. It searches recursively.

Find all the files under the current tree that have the .js extension and print the relative path of each file matching:

It’s important to use quotes around special characters like * to avoid the shell interpreting them.

```
find . -name '*.js'
```

### Find directories under the current tree matching the name “src”:

```
find . -type d -name src
```

### Use -type f to search only files, or -type l to only search symbolic links.

-name is case sensitive. use -iname to perform a case-insensitive search.

### You can search under multiple root trees

```
find folder1 folder2 -name filename.txt
```

### Find directories under the current tree matching the name “node_modules” or ‘public’

```
find . -type d -name node_modules -or -name public
```

### You can also exclude a path, using -not -path

```
find . -type d -name '*.md' -not -path 'node_modules/*'
```

### You can search files that have more than 100 characters (bytes) in them

```
find . -type f -size +100c
```

### Search files bigger than 100KB but smaller than 1MB

```
find . -type f -size +100k -size -1M
```

### Search files edited more than 3 days ago

```
find . -type f -mtime +3
```

### Search files edited in the last 24 hours

```
find . -type f -mtime -1
```

### delete all the files matching a search by adding the -delete option. This deletes all the files edited in the last 24 hours

```
find . -type f -mtime -1 -delete
```

### command on each result of the search. In this example we run cat to print the file content.

### notice the terminating \;. {} is filled with the file name at execution time

```
find . -type f -exec cat {} \;
```

### command to search file by specific word in file name

```
find <path> -maxdepth 1 -name "*<text>*" -print| sed 's|^./||'
find . -maxdepth 1 -name "*core*" -print| sed 's|^./||'
```

### The Linux ‘tar’ stands for tape archive, is used to create Archive and extract the Archive files

> #Options:
> -c : Creates Archive
> -x : Extract the archive
> -f : creates archive with given filename
> -t : displays or lists files in archived file
> -u : archives and adds to an existing archive file
> -v : Displays Verbose Information
> -A : Concatenates the archive files
> -z : zip, tells tar command that create tar file using gzip
> -j : filter archive tar file using tbzip
> -W : Verify a archive file
> -r : update or add file or directory in already existed .tar file

```
tar [options] [archive-file] [file or directory to be archived]
```

### This command creates a tar file called file.tar which is the Archive of all .c files in current directory

```
tar cvf file.tar *.c/dierctory-name
Output :
os2.c
os3.c
os4.c
```

### This command extracts files from Archives

```
tar xvf file.tar
Output :
os2.c
os3.c
os4.c
```

### "Top" command is used to show the Linux processes. It provides a dynamic real-time view of the running system

The Output coloums will be stands for mentioned below

```
PID: Shows task’s unique process id.
PR: Stands for priority of the task.
SHR: Represents the amount of shared memory used by a task.
VIRT: Total virtual memory used by the task.
USER: User name of owner of task.
%CPU: Represents the CPU usage.
TIME+: CPU Time, the same as ‘TIME’, but reflecting more granularity through hundredths of a second.
SHR: Represents the Shared Memory size (kb) used by a task.
NI: Represents a Nice Value of task. A Negative nice value implies higher priority, and positive Nice value means lower priority.
%MEM: Shows the Memory usage of task.
```

```
top
top -p pid
top -c|grep keyword&search
```

### Display Specific User Process

```
top -u username
```

### clear buffer/cache

```
sudo sysctl vm.drop_caches=1
sudo sysctl vm.drop_caches=2
```

### Clear PageCache only

```
echo 1 > /proc/sys/vm/drop_caches
```

### Clear dentries and inodes.

```
echo 2 > /proc/sys/vm/drop_caches
```

### Clear PageCache, dentries and inodes

```
echo 3 > /proc/sys/vm/drop_caches
```

### to check number of cpu

```
lscpu
```

### To check Ram size in Linux

```
free -h
```

### See Ram Memory status in % in linux

```
Memory_Status=$(free | awk '/Mem/{printf("Mem free: %.1f%"), $4/($2+.000000001)*100} /Mem/{printf(", Mem Used: %.1f%"), $3/($2+.000000001)*100} /buffers\/cache/{printf(", buffers: %.1f%"), $4/($3+$4)+.000000001*100} /Swap/{printf(", swap: %.1f%"), $4/($2+.000000001)*100}';)
echo $Memory_status
```

### This will report the percentage of memory in use

```
free | grep Mem | awk '{print $3/$2 * 100.0}'
```

### This will report the percentage of memory that's free

```
free | grep Mem | awk '{print $4/$2 * 100.0}'
```

### This will report the percentage of memory in use in details

```
Memory_Used=$(free | awk '/Mem/{printf("Mem used: %.1f%"), $3/($2+.000000001)*100} /buffers\/cache/{printf(", buffers: %.1f%"), $4/($3+$4)+.000000001*100} /Swap/{printf(", swap: %.1f%"), $3/($2+.000000001)*100}';)
echo $Memory_Used
```

### This will report the percentage of memory in free in details

```
Memory_Free=$(free | awk '/Mem/{printf("Mem free: %.1f%"), $4/($2+.000000001)*100} /buffers\/cache/{printf(", buffers: %.1f%"), $4/($3+$4)+.000000001*100} /Swap/{printf(", swap: %.1f%"), $4/($2+.000000001)*100}';)
echo $Memory_Free
```

### to check HDD size in linux

```
df -T -H
df -H | grep -vE '^Filesystem|tmpfs|cdrom'
```

### Next filter out filesystem and find out the percentage of space

```
df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }'
```

### How to Copy All Files and Folders from One Location to Another in Linux Using “wildcard (*)”

```
cp -R /home/user1/* /home/user2/
```

### This command will delete all files older than 30 days in system /opt/backup directory.

```
find /opt/backup -type f -mtime +30 -exec rm -f {} \;
```

### Delete Files Older Than 30 Days with .log Extension

### If you want to delete only specified extension files, you can use the following command

```
find /var/log -name "*.log" -type f -mtime +30 -exec rm -f {} \;
```

### This command will delete folder older than x days

```
find /tmp/* -mtime +x -exec rm -rf {} \;
```

### Next filter out filesystem and find out the percentage of space

```
df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }'
```

### Check port no up/down in terminal

```
lsof -i:port no.
```

### to check port used by services

```
lsof -i -P -n | grep LISTEN
```

---

### VMSTAT COMMAND

- vmstat as a command with no parameters, it will show you a set of values. 
- These values are the averages for each of the statistics since your computer was last rebooted.

> vmstat -[option] delay count
> options:
> delay- The delay value is provided in seconds to regular upadted in interval
> count-The count value tells vmstat how many updates to perform before it exits 
> -S M -The memory and swap statistics are now shown in megabytes
> -f   -displays the number of forks since the computer was booted up.shows the number of tasks that have been launched
> -D   -quick display of summary statistics for your disk activity
> -t   -appends timestamp to each output line 
> -a   -It displays active and inactive memory of the system running.
> -n   -It is used to display header only once rather than periodically

```
vmstat -n 10 400 > vmstat_POS_19Aug_linux.txt &
```

### Command ouput section:

- Procs
    r: The number of runnable processes (running or waiting for run time).
    b: The number of processes in uninterruptible sleep.

- Memory
    swpd: the amount of virtual memory used.
    free: the amount of idle memory.
    buff: the amount of memory used as buffers.
    cache: the amount of memory used as cache.
    inact: the amount of inactive memory.  (-a option)
    active: the amount of active memory.  (-a option)

- Swap
    si: Amount of memory swapped in from disk (/s).
    so: Amount of memory swapped to disk (/s).

- IO
    bi: Blocks received from a block device (blocks/s).
    bo: Blocks sent to a block device (blocks/s).

- System
    in: The number of interrupts per second, including the clock.
    cs: The number of context switches per second.

- CPU
    These are percentages of total CPU time.
    us: Time spent running non-kernel code.  (user time, including nice time)
    sy: Time spent running kernel code.  (system time)
    id: Time spent idle.  Prior to Linux 2.5.41, this includes IO-wait time.
    wa: Time spent waiting for IO.  Prior to Linux 2.5.41, included in idle.
    st: Time stolen from a virtual machine.  Prior to Linux 2.6.11, unknown.

---

### change timezone in centos7

- to check current timezone
  
  **timedatectl**

- The system timezone is configured by symlinking /etc/localtime to a 
  binary timezone identifier in the /usr/share/zoneinfo directory. 
  So, another option to check the timezone is to show the path the symlink points to using the ls command :
  **ls -l /etc/localtime**

- To list all available time zones
  **timedatectl list-timezones**

- set the timezone from above list
  **sudo timedatectl set-timezone your_time_zone
  sudo timedatectl set-timezone UTC**

### set timezone in tomcat server

```
CATALINA_OPTS="-Djava.awt.headless=true -Xms1024 -Xmx4096M -server -Duser.timezone=Europe/Budapest"
```

---

### password less aunthentication using ssh in linux server

- login to source server

- generate SSH keys in source server using these commands
  **ssh-keygen -t rsa**
  
  ![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-09-20-07-33-image.png)

- **cd /root/.ssh/**

- **ls**

- go to id_rsa.pub file and copy the whole content paste into target server with commands
  **ssh-copy-id -i /home/omniops/.ssh/id_rsa.pub TargetServerUser@TargetServerURL**

- enter the target server password once

- to check login in target server by command it will login automatically with authorization key
  **ssh TargetServerUser@TargetServerURL**

### To find out where disk space is being used:

```
GNote which directories are using a lot of disk space.
cd into one of the big directories.
Run ls -l to see which files are using a lot of space. Delete any you don’t need.
Repeat steps 2 to 5.et to the root of your machine by running cd /
Run sudo du -h --max-depth=
```

### properties changes by command through script in application.properties file in Java Spring boot application

```
#!/bin/bash
#mysql service start
systemctl start/status/stop mysqld.service

#varible defination
dbuser=sawan
msport=0000
dbpassword=Example@34
dbhost=10.11.135.65
dbport=5432
redishost=10.11.142.226
redisport=8200
redisdb=0
redispassword=Example@3407

#new properties key value
thekey=cache.local.config-file
newvalue=\${OMNISTORE_HOME}/etc/properties/cache-config/saleReturn-ehcache.xml

#add new property add end of the file
printf '$thekey=$newvalue\n' >> application.properties

#replacing properties
sed -i "s|^[#]*\s*server.port=.*|server.port=$msport|" application.properties
sed -i "s|^[#]*\s*hibernate.hikari.pds.db.url=.*|hibernate.hikari.pds.db.url=jdbc:mysql://$dbhost:$dbport/omnistore_salesreturn?useLocalSessionState=true\&useLocalTransactionState=true|" application.properties
sed -i "s|^[#]*\s*hibernate.hikari.pds.user.name=.*|hibernate.hikari.pds.user.name=$dbuser|" application.properties
sed -i "s|^[#]*\s*hibernate.hikari.pds.passwd=.*|hibernate.hikari.pds.passwd=$dbpassword|" application.properties
sed -i "s|^[#]*\s*redis.host=.*|redis.host=$redishost|" application.properties
sed -i "s|^[#]*\s*redis.port=.*|redis.port=$redisport|" application.properties
sed -i "s|^[#]*\s*redis.database=.*|redis.database=$redisdb|" application.properties
sed -i "s|^[#]*\s*redis.password=.*|redis.password=$redispassword|" application.properties
sed -i "s|^[#]*\s*redis.isPasswordEnabled=.*|redis.isPasswordEnabled=true|" application.properties
sed -i "s|^[#]*\s*item.base.url=.*|item.base.url=$redishost:8120/os-item|" application.properties
sed -i 's/#hibernate.hikari.pds.ds.class.name=com.mysql.cj.jdbc.MysqlDataSource/hibernate.hikari.pds.ds.class.name=com.mysql.cj.jdbc.MysqlDataSource/g' application.properties
sed -i 's/hibernate.hikari.pds.ds.class.name=org.postgresql.ds.PGSimpleDataSource/#hibernate.hikari.pds.ds.class.name=org.postgresql.ds.PGSimpleDataSource/g' application.properties
```

---

### mongodb installation and configuration

```
sudo apt-get install mongodb
sudo service mongodb start
mongod --auth --port 27017 --dbpath /var/lib/mongodb 

configuration file:
   ip_bind=0.0.0.0
   port=27017
   auth=true


mongo --host  192.168.0.4 --port 27017  --authenticationDatabase "databasename" -u "user" -p "password"

mongo --host  192.168.0.4 --port 27017  --authenticationDatabase "databasename" --username --password
```

### connection by connection-string

```
mongo "mongodb://192.168.0.4:28015/?authSource=admin"
```

### linux color code for print statement output in colour

```
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color 

echo -e "${YELLOW}\nyou opted for ${NC}"
             |___________
                         |
o/p = you opted for(in yellow color)
```

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
