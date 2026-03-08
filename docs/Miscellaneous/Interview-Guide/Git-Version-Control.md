## Git & Version Control

### Source Control & Collaboration

##### Q. Difference between rebase and merge?

**Merge:**
- Combines histories of two branches
- Creates merge commit with two parents
- Preserves complete history
- Can lead to cluttered history
- **Use when:** Preserving exact history, collaborative environment

**Rebase:**
- Reapplies commits from one branch onto another
- Creates linear history
- Rewrites commit history
- **Use when:** Clean linear history desired, working on local branches

##### Q. Resolve complex merge conflicts across multiple files?

1. **Understand the Conflict:**
   - Review conflicted files
   - Assess context from commits

2. **Communicate with Team:**
   - Discuss with team members
   - Coordinate resolution efforts

3. **Manual Conflict Resolution:**
   - Edit files to resolve conflicts
   - Remove conflict markers
   - Test changes

4. **Use Merge Tool:**
   - Tools like KDiff3, Beyond Compare, VS Code
   - `git mergetool` command

##### Q. Git "Detached HEAD" state?

Occurs when checking out a commit directly instead of a branch.

**Recovery:**
1. **Create new branch:** `git checkout -b my-new-branch`
2. **Stash changes:** `git stash` then switch branch
3. **Checkout branch:** `git checkout main`
4. **Discard changes:** Switch to branch (discards changes)

##### Q. What are Git submodules?
Embedded Git repositories within parent repository. Used for:
- Third-party libraries
- Shared code across projects
- Modular projects

**Commands:**
```bash
# Add submodule
git submodule add <repository-url> [path]

# Clone with submodules
git clone <repository-url>
git submodule update --init --recursive

# Update submodules
git submodule update --remote

# Remove submodule
git submodule deinit <submodule-path>
rm -rf <submodule-path>
git rm --cached <submodule-path>
```

##### Q. Handle large binary files in Git?

**Git Large File Storage (LFS):**
```bash
git lfs install
git lfs track "*.psd"
git add .gitattributes
git add path/to/largefile
git commit -m "Add large file with LFS"
```

**Alternatives:**
- Git-Annex
- External Storage (cloud/file hosting)
- Submodules/Subtrees
- Archiving for static files

##### Q. Git internal storage mechanism impact on performance?

**Objects:**
- Blobs: Store file content
- Trees: Represent directory structures
- Commits: Snapshots with metadata

**Performance factors:**
- Repository size
- Disk I/O and memory usage
- Indexing and caching
- Repository history complexity

**Optimization strategies:**
- Use Git LFS for large files
- Regular maintenance (git gc, git repack)
- Optimize history (rebase vs merge)
- Split large repositories

##### Q. Using git reflog for recovery?

**Scenario:** Accidentally dropped commit during rebase

**Steps:**
```bash
# View reflog
git reflog

# Find commit hash
# Create new branch from it
git checkout -b recovered-branch <commit-hash>

# Or reset current branch
git reset --hard <commit-hash>
```

Reflog tracks all HEAD changes, allowing recovery of lost commits.

##### Q. Git bisect to find bug-introducing commit?

**Steps:**
```bash
# Start bisect
git bisect start

# Mark current (bad) commit
git bisect bad

# Mark known good commit
git bisect good <good-commit>

# Git checks out middle commit
# Test and mark
git bisect bad  # or
git bisect good

# Repeat until culprit found

# End bisect
git bisect reset
```

Binary search through commits to identify bug introduction.

##### Q. Difference between git reset variations?

```bash
# Keep work, remove from staging
git reset --soft HEAD~1

# Destroy work
git reset --hard HEAD~1

# Remove file from staging
git reset
```

##### Q. Git branching strategies?
**Gitflow:**
```
Main ← Hotfix ← Release ← Development ← Features
```

**Flow:**
1. Develop branch from main
2. Feature branches from develop
3. Release branch from develop
4. Merge release to develop and main
5. Hotfix from main, merge to develop and main

##### Q. Cherry-pick commit across branches?
```bash
# Clone repository
git clone "https://github.com/user/repo.git" -b master

# Check commit ID
git log

# Switch to target branch
git checkout release-1.0.0

# Cherry-pick commit
git cherry-pick <commit-id>

# Add, commit, push
git add .
git commit -m "message"
git push
```

---

