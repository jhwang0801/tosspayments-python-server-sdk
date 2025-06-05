# TossPayments Python Server SDK

> **안내**  
> - 이 패키지는 토스페이먼츠에서 공식적으로 제공하는 SDK가 아닙니다.  
> - 토스페이먼츠 API를 Python 서버 환경에서 보다 편리하게 활용할 수 있도록 개발된 서드파티 라이브러리입니다.  
> - 모든 기능은 토스페이먼츠 공식 API 문서(v1)를 기반으로 구현되었으며, 예제 데이터 역시 공식 문서에서 제공되는 샘플을 활용했습니다.

## 설치

```bash
pip install tosspayments-python-server-sdk
```

## 빠른 시작

### 클라이언트 초기화

```python
from tosspayments_server_sdk import Client

# 테스트 환경
client = Client(secret_key="test_sk_...")

# 실제 환경  
client = Client(secret_key="live_sk_...")
```

### 결제 승인

```python
try:
    payment = client.payments.confirm(
        payment_key="5zJ4xY7m0kODnyRpQWGrN2xqGlNvLrKwv1M9ENjbeoPaZdL6",
        order_id="a4CWyWY5m89PNh7xJwhk1",
        amount=15000
    )
    
    print(f"결제 완료: {payment.order_name}")
    print(f"결제 금액: {payment.total_amount:,}원")
    
except tosspayments_server_sdk.APIError as e:
    print(f"결제 실패: {e.message}")
```

### 결제 조회

```python
# 결제키로 조회
payment = client.payments.retrieve("5zJ4xY7m0kODnyRpQWGrN2xqGlNvLrKwv1M9ENjbeoPaZdL6")

# 주문번호로 조회  
payment = client.payments.retrieve_by_order_id("a4CWyWY5m89PNh7xJwhk1")

print(f"결제 상태: {payment.status.value}")
print(f"결제 방법: {payment.method}")
```

### 결제 취소

```python
# 전체 취소
canceled_payment = client.payments.cancel(
    payment_key="5zJ4xY7m0kODnyRpQWGrN2xqGlNvLrKwv1M9ENjbeoPaZdL6",
    cancel_reason="고객 요청"
)

# 부분 취소
canceled_payment = client.payments.cancel(
    payment_key="5zJ4xY7m0kODnyRpQWGrN2xqGlNvLrKwv1M9ENjbeoPaZdL6",
    cancel_reason="부분 환불",
    cancel_amount=5000
)

print(f"취소 완료: {canceled_payment.get_canceled_amount():,}원")
```

### 웹훅 처리

```python
from tosspayments_server_sdk import WebhookVerificationError

def handle_webhook(request):
    try:
        # 웹훅 데이터 파싱
        webhook_event = client.webhooks.verify_and_parse(request.body)
        
        if webhook_event.is_payment_event:
            payment_event = webhook_event
            print(f"결제 상태 변경: {payment_event.payment_key}")
            print(f"새로운 상태: {payment_event.status.value}")
            
            if payment_event.is_payment_completed():
                # 결제 완료 처리 로직
                pass
                
        elif webhook_event.is_cancel_event:
            cancel_event = webhook_event  
            print(f"취소 완료: {cancel_event.transaction_key}")
            
    except WebhookVerificationError as e:
        print(f"웹훅 검증 실패: {e}")
        return "Bad Request", 400
        
    return "OK", 200
```

## 주요 기능

### 🔐 인증
- 테스트/실제 환경 자동 감지
- Basic Auth 방식의 안전한 API 키 인증

### 💳 결제 관리
- 결제 승인 (`confirm`)
- 결제 조회 (`retrieve`, `retrieve_by_order_id`) 
- 결제 취소 (`cancel`)

### 🔔 웹훅 처리
- 결제 상태 변경 이벤트
- 취소 상태 변경 이벤트  
- 가상계좌 입금 완료 이벤트

### ⚡ HTTP 클라이언트
- 자동 재시도 및 백오프
- 타임아웃 설정

## 설정

```python
client = Client(
    secret_key="test_sk_...",
    api_version="v1",           # API 버전 (기본값: v1)
    timeout=30,                 # 타임아웃 (기본값: 30초)
    max_retries=3               # 최대 재시도 (기본값: 3회)
)

# 환경 확인
print(f"테스트 모드: {client.is_test_mode}")
print(f"실제 모드: {client.is_live_mode}")
```

## 지원하는 Python 버전

- Python 3.9+

## 의존성

- `requests>=2.28.0`

## 라이센스

MIT License

## 지원

- [토스페이먼츠 개발자 문서](https://docs.tosspayments.com/reference)
- [GitHub Issues](https://github.com/jhwang0801/tosspayments-python-server-sdk/issues)

## 변경 로그

### 1.0.0 (2025-06-05)
- 초기 릴리즈
- 결제 승인, 조회, 취소 기능
- 웹훅 처리 기능  