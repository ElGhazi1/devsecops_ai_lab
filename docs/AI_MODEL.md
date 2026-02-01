# 🤖 AI/ML Model Documentation

## BERT Model Overview

### Model Details
- **Architecture**: BERT-base-uncased
- **Task**: Binary Classification (Safe/Threat)
- **Layers**: 12 transformer layers
- **Parameters**: 110M
- **Max Sequence Length**: 512 tokens
- **Framework**: PyTorch + Transformers

### Input/Output

#### Input
```python
{
  "text": "SELECT * FROM users WHERE id = 1",
  "threshold": 0.7
}
```

#### Output
```python
{
  "text": "SELECT * FROM users...",
  "is_threat": True,
  "confidence": 0.95,
  "threat_type": "injection"
}
```

## Threat Classification

### Threat Types
1. **injection** - SQL/NoSQL/Command injection
2. **xss** - Cross-site scripting
3. **privilege_escalation** - Elevation attacks
4. **path_traversal** - Directory traversal
5. **malware** - Malicious payloads
6. **other** - Unclassified threats

### Classification Heuristics
```python
threat_keywords = {
    "injection": ["sql", "injection", "exploit", "payload"],
    "xss": ["script", "alert", "<>", "javascript"],
    "privilege_escalation": ["sudo", "admin", "privilege", "root"],
    "path_traversal": ["../", "..\\", "etc/passwd"],
    "malware": ["malware", "trojan", "virus", "ransomware"],
}
```

## Performance Metrics

### Inference Speed
- **CPU**: ~200ms per request
- **GPU**: ~50ms per request

### Model Size
- **Compressed**: ~250 MB
- **Uncompressed**: ~440 MB

## Fine-tuning

### Dataset Requirements
- Minimum: 500 labeled examples
- Balanced: 50% safe, 50% threat
- Format: CSV with `text` and `label` columns

### Training Script
```bash
python notebooks/train_bert_classifier.ipynb
```

### Fine-tuning Parameters
- **Learning Rate**: 2e-5
- **Batch Size**: 32
- **Epochs**: 3
- **Optimizer**: AdamW

## API Endpoints

### Single Threat Detection
```bash
POST /detect-threat
{
  "text": "string",
  "threshold": 0.7
}
```

### Batch Threat Detection
```bash
POST /detect-threats-batch
{
  "texts": ["string1", "string2"],
  "threshold": 0.7
}
```

### Model Stats
```bash
GET /model-stats
```

## Monitoring

### Key Metrics
- **Inference Latency**: p50, p95, p99
- **Model Accuracy**: Precision, Recall, F1
- **Throughput**: Requests per second
- **Error Rate**: Failed predictions

### Logging
```python
import logging
logger = logging.getLogger(__name__)
logger.info(f"Threat detected: {text} ({confidence:.2f})")
```

## Future Improvements

- [ ] Fine-tune on custom dataset
- [ ] Add uncertainty estimation (Bayesian)
- [ ] Implement model versioning
- [ ] Add A/B testing framework
- [ ] Deploy with TorchServe for scaling
- [ ] Implement model monitoring (Evidently AI)
