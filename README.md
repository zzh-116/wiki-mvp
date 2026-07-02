# Wiki MVP

A minimal wiki application built with FastAPI.

## Project Structure

```
wiki-mvp/
├── app/              # Application code
│   ├── api/          # API endpoints
│   ├── services/     # Business logic
│   ├── models/       # Data models
│   ├── core/         # Core utilities & config
│   └── main.py       # Application entry point
├── data/             # Data storage
│   ├── uploads/      # Uploaded files
│   └── chunks/       # Document chunks
├── docker/           # Docker configuration
├── docker-compose.yml
└── README.md
```

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

## Docker

```bash
docker-compose up --build
```
