!pip install PyPDF2

    
import PyPDF2 as pypdf

pdfobject=open(r'path','rb')
pdf=pypdf.PdfFileReader(pdfobject)
#print(pdf.getPage(0).extractText().split('\n'))


for num in range(pdf.numPages):
    for x in pdf.getPage(num).extractText().splitlines():
        if 'experience' in x:
            print(x)
        if 'integration' in x.lower() or 'billing' in x.lower() or 'policy' in x.lower() or 'insights' in x.lower() or 'duckcreek' in x.lower():
            print(x)
        
print('completed')
