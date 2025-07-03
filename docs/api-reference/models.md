# Models

This section documents all data models used by the TossPayments Python Server SDK.

## Base Model

### `BaseModel`

Abstract base class for all SDK models.

```python
class BaseModel(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T
    
    def to_dict(self) -> Dict[str, Any]
    def __repr__(self)
```

All models inherit from `BaseModel` and provide:
- `from_dict()` - Create instance from API response data
- `to_dict()` - Convert instance to dictionary
- `__repr__()` - String representation for debugging

## Payment Models

### `Payment`

Main payment object containing all payment information.

```python
@dataclass
class Payment(BaseModel):
    # Mandatory Fields
    version: str
    payment_key: str
    type: PaymentType
    order_id: str
    order_name: str
    mid: str
    currency: str
    method: str
    total_amount: int
    balance_amount: int
    status: PaymentStatus
    requested_at: datetime
    
    # Optional Fields
    approved_at: Optional[datetime] = None
    use_escrow: bool = False
    last_transaction_key: Optional[str] = None
    supplied_amount: int = 0
    vat: int = 0
    cultural_expense: bool = False
    tax_free_amount: int = 0
    tax_exemption_amount: int = 0
    cancels: List[Cancellation] = field(default_factory=list)
    is_partial_cancelable: bool = True
    
    # Payment Method Information
    card: Optional[Card] = None
    virtual_account: Optional[VirtualAccount] = None
    mobile_phone: Optional[Dict[str, Any]] = None
    gift_certificate: Optional[Dict[str, Any]] = None
    transfer: Optional[Dict[str, Any]] = None
    receipt: Optional[Dict[str, Any]] = None
    easy_pay: Optional[Dict[str, Any]] = None
    
    # Additional Information
    country: str = "KR"
    failure: Optional[Dict[str, Any]] = None
    cash_receipt: Optional[Dict[str, Any]] = None
    discount: Optional[Dict[str, Any]] = None
```

#### Fields

**Mandatory Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `version` | `str` | TossPayments API version |
| `payment_key` | `str` | Unique payment identifier |
| `type` | `PaymentType` | Payment type (NORMAL, BILLING, BRANDPAY) |
| `order_id` | `str` | Your system's order identifier |
| `order_name` | `str` | Display name for the order |
| `mid` | `str` | Merchant ID |
| `currency` | `str` | Currency code (usually "KRW") |
| `method` | `str` | Payment method used |
| `total_amount` | `int` | Total payment amount |
| `balance_amount` | `int` | Remaining balance (after cancellations) |
| `status` | `PaymentStatus` | Current payment status |
| `requested_at` | `datetime` | When payment was requested |

**Optional Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `approved_at` | `Optional[datetime]` | `None` | When payment was approved |
| `use_escrow` | `bool` | `False` | Whether escrow is used |
| `last_transaction_key` | `Optional[str]` | `None` | Latest transaction key |
| `supplied_amount` | `int` | `0` | Supplied amount |
| `vat` | `int` | `0` | VAT amount |
| `cultural_expense` | `bool` | `False` | Cultural expense benefit |
| `tax_free_amount` | `int` | `0` | Tax-free amount |
| `tax_exemption_amount` | `int` | `0` | Tax exemption amount |
| `cancels` | `List[Cancellation]` | `[]` | List of cancellations |
| `is_partial_cancelable` | `bool` | `True` | Whether partial cancellation is allowed |

**Payment Method Objects:**

| Field | Type | Description |
|-------|------|-------------|
| `card` | `Optional[Card]` | Card payment details |
| `virtual_account` | `Optional[VirtualAccount]` | Virtual account details |
| `mobile_phone` | `Optional[Dict[str, Any]]` | Mobile payment details |
| `gift_certificate` | `Optional[Dict[str, Any]]` | Gift certificate details |
| `transfer` | `Optional[Dict[str, Any]]` | Bank transfer details |
| `receipt` | `Optional[Dict[str, Any]]` | Receipt information |
| `easy_pay` | `Optional[Dict[str, Any]]` | Easy payment details |

#### Methods

**Status Check Methods:**

```python
def is_paid(self) -> bool
```
Returns `True` if payment status is `DONE`.

```python
def is_canceled(self) -> bool
```
Returns `True` if payment status is `CANCELED` or `PARTIAL_CANCELED`.

**Amount Methods:**

```python
def get_cancelable_amount(self) -> int
```
Returns the amount that can still be canceled (`balance_amount`).

```python
def get_canceled_amount(self) -> int
```
Returns the total amount that has been canceled (`total_amount - balance_amount`).

```python
def can_be_canceled(self) -> bool
```
Returns `True` if the payment can be canceled (`balance_amount > 0`).

#### Example

```python
# Access payment information
print(f"Order: {payment.order_id}")
print(f"Status: {payment.status.value}")
print(f"Total: {payment.total_amount:,} KRW")
print(f"Balance: {payment.balance_amount:,} KRW")

# Check payment status
if payment.is_paid():
    print("✅ Payment completed")
elif payment.is_canceled():
    print("❌ Payment canceled")
    print(f"Canceled amount: {payment.get_canceled_amount():,} KRW")

# Check cancellation capability
if payment.can_be_canceled():
    print(f"Can cancel up to: {payment.get_cancelable_amount():,} KRW")

# Access payment method details
if payment.card:
    print(f"Card issuer: {payment.card.issuer_code}")
elif payment.virtual_account:
    print(f"Virtual account: {payment.virtual_account.account_number}")
```

### `Card`

Card payment information.

```python
@dataclass
class Card(BaseModel):
    amount: int
    issuer_code: str
    acquirer_code: Optional[str] = None
    number: Optional[str] = None
    installment_plan_months: Optional[int] = None
    approve_no: Optional[str] = None
    use_card_point: Optional[bool] = None
    card_type: Optional[str] = None
    owner_type: Optional[str] = None
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `amount` | `int` | Amount paid with this card |
| `issuer_code` | `str` | Card issuer code |
| `acquirer_code` | `Optional[str]` | Card acquirer code |
| `number` | `Optional[str]` | Masked card number |
| `installment_plan_months` | `Optional[int]` | Installment plan months |
| `approve_no` | `Optional[str]` | Card approval number |
| `use_card_point` | `Optional[bool]` | Whether card points were used |
| `card_type` | `Optional[str]` | Type of card |
| `owner_type` | `Optional[str]` | Card owner type |

#### Example

```python
if payment.card:
    card = payment.card
    print(f"Card amount: {card.amount:,} KRW")
    print(f"Issuer: {card.issuer_code}")
    print(f"Masked number: {card.number}")
    
    if card.installment_plan_months:
        print(f"Installments: {card.installment_plan_months} months")
```

### `VirtualAccount`

Virtual account payment information.

```python
@dataclass
class VirtualAccount(BaseModel):
    account_type: str
    account_number: str
    bank_code: str
    customer_name: str
    due_date: datetime
    refund_status: str
    expired: bool
    settled_amount: int
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `account_type` | `str` | Type of virtual account |
| `account_number` | `str` | Virtual account number |
| `bank_code` | `str` | Bank code |
| `customer_name` | `str` | Customer name for the account |
| `due_date` | `datetime` | Payment due date |
| `refund_status` | `str` | Refund status |
| `expired` | `bool` | Whether the account has expired |
| `settled_amount` | `int` | Amount that has been settled |

#### Example

```python
if payment.virtual_account:
    va = payment.virtual_account
    print(f"Account: {va.account_number}")
    print(f"Bank: {va.bank_code}")
    print(f"Customer: {va.customer_name}")
    print(f"Due date: {va.due_date}")
    print(f"Settled: {va.settled_amount:,} KRW")
    
    if va.expired:
        print("⚠️ Virtual account has expired")
```

### `Cancellation`

Information about a payment cancellation.

```python
@dataclass
class Cancellation(BaseModel):
    cancel_amount: int
    cancel_reason: str
    canceled_at: datetime
    transaction_key: str
    receipt_key: Optional[str] = None
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `cancel_amount` | `int` | Amount that was canceled |
| `cancel_reason` | `str` | Reason for cancellation |
| `canceled_at` | `datetime` | When cancellation occurred |
| `transaction_key` | `str` | Cancellation transaction key |
| `receipt_key` | `Optional[str]` | Receipt key for cancellation |

#### Example

```python
for cancellation in payment.cancels:
    print(f"Canceled: {cancellation.cancel_amount:,} KRW")
    print(f"Reason: {cancellation.cancel_reason}")
    print(f"Date: {cancellation.canceled_at}")
    print(f"Transaction: {cancellation.transaction_key}")
```

## Enumeration Types

### `PaymentStatus`

Available payment statuses.

```python
class PaymentStatus(Enum):
    READY = "READY"                                # Payment ready
    IN_PROGRESS = "IN_PROGRESS"                    # Payment in progress
    WAITING_FOR_DEPOSIT = "WAITING_FOR_DEPOSIT"    # Waiting for deposit
    DONE = "DONE"                                  # Payment completed
    CANCELED = "CANCELED"                          # Payment canceled
    PARTIAL_CANCELED = "PARTIAL_CANCELED"          # Partially canceled
    ABORTED = "ABORTED"                            # Payment aborted
    EXPIRED = "EXPIRED"                            # Payment expired
```

#### Usage

```python
from tosspayments_server_sdk.models.enums import PaymentStatus

# Check specific status
if payment.status == PaymentStatus.DONE:
    print("Payment completed")

# Status-based logic
match payment.status:
    case PaymentStatus.DONE:
        process_completed_payment(payment)
    case PaymentStatus.CANCELED:
        handle_canceled_payment(payment)
    case PaymentStatus.WAITING_FOR_DEPOSIT:
        wait_for_deposit(payment)
    case _:
        log_payment_status(payment.status.value)
```

### `PaymentMethod`

Available payment methods.

```python
class PaymentMethod(Enum):
    CARD = "카드"                                    # Card
    VIRTUAL_ACCOUNT = "가상계좌"                       # Virtual account
    SIMPLE_PAYMENT = "간편결제"                        # Simple payment
    MOBILE_PHONE = "휴대폰"                           # Mobile phone
    ACCOUNT_TRANSFER = "계좌이체"                      # Account transfer
    CULTURE_GIFT_CERTIFICATE = "문화상품권"            # Culture gift certificate
    BOOK_CULTURE_GIFT_CERTIFICATE = "도서문화상품권"    # Book culture gift certificate
    GAME_CULTURE_GIFT_CERTIFICATE = "게임문화상품권"    # Game culture gift certificate
```

### `PaymentType`

Payment type enumeration.

```python
class PaymentType(Enum):
    NORMAL = "NORMAL"      # Normal payment
    BILLING = "BILLING"    # Billing payment
    BRANDPAY = "BRANDPAY"  # Brand pay
```

#### Usage

```python
from tosspayments_server_sdk.models.enums import PaymentType

# Check payment type
if payment.type == PaymentType.NORMAL:
    print("Standard one-time payment")
elif payment.type == PaymentType.BILLING:
    print("Recurring/subscription payment")
```


## Related Documentation

- [Client](client.md) - Main client class
- [PaymentResource](payments.md) - Payment operations
- [WebhookResource](webhooks.md) - Webhook handling
- [Getting Started](../getting-started/quickstart.md) - Quickstart guide with error handling