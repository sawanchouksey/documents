# AWS SSM Manager Integration for Docker-based Development Environments

<img src="https://sawanchouksey.github.io/documents/blob/main/docs/Cloud/ec2ssmdocker.png?raw=true" title="SSM Manager Integration" alt="SSM Manager Integration" data-align="center">

This guide outlines the complete setup process for implementing AWS Systems Manager (SSM) for EC2 instances running containerized SIT and QA environments with Docker.

## Prerequisites
- An AWS account with administrator access
- Basic knowledge of AWS services, Docker, and containerization
- Terraform or CloudFormation (optional for IaC deployment)

## Part 1: SSM Setup (Before Environment Deployment)

### Step 1: Create 4 VPC Endpoints with Interface Endpoint Type
1. In the AWS Management Console, navigate to **VPC** > **Endpoints**.
2. Create 4 VPC endpoints with the **Interface** type for services like SSM, EC2, etc.
   - Select the required service names for each endpoint (for example, **com.amazonaws.region.ssm** for SSM).
   - Choose the correct VPC and subnet.
   - <img src="https://sawanchouksey.github.io/documents/blob/main/docs/Cloud/ssmendpoints.jpg?raw=true" title="SSMEndpoints" alt="SSMEndpoints">

### Step 2: Create Inbound Rule for HTTPS (443) for Security Group (SG)
1. Go to **EC2** > **Security Groups**.
2. Select your security group and add an inbound rule.
   - Protocol: **HTTPS**
   - Port range: **443**
   - Source: **0.0.0.0/0** (or your specific source IP range)

### Step 3: Create IAM Role for EC2 Instances with SSM Permissions
1. Navigate to the **IAM Console** > **Roles** > **Create Role**.
2. Select **AWS Service** and then **EC2** as the use case.
3. Attach the following policies:
   - `AmazonSSMManagedInstanceCore` (required for SSM)
   - `AmazonEC2RoleforSSM` (optional for extended functionality)
4. Name the role `EC2-Docker-SSM-Role` and click **Create Role**.

### Step 4: Attach IAM Role to EC2 Instance
1. When launching your EC2 instance, assign the **EC2-Docker-SSM-Role** IAM role.
2. If the EC2 instance is already created, attach the IAM role using the EC2 console under **Actions** > **Security** > **Modify IAM Role**.

### Step 5: Check and Install SSM Agent in EC2 Instance
1. **If using Amazon Linux 2**: The SSM agent is pre-installed. You can verify its status:
   ```bash
   sudo systemctl status amazon-ssm-agent
   ```
2. **For non-Amazon Linux 2 instances**: You may need to manually install the SSM agent by running the following commands:
   ```bash
   sudo yum install -y https://amazon-ssm-<region>.s3.amazonaws.com/latest/linux_amd64/amazon-ssm-agent.rpm
   sudo systemctl enable amazon-ssm-agent
   sudo systemctl start amazon-ssm-agent
   ```

### Step 6: Create EC2 Instance Without SSH Port, Key Pair, or Public IP
1. Launch an EC2 instance without enabling SSH (port 22) and without a key pair or public IP.
2. Make sure the instance is in a private subnet or has no direct internet access.
3. If there's an existing EC2 instance, delete any SSH keys, public IPs, or associated security groups for compliance.

### Step 7: Reboot or Restart the EC2 Instance After Changes
1. After making the changes (such as attaching IAM roles and configuring the instance), reboot the EC2 instance to apply the new configurations.
2. This ensures the changes take effect properly.

### Step 8: Wait for 5-10 Minutes for the SSM "Connect" Button to Appear in the Session Manager Console
1. After rebooting, wait for **5-10 minutes** for the instance to appear in **Systems Manager** > **Session Manager** > **Managed Instances**.
2. You should see the **Connect** button appear next to the instance once it's ready for use.

## Part 2: SSM Setup (Before Environment Deployment)
### Step 1: Create IAM Role for SSM Access
1. Navigate to the IAM console at [IAM Console](https://console.aws.amazon.com/iam/)
2. Choose **Roles** > **Create Role**
3. Select **AWS Service** as the trusted entity type
4. Choose **EC2** as the use case
5. Attach the following policies:
   - `AmazonSSMManagedInstanceCore` (required)
   - `AmazonEC2RoleforSSM` (optional, for expanded functionality)
6. Name your role `EC2-Docker-SSM-Role`
7. Click **Create Role**

### Step 2: Create EC2 Launch Template with SSM Enabled
1. Go to the EC2 Console: [EC2 Dashboard](https://console.aws.amazon.com/ec2/)
2. Select **Launch Templates** from the left menu
3. Click **Create launch template**
4. Configure the following:
   - Name: `docker-dev-environments-template`
   - AMI: Amazon Linux 2 (has SSM agent pre-installed)
   - Instance type: t3.large (or appropriate size for your workload)
   - Key pair: (optional - with SSM you don't need SSH keys)
   - Network settings: Select your VPC and subnet
   - Security group: Create one that allows HTTP (80), custom port (8080), and **NO** SSH (22)
   - IAM instance profile: Select `EC2-Docker-SSM-Role`
   - Advanced details:
     - User data:
       ```bash
       #!/bin/bash
       # Update system
       yum update -y
       
       # Install Docker
       amazon-linux-extras install docker -y
       systemctl start docker
       systemctl enable docker
       
       # Install Docker Compose
       curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
       chmod +x /usr/local/bin/docker-compose
       
       # Verify SSM agent is running
       systemctl status amazon-ssm-agent
       systemctl enable amazon-ssm-agent
       ```
5. Click **Create launch template**

### Step 3: Configure SSM Session Manager Preferences
1. Navigate to the Systems Manager Console
2. Under **Session Manager**, select **Preferences**
3. Configure the following optional settings:
   - Enable **CloudWatch logging** for audit purposes
   - Configure **KMS encryption** for session data
   - Set **Session timeout** to your organization's requirements
4. Click **Save**

---

## Part 2: Deploy Docker Environment Structure

### Step 1: Launch EC2 Instance
1. Use the launch template created above to provision your EC2 instance
2. Tag the instance appropriately (e.g., Name: `docker-sit-qa-environments`)

### Step 2: Verify SSM Connection
1. Go to **Systems Manager** > **Fleet Manager**
2. Confirm your instance appears in the managed instances list
3. Test connection by starting a session:
   - Go to **Session Manager** > **Start session**
   - Select your instance and click **Start session**
   - Run `sudo systemctl status docker` to verify Docker is running

### Step 3: Set Up Docker Environment Structure
Using Session Manager, connect to your instance and create the following directory structure:

```bash
mkdir -p /opt/docker-environments
cd /opt/docker-environments
mkdir -p sit qa
```

### Step 4: Create Docker Compose Files
1. Create SIT environment configuration:
```bash
cat > /opt/docker-environments/sit/docker-compose.yml << 'EOF'
version: '3.8'

networks:
  sit_bridge_network:
    driver: bridge

services:
  nginx:
    image: nginx:latest
    container_name: SIT_Nginx
    ports:
      - "80:80"
    networks:
      - sit_bridge_network
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
    restart: always
    
  frontend:
    image: your-frontend-image:latest
    container_name: SIT_FrontEnd
    networks:
      - sit_bridge_network
    environment:
      - NODE_ENV=sit
    restart: always
    
  backend:
    image: your-backend-image:latest
    container_name: SIT_BackEnd
    networks:
      - sit_bridge_network
    environment:
      - NODE_ENV=sit
      - DB_HOST=mysql
      - DB_SCHEMA=sit_db
    restart: always

volumes:
  mysql_data:
EOF
```

2. Create QA environment configuration:
```bash
cat > /opt/docker-environments/qa/docker-compose.yml << 'EOF'
version: '3.8'

networks:
  qa_bridge_network:
    driver: bridge

services:
  nginx:
    image: nginx:latest
    container_name: QA_Nginx
    ports:
      - "8080:80"
    networks:
      - qa_bridge_network
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
    restart: always
    
  frontend:
    image: your-frontend-image:latest
    container_name: QA_FrontEnd
    networks:
      - qa_bridge_network
    environment:
      - NODE_ENV=qa
    restart: always
    
  backend:
    image: your-backend-image:latest
    container_name: QA_BackEnd
    networks:
      - qa_bridge_network
    environment:
      - NODE_ENV=qa
      - DB_HOST=mysql
      - DB_SCHEMA=qa_db
    restart: always

volumes:
  mysql_data:
EOF
```

<!-- 3. Create shared MySQL service configuration:
```bash
cat > /opt/docker-environments/docker-compose.yml << 'EOF'
version: '3.8'

networks:
  shared_network:
    driver: bridge

services:
  mysql:
    image: mysql:8.0
    container_name: Shared_MySQL
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=secure_password
      - MYSQL_DATABASE=sit_db
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql/init:/docker-entrypoint-initdb.d
    networks:
      - shared_network
    restart: always

volumes:
  mysql_data:
EOF
``` -->

### Step 5: Configure Nginx for Each Environment
1. Set up SIT Nginx configuration:
```bash
mkdir -p /opt/docker-environments/sit/nginx/conf.d
cat > /opt/docker-environments/sit/nginx/conf.d/default.conf << 'EOF'
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
```

2. Set up QA Nginx configuration:
```bash
mkdir -p /opt/docker-environments/qa/nginx/conf.d
cat > /opt/docker-environments/qa/nginx/conf.d/default.conf << 'EOF'
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
```
## Part 4: Security Considerations

### Step 1: Configure Security Groups
1. Ensure the EC2 instance security group:
   - Allows inbound traffic only on ports 80 (SIT) and 8080 (QA)
   - Blocks all SSH access (port 22)
   - Allows outbound internet access for updates and container pulls

### Step 2: Implement SSM Parameter Store for Secrets
1. Store sensitive information (database passwords, API keys) in SSM Parameter Store:
```bash
# Example commands using Session Manager
aws ssm put-parameter \
    --name "/docker-env/mysql/root-password" \
    --value "secure_password" \
    --type "SecureString"

aws ssm put-parameter \
    --name "/docker-env/sit/api-key" \
    --value "sit-api-key-value" \
    --type "SecureString"
```

2. Create an SSM document to refresh environment variables:
   - Name: `Update-Environment-Secrets`
   - Document type: `Command document`
   - Content to pull secrets and update docker-compose files

## Part 5: Cost Optimization

### Step 1: Set Up Auto Scaling Based on Usage Patterns
1. Create an SSM Automation document for instance scaling:
   - Scale down instance type during non-business hours
   - Scale up during work hours
   - Implement through AWS Lambda or EventBridge rules

### Step 2: Implement Monitoring for Cost Analysis
1. Create CloudWatch Dashboard for resource utilization tracking
2. Set up AWS Budgets alerts for cost thresholds

## Part 6: Maintenance and Operations

### Step 1: Create Regular Backup Procedures
1. Create an SSM document for database backups:
   - Name: `Backup-Docker-Environments`
   - Schedule daily execution
   - Store backups in S3 with lifecycle policies

### Step 2: Create Update Procedures
1. Create an SSM document for container updates:
   - Name: `Update-Docker-Images`
   - Pull latest images and rebuild environments

## Conclusion

This implementation provides a secure, cost-effective, and manageable approach to running SIT and QA environments on a single EC2 instance using Docker. By leveraging AWS SSM, you eliminate the need for direct SSH access while maintaining full administrative control over your instances and containerized applications.

Key benefits of this approach:
- Enhanced security through elimination of SSH access
- Cost optimization by consolidating environments on a single instance
- Simplified management through SSM documents and automation
- Consistent environment configuration through Docker
- Scalable architecture that can grow as development needs increase

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚