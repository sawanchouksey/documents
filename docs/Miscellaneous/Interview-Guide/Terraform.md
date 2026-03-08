## Terraform

### Infrastructure as Code

##### Q. What is Terraform?
Terraform is an infrastructure as code tool that lets you define cloud and on-premises resources in configuration files.

##### Q. Differentiate between Terraform and CloudFormation?

**Declarative vs. Imperative:**
- **Terraform:** Declarative (specify desired state)
- **CloudFormation:** Imperative (specify sequence of steps)

**Configuration Language:**
- **Terraform:** HCL (HashiCorp Configuration Language)
- **CloudFormation:** JSON or YAML

**State Management:**
- **Terraform:** Uses state file (terraform.tfstate)
- **CloudFormation:** Manages state internally

##### Q. How to prevent "Duplicate Resource" error?

1. Use unique resource names
2. Utilize variables for reusability
3. Leverage data sources for existing resources
4. Review dependencies with `depends_on`
5. Check for resource existence before creation
6. Review state files
7. Run `terraform plan` before applying

##### Q. Are callbacks possible with Terraform on Azure?
Yes, using:
- Azure Functions or Logic Apps
- Azure Event Grid for event handling

##### Q. What is tainted resource?
A resource marked for recreation during next apply due to configuration changes that can't be applied in place.
```bash
terraform taint resource_type.resource_name
```

##### Q. What is Remote Backend?
Central location for storing Terraform state file enabling:
- Team collaboration
- State locking
- Consistent state across users

**Types:**
- Amazon S3
- Azure Storage
- Google Cloud Storage
- HashiCorp Consul
- HTTP

##### Q. What is Terragrunt?
Thin wrapper for Terraform providing:
- DRY configurations
- Remote state management
- Encrypted variables
- Workspace/environment management
- Dependency management
- Dynamic configuration
- Concurrent operations

##### Q. What is state file locking?
Prevents concurrent access/modifications to state file. Two types:
- **File-Based:** Uses lock file
- **Backend-Based:** Managed by backend (S3+DynamoDB, etc.)

##### Q. Making module objects available across modules?

1. Define output variables in source module
2. Reference outputs in parent module using `module.source_module.output_name`
3. Run terraform init/apply
4. Handle dependencies correctly

##### Q. What are provisioners?
Built-in configurations for running scripts during resource creation/destruction:

1. **Local-Exec:** Run commands on Terraform machine
2. **Remote-Exec:** Run commands on remote resource
3. **File:** Copy files to remote resource
4. **Connection:** Define SSH/WinRM connections
5. **Chef/Puppet:** Configuration management integration

##### Q. Terraform request flow architecture?

1. Configuration Files (HCL)
2. Terraform CLI commands
3. Provider Plugins
4. Provider Configurations
5. Initialization (terraform init)
6. Resource Graph building
7. Plan Generation (terraform plan)
8. Execution (terraform apply)
9. State Management
10. Concurrency/Parallelism
11. Output and Feedback
12. Post-Apply Tasks

##### Q. Terraform lifecycle arguments?

**Prevent resource deletion:**
```hcl
lifecycle {
  prevent_destroy = true
}
```

**Create before destroy:**
```hcl
lifecycle {
  create_before_destroy = true
}
```

**Ignore changes:**
```hcl
lifecycle {
  ignore_changes = [tags]
}
```

**Custom condition checks:**
```hcl
lifecycle {
  precondition {
    condition = data.aws_ami.example.architecture == "x86_64"
    error_message = "AMI must be x86_64."
  }
}
```

##### Q. Import existing resources to Terraform?
```bash
# Import AWS instance
terraform import aws_instance.foo i-abcd1234

# Import into module
terraform import module.foo.aws_instance.bar i-abcd1234
```

##### Q. What is Terraform state file?
Stores information about infrastructure, tracking resources and mapping them to real-world resources.

##### Q. Where can Terraform state file be stored?
- Local machine (default: terraform.tfstate)
- Remote storage (Azure Storage Account, AWS S3)
- Terraform Cloud

##### Q. Delete and apply specific resource?
```bash
terraform destroy -target=resource_type.resource_name
terraform apply -target=resource_type.resource_name
```

##### Q. What is dynamic block?
Construct repeatable nested blocks dynamically:
```hcl
locals {
  ports = [22, 80, 8080, 8081]
}

dynamic "security_rule" {
  for_each = local.ports
  content {
    name = "Inbound-rule-${security_rule.key}"
    priority = sum([100, security_rule.key])
    source_port_range = security_rule.value
  }
}
```

##### Q. Authenticate Terraform with Azure?
Via Service Principal:
```hcl
provider "azurerm" {
  features {}
  subscription_id = "00000000-0000-0000-0000-000000000000"
  client_id = "00000000-0000-0000-0000-000000000000"
  client_certificate_path = var.client_certificate_path
  tenant_id = "00000000-0000-0000-0000-000000000000"
}
```

Or environment variables:
```bash
export ARM_CLIENT_ID="00000000-0000-0000-0000-000000000000"
export ARM_SUBSCRIPTION_ID="00000000-0000-0000-0000-000000000000"
export ARM_TENANT_ID="00000000-0000-0000-0000-000000000000"
```

### Intermediate/Advanced Terraform Scenarios

##### Q. What strategies do you use for managing Terraform state in a team? How do you handle state locking and backups in Azure?
- **Remote Backend:** Always use a remote backend (e.g., `azurerm` backend) rather than local state.
- **State Storage:** Use an Azure Storage Account container.
- **State Locking:** The `azurerm` backend intrinsically supports state locking via Azure Blob Storage leases. This prevents concurrent pipeline runs from corrupting the state.
- **Backups:** Enable soft delete, blob versioning, and point-in-time recovery on the Azure Storage Account holding the state file.

##### Q. Explain the differences between terraform plan, terraform refresh, and terraform apply. When should each be used?
- **terraform refresh:** Queries providers to update the local state file with the current real-world infrastructure configuration. *Note: As of newer versions, refresh is built into plan/apply.*
- **terraform plan:** Compares the desired state (code), the state file, and the real-world infrastructure, emitting an execution plan detailing what will be added, changed, or destroyed. Used in CI/CD for peer review prior to changes.
- **terraform apply:** Executes the actions proposed in the plan to reach the desired state. It writes the outcome to the state file upon completion.

##### Q. How do you modularize Terraform for large-scale projects? Give examples.
- Separate code into **modules** based on specific resource collections offering logical functions (e.g., a "vnet" module, an "aks_cluster" module).
- Maintain a **Module Registry** or a separate Git repo for modules. App teams call these modules from their root configurations specifying the source and a version tag.
- By providing constrained inputs (variables) and standardized outputs, organizations impose security compliance inside the module (e.g., always enforcing logging on a storage account) while giving devs an easy-to-consume interface.

##### Q. How do you detect and resolve drift in Terraform-managed resources?
- **Detect:** Run a scheduled CI pipeline nightly executing `terraform plan` with a `detailed-exitcode`. If drift occurs (someone manually changed AWS/Azure), the step returns an exit code of 2, alerting the team.
- **Resolve:** Ideally, revert the manual drift by running `terraform apply`, forcing the real-world environment back to the state dictated by code. If the manual change was correct, backport the change into the Terraform code, run plan to ensure 0 changes, and apply.

##### Q. Explain how to set up remote Terraform backends in Azure (Blob Storage) and enable state locking with Azure CosmosDB or similar.
- **Setup:** Create a Resource Group, a Storage Account, and a Blob Container using a separate script or pipeline (the bootstrapping phase). 
- **Backend Block:** Add a `backend "azurerm"` block inside the `terraform` block referencing the storage account name, container, and state key.
- **State Locking:** Azure Blob Storage natively handles state locking by automatically acquiring a lease on the Blob when an operation starts. CosmosDB or DynamoDB are typically needed for locking only when using the standard S3 backend in AWS, whereas Azure Blob handles both storage and locks out-of-the-box.

##### Q. Show a use-case for for_each vs count in a real Terraform deployment. When should dynamic blocks be preferred?
- **`count`:** Best for identical resources (e.g., generating 3 VMs: `count = 3`). But if the middle VM is removed, indexes shift, causing recreation of subsequent VMs.
- **`for_each`:** Best when mapping over a dictionary/set (e.g., creating subnets with different CIDRs). Removing an item uniquely destroys that specific resource without shifting others.
- **Dynamic Blocks:** Used to generate repeatable nested blocks *within* a resource (like multiple `ingress` rules inside an NSG or `setting` blocks inside an Azure App Service), rather than multiple top-level resources.

##### Q. Explain the purpose and real-world use of lifecycle blocks (prevent_destroy, create_before_destroy) in Terraform.
- **prevent_destroy:** Prevents Terraform from accidentally destroying a critical resource (e.g., a Production Database or Key Vault). Any plan attempting to destroy it will error out.
- **create_before_destroy:** By default, Terraform destroys a resource before recreating it. This block reverses the order, creating the replacement first. Crucial for zero-downtime deployments like rotating a VM Scale Set or updating an IP address.

---



### Advanced Terraform Scenarios

##### Q. Can you explain the Terraform plan and its purpose?
`terraform plan` compares the declarative HCL configuration files with the current saved state (`terraform.tfstate`) and real-world infrastructure. It generates an execution plan highlighting exactly what resources will be added (`+`), modified (`~`), or destroyed (`-`). The primary purpose is a "dry-run" validation to ensure the changes are accurate and safe before applying them to production.

##### Q. Why did you choose Terraform over Boto3 for infrastructure provisioning?
- **Declarative Approach:** With Terraform, you define the *desired end-state*, and it figures out how to achieve it, safely managing dependencies and lifecycle automatically.
- **Complexity:** Boto3 is procedural (imperative). To create infrastructure, you must write extensive custom logic to handle API pagination, wait states (waiting for an EC2 to boot before creating an ALB), and error handling.
- **State Management:** Terraform keeps an intrinsic state to detect drift and safely update resources, whereas Boto3 requires manual tracking. Terraform is purpose-built for IaC; Boto3 is better suited for operational scripts or Lambda workloads.

##### Q. Where do you run Terraform code, remotely or locally?
During active development, Terraform is executed **locally** using the CLI, but it is strictly configured to use a **Remote Backend** (e.g., AWS S3 with DynamoDB locking) so state is never local. For actual environment deployments (Staging/Prod), Terraform is strictly executed **remotely via CI/CD pipelines** (e.g., Jenkins or GitHub Actions) to enforce consistent environment variables, peer approvals, and centralized audit logging.

##### Q. What are Terraform modules, and have you used any in your project?
Terraform modules are logical, reusable containers for multiple integrated resources. **Yes**, we use them heavily to enforce DRY principles and security standards. For example, a custom `vpc-network` module standardizes the creation of a VPC, subnets, IGW, and NAT gateways. App teams just call `module "vpc"` referencing our private registry and passing specific CIDR variables, without needing to know the complexities underneath.

### Edge-Case & Scenario-Based Troubleshooting

##### Q. What happens if your state file gets corrupted during a multi-cloud deployment?
**Answer:** Terraform can’t reconcile resources across AWS, Azure, and GCP. Each provider shows different resource states, and you’re stuck with infrastructure that exists in some clouds but not in Terraform’s memory. *Fix:* You must manually inspect the real-world state and pull them back into a new state file using `terraform import`, or restore a previous uncorrupted state from the remote backend's version history (e.g., S3 versioning).

##### Q. What happens when your Terraform Cloud workspace runs out of credits mid-apply?
**Answer:** Your deployment stops immediately, leaving resources in various states of creation. Some EC2 instances are running, some security groups are half-configured, and your application is completely broken. *Fix:* Top up the credits, then run `terraform plan` and `terraform apply` again. Terraform's idempotent nature will resume the creation of the remaining unprovisioned resources and reconcile the partial state.

##### Q. What happens if your team uses AI-generated Terraform code that creates naming conflicts?
**Answer:** ChatGPT creates resource names that seem fine in isolation but clash with existing infrastructure. Your apply fails with cryptic AWS errors about duplicate names, and you’re debugging AI code at 2 AM. *Fix:* Utilizing `random_pet` or `random_string` resources as suffixes for globally unique resources (like S3 buckets), and strictly enforcing static code analysis (like Checkov/TFLint) in CI/CD before any AI-generated code is permitted to run.

##### Q. What happens when Kubernetes updates break your Terraform provider compatibility?
**Answer:** Your cluster updates to K8s 1.30, but your Terraform Kubernetes provider only supports up to 1.28. All your deployments start failing with “resource mapping not found” errors. *Fix:* You must explicitly pin provider versions inside the `terraform { required_providers {} }` block to strictly match your current cluster version, preventing automatic upgrades until you purposefully test the provider upgrade in a staging environment.

##### Q. What happens if your GitOps pipeline applies malicious Terraform changes from a compromised PR?
**Answer:** An attacker submits seemingly innocent changes that actually create backdoor access or expensive resources. Your automated pipeline applies them before security review, compromising your entire infrastructure. *Fix:* Enforce branch protection rules requiring multiple human approvals, integrate OPA (Open Policy Agent) or HashiCorp Sentinel to automatically block unauthorized resource types (e.g., `aws_iam_access_key`), and run Checkov to fail pipelines on security deviations.

##### Q. What happens when your Terraform state grows to 100MB+ with microservices architecture?
**Answer:** Every plan and apply takes 15+ minutes. Your CI/CD pipeline times out, developers wait forever for infrastructure changes, and productivity crashes. *Fix:* You must break the monolithic state file into smaller, decoupled logical components (e.g., network, database, application layers). Use `terraform_remote_state` data sources to pass outputs between these isolated mini-states.

##### Q. What happens if cloud provider regions go down during your Terraform deployment?
**Answer:** You’re deploying across multiple regions when us-east-1 has an outage. Half your resources are created, half aren’t, and Terraform can’t complete the apply because APIs are unreachable. *Fix:* You must wait for the region to recover. Since state changes are locked and saved gradually, Terraform knows what succeeded. Running `terraform apply` post-outage will resume the deployment of the remaining resources. 

##### Q. What happens when your organization hits cloud spending limits during a large deployment?
**Answer:** You’re provisioning 200 EC2 instances when AWS cuts off your account for exceeding budget alerts. Some instances are running, billing is frozen, and you can’t create or destroy anything. *Fix:* You must negotiate limit increases via AWS Support or pay outstanding bills. Once the account is unlocked, running `terraform plan` will reconcile the half-deployed state, and `terraform apply` or `terraform destroy` will resume normal operations.

##### Q. What happens if your remote state backend gets accidentally deleted by cloud retention policies?
**Answer:** Your S3 bucket had a 30-day lifecycle policy that someone forgot about. Three months later, your entire Terraform state is gone, and you have no record of what infrastructure exists. *Fix:* You must use `terraform import` to manually map every single existing cloud resource back into a fresh state file, block by block. To prevent this, state backend buckets must *always* have object versioning enabled, explicit `prevent_destroy` lifecycle blocks, and cross-region replication.

##### Q. What happens when Terraform provider rate limits conflict with your CI/CD frequency?
**Answer:** Your team pushes 50+ changes per day, but the AWS provider can only handle 20 API calls per minute. Deployments start queuing up, failing randomly, and creating inconsistent infrastructure states. *Fix:* Implement exponential backoff configurations or explicit retry limits in the provider block. Long-term, decouple the CI/CD pipelines to ensure less frequent, batched applies, or break monolithic workspaces into smaller states so less data is queried during the `terraform refresh` phase.

##### Q. How would you implement immutable infrastructure using containers and Infrastructure-as-Code tools like Terraform?
**Answer:**
Immutable infrastructure asserts that servers/components are never modified after deployment. If an update is required, the old component is destroyed and replaced via a brand-new component.
1. **Machine Images:** For VMs, I use **HashiCorp Packer** in CI pipelines to "bake" base AMIs completely loaded with OS patches and application logic. 
2. **Terraform (IaC):** My Terraform configuration maps exactly to the Auto Scaling Groups (ASG) or Virtual Machine Scale Sets (VMSS) utilizing this pre-baked AMI. I never use SSH/Ansible to tweak running servers. 
3. **Update Cycle:** When an app change happens, Packer bakes a new image `v2`. Terraform updates the Launch Template and applies the change using `instance_refresh` rolling update strategies, cleanly terminating old `v1` VMs and substituting them with the pure `v2` images cleanly. For containers, the image acts as the base immutability layer deployed via Kubernetes resources.


### Advanced Architectural & Enterprise Terraform

##### Q. How would you manage cross-region deployments using Terraform in a multi-cloud setup?
**Answer:**
1. **Multi-Provider Configurations:** You instantiate multiple provider blocks in your Terraform configuration with distinct `alias` definitions (e.g., `provider "aws" { alias = "us-east" region = "us-east-1" }` and `provider "aws" { alias = "us-west" region = "us-west-2" }`).
2. **Module Instantiation:** You call your deployment module twice, explicitly passing in the different `providers = { aws = aws.us-east }` variables.
3. **Workspace Isolation:** Alternatively, rather than a monolithic multi-region state, use Terraform Workspaces or separate state files (`prod-us-east`, `prod-us-west`) managed through a tool like **Terragrunt**, abstracting the repetitive provider boilerplate.

##### Q. How would you refactor a legacy Terraform codebase used by multiple teams to follow best practices like DRY and modularity?
**Answer:**
Refactoring active states is highly dangerous; it requires careful state manipulation.
1. **Identify Patterns:** Find repetitive blocks (e.g., standard VM + NSG + Disk deployments). Abstract this into a generalized, reusable `compute` module. 
2. **Refactor Code:** Publish the module to a private Git repository or Terraform Cloud registry. In the legacy codebase, delete the raw components and point to the `module "compute"`.
3. **Manipulate State:** To prevent Terraform from destroying the live VMs and recreating them via the module, run `terraform state mv` commands: `terraform state mv azurerm_virtual_machine.old module.compute.azurerm_virtual_machine.new`.
4. **Validation:** Run `terraform plan`. It should conclusively show `0 added, 0 changed, 0 destroyed`, proving the codebase is modernized while the real-world state remained purely intact.

##### Q. Explain the internals of how Terraform handles dependencies and graph building during the planning phase.
**Answer:**
Terraform essentially builds a **Directed Acyclic Graph (DAG)**. 
1. **Implicit Dependencies:** By analyzing the HCL interpolation syntax (e.g., a subnet block referencing `vpc_id = aws_vpc.main.id`), Terraform identifies that the VPC *must* be created before the subnet. It draws a directional vertex between these two nodes.
2. **Explicit Dependencies:** Developers use the `depends_on = [aws_iam_role.app]` array to force a strict ordering where interpolation doesn't exist natively.
3. **Concurrency:** Once the graph is mathematically built, Terraform walks the DAG from the leaves upward. If two branches (e.g., establishing two discrete VMs) have absolutely no intersecting lines, Terraform automatically executes their creation API calls simultaneously in parallel, dramatically speeding up provisioning.

##### Q. How do you manage and isolate Terraform state files across multiple environments and teams?
**Answer:**
Never use a monolithic state file for an entire enterprise. Destroying the dev environment could accidentally corrupt the isolated prod state if not strictly separated.
1. **Logical Separation (Directories):** Use separate directories mapped to strict, independent backend states (`environments/dev`, `environments/prod`).
2. **Terragrunt / Workspaces:** Use Terragrunt to automatically configure remote backends based on the directory path, keeping the code completely DRY.
3. **RBAC Isolation:** The `dev` state file lives in a different S3 bucket or Storage Container than the `prod` state file. Developers are granted IAM IAM Read/Write access strictly to the `dev` state bucket, mathematically preventing them from executing `terraform apply` targeting production.

##### Q. What’s your strategy to prevent and recover from a corrupted or deleted remote backend state file?
**Answer:**
1. **Prevention:** Enforce strictly configured S3 buckets / Azure Storage Accounts with Object Versioning enabled, an explicit Cloud Provider `prevent_destroy` lock, and Cross-Region Replication backing up the bucket natively.
2. **Recovery (If Versioning is enabled):** Simply restore the previous uncorrupted blob version from the bucket directly within the Cloud Console.
3. **Recovery (Worst Case):** Run `terraform import`. I will manually go through the `.tf` definitions, finding the actual Resource IDs using the Azure Portal or AWS CLI, and individually `terraform import aws_vpc.main vpc-1234abc` block by block rebuilding the state mappings.

##### Q. Have you implemented policy-as-code (e.g., Sentinel, OPA) with Terraform? Give a real use case.
**Answer:**
Yes, I integrate **OPA (Open Policy Agent) utilizing Rego policies / Conftest** inside the CI/CD pipeline post-plan.
*Use Case:* Preventing unencrypted storage and controlling costs.
1. CI executes `terraform plan -out=tfplan` and outputs the JSON equivalent `terraform show -json tfplan`.
2. OPA parses the JSON mathematically evaluating the changeset against organizational policies. 
3. *Policy:* If `type == "azurerm_storage_account"` and `min_tls_version != "TLS1_2"`, or if `type == "aws_instance"` and `instance_type == "p3.16xlarge"`, the policy evaluation returns a violation.
4. The CI pipeline fails violently, explicitly blocking the `terraform apply` from physically manifesting the violation.
