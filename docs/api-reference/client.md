# Client

The `Client` class is the main entry point for interacting with the TossPayments API.

## Class Definition

```python
class Client:
    def __init__(
        self,
        secret_key: str,
        api_version: str = "v1",
        timeout: int = 30,
        max_retries: int = 3,
    )
```

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `secret_key` | `str` | Required | TossPayments secret key (`test_sk_*` or `live_sk_*`) |
| `api_version` | `str` | `"v1"` | TossPayments API version |
| `timeout` | `int` | `30` | HTTP request timeout in seconds |
| `max_retries` | `int` | `3` | Maximum number of retry attempts for failed requests |

## Properties

### `is_live_mode`

```python
@property
def is_live_mode(self) -> bool
```

Returns `True` if the client is configured for live (production) mode.

**Returns:** `bool`

**Example:**
```python
client = Client(secret_key="live_sk_...")
print(client.is_live_mode)  # True
```

### `is_test_mode`

```python
@property
def is_test_mode(self) -> bool
```

Returns `True` if the client is configured for test mode.

**Returns:** `bool`

**Example:**
```python
client = Client(secret_key="test_sk_...")
print(client.is_test_mode)  # True
```

## Resource Access

### `payments`

```python
@property
def payments(self) -> PaymentResource
```

Access to payment-related operations.

**Returns:** [`PaymentResource`](payments.md)

**Example:**
```python
client = Client(secret_key="test_sk_...")
payment = client.payments.retrieve("payment_key_here")
```

### `webhooks`

```python
@property
def webhooks(self) -> WebhookResource
```

Access to webhook-related operations.

**Returns:** [`WebhookResource`](webhooks.md)

**Example:**
```python
client = Client(secret_key="test_sk_...")
webhook_event = client.webhooks.verify_and_parse(request_body)
```

## Usage Examples

### Basic Initialization

```python
from tosspayments_server_sdk import Client

# Test environment
client = Client(secret_key="test_sk_your_key_here")

# Live environment
client = Client(secret_key="live_sk_your_key_here")
```

### Advanced Configuration

```python
from tosspayments_server_sdk import Client

client = Client(
    secret_key="test_sk_your_key_here",
    api_version="v1",
    timeout=60,         # 60 second timeout
    max_retries=5       # 5 retry attempts
)
```

### Environment Detection

```python
client = Client(secret_key="test_sk_your_key_here")

if client.is_test_mode:
    print("Running in test mode")
    # Use test payment methods
elif client.is_live_mode:
    print("Running in live mode")
    # Process real payments
```

### Using Environment Variables

```python
import os
from tosspayments_server_sdk import Client

client = Client(secret_key=os.getenv("TOSS_SECRET_KEY"))

# Verify configuration
print(f"Environment: {'Test' if client.is_test_mode else 'Live'}")
print(f"API URL: {client.config.api_url}")
```

## Configuration Details

The client automatically configures internal components:

### HTTP Client Settings

- **Base URL**: `https://api.tosspayments.com`
- **Authentication**: Basic Auth with secret key
- **Retry Policy**: Exponential backoff for 5xx errors
- **Timeout**: Configurable (default: 30 seconds)

### Retry Behavior

The client automatically retries requests for the following HTTP status codes:
- `500` - Internal Server Error
- `502` - Bad Gateway
- `503` - Service Unavailable
- `504` - Gateway Timeout

Retry delay follows exponential backoff with a factor of 0.5 seconds.

## Error Handling

The client may raise the following exceptions during initialization:

```python
from tosspayments_server_sdk import Client, ValidationError

try:
    client = Client(secret_key="invalid_key_format")
except ValidationError as e:
    print(f"Configuration error: {e}")
```

### Common Validation Errors

- **Invalid secret key format**: Key must start with `test_sk_` or `live_sk_`
- **Invalid timeout**: Must be a positive integer
- **Invalid max_retries**: Must be a non-negative integer

## Related Documentation

- [PaymentResource](payments.md) - Payment operations
- [WebhookResource](webhooks.md) - Webhook handling
- [Models](models.md) - Data structures
- [Getting Started](../getting-started/quickstart.md) - Quickstart guide