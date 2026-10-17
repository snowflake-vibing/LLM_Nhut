"""
Retriever Module
Trích xuất tài liệu phù hợp và định dạng trích dẫn pháp lý rõ ràng (Citation)
kèm đường link kiểm chứng chính thức (Verify URL) và đoạn trích nguyên văn.
Hỗ trợ lọc theo Lĩnh vực pháp lý (Legal Domain Filtering - Hierarchical RAG).
"""

from typing import List, Dict, Any, Tuple, Optional
from .vector_store import LegalVectorStore
from .ingestion import LegalDocumentIngestor


class LegalRetriever:
    """
    RAG Retriever chuyên trách văn bản pháp lý Việt Nam đa lĩnh vực
    (Doanh nghiệp, Dân sự, Lao động, Thương mại).
    """

    def __init__(self, vector_store: LegalVectorStore = None):
        self.vector_store = vector_store or LegalVectorStore()
        
        # Kiểm tra nạp lại nếu index chưa có đầy đủ các bộ luật mới của Version 2.0
        existing_sources = {doc.get("metadata", {}).get("source", "") for doc in self.vector_store.documents}
        required_sources = {
            "Luat_Doanh_Nghiep_2020.txt",
            "Bo_Luat_Dan_Su_2015.txt",
            "Bo_Luat_Lao_Dong_2019.txt",
            "Luat_Thuong_Mai_2005.txt"
        }
        needs_reload = not required_sources.issubset(existing_sources)

        if needs_reload:
            ingestor = LegalDocumentIngestor()
            chunks = ingestor.load_all_documents()
            if chunks:
                self.vector_store.documents = []  # Làm mới lại index với đầy đủ các bộ luật
                self.vector_store.add_documents(chunks)

    def retrieve(
        self, query: str, top_k: int = 3, domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Lấy danh sách các đoạn trích dẫn pháp lý liên quan nhất.
        Hỗ trợ domain: 'corporate', 'civil', 'labor', 'commercial'.
        """
        raw_results = self.vector_store.similarity_search(query, k=top_k * 2 if domain else top_k)
        if not domain:
            return raw_results[:top_k]

        filtered = [
            r for r in raw_results
            if r.get("metadata", {}).get("domain") == domain
        ]
        # Nếu lọc theo domain có kết quả thì dùng, nếu không thì fallback về kết quả chung
        return filtered[:top_k] if filtered else raw_results[:top_k]

    def format_context_with_citations(
        self, query: str, top_k: int = 3, domain: Optional[str] = None
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Định dạng ngữ cảnh kèm danh sách trích dẫn có cấu trúc (Structured Citations)
        gồm tên Luật, số Điều, Tiêu đề, Link kiểm chứng và nội dung tóm lược.
        Returns:
            Tuple[context_text, list_of_structured_citations]
        """
        results = self.retrieve(query, top_k=top_k, domain=domain)
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
