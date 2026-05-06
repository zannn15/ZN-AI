import os
import sys
import time
import requests
import platform
from datetime import datetime

# --- STANDAR UI @ZN.MultiMedia ---
try:
    from colorama import init, Fore, Style
    import pyfiglet
    from dotenv import load_dotenv
except ImportError:
    print("\n[!] Error: Library belum lengkap.")
    print("[!] Jalankan: pip install requests colorama pyfiglet python-dotenv\n")
    sys.exit(1)

init(autoreset=True)

# Warna Estetik
VIOLET = Fore.MAGENTA + Style.BRIGHT
WHITE  = Fore.WHITE + Style.BRIGHT
SUBTLE = Fore.MAGENTA
SUCCESS = Fore.GREEN + Style.BRIGHT
WARN   = Fore.YELLOW + Style.BRIGHT
ERROR  = Fore.RED + Style.BRIGHT
DARK   = Fore.BLACK + Style.BRIGHT

class ZNAI_Titanium_Fixed:
    def __init__(self):
        self.cls()
        # 1. AUTO-CONFIG (Secret Variable Check)
        if not os.path.exists(".env"):
            self.setup_env()

        load_dotenv()
        self.token = os.getenv("HF_TOKEN")
        
        # 2. IDENTITY & ENGINE
        self.identity = {"ver": "6.7.0-Fixed", "owner": "Zan", "brand": "@ZN.MultiMedia"}
        self.api_url = "https://api-inference.huggingface.co/models/"
        
        # Menggunakan Model yang Paling Stabil (Anti 403/400)
        self.engines = {
            "CHAT": "Qwen/Qwen2.5-7B-Instruct",
            "LOGIC": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        }

        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.active = True

    def setup_env(self):
        print(f"{VIOLET}" + pyfiglet.figlet_format("ZN-FIX", font="small"))
        print(f"{DARK}—" * 50)
        print(f"{WHITE}[!] SETUP TOKEN @ZN.MultiMedia")
        token = input(f"{WHITE}Masukkan Token Hugging Face: {Fore.YELLOW}").strip()
        if token.startswith("hf_"):
            with open(".env", "w") as f: f.write(f"HF_TOKEN={token}")
            print(f"{SUCCESS}[+] File .env berhasil dibuat!")
            time.sleep(1.5)
            self.cls()
        else:
            print(f"{ERROR}[!] Token salah. Harus diawali 'hf_'."); sys.exit(1)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def loading(self):
        sys.stdout.write(f"{SUBTLE}[PROCESS]{WHITE} Neural Processing")
        for _ in range(3):
            time.sleep(0.3); sys.stdout.write("."); sys.stdout.flush()
        print("")

    def send_request(self, prompt):
        # Deteksi apakah butuh hitungan/logika
        mode = "LOGIC" if any(x in prompt.lower() for x in ['hitung', 'akar', 'mtk', 'math']) else "CHAT"
        model = self.engines[mode]

        # FIX PAYLOAD: Format paling aman untuk menghindari Error 400
        payload = {
            "inputs": f"User: {prompt}\nAI:",
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False
            },
            "options": {
                "wait_for_model": True # Mencegah error saat model lagi loading
            }
        }

        try:
            self.loading()
            response = requests.post(
                f"{self.api_url}{model}",
                headers=self.headers,
                json=payload,
                timeout=40
            )

            if response.status_code == 200:
                result = response.json()
                # Handle output list atau dict
                out_text = result[0]['generated_text'] if isinstance(result, list) else result['generated_text']
                
                print(f"{VIOLET} ZN-AI ❯ {WHITE}", end="")
                for char in out_text.strip():
                    sys.stdout.write(char); sys.stdout.flush(); time.sleep(0.01)
                print(f"\n{DARK}" + "—" * 45)
                
            elif response.status_code == 400:
                print(f"{ERROR}[!] Neural Error 400: Format ditolak. Mencoba fallback...")
            elif response.status_code == 403:
                print(f"{ERROR}[!] Neural Error 403: Akses ditolak. Cek Token atau klik 'Agree' di model.")
            else:
                print(f"{ERROR}[!] Neural Error {response.status_code}: {response.text}")

        except Exception as e:
            print(f"{ERROR}[SYSTEM CRITICAL]: {e}")

    def start(self):
        banner = pyfiglet.figlet_format("ZN-AI", font="slant")
        print(f"{VIOLET}{banner}")
        print(f"{SUBTLE}  [ VERSION ] : {self.identity['ver']}")
        print(f"{SUBTLE}  [ OWNER   ] : {self.identity['owner']} ({self.identity['brand']})")
        print(f"{DARK}  " + "=" * 55 + "\n")

        while self.active:
            try:
                t = datetime.now().strftime("%H:%M:%S")
                user_in = input(f"{DARK}[{t}]{WHITE} $ znai chat > {Style.RESET_ALL}")

                if not user_in.strip(): continue
                if user_in.lower() in ['exit', 'clear']:
                    if user_in.lower() == 'clear': self.start(); continue
                    self.active = False; break

                self.send_request(user_in)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    bot = ZNAI_Titanium_Fixed()
    bot.start()
    
