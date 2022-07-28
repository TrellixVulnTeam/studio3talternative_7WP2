import xlsxwriter
from pprint import pprint
import json
from datetime import datetime
class FileManagement:
    def __init__(self,data):
        self.excel_file_name="report1.xlsx"
        self.data=data
        self.expenses=list()
    def format_data(self):
        try:
            for obj in self.data:
                PhoneNumber=obj["PhoneNumber"]
                name=obj["name"]
                type=obj["type"]
                Status=obj["Status"]
                RegisterDate=obj["RegisterDate"]
                occupiedProperties=obj["occupiedProperties"]
                vacantProperties=obj["vacantProperties"]
                totalProperties=obj["totalProperties"]
                totalTeamMembers=obj["totalTeamMembers"]
                totalBankAccounts=obj["totalBankAccounts"]
                totalMaintainanceRequest=obj["totalMaintainanceRequest"]
                totalInvoicePaidOnlineThisMonth=obj["totalInvoicePaidOnlineThisMonth"]
                self.expenses.append([PhoneNumber,name,type,Status,RegisterDate,occupiedProperties,vacantProperties,totalProperties,totalTeamMembers,totalBankAccounts,totalMaintainanceRequest,totalInvoicePaidOnlineThisMonth])
            self.save_to_xlsx()
        except Exception as e:    
            print(e)
    def save_to_xlsx(self):
        try:
            workbook = xlsxwriter.Workbook(self.excel_file_name)
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 1})
            worksheet.write('A1', 'PhoneNumber', bold)
            worksheet.write('B1', 'name', bold)
            worksheet.write('C1', 'type', bold)
            worksheet.write('D1', 'Status', bold)
            worksheet.write('E1', 'RegisterDate', bold)
            worksheet.write('F1', 'occupiedProperties', bold)
            worksheet.write('G1', 'vacantProperties', bold)
            worksheet.write('H1', 'totalProperties', bold)
            worksheet.write('I1', 'totalTeamMembers', bold)
            worksheet.write('J1', 'totalBankAccounts', bold)
            worksheet.write('K1', 'totalMaintainanceRequest', bold)
            worksheet.write('L1', 'totalInvoicePaidOnlineThisMonth', bold)
            row = 1
            col = 0
            for obj in self.expenses:
                for i in range(12):
                    worksheet.write_string(row, col + i, str(obj[i]))
                row += 1
            workbook.close()
        except Exception as e:
            print("Test"+e)    
               
        




