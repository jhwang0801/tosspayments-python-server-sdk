import base64
import hashlib
import hmac
from typing import Union, Dict, Any


def verify_payment_webhook_secret(
    webhook_data: Dict[str, Any],
    expected_secret: str,
) -> bool:
    """verify secret value for payment webhook (only for DEPOSIT_CALLBACK)

    Args:
        webhook_data (Dict[str, Any]): webhook event body (웹훅 이벤트 본문)
        expected_secret (str): secret (결제 승인 시 받은 secret 값)

    Returns:
        bool: 검증 성공 여부
    """
    webhook_secret = webhook_data.get("secret")
    return webhook_secret == expected_secret


# def verify_webhook_signature(
#     payload: Union[str, bytes], signature: str, secret_key: str, transmission_time: str
# ) -> bool:
#     """웹훅 시그니처 검증 (HMAC SHA-256)
#
#     Args:
#         payload (Union[str, bytes]): 웹훅 페이로드
#         signature (str): tosspayments-signature 헤더 값
#         secret_key (str): 토스페이먼츠 시크릿 키
#         transmission_time (str): tosspayments-webhook-transmission-time 헤더 값
#
#     Returns:
#         bool: 검증 성공 여부
#
#     Example:
#         >>> verify_webhook_signature(payload, signature, "sk_test_...", "1640995200")
#         True
#     """
#     try:
#         if not signature.startswith("v1:"):
#             return False
#
#         signature_parts = signature[3:].split(",")
#
#         if isinstance(payload, str):
#             payload_bytes = payload.encode("utf-8")
#         else:
#             payload_bytes = payload
#
#         message = f"{payload_bytes.decode('utf-8')}:{transmission_time}"
#
#         expected_hash = hmac.new(
#             secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
#         ).digest()
#
#         for signature_part in signature_parts:
#             try:
#                 decoded_signature = base64.b64decode(signature_part)
#
#                 if hmac.compare_digest(expected_hash, decoded_signature):
#                     return True
#             except Exception:
#                 continue
#
#         return False
#
#     except Exception:
#         return False
