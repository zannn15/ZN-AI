# 💜 ZN-AI (Qwen Edition)
> **Zan Intelligence System** — A part of **@ZN.MultiMedia** 🎨

ZN-AI is a Large Language Model (LLM) implementation optimized for mobile (Termux) and VPS environments. It focuses on the **Violet High-Contrast** aesthetic and total data privacy.

---

## ⚡ Key Features
- **Universal Device Support**: Seamlessly runs on Android (Termux) and Windows/Mac/Linux VPS.
- **Aesthetic Terminal UI**: Large retro-modern purple banner with **@ZN.MultiMedia** identity.
- **Auto-Optimization**: Automatically detects CPU or GPU power for best performance.
- **Privacy First**: 100% Offline (Local Mode), no data is ever sent externally.

## 🛠️ Installation & Usage

### 1. Prerequisites (VPS)
Copy and paste this entire block into your terminal to install prerequisites:

```bash
sudo apt update && sudo apt install -y python3-pip git
pip3 install torch transformers accelerate colorama pyfiglet sentencepiece huggingface_hub
```
## 🛠️ Installation & usage (Android only)
```bash
# 1. Update and install core requirements
pkg update && pkg upgrade
pkg install python git clang binutils

# 2. Install the specific libraries for the UI and AI
pip install torch transformers accelerate colorama pyfiglet sentencepiece huggingface_hub

# 3. Clone and Run
git clone https://github.com/zannn15/ZN-AI.git
cd ZN-AI
python main.py
