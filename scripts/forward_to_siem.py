#!/usr/bin/env python3
"""
Forward security reports to SIEM/SOAR platforms.
Usage: python forward_to_siem.py --report security-report.json
"""
import os
import sys
import json
import argparse
from pathlib import Path
import requests


def send_to_endpoint(url: str, api_key: str, payload: dict, path: str = "/api/events") -> bool:
    if not url or not api_key:
        print("⚠️  Missing endpoint or API key")
        return False
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        resp = requests.post(f"{url.rstrip('/')}{path}", json=payload, headers=headers, timeout=15)
        print(f"→ {url} returned {resp.status_code}")
        return resp.status_code in (200, 201, 202)
    except Exception as e:
        print(f"❌ Error sending to {url}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, help="Path to JSON report")
    args = parser.parse_args()

    report_path = Path(args.report)
    if not report_path.exists():
        print(f"❌ Report not found: {report_path}")
        sys.exit(2)

    try:
        with open(report_path, "r") as f:
            payload = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read report: {e}")
        sys.exit(3)

    success = False

    # Forward to SIEM
    siem_url = os.getenv("SIEM_URL")
    siem_key = os.getenv("SIEM_API_KEY")
    if siem_url and siem_key:
        print(f"Sending report to SIEM: {siem_url}")
        success = send_to_endpoint(siem_url, siem_key, payload, path="/api/events") or success

    # Forward to TheHive (SOAR)
    thehive_url = os.getenv("THEHIVE_URL")
    thehive_key = os.getenv("THEHIVE_API_KEY")
    if thehive_url and thehive_key:
        print(f"Creating case in TheHive: {thehive_url}")
        success = send_to_endpoint(thehive_url, thehive_key, payload, path="/api/case") or success

    # Forward to MISP (CTI) - example endpoint
    misp_url = os.getenv("MISP_URL")
    misp_key = os.getenv("MISP_API_KEY")
    if misp_url and misp_key:
        print(f"Publishing to MISP: {misp_url}")
        success = send_to_endpoint(misp_url, misp_key, payload, path="/events") or success

    # Slack notification (summary)
    slack_webhook = os.getenv("SLACK_WEBHOOK")
    if slack_webhook:
        try:
            findings = payload.get("summary", {}).get("total_issues", "N/A")
            slack_payload = {"text": f"🔔 Security report forwarded: {report_path.name} - issues: {findings}"}
            resp = requests.post(slack_webhook, json=slack_payload, timeout=10)
            print(f"→ Slack returned {resp.status_code}")
            success = success or (resp.status_code == 200)
        except Exception as e:
            print(f"❌ Slack error: {e}")

    if not success:
        print("❌ No forwarding succeeded.")
        sys.exit(4)

    print("✅ Forwarding complete.")
    sys.exit(0)


if __name__ == "__main__":
    main()
