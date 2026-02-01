import json
from datetime import datetime
from typing import Dict, List
from jinja2 import Template


class SecurityReportGenerator:
    def __init__(self):
        self.timestamp = datetime.now()
        self.findings = {
            "bandit": [],
            "semgrep": [],
            "safety": [],
            "trivy": [],
            "threats": [],
        }

    def add_bandit_findings(self, findings: List[Dict]):
        self.findings["bandit"] = findings

    def add_semgrep_findings(self, findings: List[Dict]):
        self.findings["semgrep"] = findings

    def add_safety_findings(self, findings: List[Dict]):
        self.findings["safety"] = findings

    def add_trivy_findings(self, findings: List[Dict]):
        self.findings["trivy"] = findings

    def add_threat_detections(self, findings: List[Dict]):
        self.findings["threats"] = findings

    def generate_json_report(self, output_path: str):
        """Generate JSON report"""
        report = {
            "timestamp": self.timestamp.isoformat(),
            "summary": self._generate_summary(),
            "findings": self.findings,
        }

        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

        return report

    def generate_html_report(self, output_path: str):
        """Generate HTML report"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Security Report</title>
            <style>
                body { font-family: Arial; margin: 20px; }
                .summary { background: #f0f0f0; padding: 10px; margin: 10px 0; }
                .high { color: red; font-weight: bold; }
                .medium { color: orange; font-weight: bold; }
                .low { color: green; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #4CAF50; color: white; }
            </style>
        </head>
        <body>
            <h1>Security Assessment Report</h1>
            <p>Generated: {{ timestamp }}</p>
            <div class="summary">
                <h2>Summary</h2>
                <p>Total Issues: <strong>{{ total_issues }}</strong></p>
                <p>Critical: <strong>{{ critical }}</strong></p>
                <p>High: <strong>{{ high }}</strong></p>
                <p>Medium: <strong>{{ medium }}</strong></p>
                <p>Low: <strong>{{ low }}</strong></p>
            </div>
            <h2>Bandit Findings (Python Security)</h2>
            <table>
                <tr><th>File</th><th>Line</th><th>Severity</th><th>Issue</th></tr>
                {% for issue in bandit %}
                <tr><td>{{ issue.file }}</td><td>{{ issue.line }}</td><td class="{{ issue.severity.lower() }}">{{ issue.severity }}</td><td>{{ issue.message }}</td></tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """

        summary = self._generate_summary()
        template = Template(html_template)
        html_content = template.render(
            timestamp=self.timestamp.isoformat(),
            total_issues=sum(len(v) for v in self.findings.values()),
            critical=summary.get("critical", 0),
            high=summary.get("high", 0),
            medium=summary.get("medium", 0),
            low=summary.get("low", 0),
            bandit=self.findings["bandit"],
        )

        with open(output_path, "w") as f:
            f.write(html_content)

    def _generate_summary(self) -> Dict:
        """Generate summary statistics"""
        summary = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}

        for findings_list in self.findings.values():
            for finding in findings_list:
                severity = finding.get("severity", "info").lower()
                if severity in summary:
                    summary[severity] += 1

        return summary
