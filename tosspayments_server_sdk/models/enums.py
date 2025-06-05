from enum import Enum


class PaymentStatus(Enum):
    """결제 상태"""

    READY = "READY"  # 결제 준비
    IN_PROGRESS = "IN_PROGRESS"  # 결제 진행 중
    WAITING_FOR_DEPOSIT = "WAITING_FOR_DEPOSIT"  # 입금 대기
    DONE = "DONE"  # 결제 완료
    CANCELED = "CANCELED"  # 결제 취소
    PARTIAL_CANCELED = "PARTIAL_CANCELED"  # 부분 취소
    ABORTED = "ABORTED"  # 결제 중단
    EXPIRED = "EXPIRED"  # 결제 만료


class PaymentMethod(Enum):
    """결제 수단"""

    CARD = "카드"
    VIRTUAL_ACCOUNT = "가상계좌"
    SIMPLE_PAYMENT = "간편결제"
    MOBILE_PHONE = "휴대폰"
    ACCOUNT_TRANSFER = "계좌이체"
    CULTURE_GIFT_CERTIFICATE = "문화상품권"
    BOOK_CULTURE_GIFT_CERTIFICATE = "도서문화상품권"
    GAME_CULTURE_GIFT_CERTIFICATE = "게임문화상품권"


class PaymentType(Enum):
    """결제 타입"""

    NORMAL = "NORMAL"  # 일반결제
    BILLING = "BILLING"  # 자동결제
    BRANDPAY = "BRANDPAY"  # 브랜드페이
