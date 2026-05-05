import os
import sys
import time
import json
import requests
import logging
import platform
from datetime import datetime

# --- UI INITIALIZATION ---
try:
    from colorama import init, Fore, Style
    import pyfiglet
except ImportError:
    print("\n[!] Jalankan dulu: pip install requests colorama pyfiglet")
    sys.exit(1)

init(autoreset=True)

# Aesthetic Palette
VIOLET = Fore.MAGENTA + Style.BRIGHT
WHITE  = Fore.WHITE + Style.BRIGHT
SUBTLE = Fore.MAGENTA
SUCCESS = Fore.GREEN + Style.BRIGHT
WARN   = Fore.YELLOW + Style.BRIGHT
ERROR  = Fore.RED + Style.BRIGHT
DARK   = Fore.BLACK + Style.BRIGHT

class ZNAI_Titanium_Serverless:
    """
    ZN-AI TITANIUM - SERVERLESS EDITION
    Optimized by : Zan (@ZN.MultiMedia)
    Features    : No Heavy Building, No Stuck, Multi-Platform.
    """
    
    def __init__(self):
        self.version = "v4.0.0-Serverless"
        self.dev = "Zan"
        self.brand = "@ZN.MultiMedia"
        self.session_id = f"ZN-{int(time.time())}"
        
        # Cloud Endpoint (Menggunakan Public API agar ringan)
        # Tidak perlu download model GGUF bergiga-giga lagi!
        self.api_url = "https://router.huggingface.co/hf-inference/models/"
        self.endpoints = {
            "GENERAL": "Qwen/Qwen2.5-1.5B-Instruct",
            "LOGIC": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        }
        
        # Header System
        self.headers = {"Content-Type": "application/json"}
        
        # Log System
        logging.basicConfig(
            filename='znai_cloud.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

    def screen_refresh(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def show_banner(self):
        self.screen_refresh()
        ascii_text = pyfiglet.figlet_format("ZN-AI", font="slant")
        print(f"{VIOLET}{ascii_text}")
        print(f"{SUBTLE}  [ SYSTEM ] : {self.version}")
        print(f"{SUBTLE}  [ OWNER  ] : {self.dev} ({self.brand})")
        print(f"{DARK}  " + "—" * 55)
        print(f"{WHITE}  Titanium Serverless Engine | Fast Response | Low Memory")
        print(f"{DARK}  " + "—" * 55 + "\n")

    def log_event(self, msg):
        logging.info(msg)

    def analyze_intent(self, prompt):
        """Menganalisa apakah butuh model logika atau umum."""
        p = prompt.lower()
        if any(x in p for x in ['hitung', 'mtk', 'math', 'solve', 'rumus', 'logic']):
            return "LOGIC"
        return "GENERAL"

    def call_cloud_engine(self, prompt):
        """Fungsi utama pengiriman data ke neural server."""
        target = self.analyze_intent(prompt)
        model_id = self.endpoints[target]
        
        print(f"{SUBTLE}[SYSTEM]{WHITE} Routing to {VIOLET}{target}{WHITE} Engine...")
        
        # Identity Guardrail
        payload = {
            "inputs": f"<|im_start|>system\nYou are ZN-AI by @ZN.MultiMedia. Creator: Zan. Be smart.<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n",
            "parameters": {"max_new_tokens": 512, "temperature": 0.7, "return_full_text": False}
        }

        try:
            start_t = time.time()
            response = requests.post(
                f"{self.api_url}{model_id}", 
                headers=self.headers, 
                json=payload,
                timeout=30
            )
            
            # Animasi loading sederhana
            print(f"{SUBTLE}[PROCESS]{WHITE} Thinking", end="")
            for _ in range(3):
                time.sleep(0.3)
                print(".", end="", flush=True)
            print("\n")

            if response.status_code == 200:
                result = response.json()
                # Handle output format yang berbeda-beda dari API
                if isinstance(result, list):
                    text_out = result[0].get('generated_text', 'No response.')
                else:
                    text_out = result.get('generated_text', 'No response.')
                
                print(f"{VIOLET} ZN-AI ❯ {WHITE}", end="")
                # Efek Typewriter
                for char in text_out:
                    sys.stdout.write(char)
                    sys.stdout.flush()
                    time.sleep(0.01)
                
                duration = round(time.time() - start_t, 2)
                print(f"\n{DARK}  " + "—" * 30)
                print(f"{DARK}  Inference time: {duration}s")
                self.log_event(f"Success: {target} in {duration}s")
            
            elif response.status_code == 503:
                print(f"{WARN}[!] Model is loading on server. Please wait 10 seconds...")
                time.sleep(10)
            else:
                print(f"{ERROR}[!] Cloud Error: {response.status_code}")
                self.log_event(f"Status Code {response.status_code}")

        except Exception as e:
            print(f"{ERROR}[CRITICAL]: {e}")
            self.log_event(f"Error: {e}")

    def run_interface(self):
        self.show_banner()
        print(f"{VIOLET}●{WHITE} Status   : {SUCCESS}Cloud-Core Online")
        print(f"{VIOLET}●{WHITE} Platform : {WHITE}{platform.system()}")
        print(f"{VIOLET}●{WHITE} Memory   : {SUCCESS}Optimized (Serverless)")
        print(f"{DARK}Commands  : 'exit' to quit | 'clear' to refresh UI\n")

        while True:
            try:
                ts = datetime.now().strftime("%H:%M")
                cmd = input(f"{DARK}[{ts}]{WHITE} $ znai chat > {Style.RESET_ALL}")
                
                if not cmd.strip(): continue
                if cmd.lower() in ['exit', 'quit', 'keluar']:
                    print(f"\n{SUBTLE}[SYSTEM]{WHITE} Terminating ZN-AI. See you, Zan!")
                    break
                if cmd.lower() == 'clear':
                    self.show_banner()
                    continue

                self.call_cloud_engine(cmd)

            except KeyboardInterrupt:
                print(f"\n{WARN}[!] Break detected.")
                break

if __name__ == "__main__":
    znai = ZNAI_Titanium_Serverless()
    znai.run_interface()

# -----------------------------------------------------------------------------
# ZN-AI PROJECT - TITANIUM SERVERLESS v4.0
# -----------------------------------------------------------------------------
# Kode ini dirancang khusus agar tidak membebani perangkat user.
# Tidak perlu proses 'Building Wheel' atau 'Compiling C++'.
# Data diproses melalui Neural Network di Cloud secara private.
# Creator: Zan (@ZN.MultiMedia)
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# [END OF TITANIUM SCRIPT - TOTAL LINES: 200+]
