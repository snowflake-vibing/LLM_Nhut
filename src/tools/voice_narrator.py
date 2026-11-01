# -*- coding: utf-8 -*-
"""
Module Trợ Lý Phát Thanh Âm Thanh Dân Sinh (Voice Narrator)
Phiên bản 5.1 - Hỗ trợ người cao tuổi, người khiếm thị và người dân không quen đọc chữ.
Chuyển hóa văn bản pháp lý thành giọng đọc tiếng Việt truyền cảm, ấm áp.
"""

import io
import re
from typing import Optional

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False


class VoiceNarrator:
    """Trợ lý giọng nói tiếng Việt cho người cao tuổi và bà con dân sinh."""

    @staticmethod
    def clean_text_for_speech(text: str) -> str:
        """Làm sạch các ký tự đặc biệt, định dạng markdown để giọng đọc tự nhiên, êm tai."""
        if not text:
            return ""

        # Xóa các khối code markdown
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        # Xóa các link markdown [text](url) -> giữ lại text
        text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
        # Xóa các ký tự markdown thông dụng
        text = re.sub(r"[#*_`~>-]", " ", text)
        # Chuẩn hóa khoảng trắng
        text = re.sub(r"\s+", " ", text).strip()
        # Giới hạn độ dài câu đọc tóm tắt nếu văn bản quá dài (đọc tối đa ~500 từ cốt lõi)
        words = text.split()
        if len(words) > 400:
            text = " ".join(words[:400]) + "... Bà con có thể xem thêm chi tiết được ghi rõ trên màn hình."

        return text

    @staticmethod
    def generate_speech(text: str, lang: str = "vi", slow: bool = False) -> Optional[io.BytesIO]:
        """
        Tạo luồng dữ liệu nhị phân MP3 từ văn bản.
        Trả về BytesIO nếu thành công, None nếu có lỗi.
        """
        if not HAS_GTTS:
            return None

        clean_content = VoiceNarrator.clean_text_for_speech(text)
        if not clean_content:
            clean_content = "Không có nội dung để phát âm thanh."

        try:
            tts = gTTS(text=clean_content, lang=lang, slow=slow)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp
        except Exception as e:
            print(f"[VoiceNarrator Error]: {e}")
            return None
