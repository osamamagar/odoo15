from odoo import fields , models

class HMS_Doctor(models.Model):
    _name = 'hms.doctor'
    _rec_name = 'first_name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Image()