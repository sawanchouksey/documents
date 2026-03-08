## Docker

### Containerization & Container Management

##### Q. How would you free up disk space on a Docker host?
- Remove unused containers with: `docker container prune`
- Remove unused images (dangling and unreferenced): `docker image prune -a`
- Remove unused volumes: `docker volume prune`
- Clean up unused networks: `docker network prune`
- Reclaim space from all unused objects: `docker system prune -a`

##### Q. How would you troubleshoot and debug a running Docker container?
- Access the container's shell using: `docker exec -it <container_name> /bin/bash`
- Check container logs using: `docker logs <container_name>`
- Inspect the container's state with: `docker inspect <container_name>`

##### Q. How would you troubleshoot and resolve network connectivity issues between Docker containers?
- Verify network configuration using: `docker network inspect <network_name>`
- Check connectivity between containers using: `docker exec -it <container_name> ping <other_container_ip_or_name>`
- If DNS resolution is failing, ensure you are using the correct container names, as Docker provides built-in DNS resolution for containers on the same network.

##### Q. How would you investigate and resolve a container that continuously restarts?
- Examine the logs using: `docker logs <container_name>`
- Use the docker inspect command to check the container's restart policy: `docker inspect <container_name> | grep RestartPolicy`
- Adjust the policy to avoid endless restarts: `docker run --restart=on-failure:3 <container_image>`

##### Q. What steps would you take to secure a Docker container?
- Avoid running applications as root inside the container. In the Dockerfile, create a non-root user:
  ```dockerfile
  RUN useradd -ms /bin/bash myuser
  USER myuser
  ```
- Enable user namespaces to map container users to different users on the host
- Only expose necessary ports and limit external access with firewall rules
- Use Docker's bridge network mode for isolation

##### Q. How would you roll back to a previous Docker image version?
- If tagged properly: `docker run -d my_image:previous_version`
- If the old image is present: `docker images` then `docker run -d <image_id>`

##### Q. How would you force stop a Docker container that refuses to stop?
- Attempt graceful stop: `docker stop <container_name>`
- Forcibly kill it: `docker kill <container_name>`
- Investigate using `docker inspect` to check for resource constraints or system issues

##### Q. What is a Docker registry and why do we need it?
A Docker registry is a storage and distribution system for Docker images. It allows users to store, manage, and distribute Docker container images.

**Key Points:**
- **Storage:** Stores Docker images and their versions in a central location
- **Distribution:** Facilitates sharing and deploying images across different environments and teams
- **Security:** Manages access controls and authentication
- **Versioning:** Keeps track of different versions of images

**Why We Need It:**
- Centralized management
- Consistency across environments
- Efficient deployment
- Team collaboration

##### Q. What is the difference between COPY and ADD command in Dockerfile?

**1. Functionality:**
- **COPY:** Straightforward file transfer without extraction or processing
- **ADD:** Can use URLs or extract compressed archives directly into the image

**2. Caching:**
- **COPY:** Cacheable, leading to faster builds when source files haven't changed
- **ADD:** Not cacheable in the same way due to complex operations

**3. URLs and Archives:**
- **COPY:** Only for local files and directories
- **ADD:** Supports URLs and automatic extraction of compressed archives

**Best Practices:** Use COPY when only copying local files, use ADD when specifically requiring URL downloads or archive extraction.

##### Q. Explain the typical lifecycle of a Docker container

1. Pull or create a Docker image
2. Create a container from the image
3. Run the container
4. Stop the container
5. Restart the container
6. Kill the container (if needed)
7. Prune or reclaim the resources

##### Q. What are the two ways to download Docker images?
- **Explicit:** Using `docker pull` command
- **Implicit:** When executing `docker run`, Docker daemon searches locally and downloads if not found

##### Q. How to transfer Docker images between machines without internet?
```bash
docker save -o images.tar image1 image2 image3
docker load -i images.tar
```

##### Q. How to import and export Docker containers?
```bash
docker export -o container.tar container_name
docker import container.tar
```

##### Q. How to check steps executed in Docker images?
```bash
docker image history acme/my-final-image:1.0
```

##### Q. How many types of Docker volumes?

1. **Host volumes:** Direct access to host file system
   ```bash
   docker run -v /path/on/host:/path/in/container
   ```

2. **Anonymous volumes:** Managed by Docker, automatically deleted with container
   ```bash
   docker run -v /path/in/container
   ```

3. **Named volumes:** Easier to manage and share between containers
   ```bash
   docker volume create somevolumename
   docker run -v somevolumefileName:/path/in/container
   ```

##### Q. Difference between --mount vs --volume in Docker?
- **--volume (-v):** Three colon-separated fields, order-dependent
  ```bash
  --volume $(pwd):/backup/user:rw
  ```
- **--mount:** Key-value pairs, more verbose but clearer
  ```bash
  --mount 'type=volume,src=<VOLUME-NAME>,dst=<CONTAINER-PATH>'
  ```

##### Q. How many types of Docker network?

1. **Bridge networks:** Default, used within a single host
2. **Overlay networks:** For multi-host communication
3. **Macvlan networks:** Connect containers directly to host network interfaces

##### Q. What is the default Docker network?
**Bridge** is the default network driver for standalone containers that need to communicate.

##### Q. What does "docker inspect" command do?
```bash
docker inspect --format '{{ .NetworkSettings.IPAddress }}' container_id
```
This extracts the exact private IP address of the container.

##### Q. Can you override the ENTRYPOINT at runtime?
Yes, using `--entrypoint` flag.

##### Q. What are the two types of registries in Docker?
1. **Public Registry:** Docker Hub for public images
2. **Private Registry:** For in-premise or private use

##### Q. How do Docker client and Docker Daemon communicate?
Through a mix of RESTful API, socket I/O, and TCP.

##### Q. Can we add multiple machines in Docker Swarm without installing Docker Swarm on each machine?
No, Docker Swarm must be installed on each machine.

##### Q. Difference between "docker create" and "docker run"?
- **docker create:** Creates container but doesn't start it
- **docker run:** Creates and starts the container

##### Q. What is "null" network driver?
Activated with `docker run --net none`. The container gets no IP address and has no external network access. Used for local batch jobs.

##### Q. How to ensure container execution order in Docker Compose?
Use the `depends_on` condition:
```yaml
version: "2.4"
services:
  backend:
    build: .
    depends_on:
      - db
  db:
    image: postgres
```

##### Q. Who owns the Docker control socket?
Docker control socket is owned by the docker group.

##### Q. Can an ARG variable be used by the running container?
No, ARG variables are exclusively for Dockerfile use.

##### Q. How to see container logs in real-time?
```bash
docker logs --follow <container_id>
```

##### Q. Can a normal user read files mounted by Docker container with root user?
No.

### Intermediate/Advanced Docker Scenarios

##### Q. Write a Dockerfile for a secure Python/Node.js API with multistage builds and best practices.
```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
# Do not run as root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
# Copy isolated dependencies
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/src ./src
# Assign permissions
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 3000
CMD ["node", "src/index.js"]
```

##### Q. How do multistage Docker builds improve security and reduce image size?
- Multistage builds allow separating the build environment (which needs compilers, SDKs, and source code) from the runtime environment.
- Only the compiled artifacts/executables are copied to the final stage.
- **Size:** Eliminates bulky dev dependencies, leading to smaller, faster-loading images.
- **Security:** Reduces the attack surface by excluding tools (e.g., curl, bash, compilers) that attackers could exploit if the container is compromised.

##### Q. Differentiate between Docker volumes and bind mounts. When do you use each in a Kubernetes environment?
- **Docker Volumes:** Managed by Docker/Kubernetes inside its own storage directory. Independent of the underlying host OS paths. Best for persistent databases.
- **Bind Mounts:** Maps a specific, absolute path on the host machine to a directory in the container.
- **In K8s:** `hostPath` (bind mount) is rarely used, mostly for accessing host-level configurations (like node logs or DaemonSets). PersistentVolumeClaims (PVCs) mapping to remote cloud storage (abstracted volumes) are the standard for stateful workloads.

---



### Advanced Docker Scenarios & Security

##### Q. You need to run Docker-in-Docker (DinD) for a nested CI pipeline. How do you design this securely and reliably?
**Answer:**
Running pure Docker-in-Docker (DinD) requires granting the CI agent container `--privileged` mode, exposing the host kernel to immense security risks.
- **Secure Alternative 1 (Kaniko / Buildah):** I avoid DinD entirely. I use tools like Google's Kaniko or Buildah, which run as unprivileged user-space applications to build container images without requiring a Docker daemon or root privileges.
- **Secure Alternative 2 (Sysbox):** If full Docker functionality is strictly mandated, I run the workload inside a Sysbox runtime (a specialized runc) that provides strong isolation via user-namespaces, allowing system-level software to run inside a container safely without `--privileged` flags.
- **Sock Mounting:** If using traditional Docker-out-of-Docker (DooD), pass the `/var/run/docker.sock` volume carefully, acknowledging the container can spin up sibling containers on the underlying host.

##### Q. How do you ensure that your container images are immutable and traceable across environments?
**Answer:**
1. **Immutability:** Configure your container registry (like ECR, ACR, or Harbor) to enable `Immutable Tags`. This hard-blocks developers from overwriting `/pushing` an existing tag like `v1.2.0`, preventing identical tags from pointing to completely different code.
2. **Digest Hashing:** Always deploy images to production using their immutable SHA256 digest (e.g., `image: myapp@sha256:abcd123...`) rather than mutable tags like `latest`.
3. **Traceability & Signatures:** Utilize **Cosign (Sigstore)** during the CI pipeline. The pipeline builds the image, signs it cryptographically, and pushes the signature alongside it. An admission controller (like Kyverno) on the production cluster independently verifies the Cosign signature before allowing the pod to boot, guaranteeing exactly which pipeline built it.


### Container Security & Management

##### Q. What’s your strategy for managing container image security across all stages of a DevOps pipeline?
**Answer:**
Container security involves protecting the build phase, registry phase, and runtime phase.
1. **Base Images:** Developers must universally use minimal "Distroless" or "Alpine" base images heavily eliminating extraneous OS binaries (like `curl` or `bash`) preventing attackers from establishing firm footholds.
2. **CI Pipeline (Build Time):** Tools like **Trivy** or **Grype** statically scan the generated image in the pipeline. The pipeline errors heavily and halts the push manually if any Critical/High OS or Library CVEs persist.
3. **Registry (Storage Time):** Continuous background scanning enabled within ECR/ACR triggering notifications securely as entirely new vulnerabilities are dynamically discovered weeks post-deployment.
4. **Runtime (Admission Control):** An OPA Gatekeeper policy mathematically preventing Pods executing as `root`, disallowing privilege escalation parameters globally across clusters.
