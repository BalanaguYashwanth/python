import os
import xml.etree.ElementTree as ET

directory=r'C:\Users\KZ623JK\OneDrive - EY\Documents\Carrier'

a = input('enter the name')

for entry in os.scandir(directory):
    with open(entry.path) as f:
        myroot=ET.parse(f)
        myroot.getroot()[0].attrib['name']=a
        myroot.write(entry.path)
        
