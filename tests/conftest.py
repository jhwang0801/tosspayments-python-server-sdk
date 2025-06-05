from unittest.mock import patch

import pytest

from tosspayments_server_sdk.client import Client


@pytest.fixture
def test_secret_key():
    return "test_sk"


@pytest.fixture
def live_secret_key():
    return "live_sk"


@pytest.fixture
def toss_client(test_secret_key):
    return Client(secret_key=test_secret_key)


@pytest.fixture
def mock_payment_data():
    return {
        "mId": "tosspayments",
        "lastTransactionKey": "9C62B18EEF0DE3EB7F4422EB6D14BC6E",
        "paymentKey": "5EnNZRJGvaBX7zk2yd8ydw26XvwXkLrx9POLqKQjmAw4b0e1",
        "orderId": "a4CWyWY5m89PNh7xJwhk1",
        "orderName": "토스 티셔츠 외 2건",
        "taxExemptionAmount": 0,
        "status": "DONE",
        "requestedAt": "2024-02-13T12:17:57+09:00",
        "approvedAt": "2024-02-13T12:18:14+09:00",
        "useEscrow": False,
        "cultureExpense": False,
        "card": {
            "issuerCode": "71",
            "acquirerCode": "71",
            "number": "12345678****000*",
            "installmentPlanMonths": 0,
            "isInterestFree": False,
            "interestPayer": None,
            "approveNo": "00000000",
            "useCardPoint": False,
            "cardType": "신용",
            "ownerType": "개인",
            "acquireStatus": "READY",
            "amount": 1000,
        },
        "virtualAccount": None,
        "transfer": None,
        "mobilePhone": None,
        "giftCertificate": None,
        "cashReceipt": None,
        "cashReceipts": None,
        "discount": None,
        "cancels": None,
        "secret": None,
        "type": "NORMAL",
        "easyPay": {"provider": "토스페이", "amount": 0, "discountAmount": 0},
        "country": "KR",
        "failure": None,
        "isPartialCancelable": True,
        "receipt": {
            "url": "https://dashboard.tosspayments.com/receipt/redirection?transactionId=tviva20240213121757MvuS8&ref=PX"
        },
        "checkout": {
            "url": "https://api.tosspayments.com/v1/payments/5EnNZRJGvaBX7zk2yd8ydw26XvwXkLrx9POLqKQjmAw4b0e1/checkout"
        },
        "currency": "KRW",
        "totalAmount": 1000,
        "balanceAmount": 1000,
        "suppliedAmount": 909,
        "vat": 91,
        "taxFreeAmount": 0,
        "metadata": None,
        "method": "카드",
        "version": "2022-11-16",
    }


@pytest.fixture
def mock_cancel_data():
    return {
        "mId": "tosspayments",
        "lastTransactionKey": "090A796806E726BBB929F4A2CA7DB9A7",
        "paymentKey": "5EnNZRJGvaBX7zk2yd8ydw26XvwXkLrx9POLqKQjmAw4b0e1",
        "orderId": "a4CWyWY5m89PNh7xJwhk1",
        "orderName": "토스 티셔츠 외 2건",
        "taxExemptionAmount": 0,
        "status": "CANCELED",
        "requestedAt": "2024-02-13T12:17:57+09:00",
        "approvedAt": "2024-02-13T12:18:14+09:00",
        "useEscrow": False,
        "cultureExpense": False,
        "card": {
            "issuerCode": "71",
            "acquirerCode": "71",
            "number": "12345678****000*",
            "installmentPlanMonths": 0,
            "isInterestFree": False,
            "interestPayer": None,
            "approveNo": "00000000",
            "useCardPoint": False,
            "cardType": "신용",
            "ownerType": "개인",
            "acquireStatus": "READY",
            "amount": 1000,
        },
        "virtualAccount": None,
        "transfer": None,
        "mobilePhone": None,
        "giftCertificate": None,
        "cashReceipt": None,
        "cashReceipts": None,
        "discount": None,
        "cancels": [
            {
                "transactionKey": "090A796806E726BBB929F4A2CA7DB9A7",
                "cancelReason": "테스트 결제 취소",
                "taxExemptionAmount": 0,
                "canceledAt": "2024-02-13T12:20:23+09:00",
                "transferDiscountAmount": 0,
                "easyPayDiscountAmount": 0,
                "receiptKey": None,
                "cancelAmount": 1000,
                "taxFreeAmount": 0,
                "refundableAmount": 0,
                "cancelStatus": "DONE",
                "cancelRequestId": None,
            }
        ],
        "secret": None,
        "type": "NORMAL",
        "easyPay": {"provider": "토스페이", "amount": 0, "discountAmount": 0},
        "country": "KR",
        "failure": None,
        "isPartialCancelable": True,
        "receipt": {
            "url": "https://dashboard.tosspayments.com/receipt/redirection?transactionId=tviva20240213121757MvuS8&ref=PX"
        },
        "checkout": {
            "url": "https://api.tosspayments.com/v1/payments/5EnNZRJGvaBX7zk2yd8ydw26XvwXkLrx9POLqKQjmAw4b0e1/checkout"
        },
        "currency": "KRW",
        "totalAmount": 1000,
        "balanceAmount": 0,
        "suppliedAmount": 0,
        "vat": 0,
        "taxFreeAmount": 0,
        "method": "카드",
        "version": "2022-11-16",
        "metadata": None,
    }


@pytest.fixture
def mock_http_client():
    with patch("tosspayments_server_sdk.client.HTTPClient") as mock:
        yield mock
