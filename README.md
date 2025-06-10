# 🦾 Elon Musk Life MiniApp Auto Miner & Task Claimer

Skrip Python ini dirancang untuk **mengotomatisasi proses mining dan klaim task** pada platform [DAFTAR DISINI]([https://miniapp.elonmusklife.com](https://t.me/elonmusklifebot/earn?startapp=1824331381)). Script ini mendukung **multi akun** dan **proxy** secara otomatis, serta dilengkapi **tampilan konsol interaktif** yang menarik menggunakan `rich` dan `colorama`.

## ✨ Fitur

- ✅ Load otomatis banyak akun dari `token.json`
- 🌐 Dukungan proxy dari `proxy.txt` (opsional)
- 👤 Cek informasi akun & status poin
- ⛏️ Cek dan mulai mining secara otomatis
- 📋 Ambil dan klaim task yang tersedia
- 🔁 Siklus mining dan klaim berulang
- 🎨 Output konsol berwarna dan emoji friendly

## RUN BOT

```bash
git clone https://github.com/danzkyxyz/Elon-Musk-Life-MiniApp-Auto-Miner-Task-Claimer.git
```
```bash
pip install requests colorama rich
```
```bash
python main.py
```
or
```bash
python3 main.py
```

## 🗂️ Struktur File

- `main.py` — Script utama untuk menjalankan bot
- `token.json` — File berisi daftar token akun dalam format:
- ```bash
  TOKEN=xxx
  BEAR_TOKEN=yyy
  ```
Support Multi Account :
```bash
TOKEN=xxx
BEAR_TOKEN=yyy
TOKEN=xxx
BEAR_TOKEN=yyy
```
- `proxy.txt` — (Opsional) Daftar proxy satu per baris, format:
- Tanpa autentikasi: `http://ip:port`
- Dengan autentikasi: `http://user:pass@ip:port`
