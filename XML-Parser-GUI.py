import os
import time
import xml.etree.ElementTree as ET
import tkinter as tk

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 600, height = 600)
canvas1.pack()

label2=tk.Label(root,text="enter the directory")
canvas1.create_window(300,60,window=label2)

input1=tk.Entry(width=70)
canvas1.create_window(300,100,window=input1)

label3 = tk.Label(root,text="enter the name")
canvas1.create_window(300,150,window=label3)

input2=tk.Entry()
canvas1.create_window(300,190,window=input2)

button1 = tk.Button(text='Submit',command=hello, bg='brown',fg='white')
canvas1.create_window(300, 250, window=button1)

def hello ():
    directory=input1.get()
    os.chdir(directory)

    a = input2.get()

    obj = os.scandir(directory)


    for entry in obj:
        filename=entry.name.split('_')[1]
        #print(filename)
        os.rename(entry.path,directory+'\\'+a+'_'+filename)
        print(entry.path)

    print('processing...')
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

    
    label1 = tk.Label(root, text= "done", fg='green', font=('helvetica', 12, 'bold'))
    canvas1.create_window(300, 300, window=label1)

root.mainloop()
