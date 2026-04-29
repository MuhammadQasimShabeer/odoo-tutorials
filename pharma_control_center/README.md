# 💊 Pharma Control Center (Odoo 18+ Module)

## Overview
**Pharma Control Center** is a comprehensive Odoo 18+ module for modern pharmacy management. It provides complete functionality for medicine cataloguing, batch/expiry tracking, stock management, patient records management, doctor-patient assignments, invoicing, and real-time clinical dashboards. The module follows Odoo 18 best practices (`<list>` instead of deprecated `<tree>`, emoji-rich UI, computed fields, and modern QWeb templates) and seamlessly integrates with Odoo's accounting, sales, and product modules for complete pharmacy operations.

---

## ✨ Features

### 🏥 Complete Medicine Management
- **Full Medicine Catalogue** – name, batch number, manufacturer, barcode, category, sub-category
- **Pricing Management** – selling price, cost price, automatic profit margin calculation
- **Stock Control** – tracked quantity, reorder level, "Need Reorder" alerts
- **Expiry Tracking** – automatic days-to-expiry calculation and status (Fresh / Expiring Soon / Expired)
- **Storage Conditions** – room temperature, cold storage, frozen storage
- **License Categorization** – medicines marked with Pharmacy Category (Green / Blue / White) for role-based access control
- **Dosage & Safety** – dosage instructions and side effects documentation

### 👥 Advanced Patient Management
- **Dedicated Patient Model** – comprehensive patient records with personal info, medical history, allergies, blood group
- **Doctor Assignment** – each patient assigned to a specific doctor (user in Doctor group)
- **Role-Based Visibility** – doctors see only their own patients; managers see all patients; patients cannot access patient list
- **Medical Records** – medical history, allergies, blood group, contact information
- **Doctor-Patient Relationship** – secure patient-to-doctor assignment with edit permissions

### 🛒 Order Management & Invoicing (Full Integration)
- **"Order Now" Button** – available on each medicine (form and kanban views)
- **Automatic Sale Order Creation** – creates an Odoo Sale Order with the medicine as line item
- **Automatic Invoice Generation** – automatically creates and posts an invoice upon ordering
- **Order Menu** – dedicated "Orders" menu lists all sale orders created via the module (visible to managers and doctors, read-only for doctors)
- **Order Restrictions** – record rules restrict order editing to managers only; doctors/patients have read-only access
- **Order Status Tracking** – after ordering, the button changes to "✅ Ordered" and the medicine cannot be re-ordered
- **Product Linking** – automatically creates linked products in Odoo's product module
- **Invoice Tracking** – tracks last sale order and invoice for each medicine

### 📊 Comprehensive Dashboard
- **Medicine Statistics** – total medicines, total stock quantity, stock value (quantity × price), out-of-stock count, low stock count (1-9 units), expiring soon count (≤30 days), expired count
- **Patient Statistics** – total patients, my patients (for doctors), dynamic patient list
- **Dynamic Patient List** – displayed directly on the dashboard, filtered by user role
  - Doctors see only their assigned patients (read-only)
  - Managers see all patients (read-only)
  - Patients see nothing
- **Real-Time Updates** – statistics update automatically based on current inventory
- **Visual Alerts** – color-coded badges for low stock, expiring soon, and expired medicines

### 🔐 Role-Based Access Control (Complete)
Three user groups with distinct permissions:

#### 🟢 **Pharmacy Manager Group**
- **Full Access** to all medicines (all license categories)
- **Full CRUD** on patients
- **Full CRUD** on categories and configuration
- **Can Place Orders** – "Order Now" button visible and functional
- **Can Edit Orders** – full read/write access to all sale orders
- **Can View Dashboard** – see all statistics and all patients
- **Menu Access** – Dashboard, Medicines, Patients, Orders, Categories (Configuration)

#### 🔵 **Doctor Group**
- **Read-Only Access** to Blue (Limited License) and White (OTC) medicines only
- **Read & Write Own Patients** – can manage patients they are assigned to
- **Cannot Create/Edit Medicines** – read-only access only
- **Cannot Place Orders** – "Order Now" button hidden (UI + security check)
- **Can View Orders** – read-only access to all orders (record rule restricted)
- **Can View Dashboard** – see statistics and their own patients only
- **Menu Access** – Dashboard, Medicines, Patients, Orders (read-only)

#### ⚪ **Patient Group**
- **Read-Only Access** to White (Basic OTC) medicines only
- **No Patient List Access** – cannot see patient records or list
- **No Dashboard Access** – dashboard menu hidden
- **No Ordering Capability** – "Order Now" button hidden
- **Menu Access** – Medicines (white licenses only)

### 🔒 Security Layer Details

**Medicine Visibility (Record Rules):**
- Patients see ONLY `license_category = 'white'` medicines
- Doctors see `license_category in ['blue', 'white']` medicines
- Managers see ALL medicines (no restrictions)

**Patient Visibility (Record Rules):**
- Patients cannot view any patient records (CSV: no read access)
- Doctors can read/write/create patients assigned to them: `[('doctor_id','=',user.id)]`
- Doctors cannot delete patients (unlink=False)
- Managers have full CRUD on all patients

**Sale Order Visibility (Record Rules):**
- Global rule: all sale orders are read-only by default
- Manager override: managers have full read/write/create/delete on sale orders
- Doctors/Patients have read-only access via global rule

**Category Visibility:**
- Patients cannot view categories (CSV: no read access)
- Doctors can view categories (read-only)
- Managers have full CRUD on categories

### 🎨 Modern User Interface
- **List View** – replaces deprecated `<tree>`, multi-edit support for batch operations
- **Form View** – intuitive grouped layouts with emojis, placeholders, and badges
- **Kanban View** – card-based design with license/expiry badges, stock status, and "Order Now" button
- **Search View** – advanced filters for:
  - Stock status (In Stock, Out of Stock, Need Reorder)
  - Expiry status (Expired, Expiring Soon)
  - License category filters
  - Medicine name, batch, manufacturer search
  - Group-by options (Category, Expiry Status, Storage, License)
- **Dashboard Form** – statistics display with visual widgets and alerts
- **Emoji Rich** – 💊 🏥 📊 💰 🔒 for enhanced visual recognition

### 📦 Additional Models & Data Structures

**pharmacy.category** – Hierarchical Medicine Categories
- Parent-child relationships for taxonomy (e.g., Antibiotics → Penicillin)
- Translatable names and descriptions
- Manager-only access

**pharmacy.patient** – Patient Records
- Linked to doctors via `doctor_id` (Many2one res.users)
- Medical information (history, allergies, blood group)
- Contact details (phone, email, address)
- Active/inactive status

---

## 🧱 Module Structure
```
odoo-tutorials/
└── pharma_control_center/
    ├── __init__.py                          # Module initialization
    ├── __manifest__.py                      # Module manifest & settings
    ├── README.md                            # This file
    │
    ├── data/
    │   ├── demo_medicines.xml               # Demo medicine records (various categories & licenses)
    │   └── demo_patients.xml                # Demo doctor & patient records
    │
    ├── models/
    │   ├── __init__.py                      # Model imports
    │   ├── pharma_control_center.py         # Dashboard model (statistics & patient list)
    │   ├── pharma_medicine.py               # Medicine model (CRUD, ordering, invoicing)
    │   ├── pharmacy_category.py             # Medicine category model (hierarchical)
    │   └── pharmacy_patient.py              # Patient model (doctor assignment, records)
    │
    ├── security/
    │   ├── groups.xml                       # User groups (Patient, Doctor, Manager)
    │   ├── ir.model.access.csv              # Model-level access permissions
    │   ├── pharmacy_security.xml            # Record rules for medicines (license-based)
    │   ├── pharmacy_patient_security.xml    # Record rules for patients (doctor assignment)
    │   └── sale_order_security.xml          # Record rules for sale orders (manager access)
    │
    ├── views/
    │   ├── pharma_control_center_views.xml  # Dashboard views & root menu
    │   ├── pharmacy_medicine_views.xml      # Medicine list/form/kanban/search & menu
    │   ├── pharmacy_patient_views.xml       # Patient list/form/search & menu
    │   ├── pharmacy_category_views.xml      # Category views & menu
    │   └── pharmacy_order_views.xml         # Sale order lists & Orders menu
    │
    └── test/
        └── test_pharma_control_center.py    # Unit tests for core functionality
```

---

## 🔧 Technical Details

### Model: `pharmacy.medicine`

| Field | Type | Description | Required | Notes |
|-------|------|-------------|----------|-------|
| `name` | Char | Medicine name | ✓ | Max 255 chars |
| `description` | Text | Short description | - | Optional |
| `manufacturer` | Char | Manufacturer name | - | Optional |
| `barcode` | Char | Product barcode (EAN/UPC) | - | Optional, for scanning |
| `category_id` | Many2one | Link to `pharmacy.category` | ✓ | Prevents deletion of category if medicines exist |
| `sub_category` | Char | Optional sub-category | - | Text field (not entity-linked) |
| `license_category` | Selection | `green` / `blue` / `white` | ✓ | Controls visibility & access |
| `batch_number` | Char | Batch/Lot number | ✓ | Required for traceability |
| `expiry_date` | Date | Expiry/Expiration date | ✓ | Used for expiry calculations |
| `price` | Float | Selling price per unit | ✓ | Required for invoicing |
| `cost_price` | Float | Purchase/cost price | - | Optional, used for margin calculation |
| `profit_margin` | Float | Profit margin % | - | Computed: `((price - cost_price) / cost_price) * 100` |
| `quantity` | Integer | Stock quantity | ✓ | Default: 0, tracked for inventory |
| `reorder_level` | Integer | Reorder threshold | - | Default: 10, triggers "Need Reorder" alert |
| `need_reorder` | Boolean | Computed low stock flag | - | Computed: `quantity <= reorder_level` |
| `in_stock` | Boolean | Computed stock status | - | Computed: `quantity > 0` |
| `days_to_expiry` | Integer | Days remaining until expiry | - | Computed: `(expiry_date - today).days` |
| `expiry_status` | Selection | Status badge | - | Computed: `fresh` / `expiring_soon` / `expired` |
| `storage_location` | Selection | Storage condition | ✓ | `room_temp` / `cold` / `frozen` |
| `dosage` | Char | Usage instructions | - | Optional, e.g., "1 tablet twice daily" |
| `side_effects` | Text | Possible side effects | - | Optional, medical notes |
| `product_id` | Many2one | Linked `product.product` | - | Auto-created on first order, read-only |
| `is_ordered` | Boolean | Order status flag | - | True after "Order Now" clicked, prevents re-ordering |
| `last_sale_order_id` | Many2one | Last `sale.order` created | - | Read-only, for tracking |
| `last_invoice_id` | Many2one | Last `account.move` created | - | Read-only, for tracking |

**Computed Fields (Auto-updated):**
- `profit_margin` – Depends on `price`, `cost_price`
- `need_reorder` – Depends on `quantity`, `reorder_level`
- `in_stock` – Depends on `quantity`
- `days_to_expiry` – Depends on `expiry_date` (daily refresh)
- `expiry_status` – Depends on `expiry_date` (daily refresh)

### Model: `pharma.control.center` (Dashboard)

| Field | Type | Description | Computed | Notes |
|-------|------|-------------|----------|-------|
| `name` | Char | Dashboard name | - | Default: "Pharmacy Dashboard", required |
| `description` | Text | Dashboard description | - | Optional |
| `last_updated` | Datetime | Last update timestamp | - | Auto-set on creation |
| `total_medicines` | Integer | Count of all medicines | ✓ | `COUNT(pharmacy.medicine)` |
| `total_stock_quantity` | Integer | Sum of all quantities | ✓ | `SUM(quantity)` across all medicines |
| `stock_value` | Float | Inventory value (₹) | ✓ | `SUM(quantity × price)` |
| `out_of_stock_count` | Integer | Medicines with qty = 0 | ✓ | Count where `quantity == 0` |
| `low_stock_count` | Integer | Medicines with 1-9 units | ✓ | Count where `0 < quantity < 10` |
| `expiring_soon_count` | Integer | Medicines expiring ≤30 days | ✓ | Count where `today < expiry_date <= today + 30 days` |
| `expired_count` | Integer | Medicines past expiry | ✓ | Count where `expiry_date < today` |
| `total_patients` | Integer | Total patient records | ✓ | `COUNT(pharmacy.patient)` |
| `my_patients` | Integer | Doctor's assigned patients | ✓ | Count for doctors only, `COUNT(pharmacy.patient where doctor_id=user)` |
| `patient_ids` | One2many | Patient records list | ✓ | Role-filtered (doctors: own patients; managers: all; patients: none) |

**Computed Fields (Live Updates):**
- All numeric fields recompute on each dashboard access
- `patient_ids` filters based on current user's role

### Model: `pharmacy.category`

| Field | Type | Description | Required | Notes |
|-------|------|-------------|----------|-------|
| `name` | Char | Category name | ✓ | Translatable |
| `code` | Char | Short code | - | Optional, e.g., "ANTIBIOTIC" |
| `description` | Text | Category description | - | Optional |
| `parent_id` | Many2one | Parent category (self) | - | For hierarchical classification |
| `child_ids` | One2many | Child categories (self) | - | Auto-computed inverse |

**Use Case:** Create taxonomy like:
- Antibiotics (Parent)
  - Penicillins (Child)
  - Cephalosporins (Child)

### Model: `pharmacy.patient`

| Field | Type | Description | Required | Notes |
|-------|------|-------------|----------|-------|
| `name` | Char | Patient full name | ✓ | 255 chars max |
| `age` | Integer | Patient age | - | Optional |
| `gender` | Selection | Gender | - | `male` / `female` / `other` |
| `phone` | Char | Contact number | - | Optional |
| `email` | Char | Email address | - | Optional |
| `address` | Text | Full address | - | Optional |
| `blood_group` | Selection | Blood type | - | `A+` / `A-` / `B+` / `B-` / `O+` / `O-` / `AB+` / `AB-` |
| `doctor_id` | Many2one | Assigned doctor (`res.users`) | ✓ | Doctor group member, controls visibility |
| `medical_history` | Text | Past medical conditions | - | Free-form notes |
| `allergies` | Text | Known allergies | - | Critical for prescription safety |
| `active` | Boolean | Is active patient | - | For soft-delete, default True |

**Access Logic:**
- Doctors can CRUD their assigned patients only
- Managers can CRUD all patients
- Patients have no access

---

## 🔐 Security Groups & Record Rules

### User Groups (3-tier)

**1. Patient Group** (`group_pharmacy_patient`)
- Lowest privilege level
- Purpose: End-users buying OTC medicines
- Access: White-license medicines ONLY
- Actions: View, read medicine information
- Visibility: No patient list, no dashboard

**2. Doctor Group** (`group_pharmacy_doctor`)
- Medium privilege level
- Purpose: Medical professionals prescribing medicines
- Access: Blue & White medicines (licensed + OTC)
- Actions: View medicines, manage assigned patients
- Visibility: See dashboard, patients, orders (read-only), medicines list

**3. Manager Group** (`group_pharmacy_manager`)
- Full administrative access
- Purpose: Pharmacy administrators/owners
- Access: All medicines (Green, Blue, White)
- Actions: Full CRUD on all objects, place orders, create invoices
- Visibility: Full access to all menus, dashboards, orders

### Record Rules (ir.rule)

#### Medicines (`pharmacy.medicine`)
```
Patient: domain [('license_category', '=', 'white')] → read-only
Doctor: domain [('license_category', 'in', ['blue', 'white'])] → read-only
Manager: no rule → full CRUD
```

#### Patients (`pharmacy.patient`)
```
Patient: no read access (CSV-level)
Doctor: domain [('doctor_id', '=', user.id)] → read/write/create (no delete)
Manager: domain [(1, '=', 1)] → full CRUD
```

#### Sale Orders (`sale.order`)
```
Global: read-only for all users (domain [(1, '=', 1)])
Manager Override: full CRUD (domain [(1, '=', 1)], all perms=True)
Doctors: read-only via global rule
```

#### Categories (`pharmacy.category`)
```
Patient: no read access (CSV-level)
Doctor: read-only (CSV-level)
Manager: full CRUD (CSV-level)
```

### Model-Level Permissions (ir.model.access)

| Model | Patient | Doctor | Manager | Notes |
|-------|---------|--------|---------|-------|
| `pharmacy.medicine` | Read | Read | Create/Read/Write/Delete | Via record rules |
| `pharma.control.center` | No Access | Read | Create/Read/Write/Delete | Dashboard model |
| `pharmacy.category` | No Access | Read | Create/Read/Write/Delete | Config only for managers |
| `pharmacy.patient` | No Access | Create/Read/Write | Create/Read/Write/Delete | Doc via record rule |
| `sale.order` | No Access | Read | Create/Read/Write/Delete | Via record rules |

### Menu Item Visibility

| Menu | Patient | Doctor | Manager | Visible |
|------|---------|--------|---------|---------|
| 💊 Pharma Control Center (root) | - | - | - | Always |
| 📊 Dashboard | ✗ | ✓ | ✓ | No |
| 💊 Medicines | ✗ | ✓ | ✓ | Yes |
| 👥 Patients | ✗ | ✓ | ✓ | Yes |
| 🧾 Orders | ✗ | ✓ | ✓ | Yes |
| ⚙️ Categories | ✗ | ✗ | ✓ | Yes (Config) |

---

## 📦 Dependencies

- `base_setup` – Odoo base setup module (users, groups, settings)
- `product` – Odoo product module (for product creation on ordering)
- `account` – Odoo accounting module (for invoice generation)
- `sale` – Odoo sales module (for sale order creation)

All dependencies are core Odoo modules. No third-party packages required.

---

## 🚀 Installation & Setup

### Step 1: Copy Module
```bash
cp -r pharma_control_center /path/to/odoo/addons/
```

### Step 2: Update Apps List (Odoo UI)
1. Go to **Apps** menu
2. Click **Update Apps List** button
3. Click **Update** in the confirmation dialog

### Step 3: Install Module
1. Search for "Pharma Control Center" in Apps
2. Click the module card
3. Click **Install** button
4. Wait for installation to complete (green checkmark)

### Step 4: Configure User Groups
1. Go to **Settings** → **Users & Companies** → **Users** (or **Users**)
2. Select a user
3. Scroll to **Access Rights** section
4. Check one of:
   - ✓ **Pharma Control Center / Patient** – for patients/end-users
   - ✓ **Pharma Control Center / Doctor** – for medical staff
   - ✓ **Pharma Control Center / Manager** – for administrators
5. **Save** user

### Step 5: Create Demo Data (Optional)
Demo data is loaded automatically if `demo_patients.xml` and `demo_medicines.xml` are in `__manifest__.py` `data` list. No additional steps needed.

### Step 6: Verify Installation
1. **Logout** and **Log In** to refresh user permissions
2. Check if **💊 Pharma Control Center** menu appears in sidebar
3. Navigate through menus (Dashboard, Medicines, Patients, Orders)
4. Verify correct data is visible based on your user group

---

## 🧪 Demo Data

The module includes comprehensive demo data:

### Demo Users
- **doctor_demo** (Doctor Group)
  - Username: `doctor_demo`
  - Password: `demo`
  - Assigned to: Doctor group

### Demo Patients (3 records)
- Patient 1 → Assigned to doctor_demo
- Patient 2 → Assigned to doctor_demo
- Patient 3 → Assigned to doctor_demo

Medical info included:
- Age, gender, blood group
- Medical history
- Allergy information
- Contact details

### Demo Medicines (Various)
- **Green License (Full):** 1-2 medicines
- **Blue License (Limited):** 2-3 medicines
- **White License (OTC):** 3-4 medicines

Each includes:
- Batch number & expiry date (mix of fresh, expiring, expired)
- Stock levels (mix of in-stock, low-stock, out-of-stock)
- Pricing (cost & selling price)
- Storage conditions
- Dosage & side effects

**To Load Demo Data:**
Ensure `demo_patients.xml` and `demo_medicines.xml` are listed in `__manifest__.py` under `data:`. Demo data loads automatically during module install.

**To Clear Demo Data:**
- Edit demo XML files or delete records via Odoo UI
- No automated cleanup provided

---

## 🛠️ Compatibility & Requirements

### Odoo Compatibility
- **Odoo 18.0+** (uses `<list>` instead of deprecated `<tree>`, modern QWeb)
- **Tested on:** Odoo 18.0

### System Requirements
- **Python:** 3.10+
- **PostgreSQL:** 13+ (recommended: 14+)
- **Browser:** Modern browser supporting ES6 JavaScript (Chrome, Firefox, Safari, Edge)

### Known Limitations
- Orders (sale orders) created via module are standard Odoo orders; full order workflow (payment, shipping) uses standard Odoo modules (not included)
- Invoices created are account.move records; additional accounting is handled by Odoo account module
- No multi-language support for medicine names (but categories are translatable)
- Medicine photo/image storage not included (use Odoo's attachment system separately)

---

## 🧑‍💻 Development & Customization

### Adding Custom Fields
1. Edit relevant model file (`pharma_medicine.py`, `pharmacy_patient.py`, etc.)
2. Add field definition: `custom_field = fields.Char(...)`
3. Update XML view to display field
4. Run module upgrade in Odoo UI or CLI

### Extending Security Rules
1. Edit security XML file (`pharmacy_security.xml`, etc.)
2. Add new `<record model="ir.rule">` with custom domain
3. Link to appropriate group
4. Reload module

### Customizing Dashboard Statistics
Edit `_compute_statistics` method in `pharma_control_center.py` to add custom calculations.

### Adding Reports
Create new view type in views XML or use Odoo's PDF report engine (separate implementation).

---

## 📄 License

LGPL-3.0 (GNU Lesser General Public License v3)

Full license text in LICENSE file.

---

## 🙌 Contributing

Contributions welcome! To contribute:

1. **Fork** the module repository
2. **Create feature branch:** `git checkout -b feature/my-feature`
3. **Make changes** with clear commit messages
4. **Test** your changes thoroughly
5. **Submit pull request** with description

**For major changes:**
- Open an issue first to discuss
- Update README.md with new features
- Add unit tests if applicable
- Provide demo data for new features

---

## 📧 Support & Issues

- **Report Bugs:** Create issue with clear description, steps to reproduce, attached logs
- **Request Features:** Create issue with `[FEATURE REQUEST]` tag
- **Questions:** Check README.md first, then open discussion

---

## Change History

### Version 1.0 (Current)
- ✅ Complete medicine management module
- ✅ Patient records with doctor assignment
- ✅ Sales order & invoice integration
- ✅ Role-based access control (Patient/Doctor/Manager)
- ✅ Real-time dashboard with statistics
- ✅ Inventory tracking & expiry management
- ✅ Odoo 18 compatibility

---

**Developed with ❤️ for the Odoo community.**  
**Muhammad Qasim Shabbir (AI Trainer/Developer) – 2026**

**Module Version:** 1.0  
**Last Updated:** April 29, 2026

