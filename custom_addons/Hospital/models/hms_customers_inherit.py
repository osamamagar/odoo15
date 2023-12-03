from odoo import fields , models, api
from odoo.exceptions import  ValidationError, UserError


class HMS_Customers(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient')

    @api.constrains('related_patient_id')
    def valid_email(self):
        for record in self :
            if record.email == record.related_patient_id.email:
                raise ValidationError('This User Has An Email That Is Already Assigned To A Customer')
        
    def unlink(self):
        for record in self :
            if record.related_patient_id:
                raise UserError('This Customer Is Linked To A Patient')