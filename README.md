# Fermentation Gas Mass Spectrometry

> **Domain:** Clinical Decision Support & Biomedical Computing
> **Reference Guidelines & Standards:** Standard Clinical Formulations & ISO/IEC Quality Frameworks

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

Fermentation Gas Mass Spectrometry is an enterprise analytical platform that evaluates fermentation process data through specialized worker agents. It provides:

- **Respiratory Quotient (RQ) Analysis**: Computes RQ = CER/OUR from off-gas measurements
- **Oxygen Uptake Rate (OUR) & CO2 Evolution Rate (CER) Evaluation**: Real-time metabolic state classification
- **Multi-Agent Consensus**: Coordinated evaluation across QC, Safety, and Protocol Conformance workers
- **Risk Stratification**: Multi-tier urgency classification with actionable remediation

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds
- **Risk & Urgency Classification**: Multi-tier categorization with automated clinical/operational action recommendations
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection
- **Zero-PHI Outbound Interceptor**: AST and regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers
- **Tamper-Evident HMAC-SHA256 Audit Trail**: Chained, cryptographically signed logs with full signature verification

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/fermentation-gas-mass-spectrometry.git
cd fermentation-gas-mass-spectrometry

# Install production dependencies
pip install -e .

# Install development dependencies (includes pytest)
pip install -e ".[dev]"

# Set audit key (recommended for production)
export AUDIT_SECRET_KEY="your-secure-random-key-here"
```

---

## 💻 CLI Quickstart & Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Supervisory Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch CSV Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
| Flag | Description | Default |
|:-----|:------------|:--------|
| `--task-id` | Unique task identifier | `TASK-2026-001` |
| `--target` | Target/specimen identifier | `KEY-TARGET-01` |
| `--primary` | Primary metric measurement | `28.5` |
| `--secondary` | Secondary metric measurement | `14.2` |
| `--critical` | Enable critical flag | `False` |
| `--status` | Status descriptor | `DISCORDANT` |

### Input Data Schema

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Parameter / observation metric | Required |
| `target_identifier` | Parameter / observation metric | Required |
| `primary_metric` | Primary measurement value | Required |
| `secondary_metric` | Secondary measurement value | Optional |
| `is_critical_flag` | Emergency escalation trigger | Optional |
| `status_descriptor` | Status code or phenotype | Optional |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, emails, DOB patterns, and patient names
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs with full HMAC signature verification (not just chain linkage)
* **Input Validation:** Pydantic models enforce length bounds, reject NaN/Inf values, and strip control characters
* **Secure Defaults:** Random audit key generated if `AUDIT_SECRET_KEY` env var is not set (forces explicit production configuration)
* **API Error Sanitization:** Internal exceptions are logged server-side; clients receive generic error messages

### Environment Variables
| Variable | Description | Required |
|:---------|:------------|:---------|
| `AUDIT_SECRET_KEY` | HMAC key for audit trail signing | Recommended |
| `MODEL_PROVIDER` | LLM provider (`mock`, `ollama`, `claude`, `openai`) | No (default: `mock`) |

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

---

## 🐳 Container Deployment

```bash
# Build and run with Docker Compose (requires AUDIT_SECRET_KEY)
export AUDIT_SECRET_KEY="$(python -c 'import os; print(os.urandom(32).hex())')"
docker compose up --build

# Or use Docker directly
docker build -t fermentation-gas-mass-spectrometry .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY="your-key" fermentation-gas-mass-spectrometry
```

---

## 📁 Project Structure

```
fermentation-gas-mass-spectrometry/
├── agents/                  # Core multi-agent framework
│   ├── base.py             # Security guards, HMAC audit trail
│   ├── models.py           # Pydantic schemas with validation
│   ├── supervisor.py       # Orchestrator coordinating workers
│   ├── workers.py          # QC, Safety, Protocol workers
│   ├── api.py              # FastAPI REST endpoints
│   ├── metrics.py          # Prometheus metrics exporter
│   ├── llm_factory.py      # LLM provider abstraction
│   └── learning.py         # Bayesian calibration engine
├── offgas_analyzer/         # Domain-specific analyzer module
│   ├── models.py           # Frontier payload definitions
│   ├── engine.py           # Core evaluation algorithms
│   ├── agents.py           # OUR/CER/RQ specialist agents
│   ├── cli.py              # Domain-specific CLI
│   └── server.py           # Domain-specific FastAPI server
├── tests/                   # Pytest test suite
├── web/index.html           # Operations console UI
├── cli.py                   # Main CLI entry point
├── enrichment.py            # Enrichment feature engines
├── simulator.py             # Load testing simulator
├── pyproject.toml           # Project configuration
├── Dockerfile               # Container image definition
└── docker-compose.yml       # Multi-service orchestration
```
