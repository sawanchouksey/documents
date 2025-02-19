# Windows Commands List
### Create Alias in Windows OS for terminal
- Create a folder called C:\Aliases
- Add C:\Aliases to your path (so any files in it will be found every time)
- Create a .bat file in C:\Aliases for each of the aliases you want
- For instance, I have a file called k.bat with the following in it:
  ```
  @echo off
  echo.
  kubectl %*
  ```
- add `PATH` Variable for Your Account as `C:\Aliasas` 
### For hostname

```
open command prompt ->   type hostname ->   enter (My-PC-01......)
```

### For serialnumber

```
open command prompt ->  type  wmic bios get serialnumber -> enter
```

### For windows version

```
open run command (windows key + R )   -> type winver -> enter
```

### Java OutOfMemeory Heap Size Issue in tomcat setenv.bat in TOMCAT_HOME/bin folder

```
set "JAVA_OPTS"="%JAVA_OPTS% -Xms4000M -Xmx8000M"
Xms is the initial (start) memory pool
Xmx is the maximum memory pool
Xss is the thread stack size
```

### APM agent in Windows Tomcat server setenv.bat

```
set "JAVA_OPTS"="%JAVA_OPTS% -javaagent:elastic-apm-agent-1.26.0.jar"
set "JAVA_OPTS"="%JAVA_OPTS% -Delastic.apm.service_name=omnistore-pos-services"
set "JAVA_OPTS"="%JAVA_OPTS% -Delastic.apm.application_packages=com.tcs.retail.store"
set "JAVA_OPTS"="JAVA_OPTS% -Delastic.apm.server_url=http://apm-server-apm-server:8200"
set "JAVA_OPTS"="$JAVA_OPTS -Xms1500M -Xmx3000M -XX:+UseParallelGC -XX:+DisableExplicitGC -XX:ParallelGCThreads=4"
```

### jconsole for checking JVM in Windows UI tool with JDK

```
open command prompt and run below command
jconsole
```

### Startup folder open in Windows

```
1. Open Run 
   win + R
2. Type:
   shell:startup
```

### shortcuts of windows

```
open the application available 1...n application in taskbar 
> window_key + 1..n 

open clipboard 
> window_key + v

take screenshot and copy
>window_key + shift + s

switch to desktop directly from any window
>window_key + d

>open emoji keyboard
window_key + .
```

### import certificate in jdk from export website

error - PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target

```
#password - changeit
%JAVA_HOME%\bin\keytool -import -alias spring -keystore  "%JAVA_HOME%\lib\security\cacerts" -file "%USER_HOME%\springsource.cer"
```

### read the data from file and update at the end of another file

```
FOR /F "eol=; tokens=2,2 delims==" %%i IN ('findstr /i "FDRAPC_MID" %USER_HOME%Desktop\azure-tcs\pga-poc\fipayeps_def.cfg') DO SET var1=%%i
echo %var1%

type %USER_HOME%\payment.properties | findstr /v fdrapc_mid | findstr /v } > %USER_HOME%\payment-new.properties

echo "fdrapc_mid":%var1% >> payment-new.properties
echo } >> payment-new.properties 


move "%USER_HOME%\payment-new.properties" "%USER_HOME%\payment.properties"
```

### Install docker in windows server with hyper-V

```
Virtual machine name: Server2016Azure.
Image: Windows Server 2016 Datacenter (Windows Server 2016 is preferred because supports more Hyper-V features than Windows Server 2012 R2 Datacenter).
https://computingforgeeks.com/how-to-run-docker-containers-on-windows-server-2019/
Install-Module -Name DockerMsftProvider -Repository PSGallery -Force
Install-Package -Name docker -ProviderName DockerMsftProvider
Restart-Computer -Force
Get-Package -Name Docker -ProviderName DockerMsftProvider
docker version
Install-Package -Name Docker -ProviderName DockerMsftProvider -Update -Force
Start-Service Docker
-----------------------------------------------------------------------------
DockerInstall.ps1
-----------------------------------------------------------------------------
$rebootNeeded = $false
if (-not (Get-WindowsFeature Containers).Installed) {
  $rebootNeeded = $rebootNeeded -or (Install-WindowsFeature -Name Containers).RestartNeeded
}

if ((Get-WindowsFeature Windows-Defender).Installed) {
  $rebootNeeded = $rebootNeeded -or (Uninstall-WindowsFeature Windows-Defender).RestartNeeded
}

if ($rebootNeeded) { throw "Reboot then rerun to complete docker installation" }

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
Install-Module -Name DockerMsftProvider -Repository PSGallery -Force
Install-Package -Name docker -ProviderName DockerMsftProvider -Force
Start-Service docker  
docker --version
```

### Encode decode password

https://www.base64encode.org/

### SSL setup in tomcat

[How to Implement SSL in Apache Tomcat?](http://geekflare.com/tomcat-ssl-guide/)

## to check ssl certificate garde/SSL/TLS Vulnerability Test online tools

http://www.ssllabs.com/ssltest/

### To long path enable

[How To Fix &#8216;Filename Is Too Long&#8217; Issue In Windows](http://helpdeskgeek.com/how-to/how-to-fix-filename-is-too-long-issue-in-windows/)

### Copy new.jar file into new.war

```
jar -xf os-coredata.war|copy sawan-1.0.0-snapshot.jar WEB-INF\lib\|jar -cf os-coredata.war WEB-INF META-INF
```

### create zip file from jar command with manifest file

```
jar -cvf file.zip sawan sawantxt.txt
```

### create zip file from jar command without manifest file

```
jar -cvMf file.zip sawan sawantxt.txt
```

### delete all files and folder from the directory in windows

```
del /q %USER_HOME%Desktop\warjarpoc\delete\*.*
for /d %i in (%USER_HOME%Desktop\warjarpoc\delete\*.*) do @rmdir /s /q "%i"
```

### kill service with pid in windows

```
pid=tasklist /v /fo csv | findstr /i "8150"
taskkill /pid <SERVICE_PID> /f
```

### find port is running

```
netstat -ano | findStr "8007"
```

### run java process in background

```
javaw -jar Omnichannel-microservices-0.0.1-SNAPSHOT.jar --spring.config.location=application.properties
```

### to know about the process running in windows

```
netstat -a -n -o | find "5432"
```

### allowed incoming port in windows defender  firewall

```
1.go control panel
2.go to control-->system and security
3.go to control-->system and security-->windows defender firewall
3.click on "Advanced Setting" option in left side corner
4.click on add "New Rule" with below field configuration
    Rule Type                : Port 
    TCP or UDP               : TCP
    Specific local ports     : 5432
    Action                   : Allow the connection
    When does this rule apply: Domain, Private and Public (all three checked)
    Name                     : "PostgreSQL Incoming"
5.click "OK" 
6.Finished.
```

### Set JAVA_HOME & MAVEN HOME

```
set JAVA_HOME=%USER_HOME%\jdk-17.0.4
set PATH=%JAVA_HOME%\bin%PATH%
set M2_HOME=C:\software\apache-maven-3.6.3-bin\apache-maven-3.6.3
set PATH=%M2_HOME%\bin%PATH%
```

### snipping tools shortcuts

```
win_key + shift_key + S
```

### java.net.BindException: Address already in use:connect error message is throwing

http://www.baselogic.com/2011/11/23/solved-java-net-bindexception-address-use-connect-issue-windows/

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
