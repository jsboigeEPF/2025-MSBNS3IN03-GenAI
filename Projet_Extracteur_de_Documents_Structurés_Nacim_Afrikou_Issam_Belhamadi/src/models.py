"""Modèles Pydantic pour structurer les données extraites (commandes et factures).

Ces modèles servent de JSON Schema pour les Structured Outputs d'OpenAI
et de validation automatique via model_validate_json().
"""

from typing import List, Optional, Union

from pydantic import BaseModel, Field


# --- Sous-modèles partagés ---

class ProductLine(BaseModel):
    """Ligne de produit (commande)."""
    description: str = Field(description="Nom / description du produit")
    quantity: Optional[float] = Field(None, description="Quantité commandée")
    unit_price: Optional[float] = Field(None, description="Prix unitaire")
    line_total: Optional[float] = Field(None, description="Montant total de la ligne")


class ShippingDetails(BaseModel):
    """Détails de livraison."""
    ship_name: Optional[str] = None
    ship_address: Optional[str] = None
    ship_city: Optional[str] = None
    ship_region: Optional[str] = None
    ship_postal_code: Optional[str] = None
    ship_country: Optional[str] = None


class Address(BaseModel):
    """Adresse postale (vendeur / acheteur)."""
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


class InvoiceLine(BaseModel):
    """Ligne d'article (facture)."""
    description: str = Field(description="Description de l'article")
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    tax_rate: Optional[float] = None
    line_total: Optional[float] = None


# --- Modèle Commande ---

class Order(BaseModel):
    """Commande (purchase order) extraite d'un PDF."""
    source_file: str = ""
    document_type: str = "order"

    order_id: Optional[str] = None
    order_date: Optional[str] = Field(None, description="Date de commande (YYYY-MM-DD)")
    shipped_date: Optional[str] = Field(None, description="Date d'expédition (YYYY-MM-DD)")

    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    employee_name: Optional[str] = None

    shipper_id: Optional[str] = None
    shipper_name: Optional[str] = None
    shipping: Optional[ShippingDetails] = None

    products: List[ProductLine] = Field(default_factory=list)
    total_price: Optional[float] = None
    currency: Optional[str] = None


# --- Modèle Facture ---

class Invoice(BaseModel):
    """Facture extraite d'un PDF."""
    source_file: str = ""
    document_type: str = "invoice"

    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = Field(None, description="Date d'émission (YYYY-MM-DD)")
    due_date: Optional[str] = Field(None, description="Date d'échéance (YYYY-MM-DD)")

    seller: Optional[Address] = None
    seller_tax_id: Optional[str] = None
    buyer: Optional[Address] = None
    buyer_tax_id: Optional[str] = None

    items: List[InvoiceLine] = Field(default_factory=list)

    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = None
    payment_terms: Optional[str] = None


# Type union : résultat d'extraction (Order ou Invoice)
ExtractedDocument = Union[Order, Invoice]

