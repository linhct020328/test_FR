from mainMqttPubAes256CBC import *
from getDataset import *
from trainer import *

import os, glob

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, PhotoImage
import tkinter.simpledialog as tsd

names = set()
ids = set()
id = 0
count = 0

class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names, ids, id
        f = open("listNames/nameslist.txt", "r")
        x = f.read()
        z = x.rstrip().split("\n")
        for i in z:
            names.add(i)
        lenght = len(z)
        for l in range(lenght):
            ids.add(l)
        id = lenght - 1
        f.close()

        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.geometry("770x500")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        self.container = tk.Frame(self)
        self.container.grid(sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (LoginPage, StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.destroy()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label1 = tk.Label(self, text="BAN CO YEU CHINH PHU\nHOC VIEN KY THUAT MAT MA ", font=self.controller.title_font, fg="#3366FF")
        self.label1.grid(row=0, column=0, sticky="ew", ipadx=5, ipady=4, padx=20, pady=10)

        self.label2 = tk.Label(self, text="Do an:   Xay dung he thong chong trom thong minh su dung Raspbery\nva thuat toan hoc may",
                              font=self.controller.title_font, fg="#3366FF")
        self.label2.grid(row=1, column=0, sticky="ew",  ipadx=5, ipady=4, padx=20, pady=10)

        self.label_frame = tk.LabelFrame(self)
        self.label_frame.grid(row=2, column=0, sticky="ew", ipadx=4, ipady=4, padx=40, pady=10)

        tk.Label(self.label_frame, text="\tUserName:\t", font='Helvetica 12 bold', fg="#3366FF").grid(row=0, column=0, sticky="ew", ipadx=4, ipady=4, padx=40, pady=10)
        tk.Label(self.label_frame, text="\tPassWord:\t", font='Helvetica 12 bold', fg="#3366FF").grid(row=1, column=0, sticky="ew", ipadx=4, ipady=4, padx=40, pady=10)

        self.e1 = tk.Entry(self.label_frame, fg="#3366FF", font='Helvetica 12 bold')
        self.e1.grid(row=0, column=1, sticky="ew", ipadx=40, ipady=4, padx=20, pady=20)
        self.e2 = tk.Entry(self.label_frame, fg="#3366FF", show='*', font='Helvetica 12 bold')
        self.e2.grid(row=1, column=1, sticky="ew", ipadx=40, ipady=4, padx=20, pady=20)

        self.buttonLogin = tk.Button(self.label_frame, text="Login", font='Helvetica 12 bold',  fg="#ffffff", bg="#3366FF", command=self.login)
        self.buttonLogin.grid(row=2, column=1, sticky="ew", ipadx=40, ipady=4, padx=20, pady=20)

        self.buttonQuit = tk.Button(self, text="Quit", fg="#DD0000", bg="#ffffff", font='Helvetica 12 bold', command=self.on_closing)
        self.buttonQuit.grid(row=3, column=0, sticky="ew", ipadx=40, ipady=4, padx=40, pady=20)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.controller.destroy()

    def login(self):
        uname = self.e1.get()
        passwd = self.e2.get()
        if (uname == "" and passwd == ""):
            messagebox.showinfo("", "Blank Not allowed")

        elif (uname == "admin" and passwd == "admin"):
            self.controller.show_frame("StartPage")

        else:
            messagebox.showinfo("", "Incorrent Username and Password")


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="SELECT THE FUNCTION OF THE APPLICATION", font=self.controller.title_font, fg="#3366FF")
        self.label.grid(row=0, column=0, sticky="ew", ipadx=5, ipady=4, padx=40, pady=20)

        self.label_frame = tk.LabelFrame(self)
        self.label_frame.grid(row=1, column=0, sticky="ew", ipadx=20, ipady=4, padx=40, pady=20)

        self.button1 = tk.Button(self.label_frame, text="Face recognition", fg="#ffffff", bg="#3366FF", font='Helvetica 12 bold',
                                command=lambda: self.controller.show_frame("PageFour"))
        self.button2 = tk.Button(self.label_frame, text="List of faces", fg="#ffffff", bg="#3366FF",
                                 font='Helvetica 12 bold',
                                 command=lambda: self.controller.show_frame("PageTwo"))
        self.button4 = tk.Button(self.label_frame, text="Logout", fg="#DD0000", bg="#ffffff", font='Helvetica 12 bold',
                                 command=lambda: controller.show_frame("LoginPage"))
        self.button1.grid(row=0, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=20)
        self.button2.grid(row=1, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=20)
        self.button4.grid(row=2, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=20)

        render = PhotoImage(file='Image/homepagepic.png')
        self.img = tk.Label(self.label_frame, image=render)
        self.img.image = render
        self.img.grid(row=0, column=1, rowspan=3, sticky="nsew", ipadx=10, ipady=10, padx=60, pady=20)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="ADD MEMBER FACIAL RECOGNITION", font=self.controller.title_font,
                              fg="#3366FF")
        self.label.grid(row=0, column=0, sticky="ew", ipadx=5, ipady=4, padx=40, pady=10)

        self.label_frame = tk.LabelFrame(self)
        self.label_frame.grid(row=1, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=20)

        tk.Label(self.label_frame, text="Enter the name", fg="#3366FF", font='Helvetica 12 bold').grid(row=0, column=0, sticky="ew", ipadx=20, ipady=4, padx=60, pady=20)
        self.user_name = tk.Entry(self.label_frame, borderwidth=3, bg="lightgrey", font='Helvetica 12 bold')
        self.user_name.grid(row=0, column=1, sticky="ew", ipadx=60, ipady=4, padx=40, pady=20)
        self.check_name = tk.Button(self.label_frame, text="List of faces", font='Helvetica 12 bold', fg="#ffffff", bg="#3366FF", command=lambda: controller.show_frame("PageTwo"))
        self.buttonext = tk.Button(self.label_frame, text="Next", font='Helvetica 12 bold', fg="#ffffff", bg="#3366FF", command=self.start_training)
        self.buttoncanc = tk.Button(self.label_frame, text="Cancel", font='Helvetica 12 bold', bg="#ffffff", fg="#DD0000", command=lambda: controller.show_frame("StartPage"))
        self.buttonext.grid(row=1, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)
        self.check_name.grid(row=2, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)
        self.buttoncanc.grid(row=3, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)

        render = PhotoImage(file='Image/homepagepic.png')
        self.img = tk.Label(self.label_frame, image=render)
        self.img.image = render
        self.img.grid(row=1, column=1, rowspan=4, sticky="nsew", ipadx=10, ipady=10, padx=60, pady=10)

    def start_training(self):
        global names, ids, id
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        id = id + 1
        ids.add(id)
        f = open("listNames/nameslist.txt", "a+")
        f.write("\n" + self.controller.active_name)
        f.close()
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names, ids
        self.controller = controller
        self.lable = tk.Label(self, text="LIST OF FACIAL RECOGNITION MEMBERS", fg="#3366FF", font=self.controller.title_font)
        self.lable.grid(row=0, column=0, sticky="ew", ipadx=5, ipady=8, padx=40, pady=10)
        self.label_frame = tk.LabelFrame(self)
        self.label_frame.grid(row=1, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)
        self.label_frame_list = tk.LabelFrame(self.label_frame)
        self.label_frame_list.grid(row=0, column=0, sticky="ew", rowspan=5, padx=40, pady=20)

        self.yScroll = tk.Scrollbar(self.label_frame_list, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=1, sticky='ns')
        self.xScroll = tk.Scrollbar(self.label_frame_list, orient=tk.HORIZONTAL)
        self.xScroll.grid(row=1, column=0, sticky='ew')

        self.listNames = tk.Listbox(self.label_frame_list, height=15, fg="#3366FF", font='Helvetica 12 bold' ,xscrollcommand=self.xScroll.set, yscrollcommand=self.yScroll.set)
        self.listNames.grid(row=0, column=0, sticky='nsew', ipadx=75)
        self.xScroll['command'] = self.listNames.xview
        self.yScroll['command'] = self.listNames.yview

        list_names = []
        f = open("listNames/nameslist.txt", "r")
        x = f.read()
        z = x.rstrip().split("\n")
        for i in z:
            smallList = i.rstrip()
            list_names.append(smallList)
        for name in list_names:
            if name == 'None':
                continue
            self.listNames.insert(tk.END, name)
        f.close()

        self.add_user = tk.Button(self.label_frame, text="Add a face", fg="#ffffff", bg="#3366FF", font='Helvetica 12 bold',
                                  command=lambda: controller.show_frame("PageOne"))
        self.edit_user = tk.Button(self.label_frame, text="Edit a face", fg="#ffffff", bg="#3366FF", font='Helvetica 12 bold',
                                  command=self.edit_name)
        self.delete_user = tk.Button(self.label_frame, text="Delete a face", fg="#ffffff", bg="#3366FF", font='Helvetica 12 bold',
                                  command=self.delete_name)
        self.delete_all_users = tk.Button(self.label_frame, text="Delete all faces", fg="#ffffff", bg="#3366FF", font='Helvetica 12 bold',
                                     command=self.delete_all_names)
        self.buttoncanc = tk.Button(self.label_frame, text="Cancel", command=lambda: controller.show_frame("StartPage"), font='Helvetica 12 bold',
                                    bg="#ffffff", fg="#DD0000")

        self.add_user.grid(row=0, column=1, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)
        self.edit_user.grid(row=1, column=1, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)
        self.delete_user.grid(row=2, column=1, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)
        self.delete_all_users.grid(row=3, column=1, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)
        self.buttoncanc.grid(row=4, column=1, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)

    def refresh_names(self):#update listbox
        global names, ids, id
        self.listNames.delete(0, tk.END)
        list_names = []
        f = open("listNames/nameslist.txt", "r")
        x = f.read()
        z = x.rstrip().split("\n")
        for i in z:
            smallList = i.rstrip()
            list_names.append(smallList)
        lenght = len(z)
        for l in range(lenght):
            ids.add(l)
        id = lenght - 1
        for name in list_names:
            if name == 'None':
                continue
            self.listNames.insert(tk.END, name)
        f.close()

    def edit_name(self):
        global names, ids
        if messagebox.askokcancel("Quit", "Are you sure?"):
            for line in self.listNames.curselection():
                name_old = self.listNames.get(line)
                name_new = tsd.askstring("Input", "Enter a new name instead of " + name_old)
                if name_new == None:
                    messagebox.showerror("Error", "Name cannot be 'None'")
                    return
                elif name_new in names:
                    messagebox.showerror("Error", "User already exists!")
                    return
                elif name_new == name_old:
                    messagebox.showerror("Error", "User already exists!")
                    return
                elif len(name_new) == 0:
                    messagebox.showerror("Error", "Name cannot be empty!")
                    return
                a_file = open("listNames/nameslist.txt", "r")
                list_of_lines = a_file.readlines()
                if line < self.listNames.size() - 1:
                    list_of_lines[line+1] = name_new + "\n"

                    a_file = open("listNames/nameslist.txt", "w")
                    a_file.writelines(list_of_lines)
                    a_file.close()
                else:
                    list_of_lines[line + 1] = name_new

                    a_file = open("listNames/nameslist.txt", "w")
                    a_file.writelines(list_of_lines)
                    a_file.close()

                self.listNames.delete(line)
                names.remove(name_old)
                names.add(name_new)
                self.listNames.insert(line, name_new)
                self.controller.active_name = name_new
                self.controller.frames["PageTwo"].refresh_names()
                try:
                    if messagebox.askokcancel("Quit", "you want to train again?"):
                        startTrain()
                        messagebox.showinfo("SUCCESS", "successful training!")
                        self.controller.show_frame("PageTwo")
                except:
                    pass

    def delete_name(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names, ids
            for line in self.listNames.curselection():

                name = self.listNames.get(line)
                p = './datasets/User.' + str(line+1) + '.' + "*" + '.jpg'
                fileDataset = glob.glob(p, recursive=True)
                for f in fileDataset:
                    try:
                        os.remove(f)
                    except OSError as e:
                        print("Error: %s : %s" % (f, e.strerror))
                if line < self.listNames.size() - 1:
                    a_file = open("listNames/nameslist.txt", "r")
                    list_of_lines = a_file.readlines()
                    list_of_lines[line + 1] = ""

                    a_file = open("listNames/nameslist.txt", "w")
                    a_file.writelines(list_of_lines)
                    a_file.close()
                else:
                    a_file = open("listNames/nameslist.txt", "r")
                    readFile = a_file.read()
                    a_file.close()
                    m = readFile.split("\n")
                    lines = "\n".join(m[:-1])
                    a_file = open("listNames/nameslist.txt", "w+")
                    for i in range(len(lines)):
                        a_file.write(lines[i])
                    a_file.close()

                names.remove(name)
                ids.remove(line + 1)
                self.listNames.delete(line)

                listIds = sorted(ids)#chuyen sang lisst
                #chay tat ca cac file: neu count 2 file canh nhau l?? cach nhau th?? rename
                global count
                for i in listIds:
                    if i > line + 1:
                        path_old = './datasets/User.' + str(i) + '.' + "*" + '.jpg'
                        for file_name_old in glob.glob(path_old):
                            p_old = file_name_old
                            p_new = './datasets/User.' + str(int(i) - 1) + '.' + str(count) + '.jpg'
                            count += 1
                            os.rename(p_old, p_new)
                            if count == 200:
                                count = 0

                self.controller.frames["PageTwo"].refresh_names()

            try:
                if messagebox.askokcancel("Quit", "you want to train again?"):
                    startTrain()
                    messagebox.showinfo("SUCCESS", "successful training!")
                    self.controller.show_frame("PageTwo")
            except:
                pass

    def delete_all_names(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names, ids
            p = './datasets/*.jpg'
            fileDataset = glob.glob(p, recursive=True)
            for f in fileDataset:
                try:
                    os.remove(f)
                except OSError as e:
                    print("Error: %s : %s" % (f, e.strerror))

            list_names = []
            f = open("listNames/nameslist.txt", "r")
            x = f.read()
            z = x.rstrip().split("\n")
            for i in z:
                smallList = i.rstrip()
                list_names.append(smallList)
            for name in list_names:
                names.remove(name)
            for i in range(len(list_names)):
                ids.remove(i)
            f.close()
            f = open("listNames/nameslist.txt", "w")
            f.write('None')
            f.close()
            self.listNames.delete(0, tk.END)

            self.controller.show_frame("PageTwo")
            self.controller.frames["PageTwo"].refresh_names()
            try:
                if messagebox.askokcancel("Quit", "you want to train again?"):
                    startTrain()
                    messagebox.showinfo("SUCCESS", "successful training!")
                    self.controller.show_frame("PageTwo")
            except:
                pass

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.lable = tk.Label(self, text="GET THE DATASET AND TRAINING", fg="#3366FF", font=self.controller.title_font)
        self.lable.grid(row=0, column=0, sticky="ew", ipadx=5, ipady=8, padx=40, pady=10)
        self.label_frame = tk.LabelFrame(self)
        self.label_frame.grid(row=1, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)

        self.numimglabel = tk.Label(self.label_frame, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#3366FF")
        self.numimglabel.grid(row=0, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)
        self.capturebutton = tk.Button(self.label_frame, text="Capture Data Set", font='Helvetica 12 bold', fg="#ffffff", bg="#3366FF", command=self.capimg)
        self.button4 = tk.Button(self.label_frame, text="Go to Home Page", font='Helvetica 12 bold', command=lambda: self.controller.show_frame("StartPage"),
                            bg="#ffffff", fg="#DD0000")
        self.capturebutton.grid(row=1, column=0, sticky="ew", ipadx=10, ipady=4, padx=20, pady=10)
        self.button4.grid(row=2, column=0, sticky="ew", ipadx=10, ipady=4, padx=20, pady=10)

        render = PhotoImage(file='Image/homepagepic.png')
        self.img = tk.Label(self.label_frame, image=render)
        self.img.image = render
        self.img.grid(row=0, column=1, rowspan=3, sticky="nsew", ipadx=10, ipady=10, padx=20, pady=20)

    def capimg(self):
        global id
        self.numimglabel.config(text=str("Number of images captured = 0"))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 200 pic of your Face.")
        x = start_dataset(id)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))
        try:
            if messagebox.askokcancel("Quit", "you want to train again?"):
                startTrain()
                messagebox.showinfo("SUCCESS", "successful training!")
                self.controller.show_frame("PageTwo")
        except:
            pass


class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.lable = tk.Label(self, text="START FACIAL RECOGNITION MODEL", fg="#3366FF", font=self.controller.title_font)
        self.lable.grid(row=0, column=0, sticky="ew", ipadx=5, ipady=8, padx=40, pady=20)
        self.label_frame = tk.LabelFrame(self)
        self.label_frame.grid(row=1, column=0, sticky="ew", ipadx=10, ipady=10, padx=40, pady=20)

        self.button1 = tk.Button(self.label_frame, text="Capture open", font='Helvetica 12 bold', command=self.openwebcam, fg="#ffffff", bg="#3366FF")
        self.trainbutton = tk.Button(self.label_frame, text="Training", font='Helvetica 12 bold', command=self.trainmodel, fg="#ffffff", bg="#3366FF")
        self.button2 = tk.Button(self.label_frame, text="Go to Home Page", font='Helvetica 12 bold', command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#DD0000")
        self.button1.grid(row=1, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)
        self.trainbutton.grid(row=2, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)
        self.button2.grid(row=3, column=0, sticky="ew", ipadx=10, ipady=4, padx=40, pady=10)

        render = PhotoImage(file='Image/homepagepic.png')
        self.img = tk.Label(self.label_frame, image=render)
        self.img.image = render
        self.img.grid(row=1, column=3, rowspan=3, sticky="nsew", ipadx=10, ipady=10, padx=60, pady=10)

    def openwebcam(self):
        startFaceRecongition()

    def trainmodel(self):
        startTrain()
        messagebox.showinfo("SUCCESS", "successful training!")
        self.controller.show_frame("PageFour")


app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='Image/icon.png'))
app.mainloop()


