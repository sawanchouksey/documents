# # Access Secrets From AWS Secret Manager Mount to EKS Pods inside EKS cluster

### Pre-Requisite

- AWS CLI

- Kubectl Cli

- Eksctl Cli

- AWS Account with admin access

##### AWS Secrets Manager is a service provided by Amazon Web Services (AWS) that helps you protect sensitive data, such as passwords, API keys, and database credentials, by encrypting and storing them securely. When working with Amazon Elastic Kubernetes Service (EKS) clusters and pods, you can use AWS Secrets Manager to securely store and retrieve sensitive data.

Here's a general outline of how you can use AWS Secrets Manager with an EKS cluster and pods:

1. **Create a Secret in AWS Secrets Manager**: Store the sensitive data you want to use in your EKS cluster and pods as a secret in AWS Secrets Manager. You can create a new secret or store an existing one.
2. **Create an IAM Policy and Role**: Create an AWS Identity and Access Management (IAM) policy that grants permission to access the specific secret in AWS Secrets Manager. Create an IAM role associated with the EKS cluster and attach the IAM policy to this role.
3. **Configure the EKS Cluster to Use the IAM Role**: Associate the IAM role you created with the EKS cluster. This allows the EKS control plane to assume the role and access the secrets on your behalf.
4. **Create a Kubernetes Secret**: In your EKS cluster, create a Kubernetes secret that references the AWS Secrets Manager secret. You can use the AWS CLI or the AWS SDK to retrieve the secret value from AWS Secrets Manager and create a Kubernetes secret with the same value.
5. **Use the Kubernetes Secret in Your Pods**: Mount the Kubernetes secret as a volume or an environment variable in your pod's specification. This way, your application running inside the pod can access the sensitive data without exposing it directly.

#### create aws secrets,mount to eks deployments or use it as environment variable.

###### Create IAM User with Full Access

- Create admin user and place it in Admin IAM group
- Configure aws cli aws configure

##### Create Secret in AWS Secrets Manager

```
aws --region "$AWS_REGION" secretsmanager \
  create-secret --name MySecret \
  --secret-string '{"username":"postgres", "password":"test@123"}'
```

##### Create EKS Cluster Using eksctl

- Create cluster.yaml config file
  
  ```
  apiVersion: eksctl.io/v1alpha
  kind: ClusterConfig
  metadata:
    name: sad
    region: ap-south-1
  nodeGroups:
    - name: ng1
      instanceType: t2.large
      desiredCapacity: 1
      volumeSize: 20
      ssh:
        allow: false
  Create EKS cluste
  ```

- Apply the cluster.yaml file
  
  ```
  eksctl create cluster -f cluster.yaml
  ```

##### Create IAM OIDC Provider for EKS

```
eksctl utils associate-iam-oidc-provider \
    --region=ap-south-1 --cluster=sad \
    --approve
```

##### Create IAM Policy to Read Secrets

- Create APITokenReadAccess IAM policy
  
  ```
  POLICY_ARN=$(aws --region ap-south-1 --query Policy.Arn --output text iam create-policy --policy-name nginx-deployment-policy --policy-document '{
      "Version": "2012-10-17",
      "Statement": [ {
          "Effect": "Allow",
          "Action": ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"],
          "Resource": [ARN_AWS_RESOURCE]
      } ]
  ```

##### Create IAM Role and Kubernetes Service Account

```
eksctl create iamserviceaccount --name nginx-deployment-sa --region="$REGION" --cluster "$CLUSTERNAME" --attach-policy-arn "$POLICY_ARN" --approve --override-existing-serviceaccounts
```

##### Install CSI drivers and ASCP Providers

- With the help of Helm Repo
  
  ```
  helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
  helm install -n kube-system csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver
  
  helm repo add aws-secrets-manager https://aws.github.io/secrets-store-csi-driver-provider-aws
  helm install -n kube-system secrets-provider-aws aws-secrets-manager/secrets-store-csi-driver-provider-aws
  
  helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
  helm install -n kube-system csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver
  ```

- With the help of Yaml file
  
  ```
  # https://kubernetes.io/docs/reference/access-authn-authz/rbac
  apiVersion: v1
  kind: ServiceAccount
  metadata:
    name: csi-secrets-store-provider-aws
    namespace: kube-system
  ---
  apiVersion: rbac.authorization.k8s.io/v1
  kind: ClusterRole
  metadata:
    name: csi-secrets-store-provider-aws-cluster-role
  rules:
  - apiGroups: [""]
    resources: ["serviceaccounts/token"]
    verbs: ["create"]
  - apiGroups: [""]
    resources: ["serviceaccounts"]
    verbs: ["get"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get"]
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get"]
  ---
  apiVersion: rbac.authorization.k8s.io/v1
  kind: ClusterRoleBinding
  metadata:
    name: csi-secrets-store-provider-aws-cluster-rolebinding
  roleRef:
    apiGroup: rbac.authorization.k8s.io
    kind: ClusterRole
    name: csi-secrets-store-provider-aws-cluster-role
  subjects:
  - kind: ServiceAccount
    name: csi-secrets-store-provider-aws
    namespace: kube-system
  ---
  apiVersion: apps/v1
  kind: DaemonSet
  metadata:
    namespace: kube-system
    name: csi-secrets-store-provider-aws
    labels:
      app: csi-secrets-store-provider-aws
  spec:
    updateStrategy:
      type: RollingUpdate
    selector:
      matchLabels:
        app: csi-secrets-store-provider-aws
    template:
      metadata:
        labels:
          app: csi-secrets-store-provider-aws
      spec:
        serviceAccountName: csi-secrets-store-provider-aws
        hostNetwork: false
        containers:
          - name: provider-aws-installer
            image: public.ecr.aws/aws-secrets-manager/secrets-store-csi-driver-provider-aws:1.0.r2-58-g4ddce6a-2024.01.31.21.42
            imagePullPolicy: Always
            args:
                - --provider-volume=/etc/kubernetes/secrets-store-csi-providers
            resources:
              requests:
                cpu: 50m
                memory: 100Mi
              limits:
                cpu: 50m
                memory: 100Mi
            securityContext:
              privileged: false
              allowPrivilegeEscalation: false
            volumeMounts:
              - mountPath: "/etc/kubernetes/secrets-store-csi-providers"
                name: providervol
              - name: mountpoint-dir
                mountPath: /var/lib/kubelet/pods
                mountPropagation: HostToContainer
        volumes:
          - name: providervol
            hostPath:
              path: "/etc/kubernetes/secrets-store-csi-providers"
          - name: mountpoint-dir
            hostPath:
              path: /var/lib/kubelet/pods
              type: DirectoryOrCreate
        nodeSelector:
          kubernetes.io/os: linux
  ```
  
  ```
  kubectl apply -f https://raw.githubusercontent.com/aws/secrets-store-csi-driver-provider-aws/main/deployment/aws-provider-installer.yaml
  ```

- Verify the installation 
  
  ```
  kubectl get daemonsets -n kube-system -l app=csi-secrets-store-provider-aws
  kubectl get daemonsets -n kube-system -l app.kubernetes.io/instance=csi-secrets-store
  
  output:
  NAME                             DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
  csi-secrets-store-provider-aws   1         1         1       1            1           kubernetes.io/os=linux   2m34s
  
  NAME                                         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
  csi-secrets-store-secrets-store-csi-driver   1         1         1       1            1           kubernetes.io/os=linux   2m42s
  ```

##### Create SecretProviderClass to extract key-value pairs

```
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: nginx-deployment-spc
spec:
  provider: aws
  parameters: 
    objects: |
      - objectName: "mysecret"
        objectType: "secretsmanager"
        jmesPath:
          - path: username
            objectAlias: dbusername
          - path: password
            objectAlias: dbpassword
  secretObjects:                
    - secretName: my-secret-01
      type: Opaque
      data:
        - objectName: dbusername
          key: db_username_01
        - objectName: dbpassword
          key: db_password_01
```

##### The following example shows a another way `SecretProviderClass` that mounts three files in Amazon EKS

1. A secret specified by full ARN.

2. A secret specified by name.

3. A specific version of a secret.

```
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: nginx-deployment-spc
spec:
  provider: aws
  parameters:
    objects: |
        - objectName: "arn:aws:secretsmanager:us-east-2:111122223333:secret:MySecret2-d4e5f6"
        - objectName: "MySecret3"
          objectType: "secretsmanager"
        - objectName: "MySecret4"
          objectType: "secretsmanager"
          objectVersionLabel: "AWSCURRENT"
```

##### Above mentioned `nginx-deployment-spc.yaml` secretObjects block is used to mount secret as environment variables,and Objects block avails the secret for the secretObjects block and volume mounting.

```
kubectl apply -f nginx-deployment-spc.yaml
```

##### Create pod mount secrets volumes and set up Environment variables.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment-k8s-secrets
  labels:
    app: nginx-k8s-secrets
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-k8s-secrets
  template:
    metadata:
      labels:
        app: nginx-k8s-secrets
    spec:
      serviceAccountName: nginx-deployment-sa
      containers:
      - name: nginx-deployment-k8s-secrets
        image: nginx
        imagePullPolicy: IfNotPresent
        ports:
          - containerPort: 80
        volumeMounts:
          - name: secrets-store-inline
            mountPath: "/mnt/secrets"
            readOnly: true
        env:
          - name: DB_USERNAME_01
            valueFrom:
              secretKeyRef:
                name: my-secret-01
                key: db_username_01
          - name: DB_PASSWORD_01
            valueFrom:
              secretKeyRef:
                name: my-secret-01
                key: db_password_01
      volumes:
        - name: secrets-store-inline
          csi:
            driver: secrets-store.csi.k8s.io
            readOnly: true
            volumeAttributes:
              secretProviderClass: nginx-deployment-spc
```

##### create and apply the `nginx-deployment.yaml` deployment file

```
kubectl apply -f nginx-deployment.yaml
```

##### Verify the result and deployment by access secret manager values

```
kubectl get pod 
kubectl exec -it ${POD_NAME} -- /bin/bash
cat /mnt/secrets/MySecret

output:
{"username":"postgres", "password":"test@123"}

cat /mnt/secrets/dbusername

output:
postgres

- which means secrets are mounted as a file.
env | grep DB 

output:
root@nginx-deployment-k8s-secrets-7478c89bd8-qc4jp:/# env | grep DB
DB_USERNAME_01=postgres
DB_PASSWORD_01=test@123
```

**which means secrets are mounted as environment variable.**

**we can clearly see secrets that are stored in the aws secrets are retrieved and deployment having right service-account can access those.**

#### References and links:

https://www.linkedin.com/pulse/mounting-aws-secrets-eks-pods-mohammad-akif/
https://docs.aws.amazon.com/secretsmanager/latest/userguide/integrating_csi_driver.html

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
