from odoo import fields , models, api
from odoo.exceptions import  ValidationError
import re
from datetime import date

class HMS_Patient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'first_name'

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'This E-mail Already Exist')
    ]

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([('A', 'A'),('B', 'B'),('O', 'O'),('AB','AB'),('AO','AO'),('BO','BO')])
    states = fields.Selection([('Undetermined','Undetermined'),('Good','Good'),('Fair','Fair'),('Serious','Serious')], default = 'Undetermined')
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer(compute = '_compute_age')
    department_id = fields.Many2one('hms.department')
    capacity = fields.Integer(related='department_id.capacity')
    doctor_ids = fields.Many2many('hms.doctor')
    logs = fields.One2many('hms.patient.log','patient_id')
    email = fields.Char()


    @api.onchange('age')
    def check_pcr(self):
        if self.age < 30 and self.age != 0:
            self.pcr = True
            return {
                'warning': {
                    'title': ('PCR'),
                    'message': 'PCR was Checked'
                }
            }
        else:
            self.pcr = False
    
    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - (
                        (today.month, today.day) < (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 1

    @api.onchange('states')
    def create_state_log(self):
        for record in self:
            vals = {
                'description': 'State Changed To %s' % (record.states),
                'patient_id': record.id
            }
            record.env['hms.patient.log'].create(vals)

    @api.onchange('email')
    def check_email(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError("You Enter Invalid E-mail")
