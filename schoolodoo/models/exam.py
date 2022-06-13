# -*- coding: utf-8 -*-

from odoo import fields, models


class Exam(models.Model):

    _name = "schoolodoo.exam"
    _description = "Exams for student"

    name = fields.Char('Examination Name')
    student_id = fields.Many2one("schoolodoo.student", string="Student Name")
    subject_id = fields.Many2one("schoolodoo.subject", string="Subject")
    student_marks = fields.Integer("Marks")



