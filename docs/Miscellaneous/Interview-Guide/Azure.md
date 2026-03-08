## Azure

### Microsoft Cloud Platform

##### Q. Access services without login through portal?
**Microsoft Graph API** - RESTful web API for accessing Microsoft Cloud resources

##### Q. Data migration strategy for cloud?
1. Problem and requirements analysis
2. Check ROI, CapEx, and zero downtime
3. Complete strategy and infrastructure plan with costs
4. Convince customer
5. Check pre-requisites and start migration

##### Q. Storage account access disabled at networking level?
Add "My Client IP Address" to Firewall networking rules, or:
- Use Virtual Network Service Endpoints
- Configure subnet access
- Access from virtual network

##### Q. Secured way to store secrets in Azure?
**Azure Key Vault** - Secure storage for secrets, keys, and certificates

##### Q. Access secured password from Key Vault via Terraform?
```hcl
data "azurerm_key_vault_secret" "example" {
  name = "secret-sauce"
  key_vault_id = data.azurerm_key_vault.existing.id
}

output "secret_value" {
  value = data.azurerm_key_vault_secret.example.value
  sensitive = true
}
```

##### Q. What is service principal?
Identity created for use with applications, hosted services, and automated tools to access Azure resources.

##### Q. What are managed identities?
Enterprise Application (Service Principal) linked to Azure resource, enables authentication without stored credentials.

**Types:**
1. **System-assigned:** Lifecycle tied to resource
2. **User-assigned:** Independent lifecycle, can be assigned to multiple resources

##### Q. Use case of Azure managed identities?
- Access resources from AKS (system-assigned)
- Perform AKS operations (user-assigned)

##### Q. What is Logic App?
Serverless orchestration and integration service with:
- Hundreds of connectors
- SQL Server, SAP, Azure Cognitive Services
- No scale/instance management
- Workflow definition with triggers and actions

**Trigger types:**
- Polling triggers (regular checks)
- Push triggers (event-driven)
- Recurrence, email, HTTP webhook

##### Q. What is Azure Hybrid Benefit?
Licensing offer for migration savings:
- Cost savings on Windows Server/SQL Server/Linux
- Requires Software Assurance or active subscription
- Modernization support
- Flexible hybrid environment

##### Q. What is Azure Service connection?
Represents Service Principal in Azure AD for headless authentication.

##### Q. Migrate Azure Key Vault secrets across subscriptions?
```bash
#!/bin/bash
SOURCE_KEYVAULT="keyvaultold"
DESTINATION_KEYVAULT="keyvaultnewtest"

SECRETS+=($(az keyvault secret list --vault-name $SOURCE_KEYVAULT --query "[].id" -o tsv))

for SECRET in "${SECRETS[@]}"; do
  SECRETNAME=$(echo "$SECRET" | sed 's|.*/||')
  SECRET_CHECK=$(az keyvault secret list --vault-name $DESTINATION_KEYVAULT --query "[?name=='$SECRETNAME']" -o tsv)
  
  if [ -n "$SECRET_CHECK" ]; then
    echo "Secret $SECRETNAME already exists"
  else
    echo "Copying $SECRETNAME"
    SECRET=$(az keyvault secret show --vault-name $SOURCE_KEYVAULT -n $SECRETNAME --query "value" -o tsv)
    az keyvault secret set --vault-name $DESTINATION_KEYVAULT -n $SECRETNAME --value "$SECRET" >/dev/null
  fi
done
```

##### Q. Azure DevOps migration between tenants?
1. Prepare users in new tenant
2. Change AAD connection
3. User mapping after migration
4. Document all RBAC roles
5. Migrate subscription
6. Restore RBAC, Key Vault, Storage Account access
7. Re-create Service Principals
8. Adjust pipelines

##### Q. Azure Front Door vs Traffic Manager vs Application Gateway vs Load Balancer?

**Load Balancer:**
- Network load balancer (Layer 4)
- Internal and Public
- Regional
- Non-HTTP(S) traffic
- Zone redundant

**Application Gateway:**
- Web traffic load balancer (Layer 7)
- Path-based routing
- Regional
- HTTP(S) traffic
- Zone redundant
- WAF support

**Traffic Manager:**
- DNS-based (Layer 7)
- Global
- Multiple routing methods
- Resilient to regional failures

**Front Door:**
- Global application delivery (Layer 7)
- Edge network proxy
- Global
- HTTP(S) traffic
- Resilient to regional failures
- WAF support

##### Q. Deploy container based on label in AKS?
Use Azure/Kubernetes Policy: "Kubernetes cluster pods should use specified labels"

Policy enforces label requirements for pod deployment.

---

### MLOps, AIOps, Data Engineering & Security

##### Q. How do you implement an end-to-end MLOps pipeline in Azure with automated retraining and deployment?

**Answer:**
Building a production-grade MLOps pipeline in Azure requires orchestrating multiple services for continuous training, validation, and deployment.

**Architecture Components:**
1. **Azure Machine Learning Workspace** - Central hub for ML operations
2. **Azure DevOps/GitHub Actions** - CI/CD orchestration
3. **Azure Data Factory** - Data pipeline automation
4. **Azure Container Registry** - Model container storage
5. **Azure Kubernetes Service** - Model serving infrastructure

**Implementation Steps:**

```bash
# Create ML Workspace
az ml workspace create \
  --name ml-workspace-prod \
  --resource-group ml-rg \
  --location eastus

# Create compute cluster for training
az ml compute create \
  --name gpu-cluster \
  --type AmlCompute \
  --size Standard_NC6s_v3 \
  --min-instances 0 \
  --max-instances 4 \
  --workspace-name ml-workspace-prod \
  --resource-group ml-rg

# Register dataset
az ml data create \
  --name customer-churn-data \
  --version 1 \
  --type uri_folder \
  --path azureml://datastores/workspaceblobstore/paths/data/ \
  --workspace-name ml-workspace-prod \
  --resource-group ml-rg
```

**Python MLOps Pipeline (training_pipeline.py):**
```python
from azure.ai.ml import MLClient, command, Input, Output
from azure.ai.ml.entities import Model, ManagedOnlineEndpoint, ManagedOnlineDeployment
from azure.identity import DefaultAzureCredential
import mlflow

# Connect to workspace
ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="<subscription-id>",
    resource_group_name="ml-rg",
    workspace_name="ml-workspace-prod"
)

# Define training job
job = command(
    code="./src",
    command="python train.py --data ${{inputs.training_data}} --model-output ${{outputs.model_output}}",
    inputs={
        "training_data": Input(type="uri_folder", path="azureml:customer-churn-data:1")
    },
    outputs={
        "model_output": Output(type="uri_folder", mode="rw_mount")
    },
    environment="azureml:sklearn-env:1",
    compute="gpu-cluster",
    experiment_name="churn-prediction",
    display_name="automated-training-run"
)

# Submit training job
returned_job = ml_client.jobs.create_or_update(job)

# Model registration with MLflow
mlflow.set_tracking_uri(ml_client.workspaces.get(ml_client.workspace_name).mlflow_tracking_uri)

with mlflow.start_run():
    mlflow.sklearn.log_model(model, "model")
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("precision", 0.93)
    mlflow.register_model("runs:/<run-id>/model", "churn-predictor")
```

**Azure DevOps Pipeline (azure-pipelines.yml):**
```yaml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - data/*
      - models/*

variables:
  - group: ml-variables

stages:
  - stage: DataValidation
    jobs:
      - job: ValidateData
        steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'ml-service-connection'
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                az extension add -n ml
                python scripts/validate_data.py

  - stage: TrainModel
    dependsOn: DataValidation
    jobs:
      - job: TrainAndValidate
        steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'ml-service-connection'
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                az ml job create --file training-job.yml
                python scripts/validate_model.py --min-accuracy 0.90

  - stage: DeployModel
    dependsOn: TrainModel
    condition: succeeded()
    jobs:
      - deployment: DeployToStaging
        environment: 'staging'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureCLI@2
                  inputs:
                    azureSubscription: 'ml-service-connection'
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      # Create/update endpoint
                      az ml online-endpoint create --name churn-endpoint-staging -f endpoint.yml
                      
                      # Deploy model
                      az ml online-deployment create \
                        --name blue \
                        --endpoint churn-endpoint-staging \
                        --file deployment.yml \
                        --all-traffic

      - deployment: DeployToProduction
        dependsOn: DeployToStaging
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureCLI@2
                  inputs:
                    azureSubscription: 'ml-service-connection'
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      # Blue-Green deployment
                      az ml online-deployment create \
                        --name green \
                        --endpoint churn-endpoint-prod \
                        --file deployment.yml
                      
                      # Gradual traffic shift
                      az ml online-endpoint update \
                        --name churn-endpoint-prod \
                        --traffic "blue=90 green=10"
```

**Automated Retraining with Data Drift Detection:**
```python
from azureml.datadrift import DataDriftDetector
from azure.ai.ml import MLClient

# Set up data drift monitoring
drift_detector = DataDriftDetector.create_from_datasets(
    workspace=workspace,
    name="churn-data-drift",
    baseline_data_set=baseline_dataset,
    target_data_set=production_dataset,
    compute_target="cpu-cluster",
    frequency="Week",
    feature_list=["age", "tenure", "monthly_charges"],
    drift_threshold=0.3
)

# Automated retraining trigger
if drift_detector.get_output().drift_coefficient > 0.3:
    # Trigger retraining pipeline
    ml_client.jobs.create_or_update(training_job)
```

**Key Best Practices:**
- Implement model versioning with semantic versioning
- Use feature stores for consistent feature engineering
- Monitor model performance with Azure Monitor
- Implement A/B testing with traffic splitting
- Use responsible AI dashboard for bias detection
- Enable audit logging for compliance

---

##### Q. How do you implement AIOps for incident prediction and automated remediation in Azure?

**Answer:**
AIOps in Azure leverages machine learning to predict incidents, detect anomalies, and automate remediation before they impact users.

**Architecture:**
1. **Azure Monitor** - Metrics and log collection
2. **Log Analytics** - Centralized logging
3. **Azure Machine Learning** - Anomaly detection models
4. **Azure Logic Apps/Automation** - Automated remediation
5. **Application Insights** - Smart detection

**Implementation:**

```bash
# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group aiops-rg \
  --workspace-name aiops-workspace \
  --location eastus

# Enable diagnostic settings for all resources
az monitor diagnostic-settings create \
  --name send-to-analytics \
  --resource /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{vm} \
  --workspace aiops-workspace \
  --logs '[{"category": "Administrative", "enabled": true}]' \
  --metrics '[{"category": "AllMetrics", "enabled": true}]'
```

**KQL Query for Anomaly Detection:**
```kusto
// Detect CPU anomalies using time series analysis
Perf
| where TimeGenerated > ago(30d)
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| make-series CPUUsage=avg(CounterValue) on TimeGenerated step 5m
| extend anomalies = series_decompose_anomalies(CPUUsage, 1.5, -1, 'linefit')
| mv-expand TimeGenerated, CPUUsage, anomalies
| where anomalies != 0
| project TimeGenerated, CPUUsage, anomalies, Computer
```

**Python Script for Predictive Incident Detection:**
```python
from azure.monitor.query import LogsQueryClient, MetricsQueryClient
from azure.identity import DefaultAzureCredential
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np

credential = DefaultAzureCredential()
logs_client = LogsQueryClient(credential)

# Query historical incident data
query = """
AzureActivity
| where TimeGenerated > ago(90d)
| where CategoryValue == "Administrative" and ActivityStatusValue == "Failure"
| summarize FailureCount=count() by bin(TimeGenerated, 1h), ResourceGroup, OperationNameValue
| extend Hour = hourofday(TimeGenerated), DayOfWeek = dayofweek(TimeGenerated)
"""

response = logs_client.query_workspace(workspace_id, query, timespan=timedelta(days=90))
df = pd.DataFrame(response.tables[0].rows, columns=[col.name for col in response.tables[0].columns])

# Train anomaly detection model
features = df[['Hour', 'DayOfWeek', 'FailureCount']].values
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(features)

# Predict anomalies in real-time
predictions = model.predict(current_metrics)
anomalies = predictions == -1

if anomalies.any():
    # Trigger alert
    trigger_remediation(df[anomalies])
```

**Automated Remediation with Azure Automation:**
```python
# automation_runbook.py
import azure.mgmt.compute
from azure.identity import DefaultAzureCredential

def remediate_high_cpu(vm_name, resource_group):
    """Automatically restart VM if CPU is consistently high"""
    credential = DefaultAzureCredential()
    compute_client = azure.mgmt.compute.ComputeManagementClient(credential, subscription_id)
    
    # Check if issue persists
    if confirm_issue_persists(vm_name):
        # Take snapshot before remediation
        snapshot = create_vm_snapshot(vm_name, resource_group)
        
        # Restart VM
        async_vm_restart = compute_client.virtual_machines.begin_restart(
            resource_group, vm_name
        )
        async_vm_restart.wait()
        
        # Verify remediation
        if check_health(vm_name):
            log_success(vm_name, "CPU issue resolved after restart")
        else:
            escalate_to_oncall(vm_name, snapshot)
```

**Alert Rule with Action Group:**
```bash
# Create action group for automated remediation
az monitor action-group create \
  --name auto-remediation-group \
  --resource-group aiops-rg \
  --action webhook aiops-webhook https://automation-webhook.azure.com/webhooks \
  --action azurefunction aiops-function /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Web/sites/{function-app}/functions/remediate

# Create smart alert rule
az monitor metrics alert create \
  --name high-cpu-prediction \
  --resource-group aiops-rg \
  --scopes /subscriptions/{sub}/resourceGroups/{rg} \
  --condition "avg Percentage CPU > 80" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action auto-remediation-group \
  --description "Predicted CPU spike - auto-remediate"
```

**Application Insights Smart Detection:**
```bash
# Enable proactive detection
az monitor app-insights component update \
  --app aiops-app-insights \
  --resource-group aiops-rg \
  --set "properties.DisableIpMasking=false" \
  --set "properties.IngestionMode=LogAnalytics"

# Configure smart detection rules
az rest --method PUT \
  --url "https://management.azure.com/subscriptions/{sub}/resourceGroups/{rg}/providers/microsoft.insights/components/{app}/ProactiveDetectionConfigs/slowpageloadtime?api-version=2018-05-01-preview" \
  --body '{"properties": {"enabled": true, "sendEmailsToSubscriptionOwners": true, "customEmails": ["oncall@example.com"]}}'
```

---

##### Q. How do you build a secure, real-time data engineering pipeline in Azure with data quality checks?

**Answer:**
Modern data engineering in Azure requires real-time processing, data quality validation, and security at every layer.

**Architecture:**
1. **Azure Event Hubs** - Streaming ingestion
2. **Azure Stream Analytics** - Real-time processing
3. **Azure Data Factory** - Batch orchestration
4. **Azure Databricks** - Advanced transformations
5. **Azure Purview** - Data governance
6. **Azure Synapse Analytics** - Data warehouse

**Secure Real-time Pipeline Implementation:**

```bash
# Create Event Hub with encryption
az eventhubs namespace create \
  --name streaming-data-hub \
  --resource-group data-eng-rg \
  --location eastus \
  --sku Standard \
  --enable-kafka true \
  --enable-auto-inflate true \
  --maximum-throughput-units 20

# Enable customer-managed key encryption
az eventhubs namespace encryption create \
  --namespace-name streaming-data-hub \
  --resource-group data-eng-rg \
  --encryption-config key-name=data-encryption-key \
    key-vault-uri=https://data-keyvault.vault.azure.net \
    user-assigned-identity=/subscriptions/{sub}/resourcegroups/{rg}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/eventhub-identity

# Create Event Hub with private endpoint
az eventhubs eventhub create \
  --name transaction-events \
  --namespace-name streaming-data-hub \
  --resource-group data-eng-rg \
  --partition-count 8 \
  --message-retention 7

# Set up private endpoint
az network private-endpoint create \
  --name eventhub-private-endpoint \
  --resource-group data-eng-rg \
  --vnet-name data-vnet \
  --subnet data-subnet \
  --private-connection-resource-id /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.EventHub/namespaces/streaming-data-hub \
  --group-id namespace \
  --connection-name eventhub-connection
```

**Stream Analytics with Data Quality Checks:**
```sql
-- Stream Analytics Query with validation
WITH ValidatedData AS (
    SELECT
        *,
        CASE 
            WHEN transaction_amount IS NULL THEN 'NULL_AMOUNT'
            WHEN transaction_amount < 0 THEN 'NEGATIVE_AMOUNT'
            WHEN transaction_amount > 1000000 THEN 'SUSPICIOUS_AMOUNT'
            WHEN LEN(customer_id) != 10 THEN 'INVALID_CUSTOMER_ID'
            WHEN transaction_timestamp > System.Timestamp() THEN 'FUTURE_TIMESTAMP'
            ELSE 'VALID'
        END AS ValidationStatus
    FROM TransactionInputStream TIMESTAMP BY transaction_timestamp
),
DataQualityMetrics AS (
    SELECT
        System.Timestamp() AS WindowEnd,
        COUNT(*) AS TotalRecords,
        SUM(CASE WHEN ValidationStatus = 'VALID' THEN 1 ELSE 0 END) AS ValidRecords,
        SUM(CASE WHEN ValidationStatus != 'VALID' THEN 1 ELSE 0 END) AS InvalidRecords,
        (SUM(CASE WHEN ValidationStatus = 'VALID' THEN 1.0 ELSE 0 END) / COUNT(*)) * 100 AS DataQualityScore
    FROM ValidatedData
    GROUP BY TumblingWindow(minute, 5)
)

-- Output valid data to Synapse
SELECT 
    transaction_id,
    customer_id,
    transaction_amount,
    transaction_timestamp,
    merchant_id
INTO SynapseOutput
FROM ValidatedData
WHERE ValidationStatus = 'VALID'

-- Output invalid data to quarantine
SELECT 
    *,
    System.Timestamp() AS QuarantineTimestamp
INTO QuarantineOutput
FROM ValidatedData
WHERE ValidationStatus != 'VALID'

-- Output quality metrics to monitoring
SELECT *
INTO QualityMetricsOutput
FROM DataQualityMetrics
WHERE DataQualityScore < 95 -- Alert when quality drops below 95%
```

**Azure Databricks Pipeline with Great Expectations:**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from delta.tables import DeltaTable
import great_expectations as ge
from great_expectations.dataset import SparkDFDataset

# Initialize Spark with Delta Lake
spark = SparkSession.builder \
    .appName("SecureDataPipeline") \
    .config("spark.databricks.delta.optimizeWrite.enabled", "true") \
    .config("spark.databricks.delta.autoCompact.enabled", "true") \
    .getOrCreate()

# Read from Event Hub with managed identity
df_stream = spark.readStream \
    .format("eventhubs") \
    .option("eventhubs.connectionString", dbutils.secrets.get("keyvault", "eventhub-connection")) \
    .option("eventhubs.consumerGroup", "databricks-consumer") \
    .load()

# Parse JSON payload
parsed_df = df_stream.select(
    get_json_object(col("body").cast("string"), "$.transaction_id").alias("transaction_id"),
    get_json_object(col("body").cast("string"), "$.customer_id").alias("customer_id"),
    get_json_object(col("body").cast("string"), "$.amount").cast("decimal(18,2)").alias("amount"),
    get_json_object(col("body").cast("string"), "$.timestamp").cast("timestamp").alias("timestamp"),
    col("enqueuedTime")
)

# Data quality validation with Great Expectations
def validate_data_quality(df, batch_id):
    """Apply data quality checks using Great Expectations"""
    
    # Convert to Pandas for GE (for batch processing)
    pandas_df = df.toPandas()
    ge_df = ge.from_pandas(pandas_df)
    
    # Define expectations
    expectation_suite = {
        "transaction_id": [
            ge_df.expect_column_values_to_not_be_null("transaction_id"),
            ge_df.expect_column_values_to_be_unique("transaction_id")
        ],
        "amount": [
            ge_df.expect_column_values_to_be_between("amount", min_value=0, max_value=1000000),
            ge_df.expect_column_values_to_not_be_null("amount")
        ],
        "customer_id": [
            ge_df.expect_column_values_to_match_regex("customer_id", r"^CUST\d{6}$")
        ]
    }
    
    # Validate and get results
    validation_result = ge_df.validate()
    
    if not validation_result["success"]:
        # Log failures to monitoring
        failed_expectations = [exp for exp in validation_result["results"] if not exp["success"]]
        log_data_quality_issues(failed_expectations, batch_id)
        
        # Quarantine bad records
        quarantine_df = df.filter(~quality_condition)
        quarantine_df.write.format("delta").mode("append").save("/mnt/quarantine/")
        
        # Filter to valid records only
        return df.filter(quality_condition)
    
    return df

# Apply transformations with PII masking
transformed_df = parsed_df \
    .withColumn("customer_id_masked", 
                when(col("customer_id").isNotNull(), 
                     concat(lit("***"), substring(col("customer_id"), -4, 4)))
                .otherwise(None)) \
    .withColumn("processing_timestamp", current_timestamp()) \
    .withColumn("data_classification", lit("CONFIDENTIAL"))

# Write to Delta Lake with ACID transactions
query = transformed_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/mnt/checkpoints/transactions") \
    .foreachBatch(validate_data_quality) \
    .trigger(processingTime="10 seconds") \
    .start("/mnt/delta/transactions")

query.awaitTermination()
```

**Data Factory Pipeline with Monitoring:**
```json
{
  "name": "SecureDataPipeline",
  "properties": {
    "activities": [
      {
        "name": "ValidateSourceData",
        "type": "Validation",
        "policy": {
          "timeout": "0.00:10:00",
          "retry": 3
        },
        "typeProperties": {
          "dataset": {
            "referenceName": "SourceDataset"
          },
          "minimumSize": 1024,
          "childItems": true
        }
      },
      {
        "name": "ExecuteDataQuality",
        "type": "DatabricksNotebook",
        "dependsOn": [
          {
            "activity": "ValidateSourceData",
            "dependencyConditions": ["Succeeded"]
          }
        ],
        "typeProperties": {
          "notebookPath": "/Notebooks/DataQualityChecks",
          "baseParameters": {
            "batch_id": "@pipeline().RunId",
            "source_path": "@dataset().folderPath"
          }
        },
        "linkedServiceName": {
          "referenceName": "DatabricksLinkedService"
        }
      },
      {
        "name": "DataQualityCheck",
        "type": "IfCondition",
        "dependsOn": [
          {
            "activity": "ExecuteDataQuality",
            "dependencyConditions": ["Succeeded"]
          }
        ],
        "typeProperties": {
          "expression": {
            "@greater(activity('ExecuteDataQuality').output.qualityScore, 95)"
          },
          "ifTrueActivities": [
            {
              "name": "LoadToSynapse",
              "type": "Copy",
              "inputs": [
                {
                  "referenceName": "ValidatedDelta"
                }
              ],
              "outputs": [
                {
                  "referenceName": "SynapseDestination"
                }
              ]
            }
          ],
          "ifFalseActivities": [
            {
              "name": "SendQualityAlert",
              "type": "WebActivity",
              "typeProperties": {
                "url": "https://logic-app-url.azure.com",
                "method": "POST",
                "body": {
                  "message": "Data quality below threshold",
                  "pipeline": "@pipeline().Pipeline",
                  "runId": "@pipeline().RunId"
                }
              }
            }
          ]
        }
      }
    ]
  }
}
```

**Azure Purview for Data Governance:**
```bash
# Register data sources in Purview
az purview account create \
  --name data-governance-purview \
  --resource-group data-eng-rg \
  --location eastus \
  --managed-resource-group-name purview-managed-rg

# Scan data sources
az purview scan create \
  --account-name data-governance-purview \
  --data-source-name synapse-source \
  --scan-name daily-scan \
  --scan-ruleset-name "AzureSynapseAnalytics"
```

---

##### Q. How do you implement Zero Trust security architecture in Azure for multi-cloud data platforms?

**Answer:**
Zero Trust in Azure assumes breach and verifies every request, essential for modern multi-cloud environments.

**Core Principles:**
1. Verify explicitly - Always authenticate and authorize
2. Use least privilege access - JIT/JEA
3. Assume breach - Minimize blast radius

**Implementation:**

```bash
# Enable Azure AD Conditional Access
az ad policy create \
  --display-name "Zero-Trust-Data-Access" \
  --definition '{
    "conditions": {
      "users": {"includeUsers": ["all"]},
      "applications": {"includeApplications": ["all"]},
      "locations": {"includeLocations": ["all"]},
      "clientAppTypes": ["browser", "mobileAppsAndDesktopClients"],
      "signInRiskLevels": ["high", "medium"],
      "deviceStates": {"excludeStates": ["compliant"]}
    },
    "grantControls": {
      "operator": "AND",
      "builtInControls": ["mfa", "compliantDevice", "domainJoinedDevice"]
    },
    "sessionControls": {
      "signInFrequency": {"value": 1, "type": "hours"}
    }
  }'

# Implement JIT VM access
az security jit-policy create \
  --resource-group data-eng-rg \
  --name jit-vm-policy \
  --location eastus \
  --virtual-machines "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/data-vm" \
  --ports '[{"number": 22, "protocol": "TCP", "allowedSourceAddressPrefix": "10.0.0.0/8", "maxRequestAccessDuration": "PT3H"}]'

# Enable Microsoft Defender for Cloud
az security pricing create \
  --name VirtualMachines \
  --tier Standard

az security pricing create \
  --name SqlServers \
  --tier Standard

az security pricing create \
  --name StorageAccounts \
  --tier Standard

# Configure Private Link for all services
az network private-endpoint create \
  --name synapse-private-endpoint \
  --resource-group data-eng-rg \
  --vnet-name data-vnet \
  --subnet data-subnet \
  --private-connection-resource-id /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Synapse/workspaces/data-synapse \
  --group-id Sql \
  --connection-name synapse-sql-connection

# Disable public network access
az synapse workspace update \
  --name data-synapse \
  --resource-group data-eng-rg \
  --enable-public-network-access false

az storage account update \
  --name datastorageacct \
  --resource-group data-eng-rg \
  --default-action Deny \
  --bypass AzureServices
```

**Implement Customer-Managed Keys:**
```bash
# Create Key Vault with purge protection
az keyvault create \
  --name data-encryption-kv \
  --resource-group data-eng-rg \
  --location eastus \
  --enable-purge-protection true \
  --enable-soft-delete true \
  --retention-days 90

# Create encryption key
az keyvault key create \
  --vault-name data-encryption-kv \
  --name data-master-key \
  --protection hsm \
  --size 4096 \
  --kty RSA-HSM

# Enable CMK encryption on storage
az storage account update \
  --name datastorageacct \
  --resource-group data-eng-rg \
  --encryption-key-name data-master-key \
  --encryption-key-vault https://data-encryption-kv.vault.azure.net \
  --encryption-key-source Microsoft.Keyvault

# Enable CMK for Synapse
az synapse workspace key create \
  --workspace-name data-synapse \
  --name workspace-encryption-key \
  --key-identifier https://data-encryption-kv.vault.azure.net/keys/data-master-key
```

**Network Security with Azure Firewall:**
```bash
# Create Azure Firewall for data platform
az network firewall create \
  --name data-firewall \
  --resource-group data-eng-rg \
  --location eastus \
  --vnet-name data-vnet

# Create application rules for data egress
az network firewall application-rule create \
  --collection-name AllowDataSources \
  --firewall-name data-firewall \
  --name AllowAPI \
  --protocols https=443 \
  --source-addresses 10.0.0.0/16 \
  --target-fqdns "*.database.windows.net" "*.vault.azure.net" "*.blob.core.windows.net" \
  --priority 100 \
  --action Allow \
  --resource-group data-eng-rg

# Deny all other traffic
az network firewall network-rule create \
  --collection-name DenyAllOutbound \
  --destination-addresses "*" \
  --destination-ports "*" \
  --firewall-name data-firewall \
  --name DenyInternet \
  --protocols Any \
  --source-addresses 10.0.0.0/16 \
  --action Deny \
  --priority 200 \
  --resource-group data-eng-rg
```

**Data Classification and DLP:**
```python
# Azure Purview data classification
from azure.purview.catalog import PurviewCatalogClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = PurviewCatalogClient(
    endpoint="https://data-governance-purview.purview.azure.com",
    credential=credential
)

# Apply sensitivity labels
classification = {
    "typeName": "Microsoft.Label.Confidential",
    "attributes": {
        "name": "customer_pii",
        "description": "Customer Personal Identifiable Information"
    }
}

# Implement column-level security in Synapse
synapse_security_sql = """
-- Dynamic data masking for PII
ALTER TABLE customers
ALTER COLUMN email ADD MASKED WITH (FUNCTION = 'email()');

ALTER TABLE customers
ALTER COLUMN phone ADD MASKED WITH (FUNCTION = 'partial(1,"XXX-XXX-",4)');

ALTER TABLE customers  
ALTER COLUMN ssn ADD MASKED WITH (FUNCTION = 'default()');

-- Row-level security
CREATE SCHEMA Security;

CREATE FUNCTION Security.fn_securitypredicate(@Region AS nvarchar(100))
    RETURNS TABLE
WITH SCHEMABINDING
AS
    RETURN SELECT 1 AS fn_securitypredicate_result
    WHERE @Region = USER_NAME() OR USER_NAME() = 'DataAdmin';

CREATE SECURITY POLICY RegionFilter
ADD FILTER PREDICATE Security.fn_securitypredicate(Region)
ON dbo.Sales
WITH (STATE = ON);
```

---

##### Q. How do you implement a Feature Store in Azure for ML model consistency and governance?

**Answer:**
A Feature Store centralizes feature engineering, ensuring consistency between training and serving while providing governance and lineage.

**Architecture with Azure ML Feature Store:**

```bash
# Create feature store (preview feature)
az ml feature-store create \
  --name enterprise-feature-store \
  --resource-group ml-rg \
  --location eastus \
  --materialization-store account_name=featurestoreacct \
  --offline-store account_name=offlinestoreacct \
  --online-store account_name=onlinestoreacct \
  --grant-materialization-permissions true
```

**Define Feature Sets:**
```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import FeatureSet, FeatureSetSpecification
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="<sub-id>",
    resource_group_name="ml-rg",
    workspace_name="enterprise-feature-store"
)

# Define customer features
customer_features_spec = FeatureSetSpecification(
    source={
        "type": "parquet",
        "path": "azureml://datastores/feature_data/paths/customer_features/"
    },
    feature_transformation_code={
        "path": "./feature_engineering",
        "transformer_class": "CustomerFeatureTransformer"
    },
    timestamp_column="event_timestamp",
    index_columns=[{"name": "customer_id"}],
    features=[
        {"name": "customer_lifetime_value", "type": "float"},
        {"name": "days_since_last_purchase", "type": "integer"},
        {"name": "average_order_value", "type": "float"},
        {"name": "purchase_frequency", "type": "float"},
        {"name": "customer_segment", "type": "string"}
    ]
)

customer_feature_set = FeatureSet(
    name="customer_features",
    version="1",
    description="Aggregated customer behavior features",
    entities=["customer"],
    stage="Production",
    specification=customer_features_spec,
    tags={"team": "data-science", "domain": "customer-analytics"}
)

# Register feature set
ml_client.feature_sets.begin_create_or_update(customer_feature_set).result()
```

**Feature Engineering Pipeline:**
```python
# feature_engineering/transformer.py
from pyspark.sql import DataFrame
from pyspark.sql.functions import *
from pyspark.sql.window import Window

class CustomerFeatureTransformer:
    """Transform raw data into ML-ready features"""
    
    def transform(self, df: DataFrame) -> DataFrame:
        """Apply feature transformations"""
        
        # Window for customer aggregations
        customer_window = Window.partitionBy("customer_id").orderBy("event_timestamp")
        
        # Calculate features
        features_df = df \
            .withColumn("days_since_last_purchase",
                       datediff(current_date(), max("purchase_date").over(customer_window))) \
            .withColumn("total_spend",
                       sum("order_amount").over(customer_window)) \
            .withColumn("purchase_count",
                       count("order_id").over(customer_window)) \
            .withColumn("average_order_value",
                       col("total_spend") / col("purchase_count")) \
            .withColumn("purchase_frequency",
                       col("purchase_count") / col("days_since_first_purchase")) \
            .withColumn("customer_lifetime_value",
                       self.calculate_clv(col("average_order_value"),
                                         col("purchase_frequency"),
                                         col("days_since_first_purchase"))) \
            .withColumn("customer_segment",
                       when(col("customer_lifetime_value") > 10000, "VIP")
                       .when(col("customer_lifetime_value") > 5000, "High Value")
                       .when(col("customer_lifetime_value") > 1000, "Medium Value")
                       .otherwise("Low Value"))
        
        return features_df
    
    def calculate_clv(self, avg_order_value, frequency, lifetime_days):
        """Calculate Customer Lifetime Value"""
        # Simplified CLV calculation
        return avg_order_value * frequency * (lifetime_days / 365) * 3  # 3 year projection
```

**Materialization and Serving:**
```python
from azure.ai.ml.entities import MaterializationSettings, MaterializationStore

# Configure feature materialization
materialization_settings = MaterializationSettings(
    offline_enabled=True,
    online_enabled=True,
    schedule={
        "type": "recurrence",
        "frequency": "Day",
        "interval": 1,
        "start_time": "2026-01-01T00:00:00"
    },
    resource={
        "instance_type": "Standard_E4s_v3"
    },
    spark_configuration={
        "spark.driver.memory": "8g",
        "spark.executor.memory": "8g",
        "spark.executor.instances": "4"
    }
)

# Update feature set with materialization
customer_feature_set.materialization_settings = materialization_settings
ml_client.feature_sets.begin_create_or_update(customer_feature_set).result()

# Backfill features
from azure.ai.ml.entities import FeatureWindow

backfill_job = ml_client.feature_sets.begin_backfill(
    name="customer_features",
    version="1",
    feature_window=FeatureWindow(
        start_time="2025-01-01T00:00:00",
        end_time="2026-02-24T00:00:00"
    )
).result()
```

**Feature Retrieval for Training:**
```python
from azure.ai.ml.entities import FeatureRetrievalSpec

# Define feature retrieval for training
feature_retrieval_spec = FeatureRetrievalSpec(
    features=[
        {
            "feature_set": "customer_features:1",
            "features": ["customer_lifetime_value", "purchase_frequency", "customer_segment"]
        },
        {
            "feature_set": "transaction_features:1",
            "features": ["avg_transaction_amount", "transaction_velocity"]
        }
    ],
    index_columns=[{"name": "customer_id"}],
    temporal_join_settings={
        "timestamp_column": "event_timestamp",
        "temporal_join_type": "AsOf"
    }
)

# Get training data with features
training_data = ml_client.feature_sets.get_offline_features(
    feature_retrieval_spec=feature_retrieval_spec,
    observation_data="azureml://datastores/training/paths/labels.parquet"
)

# Train model with retrieved features
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

df = training_data.to_pandas_dataframe()
X = df[["customer_lifetime_value", "purchase_frequency", "avg_transaction_amount"]]
y = df["churn_label"]

model = RandomForestClassifier()
model.fit(X, y)
```

**Online Feature Serving for Real-time Inference:**
```python
from azure.ai.ml.entities import OnlineFeatureStore

# Initialize online feature store client
online_store = OnlineFeatureStore(
    ml_client=ml_client,
    feature_store_name="enterprise-feature-store"
)

# Real-time feature lookup
def get_prediction(customer_id: str):
    """Get real-time prediction with fresh features"""
    
    # Retrieve latest features
    features = online_store.get_online_features(
        feature_set_name="customer_features",
        feature_set_version="1",
        index_keys={"customer_id": customer_id},
        feature_names=["customer_lifetime_value", "purchase_frequency", "customer_segment"]
    )
    
    # Make prediction
    feature_vector = [
        features["customer_lifetime_value"],
        features["purchase_frequency"]
    ]
    
    prediction = model.predict([feature_vector])
    
    return {
        "customer_id": customer_id,
        "churn_probability": float(prediction[0]),
        "features_used": features,
        "model_version": "v1.2.3"
    }
```

**Feature Store Governance:**
```python
# Monitor feature drift
from azure.ai.ml.entities import MonitorSchedule, MonitoringTarget

monitor_schedule = MonitorSchedule(
    name="feature-drift-monitor",
    trigger={"type": "recurrence", "frequency": "Day", "interval": 1},
    monitoring_target=MonitoringTarget(
        feature_set="customer_features:1"
    ),
    monitoring_signals={
        "feature_drift": {
            "type": "DataDrift",
            "baseline_dataset": "production_baseline",
            "target_dataset": "latest_features",
            "features": ["customer_lifetime_value", "purchase_frequency"],
            "alert_threshold": 0.3
        }
    },
    alert_notification={
        "emails": ["ml-team@example.com"]
    }
)

ml_client.schedules.begin_create_or_update(monitor_schedule).result()
```

---

##### Q. How do you implement DataOps practices in Azure for continuous data delivery and quality?

**Answer:**
DataOps applies DevOps principles to data analytics, ensuring reliable, high-quality data delivery.

**Core Practices:**
1. Version control for data pipelines
2. Automated testing and validation
3. CI/CD for data workflows
4. Data quality monitoring
5. Observability and lineage

**Implementation:**

```yaml
# azure-data-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - data-pipelines/*
      - schemas/*
      - tests/*

variables:
  - group: data-platform-variables
  - name: databricks_host
    value: https://adb-123456789.azuredatabricks.net

stages:
  - stage: Validate
    jobs:
      - job: ValidateSchemas
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '3.10'
          
          - script: |
              pip install pyspark great-expectations pytest
              pytest tests/schema_tests/ -v
            displayName: 'Validate Data Schemas'
          
          - task: PublishTestResults@2
            inputs:
              testResultsFiles: '**/test-results.xml'
              testRunTitle: 'Schema Validation Tests'

      - job: DataQualityTests
        steps:
          - script: |
              # Run data quality tests on sample data
              python tests/data_quality_tests.py --env dev
            displayName: 'Run Data Quality Tests'

  - stage: DeployDev
    dependsOn: Validate
    condition: succeeded()
    jobs:
      - job: DeployDatabricks
        steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'data-platform-connection'
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                # Install Databricks CLI
                pip install databricks-cli
                
                # Configure Databricks
                echo "[DEFAULT]
                host = $(databricks_host)
                token = $(databricks_token)" > ~/.databrickscfg
                
                # Upload notebooks
                databricks workspace import_dir \
                  ./notebooks /Shared/DataPipelines \
                  --overwrite
                
                # Create/update jobs
                databricks jobs create --json-file jobs/ingestion_job.json || \
                databricks jobs reset --job-id $(job_id) --json-file jobs/ingestion_job.json

      - job: DeployADF
        steps:
          - task: AzureResourceManagerTemplateDeployment@3
            inputs:
              azureSubscription: 'data-platform-connection'
              resourceGroupName: 'data-eng-dev-rg'
              location: 'East US'
              templateLocation: 'Linked artifact'
              csmFile: 'adf/ARMTemplateForFactory.json'
              csmParametersFile: 'adf/ARMTemplateParametersForFactory-dev.json'
              overrideParameters: '-factoryName "data-factory-dev"'

  - stage: IntegrationTests
    dependsOn: DeployDev
    jobs:
      - job: RunEndToEndTests
        steps:
          - script: |
              # Trigger test pipeline run
              python tests/integration_tests.py \
                --factory data-factory-dev \
                --pipeline test-data-pipeline \
                --wait-for-completion
            displayName: 'Run Integration Tests'

  - stage: DeployProd
    dependsOn: IntegrationTests
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: ProductionDeployment
        environment: 'production-data'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureResourceManagerTemplateDeployment@3
                  inputs:
                    azureSubscription: 'data-platform-connection'
                    resourceGroupName: 'data-eng-prod-rg'
                    templateLocation: 'Linked artifact'
                    csmFile: 'adf/ARMTemplateForFactory.json'
                    csmParametersFile: 'adf/ARMTemplateParametersForFactory-prod.json'
```

**Data Quality Test Framework:**
```python
# tests/data_quality_tests.py
import pytest
from pyspark.sql import SparkSession
from great_expectations.dataset import SparkDFDataset
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataQualityTests:
    """Automated data quality testing"""
    
    def __init__(self, spark: SparkSession):
        self.spark = spark
    
    @pytest.fixture
    def sample_data(self):
        """Load sample data for testing"""
        return self.spark.read.parquet("abfss://test@storage.dfs.core.windows.net/sample/")
    
    def test_schema_compliance(self, sample_data):
        """Verify data matches expected schema"""
        expected_schema = {
            "customer_id": "string",
            "transaction_date": "timestamp",
            "amount": "decimal(18,2)",
            "status": "string"
        }
        
        actual_schema = {field.name: str(field.dataType) for field in sample_data.schema.fields}
        
        for column, expected_type in expected_schema.items():
            assert column in actual_schema, f"Missing column: {column}"
            assert expected_type in actual_schema[column], \
                f"Column {column} has wrong type: {actual_schema[column]}"
    
    def test_data_freshness(self, sample_data):
        """Ensure data is fresh (< 24 hours old)"""
        from pyspark.sql.functions import max, current_timestamp, col
        from datetime import timedelta
        
        max_timestamp = sample_data.select(max("transaction_date")).collect()[0][0]
        age_hours = (datetime.now() - max_timestamp).total_seconds() / 3600
        
        assert age_hours < 24, f"Data is stale: {age_hours} hours old"
    
    def test_completeness(self, sample_data):
        """Check for NULL values in critical columns"""
        ge_df = SparkDFDataset(sample_data)
        
        critical_columns = ["customer_id", "transaction_date", "amount"]
        
        for column in critical_columns:
            result = ge_df.expect_column_values_to_not_be_null(column)
            assert result["success"], \
                f"Column {column} has {result['unexpected_count']} NULL values"
    
    def test_referential_integrity(self, sample_data):
        """Verify foreign key relationships"""
        customers = self.spark.read.table("dim_customers")
        
        # All customer_ids should exist in dimension table
        invalid_customers = sample_data \
            .join(customers, "customer_id", "left_anti") \
            .count()
        
        assert invalid_customers == 0, \
            f"Found {invalid_customers} records with invalid customer_id"
    
    def test_business_rules(self, sample_data):
        """Validate business logic constraints"""
        ge_df = SparkDFDataset(sample_data)
        
        # Amount should be positive
        result = ge_df.expect_column_values_to_be_between("amount", min_value=0)
        assert result["success"], "Found negative transaction amounts"
        
        # Status should be valid enum
        valid_statuses = ["COMPLETED", "PENDING", "FAILED", "REFUNDED"]
        result = ge_df.expect_column_values_to_be_in_set("status", valid_statuses)
        assert result["success"], "Found invalid status values"
    
    def test_data_distribution(self, sample_data):
        """Check for anomalies in data distribution"""
        from pyspark.sql.functions import mean, stddev
        
        stats = sample_data.select(
            mean("amount").alias("mean_amount"),
            stddev("amount").alias("stddev_amount")
        ).collect()[0]
        
        # Check if mean is within expected range (business KPI)
        assert 50 <= stats.mean_amount <= 500, \
            f"Average transaction amount {stats.mean_amount} is out of normal range"
    
    def test_duplicate_detection(self, sample_data):
        """Detect duplicate records"""
        total_count = sample_data.count()
        distinct_count = sample_data.select("customer_id", "transaction_date").distinct().count()
        
        duplicate_rate = (total_count - distinct_count) / total_count
        
        assert duplicate_rate < 0.01, \
            f"Duplicate rate {duplicate_rate:.2%} exceeds threshold"

# Run tests
if __name__ == "__main__":
    spark = SparkSession.builder.appName("DataQualityTests").getOrCreate()
    
    tester = DataQualityTests(spark)
    pytest.main([__file__, "-v", "--tb=short"])
```

**Data Observability with Monte Carlo or custom solution:**
```python
# data_observability.py
from azure.monitor.query import LogsQueryClient, MetricsQueryClient
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta
import pandas as pd

class DataObservability:
    """Monitor data pipeline health and quality"""
    
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.logs_client = LogsQueryClient(self.credential)
        self.metrics_client = MetricsQueryClient(self.credential)
    
    def detect_volume_anomalies(self, table_name: str):
        """Detect unexpected changes in data volume"""
        query = f"""
        {table_name}
        | where TimeGenerated > ago(7d)
        | summarize RecordCount=count() by bin(TimeGenerated, 1h)
        | extend AvgCount = avg(RecordCount)
        | extend StdDev = stdev(RecordCount)
        | extend IsAnomaly = abs(RecordCount - AvgCount) > (2 * StdDev)
        | where IsAnomaly == true
        """
        
        response = self.logs_client.query_workspace(workspace_id, query, timespan=timedelta(days=7))
        anomalies = pd.DataFrame(response.tables[0].rows)
        
        if not anomalies.empty:
            self.alert_team(f"Volume anomaly detected in {table_name}", anomalies)
    
    def monitor_freshness(self, table_name: str, max_age_hours: int = 2):
        """Alert if data becomes stale"""
        query = f"""
        {table_name}
        | summarize MaxTimestamp=max(TimeGenerated)
        | extend AgeHours = datetime_diff('hour', now(), MaxTimestamp)
        | where AgeHours > {max_age_hours}
        """
        
        response = self.logs_client.query_workspace(workspace_id, query, timespan=timedelta(days=1))
        
        if response.tables[0].rows:
            age_hours = response.tables[0].rows[0][1]
            self.alert_team(f"{table_name} is stale: {age_hours} hours old")
    
    def track_schema_changes(self, table_name: str):
        """Detect schema drift"""
        current_schema = self.get_current_schema(table_name)
        expected_schema = self.load_schema_from_registry(table_name)
        
        added_columns = set(current_schema.keys()) - set(expected_schema.keys())
        removed_columns = set(expected_schema.keys()) - set(current_schema.keys())
        type_changes = {
            col: (expected_schema[col], current_schema[col])
            for col in set(current_schema.keys()) & set(expected_schema.keys())
            if current_schema[col] != expected_schema[col]
        }
        
        if added_columns or removed_columns or type_changes:
            self.alert_team("Schema drift detected", {
                "added": list(added_columns),
                "removed": list(removed_columns),
                "changed": type_changes
            })
    
    def monitor_pipeline_sla(self, pipeline_name: str, sla_minutes: int = 60):
        """Track pipeline execution time against SLA"""
        query = f"""
        AzureActivity
        | where OperationName == "Microsoft.DataFactory/factories/pipelines/write"
        | where Properties contains "{pipeline_name}"
        | summarize 
            StartTime=min(TimeGenerated),
            EndTime=max(TimeGenerated)
            by CorrelationId
        | extend DurationMinutes = datetime_diff('minute', EndTime, StartTime)
        | where DurationMinutes > {sla_minutes}
        """
        
        response = self.logs_client.query_workspace(workspace_id, query, timespan=timedelta(days=1))
        
        for row in response.tables[0].rows:
            duration = row[3]
            self.alert_team(f"Pipeline {pipeline_name} exceeded SLA: {duration} minutes")
```

---

##### Q. How do you implement secure multi-tenant data isolation in Azure Synapse Analytics?

**Answer:**
Multi-tenant data isolation ensures customers' data remains segregated with strong security boundaries.

**Architecture Patterns:**

**1. Database-per-Tenant (Highest Isolation):**
```sql
-- Create dedicated SQL pools per tenant
CREATE DATABASE [Tenant_TenantA]
WITH (SERVICE_OBJECTIVE = 'DW100c');

CREATE DATABASE [Tenant_TenantB]
WITH (SERVICE_OBJECTIVE = 'DW100c');

-- Tenant-specific schemas
USE [Tenant_TenantA];

CREATE SCHEMA Sales AUTHORIZATION dbo;
CREATE SCHEMA Analytics AUTHORIZATION dbo;

-- Grant access only to tenant users
CREATE USER [TenantA_user] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [TenantA_user];
```

**2. Schema-per-Tenant (Moderate Isolation):**
```sql
-- Shared database with tenant schemas
CREATE SCHEMA [Tenant_TenantA] AUTHORIZATION dbo;
CREATE SCHEMA [Tenant_TenantB] AUTHORIZATION dbo;

-- Create tables in tenant schemas
CREATE TABLE [Tenant_TenantA].Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATETIME2 NOT NULL,
    TenantID VARCHAR(50) NOT NULL DEFAULT 'TenantA'
);

-- Row-level security for additional protection
CREATE FUNCTION [Tenant_TenantA].fn_tenantAccessPredicate(@TenantID VARCHAR(50))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS accessResult
WHERE @TenantID = CAST(SESSION_CONTEXT(N'TenantID') AS VARCHAR(50));

CREATE SECURITY POLICY TenantPolicy
ADD FILTER PREDICATE [Tenant_TenantA].fn_tenantAccessPredicate(TenantID) 
ON [Tenant_TenantA].Orders
WITH (STATE = ON);
```

**3. Row-Level Security (RLS) Pattern:**
```sql
-- Shared tables with tenant identifier
CREATE TABLE dbo.Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATETIME2 NOT NULL,
    TenantID VARCHAR(50) NOT NULL,
    INDEX IX_TenantID NONCLUSTERED (TenantID)
) WITH (DISTRIBUTION = HASH(OrderID));

-- Create security function
CREATE FUNCTION dbo.fn_SecurityPredicate(@TenantID VARCHAR(50))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS fn_SecurityPredicate_result
WHERE 
    @TenantID = CAST(SESSION_CONTEXT(N'TenantID') AS VARCHAR(50))
    OR IS_MEMBER('db_owner') = 1;  -- Admins can see all

-- Apply security policy
CREATE SECURITY POLICY dbo.TenantSecurityPolicy
ADD FILTER PREDICATE dbo.fn_SecurityPredicate(TenantID) ON dbo.Orders,
ADD BLOCK PREDICATE dbo.fn_SecurityPredicate(TenantID) ON dbo.Orders AFTER INSERT,
ADD BLOCK PREDICATE dbo.fn_SecurityPredicate(TenantID) ON dbo.Orders AFTER UPDATE
WITH (STATE = ON);

-- Application sets tenant context
EXEC sp_set_session_context @key = N'TenantID', @value = 'TenantA', @read_only = 1;
```

**Implement with Azure AD and Managed Identities:**
```python
# Python application with tenant isolation
from azure.identity import DefaultAzureCredential
from azure.synapse.spark import SparkClient
import pyodbc

class MultiTenantDataAccess:
    """Secure multi-tenant data access layer"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.credential = DefaultAzureCredential()
        
    def get_connection(self):
        """Get database connection with tenant context"""
        # Get access token for Azure SQL
        token = self.credential.get_token("https://database.windows.net/.default")
        
        connection_string = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=synapse-workspace.sql.azuresynapse.net;"
            "Database=TenantDatabase;"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        
        conn = pyodbc.connect(
            connection_string,
            attrs_before={
                SQL_COPT_SS_ACCESS_TOKEN: token.token.encode('utf-16-le')
            }
        )
        
        # Set tenant context for RLS
        cursor = conn.cursor()
        cursor.execute(
            "EXEC sp_set_session_context @key=N'TenantID', @value=?, @read_only=1",
            (self.tenant_id,)
        )
        cursor.commit()
        
        return conn
    
    def query_tenant_data(self, query: str):
        """Execute query with automatic tenant filtering"""
        conn = self.get_connection()
        
        try:
            df = pd.read_sql(query, conn)
            
            # Verify all returned data belongs to tenant
            if 'TenantID' in df.columns:
                assert (df['TenantID'] == self.tenant_id).all(), \
                    "Data leak detected: returned data from other tenants!"
            
            return df
        finally:
            conn.close()

# Usage
tenant_accessor = MultiTenantDataAccess(tenant_id="TenantA")
orders = tenant_accessor.query_tenant_data("SELECT * FROM dbo.Orders WHERE OrderDate > '2026-01-01'")
```

**Encryption and Key Management:**
```bash
# Separate encryption keys per tenant using Key Vault
az keyvault create \
  --name tenant-TenantA-kv \
  --resource-group multi-tenant-rg \
  --location eastus \
  --enable-purge-protection true

# Create tenant-specific key
az keyvault key create \
  --vault-name tenant-TenantA-kv \
  --name tenant-encryption-key \
  --protection hsm \
  --size 4096

# Enable transparent data encryption with CMK
az sql db tde set \
  --resource-group multi-tenant-rg \
  --server synapse-server \
  --database Tenant_TenantA \
  --status Enabled \
  --encryption-protector ServerManagedKey

az sql db tde key set \
  --resource-group multi-tenant-rg \
  --server synapse-server \
  --database Tenant_TenantA \
  --kid https://tenant-TenantA-kv.vault.azure.net/keys/tenant-encryption-key
```

**Audit and Compliance:**
```sql
-- Enable auditing per tenant
CREATE DATABASE AUDIT SPECIFICATION [Tenant_TenantA_Audit]
FOR SERVER AUDIT [SynapseAudit]
ADD (SELECT ON DATABASE::Tenant_TenantA BY public),
ADD (INSERT ON DATABASE::Tenant_TenantA BY public),
ADD (UPDATE ON DATABASE::Tenant_TenantA BY public),
ADD (DELETE ON DATABASE::Tenant_TenantA BY public)
WITH (STATE = ON);

-- Query audit logs for tenant
SELECT 
    event_time,
    statement,
    server_principal_name,
    database_name,
    schema_name,
    object_name,
    client_ip
FROM sys.fn_get_audit_file('https://auditlogs.blob.core.windows.net/sqldbauditlogs/*/*', default, default)
WHERE database_name = 'Tenant_TenantA'
    AND event_time > DATEADD(day, -7, GETUTCDATE())
ORDER BY event_time DESC;
```

---

##### Q. How do you implement Continuous Training (CT) for ML models in Azure with automated drift detection?

**Answer:**
Continuous Training automatically retrains models when data drift or performance degradation is detected.

**Architecture:**

```python
# Automated CT Pipeline
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Job, Model
from azureml.core import Workspace, Experiment, Run
from azureml.datadrift import DataDriftDetector
from azure.identity import DefaultAzureCredential
import mlflow

class ContinuousTrainingPipeline:
    """Automated continuous training with drift detection"""
    
    def __init__(self, workspace_name: str, resource_group: str):
        self.credential = DefaultAzureCredential()
        self.ml_client = MLClient(
            self.credential,
            subscription_id="<sub-id>",
            resource_group_name=resource_group,
            workspace_name=workspace_name
        )
        self.ws = Workspace.get(name=workspace_name, subscription_id="<sub-id>", resource_group=resource_group)
        
    def setup_drift_detection(self):
        """Configure data drift monitoring"""
        from azureml.datadrift import DataDriftDetector, AlertConfiguration
        
        # Create drift detector
        drift_detector = DataDriftDetector.create_from_datasets(
            workspace=self.ws,
            name="customer-churn-drift",
            baseline_dataset_name="training_baseline_v1",
            target_dataset_name="production_inference_data",
            compute_target_name="cpu-cluster",
            frequency="Week",
            feature_list=["age", "tenure", "monthly_charges", "total_charges"],
            drift_threshold=0.3,
            latency=24,  # Hours
            alert_config=AlertConfiguration(
                ['ml-team@example.com'],
                use_kusto_analytics=True
            )
        )
        
        # Enable drift detection
        drift_detector.enable_schedule()
        drift_detector.run(
            start_time=datetime(2026, 1, 1),
            end_time=datetime(2026, 2, 24)
        )
        
        return drift_detector
    
    def setup_model_monitoring(self, model_name: str, endpoint_name: str):
        """Monitor model performance in production"""
        from azure.ai.ml.entities import (
            MonitorSchedule,
            MonitoringTarget,
            MonitorDefinition
        )
        
        # Model quality monitoring
        monitor = MonitorSchedule(
            name="model-performance-monitor",
            trigger={"type": "recurrence", "frequency": "Day", "interval": 1},
            create_monitor=MonitorDefinition(
                compute={"instance_type": "Standard_DS3_v2"},
                monitoring_target=MonitoringTarget(
                    endpoint_deployment_id=f"azureml:{endpoint_name}:blue"
                ),
                monitoring_signals={
                    "data_drift": {
                        "type": "DataDrift",
                        "baseline_dataset": "training_baseline_v1",
                        "target_dataset": "${{monitoring_input_data.production_data}}",
                        "features": ["age", "tenure", "monthly_charges"],
                        "alert_threshold": 0.3
                    },
                    "prediction_drift": {
                        "type": "PredictionDrift",
                        "production_data": "${{monitoring_input_data.production_data}}",
                        "signal_type": "regression",
                        "alert_threshold": 0.25
                    },
                    "model_performance": {
                        "type": "ModelPerformance",
                        "production_data": "${{monitoring_input_data.production_data}}",
                        "ground_truth_data": "${{monitoring_input_data.ground_truth}}",
                        "metrics": ["accuracy", "precision", "recall", "f1_score"],
                        "alert_enabled": True,
                        "alert_threshold": 0.85  # Alert if accuracy < 85%
                    }
                },
                alert_notification={"emails": ["ml-team@example.com"]}
            )
        )
        
        created_monitor = self.ml_client.schedules.begin_create_or_update(monitor).result()
        return created_monitor
    
    def trigger_retraining(self, drift_score: float, performance_metrics: dict):
        """Decide if retraining is needed"""
        needs_retraining = (
            drift_score > 0.3 or  # Significant drift
            performance_metrics.get('accuracy', 1.0) < 0.85 or  # Performance degraded
            performance_metrics.get('f1_score', 1.0) < 0.80
        )
        
        if needs_retraining:
            print(f"Triggering retraining: drift={drift_score}, accuracy={performance_metrics.get('accuracy')}")
            self.run_training_pipeline()
        else:
            print("Model performance acceptable, no retraining needed")
    
    def run_training_pipeline(self):
        """Execute automated training pipeline"""
        from azure.ai.ml import command, Input, Output
        
        # Get latest production data
        latest_data = self.get_latest_production_data()
        
        # Define training job
        training_job = command(
            code="./src",
            command="""
            python train.py \
                --data ${{inputs.training_data}} \
                --model-output ${{outputs.model_output}} \
                --register-model true \
                --experiment-name ${{inputs.experiment_name}}
            """,
            inputs={
                "training_data": Input(type="uri_folder", path=latest_data),
                "experiment_name": "continuous-training-automated"
            },
            outputs={
                "model_output": Output(type="mlflow_model", mode="rw_mount")
            },
            environment="azureml:sklearn-training-env:1",
            compute="gpu-cluster",
            experiment_name="continuous-training",
            display_name=f"automated-retrain-{datetime.now().strftime('%Y%m%d-%H%M')}"
        )
        
        # Submit and wait
        returned_job = self.ml_client.jobs.create_or_update(training_job)
        self.ml_client.jobs.stream(returned_job.name)
        
        # If successful, deploy new model
        job_status = self.ml_client.jobs.get(returned_job.name).status
        
        if job_status == "Completed":
            self.deploy_new_model_version(returned_job.name)
    
    def deploy_new_model_version(self, job_name: str):
        """Deploy newly trained model with blue-green strategy"""
        from azure.ai.ml.entities import ManagedOnlineDeployment
        
        # Register new model version
        model_uri = f"azureml://jobs/{job_name}/outputs/model_output"
        
        new_model = Model(
            name="churn-predictor",
            path=model_uri,
            description=f"Automated retrained model from job {job_name}",
            tags={"training_type": "continuous", "job_id": job_name}
        )
        
        registered_model = self.ml_client.models.create_or_update(new_model)
        
        # Deploy to green slot
        green_deployment = ManagedOnlineDeployment(
            name="green",
            endpoint_name="churn-prediction-endpoint",
            model=registered_model.id,
            instance_type="Standard_DS3_v2",
            instance_count=1,
            environment_variables={
                "MODEL_VERSION": registered_model.version,
                "DEPLOYMENT_DATE": datetime.now().isoformat()
            }
        )
        
        self.ml_client.online_deployments.begin_create_or_update(green_deployment).result()
        
        # Run validation tests
        if self.validate_deployment("green"):
            # Gradually shift traffic
            self.gradual_traffic_shift("churn-prediction-endpoint", "green")
        else:
            print("Deployment validation failed, rolling back")
            self.ml_client.online_deployments.delete("churn-prediction-endpoint", "green")
    
    def gradual_traffic_shift(self, endpoint_name: str, new_deployment: str):
        """Gradually shift traffic to new deployment"""
        from azure.ai.ml.entities import ManagedOnlineEndpoint
        import time
        
        traffic_steps = [10, 25, 50, 75, 100]
        
        for traffic_percent in traffic_steps:
            print(f"Shifting {traffic_percent}% traffic to {new_deployment}")
            
            endpoint = self.ml_client.online_endpoints.get(endpoint_name)
            endpoint.traffic = {
                "blue": 100 - traffic_percent,
                new_deployment: traffic_percent
            }
            
            self.ml_client.online_endpoints.begin_create_or_update(endpoint).result()
            
            # Monitor for 30 minutes at each step
            time.sleep(1800)
            
            metrics = self.get_deployment_metrics(endpoint_name, new_deployment)
            
            if metrics['error_rate'] > 0.05 or metrics['latency_p95'] > 1000:
                print("Performance degradation detected, rolling back")
                self.rollback_traffic(endpoint_name)
                return
        
        print("Traffic shift completed successfully")
        
        # Remove old deployment
        self.ml_client.online_deployments.delete(endpoint_name, "blue")
```

**Azure DevOps Pipeline for CT:**
```yaml
# continuous-training-pipeline.yml
schedules:
  - cron: "0 2 * * 0"  # Weekly on Sunday 2 AM
    displayName: Weekly Model Retraining Check
    branches:
      include:
        - main

trigger: none

variables:
  - group: ml-prod-variables

stages:
  - stage: DriftDetection
    jobs:
      - job: CheckDrift
        steps:
          - task: AzureCLI@2
            name: DriftCheck
            inputs:
              azureSubscription: 'ml-service-connection'
              scriptType: 'python'
              scriptLocation: 'inlineScript'
              inlineScript: |
                from azureml.datadrift import DataDriftDetector
                from azureml.core import Workspace
                
                ws = Workspace.get(name="ml-workspace-prod")
                drift_detector = DataDriftDetector.get_by_name(ws, "customer-churn-drift")
                
                drift_result = drift_detector.get_output(end_time=datetime.utcnow())
                drift_coefficient = drift_result.drift_coefficient
                
                print(f"##vso[task.setvariable variable=driftScore;isOutput=true]{drift_coefficient}")
                
                if drift_coefficient > 0.3:
                    print("##vso[task.setvariable variable=needsRetraining;isOutput=true]true")
                else:
                    print("##vso[task.setvariable variable=needsRetraining;isOutput=true]false")

  - stage: ModelRetraining
    dependsOn: DriftDetection
    condition: eq(stageDependencies.DriftDetection.CheckDrift.outputs['DriftCheck.needsRetraining'], 'true')
    jobs:
      - job: RetrainModel
        steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'ml-service-connection'
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                az extension add -n ml
                
                # Submit training job
                run_id=$(az ml job create --file training-job.yml --query name -o tsv)
                
                # Wait for completion
                az ml job stream --name $run_id
                
                echo "##vso[task.setvariable variable=trainingRunId;isOutput=true]$run_id"
            name: Training

  - stage: ModelValidation
    dependsOn: ModelRetraining
    jobs:
      - job: ValidateModel
        steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'ml-service-connection'
              scriptType: 'python'
              scriptLocation: 'scriptPath'
              scriptPath: 'tests/validate_model.py'
              arguments: '--run-id $(trainingRunId)'

  - stage: DeployModel
    dependsOn: ModelValidation
    condition: succeeded()
    jobs:
      - deployment: BlueGreenDeployment
        environment: 'production-ml'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureCLI@2
                  inputs:
                    azureSubscription: 'ml-service-connection'
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      # Deploy to green slot
                      az ml online-deployment create \
                        --name green \
                        --endpoint churn-prediction-endpoint \
                        --file deployment-green.yml
                      
                      # Gradual traffic shift
                      python scripts/gradual_rollout.py \
                        --endpoint churn-prediction-endpoint \
                        --new-deployment green \
                        --steps 10,25,50,100 \
                        --wait-minutes 30
```

---

##### Q. How do you implement cost optimization and FinOps practices for Azure data platforms?

**Answer:**
FinOps ensures cloud costs are optimized while maintaining performance and reliability.

**Cost Monitoring and Attribution:**

```bash
# Enable Azure Cost Management
az consumption budget create \
  --resource-group data-platform-rg \
  --budget-name monthly-data-budget \
  --amount 50000 \
  --time-grain Monthly \
  --start-date 2026-01-01 \
  --end-date 2026-12-31 \
  --notifications '[
    {
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 80,
      "contactEmails": ["finops@example.com"],
      "contactRoles": ["Owner", "Contributor"]
    },
    {
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 100,
      "contactEmails": ["finops@example.com", "cto@example.com"],
      "contactRoles": ["Owner"]
    }
  ]'

# Tag resources for cost attribution
az resource tag \
  --ids /subscriptions/{sub}/resourceGroups/data-platform-rg/providers/Microsoft.Synapse/workspaces/data-synapse \
  --tags CostCenter=DataEngineering Project=CustomerAnalytics Environment=Production

# Create cost allocation views
az consumption usage list \
  --start-date 2026-02-01 \
  --end-date 2026-02-24 \
  --query "[?tags.CostCenter=='DataEngineering'] | [?tags.Environment=='Production']" \
  --output table
```

**Automated Cost Optimization:**

```python
# cost_optimizer.py
from azure.mgmt.synapse import SynapseManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.consumption import ConsumptionManagementClient
import pandas as pd
from datetime import datetime, timedelta

class AzureCostOptimizer:
    """Automated cost optimization for data platform"""
    
    def __init__(self, subscription_id: str):
        self.subscription_id = subscription_id
        self.credential = DefaultAzureCredential()
        self.synapse_client = SynapseManagementClient(self.credential, subscription_id)
        self.adf_client = DataFactoryManagementClient(self.credential, subscription_id)
        self.storage_client = StorageManagementClient(self.credential, subscription_id)
        self.cost_client = ConsumptionManagementClient(self.credential, subscription_id)
    
    def optimize_synapse_pools(self, resource_group: str, workspace_name: str):
        """Auto-pause/scale Synapse SQL pools based on usage"""
        
        # Get all SQL pools
        pools = self.synapse_client.sql_pools.list_by_workspace(resource_group, workspace_name)
        
        for pool in pools:
            # Check usage metrics
            usage_stats = self.get_pool_usage(pool.name)
            
            # Auto-pause if idle
            if usage_stats['idle_hours'] > 2:
                print(f"Pausing idle pool: {pool.name}")
                self.synapse_client.sql_pools.begin_pause(
                    resource_group,
                    workspace_name,
                    pool.name
                ).result()
            
            # Auto-scale down if underutilized
            elif usage_stats['avg_dtu_percent'] < 30:
                current_dw = pool.sku.capacity
                recommended_dw = max(100, current_dw // 2)
                
                print(f"Scaling down {pool.name}: DW{current_dw}c -> DW{recommended_dw}c")
                self.synapse_client.sql_pools.begin_update(
                    resource_group,
                    workspace_name,
                    pool.name,
                    {
                        "sku": {
                            "name": f"DW{recommended_dw}c"
                        }
                    }
                ).result()
    
    def optimize_storage_lifecycle(self, resource_group: str, storage_account: str):
        """Implement intelligent storage tiering"""
        
        # Define lifecycle policy
        lifecycle_policy = {
            "properties": {
                "rules": [
                    {
                        "name": "MoveToArchive",
                        "enabled": True,
                        "type": "Lifecycle",
                        "definition": {
                            "actions": {
                                "baseBlob": {
                                    "tierToCool": {
                                        "daysAfterModificationGreaterThan": 30
                                    },
                                    "tierToArchive": {
                                        "daysAfterModificationGreaterThan": 90
                                    },
                                    "delete": {
                                        "daysAfterModificationGreaterThan": 365
                                    }
                                },
                                "snapshot": {
                                    "delete": {
                                        "daysAfterCreationGreaterThan": 90
                                    }
                                }
                            },
                            "filters": {
                                "blobTypes": ["blockBlob"],
                                "prefixMatch": ["archive/", "backup/"]
                            }
                        }
                    },
                    {
                        "name": "DeleteOldLogs",
                        "enabled": True,
                        "type": "Lifecycle",
                        "definition": {
                            "actions": {
                                "baseBlob": {
                                    "delete": {
                                        "daysAfterModificationGreaterThan": 30
                                    }
                                }
                            },
                            "filters": {
                                "blobTypes": ["blockBlob"],
                                "prefixMatch": ["logs/"]
                            }
                        }
                    }
                ]
            }
        }
        
        self.storage_client.management_policies.create_or_update(
            resource_group,
            storage_account,
            "default",
            lifecycle_policy
        )
    
    def optimize_databricks_autoscaling(self, databricks_workspace: str):
        """Configure intelligent autoscaling for Databricks clusters"""
        
        cluster_config = {
            "autoscale": {
                "min_workers": 2,
                "max_workers": 20
            },
            "autotermination_minutes": 30,
            "enable_elastic_disk": True,
            "spark_conf": {
                "spark.databricks.delta.optimizeWrite.enabled": "true",
                "spark.databricks.delta.autoCompact.enabled": "true"
            },
            "custom_tags": {
                "CostCenter": "DataEngineering",
                "AutoShutdown": "true"
            },
            "instance_pool_id": "spot-instance-pool",  # Use spot instances
            "driver_instance_pool_id": "on-demand-pool"  # Driver on on-demand
        }
        
        return cluster_config
    
    def generate_cost_report(self, days: int = 30):
        """Generate detailed cost analysis"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get usage details
        usage = self.cost_client.usage_details.list(
            scope=f"/subscriptions/{self.subscription_id}",
            filter=f"properties/usageStart ge '{start_date.isoformat()}' and properties/usageEnd le '{end_date.isoformat()}'"
        )
        
        cost_data = []
        for item in usage:
            cost_data.append({
                "date": item.date,
                "resource": item.instance_name,
                "resource_type": item.consumed_service,
                "cost": item.cost,
                "currency": item.billing_currency,
                "tags": item.tags
            })
        
        df = pd.DataFrame(cost_data)
        
        # Analyze by cost center
        cost_by_center = df.groupby(df['tags'].apply(lambda x: x.get('CostCenter', 'Untagged')))['cost'].sum()
        
        # Identify top cost drivers
        top_resources = df.groupby('resource')['cost'].sum().nlargest(10)
        
        # Trend analysis
        daily_cost = df.groupby('date')['cost'].sum()
        
        report = {
            "total_cost": df['cost'].sum(),
            "by_cost_center": cost_by_center.to_dict(),
            "top_10_resources": top_resources.to_dict(),
            "daily_trend": daily_cost.to_dict(),
            "recommendations": self.generate_recommendations(df)
        }
        
        return report
    
    def generate_recommendations(self, cost_df: pd.DataFrame):
        """Generate cost optimization recommendations"""
        recommendations = []
        
        # Check for untagged resources
        untagged = cost_df[cost_df['tags'].apply(lambda x: not x or 'CostCenter' not in x)]
        if not untagged.empty:
            recommendations.append({
                "priority": "High",
                "category": "Governance",
                "issue": f"{len(untagged)} untagged resources",
                "potential_savings": 0,
                "action": "Tag all resources with CostCenter and Project"
            })
        
        # Check for idle resources
        idle_resources = cost_df[
            (cost_df['resource_type'].str.contains('Synapse|SqlDatabase')) &
            (cost_df['tags'].apply(lambda x: x.get('Usage', '') == 'Idle'))
        ]
        if not idle_resources.empty:
            potential_savings = idle_resources['cost'].sum()
            recommendations.append({
                "priority": "High",
                "category": "Compute",
                "issue": f"Idle database resources detected",
                "potential_savings": potential_savings,
                "action": "Pause or delete unused SQL pools and databases"
            })
        
        # Check storage tier optimization
        storage_costs = cost_df[cost_df['resource_type'] == 'Storage']
        if storage_costs['cost'].sum() > 5000:
            recommendations.append({
                "priority": "Medium",
                "category": "Storage",
                "issue": "High storage costs",
                "potential_savings": storage_costs['cost'].sum() * 0.3,  # 30% savings estimate
                "action": "Implement lifecycle policies to tier cold data to Archive"
            })
        
        return recommendations

# Usage
optimizer = AzureCostOptimizer(subscription_id="<sub-id>")

# Run optimizations
optimizer.optimize_synapse_pools("data-platform-rg", "data-synapse")
optimizer.optimize_storage_lifecycle("data-platform-rg", "datastorageacct")

# Generate report
cost_report = optimizer.generate_cost_report(days=30)
print(json.dumps(cost_report, indent=2))
```

**Reserved Instances and Savings Plans:**
```bash
# Purchase reserved capacity for predictable workloads
az reservations reservation-order purchase \
  --reservation-order-id <order-id> \
  --sku-name "Standard_D4s_v3" \
  --location eastus \
  --quantity 10 \
  --term P1Y \
  --billing-scope /subscriptions/<sub-id>

# Azure Synapse reserved capacity
az synapse sql pool update \
  --resource-group data-platform-rg \
  --workspace-name data-synapse \
  --name production-pool \
  --sku-name DW1000c \
  --tags ReservedCapacity=true CommitmentTerm=1Year
```

---

##### Q. How do you implement disaster recovery and business continuity for Azure ML and data platforms?

**Answer:**
DR for ML platforms requires protecting models, data, infrastructure, and ensuring quick recovery.

**Multi-Region Architecture:**

```bash
# Primary region: East US
# Secondary region: West US 2

# Create paired workspaces
az ml workspace create \
  --name ml-workspace-primary \
  --resource-group ml-dr-eastus-rg \
  --location eastus

az ml workspace create \
  --name ml-workspace-secondary \
  --resource-group ml-dr-westus2-rg \
  --location westus2

# Enable geo-redundant storage
az storage account create \
  --name mlstorprimary \
  --resource-group ml-dr-eastus-rg \
  --location eastus \
  --sku Standard_RAGRS \
  --enable-hierarchical-namespace true

# Create Traffic Manager for global load balancing
az network traffic-manager profile create \
  --name ml-inference-global \
  --resource-group ml-dr-rg \
  --routing-method Priority \
  --unique-dns-name ml-inference-global \
  --ttl 30 \
  --protocol HTTPS \
  --port 443 \
  --path /health

# Add endpoints
az network traffic-manager endpoint create \
  --name primary-endpoint \
  --profile-name ml-inference-global \
  --resource-group ml-dr-rg \
  --type azureEndpoints \
  --target-resource-id /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.MachineLearningServices/workspaces/ml-workspace-primary/onlineEndpoints/churn-predictor \
  --priority 1 \
  --endpoint-status Enabled

az network traffic-manager endpoint create \
  --name secondary-endpoint \
  --profile-name ml-inference-global \
  --resource-group ml-dr-rg \
  --type azureEndpoints \
  --target-resource-id /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.MachineLearningServices/workspaces/ml-workspace-secondary/onlineEndpoints/churn-predictor \
  --priority 2 \
  --endpoint-status Enabled
```

**Automated Cross-Region Replication:**

```python
# ml_dr_orchestrator.py
from azure.ai.ml import MLClient
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import json

class MLDisasterRecovery:
    """Orchestrate ML platform disaster recovery"""
    
    def __init__(self):
        self.credential = DefaultAzureCredential()
        
        # Primary workspace
        self.ml_client_primary = MLClient(
            self.credential,
            subscription_id="<sub-id>",
            resource_group_name="ml-dr-eastus-rg",
            workspace_name="ml-workspace-primary"
        )
        
        # Secondary workspace
        self.ml_client_secondary = MLClient(
            self.credential,
            subscription_id="<sub-id>",
            resource_group_name="ml-dr-westus2-rg",
            workspace_name="ml-workspace-secondary"
        )
    
    def replicate_models(self):
        """Replicate all production models to secondary region"""
        
        # Get all production models from primary
        primary_models = self.ml_client_primary.models.list()
        
        for model in primary_models:
            if model.tags.get("environment") == "production":
                print(f"Replicating model: {model.name} v{model.version}")
                
                # Download model from primary
                model_path = self.ml_client_primary.models.download(
                    name=model.name,
                    version=model.version,
                    download_path="./temp_models"
                )
                
                # Upload to secondary
                from azure.ai.ml.entities import Model
                
                secondary_model = Model(
                    name=model.name,
                    version=model.version,
                    path=model_path,
                    description=model.description,
                    tags={**model.tags, "replicated_from": "primary"},
                    properties=model.properties
                )
                
                self.ml_client_secondary.models.create_or_update(secondary_model)
    
    def replicate_endpoints(self):
        """Replicate inference endpoints to secondary region"""
        
        primary_endpoints = self.ml_client_primary.online_endpoints.list()
        
        for endpoint in primary_endpoints:
            if endpoint.tags.get("dr_enabled") == "true":
                print(f"Replicating endpoint: {endpoint.name}")
                
                # Get endpoint config
                deployments = self.ml_client_primary.online_deployments.list(endpoint.name)
                
                # Create endpoint in secondary
                from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment
                
                secondary_endpoint = ManagedOnlineEndpoint(
                    name=endpoint.name,
                    description=endpoint.description,
                    auth_mode=endpoint.auth_mode,
                    tags={**endpoint.tags, "region": "secondary"}
                )
                
                self.ml_client_secondary.online_endpoints.begin_create_or_update(
                    secondary_endpoint
                ).result()
                
                # Replicate deployments
                for deployment in deployments:
                    secondary_deployment = ManagedOnlineDeployment(
                        name=deployment.name,
                        endpoint_name=endpoint.name,
                        model=deployment.model,
                        instance_type=deployment.instance_type,
                        instance_count=deployment.instance_count,
                        environment_variables=deployment.environment_variables
                    )
                    
                    self.ml_client_secondary.online_deployments.begin_create_or_update(
                        secondary_deployment
                    ).result()
    
    def replicate_datasets(self):
        """Replicate datasets and feature stores"""
        
        # Storage account replication (using RAGRS)
        primary_storage = BlobServiceClient(
            account_url="https://mlstorprimary.blob.core.windows.net",
            credential=self.credential
        )
        
        secondary_storage = BlobServiceClient(
            account_url="https://mlstorsecondary.blob.core.windows.net",
            credential=self.credential
        )
        
        # Copy critical datasets
        containers = ["datasets", "feature-store", "model-artifacts"]
        
        for container_name in containers:
            source_container = primary_storage.get_container_client(container_name)
            dest_container = secondary_storage.get_container_client(container_name)
            
            # Ensure destination container exists
            try:
                dest_container.create_container()
            except:
                pass
            
            # Copy blobs
            blobs = source_container.list_blobs()
            for blob in blobs:
                source_blob = source_container.get_blob_client(blob.name)
                dest_blob = dest_container.get_blob_client(blob.name)
                
                # Start async copy
                dest_blob.start_copy_from_url(source_blob.url)
                print(f"Copying {container_name}/{blob.name}")
    
    def test_failover(self):
        """Test disaster recovery failover procedure"""
        
        test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
        
        # Test endpoint availability in secondary
        try:
            endpoints = self.ml_client_secondary.online_endpoints.list()
            test_results["tests"].append({
                "name": "Secondary endpoints available",
                "status": "PASS",
                "endpoint_count": len(list(endpoints))
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "Secondary endpoints available",
                "status": "FAIL",
                "error": str(e)
            })
        
        # Test model inference in secondary
        try:
            # Make test prediction
            response = self.ml_client_secondary.online_endpoints.invoke(
                endpoint_name="churn-predictor",
                request_file="test_data.json"
            )
            test_results["tests"].append({
                "name": "Secondary inference working",
                "status": "PASS",
                "latency_ms": response.elapsed.total_seconds() * 1000
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "Secondary inference working",
                "status": "FAIL",
                "error": str(e)
            })
        
        # Test data availability
        try:
            datasets = self.ml_client_secondary.data.list()
            test_results["tests"].append({
                "name": "Secondary data available",
                "status": "PASS",
                "dataset_count": len(list(datasets))
            })
        except Exception as e:
            test_results["tests"].append({
                "name": "Secondary data available",
                "status": "FAIL",
                "error": str(e)
            })
        
        # Calculate RTO (Recovery Time Objective)
        start_time = datetime.now()
        self.execute_failover(test_mode=True)
        rto_seconds = (datetime.now() - start_time).total_seconds()
        
        test_results["rto_seconds"] = rto_seconds
        test_results["rto_target_met"] = rto_seconds < 900  # 15 minute target
        
        return test_results
    
    def execute_failover(self, test_mode: bool = False):
        """Execute failover to secondary region"""
        
        print("Starting failover procedure...")
        
        # Update Traffic Manager to route to secondary
        from azure.mgmt.trafficmanager import TrafficManagerManagementClient
        
        tm_client = TrafficManagerManagementClient(self.credential, "<sub-id>")
        
        if not test_mode:
            # Disable primary endpoint
            tm_client.endpoints.update(
                resource_group_name="ml-dr-rg",
                profile_name="ml-inference-global",
                endpoint_type="azureEndpoints",
                endpoint_name="primary-endpoint",
                parameters={"endpoint_status": "Disabled"}
            )
            
            print("Primary endpoint disabled, traffic routing to secondary")
        
        # Verify secondary is healthy
        health_check = self.verify_secondary_health()
        
        if health_check["healthy"]:
            print("Failover completed successfully")
            return True
        else:
            print("Secondary health check failed!")
            if not test_mode:
                # Rollback
                self.execute_failback()
            return False
    
    def execute_failback(self):
        """Failback to primary region"""
        from azure.mgmt.trafficmanager import TrafficManagerManagementClient
        
        tm_client = TrafficManagerManagementClient(self.credential, "<sub-id>")
        
        # Re-enable primary endpoint
        tm_client.endpoints.update(
            resource_group_name="ml-dr-rg",
            profile_name="ml-inference-global",
            endpoint_type="azureEndpoints",
            endpoint_name="primary-endpoint",
            parameters={"endpoint_status": "Enabled"}
        )
        
        print("Failback to primary completed")

# Automated DR testing (run monthly)
dr_orchestrator = MLDisasterRecovery()

# Replicate all resources
dr_orchestrator.replicate_models()
dr_orchestrator.replicate_endpoints()
dr_orchestrator.replicate_datasets()

# Test failover
test_results = dr_orchestrator.test_failover()
print(json.dumps(test_results, indent=2))
```

**Backup Strategy:**
```bash
# Automated backup of ML workspace metadata
az ml workspace export \
  --name ml-workspace-primary \
  --resource-group ml-dr-eastus-rg \
  --output-file workspace-backup-$(date +%Y%m%d).json

# Backup pipelines
az ml job list \
  --workspace-name ml-workspace-primary \
  --resource-group ml-dr-eastus-rg \
  --output json > pipelines-backup-$(date +%Y%m%d).json

# Backup compute configurations
az ml compute list \
  --workspace-name ml-workspace-primary \
  --resource-group ml-dr-eastus-rg \
  --output json > compute-backup-$(date +%Y%m%d).json
```

### Intermediate/Advanced Azure DevOps & CI/CD Scenarios

##### Q. How would you architect a secure, auditable CI/CD pipeline in Azure DevOps for multi-environment (Dev/Test/Prod) deployments?
- **Architecture:** Use YAML-based multi-stage pipelines describing the build and deployment phases.
- **Environments:** Leverage Azure DevOps Environments (Dev, Test, Prod) to manage deployments, with approval checks and exclusive locks on production.
- **Security & Secrets:** Store sensitive parameters in Azure Key Vault and integrate using service connections. Do not hardcode secrets in YAML.
- **Service Connections:** Use Workload Identity Federation (OIDC) or strict service principals with least-privilege RBAC.
- **Auditability:** Ensure traceability by linking commits to work items. Keep branch policies active so every PR requires review, build success, and linked issues.

##### Q. Differentiate between classic pipelines and YAML pipelines in Azure DevOps. Which one is better for Infrastructure-as-Code and why?
- **Classic Pipelines:** GUI-based, separated into Build and Release pipelines. Revisions are tracked but not alongside the application/infra code.
- **YAML Pipelines:** Unified pipeline-as-code. Both CI and CD exist in the same artifact. 
- **Better for IaC:** YAML pipelines are superior for IaC. Changes to infrastructure (Terraform, ARM) and the deployment pipeline (YAML) are version-controlled together in the same Git repo. This provides better peer review (PR processes), rollback capabilities, and strict audit trails.

##### Q. What rollback strategies have you implemented in mission-critical environments? Can you detail a real-world example?
- **Strategy:** I prefer "forward fixing" if the issue is minor, or "infrastructure state rollback" if an entire release goes bad.
- **Real-world example:** For an AKS microservice deployment, we utilized Helm. When a deployment failed health checks in production, we triggered a rollback step that ran `helm rollback <release_name> 0` to revert to the previous stable state. For DB migrations, we use a separate job. If backwards-compatibility isn't possible, we retain a snapshot prior to rollout to restore rapidly.

##### Q. Explain the use of Jenkins Shared Libraries or Azure DevOps Templates for enterprise-level DRY (Don't Repeat Yourself) pipelines.
- **Purpose:** They prevent duplication of identical pipeline logic (e.g., security scanning, building Docker images) across hundreds of microservice repositories.
- **Azure DevOps Templates:** You define a core template YAML in a central repository, containing standardized steps (e.g., SonarQube analysis, container build). App repositories reference this template by passing parameters, ensuring that a single update to the template propagates organizations-wide enforcement of standards securely.

##### Q. How do you handle multi-repo CI/CD pipelines when deploying a microservices-based application with interdependencies?
- **Triggering:** Use pipeline triggers where one pipeline completion triggers a downstream pipeline, or use repository resources in YAML (`resources: repositories`) to trigger on branch updates.
- **Artifacts & Versioning:** Publish microservices as immutable artifacts (e.g., Docker tags) to a registry. 
- **Decoupling:** Ideally, microservices should be independently deployable. If strict coordination is needed, a release manifest repository can manage the versions of all microservices, using a GitOps approach (like ArgoCD) to apply the interconnected state.

##### Q. Describe techniques to cache Docker layers or NuGet/NPM packages in pipelines for speed optimization.
- **Docker Caching:** Use the `--cache-from` parameter or buildx caching pointing to an Azure Container Registry (ACR) to reuse unchanged layers.
- **Package Caching:** In Azure DevOps, use the `Cache@2` task. Key the cache against `package-lock.json` or `packages.lock.json`. If the hash matches, it restores from the pipeline's storage, bypassing the registry download phase.

##### Q. How do you integrate Azure Key Vault with DevOps pipelines securely, especially with rotating secrets or certificates?
- Use the **Azure Key Vault Task** in DevOps, authenticated via an Azure Resource Manager (ARM) service connection (preferably with Workload Identity Federation).
- The task fetches the latest values of specified secrets and sets them as masked pipeline variables at runtime. 
- For certificates, fetch them as binary or base64 secrets, decode them during the pipeline, and feed them securely to the target resources (like AKS or App Services) without persisting them to disk.

##### Q. What is the purpose of manual intervention gates, and how would you enforce them before production release?
- **Purpose:** To prevent automated deployments to sensitive environments without explicit sign-off from stakeholders (QA, management, or CAB).
- **Enforcement:** In Azure DevOps, configure an **Environment** for Production. Under the environment limits, add an "Approvals and Checks" gate requiring a specific group to approve. The pipeline execution will pause at the Deployment job targeting this environment until acted upon.

##### Q. Explain how you implement compliance as code (security scanning, code coverage, policy checks) in Azure DevOps pipelines.
- **Static Code Analysis (SAST):** Integrate SonarQube or Checkmarx in the build stage, enforcing quality gates.
- **Dependency Scanning:** Use Mend (WhiteSource) or GitHub Advanced Security.
- **Code Coverage:** Enforce testing tools (like Cobertura/Jacoco) to publish coverage reports, failing the build if it drops below a threshold (e.g., 80%).
- **Infrastructure Policy:** Integrate tools like Checkov or OPA (Open Policy Agent) to scan Terraform code for compliance against internal security baselines.

##### Q. How do you enforce pipeline security – from source control (Git) to deployment? Tools? Policies?
- **Source Control:** Branch policies (min 2 reviewers, successful CI build, no secrets in PR).
- **Security Scanning:** Shift-left security (Trivy, SonarQube, Checkov) inside the CI process.
- **Pipeline Permissions:** Restrict who can create/edit pipelines. Mask all variables mapped from key vaults.
- **Execution Environment:** Run agents in private networks (self-hosted agents or VNET-integrated MS-hosted agents). Use short-lived credentials via Entra ID (Workload Identity) rather than static PATs or secrets for deployment steps.

---



### Advanced Azure DevOps & CI/CD Pipelines

##### Q. How do you design a scalable and secure release pipeline across multiple environments in Azure DevOps?
**Answer:** A scalable and secure release pipeline in Azure DevOps uses **YAML multi-stage pipelines** defining stages like Build, Dev, Test, and Prod.
- **Scalability:** Utilize pipeline templates mapping to shared, common code bases to keep pipelines DRY (Don't Repeat Yourself). Use matrix strategies for large builds. 
- **Security:** Use **Environments** in Azure DevOps with implicit Approval Checks and Gates for production deployments. Store credentials externally in Azure Key Vault and authenticate via Workload Identity Federation instead of static secrets. Require branch policies across source repos prior to deployment.

##### Q. Explain how environment variables differ in variable groups and pipeline variables.
**Answer:**
- **Pipeline Variables:** Defined directly inside the YAML file (`variables` block) or UI for a single pipeline. They are scoped strictly to that pipeline and are committed to version control.
- **Variable Groups:** Stored centrally under "Library" in Azure DevOps. They can be shared securely across *multiple* pipelines. They integrate directly with Azure Key Vault to dynamically fetch secrets at runtime without exposing them to developers.

##### Q. How would you handle blue-green deployments using Azure DevOps?
**Answer:**
Blue-green deployment minimizes downtime by spinning up a new duplicate environment (Green) alongside the old one (Blue). In Azure DevOps:
1. Define a deployment job targeting your Green environment slot (e.g., Azure App Service Staging Slot or AKS Green Namespace).
2. Run automated validation/integration tests against the Green slot using tasks in the pipeline.
3. Once validated, use the `AzureAppServiceManage@0` task to trigger a "Swap" action, seamlessly routing public traffic to Green and demoting Blue.

##### Q. What’s the difference between Service Connections and Service Principals in Azure DevOps?
**Answer:**
- **Service Principal:** An identity created in Microsoft Entra ID (Azure AD) used by applications or tools to access Azure resources.
- **Service Connection:** An Azure DevOps abstraction that *stores and uses* the Service Principal (or Workload Identity/Managed Identity) to securely authenticate the DevOps project to the external Azure environment. Without the Service Connection, Azure DevOps cannot communicate with Azure Subscriptions.

##### Q. How do you integrate Azure Key Vault with your pipelines securely?
**Answer:**
1. Create a Service Connection (preferably using Workload Identity Federation) in Azure DevOps that has `Key Vault Secrets User` RBAC on the Key Vault.
2. Store the non-sensitive configuration in a Variable Group, and toggle "Link secrets from an Azure key vault as variables".
3. Use the `AzureKeyVault@2` task in the YAML pipeline to download secrets dynamically.
4. Azure DevOps automatically masks these secret values (***) in pipeline logs to prevent leakage.

##### Q. Describe the steps to implement Infrastructure as Code using Azure DevOps and Terraform.
**Answer:**
1. Store Terraform code (HCL) in Azure Repos.
2. Create an Azure Storage Account to act as the Terraform remote backend (for `terraform.tfstate`).
3. Set up an Azure DevOps pipeline with stages:
   - **Init:** `terraform init` connecting to the Azure backend using a Service Connection.
   - **Validate & Plan:** `terraform validate` and `terraform plan`, outputting an execution plan as a secure artifact.
   - **Apply:** A deployment job with an explicit manual approval gate. If approved, `terraform apply` executes the saved plan.

##### Q. What are the best practices for handling secrets and credentials in YAML pipelines?
**Answer:**
- **Never Hardcode:** Never put plain-text secrets in YAML or Git.
- **Azure Key Vault:** Centralize secrets using the Key Vault integration.
- **Secure DevOps Library:** Use Variable Groups specifically flagged as "Secret".
- **Short-Lived Credentials:** Use OIDC (Workload Identity Federation) for Service Connections instead of persistent passwords.
- **Masking:** Ensure any manual script outputting a secret explicitly uses the `##vso[task.setvariable secure=true]` logging command.

##### Q. How does approval and gates work in multi-stage pipelines?
**Answer:**
In YAML pipelines, approvals and gates are configured at the **Environment** level (e.g., "Production Environment").
- **Approvals:** When a deployment job targets the Environment, the pipeline automatically pauses and emails designated approvers.
- **Gates:** Automated checks (e.g., querying Azure Monitor alerts, checking SonarQube quality gates, or calling a webhook) that must return a healthy status before the deployment proceeds.

##### Q. Explain how to configure branch policies and protect the main branch in Azure Repos.
**Answer:**
Navigate to Repos > Branches > select `main` > Branch Policies.
- Require a minimum number of reviewers (e.g., 2).
- Require linked work items for traceability.
- **Build Validation:** Enforce that a specific PR validation pipeline must run and succeed (build code, run unit tests, detect lint issues) before the Merge button is enabled.

##### Q. How would you implement a strategy for rollback in case of deployment failure?
**Answer:**
- **Code Rollback:** Revert the PR block in Git and let the CI/CD pipeline roll out the previous stable state (best for Infrastructure/GitOps).
- **Deployment Rollback:** In Azure DevOps pipelines, deploy infrastructure utilizing a deployment strategy like `runOnce` with `on: failure:` hooks that execute scripts to invoke `helm rollback` or swap an App Service back to the previous slot.

##### Q. What are some ways to manage pipeline templates across multiple projects?
**Answer:**
Create a dedicated "Pipeline Templates" repository. Teams across different projects can reference this repository in their own YAML via the `resources: repositories` block. They can then extend the central template using `template: path/to/template.yml@templates` allowing the enterprise to enforce central security, SAST scanning, and standardized container builds globally.

##### Q. Explain the difference between deployment job and job in Azure DevOps YAML pipelines.
**Answer:**
- **`job`:** A standard execution block containing steps (scripts/tasks). It runs on an agent and is typically used for build, test, and package activities.
- **`deployment` job:** A specialized job type explicitly designed for CD. It integrates natively with Azure DevOps **Environments**, tracks deployment history, allows deployment strategies (runOnce, canary, rolling), and honors environment-level approvals and gates.

##### Q. How do you design an audit-compliant CI/CD pipeline in a highly regulated environment?
**Answer:**
- **Source Control:** Strict branch policies, preventing direct pushes to `main`.
- **Traceability:** Force automatic linking of Jira/Azure Boards work items to commits and PRs.
- **Immutability:** Build artifacts once, hash them, and promote the exact same binary across all environments.
- **Gates:** Separate duties by forcing Management/QA approvals in production environments.
- **Logs:** Retain pipeline execution logs and pipeline artifact hashes for auditing. 

##### Q. What is the purpose of the agentless job in Azure Pipelines?
**Answer:**
An Agentless job runs on the Azure DevOps server orchestration engine, not on a dedicated worker agent. It is used exclusively for lightweight operations that invoke external services: hitting REST APIs, pausing for manual intervention, checking Azure Monitor alerts, or communicating with Service Bus queues. It saves agent compute resources and money.

##### Q. How can you trigger a pipeline based on path filters and branches?
**Answer:**
By specifying the `trigger` block in the YAML file at the root:
```yaml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - src/*
    exclude:
      - docs/*
```
This limits CI execution, saving compute costs so documentation changes won't trigger a heavy application build.

##### Q. How do you integrate security scanning tools (like SonarQube, Snyk) into Azure DevOps pipelines?
**Answer:**
You install the respective extensions from the Azure DevOps Marketplace.
- For **SonarQube**, add the `SonarQubePrepare@5`, `SonarQubeAnalyze@5`, and `SonarQubePublish@5` tasks sequentially around your build step. 
- You then add a Build Validation PR policy that looks for the SonarQube Quality Gate status, blocking the PR if vulnerabilities or technical debt exceed enterprise thresholds.

##### Q. What’s the difference between Hosted Agents and Self-hosted Agents? When should each be used?
**Answer:**
- **Microsoft-hosted Agents:** Ephemeral VMs managed completely by Microsoft. They boot up clean, run the pipeline, and get destroyed. Used for 90% of workloads lacking strict network boundary requirements.
- **Self-hosted Agents:** VMs or Containers instantiated and managed by the customer within their own VNet/VPC. Used when builds need access to internal corporate network resources (like an on-premise database, internal NuGet feed, or private endpoints) or when requiring heavy caching / specialized hardware (GPUs).

##### Q. How would you reduce build time in Azure Pipelines for a monorepo?
**Answer:**
- **Path Filtering:** Use PR triggers with path inclusion/exclusion so only modified microservices are built.
- **Caching:** Utilize the `Cache@2` task to cache `.npm`, `node_modules`, `.m2/repository`, or Docker layers, saving heavy download times.
- **Parallelism:** Split unit tests or microservice matrix builds into multiple parallel jobs running concurrently across multiple agents. 

##### Q. Explain how to set up canary deployment using Azure DevOps and Azure Kubernetes Service.
**Answer:**
Canary deployments route a small percentage of traffic to a new version. In Azure DevOps:
1. Use an Environment with a `Deployment` job utilizing the `strategy: canary` block.
2. In the setup, define increments (e.g., 10%, 25%).
3. Use the `KubernetesManifest@0` task. Azure DevOps will automatically generate a `-canary` variant of your deployment and service configurations, utilizing Service Mesh (Istio) or Ingress (NGINX) weighting to securely route the specified percentage of traffic.

##### Q. How do you monitor and troubleshoot pipeline performance and failure trends?
**Answer:**
- **Pipeline Analytics:** Utilize the built-in "Analytics" tab in Azure Pipelines to view pass/fail rates, pipeline duration, and test execution history over 14/30 days.
- **Test Failures:** Track the "Top failing tests" dashboard.
- **Logging:** Enable `system.debug = true` as a variable during a run to generate verbose diagnostic logs for detailed step-by-step troubleshooting.

##### Q. What are deployment groups and how do they differ from environments?
**Answer:**
- **Deployment Groups:** Used primarily in Classic Release pipelines. They represent a logical set of target machines (VMs) that have the Azure Pipelines agent installed natively on them.
- **Environments:** The modern YAML equivalent. Environments track deployments across native Kubernetes, Web Apps, and VMs. They act as logical boundaries defining approvals, security checks, and deployment history traceability.

##### Q. How do you handle CI/CD for microservices architecture in Azure DevOps?
**Answer:**
Unlike monoliths, microservices scale well when decoupled.
- **Pipelines:** 1 code repo = 1 independent CI/CD YAML pipeline.
- **Artifacts:** CI builds output immutable Docker images tagged with the `$(Build.BuildId)` and pushed to ACR.
- **CD:** The CD pipeline uses Helm or Kustomize to update the specific Kubernetes deployment manifest. Use path filters or repository resources to invoke targeted deployments independently, ensuring minimal blast radius.

##### Q. How would you manage shared libraries across multiple pipelines?
**Answer:**
Use YAML Templates. Standardize your organizational logic (like Docker builds, Veracode scans, or Terraform deployments) into modular YAML files stored in a central "DevOps-Templates" repository. Individual pipeline developers then import those steps seamlessly using the `template` keyword, guaranteeing everyone builds identically.

##### Q. How do you implement conditional execution of jobs in a YAML pipeline?
**Answer:**
Use the `condition` property on a job or step. Example: running a specific script only on the `main` branch or only if the previous job failed:
```yaml
jobs:
- job: CleanupJob
  condition: failed()
- job: DeployProd
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
```

##### Q. What are your strategies for minimizing downtime during production deployments?
**Answer:**
- **Decoupled Databases:** Execute non-destructive database schema migrations in advance before deploying application code.
- **Deployment Strategies:** Always use Blue-Green or Rolling Updates in AKS/App Services instead of destructive stops/starts.
- **Health Probes:** Rely on Kubernetes Readiness Probes or App Service Health Checks to prevent the routing of live traffic to instances that haven't fully booted up or connected to dependencies. 



### Complex Scenarios & Architectures

##### Q. CI/CD pipeline takes 40 mins to deploy a small change. What would you do to optimize it?
**Answer:**
1. **Caching:** Implement the `Cache@2` task to cache heavy dependencies (like `node_modules`, `.m2`, or NuGet packages) and Docker layers to bypass downloads.
2. **Parallelism:** Split independent jobs (e.g., Unit Tests, SAST/SonarQube Scanning, Linting) to run concurrently using multiple parallel execution agents.
3. **Path Filtering & Monorepos:** If deploying a microservice, use path triggers so the pipeline only builds the specific microservice folder that changed, rather than rebuilding the entire repository.
4. **Agent Types:** If using Microsoft-hosted agents, consider switching to Self-hosted agents on high-CPU VMs with pre-warmed caches to drastically speed up execution.

##### Q. You’re asked to design a highly available logging system for 100+ microservices across 3 regions. What tools and architecture would you suggest?
**Answer:**
1. **Collection:** Deploy **FluentBit** or **Fluentd** as DaemonSets on all Kubernetes clusters to scrape container `stdout`/`stderr` asynchronously to prevent backpressure.
2. **Buffer/Ingestion:** Route the logs to a regional **Azure Event Hubs** (acting as a Kafka-like high-throughput buffer) to ensure no logs are lost during massive spikes.
3. **Storage/Analytics:** Use **Azure Data Explorer (ADX)** or **Azure Log Analytics** connected to the Event Hubs for blazing-fast indexing and long-term querying.
4. **HA Design:** Event Hubs implicitly provide multi-zone HA. For multi-region DR, configure Event Hubs Geo-Disaster Recovery to pair primary and secondary namespaces.

##### Q. How do you ensure secure and dynamic secret rotation in Azure DevOps pipelines?
**Answer:**
Never store static passwords directly in Azure DevOps Variable Groups if they rotate dynamically.
1. Store all secrets centrally in **Azure Key Vault** and configure auto-rotation policies on the keys/secrets within Azure.
2. Grant the Azure DevOps Service Connection (using Workload Identity) "Key Vault Secrets User" RBAC.
3. Within the YAML pipeline, use the `AzureKeyVault@2` task to fetch the *latest* version of the secret dynamically at runtime. This ensures the pipeline always pulls the correct, newly rotated secret right before execution without developer intervention.

##### Q. Explain how you’d use Azure Application Gateway with Web Application Firewall for a sensitive banking application.
**Answer:**
1. **Deployment:** Deploy Application Gateway v2 across Availability Zones for high availability. 
2. **WAF Tier:** Enable the WAF Tier in **Prevention Mode** using the OWASP ModSecurity Core Rule Set (CRS 3.2+) to actively block SQL injection, XSS, and malicious payloads.
3. **E2E Encryption:** Terminate the SSL certificate at the App Gateway to allow the WAF to inspect the plain-text HTTP payload, and then re-encrypt the traffic using internal certificates before routing it to the backend AKS/App Service pool.
4. **Custom Rules:** Apply Geo-Match custom rules to block traffic attempting to access the banking API from highly sanctioned countries.

##### Q. During an Azure deployment, you receive intermittent DNS resolution issues. What can be the causes?
**Answer:**
1. **Azure DNS Rate Limits:** Azure explicitly limits DNS queries to **1000 queries per second per VM**. If deploying hundreds of microservices that all query DNS simultaneously, the underlying AKS nodes will silently drop DNS packets.
2. **Fix:** Deploy **NodeLocal DNSCache** in Kubernetes. It runs a DNS caching agent on every node, drastically reducing upstream queries to the Azure DNS resolver and preventing rate-limiting.
3. **VNet Peering:** Ensure Virtual Network Links are correctly attached to Private DNS Zones if resolving private endpoints across peered networks.

##### Q. Design a cost-optimized cloud architecture for an internal reporting app that runs every night and stores logs for 3 years.
**Answer:**
Since it only runs at night, paying for 24/7 compute is wasted money.
1. **Compute:** Use **Azure Functions** (Consumption/Serverless plan) or **Azure Container Instances** triggered on an automated CRON schedule. You only pay for the exact compute minutes used during the nightly generation.
2. **Database:** Use **Azure SQL Database Serverless**, which automatically auto-pauses compute scaling down to 0 vCores when inactive, severely cutting costs.
3. **Storage:** Output the generated reports to **Azure Blob Storage**. Implement a **Lifecycle Management Policy** to move data from Hot -> Cool (after 30 days) -> Archive tier (after 90 days), providing the absolute cheapest possible storage for the mandatory 3-year compliance retention.

##### Q. An Azure function is being throttled. How will you detect and fix it?
**Answer:**
1. **Detect:** Monitor Application Insights for HTTP `429 Too Many Requests` status codes and evaluate the "Function Execution Units" metrics.
2. **Concurrency Limits:** If using a Consumption plan, scale-out has hard limits (e.g., 200 instances).
3. **Fix:** 
   - Switch to the **Premium Plan** providing higher maximum scale-out limits and pre-warmed instances to combat cold-start cascades. 
   - If triggered by a queue (Service Bus), adjust the `host.json` `maxConcurrentCalls` and `batchSize` settings to throttle the input ingestion gracefully, smoothing out the processing spikes.

##### Q. Define a plan for blue/green deployment with rollback on Azure using Terraform and pipelines.
**Answer:**
1. **Infra (Terraform):** Provision an Azure App Service with two deployment slots: `Production` and `Staging-Green`.
2. **CI/CD Pipeline:** Build the container/artifact and deploy it strictly to the `Staging-Green` slot.
3. **Validation:** Run automated E2E and integration tests against the isolated Staging slot URL.
4. **Swap:** If tests pass, invoke the `AzureAppServiceManage@0` pipeline task with the Action `Swap Slots`. Azure seamlessly switches the routing rules so Production traffic hits Green.
5. **Rollback:** If telemetry/alerts fire within the post-deployment window, an automated gate or a manual click triggers the Swap task again, instantly reverting traffic back to the original container.

##### Q. Explain the difference in scaling strategies for compute-intensive vs I/O-intensive workloads in Azure.
**Answer:**
- **Compute-Intensive (e.g., ML algorithms, video transcoding):** Scale primarily **Horizontally** (out). Use F-Series VMs (Compute optimized) inside a Virtual Machine Scale Set (VMSS) scaling dynamically based on metrics like CPU percentage or Service Bus queue length.
- **I/O-Intensive (e.g., Elasticsearch, high-throughput Databases):** Scaling out is difficult without heavy manual data sharding. Typically, you must scale **Vertically** (up). You must utilize L-Series VMs (Storage optimized) or attach Premium SSD v2 / Ultra Disks. Azure strictly caps Disk IOPS and Throughput based on the VM size, meaning you often must provision a larger VM *just* to unlock higher disk speed limits.
