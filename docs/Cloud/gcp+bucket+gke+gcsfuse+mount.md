# GCSFUSE+GCP+BUCKET+GKE+MOUNT

# For Java Application with Ubuntu Linux Docker Images

### Create Dockerfile and install GcsFuse inside the image

### Dockerfile

```
# Pull base image.
FROM tomcat:9.0.58-jdk17-openjdk-slim

# Set Locale for container..
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

# Copy environment helper script
COPY setenv.sh /usr/local/tomcat/bin

#Copy GKE credentials for connect GKE with Bucket
COPY ./gke-creds.json /usr/local/tomcat

#Copy war files in webapps folder in tomcat
COPY ./example.war /usr/local/tomcat/webapps

# Install GCS Fuse
ENV GCSFUSE_REPO gcsfuse-stretch
RUN apt-get update && apt-get install --yes --no-install-recommends \
    ca-certificates \
    curl \
    gnupg \
  && echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" \
    | tee /etc/apt/sources.list.d/gcsfuse.list \
  && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
  && apt-get update \
  && apt-get install --yes gcsfuse \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 
```

### Create setenv.sh file to mount bucket with gcsfuse

### setenv.sh

```
#!/bin/bash
mkdir BucketTest && gcsfuse --key-file="/usr/local/tomcat/cred.json" gcs_fuse_test BucketTest
export JAVA_OPTS
```

### Create deployment.yaml file for deploy application in gke

### deployment.yaml

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: example-admin-services
  name: example-admin-services
spec:
  selector:
    matchLabels:
      app: example-admin-services
  replica: 1
  template:
    metadata:
      labels:
        app: example-admin-services
    spec:
      containers:
        image: europe-west1-docker.pkg.dev/example-poc/example/example-admin-services:gcsfuse
        imagePullPolicy: IfNotPresent
        lifecycle:
          preStop:
            exec:
              command:
              - fusermount
              - -u
              - /data
        livenessProbe:
          failureThreshold: 5
          httpGet:
            path: /example-admin-services/rest/health
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 600
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        name: example-admin-services-ctr
        ports:
        - containerPort: 8080
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /example-admin-services/rest/health
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 60
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        resources:
          limits:
            cpu: "1"
            memory: 4Gi
          requests:
            cpu: 500m
            memory: 2Gi
        securityContext:
          capabilities:
            add:
            - SYS_ADMIN
          privileged: true
```

# For Node Application with alpine linux docker image

### Create Dockerfile and install GcsFuse inside the image

### Dockerfile

```
FROM node:16.17-alpine3.15

# add required tools and dependencies
RUN apk add --no-cache \
ca-certificates \
fuse \
openssl \
wget \
curl \
go \
git \
&& update-ca-certificates

WORKDIR /app

RUN git clone https://github.com/GoogleCloudPlatform/gcsfuse.git

WORKDIR /app/gcsfuse

RUN go install .

RUN ["chmod", "+x", "/root/go/bin/gcsfuse"]

WORKDIR /app

COPY ["package.json", "package-lock.json","./"]

COPY ["gke-bucket-cred.json","./"]

RUN npm add

COPY . /app

RUN ["chmod", "+x", "/app/startup.sh"]

ENTRYPOINT ["/app/startup.sh"]
```

### Create startup.sh file to mount folder inside bucket with gcsfuse

### startup.sh

```
#!/bin/sh
mkdir /app/logs && /root/go/bin/gcsfuse --key-file="/app/.gke-bucket-credjson" --only-dir=logs poc-bucket /app/logs 
npm run start:${ENV_NAME}
```

### Create deployment.yaml file for deploy application in gke

### deployment.yaml

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-dev-logs
  labels:
    app: example-dev-logs
spec:
  replicas: 1
  selector:
    matchLabels:
      app: example-dev-logs
  template:
    metadata:
      labels:
        app: example-dev-logs
    spec:
      containers:
        - name: example-dev-logs
          image: asia-south1-docker.pkg.dev/example-poc/example/example-dev:gcsfuse
          lifecycle:
            preStop:
              exec:
                command: ["fusermount", "-u", "/app/logs"]
          env:
          - name: ENV_NAME
            value: "dev"
          ports:
            - containerPort: 5004
          securityContext:
            capabilities:
              add:
              - SYS_ADMIN
            privileged: true
```

# GCP storage bucket mount to GKE with CSI driver

https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/cloud-storage-fuse-csi-driver

https://chimbu.medium.com/access-cloud-storage-buckets-as-volumes-in-gke-c2e405adea6c

### To enable the driver on an existing Standard cluster

```
gcloud container clusters update kubernetes \
    --update-addons GcsFuseCsiDriver=ENABLED \
    --region=asia-south1
```

### Create service account in gke

```
kubectl create serviceaccount k8s-gcs \
    --namespace default
```

### Create an IAM service account for your application or use an existing IAM service account

```
gcloud iam service-accounts create k8s-gcs-bucket \
    --project=example-gcsfuse-prj
```

### You can grant the role to your IAM service account to only access a specific Cloud Storage bucket

```
gcloud storage buckets add-iam-policy-binding gs://bucket-001 \
    --member "serviceAccount:k8s-gcs-bucket@test-dev.iam.gserviceaccount.com" \
    --role "editor"
```

### Allow the Kubernetes service account to impersonate the IAM service account by adding an IAM policy binding between the two service accounts

```
gcloud iam service-accounts add-iam-policy-binding k8s-gcs-bucket@example-gcsfuse-prj.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:example-gcsfuse-prj.svc.id.goog[default/k8s-gcs]"
```

### Annotate the Kubernetes service account with the email address of the IAM service account

```
kubectl annotate serviceaccount k8s-gcs \
    --namespace default \
    iam.gke.io/gcp-service-account=k8s-gcs-bucket@example-gcsfuse-prj.iam.gserviceaccount.com
```

### Configure resources for the sidecar container overwrite deafult value

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

### Consume the CSI ephemeral storage volume in a Pod

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
        bucketName: bucket-001
        mountOptions: "implicit-dirs"
```

### Disable the Cloud Storage FUSE CSI driver

```
gcloud container clusters update CLUSTER_NAME \
    --update-addons GcsFuseCsiDriver=DISABLED
```

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
