#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from datetime import datetime, date, time, timedelta
import tkinter as tk
import sqlite3, string, math, sys, re, calendar

conn = sqlite3.connect('ptardsapi.db')

root = tk.Tk()
root.geometry("1050x650+0+0")
root.title("Programa aplicado a las zanjas de oxidación")

signo = tk.PhotoImage(file ="int.png")
uno = tk.PhotoImage(file ="numerouno.png")
uno = tk.PhotoImage(file ="numerouno.png")
dos = tk.PhotoImage(file ="numerodos.png")
tres = tk.PhotoImage(file ="numerotres.png")
cuatro = tk.PhotoImage(file ="numerocuatro.png")
Carcir = PhotoImage(file="carca.png")
CarRecta = PhotoImage(file="carcarec.png")
Carcir2 = PhotoImage(file="carcacrc.png")
CarRecta2 = PhotoImage(file="carcarc.png")
Zanjorb = PhotoImage(file="orbal.png")
Zanjislas = PhotoImage(file="isla.png")
Zanjrecta = PhotoImage(file="rcta.png")
Zanjherra = PhotoImage(file="herradura.png")
erasSecado = PhotoImage(file="eras.png")
Croquis = PhotoImage(file="imagenes.png")

notebook = ttk.Notebook(root)
notebook.pack(fill= 'both', expand = 'yes')

pesambient = ttk.Frame(notebook)
notebook.add(pesambient, text = "Datos del lugar", image = uno, compound=tk.LEFT)
pesPre = ttk.Frame(notebook)
notebook.add(pesPre, text = "Pretratamiento", state="disabled", image = dos, compound=tk.LEFT)
pesVert = ttk.Frame(notebook)
notebook.add(pesVert, text = "Vertedor y zanjas", state="disabled", image = tres, compound=tk.LEFT)
pesClora = ttk.Frame(notebook)
notebook.add(pesClora, text = "Sedimentador, tratamiento de lodos y tanque de cloración", state="disabled", image = cuatro, compound=tk.LEFT)

def pobla():
    messagebox.showinfo(title ="Sugerencia sobre la dotación", message = "La dotación depende de la población:\nPoblaciones grandes (20000 Hab) = 350 L/Hab*día,\npoblaciones medianas (2500 Hab) = 240 L/Hab*día,\npoblaciones chicas (500 Hab)= 180 L/Hab*día.")

def Ajust():
    global poblacion
    poblacion = float(entrPob.get())
    if poblacion >= 0:
        entrHar.set(3.5)
    if poblacion >= 2500:
        Harmon = float(1 +(14 / (4 + (poblacion / 1000) ** 0.5)))
    if poblacion >= 20000:
        Harmon = float(1 +(14 / (4 + (poblacion / 1000) ** 0.5)))
        messagebox.showinfo(title ="Sugerencia al diseñador", message = "Debido al tamaño de la población proyectada\nse sugiere construir el pretratamiento\nantes del cárcamo elegido")
        Harmon = round(Harmon,2)
        entrHar.set(Harmon)

def resulcau():
    root3 = Toplevel(root)
    root3.geometry("480x340+0+0")
    root3.title("Resultado de caudales")

    global Qproml
    global Qminl
    global Qmaxl
    global Qmaxextl

    n2 = float(entrDot.get())
    n3 = float(entrHar.get())
    n4 = float(entrApor.get())
#caudales en litros/segundos
    Qproml = float((poblacion * n2 * n4) / 86400)
    Qminl = float(Qproml / 2)
    Qmaxl = float(Qproml * n3)
    Qmaxextl = float(Qmaxl * 1.43)
#caudales en metros cúbicos/segundos
    Qpromm3 = float(Qproml / 1000)
    Qminm3 = float(Qminl / 1000)
    Qmaxm3 = float(Qmaxl / 1000)
    Qmaxextm3 = float(Qmaxextl / 1000)
#caudales en metros cúbicos/dias
    Qprommd = float(Qpromm3 * 86400)
    Qminmd = float(Qminm3 * 86400)
    Qmaxmd = float(Qmaxm3 * 86400)
    Qmaxextmd = float(Qmaxextm3 * 86400)

    ccau = conn.cursor()

    pbdb = """
    CREATE TABLE IF NOT EXISTS poblacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Qproml FLOAT NOT NULL,
    Qminl FLOAT NOT NULL,
    Qmaxl FLOAT NOT NULL,
    Qmaxextl FLOAT NOT NULL,
    Qpromm3 FLOAT NOT NULL,
    Qminm3 FLOAT NOT NULL,
    Qmaxm3 FLOAT NOT NULL,
    Qmaxextm3 FLOAT NOT NULL,
    Qprommd FLOAT NOT NULL,
    Qminmd FLOAT NOT NULL,
    Qmaxmd FLOAT NOT NULL,
    Qmaxextmd FLOAT NOT NULL,
    poblacion INTEGER NOT NULL)"""

    ccau.execute(pbdb)

    argcau = (poblacion, Qproml, Qminl, Qmaxl, Qmaxextl, Qpromm3, Qminm3, Qmaxm3, Qmaxextm3, Qprommd, Qminmd, Qmaxmd, Qmaxextmd)

    cauconec = """
    INSERT INTO poblacion (poblacion, Qproml, Qminl, Qmaxl, Qmaxextl, Qpromm3, Qminm3, Qmaxm3, Qmaxextm3, Qprommd, Qminmd, Qmaxmd, Qmaxextmd)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""

    ccau.execute(cauconec, argcau)

    conn.commit()

    ccau.close()

    Qpromlre = round(Qproml,2)
    Qminlre = round(Qminl,2)
    Qmaxlre = round(Qmaxl,2)
    Qmaxextlre = round(Qmaxextl,2)

    framecaut = LabelFrame(root3, text = "Resultados de caudales", width = 440, height = 305, bd = 2, relief = RIDGE)
    framecaut.place(x = 20, y = 15)

    etiqueta6 = Label(framecaut,text = "Caudal promedio en L/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
    etiqueta7 = Label(framecaut, text = "Caudal mínimo en L/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
    etiqueta8 = Label(framecaut, text = "Caudal máximo en L/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 130)
    etiqueta9 = Label(framecaut, text = "Caudal máximo extraordinario en L/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 200)

    global entrQprom
    global entrQmin
    global entrQmax
    global entrQmaxext

    entrQprom = DoubleVar()
    entrQprom.set(Qpromlre)
    entrQmin = DoubleVar()
    entrQmin.set(Qminlre)
    entrQmax = DoubleVar()
    entrQmax.set(Qmaxlre)
    entrQmaxext = DoubleVar()
    entrQmaxext.set(Qmaxextlre)

    nombrearch = "Pazox"
    file = str(nombrearch + ".txt")
    archivo = open(file,"w")
    Qpromedio = str(entrQprom.get())
    Qminimo = str(entrQmin.get())
    Qmáximo = str(entrQmax.get())
    Qmáximoextraordinario = str(entrQmaxext.get())
    txto = ("\n\nLos caudales en litros por segundo resultantes fueron:\nCaudal promedio:\t\t"+Qpromedio+"\nCaudal mínimo:\t\t\t"+Qminimo+"\nCaudal máximo:\t\t\t"+Qmáximo+"\nCaudal máximo extraordinario:\t"+Qmáximoextraordinario)
    archivo.write(txto)
    archivo.close()

    txtQprom = Entry(framecaut, textvariable = entrQprom, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
    txtQmin = Entry(framecaut, textvariable = entrQmin, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
    txtQmax = Entry(framecaut, textvariable = entrQmax, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 20, y= 155)
    txtQmaxext = Entry(framecaut, textvariable = entrQmaxext, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 20, y = 225)

def continuar():
    notebook.add(pesPre, text = "Pretratamiento", state="normal")

    respuesta = askquestion(title = "Guardar y continuar proceso", message= "¿Desea crear un archivo y guardar antes de continuar?")
    if respuesta == "yes":
        Archivos = asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        if Archivos!='':
            file = str(Archivos + ".txt")
            archivo = open(file,"w")
            Qpromedio = str(entrQprom.get())
            Qminimo = str(entrQmin.get())
            Qmáximo = str(entrQmax.get())
            Qmáximoextraordinario = str(entrQmaxext.get())
            txto = ("\n\nLos caudales en litros por segundo resultantes fueron:\nCaudal promedio:\t\t"+Qpromedio+"\nCaudal mínimo:\t\t\t"+Qminimo+"\nCaudal máximo:\t\t\t"+Qmáximo+"\nCaudal máximo extraordinario:\t"+Qmáximoextraordinario)
            archivo.write(txto)
            archivo.close()


    def croquiscarca():
        if poblacion < 20000 and carcamo.get() == 1:
            rootcc = Toplevel(root)
            rootcc.geometry("808x298+0+0")
            rootcc.title("Esquema del cárcamo circular antes del pretratamiento")

            lblcarcircu = Label(rootcc, image = Carcir).place(x = 0, y = 0)
        elif poblacion < 20000 and carcamo.get() == 2:
            rootcc = Toplevel(root)
            rootcc.geometry("808x298+0+0")
            rootcc.title("Esquema del cárcamo rectangular antes del pretratamiento")

            lblcarcircu = Label(rootcc, image = CarRecta).place(x = 0, y = 0)
        elif  poblacion >= 20000 and carcamo.get() == 1:
            rootcc2 = Toplevel(root)
            rootcc2.geometry("808x298+0+0")
            rootcc2.title("Esquema del cárcamo circular después del pretratamiento")

            lblcarcircu2 = Label(rootcc2, image = Carcir2).place(x = 0, y = 0)
        elif poblacion >= 20000 and carcamo.get() == 2:
            rootcc = Toplevel(root)
            rootcc.geometry("808x298+0+0")
            rootcc.title("Esquema del cárcamo rectangular antes del pretratamiento")

            lblcarcircu = Label(rootcc, image = CarRecta2).place(x = 0, y = 0)

    def framecar(presbombs, altimp):

        def rescar():
            root4 = Toplevel(root)
            root4.geometry("990x450+0+0")
            root4.title("Resultado de cárcamo")

            flagCarcamo= 1

            Qmaxm3 = float(Qmaxl / 1000)
            Qminm3 = float(Qminl / 1000)
            Qpromm3 = float(Qproml / 1000)

            if carcamo.get() == 1:

                ntf = int(valortf.get())
                nH = int(entHimp.get())

                Tf = ntf * 60
                VcCar = float(Tf / (1 / Qmaxm3) + (1 / (Qmaxm3 - Qminm3)))
                AsCar = float(VcCar / nH)
                import math
                RcCar = float(math.sqrt(AsCar / 3.1416))
                DcCar = float(RcCar * 2)
                TllQmaxCar = float(VcCar / Qmaxm3)
                TllQmaxCar = float(TllQmaxCar / 60)
                TllQminCar = float(VcCar / Qminm3)
                TllQminCar = float(TllQminCar / 60)
                TvaCar = float(VcCar / (Qmaxm3 - Qminm3))
                TvaCar = float(TvaCar / 60)
                CopCar = float(TllQmaxCar + TvaCar)
                CopehCar = float(60 / (CopCar))

                VcCar = round(VcCar,2)
                AsCar = round(AsCar,2)
                RcCar = round(RcCar,2)
                DcCar = round(DcCar,2)
                TllQmaxCar = round(TllQmaxCar,2)
                TllQminCar = round(TllQminCar,2)
                TvaCar = round(TvaCar,2)
                CopCar = round(CopCar,2)
                CopehCar = round(CopehCar,2)

                ccar= conn.cursor()

                ccdb = """
                CREATE TABLE IF NOT EXISTS carcamo (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                VcCar FLOAT NOT NULL,
                AsCar FLOAT NOT NULL,
                RcCar FLOAT NOT NULL,
                DcCar  FLOAT NOT NULL,
                TllQmaxCar  FLOAT NOT NULL,
                TllQminCar  FLOAT NOT NULL,
                TvaCar  FLOAT NOT NULL,
                CopCar  FLOAT NOT NULL,
                CopehCar  FLOAT NOT NULL)"""

                ccar.execute(ccdb)

                argcar = (VcCar, AsCar, RcCar, DcCar, TllQmaxCar, TllQminCar, TvaCar, CopCar,CopehCar)

                carconec = """
                INSERT INTO carcamo (VcCar, AsCar, RcCar, DcCar, TllQmaxCar, TllQminCar, TvaCar, CopCar,CopehCar)
                VALUES (?,?,?,?,?,?,?,?,?)"""

                ccar.execute(carconec, argcar)

                conn.commit()

                ccar.close()

                framecart = LabelFrame(root4, text="Dimensiones del cárcamo circular", width = 950, height = 420, bd = 2, relief = RIDGE)
                framecart.place(x = 20, y = 15)

                etiqueta13 = Label(framecart,text = "Volumen en m^3:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta14 = Label(framecart, text = "Área superficial en m^2:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta15 = Label(framecart, text = "Radio en m:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 140)
                etiqueta16 = Label(framecart, text = "Diametro en m:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 210)
                etiqueta16 = Label(framecart, text = "Tiempo de llenado a caudal máximo en minutos:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 280)
                etiqueta16 = Label(framecart, text = "Tiempo de llenado a caudal mínimo en minutos:", font = ("Time new roman", 13), fg = "black").place(x = 530, y = 10)
                etiqueta16 = Label(framecart, text = "Tiempo de vaciado en minutos:", font = ("Time new roman", 13), fg = "black").place(x = 530, y = 70)
                etiqueta16 = Label(framecart, text = "Ciclo de operación en minutos:", font = ("Time new roman", 13), fg = "black").place(x = 530, y = 140)
                etiqueta16 = Label(framecart, text = "Ciclo de operación por hora:", font = ("Time new roman", 13), fg = "black").place(x = 530, y = 210)

                global entrAsCar
                global entrRcCar
                global entrVcCar

                entrVcCar = DoubleVar()
                entrVcCar.set(VcCar)
                entrAsCar = DoubleVar()
                entrAsCar.set(AsCar)
                entrRcCar = DoubleVar()
                entrRcCar.set(RcCar)
                entrDcCar = DoubleVar()
                entrDcCar.set(DcCar)
                entrTllQmaxCar = DoubleVar()
                entrTllQmaxCar.set(TllQmaxCar)
                entrTllQminCar = DoubleVar()
                entrTllQminCar.set(TllQminCar)
                entrTvaCar = DoubleVar()
                entrTvaCar.set(TvaCar)
                entrCopCar = DoubleVar()
                entrCopCar.set(CopCar)
                entrCopehCar = DoubleVar()
                entrCopehCar.set(CopehCar)

                txtVc = Entry(framecart, textvariable = entrVcCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 50, y= 35)
                txtAc = Entry(framecart, textvariable = entrAsCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 50, y = 95)
                txtRc = Entry(framecart, textvariable = entrRcCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 50, y= 165)
                txtDc = Entry(framecart, textvariable = entrDcCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 50, y = 235)
                txtTllQmaxCar = Entry(framecart, textvariable = entrTllQmaxCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 50, y = 305)
                txtTllQminCar = Entry(framecart, textvariable = entrTllQminCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 530, y = 35)
                txtTvaCar = Entry(framecart, textvariable = entrTvaCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 530, y = 95)
                txtCopCar = Entry(framecart, textvariable = entrCopCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 530, y = 165)
                txtCopehCar = Entry(framecart, textvariable = entrCopehCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 530, y = 235)
            elif carcamo.get() == 2:
                
                flagCarcamo=1

                ntf = int(valortf.get())
                nH = int(entHimp.get())

                Tf = ntf * 60
                VcCar = float(Tf / (1 / Qmaxm3) + (1 / (Qmaxm3 - Qminm3)))
                AsCar = float(VcCar / nH)
                BaseCar = float(AsCar / nH)
                AsCar = float(BaseCar / nH)
                TllQmaxCar = float(VcCar / Qmaxm3)
                TllQmaxCar = float(TllQmaxCar / 60)
                TllQminCar = float(VcCar / Qminm3)
                TllQminCar = float(TllQminCar / 60)
                TvaCar = float(VcCar / (Qmaxm3 - Qminm3))
                TvaCar = float(TvaCar / 60)
                CopCar = float(TllQmaxCar + TvaCar)
                CopehCar = float(60 / (CopCar))

                VcCar = round(VcCar,2)
                BaseCar = round(BaseCar,2)
                AsCar = round(AsCar,2)
                TllQmaxCar = round(TllQmaxCar,2)
                TllQminCar = round(TllQminCar,2)
                TvaCar = round(TvaCar,2)
                CopCar = round(CopCar,2)
                CopehCar = round(CopehCar,2)

                carcrect = conn.cursor()

                carcmrecdb = """
                CREATE TABLE IF NOT EXISTS carcamo_rectangular (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                VcCar FLOAT NOT NULL,
                BaseCar FLOAT NOT NULL,
                AsCar FLOAT NOT NULL,
                TllQmaxCar  FLOAT NOT NULL,
                TllQminCar  FLOAT NOT NULL,
                TvaCar  FLOAT NOT NULL,
                CopCar  FLOAT NOT NULL,
                CopehCar  FLOAT NOT NULL)"""

                carcrect.execute(carcmrecdb)

                argcarcrect = (VcCar, BaseCar, AsCar, TllQmaxCar, TllQminCar, TvaCar, CopCar, CopehCar)

                carcarectconec = """
                INSERT INTO carcamo_rectangular (VcCar, BaseCar, AsCar, TllQmaxCar, TllQminCar, TvaCar, CopCar, CopehCar)
                VALUES (?,?,?,?,?,?,?,?)"""

                carcrect.execute(carcarectconec, argcarcrect)

                conn.commit()

                carcrect.close()

                framecart = LabelFrame(root4, text="Dimensiones del cárcamo rectangular", width = 950, height = 420, bd = 2, relief = RIDGE)
                framecart.place(x = 20, y = 15)

                etiqueta13 = Label(framecart,text = "Volumen en m^3:", font = ("Time new roman", 13), fg = "black").place(x = 50, y = 10)
                etiqueta14 = Label(framecart, text = "Área superficial en m^2:", font = ("Time new roman", 13), fg = "black").place(x = 50, y = 70)
                etiqueta15 = Label(framecart, text = "Largo en m: ", font = ("Time new roman", 13), fg = "black").place(x = 50, y = 140)
                etiqueta16 = Label(framecart, text = "Tiempo de llenado a caudal máximo en minutos:", font = ("Time new roman", 13), fg = "black").place(x = 50, y = 210)
                etiqueta16 = Label(framecart, text = "Tiempo de llenado a caudal mínimo en minutos:", font = ("Time new roman", 13), fg = "black").place(x = 50, y = 280)
                etiqueta16 = Label(framecart, text = "Tiempo de vaciado en minutos:", font = ("Time new roman", 13), fg = "black").place(x = 530, y = 10)
                etiqueta16 = Label(framecart, text = "Ciclo de operación en minutos:", font = ("Time new roman", 13), fg = "black").place(x = 530, y = 70)
                etiqueta16 = Label(framecart, text = "Ciclo de operación por hora:", font = ("Time new roman", 13), fg = "black").place(x = 530, y = 140)

                global entrBaseCar

                entrVcCar = DoubleVar()
                entrVcCar.set(VcCar)
                entrAsCar = DoubleVar()
                entrAsCar.set(AsCar)
                entrBaseCar = DoubleVar()
                entrBaseCar.set(BaseCar)
                entrTllQmaxCar = DoubleVar()
                entrTllQmaxCar.set(TllQmaxCar)
                entrTllQminCar = DoubleVar()
                entrTllQminCar.set(TllQminCar)
                entrTvaCar = DoubleVar()
                entrTvaCar.set(TvaCar)
                entrCopCar = DoubleVar()
                entrCopCar.set(CopCar)
                entrCopehCar = DoubleVar()
                entrCopehCar.set(CopehCar)

                txtVc = Entry(framecart, textvariable = entrVcCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 50, y= 35)
                txtAc = Entry(framecart, textvariable = entrAsCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 50, y = 95)
                txtBaseCar = Entry(framecart, textvariable = entrBaseCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 50, y= 165)
                txtTllQmaxCar = Entry(framecart, textvariable = entrTllQmaxCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 50, y = 235)
                txtTllQminCar = Entry(framecart, textvariable = entrTllQminCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 50, y = 305)
                txtTvaCar = Entry(framecart, textvariable = entrTvaCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 530, y = 35)
                txtCopCar = Entry(framecart, textvariable = entrCopCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 530, y = 95)
                txtCopehCar = Entry(framecart, textvariable = entrCopehCar, width = 20, font =("Time new roman", 11),  relief=FLAT, state=DISABLED).place(x = 530, y = 165)

        framecar = LabelFrame(pesPre, text = "Datos del cárcamo", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
        framecar.place(x = 20, y = 15)

        Prebombas = Label(framecar, text = "Presión necesaria para", font =("Time new roman", 13), fg = "black").place(x = 20, y = 20)
        Prebombas = Label(framecar, text = "las bombas en Kg/cm^2:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 45)
        Hbombas = Label(framecar, text = "Altura de impulsión en m", font =("Time new roman", 13), fg = "black").place(x = 20, y = 110)
        etiqueta9 = Label(framecar, text = "Tiempo funcional", font = ("Time new roman", 13), fg = "black").place(x = 280, y = 20)
        etiqueta9 = Label(framecar, text = "en minutos: ", font = ("Time new roman", 13), fg = "black").place(x = 280, y = 40)

        global entHimp
        global valortf

        entprb = DoubleVar()
        entprb.set(presbombs)
        entHimp = DoubleVar()
        entHimp.set(altimp)
        valortf = IntVar(value = 1)

        txtprb = Entry(framecar, textvariable = entprb, width = 20, font =("Time new roman", 11)).place(x = 20, y = 67)
        txtHimp = Entry(framecar, textvariable = entHimp, width = 20, font =("Time new roman", 11)).place(x = 20, y = 135)
        tf = Spinbox(framecar,from_=10, to=60, increment = 10,width= 3, font =("Time new roman", 10),  textvariable = valortf).place(x = 368, y = 42)

        botonrescar = Button(framecar, command = rescar, text = "Ver resultado del cárcamo", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 310, y = 225)

    def respcanal():
        root6 = Toplevel(root)
        root6.geometry("600x350+0+0")
        root6.title("Resultado del canal de llegada")

        flagCanalllegada=1

        Qmaxextm3 = float(Qmaxextl / 1000)
        nAnccanl = float(entrAnctu.get())
        nVcanl = float(entrV.get())
        nNcanl = float(entrn.get())

        if mett.get() == 2:
            nAnccanl = float(entrAnctu.get())

            nAnccanl = float(nAnccanl*0.0254)

            nAnccanl = round(nAnccanl,2)

        global AsCan
        global HCan
        global HeCan
        global LCan
        global RhCan
        global SCan
        global VcnCan

        AsCan = float(Qmaxextm3 / nVcanl)
        HCan = float(AsCan / nAnccanl)
        HeCan = float(HCan  + 0.30)
        LCan = float(nAnccanl * 2)
        RhCan = float(AsCan / ((HCan * 2) + nAnccanl))
        SCan = float(((nVcanl * nNcanl) / (RhCan ** (2/3))) **2)
        VsuCan = float(74.5/((3.1416)*(math.atan((149 / 10)** 0.5))))
        VcnCan = float((1 / nNcanl) * (VsuCan ** 0.66) * (SCan **0.5))
        AsCan = float(math.sqrt(AsCan))

        AsCan = round(AsCan,2)
        HCan = round(HCan,2)
        HeCan = round(HeCan,2)
        LCan = round(LCan,2)
        RhCan = round(RhCan,2)
        SCan = round(SCan,4)
        VcnCan = round(VcnCan,2)

        ccan= conn.cursor()

        clldb = """
        CREATE TABLE IF NOT EXISTS canal_llegada (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        AsCan FLOAT NOT NULL,
        HCan FLOAT NOT NULL,
        HeCan FLOAT NOT NULL,
        LCan  FLOAT NOT NULL,
        RhCan FLOAT NOT NULL,
        SCan FLOAT NOT NULL,
        VcnCan FLOAT NOT NULL)"""

        ccan.execute(clldb)

        argcan = (AsCan, HCan, HeCan, LCan, RhCan, SCan, VcnCan)

        canconec = """
        INSERT INTO canal_llegada (AsCan, HCan, HeCan, LCan, RhCan, SCan, VcnCan)
        VALUES (?,?,?,?,?,?,?)"""

        ccan.execute(canconec, argcan)

        conn.commit()

        ccan.close()

        framecanlleto = Frame(root6, width = 550, height = 310, bd = 2, relief = RIDGE)
        framecanlleto.place(x = 20, y = 15)

        etiqueta21 = Label(framecanlleto, text = "Área superficial en m^2:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 10)
        etiqueta22 = Label(framecanlleto, text = "Altura en m:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 70)
        etiqueta23 = Label(framecanlleto, text = "Altura efectiva en m:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 130)
        etiqueta24 = Label(framecanlleto, text = "Largo del canal en m:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 200)
        etiqueta25 = Label(framecanlleto, text = "Radio hidraúlico en m:", font = ("Time new roman", 13), fg = "black").place(x = 320, y = 10)
        etiqueta26 = Label(framecanlleto, text = "Pendiente en m:", font = ("Time new roman", 13), fg = "black").place(x = 320, y = 70)
        etiqueta27 = Label(framecanlleto, text = "Velocidad del canal en m/s:", font = ("Time new roman", 13), fg = "black").place(x = 320, y = 130)

        global entrAsCan
        global entrHeCan
        global entrLCan

        entrAsCan = DoubleVar()
        entrAsCan.set(AsCan)
        entrHCan = DoubleVar()
        entrHCan.set(HCan)
        entrHeCan = DoubleVar()
        entrHeCan.set(HeCan)
        entrLCan = DoubleVar()
        entrLCan.set(LCan)
        entrRhCan = DoubleVar()
        entrRhCan.set(RhCan)
        entrSCan = DoubleVar()
        entrSCan.set(SCan)
        entrVcnCan = DoubleVar()
        entrVcnCan.set(VcnCan)

        txtAs = Entry(framecanlleto, textvariable = entrAsCan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
        txtH = Entry(framecanlleto, textvariable = entrHCan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
        txtHe = Entry(framecanlleto, textvariable = entrHeCan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 155)
        txtL = Entry(framecanlleto, textvariable = entrLCan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 225)
        txtRh = Entry(framecanlleto, textvariable = entrRhCan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 320, y = 35)
        txtS = Entry(framecanlleto, textvariable = entrSCan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 320, y = 95)
        txtVcn = Entry(framecanlleto, textvariable = entrVcnCan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 320, y = 155)

    def respdesare():
        root8 = Toplevel(root)
        root8.geometry("1160x650+0+0")
        root8.title("Resultado del desarenador")

        flagDesarenador=1

        Qmaxmd = float((Qmaxl * 86400 ) / 1000)
        Qprommd = float((Qproml * 86400 ) / 1000)

        nPlDesa = float(entPl.get())
        nCsDesa = float(entCs.get())
        nLgDesa = float(valorLg.get())

        global AncDes
        global HDes

        VsDes = float((1/18) * (((2.65 - 0.998) * 981 * (0.0004)) / 0.01011))
        qDes = float((VsDes * 86400) / 100)
        AsDes = float(Qmaxmd / qDes)
        import math
        AnchDes = float(math.sqrt(AsDes / 3))
        AncDes = float(AnchDes / 2)
        LcDes = float(AnchDes  * nLgDesa)
        HDes = float(LcDes * (AnchDes / LcDes))
        VDes = float(LcDes * AnchDes * HDes)
        AtrnsDes = float(AnchDes * HDes)
        TFDes = float((HDes * 100) / VsDes)
        TRHDes = float(VDes / Qmaxmd)
        TRHDes = float(TRHDes * 86400)
        ParsDes = float(((Qprommd * 0.06) / 1000) * nPlDesa)
        H3Des = float(ParsDes / (AnchDes * LcDes))
        PartDes = float((Qprommd * 2.5) / 100)
        PartDes = float(PartDes / 10)
        import math
        VcDes = float(math.sqrt(((8 * 0.004) * (2.65 - 1) * 981 * 0.02) / 0.003))
        VhDes = float(Qmaxmd / (HDes * AnchDes))
        VhDes = float((VhDes * 100) / 86400)
        CSSTDes = float(nCsDesa - (nCsDesa * 0.4))

        if VhDes > VcDes:
            messagebox.showwarning(title ="Advertencia", message = "Habrá resuspención")

        VsDes = round(VsDes,2)
        qDes = round(qDes,2)
        AsDes = round(AsDes,2)
        AncDes = round(AnchDes,2)
        LcDes = round(LcDes,2)
        HDes = round(HDes,2)
        VDes = round(VDes,2)
        AtrnsDes = round(AtrnsDes,2)
        TFDes = round(TFDes,2)
        TRHDes = round(TRHDes,2)
        ParsDes = round(ParsDes,2)
        H3Des = round(H3Des,2)
        PartDes = round(PartDes,2)
        VcDes = round(VcDes,2)
        VhDes = round(VhDes,2)
        CSSTDes = round(CSSTDes,2)

        cdesa= conn.cursor()

        desadb = """
        CREATE TABLE IF NOT EXISTS desarenador (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        VsDes FLOAT NOT NULL,
        qDes FLOAT NOT NULL,
        AsDes FLOAT NOT NULL,
        AnchDes FLOAT NOT NULL,
        AncDes  FLOAT NOT NULL,
        LcDes FLOAT NOT NULL,
        HDes FLOAT NOT NULL,
        VDes FLOAT NOT NULL,
        AtrnsDes FLOAT NOT NULL,
        TFDes FLOAT NOT NULL,
        TRHDes  FLOAT NOT NULL,
        ParsDes FLOAT NOT NULL,
        H3Des FLOAT NOT NULL,
        PartDes FLOAT NOT NULL,
        VcDes FLOAT NOT NULL,
        VhDes  FLOAT NOT NULL,
        CSSTDes FLOAT NOT NULL)"""

        cdesa.execute(desadb)

        argdesa = (VsDes, qDes, AsDes, AnchDes, AncDes, LcDes, HDes, VDes, AtrnsDes, TFDes, TRHDes, ParsDes, H3Des, PartDes, VcDes, VhDes, CSSTDes)

        desaconec = """
        INSERT INTO desarenador (VsDes, qDes, AsDes, AnchDes, AncDes, LcDes, HDes, VDes, AtrnsDes, TFDes, TRHDes, ParsDes, H3Des, PartDes, VcDes, VhDes, CSSTDes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

        cdesa.execute(desaconec, argdesa)

        conn.commit()

        cdesa.close()

        framedesato = LabelFrame(root8, text = "Dimensiones del desarenador",width = 1110, height = 610, bd = 2, relief = RIDGE)
        framedesato.place(x = 20, y = 15)

        etiqueta97 = Label(framedesato, text = "Velocidad de sedimentación en cm/s: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
        etiqueta98= Label(framedesato, text = "Factor de carga en m^3/m^2*día: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
        etiqueta99 = Label(framedesato, text = "Área superficial en m^2: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 140)
        etiqueta100 = Label(framedesato, text = "Ancho del canal en m: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 210)
        etiqueta101 = Label(framedesato, text = "Largo del  en m: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 280)
        etiqueta102 = Label(framedesato, text = "Profundida del canal en m: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 350)
        etiqueta103 = Label(framedesato, text = "Volumen en m^3: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 420)
        etiqueta104 = Label(framedesato, text = "Área transversal en m^2: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 490)
        etiqueta105 = Label(framedesato, text = "Tiempo en sedimentar en segundos: ", font =("Time new roman", 13), fg = "black").place(x = 620, y = 10)
        etiqueta106 = Label(framedesato, text = "Tiempo de retención hidráulica en segundos: ", font =("Time new roman", 13), fg = "black").place(x = 620, y = 70)
        etiqueta107 = Label(framedesato, text = "Producción total de arena seca en m^3: ", font =("Time new roman", 13), fg = "black").place(x = 620, y = 140)
        etiqueta108 = Label(framedesato, text = "Profundidad para almacenamiento en m: ", font =("Time new roman", 13), fg = "black").place(x = 620, y = 210)
        etiqueta109 = Label(framedesato, text = "Producción de arena con tormenta en m^3: ", font =("Time new roman", 13), fg = "black").place(x = 620, y = 280)
        etiqueta110 = Label(framedesato, text = "Velocidad de arrastre en cm/s: ", font =("Time new roman", 13), fg = "black").place(x = 620, y = 350)
        etiqueta111 = Label(framedesato, text = "Velocidad horizontal en cm/s: ", font =("Time new roman", 13), fg = "black").place(x = 620, y = 420)
        etiqueta112 = Label(framedesato, text = "Concentración esperada de SST en el efluente: ", font =("Time new roman", 13), fg = "black").place(x = 620, y = 490)

        global entAtrns
        global entAnc
        global entLc
        global entH

        entVs = DoubleVar()
        entVs.set(VsDes)
        entq = DoubleVar()
        entq.set(qDes)
        entAs = DoubleVar()
        entAs.set(AsDes)
        entAnc = DoubleVar()
        entAnc.set(AncDes)
        entLc = DoubleVar()
        entLc.set(LcDes)
        entH = DoubleVar()
        entH.set(HDes)
        entV = DoubleVar()
        entV.set(VDes)
        entAtrns = DoubleVar()
        entAtrns.set(AtrnsDes)
        entTF = DoubleVar()
        entTF.set(TFDes)
        entTRH = DoubleVar()
        entTRH.set(TRHDes)
        entPars = DoubleVar()
        entPars.set(ParsDes)
        entH3 = DoubleVar()
        entH3.set(H3Des)
        entPart = DoubleVar()
        entPart.set(PartDes)
        entVc = DoubleVar()
        entVc.set(VcDes)
        entVh = DoubleVar()
        entVh.set(VhDes)
        entCSST = DoubleVar()
        entCSST.set(CSSTDes)

        txtVs = Entry(framedesato, textvariable = entVs, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
        txtq = Entry(framedesato, textvariable = entq, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
        txtAs = Entry(framedesato, textvariable = entAs, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 165)
        txtAnc = Entry(framedesato, textvariable = entAnc, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 235)
        txtLc = Entry(framedesato, textvariable = entLc, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 305)
        txtH = Entry(framedesato, textvariable = entH, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 375)
        txtV = Entry(framedesato, textvariable = entV, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 445)
        txtAtrns = Entry(framedesato, textvariable = entAtrns, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 515)
        txtTF = Entry(framedesato, textvariable = entTF, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 35)
        txtTRH = Entry(framedesato, textvariable = entTRH, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 95)
        txtPars = Entry(framedesato, textvariable = entPars, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y= 165)
        txtH3 = Entry(framedesato, textvariable = entH3, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 235)
        txtPart = Entry(framedesato, textvariable = entPart, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 305)
        txtVc = Entry(framedesato, textvariable = entVc, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 375)
        txtVh = Entry(framedesato, textvariable = entVh, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y= 445)
        txtCSST = Entry(framedesato, textvariable = entCSST, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 515)

    def framerejillas():

        framerej = LabelFrame(pesPre, text = "Datos del canal de rejillas", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
        framerej.place(x = 520, y = 15)

        def resprejillas():
            


            Qmaxextm3 = float(Qmaxextl  / 1000)
            Qpromm3 = float(Qproml  / 1000)
            Qminm3 = float(Qminl / 1000)

            if reji.get() == 1:
                root7 = Toplevel(root)
                root7.geometry("940x630+0+0")
                root7.title("Resultado de rejillas finas")

                nVaprox1 = float(entVaprox.get())
                nVprsreji1 = float(entVprs.get())
                nTetareji1 = int(entTeta.get())

                AsPre1 = float(Qmaxextm3 / nVaprox1)
                VprlPre1 = float(nVprsreji1 * 0.7)
                VprlQmaxPre1 = float(VprlPre1 * (Qmaxextm3 / Qpromm3))
                VprcolQmaxPre1 = float(nVprsreji1 * (Qmaxextm3 / Qpromm3))
                VaproxQmaxPre1 = float(Qmaxextm3 / AsPre1)
                VaproxQminPre1 = float(Qminm3 / AsPre1)
                import math
                AnPre1 = float(math.sqrt(AsPre1) + 0.10)
                HuPre1 = float(AsPre1 / AnPre1)
                AnefecPre1 = float(AnPre1 * 1.156)
                HePre1 = float(HuPre1 * 1.156)
                HtPre1 = float(HePre1 + 0.3)
                LcPre1 = float((AnefecPre1/ math.sin(nTetareji1)) * 1.5)
                NfPre1 = int((AnefecPre1 + 0.025) / (0.025 + 0.015))
                NefPre1 =  int(NfPre1 - 1)
                AnrfPre1 = float((NfPre1 * 0.015) + (NefPre1 * 0.025))
                EffPre1 = float((AnrfPre1 / AnefecPre1) * 100)
                HfPre1 =float((1.79 * ((0.015 / 0.025) ** 1.33) * (0.36 / (2 * 9.81))) * math.sin (nTetareji1))

                AsPre1 = round(AsPre1,2)
                VprlPre1 = round(VprlPre1,2)
                VprlQmaxPre1 = round(VprlQmaxPre1,2)
                VprcolQmaxPre1 = round(VprcolQmaxPre1,2)
                VaproxQmaxPre1 = round(VaproxQmaxPre1,2)
                VaproxQminPre1 = round(VaproxQminPre1,2)
                AnPre1 = round(AnPre1,2)
                HuPre1 = round(AnefecPre1,2)
                Anefecv = round(AnefecPre1,2)
                HePre1 = round(HePre1,2)
                HtPre1 = round(HtPre1,2)
                LcPre1 = round(LcPre1,2)
                NfPre1 = round(NfPre1,2)
                NefPre1 = round(NefPre1,2)
                AnrfPre1 = round(AnrfPre1,2)
                EffPre1 = round(EffPre1,2)
                HfPre1 = round(HfPre1,2)

                cpre1= conn.cursor()

                pret1db = """
                CREATE TABLE IF NOT EXISTS pretratamiento1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                AsPre1 FLOAT NOT NULL,
                VprlPre1 FLOAT NOT NULL,
                VprlQmaxPre1 FLOAT NOT NULL,
                VprcolQmaxPre1  FLOAT NOT NULL,
                VaproxQmaxPre1 FLOAT NOT NULL,
                VaproxQminPre1 FLOAT NOT NULL,
                AnPre1 FLOAT NOT NULL,
                HuPre1 FLOAT NOT NULL,
                HtPre1 FLOAT NOT NULL,
                LcPre1  FLOAT NOT NULL,
                NfPre1 FLOAT NOT NULL,
                NefPre1 FLOAT NOT NULL,
                AnrfPre1 FLOAT NOT NULL,
                EffPre1 FLOAT NOT NULL,
                HfPre1 FLOAT NOT NULL)"""

                cpre1.execute(pret1db)

                argpre1 = (AsPre1, VprlPre1, VprlQmaxPre1, VprcolQmaxPre1, VprcolQmaxPre1, VaproxQmaxPre1, VaproxQminPre1, AnPre1, HuPre1, HtPre1, LcPre1, NfPre1, NefPre1, AnrfPre1, EffPre1, HfPre1)

                pre1conec = """
                INSERT INTO pretratamiento1 (AsPre1, VprlPre1, VprlQmaxPre1, VprcolQmaxPre1, VprcolQmaxPre1, VaproxQmaxPre1, VaproxQminPre1, AnPre1, HuPre1, HtPre1, LcPre1, NfPre1, NefPre1, AnrfPre1, EffPre1, HfPre1)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

                cpre1.execute(pre1conec, argpre1)

                conn.commit()

                cpre1.close()

                framerejillato = LabelFrame(root7, text="Dimensiones de las rejillas finas", width = 880, height = 600, bd = 2, relief = RIDGE)
                framerejillato.place(x = 20, y = 15)

                etiqueta28 = Label(framerejillato, text = "Área superficial en m^2:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta29 = Label(framerejillato, text = "Velocidad de paso con rejilla limpia en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta30 = Label(framerejillato, text = "Velocidad de paso con  rejilla limpia y caudal máximo en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 130)
                etiqueta31 = Label(framerejillato, text = "Velocidad de paso con reja colmatada y caudal máximo en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 200)
                etiqueta32 = Label(framerejillato, text = "Velocidad de aproximación máxima en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 270)
                etiqueta33 = Label(framerejillato, text = "Velocidad de aproximación mínima en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 340)
                etiqueta34 = Label(framerejillato, text = "Ancho del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 410)
                etiqueta35 = Label(framerejillato, text = "Altura útil del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 480)
                etiqueta36 = Label(framerejillato, text = "Altura total del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 10)
                etiqueta37 = Label(framerejillato, text = "Longitud del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 70)
                etiqueta38 = Label(framerejillato, text = "Número de barras:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 130)
                etiqueta39 = Label(framerejillato, text = "Número de espacio de barras:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 200)
                etiqueta40 = Label(framerejillato, text = "Ancho de las rejas:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 270)
                etiqueta41 = Label(framerejillato, text = "Eficiencia de la reja:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 340)
                etiqueta42 = Label(framerejillato, text = "Perdida hidráulica a rejas limpia:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 410)

                global entAs
                global entAn
                global entHt
                global entLc

                entAs = DoubleVar()
                entAs.set(AsPre1)
                entVprl = DoubleVar()
                entVprl.set(VprlPre1)
                entVprlQmax = DoubleVar()
                entVprlQmax.set(VprlQmaxPre1)
                entVprcolQmax = DoubleVar()
                entVprcolQmax.set(VprcolQmaxPre1)
                entVaproxQmax = DoubleVar()
                entVaproxQmax.set(VaproxQmaxPre1)
                entVaproQmin = DoubleVar()
                entVaproQmin.set(VaproxQminPre1)
                entAn = DoubleVar()
                entAn.set(Anefecv)
                entHu = DoubleVar()
                entHu.set(HuPre1)
                entHt = DoubleVar()
                entHt.set(HtPre1)
                entLc = DoubleVar()
                entLc.set(LcPre1)
                entNf = DoubleVar()
                entNf.set(NfPre1)
                entNef = DoubleVar()
                entNef.set(NefPre1)
                entAnrf = DoubleVar()
                entAnrf.set(AnrfPre1)
                entEff = DoubleVar()
                entEff.set(EffPre1)
                entHf = DoubleVar()
                entHf.set(HfPre1)

                txtAs = Entry(framerejillato, textvariable = entAs, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
                txtVprl = Entry(framerejillato, textvariable = entVprl, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
                txtVprlQmax = Entry(framerejillato, textvariable = entVprlQmax, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 155)
                txtVprcolQmax = Entry(framerejillato, textvariable = entVprcolQmax, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 225)
                txtVaproxQmax = Entry(framerejillato, textvariable = entVaproxQmax, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 295)
                txtVaproQmin = Entry(framerejillato, textvariable = entVaproQmin, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 365)
                txtAn = Entry(framerejillato, textvariable = entAn, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 435)
                txtHu = Entry(framerejillato, textvariable = entHu, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 505)
                txtHt = Entry(framerejillato, textvariable = entHt, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 35)
                txtLc = Entry(framerejillato, textvariable = entLc, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y= 95)
                txtNf = Entry(framerejillato, textvariable = entNf, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 155)
                txtNef = Entry(framerejillato, textvariable = entNef, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 225)
                txtAnrf = Entry(framerejillato, textvariable = entAnrf, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 295)
                txtEff = Entry(framerejillato, textvariable = entEff, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 365)
                txtHf = Entry(framerejillato, textvariable = entHf, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 435)
            elif reji.get() == 2:
                root7 = Toplevel(root)
                root7.geometry("1380x620+0+0")
                root7.title("Resultado de rejillas medias")

                nVaproxreji2 = float(entVaprox.get())
                nVprsreji2 = float(entVprs.get())
                nTetareji2 = int(entTeta.get())

                AsPre2 = float(Qmaxextm3 / nVaproxreji2)
                VprlPre2 = float(nVprsreji2 * 0.7)
                VprlQmaxPre2 = float(VprlPre2 * (Qmaxextm3 / Qpromm3))
                VprcolQmaxPre2 = float(nVprsreji2 * (Qmaxextm3 / Qpromm3))
                VaproxQmaxPre2 = float(Qmaxextm3 / AsPre2)
                VaproxQminPre2 = float(Qminm3 / AsPre2)
                import math
                AnPre2 = float(math.sqrt(AsPre2))
                HuPre2 = float(AsPre2 / AnPre2)
                AnefecPre2 = float(AnPre2 * 1.156)
                HePre2 = float(HuPre2 * 1.156)
                HtPre2 = float(HePre2 + 0.3)
                LcPre2 = float((AnefecPre2/ math.sin(nTetareji2))* 1.5)
                NmPre2 = int((AnefecPre2 + 0.020) / (0.020 + 0.035))
                NemPre2 =  int(NmPre2 - 1)
                AnrmPre2 = float((NmPre2 * 0.035) + (NemPre2 * 0.020))
                EfmPre2 = float((AnrmPre2 / AnefecPre2) * 100)
                HmPre2 =float((1.79 * ((0.035 / 0.020) ** 1.33) * (0.36 / (2 * 9.81))) * math.sin (nTetareji2))
                NgPre2 = int((AnefecPre2 + 0.025) / (0.025 + 0.05))
                NegPre2 =  int(NgPre2 - 1)
                AnrgPre2 = float((NgPre2 * 0.05) + (NegPre2 * 0.025))
                EfgPre2 = float((AnrgPre2 / AnefecPre2) * 100)
                HgPre2 =float((1.79 * ((0.05 / 0.025) ** 1.33) * (0.36 / (2 * 9.81))) * math.sin (nTetareji2))

                AsPre2 = round(AsPre2,2)
                VprlPre2 = round(VprlPre2,2)
                VprlQmaxPre2 = round(VprlQmaxPre2,2)
                VprcolQmaxPre2 = round(VprcolQmaxPre2,2)
                VaproxQmaxPre2 = round(VaproxQmaxPre2,2)
                VaproxQminPre2 = round(VaproxQminPre2,2)
                AnPre2 = round(AnPre2,2)
                HuPre2 = round(HuPre2,2)
                AnefecPre2 = round(AnefecPre2,2)
                HePre2 = round(HePre2,2)
                HtPre2 = round(HtPre2,2)
                LcPre2 = round(LcPre2,2)
                NmPre2 = round(NmPre2,2)
                NemPre2 = round(NemPre2,2)
                AnrmPre2 = round(AnrmPre2,2)
                EfmPre2= round(EfmPre2,2)
                HmPre2 = round(HmPre2,2)
                NgPre2 = round(NgPre2,2)
                NegPre2 = round(NegPre2,2)
                AnrgPre2 = round(AnrgPre2,2)
                EfgPre2 = round(EfgPre2,2)
                HgPre2 = round(HgPre2,2)

                cpre2= conn.cursor()

                pret2db = """
                CREATE TABLE IF NOT EXISTS pretratamiento2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                AsPre2 FLOAT NOT NULL,
                VprlPre2 FLOAT NOT NULL,
                VprlQmaxPre2 FLOAT NOT NULL,
                VprcolQmaxPre2  FLOAT NOT NULL,
                VaproxQmaxPre2 FLOAT NOT NULL,
                VaproxQminPre2 FLOAT NOT NULL,
                AnPre2 FLOAT NOT NULL,
                HuPre2 FLOAT NOT NULL,
                HtPre2 FLOAT NOT NULL,
                LcPre2  FLOAT NOT NULL,
                NmPre2 FLOAT NOT NULL,
                NemPre2 FLOAT NOT NULL,
                AnrmPre2 FLOAT NOT NULL,
                EfmPre2 FLOAT NOT NULL,
                HmPre2 FLOAT NOT NULL,
                NgPre2 FLOAT NOT NULL,
                NegPre2 FLOAT NOT NULL,
                AnrgPre2  FLOAT NOT NULL,
                EfgPre2 FLOAT NOT NULL,
                HgPre2 FLOAT NOT NULL)"""

                cpre2.execute(pret2db)

                argpre2 = (AsPre2, VprlPre2, VprlQmaxPre2, VprcolQmaxPre2, VprcolQmaxPre2, VaproxQmaxPre2, VaproxQminPre2, AnPre2, HuPre2, HtPre2, LcPre2, NmPre2, NemPre2, AnrmPre2, EfmPre2, HmPre2, NgPre2, NegPre2, AnrgPre2, EfgPre2, HgPre2)

                pre2conec = """
                INSERT INTO pretratamiento2 (AsPre2, VprlPre2, VprlQmaxPre2, VprcolQmaxPre2, VprcolQmaxPre2, VaproxQmaxPre2, VaproxQminPre2, AnPre2, HuPre2, HtPre2, LcPre2, NmPre2, NemPre2, AnrmPre2, EfmPre2, HmPre2, NgPre2, NegPre2, AnrgPre2, EfgPre2, HgPre2)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

                cpre2.execute(pre2conec, argpre2)

                conn.commit()

                cpre2.close()

                framerejillamedito = LabelFrame(root7, text ="Dimensiones de las rejillas medianas y grandes", width = 1300, height = 580, bd = 2, relief = RIDGE)
                framerejillamedito.place(x = 20, y = 15)


                etiqueta43 = Label(framerejillamedito, text = "Área superficial en m^2:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta44 = Label(framerejillamedito, text = "Velocidad de paso con rejilla limpia en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta45 = Label(framerejillamedito, text = "Velocidad de paso con rejilla limpia y caudal máximo en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 140)
                etiqueta46 = Label(framerejillamedito, text = "Velocidad de paso con rejilla colmatada y caudal máxima en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 210)
                etiqueta47 = Label(framerejillamedito, text = "Velocidad de aproximación máxima en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 280)
                etiqueta48 = Label(framerejillamedito, text = "Velocidad de aproximación mínima en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 350)
                etiqueta49 = Label(framerejillamedito, text = "Ancho del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 420)
                etiqueta50 = Label(framerejillamedito, text = "Altura útil del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 10)
                etiqueta51 = Label(framerejillamedito, text = "Altura total del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 70)
                etiqueta52 = Label(framerejillamedito, text = "Longitud del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 140)
                etiqueta53 = Label(framerejillamedito, text = "Número de barras medias:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 210)
                etiqueta54 = Label(framerejillamedito, text = "Número de espacios entre barras medias:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 280)
                etiqueta55 = Label(framerejillamedito, text = "Ancho de las rejillas medias:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 350)
                etiqueta56 = Label(framerejillamedito, text = "Eficiencia de la reja media:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 420)
                etiqueta57 = Label(framerejillamedito, text = "Perdida hidráulica a reja mediana limpia:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 10)
                etiqueta58 = Label(framerejillamedito, text = "Número de barras gruesas:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 70)
                etiqueta59 = Label(framerejillamedito, text = "Número de espacios entre de barras gruesas:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 140)
                etiqueta60 = Label(framerejillamedito, text = "Ancho de las rejillas gruesas:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 210)
                etiqueta61 = Label(framerejillamedito, text = "Eficiencia de la reja gruesa:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 280)
                etiqueta62 = Label(framerejillamedito, text = "Perdida hidráulica a reja gruesa limpia:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 350)

                entAs = DoubleVar()
                entAs.set(AsPre2)
                entVprl = DoubleVar()
                entVprl.set(VprlPre2)
                entVprlQmax = DoubleVar()
                entVprlQmax.set(VprlQmaxPre2)
                entVprcolQmax = DoubleVar()
                entVprcolQmax.set(VprcolQmaxPre2)
                entVaproxQmax = DoubleVar()
                entVaproxQmax.set(VaproxQmaxPre2)
                entVaproQmin = DoubleVar()
                entVaproQmin.set(VaproxQminPre2)
                entAn = DoubleVar()
                entAn.set(AnefecPre2)
                entHu = DoubleVar()
                entHu.set(HuPre2)
                entHt = DoubleVar()
                entHt.set(HtPre2)
                entLc = DoubleVar()
                entLc.set(LcPre2)
                entNm = DoubleVar()
                entNm.set(NmPre2)
                entNem = DoubleVar()
                entNem.set(NemPre2)
                entAnrm = DoubleVar()
                entAnrm.set(AnrmPre2)
                entEfm = DoubleVar()
                entEfm.set(EfmPre2)
                entHm = DoubleVar()
                entHm.set(HmPre2)
                entNg = DoubleVar()
                entNg.set(NgPre2)
                entNeg = DoubleVar()
                entNeg.set(NegPre2)
                entAnrg = DoubleVar()
                entAnrg.set(AnrgPre2)
                entEfg = DoubleVar()
                entEfg.set(EfgPre2)
                entHg = DoubleVar()
                entHg.set(HgPre2)

                txtAs = Entry(framerejillamedito, textvariable = entAs, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
                txtVprl = Entry(framerejillamedito, textvariable = entVprl, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
                txtVprlQmax = Entry(framerejillamedito, textvariable = entVprlQmax, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 165)
                txtVprcolQmax = Entry(framerejillamedito, textvariable = entVprcolQmax, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 235)
                txtVaproxQmax = Entry(framerejillamedito, textvariable = entVaproxQmax, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 305)
                txtVaproQmin = Entry(framerejillamedito, textvariable = entVaproQmin, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 375)
                txtAn = Entry(framerejillamedito, textvariable = entAn, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 445)
                txtHu = Entry(framerejillamedito, textvariable = entHu, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 35)
                txtHt = Entry(framerejillamedito, textvariable = entHt, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 95)
                txtLc = Entry(framerejillamedito, textvariable = entLc, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y= 165)
                txtNm = Entry(framerejillamedito, textvariable = entNm, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 235)
                txtNef = Entry(framerejillamedito, textvariable = entNem, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 305)
                txtAnrm = Entry(framerejillamedito, textvariable = entAnrm, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 375)
                txtEfm = Entry(framerejillamedito, textvariable = entEfm, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 445)
                txtHm = Entry(framerejillamedito, textvariable = entHm, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 35)
                txtNg = Entry(framerejillamedito, textvariable = entNg, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 95)
                txtNeg = Entry(framerejillamedito, textvariable = entNeg, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 165)
                txtAnrg = Entry(framerejillamedito, textvariable = entAnrg, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 235)
                txtEfg = Entry(framerejillamedito, textvariable = entEfg, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 305)
                txtHg = Entry(framerejillamedito, textvariable = entHg, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 375)
            elif reji.get() == 3:
                root7 = Toplevel(root)
                root7.geometry("1380x710+0+0")
                root7.title("Resultado de rejillas grandes")

                nVaproxreji3 = float(entVaprox.get())
                nVprsreji3 = float(entVprs.get())
                nTetareji3 = int(entTeta.get())

                AsPre3 = float(Qmaxextm3 / nVaproxreji3)
                VprlPre3 = float(nVprsreji3 * 0.7)
                VprlQmaxPre3 = float(VprlPre3 * (Qmaxextm3 / Qpromm3))
                VprcolQmaxPre3 = float(nVprsreji3 * (Qmaxextm3 / Qpromm3))
                VaproxQmaxPre3 = float(Qmaxextm3 / AsPre3)
                VaproxQminPre3 = float(Qminm3 / AsPre3)
                import math
                AnPre3 = float(math.sqrt(AsPre3))
                HuPre3 = float(AsPre3 / AnPre3)
                AnefecPre3 = float(AnPre3 * 1.156)
                HePre3 = float(HuPre3 * 1.156)
                HtPre3 = float(HePre3 + 0.3)
                LcPre3 = float((AnefecPre3/ math.sin(nTetareji3)) * 1.5)
                NfPre3 = int((AnefecPre3 + 0.025) / (0.025 + 0.015))
                NefPre3 =  int(NfPre3 - 1)
                AnrfPre3 = float((NfPre3 * 0.015) + (NefPre3 * 0.025))
                EffPre3 = float((AnrfPre3 / AnefecPre3) * 100)
                HfPre3 =float((1.79 * ((0.015 / 0.025) ** 1.33) * (0.36 / (2 * 9.81))) * math.sin (nTetareji3))
                NmPre3 = int((AnefecPre3 + 0.020) / (0.020 + 0.035))
                NemPre3 =  int(NmPre3 - 1)
                AnrmPre3 = float((NmPre3 * 0.035) + (NemPre3 * 0.020))
                EfmPre3 = float((AnrmPre3 / AnefecPre3) * 100)
                HmPre3 =float((1.79 * ((0.035 / 0.020) ** 1.33) * (0.36 / (2 * 9.81))) * math.sin (nTetareji3))
                NgPre3 = int((AnefecPre3 + 0.025) / (0.025 + 0.05))
                NegPre3 =  int(NgPre3 - 1)
                AnrgPre3 = float((NgPre3 * 0.05) + (NegPre3 * 0.025))
                EfgPre3 = float((AnrgPre3 / AnefecPre3) * 100)
                HgPre3 =float((1.79 * ((0.05 / 0.025) ** 1.33) * (0.36 / (2 * 9.81))) * math.sin (nTetareji3))

                AsPre3 = round(AsPre3,2)
                VprlPre3 = round(VprlPre3,2)
                VprlQmaxPre3 = round(VprlQmaxPre3,2)
                VprcolQmaxPre3 = round(VprcolQmaxPre3,2)
                VprlQmaxPre3 = round(VprlQmaxPre3,2)
                VaproxQmaxPre3 = round(VaproxQmaxPre3,2)
                VaproxQminPre3 = round(VaproxQminPre3,2)
                AnPre3 = round(AnPre3,2)
                HuPre3 = round(HuPre3,2)
                AnefecPre3 = round(AnefecPre3,2)
                HePre3 = round(HePre3,2)
                HtPre3 = round(HtPre3,2)
                LcPre3 = round(LcPre3,2)
                NfPre3 = round(NfPre3,2)
                NefPre3 = round(NefPre3,2)
                AnrfPre3 = round(AnrfPre3,2)
                EffPre3 = round(EffPre3,2)
                HfPre3 = round(HfPre3,2)
                NmPre3 = round(NmPre3,2)
                NemPre3 = round(NemPre3,2)
                AnrmPre3 = round(AnrmPre3,2)
                EfmPre3 = round(EfmPre3,2)
                HmPre3 = round(HmPre3,2)
                NgPre3 = round(NgPre3,2)
                NegPre3 = round(NegPre3,2)
                AnrgPre3 = round(AnrgPre3,2)
                EfgPre3 = round(EfgPre3,2)
                HgPre3 = round(HgPre3,2)

                cpre3= conn.cursor()

                pret3db = """
                CREATE TABLE IF NOT EXISTS pretratamiento3 (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                AsPre3 FLOAT NOT NULL,
                VprlPre3 FLOAT NOT NULL,
                VprlQmaxPre3 FLOAT NOT NULL,
                VprcolQmaxPre3  FLOAT NOT NULL,
                VaproxQmaxPre3 FLOAT NOT NULL,
                VaproxQminPre3 FLOAT NOT NULL,
                AnPre3 FLOAT NOT NULL,
                HuPre3 FLOAT NOT NULL,
                HtPre3 FLOAT NOT NULL,
                LcPre3  FLOAT NOT NULL,
                NfPre3 FLOAT NOT NULL,
                NefPre3 FLOAT NOT NULL,
                AnrfPre3 FLOAT NOT NULL,
                EffPre3 FLOAT NOT NULL,
                HfPre3 FLOAT NOT NULL,
                NmPre3 FLOAT NOT NULL,
                NemPre3 FLOAT NOT NULL,
                AnrmPre3  FLOAT NOT NULL,
                EfmPre3 FLOAT NOT NULL,
                HmPre3 FLOAT NOT NULL,
                NgPre3 FLOAT NOT NULL,
                NegPre3 FLOAT NOT NULL,
                AnrgPre3  FLOAT NOT NULL,
                EfgPre3 FLOAT NOT NULL,
                HgPre3 FLOAT NOT NULL)"""

                cpre3.execute(pret3db)

                argpre3 = (AsPre3, VprlPre3, VprlQmaxPre3, VprcolQmaxPre3, VprcolQmaxPre3, VaproxQmaxPre3, VaproxQminPre3, AnPre3, HuPre3, HtPre3, LcPre3, NfPre3, NefPre3, AnrfPre3, EffPre3, HfPre3, NmPre3, NemPre3, AnrmPre3, EfmPre3, HmPre3, NgPre3, NegPre3, AnrgPre3, EfgPre3, HgPre3)

                pre3conec = """
                INSERT INTO pretratamiento3 (AsPre3, VprlPre3, VprlQmaxPre3, VprcolQmaxPre3, VprcolQmaxPre3, VaproxQmaxPre3, VaproxQminPre3, AnPre3, HuPre3, HtPre3, LcPre3, NfPre3, NefPre3, AnrfPre3, EffPre3, HfPre3, NmPre3, NemPre3, AnrmPre3, EfmPre3, HmPre3, NgPre3, NegPre3, AnrgPre3, EfgPre3, HgPre3)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

                cpre3.execute(pre3conec, argpre3)

                conn.commit()

                cpre3.close()

                framerejillagradito = LabelFrame(root7, text = "Dimensiones de rejillas finas, medianas y grandes", width = 1310, height = 670, bd = 2, relief = RIDGE)
                framerejillagradito.place(x = 20, y = 15)

                etiqueta63 = Label(framerejillagradito, text = "Área superficial en m^2:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta64 = Label(framerejillagradito, text = "Velocidad de paso con rejilla limpia en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta65 = Label(framerejillagradito, text = "Velocidad de paso con rejilla limpia y caudal máximo en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 140)
                etiqueta66 = Label(framerejillagradito, text = "Velocidad de paso con rejilla colmatada y caudal máximo en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 210)
                etiqueta67 = Label(framerejillagradito, text = "Velocidad de aproximación máxima en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 280)
                etiqueta68 = Label(framerejillagradito, text = "Velocidad de aproximación mínima en m/s:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 350)
                etiqueta69 = Label(framerejillagradito, text = "Ancho del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 420)
                etiqueta70 = Label(framerejillagradito, text = "Altura útil del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 490)
                etiqueta71 = Label(framerejillagradito, text = "Altura total del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 560)
                etiqueta72 = Label(framerejillagradito, text = "Longitud del canal en m:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 10)
                etiqueta73 = Label(framerejillagradito, text = "Número de barras finas:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 70)
                etiqueta74 = Label(framerejillagradito, text = "Número de espacio entre barras finas:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 140)
                etiqueta75 = Label(framerejillagradito, text = "Ancho de las rejillas finas:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 210)
                etiqueta76 = Label(framerejillagradito, text = "Eficiencia de la reja fina:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 280)
                etiqueta77 = Label(framerejillagradito, text = "Perdida hidráulica a reja limpia:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 350)
                etiqueta78 = Label(framerejillagradito, text = "Número de barras medias:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 420)
                etiqueta79 = Label(framerejillagradito, text = "Número de espacio entre barras medias:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 490)
                etiqueta80 = Label(framerejillagradito, text = "Ancho de las rejillas medias:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 10)
                etiqueta81 = Label(framerejillagradito, text = "Eficiencia de la reja media:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 70)
                etiqueta82 = Label(framerejillagradito, text = "Perdida hidráulico a reja mediana limpia:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 140)
                etiqueta83 = Label(framerejillagradito, text = "Número de barras gruesas:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 210)
                etiqueta84 = Label(framerejillagradito, text = "Número de espacio entre barras gruesas:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 280)
                etiqueta85 = Label(framerejillagradito, text = "Ancho de las rejillas gruesas:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 350)
                etiqueta86 = Label(framerejillagradito, text = "Eficiencia de la reja gruesa:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 420)
                etiqueta87 = Label(framerejillagradito, text = "Perdida hidráulica a reja gruesa limpia:", font =("Time new roman", 13), fg = "black").place(x = 940, y = 490)

                entAs = DoubleVar()
                entAs.set(AsPre3)
                entVprl = DoubleVar()
                entVprl.set(VprlPre3)
                entVprlQmax = DoubleVar()
                entVprlQmax.set(VprlQmaxPre3)
                entVprcolQmax = DoubleVar()
                entVprcolQmax.set(VprcolQmaxPre3)
                entVaproxQmax = DoubleVar()
                entVaproxQmax.set(VaproxQmaxPre3)
                entVaproQmin = DoubleVar()
                entVaproQmin.set(VaproxQminPre3)
                entAn = DoubleVar()
                entAn.set(AnefecPre3)
                entHu = DoubleVar()
                entHu.set(HuPre3)
                entHt = DoubleVar()
                entHt.set(HtPre3)
                entLc = DoubleVar()
                entLc.set(LcPre3)
                entNf = DoubleVar()
                entNf.set(NfPre3)
                entNef = DoubleVar()
                entNef.set(NefPre3)
                entAnrf = DoubleVar()
                entAnrf.set(AnrfPre3)
                entEff = DoubleVar()
                entEff.set(EffPre3)
                entHf = DoubleVar()
                entHf.set(HfPre3)
                entNm = DoubleVar()
                entNm.set(NmPre3)
                entNem = DoubleVar()
                entNem.set(NemPre3)
                entAnrm = DoubleVar()
                entAnrm.set(AnrmPre3)
                entEfm = DoubleVar()
                entEfm.set(EfmPre3)
                entHm = DoubleVar()
                entHm.set(HmPre3)
                entNg = DoubleVar()
                entNg.set(NgPre3)
                entNeg = DoubleVar()
                entNeg.set(NegPre3)
                entAnrg = DoubleVar()
                entAnrg.set(AnrgPre3)
                entEfg = DoubleVar()
                entEfg.set(EfgPre3)
                entHg = DoubleVar()
                entHg.set(HgPre3)

                txtAs = Entry(framerejillagradito, textvariable = entAs, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
                txtVprl = Entry(framerejillagradito, textvariable = entVprl, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
                txtVprlQmax = Entry(framerejillagradito, textvariable = entVprlQmax, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 165)
                txtVprcolQmax = Entry(framerejillagradito, textvariable = entVprcolQmax, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 235)
                txtVaproxQmax = Entry(framerejillagradito, textvariable = entVaproxQmax, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 305)
                txtVaproQmin = Entry(framerejillagradito, textvariable = entVaproQmin, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 375)
                txtAn = Entry(framerejillagradito, textvariable = entAn, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 445)
                txtHu = Entry(framerejillagradito, textvariable = entHu, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 515)
                txtHt = Entry(framerejillagradito, textvariable = entHt, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 585)
                txtLc = Entry(framerejillagradito, textvariable = entLc, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y= 35)
                txtNf = Entry(framerejillagradito, textvariable = entNf, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 95)
                txtNef = Entry(framerejillagradito, textvariable = entNef, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 165)
                txtAnrf = Entry(framerejillagradito, textvariable = entAnrf, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 235)
                txtEff = Entry(framerejillagradito, textvariable = entEff, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 305)
                txtHf = Entry(framerejillagradito, textvariable = entHf, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 375)
                txtNm = Entry(framerejillagradito, textvariable = entNm, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 445)
                txtNem = Entry(framerejillagradito, textvariable = entNem, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 515)
                txtAnrm = Entry(framerejillagradito, textvariable = entAnrm, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 35)
                txtEfm = Entry(framerejillagradito, textvariable = entEfm, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 95)
                txtHm = Entry(framerejillagradito, textvariable = entHm, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 165)
                txtNg = Entry(framerejillagradito, textvariable = entNg, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 235)
                txtNeg = Entry(framerejillagradito, textvariable = entNeg, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 305)
                txtAnrg = Entry(framerejillagradito, textvariable = entAnrg, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 375)
                txtEfg = Entry(framerejillagradito, textvariable = entEfg, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 445)
                txtHg = Entry(framerejillagradito, textvariable = entHg, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 940, y = 515)

        etiqueta92 = Label(framerej, text = "Velocidad de aproximación m/s: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
        etiqueta92 = Label(framerej, text = "Velocidad con rejillas sucias en m/s: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
        etiqueta96 = Label(framerej, text = "θ de inclinación: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 135)

        global entVaprox
        global entVprs
        global entTeta

        entVaprox = DoubleVar()
        entVaprox.set(0.3)
        entVprs = DoubleVar()
        entVprs.set(0.9)

        entTeta = IntVar(value = 1)
        txtTeta = Spinbox(framerej,from_=45, to=60, increment = 5,width= 3, textvariable = entTeta).place(x = 146, y = 137)

        txtVaprox = Entry(framerej, textvariable = entVaprox, width = 20, font =("Time new roman", 11)).place(x = 20, y = 35)
        txtVprs = Entry(framerej, textvariable = entVprs, width = 20, font =("Time new roman", 11)).place(x = 20, y = 97)

        botonresrej = Button(framerej, command = resprejillas, text = "Ver resultado de las rejillas", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 305, y = 225)

    Mar = float(entrMSNM.get())
    if carcamo.get() == 1 and Mar <= 400:
        framecar(1.033, 10.33)
    elif carcamo.get() == 1 and Mar <= 1200:
        framecar(0.996, 9.86)
    elif carcamo.get() == 1 and Mar <= 1600:
        framecar(0.845, 8.90)
    elif carcamo.get() == 1 and Mar <= 2000:
        framecar(0.804, 8.40)
    elif carcamo.get() == 1 and Mar <= 2400:
        framecar(0.765, 7.65)
    elif carcamo.get() == 1 and Mar <= 3600:
        framecar(0.695, 6.95)
    elif carcamo.get() == 2 and Mar <= 400:
        framecar(1.033, 10.33)
    elif carcamo.get() == 2 and Mar <= 1200:
        framecar(0.996, 9.86)
    elif carcamo.get() == 2 and Mar <= 1600:
        framecar(0.845, 8.90)
    elif carcamo.get() == 2 and Mar <= 2000:
        framecar(0.804, 8.40)
    elif carcamo.get() == 2 and Mar <= 2400:
        framecar(0.765, 7.65)
    elif carcamo.get() == 2 and Mar <= 3600:
        framecar(0.695, 6.95)

    if reji.get() == 1:
        framerejillas()
    elif reji.get() == 2:
        framerejillas()
    elif reji.get() == 3:
        framerejillas()

    def continuar2():
        notebook.add(pesVert, text = "Vertedor y zanjas", state="normal")

        respuesta = askquestion(title = "Guardar y continuar proceso", message= "¿Desea guardar antes de continuar?")
        if respuesta == "yes":
            if carcamo.get() == 1:
                Áreacarc = str(entrAsCar.get())
                Radiocarc = str(entrRcCar.get())
                Profundidadcarc = str(entHimp.get())
                Volumencarc = str(entrVcCar.get())
                txtocar = ("\n\nLas dimensiones del cárcamo circular resultantes fueron:\nÁrea superficial:\t\t"+Áreacarc+"\tm^2\nRadio:\t\t\t\t"+Radiocarc+"\tm\nProfundidad:\t\t\t"+Profundidadcarc+"\tm")
                archivo = open(file,"a")
                archivo.write(txtocar)
                archivo.close()
            else:
                Áreacarr = str(entrAsCar.get())
                Largocarr = str(entrBaseCar.get())
                Profundidadcarr = str(entHimp.get())
                Volumencarr = str(entrVcCar.get())
                txtocar = ("\n\nLas dimensiones del cárcamo rectangular resultantes fueron:\nÁrea superficial:\t\t"+Areacarr+"\tm^2\nLargo:\t\t\t\t"+Largocarr+"\tm\nProfundidad:\t\t\t"+Profundidadcarr+"\tm")
                archivo = open(file,"a")
                archivo.write(txtocar)
                archivo.close()

            Areacanl= str(entrAsCan.get())
            Alturacanl = str(entrHeCan.get())
            Largocanl = str(entrLCan.get())
            txtocanl = ("\n\nLas dimensiones del canal de llegada resultantes fueron:\nÁrea superficial:\t\t"+Areacanl+"\tm^2\nLargo:\t\t\t\t"+Largocanl+"\tm\nAlto:\t\t\t\t"+Largocanl+"\tm")
            archivo = open(file,"a")
            archivo.write(txtocanl)
            archivo.close()

            Areareji3= str(entAs.get())
            Anchoreji3 = str(entAn.get())
            Alturareji3 = str(entHt.get())
            Largoreji3 = str(entLc.get())
            txtoreji3 = ("\n\nLas dimensiones del canal de rejillas resultantes fueron:\nÁrea superficial:\t\t"+Areareji3+"\tm^2\nLargo:\t\t\t\t"+Largoreji3+"\tm\nAltura:\t\t\t\t"+Alturareji3+"\tm\nAncho:\t\t\t\t"+Anchoreji3+"\tm")
            archivo = open(file,"a")
            archivo.write(txtoreji3)
            archivo.close()

            Areadesa = str(entAs.get())
            Areatransdesa = str(entAtrns.get())
            Anchodesa = str(entAnc.get())
            Largodesa = str(entLc.get())
            Profundidaddesa = str(entH.get())
            txtodesa = ("\n\nLas dimensiones del desarenador resultantes fueron:\nÁrea superficial:\t\t"+Areadesa+"\tm^2\nÁrea transversa:\t\t"+Areatransdesa+"\tm^2\nAncho:\t\t\t\t"+Anchodesa+"\tm\nLargo:\t\t\t\t"+Largodesa+"\tm\nProfundidad"+Profundidaddesa+"\tm")
            archivo = open(file,"a")
            archivo.write(txtodesa)
            archivo.close()

        def croquiszanjas():
            if zanja.get() == 1:
                rootcz = Toplevel(root)
                rootcz.geometry("808x298+0+0")
                rootcz.title("Esquema del vertedor sutro, la zanja orbal y sedimentador")

                lblzanorb = Label(rootcz, image = Zanjorb).place(x = 0, y = 0)
            elif zanja.get() == 2:
                rootcz = Toplevel(root)
                rootcz.geometry("808x298+0+0")
                rootcz.title("Esquema del vertedor sutro, la zanja isla y sedimentador")

                lblzanisl = Label(rootcz, image = Zanjislas).place(x = 0, y = 0)
            elif zanja.get() == 3:
                rootcz = Toplevel(root)
                rootcz.geometry("808x298+0+0")
                rootcz.title("Esquema del vertedor sutro, la zanja recta y sedimentador")

                lblzanisl = Label(rootcz, image = Zanjrecta).place(x = 0, y = 0)
            elif zanja.get() == 4 :
                rootcz = Toplevel(root)
                rootcz.geometry("808x298+0+0")
                rootcz.title("Esquema del vertedor sutro, la zanja herradura y sedimentador")

                lblzanherra = Label(rootcz, image = Zanjherra).place(x = 0, y = 0)

        def respvertedor():

                root9 = Toplevel(root)
                root9.geometry("790x480+0+0")
                root9.title("Resultados de vertedor sutro")

                frameverto = Frame(root9, width = 1310, height = 250, bd = 2, relief = RIDGE)
                frameverto.place(x = 20, y = 15)

                n1 = float(entAnchZut.get())
                n2 = float(entHZut.get())

                rows = []

                nazut = float(enta.get())
                nnzut = int(entn.get())

                i = 0
                t = 0
                j = 0

                a1 = float(nazut / 100)
                b1 = float(n1 / 100)
                H1 = float(n2 / 100)
                cols = []

                while i < (nnzut + 1):

                    cols = []

                    if i == nnzut :
                        AltVert = float(((n2 / nnzut) * i) + 10)
                    if i > nnzut:
                        AltVert = float(n2 / nnzut) * i
                    if i < nnzut:
                        AltVert = float(n2 / nnzut) * (i + 1)
                    import math
                    AncVert = n1 / ((3.1416) * (math.atan((AltVert / nazut) ** 0.5)))
                    versutro = AncVert * 2
                    QpromVert = float(2.08 * (((AltVert / 100) + (2/3)) * a1))

                    i+=1

                    AltVert = round(AltVert,2)
                    AncVert = round(AncVert,2)
                    versutro = round(versutro,2)
                    QpromVert = round(QpromVert,2)

                    Label(frameverto, text="Altura en cm:", font =("Time new roman", 13), fg = "black").grid(pady=5, row=0, column=0,)
                    Label(frameverto, text="Ancho en cm:", font =("Time new roman", 13), fg = "black").grid(pady=5, row=0, column=1,)
                    Label(frameverto, text="Vertedor propocional en cm:", font =("Time new roman", 13), fg = "black").grid(pady=5, row=0, column=2,)
                    Label(frameverto, text="Caudal en m^3/s:", font =("Time new roman", 13), fg = "black").grid(pady=5, row=0, column=3)

                    e = Entry(frameverto, width = 20, font =("Time new roman", 11), relief=FLAT)
                    e.grid(pady=3, padx=3, row=i+1, column=j, sticky=S+N+E+W)
                    e.insert(END, '%f' % AltVert)
                    cols.append(e)
                    j+=1
                    e = Entry(frameverto, width = 20, font =("Time new roman", 11), relief=FLAT)
                    e.grid(pady=3, padx=3, row=i+1, column=j, sticky=S+N+E+W)
                    e.insert(END, '%f' % AncVert)
                    cols.append(e)
                    j+=1
                    e = Entry(frameverto, width = 20, font =("Time new roman", 11), relief=FLAT)
                    e.grid(pady=3, padx=3, row=i+1, column=j, sticky=S+N+E+W)
                    e.insert(END, '%f' % versutro)
                    cols.append(e)
                    j+=1
                    e = Entry(frameverto, width = 20, font =("Time new roman", 11), relief=FLAT)
                    e.grid(pady=3, padx=3, row=i+1, column=j, sticky=S+N+E+W)
                    e.insert(END, '%f' % QpromVert)
                    cols.append(e)
                    j = 0
                    rows.append(cols)

                    frameVertezto = Frame(root9, width = 737, height = 150, bd = 2, relief = RIDGE)
                    frameVertezto.place(x = 15, y = 300)

                    QHa = float(b1 * ((2 * a1 * 9.81) ** 0.5) * ((H1 + 2) / (3 * a1)))
                    QhA = float((0.66) * b1 *((2 * 9.81) ** (0.5)) * (((H1 + a1) ** (1.5)) - (H1 ** (0.66))))

                    QHa = round(QHa,2)
                    QhA = round(QhA,2)

                    etiqueta17 = Label(frameVertezto, text = "Caudal cuando el tirante es mayor en m^3/s:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                    #etiqueta17 = Label(frameVertezto, text = "Caudal cuando el tirante es menor:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 70)

                    entQ = DoubleVar()
                    entQ.set(QHa)
                    entQ1 = DoubleVar()
                    #entQ1.set(QhA)

                    txtQ = Entry(frameVertezto, textvariable = entQ, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
                #txtQ1 = Entry(frameVertezto, textvariable = entQ1, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)

        def respzanja():

            Qprommd = float((Qproml * 86400) / 1000)

            if zanja.get() == 1:

                root10 = Toplevel(root)
                root10.geometry("1050x600+0+0")
                root10.title("Resultados de la zanja orbal")

                nSoZaor = float(entSoZanor.get())
                nFcZaor = float(entFcZanor.get())
                nPaZaor = float(entPa.get())
                nTZaor = float(entrTempro.get())
                nCZaor = float(entCZanor.get())
                nAsupZaor = float(entAsupZanor.get())
                nHZaor = float(entHZanor.get())
                nSZaor = float(entSZanor.get())
                nvalorZaor = float(valorZanor.get())
                nPoblZaor = float(entrPob.get())

                if nvalorZaor > 1:
                    messagebox.showinfo(title = "Zanjas", message = "Dimensiones por Zanja")

                QpromZor = float(Qprommd / nvalorZaor)
                PoblZor = float(nPoblZaor / nvalorZaor)
                VtZor = float((QpromZor * nSoZaor) / (0.1 * 3000))
                TRHZor= float((VtZor / QpromZor) * 24)
                DBOaZor = float(nFcZaor * PoblZor * 0.001)
                OrZor = float(DBOaZor * 2)
                Cs3Zor = float((8.36 * nPaZaor) / 760)
                NZor = float(6 * 0.82 * (1.024 ) ** (nTZaor - 20) * (0.9 * Cs3Zor - nCZaor) / 9.17)
                N2Zor = float(24*NZor)
                LcZor = float((OrZor / N2Zor) * 2.5)
                COVZor = float((DBOaZor * 1000) / QpromZor)
                DiaZor =float(nAsupZaor * 2)
                AsZor =float(3.1416 * (nAsupZaor * nAsupZaor))
                PxZor = float(0.5 * ( nSoZaor - nSZaor) * QpromZor * 0.001)
                PoZor = float(NZor * 2 * 24)
                OcZor = float((3000 * VtZor * 0.001) / PxZor)

                VtZor = round(VtZor,2)
                TRHZor = round(TRHZor,2)
                DBOaZor = round(DBOaZor,2)
                OrZor = round(OrZor,2)
                Cs3Zor = round(Cs3Zor,2)
                NZor = round(NZor,2)
                LcZor = round(LcZor,2)
                COVZor = round(COVZor,2)
                DiaZor = round(DiaZor,2)
                AsZor = round(AsZor,2)
                PxZor = round(PxZor,2)
                PoZor = round(PoZor,2)
                OcZor = round(OcZor,2)

                czanor = conn.cursor()

                zoordb = """
                CREATE TABLE IF NOT EXISTS zanja_orbal (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                VtZor FLOAT NOT NULL,
                TRHZor FLOAT NOT NULL,
                DBOaZor FLOAT NOT NULL,
                OrZor  FLOAT NOT NULL,
                Cs3Zor FLOAT NOT NULL,
                NZor FLOAT NOT NULL,
                LcZor FLOAT NOT NULL,
                COVZor FLOAT NOT NULL,
                DiaZor FLOAT NOT NULL,
                AsZor FLOAT NOT NULL,
                PxZor FLOAT NOT NULL,
                PoZor FLOAT NOT NULL,
                OcZor FLOAT NOT NULL)"""

                czanor.execute(zoordb)

                argzanor = (VtZor, TRHZor, DBOaZor, OrZor, Cs3Zor, NZor, LcZor, COVZor, DiaZor, AsZor, PxZor, PoZor, OcZor)

                zanorconec = """
                INSERT INTO zanja_orbal (VtZor, TRHZor, DBOaZor, OrZor, Cs3Zor, NZor, LcZor, COVZor, DiaZor, AsZor, PxZor, PoZor, OcZor)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"""

                czanor.execute(zanorconec,argzanor)

                conn.commit ()

                czanor.close ()

                framezanjaorbalto = LabelFrame(root10, text = "Dimensiones de la zanja orbal", width = 1000, height = 550, bd = 2, relief = RIDGE)
                framezanjaorbalto.place(x = 20, y = 15)

                etiqueta138 = Label(framezanjaorbalto, text = "Volumen total del reactor en m^3:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta139 = Label(framezanjaorbalto, text = "Tiempo de retención hidrálica en horas:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta140 = Label(framezanjaorbalto, text = "Carga orgánica aplicada en kgDBO/Día:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 140)
                etiqueta141 = Label(framezanjaorbalto, text = "Oxígeno requerido en kgO2/Día:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 210)
                etiqueta142 = Label(framezanjaorbalto, text = "Concentración de saturación de O2 disuelto en mg/L:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 280)
                etiqueta143 = Label(framezanjaorbalto, text = "Capacidad real de transferencia de O2 del cepillo en kgO2/m*h:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 350)
                etiqueta144 = Label(framezanjaorbalto, text = "Largo del cepillo en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 420)
                etiqueta145 = Label(framezanjaorbalto, text = "Carga orgánica volumetrica en grDBO/m^3:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 10)
                etiqueta150 = Label(framezanjaorbalto, text = "Diámetro en m:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 70)
                etiqueta150 = Label(framezanjaorbalto, text = "Área superficial en m^2:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 140)
                etiqueta151 = Label(framezanjaorbalto, text = "Producción de lodos en ggSS/día:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 210)
                etiqueta152 = Label(framezanjaorbalto, text = "Producción de oxígeno en el cepillo en KgO2/d:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 280)
                etiqueta153 = Label(framezanjaorbalto, text = "Edad de lodos en días:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 350)

                global entAsZor
                global entDiaZor
                global entLcZor

                entVtZor = DoubleVar()
                entVtZor.set(VtZor)
                entTRHZor = DoubleVar()
                entTRHZor.set(TRHZor)
                entDBOaZor = DoubleVar()
                entDBOaZor.set(DBOaZor)
                entOrZor = DoubleVar()
                entOrZor.set(OrZor)
                entCs3Zor = DoubleVar()
                entCs3Zor.set(Cs3Zor)
                entNZor = DoubleVar()
                entNZor.set(NZor)
                entLcZor = DoubleVar()
                entLcZor.set(LcZor)
                entCOVZor = DoubleVar()
                entCOVZor.set(COVZor)
                entDiaZor = DoubleVar()
                entDiaZor.set(DiaZor)
                entAsZor = DoubleVar()
                entAsZor.set(AsZor)
                entPxZor = DoubleVar()
                entPxZor.set(PxZor)
                entPoZor = DoubleVar()
                entPoZor.set(PoZor)
                entOcZor = DoubleVar()
                entOcZor.set(OcZor)

                txtVtZor = Entry(framezanjaorbalto, textvariable = entVtZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
                txtTRHZor = Entry(framezanjaorbalto, textvariable = entTRHZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
                txtDBOaZor = Entry(framezanjaorbalto, textvariable = entDBOaZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 165)
                txtOrZor = Entry(framezanjaorbalto, textvariable = entOrZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 235)
                txtCs3Zor = Entry(framezanjaorbalto, textvariable = entCs3Zor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 305)
                txtNZor = Entry(framezanjaorbalto, textvariable = entNZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 375)
                txtLcZor = Entry(framezanjaorbalto, textvariable = entLcZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 445)
                txtCOVZor = Entry(framezanjaorbalto, textvariable = entCOVZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 35)
                txtDiaZor = Entry(framezanjaorbalto, textvariable = entDiaZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 95)
                txtAsZor = Entry(framezanjaorbalto, textvariable = entAsZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 165)
                txtPxZor = Entry(framezanjaorbalto, textvariable = entPxZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 235)
                txtPoZor = Entry(framezanjaorbalto, textvariable = entPoZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 305)
                txtOcZor = Entry(framezanjaorbalto, textvariable = entOcZor, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 375)

            elif zanja.get() == 2:

                root10 = Toplevel(root)
                root10.geometry("1050x700+0+0")
                root10.title("Resultados de la zanja isla")

                nSoZanis = float(entSoZanis.get())
                nFcZanis = float(entFcZanis.get())
                nPaZanis = float(entPa.get())
                nTZanis = float(entrTempro.get())
                nCZanis = float(entCZanis.get())
                nAsupZanis = float(entAsupZanis.get())
                nHZanis = float(entHZanis.get())
                nSZanis = float(entSZanis.get())
                nvalorZanis = float(valorZanis.get())
                nPoblZanis = float(entrPob.get())

                if nvalorZanis > 1:
                    messagebox.showinfo(title = "Zanjas", message = "Dimensiones por Zanja")

                QpromZanis = float(Qprommd / nvalorZanis)
                PoblZanis = float(nPoblZanis / nvalorZanis)
                VtZanis = float((QpromZanis * nSoZanis) / (0.1 * 3000))
                TRHZanis = float((VtZanis / QpromZanis) * 24)
                DBOaZanis = float(nFcZanis * PoblZanis * 0.001)
                OrZanis = float(DBOaZanis * 2)
                Cs3Zanis = float((8.36 * nPaZanis) / 760)
                NZanis = float(6 * 0.82 * (1.024 ) ** (nTZanis - 20) * (0.9 * Cs3Zanis - nCZanis) / 9.17)
                N2Zanis = float(24 * NZanis)
                LcZanis = float(OrZanis / N2Zanis)
                COVZanis = float((DBOaZanis * 1000) / QpromZanis)
                Vc1Zanis = float(3.1416 * (nAsupZanis ** 2) / nHZanis)
                Vc2Zanis = float(3.1416 * ((nAsupZanis - nHZanis) ** 2) / nHZanis)
                VtronZanis = float(Vc1Zanis - Vc2Zanis)
                VrZanis = float(VtZanis - VtronZanis)
                LsrZanis = float(VrZanis / (((nAsupZanis * 2) / 2) * nHZanis * 2))
                LeZanis = float(LsrZanis + (2 * nAsupZanis))
                AsZanis = float((LeZanis * (nAsupZanis * 2)) * nvalorZanis)
                PxZanis = float(0.5 * ( nSoZanis - nSZanis) * QpromZanis * 0.001)
                PoZanis = float(NZanis * 2 * 24)
                OcZanis = float((3000 * VtZanis * 0.001) / PxZanis)

                VtZanis = round(VtZanis,2)
                TRHZanis = round(TRHZanis,2)
                DBOaZanis = round(DBOaZanis,2)
                OrZanis = round(OrZanis,2)
                Cs3Zanis = round(Cs3Zanis,2)
                NZanis = round(NZanis,2)
                LcZanis = round(LcZanis,2)
                COVZanis = round(COVZanis,2)
                VcZanis = round(VtronZanis,2)
                VrZanis = round(VrZanis,2)
                LsrZanis = round(LsrZanis,2)
                LeZanis = round(LeZanis,2)
                AsZanis = round(AsZanis,2)
                PxZanis = round(PxZanis,2)
                PoZanis = round(PoZanis,2)
                OcZanis = round(OcZanis,2)

                czani= conn.cursor()

                zopidb = """
                CREATE TABLE IF NOT EXISTS zanja_oxidacion_isla (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                VtZanis FLOAT NOT NULL,
                TRHZanis FLOAT NOT NULL,
                DBOaZanis FLOAT NOT NULL,
                OrZanis  FLOAT NOT NULL,
                Cs3Zanis FLOAT NOT NULL,
                NZanis FLOAT NOT NULL,
                LcZanis FLOAT NOT NULL,
                COVZanis FLOAT NOT NULL,
                VcZanis FLOAT NOT NULL,
                VrZanis  FLOAT NOT NULL,
                LsrZanis FLOAT NOT NULL,
                LeZanis FLOAT NOT NULL,
                AsZanis FLOAT NOT NULL,
                PxZanis FLOAT NOT NULL,
                PoZanis FLOAT NOT NULL,
                OcZanis FLOAT NOT NULL)"""

                czani.execute(zopidb)

                argzani = (VtZanis, TRHZanis, DBOaZanis, OrZanis, Cs3Zanis, NZanis, LcZanis, COVZanis, VcZanis, VrZanis, LsrZanis, LeZanis, AsZanis, PxZanis, PoZanis, OcZanis)

                zaniconec = """
                INSERT INTO zanja_oxidacion_isla (VtZanis, TRHZanis, DBOaZanis, OrZanis, Cs3Zanis, NZanis, LcZanis, COVZanis, VcZanis, VrZanis, LsrZanis, LeZanis, AsZanis, PxZanis, PoZanis, OcZanis)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

                czani.execute(zaniconec, argzani)

                conn.commit()

                czani.close()

                framezanjaislato = LabelFrame(root10, text = "Dimensiones de la zanja pared isla", width = 1000, height = 670, bd = 2, relief = RIDGE)
                framezanjaislato.place(x = 20, y = 15)

                etiqueta138 = Label(framezanjaislato, text = "Volumen total del reactor en m^3:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta139 = Label(framezanjaislato, text = "Tiempo de retención hidráulica en Horas:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta140 = Label(framezanjaislato, text = "Carga orgánica aplicada en KgDBO/día:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 140)
                etiqueta141 = Label(framezanjaislato, text = "Oxígeno requerido en kgO2/día:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 210)
                etiqueta142 = Label(framezanjaislato, text = "Concentración de saturación de O2 disuelto en mg/L:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 280)
                etiqueta143 = Label(framezanjaislato, text = "Capacidad real de transferencia de O2 del cepillo en kgO2/m*h:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 350)
                etiqueta144 = Label(framezanjaislato, text = "Largo del cepillo en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 420)
                etiqueta145 = Label(framezanjaislato, text = "Carga orgánica volumetrica en grDBO/m3:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 490)
                etiqueta146 = Label(framezanjaislato, text = "Volumen de la sección curva en m^3:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 10)
                etiqueta147 = Label(framezanjaislato, text = "Volumen de la sección recta en m^3:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 70)
                etiqueta148 = Label(framezanjaislato, text = "Longitud de la sección recta en m:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 140)
                etiqueta149 = Label(framezanjaislato, text = "Longitud efectiva en m:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 210)
                etiqueta150 = Label(framezanjaislato, text = "Área superficial en m^2: ", font =("Time new roman", 13), fg = "black").place(x = 620, y = 280)
                etiqueta151 = Label(framezanjaislato, text = "Producción de lodos en KgSS/día:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 350)
                etiqueta152 = Label(framezanjaislato, text = "Producción de oxígeno en el cepillo KgO2/d:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 420)
                etiqueta153 = Label(framezanjaislato, text = "Edad de lodos en días:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 490)

                global entAszis
                global entLsrzis
                global entLczis

                entVt = DoubleVar()
                entVt.set(VtZanis)
                entTRH = DoubleVar()
                entTRH.set(TRHZanis)
                entDBOa = DoubleVar()
                entDBOa.set(DBOaZanis)
                entOr = DoubleVar()
                entOr.set(OrZanis)
                entCs3 = DoubleVar()
                entCs3.set(Cs3Zanis)
                entN = DoubleVar()
                entN.set(NZanis)
                entLczis = DoubleVar()
                entLczis.set(LcZanis)
                entCOV = DoubleVar()
                entCOV.set(COVZanis)
                entVc = DoubleVar()
                entVc.set(VcZanis)
                entVr = DoubleVar()
                entVr.set(VrZanis)
                entLsrzis = DoubleVar()
                entLsrzis.set(LsrZanis)
                entLe = DoubleVar()
                entLe.set(LeZanis)
                entAszis = DoubleVar()
                entAszis.set(AsZanis)
                entPx = DoubleVar()
                entPx.set(PxZanis)
                entPo = DoubleVar()
                entPo.set(PoZanis)
                entOc = DoubleVar()
                entOc.set(OcZanis)

                txtVt = Entry(framezanjaislato, textvariable = entVt, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
                txtTRH = Entry(framezanjaislato, textvariable = entTRH, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 90)
                txtDBOa = Entry(framezanjaislato, textvariable = entDBOa, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 165)
                txtOr = Entry(framezanjaislato, textvariable = entOr, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 235)
                txtCs3 = Entry(framezanjaislato, textvariable = entCs3, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 305)
                txtN = Entry(framezanjaislato, textvariable = entN, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 375)
                txtLc = Entry(framezanjaislato, textvariable = entLczis, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 445)
                txtCOV = Entry(framezanjaislato, textvariable = entCOV, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 515)
                txtVc = Entry(framezanjaislato, textvariable = entVc, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 35)
                txtVr = Entry(framezanjaislato, textvariable = entVr, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y= 90)
                txtLsr = Entry(framezanjaislato, textvariable = entLsrzis, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 165)
                txtLe = Entry(framezanjaislato, textvariable = entLe, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y= 235)
                txtAs = Entry(framezanjaislato, textvariable = entAszis, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 305)
                txtPx = Entry(framezanjaislato, textvariable = entPx, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 375)
                txtPo = Entry(framezanjaislato, textvariable = entPo, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 445)
                txtOc = Entry(framezanjaislato, textvariable = entOc, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 515)
            elif zanja.get() == 3:

                root10 = Toplevel(root)
                root10.geometry("1050x700+0+0")
                root10.title("Resultados de la zanja recta")

                nSoZarec = float(entSoZanrec.get())
                nFcZarec = float(entFcZanrec.get())
                nPaZarec = float(entPa.get())
                nTZarec = float(entrTempro.get())
                nCZarec = float(entCZanrec.get())
                nAsupZarec = float(entAsupZanrec.get())
                nHZarec = float(entHZanrec.get())
                nSZarec = float(entSZanrec.get())
                nvalorZarec = float(valorZanrec.get())
                nPoblZarec = float(entrPob.get())

                if nvalorZarec > 1:
                    messagebox.showinfo(title = "Zanjas", message = "Dimensiones por Zanja")

                QpromZanr = float(Qprommd / nvalorZarec)
                PoblZanr = float(nPoblZarec / nvalorZarec)
                VtZar = float((QpromZanr * nSoZarec) / (0.1 * 3000))
                TRHZar= float((VtZar / QpromZanr) * 24)
                DBOaZar = float(nFcZarec * PoblZanr * 0.001)
                OrZar = float(DBOaZar * 2)
                Cs3Zar = float((8.36 * nPaZarec) / 760)
                NZar = float(6 * 0.82 * (1.024 ) ** (nTZarec - 20) * (0.9 * Cs3Zar - nCZarec) / 9.17)
                N2Zar = float(24*NZar)
                LcZar = float(OrZar / N2Zar)
                COVZar = float((DBOaZar * 1000) / QpromZanr)
                VcZar = float(3.1416 * (nAsupZarec ** 2) * nHZarec)
                VrZar = float(VtZar - VcZar)
                LsrZar = float(VrZar / (((nAsupZarec * 2) / 2) * nHZarec))
                LeZar = float(LsrZar + (2 * nAsupZarec))
                AsZar = float(LeZar * (nAsupZarec * 2))
                PxZar = float(0.5 * ( nSoZarec - nSZarec) * QpromZanr * 0.001)
                PoZar = float(NZar * 2 * 24)
                OcZar = float((3000 * VtZar * 0.001) / PxZar)
                DeflZan = float(nAsupZarec / 2)

                VtZan = round(VtZar,2)
                TRHZan = round(TRHZar,2)
                DBOaZan = round(DBOaZar,2)
                OrZan = round(OrZar,2)
                Cs3Zan = round(Cs3Zar,2)
                NZan = round(NZar,2)
                LcZan = round(LcZar,2)
                COVZan = round(COVZar,2)
                VcZan = round(VcZar,2)
                VrZan = round(VrZar,2)
                LsrZan = round(LsrZar,2)
                LeZan = round(LeZar,2)
                AsZan = round(AsZar,2)
                PxZan = round(PxZar,2)
                PoZan = round(PoZar,2)
                OcZan = round(OcZar,2)

                czanre = conn.cursor()

                zordb = """
                CREATE TABLE IF NOT EXISTS zanja_oxidacion_recta (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                VtZan FLOAT NOT NULL,
                TRHZan FLOAT NOT NULL,
                DBOaZan FLOAT NOT NULL,
                OrZan  FLOAT NOT NULL,
                Cs3Zan FLOAT NOT NULL,
                NZan FLOAT NOT NULL,
                LcZan FLOAT NOT NULL,
                COVZan FLOAT NOT NULL,
                VcZan FLOAT NOT NULL,
                VrZan  FLOAT NOT NULL,
                LsrZan FLOAT NOT NULL,
                LeZan FLOAT NOT NULL,
                AsZan FLOAT NOT NULL,
                PxZan FLOAT NOT NULL,
                PoZan FLOAT NOT NULL,
                OcZan FLOAT NOT NULL,
                DeflZan FLOAT NOT NULL)"""

                czanre.execute(zordb)

                argzanre = (VtZan, TRHZan, DBOaZan, OrZan, Cs3Zan, NZan, LcZan, COVZan, VcZan, VrZan, LsrZan, LeZan, AsZan, PxZan, PoZan, OcZan, DeflZan)

                zanreconec = """
                INSERT INTO zanja_oxidacion_recta (VtZan, TRHZan, DBOaZan, OrZan, Cs3Zan, NZan, LcZan, COVZan, VcZan, VrZan, LsrZan, LeZan, AsZan, PxZan, PoZan, OcZan, DeflZan)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

                czanre.execute(zanreconec, argzanre)

                conn.commit()

                czanre.close()

                framezanjarectato = LabelFrame(root10, text = "Dimensiones de la zanja recta", width = 1000, height = 670, bd = 2, relief = RIDGE)
                framezanjarectato.place(x = 20, y = 15)

                etiqueta138 = Label(framezanjarectato, text = "Volumen total del reactor en m^3:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta139 = Label(framezanjarectato, text = "Tiempo de retención hidrálica en horas:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta140 = Label(framezanjarectato, text = "Carga orgánica aplicada en grDBO/día:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 140)
                etiqueta141 = Label(framezanjarectato, text = "Oxígeno requerido en kgO2/día:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 210)
                etiqueta142 = Label(framezanjarectato, text = "Concentración de saturación de O2 en mg/L:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 280)
                etiqueta143 = Label(framezanjarectato, text = "Capacidad real de transferencia de O2 del cepillo en KgO2/m*h:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 350)
                etiqueta144 = Label(framezanjarectato, text = "Largo del cepillo en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 420)
                etiqueta145 = Label(framezanjarectato, text = "Carga orgánica volumentrica en grDBO/m^3:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 490)
                etiqueta146 = Label(framezanjarectato, text = "Volumen de la sección curva en m^3:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 560)
                etiqueta147 = Label(framezanjarectato, text = "Volumen de la sección recta en m^3:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 10)
                etiqueta148 = Label(framezanjarectato, text = "Longitud requerida en m:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 70)
                etiqueta149 = Label(framezanjarectato, text = "Longitud efectiva en m:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 140)
                etiqueta150 = Label(framezanjarectato, text = "Área superficial en m^2:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 210)
                etiqueta151 = Label(framezanjarectato, text = "Producción de lodos en KgSS/día:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 280)
                etiqueta152 = Label(framezanjarectato, text = "Producción de oxigeno en el cepillo en KgO2/d:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 350)
                etiqueta153 = Label(framezanjarectato, text = "Edad de lodos en días:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 420)
                etiqueta154 = Label(framezanjarectato, text = "Deflector en m:", font =("Time new roman", 13), fg = "black").place(x = 620, y = 490)

                global entAszr
                global entLsrzr
                global entLczr

                entVt = DoubleVar()
                entVt.set(VtZan)
                entTRH = DoubleVar()
                entTRH.set(TRHZan)
                entDBOa = DoubleVar()
                entDBOa.set(DBOaZan)
                entOr = DoubleVar()
                entOr.set(OrZan)
                entCs3 = DoubleVar()
                entCs3.set(Cs3Zan)
                entN = DoubleVar()
                entN.set(NZan)
                entLczr = DoubleVar()
                entLczr.set(LcZan)
                entCOV = DoubleVar()
                entCOV.set(COVZan)
                entVc = DoubleVar()
                entVc.set(VcZan)
                entVr = DoubleVar()
                entVr.set(VrZan)
                entLsrzr = DoubleVar()
                entLsrzr.set(LsrZan)
                entLe = DoubleVar()
                entLe.set(LeZan)
                entAszr = DoubleVar()
                entAszr.set(AsZan)
                entPx = DoubleVar()
                entPx.set(PxZan)
                entPo = DoubleVar()
                entPo.set(PoZan)
                entOc = DoubleVar()
                entOc.set(OcZan)
                entDefl = DoubleVar()
                entDefl.set(DeflZan)

                txtVt = Entry(framezanjarectato, textvariable = entVt, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
                txtTRH = Entry(framezanjarectato, textvariable = entTRH, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
                txtDBOa = Entry(framezanjarectato, textvariable = entDBOa, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 165)
                txtOr = Entry(framezanjarectato, textvariable = entOr, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 235)
                txtCs3 = Entry(framezanjarectato, textvariable = entCs3, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 305)
                txtN = Entry(framezanjarectato, textvariable = entN, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 375)
                txtLc = Entry(framezanjarectato, textvariable = entLczr, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 445)
                txtCOV = Entry(framezanjarectato, textvariable = entCOV, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 515)
                txtVc = Entry(framezanjarectato, textvariable = entVc, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 585)
                txtVr = Entry(framezanjarectato, textvariable = entVr, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y= 35)
                txtLsr = Entry(framezanjarectato, textvariable = entLsrzr, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 95)
                txtLe = Entry(framezanjarectato, textvariable = entLe, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y= 165)
                txtAs = Entry(framezanjarectato, textvariable = entAszr, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 235)
                txtPx = Entry(framezanjarectato, textvariable = entPx, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 305)
                txtPo = Entry(framezanjarectato, textvariable = entPo, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 375)
                txtOc = Entry(framezanjarectato, textvariable = entOc, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 445)
                txtDefl = Entry(framezanjarectato, textvariable = entDefl, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 620, y = 515)
            elif zanja.get() == 4:

                root10 = Toplevel(root)
                root10.geometry("1380x550+0+0")
                root10.title("Resultados de la zanja herradura")

                nSoZah = float(entSoZanherr.get())
                nFcZah = float(entFcZanherr.get())
                nPaZah = float(entPa.get())
                nTZah = float(entrTempro.get())
                nCZah = float(entCZanherr.get())
                nAsupZah = float(entAsupZanherr.get())
                nHZah = float(entHZanherr.get())
                nSZah = float(entSZanherr.get())
                nvalorZah = float(valorZanherr.get())
                nPoblZah = float(entrPob.get())

                if nvalorZah > 1:
                    messagebox.showinfo(title = "Zanjas", message = "Dimensiones por Zanja")

                QpromZah = float(Qprommd / nvalorZah)
                PoblZah = float(nPoblZah / nvalorZah)
                VtZah = float((QpromZah * nSoZah) / (0.1 * 3000))
                TRHZah= float((VtZah / QpromZah) * 24)
                DBOaZah = float(nFcZah * PoblZah * 0.001)
                OrZah = float(DBOaZah * 2)
                Cs3Zah = float((8.36 * nPaZah) / 760)
                NZah = float(6 * 0.82 * (1.024 ) ** (nTZah - 20) * (0.9 * Cs3Zah - nCZah) / 9.17)
                N2Zah = float(24 * NZah)
                LcZah = float(OrZah / N2Zah)
                COVZah = float((DBOaZah * 1000) / QpromZah)
                VcZah = float(3.1416 * (nAsupZah ** 2) * nHZah)
                VrZah = float(VtZah - VcZah)
                LsrZah = float(VrZah / (((nAsupZah/2)* nHZah) * 2))
                LeZah = float(LsrZah + (2 * nAsupZah))
                AsZah = float((LeZah * ((nAsupZah + nAsupZah)* 2)))
                AsctZah = float(VcZah / nHZah)
                AscmZah = float (AsctZah / 2)
                AsccZah = float (AscmZah / 2)
                PxZah = float(0.5 * ( nSoZah - nSZah) * QpromZah * 0.001)
                PoZah = float(NZah * 2 * 24)
                OcZah = float((3000 * VtZah * 0.001) / PxZah)
                DeflZah = float(nAsupZah / 2)

                VtZah = round(VtZah,2)
                TRHZah = round(TRHZah,2)
                DBOaZah = round(DBOaZah,2)
                OrZah = round(OrZah,2)
                Cs3Zah = round(Cs3Zah,2)
                NZah = round(NZah,2)
                LcZah = round(LcZah,2)
                COVZah = round(COVZah,2)
                VcZah = round(VcZah,2)
                VrZah = round(VrZah,2)
                LsrZah = round(LsrZah,2)
                LeZah = round(LeZah,2)
                AscmZah = round(AscmZah,2)
                AsccZah = round(AsccZah,2)
                AsZah = round(AsZah,2)
                PxZah = round(PxZah,2)
                PoZah = round(PoZah,2)
                OcZah = round(OcZah,2)

                czanhe = conn.cursor()

                zohedb = """
                CREATE TABLE IF NOT EXISTS zanja_herradura (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                VtZah FLOAT NOT NULL,
                TRHZah FLOAT NOT NULL,
                DBOaZah FLOAT NOT NULL,
                OrZah  FLOAT NOT NULL,
                Cs3Zah FLOAT NOT NULL,
                NZah FLOAT NOT NULL,
                LcZah FLOAT NOT NULL,
                COVZah FLOAT NOT NULL,
                VcZah FLOAT NOT NULL,
                VrZah  FLOAT NOT NULL,
                LsrZah FLOAT NOT NULL,
                LeZah FLOAT NOT NULL,
                AsctZah FLOAT NOT NULL,
                AscmZah FLOAT NOT NULL,
                AsccZah FLOAT NOT NULL,
                AsZah FLOAT NOT NULL,
                PxZah FLOAT NOT NULL,
                PoZah FLOAT NOT NULL,
                OcZah FLOAT NOT NULL)"""

                czanhe.execute(zohedb)

                argzanhe = (VtZah, TRHZah, DBOaZah, OrZah, Cs3Zah, NZah, LcZah, COVZah, VcZah, VrZah, LsrZah, LeZah, AsctZah, AscmZah, AsccZah, AsZah, PxZah, PoZah, OcZah)

                zanheconec = """
                INSERT INTO zanja_herradura (VtZah, TRHZah, DBOaZah, OrZah, Cs3Zah, NZah, LcZah, COVZah, VcZah, VrZah, LsrZah, LeZah, AsctZah, AscmZah, AsccZah, AsZah, PxZah, PoZah, OcZah)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

                czanhe.execute(zanheconec, argzanhe)

                conn.commit()

                czanhe.close()

                framezanjaherraduto = Frame(root10, width = 1310, height = 500, bd = 2, relief = RIDGE)
                framezanjaherraduto.place(x = 20, y = 15)

                etiqueta138 = Label(framezanjaherraduto, text = "Volumen total del reactor en m^3:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta139 = Label(framezanjaherraduto, text = "Tiempo de retención hidráulica en horas:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta140 = Label(framezanjaherraduto, text = "Carga orgánica aplicada en kgDBO/día:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 140)
                etiqueta141 = Label(framezanjaherraduto, text = "Oxígeno requerido en kgO2/día:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 210)
                etiqueta142 = Label(framezanjaherraduto, text = "Concentración de saturación de O2 en mg/L:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 280)
                etiqueta143 = Label(framezanjaherraduto, text = "Capacidad real de transferencia de O2 del cepillo en KgO2/m*h:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 350)
                etiqueta144 = Label(framezanjaherraduto, text = "Largo del cepillo en m: ", font =("Time new roman", 13), fg = "black").place(x = 580, y = 10)
                etiqueta145 = Label(framezanjaherraduto, text = "Carga orgánica volumetrica en grDBO/m^3:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 70)
                etiqueta146 = Label(framezanjaherraduto, text = "Volumen de la sección curva en m3:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 140)
                etiqueta147 = Label(framezanjaherraduto, text = "Volumen de la sección recta en m3:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 210)
                etiqueta148 = Label(framezanjaherraduto, text = "Longitud requerida en m:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 280)
                etiqueta149 = Label(framezanjaherraduto, text = "Longitud efectiva en m:", font =("Time new roman", 13), fg = "black").place(x = 580, y = 350)
                etiqueta1501 = Label(framezanjaherraduto, text = "Área de la sección curva en m^2:", font =("Time new roman", 13), fg = "black").place(x = 930, y = 10)
                etiqueta1502 = Label(framezanjaherraduto, text = "Área de la sección curva chica en m^2:", font =("Time new roman", 13), fg = "black").place(x = 930, y = 70)
                etiqueta150 = Label(framezanjaherraduto, text = "Área superficial en m^2:", font =("Time new roman", 13), fg = "black").place(x = 930, y = 140)
                etiqueta151 = Label(framezanjaherraduto, text = "Producción de lodos en kgSS/día:", font =("Time new roman", 13), fg = "black").place(x = 930, y = 210)
                etiqueta152 = Label(framezanjaherraduto, text = "Producción de oxígeno en el cepillo en KgO2/d:", font =("Time new roman", 13), fg = "black").place(x = 930, y = 280)
                etiqueta153 = Label(framezanjaherraduto, text = "Edad de lodos en días:", font =("Time new roman", 13), fg = "black").place(x = 930, y = 350)

                global entAsher
                global entLsrher
                global entLcher

                entVther = DoubleVar()
                entVther.set(VtZah)
                entTRHher = DoubleVar()
                entTRHher.set(TRHZah)
                entDBOaher = DoubleVar()
                entDBOaher.set(DBOaZah)
                entOrher = DoubleVar()
                entOrher.set(OrZah)
                entCs3her = DoubleVar()
                entCs3her.set(Cs3Zah)
                entNher = DoubleVar()
                entNher.set(NZah)
                entLcher = DoubleVar()
                entLcher.set(LcZah)
                entCOVher = DoubleVar()
                entCOVher.set(COVZah)
                entVcher = DoubleVar()
                entVcher.set(VcZah)
                entVrher = DoubleVar()
                entVrher.set(VrZah)
                entLsrher = DoubleVar()
                entLsrher.set(LsrZah)
                entLeher = DoubleVar()
                entLeher.set(LeZah)
                entAscher = DoubleVar()
                entAscher.set(AscmZah)
                entAsccher = DoubleVar()
                entAsccher.set(AsccZah)
                entAsher = DoubleVar()
                entAsher.set(AsZah)
                entPxher = DoubleVar()
                entPxher.set(PxZah)
                entPoher = DoubleVar()
                entPoher.set(PoZah)
                entOcher = DoubleVar()
                entOcher.set(OcZah)

                txtVt = Entry(framezanjaherraduto, textvariable = entVther, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
                txtTRH = Entry(framezanjaherraduto, textvariable = entTRHher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
                txtDBOa = Entry(framezanjaherraduto, textvariable = entDBOaher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 165)
                txtOr = Entry(framezanjaherraduto, textvariable = entOrher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 235)
                txtCs3 = Entry(framezanjaherraduto, textvariable = entCs3her, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 305)
                txtN = Entry(framezanjaherraduto, textvariable = entNher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 375)
                txtLc = Entry(framezanjaherraduto, textvariable = entLcher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 35)
                txtCOV = Entry(framezanjaherraduto, textvariable = entCOVher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 95)
                txtVc = Entry(framezanjaherraduto, textvariable = entVcher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 165)
                txtVr = Entry(framezanjaherraduto, textvariable = entVrher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y= 235)
                txtLsr = Entry(framezanjaherraduto, textvariable = entLsrher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y = 305)
                txtLe = Entry(framezanjaherraduto, textvariable = entLeher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 580, y= 375)
                txtAscher = Entry(framezanjaherraduto, textvariable = entAscher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 930, y = 35)
                txtAsccher = Entry(framezanjaherraduto, textvariable = entAsccher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 930, y = 95)
                txtAs = Entry(framezanjaherraduto, textvariable = entAsher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 930, y = 165)
                txtPx = Entry(framezanjaherraduto, textvariable = entPxher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 930, y = 235)
                txtPo = Entry(framezanjaherraduto, textvariable = entPoher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 930, y = 305)
                txtOc = Entry(framezanjaherraduto, textvariable = entOcher, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 930, y = 375)

        def continuar3():
            respuesta = askquestion(title = "Guardar y continuar proceso", message= "¿Desea y guardar antes de continuar?")
            if respuesta == "yes":
                if zanja.get()== 1:
                    Áreazc = str(entAsZor.get())
                    Diametrozc = str(entDiaZor.get())
                    Largocepizc = str(entLcZor.get())
                    Profundidadzc = str(entHZanor.get())
                    txtozac = ("\n\nLas dimensiones de la zanja orbal resultantes fueron:\nÁrea superficial:\t\t"+Áreazc+"\tm^2\nDiametro:\t\t\t"+Diametrozc+"\tm\nLargo del cepillo:\t\t"+Largocepizc+"\tm\nProfundidad:\t\t\t"+Profundidadzc+"\tm")
                    archivo = open(file,"a")
                    archivo.write(txtozac)
                    archivo.close()
                elif zanja.get()==2:
                    Áreazi = str(entAszis.get())
                    Longitudefectzi = str(entLsrzis.get())
                    Largocepizi = str(entLczis.get())
                    Profundidadzi = str(entHZanis.get())
                    txtozai = ("\n\nLas dimensiones de la zanja isla resultantes fueron:\nÁrea superficial:\t\t"+Áreazi+"\tm^2\nLongitud de la zanja:\t\t"+Longitudefectzi+"\tm\nLargo del cepillo:\t\t"+Largocepizi+"\tm\nProfundidad:\t\t\t"+Profundidadzi+"\tm")
                    archivo = open(file,"a")
                    archivo.write(txtozai)
                    archivo.close()
                elif zanja.get()==3:
                    Áreazr = str(entAszr.get())
                    Longitudefectzr = str(entLsrzr.get())
                    Largocepizr = str(entLczr.get())
                    Profundidadzr = str(entHZanrec.get())
                    txtozar = ("\n\nLas dimensiones de la zanja recta resultantes fueron:\nÁrea superficial:\t\t"+Áreazr+"\tm^2\nLongitud de la zanja:\t\t"+Longitudefectzr+"\tm\nLargo del cepillo:\t\t"+Largocepizr+"\tm\nProfundidad:\t\t\t"+Profundidadzr+"\tm")
                    archivo = open(file,"a")
                    archivo.write(txtozar)
                    archivo.close()
                elif zanja.get()==4:
                    Áreazh = str(entAsher.get())
                    Longitudefectzh = str(entLsrher.get())
                    Largocepizh = str(entLcher.get())
                    Profundidadzh = str(entHZanherr.get())
                    txtozah = ("\n\nLas dimensiones de la zanja herradura resultantes fueron:\nÁrea superficial:\t\t"+Áreazh+"\tm^2\nLongitud de la zanja:\t\t"+Longitudefectzh+"m\nLargo del cepillo:\t\t"+Largocepizh+"\tm\nProfundidad:\t\t\t"+Profundidadzh+"\tm")
                    archivo = open(file,"a")
                    archivo.write(txtozah)
                    archivo.close()

            def croquislodos():
                rootcl = Toplevel(root)
                rootcl.geometry("1005x338+0+0")
                rootcl.title("Esquema de las eras de secado y el tanque de cloración")

                lbleras = Label(rootcl, image = erasSecado).place(x = 0, y = 0)

            def respclora():
                root14 = Toplevel(root)
                root14.geometry("700x350+0+0")
                root14.title("Resultados del tanque de cloración")

                Qprommd = float((Qproml * 86400)/1000)

                nTRHTan = float(entTRHTandiges.get())
                nHTan = float(entHTandiges.get())
                nFvaTan = float(entFvaTandiges.get())
                n5 = float(entDclTandiges.get())
                nClactTan= float(entClactTandiges.get())

                TRHTan = float(nTRHTan / 1440)
                TRHTan = round(TRHTan,8)

                VeTan = float((Qprommd * TRHTan)/ 10)
                VrTan = float(VeTan * nFvaTan)
                AsTan = float(VrTan / nHTan)
                AncdTan = float((AsTan ** 0.5) / 2)
                LdTan = float(AncdTan * 2)
                STan = float(LdTan * 0.25)
                DsTan = float(((Qprommd * 2) / nClactTan) / 10)

                VeTan = round(VeTan,2)
                VrTan = round(VrTan,2)
                AsTan = round(AsTan,2)
                AncdTan = round(AncdTan,2)
                LdTan = round(LdTan,2)
                STan = round(STan,2)
                WTan = round(DsTan,2)

                cerclo= conn.cursor()

                tcdb = """
                CREATE TABLE IF NOT EXISTS tanque_cloracion (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                VeTan FLOAT NOT NULL,
                VrTan FLOAT NOT NULL,
                AsTan FLOAT NOT NULL,
                AncdTan  FLOAT NOT NULL,
                LdTan FLOAT NOT NULL,
                STan FLOAT NOT NULL,
                WTan FLOAT NOT NULL)"""

                cerclo.execute(tcdb)

                argclo = (VeTan, VrTan, AsTan, AncdTan, LdTan, STan, WTan)

                cloconec = """
                INSERT INTO tanque_cloracion (VeTan, VrTan, AsTan, AncdTan, LdTan, STan, WTan)
                VALUES (?,?,?,?,?,?,?)"""

                cerclo.execute(cloconec, argclo)

                conn.commit ()

                cerclo.close()

                framecloracionto = LabelFrame(root14, text = "Dimensiones del tanque de cloración", width = 650, height = 300, bd = 2, relief = RIDGE)
                framecloracionto.place(x = 20, y = 15)

                etiqueta117 = Label(framecloracionto, text = "Volumen efectivo en m^3:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta118 = Label(framecloracionto, text = "Volumen requerido en m^3:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta119 = Label(framecloracionto, text = "Área superficial en m^2:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 140)
                etiqueta120 = Label(framecloracionto, text = "Ancho de la cámara en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 210)
                etiqueta121 = Label(framecloracionto, text = "Largo de la cámara en m:", font =("Time new roman", 13), fg = "black").place(x = 320, y = 10)
                etiqueta122 = Label(framecloracionto, text = "Longitud de intersección en m:", font =("Time new roman", 13), fg = "black").place(x = 320, y = 70)
                etiqueta123 = Label(framecloracionto, text = "Dosis de ClO- en gr de ClO-/día:", font =("Time new roman", 13), fg = "black").place(x = 320, y = 140)

                global entAsTan
                global entLdTan
                global entSTan
                global entAncdTan

                entVeTan = DoubleVar()
                entVeTan.set(VeTan)
                entVrTan = DoubleVar()
                entVrTan.set(VrTan)
                entAsTan = DoubleVar()
                entAsTan.set(AsTan)
                entAncdTan = DoubleVar()
                entAncdTan.set(AncdTan)
                entLdTan = DoubleVar()
                entLdTan.set(LdTan)
                entSTan = DoubleVar()
                entSTan.set(STan)
                entWTan = DoubleVar()
                entWTan.set(WTan)

                txtVeTan = Entry(framecloracionto, textvariable = entVeTan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
                txtVrTan = Entry(framecloracionto, textvariable = entVrTan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
                txtAsTan = Entry(framecloracionto, textvariable = entAsTan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 165)
                txtAncdTan = Entry(framecloracionto, textvariable = entAncdTan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 235)
                txtLdTan = Entry(framecloracionto, textvariable = entLdTan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 320, y= 35)
                txtSTan = Entry(framecloracionto, textvariable = entSTan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 320, y = 95)
                txtWTan = Entry(framecloracionto, textvariable = entWTan, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 320, y = 165)

            def resperas():
                root12 = Toplevel(root)
                root12.geometry("350x350+0+0")
                root12.title("Resultado de las eras")

                nPlsSec = float(entPlsSec.get())
                nTRHSec = int(entTRHSec.get())
                nECPSec = float(entECPSec.get())
                nAncSec = int(entAncSec.get())
                nvalorSec = int(valorSec.get())

                VnSec = float((poblacion * nPlsSec * nTRHSec) / 1000)
                AsSec = float(VnSec / nECPSec)
                if nvalorSec >1:
                    AsSec = float((VnSec / nECPSec) / nvalorSec)
                    messagebox.showinfo(title = "Área superficial", message = "Área superficial por era")
                LSec = float ((AsSec / nAncSec) / nvalorSec)

                VnSec = round(VnSec,2)
                AsSec = round(AsSec,2)
                LSec = round(LSec,2)

                ceras= conn.cursor()

                ersdb = """
                CREATE TABLE IF NOT EXISTS eras_secado (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                VnSec FLOAT NOT NULL,
                AsSec FLOAT NOT NULL,
                LSec FLOAT NOT NULL)"""

                ceras.execute(ersdb)

                argeras = (VnSec, AsSec, LSec)

                erasconec = """
                INSERT INTO eras_secado (VnSec, AsSec, LSec)
                VALUES (?,?,?)"""

                ceras.execute(erasconec, argeras)

                conn.commit ()

                ceras.close()

                frameerasto = LabelFrame(root12, text = "Dimensión de las eras de secado", width = 300, height = 300, bd = 2, relief = RIDGE)
                frameerasto.place(x = 20, y = 15)

                etiqueta118 = Label(frameerasto, text = "Volumen en m^3:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta118 = Label(frameerasto, text = "Área superficial en m^2:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta118 = Label(frameerasto, text = "Largo de cada era en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 140)

                global entAsSec
                global entLSec

                entVnSec = DoubleVar()
                entVnSec.set(VnSec)
                entAsSec = IntVar()
                entAsSec.set(AsSec)
                entLSec = DoubleVar()
                entLSec.set(LSec)

                txtVn = Entry(frameerasto, textvariable = entVnSec, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 35)
                txtAs = Entry(frameerasto, textvariable = entAsSec, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
                txtL = Entry(frameerasto, textvariable = entLSec, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 165)

            def respsedi():
                root11 = Toplevel(root)
                root11.geometry("500x500+0+0")
                root11.title("Resultado del sedimentador")

                Qprommd = float((Qproml * 86400) / 1000)

                nvalorZan = float(valorZan.get())
                nCsSed = float(entCsSed.get())

                Qprom = float(Qprommd / nvalorZan)
                AsSed = float(Qprom / nCsSed)
                DSed = float(math.sqrt((4 * AsSed) / 3.1416))
                VSed = float((3 * Qprom * 2) / 24)
                HSed = float(VSed / AsSed)
                TRHSed = float(VSed / Qprom)
                TRHSed = float(TRHSed * 24)

                AsSed = round(AsSed,2)
                DSed = round(DSed,2)
                TRHSed = round(TRHSed,2)
                HSed = round(HSed,2)
                VSed = round(VSed,2)

                csed= conn.cursor()

                sdcdb = """
                CREATE TABLE IF NOT EXISTS sedimentador_circular (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                AsSed FLOAT NOT NULL,
                DSed FLOAT NOT NULL,
                VSed FLOAT NOT NULL,
                HSed  FLOAT NOT NULL,
                TRHSed FLOAT NOT NULL)"""

                csed.execute(sdcdb)

                argsed = (AsSed, DSed, VSed, HSed, TRHSed)

                sedconec = """
                INSERT INTO sedimentador_circular (AsSed, DSed, VSed, HSed, TRHSed)
                VALUES (?,?,?,?,?)"""

                csed.execute(sedconec, argsed)

                conn.commit ()

                csed.close()

                framesedimento = LabelFrame(root11, text= "Dimensión del sedimentador secundario", width = 450, height = 450, bd = 2, relief = RIDGE)
                framesedimento.place(x = 20, y = 15)

                etiqueta116 = Label(framesedimento, text = "Área superficial del sedimentador en m^2: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta117 = Label(framesedimento, text = "Diámetro del tanque en m: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta118 = Label(framesedimento, text = "Volumen del tanque en m^3: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 140)
                etiqueta119 = Label(framesedimento, text = "Profundidad en m: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 210)
                etiqueta120 = Label(framesedimento, text = "Tiempo de retención hidrálica en horas:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 280)

                global entAsSed
                global entDSed
                global entHSed

                entAsSed = DoubleVar()
                entAsSed.set(AsSed)
                entDSed = DoubleVar()
                entDSed.set(DSed)
                entVSed = DoubleVar()
                entVSed.set(VSed)
                entHSed = DoubleVar()
                entHSed.set(HSed)
                entTHRSed = DoubleVar()
                entTHRSed.set(TRHSed)

                txtAs = Entry(framesedimento, textvariable = entAsSed, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 35)
                txtD = Entry(framesedimento, textvariable = entDSed, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 95)
                txtV = Entry(framesedimento, textvariable = entVSed, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y= 165)
                txtH = Entry(framesedimento, textvariable = entHSed, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 235)
                txtTRH = Entry(framesedimento, textvariable = entTHRSed, width = 20, font =("Time new roman", 11), relief=FLAT, state=DISABLED).place(x = 20, y = 305)

            def continuar4():
                respuesta = askquestion(title = "Guardar y finalizar proceso", message= "¿Desea guardar y finalizar?")
                if respuesta == "yes":
                    Áreasd = str(entAsSed.get())
                    Diametrosd = str(entDSed.get())
                    Profundidadsd = str(entHSed.get())
                    txtozsd = ("\n\nLas dimensiones del sedimentador resultantes fueron:\nÁrea superficial:\t\t"+Áreasd+"\tm^2\nDiametro:\t\t\t"+Diametrosd+"\tm\nProfundidad:\t\t\t"+Profundidadsd+"\tm")
                    archivo = open(file,"a")
                    archivo.write(txtozsd)
                    archivo.close()

                    Áreaer = str(entAsSec.get())
                    Largoer = str(entLSec.get())
                    txtoer = ("\n\nLas dimensiones de las eras resultantes fueron:\nÁrea superficial:\t\t"+Áreaer+"\tm^2\nLargo:\t\t\t\t"+Largoer+"\tm")
                    archivo = open(file,"a")
                    archivo.write(txtoer)
                    archivo.close()

                    Áreaclo = str(entAsTan.get())
                    Largoclo = str(entLdTan.get())
                    Seccionclo = str(entSTan.get())
                    Anchoclo = str(entAncdTan.get())
                    txtoclo = ("\n\nLas dimensiones de tanque de cloracion resultantes fueron:\nÁrea superficial:\t\t"+Áreaclo+"\tm^2\nLargo:\t\t\t\t"+Largoclo+"\tm\nSección:\t\t\t"+Seccionclo+"\tm\nAncho:\t\t\t\t"+Anchoclo+"\tm")
                    archivo = open(file,"a")
                    archivo.write(txtoclo)
                    archivo.close()

                    messagebox.showinfo(title ="Diseño terminado", message = "Ha concluido su diseño exitosamente. Puede ver sus dimensiones en el archivo creado al comienzo")


            def framesedimentador():

                frameSed = LabelFrame(pesClora, text = "Datos del sedimentador secundario", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
                frameSed.place(x = 20, y = 15)

                etiqueta115 = Label(frameSed, text = "Carga sedimentable en m^3/m^2*día ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta139 = Label(frameSed, text = "Número de zanjas:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)

                global entCsSed
                global valorZan

                entCsSed = IntVar()
                entCsSed.set(20)

                valorZan = IntVar(value = 1)
                Nzscor = Spinbox(frameSed, from_=1, to=4, width= 3, textvariable = valorZan).place(x = 164, y = 73)

                txtCs = Entry(frameSed, textvariable = entCsSed, width = 20, font =("Time new roman", 11)).place(x = 20, y = 35)

                botonrsed = Button(frameSed, command = respsedi, text = "Ver resultado del sedimentador circular", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 235, y = 223)

            def frameras():

                frameerasda = LabelFrame(pesClora, text = "Datos de diseño de las eras de secado", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
                frameerasda.place(x = 520, y = 15)

                etiqueta115 = Label(frameerasda, text = "Distribución de capas en m: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta117 = Label(frameerasda, text = "Ancho de cada era en m: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta116 = Label(frameerasda, text = "Número de eras: ", font =("Time new roman", 13), fg = "black").place(x = 280, y = 10)
                etiqueta113 = Label(frameerasda, text = "Producción de lodo seco en L/hab*día:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 130)
                etiqueta114 = Label(frameerasda, text = "Edad de lodos en días: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 200)

                global entECPSec
                global entAncSec
                global valorSec
                global entPlsSec
                global entTRHSec

                entECPSec = DoubleVar()
                entECPSec.set(0.20)
                entAncSec = DoubleVar()
                entPlsSec = DoubleVar()
                entPlsSec.set(0.1)
                entTRHSec = IntVar()
                entTRHSec.set(30)

                valorSec = IntVar(value = 1)
                erasva = Spinbox(frameerasda, textvariable = valorSec, from_=1, to=10, width= 3).place(x = 407, y = 13)

                txtECP = Entry(frameerasda, textvariable = entECPSec, width = 20, font =("Time new roman", 11)).place(x = 20, y = 35)
                txtAnc = Entry(frameerasda, textvariable = entAncSec, width = 20, font =("Time new roman", 11)).place(x = 20, y= 95)
                txtPls = Entry(frameerasda, textvariable = entPlsSec, width = 20, font =("Time new roman", 11)).place(x = 20, y = 155)
                txtTRH = Entry(frameerasda, textvariable = entTRHSec, width = 20, font =("Time new roman", 11)).place(x = 20, y= 225)

                botonreras = Button(frameerasda, command = resperas, text = "Ver resultado de las eras", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 320, y = 223)

            def framecloracion():

                framecloracda = LabelFrame(pesClora, text = "Datos de diseño del tanque de cloración", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
                framecloracda.place(x = 20, y = 310)

                etiqueta113 = Label(framecloracda, text = "Profundidad en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta114 = Label(framecloracda, text = "Factor de volumen adicional:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
                etiqueta112 = Label(framecloracda, text = "Tiempo de retención hidráulica en minutos:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 130)

                global entTRHTandiges
                global entFvaTandiges
                global entHTandiges

                entTRHTandiges = DoubleVar()
                entFvaTandiges = DoubleVar()
                entFvaTandiges.set(1.5)
                entHTandiges = DoubleVar()

                txtH = Entry(framecloracda, textvariable = entHTandiges, width = 20, font =("Time new roman", 11)).place(x = 20, y= 35)
                txtFva = Entry(framecloracda, textvariable = entFvaTandiges, width = 20, font =("Time new roman", 11)).place(x = 20, y = 95)
                txtTRH = Entry(framecloracda, textvariable = entTRHTandiges, width = 20, font =("Time new roman", 11)).place(x = 20, y = 155)

                frametancloracio = LabelFrame(pesClora, text = "Datos de la cloración en el tanque", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
                frametancloracio.place(x = 520, y = 310)

                etiqueta115 = Label(frametancloracio, text = "Dosis de ClO- en g/m^3: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
                etiqueta116 = Label(frametancloracio, text = "Contenido en fracción de Cl: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)

                global entDclTandiges
                global entClactTandiges

                entDclTandiges = IntVar()
                entDclTandiges.set(2)
                entClactTandiges = DoubleVar()
                entClactTandiges.set(65)

                txtDcl = Entry(frametancloracio, textvariable = entDclTandiges, width = 20, font =("Time new roman", 11)).place(x = 20, y = 35)
                txtClact = Entry(frametancloracio, textvariable = entClactTandiges, width = 20, font =("Time new roman", 11)).place(x = 20, y = 95)

                botoncs = tk.Button(frametancloracio, command = croquislodos, image = Croquis)
                botoncs["border"] = "0"
                botoncs.place(x = 390, y = 10)

                botonrestanq = Button(frametancloracio, command = respclora, text = "Ver resultado del tanque de cloración", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 50, y = 235)
                botoncroquiss = Button(frametancloracio, command = continuar4, text = "Finalizar y guardar", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 290, y = 235)

            if lodo.get() == 1:
                notebook.add(pesClora, text = "Sedimentador, tratamiento de lodos y tanque de cloración", state="normal")

                framesedimentador()
                frameras()
                framecloracion()

        frameVer = LabelFrame(pesVert, text = "Datos del vertedor sutro", width = 500, height = 295, bd = 2, relief =  RIDGE, font =("Time new roman", 11))
        frameVer.place(x = 20, y = 15)

        etiqueta11 = Label(frameVer,text = "Altura minima en cm: ", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 10)
        etiqueta12 = Label(frameVer, text = "Ancho de la mitad de", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 80)
        etiqueta12 = Label(frameVer, text = "la base en cm:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 100)
        etiqueta11 = Label(frameVer,text = "Carga del vertedor en cm: ", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 170)
        etiqueta14 = Label(frameVer, text = "Número de secciones: ", font = ("Time new roman", 13), fg = "black").place(x = 270, y = 10)

        enta = DoubleVar()
        enta.set(10)
        entAnchZut = DoubleVar()
        entHZut = DoubleVar()
        entn = IntVar()

        txta = Entry(frameVer, textvariable = enta, width = 20, font =("Time new roman", 11)).place(x = 20, y = 35)
        txtb = Entry(frameVer, textvariable = entAnchZut, width = 20, font =("Time new roman", 11)).place(x = 20, y = 120)
        txtH = Entry(frameVer, textvariable = entHZut, width = 20, font =("Time new roman", 11)).place(x = 20, y= 195)
        txtn = Entry(frameVer, textvariable = entn, width = 20, font =("Time new roman", 11)).place(x = 270, y = 35)

        botonresvert = Button(frameVer, command = respvertedor, text = "Ver resultado del vertedor sutro", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 290, y = 215)

        if zanja.get() == 1:

            framezandatosdiseor = LabelFrame(pesVert, text = "Datos de diseño de zanja orbal", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosdiseor.place(x = 520, y = 15)

            etiqueta126 = Label(framezandatosdiseor, text = "Radio en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta128 = Label(framezandatosdiseor, text = "Profundidad en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
            etiqueta139 = Label(framezandatosdiseor, text = "Número de zanjas:", font =("Time new roman", 13), fg = "black").place(x = 280, y = 10)

            global valorZanor
            global entAsupZanor
            global entHZanor

            valorZanor = IntVar(value = 1)
            Nzscor = Spinbox(framezandatosdiseor, from_=1, to=4, width= 3, textvariable = valorZanor).place(x = 422, y = 13)

            entAsupZanor = IntVar()
            entHZanor = DoubleVar()

            txtAsupor = Entry(framezandatosdiseor, textvariable = entAsupZanor, width = 20, font =("Time new roman", 11)).place(x = 20, y = 35)
            txtHor = Entry(framezandatosdiseor, textvariable = entHZanor, width = 20, font =("Time new roman", 11)).place(x = 20, y = 95)

            framezandatosenflu = LabelFrame(pesVert, text = "Datos dentro del zanjón orbal", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosenflu.place(x = 20, y = 310)

            etiqueta137 = Label(framezandatosenflu, text = "Concentración de O2 disuelto ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta137 = Label(framezandatosenflu, text = "en el zanjón en mg/L: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 35)
            etiqueta138 = Label(framezandatosenflu, text = "Calidad del efluente según la norma: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 105)

            global entCZanor
            global entSZanor

            entCZanor = DoubleVar()
            entCZanor.set(1.5)
            entSZanor = DoubleVar()
            entSZanor.set(30)

            txtC = Entry(framezandatosenflu, textvariable = entCZanor, width = 20, font =("Time new roman", 11)).place(x = 20, y = 57)
            txtS = Entry(framezandatosenflu, textvariable = entSZanor, width = 20, font =("Time new roman", 11)).place(x = 20, y = 130)

            framezandatosinflu = LabelFrame(pesVert, text = "Carga contaminante en la zanja orbal", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosinflu.place(x = 520, y = 310)

            etiqueta123 = Label(framezandatosinflu, text = "Factor de carga contaminante", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta123 = Label(framezandatosinflu, text = "en DBO/hab*día: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 35)
            etiqueta129 = Label(framezandatosinflu, text = "Concentración de DBO en mg/L: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 105)

            global entFcZanor
            global entSoZanor

            entFcZanor = DoubleVar()
            entSoZanor = IntVar()

            txtFc = Entry(framezandatosinflu, textvariable = entFcZanor, width = 20, font =("Time new roman", 11)).place(x = 20, y = 57)
            txtSo = Entry(framezandatosinflu, textvariable = entSoZanor, width = 20, font =("Time new roman", 11)).place(x = 20, y= 130)

            botonc = tk.Button(framezandatosinflu, command = croquiszanjas, image = Croquis)
            botonc["border"] = "0"
            botonc.place(x = 390, y = 10)

            botonresorbal = Button(framezandatosinflu, command = respzanja, text = "Ver resultado de la zanja orbal", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 50, y = 235)
            botoncont3 = Button(framezandatosinflu, command = continuar3, text = "Continuar proceso", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 290, y = 235)
        elif zanja.get() == 2:

            framezandatosdiseisla = LabelFrame(pesVert, text = "Datos de diseño de la zanja pared isla", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosdiseisla.place(x = 520, y = 15)

            etiqueta126 = Label(framezandatosdiseisla, text = "Ancho superficial en m: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta127 = Label(framezandatosdiseisla, text = "Profundidad en m: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
            etiqueta139 = Label(framezandatosdiseisla, text = "Número de zanjas: ", font =("Time new roman", 13), fg = "black").place(x = 250, y = 10)
            etiqueta140=Label(framezandatosdiseisla, text = "Ancho de la isla: ", font =("Time new roman", 13), fg = "black").place(x = 250, y = 70)

            global valorZanis
            global entAsupZanis
            global entHZanis

            valorZanis = IntVar(value = 1)
            Nzs = Spinbox(framezandatosdiseisla, from_=1, to=4, width= 3, textvariable = valorZanis).place(x = 393, y = 13)
            valorPared= IntVar(value = 1)
            Anis = Spinbox(framezandatosdiseisla, from_=0.5, to=2.5, increment = 0.5, width= 3, textvariable = valorPared).place(x = 380, y = 73)

            entAsupZanis = IntVar()
            entHZanis = DoubleVar()

            txtAsupis = Entry(framezandatosdiseisla, textvariable = entAsupZanis, width = 20, font =("Time new roman", 11)).place(x = 20, y = 35)
            txtHis = Entry(framezandatosdiseisla, textvariable = entHZanis, width = 20, font =("Time new roman", 11)).place(x = 20, y = 95)

            framezandatosenflu = LabelFrame(pesVert, text = "Datos dentro del zanjón isla", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosenflu.place(x = 20, y = 310)

            etiqueta137 = Label(framezandatosenflu, text = "Concentración de O2 disuelto ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta137 = Label(framezandatosenflu, text = "en el zanjón en mg/L: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 35)
            etiqueta138 = Label(framezandatosenflu, text = "Calidad del efluente según la norma: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 105)

            global entCZanis
            global entSZanis

            entCZanis = DoubleVar()
            entCZanis.set(1.5)
            entSZanis = DoubleVar()
            entSZanis.set(30)

            txtC = Entry(framezandatosenflu, textvariable = entCZanis, width = 20, font =("Time new roman", 11)).place(x = 20, y = 57)
            txtS = Entry(framezandatosenflu, textvariable = entSZanis, width = 20, font =("Time new roman", 11)).place(x = 20, y = 130)

            framezandatosinflu = LabelFrame(pesVert, text = "Carga contaminante en la zanja isla", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosinflu.place(x = 520, y = 310)

            etiqueta123 = Label(framezandatosinflu, text = "Factor de carga contaminante", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta123 = Label(framezandatosinflu, text = "en DBO/hab*día: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 35)
            etiqueta129 = Label(framezandatosinflu, text = "Concentración de DBO en mg/L: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 105)

            global entFcZanis
            global entSoZanis

            entFcZanis = DoubleVar()
            entSoZanis = IntVar()

            txtFc = Entry(framezandatosinflu, textvariable = entFcZanis, width = 20, font =("Time new roman", 11)).place(x = 20, y = 57)
            txtSo = Entry(framezandatosinflu, textvariable = entSoZanis, width = 20, font =("Time new roman", 11)).place(x = 20, y= 130)

            botonc = tk.Button(framezandatosinflu, command = croquiszanjas, image = Croquis)
            botonc["border"] = "0"
            botonc.place(x = 390, y = 10)

            botonresisla = Button(framezandatosinflu, command = respzanja, text = "Ver resultado de la zanja isla", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 50, y = 235)
            botoncont3 = Button(framezandatosinflu, command = continuar3, text = "Continuar proceso", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 290, y = 235)
        elif zanja.get() == 3:

            framezandatosdiserec = LabelFrame(pesVert, text = "Datos de diseño de la zanja recta", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosdiserec.place(x = 520, y = 15)

            etiqueta126 = Label(framezandatosdiserec, text = "Ancho superficial en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta128 = Label(framezandatosdiserec, text = "Profundidad en m:", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
            etiqueta139 = Label(framezandatosdiserec, text = "Número de zanjas:", font =("Time new roman", 13), fg = "black").place(x = 250, y = 10)

            global valorZanrec
            global entAsupZanrec
            global entHZanrec

            valorZanrec = IntVar(value = 1)
            Nzsrec = Spinbox(framezandatosdiserec, from_=1, to=4, width= 3, textvariable = valorZanrec).place(x = 393, y = 13)

            entAsupZanrec = IntVar()
            entHZanrec = DoubleVar()

            txtAsuprec = Entry(framezandatosdiserec, textvariable = entAsupZanrec, width = 20, font =("Time new roman", 11)).place(x = 20, y = 35)
            txtHrec = Entry(framezandatosdiserec, textvariable = entHZanrec, width = 20, font =("Time new roman", 11)).place(x = 20, y = 95)

            framezandatosenflu = LabelFrame(pesVert, text = "Datos dentro del zanjón recto", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosenflu.place(x = 20, y = 310)

            etiqueta137 = Label(framezandatosenflu, text = "Concentración de O2 disuelto ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta137 = Label(framezandatosenflu, text = "en el zanjón en mg/L: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 35)
            etiqueta138 = Label(framezandatosenflu, text = "Calidad del efluente según la norma: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 105)

            global entCZanrec
            global entSZanrec

            entCZanrec = DoubleVar()
            entCZanrec.set(1.5)
            entSZanrec = DoubleVar()
            entSZanrec.set(30)

            txtC = Entry(framezandatosenflu, textvariable = entCZanrec, width = 20, font =("Time new roman", 11)).place(x = 20, y = 57)
            txtS = Entry(framezandatosenflu, textvariable = entSZanrec, width = 20, font =("Time new roman", 11)).place(x = 20, y = 130)

            framezandatosinflu = LabelFrame(pesVert, text = "Carga contaminante en la zanja recta", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosinflu.place(x = 520, y = 310)

            etiqueta123 = Label(framezandatosinflu, text = "Factor de carga contaminante", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta123 = Label(framezandatosinflu, text = "en DBO/hab*día: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 35)
            etiqueta129 = Label(framezandatosinflu, text = "Concentración de DBO en mg/L: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 105)

            global entFcZanrec
            global entSoZanrec

            entFcZanrec = DoubleVar()
            entSoZanrec = IntVar()

            txtFc = Entry(framezandatosinflu, textvariable = entFcZanrec, width = 20, font =("Time new roman", 11)).place(x = 20, y = 57)
            txtSo = Entry(framezandatosinflu, textvariable = entSoZanrec, width = 20, font =("Time new roman", 11)).place(x = 20, y= 130)

            botonc = tk.Button(framezandatosinflu, command = croquiszanjas, image = Croquis)
            botonc["border"] = "0"
            botonc.place(x = 390, y = 10)

            botonresorbal = Button(framezandatosinflu, command = respzanja, text = "Ver resultado de la zanja recta", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 50, y = 235)
            botoncont3 = Button(framezandatosinflu, command = continuar3, text = "Continuar proceso", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 290, y = 235)
        elif zanja.get() == 4:

            framezandatosdiseherr = LabelFrame(pesVert, text = "Datos de diseño de zanja herradura", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosdiseherr.place(x = 520, y = 15)

            etiqueta126 = Label(framezandatosdiseherr, text = "Ancho superficial en m: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta128 = Label(framezandatosdiseherr, text = "Profundidad en m: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
            etiqueta139 = Label(framezandatosdiseherr, text = "Número de zanjas: ", font =("Time new roman", 13), fg = "black").place(x = 250, y = 10)

            global valorZanherr
            global entAsupZanherr
            global entHZanherr

            valorZanherr = IntVar(value = 1)
            Nzsrecherr = Spinbox(framezandatosdiseherr, from_=1, to=4, width= 3, textvariable = valorZanherr).place(x = 393, y = 13)

            entAsupZanherr = IntVar()
            entHZanherr = DoubleVar()

            txtAsupherr = Entry(framezandatosdiseherr, textvariable = entAsupZanherr, width = 20, font =("Time new roman", 11)).place(x = 20, y = 35)
            txtHherr = Entry(framezandatosdiseherr, textvariable = entHZanherr, width = 20, font =("Time new roman", 11)).place(x = 20, y = 95)

            framezandatosenflu = LabelFrame(pesVert, text = "Datos dentro del zanjón herradura", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosenflu.place(x = 20, y = 310)

            etiqueta137 = Label(framezandatosenflu, text = "Concentración de O2 disuelto ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta137 = Label(framezandatosenflu, text = "en el zanjón en mg/L: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 35)
            etiqueta138 = Label(framezandatosenflu, text = "Calidad del efluente según la norma: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 105)

            global entCZanherr
            global entSZanherr

            entCZanherr = DoubleVar()
            entCZanherr.set(1.5)
            entSZanherr = DoubleVar()
            entSZanherr.set(30)

            txtC = Entry(framezandatosenflu, textvariable = entCZanherr, width = 20, font =("Time new roman", 11)).place(x = 20, y = 57)
            txtS = Entry(framezandatosenflu, textvariable = entSZanherr, width = 20, font =("Time new roman", 11)).place(x = 20, y = 130)

            framezandatosinflu = LabelFrame(pesVert, text = "Carga contaminante en la zanja herradura", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
            framezandatosinflu.place(x = 520, y = 310)

            etiqueta123 = Label(framezandatosinflu, text = "Factor de carga contaminante", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
            etiqueta123 = Label(framezandatosinflu, text = "en DBO/hab*día: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 35)
            etiqueta129 = Label(framezandatosinflu, text = "Concentración de DBO en mg/L: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 105)

            global entFcZanherr
            global entSoZanherr

            entFcZanherr = DoubleVar()
            entSoZanherr = IntVar()

            txtFc = Entry(framezandatosinflu, textvariable = entFcZanherr, width = 20, font =("Time new roman", 11)).place(x = 20, y = 57)
            txtSo = Entry(framezandatosinflu, textvariable = entSoZanherr, width = 20, font =("Time new roman", 11)).place(x = 20, y= 130)

            botoncz = tk.Button(framezandatosinflu, command = croquiszanjas, image = Croquis)
            botoncz["border"] = "0"
            botoncz.place(x = 390, y = 10)

            botonresorbal = Button(framezandatosinflu, command = respzanja, text = "Ver resultado de la zanja herradura", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 50, y = 235)
            botoncont3 = Button(framezandatosinflu, command = continuar3, text = "Continuar proceso", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 290, y = 235)

    framecan = LabelFrame(pesPre, text = "Datos del canal de llegada", width = 500, height = 295, bd = 2, relief = RIDGE, font =("Time new roman", 11))
    framecan.place(x = 20, y = 310)

    etiqueta18pulg = Label(framecan, text = "Ancho de tuberia remitente:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 10)
    etiqueta19 = Label(framecan, text = "Velocidad de agua remitente m/s:", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 75)
    etiqueta20 = Label(framecan, text = "Coeficiente de Manning: ", font = ("Time new roman", 13), fg = "black").place(x = 20, y = 135)

    global mett

    mett = IntVar()
    metros = Radiobutton(framecan, text = "Metros",  width = 10, font =("Time new roman", 12), variable = mett, value = 1).place(x = 220, y = 10)
    pulgadas = Radiobutton(framecan, text = "Pulgadas",  width = 10, font =("Time new roman", 12), variable = mett, value = 2).place(x = 340, y = 10)

    entrAnctu = DoubleVar()
    entrV = DoubleVar()
    entrV.set(1.4)
    entrn = DoubleVar()
    entrn.set(0.013)

    txtAnctu = Entry(framecan,textvariable = entrAnctu, width = 20, font =("Time new roman", 11)).place(x = 20, y = 35)
    txtV = Entry(framecan, textvariable = entrV, width = 20, font =("Time new roman", 11)).place(x = 20, y = 97)
    txtn = Entry(framecan,textvariable = entrn, width = 20, font =("Time new roman", 11), state='disabled').place(x = 20, y = 157)

    botonresrej = Button(framecan, command = respcanal, text = "Ver resultado del canal de llegada", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 270, y = 225)

    frameDesa = LabelFrame(pesPre, text = "Datos del desarenador", width = 500, height = 295, bd = 2, relief =  RIDGE, font =("Time new roman", 11))
    frameDesa.place(x = 520, y = 310)

    etiqueta150 = Label(frameDesa, text = "Propuesta de limpieza en días: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
    etiqueta151 = Label(frameDesa, text = "Ajuste para el largo del canal: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 80)

    entPl = IntVar()
    entPl.set(3)

    valorLg = IntVar(value = 3)
    Lg = Spinbox(frameDesa, from_=3, to=5, width= 5, font =("Time new roman", 10), textvariable = valorLg).place(x = 240, y = 83)

    txtPl = Entry(frameDesa, textvariable = entPl, width = 20).place(x = 20, y= 35)

    botonc = tk.Button(frameDesa, command = croquiscarca, image = Croquis)
    botonc["border"] = "0"
    botonc.place(x = 390, y = 10)

    botonresdes = Button(frameDesa, command = respdesare, text = "Ver resultado del desarenador", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 90, y = 225)
    botoncont2 = Button(frameDesa, command = continuar2, text = "Continuar proceso", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 320, y = 225)

frameestados = LabelFrame(pesambient, text ="Datos del proyecto", width = 350, height = 300, bd = 2, relief = RIDGE, font =("Time new roman", 11))
frameestados.place(x = 20, y = 15)

lstedos = ttk.Combobox(frameestados, state="readonly")
lstedos.place(x = 20, y = 35)

lstedos['values'] = ('Aguascalientes','Baja California','Baja California Sur','Campeche', 'Chiapas', 'Chihuahua', 'Ciudad de México', 'Coahuila', 'Colima', 'Durango', 'Estado de México', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán', 'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán', 'Zacatecas')

Edo = Label(frameestados, text = "Elija el estado", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
MSNM = Label(frameestados, text = "Altura sobre el nivel del mar", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
Temperatura = Label(frameestados, text = "Temperatura promedio en °C", font =("Time new roman", 13), fg = "black").place(x = 20, y = 130)
Prebaro = Label(frameestados, text = "Presión barométrica en mmHg: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 190)

global entrMSNM
global entrTempro
global entPa

entrMSNM = IntVar()
entrTempro = DoubleVar()
entPa = DoubleVar()

txtMSNM = Entry(frameestados, textvariable = entrMSNM, width = 20, font =("Time new roman", 11), ).place(x = 20, y = 95)
txtTprom = Entry(frameestados, textvariable = entrTempro, width = 20, font =("Time new roman", 11), ).place(x = 20, y = 155)
txtPa = Entry(frameestados, textvariable = entPa, width = 20, font =("Time new roman", 11), ).place(x = 20, y= 215)

def ubicacion():

    if lstedos.get() == 'Aguascalientes':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Aguascalientes", message = "Altura máxima: Cerro Ardilla con 3,050 m\nAltura mínima: Río Calvillo con 1,550 m.")
    elif lstedos.get() == 'Baja California':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Baja California", message = "Altura máxima: Sierra San Pedro Mártir con 3,050 m\nAltura mínima: Laguna Salada con -10 m.")
    elif lstedos.get() == 'Baja California Sur':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Baja California Sur", message = "Altura máxima: Sierra La Laguna con 2,080 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Campeche':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Campeche", message = "Altura máxima: Cerro Champerico con 380 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Chiapas':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Chiapas", message = "Altura máxima: Volcán Tacaná con 3,284 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Chihuahua':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Chihuahua", message = "Altura máxima: Guadalupe y Calvo con 3,293 m\nAltura mínima: Río Mohinora con 580 m.")
    elif lstedos.get() == 'Ciudad de México':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Ciudad de México", message = "Altura máxima: Cerro la Cruz del Marqués (Ajusco) con 3,293 m\nAltura mínima: Alcadías Madero, Carranza, Iztacalco e Iztapalapa con 2,240 m.")
    elif lstedos.get() == 'Coahuila':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Coahuila", message = "Altura máxima: Cerro San Rafael con 3,293 m\nAltura mínima: Valle del Río Bravo con 200 m.")
    elif lstedos.get() == 'Colima':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Colima", message = "Altura máxima: Volcán de Fuego de Colima con 3,820 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Durango':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Durango", message = "Altura máxima: Cerro Gordo con 3,328 m\nAltura mínima: Río Piaxtla 440 m.")
    elif lstedos.get() == 'Estado de México':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Estado de México", message = "Altura máxima: Volcán Popocatépetl con 5,380 m\nAltura mínima: Presa Vicente Guerrero 420 m.")
    elif lstedos.get() == 'Guanajuato':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Guanajuato", message = "Altura máxima: Sierra Los Agustinos con 3,110 m\nAltura mínima: Cañón del Río Santa María con 720 m.")
    elif lstedos.get() == 'Guerrero':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Guerrero", message = "Altura máxima: Cerro Tiotepec con 3,533 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Hidalgo':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Hidalgo", message = "Altura máxima: Cerro La Peñuela con 3,380 m\nAltura mínima: Río Tecoluco con 154 m.")
    elif lstedos.get() == 'Jalisco':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Jalisco", message = "Altura máxima: Volcán Nevado de Colima con 4,240 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Michoacán':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Michoacán", message = "Altura máxima: Cerro Pico de Tancítaro con 3,840 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Morelos':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Morelos", message = "Altura máxima: Volcán Popocatépetl con 5,380 m\nAltura mínima: Valle de Cuernavaca con 700 m.")
    elif lstedos.get() == 'Nayarit':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Nayarit", message = "Altura máxima: Cerro del Faro con 2,760 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Nuevo León':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Nuevo León", message = "Altura máxima: Cerro El Potosí 3,710 m\nAltura mínima: Llanura Costera 100 m.")
    elif lstedos.get() == 'Oaxaca':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Oaxaca", message = "Altura máxima: Nube Flane (Quie Yelaag) con 2,760 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Puebla':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Puebla", message = "Altura máxima: Pico de Orizaba con 5,610 m\nAltura mínima: Río Pantepec con 120 m.")
    elif lstedos.get() == 'Querétaro':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Querétaro", message = "Altura máxima: Cerro El Zamorano con 3,340 m\nAltura mínima: Jalpan de Serra con 450 m.")
    elif lstedos.get() == 'Quintana Roo':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Quintana Roo", message = "Altura máxima: Cerro El Charro con 230 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'San Luis Potosí':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en San Luis Potosí", message = "Altura máxima: Cerro Grande con 3,180 m\nAltura mínima: Ríos Tampaón y Moctezuma 50 m.")
    elif lstedos.get() == 'Sinaloa':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Sinaloa", message = "Altura máxima: Cerro Alto con 2,800 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Sonora':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Sonora", message = "Altura máxima: Cerro Pico Guacamayas con 2,620 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Tabasco':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Tabasco", message = "Altura máxima: Sierra Tapijulapa con 900 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Tamaulipas':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Tamaulipas", message = "Altura máxima: Peña Nevada con 3,510 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Tlaxcala':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Tlaxcala", message = "Altura máxima: Volcán La Malinche con 4,438 m\nAltura mínima: Río Zahuapan 2,270 m.")
    elif lstedos.get() == 'Veracruz':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Veracruz", message = "Altura máxima: Pico de Orizaba con 5,610 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Yucatán':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Yucatán", message = "Altura máxima: Cerro Benito Juárez con 210 m\nAltura mínima: 0 m.")
    elif lstedos.get() == 'Zacatecas':
        messagebox.showinfo(title ="Metros sobre el nivel del mar en Zacatecas", message = "Altura máxima: Cerro Los Pelones con 3,160 m\nAltura mínima: Cañón del Río Jichipila 840 m.")

botonubi = tk.Button(frameestados, command = ubicacion, image = signo)
botonubi["border"] = "0"
botonubi.place(x = 200, y = 35)

frameca = LabelFrame(pesambient, text = "Caudales", width = 350, height = 300, bd = 2, relief = RIDGE, font =("Time new roman", 11))
frameca.place(x = 370, y = 15)

etiqueta1 = Label(frameca, text = "Población: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
etiqueta2 = Label(frameca, text = "Dotación L/hab*día: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 70)
etiqueta3 = Label(frameca, text = "Harmon: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 130)
etiqueta4 = Label(frameca, text = "Factor de aportación: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 190)

global entrPob
global entrDot
global entrHar
global entrApor

entrPob = IntVar()
entrDot = IntVar()
entrHar = DoubleVar()
entrApor = StringVar()
entrApor.set(0.775)

txtpob = Entry(frameca, textvariable = entrPob, width = 20, font =("Time new roman", 11), ).place(x = 20, y = 35)
txtdot = Entry(frameca, textvariable = entrDot, width = 20, font =("Time new roman", 11), ).place(x = 20, y = 95)
txtHarmon = Entry(frameca, textvariable = entrHar, width = 20, font =("Time new roman", 11), ).place(x = 20, y= 155)
txtFc = Entry(frameca, textvariable = entrApor, width = 20, font =("Time new roman", 11), ).place(x = 20, y = 215)

botoncau = tk.Button(frameca, command = pobla, image = signo)
botoncau["border"] = "0"
botoncau.place(x = 200, y = 90)

botonAjs = Button(frameca, command = Ajust, text = "Ajustar Harmon", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 200, y = 155)
botonres = Button(frameca, command = resulcau, text = "Ver resultado de caudales", font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 100, y = 240)

frameh2o = LabelFrame(pesambient, text = "Datos de calidad del agua", width = 310, height = 300, bd = 2, relief = RIDGE, font =("Time new roman", 11))
frameh2o.place(x = 720, y = 15)

etiqueta150 = Label(frameh2o, text = "Carga de sólidos en", font =("Time new roman", 13), fg = "black").place(x = 20, y = 10)
etiqueta150 = Label(frameh2o, text = "suspensión en mg/L: ", font =("Time new roman", 13), fg = "black").place(x = 20, y = 35)

global entCs

entCs = DoubleVar()
entCs.set(92)

txtCs = Entry(frameh2o, textvariable = entCs, width = 20, font =("Time new roman", 11)).place(x = 20, y = 60)

frameeleccionescar = LabelFrame(pesambient, text = "Elección de cárcamo", width = 250, height = 290, bd = 2, relief = RIDGE, font =("Time new roman", 11))
frameeleccionescar.place(x = 20, y = 315)

carcamo = IntVar()
carc1 = Radiobutton(frameeleccionescar, text = "Circular",  width = 15, font =("Time new roman", 12), variable = carcamo, value = 1).place(x = 0, y = 50)
carc2 = Radiobutton(frameeleccionescar, text = "Rectangular",  width = 15, font =("Time new roman", 12), variable = carcamo, value = 2).place(x = 15, y = 100)

frameeleccionesrej = LabelFrame(pesambient, text = "Elección de rejillas", width = 250, height = 290, bd = 2, relief =  RIDGE, font =("Time new roman", 11))
frameeleccionesrej.place(x = 270, y = 315)

reji = IntVar()
rej1 = Radiobutton(frameeleccionesrej, text = "Pequeñas",  width = 15, font =("Time new roman", 12), variable = reji, value = 1).place(x = 15, y = 50)
rej2 = Radiobutton(frameeleccionesrej, text = "Medianas",  width = 15, font =("Time new roman", 12), variable = reji, value = 2).place(x = 15, y = 100)
rej3 = Radiobutton(frameeleccionesrej, text = "Grandes",  width = 15, font =("Time new roman", 12), variable = reji, value = 3).place(x = 15, y = 150)

frameeleccioneszan = LabelFrame(pesambient, text = "Elección de zanjas", width = 250, height = 290, bd = 2, relief =  RIDGE, font =("Time new roman", 11))
frameeleccioneszan.place(x = 520, y = 315)

zanja = IntVar()
zan1 = Radiobutton(frameeleccioneszan, text = "Orbal",  width = 15, font =("Time new roman", 12), variable = zanja, value = 1).place(x = 18, y = 50)
zan2 = Radiobutton(frameeleccioneszan, text = "Pared Isla",  width = 15, font =("Time new roman", 12), variable = zanja, value = 2).place(x = 33, y = 100)
zan3 = Radiobutton(frameeleccioneszan, text = "Recta",  width = 15, font =("Time new roman", 12), variable = zanja, value = 3).place(x = 18, y = 150)
zan4 = Radiobutton(frameeleccioneszan, text = "Herradura",  width = 15, font =("Time new roman", 12), variable = zanja, value = 4).place(x = 33, y = 200)

frameeleccioneslo = LabelFrame(pesambient, text = "Elección de tratamiento de lodos", width = 260, height = 290, bd = 2, relief = RIDGE, font =("Time new roman", 11))
frameeleccioneslo.place(x = 770, y = 315)

lodo = IntVar()
lodo1 = Radiobutton(frameeleccioneslo, text = "Eras", width = 15, font =("Time new roman", 12), variable = lodo, value = 1).place(x = 18, y = 50)

botonres = Button(frameeleccioneslo, text = "Continuar proceso", command = continuar, font = ("Time new roman", 10), background = "white", relief = "ridge").place(x = 120, y = 225)

root.mainloop()
