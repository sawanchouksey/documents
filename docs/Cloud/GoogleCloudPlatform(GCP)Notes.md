# Google Cloud Platform (GCP) Notes

<img src="https://sawanchouksey.github.io/documents/blob/main/docs/Cloud/GCP.jpg?raw=true" title="" alt="alt text" data-align="center">

**Google Cloud Platform (GCP)** is a suite of cloud computing services offered by Google that provides a variety of infrastructure and platform services for building, deploying and scaling applications and services.

Some of the key services and products offered by Google Cloud Platform include:

1. **Compute Services**: Google Compute Engine (Virtual Machines), Google Kubernetes Engine (Managed Kubernetes), Google App Engine (PaaS), Google Cloud Functions (Serverless execution).

2. **Storage Services**: Google Cloud Storage, Cloud Bigtable, Cloud Datastore, Persistent Disk.

3. **Networking Services**: Virtual Private Cloud (VPC), Cloud Load Balancing, Cloud CDN, Cloud Interconnect.

4. **Big Data and Machine Learning**: BigQuery, Cloud Dataflow, Cloud Dataproc, Cloud Dataprep, Cloud ML Engine, Vertex AI.

5. **Management Tools**: Google Cloud Console, Cloud Deployment Manager, Cloud Monitoring, Cloud Logging.

6. **Security and Identity**: Cloud Identity and Access Management (IAM), Cloud Key Management Service, Cloud Security Scanner.

7. **Databases**: Cloud SQL, Cloud Spanner, Cloud Bigtable, Cloud Datastore.

8. **Internet of Things (IoT)**: Cloud IoT Core.

9. **API Management**: Cloud Endpoints, Apigee.

10. **Developer Tools**: Cloud Source Repositories, Cloud Build, Cloud Tasks, Cloud Scheduler.

Google Cloud Platform provides a global infrastructure with data centers around the world, enabling customers to deploy their applications and services closer to their users. It also offers a range of pricing models, including pay-as-you-go, sustained use discounts, and committed use discounts, allowing customers to optimize their costs based on their usage patterns.

### GCP free account with 300 credit with 90 days

https://console.cloud.google.com/

### Regions and Zones

- **Availablity Region(DR)** : East US x West US (For disaster Recovery or Region geographical Failure)
- **Availablity Zone(99.99% SLA)** : Zone 1 x Zone 2 x Zone 3 (For Data centre Recovery or Data Centre Zone failure)
- **Availablity Set(99.95% SLA)** : Fault Domain x 3 and Update Domain x 20( for upgrade or maintenance phyiscal Hardware)
- **Single VM (99.9% SLA)** : Configuration of Machine in Single centre only

### Some Major Type of services which offers by GCP are below

- **Compute Service**
  
  - GCP provides a scalable range of Computing
    resources. It’s highly customizable virtual machine and option to deploy
    your code directly or via container.
    
    - Google Compute Engine
    
    - Google App Engine
    
    - Google Kubernetes Engine
    
    - Google Cloud Container Registry
    
    - Google Cloud Functions

- **Networking**
  
  - It includes services related to Networking. It include
    following
    
    - Virtual Private Cloud Network (VPC)
    
    - Cloud Load Balancing
    
    - Content Delivery Network
    
    - Google Cloud Interconnect
    
    - Google Cloud DNS Service

- **Storage & DataBase**
  
  - It includes services related to Storage and DB. It
    include following
    
    - Google Cloud Storage
    
    - Cloud SQL DB
    
    - Cloud BigTable
    
    - Cloud Data Store
    
    - Cloud Persistent Disk

- **Big Data Processing and Management**
  
  - It includes services related to Big Data. It include following
    
    - Google Cloud BigQuery
    
    - Cloud DataProc
    
    - Cloud DataLab
    
    - Cloud Pub/Sub

- **Machine Learning**
  
  - It includes services related to Machine Learning and Artificial
    Intelligence. It include following
    
    - Google Cloud Machine Learning
    
    - Vision APIs
    
    - Natural Language APIs
    
    - Translation APIs
    
    - Speech APIs

- **Identity and Access Management**
  
  - It includes services related to access management
    and security. It include following
    
    - Google Cloud Resource Manager
    
    - Cloud IAM
    
    - Cloud Security Scanner
    
    - Cloud Platform Security

- **Management and Development Tools**
  
  - It includes services related to cloud management
    and monitoring. It include following
    
    - StackDriver
    
    - Monitoring
    
    - Logging
    
    - Error Reporting
    
    - Trace

- **Developer’s tools**
  
  - It includes services related to cloud development. It
    include following
    
    - Cloud SDK
    
    - Deployment Manager
    
    - Cloud Source Repository
    
    - Cloud Test Lab

### GCP Pricing

- Google Cloud Platform first public Cloud Service, which provides per
  second Billing.

- Customer Friendly Pricing
  
  - No Upfront Costs
  
  - Pay as you Go
  
  - No Termination Fee
  
  - Sustained Use Discount

- **GCP Pricing calculator**
  
  https://cloud.google.com/products/calculator 

### Ways to Interact with Google Cloud

- **GCP Web Console - Web User Interface**
  
  - It is powerful tool but used for administrative tasks.
  
  - Allows view of all Projects and Resources.
  
  - Enable-Disable Resource REST API.
  
  - Offers access to Cloud Shell.

- **GCP Cloud Shell - Terminal base Interface**
  
  - It is a way powerful as compare to Web - Interface.
  
  - Allows user to access and command cloud environment via terminal.
  
  - Include pre-install SDK and other Utilities.
  
  - Google Cloud Shell is an Interactive terminal to Interact with Google Cloud.
  
  - Cloud Shell is Browser Based Terminal.
  
  - Cloud SDK, gcloud CLI and other Utilities are pre-installed in Google Cloud Shell.
  
  - Cloud Shell comes with Inbuilt Code Editor. You can use this editor to Open Directories, Files and Edit them.
  
  - Google Cloud Shell is fully Browser Based Application, No local Installation is required to use Google Cloud shell.
  
  - Cloud Shell have 5GB Persistent Disk Attached.
  
  - Easy Access to pre-install tools.
    
    - gcloud, bq, vim, gsutil, python, ruby, docker, npm, bash etc.

- **REST APIs - Rest APIs are programmatic access to cloud resources**
  
  - Most powerful way to interact with google cloud.
  
  - Use JSON as interchange format.
  
  - Use Oauth 2.0 for authentication.
  
  - Mostly APIs include daily quota and rate limits, that can be raised by request.
  
  - Many APIs are “Disabled” by default.

- **GCP Console Mobile App - For IOS and Android.**
  
  - You can monitor and make changes to Google Cloud resources from your mobile device. This includes managing projects, billing, App Engine apps, and Compute Engine VMs.
  
  - The app allows you to receive and respond to alerts, helping you quickly address production-impacting issues.
  
  - You can open, assign, acknowledge, and resolve incidents to keep your team in sync.
  
  - The app provides a way to triage and understand the crashes of your cloud services.
  
  - You can start, stop, and SSH into instances. You can also see logs from each instance.
  
  - The app provides customizable graphs that give you key metrics such as CPU usage, network usage, requests per second, server errors, and much more at a glance.
  
  - The app provides up-to-date billing information and cost forecasts. You can also get billing alerts for projects going over budget.
  
  - You can see errors, roll back, and change traffic splitting.
  
  - You can view and delete Cloud Storage data (image, logs, files, etc.).
  
  - You can view health, start, and stop Cloud SQL instances.

### Machine Types

- Machines types are templates of virtualized hardware that will be available to the VM instance. 

- These resources include the CPU, Memory, Disk capabilities, and so on.
1. **Standard machine type**
   
   - Ideal for typical balanced instances with respect to RAM and CPU
   
   - Have 3.75GB of RAM per virtual CPU

2. **High-memory machine types**
   
   - Ideal for applications that require more memory
   
   - Have 6.5GB of RAM per virtual CPU

3. **Shared-core machine types**
   
   - These machines have one virtual CPU on a single hyper-thread of a single host CPU that is running the instance. 
   
   - Ideal for non-resource intensive applications.
   
   - Very cost effective

4. **Large machine types**
   
   - Ideal for resource-intensive workloads
   
   - Up to 1TB of memory

5. **Custom machine types**
   
   - This is ideal if you have a workload that maybe requires more processing power or memory than what is offered by the Google-provided types, or if you need GPUs.

6. **Preemptibility machine Types**
   
   - Preemptible VM is an affordable, short-lived instance ideal for batch jobs or fault-tolerant workloads.
   
   - They’re up to 80% cheaper than regular instances, so if your application can handle random the termination of VMs at any
     time, then this is best option.
   
   - Some common applications that use preemptible VMs are modeling or simulations, rendering, media transcending, big data, continuous integration, and web crawling.

### Disks

- The disk you choose will be your single root disk in which your image is loaded during the boot process. Do you choose a persistent disk or a local disk?
1. **Persistent Disks**
   
   - Persistent disks are network-based “disks” abstracted to appear as a block device. 
   
   - Data is durable, meaning the data will remain as you left it after reboots and shutdowns.
   
   - Available as either a standard hard disk drive or as a solid state drive (SSD), persistent disks are located independently of the VM instances, which means they can be detached and reattached to other instances.
     
     - **Standard persistent disks**
       
       - Ideal for efficient and reliable block storage
       
       - Max 64TB per instance
       
       - Only available within a single zone
     
     - **SSD persistent disks**
       
       - Ideal for fast and reliable block storage
       
       - Max 64TB per instance
       
       - Only available within a single zone

### Create Custom Machine/VM/Compute Engine in GCP

```
GCP-DashBoards-Cosole-->Select Project-->Go to Hamburger Navigation menu-->compute section-->select compute Engine-->select VM instances-->create-->Name:Instance/VM name-->add labels-->Regions:Select Region & Zones:Select Zone-->Machine Configuration-->Machine Family:Genral Purpose/Memory Optimized/Compute Optimized | Series : N1,N2,E2,N2D(Genration of CPU) | Machine Type:Custom-->Cores:select vcpu | Memory:select GB-->Boot Disk-->Operating System:Select OS for VM | Version : Select Image Type or Version of OS | Boot Disk Type: Standard Persistant Disk | Size(GB):10-->select-->Identity and API access-->Service account:Select service Account | Access Scope:Seelct Access Scope-->Firewall-->checkBox:Allow HTTP,HTTPS traffics-->Mangement-->Management | Security | Disks | Networking | SoleTenancy-->Create
```

### Create Google Compute Engine/Virtual Machine

```
GCP-DashBoards-Cosole-->Select Project-->Go to Hamburger Navigation menu-->compute section-->select compute Engine-->select VM instances-->create-->Name:Instance/VM name-->add labels-->Regions:Select Region & Zones:Select Zone-->Machine Configuration-->Machine Family:Genral Purpose/Memory Optimized/Compute Optimized | Series : N1,N2,E2,N2D(Genration of CPU) | Machine Type:Custom,Micro,Small,Standard-->Boot Disk-->Operating System:Select OS for VM | Version : Select Image Type or Version of OS | Boot Disk Type: Standard Persistant Disk | Size(GB):10-->select-->Identity and API access-->Service account:Select service Account | Access Scope:Seelct Access Scope-->Firewall-->checkBox:Allow HTTP,HTTPS traffics-->Mangement-->Management | Security | Disks | Networking | SoleTenancy-->Create
```

### GKE (Google Kubernates Engine)

- Kubernetes is an open source solution for managing application containers.

- It is a cluster manager and orchestration system for running Docker containers in the cloud.

- GKE a production-ready environment with guaranteed uptime, load balancing and included container networking features. 

- It allows you to create multiple-node clusters while also providing access to all Kubernetes’ features.
  
  ```
  GCP-DashBoards-Cosole-->Select Project-->Go to Hamburger Navigation menu-->compute section-->select Kubernates Engine-->clusters-->create cluster-->Name:ClusterName-->Location Type:Zonal,Regional-->Zone:Select Zone|Region:Select region-->Specify node Location:Specify Master Node Location-->Master Version:Static-->Static Version:Select Version of GKE-->Create
  ```

### Standard App Engine

- Google App Engine is a Platform as a Service (PaaS) product that provides Web app developers and enterprises with access to Google's scalable hosting.

- App Engine makes deployment, maintenance, Scalability easy so that you can focus on Innovation.

- Especially suitable for building scalable web Applications & Mobile backends.

- Google App Engine is free up to a certain amount of resource usage.

- App Engine standard environment is based on container instances running on Google's infrastructure.
  -App Engine standard environment makes it easy to build and deploy an application that runs reliably even under heavy load
  and with large amounts of data.

- Free Daily Quota.

- Usage based Billing.

- Applications run in a secure, sandboxed environment.

- Application runs within its own secure, reliable environment that is independent of the hardware, operating system, or
  physical location of the server.

- Standard environment supports the following languages: Java, Python, Node.js, PHP, Ruby, Go.

- App Engine standard environment gives you 1 GB of data storage and traffic for free, which can be increased by enabling
  paid applications.

- App Engine Standard Environment Runtimes - App Engine standard environment has two generations of runtime environments.
  
  1. **1st Generation**
     
     - Supported languages: Python 2.7, Java 8, PHP 5.5, Go 1.11
     
     - External network access: Python 2.7 and PHP 5.5 have access via the URL Fetch API, while Java 8 and Go 1.11 have full access.
     
     - File system access: Python 2.7 and PHP 5.5 have no file system access, while Java 8 and Go 1.11 have read/write access to the /tmp directory.
  
  2. **2nd Generation**
     
     - Supported languages: Python 3.7, Java 11, Node.js, PHP 7.2, Ruby, and Go 1.2+
     
     - External network access: Full access
     
     - File system access: Read/write access to the /tmp directory
  
  It's important to note that the 1st generation of the App Engine Standard Environment is being gradually deprecated, and new applications are recommended to use the 2nd generation for better performance, security, and access to the latest language versions and features.

### Flexible App Engine

- Flexible App Engine overcome the constraints of Standard App Engine. 

- App Engine allows developers to focus on what they do best: writing code. Based on Google Compute Engine, the App Engine flexible environment automatically scales your app up and down while also balancing the load. 

- In flex App Engine, You can customize runtimes or provide your own runtime by supplying a custom Docker image or
  Dockerfile from the open source community.

- Features
  
  - **Customizable infrastructure**
    
    - App Engine flexible environment instances are Compute Engine virtual machines, which means that you can take advantage of custom libraries, use SSH for debugging, and deploy your own Docker containers.
  
  - **Performance options**
    
    - You can specify how much CPU and memory each instance of your application needs, and the flexible environment will provision the necessary infrastructure for you.
  
  - **Native feature support**
    
    - Features such as microservices, authorization, SQL and NoSQL databases, traffic splitting, logging, versioning, security scanning, and content delivery networks are natively supported.

### Managed virtual machines

- App Engine manages your virtual machines, ensuring that:
- Instances are health-checked, healed as necessary, and co-located with other services within the project.
- Critical, backwards compatible updates are automatically applied to the underlying operating system.
- VM instances are automatically located by geographical region according to the settings in your project. Google's management services ensure that all of a project's VM instances are co-located for optimal performance.
- VM instances are restarted on a weekly basis. During restarts Google's management services will apply any necessary operating system and security updates.
- You always have root access to Compute Engine VM instances. SSH access to VM instances in the flexible environment is disabled by default. If you choose, you can enable root access to your app's VM instances.
- All Compute Engine needs Disk to read/write data or to operate.

### Persistent Disk

- Persistent Disk - Single root disk attached to VM.

- Network Attached Disk. Array of multiple Disks.

- Redundancy, Reliability, Performance

- Benefit of RAID (Redundant Array of Independent Disks)
  
  - **RAID 0 (Striping)** - Stream of data is divided into multiple segments or blocks and each of those blocks is stored on
    different disks.
  
  - **RAID 1 (Mirroring)** - Data is mirrored or cloned to an identical set of disks so that if one of the disks fails, the
    other one can be used.

- Very flexible and Powerful.

- Independent from VM not physically attached.

- Can be Detach/Move.

- Can be read multiple instance at Once.

- Preserve Data even after deleting Instance.

- Resize, Move, Attach additional Disk- even when in-use.

- Performance scale with Size.

- SSD Options are available.

- Encryption - Google Encryption or Custom Encryption.

- Common and Default Option

- Not Directly attached to Compute Engine, but Network Attached Disk

- Standard and SSD options available

### Local SSD

- Directly attached to Compute Engine VM.

- Highest Performance Disk

- Physically attached to VM

- Can’t be boot disk

- Must create on Instance Creation

- Fix in Size and attach upto 8 Disk

- All Data lost in case Instance Terminate

- Only Support Google Supplied Encryption.

- Can attach Local SSD and Persistent Disk to same Instance

### Create Disk

```
GCP-DashBoards-Cosole-->Select Project-->Go to Hamburger Navigation menu-->compute section-->Storage-->Disk-->create disk-->Name:Disk Name-->Select Zone|region(Remember VM instnace and disk must be in same zone for attchment)-->Disk Source type:Blank Disk-->Disk Type:Balanced persistent disk-->Size:100GB-->encryption-->Google Managed Encryption-->Create
```

### Snapshots in GCP

- Reducing activity while backup disk.

- Prepare disk for better consistency.
  
  - Pause application that write the data
  
  - If possible, unmount the disk completely
  
  - For windows, use VSS snapshot
  
  - For Linux, use ext4 snapshot

- Take only one snapshot per disk.

- Scheduling during off hours.

- Run fstrim before snapshot to cleanup space.

- This are Disk BackUps.

- **SnapShot Disk**
  
  ```
  GCP-DashBoards-Cosole-->Select Project-->Go to Hamburger Navigation menu-->compute section-->Storage-->Disk-->create SnapShot-->
  Name:SnapShot-1-->Source Disk:Select Disk-->Location:Multiregional|regional-->Select Location:Location-->Create
  ```

- Snapshot is useful for periodic BackUps.

- Can be created on Running Instance Disk.

- Share across the Projects.

- You can create Instance Copy in another Zone as well.

- You can create SnapShot of Boot disk or Secondary Disk.

### Cloud Storage Bucket - Infinite Space

- No Block Storage allowed
- Can't be a Boot Disk
- Most Flexible, Durable, Scalable Disk Options
- Lower Performance then Other Disk Options
- Global accessibility
  - Instance multiple region/zone can use the same bucket.

### Access storage class for bucket

1. **Standard** - best for short term storage and frequently access data

2. **Nearline** - best for backup and data access less than once a month

3. **Coldline** - Best for disaster recovery and data access less than once a quarter

4. **Archive** - Best for long term preservation of data access less than once a year
- make bucket `publically access`
  
  ```
  gcp-->navigation menu-->storage-->bucket-->select bucket-->select file-->edit metadata-->[Entity : User | Name : allUsers | Access : Reader | Save ]
  ```

- Google Cloud Storage is a RESTful online file storage web service for storing and accessing data on Google Cloud Platform infrastructure.
  
  - It is an Infrastructure as a Service (IaaS), comparable to Amazon S3 online storage service.
  
  - Cloud Storage is unified object storage service.
  
  - Cloud Storage is a persistent storage, it is durable, replicated and also made globally available via HTTP URL.
  
  - Cloud Storage is auto scalable service.
  
  - Cloud Storage is not a File System, because each item in cloud storage have unique URL.

### GCP Buckets

Basic containers that hold your data. Everything that you store in Google Cloud Storage must be contained in a bucket. You can use buckets to organize your data and control access to your data, but unlike directories and folders, you
cannot nest buckets.

- **Bucket names**
  
  - Should be unique as the name of the buckets stored in single Cloud Storage namespace. 
  
  - Also, bucket names can be used with a CNAME redirect, which means they need to conform to DNS naming conventions.

- **Bucket labels**
  
  - Bucket labels are key:value metadata pairs that allow you to group your buckets along with other Google Cloud.

- **Objects**
  
  - Objects are the individual pieces of data that you store in Google Cloud Storage.

- **Objects have two components**
  
  - object data and object metadata.
    
    - The object data component is usually a file that you want to store in Google Cloud Storage
    
    - The object metadata component is a collection of name-value pairs that describe various object qualities

- There is no limit on the number of objects that you can create in a bucket.

- Cloud Storage objects are immutable.

- Cloud Storage allow to version the stored objects.

- Object Versioning needs to be enable explicitly, in absence of Object Versioning, new objects terminates the old.

- Cloud Storage offers life cycle management policy for the objets in bucket.

- **Create Bucket**
  
  ```
  GCP-DashBoards-Cosole-->Select Project-->Go to Hamburger Navigation menu-->storage-->browse-->create bucket-->bucket name(globally unique)-->location type-->default storage class-->retention policy-->Labels-->create
  ```

- **Make file publically accessable over the internet**
  
  ```
  GCP-DashBoards-Cosole-->Select Project-->Go to Hamburger Navigation menu-->storage-->browse-->select bucket-->select file-->edit metadata-->Entity:User,Name:allUsers,Access:Reader-->save
  ```

### GCP Bucket `gsutil` commands

- Create Bucket
  
  ```
  gsutil mb gs://<bucket-name>
  gsutil mb gs://my-first-bucket-001
  ```

- upload file using cmd
  
  ```
  gsutil cp filename.jpg <bucket uri>
  gsutil cp filename.jpg gs://my-first-bucket-001
  ```

- make file public
  
  ```
  gsutil acl ch -u <userdetails>:<permission> <bucket_Uri>/<filename>
  gsutil acl ch -u AllUsers:R gs://my-first-bucket-001/filename.jpg
  ```

- copy data from one bucket to another
  
  ```
  gsutil cp gs://<source-bucket-name>/<filename> gs://<destination-bucket-name>
  gsutil cp gs://my-first-bucket-src/sawan.jpg gs://my-first-bucket-dest
  ```

- List the content of the Bucket
  
  ```
  gsutil ls <bucket uri>
  gsutil ls gs://my-first-bucket-001
  ```

- Enable the versioning in bucket
  
  - **Remarks**
    
    - we cant enable the versoning in bucket if retention policy is exist
    
    - we cant enable lifecycle and versioning from console or portal
  
  ```
  gsutil versioning set on gs://my-first-bucket-001
  ```

- get the last version of file in bucket
  
  ```
  gsutil lifecycle set lifecycle-filename.json gs://my-first-bucket-001
  ```

- update the lifecycle for the bucket by json file
  
  ```
  gsutil lifecycle set lifecycle-filename.json gs://my-first-bucket-001
  ```

- get the lifecycle for the bucket
  
  ```
  gsutil lifecycle get gs://my-first-bucket-001
  ```

### Create `Cloud Spanner`

```
gcp-->navigation menu-->Storage-->Spanner-->[+] create Instance-->[ Instance Name | InstanceId | Regional/Multi-Region | Configuration | Allocate Nodes | Create ]
```

### ### Execute Cloud SQL DB

1. Connect with CLOUD SQL DB
   
   ```
   gcloud sql connect <INSTANCE_NAME> --user=root
   ```

2. Create Database.
   
   ```
   create database [databasename];
   ```

3. Use Specific DataBase.
   
   ```
   use [db name];
   ```

4. List all databases on the sql server.
   
   ```
   show databases;
   ```

5. To see all the tables in the db.
   
   ```
   show tables;
   ```

6. To see table's field formats.
   
   ```
   describe [table name];
   ```

7. To delete a db.
   
   ```
   drop database [database name];
   ```

8. To delete a table.
   
   ```
   drop table [table name];
   ```

9. Show all data from a table.
   
   ```
   SELECT * FROM [table name];
   ```

10. To return columns and column information.
    
    ```
    show columns from [table name];
    ```

11. Create the table "products".
    
    ```
    CREATE TABLE products (
    productIDINT UNSIGNEDNOT NULL AUTO_INCREMENT,
    productCodeCHAR(3) NOT NULL DEFAULT '',
    name VARCHAR(30) NOT NULL DEFAULT '',
    quantity INT UNSIGNEDNOT NULL DEFAULT 0,
    priceDECIMAL(7,2)NOT NULL DEFAULT 99999.99,
    PRIMARY KEY(productID)
    );
    ```

12. Show all the tables to confirm that the "products" table has been created
    
    ```
    SHOW TABLES;
    ```

13. Describe the fields (columns) of the "products" table
    
    ```
    DESCRIBE products;
    ```

14. Show the complete CREATE TABLE statement used by MySQL to create this table
    
    ```
    SHOW CREATE TABLE products \G
    ```

15. Insert a row with all the column values
    
    ```
    INSERT INTO products VALUES (1001, 'PEN', 'Pen Red', 5000, 1.23);
    INSERT INTO products VALUES
    (NULL, 'PEN', 'Pen Blue',8000, 1.25),
    (NULL, 'PEN', 'Pen Black', 2000, 1.25);
    INSERT INTO products (productCode, name, quantity, price) VALUES
    ('PEC', 'Pencil 2B', 10000, 0.48),
    ('PEC', 'Pencil 2H', 8000, 0.49);
    INSERT INTO products (productCode, name) VALUES ('PEC', 'Pencil HB');
    SELECT * FROM products;
    ```

16. Sample MySQL DataSet from github.
    
    ```
    https://github.com/datacharmer/test_db.git
    ```

17. Run SQL file on your MySQL Instace.
    
    ```
    gcloud sql connect <INSTANCE_NAME> --user= root < <SQL_FILE_NAME>
    ```

### ### SetUp Cloud Storage CLI (gsutil) in VM

1. Create Instance

2. Create a Service Account
- Assign Role Product Editor
3. Get the Private key of Service Account

4. Create a Cloud Storage Bucket

5. SSH the VM Instance

6. Copy the Service Account Private key

7. Use Service Account to Interact with Project using CLI
   
   ```
   gcloud auth activate-service-account --key-file <JSON_FILE>
   ```

8. Reset Local profile on Instance and Initialize API
   
   ```
   gcloud init
   ```

9. Copy Few Files to Bucket

10. Get ACL of file or Bucket
    
    ```
    gsutil acl get <BUCKET_NAME/FILE_NAME> > <FILE_TO_SAVE>
    ```

11. Set File as Private
    
    ```
    gsutil acl set private <BUCKET_NAME/FILE_NAME>
    ```

12. Make File accessible to everyone
    
    ```
    gsutil acd ch -u AllUsers:R <BUCKET_NAME/FILE_NAME>
    ```

### What kind of Storage suppose to use for What use Case

| Block Storage for GCP VMs | Persistent Disk             |
| ------------------------- | --------------------------- |
| **Immutable Blobs**       | **Cloud Storage**           |
| **RDBMS**                 | **CloudSQL & CloudSpanner** |
| **NoSQL Database**        | **Datastore**               |
| **NoSQL Key-Value DB**    | **BigTable**                |
| **Import Data in Cloud**  | **Transfer Service**        |

### Install Helm on Linux Machines

```
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get-helm-3 > get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh
```

### Any Resource in GCP either be Regional, Zonal or Global.

### GCP is organized into Regions and zones.

### In a single region there will be 1,2,3 and 4 zones.

```
us-central1 [Region] 
   |__us-central1-a____
   |__us-central1-b    |
   |__us-central1-c    |-Zones
   |__us-central1-f____|
```

### RPO (Recovery Points Objective)

- Data loss due to accident and recovering 
- Maximum time for which system can be down

### RTO (Recovery Time Objective)

- Downtime due to System recovering
- Maximum time for which organization can tolerate Dataloss

### sustain user discount

- Automatic Discount upto 30% on workloads that run for a significant portion of billing month. i.e.
- As long as the resource will sustain google will provide more discount on resource billing.
- If you terminate machine in 10 days - 5% discount given by Google on Billing Amount
- If you terminate machine in 20 days - 10% discount given by Google on Billing Amount
- If you terminate machine in 30 days - 30% discount given by Google on Billing Amount
- **Preemptible VM** - Upto 80% off on Workload. But workload can be interrupted.
- **ColdLine Storage** - Archival Storage at very Cheap rate.
- **Custom Machines** - Pick any Configuration of CPU & Memory and Save Up to 48% on Compute Engine resources.
- **Committed Use Discount** - Save up to 57% on Lock-In resources.

### The service account must be created before you create a firewall rule that relies on it.

### Firewall rules that use service accounts to identify instances apply to both new instances created and associated with the service account and existing instances if you change their service accounts.

### User can associate service accounts with individual instances and with instance templates used by managed instance groups.

### GCP default vpc have subnet like this

- Each subnet for each 1 region
  
  ```
  Total no. of subnets = Regions available in GCP
  ```

### Managing cloud infrastructure from k8s

- we can do it by using crossplane
  
  https://docs.crossplane.io/v1.14/getting-started/
  
  https://docs.crossplane.io/v1.14/getting-started/provider-gcp/
  
  https://doc.crds.dev/github.com/crossplane/provider-gcp@v0.22.0
  
  https://github.com/crossplane-contrib/provider-gcp/tree/master/examples

### Migration to Google Cloud

1. What does google cloud do, that we can't do right Now?

2. Why should we migrate our resources to GCP?

3. What is ROI if we move to Google cloud?

4. Things care about migration as leader/Architect?
   
   - Costs
   
   - Future-proof infrastructure
   
   - Scale to meet demands
   
   - Data Analytics
   
   - Greater Businness agility
   
   - Managed Services
   
   - Global Reach
   
   - Secuirty at scale

### Five Phases of Cloud Migration

```
[1]Assess ==>
   [2]Pilot ===>
      [3]Move Data ====>
         [4]Move App =====>
            [5]Optimize
```

### Principles of Good Cloud Design

- High Availablity
- Scalablity
- Security
- Disaster Recovery
- Cost Control

## Migration Services end to end migrate

| *Services Types* | *Own Data Center*                  | *GCP(Google Cloud Platform)*               |
| ---------------- | ---------------------------------- | ------------------------------------------ |
| Compute          | Physical\|Virtualize Hardware      | **Compute Engine**                         |
| Storage          | SAN, NAS, DAS                      | **Persistant Disk, Cloud Storage**         |
| Network          | MPLN, VPN, DNS, H/W Load Balancing | **Cloud VPN, Cloud LB, CDN**               |
| Security         | Firewall, Route Table etc.         | **Firewall, Encryption etc**.              |
| Identity         | Active Directory, LDAP             | **IAM, LDAP**                              |
| Management       | Configuration Service, CICD tools  | **GCP Deployment Manager, CI,Cloud Build** |

### Data tranfer by Gsutil

- Multi Threaded Transfer Copy using `gsutil`
  
  ```
  - Use -m Option
  gsutil -m cp -r [SOURCE] gs://[BUCKET_NAME]
  ```

- Parallel Uploads
  
  ```
  - Break Single File into Chunks
  - Don’t use for Nearline/Coldline Buckets - Extra Charge for
  ‘Modifying’ files on upload
  gsutil -o GSUtil:parallel_composite_uplaod_threashold=200M cp
  [SOURCE] gs://[BUCKET_NAME]
  ```

### Removing old replicasets is part of the Deployment object, but it is optional. You can set .spec.revisionHistoryLimit to tell the Deployment how many old replicasets to keep around.Here is a YAML example:

```
apiVersion: apps/v1
kind: Deployment
# ...
spec:
  # ...
  revisionHistoryLimit: 0 # Default to 10 if not specified
  # ...
```

### Execute trigger from cloudbuild.yaml file

```
- name: gcr.io/cloud-builders/gcloud
    args:
      - builds
      - triggers
      - run
      - MY-TRIGGER
      - '--region=asia-south1'
```

### Install gke-auth plugin in private VM

```
sudo apt-get install google-cloud-sdk-gke-gcloud-auth-plugin
```

### Create cloudbuild trigger with the help of shell script

```
#!/bin/bash
ms_name =("test1" "test2" "test3") 
for n in ${ms_name[@]}; 
do
  gcloud builds triggers create cloud-source-repositories --name=tyh-$n-microservice-docker-image-puild-push-uat --repo=tyh-$n-microservice-uat  --branch-pattern=^development$ --build-config=cloudbuild-docker-build-push.yaml --region=asia-south1 --description="This trigger used to build and push docker images in artifact repositories"

  gcloud builds triggers create cloud-source-repositories --name=tyh-$n-microservice-gke-deploy-uat --repo=tyh-$n-microservice-uat  --branch-pattern=^development$ --build-config=cloudbuild-k8s-deploy-uat.yaml --region=asia-south1 --description="This trigger used to deploy microservice in gke k8s engine"
done
```

### gcloud cli login

```
gcloud auth login --no-launch-browser
```

### Resize disk in VM

https://cloud.google.com/compute/docs/disks/resize-persistent-disk

### attach mount non-boot disk in VM

- **WINDOWS** : https://cloud.google.com/compute/docs/disks/format-mount-disk-windows

- **LINUX**   : https://cloud.google.com/compute/docs/disks/format-mount-disk-linux

### Mount disk to the Linux VM

- Create a directory that serves as the mount point for the new disk on the VM. You can use any directory. The following example creates a directory under /mnt/disks/
  
  ```
  sudo mkdir -p /mnt/disks/MOUNT_DIR
  ```

- Use the mount tool to mount the disk to the instance, and enable the discard option:
  
  ```
  sudo mount -o discard,defaults /dev/DEVICE_NAME /mnt/disks/MOUNT_DIR
  ```

- Configure read and write permissions on the disk. For this example, grant write access to the disk for all users
  
  ```
  sudo chmod a+w /mnt/disks/MOUNT_DIR
  ```

- Configure automatic mounting on VM restart, Create a backup of your current /etc/fstab file.
  
  ```
  sudo cp /etc/fstab /etc/fstab.backup
  ```

- Use the blkid command to list the UUID for the disk.
  
  ```
  sudo blkid /dev/DEVICE_NAME
  Output: 
  /dev/DEVICE_NAME: UUID="a9e1c14b-f06a-47eb-adb7-622226fee060" BLOCK_SIZE="4096"
  TYPE="ext4" PARTUUID="593b3b75-108f-bd41-823d-b7e87d2a04d1"
  ```

- Open the /etc/fstab file in a text editor and create an entry that includes the UUID. For example:
  
  ```
  UUID=UUID_VALUE /mnt/disks/MOUNT_DIR ext4 discard,defaults,MOUNT_OPTION 0 2
  ```

- Use the cat command to verify that your /etc/fstab entries are correct:
  
  ```
  cat /etc/fstab
  ```

- If you detach this disk or create a snapshot from the boot disk for this VM, edit the /etc/fstab file and remove the entry for this disk. Even with MOUNT_OPTION set to nofail or nobootwait, keep the /etc/fstab file in sync with the devices that are attached to your VM and remove these entries before you create your boot disk snapshot or detach the disk.

### cloudbuild trigger names list

```
gcloud alpha builds triggers list --region=asia-south1 --format="value(name)"
```

### Give your account permissions to perform all administrative actions needed in k8s

```
kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=<GOOGLE-EMAIL-ACCOUNT>
```

### rollout deployment in GKE

```
kubectl rollout undo deployment/tyh-test-uat --to-revision=<revision No>
kubectl set image deployment/tyh-test-uat tyh-test-uat=asia-south1-docker.pkg.dev/tyh-uat-svc-poc/tyh-poc/test-microservice:2188c4b
```

### insecure-skip-tls-verify in .kube/config file for connecting GKE (*NOT Recommended*)

[ssl - helm: x509: certificate signed by unknown authority - Stack Overflow](https://stackoverflow.com/questions/48119650/helm-x509-certificate-signed-by-unknown-authority)

```
apiVersion: v1
clusters:
- cluster:
    server: https://192.168.0.3
    insecure-skip-tls-verify: true
  name: gke_my_k8s
```

### check tls through nmap for ssl certificates

```
nmap --script ssl-enum-ciphers -p 443 poc-dev.test.com
nmap --script ssl-enum-ciphers -p 80 34.45.667.8
```

### update SSL policy in gcp for compute resources or Load Balancer in GKE ingress

```
- Create an SSL policy with desired settings
gcloud compute ssl-policies create my-ssl-policy \
  --profile=MODERN \
  --min-tls-version=1.2\
  --custom-features=TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SH

- Create front end config yaml for ssl-policy
apiVersion: networking.gke.io/v1beta1
kind: FrontendConfig
metadata:
  name: my-frontend-config
  namespace: poc-dev
spec:
  sslPolicy: my-ssl-policy

- create ingress file with ssl policy gke
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    networking.gke.io/v1beta1.FrontendConfig: "my-frontend-config"
```

### disable tls in gcloud

```
gcloud config set auth/disable_ssl_validation  True
```

### remove file start `--` in linux

```
rm ./--02102023-2005PM.log
```

### you can check here if any service getting issue from gcp side

https://status.cloud.google.com/

### cloudbuild default variable list

[Substituting variable values &nbsp;|&nbsp; Cloud Build Documentation &nbsp;|&nbsp; Google Cloud](https://cloud.google.com/build/docs/configuring-builds/substitute-variable-values)

### nginx annotation ingress

https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/annotations.md

### kubectl logs with tail in GKE

```
kubectl logs --tail=50 <pod_name>
```

### Logs explorere load balancer logs check query

```
resource.type="http_load_balancer"
resource.labels.forwarding_rule_name="k8s2-fs-xvv-test-ingress-route-kx8tb"
resource.labels.url_map_name="k8s2-um-xvv3k-test-uat-ingress-route-6u8tb"
severity>=WARNING
httpRequest.status=502 OR
httpRequest.status=500 OR
httpRequest.status=403
```

### install telnet in alpind linux docker images

```
apk update install
apk add busybox-extras
```

### replace subsitute variable in yaml file in cloudbuild

```
steps:
  - name: 'gcr.io/cloud-builders/gcloud'
    id: commit
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        echo ${_VERSION}
        sed -i "s/latest/${_VERSION}/g" k8/deploymentprod.yaml
        cat k8/deploymentprod.yaml
```

### Spin K8s Self Managed Cluster on GCP

- Set Project in gcloud
  
  ```
  gcloud config set project <myProject>
  ```

- Set the zone property in the compute section
  
  ```
  gcloud config set compute/zone us-east1-b
  ```

- Create the VPC
  
  ```
  gcloud compute networks create k8s-cluster --subnet-mode custom
  ```

- Create the k8s-nodes subnet in the k8s-cluster VPC network
  
  ```
  gcloud compute networks subnets create k8s-nodes \
  --network k8s-cluster \
  --range 10.240.0.0/24
  ```

- Create a firewall rule that allows internal communication across TCP, UDP, ICMP and IP in IP.
  
  ```
  gcloud compute firewall-rules create k8s-cluster-allow-internal \
  --allow tcp,udp,icmp,ipip \
  --network k8s-cluster \
  --source-ranges 10.240.0.0/24
  ```

- Create a firewall rule that allows external SSH, ICMP, and HTTPS
  
  ```
  gcloud compute firewall-rules create k8s-cluster-allow-external \
  --allow tcp:22,tcp:6443,icmp \
  --network k8s-cluster \
  --source-ranges 0.0.0.0/0
  ```

- Create the controller VM (Master Node)
  
  ```
  gcloud compute instances create master-node \
    --async \
    --boot-disk-size 200GB \
    --can-ip-forward \
    --image-family ubuntu-1804-lts \
    --image-project ubuntu-os-cloud \
    --machine-type n1-standard-2 \
    --private-network-ip 10.240.0.11 \
    --scopes compute-rw,storage-ro,service-management,service-control,logging-write,monitoring \
    --subnet k8s-nodes \
    --zone us-east1-b \
    --tags k8s-cluster,master-node,controller
  ```

- Create Two worker VMs
  
  ```
  for i in 0 1; do
  gcloud compute instances create workernode-${i} \
    --async \
    --boot-disk-size 200GB \
    --can-ip-forward \
    --image-family ubuntu-1804-lts \
    --image-project ubuntu-os-cloud \
    --machine-type n1-standard-2 \
    --private-network-ip 10.240.0.2${i} \
    --scopes compute-rw,storage-ro,service-management,service-control,logging-write,monitoring \
    --subnet k8s-nodes \
    --zone us-east1-b \
    --tags k8s-cluster,worker
  done
  ```

- Install Docker on the controller VM and each worker VM.
  
  ```
  sudo apt update
  sudo apt install -y docker.io 
  sudo systemctl enable docker.service
  sudo apt install -y apt-transport-https curl
  ```

- Install kubeadm, kubelet, and kubectl on the controller VM and each worker VM.
  
  ```
  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
  cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
  deb https://apt.kubernetes.io/ kubernetes-xenial main
  EOF
  sudo apt-get update
  sudo apt-get install -y kubelet kubeadm kubectl
  sudo apt-mark hold kubelet kubeadm kubectl
  ```

- Create the controller node of a new cluster. On the controller VM, execute:
  
  ```
  sudo kubeadm init --pod-network-cidr 192.168.0.0/16
  ```

- To set up kubectl for the ubuntu user, run:
  
  ```
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
  ```

- On Worker Nodes Execute the Join Command
  
  ```
  kubeadm join --discovery-token abcdef.1234567890abcdef --discovery-token-ca-cert-hash sha256:1234..cdef 1.2.3.4:6443
  ```

- Verify the Cluster Status
  
  ```
  kubectl get nodes
  ```

- On the controller, install Calico from the manifest:
  
  ```
  curl https://docs.projectcalico.org/manifests/calico.yaml -O kubectl apply -f calico.yaml
  ```

### Add custom header through yaml in Load Balancer for GKE Ingress

https://cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration#1.16-gke.3+

- Create BackendConfig.yaml as mentioned below
  
  ```
  apiVersion: cloud.google.com/v1
  kind: BackendConfig
  metadata:
  name: my-backendconfig
  spec:
  customResponseHeaders:
    headers:
    - "server: hide"
    - "X-Content-Type-Options: nosniff"
    - "X-Frame-Options: DENY"
    - "X-XSS-Protection: 1; mode=block"
    - "Strict-Transport-Security: max-age=31536000; includeSubDomains; preload"
    - "Content-Security-Policy: default-src 'self';script-src 'self';style-src 'self';font-src 'self';img-src 'self' data:;base-uri 'self';form-action 'self';frame-ancestors 'none';block-all-mixed-content;upgrade-insecure-requests;-cache--control no-cache no-store;no-store;object-src 'none';script-src-attr 'none'"
    - "Referrer-Policy: strict-origin-when-cross-origin"
  ```

- apply the BackendConfig yaml in k8s
  
  ```
  kubectl apply -f BackendConfig.yaml
  ```

- Add above Backend annotation to application servivce.yaml
  
  ```
  kind: Service
  apiVersion: v1
  metadata:
  name: tyh-webui-uat
  annotations:
    cloud.google.com/backend-config: '{"ports": {"3000":"my-backendconfig"}}'
  spec:
  type: NodePort
  ports:
  - name: http
    port: 3000
    targetPort: 3000
    protocol: TCP
  selector:
    app: tyh-webui-uat
  ```

- apply the application service.yaml
  
  ```
  kubectl apply -f service.yaml
  ```

- traffic Routing workflow to application in gke
  
  ```
  User request-->
              DNS-->
                 ALB Front End-->
                              GKE Ingress Route-->
                                               GKE Application Backend service-->
                                                                              GKE Application Pod-->Application Running
  ```

- All backend service in GCP ALB created through GKE ingress didn't update or delete until you will not change or delete GKE application service exposed internet through Ingress.

### add request header to gcp alb backend by gcloud command

```
gcloud compute backend-services update <Backend Name> --global --custom-request-header <Headers>

gcloud compute backend-services update k8s-be-30314--8b39b28cb6b1eb84 --global --custom-request-header "X-Frame-Options:DENY" --custom-request-header "X-Content-Type-Options: nosniff" --custom-request-header "server: hide" --custom-request-header "X-XSS-Protection: 1; mode=block" --custom-request-header "Strict-Transport-Security: max-age=31536000; includeSubDomains; preload"
```

### add response header to gcp alb backend by gcloud command

```
gcloud compute backend-services update <Backend Name> --global --custom-response-header <Headers>

gcloud compute backend-services update k8s-be-30314--8b39b28cb6b1eb84 --global --custom-response-header "X-Frame-Options:DENY" --custom-response-header "X-Content-Type-Options: nosniff" --custom-response-header "server: hide" --custom-response-header "X-XSS-Protection: 1; mode=block" --custom-response-header "Strict-Transport-Security: max-age=31536000; includeSubDomains; preload"
```

### remove header form backend gcp alb

```
gcloud compute backend-services update <Backend Name> --global --no-custom-request-headers
gcloud compute backend-services update k8s-be-30314--8b39b28cb6b1eb84 --global --no-custom-request-headers

gcloud compute backend-services update <Backend Name> --global --no-custom-response-header
gcloud compute backend-services update k8s-be-30314--8b39b28cb6b1eb84 --global --no-custom-response-headers
```

### security annotation in nginx lb deployed in GKE

```
nginx.ingress.kubernetes.io/configuration-snippet: |
      more_set_headers "server: hide";
      more_set_headers "X-Content-Type-Options: nosniff";
      more_set_headers "X-Frame-Options: DENY";
      more_set_headers "X-XSS-Protection: 1; mode=block";
      more_set_headers "Strict-Transport-Security: max-age=31536000; includeSubDomains; preload"
```

### logs explorere query for specific time to find logs

- Time must be in Container Pod timezone UTC
  
  ```
  resource.type="k8s_container"
  resource.labels.project_id="tyh-dev-svcprj"
  resource.labels.location="asia-south1"
  resource.labels.cluster_name="tyhpockubernetes"
  resource.labels.namespace_name="default"
  labels.k8s-pod/app="tyh-prescription-dev" severity>=DEFAULT
  timestamp>="2023-09-08T22:00:00Z" AND timestamp<="2023-09-08T23:45:00Z"
  ```

### Variablized default GCP compute engine service account for automation

```
SVC_ACCOUNT="${PROJECT_NUM//\'/}-compute@developer.gserviceaccount.com"
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member serviceAccount:$SVC_ACCOUNT --role roles/storage.objectAdmin
```

### GCP AI & ML Demo Service online

```
https://cloud.google.com/?hl=en
--> Products
-->AI and Machine Learning 
-->Speech-To-Text
```

### Cloud Run

- Deploy containerized application through serverless services just like AWS fargate, Azure container etc.
  
  ```
  gcloud run deploy translate --source . --allow-unauthenticated --platform
  ```

### search google API

```
[GCP Console] --> [API & Services] --> [library,Enabled API's & Services, Credentials]
gcloud services enable artifactregistry.googleapis.com 
```

### deploy application in AppEngine Service by app.yaml file

```
- deploy application
gcloud app deploy

- stream logs 
gcloud app logs tail -s deafult

- To view application in web browser run
gcloud app browse
```

### run docker application in cloud shell and access it using another cloudshell with curl http://localhost:8080/

```
docker run --rm -p 8080:8080 gcr.io/{PROJECT_ID}/hello-app:v1
```

### Submit cloudbuild.yaml by gcloud command

```
gcloud builds submit --config cloudbuild.yaml
```

### Build docker image and push to GCR with the help of gcloud

```
gcloud builds submit --tag gcr.io/{google_cloud_project_id}/hello-world .
```

### mount filestore in VM with server address

```
sudo apt-get -y update && sudo apt-get -y install nfs-common
sudo mkdir -p /mnt/test
sudo mount 10.0.134.23:/filshareName /mnt/test
sudo chmod go+rw /mnt/test
```

### Policy role inherit from top to download

- `Organization-->Folder-->Project-->Resource`
  i.e Sawan has "viewer" role in organinzation. Then it will automatically inherit to all child folder,project,resource.
  
  ```
  {
      "binding": [
      {
          members: [
              "user:raha@example.com"
          ],
          "role": "roles/storage.objectViewer"
        }
      ]
      "etag": "wjehqoi"
      "version": 1
  }
  ```

### gcsfuse command for mount to gcp bucket with gke with alpine linux images i.e. node with GKE application pod

- Create startup.sh
  
  ```
  MOUNT_DIR_PATH="/app/logs"
  BUCKET_NAME="tyh-dev-pharmacy-001"
  BUCKET_DIR_NAME="tyh-poc-logs"
  GCP_CREDENTIALS_JSON_PATH="/app/tyh-dev-1234567890.json"
  mkdir ${MOUNT_DIR_PATH} && /root/go/bin/gcsfuse --key-file=${GCP_CREDENTIALS_JSON_PATH} --only-dir=${BUCKET_DIR_NAME} ${BUCKET_NAME} ${MOUNT_DIR_PATH}
  ```

- Create Dockerfile
  
  ```
  FROM node:16.17-alpine3.15
  
  # add required tools and dependencies
  RUN apk add --no-cache ca-certificates fuse openssl wget curl go git && update-ca-certificates
  WORKDIR /app
  RUN git clone https://github.com/GoogleCloudPlatform/gcsfuse.git
  WORKDIR /app/gcsfuse
  RUN go install .
  RUN ["chmod", "+x", "/root/go/bin/gcsfuse"]
  WORKDIR /app
  COPY ["package.json", "package-lock.json","./"]
  COPY ["tyh-dev-1234567890.json","./"]
  RUN npm add
  COPY . /app
  RUN ["chmod", "+x", "/app/startup.sh"]
  ENTRYPOINT ["/app/startup.sh"]
  ```

- Create k8s-deployment.yaml
  
  ```
  lifecycle:
            preStop:
              exec:
                command:
                - fusermount
                - -u
                - /app/logs
  ```

### `Policy analyzer` in IAM

- It is used to create query from template `who access what resources etc`

### Zero downtime with rolling update in GKE deployed application

```
spec:
  replicas: 1
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
kubectl rollout restart deployment $app_name -n $namespace --message="version upgrade"
```

### Access private rdp VM through IAP tunnel user

- use IAP-Desktop application

- Create Firewall rule
  
  ```
  Name : iap-tcp
  source: rdp-VM-IP
  destination: 3389
  ```

### find and fetch service account key with gcloud command

```
gcloud beta iam service-accounts keys get-public-key KEY_ID \
    --iam-account=SA_NAME@PROJECT_ID.iam.gserviceaccount.com \
    --output-file=FILENAME
```

### add custom compte machine `Worker pool`  for execute build steps as cloudbuild privately which defined in Cloudbuil.yaml .

```
steps:
  - name: 'gcr.io/cloud-builders/kubectl'
    args: ['apply', '-f', 'k8/deploymentprod.yaml']
    id: apply-deployment
    env:
    - 'CLOUDSDK_COMPUTE_ZONE=${_ZONE}'
    - 'CLOUDSDK_CONTAINER_CLUSTER=${_GKE_CLUSTER}'
    waitFor: ['delete-deployment']
substitutions:
    #GCP Specific configuration. Please DON'T change anything
    _PROJECT: tyh-prd-svc-poc
    _ZONE: asia-south1
    _GKE_CLUSTER: tyh-poc-prod-gke    
options:
    substitution_option: 'ALLOW_LOOSE'
    workerPool:
      'projects/tyh-prd-svc-poc/locations/asia-south1/workerPools/gke-private-pool'
```

### GCP storage bucket mount to GKE application pod

https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/cloud-storage-fuse-csi-driver

https://chimbu.medium.com/access-cloud-storage-buckets-as-volumes-in-gke-c2e405adea6c

- To enable the driver on an existing Standard cluster
  
  ```
  gcloud container clusters update tyhpockubernetes --update-addons GcsFuseCsiDriver=ENABLED --region=asia-south1
  ```

- Create service account
  
  ```
  kubectl create serviceaccount k8s-gcs --namespace default
  ```

- Create an IAM service account for your application or use an existing IAM service account instead
  
  ```
  gcloud iam service-accounts create k8s-gcs-bucket --project=tyh-dev-tyolpo
  ```

- You can grant the role to your IAM service account to only access a specific Cloud Storage bucket
  
  ```
  gcloud storage buckets add-iam-policy-binding gs://tyh-dev-response-001 --member "serviceAccount:k8s-gcs-bucket@tyh-dev-tyolpo.iam.gserviceaccount.com" --role "editor"
  ```

- Allow the Kubernetes service account to impersonate the IAM service account by adding an IAM policy binding between the two service accounts
  
  ```
  gcloud iam service-accounts add-iam-policy-binding k8s-gcs-bucket@tyh-dev-tyolpo.iam.gserviceaccount.com --role roles/iam.workloadIdentityUser --member "serviceAccount:tyh-dev-tyolpo.svc.id.goog[default/k8s-gcs]"
  ```

- Annotate the Kubernetes service account with the email address of the IAM service account
  
  ```
  kubectl annotate serviceaccount k8s-gcs --namespace default iam.gke.io/gcp-service-account=k8s-gcs-bucket@tyh-dev-tyolpo.iam.gserviceaccount.com
  ```

- Configure resources for the sidecar container overwrite deafult value
  
  ```
  apiVersion: v1
  kind: Pod
  metadata:
  annotations:
    gke-gcsfuse/volumes: "true"
    gke-gcsfuse/cpu-limit: 500m
    gke-gcsfuse/memory-limit: 100Mi
    gke-gcsfuse/ephemeral-storage-limit: 50Gi
  ```

- Consume the CSI ephemeral storage volume in a Pod
  
  ```
  apiVersion: v1
  kind: Pod
  metadata:
  name: gcs-fuse-csi-example-ephemeral
  namespace: NAMESPACE
  annotations:
    gke-gcsfuse/volumes: "true"
  spec:
  terminationGracePeriodSeconds: 60
  containers:
  - image: busybox
    name: busybox
    volumeMounts:
    - name: gcs-fuse-csi-ephemeral
      mountPath: /app/logs
      readOnly: false
  serviceAccountName: KSA_NAME
  volumes:
  - name: gcs-fuse-csi-ephemeral
    csi:
      driver: gcsfuse.csi.storage.gke.io
      readOnly: true
      volumeAttributes:
        bucketName: tyh-dev-response-001
        mountOptions: "implicit-dirs"
  ```

- Disable the Cloud Storage FUSE CSI driver
  
  ```
  gcloud container clusters update CLUSTER_NAME --update-addons GcsFuseCsiDriver=DISABLED
  ```

### FileStore mount in GKE deployed application pod

https://upendra-kumarage.medium.com/gcp-filestore-as-a-persistent-storage-in-google-kubernetes-engine-clusters-ab4f76b34118

- create File store Server get in gcp to get following information
  
  ```
  gcloud filestore instances create my-filestore \
    --project=YOUR_PROJECT_ID \
    --zone=us-central1-a \
    --tier=BASIC_HDD \
    --file-share=name=volume1,capacity=1024 \
    --network=name=default,reserved-ip-range=10.0.0.1/29 \
    --description="My Cloud Filestore instance"    
  
  FileStoreFileShare Name : volume1
  FileStore Server IP     : 10.0.0.1 
  ```

- create a Kubernetes Persistent Volume nfs-pv.yaml
  
  ```
  apiVersion: v1
  kind: PersistentVolume
  metadata:
  name: filestore-nfs-pv
  spec:
  capacity:
    storage: 20Gi
  accessModes:
  - ReadWriteMany
  nfs:
    path: /volume1
    server: 10.0.0.1
  ```

- create a Kubernetes Persistent Volume Claim nfs-pvc.yaml
  
  ```
  apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
  name: filestore-nfs-pvc
  spec:
  accessModes:
  - ReadWriteMany
  storageClassName: ""
  volumeName: filestore-nfs-pv
  resources:
    requests:
      storage: 20Gi
  ```

- create a Pod and mount the created volume sample-nginx-pod.yaml
  
  ```
  apiVersion: apps/v1
  kind: Deployment
  metadata:
  name: nginx-deployment
  spec:
  selector:
    matchLabels:
       app: nginx
    replicas: 1
    template:
      metadata:
         labels:
           app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        volumeMounts:
        - mountPath: /mnt/shared-files
          name: nfs-pvc
        ports:
        - containerPort: 80
      volumes:
        - name:  nfs-pvc
          persistentVolumeClaim:
            claimName: filestore-nfs-pvc
            readOnly: false    
  ```

### Get pod count or details in GKE

```
kubectl get pod -A -o wide
kubectl get pod -A -o wide | wc -l
```

### generate self signed ssl certitficate for domain online

https://regery.com/en/security/ssl-tools/self-signed-certificate-generator

### gcp cloudshell `web preview`

In google cloud shell used for opening or access cloud shell running any application on browser.

### Scan vulnerablity container scan api in gcp

```
gcloud artifact docker images scan imageurl --remote
gcp portal-->artifact/gcr-->select container registry-->setting-->vulnerablity scanning-->turn on
```

### operation on container registries

```
gcloud artifact docker images [operation] [Resource URL]
- operation name
scan | get-opearation | describe | list | list-vulnerablities | delete
```

### Select base image for the container google varified for 0 vulnerablities

https://console.cloud.google.com/gcr/images/cloud-marketplace/GLOBAL/google

```
docker pull gcr.io/cloud-marketplace/google/nodejs:latest
```

### to secure conatiner secuirty enable `binary authorization`

```
gcp portal-->security-->binary authorization-->edit policy-->save policy
```

### enable binary authorization in GKE

```
gcp portal-->create GKE-->security-->[checkbox] enable binary authorization
```

### error: enospc-no-space-left-on-device-nodejs in docker and cloudbuild service with cloudbuild.yaml

```
docker system prune --all
steps:
    # Step 2: Run Docker system prune --all
    - name: 'gcr.io/cloud-builders/docker'
      args: ['system', 'prune', '--all', '--force']
```

### Google Deployment Manager

- It is infrastructure deployment service that automate the creation and management of google cloud resources.

- It is set of Google Cloud Resources and manage them as a unit Called Deployment.

- It use the Configuration file(YAML) to define the resources and deployment properties.

- User can use Jinja and Python template to parametrize the configuration and allow reuse of comman deployment params such as load balanced, auto scale instance group etc.

- Component of resource Section
  
  - `name` : A user defined string to identify the resource.
  
  - `type` : It is type of the resources being deployed such as compute.v1.instance, compute.v1.disk.
  
  - `properties` : The parameters od this resource types. such as zone: asia-east1-a, boot: true.

- Create deployment
  
  ```
  gcloud deployment-manager deployment create <Deployment_Name> --config <YAML_File>
  ```

- update deployment before execute it on real environment
  
  ```
  gcloud deployment-manager deployment update <Deployment_Name> --config <YAML_File> --preview
  ```

- update deployment
  
  ```
  gcloud deployment-manager deployment update <Deployment_Name>
  ```

- Cancel deployment preview
  
  ```
  gcloud deployment-manager deployment cancel-preview <Deployment_Name>
  ```

- Add label to deployment
  
  ```
  gcloud deployment-manager deployment create <Deployment_Name> --config <YAML_File> --labels devserver=backend, storage=media
  ```

- Describe deployment
  
  ```
  gcloud deployment-manager deployment describe <Deployment_Name>
  ```

- Delete deployment
  
  ```
  gcloud deployment-manager deployment delete <Deployment_Name>
  ```

### Google Deployment Manager Console

- gcp console access
  
  ```
  GCP-->Navigation menu-->APIs & Services-->DashBoards-->[+] ENABLE APIs AND SERVICES--->search "CLoud Deployment Manager V2 API"-->Enable API-->Search "Deployment Manager"-->open it-->cloud shell login
  ```

- create `sampleConfig.yaml` for deployment
  
  ```
  resources:
  - name: my-first-deployment-vm
  type: compute.v1.instance
  properties:
  zone: us-central1-a
  machineType: zones/us-central1-a/machineTypes/n1-standard-1
  disks:
  - deviceName: boot
  type: PERSISTENT
  boot: true
  autoDelete: true
  initializeParams:
  sourceImage: projects/debian-cloud/global/images/family/debian-10
  networkInterfaces:
  - network: global/networks/default
  ```

- Create resource with `jinja` template
  
  - create `resourceName.txt`
    
    ```
    michael-machine-1
    ```
  
  - create `vm-template.jinja`
    
    ```
    imports:
    - path: resourcename.txt
    
    resources:
    - name: {{ imports["resourcename.txt"] }}
    type: compute.v1.instance
    properties:
    zone: us-central1-a
    machineType: zones/us-central1-a/machineTypes/n1-standard-1
    disks:
    - deviceName: boot
    type: PERSISTENT
    boot: true
    autoDelete: true
    initializeParams:
    sourceImage: projects/debian-cloud/global/images/family/debian-10
    networkInterfaces:
    - network: global/networks/default
    ```
  
  - create `deploymentConfig.yaml`
    
    ```
    imports:
    - path: vm-template.jinja
    - path: resourcename.txt
    
    resources:
    - name: my-vm
    type: vm-template.jinja
    ```

### `Labels` in GCP

- It is key-value pair

- Key is unique Identifier and Value can be duplicate/Empty

- It is allowed maximum 64 Labels/resource

- It can be applied across all GCP resource

- It cannot effect the resource Operation

- Use Case:
  
  - Define cost center/Location
  
  - Define Resource Environment/Project
  
  - Define service type/owner
  
  - Define Resource State ready,inuse,readyForDeletion etc.
  
  - Define for monitoring purpose

- Update label on existing resource
  
  ```
  gcloud compute instance update instance-2 --update-labels key1=value1,key2=value2
  ```

- Remove label
  
  ```
  gcloud compute instance update instance-2 --remove-label "labelKey"
  ```

- Create instnace with labels
  
  ```
  gcloud compute instance create instance-2 --labels env=uat,owner=sawan,team=qa,location=europe
  ```

- List existing Labels
  
  ```
  gcloud compute instance describe instance-2 --format "yaml(labels)"
  gcloud compute instance describe instance-2 --format "json(labels)"
  ```

### `resource Quota` in GCP

```
GCP-->project-->Navigation Menu-->IAM & Admin-->Quotas
```

- Capping limit on resources that you create

- It will assigned as project wise

- It prevent unexpected spikes in the resources

- Types:
  
  1. Resource per project
  
  2. API rate limit Request
  
  3. API Resource Quota

### GCDS (Google Cloud Directory Sync)

- It is GCDS agent installed in ACtive Directory server for one way communication to google cloud identity.

### Data Backup

- Cloud Storage On-premises
  
  ```
  gsutil -m cp -r [source directory] gs://[bucket name]
  gsutil -m rsync -r [source directory] gs://[bucket name]
  ```

- Cloud Interconnect
  
  ```
  CP-->Hamburger-->Networking-->Hybrid Connectivity-->Interconnect
  ```

- Transfer Services for Cloud
  
  ```
  GCP-->Hamburger-->Storage-->Data Transfer-->[+] create transfer job-->[Source : Source Type | Destination : Bucket Name | Decription | When to overwrite | When to delete | Scheduling Option | Create ]
  ```

- Transfer Services for on-primesis data
  
  ```
  GCP-->Hamburger-->Storage-->Data Transfer-->[+] create transfer job-->[ Source : Full Path to the source directory | Install Agent & Setup Connection | Destination : Bucket Name | Describe Tranfer Job | When to delete | Scheduling Option | Create ]
  ```

- Transfer appliance 
  
  ```
  CP-->Hamburger-->Storage-->Data Transfer-->[ Contact Email | Amount of data to move | Business Name | Business Domain Name | Current Location of Data | Submit Request ]
  ```

- Persistant Disk backup from Take Snapshot 
  
  ```
  GCP-->Hamburger-->Compute-->Compute Engine-->Storage-->Snapshot-->[+] create snapshot-->[ Name | Description | Source Disk | Location | Encryption Type | Create ]
  ```

- VM Backup from the custom Image
  
  ```
  GCP-->Hamburger-->Compute-->Compute Engine-->Storage-->Image-->[+] create Image-->[ Name | Source | Location | Encryption Type | Create ]
  ```

- DataBase Backup
  
  - If you database is at on-primesis or Other Public Cloud
    
    1. For each Vendor there is method to export data services
    
    2. Upload to GCS
    
    3. Import Data to database instance
    
    ```
    GCP-->Hamburger-->DataBase-->SQL-->[Backup Option Configuration in DB creation] or [Instance select]-->[+] create Backup
    ```

### WEB security Scanner

- It is used for public URL Scanning to identify vulnerablities in Web Application(App Engine, Compute Engine,GKE)
- Scan Type : Cross-site Scripting(XSS)
- Clear Text Password
- Invalid Header
- Mixed Content
- Outdated Library

```
GCP-->Hamburger-->security-->Web Secuirty Scanner-->Create a New Scan-->[Name | Strating URL | Exclude URLS | Authentication | Sign In URL | User Name | Password | Save ]-->Run Scan
```

### Secuirty Command Center

- Centralize place to see security of GCP via DashBoards
- It has number of services to analyze security
- It has a pricing tier i.e. Standard Tier & Premium Tier
- It works always in organization level

```
GCP-->Hamburger-->security-->Secuirty Command Center
```

### Cloud Logging

```
GCP-->Hamburger-->operation-->logging-->Logs Explorer | Logs DashBoards | Log Based Metrics | Logs Router | Logs Storage 
```

### Container Scanning API

- Scanning vulnerablities inside container

- Enable Container scanning API

- It works with
  
  1. Container Registry
  
  2. Artifact Registry
  
  ```
  GCP-->Hamburger-->CICD-->Artifact/Container Registry-->Setting-->Enable/Disable Vulnerablity Sanning 
  ```

### Binary Authorization

- policy : Ensure that trusted images are deployed to GCP

- Enable Binary Authorization

- It works with
  
  1. GKE
  
  2. Cloud Run
  
  ```
  GCP-->Hamburger-->Secuirty-->Binary Authorization-->Configure Policy-->[Default Rule | Custom Exemption Rule |ADD Image Path | Save Policy ]
  ```

### Forseti Security

- It is a collection of community driven , open source tool to help you improve the security of GCP environment.

- Systematically monitor your GCP resources to ensure that access control are set as you intended

- Working Model
  
  1. Inventory
  
  2. Scanner
  
  3. Enforcer
  
  4. Explain
  
  5. Notifications

### Cloud SQL instance - Inside GCP

1. On-demand Backup
2. Schedules Backup

### Cloud IAP - Identity Aware Proxy

- With IAP you can guard access to your application and vm

- It provide single point of control for managing user access to web application and cloud resources

- Protect access to application hosted on Google Cloud . Other Cloud and on-primses

- It works with App Engine API, Compute Engine Instance, HTTPS Load Balancer
  
  ```
  GCP-->Security-->Identity-Aware Proxy-->Configure Consent Screen-->[ User type : Internal/External | Create ]-->[App Name | User support email | App Logo | App Home Page Url | [+] Add Domain | Email Address For Developer’s contact | Save & Continue]-->Security-->IAP section-->Enable IAP ON/OFF-->Add Member-->[New Member | Select Role : Cloud IAP : IAP Secured Web APP User | Save]
  ```

- if IAP not configured you can't connect with VM without External IP through SSH
  
  ```
  gcloud beta compute ssh --zone "us-central1-a" "tunneling" --tunnel-through-iap --project "sawanDemo"
  ```

- manage HTTP and SSH based resources

- Enable IAP
  
  ```
  GCP-->security-->Identity Aware Proxy-->enable API-->SSH and TCP resources-->select instance-->Add principal-->Name principal-->Role:IAP-Secured Tunnel User-->save-->
  ```

### DLP API (Data Loss Prevention API)

- fully managed service designed to help you discover, classify and protect your most sensitive data.

- Apply API on Cloud Storage, Big Query, free from text, Structure and Unstructure data(Image) 

- identify and de identify with Masking and Encryption of senstive data
1. **DLP API - TEMPLATE**
   
   - configuration which defines for Types
     
     1. inspection for jobs
     
     2. De-identification of jobs

2. **DLP API - INFOTYPE**
   
   - What to scan for Built-in 120 InfoType or we can create custom InfoType also
     
     1. Like Credit Card
     
     2. SSN
     
     3. Age

3. **DLP API - LIKELIHOOD**
   
   - There are 6 categories for define it
     
     1. LIKELIHOOD_UNSPECIFIED - Default Value; Same as possible
     
     2. VERY_UNLIKELY- It is very unlikely that the data matches the given InfoType
     
     3. UNLIKELY - It is unlikely that the data matches the given InfoType
     
     4. POSSIBLE - It is possible that the data matches the given InfoType
     
     5. LIKELY - It is Likely that the data matches the given InfoType
     
     6. VERY_LIKELY - It is very likely that the data matches the given InfoType

4. Create Stored InfoType
   
   ```
   GCP-->Security-->Data Loss Prevention-->create-->stored InfoType-->[ Tyep | InfoType ID | InfoType Display Name | Description | Resource Indication | Resource Preview | Regex Patters | Create ]
   ```

5. Create Template
   
   ```
   GCP-->Security-->Data Loss Prevention-->create-->Template-->[ Template type : inspection/De-identify | Template ID | Display Name | Resource Location | Continue ]-->[ Manage InfoType | Select ID | Inspect Ruleset [+] Add Rule | Exclusion Rule-->InfoTypes | LikELIHOOD | Create ]
   ```

6. Create Job for Inspection
   
   ```
   GCP-->Security-->Data Loss Prevention-->create-->Template-->Job or Job trigger-->Inspection-->[ Job Id | Resource Location | Location | location type | url | Percentage of included objects scanned within the buckets | Sampling Method | Limit per-object scan by | Max Byte to scan per file | File Types | Continue]-->[Template Name | InfoTypes | Confidence Threshold | Likelihood | Continue ]-->[Time Span or schedule | Trigger scan repeat | Continue]-->Review | Create ]
   ```

### GCP cloud Security Services

```
GCP Portal-->Hambutger Menu-->Security-->Security Services Available mentioned below
```

- SSC(Security Command Centre) : Help to identify all vulnerablity in Cloud Services
- Identity Aware Proxy : It helps us to protect our application
- Binary Authorization : It helps us to deployed only trusted docker images
- Data Loss Prevention : Check and detect personal Data from PII(Personal Identify Information).
- Key Management : Used to manage key to security encrypt data
- Web Security Scanner : Used to define Vulnerablity or security risk detect in our different Web applications.

### Data Encryption

- Data at rest
  
  - data situated at GCS and DataBases

- Data in motion
  
  - data transfer one network to another network
  
  - within GCP or Outside GCP

- Data in Use
  
  - Data situated in RAM
  
  - Memory Store , Memory data processing

### Cloud KMS(Key Management System)

- Google Managed Key
- Customer Managed key
- Customer supplied key

### Cloud Secret Manager

```
pip3 install google-cloud-secret-manager

from google.cloud import secretmanager
client = secretmanager.SecretManagerServiceClient()
name = f"projects/gcp-pse/secrets/dev-secret/versions/latest"
response = client.access_secret_version(request={"name": name})
payload = response.payload.data.decode("UTF-8")
print("Plaintext: {}".format(payload))
```

```
GCP-->security-->Secret manager-->[+] Create Secret-->[ Name | Secret value | Manually Manage location for this access | Encryption | Rotation Period | Notifications | Create ]
```

### IAM (Identity Access Management)

- IAM centrally manages all authorization.

- Who can do what on which resources.

- *.gserviceaccount.com (create by Google default service account)

### Billing + Cloud IAM

- Billing Account Creator
  
  - Create new Organization Level billing Account

- Billing Account Administratos
  
  - Manage billing account
  
  - configure Billing Export
  
  - Link/Unlink Project
  
  - Manage Billing User Roles

- Billing Account User
  
  - Link Project with billing account

- Billing Account Viewer
  
  - View Billing Information(Finance Team)

### Logging

```
gcp-->selectProject-->navigation Menu-->Operation-->Logging 
```

### Export of log in Gcp

```
GCP-->selectProject-->navigation Menu-->operation-->logging-->Logs Router-->[Y]Create Sink-->[ Sink NAme | Sink Description | Select Sink service | Select the Service | Choose logs to include in sink : Query type of logs filter i.e. resource.type="gce_instance" | Exclusion | create sink ]
```

### Monitoring - Uptime Check

```
gcp-->selectProject-->navigation Menu-->Operation-->Monitoring-->Uptime Check-->[+] Create UPtime Check-->[ title | Target : Protocol | Select ResourceType : URL, K8s LB Service , AppEngine , Instnace , Elastic Load Balancer | Applies to : Single/ Group | Instance | Port | Check Frequency | Response Timeout | Alert & Notifications : Create An alert | Name | Duration | Manage Notifications channel : Select Notifications Channel Email, SMS etc. | Add New | Select Email | Create ]
```

### Generate load on VM

```
sudo yum install -y epel-release
sudo yum install -y stress
sudo stress --cpu 2 --timeout 10m
```

### Genarate alert incident

```
gcp-->navigation menu-->operation-->monitoring-->Alerting-->[+] CREATE POLICY-->[ what do you want to track [add condition : Metrics | Find Resource type and metrics | Add filter | Group By | Aggregator | period | Configuration : condition triggers if | condition | Threshold | for | ADD] | Notifications Channel | Select email | Notify on Incident closure | time | Alert Name | Description | Save ]
```

### VPC Layers Security

- Some Cloud Native Solution
- Subnet
- Firewall Rules
- Ingress/Egress Traffic
- Cloud Armor

### Operation

- Logging , Monitoring , Trace , Profiling

### Cloud Identity (Ways to Interact with GCP ) IDAAS (Identity as a services) It Mangaes users and groups in Google Cloud.

- Google Account
- Service Account
- Google Workspace
- Cloud Identity Domain
- Google Groups

### Setup google cloud identity for Organization domain level

https://workspace.google.com/ 

### Register domain with Google

https://domains.google/

### GCDS(Google Cloud Directory Sync)

- It helps you can synchorize the data in your Google Account with Microsoft AD or LDAP server.

### Resource Hierarchy

```
Organization(Company)
   |________Folder(Teams)
              |______Project(Project for Dev,Test, Production)
                       |________Resources(GKE , App Engine , Bucket etc)
```

### Create Organization Hierarchy with create folder, Project

```
GCP-->Hamburger Menu-->Manage Resources-->Create Folder
```

### To see organinzation Policies

- we need to select any project first.

- We can create policy according to our requirements on hierachal level like project , organization and folder level.

- Use case of Policy
  
  1. Disable Service Account Creation
  
  2. Enforce uniform bucket-level access
  
  3. Skip default network creation
  
  ```
  gcp-->select project-->hamburger menu-->IAM & Admin-->organinzation policies
  ```

### skip default network creation policy in organinzation level

- There will be no VPC network will be created in New project after apply below policy
  
  ```
  gcp-->select project-->hamburger menu-->IAM & Admin-->Organization policies-->search & select-->skip default network creation policy-->click Edit-->[ applies to : Customize | Enforcement : On | save ]
  ```

### IAM (Identity and Access Management)

- WHO can do WHAT on WHICH resources
  
  - **WHO**: Identity Member Email
  
  - **WHAT** : Roles (Collection of Permissions)
  
  - **WHICH**: Resources (Compute AppEngine BigQuery) etc.
  
  ```
  i.e. X(who) can CreateVM(what) in ComputeEngine(which)
  ```

### Roles (Collection of permission)

- **Primitive**: Owner, Editor, Viewer
  
  - Viewer : read only permission for all resources inside the project | Only view all resources in gcp
  
  - Editor : Reader + Modification | Modify all resources and No access to IAM billing
  
  - Owner: Editor + manage user, group , billing | Modify all Resources and Manage IAM & Billing
  
  - Assign Primitive Roles to Users
  
  ```
  gcp-->selectProject-->hamburgerMenu-->IAM&Admin-->IAM-->Member-->[+]ADD-->[ New Member | Select Role : Editor | Save ]
  ```

- **PreDefined**: Roles in single services i.e. Compute admin, Network viewer, Big Query Job user
  
  - GCP defined Role & Maintained by GCP & For each product/services - Different sets of Roles defined
  
  - i.e. Compute Admin, Network Viewer , BigQuery Job User
  
  ```
  gcp-->selectProject-->hamburgerMenu-->IAM&Admin-->IAM-->Member-->Select User-->Edit Permissions-->[ Member | Project | Role : Storage Admin | Save ]
  ```

- **CustomRole**: Customised Role, Can be Created from Pre-defined Role
  
  - Combined/Remove/Add permission from multiple pre-defined roles
  
  ```
  gcp-->selectProject-->hamburgerMenu-->IAM&Admin-->Roles-->Create From Role-->[ Title | Description | ID : CustomStorageObjectAdmin | Role launch Stage : Alpha | Select Permissions | Create ]
  gcp-->selectProject-->hamburgerMenu-->IAM&Admin-->IAM-->Member-->Select User-->Edit Permissions-->[ Member | Project | Role : CustomRoleTitle | Save ]
  ```

### Permissions

- **Structure Of Permissions** : <Services>.<ResourceType>.<Verb>
- **Example of Permissions** : BigTable.tables.get | cloudfunction.function.list | storage.object.delete | compute.disk.create

### Assign Role at Organization & Folder Level

- The child can not override parent level assigned role to user.
  
  ```
  gcp-->selectProject-->Switch to Organization-->IAM-->Permissions-->[+]ADD-->[ New Member | Role | Save ]
  ```

### Service Account

- For non humman like Apps, Services

- It is identity for compute Engines i.e. VM

- SA keys for authentication 

- Max 10 key Per Service Account

- Max 100 Service Account per Project

- Assign role to SA like identity

- Types of Service Account
  
  - Google Managed SA
  
  - BuildIn SA i.e. Compute Engine, App Engine & Default SA 
  
  - User created custom SA

- Create Service Account
  
  ```
  gcp-->selectProject-->hamburgerMenu-->IAM&Admin-->Service Accounts-->[+] Create Service Account-->[ SA Name | SA ID | SA description | Create and Continue | Grant this SA access to Project - Select Role | Continue | Grant User access to this SA - SA user role | SA admin role | Done ]
  ```

- Create Service Account with Virtual Machine
  
  - Select SA during creation of VM.
  
  - To check SA associated with VM by login to VM by SSH from GCP
    
    ```
    gcloud auth list
    ```

### Cloud API Access Scopes

- Allow default access
- Allow full access to all cloud APIs
- Set Access for each API
- Drawback : 
  - Machine Must be Stopped after changing access Scope

### Service Account RSA Private Key

- key is the password for SA 

- Keys can used for Authentication

- Genarate key from cloud console
  
  ```
  gcp-->selectProject-->hamburgerMenu-->IAM&Admin-->Service Account-->Select Service Account-->Keys-->ADD key-->Json-->save to local Machine
  ```

- Activate SA by key by command
  
  ```
  gcloud auth activate-service-account --key-file=rsa private keys.json
  ```

### RFC 1918 : Standard for Private IP addressing

- **Class A** - 10.0.0.0-10.255.255.255 - 10.0.0.0/8

- **Class B** - 172.16.0.0-171.31.255.255 - 172.16.0.0/12

- **Class C** - 192.168.0.0-192.168.255.255 - 10.0.0.0/16

### CIDR Notation- Classless Inter-Domain Routing or supernetting

- **123.52.36.0/24** - 24 bits are fixed-8 bits are available-Total IP address - 2(Power of)8=256
- **123.52.36.0/28** - 28 bits are fixed-4 bits are available-Total IP address - 2(Power of)4=16
- **123.52.36.0/31** - 31 bits are fixed-1 bits are available-Total IP address - 2(Power of)1=2
- **0.0.0.0/32** - 32 bits are fixed-0 bits are available-Total IP address - 2(Power of)0=1
- **0.0.0.0/0** - 0 bits are fixed -32 bits are available -Total IP address - 2(Power of)32=4,294,967,296
- `Each region` have `1 subnet` it must for communication between different regions.

### VPC(virtual Private Cloud) - `Global Entity` but Subnet - `Region based Entity`

### `default VPC` is created by GCP by enabling `Compute Engine API`

- skip `default VPC` creation
  
  ```
  GCP-->IAM & Admin-->Organization Policies-->search(skip default network creation)-->select Policy-->Disable
  ```

### list of vpc

```
gcloud compute network list
```

### list of subnet

```
gcloud compute network subnet list
```

#### protcol used in networking mostly

- **SSH** - Secure Shell - port(22)
- **ICMP** - Internet Control Managed Protocol - Ping
- **Http** - Hypertext Transfer protocol - Port(80)
- **Https** - Hypertext Transfer protocol - Port(443)
- **RDP** - Remote Desktop Protocol(3389)

### Firewall : It is a door for incoming or outgoing traffic to an instance

- default rule : **Allow** all outgoing traffic(egress)
- default rule : **Deny** all incoming traffic(ingress)

### Shared VPC

- Shared VPC allows an organization to connect resources from multiple projects to a common VPC.

- Using shared VPC resources in multiple Project can communicate each other on internal IPs without any extra router, VPN or Tunnel.

- When you use Shared VPC, you designate a project as a host project and attach one or more other service projects to it. The VPC networks in the host project are called Shared VPC networks.

- Host project contains one or more Shared VPC networks. A Shared VPC Admin must first enable a project as a host project. After that, a Shared VPC
  Admin can attach one or more service projects to it.

- Service project is any project that has been attached to a host project by a Shared VPC Admin. It's a common practice to have multiple service projects operated and administered by different departments or teams in your organization.A project cannot be both a host and a service project simultaneously. Thus, a service project cannot be a host project to further service projects.

- A project cannot be both a host and a service project simultaneously. Thus, a service project cannot be a host project to further service projects.

- User can create and use multiple host projects; however, each service project can only be attached to a single host project.

- When a host project is enabled, all of its existing VPC networks become Shared VPC networks, and any new network created in it will automatically be a Shared VPC network as well.

- **Host-Project** 
  
  - this project will be a hosted project where shared VPC will be configured.
  
  - When you create shared VPC in first project you need to enabled that project as HOST project.

- **ServiceA Project**
  
  - This is a Service /Consumer Project.

- **My First Project**
  
  - This is a Service /Consumer Project.

- It is used to oprate or shared subnet from VPC between multiple projects.

- **enable permission :**
  
  - You can put these permissions in a custom role and can be attached to your account.
    
    ```
    compute.organizations.disableXpnHost
    compute.organizations.disableXpnResource
    compute.organizations.enableXpnHost
    compute.organizations.enableXpnResource
    compute.projects.get
    resourcemanager.projects.get
    resourcemanager.projects.getIamPolicy
    resourcemanager.projects.list
    ```
  
  ```
  GCP-->IAM & Admin-->Roles-->compute.organization.enableXpnHost-->copy:compute Shared VPC Admin-->IAM-->chnage the permission to Organization level-->Select User-->edit user-->add role : compute Shared VPC Admin-->save
  
  GCP-->VPC Network-->Shared VPC-->SetUP shared VPC-->Save&Continue-->select Subnet-->continue-->attach the project where you want to use this subnet-->select user role : Compute Network Admins-->Save
  ```

### DNSSEC (Domain Name System Security)

- It is an security extension for DNS security provided by google
  
  ```
  GCP-->Networking-->Network-->Cloud DNS-->Select DNS-->DNSSEC-->ON/OFF
  ```

### Google API Private Access

- Private Access allow different subnetwork to use GCP Services privately
- It will configured on Subnet level make -- Private Google Option -->ON/OFF

### create VM from gcloud cli

```
gcloud compute instances create VM_NAME --image-project IMAGE_PROJECT --image IMAGE_NAME --subnet SUBNET_NAME
```

### create multiple vm instances with same configuration from gcloud cli

```
gcloud compute instances create VM_NAME-1 VM_NAME-2 VM_NAME-3 --image-project IMAGE_PROJECT --image IMAGE_NAME --subnet SUBNET_NAME
```

### install ping command

```
sudo apt-get install iputils-ping
```

### find ipaddress for cloud cli

```
curl https://api.ipify.org
```

### create firewall rule with tags also for communication

- add network tag : learntag //in compute instnace
- select Source & Target with Tags instead of IP address

### we need to allow google.api in access for accessing services to each other communication

- This communication will be public access only through external IP

### private google access

- This communication will be private access by private IP
  
  ```
  GCP-->VPC network-->subnet-->edit-->private google access:on-->save
  ```

### serverless private vpc services

- app engine

- cloud run

- cloud function

### cloud function communication with serverless vpc private access

```
GCP-->vpc network-->serverless vpc access-->connector-->cloud function-->connection-->egress setting-->select VPC connectors-->Route only request to private IPs through the VPC connectors-->next-->code-->deploy
```

### Types of IP

- **Internal Private IP** : Access from Private Network inside GCP
- **External Public IP** : Access from anywhere on internet
- **Ephermal Temporal Dynamic IP** : Once we start resource , new IP will be assigned
- **Static Permanent IP** : Can be assigned from one resource to another resource
- Max NIC can be attached to one instance - **8** 

### install kubectl in VM

```
gcloud components install kubectl
apt-get install kubectl
```

### set access scope in VM

- Access Scopes - Allow full access to all cloud APIs

### Cloud Load Balancer

- A load balancer distributes user traffic across multiple instances of your applications.

- By spreading the load, load balancing reduces the risk that your applications experience performance issues.

- Cloud Load Balancing is a fully distributed

- Software defined managed GCP service.

- It isn't hardware based, so you don't need to manage a physical load balancing infrastructure

- Health check
  
  - route traffic to only healthy instance
  
  - maintain minimum number of instances

- Auto scaling based on traffic

- High availability

- Single anycast IP

### There are different type of load Balancer

- **Global LB** : Use global load balancing when your backends are distributed across multiple regions. You can provide access by using a single anycast IP address.
  - `Global load balancing` requires that you use the `Premium Tier of Network Service Tiers`.
- **Regional LB** : Use regional load balancing when your backends are in one region, and you only require IPv4.
  - For `regional load balancing`, you can use `Standard Tier`.
- **Internal LB** : Distribute traffic to instances inside of Google Cloud.
- **External LB** : Distribute traffic coming from the internet to your Google Cloud Virtual Private Cloud (VPC) network. 
- **SSL Proxy LB**: The SSL Proxy LB terminates the SSL/TLS connection from the client and establishes a new SSL/TLS connection with the backend server.

### cloud Run

- ### Serverless deployment for application with docker images etc like fargate containers.

### Http/Https Load Balancer

```
GCP-->Networking-->Network Services-->Load Balancing-->Create Load Balancer-->Select Load balancing Solution(Https,TCP & UDP)-->Select Https Load Balancer-->Start configuration-->Internet facing or Internal Only : From internet to my vm and serverless services-->Global & Regional : Global Http LB-->continue-->[ Name : LB Name | Backend Configuration-->

{Create Backend Services|Name: Backend Services Name | Backend Type : Select Backend Types|Protocol : https| New Backend | Create serverless network endpoint group|Name: backend Name | Region : select region | Serverless network endpoint group : cloud Run | select service : service name -->create}-->create-->OK-->

{Host & Path Rule | mode : simple host & path rule | backend1* : select backend services created earlier}-->{Frontend Configuration | New Frontend IP and Port : Name | protocol : http | Network service tier : Premium | IP version : IPv4 | IP address : Create Reserve IP address | Port : 80-->done}-->

Review and finalization-->create
```

### Cloud DNS

- DNS Address book for internet
  
  - www.google.com 74.125.29.101

- Highly Scalable , Reliable and Managed Domain Name System (DNS) service on GCP infrastructure

- 100% SLA

- Manage millions of DNS zones and records

- Cloud DNS
  
  - Public Zone
  
  - Private Zone

- get Domain free `https://freenom.com`

- check DNS record `https://dnschecker.org`

### Public CLoud DNS With Load Balancer

```
GCP-->Networking-->network services-->[ Cloud Domain-->Buy Domain-->fill details-->get domain

[ GCP-->Networking-->network services-->Cloud DNS-->create Zone { Zone Type : Public | Zone Name : Name | DNS Name : DNS or domain name | DNSSEC : ON | Cloud Logging : ON-->create}]--> Select DNS Name with Type : NS-->Copy Name Server--> Update it on Name server in Domain Register Website | Copy Public IP address | Add records set in Cloud DNS | DNS Name : domain | Resource Record Type : A | TTL : 5 | TTL Unit : Minute | Routing Policy : select Routing Method | IPv4 Address : paste your public IP Address-->Create } Add records set in Cloud DNS | DNS Name : www.domain.com | Resource Record Type : CNAME | TTL : 5 | TTL Unit : Minute | Routing Policy : select Routing Method | Canonical name : domain name-->Create } ]
```

### update existing public internet facing LB with Https

```
GCP-->Networking-->network services-->Load Balancing-->select Load Balancer-->Frontend IP Configuration-->Add Frontend IP and Port-->Name : https | protocol : HTTPS | IPv4 version : IPv4 | IP Address : Select IP address | Port : 443 | Certificate : Upload Certificate or Create New certificate | name : my-certificate-name | Create Mode : Upload or Create Google Managed Certificate | Domains : Add your all domain-->Create-->Update
```

### Private cloud DNS

- Its doesn't required any public domain because it is internal to the network
  
  ```
  [ GCP-->Networking-->network services-->Cloud DNS-->create Zone { Zone Type : Private | Zone Name : Anything Name | DNS Name : dns-my-sawan.com(any thing) | Network : vpc name}-->Create | Copy Private IP address VPC | Add records set in Private Cloud DNS | DNS Name : vm1.domain.com | Resource Record Type : A | TTL : 5 | TTL Unit : Minute | Routing Policy : select Routing Method | IPv4 Address : paste your private IP Address-->Create } Add records set in Cloud DNS | DNS Name : www.domain.com | Resource Record Type : CNAME | TTL : 5 | TTL Unit : Minute | Routing Policy : select Routing Method | Canonical name : domain name-->Create }]
  ```

### Redirect http to https in LB

- Enable Flag "redirect to Https" in HOSt configuration in LB.

### Cloud CDN : Content Delivery Network

- It works with https load balancer only
- It Helps to deliver network quick to user by cache hit and miss mechanism through nearest CDN centre

### Cloud CDN Enabled in LB

```
GCP-->networking-->Network services-->Load Balancing-->select HTTP Load Balancer-->edit-->Beckend configuration-->backend buckets-->edit-->Enable Cloud CDN flag-->update-->Update
```

### Cloud Armor : It is advanced and more secured firewall services just like VPC firewall

- WAF(Web application firewall) + DDos Attack prevention

- Works layer 3 to layer 7

- ML based Adaptive filtering

- Works with Cloud Load Balancer

- Need to have Org Node 

- Deny All Traffic rule
  
  ```
  GCP-->Networking-->Network Security-->Cloud Armor-->Create Policy [ name : name | policy type : Backend security policy | Default rule action : Deny(error type) ]-->add policy to target [ type 1 : load balancer backend services | backend services target : backend service type ]-->create policy
  ```

- Allow All Traffic rule
  
  ```
  GCP-->Networking-->Network Security-->Cloud Armor-->rules-->add rule[ description : allow all | mode : basic mode | match : 0.0.0.0/0(for all) | action : allow | priority : 1000(less than deny rule)]-->add
  ```

- Allow from cloud shell only not local machines
  
  ```
  GCP-->Networking-->Network Security-->Cloud Armor-->rules-->add rule[ description : Cloud shell | mode : basic mode | match : 32.45.67.9/32(for cloud shell IP) | action : allow | priority : 900(less than deny rule)]-->add
  ```

- Allow from local machine only not cloud shell
  
  ```
  GCP-->Networking-->Network Security-->Cloud Armor-->rules-->add rule[ description : local machine | mode : basic mode | match : 10.46.68.9/32(for local VM IP) | action : deny | priority : 800(less than deny rule)]-->add
  ```

- Crete custom expression : allow or deny based on path expression
  
  ```
  GCP-->Networking-->Network Security-->Cloud Armor-->rules-->add rule[ description : allow good path | mode : advanced mode | match : request.path.contains("goodpath")(for expression in URL) | action : allow | priority : 700(less than deny rule)]-->add 
  ```

### Network Service Tier

- **premium tier** : fast network, take less time to reach google network , use less hop(i.e 11) to reach google network
- **standard tier** : moderate network, take more time to reach google network , use more hop(1.e.18) to reach google network

### Logging VPC flow logs : Enabled Flag in Subnet level i.e [Flow Logs : on]

```
GCP-->Cloud Logging-->search Logging in GCP-->logs explorer-->Query[logname:("projects/gcp-network-349067/compute.googleapis.com%2Fvpc_flows") AND resource.labels.subnetwork_id:(4567890543)]-->Query Run
```

### GCP SQL storage keeps growing

[Google Cloud SQL - Postgresql storage keeps growing - Stack Overflow](https://stackoverflow.com/questions/63013896/google-cloud-sql-postgresql-storage-keeps-growing)

### The following command will create a new JSON key and download it

```
gcloud iam service-accounts keys create my-service-account.json --iam-account <EMAIL ADDRESS>
```

### Install a new plugin binary to support Kubectl access to GKE clusters-v1.25+

- Install using `gcloud components install`
  
  ```
  gcloud components install gke-gcloud-auth-plugin
  ```

- Install using `apt-get install` for DEB based systems
  
  ```
  apt-get install google-cloud-sdk-gke-gcloud-auth-plugin
  ```

- Install using `yum install` for RPM based systems
  
  ```
  yum install google-cloud-sdk-gke-gcloud-auth-plugin
  ```

### GCP HYbrid Interconnect

- steps to perform
  
  - Create Two Custom VPC Network
  - Create Firewall Rules in both VPC
  - Create Instance Each using one VPC
  - Verify Connectivity
  - Create Two VPN one for each Network
  - Create Static IP one for each Network
  - Set Forwarding Rules for each VPN Gateway
  - Create Tunnel between each Gateway
  - Create Route for Each Network

- Create Two VPN one for each Network 
  
  ```
  gcloud compute target-vpn-gateways create myvpn-1 --network <NETWORK_NAME> --region <SUBNET_REGION>
  ```

- Create Static IP one for each Network for each VPN
  
  ```
  gcloud compute addresses create --region <SUBNET_REGION> <STATIC_IP NAME>
  ```

- List Static IP, you just created
  
  ```
  gcloud compute list addresses list
  ```

- Set Forwarding Rules for each VPN Gateway
  
  - Set Forwarding Rule to SetUp send IP Address traffic to VPN gateway
    
    ```
    gcloud compute forwarding-rules create <RULE_NAME> --region <STATIC_IP_REGION> --ip-protocol ESP --address <YOUR_IP_ADDRESS> --target-vpn-gateway <GATEWAY_NAME>
    ```
    
    - Redirect UDP Traffic
      
      ```
      gcloud compute forwarding-rules create <RULE_NAME> --region <STATIC_IP_REGION> --ip-protocol UDP --ports 500 --address <YOUR_IP_ADDRESS> --target-vpn-gateway <GATEWAY_NAME>
      ```
    
    - Redirect UDP Traffic
      
      ```
      gcloud compute forwarding-rules create <RULE_NAME> --region <STATIC_IP_REGION> --ip-protocol UDP --ports 4500 --address <YOUR_IP_ADDRESS> --target-vpn-gateway <GATEWAY_NAME>
      ```
    
    - Create the Second Gateway with similar commands
    
    - list forwarding-rules list
      
      ```
      gcloud compute forwarding-rules list
      ```

- **NOTE** : Follow All the above commands with new Values for VPN-2

- List VPN Gateways
  
  ```
  gcloud compute target-vpn-gateways list
  ```

- Create Tunnel between each Gateway
  
  - Create a Tunnel between each VPC network. Create a Tunnel from First Gateway to Second Gateway VPC1-->VPC2
    
    ```
    gcloud compute vpn-tunnels create <TUNNEL_NAME> --peer-address <STATIC_IP_SECOND_GATEWAY> --region <REGION_FIRST_GATEWAY_SUBNET> --ike-version 2 --shared-secret <SECRET> --target-vpn-gateway <FIRST_VPN> --local-traffic-selector 0.0.0.0/0 --remote-traffic-selector 0.0.0.0/0
    ```
  
  - Create Second Tunnel, Direct traffic from the second VPC to First VPC VPC2-->VPC1
    
    ```
    gcloud compute vpn-tunnels create <TUNNEL_NAME> --peer-address <STATIC_IP_FIRST_GATEWAY> --region <REGION_SECOND_GATEWAY_SUBNET> --ike-version 2 --shared-secret <SAME_SECRET> --target-vpn-gateway <SECOND_VPN> --local-traffic-selector 0.0.0.0/0 --remote-traffic-selector 0.0.0.0/0
    ```
  
  - Get Tunnels list
    
    ```
    gcloud compute vpn-tunnels list
    ```

- Create Route for Each Network
  
  - Create a Static Router for both networks. The route goes out from First to Second Network
    
    ```
    gcloud compute routes create <ROUTE_NAME> --network <SOURCE_NETWORK> --next-hop-vpn-tunnel <FIRST_TUNNEL> --next-hop-vpn-tunnel-region <FIRST_TUNNEL_REGION> --destination-range <SECOND_NETWORK_SUBNET>
    ```
  
  - Create Second Route-
    
    ```
    gcloud compute routes create <ROUTE_NAME> --network <SOURCE_NETWORK> --next-hop-vpn-tunnel <SECOND_TUNNEL> --next-hop-vpn-tunnel-region <SECOND_TUNNEL_REGION> --destination-range <FIRST_NETWORK_SUBNET>
    ```
  
  - get the list of all routes
    
    ```
    gcloud compute routes list
    ```

### Hybrid Networking : It means connect google cloud with on-primesis data centre

1. **Cloud VPN - IPSEC** 

2. **Cloud Interconnect** : Dedicated interconnect , Partner Interconnect

3. **peering with Google** : Direct , Carrier
- connect instance with iap without public address "--tunnel-through-iap"
  
  ```
  gcloud compute ssh --zone "asia-southest1-b" "without-public" --tunnel-through-iap --project "gcp-network-349067"
  ```

- **Cloud Router**
  
  - It enables user to dynamically exchange routes between your VPC and on-primesis network.
  - Cloud Router is a fully distributed and managed Google Cloud service that uses the Border Gateway Protocol ( BGP ) to advertise IP address ranges
  - Router detect all changes and create new optimal routes like Google Maps
  - It makes intelligent decision and exchange information in network
  - Discovery of remote networks

- **Cloud VPN** : GCP connect with own private network
  
  - It connect peer network to google VPC through IPSec VPN
  - It works between google cloud and On-prim datacentre or google cloud with other cloud network like Azure,AWS etc.
  - Traffic between hybrid cloud is encrypted with One VPN gateway and Decrypted with Other VPN gateway.
  - Traffic Travelled over public Internet.
  - Single Cloud tunnel can support upto 3Gbps bandwidth.

- **Action to perform**Action to perform
  
  - Create Two VPC Network
  
  - Create Instance Each using one VPC
  
  - Verify Connectivity
  
  - Create Cloud Router for Each VPC
  
  - Create Static IP one for each Network
  
  - Create VPN Connection for Routers & Networks

### Cloud VPN with Static Routing

- Illustration :
  
  ```
  GCP VPC ++++++++++> CloudVPN <=========> Public Internet <=============> Router +++++++++> Office-On-Primesis-Network
  ```

- Cloud VPN with Static Routing but static IP address is required
  
  ```
  GCP-->Networking-->Create VPC+Subnet-->Firewall-->Allow SSH,ICMP protocol-->create static IP address
  ```

### Cloud VPN with Dynamic Routing

- Illustration :
  
  ```
  GCP VPC || Cloud Router ++++> CloudVPN <====> Public Internet + BGP Protocol <======> Router ++++++> Office-On-Primesis-Network
  ```

- Cloud VPN with Dynamic Routing but No static IP address is required
  
  ```
  GCP-->Networking-->Create VPC+Subnet-->Firewall-->Allow SSH,ICMP protocol
  ```
1. **Create VPN Connection for Routers & Networks**
   
   - Cloud VPN Tunnel And Gateway
     
     ```
     GCP-->Networking-->Hybrid-Connectivity-->VPN-->Create VPN connection-->Classic VPN-->Continue-->[ GCP Conpute Engine VPN Gateway Configuration Section-->Name : VPN-GCP | Network : VPC Network | Region : Select Region(Static IP exist) | IP address : Select Static IP ]-->[Tunnel(We can create Multiples tunnel also)Configuration Section-->Name : Tunnel Name | Remote Peer IP Address : On-prim Network Static IP address | IKE version : IKEv2 | IKE Pre-Shared Key : Genarate or copy key/use existing key or create own key(Required for connection in on prim)|Routing Option : Route Based(Select any Routing Option)|Remote network IP address range : on-primesis network IP/CIDR ]-->Done-->Create 
     ```
   
   - When the tunnel created one Tunnel VPN Gateway route automatically created
     
     ```
     GCP-->Networking-->Routes-->VPN Gateway Route exist(If not please create Route with Destination IP ranges,1000 priority,Next HOp destination Tunnel Route,Network network-on-primesis)
     ```
   
   - After VPN gateway created Static IP address att to it.
   
   - There is always problem with Static routing when new subnet added in existing VPC network so recommended is use Dynamic Routing

2. **Cloud VPN and Cloud Router**
   
   - Create Cloud Router for Each VPC
     
     ```
     GCP-->Networking-->Hybrid-Connectivity-->Cloud Router-->Create Router--> Name : Cloud Router Name | Network : Select GCP VPC | Region : Select Region | Google ASN : 64512(default Google recommended Value) | Advertise Routes : Advertise all subnet visible to the cloud Router-->create
     ```

3. **Create VPN Connection for Routers & Networks**
   
   - Create VPN gateway
     
     ```
     GCP-->Networking-->Hybrid-Connectivity-->VPN-->Create VPN connection-->Select High Availablity-->Continue-->[ GCP Cloud HA VPN Gateway Configuration Section-->Name : VPN-GCP | Network : VPC Network | Region : Select Region(Static IP exist) | VPN Tunnel inner IP Stack Type : Select IP type IPv4 ]-->Create & Contine-->
     ```
     
     ```
     [ Tunnel(We can create Multiples tunnel also)Configuration Section-->Add VPN Tuunel | Name : Tunnel Name | Interface : 0:Ip address1 1:Ip Address2 | Peer VPN Gateway : On-prim & GCP If GCP | select Gateway : Peer Gateway Name | High Availablity : Create a pair of VPN tunnel | Routing Option : Dynamic(BGP) | Cloud Router : Select Cloud Router--> 
     ```
     
     ```
     { VPN Tunnel-1 | Associate Cloud VPN Gateway Interface : 0:IP address1| Associate Peer VPN Gateway Interface : 0:Peer IP address1 | Name : Name of Tunnel-1| IKE : IKEv2| IKE Pre-Shared Key : Genarate or copy key/use existing key or create own key(Required for connection in on prim)}-->
     ```
     
     ```
     { VPN Tunnel-2 | Associate Cloud VPN Gateway Interface : 1:IP address1| Associate Peer VPN Gateway Interface : 1:Peer IP address2 | Name : Name of Tunnel-1| IKE : IKEv2| IKE Pre-Shared Key : Genarate or copy key/use existing key or create own key(Required for connection in on prim)
     }]--> Create & Continue-->
     ```
     
     ```
     Configuration BGP Session For Tunnel-1-->Name : BGP Session Name | peer ASN Name : Remote Peer Cloud Router ASN | Multiprotocol BGP | Allocate BGP IPv4 Address : Automatically--> Save BGP Configuration-->Save Reminder ScreeShot-->OK
     ```
     
     ```
     Configuration BGP Session For Tunnel-2-->Name : BGP Session Name | peer ASN Name : Remote Peer Cloud Router ASN | Multiprotocol BGP | Allocate BGP IPv4 Address : Automatically--> Save BGP Configuration-->Save Reminder ScreeShot-->OK
     ```
   
   - Dynamic Routing VPN Gateway routes doesn't Change and can't be edit like immutable

### Cloud NAT : Cloud Network Address Translation

- It is the solution which allow VM to connect internet without External IP

- It is bind to VPC-Region
  
  ```
  GCP-->Networking-->Network Services-->Cloud NAT-->Get Started-->Gateway Name : Name of Cloud NAT | Select Cloud Router |
  Network : SelectVPC | Region : Select Region | [ Create Cloud Router-->Name : Cloud Router Name | Network : SelectVPC | 
  Region : Select VPC region-->Create ] | Cloud NAT Mapping | Sources : Primary & Secondary ranges for all subnets | Cloud NAT IP Address : Automatic(recommended)-->Create
  ```

### Cloud Interconnect

- Extend your on premises VPC to GCP network

- highly available, low latency connection

- Cloud VPN use Public internet.

- Access resource with Internal IP address only

- Require time for initial setup

- Once setup, it works with very low latency & with Internal IP address

- No encryption while traffic travelled

- **We can use partner interconnect also with third party services provider like tata communication etc.**

- Illustration
  
  ```
  on-primesis ++++++++++++++++++++++> Service Provider +++++++++++++++++++++++++> GCP VPC Network
  ```
  
  ```
  GCP-->Networking-->Hybrid-Connectivity-->Interconnect-->Get Started-->Dedicated Interconnect Connection-->Continue-->Order new Dedicated interconnect Connection-->Continue-->[ Name : ConnectionName | Location : Location |
  Capacity : Speed of Connection | Create Redundant Interconnect | Create second Interconnect for Redundancy + SLA |Contact Information | Review | create ---> AFter some day Google representative Call you 
  ```

### BigQuery

- It is google serverless cloud storage platform designed for large data sets. 
- It in Non-RDBMS column base DataBase in Google Cloud Infra.
- It is an enterprise data warehouse built using BigTable.
- It works great with all size of data, from 100 rows Excel spreadsheet to several petabyte of data.
- It is fully managed solution for companies who need a fully-managed and cloud based interactive query service for massive dataset.
- It is superfast and execute search on millions of rows in seconds.
- it is great alternative for Apache Hive and used in analytics.
- It is ideal for BigData Solution.

### Lab BigTable

- Update the Packages
  
  ```
  sudo apt-get update
  ```

- Install Java 8 to work with BiTable
  
  ```
  sudo apt-get install openjdk-8-jdk-headless
  ```

- Export Environment Variable JAVA_HOME
  
  ```
  export JAVA_HOME=$(update-alternatives --list java | tail -1 | sed -E 's/\/bin\/java//')
  ```

- Clone the Cloud Project to Set-Up HBASE Terminal
  
  ```
  git clone https://github.com/GoogleCloudPlatform/cloud-bigtable-examples.git
  ```

- Start the HBASE Terminal
  
  ```
  cd cloud-bigtable-examples/quickstart
  ./quickstart.sh
  ```

### Lab CSV Data Handling in BigQuery

- Website to download the Data:
  https://population.un.org/wpp/Download/Standard/CSV/

- Queries :
  
  ```
  Select * from [TABLE] LIMIT 10000;
  Selct Top Contries via Population Variant wise:
  Select location, Time, PopTotal 
  FROM [TABLE] 
  WHERE Variant = '*****'
  ORDER BY PopTotal DESC LIMIT 20;
  Select Medium Variant Population of Each Country in 2021:
  Select location, Time, PopTotal 
  FROM [TABLE] 
  WHERE Variant = '*****' 
  AND Time = 2021;
  ```

### Lab - JSON Data Handling in BigQuery

- Command to Convert JSON to NewLine Delimited JSON
  
  ```
  sudo apt-get update -y
  sudo apt-get install -y jq
  cat mysample.json | jq -c '.[]' > mysampleNDJSON.json
  ```

### Lab - BigQuery via CLI

1. Get Help in BigQuery
   
   ```
   bq help
   ```

2. Include a command name to get information about a specific command
   
   ```
   bq help query
   ```

3. Examine a Table in any DataSet
   
   ```
   bq show bigquery-public-data:samples.shakespeare
   ```

4. Execute SQL Query from CLI
   
   ```
   bq query --use_legacy_sql=false \
   'SELECT
   word,
   SUM(word_count) AS count
   FROM
   `bigquery-public-data`.samples.shakespeare
   WHERE
   word LIKE "%the%"
   GROUP BY
   word'
   ```

5. Find default project has any existing datasets.
   
   ```
   bq ls
   ```

6. Download Sample Data 
   http://www.ssa.gov/OACT/babynames/names.zip

7. create a new dataset.
   
   ```
   bq mk baby_names
   ```

8. Verify DataSet Created
   
   ```
   bq show baby_names
   ```

9. Upload a Table
   
   ```
   bq load --source_format=CSV baby_names.names_2016 <BUCKET_URL> name:string,gender:string,count:integer
   ```

10. List Tables
    
    ```
    bq ls baby_names
    bq show baby_names.names_2016
    ```

11. Run Some Quries
    
    ```
    bq query "SELECT name,count FROM baby_names.names_2016 WHERE gender = 'F' ORDER BY count DESC LIMIT 10"
    bq query "SELECT name,count FROM baby_names.names_2016 WHERE gender = 'M' ORDER BY count ASC LIMIT 10"
    ```

12. CleanUp a DataSet
    
    ```
    bq rm -r baby_names.names_2016
    bq rm -r baby_names
    ```
    
    ### Lab - WikiData in BigQuery
- Create Schema
  
  ```
  bq mk wiki_data
  ```

- Create Table and Load Data:
  
  ```
  bq load \
  --source_format CSV \
  --field_delimiter " " \
  --quote "" \
  --max_bad_records 3 \
  $GOOGLE_CLOUD_PROJECT:wiki_data.wiki_page_set1 \
  gs://cloud-samples-data/third-party/wikimedia/pageviews/pageviews-20190410-140000.gz \
  wiki,title,requests:integer,zero:integer
  ```

- Perform Query in BigQuery
  
  ```
  SELECT title, SUM(requests) requests
  FROM wiki_data.wiki_page_set1
  WHERE
  wiki = "en"
  AND REGEXP_CONTAINS(title, 'Red.*t')
  GROUP BY title
  ORDER BY requests DESC
  ```
  
  ```
  SELECT title, SUM(requests) requests
  FROM wiki_data.wiki_page_set1
  WHERE
  wiki = "en"
  GROUP BY title
  ```
  
  ```
  SELECT title, requests
  FROM wiki_data.wiki_page_set1
  WHERE
  wiki = "en"
  ```

### Install kubectl or gloucd components operations

- To install specific component
  
  ```
  gcloud components install kubectl 
  ```

- To list all available installed or not installed component
  
  ```
  gcloud components list
  ```

- To reinstall the component
  
  ```
  gcloud components reinstall kubectl
  ```

- To remove the component
  
  ```
  gcloud components remove kubectl
  ```

- To restore component 
  
  ```
  gcloud components restore
  ```

- To update the all installed modules
  
  ```
  gcloud components update
  ```

- Check gke logs for pod it return snapshot of previous terminated ruby container logs from pod web-1
  
  ```
  kubectl logs -p -c ruby web-1
  ```

- Check gke logs for pod it return begin streaming the logs of the ruby container logs from pod web-1
  
  ```
  kubectl logs -f -c ruby web-1
  ```

- Check gke logs for pod it return most recent 20 lines of outputs in pod nginx
  
  ```
  kubectl logs -tail=20 nginx
  ```

- Check gke logs for pod it return last 1 hour ruby container logs from pod web-1
  
  ```
  kubectl logs --since=1h nginx
  ```

### Kubernetes headless service

- When using headless service we should use not the "Service port and Target port" is same.
- To create headless service we need to define "clusterIP=None" in service

### GKE private cluster

- In network "private cluster flag" should be enabled.
- "control plane authorized network enabled" for private cluster kubeapi server (kubectl get pod) access from specific network.
- It will hide the all GKE node behind VPC and all other k8s component(schedular etc.) communicate by VPC peering.
- To access private cluster for download dockerimages from dockerhub we need to create Cloud NAT for k8s ccommunication with internet.

### create and restore PVC by volume snapshot for GKE by volumesnapshotclass for persistent disk

- We can find the snapshot details in GCP by compute engine-->snapshots-->your snapshot name

### Create mysql external service name with CloudSQL for database by its external name with public IP and private IP

- mysql-externalName-Service.yaml 
  
  ```
  apiVersion: v1
  kind: Service
  metadata: 
      name: mysql-externalName-service
  spec:
      type: ExternalName
      externalName: 35.167.78.98 #External IP for CLoudSQL MySQL Database Server
  ```

- mysql-externalName-Service.yaml 
  
  ```
  apiVersion: v1
  kind: Service
  metadata: 
      name: mysql-externalName-service
  spec:
      type: ExternalName
      externalName: 10.0.1.9 #Internal IP for CLoudSQL MySQL Database Server
  ```

- myapp.yaml
  
  ```
  apiVersion: apps/v1
  kind: Deployment 
  metadata:
    name: usermgmt-webapp
    labels:
      app: usermgmt-webapp
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: usermgmt-webapp
    template:  
      metadata:
        labels: 
          app: usermgmt-webapp
      spec:
        #To check the DataBase connection availablity before start container
        initContainers:
          - name: init-db
            image: busybox:1.31
            command: ['sh', '-c', 'echo -e "Checking for the availability of MySQL Server deployment"; while ! nc -z mysql-externalname-service 3306; do sleep 1; printf "-"; done; echo -e "  >> MySQL DB Server has started";']      
        containers:
          - name: usermgmt-webapp
            image: stacksimplify/kube-usermgmt-webapp:1.0.0-MySQLDB
            imagePullPolicy: Always
            ports: 
              - containerPort: 8080           
            env:
              - name: DB_HOSTNAME
                value: "mysql-externalname-service"            
              - name: DB_PORT
                value: "3306"            
              - name: DB_NAME
                value: "webappdb"            
              - name: DB_USERNAME
                value: "root"            
              - name: DB_PASSWORD
                valueFrom:
                  secretKeyRef:
                    name: mysql-db-password
                    key: db-password
  ```

- MySQL Client 8.0: Replace External Name Service, Username and Password
  
  ```
  kubectl run -it --rm --image=mysql:8.0 --restart=Never mysql-client -- mysql -h mysql-externalname-service -u root -pKalyanReddy13
  ```

### filestore CSI driver is running as daemonset in each node of GKE

```
kubectl -n kube-system get ds | grep file
O/P : 
filestore-node kubernetes.io/os=linux  2d1h 3 3 3 3 3
```

### Ingress Classes & Annotation for Load Balancer setting

- External Ingress
  
  ```
  annotation:
      kubernetes.io/ingress.class:"gce"
  ```

- Internal Ingress
  
  ```
  annotation:
      kubernetes.io/ingress.class:"gce-internal"
  ```

- Multicluster Ingress
  
  - k8s Services : 
    1. **MultiClusterService** 
    2. **MultiClusterServiceIngress**

- Third Party Ingress(Nginx)
  
  ```
  kubernetes.io/ingress.class:"nginx"
  ```

### Ingress context path base routing for GCE kubernestes cluster

- Ingress Route.yaml
  
  ```
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: ingress-cpr
    annotations:
      # External Load Balancer  
      kubernetes.io/ingress.class: "gce"  
  spec: 
    defaultBackend:
      service:
        name: app3-nginx-nodeport-service
        port:
          number: 80                            
    rules:
      - http:
          paths:           
            - path: /app1
              pathType: Prefix
              backend:
                service:
                  name: app1-nginx-nodeport-service
                  port: 
                    number: 80
            - path: /app2
              pathType: Prefix
              backend:
                service:
                  name: app2-nginx-nodeport-service
                  port: 
                    number: 80
  ```

- To get ingress accessing IP or DNS Name
  
  ```
  kubectl get ingress
  ```

### Create ingress with External IP pre-defined so it will not changed and make it reserve static

- Create External IP Address
  
  ```
  gcloud compute addresses create ADDRESS_NAME --global
  gcloud compute addresses create gke-ingress-extip1 --global
  ```

- Describe External IP Address 
  
  ```
  gcloud compute addresses describe ADDRESS_NAME --global
  gcloud compute addresses describe gke-ingress-extip1 --global
  ```

- List External IP Address
  
  ```
  gcloud compute addresses list
  ```

- Verify
  
  ```
  Go to VPC Network -> IP Addresses -> External IP Address 
  ```

- Add RECORDSET Google Cloud DNS for this External IP
  
  ```
  - Go to Network Services -> Cloud DNS -> sawanchouksey.com -> **ADD RECORD SET**
  - DNS NAME: demo1.sawanchouksey.com
  - **IPv4 Address:** <EXTERNAL-IP-RESERVERD-IN-STEP-02>
  - Click on **CREATE**
  ```

- nslookup test
  
  ```
  nslookup demo1.sawanchouksey.com
  ```

- Create Ingress-external-ingress-ip.yaml
  
  ```
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: ingress-external-ip
    annotations:
      # External Load Balancer
      kubernetes.io/ingress.class: "gce"  
      # Static IP for Ingress Service
      kubernetes.io/ingress.global-static-ip-name: "gke-ingress-extip1"   
  spec: 
    defaultBackend:
      service:
        name: app3-nginx-nodeport-service
        port:
          number: 80                            
    rules:
      - http:
          paths:           
            - path: /app1
              pathType: Prefix
              backend:
                service:
                  name: app1-nginx-nodeport-service
                  port: 
                    number: 80
            - path: /app2
              pathType: Prefix
              backend:
                service:
                  name: app2-nginx-nodeport-service
                  port: 
                    number: 80
  ```

### Create google managed certificate for ingress in GCP

- Google Managed Certificates for GKE Ingress

- Ingress SSL

- Certificate Validity: 90 days

- 30 days before expiry google starts renewal process. We dont need to worry about it.

- Google-managed certificates are only supported with GKE Ingress using the external HTTP(S) load balancer. Google-managed certificates do not support third-party Ingress controllers.

- Registered Domain using Google Cloud Domains

- DNS name for which SSL Certificate should be created should already be added as DNS in Google Cloud DNS (Example: demo1.sawanchouksey.com)

- Create manage-certificate-ssl.yaml
  
  ```
  apiVersion: networking.gke.io/v1
  kind: ManagedCertificate
  metadata:
    name: managed-cert-for-ingress
  spec:
    domains:
      - demo1.sawanchouksey.com
  ```

- Create Ingress-SSL.yaml
  
  ```
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: ingress-ssl
    annotations:
      # External Load Balancer
      kubernetes.io/ingress.class: "gce"  
      # Static IP for Ingress Service
      kubernetes.io/ingress.global-static-ip-name: "gke-ingress-extip1"   
      # Google Managed SSL Certificates
      networking.gke.io/managed-certificates: managed-cert-for-ingress
  spec: 
    defaultBackend:
      service:
        name: app3-nginx-nodeport-service
        port:
          number: 80                            
    rules:
      - http:
          paths:           
            - path: /app1
              pathType: Prefix
              backend:
                service:
                  name: app1-nginx-nodeport-service
                  port: 
                    number: 80
            - path: /app2
              pathType: Prefix
              backend:
                service:
                  name: app2-nginx-nodeport-service
                  port: 
                    number: 80
  ```

- List Managed Certificate
  
  ```
  kubectl get managedcertificate
  ```

- Describe managed certificate
  
  ```
  kubectl describe managedcertificate managed-cert-for-ingress
  ```

- Verify SSL Certificates from Certificate Tab in Load Balancer
  
  ```
  GCP-->search-->load balancing-->Network services-->Load Balancing-->Load Balancer-->click on "load balancing components view"-->click on "certificates" tab-->select certificate
  ```

- Http to https redirecting ingress services

- Create frontendconfig.yaml
  
  ```
  apiVersion: networking.gke.io/v1beta1
  kind: FrontendConfig
  metadata:
    name: my-frontend-config
  spec:
    redirectToHttps:
      enabled: true
      #responseCodeName: RESPONSE_CODE
  ```

- Create Ingress-SSL.yaml
  
  ```
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: ingress-ssl
    annotations:
      # External Load Balancer
      kubernetes.io/ingress.class: "gce"  
      # Static IP for Ingress Service
      kubernetes.io/ingress.global-static-ip-name: "gke-ingress-extip1"   
      # Google Managed SSL Certificates
      networking.gke.io/managed-certificates: managed-cert-for-ingress
      # SSL Redirect HTTP to HTTPS
      networking.gke.io/v1beta1.FrontendConfig: "my-frontend-config"    
  spec: 
    defaultBackend:
      service:
        name: app3-nginx-nodeport-service
        port:
          number: 80                            
    rules:
      - http:
          paths:           
            - path: /app1
              pathType: Prefix
              backend:
                service:
                  name: app1-nginx-nodeport-service
                  port: 
                    number: 80
            - path: /app2
              pathType: Prefix
              backend:
                service:
                  name: app2-nginx-nodeport-service
                  port: 
                    number: 80
  ```

### Enable external DNS for LoadBalancer type service

```
annotations:
    external-dns.alpha.kubernestes.io/hostname: extdns.k8s.svc.demo.sawan.com
```

### Ingress with IAP(Identity Aware Proxy)

- IAP enable Centralize authentication and authorization accessed using HTTPS
- with IAP, we can enforce Access control policies to our applications
- With IAP we can enable group based application access i.e. A specific resource application can given access to only employess not for contractors.

### Add approval in CICD pipeline

- Enable cloud build approvals in GCP pipeline and enable with email id.
  
  ```
  IAM-->Service account-->edit-->add role-->cloudbuild approver.
  ```

### Defined resource Quata for namespace

```
apiVersion: v1
kind: ResourceQuota
metadata:
  name: qa-namespace-resource-quota
  namespace: qa
spec:
  hard:
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi  
    pods: "3"    
    configmaps: "3" 
    persistentvolumeclaims: "3" 
    secrets: "3" 
    services: "3"
```

### Define limitrange quota for namespace

```
apiVersion: v1
kind: ResourceQuota
metadata:
  name: qa-namespace-resource-quota
  namespace: qa
spec:
  hard:
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi  
    pods: "3"    
    configmaps: "3" 
    persistentvolumeclaims: "3" 
    secrets: "3" 
    services: "3" 
---    
apiVersion: v1
kind: LimitRange
metadata:
  name: default-cpu-mem-limit-range
  namespace: qa
spec:
  limits:
    - default:
        cpu: "400m"  # If not specified default limit is 1 vCPU per container     
        memory: "256Mi" # If not specified the Container's memory limit is set to 512Mi, which is the default memory limit for the namespace.
      defaultRequest:
        cpu: "200m" # If not specified default it will take from whatever specified in limits.default.cpu      
        memory: "128Mi" # If not specified default it will take from whatever specified in limits.default.memory
      max: 
        cpu: "500m"
        memory: "500Mi"
      min:       
        cpu: "100m"
        memory: "100Mi"
      type: Container
```

### LimitRange quota with minMax in namespace

```
apiVersion: v1
kind: LimitRange
metadata:
  name: default-cpu-mem-limit-range
  namespace: qa
spec:
  limits:
    - default:
        cpu: "400m"  # If not specified default limit is 1 vCPU per container     
        memory: "256Mi" # If not specified the Container's memory limit is set to 512Mi, which is the default memory limit for the namespace.
      defaultRequest:
        cpu: "200m" # If not specified default it will take from whatever specified in limits.default.cpu      
        memory: "128Mi" # If not specified default it will take from whatever specified in limits.default.memory
      max: 
        cpu: "500m"
        memory: "500Mi"
      min:       
        cpu: "100m"
        memory: "100Mi"
      type: Container
```

### Ingress with SSL certificate with existing IP

- Create application with NodePort service type 

- update application with readiness probe for health

- Create External IP Address
  
  ```
  gcloud compute addresses create poc-ip --global
  ```

- Certificate creation with pfx certificate
  
  ```
  openssl pkcs12 -in NewSSL2024.pfx -nocerts -out server-en.key (give cert password)
  openssl pkcs12 -in NewSSL2024.pfx -clcerts -nokeys -out app1-ingress.crt
  openssl rsa -in server-en.key -out app1-ingress.key (give PEM pass password)
  ```

- Create a certificate resource in your Google Cloud project
  
  ```
  gcloud compute ssl-certificates create app1-ingress --certificate app1-ingress.crt  --private-key app1-ingress.key
  ```

- List certificate
  
  ```
  gcloud compute ssl-certificates list
  ```

- Http to https redirecting ingress services
  
  - frontendconfig.yaml
    
    ```
    apiVersion: networking.gke.io/v1beta1
    kind: FrontendConfig
    metadata:
      name: my-frontend-config
    spec:
      redirectToHttps:
        enabled: true
    ```
  
  - create secret for ingress SSL certificate `Ingress-tls-secret.yaml`
    
    ```
    apiVersion: v1
    kind: Secret
    metadata:
      name: ingress-tls-secret
      namespace: default
    type: kubernetes.io/tls
    data: 
      tls.crt: "base64 encoded cert"
      tls.key: "base64 encoded key"
    ```
  
  - Create Ingress Route File `Ingress-Route.yaml`
    
    ```
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: ingress-route
      annotations:
        # External Load Balancer
        kubernetes.io/ingress.class: "gce"
        #Name of load balancer
        networking.gke.io/load-balancer-name: my-load-balancer-name
        # SSL Redirect HTTP to HTTPS
        #networking.gke.io/v1beta1.FrontendConfig: "my-frontend-config"
        #redirect ingress to ssl
        #ingress.kubernetes.io/ssl-redirect: "true"
        # Static IP for Ingress Service
        kubernetes.io/ingress.global-static-ip-name: "gke-ingress-uat-ip"   
        # SSL Redirect HTTP to HTTPS
        networking.gke.io/v1beta1.FrontendConfig: "my-frontend-config"   
        # Pre-shared certificate resources  
        ingress.gcp.kubernetes.io/pre-shared-cert: "app1-ingress"
    spec:
    #  tls:
    #  - hosts:
    #    - dev.tyh.poc.com
    #    secretName: ingress-tls-secret
      rules:
        - http:
            paths:
            - path: /api
              pathType: Prefix
              backend:
                service:
                  name: tyh-test-uat
                  port:
                    number: 4001
    spec:
      rules:
        - host: dev.tyh.poc.com
          http:
            paths:
              - path: /patient(/|$)(.*)
                pathType: prefix
                backend:
                  service:
                    name: tyh-webui-poc
                    port:
                      number: 3000
              - path: /api(/|$)(.*)
                pathType: Prefix
                backend:
                  service:
                    name: tyh-test-poc
                    port:
                      number: 4001
        #- host: qa.tyh.poc.com
        #  http:
        #    paths:
        #      - path: /pat(/|$)(.*)
        #        pathType: prefix
        #        backend:
        #          service:
        #            name: tyh-webui-poc
        #            port:
        #              number: 3000
        #      - path: /api(/|$)(.*)
        #        pathType: Prefix
        #        backend:
        #          service:
        #           name: tyh-test-poc
        #            port:
        #             number: 4001
    ```

### get ip only from gcloud describe command

```
gcloud compute addresses describe ingress-dev  --region asia-south1 --format=json | jq -r '.address'
```

### Use substitution variable in GCP cloud build pipeline

```
variableName = _SONAR_TOKEN
UseInYamlfile= ${_SONAR_TOKEN}
```

### Terraform with google cloud

- provider configuration
  
  ```
  terraform {
      required_providers{
          google = {
              source = "hashicorp/google"
              version= "3.84.0"
              } 
          }
      }
  }
  provider "google" {
      project = "my-project-id"
      region  = "us-central1"
      zone    = "us-central1-a"
  }
  ```

- Connect Terraform with GCP by username/password run command with gcloud
  
  ```
  gcloud auth application-default login
  ```

- list of gcloud account
  
  ```
  gcloud auth list
  ```

- connect terraform with cloudshell VM

- Connect terraform with GCP with service account - preferred in production
  
  ```
  gcp-->IAM and Admin-->select service-account-->manage keys-->ADD KEY-->create key-->key type :JSON-->create-->downloaded keys.json file for this project-->
  ```

- give access to "editor" role for the service-account

- move "keys.json" file to folder where main.tf exist for root module
  
  ```
  provider "google" {
      project = "my-project-id"
      region  = "us-central1"
      zone    = "us-central1-a"
      credentials = "keys.json"
  }
  ```

### Delete an ip address

```
gcloud compute addresses delete address-name --region regionName | --global
gcloud compute addresses delete gke-ingress-uat-ip --global
```

### Cloud Run

- It is used to deploy complete application in GCP
- It is works as similar way like serverless container application like ACI in azure.
- It is help to focus developers on development instead of maintenance and deployment of application.

### Uptime check and manage notification

```
gcp-->monitoring-->uptime check-->configure HTTP URL and mnagae Chnannel notification for it
```

### Logging available in GCP

| Logs Details        | Enable                | Days Retention | Activities Capture          |
| ------------------- | --------------------- | -------------- | --------------------------- |
| Admin Activity logs | Enable By default     | 400 days       | Generated by activities     |
| System logs         | Enable By default     | 400 days       | Generated by google System  |
| data access logs    | By default Not Enable | 30 days        | -                           |
| Policy Logs         | Enable By default     | 30 days        | Generated by Policy Changes |

### log collection

- **by agent**
  
  - Log Agent for Compute engine VM | AWS VM | Azure VM 
  - Legacy Agent | Ops Agent

- **by Cloud SDK**
  
  ```
  gcloud logging write log-name "log info message"
  gcloud logging write log-name '{"key":"value"} --payload-type=json --severity CRITICAL 
  ```

- Automatically on Cloud Run, GKE, App Engine

- **Cloud Logging API**
  
  - Python/Java SDK
  - From on-premises

- Logs Storage is used for store logs data in customize bucket.

- logs router used to sync and route data to logs storage buckets by creating synk between gcp service and bucket.

### DevOps tool

- **Cloud Error Reporting** -  detect error
  
  ```
  GCP-->Operation-->Error reporting(App Engine)
  ```

- **Cloud Debugger** - Find state of running application
  
  ```
  GCP-->Operation-->Debugger(App Engine)
  ```

- **Cloud Trace** - Latency
  
  ```
  GCP-->Operation-->Trace(App Engine)
  ```

- **Cloud Profiler** - How much resource consumed
  
  ```
  GCP-->Operation-->Profiles(App Engine)
  ```

### Pre-emptible VM

- Up to **80% discount**

- max life is **24 hours**

- Goggle give **30 sec** warning before **auto shutdown**
  
  ```
  GCP-->ComputeEngine-->create instance-->Management Secuirty-->Availablity Policy-->Preemptibility(off(recommended))-->change to on
  ```

### SSL certificate in gcloud cli error

```
gcloud components update
```

### Download file from cloud shell

```
cloudshell download cluster.sh
```

### **Apache beam** - Dataflow service

- Apache Beam is helpful to create the the DataProcessing Pipeline.

- Beam is a framework with bindings in both Python and Java that allows you to represent a data processing pipeline with actions for inputs and outputs as well as a variety of built-in data transformations.

- Pipeline is unit which collects the Data, process the data and produce the output.

- Data that flows through the pipeline called PCollections.

- Manipulations happens on data in pipeline called Transformation.
  
  ```
        +---------------+
        |   Input Data  |
        +-------+-------+
                |
                v
        +-------+-------+
        | Data Ingestion|
        +-------+-------+
                |
                v
        +-------+-------+
        |   Transform   |
        +-------+-------+
                |
                v
        +-------+-------+
        | PCollection 1 |
        +-------+-------+
                |
                v
        +-------+-------+
        |   Transform   |
        +-------+-------+
                |
                v
        +-------+-------+
        | PCollection 2 |
        +-------+-------+
                |
                v
        +-------+-------+
        |   Transform   |
        +-------+-------+
                |
                v
        +-------+-------+
        | PCollection 3 |
        +-------+-------+
                |
                v
        +-------+-------+
        |    Write      |
        +-------+-------+
                |
                v
        +-------+-------+
        |  Output Data  |
        +---------------+
  ```

### **Pipeline** :

- A pipeline refers to the high-level container of a bunch of data processing operations. Pipelines encapsulate all of the input and output data as well as the transformation steps that manipulate data from the input to the desired output.

- Pipelines themselves can have lots of configuration options, which allows them to be somewhat customizable.

- **PCollections** : 
  
  - PCollections, the data in your pipeline, act as a way to represent intermediate chunks or streams of data as they flow through a
    pipeline. User can create them either by reading from some raw data points or by applying some transformation to another PCollection.
  - The data could be of any size, ranging from a few rows that you add to your pipeline code to an enormous amount of data distributed across lots of
    machines. In some cases, the data could even be an infinite stream of incoming data that may never end.
  - PCollection can be either bounded or unbounded. Bounded, you may not know the exact size. A bounded PCollection is one that you’re sure won’t go on forever.
  - Unbounded PCollection is one that has no predefined finite size and may go on forever. The typical example of an unbounded PCollection
    is a stream of data that’s being generated in real time, such as the temperature sensor.
  - PCollection can’t be share in between Pipelines. User always create a PCollection within a pipeline, and it must stay within that pipeline.
    You can’t create a PCollection inside one pipeline and then reference it from another.
  - PCollections themselves are immutable. Once you create a PCollection, you can’t change its data.

- **Transforms** : 
  
  - Transforms are the way you take chunks of input data and mutate them into chunks of output data.
  - Transforms are the way to take PCollections and turn them into other PCollections.
  - Transforms can do a variety of things, and Beam comes with quite a few built-in transforms to help make it easy to manipulate data in your pipelines without writing a lot of boilerplate code.
  - Filter out unwanted data that you’re not interested.
  - Split the data into separate chunks.
  - Group the data by a certain property.
  - Join together two (or more) chunks of data.
  - Enrich the data by calculating something new.

### Lab - Running Python DataFlow

1. Enable Cloud Data Flow API from API Manager

2. Create a Standard Google Cloud Storage Bucket

3. Download the Code from below shared Bucket.
   https://github.com/GoogleCloudPlatform/training-data-analyst.git and 
   
   ```
   - run sudo ./install_package.sh
   - run python3 grep.py
   - run gsutil cp ../javahelp/..../javahelp/*.java gs://bucketName
   ```

4. Change Project and Bucket name in grepc.py file. It will do all above steps automatically give region in input variable

5. Identify the Service Account and provide the DataFlow Admin and Worker Role to Service Account.

6. If Job is failing with write permission in Storage then in Storage permission Section, identify your Service Account and provide the right of Storage Admin.

### Lab - Provision DataProc Cluster with Command Line

- SetUp DataProc Cluster Using GCloud
  
  1. Enable the DataProc Cloud API if already Not enabled.
  
  2. Open Cloud Shell and verify the Project
     
     ```
     gcloud config list project
     echo $GOOGLE_CLOUD_PROJECT
     ```
  
  3. Set Project if not already set.
     
     ```
     gcloud config set project <PROJECT_ID>
     ```
  
  4. Import the Zone which you want to use.
     
     ```
     gcloud config set compute/zone us-central1-c
     ```
  
  5. Choose Cluster Name
     
     ```
     CLUSTERNAME=${USER}-levelup
     ```
  
  6. Start a New Cluster
     
     ```
     gcloud dataproc clusters create ${CLUSTERNAME} --region us-central1 --subnet default --zone us-central1-c --master-machine-type n1-standard-1 --master-boot-disk-size 50 --num-workers 2 --worker-machine-type n1-standard-1 --worker-boot-disk-size 50 --image-version 1.4-debian10 --project ${GOOGLE_CLOUD_PROJECT}
     ```
  
  7. Submit a Spark job to your cluster
     
     ```
     gcloud dataproc jobs submit spark --cluster ${CLUSTERNAME} \
     --class org.apache.spark.examples.SparkPi \
     --jars file:///usr/lib/spark/examples/jars/spark-examples.jar -- 1000
     ```
  
  8. Get the List of Jobs
     
     ```
     gcloud dataproc jobs list --cluster ${CLUSTERNAME}
     ```
  
  9. Get the Output of any Job
     
     ```
     gcloud dataproc jobs wait jobId
     ```
  
  10. Describe your DataProc Cluster
      
      ```
      gcloud dataproc clusters describe ${CLUSTERNAME}
      ```
  
  11. Resize the Cluster
      
      ```
      gcloud dataproc clusters update ${CLUSTERNAME} --num-preemptible-workers=2
      gcloud dataproc clusters describe ${CLUSTERNAME}
      ```
  
  12. SSH into Cluster Master Node
      
      ```
      gcloud compute ssh ${CLUSTERNAME}-m --zone=us-central1-c
      hostname
      ```
  
  13. List Cluster and Logout
      
      ```
      gcloud dataproc clusters list --region us-central1
      logout
      ```
  
  14. Delete the Cluster
      
      ```
      gcloud dataproc clusters delete ${CLUSTERNAME}
      ```

### Lab - Pub/Sub using CLI

1. Reinitialize Cloud SDK and follow the instructions
   
   ```
   gcloud init
   ```

2. Create topic in Pub/Sub
   
   ```
   gcloud pubsub topics create <Topic_Name>
   ```

3. Publish a Message to Topic
   
   ```
   gcloud pubsub topics publish foodmart --message="hello foodies" --attribute="locale=english,username=gcp"
   ```

4. Create Subscriber in PubSub
   
   ```
   gcloud pubsub subscriptions create --topic <Topic_Name> <Subscriber_Name>
   ```

5. Check if Subcriber received the earlier message published on Topic
   
   ```
   gcloud pubsub subscriptions pull --auto-ack <Subscriber_Name>
   ```

### Lab - Setting Up Pub/Sub Using Python

1. Clone python-docs-samples and change directory to the sample directory you want to use.
   git clone https://github.com/googleapis/python-pubsub.git

2. Create a virtualenv. Samples are compatible with Python 3.6+.
   
   ```
   virtualenv env
   source env/bin/activate
   ```

3. Install the dependencies needed to run the samples.
   
   ```
   pip install -r requirements.txt
   ```

4. Run Samples
   
   ```
   - python publisher.py
   ```

5. positional arguments for `publisher.py`
   
   | Arguments                      | Description                                                            |
   | ------------------------------ | ---------------------------------------------------------------------- |
   | project_id                     | Your Google Cloud project ID                                           |
   | list                           | Lists all Pub/Sub topics in the given project.                         |
   | create                         | Create a new Pub/Sub topic.                                            |
   | delete                         | Deletes an existing Pub/Sub topic.                                     |
   | publish                        | Publishes multiple messages to a Pub/Sub topic.                        |
   | publish-with-custom-attributes | Publishes multiple messages with custom attributes to a Pub/Sub topic. |
   | publish-with-error-handler     | Publishes multiple messages to a Pub/Sub topic with an error handler.  |
   | publish-with-batch-settings    | Publishes multiple messages to a Pub/Sub topic with batch settings.    |
   | publish-with-retry-settings    | Publishes messages with custom retry settings.                         |

6. Subscribe the publisher data
   
   ```
   python subscriber.py
   ```

7. positional arguments for `subscriber.py`
   
   | Arguments                               | description                                                                                                                                                    |
   | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | project_id                              | Your Google Cloud project ID                                                                                                                                   |
   | list-in-topic                           | Lists all subscriptions for a given topic.                                                                                                                     |
   | list-in-project                         | Lists all subscriptions in the current project.                                                                                                                |
   | create                                  | Create a new pull subscription on the given topic.                                                                                                             |
   | create-with-dead-letter-policy          | Create a subscription with dead letter policy.                                                                                                                 |
   | create-push                             | Create a new push subscription on the given topic.                                                                                                             |
   | delete                                  | Deletes an existing Pub/Sub topic.                                                                                                                             |
   | update-push                             | Updates an existing Pub/Sub subscription's push endpoint URL. Note that certain properties of a           subscription, such as its topic, are not modifiable. |
   | update-dead-letter-policy               | Update a subscription's dead letter policy.                                                                                                                    |
   | remove-dead-letter-policy               | Remove dead letter policy from a subscription.                                                                                                                 |
   | receive                                 | Receives messages from a pull subscription.                                                                                                                    |
   | receive-custom-attributes               | Receives messages from a pull subscription.                                                                                                                    |
   | receive-flow-control                    | Receives messages from a pull subscription with flow control.                                                                                                  |
   | receive-synchronously                   | Pulling messages synchronously.                                                                                                                                |
   | receive-synchronously-with-lease        | Pulling messages synchronously with lease management                                                                                                           |
   | listen-for-errors                       | Check for if any error exist while pulling                                                                                                                     |
   | receive-messages-with-delivery-attempts | Support Me                                                                                                                                                     |

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚