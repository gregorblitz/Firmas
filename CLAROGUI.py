# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 08:59:54 2022

@author: 57321
"""

from tkinter import *
from PIL import ImageTk,Image,ImageDraw,ImageFont
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime


#---------FUNCIONES-----------

def abrirFirma():
    root.filename = filedialog.askopenfilename(initialdir = "C:",title = "Seleccionar Firma", filetypes =(("png files","*.png"),("all files","*.*")))
    ubicacionFirma.set(root.filename)

def carpEntrada():
    filename = filedialog.askdirectory()
    EntCarpeta.set(filename)
    
def carpSalida():
    filename = filedialog.askdirectory()
    SalCarpeta.set(filename)
    
def comenzar():
    print('Hola')
    
def resumen(nombre,apellido,tipofirma,carpetaentrada,carpetasalida):
    response = messagebox.askyesno("Verifique los datos "
                                   ,"Nombre: "+nombre+"\n\nApellido: "+apellido
                                   +"\n\nTipo de Firma: "+tipofirma
                                   +"\n\nCarpeta de Entrada: "+carpetaentrada
                                   +"\n\nCarpeta de Salida: "+carpetasalida)
    #Label(root, text=response).pack()
    
    # if response == 1:
    #     Label(root, text="Stop it bro").pack()
    # else:
    #     Label(root, text="What have u done").pack()
    
def cargarFirma(nombre,apellido,opcion,ubicFirma):
    
    if opcion=="Manuscrito":
        firmapuesta = Image.open(ubicFirma)
        firmapuesta = firmapuesta.resize((220,80))
        firmapuestaimg = ImageTk.PhotoImage(firmapuesta)
                              
        firmafinal = Label(firmamos,image=firmapuestaimg) 
        firmafinal.image = firmapuestaimg
        firmafinal.grid(row=1, column=0,padx=80)
    else:
        base=Image.open("base.png").convert("RGBA")
        txt=Image.new("RGBA",base.size,(255,255,255,0))
        fnt=ImageFont.truetype("arial.ttf",50)
        Nombres=ImageDraw.Draw(txt)
        Nombres.text((150,200),str(nombre)+" "+str(apellido),font=fnt,fill=(0,0,0,250))
        out=Image.alpha_composite(base,txt)
        out.save("Nombres.png")

        today=datetime.today()
        base_1=Image.open("base_1.png").convert("RGBA")
        txt_1=Image.new("RGBA",base_1.size,(255,255,255,0))
        Fecha=ImageDraw.Draw(txt_1)
        Fecha.text((150,200),str(today),font=fnt,fill=(0,0,0,250))
        out=Image.alpha_composite(base_1,txt_1)
        #out.show()
        out.save("Fecha_hora.png")
        
        firmapuesta = Image.open("Nombres.png")
        firmapuesta = firmapuesta.resize((220,80))
        firmapuestaimg = ImageTk.PhotoImage(firmapuesta)
                              
        firmafinal = Label(firmamos,image=firmapuestaimg) 
        firmafinal.image = firmapuestaimg
        firmafinal.grid(row=1, column=0,padx=80)

#----------------------------------------


#------Configuraciones Iniciales---------------
#Inicializa el tkinter
root = Tk()

#Tamaño de la ventana
root.geometry("940x600")
root.resizable(False,False) #No permite hacer la ventana mas grande

#Permite colocarle un titulo al programa
root.title("Firmas Gen XXI")

#Permite colocarle el logo al programa
root.iconbitmap("clarocirculo.ico")

#----------------------------------------------

fuente = "DIN Alternate"

#-----------------LOGOS------------------------
#Permite Poner el texto del proyecto
FirmaTexto = "                            Firmas Gen XXI                           "
FirmaTxt = Label(root,text=FirmaTexto,font=(fuente,18)).grid(row=1,column=1)#Puede marcar error si no se tiene el font instalado

#Permite Poner el Logo de Claro
LogoClaro = Image.open("claroplano.png")
LogoClaro = LogoClaro.resize((220,80))
LogoImg = ImageTk.PhotoImage(LogoClaro)
                      
LogoPoner = Label(image=LogoImg) 
LogoPoner.image = LogoImg
LogoPoner.grid(row=1, column=0)


#Permite Poner el Logo de Gen XXI
LogoGen = Image.open("genlogo2.png")
LogoGen = LogoGen.resize((200,100))
LogoGImg = ImageTk.PhotoImage(LogoGen)
                      
LogoGPoner = Label(image=LogoGImg)
LogoGPoner.image = LogoGImg
LogoGPoner.grid(row=1, column=2)
#----------------------------------------------


#------------Hacer los dos frames--------------
ConfigInicial = Frame(root, bd=2, relief=SOLID, padx=10, pady=10)
archivos = Frame(root, bd=2, relief=SOLID, padx=10, pady=10)
firmamos = Frame(root, bd=2, relief=SOLID, padx=10, pady=10)
#----------------------------------------------

#------------------Para ingresar Nombre--------
Label(ConfigInicial, text="Ingrese Nombre: ", font=(fuente, 14)).grid(row=0, column=0, sticky=W, pady=10)
entradaNombre = Entry(ConfigInicial, font=(fuente, 14))
entradaNombre.grid(row=0, column=1, pady=10, padx=20)

#---------------------------------------------

#------------------Para ingresar Apellido--------
Label(ConfigInicial, text="Ingrese Apellido: ", font=(fuente, 14)).grid(row=1, column=0, pady=10)
entradaApellido = Entry(ConfigInicial, font=(fuente, 14))
entradaApellido.grid(row=1, column=1, pady=10, padx=20)
#---------------------------------------------


#---------Menu desplegable tipo de firma--------
Label(ConfigInicial, text="Tipo de Firma: ", font=(fuente, 14)).grid(row=2, column=0, sticky=W, pady=10)
opcionesFirma = ["Manuscrito","Nombre"]
Firmado = StringVar()
Firmado.set(opcionesFirma[0])
menuFirma = OptionMenu(ConfigInicial, Firmado,*opcionesFirma)
menuFirma.grid(row=2, column=1, pady=10, padx=20)
menuFirma.config(width=10, font=(fuente, 14))
#-----------------------------------------------

#------------Cargar Firma---------------------

ubicacionFirma = StringVar()
Label(ConfigInicial, text="Cargar Firma: ", font=(fuente, 14)).grid(row=3, column=0, sticky=W, pady=10)
botonCargar = Button(ConfigInicial, text="Abrir",command = abrirFirma,font=(fuente, 14)).grid(row=3, column=1, sticky=W, pady=10,padx=10)
botonMostrar = Button(ConfigInicial, text="Cargar",
                      command = lambda: cargarFirma(entradaNombre.get(),entradaApellido.get(),Firmado.get(),ubicacionFirma.get()),font=(fuente, 14)).grid(row=3, column=1, sticky=W, pady=10,padx=80)
#Label(ConfigInicial, text="...", textvariable = ubicacionFirma, font=(fuente, 14)).grid(row=4, column=0, sticky=W, pady=10) #Para probar nada mas
#--------------------------------------------

ConfigInicial.place(x=50, y=150)


Label(firmamos, text="Firma ingresada: ", font=(fuente, 14)).grid(row=0, column=0, sticky=W, pady=10)



firmamos.place(x=50,y=400)

#--------Frame Derecho-------------------
EntCarpeta = StringVar()
SalCarpeta = StringVar()

Label(archivos, text="Entrada Carpeta: ", font=(fuente, 14)).grid(row=0, column=0, sticky=W, pady=10)
botonEntCarpeta = Button(archivos, text="Abrir",command = carpEntrada,font=(fuente, 14)).grid(row=0, column=1, sticky=W, pady=10,padx=20)
Label(archivos, text="Salida Carpeta: ", font=(fuente, 14)).grid(row=1, column=0, sticky=W, pady=10)
botonSalCarpeta = Button(archivos, text="Abrir",command = carpSalida,font=(fuente, 14)).grid(row=1, column=1, sticky=W, pady=10,padx=20)

#Label(archivos, text="...", textvariable = EntCarpeta, font=(fuente, 14)).grid(row=3, column=0, sticky=W, pady=10) #Para probar nada mas
#Label(archivos, text="...", textvariable = SalCarpeta, font=(fuente, 14)).grid(row=4, column=0, sticky=W, pady=10) #Para probar nada mas

botonComenzar = Button(archivos, width=15, text='Comenzar', font=(fuente, 14)
                       , command=lambda: resumen(entradaNombre.get(),entradaApellido.get(),Firmado.get(),EntCarpeta.get(),SalCarpeta.get()))
botonComenzar.grid(row=7, column=1, pady=10, padx=20)

#-------------------------------------------
archivos.place(x=500, y=150)


root.mainloop()



