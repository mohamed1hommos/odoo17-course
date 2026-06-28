from wsgiref import headers
from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval


class PropertyReport(http.Controller):


    @http.route('/property/excel/report/<string:property_ids>',type='http',auth="user")
    def property_excel_report(self,property_ids):
        property_ids = request.env['property'].browse(literal_eval(property_ids))
        output =io.BytesIO()
        workbook = xlsxwriter.Workbook(output,{'constant_memory': True})
        worksheet = workbook.add_worksheet('Property Report')

        header_format = workbook.add_format({'bold':True,'bg_color':'#F54927','border':1,'align':'center'})
        values_format = workbook.add_format({'border':1,'align':'center'})
        price_format = workbook.add_format({'border':1,'align':'center','num_format':'$##,##00.00'}) #for currencies



        headers=['Name','Postcode','selling_price','Garden']
        for col_num ,header in enumerate(headers):
            worksheet.write(0,col_num,header,header_format)
        row_number = 1
        for property in property_ids:
                worksheet.write(row_number,0,property.name,values_format)
                worksheet.write(row_number, 1, property.postcode,values_format)
                worksheet.write(row_number, 2, property.selling_price,price_format)
                worksheet.write(row_number, 3, 'Yes'if property.garafe else 'NO', values_format)
                row_number += 1

        workbook.close()
        output.seek(0) #read file from memory from begin

        file_name = 'Property Report.xlsx'

        response = request.make_response(
            output.getvalue(),
            [
                ('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition',f'attachment;filename={file_name}'),
            ]

        )
        return response
