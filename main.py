import os
import sys
import time
import json
import logging
import threading
from datetime import datetime

# --- EMERGENCY LIBRARY CHECK ---
try:
    from ctransformers import AutoModelForCausalLM, AutoConfig
    from colorama import init, Fore, Style
    import pyfiglet
    from tqdm import tqdm
except ImportError as e:
    print(f"\n[!] Missing Module: {e}")
    print("[!] Fix with: pip install ctransformers colorama pyfiglet tqdm\n")
    sys.exit(1)

# Inisialisasi Terminal UI
init(autoreset=True)

# Konfigurasi Estetika @ZN.MultiMedia
VIOLET = Fore.MAGENTA + Style.BRIGHT
WHITE  = Fore.WHITE + Style.BRIGHT
SUBTLE = Fore.MAGENTA
SUCCESS = Fore.GREEN + Style.BRIGHT
WARN   = Fore.YELLOW + Style.BRIGHT
ERROR  = Fore.RED + Style.BRIGHT
DARK   = Fore.BLACK + Style.BRIGHT

class ZNAI_System:
    def __init__(self):
        # Metadata
        self.identity = {
            "name": "ZN-AI",
            "version": "Titanium v2.0.1",
            "creator": "Zan",
            "org": "@ZN.MultiMedia",
            "status": "Alpha Access"
        }
        
        # Database Model (GGUF Official - No Login Required)
        self.registry = {
            "GENERAL": {
                "repo": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
                "file": "qwen2.5-1.5b-instruct-q4_k_m.gguf",
                "type": "gpt2"
            },
            "LOGIC": {
                "repo": "unsloth/DeepSeek-R1-Distill-Qwen-1.5B-GGUF",
                "file": "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf",
                "type": "llama"
            }
        }
        
        self.active_model = None
        self.active_engine_name = None
        self.history = []
        
        # Inisialisasi Log
        logging.basicConfig(
            filename='zn_ai_internal.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def screen_refresh(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def boot_sequence(self):
        self.screen_refresh()
        ascii_art = pyfiglet.figlet_format("ZN-AI", font="slant")
        print(f"{VIOLET}{ascii_art}")
        print(f"{SUBTLE}  — Core System: {self.identity['version']}")
        print(f"{SUBTLE}  — Developer: {self.identity['creator']} ({self.identity['org']})")
        print(f"{DARK}  " + "=" * 50)
        print(f"{WHITE}  Offline Engine. Private Processing. No Internet Required.")
        print(f"{DARK}  " + "=" * 50 + "\n")

    def log_event(self, message, level="info"):
        if level == "info":
            logging.info(message)
        else:
            logging.error(message)

    def engine_loader(self, engine_key):
        """Memuat Neural Core ke RAM dengan optimasi CPU."""
        if self.active_engine_name == engine_key:
            return

        print(f"{SUBTLE}[SYSTEM]{WHITE} Warming up {VIOLET}{engine_key}{WHITE} Neural Core...")
        
        try:
            start_time = time.time()
            
            # Auto-detect hardware for optimization
            is_android = os.path.exists("/system/app")
            
            self.active_model = AutoModelForCausalLM.from_pretrained(
                self.registry[engine_key]["repo"],
                model_file=self.registry[engine_key]["file"],
                model_type=self.registry[engine_key]["type"],
                context_length=2048,
                threads=4 if is_android else 8
            )
            
            self.active_engine_name = engine_key
            elapsed = round(time.time() - start_time, 2)
            
            print(f"{SUBTLE}[SYSTEM]{SUCCESS} Engine Ready in {elapsed}s.\n")
            self.log_event(f"Engine {engine_key} initialized in {elapsed}s")
            
        except Exception as e:
            self.log_event(f"Boot Failure {engine_key}: {e}", "error")
            print(f"{ERROR}[CRITICAL] Boot Failure: {e}")
            print(f"{WARN}[ADVICE] Check storage or update link in main.py.")
            sys.exit(1)

    def router(self, user_input):
        """Menganalisa input untuk memilih model terbaik."""
        logic_triggers = ['hitung', 'mtk', 'matematika', 'rumus', 'solve', 'logic', 'problem']
        if any(trigger in user_input.lower() for trigger in logic_triggers):
            return "LOGIC"
        return "GENERAL"

    def process_chat(self, user_prompt):
        # Pilih engine yang sesuai secara dinamis
        target = self.router(user_prompt)
        self.engine_loader(target)

        print(f"{VIOLET} ZN-AI {DARK}({target}){VIOLET} > {WHITE}", end="", flush=True)
        
        # Hardcoded Identity Instructions (The Guardrail)
        system_instructions = (
            f"Instruction: You are ZN-AI, a smart digital assistant. "
            f"Created by Zan under @ZN.MultiMedia. Be helpful, concise, and professional. "
            f"User: {user_prompt}\nAI:"
        )

        output_buffer = ""
        try:
            # Streaming tokens untuk efek real-time
            for token in self.active_model(system_instructions, stream=True, temperature=0.7):
                sys.stdout.write(token)
                sys.stdout.flush()
                output_buffer += token
            
            print("\n" + f"{DARK}" + "—" * 40)
            self.history.append({"q": user_prompt, "a": output_buffer})
            
        except Exception as e:
            print(f"\n{ERROR}[PROCESSOR ERROR]: {e}")
            self.log_event(f"Inference error: {e}", "error")

    def session_manager(self):
        self.boot_sequence()
        # Default load Qwen (GENERAL)
        self.engine_loader("GENERAL")
        
        print(f"{VIOLET}●{WHITE} Status: {SUCCESS}Ready for Alpha Access")
        print(f"{VIOLET}●{WHITE} Dev: {WHITE}{self.identity['org']}")
        print(f"{DARK}Type 'exit' to quit | 'clear' to refresh UI\n")

        while True:
            try:
                timestamp = datetime.now().strftime("%H:%M")
                prompt = input(f"{DARK}[{timestamp}]{WHITE} $ znai chat > {Style.RESET_ALL}")
                
                if not prompt.strip():
                    continue
                
                if prompt.lower() in ['exit', 'quit', 'keluar']:
                    print(f"\n{SUBTLE}[SYSTEM]{WHITE} Powering down. Goodbye, Zan!")
                    break
                
                if prompt.lower() == 'clear':
                    self.boot_sequence()
                    continue

                self.process_chat(prompt)

            except KeyboardInterrupt:
                print(f"\n{WARN}[!] Interrupted by user.")
                break

if __name__ == "__main__":
    # Starting the ZN-AI Titanium Core
    zn_core = ZNAI_System()
    zn_core.session_manager()
    
