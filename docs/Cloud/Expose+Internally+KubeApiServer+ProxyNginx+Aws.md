# Provide developers with secure access to the Kubernetes API server of a private Amazon EKS cluster for the purpose of troubleshooting and debugging cloud-deployed applications.

![RequestFlowDiagram](https://sawanchouksey.github.io/documents/blob/main/docs/Cloud/Nginx+KubeAPi.png?raw=true)

### Context:

- The EKS cluster is configured with private endpoints, meaning the Kubernetes API server is not directly accessible from the public internet.

- Developers need to access the API server to debug and troubleshoot issues that cannot be resolved through other means.

### Use Case Description:

- **Actors**: Developers, DevOps Engineers

- **Precondition**: Developers have appropriate permissions to access the cluster and perform troubleshooting.

- **Trigger**: Need to diagnose issues within the EKS cluster that require direct interaction with the Kubernetes API server.

### Scenario:

- **Authentication**: Developers authenticate through a secure method to gain temporary access to the Kubernetes API server.

- **Access Method**: Developers access the API server via a secure channel, such as a bastion host or VPN.

- **Debugging**: Developers perform necessary debugging and troubleshooting tasks.

- **Termination**: Access is terminated when the troubleshooting session is complete.

### Pre-Requisite

1. EC2 Computer Instance

2. Elastic Kubernetes Service(eks)

3. AWS Account with admin access (or with minimum required permission IAM,EKS,Route53,LB,EC2 etc.)

4. Nginx Software installed in EC2 Instance

5. Automation Script | Automation Job - Optional

6. Jenkins - Optional

7. VPN access to Nginx Server from System

### Steps to be Peformed for Installation and Setup


1. Create EKS Cluster.

2. Create `kubernetes-exteranl` service with `internal Load Balancer` Annotation to access traffic by `Nginx Server` privately in VPC.

```
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-external
  namespace: default
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-internal: "true"
spec:
  type: LoadBalancer
  ports:
    - name: https
      port: 443
      targetPort: 443

```

```
kubectl apply -f kubernetes-external-svc.yaml

```

3. Create `IAM role` for allow access kubernetes object in EKS.

4. Create `Secret` with kubernetes `ca.cert` and access `token` and `namespace` for authentication.

```
apiVersion: v1
data:
  ca.crt: "BASE_64_ENCODED_VALUE"
  namespace: "BASE_64_ENCODED_VALUE"
  token: "BASE_64_ENCODED_VALUE"
kind: Secret
metadata:
  annotations:
    kubernetes.io/service-account.name: admin-sa
  name: admin-sa-token-2gkrq
  namespace: kube-system
type: kubernetes.io/service-account-token

```

```
kubectl apply -f kubernetes-external-secret.yaml

```

5. Create `Service Account` with `IAM Role` annotations.

```
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::11234567890:role/AwsDevPodRole
  name: admin-sa
  namespace: kube-system
secrets:
- name: admin-sa-token-2gkrq

```

```
kubectl apply -f kubernetes-external-sa.yaml

```

6. Create `RoleBinding` for RBAC Access with `Service Account` token based authentication only.

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-sa-rb
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: admin-sa
    namespace: kube-system

```

```
kubectl apply -f kubernetes-external-rbac.yaml

```

7. Get the `API Server` endpoint IPs by kubectl command and update the IPs in Internally Exposed Service `EndPoints`.

```
kubectl describe svc kubernetes

```

8. Create `EndPoint` for access default `k8s API server` internally from `kubernetes` endpoints IPs.

```
apiVersion: v1
kind: Endpoints
metadata:
  name: kubernetes-external
  namespace: default
subsets:
- addresses:
  # Get the IPs from kubernetes endpoints `kubectl get ep`
  - ip: 10.1.2.3
  - ip: 10.4.5.6
  ports:
  - port: 443
    name: https

```

```
kubectl apply -f kubernetes-external-ep.yaml

```
9. Now Check `endPoints` IPs for both `kubernetes` & `kubernetes-external` must be same

```
kubectl get ep -n default | grep -i 'kubernetes'

```

10. Now get the `Load balancer url` from `kubernetes-external svc` for update configuration in `nginx` server.

```
kubectl get svc -n default | grep -i 'kubernetes-external'

```

11. Create ec2 instnace i.e. ubuntu machine server and install `Nginx Software`.

```
sudo apt update
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx

```

11. update `nginx.conf` file or create `kube-api.conf` file for `Nginx` server. and update with `load balancer url` as proxy pass routing url. 

```
systemctl stop nginx

```

```
server {
    listen  443 ssl http2;

    include /etc/nginx/ssl/ssl.conf;

    server_name  kubi-api.xyz.com;

    location / {
        set $masters_elb 'https://internal-a8eff9a392ac240dd8e80a9djhafjdhfuh-1222210832.ap-south-1.elb.amazonaws.com';
        proxy_pass $masters_elb;
        proxy_http_version 1.1;
        proxy_pass_header Server;
        proxy_pass_header X-Auth;
        proxy_pass_request_headers  on;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
}

```

```
nginx -t
systemctl start nginx
systemctl status nginx

```

12. Create a `A` Name `DNS Record` entry in Hosted Zone in `Route 53` for you DNS i.e. `xyz.com`

```
subdomain name: `kube-api.xyz.com`
DNS Record Type: `A`
IP Address: `Nginx Server private IP i.e. 10.1.7.8`

```

13. Update `.kube/config` in your local system for run `kubectl` commands.

```
apiVersion: v1
clusters:
  - cluster:
      #insecure-skip-tls-verify: true
      server: https://kube-api.xyz.com
    name: arn:aws:eks:ap-south-1:11234567890:cluster/EKSKubeAPITest
contexts:
  - context:
      cluster: arn:aws:eks:ap-south-1:11234567890:cluster/EKSKubeAPITest
      user: admin-sa
    name: arn:aws:eks:ap-south-1:11234567890:cluster/EKSKubeAPITest
current-context: arn:aws:eks:ap-south-1:11234567890:cluster/EKSKubeAPITest
kind: Config
preferences: {}
users:
  - name: admin-sa
    user:
      token: <Authentication_Token_Value_for_admin-sa>

```

14. Now run and test `kubectl` command from your local system

```
kubectl get pod -A

```

15. Create automation script or Jenkins job for update `endpointIP` if it changed due to eks upgrade or migration or unexpected incident happened. There is `Jenkins Job` we used for autamtion in pipeline just for reference.

```
@Library(value = "shared-jenkins-library", changelog = false) _
pipeline{
    agent {
            kubernetes {
                yaml libraryResource("jenkins-deploy-agent.yaml")
            }
    }
    environment {
        KUBECONFIGFILE = credentials('eks-creds')
        SOURCE_ENDPOINT = 'kubernetes'
        TARGET_ENDPOINT = 'kubernetes-external'        
    }

    stages {
        stage('pre-deployment check'){
            steps{
                script{
                      sh "mkdir ~/.kube"
                      sh "cp ${KUBECONFIGFILE} ~/.kube/config;chmod 777 /home/jenkins/.kube/config;grep cluster /home/jenkins/.kube/config" 
                      sh "cat /home/jenkins/.kube/config"
                      sh "kubectl get ep -n default"
                }
            }
        }
        stage('Update Endpoints') {
            steps {
                script {
                    def updateScript = '''#!/bin/bash
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
                    '''

                    // Execute the script
                    sh updateScript
                }
            }
        }
    }
}

```

### Tips - Things to remember

- There must be interconnectivity between `nginx server` and `eks server`.

- There must be proper permission needs to be allow for access `kubernetes object`.

- There must be `domain whitelisting` through `VPN` in your system or cloud vice-versa. 

- There must be one system, worker node required to run `kubectl` ommand before this setup i.e. Linux ec2 instnace in same subnet where eks located.

- Apply and install all `yaml` files in order to prevent conflict with inter dependencies.

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
 