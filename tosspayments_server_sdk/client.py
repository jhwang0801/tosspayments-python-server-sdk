from tosspayments_server_sdk.config import Config
from tosspayments_server_sdk.http_client import HTTPClient
from tosspayments_server_sdk.resources.payments import PaymentResource
from tosspayments_server_sdk.resources.webhooks import WebhookResource


class Client:

    def __init__(
        self,
        secret_key: str,
        api_version: str = "v1",
        timeout: int = 30,
        max_retries: int = 3,
    ):
        """

        Args:
            secret_key: 토스페이먼츠 시크릿 키
            api_version:  API 버전
            timeout:  요청 타임아웃 (초)
            max_retries: 최대 재시도 횟수
        """
        self.config = Config(
            secret_key=secret_key,
            api_version=api_version,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.config.validate()

        self._http_client = HTTPClient(self.config)
        self.payments = PaymentResource(self._http_client)
        self.webhooks = WebhookResource()  # HTTP client 필요 없음

    @property
    def is_live_mode(self) -> bool:
        return self.config.is_live_mode

    @property
    def is_test_mode(self) -> bool:
        return self.config.is_test_mode
