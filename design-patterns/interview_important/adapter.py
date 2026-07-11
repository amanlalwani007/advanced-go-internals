"""
** Adapter Pattern (Interview Important)
When to use: When you need to make incompatible interfaces work together without modifying their source code. Use when integrating third-party libraries, legacy systems, or multiple APIs with different interfaces.

Real-world examples:
- Django ORM adapters for multiple database backends (PostgreSQL, MySQL, SQLite)
- Payment gateway integrations (PayPal, Stripe, Razorpay, Square)
- Cloud provider SDK wrappers (AWS, GCP, Azure)
- ORM session adapters in SQLAlchemy
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class PaymentResult:
    transaction_id: str
    status: str
    amount: float
    currency: str
    timestamp: datetime
    error_message: Optional[str] = None


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float, currency: str, source: str) -> PaymentResult:
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: Optional[float] = None) -> PaymentResult:
        pass

    @abstractmethod
    def get_status(self, transaction_id: str) -> str:
        pass


class StripePayment:
    def create_payment_intent(self, amount_cents: int, currency: str, payment_method: str) -> dict:
        txn_id = f"pi_{uuid.uuid4().hex[:24]}"
        return {
            "id": txn_id,
            "amount": amount_cents,
            "currency": currency,
            "status": "succeeded",
            "payment_method": payment_method,
        }

    def refund_payment(self, payment_intent_id: str, amount_cents: Optional[int] = None) -> dict:
        return {
            "id": f"rf_{uuid.uuid4().hex[:24]}",
            "payment_intent": payment_intent_id,
            "status": "succeeded",
            "amount": amount_cents or 0,
        }

    def retrieve_payment(self, payment_intent_id: str) -> dict:
        return {"id": payment_intent_id, "status": "succeeded"}


class PayPalPayment:
    def execute_payment(self, total: str, currency: str, card_token: str) -> dict:
        txn_id = f"PAY-{uuid.uuid4().hex[:16].upper()}"
        return {
            "transaction_id": txn_id,
            "state": "completed",
            "total": total,
            "currency": currency,
        }

    def issue_refund(self, sale_id: str, refund_amount: Optional[str] = None) -> dict:
        return {
            "refund_id": f"REF-{uuid.uuid4().hex[:12].upper()}",
            "sale_id": sale_id,
            "state": "completed",
            "total": refund_amount or "0.00",
        }

    def lookup_transaction(self, transaction_id: str) -> dict:
        return {"transaction_id": transaction_id, "state": "completed"}


class RazorpayPayment:
    def create_order(self, amount_paise: int, currency: str, payment_source: str) -> dict:
        order_id = f"order_{uuid.uuid4().hex[:20]}"
        return {
            "order_id": order_id,
            "amount": amount_paise,
            "currency": currency,
            "status": "created",
            "source": payment_source,
        }

    def capture_payment(self, order_id: str, amount_paise: Optional[int] = None) -> dict:
        return {
            "payment_id": f"pay_{uuid.uuid4().hex[:20]}",
            "order_id": order_id,
            "status": "captured",
            "amount": amount_paise or 0,
        }

    def refund_payment(self, payment_id: str, amount_paise: Optional[int] = None) -> dict:
        return {
            "refund_id": f"rfnd_{uuid.uuid4().hex[:16]}",
            "payment_id": payment_id,
            "status": "processed",
            "amount": amount_paise or 0,
        }

    def fetch_payment(self, payment_id: str) -> dict:
        return {"payment_id": payment_id, "status": "captured"}


class StripeAdapter(PaymentGateway):
    def __init__(self, stripe: StripePayment):
        self._stripe = stripe

    def charge(self, amount: float, currency: str, source: str) -> PaymentResult:
        amount_cents = int(round(amount * 100))
        resp = self._stripe.create_payment_intent(amount_cents, currency, source)
        return PaymentResult(
            transaction_id=resp["id"],
            status=resp["status"],
            amount=amount,
            currency=currency,
            timestamp=datetime.now(),
        )

    def refund(self, transaction_id: str, amount: Optional[float] = None) -> PaymentResult:
        amount_cents = int(round(amount * 100)) if amount else None
        resp = self._stripe.refund_payment(transaction_id, amount_cents)
        return PaymentResult(
            transaction_id=resp["id"],
            status=resp["status"],
            amount=amount or 0.0,
            currency="USD",
            timestamp=datetime.now(),
        )

    def get_status(self, transaction_id: str) -> str:
        resp = self._stripe.retrieve_payment(transaction_id)
        return resp["status"]


class PayPalAdapter(PaymentGateway):
    def __init__(self, paypal: PayPalPayment):
        self._paypal = paypal

    def charge(self, amount: float, currency: str, source: str) -> PaymentResult:
        resp = self._paypal.execute_payment(str(amount), currency, source)
        return PaymentResult(
            transaction_id=resp["transaction_id"],
            status=resp["state"],
            amount=amount,
            currency=currency,
            timestamp=datetime.now(),
        )

    def refund(self, transaction_id: str, amount: Optional[float] = None) -> PaymentResult:
        refund_amount = str(amount) if amount else None
        resp = self._paypal.issue_refund(transaction_id, refund_amount)
        return PaymentResult(
            transaction_id=resp["refund_id"],
            status=resp["state"],
            amount=amount or 0.0,
            currency="USD",
            timestamp=datetime.now(),
        )

    def get_status(self, transaction_id: str) -> str:
        resp = self._paypal.lookup_transaction(transaction_id)
        return resp["state"]


class RazorpayAdapter(PaymentGateway):
    def __init__(self, razorpay: RazorpayPayment):
        self._razorpay = razorpay

    def charge(self, amount: float, currency: str, source: str) -> PaymentResult:
        amount_paise = int(round(amount * 100))
        order = self._razorpay.create_order(amount_paise, currency, source)
        payment = self._razorpay.capture_payment(order["order_id"], amount_paise)
        return PaymentResult(
            transaction_id=payment["payment_id"],
            status=payment["status"],
            amount=amount,
            currency=currency,
            timestamp=datetime.now(),
        )

    def refund(self, transaction_id: str, amount: Optional[float] = None) -> PaymentResult:
        amount_paise = int(round(amount * 100)) if amount else None
        resp = self._razorpay.refund_payment(transaction_id, amount_paise)
        return PaymentResult(
            transaction_id=resp["refund_id"],
            status=resp["status"],
            amount=amount or 0.0,
            currency="INR",
            timestamp=datetime.now(),
        )

    def get_status(self, transaction_id: str) -> str:
        resp = self._razorpay.fetch_payment(transaction_id)
        return resp["status"]


class PaymentRouter:
    def __init__(self):
        self._gateways: dict[str, PaymentGateway] = {}

    def register(self, name: str, gateway: PaymentGateway):
        self._gateways[name] = gateway

    def process_payment(self, gateway_name: str, amount: float, currency: str, source: str) -> PaymentResult:
        gateway = self._gateways.get(gateway_name)
        if not gateway:
            raise ValueError(f"Unknown gateway: {gateway_name}")
        print(f"[Router] Routing ${amount:.2f} {currency} through {gateway_name}...")
        return gateway.charge(amount, currency, source)

    def process_refund(self, gateway_name: str, transaction_id: str, amount: Optional[float] = None) -> PaymentResult:
        gateway = self._gateways.get(gateway_name)
        if not gateway:
            raise ValueError(f"Unknown gateway: {gateway_name}")
        print(f"[Router] Issuing refund via {gateway_name} for transaction {transaction_id}...")
        return gateway.refund(transaction_id, amount)


if __name__ == "__main__":
    router = PaymentRouter()
    router.register("stripe", StripeAdapter(StripePayment()))
    router.register("paypal", PayPalAdapter(PayPalPayment()))
    router.register("razorpay", RazorpayAdapter(RazorpayPayment()))

    results = []
    results.append(router.process_payment("stripe", 49.99, "USD", "tok_visa"))
    results.append(router.process_payment("paypal", 129.99, "USD", "card_12345"))
    results.append(router.process_payment("razorpay", 2499.00, "INR", "upi_98765"))

    for r in results:
        print(f"  {r.transaction_id}: {r.status} | ${r.amount:.2f} {r.currency} @ {r.timestamp}")

    refund = router.process_refund("stripe", results[0].transaction_id)
    print(f"  Refund: {refund.transaction_id}: {refund.status}")

    for name in ["stripe", "paypal", "razorpay"]:
        txn = results[0] if name != "razorpay" else results[2]
        status = router._gateways[name].get_status(txn.transaction_id)
        print(f"  {name} status: {status}")

