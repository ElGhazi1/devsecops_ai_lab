# 🔄 GitHub Actions Workflows

## Workflow Triggers

| Workflow | Trigger | Schedule |
|----------|---------|----------|
| SAST | Push/PR to main/develop | Weekly Monday 2 AM |
| SCA | Push to main/develop + requirements.txt changes | Weekly Monday 3 AM |
| Container | Push Dockerfile changes | Weekly Monday 4 AM |
| AI Model | Push to llm-nlp-service or notebooks | On-demand |
| Tests | Push/PR to main/develop | On every push |
| Report | All security workflows complete | Automatic |

## Workflow: Security - SAST

### Jobs
1. **Bandit** - Python-specific security analysis
   - Output: `bandit-report.json`
   - Issues: Hardcoded secrets, SQL injection patterns
   
2. **Semgrep** - Multi-language pattern matching
   - Output: `semgrep.sarif`, `semgrep.json`
   - Issues: OWASP Top 10, security patterns

3. **Pylint** - Code quality and security
   - Output: `pylint-report.txt`
   - Issues: Code smells, potential bugs

### Artifacts
- `bandit-report/bandit-report.json` - 30 days retention
- `semgrep-report/semgrep.json` - 30 days retention
- `pylint-report/pylint-report.txt` - 30 days retention

### PR Comments
Automatically comments on PRs with critical findings.

## Workflow: Security - SCA

### Jobs
1. **Safety** - Python vulnerability database
   - Checks: Known CVEs in dependencies
   - Output: `safety-reports/{service}.json`

2. **pip-audit** - Alternative vulnerability scanner
   - Checks: PyPA advisory database
   - Output: `pip-audit-reports/{service}.json`

### Artifacts
- `safety-reports/` - 30 days retention
- `pip-audit-reports/` - 30 days retention

## Workflow: Security - Container

### Jobs
1. **Trivy Dockerfile Scan**
   - Checks: Misconfigurations, hardcoded values
   - Output: `{service}-trivy.sarif`

2. **Trivy Image Scan**
   - Checks: OS and library vulnerabilities
   - Output: `{service}-image-trivy.sarif`

### SARIF Upload
Findings uploaded to GitHub Security tab for visibility.

## Workflow: AI - Model Integrity

### Jobs
1. **Model Validation**
   - Tests: BERT model loading
   - Tests: Inference capability
   - Coverage: Model unit tests

2. **Threat Detection Tests**
   - Tests: Prompt injection detection
   - Tests: Attack pattern classification

## Workflow: Tests & Code Quality

### Jobs
1. **Unit & Integration Tests**
   - Framework: PyTest
   - Coverage: Target 80%+
   - Databases: PostgreSQL instances

2. **Code Formatting**
   - Black: Code formatting
   - isort: Import sorting
   - Flake8: Linting

3. **Docker Compose**
   - Validation: docker-compose config
   - Build: All services
   - Health: Service health checks

## Accessing Reports

### GitHub UI
1. Navigate to **Actions** tab
2. Select workflow run
3. Download from **Artifacts**

### GitHub Security Tab
1. Navigate to **Security** → **Code scanning alerts**
2. View SARIF findings from Trivy/Semgrep

### Command Line
```bash
# Download artifacts locally
gh run download {run-id} -D ./artifacts
```

## Local Testing

### Run Workflow Locally
```bash
# Install act: https://github.com/nektos/act
act push -j bandit
act push -j semgrep
act push -j safety
```

## Troubleshooting

### Workflow Fails
1. Check workflow logs in Actions tab
2. View step output for error details
3. Run commands locally to reproduce

### Missing Artifacts
- Ensure retention-days is set
- Check if job succeeded/failed
- Artifacts deleted after retention period

### Slow Tests
- Parallelize with matrix jobs
- Cache dependencies between runs
- Use composite actions to reduce duplication
