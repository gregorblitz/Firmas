# Import Libraries
import OpenSSL
import os #crear un archivo dentro de la carpeta,
import time
import argparse
from PDFNetPython3.PDFNetPython import *
from typing import Tuple


## Apartir de aca empieza lo que necesitamos

def firmar_archivo(archivo_in: str, firmaID: str, x_coordenada: int, #Funcion que permite insertar widget de firma en las pag elegidas en una ubicacion determinada y agrega la firma
            y_coordenada: int, paginas: Tuple = None, archivo_out: str = None
              ):
    """Firma un archivo PDF"""
    # Un archivo de salida se genera automáticamente con la palabra firmada agregada al final
    if not archivo_out:
        archivo_out = (os.path.splitext(archivo_in)[0]) + "_firmado.pdf" #le agrega _firmado al pdf
    # inicializa la libreria
    PDFNet.Initialize()
    doc = PDFDoc(archivo_in)#PDFDoc CLASE CLAVE lee el documento
    # Crear un campo de firma
    campoFirma = SignatureWidget.Create(doc, Rect( #metodo que Crea una nueva anotación SignatureWidget en el documento especificado y agrega un campo de formulario de firma asociado al documento con un nombre de campo predeterminado.
        x_coordenada, y_coordenada, x_coordenada+100, y_coordenada+50), firmaID)
    # Iterar a lo largo de las páginas del documento
    for pag in range(1, (doc.GetPageCount() + 1)):# GetPageCount Devuelve el número de páginas del documento PDF cargado actualmente
        # Si es necesario para páginas específicas
        if paginas:
            if str(pag) not in paginas:
                continue
        pg = doc.GetPage(pag)#obtiene contenido pagina especificada
        # Crea un campo de texto de firma y empújelo en la página
        pg.AnnotPushBack(campoFirma)#metodo que Agrega una anotación al final de la matriz de anotaciones de una página.
    # imagen de la firma
    firm_nombrearch = os.path.dirname( #funcion extrae la carpeta principal de la ruta en Python
        os.path.abspath(__file__)) + "\static\signature.jpg"
    # Self signed certificate
    pk_archivonombre = os.path.dirname(
        os.path.abspath(__file__)) + "\static\container.pfx" #abspath() toma una ruta o un nombre de archivo como parámetro que representa una ruta del sistema de archivos.
    # Recuperar el campo de la firma.
    campo_aprob = doc.GetField(firmaID)
    firma_aprob_campo_firmdig = DigitalSignatureField(campo_aprob)#permite agregar un campo de formulario de firma digital vacío a un documento.
    # Agrega apariencia al campo de la firma.
    img = Image.Create(doc.GetSDFDoc(), firm_nombrearch)#DFDoc es un documento de bajo nivel que representa un gráfico de nodos SDF.Obj
    encuentra_widget_aprob_firm = SignatureWidget(
        campo_aprob.GetSDFObj()) # GetSDFDoc Devuelve el diccionario ClassMap.
    encuentra_widget_aprob_firm.CreateSignatureAppearance(img)
    # Prepare la firma y el controlador de firma para la firma.
    firma_aprob_campo_firmdig.SignOnNextSave(pk_archivonombre, '')#Se debe llamar para preparar una firma para la firma, lo cual se hace posteriormente llamando a Guardar. No se pueden firmar dos firmas durante un guardado (lanzamientos).
    # La firma se realizará durante la siguiente operación de guardado incremental.
    doc.Save(archivo_out, SDFDoc.e_incremental)
    # Desarrollar un resumen del proceso
    resum = {
        "Input File": archivo_in, "Signature ID": firmaID, 
        "Output File": archivo_out, "Signature File": firm_nombrearch, 
        "Certificate File": pk_archivonombre
    }
    # Resumen de impresión
    print("## resum ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in resum.items()))
    print("###################################################################")
    return True

#la siguiente función es útil para firmar todos los archivos PDF dentro de una carpeta específica:

def firm_carpeta(**kwargs):#**kwargs permite pasar argumentos de longitud variable asociados con un nombre o key a una función
    """Firme todos los archivos PDF dentro de una ruta específica"""
    carpeta_in = kwargs.get('carpeta_in')#obtener el valor asociado con una clave específica que no existe en el diccionario
    firmaID = kwargs.get('firmaID')
    paginas = kwargs.get('paginas')
    x_coordenada = int(kwargs.get('x_coordenada'))
    y_coordenada = int(kwargs.get('y_coordenada'))
    # Ejecutar en modo recursivo
    recursivo = kwargs.get('recursivo')
    # Recorra los archivos dentro de la carpeta de entrada.
    for foldername, dirs, filenames in os.walk(carpeta_in):
        for filename in filenames:
            # Comprobar si el archivo pdf
            if not filename.endswith('.pdf'): #endswith()método devuelve Truesi una cadena termina con el sufijo especificado
                continue
            # Archivo PDF encontrado
            inp_pdf_file = os.path.join(foldername, filename)
            print("Procesamiento de archivo =", inp_pdf_file)
            # Comprimir archivo existente
            firmar_archivo(archivo_in=inp_pdf_file, firmaID=firmaID, x_coordenada=x_coordenada,
                      y_coordenada=y_coordenada, paginas=paginas, archivo_out=None)
        if not recursivo:
            break


def es_ruta_invalida(path):
    """Validates the path inputted and checks whether it is a file path or a folder path"""
    if not path:
        raise ValueError(f"Invalid Path")
    if os.path.isfile(path):
        return path
    elif os.path.isdir(path):
        return path
    else:
        raise ValueError(f"Ruta Invalida {path}")


def parse_args():
    """Get user command line parameters"""
    parser = argparse.ArgumentParser(description="Available Options")
    parser.add_argument('-l', '--load', dest='load', action="store_true",
                        help="Load the required configurations and create the certificate")
    parser.add_argument('-i', '--input_path', dest='input_path', type=es_ruta_invalida,
                        help="Enter the path of the file or the folder to process")
    parser.add_argument('-s', '--firmaID', dest='firmaID',
                        type=str, help="Enter the ID of the signature")
    parser.add_argument('-p', '--paginas', dest='paginas', type=tuple,
                        help="Enter the paginas to consider e.g.: [1,3]")
    parser.add_argument('-x', '--x_coordenada', dest='x_coordenada',
                        type=int, help="Enter the x coordenada.")
    parser.add_argument('-y', '--y_coordenada', dest='y_coordenada',
                        type=int, help="Enter the y coordenada.")
    path = parser.parse_known_args()[0].input_path
    if path and os.path.isfile(path):
        parser.add_argument('-o', '--archivo_out', dest='archivo_out',
                            type=str, help="Enter a valid output file")
    if path and os.path.isdir(path):
        parser.add_argument('-r', '--recursivo', dest='recursivo', default=False, type=lambda x: (
            str(x).lower() in ['true', '1', 'yes']), help="Process Recursively or Non-Recursively")
    args = vars(parser.parse_args())
    # To Display The Command Line Arguments
    print("## Command Arguments #################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in args.items()))
    print("######################################################################")
    return args


if __name__ == '__main__':
    # Parsing command line arguments entered by user
    args = parse_args()
    if args['load'] == True:
        load()
    else:
        # If File Path
        if os.path.isfile(args['input_path']):
            firmar_archivo(
                archivo_in=args['input_path'], firmaID=args['firmaID'],
                x_coordenada=int(args['x_coordenada']), y_coordenada=int(args['y_coordenada']), 
                paginas=args['paginas'], archivo_out=args['archivo_out']
            )
        # If Folder Path
        elif os.path.isdir(args['input_path']):
            # Process a folder
            firm_carpeta(
                carpeta_in=args['input_path'], firmaID=args['firmaID'], 
                x_coordenada=int(args['x_coordenada']), y_coordenada=int(args['y_coordenada']),
                paginas=args['paginas'], recursivo=args['recursivo']
            )
