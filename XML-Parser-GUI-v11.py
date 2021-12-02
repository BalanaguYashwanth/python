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

#version_directory=Label(roottk,text="Versioning Files Directory").place(x=30,y=160)
version=Label(roottk,text="Version No.").place(x=30,y=180)


input_directory = Entry(roottk,width=70)
input_directory.place(x=180,y=20)
input_catalogdir = Entry(roottk,width=70)
input_catalogdir.place(x=180,y=60)
newfile_input = Entry(roottk,width=40)
newfile_input.place(x=180,y=100)
input_effective_date = Entry(roottk,width=40)
input_effective_date.place(x=180,y=140)

#input_versiondirectory = Entry(roottk,width=70)
#input_versiondirectory.place(x=180,y=160)
input_version = Entry(roottk,width=40)
input_version.place(x=180,y=180)

alls=[]

def operation():
    
    states=['Import','RemoveLOB','Data','Product','Rating','RatingControl','Validation','Forms','Pages','FormsControl']
    
    Label(roottk,text="processed",font=('helvetica', 12, 'bold')).place(x=230,y=360)

    directory=input_directory.get()
    catalogdir=input_catalogdir.get()
    userinput = newfile_input.get()
    effective_date = input_effective_date.get()
    productname = userinput
    
    #v_directory = input_versiondirectory.get()
    v_version = input_version.get()
    
    obj = os.scandir(directory)

    updatedname=[]
    newname=''
    samplename=[]
    oldname=[]
    oldpath=[]
    global alls
    
    parser=ET.XMLParser(encoding='utf-8')
    catalogroot=ET.parse(catalogdir,parser=parser)
    
    
    def rename(name):
        try:
            global number
            for z in userinput:
                if z == '_':
                    #print('underscored called')
                    number=2
                    return name[2:]
                    break
            if name[0]=='DuckCreekTech':
                #print('dct called')
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
                        #print(x)
                        #global number
                        number=1
                        return name[1:]
                if flag==0:
                    #print('warning:check to files processed properly')
                    Label(roottk,text="warning:check the files whether processed properly").place(x=190,y=380)
                    number=2
                    return name[2:]
        except Exception as e:
            print('rename error is',e)


    for entry in obj:                            #main_code
        for x in os.scandir(entry.path):
            oldname.append(x.path)
            oldpath.append(entry.path)
            name=x.name.split('_')
            uname=rename(name)
            updatedname=uname
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


    for x in range(0,len(samplename)):
        os.rename(oldname[x],oldpath[x]+'\\'+samplename[x]) #need to change

    print('done')
    print('processing...') #setup some delay
    time.sleep(3)

    def splitjoin(sampleid, productname):
        try:
            #if not "Data" in file.name and not "Product" in file.name and not "Rating_US" in file.name and not "RatingControl_US" in file.name:
            newsampleid=sampleid.split('_')
            newmanuscript=newsampleid[number:]
            #print('newmanuscript productname',newmanuscript,productname)
            newmanuscript.insert(0,productname)
            newmanuscript= '_'.join(newmanuscript)
            return newmanuscript
            #else:
                #return sampleid
        except Exception as e:
            print("splitjoin error is",e)

    def splitjoinlob(productname,manuscriptid):
        try:
            for x in manuscriptid.split('_'):
                if x == 'Forms':
                    productname=productname+x
                elif x == 'FormsControl':
                    productname=productname+'Forms'
            productname=productname.split('_')
            productname=''.join(productname)
            return productname
        except Exception as e:
            print("splitjoin lob error is",e)

    def splitjoincaption(caption,productname):
        try:
            #if not "Data" in file.name and not "Product" in file.name and not "Rating_US" in file.name and not "RatingControl_US" in file.name:
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
            #else:
             #   return caption
        except Exception as e:
            print("splitjoin caption error is",e)

    def renameurl(path):
        try:
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
        except Exception as e:
            print("rename url error is",e)
    
    
    #versioning startcode
    
    datas={}
    #alls=[]
    v_caption=[]
    #versionID=''
    #version_caption=[]
    
    #v_directory=input('enter the directory')
    version=v_version
    #effectivedate=input('enter the effective date')

    if directory and version:
        def retrive(obj):
            #global alls
            for files in os.scandir(obj):
                if files.is_file():
                    alls.append(files)
                else:
                    retrive(files.path)

        retrive(directory)


        def filterfiles(alls):
            try:
                totalarr=[]
                arrdata=[]
                arrpages=[]
                arrproduct=[]
                arrRating=[]
                arrRatingControl=[]
                arrforms_multistate=[]
                arrforms_us=[]
                arrformscontrol_us=[]
                latest=[]
                
                for x in alls:
                    if "Data" in x.name:
                        arrdata.append(x)
                    elif "Pages" in x.name:
                        arrpages.append(x)
                    elif "Product" in x.name:
                        arrproduct.append(x)
                    elif "Rating_US" in x.name:
                        arrRating.append(x)
                    elif "RatingControl_US" in x.name:
                        arrRatingControl.append(x)
                    elif "Forms_Multistate" in x.name:
                        arrforms_multistate.append(x)
                    elif "Forms_US" in x.name:
                        arrforms_us.append(x)
                    elif "FormsControl_US" in x.name:
                        arrformscontrol_us.append(x)

                totalarr.extend([arrdata,arrpages,arrproduct,arrRating,arrRatingControl,arrforms_multistate,arrforms_us,arrformscontrol_us])


                for x in totalarr:
                    if len(x)>0:
                        latestdata=getlatestversion(x)
                        latest.extend([latestdata])

                #print(latest)
                userchanges(latest)
            except Exception as e:
                print('error',e)


        def userchanges(datas):
            try:
                arr=[]
                for x in datas:
                    newname=modify(x.name)
                    y=x.path.split('\\')[:-1]
                    z='\\'.join(y)
                    latestpath=z+'\\'+newname+'.xml'
                    print('path',latestpath) #gets the name of the latest files
                    tree=ET.parse(x.path)
                    tree.write(latestpath)
                    arr.append(latestpath)
                    time.sleep(2)
                changes(arr)
                #print(n)
            except Exception as e:
                print('error',e)


        #add print of new name
        def changes(arrdatas):
            try:
                for y in arrdatas:
                    #print('path',y)
                    tree=ET.parse(y)
                    root=tree.getroot()[0]
                    manuscriptname=modify(tree.getroot()[0].attrib['manuscriptID']+'.xml')
                    #print('updatedmanuscriptname',manuscriptname)
                    v_caption=tree.getroot()[0].attrib['caption'].split(' ')[:-1]
                    v_caption.append('('+version+')')
                    v_newcaption=' '.join(v_caption)
                    
                    tree.getroot()[0].attrib['caption']=v_newcaption
                    tree.getroot()[0].attrib['manuscriptID']=manuscriptname
                    tree.getroot()[0].attrib['versionDate']=effective_date
                    for objs in root:
                        #if objs.tag=='notes':
                            #print(objs.text)
                        if objs.tag=='keys':
                            for obj in objs:
                                if obj.attrib['name']=='version':
                                    obj.attrib['value']=version
                                    #print(obj.attrib['value'])
                                if obj.attrib['name'] == 'effectiveDateNew':
                                    obj.attrib['value']=effective_date
                                if obj.attrib['name'] == 'effectiveDateRenewal':
                                    obj.attrib['value']=effective_date

                    tree.write(y)
            except Exception as e:
                print(e)



        def modify(name):
            if version:
                num=len(version.split('.'))
                versionarr=version.split('.')
                #print(versionarr)
                modified=name.split('.')[0]
                modified1=name.split('.')[1]
                latestmodified=modified.split('_')[:-num]
                return '_'.join(latestmodified+versionarr)
            else:
                return ''




        def getlatestversion(arrdata):
            #print('arrdata',arrdata)
            new=0
            datadict={}
            for n in arrdata:
                #print(n.path)
                tree=ET.parse(n.path)
                root=tree.getroot()[0]
                for x in root:
                    if x.tag=='keys':
                        for y in x:
                            if y.attrib['name']=='version':
                                total=''
                                for num in (y.attrib['value'].split('.')):
                                    total=total+(num)
                                    numtotal=int(total)
                                datadict[numtotal]=n
                                if numtotal>new:
                                    new=numtotal

            #print(new)
            return (datadict[new])


        filterfiles(alls)
        print('succesfully completed')
    else:
        print('please enter the required details')
    
    
    
    #versioning endcode
    
    try:
        for entry in os.scandir(directory):
            for file in os.scandir(entry):
                parser=ET.XMLParser(encoding='utf-8')
                root=ET.parse(file.path,parser=parser)
                root.getroot()[0].attrib['versionDate']=effective_date
                
                manuscriptid = root.getroot()[0].attrib['manuscriptID']
                versionid = root.getroot()[0].attrib['versionID']
                caption = root.getroot()[0].attrib['caption']

                #print('manuscriptid, productname, caption - ',manuscriptid, productname, caption)
                updatedmanuscriptid=splitjoin(manuscriptid, productname)
                time.sleep(0.4)
                updatedlob=splitjoinlob(productname,manuscriptid)
                time.sleep(0.2)
                updatedcaption=splitjoincaption(caption,productname)
                time.sleep(0.4)
                updatedversionid=updatedmanuscriptid
              
                #root.getroot()[0].attrib['lob']=updatedlob
                
                root.getroot()[0].attrib['caption']=updatedcaption
                root.getroot()[0].attrib['manuscriptID']=updatedmanuscriptid
                root.getroot()[0].attrib['versionID']=updatedversionid
                
                
                #manuscriptcatalog
                try:
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
                except Exception as e:
                    print("manuscript catalog error is",e)
                #Label1=Label(roottk,text="processing...",font=('helvetica', 12, 'bold')).place(x=230,y=360)
                #print('wait...')
    except Exception as e:
        print('error is',e)

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
