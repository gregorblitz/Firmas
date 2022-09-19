# [Firma PDF ](https://gitlab.com/bitconrad/firma-pdf)
Ejecutar los siguiente comandos en el terminal VS Code para firmar PDF:
- Instalar paquetes (debe tener la version 3.8.1 de python): `pip install PDFNetPython3==8.1.0 pyOpenSSL==20.0.1`
- Para firmar el documento en una coordenada especificada: `python sign_pdf.py -i ".\static\Letter of confirmation.pdf" -s "BM" -x 330 -y 280`
- Si llega a saltar el error: `AttributeError: module 'lib' has no attribute 'X509_V_FLAG_CB_ISSUER_CHECK' CB_ISSUER_CHECK = _lib.X509_V_FLAG_CB_ISSUER_CHECK` , debe irse a la línea 1577 en File "C:\Users\USUARIODELPC\anaconda3\lib\site-packages\OpenSSL\crypto.py", line 1577, in X509StoreFlags y comentar la línea.
- Para firmar documentos de la carpeta static en una coordenada especificada: `python sign_pdf.py -i ".\static" -s "BM" -x 330 -y 280`
- Se genera un documento con el mismo nombre pero con extensión agregada _signed
- Referencia usada [tutorial](https://www.thepythoncode.com/article/sign-pdf-files-in-python) para ejecutar el programa
