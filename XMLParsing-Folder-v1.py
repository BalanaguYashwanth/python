import os
import time
import xml.etree.ElementTree as ET

#directory=r'C:\Users\KZ623JK\OneDrive - EY\Documents\Carrier'

directory=input(r'enter the directory: ')
os.chdir(directory)

a = input('enter the name: ')
value = input('enter the attr name: ')

obj = os.scandir(directory)


for entry in obj:
    filename=entry.name.split('_')[1]
    os.rename(entry.path,directory+'\\'+a+'_'+filename)
    print(entry.path)

print('processing...')
time.sleep(4)

for entry in os.scandir(directory):
    with open(entry.path) as f:
        myroot=ET.parse(f)
        myroot.getroot()[0].attrib[value] = a
        myroot.write(entry.path)
print('done')
        
obj.close()


