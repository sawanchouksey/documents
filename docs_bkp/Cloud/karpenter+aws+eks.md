# Enable Karpenter with AWS EKS

Set up a cluster and add Karpenter

###### Karpenter automatically provisions new nodes in response to unschedulable pods. Karpenter does this by observing events within the Kubernetes cluster, and then sending commands to the underlying cloud provider.

###### Karpenter provides automatic and highly scalable node provisioning tailored specifically for Kubernetes in a vendor neutral manner.

###### Karpenter is more flexible, cost-focused, and easy to use for autoscaling diverse Kubernetes deployments across multiple cloud providers.

### Advantages of using Karpenter:

- **Automatic node discovery** - Karpenter automatically finds eligible node groups to scale, while Cluster Autoscaler requires configuring node groups.
- **No overprovisioning** - Karpenter scales nodes up and down to match workload demand. Cluster Autoscaler focuses on scaling up and preventing overprovisioning.
- **Cost optimization** - Karpenter aims to optimize cloud costs by minimizing idle resources. Cluster Autoscaler has less of a cost optimization focus.
- **Custom metrics** - Karpenter can scale on custom app-specific metrics beyond just CPU/memory. Cluster Autoscaler focuses on system metrics.
- **Descheduling** - Karpenter can deschedule pods to make room for pending pods. Cluster Autoscaler only scales up nodes.
- **High scalability** - Karpenter is designed to manage thousands of nodes. Cluster Autoscaler can struggle with scale.
- **Ease of use** - Karpenter aims for simpler setup and configuration vs Cluster Autoscaler's more complex yaml-based configuration.

### Pre-requisite

Karpenter requires cloud provider permissions to provision nodes, for AWS IAM Roles for Service Accounts (IRSA) should be used. IRSA permits Karpenter (within the cluster) to make privileged requests to AWS (as the cloud provider) via a ServiceAccount.

1. AWS Cli

2. Kubectl Cli

3. eksctl

4. helm

[Configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) with a user that has sufficient privileges to create an EKS cluster. Verify that the CLI can authenticate properly by running `aws sts get-caller-identity`

### Set environment variables to use whole implementation

```
export KARPENTER_NAMESPACE=kube-system
export KARPENTER_VERSION=v0.34.1
export K8S_VERSION=1.29
```

```
export AWS_PARTITION="aws" # if you are not using standard partitions, you may need to configure to aws-cn / aws-us-gov
export CLUSTER_NAME="${USER}-karpenter-demo"
export AWS_DEFAULT_REGION="ap-south-1"
export AWS_ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
export TEMPOUT=$(mktemp)
```

### Check the all environment variable properly set

```
echo $KARPENTER_NAMESPACE $KARPENTER_VERSION $K8S_VERSION $CLUSTER_NAME $AWS_DEFAULT_REGION $AWS_ACCOUNT_ID $TEMPOUT
```

### Create kubernetes cluster with the help of eksctl and cloudformation stack

- Use CloudFormation to set up the infrastructure needed by the EKS cluster. See [CloudFormation](https://karpenter.sh/docs/reference/cloudformation/) for a complete description of what `cloudformation.yaml` does for Karpenter.
  
  ```
  curl -fsSL https://raw.githubusercontent.com/aws/karpenter-provider-aws/"${KARPENTER_VERSION}"/website/content/en/preview/getting-started/getting-started-with-karpenter/cloudformation.yaml  > $TEMPOUT \
  && aws cloudformation deploy \
    --stack-name "Karpenter-${CLUSTER_NAME}" \
    --template-file "${TEMPOUT}" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides "ClusterName=${CLUSTER_NAME}"
  ```

- Create `eks-cluster.yaml` to create aws eks. Please don't forget to mention tag `karpenter.sh/discovery: ${CLUSTER_NAME}`
  
  ```
  apiVersion: eksctl.io/v1alpha5
  kind: ClusterConfig
  metadata:
    name: ${CLUSTER_NAME}
    region: ${AWS_DEFAULT_REGION}
    version: "${K8S_VERSION}"
    tags:
      karpenter.sh/discovery: ${CLUSTER_NAME}
  
  iam:
    withOIDC: true
    podIdentityAssociations:
    - namespace: "${KARPENTER_NAMESPACE}"
      serviceAccountName: karpenter
      roleName: ${CLUSTER_NAME}-karpenter
      permissionPolicyARNs:
      - arn:${AWS_PARTITION}:iam::${AWS_ACCOUNT_ID}:policy/KarpenterControllerPolicy-${CLUSTER_NAME}
  
  ## Optionally run on fargate or on k8s 1.23
  # Pod Identity is not available on fargate  
  # https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html
  # iam:
  #   withOIDC: true
  #   serviceAccounts:
  #   - metadata:
  #       name: karpenter
  #       namespace: "${KARPENTER_NAMESPACE}"
  #     roleName: ${CLUSTER_NAME}-karpenter
  #     attachPolicyARNs:
  #     - arn:${AWS_PARTITION}:iam::${AWS_ACCOUNT_ID}:policy/KarpenterControllerPolicy-${CLUSTER_NAME}
  #     roleOnly: true
  
  iamIdentityMappings:
  - arn: "arn:${AWS_PARTITION}:iam::${AWS_ACCOUNT_ID}:role/KarpenterNodeRole-${CLUSTER_NAME}"
    username: system:node:{{EC2PrivateDNSName}}
    groups:
    - system:bootstrappers
    - system:nodes
    ## If you intend to run Windows workloads, the kube-proxy group should be specified.
    # For more information, see https://github.com/aws/karpenter/issues/5099.
    # - eks:kube-proxy-windows
  
  managedNodeGroups:
  - instanceType: m5.large
    amiFamily: AmazonLinux2
    name: ${CLUSTER_NAME}-ng
    desiredCapacity: 2
    minSize: 1
    maxSize: 10
  
  addons:
  - name: eks-pod-identity-agent
  
  ## Optionally run on fargate
  # fargateProfiles:
  # - name: karpenter
  #  selectors:
  #  - namespace: "${KARPENTER_NAMESPACE}"
  ```

- apply the `eks-cluster.yaml` from `eksctl cli` command
  
  ```
  eksctl create cluster -f eks-cluster.yaml
  ```

- Create a Kubernetes service account and AWS IAM Role, and associate them using IRSA to let Karpenter launch instances.

- Add the Karpenter node role to the aws-auth configmap to allow nodes to connect.

- Use [AWS EKS managed node groups](https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html) for the kube-system and karpenter namespaces. Uncomment fargateProfiles settings (and comment out managedNodeGroups settings) to use Fargate for both namespaces instead.

- Set KARPENTER_IAM_ROLE_ARN variables.
  
  ```
  export CLUSTER_ENDPOINT="$(aws eks describe-cluster --name ${CLUSTER_NAME} --query "cluster.endpoint" --output text)"
  export KARPENTER_IAM_ROLE_ARN="arn:${AWS_PARTITION}:iam::${AWS_ACCOUNT_ID}:role/${CLUSTER_NAME}-karpenter"
  
  echo $CLUSTER_ENDPOINT $KARPENTER_IAM_ROLE_ARN
  ```

- Create a role to allow spot instances.
  
  ```
  aws iam create-service-linked-role --aws-service-name spot.amazonaws.com || true
  # If the role has already been successfully created, you will see:
  # An error occurred (InvalidInput) when calling the CreateServiceLinkedRole operation: Service role name AWSServiceRoleForEC2Spot has been taken in this account, please try a different suffix.
  ```

- Connect eks cluster and Run helm to install karpenter
  
  ```
  #connect eks cluster
  aws eks update-kubeconfig --region ${AWS_DEFAULT_REGION} --name ${CLUSTER_NAME}
  
  # Logout of helm registry to perform an unauthenticated pull against the public ECR
  helm registry logout public.ecr.aws
  
  helm upgrade --install karpenter oci://public.ecr.aws/karpenter/karpenter --version "${KARPENTER_VERSION}" --namespace "${KARPENTER_NAMESPACE}" --create-namespace \
    --set "settings.clusterName=${CLUSTER_NAME}" \
    --set "settings.interruptionQueue=${CLUSTER_NAME}" \
    --set controller.resources.requests.cpu=1 \
    --set controller.resources.requests.memory=1Gi \
    --set controller.resources.limits.cpu=1 \
    --set controller.resources.limits.memory=1Gi \
    --wait
  ```

### Create NodePool for eks cluster by Karpenter

Create a default NodePool using the command below. This NodePool uses `securityGroupSelectorTerms` and `subnetSelectorTerms` to discover resources used to launch nodes. We applied the tag `karpenter.sh/discovery` in the `eksctl` command above. Depending on how these resources are shared between clusters, you may need to use different tagging schemes.

The `consolidationPolicy` set to `WhenUnderutilized` in the `disruption` block configures Karpenter to reduce cluster cost by removing and replacing nodes. As a result, consolidation will terminate any empty nodes on the cluster. This behavior can be disabled by setting `consolidateAfter` to `Never`, telling Karpenter that it should never consolidate nodes

```
cat <<EOF | envsubst | kubectl apply -f -
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      requirements:
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: kubernetes.io/os
          operator: In
          values: ["linux"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot"]
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["c", "m", "r"]
        - key: karpenter.k8s.aws/instance-generation
          operator: Gt
          values: ["2"]
      nodeClassRef:
        name: default
  limits:
    cpu: 1000
  disruption:
    consolidationPolicy: WhenUnderutilized
    expireAfter: 720h # 30 * 24h = 720h
---
apiVersion: karpenter.k8s.aws/v1beta1
kind: EC2NodeClass
metadata:
  name: default
spec:
  amiFamily: AL2 # Amazon Linux 2
  role: "KarpenterNodeRole-${CLUSTER_NAME}" # replace with your cluster name
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: "${CLUSTER_NAME}" # replace with your cluster name
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: "${CLUSTER_NAME}" # replace with your cluster name
EOF
```

Karpenter is now active and ready to begin provisioning nodes.

### Create and Scale up deployment

```
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: inflate
spec:
  replicas: 0
  selector:
    matchLabels:
      app: inflate
  template:
    metadata:
      labels:
        app: inflate
    spec:
      terminationGracePeriodSeconds: 0
      containers:
        - name: inflate
          image: public.ecr.aws/eks-distro/kubernetes/pause:3.7
          resources:
            requests:
```

### Scale and check the deployment status with node increase by Karpenter automatically in with respect to consumption

```
kubectl scale deployment inflate --replicas 5
kubectl logs -f -n "${KARPENTER_NAMESPACE}" -l app.kubernetes.io/name=karpenter -c controller
kubectl get pod 
kubectl get node
```

### Scale down and delete the deployment . node decrease by Karpenter automatically in with respect to consumption. After a short amount of time, Karpenter should terminate the empty nodes due to consolidation.

```
kubectl delete deployment inflate
kubectl logs -f -n "${KARPENTER_NAMESPACE}" -l app.kubernetes.io/name=karpenter -c controller
kubectl get pod
kubectl get node
```

## Delete Karpenter nodes manually

If you delete a node with kubectl, Karpenter will gracefully cordon, drain, and shutdown the corresponding instance. Under the hood, Karpenter adds a finalizer to the node object, which blocks deletion until all pods are drained and the instance is terminated. Keep in mind, this only works for nodes provisioned by Karpenter.

```
kubectl delete node $NODE_NAME
```

Certainly! Here's an updated documentation that includes information about using custom tags in Karpenter configurations:

---

### Karpenter Node Pool Configuration Documentation

#### Overview

Karpenter is a Kubernetes cluster autoscaler that provisions nodes based on the requirements of unschedulable pods. Node provisioning can be customized using selectors, allowing you to specify which security groups and subnets to use based on tags.

#### Configuration Breakdown

1. **securityGroupSelectorTerms**:
   - Specifies the security groups used for the nodes based on tags. 

2. **subnetSelectorTerms**:
   - Defines which subnets to use for provisioning nodes, also based on tags.

#### Example Node Pool Configuration

```yaml
apiVersion: karpenter.sh/v1alpha5
kind: Provisioner
metadata:
  name: example-provisioner
spec:
  limits:
    resources:
      requests:
        cpu: "1000m"   # Total CPU requested across the nodes
      limits:
        cpu: "2000m"    # Total CPU limit across the nodes
  provider:
    subnetSelectorTerms:
      - tags:
          karpenter.sh/discovery1: karpenter-test
    securityGroupSelectorTerms:
      - tags:
          karpenter.sh/discovery1: karpenter-test
  requirements:
    - key: "karpenter.sh/capacity-type"
      operator: In
      values: ["on-demand", "spot"]
```

#### Tagging Guidelines

- **Tag Format**: While the example uses a specific format (e.g., `karpenter.sh/discovery1`), it is not strictly necessary to adhere to this format. You can use custom tags that fit your organization’s naming conventions.
  
- **Custom Tags**: You can define your own tags for `subnetSelectorTerms` and `securityGroupSelectorTerms`. Just ensure that the tags you specify exist on your AWS resources (like subnets and security groups). For example:

  ```yaml
  subnetSelectorTerms:
    - tags:
        custom-tag: MyCustomValue
  securityGroupSelectorTerms:
    - tags:
        custom-tag: MyCustomValue
  ```

#### Working Mechanism

1. **Discovery**: Karpenter checks the specified tags to discover appropriate resources.
2. **Provisioning**: It provisions nodes using the filtered security groups and subnets based on the defined tags.
3. **Node Creation**: Nodes are created in the selected subnets with the corresponding security groups.

#### Monitoring and Troubleshooting

- **Check Events**: Use `kubectl get events` to monitor Karpenter events.
- **Pod Status**: Check the status of unschedulable pods to determine provisioning needs.
- **Logs**: Review Karpenter logs for detailed information:

  ```bash
  kubectl logs -l app=karpenter -n karpenter
  ```

- Karpenter provides a flexible way to manage node provisioning using both predefined and custom tags. This allows you to tailor the autoscaling capabilities to meet your specific infrastructure and application requirements.

### References

[Getting Started with Karpenter | Karpenter](https://karpenter.sh/docs/getting-started/getting-started-with-karpenter/)

[NodePools Configuration](https://karpenter.sh/docs/concepts/nodepools/)

[Karpenter - EKS Best Practices Guides](https://aws.github.io/aws-eks-best-practices/karpenter/)

https://aws.plainenglish.io/how-to-setup-karpenter-in-the-eks-cluster-3c8e285733f6

https://www.nops.io/blog/karpenter/

[Migrating from Cluster Autoscaler | Karpenter](https://karpenter.sh/docs/getting-started/migrating-from-cas/)

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
