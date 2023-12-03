from odoo import fields , models

class HMS_Patient_Log(models.Model):
    _name = 'hms.patient.log'

    description = fields.Char(required=True)
    patient_id = fields.Many2one('hms.patient')