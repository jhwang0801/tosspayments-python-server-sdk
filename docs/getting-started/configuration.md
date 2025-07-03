# Configuration

## API Credentials

To use the TossPayments Python Server SDK, you need to obtain API credentials from the TossPayments Developer Console.

### Getting Your API Keys

1. **Register at TossPayments**: Visit [TossPayments Developer Console](https://developers.tosspayments.com/)
2. **Create an Application**: Set up your application to get API keys
3. **Obtain Secret Keys**:
   - **Test Key**: `test_sk_...` for development and testing
   - **Live Key**: `live_sk_...` for production use

!!! warning "Security Notice"
    Never expose your secret keys in client-side code, public repositories, or logs. Always use server-side environment variables.

## Client Configuration

### Basic Configuration

```python
from tosspayments_server_sdk import Client

# Test environment
client = Client(secret_key="test_sk_your_test_key_here")

# Live environment
client = Client(secret_key="live_sk_your_live_key_here")
```

### Advanced Configuration

```python
from tosspayments_server_sdk import Client

client = Client(
    secret_key="test_sk_your_key_here",
    api_version="v1",           # API version (default: "v1")
    timeout=30,                 # Request timeout in seconds (default: 30)
    max_retries=3              # Maximum retry attempts (default: 3)
)
```

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `secret_key` | `str` | Required | TossPayments secret key |
| `api_version` | `str` | `"v1"` | TossPayments API version |
| `timeout` | `int` | `30` | HTTP request timeout in seconds |
| `max_retries` | `int` | `3` | Maximum number of retry attempts |

## Environment Detection

The SDK automatically detects your environment based on your secret key:

```python
client = Client(secret_key="test_sk_...")

# Environment detection
print(f"Test mode: {client.is_test_mode}")      # True
print(f"Live mode: {client.is_live_mode}")      # False

# Configuration details
print(f"API URL: {client.config.api_url}")
print(f"Timeout: {client.config.timeout}")
print(f"Max retries: {client.config.max_retries}")
```

## Environment Variables

For better security, store your API keys in environment variables:

### Setting Environment Variables

```python
# .env file
TOSS_SECRET_KEY=test_sk_your_key_here
```

### Using Environment Variables

```python
import os
from tosspayments_server_sdk import Client

# Load from environment variable
secret_key = os.getenv("TOSS_SECRET_KEY")
if not secret_key:
    raise ValueError("TOSS_SECRET_KEY environment variable is required")

client = Client(secret_key=secret_key)
```

### Using python-dotenv

```python
# First install: pip install python-dotenv
from dotenv import load_dotenv
import os
from tosspayments_server_sdk import Client

# Load environment variables from .env file
load_dotenv()

client = Client(secret_key=os.getenv("TOSS_SECRET_KEY"))
```

## Configuration Validation

The SDK automatically validates your configuration:

```python
from tosspayments_server_sdk import Client
from tosspayments_server_sdk.exceptions import ValidationError

try:
    client = Client(secret_key="invalid_key")
except ValidationError as e:
    print(f"Configuration error: {e}")
```

### Validation Rules

- **Secret Key Format**: Must start with `test_sk_` or `live_sk_`
- **Timeout**: Must be a positive integer
- **Max Retries**: Must be a non-negative integer
- **API Version**: Must be a valid string

## HTTP Client Configuration

The SDK uses an HTTP client with the following default settings:

```python
# Default HTTP client settings
{
    "timeout": 30,              # Request timeout
    "max_retries": 3,           # Retry attempts
    "backoff_factor": 0.5,      # Exponential backoff factor
    "status_forcelist": [500, 502, 503, 504]  # HTTP statuses to retry
}
```

### Custom HTTP Configuration

```python
from tosspayments_server_sdk import Client

# Custom timeout and retry settings
client = Client(
    secret_key="test_sk_your_key_here",
    timeout=60,        # 60 seconds timeout
    max_retries=5      # 5 retry attempts
)
```

## Testing Configuration

For testing your configuration:

```python
from tosspayments_server_sdk import Client

def test_configuration():
    client = Client(secret_key="test_sk_your_key_here")
    
    # Test environment detection
    assert client.is_test_mode == True
    assert client.is_live_mode == False
    
    # Test API URL construction
    expected_url = "https://api.tosspayments.com/v1"
    assert client.config.api_url == expected_url
    
    print("✅ Configuration test passed!")

if __name__ == "__main__":
    test_configuration()
```

## Next Steps

With your configuration set up, you're ready to:

1. [Quickstart Guide](quickstart.md) - Make your first API call
2. [Payment Processing](../api-reference/payments.md) - Learn about payment operations
3. [API Reference](../api-reference/client.md) - Complete client documentation