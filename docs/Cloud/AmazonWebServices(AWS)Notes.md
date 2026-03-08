# ☁️ The Ultimate AWS Masterclass: Zero to Cloud Architect

This guide is systematically designed to take a learner from an **absolute beginner** to an **expert-level Cloud Architect**. 
Below you will find deep technical content, real-world examples, disaster recovery scenarios, test cases, and widely used AWS CLI operations perfectly tailored for the modern DevOps platform.

---

## 📑 Table of Contents
1. [AWS CLI Fundamentals (The Foundation)](#1-aws-cli-fundamentals)
2. [IAM (Identity & Access Management)](#2-iam-identity--access-management)
3. [EC2 & Auto Scaling (Compute)](#3-ec2--auto-scaling)
4. [VPC & Networking (The Backbone)](#4-vpc--networking)
5. [S3 (Storage & Data Security)](#5-s3--storage-security)
6. [EKS & Containerization (Advanced Compute)](#6-eks-elastic-kubernetes-service)
7. [Disaster Recovery & Enterprise Scenarios](#7-enterprise-architecture--scenarios)

---

## 1. AWS CLI Fundamentals
Before interacting with the console, mastering the AWS CLI natively is mandatory for automation.

### Beginner: Initializing configurations
```bash
# Set up Access Keys, Default Region (e.g., us-east-1), and output format (json)
aws configure 

# Check which identity you are actively logged in as
aws sts get-caller-identity
```

### Expert: Cross-Account Role Assumption (Real World)
*Scenario:* You are an admin in `Account A`. You need to deploy infrastructure in `Dev Account B` securely without generating long-lived keys.
```bash
# Assume a Role in Account B dynamically returning ephemeral (1-hour) tokens
aws sts assume-role \
  --role-arn "arn:aws:iam::123456789012:role/DevOpsAdmin" \
  --role-session-name "CLI-Deployment-Session" \
  --duration-seconds 3600

# Export the returned JSON variables securely into your bash profile
export AWS_ACCESS_KEY_ID="ASIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."
```

---

## 2. IAM (Identity & Access Management)
The security perimeter of AWS. Zero-trust principles start here.

### Real World Use Case: The Principle of Least Privilege
**Use Case:** An application running on EC2 needs to download logs from an S3 bucket named `company-logs`. 
*Rookie Mistake:* Giving the EC2 instance `AmazonS3FullAccess`.
*Expert Solution:* Create an inline IAM Policy allowing exactly *one* API call (`s3:GetObject`) strictly mapped to that single ARN.

**IAM Policy Example:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::company-logs/*"]
    }
  ]
}
```

### Key Commands:
```bash
# List all IAM Users physically active
aws iam list-users

# Attach the Least-Privilege policy to the EC2 Instance Profile dynamically
aws iam put-role-policy --role-name "EC2-LogReader-Role" --policy-name "StrictS3Policy" --policy-document file://policy.json
```

---

## 3. EC2 & Auto Scaling
Virtual Machines acting as the core compute mechanism.

### Beginner: Launching an Instance
*How do I provision a rapid test server?*
```bash
# Launch a micro instance utilizing an SSH key
aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --count 1 --instance-type t3.micro --key-name MyProdKey --security-group-ids sg-1234abcd
```

### Expert: Resilient Auto Scaling & Spot Instances
**Scenario:** A chaotic web application encounters hyper-spikes during sales events.
1. **Launch Template:** Build an immutable Launch Template utilizing a `golden-AMI` baked via **Packer**.
2. **Auto Scaling Group (ASG):** Configure an ASG mapped across 3 Availability Zones (us-east-1a, 1b, 1c).
3. **Cost Optimization:** Mix **On-Demand** (20%) and **Spot Instances** (80%). Spot instances are 90% cheaper but can be terminated by AWS with a 2-minute warning.
4. **Behavior:** If AWS terminates a Spot Instance, the ASG detects the underlying EC2 death mathematically and automatically provisions a replacement node instantly.

**Testing the ASG (Chaos Engineering):**
```bash
# Terminate an instance manually to forcefully trigger the ASG recovery loop
aws ec2 terminate-instances --instance-ids i-0abcdef1234567890

# Monitor the ASG spinning up the replacement natively
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names Prod-Web-ASG
```

---

## 4. VPC (Virtual Private Cloud) & Networking
The absolute hardest concept to master natively, but the most important.

### Subnet Layout Strategy
*   **Public Subnet:** Houses Internet Gateways. Only resources needing public internet (Load Balancers, Bastion Hosts) live here.
*   **Private Subnet:** Houses the NAT Gateway router. 99% of your EC2/EKS Nodes live securely here. They can reach the internet to download updates, but the internet *cannot* reach them.
*   **Database Subnet:** Completely disconnected. No NAT gateways. Only the Private Subnets can query them.

### Troubleshooting Scenario: "My EC2 Instance cannot reach the internet"
**Diagnostic Test Cases Checklist:**
1. Is it in a Private Subnet? If yes, does the Subnet's Route Table point `0.0.0.0/0` to a **NAT Gateway**?
2. If it's a Public Subnet, does it have an **Elastic IP / Public IP** attached? Does the Route Table map natively to an **Internet Gateway (IGW)**?
3. Check the **Security Group**. Is Outbound (Egress) heavily restricted?
4. Check the **NACL (Network Access Control List)**. Are ephemeral ports (1024-65535) open for the return HTTP traffic?

---

## 5. S3 (Storage & Security)

### Real-World Use Case: Preventing Ransomware
**The Attack:** A compromised developer laptop issues an AWS CLI command recursively deleting the massive production S3 DB backups.
**The Defense (Expert Level):** 
1. Enable **S3 Versioning**. When an object is "deleted", it simply applies a Delete Marker rather than actually destroying the physical bits.
2. Enable **MFA Delete**. Physically requires a rolling 6-digit Google Authenticator code sent by the Root user to physically delete a file.
3. Enable **Object Lock (Compliance Mode)**. A WORM (Write Once, Read Many) model. Not even the Root User account can aggressively delete or overwrite the object until the mathematical timestamp expires (e.g., 5 years).

### Useful CLI Commands:
```bash
# Synchronize a local directory securely directly to S3
aws s3 sync /var/log/nginx s3://my-backup-logs/

# Make an S3 bucket 100% private forcefully via CLI
aws s3api put-public-access-block \
    --bucket my-secure-data \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

---

## 6. EKS (Elastic Kubernetes Service)
When you outgrow EC2, you move to container orchestration.

### Expert Scenario: Node Throttling & Karpenter Autoscaling
*The Problem:* The traditional Cluster Autoscaler (CA) takes 3-5 minutes to provision new EC2 nodes for Pending Pods. During traffic spikes, users experience 504 Timeouts waiting for backend capacity.
*The Solution:* Migrate exclusively to **Karpenter**.
*   **Just-in-Time Nodes:** Karpenter reads the exact physical CPU/RAM requirements of the Pending Pods. It bypasses ASGs completely, calling the EC2 Fleet API directly. 
*   **Zero-Waste:** It provisions the mathematically perfect instance type (e.g., exactly `c5.xlarge`) in under 45 seconds, maximizing cost density and slashing the timeout window dramatically.

**Updating the Kubeconfig:**
```bash
# Connect local kubectl auth context dynamically to the EKS Cluster
aws eks update-kubeconfig --region us-east-1 --name production-eks-cluster
```

---

## 7. Enterprise Architecture & Scenarios

### Disaster Recovery: Cross-Region Aurora Failover
**Test Case:** The entire `us-east-1` AWS region suffers a catastrophic power outage.
**Execution:**
1. You have an **Amazon Aurora Global Database**. Data is synchronously replicating to `us-west-2` with sub-second latency.
2. When `us-east-1` dies, the database in `us-west-2` automatically promotes itself from an explicitly Read-Only Replica to the Primary Writer.
3. **Route 53 DNS** health checks fail heavily on the East Load Balancer. It instantaneously shifts 100% of global DNS traffic exclusively strictly to the West Load Balancer endpoints.
4. The system is structurally recovered natively within 60 seconds with **Zero Data Loss**.

### Cost Optimization: EIP Sprawl
**The Scenario:** AWS bills skyrocketed because the developer team provisioned hundreds of Elastic IPs (EIPs) and never attached them to running instances. AWS charges hourly strictly for *unattached* EIPs.
**The Fix:**
```bash
# Find all completely orphaned (unattached) Elastic IPs using JmesPath Queries
aws ec2 describe-addresses --query 'Addresses[?AssociationId==null].PublicIp'

# Delete them automatically via a bash script
aws ec2 describe-addresses --query 'Addresses[?AssociationId==null].AllocationId' --output text | xargs -n 1 aws ec2 release-address --allocation-id
```

---
*Created dynamically for absolute mastery across AWS Architecture, Operations, and Engineering.*


---

## 8. Serverless Compute (AWS Lambda & API Gateway)
Moving away from managing servers entirely. Code runs strictly in response to events.

### Real-World Problem: CloudWatch Log Sprawl Costs
**The Scenario:** A high-traffic application is writing thousands of GBs of logs to CloudWatch Daily. The bill is skyrocketing because the logs are kept implicitly "Forever".
**The Solution (Serverless Event-Driven Cleanup):**
1. Create a Python Lambda function that uses the `boto3` SDK to scan all CloudWatch Log Groups.
2. If a Log Group has a `RetentionInDays` set to `null` (Forever), the Lambda forces it to 30 days automatically.
3. **EventBridge (CloudWatch Events):** Trigger this Lambda on a `cron(0 12 * * ? *)` schedule daily. No servers to maintain, costs $0.01 per month, saves thousands natively.

**Snippet of the boto3 logic:**
```python
import boto3
logs = boto3.client('logs')

def lambda_handler(event, context):
    paginator = logs.get_paginator('describe_log_groups')
    for page in paginator.paginate():
        for group in page['logGroups']:
            if 'retentionInDays' not in group:
                logs.put_retention_policy(
                    logGroupName=group['logGroupName'],
                    retentionInDays=30
                )
```

---

## 9. Databases (RDS & Aurora)
Managing relational capabilities natively across Availability Zones.

### Real-World Problem: Connection Exhaustion during Spikes
**The Scenario:** You rely heavily on AWS Lambda for an API, scaling dynamically to 1000 concurrent invocations instantly during a flash sale. Each Lambda spawns a direct TCP connection to the RDS PostgreSQL instance. The database reaches `max_connections`, completely locking up and returning `500 Internal Server Errors`.
**The Solution (Amazon RDS Proxy):**
Direct connections from serverless compute to relational DBs are dangerous. By deploying **RDS Proxy** (a fully managed, highly available database proxy) sitting directly between Lambda and RDS:
1. The Lambda functions connect purely to the Proxy.
2. The Proxy mathematically multiplexes and pools the connections, sending only a safe, steady handful of long-lived connections physically down to the RDS DB.
3. This prevents connection thrashing entirely while absorbing the immense serverless scale automatically.

---

## 10. Global Networking & DNS (Route 53)
Enterprise-grade DNS routing and high availability spanning the globe.

### Real-World Use Case: Global Blue/Green Deployment
**The Scenario:** You have `v1` of your application running in `eu-west-1` and you just deployed `v2` securely into `us-east-1`. You want to test `v2` safely without shifting all traffic and causing an outage.
**The Solution (Route 53 Weighted Routing):**
1. Create a **Weighted Routing Policy** explicitly on the `api.example.com` A-Record.
2. Assign **Weight: 90** securely pointing to the `eu-west-1` Load Balancer.
3. Assign **Weight: 10** pointing exclusively to the `us-east-1` Load Balancer.
4. Exactly 10% of global DNS queries will be routed dynamically to the new infrastructure. If CloudWatch visualizes 5xx errors spiking, simply change `v2` weight back to 0 instantaneously. 

---

## 11. Edge Security & Delivery (CloudFront & AWS WAF)
Dedicating caching and threat mitigation explicitly to the network edge, stopping bad actors before they even hit your VPC.

### Real-World Problem: Layer 7 DDoS & SQL Injection
**The Scenario:** Competitors/Bots are spamming your Application Load Balancer natively with massive POST requests attempting SQL injections. Your EC2 instances CPU is spiking to 100% just trying to reject the bad requests.
**The Solution (AWS WAF & CloudFront):**
1. Map your ALB exclusively behind an **Amazon CloudFront** distribution.
2. Attach an **AWS Web Application Firewall (WAF)** directly to CloudFront.
3. Enable managed rule groups like `AWSManagedRulesSQLiRuleSet` and setup a Rate-Based Rule restricting IP addresses to a max of 2000 requests per 5 minutes.
4. The malicious traffic hits the physical AWS Edge Location nearest to the attacker, natively evaluated by the WAF in microseconds, and completely dropped *before* it ever traverses the AWS backbone to reach your physical compute.

### CLI Setup: Creating a WAF IP Set
```bash
aws wafv2 create-ip-set \
    --name "BlockList" \
    --scope CLOUDFRONT \
    --ip-address-version IPV4 \
    --addresses 192.0.2.44/32 203.0.113.0/24
```

---

## 12. Monitoring & Automated Remediation (CloudWatch & SNS)
Going beyond just dashboards by actively fixing infrastructure automatically.

### Real-World Use Case: The Runaway CPU
**The Scenario:** A background worker VM suffers a memory leak and pins its CPU at 100% for an hour, rendering it completely useless.
**The Fix (Automated Remediation):**
1. Configure a CloudWatch Alarm monitoring the exact `AWS/EC2 CPUUtilization` metric heavily natively for that specific Instance ID.
2. Threat Condition: `CPU > 95% for 3 consecutive 5-minute periods`.
3. Instead of simply sending an email alert to PagerDuty via an SNS Topic, assign an automatic **EC2 Action** to the Alarm: `arn:aws:automate:us-east-1:ec2:reboot`.
4. CloudWatch will physically reboot the specific instance via the hypervisor exclusively without human intervention, immediately resolving the memory leak and restoring normal telemetry natively at 3 AM while you sleep.

---

## 13. Storage & Content Delivery (S3 & CloudFront)
Managing petabyte-scale object storage and global content distribution.

### Real-World Problem: S3 Bucket Public Exposure & Data Exfiltration
**The Scenario:** A developer accidentally sets the public access block settings to `false` on a critical S3 bucket containing customer PII. The bucket is immediately scanned by bots and data starts being downloaded rapidly.
**The Solution (S3 Block Public Access & Bucket Policies):**
1. **Block Public Access (BPA):** Ensure BPA is enabled at the account level. This is the absolute first line of defense, preventing accidental public exposure natively.
2. **Bucket Policies:** Explicitly deny all public access within the bucket policy itself, even if BPA were somehow disabled.
3. **VPC Endpoints:** Force all traffic to the S3 bucket to travel strictly through your private VPC network using **Gateway Endpoints**, ensuring data never touches the public internet.

**CLI Setup: Enforcing Private Access via VPC Endpoint Policy:**
```bash
aws ec2 create-vpc-endpoint \
    --vpc-id vpc-12345678 \
    --vpc-endpoint-type Gateway \
    --service-name com.amazonaws.us-east-1.s3 \
    --route-table-ids rtb-abc123

# Attach a policy to the endpoint to strictly deny public access
aws ec2 modify-vpc-endpoint \
    --vpc-endpoint-id vpce-98765432 \
    --policy '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::my-sensitive-bucket",
                "arn:aws:s3:::my-sensitive-bucket/*"
            ]
        }]
    }'
```

---

## 14. Security, Identity, & Compliance (IAM, Cognito, & KMS)
Managing access control and encryption keys natively across the entire AWS ecosystem.

### Real-World Problem: Over-Privileged IAM Users & Stale Credentials
**The Scenario:** Your development team has grown to 50 engineers. Many IAM users have `AdministratorAccess` policies attached "just in case" they need access later. Furthermore, old employee credentials (Access Keys) are floating around in code repositories.
**The Solution (IAM Access Analyzer & Credential Rotation):**
1. **IAM Access Analyzer:** Run this service to scan all IAM policies and identify resources (like S3 buckets or DynamoDB tables) that are accessible from outside your AWS account. It will flag every single over-privileged resource immediately.
2. **IAM Credential Report:** Generate a report to see exactly when each user last used their access keys. Force rotation on any key that hasn't been used in 90 days.
3. **IAM Policy Simulator:** Before deploying a new policy, simulate the exact API calls it would allow to ensure you aren't granting unintended access.

**CLI Setup: Generating a Credential Report:**
```bash
# Generate the report (this takes a few minutes)
aws iam generate-credential-report

# Download and view the report
aws iam get-credential-report --output text > credential-report.csv

# Analyze for stale keys (e.g., last used > 90 days ago)
# (Requires scripting or CSV parsing)
```

---

## 15. Analytics & Big Data (EMR, Redshift, & Athena)
Processing and analyzing massive datasets natively at scale.

### Real-World Use Case: Interactive SQL Queries on Petabyte-Scale Data Lakes
**The Scenario:** You store terabytes of raw JSON logs from your application in S3. Running complex analytical SQL queries directly on this data is slow and expensive using traditional Hadoop clusters.
**The Solution (Amazon Athena):**
**Amazon Athena** is a serverless, interactive query service that uses standard SQL to analyze data directly in S3. It requires zero infrastructure management.
1. **Create a Glue Data Catalog:** Define the schema (table structure) for your raw S3 data using the AWS Glue Crawler or manually.
2. **Run SQL Queries:** Execute standard ANSI SQL queries directly against the S3 data.
3. **Pay Per Query:** You only pay for the amount of data scanned by your queries. Optimizing with partitioning and columnar formats (like Parquet) reduces costs dramatically.

**Example Athena Query (Querying JSON Logs in S3):**
```sql
-- Define the table structure (Schema) for your JSON data in S3
CREATE EXTERNAL TABLE IF NOT EXISTS my_logs (
  timestamp STRING,
  user_id STRING,
  action STRING,
  ip_address STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.JsonSerde'
LOCATION 's3://my-data-lake/raw-logs/';

-- Now run a fast, interactive SQL query
SELECT
  user_id,
  COUNT(*) as event_count
FROM my_logs
WHERE timestamp > '2023-01-01'
GROUP BY user_id
ORDER BY event_count DESC
LIMIT 10;
```


---

## 26. MLOps Pipeline Architecture (Amazon SageMaker)
Building secure, enterprise-grade Machine Learning pipelines mathematically deploying models from training to production.

### Real-World Use Case: Automated Model Retraining Pipeline
**The Scenario:** Data Scientists hand off a Jupyter Notebook. You need to convert this into a repeatable, automated pipeline that retrains the model on fresh data weekly and deploys the Endpoint automatically, without manual intervention.
**The Solution (SageMaker Pipelines & EventBridge):**
1. **The Data Pipeline:** Raw data lands in an S3 Bucket (`s3://raw-ml-data`).
2. **The Trigger:** EventBridge catches the `s3:ObjectCreated:Put` event natively and starts a **SageMaker Pipeline** execution.
3. **The Processing Step:** An ephemeral SageMaker Processing Job spins up a cluster, cleans the data, and writes the engineered features back to S3.
4. **The Training Step:** SageMaker provisions an isolated GPU instance (`ml.p3.2xlarge`), fetches your Docker container from ECR, trains the model, and outputs the mathematical `.tar.gz` model artifact.
5. **The Condition Step:** The pipeline evaluates the model's accuracy natively. If `Accuracy > 85%`, it executes the deployment step.
6. **The Deployment:** SageMaker mathematically swaps the production REST API Endpoint (Real-Time Inference) dynamically via Blue/Green to the new model without dropping live requests.

**CLI Setup: Starting a Pipeline Execution**
```bash
aws sagemaker start-pipeline-execution \
    --pipeline-name "Weekly-Fraud-Detection-Pipeline" \
    --pipeline-execution-description "Automated run via EventBridge"
```

---

## 27. MLOps Networking & Endpoint Troubleshooting
When you place AI workloads into isolated enterprise VPCs, networking becomes the absolute hardest obstacle.

### Real-World Problem: "SageMaker Training Job Stuck in Downloading data"
**The Scenario:** Data scientists complain that their deep learning training jobs take 3 hours just to download the dataset from S3 before training even starts, or the job permanently times out with `ClientError`.
**The Networking Root Cause:** 
SageMaker Training instances are launched inside an isolated AWS-managed VPC. By default, they must route over the public internet (via NAT Gateway) to reach your S3 bucket, massively throttling download speeds. If your private VPC lacks a NAT Gateway, it times out mathematically.
**The MLOps Solution (VPC Endpoints & Fast File Mode):**
1. **S3 Gateway Endpoint:** Create a Gateway VPC Endpoint securely inside the subnet routing table. Traffic mathematically bypasses the internet, traveling across the AWS high-speed internal backbone natively resulting in gigabit download speeds for free.
2. **Fast File Mode:** Instead of downloading 100GB of images to the local EBS volume (`File` input mode), switch the SageMaker estimator to `FastFile` mode. SageMaker streams the data exactly as-needed directly from S3 natively avoiding the 3-hour pre-download penalty entirely.

**CLI Setup: Creating an S3 Gateway Endpoint for MLOps**
```bash
aws ec2 create-vpc-endpoint \
    --vpc-id vpc-0abc12345def67890 \
    --vpc-endpoint-type Gateway \
    --service-name com.amazonaws.us-east-1.s3 \
    --route-table-ids rtb-1234567890abcdef0
```

---

## 28. IAM Security for AI & MLOps (PassRole)
Zero-trust architecture specifically structured for Machine Learning isolation.

### Real-World Problem: The "iam:PassRole" Vulnerability
**The Scenario:** You grant an MLOps CI/CD pipeline role permission to start a SageMaker Training Job. The pipeline starts the job successfully, but the Training Job crashes with `AccessDenied` when trying to save the model to S3.
**The IAM Root Cause:**
The CI/CD pipeline does *not* execute the training job. SageMaker natively assumes an entirely separate `Execution Role` to run the active compute.
1. The CI/CD Pipeline must have `sagemaker:CreateTrainingJob`.
2. The CI/CD Pipeline must ALSO have `iam:PassRole` strictly allowing it to mathematically "hand over" the Execution Role securely to the SageMaker service.
3. The Execution Role itself must legally contain the `s3:PutObject` permission.

**The Solution (Strict IAM PassRole Constraint):**
If a developer has `iam:PassRole` securely but it lacks bounds, they could pass an `AdministratorAccess` role to a SageMaker instance they control, executing full environment takeover. You must strictly bound the PassRole permission.

**IAM Policy for the CI/CD Pipeline:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::123456789012:role/Specific-SageMaker-ExecutionRole-Only",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "sagemaker.amazonaws.com"
        }
      }
    }
  ]
}
```

---

## 29. MLOps Inference Troubleshooting & Cost Optimization
Stopping AI from destroying your cloud budget gracefully.

### Real-World Problem: Wasted GPU Endpoints
**The Scenario:** You deployed a highly complex 15-billion parameter LLM to a SageMaker Real-Time Endpoint running on an `ml.g5.12xlarge` ($7.00/hour). Users only query the model 10 times a day, but you are paying mathematically $5,000+ a month permanently.
**The Solution (Serverless Inference & Asynchronous Endpoints):**
1. **Serverless Inference:** If the model size is smaller, switch instantly to SageMaker Serverless Inference. It scales to zero mathematically when not in use. You pay exclusively per millisecond of compute.
2. **Asynchronous Endpoints (For massive models):** If the model is too large for Serverless, deploy an Asynchronous Endpoint backed by native Auto Scaling securely.
   * Configure the ASG to scale the instance count strictly to `0`.
   * When a user sends a payload, SageMaker queues it natively via an internal SNS/SQS structure.
   * The queue length dynamically spins up the `ml.g5.12xlarge`, processes the request, drops the answer securely into an S3 bucket, and aggressively scales back to `0`, mathematically collapsing the cloud bill.

**CLI Setup: Scaling an MLOps Endpoint to Zero**
```bash
# Register the SageMaker scalable target natively
aws application-autoscaling register-scalable-target \
    --service-namespace sagemaker \
    --resource-id endpoint/MyLLMEndpoint/variant/MyVariant \
    --scalable-dimension sagemaker:variant:DesiredInstanceCount \
    --min-capacity 0 \
    --max-capacity 2
```


---

# 📚 THE ULTIMATE AWS CHEAT SHEET & QUICK REFERENCE 
*Source: digitalcloud.training | Compiled Quick-Reference Notes*

This section is a massive, rapid-fire cheat sheet covering core concepts, architectural rules, and Hands-On Labs (HOL) spanning the entirety of the AWS ecosystem.

---

## 🔐 30. AWS Identity and Access Management (IAM)
IAM is universal (Global) and does not apply to any specific region. All permissions are **implicitly denied by default** for all resources (except for the Root user). 

*   **User:** An identity bound to a person or application.
*   **Group:** A collection of Users for organized permission management.
*   **Role:** An identity with specific permissions meant to be *assumed* temporarily by users, applications, and AWS services.
*   **Policy:** A JSON document defining exactly what API actions are `Allowed` or `Denied` on specific `Resources`.

### IAM Policies & Boundaries
*   **Identity-based Policy:** Applied to users, groups, or roles.
*   **Resource-based Policy:** Applied directly to resources (e.g., S3 buckets, DynamoDB tables).
*   **Permissions Boundary:** Sets the absolute *maximum* permissions an identity can have.
*   **Service Control Policies (SCPs):** Set the maximum permissions for an entire Organization or Organizational Unit (OU).

**Root User vs. IAM User:**
| Identity | Login Details | Permissions |
| :--- | :--- | :--- |
| **Root User** | `@Email Address` | Full Unrestricted Access |
| **IAM User** | `Friendly Name (e.g., John) + Account ID/Alias` | Bound strictly by IAM Policies |

### Basic CLI Operations for IAM & Setup
```bash
# Configure Access Keys
aws configure

# Check active identity
aws sts get-caller-identity
```

---

## 💻 31. Amazon Elastic Compute Cloud (EC2)
EC2 instances utilize various virtualization servers. Data is stored natively on **EBS (Elastic Block Store)** volumes acting as virtual hard drives at the block level.

*   **Security Groups (SGs):** Instance-level firewalls. **Stateful** (return traffic is automatically allowed). Only support `Allow` rules.
*   **Network ACLs (NACLs):** Subnet-level firewalls. **Stateless** (return traffic must be explicitly allowed). Support both `Allow` and `Explicit Deny` rules.
*   **Instance Metadata:** Accessible exclusively from within the instance at `http://169.254.169.254/latest/meta-data`.

### Network Interfaces & IP Addresses 
*   **ENI (Elastic Network Interface):** Standard interface for all instances.
*   **ENA (Elastic Network Adapter):** Enhanced networking, higher bandwidth, lower latency.
*   **EFA (Elastic Fabric Adapter):** High-Performance Computing (HPC), tightly coupled ML workloads.
*   **Elastic IP (EIP):** Static public IPv4 address. You are charged if it is provisioned but *not* attached to a running instance. Remains when instances stop.
*   **Public IP:** Dynamic. Lost when an instance is explicitly stopped (but not on reboot). 

### Elastic Load Balancing (ELB)
*   **Application Load Balancer (ALB):** Layer 7 (HTTP/HTTPS). Routes based on paths, headers, queries.
*   **Network Load Balancer (NLB):** Layer 4 (TCP/UDP). Ultra-high performance, low latency, handles millions of requests per second. Can use a static EIP.
*   **Gateway Load Balancer (GWLB):** Layer 3. Used inline for virtual firewalls, deep packet inspection.

---

## 🌐 32. Amazon VPC (Virtual Private Cloud)
Logically isolated virtual networks. By default, you can create 5 VPCs per region.

*   **Internet Gateway (IGW):** Enables internet access for Public Subnets. Target in Route Table: `0.0.0.0/0 -> igw-id`.
*   **NAT Gateway:** Enables internet access for Private Subnets (outbound only). Must be deployed physically inside a *Public* subnet. Private Route Table points `0.0.0.0/0 -> nat-gw-id`.
*   **VPC Peering:** Direct connection between two VPCs. Requires **non-overlapping CIDR blocks**.
*   **VPC Flow Logs:** Captures IP traffic meta-data going to/from network interfaces. Does not capture the packet payload.

---

## 🪣 33. Amazon Simple Storage Service (S3)
Global REST API object storage, but buckets are provisioned physically within a specific Region. Unlimited storage capacity. File sizes range from 0 bytes to 5 TB.

### Storage Classes
1.  **S3 Standard:** Frequently accessed data (default).
2.  **S3 Intelligent-Tiering:** Uses ML to automatically move data to the cheapest tier based on changing access patterns automatically without performance hits.
3.  **S3 Standard-IA:** Infrequent access, but requires millisecond retrieval when needed.
4.  **S3 One Zone-IA:** Data stored in only one AZ (lower cost, lower durability).
5.  **S3 Glacier Flexible Retrieval:** Archival storage (minutes to hours retrieval).
6.  **S3 Glacier Deep Archive:** Lowest cost in AWS. Long-term compliance archival (12 hours retrieval).

### Security & Advanced Features
*   **MFA Delete:** Requires a rolling 6-digit MFA token to permanently delete a file or change versioning state. Must be enabled by the Root user.
*   **S3 Presigned URLs:** Grants temporary, time-bound access to private objects securely without making the bucket public.
*   **Object Lock (WORM):** Write Once, Read Many. Prevents deletion even by Root users for compliance.
*   **Transfer Acceleration:** Routes uploads through the global CloudFront Edge Network backbone directly to the S3 bucket for massive speed improvements.

---

## 🚀 34. DNS, Caching, and CDN
### Amazon Route 53 (DNS)
*   **Simple Routing:** Standard `A` record response.
*   **Failover Routing:** Active/Passive routing based on Health Checks.
*   **Geolocation Routing:** Routes based on where the user physically is in the world.
*   **Weighted Routing:** Directs exact percentages of traffic (e.g., Blue/Green testing).
*   **Latency Routing:** Directs users to the AWS region that provides them the absolute lowest latency.

### Amazon CloudFront (CDN)
*   Caches static and dynamic content globally at Edge Locations.
*   **Time To Live (TTL):** Dictates how long objects sit in the cache before CloudFront checks the origin.
*   **Origin Access Identity (OAI):** A virtual user identity. Locks down S3 buckets so users *must* go through CloudFront to access the files, preventing direct S3 access.
*   **Lambda@Edge:** Runs lightweight Node.js/Python functions natively at Edge Locations to manipulate HTTP requests dynamically before they hit the origin.

---

## 💾 35. Block, File, and Hybrid Storage
*   **EBS (Elastic Block Store):** Network-attached block storage for EC2. Replicated within a single AZ.
*   **Instance Store:** Extremely fast, physically attached ephemeral NVMe disks. Data is permanently lost if the instance stops or fails.
*   **EFS (Elastic File System):** NFS file storage supporting thousands of concurrent Linux instances across multiple AZs. 
*   **FSx for Windows File Server:** Fully native SMB/NTFS Microsoft file system supporting Active Directory.
*   **FSx for Lustre:** Posix-compliant high-performance file system dedicated to Machine Learning & HPC compute clusters. Native S3 integration.
*   **AWS Storage Gateway:** Bridges on-premises servers to AWS. Includes *File Gateway* (NFS/SMB to S3), *Volume Gateway* (iSCSI), and *Tape Gateway* (VTL physical tape replacement).

---

## 🐳 36. Containers (ECS & EKS)
*   **Amazon ECS (Elastic Container Service):** AWS-native container orchestration.
    *   **EC2 Launch Type:** You manage the underlying EC2 compute instances.
    *   **Fargate Launch Type:** Serverless natively. You only define CPU/RAM, AWS manages the underlying compute infrastructure.
*   **Amazon EKS (Elastic Kubernetes Service):** Managed upstream Kubernetes. Uses "Pods" instead of "Tasks". Highly extensible, steeper learning curve, industry standard.

---

## ⚡ 37. Serverless & Application Integration
### AWS Lambda
Serverless compute. Pay exclusively per millisecond. 
*   **Synchronous Invocations:** API Gateway waiting for a response.
*   **Asynchronous Invocations:** S3 Event drops, SNS notifications.
*   **Event Source Mapping:** Polling queues like SQS or Kinesis streams.

### SQS vs SNS vs EventBridge
*   **Amazon SQS (Simple Queue Service):** Pull-based message queuing. Standard (At-least-once, best-effort ordering) and FIFO (First-in-first-out, exactly-once processing).
*   **Amazon SNS (Simple Notification Service):** Push-based pub/sub. Fans out messages to thousands of subscribers (Email, SMS, Lambdas, SQS Queues).
*   **Amazon EventBridge (formerly CloudWatch Events):** Central enterprise event bus. Routes state changes (e.g., "EC2 instance terminated") natively across AWS to targets.

---

## 📊 38. Databases & Analytics 
*   **Amazon RDS:** Managed relational DBs (MySQL, PostgreSQL, SQL Server). Scales vertically. Multi-AZ provides Disaster Recovery. Read Replicas scale performance.
*   **Amazon Aurora:** Cloud-native relational DB. 5x faster than standard MySQL. Storage auto-scales to 128TB mathematically. Up to 15 Read Replicas with sub-millisecond lag.
*   **Amazon DynamoDB:** Fully managed, serverless NoSQL key-value database. Single-digit millisecond latency at any scale.
    *   *DynamoDB Streams:* Captures item-level changes natively in real-time, instantly triggering Lambda responses.
*   **Amazon Redshift:** Petabyte-scale SQL Data Warehouse (OLAP). Columnar storage optimized for vast analytical aggregations.
*   **Amazon ElastiCache:** Managed Redis & Memcached providing microsecond in-memory caching to slash database loads. 

### Big Data & Analytics Tools
*   **Amazon EMR:** Managed Hadoop/Spark clusters for massively parallel data processing.
*   **Amazon Athena:** Serverless interactive querying engine allowing standard SQL queries to run directly against raw CSV/JSON/Parquet files sitting in S3 without loading them.
*   **AWS Glue:** Managed serverless ETL (Extract, Transform, Load) service containing the Data Catalog.

---

## 🛠️ 39. Infrastructure as Code (IaC) & Deployment
*   **AWS CloudFormation:** Provisions infrastructure declaratively using JSON/YAML templates.
*   **AWS Elastic Beanstalk:** PaaS. You upload ZIP/code, AWS provisions the ALB, Auto Scaling, and EC2 nodes automatically.
*   **AWS Systems Manager (SSM) Parameter Store:** Hierarchical secure storage for configuration strings and encrypted secrets. No native automatic key rotation.
*   **AWS Secrets Manager:** Automatically rotates database passwords natively inside RDS securely.

---

## 🛡️ 40. Security & Threat Detection
*   **AWS KMS (Key Management Service):** Manages encryption Customer Master Keys (CMKs). Symmetric and Asymmetric. 
*   **AWS WAF (Web Application Firewall):** Layer 7 firewall filtering SQL injection and Cross-Site Scripting (XSS).
*   **AWS Shield:** Managed DDoS protection. Standard is free; Advanced costs $3,000/month providing financial threat coverage.
*   **Amazon Macie:** ML-powered engine scanning S3 specifically looking for unsecured PII (e.g., unencrypted Credit Card numbers).
*   **Amazon Inspector:** Installed on EC2 instances to scan for CVE software vulnerabilities and exposed ports dynamically.
*   **Amazon GuardDuty:** Intelligent threat detection silently analyzing CloudTrail, VPC Flow Logs, and DNS logs for compromised AWS accounts or crypto-mining malware natively.


---

## 🧪 41. Complete Hands-On Labs (HOL) Step-by-Step Guide
*Extracted directly from comprehensive test cases*

### 🛠️ Aws Account
- **Step:** AWS Account ➡ Account Root User(Full Control over Account) ➡ AWS IAM(Identity Access mgmnt) ➡ Manage(Users, Group, Roles, Policy)

### 🛠️ Configure Account Alias,Billing Alert
- **Step:** AWS mgmnt console ➡ select region ➡ Security,Identity & Compliance ➡ IAM ➡ Account ID same as Account Alias ➡ create Account Alias to remember ➡ Billing Preferences ➡ Tick check box 1. Receive billing Alert etc.  ➡

### 🛠️ Adding Billing Alarm With Sns(Simple Notification Services) By Cloudwatch(It Is Performance Monitoring Service)
- **Step:** AWS mgmnt console ➡ Management & Governance ➡ CloudWatch ➡ Alarm ➡ Billing ➡ Create Alarm ➡ Select Merics ➡ Billing ➡ Total Estimate charge ➡ select Currency(i.e USD) ➡ Select metrics ➡ Condition ➡ Select Greater > Threshold Amount(i.e $5.00) ➡ Next ➡ Select Alarm state trigger ➡ Select Create new topic ➡ Next ➡ Alrm Name & description ➡ Next ➡ Create Alrm Finished ➡ Click on the email box and confirm Subscription for Alarm noticfication for Billing.

### 🛠️ Create Iam User Account
- **Step:** users ➡ Add user ➡ User Name ➡ Tick checkbox:AWS mgmnt Console Access ➡ Console Password ➡ Next:permission ➡ Add group ➡ Group Name ➡ Assign Policy to group:AdministratorAccess ➡ create Group ➡ User Will Added to the Group ➡ Next:Tag ➡ Next:Review ➡ Create user ➡ Close ➡ Finished

### 🛠️ Enable Mfa(Multi Factor Authentication)
- **Step:** IAM console ➡ user ➡ Select User Account ➡ Security Credentials ➡ Assigned MFA devices:Manage ➡ Select Virtual MFA device ➡ Download & Open Google Authenticator App in mobile ➡ Scan QR code or type the secret Key ➡ Type 2 consecutive MFA code ➡ Assign MFA ➡ Finished

### 🛠️ Iam Password Policy
- **Step:** IAM console ➡ account settings ➡ change password policy ➡ Set Password Policy:Check Box as Requirement ➡ Save Changes ➡ Finished

### 🛠️ Create Ec2 Instnace
- **Step:** AWS Console ➡ EC2 mgmnt Console ➡ Select Region ➡ Click Launch Instance ➡ Choose AMI(Amazon Machine Image) ➡ Choose Instance Type(Size&Hardware Configuartion etc.) ➡ Configure instance detail ➡ next:Add Storage ➡ select volume type ➡ Next:Add Tag ➡ Next:Configure Security Group ➡ Create New key Pair and download ➡ Launch Instance ➡ View instnace ➡ Finished

### 🛠️ How To Connect Rdp Server Ec2 Instnace
- **Step:** AWS Console ➡ Select Windows server EC2 instnace ➡ connect ➡ choose RDP client ➡ get password ➡ upload key pair file(.pem) associated with the instance ➡ decrypt password by AWS ➡ Copy the Password ➡ copy DNS name ➡ connect by RDP client in windows ➡ User Default(Administrator) ➡ Password ➡ connect ➡ finished

### 🛠️ How To Delete Ec2 Instnace
- **Step:** AWS Console ➡ select EC2 instance ➡ scroll down instnace state ➡ select Terminate instnace ➡ click on terminate ➡ Finished

### 🛠️ Create S3 Bucket And Access It From Ec2 Instance By Access Key
- **Step:** AWS Console ➡ create s3 bucket ➡ IAM ➡ users ➡ security credentials ➡ create access key ➡ Download .csv file ➡ note somewhere Access key ID and Access key ➡ Launch EC2 Instance ➡ command:aws configure ➡ pass the Access key ID. acccess key value and Default-region-name ➡ finished

### 🛠️ Create Role Access Resource By Ec2 Instnace
- **Step:** AWS Console ➡ IAM ➡ Roles ➡ create role ➡ select AWS services ➡ comman use case:EC2(Allow EC2 instnaces to call aws services in your behaif) ➡ create policies according to the requirement ➡ Next tag ➡ next ➡ Add role Name ➡ Create Role ➡ Finsihed
- **Step:** AWS Console ➡ EC2 instnace ➡ select instance ➡ action ➡ security ➡ modify IAM role ➡ Select the role whatever we created for access resource ➡ Save ➡ finished

### 🛠️ Create Nat Gateway
- **Step:** AWS Console ➡ select region ➡ go to NAT gateway service ➡ Create NAT gateway ➡ Name/PublicSubnet/ConnectivityType:Public/ElasticIPAllocation ➡ Create ➡ finish
- **Step:** AWS Console ➡ go to route table of private subnet ➡ select subnet ➡ route ➡ edit route ➡ add route ➡ Destonation:0.0.0.0/0/Target:NAT gateway:nat-gw-id ➡ save changes.
- **Step:** There must be security group attched with subnet and also there must be an outbound rule for all trafic with destination address 0.0.0.0/0
- **Step:** This is only outbound access for NAT gateway you dont have any inbound access at all.

### 🛠️ Create Auto Scaling Group
- **Step:** EC2 management console ➡ Launch template ➡ create launch template ➡ View launch template ➡ finished
- **Step:** EC2 management console ➡ Create auto sca group ➡ Select Launch template created earlier ➡ next ➡ select purchase option ➡ select vpc ➡ select subnet ➡ next ➡ checkbox Enable group metrics collection within cloudwatch ➡ Next ➡ define desired,minimum,maximum capacity ➡ next ➡ next ➡ next ➡ Create Auto Scaling Group ➡ Finished

### 🛠️ Create A Target Group
- **Step:** AWS management console ➡ Region ➡ EC2 management console ➡ Select Target Group ➡ select instnace  ➡ for ALB(Https/HTTPS) or for NLB(TCP) ➡ select VPC ➡ next ➡ finished

### 🛠️ Create Nlb
- **Step:** EC2 Management Console ➡ Load Balancer ➡ Create Load Balancer ➡ Select NLB ➡ Add Diffrent Elastic IP to Subnet to NLB ➡ Add listner to Target Group ➡ finish

### 🛠️ Add Network Target Group To Auto Scaling Group
- **Step:** EC2 Management Console ➡ Auto scaling Group ➡ select Network target group ➡ edit ➡ select load balancer ➡ Select Target Group ➡ Update ➡ finish

### 🛠️ Create Alb
- **Step:** EC2 Management Console ➡ Load Balancer ➡ Create Load Balancer ➡ Select ALB ➡ Select VPC ➡ Add all subnet ➡ select security group ➡ Add listner to select application target Group ➡ close ➡ finish

### 🛠️ Add Application Target Group To Auto Scaling Group
- **Step:** EC2 Management Console ➡ Auto scaling Group ➡ select Application target group ➡ edit ➡ select load balancer ➡ Select Target Group ➡ Update ➡ finish

### 🛠️ Enable Sticky Session In Ec2 Instnace
- **Step:** EC2 management console ➡ target group ➡ select TG-ALB ➡ Attribute ➡ check stickiness:Stickiness Type:select Load Balancer generated cookies,Stickiness duration:1 days  ➡ Save ➡ finished

### 🛠️ Create Secure Listner For Elb(Ssl)
- **Step:** AWS Management console ➡ Certificate manager ➡ Provision authority:Get started ➡ Request a Public Certificate ➡ Add domain name(Get from Route 53) ➡ choose email validation ➡ next ➡ review ➡ confirm ➡ continue
- **Step:** EC2 Management Console ➡ load Balancer ➡ select load balancer ➡ listener ➡ add new listener ➡ Portocal:Https,port:443,Default Action : Forward to : select target group,Default SSl certificate:From ACM recommmneded:Select certificate which you created earlier ➡ Add listener ➡ finished
- **Step:** We need to add A-Name record for Load Balancer with Route53 DNS zone.

### 🛠️ Create Organization And Add Account
- **Step:** AWS management Console ➡ Services ➡ Management & Governace ➡ select AWS organization ➡ Create An organization ➡ Add Aws Account ➡ Account Name,Email Address,IAM role Name ➡ create AWS account ➡ finished

### 🛠️ Create Organization Unit(Ou)
- **Step:** AWS management Console ➡ Services ➡ Management & Governace ➡ select AWS organization ➡ select Root Account ➡ Actions ➡ Create New OU ➡ OU name ➡ Create OU ➡ Finished

### 🛠️ Move Account To Specific Ou
- **Step:** AWS management Console ➡ Services ➡ Management & Governace ➡ select AWS organization ➡ select AWS account ➡ Action ➡ Move ➡ OU Name where you want to move ➡ finished

### 🛠️ Attch Scp Policies To Aws Account
- **Step:** AWS management Console ➡ Services ➡ Management & Governace ➡ select AWS organization ➡ select AWS account ➡ policies ➡ Attach ➡ Select SCP policies ➡ Attach Policy ➡ Finished

### 🛠️ Vpc Wizard
- **Step:** It helps to design VPC network with default template and configuration
- **Step:** AWS management console ➡ service ➡ Networking & Content Delivery ➡ VPC ➡ Launch VPC wizard ➡ Select configuration as requirement ➡ Fill detail ➡ create/save ➡ finished

### 🛠️ Create Custom Vpc With Public And Private Subnet
- **Step:** VPC management Console ➡ your VPC ➡ create VPC ➡ Name,CIDR block,Tenancy:Default ➡ Create VPC ➡ create ➡ Finished

### 🛠️ Create Public And Private Subnet In Vpc
- **Step:** VPC management Console ➡ Subnet ➡ create Subnet ➡ Select VPC ID,Subnet Name,Availability Zone,IPv4 CIDR Block ➡ create ➡ Finished

### 🛠️ Assign Public Ip To Public Subnet
- **Step:** VPC management Console ➡ Subnet ➡ select public subnet ➡ Action ➡ modify auto-assign IP setting ➡ checkbox Enable auto-assign public IPv4 Address ➡ Save ➡ finished

### 🛠️ Create Route Table For Private Subnet
- **Step:** There always is main route table Exist in VPC.
- **Step:** We explicitly assign subnet to new Route Table.It is called Explicit Subnet Association
- **Step:** VPC management Console ➡ Route Table ➡ Create route Table ➡ Name,VPC ID ➡ Create Route Table ➡ Finished
- **Step:** VPC management Console ➡ Route Table ➡ select Route Table ➡ subnet association ➡ Edit Subnet association ➡ Select subnet w/o Elatsic Public IP ➡ save association ➡ finished

### 🛠️ Create Internet Gateway In Vpc
- **Step:** VPC management Console ➡ Internet Gateway ➡ create internet gateway ➡ Name ➡ Create Internet Gateway ➡ finished
- **Step:** VPC management Console ➡ Internet Gateway ➡ select internet gateway ➡ action ➡ attach to VPC ➡ Select VPC ID ➡ Attach internet Gateway ➡ finished
- **Step:** VPC management Console ➡ Route Table ➡ select Main Route Table ➡ Routes ➡ Edit route ➡ Add route ➡ Destonation:0.0.0.0/0,Target:select Internet gateway ID ➡ save chnages ➡ finished

### 🛠️ Private Access Of Vpc Subnet To Internet By Nat Gateway
- **Step:** VPC management Console ➡ NAT gateway ➡ Create NAT gateway ➡ Name,select Public Subnet Having Elastic Public IP,Connectivity type:Public,Allocate elastic ip ➡ Create NAT gateway ➡ finished
- **Step:** VPC management Console ➡ Route Table ➡ select private Route Table ➡ routes ➡ edit routes ➡ Add route ➡ Destonation:0.0.0.0/0,Target:select NAT gateway ID ➡ save changes ➡ finished

### 🛠️ Configure Vpc Peering Between Two Vpc With Existing In Two Diffrent Account
- **Step:** VPC management Console ➡ create peering connection ➡ Name,select Local VPC peer ID,Select account if Another VPC exist in another account:Account ID,VPC ID ➡ Create Peering connection ➡ finished
- **Step:** Go to another Account ➡ VPC management Console ➡ peering connection ➡ select peering reuest ➡ action ➡ accept the request ➡ finished

### 🛠️ Create Vpc Flow Logs
- **Step:** AWS management Console ➡ services ➡ cloudwatch ➡ logs ➡ select log groups ➡ create log group ➡ name,retention period:5 days ➡ create ➡ finished
- **Step:** Create IAM role for logs ➡ EC2 Management Console ➡ Network interface ➡ select Network interface ➡ flow logs ➡ create flow logs ➡ name,Choose destination log group,choose IAM role ➡ create flow logs finished
- **Step:** AWS management Console ➡ services ➡ cloudwatch ➡ logs ➡ select log group ➡ select log stream ➡ see VPC network interface log data ➡ finished

### 🛠️ Create Amazon S3 Bucket
- **Step:** AWS management Console ➡ services ➡ storage ➡ s3 ➡ create bucket ➡ select aws region ➡ create bucket ➡ finished

### 🛠️ Define Properties For Object And Upload Files In S3 Bucket
- **Step:** S3 management console ➡ select Bucket ➡ upload files and folder ➡ go to properties ➡ select storage class ➡ upload ➡ finished

### 🛠️ Define Permission To S3 File To Public Access
- **Step:** S3 management console ➡ select Bucket ➡ permission ➡ block public access: off ➡ save ➡ select file(called key) ➡ permission ➡ ACL(Access Control List) ➡ grant access according to requirements ➡ save chnages ➡ finished
- **Step:** S3 management console ➡ select Bucket ➡ select file(called key) ➡ action ➡ make public ➡ finished

### 🛠️ Version And Replication Enabled
- **Step:** s3-management-console ➡ select bukcet ➡ properties ➡ enabled version ➡ finished
- **Step:** s3-management-console ➡ select bucket ➡ management ➡ create replication rule ➡ name,choose bucket,IAM rule:create IAM rule,select addition replication option as requirement ➡ save ➡ finished

### 🛠️ Lifecycle Rule For Manage Our Object In S3 Bucket
- **Step:** s3-management-console ➡ select bucket ➡ management ➡ create replication rule ➡ select life cycle rule action ➡ select approriate action properties according to requirement ➡ create rule ➡ finished

### 🛠️ Enforce Encryption In S3 Bucket
- **Step:** s3-management-console ➡ select bucket ➡ properties ➡ default encryption ➡ server side encryption ➡ Enable ➡ Encryption key type:AWS Key management Service key(SSE-KMS) ➡ AWS KMS key:AWS managed keys(AWS:S3) ➡ bucket key ➡ Enable ➡ save chnaages ➡ finished

### 🛠️ Enforce Encryption In S3 Bucket Object
- **Step:** s3-management-console ➡ select bucket ➡ upload data ➡ properties ➡ server side encryption setting ➡ server side encryption ➡ specify an encryption key ➡ Amazon S3 keys(SSE-S3) ➡ upload ➡ finished

### 🛠️ S3 Event Notifications Integrate With Amazon Simple Notification Service (Sns)
- **Step:** AWS-management-console ➡ services ➡ Application intergration ➡ select SNS ➡ search ➡ MyEmailNotification ➡ create topic ➡ Standard ➡ define access policy json for S3 bucket ➡ create topic ➡ Subscription ➡ create subscription ➡ Topic ARN,Protocol:Email,Endpoint:Email ➡ create subscription ➡ finished
- **Step:** S3-management-console ➡ bucket ➡ select bucket ➡ properties ➡ Event notification ➡ Event Name ➡ Event Type:Select As requirement ➡ Destination ➡ select SNS topic ➡ Specify SNS topic:SNS Topic Name ➡ save changes ➡ finished

### 🛠️ Enable Server Access Logging In S3 Bucket
- **Step:** S3-management-console ➡ bucket ➡ properties ➡ Server access logging ➡ choose Edit ➡ select Enable ➡ Target bucket ➡ Save changes ➡ finished

### 🛠️ S3 Static Website
- **Step:** S3-management-console ➡ bucket ➡ properties ➡ Static website hosting ➡ edit ➡ enable ➡ give index.html,error.html ➡ save chnages ➡ finished

### 🛠️ Register Domain With Route 53
- **Step:** AWS-Management-console ➡ services ➡ Networking and Content delivery ➡ Route 53 ➡ register Domain ➡ choose domain name:sawan.com ➡ add to cart ➡ continue ➡ Registrant Contact information fill ➡ complete order ➡ finished
- **Step:** Route53-management-console ➡ Hosted zones ➡ you will see the list of domain name zone here.

### 🛠️ Enable Routing Policies
- **Step:** Route53-management-console ➡ Hosted Zone ➡ select domain name ➡ Create record ➡ Recore type:A ➡ VAlue:Ip address ➡ Routing Policy as requirement->create record ➡ finished

### 🛠️ Cloudfront And Distribution
- **Step:** AWS-management-console ➡ services ➡ Amazon cloud front ➡ create distribution ➡ Origin Domain Name ➡ fill details as requirement ➡ create ditribution ➡ finished

### 🛠️ Create Aws Global Accelerator
- **Step:** AWS-management-console ➡ Global Accelerator ➡ select accelerator ➡ listeners ➡ select listener ➡ add endpoint group ➡ finished

### 🛠️ Ec2 Image Builder
- **Step:** EC2-management-console ➡ EC2 Image builder ➡ Create Image pipeline ➡ name,Build schedule:Manual ➡ Next ➡ Recipe:Create New recipe ➡ Select Recipe details ➡ Image Type:AMI ➡ Image Name,Version ➡ Select image ➡ source managed images:Amazon linux ➡ Images Name:As architecture ➡ Select component for build as requirement ➡ Genral Informtion ➡ Name,Infrastructure,VPC etc ➡ next ➡ next ➡ create pipeline ➡ finished

### 🛠️ Create Efs Filesystem
- **Step:** NFS port range - 2049
- **Step:** EFS must be in the same VPC of Instance which you are going to mount or connect
- **Step:** AWS-management-console ➡ services ➡ storage ➡ EFS ➡ create a file system ➡ Name,VPC,regional/One Zone ➡ customize ➡ next ➡ Network Acess ➡ Specify correct security group ➡ next ➡ define or select policy option ➡ create ➡ finished

### 🛠️ Aws Backup
- **Step:** Schedule and backup for mutiple resources
- **Step:** AWS-management-console ➡ services ➡ AWS backup ➡ Backup plan ➡ Select option- start with template ➡ fill details as requirement ➡ create plan ➡ finished
- **Step:** AWS-Backup ➡ backup-plan ➡ select plan ➡ Resource assignment ➡ assign resources ➡ finished

### 🛠️ Launch Task On Aws Fargate
- **Step:** - CLuster Defination
- **Step:** AWS-management-console ➡ services ➡ containers ➡ Elastic container service ➡ Create cluster ➡ select networking only ➡ Cluster Name ➡ Enable container Insight ➡ create Cluster ➡ finished

### 🛠️ Deploy Ecs Cluster (Ec2 Launch Type)
- **Step:** - CLuster Defination
- **Step:** ECS-Management-console ➡ create cluster ➡ EC2 linux+Networking ➡ Next step ➡ Cluster Name,Size,Number of instance,volume,ssh key pair,Networking,enable container insight ➡ create ➡ finished

### 🛠️ Use Alb With Fargate Cluster
- **Step:** - Service creation
- **Step:** ECS-Management-console ➡ Cluster ➡ select cluster ➡ deploy ➡ Service,famile:task name,revision,desired task ➡ Load balancing ➡ application load balancer ➡ name,listener,port:80,protocol:http ➡ Target Group Name,Protocol:Http ➡ Healthcheck Path:/ ➡ Networking ➡ select VPC ➡ select Public Subnet ➡ select security group ➡ Enable Public IP assignment ➡ deploy ➡ finished

### 🛠️ Create Simple Lambda Function
- **Step:** AWS-management-console ➡ Services ➡ Compute ➡ Lambda ➡ create Function ➡ Select Author from Scratch ➡ Fucntion Name ➡ Runtime ➡ select Lnaguage to code ➡ Create new role with basic Lambda ➡ Create Function
- **Step:** Trigger is an event Source.
- **Step:** Desitination is the responce to send lambda function after successfull execution.
- **Step:** Lambda-Management-console ➡ select function ➡ code ➡ test ➡ New event,Template,hello ➡ Save chnages ➡ test
- **Step:** cloudwatch ➡ logs ➡ logs group ➡ select lambda function ➡ finished

### 🛠️ Create A State Machine By Step Function And Visulaize Workflow
- **Step:** AWS-management-console ➡ services ➡ appli Invocations ➡ AWS step function ➡ Get started ➡ Definaton in Json ➡ next ➡ start Execution ➡ Name,input:{"IsHelloWorldExample: true"} ➡ start execution ➡ you can see workflow in realtime ➡ finished

### 🛠️ Create Aws Step Function State Machine With Lambda
- **Step:** AWS-management-console ➡ service ➡ EC2 ➡ Create lambda function ➡ create state machine ➡ write workflow in code select ➡ create ➡ finished

### 🛠️ Create Event Bus And Rule That Take Ec2 Instance Chnages By Terminated And Update By Event Bus To Email Service
- **Step:** AWS-management-console ➡ amazon event bridge ➡ Events ➡ rules ➡ Create rule ➡ Name,Event pattern:pre-defined pattern by service,service provider:AWS,service Name:EC2,Events:EC2 Instance state-chnage notification,specific state:terminated,specific intance-ID:EC2 instnace ID ➡ Target ➡ SNS Topic,Topic:MyEmail notification ➡ create ➡ finished

### 🛠️ Structure Of A Rest Api
- **Step:** WEbApp ➡ Published API ➡ HTTP Method Request ➡ Integration Request ➡ EndPoint ➡ Convert Pass through ➡ HTTP STATUS CODES RESPONSE BODIES ➡ WEbApp
- **Step:** HTTP Method Request - ANY,DELETE,GET,HEAD,OPTIONS,PATCH,POST,Put
- **Step:** Integration Request - Map the request parameters of method request to the format required by the backend
- **Step:** EndPoint - Lambda function, HTTP endpoint, EC2 instance, AWS service etc.
- **Step:** HTTP STATUS CODES RESPONSE BODIES - Map the status codes, headers, and payload received from backend into format for client

### 🛠️ Create Simple Rest Api
- **Step:** AWS-management-console ➡ services ➡ API Gateway ➡ Select Rest API ➡ choose protocol:rest ➡ Create New Api:Example API ➡ EndPoint Type:Regional ➡ Import ➡ finished

### 🛠️ Web App With Http Api
- **Step:** AWS-management-console ➡ Services ➡ Management and Governance ➡ cloudformation ➡ create stck ➡ Prerequisite - Prepare Template:Template is Ready ➡ Specify template:upload a template file:choose file from local system ➡ select template.yaml file ➡ upload ➡ View in desgner ➡ create stack ➡ next ➡ stack name:any name ➡ next ➡ next ➡ create stack ➡ finished
- **Step:** create s3 bucket ➡ enable static website ➡ finished
- **Step:** AWS-management-console ➡ API gateway ➡ select API ➡ select Stages ➡ create stage ➡ Name:prod ➡ create ➡ finished
- **Step:** AWS-management-console ➡ API gateway ➡ integration ➡ manage integration ➡ create new ➡ Integration type:Lambda function ➡ select region and lambda function ➡ create ➡ finished
- **Step:** copy integraton ID : 7679fdsvbfjk
- **Step:** AWS-management-console ➡ API gateway ➡ route ➡ create ➡ Route and Method:GET,/api ➡ select API Method ➡ attach integration ➡ chhose one with integration ID ➡ finished
- **Step:** AWS-management-console ➡ API gateway ➡ cors ➡ configure cors ➡ Access-control-allow-origin:https://URlofbucketname.s3.amazon.com ➡ Access-control-allow-header:* ➡ access-control-allow-method:* ➡ access-control-expose-header:* ➡ access-control-max-age:96400 ➡ Access-control-allow-credentials:Yes ➡ save ➡ deploy ➡ select stage ➡ finished

### 🛠️ Delete Infra
- **Step:** AWS-management-console ➡ Services ➡ Management and Governance ➡ cloudformation ➡ select stack ➡ delete ➡ finished

### 🛠️ Create Amazon Rds Database
- **Step:** AWS-management-console ➡ services ➡ amazon RDS ➡ database ➡ create database ➡ standard ➡ mysql ➡ pricing tier ➡ master name ➡ password ➡ DB instnace class ➡ sizing and infra ➡ multi-Az ➡ default VPC ➡ public Access:No ➡ password authentication ➡ backup & maintennace windows option ➡ finished

### 🛠️ Read Replicas And Multi-Az
- **Step:** Amazon-RDS-console ➡ select database ➡ action ➡ create Read replicas ➡ create read replicas ➡ finished

### 🛠️ Create Encrypted Copy Of Rds Database And Restore It
- **Step:** Amazon-RDS-console ➡ snapshots ➡ select unencrypted snapshot ➡ action ➡ copy ➡ Enable Encryption ➡ AWS KMS key ➡ copy snapshot ➡ action ➡ restore ➡ encrytion windows enabled automatically ➡ restore DB instance ➡ finished

### 🛠️ Create Elasticache Cluster Redis
- **Step:** AWS-management-console ➡ services ➡ elasticcache dashboards ➡ get started now ➡ redis ➡ cluster mode enabled:NO ➡ amazon cloud ➡ create ➡ finished

### 🛠️ Create Dynamodb Table
- **Step:** AWS-management-console ➡ services ➡ dynamoDB ➡ create table ➡ tableName ➡ partition key ➡ sort key ➡ capacity calculator ➡ read/write capacity setting ➡ encryption at rest ➡ Owned by amazon DynamoDB ➡ create table ➡ finished

### 🛠️ Create And Store Data By File
```bash
aws dynamoDB batch-write-item --request-items file://mystore.json(local system path)
```

### 🛠️ Create Dynamodb Global Table
- **Step:** dynamoDB-management-console ➡ select table ➡ select global table ➡ create replica ➡ available replication region ➡ create replica ➡ finished

### 🛠️ Query S3 Alb Access Logs With Athena
- **Step:** AWS-management-console ➡ Services ➡ ec2 instance ➡ ALB ➡ select ALB ➡ action ➡ edit attribute ➡ access log S3 location ➡ select create location for me ➡ go to S3 location ➡ download the access logs
- **Step:** AWS-management-console ➡ service ➡ Amazon ethena ➡ get started ➡ set query result location in S3 ➡ create table with logs column ➡ select SQL query to get result ➡ finished

### 🛠️ Deploy Stack And Chnage Set
- **Step:** AWS-management-console ➡ services ➡ Management and Governance ➡ cloudFormation ➡ create stack ➡ use-current-template ➡ upload template file(json and yaml) ➡ select file ➡ next ➡ stack name ➡ paramter file window ➡ next ➡ next ➡ create stack ➡ finished

### 🛠️ Update Stack
- **Step:** AWS-management-console ➡ services ➡ Management and Governance ➡ cloudFormation ➡ select stack ➡ Stack Action ➡ create chnage set of current stack ➡ replace current template ➡ upload file ➡ select file ➡ next ➡ next ➡ create chnage set ➡ it will show chnages ➡ if you satisfied ➡ execute ➡ it will update the stack ➡ finished

### 🛠️ Deploy Elastic Beanstalk Web Server And Worker
- **Step:** AWS-management-console ➡ services ➡ EC2 ➡ Elastic Beanstack ➡ create an application ➡ aoolication name:myapp ➡ Platform:Node.js ➡ configure more option ➡ preset:high Availability ➡ create app ➡ finished

### 🛠️ Aws Config Rule With Remediation
- **Step:** AWS-management-console ➡ services ➡ Management and Governace ➡ config ➡ rules ➡ add rule ➡ select AWS managed rule ➡ next ➡ add rule ➡ finished

### 🛠️ Share A Subnet Across Accounts
- **Step:** AWS-management-console ➡ services ➡ Resorce Access manager console ➡ setting ➡ settings ➡ Checkbox:Enable sharing with AWS organization ➡ save settings ➡ finished
- **Step:** AWS-management-console ➡ services ➡ Resorce Access manager console ➡ Resource Share ➡ Name ➡ Select Resource Type ➡ choose id of resource ➡ next ➡ next ➡ Allow sharing with principals in organization only ➡ select accoubt from AWS organization display structure ➡ next ➡ create Resource share ➡ finished

### 🛠️ Create A Custom Metric With Command Line
```bash
#PutMetricData CLI command
aws cloudwatch put-metric-data --metric-name bytes --namespace MyCustomNameSpace --unit Bytes --value 242678092 --dimensions InstanceId=i-dshfdfh4785437,InstanceType=t2.micro --region us-east-1

aws cloudwatch put-metric-data --metric-name latency --namespace MyCustomNameSpace --unit Milliseconds --value 24 --dimensions InstanceId=i-dshfdfh4785437,InstanceType=t2.micro --region us-east-1
```

### 🛠️ Create Cloudwatch Alarm
- **Step:** cloudwatch-management-console ➡ all-alarms ➡ create-alarm ➡ select-metric ➡ mycostomnamespace ➡ InstanceId,InstanceType ➡ select metrics ➡ select configuartion as reuirement ➡ next ➡ EC2-action ➡ In alarm ➡ Terminate this instance ➡ Next ➡ Alarm Name ➡ finished

### 🛠️ Create A Cloudtrail Trail
- **Step:** AWS-management-console ➡ services ➡ Management&Governace ➡ AWS-cloudtrail ➡ create a trail ➡ storage location ➡ crate S3 bucket ➡ Trail log bucket & filetr ➡ Enable Cloudwatch log ➡ log group New ➡ log group name ➡ next ➡ Select management event in event type ➡ api activity:read and write ➡ next ➡ create trail ➡ finished

### 🛠️ Create Eventbridge Rule For Cloudtrail Api Calls
- **Step:** Create Cloudtrail & Lambda Function first
- **Step:** AWS-management-console ➡ service ➡ Amazon EventBridge ➡ Events ➡ rules ➡ create rule ➡ name ➡ eventPattern ➡ pre-defined pattern by services ➡ select Event Bus:AWS default Event Bus,Enable the rule in selected event bus ➡ select target ➡ Lambda function ➡ select labda function name ➡ create ➡ finished
- **Step:** we can check in cloudwatch ➡ logs ➡ logsGroup ➡ select Log group ➡ select log stream ➡ log events info ➡ finished

### 🛠️ Create Encryption Key
- **Step:** AWS-management-console ➡ key-management-service(KMS) ➡ customer-managed-key ➡ create key ➡ configure key:key type:Symmetric ➡ KMS ➡ next ➡ aias ➡ next ➡ define-key-administrator-permission ➡ allow-key-administrator-to-delete-the-key ➡ next ➡ define key usage permission ➡ next ➡ finish ➡ finished

### 🛠️ Ssl/Tls Certificate In Acm
- **Step:** AWS-management-console ➡ service ➡ ACM ➡ request a certificate ➡ request public certificate ➡ request-certificate ➡ add domain name ➡ next ➡ DNS/email validation ➡ finished



---

## 📖 42. Deep Dive Reference Guide (Extracted Sections)
*Comprehensive notes extracted section-by-section*

#### learning or cheat sheet
https://digitalcloud.training/

AWS Account-->Account Root User(Full Control over Account)-->AWS IAM(Identity Access mgmnt)-->Manage(Users, Group, Roles, Policy)

#### AWS Region
select region i.e US East (N. Virginia) us-east-1
Region is the top most Hierchy of AWS.
All resources create under specific region only.

AWS mgmnt console-->select region-->Security,Identity & Compliance-->IAM-->Account ID same as Account Alias-->create Account Alias to remember-->Billing Preferences-->Tick check box 1. Receive billing Alert etc. -->

AWS mgmnt console-->Management & Governance-->CloudWatch-->Alarm-->Billing-->Create Alarm-->Select Merics-->Billing-->Total Estimate charge-->select Currency(i.e USD)-->Select metrics-->Condition-->Select Greater > Threshold Amount(i.e $5.00)-->Next-->Select Alarm state trigger-->Select Create new topic-->Next-->Alrm Name & description-->Next-->Create Alrm Finished-->Click on the email box and confirm Subscription for Alarm noticfication for Billing.

#### Cloud Shell data file stored in persistant storage of 1 Gb per region and 120 retention Days at last Active session
#### If you want to increase Persistant storage by AWS contact Support Team.
#### cloud shell data stored in $HOME_DIRECTORY Only.
#### For Reuse same storage you need to active or restart cloud shell with same region.
#### To persist data and save dont Delete $HOME_DIRECTORY from cloud shell logout/exit option.
### 🗂️ Aws Identity Access And Management
#### IAM is universal(Global) and does not apply to any regions.
#### API keys used to programmatic access only.
#### User - A ctaogory to assigned task.

#### Group - It is group of User for organized way for specific pupose or conditions.

#### Role - It is used for delegation and assumed.An identity has a specific permission.
Roles assumed by users,applications and services.

#### Policy - It is pricipal to assign allow to which action perform on resources by which user.
Policies are documents that define permissions and are written in Json.
All permission are implicitly denied by default for all resources except administrator access/Admin(Root) user.

Identity-based-Policy - Can be applied to user, group or role.

Resource-based-Policy - can be applied to resources such as S3 buckets or DynamoDB tables.

IAM Permission Boundaries - Set the maximum permission an identity-based policy can grant an IAM entity.

AWS organiztion service control policies - Specify the max. permission for an organization or Operation Unit(OU).

Session Policies - used with AssumeRole* API actions

#### Root User v/s IAM users
USER             |         Login Details                       |     Permission        |
Root User        |         @Email Address                      | Full Unretsricted     |
IAM User         |Friendly Name : Johhn + AWS A/c id or Alias  | IAM permission Policy |

users-->Add user-->User Name-->Tick checkbox:AWS mgmnt Console Access-->Console Password-->Next:permission-->Add group-->Group Name-->Assign Policy to group:AdministratorAccess-->create Group-->User Will Added to the Group-->Next:Tag-->Next:Review-->Create user-->Close-->Finished

IAM console-->user-->Select User Account-->Security Credentials-->Assigned MFA devices:Manage-->Select Virtual MFA device-->Download & Open Google Authenticator App in mobile-->Scan QR code or type the secret Key-->Type 2 consecutive MFA code-->Assign MFA-->Finished

#### AWS Security Service Token(STS)
Temporary security credentials are returned.
Temporary Credentials used with identity federation, delegation,cross-account access, and IAM Roles.
Credentials Include:
1. Access key ID
2. Expiration
3. SecretAccessKey
4. Session Token

IAM console-->account settings-->change password policy-->Set Password Policy:Check Box as Requirement-->Save Changes-->Finished

#### An IAM policy is  json document that consist of one or more statement
{
"Statement":[{
"Effect" : "effect",---------------------------->Element can 'Allow' or 'Deny'
"Action" : "action",---------------------------->Specific api action for which you are granting and denying permission
"Resource" : "arn(aws resource name",----------->Resource that affected by action
"Condition" :{
"Key" : "value"------------------------->Optional & can be used to control when your policy is in effect
}
}]
}

#### IAM Policy Simulator--> used to check and know about access of resources and restriction on API action
### 🗂️ Amazon Elastic Compute Cloud
#### EC2 instnces have various virtualization server with different os i.e windows,linux and Mac OS

#### Launching EC2 instnace in public Subnet(Means connect instnace from public internet)
Region HAVE vpc|vpc HAVE availablity zone|Availablity zone HAVE public subnet|Launch EC2 Instance in public Subnet

#### DATA is stored in EBS volume in EC2(Virtual Hard drives)

#### A security Group control inbound and outbound traffic

#### The internet Gateway enable Access to/from internet located at VPC layer

#### EC2 Inatance type and Size diffrentiate depends on memory specially with respect to usage purpose also

AWS Console-->EC2 mgmnt Console-->Select Region-->Click Launch Instance-->Choose AMI(Amazon Machine Image)-->Choose Instance Type(Size&Hardware Configuartion etc.)-->Configure instance detail-->next:Add Storage-->select volume type-->Next:Add Tag-->Next:Configure Security Group-->Create New key Pair and download-->Launch Instance-->View instnace-->Finished

AWS Console-->Select Windows server EC2 instnace-->connect-->choose RDP client-->get password-->upload key pair file(.pem) associated with the instance-->decrypt password by AWS-->Copy the Password-->copy DNS name-->connect by RDP client in windows-->User Default(Administrator)-->Password-->connect-->finished

AWS Console-->select EC2 instance-->scroll down instnace state-->select Terminate instnace-->click on terminate-->Finished

#### EC2 metadata is data about your instnace it is access from the instance only
Instnace metadata is available at http://169.254.169.254/latest/meta-data

#### Launch EC2 instnace with user data and meta data
Write script or file limited to 16kb while launching instnace it will immediate run first at after instance

#### Accessing services - Access Keys and IAM roles
#### Access keys used to access resources from AWS by command line

#### configure the aws credentials in cmd
aws configure

AWS Console-->create s3 bucket-->IAM-->users-->security credentials-->create access key-->Download .csv file-->note somewhere Access key ID and Access key-->Launch EC2 Instance-->command:aws configure-->pass the Access key ID. acccess key value and Default-region-name-->finished

#### to check all s3 bucket list
aws s3 ls

#### to check file in bucket
aws s3 ls s3://bucket-name

#### Access key and id store in crednetials file in .aws root directory
cd ~/.aws
ls---->o/p config credentials
cat credentials-->o/p aws_access_key_id=<YOUR_ACCESS_KEY_ID> , aws_secret_access_key=<YOUR_SECRET_ACCESS_KEY>

AWS Console-->IAM-->Roles-->create role-->select AWS services-->comman use case:EC2(Allow EC2 instnaces to call aws services in your behaif)-->create policies according to the requirement-->Next tag-->next-->Add role Name-->Create Role-->Finsihed

AWS Console-->EC2 instnace-->select instance-->action-->security-->modify IAM role-->Select the role whatever we created for access resource-->Save-->finished

#### Status check and Monitoring available at CloudWatch service under management and Governance

#### Network Interface(ENI[Elastic Network Interface],ENA[Elastic Network Adapter] & EFA[Elastic febri adapter])
ENI - Use with all instance, Not used for High Peformance Requirement
ENA - Supported Instance type, Enhanced networking performance, Higher bandwidth and lower inter-instance latency
EFA - use with all instance type, HPC(High Peformance Computing), MPI(Msg passing Interface) and ML use cases, Tightly Coupled  Application

#### EIP(Elastic IP)
It is static IP.
we can move or remapped ENI & EIP to different instnaces.
It can be remapped across Availablity zone also.
Associate with a private IP of instance.
You are charged if not used.
We can create and associate it with Network interface and instnace.

#### Public IP
Lost when the instance is stopped but not in reboot or restart. It is dynamic.
Used in public subnet.
No charge.
Associate with the private IP of instance.
Cannot be moved between instnaces.

#### private IP
Retained when the instance is stopped.
Used in public or private subnet.

#### NAT(Network Address translation for PublicIP address
Internet Gateway(IGW) perform NAT.

#### private subnet
There is one address prefix(173.23.0.0/16) associate with it.
Route table help to intercommunication between the network.

#### public subnet/Bastion host
There is two address prefix associate with it.
173.31.0.0/16 - local subnet prefix route table for intercommunication
0.0.0.0/0 - igw-id subnet prefix route table for communication with public internet by internet gateway

#### subnet count by default
Each VPC has total number of subnet depends on the availablity zone in region i.e N. Virginia - 6 subnet & 6 availablity zone
Each VPC has separte Route table with associate address prefeix.

#### NAT gateway to access private subnet
The NAT gateway always created in the public subnet only
Add the 0.0.0.0/0 address as NAT gatewayID must be specified in private subnet route table
NAT Gateway provide high availablity and automatic scaling.

AWS Console-->select region-->go to NAT gateway service-->Create NAT gateway-->Name/PublicSubnet/ConnectivityType:Public/ElasticIPAllocation-->Create-->finish

AWS Console-->go to route table of private subnet-->select subnet-->route-->edit route-->add route-->Destonation:0.0.0.0/0/Target:NAT gateway:nat-gw-id-->save changes.

There must be security group attched with subnet and also there must be an outbound rule for all trafic with destination address 0.0.0.0/0

This is only outbound access for NAT gateway you dont have any inbound access at all.

#### EC2 billing
linux Ubuntu --> billed per second basis minimum per minute billing
Windows/RHEL/CENTOS -- > Billed per hour basis minimum 1 hour billing

#### EC2 Pricing Use cases Type
1.On-demand 2.Reserved 3.Scheduled Reserved 4.Spot Instance 5.Dedicated Instance 6.Dedicated Hosts

#### amazon EC2 auto Scaling
ec2 instance always keep inside auto scaling group.
Cloudwatch moniter the metrics frequently and notifies schedular to auto scale at threshold metrics limit reached.
It is an Horizontal scaling(Scale Out).

#### configuration of an auto scaling group
Launch Template - It specified the EC2 instance configuration
Configure VPC,subnet ,EC2 instnace and attch load balancer - configure health check EC2 and ELB(elastic Load Balancer)
Cooldown  default value is 300sec(5min).

EC2 management console-->Launch template-->create launch template-->View launch template-->finished

EC2 management console-->Create auto sca group-->Select Launch template created earlier-->next-->select purchase option-->select vpc-->select subnet-->next-->checkbox Enable group metrics collection within cloudwatch-->Next-->define desired,minimum,maximum capacity-->next-->next-->next-->Create Auto Scaling Group-->Finished

#### Load Balancing and High Availablity & Fault tolerance(Component failure in Instnace)
Load Balancing help to high availablity as well as fault tolerance.

#### Types of ELB(Elastic Load Balancer)
- Application Load Balancer
Operates at the request level
Routes based on the content of the request (layer 7)
Supports path-based routing, host-based routing, query string
parameter-based routing, and source IP address-based routing
Supports instances, IP addresses, Lambda functions and
containers as targets

- Network Load Balancer
Operates at the connection level
Routes connections based on IP protocol data (layer 4)
Offers ultra high performance, low latency and TLS offloading at scale
Can have a static IP / Elastic IP
Supports UDP and static IP addresses as targets

-Gateway Load Balancer
Used in front of virtual appliances such as firewalls, IDS(Intrusion detection systems)/IPS(intrusion prevention system),and deep packet inspection systems.
Operates at Layer 3 – listens for all packets on all ports
Forwards traffic to the TG specified in the listener rules
Exchanges traffic with appliances using the GENEVE protocol on port 6081

AWS management console-->Region-->EC2 management console-->Select Target Group-->select instnace -->for ALB(Https/HTTPS) or for NLB(TCP)-->select VPC-->next-->finished
### 🗂️ Network Load Balancer
#### Create Elastic IP
EC2 Management Console-->create Elastic IP(for allocate to NLB)

EC2 Management Console-->Load Balancer-->Create Load Balancer-->Select NLB-->Add Diffrent Elastic IP to Subnet to NLB-->Add listner to Target Group-->finish

EC2 Management Console-->Auto scaling Group-->select Network target group-->edit-->select load balancer-->Select Target Group-->Update-->finish
### 🗂️ Application Load Balancer
EC2 Management Console-->Load Balancer-->Create Load Balancer-->Select ALB-->Select VPC-->Add all subnet-->select security group-->Add listner to select application target Group-->close-->finish

EC2 Management Console-->Auto scaling Group-->select Application target group-->edit-->select load balancer-->Select Target Group-->Update-->finish

#### Amazon EC2 scaling policies
AWS recommmneded scaling on metrics with a 1 minute Frequency.
We need to enable Monitoring for enable Scaling policies and EC2 instnaces.

Dynamic Scaling -
Target Tracking :(ASGAverageCPUUtilization(Avg CPU utilisation of Target Group)=60% then launch new instnace)

Simple Scaling  :(Auto scaling group Alarm set to cpu >= 60% then launch 2 instnace)

Step Scaling    : (Auto scaling group Alarm set to cpu >= 60% if CPU go 70% then launch 2 instance, elif CPU go 80% then launch 4Instnace launch)

Scheduled Scaling - Scheduled set to scale at 4:00PM on specific time launch X instnaces as desired,min,max count.

#### Cross Zone Load Balancing
It is a Feature of Elastic Load Balancer.
With Application Load Balancers, cross-zone load balancing is always enabled
With Network Load Balancers and Gateway Load Balancers, crosszone load balancing is disabled by default

- When cross-zone load balancing is enabled:
Each load balancer node distributes traffic across the registered targets in all enabled Availability Zones

- When cross-zone load balancing is disabled:
Each load balancer node distributes traffic only across the registered targets in its Availability Zone

EC2 management console-->target group-->select TG-ALB-->Attribute-->check stickiness:Stickiness Type:select Load Balancer generated cookies,Stickiness duration:1 days -->Save-->finished

AWS Management console-->Certificate manager-->Provision authority:Get started-->Request a Public Certificate-->Add domain name(Get from Route 53)-->choose email validation-->next-->review-->confirm--continue

EC2 Management Console-->load Balancer-->select load balancer-->listener-->add new listener-->Portocal:Https,port:443,Default Action : Forward to : select target group,Default SSl certificate:From ACM recommmneded:Select certificate which you created earlier-->Add listener-->finished

We need to add A-Name record for Load Balancer with Route53 DNS zone.
### 🗂️ Aws Organization
AWS organizations allows you to consolidate multiple AWS accounts into an organization that you create and centrally manage
Available in two feature sets:
- Consolidated Billing
- All features
Includes root accounts and organizational units
Policies are applied to root accounts or OUs
Consolidated billing includes:
- Paying Accounts – independent and cannot access resources of other accounts
- Linked Accounts – all linked accounts are independent
You can group account into Organization Units(OU)
SCP(Services control Policies) - It can control tagging and other avialble API action with the help of JSON policies structure
Create acoount programmatically using the organization API
Enable cloudTrail in management account and apply to members.

AWS Organization-------------
|
Management Accounts(Receive Consolated Billing of All child Account)
|
|                    |                  |                   |
|                    |                  |                   |
QA A/C            TEST A/C             Dev A/c           Prod A/c

AWS management Console-->Services-->Management & Governace-->select AWS organization-->Create An organization-->Add Aws Account-->Account Name,Email Address,IAM role Name-->create AWS account-->finished

AWS management Console-->Services-->Management & Governace-->select AWS organization-->select Root Account-->Actions-->Create New OU-->OU name-->Create OU-->Finished

AWS management Console-->Services-->Management & Governace-->select AWS organization-->select AWS account-->Action-->Move-->OU Name where you want to move-->finished

AWS management Console-->Services-->Management & Governace-->select AWS organization-->select AWS account-->policies-->Attach-->Select SCP policies-->Attach Policy-->Finished
### 🗂️ Amazon Vpc
It is a logically  isolated virtual network in AWS cloud within a region.
It is a private space for your services and full control over it with configuration.
Subnet created within availablity Zone only.
By default we can create 5 VPC per region.
An Internet Gateway is attched to VPC and used to connect with internet.

#### VPC Router
Cant visible but exist. It take care of routing within the VPC and outside the VPC.
We can see the route table which configured route network for the VPC for you and used in VPC router.

#### peering Connection
direct connection and cummunication between two VPC network.

#### Subnet
A segment of a VPC’s IP address range where you can place groups of isolated resources.

#### Internet Gateway/Egress only
The Amazon VPC side of a connection to the public Internet for IPv4/IPv6

#### Router
Routers interconnect subnets and direct traffic between Internet gateways, virtual private gateways, NAT gateways, and subnets.

#### VPC Endpoints
Private connection to public AWS services.

#### NAT Instance
Enables Internet access for EC2 instances in private subnets managed by you)

#### NAT Gateway
Enables Internet access for EC2 instances in private subnets (managed by AWS)

#### Virtual Private Gateway
The Amazon VPC side of a Virtual Private Network (VPN) connection

#### Customer Gateway
customer side of a VPN connection.

#### AWS Direct Connect
High speed, high bandwidth, private network connection from customer to aws

#### Security Group
Instance level firewall

#### Network ACL
Subnet-level firewall

#### Defining VPC CIDR block - Rules & Guidelines
CIDR block size can be between /16 and /28
The CIDR block must not overlap with any existing CIDR block that's associated with the VPC
You cannot increase or decrease the size of an existing CIDR block
The first four and last IP address are not available for use
Ensure you have enough networks and hosts
Bigger CIDR blocks are typically better (more flexibility)
Smaller subnets are OK for most use cases
Consider deploying application tiers per subnet
Split your HA resources across subnets in different AZs
VPC Peering requires non-overlapping CIDR blocks
This is across all VPCs in all Regions / accounts you want to connect
Avoid overlapping CIDR blocks as much as possible!

It helps to design VPC network with default template and configuration

AWS management console-->service-->Networking & Content Delivery-->VPC-->Launch VPC wizard-->Select configuration as requirement-->Fill detail-->create/save-->finished

VPC management Console-->your VPC-->create VPC-->Name,CIDR block,Tenancy:Default-->Create VPC-->create-->Finished

VPC management Console-->Subnet-->create Subnet-->Select VPC ID,Subnet Name,Availability Zone,IPv4 CIDR Block-->create-->Finished

VPC management Console-->Subnet-->select public subnet-->Action-->modify auto-assign IP setting-->checkbox Enable auto-assign public IPv4 Address-->Save-->finished

There always is main route table Exist in VPC.
We explicitly assign subnet to new Route Table.It is called Explicit Subnet Association

VPC management Console-->Route Table-->Create route Table-->Name,VPC ID-->Create Route Table-->Finished

VPC management Console-->Route Table-->select Route Table-->subnet association-->Edit Subnet association-->Select subnet w/o Elatsic Public IP-->save association-->finished

VPC management Console-->Internet Gateway-->create internet gateway-->Name-->Create Internet Gateway-->finished

VPC management Console-->Internet Gateway-->select internet gateway-->action-->attach to VPC-->Select VPC ID-->Attach internet Gateway-->finished

VPC management Console-->Route Table-->select Main Route Table-->Routes-->Edit route-->Add route-->Destonation:0.0.0.0/0,Target:select Internet gateway ID-->save chnages-->finished

VPC management Console-->NAT gateway-->Create NAT gateway-->Name,select Public Subnet Having Elastic Public IP,Connectivity type:Public,Allocate elastic ip-->Create NAT gateway-->finished

VPC management Console-->Route Table-->select private Route Table-->routes-->edit routes-->Add route-->Destonation:0.0.0.0/0,Target:select NAT gateway ID-->save changes-->finished

#### Difference between Internet Gateway v/S NAT gateway
Internet gateway is used to connect a vpc to the internet
v/s
NAT gateway is used to connect the Private subnet to the internet(which means what ever traffic is coming to private subnet instance which will forward to the NAT gateway).
you need to forward the traffic in the route table to NAT Route table 0.0.0.0/0

Internet Gateways are attached to the VPC. You then need to add entries to the route tables for your public subnets to point to the IGW.

#### Security group and Network ACLs(Access controllers)
Security Groups can be applied to instances in any subnet.
v/s
NACLs apply only to traffic entering/exiting the subnet.

Security Groups apply at the Instance level.
v/s
NACLs apply at the Security Groups subnet level

Security Groups works in statefull(It allows returns traffic automatically) firewall.
v/s
NACLs works in stateless(It check for an allow rule for both in&out connection) firewall.

Security Groups only support allow rules only.
v/s
NACLs support both allow as well as explicit deny rule also.

VPC management Console-->create peering connection-->Name,select Local VPC peer ID,Select account if Another VPC exist in another account:Account ID,VPC ID-->Create Peering connection--finished

Go to another Account-->VPC management Console-->peering connection-->select peering reuest-->action-->accept the request-->finished

#### Configure VPC peering enable communication between two VPC network in Security Group
Allow connection from VPC Address/cidr with All port with ICMP protocol
Protocol         Port              Source
ICMP             All               10.1.0.0/16
TCP              22                0.0.0.0/0

#### Configure VPC peering enable communication between two VPC network in Route Table
Destination VPC address/CIDR of Other VPC Target as Peering ID.
Destination     Target         |  Destination              Target
10.0.0.0/16     peering-ID     |  10.0.1.0/16              peering-ID

#### VPC flow logs
Flow Logs capture information about the IP traffic going to and from network interfaces in a VPC
Flow log data is stored using Amazon CloudWatch Logs or S3
Flow logs can be created at the following levels:
- VPC
- Subnet
- Network interface

AWS management Console-->services-->cloudwatch-->logs-->select log groups-->create log group-->name,retention period:5 days-->create-->finished

Create IAM role for logs-->EC2 Management Console-->Network interface-->select Network interface-->flow logs-->create flow logs-->name,Choose destination log group,choose IAM role-->create flow logs finished

AWS management Console-->services-->cloudwatch-->logs-->select log group-->select log stream-->see VPC network interface log data-->finished

#### AWS Direct Connect uses private network connections into the AWS Cloud and is high-bandwidth and low-latency. This is good for establishing hybrid cloud configurations.

#### By default, new subnets are associated with the default route table. You need to assign the new route table in order for the instances to see the route to the NAT gateway.

#### You should create multiple subnets each within a different AZ and launch EC2 instances running your application across these subnets.
### 🗂️ S3

Amazon S3 is a public service. It scope is global no region specific.

A bucket is a container for objects.

An object is a file you upload.

You can store millions of objects in a bucket.

The HTTP protocol is used with a REST API (e.g. GET, PUT, POST, SELECT, DELETE)

You can store any type of file in S3

Files can be anywhere from 0 bytes to 5 TB

There is unlimited storage available

S3 is a universal namespace so bucket names must be unique globally

However, you create your buckets within a REGION

It is a best practice to create buckets in regions that are physically closest to your users to reduce latency

There is no hierarchy for objects within a bucket

Delivers strong read-after-write consistency

Folders can be created within folders

Buckets cannot be created within other buckets

An objects consists of:
• Key (the name of the object)
• Version ID
• Value (actual data)
• Metadata
• Subresources
• Access control information

#### Accessing objects in a bucket where bucket(name),aws_region and key(file_name) is variable
https://bucket.s3.aws-region.amazonaws.com/key
https://s3.aws-region.amazonaws.com/bucket/key

EC2 instances connect using private addresses by S3 gateway Endpoint.

EC2 instances connect using public addresses.

User browses with a standard web browser.

Application uses REST API programmatically.

#### S3 Storage Class Use Cases
S3 Standard - Frequently accessed data; ad-hoc needs; short-term requirements (<30 days)

S3 Intelligent Tiering - automatic storage cost savings when data access patterns change, without performance impact or    operational overhead.

The Amazon S3 Intelligent-Tiering storage class is designed to optimize storage costs by automatically moving data to the most cost-effective access tier when access patterns change.

For a small monthly object monitoring and automation charge, S3 Intelligent-Tiering monitors access patterns and automatically moves objects that have not been accessed to lower-cost access tiers.

S3 Standard-IA - Require long-term storage for production data with low cost and immediate access for occasional requests

S3 One Zone-IA - Copy of backup data required in a separate Region with minimal access latency

S3 Glacier - Require for storage for Archiving file and access it.

S3 Glacier Deep Archive - Lowest cost required for long-term archival of data for compliance purposes

AWS management Console-->services-->storage-->s3-->create bucket-->select aws region-->create bucket-->finished

S3 management console-->select Bucket-->upload files and folder-->go to properties-->select storage class-->upload-->finished

#### Bucket Policies(Resource-based-Policy)
Can only be attached to Amazon S3 buckets.

Also use the AWS access policy language json format.

#### S3 Access Control Lists (ACLs)
Legacy access control mechanism that predates IAM.

AWS generally recommends using S3 bucket policies or IAM policies rather than ACLs.

Can be attached to a bucket or directly to an object.

Limited options for grantees and permissions.

#### When to use each access control mechanism
- Use IAM policies if:
You need to control access to AWS services other than S3

You have numerous S3 buckets each with different permissions requirements (IAM policies will be easier to manage)

You prefer to keep access control policies in the IAM
environment

- Use S3 bucket policies if:
You want a simple way to grant cross-account access to your S3 environment, without using IAM roles

Your IAM policies are reaching the size limits

You prefer to keep access control policies in the S3 environment

S3 management console-->select Bucket-->permission-->block public access: off-->save-->select file(called key)-->permission-->ACL(Access Control List)-->grant access according to requirements-->save chnages-->finished

S3 management console-->select Bucket-->select file(called key)-->action-->make public-->finished

#### S3 Versioning
Versioning is a means of keeping multiple variants of an object in the same bucket

Use versioning to preserve, retrieve, and restore every version of every object stored in your Amazon S3 bucket

Versioning-enabled buckets enable you to recover objects from accidental deletion or overwrite

#### S3 replication
CRR(cross-region-replication) - replication within buckets in diffrent region

SRR(same-region-replication) - replication within bucket in same region but may be different account

#### S3 Lifecycle Management
There are two types of actions:
- Transition actions - Define when objects transition to another storage class

- Expiration actions - Define when objects expire (deleted by S3)

#### S3 LM: Supported Transitions
- You can transition from the following:
The S3 Standard storage class to any other storage class

Any storage class to the S3 Glacier or S3 Glacier Deep Archive storage classes

The S3 Standard-IA storage class to the S3 Intelligent-Tiering or S3 One Zone-IA storage classes

The S3 Intelligent-Tiering storage class to the S3 One Zone-IA storage class

The S3 Glacier storage class to the S3 Glacier Deep Archive storage class

#### S3 LM: Unsupported Transitions
- You can't transition from the following:
Any storage class to the S3 Standard storage class

Any storage class to the Reduced Redundancy storage class

The S3 Intelligent-Tiering storage class to the S3 Standard-IA storage class

The S3 One Zone-IA storage class to the S3 Standard-IA or S3 Intelligent-Tiering storage classes

s3-management-console-->select bukcet-->properties-->enabled version-->finished

s3-management-console-->select bucket-->management-->create replication rule-->name,choose bucket,IAM rule:create IAM rule,select addition replication option as requirement-->save-->finished

s3-management-console-->select bucket-->management-->create replication rule-->select life cycle rule action-->select approriate action properties according to requirement-->create rule-->finished

#### S3 Multi-Factor Authentication Delete (MFA Delete)
- Adds MFA requirement for bucket owners to the following operations:
Changing the versioning state of a bucket

Permanently deleting an object version

The x-amz-mfa request header must be included in the above requests

The second factor is a token generated by a hardware device or software program

Requires versioning to be enabled on the bucket

- Versioning can be enabled by:
Bucket owners (root account)

AWS account that created the bucket

Authorized IAM users

- MFA delete can be enabled by:
Bucket owner (root account)

#### MFA-Protected API Access
Used to enforce another authentication factor (MFA code) when accessing AWS resources (not just S3)

Enforced using the aws:MultiFactorAuthAge key in a bucket policy:

Denies any API operation that is not authenticated using MFA

#### S3 Encryption
- Server-side encryption with S3 managed keys (SSE-S3)
S3 managed keys

Unique object keys

Master key

AES 256

- Server-side encryption with AWS KMS managed keys (SSE-KMS)
KMS managed keys

Customer master keys

CMK can be customer generated

- Server-side encryption with client provided keys (SSE-C)
Client managed keys

Not stored on AWS

- Client-side encryption
Client managed keys

Not stored on AWS

OR you can use a KMS CMK

s3-management-console-->select bucket-->properties-->default encryption-->server side encryption-->Enable-->Encryption key type:AWS Key management Service key(SSE-KMS)-->AWS KMS key:AWS managed keys(AWS:S3)-->bucket key-->Enable-->save chnaages-->finished

s3-management-console-->select bucket-->upload data-->properties-->server side encryption setting-->server side encryption-->specify an encryption key-->Amazon S3 keys(SSE-S3)-->upload--finished

#### S3 Event Notifications
Sends notifications when events happen in buckets

- Destinations include:
Amazon Simple Notification Service (SNS) topics

Amazon Simple Queue Service (SQS) queues

AWS Lambda

AWS-management-console-->services-->Application intergration-->select SNS-->search-->MyEmailNotification-->create topic-->Standard-->define access policy json for S3 bucket-->create topic-->Subscription-->create subscription-->Topic ARN,Protocol:Email,Endpoint:Email-->create subscription-->finished

S3-management-console-->bucket-->select bucket-->properties-->Event notification-->Event Name-->Event Type:Select As requirement-->Destination-->select SNS topic-->Specify SNS topic:SNS Topic Name-->save changes-->finished

#### S3 Presigned URLs
It is used to give access of object to user for sometime without enable s3 bucket or object publically

command:
aws s3 presign s3://<bucketName>/<filename> --expires-in time_in_seconds
aws s3 presign s3://dct-data-bucket/cool_image.jpeg --expires-in 60

Output as accessing URL:
https://my-bucket.s3.ap-southeast-2.amazonaws.com/cool_image.jpeg?X-Amz-Algorithm=AWS4-HMACSHA256&X-Amz-Credential=AKIAEXAMPLE12345678%2F20200909%2Fapsoutheast-2%2Fs3%2Faws4_request&X-Amz-Date=20200909T053538Z&XAmz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=REDACTED_SIGNATURE_VALUE

#### S3 Multipart Upload
Multipart upload uploads objects in parts independently, in parallel and in any order

Performed using the S3 Multipart upload API

It is recommended for objects of 100 MB or larger

Can be used for objects from 5 MB up to 5 TB

Must be used for objects larger than 5 GB

#### S3 Transfer Acceleration
CloudFront edge locations - CloudFront is made up of many edge locations. Each edge location is an Amazon datacenter (or colocation facility that has Amazon equipment somewhere in it), spread out all over the world for low latency. A request to a CloudFront endpoint goes to one of the edge locations closest to your current physical location

Uses CloudFront edge locations to improve performance of transfers from client to S3 bucket

Transfer Acceleration is enabled at the bucket level

AWS only charges if there’s a performance improvement

#### Server Access Logging
Provides detailed records for the requests that are made to a bucket

Details include the requester, bucket name, request time, request action, response status, and error code (if applicable)

Disabled by default

Only pay for the storage space used

Must configure a separate bucket as the destination (can specifya prefix)

Must grant write permissions to the Amazon S3 Log Delivery group on destination bucket

S3-management-console-->bucket-->properties-->Server access logging-->choose Edit-->select Enable-->Target bucket-->Save changes-->finished

S3-management-console-->bucket-->properties-->Static website hosting-->edit-->enable-->give index.html,error.html-->save chnages-->finished

#### CORS with Amazon S3
Allows requests from an origin to another origin

Origin is defined by DNS name, protocol, and port

- Enabled through setting:
• Access-Control-Allow-Origin
• Access-Control-Allow-Methods
• Access-Control-Allow-Headers

These settings are defined using rules

Rules are added using JSON files in S3

#### Cross Account Access Methods
Resource-based policies and IAM policies for programmatic-only access to S3 bucket objects

Resource-based ACL and IAM policies for programmatic-only access to S3 bucket objects

Cross-account IAM roles for programmatic and console access to S3 bucket objects
### 🗂️ Dns
Amazon Route 53 is DNS service.

A hosted zone represents a set of records belonging to a domain.

#### Amazon Route 53 Routing Policies
Routing Policy       |                   What it does
Simple               |    Simple DNS response providing the IP address associated with a name
Failover             |     If primary is down (based on health checks), routes to secondary destination
Geolocation          |     Uses geographic location you’re in (e.g. Europe) to route you to the closest region
Geoproximity         |     Routes you to the closest region within a geographic area
Latency              |     Directs you based on the lowest latency route to resources
Multivalue           |     answer Returns several IP addresses and functions as a basic load balancer
Weighted             |     Uses the relative weights assigned to resources to determine which to route to

#### Amazon Route Features
Domain Registration - .net .com .org

Hosted zone - example.com dctlabs.com

Health Checks

Traffic Flow

AWS-Management-console-->services-->Networking and Content delivery-->Route 53-->register Domain-->choose domain name:sawan.com-->add to cart-->continue-->Registrant Contact information fill-->complete order-->finished

Route53-management-console-->Hosted zones-->you will see the list of domain name zone here.

#### Amazon Route 53 Hosted Zones
You can migrate from another DNS provider and can import records

You can migrate a hosted zone to another AWS account

You can migrate from Route 53 to another registrar

- You can also associate a Route 53 hosted zone with a VPC in another account
Authorize association with VPC in the second account.
Create an association in the second account

Route53-management-console-->Hosted Zone-->select domain name-->Create record-->Recore type:A-->VAlue:Ip address-->Routing Policy as requirement->create record-->finished

#### CloudFront Web Distribution:
Speed up distribution of static and dynamic content, for example, .html, .css, .php, and graphics files

Distribute media files using HTTP or HTTPS

Add, update, or delete objects, and submit data from web forms

Use live streaming to stream an event in real time

#### Amazon CloudFront Caching
You can define a maximum Time To Live (TTL) and a default TTL

TTL is defined at the behavior level

This can be used to define different TTLs for different file types (e.g. png vs jpg)

After expiration, CloudFront checks the origin for any new requests (check the file is the latest version)

Headers can be used to control the cache:
• Cache-Control max-age=(seconds) - specify how long before CloudFront gets the object again from the origin server
• Expires – specify an expiration date and time

The default origin is used for any requests that don’t match a path pattern

The path pattern determines where to send the request

#### Caching Based on Request Headers
You can configure CloudFront to forward headers in the viewer request to the origin

CloudFront can then cache multiple versions of an object based on the values in one or more request headers

Controlled in a behavior to do one of the following:
• Forward all headers to your origin (objects are not cached)
• Forward a whitelist of headers that you specify
• Forward only the default headers (doesn’t cache objects based on values in request headers)

#### CloudFront Signed URLs
Signed URLs provide more control over access to content.

Can specify beginning and expiration date and time, IP addresses/ranges of users.

Mobile app uses signed URL to access distribution

Signed URLs should be used for individual files and clients that don’t support cookies

#### CloudFront Signed Cookies
Similar to Signed URLs

Use signed cookies when you don’t want to change URLs

Can also be used when you want to provide access to multiple restricted files (Signed URLs are for individual files)

#### CloudFront Origin Access Identity (OAI)
There is policy to restrict or allow Origin Access identity for access content.

AWS-management-console-->services-->Amazon cloud front-->create distribution-->Origin Domain Name-->fill details as requirement-->create ditribution-->finished

#### Lambda@Edge
Run Node.js and Python Lambda functions to customize the content CloudFront delivers

Executes functions closer to the viewer

- Can be run at the following points
After CloudFront receives a request from a viewer (viewer request)
Before CloudFront forwards the request to the origin (origin request)
After CloudFront receives the response from the origin (origin response)
Before CloudFront forwards the response to the viewer (viewer response)

#### AWS Global Accelerator
Network global service to use Microsoft network for content delivery around the world.

It allows User traffic ingresses using the closest Edge Location

It help Requests are routed to the optimal endpoint

AWS-management-console-->Global Accelerator-->select accelerator-->listeners-->select listener-->add endpoint group-->finished

#### An Architect needs to point the domain name dctlabs.com to the DNS name of an Elastic Load Balancer - Alias Record
### 🗂️ Block And File Storage
#### Block Storage(Disk & Hard Drives) - EBS(Elastic block Store) AWS service
The OS sees volumes that can be partitioned and formatted

The OS reads/writes at the block level. Disks can be internal, or network attached

#### File Storage - EFS(Elastic File System) AWS service
A filesystem can be shared by many users/computers

A filesystem is “mounted” to the OS using a network share

#### Object Storage - S3(simple storage system) AWS service
Massively scalable, low cost

There is no hierarchy of objects in the container

Uses a REST API

#### Amazon EBS Deployment and Volume Types
Limited support for attaching multiple instances*

EC2 instances must be in the same AZ as the EBS volume

EBS volumes are replicated within an AZ

#### Amazon EBS Multi-Attach
Must be a Provisioned IOPS io1 volume

Must be within a single AZ

Up to 16 instances can be attached to a single volume

Available for Nitro system-based EC2 instances

#### Amazon EBS
EBS volume data persists independently of the life of the instance

EBS volumes do not need to be attached to an instance

You can attach multiple EBS volumes to an instance

You can use multi-attach to attach a volume to multiple instances but with some constraints

EBS volumes must be in the same AZ as the instances they are attached to

Root EBS volumes are deleted on termination by default

Extra non-boot volumes are not deleted on termination by default

#### Amazon EBS Snapshots
Snapshot taken to Snap C capture a point-in-time state of an instance

Snapshots are stored on Amazon S3

Snapshots are incremental

A snapshot can be used to create an AMI(Amazon Machine images)

You can create an EBS volume in another AZ from a snapshot

#### Amazon Data Lifecycle Manager (DLM)
DLM automates the creation, retention, and deletion of EBS snapshots and EBS-backed AMIs

DLM helps with the following:
• Protects valuable data by enforcing a regular backup schedule
• Create standardized AMIs that can be refreshed at regular intervals
• Retain backups as required by auditors or internal compliance
• Reduce storage costs by deleting outdated backups
• Create disaster recovery backup policies that back up data to isolated accounts

#### EBS vs instance store
Instance Stores are ephemeral - data is lost when the instance is powered down

EBS volumes are attached over the network

Instance Store volumes are physically attached to the host

Instance store volumes are ephemeral (non-persistent) local disks that offer very high performance

Instance store volumes are high performance local disks that are physically attached to the host computer on which an EC2 instance runs

Instance stores are ephemeral which means the data is lost when powered off (non-persistent)

Instance stores are ideal for temporary storage of information that changes frequently, such as buffers, caches, or scratch data

Instance store volume root devices are created from AMI templates stored on S3

Instance store volumes cannot be detached/reattached

#### Amazon Machine Images (AMIs)
An Amazon Machine Image (AMI) provides the information required to launch an instance

An AMI includes the following:
• One or more EBS snapshots, or, for instance-store-backed AMIs, a template for the root volume of the instance (for example, an operating system, an application server, and applications)
• Launch permissions that control which AWS accounts can use the AMI to launch instances
• A block device mapping that specifies the volumes to attach to the instance when it's launched

AMIs come in three main categories:
• Community AMIs - free to use, generally you just select the operating system you want
• AWS Marketplace AMIs - pay to use, generally come packaged with additional, licensed software
• My AMIs - AMIs that you create yourself

EC2-management-console-->EC2 Image builder-->Create Image pipeline-->name,Build schedule:Manual-->Next-->Recipe:Create New recipe-->Select Recipe details-->Image Type:AMI-->Image Name,Version-->Select image-->source managed images:Amazon linux-->Images Name:As architecture-->Select component for build as requirement-->Genral Informtion-->Name,Infrastructure,VPC etc-->next-->next-->create pipeline-->finished

#### Using RAID with EBS
RAID stands for Redundant Array of Independent disks

Not provided by AWS, you must configure through your operating system

RAID 0 and RAID 1 are potential options on EBS

RAID 5 and RAID 6 are not recommended by AWS

#### Amazon Elastic File System (EFS) Overview
Can simultaneously connect thousands of instances

Can connect instances from other VPCs

NFS Protocol is used

EFS is only available for Linux instances

On-premises computers can be connected

Can also be separate AWS accounts

Mount using mount target IP address (no DNS)

NFS port range - 2049

EFS must be in the same VPC of Instance which you are going to mount or connect

AWS-management-console-->services-->storage-->EFS-->create a file system-->Name,VPC,regional/One Zone-->customize-->next-->Network Acess-->Specify correct security group-->next-->define or select policy option-->create-->finished

#### Amazon FSX
Amazon FSx provides fully managed thirdparty file systems

Amazon FSx provides you with two file systems to choose from:
• Amazon FSx for Windows File Server for Windows-based applications
• Amazon FSx for Lustre(High performance computing) for compute-intensive workloads

#### Amazon FSx for Windows File Server
Provides a fully managed native Microsoft Windows file system

Full support for the SMB protocol, Windows NTFS, and Microsoft Active Directory (AD) integration

Supports Windows-native file system features:
• Access Control Lists (ACLs), shadow copies, and user quotas.
• NTFS file systems that can be accessed from up to thousands of compute instances using the SMB protocol

High availability: replicates data within an Availability Zone (AZ)

Multi-AZ: file systems include an active and standby file server in separate AZs

#### Amazon FSx for Lustre
• High-performance file system optimized for fast processing of workloads such as:
• Machine learning
• High performance computing (HPC)
• Video processing
• Financial modeling
• Electronic design automation (EDA)

Works natively with S3, letting you transparently access your S3 objects as files

Your S3 objects are presented as files in your file system, and you can write your results back to S3

Provides a POSIX-compliant file system interface

#### AWS Storage Gateway
It help to connect on premises storage to aws.

#### AWS Storage Gateway – File Gateway
File gateway provides a virtual on-premises file server

Store and retrieve files as objects in Amazon S3

Use with on-premises applications, and EC2-based applications that need file storage in S3 for objectbased workloads

File gateway offers SMB or NFS-based access to data in Amazon S3 with local caching

#### AWS Storage Gateway - Volume Gateway
The volume gateway supports block-based volumes

Block storage – iSCSI protocol

Cached Volume mode – the entire dataset is stored on S3 and a cache of the most frequently accessed data is cached on-site

Stored Volume mode – the entire dataset is stored on-site and is asynchronously backed up to S3 (EBS point-in-time snapshots).
Snapshots are incremental and compressed

#### AWS Storage Gateway - Tape Gateway
Used for backup with popular backup software

Each gateway is preconfigured with a media changer and tape drives. Supported by NetBackup, Backup Exec, Veeam etc.

When creating virtual tapes, you select one of the following sizes: 100 GB, 200 GB, 400 GB, 800 GB, 1.5 TB, and 2.5 TB

A tape gateway can have up to 1,500 virtual tapes with a maximum aggregate capacity of 1 PB

All data transferred between the gateway and AWS storage is encrypted using SSL

All data stored by tape gateway in S3 is encrypted server-side with Amazon S3-Managed Encryption Keys (SSE-S3)

Schedule and backup for mutiple resources

AWS-management-console-->services-->AWS backup-->Backup plan-->Select option- start with template-->fill details as requirement-->create plan-->finished

AWS-Backup-->backup-plan-->select plan-->Resource assignment-->assign resources-->finished
### 🗂️ Docker Containers And Ecs
Containers start up very quickly

Containers are very resource efficient

A container includes all the code, settings, and dependencies for running the application

Each container is isolated from other containers

ECS allows us to run docker container on Aws

#### Amazon Elastic Container Service (ECS)
An Amazon ECS Cluster is a logical grouping of tasks or services

ECS Services are used to maintain a desired count of tasks

An ECS Task is a running Docker container

An ECS Task is created from a Task Definition

Docker images can be stored in Amazon ECR

#### Amazon ECS Key Features
Serverless with AWS Fargate           – managed for you and fully scalable

Fully managed container orchestration – control plane is managed for you

Docker support                        – run and manage Docker containers with integration into the Docker Compose CLI

Windows container support             – ECS supports management of Windows containers

Elastic Load Balancing integration    – distribute traffic across containers using ALB or NLB

Amazon ECS Anywhere (NEW)             – enables the use of Amazon ECS control plane to manage on-premises implementations
Elastic Container Service (ECS) |               Description
Cluster                         |    Logical grouping of EC2 instances
Container instance              | EC2 instance running the the ECS agent
Task Definition                 |  Blueprint that describes how a docker container should launch
Task                            |    A running container using settings in a Task Definition
Service                         |  Defines long running tasks – can control task count with Auto Scaling and attach an ELB

#### Amazon ECS Launch Types
EC2 Launch Type                                       |  Fargate Launch Type
You explicitly provision EC2 instances                | Fargate automatically provisions resources
You’re responsible for managing EC2 instances         | Fargate provisions and manages compute
Charged per running EC2 instance                      | Charged for running tasks
Docker volumes, EFS, and FSx for Windows File Server  | EFS integration
You handle cluster optimization                       | Fargate handles cluster optimization
More granular control over infrastructure             | Limited control, infrastructure is automated

- CLuster Defination
AWS-management-console-->services-->containers-->Elastic container service-->Create cluster-->select networking only-->Cluster Name-->Enable container Insight-->create Cluster-->finished

- Task Defination
ECS-Management-console-->task defination-->Create new task defination-->select Fargate-->next-->name,infra,role,etc-->Conatiner defination-->add container-->container name,image,port mapping,memory limit-->fill other details like-->health check,Environment varibale etc-->Add-->create-->finished

- Run New task on Cluster
ECS-Management-console-->Cluster-->select cluster-->Tasks-->Run new task-->Deployment configuration-->select task-->family choose task name,Revision,Number of launch task(intances)-->Networking-->select VPC,subnet,security group-->deploy-->finished

- Access task by url
ECS-Management-console-->Cluster-->select cluster-->Tasks-->select task id-->Networking-->Public IP-->hit on browser-->finished

#### Amazon ECS and IAM Roles
The container instance IAM role provides permissions to the host

The ECS task IAM role provides permissions to the container

NOTE : container instances have access to all of thepermissions that are supplied to the container instance role through instance metadata

With the Fargate launch type only IAM task roles can be applied

#### Auto Scaling for ECS
Two types of scaling:
- Service auto scaling(for Container/task running)
• Metric reports CPU > 80%
• CloudWatch notifies Application Auto Scaling
• ECS launches additional task

Amazon ECS Service Auto Scaling supports the following types of scaling policies:
•Target Tracking Scaling Policies — Increase or decrease the number of tasks that your service runs based on a target value for a specific CloudWatch metric

• Step Scaling Policies — Increase or decrease the number of tasks that your service runs in response to CloudWatch alarms. Step scaling is based on a set of scaling adjustments, known as step adjustments, which vary based on the size of the alarm breach

• Scheduled Scaling — Increase or decrease the number of tasks that your service runs based on the date and time

Service auto scaling - automatically adjusts the desired task count up or down using the Application Auto Scaling service

Service auto scaling - supports target tracking, step, and scheduled scaling policies

- Cluster auto scaling
• Metric reports target capacity > 80%
• CloudWatch notifies ASG
• AWS launches additional container instance

Uses an ECS resource type called a Capacity Provider

A Capacity Provider can be associated with an EC2 Auto Scaling Group (ASG)

ASG can automatically scale using:
• Managed scaling - with an automatically-created scaling policy on your ASG

• Managed instance termination protection - which enables containeraware termination of instances in the ASG when scale-in happens

ASG is linked to ECS using a Capacity Provider

A Capacity provider reservation metric measures the total percentage of cluster resources needed by all ECS workloads in the cluster

Cluster auto scaling - uses a Capacity Provider to scale the number of EC2 cluster instances using EC2 Auto Scaling

#### Amazon ECS with ALB(Application Load Balancer)
Each task is running a web service on port 80

All connections to web services coming into HTTP listener (port 80) in ALB

NAT gateway required for tasks in private subnets to access the internet

A dynamic port is allocated on the host

- CLuster Defination
ECS-Management-console-->create cluster-->EC2 linux+Networking-->Next step-->Cluster Name,Size,Number of instance,volume,ssh key pair,Networking,enable container insight-->create-->finished

- Task Defination
ECS-Management-console-->task defination-->Create new task defination-->select EC2-->next-->name,infra,role,etc-->Conatiner defination-->add container-->container name,image,port mapping(0-80),memory limit-->fill other details like-->health check,Environment varibale etc-->Add-->create-->finished

-create service
ECS-Management-console-->task defination-->Create new task defination-->select EC2-->service-->create-->launch type EC2-->fill details-->next-->networking-->set auto scaling-->create service-->finished

to run multiple container in EC2 launch type instnace for ECS we need to use Network Mode : Bridge

- Service creation
ECS-Management-console-->Cluster-->select cluster-->deploy-->Service,famile:task name,revision,desired task-->Load balancing-->application load balancer-->name,listener,port:80,protocol:http-->Target Group Name,Protocol:Http-->Healthcheck Path:/-->Networking-->select VPC-->select Public Subnet-->select security group-->Enable Public IP assignment-->deploy-->finished

#### Amazon EKS(Elastic Kubernates service)
Managed Kubernetes service – runs on EC2 / Fargate and also AWS Outposts

Groups of containers are known as Pods in Kubernetes

EKS supports load balancing with ALB, NLB, CLB

#### Amazon EKS Use Cases
Use when you need to standardize container orchestration across multiple environments using a managed Kubernetes implementation

Hybrid Deployment - manage Kubernetes clusters and applications across hybrid environments (AWS + On-premises)

Batch Processing  - run sequential or parallel batch workloads on your EKS cluster using the Kubernetes Jobs API. Plan, schedule and execute batch workloads

Machine Learning - use Kubeflow with EKS to model your machine learning workflows and efficiently run distributed training jobs using the latest EC2 GPU-powered instances, including Inferentia

Web Applications - build web applications that automatically scale up and down and run in a highly available configuration across multiple Availability Zones

#### Amazon ECS v/s Amazon EKS
Amazon ECS                                               |                       Amazon EKS
Managed, highly available, highly scalable container     | Managed, highly available, highly scalable container platform
platform

AWS-specific platform that supports Docker Containers    | Compatible with upstream Kubernetes so it’s easy to lift and                                                        and from other Kubernetes deployments

Considered simpler and easier to use                     | Considered more feature-rich and complex with a steep learning curve

Leverages AWS services like Route 53, ALB, and CloudWatch| A hosted Kubernetes platform that handles many things internally

“Tasks” are instances of containers that are run         | “Pods” are containers collocated with one another and can
on underlying compute but more of less isolated             have shared access to each other

Limited extensibility                                    | Extensible via a wide variety of third-party and community add-ons.
### 🗂️ Serverless Applications
It is concept of you dont need to manage computation reosurces for any services which provide you capablity.

#### Serverless Services and Event-Driven Architecture
s3 static website------------->Lambda Function------------->SQS Queue------------->Lambda fintion-------------->DynamoDB Table
- User uploads a                 - Serverless function                             - SNS topic        - Function processes
file through                     processes file                                  - A notification     the message and
a static                       - Processed file is                                 sent using SNS     stores information in
website                          stored in a bucket                                and email          a database

#### Serverless Services
With serverless there are no instances to manage

You don’t need to provision hardware

There is no management of operating systems or software

Capacity provisioning and patching is handled automatically

Provides automatic scaling and high availability

Can be very cheap!

#### AWS Lambda
AWS Lambda executes code only when needed and scales automatically

You pay only for the compute time you consume (you pay nothing when your code is not running)

Benefits of AWS Lambda:
• No servers to manage
• Continuous scaling
• Millisecond billing
• Integrates with almost all other AWS services

Primary use cases for AWS Lambda:
• Data processing
• Real-time file processing
• Real-time stream processing
• Build serverless backends for web, mobile, IOT, and 3rd party API requests

#### Lambda Function Invocations
SQS(simple Queue service) can also trigger Lambda

Synchronous:
• CLI, SDK, API Gateway
• Wait for the function to process the event and return a response
• Error handling happens client side (retries, exponential backoff etc.)

Asynchronous:
• S3, SNS, CloudWatch Events etc.
• Event is queued for processing and a response is returned immediately
• Lambda retries up to 3 times
• Processing must be idempotent (due to retries)

Event source mapping:
• SQS, Kinesis Data Streams, DynamoDB Streams
• Lambda does the polling (polls the source)
• Records are processed in order (except for SQS standard)

#### Lambda Function Concurrency

Function invocation     lambda     funtion executed    Additional functions are      If the concurrency limit is exceeded
### 🗂️ Function
#### Burst concurrency quotas:                             burst or account limit      exceeded” and 429 “TooManyRequestsException”
• 3000 – US West (Oregon), US East (N. Virginia), Europe(Ireland)
• 1000 – Asia Pacific (Tokyo), Europe (Frankfurt), US East (Ohio)
• 500 – Other Regions

AWS-management-console-->Services-->Compute-->Lambda-->create Function-->Select Author from Scratch-->Fucntion Name-->Runtime-->select Lnaguage to code-->Create new role with basic Lambda-->Create Function

Trigger is an event Source.

Desitination is the responce to send lambda function after successfull execution.

Lambda-Management-console-->select function-->code-->test-->New event,Template,hello-->Save chnages-->test

cloudwatch-->logs-->logs group-->select lambda function-->finished


#### Application Integration Services Overview

Note: AWS recommends that for new applications customers consider Step Functions instead of SWF
Service                        |              What it does                    |                     Example use cases
Simple Queue Service              Messaging queue; store and forward patterns  Building distributed / decoupled applications

Simple Notification Service       Set up, operate, and send notifications      Send email notification when CloudWatch alarm is
.                                 from the cloud                               triggered

Step Functions                    Out-of-the-box coordination of AWS           Order processing workflow
.                                 service components with visual workflow

Simple Workflow Service           Need to support external processes or        Human-enabled workflows like an order fulfilment
.                                 specialized execution logic                  system or for procedural requests

Amazon MQ                         Message broker service for Apache            Need a message queue that supports industry
.                                 Active MQ and RabbitMQ                       standard APIs & protocols; migrate queues to AWS

Amazon Kinesis                    Collect,process & analyze streaming data    Collect data from IoT devices for processing

#### Kinesis vs SQS vs SNS
Amazon Kinesis                     |              Amazon SQS              |              Amazon SNS
### 🗂️ Consumers Pull Data                         Consumers Pull Data               Push Data To Many Subscribers

As many consumers as you need         Data is deleted after being consumed    Publisher / subscriber model

Routes related records to same        Can have as many workers (consumers)    Integrates with SQS for fan-out
record processor                      as you need                             architecture pattern

Multiple applications can access      No ordering guarantee                   Up to 10,000,000 subscribers
stream concurrently                   (except with FIFO Queues)

Ordering at the shard level           Provides messaging semantics            Up to 100,000 topics

Can consume records in correct        Individual message delay                Data is not persisted
order at later time

Must provision throughput             Dynamically scales                      No need to provision throughput

#### SQS(Simple Queue Service) Types
- Standard Queue
Unlimited Throughput: Standard queues support a nearly unlimited number of transactions per second (TPS) per API action

Best-Effort Ordering: Occasionally, messages might be delivered in an order different from which they were sent

At-Least-Once Delivery: A message is delivered at least once, but occasionally more than one copy of a message is delivered

- FIFO Queue(First In First Out)
High Throughput: FIFO queues support up to 300 messages per second (300 send, receive, or delete operations per second). When you batch 10 messages per operation (maximum), FIFO queues can support up to 3,000 messages per second

First-ln-First-out Delivery: The order in which messages are sent and received is strictly preserved

Exactly-Once Processing: A message is delivered once and remains available until a consumer processes and deletes it. Duplicates are not introduced into the queue

#### SQS Queue Types
FIFO queues require the Message Group ID and Message Deduplication ID parameters to be added to messages
Message Group ID:
• The tag that specifies that a message belongs to a specific message group Messages that belong to the same message group are guaranteed to be processed in a FIFO manner

Message Deduplication ID:
• The token used for deduplication of messages within the deduplication interval

#### SQS – Dead Letter Queue
Message not processed successfully (ReceiveCount exceeds maxReceiveCount for queue)

Dead-letter queue is a standard or FIFO queue that has been specified as a dead-letter queue

The main task of a dead-letter queue is handling message failure

A dead-letter queue lets you set aside and isolate messages that can’t be processed correctly to determine why their processing didn’t succeed

It is not a queue type, it is a standard or FIFO queue that has been specified as a dead-letter queue in the configuration of another standard or FIFO queue

#### SQS – Delay Queue
Message is visible-->Message is received-->lambda funtion-->Delay Seconds

Message cannot be returned

#### SQS Long Polling vs Short Polling
Long polling - waits for the WaitTimeSeconds and eliminates empty responses

Short polling - checks a subset of servers and may not return all messages

SQS Long polling is a way to retrieve messages from SQS queues – waits for messages to arrive

SQS Short polling returns immediately (even if the message queue is empty)

SQS Long polling can lower costs

SQS Long polling can be enabled at the queue level or at the API level using WaitTimeSeconds

SQS Long polling is in effect when the Receive Message Wait Time is a value greater than 0 seconds and up to 20 seconds

The maximum amount of time that a long polling receive call will wait for a message to become available before returning an empty response.

#### Amazon SNS
Amazon SNS is a highly available, durable, secure, fully managed pub/sub messaging service

Amazon SNS provides topics for high-throughput, push-based, many-to-many messaging

Publisher systems can fan out messages to a large number of subscriber endpoints:

Endpoints include:
• Amazon SQS queues
• AWS Lambda functions
• HTTP/S webhooks
• Mobile push
• SMS
• Email

Multiple recipients can be grouped using Topics

A topic is an “access point” for allowing recipients to dynamically subscribe for identical copies of the same notification

One topic can support deliveries to multiple endpoint types

Simple APIs and easy integration with applications

Flexible message delivery over multiple transport protocols

#### Amazon SNS + Amazon SQS Fan-Out
You can subscribe one or more Amazon SQS queues to an Amazon SNS topic

Amazon SQS manages the subscription and any necessary permissions

When you publish a message to a topic, Amazon SNS sends the message to every subscribed queue

#### AWS Step Functions
AWS Step Functions is used to build distributed applications as a series of steps in a visual workflow.

You can quickly build and run state machines to execute the steps of your application

How it works:
1. Define the steps of your workflow in the JSON-based Amazon States Language. The visual console automatically graphs each step in the order of execution

2. Start an execution to visualize and verify the steps of your application are operating as intended. The console highlights the real-time status of each step and provides a detailed history of every execution

3. AWS Step Functions operates and scales the steps of your application and underlying compute for you to help ensure your application executes reliably under increasing demand

AWS-management-console-->services-->appli Invocations-->AWS step function-->Get started-->Definaton in Json-->next-->start Execution-->Name,input:{"IsHelloWorldExample: true"}-->start execution-->you can see workflow in realtime-->finished

AWS-management-console-->service-->EC2-->Create lambda function-->create state machine-->write workflow in code select-->create-->finished

#### Amazon EventBridge
EventBridge used to be known as CloudWatch Events

AWS-management-console-->amazon event bridge-->Events-->rules-->Create rule-->Name,Event pattern:pre-defined pattern by service,service provider:AWS,service Name:EC2,Events:EC2 Instance state-chnage notification,specific state:terminated,specific intance-ID:EC2 instnace ID-->Target-->SNS Topic,Topic:MyEmail notification-->create-->finished

#### Amazon API Gateway
It is used to create Application programing Interface which is essentially the frontdoor of business logic on application.

#### Amazon API Gateway Deployment Types
- Edge-optimized endpoint
• Reduced latency for requests from around the world

- Regional endpoint
• Reduced latency for requests that originate in the same region
• Can also configure your own CDN and protect with WAF

- Private endpoint
Securely expose your REST APIs only to other services within your VPC or connect via Direct Connect

#### API Gateway Integrations
- For a Lambda function you can have:
• Lambda proxy integration
• Lambda custom integration

- For an HTTP endpoint you can have:
• HTTP proxy integration
• HTTP custom integration

- For an AWS service action you have the AWS
integration of the non-proxy type only

#### API Gateway - Caching
You can add caching to API calls by provisioning an Amazon API Gateway cache and specifying its size in gigabytes

Caching allows you to cache the endpoint's response

Caching can reduce number of calls to the backend and improve latency of requests to the API

#### API Gateway - Throttling
API Gateway sets a limit on a steady-state rate and a burst of request submissions against all APIs in your account

- Limits:
• By default API Gateway limits the steady-state request rate to 10,000 requests per second
• The maximum concurrent requests is 5,000 requests across all APIs within an AWS account
• If you go over 10,000 requests per second or 5,000 concurrent requests you will receive a 429 Too Many Requests error response
• Upon catching such exceptions, the client can resubmit the failed requests in a way that is rate limiting, while complying with the API Gateway throttling limits


WEbApp-->Published API-->HTTP Method Request-->Integration Request-->EndPoint-->Convert Pass through-->HTTP STATUS CODES RESPONSE BODIES-->WEbApp

HTTP Method Request - ANY,DELETE,GET,HEAD,OPTIONS,PATCH,POST,Put

Integration Request - Map the request parameters of method request to the format required by the backend

EndPoint - Lambda function, HTTP endpoint, EC2 instance, AWS service etc.

HTTP STATUS CODES RESPONSE BODIES - Map the status codes, headers, and payload received from backend into format for client

AWS-management-console-->services-->API Gateway-->Select Rest API-->choose protocol:rest-->Create New Api:Example API-->EndPoint Type:Regional-->Import-->finished

AWS-management-console-->Services-->Management and Governance-->cloudformation-->create stck-->Prerequisite - Prepare Template:Template is Ready-->Specify template:upload a template file:choose file from local system-->select template.yaml file-->upload-->View in desgner-->create stack-->next-->stack name:any name-->next-->next-->create stack-->finished

create s3 bucket-->enable static website-->finished

AWS-management-console-->API gateway-->select API-->select Stages-->create stage-->Name:prod-->create-->finished

AWS-management-console-->API gateway-->integration-->manage integration-->create new-->Integration type:Lambda function-->select region and lambda function-->create-->finished

copy integraton ID : 7679fdsvbfjk

AWS-management-console-->API gateway-->route-->create-->Route and Method:GET,/api-->select API Method-->attach integration-->chhose one with integration ID-->finished

AWS-management-console-->API gateway-->cors-->configure cors-->Access-control-allow-origin:https://URlofbucketname.s3.amazon.com-->Access-control-allow-header:*-->access-control-allow-method:*-->access-control-expose-header:*-->access-control-max-age:96400-->Access-control-allow-credentials:Yes-->save-->deploy-->select stage-->finished

AWS-management-console-->Services-->Management and Governance-->cloudformation-->select stack-->delete-->finished
### 🗂️ Databases And Analytics
Data Store                                                        Use Case
Database on EC2                                   • Need full control over instance and database
.                                                 • Third-party database engine (not available in RDS)

Amazon RDS                                        • Need traditional relational database
.                                                 • e.g. Oracle, PostgreSQL, Microsoft SQL, MariaDB, MySQL
.                                                 • Data is well-formed and structured

Amazon DynamoDB                                   • NoSQL database
.                                                 • In-memory performance
.                                                 • High I/O needs
.                                                 • Dynamic scaling

Amazon RedShift                                   • Data warehouse for large volumes of aggregated data

Amazon ElastiCache                                • Fast temporary storage for small amounts of data
.                                                 • In-memory database

Amazon EMR                                        • Analytics workloads using the Hadoop framework

#### Amazon Relational Database Service (RDS)
RDS runs on EC2 instances, so you must choose an instance type

RDS is a managed,relational database

RDS supports the following database engines:
• Amazon Aurora
• MySQL
• MariaDB
• Oracle
• Microsoft SQL Server
• PostgreSQL

RDS uses EC2 instances, so you must choose an instance family/type

Relational databases are known as Structured Query Language (SQL) databases

RDS is an Online Transaction Processing (OLTP) type of database

Easy to setup, highly available, fault tolerant, and scalable

Common use cases include online stores and banking systems

You can encrypt your Amazon RDS instances and snapshots at rest by enabling the encryption option for your Amazon RDS DB instance (duringcreation)

Encryption uses AWS Key Management Service (KMS)

Scales up by increasing instance size (compute and storage)

Read replicas option for read heavy workloads (scales out for reads/queries only)

Disaster recovery with Multi-AZ option

#### Amazon RDS Manual Backups (Snapshot)
Backs up the entire DB instance, not just individual databases

For single-AZ DB instances there is a brief suspension of I/O

For Multi-AZ SQL Server, I/O activity is briefly suspended on primary

For Multi-AZ MariaDB, MySQL, Oracle and PostgreSQL the snapshot is taken from the standby

Snapshots do not expire (no retention period)

Restore can be to any point in time during the retention period

#### Amazon RDS Maintenance Windows
Operating system and DB patching can require taking the database offline

These tasks take place during a maintenance window

By default a weekly maintenance window is configured

You can choose your own maintenance window

AWS-management-console-->services-->amazon RDS-->database-->create database-->standard-->mysql-->pricing tier-->master name-->password-->DB instnace class-->sizing and infra-->multi-Az-->default VPC-->public Access:No-->password authentication-->backup & maintennace windows option-->finished

Amazon-RDS-console-->select database-->action-->create Read replicas-->create read replicas-->finished

#### switch to secondary available zone RDS
Amazon-RDS-console-->select database-->action-->reboot-->failover-->finished

#### Amazon RDS Security
Encryption at rest can be enabled – includes DB storage, backups, read replicas and snapshots

You can only enable encryption for an Amazon RDS DB instance when you create it, not after the DB instance is created

DB instances that are encrypted can't be modified to disable encryption

Uses AES 256 encryption and encryption is transparent with minimal performance impact

RDS for Oracle and SQL Server is also supported using Transparent Data Encryption (TDE) (may have performance impact)

AWS KMS is used for managing encryption keys

You can't have:
• An encrypted read replica of an unencrypted DB instance
• An unencrypted read replica of an encrypted DB instance

Read replicas of encrypted primary instances are encrypted

The same KMS key is used if in the same Region as the primary

If the read replica is in a different Region, a different KMS key is used

You can't restore an unencrypted backup or snapshot to an encrypted DB instance

Amazon-RDS-console-->snapshots-->select unencrypted snapshot-->action-->copy-->Enable Encryption-->AWS KMS key-->copy snapshot-->action-->restore-->encrytion windows enabled automatically-->restore DB instance-->finished

#### Amazon Aurora
Amazon Aurora is an AWS database offering in the RDS family

Amazon Aurora is a MySQL and PostgreSQL-compatible relational database built for the cloud

Amazon Aurora is up to five times faster than standard MySQL databases and three times faster than standard PostgreSQL databases

Amazon Aurora features a distributed, fault-tolerant, self-healing storage system that auto-scales up to 128TB per database
instance

#### Aurora Fault Tolerance
• Fault tolerance across 3 AZs
• Single logical volume
• Aurora Replicas scale-out read requests
• Can promote Aurora Replica to be a new primary or create new primary
• Can use Auto Scaling to add replicas

#### Aurora Feature & benefits
High performance and scalability - Offers high performance, self-healing storage that scales up to 128TB, point-in-time
recovery and continuous backup to S3

DB compatibility - Compatible with existing MySQL and PostgreSQL open source databases

Aurora Replicas - In-region read scaling and failover target – up to 15 (can use Auto Scaling)

MySQL Read Replicas - Cross-region cluster with read scaling and failover target – up to 5 (each can have up to 15
Aurora Replicas)

Global Database -Cross-region cluster with read scaling (fast replication / low latency reads). Can remove secondary and promote

Multi-Master - Scales out writes within a region. In preview currently and will not appear on the exam

Serverless - On-demand, autoscaling configuration for Amazon Aurora - does not support read replicas
or public IPs (can only access through VPC or Direct Connect - not VPN)

#### Aurora Serverless Use Cases
• Infrequently used applications
• New applications
• Variable workloads
• Unpredictable workloads
• Development and test databases
• Multi-tenant applications

#### When NOT to use Amazon RDS (anti-patterns)
Anytime you need a DB type other than:
• MySQL
• MariaDB
• SQL Server
• Oracle
• PostgreSQL

You need root access to the OS (e.g. install software such as management tools)

#### Amazon ElastiCache
Fully managed implementations Redis and Memcached

ElastiCache is a key/value store

In-memory database offering high performance and low latency

Can be put in front of databases such as RDS and DynamoDB

ElastiCache nodes run on Amazon EC2 instances, so you must choose an instance family/type
Feature                     Memcached                 Redis (cluster mode disabled)                Redis (cluster mode enabled)
Data persistence                No                                Yes                                             Yes

Data types                    Simple                            Complex                                          Complex

Data partitioning              Yes                                No                                              Yes

Encryption                     No                                 Yes                                             Yes

High availability              No                                 Yes                                             Yes
(Replication)

Multi-AZ            Yes, place nodes in multiple AZs. Yes, with auto-failover. Uses read     Yes,with auto-failover .Uses read
.                   No failover or replication        replicas(0-5 per shard)                    replicas   (0-5pershard)


Scaling             Up (node type); out (add nodes)      Up (node type); out (add replica)     Up (node type); out (add shards)

Multithreaded                Yes                                   No                                              No

Backup and restore  No (and no snapshots)             Yes, automatic and manual snapshots   Yes, automatic and manual snapshots

#### Amazon ElastiCache Use Cases
Data that is relatively static and frequently accessed

Applications that are tolerant of stale data

Data is slow and expensive to get compared to cache retrieval

Require push-button scalability for memory, writes and reads

Often used for storing session state

#### Amazon ElastiCache Examples Use Case Benefit
Web session store - In cases with load-balanced web servers, store web session information in Redis so if a server is lost, the session info is not lost, and another web server can pick it up

Database caching  - Use Memcached in front of AWS RDS to cache popular queries to offload work from RDS and return results faster to users

Leaderboards      - Use Redis to provide a live leaderboard for millions of users of your mobile app

Streaming data dashboards - Provide a landing spot for streaming sensor data on the factory floor, providing live real-time
dashboard displays

#### Amazon ElastiCache - Scalability
- Memcached
• Add nodes to a cluster
• Scale vertically (node type) – must create a new cluster manually Redis

- Redis
Cluster mode disabled:
• Add replica or change node type – creates a new cluster and migrates data

Cluster mode enabled:
• Online resharding to add or remove shards; vertical scaling to change node type
• Offline resharding to add or remove shards change node type or upgrade engine (more flexible than online)

AWS-management-console-->services-->elasticcache dashboards-->get started now-->redis-->cluster mode enabled:NO-->amazon cloud-->create-->finished

#### Amazon DynamoDB
Fully managed NoSQL database service

Key/value store and document store

It is a non-relational, key-value type of database

Fully serverless service

Push button scaling

DynamoDB is made up of:
• Tables
• Items
• Attributes

#### DynamoDB Time to Live (TTL)
TTL lets you define when items in a table expire so that they can be automatically deleted from the database

With TTL enabled on a table, you can set a timestamp for deletion on a per-item basis
No extra cost and does not use WCU / RCU

Helps reduce storage and manage the table size over time

#### features and benefits
DynamoDB Feature                                                    Benefits
NoSQL type of database         Flexible schema, good for when data is not well structured or unpredictable
with Name / Value structure

Serverless                     Fully managed, fault tolerant, service

Highly available               99.99% availability SLA – 99.999% for Global Tables!

Horizontal scaling             Seamless scalability to any scale with push button scaling or Auto Scaling

DynamoDB                       Captures a time-ordered sequence of item-level modifications in a DynamoDB table and durably
Streams                        stores the information for up to 24 hours. Often used with Lambda and the Kinesis Client
.                              Library (KCL)

DynamoDB Accelerator (DAX)     Fully managed in-memory cache for DynamoDB that increases performance (microsecond latency)

Transaction options            Strongly consistent or eventually consistent reads, support for ACID transactions

Backup                         Point-in-time recovery down to the second in last 35 days; On-demand backup and restore

Global Tables                  Fully managed multi-region, multi-master solution
AWS-management-console--services--dynamoDB-->create table-->tableName-->partition key-->sort key-->capacity calculator-->read/write capacity setting-->encryption at rest-->Owned by amazon DynamoDB-->create table-->finished

aws dynamoDB batch-write-item --request-items file://mystore.json(local system path)

#### dynamoDB Stream
step 1 - Application inserts / updates /deletes item
step 2 - A record is written to the DynamoDB stream
step 3 - A Lambda function is triggered
step 4 - The Lambda function writes to CloudWatch Logs

Application--(1)-->DynamoDB Table--(2)-->DynamoDB stream--(3)-->Aws Lambda--(4)-->Amazon CloudWatch


Captures a time-ordered sequence of item-level modifications in any DynamoDB table and stores this information in a log for up to 24 hours

Can configure the information that is written to the stream:
• KEYS_ONLY —Only the key attributes of the modified item

• NEW_IMAGE —The entire item, as it appears after it was modified

• OLD_IMAGE —The entire item, as it appeared before it was modified

• NEW_AND_OLD_IMAGES —Both the new and the old images of the item

#### DynamoDB Accelerator (DAX)
DAX is a fully managed, highly available, in-memory cache for DynamoDB

Improves performance from milliseconds to microseconds

Can be a read-through cache and a write-through cache

Used to improve READ and WRITE performance

You do not need to modify application logic, since DAX is compatible with existing DynamoDB API calls

#### DAX vs ElastiCache
DAX is optimized for DynamoDB

With ElastiCache you have more management overhead (e.g. invalidation)

With ElastiCache you need to modify application code to point to cache

ElastiCache supports more datastores

#### DynamoDB Global Tables
Global Tables is a Multi-region, multiactive database

Use logic in the application to failover to a replica region

Each replica table stores the same set of data items

The data sync by Asynchronous replication

we can create as much replica we want in different regions

dynamoDB-management-console-->select table-->select global table-->create replica-->available replication region-->create replica-->finished

#### Amazon RedShift
Amazon Redshift is a fast, fully managed data warehouse

Analyze data using standard SQL and existing Business Intelligence (BI) tools

RedShift is a SQL based data warehouse used for analytics applications

RedShift is a relational database that is used for Online Analytics Processing (OLAP) use cases

RedShift uses Amazon EC2 instances, so you must choose an instance family/type

RedShift always keeps three copies of your data

RedShift provides continuous/incremental backups

#### OLTP vs OLAP (refresher)
Operational / transactional                                            Analytical
Online Transaction Processing (OLTP)             Online Analytics Processing (OLAP) – the source data comes from OLTP DBs

Production DBs that process transactions.        Data warehouse. Typically, separated from the customer facing DBs.
E.g. adding customer records, checking stock     Data is extracted for decision making
availability (INSERT, UPDATE, DELETE)

Short transactions and simple queries            Long transactions and complex queries

Examples: Amazon RDS, DynamoDB                   Examples: Amazon RedShift, Amazon EMR

RedShift Spectrum can run SQL queries on data directly in S3

#### RedShift Use Cases
Perform complex queries on massive collections of structured and semi-structured data and get fast performance

Frequently accessed data that needs a consistent, highly structured format

Use Spectrum for direct access of S3 objects in a data lake

Managed data warehouse solution with:
• Automated provisioning, configuration and patching
• Data durability with continuous backup to S3
• Scales with simple API calls
• Exabyte scale query capability

#### RedShift Data Source
Amazon EC2 , Amazon RDS , Amazon DynamoDB , Amazon EMR , Amazon S3 , AWS Data Pipeline , AWS Glue , On-Premises Server

#### Amazon Elastic Map Reduce (EMR)
Managed cluster platform that simplifies running big data frameworks including Apache Hadoop and Apache Spark

Used for processing data for analytics and business intelligence

Can also be used for transforming and moving large amounts of data

Performs extract, transform, and load (ETL) functions

#### Amazon EMR archietecture
Optionally attach----------->Root access to--------------->Amazon EMR--------------->Scale cluster instances or deploy multiple
EBS volumes                  cluster instances                                       clusters
EBS volume------------------------------------------->Cluster Cluster cluster

#### Data Store options
Amazon S3 , Amazon S3 Glacier , Amazon Redshift , Amazon DynamoDB , Amazon RDS , HDFS(hadoop file system)

#### Amazon Athena and AWS Glue(Analytical services)
Athena - can query data in CSV, TSV, JSON, Parquet and ORC formats
.        Point Athena at data source in S3 and then run SQL queries
.        A Lambda function connects Athena to data source
.        SQL queries can also be run against these data sources
.        Data from source is mapped in tables in Athena and is queryable

Athena queries data in S3 using SQL

Can be connected to other data sources with Lambda

Data can be in CSV, TSV, JSON, Parquet and ORC formats

Uses a managed Data Catalog (AWS Glue) to store information and schemas about the databases and tables

#### Optimizing Athena for Performance
Partition your data

Bucket your data – bucket the data within a single partition

Use Compression – AWS recommend using either Apache Parquet or Apache ORC

Optimize file sizes

Optimize columnar data store generation – Apache Parquet and Apache ORC are popular columnar data stores

Optimize ORDER BY and Optimize GROUP BY

Use approximate functions

Only include the columns that you need

#### AWS Glue

AWS Glue - is used as a metadata catalog (can also use Apache Hive)

Fully managed extract, transform and load (ETL) service

Used for preparing data for analytics

AWS Glue runs the ETL jobs on a fully managed, scale-out Apache Spark environment

AWS Glue discovers data and stores the associated metadata (e.g. table definition and schema) in the AWS Glue Data Catalog

Works with data lakes (e.g. data on S3), data warehouses (including RedShift), and data stores (including RDS or EC2 databases)

You can use a crawler to populate the AWS Glue Data Catalog with tables

A crawler can crawl multiple data stores in a single run

Upon completion, the crawler creates or updates one or more tables in your Data Catalog.

ETL jobs that you define in AWS Glue use the Data Catalog tables as sources and targets

AWS-management-console-->Services-->ec2 instance-->ALB-->select ALB-->action-->edit attribute-->access log S3 location-->select create location for me-->go to S3 location-->download the access logs

AWS-management-console-->service-->Amazon ethena-->get started-->set query result location in S3-->create table with logs column-->select SQL query to get result-->finished

#### Amazon OpenSearch Service(Elasticsearch)
Distributed search and analytics suite

Based on the popular open source Elasticsearch

Supports queries using SQL syntax

Integrates with open-source tools

Scale by adding or removing instances

Availability in up to three Availability Zones

Backup using snapshots

Encryption at-rest and in-transit

Search, visualize, and analyze text and unstructured data

Successor to Amazon Elasticsearch Service

Deploy nodes and replicas across AZs

Deploy to Amazon VPC and integrates with IAM

#### OpenSearch Service Deployment
Clusters are created (Management Console, API, or CLI)

Clusters are also known as OpenSearch Service domains

You specify the number of instances and instance types

Storage options include UltraWarm or Cold storage

#### OpenSearch in an Amazon VPC
Clusters can be deployed in a VPC for secure intra-VPC communications

VPN or proxy required to connect from the internet (public domains are directly accessible)

Cannot use IP-based access policies

Limitations of VPC deployments:
• You can’t switch from VPC to a public endpoint. The reverse is also true
• You can’t launch your domain within a VPC that uses dedicated tenancy
• After you place a domain within a VPC, you can’t move it to a different VPC, but you can change the subnets and security group settings

#### OpenSearch Access Control
Resource-based policies – often called a domain access policy

Identity-based policies – attached to users or roles(principals)

IP-based policies – Restrict access to one or more IP addresses or CIDR blocks

Fine-grained access control – Provides:
• Role-based access control
• Security at the index, document, and field level
• OpenSearch Dashboards multi-tenancy
• HTTP basic authentication for OpenSearch and OpenSearch Dashboards

#### OpenSearch Access Control
Authentication options include:
• Federation using SAML to on-premises directories
• Amazon Cognito and social identity providers

#### OpenSearch Best Practices
Deploy OpenSearch data instances across three Availability Zones (AZs) for the best availability

Provision instances in multiples of three for equal distribution across AZs

If three AZs are not available use two AZs with equal numbers of instances

Use three dedicated master nodes

Configure at least one replica for each index

Apply restrictive resource-based access policies to the domain (or use fine-grained access control)

Create the domain within an Amazon VPC

For sensitive data enable node-to-node encryption and encryption at rest
### 🗂️ Deployment And Management
#### AWS CloudFormation
Infrastructure patterns are defined in a template file using code

CloudFormation builds your infrastructure according to the template

#### AWS CloudFormation - Benefits
Infrastructure is provisioned consistently, with fewer mistakes (human error)

Less time and effort than configuring resources manually

You can use version control and peer review for your CloudFormation templates

Free to use (you're only charged for the resources provisioned)

Can be used to manage updates and dependencies

Can be used to rollback and delete the entire stack as well

#### AWS CloudFormation Component
Templates - The JSON or YAML text file that contains the instructions for building out the AWS environment

Stacks - The entire environment described by the template and created, updated, and deleted as a single unit

StackSets - AWS CloudFormation StackSets extends the functionality of stacks by enabling you to create, update, or delete stacks across multiple accounts and regions with a single operation

Change Sets - A summary of proposed changes to your stack that will allow you to see how those changes might impact your existing resources before implementing them

AWS-management-console--services--Management and Governance-->cloudFormation-->create stack-->use-current-template-->upload template file(json and yaml)-->select file-->next-->stack name-->paramter file window-->next-->next-->create stack-->finished

AWS-management-console--services--Management and Governance-->cloudFormation-->select stack-->Stack Action-->create chnage set of current stack-->replace current template-->upload file-->select file-->next-->next-->create chnage set-->it will show chnages-->if you satisfied-->execute-->it will update the stack-->finished

#### AWS Elastic Beanstalk
Supports Java, .NET, PHP, Node.js, Python, Ruby, Go, and Docker web applications

Supports the following languages and development stacks:
• Apache Tomcat for Java applications
• Apache HTTP Server for PHP applications
• Apache HTTP Server for Python applications
• Nginx or Apache HTTP Server for Node.js applications
• Passenger or Puma for Ruby applications
• Microsoft IIS 7.5, 8.0, and 8.5 for .NET applications
• Java SE
• Docker
• Go

#### There are several layers
Applications:
• Contain environments, environment configurations, and application versions
• You can have multiple application versions held within an application

Application version
• A specific reference to a section of deployable code
• The application version will point typically to an Amazon S3 bucket containing the code

Environments:
• An application version that has been deployed on AWS resources
• The resources are configured and provisioned by AWS Elastic Beanstalk
• The environment is comprised of all the resources created by Elastic
Beanstalk and not just an EC2 instance with your uploaded code

#### Web Servers and Workers
Web servers are standard applications that listen for and then process HTTP requests, typically over port 80

Workers are specialized applications that have a background processing task that listens for messages on an Amazon SQS queue

Workers should be used for long-running tasks

AWS-management-console-->services-->EC2-->Elastic Beanstack-->create an application-->aoolication name:myapp-->Platform:Node.js-->configure more option-->preset:high Availability-->create app-->finished

#### SSM parameters store
Parameter Store provides secure, hierarchical storage for configuration data and secrets

Highly scalable, available, and durable

Store data such as passwords, database strings, and license codes as parameter values

Store values as plaintext (unencrypted data) or ciphertext (encrypted data)

Reference values by using the unique name that you specified when you created the parameter

No native rotation of keys (difference with AWS Secrets Manager which does it automatically)

#### AWS config
Evaluate your AWS resource configurations for desired settings

Get a snapshot of the current configurations of resources that are associated with your AWS account

Retrieve configurations of resources that exist in your account

Retrieve historical configurations of one or more resources

Receive a notification whenever a resource is created, modified, or deleted

View relationships between resources

AWS-management-console-->services-->Management and Governace-->config-->rules-->add rule-->select AWS managed rule-->next-->add rule-->finished

#### AWS Secrets Manager
Stores and rotate secrets safely without the need for code deployments

Secrets Manager offers automatic rotation of credentials (built-in) for:
• Amazon RDS (MySQL, PostgreSQL, and Amazon Aurora)
• Amazon Redshift
• Amazon DocumentDB
For other services you can write your own AWS Lambda function for automatic rotation

#### AWS Secrets Manager vs SSM Parameter Store
.                                   Secrets Manager                                SSM Parameter Store
Automatic Key Rotation   Yes, built-in for some services, use            No native key rotation; can use custom
.                            Lambda for others                               Lambda

Key/Value Type           String or Binary (encrypted)                    String, StringList, SecureString (encrypted)

Hierarchical Keys                         No                                                     Yes

Price                     Charges apply per secret                       Free for standard, charges for advanced

#### AWS OpsWorks
AWS OpsWorks is a configuration management service that provides managed instances of Chef and Puppet

Updates include patching, updating, backup, configuration and compliance management

SysOps Admin-------------->AWS OpsWorks------------------------->Instances are configured by OpsWorks using Chef/Puppet
.            <-Configuration changes are submitted to OpsWorks->

#### AWS Resource Access Manager (RAM)
Shares resources:
• Across AWS accounts
• Within AWS Organizations or OUs
• IAM roles and IAM users

Resource shares are created with:
• The AWS RAM Console
• AWS RAM APIs
• AWS CLI
• AWS SDKs

RAM can be used to share:
• AWS App Mesh
• Amazon Aurora
• AWS Certificate Manager Private Certificate Authority
• AWS CodeBuild
• Amazon EC2
• EC2 Image Builder
• AWS Glue
• AWS License Manager
• AWS Network Firewall
• AWS Outposts
• Amazon S3 on Outposts
• AWS Resource Groups
• Amazon Route 53
• AWS Systems Manager Incident Manager
• Amazon VPC

AWS-management-console-->services-->Resorce Access manager console-->setting-->settings-->Checkbox:Enable sharing with AWS organization-->save settings-->finished

AWS-management-console-->services-->Resorce Access manager console-->Resource Share-->Name-->Select Resource Type-->choose id of resource-->next-->next-->Allow sharing with principals in organization only-->select accoubt from AWS organization display structure-->next-->create Resource share-->finished
### 🗂️ Monitoring
#### Amazon CloudWatch
CloudWatch is used for performance monitoring, alarms, log collection and automated actions

Use cases / benefits include:
• Collect performance metrics from AWS and onpremises systems
• Automate responses to operational changes
• Improve operational performance and resource optimization
• Derive actionable insights from logs
• Get operational visibility and insight

#### CloudWatch Core Features:
CloudWatch Metrics – services send time-ordered data points to CloudWatch

CloudWatch Alarms – monitor metrics and initiate actions

CloudWatch Logs – centralized collection of system and application logs

CloudWatch Events – stream of system events describing changes to AWS resources and can trigger actions

#### Amazon CloudWatch Metrics
Metrics are sent to CloudWatch for many AWS services

EC2 metrics are sent every 5 minutes by default (free)

Detailed EC2 monitoring sends every 1 minute (chargeable)

Unified CloudWatch Agent sends system-level metrics for EC2 and on-premises servers

System-level metrics include memory and disk usage

Can publish custom metrics using CLI or API

Custom metrics are one of the following resolutions:
• Standard resolution – data having a one-minute granularity
• High resolution – data at a granularity of one second

AWS metrics are standard resolution by default

#### Amazon CloudWatch Alarms
Two types of alarms
• Metric alarm – performs one or more actions based on a single metric
• Composite alarm – uses a rule expression and takes into account multiple alarms

Metric alarm states:
• OK – Metric is within a threshold
• ALARM – Metric is outside a threshold
• INSUFFICIENT_DATA – not enough data

#### PutMetricData CLI command
aws cloudwatch put-metric-data --metric-name bytes --namespace MyCustomNameSpace --unit Bytes --value 242678092 --dimensions InstanceId=i-dshfdfh4785437,InstanceType=t2.micro --region us-east-1

aws cloudwatch put-metric-data --metric-name latency --namespace MyCustomNameSpace --unit Milliseconds --value 24 --dimensions InstanceId=i-dshfdfh4785437,InstanceType=t2.micro --region us-east-1

cloudwatch-management-console-->all-alarms-->create-alarm-->select-metric-->mycostomnamespace-->InstanceId,InstanceType-->select metrics-->select configuartion as reuirement-->next-->EC2-action-->In alarm-->Terminate this instance-->Next-->Alarm Name-->finished

#### Amazon CloudWatch Logs
Gather application and system logs in CloudWatch

Defined expiration policies and KMS encryption

Send to:
• Amazon S3 (export)
• Kinesis Data Streams
• Kinesis Data Firehose

Unified CloudWatch Agent installed on EC2 and onpremises servers

Function requires permissions to CloudWatch Logs

Real-time log processing with subscription filters

#### The Unified CloudWatch Agent
The unified CloudWatch agent enables you to do the following:
• Collect internal system-level metrics from Amazon EC2 instances across operating systems
• Collect system-level metrics from on-premises servers
• Retrieve custom metrics from your applications or services using the StatsD and collectd protocols
• Collect logs from Amazon EC2 instances and onpremises servers (Windows / Linux)

Agent must be installed on the server

Can be installed on:
• Amazon EC2 instances
• On-premises servers
• Linux, Windows Server, or macOS

#### AWS CloudTrail
CloudTrail logs API activity for auditing

By default, management events are logged and retained for 90 days

A CloudTrail Trail logs any events to S3 for indefinite retention

Trail can be within Region or all Regions

CloudWatch Events can triggered based on API calls in CloudTrail

Events can be streamed to CloudWatch Logs

#### CloudTrail – Types of Events
Management events - provide information about management operations that are performed on resources in your AWS account

Data events - provide information about the resource operations performed on or in a resource

Insights events - identify and respond to unusual activity associated with write API calls by continuously analyzing CloudTrail management events

AWS-management-console-->services-->Management&Governace-->AWS-cloudtrail-->create a trail-->storage location-->crate S3 bucket-->Trail log bucket & filetr-->Enable Cloudwatch log-->log group New-->log group name-->next-->Select management event in event type-->api activity:read and write-->next-->create trail-->finished

#### Amazon CloudWatch Events / EventBridge
EventBridge used to be known as CloudWatch Events

Event Sources------>Events----->EventBridge event bus----->Rules----->Targets
AWS Services
Custom Apps
SaaS Apps

Create Cloudtrail & Lambda Function first
AWS-management-console-->service-->Amazon EventBridge-->Events-->rules-->create rule-->name-->eventPattern-->pre-defined pattern by services-->select Event Bus:AWS default Event Bus,Enable the rule in selected event bus-->select target-->Lambda function-->select labda function name-->create-->finished

we can check in cloudwatch-->logs-->logsGroup-->select Log group-->select log stream-->log events info-->finished
### 🗂️ Security In The Cloud
#### AWS Managed Microsoft AD(Active directory service)
Synchronize users and federate identities with Azure/O365

Also Allows you to:
• Apply group policy
• Use single sign-on to apps and services
• Enable MFA with RADIUS

Managed implementation of Microsoft Active Directory running on Windows Server in AWS data centre

HA pair of Windows Server Domain Controllers (DCs)

One or twoway trust relationship

Securely connect to Amazon EC2 Linux and Windows instances

Example apps and services that support authentication and authorization using AWS Directory Service

Fully managed AWS service

Best choice if you have more than 5000 users and/or need a trust relationship set up

Can perform schema extensions

Can setup trust relationships to with on-premises Active Directories:
• On-premise users and groups can access resources in either domain using SSO
• Requires a VPN or Direct Connect connection

Can be used as a standalone AD in the AWS cloud

#### AD Connector
Self-managed Microsoft AD

Connect over VPN or Direct Connect

Provides federated sign-in to the AWS Management Console by mapping Active Directory identities to IAM Roles

Sign-in to AWS applications such as Amazon WorkSpaces, Amazon WorkDocs, and Amazon WorkMail by using your Active Directory credentials

Seamlessly join Windows EC2 instances to an onpremise AD domain

Redirects directory requests to your on-premise Active Directory

Best choice when you want to use an existing Active Directory with AWS services

AD Connector comes in two sizes:
• Small – designed for organizations up to 500 users
• Large – designed for organizations up to 5000 users

Requires a VPN or Direct Connect connection

Join EC2 instances to your on-premise AD through AD Connector

Login to the AWS Management Console using your on-premise AD DCs for authentication

#### Simple AD
Inexpensive Active Directory-compatible service with common directory features

Standalone, fully managed, directory on the AWS cloud

Simple AD is generally the least expensive option

Best choice for less than 5000 users and don’t need advanced AD features

Features include:
• Manage user accounts / groups
• Apply group policies
• Kerberos-based SSO
• Supports joining Linux or Windows based EC2 instances

#### Identity Federation steps by steps illustration
1. Client application attempts to authenticate using IdP
2. IdP authenticates the user
3. IdP sends client SAML assertion
4. App calls sts:AssumeRoleWithSAML
5. AWS return temporary security credentials
6. App uses credentials to access S3 bucket

#### IAM fedaration
SAML 2.0 compatible LDAP source (AD + ADFS)

Identity provider is configured in AWS IAM - Either SAML or OIDC

Web Identity Federation for mobile apps uses OpenID Connect (OIDC)

AWS recommend to use Cognito for web identity federation in most cases

Authenticated and authorized users can access AWS services

#### AWS Single Sign-on (SSO)
Identity sources can be AWS SSO, Active Directory and standard providers using SAML 2.0

Enables centralized permissions management

Built-in SSO integrations to business applications

Connect AWS accounts and Organizations

#### Amazon Congnito
adding user sign-in and sign-off functionality

#### Cognito User Pools
A User Pool is a directory for managing sign-in and sign-up for mobile applications

Cognito acts as an Identity Broker between the IdP and AWS

Users can also sign in using social IdPs

API Gateway used for application

Lambda authorizer accepts JWT

#### Cognito Identity Pool
Identity pools are used to obtain temporary, limited-privilege credentials for AWS services

Identity pools use AWS STS to obtain the credentials

Identities can come from a Cognito user pool

Identities can come from social IdPs

An IAM role is assumed providing access to the AWS services

#### AWS Key Management Service (KMS)
Customer Master Keys (CMKs)
• Customer master keys are the primary resources in AWS KMS
• The CMK also contains the key material used to encrypt and decrypt data
• CMKs are created in AWS KMS
• Symmetric CMKs and the private keys of asymmetric CMKs never leave AWS KMS unencrypted
• By default, AWS KMS creates the key material for a CMK
• Can also import your own key material
• A CMK can encrypt data up to 4KB in size
• A CMK can generate, encrypt and decrypt Data Encryption Keys
• Data Encryption Keys can be used for encrypting large amounts of data
Type of CMK             Can view          Can manage             Used only for my AWS account          Automatic rotation
Customer managed CMK      Yes               Yes                          Yes                           Optional. Every 365 days
AWS managed CMK           Yes               No                           Yes                          Required. Every 1095 days
AWS owned CMK             No                No                           No                                      Varies

AWS Managed CMKs
• Created, managed, and used on your behalf by an AWS service that is integrated with AWS KMS
• You cannot manage these CMKs, rotate them, or change their key policies
• You also cannot use AWS managed CMKs in cryptographic operations directly; the service that creates them uses them on your behalf

Data Encryption Keys
• Data keys are encryption keys that you can use to encrypt data, including large amounts of data and other data encryption keys
• You can use AWS KMS customer master keys (CMKs) to generate, encrypt, and decrypt data keys
• AWS KMS does not store, manage, or track your data keys, or perform cryptographic operations with data keys
• You must use and manage data keys outside of AWS KMS

AWS-management-console-->key-management-service(KMS)-->customer-managed-key-->create key-->configure key:key type:Symmetric-->KMS-->next-->aias-->next-->define-key-administrator-permission-->allow-key-administrator-to-delete-the-key-->next-->define key usage permission-->next-->finish-->finished

#### AWS CloudHSM
AWS CloudHSM is a cloud-based hardware security module(HSM)

Generate and use your own encryption keys on the AWS Cloud

CloudHSM runs in your Amazon VPC

Uses FIPS 140-2 level 3 validated HSMs

Managed service and automatically scales

Retain control of your encryption keys - you control access (and AWS has no visibility of your encryption keys)

#### AWS CloudHSM Use Cases
• Offload SSL/TLS processing from web servers
• Protect private keys for an issuing certificate authority (CA)
• Store the master key for Oracle DB Transparent Data Encryption
• Custom key store for AWS KMS – retain control of the HSM that protects the master keys

#### AWS Certificate Manager(ACM)
Create, store and renew SSL/TLS X.509 certificates

Single domains, multiple domain names and wildcards

Integrates with several AWS services including:
• Elastic Load Balancing
• Amazon CloudFront
• AWS Elastic Beanstalk
• AWS Nitro Enclaves
• AWS CloudFormation

Public certificates are signed by the AWS public Certificate Authority

You can also create a Private CA with ACM

Can then issue private certificates

You can also import certificates from third-party issuers

AWS-management-console-->service-->ACM-->request a certificate-->request public certificate-->request-certificate-->add domain name-->next-->DNS/email validation-->finished

#### AWS Web Application Firewall (WAF)
AWS WAF is a web application firewall

WAF lets you create rules to filter web traffic based on conditions that include IP addresses, HTTP headers and body, or custom URIs

WAF makes it easy to create rules that block common web exploits like SQL injection and cross site scripting

#### AWS WAF
Web ACLs – You use a web access control list (ACL) to protect a set of AWS resources

Rules – Each rule contains a statement that defines the inspection criteria, and an action to take if a web request meets the criteria

Rule groups – You can use rules individually or in reusable rule groups

IP Sets - An IP set provides a collection of IP addresses and IP address ranges that you want to use together in a rule statement

Regex pattern set - A regex pattern set provides a collection of regular expressions that you want to use together in a rule
statement

A rule action tells AWS WAF what to do with a web request when it matches the criteria defined in the rule:
• Count – AWS WAF counts the request but doesn't determine whether to allow it or block it. With this action, AWS WAF
continues processing the remaining rules in the web ACL

• Allow – AWS WAF allows the request to be forwarded to the AWS resource for processing and response

• Block – AWS WAF blocks the request and the AWS resource responds with an HTTP 403 (Forbidden) status code

#### AWS Shield
AWS Shield is a managed Distributed Denial of Service(DDoS) protection service

Safeguards web application running on AWS with always-on detection and automatic inline mitigations

Helps to minimize application downtime and latency
Two tiers –
• Standard – no cost
• Advanced - $3k USD per month and 1 year commitment

Integrated with Amazon CloudFront (standard included by default)

#### Amazon Macie
Macie is a fully managed data security and data privacy service

Uses machine learning and pattern matching to discover, monitor, and help you protect your sensitive data on Amazon S3

Macie enables security compliance and preventive security as follows:
• Identify a variety of data types, including PII, Protected Health Information (PHI), regulatory documents, API keys, and secret keys
• Identify changes to policy and access control lists
• Continuously monitor the security posture of Amazon S3
• Generate security findings that you can view using the Macie console, AWS Security Hub, or Amazon EventBridge
• Manage multiple AWS accounts using AWS Organizations

#### Amazon Inspector
Runs assessments that check for security exposures and vulnerabilities in EC2 instances

Can be configured to run on a schedule

Agent must be installed on EC2 for host assessments

Network assessments do not require an agent

Network Assessments
• Assessments: Network configuration analysis to check for ports reachable from outside the VPC
• If the Inspector Agent is installed on your EC2 instances, the assessment also finds processes reachable on port
• Price based on the number of instance assessments

Host Assessments
• Assessments: Vulnerable software (CVE), host hardening (CIS benchmarks), and security best practices
• Requires an agent (auto-install with SSM Run Command)
• Price based on the number of instance assessments

#### AWS GuardDuty
Intelligent threat detection service

Detects account compromise, instance compromise, malicious reconnaissance, and bucket compromise

Continuous monitoring for events across:
• AWS CloudTrail Management Events
• AWS CloudTrail S3 Data Events
• Amazon VPC Flow Logs
• DNS Logs
### 🗂️ Migration And Transfer Services
#### AWS Migration Tools
Collect data about servers in on-premises DC

Monitor migrations that use AWS or partner tools

#### AWS Application Discovery Service

#### AWS Database Migration Service (DMS)
Use the Schema Conversion Tool for heterogeneous migrations

Destinations include Aurora, RedShift DynamoDB, and DocumentDB

#### AWS DMS Use Cases
Cloud to Cloud – EC2 to RDS, RDS to RDS, RDS to Aurora

On-Premises to Cloud

Homogeneous migrations – Oracle to Oracle, MySQL to RDS
MySQL, Microsoft SQL to RDS for SQL Server

Heterogeneous migrations – Oracle to Aurora, Oracle to PostgreSQL, Microsoft SQL to RDS MySQL (must convert schema first wit the Shema Conversion Tool (SCT))

Development and Test – use the cloud for dev/test workloads

Database consolidation – consolidate multiple source DBs to a single target DB

Continuous Data Replication – use for DR, dev/test, single source multi-target or multi-source single target

#### AWS Server Migration Service (SMS)
AWS SMS migrates VMware vSphere, Microsoft Hyper-V/SCVMM, and Azure virtual machines to Amazon EC2

#### AWS SMS – Application Migration
Entire application group is launched from AMIs using CloudFormation template

#### AWS DataSync
DataSync agent installed on Snowcone

DataSync software agent connects to storage system

Data is encrypted in transit with TLS

Scheduled, automated data transfer

#### AWS Snow Family
AWS Snowball and Snowmobile - are used for migrating large volumes of data to AWS

Snowball Edge Compute Optimized
• Provides block and object storage and optional GPU
• Use for data collection, machine learning and processing, and storage in environments with intermittent connectivity (edge
use cases)

Snowball Edge Storage Optimized
• Provides block storage and Amazon S3-compatible object storage
• Use for local storage and large-scale data transfer

Snowcone
• Small device used for edge computing, storage and data transfer
• Can transfer data offline or online with AWS DataSync agent

#### AWS Snowball Family
Uses a secure storage device for physical transportation

Snowball Client is software that is installed on a local computer and is used to identify, compress, encrypt, and transfer data

Uses 256-bit encryption (managed with the AWS KMS) and tamper-resistant enclosures with TPM

Snowball (80TB) (50TB ) “petabyte scale”

Snowball Edge (100TB) “petabyte scale”

Snowmobile – “exabyte scale” with up to 100PB per Snowmobile

#### Ways to optimize the performance of Snowball transfers:
1. Use the latest Mac or Linux Snowball client
2. Batch small files together
3. Perform multiple copy operations at one time
4. Copy from multiple workstations
5. Transfer directories, not files

#### AWS Snowball Use Cases
Cloud data migration – migrate data to the cloud

Content distribution – send data to clients or customers

Tactical Edge Computing – collect data and compute

Machine learning – run ML directly on the device

Manufacturing – data collection and analysis in the factory

Remote locations with simple data – preprocessing, tagging, compression etc.
