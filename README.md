# 🔒 DevSecOps + AI Lab - Professional Security Pipeline

> Enterprise-grade DevSecOps project with AI/ML threat detection, microservices architecture, and automated security scanning.

[![Security - SAST](https://github.com/yourusername/devsecops_ai_lab/actions/workflows/security-sast.yml/badge.svg)](../../actions/workflows/security-sast.yml)
[![Security - SCA](https://github.com/yourusername/devsecops_ai_lab/actions/workflows/security-sca.yml/badge.svg)](../../actions/workflows/security-sca.yml)
[![Tests & Quality](https://github.com/yourusername/devsecops_ai_lab/actions/workflows/test-and-quality.yml/badge.svg)](../../actions/workflows/test-and-quality.yml)

## 🎯 Overview

This project demonstrates a **complete DevSecOps pipeline** with:

- ✅ **4 Microservices** (OAuth2, FastAPI, LLM/NLP, Security Automation)
- ✅ **6 GitHub Actions Workflows** (SAST, SCA, Container, AI, Tests, Reporting)
- ✅ **BERT-based Threat Detection** (Prompt injection, SQL injection detection)
- ✅ **Multi-layer Security Scanning** (Bandit, Semgrep, Safety, Trivy)
- ✅ **Automated Reporting** (JSON, HTML, SARIF formats)
- ✅ **Pre-commit Security Hooks** (Black, isort, Flake8, Bandit)

## 🏗️ Architecture

### Microservices
- **OAuth2 Service** (Port 8001): JWT token management
- **API Backend** (Port 8002): FastAPI REST service with OAuth2 integration
- **LLM/NLP Service** (Port 8003): BERT-based threat detector
- **Security Automation**: Scanning & reporting orchestration
- **PostgreSQL (x2)**: Separate databases for OAuth2 and API

### Security Pipeline
1. **SAST**: Bandit + Semgrep
2. **SCA**: Safety + pip-audit
3. **Container**: Trivy
4. **AI Model**: BERT integrity checks
5. **Reporting**: Consolidated JSON/HTML reports

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- Python 3.10+

### Setup

```bash
# Clone repo
cd /home/debianuser/ai_devsecops/ai_labs/devsecops_ai_lab

# Start services
docker-compose up -d

# Verify health
curl http://localhost:8001/health  # OAuth2
curl http://localhost:8002/health  # API
curl http://localhost:8003/health  # LLM
```

### Running Workflows Locally

```bash
# Install act (GitHub Actions locally)
brew install act

# Run security workflow
act push -j bandit

# Run all tests
act push -j test
```

## 📊 Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `security-sast.yml` | Push/PR | Python & multi-lang SAST |
| `security-sca.yml` | requirements.txt changes | Dependency vulnerabilities |
| `security-container.yml` | Dockerfile changes | Container image scanning |
| `ai-model-integrity.yml` | LLM service changes | Model validation |
| `test-and-quality.yml` | Push/PR | Unit tests + code quality |
| `security-report.yml` | All security scans complete | Consolidated report |

## 📈 Accessing Reports

### GitHub UI
1. **Actions** tab → Select workflow
2. **Artifacts** section → Download reports
3. **Security** tab → View SARIF findings

### Report Types
- `security-report.json` - Consolidated findings
- `bandit-report.json` - Python security issues
- `semgrep-report.json` - Pattern matches
- `safety-report.json` - Dependency vulnerabilities
- `*-trivy.sarif` - Container vulnerabilities

## 🤖 AI Threat Detection

### BERT Model
- **Architecture**: Bidirectional Encoder (12 layers)
- **Task**: Binary classification (safe/threat)
- **Inputs**: Prompts, payloads, API requests
- **Outputs**: Threat probability + classification

### API Endpoint
```bash
curl -X POST http://localhost:8003/detect-threat \
  -H "Content-Type: application/json" \
  -d '{
    "text": "SELECT * FROM users",
    "threshold": 0.7
  }'
```

## 🔐 Security Policy

### ❌ NO AUTO-MERGE

**IMPORTANT**: This project **DOES NOT auto-merge** security findings.

All security workflows run with `continue-on-error: true` to:
- ✅ Prevent blocking merges on scanner errors (NVD timeout, etc.)
- ✅ Allow visibility of all findings
- ✅ Require manual review for all security alerts

### 📊 Alert Handling

| Alert Type | Action | Auto-Fix |
|-----------|--------|----------|
| Dependabot | Open PR | ✅ Optional |
| CodeQL | Review + merge manually | ❌ Never auto |
| Trivy | Critical only | ❌ Manual review |
| Bandit | Informational | ✅ If low-risk |
| NVD CVEs | Context-based | ⚠️ See policy |

### 🧠 Vulnerability Triage

Use the triage script to classify vulnerabilities:

```bash
python scripts/triage_vulnerabilities.py
```

**Rules**:
- ✅ ML libraries (transformers, torch) - acceptable deserialization risk
- ✅ Dev dependencies (pytest) - not in production
- ❌ Production secrets - always block
- ❌ Critical RCE - always block

### 🔄 Pull Request Merge Requirements

- [ ] All workflows completed (pass or continue-on-error)
- [ ] Code review approved
- [ ] Security findings triaged
- [ ] Critical vulnerabilities addressed
- [ ] Tests passing

**Protection rules** can be configured in GitHub Settings to require manual approval.

## 📁 Project Structure
```plaintext
devsecops_ai_lab/
├── .github/                # GitHub-specific files
│   └── workflows/          # GitHub Actions workflows
├── reports/                # Test and coverage reports
├── src/                    # Source code
│   ├── api/                # API-related code
│   ├── ml/                 # Machine learning models
│   └── utils/              # Utility functions
├── tests/                  # Test cases
│   ├── api/                # API tests
│   └── ml/                 # ML model tests
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
└── requirements.txt         # Python dependencies
```

## GitHub Secrets / Variables to add for automated forwarding
- NVD_API_KEY
- SIEM_URL
- SIEM_API_KEY
- THEHIVE_URL
- THEHIVE_API_KEY
- MISP_URL
- MISP_API_KEY
- SLACK_WEBHOOK
- S3_ARTIFACT_BUCKET (optional)
- ELK_URL, ELK_API_KEY (optional)

## Troubleshooting Common Issues

- **Permission denied (publickey)**:
  - Ensure your SSH key is added to the ssh-agent and your GitHub account.
  - Command to add SSH key: `ssh-add ~/.ssh/id_rsa`

- **Repository not found**:
  - Check if the repository URL is correct.
  - Ensure you have access to the repository.

- **Docker issues**:
  - Ensure Docker is installed and running.
  - For permission issues, consider adding your user to the `docker` group: `sudo usermod -aG docker $USER`

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Testing with pytest](https://docs.pytest.org/en/stable/)
- [Pylint Documentation](https://pylint.pycqa.org/en/latest/)
- [Black Documentation](https://black.readthedocs.io/en/stable/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
