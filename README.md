# FastAPI Testing Lab (Unit Testing & Integration Testing)

คู่มือปฏิบัติการ Unit Testing และ Integration Testing สำหรับ FastAPI ด้วย pytest, Postman, Newman และ GitHub Actions
รายวิชา **Software Engineering**

## โครงสร้างโปรเจกต์ (Project Structure)

```text
fastapi-testing-lab/
├── app/
│   ├── __init__.py
│   ├── errors.py
│   ├── auth.py
│   ├── main.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── product_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── product_service.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       └── products.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_product_service.py
│   └── integration/
│       ├── __init__.py
│       └── test_products_api.py
├── postman/
│   ├── API-Testing-Lab.postman_collection.json
│   ├── local.postman_environment.json
│   └── data/
│       └── products.csv
├── scripts/
│   └── run_postman.py
├── .github/
│   └── workflows/
│       └── api-tests.yml
├── requirements.txt
├── pytest.ini
└── .gitignore
```

## วิธีการรันโปรเจกต์ (How to Run)

### 1. ติดตั้ง Dependencies
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. รัน Server
```bash
uvicorn app.main:app --reload --port 8000
```
เปิดเอกสาร API Interactive Swagger UI ได้ที่: `http://127.0.0.1:8000/docs`

### 3. รัน Unit Tests และ Integration Tests (pytest)
```bash
# Unit Tests
pytest tests/unit -v

# Integration Tests
pytest tests/integration -v

# Code Coverage
pytest --cov=app --cov-report=term-missing
```

### 4. รัน Newman อัตโนมัติ (Automated API Test Runner)
```bash
npm install -g newman newman-reporter-htmlextra
python scripts/run_postman.py
```
รายงานผล HTML จะถูกบันทึกไว้ที่ `reports/postman-report.html`
