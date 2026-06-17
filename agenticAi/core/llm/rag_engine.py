from __future__ import annotations

import os
import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

from agenticAi.core.llm.ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class Document:
    """Lightweight representation of a RAG document chunk."""

    def __init__(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        self.content = content
        self.metadata: Dict[str, Any] = metadata or {}

    def __repr__(self) -> str:
        preview = self.content[:80].replace("\n", " ")
        return f"Document(preview={preview!r}, metadata={self.metadata})"


class RagEngine:
    """
    Phase 2 - Agentic AI Core Library
    Simple Retrieval-Augmented Generation engine.

    Architecture (no external vector DB required for Phase 2):
      1. Load plain-text / JSON documents from a docs directory.
      2. Split them into overlapping chunks.
      3. On query, perform keyword-based retrieval (TF-IDF-style scoring).
      4. Feed top-k chunks to OllamaClient.chat() with an augmented prompt.

    Designed for the KISA security documentation corpus used by BlueAgent.
    """

    DEFAULT_CHUNK_SIZE = 512   # characters
    DEFAULT_CHUNK_OVERLAP = 64  # characters
    DEFAULT_TOP_K = 5

    def __init__(
        self,
        docs_dir: Optional[str] = None,
        ollama_client: Optional[OllamaClient] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
        top_k: int = DEFAULT_TOP_K,
    ):
        self.docs_dir = Path(docs_dir) if docs_dir else None
        self.llm = ollama_client or OllamaClient()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self._documents: List[Document] = []
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # Document loading
    # ------------------------------------------------------------------

    def load_documents(self, docs_dir: Optional[str] = None) -> int:
        """
        Load all .txt and .json files from docs_dir.
        Returns the number of chunks loaded.
        """
        target = Path(docs_dir) if docs_dir else self.docs_dir
        if target is None or not target.exists():
            self.logger.warning("[RagEngine] docs_dir not set or does not exist: %s", target)
            return 0

        raw_texts: List[tuple] = []  # (source_path, text)
        for path in target.rglob("*"):
            if path.suffix == ".txt":
                raw_texts.append((str(path), path.read_text(encoding="utf-8", errors="ignore")))
            elif path.suffix == ".json":
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    # Support both string and list/dict JSON
                    if isinstance(data, str):
                        raw_texts.append((str(path), data))
                    elif isinstance(data, list):
                        for item in data:
                            raw_texts.append((str(path), str(item)))
                    else:
                        raw_texts.append((str(path), json.dumps(data, ensure_ascii=False)))
                except Exception as exc:
                    self.logger.warning("[RagEngine] Failed to parse JSON %s: %s", path, exc)

        self._documents.clear()
        for source, text in raw_texts:
            chunks = self._split_text(text, source)
            self._documents.extend(chunks)

        self.logger.info(
            "[RagEngine] Loaded %d chunks from %d files in %s",
            len(self._documents), len(raw_texts), target,
        )
        return len(self._documents)

    def add_document(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a single document string directly (bypassing file loading)."""
        chunks = self._split_text(content, source=metadata.get("source", "manual") if metadata else "manual")
        self._documents.extend(chunks)
        self.logger.debug("[RagEngine] Added %d chunks", len(chunks))

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Document]:
        """
        Keyword-based retrieval: score each chunk by term overlap with the query.
        Returns the top_k most relevant Document chunks.
        """
        if not self._documents:
            self.logger.warning("[RagEngine] No documents loaded; returning empty context.")
            return []

        k = top_k or self.top_k
        query_terms = set(query.lower().split())

        scored: List[tuple] = []
        for doc in self._documents:
            doc_terms = set(doc.content.lower().split())
            overlap = len(query_terms & doc_terms)
            if overlap > 0:
                scored.append((overlap, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [doc for _, doc in scored[:k]]
        self.logger.debug(
            "[RagEngine] retrieve query=%r -> %d/%d chunks matched",
            query[:50], len(scored), len(self._documents),
        )
        return results

    # ------------------------------------------------------------------
    # RAG Query
    # ------------------------------------------------------------------

    def query(
        self,
        question: str,
        system_prompt: Optional[str] = None,
        top_k: Optional[int] = None,
    ) -> str:
        """
        Retrieve relevant chunks and send an augmented prompt to the LLM.
        Returns the LLM response string.
        """
        context_docs = self.retrieve(question, top_k=top_k)

        if context_docs:
            context_text = "\n\n---\n\n".join(
                f"[Source: {d.metadata.get('source', 'unknown')}]\n{d.content}"
                for d in context_docs
            )
            augmented_prompt = (
                f"Use the following context to answer the question.\n\n"
                f"Context:\n{context_text}\n\n"
                f"Question: {question}"
            )
        else:
            augmented_prompt = question

        default_system = (
            "You are a cybersecurity and trading platform expert. "
            "Answer concisely and accurately based on provided context."
        )
        return self.llm.chat(
            prompt=augmented_prompt,
            system_prompt=system_prompt or default_system,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _split_text(self, text: str, source: str) -> List[Document]:
        """Split text into overlapping chunks."""
        chunks: List[Document] = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            if chunk_text.strip():
                chunks.append(Document(
                    content=chunk_text,
                    metadata={"source": source, "start": start, "end": end},
                ))
            start += self.chunk_size - self.chunk_overlap
        return chunks

    @property
    def document_count(self) -> int:
        """Return the number of loaded document chunks."""
        return len(self._documents)
