"""Unit tests for memory service."""

import pytest
from datetime import datetime, timedelta
from typing import Generator
from src.memory import memory_service
from src.database import db
from src.models import SaveMemoryRequest


@pytest.fixture(autouse=True)
def setup_test_db() -> Generator[None, None, None]:
    """Setup test database before each test."""
    db.db_path = ":memory:"
    db.connect()
    yield
    db.close()


def test_save_memory() -> None:
    """Test saving a memory."""
    request = SaveMemoryRequest(
        text="Python is a programming language", project="TEST", tags=["python", "test"]
    )

    memory_id, is_duplicate, reason = memory_service.save_memory(request)

    assert memory_id is not None
    assert is_duplicate is False
    assert reason == "created"


def test_save_duplicate_memory() -> None:
    """Test duplicate detection."""
    request = SaveMemoryRequest(text="Duplicate text", project="TEST", tags=["test"])

    # Save first time
    id1, dup1, _ = memory_service.save_memory(request)
    assert dup1 is False

    # Save again (should be duplicate)
    id2, dup2, reason2 = memory_service.save_memory(request)
    assert dup2 is True
    assert reason2 == "duplicate"
    assert id1 == id2


def test_search_memory() -> None:
    """Test semantic search."""
    # Save some memories
    memory_service.save_memory(
        SaveMemoryRequest(text="Python is great for AI", project="AI", tags=["python"])
    )
    memory_service.save_memory(
        SaveMemoryRequest(text="JavaScript for web development", project="WEB", tags=["js"])
    )
    memory_service.save_memory(
        SaveMemoryRequest(
            text="Machine learning with Python", project="AI", tags=["python", "ml"]
        )
    )

    # Search for Python-related
    results = memory_service.search_memory(query="Python programming", limit=5, threshold=0.3)

    assert len(results) > 0
    # Should find Python-related memories
    assert any("Python" in r.text for r in results)


def test_search_with_project_filter() -> None:
    """Test search with project filtering."""
    memory_service.save_memory(
        SaveMemoryRequest(text="AI project memory", project="AI", tags=["ai"])
    )
    memory_service.save_memory(
        SaveMemoryRequest(text="Web project memory", project="WEB", tags=["web"])
    )

    results = memory_service.search_memory(
        query="project memory", project="AI", limit=5, threshold=0.3
    )

    assert len(results) > 0
    assert all(r.project == "AI" for r in results)


def test_search_with_date_range() -> None:
    """Test search with date filtering."""
    # Save a memory
    memory_service.save_memory(
        SaveMemoryRequest(text="Recent memory", project="TEST", tags=["test"])
    )

    # Search with date range
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).isoformat()
    tomorrow = (now + timedelta(days=1)).isoformat()

    results = memory_service.search_memory(
        query="memory", after_date=yesterday, before_date=tomorrow, threshold=0.1
    )

    assert len(results) > 0


def test_list_memories() -> None:
    """Test listing memories."""
    # Save multiple memories
    for i in range(5):
        memory_service.save_memory(
            SaveMemoryRequest(text=f"Memory {i}", project="TEST", tags=[f"tag{i}"])
        )

    memories, total = memory_service.list_memories(page=1, limit=10)

    assert total == 5
    assert len(memories) == 5


def test_list_with_project_filter() -> None:
    """Test listing with project filter."""
    memory_service.save_memory(
        SaveMemoryRequest(text="AI memory", project="AI", tags=["ai"])
    )
    memory_service.save_memory(
        SaveMemoryRequest(text="WEB memory", project="WEB", tags=["web"])
    )

    memories, total = memory_service.list_memories(project="AI", page=1, limit=10)

    assert total == 1
    assert memories[0].project == "AI"


def test_list_with_relevance_sort() -> None:
    """Test listing with relevance sorting."""
    memory_service.save_memory(
        SaveMemoryRequest(
            text="Python programming language", project="CODE", tags=["python"]
        )
    )
    memory_service.save_memory(
        SaveMemoryRequest(text="JavaScript is cool", project="CODE", tags=["js"])
    )

    memories, total = memory_service.list_memories(
        page=1, limit=10, sort="relevance", search_query="Python"
    )

    assert len(memories) > 0
    # First result should be most relevant
    if len(memories) > 0:
        assert memories[0].score is not None


def test_delete_memory() -> None:
    """Test deleting a memory."""
    request = SaveMemoryRequest(text="Memory to delete", project="TEST", tags=["test"])
    memory_id, _, _ = memory_service.save_memory(request)

    # Delete it
    deleted = memory_service.delete_memory(memory_id)
    assert deleted is True

    # Try to delete again (should fail)
    deleted_again = memory_service.delete_memory(memory_id)
    assert deleted_again is False


def test_bulk_delete() -> None:
    """Test bulk deletion."""
    # Save memories in different projects
    memory_service.save_memory(
        SaveMemoryRequest(text="Memory 1", project="PROJECT_A", tags=["test"])
    )
    memory_service.save_memory(
        SaveMemoryRequest(text="Memory 2", project="PROJECT_A", tags=["test"])
    )
    memory_service.save_memory(
        SaveMemoryRequest(text="Memory 3", project="PROJECT_B", tags=["test"])
    )

    # Bulk delete PROJECT_A
    count = memory_service.bulk_delete(project="PROJECT_A")
    assert count == 2

    # Check remaining
    memories, total = memory_service.list_memories(page=1, limit=10)
    assert total == 1
    assert memories[0].project == "PROJECT_B"


def test_get_stats() -> None:
    """Test statistics retrieval."""
    # Save some test data
    memory_service.save_memory(
        SaveMemoryRequest(text="Memory 1", project="PROJECT_A", tags=["tag1", "tag2"])
    )
    memory_service.save_memory(
        SaveMemoryRequest(text="Memory 2", project="PROJECT_B", tags=["tag1"])
    )

    stats = memory_service.get_stats()

    assert stats["total_memories"] == 2
    assert stats["total_projects"] == 2
    assert "PROJECT_A" in stats["by_project"]
    assert "PROJECT_B" in stats["by_project"]
    assert "tag1" in stats["top_tags"]


def test_export_json() -> None:
    """Test JSON export."""
    memory_service.save_memory(
        SaveMemoryRequest(text="Export test", project="TEST", tags=["export"])
    )

    data = memory_service.export_memories(format="json")

    assert isinstance(data, dict)
    assert "memories" in data
    assert len(data["memories"]) > 0


def test_export_markdown() -> None:
    """Test Markdown export."""
    memory_service.save_memory(
        SaveMemoryRequest(text="Export test", project="TEST", tags=["export"])
    )

    data = memory_service.export_memories(format="markdown")

    assert isinstance(data, str)
    assert "Export test" in data
    assert "TEST" in data
