# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SchoolTeacher(models.Model):

    _inherit = "hr.employee"

    class_ids = fields.Many2many('schoolodoo.level', string="Class")
    subject_ids = fields.Many2many('schoolodoo.subject', string="Subject")

