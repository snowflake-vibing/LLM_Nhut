"""
Model Factory & Switcher
Cơ chế Factory cho phép chuyển đổi tức thì giữa Cloud Model và Local Model
dựa vào biến môi trường, cấu hình hoặc nút chuyển đổi trên UI.
"""

import os
from enum import Enum
from typing import Optional, Union, Dict, Any
from dotenv import load_dotenv

from .cloud_provider import CloudLLMProvider
from .local_provider import LocalLLMProvider

load_dotenv()


class ProviderType(str, Enum):
    CLOUD = "cloud"
    LOCAL = "local"


class ModelFactory:
    """
    Factory Pattern quản lý việc khởi tạo và chuyển đổi mô hình LLM.
    """

    def __init__(self, default_provider: Optional[Union[ProviderType, str]] = None):
        env_mode = os.getenv("DEFAULT_MODE", "cloud").lower()
        self.current_provider_type = (
            ProviderType(default_provider)
            if default_provider
            else (ProviderType.LOCAL if env_mode == "local" else ProviderType.CLOUD)
        )
        self._cloud_provider: Optional[CloudLLMProvider] = None
        self._local_provider: Optional[LocalLLMProvider] = None

    def get_cloud_provider(self, **kwargs) -> CloudLLMProvider:
        """Khởi tạo hoặc trả về Cloud Provider hiện tại."""
        if self._cloud_provider is None or kwargs:
            self._cloud_provider = CloudLLMProvider(**kwargs)
        return self._cloud_provider

    def get_local_provider(self, **kwargs) -> LocalLLMProvider:
        """Khởi tạo hoặc trả về Local Provider hiện tại."""
        if self._local_provider is None or kwargs:
            self._local_provider = LocalLLMProvider(**kwargs)
        return self._local_provider

    def set_provider(self, provider_type: Union[ProviderType, str]) -> None:
        """
        Chuyển đổi provider hoạt động (dùng khi người dùng gạt nút trên UI).
        """
        if isinstance(provider_type, str):
            provider_type = ProviderType(provider_type.lower())
        self.current_provider_type = provider_type

    def get_provider(
        self,
        provider_type: Optional[Union[ProviderType, str]] = None,
        **kwargs,
    ) -> Union[CloudLLMProvider, LocalLLMProvider]:
        """
        Lấy provider theo loại chỉ định hoặc theo provider đang kích hoạt.
        """
        target = provider_type or self.current_provider_type
        if isinstance(target, str):
            target = ProviderType(target.lower())

        if target == ProviderType.LOCAL:
            return self.get_local_provider(**kwargs)
        return self.get_cloud_provider(**kwargs)

    def get_llm(
        self,
        provider_type: Optional[Union[ProviderType, str]] = None,
        **kwargs,
    ) -> Any:
        """
        Trả về LangChain BaseChatModel phù hợp để gắn vào LangGraph hoặc Chains.
        """
        provider = self.get_provider(provider_type, **kwargs)
        return provider.get_llm()

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        provider_type: Optional[Union[ProviderType, str]] = None,
        auto_fallback: bool = True,
    ) -> str:
        """
        Sinh văn bản với cơ chế tự động chuyển đổi phòng vệ (Auto-fallback):
        Nếu chế độ Local không phản hồi, tự động dùng Cloud nếu được cho phép.
        """
        target = provider_type or self.current_provider_type
        provider = self.get_provider(target)

        try:
            return provider.generate(prompt=prompt, system_prompt=system_prompt)
        except Exception as err:
            if auto_fallback and target == ProviderType.LOCAL:
                cloud = self.get_cloud_provider()
                if cloud.is_available():
                    return cloud.generate(prompt=prompt, system_prompt=system_prompt)
            raise err

    def check_health(self) -> Dict[str, Any]:
        """
        Kiểm tra trạng thái kết nối của cả 2 môi trường để hiển thị trên UI Dashboard.
        """
        cloud = self.get_cloud_provider()
        local = self.get_local_provider()

        return {
            "current_active": self.current_provider_type.value,
            "cloud": {
                "available": cloud.is_available(),
                "model": cloud.model_name,
            },
            "local": {
                "available": local.is_available(),
                "model": local.model_name,
                "installed_models": local.list_models() if local.is_available() else [],
            },
        }
