# DevSecOps AI Lab

Simple AI/ML project with sentiment classification using HuggingFace transformers.

## Setup

```bash
pip install -r requirements.txt
```

## Running Locally

```bash
python -m src.api.main
```

API will be available at `http://localhost:5000`

## API Endpoints

- **GET** `/health` - Health check
- **POST** `/predict` - Single text prediction
  ```json
  {"text": "This is amazing!"}
  ```
- **POST** `/batch-predict` - Multiple texts
  ```json
  {"texts": ["text1", "text2"]}
  ```

## Docker

```bash
docker-compose up
```

## Testing

```bash
pytest tests/ -v
```

## HuggingFace Models

**No API key or sign-in required!** Models are automatically downloaded on first use and cached locally. The `distilbert-base-uncased-finetuned-sst-2-english` model is lightweight and runs on CPU.

## Git Commands to Test

```bash
git clone <repo>
git checkout -b feature/new-feature
git add .
git commit -m "message"
git push origin feature/new-feature
git pull origin main
```
# devsecops_ai_lab
