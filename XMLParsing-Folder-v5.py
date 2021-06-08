import os
import time
import xml.etree.ElementTree as ET

directory=r'C:\Users\KZ623JK\OneDrive - EY\Documents\Carrier'
obj = os.scandir(directory)

userinput = input(' enter the new filename')
effective_date = input(' enter the effectivedate')
input_manuscriptid = input(' enter the manuscript id')
input_versionid = input(' enter the version id')
input_lob = input(' enter the lob')
input_caption = input(' enter the caption')


updatedname=[]
newname=''
samplename=[]
oldname=[]
oldpath=[]

for entry in obj:
    for x in os.scandir(entry.path):
        oldname.append(x.path)
        oldpath.append(entry.path)
        name=x.name.split('_')
        updatedname=name[2:]
        newname=userinput+'_'
        arraylength = len(updatedname)
        for z in range(0,arraylength):
            if z==arraylength-1:
                newname=newname+updatedname[z]
            else:
                newname=newname+updatedname[z]+'_'
        samplename.append(newname)
        newname=''
        
if len(oldname) and len(oldpath) and len(samplename):
    print('code is executing')
else:
    print('code is going to fail')

#print(samplename)
#print(len(oldname))
#print(len(oldpath))
#print(len(samplename))

 
for x in range(0,len(samplename)):
    os.rename(oldname[x],oldpath[x]+'\\'+samplename[x])

print('done')



print('processing...') #setup some delay
time.sleep(5)

for entry in os.scandir(directory):
    for file in os.scandir(entry):
        parser=ET.XMLParser(encoding='utf-8')
        root=ET.parse(file.path,parser=parser)
        #print('manuscriptID',root.getroot()[0].attrib['manuscriptID'])
        #print('versionDate',root.getroot()[0].attrib['versionDate'])
        root.getroot()[0].attrib['versionDate']=effective_date
        root.getroot()[0].attrib['manuscriptID']=input_manuscriptid
        root.getroot()[0].attrib['versionID'] = input_versionid
        root.getroot()[0].attrib['lob'] = input_lob
        root.getroot()[0].attrib['caption'] = input_caption
            
        
        myroot=root.getroot()[0]
        for x in myroot:
            if x.tag=='keys':
                for y in x:
                    if y.attrib['name']=='lob':
                        y.attrib['value']=input_lob
                    if y.attrib['name']=='effectiveDateNew':
                        y.attrib['value']=effective_date
                        #print(y.attrib['value'])
                    if y.attrib['name']=='effectiveDateRenewal':
                        y.attrib['value']=effective_date
                        
                        
        root.write(file.path)
        print('wait...')


        
obj.close()
print('done')
