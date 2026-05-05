import os
import sys
import time
from ctransformers import AutoModelForSequenceGeneration, AutoConfig
from colorama import init, Fore, Style

init(autoreset=True)

# Branding Palette @ZN.MultiMedia
VIOLET = Fore.MAGENTA + Style.BRIGHT
SUBTLE = Fore.MAGENTA
WHITE = Fore.WHITE + Style.BRIGHT
DARK = Fore.BLACK + Style.BRIGHT
SUCCESS = Fore.GREEN + Style.BRIGHT
WARN = Fore.YELLOW + Style.BRIGHT

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    try:
        import pyfiglet
        banner = pyfiglet.figlet_format("ZN-AI", font="slant")
        print(f"{VIOLET}{banner}")
        print(f"{SUBTLE}  ZN.AI CLI (Alpha) - Offline. Private. Powerful.")
        print(f"{SUBTLE}  A part of @ZN.MultiMedia")
        print(f"{DARK}  " + "—" * 45 + "\n")
    except:
        print(f"\n{VIOLET}=== ZN-AI CLI ===\n{SUBTLE}@ZN.MultiMedia\n")

class ZNAICore:
    def __init__(self):
        self.model = None
        self.current_mode = None
        # Menggunakan format GGUF agar hemat storage (hanya ~1GB per model)
        self.models_config = {
            "QWEN": "TheBloke/Qwen-1_8B-GGUF", # Untuk chat umum/berat
            "DEEPSEEK": "TheBloke/deepseek-llm-7B-chat-GGUF" # Untuk logika/MTK
        }

    def load_engine(self, mode):
        if self.current_mode == mode:
            return
        
        print(f"{SUBTLE}[SYSTEM]{WHITE} Switching to {VIOLET}{mode}{WHITE} Engine...")
        try:
            # Menggunakan Ctransformers (Sangat ringan dibanding Torch)
            self.model = AutoModelForSequenceGeneration.from_pretrained(
                self.models_config[mode],
                model_type="gpt2" if mode == "QWEN" else "llama",
                lib="avx2" # Optimasi untuk CPU VPS/Termux
            )
            self.current_mode = mode
            print(f"{SUBTLE}[SYSTEM]{SUCCESS} Engine Ready.\n")
        except Exception as e:
            print(f"{SUBTLE}[SYSTEM]{Fore.RED} Error: {e}")

    def analyze_task(self, prompt):
        # Mekanisme deteksi otomatis: Jika ada angka/logika pakai DeepSeek
        logic_keywords = ['hitung', 'matematika', 'mtk', 'rumus', 'logic', 'solve', '+', '-', '*', '/']
        if any(word in prompt.lower() for word in logic_keywords):
            return "DEEPSEEK"
        return "QWEN"

    def generate(self, prompt):
        target_mode = self.analyze_task(prompt)
        self.load_engine(target_mode)
        
        print(f"{VIOLET} ZN-AI > {WHITE}", end="", flush=True)
        response = ""
        for token in self.model(prompt, stream=True):
            sys.stdout.write(token)
            sys.stdout.flush()
            response += token
        print("\n")

def main():
    clear()
    print_banner()
    core = ZNAICore()
    
    # Pre-load model awal (Qwen)
    core.load_engine("QWEN")
    
    print(f"{VIOLET}●{WHITE} Status: {SUCCESS}System Active{Style.RESET_ALL}")
    print(f"{DARK}Ketik 'exit' untuk keluar.\n")

    while True:
        try:
            user_input = input(f"{WHITE} $ znai chat > {Style.RESET_ALL}")
            if not user_input.strip(): continue
            if user_input.lower() in ['exit', 'keluar', 'quit']: break
            
            core.generate(user_input)
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
    
