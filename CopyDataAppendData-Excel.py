from xlutils.copy import copy
from xlrd import open_workbook

rb=open_workbook('/output.xlsx')
wb=copy(rb)

w_sheet=wb.get_sheet(0)

a=input('enter the start date')
b=input('enter the end date')

a1=int(a.split('/')[1])
b1=int(b.split('/')[1])

c=b1-a1

for x in range(c+1):
    w_sheet.write(0,x,str(a1+x)+'-march-'+'2021')

wb.save('yash.xls')
