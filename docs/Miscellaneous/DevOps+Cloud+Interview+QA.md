# DevOps, Cloud & Programming Interview Questions & Answers

## Table of Contents

- [Ansible](#ansible)
- [Docker](#docker)
- [Kubernetes (K8s)](#kubernetes-k8s)
- [Terraform](#terraform)
- [Git & Version Control](#git--version-control)
- [Jenkins & CI/CD](#jenkins--cicd)
- [AWS (Amazon Web Services)](#aws-amazon-web-services)
- [Azure](#azure)
- [GCP (Google Cloud Platform)](#gcp-google-cloud-platform)
- [Networking](#networking)
- [Python Programming](#python-programming)
- [Shell Scripting](#shell-scripting)
- [DevOps Best Practices](#devops-best-practices)
- [Security & Compliance](#security--compliance)
- [HashiCorp Nomad](#hashicorp-nomad)
- [Additional Resources](#additional-resources)

---

## Ansible

### Configuration Management & Automation

##### Q. How would you ensure that a specific package is installed on multiple servers?
You can use the package module in a playbook to ensure that a specific package is installed across multiple servers.

##### Q. How do you handle different environments (development, testing, production) with Ansible?
You can manage different environments by using inventory files and group variables. Create separate inventory files for each environment and use group variables to specify environment-specific configurations. Each hosts file would define the servers for that specific environment, and you can create a group_vars directory for each environment.

##### Q. How would you restart a service after updating a configuration file?
You can use the notify feature in Ansible to restart a service after a configuration file is updated.

##### Q. How can you ensure idempotency in your Ansible playbook?
Ansible modules are designed to be idempotent, meaning they can be run multiple times without changing the result beyond the initial application. For instance, if you use the file module to create a file, Ansible will check if the file already exists before trying to create it.

##### Q. How do you handle secrets or sensitive data in Ansible?
You can handle sensitive data using Ansible Vault, which allows you to encrypt files or variables.

##### Q. Can you explain how you would deploy an application using Ansible?
**Define Inventory:** Create an inventory file with the target hosts.
**Create a Playbook:** Write a playbook that includes tasks for pulling the application code from a repository, installing dependencies, configuring files, and starting services.

##### Q. How would you handle task failures and retries in Ansible?
You can use the retry and when directives to handle task failures in Ansible. The retries and delay parameters can be specified for tasks that might need to be retried.

##### Q. How would you roll back a deployment if the new version fails?
To roll back a deployment, you can maintain a previous version of the application and use a playbook that checks the health of the new version before deciding to switch back.

##### Q. How can you manage firewall rules across multiple servers using Ansible?
You can use the firewalld or iptables modules to manage firewall rules.

##### Q. How do you implement a continuous deployment pipeline using Ansible?
To implement a continuous deployment pipeline, you can integrate Ansible with a CI/CD tool like Jenkins, GitLab CI, or GitHub Actions.

##### Q. How can you check if a file exists and create it if it doesn't?
You can use the stat module to check if a file exists and then use the copy or template module to create it if it doesn't.

##### Q. How can you execute a command on remote hosts and capture its output?
You can use the command or shell module to run commands on remote hosts and register the output.

##### Q. What is Ansible ad-hoc command?
Command used in Ansible without playbook is called ad-hoc command.

---

## Docker

### Containerization & Container Management

##### Q. How would you free up disk space on a Docker host?
- Remove unused containers with: `docker container prune`
- Remove unused images (dangling and unreferenced): `docker image prune -a`
- Remove unused volumes: `docker volume prune`
- Clean up unused networks: `docker network prune`
- Reclaim space from all unused objects: `docker system prune -a`

##### Q. How would you troubleshoot and debug a running Docker container?
- Access the container's shell using: `docker exec -it <container_name> /bin/bash`
- Check container logs using: `docker logs <container_name>`
- Inspect the container's state with: `docker inspect <container_name>`

##### Q. How would you troubleshoot and resolve network connectivity issues between Docker containers?
- Verify network configuration using: `docker network inspect <network_name>`
- Check connectivity between containers using: `docker exec -it <container_name> ping <other_container_ip_or_name>`
- If DNS resolution is failing, ensure you are using the correct container names, as Docker provides built-in DNS resolution for containers on the same network.

##### Q. How would you investigate and resolve a container that continuously restarts?
- Examine the logs using: `docker logs <container_name>`
- Use the docker inspect command to check the container's restart policy: `docker inspect <container_name> | grep RestartPolicy`
- Adjust the policy to avoid endless restarts: `docker run --restart=on-failure:3 <container_image>`

##### Q. What steps would you take to secure a Docker container?
- Avoid running applications as root inside the container. In the Dockerfile, create a non-root user:
  ```dockerfile
  RUN useradd -ms /bin/bash myuser
  USER myuser
  ```
- Enable user namespaces to map container users to different users on the host
- Only expose necessary ports and limit external access with firewall rules
- Use Docker's bridge network mode for isolation

##### Q. How would you roll back to a previous Docker image version?
- If tagged properly: `docker run -d my_image:previous_version`
- If the old image is present: `docker images` then `docker run -d <image_id>`

##### Q. How would you force stop a Docker container that refuses to stop?
- Attempt graceful stop: `docker stop <container_name>`
- Forcibly kill it: `docker kill <container_name>`
- Investigate using `docker inspect` to check for resource constraints or system issues

##### Q. What is a Docker registry and why do we need it?
A Docker registry is a storage and distribution system for Docker images. It allows users to store, manage, and distribute Docker container images.

**Key Points:**
- **Storage:** Stores Docker images and their versions in a central location
- **Distribution:** Facilitates sharing and deploying images across different environments and teams
- **Security:** Manages access controls and authentication
- **Versioning:** Keeps track of different versions of images

**Why We Need It:**
- Centralized management
- Consistency across environments
- Efficient deployment
- Team collaboration

##### Q. What is the difference between COPY and ADD command in Dockerfile?

**1. Functionality:**
- **COPY:** Straightforward file transfer without extraction or processing
- **ADD:** Can use URLs or extract compressed archives directly into the image

**2. Caching:**
- **COPY:** Cacheable, leading to faster builds when source files haven't changed
- **ADD:** Not cacheable in the same way due to complex operations

**3. URLs and Archives:**
- **COPY:** Only for local files and directories
- **ADD:** Supports URLs and automatic extraction of compressed archives

**Best Practices:** Use COPY when only copying local files, use ADD when specifically requiring URL downloads or archive extraction.

##### Q. Explain the typical lifecycle of a Docker container

1. Pull or create a Docker image
2. Create a container from the image
3. Run the container
4. Stop the container
5. Restart the container
6. Kill the container (if needed)
7. Prune or reclaim the resources

##### Q. What are the two ways to download Docker images?
- **Explicit:** Using `docker pull` command
- **Implicit:** When executing `docker run`, Docker daemon searches locally and downloads if not found

##### Q. How to transfer Docker images between machines without internet?
```bash
docker save -o images.tar image1 image2 image3
docker load -i images.tar
```

##### Q. How to import and export Docker containers?
```bash
docker export -o container.tar container_name
docker import container.tar
```

##### Q. How to check steps executed in Docker images?
```bash
docker image history acme/my-final-image:1.0
```

##### Q. How many types of Docker volumes?

1. **Host volumes:** Direct access to host file system
   ```bash
   docker run -v /path/on/host:/path/in/container
   ```

2. **Anonymous volumes:** Managed by Docker, automatically deleted with container
   ```bash
   docker run -v /path/in/container
   ```

3. **Named volumes:** Easier to manage and share between containers
   ```bash
   docker volume create somevolumename
   docker run -v somevolumefileName:/path/in/container
   ```

##### Q. Difference between --mount vs --volume in Docker?
- **--volume (-v):** Three colon-separated fields, order-dependent
  ```bash
  --volume $(pwd):/backup/user:rw
  ```
- **--mount:** Key-value pairs, more verbose but clearer
  ```bash
  --mount 'type=volume,src=<VOLUME-NAME>,dst=<CONTAINER-PATH>'
  ```

##### Q. How many types of Docker network?

1. **Bridge networks:** Default, used within a single host
2. **Overlay networks:** For multi-host communication
3. **Macvlan networks:** Connect containers directly to host network interfaces

##### Q. What is the default Docker network?
**Bridge** is the default network driver for standalone containers that need to communicate.

##### Q. What does "docker inspect" command do?
```bash
docker inspect --format '{{ .NetworkSettings.IPAddress }}' container_id
```
This extracts the exact private IP address of the container.

##### Q. Can you override the ENTRYPOINT at runtime?
Yes, using `--entrypoint` flag.

##### Q. What are the two types of registries in Docker?
1. **Public Registry:** Docker Hub for public images
2. **Private Registry:** For in-premise or private use

##### Q. How do Docker client and Docker Daemon communicate?
Through a mix of RESTful API, socket I/O, and TCP.

##### Q. Can we add multiple machines in Docker Swarm without installing Docker Swarm on each machine?
No, Docker Swarm must be installed on each machine.

##### Q. Difference between "docker create" and "docker run"?
- **docker create:** Creates container but doesn't start it
- **docker run:** Creates and starts the container

##### Q. What is "null" network driver?
Activated with `docker run --net none`. The container gets no IP address and has no external network access. Used for local batch jobs.

##### Q. How to ensure container execution order in Docker Compose?
Use the `depends_on` condition:
```yaml
version: "2.4"
services:
  backend:
    build: .
    depends_on:
      - db
  db:
    image: postgres
```

##### Q. Who owns the Docker control socket?
Docker control socket is owned by the docker group.

##### Q. Can an ARG variable be used by the running container?
No, ARG variables are exclusively for Dockerfile use.

##### Q. How to see container logs in real-time?
```bash
docker logs --follow <container_id>
```

##### Q. Can a normal user read files mounted by Docker container with root user?
No.

---

## Kubernetes (K8s)

### Container Orchestration & Management

### Troubleshooting & Operations

##### Q. How do I check the status of my Kubernetes cluster?
- Use `kubectl cluster-info` for summary
- Use `kubectl get nodes` for node status
- Use `kubectl get componentstatuses` for overall health

##### Q. What should I do if a pod is stuck in Pending state?
Check pod description: `kubectl describe pod <pod-name>` to see events and reasons for not being scheduled. Review node resources, quotas, and affinity rules.

##### Q. How to troubleshoot a pod stuck in CrashLoopBackOff state?
- View logs: `kubectl logs <pod-name>`
- Describe pod: `kubectl describe pod <pod-name>`
- Check container state and events

##### Q. How to investigate if a service is not exposing pods correctly?
- List services: `kubectl get svc`
- Describe service: `kubectl describe svc <service-name>`
- Check selectors match pod labels
- Verify endpoints: `kubectl get endpoints <service-name>`

##### Q. Steps if deployment is not rolling out as expected?
- Check status: `kubectl rollout status deployment/<deployment-name>`
- Describe deployment: `kubectl describe deployment/<deployment-name>`
- Review pod logs and events
- Check rollout history: `kubectl rollout history deployment/<deployment-name>`

##### Q. How to resolve issues with Kubernetes network policies?
- List policies: `kubectl get networkpolicies`
- Describe policy: `kubectl describe networkpolicy <policy-name>`
- Ensure policies allow necessary traffic between pods

##### Q. How to debug a node not accepting new pods?
- Check node status: `kubectl get nodes` and `kubectl describe node <node-name>`
- Look for resource pressure (memory/CPU)
- Review kubelet logs on the node

##### Q. What if kubectl commands fail with connectivity issues?
- Verify kubeconfig file is correctly configured
- Check API server status and logs
- Verify network connectivity to API server
- Use `kubectl cluster-info` to check for errors

##### Q. Why is my pod experiencing high CPU or memory usage?
- Check usage: `kubectl top pod <pod-name>`
- Review resource requests and limits in YAML
- Examine application logs for inefficiencies or bugs

##### Q. What if a Kubernetes job fails to complete?
- Check job status: `kubectl describe job <job-name>`
- View logs: `kubectl logs <pod-name>`
- Verify job specifications (backoff limit, parallelism, completions)

##### Q. How to address deployment rollback issues?
- Check history: `kubectl rollout history deployment/<deployment-name>`
- Monitor status: `kubectl rollout status deployment/<deployment-name>`
- Ensure previous revision is correct

##### Q. How to resolve Kubernetes ingress controller issues?
- Check controller pods: `kubectl get pods -n <ingress-namespace>`
- View logs: `kubectl logs <ingress-controller-pod>`
- Verify ingress resources: `kubectl describe ingress <ingress-name>`
- Ensure proper configuration and permissions

##### Q. Steps if Kubernetes API server is unresponsive?
Check control plane components' status and logs. For managed services, check provider's status dashboard.

##### Q. How to troubleshoot ConfigMaps and Secrets issues?
- Check existence: `kubectl get configmap <name>` and `kubectl get secret <name>`
- Verify they are correctly defined and mounted
- Describe resources for details

### Core Concepts & Architecture

##### Q. What is Kubernetes and why is it important?
Kubernetes is an open-source platform for automating deployment, scaling, and management of containerized applications. It acts as a traffic controller for containerized applications, ensuring efficiency and reliability. It provides:
- Easier deployment across environments
- Consistent platform for applications
- Efficiency, scalability, and flexibility
- Cost savings and faster time-to-market

##### Q. How does Kubernetes handle network communication between containers?
Kubernetes uses the Container Network Interface (CNI). Network plugins allocate IP addresses to pods and enable communication within the cluster. Each container in a pod gets a unique IP within the pod's network namespace, allowing localhost communication. A virtual network overlay enables inter-pod communication across nodes.

##### Q. How does Kubernetes handle scaling of applications?
- **Horizontal scaling (scaling out):** Adding more instances via ReplicaSet
- **Vertical scaling (scaling up):** Increasing resources via Horizontal Pod Autoscaler (HPA)
- HPA automatically adjusts replicas based on CPU/memory utilization

##### Q. What is a Kubernetes Deployment and how does it differ from a ReplicaSet?
- **Deployment:** Higher-level object managing desired state of pods, providing declarative updates, rolling updates, and rollbacks
- **ReplicaSet:** Lower-level object managing scaling and lifecycle of pods
- Deployment manages ReplicaSets, which in turn manage Pods

##### Q. Explain rolling updates in Kubernetes
Rolling updates gradually replace old pods with new ones:
1. Create new version of deployment/replica set
2. Gradually replace old pods one at a time
3. Both old and new pods run simultaneously
4. Delete old pods once all new pods are running
This ensures zero downtime during updates with rollback capability.

##### Q. How does Kubernetes handle network security and access control?
- **Network policies:** Define traffic flow rules within cluster
- **RBAC:** Granular permissions based on roles
- **CNI:** Plugin-based interface for network integration
- Service meshes for additional security layers

##### Q. Example of deploying a highly available application?
1. Create multi-node cluster across availability zones
2. Create Deployment specifying replica count
3. Create Service with stable IP/DNS
4. Use Ingress for load-balancing traffic across replicas
Kubernetes monitors and maintains specified replicas even if nodes fail.

##### Q. What is namespace in Kubernetes? Which namespace if not specified?
Namespaces are virtual clusters within Kubernetes providing logical isolation. Default namespace is used if not specified.

**Default namespaces:**
- `default`
- `kube-system`
- `kube-public`
- `kube-node-lease`

##### Q. How does Ingress help in Kubernetes?
Ingress provides Layer 7 load balancing for HTTP/HTTPS traffic:
- Load balancing across services
- URL/hostname-based routing
- Access control by IP/headers
- TLS termination

##### Q. Different types of services in Kubernetes?
1. **ClusterIP (default):** Internal cluster IP
2. **NodePort:** Exposes service on each node's port
3. **LoadBalancer:** Cloud load balancer for external access
4. **ExternalName:** Maps service to external DNS name

##### Q. Explain self-healing in Kubernetes
Self-healing automatically recovers from failures:
- Monitors container health via health checks
- Terminates failed containers
- Creates replacement containers
- Maintains desired replica count
- Supports rolling updates without downtime

##### Q. How does Kubernetes handle storage management?
- **Volumes:** Directories accessible to containers in pods
- **Persistent Volumes (PVs):** Storage resources provisioned by admin
- **Storage Classes:** Define types of dynamically provisioned storage
- Supports various volume types: emptyDir, hostPath, configMap, secret, etc.

##### Q. How does NodePort service work?
1. Create NodePort service in manifest
2. Kubernetes assigns random port (30000-32767)
3. Maps NodePort to container's target port
4. Access via any node's IP + NodePort
5. Node routes traffic to correct pod

##### Q. Difference between multinode and single-node cluster?
- **Single-node:** All applications on one node (testing/development only)
- **Multi-node:** Multiple nodes for workload distribution and high availability

##### Q. Difference between "create" and "apply" in Kubernetes?
- **create:** Creates new resource, errors if exists
- **apply:** Creates or updates existing resource

##### Q. What is Kubernetes architecture?
**Master Node (Control Plane):**
- API Server: Central management point
- Scheduler: Places containers on nodes
- Controller Manager: Manages controllers
- etcd: Distributed key-value store

**Worker Nodes:**
- Kubelet: Node agent
- Kube Proxy: Network routing
- Container Runtime: Runs containers
- Pods: Smallest deployable units
- Services: Stable network endpoints
- Ingress: External access management

##### Q. What are taints and tolerations?
- **Taints:** Allow nodes to repel pods
- **Tolerations:** Allow pods to schedule on tainted nodes
Work together to control pod placement on nodes.

##### Q. Ways to assign pod to specific node?
- nodeSelector by label
- nodeName
- nodeAffinity
- podAffinity

##### Q. How to stop pod scheduling to specific node?
By tainting the node.

##### Q. How to manage high availability of pods?
ReplicaSet automatically creates new pods to maintain HA.

##### Q. What is availability zone in Azure?
Physically and logically separated datacenters with independent power, network, and cooling, connected via low-latency network.

##### Q. What is availability set in Azure?
- Configures multiple VM copies isolated across different physical infrastructure
- 2 Fault Domains and 5 Update Domains (ASM)
- 3 Fault Domains and 5-20 Update Domains (ARM)

##### Q. Default directory when docker exec into container?
- `/` (root directory)
- `/workdir` (if defined in Dockerfile)

##### Q. Docker exec with specific user?
```bash
docker exec -it --user sawan <container_name> /bin/bash
```

##### Q. Docker exec with specific directory?
```bash
docker exec -w /path/to/directory <container_name> /bin/bash
```

##### Q. Workflow for "kubectl get pod" command?
```
kubectl → kubeconfig → kubeApiServer → ETCD
```

##### Q. Communication between Docker containers?
Docker creates a virtual network called "bridge" by default and connects containers to it.

##### Q. How to find IP of Docker container?
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id
```

##### Q. Difference between ReplicaSet and DaemonSet?
- **ReplicaSet:** For apps decoupled from nodes, can run multiple copies per node
- **DaemonSet:** Runs single copy on all/subset of nodes (e.g., monitoring, logging)

##### Q. YAML manifest sections in Kubernetes?
1. **apiVersion:** Group_Name/VERSION
2. **Kind:** Resource type (Pod, Deployment, Service, etc.)
3. **Metadata:** Resource metadata
4. **Spec:** Resource specifications

##### Q. Types of VMs in Azure?
- General purpose
- Compute optimized
- Memory optimized
- Storage optimized
- GPU
- High performance compute

##### Q. Secure way to store secrets in Azure?
Azure Key Vault

##### Q. What is sidecar container in AKS?
A container that runs alongside the main container in a pod, sharing volume and network, enhancing application functionality. Independent of programming language, uses same resources as main container.

##### Q. Create Azure Front Door with WAF policy?
1. Create Azure Front Door
2. Create WAF policy with custom rules (e.g., geo-location blocking)
3. Associate WAF policy with Front Door
4. Verify in Front Door WAF section

##### Q. Difference between Traffic Manager and Front Door?
**Traffic Manager:**
- DNS layer (any protocol)
- On-premises routing support
- Regional

**Front Door:**
- HTTP(S) proxy at Microsoft Edge
- Better latency/throughput
- Independent scalability
- Global

##### Q. How to know who committed code with author in file?
```bash
git blame <filename>
```

##### Q. How to upgrade/renew SSL certificate in Azure Application Gateway?
1. Navigate to Application Gateway listeners
2. Select listener with certificate to renew
3. Select "Renew or edit selected certificate"
4. Upload new PFX certificate, name it, enter password
5. Save

##### Q. Types of Subnets?
- **Public:** Direct internet access via Public IP
- **Private:** Internet access via NAT Gateway

##### Q. Difference between default NACL and user-created NACL?
- **Default NACL:** All traffic allowed
- **User-created NACL:** All traffic denied

##### Q. Communicate between instances in different VPCs?
VPC Peering (only if IP ranges don't overlap)

##### Q. How to access all VPCs for communication?
Transit Gateway

##### Q. Access private EC2 with S3 bucket?
VPC Endpoint

##### Q. Which endpoint is cheaper: Gateway or Interface?
Gateway Service Type VPC Endpoint is cheaper.

##### Q. Monitoring effectiveness of scaling in Kubernetes?
Use Prometheus and Grafana to track:
- CPU utilization
- Memory usage
- Pod deployment
- Response times

##### Q. Role of Kubernetes API server in scaling?
Receives scaling requests, validates them, and orchestrates cluster size adjustments.

##### Q. Ensure high availability when scaling?
- Distribute workload across nodes
- Implement redundancy
- Use rolling updates
- Configure load balancers

##### Q. Optimize resource utilization strategies?
- Rightsize pods
- Implement pod affinity/anti-affinity
- Use resource quotas and limits
- Leverage advanced scheduling (pod disruption budgets)

##### Q. Prevent over/under-provisioning?
- Monitor resource usage regularly
- Set appropriate scaling thresholds
- Perform capacity planning
- Use autoscaling mechanisms

##### Q. How does Kubernetes scheduler handle pod placement?
Based on:
- Resource availability
- Affinity/anti-affinity rules
- Node taints
- Pod priority/class

##### Q. Scaling across multiple cloud providers/regions?
Consider:
- Network latency
- Data locality
- Cross-cloud traffic costs
- Data synchronization
- Cloud-specific service compatibility

##### Q. Rollback scaling changes?
Use revision history and deployment rollbacks to revert to previous stable state.

##### Q. Handle application dependencies in microservices?
- Decouple services
- Use service discovery (Kubernetes Services)
- Implement health checks
- Ensure proper inter-service communication

##### Q. Difference between Deployment and StatefulSet?
- **Deployment:** For stateless applications
- **StatefulSet:** For stateful applications requiring:
  - Persistent state information
  - Stable network IDs
  - Ordered deployment
  - Persistent storage

##### Q. What is DaemonSet?
Ensures specific pod runs on all/subset of nodes. Used for system-level services like:
- Cluster storage daemons
- Log collection daemons
- Node monitoring daemons

##### Q. What is PDB (Pod Disruption Budget)?
Ensures minimum number of pods run for an application during voluntary disruptions (e.g., node draining for maintenance/upgrades).

##### Q. Difference between PDB and Replica?
- **PDB:** Ensures minimum availability during disruptions
- **ReplicaSet:** Only ensures specified replicas are created

PDB provides additional availability guarantees over ReplicaSet alone.

##### Q. Schedule pod on tainted node?
Use tolerations matching the node's taint.

##### Q. Autoscaling types in cloud services?
- **Horizontal scaling (scaling out):** Adding more machines
- **Vertical scaling (scaling up):** Adding more power (CPU/RAM) to existing machines

##### Q. Kubernates solution for PVC autogrow?

**Method - 1: StorageClass with allowVolumeExpansion**
```yaml
allowVolumeExpansion: true
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
  name: gp2
parameters:
  fsType: ext4
  type: gp2
provisioner: kubernetes.io/aws-ebs
reclaimPolicy: Delete
volumeBindingMode: Immediate
```
Edit PVC, resize it, and recreate application/StatefulSet.

**Method - II: Using Autopilot**
Create AutopilotRule with:
- PVC Selector
- Namespace Selector
- Metric conditions
- PVC resize action

Example rule monitors volume usage and automatically resizes when threshold met.

##### Q. How to control communication between pods?
Use Network Policies:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: simple-policy
spec:
  podSelector:
    matchLabels:
      app: target-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: allowed-pod
    ports:
    - protocol: TCP
      port: 6379
```

##### Q. What is Ingress controller?
Software providing reverse proxy, traffic routing, and TLS termination for Kubernetes services. Configured via Ingress resources.

##### Q. What is trigger in Azure DevOps?
Specifies events that cause tasks to execute, such as:
- Code push to branches
- Continuous integration builds
- Continuous deployment after builds

##### Q. Difference between StatefulSet and Deployment?
- **Deployment:** For stateless applications (no persistent storage dependency)
- **StatefulSet:** For stateful applications (requires persistent storage, unique network IDs)

##### Q. Kubernetes components?

**Master Node (Control Plane):**
1. **API Server (port 6443):** Component communication hub, handles CRUD operations
2. **ETCD (port 2379):** Key-value database storing cluster configuration
3. **Controller Manager (port 10252):** Manages node, replication, endpoint, token controllers
4. **Scheduler (port 10251):** Assigns pods to appropriate worker nodes

**Worker Node:**
1. **Kubelet (port 10250):** Node agent communicating with API server
2. **Kube-Proxy (ports 30000-32767):** Network agent for routing and load balancing
3. **CRI:** Container Runtime Interface (Docker, containerd, etc.)

##### Q. Kubernetes deployment types?

1. **Recreate:** All-or-nothing update with downtime
2. **Rolling:** Gradual update in batches
3. **Blue/Green:** Switch between two identical environments
4. **Canary:** Progressive delivery to subset of users
5. **Shadow:** Test new version with production traffic copy

##### Q. Print line containing "sawan" in file.txt?
```bash
grep -n "sawan" file.txt
```

##### Q. Upgrade Kubernetes cluster with zero downtime?
1. Upgrade kubeadm on first node
2. Verify and apply upgrade plan
3. Update kubelet and restart service
4. Upgrade other master nodes
5. Upgrade kubectl on all masters
6. For each worker: upgrade kubeadm, drain node, upgrade config/kubelet, restore node

Or use Node Pools migration:
1. Create new node pools with new version
2. Cordon old nodes
3. Drain old nodes
4. Delete old nodes after migration

##### Q. Upgrade AKS with zero downtime?

**Pre-Upgrade Planning:**
1. Identify standalone pods
2. Setup Pod Disruption Budget
3. Customize node surge upgrade

**Process:**
1. Get current/latest versions
2. Update node pool surge setting
3. Perform cluster upgrade
4. Monitor events

Control plane upgrade doesn't impact applications.

---

## Terraform

### Infrastructure as Code

##### Q. What is Terraform?
Terraform is an infrastructure as code tool that lets you define cloud and on-premises resources in configuration files.

##### Q. Differentiate between Terraform and CloudFormation?

**Declarative vs. Imperative:**
- **Terraform:** Declarative (specify desired state)
- **CloudFormation:** Imperative (specify sequence of steps)

**Configuration Language:**
- **Terraform:** HCL (HashiCorp Configuration Language)
- **CloudFormation:** JSON or YAML

**State Management:**
- **Terraform:** Uses state file (terraform.tfstate)
- **CloudFormation:** Manages state internally

##### Q. How to prevent "Duplicate Resource" error?

1. Use unique resource names
2. Utilize variables for reusability
3. Leverage data sources for existing resources
4. Review dependencies with `depends_on`
5. Check for resource existence before creation
6. Review state files
7. Run `terraform plan` before applying

##### Q. Are callbacks possible with Terraform on Azure?
Yes, using:
- Azure Functions or Logic Apps
- Azure Event Grid for event handling

##### Q. What is tainted resource?
A resource marked for recreation during next apply due to configuration changes that can't be applied in place.
```bash
terraform taint resource_type.resource_name
```

##### Q. What is Remote Backend?
Central location for storing Terraform state file enabling:
- Team collaboration
- State locking
- Consistent state across users

**Types:**
- Amazon S3
- Azure Storage
- Google Cloud Storage
- HashiCorp Consul
- HTTP

##### Q. What is Terragrunt?
Thin wrapper for Terraform providing:
- DRY configurations
- Remote state management
- Encrypted variables
- Workspace/environment management
- Dependency management
- Dynamic configuration
- Concurrent operations

##### Q. What is state file locking?
Prevents concurrent access/modifications to state file. Two types:
- **File-Based:** Uses lock file
- **Backend-Based:** Managed by backend (S3+DynamoDB, etc.)

##### Q. Making module objects available across modules?

1. Define output variables in source module
2. Reference outputs in parent module using `module.source_module.output_name`
3. Run terraform init/apply
4. Handle dependencies correctly

##### Q. What are provisioners?
Built-in configurations for running scripts during resource creation/destruction:

1. **Local-Exec:** Run commands on Terraform machine
2. **Remote-Exec:** Run commands on remote resource
3. **File:** Copy files to remote resource
4. **Connection:** Define SSH/WinRM connections
5. **Chef/Puppet:** Configuration management integration

##### Q. Terraform request flow architecture?

1. Configuration Files (HCL)
2. Terraform CLI commands
3. Provider Plugins
4. Provider Configurations
5. Initialization (terraform init)
6. Resource Graph building
7. Plan Generation (terraform plan)
8. Execution (terraform apply)
9. State Management
10. Concurrency/Parallelism
11. Output and Feedback
12. Post-Apply Tasks

##### Q. Terraform lifecycle arguments?

**Prevent resource deletion:**
```hcl
lifecycle {
  prevent_destroy = true
}
```

**Create before destroy:**
```hcl
lifecycle {
  create_before_destroy = true
}
```

**Ignore changes:**
```hcl
lifecycle {
  ignore_changes = [tags]
}
```

**Custom condition checks:**
```hcl
lifecycle {
  precondition {
    condition = data.aws_ami.example.architecture == "x86_64"
    error_message = "AMI must be x86_64."
  }
}
```

##### Q. Import existing resources to Terraform?
```bash
# Import AWS instance
terraform import aws_instance.foo i-abcd1234

# Import into module
terraform import module.foo.aws_instance.bar i-abcd1234
```

##### Q. What is Terraform state file?
Stores information about infrastructure, tracking resources and mapping them to real-world resources.

##### Q. Where can Terraform state file be stored?
- Local machine (default: terraform.tfstate)
- Remote storage (Azure Storage Account, AWS S3)
- Terraform Cloud

##### Q. Delete and apply specific resource?
```bash
terraform destroy -target=resource_type.resource_name
terraform apply -target=resource_type.resource_name
```

##### Q. What is dynamic block?
Construct repeatable nested blocks dynamically:
```hcl
locals {
  ports = [22, 80, 8080, 8081]
}

dynamic "security_rule" {
  for_each = local.ports
  content {
    name = "Inbound-rule-${security_rule.key}"
    priority = sum([100, security_rule.key])
    source_port_range = security_rule.value
  }
}
```

##### Q. Authenticate Terraform with Azure?
Via Service Principal:
```hcl
provider "azurerm" {
  features {}
  subscription_id = "00000000-0000-0000-0000-000000000000"
  client_id = "00000000-0000-0000-0000-000000000000"
  client_certificate_path = var.client_certificate_path
  tenant_id = "00000000-0000-0000-0000-000000000000"
}
```

Or environment variables:
```bash
export ARM_CLIENT_ID="00000000-0000-0000-0000-000000000000"
export ARM_SUBSCRIPTION_ID="00000000-0000-0000-0000-000000000000"
export ARM_TENANT_ID="00000000-0000-0000-0000-000000000000"
```

---

## Git & Version Control

### Source Control & Collaboration

##### Q. Difference between rebase and merge?

**Merge:**
- Combines histories of two branches
- Creates merge commit with two parents
- Preserves complete history
- Can lead to cluttered history
- **Use when:** Preserving exact history, collaborative environment

**Rebase:**
- Reapplies commits from one branch onto another
- Creates linear history
- Rewrites commit history
- **Use when:** Clean linear history desired, working on local branches

##### Q. Resolve complex merge conflicts across multiple files?

1. **Understand the Conflict:**
   - Review conflicted files
   - Assess context from commits

2. **Communicate with Team:**
   - Discuss with team members
   - Coordinate resolution efforts

3. **Manual Conflict Resolution:**
   - Edit files to resolve conflicts
   - Remove conflict markers
   - Test changes

4. **Use Merge Tool:**
   - Tools like KDiff3, Beyond Compare, VS Code
   - `git mergetool` command

##### Q. Git "Detached HEAD" state?

Occurs when checking out a commit directly instead of a branch.

**Recovery:**
1. **Create new branch:** `git checkout -b my-new-branch`
2. **Stash changes:** `git stash` then switch branch
3. **Checkout branch:** `git checkout main`
4. **Discard changes:** Switch to branch (discards changes)

##### Q. What are Git submodules?
Embedded Git repositories within parent repository. Used for:
- Third-party libraries
- Shared code across projects
- Modular projects

**Commands:**
```bash
# Add submodule
git submodule add <repository-url> [path]

# Clone with submodules
git clone <repository-url>
git submodule update --init --recursive

# Update submodules
git submodule update --remote

# Remove submodule
git submodule deinit <submodule-path>
rm -rf <submodule-path>
git rm --cached <submodule-path>
```

##### Q. Handle large binary files in Git?

**Git Large File Storage (LFS):**
```bash
git lfs install
git lfs track "*.psd"
git add .gitattributes
git add path/to/largefile
git commit -m "Add large file with LFS"
```

**Alternatives:**
- Git-Annex
- External Storage (cloud/file hosting)
- Submodules/Subtrees
- Archiving for static files

##### Q. Git internal storage mechanism impact on performance?

**Objects:**
- Blobs: Store file content
- Trees: Represent directory structures
- Commits: Snapshots with metadata

**Performance factors:**
- Repository size
- Disk I/O and memory usage
- Indexing and caching
- Repository history complexity

**Optimization strategies:**
- Use Git LFS for large files
- Regular maintenance (git gc, git repack)
- Optimize history (rebase vs merge)
- Split large repositories

##### Q. Using git reflog for recovery?

**Scenario:** Accidentally dropped commit during rebase

**Steps:**
```bash
# View reflog
git reflog

# Find commit hash
# Create new branch from it
git checkout -b recovered-branch <commit-hash>

# Or reset current branch
git reset --hard <commit-hash>
```

Reflog tracks all HEAD changes, allowing recovery of lost commits.

##### Q. Git bisect to find bug-introducing commit?

**Steps:**
```bash
# Start bisect
git bisect start

# Mark current (bad) commit
git bisect bad

# Mark known good commit
git bisect good <good-commit>

# Git checks out middle commit
# Test and mark
git bisect bad  # or
git bisect good

# Repeat until culprit found

# End bisect
git bisect reset
```

Binary search through commits to identify bug introduction.

##### Q. Difference between git reset variations?

```bash
# Keep work, remove from staging
git reset --soft HEAD~1

# Destroy work
git reset --hard HEAD~1

# Remove file from staging
git reset
```

##### Q. Git branching strategies?
**Gitflow:**
```
Main ← Hotfix ← Release ← Development ← Features
```

**Flow:**
1. Develop branch from main
2. Feature branches from develop
3. Release branch from develop
4. Merge release to develop and main
5. Hotfix from main, merge to develop and main

##### Q. Cherry-pick commit across branches?
```bash
# Clone repository
git clone "https://github.com/user/repo.git" -b master

# Check commit ID
git log

# Switch to target branch
git checkout release-1.0.0

# Cherry-pick commit
git cherry-pick <commit-id>

# Add, commit, push
git add .
git commit -m "message"
git push
```

---

## Jenkins & CI/CD

### Continuous Integration & Deployment

##### Q. What is Jenkins?
Open-source CI/CD server written in Java for automating build cycles. Can be self-hosted, triggered via CLI or web interface.

**Benefits:**
- Open-source with large community
- Many available plugins
- Java-based (portable)
- Automated integration reduces manual work
- Faster development
- Early issue detection
- Higher quality software

##### Q. What are Jenkins plugins?
Primary means of enhancing Jenkins functionality to suit organization/user-specific needs.

##### Q. Connect Jenkins with Azure cloud without user credentials?
Using System Managed Identity (exists as long as resource exists).

##### Q. What is CI/CD?

**Continuous Integration (CI):**
- Automatic code integration from multiple developers
- Automated testing
- Multiple merges per day/commit
- Uses CI tools

**Continuous Delivery (CD):**
- Automated building and packaging
- Ready for deployment (one-click release)
- Minimal human intervention

**Continuous Deployment:**
- Automatic deployment to production
- Full automation from commit to production

##### Q. What is GitLab Runner?
Application that works with GitLab CI/CD to run jobs in a pipeline.

##### Q. Store environment variables for Jenkins pipeline?

**1. Pipeline Environment Blocks:**
```groovy
pipeline {
    agent any
    environment {
        MY_VARIABLE = 'my_value'
    }
    stages {
        stage('Build') {
            steps {
                echo "My variable: ${MY_VARIABLE}"
            }
        }
    }
}
```

**2. Global Environment Variables:**
Manage Jenkins > Configure System > Global properties

**3. Credentials Plugin:**
```groovy
withCredentials([string(credentialsId: 'my-secret-credential', variable: 'SECRET_KEY')]) {
    // Access SECRET_KEY in this block
}
```

##### Q. Troubleshoot failing pipelines automatically?

1. **Monitoring and Alerting:**
   - Prometheus, Grafana, New Relic, Datadog
   - Track pipeline health and performance

2. **Logging and Tracing:**
   - ELK Stack, Fluentd, Splunk
   - Centralized log storage
   - Automated log analysis

3. **Automatic Remediation:**
   - Automation scripts for known issues
   - Auto-restart for crashes

4. **Clear Success/Failure Criteria:**
   - Define alerts for various stages
   - Set up notifications

---

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
  --body '{"properties": {"enabled": true, "sendEmailsToSubscriptionOwners": true, "customEmails": ["oncall@company.com"]}}'
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
  --name company-feature-store \
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
    workspace_name="company-feature-store"
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
    feature_store_name="company-feature-store"
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
        "emails": ["ml-team@company.com"]
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
CREATE DATABASE [Tenant_CompanyA]
WITH (SERVICE_OBJECTIVE = 'DW100c');

CREATE DATABASE [Tenant_CompanyB]
WITH (SERVICE_OBJECTIVE = 'DW100c');

-- Tenant-specific schemas
USE [Tenant_CompanyA];

CREATE SCHEMA Sales AUTHORIZATION dbo;
CREATE SCHEMA Analytics AUTHORIZATION dbo;

-- Grant access only to tenant users
CREATE USER [companyA_user] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [companyA_user];
```

**2. Schema-per-Tenant (Moderate Isolation):**
```sql
-- Shared database with tenant schemas
CREATE SCHEMA [Tenant_CompanyA] AUTHORIZATION dbo;
CREATE SCHEMA [Tenant_CompanyB] AUTHORIZATION dbo;

-- Create tables in tenant schemas
CREATE TABLE [Tenant_CompanyA].Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATETIME2 NOT NULL,
    TenantID VARCHAR(50) NOT NULL DEFAULT 'CompanyA'
);

-- Row-level security for additional protection
CREATE FUNCTION [Tenant_CompanyA].fn_tenantAccessPredicate(@TenantID VARCHAR(50))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS accessResult
WHERE @TenantID = CAST(SESSION_CONTEXT(N'TenantID') AS VARCHAR(50));

CREATE SECURITY POLICY TenantPolicy
ADD FILTER PREDICATE [Tenant_CompanyA].fn_tenantAccessPredicate(TenantID) 
ON [Tenant_CompanyA].Orders
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
EXEC sp_set_session_context @key = N'TenantID', @value = 'CompanyA', @read_only = 1;
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
tenant_accessor = MultiTenantDataAccess(tenant_id="CompanyA")
orders = tenant_accessor.query_tenant_data("SELECT * FROM dbo.Orders WHERE OrderDate > '2026-01-01'")
```

**Encryption and Key Management:**
```bash
# Separate encryption keys per tenant using Key Vault
az keyvault create \
  --name tenant-companya-kv \
  --resource-group multi-tenant-rg \
  --location eastus \
  --enable-purge-protection true

# Create tenant-specific key
az keyvault key create \
  --vault-name tenant-companya-kv \
  --name tenant-encryption-key \
  --protection hsm \
  --size 4096

# Enable transparent data encryption with CMK
az sql db tde set \
  --resource-group multi-tenant-rg \
  --server synapse-server \
  --database Tenant_CompanyA \
  --status Enabled \
  --encryption-protector ServerManagedKey

az sql db tde key set \
  --resource-group multi-tenant-rg \
  --server synapse-server \
  --database Tenant_CompanyA \
  --kid https://tenant-companya-kv.vault.azure.net/keys/tenant-encryption-key
```

**Audit and Compliance:**
```sql
-- Enable auditing per tenant
CREATE DATABASE AUDIT SPECIFICATION [Tenant_CompanyA_Audit]
FOR SERVER AUDIT [SynapseAudit]
ADD (SELECT ON DATABASE::Tenant_CompanyA BY public),
ADD (INSERT ON DATABASE::Tenant_CompanyA BY public),
ADD (UPDATE ON DATABASE::Tenant_CompanyA BY public),
ADD (DELETE ON DATABASE::Tenant_CompanyA BY public)
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
WHERE database_name = 'Tenant_CompanyA'
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
                ['ml-team@company.com'],
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
                alert_notification={"emails": ["ml-team@company.com"]}
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
      "contactEmails": ["finops@company.com"],
      "contactRoles": ["Owner", "Contributor"]
    },
    {
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 100,
      "contactEmails": ["finops@company.com", "cto@company.com"],
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

---

## GCP (Google Cloud Platform)

### Advanced Networking & Security

##### Q. How do you create a custom VPC network with multiple subnets in different regions?

**Answer:**
In GCP, VPC networks are global resources, and subnets are regional. Here's how to create a custom VPC with multiple subnets:

**Steps:**
1. Create a custom VPC network
2. Create subnets in different regions
3. Configure firewall rules

**Commands:**
```bash
# Create custom VPC network
gcloud compute networks create my-custom-vpc \
    --subnet-mode=custom \
    --bgp-routing-mode=regional

# Create subnet in us-central1
gcloud compute networks subnets create subnet-us-central \
    --network=my-custom-vpc \
    --region=us-central1 \
    --range=10.0.1.0/24

# Create subnet in europe-west1
gcloud compute networks subnets create subnet-europe \
    --network=my-custom-vpc \
    --region=europe-west1 \
    --range=10.0.2.0/24

# List subnets
gcloud compute networks subnets list --network=my-custom-vpc
```

---

##### Q. Explain VPC Peering in GCP and how to configure it securely?

**Answer:**
VPC Network Peering allows private communication between VPC networks across projects or organizations. Traffic stays within Google's network and doesn't traverse the public internet.

**Key Security Features:**
- Private IP connectivity
- No external IP addresses required
- No network bandwidth bottlenecks
- Lower network latency

**Steps:**
1. Create peering connection from both VPCs
2. Configure firewall rules
3. Verify connectivity

**Commands:**
```bash
# From VPC Network 1
gcloud compute networks peerings create peer-1-to-2 \
    --network=vpc-network-1 \
    --peer-project=PROJECT_ID_2 \
    --peer-network=vpc-network-2 \
    --auto-create-routes

# From VPC Network 2
gcloud compute networks peerings create peer-2-to-1 \
    --network=vpc-network-2 \
    --peer-project=PROJECT_ID_1 \
    --peer-network=vpc-network-1 \
    --auto-create-routes

# List peering connections
gcloud compute networks peerings list --network=vpc-network-1

# Verify peering status
gcloud compute networks peerings list-routes peer-1-to-2 \
    --network=vpc-network-1 \
    --region=us-central1
```

---

##### Q. How do you implement Cloud NAT for private instances to access the internet securely?

**Answer:**
Cloud NAT enables private instances without external IP addresses to access the internet securely while maintaining security by blocking inbound connections.

**Steps:**
1. Create Cloud Router
2. Configure Cloud NAT
3. Verify NAT gateway

**Commands:**
```bash
# Create Cloud Router
gcloud compute routers create nat-router \
    --network=my-vpc \
    --region=us-central1

# Create Cloud NAT configuration
gcloud compute routers nats create my-nat-config \
    --router=nat-router \
    --region=us-central1 \
    --nat-all-subnet-ip-ranges \
    --auto-allocate-nat-external-ips

# Create NAT with specific IP addresses
gcloud compute addresses create nat-ip-1 nat-ip-2 \
    --region=us-central1

gcloud compute routers nats create my-nat-config \
    --router=nat-router \
    --region=us-central1 \
    --nat-custom-subnet-ip-ranges=subnet-us-central \
    --nat-external-ip-pool=nat-ip-1,nat-ip-2

# Describe NAT configuration
gcloud compute routers nats describe my-nat-config \
    --router=nat-router \
    --region=us-central1

# View NAT gateway logs
gcloud logging read "resource.type=nat_gateway" \
    --limit=50 \
    --format=json
```

---

##### Q. Configure Cloud Armor security policies for DDoS protection and WAF rules?

**Answer:**
Cloud Armor provides DDoS protection and WAF capabilities at the edge of Google's network. It integrates with Cloud Load Balancing.

**Steps:**
1. Create security policy
2. Add rules (allow/deny)
3. Configure rate limiting
4. Attach to backend service

**Commands:**
```bash
# Create security policy
gcloud compute security-policies create my-security-policy \
    --description="DDoS and WAF protection"

# Add rule to block specific IP range
gcloud compute security-policies rules create 1000 \
    --security-policy=my-security-policy \
    --expression="origin.ip == '203.0.113.0/24'" \
    --action=deny-403 \
    --description="Block malicious IP range"

# Add rule to allow specific countries
gcloud compute security-policies rules create 2000 \
    --security-policy=my-security-policy \
    --expression="origin.region_code == 'US' || origin.region_code == 'CA'" \
    --action=allow \
    --description="Allow US and Canada"

# Add rate limiting rule
gcloud compute security-policies rules create 3000 \
    --security-policy=my-security-policy \
    --expression="true" \
    --action=rate-based-ban \
    --rate-limit-threshold-count=100 \
    --rate-limit-threshold-interval-sec=60 \
    --ban-duration-sec=600 \
    --conform-action=allow \
    --exceed-action=deny-429 \
    --enforce-on-key=IP

# Add SQL injection protection
gcloud compute security-policies rules create 4000 \
    --security-policy=my-security-policy \
    --expression="evaluatePreconfiguredExpr('sqli-stable')" \
    --action=deny-403 \
    --description="Block SQL injection attempts"

# Add XSS protection
gcloud compute security-policies rules create 5000 \
    --security-policy=my-security-policy \
    --expression="evaluatePreconfiguredExpr('xss-stable')" \
    --action=deny-403 \
    --description="Block XSS attacks"

# Attach to backend service
gcloud compute backend-services update my-backend-service \
    --security-policy=my-security-policy \
    --global

# List security policies
gcloud compute security-policies list

# Describe policy
gcloud compute security-policies describe my-security-policy
```

---

##### Q. How do you set up Private Google Access and Private Service Connect?

**Answer:**
**Private Google Access:** Allows VMs without external IPs to access Google APIs
**Private Service Connect:** Enables private connectivity to Google services and third-party services

**Private Google Access Setup:**
```bash
# Enable Private Google Access on subnet
gcloud compute networks subnets update subnet-us-central \
    --region=us-central1 \
    --enable-private-ip-google-access

# Verify Private Google Access
gcloud compute networks subnets describe subnet-us-central \
    --region=us-central1 \
    --format="get(privateIpGoogleAccess)"

# Create custom route to Google APIs
gcloud compute routes create route-to-google-apis \
    --network=my-vpc \
    --destination-range=199.36.153.8/30 \
    --next-hop-gateway=default-internet-gateway
```

**Private Service Connect Setup:**
```bash
# Create Private Service Connect endpoint
gcloud compute addresses create psc-endpoint-ip \
    --global \
    --purpose=PRIVATE_SERVICE_CONNECT \
    --addresses=10.0.3.10 \
    --network=my-vpc

# Create forwarding rule for Private Service Connect
gcloud compute forwarding-rules create psc-forwarding-rule \
    --global \
    --network=my-vpc \
    --address=psc-endpoint-ip \
    --target-google-apis-bundle=all-apis \
    --service-directory-registration=projects/PROJECT_ID/locations/us-central1

# List Private Service Connect endpoints
gcloud compute forwarding-rules list \
    --filter="loadBalancingScheme:INTERNAL"
```

---

##### Q. Implement Cloud VPN with high availability and configure BGP routing?

**Answer:**
Cloud VPN provides encrypted connectivity between on-premises network and GCP VPC. HA VPN provides 99.99% availability.

**Steps:**
1. Create Cloud Router with BGP
2. Create HA VPN Gateway
3. Create VPN tunnels
4. Configure BGP sessions

**Commands:**
```bash
# Create Cloud Router with BGP
gcloud compute routers create vpn-router \
    --region=us-central1 \
    --network=my-vpc \
    --asn=65001

# Create HA VPN Gateway
gcloud compute vpn-gateways create ha-vpn-gateway \
    --network=my-vpc \
    --region=us-central1

# Get gateway details
gcloud compute vpn-gateways describe ha-vpn-gateway \
    --region=us-central1

# Create peer VPN gateway
gcloud compute external-vpn-gateways create peer-gateway \
    --interfaces=0=PEER_IP_ADDRESS_1,1=PEER_IP_ADDRESS_2

# Create VPN tunnels (2 tunnels for HA)
gcloud compute vpn-tunnels create tunnel-1 \
    --peer-external-gateway=peer-gateway \
    --peer-external-gateway-interface=0 \
    --region=us-central1 \
    --ike-version=2 \
    --shared-secret=SECRET_1 \
    --router=vpn-router \
    --vpn-gateway=ha-vpn-gateway \
    --interface=0

gcloud compute vpn-tunnels create tunnel-2 \
    --peer-external-gateway=peer-gateway \
    --peer-external-gateway-interface=1 \
    --region=us-central1 \
    --ike-version=2 \
    --shared-secret=SECRET_2 \
    --router=vpn-router \
    --vpn-gateway=ha-vpn-gateway \
    --interface=1

# Configure BGP sessions
gcloud compute routers add-interface vpn-router \
    --interface-name=if-tunnel-1 \
    --ip-address=169.254.1.1 \
    --mask-length=30 \
    --vpn-tunnel=tunnel-1 \
    --region=us-central1

gcloud compute routers add-bgp-peer vpn-router \
    --peer-name=bgp-peer-1 \
    --interface=if-tunnel-1 \
    --peer-ip-address=169.254.1.2 \
    --peer-asn=65002 \
    --region=us-central1

# Verify VPN tunnel status
gcloud compute vpn-tunnels describe tunnel-1 \
    --region=us-central1

# Check BGP routes
gcloud compute routers get-status vpn-router \
    --region=us-central1
```

---

##### Q. How do you configure Cloud Load Balancing with SSL/TLS termination and backend security?

**Answer:**
GCP offers various load balancers (HTTP(S), TCP/SSL Proxy, Network). HTTPS Load Balancing provides SSL termination, CDN, and Cloud Armor integration.

**Steps:**
1. Create SSL certificate
2. Create backend service with health check
3. Create URL map
4. Create target HTTPS proxy
5. Create forwarding rule

**Commands:**
```bash
# Create managed SSL certificate
gcloud compute ssl-certificates create my-ssl-cert \
    --domains=example.com,www.example.com \
    --global

# Or upload self-managed certificate
gcloud compute ssl-certificates create my-ssl-cert \
    --certificate=PATH_TO_CERT.crt \
    --private-key=PATH_TO_KEY.key \
    --global

# Create health check
gcloud compute health-checks create https https-health-check \
    --port=443 \
    --request-path=/health \
    --check-interval=10s \
    --timeout=5s \
    --unhealthy-threshold=3 \
    --healthy-threshold=2

# Create backend service with security features
gcloud compute backend-services create my-backend-service \
    --protocol=HTTPS \
    --health-checks=https-health-check \
    --port-name=https \
    --timeout=30s \
    --enable-cdn \
    --enable-logging \
    --logging-sample-rate=1.0 \
    --connection-draining-timeout=300 \
    --global

# Add instance group to backend
gcloud compute backend-services add-backend my-backend-service \
    --instance-group=my-instance-group \
    --instance-group-zone=us-central1-a \
    --balancing-mode=UTILIZATION \
    --max-utilization=0.8 \
    --capacity-scaler=1.0 \
    --global

# Configure Cloud Armor on backend
gcloud compute backend-services update my-backend-service \
    --security-policy=my-security-policy \
    --global

# Create URL map
gcloud compute url-maps create my-url-map \
    --default-service=my-backend-service

# Add path matcher for advanced routing
gcloud compute url-maps add-path-matcher my-url-map \
    --path-matcher-name=my-matcher \
    --default-service=my-backend-service \
    --path-rules="/api/*=api-backend-service,/static/*=static-backend-service"

# Create target HTTPS proxy with SSL policy
gcloud compute ssl-policies create my-ssl-policy \
    --profile=MODERN \
    --min-tls-version=1.2

gcloud compute target-https-proxies create my-https-proxy \
    --url-map=my-url-map \
    --ssl-certificates=my-ssl-cert \
    --ssl-policy=my-ssl-policy

# Create global forwarding rule
gcloud compute forwarding-rules create my-https-forwarding-rule \
    --address=my-static-ip \
    --global \
    --target-https-proxy=my-https-proxy \
    --ports=443

# Enable HTTP to HTTPS redirect
gcloud compute url-maps import my-url-map \
    --source=url-map-redirect.yaml \
    --global
```

---

##### Q. Set up VPC Service Controls to create security perimeters for GCP services?

**Answer:**
VPC Service Controls provide security perimeters around GCP resources to prevent data exfiltration.

**Steps:**
1. Create access policy
2. Define service perimeter
3. Configure access levels
4. Set up ingress/egress rules

**Commands:**
```bash
# Create access policy (one-time setup per organization)
gcloud access-context-manager policies create \
    --organization=ORGANIZATION_ID \
    --title="My Access Policy"

# Set default policy
export POLICY_NAME=$(gcloud access-context-manager policies list \
    --organization=ORGANIZATION_ID \
    --format="value(name)")

# Create access level
gcloud access-context-manager levels create trusted_network \
    --policy=$POLICY_NAME \
    --title="Trusted Network Access" \
    --basic-level-spec=access-level.yaml

# access-level.yaml content:
# combiningFunction: AND
# conditions:
#   - ipSubnetworks:
#       - "203.0.113.0/24"
#     regions:
#       - US
#     members:
#       - "user:admin@example.com"

# Create service perimeter (dry-run mode first)
gcloud access-context-manager perimeters create my_perimeter \
    --policy=$POLICY_NAME \
    --title="Production Perimeter" \
    --resources=projects/PROJECT_NUMBER \
    --restricted-services=storage.googleapis.com,bigquery.googleapis.com \
    --access-levels=trusted_network \
    --enable-vpc-accessible-services \
    --vpc-allowed-services=storage.googleapis.com \
    --perimeter-type=regular

# Create perimeter with dry-run config
gcloud access-context-manager perimeters dry-run create my_perimeter \
    --policy=$POLICY_NAME \
    --perimeter-title="Test Perimeter" \
    --perimeter-resources=projects/PROJECT_NUMBER \
    --perimeter-restricted-services=storage.googleapis.com

# Add ingress rule
gcloud access-context-manager perimeters update my_perimeter \
    --policy=$POLICY_NAME \
    --set-ingress-policies=ingress-policy.yaml

# Add egress rule
gcloud access-context-manager perimeters update my_perimeter \
    --policy=$POLICY_NAME \
    --set-egress-policies=egress-policy.yaml

# List perimeters
gcloud access-context-manager perimeters list \
    --policy=$POLICY_NAME

# Monitor VPC-SC violations
gcloud logging read "protoPayload.metadata.@type=\"type.googleapis.com/google.cloud.audit.VpcServiceControlAuditMetadata\"" \
    --limit=50 \
    --format=json
```

---

##### Q. Configure Identity-Aware Proxy (IAP) for secure application access without VPN?

**Answer:**
IAP provides application-level access control, verifying user identity and context before granting access to applications.

**Steps:**
1. Enable IAP API
2. Configure OAuth consent screen
3. Enable IAP on backend service
4. Grant IAP roles

**Commands:**
```bash
# Enable IAP API
gcloud services enable iap.googleapis.com

# Configure IAP for App Engine
gcloud iap web enable \
    --resource-type=app-engine \
    --service=default

# Configure IAP for Compute Engine
gcloud iap web enable \
    --resource-type=backend-services \
    --service=my-backend-service

# Grant IAP access to user
gcloud iap web add-iam-policy-binding \
    --resource-type=backend-services \
    --service=my-backend-service \
    --member=user:user@example.com \
    --role=roles/iap.httpsResourceAccessor

# Grant IAP access to group
gcloud iap web add-iam-policy-binding \
    --resource-type=backend-services \
    --service=my-backend-service \
    --member=group:developers@example.com \
    --role=roles/iap.httpsResourceAccessor

# Configure access levels with context-aware access
gcloud iap settings set \
    --project=PROJECT_ID \
    --resource-type=backend-services \
    --service=my-backend-service \
    --access-levels=trusted_network

# Set OAuth client credentials
gcloud iap oauth-brands create \
    --application_title="My Application" \
    --support_email=support@example.com

# Get IAP settings
gcloud iap settings get \
    --project=PROJECT_ID \
    --resource-type=backend-services \
    --service=my-backend-service

# View IAP access logs
gcloud logging read "resource.type=gce_backend_service AND protoPayload.resourceName:iap" \
    --limit=50 \
    --format=json
```

---

##### Q. Implement Cloud Firewall rules with hierarchical firewall policies?

**Answer:**
Firewall rules control traffic to/from VM instances. Hierarchical firewall policies allow organization-level policy management.

**Steps:**
1. Create firewall rules at VPC level
2. Create hierarchical policies at org/folder level
3. Apply security best practices

**Commands:**
```bash
# VPC-level firewall rules

# Allow SSH from specific IP
gcloud compute firewall-rules create allow-ssh-from-office \
    --network=my-vpc \
    --action=ALLOW \
    --rules=tcp:22 \
    --source-ranges=203.0.113.0/24 \
    --priority=1000 \
    --description="Allow SSH from office IP"

# Allow internal traffic
gcloud compute firewall-rules create allow-internal \
    --network=my-vpc \
    --action=ALLOW \
    --rules=all \
    --source-ranges=10.0.0.0/8 \
    --priority=2000 \
    --description="Allow internal VPC traffic"

# Allow HTTPS with specific service account
gcloud compute firewall-rules create allow-https-from-lb \
    --network=my-vpc \
    --action=ALLOW \
    --rules=tcp:443 \
    --source-ranges=130.211.0.0/22,35.191.0.0/16 \
    --target-service-accounts=backend-sa@PROJECT_ID.iam.gserviceaccount.com \
    --priority=1000

# Deny all egress to specific IP
gcloud compute firewall-rules create deny-egress-to-restricted \
    --network=my-vpc \
    --action=DENY \
    --rules=all \
    --direction=EGRESS \
    --destination-ranges=192.0.2.0/24 \
    --priority=900

# Hierarchical Firewall Policies

# Create organization-level policy
gcloud compute firewall-policies create my-org-policy \
    --organization=ORGANIZATION_ID \
    --description="Organization-wide security policy"

# Add rule to block malicious IPs
gcloud compute firewall-policies rules create 1000 \
    --firewall-policy=my-org-policy \
    --organization=ORGANIZATION_ID \
    --action=deny \
    --direction=INGRESS \
    --src-ip-ranges=198.51.100.0/24,203.0.113.0/24 \
    --layer4-configs=all \
    --description="Block known malicious IPs"

# Add rule to allow monitoring
gcloud compute firewall-policies rules create 2000 \
    --firewall-policy=my-org-policy \
    --organization=ORGANIZATION_ID \
    --action=allow \
    --direction=INGRESS \
    --src-ip-ranges=35.191.0.0/16 \
    --layer4-configs=tcp:80,tcp:443 \
    --target-service-accounts=monitoring-sa@PROJECT_ID.iam.gserviceaccount.com

# Associate policy with folder
gcloud compute firewall-policies associations create \
    --firewall-policy=my-org-policy \
    --organization=ORGANIZATION_ID \
    --folder=FOLDER_ID \
    --name=production-policy

# Enable firewall logging
gcloud compute firewall-rules update allow-ssh-from-office \
    --enable-logging \
    --logging-metadata=include-all

# List firewall rules
gcloud compute firewall-rules list --filter="network:my-vpc"

# Describe firewall rule
gcloud compute firewall-rules describe allow-ssh-from-office
```

---

##### Q. Configure Cloud DNS with DNSSEC and private DNS zones?

**Answer:**
Cloud DNS provides managed DNS with DNSSEC support for security and private zones for internal name resolution.

**Steps:**
1. Create public/private DNS zones
2. Enable DNSSEC
3. Configure DNS records
4. Set up DNS forwarding

**Commands:**
```bash
# Create public DNS zone
gcloud dns managed-zones create my-public-zone \
    --dns-name=example.com. \
    --description="Public DNS zone for example.com" \
    --visibility=public

# Enable DNSSEC on public zone
gcloud dns managed-zones update my-public-zone \
    --dnssec-state=on

# Get DNSSEC key details for parent zone
gcloud dns managed-zones describe my-public-zone \
    --format="get(dnssecConfig.state)"

gcloud dns dns-keys list --zone=my-public-zone

# Create private DNS zone
gcloud dns managed-zones create my-private-zone \
    --dns-name=internal.example.com. \
    --description="Private DNS zone" \
    --visibility=private \
    --networks=my-vpc

# Add DNS records to public zone
gcloud dns record-sets create www.example.com. \
    --zone=my-public-zone \
    --type=A \
    --ttl=300 \
    --rrdatas=203.0.113.10

# Add MX record
gcloud dns record-sets create example.com. \
    --zone=my-public-zone \
    --type=MX \
    --ttl=3600 \
    --rrdatas="10 mail.example.com."

# Add TXT record for SPF
gcloud dns record-sets create example.com. \
    --zone=my-public-zone \
    --type=TXT \
    --ttl=3600 \
    --rrdatas="v=spf1 include:_spf.google.com ~all"

# Add CNAME record
gcloud dns record-sets create blog.example.com. \
    --zone=my-public-zone \
    --type=CNAME \
    --ttl=300 \
    --rrdatas=www.example.com.

# Add records to private zone
gcloud dns record-sets create db.internal.example.com. \
    --zone=my-private-zone \
    --type=A \
    --ttl=300 \
    --rrdatas=10.0.1.10

# Create DNS forwarding zone
gcloud dns managed-zones create forward-zone \
    --dns-name=onprem.local. \
    --description="Forward to on-premises DNS" \
    --visibility=private \
    --networks=my-vpc \
    --forwarding-targets=192.168.1.53,192.168.1.54

# Create DNS peering zone
gcloud dns managed-zones create peering-zone \
    --dns-name=peer.example.com. \
    --description="DNS peering zone" \
    --visibility=private \
    --networks=my-vpc \
    --target-network=projects/PEER_PROJECT/global/networks/peer-vpc

# Update record set
gcloud dns record-sets update www.example.com. \
    --zone=my-public-zone \
    --type=A \
    --ttl=300 \
    --rrdatas=203.0.113.20

# List DNS zones
gcloud dns managed-zones list

# List records in zone
gcloud dns record-sets list --zone=my-public-zone

# Export zone file
gcloud dns record-sets export zone-file.txt \
    --zone=my-public-zone

# Import zone file
gcloud dns record-sets import zone-file.txt \
    --zone=my-public-zone \
    --zone-file-format
```

---

##### Q. Set up Binary Authorization for container image security in GKE?

**Answer:**
Binary Authorization ensures only trusted container images are deployed to GKE clusters.

**Steps:**
1. Enable Binary Authorization API
2. Create attestors
3. Create policy
4. Sign images with attestation

**Commands:**
```bash
# Enable required APIs
gcloud services enable \
    binaryauthorization.googleapis.com \
    containeranalysis.googleapis.com \
    container.googleapis.com

# Create attestor
gcloud container binauthz attestors create my-attestor \
    --attestation-authority-note=my-note \
    --attestation-authority-note-project=PROJECT_ID

# Create note for attestor
cat > note.json <<EOF
{
  "name": "projects/PROJECT_ID/notes/my-note",
  "attestation": {
    "hint": {
      "human_readable_name": "Security Team Attestation"
    }
  }
}
EOF

curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    --data-binary @note.json \
    "https://containeranalysis.googleapis.com/v1/projects/PROJECT_ID/notes?noteId=my-note"

# Generate key pair for signing
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

# Add public key to attestor
gcloud container binauthz attestors public-keys add \
    --attestor=my-attestor \
    --public-key-file=public.pem \
    --public-key-id-override=my-key-id

# Create Binary Authorization policy
cat > policy.yaml <<EOF
admissionWhitelistPatterns:
- namePattern: gcr.io/google_containers/*
- namePattern: gcr.io/google-containers/*
- namePattern: k8s.gcr.io/*
- namePattern: gke.gcr.io/*
defaultAdmissionRule:
  requireAttestationsBy:
  - projects/PROJECT_ID/attestors/my-attestor
  enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
  evaluationMode: REQUIRE_ATTESTATION
globalPolicyEvaluationMode: ENABLE
EOF

# Import policy
gcloud container binauthz policy import policy.yaml

# Create attestation for image
IMAGE_URL="gcr.io/PROJECT_ID/my-app:v1.0"
IMAGE_DIGEST=$(gcloud container images describe $IMAGE_URL --format='get(image_summary.digest)')

# Generate signature
echo -n "$IMAGE_DIGEST" | openssl dgst -sha256 -sign private.pem | base64 > signature.txt

# Create attestation
cat > attestation.json <<EOF
{
  "resourceUri": "$IMAGE_URL",
  "noteReference": "projects/PROJECT_ID/notes/my-note",
  "attestation": {
    "signature": {
      "publicKeyId": "my-key-id",
      "signature": "$(cat signature.txt)"
    }
  }
}
EOF

curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    --data-binary @attestation.json \
    "https://containeranalysis.googleapis.com/v1/projects/PROJECT_ID/occurrences"

# Enable Binary Authorization on GKE cluster
gcloud container clusters update my-cluster \
    --zone=us-central1-a \
    --enable-binauthz

# Verify policy
gcloud container binauthz policy export
```

---

##### Q. Configure GKE Private Cluster with authorized networks and Private Google Access?

**Answer:**
GKE Private Clusters keep nodes and control plane endpoints private, enhancing security.

**Steps:**
1. Create private GKE cluster
2. Configure authorized networks
3. Enable Private Google Access
4. Set up workload identity

**Commands:**
```bash
# Create GKE private cluster
gcloud container clusters create my-private-cluster \
    --region=us-central1 \
    --enable-ip-alias \
    --enable-private-nodes \
    --enable-private-endpoint \
    --master-ipv4-cidr=172.16.0.0/28 \
    --enable-master-authorized-networks \
    --master-authorized-networks=203.0.113.0/24 \
    --network=my-vpc \
    --subnetwork=my-subnet \
    --cluster-secondary-range-name=pod-range \
    --services-secondary-range-name=service-range \
    --enable-shielded-nodes \
    --enable-network-policy \
    --enable-workload-identity \
    --workload-pool=PROJECT_ID.svc.id.goog

# Update authorized networks
gcloud container clusters update my-private-cluster \
    --region=us-central1 \
    --enable-master-authorized-networks \
    --master-authorized-networks=203.0.113.0/24,198.51.100.0/24

# Create bastion host for cluster access
gcloud compute instances create bastion-host \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network=my-vpc \
    --subnet=my-subnet \
    --no-address \
    --metadata=enable-oslogin=TRUE \
    --scopes=cloud-platform

# Connect to cluster from bastion
gcloud container clusters get-credentials my-private-cluster \
    --region=us-central1 \
    --internal-ip

# Configure Workload Identity for pod
kubectl create serviceaccount my-ksa

gcloud iam service-accounts create my-gsa

gcloud iam service-accounts add-iam-policy-binding \
    my-gsa@PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/iam.workloadIdentityUser \
    --member="serviceAccount:PROJECT_ID.svc.id.goog[default/my-ksa]"

kubectl annotate serviceaccount my-ksa \
    iam.gke.io/gcp-service-account=my-gsa@PROJECT_ID.iam.gserviceaccount.com

# Deploy pod with Workload Identity
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: workload-identity-test
spec:
  serviceAccountName: my-ksa
  containers:
  - name: test
    image: google/cloud-sdk:slim
    command: ["sleep", "infinity"]
EOF

# Enable maintenance windows
gcloud container clusters update my-private-cluster \
    --region=us-central1 \
    --maintenance-window-start=2024-01-01T00:00:00Z \
    --maintenance-window-duration=4h \
    --maintenance-window-recurrence="FREQ=WEEKLY;BYDAY=SU"

# Configure cluster autoscaling
gcloud container clusters update my-private-cluster \
    --region=us-central1 \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=10

# Enable vertical pod autoscaling
gcloud container clusters update my-private-cluster \
    --region=us-central1 \
    --enable-vertical-pod-autoscaling
```

---

##### Q. Implement Cloud Key Management Service (KMS) for encryption key management?

**Answer:**
Cloud KMS provides centralized key management for encryption keys with hardware security modules (HSM) support.

**Steps:**
1. Create key ring
2. Create encryption keys
3. Manage key versions and rotation
4. Use keys for encryption/decryption

**Commands:**
```bash
# Create key ring
gcloud kms keyrings create my-keyring \
    --location=us-central1

# Create symmetric encryption key
gcloud kms keys create my-encryption-key \
    --location=us-central1 \
    --keyring=my-keyring \
    --purpose=encryption \
    --rotation-period=90d \
    --next-rotation-time=2024-04-01T00:00:00Z

# Create HSM-backed key
gcloud kms keys create my-hsm-key \
    --location=us-central1 \
    --keyring=my-keyring \
    --purpose=encryption \
    --protection-level=hsm

# Create asymmetric signing key
gcloud kms keys create my-signing-key \
    --location=us-central1 \
    --keyring=my-keyring \
    --purpose=asymmetric-signing \
    --default-algorithm=rsa-sign-pkcs1-4096-sha512

# Create asymmetric encryption key
gcloud kms keys create my-asymmetric-key \
    --location=us-central1 \
    --keyring=my-keyring \
    --purpose=asymmetric-encryption \
    --default-algorithm=rsa-decrypt-oaep-4096-sha512

# Grant encryption/decryption permissions
gcloud kms keys add-iam-policy-binding my-encryption-key \
    --location=us-central1 \
    --keyring=my-keyring \
    --member=serviceAccount:my-sa@PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/cloudkms.cryptoKeyEncrypterDecrypter

# Encrypt data
echo "Sensitive data" > plaintext.txt

gcloud kms encrypt \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-encryption-key \
    --plaintext-file=plaintext.txt \
    --ciphertext-file=ciphertext.enc

# Decrypt data
gcloud kms decrypt \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-encryption-key \
    --ciphertext-file=ciphertext.enc \
    --plaintext-file=decrypted.txt

# Sign data
gcloud kms asymmetric-sign \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-signing-key \
    --version=1 \
    --digest-algorithm=sha512 \
    --input-file=document.txt \
    --signature-file=signature.sig

# Verify signature
gcloud kms asymmetric-verify \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-signing-key \
    --version=1 \
    --digest-algorithm=sha512 \
    --input-file=document.txt \
    --signature-file=signature.sig

# Create new key version
gcloud kms keys versions create \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-encryption-key

# Disable key version
gcloud kms keys versions disable 1 \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-encryption-key

# Destroy key version (scheduled destruction)
gcloud kms keys versions destroy 1 \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-encryption-key

# List keys
gcloud kms keys list \
    --location=us-central1 \
    --keyring=my-keyring

# Use KMS with Cloud Storage
gsutil kms encryption \
    -k projects/PROJECT_ID/locations/us-central1/keyRings/my-keyring/cryptoKeys/my-encryption-key \
    gs://my-bucket

# Use KMS with Compute Engine disk
gcloud compute disks create my-disk \
    --size=100GB \
    --zone=us-central1-a \
    --kms-key=projects/PROJECT_ID/locations/us-central1/keyRings/my-keyring/cryptoKeys/my-encryption-key
```

---

##### Q. Configure Secret Manager for secure secrets storage and access control?

**Answer:**
Secret Manager stores API keys, passwords, certificates, and other sensitive data with automatic replication and versioning.

**Steps:**
1. Create secrets
2. Add versions
3. Grant access permissions
4. Access secrets from applications

**Commands:**
```bash
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create secret
gcloud secrets create my-api-key \
    --replication-policy="automatic" \
    --labels=env=production,team=backend

# Create secret with specific replication
gcloud secrets create my-db-password \
    --replication-policy="user-managed" \
    --locations=us-central1,us-east1

# Add secret version from file
echo -n "mysecretapikey12345" | gcloud secrets versions add my-api-key \
    --data-file=-

# Add secret version from file
gcloud secrets versions add my-db-password \
    --data-file=password.txt

# Grant access to service account
gcloud secrets add-iam-policy-binding my-api-key \
    --member=serviceAccount:my-app@PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor

# Grant access to user
gcloud secrets add-iam-policy-binding my-api-key \
    --member=user:developer@example.com \
    --role=roles/secretmanager.secretVersionManager

# Access secret
gcloud secrets versions access latest \
    --secret=my-api-key

# Access specific version
gcloud secrets versions access 2 \
    --secret=my-api-key

# List secrets
gcloud secrets list

# Describe secret
gcloud secrets describe my-api-key

# List versions
gcloud secrets versions list my-api-key

# Disable version
gcloud secrets versions disable 1 \
    --secret=my-api-key

# Enable version
gcloud secrets versions enable 1 \
    --secret=my-api-key

# Destroy version
gcloud secrets versions destroy 1 \
    --secret=my-api-key

# Update secret labels
gcloud secrets update my-api-key \
    --update-labels=version=v2

# Use in Cloud Run
gcloud run deploy my-app \
    --image=gcr.io/PROJECT_ID/my-app \
    --update-secrets=API_KEY=my-api-key:latest \
    --region=us-central1

# Use in GKE with Secret Manager add-on
kubectl create secret generic app-secrets \
    --from-literal=database-url="gcpsm://projects/PROJECT_ID/secrets/my-db-password"

# Python code to access secret
cat > access_secret.py <<EOF
from google.cloud import secretmanager

def access_secret(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Usage
api_key = access_secret("PROJECT_ID", "my-api-key")
EOF

# Audit secret access
gcloud logging read "resource.type=secretmanager.googleapis.com/Secret" \
    --limit=50 \
    --format=json
```

---

##### Q. Set up Organization Policy constraints for security compliance?

**Answer:**
Organization Policies enforce compliance and security requirements across GCP resources.

**Steps:**
1. Define organization policies
2. Apply constraints at org/folder/project level
3. Monitor compliance

**Commands:**
```bash
# List available constraints
gcloud resource-manager org-policies list \
    --organization=ORGANIZATION_ID

# Restrict VM external IPs
cat > restrict-external-ips.yaml <<EOF
constraint: constraints/compute.vmExternalIpAccess
listPolicy:
  deniedValues:
  - "*"
EOF

gcloud resource-manager org-policies set-policy restrict-external-ips.yaml \
    --organization=ORGANIZATION_ID

# Allow specific external IPs for certain projects
cat > allow-external-ips.yaml <<EOF
constraint: constraints/compute.vmExternalIpAccess
listPolicy:
  allowedValues:
  - "projects/PROJECT_ID/zones/us-central1-a"
EOF

gcloud resource-manager org-policies set-policy allow-external-ips.yaml \
    --project=PROJECT_ID

# Require OS Login
cat > require-os-login.yaml <<EOF
constraint: constraints/compute.requireOsLogin
booleanPolicy:
  enforced: true
EOF

gcloud resource-manager org-policies set-policy require-os-login.yaml \
    --organization=ORGANIZATION_ID

# Disable service account key creation
cat > disable-sa-key-creation.yaml <<EOF
constraint: constraints/iam.disableServiceAccountKeyCreation
booleanPolicy:
  enforced: true
EOF

gcloud resource-manager org-policies set-policy disable-sa-key-creation.yaml \
    --organization=ORGANIZATION_ID

# Restrict resource locations
cat > restrict-locations.yaml <<EOF
constraint: constraints/gcp.resourceLocations
listPolicy:
  allowedValues:
  - "in:us-locations"
  - "in:eu-locations"
EOF

gcloud resource-manager org-policies set-policy restrict-locations.yaml \
    --organization=ORGANIZATION_ID

# Disable automatic IAM grants for default service accounts
cat > disable-auto-iam.yaml <<EOF
constraint: constraints/iam.automaticIamGrantsForDefaultServiceAccounts
booleanPolicy:
  enforced: true
EOF

gcloud resource-manager org-policies set-policy disable-auto-iam.yaml \
    --organization=ORGANIZATION_ID

# Restrict protocol forwarding
cat > restrict-protocol-forwarding.yaml <<EOF
constraint: constraints/compute.restrictProtocolForwardingCreationForTypes
listPolicy:
  deniedValues:
  - "EXTERNAL"
EOF

gcloud resource-manager org-policies set-policy restrict-protocol-forwarding.yaml \
    --organization=ORGANIZATION_ID

# Enforce uniform bucket-level access
cat > uniform-bucket-access.yaml <<EOF
constraint: constraints/storage.uniformBucketLevelAccess
booleanPolicy:
  enforced: true
EOF

gcloud resource-manager org-policies set-policy uniform-bucket-access.yaml \
    --organization=ORGANIZATION_ID

# Restrict shared VPC projects
cat > restrict-shared-vpc.yaml <<EOF
constraint: constraints/compute.restrictSharedVpcSubnetworks
listPolicy:
  allowedValues:
  - "projects/HOST_PROJECT_ID/regions/us-central1/subnetworks/allowed-subnet"
EOF

gcloud resource-manager org-policies set-policy restrict-shared-vpc.yaml \
    --folder=FOLDER_ID

# Get effective policy
gcloud resource-manager org-policies describe \
    constraints/compute.vmExternalIpAccess \
    --project=PROJECT_ID \
    --effective

# List all policies for organization
gcloud resource-manager org-policies list \
    --organization=ORGANIZATION_ID

# Delete policy
gcloud resource-manager org-policies delete \
    constraints/compute.vmExternalIpAccess \
    --organization=ORGANIZATION_ID
```

---

##### Q. Configure Cloud Logging and Cloud Monitoring for security event detection?

**Answer:**
Cloud Logging and Monitoring provide comprehensive visibility into security events and system health.

**Steps:**
1. Configure log sinks
2. Create log-based metrics
3. Set up alerts
4. Create monitoring dashboards

**Commands:**
```bash
# Create log sink to export to BigQuery
gcloud logging sinks create security-logs-sink \
    bigquery.googleapis.com/projects/PROJECT_ID/datasets/security_logs \
    --log-filter='protoPayload.methodName:"iam.googleapis.com" OR
                  protoPayload.authenticationInfo.principalEmail!=""'

# Create log sink to Cloud Storage
gcloud logging sinks create audit-logs-sink \
    storage.googleapis.com/audit-logs-bucket \
    --log-filter='logName:"logs/cloudaudit.googleapis.com"'

# Create log sink to Pub/Sub
gcloud logging sinks create security-events-sink \
    pubsub.googleapis.com/projects/PROJECT_ID/topics/security-events \
    --log-filter='severity>=WARNING'

# Grant necessary permissions to sink service account
PROJECT_NUMBER=$(gcloud projects describe PROJECT_ID --format="value(projectNumber)")
SINK_SA="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-logging.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member=$SINK_SA \
    --role=roles/bigquery.dataEditor

# Create log-based metric for failed login attempts
gcloud logging metrics create failed_logins \
    --description="Count of failed login attempts" \
    --log-filter='protoPayload.methodName="google.identity.scp.v1.Login" AND
                  protoPayload.status.code!=0'

# Create log-based metric for privilege escalation
gcloud logging metrics create privilege_escalation \
    --description="IAM role binding changes" \
    --log-filter='protoPayload.methodName="SetIamPolicy" AND
                  protoPayload.serviceData.policyDelta.bindingDeltas.action="ADD" AND
                  protoPayload.serviceData.policyDelta.bindingDeltas.role:"roles/owner"' \
    --value-extractor='EXTRACT(protoPayload.authenticationInfo.principalEmail)'

# Create alerting policy for failed logins
cat > alert-policy.yaml <<EOF
displayName: "Failed Login Attempts Alert"
conditions:
  - displayName: "Failed login threshold"
    conditionThreshold:
      filter: 'metric.type="logging.googleapis.com/user/failed_logins" AND resource.type="global"'
      comparison: COMPARISON_GT
      thresholdValue: 5
      duration: 300s
      aggregations:
        - alignmentPeriod: 60s
          perSeriesAligner: ALIGN_RATE
notificationChannels:
  - projects/PROJECT_ID/notificationChannels/CHANNEL_ID
alertStrategy:
  autoClose: 604800s
EOF

gcloud alpha monitoring policies create --policy-from-file=alert-policy.yaml

# Create notification channel for email
gcloud alpha monitoring channels create \
    --display-name="Security Team Email" \
    --type=email \
    --channel-labels=email_address=security@example.com

# Create notification channel for Slack
gcloud alpha monitoring channels create \
    --display-name="Security Slack Channel" \
    --type=slack \
    --channel-labels=url=SLACK_WEBHOOK_URL

# Create uptime check for endpoint
gcloud monitoring uptime create my-https-check \
    --display-name="Website Uptime Check" \
    --resource-type=uptime-url \
    --monitored-resource=host=example.com,path=/health \
    --period=60 \
    --timeout=10

# Query logs for security events
gcloud logging read "protoPayload.methodName:SetIamPolicy" \
    --limit=50 \
    --format=json \
    --freshness=7d

# Query logs for unauthorized access attempts
gcloud logging read 'protoPayload.status.code=7 AND
                      protoPayload.authenticationInfo.principalEmail!=""' \
    --limit=50 \
    --format=json

# Query logs for data access
gcloud logging read 'protoPayload.methodName:"storage.objects.get" OR
                      protoPayload.methodName:"storage.objects.list"' \
    --limit=50 \
    --format=json

# Create custom dashboard
cat > dashboard.json <<EOF
{
  "displayName": "Security Dashboard",
  "mosaicLayout": {
    "columns": 12,
    "tiles": [
      {
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Failed Login Attempts",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "metric.type=\"logging.googleapis.com/user/failed_logins\""
                }
              }
            }]
          }
        }
      }
    ]
  }
}
EOF

gcloud monitoring dashboards create --config-from-file=dashboard.json

# Export logs for analysis
gcloud logging read "resource.type=gce_instance" \
    --format=json \
    --freshness=1d > exported-logs.json

# Create log exclusion to reduce costs
gcloud logging exclusions create exclude-debug-logs \
    --log-filter='severity<WARNING'
```

---

##### Q. Implement Shared VPC for centralized network management?

**Answer:**
Shared VPC allows organization to connect resources from multiple projects to a common VPC network.

**Steps:**
1. Enable Shared VPC on host project
2. Attach service projects
3. Grant IAM permissions
4. Create resources in service projects

**Commands:**
```bash
# Enable Shared VPC on host project
gcloud compute shared-vpc enable HOST_PROJECT_ID

# Attach service project to host
gcloud compute shared-vpc associated-projects add SERVICE_PROJECT_ID \
    --host-project=HOST_PROJECT_ID

# Grant Shared VPC Admin role at organization level
gcloud organizations add-iam-policy-binding ORGANIZATION_ID \
    --member=user:admin@example.com \
    --role=roles/compute.xpnAdmin

# Grant Network User role for specific subnet
gcloud compute networks subnets add-iam-policy-binding shared-subnet \
    --project=HOST_PROJECT_ID \
    --region=us-central1 \
    --member=serviceAccount:SERVICE_PROJECT_NUMBER@cloudservices.gserviceaccount.com \
    --role=roles/compute.networkUser

# Grant Network User role for service account
gcloud projects add-iam-policy-binding HOST_PROJECT_ID \
    --member=serviceAccount:my-app@SERVICE_PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/compute.networkUser

# Create instance in service project using Shared VPC
gcloud compute instances create my-instance \
    --project=SERVICE_PROJECT_ID \
    --zone=us-central1-a \
    --network=projects/HOST_PROJECT_ID/global/networks/shared-vpc \
    --subnet=projects/HOST_PROJECT_ID/regions/us-central1/subnetworks/shared-subnet

# Create GKE cluster with Shared VPC
gcloud container clusters create my-gke-cluster \
    --project=SERVICE_PROJECT_ID \
    --region=us-central1 \
    --network=projects/HOST_PROJECT_ID/global/networks/shared-vpc \
    --subnetwork=projects/HOST_PROJECT_ID/regions/us-central1/subnetworks/shared-subnet \
    --cluster-secondary-range-name=pod-range \
    --services-secondary-range-name=service-range \
    --enable-ip-alias

# List associated projects
gcloud compute shared-vpc list-associated-resources HOST_PROJECT_ID

# Get Shared VPC status
gcloud compute shared-vpc get-host-project SERVICE_PROJECT_ID

# Disable Shared VPC (must remove all associated projects first)
gcloud compute shared-vpc associated-projects remove SERVICE_PROJECT_ID \
    --host-project=HOST_PROJECT_ID

gcloud compute shared-vpc disable HOST_PROJECT_ID
```

---

##### Q. Configure Cloud Interconnect for dedicated private connectivity?

**Answer:**
Cloud Interconnect provides low-latency, highly available connections between on-premises and GCP.

**Types:**
- **Dedicated Interconnect:** Direct physical connection (10 Gbps or 100 Gbps)
- **Partner Interconnect:** Connection through supported service provider

**Steps:**
1. Create VLAN attachments
2. Configure Cloud Router
3. Establish BGP sessions
4. Verify connectivity

**Commands:**
```bash
# Create Cloud Router for Interconnect
gcloud compute routers create interconnect-router \
    --region=us-central1 \
    --network=my-vpc \
    --asn=65001

# Create Dedicated Interconnect VLAN attachment
gcloud compute interconnects attachments dedicated create my-vlan-attachment \
    --region=us-central1 \
    --router=interconnect-router \
    --interconnect=my-interconnect \
    --vlan=100

# Create Partner Interconnect VLAN attachment
gcloud compute interconnects attachments partner create my-partner-attachment \
    --region=us-central1 \
    --router=interconnect-router \
    --edge-availability-domain=AVAILABILITY_DOMAIN_1 \
    --admin-enabled

# Get pairing key for partner
gcloud compute interconnects attachments describe my-partner-attachment \
    --region=us-central1 \
    --format="get(pairingKey)"

# Configure BGP session on router
gcloud compute routers add-interface interconnect-router \
    --interface-name=if-vlan-100 \
    --interconnect-attachment=my-vlan-attachment \
    --region=us-central1

gcloud compute routers add-bgp-peer interconnect-router \
    --peer-name=bgp-peer-vlan-100 \
    --interface=if-vlan-100 \
    --peer-ip-address=169.254.100.2 \
    --peer-asn=65002 \
    --region=us-central1 \
    --advertised-route-priority=100

# Add custom route advertisements
gcloud compute routers update interconnect-router \
    --region=us-central1 \
    --advertisement-mode=CUSTOM \
    --set-advertisement-ranges=10.0.0.0/8,172.16.0.0/12

# View router status and BGP routes
gcloud compute routers get-status interconnect-router \
    --region=us-central1 \
    --format=json

# List interconnects
gcloud compute interconnects list

# List VLAN attachments
gcloud compute interconnects attachments list

# Monitor interconnect metrics
gcloud monitoring time-series list \
    --filter='metric.type="interconnect.googleapis.com/network/sent_bytes_count"' \
    --format=json

# Create redundant attachment for HA
gcloud compute interconnects attachments dedicated create my-vlan-attachment-2 \
    --region=us-central1 \
    --router=interconnect-router \
    --interconnect=my-interconnect-2 \
    --vlan=101
```

---

##### Q. Set up Network Intelligence Center for network monitoring and troubleshooting?

**Answer:**
Network Intelligence Center provides comprehensive network monitoring, topology visualization, and troubleshooting tools.

**Features:**
- Network Topology
- Connectivity Tests
- Performance Dashboard
- Firewall Insights

**Commands:**
```bash
# Enable Network Management API
gcloud services enable networkmanagement.googleapis.com

# Create connectivity test (VM to VM)
gcloud network-management connectivity-tests create vm-to-vm-test \
    --source-instance=projects/PROJECT_ID/zones/us-central1-a/instances/source-vm \
    --destination-instance=projects/PROJECT_ID/zones/us-east1-b/instances/dest-vm \
    --protocol=TCP \
    --destination-port=443

# Create connectivity test (VM to external IP)
gcloud network-management connectivity-tests create vm-to-external \
    --source-instance=projects/PROJECT_ID/zones/us-central1-a/instances/my-vm \
    --destination-ip-address=8.8.8.8 \
    --protocol=TCP \
    --destination-port=53

# Create connectivity test (VM to Google API)
gcloud network-management connectivity-tests create vm-to-google-api \
    --source-instance=projects/PROJECT_ID/zones/us-central1-a/instances/my-vm \
    --destination-network=projects/PROJECT_ID/global/networks/my-vpc \
    --destination-ip-address=storage.googleapis.com \
    --protocol=HTTPS

# Run connectivity test
gcloud network-management connectivity-tests rerun vm-to-vm-test

# Get test results
gcloud network-management connectivity-tests describe vm-to-vm-test \
    --format=json

# List all connectivity tests
gcloud network-management connectivity-tests list

# Delete connectivity test
gcloud network-management connectivity-tests delete vm-to-vm-test

# View Network Topology (use Console UI)
# https://console.cloud.google.com/net-intelligence/topology

# View Performance Dashboard
# https://console.cloud.google.com/net-intelligence/performance

# Get Firewall Insights recommendations
gcloud compute firewall-rules list \
    --format="table(
        name,
        network,
        direction,
        priority,
        sourceRanges.list():label=SRC_RANGES,
        allowed[].map().firewall_rule().list():label=ALLOW,
        denied[].map().firewall_rule().list():label=DENY,
        targetTags.list():label=TARGET_TAGS
    )"

# Analyze firewall rules for shadowed rules
# (Use Console Network Intelligence Center > Firewall Insights)

# Monitor VPC Flow Logs
gcloud compute networks subnets update my-subnet \
    --region=us-central1 \
    --enable-flow-logs \
    --logging-aggregation-interval=interval-5-sec \
    --logging-flow-sampling=0.5 \
    --logging-metadata=include-all

# Query VPC Flow Logs
gcloud logging read "resource.type=gce_subnetwork AND
                      logName:compute.googleapis.com%2Fvpc_flows" \
    --limit=50 \
    --format=json

# Create metric from VPC Flow Logs
gcloud logging metrics create vpc_traffic_volume \
    --description="VPC traffic volume" \
    --log-filter='resource.type="gce_subnetwork"
                  logName:"vpc_flows"' \
    --value-extractor='EXTRACT(jsonPayload.bytes_sent)'
```

---

##### Q. Configure Packet Mirroring for network traffic analysis?

**Answer:**
Packet Mirroring clones traffic of specified instances and forwards it to collector instances for analysis, security monitoring, and troubleshooting.

**Steps:**
1. Create collector instance or load balancer
2. Create packet mirroring policy
3. Apply policy to instances or subnets
4. Analyze mirrored traffic

**Commands:**
```bash
# Create collector instance
gcloud compute instances create packet-collector \
    --zone=us-central1-a \
    --machine-type=n2-standard-4 \
    --network=my-vpc \
    --subnet=collector-subnet \
    --can-ip-forward \
    --tags=packet-collector

# Create internal load balancer as collector
gcloud compute forwarding-rules create packet-collector-lb \
    --region=us-central1 \
    --load-balancing-scheme=INTERNAL \
    --network=my-vpc \
    --subnet=collector-subnet \
    --ip-protocol=TCP \
    --ports=ALL \
    --backend-service=collector-backend-service

# Create packet mirroring policy
gcloud compute packet-mirrorings create my-mirroring-policy \
    --region=us-central1 \
    --network=my-vpc \
    --collector-ilb=packet-collector-lb \
    --mirrored-subnets=monitored-subnet \
    --filter-cidr-ranges=0.0.0.0/0 \
    --filter-protocols=tcp,udp,icmp

# Mirror specific instances
gcloud compute packet-mirrorings create instance-mirroring \
    --region=us-central1 \
    --network=my-vpc \
    --collector-ilb=packet-collector-lb \
    --mirrored-instances=instance-1,instance-2 \
    --filter-protocols=tcp \
    --filter-direction=INGRESS

# Mirror with specific tags
gcloud compute packet-mirrorings create tag-based-mirroring \
    --region=us-central1 \
    --network=my-vpc \
    --collector-ilb=packet-collector-lb \
    --mirrored-tags=web-server,app-server

# Update mirroring policy
gcloud compute packet-mirrorings update my-mirroring-policy \
    --region=us-central1 \
    --add-mirrored-instances=instance-3

# Enable/Disable mirroring
gcloud compute packet-mirrorings update my-mirroring-policy \
    --region=us-central1 \
    --no-enable

gcloud compute packet-mirrorings update my-mirroring-policy \
    --region=us-central1 \
    --enable

# List packet mirroring policies
gcloud compute packet-mirrorings list

# Describe mirroring policy
gcloud compute packet-mirrorings describe my-mirroring-policy \
    --region=us-central1

# Delete mirroring policy
gcloud compute packet-mirrorings delete my-mirroring-policy \
    --region=us-central1

# Install traffic analysis tools on collector
sudo apt-get update
sudo apt-get install -y tcpdump wireshark-common tshark

# Capture mirrored traffic
sudo tcpdump -i eth0 -w captured-traffic.pcap

# Analyze with tshark
tshark -r captured-traffic.pcap -q -z io,stat,1
```

---

##### Q. Implement Security Command Center for centralized security management?

**Answer:**
Security Command Center (SCC) provides centralized visibility into security and compliance across GCP resources.

**Features:**
- Asset inventory and discovery
- Vulnerability scanning
- Threat detection
- Compliance monitoring

**Commands:**
```bash
# Enable Security Command Center API
gcloud services enable securitycenter.googleapis.com

# Grant SCC admin role
gcloud organizations add-iam-policy-binding ORGANIZATION_ID \
    --member=user:security-admin@example.com \
    --role=roles/securitycenter.admin

# List all findings
gcloud scc findings list ORGANIZATION_ID \
    --source=SOURCE_ID

# List findings by category
gcloud scc findings list ORGANIZATION_ID \
    --source=SOURCE_ID \
    --filter="category=\"OPEN_FIREWALL\""

# List high severity findings
gcloud scc findings list ORGANIZATION_ID \
    --source=SOURCE_ID \
    --filter="severity=\"HIGH\""

# List findings for specific project
gcloud scc findings list ORGANIZATION_ID \
    --source=SOURCE_ID \
    --filter="resourceName:\"projects/PROJECT_ID\""

# Update finding state
gcloud scc findings update FINDING_ID \
    --organization=ORGANIZATION_ID \
    --source=SOURCE_ID \
    --state=INACTIVE

# Create finding
gcloud scc findings create FINDING_ID \
    --organization=ORGANIZATION_ID \
    --source=SOURCE_ID \
    --category=CUSTOM_FINDING \
    --resource-name=//compute.googleapis.com/projects/PROJECT_ID/zones/us-central1-a/instances/my-instance \
    --event-time=2024-01-01T00:00:00Z \
    --state=ACTIVE

# List assets
gcloud scc assets list ORGANIZATION_ID \
    --filter="securityCenterProperties.resourceType=\"google.compute.Instance\""

# Get asset details
gcloud scc assets describe ASSET_ID \
    --organization=ORGANIZATION_ID

# List sources
gcloud scc sources list ORGANIZATION_ID

# Create notification config
gcloud scc notifications create my-notification \
    --organization=ORGANIZATION_ID \
    --description="High severity findings" \
    --pubsub-topic=projects/PROJECT_ID/topics/security-notifications \
    --filter="severity=\"HIGH\" OR severity=\"CRITICAL\""

# Update notification
gcloud scc notifications update my-notification \
    --organization=ORGANIZATION_ID \
    --description="Updated notification" \
    --filter="category=\"OPEN_FIREWALL\" OR category=\"WEAK_PASSWORD\""

# Delete notification
gcloud scc notifications delete my-notification \
    --organization=ORGANIZATION_ID

# Export findings to BigQuery
gcloud scc bqexports create my-export \
    --organization=ORGANIZATION_ID \
    --dataset=projects/PROJECT_ID/datasets/security_findings \
    --description="Export all findings" \
    --filter="state=\"ACTIVE\""

# Monitor using Cloud Monitoring
gcloud alpha monitoring policies create \
    --notification-channels=CHANNEL_ID \
    --display-name="SCC Critical Findings" \
    --condition-display-name="Critical findings threshold" \
    --condition-threshold-value=1 \
    --condition-threshold-duration=0s \
    --condition-filter='resource.type="scc.googleapis.com/Finding" AND severity="CRITICAL"'
```

---

### Theoretical Concepts & Design Patterns

##### Q. When would you choose Cloud Interconnect over Cloud VPN, and what are the trade-offs?

**Answer:**
This is actually a question I get asked a lot in real-world scenarios. The choice really depends on your bandwidth requirements, latency sensitivity, and budget.

I'd recommend Cloud Interconnect when you're dealing with large-scale data transfers or latency-critical applications. For example, if you're migrating terabytes of data regularly or running real-time analytics workloads that can't tolerate the variable latency of internet-based VPN, Interconnect is the way to go. It gives you dedicated 10 Gbps or 100 Gbps circuits with consistent performance.

On the other hand, Cloud VPN is perfect for smaller workloads or when you're just starting out. It's much easier to set up - you can have it running in under an hour - and the costs are predictable. I've used it successfully for hybrid cloud setups where we needed to connect a handful of on-premises servers to GCP for disaster recovery.

The main trade-offs are:
- **Cost:** Interconnect requires a significant upfront investment and monthly charges, while VPN is pay-as-you-go
- **Bandwidth:** Interconnect offers much higher throughput (10-100 Gbps vs VPN's 3 Gbps per tunnel)
- **Latency:** Interconnect provides consistent low latency since it doesn't go over the public internet
- **Setup time:** VPN can be configured in minutes, while Interconnect takes weeks to provision

In my experience, most organizations start with VPN and migrate to Interconnect as their cloud footprint grows. You can also use both - VPN as a backup for Interconnect to ensure redundancy.

---

##### Q. Explain the concept of Shared VPC and when you should use it versus VPC Peering?

**Answer:**
Shared VPC and VPC Peering solve different organizational challenges, and I've implemented both in various enterprise environments.

Shared VPC is really about centralized management and administration. Think of it as having a central networking team that manages all the network infrastructure, while different application teams can use those networks without having admin access. It's perfect for large organizations with strict security and governance requirements.

For instance, in my previous project with a financial services company, we used Shared VPC where the network security team owned the host project with all the VPC networks, firewall rules, and routing. Individual business units had service projects where they deployed their applications. This way, developers couldn't accidentally misconfigure firewall rules or create security holes, but they still had the flexibility to deploy resources.

VPC Peering, on the other hand, is about connecting independent networks. Use it when you have separate organizations or teams that need to maintain their own network administration but still need private connectivity. I've used this when connecting a customer's VPC to our SaaS platform's VPC - both parties maintain full control over their own networks.

Key differences:
- **Administration:** Shared VPC centralizes control; Peering keeps networks independent
- **IAM:** With Shared VPC, you can grant granular permissions at the subnet level; Peering is all-or-nothing at the network level
- **Quotas:** Shared VPC shares quotas across projects; Peering keeps them separate
- **Pricing:** Shared VPC traffic is considered internal; Peering has egress charges

Bottom line: Use Shared VPC for centralized governance within your organization, and VPC Peering when connecting separate entities that need to maintain independence.

---

##### Q. How do you design a multi-region GCP architecture for high availability and disaster recovery?

**Answer:**
Designing for multi-region HA and DR in GCP is something I'm really passionate about because I've seen both successful implementations and costly failures.

The first thing I always tell people is to distinguish between high availability (handling failures gracefully) and disaster recovery (recovering from catastrophic events). They require different strategies.

For high availability, I typically design with at least two regions - primary and secondary. Here's my approach:

**Compute Layer:**
- Use regional managed instance groups (MIGs) that span multiple zones within a region
- Set up Global Load Balancer to distribute traffic across regions
- Implement health checks that automatically route traffic away from unhealthy instances or entire regions
- I usually aim for N+1 redundancy at minimum, N+2 for critical workloads

**Data Layer:**
This is where it gets interesting. You have to balance between consistency and availability:
- For databases, I use Cloud Spanner for globally distributed relational data with strong consistency
- Cloud SQL with cross-region read replicas for read-heavy workloads
- Firestore in Datastore mode for flexible, multi-region NoSQL
- Regular automated backups with versioning, stored in multi-region Cloud Storage buckets

**Network Layer:**
- Deploy Cloud Armor at the edge for DDoS protection
- Use Cloud CDN to cache content closer to users
- Implement Cloud DNS with low TTL values for quick failover
- Set up VPN or Interconnect in multiple regions for hybrid connectivity

**Disaster Recovery Strategy:**
I follow the RPO (Recovery Point Objective) and RTO (Recovery Time Objective) framework:
- **RPO < 1 hour:** Continuous replication using tools like Actifio or native replication
- **RTO < 15 minutes:** Active-active multi-region setup with automated failover
- Regular DR drills - I schedule these quarterly because theoretical plans often fail in practice

One lesson I learned the hard way: always test your failover procedures. In one incident, we had perfect replication, but the failover took 4 hours instead of 15 minutes because DNS propagation wasn't properly configured.

Also, don't forget about data egress costs - they can be significant in multi-region setups. I've seen bills skyrocket when teams didn't account for cross-region data transfer.

---

##### Q. What are the security best practices for managing service accounts in GCP, and how do you prevent privilege escalation?

**Answer:**
Service account security is one of those areas where small mistakes can have huge consequences. I've had to clean up after incidents where overly permissive service accounts were compromised, so I'm pretty strict about this now.

**Principle of Least Privilege:**
This is non-negotiable. Every service account should have exactly the permissions it needs - nothing more. I never use primitive roles like Owner, Editor, or Viewer in production. Instead, I create custom roles tailored to specific functions.

For example, if a Cloud Run service only needs to read from Cloud Storage, I grant it `roles/storage.objectViewer` on specific buckets, not `roles/storage.admin` across the entire project.

**Key Management:**
Here's my controversial take: I avoid service account keys whenever possible. They're essentially long-lived credentials that can be stolen or leaked. Instead, I use:
- Workload Identity for GKE - this is a game changer
- Service Account impersonation for admin tasks
- Default service accounts with IAM bindings for Compute Engine and Cloud Run

When keys are absolutely necessary (like for on-premises applications), I rotate them every 90 days and store them in Secret Manager, never in code repositories or environment variables in plain text.

**Preventing Privilege Escalation:**
This requires multiple layers of defense:

1. **Organization Policies:** I enable `constraints/iam.disableServiceAccountKeyCreation` to prevent developers from creating keys
2. **IAM Conditions:** Use time-based or IP-based restrictions on sensitive permissions
3. **Service Account Separation:** Never reuse service accounts across environments (dev/staging/prod)
4. **Audit Logging:** Monitor for suspicious activities like `iam.serviceAccounts.actAs` or `iam.serviceAccountKeys.create`

I also implement the "break glass" pattern for emergency access. Instead of giving people broad permissions, I have a documented process for temporary privilege elevation that's automatically logged and reviewed.

**Real-world example:**
In one organization, a developer had `roles/iam.serviceAccountUser` on a highly privileged service account. They could essentially impersonate that account and gain admin access. We caught it during a security review and implemented conditional IAM policies that restricted impersonation to specific IP ranges and working hours.

The key is continuous monitoring. I set up Cloud Monitoring alerts for any service account permission changes and review Cloud Asset Inventory reports monthly to catch permission creep.

---

##### Q. How does VPC Service Controls differ from firewall rules, and when would you use one over the other?

**Answer:**
This is a great question because people often confuse these two security mechanisms, but they work at completely different layers and solve different problems.

**Firewall Rules** are network-layer controls. They work at the IP and port level - basically allowing or denying traffic based on source/destination IPs, protocols, and ports. Think of them as your traditional network security that's been around forever. They're perfect for:
- Controlling ingress/egress traffic to VMs
- Segmenting your network (like preventing dev VMs from talking to production)
- Allowing only specific IP ranges to access your infrastructure

**VPC Service Controls** operate at the API/service layer. They create security perimeters around Google Cloud services like Cloud Storage, BigQuery, or Cloud SQL. This is data exfiltration prevention - ensuring that even if someone has valid credentials, they can't access resources from unauthorized networks or locations.

Here's where it clicked for me: Firewall rules protect your VMs and network traffic. VPC Service Controls protect your data in managed services.

**Real-world scenario:**
Imagine an employee's laptop gets compromised, and an attacker gains access to their GCP credentials. With just firewall rules:
- The attacker could still access Cloud Storage buckets from anywhere in the world
- They could copy sensitive data from BigQuery to an external project
- They could exfiltrate data through legitimate API calls

With VPC Service Controls in place:
- Access to protected services is limited to authorized VPC networks or on-premises networks
- Data can't be copied to projects outside the security perimeter
- Even with valid credentials, the attacker can't access resources from their location

**When to use what:**

I use **Firewall Rules** for:
- VM-to-VM communication control
- Allowing/blocking specific ports and protocols
- Traditional network segmentation
- Quick, granular traffic control

I use **VPC Service Controls** for:
- Protecting sensitive data in managed services (GCS, BQ, Cloud SQL)
- Compliance requirements (PCI-DSS, HIPAA, GDPR)
- Preventing data exfiltration and unauthorized data access
- Creating secure perimeters around critical resources

**In practice, I use both together.** For a healthcare application I worked on:
- Firewall rules controlled access to application servers and databases
- VPC Service Controls created a perimeter around all PHI data in Cloud Storage and BigQuery
- This layered approach meant that even if one control failed, we had defense in depth

One caveat: VPC Service Controls can be tricky to implement because they're quite restrictive by default. I always recommend starting with dry-run mode to see what would be blocked before enforcing the policies. I've seen organizations lock themselves out of their own resources by applying too-restrictive policies without testing first!

---

### MLOps, AIOps, Data Engineering & Security

##### Q. How do you implement an end-to-end MLOps pipeline on GCP using Vertex AI with automated retraining?

**Answer:**
Vertex AI Pipelines provides a comprehensive MLOps platform on GCP for building, deploying, and managing ML models at scale.

**Architecture Components:**
1. **Vertex AI Workbench** - Managed Jupyter notebooks
2. **Vertex AI Pipelines** - Kubeflow-based orchestration
3. **Vertex AI Feature Store** - Centralized feature management
4. **Vertex AI Model Registry** - Versioned model storage
5. **Vertex AI Endpoints** - Managed model serving
6. **Cloud Build** - CI/CD automation
7. **Cloud Composer (Airflow)** - Workflow orchestration

**Implementation:**

```python
# vertex_mlops_pipeline.py
from google.cloud import aiplatform
from kfp.v2 import dsl, compiler
from kfp.v2.dsl import component, pipeline, Input, Output, Dataset, Model, Metrics
from typing import NamedTuple

# Initialize Vertex AI
aiplatform.init(
    project='my-project',
    location='us-central1',
    staging_bucket='gs://mlops-staging'
)

# Define pipeline components
@component(
    base_image='python:3.9',
    packages_to_install=['pandas', 'scikit-learn', 'google-cloud-aiplatform']
)
def load_data(
    dataset_name: str,
    output_dataset: Output[Dataset]
):
    """Load training data from BigQuery"""
    from google.cloud import bigquery
    import pandas as pd
    
    client = bigquery.Client()
    
    query = f"""
        SELECT 
            customer_id,
            age,
            tenure_months,
            monthly_charges,
            total_charges,
            churn_label
        FROM `{dataset_name}`
        WHERE partition_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    """
    
    df = client.query(query).to_dataframe()
    
    # Save dataset
    df.to_csv(output_dataset.path, index=False)
    
    print(f"Loaded {len(df)} records")

@component(
    base_image='python:3.9',
    packages_to_install=['pandas', 'great-expectations']
)
def validate_data(
    input_dataset: Input[Dataset],
    validation_report: Output[Metrics]
) -> NamedTuple('Outputs', [('is_valid', bool), ('quality_score', float)]):
    """Validate data quality with Great Expectations"""
    import pandas as pd
    import great_expectations as ge
    
    df = pd.read_csv(input_dataset.path)
    ge_df = ge.from_pandas(df)
    
    # Define expectations
    results = []
    results.append(ge_df.expect_column_values_to_not_be_null('customer_id'))
    results.append(ge_df.expect_column_values_to_be_between('age', 18, 100))
    results.append(ge_df.expect_column_values_to_be_between('monthly_charges', 0, 10000))
    
    # Calculate quality score
    successful = sum([1 for r in results if r.success])
    quality_score = successful / len(results)
    
    validation_report.log_metric('quality_score', quality_score)
    validation_report.log_metric('total_checks', len(results))
    validation_report.log_metric('passed_checks', successful)
    
    from collections import namedtuple
    output = namedtuple('Outputs', ['is_valid', 'quality_score'])
    return output(quality_score >= 0.95, quality_score)

@component(
    base_image='gcr.io/deeplearning-platform-release/sklearn-cpu.0-24',
    packages_to_install=['google-cloud-aiplatform']
)
def train_model(
    input_dataset: Input[Dataset],
    model: Output[Model],
    metrics: Output[Metrics],
    learning_rate: float = 0.01,
    n_estimators: int = 100
):
    """Train ML model with hyperparameter tuning"""
    import pandas as pd
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    import pickle
    
    # Load data
    df = pd.read_csv(input_dataset.path)
    
    # Prepare features
    X = df[['age', 'tenure_months', 'monthly_charges', 'total_charges']]
    y = df['churn_label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    clf = GradientBoostingClassifier(
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        random_state=42
    )
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Log metrics
    metrics.log_metric('accuracy', accuracy)
    metrics.log_metric('precision', precision)
    metrics.log_metric('recall', recall)
    metrics.log_metric('f1_score', f1)
    
    # Save model
    with open(model.path, 'wb') as f:
        pickle.dump(clf, f)
    
    print(f"Model trained - Accuracy: {accuracy:.4f}, F1: {f1:.4f}")

@component(
    base_image='python:3.9',
    packages_to_install=['google-cloud-aiplatform']
)
def register_model(
    model: Input[Model],
    accuracy: float,
    model_name: str = 'churn-predictor'
) -> str:
    """Register model in Vertex AI Model Registry"""
    from google.cloud import aiplatform
    
    aiplatform.init(project='my-project', location='us-central1')
    
    # Upload model
    uploaded_model = aiplatform.Model.upload(
        display_name=model_name,
        artifact_uri=model.uri,
        serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-24:latest',
        labels={'accuracy': str(accuracy), 'framework': 'sklearn'}
    )
    
    return uploaded_model.resource_name

@component(
    base_image='python:3.9',
    packages_to_install=['google-cloud-aiplatform']
)
def deploy_model(
    model_resource_name: str,
    endpoint_name: str = 'churn-prediction-endpoint',
    traffic_split: int = 100
):
    """Deploy model to Vertex AI endpoint with traffic splitting"""
    from google.cloud import aiplatform
    
    aiplatform.init(project='my-project', location='us-central1')
    
    # Get or create endpoint
    endpoints = aiplatform.Endpoint.list(
        filter=f'display_name="{endpoint_name}"'
    )
    
    if endpoints:
        endpoint = endpoints[0]
        print(f"Using existing endpoint: {endpoint.resource_name}")
    else:
        endpoint = aiplatform.Endpoint.create(display_name=endpoint_name)
        print(f"Created new endpoint: {endpoint.resource_name}")
    
    # Get model
    model = aiplatform.Model(model_resource_name)
    
    # Deploy with traffic splitting (blue-green deployment)
    deployed_model = endpoint.deploy(
        model=model,
        deployed_model_display_name=f'deployment-{model.version_id}',
        machine_type='n1-standard-4',
        min_replica_count=1,
        max_replica_count=5,
        traffic_percentage=traffic_split,
        sync=True
    )
    
    print(f"Model deployed: {deployed_model}")

# Define complete MLOps pipeline
@pipeline(
    name='churn-prediction-mlops',
    description='End-to-end MLOps pipeline with validation and deployment'
)
def mlops_pipeline(
    dataset_name: str = 'my-project.customer_data.transactions',
    model_name: str = 'churn-predictor',
    min_accuracy: float = 0.85
):
    """Complete MLOps pipeline"""
    
    # Step 1: Load data
    load_data_task = load_data(dataset_name=dataset_name)
    
    # Step 2: Validate data quality
    validate_task = validate_data(input_dataset=load_data_task.outputs['output_dataset'])
    
    # Step 3: Train model (conditional on data quality)
    with dsl.Condition(
        validate_task.outputs['is_valid'] == True,
        name='data-quality-passed'
    ):
        train_task = train_model(input_dataset=load_data_task.outputs['output_dataset'])
        
        # Step 4: Register model (conditional on accuracy)
        with dsl.Condition(
            train_task.outputs['metrics'].metadata['accuracy'] >= min_accuracy,
            name='accuracy-threshold-met'
        ):
            register_task = register_model(
                model=train_task.outputs['model'],
                accuracy=train_task.outputs['metrics'].metadata['accuracy'],
                model_name=model_name
            )
            
            # Step 5: Deploy model
            deploy_task = deploy_model(
                model_resource_name=register_task.output,
                endpoint_name=f'{model_name}-endpoint'
            )

# Compile pipeline
compiler.Compiler().compile(
    pipeline_func=mlops_pipeline,
    package_path='churn_mlops_pipeline.json'
)

# Run pipeline
job = aiplatform.PipelineJob(
    display_name='churn-mlops-pipeline',
    template_path='churn_mlops_pipeline.json',
    pipeline_root='gs://mlops-staging/pipeline-runs',
    parameter_values={
        'dataset_name': 'my-project.customer_data.transactions',
        'model_name': 'churn-predictor',
        'min_accuracy': 0.85
    },
    enable_caching=True
)

job.run(sync=True)
```

**Automated Retraining with Cloud Scheduler:**

```python
# monitoring_and_retraining.py
from google.cloud import aiplatform, monitoring_v3
import json

def setup_model_monitoring():
    """Configure model monitoring for drift detection"""
    
    # Create monitoring job
    monitoring_job_config = {
        "displayName": "churn-model-monitoring",
        "modelMonitoringObjectiveConfig": {
            "trainingDataset": {
                "bigquerySource": {
                    "inputUri": "bq://my-project.customer_data.training_baseline"
                }
            },
            "trainingPredictionSkewDetectionConfig": {
                "skewThresholds": {
                    "age": {"value": 0.3},
                    "monthly_charges": {"value": 0.3},
                    "tenure_months": {"value": 0.3}
                }
            },
            "predictionDriftDetectionConfig": {
                "driftThresholds": {
                    "age": {"value": 0.3},
                    "monthly_charges": {"value": 0.3}
                }
            }
        },
        "modelMonitoringAlertConfig": {
            "emailAlertConfig": {
                "userEmails": ["ml-team@company.com"]
            },
            "enableLogging": True
        },
        "loggingSamplingStrategy": {
            "randomSampleConfig": {"sampleRate": 0.8}
        },
        "schedule": {
            "cron": "0 */12 * * *"  # Every 12 hours
        }
    }
    
    return monitoring_job_config

def trigger_retraining_on_drift():
    """Cloud Function to trigger retraining on drift detection"""
    
    def retraining_trigger(event, context):
        """Triggered by Pub/Sub message from model monitoring"""
        import base64
        
        # Parse monitoring alert
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        alert_data = json.loads(pubsub_message)
        
        drift_detected = alert_data.get('driftDetected', False)
        drift_score = alert_data.get('driftScore', 0)
        
        if drift_detected and drift_score > 0.3:
            print(f"Drift detected with score {drift_score}, triggering retraining")
            
            # Trigger pipeline
            job = aiplatform.PipelineJob(
                display_name='automated-retraining',
                template_path='gs://mlops-staging/churn_mlops_pipeline.json',
                pipeline_root='gs://mlops-staging/pipeline-runs',
                parameter_values={
                    'dataset_name': 'my-project.customer_data.transactions',
                    'model_name': 'churn-predictor',
                    'min_accuracy': 0.85
                }
            )
            
            job.submit()
            
            return {'status': 'retraining_triggered', 'job_id': job.resource_name}
        
        return {'status': 'no_action_needed'}
    
    return retraining_trigger
```

**Cloud Build CI/CD Pipeline:**

```yaml
# cloudbuild.yaml
steps:
  # Step 1: Run unit tests
  - name: 'python:3.9'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        pip install pytest pandas scikit-learn
        pytest tests/ -v

  # Step 2: Build training container
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/churn-trainer:$SHORT_SHA'
      - '-f'
      - 'Dockerfile.training'
      - '.'

  # Step 3: Push container
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'gcr.io/$PROJECT_ID/churn-trainer:$SHORT_SHA'

  # Step 4: Compile pipeline
  - name: 'python:3.9'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        pip install kfp google-cloud-aiplatform
        python compile_pipeline.py

  # Step 5: Deploy to staging
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        gcloud ai custom-jobs create \
          --region=us-central1 \
          --display-name=pipeline-validation-$SHORT_SHA \
          --config=pipeline_config.yaml

  # Step 6: Run integration tests
  - name: 'python:3.9'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        pip install google-cloud-aiplatform requests
        python tests/integration_tests.py --endpoint staging-endpoint

  # Step 7: Deploy to production (on main branch)
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        if [ "$BRANCH_NAME" = "main" ]; then
          python deploy_production.py --traffic-split 10
        fi

options:
  logging: CLOUD_LOGGING_ONLY
  machineType: 'N1_HIGHCPU_8'

timeout: '1800s'
```

**Key Features:**
- Automated data quality validation with Great Expectations
- Conditional pipeline execution based on metrics
- Model versioning and registry integration
- Blue-green deployment with traffic splitting
- Drift detection and automated retraining
- CI/CD with Cloud Build
- Comprehensive monitoring and alerting

---

##### Q. How do you implement AIOps for predictive incident detection on GCP using Cloud Operations?

**Answer:**
AIOps on GCP leverages Cloud Operations Suite (formerly Stackdriver) with machine learning for proactive incident detection and automated remediation.

**Architecture:**
1. **Cloud Logging** - Centralized log aggregation
2. **Cloud Monitoring** - Metrics and alerting
3. **Cloud Trace** - Distributed tracing
4. **Cloud Profiler** - Performance profiling
5. **Error Reporting** - Error tracking
6. **BigQuery** - Log analytics
7. **Vertex AI** - Anomaly detection models

**Implementation:**

```python
# aiops_anomaly_detection.py
from google.cloud import logging_v2, monitoring_v3, bigquery
from google.cloud import aiplatform
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta

class GCPAIOps:
    """AIOps implementation for GCP infrastructure"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.logging_client = logging_v2.Client(project=project_id)
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        self.bq_client = bigquery.Client(project=project_id)
        
    def setup_log_based_metrics(self):
        """Create log-based metrics for anomaly detection"""
        
        # Create metric for error rate
        metric_descriptor = {
            "type": f"logging.googleapis.com/user/error_rate",
            "metric_kind": monitoring_v3.MetricDescriptor.MetricKind.GAUGE,
            "value_type": monitoring_v3.MetricDescriptor.ValueType.DOUBLE,
            "description": "Application error rate per minute",
            "display_name": "Error Rate"
        }
        
        # Create log sink to BigQuery for ML analysis
        sink_name = f"projects/{self.project_id}/sinks/aiops-analysis"
        destination = f"bigquery.googleapis.com/projects/{self.project_id}/datasets/aiops_logs"
        
        log_filter = '''
        severity >= ERROR
        OR resource.type = "gce_instance"
        OR resource.type = "k8s_cluster"
        OR protoPayload.status.code != 0
        '''
        
        sink = self.logging_client.sink(sink_name, filter_=log_filter, destination=destination)
        
        if not sink.exists():
            sink.create()
            print(f"Created log sink: {sink_name}")
        
        return sink
    
    def collect_metrics_for_training(self, days: int = 30):
        """Collect historical metrics for anomaly detection model"""
        
        query = f"""
        SELECT
            TIMESTAMP_TRUNC(timestamp, MINUTE) as time_bucket,
            resource.type as resource_type,
            resource.labels.instance_id as instance_id,
            
            -- CPU metrics
            AVG(IF(metric.type = 'compute.googleapis.com/instance/cpu/utilization',
                metric.value, NULL)) as cpu_utilization,
            
            -- Memory metrics
            AVG(IF(metric.type = 'compute.googleapis.com/instance/memory/used_bytes',
                metric.value, NULL)) as memory_used,
            
            -- Network metrics
            SUM(IF(metric.type = 'compute.googleapis.com/instance/network/received_bytes_count',
                metric.value, NULL)) as network_rx_bytes,
            SUM(IF(metric.type = 'compute.googleapis.com/instance/network/sent_bytes_count',
                metric.value, NULL)) as network_tx_bytes,
            
            -- Disk metrics
            AVG(IF(metric.type = 'compute.googleapis.com/instance/disk/write_ops_count',
                metric.value, NULL)) as disk_write_ops,
            AVG(IF(metric.type = 'compute.googleapis.com/instance/disk/read_ops_count',
                metric.value, NULL)) as disk_read_ops,
            
            -- Error count from logs
            COUNTIF(severity = 'ERROR') as error_count,
            COUNTIF(severity = 'WARNING') as warning_count
            
        FROM `{self.project_id}.aiops_logs.compute_googleapis_com_*`
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
        GROUP BY time_bucket, resource_type, instance_id
        ORDER BY time_bucket DESC
        """
        
        df = self.bq_client.query(query).to_dataframe()
        return df
    
    def train_anomaly_detector(self):
        """Train ML model for anomaly detection"""
        
        # Collect training data
        df = self.collect_metrics_for_training(days=90)
        
        # Feature engineering
        features = [
            'cpu_utilization',
            'memory_used',
            'network_rx_bytes',
            'network_tx_bytes',
            'disk_write_ops',
            'disk_read_ops',
            'error_count',
            'warning_count'
        ]
        
        # Fill missing values
        df[features] = df[features].fillna(0)
        
        # Add temporal features
        df['hour'] = pd.to_datetime(df['time_bucket']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['time_bucket']).dt.dayofweek
        
        features.extend(['hour', 'day_of_week'])
        
        # Train Isolation Forest for anomaly detection
        X = df[features].values
        
        model = IsolationForest(
            contamination=0.1,  # Expect 10% anomalies
            random_state=42,
            n_estimators=100
        )
        model.fit(X)
        
        # Save model to Vertex AI
        import pickle
        with open('anomaly_detector.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        # Upload to Vertex AI Model Registry
        aiplatform.init(project=self.project_id, location='us-central1')
        
        uploaded_model = aiplatform.Model.upload(
            display_name='infrastructure-anomaly-detector',
            artifact_uri='gs://aiops-models/anomaly_detector.pkl',
            serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-24:latest'
        )
        
        return uploaded_model
    
    def predict_anomalies_realtime(self):
        """Real-time anomaly detection on streaming metrics"""
        
        # Get current metrics
        now = datetime.utcnow()
        interval = monitoring_v3.TimeInterval({
            'end_time': {'seconds': int(now.timestamp())},
            'start_time': {'seconds': int((now - timedelta(minutes=5)).timestamp())}
        })
        
        # Query multiple metrics
        results = self.monitoring_client.list_time_series(
            request={
                'name': f'projects/{self.project_id}',
                'filter': 'resource.type = "gce_instance"',
                'interval': interval,
                'view': monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
            }
        )
        
        anomalies = []
        
        for result in results:
            # Extract metrics
            for point in result.points:
                # Call Vertex AI model for prediction
                # If anomaly score high, trigger alert
                
                if self.is_anomalous(point.value):
                    anomalies.append({
                        'resource': result.resource.labels,
                        'metric': result.metric.type,
                        'value': point.value.double_value,
                        'timestamp': point.interval.end_time
                    })
        
        return anomalies
    
    def automated_remediation(self, anomaly):
        """Automated incident remediation"""
        
        from googleapiclient import discovery
        
        compute = discovery.build('compute', 'v1')
        
        resource_type = anomaly['resource'].get('resource_type')
        instance_name = anomaly['resource'].get('instance_id')
        zone = anomaly['resource'].get('zone')
        
        # Determine remediation action
        if anomaly['metric'] == 'cpu_utilization' and anomaly['value'] > 90:
            # High CPU - restart instance
            print(f"High CPU detected on {instance_name}, restarting...")
            
            # Take snapshot first
            snapshot_body = {
                'name': f'{instance_name}-snapshot-{int(datetime.now().timestamp())}',
                'sourceDisk': f'zones/{zone}/disks/{instance_name}'
            }
            
            compute.disks().createSnapshot(
                project=self.project_id,
                zone=zone,
                disk=instance_name,
                body=snapshot_body
            ).execute()
            
            # Restart instance
            compute.instances().reset(
                project=self.project_id,
                zone=zone,
                instance=instance_name
            ).execute()
            
            return {'action': 'instance_restarted', 'instance': instance_name}
        
        elif anomaly['metric'] == 'error_count' and anomaly['value'] > 100:
            # High error rate - scale up
            print(f"High error rate detected, scaling up...")
            
            # Trigger autoscaler
            # This would integrate with GKE or Instance Groups
            
            return {'action': 'scaled_up', 'reason': 'high_error_rate'}
        
        return {'action': 'alert_only', 'reason': 'no_automation_defined'}
    
    def setup_slo_monitoring(self):
        """Configure SLO-based alerting"""
        
        # Create SLO for API availability
        slo_config = {
            "displayName": "API Availability SLO",
            "serviceLevelIndicator": {
                "requestBased": {
                    "goodTotalRatio": {
                        "goodServiceFilter": 'metric.type="loadbalancing.googleapis.com/https/request_count" AND metric.response_code_class="2xx"',
                        "totalServiceFilter": 'metric.type="loadbalancing.googleapis.com/https/request_count"'
                    }
                }
            },
            "goal": 0.995,  # 99.5% availability
            "rollingPeriod": "2592000s"  # 30 days
        }
        
        return slo_config

# Deploy as Cloud Function for continuous monitoring
def aiops_monitor(event, context):
    """Cloud Function triggered every 5 minutes"""
    
    aiops = GCPAIOps(project_id='my-project')
    
    # Detect anomalies
    anomalies = aiops.predict_anomalies_realtime()
    
    # Remediate automatically
    for anomaly in anomalies:
        result = aiops.automated_remediation(anomaly)
        print(f"Remediation result: {result}")
    
    return {'anomalies_detected': len(anomalies)}
```

**Cloud Function for Intelligent Alerting:**

```python
# intelligent_alerting.py
from google.cloud import logging_v2, monitoring_v3
import json

def intelligent_alert_routing(event, context):
    """Route alerts based on ML-predicted severity and context"""
    
    import base64
    alert_data = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    
    # Extract alert details
    incident = alert_data.get('incident', {})
    severity = incident.get('severity', 'UNKNOWN')
    resource = incident.get('resource', {})
    
    # Determine routing based on context
    if severity == 'CRITICAL':
        # Page on-call engineer
        notify_pagerduty(incident)
        
        # Create high-priority ticket
        create_jira_ticket(incident, priority='P1')
        
        # Attempt auto-remediation
        auto_remediate(incident)
        
    elif severity == 'WARNING':
        # Check if part of known pattern
        if is_recurring_pattern(incident):
            # Suppress if already being tracked
            update_existing_incident(incident)
        else:
            # Create normal ticket
            create_jira_ticket(incident, priority='P3')
            send_slack_notification(incident)
    
    return {'status': 'processed'}

def correlation_analysis(alerts):
    """Correlate multiple alerts to identify root cause"""
    
    # Group alerts by time window and resource
    time_window = timedelta(minutes=5)
    
    correlated_groups = []
    
    for alert in alerts:
        # Check if related to existing group
        added_to_group = False
        
        for group in correlated_groups:
            if (alert['timestamp'] - group['start_time'] < time_window and
                alert['resource'] == group['resource']):
                group['alerts'].append(alert)
                added_to_group = True
                break
        
        if not added_to_group:
            correlated_groups.append({
                'start_time': alert['timestamp'],
                'resource': alert['resource'],
                'alerts': [alert]
            })
    
    # Identify root cause
    for group in correlated_groups:
        if len(group['alerts']) > 3:
            # Multiple correlated alerts - likely cascading failure
            root_cause = identify_root_cause(group['alerts'])
            group['root_cause'] = root_cause
    
    return correlated_groups
```

**Terraform for AIOps Infrastructure:**

```hcl
# aiops_infrastructure.tf

# Log sink to BigQuery for ML analysis
resource "google_logging_project_sink" "aiops_logs" {
  name        = "aiops-log-sink"
  destination = "bigquery.googleapis.com/projects/${var.project_id}/datasets/aiops_logs"
  
  filter = <<-EOT
    severity >= ERROR
    OR resource.type = "gce_instance"
    OR resource.type = "k8s_cluster"
  EOT
  
  unique_writer_identity = true
}

# BigQuery dataset for log storage
resource "google_bigquery_dataset" "aiops_logs" {
  dataset_id = "aiops_logs"
  location   = "US"
  
  default_table_expiration_ms = 7776000000  # 90 days
}

# Cloud Function for anomaly detection
resource "google_cloudfunctions_function" "aiops_monitor" {
  name        = "aiops-anomaly-detector"
  runtime     = "python39"
  entry_point = "aiops_monitor"
  
  source_archive_bucket = google_storage_bucket.functions.name
  source_archive_object = google_storage_bucket_object.function_code.name
  
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.metrics_stream.id
  }
  
  environment_variables = {
    PROJECT_ID = var.project_id
  }
}

# Pub/Sub topic for metrics streaming
resource "google_pubsub_topic" "metrics_stream" {
  name = "aiops-metrics-stream"
}

# Cloud Scheduler for periodic monitoring
resource "google_cloud_scheduler_job" "aiops_check" {
  name     = "aiops-periodic-check"
  schedule = "*/5 * * * *"  # Every 5 minutes
  
  pubsub_target {
    topic_name = google_pubsub_topic.metrics_stream.id
    data       = base64encode("{\"action\": \"check_anomalies\"}")
  }
}

# Alert policy for ML-detected anomalies
resource "google_monitoring_alert_policy" "anomaly_detected" {
  display_name = "ML Anomaly Detection Alert"
  combiner     = "OR"
  
  conditions {
    display_name = "Anomaly Score Threshold"
    
    condition_threshold {
      filter          = "metric.type=\"custom.googleapis.com/aiops/anomaly_score\" AND resource.type=\"global\""
      duration        = "60s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.8
      
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_MEAN"
      }
    }
  }
  
  notification_channels = [
    google_monitoring_notification_channel.oncall.id
  ]
  
  alert_strategy {
    auto_close = "604800s"  # 7 days
  }
}
```

---

##### Q. How do you build a secure, serverless data lakehouse on GCP with BigQuery and Dataproc?

**Answer:**
A modern data lakehouse on GCP combines BigQuery's analytics capabilities with Cloud Storage's flexibility, secured with comprehensive access controls.

**Architecture:**
1. **Cloud Storage** - Raw/processed data lake
2. **BigQuery** - Analytics and serving layer
3. **Dataproc Serverless** - Spark processing
4. **Dataflow** - Stream processing
5. **Data Catalog** - Metadata and governance
6. **DLP API** - Data loss prevention
7. **VPC Service Controls** - Security perimeter

**Implementation:**

```bash
# Setup secure data lake infrastructure

# Create data lake buckets with encryption
gcloud storage buckets create gs://data-lake-raw-${PROJECT_ID} \
    --location=us-central1 \
    --uniform-bucket-level-access \
    --encryption-key=projects/${PROJECT_ID}/locations/us-central1/keyRings/data-lake/cryptoKeys/storage-key

gcloud storage buckets create gs://data-lake-processed-${PROJECT_ID} \
    --location=us-central1 \
    --uniform-bucket-level-access \
    --encryption-key=projects/${PROJECT_ID}/locations/us-central1/keyRings/data-lake/cryptoKeys/storage-key

# Set lifecycle policies
cat > lifecycle-config.json <<EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
        "condition": {"age": 30, "matchesPrefix": ["raw/"]}
      },
      {
        "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
        "condition": {"age": 90, "matchesPrefix": ["raw/"]}
      },
      {
        "action": {"type": "SetStorageClass", "storageClass": "ARCHIVE"},
        "condition": {"age": 365, "matchesPrefix": ["raw/"]}
      },
      {
        "action": {"type": "Delete"},
        "condition": {"age": 730, "matchesPrefix": ["temp/"]}
      }
    ]
  }
}
EOF

gcloud storage buckets update gs://data-lake-raw-${PROJECT_ID} \
    --lifecycle-file=lifecycle-config.json

# Create BigQuery datasets with encryption
bq mk \
    --dataset \
    --location=us-central1 \
    --default_table_expiration=0 \
    --default_kms_key=projects/${PROJECT_ID}/locations/us-central1/keyRings/data-lake/cryptoKeys/bq-key \
    ${PROJECT_ID}:data_warehouse

bq mk \
    --dataset \
    --location=us-central1 \
    ${PROJECT_ID}:data_staging

# Enable column-level security
bq mk --table \
    --schema=schema.json \
    --time_partitioning_field=event_timestamp \
    --clustering_fields=customer_id,region \
    ${PROJECT_ID}:data_warehouse.customer_transactions
```

**Dataproc Serverless for Data Processing:**

```python
# dataproc_serverless_job.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from google.cloud import storage, dlp_v2

class SecureDataProcessor:
    """Secure data processing with PII detection and masking"""
    
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("SecureDataLakehouse") \
            .config("spark.sql.catalog.bigquery", "com.google.cloud.spark.bigquery.v2.BigQueryConnector") \
            .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.28.0") \
            .getOrCreate()
        
        self.dlp_client = dlp_v2.DlpServiceClient()
        
    def read_from_gcs(self, bucket: str, path: str):
        """Read data from Cloud Storage"""
        
        df = self.spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(f"gs://{bucket}/{path}")
        
        return df
    
    def detect_and_mask_pii(self, df, column_name: str):
        """Detect and mask PII using Cloud DLP API"""
        
        project_id = self.spark.conf.get("spark.app.id").split('-')[0]
        
        # Define PII detection config
        inspect_config = {
            "info_types": [
                {"name": "EMAIL_ADDRESS"},
                {"name": "PHONE_NUMBER"},
                {"name": "CREDIT_CARD_NUMBER"},
                {"name": "US_SOCIAL_SECURITY_NUMBER"}
            ],
            "min_likelihood": dlp_v2.Likelihood.LIKELY
        }
        
        # Define de-identification config
        deidentify_config = {
            "info_type_transformations": {
                "transformations": [
                    {
                        "primitive_transformation": {
                            "character_mask_config": {
                                "masking_character": "*",
                                "number_to_mask": 0
                            }
                        }
                    }
                ]
            }
        }
        
        # Apply masking UDF
        def mask_pii(value):
            if not value:
                return value
            
            parent = f"projects/{project_id}"
            
            item = {"value": str(value)}
            
            response = self.dlp_client.deidentify_content(
                request={
                    "parent": parent,
                    "deidentify_config": deidentify_config,
                    "inspect_config": inspect_config,
                    "item": item
                }
            )
            
            return response.item.value
        
        mask_pii_udf = udf(mask_pii, StringType())
        
        return df.withColumn(f"{column_name}_masked", mask_pii_udf(col(column_name)))
    
    def apply_data_quality_checks(self, df):
        """Apply data quality validations"""
        
        # Check for nulls in critical columns
        null_checks = df.select([
            count(when(col(c).isNull(), c)).alias(c) 
            for c in df.columns
        ])
        
        # Check for duplicates
        duplicate_count = df.count() - df.dropDuplicates().count()
        
        # Check value ranges
        quality_metrics = {
            'total_records': df.count(),
            'duplicate_records': duplicate_count,
            'null_counts': null_checks.first().asDict()
        }
        
        # Write quality metrics to BigQuery
        quality_df = self.spark.createDataFrame([quality_metrics])
        
        quality_df.write \
            .format("bigquery") \
            .option("table", f"{project_id}:data_warehouse.quality_metrics") \
            .option("temporaryGcsBucket", f"dataproc-temp-{project_id}") \
            .mode("append") \
            .save()
        
        # Fail if quality threshold not met
        if duplicate_count > df.count() * 0.01:  # More than 1% duplicates
            raise ValueError(f"Data quality check failed: {duplicate_count} duplicates found")
        
        return df
    
    def write_to_bigquery_partitioned(self, df, table_name: str, partition_field: str):
        """Write to BigQuery with partitioning and clustering"""
        
        project_id = self.spark.conf.get("spark.app.id").split('-')[0]
        
        df.write \
            .format("bigquery") \
            .option("table", f"{project_id}:data_warehouse.{table_name}") \
            .option("temporaryGcsBucket", f"dataproc-temp-{project_id}") \
            .option("partitionField", partition_field) \
            .option("partitionType", "DAY") \
            .option("clusteredFields", "customer_id,region") \
            .option("allowFieldAddition", "true") \
            .option("allowFieldRelaxation", "true") \
            .mode("append") \
            .save()
    
    def process_incremental_data(self):
        """Process incremental data with CDC pattern"""
        
        # Read new data from GCS
        raw_df = self.read_from_gcs(
            bucket=f"data-lake-raw-{project_id}",
            path="transactions/date=2026-02-24/*.csv"
        )
        
        # Add processing metadata
        processed_df = raw_df \
            .withColumn("processing_timestamp", current_timestamp()) \
            .withColumn("data_source", lit("customer_transactions")) \
            .withColumn("partition_date", to_date(col("event_timestamp")))
        
        # Mask PII columns
        processed_df = self.detect_and_mask_pii(processed_df, "email")
        processed_df = self.detect_and_mask_pii(processed_df, "phone")
        
        # Apply quality checks
        processed_df = self.apply_data_quality_checks(processed_df)
        
        # Write to processed zone
        processed_df.write \
            .mode("append") \
            .partitionBy("partition_date") \
            .parquet(f"gs://data-lake-processed-{project_id}/transactions/")
        
        # Load to BigQuery
        self.write_to_bigquery_partitioned(
            processed_df,
            table_name="customer_transactions",
            partition_field="event_timestamp"
        )
        
        print(f"Processed {processed_df.count()} records")

# Submit Dataproc Serverless job
if __name__ == "__main__":
    processor = SecureDataProcessor()
    processor.process_incremental_data()
```

**Submit job with gcloud:**

```bash
# Submit Dataproc Serverless Spark job
gcloud dataproc batches submit pyspark dataproc_serverless_job.py \
    --region=us-central1 \
    --batch=data-processing-$(date +%Y%m%d-%H%M%S) \
    --deps-bucket=gs://dataproc-deps-${PROJECT_ID} \
    --subnet=projects/${PROJECT_ID}/regions/us-central1/subnetworks/dataproc-subnet \
    --service-account=dataproc-sa@${PROJECT_ID}.iam.gserviceaccount.com \
    --properties=spark.dynamicAllocation.enabled=true,spark.dynamicAllocation.minExecutors=2,spark.dynamicAllocation.maxExecutors=20 \
    --kms-key=projects/${PROJECT_ID}/locations/us-central1/keyRings/data-lake/cryptoKeys/compute-key
```

**BigQuery Security and Governance:**

```sql
-- Row-level security for multi-tenant data
CREATE ROW ACCESS POLICY tenant_filter
ON data_warehouse.customer_transactions
GRANT TO ('user:analyst@company.com')
FILTER USING (tenant_id = SESSION_USER());

-- Column-level security with policy tags
CREATE TAXONOMY pii_taxonomy
  OPTIONS(
    display_name="PII Data Classification",
    description="Data sensitivity classification"
  );

CREATE POLICY TAG pii_taxonomy.highly_sensitive
  OPTIONS(
    display_name="Highly Sensitive PII",
    description="Contains sensitive personal information"
  );

-- Apply policy tag to columns
ALTER TABLE data_warehouse.customer_transactions
  ALTER COLUMN email SET OPTIONS (
    policy_tags=('projects/${PROJECT_ID}/locations/us-central1/taxonomies/pii_taxonomy/policyTags/highly_sensitive')
  );

-- Data masking with authorized views
CREATE VIEW `data_warehouse.customer_transactions_masked` AS
SELECT
  transaction_id,
  customer_id,
  CASE 
    WHEN SESSION_USER() IN ('user:admin@company.com') THEN email
    ELSE CONCAT('***', SUBSTR(email, INSTR(email, '@'), LENGTH(email)))
  END AS email,
  transaction_amount,
  event_timestamp
FROM `data_warehouse.customer_transactions`;

-- Grant access to masked view
GRANT `roles/bigquery.dataViewer`
ON VIEW `data_warehouse.customer_transactions_masked`
TO 'group:analysts@company.com';
```

**Data Catalog for Discovery and Lineage:**

```python
# setup_data_catalog.py
from google.cloud import datacatalog_v1

def tag_bigquery_tables():
    """Tag BigQuery tables with metadata"""
    
    datacatalog_client = datacatalog_v1.DataCatalogClient()
    
    # Create tag template
    tag_template = datacatalog_v1.TagTemplate()
    tag_template.display_name = "Data Quality Metrics"
    
    tag_template.fields["data_owner"] = datacatalog_v1.TagTemplateField()
    tag_template.fields["data_owner"].display_name = "Data Owner"
    tag_template.fields["data_owner"].type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.STRING
    
    tag_template.fields["quality_score"] = datacatalog_v1.TagTemplateField()
    tag_template.fields["quality_score"].display_name = "Quality Score"
    tag_template.fields["quality_score"].type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.DOUBLE
    
    tag_template.fields["contains_pii"] = datacatalog_v1.TagTemplateField()
    tag_template.fields["contains_pii"].display_name = "Contains PII"
    tag_template.fields["contains_pii"].type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.BOOL
    
    # Create template
    parent = f"projects/{project_id}/locations/us-central1"
    
    created_template = datacatalog_client.create_tag_template(
        parent=parent,
        tag_template_id="data_quality_template",
        tag_template=tag_template
    )
    
    # Tag tables
    table_resource = f"//bigquery.googleapis.com/projects/{project_id}/datasets/data_warehouse/tables/customer_transactions"
    
    entry = datacatalog_client.lookup_entry(
        request={"linked_resource": table_resource}
    )
    
    tag = datacatalog_v1.Tag()
    tag.template = created_template.name
    tag.fields["data_owner"].string_value = "data-engineering-team@company.com"
    tag.fields["quality_score"].double_value = 0.98
    tag.fields["contains_pii"].bool_value = True
    
    datacatalog_client.create_tag(parent=entry.name, tag=tag)
    
    print(f"Tagged table: {table_resource}")
```

**VPC Service Controls for Data Perimeter:**

```bash
# Create service perimeter for data lakehouse
gcloud access-context-manager perimeters create data_lakehouse_perimeter \
    --title="Data Lakehouse Security Perimeter" \
    --resources=projects/${PROJECT_NUMBER} \
    --restricted-services=bigquery.googleapis.com,storage.googleapis.com,dataproc.googleapis.com \
    --policy=${POLICY_NAME} \
    --perimeter-type=regular \
    --enable-vpc-accessible-services \
    --vpc-allowed-services=bigquery.googleapis.com,storage.googleapis.com

# Add ingress rule for trusted sources
cat > ingress-policy.yaml <<EOF
- ingressFrom:
    sources:
      - accessLevel: accessPolicies/${POLICY_NAME}/accessLevels/trusted_networks
    identities:
      - serviceAccount:dataproc-sa@${PROJECT_ID}.iam.gserviceaccount.com
  ingressTo:
    resources:
      - projects/${PROJECT_NUMBER}
    operations:
      - serviceName: bigquery.googleapis.com
        methodSelectors:
          - method: "*"
      - serviceName: storage.googleapis.com
        methodSelectors:
          - method: "storage.objects.get"
          - method: "storage.objects.create"
EOF

gcloud access-context-manager perimeters update data_lakehouse_perimeter \
    --set-ingress-policies=ingress-policy.yaml \
    --policy=${POLICY_NAME}
```

---

##### Q. How do you implement cost optimization and FinOps for GCP data platforms?

**Answer:**
FinOps on GCP requires continuous monitoring, rightsizing, and intelligent resource management.

**Cost Monitoring and Budgets:**

```bash
# Create budget with alerts
gcloud billing budgets create \
    --billing-account=${BILLING_ACCOUNT_ID} \
    --display-name="Data Platform Monthly Budget" \
    --budget-amount=50000USD \
    --threshold-rule=percent=50 \
    --threshold-rule=percent=90 \
    --threshold-rule=percent=100 \
    --all-updates-rule-pubsub-topic=projects/${PROJECT_ID}/topics/budget-alerts

# Export billing data to BigQuery
gcloud beta billing accounts describe ${BILLING_ACCOUNT_ID} \
    --format="value(billingAccountId)"

# Configure export
gcloud beta billing accounts update ${BILLING_ACCOUNT_ID} \
    --billing-data-export-project=${PROJECT_ID} \
    --billing-data-export-dataset-id=billing_export
```

**Automated Cost Optimization:**

```python
# cost_optimizer.py
from google.cloud import bigquery, compute_v1, recommender_v1
from google.cloud import billing_v1
import pandas as pd
from datetime import datetime, timedelta

class GCPCostOptimizer:
    """Automated cost optimization for GCP"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        self.compute_client = compute_v1.InstancesClient()
        self.recommender_client = recommender_v1.RecommenderClient()
        
    def analyze_bigquery_costs(self, days: int = 30):
        """Analyze BigQuery costs and identify savings opportunities"""
        
        query = f"""
        SELECT
            DATE(usage_start_time) as usage_date,
            service.description as service,
            sku.description as sku,
            project.id as project_id,
            SUM(cost) as total_cost,
            SUM(usage.amount) as usage_amount,
            usage.unit as usage_unit,
            location.region as region
        FROM `{self.project_id}.billing_export.gcp_billing_export_*`
        WHERE service.description = 'BigQuery'
            AND DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
        GROUP BY usage_date, service, sku, project_id, usage_unit, region
        ORDER BY total_cost DESC
        """
        
        df = self.bq_client.query(query).to_dataframe()
        
        # Identify expensive queries
        expensive_queries = df[df['sku'].str.contains('Analysis|Streaming')]
        
        recommendations = []
        
        # Check for partition pruning opportunities
        if expensive_queries['total_cost'].sum() > 1000:
            recommendations.append({
                'category': 'BigQuery',
                'issue': 'High query analysis costs',
                'recommendation': 'Implement partition pruning and clustering',
                'potential_savings': expensive_queries['total_cost'].sum() * 0.4
            })
        
        # Check for storage optimization
        storage_costs = df[df['sku'].str.contains('Storage')]
        
        if storage_costs['total_cost'].sum() > 500:
            recommendations.append({
                'category': 'BigQuery',
                'issue': 'High storage costs',
                'recommendation': 'Implement table expiration and archive old data',
                'potential_savings': storage_costs['total_cost'].sum() * 0.3
            })
        
        return recommendations
    
    def optimize_compute_instances(self):
        """Rightsize and schedule compute instances"""
        
        # Get all instances
        instances = self.compute_client.aggregated_list(project=self.project_id)
        
        recommendations = []
        
        for zone, instance_list in instances:
            if not instance_list.instances:
                continue
            
            for instance in instance_list.instances:
                # Get CPU utilization metrics
                utilization = self.get_instance_utilization(instance.name, zone)
                
                if utilization['avg_cpu'] < 20:  # Underutilized
                    current_machine = instance.machine_type.split('/')[-1]
                    recommended_machine = self.recommend_smaller_machine(current_machine)
                    
                    recommendations.append({
                        'category': 'Compute Engine',
                        'instance': instance.name,
                        'current': current_machine,
                        'recommended': recommended_machine,
                        'potential_savings': self.calculate_savings(current_machine, recommended_machine)
                    })
                
                # Check for idle instances
                if utilization['avg_cpu'] < 5 and utilization['network_bytes'] < 1000000:
                    recommendations.append({
                        'category': 'Compute Engine',
                        'instance': instance.name,
                        'issue': 'Idle instance detected',
                        'recommendation': 'Delete or stop instance',
                        'potential_savings': self.get_instance_monthly_cost(instance.machine_type)
                    })
        
        return recommendations
    
    def optimize_storage_lifecycle(self):
        """Implement intelligent storage tiering"""
        
        from google.cloud import storage
        
        storage_client = storage.Client()
        
        recommendations = []
        
        for bucket in storage_client.list_buckets():
            # Analyze blob access patterns
            blobs = list(bucket.list_blobs())
            
            old_blobs = [
                b for b in blobs 
                if (datetime.now() - b.time_created).days > 30
            ]
            
            if old_blobs:
                # Calculate potential savings by moving to Nearline/Coldline
                total_size_gb = sum([b.size for b in old_blobs]) / (1024**3)
                
                # Standard: $0.020/GB, Nearline: $0.010/GB, Coldline: $0.004/GB
                current_cost = total_size_gb * 0.020
                nearline_cost = total_size_gb * 0.010
                
                recommendations.append({
                    'category': 'Cloud Storage',
                    'bucket': bucket.name,
                    'issue': f'{len(old_blobs)} objects older than 30 days in Standard storage',
                    'recommendation': 'Move to Nearline or Coldline storage',
                    'potential_savings': current_cost - nearline_cost
                })
                
                # Auto-apply lifecycle policy
                self.apply_lifecycle_policy(bucket.name)
        
        return recommendations
    
    def apply_lifecycle_policy(self, bucket_name: str):
        """Apply lifecycle management to bucket"""
        
        from google.cloud import storage
        
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        
        rule = storage.lifecycle.LifecycleRule(
            action=storage.lifecycle.SetStorageClass("NEARLINE"),
            condition=storage.lifecycle.Age(30)
        )
        
        rule2 = storage.lifecycle.LifecycleRule(
            action=storage.lifecycle.SetStorageClass("COLDLINE"),
            condition=storage.lifecycle.Age(90)
        )
        
        rule3 = storage.lifecycle.LifecycleRule(
            action=storage.lifecycle.Delete(),
            condition=storage.lifecycle.Age(365)
        )
        
        bucket.lifecycle_rules = [rule, rule2, rule3]
        bucket.patch()
        
        print(f"Applied lifecycle policy to {bucket_name}")
    
    def get_recommender_insights(self):
        """Get Google Cloud Recommender suggestions"""
        
        parent = f"projects/{self.project_id}/locations/global/recommenders/google.compute.instance.MachineTypeRecommender"
        
        recommendations = []
        
        for recommendation in self.recommender_client.list_recommendations(parent=parent):
            recommendations.append({
                'name': recommendation.name,
                'description': recommendation.description,
                'primary_impact': recommendation.primary_impact,
                'state': recommendation.state
            })
        
        return recommendations
    
    def generate_cost_report(self):
        """Generate comprehensive cost optimization report"""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_id': self.project_id,
            'recommendations': []
        }
        
        # Collect all recommendations
        report['recommendations'].extend(self.analyze_bigquery_costs())
        report['recommendations'].extend(self.optimize_compute_instances())
        report['recommendations'].extend(self.optimize_storage_lifecycle())
        report['recommendations'].extend(self.get_recommender_insights())
        
        # Calculate total potential savings
        total_savings = sum([
            r.get('potential_savings', 0) 
            for r in report['recommendations']
        ])
        
        report['total_potential_monthly_savings'] = total_savings
        
        # Write report to BigQuery
        df = pd.DataFrame(report['recommendations'])
        
        df.to_gbq(
            destination_table=f'{self.project_id}.cost_optimization.recommendations',
            project_id=self.project_id,
            if_exists='append'
        )
        
        return report

# Usage
optimizer = GCPCostOptimizer(project_id='my-project')
report = optimizer.generate_cost_report()

print(f"Total potential monthly savings: ${report['total_potential_monthly_savings']:.2f}")
```

**BigQuery Cost Controls:**

```sql
-- Set max bytes billed for queries
CREATE OR REPLACE PROCEDURE enforce_query_limits()
BEGIN
  -- Set project-level quota
  ALTER PROJECT `my-project`
  SET OPTIONS (
    max_bytes_billed = 1099511627776  -- 1 TB
  );
END;

-- Create materialized view for frequently queried data
CREATE MATERIALIZED VIEW data_warehouse.customer_summary
PARTITION BY DATE(last_updated)
CLUSTER BY customer_id
AS
SELECT
  customer_id,
  COUNT(*) as transaction_count,
  SUM(transaction_amount) as total_spent,
  AVG(transaction_amount) as avg_transaction,
  MAX(transaction_date) as last_transaction_date,
  CURRENT_TIMESTAMP() as last_updated
FROM data_warehouse.customer_transactions
GROUP BY customer_id;

-- Use partitioned and clustered tables to reduce costs
CREATE OR REPLACE TABLE data_warehouse.transactions
PARTITION BY DATE(transaction_date)
CLUSTER BY customer_id, region
OPTIONS(
  partition_expiration_days=90,
  require_partition_filter=true
) AS
SELECT * FROM data_warehouse.raw_transactions;

-- Cost monitoring query
SELECT
  user_email,
  query,
  ROUND(total_bytes_billed / 1024 / 1024 / 1024, 2) as gb_billed,
  ROUND(total_slot_ms / 1000 / 60 / 60, 2) as slot_hours,
  ROUND(total_bytes_billed / 1024 / 1024 / 1024 * 5 / 1000, 2) as estimated_cost_usd,
  creation_time
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND state = 'DONE'
  AND total_bytes_billed > 0
ORDER BY total_bytes_billed DESC
LIMIT 100;
```

**Committed Use Discounts and Reservations:**

```bash
# Purchase committed use discount for BigQuery
gcloud beta compute commitments create bigquery-commitment \
    --region=us-central1 \
    --plan=12-month \
    --resources=slots=500 \
    --auto-renew

# Purchase committed use for Compute Engine
gcloud compute commitments create compute-commitment \
    --region=us-central1 \
    --resources=vcpu=100,memory=400GB \
    --plan=12-month

# Create BigQuery reservation
bq mk \
    --project_id=${PROJECT_ID} \
    --location=us-central1 \
    --reservation \
    --slots=500 \
    --ignore_idle_slots=false \
    prod-reservation

# Assign reservation to project
bq mk \
    --project_id=${PROJECT_ID} \
    --location=us-central1 \
    --reservation_assignment \
    --reservation_id=projects/${PROJECT_ID}/locations/us-central1/reservations/prod-reservation \
    --job_type=QUERY \
    --assignee_type=PROJECT \
    --assignee_id=${PROJECT_ID}
```

---

## Networking

## Networking

### Network Configuration & Security

##### Q. Service Endpoint vs Private Endpoint?

**Azure Private Link (Private Endpoint):**
- Access PaaS over private IP within VNet
- Gets new private IP on VNet
- Traffic stays within VNet
- Inbuilt data protection
- Extensible for on-premises via ExpressRoute/VPN
- Additional resource to manage
- Cost based on traffic and runtime
- Blocks all internet traffic to resource

**Azure Service Endpoint:**
- Secure connectivity over Azure backbone
- Traffic leaves VNet to public endpoint
- Publicly routable IP remains
- Not easily restricted for on-premises
- Simpler implementation
- No additional cost
- Only secures to Azure VNet

##### Q. Public vs Private networking?

**Public Networking:**
- Internet-accessible
- Public IP addresses
- Less secure (requires firewalls, encryption)

**Private Networking:**
- Organization/group restricted
- Private IP addresses
- Not directly internet-accessible
- More secure (internal security, controlled access)

##### Q. Connect bastion host to private network?

1. **Deploy Bastion Host:**
   - Place in public subnet
   - Configure security groups (SSH/RDP from trusted IPs)

2. **Access Private Resources:**
   - Place resources in private subnets
   - Configure security groups allowing bastion traffic

3. **SSH/RDP into Bastion:**
   - Connect from local machine to bastion

4. **Access Private Instances:**
   - SSH tunnel through bastion to private IPs

##### Q. What is VPC?
Logically isolated network in cloud with:
- Custom IP address ranges
- Subnets (public/private)
- Internet Gateway (IGW)
- NAT Gateway/Instance
- Route Tables
- Security Groups
- Network ACLs

##### Q. What is VPC Peering?
Enables communication between two VPCs using private IPs:
1. Create peering connection
2. Update route tables in both VPCs
3. Configure security groups/NACLs
4. Private communication without public IPs

##### Q. What is load balancer?
Distributes incoming traffic across multiple servers for:
- Increased availability
- Scalability
- Improved performance
- Health monitoring
- Fault tolerance
- SSL termination
- Geographic distribution

##### Q. What is Cloud NAT?
Managed service enabling private instances to access internet without exposing private IPs:
- Managed by cloud provider
- Security (prevents inbound connections)
- Automatic scaling
- Cost-efficient
- High availability

##### Q. Load Balancer vs Cloud NAT Gateway?

**Load Balancer:**
- Distributes incoming traffic
- Layer 4 (TCP/UDP)
- Health monitoring
- Scalability and fault tolerance
- SSL termination
- Session persistence

**Cloud NAT Gateway:**
- Handles outbound traffic
- Private IP masking
- Managed service
- Security (no inbound access)
- Automatic scaling
- High availability

##### Q. Secure way to manage sensitive information?
1. Use Secrets Manager
2. Encrypt data (rest and transit)
3. Implement access controls
4. Automate secret rotation
5. Audit and monitor access
6. Use environment variables
7. Secure backup/recovery
8. Regular security assessments

##### Q. What is secrets manager?
Tool for securely storing, managing, and accessing:
- Passwords
- API keys
- Encryption keys
- Confidential data

**Features:**
- Secure encrypted storage
- Access control
- Automated rotation
- Audit and monitoring

##### Q. Networking setup rules?

**1. Network Segmentation:**
- VPCs and subnets
- Network ACLs and security groups

**2. Access Control:**
- Least privilege principle
- Private connectivity

**3. Performance:**
- Load balancers
- DNS configuration

**4. High Availability:**
- Multi-AZ deployments
- Failover mechanisms

**5. Monitoring:**
- Network monitoring tools
- Traffic logging

**6. Compliance:**
- Industry standards
- Regular patching

**7. Scalability:**
- Auto-scaling
- Elastic IPs

##### Q. Deny traffic from specific IP for AKS pod?
Using NACL deny rule.

##### Q. Create private or public subnet?
- **Private:** Routing table without internet gateway
- **Public:** Routing table with internet gateway

##### Q. SGID, SUID, Sticky Bit, ACL commands?

**SUID (Set User ID):**
- Run programs as file owner
- Value: 4 or u+s
```bash
chmod 4775 um.sh
chmod u+s um.sh
```

**SGID (Set Group ID):**
- Inherit group ownership
- Value: 2 or g+s
```bash
chmod 2775 /data
chmod g+s /data
```

**Sticky Bit:**
- Only owner can delete file
- Value: 1 or +t
```bash
chmod 1775 /tmp
chmod +t /tmp
```

**ACL (Access Control List):**
```bash
# Check ACL
getfacl

# Set ACL
setfacl -R -m d:g:marketing:rw acl/
setfacl -R -m user:geeko:rwx,group:mascots:rwx mydir/
```

---

## Python Programming

### Python Scripting & Development

##### Q. Exception handling keywords?
- **try:** Code that might cause exception
- **catch:** Handle exception
- **else:** Execute if no exception
- **finally:** Execute regardless of exception

##### Q. What is *args in function?
Allows any number of arguments as tuple.
```python
def sum(*args):
    return sum(args)
```

##### Q. What is **kwargs in function?
Allows any number of keyword arguments as dictionary.
```python
def sum(**kwargs):
    return sum(kwargs.values())
```

##### Q. What is list comprehension?
Concise way to create lists:
```python
# Copy listA to listB with adding 1
listA = [1, 2, 3]
listB = [n + 1 for n in listA]

# With condition
l1 = ['sawan', 'muskan', 'srajan', 'vasu']
l2 = [name.upper() for name in l1 if len(name) > 5]
```

##### Q. Leap year conditions?
1. Divisible by 4
2. NOT divisible by 100 (except...)
3. OR divisible by 400

##### Q. Block scope in Python?
No block scope in Python - if/else/for/while blocks share scope with surrounding code.

##### Q. Output of print(734_529.678)?
734529.678 (underscores are ignored in numeric literals)

##### Q. Reverse string in Python?
```python
# Slicing
txt = "Hello World"[::-1]

# Loop
def reverse(s):
    str = ""
    for i in s:
        str = i + str
    return str
```

---

## Shell Scripting

### Bash & Shell Programming

##### Q. Find length of string variable?
```bash
${#string}
```

##### Q. Convert string to substring?
```bash
string="abcdef"
echo "${string:1}"      # bcdef
echo "${string:4}"      # ef
echo "${string:0:3}"    # abc
echo "${string:3:3}"    # def
echo "${string: -1}"    # f
```

##### Q. Set default value for variable?
```bash
name=${name:-'default_value'}
```

##### Q. Check if user passed value?
```bash
#!/bin/bash
: ${1:?"Please provide a variable value"}
echo "You provided: $1"
```

##### Q. Script output examples?
```bash
# Script 1
#!/bin/bash
echo ${0}  # script name
echo ${1}  # first argument
echo ${2}  # second argument

./test.sh test 20
# Output: test.sh, test, 20

# Script 2
#!/bin/bash
echo $#    # number of arguments
echo $@    # all arguments (separate)
echo $*    # all arguments (combined)

./test.sh sawan 20 21 34
# Output: 4, sawan 20 21 34, sawan 20 21 34

# Script 3
#!/bin/bash
pwd="sawan"
echo ${pwd}  # variable value
echo $(pwd)  # command output
echo `pwd`   # command output

# Output: sawan, /current/directory, /current/directory

# Script 4 - readonly
#!/bin/bash
pwd="sawan"
echo ${pwd}  # sawan
pwd="test"
echo ${pwd}  # test
readonly pwd
pwd="chouksey"  # Error: readonly variable
echo ${pwd}  # test
```

---

## DevOps Best Practices

### Professional Development & Deployment

##### Q. Benefits of Infrastructure as Code (IaC)?
- **Consistency:** Automated, identical environments
- **Efficiency:** Rapid provisioning and scaling
- **Version Control:** Live documentation
- **Cost Management:** Optimized resource use
- **Collaboration:** Shared, understandable code
- **Security:** Integrated best practices
- **Troubleshooting:** Quick diagnosis and rollback

##### Q. Ways to create IaC?

**1. Declarative Tools:**
- Terraform, AWS CloudFormation, Azure ARM templates
- Define desired state

**2. Imperative Tools:**
- Ansible, Chef, Puppet
- Define sequence of steps

**3. Configuration Management:**
- Ansible, Chef, Puppet
- Automate server configuration

**4. Containers & Orchestration:**
- Docker, Kubernetes with Helm
- Manage containerized infrastructure

**5. Serverless Frameworks:**
- AWS SAM, Serverless Framework, Azure Functions
- Deploy serverless functions

##### Q. Have you managed an application single-handedly?
Yes. Experience includes:

**Deployment & Configuration:**
- Docker containers for consistency
- Terraform for IaC
- AWS EC2 management

**CI/CD Pipeline:**
- Jenkins automation
- Automated testing
- Release management

**Monitoring & Optimization:**
- Prometheus and Grafana
- Performance tuning
- Database optimization

**Incident Management:**
- Root cause analysis
- Quick fixes
- Documentation

**Security & Compliance:**
- Regular updates
- Encryption and access controls
- Compliance audits

##### Q. End-to-end deployment process?

1. **Development:** Write and test code locally
2. **Version Control:** Commit to Git
3. **CI (Continuous Integration):**
   - Automated builds
   - Automated testing
   - Artifact creation (Docker images)
4. **CD (Continuous Delivery):**
   - Staging deployment
   - Integration testing
5. **Approval:** Code review and approval
6. **Production Deployment:**
   - Deploy using orchestration tools
   - Apply configurations
7. **Post-Deployment:**
   - Monitoring (Prometheus, Grafana)
   - Logging and analysis
   - Scaling as needed
8. **Feedback Loop:**
   - User feedback
   - Bug fixes and improvements

##### Q. Switch from EC2 to Kubernetes with Helm?

**Setup:**
1. Choose managed K8s (EKS, GKE, AKS)
2. Configure cluster

**Containerize:**
1. Dockerize microservices
2. Push to registry

**Helm Deployment:**
1. Install Helm
2. Create Helm charts
3. Deploy with Helm

**CD Tools:**
1. Argo CD, Flux, Jenkins X
2. Automate deployments

**Multiple Microservices:**
1. Separate Helm charts
2. Configure networking and service discovery
3. Use ConfigMaps/Secrets
4. Configure autoscaling
5. Implement monitoring

##### Q. Set up Nginx on server?

**1. Install:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install nginx

# CentOS/RHEL
sudo yum install epel-release && sudo yum install nginx
```

**2. Start & Enable:**
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

**3. Configure Firewall:**
```bash
# Ubuntu
sudo ufw allow 'Nginx Full'

# CentOS
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

**4. Configure:**
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

**5. Test & Restart:**
```bash
sudo nginx -t
sudo systemctl restart nginx
```

**6. SSL/TLS (Optional):**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx
```

##### Q. Challenges faced as DevOps engineer?

**1. Balancing Speed and Stability:**
- CI/CD pipelines with automated testing
- Feature flags for gradual releases
- Robust monitoring and alerts

**2. Managing Infrastructure Complexity:**
- Infrastructure as Code (Terraform, CloudFormation)
- Modularization

**3. Security and Compliance:**
- Automated security scans
- Secrets management (Vault, AWS Secrets Manager)
- Regular compliance checks

**4. Handling Scalability:**
- Auto-scaling policies
- Load balancing

**5. Effective Communication:**
- Regular cross-functional meetings
- Comprehensive documentation
- Collaborative tools (Slack, Jira)

**6. Managing Legacy Systems:**
- Incremental refactoring
- Hybrid approaches

**7. Downtime and Outages:**
- Incident response plans
- Disaster recovery strategies

**8. Cost Management:**
- Cost monitoring tools
- Resource optimization
- Cost alerts

##### Q. Real-life incident solving?

**Incident: Database Performance Degradation**

**Day 1:**
- Identified slow queries via logs/metrics
- Temporarily scaled database
- Analyzed historical data

**Day 2:**
- Profiled slow queries
- Identified missing/inefficient indexes
- Optimized queries and code
- Tested in staging
- Deployed to production

**Outcome:**
- 30% faster query performance
- Improved user experience
- Enhanced monitoring
- Better review processes

##### Q. Managing large-scale databases?

**Scaling:**
- Vertical: Increase instance size
- Horizontal: Sharding, distributed databases

**Performance:**
- Indexing optimization
- Query optimization
- Read replicas

**Management Tools:**
- Amazon RDS
- Amazon Aurora

**Real-time Backups & Replication:**
- Automated backups
- Multi-AZ deployments
- Change Data Capture (CDC)
- Monitoring and failover testing

##### Q. Data loss prevention in critical applications?

**Preventive Measures:**
- Frequent automated backups
- Geographic redundancy
- ACID compliance
- Multi-AZ deployments
- Real-time replication

**Detection & Monitoring:**
- CloudWatch monitoring
- Automated alerts
- Detailed logging

**Recovery Strategies:**
- Point-in-time recovery
- Transaction logs
- Regular DR drills
- Define RTO/RPO

**Mock DR Drill Plan:**
1. Planning (every 2-3 months)
2. Execution in non-prod
3. Evaluation and improvement
4. Documentation updates

##### Q. Cost optimization while managing resources?

**Situation:** Rising cloud costs

**Actions:**
1. Cost analysis and monitoring
2. Right-sizing resources
3. Reserved instances/savings plans
4. Storage optimization
5. Spot instances for flexible workloads
6. Cost alerts and budgeting

**Results:**
- 30% monthly cost reduction
- Improved resource efficiency
- Ongoing savings processes

##### Q. Fit for role?
Align skills and experience with role requirements:

**Technical Skills:**
- Proven expertise in CI/CD, cloud, containers, orchestration
- Problem-solving and optimization

**Project Experience:**
- Relevant past projects
- Specific achievements (reduced deployment time, improved reliability)

**Soft Skills:**
- Communication with stakeholders
- Collaboration across teams
- Adaptability to change

**Approach:**
- Initiative and proactive problem-solving
- Continuous improvement
- Efficient problem-solving

**Culture Fit:**
- Values alignment
- Team dynamics

##### Q. Blue-green deployment?
Two identical environments (blue=current, green=new):
1. Deploy new version to green
2. Test in green
3. Switch traffic to green
4. Monitor green
5. Rollback to blue if issues
6. Update blue for next cycle

**Benefits:**
- Minimal downtime
- Easy rollback
- Thorough testing
- Continuous deployment support

##### Q. Technology learned on your own?

**AWS Step Functions:**

**Learning Process:**
1. AWS documentation review
2. Online tutorials and courses
3. Hands-on practice in console
4. Sample projects

**Integration:**
1. Identified use case (ETL pipeline)
2. Designed state machine
3. Configured tasks and error handling
4. Tested thoroughly
5. Deployed via CI/CD
6. Monitored with CloudWatch

**Outcome:**
- Streamlined workflows
- Better visibility
- Enhanced automation

##### Q. What is DevOps?
Gray area between Dev and Ops emphasizing:
- Communication
- Integration
- Collaboration
- Rapid and continuous deployment
- Eliminates silos

##### Q. What is webhook in Git?
HTTP POST request triggered by subscribed events, sent to defined URL endpoint.

##### Q. What is Checkpoint (Nomad)?
HashiCorp service for update checks and security bulletins. Uses anonymous information only. Optional and can be disabled.

##### Q. OS version and kernel?
```bash
# Kernel version
uname -r

# Kernel release details
uname -a

# Alternative
cat /proc/version

# Linux OS version
cat /etc/os-release
lsb_release -a
```

---

## Security & Compliance

### Security Best Practices

##### Q. Cyberattack precautions?

1. **Security Best Practices:** Secure coding, regular reviews, industry standards
2. **Access Controls:** RBAC, least privilege
3. **Encryption:** Data at rest and in transit
4. **Regular Updates:** Latest security patches
5. **Monitoring & Alerts:** Detect suspicious activity
6. **Backup & Recovery:** Regular backups, tested recovery
7. **Training:** Security awareness for team

---

## HashiCorp Nomad

### Workload Orchestration

##### Q. Is Nomad eventually or strongly consistent?
Uses both:
- **Consensus protocol:** Strongly consistent (state replication, scheduling)
- **Gossip protocol:** Manages server addresses (clustering, federation)

All Nomad-managed data is strongly consistent.

##### Q. Nomad datacenter vs Consul datacenter?
- **Nomad datacenter:** Equivalent to region, can have multiple datacenters
- **Consul datacenter:** More equivalent to Nomad region

Nomad supports two-tier approach; Consul relies on federation.

##### Q. What is bootstrapping a Nomad cluster?
Process of electing first leader and writing initial cluster state. Occurs when `bootstrap_expect` servers connect. Options like `default_scheduler_config` only affect initial bootstrap.

If state destroyed on all servers, cluster re-bootstraps with defaults.

---

## Additional Resources

### Key Takeaways

#### Configuration Management
- Ansible for automation and idempotency
- Version control for infrastructure
- Environment-specific configurations

#### Containerization
- Docker for consistent environments
- Image optimization and security
- Volume and network management

#### Orchestration
- Kubernetes for container orchestration
- Scaling strategies (horizontal/vertical)
- High availability and self-healing

#### Infrastructure as Code
- Terraform for cloud-agnostic IaC
- State management and locking
- Modular and reusable configurations

#### Version Control
- Git workflows and branching strategies
- Conflict resolution
- Large file handling (LFS)

#### CI/CD
- Jenkins for automation
- Pipeline as code
- Automated testing and deployment

#### Cloud Platforms
- AWS services (Lambda, ECS, EKS, RDS)
- Azure services (AKS, Key Vault, Front Door)
- Multi-cloud strategies

#### Monitoring & Observability
- Prometheus and Grafana
- CloudWatch, ELK Stack
- Alerting and incident response

#### Security
- Secrets management
- Encryption and access control
- Compliance and auditing

#### Best Practices
- Automation first
- Infrastructure as code
- Continuous improvement
- Documentation and collaboration

---

### Support

**If you find this content useful, you can support by buying me a coffee:**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support! 💚
