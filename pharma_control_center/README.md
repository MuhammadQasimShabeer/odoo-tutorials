# Pharma Control Center (Odoo 18+)

Pharma Control Center is an Odoo backend module for basic pharmacy operations: a medicine catalog (batch/expiry/custom stock), a per-user cart checkout flow (Sales Order + Invoice), an operational dashboard, and simple patient records with doctor assignment.

This module is implemented as standard Odoo models + backend views (no website/portal pages).

## What’s Included (As Implemented)

- **Medicines** (`pharmacy.medicine`)
  - Batch + expiry tracking (`expiry_date`, `days_to_expiry`, `expiry_status`)
  - Custom stock quantity + reorder indicator (`quantity`, `reorder_level`, `need_reorder`)
  - License category field (`green` / `blue` / `white`) used in medicine visibility record rules
  - Kanban / list / form views + search filters

- **Cart & checkout** (`pharmacy.cart`, `pharmacy.cart.line`)
  - Add medicines to your cart (including quick add by barcode)
  - Shows interaction warnings for medicines currently in the cart
  - Checkout creates and confirms a `sale.order`, creates an invoice (`account.move`), posts it, reduces `pharmacy.medicine.quantity`, and clears the cart

- **Dashboard** (`pharma.control.center`)
  - Profile panel (avatar stored on the dashboard; name/email/phone synced to the linked `res.users` / `res.partner`)
  - Live KPIs (medicine counts, stock value, expiring soon, etc.)
  - “Today’s orders” summary + drill-down list

- **Patients** (`pharmacy.patient`)
  - Doctors can manage patients assigned to them (record rule on `doctor_id`)
  - Managers can see all patients

- **Drug interactions** (`pharmacy.interaction`)
  - Managers define medicine pairs with severity + warning text
  - Cart shows warnings; checkout blocks when any interaction is **Severe**

- **Manager analytics**
  - Graph/pivot views on `sale.order` under the **Analytics** menu (manager-only)

## Dependencies

Declared in [`__manifest__.py`](__manifest__.py): `base_setup`, `product`, `sale`, `account`.

## Installation

1. Put `pharma_control_center/` in one of your Odoo `addons_path` directories.
2. Restart Odoo, then go to **Apps** and click **Update Apps List**.
3. Search for **Pharma Control Center** and install it.

## Configuration (Roles)

Assign users to one of these groups:
- **Pharma Control Center / Patient**
- **Pharma Control Center / Doctor**
- **Pharma Control Center / Manager**

## Demo Data

When demo data is enabled, the module loads:
- Sample medicines in [`data/demo_medicines.xml`](data/demo_medicines.xml)
- Sample patients in [`data/demo_patients.xml`](data/demo_patients.xml)

## Notes / Limitations

- Inventory is tracked on `pharmacy.medicine.quantity` (this module does **not** use Odoo’s Inventory/Stock app and does not generate stock moves).
- Checkout posts the invoice automatically; this requires your Odoo Accounting configuration to be set up (journals, accounts, etc.).

## Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [TECHNICAL_DETAILS.md](docs/TECHNICAL_DETAILS.md)
- [SECURITY.md](docs/SECURITY.md)
- [USER_GUIDE.md](docs/USER_GUIDE.md)
- [DEMO_DATA.md](docs/DEMO_DATA.md)
- [CHANGELOG.md](docs/CHANGELOG.md)
- [TESTING.md](TESTING.md)

## License

LGPL-3 (see `license` in the manifest).
