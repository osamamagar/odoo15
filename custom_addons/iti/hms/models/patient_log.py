from odoo import fields, models

class patient_log(models.Model):
    _name = 'hms.patientlogs'


    description = fields.Text()
    patient_id = fields.Many2one('hms.patient')