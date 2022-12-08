import io

import xlsxwriter

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
from odoo.tools.safe_eval import json


class CreateStockReportWizard(models.TransientModel):
    _name = 'stock.move.wizard'
    _description = 'CreateStockReportWizard '

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(strreporting="End Date")
    status = fields.Selection(selection=[
        ('available', 'Available'),
        ('not_available', 'Not Available')],
        string="Status")
    location_type = fields.Selection(
        selection=[
            ('supplier', 'Vendor Location'),
            ('view', 'View'),
            ('internal', 'Internal Location'),
            ('customer', 'Customer Location'),
            ('inventory', 'Inventory Loss'),
            ('production', 'Production'),
            ('transit', 'Transit Location')],
        string="Location Type")
    product_id = fields.Many2one('product.product', string='Product')

    def action_print_pdf_report(self):
        var = """select date,reference,product_template.name ->> 'en_US' as name  ,stock_location.complete_name as 
        source_location,sl.complete_name as destination_location,state from stock_move inner join product_product on 
        product_product.id = stock_move.product_id inner join product_template on product_template.id = 
        product_product.product_tmpl_id inner join stock_location on stock_location.id = stock_move.location_id inner 
        join stock_location sl on sl.id = stock_move.location_dest_id """

        if self.product_id:
            new_var = """ and stock_move.product_id = '%s' """ % self.product_id.id
            var += new_var

        if self.start_date:
            new_var = """ and date >= '%s' """ % self.start_date
            var += new_var

        if self.end_date:
            new_var = """ and date <= '%s' """ % self.end_date
            var += new_var

        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError('Start Date And To End Is Reversible')
        list1 = []
        list2 = []
        for rec in self.env['stock.location'].search([]):
            if self.location_type == rec.usage:
                print(rec.id)
                list1.append(rec.id)
                for dec in self.env['stock.quant'].search([('location_id', 'in', list1)]):
                    print(dec.product_id)
                    print(list2)
                    list2.append(dec.product_id.id)
                if len(list2) == 1:
                    pd = tuple(list2)
                    new_var = """ and stock_move.product_id  = '%s' """ % pd
                    var += new_var
                elif len(list2) > 1:
                    pd = tuple(list2)
                    print(pd)
                    new_var = """ and stock_move.product_id in %s """ % (pd,)
                    var += new_var
                else:
                    raise ValidationError('There Is No Data Inside The Location Type')
            print(var)

        self.env.cr.execute(var)
        record = self.env.cr.dictfetchall()
        # print(record)
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'product_id': self.product_id.name,
            'status': self.status,
            'location_type': self.location_type,
            'query': record,

        }
        return self.env.ref('stock_move_report.action_stock_move_report').report_action(None, data=data)

    def action_print_xls_report(self):
        var = """select date,reference,product_template.name ->> 'en_US' as name  ,stock_location.complete_name as 
        source_location,sl.complete_name as destination_location,state from stock_move inner join product_product on 
        product_product.id = stock_move.product_id inner join product_template on product_template.id = 
        product_product.product_tmpl_id inner join stock_location on stock_location.id = stock_move.location_id inner 
        join stock_location sl on sl.id = stock_move.location_dest_id """

        if self.product_id:
            new_var = """ and stock_move.product_id = '%s' """ % self.product_id.id
            var += new_var

        if self.start_date:
            new_var = """ and date >= '%s' """ % self.start_date
            var += new_var

        if self.end_date:
            new_var = """ and date <= '%s' """ % self.end_date
            var += new_var

        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError('Start Date And To End Is Reversible')

        list1 = []
        list2 = []
        for rec in self.env['stock.location'].search([]):
            if self.location_type == rec.usage:
                list1.append(rec.id)
                print(var)
                for dec in self.env['stock.quant'].search([('location_id', 'in', list1)]):
                    print("quant_product_id", dec.product_id)
                    list2.append(dec.product_id.id)
                    print("list2", list2)
                if len(list2) == 1:
                    pd = tuple(list2)
                    new_var = """ and stock_move.product_id  = '%s' """ % pd
                    var += new_var
                elif len(list2) > 1:
                    pd = tuple(list2)
                    print(pd)
                    new_var = """ and stock_move.product_id in %s """ % (pd,)
                    var += new_var
                else:
                    raise ValidationError('There Is No Data Inside The Location Type')

        self.env.cr.execute(var)
        record = self.env.cr.dictfetchall()
        # print(record)
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'product_id': self.product_id.name,
            'status': self.status,
            'location_type': self.location_type,
            'query': record,

        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'stock.move.wizard',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Stock Move Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px', 'bold': True})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px'})
        sheet.merge_range('H2:N3', 'STOCK MOVE REPORT', head)
        sheet.write('B6', 'From:', cell_format)
        sheet.merge_range('C6:D6', data['start_date'], txt)
        sheet.write('F6', 'To:', cell_format)
        sheet.merge_range('G6:H6', data['end_date'], txt)

        sheet.write('A11:B11', 'Sl no', cell_format)
        sheet.write('B11:D11', 'Date', cell_format)
        sheet.write('E11:H11', 'Reference', cell_format)
        sheet.write('I11:L11', 'Product Name', cell_format)
        sheet.write('M11:R11', 'From', cell_format)
        sheet.write('S11:U11', 'To', cell_format)
        sheet.write('W11:Y11', 'Status', cell_format)

        row = 11
        column = 0
        a = 1
        for i in data['query']:
            sheet.write(row, column, a)
            a = a + 1
            sheet.write(row, column + 1, i['date'])
            sheet.write(row, column + 4, i['reference'])
            sheet.write(row, column + 8, i['name'])
            sheet.write(row, column + 12, i['source_location'])
            sheet.write(row, column + 18, i['destination_location'])
            sheet.write(row, column + 22, i['state'])

            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
