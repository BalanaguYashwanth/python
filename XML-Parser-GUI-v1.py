from tkinter import *  
import tkinter as tk
import os
import time
import xml.etree.ElementTree as ET

roottk=Tk()
roottk.geometry("750x500")

Directory=Label(roottk,text="File Directory").place(x=30,y=20)
FileName=Label(roottk,text="Product Name").place(x=30,y=60)
EffectiveDate=Label(roottk,text="Effective Date").place(x=30,y=100)

input_directory = Entry(roottk,width=70)
input_directory.place(x=180,y=20)
newfile_input = Entry(roottk,width=40)
newfile_input.place(x=180,y=60)
input_effective_date = Entry(roottk,width=40)
input_effective_date.place(x=180,y=100)


def operation():
    Label(roottk,text="processing",font=('helvetica', 12, 'bold')).place(x=230,y=360)

    directory=input_directory.get()
    userinput = newfile_input.get()
    effective_date = input_effective_date.get()
    productname = userinput
    
    obj = os.scandir(directory)

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
        captionarr=[]
        newcaption=caption.split(' ')
        for x in newcaption:
            if x != '':
                captionarr.append(x)       
        updatedcaption=captionarr[2:]
        productname=productname.split('_')
        for y in range(0,len(productname)):    
            updatedcaption.insert(y,productname[y])
        updatedcaption=' '.join(updatedcaption)
        return updatedcaption


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
            updatedversionid=updatedmanuscriptid
            #print(updatedmanuscriptid, updatedversionid)

            #root.getroot()[0].attrib['lob']=updatedlob
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
            #Label1=Label(roottk,text="processing...",font=('helvetica', 12, 'bold')).place(x=230,y=360)
            print('wait...')


    obj.close()
    print('done')

    Label(roottk,text="Executed",font=('helvetica', 12, 'bold')).place(x=230,y=390)

submit=Button(roottk,text="submit",command=operation).place(x=240,y=320)
roottk.mainloop()
