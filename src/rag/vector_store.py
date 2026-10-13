"""
Vector Store Module
Quản lý lưu trữ và tìm kiếm vector tương đồng ngữ nghĩa.
Tương thích ChromaDB và tích hợp Persistent JSON Vector Index dự phòng.
"""

import os
import json
import math
from typing import List, Dict, Any, Optional
from .embeddings import LegalEmbeddingFunction

CHROMA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "chromadb"
)


class LegalVectorStore:
    """
    Quản lý Vector Store cho tri thức pháp lý SME.
    Tự động lưu trữ xuống đĩa và hỗ trợ tìm kiếm ngữ nghĩa theo Cosine Similarity.
    """

    def __init__(self, persist_directory: str = None):
        self.persist_directory = persist_directory or CHROMA_DIR
        os.makedirs(self.persist_directory, exist_ok=True)
        self.embedding_fn = LegalEmbeddingFunction()
        self.index_file = os.path.join(self.persist_directory, "legal_index.json")
        self.documents: List[Dict[str, Any]] = []
        self._load_local_index()

    def _load_local_index(self):
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    self.documents = json.load(f)
            except Exception:
                self.documents = []

    def _save_local_index(self):
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)

    def add_documents(self, chunks: List[Dict[str, Any]]):
        """
        Nhúng vector và thêm tài liệu vào Vector Store.
        """
        texts = [c["text"] for c in chunks]
        vectors = self.embedding_fn.embed_documents(texts)

        for chunk, vec in zip(chunks, vectors):
            self.documents.append({
                "id": chunk.get("id"),
                "text": chunk.get("text"),
                "metadata": chunk.get("metadata", {}),
                "vector": vec,
            })
        self._save_local_index()

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def similarity_search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Tìm kiếm k đoạn văn bản có độ tương đồng ngữ nghĩa cao nhất với câu hỏi.
        """
        if not self.documents:
            return []

        q_vec = self.embedding_fn.embed_query(query)
        scored = []

        # Kết hợp semantic vector + keyword boost cho từ khóa số Điều
        for doc in self.documents:
            sim = self._cosine_similarity(q_vec, doc["vector"])
            # Keyword matching bonus
            query_lower = query.lower()
            text_lower = doc["text"].lower()
            if any(term in text_lower for term in query_lower.split() if len(term) > 3):
                sim += 0.15
            scored.append((sim, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "text": item[1]["text"],
                "metadata": item[1]["metadata"],
                "score": float(item[0]),
            }
            for item in scored[:k]
        ]
