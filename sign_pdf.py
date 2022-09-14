# Import Libraries
import OpenSSL
import os #crear un archivo dentro de la carpeta,
import time
import argparse
from PDFNetPython3.PDFNetPython import *
from typing import Tuple


def createKeyPair(type, bits):
    """
    Create a public/private key pair
    Arguments: Type - Key Type, must be one of TYPE_RSA and TYPE_DSA
               bits - Number of bits to use in the key (1024 or 2048 or 4096)
    Returns: The public/private key pair in a PKey object
    """
    pkey = OpenSSL.crypto.PKey()
    pkey.generate_key(type, bits)
    return pkey



def create_self_signed_cert(pKey):
    """Create a self signed certificate. This certificate will not require to be signed by a Certificate Authority."""
    # Create a self signed certificate
    cert = OpenSSL.crypto.X509()
    # Common Name (e.g. server FQDN or Your Name)
    cert.get_subject().CN = "BASSEM MARJI"
    # Serial Number
    cert.set_serial_number(int(time.time() * 10))
    # Not Before
    cert.gmtime_adj_notBefore(0)  # Not before
    # Not After (Expire after 10 years)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    # Identify issue
    cert.set_issuer((cert.get_subject()))
    cert.set_pubkey(pKey)
    cert.sign(pKey, 'md5')  # or cert.sign(pKey, 'sha256')
    return cert


def load():
    """Generate the certificate"""
    summary = {}
    summary['OpenSSL Version'] = OpenSSL.__version__
    # Generating a Private Key...
    key = createKeyPair(OpenSSL.crypto.TYPE_RSA, 1024)
    # PEM encoded
    with open('.\static\private_key.pem', 'wb') as pk:
        pk_str = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
        pk.write(pk_str)
        summary['Private Key'] = pk_str
    # Done - Generating a private key...
    # Generating a self-signed client certification...
    cert = create_self_signed_cert(pKey=key)
    with open('.\static\certificate.cer', 'wb') as cer:
        cer_str = OpenSSL.crypto.dump_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert)
        cer.write(cer_str)
        summary['Self Signed Certificate'] = cer_str
    # Done - Generating a self-signed client certification...
    # Generating the public key...
    with open('.\static\public_key.pem', 'wb') as pub_key:
        pub_key_str = OpenSSL.crypto.dump_publickey(
            OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey())
        #print("Public key = ",pub_key_str)
        pub_key.write(pub_key_str)
        summary['Public Key'] = pub_key_str
    # Done - Generating the public key...
    # Take a private key and a certificate and combine them into a PKCS12 file.
    # Generating a container file of the private key and the certificate...
    p12 = OpenSSL.crypto.PKCS12()
    p12.set_privatekey(key)
    p12.set_certificate(cert)
    open('.\static\container.pfx', 'wb').write(p12.export())
    # You may convert a PKSC12 file (.pfx) to a PEM format
    # Done - Generating a container file of the private key and the certificate...
    # To Display A Summary
    print("## Initialization Summary ##################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("############################################################################")
    return True

## Apartir de aca empieza lo que necesitamos

def sign_file(input_file: str, signatureID: str, x_coordinate: int, #Funcion que permite insertar widget de firma en las pag elegidas en una ubicacion determinada y agrega la firma
            y_coordinate: int, pages: Tuple = None, output_file: str = None
              ):
    """Sign a PDF file"""
    # Un archivo de salida se genera automáticamente con la palabra firmada agregada al final
    if not output_file:
        output_file = (os.path.splitext(input_file)[0]) + "_signed.pdf" #le agrega _signed al pdf
    # inicializa la libreria
    PDFNet.Initialize()
    doc = PDFDoc(input_file)#PDFDoc CLASE CLAVE lee el documento
    # Crear un campo de firma
    sigField = SignatureWidget.Create(doc, Rect( #metodo que Crea una nueva anotación SignatureWidget en el documento especificado y agrega un campo de formulario de firma asociado al documento con un nombre de campo predeterminado.
        x_coordinate, y_coordinate, x_coordinate+100, y_coordinate+50), signatureID)
    # Iterar a lo largo de las páginas del documento
    for page in range(1, (doc.GetPageCount() + 1)):# GetPageCount Devuelve el número de páginas del documento PDF cargado actualmente
        # Si es necesario para páginas específicas
        if pages:
            if str(page) not in pages:
                continue
        pg = doc.GetPage(page)#obtiene contenido pagina especificada
        # Crea un campo de texto de firma y empújelo en la página
        pg.AnnotPushBack(sigField)#metodo que Agrega una anotación al final de la matriz de anotaciones de una página.
    # imagen de la firma
    sign_filename = os.path.dirname( #funcion extrae la carpeta principal de la ruta en Python
        os.path.abspath(__file__)) + "\static\signature.jpg"
    # Self signed certificate
    pk_filename = os.path.dirname(
        os.path.abspath(__file__)) + "\static\container.pfx" #abspath() toma una ruta o un nombre de archivo como parámetro que representa una ruta del sistema de archivos.
    # Recuperar el campo de la firma.
    approval_field = doc.GetField(signatureID)
    approval_signature_digsig_field = DigitalSignatureField(approval_field)#permite agregar un campo de formulario de firma digital vacío a un documento.
    # Agrega apariencia al campo de la firma.
    img = Image.Create(doc.GetSDFDoc(), sign_filename)#DFDoc es un documento de bajo nivel que representa un gráfico de nodos SDF.Obj
    found_approval_signature_widget = SignatureWidget(
        approval_field.GetSDFObj()) # GetSDFDoc Devuelve el diccionario ClassMap.
    found_approval_signature_widget.CreateSignatureAppearance(img)
    # Prepare la firma y el controlador de firma para la firma.
    approval_signature_digsig_field.SignOnNextSave(pk_filename, '')#Se debe llamar para preparar una firma para la firma, lo cual se hace posteriormente llamando a Guardar. No se pueden firmar dos firmas durante un guardado (lanzamientos).
    # La firma se realizará durante la siguiente operación de guardado incremental.
    doc.Save(output_file, SDFDoc.e_incremental)
    # Desarrollar un resumen del proceso
    summary = {
        "Input File": input_file, "Signature ID": signatureID, 
        "Output File": output_file, "Signature File": sign_filename, 
        "Certificate File": pk_filename
    }
    # Resumen de impresión
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return True

#la siguiente función es útil para firmar todos los archivos PDF dentro de una carpeta específica:

def sign_folder(**kwargs):#**kwargs permite pasar argumentos de longitud variable asociados con un nombre o key a una función
    """Firme todos los archivos PDF dentro de una ruta específica"""
    input_folder = kwargs.get('input_folder')#obtener el valor asociado con una clave específica que no existe en el diccionario
    signatureID = kwargs.get('signatureID')
    pages = kwargs.get('pages')
    x_coordinate = int(kwargs.get('x_coordinate'))
    y_coordinate = int(kwargs.get('y_coordinate'))
    # Ejecutar en modo recursivo
    recursive = kwargs.get('recursive')
    # Recorra los archivos dentro de la carpeta de entrada.
    for foldername, dirs, filenames in os.walk(input_folder):
        for filename in filenames:
            # Comprobar si el archivo pdf
            if not filename.endswith('.pdf'): #endswith()método devuelve Truesi una cadena termina con el sufijo especificado
                continue
            # Archivo PDF encontrado
            inp_pdf_file = os.path.join(foldername, filename)
            print("Procesamiento de archivo =", inp_pdf_file)
            # Comprimir archivo existente
            sign_file(input_file=inp_pdf_file, signatureID=signatureID, x_coordinate=x_coordinate,
                      y_coordinate=y_coordinate, pages=pages, output_file=None)
        if not recursive:
            break


def is_valid_path(path):
    """Validates the path inputted and checks whether it is a file path or a folder path"""
    if not path:
        raise ValueError(f"Invalid Path")
    if os.path.isfile(path):
        return path
    elif os.path.isdir(path):
        return path
    else:
        raise ValueError(f"Invalid Path {path}")


def parse_args():
    """Get user command line parameters"""
    parser = argparse.ArgumentParser(description="Available Options")
    parser.add_argument('-l', '--load', dest='load', action="store_true",
                        help="Load the required configurations and create the certificate")
    parser.add_argument('-i', '--input_path', dest='input_path', type=is_valid_path,
                        help="Enter the path of the file or the folder to process")
    parser.add_argument('-s', '--signatureID', dest='signatureID',
                        type=str, help="Enter the ID of the signature")
    parser.add_argument('-p', '--pages', dest='pages', type=tuple,
                        help="Enter the pages to consider e.g.: [1,3]")
    parser.add_argument('-x', '--x_coordinate', dest='x_coordinate',
                        type=int, help="Enter the x coordinate.")
    parser.add_argument('-y', '--y_coordinate', dest='y_coordinate',
                        type=int, help="Enter the y coordinate.")
    path = parser.parse_known_args()[0].input_path
    if path and os.path.isfile(path):
        parser.add_argument('-o', '--output_file', dest='output_file',
                            type=str, help="Enter a valid output file")
    if path and os.path.isdir(path):
        parser.add_argument('-r', '--recursive', dest='recursive', default=False, type=lambda x: (
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
            sign_file(
                input_file=args['input_path'], signatureID=args['signatureID'],
                x_coordinate=int(args['x_coordinate']), y_coordinate=int(args['y_coordinate']), 
                pages=args['pages'], output_file=args['output_file']
            )
        # If Folder Path
        elif os.path.isdir(args['input_path']):
            # Process a folder
            sign_folder(
                input_folder=args['input_path'], signatureID=args['signatureID'], 
                x_coordinate=int(args['x_coordinate']), y_coordinate=int(args['y_coordinate']),
                pages=args['pages'], recursive=args['recursive']
            )
