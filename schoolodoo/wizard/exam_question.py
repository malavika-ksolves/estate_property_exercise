# -*- coding: utf-8 -*-

from odoo import fields, models

class Question(models.TransientModel):
    _name = 'schoolodoo.maths'
    _description = 'School Wizard Maths'

    question1 = fields.Char(string='Question1')
    question2 = fields.Char(string='Question2')
    question3 = fields.Char(string='Question3')
    question4 = fields.Char(string='Question4')









