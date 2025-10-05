#!/bin/bash
# Example curl commands for testing Cognio API

BASE_URL="http://localhost:8080"

echo "=== Cognio API Examples ==="
echo ""

# 1. Health check
echo "1. Health Check"
curl -s "$BASE_URL/health" | jq .
echo ""

# 2. Save a memory
echo "2. Save Memory"
MEMORY_ID=$(curl -s -X POST "$BASE_URL/memory/save" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "PostgreSQL is a powerful open-source relational database",
    "project": "DATABASE_LEARNING",
    "tags": ["postgresql", "database", "sql"]
  }' | jq -r '.id')
echo "Saved memory: $MEMORY_ID"
echo ""

# 3. Search memories
echo "3. Search Memories"
curl -s "$BASE_URL/memory/search?q=database&limit=3" | jq .
echo ""

# 4. List memories
echo "4. List Memories"
curl -s "$BASE_URL/memory/list?page=1&limit=5" | jq .
echo ""

# 5. Get statistics
echo "5. Get Statistics"
curl -s "$BASE_URL/memory/stats" | jq .
echo ""

# 6. Export to JSON
echo "6. Export to JSON"
curl -s "$BASE_URL/memory/export?format=json" | jq '.memories | length'
echo ""

# 7. Delete memory (optional - uncomment to use)
# echo "7. Delete Memory"
# curl -s -X DELETE "$BASE_URL/memory/$MEMORY_ID" | jq .
# echo ""

echo "=== Done ==="
