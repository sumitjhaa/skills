# Skills Roadmap — Master Plan

> **Mission:** Top 0.0000001% programmer. Every concept implemented from first principles. Nothing black-boxed.

All skills follow the same pattern: one concept per file, runnable code, practice exercises, integration projects.

> **Status:** `⬜` Not started | `🔄` Building | `✅` Complete

---

**Jump to:**
[Python](#-tier-1--core) · [Machine Learning](#4-machine-learning--ai) · [Languages](#-tier-2--programming-languages) · [CS Foundations](#-tier-3--computer-science-foundations) · [Systems](#-tier-4--systems--infrastructure) · [Specialized Domains](#-tier-5--specialized-domains) · [Paradigms & Practices](#-tier-6--paradigms--practices) · [Math & Science](#-tier-7--math--science-frontier) · [Total Scope](#-total-scope)

---

## 🟢 Tier 1 — Core

### 1. JavaScript / TypeScript — Full-Stack Web
**Target:** ~120 lessons, 10 phases | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Web Foundations (HTML5, CSS3, flexbox, grid, responsive, dev tools) | 8 |
| 02 | JS Core (types, functions, objects, arrays, loops, operators, modules) | 10 |
| 03 | JS Deep (async/await, promises, closures, prototypes, `this`, ES6+) | 12 |
| 04 | DOM & Browser APIs (DOM, events, fetch, localStorage, forms, Web APIs) | 10 |
| 05 | TypeScript Intro (types, interfaces, generics, unions, enums, utility types) | 10 |
| 06 | TypeScript Deep (conditional/mapped/template literal types, declarations) | 10 |
| 07 | React Fundamentals (JSX, components, props, state, hooks) | 14 |
| 08 | React Deep (context, reducers, custom hooks, performance, testing) | 14 |
| 09 | Node.js / Express (APIs, middleware, routing, auth, MongoDB) | 12 |
| 10 | Next.js & Production (SSR, SSG, API routes, auth, deployment, build tools) | 12 |

---

### 2. Python + Frameworks
**Target:** ~491 lessons (100 + 391)  | **Status:** ✅ Complete

| Module | Lessons | Code |
|--------|---------|------|
| Python (core) | ~100 | ~100 |
| Django | 60 | 60 |
| FastAPI | 30 | 30 |
| Flask | 20 | 20 |
| SQLAlchemy | 20 | 20 |
| NumPy + Pandas | 30 | 30 |
| scikit-learn | 30 | 30 |
| PyTorch | 40 | 40 |
| pytest Deep | 15 | 15 |
| Celery | 15 | 15 |
| LangChain | 20 | 20 |
| Playwright | 15 | 15 |
| Pydantic | 10 | 10 |
| Airflow | 20 | 20 |
| **Total** | **~491** | **~491** |

See [`python/`](python/) and [`python-frameworks/`](python-frameworks/).

---

### 3. Go / Systems Programming
**Target:** ~80 lessons, 8 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Go Fundamentals (types, structs, interfaces, packages, tooling) | 12 |
| 02 | Concurrency (goroutines, channels, select, mutexes, sync, patterns) | 10 |
| 03 | Standard Library Deep (HTTP, JSON, I/O, templates, testing) | 10 |
| 04 | HTTP Services (REST, middleware, routing, OpenAPI, gRPC) | 10 |
| 05 | Database & Storage (sqlx, PostgreSQL, migrations, Redis pub/sub) | 8 |
| 06 | CLI & Tooling (Cobra/Viper, CLI design, cross-compilation) | 8 |
| 07 | Production Go (profiling, tracing, logging, graceful shutdown) | 10 |
| 08 | Advanced (generics, reflection, unsafe, WASM, cgo, design patterns) | 10 |

---

### 4. Machine Learning & AI
**Target:** ~371 lessons, 12 phases  | **Status:** ✅ Complete

| Phase | Topic | Lessons | Code |
|-------|-------|---------|------|
| 01 | Linear Algebra | 30 | 30 |
| 02 | Calculus & Optimization | 40 | 40 |
| 03 | Probability & Statistics | 40 | 40 |
| 04 | Information Theory & Advanced Math | 36 | 36 |
| 05 | Classical ML (from scratch) | 55 | 55 |
| 06 | Deep Learning Foundations | 32 | 32 |
| 07 | Advanced Architectures (KAN, Mamba, Diffusion) | 30 | 30 |
| 08 | Computer Vision | 31 | 31 |
| 09 | NLP & LLMs | 30 | 30 |
| 10 | Reinforcement Learning | 20 | 20 |
| 11 | MLOps & Engineering | 16 | 16 |
| 12 | Grand Capstones | 11 | 11 |

See [`machine-learning/`](machine-learning/). Full interconnect at [`machine-learning/INDEX.md`](machine-learning/INDEX.md).

---

## 🟡 Tier 2 — Programming Languages

### 5. Rust
**Target:** ~100 lessons, 10 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Rust Fundamentals (ownership, borrowing, lifetimes, traits, enums, pattern matching) | 12 |
| 02 | Type System Deep (generics, trait bounds, associated types, GATs, HRTB) | 10 |
| 03 | Memory Model (allocators, Box/Rc/Arc, Cell/RefCell, Pin, unsafe, raw pointers) | 10 |
| 04 | Concurrency (Send/Sync, scoped threads, channels, Mutex/RwLock, atomics, rayon) | 10 |
| 05 | Async Rust (Tokio, async/await, futures, streams, async traits, select) | 12 |
| 06 | FFI & Interop (C bindings, `#[no_mangle]`, cbindgen, wasm-bindgen) | 8 |
| 07 | Embedded Rust (no_std, HAL, PAC, RTIC, embassy, display drivers) | 8 |
| 08 | Systems Programming (networking, file systems, OS primitives, io_uring) | 10 |
| 09 | WebAssembly (wasm-pack, wasm-bindgen, web-sys, js-sys, wasi) | 10 |
| 10 | Advanced (macros, proc macros, build scripts, compiler plugins, fuzzing) | 10 |

**Integration theme:** Database engine or game engine

---

### 6. C / C++
**Target:** ~120 lessons, 12 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | C Fundamentals (pointers, memory layout, structs, preprocessor, stdlib) | 12 |
| 02 | C Memory Deep (malloc/free, heap/stack, memory pools, fragmentation) | 10 |
| 03 | C++ Fundamentals (classes, RAII, templates, STL, operator overloading) | 12 |
| 04 | C++ Move Semantics (rvalue references, move constructors, perfect forwarding) | 8 |
| 05 | C++ Templates Deep (SFINAE, CRTP, variadic, constexpr, concepts/C++20) | 10 |
| 06 | C++ Concurrency (threads, async, futures, promises, memory ordering) | 10 |
| 07 | C++ Performance (SIMD, cache optimization, profile-guided, link-time opt) | 10 |
| 08 | Build Systems (CMake, Make, Meson, Ninja, vcpkg, Conan) | 8 |
| 09 | Debugging & Tooling (GDB, Valgrind, Sanitizers, perf, strace, ltrace) | 8 |
| 10 | Linkers & Loaders (symbol resolution, relocation, dynamic linking, PIC) | 8 |
| 11 | Windows Programming (Win32 API, COM, DLLs, MSVC toolchain) | 12 |
| 12 | Real-World C++ (game engines, browsers, compilers, databases) | 12 |

**Integration theme:** Build a real database or game engine

---

### 7. Java / Kotlin
**Target:** ~100 lessons, 10 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Java Fundamentals (OOP, collections, streams, exceptions, I/O) | 12 |
| 02 | JVM Deep (bytecode, classloading, memory model, GC algorithms, JIT) | 10 |
| 03 | Concurrency in Java (threads, synchronized, Locks, CompletableFuture, ForkJoin) | 10 |
| 04 | Enterprise Java (Servlets, JPA/Hibernate, CDI, JMS, JAX-RS) | 12 |
| 05 | Spring Boot (IoC, AOP, REST, security, data, testing, actuator) | 14 |
| 06 | Kotlin (null safety, coroutines, extensions, sealed classes, DSL) | 12 |
| 07 | Android Development (Jetpack Compose, activities, services, Room, WorkManager) | 12 |
| 08 | Big Data Ecosystem (Hadoop, Spark, Kafka, Flink, Cassandra) | 10 |
| 09 | Build & Tooling (Maven, Gradle, Jenkins, Sonar, JUnit, Mockito) | 8 |
| 10 | Production Java (monitoring, profiling, heap dumps, tuning, JMX) | 8 |

**Integration theme:** Microservices platform + Android app

---

### 8. C# / .NET
**Target:** ~80 lessons, 8 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | C# Fundamentals (OOP, LINQ, async/await, generics, records, pattern matching) | 12 |
| 02 | .NET Runtime (CLR, JIT, GC, value/reference types, stack/ heap, Span<T>) | 10 |
| 03 | ASP.NET Core (minimal APIs, MVC, middleware, DI, auth, EF Core) | 14 |
| 04 | Blazor (components, render tree, JS interop, WASM/Server modes) | 8 |
| 05 | Game Dev with Unity (ECS, jobs, burst compiler, scriptable objects) | 12 |
| 06 | F# / Functional .NET (discriminated unions, computation expressions, type providers) | 8 |
| 07 | MAUI / Desktop (cross-platform UI, WinUI, platform-specific APIs) | 8 |
| 08 | Advanced (Unsafe/pointers, source generators, AOT, WinRT interop) | 8 |

**Integration theme:** Desktop app + Unity game + Web API

---

### 9. Swift / iOS
**Target:** ~70 lessons, 7 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Swift Fundamentals (optionals, structs/classes, protocols, generics, closures) | 12 |
| 02 | Swift Advanced (result builders, property wrappers, actors, async/await, macros) | 10 |
| 03 | SwiftUI (views, state, data flow, navigation, animations, previews) | 12 |
| 04 | UIKit (view controller life cycle, auto layout, delegates, collection/table views) | 10 |
| 05 | iOS APIs (Core Data, networking, notifications, background modes, SiriKit) | 8 |
| 06 | Performance & App Store (instruments, profiling, app review, distribution) | 8 |
| 07 | Metal / GPU Programming (shaders, compute, rendering pipeline, ARKit) | 10 |

**Integration theme:** Full-featured iOS app with Metal graphics

---

### 10. Ruby
**Target:** ~40 lessons, 4 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Ruby Fundamentals (blocks, symbols, modules, metaprogramming, duck typing) | 12 |
| 02 | Ruby Metaprogramming (method_missing, define_method, class macros, DSLs) | 8 |
| 03 | Ruby on Rails (MVC, Active Record, migrations, views, testing, Action Cable) | 14 |
| 04 | Ruby Internals (YARV, GC, C extensions, Ractors, Fiber scheduler) | 6 |

---

### 11. PHP
**Target:** ~40 lessons, 4 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | PHP Fundamentals (types, OOP, traits, namespaces, closures, attributes) | 10 |
| 02 | Laravel (IoC, Eloquent, Blade, Artisan, queues, events, broadcasting) | 14 |
| 03 | WordPress (plugin/theme dev, hooks, REST API, block editor, multisite) | 8 |
| 04 | PHP Internals (Zend Engine, opcache, JIT, extensions, HHVM) | 8 |

---

### 12. Scala
**Target:** ~50 lessons, 5 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Scala Fundamentals (case classes, pattern matching, options, implicits) | 10 |
| 02 | Functional Scala (monads, for-comprehensions, type classes, cats/ZIO) | 12 |
| 03 | Scala Type System (path-dependent types, type members, higher-kinded, variance) | 10 |
| 04 | Akka / Distributed (actors, streams, clustering, Akka HTTP) | 10 |
| 05 | Big Data (Spark with Scala, data frames, MLlib, structured streaming) | 8 |

---

### 13. R
**Target:** ~40 lessons, 4 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | R Fundamentals (vectors, data frames, factors, lists, S3/S4 objects) | 10 |
| 02 | Statistical Modeling (lm, glm, mixed models, time series, caret/tidymodels) | 14 |
| 03 | Data Visualization (ggplot2 deep, lattice, shiny, plotly, leaflet) | 8 |
| 04 | R Package Dev (R CMD, testthat, Rcpp, roxygen2, CRAN submission) | 8 |

---

### 14. Haskell / OCaml / F#
**Target:** ~60 lessons, 6 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Pure Functional (purity, laziness, ADTs, pattern matching, type inference) | 12 |
| 02 | Type Systems (Hindley-Milner, GADTs, type families, multi-param type classes) | 10 |
| 03 | Monads Deep (Functor, Applicative, Monad, Monad Transformers, Free Monads) | 10 |
| 04 | Optics (Lens, Prism, Traversal, Iso — van Laarhoven and profunctor) | 8 |
| 05 | Production Haskell (Servant, persistent, testing, profiling, Haskell Tool Stack) | 10 |
| 06 | Dependent Types / Idris / Agda (Dependent pattern matching, theorem proving) | 10 |

**Integration theme:** Implement a production web API + a proof assistant

---

### 15. Prolog / Logic Programming
**Target:** ~20 lessons, 2 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Logic Programming (unification, backtracking, cuts, DCGs, CLP(FD)) | 10 |
| 02 | Advanced (answer set programming, core.logic, miniKanren, Prolog-ML) | 10 |

---

### 16. Assembly (x86, ARM, RISC-V)
**Target:** ~50 lessons, 5 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | x86/x64 (registers, instructions, calling conventions, stack frames, syscalls) | 12 |
| 02 | ARM64 (AArch64, registers, NEON/SIMD, calling convention, Apple Silicon) | 10 |
| 03 | RISC-V (base ISA, extensions, privileged spec, MMU, interrupts) | 10 |
| 04 | Reverse Engineering (disassembly, debugging, anti-debug, obfuscation, patching) | 10 |
| 05 | Exploit Development (buffer overflow, ROP, return-to-libc, heap spray, SEH) | 8 |

---

### 17. WebAssembly
**Target:** ~30 lessons, 3 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | WASM Core (stack machine, linear memory, imports/exports, wat/wast format) | 10 |
| 02 | WASI & System Interface (files, networking, clocks, POSIX interop) | 8 |
| 03 | Production WASM (emscripten, wasm-pack, WASM GC, reference types, component model) | 12 |

---

## 🔵 Tier 3 — Computer Science Foundations

### 18. Operating Systems
**Target:** ~80 lessons, 8 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Processes & Scheduling (PCB, context switch, scheduling algorithms, fork/exec) | 10 |
| 02 | Memory Management (paging, segmentation, TLB, page replacement, MMIO) | 10 |
| 03 | File Systems (inodes, ext4, FAT, NTFS, VFS, journaling, FUSE) | 10 |
| 04 | I/O & Device Drivers (interrupts, DMA, kernel modules, char/block devices) | 10 |
| 05 | Synchronization (spinlocks, mutexes, semaphores, condition variables, futex) | 10 |
| 06 | Networking Stack (socket API, TCP/UDP in kernel, netfilter, eBPF) | 10 |
| 07 | Linux Kernel Deep (syscalls, procfs, cgroups, namespaces, seccomp, LSM) | 10 |
| 08 | Build Your Own Kernel (boot, GDT/IDT, paging, interrupts, syscalls, user mode) | 10 |

**Integration theme:** Build a minimal x86 kernel from scratch

---

### 19. Computer Architecture & Organization
**Target:** ~60 lessons, 6 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Digital Logic (gates, flip-flops, adders, ALU, multiplexers, memory cells) | 10 |
| 02 | CPU Architecture (datapath, control unit, pipelining, hazards, forwarding) | 12 |
| 03 | Memory Hierarchy (caches, associativity, replacement, prefetch, NUMA) | 10 |
| 04 | Instruction-Level Parallelism (superscalar, OoO, branch prediction, speculation) | 8 |
| 05 | SIMD / Vector Processing (AVX, NEON, SVE, GPU warp/wavefront) | 10 |
| 06 | Modern Architectures (ARM vs x86, Apple M-series, RISC-V, CXL, chiplet) | 10 |

**Integration theme:** CPU simulator + cache performance analyzer

---

### 20. Algorithms & Data Structures Deep
**Target:** ~100 lessons, 10 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Asymptotic Analysis (Big-O, amortized, randomized, competitive analysis) | 8 |
| 02 | Sorting & Selection (quickselect, introselect, radix, counting, timsort) | 10 |
| 03 | Trees (BST, AVL, red-black, B-trees, segment trees, Fenwick, tries, suffix) | 12 |
| 04 | Graphs (traversal, shortest paths, MST, max flow, matching, planar) | 14 |
| 05 | Hashing (rolling hash, perfect hash, consistent hash, Cuckoo, locality-sensitive) | 8 |
| 06 | Dynamic Programming (knapsack, edit distance, DP on trees/graphs, bitmask) | 12 |
| 07 | String Algorithms (KMP, Z-algorithm, Manacher, Suffix array/LCP, Aho-Corasick) | 10 |
| 08 | Geometric Algorithms (convex hull, point location, range trees, KD-tree) | 8 |
| 09 | Approximation & Randomized (approx algorithms, Monte Carlo, streaming) | 8 |
| 10 | Advanced (cache-oblivious, succinct data structures, external memory) | 10 |

**Integration theme:** Competitive programming mastery + library implementation

---

### 21. Discrete Mathematics
**Target:** ~50 lessons, 5 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Logic & Proofs (propositional, predicate, induction, contradiction, combinatorial) | 10 |
| 02 | Set Theory & Combinatorics (sets, relations, counting, inclusion-exclusion) | 10 |
| 03 | Number Theory (modular arithmetic, primes, GCD, RSA, Chinese remainder) | 10 |
| 04 | Graph Theory (trees, coloring, Ramsey, extremal, spectral, random graphs) | 10 |
| 05 | Algebraic Structures (groups, rings, fields, lattices, boolean algebra) | 10 |

---

### 22. Compiler Design
**Target:** ~80 lessons, 8 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Lexical Analysis (regex, NFA/DFA, lex/flex, Unicode, tokens) | 8 |
| 02 | Parsing (recursive descent, LL, LR, LALR, PEG, parser combinators) | 12 |
| 03 | Semantic Analysis (symbol table, type checking, overload resolution, name binding) | 10 |
| 04 | Intermediate Representations (AST, IR, SSA, CFG, three-address code) | 8 |
| 05 | Optimization (constant folding, dead code, CSE, loop unrolling, inlining) | 12 |
| 06 | Code Generation (instruction selection, register allocation, scheduling) | 10 |
| 07 | JIT Compilation (tracing JIT, method JIT, tiered compilation, deoptimization) | 10 |
| 08 | Build Your Own Language (full compiler from scratch: source → binary) | 10 |

**Integration theme:** Full compiler for a custom programming language

---

### 23. Formal Verification & Model Checking
**Target:** ~40 lessons, 4 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Propositional Logic & SAT (DPLL, CDCL, resolution, #SAT, MaxSAT) | 10 |
| 02 | SMT Solvers (quantifier-free theories, arrays, bitvectors, Z3 API) | 10 |
| 03 | Model Checking (CTL, LTL, Kripke, SPIN, NuSMV, symbolic model checking) | 10 |
| 04 | Proof Assistants (Coq, Lean, Isabelle/HOL, dependent types, extraction) | 10 |

---

### 24. Computational Complexity Theory
**Target:** ~30 lessons, 3 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Time & Space Complexity (P, NP, PSPACE, EXPTIME, hierarchy theorems) | 12 |
| 02 | NP-Completeness (reductions, Cook-Levin, approximation hardness) | 10 |
| 03 | Advanced Topics (interactive proofs, PCP theorem, circuit complexity, quantum) | 8 |

---

### 25. Programming Language Theory
**Target:** ~50 lessons, 5 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Lambda Calculus (Church encoding, combinators, reduction strategies, Y combinator) | 10 |
| 02 | Type Theory (simply typed, Hindley-Milner, system F, dependent types) | 12 |
| 03 | Operational & Denotational Semantics (small-step, big-step, domain theory) | 10 |
| 04 | Effect Systems (algebraic effects, handlers, monads, effect handlers in practice) | 8 |
| 05 | Substructural Logics (linear, affine, relevant, ordered — Rust borrow checker) | 10 |

---

## 🟣 Tier 4 — Systems & Infrastructure

### 26. Distributed Systems
**Target:** ~80 lessons, 8 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Foundations (CAP, FLP, PACELC, time/clocks, causality, vector clocks) | 10 |
| 02 | Consensus (Paxos, Raft, Zab, PBFT, HotStuff, blockchain consensus) | 12 |
| 03 | Replication (primary-backup, multi-primary, quorum, chain, state machine) | 8 |
| 04 | Distributed Storage (GFS, HDFS, Cassandra, Dynamo, Spanner, Ceph) | 12 |
| 05 | Distributed Compute (MapReduce, Spark, Flink, Ray, Dask) | 10 |
| 06 | Distributed Coordination (ZooKeeper, etcd, Chubby, distributed locks) | 8 |
| 07 | Streaming & Messaging (Kafka deep, Pulsar, NATS, RabbitMQ, ZeroMQ) | 10 |
| 08 | Distributed Transactions (2PC, 3PC, saga, TCC, idempotency, exactly-once) | 10 |

**Integration theme:** Build a distributed key-value store from scratch

---

### 27. Database Internals
**Target:** ~70 lessons, 7 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Storage Engines (B-trees, LSM-trees, append-only, columnar, bitmap) | 12 |
| 02 | Buffer Pool & Caching (page management, replacement, prefetching, mmap) | 8 |
| 03 | Indexing (hash, B+tree, GiST, BRIN, inverted, vector (HNSW, IVF)) | 10 |
| 04 | Query Processing (parser, optimizer, cost estimation, join algorithms, pushdown) | 12 |
| 05 | Transaction Processing (ACID, MVCC, isolation levels, locking, OCC, SSI) | 10 |
| 06 | Recovery & Logging (WAL, ARIES, checkpointing, fuzzy dumps, point-in-time) | 8 |
| 07 | Distributed Databases (sharding, consistent hashing, distributed Joins, HTAP) | 10 |

**Integration theme:** Build a toy SQL database engine from scratch

---

### 28. Performance Engineering
**Target:** ~60 lessons, 6 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Profiling (CPU, memory, I/O, wall-clock, sampling, instrumentation, flamegraphs) | 10 |
| 02 | CPU Optimization (instruction-level, pipelining, branch prediction, cache misses) | 10 |
| 03 | Memory Optimization (allocators, cache lines, false sharing, NUMA, huge pages) | 10 |
| 04 | I/O Optimization (io_uring, AIO, mmap, DMA, SPDK, DPDK) | 10 |
| 05 | Concurrency Optimization (lock-free, wait-free, RCU, hazard pointers, MPMC) | 10 |
| 06 | Benchmarking & Statistics (statistical rigor, warmup, measurement, A/B testing) | 10 |

**Integration theme:** Performance optimization case study (database, web server, game)

---

### 29. Cloud Architecture & Infrastructure
**Target:** ~100 lessons, 10 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | AWS Deep (compute, storage, networking, serverless, databases, AI services) | 16 |
| 02 | GCP Deep (compute, storage, networking, data, ML, Kubernetes) | 12 |
| 03 | Azure Deep (compute, storage, networking, identity, DevOps, AI) | 12 |
| 04 | Multi-Cloud & Abstraction (Terraform + Pulumi + Crossplane + Porter) | 8 |
| 05 | Containers Deep (Docker internals, containerd, runc, cgroups, namespaces) | 10 |
| 06 | Kubernetes Deep (scheduler, controller manager, API, CNI, CSI, admission) | 14 |
| 07 | Service Mesh (Istio, Linkerd, Consul, Envoy, mTLS, traffic management) | 8 |
| 08 | Observability (OpenTelemetry, Prometheus deep, Grafana, Loki, Tempo) | 10 |
| 09 | CI/CD Deep (GitHub Actions, ArgoCD, GitOps, canary, blue-green, feature flags) | 6 |
| 10 | Cost & Security (FinOps, IAM deep, policy as code, secrets, compliance) | 4 |

---

## 🟠 Tier 5 — Specialized Domains

### 30. Computer Graphics
**Target:** ~80 lessons, 8 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Rendering Pipeline (rasterization, transformations, clipping, z-buffer) | 10 |
| 02 | Shaders (vertex, fragment, compute, geometry, tessellation, ray tracing) | 12 |
| 03 | Lighting & Materials (Phong, PBR, subsurface scattering, ambient occlusion) | 10 |
| 04 | Ray Tracing (Whitted, path tracing, bidirectional, photon mapping, denoising) | 10 |
| 05 | Geometry Processing (meshes, subdivision, Boolean, simplification, parameterization) | 10 |
| 06 | Animation (skeletal, blend shapes, skinning, IK, physics, cloth, fluids) | 10 |
| 07 | GPU Architecture (CUDA, warp scheduling, shared memory, tensor cores) | 8 |
| 08 | Real-Time Graphics (OpenGL/Vulkan, deferred shading, LOD, streaming) | 10 |

**Integration theme:** Software renderer + real-time 3D engine

---

### 31. Cryptography
**Target:** ~50 lessons, 5 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Symmetric (AES, ChaCha20, block ciphers, modes, padding, AEAD) | 10 |
| 02 | Asymmetric (RSA, ECC, DH, ECDH, Ed25519, post-quantum, Kyber) | 12 |
| 03 | Hash Functions (SHA-2/3, BLAKE, Merkle trees, SMT, polynomial commitments) | 8 |
| 04 | Protocols (TLS 1.3, Signal, Noise, OPAQUE, PAKE, secure enclaves) | 10 |
| 05 | Zero-Knowledge Proofs (SNARKs, STARKs, Bulletproofs, circom, bellman) | 10 |

**Integration theme:** Implement a cryptographic protocol from scratch

---

### 32. Robotics
**Target:** ~60 lessons, 6 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Kinematics & Dynamics (forward/inverse, Jacobian, Euler-Lagrange, ROS 2) | 12 |
| 02 | Control Theory (PID, LQR, MPC, adaptive, robust, nonlinear) | 12 |
| 03 | Perception (sensor fusion, Kalman, SLAM, point clouds, object detection) | 12 |
| 04 | Planning (RRT, A*, CHOMP, STOMP, trajectory optimization) | 8 |
| 05 | Manipulation (grasping, force control, impedance, dexterous manipulation) | 8 |
| 06 | Locomotion (walking, running, balance, MPC for quadrupeds, bipeds) | 8 |

---

### 33. AR / VR / Spatial Computing
**Target:** ~50 lessons, 5 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Spatial Math (quaternions, transformation matrices, coordinate systems) | 8 |
| 02 | Rendering for XR (stereoscopic, foveated, reprojection, pass-through) | 10 |
| 03 | Tracking (SLAM, VIO, inside-out, eye tracking, hand tracking) | 12 |
| 04 | Interaction (raycasting, hand gestures, gaze, haptics, spatial UI) | 10 |
| 05 | Platforms (ARKit, ARCore, OpenXR, WebXR, Unity XR Toolkit) | 10 |

---

### 34. Game Engine Development
**Target:** ~60 lessons, 6 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | ECS Architecture (entities, components, systems, archetypes, chunks) | 10 |
| 02 | Game Loop & Physics (fixed timestep, interpolation, broad/narrow phase, constraint) | 12 |
| 03 | Audio (DSP, mixing, spatial audio, FMOD/Wwise integration, MIDI) | 8 |
| 04 | Networking for Games (replication, prediction, reconciliation, rollback, lobbies) | 10 |
| 05 | Tools & Pipeline (asset pipeline, serialization, hot reload, debug UI) | 10 |
| 06 | Full Engine (renderer + physics + audio + tools + networking) | 10 |

**Integration theme:** Build a complete 2D/3D game engine

---

### 35. Audio / DSP Programming
**Target:** ~40 lessons, 4 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Digital Signal Processing (sampling, Fourier, filters, convolution, modulation) | 12 |
| 02 | Audio Synthesis (oscillators, envelopes, FM, granular, physical modeling) | 10 |
| 03 | Audio Effects (reverb, delay, chorus, compression, EQ, distortion) | 8 |
| 04 | Real-Time Audio (JUCE, PortAudio, ASIO, MIDI, plugin dev, VST/AU) | 10 |

---

### 36. Computer Networks Deep
**Target:** ~60 lessons, 6 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Physical & Link Layer (Ethernet, WiFi, switching, ARP, VLAN, STP) | 10 |
| 02 | IP & Routing (IPv4/IPv6, OSPF, BGP, MPLS, segment routing, VXLAN) | 12 |
| 03 | Transport (TCP deep, QUIC, SCTP, DCCP, congestion control algorithms) | 10 |
| 04 | HTTP & Web (HTTP/1.1, HTTP/2, HTTP/3, WebSockets, WebTransport, CDN) | 10 |
| 05 | DNS & Load Balancing (DNS deep, Anycast, global load balancing, DoH/DoT) | 8 |
| 06 | Network Security (IPsec, WireGuard, TLS deep, DDoS mitigation, WAF) | 10 |

---

### 37. FinTech & Trading Systems
**Target:** ~40 lessons, 4 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Market Microstructure (order types, matching engines, L2 data, dark pools) | 10 |
| 02 | Low-Latency Systems (kernel bypass, DPDK, FPGA, nanosecond optimization) | 12 |
| 03 | Trading Strategies (market making, arbitrage, momentum, stat arb, HFT) | 10 |
| 04 | Risk & Compliance (VaR, stress testing, position keeping, regulation) | 8 |

---

### 38. Bioinformatics / Computational Biology
**Target:** ~40 lessons, 4 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Sequence Analysis (alignment, BLAST, HMMER, assembly, phylogenetics) | 12 |
| 02 | Structural Biology (protein folding, molecular dynamics, docking, AlphaFold) | 10 |
| 03 | Genomics (variant calling, GWAS, transcriptomics, single-cell, epigenomics) | 10 |
| 04 | Systems Biology (network inference, ODE modeling, constraint-based, Boolean) | 8 |

---

## 🟤 Tier 6 — Paradigms & Practices

### 39. Software Architecture & Design Patterns
**Target:** ~60 lessons, 6 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | SOLID & Principles (single responsibility, open/closed, Liskov, DI) | 8 |
| 02 | Creational Patterns (factory, builder, singleton, prototype, abstract factory) | 8 |
| 03 | Structural Patterns (adapter, bridge, composite, decorator, facade, proxy) | 8 |
| 04 | Behavioral Patterns (observer, strategy, command, state, visitor, mediator) | 10 |
| 05 | Architecture Patterns (layered, hexagonal, CQRS, event sourcing, DDD) | 14 |
| 06 | Enterprise Patterns (saga, outbox, throttling, circuit breaker, retry, bulkhead) | 12 |

---

### 40. API Design
**Target:** ~40 lessons, 4 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | REST Deep (resources, HATEOAS, versioning, pagination, caching, idempotency) | 10 |
| 02 | GraphQL (schema, resolvers, N+1, subscriptions, federation, Apollo) | 10 |
| 03 | gRPC & Protobuf (services, streams, interceptors, gateway, grpc-web) | 10 |
| 04 | API Security (OAuth 2.1, OIDC, JWT, API keys, rate limiting, CORS) | 10 |

---

### 41. Developer Experience & Tooling
**Target:** ~40 lessons, 4 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Editor Deep (VS Code extensions, LSP, DAP, tree-sitter, snippets) | 10 |
| 02 | Git Deep (internals, hooks, rebase, bisect, worktrees, submodules, large files) | 10 |
| 03 | Dev Containers & Environments (Docker dev, nix, devbox, direnv, taskfile) | 10 |
| 04 | Build & Package Systems (npm/pip/cargo/go - package lifecycle, registries, CI) | 10 |

---

### 42. UI/UX Design
**Target:** ~30 lessons, 3 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Design Principles (color, typography, layout, hierarchy, accessibility, Figma) | 12 |
| 02 | Interaction Design (user research, wireframes, prototypes, usability testing) | 10 |
| 03 | Design Systems (component libraries, tokens, theming, documentation) | 8 |

---

## ⚫ Tier 7 — Math & Science Frontier

### 43. Quantum Computing
**Target:** ~40 lessons, 4 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Qubits & Gates (superposition, measurement, entanglement, Bloch sphere) | 10 |
| 02 | Quantum Algorithms (Deutsch-Jozsa, Grover, Shor, QFT, HHL, VQE) | 12 |
| 03 | Quantum Hardware (superconducting, trapped ion, photonic, error correction) | 8 |
| 04 | Quantum Programming (Qiskit, Cirq, PennyLane, Q#, quantum ML) | 10 |

---

### 44. Computational Physics
**Target:** ~40 lessons, 4 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Numerical Methods (ODE, PDE, finite difference, FEM, Monte Carlo) | 12 |
| 02 | Classical Mechanics (N-body, molecular dynamics, lattice Boltzmann) | 10 |
| 03 | Electromagnetics & Optics (FDTD, ray tracing, Maxwell solvers) | 8 |
| 04 | Quantum Mechanics (Schrödinger solver, DFT, tight-binding, tensor networks) | 10 |

---

### 45. Formal Languages & Automata Theory
**Target:** ~30 lessons, 3 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Regular Languages (DFA, NFA, regex, pumping lemma, Myhill-Nerode) | 10 |
| 02 | Context-Free Languages (CFG, PDA, parse trees, Chomsky normal form, CYK) | 10 |
| 03 | Turing Machines & Computability (decidability, halting problem, reductions) | 10 |

---

### 46. Category Theory for Programmers
**Target:** ~30 lessons, 3 phases  | **Status:** ⬜

| Phase | Topic | Lessons |
|-------|-------|---------|
| 01 | Categories & Functors (objects, morphisms, functors, natural transformations) | 10 |
| 02 | Universal Constructions (products, coproducts, limits, colimits, adjunctions) | 10 |
| 03 | Monads & Algebras (monads, Kleisli, Eilenberg-Moore, F-algebras, recursion schemes) | 10 |

---

## 📊 Total Scope

| Category | Topics | Est. Lessons |
|----------|--------|-------------|
| **✅ Complete** | 2 (Python + Frameworks, ML/AI) | ~862 |
| **⬜ Planned** | 44 topics | ~2,500+ |
| **Grand Total** | **46 subjects** | **~3,400+** |

```
Python + Frameworks  ── DONE ✅ (491 lessons)
Machine Learning      ── DONE ✅ (371 lessons)

Next priority:
  JavaScript/TS       ── ~120  (web foundation)
  C/C++               ── ~120  (systems foundation)
  Rust                ── ~100  (modern systems)
  OS                  ── ~80   (kernel from scratch)
  Algorithms Deep     ── ~100  (interview + mastery)
  Distributed Systems ── ~80   (senior/staff level)
  Database Internals  ── ~70   (build your own DB)
  Compiler Design     ── ~80   (build your own language)
```

Each topic is a standalone `skills/<topic>/` directory with lessons, code, practice, and INDEX.
