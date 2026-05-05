import os
import sys
import time
import json
import logging
from datetime import datetime

# Mencoba import library dengan error handling yang pro
try:
    from ctransformers import AutoModelForCausalLM, AutoConfig
    from colorama import init, Fore, Style
    import pyfiglet
except ImportError as e:
    print(f"[!] Library missing: {e}")
    print("[!] Run: pip install ctransformers colorama pyfiglet tqdm requests")
    sys.exit(1)

# Inisialisasi Colorama untuk UI Aesthetic
init(autoreset=True)

# Konfigurasi Branding @ZN.MultiMedia
VIOLET = Fore.MAGENTA + Style.BRIGHT
WHITE  = Fore.WHITE + Style.BRIGHT
SUBTLE = Fore.MAGENTA
SUCCESS = Fore.GREEN + Style.BRIGHT
WARN   = Fore.YELLOW + Style.BRIGHT
ERROR  = Fore.RED + Style.BRIGHT
DARK   = Fore.BLACK + Style.BRIGHT

class ZNAI_Engine:
    def __init__(self):
        self.version = "Alpha 1.5.0"
        self.creator = "Zan (@ZN.MultiMedia)"
        self.model = None
        self.current_engine_name = None
        
        # Database Model GGUF (Hemat RAM & Storage)
        self.registry = {
            "QWEN": {
                "repo": "TheBloke/Qwen-1_8B-GGUF",
                "file": "qwen-1_8b-chat.Q4_K_M.gguf",
                "type": "gpt2"
            },
            "DEEPSEEK": {
                "repo": "TheBloke/deepseek-llm-7B-chat-GGUF",
                "file": "deepseek-llm-7b-chat.Q2_K.gguf",
                "type": "llama"
            }
        }
        
        # Logging System
        logging.basicConfig(filename='znai_system.log', level=logging.INFO)

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_banner(self):
        self.clear_terminal()
        banner_text = pyfiglet.figlet_format("ZN-AI", font="slant")
        print(f"{VIOLET}{banner_text}")
        print(f"{SUBTLE}  [ VERSION: {self.version} ]")
        print(f"{SUBTLE}  [ CREATOR: {self.creator} ]")
        print(f"{DARK}  " + "—" * 55)
        print(f"{WHITE}  Offline. Private. Multi-Engine Terminal Interface.")
        print(f"{DARK}  " + "—" * 55 + "\n")

    def load_model(self, engine_key):
        """Memuat model AI ke memori dengan optimasi CPU."""
        if self.current_engine_name == engine_key:
            return

        print(f"{SUBTLE}[SYSTEM]{WHITE} Initializing {VIOLET}{engine_key}{WHITE} Neural Core...")
        
        try:
            start_time = time.time()
            # Auto-optimization berdasarkan OS
            is_termux = "com.termux" in sys.executable
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.registry[engine_key]["repo"],
                model_type=self.registry[engine_key]["type"],
                context_length=2048,
                # Menghindari error di Termux dengan lib generic jika perlu
                lib="avx2" if not is_termux else None 
            )
            
            self.current_engine_name = engine_key
            duration = round(time.time() - start_time, 2)
            print(f"{SUBTLE}[SYSTEM]{SUCCESS} Engine Loaded successfully in {duration}s.\n")
            logging.info(f"Engine {engine_key} loaded in {duration}s")
            
        except Exception as e:
            print(f"{ERROR}[CRITICAL] Boot Failure: {e}")
            logging.error(f"Failed to load {engine_key}: {e}")
            sys.exit(1)

    def analyze_intent(self, user_input):
        """Logika Switcher: Deteksi apakah user butuh MTK atau Chat Umum."""
        math_keywords = ['hitung', 'mtk', 'matematika', 'rumus', 'solve', 'kuadrat', 'logaritma', '+', '/', '*']
        if any(word in user_input.lower() for word in math_keywords):
            return "DEEPSEEK"
        return "QWEN"

    def typewriter_effect(self, text):
        """Efek mengetik biar makin cinematic."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.005)

    def generate_response(self, prompt):
        target_engine = self.analyze_intent(prompt)
        self.load_model(target_engine)

        print(f"{VIOLET} ZN-AI {DARK}({target_engine}){VIOLET} > {WHITE}", end="", flush=True)
        
        # Identity Protection Prompt
        system_rules = (
            f"Identify as ZN-AI by @ZN.MultiMedia. Creator: Zan. "
            f"You are a computer program. Current time: {datetime.now().strftime('%H:%M')}. "
            f"User says: {prompt} \nAI:"
        )

        full_response = ""
        try:
            for token in self.model(system_rules, stream=True, max_new_tokens=1024, temperature=0.7):
                sys.stdout.write(token)
                sys.stdout.flush()
                full_response += token
            print("\n" + f"{DARK}" + "—" * 30)
        except Exception as e:
            print(f"\n{ERROR}[PROCESS ERROR]: {e}")

    def run(self):
        self.display_banner()
        # Default awal pakai Qwen biar cepat
        self.load_model("QWEN")
        
        print(f"{VIOLET}●{WHITE} Status: {SUCCESS}System Active")
        print(f"{VIOLET}●{WHITE} Model: {WHITE}GGUF Compressed (Storage Optimized)")
        print(f"{DARK}Type 'exit' or 'clear' to manage session.\n")

        while True:
            try:
                now = datetime.now().strftime("%H:%M")
                user_cmd = input(f"{DARK}[{now}]{WHITE} $ znai chat > {Style.RESET_ALL}")
                
                if not user_cmd.strip():
                    continue
                
                if user_cmd.lower() in ['exit', 'quit', 'keluar']:
                    print(f"{SUBTLE}[SYSTEM]{WHITE} Shutting down ZN-AI Core. See you, Zan!")
                    break
                
                if user_cmd.lower() == 'clear':
                    self.display_banner()
                    continue

                self.generate_response(user_cmd)

            except KeyboardInterrupt:
                print(f"\n{WARN}[!] Force stop detected.")
                break

if __name__ == "__main__":
    app = ZNAI_Engine()
    app.run()
            
