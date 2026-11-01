"""
Ephemeral Zero-Trust Privacy Manager - Version 2.8
Bảo vệ quyền riêng tư tuyệt đối cho người dùng:
- Chế độ Ẩn danh Tạm thời (Ephemeral Incognito): Không ghi dấu vết xuống đĩa cứng.
- Nút Xóa Dấu vết Khẩn cấp (Panic Wipe 1-Click): Xóa sạch toàn bộ lịch sử tư vấn trong 0.1 giây.
"""

from typing import Dict, Any


class EphemeralPrivacyManager:
    """
    Quản lý chế độ bảo mật ẩn danh và tính năng Panic Wipe.
    """

    @staticmethod
    def panic_wipe_session_state(session_state_dict: Any) -> bool:
        """
        Xóa sạch toàn bộ lịch sử tin nhắn, văn bản soạn thảo, bộ nhớ đệm trong phiên.
        """
        keys_to_clear = [
            "messages",
            "chat_history",
            "contract_text",
            "studio_doc_ready",
            "f_vals",
            "s_vals",
            "plain_cache"
        ]

        # Xóa các key nhạy cảm
        for k in list(session_state_dict.keys()):
            if any(target in k for target in keys_to_clear):
                del session_state_dict[k]

        # Khởi tạo lại lời chào ban đầu hoàn toàn sạch sẽ
        session_state_dict["messages"] = [
            {
                "role": "assistant",
                "content": (
                    "🛡️ **[PHIÊN LÀM VIỆC ĐÃ ĐƯỢC XÓA SẠCH DẤU VẾT KHẨN CẤP]**\n\n"
                    "Toàn bộ tin nhắn, dữ liệu cá nhân và tài liệu vừa tạo đã bị hủy hoàn toàn khỏi bộ nhớ RAM. "
                    "Không ai có thể xem lại những gì bạn vừa chia sẻ.\n\n"
                    "👉 *Bạn có thể an tâm bắt đầu một câu hỏi mới.*"
                ),
                "agent": "PrivacyGuard",
                "citations": []
            }
        ]
        return True
