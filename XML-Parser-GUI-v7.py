from tkinter import *  
import tkinter as tk
import os
import time
import xml.etree.ElementTree as ET
import re

roottk=Tk()
roottk.geometry("750x500")

Directory=Label(roottk,text="File Directory").place(x=30,y=20)
Catalogdir=Label(roottk,text="ManuscriptCatalog Dir").place(x=30,y=60)
FileName=Label(roottk,text="Product Name").place(x=30,y=100)
EffectiveDate=Label(roottk,text="Effective Date").place(x=30,y=140)

input_directory = Entry(roottk,width=70)
input_directory.place(x=180,y=20)
input_catalogdir = Entry(roottk,width=70)
input_catalogdir.place(x=180,y=60)
newfile_input = Entry(roottk,width=40)
newfile_input.place(x=180,y=100)
input_effective_date = Entry(roottk,width=40)
input_effective_date.place(x=180,y=140)


def operation():
    
    states=['Import','RemoveLOB','Data','Product','Rating','RatingControl','Validation','Forms','Pages']
    
    Label(roottk,text="processed",font=('helvetica', 12, 'bold')).place(x=230,y=360)

    directory=input_directory.get()
    catalogdir=input_catalogdir.get()
    userinput = newfile_input.get()
    effective_date = input_effective_date.get()
    productname = userinput
    
    obj = os.scandir(directory)

    updatedname=[]
    newname=''
    samplename=[]
    oldname=[]
    oldpath=[]
    
    parser=ET.XMLParser(encoding='utf-8')
    catalogroot=ET.parse(catalogdir,parser=parser)
    
    
    def rename(name):
        #print(name)
        global number
        for z in userinput:
            if z == '_':
                print('underscored called')
                number=2
                return name[2:]
                break
        if name[0]=='DuckCreekTech':
            print('dct called')
            #global number
            number=2
            return name[2:]
       
        if name[0]!='DuckCreekTech' and len(name[1])==2:
            print('uniquename')
            number=1
            return name[1:]

        elif name[0]!='DuckCreekTech':
            flag=0
            for x in states:
                if name[1]==x:
                    flag=flag+1
                    print(x)
                    #global number
                    number=1
                    return name[1:]
            if flag==0:
                print('warning:check to files processed properly')
                Label(roottk,text="warning:check the files whether processed properly").place(x=190,y=380)
                number=2
                return name[2:]


    for entry in obj:
        for x in os.scandir(entry.path):
            oldname.append(x.path)
            oldpath.append(entry.path)
            name=x.name.split('_')
            #print('name',name)
            uname=rename(name)
            #print(uname)
            updatedname=uname
            #updatedname=name[2:]
            newname=userinput+'_'
            arraylength = len(updatedname)
            for z in range(0,arraylength):
                if z==arraylength-1:
                    newname=newname+updatedname[z]
                else:
                    newname=newname+updatedname[z]+'_'
            samplename.append(newname)
            #print('samplename',samplename)
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
        os.rename(oldname[x],oldpath[x]+'\\'+samplename[x]) #need to change

    print('done')

    print('processing...') #setup some delay
    time.sleep(5)

    def splitjoin(sampleid, productname):
        #print(type(number))
        newsampleid=sampleid.split('_')
        newmanuscript=newsampleid[number:]
        newmanuscript.insert(0,productname)
        newmanuscript= '_'.join(newmanuscript)
        return newmanuscript

    def splitjoinlob(productname,manuscriptid):
        for x in manuscriptid.split('_'):
            if x == 'Forms':
                productname=productname+x
                #print('productname',productname)
            elif x == 'FormsControl':
                productname=productname+'Forms'
        productname=productname.split('_')
        productname=''.join(productname)
        return productname

    def splitjoincaption(caption,productname):
        captionarr=[]
        newcaption=caption.split(' ')
        for x in newcaption:
            if x != '':
                captionarr.append(x)
        #print(captionarr)
        updatedcaption=captionarr[number:]
        productname=productname.split('_')
        for y in range(0,len(productname)):    
            updatedcaption.insert(y,productname[y])
        updatedcaption=' '.join(updatedcaption)
        return updatedcaption

    def renameurl(path):
        if 'ManuScripts' in path:
            z=path.split('ManuScripts')[1]
            z1=z.replace('\\\\','\\')
            if z1[0] == '\\':
                z2=z1[1:]
            else:
                z2=z1
            #print(z2)
            return z2
        else:
            return path
        '''
        x=path.split('\')
        for y in x:
            if y =='ManuScripts':
                z = path.split('ManuScripts',1)[1]
                break
            else:
                z=path
        print(z)
        return z
         z=re.escape(path)
        print('z',z.split("\\"))
        print('path',path)
        return path
        '''
        
    def modify(objs):
        if objs.split('_')[0] == 'DuckCreekTech':
            new_inherited=objs.split('_')[2:]
            if '_' in productname:
                newproductname=productname.split('_')[1]
                new_inherited.insert(0,newproductname)
                new_inherited='_'.join(new_inherited)
            else:
                new_inherited.insert(0,productname)
                new_inherited='_'.join(new_inherited)
                
        if objs.split('_')[0] == 'Carrier':
            new_inherited=objs.split('_')[2:]
            newproductname='Carrier_'+productname
            new_inherited.insert(0,newproductname)
            new_inherited='_'.join(new_inherited)
        return new_inherited

                     
    for entry in os.scandir(directory):
        for file in os.scandir(entry):
            parser=ET.XMLParser(encoding='utf-8')
            root=ET.parse(file.path,parser=parser)
            root.getroot()[0].attrib['versionDate']=effective_date
            manuscriptid = root.getroot()[0].attrib['manuscriptID']
            versionid = root.getroot()[0].attrib['versionID']
            caption = root.getroot()[0].attrib['caption']
            
            #print(manuscriptid)
            updatedmanuscriptid=splitjoin(manuscriptid, productname)
            updatedlob=splitjoinlob(productname,manuscriptid)
            updatedcaption=splitjoincaption(caption,productname)
            updatedversionid=updatedmanuscriptid
            #print(updatedmanuscriptid, updatedversionid)

            #root.getroot()[0].attrib['lob']=updatedlob
            root.getroot()[0].attrib['caption']=updatedcaption
            root.getroot()[0].attrib['manuscriptID']=updatedmanuscriptid
            root.getroot()[0].attrib['versionID']=updatedversionid
            
            all = root.getroot()[0].attrib
            for x in all:
                if x == 'inherited':
                    if root.getroot()[0].attrib['inherited'] !='':
                        updatedinherited=modify(root.getroot()[0].attrib['inherited'])
                        root.getroot()[0].attrib['inherited']=updatedinherited
                        
                        
                        
            #if root.getroot()[0].attrib['inherited']:
            #    print('inherited',root.getroot()[0].attrib['inherited'])
            #print(updatedlob,updatedcaption)

            #manuscriptcatalog
            sub=ET.SubElement(catalogroot.getroot(),'entry')
            sub.attrib['ID']=updatedversionid
            sub.attrib['description']=updatedcaption
            sub.attrib['versionDate']=root.getroot()[0].attrib['versionDate']
            sub.attrib['versionID']=updatedversionid
            sub.attrib['status']='ok'
            sub.attrib['url']=renameurl(file.path)
            sub.attrib['version']=root.getroot()[0].attrib['version']

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
                        #print(y.tag,y.attrib['name'])
                        sub.attrib[y.attrib['name']]=y.attrib['value']
            
           
            sub.attrib['cultures']=''
            sub.attrib['type']=''
            sub.attrib['role']=''
            
            sub.tail="\n    "

            root.write(file.path) #need to change
            catalogroot.write(catalogdir)
            #Label1=Label(roottk,text="processing...",font=('helvetica', 12, 'bold')).place(x=230,y=360)
            print('wait...')

    for entry in os.scandir(directory):
        for file in os.scandir(entry):
            filename=file.path
            parser=ET.XMLParser(encoding='utf-8')
            root=ET.parse(file.path,parser=parser)
            with open(filename,'r+',encoding='utf-8') as myfile:
                data=myfile.read()
                if '&#8211;' in data:
                    data = data.replace('&#8211;','-')
                    myfile.seek(0)
                    myfile.truncate()
                    myfile.write(data)
                    myfile.close()
                    

    obj.close()
    print('done')

    Label(roottk,text="Executed",font=('helvetica', 12, 'bold')).place(x=230,y=400)

submit=Button(roottk,text="submit",command=operation).place(x=240,y=320)
roottk.mainloop()
