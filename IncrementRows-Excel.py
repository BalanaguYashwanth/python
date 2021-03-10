import xlwt
from xlwt import Workbook

wb=Workbook()

sheet1=wb.add_sheet('sheet 1')

a=input('enter the start date')
b=input('enter the end date')

a1=int(a.split('/')[1])
b1=int(b.split('/')[1])

c=b1-a1

for x in range(c+1):
    sheet1.write(0,x,str(a1+x)+'-march-'+'2021')

wb.save('xwlwt example.xlsx')

