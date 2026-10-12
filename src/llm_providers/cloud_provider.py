"""
Cloud LLM Provider
Tích hợp Google Gemini API (và mở rộng OpenAI API) phục vụ các tác vụ
suy luận nâng cao, phân tích văn bản pháp luật phức tạp.
"""

import os
from typing import Generator, Optional, Any, Dict
import requests
from dotenv import load_dotenv

load_dotenv()


class CloudLLMProvider:
    """
    Provider quản lý kết nối và gọi mô hình Cloud (Mặc định: Google Gemini).
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.2,
        max_output_tokens: int = 2048,
    ):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        self.model_name = model_name or os.getenv("CLOUD_MODEL_NAME", "gemini-1.5-flash")
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self._llm_instance = None

    def is_available(self) -> bool:
        """Kiểm tra xem API Key đã được cấu hình hay chưa."""
        return bool(self.api_key and self.api_key.strip())

    def get_llm(self) -> Any:
        """
        Trả về LangChain BaseChatModel nếu đã cài đặt thư viện langchain_google_genai.
        Nếu chưa cài đặt, trả về chính provider wrapper này.
        """
        if self._llm_instance is not None:
            return self._llm_instance

        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            self._llm_instance = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.api_key,
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
            )
            return self._llm_instance
        except ImportError:
            # Fallback nếu môi trường chưa cài đặt langchain-google-genai
            return self

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Sinh câu trả lời từ Cloud LLM qua Gemini REST API.
        """
        if not self.is_available():
            raise ValueError(
                "Chưa cấu hình GOOGLE_API_KEY! Vui lòng cấu hình biến môi trường hoặc truyền api_key."
            )

        endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model_name}:generateContent?key={self.api_key}"
        )

        contents = []
        if system_prompt:
            contents.append({
                "role": "user",
                "parts": [{"text": f"System Instructions:\n{system_prompt}"}]
            })
            contents.append({
                "role": "model",
                "parts": [{"text": "Đã hiểu và sẵn sàng tuân thủ hướng dẫn trên."}]
            })

        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_output_tokens,
            }
        }

        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Lỗi gọi Gemini API (Status {response.status_code}): {response.text}"
            )

        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as err:
            raise RuntimeError(f"Cấu trúc phản hồi từ Gemini API không hợp lệ: {data}") from err

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """
        Stream câu trả lời từng token để hiển thị mượt mà trên giao diện người dùng.
        """
        # Hỗ trợ stream qua REST API SSE
        if not self.is_available():
            raise ValueError("Chưa cấu hình GOOGLE_API_KEY!")

        endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model_name}:streamGenerateContent?alt=sse&key={self.api_key}"
        )

        contents = []
        if system_prompt:
            contents.append({
                "role": "user",
                "parts": [{"text": f"System Instructions:\n{system_prompt}"}]
            })
            contents.append({
                "role": "model",
                "parts": [{"text": "Đã hiểu và tuân thủ."}]
            })

        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_output_tokens,
            }
        }

        with requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            stream=True,
            timeout=60,
        ) as response:
            if response.status_code != 200:
                raise RuntimeError(f"Lỗi Stream Gemini API ({response.status_code}): {response.text}")

            import json
            for line in response.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    if decoded.startswith("data: "):
                        try:
                            chunk = json.loads(decoded[6:])
                            text = chunk["candidates"][0]["content"]["parts"][0]["text"]
                            yield text
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue
