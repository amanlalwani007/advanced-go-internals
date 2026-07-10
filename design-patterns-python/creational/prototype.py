"""
Prototype Pattern
When to use:
- When creating a new instance is expensive (e.g., requires DB calls or complex computation)
- When you want to avoid subclassing and instead clone and customize existing objects
- When your system should be independent of how its products are created

Real-world examples:
- Django: model_instance.pk = None; model_instance.save() to duplicate a row
- Spreadsheets: copying cells preserves all formatting, formulas, and data
- Python's copy.copy() and copy.deepcopy() implement the Prototype pattern
- Celery: task.clone() to create new task instances with modified parameters
"""

from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
from typing import Optional


class Document(ABC):
    """Prototype interface — defines clone methods."""

    @abstractmethod
    def clone(self, deep: bool = True) -> Document:
        ...

    @abstractmethod
    def render(self) -> str:
        ...


class Address:
    def __init__(
        self, street: str, city: str, state: str, zip_code: str, country: str
    ) -> None:
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

    def __repr__(self) -> str:
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}, {self.country}"


class LineItem:
    def __init__(self, description: str, quantity: int, unit_price: float) -> None:
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price

    def __repr__(self) -> str:
        return f"  {self.description:<30} x{self.quantity:<4}  ${self.unit_price:<8.2f}  ${self.total:.2f}"


class Invoice(Document):
    def __init__(
        self,
        invoice_number: str,
        issuer_name: str,
        issuer_address: Address,
        client_name: str,
        client_address: Address,
        line_items: Optional[list[LineItem]] = None,
        issue_date: Optional[date] = None,
        due_date: Optional[date] = None,
        notes: Optional[str] = None,
    ) -> None:
        self.invoice_number = invoice_number
        self.issuer_name = issuer_name
        self.issuer_address = issuer_address
        self.client_name = client_name
        self.client_address = client_address
        self.line_items = line_items or []
        self.issue_date = issue_date or date.today()
        self.due_date = due_date or date.today() + timedelta(days=30)
        self.notes = notes

    def clone(self, deep: bool = True) -> Invoice:
        if deep:
            return copy.deepcopy(self)
        return copy.copy(self)

    @property
    def subtotal(self) -> float:
        return sum(item.total for item in self.line_items)

    def render(self) -> str:
        tax = self.subtotal * 0.08
        total = self.subtotal + tax
        sep = "=" * 60
        dash = "-" * 60
        lines = [
            f"  {sep}",
            f"  INVOICE #{self.invoice_number}",
            f"  {sep}",
            f"  From: {self.issuer_name}",
            f"        {self.issuer_address}",
            f"  To:   {self.client_name}",
            f"        {self.client_address}",
            f"  Issue: {self.issue_date}   Due: {self.due_date}",
            f"  {dash}",
            f"  Items:",
        ]
        for item in self.line_items:
            lines.append(f"    {item}")
        lines.append(f"  {dash}")
        lines.append(f"  {'Subtotal':<50} ${self.subtotal:>8.2f}")
        lines.append(f"  {'Tax (8%)':<50} ${tax:>8.2f}")
        lines.append(f"  {'TOTAL':<50} ${total:>8.2f}")
        if self.notes:
            lines.append(f"  Notes: {self.notes}")
        lines.append(f"  {sep}")
        return "\n".join(lines)


class Report(Document):
    def __init__(
        self,
        title: str,
        author: str,
        sections: Optional[list[tuple[str, str]]] = None,
        generated_at: Optional[datetime] = None,
        footer_text: Optional[str] = None,
    ) -> None:
        self.title = title
        self.author = author
        self.sections = sections or []
        self.generated_at = generated_at or datetime.now()
        self.footer_text = footer_text

    def clone(self, deep: bool = True) -> Report:
        if deep:
            return copy.deepcopy(self)
        return copy.copy(self)

    def render(self) -> str:
        sep = "=" * 60
        dash = "-" * 60
        lines = [
            f"  {sep}",
            f"  REPORT: {self.title}",
            f"  Author: {self.author}",
            f"  Generated: {self.generated_at:%Y-%m-%d %H:%M:%S}",
            f"  {sep}",
        ]
        for heading, body in self.sections:
            lines.append(f"\n  > {heading}")
            lines.append(f"  {dash}")
            lines.append(f"    {body}")
        if self.footer_text:
            lines.append(f"\n  {dash}")
            lines.append(f"  {self.footer_text}")
        return "\n".join(lines)


class Contract(Document):
    def __init__(
        self,
        contract_id: str,
        party_a: str,
        party_b: str,
        effective_date: date,
        terms: Optional[list[str]] = None,
        jurisdiction: str = "New York",
        signature_a: Optional[str] = None,
        signature_b: Optional[str] = None,
    ) -> None:
        self.contract_id = contract_id
        self.party_a = party_a
        self.party_b = party_b
        self.effective_date = effective_date
        self.terms = terms or []
        self.jurisdiction = jurisdiction
        self.signature_a = signature_a
        self.signature_b = signature_b

    def clone(self, deep: bool = True) -> Contract:
        if deep:
            return copy.deepcopy(self)
        return copy.copy(self)

    def render(self) -> str:
        sep = "=" * 60
        dash = "-" * 60
        lines = [
            f"  {sep}",
            f"  CONTRACT #{self.contract_id}",
            f"  {sep}",
            f"  Between: {self.party_a}",
            f"  And:     {self.party_b}",
            f"  Effective: {self.effective_date}",
            f"  Jurisdiction: {self.jurisdiction}",
            f"  {dash}",
            f"  Terms & Conditions:",
        ]
        for i, term in enumerate(self.terms, 1):
            lines.append(f"    {i}. {term}")
        lines.append(f"  {dash}")
        if self.signature_a:
            lines.append(f"  Signed by {self.party_a}: {self.signature_a}")
        if self.signature_b:
            lines.append(f"  Signed by {self.party_b}: {self.signature_b}")
        if not self.signature_a or not self.signature_b:
            lines.append(f"  [Status: Pending signatures]")
        lines.append(f"  {sep}")
        return "\n".join(lines)


class DocumentTemplateRegistry:
    """Registry that stores prototype instances for cloning."""

    def __init__(self) -> None:
        self._prototypes: dict[str, Document] = {}

    def register(self, name: str, prototype: Document) -> None:
        self._prototypes[name] = prototype

    def create_document(self, name: str, **overrides) -> Document:
        prototype = self._prototypes.get(name)
        if prototype is None:
            raise KeyError(f"No prototype registered for '{name}'")
        doc = prototype.clone(deep=True)
        for key, value in overrides.items():
            setattr(doc, key, value)
        return doc


if __name__ == "__main__":
    registry = DocumentTemplateRegistry()

    invoice_template = Invoice(
        invoice_number="TEMPLATE",
        issuer_name="Acme Corp",
        issuer_address=Address("123 Main St", "Springfield", "IL", "62701", "USA"),
        client_name="[CLIENT NAME]",
        client_address=Address("[STREET]", "[CITY]", "[STATE]", "[ZIP]", "USA"),
        line_items=[
            LineItem("Consulting Services", 10, 150.00),
            LineItem("Software License", 1, 2999.00),
        ],
        notes="Payment via wire transfer within 30 days.",
    )

    report_template = Report(
        title="[REPORT TITLE]",
        author="[AUTHOR]",
        sections=[
            ("Executive Summary", "[Summary text here]"),
            ("Methodology", "[Methodology description]"),
            ("Findings", "[Key findings and data]"),
            ("Recommendations", "[Action items]"),
        ],
        footer_text="CONFIDENTIAL - For internal use only.",
    )

    contract_template = Contract(
        contract_id="TMPL-001",
        party_a="[PARTY A]",
        party_b="[PARTY B]",
        effective_date=date.today(),
        terms=[
            "Scope of Work: [describe services]",
            "Payment Terms: Net 30 upon invoice",
            "Confidentiality: Both parties agree to non-disclosure",
            "Termination: 30 days written notice by either party",
            "Limitation of Liability: [cap amount]",
        ],
    )

    registry.register("invoice", invoice_template)
    registry.register("report", report_template)
    registry.register("contract", contract_template)

    print("\nCloning Invoice for Client XYZ:")
    inv = registry.create_document(
        "invoice",
        invoice_number="INV-2024-0421",
        client_name="XYZ Corp",
        client_address=Address("456 Oak Ave", "Metropolis", "NY", "10001", "USA"),
        line_items=[
            LineItem("Q1 Consulting (120h)", 120, 175.00),
            LineItem("Enterprise License (12mo)", 1, 12000.00),
            LineItem("Onboarding & Training", 1, 2500.00),
        ],
    )
    print(inv.render())

    print("\n\nCloning Monthly Report:")
    rpt = registry.create_document(
        "report",
        title="Q4 2024 Performance Review",
        author="Jane Doe",
        sections=[
            ("Executive Summary", "Revenue grew 23% YoY driven by enterprise segment."),
            ("Methodology", "Data aggregated from CRM, ERP, and support platforms."),
            ("Findings", "Customer retention hit 94%. Top 10 accounts grew 31%."),
            ("Recommendations", "Expand enterprise sales team by 5 FTE in Q1."),
        ],
    )
    print(rpt.render())

    print("\n\nCloning Contract for New Partnership:")
    ctr = registry.create_document(
        "contract",
        contract_id="CTR-2024-089",
        party_a="Acme Corp",
        party_b="DataStream Inc.",
        terms=[
            "Scope: DataStream provides real-time analytics API access",
            "Payment: $5,000/mo, billed quarterly",
            "SLA: 99.9% uptime guarantee",
            "Data retention: 90 days after termination",
            "Non-compete: 12 months, limited to analytics sector",
        ],
        signature_a="John Smith",
    )
    print(ctr.render())
