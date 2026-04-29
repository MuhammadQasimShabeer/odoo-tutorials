from odoo import models, fields, api
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

    # Patient statistics (optional – you can keep or remove)
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
        readonly=True  # because list is read‑only
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

            # Patient stats (optional)
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
        """Compute the patient list based on user's role."""
        Patient = self.env['pharmacy.patient']
        for record in self:
            if self.env.user.has_group('pharma_control_center.group_pharmacy_doctor'):
                # Doctor: see only patients assigned to them
                record.patient_ids = Patient.search([('doctor_id', '=', self.env.user.id)])
            elif self.env.user.has_group('pharma_control_center.group_pharmacy_manager'):
                # Manager: see all patients
                record.patient_ids = Patient.search([])
            else:
                # Others (Patients, etc.) see no patient list
                record.patient_ids = False