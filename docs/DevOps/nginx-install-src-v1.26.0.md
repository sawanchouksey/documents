# Install Nginx v1.26.0 from Source Package in Amazon Linux 2023 EC2 Instance and Install ngx_http_headers_more_filter_module for prevent our application to expose our server as Nginx or Its Version as well on browser Internet.

### Pre-requisite

1. **EC2 Amazon Linux 2023 Instance**

2. **Internet access**

3. **Linux Commands basics**

### Introduction

`Nginx` is an `open-source web server and reverse proxy server` known for its `high performance, stability, simple configuration, and low resource consumption`. It is widely used for serving static and dynamic content, load balancing, caching, and as a reverse proxy for various web applications.

Here are some key benefits of Nginx:

1. **High Performance**: Nginx can handle a large number of concurrent connections, making it suitable for high-traffic websites and applications.
2. **Efficient Resource Utilization**: Nginx has an event-driven architecture and uses an asynchronous, non-threaded approach, which allows it to consume fewer system resources compared to traditional web servers.
3. **Load Balancing**: Nginx can distribute incoming traffic across multiple application servers, improving availability and scalability.
4. **Reverse Proxy**: Nginx can act as a reverse proxy, forwarding client requests to various backend servers based on configured rules.
5. **Caching**: Nginx provides efficient caching mechanisms for static content, reducing the load on backend servers and improving response times.
6. **SSL/TLS Offloading**: Nginx can handle SSL/TLS termination and offloading, which can improve performance by reducing the computational overhead on backend servers.

### Benefits of Installing `Nginx from Src Package` instead of default package manager like `yum,rpm,apt,dnf` etc.

- **Flexibility and Customization**: When you compile Nginx from source, you have the ability to customize the build options and enable or disable specific modules or features based on your requirements. This level of granular control is not typically available with pre-compiled packages.
- **Latest Version and Features**: Package managers often distribute older versions of Nginx, which may lack the latest features or security updates. By installing from the source, you can ensure that you have the most recent version with the latest improvements and bug fixes.
- **Optimization**: Compiling Nginx from source allows you to optimize the build for your specific system architecture and hardware. This can result in better performance and resource utilization compared to pre-compiled binaries, which are often built with generic settings.
- **Custom Modules and Patches**: If you need to include custom modules or apply specific patches to Nginx, compiling from source makes it easier to integrate these modifications into the build process.
- **Dependency Management**: When using package managers, you may encounter dependency conflicts or version mismatches with other installed software. Building from source gives you more control over dependencies and can help avoid compatibility issues.

### Installation Steps

1. Open Linux Terminal of ec2 instnace and switch to `root` user.
   
   ```
   sudo su -
   ```

2. We need to install some pre-built packages to compile nginx src code i.e. `C compiler,make,pcre,openssl etc`.
   
   ```
   yum groupinstall 'Development Tools' -y
   yum install yum install libxml2-devel libxslt-devel pcre pcre-devel zlib zlib-devel gzip openssl openssl-devel -y
   ```

3. Check all packages installed and their information
   
   ```
   yum grouplist Dev* installed
   yum groupinfo "Development Tools"
   ```

4. Clone the latest or specific version `nginx src code` from nginx repository. We are `using v1.26.0 nginx version` for installation.
   
   ```
   wget 'http://nginx.org/download/nginx-1.26.0.tar.gz'
   ```

5. Lets untar the nginx tar `nginx-1.26.0.tar.gz` we downloaded in previous step. and move into the extracted directory.
   
   ```
   tar -xzvf nginx-1.26.0.tar.gz
   cd nginx-1.26.0/
   ```

6. We will configure one 3rd party module `headers-more-nginx-module` as well for customization. and which will prevent our `nginx server details` exposed in internet. 

7. lets download the src code of `headers-more-nginx-module` from github repository.
   
   ```
   cd /root
   git clone https://github.com/openresty/headers-more-nginx-module.git
   ```

8. Now lets configure our `nginx server` with our requirements and Configure the build environment .
   
   ```
   cd nginx-1.26.0/
   ./configure --prefix=/etc/nginx --sbin-path=/usr/bin/nginx --conf-path=/etc/nginx/nginx.conf --modules-path=/etc/nginx/modules --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --with-pcre --pid-path=/var/run/nginx.pid --with-http_image_filter_module=dynamic --with-http_perl_module=dynamic --with-http_xslt_module=dynamic --user=nginx --group=nginx --with-compat --with-file-aio --with-stream --with-threads --with-http_sub_module --with-http_secure_link_module --with-http_auth_request_module --with-http_addition_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_realip_module --with-cpp_test_module --with-http_ssl_module --add-dynamic-module=/root/headers-more-nginx-module
   ```

9. lets compile the source code and build the executable binary or library files with the help of `make` command. The make command is typically run after configuring the build environment and before installing the compiled software.
   
   ```
   make
   ```

10. lets use `make install`  command to copy the compiled binary or library files to the appropriate system directories, making the software accessible system-wide.
    
    ```
    make install
    ```

11. lets check the `Nginx version` and all information about executed command after successfully completion.
    
    ```
    nginx -V
    nginx -V output
    ```

12. Now check the configured directory for all `Nginx related files and modules`
    
    ```
    cd /etc/nginx
    ll -lart
    ```

13. Lets check the all `dynamic modules compiled binaries` exist in path or not.
    
    ```
    cd /etc/nginx/modules
    ls -lart
    ```
    
    ![diagram](https://sawanchouksey.github.io/documents/blob/main/docs/DevOps/dynamic-installed-module.png?raw=true)

14. lets configure the `nginx` as systemd service so we can controll `nginx` with `systemctl` commands in system.

15. create the `nginx.service` file with following code.
    
    ```
    - open or create file
    vi /lib/systemd/system/nginx.service
    
    - copy the below content in the file
    [Unit]
    Description=The NGINX HTTP and reverse proxy server
    After=syslog.target network-online.target remote-fs.target nss-lookup.target
    Wants=network-online.target
    
    [Service]
    Type=forking
    PIDFile=/var/run/nginx.pid
    ExecStartPre=/usr/sbin/nginx -t
    ExecStart=/usr/sbin/nginx
    ExecReload=/usr/sbin/nginx -s reload
    ExecStop=/bin/kill -s QUIT $MAINPID
    PrivateTmp=true
    
    [Install]
    WantedBy=multi-user.target
    
    - save the file
    :wq
    ```

16. As we configured `nginx` user for managing `nginx service` lets create user,group `nginx`
    
    ```
    groupadd nginx
    adduser nginx --system --no-create-home -g nginx
    ```

17. edit `nginx.conf` file for updating user for `nginx service`
    
    ```
    - open file
    vi /etc/nginx/nginx.conf
    
    - update the configuration in file on top
    user  nginx;
    
    - save the file
    :wq
    ```

18. start the `nginx.service` and check status.
    
    ```
    systemctl start nginx
    systemctl status nginx
    ```

19. if you face `problem or error` while starting the service and status is `failed`. Use below commans to check logs
    
    ```
    journalctl -xeu nginx.service
    ```

20. If everything works fine as expected then simply browser the URL with `default port 80` or `configured port <port_no>` in browser or with the help of `curl request` as well
    ![diagram](https://sawanchouksey.github.io/documents/blob/main/docs/DevOps/nginx-browser.png?raw=true)

21. Now lets check our `nginx server details` coming in header or not with curl request.
    ![diagram](https://sawanchouksey.github.io/documents/blob/main/docs/DevOps/nginx-server-expose.png?raw=true)

22. As we noticed by default its exposing our `nginx server details` in internet which will help `hackers to find vulenrablities and exploit our server or application` deployed in nginx as well.

23. Lets configure our `ngx_http_headers_more_filter_module` and some parameters to prevent our nginx server details from exposing in internet.
    
    ```
       - stop nginx server
       systemctl stop nginx
       
       - open nginx.conf file
       vi /etc/nginx/nginx.conf
       
       - add `load_module` parameter for load dynamic modules
       load_module /etc/nginx/modules/ngx_http_headers_more_filter_module.so;
       
       - we can add `more_clear_header` parameter in `http` directive for disable `server details` exposing in internet.
       http{
        more_clear_headers Server;
       }
       
       - or also we can set custom server name for our server for internet with `more_set_header`.
       http{
        more_set_headers "Server: Sawan";
       }
       
       - save file
       :wq
       
       - start nginx service
       systemctl start nginx
    ```

24. Lets again check now our server details will not be exposed and visible in internet
    ![diagram](https://sawanchouksey.github.io/documents/blob/main/docs/DevOps/disable-nginx-server-expose.png?raw=true)

25. Enable `Nginx Service` on autostart during reboot server
    
    ```
    systemctl enable nginx
    ```

### Now our installation complete . Please fine the `nginx.conf` for sample

```
 user  nginx;
 worker_processes  1;

 load_module /usr/lib64/nginx/modules/ngx_http_headers_more_filter_module.so;
 load_module /usr/lib64/nginx/modules/ngx_http_xslt_filter_module.so;

 #error_log  logs/error.log;
 #error_log  logs/error.log  notice;
 #error_log  logs/error.log  info;

 #pid        logs/nginx.pid;

 events {
     worker_connections  1024;
 }

 http {    
     include       mime.types;
     default_type  application/octet-stream;

     #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
     #                  '$status $body_bytes_sent "$http_referer" '
     #                  '"$http_user_agent" "$http_x_forwarded_for"';

     #access_log  logs/access.log  main;

     sendfile        on;
     #tcp_nopush     on;

     #keepalive_timeout  0;
     keepalive_timeout  65;

     #gzip  on;
     more_set_headers "Server: Sawan";
     more_clear_headers Server;
     server {
         listen       9090;
         server_name  localhost;

         #charset koi8-r;

         #access_log  logs/host.access.log  main;

         location / {
             root   html;
             index  index.html index.htm;
         }

         #error_page  404              /404.html;

         # redirect server error pages to the static page /50x.html
         #
         error_page   500 502 503 504  /50x.html;
         location = /50x.html {
             root   html;
         }
     }    
 }
```

### References

https://nginx.org/en/docs/configure.html

https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/

https://www.nginx.com/resources/wiki/start/topics/examples/systemd/

https://thoughtbot.com/blog/the-magic-behind-configure-make-make-install

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html

https://docs.nginx.com/nginx-management-suite/support/troubleshooting/

https://www.tecmint.com/install-nginx-from-source/

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚