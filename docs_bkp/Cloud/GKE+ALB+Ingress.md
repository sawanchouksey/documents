# GKE + Application Load Balancer + Ingress Route

### <mark>Pre-Requiste</mark>

1. Google Kubernetes Engine

2. VPC

3. SSL Certificate in .pfx format

## <mark>Tools Required</mark>

1. Kubectl Cli

2. gcloud Cli

## <mark>Access Required</mark>

### Owner or Admin level access for the following Services in GCP

- Google Kubernetes Engine

- Google Load Balancer

- IP addresses

- IAM

- Google Compute Engine

## <mark>Steps to Follow </mark>

### Create application with NodePort service type poc.yaml

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: poc-nodeport-com
  namespace: poc-nodeport
  labels:
    app: poc-nodeport-com
spec:
  replicas: 1
  selector:
    matchLabels:
      app: poc-nodeport-com
  template:
    metadata:
      labels:
        app: poc-nodeport-com
    spec:
      containers:
      - name: poc-nodeport-com
        image: asia-south1-docker.pkg.dev/poc-gcp-com/poc--registry/poc-microservice:latest
        env:
          - name: ENV_NAME
            value: 'poc'
        ports:
        - containerPort: 8080
        readinessProbe:
            httpGet:
              scheme: HTTP
              path: /api/health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 15
            timeoutSeconds: 5

---
kind: Service
apiVersion: v1
metadata:
  name: poc-nodeport-com
  namespace: poc-nodeport
spec:
  type: NodePort
  ports:
  - name: http
    port: 8080
    targetPort: 8080
    protocol: TCP
  selector:
    app: poc-nodeport-com
```

### deploy application with readiness probe for health check

### Create External IP Address

```
gcloud compute addresses create gke-ingress-extip1 --global
```

### get created-ip address from gcloud describe command

```
gcloud compute addresses describe gke-ingress-extip1  --region global --format=json | jq -r '.address'
```

## Certificate creation with pfx certificate

```
openssl pkcs12 -in NewSSL2024.pfx -nocerts -out server-en.key (give cert password)
openssl pkcs12 -in NewSSL2024.pfx -clcerts -nokeys -out app1-ingress.crt
openssl rsa -in server-en.key -out app1-ingress.key (give PEM pass password)
```

### Create a certificate resource in your Google Cloud project

```
gcloud compute ssl-certificates create app1-ingress --certificate app1-ingress.crt  --private-key app1-ingress.key
```

## Connect to GKE cluster

```
gcloud container clusters get-credentials GkeClusterName --region asia-south1 --project GCPProjectName
```

## Create namespace in GKE

```
kubectl create namespace poc-nodeport
```

## deploy application which we created earlier with NodePort Service

```
kubectl apply -f poc.yaml
```

## Use Following annotation to Create Load Balancer for Ingress

```
annotations:
    # External Load Balancer class name
    kubernetes.io/ingress.class: "gce"

    #External Laod Balancer name which will be created in GCP
    networking.gke.io/load-balancer-name: alb-gke-ingress

    #redirect ingress to ssl
    ingress.kubernetes.io/ssl-redirect: "true"

    # Static IP for Ingress Service
    kubernetes.io/ingress.global-static-ip-name: "gke-ingress-extip1"

    # Pre-shared certificate resources  
    ingress.gcp.kubernetes.io/pre-shared-cert: "app1-ingress"
```

### Create Ingress-route.yaml for create Application Load Balancer and routing traffic to your application in GKE from Internet

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-route
  namespace: poc-nodeport
  annotations:
    # External Load Balancer class name
    kubernetes.io/ingress.class: "gce"

    #External Laod Balancer name which will be created in GCP
    networking.gke.io/load-balancer-name: alb-gke-ingress

    #redirect ingress to ssl
    ingress.kubernetes.io/ssl-redirect: "true"

    # Static IP for Ingress Service
    kubernetes.io/ingress.global-static-ip-name: "gke-ingress-extip1"

    # Pre-shared certificate resources  
    ingress.gcp.kubernetes.io/pre-shared-cert: "app1-ingress"
spec:
  rules:
    - host: poc-nodeport.example.com
      http:
        paths:
        - path: /api
          pathType: Prefix
          backend:
            service:
              name: poc-nodeport-com
              port:
                number: 8080
```

## Deploy ingress-route.yaml

```
kubectl apply -f ingress-route.yaml
```

## Check Ingress deployment status

    kubectl describe ingress ingress-route -n poc-nodeport

**<u>Remark : The deployment of ingress take almost 5-10 minutes to setup in GCP</u>**

### Check Application with Exposed URL

https://poc-nodeport.example.com/api/health

##### Output:

![](C:\Users\sawchouksey\AppData\Roaming\marktext\images\2023-08-05-13-56-52-image.png)

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
