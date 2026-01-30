# DevSecOps AI Lab - Automation Testing

Simple project for testing Python automation with GitHub Actions, log generation, and artifact management.

## Quick Start

```bash
# Clone & setup
git clone https://github.com/ElGhazi1/devsecops_ai_lab.git
cd devsecops_ai_lab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Local Testing

```bash
# Run tests
pytest tests/ -v

# Generate reports
python scripts/generate_report.py

# Check code quality
pylint src/
black src/ --check
```

## GitHub Actions Workflows

Workflows are configured in `.github/workflows/` to:
- Run tests and generate reports
- Create JSON/CSV artifacts
- Upload logs automatically
- Generate SARIF security findings

### To enable GitHub DevSecOps Features:

1. **Go to Settings → Code security and analysis**
   - Enable "Dependency graph" ✓
   - Enable "Dependabot alerts" ✓
   - Enable "Dependabot security updates" ✓

2. **Go to Settings → Actions → General**
   - Allow all actions ✓
   - Artifact retention: 30 days

3. **Create NVD API Key** (optional):
   - Visit https://nvd.nist.gov/developers/request-an-api-key
   - Store in: Settings → Secrets and variables → Actions
   - Add as `NVD_API_KEY`

## Project Structure

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
