import os
import sys
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from colorama import init, Fore, Style

# Inisialisasi warna
init(autoreset=True)

# Palette Warna ZN.MultiMedia
VIOLET = Fore.MAGENTA + Style.BRIGHT
SUBTLE = Fore.MAGENTA
WHITE = Fore.WHITE + Style.BRIGHT
DARK = Fore.BLACK + Style.BRIGHT

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    try:
        import pyfiglet
        # Desain Banner Kotak-Kotak ala Claude Code
        banner = pyfiglet.figlet_format("ZN-AI", font="standard")
        print(f"{VIOLET}{banner}")
        print(f"{SUBTLE}  [ QWEN EDITION ] — A part of @ZN.MultiMedia")
        print(f"{DARK}  " + "—" * 45 + "\n")
    except:
        print(f"{VIOLET}=== ZN-AI QWEN ===\n{SUBTLE}A part of @ZN.MultiMedia\n")

def typewriter(text, color=WHITE):
    print(color, end="", flush=True)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.015)
    print(Style.RESET_ALL)

def run_system():
    clear()
    print_banner()
    
    model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    
    print(f"{SUBTLE}[SYSTEM]{WHITE} Menginisialisasi modul AI...")
    
    # Memuat Model & Tokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype="auto",
            device_map="auto"
        )
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] Gagal memuat model: {e}")
        return

    clear()
    print_banner()
    print(f"{VIOLET}●{WHITE} Status: {Fore.GREEN}Online & Secure{Style.RESET_ALL}")
    print(f"{DARK}Ketik 'exit' untuk menutup sesi.\n")

    while True:
        user_input = input(f"{WHITE} ❯ {Style.RESET_ALL}")
        
        if not user_input.strip(): continue
        if user_input.lower() in ['exit', 'quit', 'keluar']:
            print(f"\n{SUBTLE}Terminating ZN-AI... Goodbye.")
            break

        # Chat Logic
        messages = [
            {"role": "system", "content": "Kamu adalah ZN-AI, asisten cerdas buatan Zan dari @ZN.MultiMedia. Jawab dengan gaya yang keren, singkat, dan profesional."},
            {"role": "user", "content": user_input}
        ]
        
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        print(f"\n{VIOLET} 🤖 ZN-AI {Style.RESET_ALL}", end="", flush=True)
        
        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7
        )
        
        response_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        response = tokenizer.batch_decode(response_ids, skip_special_tokens=True)[0]

        typewriter(response.strip())
        print(f"\n{DARK}" + "—" * 20 + "\n")

if __name__ == "__main__":
    run_system()
      
