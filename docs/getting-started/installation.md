# Installation

## Requirements

- **Python**: 3.9 or higher
- **Dependencies**: requests>=2.28.0

## Install from PyPI

The easiest way to install the TossPayments Python Server SDK is via pip:

```bash
pip install tosspayments-python-server-sdk
```

## Verify Installation

After installation, verify that the SDK is working correctly:

```python
import tosspayments_server_sdk

print(f"SDK Version: {tosspayments_server_sdk.__version__}")

# Test client initialization (with dummy key)
try:
    client = tosspayments_server_sdk.Client(secret_key="test_sk_dummy")
    print("✅ SDK installed successfully!")
    print(f"Test mode: {client.is_test_mode}")
except Exception as e:
    print(f"❌ Installation issue: {e}")
```

## Next Steps

Once installed, proceed to:

1. [Configuration](configuration.md) - Set up your API credentials
2. [Quickstart](quickstart.md) - Your first payment integration
3. [API Reference](../api-reference/client.md) - Detailed API documentation