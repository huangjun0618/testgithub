# -*- coding: utf-8 -*-
##############################################################################
# OpenERP Connector
# Copyright 2013 Amos <sale@100china.cn>
##############################################################################


from odoo import fields, models, api, _
from odoo.exceptions import UserError


class sale_contract_wizard(models.TransientModel):
    _name = "sale.contract.wizard"
    _description = "sale contract wizard"

    text = fields.Text(u'审批意见', )

    def but_yes(self):
        obj = self.env[self.env.context['active_model']]
        instructors = obj.browse(self.env.context['active_id'])
        instructors.write({'state': 'done'})

    def but_no(self):
        obj = self.env[self.env.context['active_model']]
        instructors = obj.browse(self.env.context['active_id'])
        instructors.write({'state': 'badending'})
