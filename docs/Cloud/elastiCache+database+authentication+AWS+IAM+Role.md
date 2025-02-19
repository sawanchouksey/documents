# Authentication ElastiCache Redis Cluster with IAM role in AWS Cloud

### Pre-Requisite:

1. AWS Cli | Aws Console

2. elasticache redis cluster

3. ec2 instnace with below tools
   
   - Java 
   
   - Maven
   
   - git
   
   - redis-cli (optional)

### IAM Authentication and its benfits over password based authentication

IAM authentication in AWS refers to the use of AWS Identity and Access Management (IAM) for controlling access to AWS services and resources. IAM provides fine-grained access control to AWS resources, allowing you to define who can access which resources in your AWS environment.

When it comes to Amazon ElastiCache for Redis, IAM authentication provides several benefits over traditional password-based authentication:

1. **Enhanced Security**: IAM authentication leverages AWS’s robust security infrastructure. It eliminates the need to manage Redis passwords, which can be a security risk if not handled properly. By using IAM, you can take advantage of AWS’s existing security features like multi-factor authentication (MFA), which adds an additional layer of security.

2. **Fine-Grained Access Control**: IAM allows for more precise control over who can access your ElastiCache Redis clusters. You can define policies that specify who can perform which actions on a particular cluster. This level of control is not possible with basic password authentication.

3. **Simplified Management**: With IAM, you can centrally manage permissions for ElastiCache and other AWS services. This centralized approach simplifies the management of access permissions, as opposed to maintaining separate password-based systems for different services.

4. **Audit and Compliance**: IAM integrates with AWS CloudTrail, which provides logs of all access and actions taken by IAM users and roles. This is crucial for compliance and audit purposes, as it allows you to track who accessed your ElastiCache Redis clusters and what actions they performed.

5. **Integration with Other AWS Services**: IAM is a core component of AWS, and its integration with other AWS services means that you can create a more cohesive and secure environment. For example, you can use IAM roles to securely allow applications running on EC2 instances to access ElastiCache Redis clusters without needing to hardcode credentials.

6. **Scalability and Flexibility**: IAM is designed to work at scale, accommodating large numbers of users and complex policies. This scalability is important in dynamic environments where access requirements can change frequently.

### Steps to follow to complete setup and Intgeration

1. Create `elasticache user` iam enbaled in elasticache redis cluster from AWS console. 
   
   ```
   aws elasticache create-user \
     --user-name iam-user-01 \
     --user-id iam-user-01 \
     --authentication-mode Type=iam \
     --engine redis \
     --access-string "on ~* +@all"
   ```

2. Create a `elasticache user group` and attach the user in elastiCache redis cluster in AWS.
   
   ```
   aws elasticache create-user-group \
    --user-group-id iam-user-group-01 \
    --engine redis \
    --user-ids default iam-user-01
   ```

3. Create `elasticache redis cluster` with below configuration.
   
   ```
   aws elasticache create-cache-cluster \
   --cache-cluster-id my-cluster \
   --cache-node-type cache.r4.large \
   --engine redis \
   --num-cache-nodes 1 \
   --cache-parameter-group default.redis6.x
   
   aws elasticache modify-cache-cluster \
   --cache-cluster-id my-cluster \
   --security-group-ids my-user-group
   ```

4. Create `IAM policy` with respect to `elasticache redis cluster` configuration with below permissions.Save the policy to a file named *policy.json*.
   
   ```
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "VisualEditor0",
               "Effect": "Allow",
               "Action": "elasticache:Connect",
               "Resource": [
                   "arn:aws:elasticache:*:123456789123:user:*",
                   "arn:aws:elasticache:*:123456789123:serverlesscache:*",
                   "arn:aws:elasticache:*:123456789123:replicationgroup:*"
               ]
           }
       ]
   }
   ```

5. Create a `IAM Role` should have `IAM policy`  which we created in previous step to connect to cluster. Refer the sample IAM policy attached to the role. *Note: I have added wildcard for most of the Resources, You can limit to the users and replication groups.*
   
   ```
   aws iam create-role \
   --role-name "elasticache-iam-auth-app" \
   --assume-role-policy-document file://policy.json
   ```

6. Create `ec2 instance` and attached `IAM Role` which created in previous step.
   
   ```
   aws iam create-instance-profile \
   --instance-profile-name MyEC2InstanceProfile
   
   aws iam add-role-to-instance-profile \
   --instance-profile-name MyEC2InstanceProfile \
   --role-name elasticache-iam-auth-app
   
   aws ec2 run-instances \
    --image-id ami-id \
    --count 1 \
    --instance-type instance-type \
    --iam-instance-profile Name=MyEC2InstanceProfile
   ```

7. login to ec2 instance and `install Java,maven and git` in ec2 instance.
   
   ```
   ssh -i /path/to/your-key.pem ec2-user@your-instance-ip
   
   sudo yum install java-1.8.0-amazon-corretto
   
   sudo yum install java-1.8.0-amazon-corretto-devel
   
   sudo wget https://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
   
   sudo sed -i s/\$releasever/6/g /etc/yum.repos.d/epel-apache-maven.repo
   
   sudo yum install -y apache-maven
   
   sudo yum install git
   ```

### Steps to test the Authentication and check elastiCache Redis Cluster Connection

1. Login in `ec2 instance` .
   
   ```
   ssh -i /path/to/your-key.pem ec2-user@your-instance-ip
   ```

2. Clone the `aws-iam-auth-demo-app` from git with the help of below URL.
   
   ```
   git clone https://github.com/aws-samples/elasticache-iam-auth-demo-app.git
   
   cd elasticache-iam-auth-demo-app
   ```

3. Build the code with the help of `mvn clean install -U` command.
   
   ```
   mvn dependency:resolve-plugins
   
   mvn clean install
   ```

4. Replace with your created `cluster name, username, replicationgroupID,host` in below commands.

5. After successfull build run the below command to `generate auhtentication security token`.
   
   ```
   java -cp target/ElastiCacheIAMAuthDemoApp-1.0-SNAPSHOT.jar com.amazon.elasticache.IAMAuthTokenGeneratorApp --region ****** --replication-group-id ****** --user-id ******
   ```

6. Test the connection with `elasticache redis cluster` and `IAM authentication with the User`.
   
   ```
   java -jar target/ElastiCacheIAMAuthDemoApp-1.0-SNAPSHOT.jar --redis-host ****** --region ****** --replication-group-id ****** --user-id ****** --tls
   ```

### References and links:

[Authenticating with IAM - Amazon ElastiCache for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/auth-iam.html)

[Setting up Maven on AWS - EC2](https://www.linkedin.com/pulse/setting-up-maven-aws-ec2-lionel-tchami-nfada-bsc-msc-/)

[Amazon Corretto 8 Installation Instructions for Amazon Linux 2 and Amazon Linux 2023 - Amazon Corretto](https://docs.aws.amazon.com/corretto/latest/corretto-8-ug/amazon-linux-install.html)

https://github.com/avizway1/aws-projects/blob/main/redis.md

[Attaching AWS IAM roles To EC2 instances - Matillion Docs](https://docs.matillion.com/metl/docs/2765606/)

https://dataintegration.info/simplify-managing-access-to-amazon-elasticache-for-redis-clusters-with-iam

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
