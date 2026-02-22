# GIT

# Download git

### Linux:

yum install git

### install git in ubuntu machine

sudo apt-get update
sudo apt-get -y -qq install git

### window:

download git bash tool from Internet
https://notepad-plus-plus.org/downloads/v7.8.6/

### To intialize git repository if not clone any repository yet

```
git initlongpath with git clone 
```

### longpath enable with git clone

```
git clone --progress -c core.longpaths=true ${GIT_URL}
```

### To clone code from repository with master branch

```
git clone <repo-url>
```

### To clone code from repository with specific branch

```
git clone <repo-url> -b <branch>
```

### to add files in stage area local system

```
git add .
```

### to check files in staging area in local system

```
git status
```

### commit the all files to git repo-url

```
git commit -m "message commit"
```

### push the code in remote repository

```
git push
```

### remove files from stage area

```
git reset HEAD -- .
```

### git stash

To save changes made when they're not in a state to commit them to a
repository

```
Use of git stash:-
* touch stash.py ( Creating a new file)
* gedit stash.py (make some changes)
* git add . ( Adding to the staging area)
* git status ( It will show new file in the staging area)
-- It is not looking good, so i can put all the uncommited changes to stash.
* git stash -u
* git status
-- It converted my dirty directory to clean one with the help if git stash.
* git stash list
* git stash show (If we want to inspect)
```

### git log

This helps give context and history for a repository

```
Use of git log:-
- create a new repository
* mkdir git-log (name of my directory)
* cd git-log/ (go into the directory)
* git init (to initilize it)
* gedit krishna1.py
* git add . (add in staging area)
* git commit -m "log" (finally commit it)
* git log ( It shows the commit history for the repository)
* git log -before="give Date here" (It provide parameter here as well)
* git log --author="name of author" (show commit based on the author)
* git log --before="date" ( It give according to date as well)
```

### git rebase

Takes a set of commits, copies them and store them outside the
repository

```
Use of rebase:-
rebase is the way of combine the work between the branches
-- What rebase does:
1. Take set of commits
2. copy them
3. store them outside our repository
Advantage of rebase is that- It can be used to make linear sequence of commit.
* git rebase master( It show current master up to date)
-- move our work from current branch to master branch
-- They look like they developed sequentially, but they developed parallely.
```

### git revert

It helps you to roll back to the previous version of file

```
Use of git revert:-
- How to revert to the previous commit
1. make some changes in file again
* gedit krishna1.py
2. Add to the staging area
* git add .
3. commit it
* git commit -m "last commit"
* git log --oneline(It show in one line)
4. GO back to the previous commit
* git revert 7af537f( last commit)
* cat krishna1.py
-- Now i go ahead and revert to the last commit as well
* git revert HEAD
* ls
* cat krishna1.py
-- whatever file changes that have been done after git revert will be reflected
commit itself.
```

### To see all branches

```
git branch
```

### merge and find conflict

https://www.simplilearn.com/tutorials/git-tutorial/merge-conflicts-in-git

```
git checkout <source_brach>
git merge <destination_branch>
git mergetool (GUI interface for check conflict in flies)
```

### Empty git repository

> #clone any branch and switch to new branch with --orphan
> 
> #An orphan branch is a separate branch that starts with a different root commit. 
> 
> #So the first commit in this branch will be the root of this branch without having any history.
> 
> #It can be accomplished by using the Git checkout command with the ––orphan option.
> 
> git checkout --orphan poc-test
> 
> #remove the cached git repository data
> 
> git rm --cached -r .
> 
> #git commit the empty branch
> 
> git commit -m "Empty branch" --allow-empty
> 
> #push the branch to git
> 
> git push origin pos-test

### check logged in git user with git configuration

```
git config --list
```

### set global git credentials

```
git config --global user.name "1820387"
git config --global user.password "Example@34"
git config --global user.email "1820387@tcs.com"
git config --global http.sslVerify true
```

### Git Large File storage(lfs) use

```
git clone "repoUrl"

git lfs install

git lfs track *.exe(large file format)

git lfs push --all origin push

git add .

git commit -m "upload large files"

git push -u origin push
```

### Git Branching Strategy

![Example Git Branching Diagram](https://user-images.githubusercontent.com/1256329/117236177-33599100-adf6-11eb-967c-5ef7898b55dc.png)

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
