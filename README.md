<h1 align="center">
  <img src="https://img.shields.io/badge/QBits-Quantum--Safe%20Encryption-6c63ff?style=for-the-badge&logo=lock" alt="QBits"/>
  <br/><br/>
  🔐 QBits — AI-Powered Quantum-Safe Encryption Platform
</h1>

<p align="center">
  <strong>Encrypt your files today so they're safe from the quantum computers of tomorrow.</strong><br/>
  Built with NIST-approved Post-Quantum Cryptography (Kyber-768) and powered by a real Groq AI assistant.
</p>

<p align="center">
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick%20Start-▶-green?style=flat-square"/></a>
  <a href="#-tutorial--how-to-use-qbits"><img src="https://img.shields.io/badge/Tutorial-📖-blue?style=flat-square"/></a>
  <a href="#-deploy-to-the-web"><img src="https://img.shields.io/badge/Deploy-🚀-orange?style=flat-square"/></a>
  <a href="#-features"><img src="https://img.shields.io/badge/Features-⭐-yellow?style=flat-square"/></a>
</p>

---

## 🌟 What is QBits?

QBits is a web application that lets you **encrypt any file** using post-quantum cryptography — the gold standard recommended by NIST to resist attacks from future quantum computers.

> **Why does this matter?**
> Today's encryption (RSA, AES) can be broken by sufficiently powerful quantum computers. QBits uses **Kyber-768**, one of NIST's four selected quantum-safe algorithms, so your encrypted files stay safe even in the quantum era.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Kyber-768 Encryption** | NIST-selected post-quantum algorithm |
| 🤖 **AI Assistant** | Real-time answers to cryptography questions (powered by Groq) |
| 📊 **Benchmark Tool** | Compare Kyber vs RSA speed side-by-side |
| 🛡️ **Threat Intelligence** | Live quantum threat timeline and risk assessment |
| 🔓 **File Decryption** | Decrypt any QBits-encrypted file with your key file |
| 🔑 **Key Export/Import** | Download your private key to decrypt files across sessions |
| 📈 **Security Dashboard** | ML-based anomaly detection on encryption patterns |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- `liboqs` (Open Quantum Safe library)
- A free [Groq API key](https://console.groq.com) *(optional — for AI assistant)*

### 1. Install liboqs

```bash
sudo apt-get install liboqs-dev   # Ubuntu/Debian
# OR build from source: https://github.com/open-quantum-safe/liboqs
```

### 2. Clone & Install

```bash
git clone https://github.com/your-username/quantum-crypto-project.git
cd quantum-crypto-project

pip install -r requirements.txt
```

### 3. Set up Environment

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY (optional)
```

### 4. Start the Server

```bash
chmod +x start_server.sh
./start_server.sh
```

Then open **http://localhost:5000** in your browser. 🎉

---

## 📖 Tutorial — How to Use QBits

### 🔒 Encrypting a File (Step by Step)

Think of this like sealing a letter with a wax seal — but quantum-proof.

**Step 1 — Generate Your Keys**

1. Open QBits at `http://localhost:5000`
2. Click the **Encryption** tab
3. Select **Kyber-768** (recommended — NIST's top pick)
4. Click **"Generate Encryption Keys"**
5. Wait 1–2 seconds. You'll see a green confirmation ✅

> 💡 *Keys are generated fresh every session — they're unique to you.*

**Step 2 — Upload Your File**

1. Click the upload box or drag and drop any file
   - ✅ Supported: `.pdf`, `.docx`, `.jpg`, `.mp4`, `.zip`, anything!
   - No file size limit on local installs
2. Click **"Encrypt File"**
3. Wait a moment — you'll see timing stats appear

**Step 3 — Download Both Files**

After encryption succeeds, you'll see **two download buttons:**

| Button | What to do |
|---|---|
| ⬇️ **Download Encrypted File** | This is the secure `.encrypted` file to store or share |
| 🔑 **Download Key File** | **SAVE THIS!** Without it, the file can never be decrypted |

> ⚠️ **Critical:** The Key File (`qbits_private_key.json`) is like your house key. Lose it = locked out forever. Keep it somewhere safe (password manager, USB drive, etc.)

---

### 🔓 Decrypting a File (Step by Step)

**Step 1 — Load Your Keys**

Go to the **Decryption** tab. You have two options:

| Option | When to use it |
|---|---|
| **"Use Current Session Keys"** | If you just encrypted the file in *this same browser session* |
| **"Select Key File (.json)"** | If the file was encrypted earlier — upload your saved Key File here ✅ |

**Step 2 — Upload the Encrypted File**

1. Click the upload area in Step 2 of the Decryption tab
2. Select your `.encrypted` file
3. Click **"Decrypt File"**

**Step 3 — Open the Decrypted File**

Your browser will download a file (your original file restored). 

> 🔤 **Tip:** If the downloaded file has no extension (looks like a temp name), rename it based on what you encrypted:
> - Was it a Word document? Add `.docx`
> - Was it a PDF? Add `.pdf`
> - Then double-click to open it normally

---

### 🤖 Using the AI Assistant

Click the **AI Assistant** tab and ask anything:
- *"What is Kyber-768?"*
- *"How does post-quantum cryptography work?"*
- *"When will quantum computers break RSA?"*

The assistant is powered by a real LLM (Groq) and specializes in quantum cryptography.

---

### 📊 Running a Benchmark

Click the **Benchmark** tab to see a live comparison of:
- **Kyber-768 vs RSA-2048** — key generation, encryption, decryption speed
- You'll see bar charts showing Kyber is typically **10–100× faster** than RSA

---

### 🌐 Quantum Threat Intelligence

Click the **Threat Intel** tab to see:
- Timeline of when quantum computers are expected to break current encryption
- Risk assessment based on your data sensitivity
- Real-time threat level dashboard

---

## 🌍 Deploy to the Web

> ⚠️ **Note:** QBits uses a Python/Flask backend with `liboqs` (a compiled C library). Netlify only hosts **static sites**, so it cannot run QBits as-is. Use **Render** instead — it's free and supports Python perfectly.

### Deploy to Render (Free — Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial QBits deployment"
   git remote add origin https://github.com/YOUR_USERNAME/qbits.git
   git push -u origin main
   ```

2. **Go to [render.com](https://render.com)** → "New" → "Web Service"

3. **Connect your GitHub repo**

4. **Set these settings:**
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python src/app.py`

5. **Add Environment Variables:**
   - `GROQ_API_KEY` → your Groq API key
   - `LD_LIBRARY_PATH` → `/usr/local/lib`

6. **Click "Create Web Service"** — Render will build & deploy automatically

> ⚠️ **liboqs on Render:** The `liboqs` C library must be installed at build time. Add a `render.yaml` (see below) or a `Dockerfile` to install it automatically.

### render.yaml (auto-deploy config)

A `render.yaml` file has been added to the root of this project. Render reads it automatically when you push.

---

## 📁 Project Structure

```
quantum-crypto-project/
├── src/
│   ├── app.py                  # Main Flask web server
│   ├── crypto_engine.py        # Core Kyber/RSA encryption engine
│   ├── file_encryptor.py       # File encrypt/decrypt logic
│   ├── ai_security_monitor.py  # ML anomaly detection
│   ├── quantum_threat_intel.py # Threat intelligence engine
│   └── real_ai_assistant.py    # Groq LLM integration
├── frontend/
│   ├── templates/index.html    # Main web UI
│   └── static/
│       └── js/app.js           # Frontend JavaScript
├── requirements.txt            # Python dependencies
├── start_server.sh             # Local startup script
├── render.yaml                 # Render.com deploy config
└── README.md                   # This file
```

---

## 🔑 Key Concepts

### What is Post-Quantum Cryptography?
Traditional encryption like RSA relies on math problems (factoring large numbers) that are hard for classical computers but **trivially easy for quantum computers using Shor's algorithm**. PQC algorithms are based on different math problems that remain hard even for quantum computers.

### What is Kyber-768?
Kyber (now standardised as **ML-KEM** by NIST) is a key encapsulation mechanism based on the hardness of the *Module Learning With Errors* (MLWE) problem. It was selected by NIST in 2022 as one of the first post-quantum standards.

### The Key File — Why You Must Save It
QBits generates a unique key pair per session. The **private key** is what decrypts your files. If you lose it, your encrypted file is mathematically unrecoverable (that's the point of strong encryption). Always save your `qbits_private_key.json`.

---

## 🛡️ Security Notes

- Keys are generated in-memory and never stored on the server
- The Key File should be stored securely (never share it)
- Encrypted files are safe to share — only the Key File can unlock them
- The MAC (Message Authentication Code) check ensures the file hasn't been tampered with

---

## 📜 License

MIT License — free for personal and educational use.

---

<p align="center">
  Built with ❤️ using <a href="https://openquantumsafe.org/">Open Quantum Safe (liboqs)</a> and <a href="https://groq.com/">Groq AI</a>
  <br/>
  <strong>Securing the Post-Quantum Era, one file at a time.</strong>
</p>
