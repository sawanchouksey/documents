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

### Intermediate/Advanced Kubernetes Scenarios

##### Q. How do you implement blue-green or canary deployments in AKS using Helm or service mesh (e.g., Istio)?
- **Canary with Istio:** Deploy two versions of the app (v1 and v2). Define an Istio `VirtualService` configured to route 90% of traffic to the `v1` subset and 10% to the `v2` subset based on weights. Gradually increase v2 weight to 100%.
- **Blue-Green with Native K8s/Helm:** Deploy the "Green" namespace/deployment alongside the active "Blue" one. Run tests against Green internally. Once validated, update the main Kubernetes Service selector from `version: blue` to `version: green`, switching traffic instantly.

##### Q. What are liveness and readiness probes? Give a practical example of how incorrect config can lead to downtime.
- **Liveness Probe:** Checks if the container is alive or dead. If it fails, `kubelet` restarts the container.
- **Readiness Probe:** Checks if the app is ready to serve traffic. If it fails, the pod is removed from the Service endpoints, stopping routing.
- **Failure Example:** If a readiness probe is misconfigured with a timeout shorter than the DB connection latency, the pod keeps getting detached from the service. If a liveness probe checks a heavy backend dependency, a minor DB latency spike might cause Kubernetes to restart all your API pods simultaneously, triggering a complete outage.

##### Q. How do you securely manage secrets and certificates in AKS using Azure Key Vault and CSI drivers?
- Use the **Azure Key Vault Provider for Secrets Store CSI Driver**.
- Instead of Kubernetes Native Secrets (which are just base64 encoded by default), the CSI driver actively pulls secrets, keys, and certs from Azure Key Vault and mounts them into the pod's file system as a volume.
- Authenticate pods explicitly to the Key Vault using **Microsoft Entra Workload ID**, avoiding the injection of any storage or client credentials inside Kubernetes.

---



### Advanced Troubleshooting & Architecture

##### Q. You’ve deployed an app to Azure Kubernetes Service (AKS) and it fails health checks randomly. How do you debug this end-to-end?
**Answer:**
1. **Probe Configuration:** Validate the liveness/readiness probe timeouts and delays. If an application needs 30 seconds to warm up but the initial delay is 5 seconds, it will enter a crash loop.
2. **Resource Throttling:** Run `kubectl top pods` and check `kubectl describe pod`. If CPU limits are too strict, the app might be throttling, causing health check endpoints to respond too slowly and fail.
3. **Application Logs:** Check `kubectl logs <pod-name> --previous` to see why the container crashed before the restart.
4. **Network/SNAT:** In AKS, check if the Node is suffering from SNAT port exhaustion when making outbound calls to a database, causing intermittent application-level hangs which fail the health probe.

##### Q. In a canary deployment to production, half the traffic returns 502, while others succeed. Walk us through your troubleshooting approach.
**Answer:**
A 502 Bad Gateway means the proxy (Ingress/Service Mesh) cannot route to the backend Canary pods.
1. **Isolate Endpoints:** Use `kubectl get endpoints <service-name>` to verify if the Canary pods are actually registering as healthy endpoints.
2. **Readiness Probes:** If the readiness probe is flapping (passing, failing, passing), the endpoints are rapidly being added and removed from the active service pool, leading to intermittent 502s.
3. **Ingress Config:** Check the NGINX/Istio routing rules. Ensure the Canary weight configuration points to the correct, existing Service port.
4. **App Dependencies:** The Canary deployment might be missing a critical environment variable/secret, causing it to crash immediately upon receiving traffic.

##### Q. You see high CPU usage in one pod, but logs look clean. What next?
**Answer:**
1. **Resource Check:** Verify the requests/limits with `kubectl describe pod`. Check metrics with `kubectl top pod`.
2. **Exec into Pod:** `kubectl exec -it <pod-name> -- /bin/sh` or bash.
3. **Profiling:** If it's a Java app, use `jstack` or JVM Thread Dumps. For Python, use `py-spy`. For Node, run a CPU profiler. You need a flame graph to identify which function is spinning.
4. **Common Causes:** Often caused by an infinite loop, a deadlock, GC (Garbage Collection) heavy thrashing (when memory is near limits, CPU spikes to clean it), or a busy-wait network thread.

##### Q. A user reports 10-second delays every 15 minutes in an app running on AKS. No code changes happened. How would you begin RCA?
**Answer:**
Predictable, timed latency spikes usually point to infrastructure or background batch jobs.
1. **CronJobs / DaemonSets:** Check if a heavy Kubernetes CronJob, or a DaemonSet (like a Log Analytics agent or Prometheus scraper), runs every 15 minutes, stealing CPU/IOPS from the node.
2. **Garbage Collection:** Check the language runtime GC logs. Massive memory cleanups can cause "Stop-the-World" pauses.
3. **IOPS Throttling:** Check Azure Monitor metrics for the underlying AKS VMSS (Virtual Machine Scale Set). If the node hits its Azure disk IOPS limit, storage read/writes will queue up and cause huge latency spikes.

##### Q. How would you set up an automated rollback strategy in Kubernetes for failed deployments?
**Answer:**
- **Helm:** Use the `--atomic` and `--timeout` flags during `helm upgrade`. If the pods do not reach a ready state within the timeout, Helm automatically rolls back the entire release to the previous revision.
- **GitOps (ArgoCD/Flux):** Enable automated self-healing. If a degraded state is detected via health checks, it halts the rollout sync.
- **Progressive Delivery (Flagger/Istio):** Automate canary rollouts where Flagger queries Prometheus for HTTP 500 errors or latency metrics. If the error rate breaches a threshold during the canary test, Flagger automatically halts and routes 100% of traffic back to the primary deployment.

##### Q. What’s your approach to disaster recovery for stateful apps running on containers?
**Answer:**
State is the hardest part of container DR.
1. **Externalize State:** Prefer utilizing managed PaaS databases (like Azure Cosmos DB or PostgreSQL) outside the AKS cluster with active geo-replication.
2. **Volume Snapshots:** If state *must* be in Kubernetes (PV/PVCs), use the CSI (Container Storage Interface) driver to take scheduled Azure Disk snapshots.
3. **Backup Tools:** Utilize **Velero** or **Kasten K10**. Velero backs up all Kubernetes manifests (Deployments, Services) and triggers cloud-native snapshotting of Persistent Volumes, storing everything in Azure Blob Storage in a completely different region for cross-region DR cluster restores.


##### Q. Your EKS pods are crashing with “out of memory” errors (OOMKilled). How do you troubleshoot?
**Answer:** I’d describe the pod to confirm the Exit Code is 137 (OOMKilled). Then, I'd check the pod’s resource limits in the deployment spec. If the limits are too low, I’d adjust the memory requests and limits to match the actual workload using metrics from `kubectl top pod`. If there's a memory leak in the application, I'd capture memory dumps for the developers to analyze.

##### Q. How would you prevent developers from accidentally creating LoadBalancer services in a production environment?
**Answer:** Kubernetes RBAC alone cannot restrict specific fields within a Service object (like `type: LoadBalancer`). I would enforce this using **Dynamic Admission Control** tools like **OPA Gatekeeper** or **Kyverno**. I would write a policy mapping that explicitly denies the creation of Service resources where `spec.type == "LoadBalancer"` in the `production` namespace, forcing developers to use `ClusterIP` and an Ingress controller for external exposure.

##### Q. Your Kubernetes HPA (Horizontal Pod Autoscaler) is not scaling down even when CPU usage is low. What could be the root causes?
**Answer:**
1. **Cooldown/Delay Policies:** By default, HPA has a `scaleDown` stabilization window (often 5 minutes) to prevent thrashing. It won't scale down immediately.
2. **Missing Metrics:** The metrics-server might be degraded or pods aren't emitting CPU metrics properly.
3. **Minimum Replicas:** The `minReplicas` threshold in the HPA might already be reached.
4. **Unready/Deleted Pods:** If pods are stuck in terminating or unready states, HPA struggles to calculate the average utilization correctly.
5. **Pod Disruption Budgets (PDB):** PDBs might be restricting the eviction of pods, physically blocking the scale-down event.

##### Q. You are required to perform maintenance on a node without causing service disruption. How would you safely drain the node and ensure high availability?
**Answer:**
1. **Cordon:** First, I would run `kubectl cordon <node-name>` to mark the node as unschedulable, ensuring no new pods are placed on it.
2. **Drain:** I would execute `kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data`.
3. **PDBs:** High availability is guaranteed by configuring **Pod Disruption Budgets (PDBs)** on critical deployments (e.g., `minAvailable: 2`). `kubectl drain` intrinsically respects PDBs, moving pods gracefully to other nodes one-by-one without breaching the application's availability threshold.

##### Q. How do you manage secrets securely in your CI/CD pipelines? Compare the use of Kubernetes Secrets vs external vault systems like HashiCorp Vault or AWS Secrets Manager.
**Answer:**
Standard Kubernetes Secrets are just Base64 encoded strings stored in etcd, meaning anyone with cluster admin access can decode them. 
- **Kubernetes Secrets:** Best for low-level configurations (like TLS certs generated by cert-manager) where simplicity is key. To secure them, etcd encryption at rest must be enabled.
- **External Vaults (HashiCorp Vault / AWS Secrets Manager):** Mandatory for enterprise security. They provide dynamic secret generation, audit logging, automatic rotation, and strict RBAC. I integrate them into Kubernetes using the **Vault Agent Sidecar** or the **CSI Secrets Store Provider**, which maps external secrets into the pod as ephemeral memory volumes, completely bypassing Kubernetes etcd storage.

##### Q. How do you enforce resource quotas, image scanning, and prevent the creation of certain Kubernetes services in production?
**Answer:**
- **Resource Quotas:** Applied natively using `ResourceQuota` objects at the namespace level (restricting total CPU/Mem) and `LimitRange` objects (setting defaults per pod).
- **Service Prevention:** Enforced via Mutating/Validating Admission Webhooks utilizing OPA Gatekeeper or Kyverno (e.g., rejecting `NodePort` or `LoadBalancer`).
- **Image Scanning Policies:** Integrating an ImagePolicyWebhook tied to a container security platform (like Trivy, Aqua, or Prisma Cloud) that intercepts the deployment request and mathematically rejects applying the pod if the image digest has critical CVE vulnerabilities in the registry.

##### Q. How would you manage application rollouts across multiple Kubernetes clusters in different environments?
**Answer:**
Managing multi-cluster topology using imperative `kubectl` scripts does not scale. I would adopt a **GitOps paradigm using ArgoCD or Flux**.
For multi-cluster rollouts specifically, I would use **ArgoCD ApplicationSets**. They dynamically define deployments across multiple clusters based on label selectors or external registries. I would logically group clusters (e.g., `env=staging`, `env=production`) and allow ApplicationSets to orchestrate the rendering of Helm charts recursively to targets based on those centralized Git definitions.

##### Q. A recent CI/CD job left orphaned resources in your cluster. What measures can you take to avoid such inconsistencies?
**Answer:**
Orphaned resources (like dangling ConfigMaps or unused Services) occur when CI drops imperative `kubectl apply` commands. 
- **Helm:** Use Helm packages which group resources logically into a "Release". A `helm uninstall` cleanly removes dependencies.
- **GitOps (ArgoCD/Flux):** GitOps controllers constantly reconcile the live cluster state against the Git repository. If you enable `Prune: true` in ArgoCD, any resource existing in the cluster but removed from Git is automatically isolated and safely deleted, ensuring zero configuration drift.

##### Q. Your Kubernetes cluster’s autoscaler is launching too many nodes during peak hours, causing budget concerns. How do you control autoscaling more efficiently?
**Answer:**
1. **Cluster Autoscaler Limits:** Enforce strict maximum nodepool sizes in the provider (e.g., max 10 nodes for the compute nodepool).
2. **Pod Over-Provisioning:** Review pod CPU/Memory *Requests*. Often, developers inflate requests artificially, causing the scheduler to bin-pack inefficiently and demand unnecessary nodes.
3. **Spot Instances:** Shift stateless, fault-tolerant workloads to a secondary nodepool running heavily discounted Spot VMs to slash costs.
4. **Karpenter:** Replace the standard Cluster Autoscaler with **Karpenter** (on AWS), which dynamically provisions right-sized nodes on demand tailored exactly to the pending pods' requirements, heavily optimizing bin-packing and cost.

##### Q. You are designing a multi-region Kubernetes disaster recovery strategy for a regulated enterprise. How do you plan backup, failover, and restoration?
**Answer:**
1. **Stateless Components:** 100% of Kubernetes manifests (Deployments, Services, Ingresses) are stored in a Git repository hosted outside the clusters (e.g., GitHub). **ArgoCD** runs in both the Primary and Secondary regions, actively syncing the identical state.
2. **Stateful Data (Databases):** All critical state is offloaded to managed Cloud Databases (e.g., AWS Aurora, Cosmos DB) utilizing native Active-Passive or Active-Active geo-replication across the two regions.
3. **Stateful Data (PV/PVCs):** For unavoidable cluster state, **Velero** is scheduled to take CSI volume snapshots and back up ETCD data, replicating it into cross-region blob storage buckets daily.
4. **Failover:** Managed via a global load balancer (e.g., Azure Front Door or AWS Route53). If Region A drops, Route53 health checks trip, failing over DNS instantly to the pre-warmed Region B ArgoCD cluster processing the active replica databases.


### Deep Dive Troubleshooting & System Design

##### Q. Your pod keeps getting stuck in CrashLoopBackOff, but logs show no errors. How would you approach debugging and resolution?
**Answer:**
If `kubectl logs <pod-name>` is empty, the application is crashing before the logging framework initializes, or the container runtime drops the log.
1. **Container Exit Code:** Run `kubectl describe pod <pod-name>`. Check the numeric `Exit Code` in the `State` block. 
   - `Exit Code 137:` OOMKilled by the node (memory limits exceeded).
   - `Exit Code 1:` Application specific fatal error.
   - `Exit Code 255:` Entrypoint execution failure (e.g., shell script format/permissions).
2. **Missing Dependencies/Commands:** The `command` or `args` in the pod spec might be trying to execute a binary that doesn't exist in the container image, failing silently at the OS layer.
3. **Misconfigured Probes:** A deeply misconfigured initial delay on a Liveness probe might be killing the pod forcefully via `SIGKILL` before the application finishes booting and writing to stdout.

##### Q. You have a StatefulSet deployed with persistent volumes, and one of the pods is not recreating properly after deletion. What could be the reasons, and how do you fix it without data loss?
**Answer:**
StatefulSets ensure strict deployment ordering. Pod `web-1` will remain stuck in `Pending` if its underlying volume cannot be securely attached.
1. **Volume Attachment Limits:** The cloud provider (e.g., Azure/AWS) might have hit maximum disk attachments per VM node.
2. **Node Affinity/Availability Zones:** If `web-1`'s Persistent Volume Claim (PVC) was provisioned in `AZ-A`, but `AZ-A` lacks compute capacity, Kubernetes cannot schedule the pod in `AZ-B` because volumes cannot cross zones.
3. **Stuck VolumeAttachments:** The old pod's volume might be stuck in a "Terminating" state on the storage controller. 
**Fix:** Never delete the PVC. Delete the stuck `VolumeAttachment` object or forcefully detach the disk via the Cloud Provider console. Once freed, the Kubelet will attach the disk to the new node and successfully spin up the pod with zero data loss.

##### Q. Your cluster autoscaler is not scaling up even though pods are in Pending state. What would you investigate?
**Answer:**
1. **Maximum Node Group Limits:** The Cluster Autoscaler might have already reached the `max-nodes` threshold defined on the cloud provider's scale set (ASG/VMSS).
2. **Pod Scheduling Constraints:** The Pending pods might have impossible requests. E.g., a pod requesting a GPU (`nvidia.com/gpu: 1`), but the node group is configured for generic CPU instances. Alternatively, strict Pod Anti-Affinity rules are preventing scheduling on newly created nodes.
3. **Missing Tolerations:** The autoscaling node groups might have Taints attached to them, but the Pending pod lacks the corresponding Tolerations, meaning the Autoscaler analyzes the request and realizes spinning up a node won't help anyway.

##### Q. A network policy is blocking traffic between services in different namespaces. How would you design and debug the policy to allow only specific communication paths?
**Answer:**
**Design:** By default, Kubernetes allows all cross-namespace traffic. Activating a "Default Deny" policy isolates the namespace. To allow specific cross-namespace ingress:
```yaml
ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: frontend-namespace
      podSelector:
        matchLabels:
          app: frontend-app
```
**Debug:** I would deploy a lightweight `netshoot` or `busybox` pod in the source namespace. I would attempt `curl` and `telnet` connections. If it times out, the Network Policy dropped it. In enterprise clusters using CNI plugins like Calico or Cilium, I would enable their network flow logs or Hubble UI to visually verify exactly which policy rule rejected the packet.

##### Q. One of your microservices has to connect to an external database via a VPN inside the cluster. How would you architect this in Kubernetes with HA and security in mind?
**Answer:**
Running VPN clients inside application pods is an anti-pattern (creates massive privilege escalation risks).
**Architecture:** 
1. Deploy a dedicated, highly available Egress VPN Gateway workload (like strongSwan or WireGuard) as a `Deployment` in a dedicated `egress-system` namespace.
2. Expose the VPN Deployment internally using a standard `ClusterIP` Service.
3. Create an `ExternalName` Service or a headless service without selectors in the application namespace pointing directly to the VPN internal Service.
4. Route all traffic destined for the external database through this central Egress deployment. This centralizes encryption, minimizes the blast radius of privileged containers, and allows standard Horizontal Pod Autoscaling of the VPN gateways without touching application logic.

##### Q. You're running a multi-tenant platform on a single EKS cluster. How do you isolate workloads and ensure security, quotas, and observability for each tenant?
**Answer:**
"Hard Multi-tenancy" is notoriously difficult in Kubernetes.
1. **Namespaces & RBAC:** Each tenant gets a dedicated namespace. Strict RBAC ensures Tenant A cannot view Tenant B's secrets or pods.
2. **Resource Quotas & Limit Ranges:** Prevent "Noisy Neighbors" by strictly enforcing `ResourceQuotas` at the namespace level so Tenant A cannot exhaust cluster CPU/RAM.
3. **Network Policies:** Implement a strict "Default Deny" policy preventing any cross-namespace East-West traffic. 
4. **Node Isolation (Optional):** Use Node Taints and Pod Tolerations to physically schedule Tenant A's pods onto dedicated worker nodes, preventing kernel-level shared cache snooping.
5. **Observability:** Use PromQL label filtering (e.g., metric federation) to ensure each tenant's Grafana dashboard exclusively queries time-series data tagged with their `namespace` label.

##### Q. You notice the kubelet is constantly restarting on a particular node. What steps would you take to isolate the issue and ensure node stability?
**Answer:**
1. **Check OS Logs:** The kubelet is a systemd service, so I would SSH into the node and run `journalctl -u kubelet -f` to catch the exact panic or stack trace.
2. **Resource Starvation (OOM):** The underlying node might be running entirely out of memory, causing the Linux out-of-memory (OOM) killer to execute, targeting the kubelet process. Ensuring `kube-reserved` and `system-reserved` memory allocations are properly configured prevents OS starvation.
3. **Certificate Rotation Failures:** Kubelet client certificates have expiration dates. If the kubelet failed to auto-rotate its cert with the API Server, it will repeatedly fail TLS handshakes and restart in a crash loop.
4. **Container Runtime Unreachable:** If the Docker/containerd socket hangs, the kubelet will repeatedly restart attempting to reconnect.

##### Q. A critical pod in production gets evicted due to node pressure. How would you prevent this from happening again, and how do QoS classes play a role?
**Answer:**
Kubernetes uses **Quality of Service (QoS)** classes to dictate which pods get murdered first when a node hits memory/disk pressure.
- **BestEffort:** Pods without any CPU/Memory definitions. (Evicted First).
- **Burstable:** Pods with Requests defined, but Limits missing or set higher than Requests. (Evicted Second).
- **Guaranteed:** Pods where CPU/Memory `requests` match exactly equal to their `limits`. (Evicted Last).
**Prevention:** To protect a critical pod from eviction, I would configure its CPU and memory requests to *exactly equal* its limits, guaranteeing it receives the `Guaranteed` QoS class. This ensures Kubernetes will sacrifice all other BestEffort and Burstable workloads on the node before ever touching the critical pod.

##### Q. You need to deploy a service that requires TCP and UDP on the same port. How would you configure this in Kubernetes using Services and Ingress?
**Answer:**
1. **Service Configuration:** Kubernetes supports mixed protocols on the same `Service` (if the feature gate is enabled or newer versions). You simply define two ports in the YAML: one with `protocol: TCP` and one with `protocol: UDP`, both mapping to the exact same `targetPort`.
2. **Ingress Limitations:** Native Kubernetes `Ingress` objects are strictly Layer 7 (HTTP/HTTPS) only. An Ingress cannot route non-HTTP UDP traffic. 
3. **Workaround:** To expose it externally, I would configure the Ingress Controller's underlying deployment directly. For NGINX Ingress, I would map the specific external TCP/UDP ports via the `--tcp-services-configmap` and `--udp-services-configmap` flags to route the Layer 4 traffic directly into the cluster, completely bypassing standard Layer 7 Ingress resources.

##### Q. An application upgrade caused downtime even though you had rolling updates configured. What advanced strategies would you apply to ensure zero-downtime deployments next time?
**Answer:**
Rolling updates alone do not guarantee zero downtime. Downtime happens if traffic is sent to a pod before it's ready, or if in-flight connections are violently severed during scale-down.
1. **Strict Readiness Probes:** Ensure readiness probes meticulously validate database connections and deep endpoints before returning `200 OK`.
2. **Graceful Shutdown (SIGTERM):** Applications must explicitly handle Unix `SIGTERM` signals asynchronously, finishing processing current external requests before exiting.
3. **PreStop Hooks:** Kubernetes deletes the pod from the networking iptables simultaneously with sending the `SIGTERM`. If traffic is heavily cached, some packets will still route to the dying pod. I configure a `preStop` hook containing `sleep 10` to pause the pod's termination, allowing Kubernetes enough time to drain the endpoint from all ingress controllers universally. 

##### Q. Your service mesh sidecar (e.g., Istio Envoy) is consuming more resources than the app itself. How do you analyze and optimize this setup?
**Answer:**
In massive clusters, Envoy proxies download the entire cluster's service registry by default, converting thousands of endpoints into heavy memory routing tables.
**Analysis:** Use `istioctl proxy-config` to inspect the massive Envoy clusters/listeners footprint inside the sidecar. 
**Optimization:** Configure the Istio **`Sidecar` Custom Resource Definition (CRD)**. By applying a `Sidecar` object in the namespace, I explicitly restrict egress traffic visibility. If `App-A` only communicates with `App-B`, I configure the Sidecar CRD so Envoy drops awareness of apps C-Z. This drastically reduces the envoy proxy's memory footprint and CPU processing from 500MB+ down to <50MB.

##### Q. You need to create a Kubernetes operator to automate complex application lifecycle events. How do you design the CRD and controller loop logic?
**Answer:**
1. **CRD (Custom Resource Definition):** I utilize the `Operator SDK` or `Kubebuilder` to generate the CRD schemas. The CRD defines the *desired state* of the complex application (e.g., `ClusterSize: 3`, `BackupEnabled: true`).
2. **Reconciliation Loop:** The Operator executes an infinite event-driven polling mechanism written in Go. 
   - **Observe:** Fetch the CRD's desired configuration and compare it to the live cluster (Are there actually 3 pods running?).
   - **Analyze:** Identify drift. If the cluster only has 2 pods, determine the differential.
   - **Act:** Execute idempotent API calls to create the 3rd pod and instantiate the backup daemon. 
3. **Requeue on Error:** The custom controller exclusively handles transient errors by mathematically "Requeueing" events with exponential backoff until the actual state safely reflects the desired state.

##### Q. Multiple nodes are showing high disk IO usage due to container logs. What Kubernetes features or practices can you apply to avoid this scenario?
**Answer:**
Left unchecked, application `stdout` generates massive log files directly onto the container runtime's root volume, crippling disk IO operations.
1. **Log Rotation:** Configure the container runtime (Docker `daemon.json` or containerd config) to strictly enforce `"max-size": "50m"` and `"max-file": "3"`. This caps file growth and truncates aggressively.
2. **Ephemeral Storage Quotations:** Enforce `limits.ephemeral-storage` inside the Pod spec. If a pod attempts to write runaway logs consuming the host limits, Kubernetes safely evicts it.
3. **Streaming Architecture:** Rely entirely on a DaemonSet (Fluentd / FluentBit) to instantly stream logs off the local disk to a centralized SIEM (like Elastic or CloudWatch) rather than relying on application-level disk buffering.

##### Q. Your Kubernetes cluster's etcd performance is degrading. What are the root causes and how do you ensure etcd high availability and tuning?
**Answer:**
etcd requires extreme low-latency IO and geographic proximity since it leverages the Raft consensus algorithm.
1. **Root Cause 1: Disk Latency.** etcd must execute `fsync` sequentially. If sharing disk IO with the API server or workloads, latency spikes cause leader elections to crash. **Fix:** Provision dedicated, ultra-fast NVMe/Premium SSD storage volumes strictly for the `/var/lib/etcd` mount path.
2. **Root Cause 2: Database Size.** ETCD is famously capped at 8GB (default 2GB). It accumulates revision histories. **Fix:** Periodically enforce `etcdctl defrag` and configure aggressive auto-compaction thresholds to reclaim space.
3. **Root Cause 3: API Abuse.** Runaway custom controllers or overly aggressive Prometheus metric scrapers generating immense `Watch` API polling severely strain the database. Identify and optimize the querying agents.

##### Q. You want to enforce that all images used in the cluster must come from a trusted internal registry. How do you implement this at the policy level?
**Answer:**
I would utilize a **Validating Admission Webhook** specifically powered by **OPA Gatekeeper** or **Kyverno**. 
I would author a Rego policy (Gatekeeper) or a YAML policy (Kyverno) that intercepts every single `Pod` creation request at the API server before it gets saved to etcd. 
The Webhook parses the `spec.containers[*].image` URL string. If the string fails to strictly match the regex of the internal registry (e.g., `^myregistry.internal.corp/.*`), the webhook violently rejects the request, logging exactly which user/CI pipeline attempted to deploy external unverified code.

##### Q. You're managing multi-region deployments using a single Kubernetes control plane. What architectural considerations must you address to avoid cross-region latency and single points of failure?
**Answer:**
A single global Control Plane (single etcd cluster stretched across continents) is an extreme anti-pattern due to etcd's requirement for <10ms ping for Raft consensus. Network jitter causes rolling leader-election failure clusters.
**Correct Architecture:** 
1. Use distinct, physically isolated Kubernetes Control Planes per region. 
2. Adopt a "Management Cluster" topology utilizing **Cluster API** or multi-cluster orchestration frameworks like **Karmada**. 
3. The central management cluster tracks the metadata but deploys configurations asynchronously directly to Regional API servers. If trans-Atlantic latency surges or drops entirely, local regional Data-Planes function seamlessly, avoiding single points of globally stretched failures.

##### Q. During peak traffic, your ingress controller fails to route requests efficiently. How would you diagnose and scale ingress resources effectively under heavy load?
**Answer:**
An Ingress Controller (like NGINX) failing typically surfaces as 502/504 errors or excessive latency.
1. **Vertical Scaling (Tuning):** NGINX workers process connections contextually. I would increase the `worker-processes` and scale out `worker-connections` in the NGINX ConfigMap. Additionally, I would enable `keep-alive` connection pooling to backend pods to stop costly TCP handshake delays.
2. **Horizontal Scaling:** Ensure the Ingress Controller deployment is tethered to a dedicated **HPA (Horizontal Pod Autoscaler)** driving off CPU and Memory limits, replicating out proxy pods rapidly during traffic rushes.
3. **CPU Offloading:** SSL/TLS termination is heavily compute-intensive. Moving TLS termination heavily upwards directly onto the Cloud Provider's native Load Balancer (e.g., AWS ALB attached over the Ingress) drastically frees up Kubernetes CPU cycles.


### Advanced Architecture and Hardening

##### Q. How do you implement GitOps in a Kubernetes environment?
**Answer:**
I utilize **ArgoCD** or **FluxCD**.
1. **Declarative State:** The entire desired state of the cluster (Deployments, Services, ConfigMaps) is written in Helm or purely in Kustomize and committed to a Git repository.
2. **Reconciliation Loop:** The ArgoCD controller runs *inside* the Kubernetes cluster (Pull model). It incessantly polls the Git repository. 
3. **Synchronization:** If a developer merges an updated `deployment.yaml` in Git changing the image tag, ArgoCD detects the configuration drift mathematically. It executes the equivalent of `kubectl apply`, bringing the live cluster state directly into sync with Git, eliminating imperative manual operations completely.

##### Q. Can you explain how you would create a fully automated blue-green deployment in a Kubernetes-based microservices architecture?
**Answer:**
1. **Deploying the Parallel Environments:** Helm or Kustomize generates all Kubernetes components explicitly tagged with the version (e.g., `app-v1` (Blue) and `app-v2` (Green)) in the same namespace, creating two separate Deployments. 
2. **The Routing Service:** The main Kubernetes `Service` acts as the router. It uses a label selector: `version: v1`.
3. **Automated Cut-over:** The CI/CD pipeline deploys `app-v2`. It runs automated integration testing against a temporary `Service-v2` endpoint pointing to Green. 
4. **Swap:** If tests pass natively, the CI/CD pipeline or Argo Rollouts instantaneously updates the main `Service` selector to `version: v2`. Traffic cuts entirely over; if errors spike, an automated trigger instantaneously reverts the selector back to `version: v1`.

##### Q. How do you manage secrets and config securely at scale in Kubernetes without compromising GitOps workflows?
**Answer:**
You cannot store raw Base64 Secrets plainly in a Git repository.
1. **Sealed Secrets (Bitnami):** Developers encrypt secrets locally using the cluster\'s public key (e.g., `kubeseal`) and safely commit this `SealedSecret` cipher text into Git. The dedicated controller inside Kubernetes receives the blob and uses its private key to dynamically decrypt and instantiate the native K8s Secret.
2. **External Secrets Operator (ESO):** Instead of committing *any* secret configuration to Git, Git contains a declarative `ExternalSecret` manifest mapping. The ESO controller natively authenticates to HashiCorp Vault or AWS Secrets Manager, fetches the dynamic password, and generates the native K8s Secret dynamically at runtime.

##### Q. Explain the control plane components of Kubernetes and how you would harden them for production use.
**Answer:**
- **API Server:** Validates and processes all REST operations. *Harden:* Disable anonymous access, strictly enforce RBAC, configure Audit Logging shipped outwardly to an ELK stack, and restrict external API Server access via Cloud Provider Private Endpoints (bypassing the public internet).
- **etcd:** Distributed key-value store holding the cluster state. *Harden:* Ensure data is encrypted at rest natively, run etcd exclusively on ultra-fast isolated NVMe drives preventing Raft consensus timeouts, and orchestrate frequent volume snapshots.
- **Controller Manager & Scheduler:** They monitor states and assign nodes. *Harden:* Ensure they communicate strictly over TLS and disable unsecured ports.

##### Q. How would you scale a Kubernetes cluster horizontally across multiple regions and still ensure zero-downtime upgrades?
**Answer:**
A single stretched cluster across regions violates etcd latency requirements.
1. **Multi-Cluster Orchestration:** I spin up geographically independent clusters (e.g., `EKS-US-East` and `EKS-EU-West`). 
2. **Global Load Balancing:** I place an intelligent global router (like AWS Route53 or Azure Front Door) over them. 
3. **Zero-Downtime Upgrades:** When upgrading to K8s 1.30, I execute the control-plane upgrade on standard Region A. Meanwhile, Region B is handling global traffic. When Region A worker nodes need replacing, I explicitly cordon them. If workloads degrade natively, Route 53 health-checks fail over all targeted DNS traffic seamlessly to Region B until Region A stabilizes, yielding 100% SLA up-time.

##### Q. What is a PodDisruptionBudget and how do you use it in critical workloads?
**Answer:**
A Pod Disruption Budget (PDB) guarantees the minimum number of available pods required explicitly during highly volatile, *voluntary* disruptions (like a cluster administrator draining a node for patched restarts).
*Usage:* By configuring a PDB specifying `minAvailable: 2` or `maxUnavailable: 1` on an NGINX deployment consisting of 3 pods, `kubectl drain` is rigidly blocked mathematically if evicting the current pod would severely drop the running replica count down to 1, completely preventing administrative commands from accidentally flatlining a critical application.

##### Q. How do you implement and manage network policies in Kubernetes for strict inter-service communication?
**Answer:**
By default, Kubernetes implements an open "flat" network where any pod communicates universally.
1. **CNI Enabler:** Ensure you deploy a CNI that respects policies (like Calico or Cilium; Flannel does not execute network policies natively).
2. **Zero-Trust (Default Deny):** Deploy a Catch-all NetworkPolicy applying to all pods dropping 100% of internal traffic.
3. **Explicit Permits:** Deploy explicit isolated NetworkPolicies allowing exactly required traffic paths based primarily on labels (e.g., explicitly allowing pods possessing the label `app=frontend` to ingress heavily onto pods possessing the label `app=database` exclusively on port `3306`).

##### Q. How would you integrate runtime threat detection in Kubernetes using tools like Falco or Sysdig?
**Answer:**
1. **DaemonSet Deployment:** I deploy **Falco** as a DaemonSet across all worker nodes. It functions by intercepting raw Linux kernel system calls utilizing eBPF (Extended Berkeley Packet Filter).
2. **Rule Design:** I configure Falco rules triggering on anomalous behaviors indicating container breaches—such as a user spawning a bash shell (`/bin/sh`) inside a running NGINX pod, a modified `etc/shadow` file, or unexpected outbound network connections routing directly to an unknown cryptographic miner IP.
3. **Resolution:** Falco detects the threat natively and streams an alert asynchronously to an admission hook or a serverless function that automatically labels the pod as compromised, physically severing it from the K8s Service and terminating it while alerting SecOps.
