from tkinter import *
from tkinter.font import BOLD
import os, psutil, time
from PIL import Image, ImageTk
from prettytable import PrettyTable

class Table: 
    def __init__(self,root,lst):       
        # code for creating table 
        for i in range(len(lst)): 
            for j in range(len(lst[0])): 
                  
                self.e = Label(root, text=lst[i][j],
                               font=('Courier',14,BOLD)) 
                  
                self.e.grid(row=i, column=j,sticky="W")
                # self.e.insert(END, )

class Sthithi():

    def __init__(self):
        self.root = Tk()
        p1 = PhotoImage(file = './lotus.png')
        self.root.iconphoto(False, p1)
        self.root.wm_title('Sthithi V2.0')
        # win.geometry('500x700')
        image1 = Image.open("./lotus2.png")
        icon_image = ImageTk.PhotoImage(image1)

        img_frame = Frame(
            master=self.root,
            # relief=RAISED,
            borderwidth=1
        )
        img_frame.grid(row=0, column=0, padx=5, pady=5)
        lbl0=Label(img_frame,image=icon_image)
        lbl0.image = icon_image
        lbl0.pack(padx=5, pady=5,fill="x")

        frame = Frame(
            master=self.root,
            # relief=RAISED,
            borderwidth=1
        )
        frame.grid(row=0, column=1, padx=5, pady=5)
        lbl=Label(frame, text="Sthithi\n--------------", fg='red', font=("Courier", 16, BOLD))
        self.lbl2 =Label(frame, text="Operating System  : " + os.uname()[0], font=("Courier", 14))
        lbl.pack(padx=5, pady=5,fill="x")
        self.lbl2.pack(padx=5, pady=5,fill="x")

        img_frame2 = Frame(
            master=self.root,
            # relief=RAISED,
            borderwidth=1
        )
        img_frame2.grid(row=0, column=2, padx=5, pady=5)
        lbl02=Label(img_frame2,image=icon_image)
        lbl02.image = icon_image
        lbl02.pack(padx=5, pady=5,fill="x")

        self.poll()

    def getListOfProcessSortedByMemory(self):
        listOfProcObjects = []
        # Iterate over the list
        for proc in psutil.process_iter():
            try:
                # Fetch process details as dict
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                pinfo['vms'] = round(proc.memory_info().vms / (1024 * 1024))
                # Append dict to list
                listOfProcObjects.append(pinfo);
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        # Sort list of dict by key vms i.e. memory usage
        listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
        return listOfProcObjects

    def update_process_list(self):

        hdr_frame = Frame(
            master=self.root,
            # relief=RAISED,
            borderwidth=1
        )
        hdr_frame.grid(row=6, column=1, padx=5, pady=5)
        lbl=Label(hdr_frame, text="Top 10 Processes", font=("Courier", 14))
        lbl.pack(padx=5, pady=5,fill="x")

        table_frame = Frame(
            master=self.root,
            # relief=RAISED,
            borderwidth=1
        )
        table_frame.grid(row=7, columnspan=3)

        t=Text(table_frame)
        x=PrettyTable()
        x.field_names = ["PID", "Process Name", "User", "Virtual Memmory"]
        data = self.getListOfProcessSortedByMemory()
        for i in range(10):
            x.add_row([data[i]['pid'], data[i]['name'], data[i]['username'], str(data[i]['vms'])])

        t.insert(INSERT,x)
        t.pack(fill="x")

    def poll(self):

        frame1 = Frame(
            master=self.root,
            # relief=RAISED,
            borderwidth=1
        )
        frame1.grid(row=1, column=0, padx=5, pady=5)
        #system info
        f2 = Frame(frame1,highlightthickness=1,highlightbackground="black")
        m_details = psutil.virtual_memory()

        lst = [
            ('Total Memmory     : ', str(m_details.total >> 30) + 'Gb'),
            ('Available Memmory : ', str(m_details.available >> 30) + 'Gb'),
            ('Memmory Usage     : ', str(m_details.percent) + '%')
        ]
        t = Table(f2,lst)
        f2.grid(column=0,row=5,padx=5, pady=5)

        frame2 = Frame(
            master=self.root,
            relief=RAISED,
            borderwidth=1
        )
        frame2.grid(row=1, column=1, padx=5, pady=5)
        #time
        self.time_lbl = Label(frame2, text = time.strftime('%c'))
        self.time_lbl.pack(padx=5, pady=5,fill="x")

        #disk info
        d_details = psutil.disk_usage('/')
        frame3 = Frame(
            master=self.root,
            # relief=RAISED,
            borderwidth=1
        )
        frame3.grid(row=1, column=2, padx=5, pady=5)

        #disk info
        d_details = psutil.disk_usage('/')
        f4 = Frame(frame3,highlightthickness=1,highlightbackground="black")
        lst2 = [
            ('Total Disk : ', str(d_details.total >> 30) + 'GB'),
            ('Used Disk  : ', str(d_details.used >> 30) + 'GB'),
            ('Disk Usage : ', str(d_details.percent) + '%')
        ]
        t2 = Table(f4,lst2)
        f4.grid(column=1,row=5,padx=5, pady=5)
        
        self.update_process_list()
        self.root.after(1000, self.poll)

app = Sthithi()
app.root.mainloop()