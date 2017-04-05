# -*- coding: utf-8 -*-

from odoo import api, models
import datetime


class GooseOrderReport(models.AbstractModel):
    _name = 'report.goose.my_report'

    @api.model
    def render_html(self, docids, data=None):
        year = int(data['form']['year'][0:4]) * 100
        month = {'01': '一月', '02': '二月', '03': '三月', '04': '四月', '05': '五月', '06': '六月', '07': '七月', '08': '八月',
                 '09': '九月', '10': '十月', '11': '十一月', '12': '十二月'}
        month3 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        boom = {'kaipiao': {}, 'shoukuanbukaipiao': {}, 'price': {}, 'qty': {}, 'tiaozheng': {}, 'yinhang': {},
                'xianjin': {}, 'bukaipiao': {}, 'shoukuankaipiao': {}, 'zhangmian': {}, 'amount': {}, 'heji1': {},
                'heji2': {}, 'yuerbukaipiao': {}, 'weikaipiao': {}, 'heji3': {}, 'heji4': {}, 'szhangmian': {},
                'syuerbukaipiao': {}, 'sweikaipiao': {}, 'sheji3': {}}
        boom2 = {'kaipiao': {}, 'shoukuanbukaipiao': {}, 'price': {}, 'qty': {}, 'tiaozheng': {}, 'yinhang': {},
                 'xianjin': {}, 'bukaipiao': {}, 'shoukuankaipiao': {}, 'zhangmian': {}, 'amount': {}, 'heji1': {},
                 'heji2': {}, 'yuerbukaipiao': {}, 'weikaipiao': {}, 'heji3': {}, 'heji4': {}, 'szhangmian': {},
                 'syuerbukaipiao': {}, 'sweikaipiao': {}, 'sheji3': {}}
        li = {'kaipiao': 0, 'shoukuanbukaipiao': 0, 'price': 0, 'qty': 0, 'tiaozheng': 0, 'yinhang': 0,
              'xianjin': 0, 'bukaipiao': 0, 'shoukuankaipiao': 0, 'zhangmian': 0, 'amount': 0, 'heji1': 0,
              'heji2': 0, 'yuerbukaipiao': 0, 'weikaipiao': 0, 'heji3': 0, 'heji4': 0, 'szhangmian': 0,
              'syuerbukaipiao': 0, 'sweikaipiao': 0, 'sheji3': 0}
        li2 = {'kaipiao': 0, 'shoukuanbukaipiao': 0, 'price': 0, 'qty': 0, 'tiaozheng': 0, 'yinhang': 0,
               'xianjin': 0, 'bukaipiao': 0, 'shoukuankaipiao': 0, 'zhangmian': 0, 'amount': 0, 'heji1': 0,
               'heji2': 0, 'yuerbukaipiao': 0, 'weikaipiao': 0, 'heji3': 0, 'heji4': 0, 'szhangmian': 0,
               'syuerbukaipiao': 0, 'sweikaipiao': 0, 'sheji3': 0}
        date = []
        client = []
        clients = []
        clients_name = {}
        if data['form']['result_selection'] == 'customer':
            if data['form']['yewu']:
                for record in self.env['goose.client'].search([('yewu', '=', data['form']['yewu'][0])]):
                    client.append(record.name)
            if data['form']['sorted_by'] == 'month' and data['form']['yewu'] == False:
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        date.append(x)
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order as g
                                            WHERE g.month = %s AND g.company = 'ye'
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order as g
                                            WHERE g.month < %s AND g.company = 'ye'
                                            """
                        self.env.cr.execute(query2, tuple([year + int(x)]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([year + int(x)]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']
                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom[a][x] = res[0][a]
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order as g
                                            WHERE g.month = %s AND g.company = 'tian'
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order as g
                                            WHERE g.month < %s AND g.company = 'tian'
                                            """
                        self.env.cr.execute(query2, tuple([year + int(x)]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([year + int(x)]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']

                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom2[a][x] = res[0][a]
                for client_id in date:
                    li['kaipiao'] += boom['kaipiao'][client_id]
                    li['shoukuanbukaipiao'] += boom['shoukuanbukaipiao'][client_id]
                    li['qty'] += boom['qty'][client_id]
                    li['tiaozheng'] += boom['tiaozheng'][client_id]
                    li['yinhang'] += boom['yinhang'][client_id]
                    li['xianjin'] += boom['xianjin'][client_id]
                    li['bukaipiao'] += boom['bukaipiao'][client_id]
                    li['shoukuankaipiao'] += boom['shoukuankaipiao'][client_id]
                    li['zhangmian'] = boom['zhangmian'][client_id]
                    li['amount'] += boom['amount'][client_id]
                    li['heji1'] += boom['heji1'][client_id]
                    li['heji2'] += boom['heji2'][client_id]
                    li['yuerbukaipiao'] = boom['yuerbukaipiao'][client_id]
                    li['weikaipiao'] = boom['weikaipiao'][client_id]
                    li['heji3'] = boom['heji3'][client_id]
                    li['heji4'] += boom['heji4'][client_id]
                    li['szhangmian'] += boom['szhangmian'][client_id]
                    li['syuerbukaipiao'] += boom['syuerbukaipiao'][client_id]
                    li['sweikaipiao'] += boom['sweikaipiao'][client_id]
                    li['sheji3'] += boom['sheji3'][client_id]
                for client_id in date:
                    li2['kaipiao'] += boom2['kaipiao'][client_id]
                    li2['shoukuanbukaipiao'] += boom2['shoukuanbukaipiao'][client_id]
                    li2['qty'] += boom2['qty'][client_id]
                    li2['tiaozheng'] += boom2['tiaozheng'][client_id]
                    li2['yinhang'] += boom2['yinhang'][client_id]
                    li2['xianjin'] += boom2['xianjin'][client_id]
                    li2['bukaipiao'] += boom2['bukaipiao'][client_id]
                    li2['shoukuankaipiao'] += boom2['shoukuankaipiao'][client_id]
                    li2['zhangmian'] = boom2['zhangmian'][client_id]
                    li2['amount'] += boom2['amount'][client_id]
                    li2['heji1'] += boom2['heji1'][client_id]
                    li2['heji2'] += boom2['heji2'][client_id]
                    li2['yuerbukaipiao'] = boom2['yuerbukaipiao'][client_id]
                    li2['weikaipiao'] = boom2['weikaipiao'][client_id]
                    li2['heji3'] = boom2['heji3'][client_id]
                    li2['heji4'] += boom2['heji4'][client_id]
                    li2['szhangmian'] += boom2['szhangmian'][client_id]
                    li2['syuerbukaipiao'] += boom2['syuerbukaipiao'][client_id]
                    li2['sweikaipiao'] += boom2['sweikaipiao'][client_id]
                    li2['sheji3'] += boom2['sheji3'][client_id]
            elif data['form']['sorted_by'] == 'month' and data['form']['yewu']:
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        date.append(x)
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order as g
                                            WHERE g.month = %s AND g.company = 'ye' AND g.yewu = %s
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order as g
                                            WHERE g.month < %s AND g.company = 'ye' AND g.yewu = %s
                                            """
                        self.env.cr.execute(query2, tuple([(year + int(x)), data['form']['yewu'][0]]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([(year + int(x)), data['form']['yewu'][0]]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']
                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom[a][x] = res[0][a]
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order as g
                                            WHERE g.month = %s AND g.company = 'tian' AND g.yewu = %s
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order as g
                                            WHERE g.month < %s AND g.company = 'tian' AND g.yewu = %s
                                            """
                        self.env.cr.execute(query2, tuple([(year + int(x)), data['form']['yewu'][0]]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([(year + int(x)), data['form']['yewu'][0]]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']

                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom2[a][x] = res[0][a]
                for client_id in date:
                    li['kaipiao'] += boom['kaipiao'][client_id]
                    li['shoukuanbukaipiao'] += boom['shoukuanbukaipiao'][client_id]
                    li['qty'] += boom['qty'][client_id]
                    li['tiaozheng'] += boom['tiaozheng'][client_id]
                    li['yinhang'] += boom['yinhang'][client_id]
                    li['xianjin'] += boom['xianjin'][client_id]
                    li['bukaipiao'] += boom['bukaipiao'][client_id]
                    li['shoukuankaipiao'] += boom['shoukuankaipiao'][client_id]
                    li['zhangmian'] = boom['zhangmian'][client_id]
                    li['amount'] += boom['amount'][client_id]
                    li['heji1'] += boom['heji1'][client_id]
                    li['heji2'] += boom['heji2'][client_id]
                    li['yuerbukaipiao'] = boom['yuerbukaipiao'][client_id]
                    li['weikaipiao'] = boom['weikaipiao'][client_id]
                    li['heji3'] = boom['heji3'][client_id]
                    li['heji4'] += boom['heji4'][client_id]
                    li['szhangmian'] += boom['szhangmian'][client_id]
                    li['syuerbukaipiao'] += boom['syuerbukaipiao'][client_id]
                    li['sweikaipiao'] += boom['sweikaipiao'][client_id]
                    li['sheji3'] += boom['sheji3'][client_id]
                for client_id in date:
                    li2['kaipiao'] += boom2['kaipiao'][client_id]
                    li2['shoukuanbukaipiao'] += boom2['shoukuanbukaipiao'][client_id]
                    li2['qty'] += boom2['qty'][client_id]
                    li2['tiaozheng'] += boom2['tiaozheng'][client_id]
                    li2['yinhang'] += boom2['yinhang'][client_id]
                    li2['xianjin'] += boom2['xianjin'][client_id]
                    li2['bukaipiao'] += boom2['bukaipiao'][client_id]
                    li2['shoukuankaipiao'] += boom2['shoukuankaipiao'][client_id]
                    li2['zhangmian'] = boom2['zhangmian'][client_id]
                    li2['amount'] += boom2['amount'][client_id]
                    li2['heji1'] += boom2['heji1'][client_id]
                    li2['heji2'] += boom2['heji2'][client_id]
                    li2['yuerbukaipiao'] = boom2['yuerbukaipiao'][client_id]
                    li2['weikaipiao'] = boom2['weikaipiao'][client_id]
                    li2['heji3'] = boom2['heji3'][client_id]
                    li2['heji4'] += boom2['heji4'][client_id]
                    li2['szhangmian'] += boom2['szhangmian'][client_id]
                    li2['syuerbukaipiao'] += boom2['syuerbukaipiao'][client_id]
                    li2['sweikaipiao'] += boom2['sweikaipiao'][client_id]
                    li2['sheji3'] += boom2['sheji3'][client_id]
            elif data['form']['sorted_by'] == 'people':
                for client_id in client:
                    x = self.env['goose.client'].search([('name', '=', client_id)]).id
                    query = """
                                        SELECT
                                            sum(g.qty) as qty,
                                            sum(g.price) as price,
                                            sum(g.price*g.qty) as amount,
                                            sum(g.kaipiao) as kaipiao,
                                            sum(g.bukaipiao) as bukaipiao,
                                            sum(g.yinhang) as yinhang,
                                            sum(g.tiaozheng) as tiaozheng,
                                            sum(g.xianjin) as xianjin,
                                            sum(g.shoukuankaipiao) as shoukuankaipiao,
                                            sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                        FROM goose_order as g
                                        WHERE g.month >= %s AND g.month <= %s AND g.yewu = %s AND g.client_id = %s AND g.bujiliang = FALSE AND g.company = 'ye'
                                        """
                    query2 = """
                                SELECT
                                    sum(g.qty) as qty,
                                    sum(g.price) as price,
                                    sum(g.price*g.qty) as amount,
                                    sum(g.kaipiao) as kaipiao,
                                    sum(g.bukaipiao) as bukaipiao,
                                    sum(g.yinhang) as yinhang,
                                    sum(g.tiaozheng) as tiaozheng,
                                    sum(g.xianjin) as xianjin,
                                    sum(g.shoukuankaipiao) as shoukuankaipiao,
                                    sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                FROM goose_order as g
                                WHERE g.month < %s AND g.yewu = %s AND g.client_id = %s AND g.bujiliang = FALSE AND g.company = 'ye'
                                """
                    day = int(data['form']['year'][0:4]) * 100 + int(data['form']['date_from'])
                    day2 = int(data['form']['year'][0:4]) * 100 + int(data['form']['date_to'])
                    self.env.cr.execute(query,
                                        tuple([day, day2, data['form']['yewu'][0], x]))
                    res = self.env.cr.dictfetchall()
                    self.env.cr.execute(query2,
                                        tuple([day, data['form']['yewu'][0], x]))
                    ress = self.env.cr.dictfetchall()
                    for r in res[0]:
                        if res[0][r] == None:
                            res[0][r] = 0
                    for r in ress[0]:
                        if ress[0][r] == None:
                            ress[0][r] = 0

                    if ress == []:
                        boom['sweikaipiao'][client_id] = 0
                        boom['syuerbukaipiao'][client_id] = 0
                        boom['szhangmian'][client_id] = 0
                        boom['sheji3'][client_id] = 0

                    for a in ress:
                        a['sweikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao'] or 0
                        a['syuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao'] or 0
                        a['szhangmian'] = a['kaipiao'] - a['shoukuankaipiao'] or 0
                        a['sheji3'] = a['sweikaipiao'] + a['syuerbukaipiao'] + a['szhangmian'] or 0
                        boom['sweikaipiao'][client_id] = a['sweikaipiao']
                        boom['syuerbukaipiao'][client_id] = a['syuerbukaipiao']
                        boom['szhangmian'][client_id] = a['szhangmian']
                        boom['sheji3'][client_id] = a['sheji3']
                    if res == []:
                        boom['amount'][client_id] = 0
                        boom['weikaipiao'][client_id] = 0
                        boom['yuerbukaipiao'][client_id] = 0
                        boom['zhangmian'][client_id] = 0
                        boom['heji1'][client_id] = 0
                        boom['heji2'][client_id] = 0
                        boom['heji3'][client_id] = 0
                        boom['heji4'][client_id] = 0
                        boom['qty'][client_id] = 0
                        boom['yinhang'][client_id] = 0
                        boom['xianjin'][client_id] = 0
                        boom['tiaozheng'][client_id] = 0
                        boom['shoukuankaipiao'][client_id] = 0
                        boom['shoukuanbukaipiao'][client_id] = 0
                        boom['kaipiao'][client_id] = 0
                        boom['bukaipiao'][client_id] = 0
                    print res
                    for a in res:
                        a['weikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao']
                        a['yuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao']
                        a['zhangmian'] = a['kaipiao'] - a['shoukuankaipiao']
                        a['heji1'] = a['yinhang'] + a['xianjin'] + a['tiaozheng']
                        a['heji2'] = a['shoukuankaipiao'] + a['shoukuanbukaipiao']
                        a['heji3'] = a['weikaipiao'] + a['yuerbukaipiao'] + a['zhangmian']
                        a['heji4'] = a['kaipiao'] + a['bukaipiao']
                        boom['amount'][client_id] = a['amount']
                        boom['weikaipiao'][client_id] = a['weikaipiao']
                        boom['yuerbukaipiao'][client_id] = a['yuerbukaipiao']
                        boom['zhangmian'][client_id] = a['zhangmian']
                        boom['heji1'][client_id] = a['heji1']
                        boom['heji2'][client_id] = a['heji2']
                        boom['heji3'][client_id] = a['heji3']
                        boom['heji4'][client_id] = a['heji4']
                        boom['qty'][client_id] = a['qty']
                        boom['yinhang'][client_id] = a['yinhang']
                        boom['xianjin'][client_id] = a['xianjin']
                        boom['tiaozheng'][client_id] = a['tiaozheng']
                        boom['shoukuankaipiao'][client_id] = a['shoukuankaipiao']
                        boom['shoukuanbukaipiao'][client_id] = a['shoukuanbukaipiao']
                        boom['kaipiao'][client_id] = a['kaipiao']
                        boom['bukaipiao'][client_id] = a['bukaipiao']
                    query = """
                                    SELECT
                                        sum(g.qty) as qty,
                                        sum(g.price) as price,
                                        sum(g.price*g.qty) as amount,
                                        sum(g.kaipiao) as kaipiao,
                                        sum(g.bukaipiao) as bukaipiao,
                                        sum(g.yinhang) as yinhang,
                                        sum(g.tiaozheng) as tiaozheng,
                                        sum(g.xianjin) as xianjin,
                                        sum(g.shoukuankaipiao) as shoukuankaipiao,
                                        sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                    FROM goose_order as g
                                    WHERE g.month >= %s AND g.month <= %s AND g.yewu = %s AND g.client_id = %s AND g.bujiliang = FALSE AND g.company = 'tian'
                                    """
                    query2 = """
                                    SELECT
                                    sum(g.qty) as qty,
                                    sum(g.price) as price,
                                    sum(g.price*g.qty) as amount,
                                    sum(g.kaipiao) as kaipiao,
                                    sum(g.bukaipiao) as bukaipiao,
                                    sum(g.yinhang) as yinhang,
                                    sum(g.tiaozheng) as tiaozheng,
                                    sum(g.xianjin) as xianjin,
                                    sum(g.shoukuankaipiao) as shoukuankaipiao,
                                    sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                    FROM goose_order as g
                                    WHERE g.month < %s AND g.yewu = %s AND g.client_id = %s AND g.bujiliang = FALSE AND g.company = 'tian'
                                    """
                    self.env.cr.execute(query,
                                        tuple([day, day2, data['form']['yewu'][0], x]))
                    res = self.env.cr.dictfetchall()
                    self.env.cr.execute(query2,
                                        tuple([day, data['form']['yewu'][0], x]))
                    ress = self.env.cr.dictfetchall()
                    for r in res[0]:
                        if res[0][r] == None:
                            res[0][r] = 0
                    for r in ress[0]:
                        if ress[0][r] == None:
                            ress[0][r] = 0
                    if ress == []:
                        boom2['sweikaipiao'][client_id] = 0
                        boom2['syuerbukaipiao'][client_id] = 0
                        boom2['szhangmian'][client_id] = 0
                        boom2['sheji3'][client_id] = 0
                    for a in ress:
                        a['sweikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao']
                        a['syuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao']
                        a['szhangmian'] = a['kaipiao'] - a['shoukuankaipiao']
                        a['sheji3'] = a['sweikaipiao'] + a['syuerbukaipiao'] + a['szhangmian']
                        boom2['sweikaipiao'][client_id] = a['sweikaipiao']
                        boom2['syuerbukaipiao'][client_id] = a['syuerbukaipiao']
                        boom2['szhangmian'][client_id] = a['szhangmian']
                        boom2['sheji3'][client_id] = a['sheji3']
                    if res == []:
                        boom2['amount'][client_id] = 0
                        boom2['weikaipiao'][client_id] = 0
                        boom2['yuerbukaipiao'][client_id] = 0
                        boom2['zhangmian'][client_id] = 0
                        boom2['heji1'][client_id] = 0
                        boom2['heji2'][client_id] = 0
                        boom2['heji3'][client_id] = 0
                        boom2['heji4'][client_id] = 0
                        boom2['qty'][client_id] = 0
                        boom2['yinhang'][client_id] = 0
                        boom2['xianjin'][client_id] = 0
                        boom2['tiaozheng'][client_id] = 0
                        boom2['shoukuankaipiao'][client_id] = 0
                        boom2['shoukuanbukaipiao'][client_id] = 0
                        boom2['kaipiao'][client_id] = 0
                        boom2['bukaipiao'][client_id] = 0
                    for a in res:
                        a['weikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao']
                        a['yuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao']
                        a['zhangmian'] = a['kaipiao'] - a['shoukuankaipiao']
                        a['heji1'] = a['yinhang'] + a['xianjin'] + a['tiaozheng']
                        a['heji2'] = a['shoukuankaipiao'] + a['shoukuanbukaipiao']
                        a['heji3'] = a['weikaipiao'] + a['yuerbukaipiao'] + a['zhangmian']
                        a['heji4'] = a['kaipiao'] + a['bukaipiao']
                        boom2['amount'][client_id] = a['amount']
                        boom2['weikaipiao'][client_id] = a['weikaipiao']
                        boom2['yuerbukaipiao'][client_id] = a['yuerbukaipiao']
                        boom2['zhangmian'][client_id] = a['zhangmian']
                        boom2['heji1'][client_id] = a['heji1']
                        boom2['heji2'][client_id] = a['heji2']
                        boom2['heji3'][client_id] = a['heji3']
                        boom2['heji4'][client_id] = a['heji4']
                        boom2['qty'][client_id] = a['qty']
                        boom2['yinhang'][client_id] = a['yinhang']
                        boom2['xianjin'][client_id] = a['xianjin']
                        boom2['tiaozheng'][client_id] = a['tiaozheng']
                        boom2['shoukuankaipiao'][client_id] = a['shoukuankaipiao']
                        boom2['shoukuanbukaipiao'][client_id] = a['shoukuanbukaipiao']
                        boom2['kaipiao'][client_id] = a['kaipiao']
                        boom2['bukaipiao'][client_id] = a['bukaipiao']
                for client_id in client:
                    li['kaipiao'] += boom['kaipiao'][client_id]
                    li['shoukuanbukaipiao'] += boom['shoukuanbukaipiao'][client_id]
                    li['qty'] += boom['qty'][client_id]
                    li['tiaozheng'] += boom['tiaozheng'][client_id]
                    li['yinhang'] += boom['yinhang'][client_id]
                    li['xianjin'] += boom['xianjin'][client_id]
                    li['bukaipiao'] += boom['bukaipiao'][client_id]
                    li['shoukuankaipiao'] += boom['shoukuankaipiao'][client_id]
                    li['zhangmian'] += boom['zhangmian'][client_id]
                    li['amount'] += boom['amount'][client_id]
                    li['heji1'] += boom['heji1'][client_id]
                    li['heji2'] += boom['heji2'][client_id]
                    li['yuerbukaipiao'] += boom['yuerbukaipiao'][client_id]
                    li['weikaipiao'] += boom['weikaipiao'][client_id]
                    li['heji3'] += boom['heji3'][client_id]
                    li['heji4'] += boom['heji4'][client_id]
                    li['szhangmian'] += boom['szhangmian'][client_id]
                    li['syuerbukaipiao'] += boom['syuerbukaipiao'][client_id]
                    li['sweikaipiao'] += boom['sweikaipiao'][client_id]
                    li['sheji3'] += boom['sheji3'][client_id]
                for client_id in client:
                    li2['kaipiao'] += boom2['kaipiao'][client_id]
                    li2['shoukuanbukaipiao'] += boom2['shoukuanbukaipiao'][client_id]
                    li2['qty'] += boom2['qty'][client_id]
                    li2['tiaozheng'] += boom2['tiaozheng'][client_id]
                    li2['yinhang'] += boom2['yinhang'][client_id]
                    li2['xianjin'] += boom2['xianjin'][client_id]
                    li2['bukaipiao'] += boom2['bukaipiao'][client_id]
                    li2['shoukuankaipiao'] += boom2['shoukuankaipiao'][client_id]
                    li2['zhangmian'] += boom2['zhangmian'][client_id]
                    li2['amount'] += boom2['amount'][client_id]
                    li2['heji1'] += boom2['heji1'][client_id]
                    li2['heji2'] += boom2['heji2'][client_id]
                    li2['yuerbukaipiao'] += boom2['yuerbukaipiao'][client_id]
                    li2['weikaipiao'] += boom2['weikaipiao'][client_id]
                    li2['heji3'] += boom2['heji3'][client_id]
                    li2['heji4'] += boom2['heji4'][client_id]
                    li2['szhangmian'] += boom2['szhangmian'][client_id]
                    li2['syuerbukaipiao'] += boom2['syuerbukaipiao'][client_id]
                    li2['sweikaipiao'] += boom2['sweikaipiao'][client_id]
                    li2['sheji3'] += boom2['sheji3'][client_id]
            if data['form']['sorted_by'] == 'all':
                boom = {'kaipiao': {}, 'shoukuanbukaipiao': {}, 'price': {}, 'qty': {}, 'tiaozheng': {}, 'yinhang': {},
                        'xianjin': {}, 'bukaipiao': {}, 'shoukuankaipiao': {}, 'zhangmian': {}, 'amount': {},
                        'heji1': {},
                        'heji2': {}, 'yuerbukaipiao': {}, 'weikaipiao': {}, 'heji3': {}, 'heji4': {}, 'szhangmian': {},
                        'syuerbukaipiao': {}, 'sweikaipiao': {}, 'sheji3': {}, 'name': {}}
                boom2 = {'kaipiao': {}, 'shoukuanbukaipiao': {}, 'price': {}, 'qty': {}, 'tiaozheng': {}, 'yinhang': {},
                         'xianjin': {}, 'bukaipiao': {}, 'shoukuankaipiao': {}, 'zhangmian': {}, 'amount': {},
                         'heji1': {},
                         'heji2': {}, 'yuerbukaipiao': {}, 'weikaipiao': {}, 'heji3': {}, 'heji4': {}, 'szhangmian': {},
                         'syuerbukaipiao': {}, 'sweikaipiao': {}, 'sheji3': {}, 'name': {}}
                day = int(data['form']['year'][0:4]) * 100 + int(data['form']['date_from'])
                day2 = int(data['form']['year'][0:4]) * 100 + int(data['form']['date_to'])
                for record in self.env['hr.employee'].search([('department_id', '=',
                                                               self.env['hr.department'].search(
                                                                   [('name', '=', '销售部')]).id)]):
                    clients.append(record.id)
                    clients_name[record.id] = record.name
                    query = """
                                SELECT
                                    sum(g.qty) as qty,
                                    sum(g.price) as price,
                                    sum(g.qty*g.price) as amount,
                                    sum(g.kaipiao) as kaipiao,
                                    sum(g.bukaipiao) as bukaipiao,
                                    sum(g.yinhang) as yinhang,
                                    sum(g.tiaozheng) as tiaozheng,
                                    sum(g.xianjin) as xianjin,
                                    sum(g.shoukuankaipiao) as shoukuankaipiao,
                                    sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                FROM goose_order as g
                                WHERE g.month >= %s AND g.month <= %s AND g.yewu = %s AND g.bujiliang = FALSE AND g.company = 'ye'
                                """
                    query2 = """
                               SELECT
                                   sum(g.qty*g.price) as amount,
                                   sum(g.kaipiao) as kaipiao,
                                   sum(g.bukaipiao) as bukaipiao,
                                   sum(g.shoukuankaipiao) as shoukuankaipiao,
                                   sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                               FROM goose_order as g
                               WHERE g.month < %s AND g.yewu = %s AND g.bujiliang = FALSE AND g.company = 'ye'
                               """
                    self.env.cr.execute(query,
                                        tuple([day, day2, record.id]))
                    res = self.env.cr.dictfetchall()
                    self.env.cr.execute(query2, tuple([day, record.id]))
                    ress = self.env.cr.dictfetchall()
                    for r in res[0]:
                        if res[0][r] == None:
                            res[0][r] = 0
                    for r in ress[0]:
                        if ress[0][r] == None:
                            ress[0][r] = 0
                    client_id = record.id
                    if ress == []:
                        boom['sweikaipiao'][client_id] = 0
                        boom['syuerbukaipiao'][client_id] = 0
                        boom['szhangmian'][client_id] = 0
                        boom['sheji3'][client_id] = 0
                    for a in ress:
                        a['sweikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao'] or 0
                        a['syuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao'] or 0
                        a['szhangmian'] = a['kaipiao'] - a['shoukuankaipiao'] or 0
                        a['sheji3'] = a['sweikaipiao'] + a['syuerbukaipiao'] + a['szhangmian'] or 0
                        boom['sweikaipiao'][client_id] = a['sweikaipiao']
                        boom['syuerbukaipiao'][client_id] = a['syuerbukaipiao']
                        boom['szhangmian'][client_id] = a['szhangmian']
                        boom['sheji3'][client_id] = a['sheji3']
                    if res == []:
                        boom['amount'][client_id] = 0
                        boom['weikaipiao'][client_id] = 0
                        boom['yuerbukaipiao'][client_id] = 0
                        boom['zhangmian'][client_id] = 0
                        boom['heji1'][client_id] = 0
                        boom['heji2'][client_id] = 0
                        boom['heji3'][client_id] = 0
                        boom['heji4'][client_id] = 0
                        boom['qty'][client_id] = 0
                        boom['yinhang'][client_id] = 0
                        boom['xianjin'][client_id] = 0
                        boom['tiaozheng'][client_id] = 0
                        boom['shoukuankaipiao'][client_id] = 0
                        boom['shoukuanbukaipiao'][client_id] = 0
                        boom['kaipiao'][client_id] = 0
                        boom['bukaipiao'][client_id] = 0
                    for a in res:
                        a['weikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao'] or 0
                        a['yuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao'] or 0
                        a['zhangmian'] = a['kaipiao'] - a['shoukuankaipiao'] or 0
                        a['heji1'] = a['yinhang'] + a['xianjin'] + a['tiaozheng'] or 0
                        a['heji2'] = a['shoukuankaipiao'] + a['shoukuanbukaipiao'] or 0
                        a['heji3'] = a['weikaipiao'] + a['yuerbukaipiao'] + a['zhangmian'] or 0
                        a['heji4'] = a['kaipiao'] + a['bukaipiao'] or 0
                        boom['amount'][client_id] = a['amount']
                        boom['weikaipiao'][client_id] = a['weikaipiao']
                        boom['yuerbukaipiao'][client_id] = a['yuerbukaipiao']
                        boom['zhangmian'][client_id] = a['zhangmian']
                        boom['heji1'][client_id] = a['heji1']
                        boom['heji2'][client_id] = a['heji2']
                        boom['heji3'][client_id] = a['heji3']
                        boom['heji4'][client_id] = a['heji4']
                        boom['qty'][client_id] = a['qty'] or 0
                        boom['yinhang'][client_id] = a['yinhang'] or 0
                        boom['xianjin'][client_id] = a['xianjin'] or 0
                        boom['tiaozheng'][client_id] = a['tiaozheng'] or 0
                        boom['shoukuankaipiao'][client_id] = a['shoukuankaipiao'] or 0
                        boom['shoukuanbukaipiao'][client_id] = a['shoukuanbukaipiao'] or 0
                        boom['kaipiao'][client_id] = a['kaipiao'] or 0
                        boom['bukaipiao'][client_id] = a['bukaipiao'] or 0
                    query = """
                                                SELECT
                                                    sum(g.qty) as qty,
                                                    sum(g.price) as price,
                                                    sum(g.qty*g.price) as amount,
                                                    sum(g.kaipiao) as kaipiao,
                                                    sum(g.bukaipiao) as bukaipiao,
                                                    sum(g.yinhang) as yinhang,
                                                    sum(g.tiaozheng) as tiaozheng,
                                                    sum(g.xianjin) as xianjin,
                                                    sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                    sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                                FROM goose_order as g
                                                WHERE g.month >= %s AND g.month <= %s AND g.yewu = %s AND g.bujiliang = FALSE AND g.company = 'tian'
                                                """
                    query2 = """
                                               SELECT
                                                   sum(g.qty*g.price) as amount,
                                                   sum(g.kaipiao) as kaipiao,
                                                   sum(g.bukaipiao) as bukaipiao,
                                                   sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                   sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                               FROM goose_order as g
                                               WHERE g.month < %s AND g.yewu = %s AND g.bujiliang = FALSE AND g.company = 'tian'
                                               """
                    self.env.cr.execute(query,
                                        tuple([day, day2, record.id]))
                    res = self.env.cr.dictfetchall()
                    self.env.cr.execute(query2, tuple([day, record.id]))
                    ress = self.env.cr.dictfetchall()
                    for r in res[0]:
                        if res[0][r] == None:
                            res[0][r] = 0
                    for r in ress[0]:
                        if ress[0][r] == None:
                            ress[0][r] = 0
                    if ress == []:
                        boom2['sweikaipiao'][client_id] = 0
                        boom2['syuerbukaipiao'][client_id] = 0
                        boom2['szhangmian'][client_id] = 0
                        boom2['sheji3'][client_id] = 0
                    for a in ress:
                        a['sweikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao'] or 0
                        a['syuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao'] or 0
                        a['szhangmian'] = a['kaipiao'] - a['shoukuankaipiao'] or 0
                        a['sheji3'] = a['sweikaipiao'] + a['syuerbukaipiao'] + a['szhangmian'] or 0
                        boom2['sweikaipiao'][client_id] = a['sweikaipiao']
                        boom2['syuerbukaipiao'][client_id] = a['syuerbukaipiao']
                        boom2['szhangmian'][client_id] = a['szhangmian']
                        boom2['sheji3'][client_id] = a['sheji3']
                    if res == []:
                        boom2['amount'][client_id] = 0
                        boom2['weikaipiao'][client_id] = 0
                        boom2['yuerbukaipiao'][client_id] = 0
                        boom2['zhangmian'][client_id] = 0
                        boom2['heji1'][client_id] = 0
                        boom2['heji2'][client_id] = 0
                        boom2['heji3'][client_id] = 0
                        boom2['heji4'][client_id] = 0
                        boom2['qty'][client_id] = 0
                        boom2['yinhang'][client_id] = 0
                        boom2['xianjin'][client_id] = 0
                        boom2['tiaozheng'][client_id] = 0
                        boom2['shoukuankaipiao'][client_id] = 0
                        boom2['shoukuanbukaipiao'][client_id] = 0
                        boom2['kaipiao'][client_id] = 0
                        boom2['bukaipiao'][client_id] = 0
                    for a in res:
                        a['weikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao'] or 0
                        a['yuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao'] or 0
                        a['zhangmian'] = a['kaipiao'] - a['shoukuankaipiao'] or 0
                        a['heji1'] = a['yinhang'] + a['xianjin'] + a['tiaozheng'] or 0
                        a['heji2'] = a['shoukuankaipiao'] + a['shoukuanbukaipiao'] or 0
                        a['heji3'] = a['weikaipiao'] + a['yuerbukaipiao'] + a['zhangmian'] or 0
                        a['heji4'] = a['kaipiao'] + a['bukaipiao'] or 0
                        boom2['amount'][client_id] = a['amount']
                        boom2['weikaipiao'][client_id] = a['weikaipiao']
                        boom2['yuerbukaipiao'][client_id] = a['yuerbukaipiao']
                        boom2['zhangmian'][client_id] = a['zhangmian']
                        boom2['heji1'][client_id] = a['heji1']
                        boom2['heji2'][client_id] = a['heji2']
                        boom2['heji3'][client_id] = a['heji3']
                        boom2['heji4'][client_id] = a['heji4']
                        boom2['qty'][client_id] = a['qty'] or 0
                        boom2['yinhang'][client_id] = a['yinhang'] or 0
                        boom2['xianjin'][client_id] = a['xianjin'] or 0
                        boom2['tiaozheng'][client_id] = a['tiaozheng'] or 0
                        boom2['shoukuankaipiao'][client_id] = a['shoukuankaipiao'] or 0
                        boom2['shoukuanbukaipiao'][client_id] = a['shoukuanbukaipiao'] or 0
                        boom2['kaipiao'][client_id] = a['kaipiao'] or 0
                        boom2['bukaipiao'][client_id] = a['bukaipiao'] or 0
                    boom['name'][record.id] = record.name
                    boom2['name'][record.id] = record.name
                for client_id in clients:
                    li['kaipiao'] += boom['kaipiao'][client_id]
                    li['shoukuanbukaipiao'] += boom['shoukuanbukaipiao'][client_id]
                    li['qty'] += boom['qty'][client_id]
                    li['tiaozheng'] += boom['tiaozheng'][client_id]
                    li['yinhang'] += boom['yinhang'][client_id]
                    li['xianjin'] += boom['xianjin'][client_id]
                    li['bukaipiao'] += boom['bukaipiao'][client_id]
                    li['shoukuankaipiao'] += boom['shoukuankaipiao'][client_id]
                    li['zhangmian'] += boom['zhangmian'][client_id]
                    li['amount'] += boom['amount'][client_id]
                    li['heji1'] += boom['heji1'][client_id]
                    li['heji2'] += boom['heji2'][client_id]
                    li['yuerbukaipiao'] += boom['yuerbukaipiao'][client_id]
                    li['weikaipiao'] += boom['weikaipiao'][client_id]
                    li['heji3'] += boom['heji3'][client_id]
                    li['heji4'] += boom['heji4'][client_id]
                    li['szhangmian'] += boom['szhangmian'][client_id]
                    li['syuerbukaipiao'] += boom['syuerbukaipiao'][client_id]
                    li['sweikaipiao'] += boom['sweikaipiao'][client_id]
                    li['sheji3'] += boom['sheji3'][client_id]
                for client_id in clients:
                    li2['kaipiao'] += boom2['kaipiao'][client_id]
                    li2['shoukuanbukaipiao'] += boom2['shoukuanbukaipiao'][client_id]
                    li2['qty'] += boom2['qty'][client_id]
                    li2['tiaozheng'] += boom2['tiaozheng'][client_id]
                    li2['yinhang'] += boom2['yinhang'][client_id]
                    li2['xianjin'] += boom2['xianjin'][client_id]
                    li2['bukaipiao'] += boom2['bukaipiao'][client_id]
                    li2['shoukuankaipiao'] += boom2['shoukuankaipiao'][client_id]
                    li2['zhangmian'] += boom2['zhangmian'][client_id]
                    li2['amount'] += boom2['amount'][client_id]
                    li2['heji1'] += boom2['heji1'][client_id]
                    li2['heji2'] += boom2['heji2'][client_id]
                    li2['yuerbukaipiao'] += boom2['yuerbukaipiao'][client_id]
                    li2['weikaipiao'] += boom2['weikaipiao'][client_id]
                    li2['heji3'] += boom2['heji3'][client_id]
                    li2['heji4'] += boom2['heji4'][client_id]
                    li2['szhangmian'] += boom2['szhangmian'][client_id]
                    li2['syuerbukaipiao'] += boom2['syuerbukaipiao'][client_id]
                    li2['sweikaipiao'] += boom2['sweikaipiao'][client_id]
                    li2['sheji3'] += boom2['sheji3'][client_id]
        else:
            if data['form']['sorted_by'] == 'month':
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        date.append(x)
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_pay as g
                                            WHERE g.month = %s AND g.company = 'ye'
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_pay as g
                                            WHERE g.month < %s AND g.company = 'ye'
                                            """
                        self.env.cr.execute(query2, tuple([year + int(x)]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([year + int(x)]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']
                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom[a][x] = res[0][a]
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_pay as g
                                            WHERE g.month = %s AND g.company = 'tian'
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_pay as g
                                            WHERE g.month < %s AND g.company = 'tian'
                                            """
                        self.env.cr.execute(query2, tuple([year + int(x)]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([year + int(x)]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']

                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom2[a][x] = res[0][a]
                for client_id in date:
                    li['kaipiao'] += boom['kaipiao'][client_id]
                    li['shoukuanbukaipiao'] += boom['shoukuanbukaipiao'][client_id]
                    li['qty'] += boom['qty'][client_id]
                    li['tiaozheng'] += boom['tiaozheng'][client_id]
                    li['yinhang'] += boom['yinhang'][client_id]
                    li['xianjin'] += boom['xianjin'][client_id]
                    li['bukaipiao'] += boom['bukaipiao'][client_id]
                    li['shoukuankaipiao'] += boom['shoukuankaipiao'][client_id]
                    li['zhangmian'] = boom['zhangmian'][client_id]
                    li['amount'] += boom['amount'][client_id]
                    li['heji1'] += boom['heji1'][client_id]
                    li['heji2'] += boom['heji2'][client_id]
                    li['yuerbukaipiao'] = boom['yuerbukaipiao'][client_id]
                    li['weikaipiao'] = boom['weikaipiao'][client_id]
                    li['heji3'] = boom['heji3'][client_id]
                    li['heji4'] += boom['heji4'][client_id]
                    li['szhangmian'] += boom['szhangmian'][client_id]
                    li['syuerbukaipiao'] += boom['syuerbukaipiao'][client_id]
                    li['sweikaipiao'] += boom['sweikaipiao'][client_id]
                    li['sheji3'] += boom['sheji3'][client_id]
                for client_id in date:
                    li2['kaipiao'] += boom2['kaipiao'][client_id]
                    li2['shoukuanbukaipiao'] += boom2['shoukuanbukaipiao'][client_id]
                    li2['qty'] += boom2['qty'][client_id]
                    li2['tiaozheng'] += boom2['tiaozheng'][client_id]
                    li2['yinhang'] += boom2['yinhang'][client_id]
                    li2['xianjin'] += boom2['xianjin'][client_id]
                    li2['bukaipiao'] += boom2['bukaipiao'][client_id]
                    li2['shoukuankaipiao'] += boom2['shoukuankaipiao'][client_id]
                    li2['zhangmian'] = boom2['zhangmian'][client_id]
                    li2['amount'] += boom2['amount'][client_id]
                    li2['heji1'] += boom2['heji1'][client_id]
                    li2['heji2'] += boom2['heji2'][client_id]
                    li2['yuerbukaipiao'] = boom2['yuerbukaipiao'][client_id]
                    li2['weikaipiao'] = boom2['weikaipiao'][client_id]
                    li2['heji3'] = boom2['heji3'][client_id]
                    li2['heji4'] += boom2['heji4'][client_id]
                    li2['szhangmian'] += boom2['szhangmian'][client_id]
                    li2['syuerbukaipiao'] += boom2['syuerbukaipiao'][client_id]
                    li2['sweikaipiao'] += boom2['sweikaipiao'][client_id]
                    li2['sheji3'] += boom2['sheji3'][client_id]

        docargs = {
            'date': date,
            'res': boom,
            'res2': boom2,
            'client': client,
            'clients': clients,
            'name': clients_name,
            'data': data,
            'company': ['ye', 'tian'],
            's': li,
            's2': li2,
            'month': month,
        }
        return self.env['report'].render('goose.report_gooseorder', docargs)


class GooseOrderReportYewu(models.AbstractModel):
    _name = 'report.goose.my_report_yewu'

    @api.model
    def render_html(self, docids, data=None):
        year = int(data['form']['year'][0:4]) * 100
        month = {'01': '一月', '02': '二月', '03': '三月', '04': '四月', '05': '五月', '06': '六月', '07': '七月', '08': '八月',
                 '09': '九月', '10': '十月', '11': '十一月', '12': '十二月'}
        month3 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        boom = {'kaipiao': {}, 'shoukuanbukaipiao': {}, 'price': {}, 'qty': {}, 'tiaozheng': {}, 'yinhang': {},
                'xianjin': {}, 'bukaipiao': {}, 'shoukuankaipiao': {}, 'zhangmian': {}, 'amount': {}, 'heji1': {},
                'heji2': {}, 'yuerbukaipiao': {}, 'weikaipiao': {}, 'heji3': {}, 'heji4': {}, 'szhangmian': {},
                'syuerbukaipiao': {}, 'sweikaipiao': {}, 'sheji3': {}}
        boom2 = {'kaipiao': {}, 'shoukuanbukaipiao': {}, 'price': {}, 'qty': {}, 'tiaozheng': {}, 'yinhang': {},
                 'xianjin': {}, 'bukaipiao': {}, 'shoukuankaipiao': {}, 'zhangmian': {}, 'amount': {}, 'heji1': {},
                 'heji2': {}, 'yuerbukaipiao': {}, 'weikaipiao': {}, 'heji3': {}, 'heji4': {}, 'szhangmian': {},
                 'syuerbukaipiao': {}, 'sweikaipiao': {}, 'sheji3': {}}
        li = {'kaipiao': 0, 'shoukuanbukaipiao': 0, 'price': 0, 'qty': 0, 'tiaozheng': 0, 'yinhang': 0,
              'xianjin': 0, 'bukaipiao': 0, 'shoukuankaipiao': 0, 'zhangmian': 0, 'amount': 0, 'heji1': 0,
              'heji2': 0, 'yuerbukaipiao': 0, 'weikaipiao': 0, 'heji3': 0, 'heji4': 0, 'szhangmian': 0,
              'syuerbukaipiao': 0, 'sweikaipiao': 0, 'sheji3': 0}
        li2 = {'kaipiao': 0, 'shoukuanbukaipiao': 0, 'price': 0, 'qty': 0, 'tiaozheng': 0, 'yinhang': 0,
               'xianjin': 0, 'bukaipiao': 0, 'shoukuankaipiao': 0, 'zhangmian': 0, 'amount': 0, 'heji1': 0,
               'heji2': 0, 'yuerbukaipiao': 0, 'weikaipiao': 0, 'heji3': 0, 'heji4': 0, 'szhangmian': 0,
               'syuerbukaipiao': 0, 'sweikaipiao': 0, 'sheji3': 0}
        date = []
        client = []
        clients = []
        clients_name = {}
        if data['form']['result_selection'] == 'customer':
            if data['form']['yewu']:
                for record in self.env['goose.client'].search([('yewu', '=', data['form']['yewu'][0])]):
                    client.append(record.name)
            if data['form']['sorted_by'] == 'month' and data['form']['yewu'] == False:
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        date.append(x)
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_yewu as g
                                            WHERE g.month = %s AND g.company = 'ye'
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_yewu as g
                                            WHERE g.month < %s AND g.company = 'ye'
                                            """
                        self.env.cr.execute(query2, tuple([year + int(x)]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([year + int(x)]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']
                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom[a][x] = res[0][a]
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_yewu as g
                                            WHERE g.month = %s AND g.company = 'tian'
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_yewu as g
                                            WHERE g.month < %s AND g.company = 'tian'
                                            """
                        self.env.cr.execute(query2, tuple([year + int(x)]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([year + int(x)]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']

                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom2[a][x] = res[0][a]
                for client_id in date:
                    li['kaipiao'] += boom['kaipiao'][client_id]
                    li['shoukuanbukaipiao'] += boom['shoukuanbukaipiao'][client_id]
                    li['qty'] += boom['qty'][client_id]
                    li['tiaozheng'] += boom['tiaozheng'][client_id]
                    li['yinhang'] += boom['yinhang'][client_id]
                    li['xianjin'] += boom['xianjin'][client_id]
                    li['bukaipiao'] += boom['bukaipiao'][client_id]
                    li['shoukuankaipiao'] += boom['shoukuankaipiao'][client_id]
                    li['zhangmian'] = boom['zhangmian'][client_id]
                    li['amount'] += boom['amount'][client_id]
                    li['heji1'] += boom['heji1'][client_id]
                    li['heji2'] += boom['heji2'][client_id]
                    li['yuerbukaipiao'] = boom['yuerbukaipiao'][client_id]
                    li['weikaipiao'] = boom['weikaipiao'][client_id]
                    li['heji3'] = boom['heji3'][client_id]
                    li['heji4'] += boom['heji4'][client_id]
                    li['szhangmian'] += boom['szhangmian'][client_id]
                    li['syuerbukaipiao'] += boom['syuerbukaipiao'][client_id]
                    li['sweikaipiao'] += boom['sweikaipiao'][client_id]
                    li['sheji3'] += boom['sheji3'][client_id]
                for client_id in date:
                    li2['kaipiao'] += boom2['kaipiao'][client_id]
                    li2['shoukuanbukaipiao'] += boom2['shoukuanbukaipiao'][client_id]
                    li2['qty'] += boom2['qty'][client_id]
                    li2['tiaozheng'] += boom2['tiaozheng'][client_id]
                    li2['yinhang'] += boom2['yinhang'][client_id]
                    li2['xianjin'] += boom2['xianjin'][client_id]
                    li2['bukaipiao'] += boom2['bukaipiao'][client_id]
                    li2['shoukuankaipiao'] += boom2['shoukuankaipiao'][client_id]
                    li2['zhangmian'] = boom2['zhangmian'][client_id]
                    li2['amount'] += boom2['amount'][client_id]
                    li2['heji1'] += boom2['heji1'][client_id]
                    li2['heji2'] += boom2['heji2'][client_id]
                    li2['yuerbukaipiao'] = boom2['yuerbukaipiao'][client_id]
                    li2['weikaipiao'] = boom2['weikaipiao'][client_id]
                    li2['heji3'] = boom2['heji3'][client_id]
                    li2['heji4'] += boom2['heji4'][client_id]
                    li2['szhangmian'] += boom2['szhangmian'][client_id]
                    li2['syuerbukaipiao'] += boom2['syuerbukaipiao'][client_id]
                    li2['sweikaipiao'] += boom2['sweikaipiao'][client_id]
                    li2['sheji3'] += boom2['sheji3'][client_id]
            elif data['form']['sorted_by'] == 'month' and data['form']['yewu']:
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        date.append(x)
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_yewu as g
                                            WHERE g.month = %s AND g.company = 'ye' AND g.yewu = %s
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_yewu as g
                                            WHERE g.month < %s AND g.company = 'ye' AND g.yewu = %s
                                            """
                        self.env.cr.execute(query2, tuple([(year + int(x)), data['form']['yewu'][0]]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([(year + int(x)), data['form']['yewu'][0]]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']
                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom[a][x] = res[0][a]
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_yewu as g
                                            WHERE g.month = %s AND g.company = 'tian' AND g.yewu = %s
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_yewu as g
                                            WHERE g.month < %s AND g.company = 'tian' AND g.yewu = %s
                                            """
                        self.env.cr.execute(query2, tuple([(year + int(x)), data['form']['yewu'][0]]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([(year + int(x)), data['form']['yewu'][0]]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']

                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom2[a][x] = res[0][a]
                for client_id in date:
                    li['kaipiao'] += boom['kaipiao'][client_id]
                    li['shoukuanbukaipiao'] += boom['shoukuanbukaipiao'][client_id]
                    li['qty'] += boom['qty'][client_id]
                    li['tiaozheng'] += boom['tiaozheng'][client_id]
                    li['yinhang'] += boom['yinhang'][client_id]
                    li['xianjin'] += boom['xianjin'][client_id]
                    li['bukaipiao'] += boom['bukaipiao'][client_id]
                    li['shoukuankaipiao'] += boom['shoukuankaipiao'][client_id]
                    li['zhangmian'] = boom['zhangmian'][client_id]
                    li['amount'] += boom['amount'][client_id]
                    li['heji1'] += boom['heji1'][client_id]
                    li['heji2'] += boom['heji2'][client_id]
                    li['yuerbukaipiao'] = boom['yuerbukaipiao'][client_id]
                    li['weikaipiao'] = boom['weikaipiao'][client_id]
                    li['heji3'] = boom['heji3'][client_id]
                    li['heji4'] += boom['heji4'][client_id]
                    li['szhangmian'] += boom['szhangmian'][client_id]
                    li['syuerbukaipiao'] += boom['syuerbukaipiao'][client_id]
                    li['sweikaipiao'] += boom['sweikaipiao'][client_id]
                    li['sheji3'] += boom['sheji3'][client_id]
                for client_id in date:
                    li2['kaipiao'] += boom2['kaipiao'][client_id]
                    li2['shoukuanbukaipiao'] += boom2['shoukuanbukaipiao'][client_id]
                    li2['qty'] += boom2['qty'][client_id]
                    li2['tiaozheng'] += boom2['tiaozheng'][client_id]
                    li2['yinhang'] += boom2['yinhang'][client_id]
                    li2['xianjin'] += boom2['xianjin'][client_id]
                    li2['bukaipiao'] += boom2['bukaipiao'][client_id]
                    li2['shoukuankaipiao'] += boom2['shoukuankaipiao'][client_id]
                    li2['zhangmian'] = boom2['zhangmian'][client_id]
                    li2['amount'] += boom2['amount'][client_id]
                    li2['heji1'] += boom2['heji1'][client_id]
                    li2['heji2'] += boom2['heji2'][client_id]
                    li2['yuerbukaipiao'] = boom2['yuerbukaipiao'][client_id]
                    li2['weikaipiao'] = boom2['weikaipiao'][client_id]
                    li2['heji3'] = boom2['heji3'][client_id]
                    li2['heji4'] += boom2['heji4'][client_id]
                    li2['szhangmian'] += boom2['szhangmian'][client_id]
                    li2['syuerbukaipiao'] += boom2['syuerbukaipiao'][client_id]
                    li2['sweikaipiao'] += boom2['sweikaipiao'][client_id]
                    li2['sheji3'] += boom2['sheji3'][client_id]
            elif data['form']['sorted_by'] == 'people':
                for client_id in client:
                    x = self.env['goose.client'].search([('name', '=', client_id)]).id
                    query = """
                                        SELECT
                                            sum(g.qty) as qty,
                                            sum(g.price) as price,
                                            sum(g.price*g.qty) as amount,
                                            sum(g.kaipiao) as kaipiao,
                                            sum(g.bukaipiao) as bukaipiao,
                                            sum(g.yinhang) as yinhang,
                                            sum(g.tiaozheng) as tiaozheng,
                                            sum(g.xianjin) as xianjin,
                                            sum(g.shoukuankaipiao) as shoukuankaipiao,
                                            sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                        FROM goose_order_yewu as g
                                        WHERE g.month >= %s AND g.month <= %s AND g.yewu = %s AND g.client_id = %s AND g.bujiliang = FALSE AND g.company = 'ye'
                                        """
                    query2 = """
                                SELECT
                                    sum(g.qty) as qty,
                                    sum(g.price) as price,
                                    sum(g.price*g.qty) as amount,
                                    sum(g.kaipiao) as kaipiao,
                                    sum(g.bukaipiao) as bukaipiao,
                                    sum(g.yinhang) as yinhang,
                                    sum(g.tiaozheng) as tiaozheng,
                                    sum(g.xianjin) as xianjin,
                                    sum(g.shoukuankaipiao) as shoukuankaipiao,
                                    sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                FROM goose_order_yewu as g
                                WHERE g.month < %s AND g.yewu = %s AND g.client_id = %s AND g.bujiliang = FALSE AND g.company = 'ye'
                                """
                    day = int(data['form']['year'][0:4]) * 100 + int(data['form']['date_from'])
                    day2 = int(data['form']['year'][0:4]) * 100 + int(data['form']['date_to'])
                    self.env.cr.execute(query,
                                        tuple([day, day2, data['form']['yewu'][0], x]))
                    res = self.env.cr.dictfetchall()
                    self.env.cr.execute(query2,
                                        tuple([day, data['form']['yewu'][0], x]))
                    ress = self.env.cr.dictfetchall()
                    for r in res[0]:
                        if res[0][r] == None:
                            res[0][r] = 0
                    for r in ress[0]:
                        if ress[0][r] == None:
                            ress[0][r] = 0

                    if ress == []:
                        boom['sweikaipiao'][client_id] = 0
                        boom['syuerbukaipiao'][client_id] = 0
                        boom['szhangmian'][client_id] = 0
                        boom['sheji3'][client_id] = 0

                    for a in ress:
                        a['sweikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao'] or 0
                        a['syuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao'] or 0
                        a['szhangmian'] = a['kaipiao'] - a['shoukuankaipiao'] or 0
                        a['sheji3'] = a['sweikaipiao'] + a['syuerbukaipiao'] + a['szhangmian'] or 0
                        boom['sweikaipiao'][client_id] = a['sweikaipiao']
                        boom['syuerbukaipiao'][client_id] = a['syuerbukaipiao']
                        boom['szhangmian'][client_id] = a['szhangmian']
                        boom['sheji3'][client_id] = a['sheji3']
                    if res == []:
                        boom['amount'][client_id] = 0
                        boom['weikaipiao'][client_id] = 0
                        boom['yuerbukaipiao'][client_id] = 0
                        boom['zhangmian'][client_id] = 0
                        boom['heji1'][client_id] = 0
                        boom['heji2'][client_id] = 0
                        boom['heji3'][client_id] = 0
                        boom['heji4'][client_id] = 0
                        boom['qty'][client_id] = 0
                        boom['yinhang'][client_id] = 0
                        boom['xianjin'][client_id] = 0
                        boom['tiaozheng'][client_id] = 0
                        boom['shoukuankaipiao'][client_id] = 0
                        boom['shoukuanbukaipiao'][client_id] = 0
                        boom['kaipiao'][client_id] = 0
                        boom['bukaipiao'][client_id] = 0
                    print res
                    for a in res:
                        a['weikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao']
                        a['yuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao']
                        a['zhangmian'] = a['kaipiao'] - a['shoukuankaipiao']
                        a['heji1'] = a['yinhang'] + a['xianjin'] + a['tiaozheng']
                        a['heji2'] = a['shoukuankaipiao'] + a['shoukuanbukaipiao']
                        a['heji3'] = a['weikaipiao'] + a['yuerbukaipiao'] + a['zhangmian']
                        a['heji4'] = a['kaipiao'] + a['bukaipiao']
                        boom['amount'][client_id] = a['amount']
                        boom['weikaipiao'][client_id] = a['weikaipiao']
                        boom['yuerbukaipiao'][client_id] = a['yuerbukaipiao']
                        boom['zhangmian'][client_id] = a['zhangmian']
                        boom['heji1'][client_id] = a['heji1']
                        boom['heji2'][client_id] = a['heji2']
                        boom['heji3'][client_id] = a['heji3']
                        boom['heji4'][client_id] = a['heji4']
                        boom['qty'][client_id] = a['qty']
                        boom['yinhang'][client_id] = a['yinhang']
                        boom['xianjin'][client_id] = a['xianjin']
                        boom['tiaozheng'][client_id] = a['tiaozheng']
                        boom['shoukuankaipiao'][client_id] = a['shoukuankaipiao']
                        boom['shoukuanbukaipiao'][client_id] = a['shoukuanbukaipiao']
                        boom['kaipiao'][client_id] = a['kaipiao']
                        boom['bukaipiao'][client_id] = a['bukaipiao']
                    query = """
                                    SELECT
                                        sum(g.qty) as qty,
                                        sum(g.price) as price,
                                        sum(g.price*g.qty) as amount,
                                        sum(g.kaipiao) as kaipiao,
                                        sum(g.bukaipiao) as bukaipiao,
                                        sum(g.yinhang) as yinhang,
                                        sum(g.tiaozheng) as tiaozheng,
                                        sum(g.xianjin) as xianjin,
                                        sum(g.shoukuankaipiao) as shoukuankaipiao,
                                        sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                    FROM goose_order_yewu as g
                                    WHERE g.month >= %s AND g.month <= %s AND g.yewu = %s AND g.client_id = %s AND g.bujiliang = FALSE AND g.company = 'tian'
                                    """
                    query2 = """
                                    SELECT
                                    sum(g.qty) as qty,
                                    sum(g.price) as price,
                                    sum(g.price*g.qty) as amount,
                                    sum(g.kaipiao) as kaipiao,
                                    sum(g.bukaipiao) as bukaipiao,
                                    sum(g.yinhang) as yinhang,
                                    sum(g.tiaozheng) as tiaozheng,
                                    sum(g.xianjin) as xianjin,
                                    sum(g.shoukuankaipiao) as shoukuankaipiao,
                                    sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                    FROM goose_order_yewu as g
                                    WHERE g.month < %s AND g.yewu = %s AND g.client_id = %s AND g.bujiliang = FALSE AND g.company = 'tian'
                                    """
                    self.env.cr.execute(query,
                                        tuple([day, day2, data['form']['yewu'][0], x]))
                    res = self.env.cr.dictfetchall()
                    self.env.cr.execute(query2,
                                        tuple([day, data['form']['yewu'][0], x]))
                    ress = self.env.cr.dictfetchall()
                    for r in res[0]:
                        if res[0][r] == None:
                            res[0][r] = 0
                    for r in ress[0]:
                        if ress[0][r] == None:
                            ress[0][r] = 0
                    if ress == []:
                        boom2['sweikaipiao'][client_id] = 0
                        boom2['syuerbukaipiao'][client_id] = 0
                        boom2['szhangmian'][client_id] = 0
                        boom2['sheji3'][client_id] = 0
                    for a in ress:
                        a['sweikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao']
                        a['syuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao']
                        a['szhangmian'] = a['kaipiao'] - a['shoukuankaipiao']
                        a['sheji3'] = a['sweikaipiao'] + a['syuerbukaipiao'] + a['szhangmian']
                        boom2['sweikaipiao'][client_id] = a['sweikaipiao']
                        boom2['syuerbukaipiao'][client_id] = a['syuerbukaipiao']
                        boom2['szhangmian'][client_id] = a['szhangmian']
                        boom2['sheji3'][client_id] = a['sheji3']
                    if res == []:
                        boom2['amount'][client_id] = 0
                        boom2['weikaipiao'][client_id] = 0
                        boom2['yuerbukaipiao'][client_id] = 0
                        boom2['zhangmian'][client_id] = 0
                        boom2['heji1'][client_id] = 0
                        boom2['heji2'][client_id] = 0
                        boom2['heji3'][client_id] = 0
                        boom2['heji4'][client_id] = 0
                        boom2['qty'][client_id] = 0
                        boom2['yinhang'][client_id] = 0
                        boom2['xianjin'][client_id] = 0
                        boom2['tiaozheng'][client_id] = 0
                        boom2['shoukuankaipiao'][client_id] = 0
                        boom2['shoukuanbukaipiao'][client_id] = 0
                        boom2['kaipiao'][client_id] = 0
                        boom2['bukaipiao'][client_id] = 0
                    for a in res:
                        a['weikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao']
                        a['yuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao']
                        a['zhangmian'] = a['kaipiao'] - a['shoukuankaipiao']
                        a['heji1'] = a['yinhang'] + a['xianjin'] + a['tiaozheng']
                        a['heji2'] = a['shoukuankaipiao'] + a['shoukuanbukaipiao']
                        a['heji3'] = a['weikaipiao'] + a['yuerbukaipiao'] + a['zhangmian']
                        a['heji4'] = a['kaipiao'] + a['bukaipiao']
                        boom2['amount'][client_id] = a['amount']
                        boom2['weikaipiao'][client_id] = a['weikaipiao']
                        boom2['yuerbukaipiao'][client_id] = a['yuerbukaipiao']
                        boom2['zhangmian'][client_id] = a['zhangmian']
                        boom2['heji1'][client_id] = a['heji1']
                        boom2['heji2'][client_id] = a['heji2']
                        boom2['heji3'][client_id] = a['heji3']
                        boom2['heji4'][client_id] = a['heji4']
                        boom2['qty'][client_id] = a['qty']
                        boom2['yinhang'][client_id] = a['yinhang']
                        boom2['xianjin'][client_id] = a['xianjin']
                        boom2['tiaozheng'][client_id] = a['tiaozheng']
                        boom2['shoukuankaipiao'][client_id] = a['shoukuankaipiao']
                        boom2['shoukuanbukaipiao'][client_id] = a['shoukuanbukaipiao']
                        boom2['kaipiao'][client_id] = a['kaipiao']
                        boom2['bukaipiao'][client_id] = a['bukaipiao']
                for client_id in client:
                    li['kaipiao'] += boom['kaipiao'][client_id]
                    li['shoukuanbukaipiao'] += boom['shoukuanbukaipiao'][client_id]
                    li['qty'] += boom['qty'][client_id]
                    li['tiaozheng'] += boom['tiaozheng'][client_id]
                    li['yinhang'] += boom['yinhang'][client_id]
                    li['xianjin'] += boom['xianjin'][client_id]
                    li['bukaipiao'] += boom['bukaipiao'][client_id]
                    li['shoukuankaipiao'] += boom['shoukuankaipiao'][client_id]
                    li['zhangmian'] += boom['zhangmian'][client_id]
                    li['amount'] += boom['amount'][client_id]
                    li['heji1'] += boom['heji1'][client_id]
                    li['heji2'] += boom['heji2'][client_id]
                    li['yuerbukaipiao'] += boom['yuerbukaipiao'][client_id]
                    li['weikaipiao'] += boom['weikaipiao'][client_id]
                    li['heji3'] += boom['heji3'][client_id]
                    li['heji4'] += boom['heji4'][client_id]
                    li['szhangmian'] += boom['szhangmian'][client_id]
                    li['syuerbukaipiao'] += boom['syuerbukaipiao'][client_id]
                    li['sweikaipiao'] += boom['sweikaipiao'][client_id]
                    li['sheji3'] += boom['sheji3'][client_id]
                for client_id in client:
                    li2['kaipiao'] += boom2['kaipiao'][client_id]
                    li2['shoukuanbukaipiao'] += boom2['shoukuanbukaipiao'][client_id]
                    li2['qty'] += boom2['qty'][client_id]
                    li2['tiaozheng'] += boom2['tiaozheng'][client_id]
                    li2['yinhang'] += boom2['yinhang'][client_id]
                    li2['xianjin'] += boom2['xianjin'][client_id]
                    li2['bukaipiao'] += boom2['bukaipiao'][client_id]
                    li2['shoukuankaipiao'] += boom2['shoukuankaipiao'][client_id]
                    li2['zhangmian'] += boom2['zhangmian'][client_id]
                    li2['amount'] += boom2['amount'][client_id]
                    li2['heji1'] += boom2['heji1'][client_id]
                    li2['heji2'] += boom2['heji2'][client_id]
                    li2['yuerbukaipiao'] += boom2['yuerbukaipiao'][client_id]
                    li2['weikaipiao'] += boom2['weikaipiao'][client_id]
                    li2['heji3'] += boom2['heji3'][client_id]
                    li2['heji4'] += boom2['heji4'][client_id]
                    li2['szhangmian'] += boom2['szhangmian'][client_id]
                    li2['syuerbukaipiao'] += boom2['syuerbukaipiao'][client_id]
                    li2['sweikaipiao'] += boom2['sweikaipiao'][client_id]
                    li2['sheji3'] += boom2['sheji3'][client_id]
            if data['form']['sorted_by'] == 'all':
                boom = {'kaipiao': {}, 'shoukuanbukaipiao': {}, 'price': {}, 'qty': {}, 'tiaozheng': {}, 'yinhang': {},
                        'xianjin': {}, 'bukaipiao': {}, 'shoukuankaipiao': {}, 'zhangmian': {}, 'amount': {},
                        'heji1': {},
                        'heji2': {}, 'yuerbukaipiao': {}, 'weikaipiao': {}, 'heji3': {}, 'heji4': {}, 'szhangmian': {},
                        'syuerbukaipiao': {}, 'sweikaipiao': {}, 'sheji3': {}, 'name': {}}
                boom2 = {'kaipiao': {}, 'shoukuanbukaipiao': {}, 'price': {}, 'qty': {}, 'tiaozheng': {}, 'yinhang': {},
                         'xianjin': {}, 'bukaipiao': {}, 'shoukuankaipiao': {}, 'zhangmian': {}, 'amount': {},
                         'heji1': {},
                         'heji2': {}, 'yuerbukaipiao': {}, 'weikaipiao': {}, 'heji3': {}, 'heji4': {}, 'szhangmian': {},
                         'syuerbukaipiao': {}, 'sweikaipiao': {}, 'sheji3': {}, 'name': {}}
                day = int(data['form']['year'][0:4]) * 100 + int(data['form']['date_from'])
                day2 = int(data['form']['year'][0:4]) * 100 + int(data['form']['date_to'])
                for record in self.env['hr.employee'].search([('department_id', '=',
                                                               self.env['hr.department'].search(
                                                                   [('name', '=', '销售部')]).id)]):
                    clients.append(record.id)
                    clients_name[record.id] = record.name
                    query = """
                                SELECT
                                    sum(g.qty) as qty,
                                    sum(g.price) as price,
                                    sum(g.qty*g.price) as amount,
                                    sum(g.kaipiao) as kaipiao,
                                    sum(g.bukaipiao) as bukaipiao,
                                    sum(g.yinhang) as yinhang,
                                    sum(g.tiaozheng) as tiaozheng,
                                    sum(g.xianjin) as xianjin,
                                    sum(g.shoukuankaipiao) as shoukuankaipiao,
                                    sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                FROM goose_order_yewu as g
                                WHERE g.month >= %s AND g.month <= %s AND g.yewu = %s AND g.bujiliang = FALSE AND g.company = 'ye'
                                """
                    query2 = """
                               SELECT
                                   sum(g.qty*g.price) as amount,
                                   sum(g.kaipiao) as kaipiao,
                                   sum(g.bukaipiao) as bukaipiao,
                                   sum(g.shoukuankaipiao) as shoukuankaipiao,
                                   sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                               FROM goose_order_yewu as g
                               WHERE g.month < %s AND g.yewu = %s AND g.bujiliang = FALSE AND g.company = 'ye'
                               """
                    self.env.cr.execute(query,
                                        tuple([day, day2, record.id]))
                    res = self.env.cr.dictfetchall()
                    self.env.cr.execute(query2, tuple([day, record.id]))
                    ress = self.env.cr.dictfetchall()
                    for r in res[0]:
                        if res[0][r] == None:
                            res[0][r] = 0
                    for r in ress[0]:
                        if ress[0][r] == None:
                            ress[0][r] = 0
                    client_id = record.id
                    if ress == []:
                        boom['sweikaipiao'][client_id] = 0
                        boom['syuerbukaipiao'][client_id] = 0
                        boom['szhangmian'][client_id] = 0
                        boom['sheji3'][client_id] = 0
                    for a in ress:
                        a['sweikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao'] or 0
                        a['syuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao'] or 0
                        a['szhangmian'] = a['kaipiao'] - a['shoukuankaipiao'] or 0
                        a['sheji3'] = a['sweikaipiao'] + a['syuerbukaipiao'] + a['szhangmian'] or 0
                        boom['sweikaipiao'][client_id] = a['sweikaipiao']
                        boom['syuerbukaipiao'][client_id] = a['syuerbukaipiao']
                        boom['szhangmian'][client_id] = a['szhangmian']
                        boom['sheji3'][client_id] = a['sheji3']
                    if res == []:
                        boom['amount'][client_id] = 0
                        boom['weikaipiao'][client_id] = 0
                        boom['yuerbukaipiao'][client_id] = 0
                        boom['zhangmian'][client_id] = 0
                        boom['heji1'][client_id] = 0
                        boom['heji2'][client_id] = 0
                        boom['heji3'][client_id] = 0
                        boom['heji4'][client_id] = 0
                        boom['qty'][client_id] = 0
                        boom['yinhang'][client_id] = 0
                        boom['xianjin'][client_id] = 0
                        boom['tiaozheng'][client_id] = 0
                        boom['shoukuankaipiao'][client_id] = 0
                        boom['shoukuanbukaipiao'][client_id] = 0
                        boom['kaipiao'][client_id] = 0
                        boom['bukaipiao'][client_id] = 0
                    for a in res:
                        a['weikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao'] or 0
                        a['yuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao'] or 0
                        a['zhangmian'] = a['kaipiao'] - a['shoukuankaipiao'] or 0
                        a['heji1'] = a['yinhang'] + a['xianjin'] + a['tiaozheng'] or 0
                        a['heji2'] = a['shoukuankaipiao'] + a['shoukuanbukaipiao'] or 0
                        a['heji3'] = a['weikaipiao'] + a['yuerbukaipiao'] + a['zhangmian'] or 0
                        a['heji4'] = a['kaipiao'] + a['bukaipiao'] or 0
                        boom['amount'][client_id] = a['amount']
                        boom['weikaipiao'][client_id] = a['weikaipiao']
                        boom['yuerbukaipiao'][client_id] = a['yuerbukaipiao']
                        boom['zhangmian'][client_id] = a['zhangmian']
                        boom['heji1'][client_id] = a['heji1']
                        boom['heji2'][client_id] = a['heji2']
                        boom['heji3'][client_id] = a['heji3']
                        boom['heji4'][client_id] = a['heji4']
                        boom['qty'][client_id] = a['qty'] or 0
                        boom['yinhang'][client_id] = a['yinhang'] or 0
                        boom['xianjin'][client_id] = a['xianjin'] or 0
                        boom['tiaozheng'][client_id] = a['tiaozheng'] or 0
                        boom['shoukuankaipiao'][client_id] = a['shoukuankaipiao'] or 0
                        boom['shoukuanbukaipiao'][client_id] = a['shoukuanbukaipiao'] or 0
                        boom['kaipiao'][client_id] = a['kaipiao'] or 0
                        boom['bukaipiao'][client_id] = a['bukaipiao'] or 0
                    query = """
                                                SELECT
                                                    sum(g.qty) as qty,
                                                    sum(g.price) as price,
                                                    sum(g.qty*g.price) as amount,
                                                    sum(g.kaipiao) as kaipiao,
                                                    sum(g.bukaipiao) as bukaipiao,
                                                    sum(g.yinhang) as yinhang,
                                                    sum(g.tiaozheng) as tiaozheng,
                                                    sum(g.xianjin) as xianjin,
                                                    sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                    sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                                FROM goose_order_yewu as g
                                                WHERE g.month >= %s AND g.month <= %s AND g.yewu = %s AND g.bujiliang = FALSE AND g.company = 'tian'
                                                """
                    query2 = """
                                               SELECT
                                                   sum(g.qty*g.price) as amount,
                                                   sum(g.kaipiao) as kaipiao,
                                                   sum(g.bukaipiao) as bukaipiao,
                                                   sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                   sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                               FROM goose_order_yewu as g
                                               WHERE g.month < %s AND g.yewu = %s AND g.bujiliang = FALSE AND g.company = 'tian'
                                               """
                    self.env.cr.execute(query,
                                        tuple([day, day2, record.id]))
                    res = self.env.cr.dictfetchall()
                    self.env.cr.execute(query2, tuple([day, record.id]))
                    ress = self.env.cr.dictfetchall()
                    for r in res[0]:
                        if res[0][r] == None:
                            res[0][r] = 0
                    for r in ress[0]:
                        if ress[0][r] == None:
                            ress[0][r] = 0
                    if ress == []:
                        boom2['sweikaipiao'][client_id] = 0
                        boom2['syuerbukaipiao'][client_id] = 0
                        boom2['szhangmian'][client_id] = 0
                        boom2['sheji3'][client_id] = 0
                    for a in ress:
                        a['sweikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao'] or 0
                        a['syuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao'] or 0
                        a['szhangmian'] = a['kaipiao'] - a['shoukuankaipiao'] or 0
                        a['sheji3'] = a['sweikaipiao'] + a['syuerbukaipiao'] + a['szhangmian'] or 0
                        boom2['sweikaipiao'][client_id] = a['sweikaipiao']
                        boom2['syuerbukaipiao'][client_id] = a['syuerbukaipiao']
                        boom2['szhangmian'][client_id] = a['szhangmian']
                        boom2['sheji3'][client_id] = a['sheji3']
                    if res == []:
                        boom2['amount'][client_id] = 0
                        boom2['weikaipiao'][client_id] = 0
                        boom2['yuerbukaipiao'][client_id] = 0
                        boom2['zhangmian'][client_id] = 0
                        boom2['heji1'][client_id] = 0
                        boom2['heji2'][client_id] = 0
                        boom2['heji3'][client_id] = 0
                        boom2['heji4'][client_id] = 0
                        boom2['qty'][client_id] = 0
                        boom2['yinhang'][client_id] = 0
                        boom2['xianjin'][client_id] = 0
                        boom2['tiaozheng'][client_id] = 0
                        boom2['shoukuankaipiao'][client_id] = 0
                        boom2['shoukuanbukaipiao'][client_id] = 0
                        boom2['kaipiao'][client_id] = 0
                        boom2['bukaipiao'][client_id] = 0
                    for a in res:
                        a['weikaipiao'] = a['amount'] - a['kaipiao'] - a['bukaipiao'] or 0
                        a['yuerbukaipiao'] = a['bukaipiao'] - a['shoukuanbukaipiao'] or 0
                        a['zhangmian'] = a['kaipiao'] - a['shoukuankaipiao'] or 0
                        a['heji1'] = a['yinhang'] + a['xianjin'] + a['tiaozheng'] or 0
                        a['heji2'] = a['shoukuankaipiao'] + a['shoukuanbukaipiao'] or 0
                        a['heji3'] = a['weikaipiao'] + a['yuerbukaipiao'] + a['zhangmian'] or 0
                        a['heji4'] = a['kaipiao'] + a['bukaipiao'] or 0
                        boom2['amount'][client_id] = a['amount']
                        boom2['weikaipiao'][client_id] = a['weikaipiao']
                        boom2['yuerbukaipiao'][client_id] = a['yuerbukaipiao']
                        boom2['zhangmian'][client_id] = a['zhangmian']
                        boom2['heji1'][client_id] = a['heji1']
                        boom2['heji2'][client_id] = a['heji2']
                        boom2['heji3'][client_id] = a['heji3']
                        boom2['heji4'][client_id] = a['heji4']
                        boom2['qty'][client_id] = a['qty'] or 0
                        boom2['yinhang'][client_id] = a['yinhang'] or 0
                        boom2['xianjin'][client_id] = a['xianjin'] or 0
                        boom2['tiaozheng'][client_id] = a['tiaozheng'] or 0
                        boom2['shoukuankaipiao'][client_id] = a['shoukuankaipiao'] or 0
                        boom2['shoukuanbukaipiao'][client_id] = a['shoukuanbukaipiao'] or 0
                        boom2['kaipiao'][client_id] = a['kaipiao'] or 0
                        boom2['bukaipiao'][client_id] = a['bukaipiao'] or 0
                    boom['name'][record.id] = record.name
                    boom2['name'][record.id] = record.name
                for client_id in clients:
                    li['kaipiao'] += boom['kaipiao'][client_id]
                    li['shoukuanbukaipiao'] += boom['shoukuanbukaipiao'][client_id]
                    li['qty'] += boom['qty'][client_id]
                    li['tiaozheng'] += boom['tiaozheng'][client_id]
                    li['yinhang'] += boom['yinhang'][client_id]
                    li['xianjin'] += boom['xianjin'][client_id]
                    li['bukaipiao'] += boom['bukaipiao'][client_id]
                    li['shoukuankaipiao'] += boom['shoukuankaipiao'][client_id]
                    li['zhangmian'] += boom['zhangmian'][client_id]
                    li['amount'] += boom['amount'][client_id]
                    li['heji1'] += boom['heji1'][client_id]
                    li['heji2'] += boom['heji2'][client_id]
                    li['yuerbukaipiao'] += boom['yuerbukaipiao'][client_id]
                    li['weikaipiao'] += boom['weikaipiao'][client_id]
                    li['heji3'] += boom['heji3'][client_id]
                    li['heji4'] += boom['heji4'][client_id]
                    li['szhangmian'] += boom['szhangmian'][client_id]
                    li['syuerbukaipiao'] += boom['syuerbukaipiao'][client_id]
                    li['sweikaipiao'] += boom['sweikaipiao'][client_id]
                    li['sheji3'] += boom['sheji3'][client_id]
                for client_id in clients:
                    li2['kaipiao'] += boom2['kaipiao'][client_id]
                    li2['shoukuanbukaipiao'] += boom2['shoukuanbukaipiao'][client_id]
                    li2['qty'] += boom2['qty'][client_id]
                    li2['tiaozheng'] += boom2['tiaozheng'][client_id]
                    li2['yinhang'] += boom2['yinhang'][client_id]
                    li2['xianjin'] += boom2['xianjin'][client_id]
                    li2['bukaipiao'] += boom2['bukaipiao'][client_id]
                    li2['shoukuankaipiao'] += boom2['shoukuankaipiao'][client_id]
                    li2['zhangmian'] += boom2['zhangmian'][client_id]
                    li2['amount'] += boom2['amount'][client_id]
                    li2['heji1'] += boom2['heji1'][client_id]
                    li2['heji2'] += boom2['heji2'][client_id]
                    li2['yuerbukaipiao'] += boom2['yuerbukaipiao'][client_id]
                    li2['weikaipiao'] += boom2['weikaipiao'][client_id]
                    li2['heji3'] += boom2['heji3'][client_id]
                    li2['heji4'] += boom2['heji4'][client_id]
                    li2['szhangmian'] += boom2['szhangmian'][client_id]
                    li2['syuerbukaipiao'] += boom2['syuerbukaipiao'][client_id]
                    li2['sweikaipiao'] += boom2['sweikaipiao'][client_id]
                    li2['sheji3'] += boom2['sheji3'][client_id]
        else:
            if data['form']['sorted_by'] == 'month':
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        date.append(x)
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_pay as g
                                            WHERE g.month = %s AND g.company = 'ye'
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_pay as g
                                            WHERE g.month < %s AND g.company = 'ye'
                                            """
                        self.env.cr.execute(query2, tuple([year + int(x)]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([year + int(x)]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']
                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom[a][x] = res[0][a]
                for x in month3:
                    if x >= data['form']['date_from'] and x <= data['form']['date_to']:
                        query = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_pay as g
                                            WHERE g.month = %s AND g.company = 'tian'
                                            """
                        query2 = """
                                            SELECT
                                                sum(g.qty) as qty,
                                                sum(g.price) as price,
                                                sum(g.amount) as amount,
                                                sum(g.kaipiao) as kaipiao,
                                                sum(g.bukaipiao) as bukaipiao,
                                                sum(g.yinhang) as yinhang,
                                                sum(g.tiaozheng) as tiaozheng,
                                                sum(g.xianjin) as xianjin,
                                                sum(g.shoukuankaipiao) as shoukuankaipiao,
                                                sum(g.shoukuanbukaipiao) as shoukuanbukaipiao
                                            FROM goose_order_pay as g
                                            WHERE g.month < %s AND g.company = 'tian'
                                            """
                        self.env.cr.execute(query2, tuple([year + int(x)]))
                        ress = self.env.cr.dictfetchall()
                        self.env.cr.execute(query, tuple([year + int(x)]))
                        res = self.env.cr.dictfetchall()
                        for a in res[0]:
                            if res[0][a] == None:
                                res[0][a] = 0
                        for a in ress[0]:
                            if ress[0][a] == None:
                                ress[0][a] = 0
                        res[0]['amount'] = res[0]['qty'] * res[0]['price']

                        ress[0]['weikaipiao'] = ress[0]['amount'] - ress[0]['kaipiao'] - ress[0]['bukaipiao']
                        ress[0]['yuerbukaipiao'] = ress[0]['bukaipiao'] - ress[0]['shoukuanbukaipiao']
                        ress[0]['zhangmian'] = ress[0]['kaipiao'] - ress[0]['shoukuankaipiao']
                        res[0]['heji1'] = res[0]['yinhang'] + res[0]['xianjin'] + res[0]['tiaozheng']
                        res[0]['heji2'] = res[0]['shoukuankaipiao'] + res[0]['shoukuanbukaipiao']

                        res[0]['heji4'] = res[0]['kaipiao'] + res[0]['bukaipiao']
                        res[0]['szhangmian'] = ress[0]['zhangmian']
                        res[0]['syuerbukaipiao'] = ress[0]['yuerbukaipiao']
                        res[0]['sweikaipiao'] = ress[0]['weikaipiao']
                        res[0]['sheji3'] = res[0]['sweikaipiao'] + res[0]['syuerbukaipiao'] + res[0]['szhangmian']

                        res[0]['weikaipiao'] = res[0]['amount'] - res[0]['kaipiao'] - res[0]['bukaipiao'] + res[0][
                            'sweikaipiao']
                        res[0]['yuerbukaipiao'] = res[0]['bukaipiao'] - res[0]['shoukuanbukaipiao'] + res[0][
                            'syuerbukaipiao']
                        res[0]['zhangmian'] = res[0]['kaipiao'] - res[0]['shoukuankaipiao'] + res[0]['szhangmian']
                        res[0]['heji3'] = res[0]['weikaipiao'] + res[0]['yuerbukaipiao'] + res[0]['zhangmian']
                        for a in boom:
                            boom2[a][x] = res[0][a]
                for client_id in date:
                    li['kaipiao'] += boom['kaipiao'][client_id]
                    li['shoukuanbukaipiao'] += boom['shoukuanbukaipiao'][client_id]
                    li['qty'] += boom['qty'][client_id]
                    li['tiaozheng'] += boom['tiaozheng'][client_id]
                    li['yinhang'] += boom['yinhang'][client_id]
                    li['xianjin'] += boom['xianjin'][client_id]
                    li['bukaipiao'] += boom['bukaipiao'][client_id]
                    li['shoukuankaipiao'] += boom['shoukuankaipiao'][client_id]
                    li['zhangmian'] = boom['zhangmian'][client_id]
                    li['amount'] += boom['amount'][client_id]
                    li['heji1'] += boom['heji1'][client_id]
                    li['heji2'] += boom['heji2'][client_id]
                    li['yuerbukaipiao'] = boom['yuerbukaipiao'][client_id]
                    li['weikaipiao'] = boom['weikaipiao'][client_id]
                    li['heji3'] = boom['heji3'][client_id]
                    li['heji4'] += boom['heji4'][client_id]
                    li['szhangmian'] += boom['szhangmian'][client_id]
                    li['syuerbukaipiao'] += boom['syuerbukaipiao'][client_id]
                    li['sweikaipiao'] += boom['sweikaipiao'][client_id]
                    li['sheji3'] += boom['sheji3'][client_id]
                for client_id in date:
                    li2['kaipiao'] += boom2['kaipiao'][client_id]
                    li2['shoukuanbukaipiao'] += boom2['shoukuanbukaipiao'][client_id]
                    li2['qty'] += boom2['qty'][client_id]
                    li2['tiaozheng'] += boom2['tiaozheng'][client_id]
                    li2['yinhang'] += boom2['yinhang'][client_id]
                    li2['xianjin'] += boom2['xianjin'][client_id]
                    li2['bukaipiao'] += boom2['bukaipiao'][client_id]
                    li2['shoukuankaipiao'] += boom2['shoukuankaipiao'][client_id]
                    li2['zhangmian'] = boom2['zhangmian'][client_id]
                    li2['amount'] += boom2['amount'][client_id]
                    li2['heji1'] += boom2['heji1'][client_id]
                    li2['heji2'] += boom2['heji2'][client_id]
                    li2['yuerbukaipiao'] = boom2['yuerbukaipiao'][client_id]
                    li2['weikaipiao'] = boom2['weikaipiao'][client_id]
                    li2['heji3'] = boom2['heji3'][client_id]
                    li2['heji4'] += boom2['heji4'][client_id]
                    li2['szhangmian'] += boom2['szhangmian'][client_id]
                    li2['syuerbukaipiao'] += boom2['syuerbukaipiao'][client_id]
                    li2['sweikaipiao'] += boom2['sweikaipiao'][client_id]
                    li2['sheji3'] += boom2['sheji3'][client_id]

        docargs = {
            'date': date,
            'res': boom,
            'res2': boom2,
            'client': client,
            'clients': clients,
            'name': clients_name,
            'data': data,
            'company': ['ye', 'tian'],
            's': li,
            's2': li2,
            'month': month,
        }
        return self.env['report'].render('goose.report_gooseorder', docargs)


class GooseOrderWjReport(models.AbstractModel):
    _name = 'report.goose.my_report_wj'

    def render_html(self, docids, data=None):
        month_begin = int(data['form']['year'][0:4]) * 100 + int(data['form']['date_from'])
        month_end = int(data['form']['year'][0:4]) * 100 + int(data['form']['date_to'])
        data['month_begin'] = month_begin
        data['month_end'] = month_end
        res = {}
        res_start = {}
        res_chu = {}
        res_ru = {}
        res_heji = {}
        res_ly = {}
        res_ly_heji = {}
        res_department = {}
        if data['form']['result_selection'] == 'kucun':
            query = """
                        SELECT
                            c.name,
                            sum(g.min_stock*g.stock) as amount
                        FROM goose_product_wuliao as g
                        LEFT JOIN goose_category_wuliao as c
                        ON g.category=c.id
			            GROUP BY c.name
                    """
            self.env.cr.execute(query)
            # 期末的金额
            res = self.env.cr.dictfetchall()

            query2 = """

                        SELECT
                        g.qty,w.churu,w.month,c.min_stock,cw.name
                        FROM goose_wuliao_line as g
                        LEFT JOIN goose_wjstock as w
                        ON g.wl_id = w.id
                        LEFT JOIN goose_product_wuliao as c
                        ON g.name = c.id
                        LEFT JOIN goose_category_wuliao as cw
                        ON cw.id = c.category
                        WHERE g.wl_id in (SELECT id FROM goose_wjstock) AND w.month >%s AND w.month <=%s
                    """
            self.env.cr.execute(query2, tuple([month_begin, month_end]))
            # 期末的金额
            res2 = self.env.cr.dictfetchall()
            res_name = {}
            for r in res2:
                res_name[r['name']] = 0
            res_start = res_name.copy()
            res_chu = res_name.copy()
            res_ru = res_name.copy()
            for r in res2:
                for x in res_name:
                    if r['name'] == x and r['churu'] == 'ru':
                        res_ru[x] += r['qty'] * r['min_stock']
                    elif r['name'] == x and r['churu'] == 'chu':
                        res_chu[x] += r['qty'] * r['min_stock']
            for r in res:
                for x in res_name:
                    if r['name'] == x:
                        res_start[x] = r['amount'] - res_ru[x] + res_chu[x]
            res_heji = {'start': 0, 'ru': 0, 'chu': 0, 'res': 0}

            for r in res_name:
                res_heji['start'] += res_start[r]
                res_heji['ru'] += res_ru[r]
                res_heji['chu'] += res_chu[r]
            for x in res:
                res_heji['res'] += x['amount']
        elif data['form']['result_selection'] == 'lingyong':
            res_ly = {'ycls': {}, 'yclj': {}, 'rls': {}, 'rlj': {}, 'lpj': {}, 'fl': {}, 'lb': {}, 'bg': {}}
            res_ly_heji = {'ycls': 0, 'yclj': 0, 'rls': 0, 'rlj': 0, 'lpj': 0, 'fl': 0, 'lb': 0, 'bg': 0}
            query = """
                        SELECT
                        g.qty,
                        c.min_stock,
                        cw.name,
                        e.name as department
                        FROM goose_wuliao_line as g
                        LEFT JOIN goose_wjstock as w
                        ON g.wl_id = w.id
                        LEFT JOIN goose_product_wuliao as c
                        ON g.name = c.id
                        LEFT JOIN goose_category_wuliao as cw
                        ON cw.id = c.category
                        LEFT JOIN hr_department as e
                        ON w.department = e.id
                        WHERE g.wl_id in (SELECT id FROM goose_wjstock) AND w.churu = 'chu' AND w.month >%s AND w.month <=%s
                    """
            self.env.cr.execute(query, tuple([month_begin, month_end]))
            res = self.env.cr.dictfetchall()
            print res
            res_department = {}
            for r in res:
                res_department[r['department']] = {}
            for x in res_department:
                for y in res_ly:
                    res_ly[y][x] = 0
            for x in res_department:
                for r in res:
                    if r['department'] == x:
                        if r['name'] == u'原材料':
                            res_ly['ycls'][x] += r['qty']
                            res_ly['yclj'][x] += r['min_stock']
                        if r['name'] == u'燃料':
                            res_ly['rls'][x] += r['qty']
                            res_ly['rlj'][x] += r['min_stock']
                        if r['name'] == u'另配件':
                            res_ly['lpj'][x] += r['qty'] * r['min_stock']
                        if r['name'] == u'辅料':
                            res_ly['fl'][x] += r['qty'] * r['min_stock']
                        if r['name'] == u'劳保用品':
                            res_ly['lb'][x] += r['qty'] * r['min_stock']
                        if r['name'] == u'办公用品':
                            res_ly['bg'][x] += r['qty'] * r['min_stock']
            for x in res_department:
                res_ly_heji['ycls'] += res_ly['ycls'][x]
                res_ly_heji['yclj'] += res_ly['yclj'][x]
                res_ly_heji['rls'] += res_ly['rls'][x]
                res_ly_heji['rlj'] += res_ly['rlj'][x]
                res_ly_heji['lpj'] += res_ly['lpj'][x]
                res_ly_heji['fl'] += res_ly['fl'][x]
                res_ly_heji['lb'] += res_ly['lb'][x]
                res_ly_heji['bg'] += res_ly['bg'][x]
                print res_ly_heji
            print res_ly_heji
        docargs = {
            'data': data,
            'res': res,
            'res_ru': res_ru,
            'res_chu': res_chu,
            'res_start': res_start,
            'res_heji': res_heji,
            'res_ly': res_ly,
            'res_department': res_department,
            'res_ly_heji': res_ly_heji,
        }
        return self.env['report'].render('goose.report_gooseproductwuliao', docargs)


class GooseOrderReportYl(models.AbstractModel):
    _name = 'report.goose.my_report_yl'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('goose.my_report_yl')
        mod = self.env['goose.stock'].browse(docids)
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': mod,
        }
        print docargs
        return report_obj.render('goose.report_gooseyuanliao', docargs)


class GooseOrderReportCaigou(models.AbstractModel):
    _name = 'report.goose.my_report_caigou'

    @api.model
    def render_html(self, docids, data=None):
        query = """
                SELECT
                    c.name as name,
                    sum(g.qty) as qty,
                    sum(g.qty*g.price) as amount,
                    sum(g.shikai13) as shikai13,
                    sum(g.shikai17) as shikai17,
                    sum(g.xianjin) as xianjin,
                    sum(g.ka) as ka,
                    sum(g.yinhang) as yinhang
                FROM goose_order_pay as g
                LEFT JOIN goose_supplier as c
                ON g.client_id=c.id
                        GROUP BY c.name
               """
        self.env.cr.execute(query)
        # 期末的金额
        res = self.env.cr.dictfetchall()
        for record in res:
            code = self.env['goose.supplier'].search([('name', '=', record['name'])]).code
            record['code'] = code
        docargs = {
            'res': res,
            'data': data,
        }
        return self.env['report'].render('goose.report_goosecaigou', docargs)


class GooseOrderReportCaigoujl(models.AbstractModel):
    _name = 'report.goose.my_report_caigou_jl'

    @api.model
    def render_html(self, docids, data=None):
        query = """
                SELECT
                    c.name as name,
                    sum(g.qty) as qty,
                    sum(g.qty*g.price) as amount,
                    sum(g.shikai13) as shikai13,
                    sum(g.shikai17) as shikai17,
                    sum(g.xianjin) as xianjin,
                    sum(g.ka) as ka,
                    sum(g.yinhang) as yinhang
                FROM goose_order_pay_jl as g
                LEFT JOIN goose_supplier as c
                ON g.client_id=c.id
                        GROUP BY c.name
               """
        self.env.cr.execute(query)
        # 期末的金额
        res = self.env.cr.dictfetchall()
        for record in res:
            code = self.env['goose.supplier'].search([('name', '=', record['name'])]).code
            record['code'] = code
        docargs = {
            'res': res,
            'data': data,
        }
        return self.env['report'].render('goose.report_goosecaigou', docargs)


class GooseJxReport(models.AbstractModel):
    _name = 'report.goose.my_report_jx'

    @api.model
    def render_html(self, docids, data=None):
        data['form']['in'] = 10
        data['form']['out'] = 20
        query = """
                SELECT
                    c.name as client,
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
            date_begin =None
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
                    data2['yewu'] = r['yewu']
                    data2['in_data'] = None
                    date_end = datetime.datetime(int(r['date'][0:4]), int(r['date'][5:7]), int(r['date'][8:10]))
                    if (date_end - date_begin).days < 90:
                        data2['in'] += r['shoukuan']
                    else:
                        data2['out'] += r['shoukuan']
                    if data2['in'] + data2['out'] == data2['jine']:
                        data2['in_data'] = (date_end - date_begin).days
            mes.append(data2)
        print mes
        docargs = {
            'mes': mes,
            'data': data,
        }
        return self.env['report'].render('goose.report_goosejx', docargs)
