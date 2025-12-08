# Github Action Notes

After installing Git, you can also configure it - most importantly, you can set a username and email address that will be connected to all your code snapshots.

This can be done via:

```
git config --global user.name "your-username"
git config --global user.email "your-email"
```

[You can learn more about Git's configuration options here](https://git-scm.com/docs/git-config)


## 📘 GitHub Wiki — What It Is & How to Use It

### **What is the GitHub Wiki option?**

GitHub **Wiki** is a built-in documentation feature that lets you create **rich, structured, multi-page documentation** for your repository.

It works like a mini-website where you can write pages in **Markdown**, connect them with links, and organize your project documentation.


### **Why is GitHub Wiki used?**

GitHub Wiki is helpful for:

* 📚 **Project documentation**
* 📝 **Technical guides**
* ⚙️ **Setup instructions**
* 📡 **API documentation**
* 🗂️ **How-to tutorials**
* 🤝 **Team knowledge sharing**

Unlike the main repository docs, Wiki pages live in a **separate Git repository**, meaning:

* You can clone & edit them separately.
* They don't clutter your repo’s main files.

### 📘 GitHub Wiki — Step-by-Step Setup Guide

#### 1. Enable or Open GitHub Wiki
1. Go to your GitHub repository.
2. Click on the **"Wiki"** tab (usually at the top).
3. Click **"Create the first page"**.


#### 2. Create Your First Wiki Page
1. Enter a title, e.g., `Home`.
2. Add content in Markdown:
   ```md
   # Welcome to My Project Wiki
   This wiki contains documentation and guides.
    ```
3. Click **Save Page**.

#### 3. Create Additional Pages

1. On the right sidebar, click **"New Page"**.
2. Add a title, e.g., `Installation`.
3. Add content:

   ````md
   # Installation Guide

   ## Requirements
   - Node.js
   - Git
   - Docker (optional)

   ## Steps
   1. Clone the repo
      ```bash
      git clone https://github.com/username/repo.git
     ```

   2. Install dependencies

      ```bash
      npm install
      ```
   3. Start the server

      ```bash
      npm start
      ```
    4. Click **Save Page**.

### 4. Link Between Wiki Pages

Use normal Markdown links:

```md
See the [Installation Guide](Installation) for setup steps.

Return to the [Home](Home) page.
```

### 5. Clone the Wiki Repository Locally (Optional)

Each GitHub wiki is its **own Git repo**.

To clone:

```bash
git clone https://github.com/<username>/<repo>.wiki.git
```

Edit Markdown files locally, then push:

```bash
git add .
git commit -m "Updated wiki"
git push
```

### 6. Organize Wiki Pages with a Sidebar

1. Create a page named **_Sidebar** (case sensitive).
2. Add navigation links:

```md
# 📚 Documentation

- [Home](Home)
- [Installation](Installation)
- [API Reference](API-Reference)
- [Contributing](Contributing)
```

This will appear on the left side in all pages.

### 7. Optional: Create a Footer

Create a page named **_Footer**:

```md
© 2025 MyProject — Documentation Provided Under MIT License
```

### 🎉 You're Done!

You now have:

* A GitHub Wiki
* Multiple pages
* Markdown documentation
* Links, sidebar, and footer

## GitHub Fork — What It Is & How to Use It (Plain Text Version)

**What is the Fork option in GitHub?**
A Fork is a personal copy of someone else’s GitHub repository.
It allows you to modify the project independently, experiment safely, or contribute changes back to the original project using Pull Requests.

### Why Fork is Used

1. **Contributing to open-source projects**
   You cannot directly push to someone else’s repo. Forking lets you copy it, make changes, and then send a Pull Request.

2. **Experimenting with changes**
   You can test new features without affecting the original code.

3. **Creating your own version**
   You can customize or extend the project for personal use.

### Step-by-Step Guide to Using Fork

#### 1. Fork a Repository

1. Go to any GitHub repository you want to copy.
2. Click the “Fork” button in the top-right corner.
3. Choose your GitHub account (where the fork will be created).
4. Optionally rename the repository.
5. Click “Create Fork”.

Now you have your own editable copy of the project.

#### 2. Clone Your Fork to Your Computer

Open the terminal and run:
```
git clone [https://github.com/your-username/forked-repo.git](https://github.com/your-username/forked-repo.git)
```
Then move into the project folder:
```
cd forked-repo
```

#### 3. Make Changes to Your Fork

Edit files in your editor.
Then run:
```
git add .
git commit -m "Describe your changes"
git push
```
Your fork now contains your updates.

#### 4. Create a Pull Request (Send Your Changes to the Original Repository)

1. Go to *your* fork on GitHub.
2. Click “Contribute” → “Open pull request”.
3. Review your changes.
4. Add a title and description.
5. Click “Create Pull Request”.

The owner of the original repo will review your changes.

#### 5. Keep Your Fork Updated With the Original Repository

Add the original repository as a remote:
```
git remote add upstream [https://github.com/original-owner/original-repo.git](https://github.com/original-owner/original-repo.git)
```
Fetch updates:
```
git fetch upstream
```
Merge updates into your main branch:
```
git checkout main
git merge upstream/main
```
Push updates to your fork:
```
git push origin main
```
Your fork is now synchronized.

#### 6. Optional: Use a Branch for Your Changes

Creating a branch is recommended:
```
git checkout -b feature/my-new-feature
```
After editing, commit and push:
```
git push origin feature/my-new-feature
```
Then open a Pull Request from this branch.

### Summary

* A **Fork** is your own copy of another repo.
* Used for open-source contributions, experimentation, and custom versions.
* Workflow:
  Fork → Clone → Change → Push → Pull Request → Sync with Original Repo

---

# *Github Action*

**GitHub Actions = Automation + CI/CD inside GitHub.**

**GitHub Actions** is an automation and CI/CD (Continuous Integration / Continuous Deployment) service built directly into GitHub.

It allows you to automatically run tasks whenever certain events happen in your repository—like pushing code, creating a pull request, opening an issue, or running scheduled jobs.

## ⭐ What GitHub Actions Is

GitHub Actions is a system that lets you:

* Automate workflows
* Build, test, and deploy code
* Run jobs based on GitHub events
* Create custom pipelines
* Use thousands of ready-made actions from the GitHub Marketplace

**All workflows are defined in **YAML files** inside the `.github/workflows/` folder of your repository.**

## ⭐ What GitHub Actions Is Used For

### 1. **CI/CD Pipelines**

* Automatically build and test your code when you push to GitHub
* Deploy your application to servers, cloud platforms (AWS, Azure, GCP), or containers

### 2. **Automation**

* Auto label issues
* Auto assign reviewers
* Send notifications
* Auto merge pull requests

### 3. **Project Management**

* Generate release notes
* Manage issues
* Run scripts on schedules (cron)

### 4. **Security**

* Run security scans (SAST, dependency scanning)

## ⭐ How GitHub Actions Works (Simple Explanation)

1. You create a workflow file like:
   `.github/workflows/ci.yml`

2. Inside the workflow, you define:

   * Trigger events (e.g., on push, on pull request, scheduled)
   * Jobs to run
   * Steps inside each job (commands or pre-built actions)

3. GitHub provides a runner (Ubuntu, Windows, Mac) that executes your workflow.

### ⭐ Example of a Simple GitHub Action (Explained Simply)

Here’s how a basic workflow behaves:

**Trigger:** Whenever you push code
**Action:** It runs tests

Steps it performs:

1. Checkout the code
2. Install dependencies
3. Run tests

GitHub automatically shows results: passed or failed.

### ⭐ Example Workflow (Plain Text)

File path: `.github/workflows/test.yml`

Content description:

* Name: Run tests
* Trigger: on push
* Job: test
* Runs on: Ubuntu
* Steps:

  1. Checkout code
  2. Set up Node.js
  3. Install packages
  4. Run tests

### ⭐ Why GitHub Actions Is Popular

* Built into GitHub (no third-party tool needed)
* Free for public repositories
* Huge marketplace of ready-to-use automations
* Easy to integrate with any language or cloud provider
* Fast setup with YAML
* Works on Linux, Windows, and macOS

## Workflow , Jobs & Steps

- **Code Repository**
    - **Workflow 1**
        - *Job 1*
            - step 1
            - step 2
        - *Job 2*
            - step 1
    - **Workflow 2**
        - *Job 1*
            - step 1
            - step 2
            - step 3
            - step 4
    - **Workflow 3**
        - *Job 1*
            - step 1
        - *Job 2*
            - step 1

- ![Key Element Github Action](https://github.com/sawanchouksey/documents/blob/main/docs/DevOps/keyElementGithubAction.png?raw=true)

## GitHub Actions: Availability & Pricing

In public repositories, you can use GitHub Actions for free. For private repositories, only a certain amount of monthly usage is available for free - extra usage on top must be paid.

[The exact quotas and payment details depend on your GitHub plan, a detailed summary can be found here](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)

[If you can't find an "Actions" tab in your GitHub repository, you can should enable them as described here](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)


# ⭐ GitHub Workflow Trigger Events

GitHub Actions workflows run when certain **events** occur.
These events tell GitHub *when* to start a workflow.

![GithubFlowTrigger](https://github.com/sawanchouksey/documents/blob/main/docs/DevOps/GitFlowTriggerTypes.png?raw=true)

All triggers go under:

```
on:
```

Example:

```
on: push
```

---

## ⭐ Main Trigger Event Types (with explanations + syntax)

### 1. **push**

Triggered when you push commits to a branch or tag.

**Explanation:**
Runs when new code is pushed to GitHub.

**Syntax:**

```
on:
  push:
    branches:
      - main
      - dev
    tags:
      - "v*"
```

### 2. **pull_request**

Triggered when a Pull Request is opened, updated, reopened, or closed.

**Explanation:**
Useful for running tests **before merging code**.

**Syntax:**

```
on:
  pull_request:
    branches:
      - main
```

### 3. **workflow_dispatch**

Manual trigger button inside GitHub Actions.

**Explanation:**
Lets you start workflow manually with or without input.

**Syntax:**

```
on:
  workflow_dispatch:
    inputs:
      env:
        description: "Choose environment"
        required: true
        default: "dev"
```

### 4. **schedule**

Runs on a timer using cron syntax.

**Explanation:**
Useful for daily tasks, backups, scanning, etc.

**Syntax:**

```
on:
  schedule:
    - cron: "0 0 * * *"   # Every day at midnight
```

### 5. **workflow_run**

Triggered after another workflow completes.

**Explanation:**
Useful for chaining workflows.

**Syntax:**

```
on:
  workflow_run:
    workflows: ["Build"]
    types: [completed]
```

### 6. **release**

Triggered when a GitHub release is created, published, or updated.

**Explanation:**
Useful for publishing artifacts or tagging releases.

**Syntax:**

```
on:
  release:
    types: [published]
```

### 7. **issues**

Triggered for issue events like open, close, edit.

**Explanation:**
Automate labeling, assigning, or commenting on issues.

**Syntax:**

```
on:
  issues:
    types: [opened, edited]
```

### 8. **issue_comment**

Triggered when someone comments on an issue or PR.

**Syntax:**

```
on:
  issue_comment:
    types: [created]
```

### 9. **pull_request_review**

Triggered when a PR review is submitted.

**Syntax:**

```
on:
  pull_request_review:
    types: [submitted]
```

### 10. **delete**

Triggered when branches or tags are deleted.

**Syntax:**

```
on:
  delete
```

### 11. **create**

Triggered when branches or tags are created.

**Syntax:**

```
on:
  create
```

### 12. **fork**

Triggered when someone forks the repo.

**Syntax:**

```
on:
  fork
```

### 13. **watch**

Triggered when someone stars the repository.

**Syntax:**

```
on:
  watch
```

### 14. **push to a specific path**

Trigger only when certain folders or files change.

**Syntax:**

```
on:
  push:
    paths:
      - "src/**"
      - "docs/*.md"
```

### ⭐ Combined Example

```
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

### ⭐ Summary Table

| Trigger           | When It Runs                   |
| ----------------- | ------------------------------ |
| push              | When commits are pushed        |
| pull_request      | When PR is created/updated     |
| workflow_dispatch | Manual trigger                 |
| schedule          | Timer/cron schedule            |
| workflow_run      | When another workflow finishes |
| release           | When releases change           |
| issues            | Issue events                   |
| issue_comment     | Comments on issues/PRs         |
| create            | New branch or tag              |
| delete            | Branch or tag removed          |
| fork              | Repo is forked                 |
| watch             | Repo is starred                |


## Running Multi-Line Shell Commands

If you need to run multiple shell commands (or multi-line commands, e.g., for readability), you can easily do so by adding the pipe symbol (|) as a value after the run: key.

Like this:
```
run: |
    echo "First output"
    echo "Second output"
```
This will run both commands in one step.

## ⭐ What is `uses:` in GitHub Action Workflows?

In GitHub Actions, the **`uses:` keyword** is used to:

- ✔️ Load and run **pre-built actions**

(From GitHub Marketplace or other repositories)

- ✔️ Reuse **existing actions**

(e.g., checkout code, set up languages)

- ✔️ Call **composite actions**

(Actions you create yourself)

- ✔️ Use **Docker container actions**

Think of `uses:` as **importing a ready-made function** into your workflow.

### ⭐ Why `uses:` Is Important

Instead of writing everything manually, `uses:` lets you add:

* Code checkout
* Node/Python/JDK setup
* Cloud deployment tools
* Docker build actions
* Testing tools
* Linting tools

These are reusable, version-controlled, and easier than writing scripts.

### ⭐ `uses:` vs `run:` (Quick Difference)

| Keyword   | Purpose                        |
| --------- | ------------------------------ |
| **uses:** | Runs a pre-built action        |
| **run:**  | Executes custom shell commands |

Example:

```
uses: actions/checkout@v4   # prebuilt action
run: npm install            # manual shell command
```

### ⭐ Common Syntax Patterns

#### 1. **Using a Marketplace Action**

Example: Checkout code from repo

```
steps:
  - uses: actions/checkout@v4
```

#### 2. **Using an Action with Inputs**

Example: Installing Node.js

```
steps:
  - uses: actions/setup-node@v4
    with:
      node-version: 18
```

#### 3. **Using a Local Action**

If you created your own action inside `.github/actions/my-action/`

```
steps:
  - uses: ./.github/actions/my-action
```

#### 4. **Using a Docker Action**

Runs a Docker container action

```
steps:
  - uses: docker://alpine:3.19
```

#### 5. **Using an Action from Another Repository**

```
steps:
  - uses: username/repo-name@v1
```

### ⭐ Full Example Workflow Showing `uses:`

```
name: Example Workflow

on: push

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      # 1. Use checkout action
      - uses: actions/checkout@v4

      # 2. Use setup-node action
      - uses: actions/setup-node@v4
        with:
          node-version: 18

      # 3. Use run to install packages
      - run: npm install

      # 4. Use run to run tests
      - run: npm test
```

Here:

* `uses: actions/checkout@v4` → imports checkout action
* `uses: actions/setup-node@v4` → imports Node.js setup action
* `run:` → your custom commands

### ⭐ Summary

**`uses:`** is used to import and run **pre-built GitHub actions** in your workflow.
It helps automate tasks without writing complex scripts.

You use it to:

* Checkout code
* Set up programming languages
* Build apps
* Deploy apps
* Use Docker actions
* Use custom or third-party actions

## By default , `Pull Request` based on fork do `NOT` trigger a workflow. because Everyone can `fork` & open `Pull Request`. This leades to malicious workflow runs & excess cost could be caused. `First time` contributor must be `approve` manually.

## ⭐ PART 1 — Cancelling Workflow Runs

## 🔹 **Default Behavior (Without Concurrency)**

By default:

#### ✔ GitHub **does NOT cancel** old workflow runs.

If you push multiple commits quickly:

* Commit 1 → Workflow Run 1 starts
* Commit 2 → Workflow Run 2 starts
* Commit 3 → Workflow Run 3 starts

All **three** runs will execute independently.

This wastes:

* Runner time
* CI minutes
* Resources
* Time (if the workflow is long)

### 🔹 Enable Auto-Cancel (Concurrency Control)

Use:

```
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

#### ✔ Behavior After Adding This

* New workflow starts
* All earlier runs for the same branch are **cancelled automatically**

#### Example

```
name: CI

on: push

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building..."
```

### ⭐ Cancelling Summary Table

| Feature                      | Default Behavior                    | Custom Behavior                     |
| ---------------------------- | ----------------------------------- | ----------------------------------- |
| Cancelling old workflow runs | **Not canceled** (all run)          | Use `concurrency` → cancel old runs |
| Resource usage               | High                                | Efficient                           |
| Ideal for                    | Small repos or rarely updated repos | Active repos, large pipelines       |

## ⭐ PART 2 — Skipping Workflow Runs

Github Actions allows skipping using commit message keywords, path rules, and conditions.

### 🔹 **Default Behavior (Without Skipping Rules)**

By default:

#### ✔ Every push runs all workflows

Even if you modify only:

* README.md
* Documentation
* A small comment

#### ✔ Every pull request triggers workflows

Even if no important files changed.

#### ✔ All branches trigger workflows (if configured)

So without skip logic, **GitHub runs workflows for everything**.

## 🔹 Types of Skipping + Their Behavior

### 1️⃣ **Skipping Using Commit Messages**

Uses special keywords:

* `[skip ci]`
* `[ci skip]`
* `[skip actions]`
* `[actions skip]`

#### ✔ Default behavior

If these keywords appear **anywhere in commit message**, GitHub **skips all workflows**.

#### Example

Commit message:

```
Updated README [skip ci]
```

Result: No workflow runs.

### 2️⃣ **Skipping Using Paths**

Use `paths:` or `paths-ignore:` under triggers.

#### Example: Run only when src/ files change

```
on:
  push:
    paths:
      - 'src/**'
```

#### ✔ Default behavior here

If files **outside** `src/` change → workflow is skipped.

#### Example: Skip workflow for documentation only changes

```
on:
  pull_request:
    paths-ignore:
      - 'docs/**'
      - '*.md'
```

#### Default behavior

If only doc files changed → workflow is skipped.

### 3️⃣ **Skipping Using Conditions (`if:`)**

#### Example: Skip if triggered by Dependabot

```
jobs:
  test:
    if: github.actor != 'dependabot[bot]'
```

#### Default behavior

If actor is Dependabot → job is skipped
If actor is anyone else → job runs

### ⭐ Skipping Summary Table

| Skip Method     | Default Behavior | Condition to Skip                            |
| --------------- | ---------------- | -------------------------------------------- |
| Commit messages | Runs normally    | Skip when `[skip ci]` is used                |
| paths           | Runs always      | Skip when modified files don't match paths   |
| paths-ignore    | Runs always      | Skip when modified files match ignored paths |
| `if:` condition | Runs always      | Skip when `if:` evaluates to false           |

## ⭐ FULL SCENARIO COMPARISONS

### ✔ Scenario 1 — Developer pushes 5 quick commits

* Default → all 5 workflows run
* With concurrency → only last run continues (others auto-cancel)

### ✔ Scenario 2 — Documentation-only update

* Default → workflow runs
* With `[skip ci]` → workflow does not run
* With `paths-ignore` → workflow does not run

### ✔ Scenario 3 — Dependabot PR

* Default → workflow runs
* With `if: github.actor != 'dependabot[bot]'` → workflow skipped

### ✔ Scenario 4 — Only backend folder changed

* Default → workflow runs
* With `paths: backend/**` → only backend change triggers workflow
* Frontend-only change will skip workflow

### ⭐ Final Summary

#### Cancelling

* **Default:** ALL runs execute (nothing is cancelled)
* **After concurrency rule:** old runs are cancelled automatically

#### Skipping

* **Default:** workflow runs on every push/PR
* **Using rules:** workflow can skip based on commit message, paths, or conditions

## ✅ **Job Outputs**

#### **Purpose:**

Pass **small pieces of data** (strings, numbers, booleans) from one job to another *within the same workflow run*.

#### **Best for:**

* IDs
* Flags
* Filenames
* Simple messages
* Versions

#### **Stored where:**

Only inside the workflow run. Not downloadable.

#### **Limits:**

* Must be **small text**
* Must be set using workflow commands
* Cannot store files

### **Example: Job Output Syntax**

#### **Job 1 — Produces an output**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.version.outputs.tag }}
    steps:
      - id: version
        run: echo "tag=v1.2.3" >> $GITHUB_OUTPUT
```

#### **Job 2 — Consumes the output**

```yaml
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying version ${{ needs.build.outputs.image-tag }}"
```

## ✅ **Artifacts**

#### **Purpose:**

Upload and store **files** created during a workflow.

#### **Best for:**

* Build outputs (binaries, ZIPs, packages)
* Test reports
* Logs
* Coverage reports
* Any downloadable files

#### **Stored where:**

Uploaded to GitHub and can be downloaded later.

#### **Limits:**

* Size limit per artifact (2 GB)
* Retention time limits

### **Example: Artifact Syntax**

#### **Upload artifact**

```yaml
- name: Upload build output
  uses: actions/upload-artifact@v4
  with:
    name: my-build
    path: dist/
```

#### **Download artifact**

```yaml
- name: Download build output
  uses: actions/download-artifact@v4
  with:
    name: my-build
```

### 🔍 **Side-by-Side Comparison**

| Feature                | **Job Output**   | **Artifact**               |
| ---------------------- | ---------------- | -------------------------- |
| Stores files?          | ❌ No             | ✅ Yes                      |
| Stores text values?    | ✅ Yes            | Possible but pointless     |
| Access by another job? | ✅ Yes            | ✅ Yes (via download step)  |
| Downloadable?          | ❌ No             | ✅ Yes                      |
| Size allowed           | Very small       | Up to 2 GB                 |
| Purpose                | Passing metadata | Storing/transferring files |
| Example value          | “v1.2.3”         | `dist/app.zip`             |

### 🎯 **Simple Explanation**

* **Job Output:**
  “Here is a small piece of text data I want to share with another job.”

* **Artifact:**
  “Here is an entire file/folder that needs to be saved or downloaded later.”

## In **GitHub Actions**, a **context** is a *special variable namespace* that provides information about the workflow run, GitHub event, jobs, steps, environment, secrets, and more.

Think of a **context** as a set of values you can reference using:

```
${{ context_name.property }}
```

Example:

```yaml
run: echo "Hello from ${{ github.actor }}"
```

### ✅ **Why Contexts Matter**

Contexts allow you to access information such as:

* Who triggered the workflow
* Which branch triggered the event
* Commit details
* Job status
* Secrets
* Artifacts
* Runner information
* Outputs from previous steps/jobs

### ⭐ **Most Important & Widely Used Contexts**

Below is a list of the most common contexts with examples and syntax.

### 1️⃣ **github** context

Contains information about the GitHub event, repository, actor, ref, etc.

#### Example usage:

```yaml
run: echo "Triggered by ${{ github.actor }} on ${{ github.ref }}"
```

#### Popular values:

| Expression          | Description                               |
| ------------------- | ----------------------------------------- |
| `github.actor`      | User who triggered the workflow           |
| `github.repository` | `owner/repo`                              |
| `github.ref`        | Branch or tag ref                         |
| `github.sha`        | Commit SHA                                |
| `github.event_name` | Event type (`push`, `pull_request`, etc.) |

### 2️⃣ **env** context

Contains environment variables defined using the `env:` key.

#### Example usage:

```yaml
env:
  MY_VAR: hello

steps:
  - run: echo ${{ env.MY_VAR }}
```

#### Popular use:

* Reuse custom environment variables across steps/jobs.

### 3️⃣ **secrets** context

Used to access encrypted secrets stored in GitHub Secrets.

#### Example:

```yaml
run: echo "Password is ${{ secrets.DB_PASSWORD }}"
```

#### Notes:

* Values are masked in logs.
* Read-only.

### 4️⃣ **vars** context

Contains GitHub **Repository Variables**.

#### Example:

```yaml
run: echo "Environment: ${{ vars.APP_ENV }}"
```

### 5️⃣ **runner** context

Information about the runner machine.

#### Example:

```yaml
run: echo "Running on ${{ runner.os }}"
```

#### Useful values:

| Property      | Example                     |
| ------------- | --------------------------- |
| `runner.os`   | `Linux`, `Windows`, `macOS` |
| `runner.arch` | CPU architecture            |
| `runner.temp` | Temp directory path         |

### 6️⃣ **job** context

Information about the current job.

### Example:

```yaml
run: echo "Job status ${{ job.status }}"
```

### 7️⃣ **steps** context

Access outputs from previous steps.

#### Example:

```yaml
steps:
  - id: setvalue
    run: echo "msg=Hello" >> $GITHUB_OUTPUT

  - run: echo "Message: ${{ steps.setvalue.outputs.msg }}"
```

### 8️⃣ **needs** context

Used for accessing **outputs of previous jobs**.

#### Example:

```yaml
jobs:
  build:
    outputs:
      tag: ${{ steps.ver.outputs.tag }}
    steps:
      - id: ver
        run: echo "tag=1.0.0" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    steps:
      - run: echo "Tag is ${{ needs.build.outputs.tag }}"
```

### 9️⃣ **matrix** context

Used for matrix strategies.

#### Example:

```yaml
strategy:
  matrix:
    node: [16, 18]

steps:
  - run: echo "Node version: ${{ matrix.node }}"
```

### 🔟 **inputs** context

Used in reusable workflows or composite actions.

#### Example:

```yaml
run: echo "Input value: ${{ inputs.username }}"
```

### 🧩 Summary Table — Widely Used Contexts

| Context   | Purpose                       | Example                          |
| --------- | ----------------------------- | -------------------------------- |
| `github`  | Info about event, repo, actor | `${{ github.ref }}`              |
| `env`     | Environment variables         | `${{ env.MY_VAR }}`              |
| `secrets` | Secure secrets                | `${{ secrets.API_KEY }}`         |
| `vars`    | Repository variables          | `${{ vars.ENV_NAME }}`           |
| `runner`  | Runner system info            | `${{ runner.os }}`               |
| `job`     | Info about the current job    | `${{ job.status }}`              |
| `steps`   | Read step outputs             | `${{ steps.id.outputs.key }}`    |
| `needs`   | Read previous job outputs     | `${{ needs.build.outputs.tag }}` |
| `matrix`  | Access matrix variables       | `${{ matrix.node }}`             |
| `inputs`  | Reusable workflow inputs      | `${{ inputs.value }}`            |


## ✅ **What is an Environment Variable in GitHub Actions?**

An **environment variable (`env`)** in GitHub Actions is a variable that stores data (strings, numbers, paths, tokens, etc.) that you can reuse in **multiple steps**, **jobs**, or the whole **workflow**.

You reference an environment variable using:

```
${{ env.VARIABLE_NAME }}
```

or inside shell commands:

```
$VARIABLE_NAME
```

### 🧭 **Why use environment variables?**

* To avoid repeating values
* To store configuration values
* To pass data between steps
* To make workflows cleaner and reusable

### 🧱 **3 Levels of Environment Variables**

There are 3 levels where you can define `env`:

#### 1️⃣ **Workflow-level env**

Available to **all jobs** and **all steps**.

### Syntax:

```yaml
env:
  APP_NAME: MyApp
  ENV: production
```

### Example:

```yaml
name: Example

env:
  APP_NAME: MyApp
  ENV: production

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "App = ${{ env.APP_NAME }}, Environment = $ENV"
```

#### 2️⃣ **Job-level env**

Available **only inside a specific job**.

### Syntax:

```yaml
jobs:
  build:
    env:
      VERSION: 1.0.0
```

### Example:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      VERSION: 1.2.3
    steps:
      - run: echo "Building version $VERSION"
```

#### 3️⃣ **Step-level env**

Available **only inside one step**.

### Syntax:

```yaml
steps:
  - env:
      NAME: John
```

### Example:

```yaml
steps:
  - env:
      NAME: John
    run: echo "Hello $NAME"
```

### 🧪 **Step-by-Step Approach to Set Env Variables**

#### **Step 1 — Create/Choose workflow file**

Create `.github/workflows/demo.yml`

#### **Step 2 — Define environment variables**

You can choose the scope:

##### a) **Workflow level**

```yaml
env:
  APP_ENV: production
  SERVICE_URL: https://example.com
```

##### b) **Job level**

```yaml
jobs:
  build:
    env:
      BUILD_MODE: release
```

##### c) **Step level**

```yaml
steps:
  - env:
      NAME: TestUser
```

#### **Step 3 — Use environment variables**

Inside run command:

```yaml
run: echo "Running in $APP_ENV mode"
```

Or GitHub expression:

```yaml
run: echo "Service URL is ${{ env.SERVICE_URL }}"
```

#### **Step 4 — (Advanced) Create env variables dynamically using `$GITHUB_ENV`**

You can create env variables *during workflow execution*:

```yaml
- name: Set dynamic variable
  run: echo "VERSION=2.0.0" >> $GITHUB_ENV
```

Use later:

```yaml
- run: echo "Version is $VERSION"
```

### 🧩 **Full Practical Example**

```yaml
name: Env Variable Demo

env:
  GLOBAL_VAR: "I am global"

jobs:
  example:
    runs-on: ubuntu-latest

    env:
      JOB_VAR: "I am job level"

    steps:
      - name: Step with its own env
        env:
          STEP_VAR: "I am step level"
        run: |
          echo "GLOBAL = $GLOBAL_VAR"
          echo "JOB = $JOB_VAR"
          echo "STEP = $STEP_VAR"

      - name: Using GitHub Expression Syntax
        run: echo "Global = ${{ env.GLOBAL_VAR }}"
```

### 📌 Summary

| Level              | Scope              | Example syntax              |
| ------------------ | ------------------ | --------------------------- |
| **Workflow-level** | All jobs & steps   | `env: { VAR: value }`       |
| **Job-level**      | One job            | `jobs.<job>.env:`           |
| **Step-level**     | One step           | `steps[].env:`              |
| **Dynamic env**    | Created at runtime | `echo "X=1" >> $GITHUB_ENV` |

[GitHub Actions also provides a couple of default environment variables that are set automatically](https://docs.github.com/en/actions/learn-github-actions/environment-variables#default-environment-variables)

## ✅ **What Are Environment Secrets in GitHub Actions?**

**Environment Secrets** are encrypted variables stored in a **GitHub Environment**, used to protect sensitive information such as:

* API keys
* Database passwords
* Tokens
* Credentials

Environment-level secrets belong to a specific **Environment** (e.g., `dev`, `staging`, `prod`) and can only be accessed by workflows that deploy to that environment.

### ✅ **Why Use Environment Secrets?**

✔ Allow different secrets for different environments
✔ Provide deployment protection rules (required reviewers, wait timers)
✔ More secure than repository secrets for multi-env workflows

### 🛠️ **How to Set Up Environment Secrets (Step-By-Step)**

#### **Step 1: Go to Your GitHub Repository**

1. Open your repository on GitHub
2. Click **Settings**
3. Scroll to **Environments** on the left sidebar
4. Click **New Environment**

#### **Step 2: Create an Environment**

Example: create an environment named:

* `dev`
* `staging`
* `production`

Click **Configure environment**.

#### **Step 3: Add Secrets to the Environment**

1. Inside the environment page, find **"Environment secrets"**
2. Click **Add secret**
3. Enter:

   * **Name** (e.g., `API_KEY`)
   * **Value** (your secret string)
4. Click **Add secret**

### 🔐 **Where Are Environment Secrets Used?**

Inside a GitHub Actions workflow (`.github/workflows/...yml`), you can access environment secrets using:

```yaml
${{ secrets.SECRET_NAME }}
```

### 📘 **Example Workflow Using Environment Secrets**

#### Create workflow file:

`.github/workflows/deploy.yml`

```yaml
name: Deploy to Production

on:
  push:
    branches: [ "main" ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Link workflow to the environment

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Print secret (demo)
        run: echo "Secret value is: $MY_SECRET"
        env:
          MY_SECRET: ${{ secrets.API_KEY }}   # Access environment secret
```

#### What happens:

* The job deploys to environment `production`
* The secret `API_KEY` defined in **production environment** becomes available
* GitHub masks secrets in logs

### 📌 **Environment vs Repository Secrets**

| Feature          | Repository Secrets | Environment Secrets                    |
| ---------------- | ------------------ | -------------------------------------- |
| Scope            | Entire repository  | Specific environment                   |
| Deployment rules | ❌ None             | ✔ Reviewers, timers, branches          |
| Best for         | simple repos       | multi-stage workflows (dev/stage/prod) |

### 🔤 **Syntax Reference**

#### **Access a secret:**

```yaml
${{ secrets.SECRET_NAME }}
```

#### **Expose to a step:**

```yaml
env:
  TOKEN: ${{ secrets.MY_TOKEN }}
```

#### **Use inside a script:**

```bash
echo "$TOKEN"
```

#### **Require environment:**

```yaml
environment: staging
```

### 🎯 **Simple Example (Shortest Version)**

```yaml
steps:
  - run: echo "API: $API_KEY"
    env:
      API_KEY: ${{ secrets.API_KEY }}
```

## 🔍 **What Is Controlling Workflow & Job Execution in GitHub Actions?**

GitHub Actions allows you to **control when workflows, jobs, and steps run** using:

#### ✔ **Triggers** (when a workflow starts)

#### ✔ **Expressions & Conditions** (`if:` syntax)

#### ✔ **Dependencies** (`needs:` syntax)

#### ✔ **Environment protection rules**

#### ✔ **Concurrency control**

#### ✔ **Timeout rules**

#### ✔ **Error control (`continue-on-error`)**

These mechanisms let you decide:

* *When the workflow should run*
* *Which jobs should run*
* *Which steps should run*
* *What conditions must be met*

### 🧭 **1. Workflow-Level Controls (Start/Trigger Conditions)**

These control **when the workflow itself starts**.

#### **Common Workflow Triggers**

| Type               | Example                        |
| ------------------ | ------------------------------ |
| Push events        | `on: push`                     |
| Pull Requests      | `on: pull_request`             |
| Schedule (cron)    | `on: schedule`                 |
| Manual trigger     | `on: workflow_dispatch`        |
| Reusable workflows | `on: workflow_call`            |
| Release events     | `on: release`                  |
| Tags               | `on: push: tags: ['v*']`       |
| Specific branch    | `on: push: branches: ['main']` |

#### Example:

```yaml
on:
  push:
    branches: ["main"]
  workflow_dispatch:
```

### 🧱 **2. Job-Level Controls**

Controls **which jobs run** and **in what order**.

#### ✅ **A. Conditions using `if:`**

```yaml
jobs:
  build:
    if: github.ref == 'refs/heads/main'
```

#### Common job conditions:

* Run only on pull requests
* Skip when commit contains a message
* Run only when previous job succeeded/failed

Examples:

```yaml
if: github.event.pull_request.merged == true
if: startsWith(github.ref, 'refs/tags/')
if: contains(github.event.head_commit.message, '[deploy]')
```

#### ✅ **B. Job Dependencies (`needs:`)**

Controls order of execution.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest

  deploy:
    needs: test  # runs only if test succeeds
```

Multiple dependencies:

```yaml
needs: [test, lint]
```

#### ✅ **C. Continue on failure**

```yaml
continue-on-error: true
```

#### ✅ **D. Timeout**

```yaml
timeout-minutes: 10
```

#### ✅ **E. Concurrency (avoid duplicate runs)**

```yaml
concurrency:
  group: production-deploy
  cancel-in-progress: true
```

### 🧩 **3. Step-Level Controls**

Controls execution **inside jobs**.

#### **Syntax:**

```yaml
if: <condition>
```

Example:

```yaml
steps:
  - name: Deploy only if build succeeded
    if: success()
```

### 🧠 **4. GitHub Actions Condition Functions (MOST WIDELY USED)**

#### ✔ **success()**

Runs if all previous steps/jobs succeeded.

```yaml
if: success()
```

#### ✔ **failure()**

Runs if a previous step/job failed.

```yaml
if: failure()
```

#### ✔ **always()**

Runs regardless of success/failure.

```yaml
if: always()
```

#### ✔ **cancelled()**

Runs only if workflow was cancelled.

```yaml
if: cancelled()
```

### 🧮 **5. Expression Syntax for Conditions**

You can use:

#### **Operators**

* `==`, `!=`
* `&&`, `||`
* `!`
* `>`, `<`, `>=`, `<=`

#### **String Functions**

* `startsWith()`
* `endsWith()`
* `contains()`
* `format()`

Examples:

```yaml
if: contains(github.ref, 'feature')
if: startsWith(github.ref, 'refs/tags/')
if: github.actor == 'octocat'
if: github.event_name == 'push'
if: env.ENVIRONMENT == 'prod'
```

### 📘 **6. Example: Full Workflow With Job & Step Conditions**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: ["main"]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - run: echo "Building..."

  test:
    needs: build
    runs-on: ubuntu-latest
    if: success()

    steps:
      - run: echo "Testing..."

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && success()

    steps:
      - run: echo "Deploying to Production"
```

### 📌 **Summary Table of ALL Major Controllers**

| Level    | Control Type           | Key Syntax           |
| -------- | ---------------------- | -------------------- |
| Workflow | Triggers               | `on:`                |
| Job      | Conditions             | `if:`                |
| Job      | Dependencies           | `needs:`             |
| Job      | Concurrency            | `concurrency:`       |
| Job      | Timeout                | `timeout-minutes:`   |
| Job      | Error control          | `continue-on-error:` |
| Step     | Conditions             | `if:`                |
| Step     | Env variables          | `env:`               |
| Env      | Protected deploy rules | reviewers, approvals |

## 🔁 **What Is a Reusable Workflow in GitHub Actions?**

A **reusable workflow** is a workflow that can be **called by other workflows**, allowing you to:

✔ Reuse CI steps across repositories
✔ Centralize common logic (tests, build, deploy)
✔ Reduce duplicate YAML code
✔ Create modular pipelines

Reusable workflows behave like **functions** in programming.

They are triggered using:

```yaml
on: workflow_call
```

### 🛠️ **1. How to Create a Reusable Workflow**

You create it like a normal workflow, but the trigger must be:

```yaml
on:
  workflow_call:
```

And you can define:

* **Inputs**
* **Secrets**
* **Outputs**

### 🧩 **2. How to Add Inputs to a Reusable Workflow**

You define inputs inside `on.workflow_call.inputs`.

#### ✔ Input Syntax (Reusable Workflow)

```yaml
on:
  workflow_call:
    inputs:
      input-name:
        description: "Explain input"
        required: true/false
        type: string / boolean / number
```

Inside the workflow steps, you access inputs using:

```yaml
${{ inputs.input-name }}
```

### 📘 **3. Full Example: Reusable Workflow**

Location:
`.github/workflows/reusable-build.yml`

```yaml
name: Reusable Build Workflow

on:
  workflow_call:
    inputs:
      environment:
        description: "Deployment environment"
        required: true
        type: string
      debug_mode:
        description: "Whether to enable debug"
        required: false
        type: boolean

    secrets:
      API_KEY:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - run: echo "Environment is: ${{ inputs.environment }}"
      - run: echo "Debug mode: ${{ inputs.debug_mode }}"
      - run: echo "Using secret: ${{ secrets.API_KEY }}"
```

### 🚀 **4. How to Call a Reusable Workflow**

Create a caller workflow:

`.github/workflows/main.yml`

```yaml
name: Main Pipeline

on:
  push:
    branches: ["main"]

jobs:
  use-reusable:
    uses: ./.github/workflows/reusable-build.yml  # local repository
    with:
      environment: "production"
      debug_mode: true
    secrets:
      API_KEY: ${{ secrets.PROD_API_KEY }}
```

### 📌 **5. Calling a Reusable Workflow From Another Repository**

```yaml
uses: org/repo/.github/workflows/reusable-build.yml@v1
```

Example:

```yaml
jobs:
  deploy:
    uses: my-org/ci-library/.github/workflows/deploy.yml@main
    with:
      environment: staging
    secrets:
      API_KEY: ${{ secrets.STAGING_API_KEY }}
```

### 🧠 **6. Types of Inputs You Can Use**

| Type      | Description        |
| --------- | ------------------ |
| `string`  | default input type |
| `boolean` | true/false values  |
| `number`  | numeric inputs     |

Example:

```yaml
inputs:
  tag:
    type: string
  force:
    type: boolean
  retry_count:
    type: number
```

### 🏗️ **7. Example Using All Input Types**

#### Reusable Workflow

```yaml
on:
  workflow_call:
    inputs:
      version:
        required: true
        type: string
      force_deploy:
        type: boolean
      retries:
        type: number
```

#### Call Workflow

```yaml
uses: ./.github/workflows/reusable.yml
with:
  version: "1.0.2"
  force_deploy: false
  retries: 3
```

### 🎯 **Summary (Cheat Sheet)**

#### ✔ Reusable workflow trigger:

```yaml
on: workflow_call
```

#### ✔ Define inputs:

```yaml
on:
  workflow_call:
    inputs:
      name:
        type: string
        required: true
```

#### ✔ Access inside workflow:

```yaml
${{ inputs.name }}
```

#### ✔ Call reusable workflow:

```yaml
jobs:
  example:
    uses: path/to/workflow.yml
    with:
      name: value
```

## ✅ **1. Container (Top-Level `container:`)**

This runs **all jobs in the workflow** inside a single container image unless overridden.

### Example

```yaml
# .github/workflows/container-top-level.yml
name: Using Container at Workflow Level

on: [push]

# All jobs will run inside this container unless overridden
container: 
  image: python:3.10   # Base Docker image
  env:
    GLOBAL_VAR: "hello"

jobs:
  test:
    runs-on: ubuntu-latest    # Host runner, but job executes inside container above
    steps:
      - uses: actions/checkout@v4
      - run: python --version   # Runs inside python:3.10 container
```

## ✅ **2. Container as Job (`jobs.<job>.container:`)**

Only one job runs in the container; others run normally.

### Example

```yaml
# .github/workflows/container-job.yml
name: Container at Job Level

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: node:18       # Only this job runs inside container
      env:
        NODE_ENV: development

    steps:
      - uses: actions/checkout@v4
      - run: node --version
```

## ✅ **3. Container as Service (`services:`)**

Services are **sidecar containers** (e.g., databases, Redis).
Your job communicates with them via hostname = service name.

### Example

```yaml
# .github/workflows/container-service.yml
name: Container as Service

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      redis:
        image: redis:7
        ports:
          - 6379:6379       # Expose port (optional)
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 5s
          --health-timeout 3s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - run: |
          echo "PING" | nc redis 6379   # Use service hostname = redis
```

## ✅ **4. Communication Between Host Machine and Service Container**

GitHub Actions automatically creates a **Docker network** so the job can reach services via:

### **Service hostname = service name**

Example: `redis:6379`

### Example: Host communicating with service

```yaml
# .github/workflows/host-to-service.yml
name: Host to Service Communication

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: pass
          POSTGRES_DB: testdb
        ports:
          - 5432:5432   # Not required unless external tools need it
        options: >-
          --health-cmd="pg_isready -U user"
          --health-interval=5s
          --health-timeout=3s
          --health-retries=5

    steps:
      - uses: actions/checkout@v4

      # The job runs on host, NOT inside a container
      # but can reach the service using hostname = "postgres"
      - name: Test connection to Postgres
        run: |
          apt-get update && apt-get install -y postgresql-client
          psql -h postgres -U user -d testdb -c "SELECT 'Hello from workflow';"
```

## 📦 **Bonus: Job in a container communicating with a service**

When both job + service use containers:

### Example

```yaml
# .github/workflows/job-container-with-service.yml
name: Job Container + Service

on: [push]

jobs:
  app-test:
    runs-on: ubuntu-latest

    container:
      image: python:3.12   # Job container

    services:
      db:
        image: mysql:8
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: testdb
        ports:
          - 3306:3306

    steps:
      - uses: actions/checkout@v4

      # Inside python container — still uses hostname "db"
      - run: pip install mysqlclient

      - name: Connect from job container to DB container
        run: |
          python - <<EOF
          import MySQLdb
          conn = MySQLdb.connect(host="db", user="root", passwd="root", db="testdb")
          print("Connected:", conn)
          EOF
```

## 🎉 Summary Table

| Feature                    | Key Purpose                     | Hostname                | Scope    |
| -------------------------- | ------------------------------- | ----------------------- | -------- |
| **Top-level `container:`** | All jobs run inside container   | Normal networking       | Workflow |
| **Job container**          | Only that job runs in container | Normal networking       | Job      |
| **Service container**      | Sidecar service (DB, cache)     | hostname = service name | Job      |
| **Communication**          | Host ↔ service                  | use hostname            | Job      |


## A **custom action** in GitHub Actions is a **reusable unit of automation** you create yourself.

You can call it from multiple workflows, multiple repositories, or even publish it publicly.

### ✅ **Types of Custom Actions**

GitHub supports 3 kinds:

#### **1. JavaScript Action**

Runs Node.js code.

#### **2. Docker Action**

Runs inside a container.

#### **3. Composite Action**

Runs a sequence of steps (most common & simplest).

### 🎯 **WHAT IS A CUSTOM ACTION?**

A custom action is a directory containing:

```
action.yml     # action definition file (required)
<optional code or scripts>
```

Then you call it in a workflow like:

```yaml
uses: user/repo/path/to/action@version
```

### 🚀 **EXAMPLE: Composite Custom Action**

This is the most commonly used type.

#### 1️⃣ Create a directory for your action

Inside your repo:

```
.github/actions/say-hello/
    └── action.yml
```

#### 2️⃣ Define the custom action (`action.yml`)

```yaml
# .github/actions/say-hello/action.yml
name: "Say Hello"
description: "Outputs a greeting"
inputs:
  name:
    description: "Name to greet"
    required: true
runs:
  using: "composite"
  steps:
    - name: Greeting
      shell: bash
      run: |
        echo "Hello, ${{ inputs.name }}!"
```

### 💡 **3️⃣ Use the custom action in a workflow**

```yaml
# .github/workflows/test.yml
name: Test Custom Action

on: [push]

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Call the custom action
      - name: Run our custom greeting action
        uses: ./.github/actions/say-hello
        with:
          name: "Alice"
```

#### Output

```
Hello, Alice!
```

### 🐳 **EXAMPLE: Docker Custom Action**

Directory structure:

```
docker-hello/
 ├─ action.yml
 └─ Dockerfile
```

#### `action.yml`

```yaml
name: "Docker Hello"
runs:
  using: "docker"
  image: "Dockerfile"
```

#### `Dockerfile`

```dockerfile
FROM alpine:3.18
CMD echo "Hello from inside a Docker Action"
```

#### Use it

```yaml
- uses: ./docker-hello
```

### 🟦 **EXAMPLE: JavaScript Custom Action**

```
js-hello/
 ├─ action.yml
 └─ index.js
```

#### `action.yml`

```yaml
name: "JS Hello"
runs:
  using: "node20"
  main: "index.js"
```

#### `index.js`

```js
console.log("Hello from JS Action!");
```

#### Use it

```yaml
- uses: ./js-hello
```

### 🧩 **BENEFITS of CUSTOM ACTIONS**

| Benefit            | Why it matters                  |
| ------------------ | ------------------------------- |
| Reuse logic        | Avoid duplicating workflow code |
| Version control    | Pin actions to tags/releases    |
| Share across repos | Centralized automation          |
| Clean workflows    | Keep jobs easy to read          |

### 📦 **PUBLISH a CUSTOM ACTION**


#### 🚀 **Step-by-Step Guide: Create & Publish a Custom GitHub Action**

##### ✅ **STEP 1 — Create a new local project folder for your Action**

> Important: The **action.yml** file must be in the **root folder** — NOT inside `.github/actions`.

```bash
mkdir my-custom-action
cd my-custom-action
```

##### ✅ **STEP 2 — Add your action.yml**

Example minimal composite action:

```yaml
# action.yml
name: "My Custom Greeting Action"
description: "Says hello"
inputs:
  name:
    required: true
    description: "Person to greet"
runs:
  using: "composite"
  steps:
    - run: echo "Hello, ${{ inputs.name }}!"
      shell: bash
```

Or use your own action files (JavaScript, Docker, etc.).

##### ✅ **STEP 3 — Initialize a Git repo**

```bash
git init
```

- ✅ **STEP 4 — Add repository files and commit**

```bash
git add .
git commit -m "Initial commit: Add custom action"
```

##### ✅ **STEP 5 — Create an empty GitHub repository**

Do **NOT** check: *“Add README”*
Do **NOT** check: *“Add .gitignore”*

Then connect it:

```bash
git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-ACTION-REPO>.git
```

Example:

```bash
git remote add origin https://github.com/johndoe/my-custom-action.git
```

##### ✅ **STEP 6 — Tag your Action release**

GitHub Actions **must** be versioned with tags (like `v1`, `v1.0.0`, `v2`, etc.)

```bash
git tag -a v1 -m "First release of my action"
```

List tags:

```bash
git tag
```

##### ✅ **STEP 7 — Push the code AND the tag to GitHub**

```bash
git push origin main
git push origin v1
```

Or if your branch is `master`:

```bash
git push origin master
git push origin v1
```

If you want to push everything at once:

```bash
git push --follow-tags
```

##### 🚀 **STEP 8 — Use your action in ANY other repository**

In ANY workflow in ANY repo:

```yaml
jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Use custom action
        uses: <YOUR-USERNAME>/<YOUR-ACTION-REPO>@v1
        with:
          name: "Alice"
```

Example:

```yaml
uses: johndoe/my-custom-action@v1
```

### ⭐ Optional: Publish to GitHub Marketplace

#### Requirements:

✔ Repo must be **public**
✔ Action must have a **proper README**
✔ `action.yml` must have:

* `name`
* `description`
* `branding:` (icon + color)

Example:

```yaml
branding:
  icon: "terminal"
  color: "blue"
```

Then publish:

1. Go to your action repository
2. Click **Actions** → **Publish to Marketplace**
3. Choose a tag (v1)
4. Confirm publishing

Guide:
[https://docs.github.com/en/actions/creating-actions/publishing-actions-in-github-marketplace#publishing-an-action](https://docs.github.com/en/actions/creating-actions/publishing-actions-in-github-marketplace#publishing-an-action)
