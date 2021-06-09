import os
import time
import xml.etree.ElementTree as ET

directory=input('enter the file directory')
obj = os.scandir(directory)

userinput = input(' enter the new filename')
effective_date = input('enter the effectivedate')
productname = userinput


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

def splitjoin(sampleid, productname):
    newmanuscript=sampleid.split('_')[2:]
    newmanuscript.insert(0,productname)
    newmanuscript= '_'.join(newmanuscript)
    return newmanuscript

def splitjoinlob(productname):
    productname=productname.split('_')
    productname=''.join(productname)
    return productname

def splitjoincaption(caption,productname):
    newcaption=caption.split(' ')[2:]
    productname=productname.split('_')
    productname=' '.join(productname)
    newcaption.insert(0,productname)
    newcaption=' '.join(newcaption)
    return newcaption
    

for entry in os.scandir(directory):
    for file in os.scandir(entry):
        parser=ET.XMLParser(encoding='utf-8')
        root=ET.parse(file.path,parser=parser)
        root.getroot()[0].attrib['versionDate']=effective_date
        manuscriptid = root.getroot()[0].attrib['manuscriptID']
        versionid = root.getroot()[0].attrib['versionID']
        caption = root.getroot()[0].attrib['caption']
        
        updatedmanuscriptid=splitjoin(manuscriptid, productname)
        updatedlob=splitjoinlob(productname)
        updatedcaption=splitjoincaption(caption,productname)
        updatedversionid=splitjoin(versionid,productname)
        #print(updatedmanuscriptid, updatedversionid)
        
        root.getroot()[0].attrib['lob']=updatedlob
        root.getroot()[0].attrib['caption']=updatedcaption
        root.getroot()[0].attrib['manuscriptID']=updatedmanuscriptid
        root.getroot()[0].attrib['versionID']=updatedversionid
        #print(updatedlob,updatedcaption)
        
        myroot=root.getroot()[0]
        for x in myroot:
            if x.tag=='keys':
                for y in x:
                    if y.attrib['name']=='lob':
                        y.attrib['value']=updatedlob
                    if y.attrib['name']=='effectiveDateNew':
                        y.attrib['value']=effective_date
                        #print(y.attrib['value'])
                    if y.attrib['name']=='effectiveDateRenewal':
                        y.attrib['value']=effective_date
                        
                        
        root.write(file.path)
        print('wait...')

        
obj.close()
print('done')
