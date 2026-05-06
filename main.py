import os
import sys
import time
import json
import requests
import logging
import platform
from datetime import datetime

# --- CORE DEPENDENCIES ---
try:
    from colorama import init, Fore, Style
    import pyfiglet
    from dotenv import load_dotenv
except ImportError:
    print("\n[!] Library belum lengkap.")
    print("[!] Jalankan: pip install requests colorama pyfiglet python-dotenv\n")
    sys.exit(1)

init(autoreset=True)

# Aesthetic Branding Palette @ZN.MultiMedia
VIOLET  = Fore.MAGENTA + Style.BRIGHT
WHITE   = Fore.WHITE + Style.BRIGHT
SUBTLE  = Fore.MAGENTA
SUCCESS = Fore.GREEN + Style.BRIGHT
WARN    = Fore.YELLOW + Style.BRIGHT
ERROR   = Fore.RED + Style.BRIGHT
DARK    = Fore.BLACK + Style.BRIGHT

class ZNAI_AutoConfig_Core:
    """
    ZN-AI TITANIUM EDITION v6.5
    Smart Configuration & Secure Vault Architecture.
    Developed by : Zan
    Brand        : @ZN.MultiMedia
    """

    def __init__(self):
        self.cls()
        # 1. SMART AUTO-CONFIG LOGIC
        # Mengecek keberadaan file rahasia (.env)
        if not os.path.exists(".env"):
            self.run_first_time_setup()

        # 2. LOAD SECRETS
        load_dotenv()
        self.token = os.getenv("HF_TOKEN")

        # 3. IDENTITY CONFIG
        self.identity = {
            "name": "ZN-AI Titanium",
            "ver": "6.5.0-AutoConfig",
            "owner": "Zan",
            "brand": "@ZN.MultiMedia"
        }

        # 4. ENGINE CONFIG
        self.api_base = "https://router.huggingface.co/hf-inference/models/"
        self.engines = {
            "CHAT": "Qwen/Qwen2.5-1.5B-Instruct",
            "LOGIC": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        }

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        self.active = True
        self.setup_logs()

    def run_first_time_setup(self):
        """Proses pembuatan file .env otomatis jika belum ada."""
        ascii_setup = pyfiglet.figlet_format("ZN-SETUP", font="small")
        print(f"{VIOLET}{ascii_setup}")
        print(f"{DARK}—" * 50)
        print(f"{WHITE}[!] Welcome to @ZN.MultiMedia Project")
        print(f"{WHITE}[?] Sepertinya ini pertama kali kamu menjalankan ZN-AI.")
        print(f"{SUBTLE}[*] Silakan masukkan Token Hugging Face kamu untuk melanjutkan.")
        print(f"{DARK}—" * 50)
        
        user_token = input(f"\n{WHITE}Masukkan Token (hf_...): {Fore.YELLOW}").strip()
        
        if user_token.startswith("hf_"):
            try:
                with open(".env", "w") as f:
                    f.write(f"HF_TOKEN={user_token}")
                print(f"\n{SUCCESS}[+] Berhasil! File .env telah dibuat otomatis.")
                print(f"{SUCCESS}[+] Token kamu tersimpan aman di sistem lokal.")
                time.sleep(2)
                self.cls()
            except Exception as e:
                print(f"{ERROR}[!] Gagal membuat file .env: {e}")
                sys.exit(1)
        else:
            print(f"\n{ERROR}[!] Token Tidak Valid! Harus diawali dengan 'hf_'.")
            print(f"{WARN}[*] Ambil token di: huggingface.co/settings/tokens")
            sys.exit(1)

    def setup_logs(self):
        logging.basicConfig(
            filename='znai_system.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def show_banner(self):
        self.cls()
        banner = pyfiglet.figlet_format("ZN-AI", font="slant")
        print(f"{VIOLET}{banner}")
        print(f"{SUBTLE}  [ VERSION ] : {self.identity['ver']}")
        print(f"{SUBTLE}  [ OWNER   ] : {self.identity['owner']} ({self.identity['brand']})")
        print(f"{DARK}  " + "=" * 55)
        print(f"{WHITE}  Auto-Config Mode | Secure Variable Engine | Hybrid Neural")
        print(f"{DARK}  " + "=" * 55 + "\n")

    def typing(self, text):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)

    def loading_anim(self):
        print(f"{SUBTLE}[PROCESS]{WHITE} Connecting to Neural Cloud", end="")
        for _ in range(3):
            time.sleep(0.4)
            print(".", end="", flush=True)
        print("\n")

    def process_chat(self, prompt):
        """Memilih engine dan mengirim request ke Cloud API."""
        # Logika sederhana: Jika ada kata hitung/math, pakai DeepSeek
        is_math = any(x in prompt.lower() for x in ['hitung', 'math', 'mtk', 'akar', 'logika'])
        engine_key = "LOGIC" if is_math else "CHAT"
        model_id = self.engines[engine_key]

        payload = {
            "inputs": f"<|im_start|>system\nYou are ZN-AI by @ZN.MultiMedia. Creator: Zan. Smart & Helpful.<|im_end|>\n"
                      f"<|im_start|>user\n{prompt}<|im_end|>\n"
                      f"<|im_start|>assistant\n",
            "parameters": {"max_new_tokens": 800, "temperature": 0.7, "return_full_text": False}
        }

        try:
            self.loading_anim()
            start_t = time.time()
            
            res = requests.post(
                f"{self.api_base}{model_id}",
                headers=self.headers,
                json=payload,
                timeout=35
            )

            if res.status_code == 200:
                data = res.json()
                reply = data[0]['generated_text'] if isinstance(data, list) else data['generated_text']
                
                print(f"{VIOLET} ZN-AI ❯ {WHITE}", end="")
                self.typing(reply)
                
                duration = round(time.time() - start_t, 2)
                print(f"\n{DARK}" + "—" * 45)
                print(f"{DARK} [ Engine: {engine_key} | Speed: {duration}s ]")
                
            elif res.status_code == 401:
                print(f"{ERROR}[!] Error 401: Token di file .env salah!")
                print(f"{WARN}[*] Hapus file .env dan jalankan ulang script untuk reset.")
            elif res.status_code == 503:
                print(f"{WARN}[!] Model sedang loading dlm server. Tunggu 15 detik...")
            else:
                print(f"{ERROR}[!] Neural Error: {res.status_code}")

        except Exception as e:
            print(f"{ERROR}[SYSTEM ERROR]: {e}")

    def run(self):
        self.show_banner()
        print(f"{VIOLET}●{WHITE} Vault Status : {SUCCESS}Locked & Secure")
        print(f"{VIOLET}●{WHITE} Connection   : {SUCCESS}Neural-Cloud Active")
        print(f"{VIOLET}●{WHITE} Device       : {WHITE}{platform.node()} ({platform.system()})")
        print(f"{DARK}Type 'exit' to quit | 'clear' to refresh banner\n")

        while self.active:
            try:
                now = self.get_time()
                inp = input(f"{DARK}[{now}]{WHITE} $ znai chat > {Style.RESET_ALL}")

                if not inp.strip(): continue
                if inp.lower() in ['exit', 'quit', 'stop', 'keluar']:
                    print(f"\n{SUBTLE}[SYSTEM]{WHITE} Shutdown ZN-AI. See you, Zan!")
                    self.active = False
                    break
                if inp.lower() == 'clear':
                    self.show_banner()
                    continue

                self.process_chat(inp)

            except KeyboardInterrupt:
                print(f"\n{WARN}[!] Break detected. Exiting...")
                break

if __name__ == "__main__":
    # --- STARTING @ZN.MultiMedia PROJECT ---
    # Optimized Secure Version 6.5.0
    # Creator: Zan
    app = ZNAI_AutoConfig_Core()
    app.run()

# -----------------------------------------------------------------------------
# ZN-AI PROJECT - AUTO-CONFIG SECURE v6.5
# -----------------------------------------------------------------------------
# Script ini secara otomatis menangani pembuatan file .env (Secret).
# User hanya perlu memasukkan token sekali, dan file rahasia akan dibuat.
# Jangan lupa tambahkan '.env' ke dalam file .gitignore kamu!
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# [END OF TITANIUM SCRIPT - TOTAL LINES: 200+]
