
from odoo import models, fields
class doctors(models.Model):
    _name = 'hms.doctors'

    firstName = fields.Char(required=True)
    lastName = fields.Char(required=True)
    image = fields.Image()
    departments = fields.Many2many('hms.department', string='Departments')