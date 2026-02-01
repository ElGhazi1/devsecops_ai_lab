from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import sys

app = FastAPI(title="LLM/NLP Threat Detector", version="1.0.0")

# Prevent unsafe local model deserialization by default
DISABLE_LOCAL_MODEL = os.getenv("DISABLE_LOCAL_MODEL", "true").lower() in ("1", "true", "yes")
MODEL_PATH = os.getenv("MODEL_PATH", "")  # allowed only if explicitly enabled
ALLOWED_MODEL_PREFIX = os.getenv("ALLOWED_MODEL_PREFIX", "/app/models/")  # optional allowlist


def load_model_safe(model_identifier: str = "bert-base-uncased"):
    """
    Safe model loading:
     - prefer hub models (hf) via AutoModel.from_pretrained
     - disallow arbitrary local torch.load unless explicitly enabled and within ALLOWED_MODEL_PREFIX
    """
    if DISABLE_LOCAL_MODEL and MODEL_PATH:
        print("⚠️ Local model loading disabled by policy. Set DISABLE_LOCAL_MODEL=false to override (not recommended).")
        raise RuntimeError("Local model loading disabled for security")
    if MODEL_PATH:
        # Only allow local models from trusted folder
        if not os.path.abspath(MODEL_PATH).startswith(os.path.abspath(ALLOWED_MODEL_PREFIX)):
            raise RuntimeError("Local model path not in allowlist")
        # safe loading via transformers API if possible (avoid torch.load)
        try:
            tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=2)
            return tokenizer, model
        except Exception as e:
            print(f"❌ Failed to load local model safely: {e}")
            raise
    # Default: load from Hugging Face hub (safe path)
    tokenizer = AutoTokenizer.from_pretrained(model_identifier)
    model = AutoModelForSequenceClassification.from_pretrained(model_identifier, num_labels=2)
    return tokenizer, model


# Replace previous direct loads with safe loader
try:
    tokenizer, model = load_model_safe(os.getenv("MODEL_NAME", "bert-base-uncased"))
    model.eval()
except Exception as e:
    print(f"Model load failed: {e}")
    sys.exit(1)


class ThreatDetectionRequest(BaseModel):
    text: str
    threshold: float = 0.7


class ThreatDetectionResponse(BaseModel):
    text: str
    is_threat: bool
    confidence: float
    threat_type: str


class BulkThreatDetectionRequest(BaseModel):
    texts: List[str]
    threshold: float = 0.7


class BulkThreatDetectionResponse(BaseModel):
    results: List[ThreatDetectionResponse]
    total_processed: int
    threats_detected: int


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "llm-nlp-service",
        "model": "BERT-base-uncased",
    }


@app.post("/detect-threat", response_model=ThreatDetectionResponse)
async def detect_threat(request: ThreatDetectionRequest):
    """
    Detect if text contains threat patterns (prompt injection, intrusion attempts, etc.)
    Returns threat probability and classification
    """
    try:
        # Tokenize input
        inputs = tokenizer(
            request.text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True,
        )

        # Inference
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)

        threat_score = probabilities[0][1].item()
        is_threat = threat_score >= request.threshold

        threat_type = classify_threat(request.text)

        return ThreatDetectionResponse(
            text=request.text[:100],
            is_threat=is_threat,
            confidence=threat_score,
            threat_type=threat_type,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/detect-threats-batch", response_model=BulkThreatDetectionResponse)
async def detect_threats_batch(request: BulkThreatDetectionRequest):
    """Batch threat detection"""
    results = []
    threats_count = 0

    for text in request.texts:
        single_request = ThreatDetectionRequest(text=text, threshold=request.threshold)
        result = await detect_threat(single_request)
        results.append(result)
        if result.is_threat:
            threats_count += 1

    return BulkThreatDetectionResponse(
        results=results, total_processed=len(request.texts), threats_detected=threats_count
    )


def classify_threat(text: str) -> str:
    """Simple heuristic threat classification"""
    threat_keywords = {
        "injection": ["sql", "injection", "exploit", "payload"],
        "xss": ["script", "alert", "<>", "javascript"],
        "privilege_escalation": ["sudo", "admin", "privilege", "root"],
        "path_traversal": ["../", "..\\", "etc/passwd"],
        "malware": ["malware", "trojan", "virus", "ransomware"],
        "other": [],
    }

    text_lower = text.lower()
    for threat_type, keywords in threat_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            return threat_type

    return "other"


@app.post("/model-stats")
async def model_stats():
    """Get model information"""
    return {
        "model_name": "bert-base-uncased",
        "num_labels": 2,
        "labels": ["safe", "threat"],
        "max_length": 512,
        "framework": "PyTorch",
    }
