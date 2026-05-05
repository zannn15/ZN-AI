import os
import sys
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from colorama import init, Fore, Style

# Initialize colorama for terminal styling
init(autoreset=True)

# @ZN.MultiMedia Violet Palette
VIOLET = Fore.MAGENTA + Style.BRIGHT
SUBTLE = Fore.MAGENTA
WHITE = Fore.WHITE + Style.BRIGHT
DARK = Fore.BLACK + Style.BRIGHT
SUCCESS = Fore.GREEN + Style.BRIGHT
ERROR = Fore.RED + Style.BRIGHT

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_branding():
    try:
        import pyfiglet
        # Aesthetic Bold Banner
        banner = pyfiglet.figlet_format("ZN-AI", font="standard")
        print(f"{VIOLET}{banner}")
        print(f"{SUBTLE}  [ QWEN EDITION ] — A part of @ZN.MultiMedia")
        print(f"{DARK}  " + "—" * 50 + "\n")
    except ImportError:
        print(f"\n{VIOLET}=== ZN-AI QWEN ==={Style.RESET_ALL}")
        print(f"{SUBTLE}A part of @ZN.MultiMedia{Style.RESET_ALL}\n")

def typewriter(text, color=WHITE, delay=0.012):
    print(color, end="", flush=True)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL)

def main():
    clear_screen()
    print_branding()
    
    model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    
    # 1. Hardware Optimization Check
    print(f"{SUBTLE}[SYSTEM]{WHITE} Analyzing hardware architecture...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    if device == "cuda":
        print(f"{SUBTLE}[SYSTEM]{SUCCESS} GPU Detected (NVIDIA). Max performance enabled.")
    else:
        print(f"{SUBTLE}[SYSTEM]{WHITE} Running on CPU (Optimized for Mobile/Termux).")

    # 2. Loading the AI Core
    print(f"{SUBTLE}[SYSTEM]{WHITE} Initializing ZN-AI modules...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            # Force float32 on CPU for stability in Termux
            torch_dtype=torch.float32 if device == "cpu" else "auto",
            device_map=device
        )
    except Exception as e:
        print(f"\n{ERROR}[CRITICAL ERROR] Core initialization failed: {e}")
        return

    # 3. Deployment
    clear_screen()
    print_branding()
    print(f"{VIOLET}●{WHITE} Status: {SUCCESS}System Online{Style.RESET_ALL}")
    print(f"{DARK}Type 'exit' to terminate the session.\n")

    while True:
        try:
            # Styled Input
            user_input = input(f"{WHITE} ❯ {Style.RESET_ALL}")
            
            if not user_input.strip(): continue
            if user_input.lower() in ['exit', 'quit', 'shutdown']:
                print(f"\n{SUBTLE}Terminating ZN-AI Core... Goodbye, Zan.")
                break

            # AI Thinking Display
            print(f"\n{VIOLET} 🤖 ZN-AI {Style.RESET_ALL}", end="", flush=True)
            
            # Chat Logic
            messages = [
                {"role": "system", "content": "You are ZN-AI, a smart assistant created by Zan from @ZN.MultiMedia. Answer with a cool, professional, and aesthetic tone."},
                {"role": "user", "content": user_input}
            ]
            
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

            # Generate response
            generated_ids = model.generate(
                model_inputs.input_ids,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            
            response_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
            response = tokenizer.batch_decode(response_ids, skip_special_tokens=True)[0]

            typewriter(response.strip())
            print(f"\n{DARK}" + "—" * 25 + "\n")
            
        except KeyboardInterrupt:
            print(f"\n{SUBTLE}Session interrupted.")
            break
        except Exception as e:
            print(f"\n{ERROR}[ERROR] Anomaly detected: {e}")

if __name__ == "__main__":
    main()
    
