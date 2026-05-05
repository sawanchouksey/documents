# Multi-Cloud Interview Preparation – Q&A

> **Purpose:** This file is a collection of multi-cloud scenario-based interview questions and answers for preparation and quick revision.

---

## Q0: Multi-Cloud Authentication Mechanisms – Least Privilege Approaches (Service Account, OIDC, Access Keys)

### Question

What are the authentication mechanisms for multi-cloud scenarios with least privilege? What are the pros and cons of each approach? Provide examples of all three clouds (AWS, GCP, Azure) authenticating with each other.

---

### Overview of Authentication Mechanisms

| # | Mechanism | How It Works | Credential Type |
|---|-----------|-------------|-----------------|
| 1 | **Static Access Keys** | Long-lived key pair (ID + secret) issued to a service identity | Permanent secret (must rotate manually) |
| 2 | **Service Account Key Files** | JSON/PEM key file downloaded for a service account | Permanent secret (exportable file) |
| 3 | **OIDC / Workload Identity Federation** | Workload proves its identity via a signed JWT token; the target cloud exchanges it for short-lived credentials | Temporary token (no static secret) |
| 4 | **SAML Federation** | Typically for human users via an IdP; assertion exchanged for session credentials | Session-based (time-limited) |
| 5 | **Managed Identity (Azure) / Instance Metadata (AWS/GCP)** | Cloud-native identity attached to a resource (VM, container); credentials auto-rotated | Automatic, no user management |

---

### Comparison: Pros & Cons

#### 1. Static Access Keys (AWS Access Key, Azure Client Secret)

| Pros | Cons |
|------|------|
| Simple to set up and use | **Long-lived** – if leaked, attacker has indefinite access |
| Works from anywhere (any network, any cloud) | Must be manually rotated (compliance burden) |
| No dependency on metadata services | Stored in config files/env vars – easy to accidentally commit to Git |
| Supported by all SDKs/tools out of the box | Hard to audit which system is using which key |
| | **Violates least privilege** – key grants access until explicitly revoked |

**When to use:** Legacy systems that cannot support federation; quick prototyping only. **Avoid in production.**

---

#### 2. Service Account Key Files (GCP JSON Key, Azure Service Principal Certificate)

| Pros | Cons |
|------|------|
| Stronger than basic keys (can use certificates/X.509) | **Exportable** – if the file is stolen, access is compromised |
| Can be scoped to specific roles/permissions | Must be securely stored (vault, encrypted storage) |
| Certificate-based auth avoids plaintext secrets | Key rotation requires updating all consumers |
| Familiar pattern for service-to-service auth | GCP recommends **against** exporting SA keys |
| | Creates management overhead at scale (hundreds of keys) |

**When to use:** On-premises workloads accessing cloud that **cannot** use identity federation. Use certificates over secrets when possible.

---

#### 3. OIDC / Workload Identity Federation (Recommended – Least Privilege)

| Pros | Cons |
|------|------|
| **No static credentials** – uses short-lived tokens (minutes/hours) | Requires initial trust setup (one-time, but complex) |
| **Auto-rotating** – no manual key rotation needed | Requires the source workload to have an identity provider (OIDC issuer) |
| Scoped to specific workload identity (pod, task, VM) | Slight latency for token exchange (~100ms) |
| **Auditable** – every token exchange is logged | Not all legacy systems/tools support it |
| Follows Zero Trust principles | Debugging token issues can be harder than static keys |
| No secrets to leak, commit, or manage | Requires network access to token endpoints |
| **Industry standard** (OIDC/OAuth2) | |

**When to use:** **Always prefer this for production cross-cloud authentication.** This is the gold standard for least privilege.

---

### Mechanism Comparison Matrix

| Criteria | Access Keys | SA Key Files | OIDC Federation |
|----------|------------|-------------|-----------------|
| **Security** | ⚠️ Low | ⚠️ Medium | ✅ High |
| **Least Privilege** | ❌ Broad, persistent | ⚠️ Scoped but persistent | ✅ Scoped + temporary |
| **Key Rotation** | Manual | Manual | Automatic (tokens expire) |
| **Blast Radius if Leaked** | 🔴 High (indefinite access) | 🔴 High (until revoked) | 🟢 Low (token expires in minutes) |
| **Audit Trail** | Basic (who has key?) | Basic | ✅ Full (every exchange logged) |
| **Setup Complexity** | Low | Low-Medium | Medium-High (one-time) |
| **Operational Overhead** | High (rotation, storage) | High | Low (after setup) |
| **Best For** | Dev/test, legacy | On-prem → Cloud | **Production cross-cloud** |

---

### Cross-Cloud Authentication Examples (All Combinations)

---

#### Example 1: AWS → GCP (AWS workload accessing GCP resources)

**Method: GCP Workload Identity Federation with AWS as IdP**

```bash
# GCP Side: Create Workload Identity Pool for AWS
gcloud iam workload-identity-pools create aws-pool \
  --location=global \
  --display-name="AWS Workloads"

gcloud iam workload-identity-pools providers create-aws aws-provider \
  --workload-identity-pool=aws-pool \
  --location=global \
  --account-id=123456789012  # AWS Account ID

# Grant GCP SA impersonation to a specific AWS Role
gcloud iam service-accounts add-iam-policy-binding \
  my-gcp-sa@PROJECT.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_NUM/locations/global/workloadIdentityPools/aws-pool/attribute.aws_role/arn:aws:sts::123456789012:assumed-role/MyECSTaskRole"
```

**How it works:** AWS workload (ECS/EKS/Lambda) uses its IAM role credentials → exchanges them with GCP STS → receives short-lived GCP access token → calls GCP APIs. **No static keys anywhere.**

---

#### Example 2: GCP → AWS (GCP workload accessing AWS resources)

**Method: AWS IAM Role with Web Identity Federation (GCP as OIDC IdP)**

```bash
# AWS Side: Create IAM Role trusting GCP's OIDC token
aws iam create-role --role-name GCPWorkloadRole --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Federated": "accounts.google.com"},
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "accounts.google.com:sub": "GCP_SA_UNIQUE_ID"
      }
    }
  }]
}'

# Attach least-privilege policy
aws iam attach-role-policy --role-name GCPWorkloadRole \
  --policy-arn arn:aws:iam::123456789012:policy/S3ReadOnlySpecificBucket
```

**GCP Side (application code):**

```python
from google.auth import credentials
from google.auth.transport.requests import Request
import boto3

# GCP workload gets its identity token automatically (via metadata server)
# Then exchanges it with AWS STS for temporary AWS credentials
sts_client = boto3.client('sts')
response = sts_client.assume_role_with_web_identity(
    RoleArn='arn:aws:iam::123456789012:role/GCPWorkloadRole',
    RoleSessionName='gcp-to-aws-session',
    WebIdentityToken=gcp_identity_token,  # From GCP metadata server
    DurationSeconds=3600  # 1-hour session
)
# Use response['Credentials'] to access AWS – short-lived, auto-expires
```

---

#### Example 3: Azure → GCP (Azure workload accessing GCP resources)

**Method: GCP Workload Identity Federation with Azure AD as OIDC IdP**

```bash
# GCP Side: Create pool with Azure AD as OIDC provider
gcloud iam workload-identity-pools create azure-pool \
  --location=global

gcloud iam workload-identity-pools providers create-oidc azure-provider \
  --workload-identity-pool=azure-pool \
  --location=global \
  --issuer-uri="https://login.microsoftonline.com/TENANT_ID/v2.0" \
  --allowed-audiences="api://GCP_APP_ID" \
  --attribute-mapping="google.subject=assertion.sub"

# Grant access to specific Azure Managed Identity
gcloud iam service-accounts add-iam-policy-binding \
  my-gcp-sa@PROJECT.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principal://iam.googleapis.com/projects/PROJECT_NUM/locations/global/workloadIdentityPools/azure-pool/subject/AZURE_MI_OBJECT_ID"
```

**Azure Side (app running on Azure VM/AKS with Managed Identity):**

```python
from azure.identity import ManagedIdentityCredential
from google.auth import identity_pool

# Azure workload gets token from its Managed Identity (automatic, no secrets)
azure_cred = ManagedIdentityCredential()
token = azure_cred.get_token("api://GCP_APP_ID")

# Exchange Azure token for GCP credentials via Workload Identity Federation
# (handled automatically by google-auth library with credential config file)
```

---

#### Example 4: GCP → Azure (GCP workload accessing Azure resources)

**Method: Azure Federated Identity Credential (trusts GCP's OIDC token)**

```bash
# Azure Side: Create App Registration + Federated Credential
az ad app create --display-name "GCP-Workload-Access"

az ad app federated-credential create --id APP_OBJECT_ID --parameters '{
  "name": "gcp-federation",
  "issuer": "https://accounts.google.com",
  "subject": "GCP_SA_UNIQUE_ID",
  "audiences": ["api://AzureADTokenExchange"],
  "description": "Trust GCP service account"
}'

# Assign Azure RBAC role to the App
az role assignment create \
  --assignee APP_CLIENT_ID \
  --role "Storage Blob Data Reader" \
  --scope /subscriptions/SUB_ID/resourceGroups/RG/providers/Microsoft.Storage/storageAccounts/ACCOUNT
```

**GCP Side (application code):**

```python
from azure.identity import ClientAssertionCredential

# GCP workload gets its ID token from metadata server
gcp_token = get_gcp_identity_token(audience="api://AzureADTokenExchange")

# Use GCP token as client assertion to authenticate to Azure
azure_cred = ClientAssertionCredential(
    tenant_id="AZURE_TENANT_ID",
    client_id="APP_CLIENT_ID",
    func=lambda: gcp_token  # GCP identity token as assertion
)

# Now access Azure resources – no static secrets!
from azure.storage.blob import BlobServiceClient
blob_client = BlobServiceClient(account_url="https://ACCOUNT.blob.core.windows.net", credential=azure_cred)
```

---

#### Example 5: AWS → Azure (AWS workload accessing Azure resources)

**Method: Azure Federated Identity Credential (trusts AWS STS token)**

```bash
# Azure Side: Federated credential trusting AWS
az ad app federated-credential create --id APP_OBJECT_ID --parameters '{
  "name": "aws-federation",
  "issuer": "https://cognito-identity.amazonaws.com",
  "subject": "arn:aws:sts::123456789012:assumed-role/MyECSTaskRole",
  "audiences": ["api://AzureADTokenExchange"],
  "description": "Trust AWS ECS task role"
}'
```

**AWS Side (ECS/EKS/Lambda):**

```python
import boto3
from azure.identity import ClientAssertionCredential

# Get AWS identity token (via EKS OIDC or custom setup)
# For EKS: token is available at the projected service account token path
with open('/var/run/secrets/eks.amazonaws.com/serviceaccount/token') as f:
    aws_token = f.read()

# Exchange AWS token for Azure access
azure_cred = ClientAssertionCredential(
    tenant_id="AZURE_TENANT_ID",
    client_id="APP_CLIENT_ID",
    func=lambda: aws_token
)
# Access Azure resources with short-lived credentials
```

---

#### Example 6: Azure → AWS (Azure workload accessing AWS resources)

**Method: AWS IAM Role with OIDC Federation (Azure AD as IdP)**

```bash
# AWS Side: Create OIDC Provider for Azure AD
aws iam create-open-id-connect-provider \
  --url "https://login.microsoftonline.com/TENANT_ID/v2.0" \
  --client-id-list "APP_CLIENT_ID" \
  --thumbprint-list "AZURE_AD_THUMBPRINT"

# Create IAM Role trusting Azure AD tokens
aws iam create-role --role-name AzureWorkloadRole --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::123456789012:oidc-provider/login.microsoftonline.com/TENANT_ID/v2.0"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "login.microsoftonline.com/TENANT_ID/v2.0:sub": "AZURE_MI_OBJECT_ID"
      }
    }
  }]
}'

aws iam attach-role-policy --role-name AzureWorkloadRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

**Azure Side (app with Managed Identity):**

```python
from azure.identity import ManagedIdentityCredential
import boto3

# Get Azure AD token for the AWS audience
azure_cred = ManagedIdentityCredential()
token = azure_cred.get_token("api://aws-federation-app")

# Exchange for AWS credentials
sts = boto3.client('sts')
response = sts.assume_role_with_web_identity(
    RoleArn='arn:aws:iam::123456789012:role/AzureWorkloadRole',
    RoleSessionName='azure-to-aws',
    WebIdentityToken=token.token,
    DurationSeconds=3600
)
# Use response['Credentials'] – temporary, auto-expires
```

---

### Quick Reference: Cloud-Native Identity Names

| Cloud | Workload Identity | Human Identity (SSO) | Keyless Federation |
|-------|------------------|---------------------|-------------------|
| **AWS** | IAM Role (for EC2/ECS/EKS/Lambda) | IAM Identity Center (SSO) | `sts:AssumeRoleWithWebIdentity` |
| **GCP** | Service Account + Workload Identity | Workforce Identity Federation | Workload Identity Federation |
| **Azure** | Managed Identity (System/User-assigned) | Entra ID (Azure AD) | Federated Identity Credentials |

---

### Decision Flowchart

```
Is the workload running IN a cloud environment?
    │
    ├── YES → Does the TARGET cloud support federation from the SOURCE?
    │           │
    │           ├── YES → ✅ Use OIDC / Workload Identity Federation
    │           │
    │           └── NO → Use Service Account key (store in vault, rotate every 90 days)
    │
    └── NO (on-premises / third-party) → Can you set up an OIDC IdP (e.g., Vault, SPIFFE)?
                │
                ├── YES → ✅ Use OIDC federation with your IdP
                │
                └── NO → Use Service Account key or Access Key (last resort)
                          ⚠️ Store in HashiCorp Vault / cloud secret manager
                          ⚠️ Rotate every 90 days minimum
                          ⚠️ Scope to absolute minimum permissions
```

---

### Key Takeaways (Interview Talking Points)

- **Always prefer OIDC/Workload Identity Federation** – no static credentials, short-lived tokens, auto-rotating.
- All three clouds now support **keyless cross-cloud auth**: AWS (Web Identity Federation), GCP (Workload Identity Federation), Azure (Federated Identity Credentials).
- **Static keys are a liability** – they don't expire, are easy to leak, and violate Zero Trust.
- **Service Account keys** are acceptable ONLY for on-premises/legacy systems that cannot support OIDC.
- The pattern is always: **Source workload proves identity → Target cloud exchanges it for short-lived credentials**.
- **Audit everything** – every token exchange is logged (CloudTrail, Cloud Audit Logs, Azure Monitor).
- **Conditional trust** – restrict federation to specific subjects/audiences/claims (never allow all tokens from an issuer).

---

## Q1: Replicate files from AWS S3 to GCP Cloud Storage with least privilege (no direct GCP access)

### Scenario

An application writes files to an AWS S3 bucket. You need to replicate (sync) those same files into a GCP Cloud Storage bucket, following the principle of least privilege. You do **not** have direct access to the GCP console or GCP credentials.

### Approach: AWS IAM Role with Identity Federation (Most Secure – No Static Keys)

Since you do not have direct access to the GCP environment, the migration requires a **"handshake"** between you (AWS side) and the GCP administrator. Using an **AWS IAM Role for Identity Federation** is the most secure method as it allows GCP's Storage Transfer Service (STS) to assume a role in your account **without ever needing static access keys**. [1]

---

### Step 1: Your Action (AWS Side) – Prepare the Access Policy

Create a custom IAM policy that grants the **absolute minimum** permissions needed to read your bucket. [2, 3]

1. **Create Policy:** In the [AWS IAM Console](https://console.aws.amazon.com/iam/), create a new policy with the following JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::YOUR_S3_BUCKET_NAME"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::YOUR_S3_BUCKET_NAME/*"
    }
  ]
}
```

> **Note:** If you want GCP to **delete** files from S3 after moving them, add `s3:DeleteObject` to the actions. [3, 4, 5]

---

### Step 2: Coordination Step – Get the GCP Subject ID

You **cannot** finish your AWS role setup without a unique identifier from the GCP Admin.

- Ask the GCP Admin to provide the **Subject ID** (a long numerical string) for their project's Storage Transfer Service account.
- They can find this by running:

```bash
gcloud transfer authorize --project=PROJECT_ID
```

or via the [Google Service Accounts API](https://docs.cloud.google.com/storage-transfer/docs/source-amazon-s3). [1, 2, 6]

---

### Step 3: Your Action (AWS Side) – Create the Federated Role

Once you have the Subject ID, create the IAM role that the GCP service will assume.

1. **Create Role:** Choose **Custom Trust Policy** as the trusted entity type.
2. **Paste Trust Policy:** Use the following JSON, replacing `SUBJECT_ID` with the ID provided by the GCP Admin:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "accounts.google.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "accounts.google.com:sub": "SUBJECT_ID"
        }
      }
    }
  ]
}
```

3. **Attach Policy:** Attach the restricted S3 policy you created in Step 1.
4. **Send Role ARN:** Copy the Role ARN (e.g., `arn:aws:iam::123456789:role/GCP-Migration-Role`) and send it to the GCP Admin. [2, 5, 7]

---

### Step 4: GCP Admin Action – Start the Transfer

The GCP Admin will now use your Role ARN to pull the files.

| # | Action |
|---|--------|
| 1 | Navigate to **Data Transfer → Transfer Service** in the [GCP Console](https://console.cloud.google.com/). |
| 2 | **Source:** Amazon S3 (using your bucket name). |
| 3 | **Authentication:** Select **IAM Role ARN** and paste the ARN you provided. |
| 4 | **Destination:** Their Google Cloud Storage bucket. |
| 5 | **Schedule:** Run once or set a recurring schedule for ongoing replication. [7, 8, 9, 10, 11] |

---

### Why This Approach Is Best (Interview Talking Points)

| Aspect | IAM Role + Federation | Static Access Keys |
|--------|----------------------|-------------------|
| **Key rotation** | No keys to rotate — uses temporary STS tokens | Must rotate keys manually |
| **Blast radius** | Role is scoped to one GCP Subject ID | Keys can be leaked / reused anywhere |
| **Audit** | CloudTrail logs `AssumeRoleWithWebIdentity` events | Harder to trace key usage to a specific consumer |
| **Least privilege** | ✅ Read-only S3 + federated trust limited to one identity | ⚠️ Keys grant access to anyone who holds them |

### Key Takeaways

- **No static credentials** are exchanged — the GCP STS assumes an AWS role via Web Identity Federation.
- You only configure the **AWS side** (policy + role); the GCP Admin handles the transfer job.
- Least privilege = read-only S3 permissions + trust policy scoped to a single GCP Subject ID.
- **CloudTrail** captures every `AssumeRoleWithWebIdentity` call for full auditability.

---

### References & Video Walkthroughs

| # | Source |
|---|--------|
| [1] | [Searce Blog – GCP STS Job using AWS ARN](https://blog.searce.com/gcp-storage-transfer-service-job-using-aws-arn-81d6d9082299) |
| [2] | [Google Docs – Source Amazon S3](https://docs.cloud.google.com/storage-transfer/docs/source-amazon-s3) |
| [3] | [Google Docs – Source Amazon S3 (permissions)](https://docs.cloud.google.com/storage-transfer/docs/source-amazon-s3) |
| [4] | [Searce Blog – Delete after transfer](https://blog.searce.com/gcp-storage-transfer-service-job-using-aws-arn-81d6d9082299) |
| [5] | [Google Docs – Source Amazon S3 (role setup)](https://docs.cloud.google.com/storage-transfer/docs/source-amazon-s3) |
| [6] | [Google Cloud Blog – Transfer data AWS to GCP](https://cloud.google.com/blog/topics/developers-practitioners/transfer-data-aws-gcp-using-storage-transfer-service/) |
| [7] | [Searce Blog – Full walkthrough](https://blog.searce.com/gcp-storage-transfer-service-job-using-aws-arn-81d6d9082299) |
| [8] | [Google Cloud Blog – Practitioners guide](https://cloud.google.com/blog/topics/developers-practitioners/transfer-data-aws-gcp-using-storage-transfer-service/) |
| [9] | [CloudThat – S3 to GCS migration](https://www.cloudthat.com/resources/blog/seamless-object-storage-migration-from-amazon-s3-to-google-cloud-storage) |
| [10] | [CloudThat – Detailed steps](https://www.cloudthat.com/resources/blog/seamless-object-storage-migration-from-amazon-s3-to-google-cloud-storage) |
| [11] | [YouTube – Visual walkthrough](https://www.youtube.com/watch?v=W-AkG71n0VQ) |

**Video Guides:**

- [Data Migration using Google Storage Transfer Service | Multi-Cloud](https://www.youtube.com/watch?v=tslQCs4WjTo) – Azim Shaik
- [Migrating AWS S3 Bucket to Google Cloud Storage](https://www.youtube.com/watch?v=1rquEV84rlc) – cloudroot7
- [Transfer files from AWS S3 to GCP](https://www.youtube.com/watch?v=u_KXroDVyD0) – Latest Technologies

---

## Q2: CI/CD Pipeline for GKE Deployment (from AWS ECS background) – DevOps/Infrastructure Perspective

### Scenario

You currently run containerized workloads on **AWS ECS**. You now need to build a CI/CD pipeline to deploy containers to **GCP GKE (Google Kubernetes Engine)**. Requirements:

- Deploy **specific containers from a specific registry** (Artifact Registry).
- Include **vulnerability assessment** in the pipeline.
- Follow **production-grade best practices** from a DevOps engineer / infrastructure perspective.

---

### Architecture Overview

```
Source Code (Git)
    │
    ▼
Cloud Build / GitHub Actions (CI)
    ├── Build container image
    ├── Push to Artifact Registry
    ├── Vulnerability scan (Artifact Analysis)
    └── Gate: Block if CRITICAL/HIGH CVEs found
            │
            ▼
Cloud Deploy (CD)
    ├── Deploy to DEV (GKE cluster)
    ├── Approval gate
    ├── Deploy to STAGING (GKE cluster)
    ├── Approval gate
    └── Deploy to PROD (GKE cluster)
```

---

### Step 1: Infrastructure Setup – GKE Cluster (Terraform/IaC)

As a DevOps engineer, provision GKE using IaC (Terraform recommended).

```hcl
# Key secure GKE settings
resource "google_container_cluster" "primary" {
  name     = "prod-gke-cluster"
  location = "europe-west1"

  # Use private cluster – nodes have no public IPs
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false  # set true for full lockdown
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  # Enable Workload Identity (replaces node SA key files)
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Enable Binary Authorization
  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  # Enable Shielded GKE Nodes
  node_config {
    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }
    # Use least-privilege service account (NOT default compute SA)
    service_account = google_service_account.gke_nodes.email
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]
  }
}
```

**Key Decisions (ECS → GKE mapping for interview):**

| AWS ECS Concept | GKE Equivalent |
|----------------|----------------|
| ECS Cluster | GKE Cluster |
| Task Definition | Kubernetes Deployment / Pod Spec |
| Service | Kubernetes Service + Deployment |
| ECR (Registry) | Artifact Registry |
| Fargate (serverless) | GKE Autopilot |
| ALB / Target Groups | Ingress / GKE Gateway API |
| IAM Task Role | Workload Identity (K8s SA → GCP SA) |

---

### Step 2: Container Registry – Artifact Registry Setup

Set up a **private Artifact Registry** repository (replaces Docker Hub / ECR).

```bash
# Create Docker repository in Artifact Registry
gcloud artifacts repositories create app-images \
  --repository-format=docker \
  --location=europe-west1 \
  --description="Production container images"

# Enable vulnerability scanning (automatic)
gcloud services enable containerscanning.googleapis.com
```

**Least Privilege – Registry Access:**

| Role | Granted To | Purpose |
|------|-----------|---------|
| `roles/artifactregistry.writer` | CI/CD service account | Push images |
| `roles/artifactregistry.reader` | GKE node service account | Pull images only |
| `roles/containeranalysis.occurrences.viewer` | CI/CD service account | Read scan results |

**Restrict GKE to pull only from your registry (Binary Authorization):**

```yaml
# Binary Authorization policy – allow only images from your repo
defaultAdmissionRule:
  evaluationMode: ALWAYS_DENY
  enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
clusterAdmissionRules:
  "europe-west1.prod-gke-cluster":
    evaluationMode: REQUIRE_ATTESTATION
    enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
    requireAttestationsBy:
      - projects/YOUR_PROJECT/attestors/vulnerability-scan-passed
```

This ensures **only images from your specific registry that pass vulnerability scans** can be deployed.

---

### Step 3: CI Pipeline – Build, Scan, Push (Cloud Build)

Create `cloudbuild.yaml` for the CI pipeline:

```yaml
steps:
  # Step 1: Build the container image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'europe-west1-docker.pkg.dev/$PROJECT_ID/app-images/myapp:$SHORT_SHA'
      - '.'

  # Step 2: Push to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'europe-west1-docker.pkg.dev/$PROJECT_ID/app-images/myapp:$SHORT_SHA'

  # Step 3: Wait for vulnerability scan to complete
  - name: 'gcr.io/cloud-builders/gcloud'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        echo "Waiting for vulnerability scan..."
        gcloud artifacts docker images scan \
          europe-west1-docker.pkg.dev/$PROJECT_ID/app-images/myapp:$SHORT_SHA \
          --format='value(response.scan)' > /workspace/scan_id.txt

  # Step 4: Check scan results – FAIL build if CRITICAL or HIGH CVEs found
  - name: 'gcr.io/cloud-builders/gcloud'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        SCAN_ID=$(cat /workspace/scan_id.txt)
        CRITICAL=$(gcloud artifacts docker images list-vulnerabilities $SCAN_ID \
          --format='value(vulnerability.effectiveSeverity)' | grep -c 'CRITICAL' || true)
        HIGH=$(gcloud artifacts docker images list-vulnerabilities $SCAN_ID \
          --format='value(vulnerability.effectiveSeverity)' | grep -c 'HIGH' || true)
        echo "CRITICAL: $CRITICAL, HIGH: $HIGH"
        if [ "$CRITICAL" -gt 0 ]; then
          echo "❌ CRITICAL vulnerabilities found – blocking deployment"
          exit 1
        fi

  # Step 5: Create attestation (for Binary Authorization)
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'container'
      - 'binauthz'
      - 'attestations'
      - 'sign-and-create'
      - '--artifact-url=europe-west1-docker.pkg.dev/$PROJECT_ID/app-images/myapp:$SHORT_SHA'
      - '--attestor=vulnerability-scan-passed'
      - '--attestor-project=$PROJECT_ID'
      - '--keyversion=projects/$PROJECT_ID/locations/global/keyRings/binauthz/cryptoKeys/attestor-key/cryptoKeyVersions/1'

options:
  logging: CLOUD_LOGGING_ONLY

images:
  - 'europe-west1-docker.pkg.dev/$PROJECT_ID/app-images/myapp:$SHORT_SHA'
```

---

### Step 4: CD Pipeline – Progressive Delivery to GKE (Cloud Deploy)

Use **Google Cloud Deploy** for managed, auditable rollouts.

```bash
# Create delivery pipeline
gcloud deploy apply --file=clouddeploy.yaml --region=europe-west1
```

**clouddeploy.yaml:**

```yaml
apiVersion: deploy.cloud.google.com/v1
kind: DeliveryPipeline
metadata:
  name: myapp-pipeline
serialPipeline:
  stages:
    - targetId: dev
      profiles: [dev]
    - targetId: staging
      profiles: [staging]
      strategy:
        canary:
          runtimeConfig:
            kubernetes:
              serviceNetworking:
                service: myapp-service
          canaryDeployment:
            percentages: [25, 50, 75]
    - targetId: prod
      profiles: [prod]
      strategy:
        canary:
          runtimeConfig:
            kubernetes:
              serviceNetworking:
                service: myapp-service
          canaryDeployment:
            percentages: [10, 25, 50, 75]
---
apiVersion: deploy.cloud.google.com/v1
kind: Target
metadata:
  name: dev
gke:
  cluster: projects/PROJECT_ID/locations/europe-west1/clusters/dev-gke-cluster
---
apiVersion: deploy.cloud.google.com/v1
kind: Target
metadata:
  name: staging
gke:
  cluster: projects/PROJECT_ID/locations/europe-west1/clusters/staging-gke-cluster
requireApproval: true
---
apiVersion: deploy.cloud.google.com/v1
kind: Target
metadata:
  name: prod
gke:
  cluster: projects/PROJECT_ID/locations/europe-west1/clusters/prod-gke-cluster
requireApproval: true
```

---

### Step 5: Kubernetes Manifests – Secure Deployment Spec

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      serviceAccountName: myapp-ksa  # Workload Identity bound SA
      containers:
        - name: myapp
          # Pin to digest, not just tag – prevents tag mutation attacks
          image: europe-west1-docker.pkg.dev/PROJECT_ID/app-images/myapp@sha256:DIGEST
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          securityContext:
            runAsNonRoot: true
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
            capabilities:
              drop: ["ALL"]
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-credentials  # Use External Secrets Operator + Secret Manager
                  key: password
```

---

### Step 6: IAM & Service Accounts – Least Privilege

```bash
# 1. CI/CD Service Account (Cloud Build)
gcloud iam service-accounts create cicd-builder --display-name="CI/CD Builder"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:cicd-builder@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:cicd-builder@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/clouddeploy.releaser"

# 2. GKE Node Service Account (only pull images)
gcloud iam service-accounts create gke-nodes --display-name="GKE Node SA"

gcloud artifacts repositories add-iam-policy-binding app-images \
  --location=europe-west1 \
  --member="serviceAccount:gke-nodes@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"

# 3. Workload Identity – bind K8s SA to GCP SA (no key files on pods)
gcloud iam service-accounts create myapp-gsa --display-name="MyApp GCP SA"

gcloud iam service-accounts add-iam-policy-binding myapp-gsa@${PROJECT_ID}.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="serviceAccount:${PROJECT_ID}.svc.id.goog[production/myapp-ksa]"

kubectl annotate serviceaccount myapp-ksa \
  --namespace production \
  iam.gke.io/gcp-service-account=myapp-gsa@${PROJECT_ID}.iam.gserviceaccount.com
```

---

### Step 7: Vulnerability & Security Guardrails (Ongoing)

| Layer | Tool / Service | Purpose |
|-------|---------------|---------|
| **Image Build** | Artifact Analysis (Container Scanning) | Auto-scan on push to Artifact Registry |
| **Deployment Gate** | Binary Authorization | Block unsigned / unscanned images from GKE |
| **Runtime** | GKE Security Posture Dashboard | Detect misconfigurations in running workloads |
| **Network** | GKE Network Policies + VPC-SC | Restrict pod-to-pod & external traffic |
| **Secrets** | Secret Manager + External Secrets Operator | No hardcoded secrets in manifests |
| **Compliance** | Organization Policies | Enforce constraints (e.g., no public IPs, approved registries only) |
| **Audit** | Cloud Audit Logs + SIEM | Track who deployed what, when |

---

### Step 8: Complete Pipeline Flow Summary

```
1. Developer pushes code to Git (main/release branch)
                    │
2. Cloud Build trigger fires
                    │
3. Build → Docker image created
                    │
4. Push → Image pushed to Artifact Registry
                    │
5. Scan → Artifact Analysis runs vulnerability assessment
                    │
6. Gate → CRITICAL CVEs? ──YES──→ ❌ Build FAILS (notify team)
                    │ NO
7. Attest → Binary Authorization attestation created
                    │
8. Cloud Deploy → Create release → Deploy to DEV
                    │
9. Automated tests pass → Promote to STAGING (canary 25%→50%→75%→100%)
                    │
10. Manual approval → Promote to PROD (canary 10%→25%→50%→75%→100%)
                    │
11. Monitor → Cloud Monitoring / Error Reporting dashboards
```

---

### DevOps Best Practices Checklist

- [x] **IaC everything** – Terraform for GKE, Helm/Kustomize for K8s resources
- [x] **Private clusters** – No public IPs on GKE nodes
- [x] **Workload Identity** – No exported service account keys
- [x] **Binary Authorization** – Only attested images run on GKE
- [x] **Image digest pinning** – Use `@sha256:` not `:latest`
- [x] **Vulnerability scanning** – Block CRITICAL CVEs before deploy
- [x] **Progressive delivery** – Canary deployments, not big-bang
- [x] **Namespace isolation** – Separate namespaces per environment/team
- [x] **Network Policies** – Default deny, explicit allow
- [x] **Secret Manager** – No secrets in Git, env vars, or ConfigMaps
- [x] **RBAC** – Least-privilege K8s roles for CI/CD and operators
- [x] **Audit logging** – Every deploy action tracked in Cloud Audit Logs

---

### Binary Authorization – Deep Dive

#### What Is Binary Authorization?

Binary Authorization is a **deploy-time security control** in GCP that ensures **only trusted container images** are deployed to GKE, Cloud Run, or Anthos. It acts as an admission controller — if an image doesn't meet the policy, Kubernetes **rejects the pod creation**.

> **Analogy:** Think of it like a bouncer at a club. Every container image needs a "stamp" (attestation) from a trusted authority before it's allowed in.

---

#### Core Concepts

| Concept | Description |
|---------|-------------|
| **Policy** | A set of rules defining which images are allowed to run. Applied at project or cluster level. |
| **Attestor** | A trusted authority that vouches for an image (e.g., "this image passed vulnerability scan"). |
| **Attestation** | A signed statement by an attestor that a specific image (by digest) is approved. |
| **KMS Key** | A Cloud KMS asymmetric key used to cryptographically sign and verify attestations. |
| **Admission Rule** | The enforcement action: `ALLOW_ALL`, `DENY_ALL`, or `REQUIRE_ATTESTATION`. |

---

#### How It Works – End-to-End Flow

```
┌──────────────────────────────────────────────────────────────┐
│                        CI PIPELINE                           │
│                                                              │
│  1. Build image                                              │
│  2. Push to Artifact Registry                                │
│  3. Vulnerability scan (Artifact Analysis)                   │
│  4. If scan passes → Create ATTESTATION (signed with KMS)    │
│  5. If scan fails → NO attestation → image is blocked        │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    GKE CLUSTER                               │
│                                                              │
│  Binary Authorization Admission Controller                   │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ kubectl apply -f deployment.yaml                     │     │
│  │                                                      │     │
│  │ Check: Does image have valid attestation?            │     │
│  │   YES → ✅ Pod created                               │     │
│  │   NO  → ❌ Pod REJECTED + audit log entry            │     │
│  └─────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

---

#### Binary Authorization – Step-by-Step Setup

**Step A: Enable Required APIs**

```bash
gcloud services enable \
  binaryauthorization.googleapis.com \
  containeranalysis.googleapis.com \
  cloudkms.googleapis.com \
  artifactregistry.googleapis.com
```

**Step B: Create a KMS Key for Signing Attestations**

```bash
# Create a key ring
gcloud kms keyrings create binauthz-keyring \
  --location=global

# Create an asymmetric signing key
gcloud kms keys create attestor-key \
  --keyring=binauthz-keyring \
  --location=global \
  --purpose=asymmetric-signing \
  --default-algorithm=ec-sign-p256-sha256
```

**Step C: Create an Attestor**

```bash
# Create a Container Analysis note (attestor's identity)
cat > note.json << EOF
{
  "attestation": {
    "hint": {
      "human_readable_name": "Vulnerability scan passed"
    }
  }
}
EOF

curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://containeranalysis.googleapis.com/v1/projects/${PROJECT_ID}/notes/?noteId=vuln-scan-note" \
  -d @note.json

# Create the attestor linked to the note and KMS key
gcloud container binauthz attestors create vuln-scan-attestor \
  --attestation-authority-note=vuln-scan-note \
  --attestation-authority-note-project=${PROJECT_ID}

# Add the KMS key to the attestor
gcloud container binauthz attestors public-keys add \
  --attestor=vuln-scan-attestor \
  --keyversion=projects/${PROJECT_ID}/locations/global/keyRings/binauthz-keyring/cryptoKeys/attestor-key/cryptoKeyVersions/1
```

**Step D: Configure the Binary Authorization Policy**

```bash
# Export current policy
gcloud container binauthz policy export > policy.yaml
```

Edit `policy.yaml`:

```yaml
admissionWhitelistPatterns:
  # Allow GKE system images (required for cluster operation)
  - namePattern: "gcr.io/google_containers/*"
  - namePattern: "gcr.io/google-containers/*"
  - namePattern: "k8s.gcr.io/**"
  - namePattern: "gke.gcr.io/**"
  - namePattern: "gcr.io/gke-release/*"

defaultAdmissionRule:
  evaluationMode: ALWAYS_DENY          # Default: block everything
  enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG

clusterAdmissionRules:
  # DEV cluster – require attestation
  "europe-west1.dev-gke-cluster":
    evaluationMode: REQUIRE_ATTESTATION
    enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
    requireAttestationsBy:
      - projects/${PROJECT_ID}/attestors/vuln-scan-attestor

  # PROD cluster – require attestation (strictest)
  "europe-west1.prod-gke-cluster":
    evaluationMode: REQUIRE_ATTESTATION
    enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
    requireAttestationsBy:
      - projects/${PROJECT_ID}/attestors/vuln-scan-attestor

globalPolicyEvaluationMode: ENABLE
```

```bash
# Apply the policy
gcloud container binauthz policy import policy.yaml
```

**Step E: Create Attestations in CI Pipeline**

After a successful vulnerability scan in Cloud Build:

```bash
# Create attestation for a specific image digest
gcloud container binauthz attestations sign-and-create \
  --artifact-url="europe-west1-docker.pkg.dev/${PROJECT_ID}/app-images/myapp@sha256:${IMAGE_DIGEST}" \
  --attestor="vuln-scan-attestor" \
  --attestor-project="${PROJECT_ID}" \
  --keyversion="projects/${PROJECT_ID}/locations/global/keyRings/binauthz-keyring/cryptoKeys/attestor-key/cryptoKeyVersions/1"
```

> **Important:** Attestations are tied to the image **digest** (`sha256:...`), not the tag. This prevents tag-mutation attacks (e.g., someone overwriting `:latest`).

**Step F: Verify It Works**

```bash
# Try deploying an un-attested image → should be REJECTED
kubectl run test --image=docker.io/nginx:latest
# Error: admission webhook "imagepolicywebhook.image-policy.k8s.io" denied the request:
# Image docker.io/nginx:latest denied by Binary Authorization default admission rule

# Deploy an attested image → should SUCCEED
kubectl apply -f deployment.yaml  # with attested image digest
# deployment.apps/myapp created
```

---

#### Multiple Attestors (Multi-Gate Pattern)

For production-grade pipelines, use **multiple attestors** to create a chain of trust:

```
┌─────────────┐    ┌─────────────────┐    ┌──────────────────┐
│ build-check │───→│ vuln-scan-check │───→│ qa-approval-check│
│  attestor   │    │    attestor     │    │    attestor      │
└─────────────┘    └─────────────────┘    └──────────────────┘
     CI Build          Vuln Scan OK         QA Team Approved
```

Policy requiring **all three** attestations:

```yaml
clusterAdmissionRules:
  "europe-west1.prod-gke-cluster":
    evaluationMode: REQUIRE_ATTESTATION
    enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
    requireAttestationsBy:
      - projects/${PROJECT_ID}/attestors/build-attestor
      - projects/${PROJECT_ID}/attestors/vuln-scan-attestor
      - projects/${PROJECT_ID}/attestors/qa-approval-attestor
```

---

#### Dry-Run Mode (Recommended for Initial Rollout)

Before enforcing, run in **audit-only mode** to see what would be blocked without breaking anything:

```yaml
defaultAdmissionRule:
  evaluationMode: ALWAYS_DENY
  enforcementMode: DRYRUN_AUDIT_LOG_ONLY   # Log but don't block
```

Check audit logs:

```bash
gcloud logging read \
  'resource.type="k8s_cluster" AND
   protoPayload.response.reason="BINARY_AUTHORIZATION"' \
  --limit=20 --format=json
```

---

#### IAM Roles for Binary Authorization (Least Privilege)

| Role | Granted To | Purpose |
|------|-----------|---------|
| `roles/binaryauthorization.policyEditor` | Platform/Security team | Create and update policies |
| `roles/binaryauthorization.attestorsEditor` | Security team | Manage attestors |
| `roles/binaryauthorization.attestorsViewer` | CI/CD service account | View attestors to create attestations |
| `roles/cloudkms.signerVerifier` | CI/CD service account | Sign attestations with KMS key |
| `roles/containeranalysis.notes.editor` | Security team (one-time setup) | Create Container Analysis notes |
| `roles/containeranalysis.occurrences.editor` | CI/CD service account | Create attestation occurrences |

---

#### Binary Authorization – Interview Quick-Fire Q&A

**Q: What happens if Binary Authorization is enabled but no attestation exists for an image?**
A: The pod creation is **rejected** by the admission controller. The event is logged in Cloud Audit Logs.

**Q: Can you bypass Binary Authorization in an emergency?**
A: Yes, using **break-glass** — add an annotation to the pod spec: `alpha.image-policy.k8s.io/break-glass: "true"`. This bypasses the check but **creates an audit log entry** for review.

**Q: Why use image digest instead of tag?**
A: Tags are mutable — someone could push a malicious image to the same tag. Digests (`sha256:...`) are immutable and tied to the exact image content.

**Q: How is this different from just restricting the registry?**
A: Registry restriction (e.g., `allowedNamePatterns`) only checks **where** the image comes from. Binary Authorization checks that the image has been **explicitly approved** through a cryptographic attestation chain — it verifies the image went through your pipeline.

**Q: Does Binary Authorization add latency to deployments?**
A: Negligible. The attestation check happens at admission time (when the pod spec is submitted), not at image pull time. It's a metadata lookup, not a scan.

**Q: Can you use Binary Authorization with Cloud Run?**
A: Yes. Binary Authorization supports GKE, Cloud Run, and Anthos clusters.

---

## Q3: Multi-Cloud Network Connectivity – Securely Connecting AWS VPC to GCP VPC

### Scenario

Your organization runs backend services in an **AWS VPC** (e.g., `10.0.0.0/16` in `eu-west-1`). A new microservice has been deployed in a **GCP VPC** (e.g., `10.1.0.0/16` in `europe-west1`). The two services need **private, low-latency communication** without any traffic traversing the public internet. Design a secure multi-cloud network interconnect.

### Requirements

- Private connectivity (no public IPs on workloads)
- Encrypted in transit
- Low latency (< 20ms round trip)
- Scalable bandwidth
- Centralized firewall/security controls
- DNS resolution across clouds

---

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AWS (eu-west-1)                              │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ VPC: 10.0.0.0/16                                             │   │
│  │                                                              │   │
│  │  ┌─────────────┐     ┌──────────────────┐                   │   │
│  │  │ Backend Svc │────▶│ Virtual Private   │                   │   │
│  │  │ 10.0.1.x    │     │ Gateway (VGW)     │                   │   │
│  │  └─────────────┘     └────────┬─────────┘                   │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────┬──────────────────────────────┘
                                       │
                          IPsec VPN Tunnel (encrypted)
                          or Dedicated Interconnect
                                       │
┌──────────────────────────────────────┴──────────────────────────────┐
│                         GCP (europe-west1)                           │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ VPC: 10.1.0.0/16                                             │   │
│  │                                                              │   │
│  │  ┌──────────────────┐     ┌─────────────┐                   │   │
│  │  │ Cloud VPN Gateway│────▶│ Microservice │                   │   │
│  │  │ or Interconnect  │     │ 10.1.1.x     │                   │   │
│  │  └──────────────────┘     └─────────────┘                   │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Option Comparison: VPN vs. Dedicated Interconnect

| Feature | Cloud VPN (HA) | Dedicated Interconnect | Partner Interconnect |
|---------|---------------|----------------------|---------------------|
| **Bandwidth** | Up to 3 Gbps per tunnel (multiple tunnels) | 10 Gbps or 100 Gbps per link | 50 Mbps – 50 Gbps |
| **Encryption** | IPsec built-in | MACsec (optional), or overlay VPN | Depends on partner |
| **Latency** | Depends on internet path | Lowest (private fiber) | Low (partner fiber) |
| **Cost** | Low ($0.05/hr per tunnel) | High (port fees + colocation) | Medium |
| **Setup Time** | Minutes | Weeks (physical cross-connect) | Days |
| **Best For** | Dev/test, < 3 Gbps, quick setup | Production, high throughput, strict latency SLAs | Production, no colocation presence |

**Recommendation:** For most multi-cloud scenarios, start with **HA VPN** (99.99% SLA). Upgrade to Dedicated Interconnect when bandwidth exceeds 3 Gbps consistently or sub-5ms latency is required.

---

### Step 1: GCP Side – Create HA VPN Gateway & Cloud Router

```bash
# 1a. Create HA VPN Gateway (two interfaces for redundancy)
gcloud compute vpn-gateways create gcp-to-aws-vpn \
  --network=my-gcp-vpc \
  --region=europe-west1

# 1b. Create Cloud Router (for BGP dynamic routing)
gcloud compute routers create gcp-aws-router \
  --network=my-gcp-vpc \
  --region=europe-west1 \
  --asn=65001  # GCP-side ASN (private range: 64512–65534)
```

**Output:** Note the two external IP addresses of the HA VPN gateway (e.g., `35.220.x.x` and `35.220.y.y`).

---

### Step 2: AWS Side – Create Virtual Private Gateway & Customer Gateways

```bash
# 2a. Create Virtual Private Gateway (VGW) and attach to VPC
aws ec2 create-vpn-gateway --type ipsec.1 --amazon-side-asn 65002
aws ec2 attach-vpn-gateway --vpn-gateway-id vgw-xxxxxxxx --vpc-id vpc-xxxxxxxx

# 2b. Create Customer Gateways (one for each GCP HA VPN interface)
aws ec2 create-customer-gateway \
  --type ipsec.1 \
  --public-ip 35.220.x.x \   # GCP HA VPN interface 0
  --bgp-asn 65001             # GCP's ASN

aws ec2 create-customer-gateway \
  --type ipsec.1 \
  --public-ip 35.220.y.y \   # GCP HA VPN interface 1
  --bgp-asn 65001

# 2c. Create VPN Connections (one per Customer Gateway for HA)
aws ec2 create-vpn-connection \
  --type ipsec.1 \
  --customer-gateway-id cgw-xxxxxxxx \
  --vpn-gateway-id vgw-xxxxxxxx \
  --options '{"TunnelOptions":[{"PreSharedKey":"STRONG_PSK_HERE_32_CHARS_MIN"}]}'

aws ec2 create-vpn-connection \
  --type ipsec.1 \
  --customer-gateway-id cgw-yyyyyyyy \
  --vpn-gateway-id vgw-xxxxxxxx \
  --options '{"TunnelOptions":[{"PreSharedKey":"ANOTHER_STRONG_PSK_32_CHARS"}]}'
```

**Output:** AWS provides tunnel endpoint IPs and BGP peer IPs for each connection (download the configuration file).

---

### Step 3: GCP Side – Create VPN Tunnels & BGP Sessions

Using the AWS tunnel endpoint IPs from the downloaded configuration:

```bash
# 3a. Create VPN Tunnels (one per AWS tunnel endpoint)
gcloud compute vpn-tunnels create tunnel-to-aws-0 \
  --vpn-gateway=gcp-to-aws-vpn \
  --vpn-gateway-region=europe-west1 \
  --peer-address=AWS_TUNNEL_0_OUTSIDE_IP \
  --shared-secret="STRONG_PSK_HERE_32_CHARS_MIN" \
  --router=gcp-aws-router \
  --region=europe-west1 \
  --interface=0  # HA VPN interface 0

gcloud compute vpn-tunnels create tunnel-to-aws-1 \
  --vpn-gateway=gcp-to-aws-vpn \
  --vpn-gateway-region=europe-west1 \
  --peer-address=AWS_TUNNEL_1_OUTSIDE_IP \
  --shared-secret="ANOTHER_STRONG_PSK_32_CHARS" \
  --router=gcp-aws-router \
  --region=europe-west1 \
  --interface=1  # HA VPN interface 1

# 3b. Add BGP interfaces to Cloud Router
gcloud compute routers add-interface gcp-aws-router \
  --interface-name=bgp-aws-0 \
  --vpn-tunnel=tunnel-to-aws-0 \
  --ip-address=169.254.10.1 \   # BGP link-local IP (from AWS config)
  --mask-length=30 \
  --region=europe-west1

gcloud compute routers add-interface gcp-aws-router \
  --interface-name=bgp-aws-1 \
  --vpn-tunnel=tunnel-to-aws-1 \
  --ip-address=169.254.20.1 \
  --mask-length=30 \
  --region=europe-west1

# 3c. Add BGP peers
gcloud compute routers add-bgp-peer gcp-aws-router \
  --peer-name=aws-peer-0 \
  --interface=bgp-aws-0 \
  --peer-ip-address=169.254.10.2 \  # AWS-side BGP IP
  --peer-asn=65002 \                 # AWS ASN
  --region=europe-west1

gcloud compute routers add-bgp-peer gcp-aws-router \
  --peer-name=aws-peer-1 \
  --interface=bgp-aws-1 \
  --peer-ip-address=169.254.20.2 \
  --peer-asn=65002 \
  --region=europe-west1
```

---

### Step 4: Verify Tunnel Status & BGP Routes

```bash
# GCP: Check tunnel status (should show "Established")
gcloud compute vpn-tunnels describe tunnel-to-aws-0 --region=europe-west1 \
  --format="value(status, detailedStatus)"

# GCP: Verify BGP learned routes (should see 10.0.0.0/16 from AWS)
gcloud compute routers get-status gcp-aws-router --region=europe-west1

# AWS: Check VPN connection status
aws ec2 describe-vpn-connections --vpn-connection-ids vpn-xxxxxxxx \
  --query 'VpnConnections[].VgwTelemetry[].{Status:Status,IP:OutsideIpAddress}'
```

**Expected:** Both tunnels show `ESTABLISHED`, BGP routes show the remote CIDR blocks.

---

### Step 5: Firewall Rules – Restrict Cross-Cloud Traffic

**GCP Side – VPC Firewall Rules:**

```bash
# Allow only specific ports from AWS CIDR
gcloud compute firewall-rules create allow-aws-to-microservice \
  --network=my-gcp-vpc \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:8080,tcp:443 \
  --source-ranges=10.0.0.0/16 \   # AWS VPC CIDR only
  --target-tags=microservice \
  --description="Allow AWS backend to reach GCP microservice on 8080/443"

# Deny all other cross-cloud traffic (explicit deny for logging)
gcloud compute firewall-rules create deny-all-from-aws \
  --network=my-gcp-vpc \
  --direction=INGRESS \
  --action=DENY \
  --rules=all \
  --source-ranges=10.0.0.0/16 \
  --priority=65534 \
  --enable-logging
```

**AWS Side – Security Group:**

```bash
# Security Group for the backend service
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxx \
  --protocol tcp \
  --port 443 \
  --cidr 10.1.0.0/16   # Only GCP VPC CIDR
```

---

### Step 6: Private DNS Resolution Across Clouds

Services should resolve each other by name (e.g., `microservice.internal.gcp`) not by IP.

**GCP Side – Cloud DNS Private Zone with Forwarding:**

```bash
# Create a private DNS zone for AWS resources visible in GCP
gcloud dns managed-zones create aws-internal \
  --dns-name="internal.aws." \
  --visibility=private \
  --networks=my-gcp-vpc \
  --description="Forward DNS for AWS private hosted zone"

# Add forwarding rule to AWS Route53 Resolver inbound endpoint
gcloud dns managed-zones update aws-internal \
  --forwarding-targets=10.0.0.2  # AWS Route53 Resolver Inbound IP
```

**AWS Side – Route53 Resolver:**

```bash
# Create Inbound Endpoint (GCP can query AWS private zones)
aws route53resolver create-resolver-endpoint \
  --direction INBOUND \
  --security-group-ids sg-xxxxxxxx \
  --ip-addresses SubnetId=subnet-xxxxxxxx,Ip=10.0.0.2

# Create Outbound Endpoint + Forwarding Rule (AWS can query GCP zones)
aws route53resolver create-resolver-endpoint \
  --direction OUTBOUND \
  --security-group-ids sg-xxxxxxxx \
  --ip-addresses SubnetId=subnet-xxxxxxxx

aws route53resolver create-resolver-rule \
  --domain-name "internal.gcp" \
  --rule-type FORWARD \
  --resolver-endpoint-id rslvr-out-xxxxxxxx \
  --target-ips "Ip=10.1.0.2"  # GCP Cloud DNS inbound policy IP
```

---

### Step 7: Monitoring & Alerting

```bash
# GCP: Create alert for tunnel down
gcloud alpha monitoring policies create \
  --display-name="VPN Tunnel Down" \
  --condition-display-name="Tunnel status != Established" \
  --condition-filter='resource.type="vpn_gateway" AND metric.type="compute.googleapis.com/vpn/tunnel_established"' \
  --condition-threshold-value=1 \
  --condition-threshold-comparison=COMPARISON_LT \
  --notification-channels=projects/PROJECT_ID/notificationChannels/CHANNEL_ID
```

**AWS: CloudWatch Alarm for VPN:**

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "VPN-Tunnel-Down" \
  --metric-name TunnelState \
  --namespace AWS/VPN \
  --statistic Maximum \
  --period 60 \
  --threshold 1 \
  --comparison-operator LessThanThreshold \
  --evaluation-periods 3 \
  --alarm-actions arn:aws:sns:eu-west-1:ACCOUNT_ID:alerts-topic \
  --dimensions Name=VpnId,Value=vpn-xxxxxxxx
```

---

### Security Best Practices Summary

| Practice | Implementation |
|----------|---------------|
| **Encryption in transit** | IPsec (AES-256-GCM) – built into Cloud VPN tunnels |
| **No public IPs on workloads** | Private subnets only; traffic flows over VPN tunnel |
| **Pre-shared key management** | Store in Secret Manager / AWS Secrets Manager; rotate every 90 days |
| **Network segmentation** | Firewall rules allow only required ports between specific CIDRs |
| **BGP route filtering** | Advertise only necessary subnets, not `0.0.0.0/0` |
| **Redundancy** | HA VPN (2 tunnels) + BGP failover = 99.99% SLA |
| **Monitoring** | Alert on tunnel down, BGP flap, unusual traffic volume |
| **Non-overlapping CIDRs** | Plan IP addressing upfront: AWS `10.0.0.0/16`, GCP `10.1.0.0/16` |

---

### Key Takeaways (Interview Talking Points)

- **HA VPN with BGP** gives you encrypted, redundant, auto-failover connectivity in minutes.
- **No static routes** – BGP dynamically exchanges routes; if one tunnel fails, traffic reroutes automatically.
- **Defense in depth** – VPN encryption + firewall rules + private DNS + no public IPs.
- Always plan **non-overlapping CIDR ranges** across clouds before connecting networks.
- For bandwidth > 3 Gbps or latency < 5ms, upgrade to **Dedicated Interconnect** with MACsec encryption.

---

## Q4: Multi-Cloud IAM & Zero-Trust Access – Federating Identities Across AWS, GCP, and Azure

### Scenario

Your company uses **Azure AD (Microsoft Entra ID)** as the corporate identity provider (IdP). Engineers need to access both **AWS** and **GCP** resources without separate credentials for each cloud. Design a **federated identity and access management strategy** that enforces Zero Trust principles:

- No static credentials / long-lived keys
- MFA enforced everywhere
- Least privilege access
- Short-lived sessions
- Conditional access (device compliance, location)
- Just-in-time (JIT) privilege escalation

---

### Architecture Overview

```
┌────────────────────────────────────────────────────────────────────┐
│                    Microsoft Entra ID (Azure AD)                    │
│                    ─────────────────────────────                    │
│                    Corporate Identity Provider                      │
│                                                                    │
│  • User identities & groups                                        │
│  • MFA policies                                                    │
│  • Conditional Access policies                                     │
│  • Privileged Identity Management (PIM)                            │
└────────────┬──────────────────────────────────┬────────────────────┘
             │ SAML 2.0                         │ OIDC
             │                                  │
             ▼                                  ▼
┌────────────────────────┐          ┌────────────────────────────────┐
│      AWS                │          │          GCP                    │
│                        │          │                                │
│  IAM Identity Center   │          │  Workforce Identity Federation │
│  (AWS SSO)             │          │  (or Workload Identity Fed.)   │
│                        │          │                                │
│  • Permission Sets     │          │  • Workforce Pool              │
│  • Session duration    │          │  • Attribute mappings          │
│  • Account access      │          │  • IAM role bindings           │
└────────────────────────┘          └────────────────────────────────┘
```

---

### Step 1: Azure AD (Entra ID) – Configure as Central IdP

**1a. Create Security Groups for Cloud Access:**

```powershell
# PowerShell – Azure AD Module
# Create groups that map to cloud roles
New-AzureADGroup -DisplayName "Cloud-AWS-Admins" -MailEnabled $false -SecurityEnabled $true -MailNickName "cloud-aws-admins"
New-AzureADGroup -DisplayName "Cloud-AWS-ReadOnly" -MailEnabled $false -SecurityEnabled $true -MailNickName "cloud-aws-readonly"
New-AzureADGroup -DisplayName "Cloud-GCP-Admins" -MailEnabled $false -SecurityEnabled $true -MailNickName "cloud-gcp-admins"
New-AzureADGroup -DisplayName "Cloud-GCP-Developers" -MailEnabled $false -SecurityEnabled $true -MailNickName "cloud-gcp-developers"
```

**1b. Configure Conditional Access Policies:**

In **Entra ID → Security → Conditional Access**, create:

| Policy Name | Conditions | Controls |
|-------------|-----------|----------|
| Require MFA for Cloud Access | Apps: AWS SSO, GCP Console | Grant: Require MFA |
| Block Untrusted Locations | Location: NOT corporate IP ranges | Grant: Block |
| Require Compliant Device | Device state: NOT compliant | Grant: Require device compliance |
| Session Timeout | All cloud apps | Session: Sign-in frequency = 8 hours |

**1c. Enable Privileged Identity Management (PIM) for JIT Access:**

```
Entra ID → Identity Governance → Privileged Identity Management → Azure AD Roles
```

- Assign "Cloud-AWS-Admins" and "Cloud-GCP-Admins" as **eligible** (not permanent) roles.
- Require **justification + approval** for activation.
- Set **maximum activation duration = 4 hours**.
- Require **MFA on activation**.

---

### Step 2: AWS Side – Configure IAM Identity Center (SSO) with Azure AD

**2a. Enable IAM Identity Center & Set External IdP:**

```
AWS Console → IAM Identity Center → Settings → Identity source → External identity provider
```

- **IdP sign-in URL:** `https://login.microsoftonline.com/TENANT_ID/saml2`
- **IdP issuer URL:** `https://sts.windows.net/TENANT_ID/`
- **Certificate:** Upload the Azure AD SAML signing certificate (base64)

**2b. Configure SCIM Provisioning (Auto-Sync Users & Groups):**

In Azure AD Enterprise Applications → AWS IAM Identity Center:
- Enable **Provisioning** → Automatic
- Provide the SCIM endpoint and token from AWS IAM Identity Center
- Map Azure AD groups to AWS Identity Center groups

**2c. Create Permission Sets (Least Privilege):**

```bash
# AWS CLI – Create permission sets
aws sso-admin create-permission-set \
  --instance-arn arn:aws:sso:::instance/ssoins-xxxxxxxx \
  --name "ReadOnlyAccess" \
  --session-duration "PT4H" \   # 4-hour session max
  --description "Read-only access to AWS resources"

aws sso-admin create-permission-set \
  --instance-arn arn:aws:sso:::instance/ssoins-xxxxxxxx \
  --name "AdminAccess" \
  --session-duration "PT1H" \   # 1-hour session for admin (short!)
  --description "Admin access - requires PIM approval"

# Attach AWS managed policy to permission set
aws sso-admin attach-managed-policy-to-permission-set \
  --instance-arn arn:aws:sso:::instance/ssoins-xxxxxxxx \
  --permission-set-arn arn:aws:sso:::permissionSet/ssoins-xxxxxxxx/ps-readonly \
  --managed-policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
```

**2d. Map Groups to Permission Sets & AWS Accounts:**

| Azure AD Group | AWS Permission Set | AWS Account(s) | Session Duration |
|---------------|-------------------|----------------|-----------------|
| Cloud-AWS-ReadOnly | ReadOnlyAccess | All accounts | 4 hours |
| Cloud-AWS-Admins | AdminAccess | Production only | 1 hour |
| Cloud-AWS-Admins | ReadOnlyAccess | All accounts | 4 hours |

---

### Step 3: GCP Side – Configure Workforce Identity Federation

**3a. Create a Workforce Identity Pool:**

```bash
# Create workforce pool (one per organization)
gcloud iam workforce-pools create azure-ad-pool \
  --organization=ORG_ID \
  --location=global \
  --display-name="Azure AD Federation" \
  --description="Federate corporate identities from Entra ID" \
  --session-duration="14400s"  # 4-hour sessions

# Create OIDC provider linked to Azure AD
gcloud iam workforce-pools providers create-oidc azure-ad-provider \
  --workforce-pool=azure-ad-pool \
  --location=global \
  --issuer-uri="https://login.microsoftonline.com/TENANT_ID/v2.0" \
  --client-id="GCP_APP_CLIENT_ID" \        # From Azure AD app registration
  --client-secret-value="CLIENT_SECRET" \   # Store securely
  --attribute-mapping="google.subject=assertion.sub,google.groups=assertion.groups,google.display_name=assertion.name" \
  --attribute-condition="assertion.aud == 'GCP_APP_CLIENT_ID'"
```

**3b. Grant IAM Roles Based on Azure AD Groups:**

```bash
# Map Azure AD group "Cloud-GCP-Developers" to GCP Viewer role
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="principalSet://iam.googleapis.com/locations/global/workforcePools/azure-ad-pool/group/CLOUD_GCP_DEVELOPERS_GROUP_ID" \
  --role="roles/viewer"

# Map Azure AD group "Cloud-GCP-Admins" to GCP Editor role (specific project)
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="principalSet://iam.googleapis.com/locations/global/workforcePools/azure-ad-pool/group/CLOUD_GCP_ADMINS_GROUP_ID" \
  --role="roles/editor" \
  --condition='expression=request.time < timestamp("2026-05-05T23:59:59Z"),title=temporary-access'
```

**3c. Configure Console Access via Workforce Identity:**

```bash
# Users access GCP Console via:
# https://console.cloud.google.com/workforce?workforce_pool=locations/global/workforcePools/azure-ad-pool&provider=azure-ad-provider

# Or use gcloud CLI with workforce identity:
gcloud auth login --workforce-pool-provider="locations/global/workforcePools/azure-ad-pool/providers/azure-ad-provider"
```

---

### Step 4: Workload Identity Federation (Service-to-Service, No Keys)

For **applications** (not humans) running in one cloud accessing another:

**Scenario:** An app in AWS (ECS/EKS) needs to call a GCP API.

```bash
# GCP: Create a Workload Identity Pool for AWS workloads
gcloud iam workload-identity-pools create aws-workload-pool \
  --location=global \
  --display-name="AWS Workloads"

# Create AWS provider in the pool
gcloud iam workload-identity-pools providers create-aws aws-provider \
  --workload-identity-pool=aws-workload-pool \
  --location=global \
  --account-id=AWS_ACCOUNT_ID  # Your AWS account number

# Grant GCP service account impersonation to a specific AWS role
gcloud iam service-accounts add-iam-policy-binding \
  myapp-gsa@PROJECT_ID.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/aws-workload-pool/attribute.aws_role/arn:aws:sts::AWS_ACCOUNT_ID:assumed-role/my-ecs-task-role"
```

**AWS application code (Python/boto3) → access GCP:**

```python
from google.auth import identity_pool
import google.auth.transport.requests

# credentials.json generated by:
# gcloud iam workload-identity-pools create-cred-config \
#   projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/aws-workload-pool/providers/aws-provider \
#   --service-account=myapp-gsa@PROJECT_ID.iam.gserviceaccount.com \
#   --aws --output-file=credentials.json

credentials = identity_pool.Credentials.from_file("credentials.json")
# Now use credentials to call GCP APIs – NO static keys involved!
```

---

### Step 5: Audit & Compliance

**Centralized Logging:**

| Cloud | Audit Log Source | Forward To |
|-------|-----------------|-----------|
| Azure AD | Sign-in logs, Audit logs | Azure Sentinel / SIEM |
| AWS | CloudTrail (SSO events) | S3 → SIEM |
| GCP | Cloud Audit Logs (Admin Activity) | BigQuery / SIEM |

**Key Events to Monitor:**

```bash
# GCP: Monitor workforce identity logins
gcloud logging read \
  'protoPayload.serviceName="sts.googleapis.com" AND
   protoPayload.methodName="google.identity.sts.v1.SecurityTokenService.ExchangeToken"' \
  --limit=20

# AWS: Monitor SSO login events
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=Authenticate \
  --max-results 20
```

**Alert on Suspicious Activity:**

- Login from unusual location (not corporate IP)
- Multiple failed MFA attempts
- Permission set activation outside business hours
- Access to production accounts from non-compliant device

---

### Step 6: Emergency Break-Glass Procedure

Even with federation, you need a break-glass path if Azure AD goes down:

| Cloud | Break-Glass Method | Security Control |
|-------|-------------------|-----------------|
| AWS | Dedicated IAM user (MFA + hardware key), sealed in password manager | Alert on any usage, rotate quarterly |
| GCP | Organization admin SA key (encrypted, stored in HSM/vault) | Alert on any usage, requires 2-person authorization |

```bash
# AWS: Create break-glass user (disabled by default)
aws iam create-user --user-name break-glass-admin
aws iam attach-user-policy --user-name break-glass-admin --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
aws iam create-virtual-mfa-device --virtual-mfa-device-name break-glass-mfa
# Store credentials in sealed vault, create CloudWatch alarm for any API call by this user
```

---

### Zero Trust Implementation Summary

| Zero Trust Principle | Implementation |
|---------------------|---------------|
| **Verify explicitly** | Every access request authenticated via Azure AD + MFA |
| **Least privilege** | Permission sets scoped to minimum; JIT activation for admin |
| **Assume breach** | Short sessions (1-4 hrs), conditional access, continuous monitoring |
| **No implicit trust** | Network location alone doesn't grant access; device compliance required |
| **Micro-segmentation** | Separate permission sets per account/project, group-based access |

---

### Key Takeaways (Interview Talking Points)

- **Single IdP (Azure AD)** = single source of truth for identity; no credential sprawl
- **SAML for AWS SSO, OIDC for GCP Workforce Identity** = standard protocols, no vendor lock-in
- **SCIM provisioning** = users/groups auto-sync; no manual account creation in each cloud
- **Short-lived sessions + JIT access** = even if a token is stolen, blast radius is limited
- **Workload Identity Federation** = services across clouds authenticate without static keys
- **Break-glass accounts** are essential but must be heavily monitored and rarely used

---

## Q5: Multi-Cloud Disaster Recovery – Migrating PostgreSQL from AWS RDS to GCP Cloud SQL with Near-Zero Downtime

### Scenario

You need to migrate a **production PostgreSQL 14 database** (500 GB) from **AWS RDS** to **GCP Cloud SQL** as part of a multi-cloud disaster recovery strategy. The application serves **live traffic 24/7**, so downtime must be minimized to **under 5 minutes**. Design a secure migration plan with rollback capability.

### Requirements

- Near-zero downtime (< 5 minutes cutover window)
- No data loss (RPO = 0)
- Encrypted data transfer (in transit and at rest)
- Validate data integrity post-migration
- Rollback plan if issues arise
- IAM-based database authentication (no long-lived passwords where possible)

---

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MIGRATION PHASES                                   │
│                                                                     │
│  Phase 1: Setup & Full Load        Phase 2: CDC (Change Data       │
│  (hours – runs in background)       Capture) Replication            │
│                                     (continuous until cutover)       │
│  ┌──────────┐   Full Dump    ┌──────────────┐                      │
│  │ AWS RDS  │──────────────▶│ GCP Cloud SQL │                      │
│  │ (Source) │               │  (Target)     │                      │
│  └──────────┘               └──────────────┘                      │
│       │                            ▲                                │
│       │      Logical Replication   │                                │
│       └────────────────────────────┘                                │
│              (WAL streaming via VPN)                                 │
│                                                                     │
│  Phase 3: Cutover (< 5 min)   Phase 4: Validation & Cleanup        │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Pre-Migration Checklist

| # | Task | Status |
|---|------|--------|
| 1 | VPN/Interconnect between AWS and GCP established (see Q3) | ☐ |
| 2 | Non-overlapping IP ranges confirmed | ☐ |
| 3 | PostgreSQL version compatibility verified (14 on both sides) | ☐ |
| 4 | Extensions audit – ensure all used extensions available in Cloud SQL | ☐ |
| 5 | Database size estimated (pg_database_size) | ☐ |
| 6 | RDS parameter group reviewed for replication settings | ☐ |
| 7 | Cutover window communicated to stakeholders | ☐ |
| 8 | Rollback plan documented and tested | ☐ |

---

### Step 1: Prepare AWS RDS Source for Logical Replication

**1a. Enable Logical Replication on RDS:**

```bash
# Modify the RDS parameter group
aws rds modify-db-parameter-group \
  --db-parameter-group-name my-postgres-params \
  --parameters "ParameterName=rds.logical_replication,ParameterValue=1,ApplyMethod=pending-reboot"

# Reboot the RDS instance to apply (schedule during low-traffic window)
aws rds reboot-db-instance --db-instance-identifier my-production-db
```

**1b. Verify Replication Settings:**

```sql
-- Connect to RDS and verify
SHOW wal_level;           -- Should return 'logical'
SHOW max_replication_slots;  -- Should be >= 5
SHOW max_wal_senders;        -- Should be >= 5
```

**1c. Create a Dedicated Replication User (Least Privilege):**

```sql
-- Create user with replication privilege only
CREATE USER migration_user WITH REPLICATION LOGIN PASSWORD 'STRONG_TEMP_PASSWORD';

-- Grant SELECT on all tables to be migrated
GRANT USAGE ON SCHEMA public TO migration_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO migration_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO migration_user;

-- Grant replication privilege for logical decoding
GRANT rds_replication TO migration_user;
```

> **Security Note:** This password is temporary. It will be revoked after migration. Store it in AWS Secrets Manager during the migration window.

---

### Step 2: Prepare GCP Cloud SQL Target

**2a. Create Cloud SQL Instance:**

```bash
gcloud sql instances create prod-postgres-dr \
  --database-version=POSTGRES_14 \
  --tier=db-custom-8-32768 \          # 8 vCPUs, 32 GB RAM (match RDS)
  --region=europe-west1 \
  --availability-type=REGIONAL \       # HA with automatic failover
  --storage-type=SSD \
  --storage-size=600GB \               # 20% buffer above current 500GB
  --storage-auto-increase \
  --network=projects/PROJECT_ID/global/networks/my-gcp-vpc \
  --no-assign-ip \                     # Private IP only (no public access!)
  --enable-point-in-time-recovery \
  --backup-start-time=02:00 \
  --retained-backups-count=30 \
  --database-flags=cloudsql.logical_decoding=on \
  --root-password="INITIAL_STRONG_PASSWORD" \
  --maintenance-window-day=SUN \
  --maintenance-window-hour=3 \
  --encryption-key=projects/PROJECT_ID/locations/europe-west1/keyRings/sql-keyring/cryptoKeys/sql-key  # CMEK
```

**2b. Configure Private Connectivity (from AWS VPN):**

```bash
# Ensure Cloud SQL is accessible from AWS via private IP
# The VPN from Q3 routes AWS traffic to GCP VPC where Cloud SQL lives

# Verify Cloud SQL private IP
gcloud sql instances describe prod-postgres-dr \
  --format="value(ipAddresses.filter(type='PRIVATE').ipAddress)"
```

**2c. Create Target Database & Schema:**

```bash
# Connect to Cloud SQL (via cloud-sql-proxy or direct private IP)
gcloud sql connect prod-postgres-dr --user=postgres

# Create the target database
CREATE DATABASE myapp_production;

# Apply schema (dump schema-only from RDS first)
# On a bastion/migration host with access to both:
pg_dump -h RDS_ENDPOINT -U migration_user -d myapp_production --schema-only > schema.sql
psql -h CLOUD_SQL_PRIVATE_IP -U postgres -d myapp_production < schema.sql
```

---

### Step 3: Set Up GCP Database Migration Service (DMS)

**3a. Create a Connection Profile for the Source (AWS RDS):**

```bash
gcloud database-migration connection-profiles create aws-rds-source \
  --region=europe-west1 \
  --display-name="AWS RDS PostgreSQL Source" \
  --provider=RDS \
  --type=POSTGRESQL \
  --host=my-production-db.xxxxxxxxxxxx.eu-west-1.rds.amazonaws.com \
  --port=5432 \
  --username=migration_user \
  --password="STRONG_TEMP_PASSWORD" \
  --database=myapp_production \
  --ssl-mode=REQUIRED \                # Enforce SSL for data in transit
  --client-certificate=@client-cert.pem \
  --client-key=@client-key.pem \
  --ca-certificate=@rds-ca-cert.pem
```

**3b. Create a Connection Profile for the Target (Cloud SQL):**

```bash
gcloud database-migration connection-profiles create gcp-cloudsql-target \
  --region=europe-west1 \
  --display-name="GCP Cloud SQL Target" \
  --provider=CLOUDSQL \
  --type=POSTGRESQL \
  --cloudsql-instance=prod-postgres-dr \
  --database=myapp_production
```

**3c. Create the Migration Job:**

```bash
gcloud database-migration migration-jobs create rds-to-cloudsql-migration \
  --region=europe-west1 \
  --display-name="Production PostgreSQL Migration" \
  --type=CONTINUOUS \               # Full dump + CDC (continuous replication)
  --source=aws-rds-source \
  --destination=gcp-cloudsql-target \
  --peer-vpc=my-gcp-vpc             # Use private networking (VPN tunnel)
```

**3d. Verify & Start the Migration:**

```bash
# Verify connectivity and prerequisites
gcloud database-migration migration-jobs verify rds-to-cloudsql-migration \
  --region=europe-west1

# Start the migration (full load begins)
gcloud database-migration migration-jobs start rds-to-cloudsql-migration \
  --region=europe-west1
```

---

### Step 4: Monitor Replication Progress

```bash
# Check migration job status
gcloud database-migration migration-jobs describe rds-to-cloudsql-migration \
  --region=europe-west1 \
  --format="table(name,state,phase,error)"

# Monitor replication lag (should approach 0 before cutover)
gcloud database-migration migration-jobs describe rds-to-cloudsql-migration \
  --region=europe-west1 \
  --format="value(performanceConfig.dumpParallelLevel)"
```

**On the RDS source – Monitor replication slot:**

```sql
-- Check replication lag on source
SELECT slot_name, confirmed_flush_lsn, pg_current_wal_lsn(),
       (pg_current_wal_lsn() - confirmed_flush_lsn) AS lag_bytes
FROM pg_replication_slots
WHERE slot_name LIKE '%migration%';
```

**Wait until replication lag is consistently < 1 MB** before proceeding to cutover.

---

### Step 5: Pre-Cutover Validation

Before cutting over, validate data integrity:

```sql
-- On SOURCE (AWS RDS):
SELECT schemaname, relname, n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables ORDER BY relname;

SELECT COUNT(*) FROM critical_table_1;
SELECT COUNT(*) FROM critical_table_2;
SELECT MAX(updated_at) FROM orders;  -- Latest record timestamp

-- On TARGET (GCP Cloud SQL) – same queries, compare results:
SELECT COUNT(*) FROM critical_table_1;
SELECT COUNT(*) FROM critical_table_2;
SELECT MAX(updated_at) FROM orders;
```

**Automated Validation Script:**

```bash
#!/bin/bash
# compare_row_counts.sh – Run from migration host with access to both DBs

TABLES=("users" "orders" "products" "transactions" "audit_log")

echo "Table | Source Count | Target Count | Match"
echo "------|-------------|-------------|------"

for table in "${TABLES[@]}"; do
  SRC=$(psql -h RDS_ENDPOINT -U migration_user -d myapp_production -t -c "SELECT COUNT(*) FROM $table;")
  TGT=$(psql -h CLOUD_SQL_IP -U postgres -d myapp_production -t -c "SELECT COUNT(*) FROM $table;")
  
  if [ "$SRC" = "$TGT" ]; then
    echo "$table | $SRC | $TGT | ✅"
  else
    echo "$table | $SRC | $TGT | ❌ MISMATCH"
  fi
done
```

---

### Step 6: Cutover (< 5 Minutes Downtime)

This is the critical window. Execute during lowest-traffic period.

**Cutover Runbook:**

| Time | Action | Who |
|------|--------|-----|
| T-30 min | Final validation – confirm replication lag < 100 KB | DBA |
| T-15 min | Notify stakeholders – maintenance window starting | Ops |
| T-5 min | Scale down application replicas to reduce writes | DevOps |
| **T+0** | **Stop application writes (set DB to read-only or stop app)** | **DevOps** |
| T+30 sec | Verify replication lag = 0 (fully caught up) | DBA |
| T+1 min | **Promote Cloud SQL (stop replication, make read-write)** | DBA |
| T+2 min | Update application connection string → Cloud SQL private IP | DevOps |
| T+3 min | Start application / scale up replicas | DevOps |
| T+4 min | Verify application is serving traffic from Cloud SQL | QA |
| T+5 min | **Migration complete – downtime window closed** | All |

**Execute Cutover Commands:**

```bash
# 1. Stop application writes (example: scale to 0)
kubectl scale deployment myapp --replicas=0 -n production

# 2. Wait for replication to fully catch up (lag = 0)
gcloud database-migration migration-jobs describe rds-to-cloudsql-migration \
  --region=europe-west1 --format="value(state)"
# Wait until state = "CDC_IN_PROGRESS" and lag = 0

# 3. Promote the migration (makes Cloud SQL the primary)
gcloud database-migration migration-jobs promote rds-to-cloudsql-migration \
  --region=europe-west1

# 4. Verify Cloud SQL is now read-write
gcloud sql instances describe prod-postgres-dr \
  --format="value(state)"  # Should be "RUNNABLE"

# 5. Update application config (DNS or connection string)
# Option A: Update DNS record (if using DNS-based connection)
gcloud dns record-sets update db.internal.myapp. \
  --zone=internal-zone \
  --type=A \
  --ttl=30 \
  --rrdatas=CLOUD_SQL_PRIVATE_IP

# Option B: Update Kubernetes secret with new connection string
kubectl create secret generic db-connection \
  --from-literal=host=CLOUD_SQL_PRIVATE_IP \
  --from-literal=port=5432 \
  --from-literal=database=myapp_production \
  --dry-run=client -o yaml | kubectl apply -f -

# 6. Restart application
kubectl scale deployment myapp --replicas=5 -n production

# 7. Verify application health
kubectl get pods -n production
curl -s https://myapp.example.com/healthz
```

---

### Step 7: Rollback Plan (If Issues Arise)

**Decision Criteria for Rollback:**

- Application errors > 5% within first 15 minutes
- Data integrity issues detected
- Cloud SQL performance significantly worse than RDS

**Rollback Procedure:**

```bash
# 1. Stop application
kubectl scale deployment myapp --replicas=0 -n production

# 2. Point connection back to AWS RDS
kubectl create secret generic db-connection \
  --from-literal=host=RDS_ENDPOINT \
  --from-literal=port=5432 \
  --from-literal=database=myapp_production \
  --dry-run=client -o yaml | kubectl apply -f -

# OR update DNS
gcloud dns record-sets update db.internal.myapp. \
  --zone=internal-zone \
  --type=A \
  --ttl=30 \
  --rrdatas=RDS_PRIVATE_IP

# 3. Restart application pointing to RDS
kubectl scale deployment myapp --replicas=5 -n production

# 4. If data was written to Cloud SQL during the window,
#    export and replay those transactions back to RDS:
pg_dump -h CLOUD_SQL_IP -U postgres -d myapp_production \
  --data-only --inserts \
  --table=orders \
  --where="created_at > 'CUTOVER_TIMESTAMP'" > delta.sql

psql -h RDS_ENDPOINT -U admin -d myapp_production < delta.sql
```

> **Important:** Keep the RDS instance running for at least **72 hours** after successful cutover as a safety net.

---

### Step 8: Post-Migration Security Hardening

**8a. Switch to IAM-Based Database Authentication (No Passwords):**

```bash
# Enable IAM authentication on Cloud SQL
gcloud sql instances patch prod-postgres-dr \
  --database-flags=cloudsql.iam_authentication=on

# Create IAM database user (mapped to GCP service account)
gcloud sql users create myapp-sa@PROJECT_ID.iam \
  --instance=prod-postgres-dr \
  --type=CLOUD_IAM_SERVICE_ACCOUNT

# Grant permissions in PostgreSQL
psql -h CLOUD_SQL_IP -U postgres -d myapp_production
GRANT CONNECT ON DATABASE myapp_production TO "myapp-sa@PROJECT_ID.iam";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "myapp-sa@PROJECT_ID.iam";
```

**8b. Remove Migration Artifacts:**

```bash
# Delete replication user on RDS
psql -h RDS_ENDPOINT -U admin -d myapp_production
DROP USER migration_user;

# Drop replication slot (prevents WAL accumulation)
SELECT pg_drop_replication_slot('migration_slot');

# Delete DMS connection profiles
gcloud database-migration connection-profiles delete aws-rds-source --region=europe-west1
gcloud database-migration connection-profiles delete gcp-cloudsql-target --region=europe-west1

# Revoke temporary passwords from Secrets Manager
aws secretsmanager delete-secret --secret-id migration-db-password --force-delete-without-recovery
```

**8c. Enable Ongoing Security Controls:**

```bash
# Enable query insights (performance monitoring)
gcloud sql instances patch prod-postgres-dr \
  --insights-config-query-insights-enabled \
  --insights-config-record-application-tags \
  --insights-config-record-client-address

# Enable audit logging (pgAudit)
gcloud sql instances patch prod-postgres-dr \
  --database-flags=cloudsql.enable_pgaudit=on,pgaudit.log=all

# Set up automated backups verification
gcloud sql backups list --instance=prod-postgres-dr
```

---

### Step 9: Set Up Ongoing DR (Bi-Directional Capability)

After migration, configure Cloud SQL as the primary with cross-region read replicas:

```bash
# Create a cross-region read replica for DR
gcloud sql instances create prod-postgres-dr-replica \
  --master-instance-name=prod-postgres-dr \
  --region=us-central1 \                 # Different region for geo-redundancy
  --tier=db-custom-8-32768 \
  --availability-type=REGIONAL \
  --no-assign-ip \
  --network=projects/PROJECT_ID/global/networks/my-gcp-vpc
```

**DR Failover Architecture:**

```
┌──────────────────────┐         ┌──────────────────────┐
│ GCP Cloud SQL        │         │ GCP Cloud SQL        │
│ (Primary)            │────────▶│ (Cross-Region Replica)│
│ europe-west1         │  Async  │ us-central1          │
│ Read + Write         │  Repli- │ Read-only            │
└──────────────────────┘  cation └──────────────────────┘
                                          │
                                  Promote if primary
                                  region goes down
```

---

### Migration Security Checklist

| Security Control | Implementation |
|-----------------|---------------|
| **Encryption in transit** | SSL/TLS required on DMS connection; data flows over VPN tunnel |
| **Encryption at rest** | CMEK (Customer-Managed Encryption Key) on Cloud SQL |
| **No public IP** | Cloud SQL has private IP only; accessible via VPN from AWS |
| **Least-privilege replication user** | SELECT + replication only; dropped after migration |
| **IAM DB authentication** | Post-migration: service accounts authenticate without passwords |
| **Audit logging** | pgAudit enabled; all queries logged to Cloud Logging |
| **Backup & PITR** | Automated backups + point-in-time recovery enabled |
| **Network isolation** | Firewall rules allow only application subnet → Cloud SQL port 5432 |
| **Secrets management** | Temp passwords stored in Secrets Manager; deleted post-migration |

---

### Key Takeaways (Interview Talking Points)

- **GCP Database Migration Service (DMS)** handles the heavy lifting: full load + continuous CDC replication.
- **Logical replication** allows the source to stay fully read-write during migration – zero impact on live traffic.
- **Cutover window < 5 minutes** is achieved by replicating continuously until lag = 0, then promoting.
- **Always have a rollback plan** – keep the source RDS running for 72+ hours post-cutover.
- **Post-migration hardening** is critical: switch to IAM auth, enable pgAudit, delete replication artifacts.
- **VPN/Interconnect** (from Q3) is a prerequisite – data never traverses the public internet.
- **CMEK encryption** gives you control over the encryption keys (vs. Google-managed keys).
- **Cross-region replicas** turn this into a true DR setup, not just a one-time migration.

---

*Last updated: 2026-05-05*
