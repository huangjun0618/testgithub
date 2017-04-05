# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleContractReport(models.AbstractModel):
    _name = 'report.goose.report_salecontract'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('goose.report_salecontract')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        print docargs
        return report_obj.render('goose.report_salecontract', docargs)

# class SaleProduceReport(models.AbstractModel):
#     _name = 'report.goose.report_saleproduce'
#
#     @api.model
#     def render_html(self, docids, data=None):
#         report_obj = self.env['report']
#         report = report_obj._get_report_from_name('goose.report_saleproduce')
#         docargs = {
#             'doc_ids': docids,
#             'doc_model': report.model,
#             'docs': self,
#         }
#         return report_obj.render('goose.report_saleproduce', docargs)


