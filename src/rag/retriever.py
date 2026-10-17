"""
Retriever Module
Trích xuất tài liệu phù hợp và định dạng trích dẫn pháp lý rõ ràng (Citation)
kèm đường link kiểm chứng chính thức (Verify URL) và đoạn trích nguyên văn.
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
        # Nạp lại hoặc cập nhật tài liệu nếu index chưa có verify_url
        needs_reload = False
        if not self.vector_store.documents:
            needs_reload = True
        else:
            first_doc_meta = self.vector_store.documents[0].get("metadata", {})
            if "verify_url" not in first_doc_meta:
                needs_reload = True

        if needs_reload:
            ingestor = LegalDocumentIngestor()
            chunks = ingestor.load_all_documents()
            if chunks:
                self.vector_store.documents = []  # Làm mới lại index với metadata mới
                self.vector_store.add_documents(chunks)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Lấy danh sách các đoạn trích dẫn pháp lý liên quan nhất."""
        return self.vector_store.similarity_search(query, k=top_k)

    def format_context_with_citations(
        self, query: str, top_k: int = 3
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Định dạng ngữ cảnh kèm danh sách trích dẫn có cấu trúc (Structured Citations)
        gồm tên Luật, số Điều, Tiêu đề, Link kiểm chứng và nội dung tóm lược.
        Returns:
            Tuple[context_text, list_of_structured_citations]
        """
        results = self.retrieve(query, top_k=top_k)
        if not results:
            return "Không tìm thấy căn cứ pháp lý liên quan trong cơ sở dữ liệu.", []

        context_parts = []
        structured_citations = []
        seen_articles = set()

        for i, item in enumerate(results, 1):
            meta = item.get("metadata", {})
            law_title = meta.get("law_title", "Văn bản quy phạm pháp luật")
            article = meta.get("article", "Điều khoản")
            header = meta.get("article_header", article)
            verify_url = meta.get("verify_url", "https://vanban.chinhphu.vn/")
            text = item.get("text", "")

            citation_key = f"{law_title}_{article}"
            if citation_key not in seen_articles:
                seen_articles.add(citation_key)
                structured_citations.append({
                    "law_title": law_title,
                    "article": article,
                    "header": header,
                    "verify_url": verify_url,
                    "text_snippet": text[:200] + "..." if len(text) > 200 else text,
                    "full_text": text,
                })

            context_parts.append(
                f"--- CĂN CỨ {i}: [{law_title} - {article}] ---\n"
                f"{text}\n"
            )

        full_context = "\n".join(context_parts)
        return full_context, structured_citations
