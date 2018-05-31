import tkinter as tk
from PIL import ImageTk, Image
from pandas import DataFrame as df
import os

import argparse
# for parsing arguments from Command Line
class GUI(object):
    """Main GUI class for the system"""
    
    def __init__(self):
        self.files=[]
        self.index=0
        self.labels={}
        ap = argparse.ArgumentParser()
        ap.add_argument("-k", "--keywords", required=True,
        	help="keywords in url to be found, must be comma-separted if more than 1 Eg. class1,positve,png or class2,negative,jpg")
        # classes argument
        ap.add_argument("-c", "--classes", required=True,
            help="names of target classes to be used, must be comma-separted and mentioned ordinally (as we'll use 0 for first class, 1 for second and so on) . Eg. dog,cat or abnormal,normal")
        # keyboard shortcut arguments
        ap.add_argument("-s", "--shortcuts", required=True,
            help="keyboard shortcuts to be used to trigger label buttons, must be comma-separted and in same order as the classes in -c argument. Eg. d,g (for dog,cat) or a,n (for abnormal,normal)")
        # filename argument
        ap.add_argument("-f", "--filename",
            help="filename used to save the final label files, filename must be given without extension (mylabel for mylabels.csv). if this argument is empty, default name is \"labels.csv\" ")
        
        args = vars(ap.parse_args())
        print(args)

        #Extract arguments

        classes=args['classes'].split(',')
        shortcuts=args['shortcuts'].split(',')
        if len(classes) != len(shortcuts):
            raise ValueError("number of classes and shortcuts are not equal")


        shortcuts=["<"+key+">" for key in shortcuts]
        filename=("labels.csv",str(args['filename'])+".csv")[args['filename'] is None]

        print(classes)
        print(shortcuts)
        print(filename)

        #Get the list of files

        mylist = [x[0] for x in os.walk("..\..")]

        for i in str(args['keywords']).split(','):
        	mylist = [x for x in mylist if i.lower() in str(x).lower()]

        for x in mylist:
        	myfiles=[f[2] for f in os.walk(x)]
        	self.files+=[x+"\\"+fi for fi in myfiles[0]]	
        

        #Create main window
        window = tk.Tk()

        #divide window into two sections. One for image. One for buttons
        top = tk.Frame(window)
        top.pack(side="top")
        bottom3 = tk.Frame(window)
        bottom3.pack(side="bottom")
        bottom = tk.Frame(window)
        bottom.pack(side="bottom")
        bottom2 = tk.Frame(window)
        bottom2.pack(side="bottom")

        title = tk.Label(window,text=self.files[self.index].split("\\")[-3:-1])
        title.pack()

        #place image
        
        it=iter(self.files)
        path = self.files[self.index]
        im=Image.open(path)
        im.thumbnail((800,800),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(im)
        panel = tk.Label(window, image = img)
        panel.image = img # keep a reference!
        panel.pack(side = "top", fill = "both", expand = "yes")

        #place buttons
        prev_button = tk.Button(window, text="Previous", width=10, height=2, 
            command=lambda: self.drawImage(panel,self.getPath(-1),title))
        prev_button.pack(in_=bottom, side="left")
        next_button = tk.Button(window, text="Next", width=10, height=2, 
            command=lambda: self.drawImage(panel,self.getPath(1),title))
        next_button.pack(in_=bottom, side="right")

        buttons=[]

        for x in range(0,len(classes)):
            btn=tk.Button(window, text=classes[x].title(), width=10, height=2)
            buttons.append(btn)
            btn.pack(in_=bottom2, side="left")
            btn.bind('<Button>', lambda e: self.getRec(self.getPath(0),classes.index(e.widget.cget('text').lower()),next_button))

            window.bind(shortcuts[x], lambda e: self.getRec(self.getPath(0),shortcuts.index('<'+e.char+'>'),next_button))


        save_button = tk.Button(window, text="Save", width=10, height=2, 
            command=lambda: self.saveCSV(filename))
        save_button.pack(in_=bottom3, side="bottom")

        # binding keys
        window.bind('<Left>', lambda e: prev_button.invoke())
        window.bind('<Right>', lambda e: next_button.invoke()) 
        #Start the GUI
        window.mainloop()

    def saveCSV(self,filename):
        self.labels=[(k,v) for k,v in self.labels.items()]
        frame=df.from_records(self.labels)
        file_name="..\\..\\"+filename
        with open(file_name, 'a') as f:
            frame.to_csv(f, sep=',', encoding='utf-8', index=False, header=False)
        print("Saved!")

    def getRec(self,path,label,button):
        print(label)
        path="\\".join(path.split("\\")[2:])
        path=path.replace("\\",r"/")
        self.labels[path]=label
        print(self.labels)
        button.invoke()

    def getPath(self,num):  
        try:
            self.index+=num
            print(self.index)
            if self.index<0 or self.index>=len(self.files):
                raise ValueError('Index value out of range.')
        except Exception as e:
            print(e)
            self.index-=num
            print(self.index)
        finally:
            return self.files[self.index]

    def drawImage(self,panel,path,title):
        title.config(text=path.split("\\")[-3:-1])
        im=Image.open(path)
        im.thumbnail((600,600),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(im)
        panel.configure(image=img)
        panel.image = img # keep a reference!

GUI()