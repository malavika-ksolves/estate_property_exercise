# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Subject(models.Model):

    _name = 'schoolodoo.subject'
    _description = 'Subjects selected by students'
    _rec_name = 'name'

    name = fields.Char('Name')




