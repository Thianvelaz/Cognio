# Cognio

> Persistent semantic memory server for MCP - Long-term context that survives across AI conversations

[![CI/CD](https://github.com/0xReLogic/Cognio/actions/workflows/ci.yml/badge.svg)](https://github.com/0xReLogic/Cognio/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.118.0-009688.svg)](https://fastapi.tiangolo.com)

Cognio is a Model Context Protocol (MCP) server that provides persistent memory layer for AI assistants like Claude, Copilot, or local LLMs. Unlike ephemeral memory that disappears after each session, Cognio stores context permanently and enables semantic search based on meaning, not just keywords.

**Perfect for:**
- Personal knowledge base that grows over time
- Multi-project context that stays consistent
- Research notes and learning journal
- Conversation history that can be queried semantically

## Features

- **Semantic Search**: Find memories by meaning using sentence-transformers (all-MiniLM-L6-v2)
- **Persistent Storage**: SQLite-based storage that survives across sessions
- **Project Organization**: Organize memories by project and tags
- **Date Range Filtering**: Search memories within specific time ranges
- **Relevance Sorting**: Sort results by semantic similarity to query
- **Deduplication**: Automatic detection of duplicate memories with SHA256 hashing
- **API Authentication**: Optional API key protection for sensitive endpoints
- **CORS Support**: Cross-origin requests enabled for web applications
- **Export Capabilities**: Export memories to JSON or Markdown format
- **Statistics Dashboard**: View memory counts by project and popular tags
- **Easy Deployment**: Docker support with docker-compose for simple setup
- **RESTful API**: Standard HTTP API with automatic OpenAPI documentation
- **Migration System**: Database versioning for schema upgrades
- **CI/CD Pipeline**: Automated testing and Docker builds with GitHub Actions

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

The server will be available at `http://localhost:8080` with data persisted in `./data/memory.db`.

### Manual Installation

```bash
# Clone repository
git clone https://github.com/0xReLogic/Cognio.git
cd Cognio

# Install dependencies
pip install -r requirements.txt

# Run server
python src/main.py

# In another terminal, test it
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
# Basic semantic search
curl "http://localhost:8080/memory/search?q=QRIS%20refund&limit=5"

# Search with project filter
curl "http://localhost:8080/memory/search?q=QRIS%20refund&project=SENTINEL&limit=5"

# Search with date range
curl "http://localhost:8080/memory/search?q=webhook&after_date=2025-01-01&before_date=2025-12-31"

# Search with custom similarity threshold
curl "http://localhost:8080/memory/search?q=payment&threshold=0.6"
```

### List All Memories

```bash
# List with pagination
curl "http://localhost:8080/memory/list?page=1&limit=10"

# Filter by project
curl "http://localhost:8080/memory/list?project=SENTINEL&page=1&limit=10"

# Sort by relevance with query
curl "http://localhost:8080/memory/list?sort=relevance&q=payment&page=1&limit=10"

# Sort by date (default)
curl "http://localhost:8080/memory/list?sort=date&page=1&limit=10"
```

### Get Statistics

```bash
curl http://localhost:8080/memory/stats
```

### Delete a Memory

```bash
# Delete single memory by ID
curl -X DELETE http://localhost:8080/memory/{memory-id}

# Bulk delete by project
curl -X POST http://localhost:8080/memory/bulk-delete \
  -H "Content-Type: application/json" \
  -d '{"project": "OLD_PROJECT"}'
```

### Export Memories

```bash
# Export to JSON
curl "http://localhost:8080/memory/export?format=json" > memories.json

# Export to Markdown
curl "http://localhost:8080/memory/export?format=markdown" > memories.md

# Export with project filter
curl "http://localhost:8080/memory/export?format=json&project=SENTINEL" > sentinel.json
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

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/memory/save` | Save new memory 🔒 |
| POST | `/memory/search` | Semantic search |
| GET | `/memory/list` | List memories with filters |
| DELETE | `/memory/{id}` | Delete memory by ID 🔒 |
| POST | `/memory/bulk-delete` | Bulk delete by project 🔒 |
| GET | `/memory/stats` | Get statistics |
| GET | `/memory/export` | Export memories |

🔒 = Protected with API key (if configured)

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
API_KEY=your-secret-key-here  # Optional: Enable API authentication

# Search
DEFAULT_SEARCH_LIMIT=5
SIMILARITY_THRESHOLD=0.7

# Logging
LOG_LEVEL=info
```

### API Authentication

To enable API key authentication, set the `API_KEY` environment variable:

```bash
export API_KEY=your-secret-key-here
```

Then include the key in your requests:

```bash
curl -X POST http://localhost:8080/memory/save \
  -H "X-API-Key: your-secret-key-here" \
  -H "Content-Type: application/json" \
  -d '{"text": "Protected memory", "project": "SECURE"}'
```

Protected endpoints: `/memory/save`, `/memory/{id}`, `/memory/bulk-delete`

## Project Structure

```
cognio/
├── README.md                    # Main documentation
├── QUICKSTART.md               # Quick start guide
├── CONTRIBUTING.md             # Contributing guidelines
├── LICENSE                     # MIT License
├── pyproject.toml             # Poetry config
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker orchestration
├── Dockerfile                 # Container image
├── .env.example              # Environment template
│
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI/CD
│
├── src/
│   ├── __init__.py
│   ├── main.py               # FastAPI application
│   ├── config.py             # Configuration (env vars)
│   ├── models.py             # Pydantic schemas
│   ├── database.py           # SQLite operations
│   ├── embeddings.py         # Sentence transformers
│   ├── memory.py             # Core memory logic (CRUD)
│   └── utils.py              # Helper functions
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py           # API integration tests
│   ├── test_memory.py        # Memory service tests
│   ├── test_embeddings.py   # Embedding tests
│   └── test_utils.py         # Utility tests
│
├── scripts/
│   ├── setup.sh              # First-time setup
│   ├── backup.sh             # Backup database
│   └── migrate.py            # Database migrations
│
└── examples/
    ├── basic_usage.py        # Python examples
    ├── curl_examples.sh      # cURL examples
    └── mcp_config.json       # MCP client config
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
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_memory.py::test_save_memory -v

# Run with verbose output
pytest -v --tb=short
```

### Database Migrations

```bash
# Run migrations (auto-detects database)
python scripts/migrate.py

# Run migrations on specific database
python scripts/migrate.py ./data/memory.db
```

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI 0.118.0
- **Database**: SQLite with JSON support
- **Embeddings**: sentence-transformers 2.7.0 (all-MiniLM-L6-v2, 384 dimensions)
- **Server**: Uvicorn 0.37.0 with uvloop
- **Testing**: pytest 8.4.2, pytest-asyncio, pytest-cov
- **Code Quality**: ruff, black, mypy
- **Protocol**: MCP over HTTP
- **Container**: Docker with docker-compose

### Why These Choices?

- **SQLite**: Zero-configuration, single-file database perfect for persistent storage
- **all-MiniLM-L6-v2**: Fast (10ms/encoding), small (90MB), good quality embeddings
- **FastAPI**: Automatic OpenAPI docs, async support, type safety with Pydantic
- **Native Vector Search**: No external dependencies, pure Python cosine similarity

## Performance

- **Save memory**: ~18ms average (including embedding generation)
- **Search (semantic)**: ~15ms average for <1k memories
- **Embedding generation**: ~10ms per text (384-dimensional vector)
- **Storage efficiency**: ~1KB per memory (text + embedding + metadata)
- **Model load time**: ~6 seconds on first startup (cached afterward)
- **Memory footprint**: ~500MB RAM (model + application)

### Benchmarks

Tested on standard development machine (Intel i5, 16GB RAM):

| Operation | Memories | Time |
|-----------|----------|------|
| Save | 1 | 18ms |
| Search | 100 | 12ms |
| Search | 1,000 | 15ms |
| Search | 10,000 | 45ms |
| List | 100 | 5ms |
| Export JSON | 1,000 | 120ms |

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **Documentation**: [README](https://github.com/0xReLogic/Cognio/blob/main/README.md) | [QUICKSTART](https://github.com/0xReLogic/Cognio/blob/main/QUICKSTART.md)
- **Issues**: [GitHub Issues](https://github.com/0xReLogic/Cognio/issues)
- **Discussions**: [GitHub Discussions](https://github.com/0xReLogic/Cognio/discussions)
- **Release Notes**: [Releases](https://github.com/0xReLogic/Cognio/releases)

### FAQ

**Q: How is this different from vector databases like Pinecone or Weaviate?**  
A: Cognio is optimized for personal use and AI assistant memory, not production-scale vector search. It's lightweight, self-hosted, and zero-configuration.

**Q: Can I use this with Claude/ChatGPT/local LLMs?**  
A: Yes! Cognio implements the MCP protocol, which is supported by Claude Desktop and other MCP-compatible clients. You can also use the REST API directly.

**Q: Does it support multiple users?**  
A: v0.1.0 is single-user. Multi-user support with namespaces is planned for v2.0.0.

**Q: How do I backup my memories?**  
A: Simply copy the `data/memory.db` file, or use the `/memory/export` endpoint to export to JSON/Markdown.

**Q: Can I run this in production?**  
A: Yes, but consider adding authentication, HTTPS, rate limiting, and monitoring for production deployments.

## Roadmap

- [x] **v0.1.0**: 
  - [x] Basic CRUD operations
  - [x] Semantic search with embeddings
  - [x] Project and tag organization
  - [x] Date range filtering
  - [x] Relevance sorting
  - [x] API key authentication
  - [x] CORS support
  - [x] Docker deployment
  - [x] Comprehensive test coverage
  - [x] CI/CD with GitHub Actions
  - [x] Database migration system

- [ ] **v0.2.0**: 
  - [ ] Web UI for search and browsing
  - [ ] Auto-tagging with LLM
  - [ ] Memory summarization for long texts
  - [ ] Related memories (clustering)
  - [ ] Backup and restore tools
  - [ ] Bulk import from text files

- [ ] **v1.0.0**: 
  - [ ] Performance optimizations (vector indexing)
  - [ ] Full-text search (hybrid with semantic)
  - [ ] Memory compression
  - [ ] Advanced analytics dashboard
  - [ ] Plugin system
  - [ ] MCP 2.0 compliance

- [ ] **v1.1.0**: 
  - [ ] Obsidian sync
  - [ ] Notion integration
  - [ ] VSCode extension
  - [ ] CLI tool
  - [ ] Slack/Discord bots

- [ ] **v2.0.0**: 
  - [ ] Multi-user support with namespaces
  - [ ] Graph relationships (knowledge graph)
  - [ ] Time-based relevance decay
  - [ ] Distributed deployment
  - [ ] PostgreSQL backend option

---

Made with care for better AI conversations
