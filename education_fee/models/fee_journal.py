# -*- coding: utf-8 -*-


from odoo import models, fields, api, _


class InheritJournal(models.Model):
    _inherit = 'account.journal'

    is_fee = fields.Boolean('Is Educational fee?', default=False)

    @api.multi
    def action_create_new_fee(self):
        view = self.env.ref('education_fee.receipt_form')
        ctx = self._context.copy()
        ctx.update({'journal_id': self.id, 'default_journal_id': self.id})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'res_model': 'account.invoice',
            'view_id': view.id,
            'context': ctx,
            'type': 'ir.actions.act_window',
        }
