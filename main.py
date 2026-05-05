import os
import sys
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from colorama import init, Fore, Style

# Initialize colorama for terminal colors
init(autoreset=True)

# Define @ZN.MultiMedia Palette (VIOLET High-Contrast)
VIOLET = Fore.MAGENTA + Style.BRIGHT
SUBTLE = Fore.MAGENTA
WHITE = Fore.WHITE + Style.BRIGHT
DARK = Fore.BLACK + Style.BRIGHT
SUCCESS = Fore.GREEN + Style.BRIGHT
ERROR = Fore.RED + Style.BRIGHT

def clear_terminal():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Prints the aesthetic VIOLET banner and branding."""
    try:
        import pyfiglet
        # Larger, bold font style for the name
        banner = pyfiglet.figlet_format("ZN-AI", font="standard")
        print(f"{VIOLET}{banner}")
        print(f"{SUBTLE}  [ QWEN EDITION ] — A part of @ZN.MultiMedia")
        # Line divider
        print(f"{DARK}  " + "—" * 50 + "\n")
    except ImportError:
        # Fallback if pyfiglet is missing
        print(f"\\n{VIOLET}=== ZN-AI QWEN ==={Style.RESET_ALL}")
        print(f"{SUBTLE}A part of @ZN.MultiMedia{Style.RESET_ALL}\\n")

def typewriter(text, color=WHITE, delay=0.015):
    """Prints text with a typewriter effect."""
    print(color, end="", flush=True)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL)

def main():
    clear_terminal()
    print_banner()
    
    # Using Qwen 2.5 1.5B (Excellent local model)
    model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    
    # 1. HW Check & Optimization (Crucial for Universal/Mobile Support)
    print(f"{SUBTLE}[SYSTEM]{WHITE} Analyzing hardware core...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    if device == "cuda":
        print(f"{SUBTLE}[SYSTEM]{SUCCESS} NVIDIA GPU detected. Max performance enabled.")
    else:
        print(f"{SUBTLE}[SYSTEM]{WHITE} CPU mode active (Power Saving/Mobile optimization).")

    # 2. Model Loading
    print(f"{SUBTLE}[SYSTEM]{WHITE} Initializing AI modules. Please wait...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            # Using torch.float32 for absolute stability on CPU/Termux
            torch_dtype=torch.float32 if device == "cpu" else "auto",
            device_map=device
        )
    except Exception as e:
        print(f"\\n{ERROR}[CRITICAL ERROR] Failed to load core system: {e}")
        return

    # 3. Ready State
    clear_terminal()
    print_banner()
    print(f"{VIOLET}●{WHITE} Status: {SUCCESS}System Active{Style.RESET_ALL}")
    print(f"{DARK}Type 'exit' or 'keluar' to shutdown.\\n")

    while True:
        try:
            # Styled Input Prompt
            user_input = input(f"{WHITE} ❯ {Style.RESET_ALL}")
            
            if not user_input.strip():
                continue
            if user_input.lower() in ['exit', 'quit', 'keluar', 'shutdown']:
                print(f"\\n{SUBTLE}Terminating ZN-AI Core... Goodbye, Zan.")
                break

            # Response Loading Line
            print(f"\\n{VIOLET} 🤖 ZN-AI {Style.RESET_ALL}", end="", flush=True)
            
            # Formulating the specific conversation structure for Qwen
            messages = [
                {"role": "system", "content": "You are ZN-AI, a smart, cool, and professional assistant made by Zan from @ZN.MultiMedia."},
                {"role": "user", "content": user_input}
            ]
            
            # Apply template
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

            # Performance optimized generation (Mobile-safe settings)
            generated_ids = model.generate(
                model_inputs.input_ids,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            
            response_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
            response = tokenizer.batch_decode(response_ids, skip_special_tokens=True)[0]

            # Output AI response
            typewriter(response.strip())
            # Output response divider
            print(f"\\n{DARK}" + "—" * 25 + "\\n")
            
        except KeyboardInterrupt:
            print(f"\\n\\n{SUBTLE}Interrupted. Shutting down...")
            break
        except Exception as e:
            print(f"\\n{ERROR}[ERROR] Anomaly detected: {e}")

if __name__ == "__main__":
    main()
