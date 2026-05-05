# 💜 ZN-AI CLI (Alpha Access)
> **ZN.AI Rilis Di Terminal! (CLI)** — A part of @ZN.MultiMedia

ZN-AI adalah asisten cerdas berbasis terminal yang dirancang untuk kecepatan, efisiensi sumber daya, dan privasi total.

## 🚀 Fitur Utama
- **Offline Chat**: Chat tanpa batas, kapan pun tanpa internet!
- **Dual-Engine System**: Otomatis ganti model (Qwen untuk umum, DeepSeek untuk Logika/MTK).
- **Resource Friendly**: Tanpa Torch/Tensorflow berat. Menggunakan GGUF format untuk hemat RAM.
- **Cross-Device**: Lancar di Ubuntu VPS (CPU mode) dan Termux.

## 📖 Tutorial Instalasi

### 1. Persiapan Sistem
**VPS:**
```bash
sudo apt update && sudo apt install -y python3-pip git
```
**Termux (Android):**
```bash
pkg update && pkg upgrade
pkg install python git clang binutils
```
### 2. Deploy Project
```bash
git clone https://github.com/zannn15/ZN-AI.git
cd ZN-AI
```
### 3. Install Dependencies
```bash
pip install llama-cpp-python colorama pyfiglet huggingface_hub tqdm




```
### 4. Jalankan ZN-AI
```bash
python main.py
```
## 🎮 Mekanisme Penggunaan
- **Otomatisasi**: Sistem akan mendeteksi jika pertanyaanmu butuh logika (MTK) dan akan switch ke model DeepSeek secara mandiri.den
- **Hemat Storage**: Menggunakan library `ctransformers` yang jauh lebih kecil ukurannya dibanding library AI standar.
- **Ukuran File** Ukuran download dikirakan
### ⚠️ Catatan Instalasi (Troubleshooting)
Jika muncul error 'Failed to build hf-xet', gunakan perintah ini:
```bash
pip install --no-deps ctransformers colorama pyfiglet huggingface_hub
```
---
**© 2026 @ZN.MultiMedia — Offline. Private. Powerful.**
