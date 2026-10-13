"""
Local LLM Provider
Kết nối Ollama cục bộ (mặc định: http://localhost:11434) chạy các mô hình
mã nguồn mở như Qwen 2.5, Llama 3.1 phục vụ dữ liệu nhạy cảm / nội bộ.
"""

import os
from typing import Generator, List, Optional, Any, Dict
import requests
from dotenv import load_dotenv

load_dotenv()


class LocalLLMProvider:
    """
    Provider quản lý kết nối và gọi mô hình chạy nội bộ qua Ollama.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.2,
    ):
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        self.model_name = model_name or os.getenv("LOCAL_MODEL_NAME", "qwen2.5:latest")
        self.temperature = temperature
        self._llm_instance = None

    def is_available(self) -> bool:
        """
        Kiểm tra xem dịch vụ Ollama local có đang chạy và phản hồi hay không.
        """
        try:
            res = requests.get(f"{self.base_url}/api/tags", timeout=3)
            return res.status_code == 200
        except requests.RequestException:
            return False

    def list_models(self) -> List[str]:
        """
        Lấy danh sách các mô hình đã tải về trên máy local.
        """
        try:
            res = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if res.status_code == 200:
                data = res.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except requests.RequestException:
            return []

    def get_llm(self) -> Any:
        """
        Trả về đối tượng ChatOllama của LangChain nếu có sẵn thư viện.
        Nếu chưa có, trả về chính provider instance này.
        """
        if self._llm_instance is not None:
            return self._llm_instance

        try:
            # Thử import từ thư viện mới langchain_ollama hoặc langchain_community
            try:
                from langchain_ollama import ChatOllama
            except ImportError:
                from langchain_community.chat_models import ChatOllama

            self._llm_instance = ChatOllama(
                model=self.model_name,
                base_url=self.base_url,
                temperature=self.temperature,
            )
            return self._llm_instance
        except ImportError:
            return self

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Gửi yêu cầu sinh văn bản đến Ollama HTTP API (/api/generate).
        """
        if not self.is_available():
            raise ConnectionError(
                f"Không thể kết nối đến Ollama tại {self.base_url}. "
                f"Vui lòng đảm bảo ứng dụng Ollama đã được khởi chạy!"
            )

        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
            }
        }
        if system_prompt:
            payload["system"] = system_prompt

        response = requests.post(endpoint, json=payload, timeout=120)
        if response.status_code != 200:
            raise RuntimeError(
                f"Lỗi gọi Ollama (Status {response.status_code}): {response.text}"
            )

        data = response.json()
        return data.get("response", "")

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """
        Stream kết quả từng token từ Ollama về giao diện người dùng.
        """
        if not self.is_available():
            raise ConnectionError(f"Không thể kết nối đến Ollama tại {self.base_url}.")

        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": self.temperature,
            }
        }
        if system_prompt:
            payload["system"] = system_prompt

        with requests.post(endpoint, json=payload, stream=True, timeout=120) as response:
            if response.status_code != 200:
                raise RuntimeError(f"Lỗi stream Ollama: {response.text}")

            import json
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    text = chunk.get("response", "")
                    if text:
                        yield text
                    if chunk.get("done", False):
                        break
