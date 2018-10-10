import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
import os
from pathlib import Path
import folder_upload
import pickle

config_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Gupload')


class Gupload(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

        self.parent=root

        self.picklefilename = Path(config_dir, 'foldloc.dat')
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

        if self.picklefilename.exists():
            self.load()
        else:
            f = open(self.picklefilename, 'wb')
            pickle.dump({}, f)
            f.close()
            self.load()

    def create_widgets(self):
        self.dict = {}
        choices = tk.StringVar()
        self.dropdown = ttk.Combobox(self, width=12, textvariable=choices)
        self.dropdown['values'] = self.dict
        self.dropdown.grid(column=1, row=10)
        self.dropdown.pack(side="top")

        self.addbutton = ttk.Button(self)
        self.addbutton["text"] = "+"
        self.addbutton["command"] = self.AddLocwin
        self.addbutton.pack(side="top")

        self.button = ttk.Button(self)
        self.button["text"] = "Upload Files"
        self.button["command"] = self.upload
        self.button.pack(side="top")

        self.progress = ttk.Entry(self)
        self.progress["text"] = self.progmsg
        self.progress.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def load(self):
        f = open(self.picklefilename, 'rb')
        self.dict = pickle.load(f)
        for name in self.dict.keys():
            print(name, self.dict[name], len(self.dropdown['values']))


    def dump(self):
        f = open(self.picklefilename, 'wb')
        pickle.dump(self.dict, f)
        f.close()

    def progmsg(self, status):
        self.progress["text"] = status


    def upload(self):
        #print('local', self.dropdown.value[0])
        #print('remote', self.dropdown.value[1])
        #folder_upload.file_upload(self.dropdown.value[1], \
        #self.dropdown.value[0], self.progmsg)
        print('hello')

    def errclose(self):
        root.destroy

    def Errorwin(self):
        errorwin = tk.Toplevel(master=self.parent)
        Label(errorwin,text="Error: duplicate destination folder")
        self.extbutton = Button(errorwin,text="OK",command=self.errclose)
        self.extbutton.pack(side="bottom")

    def Errorwin2(self):
        errorwin2 = tk.Toplevel(master=self.parent)
        Label(errorwin2,text="Error: entry "+ name +" exists")
        self.extbutton2 = Button(errorwin,text="OK",command=self.errclose)
        self.extbutton2.pack(side="bottom")

    def searchdir(self):
        global dirsel
        dirsel = filedialog.askdirectory()


    def addentry(self, obj):
        name = obj.name.get()
        tup = (dirsel, obj.remote.get())
        print(name, tup)

        if name not in self.dict.keys():
            self.dict[name] = tup
            print(self.dict.keys())
            print(len(self.dict))
            print(len(self.dropdown['values']))
            n = len(self.dropdown['values'])
            print(self.dict)
            self.dropdown.configure(values = self.dict)
            if n == len(self.dropdown['values']):
                self.Errorwin()
                print('error1')
            print(name, tup, len(self.dropdown['values']))
            self.dump()
        else:
            self.Errorwin2()
            print('error2')

    def buttonfieldaction(self):
        self.addentry(self)
        root.destroy



    def AddLocwin(self):
        newwin = tk.Toplevel(master=self.parent)
        Label(newwin,text="Team Name").pack()
        self.name = ttk.Entry(newwin)
        self.name.pack(side="top")
        self.local = Button(newwin,text="Local Folder",command=self.searchdir)
        self.local.pack(side="top")
        Label(newwin,text="Remote Folder").pack()
        self.remote = Entry(newwin)
        self.remote.pack(side="top")
        self.buttonfield = Button(newwin,text="Create",command=self.buttonfieldaction)
        self.buttonfield.pack(side="bottom")




root = tk.Tk()
app = Gupload(master=root)
app.mainloop()
