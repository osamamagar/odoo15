from dateutil.relativedelta import relativedelta
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import  datetime
class patient(models.Model):
    _name = 'hms.patient'
    _description = 'patient module'

    firstName = fields.Char(required=True)
    lastName = fields.Char()
    birthDate = fields.Date(default='1980-09-15')
    history = fields.Text()
    CR_Ratio = fields.Float(required=False)
    bloodType = fields.Selection([('A','A'),('B','B'),('O','O'),('AB','AB')], default= 'A')
    PCR = fields.Boolean()
    image = fields.Image()
    address = fields.Char()
    age = fields.Integer(compute='setage',store='True',readonly=True)
    department_id = fields.Many2one('hms.department', domain="[('is_opened', '=', True)]")
    department_capacity = fields.Integer(related='department_id.capacity')
    states = fields.Selection([('Undetermined','Undetermined'),('Good','Good'),('Fair','Fair'),('Serious','Serious')], default='Undetermined')
    doctors_id = fields.Many2many('hms.doctors',string='Doctors')
    email = fields.Char()
    patient_logs = fields.One2many('hms.patientlogs','patient_id')

    customer_id = fields.One2many('res.partner',inverse_name='related_patient_id')

    _sql_constraints = [('uniquemail','UNIQUE(email)','This is email is already registered !')]

    @api.onchange('states')
    def states_changed(self):
        for record in self:
            data = {
            "description": "state changed to %s" %{record.states},
                "patient_id": record.id
            }
            record.env['hms.patientlogs'].create(data)
    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30:
            self.PCR = True
            return {'warning': {'title': 'Warning', 'message': 'The PCR field has been automatically checked because age is lower than 30.'}}
    def set_undetermined(self):
        self.states = 'Undetermined'
    def set_good(self):
        self.states = 'Good'
    def set_fair(self):
        self.states = 'Fair'
    def set_serious(self):
        self.states = 'Serious'

    @api.depends('birthDate')
    def setage(self):
        for record in self:
            today = datetime.today().date()
            record.age = relativedelta(today, record.birthDate).years

    @api.onchange('email')
    def check_mail(self):
        emailreg = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
        if self.email and not re.match(emailreg, self.email):
            return {
                'warning': {
                    'title': "Invalid Email",
                    'message': "Please enter a valid email address.",
                }
            }






