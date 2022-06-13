# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Student(models.Model):

    _name = 'schoolodoo.student'
    _description = 'Student Details'
    _order = 'first_name'
    _rec_name = 'first_name'

    first_name = fields.Char('First Name', required=True)
    last_name = fields.Char('Last Name', required=True)
    age = fields.Integer('Age', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    student_dob = fields.Date('Date of Birth')
    phone_number = fields.Char(string='Mobile Number', required=True)
    address = fields.Char(string='Address', required=True)

    subject_ids = fields.Many2many('schoolodoo.subject', string="List of Subjects")
    class_id = fields.Many2one('schoolodoo.level', "Class")
    amount_ids = fields.One2many('schoolodoo.fees', 'student_id', string='FeeAmount')


    def exam_form(self):

        return {
            'name': "exam_form",
            'context': {},
            'view_type': 'form',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'res_model': 'schoolodoo.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
