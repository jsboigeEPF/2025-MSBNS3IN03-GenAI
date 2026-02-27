## Schéma JSON – Projet NAF_ISB (commandes & factures)

Le projet détecte automatiquement le type de document (commande ou facture) et produit un JSON adapté.

---

### 1. Commande (Order)

Modèle Pydantic : `Order` dans `src/models.py`.

#### Champs principaux

| Champ | Type | Description |
|-------|------|-------------|
| `source_file` | string | Chemin du fichier PDF source |
| `document_type` | string | `"order"` |
| `order_id` | string \| null | Identifiant de la commande |
| `order_date` | string \| null | Date de commande (ISO `YYYY-MM-DD`) |
| `shipped_date` | string \| null | Date d'expédition (ISO `YYYY-MM-DD`) |
| `customer_id` | string \| null | Identifiant du client |
| `customer_name` | string \| null | Nom du client |
| `employee_name` | string \| null | Nom de l'employé |
| `shipper_id` | string \| null | Identifiant du transporteur |
| `shipper_name` | string \| null | Nom du transporteur |
| `shipping` | object \| null | Détails de livraison (voir ci-dessous) |
| `products` | array | Liste des produits (voir ci-dessous) |
| `total_price` | number \| null | Prix total de la commande |
| `currency` | string \| null | Devise (`"EUR"`, `"USD"`, etc.) |

#### Objet `shipping`

| Champ | Type | Description |
|-------|------|-------------|
| `ship_name` | string \| null | Nom du destinataire |
| `ship_address` | string \| null | Adresse de livraison |
| `ship_city` | string \| null | Ville |
| `ship_region` | string \| null | Région |
| `ship_postal_code` | string \| null | Code postal |
| `ship_country` | string \| null | Pays |

#### Objet `product` (élément de `products`)

| Champ | Type | Description |
|-------|------|-------------|
| `description` | string | Nom du produit |
| `quantity` | number \| null | Quantité |
| `unit_price` | number \| null | Prix unitaire |
| `line_total` | number \| null | Montant total de la ligne |

#### Exemple JSON (Order)

```json
{
  "source_file": "data/input/order_10999.pdf",
  "document_type": "order",
  "order_id": "10999",
  "order_date": "2018-04-03",
  "shipped_date": "2018-04-10",
  "customer_id": "OTTIK",
  "customer_name": "Ottilies Käseladen",
  "employee_name": "Michael Suyama",
  "shipper_id": "2",
  "shipper_name": "United Package",
  "shipping": {
    "ship_name": "Ottilies Käseladen",
    "ship_address": "Mehrheimerstr. 369",
    "ship_city": "Köln",
    "ship_region": "Western Europe",
    "ship_postal_code": "50739",
    "ship_country": "Germany"
  },
  "products": [
    {
      "description": "Jack's New England Clam Chowder",
      "quantity": 20,
      "unit_price": 9.65,
      "line_total": 193.0
    }
  ],
  "total_price": 1261.0,
  "currency": null
}
```

---

### 2. Facture (Invoice)

Modèle Pydantic : `Invoice` dans `src/models.py`.

#### Champs principaux

| Champ | Type | Description |
|-------|------|-------------|
| `source_file` | string | Chemin du fichier PDF source |
| `document_type` | string | `"invoice"` |
| `invoice_number` | string \| null | Numéro de facture |
| `invoice_date` | string \| null | Date d'émission (ISO `YYYY-MM-DD`) |
| `due_date` | string \| null | Date d'échéance (ISO `YYYY-MM-DD`) |
| `seller` | object \| null | Informations vendeur (voir `address`) |
| `seller_tax_id` | string \| null | N° fiscal / SIRET du vendeur |
| `buyer` | object \| null | Informations acheteur (voir `address`) |
| `buyer_tax_id` | string \| null | N° fiscal / SIRET de l'acheteur |
| `items` | array | Lignes de la facture (voir ci-dessous) |
| `subtotal` | number \| null | Sous-total HT |
| `tax_amount` | number \| null | Montant TVA |
| `total` | number \| null | Total TTC |
| `currency` | string \| null | Devise (`"EUR"`, `"USD"`, etc.) |
| `payment_terms` | string \| null | Conditions de paiement |

#### Objet `address` (seller / buyer)

| Champ | Type | Description |
|-------|------|-------------|
| `name` | string \| null | Nom ou raison sociale |
| `address` | string \| null | Rue / numéro |
| `city` | string \| null | Ville |
| `postal_code` | string \| null | Code postal |
| `country` | string \| null | Pays |

#### Objet `item` (élément de `items`)

| Champ | Type | Description |
|-------|------|-------------|
| `description` | string | Description de l'article |
| `quantity` | number \| null | Quantité |
| `unit_price` | number \| null | Prix unitaire HT |
| `tax_rate` | number \| null | Taux de TVA (%) |
| `line_total` | number \| null | Montant total de la ligne HT |

#### Exemple JSON (Invoice)

```json
{
  "source_file": "data/input/facture_001.pdf",
  "document_type": "invoice",
  "invoice_number": "FAC-2024-001",
  "invoice_date": "2024-03-15",
  "due_date": "2024-04-15",
  "seller": {
    "name": "Entreprise ABC",
    "address": "12 rue de la Paix",
    "city": "Paris",
    "postal_code": "75002",
    "country": "France"
  },
  "seller_tax_id": "FR12345678901",
  "buyer": {
    "name": "Client XYZ",
    "address": "5 avenue des Champs",
    "city": "Lyon",
    "postal_code": "69001",
    "country": "France"
  },
  "buyer_tax_id": null,
  "items": [
    {
      "description": "Prestation de conseil",
      "quantity": 10,
      "unit_price": 150.0,
      "tax_rate": 20.0,
      "line_total": 1500.0
    }
  ],
  "subtotal": 1500.0,
  "tax_amount": 300.0,
  "total": 1800.0,
  "currency": "EUR",
  "payment_terms": "30 jours net"
}
```

