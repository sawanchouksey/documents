# ♾️ DevOps CI/CD Project with Jenkins, Ansible and Kubernetes(AKS) ♾️

![diagram](https://sawanchouksey.github.io/documents/blob/main/docs/DevOps/img.png?raw=true)

### ✍Create new Ubuntu Virtual Machine and install Jenkins in it.

## ✍ Create new Ubuntu Virtual Machine and install Ansible in it.

## ✍ Create new user ansibleadmin and generate SSH key for it.

## ✍ On Jenkins dashboard install new plugin "Publish over SSH" and integrate Ansible with Jenkins.

## ✍ Install Docker on Ansible server and provide full rights to ansibleadmin on Docker.

## ✍ Create ansible host group in file /etc/ansible/host.

## ✍ Add self ssh key(ssh-copy-id localhost) so that Ansible playbook can connect to local host.

## ✍ Create Ansible playbook to create Docker image and push that Image to Docker-Hub.

## ✍ Create Jenkins job(CI_Job) to run the Ansible playbook.

## ✍ Create new Ubuntu Virtual Machine(Kube-Server) and install Azure CLI in it.

## ✍ Create AKS cluster on Azure Portal, login through Azure CLI and install aks cli.

## ✍ Create Deployment and Service Manifest files.

## ✍ Create group called kubernetes in /etc/ansible/hosts file.

## ✍ On Kube-Server enable password based authentication for "root" and set password for root.

## ✍ Copy ssh key of ansibleadmin of Ansible server to root user of Kube-Server so that playbook can interact with kubernetes as we have connected kubernetes via root user of Kube-Server.

## ✍ Create Ansible playbook to run Deployment and Service Manifest files.

## ✍ Create Jenkins deployment job(CD_Job) for Kubernetes.

## ✍ Modify CI_Job to trigger CD_Job after completion. Set build trigger in CI_Job using PollSCM.

## ✅ Verify the CI/CD by making change on GitHub Repo and confirm the changes on Application.

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
