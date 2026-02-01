"""
Generate comprehensive security reports from scanning artifacts.
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from jinja2 import Template

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate security reports from various scanners."""

    def __init__(self, artifact_dir: str = "./artifacts"):
        self.artifact_dir = Path(artifact_dir)
        self.findings = {
            "bandit": [],
            "semgrep": [],
            "safety": [],
            "trivy": [],
            "pylint": [],
        }

    def load_bandit_report(self, report_path: str) -> List[Dict]:
        """Load Bandit JSON report."""
        try:
            with open(report_path) as f:
                data = json.load(f)
                return data.get("results", [])
        except FileNotFoundError:
            logger.warning(f"Bandit report not found: {report_path}")
            return []

    def load_semgrep_report(self, report_path: str) -> List[Dict]:
        """Load Semgrep JSON report."""
        try:
            with open(report_path) as f:
                data = json.load(f)
                return data.get("results", [])
        except FileNotFoundError:
            logger.warning(f"Semgrep report not found: {report_path}")
            return []

    def load_safety_report(self, report_path: str) -> List[Dict]:
        """Load Safety JSON report."""
        try:
            with open(report_path) as f:
                data = json.load(f)
                # Safety returns different format
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            logger.warning(f"Safety report not found: {report_path}")
            return []

    def deduplicate_findings(self, findings: List[Dict]) -> List[Dict]:
        """Remove duplicate findings."""
        seen = set()
        unique_findings = []

        for finding in findings:
            finding_hash = f"{finding.get('file', '')}:{finding.get('line', 0)}:{finding.get('id', '')}"
            if finding_hash not in seen:
                seen.add(finding_hash)
                unique_findings.append(finding)

        return unique_findings

    def aggregate_findings(self) -> Dict[str, Any]:
        """Aggregate all findings."""
        aggregated = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_issues": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "info": 0,
            },
            "by_scanner": {},
            "by_severity": {},
        }

        for scanner_name, findings in self.findings.items():
            findings = self.deduplicate_findings(findings)
            aggregated["by_scanner"][scanner_name] = {
                "count": len(findings),
                "findings": findings[:10],  # Top 10 only
            }
            aggregated["summary"]["total_issues"] += len(findings)

            for finding in findings:
                severity = finding.get("severity", "info").lower()
                if severity in aggregated["summary"]:
                    aggregated["summary"][severity] += 1

        return aggregated

    def generate_html_report(self, aggregated: Dict, output_file: str = "security-report.html"):
        """Generate HTML report."""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Security Report</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana; margin: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
                h1 { color: #d32f2f; }
                .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
                .stat-card { background: #f9f9f9; padding: 15px; border-radius: 4px; border-left: 4px solid #d32f2f; }
                .stat-number { font-size: 24px; font-weight: bold; }
                .stat-label { color: #666; }
                .critical { color: #d32f2f; font-weight: bold; }
                .high { color: #f57c00; }
                .medium { color: #fbc02d; }
                .low { color: #388e3c; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #f5f5f5; font-weight: bold; }
                .scanner-section { margin: 30px 0; }
                footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔒 Security Assessment Report</h1>
                <p><strong>Generated:</strong> {{ timestamp }}</p>
                
                <div class="summary">
                    <div class="stat-card">
                        <div class="stat-number critical">{{ summary.total_issues }}</div>
                        <div class="stat-label">Total Issues</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number critical">{{ summary.critical }}</div>
                        <div class="stat-label">Critical</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number high">{{ summary.high }}</div>
                        <div class="stat-label">High</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number medium">{{ summary.medium }}</div>
                        <div class="stat-label">Medium</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number low">{{ summary.low }}</div>
                        <div class="stat-label">Low</div>
                    </div>
                </div>

                {% for scanner, data in by_scanner.items() %}
                <div class="scanner-section">
                    <h2>{{ scanner|upper }} - {{ data.count }} Issues</h2>
                    {% if data.findings %}
                    <table>
                        <tr>
                            <th>File</th>
                            <th>Line</th>
                            <th>Severity</th>
                            <th>Issue</th>
                        </tr>
                        {% for finding in data.findings %}
                        <tr>
                            <td>{{ finding.file|default('N/A') }}</td>
                            <td>{{ finding.line|default('N/A') }}</td>
                            <td class="{{ finding.severity|default('low')|lower }}">{{ finding.severity|default('LOW') }}</td>
                            <td>{{ finding.message|default(finding.issue|default('N/A')) }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                    {% else %}
                    <p><strong>✅ No issues found</strong></p>
                    {% endif %}
                </div>
                {% endfor %}

                <footer>
                    <p>Report generated by DevSecOps Automation Pipeline</p>
                    <p>For questions or issues, please contact the security team.</p>
                </footer>
            </div>
        </body>
        </html>
        """

        template = Template(html_template)
        html_content = template.render(
            timestamp=aggregated["timestamp"],
            summary=aggregated["summary"],
            by_scanner=aggregated["by_scanner"],
        )

        with open(output_file, "w") as f:
            f.write(html_content)

        logger.info(f"HTML report generated: {output_file}")

    def generate_json_report(self, aggregated: Dict, output_file: str = "security-report.json"):
        """Generate JSON report."""
        with open(output_file, "w") as f:
            json.dump(aggregated, f, indent=2)

        logger.info(f"JSON report generated: {output_file}")

    def generate_reports(self, output_dir: str = "."):
        """Generate all reports."""
        aggregated = self.aggregate_findings()

        self.generate_json_report(aggregated, f"{output_dir}/security-report.json")
        self.generate_html_report(aggregated, f"{output_dir}/security-report.html")

        return aggregated


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    generator = ReportGenerator(artifact_dir="./artifacts")

    # Load reports
    generator.findings["bandit"] = generator.load_bandit_report("./artifacts/bandit-report.json")
    generator.findings["semgrep"] = generator.load_semgrep_report("./artifacts/semgrep.json")
    generator.findings["safety"] = generator.load_safety_report("./artifacts/safety.json")

    # Generate reports
    generator.generate_reports(output_dir="./reports")
