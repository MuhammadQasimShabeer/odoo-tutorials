from odoo import models, fields, api
from datetime import date, timedelta

class PharmacyMedicine(models.Model):
    _name = "pharmacy.medicine"
    _description = "Pharmacy Medicine"
    _order = "name"

    # Basic info
    name = fields.Char(string="Medicine Name", required=True)
    description = fields.Text(string="Description")
    manufacturer = fields.Char(string="Manufacturer", help="Company that produces this medicine")
    barcode = fields.Char(string="Barcode", help="Product barcode (EAN/UPC)")

    # Category (Many2one for flexibility)
    category_id = fields.Many2one('pharmacy.category', string="Medicine Category", required=True, ondelete='restrict')
    sub_category = fields.Char(string="Sub‑Category")

    # Batch and expiry
    batch_number = fields.Char(string="Batch Number", required=True)
    expiry_date = fields.Date(string="Expiry Date", required=True)

    # Pricing and costs
    price = fields.Float(string="Selling Price", required=True)
    cost_price = fields.Float(string="Cost Price", help="Purchase cost per unit")
    profit_margin = fields.Float(string="Profit Margin (%)", compute="_compute_profit_margin", store=True)

    # Stock
    quantity = fields.Integer(string="Stock Quantity", required=True, default=0)
    reorder_level = fields.Integer(string="Reorder Level", default=10, help="Notify when stock falls below this number")
    need_reorder = fields.Boolean(string="Need Reorder", compute="_compute_need_reorder", store=True)

    # Statuses
    in_stock = fields.Boolean(string="In Stock", compute="_compute_in_stock", store=True)
    days_to_expiry = fields.Integer(string="Days to Expiry", compute="_compute_expiry_days", store=True)
    expiry_status = fields.Selection([
        ('fresh', 'Fresh'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
    ], string="Expiry Status", compute="_compute_expiry_status", store=True)

    # Storage
    storage_location = fields.Selection([
        ('room_temp', 'Room Temperature'),
        ('cold', 'Cold Storage'),
        ('frozen', 'Frozen'),
    ], string="Storage Condition", required=True)

    # Notes
    side_effects = fields.Text(string="Side Effects")
    dosage = fields.Char(string="Dosage", help="e.g., 1 tablet twice daily")

    # License category (access control)
    license_category = fields.Selection([
        ('green', '🟢 Pharmacy (Category A) - Full license'),
        ('blue', '🔵 Medical Store (Category B) - Limited license'),
        ('white', '⚪ Drug Store (Category C) - Basic OTC'),
    ], string="Pharmacy License Category", required=True, default='white',
        help="Determines which user groups can access this medicine")

    # Order/invoice integration
    product_id = fields.Many2one('product.product', string="Linked Product", readonly=True)
    is_ordered = fields.Boolean(string="Ordered", default=False, copy=False)
    last_sale_order_id = fields.Many2one('sale.order', string="Last Sale Order", readonly=True)
    last_invoice_id = fields.Many2one('account.move', string="Last Invoice", readonly=True)

    # -------------------------------------------------------------------------
    # Order & Invoice Actions
    # -------------------------------------------------------------------------
    def action_order_medicine(self):
        """Create a sale order and invoice, mark medicine as ordered."""
        self.ensure_one()
        # 1. Ensure a linked product exists
        product = self.product_id
        if not product:
            product = self._create_product()
            self.product_id = product

        # 2. Create sale order
        sale_order = self.env['sale.order'].create({
            'partner_id': self.env.user.partner_id.id,
            'order_line': [(0, 0, {
                'product_id': product.id,
                'product_uom_qty': 1,
                'price_unit': self.price,
            })],
        })
        # 3. Confirm order
        sale_order.action_confirm()
        # 4. Create and post invoice
        invoice = sale_order._create_invoices()
        invoice.action_post()

        # 5. Update medicine record
        self.is_ordered = True
        self.last_sale_order_id = sale_order.id
        self.last_invoice_id = invoice.id

        # 6. Return action to open the invoice
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_view_invoice(self):
        """Open the last invoice created for this medicine."""
        if self.last_invoice_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': self.last_invoice_id.id,
                'view_mode': 'form',
                'target': 'new',
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'No invoice found for this medicine.',
                    'type': 'warning',
                }
            }

    def action_view_order(self):
        """Open the last sale order created for this medicine."""
        if self.last_sale_order_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'res_id': self.last_sale_order_id.id,
                'view_mode': 'form',
                'target': 'new',
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'No sale order found for this medicine.',
                    'type': 'warning',
                }
            }

    def _create_product(self):
        """Create a consumable product (no inventory tracking) from the medicine."""
        product = self.env['product.product'].create({
            'name': self.name,
            'list_price': self.price,
            'standard_price': self.cost_price or 0.0,
            'type': 'consu',      # consumable, does not require stock module
            'sale_ok': True,
            'purchase_ok': False,
        })
        self.product_id = product
        return product

    # -------------------------------------------------------------------------
    # Compute Methods
    # -------------------------------------------------------------------------
    @api.depends('price', 'cost_price')
    def _compute_profit_margin(self):
        for med in self:
            if med.cost_price and med.cost_price > 0:
                med.profit_margin = ((med.price - med.cost_price) / med.cost_price) * 100
            else:
                med.profit_margin = 0.0

    @api.depends('quantity', 'reorder_level')
    def _compute_need_reorder(self):
        for med in self:
            med.need_reorder = med.quantity <= med.reorder_level

    @api.depends('quantity')
    def _compute_in_stock(self):
        for med in self:
            med.in_stock = med.quantity > 0

    @api.depends('expiry_date')
    def _compute_expiry_days(self):
        today = date.today()
        for med in self:
            if med.expiry_date:
                delta = (med.expiry_date - today).days
                med.days_to_expiry = delta
            else:
                med.days_to_expiry = 0

    @api.depends('expiry_date')
    def _compute_expiry_status(self):
        today = date.today()
        for med in self:
            if not med.expiry_date:
                med.expiry_status = 'fresh'
            elif med.expiry_date < today:
                med.expiry_status = 'expired'
            elif med.expiry_date <= today + timedelta(days=30):
                med.expiry_status = 'expiring_soon'
            else:
                med.expiry_status = 'fresh'