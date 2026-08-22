# 🚀 Modern Flask 3.x & SQLAlchemy 2.0 Enterprise Architecture Guide

This comprehensive reference manual bridges modern Python engineering paradigms with enterprise Flask web service design, highlighting patterns that differentiate scalable production systems from basic tutorial implementations.

---

## 1. SQLAlchemy 2.0 Modern Declarative Syntax

SQLAlchemy 2.0 introduces a modern, type-safe declarative mapping system centered around `Mapped[]` and `mapped_column()`. Legacy SQLAlchemy 1.x syntax (e.g., `db.Column`, `Model.query.filter_by()`) is in maintenance mode and discouraged for new production services.

### Key Syntax Differences: 1.4/Legacy vs. 2.0 Modern

| Feature | Legacy SQLAlchemy (1.x) | Modern SQLAlchemy 2.0 |
| :--- | :--- | :--- |
| **Column Definition** | `id = db.Column(db.Integer, primary_key=True)` | `id: Mapped[int] = mapped_column(primary_key=True)` |
| **Nullable Strings** | `bio = db.Column(db.String(255), nullable=True)` | `bio: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)` |
| **Relationships** | `posts = db.relationship('Post', backref='author')` | `posts: Mapped[List[Post]] = relationship(back_populates="author")` |
| **Query Execution** | `User.query.filter_by(active=True).all()` | `db.session.execute(select(User).where(User.active == True)).scalars().all()` |
| **Row by Primary Key**| `User.query.get(user_id)` | `db.session.get(User, user_id)` |
| **Bulk Updates** | `User.query.filter(...).update({...})` | `db.session.execute(update(User).where(...).values({...}))` |

### Production Model Implementation Example

```python
from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, select
from capstone.extensions import db

class Organization(db.Model):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # 1-to-Many Relationship
    members: Mapped[List[User]] = relationship("User", back_populates="organization", cascade="all, delete-orphan")


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    organization_id: Mapped[Optional[int]] = mapped_column(ForeignKey("organizations.id", ondelete="SET NULL"))

    # Many-to-1 Relationship
    organization: Mapped[Optional[Organization]] = relationship("Organization", back_populates="members")
```

---

## 2. API Versioning Strategies

Large-scale enterprise APIs must evolve without breaking existing web, mobile, and third-party consumers.

### Strategy 1: URL Path Versioning (Recommended)
Prefixing endpoints with `/api/v1/`, `/api/v2/` provides maximum visibility, clear routing blueprints, and simple cache segregation.

```
/api/v1/users
/api/v2/users
```

**Flask Blueprint Partitioning Structure:**
```
capstone/
 ├── api/
 │    ├── v1/
 │    │    ├── __init__.py      # Blueprint(url_prefix="/api/v1")
 │    │    ├── auth.py
 │    │    └── users.py
 │    └── v2/
 │         ├── __init__.py      # Blueprint(url_prefix="/api/v2")
 │         └── users.py
```

### Strategy 2: Header-Based Versioning
Clients specify desired version via custom headers:
```http
Accept: application/vnd.enterprise.v1+json
```

---

## 3. Secure File and Media Storage Patterns

### Best Practices for File Uploads
1. **Filename Sanitization**: Always apply `werkzeug.utils.secure_filename` and assign UUID-based unique filenames to prevent path traversal attacks (`../../../etc/passwd`).
2. **MIME & Magic Byte Verification**: Never trust client-provided `Content-Type`. Validate file extensions against strict whitelists and inspect file headers.
3. **Size Limits**: Enforce `MAX_CONTENT_LENGTH` at both the Flask app level and the Nginx reverse proxy level (`client_max_body_size`).
4. **Cloud S3 Abstraction**: Abstract storage behind an interface so files can be saved to local disk in development and Amazon S3 / Google Cloud Storage in production.

```python
# S3 Abstraction Interface
class S3StorageProvider:
    def __init__(self, bucket_name: str):
        import boto3
        self.s3 = boto3.client("s3")
        self.bucket = bucket_name

    def upload_file(self, file_obj, key: str) -> str:
        self.s3.upload_fileobj(file_obj, self.bucket, key)
        return f"https://{self.bucket}.s3.amazonaws.com/{key}"
```

---

## 4. Kubernetes Health Checks & Probes

Container orchestrators (Kubernetes, AWS ECS, GCP Cloud Run) require distinct endpoints for **Liveness** and **Readiness**.

| Probe | Endpoint | Purpose | Failure Consequence |
| :--- | :--- | :--- | :--- |
| **Liveness** | `/api/v1/health/healthz` | Checks if Python web process is running & responsive | Restarts the container |
| **Readiness**| `/api/v1/health/ready` | Verifies DB, Redis, and message broker connections | Removes container from load balancer routing |

---

## 5. Enterprise Secrets Management

In production, hardcoding secrets or relying solely on unencrypted `.env` files is a security risk.

### Secret Management Architecture
```
┌──────────────────────────────────────────────┐
│ AWS Secrets Manager / HashiCorp Vault       │
└──────────────────────┬───────────────────────┘
                       │ Injected at Container Startup
                       ▼
┌──────────────────────────────────────────────┐
│ Environment Variables (`os.environ`)        │
└──────────────────────┬───────────────────────┘
                       │ Read into Config Objects
                       ▼
┌──────────────────────────────────────────────┐
│ Flask Config (`current_app.config`)          │
└──────────────────────────────────────────────┘
```

---

## 6. Observability & Prometheus Metrics

Exposing standard Prometheus metrics enables real-time latency, error-rate, and throughput dashboards in Grafana.

- **Metrics Endpoint**: `GET /metrics`
- **Tracked Metrics**:
  - `flask_http_requests_total{method="POST", endpoint="/api/v1/auth/login", status="200"}`
  - `flask_http_request_duration_seconds{endpoint="/api/v1/users"}`
