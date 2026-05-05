import os
import sys
import time
import logging
import platform
import subprocess
from datetime import datetime
from threading import Thread

# --- DEPENDENCY SHIELD ---
try:
    from llama_cpp import Llama
    from colorama import init, Fore, Style
    import pyfiglet
    from huggingface_hub import hf_hub_download
except ImportError:
    print("\n[!] Error: Dependencies not found.")
    print("[!] Run: pip install llama-cpp-python colorama pyfiglet huggingface_hub\n")
    sys.exit(1)

# Inisialisasi Terminal UI
init(autoreset=True)

# Aesthetic Palette @ZN.MultiMedia
VIOLET = Fore.MAGENTA + Style.BRIGHT
WHITE  = Fore.WHITE + Style.BRIGHT
SUBTLE = Fore.MAGENTA
SUCCESS = Fore.GREEN + Style.BRIGHT
WARN   = Fore.YELLOW + Style.BRIGHT
ERROR  = Fore.RED + Style.BRIGHT
DARK   = Fore.BLACK + Style.BRIGHT

class ZNAI_Core_Universal:
    """
    ZN-AI TITANIUM MULTI-PLATFORM ENGINE
    Developed by : Zan
    Brand        : @ZN.MultiMedia
    Target       : Android (Termux), Windows, Linux, macOS
    """
    
    def __init__(self):
        self.version = "Titanium v3.0.0-Stable"
        self.dev = "Zan"
        self.brand = "@ZN.MultiMedia"
        self.engine = None
        self.active_id = None
        self.start_time = datetime.now()
        
        # Database Model GGUF - Optimal untuk semua platform
        self.models = {
            "CHITCHAT": {
                "repo": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
                "file": "qwen2.5-1.5b-instruct-q4_k_m.gguf"
            },
            "LOGIC": {
                "repo": "unsloth/DeepSeek-R1-Distill-Qwen-1.5B-GGUF",
                "file": "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf"
            }
        }
        
        # Setup Internal Logging
        logging.basicConfig(
            filename='znai_system.log',
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s'
        )

    def get_terminal_size(self):
        try:
            columns, rows = os.get_terminal_size()
        except OSError:
            columns, rows = 80, 24
        return columns

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_line(self):
        cols = self.get_terminal_size()
        print(f"{DARK}" + "—" * (cols if cols < 60 else 60))

    def show_header(self):
        self.clear_screen()
        banner = pyfiglet.figlet_format("ZN-AI", font="slant")
        print(f"{VIOLET}{banner}")
        print(f"{SUBTLE}  [ VERSION ] : {self.version}")
        print(f"{SUBTLE}  [ CREATOR ] : {self.dev} ({self.brand})")
        self.draw_line()
        print(f"{WHITE}  Running on {platform.system()} {platform.machine()} Architecture")
        self.draw_line()
        print("")

    def log(self, msg, level="info"):
        if level == "info": logging.info(msg)
        else: logging.error(msg)

    def fetch_model(self, key):
        """Mendownload model secara otomatis dari Hugging Face Cloud."""
        print(f"{SUBTLE}[CLOUD]{WHITE} Syncing {VIOLET}{key}{WHITE} Model...")
        try:
            target_path = hf_hub_download(
                repo_id=self.models[key]["repo"],
                filename=self.models[key]["file"],
                resume_download=True
            )
            return target_path
        except Exception as e:
            self.log(f"Download Error: {e}", "error")
            print(f"{ERROR}[ERROR] Cloud Sync Failed: {e}")
            return None

    def initialize_neural_core(self, key):
        """Memuat engine AI dengan optimasi thread otomatis."""
        if self.active_id == key:
            return

        self.log(f"Switching engine to {key}")
        print(f"{SUBTLE}[SYSTEM]{WHITE} Deploying {VIOLET}{key}{WHITE} Neural Core...")
        
        m_path = self.fetch_model(key)
        if not m_path: sys.exit(1)

        try:
            t_start = time.time()
            
            # Detect CPU Cores for Threading Optimization
            cpu_threads = os.cpu_count() or 4
            
            self.engine = Llama(
                model_path=m_path,
                n_ctx=2048,
                n_threads=cpu_threads,
                verbose=False
            )
            
            self.active_id = key
            t_end = round(time.time() - t_start, 2)
            print(f"{SUBTLE}[SYSTEM]{SUCCESS} Neural Core Online in {t_end}s.\n")
            
        except Exception as e:
            self.log(f"Init Error: {e}", "error")
            print(f"{ERROR}[CRITICAL] Boot Failure: {e}")
            sys.exit(1)

    def analyze_input(self, text):
        """Router cerdas untuk memilih model berdasarkan topik."""
        text = text.lower()
        logic_words = ['hitung', 'mtk', 'math', 'solve', 'logic', 'rumus', 'akar', 'persamaan']
        return "LOGIC" if any(w in text for w in logic_words) else "CHITCHAT"

    def process_ai_inference(self, user_msg):
        """Proses berpikir AI dengan Identity Guardrail."""
        target_engine = self.analyze_input(user_msg)
        self.initialize_neural_core(target_engine)

        print(f"{VIOLET} ZN-AI {DARK}({target_engine}){VIOLET} ❯ {WHITE}", end="", flush=True)
        
        # System Prompt Template (Prompt Engineering)
        prompt_struct = (
            f"<|im_start|>system\nYou are ZN-AI, a smart digital assistant by @ZN.MultiMedia. "
            f"Your owner is Zan. Platform: {platform.system()}. Be professional and efficient.<|im_end|>\n"
            f"<|im_start|>user\n{user_msg}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

        response_buffer = ""
        try:
            # Token Streaming Mode
            stream = self.engine(
                prompt_struct,
                stream=True,
                max_tokens=1024,
                stop=["<|im_end|>", "User:"]
            )
            
            for chunk in stream:
                token = chunk['choices'][0]['text']
                sys.stdout.write(token)
                sys.stdout.flush()
                response_buffer += token
            
            print("\n")
            self.draw_line()
            
        except Exception as e:
            self.log(f"Inference Error: {e}", "error")
            print(f"\n{ERROR}[RUNTIME ERROR]: {e}")

    def run(self):
        """Main Life Cycle of ZN-AI Titanium."""
        self.show_header()
        self.initialize_neural_core("CHITCHAT")
        
        print(f"{VIOLET}●{WHITE} Status   : {SUCCESS}System Active")
        print(f"{VIOLET}●{WHITE} Hardware : {WHITE}{platform.machine()}")
        print(f"{VIOLET}●{WHITE} Database : {WHITE}GGUF (Optimized)")
        print(f"{DARK}Commands  : 'exit' to quit | 'clear' to refresh\n")

        while True:
            try:
                curr_time = datetime.now().strftime("%H:%M")
                u_input = input(f"{DARK}[{curr_time}]{WHITE} $ znai chat > {Style.RESET_ALL}")
                
                if not u_input.strip():
                    continue
                
                if u_input.lower() in ['exit', 'quit', 'keluar', 'stop']:
                    print(f"\n{SUBTLE}[SYSTEM]{WHITE} Deactivating Neural Core... Goodbye, Zan!")
                    self.log("System shutdown by user.")
                    break
                
                if u_input.lower() == 'clear':
                    self.show_header()
                    continue

                self.process_ai_inference(u_input)

            except KeyboardInterrupt:
                print(f"\n{WARN}[!] Force stop by user. Exiting...")
                break
            except Exception as e:
                self.log(f"Loop Error: {e}", "error")
                print(f"{ERROR} Unexpected Error: {e}")

if __name__ == "__main__":
    # --- BOOTING THE TITANIUM CORE ---
    znai_app = ZNAI_Core_Universal()
    znai_app.run()

# -----------------------------------------------------------------------------
# @ZN.MultiMedia - THE TITANIUM PROJECT
# -----------------------------------------------------------------------------
# Kode ini dirancang untuk kestabilan di berbagai perangkat.
# Memastikan privasi data tetap terjaga secara offline.
# Menggunakan arsitektur Llama-CPP-Python untuk fleksibilitas CPU.
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# .............................................................................
# [END OF SCRIPT - TOTAL LINES: 200+]
