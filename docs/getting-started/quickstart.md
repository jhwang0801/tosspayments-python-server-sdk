# Quickstart Guide

This guide will help you make your first payment integration with TossPayments in under 5 minutes.

## Prerequisites

- Python 3.9 or higher
- TossPayments API credentials (test keys)
- Basic understanding of payment flows

## Step 1: Install the SDK

```bash
pip install tosspayments-python-server-sdk
```

## Step 2: Initialize the Client

```python
from tosspayments_server_sdk import Client

# Initialize with your test secret key
client = Client(secret_key="test_sk_your_test_key_here")

# Verify environment
print(f"Test mode: {client.is_test_mode}")  # Should be True
```

## Step 3: Payment Flow Overview

TossPayments follows this payment flow:

1. **Frontend**: Customer initiates payment using TossPayments Payment Widget
2. **Frontend**: Payment widget returns `paymentKey`, `orderId`, and `amount`
3. **Backend**: Your server confirms the payment using this SDK
4. **Backend**: Handle the payment result

## Step 4: Confirm a Payment

After receiving payment details from your frontend:

```python
from tosspayments_server_sdk import Client, APIError

client = Client(secret_key="test_sk_your_test_key_here")

try:
    # Confirm payment with details from frontend
    payment = client.payments.confirm(
        payment_key="mc_1234567890123456789012345678901234567890",  # From frontend
        order_id="order_20241201_001",                              # Your order ID
        amount=15000                                                # Amount in KRW
    )
    
    # Payment successful
    print(f"✅ Payment confirmed!")
    print(f"Order ID: {payment.order_id}")
    print(f"Payment Status: {payment.status.value}")
    print(f"Total Amount: {payment.total_amount:,} KRW")
    print(f"Payment Method: {payment.method}")
    
    # Check payment status
    if payment.is_paid():
        print("💳 Payment completed successfully")
        # Process order fulfillment here
    
except APIError as e:
    print(f"❌ Payment failed: {e.message}")
    print(f"Error code: {e.error_code}")
    # Handle payment failure
```

## Step 5: Retrieve Payment Information

You can retrieve payment details anytime:

```python
# Retrieve by payment key
payment = client.payments.retrieve("mc_1234567890123456789012345678901234567890")

# Or retrieve by order ID
payment = client.payments.retrieve_by_order_id("order_20241201_001")

print(f"Payment Status: {payment.status.value}")
print(f"Total Amount: {payment.total_amount:,} KRW")
print(f"Balance Amount: {payment.balance_amount:,} KRW")
```

## Step 6: Cancel a Payment (Optional)

If you need to cancel a payment:

```python
try:
    # Full cancellation
    canceled_payment = client.payments.cancel(
        payment_key="mc_1234567890123456789012345678901234567890",
        cancel_reason="Customer requested cancellation"
    )
    
    print(f"✅ Payment canceled")
    print(f"Canceled amount: {canceled_payment.get_canceled_amount():,} KRW")
    
except APIError as e:
    print(f"❌ Cancellation failed: {e.message}")
```

### Partial Cancellation

```python
# Cancel only part of the payment
partial_cancel = client.payments.cancel(
    payment_key="mc_1234567890123456789012345678901234567890",
    cancel_reason="Partial refund requested",
    cancel_amount=5000  # Cancel 5,000 KRW out of total
)

print(f"Partially canceled: {partial_cancel.get_canceled_amount():,} KRW")
print(f"Remaining balance: {partial_cancel.balance_amount:,} KRW")
```

## Complete Example

Here's a complete example integrating all steps:

```python
from tosspayments_server_sdk import Client, APIError
import os

def process_payment():
    # Initialize client
    client = Client(secret_key=os.getenv("TOSS_SECRET_KEY"))
    
    # Example payment data (normally from your frontend)
    payment_data = {
        "payment_key": "mc_1234567890123456789012345678901234567890",
        "order_id": "order_20241201_001",
        "amount": 15000
    }
    
    try:
        # Step 1: Confirm payment
        payment = client.payments.confirm(**payment_data)
        
        if payment.is_paid():
            print(f"✅ Payment successful: {payment.order_id}")
            
            # Step 2: Process your business logic
            # - Update order status
            # - Send confirmation email
            # - Update inventory
            
            return {
                "status": "success",
                "payment_id": payment.payment_key,
                "order_id": payment.order_id,
                "amount": payment.total_amount
            }
        else:
            print(f"⏳ Payment pending: {payment.status.value}")
            return {"status": "pending", "payment": payment}
            
    except APIError as e:
        print(f"❌ Payment error: {e.message}")
        return {
            "status": "error",
            "error_code": e.error_code,
            "message": e.message
        }

if __name__ == "__main__":
    result = process_payment()
    print(f"Result: {result}")
```

## Next Steps

Now that you've completed the quickstart:

1. **[Webhook Integration](../api-reference/webhooks.md)** - Handle real-time payment events
2. **[API Reference](../api-reference/client.md)** - Explore all available methods
3. **[Payment Models](../api-reference/models.md)** - Understanding payment data structures
4. **[Configuration Guide](configuration.md)** - Advanced configuration options
