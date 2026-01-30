import json
import csv
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create directories
Path('logs').mkdir(exist_ok=True)
Path('reports').mkdir(exist_ok=True)

def generate_json_report():
    """Generate sample JSON security report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "scan_type": "python_code_analysis",
        "status": "completed",
        "findings": [
            {
                "id": "FINDING-001",
                "severity": "HIGH",
                "category": "Code Quality",
                "description": "Missing error handling",
                "file": "src/api/main.py",
                "line": 42
            },
            {
                "id": "FINDING-002",
                "severity": "MEDIUM",
                "category": "Best Practice",
                "description": "Unused import",
                "file": "src/models/bert_classifier.py",
                "line": 5
            }
        ],
        "summary": {
            "total_findings": 2,
            "critical": 0,
            "high": 1,
            "medium": 1,
            "low": 0
        }
    }
    
    report_path = Path('reports/security_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"✓ JSON report generated: {report_path}")
    return report

def generate_csv_report():
    """Generate sample CSV findings report"""
    findings = [
        ["Finding ID", "Severity", "Category", "Description", "File", "Line"],
        ["FINDING-001", "HIGH", "Code Quality", "Missing error handling", "src/api/main.py", "42"],
        ["FINDING-002", "MEDIUM", "Best Practice", "Unused import", "src/models/bert_classifier.py", "5"],
    ]
    
    report_path = Path('reports/findings.csv')
    with open(report_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(findings)
    
    logger.info(f"✓ CSV report generated: {report_path}")

if __name__ == "__main__":
    logger.info("Starting report generation...")
    generate_json_report()
    generate_csv_report()
    logger.info("✓ All reports generated successfully!")
