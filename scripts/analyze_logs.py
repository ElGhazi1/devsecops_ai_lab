import json
import logging
from pathlib import Path
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_logs():
    """Parse and summarize logs"""
    log_file = Path('logs/analysis.log')
    
    if not log_file.exists():
        logger.warning("No logs found")
        return
    
    stats = defaultdict(int)
    
    with open(log_file, 'r') as f:
        for line in f:
            if 'ERROR' in line:
                stats['errors'] += 1
            elif 'WARNING' in line:
                stats['warnings'] += 1
            elif 'INFO' in line:
                stats['info'] += 1
    
    # Save summary
    summary_path = Path('reports/log_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(dict(stats), f, indent=2)
    
    logger.info(f"Log analysis: {dict(stats)}")
    return stats

if __name__ == "__main__":
    analyze_logs()
