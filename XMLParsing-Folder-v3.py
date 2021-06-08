import os
import time
import xml.etree.ElementTree as ET

directory=r'C:\Users\KZ623JK\OneDrive - EY\Documents\Carrier'
obj = os.scandir(directory)

userinput = input('enter the new filename')

for entry in obj:
    for file in os.scandir(entry.path):
        foldername=file.path.split('\\')[-2]
        filename=file.name.split('_')[1]
        newfilename=directory+'\\'+foldername+'\\'+userinput+'_'+filename
        os.rename(file.path,newfilename) 
        print('done') #setup some delay


        
obj.close()


directory=r'C:\Users\KZ623JK\OneDrive - EY\Documents\Carrier'
obj=os.scandir(directory)

effective_date = input('enter the effectivedate')
print(effective_date)

for entry in obj:
    for file in os.scandir(entry):
        parser=ET.XMLParser(encoding='utf-8')
        root=ET.parse(file.path,parser=parser)
        print('manuscriptID',root.getroot()[0].attrib['manuscriptID'])
        print('versionDate',root.getroot()[0].attrib['versionDate'])
        #print(root.getroot()[0][0][3].attrib['name'])
        
        myroot=root.getroot()[0]
        
        for x in myroot:
            if x.tag=='keys':
                for y in x:
                    if y.attrib['name']=='effectiveDateNew':
                        y.attrib['value']=effective_date
                        print(y.attrib['value'])
                    if y.attrib['name']=='effectiveDateRenewal':
                        print(y.attrib)
                        
        root.write(file.path)
        print('done')
