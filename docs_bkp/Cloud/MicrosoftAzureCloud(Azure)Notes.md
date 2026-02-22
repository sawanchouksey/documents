# Microsoft Azure Cloud (Azure) Notes

### Azure Solution Architect (AZ-305) Points to remember before giving exams

- When dividing 10 VMs across 3 Update Domains (UDs), the distribution would be:
  - UD1: 4 VMs
  - UD2: 3 VMs
  - UD3: 3 VMs
  - During maintenance, only one Update Domain is taken offline at a time. This means that in the worst-case scenario (when the largest UD is being updated), you would have:
```
10 total VMs - 4 VMs in the offline UD = 6 VMs still running
Therefore, the least number of running VMs during maintenance would be 6, not 7 as the statement suggests.
```
- When you back up a key vault object, such as a secret, key, or certificate, the backup operation will download the object as an encrypted blob. This blob can't be decrypted outside of Azure. To get usable data from this blob, you must always restore the blob into a key vault within the same Azure subscription and Azure geography.

- With `PTA(Pass-Through Authentication)`, AD security and password policies can be enforced, ensuring that authentication requests comply with the organization's security standards and policies.

- `PHS (Password Hash Synchronization)` is the correct choice for synchronizing Active Directory (AD) and Entra ID to fulfill the requirement of allowing users to access corporate machines without entering a password. PHS synchronizes password hashes from on-premises AD to Azure AD, allowing for seamless authentication without the need for users to re-enter their passwords.

- `PTA (Pass-Through Authentication)` is another correct choice for synchronizing AD and Entra ID to enable users to access corporate machines without entering a password. PTA allows for authentication requests to be passed through to on-premises AD, providing a seamless login experience for users without the need to store passwords in the cloud.

- A company has 10 Virtual Machines created in their Azure subscription. They want to ensure that an IT administrator receives an email whenever certain operations are performed on the Virtual Machine. These operations include:
  - Restarting the machine
  - Deallocating the machine
  - Powering off the machine.
  - You need to determine the minimum number of rules and action groups required in Azure Monitor to fulfill this requirement.
```
1. Three rules are required because each operation (restarting, deallocating, and powering off the machine) needs to be monitored separately to trigger the email notification to the IT administrator. Each rule will be responsible for detecting a specific operation.
2. One action group is sufficient to define the email notification settings for all three operations (restarting, deallocating, and powering off the machine). The action group can be configured to send an email to the IT administrator whenever any of the specified operations occur.
```
- `Azure Monitor` is the best fit for ensuring that IT administrators receive alerts based on critical conditions met in the application. It provides a comprehensive solution for collecting, analyzing, and acting on telemetry data from applications and infrastructure. With Azure Monitor, administrators can set up alerts based on specific metrics, logs, and events to proactively respond to critical conditions.

- `Azure Log Analytics` is a service that collects and analyzes data from various sources, including Azure resources and applications. It can be used to correlate Azure resource usage and performance data with the actual application configuration and performance data, making it the best choice for fulfilling this requirement.

- `Azure Activity Log` records all activities that occur in an Azure subscription, providing a detailed history of resource operations. By reviewing the Activity Log, you can track resource deployments, modifications, and deletions, making it a suitable choice for generating a monthly report detailing all resources deployed to the subscription.

- `Application Insights` is the best-suited Azure service for providing the testing team with the ability to view the different components of the application and see the calls being made between them. It offers real-time monitoring, analytics, and diagnostics to help track application performance, detect issues, and analyze dependencies between different components.

- `Microsoft Entra ID Protection` is a comprehensive solution that focuses on enhancing endpoint threat detection and remediation capabilities. It provides advanced security features such as identity protection, threat intelligence, and automated response mechanisms to help protect against security threats. This solution aligns well with the company's requirement to enhance its endpoint security posture.

- `Azure Synapse Analytics`, formerly known as Azure SQL Data Warehouse, is a cloud-based data warehousing service that combines big data and data warehousing capabilities. It is designed for running complex queries on large datasets and can handle both relational and non-relational data. It is the most suitable choice for hosting the data warehouse in this scenario.

- `Azure Data Factory` is a cloud-based data integration service that allows you to create, schedule, and manage data pipelines for moving and transforming data. While it can be used to orchestrate data movement from on-premises SQL Server to Azure, it is not specifically designed to host a data warehouse for analytical processing.

- `Azure Databricks` is an Apache Spark-based analytics platform optimized for Azure. While it provides capabilities for data engineering and analytics, it is not a data warehouse solution. It is more focused on data processing, machine learning, and collaborative data science workflows.

- `Azure Data Lake Gen2 Storage accounts` provide a scalable and secure data lake storage solution for big data analytics. While it can be used to store and manage large volumes of data from various sources, it is not a data warehouse service. It is more suitable for storing raw data in its native format for further processing.

- Configuring the maximum number of CPU cores ensures that the Azure SQL Managed Instance can handle the workload demands by providing the necessary processing power to execute queries and operations efficiently.

- Defining the maximum allocated storage is essential to ensure that the Azure SQL Managed Instance has enough storage capacity to store the application data and handle the workload demands without running out of storage space.

- The `SQL API in Azure Cosmos DB` is the most appropriate choice for accommodating a JSON document. It allows you to store JSON data natively and query it using SQL syntax, making it a versatile option for handling JSON documents efficiently.

- Deploying the databases to an `Azure SQL database-managed instance` will meet the requirement of supporting server-side transactions across both mydb1 and mydb2. Azure SQL database-managed instance provides a fully managed SQL Server instance in the cloud, offering features like high availability, automatic backups, and support for distributed transactions, which will enable server-side transactions across multiple databases.

- A `vCore-based Azure SQL Database` offers more flexibility and control over resources compared to a DTU-based database. It allows for scaling resources based on workload requirements and provides options for performance optimization. In this scenario, where metrics recording, analysis, minimal downtime, and database backups are critical requirements, a vCore-based Azure SQL Database is the recommended choice.

- A fixed size `DTU-based Azure SQL database` provides a set amount of resources based on the Database Transaction Units (DTUs) selected. While this option may be cost-effective for predictable workloads, it may not offer the flexibility and scalability needed for the database migration in this scenario. A vCore-based Azure SQL Database allows for more control over resources and performance scaling.

- An Azure `SQL database elastic pool` is a pool of shared resources that allows multiple databases to share and use the resources efficiently. However, in this scenario, where the database needs to be migrated to Azure with specific requirements for metrics recording, analysis, and minimal downtime, a dedicated vCore-based Azure SQL Database would be more suitable.

- Running a `SQL server on a virtual machine` in Azure would provide more control over the server environment. However, it would require more management and maintenance compared to a PaaS solution like Azure SQL Database. In this case, where PaaS deployments are preferred and database downtime needs to be minimized, a vCore-based Azure SQL Database is a better choice.

- `Always On availability groups` is a feature in Azure SQL databases that provides high availability and disaster recovery by automatically failing over to a secondary replica in case of a primary replica failure. It helps in maintaining continuous availability of your databases and is a suitable choice for ensuring high availability.

- `Active geo-replication` is a feature that allows you to replicate your databases to different regions for disaster recovery purposes. While it helps in ensuring data redundancy and disaster recovery, it is not specifically designed for maintaining high availability within a single region.

- `Auto-failover groups` is a feature in Azure SQL databases that automatically triggers failover to a secondary replica in case of a primary replica failure. While it helps in ensuring automatic failover and continuous availability, it is not as comprehensive as Always On availability groups in terms of high availability for your databases.

- `Auto failover groups` can have a potential data loss of up to 5 seconds during failover. This means that any transactions that occurred within the last 5 seconds before the failover may not be replicated to the secondary server, leading to potential data loss.

- `Long-term backup retention` is a feature that allows you to store backups of your databases for an extended period. While it is important for data protection and compliance, it does not directly contribute to maintaining high availability for your databases in case of failures.

- The solution suffices because creating an Azure Recovery Services vault and installing the Azure Backup agent to schedule backups ensures that data loss is prevented in case the file server fails. The Azure Backup agent will regularly back up the data from the file server to the Recovery Services vault, providing a reliable backup and recovery solution.

- While creating a Recovery Services vault and configuring a backup using Windows Server Backup is a good step towards data protection, it's insufficient to prevent data loss in case the file server fails. The Windows Server Backup helps you create local backups and store them locally, on the volume or the shared network folder. Additional measures, such as implementing a high-availability solution or using redundant storage options, are necessary to ensure comprehensive data protection and prevent potential data loss scenarios.

- Server Level IP Firewall rules in Azure SQL Database allow you to control access to the database based on specific IP addresses or ranges. By configuring these rules at the server level, you can restrict access to only certain workstations with static Public IP addresses.

- we can use the Azure Migrate service to migrate Hyper-V virtual machines to Azure. Azure Migrate provides a centralized hub for discovering, assessing, and migrating on-premises servers, apps, and data to Azure.

- An `Azure Event Grid` trigger is essential in the Logic App to monitor and respond to events related to the virtual machine in the specified resource group. It acts as the starting point for the Logic App and triggers the workflow when the settings of the virtual machine are modified.

- `Network Security Groups (NSGs)` with service tags allow you to define security rules based on predefined Azure service tags. By configuring NSGs with service tags, you can restrict traffic to only come from Azure Front Door and implement load balancing across virtual machines. This option aligns with the requirement provided in the question.

- `Azure Container Registry (Premium SKU)` provides advanced features such as geo-replication, which allows for automatic replication of container images across multiple Azure regions. This makes it the ideal choice for the company's requirement of deploying applications on multiple AKS clusters in different Azure regions while ensuring that updated container images are replicated across all clusters.

- `Azure Container Registry (Basic SKU)` offers a basic container registry service with limited features compared to the Premium SKU. It does not include the functionality needed to automatically replicate updated container images across multiple AKS clusters, making it unsuitable for this requirement.

- `Azure Container Registry (Standard SKU)` provides a basic container registry service without the advanced features required for automatic replication of container images across multiple AKS clusters. It does not offer the necessary capabilities for this specific requirement.

- While a blob is in the archive access tier, it's considered offline and can't be read or modified. To read or modify data in an archived blob, you must first rehydrate the blob to an online tier, either the hot or cool tier. There are two options for rehydrating a blob that is stored in the archive tier.

- Azure Databricks is a fully managed Apache Spark-based analytics platform optimized for Azure. It provides an interactive workspace for data engineers to collaborate and develop notebooks in Scala, R, and Python for data analysis tasks. Azure Databricks is the ideal choice for implementing a managed Spark cluster for analyzing data stored in the SQL data warehouse.

- Defining the maximum of Database Transaction Units (DTUs) is crucial for ensuring effective scaling of the database to meet workload demands. DTUs are a measure of the performance and resources allocated to the database, and setting a maximum limit helps in dynamically scaling resources based on workload requirements.

- Azure Storage account can be used to store backups created by Automated Backup for virtual machines. It allows for encryption of the backups at rest, meets the recovery point objective of 15 minutes, and supports a retention period of 30 days. This choice aligns with all the specified requirements for the backup process.

- Assigning the Azure Web App to a Basic App Service Plan allows for auto-scaling based on demand. The Basic plan supports auto-scaling, which means the application's capacity can adjust dynamically according to the incoming traffic without manual intervention. This helps in optimizing costs by scaling up or down as needed.

- Multitenant Azure Logic Apps has a default limit on the number of actions that run every 5 minutes. To raise the default value to the maximum, you can enable high throughput mode. Alternatively, you can distribute the workload across multiple logic apps and workflows rather than relying on a single logic app and workflow.

- Creating a new node pool is the correct first step to take in order to deploy a new containerized application to specific nodes with specific sizes. By creating a new node pool, you can define the size and number of nodes that meet the requirements of the new application, ensuring that it runs on four nodes of size "DS3 v2" as specified.

- An Internal Azure Standard Load Balancer is the recommended choice as it supports port forwarding, HTTPS health probes, and has an availability set as the backend pool. It is suitable for load balancing traffic between the web front end and the application tier within the Azure environment while meeting all the specified requirements.

- Enabling system-assigned Managed Identities in App Services allows the web app to authenticate securely with other Azure services without needing to store credentials in the code. By granting permissions to access Key Vault secrets, the web app can retrieve the database connection string and password as needed, following the principle of least privilege and avoiding hardcoding passwords.

- Azure Synapse Analytics service, formerly known as Azure SQL Data Warehouse, is a cloud-based analytics service that combines big data and data warehousing capabilities. It allows you to analyze large volumes of data and provides integration with Azure Data Lake Storage and Azure Data Factory. Given the need for a data warehouse and big data analytics system in the desired target state, Azure Synapse Analytics service is the most appropriate choice.

- Traffic Manager is a DNS-based traffic management service that can help with distributing user traffic to specific endpoints based on various routing methods. Application Insights is an application performance monitoring tool that can provide detailed insights into the performance of your application. Together, these components can help meet the disaster recovery, application monitoring, and geographic load balancing requirements outlined by the business.

- Functions, specifically Azure Functions, are a serverless compute service that allows you to run event-triggered code without managing infrastructure. They are ideal for short-lived processes, responding to database changes, and running scheduled tasks, making them a perfect fit for the Gaming Company's workload requirements.

- Azure Migrate is the correct choice as it is specifically designed to assess on-premises infrastructure and provide insights into the TCO of the migration, as well as recommendations for the appropriate size of Virtual Machines required for Azure. Azure Database Migration Service complements this by focusing on migrating databases to Azure, ensuring a comprehensive migration strategy for the university.

- `Kubenet` is a simple and cost-effective networking plugin for Azure Kubernetes Service. It allows pods to receive IP addresses from a different address space than the node pool's subnet, helping to avoid IPv4 exhaustion. Additionally, Kubenet supports NAT (Network Address Translation) between workloads deployed in pods and other Azure components, meeting the security consultants' requirements.

- `Microsoft Network Routing`:
This option routes traffic between your Azure Storage account and other Azure services through Microsoft's internal network backbone.
  - Key points:
    - Generally provides better performance and lower latency
    - Traffic stays within Microsoft's network as much as possible
    - Can be more secure as it minimizes exposure to the public internet
    - Typically preferred for communication between Azure services

- `Internet Routing`:
This option routes traffic over the public internet.
  - Key points:
    - Uses public IP addresses for communication
    - May have higher latency compared to Microsoft Network Routing
    - Can be useful when you need to access storage from outside Azure
    - Might be necessary for certain scenarios or legacy applications

- Azure Cosmos DB offers multiple APIs and corresponding endpoints. Here's a concise overview:
	1. Core (NoSQL) API:
	   - Default API
	   - Uses SQL-like query language
	   - Endpoint: https://<account-name>.documents.azure.com

	2. MongoDB API:
	   - Compatible with MongoDB wire protocol
	   - Endpoint: https://<account-name>.mongo.cosmos.azure.com

	3. Cassandra API:
	   - Compatible with Apache Cassandra
	   - Endpoint: https://<account-name>.cassandra.cosmos.azure.com

	4. Gremlin (Graph) API:
	   - For graph databases
	   - Endpoint: https://<account-name>.gremlin.cosmos.azure.com

	5. Table API:
	   - Compatible with Azure Table Storage
	   - Endpoint: https://<account-name>.table.cosmos.azure.com

	6. PostgreSQL API
	   - Compatible with PostgreSQL 12 and later
	   - Endpoint: <server-name>.postgres.cosmos.azure.com

- `Object replication` in Azure Storage is a feature that allows you to automatically copy blobs from one storage account to another. Here's a concise.
  - Key points:
    1. Asynchronous copying of block blobs between source and destination accounts
    2. Supports copying between general-purpose v2 or premium block blob accounts
    3. Can replicate within the same region or across regions
    4. Uses rules to define which blobs to replicate and where
  - Benefits:
    - Reduced latency for read requests
    - Improved data redundancy
    - Optimized data distribution for analytics
  - Setup involves:
    1. Configuring source and destination accounts
    2. Setting up replication rules
    3. Enabling versioning on both accounts
  - Considerations:
    - Only new and updated blobs are replicated after setup
    - Deletion of source blobs doesn't propagate to destination
    - Supports one-way replication only

### Azure conatiner instnace tutoria

```
https://learn.microsoft.com/en-us/azure/container-instances/container-instances-quickstart-portal
```

### Create Tutorilas by Visulize way

```
https://www.iorad.com/
```

### download & connect to kubectl in local sytem

```
https://storage.googleapis.com/kubernetes-release/release/v1.18.0/bin/windows/amd64/kubectl.exe
```

### kubernates access to for multiples cluster

```
https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/
```

### ARM template

https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/syntax

### ARM template format

{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "",
  "apiProfile": "",
  "parameters": {  },
  "variables": {  },
  "functions": [  ],
  "resources": [  ],
  "outputs": {  }
}

### setup kali gui in azure VM

```
https://cloudyhappypeople.com/2018/12/23/setting-up-a-kali-linux-machine-in-azure/
```

### computer vision api Azure AI

```
http://aidemos.microsoft.com/computer-vision
```

### video indexer api Azure AI

```
http://aidemos.microsoft.com/video-indexer
```

### documentation for ALL conginitive services API

```
http://centralus.dev.cognitive.microsoft.com/docs/services
```

### draw chart and cloud diagram

```
http://app.diagrams.net/ or http://draw.io/
http://lucid.app/documents#/dashboard?folder_id=home
```

### configure Azure Monitor & Application Insight for Java Application

```
https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-spring-boot
```

### azure naming convention for resources

- **aks(Resource Type)-osms(application name)-prod(Environment)-eastus(region)-001(instance count)**

```
https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming
```

### enable private cluster

```
https://docs.microsoft.com/en-us/azure/aks/command-invoke
```

### Powershell some important command Az-104

```
https://vbcloudboy.medium.com/which-powershell-commands-i-should-know-for-az-104-certification-c22a45fdd8f6
```

### microst free training and Certifcation

```
https://events.microsoft.com/en-us/mvtd-azure?language=English&clientTimeZone=1&startTime=08:00&endTime=17:00
```

### azure PT testing by Azure Load testing services

```
https://docs.microsoft.com/en-us/azure/load-testing/tutorial-identify-bottlenecks-azure-portal?wt.mc_id=azureportal_loadtesting_inproduct_overview
```

### subnet creator

```
https://network00.com/NetworkTools/IPv4SubnetCreator/
```

### azure application gateway with ingress controller

```
https://hovermind.com/azure-kubernetes-service/application-gateway-ingress-controller.html#creating-a-basic-ingress
```

### subnet calculator

```
https://www.site24x7.com/tools/ipv4-subnetcalculator.html
```

### run java application in azure batch account

```
https://linuxtut.com/run-java-application-in-azure-batch-47daa/
```

### Azure Database for PostgreSQL backup with long-term retention

```
https://docs.microsoft.com/en-us/azure/backup/backup-azure-database-postgresql
```

### PowerShell : Available in Windows, Linux & Mac OS

```
Powershell - https://learn.microsoft.com/en-us/powershell/module/?view=powershell-7.2
Azure Cli  - https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest
```

### uptime and downtime clculation w.r.t given SLA

```
https://uptime.is/
```

### pricing calculator in azure

```
https://azure.microsoft.com/en-us/pricing/calculator/
```

### control nginx for access outisde whitelist ip from get this

```
https://ipinfo.io/ip
https://whatismyipaddress.com/
```

### To check the latency of Azure data centre at specific region

```
https://www.azurespeed.com/Azure/Latency
```

### Virtual Machine series

```
https://azure.microsoft.com/en-in/pricing/details/virtual-machines/series/
```

### azure archietecture centre

```
https://docs.microsoft.com/en-us/azure/architecture/
```

### Azure diagram icons

```
http://docs.microsoft.com/en-us/azure/architecture/icons/
```

### CIDR calculator

```
http://www.ipaddressguide.com/cidr
```

### DNS configuration patterns for Azure Database for PostgreSQL – Flexible Server

```
http://azureaggregator.wordpress.com/2021/07/23/dns-configuration-patterns-for-azure-database-for-postgresql-flexible-server/
```

### nginx-ingress yaml helm

```
https://github.com/kubernetes/ingress-nginx/blob/main/deploy/static/provider/cloud/deploy.yaml
```

### az login method for cli script

```
https://learn.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli?toc=%2Fazure%2Fazure-resource-manager%2Ftoc.json&view=azure-cli-latest
```

### VM pricing details

```
https://azure.microsoft.com/en-in/pricing/details/virtual-machines/linux/
```

### shared Disk

- Enabled Shared Disk option in Disk-->configuration-->Max shres : 1,2,3 etc.

### Internal LoadBalancer vs External LoadBalancer

1. **Internal LoadBalancer**
   
   - No public Ip attached and Run exit inside the subnet

2. **External LoadBalancer**
   
   - Public IP attched and No restriction on subnet

### Cognitive services in azure for AI and ML

1. **DECISION**
   
   - Content Moderator
   
   - Check text, images or videos for offensive or undesirable content

2. **LANGUAGE**
   
   - Language Understanding (LUIS)
     
     - Extract meaning from natural language
   
   - Language
     
     - Detect sentiment, key phrases, entities and human language type in text
   
   - Translator
     
       -Translate text in near real-time

3. **SPEECH**
   
   - Speech-to-text
     
     - Enable real-time transcription of audio streams into text
   
   - Text-to-speech
     
     - Enable your applications, tools, or devices to convert text into human-like synthesized speech
   
   - Speech Translation
     
     - Enable real-time, multi-language speech-to-speech and speech-to-text translation of audio streams
   
   - All Speech documentation
     
     - Speaker recognition, custom keywords, intent recognition, and more

4. **VISION**
   
   - Computer Vision
     
     - Analyze images and recognize text, objects, and more
   
   - Face
     
     - Recognize people and their attributes in an image
   
   - Custom Vision
     
     - Build, deploy, and improve your own image classifiers

### Availablity Set VMs

- **Fault Domain**  : define the group of VM that share a common power source or network switched or hardware component.

- **Update Domain** : define the group of VM that are going to be patched/maintained/rebooted at same time.

| Fault Domain  0     | Fault Domain  1     | Fault Domain  2     |
| ------------------- | ------------------- | ------------------- |
| **Update Domain 0** |                     |                     |
|                     | **Update Domain 1** |                     |
|                     | **Update Domain 2** |                     |
|                     |                     | **Update Domain 3** |
|                     |                     | **Update Domain 4** |

### Virtual Machine Scaling Set

- **Horizontal Scaling** increases the number of instances within Azure Virtual Machine Scale Sets.

- **Vertical Scaling** increases the capacity of existing instances within Azure Virtual Machine Scale Sets.

### Migration Services end to end migrate

| Services Types | Own Data Center                    | Azure Cloud Service                                              |
| -------------- | ---------------------------------- | ---------------------------------------------------------------- |
| Compute        | Physical/Virtualize Hardware       | Virtual Machine                                                  |
| Storage        | SAN, NAS, DAS                      | Persistant disk,Azure Cloud Storage                              |
| Network        | MPLN, VPN, DNS, H/W Load Balancing | LoadBalancer,ApplicationGateway,TrafficManager,FrontDoor&CDN,VPN |
| Secuirty       | Firewall, Route Table etc.         | Firewall, Encryption, NetworkSecurityGroup etc.                  |
| Identity       | Active Directory, LDAP             | IAM, Azure AD                                                    |
| Management     | Configuration Service, CICD tools  |                                                                  |

### Types of Storage Account

| Tier of Storage Account | Type of Storage Account | Description of Storage Account                                                                                                                                                 |
| ----------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Standard**            | Genral-Purpose v2       | For utility data transfer store etc.                                                                                                                                           |
|                         | General Purpose V1      | For utility data transfer store etc. No object level access tier is available. NO life Cycle Management option is available in storage account.                                |
|                         | Blob Storage            | Only for blob level data storage supported no table,Queue and Fileshare.                                                                                                       |
| **Premium**             | Block Blob              | Only for blob level data storage supported no table,Queue and Fileshare. Premium container Blobs for low latency and better performance. Archive Access tier is not available. |
|                         | Page Blob               | Only for blob level data storage supported no table,Queue and Fileshare. For storing .VHD(Virtual hard Disk) file which used in VM.                                            |
|                         | File Share              | Only for FileShare level data storage supported no table,Queue and Blob Container. Premium files share for low latency and better performance.                                 |

### Enable Data Lake Storage Option in Storage Account while creating

- **DataLake Gen 2**
  
  - Created above Storage account on Blob storage Layer for store Peta tera byte of data.

### Azure AD RBAC Role assigned for Specific resources like storage account

### Disaster Recovery and Business continuity

- **RTO(Recovery Time Objective)**
  
  - The time to complete recovery or restore.

- **RTO(Recovery Time Objective)**
  
  - The Amount of acceptable data loss if a recovery is needed. 

### Advantages of batch processing

1. You can process large volumes of data at a time.

2. The jobs can run in the night during non-peak hours.

### Disadvantages of batch processing

1. There is a delay before you get the results.

2. The batch job that processes the results could take hours to complete.

3. If the batch job fails for any reason, you don’t get the data in the end. You could end up in partial data in the analytical system.

4. You might need to delete the data in the analytical system and then run the batch job again.

### SQL server in VM server

- Microsoft recommends some performance guidelines when trying to host a SQL Server on an Azure Virtual Machine, especially in production based environments.

- Choose VM sizes that offer 4 or more vCPUs.

- Use premium SSDs for getting the best performance.

- Use at least 2 premium SSD disks, one for the log file and the other for the data file.

- Use Standard HDDs and SSDs for development and test workloads.

- Ensure to configure ReadOnly cache for the data files. Ensure no cache is configured for the log file.

- If you need less than 1 ms storage latencies , then consider using Ultra Disks.

### databrics

- It makes use of Apache Spark to provide a Unified Analytical Plateform.

- It help to provision Infra and all pre-requisite for Apache Spark in Managed Service.

### Azure KeyVault Backup Recovery

- When you take a backup of an object in a key vault , you can restore it to another key vault in the same subscription and the same geography.

### Azure Front door

- It is basically route traffic basis on Latency which has minimum latency it will route traffic there

### Azure logic app

- It is used to define Workflow in Azure without any coding knowledge instead other services like Azure autmation account and Azure Function required Coding skills to design workflow.

### Data Analytics

1. **Descriptive Analysis** 
   
   - This helps to answer questions on what happened. This can be done based on historical data.
   
   - This technique can be used to summarize large datasets to describe outcomes to stakeholders.
   
   - Here you can use KPI – Key Performance indicators.
   
   - These can be used to track the success of failure of key objectives.

2. **Diagnostics Analysis** 
   
   - This helps to answers questions on why it happened.
   
   - Trying to identify anomalies in data.
   
   - Try to dig deeper into the root cause of the issue.

3. **Predictive Analysis** 
   
   - This helps to answer questions on what can happen in the future. 
   
   - This is helpful for business to make decisions about the future.

4. **Prescriptive Analysis** 
   
   - This can help to answer questions on what actions can be taken to achieve a goal or target.

5. **Cognitive Analysis** 
   
   - This is where you try to analyze the current situation based on the data you have. 
   
   - If you have learnt anything new, then that is added to the data set that you already have.

### Azure Data Factory

- This is cloud based ETL tool.(Extract, Transform,Load=ETL)

- Hera you can create data-driven workflow.

- The workflow help for orchestrate data movement.
  
  1. **ADF Processing**
     
     - The first step is to connect to the required data sources.
     
     - The next step is to ingest the data from the source.
     
     - You can then transform the data in the pipeline if required.
     
     - You can then publish the data onto a destination –Azure Data Warehouse, Azure SQL Database , Azure Cosmos DB.
     
     - You can also monitor the pipeline as it is running.
  
  2. **ADF Components**
     
     - **Linked Service** – This enables you to ingest data from a data source. The Linked Service can create the required compute resources to take the data from the data source.
     
     - **Datasets**–This represents the data structure within the data store that is being referenced by the Linked Service object.
     
     - **Activity** –This contains the actual transformation logic. You can also have simple Copy Activities to copy the data from the source to the destination.

```
AzurePortal-->ADF-->Author&Monitor-->Open ADF Workspace-->Select the template(create pipeline,create data flow,create pipeline from,copy data,configure SSIS,setup the code repository) you want to use-->copy data-->[properties :Task Name,Source : connection,Dataset,Destnation :connection,Dataset,Setting,Summary,deployment]-->Finish-->Monitor
```

### Azure Synapse Analytics

- You can use this service to host your data warehouse.

- You can also perform Big Data Analytics using this service.

- When it comes to allocating resources, they are allocated via DWU’s.

- These are Data Warehouse Units – This unit is a combination of CPU, Memory and IO.

- When you allocate the required resources to the Synapse resource, you choose the amount of DWU’s you want to allocate.

- The storage for the data warehouse is allocated separately.

- For Gen2 , for columnstore tables, you get unlimited storage. The storage is allocated automatically.

- You also have the ability to pause and resume the Synapse pool which hosts your data warehouse.

### Batch Processing

- Here data is collected over a period of time.

- The data is then processed as a batch job.

- For example , for an e-commerce application, all of the purchases that were carried out during the day will be collected.

- That data will then be submitted to a batch processing system.

- That system will then process the data in the night.

- The data is then stored in the analytical system

### Data ingestion and processing

- Companies normally want to analyze data that is available via their entire application landscape.

- For example, they want to get a better idea on what customers want when they visit their website.

- Normally a lot of the data would initially be in raw format.

- And then the data needs to be transformed into a more meaningful form for analysis.
1. **Wrangling**
   - This is the process of transformation of raw data into a more use format for analysis.
   - This normally involves writing code that would be used to filter, clean, combine and aggregate data from various sources.

### When considering transformation and processing, there are two approaches.

1. **ETL – Extract, Transform and Load**
   
   - Here the data is retrieved, transformed and then saved onto the destination.
   - This process can be used for basic data cleaning tasks, reformatting of data wherever required.
   - Here you can filter on data before it is load onto the destination.

2. **ELT – Extract, Load and Transform**
   
   - Here the data is transformed after it is loaded into the destination.
   - This is normally used for more complex models and when periodic batch processing is desired.

### Network Wathcer Tools Services

- IP Flow verufy
- NSG diagonistic
- Next Hop
- Effective Security Rule
- VPN troublehshoot
- Effective Secuirty rule
- PAcket Capture
- Connection Troubleshoot

### #Azure OpenAI references like

- https://learn.microsoft.com/en-us/azure/ai-services/openai/
- https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
- https://azure.microsoft.com/en-in/pricing/details/cognitive-services/openai-service/#overview
- https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits

### Service end point

- It is secured communication between Azure resources.
- It works with supported Azure Services only. And integrate within Vnet configuration.

### Azure AD Access review

- To check the specific user access dashboard and access overview

### Identity protection

- To check user data and their security assesment analyse whether user at risk,sign-in risk security breach etc

### Azure alert monitor

- Each condition have "1 rule" but "Multiple alert" can be integrate with "1 Action group"

### identity Goverance - Access Review

- for the user and group on basis of user group recommendation

### MS defender for cloud

- This is security posture management and threat protection tool

- JIT access in VM : Security Score

### conditional Access

- It gives you ability to enforce access requirements when specific condition occur. i.e.

| Condition                                   | Control                                                                 |
| ------------------------------------------- | ----------------------------------------------------------------------- |
| When users in the 'Managers' grous sign-in. | They are required to be on an intune complaint or domain joined devices |
| When any user is outside the company n/w.   | They are required to sign in MFA.                                       |

### Azure Sentinel

- This is a cloud service that provides a solution for SEIM ( Security Information Event Management) and SOAR ( Security Orchestration Automated Response).

- Collection of data – Here you can collect data across all users, devices, applications and your infrastructure. The infrastructure could be located on-premise and on the cloud.

- It helps to detect undetected threats.

- It helps to hunt for suspicious activities at scale.

- It helps to respond to incident rapidly.

- Once you start using Azure Sentinel, you can start collecting data using a variety of connectors.

- You have connectors for a variety of Microsoft products and other third-party products as well.

- You can then use in-built workbooks to get more insights on the collected data.
  
  ```
  Azure Portal-->Create Log Analytics Workspace-->Azure Sentinel-->New-->Select Workspace-->Add-->Add Connector-->select Specific connector(AWS,AAD)-->Open connecto page-->Select Instruction and Configuration-->Apply Changes
  ```

### Azure Cost Optimization Technique

```
https://techcommunity.microsoft.com/t5/fasttrack-for-azure/the-azure-finops-guide/ba-p/3704132
```

### Azure Service fabric

- **Azure Service fabric runtime = Services + Local Disk Data**

- It is conatiner orchestron service with lot of features

- It can be deployed in Dev Machine, Azure , On-premise Data centre ,Others cloud etc. 

- Copies are data are made to ensure services are more reliable

- You can use Reliable Service Framework to Develop the Services

- You can develop both stateless and statefull services

- It has facility to automatically detect and restart the service

- It can automatically discover services and route message between services.

- Application can be deployed as process or conatiner.

- Different components of Service Fabric
  
  - **Reliable Services** – This is a framework that can be used to write services that integrate with the Service Fabric platform.
      You can build a stateless Reliable service wherein the state is written to an external data store such as Azure Table storage.
      Or you can have a stateful Reliable service where the state is persisted to a Reliable Collections.
  - **Reliable Actors** – This is a framework that implements a Virtual Actor pattern.

### Use Azure open AI Service

- Create Azure OpenAI Service. 

- Launch Azure OpenAI Studio in new Tab after azure open AI services created successfully.

- Azure OpenAI Studio [ Use + Test + Customize + Deploy Model] by web interface for end users.
  
  ```
  Lets deploy a Text Model Azure OpenAI Studio-->Management-->Deployment-->[+]Create New Deployment-->Deploy Model Windows Appears [Select a Model:gpt-35turbo | Model version:Auto-update to default | Deployment Name: My_text_demo_model_01 | Create]
  ```

- Access the Model from the Playground section and test it and fine tune it

- Access the OpenAI model from Rest API in postman

- https://{resource}.openai.azure.com/openai/deployments/{deployment}/chat/completions?api-version=2023-03-15-preview

- Playground-->Chat Session Window-->Select the View Code-->[contain Code + Endpoint + Key]

- copy the endpoint-->go to postman-->paste in the URL section-->Method POST-->[URL : Click on Headers-->Add open AI keys--[api-key:paste the key value copy from playground chat session]-->Click on Body-->Click on raw-->
  
  ```
  [
    {
  "messages":[
    {
        "role": "system",
        "content": "You are a Data Science Tutor"
    },
    {
        "role": "user",
        "content": "Explain AI Model to a 4th grader"
    }
  ],
  "temperature": 0.7,        # How realistic your model behave ideal value must be between 0.5 to 0.75
  "top_p": 0.95,
  "frequency_penalty": 0,
  "presence_penalty": 0,
  "max_tokens": 800,         # Number of token or response size
  "stop": null               # which token or string after that it should stop responding or generating Max 4 values we can pass i.e. test
                             # As soon as it hit any of sequences mentioned It will stop generating or responding 
  }
  ]
  ```

- Access Model From Code or Programming

- Copy the code from Azure OpenAI Studio Playground Chat Session i.e.

- create deployment_model_name.py
  
  ```
  import os
  from openai import AzureOpenAI
  client = AzureOpenAI(
    azure_endpoint="https://neyahopenai.openai.azure.com/",
    api_version="2023-06-01-preview",
    api_key=os.environ["OPENAI_API_KEY"]
  )
  response = client.chat.completions.create(
    model="text_demo",
    messages=[{"role": "system", "content": "You are a AI Tutor"},
              {"role": "user", "content": "What is AI"}],
    temperature=0.7,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
  )
  print(response)
  print(response.choices[0].message.content)
  ```

- Deploy OpenAI Model in Web App in Azure
  
  ```
  Azure OpenAI Studio-->Chat Playground-->Click on [Deploy to]-->Select [A new web app]-->It will open 'Deploy to Web App window'-->[Create new web app | Name | Subscription | Resource group | Location | Pricing Plan | Deploy]
  ```

- Create and use content filter of Our Model
  
  ```
  AzureOpenAIStudio-->Management-->Content Filter-->Create Customized Content filter--> [ Create custom configuration name : My-Content-filter-01 | Set Severity Level : Red | Save ]
  ```

- update model to use our content filter
  
  ```
  AzureOpenAIStudio-->Management-->Edit Deployment-->Advanced option-->[Content Filter : My-Content-filter-01]-->save and close
  ```

### Set Header in application gateway

- step-1
  
  ```
  azure portal-->application-gateway-->setting-->Rewrites-->[+]Rewrite set-->[ Name Association : Name | Routing rules|Paths | Rewrite rule configuration: [+] Add rewrite rule | Do : Configure action [ Rewrite type : Request Header | Action type : set | Header name : Custom header | Custom Header : x-rgister-id | Header value : {var_add_x_forwarded_for_proxy} | OK ]]
  ```

- step-2

- add rewrite rule in ingress file `ingress-route.yaml`
  
  ```
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
  name: agic-ingress-route
  annotations:
    kubernetes.io/ingress.class: azure/application-gateway
    appgw.ingress.kubernetes.io/rewrite-rule-set: rewrite
  spec:
  rules:
  - http:
      paths:
      - path: /test-poc/*
        pathType: Prefix
        backend:
          service:
            name: test-poc-services
            port:
              number: 80
  ```

- step-3

- update the variable and value in deployment.yaml file
  
  ```
  apiVersion: apps/v1
  kind: Deployment
  metadata:
  name: test-poc-services
  spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-poc-services
  template:
    metadata:
      labels:
        app: test-poc-services
    spec:
      containers:      
      - name: test-poc-services
        image: azureimages.azurecr.io/testpoc:example
        imagePullPolicy: Always 
        env:
        - name: x-register-id
          value: "687"
        resources:
          requests:
            cpu: 500m
            memory: 1024Mi
          limits:
            cpu: 1000m
            memory: 2050Mi
        ports:
        - containerPort: 8080
      imagePullSecrets:
      - name: imagepull
  ```

- step-4

- redeploy deployment.yaml and ingress-route.yaml
  
  ```
  kubectl apply -f deployment.yaml -f ingress-route.yaml
  ```

### clear docker images with none tag

```
docker images -a | grep none | awk '{ print $3; }' | xargs docker rmi --force
```

### public IP of machine

```
curl -s https://api.ipify.org -w "\n"
```

### create Azure Synapse Analytical

- go to azure portal

- search and create Azure Synapse Analytic

- fill up the information [ Subscription | Resource Group | Work Space Name | Region | Select and Create Data Lake Storage Gen2 Storage account | File System name | SQL Server admin login | SQL password | Confirm Password | Review + Create ]

- Create SQL pool for data Ware house processing

- Open Synapse studio

- Action Items and Windows in `Azure Synpase Studio`
  
  1. **Data**: To connect data pool i.e SQL server pool. >csv file dont have datatypes everything treated as varchar(string) only.
  2. **Develop**: It is an Integrated Development Environment for Azure Synapse which include functionalities like [+] SQL Script | Notebook | Data Flow (ETL)| Apache Spark Job Defination | Browse Gallery | Import
  3. **Integrate**: It is used to create data pipeline.
  4. **Monitor**: Monitor the pipeline and data processing.

- Loading data into table by "COPY" command
  
  ```
  COPY INTO logdata FROM 'https://appdatalake7000.blob.core.windows.net/data/Log.csv'
  WITH
  (
  FIRSTROW=2
  )
  COPY INTO [logdata] FROM 'https://appdatalake7000.blob.core.windows.net/data/parquet/*.parquet'
  WITH
  (
  FILE_TYPE='PARQUET',
  CREDENTIAL=(IDENTITY= 'Shared Access Signature', SECRET='sv=2020-02-10&ss=b&srt=sco&sp=rl&se=2021-07-01T16:07:07Z&st=2021-07-01T08:07:07Z&spr=https&sig=j%2BtdThwbGU83Ol3LyyLHbFZQTMyGauCVtfKbUuUCkLM%3D')
  )
  ```

- Loading data using "POLYBASE"
  
  ```
  CREATE LOGIN user_load WITH PASSWORD = 'Azure@123';
  CREATE USER user_load FOR LOGIN user_load;
  GRANT ADMINISTER DATABASE BULK OPERATIONS TO user_load;
  GRANT CREATE TABLE TO user_load;
  GRANT ALTER ON SCHEMA::dbo TO user_load;
  CREATE WORKLOAD GROUP DataLoads
  WITH ( 
    MIN_PERCENTAGE_RESOURCE = 100
    ,CAP_PERCENTAGE_RESOURCE = 100
    ,REQUEST_MIN_RESOURCE_GRANT_PERCENT = 100
    );
  CREATE WORKLOAD CLASSIFIER [ELTLogin]
  WITH (
        WORKLOAD_GROUP = 'DataLoads'
    ,MEMBERNAME = 'user_load'
  );
  ```

- Here we are following the same process of creating an external table
  
  ```
  CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'P@ssw0rd@123';
  ```

- if you want to see existing database scoped credentials
  
  ```
  SELECT * FROM sys.database_scoped_credentials
  CREATE DATABASE SCOPED CREDENTIAL AzureStorageCredential
  WITH
  IDENTITY = 'appdatalake7000',
  SECRET = 'VqJnhlUibasTfhSuAxkgIgY97GjRzHL9VNOPkjD8y+KYzl1LSDCflF6LXlrezAYKL3Mf1buLdZoJXa/38BXLYA==';
  ```

- If you want to see the external data sources
  
  ```
  SELECT * FROM sys.external_data_sources 
  CREATE EXTERNAL DATA SOURCE log_data
  WITH (    LOCATION   = 'abfss://data@appdatalake7000.dfs.core.windows.net',
          CREDENTIAL = AzureStorageCredential,
          TYPE = HADOOP
  )
  ```

- If you want to see the external file formats
  
  ```
  SELECT * FROM sys.external_file_formats
  CREATE EXTERNAL FILE FORMAT parquetfile  
  WITH (  
    FORMAT_TYPE = PARQUET,  
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'  
  );
  ```

- Drop the existing logdata table
  
  ```
  DROP TABLE [logdata]
  ```

- Create the external table as the admin user
  
  ```
  CREATE EXTERNAL TABLE [logdata_external]
  (
  [Id] [int] NULL,
    [Correlationid] [varchar](200) NULL,
    [Operationname] [varchar](200) NULL,
    [Status] [varchar](100) NULL,
    [Eventcategory] [varchar](100) NULL,
    [Level] [varchar](100) NULL,
    [Time] [datetime] NULL,
    [Subscription] [varchar](200) NULL,
    [Eventinitiatedby] [varchar](1000) NULL,
    [Resourcetype] [varchar](1000) NULL,
    [Resourcegroup] [varchar](1000) NULL
  )
  WITH (
  LOCATION = '/parquet/',
    DATA_SOURCE = log_data,  
    FILE_FORMAT = parquetfile
  )
  ```

- Now create a normal table by selecting all of the data from the external table
  
  ```
  CREATE TABLE [logdata]
  WITH
  (
  DISTRIBUTION = ROUND_ROBIN,
  CLUSTERED INDEX (id)   
  )
  AS
  SELECT  *
  FROM  [logdata_external];
  ```

- Load data using `Azure Synapse`
  
  - Open Azure Synapse Studio
  - Click on Data then Workspace click [+]
  - Click on 'connect to external site'
  - Select external data source 'Azure Data Lake Storage Gen2'
  - Select Linked Click on 'Azure Data Lake Storage Gen2 Account'
  - Select 'blob container' having Data
  - Right click on file Log.csv
  - Click on 'New SQL Script' then click on 'Bulk Load'
  - Fill Information in 'Bulk Load' [ source Storage | File Type | Field terminator | Row Terminator | First Row: Row Number '1' to exclude for Header | Select target SQL pool | Select Target Table ]

- Building a `Fact Table`
  
  - It is usually large in size.
  
  - The fact table contain primary key used in dimensional table
  
  - you can have NULL value in fact table but don't have NULL values for the key in the fact table that will be used for joins in dimensional table.
  
  - Lets first create a view
    
    ```
    CREATE VIEW [Sales_Fact_View]
    AS
    SELECT dt.[ProductID],dt.[SalesOrderID],dt.[OrderQty],dt.[UnitPrice],hd.[OrderDate],hd.[CustomerID],hd.[TaxAmt]
    FROM [Sales].[SalesOrderDetail] dt
    LEFT JOIN [Sales].[SalesOrderHeader] hd
    ON dt.[SalesOrderID]=hd.[SalesOrderID]
    ```
  
  - Then we will create the Sales Fact table from the view
    
    ```
    SELECT [ProductID],[SalesOrderID],[CustomerID],[OrderQty],[UnitPrice],[OrderDate],[TaxAmt]
    INTO SalesFact
    FROM Sales_Fact_View
    ```

- Building a `dimension table`
  
  - Lets build a view for the customers
    
    ```
    CREATE VIEW Customer_view 
    AS
    SELECT ct.[CustomerID],ct.[StoreID],st.[BusinessEntityID],st.[Name]  as StoreName
    FROM [Sales].[Customer] as ct
    LEFT JOIN [Sales].[Store] as st 
    ON ct.[StoreID]=st.[BusinessEntityID]
    WHERE  st.[BusinessEntityID] IS NOT NULL
    ```
  
  - Lets create a customer dimension table
    
    ```
    SELECT [CustomerID],[StoreID],[BusinessEntityID],StoreName
    INTO DimCustomer
    FROM Customer_view 
    ```
  
  - Lets build a view for the products
    
    ```
    CREATE VIEW Product_view 
    AS
    SELECT prod.[ProductID],prod.[Name] as ProductName,prod.[SafetyStockLevel],model.[ProductModelID],model.[Name] as ProductModelName,category.[ProductSubcategoryID],category.[Name] AS ProductSubCategoryName
    FROM [Production].[Product] prod
    LEFT JOIN [Production].[ProductModel] model ON prod.[ProductModelID] = model.[ProductModelID]
    LEFT JOIN [Production].[ProductSubcategory] category ON prod.[ProductSubcategoryID]=category.[ProductSubcategoryID]
    WHERE prod.[ProductModelID] IS NOT NULL
    ```
  
  - Lets create a product dimension table
    
    ```
    SELECT [ProductID],[ProductModelID],[ProductSubcategoryID],ProductName,[SafetyStockLevel],ProductModelName,ProductSubCategoryName
    INTO DimProduct
    FROM Product_view 
    ```
  
  - If you want to drop the views and the tables
    
    ```
    DROP VIEW Customer_view 
    DROP TABLE DimCustomer
    DROP VIEW Product_view 
    DROP TABLE DimProduct
    ```

### Transfer data to our SQL pool

- Select Integrate section and click [+]
- click on 'copy data tool'
- Fill information from source to destination in data tool properties
  - Properties [Task Cadence or Task schedule]
  - Source [ Source Type | connection : create connection with source type | Integration runtime | Source Table: Existing Table]
  - Target [ Target Type | connection : create connection with target type | Integration runtime | Target Table: Existing Table]
  - Settings [ Task Name | Staging account linked service [+] New | Integration Runtime | Storage Path | Advanced : Polybase | Copy Command | Bulk Insert ]

### enable ssh in windows

```
https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell
```

### To know when the next versions will be introduced or retired check the AKS

```
https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions#aks-kubernetes-release-calendar
```

### powershell script to lock resource-group

```
new-azresourcelock -ResourceGroupName example -LockName dontDeleteMe -LockLevel canNotDelete
```

### remove lock

```
Remove-AzResourceLock -ResourceGrouName example -LockName dontDeleteMe
```

### Log Analytics Queries

- This can be used for search for a keyword in the event table
  
  ```
  Event | search "demovm"
  ```

- This can used to pick up 5 events taken in no specific order
  
  ```
  Event | top 10 by TimeGenerated
  ```

- This is used to filter based on a particular property of an event
  
  ```
  Event | where EventLevel == 4
  ```

- This can be used to check for the events generated in the previous 5 minutes
  
  ```
  Event | where TimeGenerated > ago(5m)
  ```

- This can be used to project certain properties
  
  ```
  Event | where TimeGenerated > ago(5m) | project EventLog, Computer
  ```

### Log Analytics - Azure Activity Table - Resources

- This shows the count of rows in the table. This depends on the time range you choose in Log Analytics
  
  ```
  AzureActivity
  | count
  ```

- Here you are returning the rows based on the TimeGenerated
  
  ```
  AzureActivity
  | where TimeGenerated < datetime(2/8/2022 00:00:00)
  | count 
  ```

- Here you are returning the rows based on the TimeGenerated
  
  ```
  AzureActivity
  | where TimeGenerated < ago(1h)
  | count 
  ```

- You can also print the values to the workspace
  
  ```
  print(ago(1h))
  print(datetime(2/8/2022 00:00:00))
  ```

- Searching for failure 
  
  ```
  AzureActivity
  | search "Failure" 
  ```

- Free Text Search
  
  ```
  AzureActivity
  | search "Failure"
  | where TimeGenerated < ago(1h)
  ```

- Here you are using the where clause to filter on a specific column value
  
  ```
  AzureActivity
  | where ActivityStatusValue contains "Failure"
  AzureActivity
  | where ActivityStatusValue contains "Failure"
  |count
  ```

- Group by ActivityStatusValue
  
  ```
  AzureActivity
  | summarize count() by ActivityStatusValue
  ```

- You can summarize by multiple columns
  
  ```
  AzureActivity
  | where TimeGenerated < ago(1h)
  | summarize count() by ResourceGroup,ActivityStatusValue
  | sort by ResourceGroup
  ```

- count - Returns the number of records in the input record set.

- count() - Aggregation function

- Grouping by buckets of TimeGenerated
  
  ```
  AzureActivity
  | summarize count() by bin(TimeGenerated, 1h)
  | sort by TimeGenerated 
  AzureActivity
  | where TimeGenerated between (datetime(2/8/2022 03:00:00) .. datetime(2/8/2022 04:00:00))
  | count
  ```

- Summarize operations per OperationNameValue and resource group
  
  ```
  AzureActivity
  | summarize count() by OperationNameValue,ResourceGroup
  ```

- Project only certain columns
  
  ```
  AzureActivity
  | project OperationNameValue,ResourceGroup
  ```

- Accessing the details of an object
  
  ```
  AzureActivity
  | project OperationNameValue,ResourceGroup,Properties_d["eventCategory"]
  ```

- Converting string to a dynamic object
  
  ```
  AzureActivity
  | extend r=todynamic(HTTPRequest)
  | project OperationNameValue,ResourceGroup,r["clientIpAddress"]
  ```

- For the Sign-in logs table
  
  ```
  SigninLogs 
  | extend s=todynamic(Status) 
  | where s["errorCode"]<>0
  ```

- For the Firewall logs in the Azure Diagnostics table
  
  ```
  AzureDiagnostics 
  | parse msg_s with Protocol 'request from ' *
  | extend l_protocol=Protocol
  | project l_protocol
  AzureDiagnostics 
  | parse msg_s with Protocol 'request from ' SourceIP ':' * 'to ' DestinationIP ':' *
  | extend l_protocol=Protocol,l_sourceip=SourceIP,l_destination=DestinationIP
  | project l_protocol,l_sourceip,l_destination
  ```

- For the Security Events table
  
  ```
  SecurityEvent
  | where EventID ==4673
  | project Account
  SecurityEvent
  | summarize count() by bin(TimeGenerated, 1h)
  | sort by TimeGenerated
  ```

### Azure Container Group

- Deploy Multiple Container at once.
  
  ```
  az container create --resource-group container-grp --file deployment.yaml
  ```

- create `deployment.yaml`
  
  ```
  apiVersion: 2018-10-01
  location: eastus
  name: container
  properties:
  containers:
  - name: nginx-demo
    properties:
      image: nginx
      resources:
        requests:
          cpu: 1
          memoryInGb: 1.5
      ports:
      - port: 80
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: tcp
      port: 80
  tags: null
  type: Microsoft.ContainerInstance/containerGroups
  ```

### Content Trust in ACR

- It is featire available in Premium service tier of ACR
- It is used to sign and aprroved docker images with content trust process and then upload in registry

### Communicate Container instnace with ACR without Access key but using Service Principal with AD authentication

- Step 1 - First you create a service principal
  
  ```
  az ad sp create-for-rbac --name registryapp --scopes $(az acr show --name appregistry200390 --query id --output tsv) --role acrpull
  ```

- Step 2 - Ensure to copy the values of the output of the previous command to the below variables
  
  ```
  $appID="a7c81986-8a36-4013-8a7d-8952a53c3897"
  $appPassword="mRFphzkEm.27nkvjAc0F0xKSSu4vwnM5~h"
  ```

- Step 3 - Then create the container instance
  
  ```
  az container create --name app-instance2000 --resource-group container-grp --image appregistry200390.azurecr.io/myapp:latest --registry-login-server appregistry200390.azurecr.io --registry-username $appID --registry-password $appPassword --ip-address Public
  ```

### Azure AntiMalware Extension

- It is free Azure solution for VMs
  
  ```
  Azure portal-->Select VM-->Extension & application-->Add extesnion-->Microsoft AntiMalware-->Next-->Configure-->review + create
  ```

### HUB and SPOKE Architecture with On-premise Network Communication with Site-to-Site communication

- **HUB**
  
  - Cetralize virtual network used for hosting Firewall services, Load Balancer i.e Application Gateway,Traffic Manager etc.
  - All the traffic flow by the Hub network only from On-primesis or intenret

- **SPOKE**
  
  - All other virtual Network Available for communication with HUB works as Spoke network.
    
    ```
    HUB Vnet<=====Vnet Peering=====> SPOKE vnet
    ```

- Create `HUB & SPOKE` setup
  
  - Step 1 - Create `Hub Virtual Network`
    
    ```
    Azure Portal-->virtual Network Create-->create Normal Subnet-->Create Gateway Subnet-->Enable Bastion Host-->Enable Bastion Subnet-->Create Bastion public IP-->Enable Firewall-->Enable Firewall Subnet-->Create Firewall Public IP-->Review + create
    ```
  
  - Step 2 - Create `Virtual Network Gateway`
    
    ```
    Azure Portal-->Create Virtual network Gateway[ Subscription | ResourceGrouName | Name | Region | Gateway type : VPN | VPN Type : Route Based | Virtual Network | Create Public IP Address ]-->review + Create
    ```
  
  - Step 3 - Create `Spoke Virtual Network with VM without Public IP associate to VM`
    
    ```
    Azure Portal-->Create VM-->virtual Network Create-->create Normal Subnet-->Review + create
    ```
  
  - Step 4 - Create `Local Network gateway`
    
    ```
    Azure Portal-->create local network gateway [ name | Enpoint | IP Address : Company On-prim VM IP | Address Range : Company On-prim Network address | Subscription | resource-group | Location ]-->Create
    ```
  
  - Step 5 - Make connection with `Gateway`
    
    ```
    Azure Portal-->select app gateway-->setting-->connection-->Add [Name | Connection Type : Site-to-Site(IPsec) | First Virtual Network gateway(Azure VPN Gateway vnet) | Second Virtual Network Gateway (Local Network Gateway On-prim Network)| Shared Key | Ok]
    ```
  
  - Step 6 - Create `Peering` with `HUB and SPOKE Vnet`
  
  - Step 7 - `Routing Traffic` through `Firewall`
  
  - Traffic Flow from `On-prim to Spoke Azure VM`
    
    ```
    On-Prim-Machine-->Traffic-->VPN Gateway + Firewall + HUB Vnet-->Spoke Vnet-->Spoke VM
    ```
    
    ```
    Azure Portal-->Create HUB Route Table-->Select route table resource-->Setting-->route-->add [ Route name | address prefix : Spoke Vnet| Next Hop type : Virtual Appliance | Next HOP Address : Firewall Private IP-->OK]-->Setting-->subnet-->Select HUB Vnet-->Select Gateway Subnet-->Ok
    ```
  
  - Traffic Flow from `Spoke Azure VM to on-prem machine`
    
    ```
    On-Prim-Machine<--Traffic<--VPN Gateway + Firewall + HUB Vnet<--Spoke Vnet<--Spoke VM
    ```
    
    ```
    Azure Portal-->Create SPOKE Route Table-->Select route table resource-->Setting-->route-->add [ Route name | address prefix : 0.0.0.0/0| Next Hop type : Virtual Appliance | Next HOP Address : Firewall Private IP-->OK]-->Setting-->subnet-->Select SPOKE Vnet-->Select Normal Subnet VM-->Ok
    ```
  
  - Step 8 - Allow `Firewall Rule` to communication from `SPOKE to On-PRIM Vm`
    
    ```
    Azure Portal-->Select Firewall-->Setting-->Firewall Manager-->Visit configure and manage Firewall-->Azure Firewall Policies-->Create azure Firewall Policy [ Subscription | resource-group | Name | region | Rules-->Add a rule collection [ Name | Rule Collection Type : Network | Priority : 100 | Rule Collection Action : Allow | Rules [ Name : Allow SPOKE | Source Type : IP Address | Source : IP address of Spoke VM | protocol : TCP | Destination Port : 80 | Destination Type : IP address | Destination : IP addres of On-Prim VM ]-->add ]-->Review + Create]
    ```
    
    ```
    Azure Portal-->Select Firewall-->Setting-->Firewall Manager-->Visit configure and manage Firewall-->Azure Firewall Policies-->Seelct Firewall Policies-->Manage Association-->Associate Vnet-->select HUB Network-->Add
    ```
    
    ### To create container from Azcpy tool in azure storage Account blob
    
    ```
    azcopy make "<http://storage.container.url>/<Conatiner Name>?SAS Token with default parameters"
    ```

### Azure API Management with Private access with Vnet only Resources i.e webapps, VMs, Kubernates Cluster etc.

- Step 1
  
  ```
  Azure Portal-->virtual network-->Create API subnet(10.0.1.0/24)-->review + create
  ```

- Step 2 
  
  ```
  Azure Portal-->Public IP in APiMgmntLocation-->review + create
  ```

- Step 3 
  
  ```
  Azure Portal-->api management services-->select API management-->Deployment + Infrastructure-->virtual Network-->Select External-->Please select Vnet-->[ select Vnet | Select API subnet | Select Public IP address-->Apply]-->Save
  ```

- Step 4 
  
  ```
  Azure Portal-->virtual network Resources(i.e. vm)-->Networking-->Select NSG(Because It is also assigned to APIMgMntSubnet Group)Add inbount port rule-->[source : Any | Sources Port Range : * |Destination : Any | Services : Custom | Destination Port Rnages : 3443 | protocol : tcp | Action : Allow | Priority : 100 | Name : ApiManagementPort_3443-->Add ]
  ```

- Step 5 
  
  ```
  Azure Portal-->virtual network Resources(i.e. vm)-->Networking-->Select NSG(Because It is also assigned to APIMgMntSubnet Group)Add inbount port rule-->[source : Any | Sources Port Range : * |Destination : Any | Services : Custom | Destination Port Rnages : 443 | protocol : tcp | Action : Allow | Priority : 100 | Name : Port_3443-->Add ]
  ```

- Step 6 
  
  ```
  Azure Portal-->api management services-->select API management-->APIs-->Create blank APi-->[Display Name | Name | Web service URl : http://10.1.0.4(Private IP of Azure resources (i.e. VM Private IP))-->create ]
  ```

### Domain Name Record setup for DNS Server

| Record Abbreviation | Record Type               | Record Description                                                                                                                                                                                  |
| ------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **NS**              | Name Server Record        | Describes a name server for the domain that permits DNS lookups within several zones. Every primary as well as secondary name server must be reported via this record.                              |
| **MX**              | Mail Exchange Record      | Permits mail to be sent to the right mail servers located in the domain. Other than IP addresses, MX records include fully-qualified domain names.                                                  |
| **A**               | Address Record            | Used to map a host name to an IP address. Generally, A records are IP addresses. If a computer consists of multiple IP addresses, adapter cards, or both, it must possess multiple address records. |
| **CNAME**           | Canonical Name Record     | Can be used to set an alias for the host name.                                                                                                                                                      |
| **TXT**             | Text Record               | Permits the insertion of arbitrary text into a DNS record. These records add SPF records into a domain.                                                                                             |
| **TTL**             | Time-to-Live Record       | Sets the period of data, which is ideal when a recursive DNS server queries the domain name information.                                                                                            |
| **SOA**             | Start of Authority Record | Declares the most authoritative host for the zone. Every zone file should include an SOA record, which is generated automatically when the user adds a zone.                                        |
| **PTR**             | Pointer Record            | Creates a pointer, which maps an IP address to the host name in order to do reverse lookups.                                                                                                        |

### Active Geo Replication in SQL database [ Primary | Secondary Database ] for failover scenarios

```
Azure Portal-->Data management-->Geo-Replication-->Secondary-->Select Target Region-->[Create or select exising server | Compute + storage ]-->Review + Create
```

### Auto-Failover SQL Server

```
Azure Portal-->Data management-->Failover Group-->Add Group-->[ Failover Group Name | Select Replicate server | Read/Write failover Policy : Automatic | Read/Write grace period : 1 hour | Configure database : Select DB fot failover ]
```

### Azure VM Disaster recovery

```
Azure Portal-->VM-->Select resource-->Operation-->Disaster Recovery-->select Target region-->Select Configuration-->review + Start replication
```

### `Databricks` setup

1. Create databricks infrastructure

2. Sigin into `workspace`

3. Create `cluster`

4. Create `notebook(language/cluster)` and `Libraries`

5. Read `data` from resource

6. Run the `query` in `Notebook` 

7. Analyze the result

8. `WASB` stands for `Windows Azure Blob storage` 
   
   - This is the protocol that can be used by `Azure Databricks` to `access Azure Blob storage`

9. Create a `mount point` onto the `storage account`

10. `<conf-key>` can be either `fs.azure.account.key.<storage-account-name>.blob.core.windows.net` 
    or fs.azure.sas.<container-name>.<storage-account-name>.blob.core.windows.net

11. `Databricks Utilities` are underlying libraries that allow you to perform a variety of tasks

12. These are available for `Python, R, and Scala notebooks`
    
    ```
    dbutils.fs.mount(
    source = "wasbs://data@datastore40000.blob.core.windows.net",
    mount_point = "/mnt/myfiles",
    extra_configs = {"fs.azure.account.key.datastore40000.blob.core.windows.net": "hJp89RB5jtkgAqEnvEZZ51dc0Lfbf/hWxeq27ndWwWTegTaD0il7eOkDY8/WYUQAE3Z3TRn2EffdErpwqnG4+w=="})   
    ```

13. See the files in the mount
    
    ```
    display(dbutils.fs.ls("/mnt/myfiles"))
    ```

14. Read the csv file into a data frame
    
    ```
    df=(spark.read.csv("/mnt/myfiles/Logdata.csv"))
    ```

15. Display the data frame
    
    ```
    display(df)
    ```

### Create Batch Account Setup

- Create `Batch Account`
  
  ```
  AzurePortal-->Batch service-->New Batch Account-->[ Subscription | ResourceGrouName | Account Name | Location | Select Storage Account | Review + create ]
  ```

- Add `Application Package & pool`
  
  ```
  AzurePortal-->Batch service-->Select Batch Account-->Features-->Application-->Add-->[ Application ID | Version | Application Package : Select package.Zip | Submit]-->Pools-->Add-->[ pool ID | Display Name | Identity | Image Type | Publisher | Size | Target Dedicated Node | Target Low-Priority node | Resize Timeout | Application Package -->Select Application Package | Virtual Network ] -->OK
  ```

- Create `Job & Task`
  
  ```
  AzurePortal-->Batch Service-->Select batch Account-->Features-->Jobs-->Add-->[ Job ID | Pool ]-->Ok-->Select JOB-->General-->Tasks-->Add-->[ Task ID | Display Name | Command Line | Resource file | Application Package ]-->Submit
  ```

### Deploy Docker Host in Ubuntu Linux VM

```
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### SQL Server Secuirty

- Masking in SQL server for Other users exept adminstrator
  
  ```
  Azure Portal-->SQL Server-->Select database-->security-->Dynamic Data Masking-->select Schema-->Table-->Coloumn Name(which data needs to be masked)-->Save
  ```

### SQL server Secuirty

- Tranparent Data Encryption
  
  ```
  Azure Portal-->SQL Server-->Select database-->security-->Tranparent data Encryption-->Turned On-->Save
  ```

### Application object : clientId

- It is more identity for application available in Azure AD.

- It will configured in azure by app registration in Azure AD.
  
  ```
  Azure Portal-->Azure AD-->app registration-->New Registration-->[ Name : Name | Supported Account type : Account in organization directory only(single tenant)]-->Resgiter-->Copy Application(client)ID-->Copy Directory(tenant)ID-->
  ```
  
  ```
  Azure Portal-->Azure AD-->app registration-->select application registered-->Certificates & secrets-->Client secret-->New Client Secret-->[ Description : Name | Expires : times for secret active ]-->add-->Copy Secret Value 
  ```
  
  ```
  Azure Portal-->Resource-->Access Control(IAM)-->Add-->Role Assignment-->[ Role : Reader | Assign Access to : Users, groups and Service principal | select : registration app name ]-->Save
  ```

- Usage
  
  - **String tenantid** : Copied Application(client)ID from app registration
  
  - **String clientid** : Copied Directory(tenant)ID from app registration
  
  - **String clientsecret** : Copied Value from application object secret from app registration

### To access application object to access api for azure resources

```
Azure Portal-->Azure AD-->app registration-->select application registered-->API permission
```

### To access application object to authentication from azure resources

```
Azure Portal-->Azure AD-->app registration-->select application registered-->Authentication
```

### To access secret (i.e. Database SQL server Password) from azure key vault

```
Azure Portal-->azure keyvault-->select Keyvault-->Add access policy-->provide permission-->select principal : Azure AD application resgistered object name-->select-->add
```

- usage:
  
  - **String tenantid** : Copied Application(client)ID from app registration
  
  - **String clientid** : Copied Directory(tenant)ID from app registration
  
  - **String clientsecret** : Copied Value from application object secret from app registration
  
  - **keyvault_url** = `https://keyvaultname.vault.azure.net/`
  
  - **secret_name** = `dbpassword`

### Managed Servive Identity

```
Azure Portal-->Resource-->identity-->System assigned-->on
```

### Azure AD connect

- Used to sync between on-primises with active directory

- **On-primesis directory <-------------> Azure AD Connect <-------------> Azure Active Directory**

### Points on Azure AD Connect

- The Azure AD Connect synchronization service is used to synchronize identity data between your on-premise environment and Azure AD.

- There are two components for this service
  
  - Azure AD Connect sync component – This is installed on the on-premise environment.
  - Azure AD Connect sync service – This service runs in Azure AD.

### To use Azure AD Connect, you need to have the following pre-requisites in place

- An Azure AD tenant

- Use the IdFix tool to identify errors such as an duplicates and formatting problems in your on-premise directory.

- The Azure AD Connect sync component must be installed on a Windows Server 2012 Standard or better. The server must have the full GUI installed. The server must be domain joined. Ideally this component must not be installed on the domain controller.

- The Azure AD Connect sync component requires a SQL Server database for storing identity data. By default , the installation of Azure AD Connect will install SQL Server 2012 Express LocalDB.

- During the configuration of the Azure AD Connect sync component, you need to use an

- Azure AD Global Administrator account for the Azure AD tenant. The account should be a school or organization account and cannot be a Microsoft account

- An Enterprise Administrator account for the on-premise Active Directory

- The Azure AD Connect server needs DNS resolution for both intranet and internet. The DNS server must be able to resolve names both to your on-premises Active Directory and the Azure AD endpoints

- **Password Hash Synchronization** : Here Azure AD Connect synchronizes a hash, of the hash, of a users password from an on-premises Active Directory instance to a cloud-based Azure AD instance.

- The advantage is that you only need to maintain one password for both authentication in your on-premise environments and in the cloud.

- If you change a user’s password in the on-premise Active Directory setup, the password will be synced onto Azure AD.

- **Pass-through Authentication** : This is kind of similar to password hash synchronization, 
  but here the users’ passwords is directly validated against the on-premise Active Directory. This allows organizations to enforce their on-premise Active Directory security and password policies.

### Application Secuirty Rule in NSG

- Create `Application Secuirty Group`
  
  ```
  Azure Portal-->application Security-group-->Create application Security-group [Subscription | resource-group-name | Name | Region ]-->Review + create
  ```

- Configure `Application Security Group` in `NSG`
  
  ```
  Azure Portal-->Select NSG-->Application Secuirty Group-->Configure the application Security-group-->Select Application Security-group-->Save
  ```

- add `Inbound Rule` for `Application Secuirty Group`
  
  ```
  Azure Portal-->NSG select-->Add inbound rule-->[source : Application Secuirty Group | Source Application Secuirty Group : Application Security Group Name | Source Port Range : * | Destination : IP Address | Destination IP Address : 10.0.0.5 | Services : MSSQL | Destination Port range : 1433 | Protocol : TCP | Priority : 100 | name : demo ASG -->Save ] 
  ```

### privileged Identity Management

- It is an extension for Azure AD roles and RBAC roles

- We can manage and assign roles to user in azure AD tenant.

- We can check all Azure AD roles settings
  
  ```
  Azure Portal-->privileged Identity Management-->settings-->select role to edit and monitor(i.e. Azure DevOps administrator)
  ```

### check Azure Active Directory-->Monitoring-->Sign-in-->gives you details about user Sign in AAD

```
KQl Query : SigninLogs
```

### Monitoring - Azure Service Map - Network traffic services connection with VM

```
Set-AzVMExtension -ExtensionName "Microsoft.Azure.Monitoring.DependencyAgent" -ResourceGroupName "new-grp" -VMName "demovm" -Publisher "Microsoft.Azure.Monitoring.DependencyAgent" -ExtensionType "DependencyAgentWindows" -TypeHandlerVersion 9.5 -Location NorthEurope
```

### NSG Flow logs

- Version2 having features to capture bytes and packets details also.

### Dynamic group in aad add user automatically in group

```
azure Portal-->azure active directory-->group-->Membership type : Dynamic user-->Query : based on condition add user in Group-->query : (user.country -eq "india")
```

### app registration and enterprise application role in AAD

- **application administrator**

### AAD role VS RBAC

- Azure roles apply to Azure resources.

- Azure AD roles apply to Azure AD resources such as users, groups, and domains.

- **AAD role** : Roles with respect to AAD

- **RBAC** : Roles with respect to subscription or resources lebel access

### move resources

```
AzurePortal-->select Resource-->Move-->1. Move to another Resourcegroup,Another Subscription or any other region
```

### Blob Storage BLOB

- It is used to store **Binary large Object (Media etc)**

### azure table storage noSQL storage works on `key(Row) : value(Coloumn)` pair

| ROW | COLOUMN 1 | COLOUMN 2 | COLOUMN 3 | COLOUMN 4 |
| --- | --------- | --------- | --------- | --------- |
| C1  | name      | class     | age       | phone     |
| C2  | name      | class     | age       | phone     |

### Blob container

- we can restore files after deletion with respect to Data Management-->Data Protection setting

### Storage account replicate data to another storage account blob container

```
Azure Portal-->StorageAccountName-->Data management-->Object Replication-->Destination storage account detail
```

### Premium Account have blob level configuration and only two Redundancy

- File Share Replication
  - **LRS**
  - **ZRS**

### Azure File Sync

- Hybrid Environment (on-primesis with Azure file share) use azure file sync agent in Win Machine
  
  ```
  Azure Portal-->VM-->Windows Server-->Login-->Server Manager-->Download Azure File Sync agent .msi w.r.t server-->Install-->open-->AzureEnvironment-->AzureCloud-->Signin-->Select subscription,Resourcegroup,Storage Sync service-->Register
  ```
  
  ```
  Azure Portal-->Storage Sync Service-->Storage File sync-->sync group-->add server point-->select registerd server-->Path sync-->enbaled
  ```

### import/export job

- used to tranfer large amount of data to cloud or vice versa

- **Export** : Identify the data and number of disk using WAImportExport tool

### Azure data box service

- It is also used to import and export data

### modify existing ARM template of resource

```
Azure Portal-->select resource-->export template-->deploy-->edit ARM-->dont change name-->thats it
```

### Creating specislized VM image for backup to create another VM with same image include data

- **VM Image** : This is copy of the full VM(inclue OS and Data disk)
  
  1. go to the VM overview table
  
  2. select Capture option
  
  3. Create compute image gallery 
  
  4. select image name/version/ and image type specialized(with Vm all information with data)
     or 
  
  5. select image name/version/ and image type generalised(w/o vm name,user data etc. only with data)
  
  6. next and start deployment

### creating VM from existing custom specialized/generalised VM image

1. select image from azure compute gallery

2. create VM or VMSS option in overview

3. configure all setting and create VM

4. if datadisk exist for old vm it will attched already

5. It will assign new public IP or network to VM

### Recommended Gateway Subnet

- `Gateway Subnet` for `P2S` VPN

```
GatewaySubnet = 10.0.0.0/27 (P2S VPN)
```

### To test inbound and outbound traffic

```
azure Portal-->network watcher-->IP flow verify-->given IP
```

### To test Network Security Group Diagnostics

```
azure Portal-->network watcher-->NSG Diagnostics-->Details IP traffic
```

### Azure monitor logs KQL(Kusto Query Language)

### Backup in Azure

```
Azure Portal-->Backup centre-->create Vault-->create backup policies or interval for specific service-->backup-->select instnace or services-->select Vault-->select policies-->Done
```

### Backup Consistent & Consistency of our restore point

- **Crash consistent** : Level of consistancy typical when VM shutdown at the time of Backup

- **Application Consistent** : The snapshot capture whole VM and running application backup

- **File System consistent** : create file system consistent snapshot backup

### Restore Azure file in Azure restore

```
Azure Portal-->virtual-machines-->backup-->restore point(only available if backup is enbaled)-->file Recovery-->choose restore point-->select for file in local system
```

### Restore Azure VM in Azure restore

```
Azure Portal-->virtual-machines-->backup-->restore point(only available if backup is enbaled)-->restore VM-->choose restore point-->create New VM or replace existing-->select storage account-->trigger
```

### Azure Queue Storage

- Messaging service store large number of Messages (buffer or backlog)

- **App1-->Send Message-->But Application 2 didn't received it immediately**

- **App1-->send message-->Store in Queue Storage Until App2 not able to received-->App2 recived**

### Disk are Virtual Hard Disk (.VHD) and store in storage account in "Page Blob" format Storage Account

- **Unmanaged Disk** : (Not recommended old practise) We decide where we need to store disk in which storage account.

- **Managed Disk**   : Azure Store this disk in Storgae Account by default we can't access it.

### create bulk user operation

```
Azure Portal-->azure Active Directory-->users-->bulk-->operations
```

### Get the public FQDN for the Azure Kubernates Services

```
AksDNS=az aks show -n aks-cluster -g resource-group --query fqdn
OutPut : "aks-cluster-resource-group-v6978f9f.hcp.eastus2.azmk8s.io"
```

### Get the private FQDN for the Azure Kubernates Services

```
AksDNS=az aks show -n aks-cluster -g resource-group --query privateFqdn
OutPut : "aks-cluster-resource-group-v6978f9f.hcp.eastus2.azmk8s.io"
```

### get the address of azure kubernates services

```
nslookup aks-cluster-resource-group-v6978f9f.hcp.eastus2.azmk8s.io
```

### Private cluster using Vnet Integration access the control plane through internal load balancer

- Any resources with access to that Internal load balancer can access the cluster control plane
  
  - **Enbale private cluster** : --enable-private-cluster
  
  - **Vnet Api server Integration** : --enable-apiserver-vnet-integration

### Disable public FQDN in Azure Kubernates Services

```
az aks update -n aks-cluster -g resource-group --disable-public-fqdn
```

### enable Network watcher in all region

```
Monitor-->network-->network watcher-->region-->change Disable to Enable
```

### Establish Hybrid connection

```
create app service-->networking-->configure hybrid connection endpoint-->add hybrid connection-->create new hybrid connection-->Http Connecton Name: Httpconnection-->Endpoint Host:VisualStudio-->Endpoint Port:80-->Service Namespace:create new-->location-->Name-->httphybridconnection-->OK
create app service-->networking-->configure hybrid connection endpoint-->Download connection manager
```

### Azure traffic manager if we set priority same for all instnace then traffic distrubuted evenly in all instnace.

### #azure Traffic Manager nested profile with multiple endpoint i.e. Highly available on Geaographic,region,zone failure

- Create child-1 Traffic Manager profile with multiple endpoint

- Create child-2 Traffic Manager profile with multiple endpoint

- Create Parent Traffic Manager profile

- **Parent Traffic Manager Profile-->Endpoint-->add-->select type:Nested Endpoint-->Target Resource : select child-1 ATM profile-->select : location-->Minimum child endpoint-->ok**

- **Parent Traffic Manager Profile-->Endpoint-->add-->select type:Nested Endpoint-->Target Resource : select child-2 ATM profile-->select : location-->Minimum child endpoint-->ok**

### create service end point for storage services with subnet

```
azurePortal-->vNet->subnet-->Service Endpoint-->select Services Name-->save
```

### configure storage account with Vnet is only applicable when both Vnet and Storage account in same region only

### Access only 1 storage account from specific VM

```
Create service end point policy-->policy defination-->select service(Microsoft.storage)-->Scope(Single Account)-->RG-->Subscription-->Resource Name-->Add-->Save-->Associate Subnet-->edit subnet association-->select vNet-->select subnet-->apply-->success
```

### Block internet traffic in VM through NSG by create outbound rule with following parameters

```
Source                  : any
Source port range       : *
Destination             : Service Tag
Destination Service Tag : Internet
Destination Port Range  : *
Protocol                : Any
Action                  : Deny
Priority                : 110 (It must be high then the traffic which you allow i.e storage account,application-gateway etc.)
Name                    : BlockInternetTraffic
```

### Azure VMSS autoscaling Profile and priorities

| 1. Default Profile        | Mandatory                                                         | Priority(3)     | ⬇   |
| ------------------------- | ----------------------------------------------------------------- | --------------- | --- |
|                           | **Default to round the clock schedule**                           |                 | ⬇   |
|                           | **Will not execute if Recurrence or fixed profile exist**         |                 | ⬇   |
| **2. Recurrence Profile** | **Recur on those days with start time specified**                 | **Priority(2)** | ⬇   |
|                           | **Week days and weekend profiles**                                |                 | ⬇   |
|                           | **Business Hour and Non Business Hour profile**                   |                 | ⬇   |
| **3. Fixed profile**      | **Execute on the specific days**                                  | **Priority(1)** | ⬇   |
|                           | **It takes priority 1 always for execution on that day if exist** |                 | ⬇   |

### Access Domain from DNS Zone

- Always Whitelist of Register all nameserver of azure DNS to Domain provider.

```
ns1-04.azure-dns.com.
ns2-04.azure-dns.net.
ns3-04.azure-dns.org.
ns4-04.azure-dns.info.
```

### SSL certificate with Application gateway

- Generate Self Signed Certificate and Private Key

```
openssl req -newkey rsa:2048 -nodes -keyout httpd.key -x509 -days 7300 -out httpd.crt
```

- Convert SSL Certificate, Key to PFX to used for Application gateway

```
openssl pkcs12 -export -out httpd.pfx -inkey httpd.key -in httpd.crt -passout pass:kalyan
```

### use NAT rule in Azure Load Balancer for connecting VM by SSH using different Ports

- **frontendPort(1022,2022,3022,4022,5022)**

- **BackendPort(22)**

### azure bastion subnet AzureBastionSubnet(/26 or larger)

- It works for Vnet basis one Azure Bastion subnet works for inside vnet only.

### check az version

```
az version
```

### upgrade az version (not work in azure-cli)

```
az upgarde
```

### To set subscription in multiple subscription

```
az account set --subscription d2e44caa-1265-4fc3-bdaf-dc76a0
```

### to show the accont list or subscription

```
az account list
```

### register feature az-cli by command in cloud shell

```
az feature register --namespace Microsoft.ContainerService -n AutoUpgradePreview
```

### List Node Pools in AKS

```
az aks nodepool list --cluster-name ClusterName --resource-group ResourceGrouName -o table
```

### disable monetring /insight in kubernates

```
az aks disable-addons -a monitoring -n cluster-name -g resource-group-name
```

### use kubernates cluster

```
az aks get-credentials --resource-group ResourceGrouName --name ClusterName --overwrite-existing
```

### bypass and Override AD Authentication

```
az aks get-credentials --resource-group ResourceGrouName --name ClusterName --admin
```

### upload contents,file,directory in blob storage

```
az storage blob upload-batch -s C:\Users\sawan\Desktop\azure\microservice-new\UI -d $web --connection-string=DefaultEndpointsProtocol=https;AccountName=csb10032000947898yuo;AccountKey=0290i8u3RtIjG2Jz58sOhz67vBoXNQKHAAqe+we6qpdbuv9Yz6syw7DlEWoOyThfQUFae+IZFzVrrWrhr8zfa6Ewlyg==;EndpointSuffix=core.windows.net
```

### delete content from blob storage

```
az storage blob delete-batch -s $web --connection-string=DefaultEndpointsProtocol=https;AccountName=csb10032000947898yuo;AccountKey=0290i8u3RtIjG2Jz58sOhz67vBoXNQKHAAqe+we6qpdbuv9Yz6syw7DlEWoOyThfQUFae+IZFzVrrWrhr8zfa6Ewlyg==;EndpointSuffix=core.windows.net 
```

### "resource Quota" used to defined how much resources used by Particular Namespace

### detach container registry from AKS cluster

```
az aks update -g resource-group-name -n aks-kluster-name --detach-acr container-registries-name
```

### acr image build

```
az acr build --image images.azurecr.io/cache:example --registry images --file Dockerfile .
```

### upload multiple file in batch in blob in stoarge account

```
az storage blob upload-batch -s C:\Users\sawan\Desktop\Foldertest -d BlobFoldertest --connection-string=DefaultEndpointsProtocol=https;AccountName=csb1003200094f9c789;AccountKey=IjG2Jz58sOhz67vBoXNQKHAAqe+we6qpdbuv9Yz6syw7DlEWoOyThfQUFae+IZFzVrrWrhr8zfa6Ewlyg==;EndpointSuffix=core.windows.net
```

### SSL enable with JDBC URL

```
jdbc:postgresql://${DB_HOST}:5432/${DB_NAME}?sslmode=require
```

### azure login from cli

```
az login -u <username> -p <password>
```

### start/stop kubernates cluster

```
az aks start/stop --resource-group testPoc --name testPoc
```

### connect cluster to azure cli

```
az aks browse --resource-group testrg --name k8s-new
```

### login to azure acr

```
az acr login --name images.azurecr.io
RegistryName : images
LoginServer  : images.azurecr.io
username     : images
password     : lMNKoxk2ncdjklf8f0NcYLtLZtGsOqKDyz
```

### attach container registries to cluster

```
az aks update -n k8s-new -g osdemorg --attach-acr images
```

### validate that the registry is accessible from the AKS cluster with kubernates clientIP

```
az aks check-acr --name test-aks --resource-group osdemorg --acr images.azurecr.io
```

### define RAM percentage in JAVA HEAP SIZE in Kubernates by (default Xmx~25% Xmx<25% of total resource)

```
-XX:MaxRAMPercentage=75.0 #we define use it 75% now
```

### create mysqlDB server from azure-cli

```
az mysql server create --resource-group <resource name> --name <server name> --location <location> --admin-user <username> --admin-password <password> --sku-name <pricingtier>_<Generation>_<core> --storage-size <Dbsize> --version <DBversion> --tags "Component=MySqlDatabase"
```

### start|stop|delete mysql server

```
az mysql server start|stop|delete --name <server-name> -g <resource-group-name>
```

### start|stop|deallocate azure vm

```
az vm start|stop|deallocate -n <vm-name> -g <resource-group-name>
```

### create Resource group

```
az group create --name myResourceGroup --location eastus
```

### create NSG

```
az network nsg create --resource-group osdemorg --name demonsg --tags "Component=Security-group"
```

### create security rule in nsg

```
az network nsg rule create --resource-group osdemorg --name Allow80 --nsg-name os-bastion-nsg --priority 102 --access allow --direction inbound --source-address-prefixes '*' --destination-address-prefixes '*' --destination-port-ranges '*' --source-port-ranges '*' --protocol Tcp
```

### create vnet

```
az network vnet create --resource-group osdemorg --name MyVnet --address-prefix 11.0.0.0/22
```

### create subnet

```
az network vnet subnet create --resource-group osdemorg --vnet-name MyVnet --name MySubnet --address-prefixes 11.0.1.0/24
```

### create mysql server

```
az mysql server create --resource-group osdemorg --name test-mysql --location eastus --admin-user test --admin-password test_123 --sku-name GP_Gen5_2 --storage-size 12288 --tags "Component=MySqlDatabase"
```

### create redis-server

```
az redis create --location eastus --name azure --resource-group osdemorg --sku Basic --vm-size c0 --enable-non-ssl-port --tags "Component=Redis-Cache"
```

### create ACR for azure

```
az acr create -n demo -g osdemorg --sku Premium --admin-enabled true  --location eastus --tags "Component=ConatinerRegistry"
```

### create kubernates cluster

```
az aks create --resource-group osdemorg --name demo-k8s --location eastus --enable-cluster-autoscaler --node-vm-size Standard_DS2_v2 --min-count 1 --max-count 3 --kubernetes-version 1.19.11 --node-count 1 --network-plugin kubenet --zones 3 --generate-ssh-keys --enable-addons monitoring --attach-acr images --tags "Component=kubernates-cluster"
```

### create cosmos-Db

```
az cosmosdb create --resource-group osdemorg --name demoPT --kind MongoDB  --server-version 4.0 --capabilities EnableServerless --locations regionName=eastus --tags "Component=CosmosDb"
```

### string connection string for postgres server with ssl in cloud in java

1. convert the client.pem file into .pk8 format by gitbash

2. create string pass all certificates i.e.
   
   ```
   String url =
   "jdbc:postgresql://10.207.206.890:5432/test_sit?sslmode=prefer&sslrootcert=C:/Users/sawan/Downloads/certificates/certifi/DBUser/server-ca-sit.pem&sslcert=C:/Users/sawan/Downloads/certificates/certifi/DBUser/client-cert-sit.pem&sslkey=C:/Users/sawan/Downloads/certificates/certifi/DBUser/client-key-sit4.pk8&sslpassword=root123";
   ```

### set TimeZone in dockerfile

```
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN date
```

### defender plans enable disable in subscription

```
microsoft defender for cloud-->getting started-->cofigure multi cloud-->Enviornment setting-->subscription-->defender plan
```

### update throughput in cosmosdb in azure

```
az cosmosdb mongodb collection throughput update -a <db_name> -d <collection_db_name> --name <collection_name> -g <resource_group_name> --max-throughput <count_of_throughput>
```

### Setup portainer in Docker

- create volume for portainer data in docker
  
  ```
  docker volume create portainer_data
  ```

- run the portainer container
  
  ```
  docker run -d -p 8160:9000 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:2.9.3
  ```

### Specifying a default Docker storage directory custom directory for manually installed Docker

- Remove all Docker containers and images.
  
  ```
  sudo docker rm -f $(docker ps -aq); docker rmi -f $(docker images -q)
  ```

- Stop the Docker service.
  
  ```
  sudo systemctl stop docker
  ```

- Remove the Docker storage directory.
  
  ```
  sudo rm -rf /var/lib/docker
  ```

- Create a new /var/lib/docker storage directory.
  
  ```
  mkdir /data/test/mnt/docker
  ```

- Note: 
  
  - A /var/lib/docker directory with less than 50 GB disk space isn’t supported.

- Use bind mount to set the new location. For example, to set the new location as /data/test/mnt/docker run commands
  
  ```
  mount --rbind /data/test/mnt/docker /var/lib/docker
  ```

- Start the Docker service
  
  ```
  sudo systemctl start docker
  ```

### edit security policy in Microsoft defender

```
Home-->Microsoft Defender for Cloud-->Environment settings-->Security Policy-->select Subscription-->Edit assignment-->Define Parameter-->{Allowed Regex for ACR-->^[^\/]+\.azurecr\.io\/.+$}
```

### ingress|application gateway|nginx inbound rule ip

```
https://ipinfo.io
```

### for access kubernates cluster API

```
public ip - https://www.iplocation.net/find-ip-address
```

### Provider register: Register the Azure Policy provider

```
powershell - Register-AzResourceProvider -ProviderNamespace 'Microsoft.PolicyInsights'
bash       - az provider register --namespace 'Microsoft.PolicyInsights'
```

### setup anchore engine for scan docker images

```
curl -s https://ci-tools.anchore.io/inline_scan-latest -o anchoree.sh
chmod -x anchore.sh
./anchore.sh -t <timeout> scan dockerimagename
./anchore.sh -t 600 scan dockerimagename
```

### store result in report

```
./anchore.sh -r dockerimagename
```

### security rule for Application Gateway NSG

- add `Application gateway` subnet to the `NSG`
  
  | priority | Name                    | port        | protocol | source            | destination | Action | Remark     |
  | -------- | ----------------------- | ----------- | -------- | ----------------- | ----------- | ------ | ---------- |
  | 100      | Allow_GWM               | 65200-65535 | Any      | GatewayManager    | Any         | Allow  | ServiceTag |
  | 110      | Allow_AzureLoadBalancer | Any         | Any      | AzureLoadBalancer | Any         | Allow  | ServiceTag |

### Update public Ip FQDN name

- Public IP address of your ingress controller

```
IP="20.106.165.30"
```

- Name to associate with public IP address

```
DNSNAME="demo-aks-ingress"
```

- Get the resource-id of the public ip

```
PUBLICIPID=$(az network public-ip list --query "[?ipAddress!=null]|[?contains(ipAddress, '$IP')].[id]" --output tsv)
```

- Update public ip address with DNS name

```
az network public-ip update --ids $PUBLICIPID --dns-name $DNSNAME
```

- Display the FQDN

```
az network public-ip show --ids $PUBLICIPID --query "[dnsSettings.fqdn]" --output tsv
```

### import image to acr from external repository

```
az acr import --name $REGISTRY_NAME --source $CERT_MANAGER_REGISTRY/$CERT_MANAGER_IMAGE_CONTROLLER:$CERT_MANAGER_TAG --image $CERT_MANAGER_IMAGE_CONTROLLER:$CERT_MANAGER_TAG
```

### create docker container as non-root user

```
RUN groupadd -r T12903789 --gid 1073 && useradd -d /home/T12903789 -ms /bin/bash -r -g T12903789 T12903789 --uid 1072
RUN chown -Rf T12903789:T12903789 /usr/local
```

### domain name for public ip

```
http://frontend.${public_ip}.nip.io/
http://frontend.52-150-19-70.nip.io/
```

### mount to another storage account directly from the Azure Cloud Shell

```
clouddrive mount -s mySubscription -g myRG -n storageAccountName -f fileShareName
```

### given access to other user in resources assigned a role

```
User Access Administrator Role
```

### install azure cli in centos

- Import the Microsoft repository key.

```
sudo rpm --import http://packages.microsoft.com/keys/microsoft.asc
```

- Create local azure-cli repository information.

```
echo -e "[azure-cli]
name=Azure CLI
baseurl=http://packages.microsoft.com/yumrepos/azure-cli
enabled=1
gpgcheck=1
gpgkey=http://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/azure-cli.repo
```

- install with or w/o gpgkey

```
yum install azure-cli --nogpgkey
```

### Add the following to the install.ps1 file in powershell to enable web server with default html file

- File `install.ps1` in VM

- Add-WindowsFeature Web-Server Set-Content -Path "C:\inetpub\wwwroot\Default.html" -Value "This is the server $($env:computername) !"

### Execute the following commands for custom script extensions by install install.ps1 by storage account

```
$config = @{
  "fileUris" = (,"http://webstorelog1000.blob.core.windows.net/script/install.ps1");
  "commandToExecute" = "powershell -ExecutionPolicy Unrestricted -File install.ps1"
}
$set = Get-AzVmss -ResourceGroupName "test-grp" -VMScaleSetName "demoscaleset"
$set = Add-AzVmssExtension -VirtualMachineScaleSet $set -Name "customScript" -Publisher "Microsoft.Compute" -Type "CustomScriptExtension" -TypeHandlerVersion 1.9 -Setting $config
Update-AzVmss -ResourceGroupName "test-grp" -Name "demoscaleset" -VirtualMachineScaleSet $set
```

### Enable multiple RDP session for Windows

1. Log into the server, where the Remote Desktop Services are installed.

2. Open the start screen (press the Windows key) and type gpedit.msc and open it.

3. Go to Computer Configuration > Administrative Templates > Windows Components > Remote Desktop Services > Remote Desktop Session Host > Connections.

4. Set Restrict Remote Desktop Services user to a single Remote Desktop Services session to Disabled.

5. Double click Limit number of connections and set the RD Maximum Connections allowed to 999999.

### Disable Multiple RDP Sessions

1. Log into the server, where the Remote Desktop Services are installed.

2. Open the start screen (press the Windows key) and type gpedit.msc and open it.

3. Go to Computer Configuration > Administrative Templates > Windows Components > Remote Desktop Services > Remote Desktop Session Host > Connections.

4. Set Restrict Remote Desktop Services user to a single Remote Desktop Services session to Enabled.

### for opening chrome in Multiple RDP session by cmd

```
chrome.exe --user-data-dir="C:\temp\osdemouser"
cd C:\Program Files\Google\Chrome\Application
chrome.exe --user-data-dir=%LOCALAPPDATA%\Google\Chrome\sawan
```

### deploy Azure conatiner instance by Yaml file

- create `appdeployment.yaml` file
  
  ```
  apiVersion: 2019-12-01
  location: northeurope
  name: AppGroup
  properties:
  containers: 
  - name: app
      properties:
      image: appregistry10002313.azurecr.io/myapp:latest
      resources:
          requests:
          cpu: 1
          memoryInGb: 1.5
      ports:
      - port: 80   
  osType: Linux
  ipAddress:
      type: Public
      ports:
      - protocol: tcp
      port: 80    
  imageRegistryCredentials:
      - server: appregistry10002313.azurecr.io
      username: appregistry10002313
      password: RGhhcWieDFffTCZ2DPYe=QEDqKr4NGbI
  type: Microsoft.ContainerInstance/containerGroups
  ```

- Deploy the yaml file by command
  
  ```
  az container create --resource-group container-grp --file appdeployment.yml
  ```

### Install azure cli in linux

1. Install the Azure command line interface
   
   ```
   curl -sL http://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc.gpg > /dev/null
   ```

2. Setup the repository
   
   ```
   AZ_REPO=$(lsb_release -cs)
   echo "deb [arch=amd64] http://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | sudo tee /etc/apt/sources.list.d/azure-cli.list
   ```

3. Update the package index
   
   ```
   sudo apt-get update
   ```

4. Install the Azure command line interface
   
   ```
   sudo apt-get install azure-cli
   ```

5. Login into Azure
   
   ```
   sudo az login
   ```

### Install docker in ubuntu VM

```
http://docs.docker.com/engine/install/ubuntu/
```

- Update the package index
  
  ```
  sudo apt-get update
  ```

- Install packages to allow apt to use the repository over HTTPS
  
  ```
  sudo apt-get install ca-certificates curl gnupg lsb-release
  ```

- Add Docker's official GPG key
  
  ```
  curl -fsSL http://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  ```

- Setup a stable repository
  
  ```
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] http://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  ```

- Update the package index
  
  ```
  sudo apt-get update
  ```

- Install docker, containerd
  
  ```
  sudo apt-get install docker-ce docker-ce-cli containerd.io
  ```

- Launching a container
  
  ```
  sudo docker run --name mynginx -p 80:80 -d nginx
  ```

### NSG rule setup for AzureBastionSubnet

```
https://francescomolfese.it/en/2020/06/come-configurare-il-servizio-azure-bastion-per-accedere-in-modo-sicuro-alle-macchine-virtuali/#:~:text=The%20Network%20Security%20Group%20(NSG,must%20include%20the%20following%20rules.&text=Inbound%20traffic%20from%20Internet%3A%20Azure,the%20Azure%20Bastion%20control%20plane.
```

- `Inbound Rule`
  
  | Priority | Name                      | Port | Protocol | Source         | Destination | Action |
  | -------- | ------------------------- | ---- | -------- | -------------- | ----------- | ------ |
  | 1000     | Allow-TCP443-FromInternet | 443  | TCP      | Internet       | any         | allow  |
  | 1001     | Allow-TCP443-FromGtwayMgr | 443  | TCP      | GatewayManager | any         | allow  |

- `Outbound Rule`
  
  | Priority | Name                      | Port    | Protocol | Source | Destination    | Action |
  | -------- | ------------------------- | ------- | -------- | ------ | -------------- | ------ |
  | 1000     | Allow-TCP3389_22-toVnet   | 3389,22 | TCP      | any    | VirtualNetwork | allow  |
  | 1001     | Allow-TCP443-toAzureCloud | 443     | TCP      | any    | AzureCloud     | allow  |

### Enable GUI in linux vm

- https://docs.microsoft.com/en-us/azure/virtual-machines/linux/use-remote-desktop

```
sudo apt-get update
sudo apt-get -y install xfce4
sudo apt install xfce4-session
sudo apt-get -y install xrdp
sudo systemctl enable xrdp
echo xfce4-session >~/.xsession
sudo service xrdp restart
```

### Open port in Azure VM

```
az vm open-port --resource-group myResourceGroup --name myVM --port 3389
```

### find azure cloud shell public ip

```
dig +short myip.opendns.com @resolver1.opendns.com
host myip.opendns.com resolver1.opendns.com | grep "myip.opendns.com has" | awk '{print $4}'
wget -qO- http://ipecho.net/plain | xargs echo
wget -qO - icanhazip.com
curl ifconfig.co
```

### #enable downloading in windowsVM

```
localserver-->IE enhance security configuration-->off-->off
```

### generate self-signed certificate for VPN gateway by powershell

```
http://docs.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-certificates-point-to-site
```

- Create a self-signed root certificate

```
$cert = New-SelfSignedCertificate -Type Custom -KeySpec Signature `
-Subject "CN=P2SRootCert" -KeyExportPolicy Exportable `
-HashAlgorithm sha256 -KeyLength 2048 `
-CertStoreLocation "Cert:\CurrentUser\My" -KeyUsageProperty Sign -KeyUsage CertSign
```

- Create a self-signed client certificate

```
New-SelfSignedCertificate -Type Custom -DnsName P2SChildCert -KeySpec Signature `
-Subject "CN=P2SChildCert" -KeyExportPolicy Exportable `
-HashAlgorithm sha256 -KeyLength 2048 `
-CertStoreLocation "Cert:\CurrentUser\My" `
-Signer $cert -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.2")
```

### point to site vpn connection establishnent

- **Server Side**
  
  1. export the root certificate with file in windows system
     
     ```
     windows-->manage-user-certificates-->certificate name-->right click on it-->All task-->export-->next-->select-->do not export private key-->save in the file in desktop(*.cer extension)-->save
     ```
  
  2. open the file copy the private key and paste into network gateway -->point-to-site configuration-->
  
  3. download VPN client and copy it to the client machine
  
  4. export the client certificate for client machine
     
     ```
     windows-->manage-user-certificates-->certificate name-->right click on it-->All task-->export-->next-->select-->export private key-->security-->enable password-->save in the file in desktop(*.pfx extension)-->save
     ```

- **Client side (Administrator Access)**
  
  1. install the client certificate in client machine with .pfx extension generated earlier
     
     ```
     windows-->manage-user-certificates-->certificate name-->right click on it-->All task-->export-->next-->select-->do not export private key-->save in the file in desktop(*.cer extension)-->save
     ```
  
  2. copy the vpn client zip folder to temp folder
  
  3. extract it
  
  4. run the application with respect to the OS
  
  5. Go to VPN setting from windows search bar
  
  6. select `azure network-->connect`

### Lab - Point-to-Site VPN - Using Azure AD Authentication - Reference

1. Use the following URL to register the Azure VPN enterprise application

```
https://login.microsoftonline.com/common/oauth2/authorize?client_id=41b23e61-6c1e-4545-b367-cd054e0ed4b4&response_type=code&redirect_uri=http://portal.azure.com&nonce=1234&prompt=admin_consent
```

2. When configuring the Point-to-Site VPN connection , use the following as a reference. Remember to change the directory ID
   
   ```
   Audience
   41b23e61-6c1e-4545-b367-cd054e0ed4b4
   
   Issuer
   http://sts.windows.net/70c0f6d9-7f3b-4425-a6b6-09b47643ec58/
   ```

### webserver for windows VM with public IP default page

```
C:\inetpub\wwwroot\Default.html
Windows server manager-->add roles and features--->next-->next-->select webserver checkbox-->next-->next-->install
```

### Add Azure load balancer for Webserver between VM

1. create `public ip`

2. dissassociate `public Ip` of VM and make `private IP` static for the webserver VM

3. create `basic/standard azure load balancer`
   
   - frontend ip confiduration--->add public ip
   
   - add backend pool-->name/vnet name/vm associate/add both webserver VM IP
   
   - add new health probe-->TCP protocal/name/port/interval/unhealthy threshhold
   
   - add Load Balancing rule-->name/frontendpublicIp/protocol/port/backend port/Health probe/    
   
   - add NAT inbound rule for specific load vm direct and with respect to port

### enable apm in tomcat by setenv.sh file

```
export JAVA_OPTS="$JAVA_OPTS -javaagent:elastic-apm-agent-1.26.0.jar"
export JAVA_OPTS="$JAVA_OPTS -Delastic.apm.service_name=poc-test-services"
export JAVA_OPTS="$JAVA_OPTS -Delastic.apm.application_packages=com.java.app.code"
export JAVA_OPTS="$JAVA_OPTS -Delastic.apm.server_url=http://apm-server-apm-server:8200"
```

### find public ip of system by powershell or search "whatsmyip" on google

```
(Invoke-WebRequest whatsmyip.strath.ac.uk).content.trim()|findstr ip:
```

### shell script to check resources in azure

- Create Resource Group or use existing one if exists
  
  ```
  validate_and_create_resource_group()
  {
      if [ $(az group exists --name microservices) = false ]
      then
          display_success Creating resource group microservices
          az group create --name microservices --location eastus > /dev/null 2>&1
          if [ $? -eq "0" ]
          then
              display_success Created resource group microservices
          else
              display_error Unable to Creating resource group microservices
              exit
          fi                    
      else
          MESSAGE="Resource Group microservices already exists. Using existing one.."
      fi
  }
  create_container_registry()
  {        
      res=`az resource list --name testimages --resource-group osdemorg --output tsv`
      if [ -z "$res" ]
      then
          echo "Creating Container Registry testimages in resource group osdemorg"
          az acr create --resource-group osdemorg --name testimages --sku Standard --location eastus            
          res=`az resource list --name testimages --resource-group osdemorg --output tsv`            
          if [ ! -z "$res" ]
          then
              echo "Successfully Created Container Registry  testimages in resource group osdemorg"
          else
              echo "display_error Unable to create Container Registry testimages in resource group osdemorg"
          fi
      else
          MESSAGE="Container Registry testimages in resource group osdemorg already in use.Using existing one..."
          echo $MESSAGE
      fi    
  }
  ```

### DISK attached to THE VM linux

- storage disk check

```
lsblk -o NAME,HCTL,SIZE,MOUNTPOINT | grep -i "sd"
output:
sda     0:0:0:0      30G
├─sda1             29.9G /
├─sda14               4M
└─sda15             106M /boot/efi
sdb     1:0:1:0      14G
└─sdb1               14G /mnt
sdc     3:0:0:0       4G(attached but not mounted)
```

- Partition a new disk

- If you are using an existing disk that contains data, skip to mounting the disk. If you are attaching a new disk, you need to partition the disk.

- The parted utility can be used to partition and to format a data disk.

- The following example uses parted on /dev/sdc, which is where the first data disk will typically be on most VMs. 

- Replace sda with the correct option for your disk. We are also formatting it using the XFS filesystem.

```
sudo parted /dev/sdc --script mklabel gpt mkpart xfspart xfs 0% 100%
sudo mkfs.xfs /dev/sdc1
sudo partprobe /dev/sdc1
```

- remark :
  
  - Use the partprobe utility to make sure the kernel is aware of the new partition and filesystem. 
  
  - Failure to use partprobe can cause the blkid or lslbk commands to not return the UUID for the new filesystem immediately

- Mount the disk

- Create a directory to mount the file system using mkdir. The following example creates a directory at /datadrive:

```
sudo mkdir /datadrive
```

- Use mount to then mount the filesystem. The following example mounts the /dev/sdc1 partition to the /datadrive mount point:

```
sudo mount /dev/sdc1 /datadrive
```

- remark:
  
  - To ensure that the drive is remounted automatically after a reboot, it must be added to the /etc/fstab file.
  
  - It is also highly recommended that the UUID (Universally Unique Identifier) is used in /etc/fstab to refer to the drive rather than just the device name (such as, /dev/sdc1). 
  
  - If the OS detects a disk error during boot, using the UUID avoids the incorrect disk being mounted to a given location.

- To find the UUID of the new drive, use the blkid utility:

```
sudo blkid
output:
/dev/sda1: LABEL="cloudimg-rootfs" UUID="11111111-1b1b-1c1c-1d1d-1e1e1e1e1e1e" TYPE="ext4" PARTUUID="1a1b1c1d-11aa-1234-1a1a1a1a1a1a"
/dev/sda15: LABEL="UEFI" UUID="BCD7-96A6" TYPE="vfat" PARTUUID="1e1g1cg1h-11aa-1234-1u1u1a1a1u1u"
/dev/sdb1: UUID="22222222-2b2b-2c2c-2d2d-2e2e2e2e2e2e" TYPE="ext4" TYPE="ext4" PARTUUID="1a2b3c4d-01"
/dev/sda14: PARTUUID="2e2g2cg2h-11aa-1234-1u1u1a1a1u1u"
/dev/sdc1: UUID="33333333-3b3b-3c3c-3d3d-3e3e3e3e3e3e" TYPE="xfs" PARTLABEL="xfspart" PARTUUID="c1c2c3c4-1234-cdef-asdf3456ghjk"
```

- open the /etc/fstab file in a text editor as follows:

- first copy the old file for backup

```
sudo nano/vi /etc/fstab
```

- Add the following line to the end of the /etc/fstab file:

```
UUID=33333333-3b3b-3c3c-3d3d-3e3e3e3e3e3e(random example purpose only)   /datadrive   xfs   defaults,nofail   1   2
UUID=1a13b7ba-8a94-4e03-a216-cb60bc427b5d /datadrive   xfs   defaults,nofail   1   2
```

- Verify the disk

```
lsblk -o NAME,HCTL,SIZE,MOUNTPOINT | grep -i "sd"
output:
sda     0:0:0:0      30G
├─sda1             29.9G /
├─sda14               4M
└─sda15             106M /boot/efi
sdb     1:0:1:0      14G
└─sdb1               14G /mnt
sdc     3:0:0:0       4G
└─sdc1                4G /datadrive(mounted ready for use)
```

### DISK attached to THE VM windows

- **winsdows server-->**
  
  - **configuration-->**
    
    - **storage & disk--->**
      
      - **select disk--->**
        
        - **right click and intialize--->**
          
          - **right click new volume with drive name or letter**

### Encryption of disk by self managed key

1. create key vault

2. select keys

3. **generate/import keys with -->generate-->key name-->key type-->RSA-->RSA key size-->2048-->create**

4. go to disk enryption set in azure portal

5. **select-->name-->resource-group-->key-vault-name-->key-->version-->review+create**

6. stopped deallocate vm first

7. select the disk which you want to encrypt

8. **select-->encryption-->encryption-type-->Encryption at rest with a customer managed keys-->disk-encryption-set-->save**

### ADE(Azure Disk Encryption) of disk

1. create key vault-->enable azure disk encryption feature

2. select keys

3. **generate/import keys with -->generate-->key name-->key type-->RSA-->RSA key size-->2048-->create**

4. stopped deallocate vm first

5. select the disk which you want to encrypt

6. go to additional setting in disk windows of vm 

7. select the all disk

8. **select-->encryption-->encryption-type-->Encryption at rest with a customer managed keys-->disk-encryption-set-->save**

### Role Management and access to user

```
subscription--><resource>-->IAM-->Add role Management-->Add user details
```

### ipwhitelist for postgresql flexibal-server

```
az postgres flexible-server firewall-rule create --resource-group $resource-group-name --name $db-server-name --rule-name $user_name --start-ip-address $ip_address --end-ip-address $ip_address
```

### start stop restart postgresql flexible-server

```
az postgres flexible-server restart --name testpsql --resource-group $Resourcegroup
```

### azure login from cli

```
az login -u <username> -p <password>
```

### start/stop kubernates cluster

```
az aks start|stop --resource-group osdemorg --name aks-Pt
```

### Automatic Assigned Public IP for Installing NGINX ingress in AKS for Load Balancer

```
http://docs.microsoft.com/en-us/azure/aks/ingress-basic
```

1. Create a namespace for your ingress resources

```
kubectl create namespace ingress-basic
```

2. Add the ingress-nginx repository

```
helm repo add ingress-nginx http://kubernetes.github.io/ingress-nginx
```

3. Use Helm to deploy an NGINX ingress controller

```
helm install nginx-ingress ingress-nginx/ingress-nginx \
    --namespace ingress-basic \
    --set controller.replicaCount=2 \
    --set controller.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set defaultBackend.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set controller.admissionWebhooks.patch.nodeSelector."beta\.kubernetes\.io/os"=linux
```

4 let's generate a self-signed certificate with openssl.

```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -out aks-ingress-tls.crt \
    -keyout aks-ingress-tls.key \
    -subj "/CN=blue-green.eastus.cloudapp.azure.com/O=aks-ingress-tls"
```

5. create AKS secret for TLS/SSl certification key or certificate

```
kubectl create secret tls aks-ingress-tls \
    --namespace ingress-basic \
    --key aks-ingress-tls.key \
    --cert aks-ingress-tls.crt
```

6. The tls section tells the ingress route to use the Secret named aks-ingress-tls for the host omnistore.retail.com

```
spec:
  tls:
  - hosts:
    - demo.azure.com
    secretName: aks-ingress-tls
  rules:
  - host: demo.azure.com
```

7. To check the Dynamic IP in assigned to loadbalancer

```
kubectl --namespace ingress-basic get services -o wide -w nginx-ingress-ingress-nginx-controller
```

8. To get loadbalancer Externalip in variable

```
LoadBalancerIP=$(kubectl get services -n ingress-basic nginx-ingress-ingress-nginx-controller --output jsonpath='{.status.loadBalancer.ingress[0].ip}')
```

9. to delete namespace and resources inside it

```
kubectl delete namespace <ingress-basic(name of namespace)>
```

### Static Assigned Public IP for Installing NGINX ingress in AKS for Load Balancer

1. Create Static Public IP for ingress

2. Get the resource group name of the AKS cluster 

```
AKS_RG=$(az aks show --resource-group osdemorg --name offers-aks --query nodeResourceGroup -o tsv)
```

3. TEMPLATE - Create a public IP address with the static allocation

```
az network public-ip create --resource-group <REPLACE-OUTPUT-RG-FROM-PREVIOUS-COMMAND> --name myAKSPublicIPForIngress --sku Standard --allocation-method static --query publicIp.ipAddress -o tsv
```

4. REPLACE - Create Public IP: Replace Resource Group value

```
PUBLIC_IP=$(az network public-ip create --resource-group $AKS_RG \
                            --name myAKSPublicIPForIngress \
                            --sku Standard \
                            --allocation-method static \
                            --query publicIp.ipAddress \
                            -o tsv)
```

5. note down the public_IP or store it in varible

```
52.154.156.139
```

6. Install Ingress Controller

7. Install Helm3 (if not installed)

```
brew install helm
```

8. Create a namespace for your ingress resources

```
kubectl create namespace ingress-basic
```

9. Add the official stable repository

```
helm repo add ingress-nginx http://kubernetes.github.io/ingress-nginx
helm repo add stable http://kubernetes-charts.storage.googleapis.com/
helm repo update
```

10. Customizing the Chart Before Installing. 

```
helm show values ingress-nginx/ingress-nginx
```

11. Use Helm to deploy an NGINX ingress controller

```
helm install ingress-nginx ingress-nginx/ingress-nginx \
    --namespace ingress-basic \
    --set controller.replicaCount=2 \
    --set controller.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set defaultBackend.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set controller.service.externalTrafficPolicy=Local \
    --set controller.service.loadBalancerIP="REPLACE_STATIC_IP" 
```

12. List Pods

```
kubectl get pods -n ingress-basic
kubectl get all -n ingress-basic
```

13. Access Public IP

```
http://<Public-IP-created-for-Ingress>
```

### aks images pull from ACR using service principal and kubernates secret

- Create Service Principal to access Azure Container Registry
  
  - Update ACR_NAME with your container registry name
  - Update SERVICE_PRINCIPAL_NAME as desired

- Review file: shell-script/generate-service-principal.sh

```
#!/bin/bash

# Modify for your environment.
# ACR_NAME: The name of your Azure Container Registry
# SERVICE_PRINCIPAL_NAME: Must be unique within your AD tenant
#ACR_NAME=<container-registry-name>
ACR_NAME=acrdemo2ss
SERVICE_PRINCIPAL_NAME=acr-sp-demo

# Obtain the full registry ID for subsequent command args
ACR_REGISTRY_ID=$(az acr show --name $ACR_NAME --query id --output tsv)

# Create the service principal with rights scoped to the registry.
# Default permissions are for docker pull access. Modify the '--role'
# argument value as desired:
# acrpull:     pull only
# acrpush:     push and pull
# owner:       push, pull, and assign roles
SP_PASSWD=$(az ad sp create-for-rbac --name http://$SERVICE_PRINCIPAL_NAME --scopes $ACR_REGISTRY_ID --role acrpull --query password --output tsv)
SP_APP_ID=$(az ad sp show --id http://$SERVICE_PRINCIPAL_NAME --query appId --output tsv)

# Output the service principal's credentials; use these in your services and
# applications to authenticate to the container registry.
echo "Service principal ID: $SP_APP_ID"
echo "Service principal password: $SP_PASSWD"
```

### disable monetring|insight in kubernates

```
az aks disable-addons -a monitoring -n cluster-name -g resource-group-name
```

### check az version

```
az version
```

### List Node Pools

```
az aks nodepool list --cluster-name ClusterName --resource-group ResourceGrouName -o table
```

### Create New Linux Node Pool

```
az aks nodepool add --resource-group AKS_RESOURCE_GROUP \
                    --cluster-name AKS_CLUSTER_NAME \
                    --name Name_Of_Node \
                    --node-count 1 \
                    --enable-cluster-autoscaler \
                    --max-count 5 \
                    --min-count 1 \
                    --mode User \
                    --node-vm-size Standard_DS2_v2 \
                    --os-type Linux \
                    --labels nodepool-type=user environment=production nodepoolos=linux app=java-apps \
                    --zones {1,2,3}
                    --tags nodepool-type=user environment=production nodepoolos=linux app=java-apps
```

### List Nodes using Labels where nodepoolos=linux where -l stands for label

```
kubectl get nodes -o wide -l nodepoolos=linux
```

### az account login with tenant

```
az login --tenant TENANT_ID
```

### register feature az-cli by command in cloud shell

```
az feature register --namespace Microsoft.ContainerService -n AutoUpgradePreview
```

### Azure cli Az storage account Queue

- To create a Queue:

```
az storage queue create --name Qname --account-name myAcc --account-key Mykey.
```

- To delete the existing Queue:

```
az storage queue delete --name Qname --account-name Myacc --account-key Acckey 
```

- To put a message in a Queue:

```
az storage message put --content mymessage --queue-name qname 
```

- To get a message in Queue:

```
az storage message get --queue-name Qname
```

- To retrieve one or more messages from the front of the queue:

```
az storage message peek --queue-name Qname.
```

### Azure cli Az storage account Table

- To create a table:

```
az storage table create --name sawan --account-name sawan --access-key <Storage Account Access Key>
```

- To delete a table:

```
az storage table delete --name tablename --account-name Accname --access-key Acckey
```

- To insert a storage entity into a table:

```
az storage entity insert --connection-string DefaultEndpointsProtocol=http;AccountName=sawan;AccountKey=<Storage Account Access key>;EndpointSuffix=core.windows.net --entity PartitionKey=AAA RowKey=BBB Content=ASDF2 --table-name sawan
```

- To update an existing entity:

```
az storage entity merge --entity PartitionKey=AAA RowKey=BBB Content=ASDF2 --table-name tableName --account-key accKey --account-name accountName --connection-string $connectionString
```

- To delete an entity:

```
az storage entity delete --partition-key KEY --row-key RKEY --table-name TName.
```

- To read an entity:

```
az storage entity show --table-name MyTable --partition-key KEY --row-key RKEY
```

- To query entities:

```
az storage entity query -t MyTable --filter "PartitionKey eq 'AAA'"
```

### mount cloudrive in azure cli

- note : storage account should be same region for multiple storage acount mount in cloud shell

```
clouddrive mount -s <subscription_name> -g <resource-group-name> -n <storage_account_name> -f <file_share_name>
```

### remove existing cloud storage account

```
clouddrive unmount
```

### to see mount storage account

```
df
```

### deployment by ARM template in azure CLI

```
az deployment group create --resource-group <name_of_resource_group> --template-file <path_of_template.json file> --parameters <path_of_parameter.json>
```

### deployment by ARM template in azure powershell

```
New-AzResourceGroupDeployment ResourceGrouName app-grp -TemplateFile template01.json -TemplateParameterFile parameters.json
```

### to watch network topology of network

- search `Network Watcher` in Azure portal

### active directory (azure AD)

```
tenant(also called directory)---->subscription(more than one possible)
```

### azure (AD connect) with on-prem data directory with single user base

```
on-primesis AD<------------>Azure AD /MS apps<----user/device sign in
```

### Create a firewall rule on Azure Database for MySQL Server

```
az mysql server firewall-rule create --resource-group myresourcegroup --server-name mydemoserver --name FirewallRule1 --start-ip-address 1.1.1.1 --end-ip-address 1.1.1.1
```

### public domain name server in azure

1. craete DNS zones

2. buy a domain from third party services

3. register the azure DNS server Name server in Domain service register name server(for domain buy godaddy.com)

4. add record with web server Ip in DNS zone

5. add inbound rule for Port 80 for web server (VM)

### ssl self signed certificate for an IP-Address

1. Create a request configuration file as follows (this is just a plain text file — and you can name it whatever you like)
   
   - file-name = `certificate.cnf`
     
     ```
     [req]
     default_bits = 4096
     default_md = sha256
     distinguished_name = req_distinguished_name
     x509_extensions = v3_req
     prompt = no
     
     [req_distinguished_name]
     C = US
     ST = VA
     L = SomeCity
     O = MyCompany
     OU = MyDivision
     CN = 192.168.13.10
     
     [v3_req]
     keyUsage = keyEncipherment, dataEncipherment
     extendedKeyUsage = serverAuth
     subjectAltName = @alt_names
     
     [alt_names]
     IP.1 = 192.168.13.10
     ```

2. Generate the certificate and private key using the config file you created above
   
   ```
   openssl req -new -nodes -x509 -days 365 -keyout domain.key -out domain.crt -config certificate.cnf
   ```

3. Verify the certificate has an IP SAN by running the following command
   
   ```
   openssl x509 -in domain.crt -noout -text
   ```

4. This will output the contents of the cert for you to inspect. 
   
   - While there is a lot there, you are looking for a couple lines like this:
     
     ```
     X509v3 Subject Alternative Name:
     IP Address:192.168.13.10
     ```

### push images to ACR by az command

```
az acr build --image images.azurecr.io/salenew:example --registry images --file Dockerfile .
```

### create vm sql server for data by select sql server image

```
ls
chmod 400 my-sql-server-vm_key.pem
ssh -i my-sql-server-vm_key.pem azureuser@13.78.236.186 
ls /opt/mssql/bin 
sudo /opt/mssql/bin/mssql-conf set-sa-password 
sudo systemctl stop mssql-server
sudo systemctl start mssql-server 
cd /opt/mssql-tools/bin
./sqlcmd -S localhost -U SA -p
```

### AzCopy Tool - Commands

- To create a container

```
azcopy make "https://appstore4040.blob.core.windows.net/tmp?sv=2020-08-04&ss=b&srt=sco&sp=rwdlac&se=2021-12-13T14:36:11Z&st=2021-12-13T06:36:11Z&spr=https&sig=RtWuKGVi%2BTp1yW1VNAqgSFMmFtrRrEsQ9f%2BJy7LuIZU%3D"
```

- To upload a file

```
azcopy copy storage1.arm.json "https://appstore4040.blob.core.windows.net/tmp/storage1.arm.json?sv=2020-08-04&ss=b&srt=sco&sp=rwdlac&se=2021-12-13T14:36:11Z&st=2021-12-13T06:36:11Z&spr=https&sig=RtWuKGVi%2BTp1yW1VNAqgSFMmFtrRrEsQ9f%2BJy7LuIZU%3D"
```

- To upload a directory

```
azcopy copy "newdir/*" "https://appstore4040.blob.core.windows.net/tmp?sv=2020-08-04&ss=b&srt=sco&sp=rwdlac&se=2021-12-13T14:36:11Z&st=2021-12-13T06:36:11Z&spr=https&sig=RtWuKGVi%2BTp1yW1VNAqgSFMmFtrRrEsQ9f%2BJy7LuIZU%3D"
```

- To upload a directory to a directory in the container

```
azcopy copy "newdir/*" "https://appstore4040.blob.core.windows.net/tmp/newdir?sv=2020-08-04&ss=b&srt=sco&sp=rwdlac&se=2021-12-13T14:36:11Z&st=2021-12-13T06:36:11Z&spr=https&sig=RtWuKGVi%2BTp1yW1VNAqgSFMmFtrRrEsQ9f%2BJy7LuIZU%3D"
```

- To upload a directory and subdirectories to a directory in the container

```
azcopy copy "newdir/*" "https://appstore4040.blob.core.windows.net/tmp/newdir?sv=2020-08-04&ss=b&srt=sco&sp=rwdlac&se=2021-12-13T14:36:11Z&st=2021-12-13T06:36:11Z&spr=https&sig=RtWuKGVi%2BTp1yW1VNAqgSFMmFtrRrEsQ9f%2BJy7LuIZU%3D" --recursive
```

- Download blob data

```
azcopy copy "https://appstore4040.blob.core.windows.net/tmp/storage1.arm.json?sv=2020-08-04&ss=b&srt=sco&sp=rwdlac&se=2021-12-13T14:36:11Z&st=2021-12-13T06:36:11Z&spr=https&sig=RtWuKGVi%2BTp1yW1VNAqgSFMmFtrRrEsQ9f%2BJy7LuIZU%3D" "storage1.arm.json"
```

- copy data between two storage accounts

```
azcopy copy "https://appstore4040.blob.core.windows.net/tmp?sv=2020-08-04&ss=b&srt=sco&sp=rwdlac&se=2021-12-13T14:36:11Z&st=2021-12-13T06:36:11Z&spr=https&sig=RtWuKGVi%2BTp1yW1VNAqgSFMmFtrRrEsQ9f%2BJy7LuIZU%3D" "https://azcopydestination100034.blob.core.windows.net/tmp?sv=2020-02-10&ss=b&srt=sco&sp=rwlac&se=2021-04-12T22:26:24Z&st=2021-04-12T14:26:24Z&spr=https&sig=TMv5LmpR0RKwpg%2B8F19Q1aLNlKUyn36%2B0B5qqu5fGok%3D" --recursive
```

- remove folder from command 

```
azcopy remove "http://csb1003200094uio0987.file.core.windows.net/cs-poc-5678-com-1003200094uio0987/user/poc-5678-home/logs/os-pos-services?sv=2020-10-02&se=2022-03-11T05%3A40%3A29Z&sr=s&sp=rwdl&sig=YcX%2Fpi%2B%2BRy%2B1kJultV88pHgfnfr1UoxzOmJPeb07VAw%3D" --recursive --log-level=INFO;
./azcopy.exe remove "http://csb1003200094uio0987.file.core.windows.net/cs-poc-5678-com-1003200094uio0987/user/poc-5678-home/logs/os-pos-services?sv=2020-10-02&se=2022-03-11T05%3A40%3A29Z&sr=s&sp=rwdl&sig=YcX%2Fpi%2B%2BRy%2B1kJultV88pHgfnfr1UoxzOmJPeb07VAw%3D" --from-to=FileTrash --recursive --log-level=INFO;
$env:AZCOPY_CRED_TYPE = "Anonymous";
./azcopy.exe remove "https://csb1003200094uio0987.file.core.windows.net/cs-poc-5678-com-1003200094uio0987/microservices-new/logs/os-transaction-poster-application?sv=2021-04-10&se=2022-10-26T10%3A05%3A19Z&sr=s&sp=rwdl&sig=YG55eKX8fgfPOlNbg09PB26NHmxPLI1LAdIDYAjqY0U%3D" --from-to=FileTrash --recursive --log-level=INFO;
$env:AZCOPY_CRED_TYPE = "";
```

- upload file in azure fileshare by azcopy

```
azcopy copy "<file name>" "<storage_account_name>/<file_share_name>?<SAS token> --recursive"
azcopy copy "ga.sql" "http://csb1003200094uio0987.file.core.windows.net/cs-poc-5678-com-1003200094uio0987?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2021-11-26T23:05:25Z&st=2021-11-26T15:05:25Z&spr=http&sig=mnWC6DQfqHvUUqT%2FwLKJLFQHjt%2FgKPPoLCWfVaeiOsM%3D"
```

- download file from azure fileshare by az copy

```
azcopy copy "<storage_account_name>/<file_share_name>/<file-path>?<SAS token>" "<local_path> --recursive"
azcopy copy "http://csb1003200094uio0987.file.core.windows.net/cs-poc-5678-com-1003200094uio0987/ga.sql?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2021-11-26T23:05:25Z&st=2021-11-26T15:05:25Z&spr=http&sig=mnWC6DQfqHvUUqT%2FwLKJLFQHjt%2FgKPPoLCWfVaeiOsM%3D" "C:\Users\1820387\Desktop\azure-tcs\SAAS\ga.sql"
```

- upload contents,file,directory in blob storage

```
az storage blob upload-batch -s C:\Users\1820387\Desktop\azure-tcs\HnM\UI -d $web --connection-string=DefaultEndpointsProtocol=http;AccountName=osmshnm;AccountKey=ijCUgD28VVaQYVijUASh1MD40f/xBLv7el7/qU/IOpndrYG3mH828YCxRZFOKgSPSoVVP79dKeCasI/ANZuDmA==;EndpointSuffix=core.windows.net
az storage blob upload-batch -s C:\Users\1820387\Desktop\azure-tcs\SAAS\01-docker-Images\os-ui-services\poc-5678-ec -d poc-5678-ec --connection-string=DefaultEndpointsProtocol=http;AccountName=retailpoc-5678;AccountKey=9o2PRt2dFcyOfJMoxoYPNixfKybvxVHuxUWgMyV7n4aL1YEjthYuQfr6Gy1NR7U+rYP5NoeW1HpR0mKw4AlgAw==;EndpointSuffix=core.windows.net
```

- delete content from blob storage

```
az storage blob delete-batch -s $web\poc-5678-pos-ms --connection-string=DefaultEndpointsProtocol=http;AccountName=osmshnm;AccountKey=ijCUgD28VVaQYVijUASh1MD40f/xBLv7el7/qU/IOpndrYG3mH828YCxRZFOKgSPSoVVP79dKeCasI/ANZuDmA==;EndpointSuffix=core.windows.net 
```

### powershell command

- to check all services running 

```
Get-Service
```

- to check service name with specific string "App"

```
Get-Service -Name "App*"
```

- to check service "running" with status

```
Get-Service -Name "App*"| Where-Object {$_.Status -eq "Running"}
```

- to run az cli command we can use file script .azcli extension

### Create Application Gateway and add to kubernates cluster

- Variable block

```
location="East US"
resourceGroup="blue-green"
vNet="blue-green-vnet"
addressPrefixVNet="10.0.0.0/16"
subnetAppGw="ingress-appgateway-subnet"
subnetPrefixAppGw="10.0.1.0/24"
publicIpAppGw="public-ip-app-gateway"
nameAppGw="myApplicationGateway"
nameAks="blue-green"
```

- Create a virtual network and a Application Gateway subnet.

```
echo "Creating $vNet and $subnetAppGw"
az network vnet create --resource-group $resourceGroup --name $vNet --address-prefix $addressPrefixVNet  --location "$location" --subnet-name $subnetAppGw --subnet-prefix $subnetPrefixAppGw
```

- Create a virtual network and a Application Gateway subnet.

```
echo "Creating $publicIpAppGw"
az network public-ip create -n $publicIpAppGw -g $resourceGroup --allocation-method Static --sku Standard
```

- Create a virtual network and a Application Gateway.

```
echo "Creating $applicationGatway"
az network application-gateway create -n $nameAppGw -l $location -g $resourceGroup --sku Standard_v2 --public-ip-address $publicIpAppGw --vnet-name $vNet --subnet $subnetAppGw
```

- Enable Application gateway in kubernates cluster

```
echo "Enable $nameApplicationGw application gateway ingress controller in $nameAks kubernates cluster"
appgwId=$(az network application-gateway show -n $nameAppGw -g $resourceGroup -o tsv --query "id") 
az aks enable-addons -n $nameAks -g $resourceGroup -a ingress-appgw --appgw-id $appgwId
```

- check profile enabled in kubernates cluster

```
az aks addon list -n k8s_name -g resource-group-name
```

### blueprint in Azure

- It is combination of resources,resource group ,policies ,roles and permission.

```
Stages : Defination --> Publishing --> Assigned(to Subscription) --> Done
```

```
Azure Portal-->BluePrint-->create a blueprint-->start with a blank blueprint-->BluePrint Name:Example-->BluePrint Description:Infomration about Blueprint-->Defination location:Subscription Name-->artifact-->add artifct-->Artifact type:Policy assignment,Roles assignment,ARM template,Resource Group-->fill artifact details after selection-->save draft
```

```
Azure Portal-->BluePrint-->Blueprint defination-->click on blueprint-->publish-->version:1.0.0-->chnage note:my first blueprint-->publish-->assign blueprint-->done
```

- we can delete blueprint if it is not assigned.

- We can lock the blueprint for deletion by select option 'dont Delete Me' while assigned to subscription

### Access azure-key-vault secret for kubernates cluster pod deployment

1. assign system managed identity aks vmss machine

```
az vmss identity assign <resource group> -n <vmss name>
az vmss identity assign -g MC_blue-green_blue-green_eastus -n aks-agentpool-36000420-vmss
```

2. show and copy the identity

```
az resource list -n <vmss name> --query [*].identity.principalId --out tsv
az resource list -n aks-agentpool-36000420-vmss --query [*].identity.principalId --out tsv
```

3. grant identity permissions that enable it to read your key vault and view its contents,assign keyvault access policy

```
az keyvault set-policy --name myKeyVault --object-id <object-id> --secret-permissions <secret-permissions> --key-permissions <key-permissions> --certificate-permissions <certificate-permissions>
az keyvault set-policy --name foo1 --object-id 5eaafbd8-75ac-4f90-8fbd-a2e2be49e7c9 --secret-permissions get list --key-permissions get list --certificate-permissions get list
az keyvault set-policy --name myKeyVault --spn <principalId> --secret-permissions <secret-permissions> --key-permissions <key-permissions> --certificate-permissions <certificate-permissions>
az keyvault set-policy --name foo1 --spn 5eaafbd8-75ac-4f90-8fbd-a2e2be49e7c9 --secret-permissions get list --key-permissions get list --certificate-permissions get list
```

4. create `secretproviderclass.yaml` as following

```
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: azure-sync
spec:
  provider: azure 
  parameters:
    usePodIdentity: "false"
    useVMManagedIdentity: "true"    # Set to true for using managed identity
    userAssignedIdentityID: ""      # If empty, then defaults to use the system assigned identity on the VM
    keyvaultName: foo1              # keyvault Name
    tenantId: 404b1967-6507-45ab-8a6d-7374a3f478be #keyvault tenant id or directory ID                           
    objects:  |
        array:
          - |
            objectName: foo1          #keyvault secret name
            objectType: secret        # object types: secret, key, or cert
            objectVersion: ""         # [OPTIONAL] object versions
  secretObjects:                      # secret object for kubernates cluster
  - secretName: foosecret             # name of kubernates secret object
    data:                         
    - key: password                   # key for the secret accessing it during deployment 
      objectName: foo1                # object name where keyvault secret stored in secretproviderclass
    type: Opaque                      
```

5. mount volume with csi and get access of secret by `deployment.yaml`

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: treatcore
spec:
  replicas: 1
  selector:
    matchLabels:
      app: treatcore
  template:
    metadata:
      labels:
        app: treatcore
    spec:
      volumes:
      - name: secrets-store01-inline
        csi:
          driver: secrets-store.csi.k8s.io
          readOnly: true
          volumeAttributes:
            secretProviderClass: "azure-sync"
      containers:      
      - name: treatcore
        image: poc-5678images.azurecr.io/treatcorenew:example        
        imagePullPolicy: Always
        readinessProbe:
          httpGet:
            path: /os-poc/manage/health
            port: 8163
          periodSeconds: 3
          timeoutSeconds: 1
        volumeMounts:
        - name: secrets-store01-inline
          mountPath: "/mnt/secrets-store"
          readOnly: true
        env:
        - name: DB_HOST
          value: "testpoc.mysql.database.azure.com"
        - name: DB_NAME
          value: "poc-5678_core"
        - name: DB_USER_NAME
          value: "treatadmin@treatcore"
        - name: DB_USER_PASS
          value: "treatadmin_123"
        #- name: DB_USER_PASS                    #for secret accessing by Azure key vault
        #  valueFrom:
        #    secretKeyRef:
        #      name: foosecret
        #      key: password
        - name: REDIS_HOST
          value: "ospoc.redis.cache.windows.net"
        - name: REDIS_PASS
          value: "wR6GtmytChbRt0owuMtbGzTphiobHYpiopijpojMU2+o="
        resources:
          requests:
            cpu: 250m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 2050Mi
        ports:
        - containerPort: 8163
      imagePullSecrets:
      - name: imagepull
---
apiVersion: v1
kind: Service
metadata:
  name: treatcore
spec:
  type: ClusterIP
  selector:
    app: treatcore
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8163
    - name: https
      protocol: TCP
      port: 443
      targetPort: 8163
```

### Automation code for VM stop

```
$connection = Get-AutomationConnection -Name AzureRunAsConnection
Connect-AzAccount -ServicePrincipal -Tenant $connection.TenantID -ApplicationId $connection.ApplicationID -CertificateThumbprint $connection.CertificateThumbprint
$context = (get-azcontext)
$subscriptions =$context.$subscription.Name
$azvm = get-azvm -resourcegroupname AzureAutomation-Demo | select Name
foreach ($i in $azvm.name) {Stop-azvm -resourcegroupname AzureAutomation-Demo -name $i -force}
```

### Max Fault Domain Recommendation  = 3

### MAx Update Domain Recommendation = 20

### PowerShell Desired State Configuration(Powershell DSC) custom extension

- It is configuration management tool for VM and used to run custom script.

### Manage Update for Azure VM by azure Automation Account

- **Update Management Overview**
  
  - Log Analytic Agent for Windows and Linux
  
  - Powershell DSC for Linux
  
  - Automation Hybrid Runbook Worker (Update on-prim as well azure VM)
  
  - Microsoft Update or Windows Server Update Services (WSUS) for Windows machines
    
    ```
    azure portal-->azure automation account-->update management-->Update Management-->Select According to requirements and schedule and also non-azure machines
    ```

### Azure Service Endpoint Vs Private Endpoint

- The biggest difference between Private Links and Service Endpoints is Public IPs. With Private Link, there is never any Public IP created and traffic can never go through the Internet, whereas with Service Endpoints, you have the option to limit access.

- The second key difference with Private Link is, once enabled, you have now granted access to a specific PaaS resource within your VNet. Meaning, you can control the egress to the PaaS resource.

- Service Endpoints are much simpler to implement and significantly reduce the complexity of your VNet/Architecture design.

- Private Link will always ensure traffic stays within your VNet.

- 

- This is something to factor when designing or implementing either solution, as Private Links will quickly add to your monthly spending.

- Another consideration is availability, meaning Service Endpoints and Private Links are not generally available for all services, for example. There is no Service Endpoint as of writing this post, for Azure Log Analytics. However, there is a solution for Private Links for Log Analytics. Both services are available but not for all resources/services.

- Ultimately, if you are considering either solution, Private Link versus Service Endpoint, then you are probably concerned with security, and with that said, Private Link is superior to Service Endpoints. The services available to Private Link will continue to grow like Service Endpoints, but based on my observation, it appears Private Link has a much deeper portfolio with Azure services integration.

### Azure Firewall

- Azure Firewall as a service

- Azure Firewall is a managed, cloud-based network security service that protects your Azure Virtual Network resources.

- It's a fully stateful firewall as a service with built-in high availability and unrestricted cloud scalability.

- You can centrally create, enforce, and log application and network connectivity policies across subscriptions and virtual networks.

- Azure Firewall uses a static public IP address for your virtual network resources allowing outside firewalls to identify traffic originating from your virtual network.

- The service is fully integrated with Azure Monitor for logging and analytics.

- High availability is built in, so no additional load balancers are required and there's nothing you need to configure. ✓ Azure Firewall can be configured during deployment to span multiple Availability Zones for increased availability.

- With Availability Zones, your availability increases to 99.99% uptime.

- There's no additional cost for a firewall deployed in an Availability Zone.

- However, there are additional costs for inbound and outbound data transfers associated with Availability
  Zones.

- For best performance, deploy one firewall per region.

- You can centrally create allow or deny network filtering rules by source and destination IP address, port, and protocol.

- FQDN tags make it easy for you to allow well-known Azure service network traffic through your firewall

- Service tags

- Threat intelligence

- Outbound SNAT support

- Inbound DNAT support

### Azure Firewall Known Issue and Limitatio

- Network filtering rules for non-TCP/UDP protocol(such as ICMP) don’t work for internet inbound traffic.

- You cannot move azure firewall to a different resource and subscription.

- Limited Port ranges

- NO custom DNS support except Azure DNS support only.

- No SNAT/DNAT for Private IP destination.

### Network Watcher

- Azure Network Watcher provides tools to monitor, diagnose, view metrics, and enable or disable logs for resources in an Azure virtual network.

- Network Watcher is designed to monitor and repair the network health of laaS (Infrastructure-as-a-Service) products which includes Virtual Machines, Virtual Networks, Application Gateways, Load balancers, etc. It is not intended for and will not work for PaaS monitoring or Web analytics.

### Network Watcher Monitoring

- The connection monitor capability monitors communication at a regular interval and informs reachability, latency, and network topology changes between the VM and the endpoint.

- If an endpoint becomes unreachable, connection troubleshoot informs you of the reason. Potential reasons are a
  DNS name resolution problem, the CPU, memory, or firewall within the operating system of a VM, or the hop
  type of a custom route, or security rule for the VM or subnet of the outbound connection.

- View resources in a virtual network and their relationships in Topology view and can be downloaded

- Diagnose Network Traffic filtering problems to or from a VM

- Diagnose network routing problems from a VM

- Diagnose outbound connections from a VM

- Capture packets to and from a VM

- Metrics

### WAF Policy

- We can create and manage WAF policy and assign it Application Gateway, Front Door and CDN profile also. 

### Privileged Identity Management(PIM)

- It required Azure AD Premium P2 license.

### Task Need to Peform After Subscription Transfer to Other ID

- keyvault : Change TENANT_ID on any key vault

- Re-Enable all managed identities

- Re-Register azure stack

- All resource will be online and not impact while transfering

```
AzurePortal-->subscription-->tranfer billing ownership-->change-->Recipient Email address-->azure AD Tenant-->Send Transfer Request-->Go to Mail-->Accept Transfer request
```

### set Azure VM password from KeyVault secret by ARM

- Select Key Vault

- Select Access policies

- Enable Access to : 
  
  - Azure Resource Manager for template deployment

- update `parameters.json` with below details
  
  ```
  adminPassword{
      reference{
          "keyvault" : {
                  "id" : "KeyVaultID"
          },
          "secretName" : "KeyVaultSecret"
      }
  }
  ```

### Windows Patch Management with azure automation account

### azure AD custom domain Integrations

```
AzurePortal-->custom Domain-->Add custom domain details-->then COPY TXT or MX record-->Update it on DNS providor Setting
```

### Customize azure Branding Page for Companies for Login in Screen

```
AzurePortal-->AzureAD-->Company branding-->configure-->Language-->Custom details regarding Images Size,File Size etc.-->select upload file-->Yes-->Save
```

### Memory optimized VMs are designed to have a high memory-to-CPU ratio. Great for relational database servers, medium to large caches, and in-memory analytics.

### Azure SQL Managed Instance is the only PaaS service that supports instance-scoped features like CLR and Service Broker.

### Azure Data Lake can ingest real-time data directly from multiple sources and quickly identify insights into the data.