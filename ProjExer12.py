from tkinter import *
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk
import csv
import os
from reportlab.pdfgen import canvas

window = Tk()
window.title("Window")
window.geometry("1300x800")
window.configure(bg = "white")

frame = Frame(window)
frame.place(x = 593, y = 65, width = 688, height = 300)

frame2 = Frame(window)
frame2.place(x = 593, y = 415, width = 688, height = 300)


############################################## GLOBAL VARIABLES ###############################################

store = []
storeCustProd = []
# currId = 1
idx = None
idxTable1 = None
idxTable2 = None
deleted = []
currDate = datetime.today().strftime("%m/%d/%Y").split("/")
prodFrame1 = None
prodFrame2 = None
prodStore1 = []
prodStore2 = []
ProdidNum, ProdType, ProdDes, ProdSupp, ProdQuant, ProdAddQuant, ProdTot, ProdDate, ProdLabor, ProdOverhead, ProdProfit = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
# tableID = 1
checkSame = []
CustProdInvoice = []
CustProdID = []
productWindow = None
################################################## FUNCTIONS ##################################################


def emailKey(q):
    emailVar = email.get()
    if "@" in emailVar and emailVar.index("@") > 0 and emailVar.count("@") == 1 and ".com" in emailVar and emailVar.index(".com") == len(emailVar)-4 and emailVar.count(".com") == 1:
        changeEmail.config(text = "Correct Email Format", foreground = "green")
    else:
        changeEmail.config(text = "Incorrect Email Format", foreground = "red")

    if not emailVar:
        changeEmail.config(text = "[a-z]@[a-z].com", foreground = "black")


def bdayKey(q):
    bdayVar = bday.get()
    splitted = bdayVar.split("/")
    if len(bdayVar) == 10:
        for x in range(len(splitted)):
            if len(splitted[0]) == 2 and splitted[0].isdigit() and int(splitted[0]) < 13:
                if len(splitted[1]) == 2 and splitted[1].isdigit() and int(splitted[1]) < 32:
                    if len(splitted[2]) == 4 and splitted[2].isdigit(): 
                        if int(splitted[x]) < int(currDate[x]) - 17:
                            changeBday.config(text = "Correct Birthday Format", foreground = "green")
                        elif int(splitted[2]) == int(currDate[2]) - 17:
                            if int(splitted[0]) <= int(currDate[0]):
                                if int(splitted[1]) <= int(currDate[1]):
                                    changeBday.config(text = "Correct Birthday Format", foreground = "green")
                                else:
                                    changeBday.config(text = "Minors are not allowed", foreground = "red")
                            else:
                                changeBday.config(text = "Minors are not allowed", foreground = "red")
                        else:
                            changeBday.config(text = "Minors are not allowed", foreground = "red")
                    else:
                        changeBday.config(text = "Incorrect Birthday Format", foreground = "red")
                else:
                    changeBday.config(text = "Incorrect Birthday Format", foreground = "red")
            else:
                changeBday.config(text = "Incorrect Birthday Format", foreground = "red")
    else:
        changeBday.config(text = "Incorrect Birthday Format", foreground = "red")
    
    if not bdayVar:
        changeBday.config(text = "MM/DD/YYYY", foreground = "black")

def delete():
    global idx
    if type(idx) == int:
        if (messagebox.askyesno("Question", f"Do you want to delete ID Number {store[idx][0]}")):
            messagebox.showinfo("Deleted", f"ID number {store[idx][0]} has been deleted")
            for w in frame.winfo_children():
                w.destroy()
            deleted.append(store[idx][0])
            deleted.sort()
            idNum.configure(text = str(deleted[0])) 
            store.pop(idx)
            createTable()
            storeCustProd.pop(idx)
        else:
            messagebox.showinfo("Cancelled", "Data was not deleted")
        idx = None
        Custwritecsv()
        ProdCustwritecsv()
        Deletewritecsv()
    else:
        messagebox.showerror("Error!", "Please select a row")

def update():
    # global currId
    global store
    global idx
    varName = name.get()
    varAdd = add.get()
    varNum = num.get()
    varBday = bday.get()
    varEmail = email.get()
    if type(idx) == int:
        if len(varName) > 0:
            if len(varAdd) > 0:
                if len(varNum) > 0:
                    if len(varEmail) > 0:
                        if len(varBday) > 0:
                            if "," in varName and varName.index(",") > 0:
                                if changeEmail['text'] == "Incorrect Email Format":
                                    vemail.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                                    messagebox.showerror("Not Saved!", "Email Format should be ([a-z]@[a-z].com)")
                                    vemail.config(highlightthickness=0)
                                elif changeBday['text'] == "Incorrect Birthday Format":
                                    vbday.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                                    messagebox.showerror("Not Saved!", "Date Format should be (MM/DD/YYYY)")
                                    vbday.config(highlightthickness=0)
                                elif changeBday['text'] == "Minors are not allowed":
                                    vbday.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                                    messagebox.showerror("Not Saved!", "Only 18 and above are allowed")
                                    vbday.config(highlightthickness=0) 
                                else:
                                    messagebox.showinfo("Saved", f"ID Number {store[idx][0]} has been Updated")
                                    store[idx] = (store[idx][0], varName, varAdd, varNum, varEmail, varBday, gender.get()) 
                                    createTable()
                                    Custwritecsv()
                            else: 
                                vname.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                                messagebox.showerror("Not Saved!", "Format should be (Lastname, Firstname)")
                                vname.config(highlightthickness=0)   
                        else:
                            vbday.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                            messagebox.showerror("Not Saved!", "Birthday is empty")  
                            vbday.config(highlightthickness=0)                           
                    else:
                        vemail.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                        messagebox.showerror("Not Saved!", "Email is empty")
                        vemail.config(highlightthickness=0)                        
                else:
                    vnum.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                    messagebox.showerror("Not Saved!", "Contact Number is empty")
                    vnum.config(highlightthickness=0)
            else:
                vadd.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                messagebox.showerror("Not Saved!", "Address is empty")
                vadd.config(highlightthickness=0)                
        else:
            vname.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
            messagebox.showerror("Not Saved!", "Name is empty")
            vname.config(highlightthickness=0)
        idx = None
    else:
        messagebox.showerror("Error!", "Please select a row")

def save():
    # global currId
    global store
    varName = name.get()
    varAdd = add.get()
    varNum = num.get()
    varBday = bday.get()
    varEmail = email.get()
    if len(varName) > 0:
        if len(varAdd) > 0:
            if len(varNum) > 0:
                if len(varEmail) > 0:
                    if len(varBday) > 0:
                        if "," in varName and varName.index(",") > 0:
                            if changeEmail['text'] == "Incorrect Email Format":
                                vemail.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                                messagebox.showerror("Not Saved!", "Email Format should be ([a-z]@[a-z].com)")
                                vemail.config(highlightthickness=0)
                            elif changeBday['text'] == "Incorrect Birthday Format":
                                vbday.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                                messagebox.showerror("Not Saved!", "Date Format should be (MM/DD/YYYY)")
                                vbday.config(highlightthickness=0)
                            elif changeBday['text'] == "Minors are not allowed":
                                vbday.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                                messagebox.showerror("Not Saved!", "Only 18 and above are allowed")
                                vbday.config(highlightthickness=0) 
                            else:
                                messagebox.showinfo("Saved", "The Data are saved")
                                checkSame.append([])
                                storeCustProd.append([])
                                CustProdID.append(0)
                                currId = len(store) + 1
                                if CustProdInvoice:
                                    CustProdInvoice.append(CustProdInvoice[-1]+1)
                                else:
                                    CustProdInvoice.append(4090)
                                if deleted:
                                    store.append((str(deleted[0]), varName, varAdd, varNum, varEmail, varBday, gender.get()))
                                    if len(deleted) > 1:
                                        idNum.configure(text = deleted[1])
                                    else:
                                        idNum.configure(text = str(currId))
                                    deleted.pop(0)
                                else:
                                    idNum.configure(text = str(currId + 1))                            
                                    store.append((str(currId), varName, varAdd, varNum, varEmail, varBday, gender.get()))
                                    # currId += 1
                                createTable()
                                Deletewritecsv()
                                Custwritecsv()
                        else: 
                            vname.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                            messagebox.showerror("Not Saved!", "Format should be (Lastname, Firstname)")
                            vname.config(highlightthickness=0)   
                    else:
                        vbday.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                        messagebox.showerror("Not Saved!", "Birthday is empty")  
                        vbday.config(highlightthickness=0)                           
                else:
                    vemail.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                    messagebox.showerror("Not Saved!", "Email is empty")
                    vemail.config(highlightthickness=0)                        
            else:
                vnum.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
                messagebox.showerror("Not Saved!", "Contact Number is empty")
                vnum.config(highlightthickness=0)
        else:
            vadd.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
            messagebox.showerror("Not Saved!", "Address is empty")
            vadd.config(highlightthickness=0)                
    else:
        vname.config(highlightbackground="red", highlightthickness=1, highlightcolor= "red")
        messagebox.showerror("Not Saved!", "Name is empty")
        vname.config(highlightthickness=0)

def addProd():
    global idx, idxTable1, idxTable2
    global CustProdID
    global checkSame
    enter = False
    num = 0
    if type(idx) == int:
        if type(idxTable1) == int:
            if type(idxTable2) == int:
                initialArr = getProd()
                # getProd()
                if initialArr:
                    for x in checkSame[idx]:
                        if x == initialArr[:2]:
                            enter = True
                            break
                        num += 1

                    if enter:
                        storeCustProd[idx][num][4] = str(int(storeCustProd[idx][num][4])+1)
                    else:
                        checkSame[idx].append([initialArr[0], initialArr[1]])
                        CustProdID[idx] += 1
                        print (initialArr[0])
                        print (initialArr[1])
                        print (initialArr[2])
                        storeCustProd[idx].append([CustProdInvoice[idx], CustProdID[idx], initialArr[0], initialArr[1], "1", "{:.2f}".format(float(initialArr[2])), "/".join(currDate)])
                        
                    createTable2()
                    idx = None
                    idxTable1 = None
                    idxTable2 = None
                    ProdCustwritecsv()
            else:
                messagebox.showinfo("Message", "Please select a row from Stock Table")
        else:
            messagebox.showinfo("Message", "Please select a row from Products Table")
    else:
        messagebox.showinfo("Message", "Please select a row from Costumers Table")    

def printInvoice():
    global idx
    custYaxis = 453 - 5.9*len(str(idx+1))*1.15
    invoiceYaxis = 468 - 5.9*len(str(CustProdInvoice[idx]))*1.15
    if type(idx) == int:
        c = canvas.Canvas("receipt.pdf")
        c.drawString(400, 800, "Date Issued: " + "/".join(currDate))
        c.drawString(invoiceYaxis, 780, "Invoice No. " + str(CustProdInvoice[idx]))
        c.drawString(custYaxis, 760, "Customer No. " + str(idx+1))
        c.setFont("Helvetica-Bold", 30)
        c.drawString(235, 720, "INVOICE")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(235, 705, "Viver's Computer Store")
        c.setFont("Helvetica", 11)
        c.drawString(260, 690, "Magallanes St.")
        c.drawString(270, 675, "Davao City")
        c.drawString(237, 660, "Contact#: 09273173194")
        c.setLineWidth(0.3)
        c.line(70, 645, 510, 645)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(70, 630, "Billed To")
        c.setFont("Helvetica", 11)
        c.drawString(70, 600, store[idx][1])
        c.drawString(70, 585, store[idx][2])
        c.drawString(70, 570, store[idx][3])
        c.setFillColorRGB(0.75,0.75,0.75)
        c.rect(70, 530, 440, 20, 0, 1)
        c.setFillColor("black")
        c.drawString(100, 537, "Product Description")
        c.drawString(300, 537, "Quantity")
        c.drawString(450, 537, "Unit Price")
        tableYaxis = 505
        subtotal = 0
        for x in storeCustProd[idx]:
            ProdDesXaxis = 145 - 2.3*len(f"({x[2]}) {x[3]}")
            quantXaxis = 315 - 2.3*len(str(x[4]))
            unitXaxis = 470 - 2.3*len(str(x[5]))
            c.drawString(ProdDesXaxis, tableYaxis, f"({x[2]}) {x[3]}")
            c.drawString(quantXaxis, tableYaxis, str(x[4]))
            c.drawString(unitXaxis, tableYaxis, str(x[5]))
            tableYaxis -= 25
            subtotal += (int(x[4]) * float(x[5]))
        
        tax = subtotal * 0.12
        Total = tax + subtotal
        c.line(70, tableYaxis, 510, tableYaxis)
        subtotalXaxis = 470 - 2.3*len("%.2f"%subtotal)
        taxXaxis = 470 - 2.3*len("%.2f"%tax)
        TotalXaxis = 470 - 2.3*len("%.2f"%Total)

        c.setFont("Helvetica-Bold", 11)
        c.drawString(370, tableYaxis-15, "Subtotal")
        c.drawString(370, tableYaxis-40, "Tax 12%")
        c.drawString(360, tableYaxis-65, "Total Cost")

        c.setFont("Helvetica", 11)
        c.drawString(subtotalXaxis, tableYaxis-15, "%.2f"%subtotal)
        c.drawString(taxXaxis, tableYaxis-40, "%.2f"%tax)
        c.drawString(TotalXaxis, tableYaxis-65, "%.2f"%Total)

        




        c.save()
        os.startfile("receipt.pdf")


        idx = None

    else:
       messagebox.showinfo("Message", "Please select a row from Costumers Table")  

def getProd():
    laborCost = ProdLabor.get()
    OverheadCost = ProdOverhead.get()
    DesiredProfit = ProdProfit.get()
    tempArr = []
    if len(laborCost) > 0:
        if len(OverheadCost) > 0:
            if len(DesiredProfit) > 0:
                if prodStore1[idxTable1][4] == "0":
                    messagebox.showinfo("Error!", "There are no stocks left for this product")
                tempArr.append(prodStore2[idxTable1][idxTable2][1])
                tempArr.append(prodStore2[idxTable1][idxTable2][2])
                PerItem = int(prodStore2[idxTable1][idxTable2][5]) / (int(prodStore2[idxTable1][idxTable2][4]) + int(prodStore2[idxTable1][idxTable2][7]))
                tempArr.append(str(PerItem + int(ProdLabor.get()) + int(ProdOverhead.get()) + int(ProdProfit.get())))
                prodStore2[idxTable1][idxTable2][4] = str(int(prodStore2[idxTable1][idxTable2][4])-1)
                prodStore1[idxTable1][4] = str(int(prodStore1[idxTable1][4])-1)
                prodStore2[idxTable1][idxTable2][7] = str(int(prodStore2[idxTable1][idxTable2][7])+1)
                prodStore1[idxTable1][5] = str(int(prodStore1[idxTable1][5])+1)
                ProdcreateTable1()
                ProdcreateTable2()
                Prodwritecsv()
                Stockwritecsv()
            else:
                messagebox.showerror("Not Saved!", "Desired Profit is empty")
        else:
            messagebox.showerror("Not Saved!", "Overhead Cost is empty")
    else:
        messagebox.showerror("Not Saved!", "Labor Cost is empty")
    return tempArr

def putSpaceRow(start, num, win):
    for x in range(num):
        space = Label(win)
        space.grid(row = start+x)

def putSpaceCol(start, num, win, rowVar):               
    for x in range(num):
        space = Label(win, width = 5, bg = "white")
        space.grid(column = start + x, row = rowVar)


def createTable():
    posy = 2
    sizes = [94, 94, 124, 94, 94, 94, 94]
    for a in range(len(store)):
        for b in range(len(store[0])):
            rowGrid = Entry(frame, bd = 0, highlightbackground="black", highlightthickness=1, disabledbackground = "white", disabledforeground = "black")
            rowGrid.insert(END, store[a][b])
            rowGrid.configure(state = "disabled")
            rowGrid._values = a
            rowGrid.place(x = sum(sizes[:b]), y = posy, width = sizes[b], height = 25)
            rowGrid.bind("<Button-1>", selectRow)
        posy += 25

def createTable2():
    for w in frame2.winfo_children():
        w.destroy() 
    posy = 0
    sizes = [94, 94, 124, 94, 94, 94, 94]
    for a in range(len(storeCustProd[idx])):
        for b in range(len(storeCustProd[idx][0])):
            rowGrid = Entry(frame2, bd = 0, highlightbackground="black", highlightthickness=1, disabledbackground = "white", disabledforeground = "black")
            rowGrid.insert(END, storeCustProd[idx][a][b])
            rowGrid.configure(state = "disabled")
            rowGrid._values = a
            rowGrid.place(x = sum(sizes[:b]), y = posy, width = sizes[b], height = 25)
            rowGrid.bind("<Button-1>", selectRow2)
        posy += 25


def ProdCreateRow():
    pass


def selectRow(event):
    global idx
    idx = event.widget._values
    event.widget.configure(disabledbackground = "yellow")
    window.after(500, lambda: event.widget.configure(disabledbackground = "white"))
    name.set(store[idx][1])
    add.set(store[idx][2])
    num.set(store[idx][3])
    email.set(store[idx][4])
    bday.set(store[idx][5])
    if store[idx][6] == " Male":
        genderValue.current(0)
    else:
        genderValue.current(1)
    idNum.configure(text = str(store[idx][0]))
    createTable2()


def selectRow2(event):
    pass

def Custwritecsv():
    saveTxt = ""
    for x in store:
        for y in x:
            saveTxt += str(y) + "~"
        saveTxt += "-"

    with open('customers.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([saveTxt])

def Custreadcsv():
    global checkSame, storeCustProd, CustProdID, store
    try:
        with open('customers.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row):
                    dash = row[0].split("-")
                    for x in range(len(dash)-1):
                        checkSame.append([])
                        storeCustProd.append([])
                        CustProdID.append(0)
                        if CustProdInvoice:
                            CustProdInvoice.append(CustProdInvoice[-1]+1)
                        else:
                            CustProdInvoice.append(4090)
                        if dash[x]:
                            store.append(dash[x].split("~")[:-1])
        createTable()

    except:
        pass

def ProdCustwritecsv():
    saveTxt = ""
    for x in storeCustProd:
        for y in x:
            for z in y:
                saveTxt += str(z) + "~"
            saveTxt += "-"
        saveTxt += "_"

    with open('customersProduct.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([saveTxt])

def ProdCustreadcsv():
    global storeCustProd
    try:
        with open('customersProduct.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row):
                    underscore = row[0].split("_")
                    for x in range(len(underscore)):
                        if underscore[x]:
                            storeCustProd.append([])
                            dash = underscore[x].split("-")
                            for y in range(len(dash)):
                                if dash[y]:
                                    storeCustProd[x].append(dash[y].split("~")[:-1])
        createTable2()
    except:
        pass

def Deletewritecsv():
    saveTxt = ""
    for x in deleted:
        saveTxt += x + "~"

    with open('deleted.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([saveTxt])

def Deletereadcsv():
    global deleted
    try:
        with open('deleted.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row):
                    deleted = row[0].split("~")
        # print (deleted)            
        deleted = [x for x in deleted if x]
        # print ("exit")
        # print (deleted)       
    except:
        pass



def products():
    global prodFrame1, prodFrame2
    global ProdidNum, ProdType, ProdDes, ProdSupp, ProdQuant, ProdAddQuant, ProdTot, ProdDate, ProdLabor, ProdOverhead, ProdProfit
    global productWindow
    productWindow = Tk()
    productWindow.title("Products")
    productWindow.geometry("1300x800")
    productWindow.configure(bg = "white")

    prodFrame1 = Frame(productWindow)
    prodFrame1.place(x = 383, y = 72, width = 684, height = 250)

    prodFrame2 = Frame(productWindow)
    prodFrame2.place(x = 383, y = 355, width = 872, height = 350)


    ################################ PRODUCTS LABEL ################################
    label = Label(productWindow, text = "New Product Stock-In", width = 20, height = 1, foreground = "black", bg ="white", pady = 10, font = ("Courier",10))
    label.grid(column = 2, row = 1)

    labels = ["Product ID", "Product Type", "Product Description","Supplier","Quantity","Total Cost", "Date Received"]
    for x in range(len(labels)):
        label = Label(productWindow, text = labels[x], width = 20, height = 1, foreground = "black", bg ="white", pady = 7)
        label.grid(column = 1, row = 2+x)

    ProdidNum = Label(productWindow, text = "1", width = 5, height = 1, foreground = "black", bg ="white", font = (10))
    ProdidNum.grid(column = 2, row = 2)

    ProdPlusSign = Label(productWindow, text = "+", width = 5, height = 1, foreground = "black", bg ="white", font = (8))
    ProdPlusSign.grid(column = 2, row = 6, sticky="NSEW")


    label = Label(productWindow, text = "Labor Cost", width = 5, height = 1, foreground = "black", bg ="white")
    label.grid(column = 1, row = 15, sticky="NSEW")
    label = Label(productWindow, text = "Overhead Cost", width = 5, height = 1, foreground = "black", bg ="white")
    label.grid(column = 1, row = 16, sticky="NSEW")
    label = Label(productWindow, text = "Desired Profit", width = 5, height = 1, foreground = "black", bg ="white")
    label.grid(column = 1, row = 17, sticky="NSEW")

    ################################ PRODUCTS INPUTS ###############################
    ProdType, ProdDes, ProdSupp, ProdQuant, ProdAddQuant, ProdTot, ProdDate, ProdLabor, ProdOverhead, ProdProfit =  StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow)
    Prodinputs = [ProdType, ProdDes, ProdSupp, ProdQuant, ProdTot, ProdDate]
    key = [None, None, None, None, None, None]
    width = [30, 30, 30, 12, 30, 30]
    ProdState = ["normal", "normal", "normal", "normal", "normal", "disabled"]

    for x in range(len(Prodinputs)):
        var = Entry(productWindow, textvariable=Prodinputs[x], width = width[x], bd = 2, state = ProdState[x])
        var.grid(column =2, row = 3+x, sticky = "W")
        if key[x]:
            var.bind("<KeyRelease>", key[x])
    
    ProdDate.set("/".join(currDate))    
    var = Entry(productWindow, textvariable= ProdAddQuant, width = 12, bd = 2)
    var.grid(column = 2, row = 6, sticky = "E")
    

    putSpaceRow(13, 2, productWindow)
    var = Entry(productWindow, textvariable= ProdLabor, width = 23, bd = 2)
    var.grid(column = 2, row = 15)
    var.bind("<KeyRelease>", ProdLaborKey)

    var = Entry(productWindow, textvariable= ProdOverhead, width = 23, bd = 2)
    var.grid(column = 2, row = 16)
    var.bind("<KeyRelease>", ProdOverheadKey)

    var = Entry(productWindow, textvariable= ProdProfit, width = 23, bd = 2)
    var.grid(column = 2, row = 17)
    var.bind("<KeyRelease>", ProdProfitKey)
    
    ################################ PRODUCTS TABLE 1 ###############################
    ProdidTable, ProdTypeTable, ProdDesTable, ProdSuppTable, ProdQuantTable, ProdOrdersTable = StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow)
    ProdinputsTable = [ProdidTable, ProdTypeTable, ProdDesTable, ProdSuppTable, ProdQuantTable, ProdOrdersTable]
    ProdlabelTable = ["ID", "Product Type", "Product Desc.", "Supplier", "Total Quantity", "Orders"]
    ProdwidthTable = [10, 20, 20, 20, 20, 20]
    putSpaceCol(3, 1, productWindow, 2)
    for x in range(len(ProdinputsTable)):
        var = Entry(productWindow, textvariable=ProdinputsTable[x], width = ProdwidthTable[x], bd =0, highlightbackground="black", highlightthickness=1, state = "disabled", disabledbackground = "light blue", disabledforeground = "black")
        var.grid(column =4+x, row = 2, sticky = "NSEW")
        ProdinputsTable[x].set(ProdlabelTable[x])

    putSpaceRow(4, 8, productWindow)

    ################################ PRODUCTS TABLE 2 ###############################
    ProdidTable2, ProdTypeTable2, ProdDesTable2, ProdSuppTable2, ProdQuantTable2, ProdCostTable2, ProdDateTable2, ProdOrdersTable2 = StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow), StringVar(productWindow)
    ProdinputsTable2 = [ProdidTable2, ProdTypeTable2, ProdDesTable2, ProdSuppTable2, ProdQuantTable2, ProdCostTable2, ProdDateTable2, ProdOrdersTable2]
    ProdlabelTable2 = ["ID", "Product Type", "Product Desc.", "Supplier", "Quantity", "Cost", "Date Received", "Orders"]
    ProdwidthTable2 = [10, 20, 20, 20, 20, 20, 15, 15, 15]
    for x in range(len(ProdinputsTable2)):
        var = Entry(productWindow, textvariable=ProdinputsTable2[x], width = ProdwidthTable2[x], bd =0, highlightbackground="black", highlightthickness=1, disabledbackground = "light blue", disabledforeground = "black")
        var.grid(column =4+x, row = 12, sticky = "NSEW")
        var.insert(0, ProdlabelTable2[x])
        var.configure(state = "disabled")

    Prodreadcsv()
    Stockreadcsv()
    Costreadcsv()


    ################################ PRODUCTS BUTTONS ##############################
    putSpaceRow(11, 2, productWindow)
    Prodsavebtn = Button(productWindow,text = "New Product", activeforeground = "green", width = 20, command = NewProd)
    Prodsavebtn.grid(column = 1, row = 13)
    Prodeditbtn = Button(productWindow,text = "Stock IN", activeforeground = "green", width = 20, command = NewStock)
    Prodeditbtn.grid(column = 2, row = 13)

def ProdLaborKey(q):
    Costwritecsv()

def ProdOverheadKey(q):
    Costwritecsv()

def ProdProfitKey(q):
    Costwritecsv()

def NewProd():
    global prodStore1, prodStore2
    # global tableID
    if ProdType.get() and ProdDes.get() and ProdSupp.get() and ProdQuant.get():
        tableID = len(prodStore1)+1
        messagebox.showinfo("Saved", "The Product was saved", master= productWindow)
        prodStore1.append([str(tableID), ProdType.get(), ProdDes.get(), ProdSupp.get(), (ProdQuant.get()), 0])
        ProdcreateTable1()
        ProdidNum.configure(text = str(tableID+1))
        prodStore2.append([[str(tableID), ProdType.get(), ProdDes.get(), ProdSupp.get(), ProdQuant.get(), ProdTot.get(), ProdDate.get(), 0]])
        # tableID += 1
        Prodwritecsv()
        Stockwritecsv()
    else:
        messagebox.showerror("Product not Saved!", "There are missing inputs", master= productWindow) 

def NewStock():
    global prodStore2
    global idxTable1
    if type(idxTable1) == int:
        if ProdType.get() and ProdDes.get() and ProdSupp.get() and ProdAddQuant.get() and ProdTot.get():
            messagebox.showinfo("Saved", "The Stock was saved", master= productWindow)
            prodStore2[idxTable1].append([str(idxTable1+1), ProdType.get(), ProdDes.get(), ProdSupp.get(), ProdAddQuant.get(), ProdTot.get(), ProdDate.get(), 0])
            ProdcreateTable2()
            prodStore1[idxTable1][4] = str(int(prodStore1[idxTable1][4]) + int(ProdAddQuant.get()))
            ProdcreateTable1()
            Prodwritecsv()
            Stockwritecsv()
        else:
            messagebox.showerror("Stock not Saved!", "There are missing inputs", master= productWindow)  
    else:
        messagebox.showerror("Error!", "Please select a row", master= productWindow)
    idxTable1 = None

def ProdcreateTable1():
    for w in prodFrame1.winfo_children():
        w.destroy()    
    posy = 1
    sizes = [64, 124, 124, 124, 124, 124, 124]
    for a in range(len(prodStore1)):
        for b in range(len(prodStore1[0])):
            rowGrid = Entry(prodFrame1, bd = 0, highlightbackground="black", highlightthickness=1, disabledbackground = "white", disabledforeground = "black")
            rowGrid.insert(0, prodStore1[a][b])
            rowGrid.configure(state = "disabled")
            rowGrid._values = a
            rowGrid.place(x = sum(sizes[:b]), y = posy, width = sizes[b], height = 25)
            rowGrid.bind("<Button-1>", selectRowTable1)
        posy += 25

def ProdcreateTable2():
    for w in prodFrame2.winfo_children():
        w.destroy()  
    posy = 0
    sizes = [64, 124, 124, 124, 124, 124, 94, 94]
    for a in range(len(prodStore2[idxTable1])):
        for b in range(len(prodStore2[idxTable1][0])):
            rowGrid = Entry(prodFrame2, bd = 0, highlightbackground="black", highlightthickness=1, disabledbackground = "white", disabledforeground = "black")
            rowGrid.insert(END, prodStore2[idxTable1][a][b])
            rowGrid.configure(state = "disabled")
            rowGrid._values = a
            rowGrid.place(x = sum(sizes[:b]), y = posy, width = sizes[b], height = 25)
            rowGrid.bind("<Button-1>", selectRowTable2)
        posy += 25

def selectRowTable1(event):
    global idxTable1
    idxTable1 = event.widget._values
    event.widget.configure(disabledbackground = "yellow")
    window.after(500, lambda: event.widget.configure(disabledbackground = "white"))
    ProdidNum.configure(text = str(idxTable1+1))
    ProdType.set(prodStore1[idxTable1][1])
    ProdDes.set(prodStore1[idxTable1][2])
    ProdSupp.set(prodStore1[idxTable1][3])
    ProdQuant.set(prodStore1[idxTable1][4])
    ProdcreateTable2()


def selectRowTable2(event):
    global idxTable2
    idxTable2 = event.widget._values
    event.widget.configure(disabledbackground = "yellow")
    window.after(500, lambda: event.widget.configure(disabledbackground = "white"))

def Prodwritecsv():
    saveTxt = ""
    for x in prodStore1:
        for y in x:
            saveTxt += str(y) + "~"
        saveTxt += "-"

    with open('products.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([saveTxt])


def Prodreadcsv():
    global prodStore1
    try:
        with open('products.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row):
                    dash = row[0].split("-")
                    for x in range(len(dash)):
                        # prodStore2.append([])
                        if dash[x]:
                            prodStore1.append(dash[x].split("~")[:-1])
        ProdcreateTable1()

    except:
        pass

def Stockwritecsv():
    saveTxt = ""
    for x in prodStore2:
        for y in x:
            for z in y:
                saveTxt += str(z) + "~"
            saveTxt += "-"
        saveTxt += "_"

    with open('stocks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([saveTxt])


def Stockreadcsv():
    global prodStore2
    try:
        with open('stocks.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row):
                    underscore = row[0].split("_")
                    for x in range(len(underscore)):
                        if underscore[x]:
                            prodStore2.append([])
                            dash = underscore[x].split("-")
                            for y in range(len(dash)):
                                if dash[y]:
                                    prodStore2[x].append(dash[y].split("~")[:-1])
        ProdcreateTable2()
    except:
        pass

def Costwritecsv():
    saveTxt = ""
    saveTxt += ProdLabor.get() + "~"
    saveTxt += ProdOverhead.get() + "~"
    saveTxt += ProdProfit.get() + "~"

    with open('cost.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([saveTxt])

def Costreadcsv():
    try:
        with open('cost.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row):
                    splitted = row[0].split("~")
                    ProdLabor.set(splitted[0])
                    ProdOverhead.set(splitted[1])
                    ProdProfit.set(splitted[2])
    except:
        pass
    

################################################## MENUBAR ##################################################



menubar = Menu(window)
filemenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "File", menu = filemenu)
filemenu.add_command(label = "Products", command = products)
filemenu.add_command(label = "Orders")
filemenu.add_separator()
filemenu.add_command(label = "Close", command = window.quit)

window.config(menu = menubar)


################################################## LABELS ##################################################



label = Label(window, text = "Costumer Registration System", width = 30, height = 1, foreground = "black", bg ="white", pady = 7, font = ("Courier",10))
label.grid(column = 2, row = 1)

labels = ["Costumer ID", "Costumer Name", "Costumer Address","Costumer Contact#","Costumer Email","Costumer Birthday", "Costumer Gender"]
for x in range(7):
    label = Label(window, text = labels[x], width = 20, height = 1, foreground = "black", bg ="white", pady = 7)
    label.grid(column = 1, row = 2+x)


idNum = Label(window, text = "1", width = 5, height = 1, foreground = "black", bg ="white", font = (10))
idNum.grid(column = 2, row = 2)

changeName = Label(window, text = "Lastname, Firstname", width = 20, height = 1, foreground = "black", bg ="white")
changeName.grid(column = 3, row = 3)

changeEmail = Label(window, text = "[a-z]@[a-z].com", width = 20, height = 1, foreground = "black", bg ="white")
changeEmail.grid(column = 3, row = 6)

changeBday = Label(window, text = "MM/DD/YYYY", width = 20, height = 1, foreground = "black", bg ="white")
changeBday.grid(column = 3, row = 7)

gender = StringVar() 
genderValue = ttk.Combobox(window, width = 27, textvariable = gender, state = "readonly") 
genderValue['values'] = (' Male', ' Female') 
genderValue.grid(column = 2, row = 8) 
genderValue.current(0) 



################################################## INPUTS #####################################################


name, add, num, email, bday = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
vname, vadd, vnum, vemail, vbday = None, None, None, None, None
ident = ["vname", "vadd", "vnum", "vemail", "vbday"]
inputs = [name, add, num, email, bday]
key = [None, None, None, emailKey, bdayKey]

for x in range(5):
    globals()[ident[x]] = Entry(window, textvariable=inputs[x], width = 30, bd = 2)
    globals()[ident[x]].grid(column =2, row = 3+x)
    if key[x]:
        globals()[ident[x]].bind("<KeyRelease>", key[x])

putSpaceCol(4, 1, window, 2)

################################################# TABLE 1 ####################################################

idTable, nameTable, addTable, numTable, emailTable, bdayTable, genderTable = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
inputsTable = [idTable, nameTable, addTable, numTable, emailTable, bdayTable, genderTable]
labelTable = ["ID", "Name", "Address", "Contact#", "Email", "Birthday", "Gender"]
widthTable = [15, 15, 20, 15, 15, 15, 15]

for x in range(7):
    var = Entry(window, textvariable=inputsTable[x], width = widthTable[x], bd =0, highlightbackground="black", highlightthickness=1, state = "disabled", disabledbackground = "light blue", disabledforeground = "black")
    var.grid(column =5+x, row = 2, sticky = "NSEW")
    inputsTable[x].set(labelTable[x])


putSpaceRow(2, 13, window)
################################################# TABLE 2 ####################################################
invoiceTable2, idTable2, typeTable2, descTable2, quantTable2, unitTable, dateTable2 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
inputsTable2 = [invoiceTable2, idTable2, typeTable2, descTable2, quantTable2, unitTable, dateTable2]
labelTable2 = ["Invoice No.", "Prod ID", "Prod Type", "Prod Desc.", "Quantity", "Unit Price", "Date"]
widthTable2 = [15, 15, 20, 15, 15, 15, 15]


for x in range(7):
    var = Entry(window, textvariable=inputsTable2[x], width = widthTable2[x], bd =0, highlightbackground="black", highlightthickness=1, state = "disabled", disabledbackground = "light blue", disabledforeground = "black")
    var.grid(column =5+x, row = 15, sticky = "NSEW")
    inputsTable2[x].set(labelTable2[x])

################################################## BUTTON ####################################################

putSpaceRow(9, 2, window)
savebtn = Button(text = "Save", command = save, activeforeground = "green", width = 20)
savebtn.grid(column = 1, row = 11)
delbtn = Button(text = "Delete", command = delete, activeforeground = "green",width = 20)
delbtn.grid(column = 2, row = 11)
updbtn = Button(text = "Update", command = update, activeforeground = "green", width = 20)
updbtn.grid(column = 3, row = 11)
addbtn = Button(text = "Add Product", activeforeground = "green", width = 20, command = addProd)
addbtn.grid(column = 3, row = 17)
printbtn = Button(text = "Print Invoice", activeforeground = "green", width = 20, command = printInvoice)
printbtn.grid(column = 2, row = 17)

########################################### AUTOMATIC RUN FUNCTIONS ###########################################
Custreadcsv()
ProdCustreadcsv()
Deletereadcsv()

window.mainloop()




