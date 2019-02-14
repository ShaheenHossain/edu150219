# -*- coding: utf-8 -*-


from odoo import fields, models, api


class ApplicationReject(models.TransientModel):
    _name = 'application.reject'
    _description = 'Choose Reject Reason'

    reject_reason_id = fields.Many2one('application.reject.reason', string="Reason",
                                       help="Select Reason for rejecting the Applications")

    @api.multi
    def action_reject_reason_apply(self):
        """Write the reject reason of the application"""
        for rec in self:
            application = self.env['education.application'].browse(self.env.context.get('active_ids'))
            application.write({'reject_reason': rec.reject_reason_id.id})
            return application.reject_application()


class ApplicationRejectReason(models.Model):
    _name = 'application.reject.reason'
    _description = 'Reject ReasonS'

    name = fields.Char(string="Reason", required=True,
                       help="Possible Reason for rejecting the Applications")
