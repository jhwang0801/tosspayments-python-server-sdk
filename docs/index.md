# TossPayments Python Server SDK

[![PyPI version](https://badge.fury.io/py/tosspayments-python-server-sdk.svg)](https://badge.fury.io/py/tosspayments-python-server-sdk)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python library for TossPayments API integration, designed to make server-side payment processing simple, secure, and intuitive.

!!! warning "Third-party Library"
    This is an unofficial SDK for TossPayments API. All features are implemented based on the official TossPayments API documentation (v1) and sample data provided in the official documentation.

## Overview

The TossPayments Python Server SDK provides a complete interface for integrating TossPayments payment processing into your Python applications. It supports all major TossPayments features including payment confirmation, retrieval, cancellation, and webhook handling.

### Key Features

- **Secure Authentication** - Automatic environment detection with secure API key handling
- **Complete Payment Lifecycle** - Support for payment confirmation, retrieval, and cancellation
- **Webhook Support** - Built-in webhook verification and event handling
- **Robust HTTP Client** - Automatic retry with exponential backoff
- **Comprehensive Error Handling** - Detailed exception types for different error scenarios
- **Type Safety** - Full type hints and dataclass models for better IDE support
- **Test Environment Support** - Seamless switching between test and live environments

### Supported Python Versions

- Python 3.9+

### Dependencies

- `requests>=2.28.0`

## Quick Start

### Installation

```bash
pip install tosspayments-python-server-sdk
```

### Basic Usage

```python
from tosspayments_server_sdk import Client

# Initialize client
client = Client(secret_key="test_sk_...")

# Confirm a payment
payment = client.payments.confirm(
    payment_key="payment_key_from_client",
    order_id="order_123",
    amount=15000
)

print(f"Payment Status: {payment.status.value}")
print(f"Amount: {payment.total_amount:,} KRW")
```

## Documentation Structure

- **[Getting Started](getting-started/installation.md)** - Installation and setup instructions
- **[API Reference](api-reference/client.md)** - Complete API documentation
- **[Payment Processing](api-reference/payments.md)** - Payment operations and examples
- **[Webhook Integration](api-reference/webhooks.md)** - Webhook implementation guide
- **[Data Models](api-reference/models.md)** - Payment data structures and types

## API Endpoints Coverage

| Feature | Status | Description |
|---------|---------|-------------|
| Payment Confirmation | ✅ | Confirm payments from client-side |
| Payment Retrieval | ✅ | Retrieve payment by key or order ID |
| Payment Cancellation | ✅ | Full and partial payment cancellation |
| Webhook Processing | ✅ | Payment and cancellation event handling |
| Virtual Account | ✅ | Virtual account payment support |
| Card Payment | ✅ | Credit/debit card payment support |
| Simple Payment | ✅ | Mobile wallet and simple payment methods |

## Environment Support

The SDK automatically detects your environment based on your API key:

- **Test Environment** - Keys starting with `test_sk_`
- **Live Environment** - Keys starting with `live_sk_`

## Getting Help

- **Official TossPayments Documentation**: [https://docs.tosspayments.com/reference](https://docs.tosspayments.com/reference)
- **GitHub Issues**: [Report bugs or request features](https://github.com/jhwang0801/tosspayments-python-server-sdk/issues)
- **API Reference**: Complete method documentation with examples

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/jhwang0801/tosspayments-python-server-sdk/blob/main/LICENSE) file for details.