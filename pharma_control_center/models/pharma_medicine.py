import json
from odoo import models, fields, api, _
from datetime import date, timedelta, datetime
from odoo.exceptions import UserError

class ResUsers(models.Model):
    _inherit = 'res.users'
    cart_data = fields.Text(string="Cart Data", default="{}", help="JSON cart for pharmacy module")

class PharmacyMedicine(models.Model):
    _name = "pharmacy.medicine"
    _description = "Pharmacy Medicine"
    _order = "name"

    name = fields.Char(string="Medicine Name", required=True)
    description = fields.Text(string="Description")
    manufacturer = fields.Char(string="Manufacturer")
    barcode = fields.Char(string="Barcode")
    category_id = fields.Many2one('pharmacy.category', string="Medicine Category", required=True, ondelete='restrict')
    sub_category = fields.Char(string="Sub‑Category")
    batch_number = fields.Char(string="Batch Number", required=True)
    expiry_date = fields.Date(string="Expiry Date", required=True)
    price = fields.Float(string="Selling Price", required=True)
    cost_price = fields.Float(string="Cost Price")
    profit_margin = fields.Float(string="Profit Margin (%)", compute="_compute_profit_margin", store=True)
    quantity = fields.Integer(string="Stock Quantity", required=True, default=0)
    reorder_level = fields.Integer(string="Reorder Level", default=10)
    need_reorder = fields.Boolean(string="Need Reorder", compute="_compute_need_reorder", store=True)
    order_qty = fields.Integer(string="Order Quantity", default=1)
    in_stock = fields.Boolean(string="In Stock", compute="_compute_in_stock", store=True)
    days_to_expiry = fields.Integer(string="Days to Expiry", compute="_compute_expiry_days", store=True)
    expiry_status = fields.Selection([
        ('fresh', 'Fresh'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
    ], string="Expiry Status", compute="_compute_expiry_status", store=True)
    storage_location = fields.Selection([
        ('room_temp', 'Room Temperature'),
        ('cold', 'Cold Storage'),
        ('frozen', 'Frozen'),
    ], string="Storage Condition", required=True)
    side_effects = fields.Text(string="Side Effects")
    dosage = fields.Char(string="Dosage")
    license_category = fields.Selection([
        ('green', '🟢 Pharmacy (Category A) - Full license'),
        ('blue', '🔵 Medical Store (Category B) - Limited license'),
        ('white', '⚪ Drug Store (Category C) - Basic OTC'),
    ], string="Pharmacy License Category", required=True, default='white')
    product_id = fields.Many2one('product.product', string="Linked Product", readonly=True)
    last_sale_order_id = fields.Many2one('sale.order', string="Last Sale Order", readonly=True)
    last_invoice_id = fields.Many2one('account.move', string="Last Invoice", readonly=True)
    today_orders_qty = fields.Float(string="Today Orders", compute="_compute_today_orders", store=False)

    # Cart fields (computed from user cart data)
    cart_quantity = fields.Integer(string="Cart Quantity", compute="_compute_cart_fields")
    cart_subtotal = fields.Float(string="Cart Subtotal", compute="_compute_cart_fields")
    cart_item_ids = fields.Many2many('pharmacy.medicine', compute="_compute_cart_item_ids")
    cart_total = fields.Float(string="Cart Total", compute="_compute_cart_total")

    # ------------------------------------------------------------
    # Cart helper methods
    # ------------------------------------------------------------
    def _get_cart_dict(self):
        """Return dict {medicine_id: quantity} from user's cart_data"""
        data = self.env.user.cart_data
        if not data:
            return {}
        return json.loads(data)

    def _set_cart_dict(self, cart_dict):
        self.env.user.sudo().write({'cart_data': json.dumps(cart_dict)})

    def _compute_cart_fields(self):
        cart = self._get_cart_dict()
        for med in self:
            qty = cart.get(str(med.id), 0)
            med.cart_quantity = qty
            med.cart_subtotal = qty * med.price

    def _compute_cart_item_ids(self):
        cart = self._get_cart_dict()
        self.cart_item_ids = self.browse([int(k) for k in cart.keys()])

    def _compute_cart_total(self):
        cart = self._get_cart_dict()
        total = 0.0
        for med_id, qty in cart.items():
            med = self.browse(int(med_id))
            total += med.price * qty
        self.cart_total = total

    # ------------------------------------------------------------
    # Cart actions
    # ------------------------------------------------------------
    def add_to_cart(self):
        self.ensure_one()
        if self.order_qty <= 0:
            raise UserError(_("Quantity must be greater than zero"))
        if self.order_qty > self.quantity:
            raise UserError(_("Not enough stock. Available: %s") % self.quantity)

        cart = self._get_cart_dict()
        key = str(self.id)
        cart[key] = cart.get(key, 0) + self.order_qty
        self._set_cart_dict(cart)
        self.order_qty = 1
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Added to Cart'),
                'message': _("Added %s to your cart.") % self.name,
                'type': 'success',
                'sticky': False,
            }
        }

    def remove_from_cart(self):
        self.ensure_one()
        cart = self._get_cart_dict()
        key = str(self.id)
        if key in cart:
            del cart[key]
            self._set_cart_dict(cart)
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def checkout(self):
        cart = self._get_cart_dict()
        if not cart:
            raise UserError(_("Your cart is empty."))
        order_lines = []
        for med_id, qty in cart.items():
            med = self.browse(int(med_id))
            if not med.product_id:
                med._create_product()
            order_lines.append((0, 0, {
                'product_id': med.product_id.id,
                'product_uom_qty': qty,
                'price_unit': med.price,
            }))
        sale_order = self.env['sale.order'].create({
            'partner_id': self.env.user.partner_id.id,
            'order_line': order_lines,
        })
        sale_order.action_confirm()
        invoice = sale_order._create_invoices()
        invoice.action_post()

        for med_id, qty in cart.items():
            med = self.browse(int(med_id))
            med.quantity -= qty

        self._set_cart_dict({})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'new',
        }

    # ------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------
    def _create_product(self):
        product = self.env['product.product'].create({
            'name': self.name,
            'list_price': self.price,
            'standard_price': self.cost_price or 0.0,
            'type': 'consu',
            'sale_ok': True,
            'purchase_ok': False,
        })
        self.product_id = product
        return product

    # ------------------------------------------------------------
    # Compute methods (unchanged)
    # ------------------------------------------------------------
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

    @api.depends('product_id')
    def _compute_today_orders(self):
        today_start = datetime.now().replace(hour=0, minute=0, second=0)
        today_end = today_start + timedelta(days=1)
        for med in self:
            total = 0.0
            if med.product_id:
                lines = self.env['sale.order.line'].search([
                    ('product_id', '=', med.product_id.id),
                    ('order_id.date_order', '>=', today_start),
                    ('order_id.date_order', '<', today_end),
                    ('order_id.state', 'not in', ['cancel'])
                ])
                total = sum(lines.mapped('product_uom_qty'))
            med.today_orders_qty = total