"""Unit tests for embedding service."""

import pytest

from src.embeddings import EmbeddingService


@pytest.fixture
def embedding_service() -> EmbeddingService:
    """Create embedding service instance."""
    return EmbeddingService()


def test_encode_single_text(embedding_service: EmbeddingService) -> None:
    """Test encoding a single text."""
    text = "This is a test sentence for embedding"
    embedding = embedding_service.encode(text)

    assert isinstance(embedding, list)
    assert len(embedding) == 384  # Default for all-MiniLM-L6-v2
    assert all(isinstance(x, float) for x in embedding)


def test_encode_batch(embedding_service: EmbeddingService) -> None:
    """Test encoding multiple texts."""
    texts = ["First text", "Second text", "Third text"]
    embeddings = embedding_service.encode_batch(texts)

    assert len(embeddings) == 3
    assert all(len(emb) == 384 for emb in embeddings)


def test_cosine_similarity(embedding_service: EmbeddingService) -> None:
    """Test cosine similarity calculation."""
    text1 = "The cat sat on the mat"
    text2 = "A cat was sitting on a mat"
    text3 = "Python programming language"

    emb1 = embedding_service.encode(text1)
    emb2 = embedding_service.encode(text2)
    emb3 = embedding_service.encode(text3)

    # Similar sentences should have high similarity
    sim_similar = embedding_service.cosine_similarity(emb1, emb2)
    assert sim_similar > 0.7

    # Dissimilar sentences should have lower similarity
    sim_different = embedding_service.cosine_similarity(emb1, emb3)
    assert sim_different < 0.5

    # Same sentence should have similarity close to 1.0
    sim_identical = embedding_service.cosine_similarity(emb1, emb1)
    assert sim_identical > 0.99
