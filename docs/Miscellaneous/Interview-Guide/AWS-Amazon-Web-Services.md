## AWS (Amazon Web Services)

### Cloud Computing Platform

##### Q. Advanced AWS resources worked with?

**1. Amazon Aurora:**
- Fully managed MySQL/PostgreSQL-compatible database
- High performance and availability
- Used for production databases with read replicas
- Automated backups and point-in-time recovery

**2. AWS Lambda:**
- Serverless compute service
- Event-driven architectures
- S3 uploads, API Gateway, CloudWatch Events
- Automated workflows

**3. Amazon ECS with Fargate:**
- Container orchestration without infrastructure management
- Serverless container engine
- Simplified scaling

**4. Amazon EKS:**
- Managed Kubernetes service
- Automatic scaling, rolling updates
- Integration with AWS services (IAM, VPC)

**5. AWS Step Functions:**
- Visual workflow coordination
- Orchestrates microservices
- Integrates Lambda and AWS services

**6. Amazon CloudFront:**
- Content delivery network (CDN)
- Low latency, high transfer speeds
- Edge location caching

**7. AWS CodePipeline:**
- CI/CD automation
- Integrates CodeBuild, CodeDeploy, GitHub
- Streamlined software delivery

**8. AWS Security Hub:**
- Comprehensive security state view
- Aggregates findings across AWS accounts
- Improves security posture

##### Q. Deploying AI/ML modules in AWS?

**Deployment:**
- AWS SageMaker for ML models
- Lambda with SageMaker for serverless
- Pre-built services (Rekognition, Comprehend, Lex)

**Customization:**
- SageMaker training on custom data
- Hyperparameter tuning
- Custom Docker containers
- Fine-tuning pre-built services

**Scaling:**
- Auto-scaling SageMaker endpoints
- Lambda automatic scaling
- API Gateway scaling
- ELB for load balancing

**DevOps Practices:**
- IaC with CloudFormation/Terraform
- CI/CD with CodePipeline
- CloudWatch monitoring
- X-Ray tracing

---

### MLOps, AIOps, Data Engineering & Security

##### Q. How do you implement an end-to-end MLOps pipeline in AWS with SageMaker Pipelines and automated model retraining?

**Answer:**
AWS provides a comprehensive MLOps stack using SageMaker, CodePipeline, and Step Functions for complete ML lifecycle automation.

**Architecture Components:**
1. **SageMaker Pipelines** - ML workflow orchestration
2. **SageMaker Model Registry** - Model versioning and approval
3. **SageMaker Feature Store** - Centralized feature management
4. **CodePipeline/CodeBuild** - CI/CD automation
5. **EventBridge** - Event-driven automation
6. **Lambda** - Serverless orchestration

**SageMaker Pipeline Definition:**

```python
# mlops_pipeline.py
import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep, CreateModelStep
from sagemaker.workflow.step_collections import RegisterModel
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.functions import JsonGet
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
from sagemaker.model_metrics import MetricsSource, ModelMetrics
from sagemaker.drift_check_baselines import DriftCheckBaselines
import boto3

class MLOpsPipeline:
    """Production-grade MLOps pipeline with automated retraining"""
    
    def __init__(self, role_arn: str, bucket: str, region: str = 'us-east-1'):
        self.role = role_arn
        self.bucket = bucket
        self.region = region
        self.sagemaker_session = sagemaker.Session()
        self.sm_client = boto3.client('sagemaker', region_name=region)
        
    def create_pipeline(self):
        """Create SageMaker Pipeline for end-to-end ML workflow"""
        
        # 1. Data Quality Check and Preprocessing
        sklearn_processor = SKLearnProcessor(
            framework_version='1.2-1',
            role=self.role,
            instance_type='ml.m5.xlarge',
            instance_count=1,
            base_job_name='data-preprocessing'
        )
        
        preprocessing_step = ProcessingStep(
            name='DataPreprocessing',
            processor=sklearn_processor,
            code='preprocessing.py',
            inputs=[
                sagemaker.processing.ProcessingInput(
                    source=f's3://{self.bucket}/raw-data/',
                    destination='/opt/ml/processing/input'
                )
            ],
            outputs=[
                sagemaker.processing.ProcessingOutput(
                    output_name='train',
                    source='/opt/ml/processing/train',
                    destination=f's3://{self.bucket}/processed/train'
                ),
                sagemaker.processing.ProcessingOutput(
                    output_name='validation',
                    source='/opt/ml/processing/validation',
                    destination=f's3://{self.bucket}/processed/validation'
                ),
                sagemaker.processing.ProcessingOutput(
                    output_name='test',
                    source='/opt/ml/processing/test',
                    destination=f's3://{self.bucket}/processed/test'
                ),
                sagemaker.processing.ProcessingOutput(
                    output_name='baseline',
                    source='/opt/ml/processing/baseline',
                    destination=f's3://{self.bucket}/baseline'
                )
            ],
            job_arguments=['--quality-threshold', '0.95']
        )
        
        # 2. Model Training
        xgboost_estimator = Estimator(
            image_uri=sagemaker.image_uris.retrieve('xgboost', self.region, version='1.5-1'),
            role=self.role,
            instance_type='ml.m5.2xlarge',
            instance_count=1,
            output_path=f's3://{self.bucket}/models',
            base_job_name='churn-prediction-training',
            enable_sagemaker_metrics=True,
            hyperparameters={
                'objective': 'binary:logistic',
                'num_round': 100,
                'max_depth': 5,
                'eta': 0.2,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            }
        )
        
        training_step = TrainingStep(
            name='TrainModel',
            estimator=xgboost_estimator,
            inputs={
                'train': TrainingInput(
                    s3_data=preprocessing_step.properties.ProcessingOutputConfig.Outputs['train'].S3Output.S3Uri,
                    content_type='text/csv'
                ),
                'validation': TrainingInput(
                    s3_data=preprocessing_step.properties.ProcessingOutputConfig.Outputs['validation'].S3Output.S3Uri,
                    content_type='text/csv'
                )
            }
        )
        
        # 3. Model Evaluation
        evaluation_processor = SKLearnProcessor(
            framework_version='1.2-1',
            role=self.role,
            instance_type='ml.m5.xlarge',
            instance_count=1,
            base_job_name='model-evaluation'
        )
        
        evaluation_step = ProcessingStep(
            name='EvaluateModel',
            processor=evaluation_processor,
            code='evaluation.py',
            inputs=[
                sagemaker.processing.ProcessingInput(
                    source=training_step.properties.ModelArtifacts.S3ModelArtifacts,
                    destination='/opt/ml/processing/model'
                ),
                sagemaker.processing.ProcessingInput(
                    source=preprocessing_step.properties.ProcessingOutputConfig.Outputs['test'].S3Output.S3Uri,
                    destination='/opt/ml/processing/test'
                )
            ],
            outputs=[
                sagemaker.processing.ProcessingOutput(
                    output_name='evaluation',
                    source='/opt/ml/processing/evaluation',
                    destination=f's3://{self.bucket}/evaluation'
                )
            ],
            property_files=[
                sagemaker.workflow.properties.PropertyFile(
                    name='EvaluationReport',
                    output_name='evaluation',
                    path='evaluation.json'
                )
            ]
        )
        
        # 4. Model Registration (conditional on accuracy)
        model_metrics = ModelMetrics(
            model_statistics=MetricsSource(
                s3_uri=f's3://{self.bucket}/evaluation/evaluation.json',
                content_type='application/json'
            )
        )
        
        drift_check_baselines = DriftCheckBaselines(
            model_data_statistics=MetricsSource(
                s3_uri=preprocessing_step.properties.ProcessingOutputConfig.Outputs['baseline'].S3Output.S3Uri,
                content_type='application/json'
            )
        )
        
        register_step = RegisterModel(
            name='RegisterModel',
            estimator=xgboost_estimator,
            model_data=training_step.properties.ModelArtifacts.S3ModelArtifacts,
            content_types=['text/csv'],
            response_types=['application/json'],
            inference_instances=['ml.m5.large', 'ml.m5.xlarge'],
            transform_instances=['ml.m5.xlarge'],
            model_package_group_name='churn-prediction-models',
            approval_status='PendingManualApproval',
            model_metrics=model_metrics,
            drift_check_baselines=drift_check_baselines
        )
        
        # 5. Conditional model registration based on accuracy
        accuracy_condition = ConditionGreaterThanOrEqualTo(
            left=JsonGet(
                step_name=evaluation_step.name,
                property_file='EvaluationReport',
                json_path='binary_classification_metrics.accuracy.value'
            ),
            right=0.90  # Only register if accuracy >= 90%
        )
        
        condition_step = ConditionStep(
            name='CheckAccuracyCondition',
            conditions=[accuracy_condition],
            if_steps=[register_step],
            else_steps=[]
        )
        
        # 6. Create Pipeline
        pipeline = Pipeline(
            name='churn-prediction-mlops-pipeline',
            parameters=[],
            steps=[
                preprocessing_step,
                training_step,
                evaluation_step,
                condition_step
            ],
            sagemaker_session=self.sagemaker_session
        )
        
        return pipeline

# Create and execute pipeline
pipeline_builder = MLOpsPipeline(
    role_arn='arn:aws:iam::123456789012:role/SageMakerRole',
    bucket='ml-ops-bucket',
    region='us-east-1'
)

pipeline = pipeline_builder.create_pipeline()
pipeline.upsert(role_arn=pipeline_builder.role)

# Start pipeline execution
execution = pipeline.start()
execution.wait()
```

**Preprocessing Script (preprocessing.py):**
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import argparse
import json
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--quality-threshold', type=float, default=0.95)
    args = parser.parse_args()
    
    # Read data
    input_path = '/opt/ml/processing/input'
    df = pd.read_csv(f'{input_path}/customer_data.csv')
    
    # Data quality checks
    null_percentage = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
    duplicate_percentage = df.duplicated().sum() / df.shape[0]
    
    quality_score = 1 - (null_percentage + duplicate_percentage)
    
    if quality_score < args.quality_threshold:
        raise ValueError(f"Data quality {quality_score:.2f} below threshold {args.quality_threshold}")
    
    # Handle missing values
    df = df.dropna()
    
    # Feature engineering
    df['tenure_months'] = df['tenure_days'] / 30
    df['avg_monthly_spend'] = df['total_spend'] / df['tenure_months']
    df['purchase_frequency'] = df['num_purchases'] / df['tenure_months']
    
    # Split data
    train, temp = train_test_split(df, test_size=0.3, random_state=42, stratify=df['churn'])
    validation, test = train_test_split(temp, test_size=0.5, random_state=42, stratify=temp['churn'])
    
    # Save splits
    train.to_csv('/opt/ml/processing/train/train.csv', index=False, header=False)
    validation.to_csv('/opt/ml/processing/validation/validation.csv', index=False, header=False)
    test.to_csv('/opt/ml/processing/test/test.csv', index=False, header=True)
    
    # Save baseline statistics for drift detection
    baseline_stats = {
        'features': list(df.drop('churn', axis=1).columns),
        'statistics': df.drop('churn', axis=1).describe().to_dict()
    }
    
    with open('/opt/ml/processing/baseline/baseline.json', 'w') as f:
        json.dump(baseline_stats, f)
```

**Evaluation Script (evaluation.py):**
```python
import json
import pandas as pd
import tarfile
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

if __name__ == '__main__':
    # Load model
    model_path = '/opt/ml/processing/model/model.tar.gz'
    with tarfile.open(model_path) as tar:
        tar.extractall('/tmp/model')
    
    with open('/tmp/model/xgboost-model', 'rb') as f:
        model = pickle.load(f)
    
    # Load test data
    test_df = pd.read_csv('/opt/ml/processing/test/test.csv')
    X_test = test_df.drop('churn', axis=1)
    y_test = test_df['churn']
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = {
        'binary_classification_metrics': {
            'accuracy': {'value': float(accuracy_score(y_test, y_pred))},
            'precision': {'value': float(precision_score(y_test, y_pred))},
            'recall': {'value': float(recall_score(y_test, y_pred))},
            'f1_score': {'value': float(f1_score(y_test, y_pred))},
            'auc': {'value': float(roc_auc_score(y_test, y_pred_proba))}
        }
    }
    
    # Save evaluation report
    with open('/opt/ml/processing/evaluation/evaluation.json', 'w') as f:
        json.dump(metrics, f)
    
    print(f"Model Evaluation Metrics: {metrics}")
```

**Automated Retraining with EventBridge and Lambda:**
```python
# lambda_trigger_retraining.py
import boto3
import json
from datetime import datetime

sagemaker = boto3.client('sagemaker')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """Trigger retraining based on drift detection or schedule"""
    
    # Check for data drift
    drift_detected = check_data_drift()
    
    # Check model performance
    model_performance = get_production_metrics()
    
    needs_retraining = (
        drift_detected or
        model_performance.get('accuracy', 1.0) < 0.85
    )
    
    if needs_retraining:
        print("Triggering automated retraining...")
        
        response = sagemaker.start_pipeline_execution(
            PipelineName='churn-prediction-mlops-pipeline',
            PipelineExecutionDisplayName=f'auto-retrain-{datetime.now().strftime("%Y%m%d-%H%M")}',
            PipelineParameters=[],
            PipelineExecutionDescription='Automated retraining triggered by drift/performance degradation'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Retraining pipeline started',
                'executionArn': response['PipelineExecutionArn']
            })
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'No retraining needed'})
        }

def check_data_drift():
    """Check if data drift exceeds threshold"""
    model_monitor = boto3.client('sagemaker')
    
    try:
        response = model_monitor.list_monitoring_executions(
            MonitoringScheduleName='churn-model-monitor',
            MaxResults=1,
            SortOrder='Descending'
        )
        
        if response['MonitoringExecutionSummaries']:
            execution_arn = response['MonitoringExecutionSummaries'][0]['MonitoringExecutionArn']
            
            # Get monitoring results
            execution_details = model_monitor.describe_monitoring_execution(
                MonitoringExecutionArn=execution_arn
            )
            
            # Check for violations
            if execution_details.get('ExitMessage', '').find('Violations detected') >= 0:
                return True
        
        return False
    except Exception as e:
        print(f"Error checking drift: {e}")
        return False

def get_production_metrics():
    """Retrieve production model metrics from CloudWatch"""
    cloudwatch = boto3.client('cloudwatch')
    
    try:
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/SageMaker',
            MetricName='ModelAccuracy',
            Dimensions=[
                {'Name': 'EndpointName', 'Value': 'churn-prediction-endpoint'}
            ],
            StartTime=datetime.now() - timedelta(days=7),
            EndTime=datetime.now(),
            Period=86400,
            Statistics=['Average']
        )
        
        if response['Datapoints']:
            latest_accuracy = response['Datapoints'][-1]['Average']
            return {'accuracy': latest_accuracy}
        
        return {'accuracy': 1.0}
    except Exception as e:
        print(f"Error getting metrics: {e}")
        return {'accuracy': 1.0}
```

**CI/CD Pipeline with CodePipeline:**
```yaml
# buildspec.yml for CodeBuild
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.9
    commands:
      - pip install sagemaker boto3 pytest

  pre_build:
    commands:
      - echo "Running tests..."
      - pytest tests/ -v
      - echo "Validating pipeline definition..."
      - python validate_pipeline.py

  build:
    commands:
      - echo "Creating/updating SageMaker Pipeline..."
      - python mlops_pipeline.py
      - echo "Pipeline updated successfully"

  post_build:
    commands:
      - echo "Starting pipeline execution for testing..."
      - python trigger_pipeline.py --test-mode

artifacts:
  files:
    - '**/*'
```

**Model Monitoring Setup:**
```python
# setup_model_monitoring.py
from sagemaker.model_monitor import DataCaptureConfig, ModelMonitor
from sagemaker.model_monitor import CronExpressionGenerator

# Enable data capture on endpoint
data_capture_config = DataCaptureConfig(
    enable_capture=True,
    sampling_percentage=100,
    destination_s3_uri=f's3://{bucket}/data-capture'
)

# Create monitoring schedule
my_monitor = ModelMonitor(
    role=role,
    instance_count=1,
    instance_type='ml.m5.xlarge',
    volume_size_in_gb=20,
    max_runtime_in_seconds=3600,
)

my_monitor.create_monitoring_schedule(
    monitor_schedule_name='churn-model-monitor',
    endpoint_input='churn-prediction-endpoint',
    statistics=f's3://{bucket}/baseline/baseline.json',
    constraints=f's3://{bucket}/baseline/constraints.json',
    schedule_cron_expression=CronExpressionGenerator.hourly(),
    enable_cloudwatch_metrics=True
)
```

---

##### Q. How do you implement AIOps with AWS using CloudWatch, EventBridge, and Machine Learning for automated incident response?

**Answer:**
AIOps in AWS uses CloudWatch Logs Insights, Anomaly Detection, EventBridge for event-driven automation, and Lambda for intelligent remediation.

**Architecture:**

```python
# aiops_framework.py
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd
import numpy as np

class AIOpsFramework:
    """Intelligent Operations with AWS services"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.logs = boto3.client('logs', region_name=region)
        self.events = boto3.client('events', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.sns = boto3.client('sns', region_name=region)
        self.ec2 = boto3.client('ec2', region_name=region)
        self.ssm = boto3.client('ssm', region_name=region)
        
    def setup_anomaly_detection(self, metric_name: str, namespace: str):
        """Enable CloudWatch Anomaly Detection"""
        
        # Create anomaly detector
        self.cloudwatch.put_anomaly_detector(
            Namespace=namespace,
            MetricName=metric_name,
            Stat='Average',
            Configuration={
                'ExcludedTimeRanges': [],
                'MetricTimezone': 'UTC'
            }
        )
        
        # Create alarm based on anomaly detection
        self.cloudwatch.put_metric_alarm(
            AlarmName=f'{metric_name}-anomaly-alarm',
            ComparisonOperator='LessThanLowerOrGreaterThanUpperThreshold',
            EvaluationPeriods=2,
            Metrics=[
                {
                    'Id': 'm1',
                    'ReturnData': True,
                    'MetricStat': {
                        'Metric': {
                            'Namespace': namespace,
                            'MetricName': metric_name
                        },
                        'Period': 300,
                        'Stat': 'Average'
                    }
                },
                {
                    'Id': 'ad1',
                    'Expression': 'ANOMALY_DETECTION_BAND(m1, 2)',
                    'Label': 'Anomaly Detection Band'
                }
            ],
            ThresholdMetricId='ad1',
            AlarmActions=[
                'arn:aws:sns:us-east-1:123456789012:aiops-alerts'
            ]
        )
        
    def create_composite_alarm(self):
        """Create composite alarm for complex incident detection"""
        
        self.cloudwatch.put_composite_alarm(
            AlarmName='critical-system-health',
            AlarmDescription='Composite alarm for critical system issues',
            ActionsEnabled=True,
            AlarmActions=[
                'arn:aws:sns:us-east-1:123456789012:critical-alerts',
                'arn:aws:lambda:us-east-1:123456789012:function:auto-remediate'
            ],
            AlarmRule="""
                (ALARM("high-cpu-alarm") AND ALARM("high-memory-alarm"))
                OR
                (ALARM("error-rate-alarm") AND ALARM("latency-alarm"))
                OR
                ALARM("database-connection-alarm")
            """
        )
    
    def analyze_logs_with_insights(self, log_group: str, query: str, hours: int = 24):
        """Use CloudWatch Logs Insights for pattern detection"""
        
        start_time = int((datetime.now() - timedelta(hours=hours)).timestamp())
        end_time = int(datetime.now().timestamp())
        
        # Start query
        response = self.logs.start_query(
            logGroupName=log_group,
            startTime=start_time,
            endTime=end_time,
            queryString=query
        )
        
        query_id = response['queryId']
        
        # Wait for query completion
        while True:
            result = self.logs.get_query_results(queryId=query_id)
            
            if result['status'] == 'Complete':
                return result['results']
            elif result['status'] == 'Failed':
                raise Exception(f"Query failed: {result}")
            
            time.sleep(1)
    
    def predict_incidents_with_ml(self):
        """Use historical data to predict potential incidents"""
        
        # Query historical incident data
        query = """
        fields @timestamp, @message, errorType, affectedService
        | filter @message like /ERROR|CRITICAL|FATAL/
        | stats count() as errorCount by bin(5m) as time_bucket, affectedService
        | sort time_bucket desc
        """
        
        results = self.analyze_logs_with_insights('/aws/lambda/production', query, hours=168)
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {field['field']: field['value'] for field in result}
            for result in results
        ])
        
        # Simple anomaly detection using statistical methods
        df['errorCount'] = pd.to_numeric(df['errorCount'])
        df['z_score'] = (df['errorCount'] - df['errorCount'].mean()) / df['errorCount'].std()
        
        # Detect anomalies (z-score > 3)
        anomalies = df[df['z_score'].abs() > 3]
        
        if not anomalies.empty:
            self.trigger_proactive_remediation(anomalies)
        
        return anomalies
    
    def setup_eventbridge_rules(self):
        """Configure EventBridge for event-driven automation"""
        
        # Rule for EC2 state changes
        self.events.put_rule(
            Name='ec2-instance-state-change',
            EventPattern=json.dumps({
                'source': ['aws.ec2'],
                'detail-type': ['EC2 Instance State-change Notification'],
                'detail': {
                    'state': ['stopped', 'terminated']
                }
            }),
            State='ENABLED',
            Description='Detect unexpected EC2 shutdowns'
        )
        
        # Add target for automated response
        self.events.put_targets(
            Rule='ec2-instance-state-change',
            Targets=[
                {
                    'Id': '1',
                    'Arn': 'arn:aws:lambda:us-east-1:123456789012:function:investigate-ec2-shutdown',
                    'RetryPolicy': {
                        'MaximumRetryAttempts': 2,
                        'MaximumEventAge': 3600
                    }
                }
            ]
        )
        
        # Rule for high error rates in Lambda
        self.events.put_rule(
            Name='lambda-error-spike',
            EventPattern=json.dumps({
                'source': ['aws.cloudwatch'],
                'detail-type': ['CloudWatch Alarm State Change'],
                'detail': {
                    'alarmName': [{'prefix': 'lambda-errors-'}],
                    'state': {'value': ['ALARM']}
                }
            }),
            State='ENABLED'
        )
        
        self.events.put_targets(
            Rule='lambda-error-spike',
            Targets=[
                {
                    'Id': '1',
                    'Arn': 'arn:aws:lambda:us-east-1:123456789012:function:analyze-lambda-errors',
                    'Input': json.dumps({
                        'action': 'investigate',
                        'severity': 'high'
                    })
                }
            ]
        )
    
    def automated_remediation(self, incident_type: str, resource_id: str):
        """Execute automated remediation based on incident type"""
        
        remediation_playbooks = {
            'high_cpu': self.remediate_high_cpu,
            'memory_leak': self.remediate_memory_leak,
            'disk_full': self.remediate_disk_full,
            'application_error': self.remediate_application_error
        }
        
        if incident_type in remediation_playbooks:
            return remediation_playbooks[incident_type](resource_id)
        else:
            self.escalate_to_oncall(incident_type, resource_id)
    
    def remediate_high_cpu(self, instance_id: str):
        """Auto-remediate high CPU usage"""
        
        # Step 1: Analyze current state
        response = self.ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        
        # Step 2: Create snapshot before remediation
        volumes = [vol['Ebs']['VolumeId'] for vol in instance['BlockDeviceMappings']]
        snapshots = []
        
        for volume_id in volumes:
            snapshot = self.ec2.create_snapshot(
                VolumeId=volume_id,
                Description=f'Pre-remediation snapshot for {instance_id}'
            )
            snapshots.append(snapshot['SnapshotId'])
        
        # Step 3: Try to identify and kill high CPU process via SSM
        command = self.ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunShellScript',
            Parameters={
                'commands': [
                    'ps aux --sort=-%cpu | head -n 10',
                    'top -b -n 1 | head -n 20'
                ]
            }
        )
        
        # Step 4: If issue persists, restart instance
        self.cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=datetime.now() - timedelta(minutes=5),
            EndTime=datetime.now(),
            Period=300,
            Statistics=['Average']
        )
        
        # Decision logic
        # If CPU still high after 10 minutes, restart
        self.ec2.reboot_instances(InstanceIds=[instance_id])
        
        return {
            'action': 'reboot',
            'instance_id': instance_id,
            'snapshots': snapshots,
            'timestamp': datetime.now().isoformat()
        }
    
    def remediate_memory_leak(self, instance_id: str):
        """Remediate memory leak issues"""
        
        # Execute memory analysis
        command_response = self.ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunShellScript',
            Parameters={
                'commands': [
                    'free -m',
                    'ps aux --sort=-%mem | head -n 20',
                    'systemctl restart application.service'  # Restart application
                ]
            }
        )
        
        return {
            'action': 'application_restart',
            'command_id': command_response['Command']['CommandId']
        }
    
    def remediate_disk_full(self, instance_id: str):
        """Remediate disk full issues"""
        
        # Clean up old logs and temp files
        cleanup_commands = [
            'df -h',
            'du -sh /var/log/* | sort -hr | head -n 10',
            'find /var/log -name "*.log" -mtime +30 -delete',
            'find /tmp -mtime +7 -delete',
            'journalctl --vacuum-time=7d',
            'df -h'
        ]
        
        response = self.ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunShellScript',
            Parameters={'commands': cleanup_commands}
        )
        
        return {
            'action': 'disk_cleanup',
            'command_id': response['Command']['CommandId']
        }

# Lambda function for automated remediation
def lambda_auto_remediate(event, context):
    """Lambda handler for automated incident remediation"""
    
    aiops = AIOpsFramework()
    
    # Parse alarm details
    message = json.loads(event['Records'][0]['Sns']['Message'])
    alarm_name = message['AlarmName']
    state = message['NewStateValue']
    
    if state == 'ALARM':
        # Extract incident details
        dimensions = message['Trigger']['Dimensions']
        instance_id = next((d['value'] for d in dimensions if d['name'] == 'InstanceId'), None)
        
        # Determine incident type from alarm name
        if 'cpu' in alarm_name.lower():
            result = aiops.automated_remediation('high_cpu', instance_id)
        elif 'memory' in alarm_name.lower():
            result = aiops.automated_remediation('memory_leak', instance_id)
        elif 'disk' in alarm_name.lower():
            result = aiops.automated_remediation('disk_full', instance_id)
        
        # Log remediation action
        print(f"Remediation executed: {json.dumps(result)}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
```

**CloudWatch Logs Insights Queries for AIOps:**
```python
# Advanced log analysis queries
aiops_queries = {
    'error_pattern_detection': """
        fields @timestamp, @message, @logStream
        | filter @message like /ERROR|Exception|failed/
        | stats count() as error_count by bin(5m) as time_window, @logStream
        | sort error_count desc
    """,
    
    'latency_analysis': """
        fields @timestamp, duration, requestId
        | filter duration > 1000
        | stats avg(duration) as avg_latency, max(duration) as max_latency, count() as slow_requests
            by bin(1m) as time_window
    """,
    
    'security_audit': """
        fields @timestamp, userIdentity.principalId, eventName, sourceIPAddress
        | filter eventName like /Delete|Terminate|Stop/
        | stats count() as destructive_actions by userIdentity.principalId, eventName
        | sort destructive_actions desc
    """,
    
    'cost_anomaly_detection': """
        fields @timestamp, resourceId, cost
        | stats sum(cost) as total_cost by resourceId, bin(1h) as hour
        | sort total_cost desc
    """
}
```

---

##### Q. How do you build a serverless real-time data pipeline in AWS with Kinesis, Lambda, and DynamoDB for high-throughput event processing?

**Answer:**
AWS serverless data pipelines provide auto-scaling, pay-per-use pricing, and minimal operational overhead for real-time analytics.

**Architecture:**
1. **Kinesis Data Streams** - Real-time data ingestion
2. **Lambda** - Stream processing and transformation
3. **Kinesis Data Firehose** - Delivery to S3/Redshift
4. **DynamoDB** - Low-latency data store
5. **Athena** - SQL analytics on S3
6. **QuickSight** - Visualization

**Implementation:**

```bash
# Create Kinesis Data Stream
aws kinesis create-stream \
  --stream-name transaction-events \
  --shard-count 10 \
  --stream-mode-details StreamMode=PROVISIONED

# Enable enhanced monitoring
aws kinesis enable-enhanced-monitoring \
  --stream-name transaction-events \
  --shard-level-metrics IncomingBytes,IncomingRecords,OutgoingBytes,OutgoingRecords,WriteProvisionedThroughputExceeded,ReadProvisionedThroughputExceeded

# Create DynamoDB table for processed data
aws dynamodb create-table \
  --table-name TransactionSummary \
  --attribute-definitions \
    AttributeName=customerId,AttributeType=S \
    AttributeName=timestamp,AttributeType=N \
  --key-schema \
    AttributeName=customerId,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES \
  --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true \
  --sse-specification Enabled=true,SSEType=KMS \
  --tags Key=Environment,Value=Production Key=DataClassification,Value=Confidential
```

**Lambda Stream Processor:**
```python
# stream_processor.py
import json
import boto3
import base64
from datetime import datetime
from decimal import Decimal
from typing import Dict, List
import hashlib

dynamodb = boto3.resource('dynamodb')
firehose = boto3.client('firehose')
cloudwatch = boto3.client('cloudwatch')

transaction_table = dynamodb.Table('TransactionSummary')
anomaly_table = dynamodb.Table('AnomalyDetection')

def lambda_handler(event, context):
    """Process Kinesis stream records"""
    
    processed_records = 0
    failed_records = 0
    anomalies_detected = 0
    
    for record in event['Records']:
        try:
            # Decode Kinesis data
            payload = base64.b64decode(record['kinesis']['data'])
            transaction = json.loads(payload)
            
            # Data validation
            if not validate_transaction(transaction):
                failed_records += 1
                send_to_dlq(transaction, 'validation_failed')
                continue
            
            # Enrich data
            enriched_transaction = enrich_transaction(transaction)
            
            # Fraud detection
            if detect_anomaly(enriched_transaction):
                anomalies_detected += 1
                flag_for_review(enriched_transaction)
            
            # Aggregate and store
            update_customer_summary(enriched_transaction)
            
            # Send to data lake
            send_to_firehose(enriched_transaction)
            
            processed_records += 1
            
        except Exception as e:
            failed_records += 1
            print(f"Error processing record: {e}")
            send_to_dlq(record, str(e))
    
    # Publish metrics
    publish_metrics(processed_records, failed_records, anomalies_detected)
    
    return {
        'statusCode': 200,
        'recordsProcessed': processed_records,
        'recordsFailed': failed_records,
        'anomaliesDetected': anomalies_detected
    }

def validate_transaction(transaction: Dict) -> bool:
    """Validate transaction data quality"""
    required_fields = ['transactionId', 'customerId', 'amount', 'timestamp', 'merchantId']
    
    # Check required fields
    if not all(field in transaction for field in required_fields):
        return False
    
    # Validate amount
    if not isinstance(transaction['amount'], (int, float)) or transaction['amount'] <= 0:
        return False
    
    # Validate timestamp (not in future)
    if transaction['timestamp'] > datetime.now().timestamp():
        return False
    
    return True

def enrich_transaction(transaction: Dict) -> Dict:
    """Enrich transaction with additional data"""
    
    # Add derived fields
    transaction['hour'] = datetime.fromtimestamp(transaction['timestamp']).hour
    transaction['dayOfWeek'] = datetime.fromtimestamp(transaction['timestamp']).weekday()
    
    # Calculate transaction hash for deduplication
    transaction['transactionHash'] = hashlib.sha256(
        f"{transaction['transactionId']}{transaction['timestamp']}".encode()
    ).hexdigest()
    
    # Lookup customer tier (cached in Lambda)
    customer_tier = get_customer_tier(transaction['customerId'])
    transaction['customerTier'] = customer_tier
    
    # Geo-enrichment
    if 'ipAddress' in transaction:
        geo_data = lookup_geo_location(transaction['ipAddress'])
        transaction['country'] = geo_data.get('country')
        transaction['city'] = geo_data.get('city')
    
    return transaction

def detect_anomaly(transaction: Dict) -> bool:
    """Real-time fraud/anomaly detection"""
    
    # Get customer's historical spending pattern
    customer_id = transaction['customerId']
    
    response = transaction_table.query(
        KeyConditionExpression='customerId = :cid',
        ExpressionAttributeValues={
            ':cid': customer_id
        },
        ScanIndexForward=False,
        Limit=100
    )
    
    if not response['Items']:
        return False  # New customer, no baseline
    
    # Calculate historical statistics
    historical_amounts = [Decimal(str(item['totalAmount'])) for item in response['Items']]
    avg_amount = sum(historical_amounts) / len(historical_amounts)
    
    # Anomaly rules
    current_amount = Decimal(str(transaction['amount']))
    
    # Rule 1: Transaction amount > 3x average
    if current_amount > avg_amount * 3:
        return True
    
    # Rule 2: Multiple transactions in short time window
    recent_count = sum(1 for item in response['Items'] 
                      if item['timestamp'] > transaction['timestamp'] - 300)  # 5 minutes
    if recent_count > 5:
        return True
    
    # Rule 3: Foreign transaction for domestic customer
    if transaction.get('country') != 'US' and transaction.get('customerTier') == 'Domestic':
        return True
    
    return False

def update_customer_summary(transaction: Dict):
    """Update customer transaction summary in DynamoDB"""
    
    try:
        transaction_table.update_item(
            Key={
                'customerId': transaction['customerId'],
                'timestamp': int(transaction['timestamp'])
            },
            UpdateExpression="""
                SET totalAmount = if_not_exists(totalAmount, :zero) + :amount,
                    transactionCount = if_not_exists(transactionCount, :zero) + :one,
                    lastUpdated = :now,
                    merchantIds = list_append(if_not_exists(merchantIds, :empty_list), :merchant)
            """,
            ExpressionAttributeValues={
                ':amount': Decimal(str(transaction['amount'])),
                ':one': 1,
                ':zero': 0,
                ':now': int(datetime.now().timestamp()),
                ':merchant': [transaction['merchantId']],
                ':empty_list': []
            },
            ReturnValues='UPDATED_NEW'
        )
    except Exception as e:
        print(f"Error updating DynamoDB: {e}")
        raise

def flag_for_review(transaction: Dict):
    """Flag suspicious transaction for manual review"""
    
    anomaly_table.put_item(
        Item={
            'anomalyId': transaction['transactionHash'],
            'transactionId': transaction['transactionId'],
            'customerId': transaction['customerId'],
            'amount': Decimal(str(transaction['amount'])),
            'timestamp': int(transaction['timestamp']),
            'reason': 'Anomaly detected by real-time processing',
            'status': 'PENDING_REVIEW',
            'flaggedAt': int(datetime.now().timestamp())
        }
    )
    
    # Send SNS notification
    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:123456789012:fraud-alerts',
        Subject='Suspicious Transaction Detected',
        Message=json.dumps(transaction, default=str)
    )

def send_to_firehose(transaction: Dict):
    """Send processed data to S3 via Firehose"""
    
    firehose.put_record(
        DeliveryStreamName='transaction-data-stream',
        Record={
            'Data': json.dumps(transaction, default=str) + '\n'
        }
    )

def send_to_dlq(record: Dict, error_reason: str):
    """Send failed records to dead letter queue"""
    
    sqs = boto3.client('sqs')
    sqs.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/123456789012/transaction-dlq',
        MessageBody=json.dumps({
            'record': record,
            'error': error_reason,
            'timestamp': datetime.now().isoformat()
        })
    )

def publish_metrics(processed: int, failed: int, anomalies: int):
    """Publish custom metrics to CloudWatch"""
    
    cloudwatch.put_metric_data(
        Namespace='TransactionPipeline',
        MetricData=[
            {
                'MetricName': 'RecordsProcessed',
                'Value': processed,
                'Unit': 'Count',
                'Timestamp': datetime.now()
            },
            {
                'MetricName': 'RecordsFailed',
                'Value': failed,
                'Unit': 'Count',
                'Timestamp': datetime.now()
            },
            {
                'MetricName': 'AnomaliesDetected',
                'Value': anomalies,
                'Unit': 'Count',
                'Timestamp': datetime.now()
            }
        ]
    )

def get_customer_tier(customer_id: str) -> str:
    """Get customer tier (with caching)"""
    # Implement caching logic or Lambda layer
    return 'Premium'  # Placeholder

def lookup_geo_location(ip_address: str) -> Dict:
    """Lookup geographic location from IP"""
    # Integrate with MaxMind or similar service
    return {'country': 'US', 'city': 'New York'}  # Placeholder
```

**Kinesis Data Firehose for S3:**
```bash
# Create Firehose delivery stream
aws firehose create-delivery-stream \
  --delivery-stream-name transaction-data-stream \
  --delivery-stream-type DirectPut \
  --s3-destination-configuration '{
    "RoleARN": "arn:aws:iam::123456789012:role/FirehoseRole",
    "BucketARN": "arn:aws:s3:::transaction-data-lake",
    "Prefix": "transactions/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/",
    "ErrorOutputPrefix": "errors/",
    "BufferingHints": {
      "SizeInMBs": 128,
      "IntervalInSeconds": 300
    },
    "CompressionFormat": "GZIP",
    "EncryptionConfiguration": {
      "KMSEncryptionConfig": {
        "AWSKMSKeyARN": "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012"
      }
    },
    "DataFormatConversionConfiguration": {
      "SchemaConfiguration": {
        "CatalogId": "123456789012",
        "RoleARN": "arn:aws:iam::123456789012:role/FirehoseRole",
        "DatabaseName": "transactions_db",
        "TableName": "transactions",
        "Region": "us-east-1"
      },
      "InputFormatConfiguration": {
        "Deserializer": {
          "OpenXJsonSerDe": {}
        }
      },
      "OutputFormatConfiguration": {
        "Serializer": {
          "ParquetSerDe": {
            "Compression": "SNAPPY"
          }
        }
      },
      "Enabled": true
    }
  }'
```

**Athena Query for Analytics:**
```sql
-- Create external table for Parquet data
CREATE EXTERNAL TABLE IF NOT EXISTS transactions (
    transactionId STRING,
    customerId STRING,
    amount DECIMAL(18,2),
    timestamp BIGINT,
    merchantId STRING,
    customerTier STRING,
    country STRING,
    city STRING,
    hour INT,
    dayOfWeek INT
)
PARTITIONED BY (
    year STRING,
    month STRING,
    day STRING
)
STORED AS PARQUET
LOCATION 's3://transaction-data-lake/transactions/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- Repair partitions
MSCK REPAIR TABLE transactions;

-- Analytics queries
-- Daily transaction volume by customer tier
SELECT 
    year,
    month,
    day,
    customerTier,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM transactions
WHERE year = '2026' AND month = '02'
GROUP BY year, month, day, customerTier
ORDER BY year, month, day, total_amount DESC;

-- Hourly transaction patterns
SELECT 
    hour,
    dayOfWeek,
    COUNT(*) as transaction_count,
    APPROX_PERCENTILE(amount, 0.5) as median_amount,
    APPROX_PERCENTILE(amount, 0.95) as p95_amount
FROM transactions
WHERE year = '2026' AND month = '02'
GROUP BY hour, dayOfWeek
ORDER BY hour, dayOfWeek;
```

---

##### Q. How do you implement Infrastructure Security and Compliance as Code in AWS using Security Hub, Config, and automated remediation?

**Answer:**
Security as Code ensures consistent security posture across AWS accounts with automated compliance checks and remediation.

**Architecture:**

```python
# security_automation.py
import boto3
import json
from typing import Dict, List

class AWSSecurityAutomation:
    """Automated security and compliance framework"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.config = boto3.client('config', region_name=region)
        self.security_hub = boto3.client('securityhub', region_name=region)
        self.iam = boto3.client('iam')
        self.ec2 = boto3.client('ec2', region_name=region)
        self.s3 = boto3.client('s3')
        self.kms = boto3.client('kms', region_name=region)
        self.guardduty = boto3.client('guardduty', region_name=region)
        
    def enable_security_hub(self, standards: List[str] = None):
        """Enable Security Hub with compliance standards"""
        
        # Enable Security Hub
        try:
            self.security_hub.enable_security_hub()
        except self.security_hub.exceptions.ResourceConflictException:
            print("Security Hub already enabled")
        
        # Enable standards
        if standards is None:
            standards = [
                'arn:aws:securityhub:us-east-1::standards/aws-foundational-security-best-practices/v/1.0.0',
                'arn:aws:securityhub:us-east-1::standards/cis-aws-foundations-benchmark/v/1.2.0',
                'arn:aws:securityhub:us-east-1::standards/pci-dss/v/3.2.1'
            ]
        
        for standard_arn in standards:
            try:
                self.security_hub.batch_enable_standards(
                    StandardsSubscriptionRequests=[
                        {'StandardsArn': standard_arn}
                    ]
                )
                print(f"Enabled standard: {standard_arn}")
            except Exception as e:
                print(f"Error enabling standard {standard_arn}: {e}")
    
    def deploy_config_rules(self):
        """Deploy AWS Config managed rules"""
        
        config_rules = [
            {
                'ConfigRuleName': 'encrypted-volumes',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'ENCRYPTED_VOLUMES'
                },
                'Scope': {
                    'ComplianceResourceTypes': ['AWS::EC2::Volume']
                }
            },
            {
                'ConfigRuleName': 's3-bucket-public-read-prohibited',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'S3_BUCKET_PUBLIC_READ_PROHIBITED'
                }
            },
            {
                'ConfigRuleName': 's3-bucket-public-write-prohibited',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'S3_BUCKET_PUBLIC_WRITE_PROHIBITED'
                }
            },
            {
                'ConfigRuleName': 'iam-password-policy',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'IAM_PASSWORD_POLICY'
                },
                'InputParameters': json.dumps({
                    'RequireUppercaseCharacters': 'true',
                    'RequireLowercaseCharacters': 'true',
                    'RequireSymbols': 'true',
                    'RequireNumbers': 'true',
                    'MinimumPasswordLength': '14',
                    'PasswordReusePrevention': '24',
                    'MaxPasswordAge': '90'
                })
            },
            {
                'ConfigRuleName': 'mfa-enabled-for-iam-console-access',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS'
                }
            },
            {
                'ConfigRuleName': 'rds-encryption-enabled',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'RDS_STORAGE_ENCRYPTED'
                }
            },
            {
                'ConfigRuleName': 'cloudtrail-enabled',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'CLOUD_TRAIL_ENABLED'
                }
            },
            {
                'ConfigRuleName': 'restricted-ssh',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'INCOMING_SSH_DISABLED'
                }
            }
        ]
        
        for rule in config_rules:
            try:
                self.config.put_config_rule(ConfigRule=rule)
                print(f"Deployed Config rule: {rule['ConfigRuleName']}")
            except Exception as e:
                print(f"Error deploying rule {rule['ConfigRuleName']}: {e}")
    
    def setup_auto_remediation(self):
        """Configure automatic remediation for Config rules"""
        
        remediations = [
            {
                'ConfigRuleName': 's3-bucket-public-read-prohibited',
                'TargetType': 'SSM_DOCUMENT',
                'TargetIdentifier': 'AWS-PublishSNSNotification',
                'TargetVersion': '1',
                'Parameters': {
                    'AutomationAssumeRole': {
                        'StaticValue': {
                            'Values': ['arn:aws:iam::123456789012:role/ConfigRemediationRole']
                        }
                    },
                    'TopicArn': {
                        'StaticValue': {
                            'Values': ['arn:aws:sns:us-east-1:123456789012:security-violations']
                        }
                    },
                    'Message': {
                        'StaticValue': {
                            'Values': ['Public S3 bucket detected and access blocked']
                        }
                    }
                },
                'Automatic': True,
                'MaximumAutomaticAttempts': 5,
                'RetryAttemptSeconds': 60
            },
            {
                'ConfigRuleName': 'encrypted-volumes',
                'TargetType': 'SSM_DOCUMENT',
                'TargetIdentifier': 'Custom-EncryptVolume',
                'Parameters': {
                    'AutomationAssumeRole': {
                        'StaticValue': {
                            'Values': ['arn:aws:iam::123456789012:role/ConfigRemediationRole']
                        }
                    },
                    'VolumeId': {
                        'ResourceValue': {
                            'Value': 'RESOURCE_ID'
                        }
                    }
                },
                'Automatic': True
            }
        ]
        
        for remediation in remediations:
            try:
                self.config.put_remediation_configurations(
                    RemediationConfigurations=[remediation]
                )
                print(f"Configured remediation for: {remediation['ConfigRuleName']}")
            except Exception as e:
                print(f"Error configuring remediation: {e}")
    
    def enable_guardduty(self):
        """Enable GuardDuty for threat detection"""
        
        try:
            response = self.guardduty.create_detector(
                Enable=True,
                FindingPublishingFrequency='FIFTEEN_MINUTES',
                DataSources={
                    'S3Logs': {'Enable': True},
                    'Kubernetes': {
                        'AuditLogs': {'Enable': True}
                    },
                    'MalwareProtection': {
                        'ScanEc2InstanceWithFindings': {
                            'EbsVolumes': {'Enable': True}
                        }
                    }
                },
                Tags={'Environment': 'Production', 'ManagedBy': 'SecurityAutomation'}
            )
            
            detector_id = response['DetectorId']
            print(f"GuardDuty enabled: {detector_id}")
            
            return detector_id
        except self.guardduty.exceptions.BadRequestException:
            # Already enabled
            detectors = self.guardduty.list_detectors()
            return detectors['DetectorIds'][0] if detectors['DetectorIds'] else None
    
    def create_threat_intelligence_set(self, detector_id: str):
        """Add threat intelligence feeds to GuardDuty"""
        
        # Upload threat IP list to S3
        threat_ips = [
            "198.51.100.0/24",
            "203.0.113.0/24"
        ]
        
        threat_list = '\n'.join(threat_ips)
        
        self.s3.put_object(
            Bucket='security-threat-intelligence',
            Key='threat-ips.txt',
            Body=threat_list.encode('utf-8')
        )
        
        # Create threat intel set in GuardDuty
        response = self.guardduty.create_threat_intel_set(
            DetectorId=detector_id,
            Name='CustomThreatIPs',
            Format='TXT',
            Location='s3://security-threat-intelligence/threat-ips.txt',
            Activate=True
        )
        
        print(f"Threat intelligence set created: {response['ThreatIntelSetId']}")
    
    def remediate_security_finding(self, finding: Dict):
        """Automatically remediate security findings"""
        
        finding_type = finding['Types'][0]
        resource_type = finding['Resources'][0]['Type']
        resource_id = finding['Resources'][0]['Id']
        
        print(f"Remediating finding: {finding_type} for {resource_id}")
        
        # S3 bucket public access
        if 'S3' in resource_type and 'public' in finding_type.lower():
            bucket_name = resource_id.split(':')[-1]
            self.remediate_public_s3(bucket_name)
        
        # Unencrypted EBS volume
        elif 'Volume' in resource_type and 'encrypt' in finding_type.lower():
            volume_id = resource_id.split('/')[-1]
            self.remediate_unencrypted_volume(volume_id)
        
        # Security group with open ports
        elif 'SecurityGroup' in resource_type:
            sg_id = resource_id.split('/')[-1]
            self.remediate_open_security_group(sg_id)
        
        # IAM user without MFA
        elif 'IAMUser' in resource_type and 'mfa' in finding_type.lower():
            username = resource_id.split('/')[-1]
            self.remediate_mfa_missing(username)
    
    def remediate_public_s3(self, bucket_name: str):
        """Block public access to S3 bucket"""
        
        try:
            self.s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
            print(f"Blocked public access for bucket: {bucket_name}")
        except Exception as e:
            print(f"Error remediating public S3 bucket: {e}")
    
    def remediate_unencrypted_volume(self, volume_id: str):
        """Create encrypted snapshot and replace volume"""
        
        try:
            # Create snapshot
            snapshot = self.ec2.create_snapshot(
                VolumeId=volume_id,
                Description=f'Pre-encryption snapshot of {volume_id}'
            )
            
            snapshot_id = snapshot['SnapshotId']
            
            # Wait for snapshot completion
            waiter = self.ec2.get_waiter('snapshot_completed')
            waiter.wait(SnapshotIds=[snapshot_id])
            
            # Copy snapshot with encryption
            encrypted_snapshot = self.ec2.copy_snapshot(
                SourceSnapshotId=snapshot_id,
                SourceRegion='us-east-1',
                Encrypted=True,
                KmsKeyId='alias/aws/ebs',
                Description=f'Encrypted copy of {snapshot_id}'
            )
            
            print(f"Created encrypted snapshot: {encrypted_snapshot['SnapshotId']}")
            print(f"Manual step required: Create new volume from {encrypted_snapshot['SnapshotId']} and replace {volume_id}")
            
        except Exception as e:
            print(f"Error remediating unencrypted volume: {e}")
    
    def remediate_open_security_group(self, sg_id: str):
        """Remove overly permissive security group rules"""
        
        try:
            # Get security group rules
            response = self.ec2.describe_security_groups(GroupIds=[sg_id])
            sg = response['SecurityGroups'][0]
            
            # Find and remove rules allowing 0.0.0.0/0 on sensitive ports
            sensitive_ports = [22, 3389, 3306, 5432, 1433]
            
            for rule in sg['IpPermissions']:
                from_port = rule.get('FromPort')
                to_port = rule.get('ToPort')
                
                if from_port in sensitive_ports or to_port in sensitive_ports:
                    for ip_range in rule.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            # Revoke the rule
                            self.ec2.revoke_security_group_ingress(
                                GroupId=sg_id,
                                IpPermissions=[rule]
                            )
                            print(f"Revoked open rule on port {from_port}-{to_port} for SG {sg_id}")
        
        except Exception as e:
            print(f"Error remediating security group: {e}")
    
    def remediate_mfa_missing(self, username: str):
        """Notify user about missing MFA"""
        
        # Cannot auto-enable MFA, but can enforce via policy
        try:
            # Attach policy requiring MFA
            self.iam.attach_user_policy(
                UserName=username,
                PolicyArn='arn:aws:iam::aws:policy/RequireMFAPolicy'
            )
            
            # Send SNS notification
            sns = boto3.client('sns')
            sns.publish(
                TopicArn='arn:aws:sns:us-east-1:123456789012:security-notifications',
                Subject='MFA Required',
                Message=f'User {username} must enable MFA within 24 hours or access will be restricted.'
            )
            
            print(f"MFA enforcement policy attached to user: {username}")
        
        except Exception as e:
            print(f"Error enforcing MFA: {e}")

# Lambda function for automated remediation
def lambda_security_remediation(event, context):
    """Lambda handler for Security Hub findings"""
    
    security_automation = AWSSecurityAutomation()
    
    # Parse Security Hub finding
    finding = event['detail']['findings'][0]
    
    # Remediate
    security_automation.remediate_security_finding(finding)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Remediation executed')
    }

# Deployment
security = AWSSecurityAutomation()
security.enable_security_hub()
security.deploy_config_rules()
security.setup_auto_remediation()
detector_id = security.enable_guardduty()
if detector_id:
    security.create_threat_intelligence_set(detector_id)
```

**EventBridge Rule for Security Automation:**
```json
{
  "source": ["aws.securityhub"],
  "detail-type": ["Security Hub Findings - Imported"],
  "detail": {
    "findings": {
      "Severity": {
        "Label": ["CRITICAL", "HIGH"]
      },
      "Compliance": {
        "Status": ["FAILED"]
      }
    }
  }
}
```

**Terraform for Security Baseline:**
```hcl
# security_baseline.tf
resource "aws_securityhub_account" "main" {}

resource "aws_securityhub_standards_subscription" "cis" {
  depends_on    = [aws_securityhub_account.main]
  standards_arn = "arn:aws:securityhub:${var.region}::standards/cis-aws-foundations-benchmark/v/1.2.0"
}

resource "aws_guardduty_detector" "main" {
  enable = true

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = true
      }
    }
    malware_protection {
      scan_ec2_instance_with_findings {
        ebs_volumes {
          enable = true
        }
      }
    }
  }
}

resource "aws_config_configuration_recorder" "main" {
  name     = "security-config-recorder"
  role_arn = aws_iam_role.config.arn

  recording_group {
    all_supported                 = true
    include_global_resource_types = true
  }
}

resource "aws_config_delivery_channel" "main" {
  name           = "security-config-channel"
  s3_bucket_name = aws_s3_bucket.config.id
  sns_topic_arn  = aws_sns_topic.config.arn

  depends_on = [aws_config_configuration_recorder.main]
}

resource "aws_config_configuration_recorder_status" "main" {
  name       = aws_config_configuration_recorder.main.name
  is_enabled = true

  depends_on = [aws_config_delivery_channel.main]
}
```

I'll continue with 5 more AWS questions in the next response to complete the set of 10...

---



### IAM & Security

##### Q. What is the role of IAM roles and policies?
**Policies** are JSON documents that explicitly define permissions (Allow/Deny actions on specific resources). **Roles** are IAM identities with no permanent credentials (unlike users). Instead, roles are assumed by users, applications, or AWS services (like EC2 or Lambda) to obtain temporary, rotated security credentials to access AWS resources securely without hardcoding access keys.

##### Q. What is the purpose of access keys and secret keys in AWS?
They are long-term programmatic credentials for an IAM User. They consist of an Access Key ID and a Secret Access Key used to authenticate API, CLI, or SDK requests to AWS using an HMAC-SHA256 signature process. They should never be hardcoded or pushed to version control, and temporary rotating roles are preferred wherever possible.

##### Q. How do you attach policies to IAM users, either individually or by group?
Following the Principle of Least Privilege, the best practice is to attach policies to **IAM Groups** (e.g., `DevOpsTeam` or `DBAdmins`) and assign users to those groups, providing scalable and auditable access control. Alternatively, managed or inline policies can be attached directly to a User, though this is discouraged for large teams.

##### Q. Do you use the same AWS account for all environments?
No, it is a strict best practice to use separate AWS environments via **AWS Organizations**. A multi-account strategy (e.g., separate Dev, Security, and Prod accounts) provides the strongest blast-radius isolation, distinct billing, and hard security boundaries that prevent accidental production breakage or credential leakage.

##### Q. If you've exhausted IP addresses in your VPC, how would you provision new resources?
Once created, you cannot resize a primary VPC CIDR block. The best solution is to associate a **Secondary IPv4 CIDR block** to the VPC and create new subnets. If peering or architecture demands it, you could also transition to a hub-and-spoke model using an AWS Transit Gateway, deploying new resources in a newly created VPC.

### Serverless & AWS Lambda

##### Q. What is AWS Lambda, and how does it work?
AWS Lambda is a serverless compute service that runs code in response to events while automatically managing the underlying compute resources. It executes your code within highly available, secure ephemeral containers, scaling precisely with the workload volume, billing only for the compute time consumed down to the millisecond.

##### Q. How do you invoke a Lambda function, and where do you configure it?
Invocations can be **Synchronous** (e.g., API Gateway, CLI), **Asynchronous** (e.g., S3 Event Notifications, EventBridge, SNS), or via **Event Source Mapping** (e.g., reading streams from SQS or DynamoDB). Configuration is done via the AWS Console, SAM, Terraform, or CloudFormation by defining the trigger (event source) and attaching the appropriate Execution Role.

##### Q. Can you describe how Lambda handles scaling and event-based invocations?
Upon receiving an invocation, Lambda securely provisions an execution environment. If concurrent requests arrive, Lambda scales horizontally by provisioning multiple independent environments automatically, up to the account's concurrency limit. Asynchronous events are placed in an internal queue with built-in retries, while Event Source Mappings poll and batch records.

##### Q. What is the maximum runtime and memory size for a Lambda function?
- **Maximum Runtime:** 15 minutes (900 seconds).
- **Maximum Memory:** 10,240 MB (10 GB). Note that vCPU is allocated proportionally based on the memory configured.

##### Q. How can you increase the runtime for a Lambda function?
You can increase the timeout setting up to the hard limit of 15 minutes via the console or IaC. If a workload takes longer than 15 minutes, you must refactor the architecture—typically by using **AWS Step Functions** to chain multiple Lambdas, or offloading the task to AWS Batch or ECS Fargate.

##### Q. Where do you write and save your Lambda function code?
Function code is actively written locally in an IDE (like VS Code) utilizing the AWS SAM CLI for local containerized testing. It is saved in version control (Git). A CI/CD pipeline then packages the code (as a ZIP file uploaded to S3, or a Docker Image uploaded to ECR) before Terraform updates the infrastructure mapping it to the Lambda service.

##### Q. What automations have you performed using Lambda in your project?
- **Cost Optimization:** EventBridge scheduled Lambdas to automatically start/stop non-production EC2 and RDS instances on weekends.
- **Operations:** Automating EBS snapshot backups and auto-tagging resources triggered by AWS CloudTrail `CreateResource` events.
- **Security:** Rotating IAM access keys and automatically reacting to AWS Config non-compliance (e.g., closing overly permissive security groups).

##### Q. What modules have you used in your Lambda function?
Mainly `boto3` (the AWS SDK for Python) to interact with EC2, S3, IAM, and DynamoDB. Standard OS handling modules like `json`, `os`, `logging`, and `datetime`. External libraries like `requests` or `pandas` are packaged heavily utilizing Lambda Layers.

### Load Balancing & Edge Networking

##### Q. What is a Content Delivery Network (CDN), and how does it work?
A CDN (like **Amazon CloudFront**) is a globally distributed network of proxy servers. It caches static and dynamic web content closer to end-users at edge locations. When requested, DNS routes users to the lowest-latency edge. If cached (a hit), it serves immediately; if not (a miss), the edge fetches the asset from the origin (S3/ALB), caches it, and serves the user.

##### Q. How does an Elastic Load Balancer (ELB) distribute traffic?
An ELB acts as a single point of ingress. 
- **ALB (Application Load Balancer)** operates at Layer 7, inspecting HTTP/HTTPS headers and URL paths to intelligently route traffic using Round Robin or Least Outstanding Requests algorithms.
- **NLB (Network Load Balancer)** operates at Layer 4 (TCP/UDP), routing traffic highly efficiently using a flow hash algorithm based on IP, Protocol, and Port for ultra-high throughput and extreme low latency.

##### Q. Can you describe the different types of Load Balancers and provide examples?
- **Application Load Balancer (ALB):** Best for HTTP/HTTPS web apps and microservices (e.g., routing `/api` to an identity service and `/images` to another target group).
- **Network Load Balancer (NLB):** Best for custom TCP/UDP protocols requiring static IPs and millions of requests per second (e.g., gaming servers, IoT).
- **Gateway Load Balancer (GLB):** Used to deploy, scale, and manage third-party virtual appliances inline, like specialized firewalls or IDS/IPS.

##### Q. What is connection draining, and how does it work?
Known as **Deregistration Delay** in AWS. When an EC2 instance becomes unhealthy or scaled down, the ELB stops sending *new* requests to it, but allows existing, in-flight requests to complete within a specified timeout (default 300s). This ensures graceful scaling and prevents abrupt termination of user sessions.

##### Q. What is auto-scaling, and how does it work?
Auto Scaling ensures you have the correct number of EC2 instances to handle the load of your application. It utilizes CloudWatch alarms (e.g., CPU > 70%) to trigger scaling policies. An Auto Scaling Group (ASG) automatically provisions new instances from a Launch Template, seamlessly registers them with the ELB Target Group, and scales back in cost-efficiently when demand drops.

### Storage, Security & Monitoring

##### Q. What is Amazon CloudWatch, and have you configured any custom metrics?
CloudWatch is a centralized native observability service for metrics, logs, and events. Yes, I've utilized the `PutMetricData` API (via Boto3 or the CloudWatch Agent) to track **custom metrics** that AWS cannot see inherently—such as "Active Application Sessions", "Completed Transactions", or explicit memory utilization inside EC2 instances.

##### Q. What metrics are available on your CloudWatch dashboard, and how do you configure CPU utilization?
- **Available Metrics:** EC2 (`CPUUtilization`, `NetworkIn/Out`), RDS (`DatabaseConnections`, `FreeStorageSpace`), ALB (`RequestCount`, `HTTPCode_Target_5XX_Count`), and Lambda (`Invocations`, `Duration`, `Errors`).
- **Configuration:** Navigate to CloudWatch > Dashboards > Add Widget > Line graph > Select Metrics > EC2 > Per-Instance Metrics > check the `CPUUtilization` box for your instances > Create widget.

##### Q. How do you attach an SSL certificate to an S3 bucket?
S3 static website hosting does not natively support custom SSL certificates at the bucket level. You must put **Amazon CloudFront** in front of the S3 bucket. You provision a public SSL certificate via AWS Certificate Manager (ACM) in the `us-east-1` region, and attach it to the CloudFront distribution while targeting the S3 endpoint.

##### Q. If an S3 bucket has a read-only policy, can you modify objects in the bucket?
No. An explicit `Deny`—or lack of `Allow` permissions for `s3:PutObject` or `s3:DeleteObject`—means modification is blocked. Identity-based policies cannot override an Explicit Deny inside an S3 Bucket Policy, returning an Access Denied (HTTP 403) error upon modification attempts.

##### Q. What type of encryption have you implemented in your project?
- **In-transit:** TLS 1.2/1.3 enforced across all API endpoints, Load Balancers, and CloudFront.
- **At-rest:** Utilized SSE-S3 (AES-256 managed by AWS) for simple storage, and **SSE-KMS** (Customer Managed Keys) for highly sensitive data in RDS, EBS, and Secrets Manager to ensure granular permission control, auditing, and automated key rotation.

##### Q. Have you used any tools to create customized Amazon Machine Images (AMIs)?
Yes, **HashiCorp Packer**. I define infrastructure templates (HCL) mapping to a source AMI (like a bare Ubuntu server). Packer utilizes provisioners (like Ansible or bash scripts) to bake in dependencies, install agents, and harden the OS. It generates an immutable, finalized AMI and outputs the new AMI ID to be consumed by Terraform.

##### Q. Have you created an SNS topic for your project?
Yes, **Amazon SNS** (Simple Notification Service) is deployed as a Pub/Sub mechanism. A practical example: Critical CloudWatch Alarms are tied to an SNS topic, which fans out alerts simultaneously to an SQS queue for self-healing worker processing, and directly emails the DevOps on-call team.


### Edge-Case & Troubleshooting Scenarios (AWS)

##### Q. You launched an EC2 instance, but it’s stuck in the “pending” state. What’s going on?
**Answer:** It could be an unavailable AMI or the requested instance type is out of capacity in that specific Availability Zone. I’d check if the AMI exists (or is shared correctly) and if the AZ supports the instance type. Occasionally, it could also be due to an EBS volume KMS key encryption issue where the EC2 service role lacks permissions.

##### Q. Your ALB is routing traffic unevenly across healthy targets. Why might that happen?
**Answer:** The ALB’s load balancing algorithm might be session-based. I’d check if sticky sessions are enabled, causing one target to absorb all traffic from a heavy user. Another common cause is having cross-zone load balancing turned off, which causes uneven distribution if targets are not evenly distributed across Availability Zones.

##### Q. You’re using AWS Secrets Manager, but your application can’t retrieve the secret. What’s wrong?
**Answer:** The application’s IAM role (e.g., EC2 Instance Profile or ECS Task Role) might lack the `secretsmanager:GetSecretValue` permission, or if the secret is encrypted with a custom KMS key, it might lack `kms:Decrypt`. Additionally, the secret’s ARN or name could be misconfigured in the application code.

##### Q. Your SQS queue is piling up messages, but your Lambda consumer isn’t processing them. Why?
**Answer:** The Lambda function might not have an Event Source Mapping configured to the SQS queue, or its execution IAM role lacks permissions (`sqs:ReceiveMessage`, `sqs:DeleteMessage`, `sqs:GetQueueAttributes`). Another possibility is that the Lambda is throwing errors and exceeding its concurrency limit, causing messages to continually return to the queue until the DLQ (Dead Letter Queue) captures them.

##### Q. You’re getting “ThrottlingException” errors from a DynamoDB table during peak traffic. How do you handle it?
**Answer:** I’d enable auto-scaling for the table’s Read/Write Capacity Units (RCU/WCU) to gracefully handle predictable traffic. If the bursts are completely unpredictable, I would switch the table to On-Demand capacity mode to handle instant spikes without throttling.

##### Q. You enabled MFA for an IAM user, but the user can still log in without it. Why?
**Answer:** Simply configuring an MFA device doesn't enforce its use. The MFA policy might not be enforced. I’d ensure an IAM policy explicitly denying all actions unless `aws:MultiFactorAuthPresent` is true is attached to the user or their group, preventing them from doing anything in the console until MFA is validated.

##### Q. Your EKS cluster can’t scale new pods due to insufficient IPs. How do you resolve this?
**Answer:** The VPC’s or Subnet's CIDR block might be too small, exhausting available IPs. Because the AWS VPC CNI assigns a real VPC IP to every pod, IP exhaustion happens quickly. I’d enable VPC CNI’s Custom Networking to place pods in a secondary, much larger CIDR block (like a 100.64.0.0/10 CGNAT range) while keeping the worker nodes in the primary subnet.
