#!/bin/bash
# Run all tests locally

echo "🧪 Running unit tests..."
pytest tests/unit -v

echo "🔒 Running security tests..."
pytest tests/security -v

echo "✅ Tests complete!"
