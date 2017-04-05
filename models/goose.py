# -*- coding: utf-8 -*-
from odoo import models, api, fields
from odoo.exceptions import UserError
import datetime
import time


class GooseClient(models.Model):
    _name = 'goose.client'

    # @api.multi
    # def read(self, fields=None, load='_classic_read'):
    #     if self.user_has_groups('goose.group_goose_user'):
    #         self = self.env['goose.client'].search(
    #             [('yewu', '=', self.env['hr.employee'].search([('user_id', '=', self.env.uid)]).id)])
    #     return super(GooseClient, self).read()

    code = fields.Char(u'客户编号', required=True)
    jiancheng = fields.Char(u'客户简称')
    faren = fields.Char(u'法人代表')
    name = fields.Char(u'中文名称', required=True)
    new_or_not = fields.Selection([('new', u'新客户'), ('old', u'老客户'), ], u'新老客户', default="new")
    name_en = fields.Char(u'英文名称')

    def _domain_yewu(self):
        return [('department_id', '=', self.env['hr.department'].search([('name', '=', u'销售部')]).id)]

    def _get_yewu(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)]).id

    # @api.multi
    # def get_zhangmian(self):
    #     zhangmian = 0
    #     records = self.env['goose.order'].search([('client_id', '=', self.env.uid)])
    #     for record in records:
    #         zhangmian += record.amount - record.kaipiao - record.bukaipiao
    #     print zhangmian
    #     return zhangmian

    yewu = fields.Many2one('hr.employee', u'业务员', required=True, domain=_domain_yewu, default=_get_yewu)
    yewu_code = fields.Char(u'业务员编号', related='yewu.code')
    registered_capital = fields.Char(u'注册资本')
    registered_date = fields.Char(u'注册日期')
    registered_address = fields.Char(u'注册地址')
    business_license = fields.Char(u'营业执照')
    business_mode = fields.Char(u'经营方式')
    zip_code = fields.Char(u'邮政编码')
    hand_phone = fields.Char(u'手机')
    phone = fields.Char(u'电话')
    fax = fields.Char(u'传真')
    company_website = fields.Char(u'公司网址')
    e_mail = fields.Char(u'电子邮箱')
    company_account = fields.Char(u'企业账号')
    company_tax_number = fields.Char(u'企业税号')
    bank_account = fields.Char(u'开户银行')
    payment_method = fields.Char(u'付款方式')
    credit_quota = fields.Float(u'授信额度', default=0.000)
    is_partner = fields.Boolean(u'贸易伙伴', default=True)
    contacts = fields.One2many('goose.contacts', 'contacts_id', u'联系人')
    delivery_address = fields.Char(u'送货地址')

    user_id = fields.Many2one('res.users',u'关联用户',related='yewu.user_id')

    # zhangmian = fields.Float(u'账面', default=0, compute=get_zhangmian, store=True)
    # bukaipiao = fields.Float(u'不开票', default=0)
    # weikaipiao = fields.Float(u'未开票', default=0)

    _sql_constraints = [
        ('goose_client_code', 'unique (code)', "客户编号必须唯一"),
    ]


class GooseSupplier(models.Model):
    _name = 'goose.supplier'

    code = fields.Char(u'供应商编号', required=True)
    jiancheng = fields.Char(u'供应商')
    faren = fields.Char(u'法人代表')
    name = fields.Char(u'中文名称', required=True)
    name_en = fields.Char(u'英文名称')
    registered_capital = fields.Char(u'注册资本')
    registered_date = fields.Char(u'注册日期')
    registered_address = fields.Char(u'注册地址')
    business_license = fields.Char(u'营业执照')
    business_mode = fields.Char(u'经营方式')
    zip_code = fields.Char(u'邮政编码')
    hand_phone = fields.Char(u'手机')
    phone = fields.Char(u'电话')
    fax = fields.Char(u'传真')
    company_website = fields.Char(u'公司网址')
    e_mail = fields.Char(u'电子邮箱')
    company_account = fields.Char(u'企业账号')
    company_tax_number = fields.Char(u'企业税号')
    bank_account = fields.Char(u'开户银行')
    contacts = fields.One2many('goose.contacts', 'contacts_id', u'联系人')
    yuer = fields.Float(u'应付余额')

    _sql_constraints = [
        ('goose_supplier_code', 'unique (code)', "供应商编号必须唯一"),
    ]


class GooseProduct(models.Model):
    _name = 'goose.product'

    def _default_uom(self):
        return self.env['product.uom'].search([('name', '=', 'kg')])

    name = fields.Char(u'中文名称', required=True)
    category = fields.Many2one('goose.category', u'类别')
    code = fields.Char(u'产品编号')
    name_en = fields.Char(u'产品英文名称')
    detail = fields.Text(u'产品描述')
    product_uom = fields.Many2one('product.uom', u'单位', default=_default_uom)

    _sql_constraints = [
        ('goose_product_code', 'unique (code)', "产品编号必须唯一"),
    ]


class GooseProductWuliao(models.Model):
    _name = 'goose.product.wuliao'

    name = fields.Char(u'中文名称', required=True)
    sort = fields.Char(u'物料分类', required=True)
    category = fields.Many2one('goose.category.wuliao', u'类别名称')
    code = fields.Char(u'物料编号')
    format = fields.Many2one('goose.format', u'物料规格')
    detail = fields.Char(u'物料描述')
    kuwei = fields.Char(u'库位')
    min_stock = fields.Float(u'单价', default=0.0)
    stock = fields.Float(u'库存', default=0.0)

    _sql_constraints = [
        ('goose_product_code', 'unique (code)', "产品编号必须唯一"),
    ]


class GooseProductYuanliao(models.Model):
    _name = 'goose.product.yuanliao'

    name = fields.Char(u'中文名称', required=True)
    category = fields.Many2one('goose.category', u'类别')
    code = fields.Char(u'原料编号')
    name_en = fields.Char(u'原料英文名称')
    detail = fields.Char(u'原料描述')

    _sql_constraints = [
        ('goose_product_code', 'unique (code)', "产品编号必须唯一"),
    ]


class GooseCategory(models.Model):
    _name = 'goose.category'


    name = fields.Char(u'类别名称')


class GooseFormat(models.Model):
    _name = 'goose.format'

    name = fields.Char(u'物料规格')


class SaleContract(models.Model):
    _name = 'sale.contract'
    _order = 'name desc'

    # @api.multi
    # def read(self, fields=None, load='_classic_read'):
    #     if self.user_has_groups('goose.group_goose_user'):
    #         self = self.env['sale.contract'].search(
    #             [('yewu', '=', self.env['hr.employee'].search([('user_id', '=', self.env.uid)]).id)])
    #     return super(SaleContract, self).read()

    @api.multi
    @api.depends('sale_contract_line.price_unit', 'sale_contract_line.product_uom_qty')
    def _amount_all(self):
        for order in self:
            amount_total = 0.0
            for line in order.sale_contract_line:
                amount_total += line.price_unit * line.product_uom_qty
            order.update({
                'amount_total': amount_total,
            })

    @api.multi
    @api.depends('sale_contract_line.price_unit', 'sale_contract_line.product_uom_qty')
    def _Num2MoneyFormat(self):
        for order in self:
            amount_total = 0.0
            for line in order.sale_contract_line:
                amount_total += line.price_unit * line.product_uom_qty
            change_number = amount_total
        format_word = ["分", "角", "元",
                       "拾", "佰", "仟", "万",
                       "拾", "佰", "仟", "亿",
                       "拾", "佰", "仟", "万",
                       "拾", "佰", "仟", "兆"]

        format_num = ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"]
        if type(change_number) == float:
            real_numbers = []
            for i in range(len(format_word) - 3, -3, -1):
                if change_number >= 10 ** i or i < 1:
                    real_numbers.append(int(round(change_number / (10 ** i), 2) % 10))

        elif isinstance(change_number, (int, long)):
            real_numbers = [int(i) for i in str(change_number) + '00']

        else:
            raise ValueError, '%s   can\'t change' % change_number

        zflag = 0
        start = len(real_numbers) - 3
        change_words = []
        for i in range(start, -3, -1):
            if 0 <> real_numbers[start - i] or len(change_words) == 0:
                if zflag:
                    change_words.append(format_num[0])
                    zflag = 0
                change_words.append(format_num[real_numbers[start - i]])
                change_words.append(format_word[i + 2])

            elif 0 == i or (0 == i % 4 and zflag < 3):
                change_words.append(format_word[i + 2])
                zflag = 0
            else:
                zflag += 1

        if change_words[-1] not in (format_word[0], format_word[1]):
            change_words.append("整")
            self.big_amount_total = ''.join(change_words)

    @api.depends('sale_contract_line.standard')
    def _default_standard(self):
        name = []
        for record in self.sale_contract_line:
            for x in record.standard:
                if name.count(x.standard) == 0 and name.count(x.standard) == 0:
                    if name == []:
                        name.append(x.standard)
                    else:
                        name.append(',' + x.standard)
                    z = ''
                    for n in name[0:name.__len__()]:
                        z = z + n
                    self.standard_value = z
                else:
                    pass

    @api.multi
    def _print_contract(self):
        return self.env['report'].get_action(self, 'goose.report_salecontract')

    def _domain_danbao(self):
        return [('create_uid', '=', self.env.uid)]

    @api.onchange('partner_id')
    def onchange_partner(self):
        self.yewu = self.partner_id.yewu.id

    company_id = fields.Many2one('goose.supplier', u'供方')
    name = fields.Char(u'合同编号', default=lambda self: self.env['ir.sequence'].next_by_code('sale.price.contract'))
    partner_id = fields.Many2one('goose.client', u'需方')
    contract_date = fields.Date(u'签订日期')
    user_id = fields.Many2one('res.users',u'关联用户',related='yewu.user_id')
    # fahuo = fields.Float(u'已发货')
    # shoukuan = fields.Float(u'已收款')

    def _domain_yewu(self):
        return [('department_id', '=', self.env['hr.department'].search([('name', '=', '销售部')]).id)]

    yewu = fields.Many2one('hr.employee', u'业务员', domain=_domain_yewu)
    sale_contract_line = fields.One2many('sale.contract.line', 'contract_id', string='产品信息', ondelete="restrict",
                                         copy=True,
                                         states={'cancel': [('readonly', True)], 'done': [('readonly', True)],
                                                 'review': [('readonly', True)],
                                                 'badending': [('readonly', True)]})
    danbao = fields.Many2one('sale.contract.danbao', u'担保方', domain=_domain_danbao)
    amount_total = fields.Monetary(string='合计', store=True,  compute='_amount_all',
                                  )
    big_amount_total = fields.Char(u'合计人民币金额（大写）',  compute='_Num2MoneyFormat',
                                   store=True)
    currency_id = fields.Many2one('res.currency', index=True,
                                  default=lambda self: self.env['res.currency'].search([('symbol', '=', 'CNY')]))

    standard_value = fields.Char(compute='_default_standard', store=True, track_visibility='always')
    rule3 = fields.Char(default='嘉善。由供方代送置需方仓库。', store=True)
    rule4 = fields.Char(default='汽运，运费已包含在单价内。', store=True)
    rule5 = fields.Char(default='包装袋包装，用后回收。', store=True)
    rule6 = fields.Char(default='货到需方仓库后，由供需双方共同取样，由需方自验或送权威机构检验，检验合格后使用。', store=True)
    rule7 = fields.Char(default='供方交货 1 0 天内书面提议', store=True)
    rule8 = fields.Char(default='合同签订后****年**月**日前预付    %货款，在每批送货后    天内扣除相应的预付款后按批付清余下的    %货款。', store=True)
    rule9 = fields.Char(default='按《合同法》。', store=True)
    rule10 = fields.Char(default='友好协商。', store=True)
    rule11 = fields.Text(
        default='1、预付款在约定时间内到账后该合同生效。2、交货时间为****年**月**日前，具体时间及数量以需方传真为准，但必须在****年**月**日前，如超过该时间视为需方放弃该合同余下之羽绒数量。3、本合同打印部分条款对对方具有约束力，不得手写涂改添加，如需手写涂改添加，须在手写涂改添加处双方盖章方为有效。4、以上条款经双方认真阅读后一致认可。与履行本合同有关的协议、合同、传真、订单、信函均为本合同的有效附件，对双方具有约束力。5、担保方担保内容：①范围：本合同货款的本金、利息及实现债权的诉讼费、律师费；②时间：全部货款付清为止。',
        store=True)
    rule12 = fields.Text(store=True)
    state = fields.Selection([('draft', u'草稿'),
                              ('review', u'等待审核'),
                              ('done', u'已通过'),
                              ('cancel', u'取消'),
                              ('badending', u'审核未过')],
                             u'状态', default='draft')

    def sale_contract_review(self):
        self.write({'state': 'review'})

    def sale_contract_cancel(self):
        self.write({'state': 'badending'})

    def sale_contract_draft(self):
        self.write({'state': 'draft'})


class SaleContractLine(models.Model):
    _name = "sale.contract.line"

    @api.onchange('product_id')
    def product_onchange(self):
        self.product_uom = self.product_id.product_uom

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            price = self.price_unit * self.product_uom_qty
            line.update({
                'price_total': price,
            })

    contract_id = fields.Many2one('sale.contract', string=u'合同')
    product_id = fields.Many2one('goose.product', string='品名规格', ondelete='restrict', required=True)
    standard = fields.Many2one('sale.contract.standard', u'标准')
    product_uom = fields.Many2one('product.uom', string=u'计量单位', required=True)
    product_uom_qty = fields.Float(string=u'数量', required=True,
                                   default=0.0)
    price_unit = fields.Float(u'单价', required=True, default=0.0)
    price_total = fields.Float(string=u'总金额', required=True, default=0.0, compute='_compute_amount', store=True)
    details = fields.Char(u'交提货时间及数量')


class SaleContractStandard(models.Model):
    _name = "sale.contract.standard"

    name = fields.Char(u'标准')
    standard = fields.Char(u'标准内容')


class SaleContractDanbao(models.Model):
    _name = "sale.contract.danbao"

    name = fields.Char(u'担保人')
    address = fields.Char(u'地址')
    identify = fields.Char(u'身份证号')
    phone = fields.Char(u'电话')


class GooseOrder(models.Model):
    _name = 'goose.order'

    @api.model
    def create(self, vals):
        res = {}
        res['contract'] = vals['sale_contract']
        res['client'] = vals['client_id']
        res['client_bh'] = vals['client_bh']
        res['yewu'] = self.env['goose.client'].search([('id', '=',vals['client_id'])]).yewu
        res['yewu_code'] = self.env['goose.client'].search([('id', '=', vals['client_id'])]).yewu.code
        res['fahuo'] = vals['qty'] * vals['price']
        res['shoukuan'] = vals['shoukuankaipiao'] + vals['shoukuanbukaipiao']
        res['date'] = vals['order_date']
        res['fhdh'] = vals['madan']
        res['product_id'] = vals['product_id']
        res['qty'] = vals['qty']
        self.env['goose.jxkh'].create(res)
        print vals['madan']
        return super(GooseOrder, self).create(vals)

    @api.multi
    def write(self, vals):
        res = {'kaipiao': 0, 'bukaipiao': 0, 'shoukuankaipiao': 0, 'shoukuanbukaipiao': 0, 'qty': 0, 'price': 0}
        for x in vals:
            res[x] = vals[x]
        for record in self.env['goose.order'].search([('id', '>', self.id), ('client_id', '=', self.client_id.id)]):
            if res['qty']:
                weikaipiao = record.client_wkp - self.qty * self.price + res['qty'] * self.price
                record.write({'client_wkp': weikaipiao})
            if res['price']:
                weikaipiao = record.client_wkp - self.qty * self.price + res['price'] * self.qty
                record.write({'client_wkp': weikaipiao})
            if res['kaipiao']:
                zhangmian = record.client_zm - self.kaipiao + res['kaipiao']
                weikaipiao = record.client_wkp + self.kaipiao - res['kaipiao']
                record.write({'client_zm': zhangmian, 'client_wkp': weikaipiao})
            if res['bukaipiao']:
                bukaipiao = record.client_bkp - self.bukaipiao + res['bukaipiao']
                weikaipiao = record.client_wkp + self.bukaipiao - res['bukaipiao']
                record.write({'client_bkp': bukaipiao, 'client_wkp': weikaipiao})
            if res['shoukuankaipiao']:
                zhangmian = record.client_zm + self.shoukuankaipiao - res['shoukuankaipiao']
                weikaipiao = record.client_wkp - self.shoukuankaipiao + res['shoukuankaipiao']
                record.write({'client_zm': zhangmian, 'client_wkp': weikaipiao})
            if res['shoukuanbukaipiao']:
                bukaipiao = record.client_bkp + self.shoukuanbukaipiao - res['shoukuanbukaipiao']
                weikaipiao = record.client_wkp - self.shoukuanbukaipiao + res['shoukuanbukaipiao']
                record.write({'client_bkp': bukaipiao, 'client_wkp': weikaipiao})
        return super(GooseOrder, self).write(vals)

    def _onchange_client_bh(self, client_bh):
        res = {}
        for record in self.env['goose.client'].search([('code', '=', client_bh)]):
            res['client_id'] = record.id
            return {'value': res}

    def _onchange_client_id(self, client_id, company):
        if client_id != False:
            res = {}
            res['client_bkp'] = 0
            res['client_wkp'] = 0
            res['client_zm'] = 0
            for record in self.env['goose.order'].search(
                    [('client_id', '=', client_id), ('bujiliang', '=', False), ('company', '=', company)]):
                res['client_bkp'] += record.bukaipiao - record.shoukuanbukaipiao
                res['client_wkp'] += record.amount - record.kaipiao - record.bukaipiao
                res['client_zm'] += record.kaipiao - record.shoukuankaipiao
            return {'value': res, 'domain': {'sale_contract': [('partner_id', '=', client_id), ('state', '=', 'done')]}}

    @api.depends('kaipiao', 'shoukuankaipiao', 'client_zm')
    def _get_zhangmian(self):
        for record in self:
            record.zhangmian = record.kaipiao - record.shoukuankaipiao + record.client_zm
            # return {'value':res}

    @api.depends('qty', 'price')
    def _get_amount(self):
        for record in self:
            record.amount = record.qty * record.price

    @api.depends('bukaipiao', 'shoukuanbukaipiao', 'client_bkp')
    def _get_yuerbukaipiao(self):
        for record in self:
            record.yuerbukaipiao = record.bukaipiao - record.shoukuanbukaipiao + record.client_bkp

    @api.depends('amount', 'kaipiao', 'bukaipiao', 'client_wkp')
    def _get_weikaipiao(self):
        for record in self:
            record.weikaipiao = record.amount - record.kaipiao - record.bukaipiao + record.client_wkp

    @api.depends('kaipiao', 'bukaipiao')
    def _get_kphj(self):
        for record in self:
            record.kaipiaoheji = record.kaipiao + record.bukaipiao

    @api.depends('yinhang', 'tiaozheng', 'xianjin')
    def _get_skhj(self):
        for record in self:
            record.shoukuanheji = record.yinhang + record.tiaozheng + record.xianjin

    @api.depends('shoukuankaipiao', 'shoukuanbukaipiao')
    def _get_skphj(self):
        for record in self:
            record.shoukuankaipiaoheji = record.shoukuankaipiao + record.shoukuanbukaipiao

    @api.depends('zhangmian', 'yuerbukaipiao', 'weikaipiao')
    def _get_yehj(self):
        for record in self:
            record.yuerheji = record.zhangmian + record.yuerbukaipiao + record.weikaipiao

    @api.depends('order_date')
    def _get_month(self):
        for record in self:
            record.month = int(record.order_date[0:4]) * 100 + int(record.order_date[5:7])

    @api.depends('client_id')
    def _get_contract(self):
        print self.with_context()
        return [('partner_id', '=', self.client_id)]

    def _onchange_category(self, category):
        return {'domain': {'product_id': [('category', '=', category)]}}

    company = fields.Selection([('ye', u'野鹅'), ('tian', u'天鹅')], u'公司', default='ye')
    order_date = fields.Date(u'录入日期', default=fields.Date.today())
    month = fields.Float(u'录入月份', compute=_get_month, store=True)
    liushui = fields.Char(u'凭证号')
    madan = fields.Char(u'码单号')
    yewu = fields.Many2one('hr.employee',u'业务员', related='client_id.yewu', store=True)
    category = fields.Many2one('goose.category',u'产品名称类别', related='product_id.category')
    product_id = fields.Many2one('goose.product', u'产品名称', ondelete='restrict')
    client_bh = fields.Char(u'客户编号', related='client_id.code')
    client_id = fields.Many2one('goose.client', u'客户名称')
    bujiliang = fields.Boolean(u'不计量')
    qty = fields.Float(u'发货数量')
    price = fields.Float(u'发货单价')
    amount = fields.Float(u'发货金额', compute=_get_amount, store=True)
    kaipiao = fields.Float(u'开票')
    bukaipiao = fields.Float(u'不开票')
    kaipiaoheji = fields.Float(u'合计', compute=_get_kphj)
    yinhang = fields.Float(u'银行')
    tiaozheng = fields.Float(u'调整')
    xianjin = fields.Float(u'现金')
    shoukuanheji = fields.Float(u'合计', compute=_get_skhj)
    shoukuankaipiao = fields.Float(u'开票')
    shoukuanbukaipiao = fields.Float(u'不开票')
    shoukuankaipiaoheji = fields.Float(u'合计', compute=_get_skphj)
    zhangmian = fields.Float(u'账面', compute=_get_zhangmian, store=True)
    yuerbukaipiao = fields.Float(u'不开票', compute=_get_yuerbukaipiao, store=True)
    weikaipiao = fields.Float(u'未开票', compute=_get_weikaipiao, store=True)
    yuerheji = fields.Float(u'合计', compute=_get_yehj)
    beizhu = fields.Text(u'备注')
    sale_contract = fields.Many2one('sale.contract', u'合同', domian=[('state', '=', 'done')])

    client_zm = fields.Float(u'客户账面')
    client_bkp = fields.Float(u'客户不开票')
    client_wkp = fields.Float(u'客户未开票')


class GooseYewuOrder(models.Model):
    _name = 'goose.order.yewu'

    def _onchange_category(self, category):
        return {'domain': {'product_id': [('category', '=', category)]}}

    # @api.multi
    # def read(self, fields=None, load='_classic_read'):
    #     if self.user_has_groups('goose.group_goose_user'):
    #         self = self.env['goose.order.yewu'].search(
    #             [('yewu', '=', self.env['hr.employee'].search([('user_id', '=', self.env.uid)]).id)])
    #     return super(GooseYewuOrder, self).read()

    @api.multi
    def write(self, vals):
        res = {'kaipiao': 0, 'bukaipiao': 0, 'shoukuankaipiao': 0, 'shoukuanbukaipiao': 0, 'qty': 0, 'price': 0}
        for x in vals:
            res[x] = vals[x]
        for record in self.env['goose.order.yewu'].search([('id', '>', self.id), ('client_id', '=', self.client_id.id)]):
            if res['qty']:
                weikaipiao = record.client_wkp - self.qty * self.price + res['qty'] * self.price
                record.write({'client_wkp': weikaipiao})
            if res['price']:
                weikaipiao = record.client_wkp - self.qty * self.price + res['price'] * self.qty
                record.write({'client_wkp': weikaipiao})
            if res['kaipiao']:
                zhangmian = record.client_zm - self.kaipiao + res['kaipiao']
                weikaipiao = record.client_wkp + self.kaipiao - res['kaipiao']
                record.write({'client_zm': zhangmian, 'client_wkp': weikaipiao})
            if res['bukaipiao']:
                bukaipiao = record.client_bkp - self.bukaipiao + res['bukaipiao']
                weikaipiao = record.client_wkp + self.bukaipiao - res['bukaipiao']
                record.write({'client_bkp': bukaipiao, 'client_wkp': weikaipiao})
            if res['shoukuankaipiao']:
                zhangmian = record.client_zm + self.shoukuankaipiao - res['shoukuankaipiao']
                weikaipiao = record.client_wkp - self.shoukuankaipiao + res['shoukuankaipiao']
                record.write({'client_zm': zhangmian, 'client_wkp': weikaipiao})
            if res['shoukuanbukaipiao']:
                bukaipiao = record.client_bkp + self.shoukuanbukaipiao - res['shoukuanbukaipiao']
                weikaipiao = record.client_wkp - self.shoukuanbukaipiao + res['shoukuanbukaipiao']
                record.write({'client_bkp': bukaipiao, 'client_wkp': weikaipiao})
        return super(GooseYewuOrder, self).write(vals)

    def _onchange_client_bh(self, client_bh):
        res = {}
        for record in self.env['goose.client'].search([('code', '=', client_bh)]):
            res['client_id'] = record.id
            return {'value': res}

    def _onchange_client_id(self, client_id, company):
        if client_id != False:
            res = {}
            c_id = 0
            res['client_bkp'] = 0
            res['client_wkp'] = 0
            res['client_zm'] = 0
            for record in self.env['goose.order.yewu'].search(
                    [('client_id', '=', client_id), ('bujiliang', '=', False), ('company', '=', company)]):
                res['client_bkp'] += record.bukaipiao - record.shoukuanbukaipiao
                res['client_wkp'] += record.amount - record.kaipiao - record.bukaipiao
                res['client_zm'] += record.kaipiao - record.shoukuankaipiao
            return {'value': res, 'domain': {'sale_contract': [('user_id', '=', self.env.uid),('state','=','done')]}}

    @api.depends('kaipiao', 'shoukuankaipiao', 'client_zm')
    def _get_zhangmian(self):
        for record in self:
            record.zhangmian = record.kaipiao - record.shoukuankaipiao + record.client_zm
            # return {'value':res}

    @api.depends('qty', 'price')
    def _get_amount(self):
        for record in self:
            record.amount = record.qty * record.price

    @api.depends('bukaipiao', 'shoukuanbukaipiao', 'client_bkp')
    def _get_yuerbukaipiao(self):
        for record in self:
            record.yuerbukaipiao = record.bukaipiao - record.shoukuanbukaipiao + record.client_bkp

    @api.depends('amount', 'kaipiao', 'bukaipiao', 'client_wkp')
    def _get_weikaipiao(self):
        for record in self:
            record.weikaipiao = record.amount - record.kaipiao - record.bukaipiao + record.client_wkp

    @api.depends('kaipiao', 'bukaipiao')
    def _get_kphj(self):
        for record in self:
            record.kaipiaoheji = record.kaipiao + record.bukaipiao

    @api.depends('yinhang', 'tiaozheng', 'xianjin')
    def _get_skhj(self):
        for record in self:
            record.shoukuanheji = record.yinhang + record.tiaozheng + record.xianjin

    @api.depends('shoukuankaipiao', 'shoukuanbukaipiao')
    def _get_skphj(self):
        for record in self:
            record.shoukuankaipiaoheji = record.shoukuankaipiao + record.shoukuanbukaipiao

    @api.depends('zhangmian', 'yuerbukaipiao', 'weikaipiao')
    def _get_yehj(self):
        for record in self:
            record.yuerheji = record.zhangmian + record.yuerbukaipiao + record.weikaipiao

    @api.depends('order_date')
    def _get_month(self):
        for record in self:
            record.month = int(record.order_date[0:4]) * 100 + int(record.order_date[5:7])

    @api.depends('client_id')
    def _get_contract(self):
        print self.with_context()
        return [('partner_id', '=', self.client_id)]

    # @api.onchange('client_id')
    # def _onchange_client_id(self):
    #     if self.client_id:
    #         return {'domain':{'sale_contract':[('partner_id','=',self.client_id.id)]}}
    #     else:
    #         return {'domian':{'sale_contract':[]}}

    name = fields.Char(u'发货编号')
    company = fields.Selection([('ye', u'野鹅'), ('tian', u'天鹅')], u'公司', default='ye')
    order_date = fields.Date(u'录入日期', default=fields.Date.today())
    month = fields.Float(u'录入月份', compute=_get_month, store=True)
    liushui = fields.Char(u'凭证号')
    madan = fields.Char(u'码单号')
    yewu = fields.Many2one('hr.employee',u'业务员', related='client_id.yewu', store=True, require=True)
    category = fields.Many2one('goose.category',u'产品名称类别', related='product_id.category')
    product_id = fields.Many2one('goose.product', u'产品名称', ondelete='restrict')
    client_bh = fields.Char(u'客户编号', related='client_id.code')
    client_id = fields.Many2one('goose.client', u'客户名称')
    bujiliang = fields.Boolean(u'不计量')
    qty = fields.Float(u'发货数量')
    price = fields.Float(u'发货单价')
    amount = fields.Float(u'发货金额', compute=_get_amount, store=True)
    kaipiao = fields.Float(u'开票')
    bukaipiao = fields.Float(u'不开票')
    kaipiaoheji = fields.Float(u'合计', compute=_get_kphj)
    yinhang = fields.Float(u'银行')
    tiaozheng = fields.Float(u'调整')
    xianjin = fields.Float(u'现金')
    shoukuanheji = fields.Float(u'合计', compute=_get_skhj)
    shoukuankaipiao = fields.Float(u'开票')
    shoukuanbukaipiao = fields.Float(u'不开票')
    shoukuankaipiaoheji = fields.Float(u'合计', compute=_get_skphj)
    zhangmian = fields.Float(u'账面', compute=_get_zhangmian, store=True)
    yuerbukaipiao = fields.Float(u'不开票', compute=_get_yuerbukaipiao, store=True)
    weikaipiao = fields.Float(u'未开票', compute=_get_weikaipiao, store=True)
    yuerheji = fields.Float(u'合计', compute=_get_yehj)
    beizhu = fields.Text(u'备注')
    sale_contract = fields.Many2one('sale.contract', u'合同')

    client_zm = fields.Float(u'客户账面')
    client_bkp = fields.Float(u'客户不开票')
    client_wkp = fields.Float(u'客户未开票')


class GooseOrderShou(models.Model):
    _name = 'goose.order.pay'

    def _onchange_client_bh(self, client_bh):
        res = {}
        for record in self.env['goose.supplier'].search([('code', '=', client_bh)]):
            res['client_id'] = record.id
            return {'value': res}

    def _onchange_client_id(self, client_id):
        res = {}
        res['yuer2'] = 0
        res['weikai2'] = 0
        res['yingkai2'] = 0
        for record in self.env['goose.order.pay'].search([('client_id', '=', client_id)]):
            res['yuer2'] += record.amount - record.heji
            res['weikai2'] += record.amount - record.shikai13 - record.shikai17
            res['yingkai2'] += record.amount - record.shikai13 - record.shikai17
        return {'value': res}

    @api.depends('amount', 'weikai2')
    def _get_yingkai(self):
        for record in self:
            record.yingkai = record.amount + record.weikai2

    @api.depends('amount', 'shikai13', 'shikai17', 'weikai2')
    def _get_weikai(self):
        for record in self:
            record.weikai = record.amount - record.shikai13 - record.shikai17 + record.weikai2

    @api.depends('qty', 'price')
    def _get_amount(self):
        for record in self:
            record.amount = record.qty * record.price

    @api.depends('yinhang', 'ka', 'xianjin')
    def _get_heji(self):
        for record in self:
            record.heji = record.yinhang + record.ka + record.xianjin

    @api.depends('yinhang', 'ka', 'xianjin', 'yuer2', 'amount')
    def _get_yuer(self):
        for record in self:
            record.yuer = record.yuer2 - record.yinhang - record.ka - record.xianjin + record.amount

    order_date = fields.Date(u'录入日期', default=fields.Date.today())
    product_id = fields.Char(u'原料名称')
    guige = fields.Char(u'规格')
    client_bh = fields.Char(u'供应商编号',related='client_id.code')
    client_id = fields.Many2one('goose.supplier', u'供应商名称')
    qty = fields.Float(u'发货数量')
    price = fields.Float(u'发货单价')
    amount = fields.Float(u'发货金额', compute=_get_amount, store=True)
    yingkai = fields.Float(u'应开', compute=_get_yingkai)
    weikai = fields.Float(u'未开', compute=_get_weikai)
    shikai13 = fields.Float(u'实开13%')
    shikai17 = fields.Float(u'实开17%')
    yinhang = fields.Float(u'银行')
    ka = fields.Float(u'卡')
    xianjin = fields.Float(u'现金')
    heji = fields.Float(u'合计', compute=_get_heji, store=True)
    yuer = fields.Float(u'余额', compute=_get_yuer, store=True)
    beizhu = fields.Text(u'备注')
    yuer2 = fields.Float()
    weikai2 = fields.Float()


class GooseOrderShouJl(models.Model):
    _name = 'goose.order.pay.jl'

    def _onchange_client_bh(self, client_bh):
        res = {}
        for record in self.env['goose.supplier'].search([('code', '=', client_bh)]):
            res['client_id'] = record.id
            return {'value': res}

    def _onchange_client_id(self, client_id):
        res = {}
        res['yuer2'] = 0
        res['weikai2'] = 0
        for record in self.env['goose.order.pay.jl'].search([('client_id', '=', client_id)]):
            res['yuer2'] += record.shikai13 + record.shikai17 - record.heji
            res['weikai2'] += record.amount - record.shikai13 - record.shikai17
        return {'value': res}

    @api.depends('amount','weikai2')
    def _get_yingkai(self):
        for record in self:
            record.yingkai = record.amount+record.weikai2

    @api.depends('yingkai', 'shikai13', 'shikai17', 'weikai2')
    def _get_weikai(self):
        for record in self:
            record.weikai = record.amount - record.shikai13 - record.shikai17 + record.weikai2

    @api.depends('qty', 'price')
    def _get_amount(self):
        for record in self:
            record.amount = record.qty * record.price

    @api.depends('yinhang', 'ka', 'xianjin')
    def _get_heji(self):
        for record in self:
            record.heji = record.yinhang + record.ka + record.xianjin

    @api.depends('yinhang', 'ka', 'xianjin', 'yuer2', 'amount')
    def _get_yuer(self):
        for record in self:
            record.yuer = record.yuer2 - record.yinhang - record.ka - record.xianjin + record.amount

    order_date = fields.Date(u'录入日期', default=fields.Date.today())
    product_id = fields.Char(u'摘要(原料名称)')
    guige = fields.Char(u'规格')
    client_bh = fields.Char(u'供应商编号', related='client_id.code')
    client_id = fields.Many2one('goose.supplier', u'供应商名称')
    qty = fields.Float(u'发货数量')
    price = fields.Float(u'发货单价')
    amount = fields.Float(u'发货金额', compute=_get_amount, store=True)
    yingkai = fields.Float(u'应开', compute=_get_yingkai)
    weikai = fields.Float(u'未开', compute=_get_weikai)
    shikai13 = fields.Float(u'实开13%')
    shikai17 = fields.Float(u'实开17%')
    yinhang = fields.Float(u'银行')
    ka = fields.Float(u'卡')
    xianjin = fields.Float(u'现金')
    heji = fields.Float(u'合计', compute=_get_heji, store=True)
    yuer = fields.Float(u'余额', compute=_get_yuer, store=True)
    beizhu = fields.Text(u'备注')
    yuer2 = fields.Float()
    weikai2 = fields.Float()


class GooseSampleOrder(models.Model):
    _name = 'goose.sample.order'

    def _onchange_client_bh(self, client_bh):
        res = {}
        for record in self.env['goose.client'].search([('code', '=', client_bh)]):
            res['client_id'] = record.id
            return {'value': res}

    def _onchange_client_jc(self, client_jc):
        res = {}
        for record in self.env['goose.client'].search([('jiancheng', '=', client_jc)]):
            res['client_id'] = record.id
            return {'value': res}

    def _onchange_client_id(self, client_id):
        if client_id != False:
            record = self.env['goose.client'].search([('id', '=', client_id)])
            res = {}
            res['yewu'] = record.yewu.id
            res['yewu_code'] = record.yewu_code
            return {'value': res}

    def _domain_yewu(self):
        return [('department_id', '=', self.env['hr.department'].search([('name', '=', u'销售部')]).id)]

    name = fields.Char(u'样品订单')
    client_id = fields.Many2one('goose.client', u'客户名称')
    client_bh = fields.Char(u'客户编号', related='client_id.code')
    client_jc = fields.Char(u'客户简称', related='client_id.jiancheng')
    order_date = fields.Date(u'订单日期', default=fields.Date.today())
    yewu = fields.Many2one('hr.employee', u'业务员')
    yewu_code = fields.Char(u'业务员编号', related='yewu.code')
    sale_way = fields.Selection([('in', '内销'), ('out', '外销')], u'销售方式', default='in')
    product_id = fields.Many2one('goose.product', u'样品名称')
    product_qty = fields.Float(u'样品重量')


class GooseStock(models.Model):
    _name = 'goose.stock'

    def _onchange_ruku_bh(self, ruku_bh):
        res = {}
        record = self.env['hr.employee'].search([('code', '=', ruku_bh)])
        res['ruku'] = record.id
        return {'value': res}

    def _domain_ruku(self):
        return [('department_id', '=', self.env['hr.department'].search([('name', '=', u'办公室')]).id)]

    def _onchange_ylbh(self, ylbh):
        res = {}
        record = self.env['goose.product.yuanliao'].search([('code', '=', ylbh)])
        res['ylmc'] = record.id
        return {'value': res}

    def _onchange_supplier_bh(self, supplier_bh):
        res = {}
        record = self.env['goose.supplier'].search([('code', '=', supplier_bh)])
        res['supplier_id'] = record.id
        return {'value': res}

    name = fields.Char(u'入库单号')
    ruku = fields.Many2one('hr.employee', u'入库人员', domain=_domain_ruku)
    ruku_bh = fields.Char(u'入库人员编号', related='ruku.code')
    ruku_date = fields.Date(u'入库日期', default=fields.Date.today())
    supplier_id = fields.Many2one('goose.supplier', u'供应商')
    supplier_bh = fields.Char(u'供应商编号', related='supplier_id.code')
    send_code = fields.Char(u'送货单号')
    ylcd = fields.Char(u'原料产地')
    hydh = fields.Many2one('goose.huayan', u'化验单号')
    price = fields.Float(u'单价')
    price_total = fields.Float(u'总价')
    ylbh = fields.Char(u'原料编码', related='ylmc.code')
    ylmc = fields.Many2one('goose.product.yuanliao', u'原料名称')
    ylpc = fields.Char(u'原料批次')
    baoshu = fields.Float(u'总包数')
    pizhongliang = fields.Float(u'批重量')
    pizhong = fields.Float(u'皮重')
    sunhao = fields.Float(u'损耗项')
    jingzhong = fields.Float(u'净重')
    cangguan = fields.Many2one('goose.cangguan', u'仓管')
    yanshou = fields.Many2one('goose.yanshou', u'验收')


class GooseCangGuan(models.Model):
    _name = 'goose.cangguan'

    name = fields.Char(u'仓管')


class GooseYanShou(models.Model):
    _name = 'goose.yanshou'

    name = fields.Char(u'验收人')


class GooseWJStock(models.Model):
    _name = 'goose.wjstock'

    def _onchange_ruku_bh(self, ruku_bh):
        res = {}
        record = self.env['hr.employee'].search([('code', '=', ruku_bh)])
        res['ruku'] = record.id
        return {'value': res}

    def _domain_ruku(self):
        return [('department_id', '=', self.env['hr.department'].search([('name', '=', u'办公室')]).id)]

    #
    # def _onchange_wlbh(self, wlbh):
    #     res = {}
    #     record = self.env['goose.product.wuliao'].search([('code', '=', wlbh)])
    #     res['wlmc'] = record.id
    #     res['price'] = record.min_stock
    #     return {'value': res}
    @api.model
    def create(self, vals):
        for x in vals['wl_line']:
            name = x[2]['name']
            qty = x[2]['qty']
            kuwei = self.env['goose.wjkuwei'].search([('id', '=', x[2]['kuwei'])]).name
            kucun = self.env['goose.product.wuliao'].search([('id', '=', name)]).stock
            if vals['churu'] == 'chu':
                kucun = kucun - qty
            else:
                kucun = kucun + qty
            self.env['goose.product.wuliao'].search([('id', '=', name)]).write({'kuwei': kuwei, 'stock': kucun})
        return super(GooseWJStock, self).create(vals)

    @api.depends('ruku_date')
    def _get_month(self):
        for record in self:
            record.month = int(record.ruku_date[0:4]) * 100 + int(record.ruku_date[5:7])

    month = fields.Float(u'录入月份', compute=_get_month, store=True)
    name = fields.Char(u'入库单号')
    ruku = fields.Many2one('hr.employee', u'入库人员', domain=_domain_ruku)
    ruku_bh = fields.Char(u'入库人员编号', related='ruku.code')
    ruku_date = fields.Date(u'入库日期', default=fields.Date.today())
    department = fields.Many2one('hr.department', u'部门')
    # wlbh = fields.Char(u'物料编码', related='wlmc.code')
    # wlmc = fields.Many2one('goose.product.wuliao', u'物料名称')
    # kucun = fields.Float(u'库存', default=0.0)
    # price = fields.Float(u'单价', readonly=True)
    churu = fields.Selection([('chu', '出库'), ('ru', '入库')], string=u'出入库', default=u'ru')
    wl_line = fields.One2many('goose.wuliao.line', 'wl_id', u'物料信息')


class GooseWuliaoLine(models.Model):
    _name = 'goose.wuliao.line'

    wl_id = fields.Many2one('goose.wjstock')
    name = fields.Many2one('goose.product.wuliao', u'物料名称')
    kuwei = fields.Many2one('goose.wjkuwei', u'库位')
    qty = fields.Float(u'数量')


class GooseWjKuwei(models.Model):
    _name = 'goose.wjkuwei'

    name = fields.Char(u'五金库位')


class GooseHuayan(models.Model):
    _name = 'goose.huayan'

    def _domain_huayan(self):
        return [('department_id', '=', self.env['hr.department'].search([('name', '=', u'办公室')]).id)]

    def _onchange_ylbh(self, ylbh):
        res = {}
        record = self.env['goose.product.yuanliao'].search([('code', '=', ylbh)])
        res['ylmc'] = record.id
        return {'value': res}

    def _onchange_supplier_bh(self, supplier_bh):
        res = {}
        record = self.env['goose.supplier'].search([('code', '=', supplier_bh)])
        res['supplier_id'] = record.id
        return {'value': res}

    def _onchange_pici(self, pici):
        res = {}
        if pici != '':
            record = self.env['goose.stock'].search([('ylpc', '=', pici)])
            res['supplier_id'] = record.supplier_id
            res['baoshu'] = record.baoshu
            res['pizhongliang'] = record.pizhongliang
            res['ylmc'] = record.ylmc
        return {'value': res}

    name = fields.Char(u'化验单号')
    pici = fields.Char(u'批次')
    supplier_id = fields.Many2one('goose.supplier', u'供应商')
    supplier_bh = fields.Char(u'供应商编号', related='supplier_id.code')
    ylmc = fields.Many2one('goose.product.yuanliao', u'原料名称')
    baoshu = fields.Float(u'总包数')
    pizhongliang = fields.Float(u'批重量')
    bianhao = fields.Char(u'编号')
    hyry = fields.Many2one('hr.employee', u'化验人员1', domain=_domain_huayan)
    hy_code = fields.Char(u'化验人员1编号', related='hyry.code')
    hyry1 = fields.Many2one('hr.employee', u'化验人员2', domain=_domain_huayan)
    hy_code1 = fields.Char(u'化验人员2编号', related='hyry1.code')
    hyry2 = fields.Many2one('hr.employee', u'化验人员3', domain=_domain_huayan)
    hy_code2 = fields.Char(u'化验人员3编号', related='hyry2.code')
    hyry3 = fields.Many2one('hr.employee', u'化验人员4', domain=_domain_huayan)
    hy_code3 = fields.Char(u'化验人员4编号', related='hyry3.code')


class GooseCategoryWuliao(models.Model):
    _name = 'goose.category.wuliao'

    name = fields.Char(u'类别名称')


class GooseContacts(models.Model):
    _name = 'goose.contacts'

    contacts_id = fields.Many2one('goose.client', u'客户ID')
    name = fields.Char(u'联系人')
    duties = fields.Char(u'职务')
    department = fields.Char(u'部门')
    hand_phone = fields.Char(u'手机')
    phone = fields.Char(u'电话')
    other_way = fields.Char(u'其他联系方式')
    remark = fields.Char(u'备注')


class HrEmployeeExtend(models.Model):
    _inherit = 'hr.employee'

    code = fields.Char(u'业务员编号')

    _sql_constraints = [
        ('hr_employee_code', 'unique (code)', "业务员编号必须唯一"),
    ]


class GooseJiXiaoKaoHe(models.Model):
    _name = 'goose.jxkh'

    def onchange_client(self, client):
        return {'domain': {'contract': [('partner_id', '=', client)]}}

    def onchange_contract(self, contract):
        res = {}
        res['client'] = self.env['goose.client'].search(
            [('id', '=', self.env['sale.contract'].search([('id', '=', contract)]).partner_id.id)])
        res['htje'] = self.env['sale.contract'].search([('id', '=', contract)]).amount_total
        return {'value': res}

    def onchange_code(self, yewu_code):
        res = {}
        res['yewu'] = self.env['hr.employee'].search([('code', '=', yewu_code)]).id
        return {'value': res, 'domain': {'client': [('yewu_code', '=', yewu_code)]}}

    def onchange_bh(self, client_bh):
        res = {}
        res['client'] = self.env['goose.client'].search([('code', '=', client_bh)]).id
        return {'value': res}

    def _domain_yewu(self):
        return [('department_id', '=', self.env['hr.department'].search([('name', '=', u'销售部')]).id)]

    date = fields.Date(u'日期', default=fields.Date.today())
    contract = fields.Many2one('sale.contract', u'合同')
    fhdh = fields.Char(u'发货码单')
    client = fields.Many2one('goose.client', u'客户')
    client_bh = fields.Char(u'客户编号', related='client.code')
    yewu = fields.Many2one('hr.employee', u'业务员', required=True, domain=_domain_yewu, related='client.yewu')
    yewu_code = fields.Char(u'业务员编号', related='yewu.code')
    fahuo = fields.Float(u'发货')
    shoukuan = fields.Float(u'收款')
    qty = fields.Float()
    product_id = fields.Many2one('goose.product')


class Email(models.Model):
    _name = 'goose.email'
    _inherit = ['mail.thread']

    name = fields.Char(u'编号', size=64, required=True, help=u"我是编号")
    yewu = fields.Many2one('hr.employee',u'业务员')

    def send_email(self):
        MailMessage = self.env['mail.message']
        MailFollowers = self.env['mail.followers']
        values = {}
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        query = """
                        SELECT
                            c.name as client,
                            h.id as client_id,
                            s.name as contract,
                            s.amount_total as amount,
                            g.date as date,
                            g.fhdh as madan,
                            g.fahuo as fahuo,
                            g.qty as qty,
                            g.shoukuan as shoukuan,
                            o.name as product,
                            h.name_related as yewu
                        FROM goose_jxkh as g
                        LEFT JOIN goose_client as c
                        ON c.id = g.client
                        LEFT JOIN hr_employee as h
                        ON c.yewu = h.id
                        LEFT JOIN sale_contract as s
                        ON s.id = g.contract
                        LEFT  JOIN goose_product as o
                        ON o.id = g.product_id
                        ORDER BY g.id
                       """
        self.env.cr.execute(query)
        # 期末的金额
        res = self.env.cr.dictfetchall()

        query2 = """
                        SELECT
                            fhdh as madan
                        FROM goose_jxkh as g
                        GROUP BY g.fhdh
                """
        self.env.cr.execute(query2)
        res2 = self.env.cr.dictfetchall()
        mes = []
        for x in res2:
            data2 = {'in': 0, 'out': 0, 'qty': 0, 'jine': 0}
            date_begin = None
            for r in res:
                if x['madan'] == r['madan']:
                    if date_begin == None:
                        date_begin = datetime.datetime(int(r['date'][0:4]), int(r['date'][5:7]), int(r['date'][8:10]))
                    data2['qty'] += r['qty']
                    data2['jine'] += r['fahuo']
                    data2['product'] = r['product']
                    data2['madan'] = x['madan']
                    data2['contract'] = r['contract']
                    data2['client'] = r['client']
                    data2['client_id'] = r['client_id']
                    data2['yewu'] = r['yewu']
                    data2['in_data'] = None
                    date_end = datetime.datetime(int(r['date'][0:4]), int(r['date'][5:7]), int(r['date'][8:10]))
                    if (date_end - date_begin).days < 90:
                        data2['in'] += r['shoukuan']
                    else:
                        data2['out'] += r['shoukuan']
                    if data2['in'] + data2['out'] == data2['jine']:
                        data2['in_data'] = (date_end - date_begin).days
                    data2['days'] = (datetime.datetime(int(day[0:4]), int(day[5:7]), int(day[8:10])) - date_begin).days
            mes.append(data2)
        for m in mes:
            if m['days'] > 90:
                body = u'回款超时,客户：' + m['client'] + u';码单号：' + m['madan'] + u';业务员：' + m['yewu']
                res_id = self.env['goose.email'].search([('yewu','=',m['client_id'])]).id
                print m['client_id']
                values.update({'body': body, 'model': 'goose.email', 'res_id': res_id,
                               'subtype_id': 1, 'author_id': 3, 'message_type': 'notification',
                               'partner_ids': [7], 'subject': True})
                MailMessage.create(values)
