# How to Send and Ship Nginx logs running in EC2 instance to AWS CloudWatch

### Prerequisites:

- Running AWS EC2 Amazon Linux 2 instance.
- Nginx Software Install in AWS EC2 Amazon Linux 2 instance 
- AWS Credentials key. 

### Purpose/Use-Case

- The primary purposes for shipping Nginx logs to CloudWatch in this context are:
  
  1. To maintain a comprehensive audit trail for security and compliance purposes.
  2. To enable proactive monitoring and rapid response to potential security threats.
  3. To facilitate compliance with various regulatory standards that require log management.
  4. To improve overall security posture through advanced log analysis and correlation.

### Benefits

- Shipping Nginx server logs to Amazon CloudWatch for security audit purposes and compliance offers several benefits:
  
  1. **Centralized log management**:
     CloudWatch provides a centralized location to store and analyze logs from multiple Nginx servers, making it easier to monitor and manage your infrastructure.
  
  2. **Real-time monitoring**:
     CloudWatch enables real-time monitoring of log data, allowing you to quickly detect and respond to security incidents or unusual activities.
  
  3. **Enhanced security analysis**:
     By aggregating logs in CloudWatch, you can perform more comprehensive security analysis, identify patterns, and detect potential threats across your Nginx servers.
  
  4. **Compliance requirements**:
     Many compliance standards (e.g., HIPAA, PCI DSS) require log retention and analysis. CloudWatch helps meet these requirements by providing secure storage and access controls.
  
  5. **Automated alerting**:
     Set up CloudWatch Alarms to automatically notify you of suspicious activities or potential security breaches based on log data.
  
  6. **Long-term log retention**:
     CloudWatch allows you to store logs for extended periods, which is often necessary for compliance and forensic analysis.
  
  7. **Integration with other AWS services**:
     CloudWatch integrates with other AWS services, enabling advanced log analysis, visualization, and automated responses to security events.
  
  8. **Scalability**:
     CloudWatch can handle log data from multiple sources and scale as your infrastructure grows.
  
  9. **Access control and encryption**:
     CloudWatch provides secure access controls and encryption options to protect sensitive log data.
  
  10. **Cost-effective storage**:
      Compared to maintaining on-premises log storage solutions, CloudWatch can be a more cost-effective option for long-term log retention.

### Quick Steps:

- Attaching an IAM role to instance. 
- Install CloudWatch Logs Agent. 
- Configure CloudWatch Logs Agent. 

### STEPS To PERFORM:

1. Create Role with IAM Policy having required permissions for Instance Profile role. 

2. Go to IAM role which is attached to Instance. 

3. Attach CloudWatchAgentServerPolicy  to your Instance role.
    ![CloudWatchAgentServerPolicy](https://github.com/sawan22071995/notes/blob/main/docs/Cloud/CloudWatchAgentServerPolicy.png?raw=true)

4. Login to the EC2 Instance and install awslogs package
   
   ```
   sudo yum install awslogs
   ```

5. Check status of awslogs service using command
   
   ```
   systemctl status awslogsd.service
   ```

6. If the service is not enabled you can enable it using command
   
   ```
   systemctl enable awslogsd.service
   ```

7. Go to /etc/awslogs and make changes to awscli.conf file, change region were your EC2 Instance is located eg: eu-central-1.
   
   ```
   sudo cd /etc/ 
   vim awscli.conf
   ```
   
    ![AwsCliConf](https://github.com/sawan22071995/notes/blob/main/docs/Cloud/awscli.png?raw=true)

8. Then in the same directory make a change to awslogs.conf file. Add the below lines, make changes as per your need
   
   ```
   vi awslogs.conf
   [/var/log/nginx/access.log] 
   datetime_format = %b %d %H:%M:%S 
   file = /var/log/nginx/access.log 
   buffer_duration = 5000 
   log_stream_name = nginx-access.log 
   initial_position = start_of_file 
   log_group_name = Nginx-logs
   ```
   
    ![AwsLogsConf](https://github.com/sawan22071995/notes/blob/main/docs/Cloud/awslogsconf.png?raw=true)

9. After these changes you have to restart awslogsd.service by using command
   
   ```
   systemctl restart awslogsd.service
   ```

10. Then go to your AWS management console > CloudWatch. When you will see the log groups. You’ll find the Nginx-logs log group automatically created and inside it log_stream will be created.
    
    - Log group
        ![AwsCloudWatchLogGroup](https://github.com/sawan22071995/notes/blob/main/docs/Cloud/loggroup.png?raw=true)
    - Log Stream
        ![AwsCloudWatchLogStream](https://github.com/sawan22071995/notes/blob/main/docs/Cloud/logstream.png?raw=true)


### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚