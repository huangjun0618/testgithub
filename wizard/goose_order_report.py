# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class Account_Report_Extend(models.TransientModel):
    _name = "goose.report.wizard"
    _description = "goose report wizard"

    def _onchange_client_bh(self, client_bh):
        res = {}
        for record in self.env['goose.client'].search([('code', '=', client_bh)]):
            res['client_id'] = record.id
            return {'value': res}

    def _domain_yewu(self):
        return [('department_id', '=', self.env['hr.department'].search([('name', '=', u'销售部')]).id)]

    def _get_year(self):
        year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
        return '{}-01-01'.format(year)

    client_bh = fields.Char(u'客户编号', related='client_id.code')
    client_id = fields.Many2one('goose.client', string=u'公司名称')
    yewu = fields.Many2one('hr.employee', u'业务员', domain=_domain_yewu)
    year = fields.Date(u'年份', default=_get_year)
    date_from = fields.Selection([
        ('01', u'一月'),
        ('02', u'二月'),
        ('03', u'三月'),
        ('04', u'四月'),
        ('05', u'五月'),
        ('06', u'六月'),
        ('07', u'七月'),
        ('08', u'八月'),
        ('09', u'九月'),
        ('10', u'十月'),
        ('11', u'十一月'),
        ('12', u'十二月')
    ], u'开始时间')
    date_to = fields.Selection([
        ('01', u'一月'),
        ('02', u'二月'),
        ('03', u'三月'),
        ('04', u'四月'),
        ('05', u'五月'),
        ('06', u'六月'),
        ('07', u'七月'),
        ('08', u'八月'),
        ('09', u'九月'),
        ('10', u'十月'),
        ('11', u'十一月'),
        ('12', u'十二月')
    ], u'结束时间')
    sorted_by = fields.Selection([('month', u'按月份'),
                                  ('people', u'按单个业务员'),
                                  ('all', u'按所有业务员'),
                                  ], string=u'查询分类', required=True, default='month')
    result_selection = fields.Selection([('customer', '应收账款'),
                                         ('supplier', '应付账款')
                                         ], string="账款类型", required=True, default='customer')
    amount_currency = fields.Boolean("With Currency",
                                     help="It adds the currency column on report if the currency differs from the company currency.")

    def _build_contexts(self, data):
        result = {}
        # result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['yewu'] = data['form']['yewu'] or False
        result['result_selection'] = data['form']['result_selection'] or False
        return result

    def pre_print_report(self, data):
        data['form'].update(self.read(['result_selection'])[0])
        return data

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'amount_currency': self.amount_currency})
        return self.env['report'].get_action(self, 'goose.my_report', data=data)

    @api.multi
    def but_print(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'sorted_by', 'yewu', 'year', 'result_selection'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        return self._print_report(data)


class Account_Report_Extend_Yewu(models.TransientModel):
    _name = "goose.report.wizard.yewu"
    _description = "goose report wizard"

    def _onchange_client_bh(self, client_bh):
        res = {}
        for record in self.env['goose.client'].search([('code', '=', client_bh)]):
            res['client_id'] = record.id
            return {'value': res}

    def _domain_yewu(self):
        return [('department_id', '=', self.env['hr.department'].search([('name', '=', u'销售部')]).id)]

    def _get_year(self):
        year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
        return '{}-01-01'.format(year)

    client_bh = fields.Char(u'客户编号', related='client_id.code')
    client_id = fields.Many2one('goose.client', string=u'公司名称')
    yewu = fields.Many2one('hr.employee', u'业务员', domain=_domain_yewu)
    year = fields.Date(u'年份', default=_get_year)
    date_from = fields.Selection([
        ('01', u'一月'),
        ('02', u'二月'),
        ('03', u'三月'),
        ('04', u'四月'),
        ('05', u'五月'),
        ('06', u'六月'),
        ('07', u'七月'),
        ('08', u'八月'),
        ('09', u'九月'),
        ('10', u'十月'),
        ('11', u'十一月'),
        ('12', u'十二月')
    ], u'开始时间')
    date_to = fields.Selection([
        ('01', u'一月'),
        ('02', u'二月'),
        ('03', u'三月'),
        ('04', u'四月'),
        ('05', u'五月'),
        ('06', u'六月'),
        ('07', u'七月'),
        ('08', u'八月'),
        ('09', u'九月'),
        ('10', u'十月'),
        ('11', u'十一月'),
        ('12', u'十二月')
    ], u'结束时间')
    sorted_by = fields.Selection([('month', u'按月份'),
                                  ('people', u'按单个业务员'),
                                  ('all', u'按所有业务员'),
                                  ], string=u'查询分类', required=True, default='month')
    result_selection = fields.Selection([('customer', '应收账款'),
                                         ('supplier', '应付账款')
                                         ], string="账款类型", default='customer')
    amount_currency = fields.Boolean("With Currency",
                                     help="It adds the currency column on report if the currency differs from the company currency.")

    def _build_contexts(self, data):
        result = {}
        # result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['yewu'] = data['form']['yewu'] or False
        result['result_selection'] = data['form']['result_selection'] or False
        return result

    def pre_print_report(self, data):
        data['form'].update(self.read(['result_selection'])[0])
        return data

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'amount_currency': self.amount_currency})
        return self.env['report'].get_action(self, 'goose.my_report_yewu', data=data)

    @api.multi
    def but_print(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'sorted_by', 'yewu', 'year', 'result_selection'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        return self._print_report(data)


class Account_Report_wj_Extend(models.TransientModel):
    _name = "goose.report.wj.wizard"
    _description = "goose report wj wizard"

    def _get_year(self):
        year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
        return '{}-01-01'.format(year)

    year = fields.Date(u'年份', default=_get_year)
    date_from = fields.Selection([
        ('01', u'一月'),
        ('02', u'二月'),
        ('03', u'三月'),
        ('04', u'四月'),
        ('05', u'五月'),
        ('06', u'六月'),
        ('07', u'七月'),
        ('08', u'八月'),
        ('09', u'九月'),
        ('10', u'十月'),
        ('11', u'十一月'),
        ('12', u'十二月')
    ], u'开始时间')
    date_to = fields.Selection([
        ('01', u'一月'),
        ('02', u'二月'),
        ('03', u'三月'),
        ('04', u'四月'),
        ('05', u'五月'),
        ('06', u'六月'),
        ('07', u'七月'),
        ('08', u'八月'),
        ('09', u'九月'),
        ('10', u'十月'),
        ('11', u'十一月'),
        ('12', u'十二月')
    ], u'结束时间')
    result_selection = fields.Selection([('kucun', '库存报表'),
                                         ('lingyong', '领用报表')
                                         ], string="报表类型", required=True)

    def _build_contexts(self, data):
        result = {}
        # result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['result_selection'] = data['form']['result_selection'] or False
        return result

    def pre_print_report(self, data):
        data['form'].update(self.read(['result_selection'])[0])
        return data

    def _print_report(self, data):
        data = self.pre_print_report(data)
        return self.env['report'].get_action(self, 'goose.my_report_wj', data=data)

    @api.multi
    def but_print(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'sorted_by', 'yewu', 'year', 'result_selection'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        return self._print_report(data)


class Account_Report_caigou_Extend(models.TransientModel):
    _name = "goose.caigou.report.wizard"
    _description = "goose caigou report wj wizard"

    @api.multi
    def but_print(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form']={}
        data['form']['used_context'] = dict(lang=self.env.context.get('lang', 'en_US'))
        return self.env['report'].get_action(self, 'goose.my_report_caigou',data=data)


class Account_Report_caigouJl_Extend(models.TransientModel):
    _name = "goose.caigoujl.report.wizard"
    _description = "goose caigou report wj wizard"

    @api.multi
    def but_print(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = {}
        data['form']['used_context'] = dict(lang=self.env.context.get('lang', 'en_US'))
        return self.env['report'].get_action(self, 'goose.my_report_caigou_jl',data=data)

class Account_Report_Jx_Extend(models.TransientModel):
    _name = "goose.jx.report.wizard"
    _description = "goose jx report wizard"

    @api.multi
    def but_print(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = {}
        data['form']['used_context'] = dict(lang=self.env.context.get('lang', 'en_US'))
        return self.env['report'].get_action(self, 'goose.my_report_jx',data=data)
