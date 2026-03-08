## Jenkins & CI/CD

### Continuous Integration & Deployment

##### Q. What is Jenkins?
Open-source CI/CD server written in Java for automating build cycles. Can be self-hosted, triggered via CLI or web interface.

**Benefits:**
- Open-source with large community
- Many available plugins
- Java-based (portable)
- Automated integration reduces manual work
- Faster development
- Early issue detection
- Higher quality software

##### Q. What are Jenkins plugins?
Primary means of enhancing Jenkins functionality to suit organization/user-specific needs.

##### Q. Connect Jenkins with Azure cloud without user credentials?
Using System Managed Identity (exists as long as resource exists).

##### Q. What is CI/CD?

**Continuous Integration (CI):**
- Automatic code integration from multiple developers
- Automated testing
- Multiple merges per day/commit
- Uses CI tools

**Continuous Delivery (CD):**
- Automated building and packaging
- Ready for deployment (one-click release)
- Minimal human intervention

**Continuous Deployment:**
- Automatic deployment to production
- Full automation from commit to production

##### Q. What is GitLab Runner?
Application that works with GitLab CI/CD to run jobs in a pipeline.

##### Q. Store environment variables for Jenkins pipeline?

**1. Pipeline Environment Blocks:**
```groovy
pipeline {
    agent any
    environment {
        MY_VARIABLE = 'my_value'
    }
    stages {
        stage('Build') {
            steps {
                echo "My variable: ${MY_VARIABLE}"
            }
        }
    }
}
```

**2. Global Environment Variables:**
Manage Jenkins > Configure System > Global properties

**3. Credentials Plugin:**
```groovy
withCredentials([string(credentialsId: 'my-secret-credential', variable: 'SECRET_KEY')]) {
    // Access SECRET_KEY in this block
}
```

##### Q. Troubleshoot failing pipelines automatically?

1. **Monitoring and Alerting:**
   - Prometheus, Grafana, New Relic, Datadog
   - Track pipeline health and performance

2. **Logging and Tracing:**
   - ELK Stack, Fluentd, Splunk
   - Centralized log storage
   - Automated log analysis

3. **Automatic Remediation:**
   - Automation scripts for known issues
   - Auto-restart for crashes

4. **Clear Success/Failure Criteria:**
   - Define alerts for various stages
   - Set up notifications

---



### Jenkins Architecture & Pipelines

##### Q. Have you created a Jenkins pipeline for your project?
Yes, I build **Declarative Jenkins Pipelines** (`Jenkinsfile`). Specifically, multibranch pipelines that automatically trigger on GitHub pushes. The pipeline consists of structured stages: Git Checkout, continuous integration tasks (Maven/NPM build, SonarQube linting, Junit tests), Docker image building/pushing to ECR, and finally invoking Terraform or Kubernetes apply for CD, utilizing manual approval gates for production.

##### Q. What is Groovy, and how is it used in Jenkins?
**Groovy** is an object-oriented scripting language tightly integrated natively with the Java platform. Jenkins uses Groovy as the underlying foundation for its Pipeline DSL (Domain Specific Language), allowing the dynamic composition of complex automated deployment tasks.

##### Q. Why do you use Groovy in Jenkins, and where do you save Jenkins files?
Groovy provides powerful dynamic typing, string processing, and deep Java integrations inherently needed when writing programmatic continuous integration workflows (especially in Jenkins Scripted Pipelines or Shared Libraries). 
The `Jenkinsfile` itself is saved strictly in the **root directory of the project's Git repository**. This is the "Pipeline as Code" method, ensuring infrastructure delivery aligns dynamically with the application code branches.

##### Q. Do you have separate Jenkins servers for each environment?
Typically, **no**. The standard architecture is a single highly available, isolated Jenkins Controller for the organization. However, workloads are segmented by routing deployment jobs for different environments (Dev/Prod) to distinct, strictly tagged **Jenkins Worker Nodes (Agents)** running in isolated VPCs. They assume different IAM roles per environment leveraging secure credential injection, ensuring a blast radius is contained.


### Advanced CI/CD Troubleshooting

##### Q. Jenkins jobs are randomly failing at the artifact upload step. What layers would you check?
**Answer:**
1. **Jenkins Agent Level:** Check if the executing Jenkins node is experiencing SNAT port exhaustion, memory limits, or running out of local disk space midway through packaging the artifact.
2. **Network Layer:** Look for intermittent proxy timeouts. If uploading a huge Docker image or a 2GB `.jar` file, Load Balancers or corporate Proxies might be enforcing TCP timeouts for long-running connections.
3. **Target Repository Level:** Verify if the target (Nexus, Artifactory, S3, ACR) is imposing rate-limiting, running background Garbage Collection pauses, or out of storage capacity, leading to intermittent 500/503 HTTP responses during uploads.

##### Q. How would you design and implement a secure and scalable CI/CD pipeline from code commit to production deployment?
**Answer:**
- **Source Phase:** Code is committed to a Git repository triggering strict branch protection (no direct pushes, requiring PR approvals, and passing unit tests).
- **Build Phase (CI):** An ephemeral agent (Jenkins/GitHub Actions) checks out the code. Dependencies are resolved, custom logic executes (compile), and static code analysis (SonarQube) runs. The app is packaged into a Docker image.
- **Security Phase:** The image is scanned by tools like Trivy for CVEs. If clean, it's pushed to a secure Registry (ACR/ECR) and cryptographically signed (Sigstore/Cosign).
- **Deployment Phase (CD):** GitOps (ArgoCD/Flux) constantly polls the registry and Git configurations. When a new valid release hash surfaces, ArgoCD safely pulls the deployment manifesting changes sequentially from Dev -> Staging -> Prod utilizing Blue/Green strategies, gated by automated integrations testing and manual sign-offs.

##### Q. What tools or techniques would you use to integrate security scanning into the CI/CD process without slowing down delivery?
**Answer:**
Security must "Shift Left" seamlessly. 
- **Pre-Commit:** Integrating `trufflehog` or `git-secrets` natively via Git hooks on the developer's laptop to block accidentally committed AWS keys instantly.
- **CI/Build Time:** 
  1. **SAST:** Implementing lightweight static analysis integrated directly onto PRs (e.g., SonarQube quality gates on differential changes only).
  2. **Dependencies (SCA):** Tools like Snyk tracking `package.json` vulnerabilities, halting builds only for High/Critical CVEs.
  3. **Container Scanning:** Tools like Trivy scanning the built Docker image locally on the CI runner, rejecting pushes to the centralized registry if severe OS vulnerabilities exist.
- **Mitigation for Speed:** I mandate incremental scanning, caching layers rigorously, and tuning security rules to fail explicitly ONLY on critical zero-days, offloading "Low/Info" warnings to asynchronous Jira ticketing rather than failing the 2000-developer pipeline.

##### Q. How do you ensure fast and safe rollback in your CI/CD deployments when a release causes issues?
**Answer:**
I design pipelines where rollbacks do not require rebuilding the application logic. 
- **Artifact Immutability:** Code is compiled only once into an immutable image digest. 
- **Infrastructure (Terraform):** Using Terraform state to simply run `terraform apply` targeting the previous commit hash to revert network/infrastructure configs.
- **Applications (Kubernetes):** Adhering to GitOps patterns. If version `v2.0.0` crashes in production, a developer performs a `git revert` on the repository manifest back to `v1.9.0`. ArgoCD instantly synchronizes the cluster, pulling the previously cached healthy `v1.9.0` image with zero compilation delay, achieving a rollback in seconds.

##### Q. How do you maintain auditability and compliance across your CI/CD pipelines, especially in enterprise or financial environments?
**Answer:**
Financial (Banking) pipelines must trace exactly who deployed what, when, and how.
1. **Pipeline-as-Code:** 100% of CI/CD logic is written in declarative YAML/Jenkinsfiles stored in Git, capturing who modified the pipeline itself via commit history.
2. **SBOMs:** Mandating the automated generation of a Software Bill of Materials (SBOM) alongside every single Docker build, generating cryptographic assertions of exactly which 3rd-party libraries are embedded.
3. **Artifact Signatures:** CI agents sign artifacts and log exactly which Git Commit produced which SHA digest.
4. **RBAC & Logging:** Segregation of duties mandates developers *cannot* deploy to production. CI/CD systems assume scoped IAM identities. Execution logs and deployment events are streamed asynchronously to immutable, append-only centralized SIEMs (like Splunk or Azure Log Analytics) for 7-year auditor retention.


### Advanced CI/CD & Pipeline Architecture

##### Q. How would you design a scalable, highly available CI/CD system for microservices across multiple teams?
**Answer:**
1. **Pipeline Architecture:** I'd use a decentralized "Pipeline as Code" model stored directly alongside the microservice code in version control. A centralized GitHub Actions/GitLab CI/Azure DevOps system provides the orchestration. 
2. **Templates:** Provide secure, centrally managed YAML templates defining standardized build, scan, and deploy steps. Teams inherit from these templates to prevent diverging configurations.
3. **Execution Layer (Agents):** Run self-hosted CI runners scaled automatically using KEDA (Kubernetes Event-driven Autoscaling) on an EKS/AKS cluster. When hundreds of teams commit code concurrently, KEDA spins up ephemeral runner pods, executing the builds and destroying them immediately after, guaranteeing high availability and absolute scale.
4. **CD/GitOps:** Decouple continuous integration from deployment. The CI pipeline produces a signed Docker image, triggering ArgoCD/Flux to pull the new digest into the Kubernetes clusters seamlessly.

##### Q. How do you design an end-to-end DevSecOps pipeline for a fintech application with strict compliance requirements (e.g., PCI-DSS)?
**Answer:**
1. **Pre-commit:** Git hooks (e.g., `trufflehog`) check for hardcoded secrets before they ever hit the centralized repo.
2. **Code Integration:** Trigger SAST (e.g., Checkmarx, SonarQube) examining the application logic, and SCA (e.g., Snyk) verifying third-party library vulnerabilities in `package.json` or `pom.xml`.
3. **Build:** Pack the artifact into a minimal scratch Docker image. Scan it with Trivy/Anchore.
4. **Attestation/Provenance:** Generate a signed Software Bill of Materials (SBOM), and cryptographically sign the image using Cosign. This proves exactly which CI agent built the image, satisfying PCI-DSS immutability and audit requirements.
5. **Deployment Gate:** Use OPA Gatekeeper inside Kubernetes to intercept the deploy request. It verifies the cryptographic signature; if unsigned, the deployment is hard-blocked.

##### Q. What are some best practices for managing pipeline as code in large, distributed teams?
**Answer:**
- **DRY (Don't Repeat Yourself):** Abstract shared logic into centralized Modules/Templates (e.g., Jenkins Shared Libraries or Azure DevOps Templates). Do not allow 50 teams to copy-paste the same Maven build steps.
- **Versioning:** Templates must be versioned. If the DevOps team updates a centralized Docker build template, it should not break all 50 downstream pipelines simultaneously. Teams should selectively bump their template references (e.g., `template@v2.0`).
- **Security Scanners:** Enforce pipeline step composition where security scanning steps are mandatory and inextricably linked to the delivery steps.

##### Q. How would you dynamically provision ephemeral environments (dev/test) using pipelines?
**Answer:**
1. **Trigger:** A developer opens a Pull Request.
2. **Namespace Provisioning:** The pipeline runs a targeted `helm upgrade --install` setting a dynamic string like `namespace: pr-123`. We optionally use `vcluster` (Virtual Cluster) to instantiate a completely isolated control plane instantly.
3. **Routing:** Subdomain routing is mapped dynamically (e.g., `pr-123.dev.example.com`) overriding the Ingress.
4. **Teardown:** On PR Merge or Close, a GitHub Actions webhook automatically calls `helm uninstall pr-123` or destroys the vcluster, instantly terminating the ephemeral compute footprint.

##### Q. In a monorepo setup, how do you ensure that only relevant services are built and deployed in a CI/CD pipeline?
**Answer:**
1. **Path Filtering (Triggers):** CI tools support triggering based on directory paths. (e.g., `paths: - src/payment-service/**`). This natively isolates executions.
2. **Differential Tools:** Use specialized monorepo build tools like **Bazel**, **Nx**, or **Turborepo**. They calculate the directed acyclic graph (DAG) of dependencies. If you modify a shared `logging` library, the tool calculates exactly which microservices depend on it and mathematically only compiles and tests those affected targets, slashing build times from hours to seconds.

##### Q. How do you implement a canary deployment strategy with real-time monitoring rollback in a CI/CD system?
**Answer:**
I would utilize a Progressive Delivery controller like **Flagger**. 
1. Flagger creates the underlying routing objects (Istio VirtualServices or NGINX Ingress annotations), starting by routing 5% of traffic to the new version.
2. It polls a tightly integrated Prometheus server checking specific PromQL metrics (e.g., HTTP 2xx rates and Latency).
3. If the metrics remain within the SLA threshold for 2 minutes, the pipeline progresses to 10%, 25%, etc.
4. If the error rate breaches 1%, Flagger automatically aborts the pipeline, routing 100% of traffic back to the stable primary replica instantly without human intervention.

##### Q. How do you set up workload identity federation between GitHub Actions and Google Cloud / Azure securely?
**Answer:**
Exporting long-lived service account keys or Azure Client Secrets into GitHub Actions introduces critical credential leakage risks.
Instead, use **OIDC (OpenID Connect) Federation**.
1. Configure an Identity Provider inside Azure AD / GCP IAM pointing to GitHub's OIDC issuer URL.
2. Define trust conditions specifying exactly which repository and branch (e.g., `repo:my-org/my-app:ref:refs/heads/main`) is permitted to authenticate.
3. In the GitHub Actions YAML, the job requests a short-lived OIDC token. AWS/Azure validates this token cryptographically against GitHub's public keys, verifying the repository. If valid, Azure issues an ephemeral access token for 1 hour to complete the Terraform apply.

##### Q. How do you ensure cost-efficient auto-scaling of infrastructure in cloud when managing high workloads in CI/CD?
**Answer:**
1. **Ephemeral Spot Instances:** Run all CI/CD builder agents (Jenkins Workers, GitLab Runners) exclusively on AWS Spot Instances or Azure Spot VMs. CI workloads are intrinsically stateless and fault-tolerant. This yields up to an 80% discount. 
2. **Scale to Zero:** Use KEDA inside Kubernetes or custom Auto-Scaling Groups to monitor the Webhook Queue length. If the queue is 0, the node pool actively shrinks back to 0 instances. It scales out massively only during the exact moments a PR surge happens.

##### Q. How do you enforce compliance and auditability in your CI/CD processes across global regions (e.g., GDPR, HIPAA)?
**Answer:**
1. **Data Sovereignty:** Ensure deployment pipelines targeting the EU rigorously point to EU-specific container registries and cloud namespaces. Enforce this via OPA Gatekeeper rejecting cross-region deployments.
2. **Immutable Audit Trails:** Send all pipeline execution logs, git commits, and deployment approvals into an immutable, append-only SIEM (Security Information and Event Management) system physically located in the mandated region.
3. **Separation of Duties:** Enforce strict Branch Policies. A developer can write code, but a completely different compliance officer/architect role must approve the PR. The CI/CD pipeline enforces the deployment programmatically using scoped roles; human users lack production CLI access altogether.
