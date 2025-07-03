# WebhookResource

The `WebhookResource` class handles webhook event verification and parsing for real-time payment notifications from TossPayments.

## Class Overview

```python
class WebhookResource:
    """Webhook verification and parsing for TossPayments events"""
```

Access the WebhookResource through the client:

```python
from tosspayments_server_sdk import Client

client = Client(secret_key="test_sk_...")
webhooks = client.webhooks  # WebhookResource instance
```

## Methods

### `verify_and_parse()`

Verify and parse webhook payload from TossPayments.

```python
def verify_and_parse(self, payload: Union[str, bytes]) -> WebhookEvent
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `payload` | `Union[str, bytes]` | Yes | Raw webhook payload from TossPayments |

**Returns:** [`WebhookEvent`](#webhook-events) - Parsed webhook event object

**Example:**
```python
from tosspayments_server_sdk import WebhookVerificationError

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        # Parse webhook data
        webhook_event = client.webhooks.verify_and_parse(request.data)
        
        # Handle different event types
        if webhook_event.is_payment_event:
            handle_payment_event(webhook_event)
        elif webhook_event.is_cancel_event:
            handle_cancel_event(webhook_event)
        elif webhook_event.is_virtual_account_event:
            handle_virtual_account_event(webhook_event)
            
        return "OK", 200
        
    except WebhookVerificationError as e:
        print(f"Webhook verification failed: {e}")
        return "Bad Request", 400
```

## Webhook Events

### `WebhookEvent` Type Union

```python
WebhookEvent = Union[
    PaymentStatusChangedEvent,
    DepositCallbackEvent,
    CancelStatusChangedEvent,
]
```

All webhook events inherit from `BaseWebhookEvent` and provide common properties.

### `BaseWebhookEvent`

Base class for all webhook events.

```python
@dataclass
class BaseWebhookEvent(BaseModel, ABC):
    created_at: datetime
    event_type: str
```

#### Properties

```python
@property
def is_payment_event(self) -> bool
```
Returns `True` if this is a payment status change event.

```python
@property
def is_cancel_event(self) -> bool
```
Returns `True` if this is a cancellation event.

```python
@property
def is_virtual_account_event(self) -> bool
```
Returns `True` if this is a virtual account deposit event.

### `PaymentStatusChangedEvent`

Triggered when a payment status changes.

```python
@dataclass
class PaymentStatusChangedEvent(BaseWebhookEvent):
    payment: Payment
```

#### Additional Properties

```python
@property
def payment_key(self) -> str
```
Returns the payment key from the embedded payment object.

```python
@property
def order_id(self) -> str
```
Returns the order ID from the embedded payment object.

```python
@property
def status(self) -> PaymentStatus
```
Returns the current payment status.

#### Methods

```python
def is_payment_completed(self) -> bool
```
Returns `True` if the payment status is `DONE`.

```python
def is_payment_canceled(self) -> bool
```
Returns `True` if the payment status is `CANCELED` or `PARTIAL_CANCELED`.

#### Example

```python
def handle_payment_event(event: PaymentStatusChangedEvent):
    payment = event.payment
    
    print(f"Payment status changed: {event.payment_key}")
    print(f"Order: {event.order_id}")
    print(f"New status: {event.status.value}")
    print(f"Amount: {payment.total_amount:,} KRW")
    
    if event.is_payment_completed():
        print("✅ Payment completed - process order")
        # Update order status, send confirmation email, etc.
        process_successful_payment(payment)
        
    elif event.is_payment_canceled():
        print("❌ Payment canceled - handle cancellation")
        # Update order status, process refund, etc.
        handle_payment_cancellation(payment)
        
    else:
        print(f"⏳ Payment status: {event.status.value}")
        # Handle other statuses (waiting, in progress, etc.)
        log_payment_status_change(payment)
```

### `CancelStatusChangedEvent`

Triggered when a payment cancellation occurs.

```python
@dataclass
class CancelStatusChangedEvent(BaseWebhookEvent):
    cancellation: Cancellation
```

#### Properties

```python
@property
def cancel_amount(self) -> int
```
Returns the amount that was canceled.

```python
@property
def cancel_reason(self) -> str
```
Returns the reason for cancellation.

```python
@property
def transaction_key(self) -> str
```
Returns the cancellation transaction key.

#### Example

```python
def handle_cancel_event(event: CancelStatusChangedEvent):
    cancellation = event.cancellation
    
    print(f"Cancellation occurred: {event.transaction_key}")
    print(f"Amount canceled: {event.cancel_amount:,} KRW")
    print(f"Reason: {event.cancel_reason}")
    print(f"Date: {cancellation.canceled_at}")
    
    # Process cancellation
    process_payment_cancellation(
        transaction_key=event.transaction_key,
        amount=event.cancel_amount,
        reason=event.cancel_reason
    )
```

### `DepositCallbackEvent`

Triggered when a virtual account deposit is completed.

```python
@dataclass
class DepositCallbackEvent(BaseWebhookEvent):
    secret: str
    status: PaymentStatus
    transaction_key: str
    order_id: str
```

#### Methods

```python
def is_deposit_completed(self) -> bool
```
Returns `True` if the deposit status indicates completion.

#### Example

```python
def handle_virtual_account_event(event: DepositCallbackEvent):
    print(f"Virtual account deposit: {event.transaction_key}")
    print(f"Order: {event.order_id}")
    print(f"Status: {event.status.value}")
    
    if event.is_deposit_completed():
        print("✅ Virtual account deposit completed")
        # Process the deposit
        process_virtual_account_deposit(
            order_id=event.order_id,
            transaction_key=event.transaction_key
        )
    else:
        print(f"⏳ Deposit status: {event.status.value}")
```

## Related Documentation

- [Models](models.md) - Webhook event data structures
- [Quickstart Guide](../getting-started/quickstart.md) - Basic error handling
- [Configuration](../getting-started/configuration.md) - Security best practices