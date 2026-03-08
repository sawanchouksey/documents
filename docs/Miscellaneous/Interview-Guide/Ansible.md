## Ansible

### Configuration Management & Automation

##### Q. How would you ensure that a specific package is installed on multiple servers?
You can use the package module in a playbook to ensure that a specific package is installed across multiple servers.

##### Q. How do you handle different environments (development, testing, production) with Ansible?
You can manage different environments by using inventory files and group variables. Create separate inventory files for each environment and use group variables to specify environment-specific configurations. Each hosts file would define the servers for that specific environment, and you can create a group_vars directory for each environment.

##### Q. How would you restart a service after updating a configuration file?
You can use the notify feature in Ansible to restart a service after a configuration file is updated.

##### Q. How can you ensure idempotency in your Ansible playbook?
Ansible modules are designed to be idempotent, meaning they can be run multiple times without changing the result beyond the initial application. For instance, if you use the file module to create a file, Ansible will check if the file already exists before trying to create it.

##### Q. How do you handle secrets or sensitive data in Ansible?
You can handle sensitive data using Ansible Vault, which allows you to encrypt files or variables.

##### Q. Can you explain how you would deploy an application using Ansible?
**Define Inventory:** Create an inventory file with the target hosts.
**Create a Playbook:** Write a playbook that includes tasks for pulling the application code from a repository, installing dependencies, configuring files, and starting services.

##### Q. How would you handle task failures and retries in Ansible?
You can use the retry and when directives to handle task failures in Ansible. The retries and delay parameters can be specified for tasks that might need to be retried.

##### Q. How would you roll back a deployment if the new version fails?
To roll back a deployment, you can maintain a previous version of the application and use a playbook that checks the health of the new version before deciding to switch back.

##### Q. How can you manage firewall rules across multiple servers using Ansible?
You can use the firewalld or iptables modules to manage firewall rules.

##### Q. How do you implement a continuous deployment pipeline using Ansible?
To implement a continuous deployment pipeline, you can integrate Ansible with a CI/CD tool like Jenkins, GitLab CI, or GitHub Actions.

##### Q. How can you check if a file exists and create it if it doesn't?
You can use the stat module to check if a file exists and then use the copy or template module to create it if it doesn't.

##### Q. How can you execute a command on remote hosts and capture its output?
You can use the command or shell module to run commands on remote hosts and register the output.

##### Q. What is Ansible ad-hoc command?
Command used in Ansible without playbook is called ad-hoc command.

---



### Core Architecture and Configuration

##### Q. What is Ansible, and what is its purpose?
Ansible is an open-source IT automation, configuration management, and application deployment tool. Its core purpose is to automate repetitive setup tasks across hundreds of servers simultaneously—such as installing software, updating configuration files, and starting services. Unlike Chef or Puppet, it relies entirely on SSH and requires **no agents** installed on target nodes.

##### Q. What language do you use in Ansible?
Ansible playbooks, task files, roles, and variables are written in **YAML** (YAML Ain't Markup Language), making automation highly readable for non-programmers. However, the core execution engine and the internal modules powering Ansible are built entirely upon **Python**.
