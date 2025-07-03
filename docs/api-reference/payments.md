# PaymentResource

The `PaymentResource` class provides methods for payment operations including confirmation, retrieval, and cancellation.

## Class Overview

```python
class PaymentResource(BaseResource):
    """Payment API Resource for TossPayments integration"""
```

Access the PaymentResource through the client:

```python
from tosspayments_server_sdk import Client

client = Client(secret_key="test_sk_...")
payments = client.payments  # PaymentResource instance
```

## Methods

### `retrieve()`

Retrieve a payment using the payment key.

```python
def retrieve(self, payment_key: str) -> Payment
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `payment_key` | `str` | Yes | TossPayments payment key |

**Returns:** [`Payment`](models.md#payment) object


**Example:**
```python
try:
    payment = client.payments.retrieve("mc_1234567890123456789012345678901234567890")
    print(f"Payment Status: {payment.status.value}")
    print(f"Amount: {payment.total_amount:,} KRW")
except PaymentNotFoundError:
    print("Payment not found")
except APIError as e:
    print(f"API Error: {e.message}")
```

### `retrieve_by_order_id()`

Retrieve a payment using the order ID.

```python
def retrieve_by_order_id(self, order_id: str) -> Payment
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `order_id` | `str` | Yes | Your system's order ID |

**Returns:** [`Payment`](models.md#payment) object


**Example:**
```python
try:
    payment = client.payments.retrieve_by_order_id("order_20241201_001")
    print(f"Order ID: {payment.order_id}")
    print(f"Payment Key: {payment.payment_key}")
    print(f"Status: {payment.status.value}")
except PaymentNotFoundError:
    print("Order not found")
```

### `confirm()`

Confirm a payment that was initiated on the client side.

```python
def confirm(self, payment_key: str, order_id: str, amount: int) -> Payment
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `payment_key` | `str` | Yes | Payment key from client-side payment widget |
| `order_id` | `str` | Yes | Your system's order identifier |
| `amount` | `int` | Yes | Payment amount in KRW (must be positive) |

**Returns:** [`Payment`](models.md#payment) object


**Example:**
```python
try:
    payment = client.payments.confirm(
        payment_key="mc_1234567890123456789012345678901234567890",
        order_id="order_20241201_001",
        amount=15000
    )
    
    if payment.is_paid():
        print("✅ Payment confirmed successfully")
        print(f"Transaction ID: {payment.payment_key}")
        print(f"Method: {payment.method}")
    else:
        print(f"Payment status: {payment.status.value}")
        
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except APIError as e:
    print(f"Payment failed: {e.message}")
    print(f"Error code: {e.error_code}")
```

### `cancel()`

Cancel a payment (full or partial cancellation).

```python
def cancel(
    self,
    payment_key: str,
    cancel_reason: str,
    cancel_amount: Optional[int] = None,
    refund_receive_account: Optional[Dict[str, str]] = None,
    tax_free_amount: Optional[int] = None,
) -> Payment
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `payment_key` | `str` | Yes | Payment key of the payment to cancel |
| `cancel_reason` | `str` | Yes | Reason for cancellation |
| `cancel_amount` | `int` | No | Amount to cancel (omit for full cancellation) |
| `refund_receive_account` | `Dict[str, str]` | No | Customer's refund account information |
| `tax_free_amount` | `int` | No | Tax-free amount in the cancellation |

**Returns:** [`Payment`](models.md#payment) object with updated cancellation information



**Example - Full Cancellation:**
```python
try:
    canceled_payment = client.payments.cancel(
        payment_key="mc_1234567890123456789012345678901234567890",
        cancel_reason="Customer requested cancellation"
    )
    
    print(f"✅ Payment canceled")
    print(f"Canceled amount: {canceled_payment.get_canceled_amount():,} KRW")
    print(f"Status: {canceled_payment.status.value}")
    
except APIError as e:
    print(f"Cancellation failed: {e.message}")
```

**Example - Partial Cancellation:**
```python
try:
    partial_cancel = client.payments.cancel(
        payment_key="mc_1234567890123456789012345678901234567890",
        cancel_reason="Partial refund for damaged item",
        cancel_amount=5000  # Cancel 5,000 KRW
    )
    
    print(f"✅ Partial cancellation completed")
    print(f"Canceled: {partial_cancel.get_canceled_amount():,} KRW")
    print(f"Remaining: {partial_cancel.balance_amount:,} KRW")
    
except APIError as e:
    print(f"Partial cancellation failed: {e.message}")
```

**Example - Cancellation with Refund Account:**
```python
refund_account = {
    "bank": "신한",
    "accountNumber": "12345678901",
    "holderName": "홍길동"
}

try:
    canceled_payment = client.payments.cancel(
        payment_key="mc_1234567890123456789012345678901234567890",
        cancel_reason="Refund to customer account",
        refund_receive_account=refund_account
    )
    
    print("✅ Payment canceled with refund account")
    
except APIError as e:
    print(f"Cancellation failed: {e.message}")
```

## Usage Patterns

### Check Payment Status Before Operations

```python
def safe_payment_operation(client, payment_key):
    # Always check current status first
    payment = client.payments.retrieve(payment_key)
    
    if payment.is_paid():
        print("Payment is completed")
        return payment
    elif payment.is_canceled():
        print("Payment is already canceled")
        return payment
    else:
        print(f"Payment status: {payment.status.value}")
        return payment
```

### Batch Payment Processing

```python
def process_payment_batch(client, payment_requests):
    results = []
    
    for req in payment_requests:
        try:
            payment = client.payments.confirm(
                payment_key=req["payment_key"],
                order_id=req["order_id"],
                amount=req["amount"]
            )
            
            results.append({
                "order_id": req["order_id"],
                "status": "success",
                "payment": payment
            })
            
        except APIError as e:
            results.append({
                "order_id": req["order_id"],
                "status": "error",
                "error": e.message,
                "error_code": e.error_code
            })
    
    return results
```

### Conditional Cancellation

```python
def conditional_cancel(client, payment_key, reason):
    payment = client.payments.retrieve(payment_key)
    
    if not payment.can_be_canceled():
        print("Payment cannot be canceled")
        return None
    
    if payment.get_cancelable_amount() < 1000:
        print("Cancelable amount too small")
        return None
    
    return client.payments.cancel(payment_key, reason)
```


## API Endpoints

The PaymentResource methods correspond to these TossPayments API endpoints:

| Method | HTTP Method | Endpoint |
|--------|-------------|----------|
| `retrieve()` | GET | `/payments/{paymentKey}` |
| `retrieve_by_order_id()` | GET | `/payments/orders/{orderId}` |
| `confirm()` | POST | `/payments/confirm` |
| `cancel()` | POST | `/payments/{paymentKey}/cancel` |

## Related Documentation

- [Payment Model](models.md#payment) - Payment data structure
- [Payment Status](models.md#paymentstatus) - Available payment statuses
- [Quickstart Guide](../getting-started/quickstart.md) - Error handling examples
- [Webhook Integration](webhooks.md) - Real-time payment events