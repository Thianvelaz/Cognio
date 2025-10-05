# Quick Start Guide

Get Cognio up and running in 5 minutes.

## Prerequisites

- Python 3.11 or higher
- Docker (optional, for container deployment)
- 500MB free disk space (for embedding model)

## Option 1: Docker (Recommended)

The fastest way to get started:

```bash
# Clone the repository
git clone https://github.com/0xReLogic/Cognio.git
cd Cognio

# Start with docker-compose
docker-compose up -d

# Verify it's running
curl http://localhost:8080/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

## Option 2: Manual Installation

### 1. Install Dependencies

```bash
# Clone the repository
git clone https://github.com/0xReLogic/Cognio.git
cd Cognio

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Run the Server

```bash
# Start the server
python src/main.py
```

On first run, the server will download the embedding model (~90MB). This takes about 30 seconds.

### 3. Verify Installation

```bash
# In another terminal
curl http://localhost:8080/health
```

## Your First Memory

### Save a Memory

```bash
curl -X POST http://localhost:8080/memory/save \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is a modern Python web framework for building APIs",
    "project": "LEARNING",
    "tags": ["python", "fastapi", "web"]
  }'
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "saved": true,
  "reason": "created",
  "duplicate": false
}
```

### Search for It

```bash
curl "http://localhost:8080/memory/search?q=Python%20web%20framework&limit=3"
```

Response:
```json
{
  "query": "Python web framework",
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "text": "FastAPI is a modern Python web framework for building APIs",
      "score": 0.89,
      "project": "LEARNING",
      "tags": ["python", "fastapi", "web"],
      "created_at": "2025-01-05T10:30:00Z"
    }
  ],
  "total": 1
}
```

Notice how it found the memory even though you searched for "web framework" and the memory says "web framework"!

## Interactive API Documentation

Open your browser and go to:

**http://localhost:8080/docs**

You'll see the Swagger UI where you can:
- Browse all API endpoints
- Try out requests interactively
- See request/response schemas
- Download the OpenAPI spec

## Configuration

Create a `.env` file to customize settings:

```bash
# Copy the example
cp .env.example .env

# Edit with your preferred settings
nano .env
```

Key settings:
```bash
# Database location
DB_PATH=./data/memory.db

# Server port
API_PORT=8080

# Search defaults
DEFAULT_SEARCH_LIMIT=5
SIMILARITY_THRESHOLD=0.7

# Optional API key for authentication
API_KEY=your-secret-key-here
```

## Next Steps

### More Examples

Check out the `examples/` directory:
- `examples/basic_usage.py` - Python SDK examples
- `examples/curl_examples.sh` - Command-line examples
- `examples/mcp_config.json` - MCP client configuration

### Full Documentation

- [API Documentation](api.md) - Complete API reference
- [Examples](examples.md) - More use cases and patterns
- [README](../README.md) - Full project documentation

### MCP Integration

To use Cognio with Claude Desktop or other MCP clients:

1. Copy `examples/mcp_config.json` to your MCP client config location
2. Update the URL if needed (default: http://localhost:8080)
3. Restart your MCP client

### Troubleshooting

**Server won't start?**
- Check if port 8080 is already in use: `lsof -i :8080`
- Try a different port: `API_PORT=8081 python src/main.py`

**Can't find saved memories?**
- Check the database exists: `ls -lh data/memory.db`
- Verify with stats endpoint: `curl http://localhost:8080/memory/stats`

**Slow searches?**
- Lower the similarity threshold: `?threshold=0.5`
- Use project filters: `?project=YOUR_PROJECT`

**Need help?**
- [GitHub Issues](https://github.com/0xReLogic/Cognio/issues)
- [GitHub Discussions](https://github.com/0xReLogic/Cognio/discussions)

## What's Next?

Now that you have Cognio running:

1. **Save your first real memories** - Notes, code snippets, learnings
2. **Organize with projects** - Group related memories together
3. **Tag effectively** - Use consistent tags for better filtering
4. **Explore search** - Try semantic queries to find memories by meaning
5. **Export your data** - Backup to JSON or Markdown anytime

Happy remembering! 🧠
