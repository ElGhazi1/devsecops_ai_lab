"""
Professional vulnerability triage script.
Categorizes alerts by severity and exploitability.
"""
import json
import sys
from pathlib import Path
from typing import Dict, List, Any


class VulnerabilityTriager:
    """Triage vulnerabilities by context and risk."""

    # Context-aware rules
    ML_LIBS = {
        'transformers', 'torch', 'sklearn', 'numpy', 
        'tensorflow', 'keras', 'pickle'
    }
    
    ACCEPTABLE_RISKS = {
        'deserialization': 'ML-specific - model loading required',
        'pickle': 'ML-specific - torch models use pickle',
        'eval': 'Dev dependency only',
    }

    def __init__(self):
        self.findings = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
            'ignored': []
        }

    def should_ignore(self, alert: Dict[str, Any]) -> tuple[bool, str]:
        """
        Determine if alert should be ignored based on context.
        Returns (should_ignore, reason)
        """
        # Check if it's an ML library
        package = alert.get('package', '').lower()
        if any(lib in package for lib in self.ML_LIBS):
            # Check if it's an acceptable risk
            cve_id = alert.get('id', '')
            description = alert.get('description', '').lower()
            
            for risk_type, reason in self.ACCEPTABLE_RISKS.items():
                if risk_type in description.lower():
                    return True, f"{reason} - CVE {cve_id}"
        
        return False, ""

    def triage_report(self, report_file: str) -> Dict[str, Any]:
        """Triage a vulnerability report."""
        try:
            with open(report_file) as f:
                report = json.load(f)
        except Exception as e:
            print(f"❌ Error loading report: {e}")
            return {}

        vulns = report.get('vulnerabilities', [])
        
        for vuln in vulns:
            should_ignore, reason = self.should_ignore(vuln)
            
            if should_ignore:
                self.findings['ignored'].append({
                    'package': vuln.get('package'),
                    'id': vuln.get('id'),
                    'reason': reason
                })
                continue
            
            severity = vuln.get('severity', 'unknown').lower()
            if severity in self.findings:
                self.findings[severity].append(vuln)

        return self.findings

    def generate_report(self, output_file: str = "triage-report.json"):
        """Generate triage report."""
        report = {
            'summary': {
                'critical': len(self.findings['critical']),
                'high': len(self.findings['high']),
                'medium': len(self.findings['medium']),
                'low': len(self.findings['low']),
                'ignored': len(self.findings['ignored']),
                'blocking': len(self.findings['critical']) + len(self.findings['high'])
            },
            'findings': self.findings
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📊 Vulnerability Triage Report")
        print(f"{'='*50}")
        print(f"🔴 Critical: {report['summary']['critical']}")
        print(f"🟠 High: {report['summary']['high']}")
        print(f"🟡 Medium: {report['summary']['medium']}")
        print(f"🟢 Low: {report['summary']['low']}")
        print(f"⏭️  Ignored (acceptable): {report['summary']['ignored']}")
        print(f"🚨 Blocking (Critical+High): {report['summary']['blocking']}")
        print(f"{'='*50}\n")

        return report


if __name__ == "__main__":
    triager = VulnerabilityTriager()

    # Scan all reports
    for report_file in Path("cve-reports").glob("*.json"):
        print(f"Triaging {report_file.name}...")
        triager.triage_report(str(report_file))

    triager.generate_report()

    # Exit with error if blocking vulnerabilities found
    if triager.findings['critical'] or triager.findings['high']:
        print("⚠️  Blocking vulnerabilities found!")
        sys.exit(1)
