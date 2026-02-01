"""
Analyze security logs and generate insights.
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class LogAnalyzer:
    """Analyze security and application logs."""

    def __init__(self, log_dir: str = "./logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

    def parse_json_logs(self, log_file: str) -> List[Dict[str, Any]]:
        """Parse JSON formatted logs."""
        logs = []
        try:
            with open(log_file, "r") as f:
                for line in f:
                    try:
                        logs.append(json.loads(line))
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse log line: {line}")
                        continue
        except FileNotFoundError:
            logger.error(f"Log file not found: {log_file}")
        return logs

    def extract_security_events(self, logs: List[Dict]) -> List[Dict]:
        """Extract security-relevant events."""
        security_events = []
        security_keywords = ["threat", "error", "unauthorized", "injection", "attack"]

        for log in logs:
            if any(keyword in str(log).lower() for keyword in security_keywords):
                security_events.append(log)

        return security_events

    def generate_summary(self, logs: List[Dict]) -> Dict[str, Any]:
        """Generate summary statistics."""
        summary = {
            "total_logs": len(logs),
            "security_events": 0,
            "errors": 0,
            "warnings": 0,
            "timestamp_range": {
                "start": None,
                "end": None,
            },
            "event_counts": {},
        }

        for log in logs:
            level = log.get("level", "unknown").upper()
            if level == "ERROR":
                summary["errors"] += 1
            elif level == "WARNING":
                summary["warnings"] += 1

            event_type = log.get("type", "unknown")
            summary["event_counts"][event_type] = summary["event_counts"].get(event_type, 0) + 1

        return summary

    def export_report(self, summary: Dict, output_file: str = "log_analysis.json"):
        """Export analysis report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "analysis": summary,
        }

        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Report exported to {output_file}")
        return report


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    analyzer = LogAnalyzer()

    # Example usage
    logs = analyzer.parse_json_logs("security.log")
    security_events = analyzer.extract_security_events(logs)
    summary = analyzer.generate_summary(logs)

    print(f"Total logs: {summary['total_logs']}")
    print(f"Security events: {len(security_events)}")
    print(f"Errors: {summary['errors']}")

    analyzer.export_report(summary)
