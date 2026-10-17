"""
Ingestion & Document Chunker
Bộ đọc văn bản pháp luật và cắt đoạn thông minh theo Điều / Khoản (Article-level chunking)
tích hợp đường link tra cứu chính thức tại Cổng thông tin Chính phủ (Verify URL).
"""

import os
import re
from typing import List, Dict, Any

DOCS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "raw_documents"
)

# Bảng ánh xạ link kiểm chứng văn bản quy phạm pháp luật chính thống
LEGAL_SOURCE_URLS = {
    "Luat_Doanh_Nghiep_2020": "https://vanban.chinhphu.vn/?pageid=27160&docid=200676",
    "Nghi_Dinh_01_2021_ND_CP": "https://vanban.chinhphu.vn/?pageid=27160&docid=202613",
    "Nghi_Dinh_39_2018_ND_CP": "https://vanban.chinhphu.vn/?pageid=27160&docid=193188",
    "Bo_Luat_Dan_Su_2015": "https://vanban.chinhphu.vn/?pageid=27160&docid=183188",
    "Bo_Luat_Lao_Dong_2019": "https://vanban.chinhphu.vn/?pageid=27160&docid=198540",
    "Luat_Thuong_Mai_2005": "https://vanban.chinhphu.vn/?pageid=27160&docid=21404",
}

# Ánh xạ lĩnh vực pháp lý (Legal Domain Taxonomy)
LEGAL_DOMAINS = {
    "Luat_Doanh_Nghiep_2020": "corporate",
    "Nghi_Dinh_01_2021_ND_CP": "corporate",
    "Nghi_Dinh_39_2018_ND_CP": "corporate",
    "Bo_Luat_Dan_Su_2015": "civil",
    "Bo_Luat_Lao_Dong_2019": "labor",
    "Luat_Thuong_Mai_2005": "commercial",
}


class LegalDocumentIngestor:
    """
    Trích xuất văn bản pháp lý và cắt thành các đoạn chunk có đầy đủ ngữ cảnh Điều / Khoản
    kèm đường link kiểm chứng chính thức của nhà nước.
    """

    def __init__(self, docs_dir: str = None):
        self.docs_dir = docs_dir or DOCS_DIR

    def parse_legal_text(self, filename: str, content: str) -> List[Dict[str, Any]]:
        """
        Tách văn bản luật theo từng Điều (Ví dụ: 'Điều 4.', 'Điều 23.'...).
        Gán metadata: tên văn bản, số Điều, tiêu đề Điều, và link kiểm chứng.
        """
        chunks = []
        base_name = os.path.splitext(filename)[0]
        doc_title = base_name.replace("_", " ")
        verify_url = LEGAL_SOURCE_URLS.get(base_name, "https://vanban.chinhphu.vn/")
        domain = LEGAL_DOMAINS.get(base_name, "general")

        # Regex tìm các Điều
        pattern = r"(Điều\s+\d+[\.:]\s*[^\n]+)"
        splits = re.split(pattern, content)

        if len(splits) <= 1:
            paragraphs = [p.strip() for p in content.split("\n\n") if len(p.strip()) > 40]
            for i, p in enumerate(paragraphs):
                chunks.append({
                    "id": f"{filename}_{i}",
                    "text": p,
                    "metadata": {
                        "source": filename,
                        "law_title": doc_title,
                        "article": f"Đoạn {i+1}",
                        "verify_url": verify_url,
                        "domain": domain,
                    }
                })
            return chunks

        # Ghép cặp Header Điều và Nội dung Điều
        i = 1
        while i < len(splits):
            header = splits[i].strip()
            body = splits[i + 1].strip() if i + 1 < len(splits) else ""
            full_text = f"{header}\n{body}"

            # Rút trích số Điều (ví dụ Điều 23)
            art_match = re.search(r"Điều\s+(\d+)", header)
            art_num = f"Điều {art_match.group(1)}" if art_match else header[:20]

            chunks.append({
                "id": f"{filename}_{art_num.replace(' ', '_')}",
                "text": full_text,
                "metadata": {
                    "source": filename,
                    "law_title": doc_title,
                    "article": art_num,
                    "article_header": header,
                    "verify_url": verify_url,
                    "domain": domain,
                }
            })
            i += 2

        return chunks

    def load_all_documents(self) -> List[Dict[str, Any]]:
        """Đọc toàn bộ file văn bản trong thư mục raw_documents."""
        all_chunks = []
        if not os.path.exists(self.docs_dir):
            return all_chunks

        for fname in os.listdir(self.docs_dir):
            if fname.endswith(".txt") or fname.endswith(".md"):
                fpath = os.path.join(self.docs_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                chunks = self.parse_legal_text(fname, content)
                all_chunks.extend(chunks)

        return all_chunks
