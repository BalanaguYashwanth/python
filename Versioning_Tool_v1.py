import os
import xml.etree.ElementTree as ET
import time

directory=r'C:\Users\KZ623JK\OneDrive - EY\Documents\Multistate'
version='20.0.0.1'
#version=input(' enter the version number ')
#effectivedate=input(' enter the effective date ')
datas={}
all=[]
caption=''
versionID=''
version_caption=[]



def retrive(obj):
    global all
    for files in os.scandir(obj):
        if files.is_file():
            all.append(files)
        else:
            retrive(files.path)

retrive(directory)


def filterfiles(all):
    arrdata=[]
    arrpages=[]
    arrproduct=[]
    arrRating=[]
    arrRatingControl=[]
    latest=[]
    for x in all:
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
            
    latestdata=getlatestversion(arrdata)
    latestpages=getlatestversion(arrpages)
    latestproduct=getlatestversion(arrproduct)
    latestrating=getlatestversion(arrRating)
    latestratingcontrol=getlatestversion(arrRatingControl)
    #print(latestdata,latestpages,latestproduct,latestrating,latestratingcontrol)
    latest.extend([latestdata,latestpages,latestproduct,latestrating,latestratingcontrol])
    userchanges(latest)
    
                
def userchanges(datas):
    try:
        arr=[]
        for x in datas:
            newname=modify(x.name)
            y=x.path.split('\\')[:-1]
            z='\\'.join(y)
            latestpath=z+'\\'+newname
            tree=ET.parse(x.path)
            tree.write(latestpath)
            arr.append(latestpath)
            #time.sleep(2)
        changes(arr)
        #print(n)
    except Exception as e:
        print('error',e)
        
        
        
def changes(arrdatas):
    for y in arrdatas:
        #print(y)
        tree=ET.parse(y)
        root=tree.getroot()[0]
        caption=tree.getroot()[0].attrib['caption'].split(' ')[:-1]
        caption.append('('+version+')')
        version_caption.append(version.split('.'))
       
        
        newcaption=' '.join(caption)
        tree.getroot()[0].attrib['caption']=newcaption
        for objs in root:
            if objs.tag=='keys':
                for obj in objs:
                    if obj.attrib['name']=='version':
                        obj.attrib['value']=version
                        #print(obj.attrib['value'])
            
        tree.write(y)


def modify(name):
    if version:
        num=len(version.split('.'))
        versionarr=version.split('.')
        #print(versionarr)
        modified=name.split('.')[0]
        modified1=name.split('.')[1]
        latestmodified=modified.split('_')[:-num]
        return '_'.join(latestmodified+versionarr)+'.'+modified1
    else:
        return ''



    
def getlatestversion(arrdata):
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
                            

filterfiles(all)
