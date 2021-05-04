import os
import time
import xml.etree.ElementTree as ET

directory=r'C:\Users\KZ623JK\OneDrive - EY\Documents\Carrier'

#directory=input(r'enter the directory: ')
os.chdir(directory)

a = input('enter the name: ')
#value = input('enter the attr name: ')

obj = os.scandir(directory)


for entry in obj:
    filename=entry.name.split('_')[1]
    #print(filename)
    os.rename(entry.path,directory+'\\'+a+'_'+filename)
    print(entry.path)

#print('processing...')
#time.sleep(4)

for entry in os.scandir(directory):
    with open(entry.path) as f:
        parser=ET.XMLParser(encoding='utf-8')
        myroot=ET.parse(entry.name,parser=parser)
        output=myroot.getroot()[0].attrib['manuscriptID'].split('_')
        output[0]=a
        #print(output)
        c=''
        for x in output:
            if c=='':
                c=c+x
            else:
                c=c+'_'+x
        #print(c)
        myroot.getroot()[0].attrib['manuscriptID']=c
        myroot.write(entry.path)

print('done')

obj.close()
