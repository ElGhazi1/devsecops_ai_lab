import json
from typing import Dict, List
from datetime import datetime


class SemgrepParser:
    def __init__(self, json_report_path: str):
        self.report_path = json_report_path
        self.data = None

    def parse(self) -> Dict:
        """Parse Semgrep JSON report"""
        try:
            with open(self.report_path, "r") as f:
                self.data = json.load(f)
        except Exception as e:
            return {"error": str(e), "status": "failed"}

        return {
            "status": "success",
            "total_findings": len(self.data.get("results", [])),
            "findings": self._extract_findings(),
            "errors": self.data.get("errors", []),
            "timestamp": datetime.now().isoformat(),
        }

    def _extract_findings(self) -> List[Dict]:
        """Extract and deduplicate findings"""
        findings = []
        seen = set()

        for result in self.data.get("results", []):
            finding_hash = f"{result['path']}:{result['start']['line']}:{result['rule_id']}"

            if finding_hash not in seen:
                seen.add(finding_hash)
                findings.append(
                    {
                        "rule_id": result.get("rule_id", "UNKNOWN"),
                        "message": result.get("extra", {}).get("message", ""),
                        "severity": result.get("extra", {}).get("severity", "INFO"),
                        "file": result.get("path", ""),
                        "line": result.get("start", {}).get("line", 0),
                        "cwe": result.get("extra", {}).get("cwe", []),
                    }
                )

        return findings
