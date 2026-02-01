import json
from typing import Dict, List
from datetime import datetime


class BanditParser:
    def __init__(self, json_report_path: str):
        self.report_path = json_report_path
        self.data = None

    def parse(self) -> Dict:
        """Parse Bandit JSON report"""
        try:
            with open(self.report_path, "r") as f:
                self.data = json.load(f)
        except Exception as e:
            return {"error": str(e), "status": "failed"}

        return {
            "status": "success",
            "total_issues": len(self.data.get("results", [])),
            "issues": self._extract_issues(),
            "metrics": self.data.get("metrics", {}),
            "timestamp": datetime.now().isoformat(),
        }

    def _extract_issues(self) -> List[Dict]:
        """Extract and deduplicate issues"""
        issues = []
        seen = set()

        for result in self.data.get("results", []):
            issue_hash = f"{result['filename']}:{result['line_number']}:{result['test_id']}"

            if issue_hash not in seen:
                seen.add(issue_hash)
                issues.append(
                    {
                        "severity": result.get("severity", "UNKNOWN"),
                        "confidence": result.get("confidence", "UNKNOWN"),
                        "type": result.get("test_id", "UNKNOWN"),
                        "message": result.get("issue_text", ""),
                        "file": result.get("filename", ""),
                        "line": result.get("line_number", 0),
                    }
                )

        return issues
