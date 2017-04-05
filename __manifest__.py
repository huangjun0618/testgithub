# -*- coding: utf-8 -*-
{
    'name': "野鹅项目",
    'summary': """野鹅项目
        """,
    'sequence': 0,
    'description': """
        蓝云公司平台模块
    """,
    'author': "浙江蓝云信息科技股份有限公司",
    'website': "http://www.zjlanyun.com",
    'category': 'lanyun',
    'version': '0.1',
    'depends': ['base', 'hr', 'product', 'report','mail'],
    'data': [

        'security/goose_security.xml',
        'security/ir.model.access.csv',
        'sequence/sequence.xml',
        'report/sale_contract_report.xml',
        'report/my_report.xml',
        'report/goose_templates.xml',
        'report/sale_contract_report_templates.xml',
        'views/goose_inherit.xml',
        'views/goose_views.xml',
        'wizard/goose_order_report.xml',
        'wizard/wizard_sale_contract.xml',
        'views/assets.xml',
        'views/sale_contract.xml',
        'data/hr_data.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
