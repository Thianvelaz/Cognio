"""Basic usage examples for Cognio."""

import requests

BASE_URL = "http://localhost:8080"


def save_memory_example():
    """Example: Save a memory."""
    print("1. Saving a memory...")

    response = requests.post(
        f"{BASE_URL}/memory/save",
        json={
            "text": "FastAPI is a modern web framework for Python with automatic API documentation",
            "project": "LEARNING",
            "tags": ["python", "fastapi", "web"],
        },
    )

    data = response.json()
    print(f"   Saved: {data['id']}")
    print(f"   Duplicate: {data['duplicate']}\n")
    return data["id"]


def search_memory_example():
    """Example: Search memories."""
    print("2. Searching memories...")

    response = requests.get(
        f"{BASE_URL}/memory/search",
        params={"q": "Python web framework", "limit": 3},
    )

    data = response.json()
    print(f"   Found {data['total']} results:")
    for result in data["results"]:
        print(f"   - Score: {result['score']:.2f} | {result['text'][:60]}...")
    print()


def list_memories_example():
    """Example: List all memories."""
    print("3. Listing memories...")

    response = requests.get(f"{BASE_URL}/memory/list", params={"page": 1, "limit": 5})

    data = response.json()
    print(f"   Total: {data['total_items']} memories")
    print(f"   Showing page {data['page']} of {data['total_pages']}")
    for memory in data["memories"]:
        print(f"   - {memory['project'] or 'No project'}: {memory['text'][:50]}...")
    print()


def get_stats_example():
    """Example: Get statistics."""
    print("4. Getting statistics...")

    response = requests.get(f"{BASE_URL}/memory/stats")

    data = response.json()
    print(f"   Total memories: {data['total_memories']}")
    print(f"   Total projects: {data['total_projects']}")
    print(f"   Storage: {data['storage_mb']} MB")
    print(f"   Projects: {data['by_project']}")
    print(f"   Top tags: {data['top_tags'][:5]}")
    print()


def delete_memory_example(memory_id):
    """Example: Delete a memory."""
    print("5. Deleting a memory...")

    response = requests.delete(f"{BASE_URL}/memory/{memory_id}")

    if response.status_code == 200:
        print(f"   Deleted: {memory_id}\n")
    else:
        print(f"   Error: {response.status_code}\n")


def main():
    """Run all examples."""
    print("=== Cognio Basic Usage Examples ===\n")

    # Save a memory
    memory_id = save_memory_example()

    # Search memories
    search_memory_example()

    # List memories
    list_memories_example()

    # Get stats
    get_stats_example()

    # Delete memory (optional)
    # delete_memory_example(memory_id)


if __name__ == "__main__":
    main()
