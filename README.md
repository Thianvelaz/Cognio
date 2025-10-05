# Cognio

> Persistent semantic memory server for MCP - Long-term context that survives across AI conversations

Cognio is a Model Context Protocol (MCP) server that provides persistent memory layer for AI assistants like Claude, Copilot, or local LLMs. Unlike ephemeral memory that disappears after each session, Cognio stores context permanently and enables semantic search based on meaning, not just keywords.

## Features

- **Semantic Search**: Find memories by meaning, not just exact matches
- **Persistent Storage**: SQLite-based storage that survives across sessions
- **Project Organization**: Organize memories by project and tags
- **Deduplication**: Automatic detection of duplicate memories
- **Easy Deployment**: Docker support for simple setup
- **RESTful API**: Standard HTTP API for easy integration

## Quick Start

### Using Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/0xReLogic/Cognio.git
cd Cognio

# Start server
docker-compose up -d

# Test it
curl http://localhost:8080/health
```

### Using Poetry

```bash
# Install dependencies
poetry install

# Run server
poetry run uvicorn src.main:app --reload

# In another terminal, test it
curl http://localhost:8080/health
```

## Usage Examples

### Save a Memory

```bash
curl -X POST http://localhost:8080/memory/save \
  -H "Content-Type: application/json" \
  -d '{
    "text": "QRIS refund flow requires webhook validation at callback_url",
    "project": "SENTINEL",
    "tags": ["qris", "refund", "webhook"]
  }'
```

### Search Memories

```bash
curl "http://localhost:8080/memory/search?q=QRIS%20refund&project=SENTINEL&limit=5"
```

### List All Memories

```bash
curl "http://localhost:8080/memory/list?page=1&limit=10"
```

### Get Statistics

```bash
curl http://localhost:8080/memory/stats
```

### Delete a Memory

```bash
curl -X DELETE http://localhost:8080/memory/{memory-id}
```

## MCP Integration

Add to your MCP client configuration (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "memory": {
      "type": "http",
      "url": "http://localhost:8080",
      "description": "Long-term semantic memory"
    }
  }
}
```

## API Documentation

Once the server is running, visit:
- **Interactive API docs**: http://localhost:8080/docs
- **OpenAPI schema**: http://localhost:8080/openapi.json

## Configuration

Create a `.env` file (see `.env.example`):

```bash
# Database
DB_PATH=./data/memory.db

# Embeddings
EMBED_MODEL=all-MiniLM-L6-v2
EMBED_DEVICE=cpu

# API
API_HOST=0.0.0.0
API_PORT=8080

# Search
DEFAULT_SEARCH_LIMIT=5
SIMILARITY_THRESHOLD=0.7

# Logging
LOG_LEVEL=info
```

## Project Structure

```
cognio/
├── src/
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration
│   ├── models.py        # Pydantic models
│   ├── database.py      # SQLite operations
│   ├── embeddings.py    # Sentence transformers
│   ├── memory.py        # Core memory logic
│   └── utils.py         # Helper functions
├── tests/               # Unit and integration tests
├── Dockerfile           # Container image
├── docker-compose.yml   # Docker orchestration
└── pyproject.toml       # Dependencies
```

## Development

### Setup

```bash
# Install dev dependencies
poetry install

# Run tests
poetry run pytest

# Run linter
poetry run ruff check src/

# Format code
poetry run black src/
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test file
poetry run pytest tests/test_api.py
```

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: SQLite
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Protocol**: MCP over HTTP

## Performance

- **Save memory**: < 50ms
- **Search (1k memories)**: < 100ms
- **Embedding generation**: < 10ms/text
- **Storage**: ~1KB per memory

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/0xReLogic/Cognio/issues)
- **Discussions**: [GitHub Discussions](https://github.com/0xReLogic/Cognio/discussions)

## Roadmap

- [x] v0.1.0: Basic CRUD and semantic search
- [ ] v1.0.0: Production-ready with full test coverage
- [ ] v1.1.0: Web UI and export features
- [ ] v1.2.0: Advanced search and clustering
- [ ] v2.0.0: Multi-user support and integrations

---

Made with care for better AI conversations
