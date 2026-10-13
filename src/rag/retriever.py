"""
Retriever Module
Trích xuất tài liệu phù hợp và định dạng trích dẫn pháp lý rõ ràng (Citation).
"""

from typing import List, Dict, Any, Tuple
from .vector_store import LegalVectorStore
from .ingestion import LegalDocumentIngestor


class LegalRetriever:
    """
    RAG Retriever chuyên trách văn bản pháp lý Việt Nam.
    """

    def __init__(self, vector_store: LegalVectorStore = None):
        self.vector_store = vector_store or LegalVectorStore()
        # Tự động nạp tài liệu nếu index đang rỗng
        if not self.vector_store.documents:
            ingestor = LegalDocumentIngestor()
            chunks = ingestor.load_all_documents()
            if chunks:
                self.vector_store.add_documents(chunks)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Lấy danh sách các đoạn trích dẫn pháp lý liên quan nhất."""
        return self.vector_store.similarity_search(query, k=top_k)

    def format_context_with_citations(self, query: str, top_k: int = 3) -> Tuple[str, List[str]]:
        """
        Định dạng ngữ cảnh kèm nguồn trích dẫn pháp luật chuẩn xác để đưa vào System Prompt.
        Returns:
            Tuple[context_text, list_of_citations]
        """
        results = self.retrieve(query, top_k=top_k)
        if not results:
            return "Không tìm thấy căn cứ pháp lý liên quan trong cơ sở dữ liệu.", []

        context_parts = []
        citations = []

        for i, item in enumerate(results, 1):
            meta = item["metadata"]
            law_title = meta.get("law_title", "Văn bản quy phạm pháp luật")
            article = meta.get("article", "Điều khoản")
            header = meta.get("article_header", article)

            citation_str = f"[{law_title} - {article}]"
            citations.append(citation_str)

            context_parts.append(
                f"--- CĂN CỨ {i}: {citation_str} ---\n"
                f"{item['text']}\n"
            )

        full_context = "\n".join(context_parts)
        return full_context, list(set(citations))
