import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
import os
from pathlib import Path
import folder_upload
import json

config_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Gupload')


class Gupload(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.dict = {}
        self.pack()
        self.create_widgets()

        self.parent=root

        self.jsonfilename = Path(config_dir, 'foldloc.dat')
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

        if self.jsonfilename.exists():
            self.load()
            update = self.dropdown.configure(values = sorted(list(self.dict.keys())))
            return update
        else:
            f = open(self.jsonfilename, 'w')
            json.dump({}, f)
            f.close()
            self.load()


    def create_widgets(self):
        choices = tk.StringVar()
        self.dropdown = ttk.Combobox(self, width=20, textvariable=choices, \
        values=sorted(list(self.dict.keys())))
        #self.dropdown['values'] = self.dict
        self.dropdown.grid(column=5, row=1)
        self.dropdown.pack(side="top")

        self.addbutton = ttk.Button(self)
        self.addbutton["text"] = "+"
        self.addbutton["command"] = self.AddLocwin
        self.addbutton.pack(side="top")

        self.button = ttk.Button(self)
        self.button["text"] = "Upload Files"
        self.button["command"] = self.upload
        self.button.pack(side="top")

        self.progress = ttk.Label(self)
        self.progress.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def load(self):
        f = open(self.jsonfilename, 'r')
        self.dict = json.load(f)
        for name in self.dict.keys():
            print(name, self.dict[name], len(self.dropdown['values']))


    def dump(self):
        f = open(self.jsonfilename, 'w')
        print(self.dict)
        json.dump(self.dict, f)
        f.close()

    def setStatus(self, status):
        self.progress["text"] = status


    def upload(self):
        selection = self.dropdown.selection_get()
        if selection in self.dict.keys():
            print('local', self.dict.get(selection)[0])
            print('remote', self.dict.get(selection)[1])
            folder_upload.file_upload((self.dict.get(selection)[1]), \
            (self.dict.get(selection)[0]), self.setStatus)
        #print('hello')

    def errclose(self):
        errorwin.destroy()

    def errclose2(self):
        errorwin2.destroy()

    def Errorwin(self, msg):
        global errorwin
        errorwin = tk.Toplevel(master=self.parent, width=200, height=120)
        errorwin.geometry("150x50")
        Label(errorwin, text=msg).pack()
        self.extbutton = Button(errorwin,text="OK",command=self.errclose)
        self.extbutton.pack(side="bottom")

    def Errorwin2(self, name):
        global errorwin2
        errorwin2 = tk.Toplevel(master=self.parent, width=200, height=120)
        errorwin2.geometry("150x50")
        Label(errorwin2,text="Error: entry "+ name +" exists").pack()
        self.extbutton2 = Button(errorwin2,text="OK",command=self.errclose2)
        self.extbutton2.pack(side="bottom")

    def searchdir(self):
        global dirsel
        dirsel = filedialog.askdirectory()


    def addentry(self, obj):
        name = obj.name.get()
        tup = (dirsel, obj.remote.get())
        print(name, tup)

        if name not in self.dict.keys():
            values = self.dict.values()
            locals = [tup[0] for tup in values]
            remotes = [tup[1] for tup in values]
            print('locals', locals)
            print('remotes', remotes)
            if len(name) == 0:
                self.Errorwin('No name given')
            if tup[0] in locals:
                self.Errorwin('Duplicate local folder')
                return
            if tup[1] in remotes:
                self.Errorwin('Duplicate remote folder')
                return
            self.dict[name] = tup

            update = self.dropdown.configure(values = sorted(list(self.dict.keys())))
            print(name, tup, len(self.dropdown['values']))
            self.dump()
            return update
        else:
            self.Errorwin2(name)
            print('error2')

    def buttonfieldaction(self):
        self.addentry(self)
        newwin.destroy()



    def AddLocwin(self):
        global newwin
        newwin = tk.Toplevel(master=self.parent, width=200, height=120)
        newwin.geometry("200x150")
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
root.geometry("200x125")
app = Gupload(master=root)
app.mainloop()
