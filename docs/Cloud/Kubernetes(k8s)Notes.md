# Kubernetes (k8s) Notes

**Kubernetes (often abbreviated as K8s)** is an open-source container orchestration platform designed to automate deploying, scaling, and managing containerized applications. It provides a framework to run distributed systems resiliently, handling scaling and failover for your applications, and provides deployment patterns, such as rolling updates.

### K8s Archietecture Diagram

![k8s Archietecture Diagram](https://github.com/sawanchouksey/documents/blob/main/docs/Cloud/Kubernetes-Architecture-Diagram.jpg?raw=true)

### Installation & Provisioning of Kubernetes

Kubernetes can be installed and provisioned using various methods and providers. Here’s a brief overview:

1. **Local Installation**:
   
   - **Minikube**: Runs a single-node Kubernetes cluster locally for testing and development.
   - **kind (Kubernetes IN Docker)**: Runs Kubernetes clusters in Docker containers.

2. **Cloud Providers**:
   
   - **Amazon EKS (Elastic Kubernetes Service)**: Managed Kubernetes service by AWS.
   - **Google GKE (Google Kubernetes Engine)**: Managed Kubernetes service by Google Cloud.
   - **Microsoft AKS (Azure Kubernetes Service)**: Managed Kubernetes service by Microsoft Azure.

3. **Kubernetes Distributions**:
   
   - **OpenShift**: A Kubernetes distribution with additional features.
   - **Rancher**: A multi-cluster management tool that can manage multiple Kubernetes clusters.

### Pros and Cons of Kubernetes

#### Pros:

- **Scalability**: Automatically scale applications based on demand.
- **High Availability**: Resilient to failures; can automatically reschedule containers.
- **Flexibility**: Supports various container runtimes and can be integrated with CI/CD pipelines.
- **Community and Ecosystem**: Large community support and numerous extensions and tools available.

#### Cons:

- **Complexity**: Steep learning curve and requires significant expertise to manage.
- **Resource Overhead**: More resource-intensive compared to simpler orchestration solutions.
- **Configuration Management**: Managing configurations can become cumbersome in large environments.

### Use Cases for Kubernetes

- **Microservices Architecture**: Running applications as loosely coupled services.
- **Hybrid Cloud**: Deploying applications across on-premises and cloud environments.
- **DevOps**: Automating application deployment and scaling in CI/CD pipelines.
- **Batch Processing**: Managing jobs and workloads that can run on a schedule.

### Differences Between AKS, EKS, and GKE

1. **AKS (Azure Kubernetes Service)**:
   
   - **Integration**: Deep integration with Azure services like Azure Active Directory and Azure Monitor.
   - **Ease of Use**: Provides a simplified deployment model with a focus on Azure-native experiences.
   - **Scaling**: Offers advanced scaling options like Virtual Node integration with Azure Container Instances.

2. **EKS (Elastic Kubernetes Service)**:
   
   - **Integration**: Integrates seamlessly with AWS services like IAM for security and CloudWatch for monitoring.
   - **Cluster Management**: Managed control plane; easy to set up and maintain.
   - **Fargate Support**: Can run containers without managing servers (serverless option).

3. **GKE (Google Kubernetes Engine)**:
   
   - **Performance**: Offers advanced performance features like autopilot mode for managing the infrastructure.
   - **Cost Management**: Fine-grained cost monitoring and optimization tools available.
   - **Innovative Features**: Early adoption of Kubernetes features and tools, often leading in new capabilities.

### Components of Kubernetes

1. **Master Node**:
   
   - **API Server**: Exposes the Kubernetes API and serves as the entry point for commands.
   - **Controller Manager**: Governs controllers that handle the routine tasks in the cluster.
   - **Scheduler**: Assigns workloads to worker nodes based on resource availability.
   - **etcd**: Key-value store that holds all cluster data.

2. **Worker Node**:
   
   - **Kubelet**: Ensures containers are running in a Pod.
   - **Kube Proxy**: Maintains network rules and handles network communication.
   - **Container Runtime**: Software responsible for running the containers (e.g., Docker, containerd).

3. **Objects**:
   
   - **Pod**: The smallest deployable unit, can host one or more containers.
   - **Service**: A stable endpoint for accessing a set of Pods.
   - **Deployment**: Manages the deployment of Pods and scaling.
   - **Namespace**: Provides a mechanism for isolating groups of resources.

4. **Networking**:
   
   - **CNI (Container Network Interface)**: Framework for configuring network interfaces in Linux containers.
   - **Ingress**: Manages external access to services within the cluster.

5. **Storage**:
   
   - **Persistent Volumes**: Abstraction for managing storage resources.
   - **Storage Classes**: Defines different types of storage and their configuration.

### Installing `kubectl`

1. Download the Latest Release
    Use the following command to download the latest version of `kubectl`:
   
   ```bash
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   ```

2. Install kubectl
    Install `kubectl` by running:
   
   ```bash
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

3. Test Installation
    Verify that the installation was successful and check the version:
   
   ```bash
   kubectl version --client
   ```
   
   ### Installing `Minikube`

4. Download the Binary
    Download the latest version of `minikube`:
   
   ```bash
   curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
   chmod +x minikube-linux-amd64
   ```

5. Install Minikube
    Move the binary to a directory in your `PATH`:
   
   ```bash
   sudo install minikube-linux-amd64 /usr/local/bin/minikube
   ```

6. Verify Installation
    Check that `minikube` is installed correctly:
   
   ```bash
   minikube version
   ```

7. Start Kubernetes Cluster
    Before starting, install `conntrack` if you haven’t already:
   
   ```bash
   sudo apt install conntrack
   sudo minikube start --vm-driver=none
   ```

8. Get Cluster Information
    To view the cluster configuration:
   
   ```bash
   kubectl config view
   ```
   
   ### 3 node self managed cluster kubeadm setup

9. create 3 vm instnace 

```
- k8s-master
- k8s-worker-1
- k8s-worker-2
```

2. swap must be off in all nodes of k8s. check with below commnd

```
free -h
```

3. disable swap if its enabled and shown in above command output and check again

```
swapoff -a
```

4. disable "swapon" while rebooting system in all nodes

```
cd /etc/fstab
comment all the line start with "swap" & "swap.img"
```

5. install docker in all nodes

6. Check required ports 6443 must be open. You can use tools like netcat to check if a port is open

```
nc 127.0.0.1 6443
```

7. Installing kubeadm, kubelet and kubectl in all nodes
   
   1. Update the apt package index and install packages needed to use the Kubernetes apt repository:
      
      ```
      sudo apt-get update
      sudo apt-get install -y apt-transport-https ca-certificates curl
      ```
   
   2. Download the public signing key for the Kubernetes package repositories. The same signing key is used for all repositories so you can disregard the version in the URL:
      
      ```
      curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.24/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
      ```
   
   3. Add the appropriate Kubernetes apt repository. Please note that this repository have packages only for Kubernetes 1.24; for other Kubernetes minor versions, you need to change the Kubernetes minor version in the URL to match your desired minor version (you should also check that you are reading the documentation for the version of Kubernetes that you plan to install).
      
      ```
      This overwrites any existing configuration in /etc/apt/sources.list.d/kubernetes.list
      echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.24/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
      ```
   
   4. Update the apt package index, install kubelet, kubeadm and kubectl, and pin their version:
      
      ```
      sudo apt-get update
      sudo apt-get install -y kubelet kubeadm kubectl
      sudo apt-mark hold kubelet kubeadm kubectl
      ```

8. intialize and create master node with kubeadm with appriate network i.e. calico, flannel or cidr value of flannel is 10.244.0.0/16

9. run below command in master node

```
kubeadm init --pod-network-cidr=10.244.0.0/16
```

10. run the command below to start cluster in master node

```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

11. run the command to check nodes is in ready state

```
kubectl get nodes
```

12. You can install a Pod network add-on with the following command on the control-plane node or a node that has the kubeconfig credentials:

```
kubectl apply -f kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```

13. run the command to check nodes is in ready state

```
kubectl get nodes
```

14. add worker node in master node . So we will run below command provide by kubeadm to run on all worker node to join master node

```
kubeadm join 192.168.25.:6443 --token xvazne.hgfif89re80ugrhgfusd --discovery-token-ca-cert-hash sha256:23798rhgr984ry4883yt59th38th95hty539th5th895t
```

15. run the command to check all nodes is in ready state

```
kubectl get nodes
```

- **Deployment Features**
1. Application Deployment
   
   1. **Rollout**
   - This feature allows for the deployment of new application versions. Users can manage and observe the rollout process to ensure that the new version is functioning as expected before fully transitioning.
   2. **Pause & Resume**
   - Users can pause a deployment in progress to prevent any further changes. This is useful for troubleshooting or when you need to intervene before the deployment continues. Once ready, the deployment can be resumed from where it was paused.
   3. **RollBack**
   - In the event of an issue with the newly deployed version, Kubernetes allows you to roll back to a previous stable version quickly. This feature ensures minimal disruption and quick recovery from potential problems.

2. Scaling
   
   1. **Replicas**
   - The number of pod replicas can be defined in the deployment configuration. This allows the application to handle increased loads by creating additional instances of the application.
   2. **Scale Up & Down**
   - Kubernetes supports scaling applications up or down as needed. Scaling up increases the number of running pods, while scaling down reduces them. This flexibility helps manage resource usage effectively based on demand.

3. Deployment Strategies
   
   1. **Recreate**
   - This strategy involves deleting all existing pods before creating new ones. While it guarantees that only the new version is running, it leads to downtime as the old version is completely shut down before the new version is deployed.
   2. **Rolling Update**
   - The default deployment strategy, rolling updates gradually replace old pods with new ones. For instance, if you have 100 replicas, the system might delete 25% of them and replace them one by one with the new version. This approach minimizes downtime and maintains service availability.
   3. **Canary**
   - The canary deployment strategy allows you to release the new version to a small subset of users while the majority still use the old version. By deleting one pod at a time and replacing it with the new version, you can monitor the performance and ensure stability before a full rollout.
   4. **Blue-Green**
   - This strategy involves maintaining two separate environments: the current (blue) and the new version (green). Traffic is switched from blue to green after the new version is fully deployed and tested. Although it requires double the infrastructure temporarily (for storage, RAM, CPU), it allows for a seamless transition without downtime.

### Important Commands and notes

- minikube default username and password

```
username: "docker", 
password: "tcuser"
```

- commadn to access minikube dashboard

```
minikube dashboard
```

- update service account in all ms if istio-ingressgateway name change because it will create new SA with new istio-ingressgateway name 

```
kubectl get authorizationpolicy test
kubectl describe authorizationpolicy test
kubectl get sa -n istio-system
```

- to know about any object in k8s with their yaml fields

```
kubectl explain pod --recursive
```

- get all pod env variable

```
kubectl exec mypod env
```

- kubectl logs with tail

```
kubectl logs --tail=50 <pod_name>
```

- update rollout with cutom message in deployment

```
kubectl annotate deployment.apps/myapp kubernetes.io/change-cause="image updated to new version v1.0.0"
```

- The "rolling update" stretegy maintain "Zero Downtime" Good for production but "recreate" stretegy good for development because of take less time for deployment

- Removing old replicasets is part of the Deployment object, but it is optional. You can set .spec.revisionHistoryLimit to tell the Deployment how many old replicasets to keep around.Here is a YAML example:

```
apiVersion: apps/v1
kind: Deployment
metadata:
spec:
  ...
  revisionHistoryLimit: 0 # Default to 10 if not specified
  ...
```

- insecure-skip-tls-verify in .kube/config file

```
https://stackoverflow.com/questions/48119650/helm-x509-certificate-signed-by-unknown-authority
apiVersion: v1
clusters:
- cluster:
    server: https://192.168.0.3
    insecure-skip-tls-verify: true
  name: gke_my_k8s
```

- Zero downtime with rolling update

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

- service DNS name

```
servicename.namespacename.svc.cluster.local
```

- dry-run

```
kubectl apply -f hello.yaml --dry-run=client
```

- record the command hostory with version in rollout 

```
kubectl rollout restart deployment $app_name -n $namespace --record
```

- When no CNI plugin is installed, Nodes will remain in the NotReady state.

- Pod domain names are of the form pod-ip-address.namespace-name.pod.cluster.local.

- Static Pods can be used to run containers on a Node in the absence of a Kubernetes API Server.

- PodSpec attributes is guaranteed to cause a Pod to run on a specific node, regardless of that Node's labels

```
nodeName
```

#show label assigned to nodes

```
kubectl get nodes  --show-labels
```

- liveness probe 
  
  - it will help to restart container at run time health check
  
  - If liveness probe failed conatiner will restart automatically
  
  - By Default, K8s only consider container to be down, if container
    process stops.
  
  - Liveness probe helps user to improve & customized this Container Monitoring mechanism.
  
  - User can execute Two types of Liveness probes - Run Command in Container, Periodic HTTP Health Check.
    
    ```
    livenessProbe:
     httpGet:
      path: /health.html
      port: 8080
      httpHeaders:
      - name: Custom-Header
        value: Awesome
     initialDelaySeconds: 3
     periodSeconds: 3
     timeoutSeconds: 1
    ```

- Startup probe
  
  - StartUp probe runs at container StartUp and stop running once container success.
  
  - Once the startup probe has succeeded once, the liveness probe takes over to provide a fast response to container deadlocks.
    
    ```
    startupProbe:
      httpGet:
          path: /health.html
          port: 8080
      failureThreshold: 30
      periodSeconds: 10
    ```

- Readiness Probe
  
  - Readiness is used to detect if a container is ready to accept traffic.
  
  - NO Traffic will be sent to a pod until container pass the Readiness Probe.
    
    ```
    readinessProbe:
     httpGet:
      path: /health.html
      port: 8080
      httpHeaders:
      - name: Custom-Header
        value: Awesome
     initialDelaySeconds: 3
     periodSeconds: 3
     timeoutSeconds: 1
    ```

- init conatiner to check service up or not

```
apiVersion: v1
kind: Pod
metadata:
  name: application-pod
spec:
  containers:
    - name: myapp-container
      image: busybox:1.28
      command: ["sh", "-c", "echo The app is running! && sleep 3600"]
  initContainers:
    - name: init-myservice
      image: busybox:1.28
      command:
        [
          "sh",
          "-c",
          "until nslookup myservice.$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace).svc.cluster.local; do echo waiting for myservice; sleep 5; done",
        ]
```

- Resource Allocation in Container
  
  - Request : It allow to help kube schedular to schedule container with respect to define resource request in node.
  - Limit   : It allow to help container to use Max or limit resource for container at run time with respect to limit.

- k8s role is limited on namespace level only

- k8s service account used by container process to Authenticate with k8s APIs

- It is used to pod communicate with k8s APIs internally

- flag allows you to see what would happen when creating an object without actually creating the object

```
kubectl apply -f deployment.yaml --dry-run=client
```

- print all env value inside pod

```
printenv
```

- configMap and scret store inside pod

```
/etc/config
     |____ConfigMap
     |____Secret
            |_____USERNAME
            |_____PASSWORD
```

- ConfigMap with POSIX(posNine configuration)
  
  - It is another way to define confgimap and read the value
  
  - In POSIX configMap Data store in key:Value pair only.
  
  - Each KEY must be in CAPITAL letter and KEY words seprated by Underscore only(_)
    
    ```
    
    ```
    
    ----------------------
  
  POSIX ConfigMap.yaml
  ----------------------
  
    apiVersion: v1
    kind: ConfigMap
    metadata:
  
      name: player-posix-demo
  
    data:
  
      PLAYER_LIVES: "5"
      PROPERTIES_FILE_NAME: "user-interface.properties"
      BASE_PROPERTIES: "Template1"
      USER_INTERFACE_PROPERTIES: "Dark"
  
  ```
  
  ```

- Access configMap Value from ConfigMap and used in application

```
envFrom:
    - configMapRef:
        name: player-posix-demo(configMap Name only)
```

```
-----------------------
NORMAL ConfigMap.yaml
-----------------------
apiVersion: v1
kind: ConfigMap
metadata:
  name: player-pro-demo
data:
  # property-like keys; each key maps to a simple value
  player_lives: "5"
  properties_file_name: "user-interface.properties"
```

- set namspace in context in kube config file

```
kubectl config set-context --current --namespace=mhe-epharmacy
```

- command to find where is secret using

```
kubectl get deployments,statefulsets,daemonsets,cronjobs,jobs,pods -n namespace-name -o yaml | grep -i -e "^ name:"  -e "^  kind" -e secret-name
```

- enable ssl ingress tls with nginx or azure/application-gateway with letsencrypt

```
https://docs.microsoft.com/en-us/azure/aks/ingress-tls?tabs=azure-cli
- set variable for kubernates cluster access
KUBERNATES_CLUSTER_NAME=blue-green
RESOURCE_GROUP_NAME=blue-green
```

- set variable for cert manager deployment

```
REGISTRY_NAME=testimages
CERT_MANAGER_REGISTRY=quay.io
CERT_MANAGER_TAG=v1.8.0
CERT_MANAGER_IMAGE_CONTROLLER=jetstack/cert-manager-controller
CERT_MANAGER_IMAGE_WEBHOOK=jetstack/cert-manager-webhook
CERT_MANAGER_IMAGE_CAINJECTOR=jetstack/cert-manager-cainjector
```

- Set variable for ACR location to use for pulling images

```
ACR_URL=testimages.azurecr.io
```

- set variable for cert-manager namespace

```
CERT_MANAGER_NAMESPACE=ingress-basic
```

- import cert manager images to ACR

```
az acr import --name $REGISTRY_NAME --source $CERT_MANAGER_REGISTRY/$CERT_MANAGER_IMAGE_CONTROLLER:$CERT_MANAGER_TAG --image $CERT_MANAGER_IMAGE_CONTROLLER:$CERT_MANAGER_TAG
az acr import --name $REGISTRY_NAME --source $CERT_MANAGER_REGISTRY/$CERT_MANAGER_IMAGE_WEBHOOK:$CERT_MANAGER_TAG --image $CERT_MANAGER_IMAGE_WEBHOOK:$CERT_MANAGER_TAG
az acr import --name $REGISTRY_NAME --source $CERT_MANAGER_REGISTRY/$CERT_MANAGER_IMAGE_CAINJECTOR:$CERT_MANAGER_TAG --image $CERT_MANAGER_IMAGE_CAINJECTOR:$CERT_MANAGER_TAG
```

- connect to the kubernates cluster

```
az aks get-credentials --resource-group $RESOURCE_GROUP_NAME --name $KUBERNATES_CLUSTER_NAME --overwrite-existing
```

- create namespace for cert-manager

```
kubectl create namespace $CERT_MANAGER_NAMESPACE
```

- Label the ingress-basic namespace to disable resource validation

```
kubectl label namespace $CERT_MANAGER_NAMESPACE cert-manager.io/disable-validation=true
```

- Add the Jetstack Helm repository

```
helm repo add jetstack https://charts.jetstack.io
```

- Update your local Helm chart repository cache

```
helm repo update
```

- Install the cert-manager Helm chart

```
helm install cert-manager jetstack/cert-manager \
  --namespace $CERT_MANAGER_NAMESPACE \
  --version $CERT_MANAGER_TAG \
  --set installCRDs=true \
  --set nodeSelector."kubernetes\.io/os"=linux \
  --set image.repository=$ACR_URL/$CERT_MANAGER_IMAGE_CONTROLLER \
  --set image.tag=$CERT_MANAGER_TAG \
  --set webhook.image.repository=$ACR_URL/$CERT_MANAGER_IMAGE_WEBHOOK \
  --set webhook.image.tag=$CERT_MANAGER_TAG \
  --set cainjector.image.repository=$ACR_URL/$CERT_MANAGER_IMAGE_CAINJECTOR \
  --set cainjector.image.tag=$CERT_MANAGER_TAG
```

```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: 1820387@tcs.com
    privateKeySecretRef:
      name: letsencrypt
    solvers:
    - http01:
        ingress:
          class: azure/application-gateway
          podTemplate:
            spec:
              nodeSelector:
                "kubernetes.io/os": linux
```

- use LENS IDE tool for control and manage multiple kubernates cluster by UI 

- delete all pod in kubernates with specific name pattern like test

```
kubectl get pods | awk '/^test/{system("kubectl delete pod " $1)}'
```

- kubernates cost analyzer by kubecost

```
https://alapmistry.hashnode.dev/integrate-and-deploy-kubecost-using-lens-ide
```

- MASTER NODE configuration used for control all cluster. There are 4 component in master node or control plane

| Component              | Description                                                                                                                                                                                                                                                       | Port  |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| **API Server**         | Used to communicate between all other components. Manages authentication and validates YAML config.                                                                                                                                                               | 6443  |
| **ETCD**               | Key-value pair database for Kubernetes. Stores all Kubernetes configurations, app configurations, and secrets.                                                                                                                                                    | 2379  |
| **Controller Manager** | Acts as a controller for controllers, managing the overall health of the Kubernetes cluster. Contains four controller components: <br> a. Node Controller <br> b. Replication Controller <br> c. End-point Controller <br> d. Token and Service Token Controllers | 10252 |
| **Scheduler**          | Responsible for scheduling tasks and checking pod configurations. Assigns configurations to nodes based on pod requirements.                                                                                                                                      | 10251 |

- WORKER NODE is used to perform task and deployed application in it.There are 3 component for worker node

| Component      | Description                                                                                                                                                                            | Port                        |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| **Kubelet**    | Agent running on every worker node. Checks API server in the master node to assign tasks and report node status and pod health.                                                        | 10250                       |
| **Kube-Proxy** | Network agent running on every worker node. Maintains all network configurations, including service configuration, routing, and load balancing tasks.                                  | Services Port (30000-32767) |
| **CRI**        | Container Runtime Interface responsible for running and downloading images on nodes. Supports various CRIs like Docker and containers.d, with Docker as the default CRI in Kubernetes. | N/A                         |

- Ensure all nodes including Master and Worker nodes are "Ready":

```
kubectl get nodes 
kubectl get nodes –o wide
```

- Ensure all K8s Master node components are in "Running" status:

```
kubectl get pods –n kube-system
kubectl get pods –n kube-system -o wide
```

- Ensure Docker and Kubelet Services are "Active(Running) and Enabled on all nodes

```
a). Checking Docker Service Status:
systemctl status docker

b). Checking Docker Kubelet Status:
systemctl status kubelet

- Deploying Test Deployment:
a). Deploying the sample "nginx" deployment:
kubectl apply -f https://k8s.io/examples/controllers/nginx-deployment.yaml

b). Validate Deployment:
kubectl get deploy
kubectl get deploy –o wide

c). Validating Pods are in "Running" status:
kubectl get pods 
kubectl get pods –o wide

d). Validate containers are running on respective worker nodes:
docker ps

e). Delete Deployment:
kubectl delete -f https://k8s.io/examples/controllers/nginx-deployment.yaml
```

- create pod by run command

```
kubectl run --generator=run-pod/v1 nginx-pod --image nginx
```

- YAML Elements
1. apiVersion
- `Group_Name/VERSION`
  
  - `apps/v1`
  - `batch/v1`
  - `batch/v1beta1`
  - `extensions/v1beta1`
  - `v1` (by default Core group)
  - `rbac.authorization.k8s.io/v1`
2. Kind
- `Pod`

- `ReplicaSet`

- `ReplicationController`

- `Deployment`

- `Service`

- `DaemonSet`

- `Secret`

- `StatefulSet`

- `ServiceAccount`

- `Role`

- `PersistentVolume`

- `RoleBinding`

- `PersistentVolumeClaim`

- `ClusterRole`

- `ConfigMap`

- `ClusterRoleBinding`

- `Namespace`

- `Job`

- `ComponentStatus`

- `CronJob`
3. Metadata

4. Spec

5. Kind vs ApiVersion

| Kind                  | apiVersion                   |
| --------------------- | ---------------------------- |
| Pod                   | v1                           |
| ReplicationController | v1                           |
| Service               | v1                           |
| Secret                | v1                           |
| ServiceAccount        | v1                           |
| PersistentVolume      | v1                           |
| PersistentVolumeClaim | v1                           |
| ConfigMap             | v1                           |
| Namespace             | v1                           |
| ComponentStatus       | v1                           |
| ReplicaSet            | apps/v1                      |
| Deployment            | apps/v1                      |
| DaemonSet             | apps/v1                      |
| StatefulSet           | apps/v1                      |
| Role                  | rbac.authorization.k8s.io/v1 |
| RoleBinding           | rbac.authorization.k8s.io/v1 |
| ClusterRole           | rbac.authorization.k8s.io/v1 |
| ClusterRoleBinding    | rbac.authorization.k8s.io/v1 |
| Job                   | batch/v1                     |
| CronJob               | batch/v1beta1                |

- Pod YAML with Environment Variables

```
- nginx-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
    tier: dev
spec:
  containers:
  - name: nginx-container
    image: nginx:1.18
    env:
    - name: DEMO_GREETING
      value: "Hello from the environment"
    - name: DEMO_FAREWELL
      value: "Such a sweet sorrow"
```

- Deploy Pods

```
kubectl apply -f <FILENAME.YAML>
(or) 
kubectl create -f <FILENAME.YAML>
```

- Display Pods

```
kubectl get pods
kubectl get pods -o wide  # Print wide output of the Pod

kubectl get pods -n <NAME-SPACE>     # Print Pods in particular NameSpace
kubectl get pods -A                  # Print Pods in all namespace

kubectl get pods <POD-NAME>
kubectl get pods <POD-NAME> -o yaml  
kubectl get pods <POD-NAME> -o json

kubectl get pods --show-labels
kubectl get pods -l app=nginx        # Print Pods with particular label
```

- Print Details of Pod

```
kubectl describe pods <POD-NAME>     
```

- Editing Pod which is running

```
kubectl edit pods <POD-NAME>
kubectl describe pods nginx-pod | grep Image
```

- Print Pod Logs

```
kubectl logs <POD-NAME>
kubectl logs <POD-NAME> -n <NAME-SPACE>
```

- Displaying Pods by Resource Usage

```
NOTE: Metrics-Server

a. To run below top commands, you need to have "Metrics-Server" Installed. 

b. For by-step demo and instructions please refer to the "Installing Metrics Server" lecture & demos that you find in "Troubleshooting" section in this series.
https://www.udemy.com/course/ultimate-cka-certified-kubernetes-administrator/learn/lecture/26854680#questions

c. Again, below are the high-level steps.

d. Installing Metrics-Server:
git clone https://github.com/kubernetes-sigs/metrics-server.git

kubectl apply -k metrics-server/manifests/test/

e. If you encounter any Image error, try updating imagePullPolicy: Always 
in metrics-server/manifests/test/patch.yaml

f. Give it a minute to gather the data and then run below Top Commands:

g. Top Command to find the CPU and Memory Usage of Pods, Nodes and Containers:
kubectl top pods
kubectl top pods -A
kubectl top pods -A --sort-by memory
kubectl top pods -A --sort-by cpu
kubectl top pods -n [name-space]  --sort-by cpu 
kubectl top pods -n [name-space]  --sort-by memory
kubectl top pods -n [name-space]  --sort-by memory > mem-usage.txt
```

- Running operations directly on the YAML file

```
SYNTAX: kubectl [OPERATION] –f [FILE-NAME.yaml]

kubectl get –f [FILE-NAME.yaml]
kubectl describe –f [FILE-NAME.yaml]
kubectl edit –f [FILE-NAME.yaml]
kubectl delete –f [FILE-NAME.yaml]
kubectl apply –f [FILE-NAME.yaml]
```

- Deleting Pod

```
kubectl delete pods <POD-NAME>
```

- Replica set 

```
# frontend.yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: guestbook
    tier: frontend
spec:
  # modify replicas according to your case
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: php-redis
        image: gcr.io/google_samples/gb-frontend:v3
```

- Deploy ReplicaSet

```
kubectl apply -f <FILENAME.YAML>
or 
kubectl create -f <FILENAME.YAML>
```

- Display ReplicaSet (rs)

```
kubectl get rs 
kubectl get rs <RS-NAME> -o wide
kubectl get rs <RS-NAME> -o yaml
kubectl get rs -l <LABEL>     
```

- Displaying Pods 

```
kubectl get pods
kubectl get pods -l <LABEL>  
```

- Print Details of ReplicaSet

```
kubectl describe rs <RS-NAME>
```

- Scaling Applications

```
kubectl scale rs <RS-NAME> --replicas=[COUNT]     
```

- Editing ReplicaSet

```
kubectl edit rs <RS-NAME>      
```

- Running operations directly on the YAML file

```
SYNTAX: kubectl [OPERATION] –f [FILE-NAME.yaml]
kubectl get –f [FILE-NAME.yaml]
kubectl describe –f [FILE-NAME.yaml]
kubectl edit –f [FILE-NAME.yaml]
kubectl delete –f [FILE-NAME.yaml]
kubectl create –f [FILE-NAME.yaml]
```

- Deleting ReplicaSet

```
kubectl delete rs <RS-NAME>
```

- Creating NameSpace Using YAML:

```
# dev-ns.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```

- Creating NameSpace Using Imepratively:

```
kubectl create namespace test
```

- Displaying Namespace

```
kubectl get ns [NAMESPACE-NAME]
kubectl get ns [NAMESPACE-NAME] -o wide
kubectl get ns [NAMESPACE-NAME] -o yaml
kubectl get pods –-namespace=[NAMESPACE-NAME]
```

- describe namespace

```
kubectl describe ns [NAMESPACE-NAME]
```

- Creating Pod Object in Specific NameSpace:

```
kubectl run nginx --image=nginx --namespace=dev
```

- Validate:

```
kubectl get pods
kubectl get pods -n dev
```

- Displaying Objects in All Namespace:

```
kubectl get pods -A
or
kubectl get [object-name] --all-namespaces
```

- Setting the namespace preference:

```
Syntax: 
kubectl config set-context --current --namespace=os-hnm-qa

1. You can permanently save the namespace for all subsequent kubectl commands in that context.

2. --minify=false: Remove all information not used by current-context from the output

kubectl config view --minify | grep namespace:

kubectl get pods

kubectl config set-context --current --namespace=1mg

kubectl config view --minify | grep namespace:

kubectl run redis --image=redis 

kubectl get pods

kubectl config set-context --current --namespace=default

kubectl config view --minify | grep namespace:

kubectl run httpd --image=httpd
```

- Deleting Namespaces

```
kubectl delete pods nginx -n dev
kubectl delete pods redis -n test
kubectl delete pods httpd
kubectl get pods -A
kubectl get ns
kubectl delete ns dev
kubectl delete ns test
kubectl get ns
kubectl get pods

a. First, we will create the test "user account" and "namespace" for testing this demo

b. Then, We will create the Role with list of actions performed in a "specific namespace"

c. And finally, We will assign this role to "user" by creating "RoleBinding"
```

- Note:
  a. Role and RoleBindings are "Namespace" specific.
  b. You can assign Role to "Service Account" instead of user. For more details, please refer below link:

```
https://kubernetes.io/docs/reference/access-authn-authz/rbac/
```

- Creating Kubernetes test User Account(appuser) (using x509 for testing RBAC)

```
1. Generating Key
openssl genrsa -out appuser.key 2048

2. Generaing Certificate Signing request (csr):
openssl req -new -key appuser.key -out appuser.csr -subj "/CN=appuser"

3. Singing CSR using K8s Cluster "Certificate" and "Key"
openssl x509 -req -in appuser.csr \
        -CA /etc/kubernetes/pki/ca.crt \
        -CAkey /etc/kubernetes/pki/ca.key \
        -CAcreateserial \
        -out appuser.crt -days 300

4. Adding user credentials to "kubeconfig" file
kubectl config set-credentials appuser  --client-certificate=appuser.crt --client-key=appuser.key

5. Creating context for this user and associating it with our cluster:
kubectl config set-context appuser-context --cluster=kubernetes --user=appuser

6. Displaying K8s Cluster Config
kubectl config view

7. Creating test Namespace:
kubectl create ns dev-ns

8. Creating test Pod:
kubectl run nginx-pod --image=nginx -n dev-ns
kubectl get pods -n dev-ns

9. Test Before Deploying:
kubectl get pods -n dev-ns --user=appuser 

10. Creating a "Role" & "RoleBinding":

11. Creating Resources Declaratively (Using YAML):

-----
Role
-----
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: dev-ns
  name: pod-reader
rules:
- apiGroups: [""] 
  resources: ["pods"]
  verbs: ["get", "watch", "list"]

------------
RoleBinding
------------
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: read-pods
  namespace: dev-ns
subjects:
- kind: User
  name: appuser 
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role 
  name: pod-reader 
  apiGroup: rbac.authorization.k8s.io

12. role
kubectl create role pod-reader --verb=get --verb=list --verb=watch --resource=pods --namespace=dev-ns

13. rolebinding
kubectl create rolebinding read-pods --role=pod-reader --user=appuser --namespace=dev-ns

14. Display Role and RoleBinding:
kubectl get role -n dev-ns
kubectl get rolebinding -n dev-ns

15. Describe Role and RoleBinding
kubectl describe role -n dev-ns
kubectl describe rolebinding -n dev-ns

16. Testing RBAC:
- Pod Operations: get, list, watch - in "dev-ns" namespace:
kubectl auth can-i get pods -n dev-ns --user=appuser
kubectl auth can-i list pods -n dev-ns --user=appuser
kubectl get pod nginx-pod -n dev-ns --user=appuser
kubectl get pods -n dev-ns --user=appuser

- Pod Operations: get, list, watch - in "NON dev-ns" namespace:
kubectl auth can-i get pods -n kube-system --user=appuser
kubectl auth can-i list pods -n kube-system --user=appuser
kubectl auth can-i watch pods -n kube-system --user=appuser
kubectl get pods --user=appuser # queries default namespace
kubectl get pods -n kube-system --user=appuser

17. Creating Objects in "dev-ns" namespace: 
kubectl auth can-i create pods -n dev-ns --user=appuser
kubectl auth can-i create services -n dev-ns --user=appuser
kubectl auth can-i create deployments -n dev-ns --user=appuser
kubectl run redis-pod -n dev-ns --image=redis --user=appuser
kubectl create deploy redis-deploy -n dev-ns --image=redis --user=appuser

18. Deleting Objects in "dev-ns" namespace: 
kubectl auth can-i delete pods -n dev-ns --user=appuser
kubectl auth can-i delete services -n dev-ns --user=appuser
kubectl auth can-i delete deployments -n dev-ns --user=appuser
kubectl delete pods nginx-pod -n dev-ns --user=appuser

19. Cleanup:
kubectl config unset contexts.appuser-context
kubectl config unset users.appuser
kubectl config view
kubectl get pod nginx-pod -n dev-ns --user=appuser
kubectl get pods -n dev-ns --user=appuser
kubectl delete role pod-reader -n dev-ns
kubectl delete rolebinding read-pods -n dev-ns

a. First, we will create the test "user account" for testing this demo

b. Next,  We will create the "ClusterRole" with list of actions performed "across all namespaces"

c. After that, We will assign this ClusterRole to "user" by creating "ClusterRoleBinding"

d. Finally, we will test the above configuration by deploying sample applications.
```

- Creating Kubernetes test User Account(emp) (using x509 for testing RBAC)

```
- Generating Key
openssl genrsa -out emp.key 2048

- Generaing Certificate Signing request (csr):
openssl req -new -key emp.key -out emp.csr -subj "/CN=emp"

- Singing CSR using K8s Cluster "Certificate" and "Key"
openssl x509 -req -in emp.csr \
        -CA /etc/kubernetes/pki/ca.crt \
        -CAkey /etc/kubernetes/pki/ca.key \
        -CAcreateserial \
        -out emp.crt -days 300

- Adding user credentials to "kubeconfig" file
kubectl config set-credentials emp  --client-certificate=emp.crt --client-key=emp.key

- Creating context for this user and associating it with our cluster:
kubectl config set-context emp-context --cluster=kubernetes --user=emp

- Displaying K8s Cluster Config
kubectl config view

- Creating Namespaces and Pod for testing RBAC:
kubectl create ns test-ns1
kubectl create ns test-ns2

- Creating test Pod:
#Pod
kubectl run nginx-pod-default --image=nginx
kubectl run redis-pod-ns1 --image=redis -n test-ns1
kubectl run httpd-pod-ns2 --image=busybox -n test-ns2

- Test Before Deploying:
kubectl get pods --user=emp
kubectl get pods -n test-ns1 --user=emp
kubectl get pods -n test-ns2 --user=emp 
kubectl get pods -n kube-system --user=emp
kubectl get pods -A --user=emp

- Creating a "ClusterRole" & "ClusterRoleBinding":

- Creating Resources Declaratively (Using YAML):
---
# ClusterRole
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: clusterrole-monitoring
rules:
- apiGroups: [""] 
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
---

# ClusterRoleBinding
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: clusterrole-binding-monitoring
subjects:
- kind: User
  name: emp 
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole 
  name: clusterrole-monitoring
  apiGroup: rbac.authorization.k8s.io

- Creating Resources Imperatively (Commands):
# Cluster-role
kubectl create clusterrole clusterrole-monitoring --verb=get,list,watch --resource=pods

# Cluster-rolebinding
kubectl create clusterrolebinding clusterrole-binding-monitoring --clusterrole=clusterrole-monitoring --user=emp

- Display ClusterRole and ClusterRoleBinding:
# clusterrole
kubectl get clusterrole | grep clusterrole-monitoring

# clusterrolebinding
kubectl get clusterrolebinding | grep clusterrole-binding-monitoring

- Describe Cluster-role and Cluster-rolebinding
kubectl describe clusterrole clusterrole-monitoring
kubectl describe clusterrolebinding clusterrole-binding-monitoring

- Testing ClusterRole & ClusterRoleBinding:
#Pod Operations: get, list, watch - in "kube-system", "default", "test-ns1", and "test-ns2" namespaces:
kubectl auth can-i get pods -n kube-system --user=emp
kubectl auth can-i get pods -n default --user=emp
kubectl auth can-i get pods -n test-ns1 --user=emp
kubectl auth can-i get pods -n test-ns2 --user=emp

kubectl get pods -n kube-system --user=emp
kubectl get pods -n default --user=emp
kubectl get pods -n test-ns1 --user=emp
kubectl get pods -n test-ns2 --user=emp

- Creating Objects in "default" (or in any other) namespace: 
kubectl auth can-i create pods --user=emp
kubectl auth can-i create services --user=emp
kubectl auth can-i create deployments --user=emp

kubectl run redis-pod --image=redis --user=emp
kubectl create deploy redis-deploy --image=redis --user=emp

- Deleting Objects in "default" (or in any other) namespace: 
kubectl auth can-i delete pods --user=emp
kubectl auth can-i delete services --user=emp
kubectl auth can-i delete deployments --user=emp

kubectl delete pods nginx-pod --user=emp

- Delete ClusterRole and ClusterRoleBinding:
kubectl delete clusterrole clusterrole-monitoring 
kubectl delete clusterrolebinding clusterrole-binding-monitoring

- Removing User and Context from Cluster Config
kubectl config unset users.emp
kubectl config unset contexts.emp-context

- Ensure user "emp" and its configuration is removed:
kubectl get pods --user=emp
kubectl config view

- Deleting Pods:
kubectl delete pod nginx-pod-default 
kubectl delete pod redis-pod-ns1 -n test-ns1
kubectl delete pod httpd-pod-ns2 -n test-ns2

- Deleting Namespace:
kubectl delete ns test-ns1
kubectl delete ns test-ns2

- Validating:
kubectl get ns
kubectl get pods
kubectl get clusterrole | grep monitoring
kubectl get clusterrolebinding | grep monitoring
```

- check stretegy type in Deployment

```
kubectl describe deploy testcore | grep StrategyType
```

- Creating Deployment Declaratively (Using YAML file)

```
# nginx-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deploy
spec:
  replicas: 3
  stretegy:
    type: RollingUpdate/Recretae
    RollingUpdate:
      maxSurge: 2        #maximum no. of pods rollout during deployment
      maxUnavailable: 0
  selector:
    matchLabels:
      app: nginx-app
  template:
    metadata:
      name: nginx-pod
      labels:
        app: nginx-app
    spec:
      containers:
      - name: nginx-container
        image: nginx:1.18
        ports:
        - containerPort: 80
```

- Deploying

```
kubectl apply -f nginx-deploy.yaml
kubectl create -f nginx-deploy.yaml
```

- Creating Deployment "Imperatively" (from command line):

```
kubectl create deployment NAME --image=[IMAGE-NAME] --replicas=[NUMBER]
```

- For dry-run: It tests to ensure were there any issues. Will NOT create the Object:

```
kubectl create deployment NAME --image=[IMAGE-NAME] --replicas=[NUMBER] --dry-run=client
Ex:
kubectl create deployment redis-deploy --image=redis --replicas=3 --dry-run=client
```

- Exporting Dry-run output to YAML format:

```
kubectl create deployment nginx-deploy --image=nginx --replicas=2 --dry-run=client -o yaml
Ex:
kubectl create deployment redis-deploy --image=redis --replicas=3 --dry-run=client -o yaml
kubectl create deployment redis-deploy --image=redis --replicas=3 --dry-run=client -o yaml > redis-deploy.yaml
```

- Displaying Deployment

```
kubectl get deploy <NAME>
kubectl get deploy <NAME> -o wide
kubectl get deploy <NAME> -o yaml
kubectl describe deploy <NAME>
```

- Print Details of Pod Created by this Deployment

```
kubectl get pods --show-labels
kubectl get pods -l [LABEL]
EX: kubectl get pods -l app=nginx-app
```

- Print Details of ReplicaSet Created by this Deployment:

```
kubectl get rs --show-labels
kubectl get rs -l [LABEL]
EX: kubectl get rs -l app=nginx-app
```

- Scaling Applications:

```
kubectl scale deploy [DEPLOYMENT-NAME] --replicas=[COUNT]     # Update the replica-count to 5
```

- Edit the Deployment:

```
kubectl edit deploy [DEPLOYMENT-NAME]
```

- Running operations directly on the YAML file:

```
SYNTAX: kubectl [OPERATION] –f [FILE-NAME.yaml]
kubectl get –f [FILE-NAME.yaml]
kubectl describe –f [FILE-NAME.yaml]
kubectl edit –f [FILE-NAME.yaml]
kubectl delete –f [FILE-NAME.yaml]
kubectl create –f [FILE-NAME.yaml]
```

- Delete the Deployment:

```
kubectl delete deploy <NAME>
```

- Creating Deployment "Imperatively" (from command line):

```
kubectl create deployment NAME --image=[IMAGE-NAME] --replicas=[NUMBER]
EX: 
kubectl create deployment nginx-deploy --image=nginx:1.18 --replicas=4
```

- Upgrading Deployment with new Image:
  
  ```
  kubectl set image deploy [DEPLOYMENT-NAME] [CONTAINER-NAME]=[CONTAINER-IMAGE]:[TAG] --record
  EX: 
  kubectl set image deploy nginx-deploy nginx=nginx:1.91 --record
  ```

- Checking Rollout Status:
  
  ```
  kubectl rollout status deploy [DEPLOYMENT-NAME]
  EX: 
  kubectl rollout status deploy nginx-deploy
  Waiting for deployment "nginx-deploy" rollout to finish: 2 out of 4 new replicas have been updated...
  ```

- **NOTE**: There is some issue. To dig deep, let's check rollout history.

- Checking Rollout History:
  
  ```
  kubectl rollout history deploy [DEPLOYMENT-NAME]
  # EX: 
  # root@master:~# kubectl rollout history deploy nginx-deploy
  # deployment.apps/nginx-deploy
  # REVISION  CHANGE-CAUSE
  # 1         kubectl set image deploy nginx-deploy nginx-container=nginx:1.91 --record=true
  # 2         kubectl set image deploy nginx-deploy nginx=nginx:1.91 --record=true
  ```

# NOTE: From the output, you can see the commands that are run previously.

# If you notice, Image tag we used is 1.91 instead of 1.19. Let's rollback!

```
- You can confirm the same from by running
```

kubectl get deploy nginx-deploy -o wide

```
- Doing previous rollout "undo":
```

kubectl rollout undo deployment/[DEPLOYMENT-NAME]
(OR)
kubectl rollout undo deployment [DEPLOYMENT-NAME] --to-revision=[DESIRED-REVISION-NUMBER]
kubectl rollout status deployment/[DEPLOYMENT-NAME]
kubectl get deploy [DEPLOYMENT-NAME] -o wide

```
- Doing Rollout with correct Image version: 
```

kubectl set image deploy [DEPLOYMENT-NAME] [CONTAINER-NAME]=[CONTAINER-IMAGE]:[TAG] --record
kubectl rollout status deploy [DEPLOYMENT-NAME]
kubectl get deploy [DEPLOYMENT-NAME] -o wide

```
- Creating Deployment "Imperatively" (from command line):
```

kubectl create deployment NAME --image=[IMAGE-NAME] --replicas=[NUMBER]
Ex:
kubectl create deployment nginx-deploy --image=nginx --replicas=3

```
- Scaling Deployment using "kubectl scale" command:
```

kubectl scale deployment nginx-deploy --replicas=[NEW-REPLICA-COUNT]

```
- Validate the Replica Count:
```

kubectl get deploy nginx-deploy 
kubectl get rs nginx-deploy
kubect get pods -o wide

```
- configmaps
1. an api object to store custm configuration outside the pod
2. not sensitive data

- inject configmap in pod
1. As a environmental variable
2. Argument to container startup command
3. Files in volume

- Creating Configmap Declaratively (Using YAML file):
```

#Example-1:
apiVersion: v1
kind: ConfigMap
metadata:
  name: env-config-yaml
data:
  ENV_ONE: "va1ue1" 
  ENV_TWO: "va1ue2"

#Example-2:
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-nginx-config-yaml
data:
  my-nginx-config.conf: |-
    server {
      listen 80;
      server_name www.kubia-example.com;
      gzip on;
      gzip_types text/plain application/xml;
      location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
      }
    }
    sleep-interval: 25

```
- Creating ConfigMap Imperatively (from Command line):
```

kubectl create configmap <NAME> <SOURCE>

```
- From Literal value:
```

kubectl create configmap env-config-cmd --from-literal=ENV_ONE=value1 --from-literal=ENV_TWO=value2

```
- From File:
```

kubectl create configmap my-ngix-config-file-cmd --from-file=/path/to/configmap-file.txt
kubectl create configmap my-config --from-file=path/to/bar

```
- Displaying ConfigMap:
```

kubectl get configmap <NAME>
kubectl get configmap <NAME> -o wide
kubectl get configmap <NAME> -o yaml
kubectl get configmap <NAME> -o json
kubectl describe configmap <NAME>

```
- Editing ConfigMap:
```

kubectl edit configmap <NAME>

```
- Injecting ConfigMap into Pod As Environment Variables (1/3):
```

# cm-pod-env.yaml

apiVersion: v1
kind: Pod
metadata:
  name: cm-pod-env
spec:
  containers:
    - name: test-container
      image: nginx
      env:
      - name: ENV_VARIABLE_1
        valueFrom:
          configMapKeyRef:
            name: env-config-yaml
            key: ENV_ONE
      - name: ENV_VARIABLE_2
        valueFrom:
          configMapKeyRef:
            name: env-config-yaml
            key: ENV_TWO
  restartPolicy: Never

```
- Deploy:
```

kubectl apply -f cm-pod-env.yaml

```
- Validate:
```

kubectl exec cm-pod-env -- env | grep ENV

```
- Injecting ConfigMap into Pod As Arguments(2/2):
```

# cm-pod-arg.yaml

apiVersion: v1
kind: Pod
metadata:
  name: cm-pod-arg
spec:
  containers:
    - name: test-container
      image: k8s.gcr.io/busybox
      command: [ "/bin/sh", "-c", "echo $(ENV_VARIABLE_1) and $(ENV_VARIABLE_2)" ]
      env:
      - name: ENV_VARIABLE_1
        valueFrom:
          configMapKeyRef:
            name: env-config-yaml
            key: ENV_ONE
      - name: ENV_VARIABLE_2
        valueFrom:
          configMapKeyRef:
            name: env-config-yaml
            key: ENV_TWO
  restartPolicy: Never

```
- Deploy:
```

kubectl apply -f cm-pod-arg.yaml

```
- Validate:
```

kubectl logs cm-pod-arg

```
- Injecting ConfigMap into As Files inside Volume(3/3):
```

# cm-pod-file-vol.yaml

apiVersion: v1
kind: Pod
metadata:
  name: cm-pod-file-vol
spec:
  volumes:
    - name: mapvol
      configMap:
        name: my-nginx-config-yaml
  containers:
    - name: test-container
      image: nginx
      volumeMounts:
      - name: mapvol
        mountPath: /etc/config
  restartPolicy: Never

```
- Deploy:
```

kubectl apply -f cm-pod-file-vol.yaml

```
- Validate:
```

kubectl exec configmap-vol-pod -- ls /etc/config
kubectl exec configmap-vol-pod -- cat /etc/config/etc/config/my-nginx-config.conf

```
- Running operations directly on the YAML file:
```

kubectl [OPERATION] –f [FILE-NAME.yaml]
kubectl get –f [FILE-NAME.yaml]
kubectl delete –f [FILE-NAME.yaml]
kubectl get -f [FILE-NAME.yaml]
kubectl create -f [FILE-NAME.yaml]

```
- Delete ConfigMap:
```

kubectl delete configmap <NAME>

```
- Creating Secrets Declaratively (Using YAML):
```

#Base-64 Encoding:
---------------------

echo -n 'admin' | base64
echo -n '1f2d1e2e67df' | base64

```
- Using Base64 Encoding in creating Secret:
```

# db-user-pass.yaml

apiVersion: v1
kind: Secret
metadata:
  name: db-user-pass
  namespace: default
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm

```
- Deploy:
```

kubectl apply –f secret-db-user-pass.yaml 

```
- Creating Secrets Imperatively (From Command line):
If you want to skip the Base64 encoding step, you can create the same Secret using the kubectl create secret command. This is more convinient.
```

#Example:
-------

kubectl create secret generic test-secret --from-literal='username=my-app' --from-literal='password=39528$vdg7Jb'

#Example:
--------

echo -n 'admin' > ./username.txt
echo -n '1f2d1e2e67df' > ./password.txt

kubectl create secret [TYPE] [NAME] [DATA]

#Example
--------

kubectl create secret generic db-user-pass-from-file --from-file=./username.txt --from-file=./password.txt

#Example:
--------

kubectl get secrets db-user-pass –o yaml

```
- Injecting "Secrets" into Pod As Environmental Variables:
```

# my-secrets-pod-env.yaml

apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:

- name: mycontainer
  image: redis
  env:
  
  - name: SECRET_USERNAME
    valueFrom:
      secretKeyRef:
    
        name: db-user-pass
        key: username
  
  - name: SECRET_PASSWORD
    valueFrom:
      secretKeyRef:
    
        name: db-user-pass
        key: password
    
    restartPolicy: Never
    
    ```
    
    ```

- Validate:
  
  ```
  kubectl exec secret-env-pod -- env
  kubectl exec secret-env-pod -- env | grep SECRET
  ```

- Injecting "Secrets" into Pod As Files inside the Volume:
  
  ```
  # my-secrets-vol-pod.yaml
  apiVersion: v1
  kind: Pod
  metadata:
  name: secret-vol-pod
  spec:
  containers:
    - name: test-container
      image: nginx
      volumeMounts:
        - name: secret-volume
          mountPath: /etc/secret-volume
  volumes:
    - name: secret-volume
      secret:
        secretName: test-secret
  ```

- Validate:
  
  ```
  kubectl exec secret-vol-pod -- ls /etc/secret-volume
  kubectl exec secret-vol-pod -- cat /etc/secret-volume/username
  kubectl exec secret-vol-pod -- cat /etc/secret-volume/password
  ```

- Displaying Secret:
  
  ```
  kubectl get secret <NAME>
  kubectl get secret <NAME> -o wide
  kubectl get secret <NAME> -o yaml
  kubectl get secret <NAME> -o json
  kubectl describe secret <NAME>
  ```

- Running operations directly on the YAML file:
  
  ```
  kubectl [OPERATION] –f [FILE-NAME.yaml]
  kubectl get –f [FILE-NAME.yaml]
  kubectl delete –f [FILE-NAME.yaml]
  kubectl get -f [FILE-NAME.yaml]
  kubectl create -f [FILE-NAME.yaml]
  ```

- Delete Secret: 
  
  ```
  kubectl delete secret <NAME>
  ```

- Labeling Node:
  
  ```
  kubectl get nodes --show-labels
  kubectl label nodes worker-1 disktype=ssd
  kubectl get nodes --show-labels
  kubectl get pods -o wide
  ```

- Deploying Node-Selector YAML:
  
  ```
  # nodeSelector-pod.yaml
  apiVersion: v1
  kind: Pod
  metadata:
  name: nodeselector-pod
  labels:
    env: test
  spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  nodeSelector:
    disktype: ssd
  kubectl apply -f ns.yaml
  ```

- Testing:
  
  ```
  kubectl get pods -o wide
  kubectl get nodes --show-labels
  ```

- Let's Delete and Deploy "again" to ensure Pod is deployed on the same node which is lablelled above.
  
  ```
  kubectl delete -f ns.yaml
  kubectl apply -f ns.yaml
  kubectl get pods -o wide
  kubectl get nodes --show-labels
  ```

- Cleanup:
  
  ```
  kubectl label nodes worker-1 disktype-
  kubectl delete pods nodeselector-pod
  ```

- Configuring Container with "Memory" Requests and Limits:

```
- First, get the output of kubectl top command to find resources that are "currently consumed".
kubectl top nodes

- Then, deploy this Pod with memory requests and limits as mentioned below
#memory-demo.yaml
apiVersion: v1
kind: Pod
metadata:
  name: memory-demo
spec:
  containers:
  - name: memory-demo-ctr
    image: polinux/stress
    resources:
      requests:
        memory: "100Mi"
      limits:
        memory: "200Mi"
    command: ["stress"]
    args: ["--vm", "1", "--vm-bytes", "150M", "--vm-hang", "1"]


# The args section in the configuration file provides arguments for the Container when it starts. 
# The "--vm-bytes", "150M" arguments tell the Container to attempt to allocate 150 MiB of memory.
```

- Deploy:
  
  ```
  kubectl apply -f memory-demo.yaml
  ```

- Validate
  
  ```
  kubectl get pods -o wide
  kubectl top nodes
  ```

- If the respective worker node has morethan 150Mi memory, then Pod should be running successfully.
  
  - Requests(Minimum Resource Quota) - specify, Pod should be scheduled on node which can minimum gurantee this Pod with 100Mi
  
  - Limits(Maximum Resource Quota)   - If the node has morethan 100Mi memory free space, it can use remaining space upto 200Mi Max.

- Manifest Management & Templating Tools
  
  ```
  # List DNS Zone
  az aks show --resource-group myResourceGroup --name myAKSCluster --query addonProfiles.httpApplicationRouting.config.HTTPApplicationRoutingZoneName -o table
  ```

- Instead of providing the -f option to kubectl to direct Kubernetes to create resources from a file, you provide -k and a directory (in this case,
  denotes the current directory). This instructs kubectl to use Kustomize and to inspect that directory’s kustomization.yml.
  
  ```
  kubectl apply -k .
  ```

- Creating Sample Deployment and Service "Declaratively (Using YAML file)":
  
  ```
  #nginx-deploy.yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
  name: nginx-deployment
  labels:
    app: nginx-app
  spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-app
  template:
    metadata:
      labels:
        app: nginx-app
    spec:
      containers:
      - name: nginx-container
        image: nginx:1.18
        ports:
        - containerPort: 80
  ```

- NodePort Service YAML file:
  
  ```
  # nginx-svc-np.yaml
  apiVersion: v1
  kind: Service    
  metadata:
  name: my-service
  labels:
    app: nginx-app
  spec:
  selector:
    app: nginx-app
  type: NodePort
  ports:
  - nodePort: 31111
    port: 80
    targetPort: 80
  ```

- Deploying Applications:
  
  ```
  kubectl apply -f nginx-deploy.yaml
  kubectl apply -f nginx-svc-np.yaml
  ```

- Creating Deployment and NodePort Service Application "Imperatively (From Command promp)":
  
  ```
  kubectl create deployment [DEPLOYMENT-NAME] --image=[CONTAINER-IMAGE]--replicas=[REPLICA-COUNT]
  ```
  
  ```
  kubectl expose deployment [DEPLOYMENT-NAME] --type=NodePort --name=[SERVICE-NAME] --port=[PORT-NUMBER]
  ```

- End-to-End Testing:
  NOTE-1: Before you test, please sure ensure you have created two network rules and assigned to nodes accordingly.

- Firewall Rules: 
  
  | Node Type       | Protocol | Ports                           |
  | --------------- | -------- | ------------------------------- |
  | **Master Node** | TCP      | 2379, 6443, 10250, 10251, 10252 |
  | **Worker Node** | TCP      | 10250, 30000-32767              |

- Create Sample Deployment
  
  ```
  kubectl create deployment test --image=nginx --replicas=3
  ```

- Next, expose the previous Deployment:
  
  ```
  kubectl expose deployment test --type=NodePort --name=test-svc --port=80
  ```

- Now, get the NodePort service number on which this service is exposed on:
  
  ```
  kubectl get svc
  ```

- Next, get the external IP address of the worker node on which this Pod is running
  
  ```
  kubectl get pods -o wide
  ```

- Then, you can open the any browser or execute curl command as mentioned below.

- The syntax is the external IP of the worker node followed by nodePort number
  
  ```
  root@master:~# curl http://35.224.90.242:31506/
  <!DOCTYPE html>
  <html>
  <head>
  <title>Welcome to nginx!</title>
  <style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
  </style>
  ```

- Cleanup
  
  ```
  kubectl delete deploy [NAME]
  kubectl delete svc [NAME]
  ```

- Service Discovery through DNS:

```
- Deploy sample POD:
kubectl run [POD-NAME] --image=[IMAGE-NAME] --port=80

- Expose above app by creating ClusterIP service
kubectl expose pod [POD-NAME]

- Find the Service created as expected
kubectl get svc 
or
kubectl get svc -A

- Validate Service Discover by deploying sample application
kubectl run busybox --image=busybox:1.28 --rm --restart=OnFailure -ti -- /bin/nslookup [SERVICE-NAME]

- End-to-End Testing (Example):
#run pod
kubectl run nginx-pod --image=nginx --port=80
pod/nginx-pod created

#expose pod by svc
kubectl expose pod nginx-pod
service/nginx-pod exposed

#check svc
kubectl get svc
NAME           TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
kubernetes     ClusterIP   10.8.0.1      <none>        443/TCP   8m24s
nginx-pod      ClusterIP   10.8.13.206   <none>        80/TCP    18s

#check all SVC
kubectl get svc -A
NAMESPACE     NAME                   TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)         AGE
default       kubernetes             ClusterIP   10.8.0.1      <none>        443/TCP         8m32s
default       nginx-pod              ClusterIP   10.8.13.206   <none>        80/TCP          26s
kube-system   default-http-backend   NodePort    10.8.13.240   <none>        80:30534/TCP    8m17s
kube-system   kube-dns               ClusterIP   10.8.0.10     <none>        53/UDP,53/TCP   8m17s ****
kube-system   metrics-server         ClusterIP   10.8.14.200   <none>        443/TCP         8m15s

#run pod 
kubectl run busybox --image=busybox:1.28 --rm --restart=OnFailure -ti
If you don't see a command prompt, try pressing enter.
/ # nslookup nginx-pod
Server:    10.8.0.10
Address 1: 10.8.0.10 kube-dns.kube-system.svc.cluster.local

Name:      nginx-pod
Address 1: 10.8.13.206 nginx-pod.default.svc.cluster.local
/ #
/ # exit
pod "busybox" deleted

#run command in pod
kubectl run busybox --image=busybox:1.28 --rm --restart=OnFailure -ti -- /bin/nslookup nginx-pod > nginx-svc-out.txt

#check previous command output
cat nginx-svc-out.txt
Server:    10.8.0.10
Address 1: 10.8.0.10 kube-dns.kube-system.svc.cluster.local

Name:      nginx-pod
Address 1: 10.8.13.206 nginx-pod.default.svc.cluster.local
pod "busybox" deleted
```

- **Practice Exercise**: Deploy sample application, then expose and ensure it creates respetive endpoints

```
#Solution: Deploy sample application, then expose and ensure it creates respetive endpoints:
root@master:~# kubectl create deployment test-deploy --image=nginx --replicas=3 --port=80
deployment.apps/test-deploy created
root@master:~#

root@master:~# kubectl expose deploy test-deploy
service/test-deploy exposed
root@master:~#

root@master:~# kubectl get svc | grep test-deploy
test-deploy    ClusterIP   10.105.64.47    <none>        80/TCP         49s
root@master:~#

root@master:~# kubectl get pods -o wide | grep test-deploy
test-deploy-7955784f5c-bq9wz    1/1     Running   0          103s   10.44.0.10   worker   <none>           <none>
test-deploy-7955784f5c-gj98x    1/1     Running   0          103s   10.44.0.12   worker   <none>           <none>
test-deploy-7955784f5c-t7b67    1/1     Running   0          103s   10.44.0.11   worker   <none>           <none>
root@master:~#

root@master:~# kubectl get ep
NAME           ENDPOINTS               AGE
kubernetes     10.128.0.4:6443         8d
nginx-deploy   10.44.0.8:80            54m
test-deploy    10.44.0.10:80,10.44.0.11:80,10.44.0.12:80   59s
test-svc       10.44.0.5:80,10.44.0.6:80,10.44.0.7:80      94m
root@master:~#

root@master:~# kubectl get ep | grep test-deploy
test-deploy    10.44.0.10:80,10.44.0.11:80,10.44.0.12:80   76s
```

- Configure Ingress Controller (Using Helm):

```
#Install Ingress Controller:
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx


#Validate Ingress Controller:
kubectl get deploy | grep ingress
kubectl get svc | grep ingress
kubectl get pod | grep ingress
kubectl get configmap | grep ingress
kubetl get events

#MY OUTPUTS:
kubectl get deploy | grep ingress
ingress-nginx-controller   1/1     1            1           35m

kubectl get svc | grep ingress
ingress-nginx-controller             LoadBalancer   10.8.5.189   34.121.139.23   80:30335/TCP,443:30964/TCP   36m
ingress-nginx-controller-admission   ClusterIP      10.8.15.53   <none>          443/TCP  36m

kubectl get pod | grep ingress
ingress-nginx-controller-f8df76cc4-j9kgg   1/1     Running   0          36m

kubectl get configmap | grep ingress
ingress-controller-leader-nginx   0      36m
ingress-nginx-controller          0      36m

#Using Ingress to access Services:
-> First, will create two Pods and exposing these with services. 
-> And then will create Ingress resource, which routes requests to these services.

#Pod-1 & Service-1 (Cat)
kind: Pod
apiVersion: v1
metadata:
  name: cat-app
  labels:
    app: cat
spec:
  containers:
    - name: cat-app
      image: hashicorp/http-echo
      args:
        - "-text=cat"
---
kind: Service
apiVersion: v1
metadata:
  name: cat-service
spec:
  selector:
    app: cat
  ports:
    - port: 5678  #Default port for image

#Pod-2 & Service-2 (Dog)
kind: Pod
apiVersion: v1
metadata:
  name: dog-app
  labels:
    app: dog
spec:
  containers:
    - name: dog-app
      image: hashicorp/http-echo
      args:
        - "-text=dog"
---
kind: Service
apiVersion: v1
metadata:
  name: dog-service
spec:
  selector:
    app: dog
  ports:
    - port: 5678 # Default port for image

#Ingress resource:
NOTE:
if running Kubernetes version 1.19 and above, use API version as networking.k8s.io/v1
In my case, GKE is running with 1.17, so has to use extensions/v1beata1
apiVersion: extensions/v1beta1  
kind: Ingress
metadata:
  name: test-ingress
  annotations:
    ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
        - path: /cat
          backend:
            serviceName: cat-service
            servicePort: 5678
        - path: /dog
          backend:
            serviceName: dog-service
            servicePort: 5678

#Deploying:
kubectl apply -f cat.yaml
kubectl apply -f dog.yaml
kubectl apply -f ingress.yaml

#Displaing:
kubectl get pods
kubectl get svc
kubectl get ingress

#Testing:
NOTE: 
a. You can open any webrowser and start access the putting external IP address of Ingress Controller, followed by path mentioned in the ingress resource.
b. You can also curl as shown below.

curl http://[EXTERNAL-IP-ADDRESS-OF-INGRESS-CONTROLLER]/cat
curl http://[EXTERNAL-IP-ADDRESS-OF-INGRESS-CONTROLLER]/dog
curl http://[EXTERNAL-IP-ADDRESS-OF-INGRESS-CONTROLLER]/wrong-request

#MY OUTPUTS:
#Deploying:
kubectl apply -f cat.yaml
pod/cat-app created
service/cat-service created

kubectl apply -f dog.yaml
pod/dog-app created
service/dog-service created

kubectl apply -f ingress.yaml
ingress.extensions/example-ingress created

#Displaing:
kubectl get pods
NAME                   READY   STATUS    RESTARTS   AGE
cat-app                1/1     Running   0          67s
dog-app                1/1     Running   0          56s
ingress-nginx-controller-f8df76cc4-j9kgg   1/1     Running   0          52m

#Testing:
kubectl get svc
NAME             TYPE           CLUSTER-IP   EXTERNAL-IP     PORT(S)  AGE
cat-service      ClusterIP      10.8.9.71    <none>          5678/TCP 76s
dog-service      ClusterIP      10.8.1.48    <none>          5678/TCP 65s
ingress-nginx-controller             LoadBalancer   10.8.5.189   34.121.139.23   80:30335/TCP,443:30964/TCP   53m
ingress-nginx-controller-admission   ClusterIP      10.8.15.53   <none>          443/TCP  53m
kubernetes       ClusterIP      10.8.0.1     <none>          443/TCP  57m

kubectl get ingress
NAME           HOSTS   ADDRESS         PORTS   AGE
test-ingress   *       130.211.5.157   80      56s

#Testing:
NOTE: You can open any webrowser and start access the putting external IP address of Ingress Controller, followed by path mentioned in the ingress resource.
curl http://34.121.139.23/cat
cat

curl http://34.121.139.23/dog
dog

curl http://34.121.139.23/wrong-request
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx</center>
</body>
</html>
```

- Deleting dirty pods if any

```
kubectl get po --all-namespaces --field-selector=status.phase=Failed --no-headers -o custom-columns=:metadata.name | xargs kubectl delete po 
```

- HostPath YAML file

```
apiVersion: v1
kind: Pod
metadata:
  name: nginx-hostpath
spec:
  containers:
    - name: nginx-container
      image: nginx
      volumeMounts:
      - mountPath: /test-mnt
        name: test-vol
  volumes:
  - name: test-vol
    hostPath:
      path: /test-vol

#Deploy:
kubectl apply -f nginx-hostpath.yaml

#Displaying Pods and Hostpath
kubectl get pods
kubectl exec nginx-hostpath -- df /test-mnt

#Testing: 
From HOST:

#First, will create the file on the host-path on the worker node where this pod is running.
cd /test-vol
echo "Hello from Host" > from-host.txt
cat from-host.txt

#From POD:
#Next, we will login to the Pod and will create the test file on the host-path directory from inside the Pod.
kubectl exec nginx-hostpath -it -- /bin/sh
cd /test-mnt
echo "Hello from Pod" > from-pod.txt
cat from-pod.txt

#From Host:
#Finally, we will validate that file from the worker node.
cd /test-vol
ls
cat from-pod.txt

#Clean up
kubectl delete po nginx-hostpath
kubectl get po
ls /test-vol

#MY-OUTPUT:
----------
#Deploying:
root@master:~# kubectl apply -f pod-hostpath.yaml
pod/nginx-hostpath created

#Displaying Pods and Hostpath:
root@master:~# kubectl get pods -o wide
NAMEREADY   STATUS    RESTARTS   AGE     IP           NODE     NOMINATED NODE   READINESS GATES
ingress-nginx-controller-7fc74cf778-9vn8d   1/1     Running   0          4h49m   10.44.0.14   worker   <none>           <none>
nginx-hostpath          1/1     Running   0          18s     10.44.0.1    worker   <none>           <none>

root@master:~# kubectl exec nginx-hostpath -- df /test-mnt
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/sda1        9983268 4413176   5553708  45% /test-mnt

#Testing:
#First, will create the file on the host-path on the worker node where this pod is running.
root@worker:/# cd /test-vol
root@worker:/test-vol# echo "Hello from Host" > from-host.txt
root@worker:/test-vol#
root@worker:/test-vol# cat from-host.txt
Hello from Host

#Next, we will login to the Pod and will create the test file on the host-path directory from inside the Pod.
root@master:~# kubectl exec nginx-hostpath -it -- /bin/sh
# cd /test-mnt
# echo "Hello from Pod" > from-pod.txt
# cat from-pod.txt
Hello from Pod

#Finally, we will validate that file from the worker node.
root@worker:/test-vol# ls
from-host.txt  from-pod.txt
root@worker:/test-vol#
root@worker:/test-vol# cat from-pod.txt
Hello from Pod

#Delete the Pod
root@master:~# kubcetl delete -f pod-hostpath.yaml
kubcetl: command not found
root@master:~# kubectl delete -f pod-hostpath.yaml               
pod "nginx-hostpath" deleted

#Files are still there after deleting the Pod
root@worker:/test-vol# ls
from-host.txt  from-pod.txt

#Recreate the Pod with same host-path
root@master:~# kubectl apply -f pod-hostpath.yaml
pod/nginx-hostpath created

#Files are still there (if it is deployed on same worker node)
root@master:~# kubectl exec nginx-hostpath -- ls /test-mnt
from-host.txt
from-pod.txt
```

- On Cluster Configured with Kubeadm

```
#First, login and created the disk.
gcloud auth login
gcloud compute disks create --size=10GB --zone=us-central1-a my-data-disk-1

#Next, create the Pod YAML.
# gce-pd.yaml
apiVersion: v1
kind: Pod
metadata:
  name: gce-pd
spec:
  containers:
  - image: mongo
    name: mongodb
    volumeMounts:
    - name: mongodb-data
      mountPath: /data/db 
  volumes:
  - name: mongodb-data
    gcePersistentDisk:
      pdName: my-data-disk-1
      fsType: ext4

#Deploy.
kubectl apply -f gce-pd.yaml

#Find, the worker node which this Pod is deployed.
kubectl get pods -o wide

#Attach the disk to respective "worker" node from Google Cloud Dashboad.
#login to the respective "worker" node and run following commands
mkfs.ext4 /dev/disk/by-id/scsi-0Google_PersistentDisk_my-data-disk-1
mkdir -p /var/lib/kubelet/plugins/kubernetes.io/gce-pd/mounts/my-data-disk-1 && 
mount /dev/disk/by-id/scsi-0Google_PersistentDisk_my-data-disk-1 /var/lib/kubelet/plugins/kubernetes.io/gce-pd/mounts/my-data-disk-1


#Wait few mins. Then, login to the "master" node and display Pods and it status to ensure it is "Running"
kubectl get pods 


#Validate:
kubectl exec gce-pd -it -- df /data/db

#On GKE:
----------
#First, create the disk.
gcloud compute disks create --size=10GB --zone=us-central1-c my-data-disk-2

#Deploy.
kubectl apply -f gce-pd.yaml

#Cleanup:
kubectl delete pods gce-pd
gcloud compute disks delete --zone=us-central1-a my-data-disk-1
gcloud compute disks delete --zone=us-central1-c my-data-disk-2
```

- Creating Persistent Volume (PV)

```
# pv-volume.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"

#Deploy and Validate:
kubectl apply -f pv-volume.yaml
kubectl get pv task-pv-volume

#Creating Persistent Volume Claim (PVC)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pv-claim
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi

#Deploy and Validate:
kubectl apply -f https://k8s.io/examples/pods/storage/pv-claim.yaml
kubectl get pv task-pv-volume
kubectl get pvc task-pv-claim

#Deploying Pod with PVC
apiVersion: v1
kind: Pod
metadata:
  name: task-pv-pod
spec:
  volumes:
    - name: task-pv-storage
      persistentVolumeClaim:
        claimName: task-pv-claim
  containers:
    - name: task-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-pv-storage

#Deploy and Validate:
kubectl apply -f https://k8s.io/examples/pods/storage/pv-pod.yaml
kubectl get pod task-pv-pod

#Testing
#Identify the node where this Pod is deployed:
kubectl get pods -o wide

#On above respective node create a sample file:
mkdir /mnt/data
sh -c "echo 'Hello from Kubernetes storage' > /mnt/data/index.html"
cat /mnt/data/index.html

#Now get inside the Pod and test it:
kubectl exec -it task-pv-pod -- /bin/bash
apt update
apt install curl
curl http://localhost/

#Cleanup
kubectl delete pod task-pv-pod
kubectl delete pvc task-pv-claim
kubectl delete pv task-pv-volume
```

- change default storage class

```
kubectl patch storageclass DEFAULT -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is default class":"false"}}}'
```

- make our gold storage class as default

```
kubectl patch storageclass GOLD -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is default class":"true"}}}'
```

- Creating Storage Class:

```
#First, notice the the default and exisiting storage class(es) in the cluster
kubectl get sc


#Create "new" Storage Class
# sc-ssd.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-sc
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  fsType: ext4
reclaimPolicy: Retain
allowVolumeExpansion: true
volumeBindingMode: Immediate

#Deploy:
kubectl apply -f sc-ssd.yaml

#Validate status of new Storage Class
kubectl get sc

#Create PVC which uses above "Storage Class"
#PVC YAML file
# pvc-ssd.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: fast-pvc
spec:
  storageClassName: fast-sc  #Using Storage Class created in 1
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi

#Deploy:
kubectl apply -f pvc-ssd.yaml

#Display PVC. Ensure PVC automatically creates new PV in the backend and also it status as Bound
kubectl get pvc
kubectl get pv

#Deploying Pod with PVC
# task-sc-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: fast-pod
spec:
  volumes:
    - name: task-sc-storage
      persistentVolumeClaim:
        claimName: fast-pvc
  containers:
    - name: task-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-sc-storage


#Deploy and Validate:
kubectl apply -f task-sc-pod.yaml
kubectl get pod task-sc-pod
kubectl exec fast-pod -- df

#Cleanup
kubectl delete -f fast-pod.yaml
kubectl delete -f fast-pvc.yaml
kubectl delete -f [PV-NAME]

#Since above storage class has "retain" reclaim policy, we need to manually delete the Disk from Google Cloud dashboard
kubectl delete -f sc-ssd.yaml
```

- Metrics Server Deployment

```
#0. Pre-Req:
Check if your cluster is running with MetricsServer by running following commands
kubectl top nodes
kubectl top pods
kubectl get pods -n kube-system | grep -i metrics

If not, go ahead with below steps. 
#Download:
git clone https://github.com/kubernetes-sigs/metrics-server.git

#Installing Metrics Server:
kubectl apply -k metrics-server/manifests/test

#Give it a minute to gather the data and run this command.
kubectl get pods -n kube-system | grep -i metrics

# Troubleshooting:

#If you encounter any Image error, try updating imagePullPolicy from "Never" to "Always
in metrics-server/manifests/test/patch.yaml

kubectl delete -k metrics-server/manifests/test
vim metrics-server/manifests/test/patch.yaml

#Then update "imagePullPolicy" from "Never" to "Always" - imagePullPolicy: Always  

kubectl apply -k metrics-server/manifests/test
kubectl get pods -n kube-system | grep -i metrics

#Validate:
kubectl get deployment metrics-server -n kube-system 
kubectl get apiservices | grep metrics
kubectl get apiservices | grep metrics
kubectl top pods
kubectl top nodes

#check pod by cpu and memory
kubectl top pod --sort-by CPU/Memory -A(for all namespace)
```

- Deploying sample Pods for "kubectl logs" output purpose:

```
# counter.yaml
apiVersion: v1
kind: Pod
metadata:
  name: one-counter-pod
spec:
  containers:
  - name: counter-container
    image: busybox
    args: [/bin/sh, -c,
            'i=0; while true; do echo "$i: $(date)"; i=$((i+1)); sleep 1; done']
---
apiVersion: v1
kind: Pod
metadata:
  name: two-counter-pod
spec:
  containers:
  - name: counter-1
    image: busybox
    args: [/bin/sh, -c,
            'i=0; while true; do echo "From Counter-ONE: $i: $(date)"; i=$((i+1)); sleep 1; done']
  - name: counter-2
    image: busybox
    args: [/bin/sh, -c,
            'i=0; while true; do echo "From Counter-TWO:  $i: $(date)"; i=$((i+1)); sleep 1; done']
```

- Display Container Logs using "kubectl logs" command:

```
kubectl logs [POD-NAME]    # dump pod logs (stdout)
kubectl logs -f [POD-NAME] # stream pod logs (stdout)
kubectl logs [POD-NAME] –-since=5m              # view logs for last 5 mins (h for hours)
kubectl logs [POD-NAME] --tail=20              # Display only more recent 20 lines of output in pod
kubectl logs [POD-NAME] --previous             # dump pod logs (stdout) for a previous instantiation of a container
kubectl logs [POD-NAME] > [FILE-NAME].log      # Save log output to a file
kubectl logs [POD-NAME] -c [CONTAINER-NAME]    # dump pod container logs (stdout, multi-container case)
kubectl logs [POD-NAME] --all-containers=true  # dump logs of all containers inside nginx pod
kubectl logs -l [KEY]=[VALUE]                  # dump pod logs, with label  (stdout)
```

- Using Journalctl:

```
journalctl  #Display all messages
journalctl -r                   #Display newest log entries first (Latest to Old order)
journalctl -f                   #Enable follow mode & display new messages as they come in
journalctl –n 3                 #Display specific number of RECENT log entries
journalctl –p crit              #Display specific priority – “info”, “warning”, “err”, “crit”, “alert”, “emerg”
journalctl –u docker            #Display log entries of only specific systemd unit
journalctl –o verbose           #Format output in “verbose”, “short”, “json” and more
journalctl –n 3 –p crit         #Combining options
journalctl --since "2019-02-02 20:30:00" --until "2019-03-31 12:00:00"       # Display all messages between specific duration
```

- Display Container Logs using "docker logs" command from respective worker node:

```
kubectl get pods -o wide
docker ps | grep [KEY-WORD]
docker logs [CONTAINER-ID]
```

- K8s Cluster Component Logs:

```
journalctl –u docker
journalctl –u kubelet
```

- If K8s Cluster Configured using "kubeadm":

```
kubectl logs kube-apiserver-master -n kube-system | more
kubectl logs kube-controller-manager-master -n kube-system
kubectl logs kube-scheduler-master -n kube-system
kubectl logs etcd-master -n kube-system
```

- If K8s Cluster Configured using "Hard-way (Manual)"

```
journalctl –u kube-apiserver 
journalctl –u kube-scheduler
journalctl –u etcd
journalctl –u kube-controller-manager 
```

- Troubleshooting Cluster and Nodes:

```
#Check:
------
kubectl get nodes
kubectl top node 
```

- Troubleshooting Components

```
#If cluster configured with "kubeadm"
-------------------------------------------
Check:
------
kubectl get pods -n kube-system
systemctl status kubelet
systemctl status docker

#Troubleshoot:
-------------
kubectl logs kube-apiserver-master -n kube-system
kubectl logs kube-scheduler-master -n kube-system
kubectl logs kube-controller-manager-master -n kube-system
kubectl logs etcd-master -n kube-system

#Possible Solutions(NOTE: Does not covered all):
-----------------------------------------------
Kubelet:
systemctl enable kubelet  #Run it on all nodes (Including worker nodes)
systemctl start kubelet   #Run it on all nodes (Including worker nodes)

Docker:
systemctl enable docker   #Run it on all nodes (Including worker nodes)
systemctl start docker    #Run it on all nodes (Including worker nodes)
```

```
If cluster configured with "Manual (Hard-way)"

Check
-----
systemctl status kube-apiserver
systemctl status kube-controller-manager 
systemctl status kube-scheduler 
systemctl status etcd

systemctl status kubelet # Run it on all nodes (Including worker nodes)
systemctl status docker  # Run it on all nodes (Including worker nodes)


#Troubleshoot
------------
journalctl –u kube-apiserver 
journalctl –u kube-scheduler
journalctl –u etcd
journalctl –u kube-controller-manager 
journalctl –u kube-proxy
journalctl –u docker
journalctl –u kubelet


#Possible Solutions(NOTE: Does not covered all):
------------------------------------------------
systemctl enable kube-apiserver kube-controller-manager kube-scheduler etcd
systemctl start kube-apiserver kube-controller-manager kube-scheduler etcd

Kubelet:
systemctl enable kubelet  #Run it on all nodes (Including worker nodes)
systemctl start kubelet   #Run it on all nodes (Including worker nodes)

Docker:
systemctl enable docker   #Run it on all nodes (Including worker nodes)
systemctl start docker    #Run it on all nodes (Including worker nodes)
```

1. POD:

```
# Start a nginx pod.
kubectl run nginx --image=ngi0nx

# Start a hazelcast pod and let the container expose port 5701
kubectl run hazelcast --image=hazelcast/hazelcast --port=5701 

# Start a hazelcast pod and set labels "app=hazelcast" and "env=prod" in the container
kubectl run hazelcast --image=hazelcast/hazelcast --labels="app=hazelcast,env=prod"

# Start a busybox pod and keep it in the foreground, don't restart it if it exits.
kubectl run -i -t busybox --image=busybox --restart=Never

# Dry run. Print the corresponding API objects without creating them.
kubectl run nginx --image=nginx --dry-run=client
```

2. APPLY:

```
# Apply the configuration in mypod.yaml to a pod
kubectl apply -f mypod.yaml

# Apply the configuration in pod.json to a pod.
kubectl apply -f ./pod.json

# Apply resources from a directory containing kustomization.yaml - e.g. dir/kustomization.yaml.
kubectl apply -k dir/

# Apply the JSON passed into stdin to a pod.
cat pod.json | kubectl apply -f -

# Note: --prune is still in Alpha # Apply the configuration in manifest.yaml that matches label app=nginx and delete all the other resources that are not in the file and match label app=nginx.
kubectl apply --prune -f manifest.yaml -l app=nginx
```

3. EDIT:

```
# Edit the deployment 'mydeployment' in YAML and save the modified config in its annotation:
kubectl edit deployment/mydeployment -o yaml --save-config
```

4. DELETE:

```
# Delete a pod using the type and name specified in pod.json.
kubectl delete -f ./pod.json

# Delete resources from a directory containing kustomization.yaml - e.g. dir/kustomization.yaml.
kubectl delete -k dir

# Delete pods and services with same names "baz" and "foo"
kubectl delete pod,service baz foo

# Delete pods and services with label name=myLabel.
kubectl delete pods,services -l name=myLabel

# Delete a pod with minimal delay
kubectl delete pod foo --now

# Force delete a pod on a dead node
kubectl delete pod foo --force

# Delete all pods
kubectl delete pods --all
```

5. NAMESPACE:

```
Create a new namespace named my-namespace
kubectl create namespace my-namespace
```

6. LABEL:

```
# Update pod 'foo' with the label 'unhealthy' and the value 'true'.
kubectl label pods foo unhealthy=true

# Update pod 'foo' with the label 'status' and the value 'unhealthy', overwriting any existing value.
kubectl label --overwrite pods foo status=unhealthy

# Update all pods in the namespace
kubectl label pods --all status=unhealthy

# Update a pod identified by the type and name in "pod.json"
kubectl label -f pod.json status=unhealthy

# Update pod 'foo' only if the resource is unchanged from version 1.
kubectl label pods foo status=unhealthy --resource-version=1

# Update pod 'foo' by removing a label named 'bar' if it exists. # Does not require the --overwrite flag.
kubectl label pods foo bar-
```

7. DESCRIBE:

```
# Describe a node
kubectl describe nodes kubernetes-node-emt8.c.myproject.internal

# Describe a pod
kubectl describe pods/nginx

# Describe a pod identified by type and name in "pod.json"
kubectl describe -f pod.json

# Describe all pods
kubectl describe pods

# Describe pods by label name=myLabel
kubectl describe po -l name=myLabel

# Describe all pods managed by the 'frontend' replication controller (rc-created pods # get the name of the rc as a prefix in the pod the name).
kubectl describe pods frontend
```

8. EXEC:

```
# Get output from running 'date' command from pod mypod, using the first container by default
kubectl exec mypod -- date

# Get output from running 'date' command in ruby-container from pod mypod
kubectl exec mypod -c ruby-container -- date

# Switch to raw terminal mode, sends stdin to 'bash' in ruby-container from pod mypod # and sends stdout/stderr from 'bash' back to the client
kubectl exec mypod -c ruby-container -i -t -- bash -il

# Get output from running 'date' command from the first pod of the deployment mydeployment, using the first container by default
kubectl exec deploy/mydeployment -- date

# Get output from running 'date' command from the first pod of the service myservice, using the first container by default
kubectl exec svc/myservice -- date
```

9. LOGS:

```
# Return snapshot logs from pod nginx with only one container
kubectl logs nginx

# Return snapshot logs from pod nginx with multi containers
kubectl logs nginx --all-containers=true

# Display only the most recent 20 lines of output in pod nginx
kubectl logs --tail=20 nginx

# Show all logs from pod nginx written in the last hour
kubectl logs --since=1h nginx

# Return snapshot logs from first container of a job named hello
kubectl logs job/hello

# Return snapshot logs from container nginx-1 of a deployment named nginx
kubectl logs deployment/nginx -c nginx-1
```

10. TOP:

```
# Show metrics for all nodes
kubectl top node

# Show metrics for a given node
kubectl top node NODE_NAME

# Show metrics for all pods in the default namespace
kubectl top pod

# Show metrics for all pods in the given namespace
kubectl top pod --namespace=NAMESPACE

# Show metrics for a given pod and its containers
kubectl top pod POD_NAME --containers

# Show metrics for the pods defined by label name=myLabel
kubectl top pod -l name=myLabe
```

11. SERVICE ACCOUNT:

```
# Set Deployment nginx-deployment's ServiceAccount to serviceaccount1
kubectl set serviceaccount deployment nginx-deployment serviceaccount1

# Print the result (in yaml format) of updated nginx deployment with serviceaccount from local file, without hitting apiserver
kubectl set sa -f nginx-deployment.yaml serviceaccount1 --local --dry-run=client -o yaml
```

12. DEPLOYMENT:

```
# Create a deployment named my-dep that runs the busybox image.
kubectl create deployment my-dep --image=busybox

# Create a deployment with command
kubectl create deployment my-dep --image=busybox -- date

# Create a deployment named my-dep that runs the nginx image with 3 replicas.
kubectl create deployment my-dep --image=nginx --replicas=3

# Create a deployment named my-dep that runs the busybox image and expose port 5701.
kubectl create deployment my-dep --image=busybox --port=5701
```

13. SCALE:

```
# If the deployment named mysql's current size is 2, scale mysql to 3
kubectl scale --current-replicas=2 --replicas=3 deployment/mysql

# Scale a replicaset named 'foo' to 3.
kubectl scale --replicas=3 rs/foo

# Scale a resource identified by type and name specified in "foo.yaml" to 3.
kubectl scale --replicas=3 -f foo.yaml
```

14. SET:

```
# Set a deployment's nginx container image to 'nginx:1.9.1', and its busybox container image to 'busybox'.
kubectl set image deployment/nginx busybox=busybox nginx=nginx:1.9.1

# Update all deployments' and rc's nginx container's image to 'nginx:1.9.1'
kubectl set image deployments,rc nginx=nginx:1.9.1 --all

# Update image of all containers of daemonset abc to 'nginx:1.9.1'
kubectl set image daemonset abc *=nginx:1.9.1
```

15. ROLLBACK:

```
# Rollback to the previous deployment
kubectl rollout undo deployment/abc

# Check the rollout status of a daemonset
kubectl rollout status daemonset/foo
```

16. Rollout HISTORY:

```
# View the rollout history of a deployment
kubectl rollout history deployment/abc

# View the details of daemonset revision 3
kubectl rollout history daemonset/abc --revision=3
```

17. Rollout UNDO:

```
# Rollback to the previous deployment
kubectl rollout undo deployment/abc

# Rollback to daemonset revision 3
kubectl rollout undo daemonset/abc --to-revision=3

# Rollback to the previous deployment with dry-run
kubectl rollout undo --dry-run=server deployment/abc
```

18. SERVICE:

```
a. Create Service:
-----------------
# Create a new ClusterIP service named my-cs
kubectl create service clusterip my-cs --tcp=5678:8080

# Create a new ClusterIP service named my-cs (in headless mode)
kubectl create service clusterip my-cs --clusterip="None"

# Create a new NodePort service named my-ns
kubectl create service nodeport my-ns --tcp=5678:8080

b. Creating Resources by Exposing a Resource:
---------------------------------------------

# create a service for a replicated nginx, which serves on port 80 and connects to the containers on port 8000.
kubectl expose rc nginx --port=80 --target-port=8000

# Create a service for a replication controller identified by type and name specified in "nginx-controller.yaml", which serves on port 80 and connects to the containers on port 8000.
kubectl expose -f nginx-controller.yaml --port=80 --target-port=8000

# Create a service for a pod valid-pod, which serves on port 444 with the name "frontend"
kubectl expose pod valid-pod --port=444 --name=frontend

# Create a second service based on the above service, exposing the container port 8443 as port 443 with the name "nginx-https"
kubectl expose service nginx --port=443 --target-port=8443 --name=nginx-https

# Create a service for a replicated streaming application on port 4100 balancing UDP traffic and named 'video-stream'.
kubectl expose rc streamer --port=4100 --protocol=UDP --name=video-stream

# Create a service for a replicated nginx using replica set, which serves on port 80 and connects to the containers on port 8000.
kubectl expose rs nginx --port=80 --target-port=8000

# Create a service for an nginx deployment, which serves on port 80 and connects to the containers on port 8000.
kubectl expose deployment nginx --port=80 --target-port=8000
```

19. CONFIGMAP:

```
# Create a new configmap named my-config based on folder bar
kubectl create configmap my-config --from-file=path/to/bar

# Create a new configmap named my-config with specified keys instead of file basenames on disk
kubectl create configmap my-config --from-file=key1=/path/to/bar/file1.txt --from-file=key2=/path/to/bar/file2.txt

# Create a new configmap named my-config with key1=config1 and key2=config2
kubectl create configmap my-config --from-literal=key1=config1 --from-literal=key2=config2

# Create a new configmap named my-config from the key=value pairs in the file
kubectl create configmap my-config --from-file=path/to/bar

# Create a new configmap named my-config from an env file
kubectl create configmap my-config --from-env-file=path/to/bar.env
```

20. SECRET (Generic)

```
# Create a new secret named my-secret with keys for each file in folder bar
kubectl create secret generic my-secret --from-file=path/to/bar

# Create a new secret named my-secret with specified keys instead of names on disk
kubectl create secret generic my-secret --from-file=ssh-privatekey=path/to/id_rsa --from-file=ssh-publickey=path/to/id_rsa.pub

# Create a new secret named my-secret with key1=supersecret and key2=topsecret
kubectl create secret generic my-secret --from-literal=key1=supersecret --from-literal=key2=topsecret

# Create a new secret named my-secret using a combination of a file and a literal
kubectl create secret generic my-secret --from-file=ssh-privatekey=path/to/id_rsa --from-literal=passphrase=topsecret

# create a new secret named my-secret from an env file
kubectl create secret generic my-secret --from-env-file=path/to/bar.env
```

21. JOB:

```
# Create a job
kubectl create job my-job --image=busybox

# Create a job with command
kubectl create job my-job --image=busybox -- date

# Create a job from a CronJob named "a-cronjob"
kubectl create job test-job --from=cronjob/a-cronjob
```

22. CRONJOB:

```
# Create a cronjob
kubectl create cronjob my-job --image=busybox --schedule="*/1 * * * *"

# Create a cronjob with command
kubectl create cronjob my-job --image=busybox --schedule="*/1 * * * *" -- date
```

23. CORDON:

```
# Mark node "foo" as unschedulable.
kubectl cordon foo
```

24. DRAIN:

```
# Drain node "foo", even if there are pods not managed by a ReplicationController, ReplicaSet, Job, DaemonSet or StatefulSet on it.
kubectl drain foo --force

# As above, but abort if there are pods not managed by a ReplicationController, ReplicaSet, Job, DaemonSet or StatefulSet, and use a grace period of 15 minutes.
kubectl drain foo --grace-period=900
```

25. TAINT:

```
# Update node 'foo' with a taint with key 'dedicated' and value 'special-user' and effect 'NoSchedule'. # If a taint with that key and effect already exists, its value is replaced as specified.
kubectl taint nodes foo dedicated=special-user:NoSchedule

# Remove from node 'foo' the taint with key 'dedicated' and effect 'NoSchedule' if one exists.
kubectl taint nodes foo dedicated:NoSchedule-

# Remove from node 'foo' all the taints with key 'dedicated'
kubectl taint nodes foo dedicated-

# Add a taint with key 'dedicated' on nodes having label mylabel=X
kubectl taint node -l myLabel=X  dedicated=foo:PreferNoSchedule

# Add to node 'foo' a taint with key 'bar' and no value
kubectl taint nodes foo bar:NoSchedule
```

26. UNCORDON:

```
# Mark node "foo" as schedulable.
kubectl uncordon foo
```

27. CLUSTERROLE:

```
# Create a ClusterRole named "pod-reader" that allows user to perform "get", "watch" and "list" on pods
kubectl create clusterrole pod-reader --verb=get,list,watch --resource=pods

# Create a ClusterRole named "pod-reader" with ResourceName specified
kubectl create clusterrole pod-reader --verb=get --resource=pods --resource-name=readablepod
```

28. CLUSTERROLEBINDING:

```
# Create a ClusterRoleBinding for user1, user2, and group1 using the cluster-admin ClusterRole
kubectl create clusterrolebinding cluster-admin --clusterrole=cluster-admin --user=user1 --user
```

29. ROLE:

```
# Create a Role named "pod-reader" that allows user to perform "get", "watch" and "list" on pods
kubectl create role pod-reader --verb=get --verb=list --verb=watch --resource=pods

# Create a Role named "pod-reader" with ResourceName specified
kubectl create role pod-reader --verb=get --resource=pods --resource-name=readablepod --resource
```

30. ROLEBINDING:

```
# Create a RoleBinding for user1, user2, and group1 using the admin ClusterRole
kubectl create rolebinding admin --clusterrole=admin --user=user1 --user=user2 --group=group1
```

31. CONFIG:

```
# Display the current-context
kubectl config current-context

# List the clusters kubectl knows about
kubectl config get-clusters

# List all the contexts in your kubeconfig file
kubectl config get-contexts

# Describe one context in your kubeconfig file.
kubectl config get-contexts my-context

# Set the user field on the gce context entry without touching other values
kubectl config set-context gce --user=cluster-admin

# Show merged kubeconfig settings.
kubectl config view
```

32. EXPLAIN:

```
# Get the documentation of the resource and its fields
kubectl explain pods

# Get the documentation of a specific field of a resource
kubectl explain pods.spec.containers
```

- kubectl fetch pod name by command

```
kubectl get pod|grep testcore | awk '{print $1}'
```

- Limiting pod communication with network policies in kubernates

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: simple-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: target-app-who-is-applied-the-policy
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 172.17.0.0/16
    - namespaceSelector:
        matchLabels:
          name: namespace-that-can-talk-to-my-app
    - podSelector:
        matchLabels:
          app: pod-that-can-talk-to-my-app
    ports:
    - protocol: TCP
      port: 6379
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    - namespaceSelector:
        matchLabels:
          name: namespace-my-app-can-talk-to
    - podSelector:
        matchLabels:
          app: pod-my-app-can-talk-to
    ports:
    - protocol: TCP
      port: 5978
```

- Allowing specific system pod to talk with your pod

```
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: ksm-can-be-accessed-by-my-app
  namespace: kube-system
spec:
  podSelector:
    matchLabels:
      app: kube-state-metrics
  ingress:
    - from:
      - podSelector:
          matchLabels:
            app: my-app-that-needs-access-to-ksm
      ports:
        - protocol: TCP
          port: 10301
```

- check podIP in kubernates 

```
POD_NAME=test-ui-services-59ffdff65b-4d8zk
PodHost=$(kubectl get pod $POD_NAME --template={{.status.podIP}})
echo $PodHost
```

- list all resources in namespace in k8s

```
kubectl api-resources --verbs=list --namespaced -o name | xargs -n 1 kubectl get --show-kind --ignore-not-found -nl -n <namespace>
```

- NodePort Service

```
apiVersion: v1
kind: Service
metadata:
  name: testcore 
  labels:
    app: testcore
spec:
  type: NodePort
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8163
  selector:
    app: testcore
```

- Kubernates dashboard rolebinding

```
kubectl create clusterrolebinding kubernetes-dashboard --clusterrole=cluster-admin --serviceaccount=kube-system:kubernetes-dashboard
```

- how to check and edit deployment

```
kubectl edit deployment.apps <deployment-name>
kubectl edit deployment.apps testreceipt
```

- create azure secret for storage account in aks

```
kubectl create secret generic offers-fileshare --from-literal=azurestorageaccountname=<name of storage account> --from-literal=azurestorageaccountkey=<access key of storage account>
```

- To check azure secret

```
kubectl get secret offers-fileshare -o yaml
```

- timebased series moniter

```
kubectl <command> --watch
```

- get the statefulset application

```
kubectl get statefulset
```

- pod ip with node details

```
kubectl get pod -o wide
```

- inside statefulset container
  
  ```
  kubectl exec -it <{pod_name}-{index}> -- sh
  ```

- get the replicaset

```
kubectl get replicaset
```

- insdie kubernates container

```
kubectl exec --stdin --tty <pod-id> -- /bin/bash
```

- Opening a shell when a Pod has more than one container

```
kubectl exec -i -t <my-pod-id> --container testtender-697cd9f677-snk6s -- /bin/bash
```

- get inside the pods

```
kubectl exec -it testtender-697cd9f677-v8rm7 bin/bash
```

- pod variables 

```
kubectl exec <enter-pod-name> -- env | grep OMNICORE
```

- multicontainer deployment in same pod logs of specific conatiner

```
kubectl logs <pod_id>/ <container_id> -c <container_name>
```

- open file inside kubernates conatiner

```
tail -f <filenme>
```

- to delete policy in cluter

```
kubectl delete hpa <name of the autoscaling pode>
kubectl delete hpa testcore
```

- hpa enabled in aks

```
kubectl autoscale deployment deployment-name --cpu-percent=average-percent --min=minimum-pod --max=maximum-pod
kubectl autoscale deployment testsale --cpu-percent=80 --min=1 --max=3
```

- create or scale deployment or increase pod by command

```
kubectl scale --replicas=<no_of_replica> deployment <deployment-name>
kubectl scale --replicas=2 deployment testtxn
kubectl scale --replicas=6 -f testtxn.yaml
kubectl scale --replicas=3 replicaset testtxn-77f46b49fd
```

- create from multiple files           

```
kubectl apply -f ./my1.yaml -f ./my2.yaml 
```

- create resource(s) in all manifest files in dir     

```
kubectl apply -f ./dir             
```

- create resource(s) from url      

```
kubectl apply -f http://git.io/vPieo  
```

- start a single instance of nginx        

```
kubectl create deployment nginx --image=nginx  
```

- create a Job which prints "Hello World"

```
kubectl create job hello --image=busybox -- echo "Hello World" 
```

- create a CronJob that prints "Hello World" every minute

```
kubectl create cronjob hello --image=busybox   --schedule="*/1 * * * *" -- echo "Hello World"    
```

- get the documentation for pod manifests

```
kubectl explain pods       
```

- Get commands with basic output

```
kubectl get pods --all-namespaces             # List all pods in all namespaces
kubectl get pods -o wide  # List all pods in the current namespace, with more details like nodepools
kubectl get deployment my-dep                 # List a particular deployment
kubectl get pod my-pod -o yaml                # Get a pod's YAML
```

- Describe commands with verbose output

```
kubectl describe nodes my-node
kubectl describe pods my-pod
```

- List Services Sorted by Name

```
kubectl get services --sort-by=.metadata.name
```

- enable service or expose deployment in internet 

```
kubectl expose deployment deployment-name --type=LoadBalancer --name=service-name
kubectl expose deployment testcore --type=LoadBalancer --name=testcore --port=80 --target-port=8000
```

- Create a service for a replicated nginx, which serves on port 80 and connects to the containers on port 8000.

```
kubectl expose rc nginx --port=80 --target-port=8000
```

- Create a service for a pod valid-pod, which serves on port 444 with the name "frontend"

```
kubectl expose pod valid-pod --port=444 --name=frontend
```

- Create a second service based on the above service, exposing the container port 8443 as port 443 with the name "nginx-http"

```
kubectl expose service nginx --port=443 --target-port=8443 --name=nginx-http
```

- Create a service for a replicated streaming application on port 4100 balancing UDP traffic and named 'video-stream'.

```
kubectl expose rc streamer --port=4100 --protocol=udp --name=video-stream
```

- Create a service for a replicated nginx using replica set, which serves on port 80 and connects to the containers on port 8000.

```
kubectl expose rs nginx --port=80 --target-port=8000
```

- List pods Sorted by Restart Count

```
kubectl get pods --sort-by='.status.containerStatuses[0].restartCount'
```

- create or run yaml file 

```
kubectl create -f deployment.yaml
```

- List PersistentVolumes sorted by capacity

```
kubectl get pv --sort-by=.spec.capacity.storage
```

- List Services with labels

```
kubectl get service -l app.kubernetes.io/name=ingress-nginx --namespace ingress-basic
```

- to get information about aks node and other information

```
kubectl get nodes -o wide
```

- all aks information and credentials store in .kubeconfig file in storage account

- update endpoint IP from different Endpoint in jenkins pipeline

```
#!/bin/bash
# Get the IPs from the source endpoint
SOURCE_IPS=$(kubectl get endpoints $SOURCE_ENDPOINT -n default -o jsonpath='{.subsets[*].addresses[*].ip}')

# Check if we got any IPs
if [ -z "$SOURCE_IPS" ]; then
    echo "No IPs found in the source endpoint $SOURCE_ENDPOINT"
    exit 1
fi

# Convert the space-separated IPs into a JSON array
IP_JSON="["
for ip in $SOURCE_IPS; do
    IP_JSON+="{\\"ip\\":\\"$ip\\"},"
done
IP_JSON="${IP_JSON%,}]"  # Remove the trailing comma and close the array

# Update the target endpoint with the new IPs
kubectl patch endpoints $TARGET_ENDPOINT -n default --type='json' -p="[{\\"op\\": \\"replace\\", \\"path\\": \\"/subsets/0/addresses\\", \\"value\\": $IP_JSON}]"

echo "Updated $TARGET_ENDPOINT with IPs from $SOURCE_ENDPOINT"
```

- Get the node IP where the pod is runningin jenkins pipeline

```
env.NODE_IP = sh(
    script: """
                        POD_NAME=\$(kubectl get pods --no-headers -n kubetail | grep 'kubetail' | awk '{print \$1}')
                        NODE_NAME=\$(kubectl get pod \${POD_NAME} -n kubetail -o jsonpath='{.spec.nodeName}')
    echo \${NODE_NAME} | awk -F'[.-]' '{print \$2 "." \$3 "." \$4 "." \$5}'
    """,
    returnStdout: true
).trim()
echo "Node IP: ${env.NODE_IP}"
```

- get the all avialbale deployed images tag

```
kubectl get pods -n <namespace> -o jsonpath="{.items[*].spec.containers[*].image}" | tr -s '[[:space:]]' '\n' | grep "string|pattern" | cut -d / -f 4 | sort | uniq

kubectl get pods -n production -o jsonpath="{.items[*].spec.containers[*].image}" | tr -s '[[:space:]]' '\n' | grep "production" | cut -d / -f 4 | sort | uniq
```

- logs pod check

```
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # For logs from the previous container instance
```

- sort by restart pod count > 1

```
kubectl get pods -A --field-selector=status.phase!=Succeeded --sort-by='.status.containerStatuses[0].restartCount' | awk '$5 > 1'|grep -E 'prod-app|prod-web|istio-system'
```

- get pod list by creation time 

```
kubectl get pods -A --sort-by='.metadata.creationTimestamp'|grep prod
```

- list api version and details by kubectl command

```
kubectl api-resources –verbs=list –namespaced -o name
```

- command to check specific coloumn output

```
kubectl get hpa -A | awk '{ $1=""; $3=""; $7=""; print $0}'|column -t
```

- To scale down all deployments in a specific namespace, you can use the following kubectl command

```
kubectl scale deployment -n <namespace> --replicas 0 --all
```

- To delete job specific namespace

```
kubectl delete jobs --field-selector status.successful=1 -n perf-app
```

- list all system default pod in control plane related for AKS running in cluster

```
kubectl get pod --all-namespaces
```

- namespace "kube-system" used for control plane namespace by default

- how to access all namespaces in AKS cluster running

```
kubectl get namespaces/ns
```

- list all object created by AKS by default like service,replicaset etc.

```
kubectl get all --all-namespaces
```

- to check the information about of cluster VM node pool

- search in azure portal "virtual machine scale set" option-->click on agent pool-->public_ip_address section in overview

- to deploy all application by single directory. put all yaml inside directory "folder-name i.e kube-manifests" and apply command

```
kubectl apply -f kube-manifests/
```

- delete all deployment

```
kubectl delete -f kube-manifests/
```

- Kubernetes abbreviations commanly used in `kubectl` commands, along with brief explanations:
  
  | Abbreviation           | Resource Type         | Explanation                                                                                   |
  | ---------------------- | --------------------- | --------------------------------------------------------------------------------------------- |
  | **po**                 | Pod                   | Represents a pod, the smallest deployable unit in Kubernetes.                                 |
  | **svc**                | Service               | Defines a logical set of pods and a policy to access them.                                    |
  | **rs**                 | ReplicaSet            | Ensures a specified number of pod replicas are running.                                       |
  | **deploy**             | Deployment            | Manages the deployment of a set of identical pods.                                            |
  | **ds**                 | DaemonSet             | Ensures that all (or some) nodes run a copy of a pod.                                         |
  | **sts**                | StatefulSet           | Manages the deployment of stateful applications.                                              |
  | **job**                | Job                   | Creates one or more pods and ensures that a specified number of them successfully terminate.  |
  | **cronjob**            | CronJob               | Manages time-based jobs, running pods on a schedule.                                          |
  | **cm**                 | ConfigMap             | Provides a way to inject configuration data into pods.                                        |
  | **secret**             | Secret                | Stores sensitive information, such as passwords or tokens.                                    |
  | **pvc**                | PersistentVolumeClaim | Requests storage resources for pods.                                                          |
  | **pv**                 | PersistentVolume      | Represents a piece of storage in the cluster.                                                 |
  | **ns**                 | Namespace             | A way to divide cluster resources between multiple users.                                     |
  | **rc**                 | ReplicationController | Ensures a specified number of pod replicas are running (deprecated in favor of ReplicaSets).  |
  | **clusterrole**        | ClusterRole           | Defines permissions across the entire cluster.                                                |
  | **role**               | Role                  | Defines permissions within a specific namespace.                                              |
  | **rolebinding**        | RoleBinding           | Grants the permissions defined in a role to a user or set of users within a namespace.        |
  | **clusterrolebinding** | ClusterRoleBinding    | Grants the permissions defined in a ClusterRole to a user or set of users across the cluster. |
  | **event**              | Event                 | Represents events generated by the Kubernetes system.                                         |
  | **cs**                 | ComponentStatus       | Represents the status of a Kubernetes component.                                              |

- make alias in bash for kubectl

```
alias <alias name>=kubectl
alias k=kubectl
```

- run command from outside for individual pod  

```
kubectl exec -it <pod_name> -- env
kubectl exec -it <pod_name> -- ls
kubectl exec -it <pod_name> -- cat /opt/test-home/logs
```

- apply latest changes to replica set without delete existing one

```
kubectl replace -f <replica-set_name>.yaml
```

- top pod command with watch option

```
watch -n<interval in sec>  kubectl top pod <pod name>
watch -n2 kubectl top pod testsale-7c85b78867-pdnlj
```

- edit deployment.yaml file in running deployment

```
kubectl edit deployment/<deployment-name> --record=true
kubectl edit deployment/testcore --record=true
```

- verify roll out status of deployment

```
kubectl rollout status deployment/testcore
```

- verify rollout history

```
kubectl rollout history deployment/testcore
```

- check rollout history with revision specific information

```
kubectl rollout history deployment/testcore --revision=1(revision no.)
```

- rollback to deployment

```
kubectl rollout undo deployment/testcore
NOTE : when you rollback the deployment the rollback previous version become current version
```

- rollback to deployment to specific revision version 

```
kubectl rollout undo deployment/testcore --to-revision=3(revision no.)
```

- pause the deployment for update it

```
kubectl rollout pause deployment/testcore
```

- resume the deplo after updating it

```
kubectl rollout resume deployment/testcore
```

- list all available storage classes

```
kubectl get sc(storage classes)
```

- to check the api version 
  http://v1-18.docs.kubernetes.io/docs/reference/generated/kubernetes-api/v<1.18-(kubernatesVersion)>

- command to connect to the database in persistant volume claim container running in k8s for Database like postgres,mysql etc

```
kubectl run -it --rm --image=mysql:5.6(docker hub image name:version used in PVC) --restart=never mysql-client -- mysql -h mysql -p******
```

- connect to Mysql server service from kubernates by external service
1. create external-service.yaml

```
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  type: ExternalName
  externalName: akswebappdb.mysql.database.azure.com(host name)
```

- command to connect mysql server by kubectl

```
kubectl run -it --rm --image=mysql:5.6(docker hub image name:version used in PVC) --restart=never mysql-client -- mysql -h mysql.host.name -u ***** -p*******
```

- how to convert string to base64 hash value in bash

```
echo -n 'string' | base64
```

- how to convert base 64 encoded string to normal string

```
echo -n 'string' | base64 --decode
```

- create kubernates-secret.yaml

```
apiVersion: v1
kind: Secret
metadata:
    name: name_of_secret
type: Opaque
data:
    key: value
```

- define secret value in deployment

```
env:
  - name: MYSQL_ROOT_PASSWORD
    valueFrom: 
    secretKeyRef:
      name: mysql-db-password(name of the secret file deployment)
      key: db-password(key from secret file)
```

- list secrets in kubernates

```
kubectl get secrets
```

- "resource Quota" used to defined how much resources used by Particular Namespace

- Create Image Pull Secret

```
# Template
kubectl create secret docker-registry <secret-name> \
    --namespace <namespace> \
    --docker-server=<container-registry-name>.azurecr.io \
    --docker-username=<service-principal-ID> \
    --docker-password=<service-principal-password>

# Replace
kubectl create secret docker-registry acrdemo2ss-secret \
    --namespace default \
    --docker-server=acrdemo2ss.azurecr.io \
    --docker-username=******** \
    --docker-password=********    

#yaml file
    spec:
      containers:
        - name: acrdemo-localdocker
          image: acrdemo2ss.azurecr.io/app2/acr-app2:v1
          imagePullPolicy: Always
          ports:
            - containerPort: 80
      imagePullSecrets:
        - name: acrdemo2ss-secret           
```

- Managing Linux Node Pools in AKS

- Create New Linux Node Pool 

```bash
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
                    --zones {1,2,3} \
                    --tags nodepool-type=user environment=production nodepoolos=linux app=java-app
```

- List Node Pools

```bash
az aks nodepool list --cluster-name ${AKS_CLUSTER} --resource-group ${AKS_RESOURCE_GROUP} -o table
```

- List Nodes Using Labels

- **Where `nodepoolos=linux`:**
  
  ```bash
  kubectl get nodes -o wide -l nodepoolos=linux
  ```

- **Where `app=java-apps`:**
  
  ```bash
  kubectl get nodes -o wide -l app=java-apps
  ```

- Schedule Pods Based on NodeSelectors

In your pod YAML configuration, specify the `nodeSelector` under the `template` → `spec` section:

```yaml
nodeSelector:
  app: java-apps
```

- command to attach label to node for manual selection

```
kubectl label nodes <node-name> <label-key>=<label-value>
kubectl label nodes kubernetes-foo-node-1.c.a-robinson.internal disktype=ssd
```

- get kubeconfig file for access clusters AKS

```
kubectl config view
```

- to check which cluster you current connected

```
kubectl config current-context
```

- to switch to another cluster

```
kubectl config use-context cluster_name
```

- To delete a user you can run 

```
kubectl config delete-user clusterUser_ResourceGroupName_ClusterName
```

- To remove a cluster, you can run 

```
kubectl config delete-cluster ClusterName
```

- To remove a context, you can run 

```
kubectl config delete-context ClusterName
```

- To check the user in kubeconfig file

```
kubectl config get-users 
```

- To check the context in kubeconfig file

```
kubectl config get-contexts
```

- To check the cluster in kubeconfig file

```
kubectl config get-clusters
```

- to get the current cluster information

```
kubectl cluster-info
```

- describe hpa in deployment

```
kubectl describe hpa/hpaDeploymentName
```

- List which pods are running in system nodepool from kube-system namespace

```
kubectl get pod -o=custom-columns=NODE-NAME:.spec.nodeName,POD-NAME:.metadata.name -n kube-system
```

- command to check ingress route file in k8s

```
kubectl get ingress
```

- command to check routing model in ingress

```
kubectl describe ingress <ingress-route-name>
```

#switch and active namespace

```
kubens <namespace>
kubens production
```

- generate output yaml from deployment

```
kubectl get deploy/svc/hpa/configmap/pvc/etc -o yaml > filename.yaml
```

- You can use any of the following methods to choose where Kubernetes schedules specific Pods:

```
------------------
- nodeselector
------------------
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  nodeSelector:
    disktype: ssd    # label of specific node

------------------
- nodeName
------------------
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  nodeName: foo-node # schedule pod to specific node
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent

-----------------
- Node affinity  
-----------------
- functions like the nodeSelector field but is more expressive and allows you to specify soft rules
- If there are two possible nodes that match the requiredDuringSchedulingIgnoredDuringExecution rule, one with the label-1:key-1 label and another with the label-2:key-2 label, the scheduler considers the weight of each node and adds the weight to the other scores for that node, and schedules the Pod onto the node with the highest final score.

apiVersion: v1
kind: Pod
metadata:
  name: with-affinity-anti-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/os
            operator: In
            values:
            - linux
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: label-1
            operator: In
            values:
            - key-1
      - weight: 50
        preference:
          matchExpressions:
          - key: label-2
            operator: In
            values:
            - key-2
  containers:
  - name: with-node-affinity
    image: k8s.gcr.io/pause:2.0

---------------
- pod-affinity
---------------
- The following Deployment for the web servers creates replicas with the label app=web-store.
- The Pod affinity rule tells the scheduler to place each replica on a node that has a Pod with the label app=store. 
- The Pod anti-affinity rule tells the scheduler to avoid placing multiple app=web-store servers on a single node.

apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server
spec:
  selector:
    matchLabels:
      app: web-store
  replicas: 3
  template:
    metadata:
      labels:
        app: web-store
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - web-store
            topologyKey: "kubernetes.io/hostname"
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - store
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: web-app
        image: nginx:1.16-alpine

Note: You can use the operator field to specify a logical operator for Kubernetes to use when interpreting the rules. You can use In, NotIn, Exists, DoesNotExist, Gt and Lt.
```

- Taints and Tolerations in Kubernetes

- Overview
  
  - **Taints** are the opposite of node affinity; they allow a node to repel a set of pods.
  - **Tolerations** are applied to pods. They enable the scheduler to schedule pods with matching taints.
  - Taints and tolerations work together to ensure that pods are not scheduled onto inappropriate nodes.

- Tainting a Node

```bash
kubectl taint nodes node1 key1=value1:NoSchedule
```

- This command applies a taint with:
  
  - **Key:** `key1`
  - **Value:** `value1`
  - **Effect:** `NoSchedule`
  
  This means that no pod will be scheduled onto `node1` unless it has a matching toleration.

- Removing a Taint

```bash
kubectl taint nodes node1 key1=value1:NoSchedule-
```

- Specifying a Toleration

```yaml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoSchedule"
```

Alternatively, you can use:

```yaml
tolerations:
- key: "key1"
  operator: "Exists"
  effect: "NoSchedule"
```

- Scenarios

- Scenario 1

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  tolerations:
  - key: "example-key"
    operator: "Exists"
    effect: "NoSchedule"
```

- Both tolerations "match" the taint created by the taint command above. Thus, a pod with either toleration would be able to schedule onto `node1`.

- Scenario 2

```bash
kubectl taint nodes node1 key1=value1:NoSchedule
kubectl taint nodes node1 key1=value1:NoExecute
kubectl taint nodes node1 key2=value2:NoSchedule
```

- And a pod has two tolerations:

```yaml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoSchedule"
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoExecute"
```

- The pod will **not** be able to schedule onto the node because there is no toleration matching the third taint.

- However, it will continue running if it is already running on the node when the taint is added because the third taint is the only one not tolerated by the pod.

- Handling NoExecute Taints

- If a taint with the effect `NoExecute` is added to a node:

- Pods that do not tolerate the taint will be evicted immediately.

- Pods that do tolerate the taint will never be evicted.

- A toleration with `NoExecute` effect can specify an optional `tolerationSeconds` field:

```yaml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoExecute"
  tolerationSeconds: 3600
```

- Built-in Taints
  The node controller automatically taints a node when certain conditions are true. The following are built-in taints:
  
  - `node.kubernetes.io/not-ready`: Node is not ready (corresponds to the NodeCondition Ready being "False").
  - `node.kubernetes.io/unreachable`: Node is unreachable from the node controller (corresponds to the NodeCondition Ready being "Unknown").
  - `node.kubernetes.io/memory-pressure`: Node has memory pressure.
  - `node.kubernetes.io/disk-pressure`: Node has disk pressure.
  - `node.kubernetes.io/pid-pressure`: Node has PID pressure.
  - `node.kubernetes.io/network-unavailable`: Node's network is unavailable.
  - `node.kubernetes.io/unschedulable`: Node is unschedulable.
  - `node.cloudprovider.kubernetes.io/uninitialized`: Marks a node as unusable when the kubelet is started with an "external" cloud provider.
    In the event of a node eviction, the node controller or the kubelet adds relevant taints with `NoExecute` effect. If the fault condition returns to normal, the kubelet or node controller can remove the relevant taint(s).

- DaemonSet 
  These pods are created with NoExecute tolerations for the following taints with no tolerationSeconds:

```
node.kubernetes.io/unreachable
node.kubernetes.io/not-ready
```

- This ensures that DaemonSet pods are never evicted due to these problems.

- A DaemonSet ensures that all (or some) Nodes run a copy of a Pod. 

- As nodes are added to the cluster, Pods are added to them. 

- As nodes are removed from the cluster, those Pods are garbage collected. Deleting a DaemonSet will clean up the Pods it created.

- Some typical uses of a DaemonSet are:
  
  - running a cluster storage daemon on every node
  
  - running a logs collection daemon on every node
  
  - running a node monitoring daemon on every node

```
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-elasticsearch
  namespace: kube-system
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd-elasticsearch
  template:
    metadata:
      labels:
        name: fluentd-elasticsearch
    spec:
      tolerations:
      # these tolerations are to have the daemonset runnable on control plane nodes
      # remove them if your control plane nodes should not run pods
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
      containers:
      - name: fluentd-elasticsearch
        image: quay.io/fluentd_elasticsearch/fluentd:v2.5.2
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

- delete daemonset without deleting pod

```
kubectl delete daemonset daemonsetname --cascade=orphan 
```

- If you subsequently create a new DaemonSet with the same selector, the new DaemonSet adopts the existing Pods.

- to get the Azure key vault class

```
kubectl get secretproviderclass
```

- Install and use stern for logs checking in all pods at same time

```
curl -kvvv -u <users>:<Password> https://artifactory.testb.com:443/artifactory/testdev-docker-local/stern_1.30.0_linux_amd64.tar.gz -o stern_1.30.0_linux_amd64.tar.gz
tar -xzvf stern_1.30.0_linux_amd64.tar.gz
sudo mv stern /usr/local/bin/
sudo chmod +x /usr/local/bin/stern
stern --version
stern test-service -n qa-app
```

- Create `kubectl` command `alias` in linux for quick access for k8s commands
  
  # General Aliases for kubectl

| Alias   | Command                                  | Description                        |
| ------- | ---------------------------------------- | ---------------------------------- |
| `k`     | `kubectl`                                | Main command for Kubernetes        |
| `kc`    | `kubectl config`                         | Manage kubeconfig settings         |
| `kcv`   | `kubectl config view`                    | View kubeconfig settings           |
| `kcgc`  | `kubectl config get-contexts`            | Get all contexts in kubeconfig     |
| `kccc`  | `kubectl config current-context`         | Get the current context            |
| `kcuc`  | `kubectl config use-context`             | Switch to a different context      |
| `kcsc`  | `kubectl config set-context --current`   | Set the current context            |
| `kdesc` | `kubectl describe`                       | Describe resources                 |
| `kcf`   | `kubectl create -f`                      | Create resources from a file       |
| `kaf`   | `kubectl apply -f`                       | Apply changes from a file          |
| `kgn`   | `kubectl get nodes`                      | List nodes                         |
| `kgp`   | `kubectl get pods`                       | List pods                          |
| `kgpa`  | `kubectl get pods --all-namespaces`      | List pods in all namespaces        |
| `kgns`  | `kubectl get namespaces`                 | List namespaces                    |
| `kgs`   | `kubectl get services`                   | List services                      |
| `kgd`   | `kubectl get deployments`                | List deployments                   |
| `kgi`   | `kubectl get ingress`                    | List ingress resources             |
| `kgcm`  | `kubectl get configmap`                  | List config maps                   |
| `kgsec` | `kubectl get secrets`                    | List secrets                       |
| `kgpv`  | `kubectl get pv`                         | List persistent volumes            |
| `kgpvc` | `kubectl get pvc`                        | List persistent volume claims      |
| `kgsa`  | `kubectl get serviceaccounts`            | List service accounts              |
| `kgsts` | `kubectl get statefulsets`               | List stateful sets                 |
| `kgds`  | `kubectl get daemonsets`                 | List daemon sets                   |
| `kgic`  | `kubectl get ingressclasses`             | List ingress classes               |
| `kgnp`  | `kubectl get networkpolicies`            | List network policies              |
| `kgcrb` | `kubectl get clusterrolebindings`        | List cluster role bindings         |
| `kgcr`  | `kubectl get clusterroles`               | List cluster roles                 |
| `kgrb`  | `kubectl get rolebindings`               | List role bindings                 |
| `kgr`   | `kubectl get roles`                      | List roles                         |
| `kgsc`  | `kubectl get storageclasses`             | List storage classes               |
| `kghpa` | `kubectl get horizontalpodautoscalers`   | List horizontal pod autoscalers    |
| `kgbc`  | `kubectl get backendconfigs`             | List backend configurations        |
| `kgfc`  | `kubectl get frontendconfigs`            | List frontend configurations       |
| `kgcj`  | `kubectl get cronjobs`                   | List cron jobs                     |
| `kgj`   | `kubectl get jobs`                       | List jobs                          |
| `kdp`   | `kubectl delete pod`                     | Delete a pod                       |
| `kds`   | `kubectl delete service`                 | Delete a service                   |
| `kdd`   | `kubectl delete deployment`              | Delete a deployment                |
| `kdns`  | `kubectl delete namespace`               | Delete a namespace                 |
| `kdn`   | `kubectl delete node`                    | Delete a node                      |
| `kdi`   | `kubectl delete ingress`                 | Delete an ingress resource         |
| `kdcm`  | `kubectl delete configmap`               | Delete a config map                |
| `kdsec` | `kubectl delete secret`                  | Delete a secret                    |
| `kdpv`  | `kubectl delete pv`                      | Delete a persistent volume         |
| `kdpvc` | `kubectl delete pvc`                     | Delete a persistent volume claim   |
| `kdsa`  | `kubectl delete serviceaccount`          | Delete a service account           |
| `kdsts` | `kubectl delete statefulset`             | Delete a stateful set              |
| `kdds`  | `kubectl delete daemonset`               | Delete a daemon set                |
| `kdic`  | `kubectl delete ingressclasses`          | Delete ingress classes             |
| `kdnp`  | `kubectl delete networkpolicies`         | Delete network policies            |
| `kdcrb` | `kubectl delete clusterrolebinding`      | Delete a cluster role binding      |
| `kdcr`  | `kubectl delete clusterrole`             | Delete a cluster role              |
| `kdrb`  | `kubectl delete rolebinding`             | Delete a role binding              |
| `kdr`   | `kubectl delete role`                    | Delete a role                      |
| `kdsc`  | `kubectl delete storageclasses`          | Delete storage classes             |
| `kdhpa` | `kubectl delete horizontalpodautoscaler` | Delete a horizontal pod autoscaler |
| `kdbc`  | `kubectl delete backendconfig`           | Delete a backend configuration     |
| `kdfc`  | `kubectl delete frontendconfig`          | Delete a frontend configuration    |
| `kdcj`  | `kubectl delete cronjobs`                | Delete cron jobs                   |
| `kdj`   | `kubectl delete jobs`                    | Delete jobs                        |

- `Static Pods` can be used to run containers on a Node in the absence of a Kubernetes API Server.

### References

1. [Kubernetes Components Overview](https://kubernetes.io/docs/concepts/overview/components/)
2. [Kubernetes Architecture by Red Hat](https://www.redhat.com/en/topics/containers/kubernetes-architecture)
3. [Kubernetes Architecture by Aqua Security](https://www.aquasec.com/cloud-native-academy/kubernetes-101/kubernetes-architecture/)
4. [Kubernetes Architecture Concepts by Platform9](https://platform9.com/blog/kubernetes-enterprise-chapter-2-kubernetes-architecture-concepts/)
5. [Assign CPU Resources to Containers](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/)
6. [Managing Kubernetes Objects with Kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
7. [Manage Kubernetes Configurations with Kustomize by DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-manage-your-kubernetes-configurations-with-kustomize)
8. [Introduction to Helm, the Package Manager for Kubernetes by DigitalOcean](https://www.digitalocean.com/community/tutorials/an-introduction-to-helm-the-package-manager-for-kubernetes)
9. [Debugging Applications in a Kubernetes Cluster](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-cluster/)
10. [Network Policies Guide by Giant Swarm](https://docs.giantswarm.io/getting-started/network-policies/)

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚