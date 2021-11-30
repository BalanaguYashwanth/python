import os
import xml.etree.ElementTree as ET
import time


directory=input('enter the directory')
version=input('enter the version number')
effectivedate=input('enter the effective date')

#version='21.0.0.1'
#effectivedate='27-11-2021'
#directory=r'C:\Users\KZ623JK\OneDrive - EY\Documents\Multistate'


datas={}
all=[]
caption=''
versionID=''
version_caption=[]


if directory and version:
    def retrive(obj):
        global all
        for files in os.scandir(obj):
            if files.is_file():
                all.append(files)
            else:
                retrive(files.path)

    retrive(directory)


    def filterfiles(all):
        try:
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


            if len(arrdata)>0:
                latestdata=getlatestversion(arrdata)
                latest.extend([latestdata])

            if len(arrpages)>0:
                latestpages=getlatestversion(arrpages)
                latest.extend([latestpages])

            if len(arrproduct)>0:
                latestproduct=getlatestversion(arrproduct)
                latest.extend([latestproduct])

            if len(arrRating)>0:
                latestrating=getlatestversion(arrRating)
                latest.extend([latestrating])

            if len(arrRatingControl)>0:
                latestratingcontrol=getlatestversion(arrRatingControl)
                latest.extend([latestratingcontrol])
            print('latest',latest)
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
                latestpath=z+'\\'+newname
                #print(newname) #gets the name of the latest files
                tree=ET.parse(x.path)
                tree.write(latestpath)
                arr.append(latestpath)
                time.sleep(2)
            changes(arr)
            #print(n)
        except Exception as e:
            print('error',e)



    def changes(arrdatas):
        try:
            for y in arrdatas:
                #print(y)
                tree=ET.parse(y)
                root=tree.getroot()[0]
                caption=tree.getroot()[0].attrib['caption'].split(' ')[:-1]
                caption.append('('+version+')')
                newcaption=' '.join(caption)
                tree.getroot()[0].attrib['caption']=newcaption
                tree.getroot()[0].attrib['versionID']=y.split('\\')[-1].split('.')[0]
                for objs in root:
                    if objs.tag=='keys':
                        for obj in objs:
                            if obj.attrib['name']=='version':
                                obj.attrib['value']=version
                                #print(obj.attrib['value'])
                            if obj.attrib['name'] == 'effectiveDateNew':
                                obj.attrib['value']=effectivedate
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
            return '_'.join(latestmodified+versionarr)+'.'+modified1
        else:
            return ''




    def getlatestversion(arrdata):
        print('arrdata',arrdata)
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
else:
    print('please enter the required details')
