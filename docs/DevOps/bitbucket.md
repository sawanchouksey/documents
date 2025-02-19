# Bitbucket (SAAS)

- It is a web-based version control repository hosting service, primarily used for source code and development project that use Git and Mercurial revision control system.
- It offers tools for managing and collabarating on code, including features such as pull request, code review and issue tracking.
- It is owned by Atlassian and integrating with other atlassian product such as Jira, Confluence and Bamboo.
- It is also offers integration with other popular development tools and service, making it a popular choice for teams and organization working on software project.

### Bitbucket URL structure

https://bitbucket.org/workspaceID/projectName/src/branchName

### create BitBucket account and login

### Create Workspace

- Top most hierachy level in Bitbucket which isolate each other.
- login
- go to profile section
- select all workspace 
- create workspace for current project

### Create project and repository

- go to profile section
- select all workspace 
- select specific workspace
- select Repositories
- create repository [workspace | Project Name | Repository Name | Access level | Default Branch Name | Create Repository]

### Items contain in Workspace section

- Items conatain in workspace | Repositories | Projects | Snippets | Members | Settings

### Item conatain in project section

- Items contain in repository |Source|Commits|Branches|PullRequest|Pipelines|JiraIssues|Security|Downloads|Repository settings

### clone repository

- Go to Repository 
- go to Clone section
- copy the url for cloning repository
  git clone https://Sawan_Chouksey@bitbucket.org/workspaceID/projectName.git

### Code update on remote repository from local

```
git status
git add fileName.txt
git commit -m "New File Commit"
git push origin naster (Origin - Same repository as intial clone repository i.e. bitbucket url, master - branch)
```

### Check commit History

- go to repository
- left side pane click on 'Commits' section

### Delete files from staging directory

```
git clean -f
```

### Check all commits in repository

```
git log
```

### Give user access to workspace

- Create user account 
- login bitbucket account
- go to profile section
- select workspace you want to give access
- go to 'settings'
- select 'user group'
- create group [ Group name | checkbox : Can admin for all workspace Repositories,Can create repository in the workspace | Automatically assign permission for new repositries : select None,Read,Write,Admin | Confirm ]
- Add members [ Enter email Address | Select group to which these users will added | Confirm ]
- New members recieve approval email from Bitbucket for accept invitation for access.

### Give user access to repository

- login bitbucket account
- go to profile section
- select workspace
- select repository you want to give access
- select 'repository settings'
- select 'User and group access'
- add members [ emailAddressofUser | Access : Delete,Admin,Read,Write | confirm ]

### create password for Your account

- login bitbucket account
- go to profile section
- go to personal settings
- go to App password 
- Create App password [ labels(Any Name) | Permission : Account - Email,Read,Write|Issue - Read,Write|Workspace Membership - Read,Write|Wikis - read and Write|Snippets - Read,Write|Projects - Read,Write|Webhooks - Read,Write|Repositories - Read,Write,Admin,Delete|Pipelines - Read,Write,Edit Variables|Pull Request - Read,Write|Runner - Read,Write | create ]
- It will generate unique AlphaNumericPassword for your account i.e. gdshfgdjka5kGh6ghT

### check avaialble branch in repository (*) Green Color indicate current branch in output

```
git branch
```

### create branch with existing branch i.e. master

```
- git clone exiting repository with existing branch
git checkout -b NewBrancName/Anything
```

### add all files from working directory to staging directory

```
git add .
```

### revert all changes from staging directory to working directory

```
git reset
```

### commit revoke and bring back revert all changes from committed to staging directory

```
git reset --soft(content chnages will be there in staging but commit has been gone) HEAD~1(for top most or latest commit avaialble in 'git log', 1 for one commit, 2 for two commits from head)
git reset --hard(content chnages will be lost permanently from all files even from all stages with commits) HEAD
```

### complete history in local working directory

```
git reflog
```

### delete commit with has id

```
git reset --hard hashCommitId
```

### forcefully push the chnages

```
git push origin master -f
```

### pull request

- It is request to merge your code to one branch to another
- It is avaialble in repository level only
- go to repository
- click on left side pane 'pull request'
- create pull request [(select which Branch need to merge)feature/profile-->master(select in which branch it will be merge)|Title|Description|Attachments|Reviewer|checkbox : Delete feature/profile after the pull request is merged|create pull request] 
- In the bottom 'diff' & 'commits' tells about the changes and difference in both branch

### Approve pull request and merge

- go to repository
- click on pull request
- click and open specific pull request
- On the top two option avaialble request changes, approve
  reques chnages(-) : if you are not satisfied with the changes revert back the author for fix it with feedback.
  Approve: Simply approve the pull request
- review each code and give comment on chnages section in Code with (+) icon.
- update code and update comment with "Addressed" on the feedback comment So Reviewer easily get details about new code on specific comment. Because it difficult to review whole code again.
- after commiting new chnages by author pull request update with new commits with address review changes.
- approve the request.

### merge code into branch

- after pull request approved 
- go to repository.
- click on pull request.
- open specific pull request which approved. 
- click 'merge' option in pull request on top for merge into specific branch.
- merge [ Source Branch | destination Branch | Commit message after approval | Merge Stretegy | checkbox : close source branch | merge]
- Types of Merge Stretegy
  1. **Merge Commit(git merge --no-ff master)** Create new commit for merge with all changes.
  
  2. **Fast Forward(git merge --ff-only master)**
  
  3. **Squash(git merge --squash)**

### How to resolve conflict while merging

```
- When it conflict it will reflect in file with special character notation by git in code we need to fix it and commit the code.
<<<<<<< Head
=======
	number c = 10;
>>>>>>>	
- remove the Head branch it will solve
	number c = 10;
```

### Rebase

- It is a process of moving or combining sequence of commit to new base commit
- It hels us to maintaining linear project history
- ```
  git checkout master
  git pull
  git checkout branch
  git rebase master
  ```

### squash

- come with all commit pickup and squash or combine them in one commit.
  **git rebase -i HEAD~2(only lastest 2 commit will pick)**
- It will open interactive editor with pick 2 commit on top.
- enter into insert mode by enter 'i' key 
  - pick commit1 step 1 changes branch
  
  - pick commit2 step2 changes branch
- now we need to squash commit2 into commit1 therefore changes as below mentioned
  - pick commit1 step 1 changes branch
  
  - squash commit2 step2 changes branch
- save the changes by enter ':wq' key 
- Now we will receive 1 commit which combination of 2 commit

### edit commit or add to last commit from staging directory

```
git commit --amend -m "replace commit message"
```

### show the changes available in commit

```
git show
```

### move a commit from one branch to another branch

```
git cherry-pick "commitId"
```

### Identify which commit caused the issue in many commits?

```
git bisect bad  'commitId'            ### move to bad commit not working 
git bisect good 'commitId'            ### confirm it is good commit where it is last worked
git bisect reset                      ### come back to original branch
```

### save local changes and dont commit it and save from lost i.e. git store it in memory storage in invisible form

```
git stash
```

### get back invisible chnages into working directory

```
git stash pop 
```

### what changes you did how to find out the changes made by you from original file

```
git diff
```

### how to know how many people working on specific file or code and get details of those people

```
git blame fileName
```

### revert the git commit with save history

```
git revert commitId
```

### create branch in repository in bitbucket

- go to repository
- on left side select branches
- create branch [ Type - BugFix,Feature,Hotfix,Release,Other|from branch|Branch Name|Create]

### Pipeline in bitbucket

- To test and check whetever code is commit It must be successfully compiled and automatic build trigger
- To use pipeline in BitBucket we need to enable 'Two-Step Varification'
- To setup 'ssh' for enable 'Two-Step Varification' inside personal settings
- Genrate ssh keys for your local system
- click on Manage SSH keys
- Add key [ label| Paste your public key|add key] 

### create bitbucket pipeline

- Go to repository

- Go to pipelines

- Whether you select pipeline template with respect to code base like python,java etc.

- create pipeline

- Repository/bitbucket-pipelines.yml
  
  ```
  image: maven:3.6.3
  
  pipelines:
  	default:
  	  - parallel:
  		- step:
  			name: build and test
  			caches:
  			  - maven
  			script:
  			  - mvn -B verify --file pom.xml
  			after-script:
  			 - pipe: atlassian/checkstyle-report:0.2.0  ### pipe - used for integration
          - step:
  			name: Security Scan
  			script:
  			  - pipe: atlassian/git-secret-scan:0.4.3
  ```

- commit file in repository parent directory where pom.xml exist

- BitBucket pipeline use docker in backend for tools and other integration

### create deployment pipeline for BitBucket

- Repository/bitbucket-pipelines.yml
  
  ```
  pipelines:
    default:
      - step:
          name: Build and push to S3
          script:
            - apt-get update
            - apt-get install -y python-dev
            - curl -O https://bootstrap.pypa.io/get-pip.py
            - python get-pip.py
            - pip install awscli
            - aws deploy push --application-name $APPLICATION_NAME --s3-location s3://$S3_BUCKET/test_app_$BITBUCKET_BUILD_NUMBER --ignore-hidden-files
      - step:
          name: Deploy to testing
          image: amazon/aws-cli:latest
          deployment: testbed ###  Test environment
          script:
            - python deploy.py test
      - step:
          name: Deploy to staging
          image: amazon/aws-cli:latest
          deployment: staging2 ###  Staging environment
          trigger: manual
          script:
            - python deploy.py staging
      - step:
          name: Deploy to QA staging
          image: amazon/aws-cli:latest
          deployment: staging1 ###  Staging environment
          trigger: manual
          script:
            - python deploy.py staging
      - step:
          name: Deploy to production
          image: amazon/aws-cli:latest
          deployment: production-east ###  Production environment
          trigger: manual
          script:
            - python deploy.py prod
  ```

### disable auto-trigger in pipeline

```
pipelines:
  custom: ###  Pipelines that can only be triggered manually
    sonar:
      - step:
          script:
            - echo "Manual triggers for Sonar are awesome!"
```

### Set up your credentials

- Create a service principal
  
  ```
  az ad sp create-for-rbac --name <name for your principal>
  ```

- add variables in Bitbucket (in repository > Settings > Repository variables.
  **appId → AZURE_APP_ID
  password → AZURE_PASSWORD
  tenant → AZURE_TENANT_I**

### git tagging

- It is used to mark important checkpoints in the repositries.
  
  ```
  create : git tag -a <tag Name> -m <message> 
  verify : git tag
  push   : git push --tags
  ```

### git clone vs git fork?

A fork creates a completely independent copy of Git repository. In contrast to a fork, a Git clone creates a linked copy that will continue to synchronize with the target repository.

![alt text](https://github.com/sawanchouksey/documents/blob/main/docs/DevOps/clonevsfork.png?raw=true)

### git fetch vs git pull?

![alt text](https://github.com/sawanchouksey/documents/blob/main/docs/DevOps/fetchpull.png?raw=true)

### sourceTree

- It is GUI interface for bitbucket operation perform related to git cli.

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
