# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Classlevel(models.Model):

    _name = 'schoolodoo.level'
    _description = 'Student Class'
    _rec_name = 'name'

    student_ids = fields.One2many('schoolodoo.student', 'class_id', string="Class")
    name = fields.Char(string='ClassName')
