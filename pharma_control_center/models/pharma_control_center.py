from odoo import models, fields, api, _
from datetime import date, timedelta

class PharmaControlCenter(models.Model):
    _name = "pharma.control.center"
    _description = "Pharma Control Center"

    name = fields.Char(string="Name", required=True, default="Pharmacy Dashboard")
    description = fields.Text(string="Description")
    last_updated = fields.Datetime(string="Last Updated", default=fields.Datetime.now)

    # Medicine statistics
    total_medicines = fields.Integer(
        string="Total Medicines", compute="_compute_statistics", store=False
    )
    total_stock_quantity = fields.Integer(
        string="Total Stock Quantity", compute="_compute_statistics", store=False
    )
    stock_value = fields.Float(
        string="Stock Value", compute="_compute_statistics", store=False
    )
    out_of_stock_count = fields.Integer(
        string="Out of Stock Medicines", compute="_compute_statistics", store=False
    )
    low_stock_count = fields.Integer(
        string="Low Stock (< 10 units)", compute="_compute_statistics", store=False
    )
    expiring_soon_count = fields.Integer(
        string="Expiring Within 30 Days", compute="_compute_statistics", store=False
    )
    expired_count = fields.Integer(
        string="Expired Medicines", compute="_compute_statistics", store=False
    )

    # Patient statistics
    total_patients = fields.Integer(
        string="Total Patients", compute="_compute_statistics", store=False
    )
    my_patients = fields.Integer(
        string="My Patients", compute="_compute_statistics", store=False
    )
    patient_ids = fields.One2many(
        'pharmacy.patient',
        string="Patients",
        compute='_compute_patient_ids',
        readonly=True
    )

    # Today's orders summary
    today_order_total_qty = fields.Float(
        string="Total Quantity Today",
        compute="_compute_today_orders_summary",
        store=False
    )
    today_order_total_amount = fields.Float(
        string="Total Sales Today",
        compute="_compute_today_orders_summary",
        store=False
    )

    @api.depends()
    def _compute_statistics(self):
        Medicine = self.env['pharmacy.medicine']
        Patient = self.env['pharmacy.patient']
        today = date.today()
        thirty_days_later = today + timedelta(days=30)

        for record in self:
            # Medicine stats
            all_meds = Medicine.search([])
            record.total_medicines = len(all_meds)
            record.total_stock_quantity = sum(med.quantity for med in all_meds)
            record.stock_value = sum(med.quantity * med.price for med in all_meds)
            record.out_of_stock_count = sum(1 for med in all_meds if med.quantity == 0)
            record.low_stock_count = sum(1 for med in all_meds if 0 < med.quantity < 10)
            record.expiring_soon_count = sum(
                1 for med in all_meds
                if med.expiry_date and med.expiry_date <= thirty_days_later and med.expiry_date > today
            )
            record.expired_count = sum(
                1 for med in all_meds if med.expiry_date and med.expiry_date < today
            )

            # Patient stats
            if Patient:
                record.total_patients = Patient.search_count([])
                if self.env.user.has_group('pharma_control_center.group_pharmacy_doctor'):
                    record.my_patients = Patient.search_count([('doctor_id', '=', self.env.user.id)])
                else:
                    record.my_patients = 0
            else:
                record.total_patients = 0
                record.my_patients = 0

    @api.depends()
    def _compute_patient_ids(self):
        Patient = self.env['pharmacy.patient']
        for record in self:
            if self.env.user.has_group('pharma_control_center.group_pharmacy_doctor'):
                record.patient_ids = Patient.search([('doctor_id', '=', self.env.user.id)])
            elif self.env.user.has_group('pharma_control_center.group_pharmacy_manager'):
                record.patient_ids = Patient.search([])
            else:
                record.patient_ids = False

    @api.depends()
    def _compute_today_orders_summary(self):
        """Compute total quantity and amount for today's orders.
        Non‑managers see only their own orders."""
        today = fields.Date.today()
        tomorrow = today + timedelta(days=1)
        domain = [
            ('order_id.date_order', '>=', today),
            ('order_id.date_order', '<', tomorrow),
            ('order_id.state', 'not in', ['cancel'])
        ]
        if not self.env.user.has_group('pharma_control_center.group_pharmacy_manager'):
            domain.append(('create_uid', '=', self.env.user.id))
        order_lines = self.env['sale.order.line'].search(domain)
        self.today_order_total_qty = sum(order_lines.mapped('product_uom_qty'))
        self.today_order_total_amount = sum(order_lines.mapped('price_subtotal'))

    def action_view_today_orders(self):
        """Open a list of today's order lines."""
        today = fields.Date.today()
        tomorrow = today + timedelta(days=1)
        domain = [
            ('order_id.date_order', '>=', today),
            ('order_id.date_order', '<', tomorrow),
            ('order_id.state', 'not in', ['cancel'])
        ]
        if not self.env.user.has_group('pharma_control_center.group_pharmacy_manager'):
            domain.append(('create_uid', '=', self.env.user.id))

        # Use the custom view
        view = self.env.ref('pharma_control_center.view_sale_order_line_today_list', raise_if_not_found=False)
        view_id = view.id if view else False
        return {
            'type': 'ir.actions.act_window',
            'name': "Today's Orders",
            'res_model': 'sale.order.line',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': domain,
            'views': [(view_id, 'list')] if view_id else [(False, 'list')],
        }