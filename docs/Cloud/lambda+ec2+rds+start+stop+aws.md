# Start Stop Postgresql RDS and EC2 instance using Lambda Function and Schedule it for every hour run

## Pre-requisite

1. AWS login User

2. AWS Cli

3. Python3 

## AWS Services Using during implementation

1. aws ec2

2. aws rds

3. aws lambda

4. aws eventbridger schedular

5. aws IAM

## Create AWS ec2 Instance

- create vpc
  
  ```
  aws ec2 create-vpc --cidr-block 10.0.0.0/16
  ```

- create subnet
  
  ```
  aws ec2 create-subnet --vpc-id vpc-id --cidr-block 10.0.1.0/24
  ```

- create internet gateway
  
  ```
  aws ec2 create-internet-gateway
  ```

- attach internet gateway to vpc
  
  ```
  aws ec2 attach-internet-gateway --vpc-id vpc-id --internet-gateway-id igw-id
  ```

- create route table for vpc
  
  ```
  aws ec2 create-route-table --vpc-id vpc-id
  ```

- create routes for internet gateway
  
  ```
  aws ec2 create-route --route-table-id rtb-id --destination-cidr-block 0.0.0.0/0 --gateway-id igw-id
  ```

- create security group 
  
  ```
  aws ec2 create-security-group --group-name my-sg --description "Allow SSH and HTTP(S)" --vpc-id vpc-id
  ```

- create inbound rule for access ec2 instance
  
  ```
  aws ec2 authorize-security-group-ingress --group-id sg-id --protocol tcp --port 22 --cidr 0.0.0.0/0 
  aws ec2 authorize-security-group-ingress --group-id sg-id --protocol tcp --port 80 --cidr 0.0.0.0/0
  aws ec2 authorize-security-group-ingress --group-id sg-id --protocol tcp --port 443 --cidr 0.0.0.0/0
  ```

- associate subnets to route table
  
  ```
  aws ec2 associate-route-table --subnet-id subnet-id --route-table-id rtb-id
  ```

- create ec2 instance with all above details 
  
  ```
  aws ec2 run-instances --image-id ami-id --count 1 --instance-type t2.micro --key-name my-key --security-group-ids sg-id --subnet-id subnet-id
  ```

## Create AWS RDS PostgreSQL Instance

```
aws rds create-db-instance \
  --db-instance-identifier my-postgres-instance \
  --db-instance-class db.t2.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password password \
  --vpc-security-group-ids sg-01234567890abcdef \
  --allocated-storage 20 \
  --db-subnet-group-name mydbsubnetgroup \
  --engine-version 12.5 \
  --license-model postgres-license
```

The key parameters:

- --engine - Specifies postgres for PostgreSQL database
- --engine-version - PostgreSQL version to use
- --license-model - Should be 'postgres-license' for PostgreSQL
- Other parameters like instance class, storage, subnet group, security groups etc. are the same as MySQL
- The security group must allow access on PostgreSQL port 5432

Some other optional parameters:

- --preferred-maintenance-window - Set weekly maintenance window
- --backup-retention-period - Days to retain backups
- --multi-az - Create a multi-AZ deployment for high availability
- --storage-encrypted - Encrypt the database storage

## Create Lambda Function to Start Stop our aws RDS and EC2 instance

```
aws lambda create-function \
--function-name my-function \
--runtime python3.11 \
--role arn:aws:iam::123456789012:role/lambda-role \  
--handler lambda_function.lambda_handler \
--zip-file fileb://function.zip
```

## Lambda_fucntion.py file inside function.zip

```
# RDS & EC2 start stop by lambda function
import boto3

rds = boto3.client('rds', region_name='ap-south-1')
ec2 = boto3.client('ec2', region_name='ap-south-1')

def lambda_handler(event, context):

    # Get the DB instance identifier (replace 'your-db-instance-id' with your actual RDS instance id)
    db_instance_id = 'my-database-psql-1'

    # Get the instance id (you can replace 'your-instance-id' with your actual instance id)
    instance_id = 'i-0feb2e9167c44f418'

    # Get the current state of the RDS instance
    rds_response = rds.describe_db_instances(DBInstanceIdentifier=db_instance_id)
    rds_state = rds_response['DBInstances'][0]['DBInstanceStatus']

    # Get the current state of the instance
    ec2_response = ec2.describe_instances(InstanceIds=[instance_id])
    ec2_state = ec2_response['Reservations'][0]['Instances'][0]['State']['Name']

    # Start or stop the RDS instance based on its current state
    if rds_state == 'available':
        rds.stop_db_instance(DBInstanceIdentifier=db_instance_id)
        print(f"RDS instance {db_instance_id} is now stopped.")
    elif rds_state == 'stopped':
        rds.start_db_instance(DBInstanceIdentifier=db_instance_id)
        print(f"RDS instance {db_instance_id} is now started.")
    else:
        print(f"RDS instance {db_instance_id} is in an unexpected state: {rds_state}")

    # Start or stop the instance based on its current state
    if ec2_state == 'running':
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} is now stopped.")
    elif ec2_state == 'stopped':
        ec2.start_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} is now started.")
    else:
        print(f"Instance {instance_id} is in an unexpected state: {ec2_state}")

    return {
        'statusCode': 200,
        'body': 'Function executed successfully!'
    }
```

## Update the above code in Lambda Function

```
zip -g function.zip lambda_function.py
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip
```

## Configure Evenbridge Scheduler for run our lambda function on hourly basis

1. Open the AWS Management Console and navigate to the Amazon EventBridge service.

2. In the left sidebar, select "schedules" under "Schedular"

3. Click on the "Create Schedule" button.

4. Fillup the all necessary details like
   
   - Schedule Name
   
   - Schedule Group 
   
   - Schedule Pattern
     
     - Recurring Schedule
       
       - Rate Based Schedule
         
         - Rate Expression 
           
           **rate (12 hours)**
   
   - Flexible time window
   
   - Click Next
   
   - Select Target
     
     - target detail
     
     - target API 
     
     - Select **Template targets**
     
     - select icon **AWS Lambda Invoke**
   
   - select Lambda fucntion **my-function** created by us from drop down menu

5. then click on **skip to review and create schedule**.

6. In the end Review the all configuration in opned window.

7. Click on the button **Create Schedule**.

## Created IAM role

1. **Amazon_EventBridge_Scheduler_LAMBDA_a0c1b2b2db**
   
   This role is create to invoke lambda function from Event bridge.

2. **my-aws-service-start-stop-role-56i4h6n0**
   
   - This role is create to execute lambda function to perform operation on rds and ec2.
   
   - We need to add some default policy in this role with respect to requirement.
     
     - EC2 and RDS  Services 
       
       - List, Describe, Start , Stop permission
     
     - AWS Lambda function
       
       - full access

     - CloudWatch Logs
       
       - logs:CreateLogGroup, logs:CreateLogStream,logs:PutLogEvents  

## Reference

[Python Install in Windows 10](https://www.digitalocean.com/community/tutorials/install-python-windows-10)

[Install, Update, and Uninstall the AWS CLI on Windows](https://docs.aws.amazon.com/cli/v1/userguide/install-windows.html)

[AWS EC2 Documentation](https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html)

[Create and Connect to a PostgreSQL Database with Amazon RDS](https://aws.amazon.com/getting-started/hands-on/create-connect-postgresql-db/)

[Lambda functions with Python - AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)

[Introducing Amazon EventBridge Scheduler | AWS Compute Blog](https://aws.amazon.com/blogs/compute/introducing-amazon-eventbridge-scheduler/)

[create-role AWS CLI 1.29.83](https://docs.aws.amazon.com/cli/latest/reference/iam/create-role.html)

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
