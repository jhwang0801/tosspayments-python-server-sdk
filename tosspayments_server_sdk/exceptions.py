from typing import Optional, Dict, Any


class TossPaymentsError(Exception):
    """모든 토스페이먼츠 SDK 예외의 기본 클래스"""

    pass


class APIError(TossPaymentsError):
    """API 호출 중 발생하는 오류"""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.response_data = response_data or {}

    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class WebhookVerificationError(TossPaymentsError):
    """웹훅 파싱 실패 에러"""

    pass


class AuthenticationError(TossPaymentsError):
    """인증 관련 오류"""

    pass


class ValidationError(TossPaymentsError):
    """입력값 검증 오류"""

    pass


class NetworkError(TossPaymentsError):
    """네트워크 관련 오류"""

    pass


class RateLimitError(APIError):
    """API 요청 한도 초과"""

    pass


class PaymentNotFoundError(APIError):
    """결제 정보를 찾을 수 없음"""

    pass


class PaymentAlreadyCanceledError(APIError):
    """이미 취소된 결제"""

    pass


class InsufficientAmountError(APIError):
    """취소 가능 금액 부족"""

    pass


class PaymentCancelError(APIError):
    """결제 취소 실패"""

    pass
