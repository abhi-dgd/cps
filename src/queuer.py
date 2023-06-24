# (A) LOAD MODULES
from tkinter import *

# (B) QUEUE MECHANICS
# (B1) COUNTERS
Q_ALL = 0 # total number of people in queue
QNOW = 0 # current queue number
 
# (B2) ISSUE QUEUE NUMBER
def issue():
   global qAll
   qAll += 1
   issL1["text"] = qAll
 
# (B3) NEXT CUSTOMER
def next():
  global qAll, qNow
  if qNow < qAll:
    qNow += 1
    issL2["text"] = qNow
    nowL1["text"] = qNow

# (C) BUILD INTERFACE
# (C1) ISSUE QUEUE NUMBER
issFONTA = ("Arial", 20)
issFONTB = ("Arial", 16)
issTK = Tk()
issF1 = Frame(issTK)
issB1 = Button(issF1, width=6, bg="red", fg="white", text="Issue", font=issFONTB, command=issue)
issB2 = Button(issF1, width=6, bg="blue", fg="white", text="Next", font=issFONTB, command=next)
issL1 = Label(issF1, text="0", fg="red", font=issFONTA)
issL2 = Label(issF1, text="0", fg="blue", font=issFONTA)
#issTK.geometry("640x480")
issF1.place(relx=.5, rely=.5, anchor=CENTER)
issB1.grid(row=0, column=0, pady=2)
issB2.grid(row=1, column=0, pady=2)
issL1.grid(row=0, column=1, pady=2, padx=10)
issL2.grid(row=1, column=1, pady=2, padx=10)
 
# (C2) NOW SERVING
issFONTA = ("Arial", 180)
issFONTB = ("Arial", 20)
nowTK = Tk()
nowF1 = Frame(nowTK)
nowL1 = Label(nowF1, text="0", font=issFONTA)
nowL2 = Label(nowF1, text="NOW SERVING", font=issFONTB)
nowTK.geometry("350x450")
nowF1.place(relx=.5, rely=.5, anchor=CENTER)
nowL1.pack()
nowL2.pack()
 
# (C3) START!
issTK.mainloop()
nowTK.mainloop()

