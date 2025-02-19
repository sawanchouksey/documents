# Use EKS Hosted Jenkins with containerd as container engine and Use EKS pod as Jenkins agent to Run Docker Command without Docker Daemon using Nerdctl Cli

### Pre-requisite

1. AWS Cli or AWS Console with Admin Access

2. Kubectl Cli 

3. Nerdctl Package (optional if you have Internet , Github access)

4. Docker (in Local machine)

5. EKS (version >=1.25)

6. Jenkins Deploy in EKS

7. Jfrog Repository (Optional)

### Steps

1. Create a Dockerfile using jenkins-inbound-agent image as base images and customise it with full nerdctl package with all pre-requiste package depends upon on your requirements. Create Startup script to override the default inbound agent behavior.
   
   ```
   ------------
   Dockerfile
   ------------
   FROM jenkins/inbound-agent:latestcurl vim telnet dnsutils
   
   USER root
   
   # For Install nerdctl
   ENV NERDCTL_VERSION=1.7.4
   
   ENV ARCH_TYPE=amd64
   
   ENV BUILDKIT_VERSION=0.11.1
   
   # Install Gradle
   ENV GRADLE_VERSION="7.4"
   
   #Installing custom packages
   RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils
    
   # Installing custom dev tools 
   RUN apt-get update \
   	&& apt-get install -y --no-install-recommends apt-utils \
   	&& apt-get install -y apt-transport-https ca-certificates software-properties-common gnupg2 unzip wget vim curl gnupg lsb-release telnet dnsutils
   
   #RUN wget -q https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip \
   RUN curl -k -LO https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip \ 
    && unzip  gradle-${GRADLE_VERSION}-bin.zip -d /usr/bin \
    && ln -sf /usr/local/gradle-${GRADLE_VERSION}/bin/* /usr/bin \
    && rm -f gradle-${GRADLE_VERSION}-bin.zip
   
   # Check architecture and update ARCH_TYPE if necessary
   RUN if [ "$(uname -m)" = "aarch64" ]; then \
           export ARCH_TYPE="arm64"; \
       fi
   
   #Download and install nerdctl
   RUN wget -q --no-check-certificate "https://github.com/containerd/nerdctl/releases/download/v${NERDCTL_VERSION}/nerdctl-full-${NERDCTL_VERSION}-linux-${ARCH_TYPE}.tar.gz" -O /tmp/nerdctl.tar.gz
   
   RUN tar -xvzf /tmp/nerdctl.tar.gz -C /usr/local 
   
   RUN chmod +x /usr/local/bin/nerdctl
   
   # Copy the entrypoint script
   COPY entrypoint.sh /usr/local/bin/entrypoint.sh
   
   RUN chmod +x /usr/local/bin/entrypoint.sh
   
   # Set entrypoint to the custom script
   ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
   
   ---------------
   entrypoint.sh
   ---------------
   #!/bin/bash
   
   # Start BuildKit daemon
   buildkitd &
   
   # Wait for a short time to ensure buildkitd has started
   sleep 15
   
   # Execute the Jenkins JNLP agent entrypoint
   exec /usr/local/bin/jenkins-agent "$@"
   ```

2. Create custom jenkins agent docker Image and push it docker image repository i.e. dockerhub, ECR, Jfrog etc.
   
   ```
   docker build --no-cache -t agent:latest . 
   docker tag agent:latest artifactory.jfrog.com/docker-local/jenkins-build-nerdctl-agent:1.0.0
   docker push artifactory.jfrog.com/docker-local/jenkins-build-nerdctl-agent:1.0.0
   ```

3. create a yaml file for use custom image as Jenkins pod for Jenkins agent.
   
   ```
   -------------------------
   Jenkins-agent-pod.yaml
   -------------------------
   apiVersion: v1
   kind: Pod
   metadata:
     name: jenkins-slave
     annotations:
       "cluster-autoscaler.kubernetes.io/safe-to-evict": "false"
   spec:
     containers:
       - name:  jnlp
         image: artifactory.jfrog.com/docker-local/jenkins-build-nerdctl-agent:1.0.0
         securityContext:
           privileged: true
         volumeMounts:
         - name: containerd-socket
           mountPath: /run/containerd/containerd.sock
           readOnly: true
         resources:
           limits:
             cpu: 3
             memory: 6Gi
           requests:
             cpu: 1
             memory: 4Gi
     imagePullSecrets:
       - name: regcred-prod
     volumes:
       - name: containerd-socket
         hostPath:
           path: /run/containerd/containerd.sock
           type: Socket
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
                   container('nerdctl') {
                       sh """
                           nerdctl build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .
                       """
                   }
               }
           }
   
           stage('Push') {
               steps {
                   container('nerdctl') {
                       withCredentials([usernamePassword(credentialsId: 'docker-registry-creds', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                           sh """
                               nerdctl login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD} ${DOCKER_REGISTRY}
                               nerdctl push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
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

[Installing nerdctl - Guide 2 WSL](https://www.guide2wsl.com/nerdctl/)

[All you need to know about moving to containerd on Amazon EKS | Containers](https://aws.amazon.com/blogs/containers/all-you-need-to-know-about-moving-to-containerd-on-amazon-eks/)



### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
