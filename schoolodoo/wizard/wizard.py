# -*- coding: utf-8 -*-

from odoo import fields, models

class SchoolWizard(models.TransientModel):
    _name = 'schoolodoo.wizard'
    _description = 'School Wizard'

    select = fields.Selection([('maths', 'Maths'), ('science', 'Science')], string='Select Subject')

    def open_sheet(self):

        if self.select == 'maths':
            return {
                'name': "maths_form",
                'context': {},
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[False, 'form']],
                'res_model': 'schoolodoo.maths',
                'type': 'ir.actions.act_window',
                'target': 'new',
            }





