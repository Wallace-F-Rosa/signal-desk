# DevOps Study Guide: Signal Desk

## How to use this guide

This is an open-ended learning path for a developer who can already work with Git/GitHub, Angular, FastAPI, and basic shell commands. Plan for roughly 3-5 hours per week.

The goal is not to memorize tools. The goal is to understand how a change moves from source code to a running, observable, recoverable service.

Use this loop for every milestone:

1. Learn the concept.
2. Apply it to Signal Desk.
3. Break something deliberately.
4. Diagnose the failure.
5. Write down what evidence led to the fix.

The examples below are deliberately small. They show mechanisms, not complete production configuration.

## Target system

The initial system has one communication path:

```text
User
  |
  v
Angular signal-interface --HTTP/REST--> FastAPI message-service --SQL--> PostgreSQL
```

The system should eventually be packaged and operated as separate components:

- `signal-interface`: browser-facing frontend
- `message-service`: API and business logic
- `postgres`: persistent data store

The first useful feature can be very small: submit a message through the Angular interface, send it to FastAPI, store it in PostgreSQL, and display the response.

### What you should be able to explain

By the end, explain what happens when:

- a browser request reaches the API;
- the API cannot reach PostgreSQL;
- a container exits;
- a Kubernetes Pod is unhealthy;
- a deployment needs to be rolled back;
- a commit passes CI but is not released;
- a released service produces errors in production.

---

## Milestone 0: Establish the mental model

### Learn

DevOps is a set of practices for delivering and operating software reliably. Study these ideas before focusing on tools:

- feedback loops and small changes;
- automation and repeatability;
- versioned configuration;
- shared responsibility between development and operations;
- reliability, security, and cost as design concerns;
- immutable artifacts versus manually changed servers.

### Minimal example

A delivery flow can be represented as:

```text
commit -> review -> test -> build artifact -> publish -> deploy -> observe -> improve
```

A deployment is not complete merely because the process returned success. You also need evidence that the service is healthy.

### Signal Desk outcome

Write a one-page description of the three components, their responsibilities, and the first REST use case. Draw the request path and identify where data is transient versus persistent.

### Checkpoint

Can you name the owner of each responsibility and explain why the browser should not connect directly to PostgreSQL?

---

## Milestone 1: Linux, networking, and troubleshooting foundations

### Learn

Focus on the parts of Linux and networking that explain runtime behavior:

- files, permissions, processes, signals, and exit codes;
- standard input, output, and error;
- services and environment variables;
- ports, localhost, IP addresses, DNS, and HTTP;
- TLS, certificates, and the difference between encryption and authentication;
- timeouts, retries, and connection refusal.

Useful commands to understand, not blindly memorize:

```bash
pwd
ps aux
curl -i http://localhost:8000/health
ss -ltn
```

`curl` makes an HTTP request, `ss` shows listening TCP sockets, and `ps` shows processes. Together they help distinguish an application problem from a network or process problem.

### Signal Desk outcome

Run a minimal local API and inspect its process and listening port. Use `curl` to compare a successful request, a wrong path, and a stopped service.

### Checkpoint

For each symptom, state the next piece of evidence you would collect:

- connection refused;
- request timeout;
- HTTP 404;
- HTTP 500.

---

## Milestone 2: HTTP and REST as an operational contract

### Learn

Study methods, status codes, headers, JSON, idempotency, validation, pagination, and error responses. Also learn why API contracts should be explicit and versioned.

### Minimal example

A request might look like:

```http
POST /messages HTTP/1.1
Content-Type: application/json

{"text":"hello"}
```

A successful response could be:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{"id":42,"text":"hello"}
```

The status code and response shape are part of the contract. A client should not need to parse human-readable log messages to know whether a request succeeded.

### Signal Desk outcome

Define a small API contract before writing code:

- `GET /health` for process health;
- `GET /ready` for dependency readiness;
- `POST /messages` to create a message;
- `GET /messages` to list messages;
- consistent validation and error responses.

### Checkpoint

Explain why `/health` and `/ready` should not necessarily return the same result when PostgreSQL is unavailable.

---

## Milestone 3: Database and service boundaries

### Learn

Study relational modeling, indexes, transactions, connection pools, migrations, backups, and least-privilege database users. Learn why schema changes must be repeatable and tracked in version control.

### Minimal example

The service boundary should be:

```text
Angular -> FastAPI endpoint -> service logic -> database access -> PostgreSQL
```

The frontend knows the API contract. It does not know SQL credentials or database tables.

A transaction conceptually groups changes:

```text
begin -> validate -> write -> commit
                    \-> rollback on failure
```

### Signal Desk outcome

Design a `messages` table with an identifier, message text, creation time, and any status needed by the first feature. Decide which fields are required and which queries need an index.

### Checkpoint

Describe what happens if the API process dies before a transaction commits. Describe how you would back up and restore the data.

---

## Milestone 4: Docker fundamentals

### Learn

Understand the difference between an image and a container:

- an image is a versioned filesystem and metadata;
- a container is a running process created from an image;
- a container should be replaceable;
- persistent data must live outside the replaceable container filesystem.

Study Dockerfiles, layers, build context, ports, volumes, networks, environment variables, health checks, and image tags.

### Minimal example

A conceptual Dockerfile contains:

```dockerfile
FROM python:3.x-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

Important questions include: what is copied into the image, what runs at build time, what runs at startup, and where secrets come from. The exact Python version and production options should be selected deliberately.

A port mapping means:

```text
host port 8000 -> container port 8000
```

It does not mean the application is automatically secure or reachable from every network.

### Signal Desk outcome

Create separate images for the Angular frontend and FastAPI service. Run PostgreSQL using a standard image with a volume for local data. Use Docker Compose to connect the three services on a private application network.

### Checkpoint

Break these cases and diagnose them:

- the API binds to `127.0.0.1` inside its container;
- the database data disappears after recreation;
- the frontend uses the wrong API hostname;
- a secret is accidentally included in an image layer.

---

## Milestone 5: Reproducible development and testing

### Learn

Study the test pyramid and the difference between:

- unit tests for isolated logic;
- integration tests for service and database behavior;
- API tests for HTTP contracts;
- browser tests for critical user journeys.

Also learn formatting, linting, dependency locking, semantic versioning, and build reproducibility.

### Minimal example

A useful local quality gate is:

```text
format -> lint -> unit tests -> integration tests -> build
```

A passing test is evidence about a defined behavior. It is not proof that the whole system is healthy.

### Signal Desk outcome

Cover at least these cases:

- valid message creation;
- invalid or empty message;
- database constraint failure;
- API response contract;
- frontend display of success and failure;
- service health endpoint.

### Checkpoint

Explain which test should catch a broken database query and which test should catch a broken Angular rendering path.

---

## Milestone 6: Kubernetes fundamentals

### Learn

Learn the Kubernetes model incrementally:

- a Pod runs one or more tightly coupled containers;
- a Deployment manages replicated, replaceable Pods;
- a Service gives Pods a stable network identity;
- a ConfigMap holds non-secret configuration;
- a Secret holds sensitive configuration, with separate secret-management concerns in real environments;
- a namespace groups resources;
- an Ingress or gateway exposes HTTP routing.

### Minimal example

The relationship is:

```text
Deployment -> Pods <- Service <- Ingress
```

A readiness probe answers whether a Pod should receive traffic. A liveness probe answers whether a process should be restarted. These are different questions.

Resource requests help scheduling; limits constrain usage. Neither automatically makes an application efficient.

### Signal Desk outcome

Run the frontend and API on a local cluster such as kind or minikube. Deploy PostgreSQL only for learning first; understand why a production database is often managed separately. Configure service discovery, probes, resources, and a persistent volume.

### Checkpoint

Investigate these scenarios:

- the Pod is running but traffic fails;
- the Pod restarts repeatedly;
- the Deployment has zero ready replicas;
- the API can resolve its Service but cannot connect to PostgreSQL.

Use events, logs, Pod status, probes, and Service endpoints as evidence.

---

## Milestone 7: GitHub Actions and CI/CD

### Learn

Study workflow triggers, jobs, steps, runners, artifacts, caching, permissions, environments, and secrets. Understand the distinction:

- CI validates and packages a change;
- CD releases a known artifact through controlled environments.

### Minimal example

A workflow conceptually looks like:

```yaml
on: [pull_request]
jobs:
  verify:
    steps:
      - checkout
      - install dependencies
      - lint and test
      - build
```

A release workflow should promote a specific image digest or immutable tag, rather than rebuilding unknown source code during deployment.

### Signal Desk outcome

Create a pipeline that:

1. checks pull requests;
2. runs frontend and backend quality checks;
3. builds container images;
4. publishes images to a registry after an approved event;
5. deploys to a non-production environment;
6. requires controlled promotion for production.

Do not put database passwords or cloud credentials in source control. Give workflow jobs only the permissions they need.

### Checkpoint

Explain what should happen when tests pass but image publishing fails, and when deployment succeeds but readiness checks fail.

---

## Milestone 8: Security and supply-chain basics

### Learn

Cover:

- authentication versus authorization;
- least privilege for users, services, and workflows;
- secret rotation and secret exposure prevention;
- dependency and image vulnerability scanning;
- non-root containers and minimal base images;
- input validation and safe error responses;
- TLS and secure headers;
- audit trails and retention;
- patching and vulnerability triage.

### Signal Desk outcome

Make a threat model for the browser, API, database, container registry, CI runner, and Kubernetes cluster. Record assets, trust boundaries, likely threats, and mitigations.

### Checkpoint

Find where each of these would be stored and rotated: API credentials, database password, signing key, and registry credential. Explain why `.env` files are useful locally but not a complete production secret strategy.

---

## Milestone 9: Observability and reliability

### Learn

Observability asks whether you can infer internal behavior from external signals:

- logs explain events;
- metrics show quantities over time;
- traces connect work across services;
- health checks support automation;
- alerts should represent actionable symptoms.

Study latency, traffic, errors, saturation, service-level objectives, graceful shutdown, retries, timeouts, and rate limits.

### Minimal example

A request should be traceable through a correlation identifier:

```text
frontend request id -> API log -> database operation log/trace
```

A useful alert is about impact, such as sustained error rate or unavailable replicas, rather than every individual warning.

### Signal Desk outcome

Add structured logs and request identifiers. Define dashboards for request rate, latency, error rate, API availability, database connections, and container restarts. Document what action follows each alert.

### Checkpoint

Break the API and use only logs, metrics, and health information to identify whether the cause is frontend routing, API failure, database failure, or cluster scheduling.

---

## Milestone 10: Operations, recovery, and incident practice

### Learn

Study deployment strategies, rollback, backups, restore testing, migrations, capacity planning, maintenance windows, incident roles, and postmortems.

A backup that has never been restored is an assumption, not evidence of recoverability.

### Signal Desk outcome

Write a short runbook for:

- API is returning 500 responses;
- PostgreSQL storage is full;
- a rollout causes readiness failures;
- a secret has been exposed;
- the latest release must be rolled back;
- data must be restored from backup.

Perform at least one restore exercise and one rollback exercise in a non-production environment.

### Checkpoint

For each incident, identify detection, immediate mitigation, root cause, recovery, and a prevention task.

---

## Milestone 11: Cloud deployment concepts

Start this milestone after you can operate the stack locally with Docker and Kubernetes. Choose AWS, Azure, Google Cloud, or remain cloud-neutral when you are ready.

### Learn

Compare:

- virtual machines;
- managed container platforms;
- managed Kubernetes;
- managed PostgreSQL;
- container registries;
- cloud identity and access management;
- virtual networks, subnets, firewalls, DNS, and TLS;
- persistent storage, backups, regions, availability, and cost.

### Signal Desk outcome

Map every local dependency to a cloud responsibility:

```text
local image -> registry
local cluster -> managed/container platform
local PostgreSQL -> managed database
local port -> private network and controlled ingress
local secret -> cloud secret manager
```

Do not assume that moving containers to the cloud automatically provides availability, security, backups, or observability.

### Checkpoint

Explain which components hold state, which can be recreated, and which failure domains must be considered for the chosen provider.

---

## Milestone 12: Expand communication patterns

Only after REST is reliable should you add other communication styles.

### Message queues

A producer sends work to a queue; a consumer processes it later. Study acknowledgements, retries, visibility timeouts, dead-letter queues, ordering, and idempotency.

```text
API -> queue -> worker -> database
```

Use a queue for work that does not need to finish during the user request.

### Event streaming

A producer appends events to a durable log. Consumers read at their own pace and may replay events. Study partitions, offsets, consumer groups, retention, ordering boundaries, and schema evolution.

```text
producer -> event stream -> consumer group(s)
```

Use streaming when multiple consumers, replay, or a history of events matters.

### Signal Desk outcome

Add one asynchronous use case, such as processing a message after submission. Compare its operational behavior with the original REST request and document the tradeoffs.

### Checkpoint

Choose REST, a queue, or a stream for three example requirements and justify each choice using latency, delivery, ordering, replay, and failure behavior.

---

## Final portfolio checkpoint

Produce these artifacts as evidence of learning:

- architecture diagram;
- API contract;
- local Docker runbook;
- Kubernetes resource explanation;
- CI/CD workflow explanation;
- security and secrets checklist;
- observability dashboard and alert notes;
- backup and restore record;
- incident investigation and postmortem;
- cloud architecture mapping;
- comparison of REST, queues, and streaming.

You are ready to move beyond the foundation when you can trace a change from commit to running service, identify the artifact deployed, explain how configuration and secrets enter the runtime, verify health, observe failures, and recover without guessing.

## Next topics

After this path, study Helm, infrastructure as code with Terraform or an equivalent tool, GitOps, autoscaling, policy as code, service meshes, advanced PostgreSQL operations, and managed messaging services. Add each topic only when a real project problem gives it a reason to exist.
