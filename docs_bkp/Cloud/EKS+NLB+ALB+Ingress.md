# AWS EKS + Network Load Balancer + Application Load Balancer + Ingress Route

# <mark>Pre-Requisite</mark>

1. EKS k8s cluster should be created and have access for deployment for application and load balancer.

2. Must have AWS Admin Access for IAM Role to Create IAM Policy and linked IAM Account with Policy.

3. Install Kubectl, Eksctl and Helm Cli tools in remote server or local machine.

4. Write all k8s application manifest Yaml and ingress route file for deployment.

# <mark>Using AWS Services For UAT Env.</mark>

- EKS CLuster Name  : ClusterName

VPC ID : vpc-02069091fada4620a

Subnet ID : subnet-07ba3a32267329ee6, subnet-02e7ae24f25be0e77, subnet-0f0c0e25e1070b0ee

Region : ap-south-1

EC2 Remote Server name : LocalMachineVmServerName

### <mark>Install kubectl binary with curl on Linux[]</mark>

### (https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-kubectl-binary-with-curl-on-linux)

1. Download the latest release with the command
   
   ```
     curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   ```

2. Install kubectl
   
   ```bash
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```
   
   **Note:**
   
   If you do not have root access on the target system, you can still install kubectl to the `~/.local/bin` directory:
   
   ```bash
   chmod +x kubectl
   mkdir -p ~/.local/bin
   mv ./kubectl ~/.local/bin/kubectl
   # and then append (or prepend) ~/.local/bin to $PATH
   ```

3. Test to ensure the version you installed is up-to-date:
   
   ```bash
   kubectl version --client
   ```

# <mark>Install helm Cli with Curl in Linux</mark>

```console
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
#Curl without ssl check certificate use [ -k or --insecure ] 
chmod 700 get_helm.sh
./get_helm.sh
```

## <mark>Install Eksctl Cli with Curl in Linux</mark>

```
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

sudo mv /tmp/eksctl /usr/local/bin

eksctl version
```

### Create EKS and Configured it with all suitable user access for accessing k8s api object.

```
eksctl create iamidentitymapping --cluster ClusterName --region=ap-south-1 \
 --arn arn:aws:iam::868909427937:role/AWS-App-Admin_55cdac5ba3f9bd94 --username accesstocluster --group system:masters \
 --no-duplicate-arns
```

### configure OIDC Provider entities in IAM that supports the OpenID Connect (OIDC) standard to CLuster

eksctl utils associate-iam-oidc-provider --region ap-south-1 --cluster ClusterName --approve 

### Download and configure AWS IAM policy for AWS load balancer for communication with k8s cluster. For this we require IAM admin access Role in AWS

#### Download

curl -o iam_policy_latest.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json

```iam_policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateServiceLinkedRole"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:AWSServiceName": "elasticloadbalancing.amazonaws.com"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeAccountAttributes",
                "ec2:DescribeAddresses",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeInternetGateways",
                "ec2:DescribeVpcs",
                "ec2:DescribeVpcPeeringConnections",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeInstances",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeTags",
                "ec2:GetCoipPoolUsage",
                "ec2:DescribeCoipPools",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeLoadBalancerAttributes",
                "elasticloadbalancing:DescribeListeners",
                "elasticloadbalancing:DescribeListenerCertificates",
                "elasticloadbalancing:DescribeSSLPolicies",
                "elasticloadbalancing:DescribeRules",
                "elasticloadbalancing:DescribeTargetGroups",
                "elasticloadbalancing:DescribeTargetGroupAttributes",
                "elasticloadbalancing:DescribeTargetHealth",
                "elasticloadbalancing:DescribeTags"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "cognito-idp:DescribeUserPoolClient",
                "acm:ListCertificates",
                "acm:DescribeCertificate",
                "iam:ListServerCertificates",
                "iam:GetServerCertificate",
                "waf-regional:GetWebACL",
                "waf-regional:GetWebACLForResource",
                "waf-regional:AssociateWebACL",
                "waf-regional:DisassociateWebACL",
                "wafv2:GetWebACL",
                "wafv2:GetWebACLForResource",
                "wafv2:AssociateWebACL",
                "wafv2:DisassociateWebACL",
                "shield:GetSubscriptionState",
                "shield:DescribeProtection",
                "shield:CreateProtection",
                "shield:DeleteProtection"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupIngress"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateSecurityGroup"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags"
            ],
            "Resource": "arn:aws:ec2:*:*:security-group/*",
            "Condition": {
                "StringEquals": {
                    "ec2:CreateAction": "CreateSecurityGroup"
                },
                "Null": {
                    "aws:RequestTag/elbv2.k8s.aws/cluster": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:DeleteTags"
            ],
            "Resource": "arn:aws:ec2:*:*:security-group/*",
            "Condition": {
                "Null": {
                    "aws:RequestTag/elbv2.k8s.aws/cluster": "true",
                    "aws:ResourceTag/elbv2.k8s.aws/cluster": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupIngress",
                "ec2:DeleteSecurityGroup"
            ],
            "Resource": "*",
            "Condition": {
                "Null": {
                    "aws:ResourceTag/elbv2.k8s.aws/cluster": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:CreateLoadBalancer",
                "elasticloadbalancing:CreateTargetGroup"
            ],
            "Resource": "*",
            "Condition": {
                "Null": {
                    "aws:RequestTag/elbv2.k8s.aws/cluster": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:CreateListener",
                "elasticloadbalancing:DeleteListener",
                "elasticloadbalancing:CreateRule",
                "elasticloadbalancing:DeleteRule"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:AddTags",
                "elasticloadbalancing:RemoveTags"
            ],
            "Resource": [
                "arn:aws:elasticloadbalancing:*:*:targetgroup/*/*",
                "arn:aws:elasticloadbalancing:*:*:loadbalancer/net/*/*",
                "arn:aws:elasticloadbalancing:*:*:loadbalancer/app/*/*"
            ],
            "Condition": {
                "Null": {
                    "aws:RequestTag/elbv2.k8s.aws/cluster": "true",
                    "aws:ResourceTag/elbv2.k8s.aws/cluster": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:AddTags",
                "elasticloadbalancing:RemoveTags"
            ],
            "Resource": [
                "arn:aws:elasticloadbalancing:*:*:listener/net/*/*/*",
                "arn:aws:elasticloadbalancing:*:*:listener/app/*/*/*",
                "arn:aws:elasticloadbalancing:*:*:listener-rule/net/*/*/*",
                "arn:aws:elasticloadbalancing:*:*:listener-rule/app/*/*/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:ModifyLoadBalancerAttributes",
                "elasticloadbalancing:SetIpAddressType",
                "elasticloadbalancing:SetSecurityGroups",
                "elasticloadbalancing:SetSubnets",
                "elasticloadbalancing:DeleteLoadBalancer",
                "elasticloadbalancing:ModifyTargetGroup",
                "elasticloadbalancing:ModifyTargetGroupAttributes",
                "elasticloadbalancing:DeleteTargetGroup"
            ],
            "Resource": "*",
            "Condition": {
                "Null": {
                    "aws:ResourceTag/elbv2.k8s.aws/cluster": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:AddTags"
            ],
            "Resource": [
                "arn:aws:elasticloadbalancing:*:*:targetgroup/*/*",
                "arn:aws:elasticloadbalancing:*:*:loadbalancer/net/*/*",
                "arn:aws:elasticloadbalancing:*:*:loadbalancer/app/*/*"
            ],
            "Condition": {
                "StringEquals": {
                    "elasticloadbalancing:CreateAction": [
                        "CreateTargetGroup",
                        "CreateLoadBalancer"
                    ]
                },
                "Null": {
                    "aws:RequestTag/elbv2.k8s.aws/cluster": "false"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:RegisterTargets",
                "elasticloadbalancing:DeregisterTargets"
            ],
            "Resource": "arn:aws:elasticloadbalancing:*:*:targetgroup/*/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:SetWebAcl",
                "elasticloadbalancing:ModifyListener",
                "elasticloadbalancing:AddListenerCertificates",
                "elasticloadbalancing:RemoveListenerCertificates",
                "elasticloadbalancing:ModifyRule"
            ],
            "Resource": "*"
        }
    ]
}
```

### Make AWS Policy from download json file

aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy_latest.json

### Make a note of Policy ARN as we are going to use that in next step when creating IAM Role.

Policy ARN:  arn:aws:iam::180789647333:policy/AWSLoadBalancerControllerIAMPolicy

### Verify if any existing service account

```
kubectl get sa -n kube-system
kubectl get sa aws-load-balancer-controller -n kube-system
```

Obseravation:

- Nothing with name "aws-load-balancer-controller" should exist

### K8S Service Account Name that need to be bound to newly created IAM Role

```
eksctl create iamserviceaccount --cluster=ClusterName --region ap-south-1 --namespace=kube-system --name=aws-load-balancer-controller --attach-policy-arn=arn:aws:iam::868909427937:policy/AWSLoadBalancerControllerIAMPolicy --override-existing-serviceaccounts --approve
```

### Get IAM Service Account Connect to Cluster

```
eksctl get iamserviceaccount --cluster ClusterName
```

## Verify again service account in k8s

```
kubectl get sa -n kube-system
kubectl get sa aws-load-balancer-controller -n kube-system
```

Obseravation:

- Now with name "aws-load-balancer-controller" created and should be exists.

### Describe Service Account aws-load-balancer-controller

```
kubectl describe sa aws-load-balancer-controller -n kube-system
```

![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-04-16-59-33-image.png)

## Configure Aws-Load-Balancer-Controller for eks with the help of helm

### Add the eks-charts repository.

```
helm repo add eks https://aws.github.io/eks-charts 
```

### Update your local repo to make sure that you have the most recent charts.

```
helm repo update
```

### Get Region Code and Account info for aws docker registry for AWS LB Controller Image

ap-south-1        602401143452.dkr.ecr.ap-south-1.amazonaws.com

![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-04-17-02-13-image.png)

### Replace Cluster Name, Region Code, VPC ID, Image Repo Account ID for install AWS LB controller in eks

```
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=ClusterName \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=ap-south-1 \
  --set vpcId=vpc-02069091fada4620a \
  --set image.repository=602401143452.dkr.ecr.ap-south-1.amazonaws.com/amazon/aws-load-balancer-controller
```

### Verify that the controller is installed

```
kubectl -n kube-system get deployment
```

![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-04-17-06-37-image.png)

```
kubectl -n kube-system get deployment aws-load-balancer-controller
```

![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-04-17-07-24-image.png)

```
kubectl -n kube-system describe deployment aws-load-balancer-controller
```

![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-04-17-09-47-image.png)

![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-04-17-10-21-image.png)

### Verify AWS Load Balancer Controller Webhook service created

```
kubectl -n kube-system get svc 
kubectl -n kube-system get svc aws-load-balancer-webhook-service
```

![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-04-17-11-40-image.png)

```
kubectl -n kube-system describe svc aws-load-balancer-webhook-service
```

![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-04-17-12-25-image.png)

### Verify Labels in Service and Selector Labels in Deployment

```
kubectl -n kube-system get svc aws-load-balancer-webhook-service -o yaml
kubectl -n kube-system get deployment aws-load-balancer-controller -o yaml
```

![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-04-17-14-53-image.png)

Observation:

1. Verify "spec.selector" label in "aws-load-balancer-webhook-service"
2. Compare it with "aws-load-balancer-controller" Deployment "spec.selector.matchLabels"
3. Both values should be same which traffic coming to "aws-load-balancer-webhook-service" on port 443 will be sent to port 9443 on "aws-load-balancer-controller" deployment related pods.

### List Pods for verification purpose

```
kubectl get pods -n kube-system
```

![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-04-17-16-21-image.png)

### Review logs for AWS LB Controller POD-1 , POD-2

```
kubectl -n kube-system logs -f  aws-load-balancer-controller-86b598cbd6-5pjfk
kubectl -n kube-system logs -f aws-load-balancer-controller-86b598cbd6-vqqsk
```

### Now create AWS K8s ingress file with Specific annotation mentioned below for routing and traffic distribution with respect to Microservice

```aws-alb-uat.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: alb-ingress-uat-internet
  namespace: test-poc
  #annotation URl info
  #https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.3/guide/ingress/annotations/#annotations
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/load-balancer-name: alb-ingress-uat
    alb.ingress.kubernetes.io/certificate-arn: "arn:aws:acm:ap-south-1:868909427937:certificate/343397f8-e3b8-447a-bf13-231f486e980f"
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS": 443}, {"HTTP": 80}]'
    alb.ingress.kubernetes.io/subnets: subnet-07ba3a32267329ee6,subnet-02e7ae24f25be0e77,subnet-0f0c0e25e1070b0ee
    alb.ingress.kubernetes.io/actions.ssl-redirect: '{"Type": "redirect", "RedirectConfig": { "Protocol": "HTTPS", "Port": "443", "StatusCode": "HTTP_301"}}'
    alb.ingress.kubernetes.io/scheme: internet-facing
    #Register Pods as Target for the ALB
    alb.ingress.kubernetes.io/target-type: ip 
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ssl-redirect
                port:
                  name: use-annotation
          # Api exposed endpoints
          - path: /test
            pathType: Prefix
            backend:
              service:
                name: ww-test-svc
                port:
                  number: 80
```

### Create Namespace or Use existing namespace for deployment of Application as well as Ingress file in same Name space

```
kubectl create namespace poc-test
```

### Deploy all application manifest and Ingress manifest in above created namespace

```
kubectl apply -f aws-alb-uat.yaml
```

### varify the exposed service with the help of AWS Application Load Balancer URL

http://alb-ingress-uat-1775792459.ap-south-1.elb.amazonaws.com

### Create Network Load Balancer from AWS Portal or AWS CLI

AWS Portal--> EC2--> Load Balancer--> Create Load Balancer--> Compare and select load balancer type--> Select : Network Load Balancer--> Create -->[ Load Balancer Name : aws-nlb-uat| Schema : Internet-facing | IP address type: IPv4 | Select VPC | Select Listener-->TCP:80 [ Protocol: TCP | Port: 80 | Create Target Group For Backend Application Load Balancer--> select Application Load Balancer: alb-ingress--uat ] || TCP:443 [ Protocol: TCP | Port: 443 | Create Target Group For Backend Application Load Balancer--> select Application Load Balancer: alb-ingress-uat ]-->Create Load Balancer.



### varify the exposed service with the help of AWS Network Load Balancer URL

http://nlb-ingress-uat-ed7051b0c64b0b2a.elb.ap-south-1.amazonaws.com

### To Setup SSL varification please enable AWS ALB with SSL by adding certificate ARN in Ingress file with the help of following annotations

```
alb.ingress.kubernetes.io/certificate-arn: "arn:aws:acm:ap-south-1:868909427937:certificate/343397f8-e3b8-447a-bf13-231f486e980f"
alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS": 443}, {"HTTP": 80}]'
```

### Then configure Both Network load Balancer and Application load balancer in Domain Provider portal with "A" name record of Load Balancer DNS name.

### Varify the Https with Domain provided by Domain Provider.

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
