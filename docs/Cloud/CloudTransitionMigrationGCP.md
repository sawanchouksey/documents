# Planning Your Cloud Migration and Transition with Google Cloud (GCP)

## Start thinking like Upper Management.

## Role of Cloud Architect is to fill the gap of Technical Requirement & Business Requirement.

## What do your Senior Leadership care about?

## Questions to ask when planning Cloud Transition?

- What does Google Cloud do, that we can’t do right now?
- Why should be migrate our resources to GCP?
- Start Asking why?
  - Why should leadership care?

## Why’s leadership care about?

- Costs
- Future-proof infrastructure
- Scale to Meet Demand
- Data Analytics
- Greater Business Agility
- Managed Services
- Global Reach
- Security at Scale

## Every Company have their own Why’s?

### Cost

- Cost is main factor for any Business
- Basic Funda - Do More with Less Cost
- No Upfront SetUp Cost, pay for your uses

### Future Proof Infrastructure

- Hardware doesn’t end life.
- Migrating to New Hardware frequently is a pain and need lot of homework and migration work.

### Scale to Meet Demand

- Distributed Computing (Elastic Computing)
- Dynamically Scale / Descale Machines as per need
  - Pay for only what you need/use at a moment

### Greater Business Agility

- Speedy Infrastructure
- Speedy Resource Creation
- Faster Data Processing
- No waiting on Hardware

### Managed Services

- Let Google Manage Infrastructure
- Less Administrative Overhead
- Serverless Support

### Global Reach

- Easy Worldwide presence
- Multinational resources on Same VPC

### Security at Scale

- Unmatched Security with Google.
- Easy access Management of projects

## Biggest Concern with Saving Cost

### All Business want to do More in less cost.

### GCP is cheapest public cloud available as of now and having multiple cost saving plans.

### Sustained Use Discount -

- Upto 30% discount Cloud Engine/Cloud SQL VMs.
- Longer the Resource will be in use, the greater the discount.
- Different VMs have different discount Mechanism.
- No Upfront commitment
- Automatic and Simple Discounts

### Custom Machines

- Unique to GCP
- Customize RAM and CPUs

### Rightsize Recommendation

- Automatically recommend machine type resizing for compute engine VM.
- Takes last 8 days of uses.
- Recommended sizing up and down to increase performance/ save cost.
- Recommends custom machine types where applicable.

### Preemptible VMs

- Low cost, short life, interruptible VM
- Upto 80% Discount
- Fixed Price not variable Market Price
- Ideal for fault tolerant, Batch processing workloads

### Nearline and Coldline Storage

- Low cost and very Low Cost Cloud Storage
- Ideal for archive/disaster recovery data
- Unique to GCP - Low cost but same fast access as premium storage

### Committed Use Discount

- Commit for 1 or 3 year for Set Amount of Resources.
- Upto 57% Discount
- Billed for CPU/RAM, whether or not they are in use.
- Committed Use Discount on All Machines

## Principles of Good Cloud Design -

1. #### High Availability

2. #### Scalability

3. #### Security

4. #### Disaster Recovery

5. #### Cost Control

### High Availability

- Can User access the application with minimum latency.
- Placement of Resources
- Serve Traffic to multiple regions via Global Load Balancer.

### Scalability

- Scale / Descale Resource on Demand.
- Best Practice - Run Load Tests
- GCE - Managed Instance groups with autoscaling
- GKE - Cluster with Auto Scaling Enable
- GAE - Autoscaler Built-in

### Security

- Limit access to those, who need it.
- Principle of least privilege
- Secure Administrative Access
- Firewall Rules to Restrict Traffic

### Disaster Recovery

- What to do when some regional outage?

- Service Unavailability = Lost Business

- GCE - Snapshots for Individual Instances

- Failover Servers

- BackUp of DataBase

- BackUp of Mount Points

- Managed / RollBack App Services
  
  - GCE - Instance Group Rolling Update
  
  - GKE - Rolling Updates
  
  - GAE - Traffic Splitting/ Versions

## Cloud Migration Planning

### Five Phases of Successful Cloud Migration.

1. ### Assess

2. ### Pilot

3. ### Move Data

4. ### Move App

5. ### Optimize

### 1. Assess - What should we move?

- Easy to Move
  
  - Newer Stuff | Fewer Dependencies
  
  - No Licencing Requirement
  
  - Tolerant to Scaling
  
  - Expensive to Run on Premise

- Hard to Move
  
  - More Dependencies
  
  - Complex Licensing Requirements

- Can’t Move
  
  - Require Special or Older Hardware
  
  - Non Cloud Compliant Licensing(Like Oracle S/w)

### 2. Pilot - Baby Steps

- Proof of Concepts

- Non-Critical or Easily Duplicated Services

- Small Steps at First

- Considerations
  
  - Licensing
  
  - RollBack Plan
  
  - Change in Process

- Start Mapping Roles/ Structure
  
  - Projects
  
  - Separation of Duties
  
  - Test/Production Environments

### Choose correct service for successfull migration.

![alt text](https://github.com/sawan22071995/notes/blob/main/docs/Cloud/migrate.png?raw=true)

### 3. Move Data

- Move Data First Before Application

- Evaluate GCP Storage Options

- Evaluate Transfer Methods
  
  ![alt text](https://github.com/sawan22071995/notes/blob/main/docs/Cloud/data.png?raw=true)

### 4. Move Application

- Self Service or partner Assisted

- Use “Lift and Shift” approach
  
  - Create Duplicate Environment for On-Prem resource
  
  - Managed Services

- VM Import is freely available option from CloudEndure

- Enable Scaling using Auto Scalable Instance Groups

- Put Global Load Balancer on your VM instances

### 5. Future Optimization

- Consider Storage Options
  
  - Cloud Storage for Static Assets
  
  - Pub/Sub for loosely coupled tier communication
  
  - Datastore for High Speed SQL Traffic

- Consider Machine Optimization

- Consider moving to Container Services and Start Using GKE

- Start working and create DR Site

- Creation and Management of Regular Data Backups

### Storage Transfer Services

- GCP Web Console & gsutil, we are familiar

- Cloud Storage Transfer Service
  
  - Handle Different Type Scenarios
  
  - Import Online Data into Cloud Storage
    
    - AWS S3 Bucket
    
    - HTTP/HTTPS Locations
    
    - Another GC Storage Bucket
    
    - Import from above Data Source to Sink
      
      - Sink - Google Cloud Storage Bucket

- Cloud Storage Transfer is managed Service

### What Transfer Service Can Do?

- BackUp Data from other Storage Providers

- Move Data from one GCS to another

- Configured through Transfer Job:
  
  - One Time or Recurring Transfer
  
  - Delete Destination Objects if not present in Source
  
  - Delete Source Object after Transfer
  
  - Periodic Sync of Data Source and Sink
  
  - Source/Sink can be outside of projects.

### gsutil or Storage Transfer Service

- Cloud Storage provide(GCS, AWS, HTTP) - Use Storage Service

- On Premise Location - use gsutil

### Data Migration Best Practices

#### Best Transfer service options depends on multiple factors.

- How much data need to be transfer?

- How close that data from destination?

#### From Cloud → Very Close

- Storage Transfer Service

#### From On Prem Data Center → Close

- Fast Bandwidth

- Copy with gsutil

#### Slower Connection → Far

- Transfer Appliances

### How to Speed Up Data Transfer?

#### Decrease Data Size

- Compress Data

- Both Reduce Transfer time and Storage Cost

- Faster Transfer

#### Increase Network Bandwidth

- Public Internet Connection

- Cloud interconnect

#### gsutil copy command Consideration

- Limitations
  
  - No Network throttling
  
  - Best for One Time Transfer
  
  - For Ongoing, automate transfer or use Cron Job

#### Tools for Better and Faster Transfer

- Multi threaded process

- Parallel composite uploads. Split large files, transfer chunks in parallel and compose at destination

- Resumability, Resume transfer after an error

#### Multi Threaded Transfer Copy using gsutil

- Use -m Option
  
  ```
  gsutil -m cp -r [SOURCE] gs://[BUCKET_NAME] 
  ```

#### Parallel Uploads

- Break Single File into Chunks

- Don’t use for Nearline/Coldline Buckets - Extra Charge for ‘Modifying’ files on upload

- ```
  gsutil -o GSUtil:parallel_composite_uplaod_threashold=200M cp
  [SOURCE] gs://[BUCKET_NAME]
  ```

#### Far Option - Mail in it

- Transfer Appliance

- Load Up and Mail Your Data
  
  - Request Transfer Appliances
  
  - Load Data into Physical Appliance(Encrypted)
  
  - Ship to Google
  
  - Google will place data in cloud storage

### Disaster Recovery is important factor for Resilient Application.

### You always have a plan in case of any “Boom & Outage”

- Network Outage

- Application Upgrade Breaks Application

- Natural Disaster

- Accidental Data Deletion

- Well Planned DR Plan, to ensure in case outage, you recover in minimum possible time.

### Disaster Recovery Metrics RTO / RPO

- #### Recovery Time Objective (RTO)
  
  - Maximum Acceptable length of time that your application can be
    offline.

- #### Recovery Point Objective (RPO)
  
  - Maximum Acceptable Length of time during which data might be
    lost from your application due to the Major Incident.

### Questions to ask?

- After Disaster, How quickly your application and app data needs to
  be reverted in its previous state.

### The shorter your RTO/RPO the higher the cost

- Much Greater Complexity and Overhead required

- Time to recover reflected by SLAs

### Disaster Recovery Patterns

- Cold / Warm / Hot

- How quickly you can recover if something gone wrong

- In Range from Manual Configure DNS switchover to Backup site to ‘hot’
  duplicated environment.

- #### Warm Failover
  
  - Manual DNS Switchover to static site
  
  - Medium Cost, Medium recovery time

- #### Hot Failover
  
  - Multizone Instance Group, replicated Cloud SQL Instances
  
  - Higher cost, shorter recovery time

### Backup & Recovery Methods

#### BackUp of Individual GCE Instance

- Disk SnapShots

- Copy of Entire Disk

- Incremental
  
  - Only BackUp of What’s different from previous backup

#### Scheduling Snapshot

- CRON job on Instance

- Snapshot scheduler

#### Cloud Storage BackUp / Rollback

- Object Versioning + Lifecycle management

- Delete + Rollback protection

- Revert on Earlier Version

#### Distributed Computing Application Rollback

- Individual Instances are not backed up
  
  - No Snapshot

- Rollback to previous version
  
  - Compute Instance Managed Instance Group
    
    - Rolling Update - Apply previous Instance Group Template
    
    - Optional - Set target %, instead of 100
  
  - App Engine
    
    - Versioning/ Split Traffic

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
