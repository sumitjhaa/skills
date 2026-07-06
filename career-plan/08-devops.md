# ☁️ DevOps / Cloud — Baby Style (8-12 weeks)

**For:** No coding experience. Like systems, servers, tools. Want high salary.

**Time:** 3-4 hrs/day | **Goal:** Junior DevOps / Cloud Engineer

**Pay:** $70-100k | **Difficulty:** Hardest track (but pays best)

---

## What is DevOps?

- Developers write code. DevOps makes it run.
- You handle: servers, deployment, scaling, monitoring, security
- You use: Linux, Docker, Kubernetes, AWS, Terraform
- Fewer entry-level jobs but less competition for them

---

## 🗓️ Week 1 — Linux + Terminal

### Day 1: What is Linux?
- Most servers run Linux. You need to talk to it.
- Terminal = type commands instead of clicking

**Do:** Install Linux in a VM or use WSL (Windows) / use your Mac terminal.

### Day 2: File system
- `ls` = list files
- `cd` = change directory
- `pwd` = where am I?
- `mkdir` = make folder
- `rm` = delete (careful!)

**Do:** Create a folder structure: projects/work/app. Navigate through it.

### Day 3: File operations
- `touch file.txt` = create file
- `cat file.txt` = show contents
- `cp` = copy
- `mv` = move/rename
- `nano file.txt` = edit file

**Do:** Create a file. Write "Hello" in it. Copy it. Rename it.

### Day 4: Permissions + Users
- `chmod 777 file` = make file accessible
- `chown user:group file` = change owner
- `sudo` = do as admin

**Do:** Create a file. Change its permissions. Try to read it as different user.

### Day 5: Processes
- `ps` = running processes
- `top` or `htop` = live view
- `kill PID` = stop process
- `systemctl start nginx` = start a service

**Do:** Run a command. Find its process ID. Kill it.

### Day 6: Bash scripting
- `#!/bin/bash` — script header
- Variables: `NAME="Alex"`, `echo $NAME`
- If/else, for loops

**Do:** Write a script that backs up a folder (copy to backup/ with date).

### Day 7: Git (deep enough)
- `git clone`, `git add`, `git commit`, `git push`, `git pull`
- `git branch`, `git checkout`, `git merge`
- Resolve merge conflicts

**Do:** Clone a repo. Create a branch. Make changes. Merge. Push.

---

## 🗓️ Week 2 — Docker

### Day 1: What is Docker?
- Problem: "It works on my machine but not on the server."
- Docker = package your app + everything it needs into a container
- Container = lightweight virtual machine

**Do:** Install Docker. Run `docker run hello-world`. See it work.

### Day 2: Dockerfile
- Instructions to build a container
```
FROM node:18
COPY . /app
RUN npm install
CMD ["npm", "start"]
```

**Do:** Create a Dockerfile for a simple Node.js app. Build the image.

### Day 3: Docker images vs containers
- Image = recipe. Container = baked cake.
- `docker build -t myapp .` — build image
- `docker run myapp` — run container
- `docker ps` — see running containers

**Do:** Build and run your app in a container. See it serve on localhost.

### Day 4: Docker Compose
- Run multiple containers together (app + database + cache)
- Define in `docker-compose.yml`

**Do:** Create a docker-compose with a web app + PostgreSQL. Start both with one command.

### Day 5: Docker volumes + networking
- Volumes = persistent data (survive container restarts)
- Networks = containers talk to each other

**Do:** Set up a volume for your database. Verify data persists after restart.

### Day 6-7: Docker project
**Do:** Dockerize a full app:
- Frontend (React) → container
- Backend (Node/Express) → container
- PostgreSQL → container
- All connected with docker-compose

---

## 🗓️ Week 3 — Kubernetes

### Day 1: What is Kubernetes (K8s)?
- Docker runs one container. K8s runs MANY containers across MANY servers.
- Auto-restarts if something crashes. Scales up if traffic is high.

**Do:** Run a K8s cluster locally with Minikube or kind.

### Day 2: Pods + Deployments
- Pod = one container (smallest unit)
- Deployment = tells K8s how many pods to run

**Do:** Create a deployment for your app. Run 3 replicas.

### Day 3: Services
- Service = exposes your app (internal or external)
- LoadBalancer = gives it a public IP

**Do:** Create a service for your deployment. Access your app from browser.

### Day 4: ConfigMaps + Secrets
- ConfigMap = config settings (non-sensitive)
- Secret = passwords, API keys (encoded)

**Do:** Store your DB password in a Secret. Use it in your app.

### Day 5: Helm
- Helm = package manager for K8s (like apt for Linux)
- Charts = pre-made K8s configs

**Do:** Install an nginx chart with Helm. Customize it.

### Day 6-7: Practice
- Deploy a full app on K8s (frontend + backend + DB)
- Scale to 5 replicas
- Roll out an update. Rollback.

---

## 🗓️ Week 4 — Cloud (AWS)

### Day 1: What is AWS?
- AWS = Amazon's cloud. Rent servers, databases, storage.
- Most companies use AWS. Skills = valuable.

**Do:** Create AWS free tier account. Set up billing alerts (so you don't accidentally spend money).

### Day 2: EC2 (virtual servers)
- EC2 = rent a Linux server in the cloud
- SSH into it. Install Docker. Run your app.

**Do:** Launch an EC2 instance. SSH in. Run your Docker container.

### Day 3: S3 (file storage)
- S3 = store files (images, backups, website assets)
- Buckets = folders in S3

**Do:** Create a bucket. Upload a file. Make it publicly accessible.

### Day 4: RDS (managed database)
- RDS = PostgreSQL/MySQL without managing the server
- AWS handles backups, updates, failover

**Do:** Create a PostgreSQL RDS instance. Connect your app to it.

### Day 5: IAM (security)
- IAM = users, roles, permissions
- Never use root account. Create users with limited permissions.

**Do:** Create an IAM user. Give it only S3 access. Test that it can't access EC2.

### Day 6-7: VPC (networking)
- VPC = virtual private network in the cloud
- Subnets, security groups, internet gateway

**Do:** Create a VPC with public + private subnets. Put your DB in private subnet (no internet access).

---

## 🗓️ Week 5 — Terraform + CI/CD

### Day 1: What is Terraform?
- Instead of clicking in AWS console, write code to create resources
- "Infrastructure as Code" — version control your servers

**Do:** Install Terraform. Write code to create an S3 bucket. Run `terraform apply`.

### Day 2: Terraform deeper
- Resources, variables, outputs, state files
- Modules = reusable configs

**Do:** Create an EC2 instance + security group with Terraform. Destroy it.

### Day 3: GitHub Actions (CI/CD)
- CI = every time you push code → run tests
- CD = after tests pass → deploy automatically

**Do:** Create a GitHub Action that runs tests on every push.

### Day 4: Deploy pipeline
- Push code → build Docker image → push to registry → deploy to server

**Do:** Full pipeline: git push → build → deploy to EC2.

### Day 5: GitOps (ArgoCD)
- GitOps = your git repo IS your server config
- Change repo → K8s auto-updates

**Do:** Set up ArgoCD. Point it at a GitHub repo. Change repo → see K8s update.

### Day 6-7: Pipeline project
**Do:** End-to-end:
- GitHub repo with app code
- Dockerfile
- GitHub Actions for CI/CD
- Deploy to K8s on AWS
- Terraform for cloud infra

---

## 🗓️ Week 6 — Monitoring + Security

### Day 1: Monitoring (Prometheus + Grafana)
- Prometheus = collects metrics (CPU, memory, requests)
- Grafana = dashboard showing those metrics

**Do:** Install Prometheus + Grafana. See your app's CPU/memory on a dashboard.

### Day 2: Logging (ELK stack)
- Elasticsearch = store logs
- Logstash = collect logs
- Kibana = search logs

**Do:** Set up basic logging for your app. Search for error logs in Kibana.

### Day 3: Security basics
- TLS/SSL = HTTPS (Let's Encrypt — free certs)
- Secrets management = don't store passwords in code (use Vault or AWS Secrets Manager)
- Container scanning (Trivy) — check for vulnerabilities

**Do:** Set up HTTPS for your app. Scan your Docker image for vulnerabilities.

### Day 4-5: Polish portfolio
**Do:** One project showing everything:
- App → Docker → K8s → AWS → Terraform → CI/CD → Monitoring

### Day 6-7: Cert prep
- AWS Cloud Practitioner (entry level cert, ~$100)
- Or Certified Kubernetes Administrator (CKA, ~$300, more valuable)

---

## 🗓️ Week 7-8 — Job Hunt

### Resume keywords:
Docker, Kubernetes, AWS, Terraform, CI/CD, Linux, Bash, Git, GitHub Actions, Prometheus, Grafana

### Roles:
Junior DevOps Engineer, Cloud Engineer, Platform Engineer, Site Reliability Engineer

### Apply:
- LinkedIn, Indeed
- Startups (less strict on years of exp)
- r/devops, DevOps Discord, K8s Slack

---

> ✅ **DevOps is hard but pays best.** If you want "shit ton of money" long term, this is the track. After 2-3 years: $120k+. After 5: $150k+.
