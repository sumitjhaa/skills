# Skills Roadmap — Master Plan

All skills follow the same pattern: one concept per file, runnable code, practice exercises, integration projects.

> **Status:** `⬜` Not started | `🔄` Building | `✅` Complete

---

## 🟢 Tier 1 — Core (Foundation for everything else)

### 1. JavaScript / TypeScript — Full-Stack Web
**Prerequisites:** None (standalone)
**Difficulty:** Beginner → Advanced
**Target:** ~120 lessons, 10 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Web Foundations | 8 | HTML5, CSS3, box model, flexbox, grid, responsive, dev tools |
| 02 | JS Core | 10 | Variables, types, functions, objects, arrays, loops, operators |
| 03 | JS Deep | 12 | Async/await, promises, closures, prototypes, `this`, modules, ES6+ features |
| 04 | DOM & Browser APIs | 10 | DOM manipulation, events, fetch, localStorage, forms, Web APIs |
| 05 | TypeScript Intro | 10 | Types, interfaces, generics, unions, enums, utility types |
| 06 | TypeScript Deep | 10 | Advanced generics, conditional/mapped/template literal types, declarations |
| 07 | React Fundamentals | 14 | JSX, components, props, state, hooks (useState, useEffect, useRef) |
| 08 | React Deep | 14 | Context, reducers, custom hooks, performance, error boundaries, testing |
| 09 | Node.js / Express | 12 | APIs, middleware, routing, auth, MongoDB/Mongoose, file uploads |
| 10 | Next.js & Production | 12 | SSR, SSG, API routes, middleware, auth, deployment (Vercel), build tools |

**Integration theme:** Full-stack SaaS dashboard (React + Next.js + Node)

---

### 2. Django Backend
**Prerequisites:** Python skill
**Difficulty:** Intermediate → Advanced
**Target:** ~90 lessons, 10 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Django Basics | 10 | Project setup, models, admin, views, templates, URLs, static files |
| 02 | Django ORM Deep | 10 | Queries, aggregation, F/Q expressions, migrations, relationships |
| 03 | Auth & Users | 8 | User model, permissions, groups, sessions, JWT, social auth |
| 04 | Django REST Framework | 10 | Serializers, viewsets, routers, permissions, filtering, pagination |
| 05 | Advanced DRF | 8 | Custom auth, throttling, versioning, HATEOAS, OpenAPI schema |
| 06 | Async Django | 10 | Celery, Redis, Channels, WebSockets, async views, background tasks |
| 07 | Forms & HTMX | 8 | Django forms, class-based views, HTMX, Alpine.js, django-crispy-forms |
| 08 | Testing | 8 | pytest-django, factories (factory_boy), DRF testing, coverage |
| 09 | Advanced Patterns | 8 | Signals, middleware, custom commands, caching, i18n/l10n, sitemaps |
| 10 | Production | 10 | Docker, Gunicorn, Nginx, cloud deploy, CI/CD, monitoring, logging |

**Integration theme:** Full SaaS product (multi-tenant, subscription, Stripe)

---

### 3. Go / Systems Programming
**Prerequisites:** Any programming language
**Difficulty:** Intermediate → Advanced
**Target:** ~80 lessons, 8 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Go Fundamentals | 12 | Variables, types, functions, structs, interfaces, packages |
| 02 | Concurrency | 10 | Goroutines, channels, select, mutexes, sync primitives, patterns |
| 03 | Standard Library Deep | 10 | HTTP server/client, JSON, file I/O, templates, testing |
| 04 | HTTP Services | 10 | REST APIs, middleware, routing (chi/stdlib), OpenAPI, gRPC |
| 05 | Database & Storage | 8 | SQL with sqlx, PostgreSQL, migrations, Redis pub/sub |
| 06 | CLI & Tooling | 8 | Cobra/Viper, CLI design, cross-compilation, build tooling |
| 07 | Production Go | 10 | Profiling, tracing, structured logging, graceful shutdown, benchmarking |
| 08 | Advanced Topics | 10 | Generics, reflection, unsafe, WASM, cgo, design patterns |

**Integration theme:** Distributed task runner / message broker

---

## 🟡 Tier 2 — Specializations (Pick based on career path)

### 4. Machine Learning & AI
**Prerequisites:** Python, NumPy, Pandas basics
**Difficulty:** Advanced
**Target:** ~90 lessons, 9 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Math Foundations | 10 | Linear algebra, calculus, probability, statistics (with Python) |
| 02 | ML Fundamentals | 10 | scikit-learn, supervised/unsupervised, train/test split, metrics |
| 03 | Classical ML | 10 | Regression, classification, clustering, ensembles, SVMs, PCA |
| 04 | Deep Learning | 12 | PyTorch, neural networks, backpropagation, CNNs, RNNs, LSTMs |
| 05 | Natural Language Processing | 10 | Tokenization, embeddings, transformers, BERT, attention mechanism |
| 06 | LLMs & GenAI | 12 | Prompt engineering, RAG, fine-tuning, LangChain, vector databases |
| 07 | Computer Vision | 10 | Image processing, CNNs, object detection (YOLO), segmentation |
| 08 | MLOps | 10 | Model deployment, monitoring, A/B testing, feature stores, drift detection |
| 09 | Responsible AI | 6 | Bias, fairness, explainability (SHAP, LIME), privacy, security |

**Integration theme:** Multi-modal AI assistant with RAG

---

### 5. Data Engineering
**Prerequisites:** Python, SQL basics
**Difficulty:** Advanced
**Target:** ~70 lessons, 7 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | SQL Deep | 10 | Window functions, CTEs, recursive queries, query optimization, indexes |
| 02 | Python Data Stack | 12 | Pandas deep, PySpark, data validation (Great Expectations), Dask |
| 03 | Data Modeling | 8 | Star schema, snowflake, slowly changing dimensions, fact tables, ERDs |
| 04 | ETL/ELT Pipelines | 12 | Airflow (DAGs, operators, sensors), dbt (models, tests, docs), Dagster |
| 05 | Streaming | 10 | Kafka (producers, consumers, topics, connect), Flink, Kinesis |
| 06 | Data Warehouses | 10 | Snowflake/BigQuery/Redshift, partitioning, clustering, materialized views |
| 07 | Production Data Engineering | 8 | Data quality, lineage, orchestration, cost optimization, monitoring |

**Integration theme:** Real-time analytics pipeline (Kafka → Spark → Snowflake → dbt)

---

### 6. DevOps & Cloud Engineering
**Prerequisites:** At least one deployed application
**Difficulty:** Advanced
**Target:** ~90 lessons, 8 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Linux Deep | 10 | File system, processes, networking, shell scripting, systemd, permissions |
| 02 | AWS / Cloud Core | 14 | EC2, S3, RDS, VPC, IAM, Lambda, CloudWatch, Route53 |
| 03 | Infrastructure as Code | 12 | Terraform (resources, modules, state, workspaces, remote backends) |
| 04 | Docker Deep | 10 | Multi-stage builds, networking, volumes, security, Compose, registries |
| 05 | Kubernetes | 14 | Pods, deployments, services, ingresses, ConfigMaps, Helm, operators |
| 06 | CI/CD & GitOps | 10 | GitHub Actions advanced, ArgoCD, GitOps, canary/blue-green deployments |
| 07 | Observability | 10 | Prometheus, Grafana, Loki, Tempo, OpenTelemetry, structured logging |
| 08 | Security & Compliance | 10 | Secrets management, network policies, IAM, audit, SOC2, incident response |

**Integration theme:** Production-grade microservices platform with monitoring

---

### 7. System Design
**Prerequisites:** Built and deployed at least one real app
**Difficulty:** Advanced
**Target:** ~50 lessons, 6 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Foundations | 8 | CAP theorem, consistency models, latency/throughput, trade-offs |
| 02 | Data Storage | 10 | SQL vs NoSQL, sharding, replication, indexing, caching (Redis deep) |
| 03 | Communication | 8 | REST, GraphQL, gRPC, message queues (Kafka, RabbitMQ), event-driven |
| 04 | Microservices | 10 | Service decomposition, API gateways, circuit breakers, service mesh |
| 05 | Scalability | 8 | Load balancing, CDN, horizontal scaling, rate limiting, backpressure |
| 06 | Real-World Systems | 6 | Design: URL shortener, chat, Twitter, YouTube, Uber, Netflix |

**Integration theme:** Design portfolio with 10 system designs

---

### 8. Mobile Development (React Native)
**Prerequisites:** JavaScript/TypeScript skill
**Difficulty:** Intermediate → Advanced
**Target:** ~60 lessons, 6 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | React Native Basics | 12 | Components, navigation, styling, platform APIs, Expo |
| 02 | State & Data | 10 | State management, async storage, REST APIs, GraphQL clients |
| 03 | Native Features | 10 | Camera, location, notifications, biometrics, file system |
| 04 | Performance & Polish | 8 | Animation (Reanimated), gestures, lists, profiling, accessibility |
| 05 | Stores & Auth | 10 | App Store/Play Store, in-app purchases, auth flows, deep linking |
| 06 | Production | 10 | Testing, CI/CD, crash reporting, analytics, app updates |

**Integration theme:** Full-featured social media app

---

## 🔴 Tier 3 — Niche / Advanced (Optional, high-value in specific domains)

### 9. Cybersecurity
**Prerequisites:** Networking basics, any programming language
**Difficulty:** Advanced
**Target:** ~60 lessons, 6 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Foundations | 8 | Threat modeling, CIA triad, cryptography basics, risk assessment |
| 02 | Network Security | 10 | Firewalls, VPNs, IDS/IPS, Wireshark, nmap, protocols |
| 03 | Web Application Security | 12 | OWASP Top 10, SQL injection, XSS, CSRF, SSRF, auth bypass |
| 04 | Penetration Testing | 10 | Metasploit, Burp Suite, exploit development, bug bounty methodology |
| 05 | Defensive Security | 10 | SIEM (Splunk/ELK), incident response, forensics, malware analysis |
| 06 | Cloud & DevSecOps | 10 | Cloud security (AWS/GCP), SAST/DAST, secrets scanning, compliance |

**Integration theme:** Security audit + penetration test of a sample web app

---

### 10. Data Analytics & Visualization
**Prerequisites:** Python, SQL basics
**Difficulty:** Intermediate
**Target:** ~50 lessons, 5 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Analytics Foundations | 8 | Metrics, KPIs, funnel analysis, cohort analysis, A/B testing |
| 02 | SQL for Analytics | 10 | Advanced SQL, window functions, retention/cohort queries, funnel queries |
| 03 | Python Analytics | 12 | Pandas deep, exploratory data analysis, statistical testing |
| 04 | Visualization | 10 | Matplotlib, Seaborn, Plotly, Dash, Tableau basics |
| 05 | Dashboarding & Reporting | 10 | Metabase, Superset, automated reporting, data storytelling |

**Integration theme:** Complete analytics suite (dashboard + automated reports)

---

### 11. QA Automation & Software Testing
**Prerequisites:** Any programming language
**Difficulty:** Intermediate
**Target:** ~50 lessons, 5 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Testing Foundations | 8 | Testing pyramid, test types, test design, TDD/BDD |
| 02 | Unit & Integration Testing | 10 | pytest deep, mocking, fixtures, parametrization, coverage |
| 03 | API Testing | 10 | REST/GraphQL testing, Postman/Newman, contract testing (Pact) |
| 04 | UI Automation | 12 | Playwright, Cypress, Selenium, page objects, visual testing |
| 05 | Performance & Load Testing | 10 | k6, Locust, JMeter, stress testing, bottleneck identification |

**Integration theme:** Complete test suite for a web application (API + UI + performance)

---

### 12. Networking Deep
**Prerequisites:** Operating systems basics
**Difficulty:** Advanced
**Target:** ~40 lessons, 4 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Foundations | 10 | OSI model, TCP/IP, UDP, DNS, HTTP/2, HTTP/3, WebSockets |
| 02 | Protocols Deep | 12 | TCP deep (flow control, congestion), TLS/SSL, QUIC, BGP, DHCP |
| 03 | Tools & Analysis | 8 | Wireshark, tcpdump, iperf, nmap, traceroute, netstat |
| 04 | Production Networking | 10 | Load balancers, proxies (Nginx, HAProxy), CDN, SDN, network policy |

**Integration theme:** Network analysis and optimization for a web service

---

### 13. Database Administration
**Prerequisites:** SQL basics
**Difficulty:** Advanced
**Target:** ~50 lessons, 5 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | PostgreSQL Deep | 14 | Architecture, configuration, indexing, vacuum, performance tuning |
| 02 | MySQL Deep | 10 | Architecture, replication, InnoDB, query optimization, partitioning |
| 03 | MongoDB Deep | 10 | Aggregation pipeline, indexing strategies, replication, sharding |
| 04 | Redis Deep | 8 | Data structures, persistence, clustering, caching patterns |
| 05 | Production DBA | 8 | Backup/restore, migration, high availability, monitoring, security |

**Integration theme:** Multi-DB production system design and optimization

---

### 14. Game Development
**Prerequisites:** Any OOP language
**Difficulty:** Advanced
**Target:** ~50 lessons, 5 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | PyGame / Python Games | 10 | Game loop, sprites, collision, input handling, sound |
| 02 | Godot Engine | 12 | Scenes, nodes, GDScript, signals, physics, 2D games |
| 03 | Unity / C# | 12 | Game objects, components, physics, scripting, 3D basics |
| 04 | Game Design & Art | 8 | Level design, UI/UX, pixel art, animation fundamentals |
| 05 | Production & Publishing | 8 | Optimization, multiplayer, Steam/App Store, analytics |

**Integration theme:** Complete 2D platformer game

---

### 15. Embedded Systems & IoT
**Prerequisites:** C or Python, electronics basics helpful
**Difficulty:** Advanced
**Target:** ~40 lessons, 4 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | MicroPython & CircuitPython | 10 | GPIO, PWM, ADC, I2C, SPI, UART, sensors |
| 02 | Raspberry Pi | 10 | GPIO, camera, display, networking, Linux on Pi, automation |
| 03 | Arduino / C++ | 10 | Digital/analog I/O, interrupts, timers, serial, motors |
| 04 | IoT Protocols & Cloud | 10 | MQTT, CoAP, HTTP, AWS IoT, ESP32, LoRaWAN, home automation |

**Integration theme:** Smart home system (sensors + cloud + dashboard)

---

### 16. Technical Writing & Documentation
**Prerequisites:** Any technical background
**Difficulty:** Beginner → Intermediate
**Target:** ~30 lessons, 3 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Writing Fundamentals | 10 | Audience, structure, clarity, conciseness, grammar for tech |
| 02 | Documentation Types | 10 | API docs, tutorials, how-tos, reference, READMEs, changelogs |
| 03 | Tools & Publishing | 10 | Markdown deep, Docusaurus, ReadTheDocs, OpenAPI/Swagger, diagrams |

**Integration theme:** Complete documentation suite for an open-source project

---

### 17. Open Source Contribution & Maintenance
**Prerequisites:** Any programming language, git
**Difficulty:** Intermediate
**Target:** ~20 lessons, 2 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Contributing | 10 | Finding projects, reading codebases, PR workflow, code review, communication |
| 02 | Maintaining | 10 | Releases, CI/CD for OSS, community management, governance, licensing |

**Integration theme:** Contribute to and maintain one real open-source project

---

### 18. Blockchain & Web3
**Prerequisites:** JavaScript, some cryptography basics
**Difficulty:** Advanced
**Target:** ~40 lessons, 4 phases
**Status:** ⬜

| Phase | Topic | Lessons | Key Content |
|-------|-------|---------|-------------|
| 01 | Blockchain Fundamentals | 10 | Consensus, mining, wallets, transactions, gas, Ethereum |
| 02 | Smart Contracts | 12 | Solidity, EVM, ERC20, ERC721, Hardhat, testing, security |
| 03 | dApp Development | 10 | ethers.js, web3.js, frontend integration, The Graph, IPFS |
| 04 | Production Web3 | 8 | DeFi, oracles (Chainlink), Layer 2, audit, deployment |

**Integration theme:** Full dApp (NFT marketplace or DeFi protocol)

---

## Dependency Map

```
JavaScript/TS  ─┬→ React Native (Mobile)
                ├→ Next.js (Web)
                └→ Blockchain/Web3 (if +crypto)

Python (done)  ─┬→ Django Backend
                ├→ ML/AI (if +math)
                ├→ Data Engineering (if +SQL)
                └→ Embedded/IoT (if +hardware)

DevOps/Cloud   ─┬→ K8s deep
                ├→ Security (if +networking)
                └→ Database Admin (if +DB)

Any language   ─→ QA Automation
                  → System Design
                  → Technical Writing
                  → Open Source
```

---

## Recommended Build Order

```
1. JavaScript/TypeScript  ← start here (enables web dev)
2. Django Backend         ← full-stack with Python
3. DevOps & Cloud         ← now you can deploy
4. System Design          ← now you can architect
5. ML/AI or Data Eng      ← choose your path
6. Mobile or Security     ← expand your reach
```

Each skill is a standalone `skills/<topic>/` directory with the same structure as `python/`.

---

**To prioritize:** Pick the first skill you want built. I'll start with phase 1 fleshed out (all lesson files + code + practice), exactly like the Python skill.
