# Use EKS Hosted Jenkins with containerd as container engine and Use EKS pod as Jenkins agent to Run Docker Command without Docker Daemon using docker Cli

### Pre-requisite

1. AWS Cli or AWS Console with Admin Access

2. Kubectl Cli 

3. Docker (in Local machine)

4. EKS (version >=1.25)

5. Jenkins Deploy in EKS

6. Jfrog Repository (Optional)

### Steps

1. Create a Dockerfile using jenkins-inbound-agent image as base images and customise it with full docker package with all pre-requiste package depends upon on your requirements. Create Startup script to override the default inbound agent behavior.

   ```
   --------------------------------
   jenkins.agent.gradle.dockerfile
   --------------------------------
   FROM jenkins/inbound-agent:latestcurl vim telnet dnsutils
   
   USER root
    
   # Install Gradle
   ENV GRADLE_VERSION="7.4"

   RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb

   RUN dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb 
   
   # Installing custom dev tools 
   RUN apt-get update \
   	&& apt-get install -y --no-install-recommends apt-utils \
   	&& apt-get install -y apt-transport-https ca-certificates software-properties-common gnupg2 unzip wget vim curl gnupg lsb-release telnet dnsutils
   
   RUN curl -k -LO https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip \ 
    && unzip  gradle-${GRADLE_VERSION}-bin.zip -d /usr/bin \
    && ln -sf /usr/local/gradle-${GRADLE_VERSION}/bin/* /usr/bin \
    && rm -f gradle-${GRADLE_VERSION}-bin.zip
   
   ```

2. Create `daemon.json` file for enable customize docker daemon related configuration in our jenkins agent while invoking docker daemon during cicd build pipeline.

   ```
   ------------
   daemon.json
   ------------
   {
    "insecure-registries": [
      "artifactory.jfrog.com"
    ]
   }
   
   ```

3. Create custom Dockerfile for dind image customization because it will used as docker daemon in our jenkins agent.
   
   ```
   --------------------------------
   docker.daemon.dind.dockerfile
   --------------------------------
   FROM docker:20.10.16-dind

   RUN apk add --no-cache curl unzip zip wget tar

   COPY daemon.json /etc/docker/daemon.json

   RUN chmod 777 /etc/docker/daemon.json
   
   ```

4. Create custom jenkins agent docker Image and push it docker image repository i.e. dockerhub, ECR, Jfrog etc.
   
   ```
   docker build -f jenkins.agent.gradle.dockerfile -t agent:latest . 
   docker tag agent:latest artifactory.jfrog.com/docker-local/jenkins-build-dind-agent:1.0.0
   docker push artifactory.jfrog.com/docker-local/jenkins-build-dind-agent:1.0.0

   ```

5. Create custom jenkins dind docker Image and push it docker image repository i.e. dockerhub, ECR, Jfrog etc.
   
   ```
   docker build -f docker.daemon.dind.dockerfile -t docker:20.10.16-dind . 
   docker tag docker:20.10.16-dind artifactory.jfrog.com/docker-local/docker:20.10.16-dind
   docker push artifactory.jfrog.com/docker-local/docker:20.10.16-dind

   ```

6. create a yaml file for use custom image as Jenkins pod for Jenkins agent and also create container for Docker daemon running with the help of dind docker image.
   
   ```
   -------------------------
   Jenkins-agent-pod.yaml
   -------------------------
    apiVersion: "v1"
    kind: "Pod"
    metadata:
      name: jenkins-slave
      annotations:
        "cluster-autoscaler.kubernetes.io/safe-to-evict": "false"
    spec:
      containers:
        - name:  jnlp
          image: artifactory.jfrog.com/docker-local/jenkins-build-dind-agent:1.0.0
          imagePullPolicy: Always
          securityContext:
            privileged: true
          resources: {} 
          volumeMounts:
          - mountPath: "/home/jenkins/agent"
            name: "workspace-volume"
            readOnly: false
          workingDir: "/home/jenkins/agent"
          hostNetwork: false
        - name: "docker"
          image: artifactory.jfrog.com/docker-local/docker:20.10.16-dind
          imagePullPolicy: Always
          securityContext:
            privileged: true
          resources: {}
          volumeMounts:
          - mountPath: "/home/jenkins/agent"
            name: "workspace-volume"
            readOnly: false
          workingDir: "/home/jenkins/agent"
          hostNetwork: false
      serviceAccountName: jenkins-eks
      imagePullSecrets:
        - name: "jfrog-secret"
      volumes:
      - emptyDir:
          medium: ""
        name: "workspace-volume"

   ```

4. Use Jenkins agent pod to run docker command.
   
   ```
   -------------
   Jenkinsfile
   -------------
   pipeline {
       agent {
           kubernetes {
               yamlFile 'jenkins-agent-pod.yaml'
           }
       }
   
       environment {
           DOCKER_REGISTRY = 'your.docker.registry.com'
           IMAGE_NAME = 'your-image-name'
           IMAGE_TAG = "${env.BUILD_NUMBER}"
       }
   
       stages {
           stage('Build') {
               steps {
                   container('docker') {
                       sh """
                           docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .
                       """
                   }
               }
           }
   
           stage('Push') {
               steps {
                   container('docker') {
                       withCredentials([usernamePassword(credentialsId: 'docker-registry-creds', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                           sh """
                               docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD} ${DOCKER_REGISTRY}
                               docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                           """
                       }
                   }
               }
           }
       }
   }
   
   ```

### References

[Creating an Amazon EKS cluster - Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html)

https://www.jenkins.io/doc/book/installing/kubernetes/

[Installing docker - Guide 2 WSL](https://www.guide2wsl.com/docker/)

[All you need to know about moving to containerd on Amazon EKS | Containers](https://aws.amazon.com/blogs/containers/all-you-need-to-know-about-moving-to-containerd-on-amazon-eks/)



### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
