# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 08:59:54 2022

@author: 57321
"""

from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import filedialog



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
    
    if response == 1:
        Label(root, text="Stop it bro").pack()
    else:
        Label(root, text="What have u done").pack()

#----------------------------------------


#------Configuraciones Iniciales---------------
#Inicializa el tkinter
root = Tk()

#Tamaño de la ventana
root.geometry("940x400")
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
botonCargar = Button(ConfigInicial, text="Abrir",command = abrirFirma,font=(fuente, 14)).grid(row=3, column=1, sticky=W, pady=10,padx=20)
#Label(ConfigInicial, text="...", textvariable = ubicacionFirma, font=(fuente, 14)).grid(row=4, column=0, sticky=W, pady=10) #Para probar nada mas
#--------------------------------------------

ConfigInicial.place(x=50, y=150)

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








#-----------------FRAMES------------------------
# Autor = LabelFrame(root, text="Autor de la Firma",padx=250)
# Autor.grid(row=2, column=0,columnspan=3,sticky=N+S+W)
# Carpeta = LabelFrame(root, text="Ubicacion de entrada y salida de archivos",padx=250)
# Carpeta.grid(row=3, column=0,columnspan=3,sticky=N+S+W)
#----------------------------------------------

#---------------Entradas----------------------


# labelNombre = Label(root,text="Nombre: ",font=("DIN Alternate",12))
# labelNombre.grid(row=2, column=0)


# E1 = Entry(root, bd =5)
# E1.grid(row=2, column=1)

# labelFirma = Label(Autor,text="Tipo de Firma: ",font=("DIN Alternate",12))
# labelFirma.pack(side=RIGHT)


# menuFirma.grid(row=1, column=0)

#e=Entry(Autor,width=50,borderwidth=2).grid(row=0,column=1)
# e.insert(0,"Su nombre muchacho ")

# b = Button(Autor, text = "Press me")
# b2 = Button(Autor, text = "Press me better")
# b.grid(row = 0, column = 0)
# b2.grid(row = 1, column = 1)

# b3 = Button(Carpeta, text = "Press me")
# b4 = Button(Carpeta, text = "Press me better")
# b3.grid(row = 0, column = 0)
# b4.grid(row = 1, column = 1)





# def opensave():
#     root.filename = filedialog.askopenfilename(initialdir = "G:\My Drive\Claro GEN XXI\PruebasTkinter",title = "Select file", filetypes =(("png files","*.png"),("all files","*.*")))
#     #my_label = Label(root, text=root.filename).pack()


# boton = Button(root, text="Open File",command=opensave).pack()


root.mainloop()