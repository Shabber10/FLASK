<div align="center">
  <h1>🧪 30-Day Enterprise Flask Masterclass</h1>
  <p><strong>A comprehensive, production-grade 30-day curriculum taking you from web architecture fundamentals to advanced microservices, real-time WebSockets, security hardening, and Dockerized production deployments.</strong></p>

  [![Flask Version](https://img.shields.io/badge/flask-3.x-blue?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
  [![Python Version](https://img.shields.io/badge/python-3.10%2B-brightgreen?style=flat-square&logo=python)](https://www.python.org/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
  [![Status](https://img.shields.io/badge/Status-100%25%20Completed-success.svg?style=flat-square)]()
</div>

<br>

Welcome to the **30-Day Enterprise Flask Masterclass**! This repository is designed to be your definitive guide to mastering Flask and Python web engineering. Whether you are building simple microservices, modular monoliths with Blueprints, real-time WebSocket applications, or containerized REST APIs, this step-by-step curriculum provides in-depth explanations, architectural diagrams, runnable code examples, memory shortcuts, and technical interview questions.

---

## 📑 Master Curriculum Index & Topic Syllabus

For a detailed topic-by-topic audit mapping every subtopic to file locations, see the dedicated [FLASK_CURRICULUM_INDEX_AND_AUDIT.md](FLASK_CURRICULUM_INDEX_AND_AUDIT.md).

```
 30-DAY ENTERPRISE FLASK MASTERCLASS
 │
 ├── 🟢 Phase 1: Core Web & Flask Architecture (Days 01 – 05)
 ├── 🟡 Phase 2: Database Integration & ORMs (Days 06 – 10)
 ├── 🔵 Phase 3: Modular Architecture & Design Patterns (Days 11 – 15)
 ├── 🟣 Phase 4: RESTful APIs, Microservices & JWT Auth (Days 16 – 20)
 ├── 🔴 Phase 5: Async Processing, Caching & WebSockets (Days 21 – 25)
 ├── 🛡️ Phase 6: Security, Observability & Performance (Days 26 – 28)
 └── 🧪 Phase 7: Testing, CI/CD & Production Capstone (Days 29 – 30)
```

---

## 🚀 Getting Started

### Prerequisites & Setup
1. Clone this repository to your local environment:
   ```bash
   git clone https://github.com/Shabber10/FLASK.git
   cd FLASK
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📚 Detailed Syllabus & Daily Subtopics

### 🟢 Phase 1: Core Web & Flask Architecture (Days 01 – 05)

| Day | Topic Name | Subtopics Covered | Link to Module |
| :---: | :--- | :--- | :---: |
| **01** | **Web Architecture, HTTP & Flask Internals** | Client-Server Architecture, Static vs Dynamic Sites, WWW, DNS, URL Anatomy, WSGI (PEP 3333), Flask Microframework, Restaurant Mental Model, `render_template()` Intro | [Day 01](DAY%2001%20-%20Introduction%20to%20Flask%20and%20Web%20Architecture/0.%20Web%20Fundamentals%20for%20Absolute%20Beginners.md) |
| **02** | **Advanced URL Routing, Converters & Requests** | Werkzeug `url_map`, Built-in Converters, Custom `EvenNumberConverter`, `redirect()` vs `url_for()`, `request.args` (GET), `request.form` (POST), `request.get_json()` (PUT/DELETE), RAM vs DB Storage, `jsonify()` | [Day 02](DAY%2002%20-%20Routing,%20Request%20and%20Response%20Objects/0.%20Routing%20and%20Request-Response%20Fundamentals%20for%20Beginners.md) |
| **03** | **Request Lifecycle & Context Locals** | Application Context (`current_app`, `g`), Request Context (`request`, `session`), Lifecycle Hooks (`before_request`, `after_request`), Request Timing Middleware | [Day 03](DAY%2003%20-%20Request%20Lifecycle%20and%20Context%20Locals/0.%20Contexts%20and%20Request%20Lifecycle%20Fundamentals%20for%20Beginners.md) |
| **04** | **Jinja2 Templating Engine Masterclass** | `render_template()` syntax, Jinja2 Delimiters (`{{ }}`, `{% %}`), `if/else` & `for` loops, Static files with `url_for('static')`, Template Inheritance (`extends`, `block`), Inclusion (`include`) | [Day 04](DAY%2004%20-%20Jinja2%20Templating%20Engine%20Masterclass/0.%20Jinja2%20Templating%20Fundamentals%20for%20Beginners.md) |
| **05** | **Web Forms, Validation & Flask-WTF** | CSRF Tokens, `FlaskForm` classes, Input Fields & Built-in Validators, Custom Field Validators, File Uploads with WTForms | [Day 05](DAY%2005%20-%20Web%20Forms,%20Validation%20and%20Flask-WTF/0.%20Web%20Forms%20and%20Flask-WTF%20Fundamentals%20for%20Beginners.md) |

---

### 🟡 Phase 2: Database Integration, ORMs & Migrations (Days 06 – 10)

| Day | Topic Name | Subtopics Covered | Link to Module |
| :---: | :--- | :--- | :---: |
| **06** | **Database Fundamentals & Flask-SQLAlchemy** | ORM vs Raw SQL, `db.Model`, Column Types, Constraints, Table Creation, Database Sessions, CRUD Operations (`add`, `commit`, `delete`) | [Day 06](DAY%2006%20-%20Database%20Fundamentals%20and%20Flask-SQLAlchemy/0.%20Database%20and%20ORM%20Fundamentals%20for%20Beginners.md) |
| **07** | **Advanced Querying, Filtering & Transactions** | Filter Operators (`like`, `in_`, `between`), Logical `and_`/`or_`, Ordering, Pagination (`paginate`), Aggregations (`count`, `avg`), Session Transactions & Rollback | [Day 07](DAY%2007%20-%20Advanced%20Querying,%20Filtering%20and%20Transactions/0.%20Advanced%20Querying%20Fundamentals%20for%20Beginners.md) |
| **08** | **Advanced Relationships, Cascades & Lazy Loading** | One-to-Many (`db.ForeignKey`), One-to-One, Many-to-Many Association Tables, Cascade Deletes (`all, delete-orphan`), Lazy Loading (`select`, `joined`, `subquery`, `dynamic`) | [Day 08](DAY%2008%20-%20Advanced%20Relationships,%20Cascades%20and%20Lazy%20Loading/0.%20Database%20Relationships%20Fundamentals%20for%20Beginners.md) |
| **09** | **Database Migrations with Flask-Migrate** | Schema Evolution, Alembic Integration, Flask-Migrate CLI Workflow (`init`, `migrate`, `upgrade`, `downgrade`), Custom Migration Scripts | [Day 09](DAY%2009%20-%20Database%20Migrations%20with%20Flask-Migrate/0.%20Database%20Migrations%20Fundamentals%20for%20Beginners.md) |
| **10** | **Multiple Databases, Binds & Raw SQL Execution** | `SQLALCHEMY_BINDS`, Model `__bind_key__`, Multi-Database Architecture, Executing Raw SQL (`db.session.execute`), Parameterized Queries & SQL Injection Prevention | [Day 10](DAY%2010%20-%20Multiple%20Databases,%20Binds%20and%20Raw%20SQL/0.%20Multiple%20Databases%20and%20Raw%20SQL%20Fundamentals%20for%20Beginners.md) |

---

### 🔵 Phase 3: Modular Architecture & Design Patterns (Days 11 – 15)

| Day | Topic Name | Subtopics Covered | Link to Module |
| :---: | :--- | :--- | :---: |
| **11** | **Modular Development with Flask Blueprints** | Monolith vs Blueprints, `Blueprint` definition, Route Registration, `url_prefix`, Blueprint Template & Static Isolation, Subdomain Dispatching | [Day 11](DAY%2011%20-%20Modular%20Development%20with%20Flask%20Blueprints/0.%20Flask%20Blueprints%20Fundamentals%20for%20Beginners.md) |
| **12** | **Application Factory Pattern & Environment Config** | Application Factory (`create_app`), Circular Import Prevention, Config Classes (`DevConfig`, `ProdConfig`), Environment Variables (`.env`, `.flaskenv`) | [Day 12](DAY%2012%20-%20Application%20Factory%20Pattern%20and%20Environment%20Config/0.%20Application%20Factory%20and%20Config%20Fundamentals%20for%20Beginners.md) |
| **13** | **Custom CLI Commands & Flask Extensions** | `@app.cli.command`, Click Command Arguments & Options, Authoring Custom Flask Extensions (`init_app` pattern) | [Day 13](DAY%2013%20-%20Custom%20CLI%20Commands%20and%20Flask%20Extensions/0.%20Custom%20CLI%20Commands%20and%20Extensions%20Fundamentals%20for%20Beginners.md) |
| **14** | **Session Management & Cookie Security** | Signed Cookie Sessions (`itsdangerous`), Cookie Flags (`HttpOnly`, `Secure`, `SameSite`), Server-Side Redis Sessions (`Flask-Session`) | [Day 14](DAY%2014%20-%20Session%20Management%20and%20Cookie%20Security/0.%20Sessions%20and%20Cookie%20Security%20Fundamentals%20for%20Beginners.md) |
| **15** | **User Authentication & Password Hashing** | Cryptographic Hashing (`Bcrypt`, `PBKDF2`), `Flask-Login` (`LoginManager`, `current_user`, `user_loader`), Role-Based Access Control (RBAC) Decorators | [Day 15](DAY%2015%20-%20User%20Authentication%20and%20Password%20Hashing/0.%20Authentication,%20Password%20Hashing%20and%20RBAC%20Fundamentals%20for%20Beginners.md) |

---

### 🟣 Phase 4: RESTful APIs, Microservices & JWT Auth (Days 16 – 20)

| Day | Topic Name | Subtopics Covered | Link to Module |
| :---: | :--- | :--- | :---: |
| **16** | **REST API Architecture & HTTP Status Codes** | REST Principles (Statelessness, Uniform Interface), HTTP Status Codes (2xx, 4xx, 5xx), Standardized JSON Response Envelopes | [Day 16](DAY%2016%20-%20REST%20API%20Architecture%20and%20HTTP%20Status%20Codes/0.%20REST%20API%20Architecture%20and%20Status%20Codes%20Fundamentals%20for%20Beginners.md) |
| **17** | **Data Serialization & Validation with Marshmallow** | Marshmallow Schemas, Dump vs Load, Field Types, Custom Validation (`@validates`), Nested Schemas, `SQLAlchemyAutoSchema` | [Day 17](DAY%2017%20-%20Data%20Serialization%20and%20Validation%20with%20Marshmallow/0.%20Serialization%20and%20Marshmallow%20Fundamentals%20for%20Beginners.md) |
| **18** | **RESTful Extensions (Flask-RESTful & Flask-Smorest)** | Class-Based Views (`Resource`), HTTP Verb Mapping, `Flask-Smorest`, Automatic Swagger UI OpenAPI Specs (`@blp.response`, `@blp.arguments`) | [Day 18](DAY%2018%20-%20RESTful%20Extensions%20and%20OpenAPI%20Documentation/0.%20REST%20Extensions%20and%20OpenAPI%20Documentation%20Fundamentals%20for%20Beginners.md) |
| **19** | **API Authentication with JWT (Flask-JWT-Extended)** | JWT Tokens (Header, Payload, Signature), `@jwt_required()`, Access vs Refresh Tokens, Redis Token Revocation & Blacklisting | [Day 19](DAY%2019%20-%20API%20Authentication%20with%20JWT/0.%20JWT%20Authentication%20Fundamentals%20for%20Beginners.md) |
| **20** | **CORS Handling & Rate Limiting** | Same-Origin Policy (SOP), `Flask-CORS` headers (`Access-Control-Allow-Origin`), Rate Limiting (`Flask-Limiter`), Redis Storage Backends | [Day 20](DAY%2020%20-%20CORS%20Handling%20and%20Rate%20Limiting/0.%20CORS%20and%20Rate%20Limiting%20Fundamentals%20for%20Beginners.md) |

---

### 🔴 Phase 5: Asynchronous Operations, Caching & Real-Time Web (Days 21 – 25)

| Day | Topic Name | Subtopics Covered | Link to Module |
| :---: | :--- | :--- | :---: |
| **21** | **Background Processing with Celery & Redis** | Async Queues, Celery Architecture (Producer, Broker, Worker, Result Backend), `@celery.task`, `.delay()`, Task State Tracking | [Day 21](DAY%2021%20-%20Background%20Processing%20with%20Celery%20and%20Redis/0.%20Celery%20and%20Background%20Processing%20Fundamentals%20for%20Beginners.md) |
| **22** | **Periodic Tasks & Scheduled Jobs with Celery Beat** | Celery Beat Scheduler, Cron Schedules (`crontab`), Task Retries with Backoff (`autoretry_for`), Dead Letter Error Callbacks | [Day 22](DAY%2022%20-%20Periodic%20Tasks%20and%20Scheduled%20Jobs/0.%20Periodic%20Tasks%20and%20Scheduled%20Jobs%20Fundamentals%20for%20Beginners.md) |
| **23** | **Application Caching Strategies with Flask-Caching** | In-Memory vs Redis Caching, `Flask-Caching`, View Caching (`@cache.cached`), Memoization (`@cache.memoize`), Cache Invalidation Triggers | [Day 23](DAY%2023%20-%20Application%20Caching%20Strategies/0.%20Caching%20Strategies%20Fundamentals%20for%20Beginners.md) |
| **24** | **Real-Time WebSockets with Flask-SocketIO** | HTTP Polling vs Full-Duplex WebSockets, `Flask-SocketIO` Event Handlers (`@socketio.on`, `emit`), Rooms & Namespaces, Redis Pub/Sub Broker | [Day 24](DAY%2024%20-%20Real-Time%20WebSockets%20with%20Flask-SocketIO/0.%20WebSockets%20and%20Flask-SocketIO%20Fundamentals%20for%20Beginners.md) |
| **25** | **Asynchronous Flask (Async Routes & Quart)** | Async Views (`async def`), WSGI vs ASGI Limitations, Quart Framework, High-Concurrency Benchmarks (Flask vs Quart vs FastAPI) | [Day 25](DAY%2025%20-%20Asynchronous%20Flask%20and%20Quart%20Integration/0.%20Async%20Flask%20and%20Quart%20Fundamentals%20for%20Beginners.md) |

---

### 🛡️ Phase 6: Enterprise Security, Observability & Performance Tuning (Days 26 – 28)

| Day | Topic Name | Subtopics Covered | Link to Module |
| :---: | :--- | :--- | :---: |
| **26** | **Enterprise Flask Security Hardening** | OWASP Top 10, Security Headers (`Flask-Talisman`, CSP, HSTS), Dynamic CSP Nonces, HTML Sanitization (`Bleach`), Security Audits (`bandit`, `pip-audit`) | [Day 26](DAY%2026%20-%20Enterprise%20Flask%20Security%20Hardening/0.%20Web%20Security%20and%20Flask%20Hardening%20Fundamentals%20for%20Beginners.md) |
| **27** | **Error Handling, Logging & Observability** | Python Logging Levels, Structured JSON Logging (`dictConfig`), Request Correlation IDs (`X-Request-ID`), Centralized Error Handlers (`@app.errorhandler`) | [Day 27](DAY%2027%20-%20Error%20Handling,%20Logging%20and%20Observability/0.%20Error%20Handling%20and%20Observability%20Fundamentals%20for%20Beginners.md) |
| **28** | **Flask Performance Tuning & Database Optimization** | N+1 Query Problem, Eager Loading (`joinedload`, `selectinload`), Database Connection Pool Tuning, Gzip Response Compression (`Flask-Compress`), CPU Profiling (`ProfilerMiddleware`) | [Day 28](DAY%2028%20-%20Flask%20Performance%20Tuning%20and%20Database%20Optimization/0.%20Performance%20Tuning%20and%20Optimization%20Fundamentals%20for%20Beginners.md) |

---

### 🧪 Phase 7: Testing, CI/CD & Capstone Production Project (Days 29 – 30)

| Day | Topic Name | Subtopics Covered | Link to Module |
| :---: | :--- | :--- | :---: |
| **29** | **Automated Testing Masterclass with Pytest** | Testing Pyramid, Pytest Fixtures (`conftest.py`), Route Testing (`app.test_client()`), Database Mocking (`pytest-mock`), Coverage (`pytest-cov`), GitHub Actions CI | [Day 29](DAY%2029%20-%20Automated%20Testing%20Masterclass%20with%20Pytest/0.%20Automated%20Testing%20and%20Pytest%20Fundamentals%20for%20Beginners.md) |
| **30** | **Production Capstone & Enterprise Deployment** | 12-Factor App Rules, Production Stack (Nginx + Gunicorn + Flask), Docker Multi-Stage Builds, `docker-compose.yml`, Kubernetes Probes (`/healthz`, `/readyz`), Capstone Microservice | [Day 30](DAY%2030%20-%20Production%20Capstone%20and%20Deployment/0.%20Production%20Deployment%20and%20Architecture%20Fundamentals%20for%20Beginners.md) |

---

## 🛠 Tech Stack & Tools

- **Core Framework**: Flask 3.x, Werkzeug, Jinja2
- **ORMs & Database**: Flask-SQLAlchemy, SQLAlchemy 2.0+, Flask-Migrate (Alembic), SQLite, PostgreSQL
- **Security & Auth**: Flask-WTF, WTForms, Flask-Login, Flask-JWT-Extended, Flask-Talisman, Flask-Limiter, Passlib, Bcrypt
- **API Tools**: Flask-RESTful, Marshmallow, Flask-CORS, Flask-Smorest (OpenAPI/Swagger)
- **Async & Realtime**: Celery, Redis, Flask-SocketIO, Gevent / Eventlet
- **Testing & Deployment**: Pytest, Pytest-Flask, Coverage, Gunicorn, Nginx, Docker, Docker-Compose

---

## 📄 License
This repository is released under the [MIT License](LICENSE).
