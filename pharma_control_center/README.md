# 💊 Pharma Control Center (Odoo 18+ Module)

## Overview

**Pharma Control Center** is a comprehensive, production-ready Odoo 18+ module designed for modern pharmacy management systems. It provides a complete ecosystem for medicine cataloguing, batch and expiry tracking, intelligent inventory management, patient records with doctor assignments, a sophisticated cart-based ordering system, and real-time operational dashboards. The module strictly adheres to Odoo 18 conventions (using `<list>` instead of deprecated `<tree>`), seamlessly integrates with Odoo's sales, accounting, and product modules, and implements multi-tier role-based access control (Patient / Doctor / Manager) with fine-grained security rules at both the model and record levels.

**Key Highlights:**
- 🏥 **Professional-grade medicine management** with expiry tracking and license categories
- 👥 **Patient-doctor relationship system** with secure record visibility
- 🛒 **Cart-based ordering workflow** with one-click checkout and automatic invoicing
- 📊 **Real-time dashboard** with user profile, statistics, and operational alerts
- ⚠️ **Drug interaction detection** system with severity levels and warnings
- 📈 **Advanced sales analytics** with graphs and pivot tables for managers
- 💌 **Email notifications** via SMTP for order confirmations and alerts
- 🔐 **Enterprise-grade security** with role-based access control and record-level rules
- ✨ **Odoo 18 compliant** with modern views, computed fields, and QWeb templates

---

## ✨ Key Features

### 💊 Complete Medicine Management System

#### Comprehensive Medicine Catalog
- **Full data model** including medicine name, manufacturer, batch number, barcode, and universal product code (UPC)
- **Hierarchical categorization** with parent-child category relationships for logical organization
- **License-based access model** (Green/Blue/White) determines which user groups can view and interact with each medicine
- **Storage conditions tracking** – room temperature, cold storage (2-8°C), and frozen storage support
- **Batch and traceability** – complete batch number tracking for recalls and regulatory compliance
- **Regulatory metadata** – dosage instructions, side effects documentation, and safety information

#### Intelligent Pricing & Profitability
- **Dual pricing system** – selling price and cost price with automatic profit margin calculation
- **Real-time margin analytics** – computed field updates profit percentage dynamically
- **Price-based stock valuation** – total inventory value calculated as sum of (quantity × selling price)

#### Advanced Stock Management
- **Real-time inventory tracking** – quantity-based stock status (in-stock, low-stock, out-of-stock)
- **Intelligent reorder system** – configurable reorder level with "Need Reorder" alerts
- **Low stock detection** – automatic flagging of medicines with 1-9 units remaining
- **Automatic stock reduction** – inventory decremented on successful cart checkout
- **Stock status badges** – visual indicators in list and kanban views for quick inventory assessment

#### Expiry Management & Alerts
- **Automated expiry calculations** – computed field tracks remaining days until expiration
- **Three-tier expiry status** – Fresh (>30 days), Expiring Soon (≤30 days), Expired (<today)
- **Color-coded badges** – visual status indicators throughout the interface
- **Expiry alerts dashboard** – dedicated tab showing medicines expiring within 30 days
- **Regulatory compliance** – supports recalls and stock rotations

### 👥 Professional Patient Management

#### Complete Patient Records System
- **Centralized patient database** – comprehensive personal information storage
- **Medical profile** – medical history, known allergies, blood group (A+/A-/B+/B-/O+/O-/AB+/AB-)
- **Contact management** – phone, email, and physical address storage
- **Demographics** – age and gender tracking for personalized healthcare delivery

#### Doctor-Patient Relationship Management
- **Secure assignment** – each patient assigned exclusively to one doctor (res.users)
- **Role-enforced visibility** – doctors see only their assigned patients via record rules
- **Doctor delegation** – ability to reassign patients between doctors
- **Read/Write permissions** – doctors can fully manage their own patients; managers see all
- **Delete restrictions** – doctors cannot delete patients (safety feature)

#### Access Control Integration
- **Doctors see only their patients** – enforced via domain-based record rules
- **Managers see all patients** – unrestricted access for administrative purposes
- **Patients have zero access** – cannot view any patient records (CSV-level restriction)
- **Active/inactive status** – soft-delete support for patient record archival

### ⚠️ Intelligent Drug Interaction Detection System

#### Comprehensive Interaction Management
- **Medicine pair tracking** – define interactions between any two medicines
- **Severity levels** – Minor, Moderate, and Severe classifications for clinical relevance
- **Interactive warnings** – descriptive warning messages explaining side effects and risks
- **Real-time validation** – automatic detection when conflicting medicines are added to cart
- **Checkout blocking** – prevents orders with severe interactions unless explicitly overridden
- **Clinical safety** – protects patients from potentially dangerous drug combinations

#### Interaction Features
- **Bidirectional detection** – interactions detected regardless of medicine order in cart
- **Warning display** – clear visual alerts in cart interface with severity indicators
- **Warning messages** – actionable information for doctors/pharmacists regarding interactions
- **Database tracking** – all interactions stored and queryable for compliance and audit trails
- **Complete interaction history** – maintains records of all detected interactions for reporting

### 🛒 Sophisticated Cart-Based Ordering System

#### Modern Shopping Cart Interface
- **Persistent user cart** – dedicated `pharmacy.cart` model linked to current user
- **One-to-many cart lines** – each cart can contain multiple medicines with independent quantities
- **Quick medicine search** – search and select medicines from catalog directly in cart
- **Quantity management** – editable quantities on cart lines with real-time subtotal updates
- **Cart summary** – displays total quantity and total amount for all items
- **Line-item removal** – delete specific medicines from cart without losing cart context
- **Dynamic pricing** – unit prices and subtotals automatically sync with latest medicine prices
- **Drug interaction warnings** – real-time detection and display of potential medicine interactions in cart

#### Streamlined Order Placement & Checkout
- **One-click checkout** – single button creates complete sale order with all cart items
- **Automatic sale order creation** – generates standard Odoo sale.order with proper order lines
- **Instant confirmation** – sale order automatically confirmed (state = 'sale')
- **Automatic invoicing** – system creates and immediately posts account.move (invoice)
- **Inventory synchronization** – stock quantities automatically reduced for each medicine
- **Cart cleanup** – cart lines deleted after successful checkout
- **User context** – sale orders linked to current user as create_uid
- **Interaction validation** – blocks checkout on severe medicine interactions

#### Orders Management Interface
- **Dedicated Orders menu** – centralized view of all sale orders created via cart
- **Role-filtered visibility** – patients/doctors see only their own orders; managers see all
- **Order history** – full audit trail of all transactions
- **Invoice tracking** – direct access to generated invoices from each order
- **Order state tracking** – full lifecycle from draft to paid/delivered

### 📊 Real-Time Operational Dashboard

#### User Profile Management
- **Profile picture upload** – user avatar displayed on dashboard (stored as binary attachment)
- **User information display** – name, email, and phone retrieved from linked res.users
- **Role badge** – displays current user's role (Patient/Doctor/Manager)
- **Editable profile** – users can update profile pictures and basic information

#### Comprehensive Medicine Statistics
- **Total medicines count** – count of all medicines in the system
- **Stock quantity summary** – total units across entire inventory
- **Inventory value** – aggregated value (sum of quantity × price for all medicines)
- **Out-of-stock count** – medicines with zero quantity
- **Low stock alert** – medicines with 1-9 units remaining
- **Expiring soon count** – medicines expiring within 30 days (from today to +30 days)
- **Expired count** – medicines past expiration date

#### Real-Time Order Analytics
- **Today's order summary** – aggregated statistics for orders placed today only
- **Today's quantity total** – sum of all product quantities ordered today
- **Today's sales amount** – total monetary value of today's orders
- **Role-aware filtering** – managers see all today's orders; doctors/patients see only their own

#### Patient Management Dashboard
- **My Patients tab** – list of patients for doctors; all patients for managers
- **Patient count statistics** – displays total patients and "my patients" count
- **Role-based filtering** – automatically filters patients based on current user's role
- **Read-only access** – dashboard patient lists displayed in read-only mode

#### Expiry Alerts Tab
- **Critical alert list** – medicines expiring within 30 days displayed prominently
- **Color-coded urgency** – visual indicators for expiration severity
- **Actionable information** – days to expiry and expiry date clearly displayed

#### Live Statistics Updates
- **Real-time computation** – all statistics recalculate on each dashboard load
- **No caching overhead** – ensures accuracy in fast-moving inventory scenarios

### 🔐 Enterprise-Grade Role-Based Access Control (RBAC)

#### Three-Tier User Hierarchy

**🟢 Manager (Pharmacy Administrator)**
- **Full system access** – complete CRUD on all objects
- **Medicine visibility** – sees all medicines regardless of license category (Green/Blue/White)
- **Patient management** – full read/write/create/delete on all patient records
- **Order control** – can view, create, edit, and delete all sale orders
- **Dashboard access** – unrestricted access to all statistics and reports
- **Configuration rights** – manage medicine categories, edit settings, etc.
- **Implied permissions** – includes account invoice group permissions for billing
- **Menu access** – Dashboard, Medicines, Patients, Orders, Categories, Settings

**🔵 Doctor (Medical Professional)**
- **Limited medicine visibility** – sees only Blue (limited license) and White (OTC) medicines
- **Medicine restrictions** – cannot view Green (full pharmacy license) medicines for security
- **Read-only medicines** – can view medicine descriptions but cannot create/edit/delete
- **Patient management** – full CRUD on patients assigned to them (doctor_id = user.id)
- **Patient visibility** – can see other doctors' patients in management, but record rule restricts editing
- **Cannot delete patients** – safety feature to maintain medical records
- **Order viewing** – read-only access to their own orders via record rule
- **Dashboard access** – can view dashboard with statistics and their assigned patients
- **Implied permissions** – includes account invoice group permissions
- **Menu access** – Dashboard, Medicines, Patients, Orders (read-only)

**⚪ Patient (End User/Customer)**
- **OTC medicines only** – sees exclusively White (basic over-the-counter) medicines
- **Read-only access** – can view medicine information but cannot edit
- **Cannot place orders directly** – must use cart system for ordering
- **No patient visibility** – cannot access patient list or view any patient records
- **No dashboard** – dashboard menu hidden from view (CSV-level access restriction)
- **My orders** – can see and manage only their own orders created via cart
- **Cannot access** – medicines list, patient records, categories, configuration
- **Menu access** – Medicines (White only), Orders (own orders)

#### Security Implementation: Record Rules (ir.rule)

**Medicine Visibility Rules**
```
Patient Rule:  domain [('license_category', '=', 'white')]
               → Read-only; cannot create, edit, or delete
               
Doctor Rule:   domain [('license_category', 'in', ['blue', 'white'])]
               → Read-only; cannot create, edit, or delete
               
Manager Rule:  No domain restriction
               → Full CRUD on all medicines
```

**Patient Visibility Rules**
```
Patient Rule:  No read access
               → CSV-level restriction; cannot view any patient records
               
Doctor Rule:   domain [('doctor_id', '=', user.id)]
               → Can read/write/create own patients
               → Cannot delete (perm_unlink=False)
               
Manager Rule:  domain [(1, '=', 1)]  [universal domain]
               → Full CRUD on all patients
```

**Sale Order Visibility Rules**
```
Patient Rule:  domain [('create_uid', '=', user.id)]
               → See only own orders; full CRUD on own orders
               
Doctor Rule:   domain [('create_uid', '=', user.id)]
               → See only own orders; full CRUD on own orders
               
Manager Rule:  domain [(1, '=', 1)]  [universal domain]
               → Full CRUD on all orders
```

#### Model-Level Access Control (CSV-based)

| Model | Patient | Doctor | Manager | Access Type |
| |-------|---------|--------|---------|-------------|
| **pharmacy.medicine** | ✓ Read | ✓ Read | ✓✓ Full CRUD | Via record rules |
| **pharma.control.center** | ✓ Read | ✓ Read | ✓✓ Full CRUD | Dashboard access |
| **pharmacy.category** | ✗ None | ✓ Read | ✓✓ Full CRUD | Config only for managers |
| **pharmacy.patient** | ✗ None | ✓ Full CRUD (own) | ✓✓ Full CRUD (all) | Via record rules |
| **pharmacy.interaction** | ✗ None | ✓ Read | ✓✓ Full CRUD | Drug interaction management |
| **pharmacy.cart** | ✓✓ Full CRUD | ✓✓ Full CRUD | ✓✓ Full CRUD | User's own cart |
| **pharmacy.cart.line** | ✓✓ Full CRUD | ✓✓ Full CRUD | ✓✓ Full CRUD | Within user's cart |
| **sale.order** | ✓ Own orders | ✓ Own orders | ✓✓ Full CRUD | Via record rules |

---

## 📈 Advanced Analytics & Reporting

### Sales Analytics Dashboard (Manager-Only)
The module provides comprehensive sales analytics exclusively for managers with real-time data visualization.

#### Graph-Based Sales Trends
- **Bar graph visualization** – daily sales trends with intuitive bar chart representation
- **Customizable intervals** – view data by day, week, month for different analysis levels
- **Sales metrics** – displays total sales amount (monetary value) with currency formatting
- **Interactive filtering** – drill-down capabilities to analyze specific time periods and products

#### Pivot Table Analysis
- **Multi-dimensional pivot views** – analyze sales data from multiple perspectives
- **Dimensional grouping** – break down by date (monthly), patient, and doctor
- **Aggregated metrics** – sum of total sales amount displayed in pivot tables
- **Export capabilities** – export pivot data for external reporting and analysis

#### Sales Report Views
- **Comprehensive reporting interface** – dedicated Sales Report menu in Analytics section
- **Filter options** – filter by date range, patient, doctor, or order status
- **Group by options** – organize data by day, week, month, patient, or doctor
- **Status filtering** – exclude cancelled orders from reports automatically
- **Order date filtering** – date range selection for specific period analysis

#### Manager-Exclusive Access
- **Role-based visibility** – analytics menus visible only to pharmacy managers
- **Full data access** – view all sales data across all doctors and patients
- **Comprehensive insights** – KPIs for performance tracking and inventory forecasting
- **Decision support** – data-driven insights for business optimization

### Email Notification System (SMTP Configuration)
The module supports automated email notifications for critical pharmacy operations.

#### Notification Features
- **Order confirmations** – automatic emails sent to customers upon successful checkout
- **Expiry alerts** – scheduled emails alerting managers about medicines expiring soon
- **Inventory alerts** – notifications when medicines reach or fall below reorder levels
- **Transaction reports** – summary emails of daily sales and transactions
- **SMTP configuration** – seamless integration with Odoo's mail server settings

#### Email Template System
- **Customizable templates** – pre-defined templates for different notification types
- **Dynamic content** – templates automatically populate with order and patient details
- **Multi-recipient support** – emails sent to patients, doctors, and managers as appropriate
- **Audit trail** – all sent emails logged in Odoo for compliance and tracking

---

## 🧱 Module Architecture & Structure

```
odoo-tutorials/pharma_control_center/
├── __init__.py                                # Module package initialization
├── __manifest__.py                            # Module metadata and configuration
├── README.md                                  # This file
│
├── data/                                      # Demo data and fixtures
│   ├── demo_medicines.xml                     # Sample medicines (all categories)
│   └── demo_patients.xml                      # Sample patients and doctor assignments
│
├── models/                                    # Python data models
│   ├── __init__.py                            # Model imports and initialization
│   ├── pharma_medicine.py                     # Medicine model (CRUD, calculations, cart actions)
│   ├── pharma_control_center.py               # Dashboard model (statistics, profile)
│   ├── pharmacy_cart.py                       # Shopping cart and checkout logic
│   ├── pharmacy_category.py                   # Hierarchical medicine categories
│   ├── pharmacy_patient.py                    # Patient records with doctor assignment
│   ├── pharmacy_interaction.py                # Drug interaction model and detection
│   └── __pycache__/                           # Compiled Python cache
│
├── security/                                  # Access control configuration
│   ├── groups.xml                             # User groups definition (Patient, Doctor, Manager)
│   ├── ir.model.access.csv                    # Model-level access control list
│   ├── pharmacy_security.xml                  # Record rules for medicines (license-based)
│   ├── pharmacy_patient_security.xml          # Record rules for patients (doctor assignment)
│   └── sale_order_security.xml                # Record rules for sale orders
│
├── views/                                     # UI configuration (XML templates)
│   ├── pharma_control_center_views.xml        # Dashboard views and root menu
│   ├── pharmacy_medicine_views.xml            # Medicine list, form, kanban, search views
│   ├── pharmacy_patient_views.xml             # Patient list, form, search views
│   ├── pharmacy_category_views.xml            # Category tree and form views
│   ├── pharmacy_cart_views.xml                # Shopping cart interface
│   ├── pharmacy_interaction_views.xml         # Drug interaction list and form views
│   ├── pharmacy_order_views.xml               # Sale order views (Orders menu)
│   ├── sales_report_views.xml                 # Sales report with pivot view
│   └── manager_analytics_views.xml            # Manager analytics with graphs
│
└── test/                                      # Unit tests
    └── test_pharma_control_center.py          # Test cases for core functionality
```

---

## 🔧 Technical Architecture

### Core Data Models

#### **pharmacy.medicine** – Medicine Model (160 lines)
Complete medicine information and inventory tracking.

| Field | Type | Description | Required | Computed |
|-------|------|-------------|----------|----------|
| `name` | Char | Medicine name | ✓ | - |
| `description` | Text | Product description | - | - |
| `manufacturer` | Char | Manufacturer name | - | - |
| `barcode` | Char | EAN/UPC barcode | - | - |
| `category_id` | Many2one → pharmacy.category | Medicine category | ✓ | - |
| `sub_category` | Char | Sub-category text | - | - |
| `batch_number` | Char | Batch/lot number | ✓ | - |
| `expiry_date` | Date | Expiration date | ✓ | - |
| `price` | Float | Selling price per unit | ✓ | - |
| `cost_price` | Float | Cost/purchase price | - | - |
| `profit_margin` | Float | Profit % | - | ✓ Computed: ((price - cost_price) / cost_price) × 100 |
| `quantity` | Integer | Stock quantity | ✓ | - |
| `reorder_level` | Integer | Reorder threshold | - | - (default: 10) |
| `need_reorder` | Boolean | Low stock flag | - | ✓ Computed: quantity ≤ reorder_level |
| `in_stock` | Boolean | Stock status | - | ✓ Computed: quantity > 0 |
| `days_to_expiry` | Integer | Days until expiry | - | ✓ Computed: (expiry_date - today).days |
| `expiry_status` | Selection | Status badge | - | ✓ Computed: fresh/expiring_soon/expired |
| `storage_location` | Selection | Storage condition | ✓ | - (room_temp/cold/frozen) |
| `dosage` | Char | Usage instructions | - | - |
| `side_effects` | Text | Side effects info | - | - |
| `license_category` | Selection | Access level | ✓ | - (green/blue/white) |
| `product_id` | Many2one → product.product | Linked Odoo product | - | - |
| `last_sale_order_id` | Many2one → sale.order | Last order | - | - |
| `last_invoice_id` | Many2one → account.move | Last invoice | - | - |
| `order_qty` | Integer | Cart quantity | - | - (default: 1) |
| `today_orders_qty` | Float | Today's quantity | - | ✓ Computed: sum of today's order line quantities |

**Key Methods:**
- `add_to_cart()` – Adds medicine to user's cart
- `_create_product()` – Auto-creates Odoo product.product on first order

#### **pharma.control.center** – Dashboard Model (142 lines)
User profile and operational statistics.

| Field | Type | Description | Computed | Purpose |
|-------|------|-------------|----------|---------|
| `user_id` | Many2one → res.users | Linked user | - | Profile owner |
| `avatar` | Binary | Profile picture | - | User-uploadable |
| `avatar_filename` | Char | Avatar filename | - | File metadata |
| `name` | Char | User name | ✓ (related) | Display name |
| `email` | Char | Email address | ✓ (related) | Contact info |
| `phone` | Char | Phone number | ✓ (related) | Contact info |
| `role` | Char | User role badge | ✓ | Patient/Doctor/Manager |
| `total_medicines` | Integer | Medicine count | ✓ | `COUNT(pharmacy.medicine)` |
| `total_stock_quantity` | Integer | Total stock | ✓ | `SUM(quantity)` across all medicines |
| `stock_value` | Float | Inventory value (₹) | ✓ | `SUM(quantity × price)` |
| `out_of_stock_count` | Integer | Out-of-stock count | ✓ | Count where quantity = 0 |
| `low_stock_count` | Integer | Low stock count | ✓ | Count where 0 < quantity < 10 |
| `expiring_soon_count` | Integer | Expiring soon count | ✓ | Count where today < expiry_date ≤ today + 30 |
| `expired_count` | Integer | Expired count | ✓ | Count where expiry_date < today |
| `total_patients` | Integer | Patient count | ✓ | `COUNT(pharmacy.patient)` |
| `my_patients` | Integer | Doctor's patients | ✓ | Count of assigned patients (doctors only) |
| `patient_ids` | One2many → pharmacy.patient | Patient list | ✓ | Role-filtered patient records |
| `today_order_total_qty` | Float | Today's qty | ✓ | Sum of today's order line quantities |
| `today_order_total_amount` | Float | Today's sales | ✓ | Sum of today's order line amounts |

**Key Methods:**
- `_compute_statistics()` – Recalculates all metrics in real-time
- `_compute_patient_ids()` – Filters patients by user role
- `_compute_today_orders_summary()` – Aggregates today's order data
- `action_view_today_orders()` – Links to today's orders list

#### **pharmacy.cart** & **pharmacy.cart.line** – Shopping Cart (89 lines)
Shopping cart functionality with checkout workflow.

**pharmacy.cart (Shopping Cart):**
| Field | Type | Description |
|-------|------|-------------|
| `user_id` | Many2one → res.users | Cart owner |
| `cart_line_ids` | One2many → pharmacy.cart.line | Cart items |
| `total_quantity` | Integer | ✓ Computed: sum of all line quantities |
| `total_amount` | Float | ✓ Computed: sum of all line subtotals |
| `quick_medicine_ids` | Many2many → pharmacy.medicine | Quick-add medicines |
| `quick_order_qty` | Integer | Quantity for quick-add (default: 1) |

**Key Methods:**
- `action_checkout()` – Creates sale order, posts invoice, reduces stock, clears cart
- `action_add_quick_medicines()` – Bulk-add medicines from search

**pharmacy.cart.line (Cart Item):**
| Field | Type | Description |
|-------|------|-------------|
| `cart_id` | Many2one → pharmacy.cart | Parent cart |
| `medicine_id` | Many2one → pharmacy.medicine | Medicine item |
| `quantity` | Integer | Quantity ordered |
| `unit_price` | Float | ✓ Related: medicine_id.price |
| `subtotal` | Float | ✓ Computed: quantity × unit_price |

#### **pharmacy.category** – Medicine Categories (12 lines)
Hierarchical medicine classification.

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Category name (translatable) |
| `code` | Char | Short code (e.g., "ANTIBIOTIC") |
| `description` | Text | Category description |
| `parent_id` | Many2one (self) | Parent category |
| `child_ids` | One2many (self) | Child categories |

#### **pharmacy.patient** – Patient Records (32 lines)
Patient information with doctor assignment.

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Patient full name |
| `doctor_id` | Many2one → res.users | Assigned doctor |
| `age` | Integer | Patient age |
| `gender` | Selection | male/female/other |
| `phone` | Char | Contact phone |
| `email` | Char | Email (unique constraint) |
| `address` | Text | Physical address |
| `blood_group` | Selection | Blood type (8 options) |
| `medical_history` | Text | Medical background |
| `allergies` | Text | Known allergies |
| `active` | Boolean | Active/archived status |

#### **pharmacy.interaction** – Drug Interaction Records (21 lines)
Drug interaction tracking and management for clinical safety.

| Field | Type | Description | Required | Computed |
|-------|------|-------------|----------|----------|
| `medicine1_id` | Many2one → pharmacy.medicine | First medicine | ✓ | - |
| `medicine2_id` | Many2one → pharmacy.medicine | Second medicine | ✓ | - |
| `severity` | Selection | Interaction severity level | ✓ | - (minor/moderate/severe) |
| `warning_text` | Text | Clinical warning message | ✓ | - |
| `display_name` | Char | Display name (computed) | - | ✓ Computed: "Medicine1 + Medicine2" |

**Key Features:**
- Bidirectional interaction detection
- Severity-based checkout blocking
- Clinical safety validation
- Warning message tracking

## 🚀 Installation & Setup

### Prerequisites
- Odoo 18.0 or later
- PostgreSQL 13+
- Python 3.10+
- Core Odoo modules: `base_setup`, `product`, `account`, `sale`

### Step-by-Step Installation

**Step 1: Copy Module to Addons Directory**
```bash
cp -r pharma_control_center /path/to/odoo/addons/
```

**Step 2: Update Apps List**
1. Go to **Apps** menu in Odoo interface
2. Click **Update Apps List** button
3. Confirm the action

**Step 3: Find and Install Module**
1. Search for "Pharma Control Center" in Apps search bar
2. Click the module card
3. Click **Install** button
4. Wait for installation to complete (green checkmark)

**Step 4: Create/Assign User Groups**
1. Navigate to **Settings** > **Users & Companies** > **Users**
2. Select a user to configure
3. Scroll to **Access Rights / Groups** section
4. Assign one of the following groups:
   - **Pharma Control Center / Patient** – for end-users
   - **Pharma Control Center / Doctor** – for medical professionals
   - **Pharma Control Center / Manager** – for administrators
5. Click **Save**

**Step 5: Load Demo Data (Automatic)**
Demo data loads automatically if `demo_medicines.xml` and `demo_patients.xml` are listed in `__manifest__.py`. No manual action needed.

**Step 6: Verify Installation**
1. **Logout** completely and **Log In** to refresh user permissions
2. Check if **💊 Pharma Control Center** menu appears in sidebar
3. Navigate through each menu section to verify correct access based on your role
4. Test cart functionality by adding items and checking out

---

## 📖 User Guide

### For Patients (End Users)
1. **View Medicines:** Click **Medicines** menu → browse OTC (White) medicines only
2. **Add to Cart:** In medicine form, set quantity in "Order Quantity" field → click **Add to Cart**
3. **View Cart:** Click **My Cart** menu → see all items, edit quantities, remove items
4. **Checkout:** Click **Checkout** button → automatic sale order creation, invoice, and stock reduction
5. **View Orders:** Click **Orders** menu → see your order history with status and dates

### For Doctors
1. **View Medicines:** Click **Medicines** menu → browse Blue (limited) and White (OTC) medicines
2. **Manage Patients:** Click **Patients** menu → create new patients, edit assigned patients, view medical history
3. **Dashboard:** Click **Dashboard** menu → view statistics, expiry alerts, and your assigned patients
4. **Place Orders:** Same as patients (add to cart → checkout)
5. **View Orders:** See only your own orders (no access to other doctors' orders)

### For Managers
1. **Full Access:** All medicines, patients, categories, and orders
2. **Dashboard:** View all statistics, all patients, and all today's orders
3. **Configuration:** Create/edit medicine categories; configure reorder levels
4. **Inventory Management:** Monitor stock, expiry dates, and low-stock alerts
5. **Orders:** View and manage all sale orders; can edit order details post-creation
6. **Drug Interactions:** Manage drug interaction database; define interactions between medicines
7. **Sales Analytics:** Access comprehensive sales analytics with graphs and pivot tables
8. **Reports:** Generate sales reports grouped by date, patient, or doctor

### Drug Interaction Management
1. **Access Interactions:** Navigate to **⚠️ Drug Interactions** menu
2. **View Interactions:** List of all configured drug interactions with severity levels
3. **Create Interaction:** Click **Create** button to define new interactions
4. **Configure Details:**
   - Select Medicine A and Medicine B
   - Set severity level (Minor/Moderate/Severe)
   - Enter warning message with clinical details
5. **Cart Validation:** System automatically detects interactions when medicines added to cart
6. **Checkout Blocking:** Severe interactions will block checkout until resolved

### Analytics & Sales Reports
1. **Access Analytics:** Click **📊 Analytics** menu (Manager-only)
2. **View Sales Analytics:** Click **📈 Sales Analytics** to see graphs and pivot tables
3. **Graph View:** Bar charts showing daily sales trends with total sales amount
4. **Pivot View:** Multi-dimensional analysis by month, patient, and doctor
5. **Sales Report:** Click **Sales Report** for detailed transaction reports
6. **Filtering:** Use date range, patient, and doctor filters
7. **Grouping:** Organize data by day, week, month, patient, or doctor
8. **Export:** Export pivot data for external analysis (Excel, sheets, etc.)

### Cart Workflow Example
```
1. Search for "Aspirin" → Click on medicine card
2. Set "Order Quantity" to 2
3. Click "Add to Cart" button → green notification
4. Click "My Cart" menu
5. See "1 item, Total: ₹50"
6. Can edit quantity or remove items
7. Click "Checkout" button
8. → Sale order created and confirmed
9. → Invoice automatically generated and posted
10. → Stock reduced by 2 units
11. → Directed to invoice view
12. → Cart cleared
```

---

## 📦 Demo Data

The module includes comprehensive sample data to facilitate testing and training.

### Demo Users
- **doctor_demo** (Doctor Group)
  - Username: `doctor_demo`
  - Password: `demo`
  - Group: Pharma Control Center / Doctor

### Demo Patients (3 records)
Located in `data/demo_patients.xml`:
- Patient 1 – Assigned to doctor_demo
- Patient 2 – Assigned to doctor_demo
- Patient 3 – Assigned to doctor_demo

**Included Information:**
- Personal demographics (age, gender, blood group)
- Contact details (phone, email, address)
- Medical information (allergies, medical history)

### Demo Medicines (Variety of Status)
Located in `data/demo_medicines.xml`:

**License Categories Represented:**
- 🟢 **Green License** (1-2 medicines) – Full pharmacy license
- 🔵 **Blue License** (2-3 medicines) – Limited medical store license
- ⚪ **White License** (3-4 medicines) – Basic OTC

**Expiry Status Mix:**
- Fresh medicines (>30 days)
- Expiring soon (≤30 days)
- Expired (<today)

**Stock Status Mix:**
- In stock (>10 units)
- Low stock (1-9 units)
- Out of stock (0 units)

**Auto-Loading:**
- Demo data automatically loads during module installation
- Remove via Odoo UI by deleting records, or comment out in XML

---

## 🛠️ Compatibility & Requirements

### Supported Odoo Versions
- **Odoo 18.0+** (minimum requirement)
- Tested on: Odoo 18.0

### Python & Database Requirements
- **Python:** 3.10 or higher
- **PostgreSQL:** 13+ (recommended: 14+)
- **Browser:** Modern browser with ES6 JavaScript support (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)

### Core Odoo Dependencies
- `base_setup` – Base setup and user management
- `product` – Product catalog and management
- `account` – Accounting and invoicing
- `sale` – Sales orders and quotations

### Known Limitations & Considerations
- **Invoice Workflow:** Invoices created by module are standard Odoo account.move; advanced billing workflows require additional configuration
- **Payment Processing:** Sale orders use standard Odoo payment flow; requires separate payment gateway setup
- **Multi-Currency:** Module supports single-currency operations; multi-currency setup requires additional configuration
- **Localization:** Medicine names not translatable; categories are translatable
- **Attachments:** Product images/documents use standard Odoo attachment system; requires separate storage configuration
- **Audit Trail:** Full transaction history available via Odoo's access logs

---

## 🧑‍💻 Development & Customization

### Adding Custom Medicine Fields
```python
# In models/pharma_medicine.py
custom_field = fields.Char(
    string="Custom Field",
    help="Your help text",
)
```
Then update views in `views/pharmacy_medicine_views.xml`.

### Extending Security Rules
```xml
<!-- In security/pharmacy_security.xml -->
<record model="ir.rule" id="custom_rule">
    <field name="name">Custom Rule</field>
    <field name="model_id" ref="model_pharmacy_medicine"/>
    <field name="groups" eval="[(4, ref('pharma_control_center.group_pharmacy_doctor'))]"/>
    <field name="domain_force">[('custom_field', '=', 'value')]</field>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="False"/>
    <field name="perm_create" eval="False"/>
    <field name="perm_unlink" eval="False"/>
</record>
```

### Customizing Dashboard Statistics
Edit `_compute_statistics()` method in `models/pharma_control_center.py` to add custom calculations.

### Creating Custom Reports
Use Odoo's built-in report engine or create custom views/actions:
```python
def action_custom_report(self):
    return {
        'type': 'ir.actions.report',
        'report_name': 'pharma_control_center.custom_report',
        'report_type': 'qweb-pdf',
    }
```

### Extending Cart Functionality
```python
# In models/pharmacy_cart.py
def custom_action_checkout(self):
    # Add custom logic before/after standard checkout
    super().action_checkout()
    # Add post-checkout actions here
```

---

## 🧪 Testing

Run unit tests:
```bash
python -m pytest test/test_pharma_control_center.py -v
```

Or via Odoo CLI:
```bash
odoo -d your_database -i pharma_control_center --test-tags pharma_control_center
```

---

## 📋 Changelog

### Version 1.1 (Current) – May 6, 2026
- ✅ Advanced drug interaction detection system with severity levels
- ✅ Real-time interaction warnings in shopping cart
- ✅ Checkout blocking for severe medicine interactions
- ✅ Comprehensive sales analytics dashboard (Manager-only)
- ✅ Graph-based sales trends with bar charts and line graphs
- ✅ Multi-dimensional pivot table analysis for sales data
- ✅ Flexible sales report views with filtering and grouping options
- ✅ Email notification system with SMTP configuration
- ✅ Order confirmation emails and expiry alert notifications
- ✅ Transaction summary reports via email

### Version 1.0 – April 29, 2026
- ✅ Complete medicine management module with batch and expiry tracking
- ✅ Patient records with doctor assignments and role-based visibility
- ✅ Cart-based ordering workflow with one-click checkout
- ✅ Automatic sale order and invoice generation
- ✅ Real-time operational dashboard with profile and statistics
- ✅ Enterprise-grade RBAC with three user tiers (Patient/Doctor/Manager)
- ✅ Record-level security rules for medicines, patients, and orders
- ✅ Full Odoo 18 compatibility with modern UI conventions
- ✅ Comprehensive demo data for testing and training

---

## 📧 Support & Contribution

### Bug Reports & Feature Requests
- Create an issue with clear description and steps to reproduce
- Include Odoo version, Python version, and error messages/logs
- Attach screenshots for UI-related issues

### Contributing Changes
1. **Fork** the repository
2. **Create feature branch:** `git checkout -b feature/your-feature`
3. **Make changes** with clear commit messages
4. **Test thoroughly** with different user roles
5. **Update README.md** with new features/changes
6. **Add unit tests** for new functionality
7. **Submit pull request** with detailed description

### Development Guidelines
- Follow Odoo coding standards and conventions
- Use descriptive variable/method names
- Add docstrings for complex logic
- Test with multiple user roles (Patient/Doctor/Manager)
- Verify security rules are enforced correctly

---

## 📄 License

**LGPL-3.0** (GNU Lesser General Public License v3.0)

This module is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License.

---

## 👨‍💻 About

**Pharma Control Center** is developed with ❤️ for the Odoo community, providing a professional-grade solution for pharmacy and healthcare operations management.

**Author:** Muhammad Qasim Shabbir (AI Trainer/Developer)  
**Date:** May 6, 2026  
**Version:** 1.1  
**Module Status:** Production-Ready  
**Odoo Compatibility:** 18.0+

---

**For questions, support, or feedback, please reach out through the official Odoo community channels.**

🏥 ***Professional Pharmacy Management, Simplified.*** 💊

