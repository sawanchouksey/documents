# Complete Guide: Create & Upgrade RDS PostgreSQL 14 to 16 using Blue/Green Deployment

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Project Structure](#project-structure)
5. [Complete Source Code](#complete-source-code)
6. [Step-by-Step Deployment](#step-by-step-deployment)
7. [Blue/Green Upgrade Process](#bluegreen-upgrade-process)
8. [Testing & Validation](#testing--validation)
9. [Troubleshooting](#troubleshooting)
10. [Cost Optimization](#cost-optimization)
11. [Security Best Practices](#security-best-practices)

---

## 1. Overview

This comprehensive guide provides everything you need to:

✅ **Deploy** RDS PostgreSQL 14.17 with Terraform  
✅ **Configure** production-ready security and networking  
✅ **Upgrade** from PostgreSQL 14.17 to 16.x using Blue/Green deployment  
✅ **Test** database connectivity and performance  
✅ **Monitor** deployment status and health  
✅ **Rollback** if needed with minimal downtime  

### Key Features

- **Infrastructure as Code**: Complete Terraform configuration
- **Zero-Downtime Upgrade**: AWS Blue/Green deployment
- **Cost-Optimized**: Free tier eligible (db.t3.micro)
- **Secure**: VPC isolation, encrypted storage, IP whitelisting
- **Automated**: One-command deployment and upgrade
- **Production-Ready**: Monitoring, backups, logging enabled

### What is Blue/Green Deployment?

```
┌─────────────────┐          ┌─────────────────┐
│  Blue (v14.17)  │  Clone   │  Green (v16.x)  │
│   Production    │─────────▶│   Testing       │
│   Database      │ Replicate│   Database      │
└────────┬────────┘          └────────┬────────┘
         │                            │
         │      ◀── Switchover ──     │
         │         (< 1 min)          │
         ▼                            ▼
    Old Prod                     New Prod
```

**Benefits:**
- < 1 minute downtime during switchover
- Test upgrade before production cutover
- Easy rollback if issues detected
- No data loss with binary replication

---

## 2. Architecture

### Infrastructure Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                     AWS Region: ap-south-1                    │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                VPC (vpc-0cbc028b5d53643ef)             │  │
│  │                                                          │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │  │
│  │  │ Subnet-1a    │  │ Subnet-1b    │  │ Subnet-1c    │ │  │
│  │  │ Public       │  │ Public       │  │ Public       │ │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │  │
│  │         │                 │                 │          │  │
│  │         └─────────────────┴─────────────────┘          │  │
│  │                           │                             │  │
│  │                  ┌────────▼────────┐                    │  │
│  │                  │  RDS PostgreSQL │                    │  │
│  │                  │   db.t3.micro   │                    │  │
│  │                  │  PostgreSQL 14  │                    │  │
│  │                  │   20GB Storage  │                    │  │
│  │                  │   Encrypted     │                    │  │
│  │                  └────────┬────────┘                    │  │
│  │                           │                             │  │
│  │                  ┌────────▼────────┐                    │  │
│  │                  │ Security Group  │                    │  │
│  │                  │  Port: 5432     │                    │  │
│  │                  │  IP Whitelist   │                    │  │
│  │                  └─────────────────┘                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  Internet ◀──────── Internet Gateway ────────▶ RDS Instance  │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### Components

| Component | Configuration | Purpose |
|-----------|--------------|---------|
| **RDS Instance** | db.t3.micro, PostgreSQL 14.17 | Main database server |
| **Storage** | 20GB GP3, encrypted | Database storage |
| **VPC** | Default VPC | Network isolation |
| **Subnets** | 3 public subnets across AZs | High availability |
| **Security Group** | Port 5432, IP whitelist | Access control |
| **Parameter Group** | postgres14/postgres16 | Database configuration |
| **Backup** | 7-day retention | Data protection |
| **Monitoring** | CloudWatch logs | Observability |

---

## 3. Prerequisites

### Required Software

```powershell
# Windows PowerShell
# Check installations:
terraform --version    # Should be >= 1.0
aws --version         # Should be >= 2.0
python --version      # Should be >= 3.7
psql --version        # PostgreSQL client
```

### AWS Account Requirements

- ✅ AWS account with admin or RDS permissions
- ✅ VPC with at least 2 subnets in different AZs
- ✅ AWS CLI configured with credentials
- ✅ SSH key pair (optional, for EC2 bastion)

### Network Requirements

- ✅ Public internet access OR VPN to AWS
- ✅ Port 5432 allowed for outbound connections
- ✅ Static or whitelisted IP address

### Knowledge Prerequisites

- Basic understanding of AWS RDS
- Familiarity with Terraform
- PostgreSQL basics
- Command line proficiency

---

## 4. Project Structure

```
auroraRdsPostgresUpgrade/
│
├── main.tf                          # Main RDS instance configuration
├── variables.tf                      # Variable definitions
├── outputs.tf                        # Output definitions
├── blue-green-upgrade.tf            # Blue/Green deployment config
├── terraform.tfvars                 # Current configuration values
├── terraform-upgrade.tfvars         # Upgrade configuration example
│
├── test_rds_connection.py           # Simple connection test
├── rds_postgres_testing_failover.py # Advanced failover testing
│
├── README.md                         # Quick start guide
├── BLUE_GREEN_UPGRADE_GUIDE.md      # Detailed upgrade guide
├── TROUBLESHOOTING.md               # Troubleshooting reference
└── Create_Upgrade_Aurora_RDS_14_to_16_BlueGreen_Deployment.md  # This file
```

---

## 5. Complete Source Code

### 5.1 main.tf

**Purpose:** Main Terraform configuration for RDS PostgreSQL instance

```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# DB Subnet Group
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "${var.db_identifier}-subnet-group"
  subnet_ids = var.subnet_ids

  tags = merge(
    var.tags,
    {
      Name = "${var.db_identifier}-subnet-group"
    }
  )
}

# Security Group for RDS
resource "aws_security_group" "rds_sg" {
  name        = "${var.db_identifier}-sg"
  description = "Security group for RDS PostgreSQL instance"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
    description = "PostgreSQL access"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.db_identifier}-sg"
    }
  )
}

# RDS Parameter Group for PostgreSQL 14
resource "aws_db_parameter_group" "postgres_pg" {
  name        = "${var.db_identifier}-pg"
  family      = "postgres14"
  description = "PostgreSQL 14 parameter group"

  parameter {
    name  = "log_statement"
    value = "all"
  }

  parameter {
    name  = "log_min_duration_statement"
    value = "1000"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.db_identifier}-pg"
    }
  )
}

# RDS PostgreSQL Instance
resource "aws_db_instance" "postgres" {
  identifier     = var.db_identifier
  engine         = "postgres"
  engine_version = var.engine_version
  instance_class = var.instance_class

  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = var.database_name
  username = var.master_username
  password = var.master_password

  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  parameter_group_name   = aws_db_parameter_group.postgres_pg.name

  publicly_accessible = var.publicly_accessible
  multi_az            = var.multi_az

  backup_retention_period         = var.backup_retention_period
  backup_window                   = var.preferred_backup_window
  maintenance_window              = var.preferred_maintenance_window
  enabled_cloudwatch_logs_exports = var.enabled_cloudwatch_logs_exports

  skip_final_snapshot       = var.skip_final_snapshot
  final_snapshot_identifier = var.skip_final_snapshot ? null : "${var.db_identifier}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"

  apply_immediately = var.apply_immediately

  # Disable performance insights and enhanced monitoring for cost savings
  performance_insights_enabled = false
  monitoring_interval          = 0

  # Auto minor version upgrade
  auto_minor_version_upgrade = true

  # Deletion protection (set to true for production)
  deletion_protection = false

  tags = merge(
    var.tags,
    {
      Name = var.db_identifier
    }
  )

  lifecycle {
    ignore_changes = [final_snapshot_identifier]
  }
}
```

### 5.2 variables.tf

**Purpose:** Define all input variables

```hcl
variable "aws_region" {
  description = "AWS region for RDS instance"
  type        = string
  default     = "ap-south-1"
}

variable "db_identifier" {
  description = "RDS instance identifier"
  type        = string
}

variable "engine_version" {
  description = "PostgreSQL engine version"
  type        = string
  default     = "14.17"
}

variable "database_name" {
  description = "Name of the default database"
  type        = string
}

variable "master_username" {
  description = "Master username for the database"
  type        = string
  sensitive   = true
}

variable "master_password" {
  description = "Master password for the database"
  type        = string
  sensitive   = true
}

variable "instance_class" {
  description = "Instance class for RDS instance"
  type        = string
  default     = "db.t3.micro"
}

variable "allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
  default     = 20
}

variable "max_allocated_storage" {
  description = "Maximum storage for autoscaling (0 to disable)"
  type        = number
  default     = 100
}

variable "vpc_id" {
  description = "VPC ID where RDS instance will be created"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for RDS instance"
  type        = list(string)
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks or IP addresses allowed to access the database (use x.x.x.x/32 for specific IPs)"
  type        = list(string)
  default     = []
}

variable "publicly_accessible" {
  description = "Whether the instance is publicly accessible"
  type        = bool
  default     = false
}

variable "backup_retention_period" {
  description = "Backup retention period in days"
  type        = number
  default     = 1
}

variable "preferred_backup_window" {
  description = "Preferred backup window"
  type        = string
  default     = "03:00-04:00"
}

variable "preferred_maintenance_window" {
  description = "Preferred maintenance window"
  type        = string
  default     = "sun:04:00-sun:05:00"
}

variable "skip_final_snapshot" {
  description = "Skip final snapshot when destroying instance"
  type        = bool
  default     = false
}

variable "apply_immediately" {
  description = "Apply changes immediately"
  type        = bool
  default     = false
}

variable "multi_az" {
  description = "Enable Multi-AZ deployment"
  type        = bool
  default     = false
}

variable "enabled_cloudwatch_logs_exports" {
  description = "List of log types to export to CloudWatch"
  type        = list(string)
  default     = ["postgresql", "upgrade"]
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

# Blue/Green Deployment Variables
variable "enable_blue_green_upgrade" {
  description = "Enable blue/green deployment for major version upgrade"
  type        = bool
  default     = false
}

variable "target_engine_version" {
  description = "Target PostgreSQL version for blue/green upgrade (e.g., 16.1)"
  type        = string
  default     = "16.1"
}

variable "target_instance_class" {
  description = "Target instance class for blue/green upgrade (optional, defaults to current)"
  type        = string
  default     = null
}
```

### 5.3 outputs.tf

**Purpose:** Define output values to display after deployment

```hcl
output "db_instance_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "db_instance_address" {
  description = "RDS instance address (hostname)"
  value       = aws_db_instance.postgres.address
}

output "db_instance_arn" {
  description = "RDS instance ARN"
  value       = aws_db_instance.postgres.arn
}

output "db_instance_id" {
  description = "RDS instance identifier"
  value       = aws_db_instance.postgres.id
}

output "db_port" {
  description = "Database port"
  value       = aws_db_instance.postgres.port
}

output "database_name" {
  description = "Database name"
  value       = aws_db_instance.postgres.db_name
}

output "security_group_id" {
  description = "Security group ID for RDS instance"
  value       = aws_security_group.rds_sg.id
}

output "db_instance_status" {
  description = "RDS instance status"
  value       = aws_db_instance.postgres.status
}

output "db_instance_resource_id" {
  description = "RDS instance resource ID"
  value       = aws_db_instance.postgres.resource_id
}

output "connection_string" {
  description = "PostgreSQL connection string (without password)"
  value       = "postgresql://${var.master_username}:<password>@${aws_db_instance.postgres.endpoint}/${var.database_name}"
  sensitive   = true
}
```

### 5.4 blue-green-upgrade.tf

**Purpose:** Blue/Green deployment configuration for major version upgrade

```hcl
# Blue/Green Deployment for RDS PostgreSQL Major Version Upgrade
# This configuration supports upgrading from PostgreSQL 14.17 to 16.x

# Target Parameter Group for PostgreSQL 16
resource "aws_db_parameter_group" "postgres_pg_v16" {
  count       = var.enable_blue_green_upgrade ? 1 : 0
  name        = "${var.db_identifier}-pg-v16"
  family      = "postgres16"
  description = "PostgreSQL 16 parameter group for blue/green upgrade"

  parameter {
    name  = "log_statement"
    value = "all"
  }

  parameter {
    name  = "log_min_duration_statement"
    value = "1000"
  }

  tags = merge(
    var.tags,
    {
      Name    = "${var.db_identifier}-pg-v16"
      Purpose = "Blue-Green-Upgrade"
    }
  )
}

# Blue/Green Deployment Resource
# Note: This creates a copy of your database and upgrades it
resource "aws_rds_blue_green_deployment" "postgres_upgrade" {
  count = var.enable_blue_green_upgrade ? 1 : 0

  blue_green_deployment_name = "${var.db_identifier}-to-pg16"
  source_arn                 = aws_db_instance.postgres.arn
  target_engine_version      = var.target_engine_version

  # Use the new parameter group for PostgreSQL 16
  target_db_parameter_group_name = aws_db_parameter_group.postgres_pg_v16[0].name

  # Optional: Upgrade DB instance class during migration
  # target_db_instance_class = var.target_instance_class

  tags = merge(
    var.tags,
    {
      Name        = "${var.db_identifier}-blue-green-upgrade"
      Source      = var.engine_version
      Target      = var.target_engine_version
      Environment = "blue-green-deployment"
    }
  )
}

# Output the Blue/Green deployment status
output "blue_green_deployment_id" {
  description = "ID of the Blue/Green deployment"
  value       = var.enable_blue_green_upgrade ? aws_rds_blue_green_deployment.postgres_upgrade[0].id : null
}

output "blue_green_deployment_arn" {
  description = "ARN of the Blue/Green deployment"
  value       = var.enable_blue_green_upgrade ? aws_rds_blue_green_deployment.postgres_upgrade[0].arn : null
}

output "blue_green_deployment_status" {
  description = "Status of the Blue/Green deployment"
  value       = var.enable_blue_green_upgrade ? aws_rds_blue_green_deployment.postgres_upgrade[0].status : null
}

output "green_environment_endpoint" {
  description = "Endpoint of the green (upgraded) environment"
  value       = var.enable_blue_green_upgrade ? try(aws_rds_blue_green_deployment.postgres_upgrade[0].target[0].endpoint, null) : null
}
```

### 5.5 terraform.tfvars

**Purpose:** Configuration values for initial deployment

```hcl
# AWS Region Configuration
aws_region = "ap-south-1" # Mumbai region

# RDS Instance Configuration
db_identifier  = "postgres-rds-instance"
engine_version = "14.17"
database_name  = "myappdb"

# Master Credentials
master_username = "postgres"
master_password = "Practice$123#Rds" # CHANGE THIS!

# Instance Configuration
instance_class        = "db.t3.micro" # Free tier eligible
allocated_storage     = 20            # Free tier: 20 GB
max_allocated_storage = 100           # Autoscaling up to 100 GB

# Multi-AZ Configuration
multi_az = false # Set to true for high availability

# Network Configuration
vpc_id = "vpc-0cbc028b5d53643ef" # UPDATE with your VPC ID
subnet_ids = [
  "subnet-00e8284becb87672b", # UPDATE with your subnet IDs
  "subnet-03f098afe6a476060",
  "subnet-0bfdaf7ba6397dd30"
]

# Security Configuration
publicly_accessible = true
allowed_cidr_blocks = [
  "49.36.25.71/32", # UPDATE with your IP address
]

# Backup Configuration
backup_retention_period      = 7 # 7-day retention recommended
preferred_backup_window      = "03:00-04:00"
preferred_maintenance_window = "sun:04:00-sun:05:00"

# CloudWatch Logs
enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

# Operational Settings
skip_final_snapshot = false
apply_immediately   = false

# Blue/Green Deployment (set to true to enable upgrade)
enable_blue_green_upgrade = false
target_engine_version     = "16.1"
target_instance_class     = null

# Tags
tags = {
  Environment = "development"
  Project     = "rds-postgres"
  ManagedBy   = "terraform"
  CostCenter  = "minimal"
}
```

### 5.6 test_rds_connection.py

**Purpose:** Simple Python script to test RDS connectivity

```python
#!/usr/bin/env python3
"""
Simple RDS PostgreSQL Connection Test
Tests basic connectivity to RDS instance
"""

import psycopg2
import sys

def test_connection():
    conn_params = {
        'host': 'postgres-rds-instance.cpmpdmefjobs.ap-south-1.rds.amazonaws.com',
        'port': 5432,
        'database': 'myappdb',
        'user': 'postgres',
        'password': 'Practice$123#Rds',
        'connect_timeout': 10,
        'sslmode': 'require'  # SSL is required by RDS
    }
    
    print("=" * 60)
    print("RDS PostgreSQL Connection Test")
    print("=" * 60)
    print(f"Host: {conn_params['host']}")
    print(f"Port: {conn_params['port']}")
    print(f"Database: {conn_params['database']}")
    print(f"User: {conn_params['user']}")
    print("-" * 60)
    
    try:
        print("\n🔄 Attempting to connect...")
        conn = psycopg2.connect(**conn_params)
        
        print("✅ Connection successful!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        print(f"\n📊 PostgreSQL Version:")
        print(version)
        
        # Get current database
        cursor.execute("SELECT current_database();")
        db = cursor.fetchone()[0]
        print(f"\n📁 Current Database: {db}")
        
        # List tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
        
        print(f"\n📋 Tables in public schema:")
        if tables:
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("  (No tables found)")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Connection failed!")
        print(f"\nError details:")
        print(str(e))
        
        if "timeout" in str(e).lower():
            print("\n💡 Possible causes:")
            print("  1. Corporate firewall blocking port 5432")
            print("  2. Network connectivity issue")
            print("  3. Security group not allowing your IP")
            print("\n🔧 Solutions:")
            print("  - Try connecting from mobile hotspot")
            print("  - Check security group allows your IP")
            print("  - Use EC2 bastion host in same VPC")
        elif "password authentication failed" in str(e).lower():
            print("\n💡 Issue: Incorrect password")
        elif "database" in str(e).lower() and "does not exist" in str(e).lower():
            print("\n💡 Issue: Database name incorrect")
            print("   Try: 'postgres' instead of 'myappdb'")
        elif "no encryption" in str(e).lower() or "no pg_hba" in str(e).lower():
            print("\n💡 Issue: SSL/TLS required")
            print("   Make sure sslmode='require' is set")
        
        print("\n" + "=" * 60)
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
```

**Usage:**
```powershell
# Update host, password in the script, then run:
python test_rds_connection.py
```

---

## 6. Step-by-Step Deployment

### Phase 1: Environment Setup

#### Step 1.1: Install Required Tools

**Windows:**
```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install Terraform
choco install terraform

# Install AWS CLI
choco install awscli

# Install Python
choco install python

# Install PostgreSQL client tools
choco install postgresql
```

#### Step 1.2: Configure AWS CLI

```powershell
# Configure AWS credentials
aws configure

# Input when prompted:
# AWS Access Key ID: <your-access-key>
# AWS Secret Access Key: <your-secret-key>
# Default region name: ap-south-1
# Default output format: json

# Verify configuration
aws sts get-caller-identity
```

#### Step 1.3: Get Network Information

```powershell
# Get your VPC ID
aws ec2 describe-vpcs --region ap-south-1 --filters Name=isDefault,Values=true --query "Vpcs[0].VpcId" --output text

# Get subnet IDs (need at least 2 in different AZs)
aws ec2 describe-subnets --region ap-south-1 --filters Name=vpc-id,Values=<your-vpc-id> --query "Subnets[*].{SubnetId:SubnetId, AZ:AvailabilityZone}" --output table

# Get your public IP
Invoke-RestMethod -Uri "https://api.ipify.org?format=text"
```

### Phase 2: Initial Deployment

#### Step 2.1: Create Project Directory

```powershell
# Create directory
New-Item -Path "C:\terraform\rds-postgres" -ItemType Directory -Force
cd C:\terraform\rds-postgres

# Create all Terraform files (copy content from Section 5)
```

#### Step 2.2: Update Configuration

Edit `terraform.tfvars` and update:

```hcl
# Update these values:
vpc_id = "vpc-xxxxxxxxxx"  # From Step 1.3
subnet_ids = [
  "subnet-xxxxxxxxxx",      # From Step 1.3
  "subnet-yyyyyyyyyy"       # From Step 1.3
]
allowed_cidr_blocks = [
  "xx.xx.xx.xx/32"         # Your IP from Step 1.3
]
master_password = "YourSecurePassword123!"  # CHANGE THIS
```

#### Step 2.3: Initialize Terraform

```powershell
# Initialize Terraform
terraform init

# Expected output:
# Terraform has been successfully initialized!
```

#### Step 2.4: Plan Deployment

```powershell
# Generate execution plan
terraform plan

# Review the plan - you should see:
# - 1 RDS instance to create
# - 1 Subnet group to create
# - 1 Security group to create
# - 1 Parameter group to create
```

#### Step 2.5: Deploy Infrastructure

```powershell
# Apply configuration
terraform apply

# Type 'yes' when prompted

# Wait for deployment (5-10 minutes)
# Monitor progress in AWS Console: RDS → Databases
```

#### Step 2.6: Verify Deployment

```powershell
# Get outputs
terraform output

# Example output:
# db_instance_endpoint = "postgres-rds-instance.xxx.ap-south-1.rds.amazonaws.com:5432"
# db_instance_address  = "postgres-rds-instance.xxx.ap-south-1.rds.amazonaws.com"
# database_name        = "myappdb"
# db_port              = 5432

# Check RDS status
aws rds describe-db-instances --db-instance-identifier postgres-rds-instance --region ap-south-1 --query "DBInstances[0].DBInstanceStatus" --output text
# Should output: available
```

### Phase 3: Test Connectivity

#### Step 3.1: Test Connection with Python Script

```powershell
# Update test_rds_connection.py with your endpoint
# Then run:
python test_rds_connection.py

# Expected output:
# ✅ Connection successful!
# PostgreSQL Version: PostgreSQL 14.17 on x86_64-pc-linux-gnu...
```

#### Step 3.2: Test with psql

```powershell
# Connect using psql
psql -h <your-endpoint> -U postgres -d myappdb -p 5432

# When prompted for password, enter your master_password

# Once connected, verify:
SELECT version();
SELECT current_database();
\l  # List databases
\q  # Quit
```

---

## 7. Blue/Green Upgrade Process

### Phase 1: Pre-Upgrade Preparation

#### Step 7.1: Create Backup

```powershell
# Create manual snapshot
aws rds create-db-snapshot `
    --db-instance-identifier postgres-rds-instance `
    --db-snapshot-identifier postgres-pre-upgrade-$(Get-Date -Format 'yyyy-MM-dd-HHmm') `
    --region ap-south-1

# Wait for snapshot to complete
aws rds describe-db-snapshots `
    --db-snapshot-identifier postgres-pre-upgrade-<timestamp> `
    --region ap-south-1 `
    --query "DBSnapshots[0].Status" `
    --output text
```

#### Step 7.2: Verify Current Version

```powershell
# Check current version
aws rds describe-db-instances `
    --db-instance-identifier postgres-rds-instance `
    --region ap-south-1 `
    --query "DBInstances[0].EngineVersion" `
    --output text

# Should output: 14.17
```

### Phase 2: Enable Blue/Green Deployment

#### Step 7.3: Update Configuration

Edit `terraform.tfvars`:

```hcl
# Enable Blue/Green deployment
enable_blue_green_upgrade = true
target_engine_version     = "16.1"  # or latest 16.x version

# Increase backup retention for safety
backup_retention_period = 7
```

#### Step 7.4: Deploy Blue/Green Environment

```powershell
# Plan changes
terraform plan

# You should see:
# + aws_db_parameter_group.postgres_pg_v16[0]
# + aws_rds_blue_green_deployment.postgres_upgrade[0]

# Apply changes
terraform apply

# Type 'yes' when prompted
# Wait 15-30 minutes for Green environment creation
```

#### Step 7.5: Monitor Deployment

```powershell
# Check deployment status
terraform output blue_green_deployment_status

# Or using AWS CLI
aws rds describe-blue-green-deployments `
    --region ap-south-1 `
    --query "BlueGreenDeployments[*].[BlueGreenDeploymentIdentifier,Status]" `
    --output table

# Wait for status: AVAILABLE
```

### Phase 3: Test Green Environment

#### Step 7.6: Get Green Endpoint

```powershell
# Get Green environment endpoint
terraform output green_environment_endpoint

# Or via AWS CLI
aws rds describe-blue-green-deployments `
    --region ap-south-1 `
    --query "BlueGreenDeployments[0].Target.Endpoint" `
    --output text
```

#### Step 7.7: Test Green Database

```powershell
# Update test script with Green endpoint
# Or use psql directly:
psql -h <green-endpoint> -U postgres -d myappdb -p 5432

# Verify version
SELECT version();
# Should show: PostgreSQL 16.x

# Run your application tests against Green environment
# Test all critical functionality
```

### Phase 4: Switchover (Production Cutover)

⚠️ **CRITICAL**: This promotes Green to production!

#### Step 7.8: Pre-Switchover Checklist

- [ ] All tests passed on Green environment
- [ ] Performance benchmarks acceptable
- [ ] Team notified
- [ ] Backup verified
- [ ] Rollback plan ready
- [ ] Maintenance window scheduled

#### Step 7.9: Perform Switchover

```powershell
# Get deployment ID
$DEPLOYMENT_ID = terraform output -raw blue_green_deployment_id

# Switchover (typically < 1 minute downtime)
aws rds switchover-blue-green-deployment `
    --blue-green-deployment-identifier $DEPLOYMENT_ID `
    --switchover-timeout 300 `
    --region ap-south-1

# Monitor switchover
aws rds describe-blue-green-deployments `
    --blue-green-deployment-identifier $DEPLOYMENT_ID `
    --region ap-south-1 `
    --query "BlueGreenDeployments[0].Status"
```

#### Step 7.10: Verify Switchover

```powershell
# Check current version (should now be 16.x)
aws rds describe-db-instances `
    --db-instance-identifier postgres-rds-instance `
    --region ap-south-1 `
    --query "DBInstances[0].EngineVersion" `
    --output text

# Test application
python test_rds_connection.py

# Verify endpoint (should be same as before)
terraform output db_instance_endpoint
```

### Phase 5: Cleanup

#### Step 7.11: Monitor Production

Wait 24-48 hours to ensure stability before cleanup.

#### Step 7.12: Delete Blue Environment

```powershell
# After confirming everything works, delete Blue/Green deployment
aws rds delete-blue-green-deployment `
    --blue-green-deployment-identifier $DEPLOYMENT_ID `
    --delete-target `
    --region ap-south-1

# Update terraform.tfvars
# Set: enable_blue_green_upgrade = false
# Set: engine_version = "16.1"

# Apply to update state
terraform apply
```

---

## 8. Testing & Validation

### 8.1 Connection Testing

**Basic Connection Test:**
```powershell
python test_rds_connection.py
```

**SQL Validation:**
```sql
-- Connect via psql and run:

-- Check version
SELECT version();

-- Check server time
SELECT NOW();

-- Test write
CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Test insert
INSERT INTO test_table (name) VALUES ('Test Entry');

-- Test read
SELECT * FROM test_table;

-- Cleanup
DROP TABLE test_table;
```

### 8.2 Performance Testing

```sql
-- Enable timing
\timing on

-- Test query performance
EXPLAIN ANALYZE SELECT * FROM pg_database;

-- Check connection count
SELECT count(*) FROM pg_stat_activity;

-- Check database size
SELECT pg_size_pretty(pg_database_size('myappdb'));
```

### 8.3 Monitoring

```powershell
# CloudWatch metrics
aws cloudwatch get-metric-statistics `
    --namespace AWS/RDS `
    --metric-name CPUUtilization `
    --dimensions Name=DBInstanceIdentifier,Value=postgres-rds-instance `
    --start-time $(Get-Date).AddHours(-1).ToString("yyyy-MM-ddTHH:mm:ss") `
    --end-time $(Get-Date).ToString("yyyy-MM-ddTHH:mm:ss") `
    --period 300 `
    --statistics Average `
    --region ap-south-1

# Database connections
aws cloudwatch get-metric-statistics `
    --namespace AWS/RDS `
    --metric-name DatabaseConnections `
    --dimensions Name=DBInstanceIdentifier,Value=postgres-rds-instance `
    --start-time $(Get-Date).AddHours(-1).ToString("yyyy-MM-ddTHH:mm:ss") `
    --end-time $(Get-Date).ToString("yyyy-MM-ddTHH:mm:ss") `
    --period 300 `
    --statistics Average `
    --region ap-south-1
```

---

## 9. Troubleshooting

### Issue 1: Connection Timeout

**Symptoms:**
```
connection to server at "..." failed: timeout
```

**Diagnosis:**
```powershell
# Check security group
aws ec2 describe-security-groups `
    --group-ids <your-sg-id> `
    --region ap-south-1 `
    --query "SecurityGroups[0].IpPermissions"

# Test network connectivity
Test-NetConnection -ComputerName <your-endpoint> -Port 5432

# Check your current IP
Invoke-RestMethod -Uri "https://api.ipify.org?format=text"
```

**Solutions:**
1. **Update security group with current IP:**
```powershell
aws ec2 authorize-security-group-ingress `
    --group-id <your-sg-id> `
    --protocol tcp `
    --port 5432 `
    --cidr <your-ip>/32 `
    --region ap-south-1
```

2. **Corporate firewall blocking port 5432:**
   - Try mobile hotspot
   - Use EC2 bastion host
   - Request firewall exception

### Issue 2: SSL/TLS Required

**Symptoms:**
```
FATAL: no pg_hba.conf entry for host "...", no encryption
```

**Solution:**
Always use `sslmode='require'` in connection parameters:
```python
conn = psycopg2.connect(
    host='...',
    sslmode='require'  # Required by RDS
)
```

### Issue 3: Blue/Green Deployment Stuck

**Symptoms:**
Status stays in "Creating" for > 45 minutes

**Diagnosis:**
```powershell
# Check deployment details
aws rds describe-blue-green-deployments `
    --region ap-south-1 `
    --query "BlueGreenDeployments[*].[Status,StatusDetails]"

# Check CloudWatch logs
aws logs tail /aws/rds/instance/postgres-rds-instance/postgresql --follow
```

**Solutions:**
1. Wait - creation can take 30-45 minutes
2. Check sufficient storage space
3. Verify parameter group compatibility
4. Review CloudWatch logs for errors

### Issue 4: Switchover Timeout

**Symptoms:**
Switchover fails or times out

**Solutions:**
1. **Increase timeout:**
```powershell
aws rds switchover-blue-green-deployment `
    --blue-green-deployment-identifier <id> `
    --switchover-timeout 600 `  # 10 minutes
    --region ap-south-1
```

2. **Reduce write traffic during switchover**
3. **Check for long-running transactions:**
```sql
SELECT * FROM pg_stat_activity WHERE state = 'active';
```

### Issue 5: Version Compatibility

**Symptoms:**
Extensions or queries fail after upgrade

**Solutions:**
```sql
-- Update extensions
ALTER EXTENSION pg_stat_statements UPDATE;
ALTER EXTENSION pgcrypto UPDATE;

-- Check extension versions
SELECT * FROM pg_available_extensions WHERE installed_version IS NOT NULL;

-- Rebuild statistics
ANALYZE;

-- Reindex if needed
REINDEX DATABASE myappdb;
```

---

## 10. Cost Optimization

### Free Tier Benefits

**AWS Free Tier (First 12 Months):**
- ✅ 750 hours/month of db.t3.micro
- ✅ 20 GB General Purpose (SSD) storage
- ✅ 20 GB backup storage
- ✅ **Total: $0/month** within limits

### Cost Breakdown

| Resource | Configuration | Monthly Cost |
|----------|--------------|--------------|
| **RDS Instance** | db.t3.micro | $13-15 (after free tier) |
| **Storage (GP3)** | 20 GB | $2.30 |
| **Backup Storage** | 20 GB | Free |
| **Data Transfer** | Varies | $0.09/GB out |
| **Total** | | **~$15-20/month** |

### Cost During Upgrade

- **Blue Environment**: Running production (~$15/month)
- **Green Environment**: During testing (~$15/month)  
- **Duration**: 1-2 days typical
- **Additional Cost**: ~$1-2 for testing period

### Cost Optimization Tips

1. **Stop instances when not in use:**
```powershell
# Stop RDS instance (storage still charged)
aws rds stop-db-instance `
    --db-instance-identifier postgres-rds-instance `
    --region ap-south-1

# Start when needed
aws rds start-db-instance `
    --db-instance-identifier postgres-rds-instance `
    --region ap-south-1
```

2. **Delete unused snapshots:**
```powershell
# List snapshots
aws rds describe-db-snapshots `
    --db-instance-identifier postgres-rds-instance `
    --region ap-south-1

# Delete old snapshots
aws rds delete-db-snapshot `
    --db-snapshot-identifier <snapshot-id> `
    --region ap-south-1
```

3. **Use GP3 instead of GP2** (better performance, same cost)
4. **Disable Multi-AZ for dev/test**
5. **Delete Blue environment after upgrade**

---

## 11. Security Best Practices

### Authentication

✅ **Use AWS Secrets Manager for credentials:**
```powershell
# Create secret
aws secretsmanager create-secret `
    --name rds/postgres/master `
    --secret-string '{"username":"postgres","password":"YourPassword"}' `
    --region ap-south-1

# Retrieve secret
aws secretsmanager get-secret-value `
    --secret-id rds/postgres/master `
    --region ap-south-1
```

### Network Security

✅ **Use VPC with private subnets (production):**
```hcl
# In terraform.tfvars
publicly_accessible = false  # Recommended for production
```

✅ **Minimum CIDR blocks:**
```hcl
allowed_cidr_blocks = [
  "10.0.1.0/24"  # Only specific subnet, not 0.0.0.0/0
]
```

### Encryption

✅ **Storage encryption** (enabled by default in our config)
✅ **SSL/TLS in transit** (always use `sslmode=require`)
✅ **Encrypted backups** (automatic with encrypted storage)

### Monitoring & Auditing

✅ **Enable CloudWatch logs:**
```hcl
enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
```

✅ **Enable deletion protection (production):**
```hcl
deletion_protection = true
```

✅ **Regular security updates:**
```hcl
auto_minor_version_upgrade = true
```

### Backup Strategy

✅ **Automated backups:**
```hcl
backup_retention_period = 7  # 7 days recommended
```

✅ **Manual snapshots before changes:**
```powershell
aws rds create-db-snapshot `
    --db-instance-identifier postgres-rds-instance `
    --db-snapshot-identifier manual-backup-$(Get-Date -Format 'yyyy-MM-dd') `
    --region ap-south-1
```

---

## Quick Reference

### Common Commands

```powershell
# Deploy initial infrastructure
terraform init
terraform plan
terraform apply

# Get outputs
terraform output
terraform output db_instance_endpoint

# Enable Blue/Green upgrade
# (Edit terraform.tfvars: enable_blue_green_upgrade = true)
terraform apply

# Check upgrade status
terraform output blue_green_deployment_status

# Test connection
python test_rds_connection.py

# Switchover to v16
aws rds switchover-blue-green-deployment `
    --blue-green-deployment-identifier <id> `
    --switchover-timeout 300 `
    --region ap-south-1

# Cleanup
terraform destroy
```

### Important Endpoints

- **AWS Console**: https://console.aws.amazon.com/rds
- **Terraform Docs**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance
- **PostgreSQL 16 Release Notes**: https://www.postgresql.org/docs/16/release-16.html
- **AWS Blue/Green Docs**: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/blue-green-deployments.html

---

## Summary

This guide provided:

✅ Complete Terraform infrastructure code  
✅ Step-by-step deployment instructions  
✅ Blue/Green upgrade process for PostgreSQL 14→16  
✅ Testing and validation procedures  
✅ Troubleshooting solutions  
✅ Cost optimization strategies  
✅ Security best practices  

**Total Time:**
- Initial deployment: ~15 minutes
- Blue/Green creation: ~30 minutes
- Testing: 2-24 hours (your choice)
- Switchover: < 1 minute
- **Total: ~1-2 hours active work**

**Total Cost:**
- First year (free tier): $0/month
- After free tier: ~$15-20/month
- Upgrade additional cost: ~$1-2

---

## Support & Resources

**Documentation:**
- This guide
- [README.md](README.md) - Quick start
- [BLUE_GREEN_UPGRADE_GUIDE.md](BLUE_GREEN_UPGRADE_GUIDE.md) - Detailed upgrade
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

**AWS Resources:**
- [RDS Documentation](https://docs.aws.amazon.com/rds/)
- [PostgreSQL on RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
- [Blue/Green Deployments](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/blue-green-deployments.html)

**Community:**
- [AWS Forums](https://forums.aws.amazon.com/)
- [PostgreSQL Community](https://www.postgresql.org/community/)
- [Terraform Community](https://discuss.hashicorp.com/)

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚

