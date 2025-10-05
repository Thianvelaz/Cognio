# Cognio - Quick Start Guide

## What is Cognio?

Cognio is a persistent semantic memory server for MCP (Model Context Protocol). It gives AI assistants long-term memory that survives across sessions with semantic search capabilities.

## Quick Setup

### Option 1: Docker (Easiest)

```bash
# Clone and run
git clone https://github.com/0xReLogic/Cognio.git
cd Cognio
docker-compose up -d

# Test
curl http://localhost:8080/health
```

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Or use Poetry
poetry install

# Run server
uvicorn src.main:app --reload

# Server runs on http://localhost:8080
```

## Basic Usage

### Save a Memory

```bash
curl -X POST http://localhost:8080/memory/save \
  -H "Content-Type: application/json" \
  -d '{"text": "Python is great for AI", "project": "LEARNING", "tags": ["python", "ai"]}'
```

### Search Memories

```bash
curl "http://localhost:8080/memory/search?q=artificial%20intelligence&limit=5"
```

### List All Memories

```bash
curl "http://localhost:8080/memory/list?page=1&limit=10"
```

### Get Statistics

```bash
curl http://localhost:8080/memory/stats
```

## API Endpoints

- `GET /` - Root info
- `GET /health` - Health check
- `POST /memory/save` - Save memory
- `GET /memory/search` - Semantic search
- `GET /memory/list` - List all memories
- `DELETE /memory/{id}` - Delete memory
- `POST /memory/bulk-delete` - Bulk delete
- `GET /memory/stats` - Statistics
- `GET /memory/export` - Export data

## Configuration

Edit `.env` file (copy from `.env.example`):

```bash
DB_PATH=./data/memory.db
EMBED_MODEL=all-MiniLM-L6-v2
API_PORT=8080
LOG_LEVEL=info
```

## Development

```bash
# Run tests
pytest

# Format code
black src/ tests/

# Lint
ruff check src/

# Type check
mypy src/
```

## MCP Integration

Add to your MCP client config:

```json
{
  "mcpServers": {
    "memory": {
      "type": "http",
      "url": "http://localhost:8080"
    }
  }
}
```

## Project Structure

```
cognio/
├── src/              # Source code
├── tests/            # Tests
├── examples/         # Usage examples
├── scripts/          # Utility scripts
├── Dockerfile        # Container
└── requirements.txt  # Dependencies
```

## Need Help?

- Issues: https://github.com/0xReLogic/Cognio/issues
- Discussions: https://github.com/0xReLogic/Cognio/discussions

## License

MIT License - See LICENSE file
