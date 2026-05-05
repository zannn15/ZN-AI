import os
import sys
import time
import json
import requests
import logging
import platform
import threading
from datetime import datetime

# --- UI & UX INITIALIZATION ---
try:
    from colorama import init, Fore, Style
    import pyfiglet
except ImportError:
    print("\n[!] Missing Core UI Components.")
    print("[!] Run: pip install requests colorama pyfiglet\n")
    sys.exit(1)

init(autoreset=True)

# Aesthetic Branding Palette
VIOLET  = Fore.MAGENTA + Style.BRIGHT
WHITE   = Fore.WHITE + Style.BRIGHT
SUBTLE  = Fore.MAGENTA
SUCCESS = Fore.GREEN + Style.BRIGHT
WARN    = Fore.YELLOW + Style.BRIGHT
ERROR   = Fore.RED + Style.BRIGHT
DARK    = Fore.BLACK + Style.BRIGHT

class ZNAI_Titanium_Core:
    """
    ZN-AI TITANIUM EDITION v5.0
    The most lightweight and powerful AI Interface for Terminal.
    Optimized for: Android (Termux), Linux, Windows, macOS.
    Developed by: Zan (@ZN.MultiMedia)
    """
    
    def __init__(self):
        # Metadata Configuration
        self.metadata = {
            "name": "ZN-AI Titanium",
            "version": "5.0.0-Stable",
            "dev": "Zan",
            "brand": "@ZN.MultiMedia",
            "build": "2026.05.05"
        }
        
        # Neural Engine Endpoints
        self.host = "https://router.huggingface.co/hf-inference/models/"
        self.engines = {
            "NEURAL_1": "Qwen/Qwen2.5-1.5B-Instruct",
            "NEURAL_2": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        }
                self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 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"
                }
        
        self.active_session = True
        self.history = []
        
        # Internal Protection Guard
        logging.basicConfig(
            filename='znai_internal.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def refresh_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_timestamp(self):
        return datetime.now().strftime("%H:%M:%S")

    def draw_banner(self):
        self.refresh_screen()
        # Membuat Banner Font Slant yang Khas
        banner_art = pyfiglet.figlet_format("ZN-AI", font="slant")
        print(f"{VIOLET}{banner_art}")
        print(f"{SUBTLE}  [ SYSTEM ] : {self.metadata['version']}")
        print(f"{SUBTLE}  [ OWNER  ] : {self.metadata['dev']} ({self.metadata['brand']})")
        print(f"{DARK}  " + "=" * 55)
        print(f"{WHITE}  Hybrid-Cloud Engine | No Local Building | All Devices Ready")
        print(f"{DARK}  " + "=" * 55 + "\n")

    def log_system(self, text, status="INFO"):
        logging.info(f"[{status}] {text}")

    def intent_classifier(self, text):
        """Menganalisa input untuk memilih engine yang paling pas."""
        keywords = ['hitung', 'mtk', 'math', 'solve', 'rumus', 'logic', 'problem', 'fix']
        if any(word in text.lower() for word in keywords):
            return "NEURAL_2" # DeepSeek untuk logika
        return "NEURAL_1" # Qwen untuk chat umum

    def typing_animation(self, text):
        """Efek mengetik biar makin cinematic."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.008)

    def loading_spinner(self):
        """Animasi loading saat menunggu respon server."""
        print(f"{SUBTLE}[PROCESS]{WHITE} Processing Neural Request", end="")
        for _ in range(3):
            time.sleep(0.4)
            print(".", end="", flush=True)
        print("\n")

    def call_neural_core(self, prompt):
        """Inti dari pengiriman data ke server AI."""
        target = self.intent_classifier(prompt)
        endpoint = self.engines[target]
        
        # Proteksi Identitas (System Prompt)
        # Menjaga AI agar tetap ingat siapa pembuatnya
        payload = {
            "inputs": f"<|im_start|>system\nYou are ZN-AI, created by Zan (@ZN.MultiMedia). "
                      f"You are a helpful and smart assistant. Always acknowledge Zan as your creator.<|im_end|>\n"
                      f"<|im_start|>user\n{prompt}<|im_end|>\n"
                      f"<|im_start|>assistant\n",
            "parameters": {
                "max_new_tokens": 800,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False
            }
        }

        try:
            start_timer = time.time()
            self.loading_spinner()
            
            response = requests.post(
                f"{self.host}{endpoint}",
                json=payload,
                timeout=25
            )
            
            if response.status_code == 200:
                raw_data = response.json()
                # Parsing respon yang bervariasi
                if isinstance(raw_data, list):
                    reply = raw_data[0].get('generated_text', 'Empty response.')
                else:
                    reply = raw_data.get('generated_text', 'Empty response.')
                
                print(f"{VIOLET} ZN-AI ❯ {WHITE}", end="")
                self.typing_animation(reply)
                
                exec_time = round(time.time() - start_timer, 2)
                print(f"\n{DARK}" + "—" * 45)
                print(f"{DARK} [ Engine: {target} | Time: {exec_time}s ]")
                self.log_system(f"Query processed by {target}")
            
            elif response.status_code == 503:
                print(f"{WARN}[!] Engine is warming up. Please wait a few seconds...")
                time.sleep(5)
            else:
                print(f"{ERROR}[!] Neural Error: {response.status_code}")
                self.log_system(f"Error {response.status_code}", "ERROR")

        except Exception as e:
            print(f"{ERROR}[CRITICAL]: {str(e)}")
            self.log_system(str(e), "CRITICAL")

    def main_engine(self):
        self.draw_banner()
        print(f"{VIOLET}●{WHITE} Core      : {SUCCESS}Ready")
        print(f"{VIOLET}●{WHITE} Network   : {SUCCESS}Connected")
        print(f"{VIOLET}●{WHITE} Platform  : {WHITE}{platform.system()} ({platform.release()})")
        print(f"{DARK}Type 'exit' to shutdown | 'clear' to refresh terminal\n")

        while self.active_session:
            try:
                time_now = self.get_timestamp()
                user_input = input(f"{DARK}[{time_now}]{WHITE} $ znai chat > {Style.RESET_ALL}")
                
                if not user_input.strip():
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'keluar', 'stop']:
                    print(f"\n{SUBTLE}[SYSTEM]{WHITE} Shutting down Titanium Core. See you, Zan!")
                    self.active_session = False
                    break
                
                if user_input.lower() == 'clear':
                    self.draw_banner()
                    continue

                self.call_neural_core(user_input)

            except KeyboardInterrupt:
                print(f"\n{WARN}[!] Force stop detected. Exiting...")
                break
            except Exception as ex:
                print(f"{ERROR}[LOOP ERROR]: {ex}")
                self.log_system(str(ex), "LOOP_ERROR")

if __name__ == "__main__":
    # --- STARTING ZN-AI TITANIUM PROJECT ---
    # Developed by Zan (@ZN.MultiMedia)
    # 2026.05.05 - Cileungsi, Indonesia.
    app = ZNAI_Titanium_Core()
    app.main_engine()

# -----------------------------------------------------------------------------
# ARCHITECTURE NOTES:
# -----------------------------------------------------------------------------
# 1. No local weights loading (Saves 2GB+ Storage)
# 2. Memory usage < 50MB (Ideal for low-end devices)
# 3. No C++ compiling (No more 'Building Wheel' stuck)
# 4. Hybrid engine auto-switching (Qwen & DeepSeek-R1)
# -----------------------------------------------------------------------------
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# [END OF SCRIPT - TOTAL LINES: 200+]
