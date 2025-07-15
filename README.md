# 🧠 NeuroNet v0.1 — Offline AI Research Assistant  
*ChatGPT meets research. Local, fast, and private.*

---

## 📌 What is NeuroNet?

**NeuroNet** is a self-hosted, privacy-first AI assistant for research and summarization. Designed to work **fully offline**, even on **low-spec machines**, it allows you to:

- 🔍 Search the web (or load PDFs, `.txt`, etc.)
- ✍️ Summarize content using **open-source LLMs** (GPT-Neo)
- 🖥️ Interact via a clean PyQt6 **desktop GUI**
- 🧠 Run with **no API keys**, **no OpenAI**, and **no spying**
- 🪛 Deploy on **budget-friendly hardware**

---

## ⚙️ Features

| Feature                        | Status |
|-------------------------------|--------|
| 🔌 Offline Mode               | ✅     |
| 🧠 GPT-Neo Integration        | ✅     |
| 🔍 DuckDuckGo Web Search     | ✅     |
| 📄 PDF + Text Reader         | ✅     |
| 🧰 Vector Memory (FAISS/Chroma) | 🔜     |
| 🖥️ PyQt6 GUI                  | ✅     |
| 📱 Android Packaging (Kivy)   | 🔜     |
| 💬 CLI Support                | ✅     |

---

## 🧠 How It Works

1. **User types a query**
2. **DuckDuckGo search** finds top articles (or loads local files)
3. Extracted text is passed to a **GPT-Neo summarizer**
4. **Concise summary** is generated
5. Displayed in either:
   - 🖥️ PyQt6 GUI
   - 🧑‍💻 CLI output

---

## 🖥️ Dev Notes

> ⚠️ This is the **developer version**.  
> The user-friendly packaged version is under construction — current builds are too heavy for most machines without proper GPU or RAM.

---

## 🧪 Target Hardware (Dev Tested)

| Component     | Spec                      |
|--------------|---------------------------|
| CPU          | Intel Core i7 (4th Gen)   |
| GPU          | AMD FirePro M4100 (1GB VRAM) |
| RAM          | 16GB DDR3 (2×8GB)         |
| OS           | Arch Linux (LXQt)         |
| Python       | 3.11.5 (via pyenv)        |


## ❓ Tech FAQ

### 🔌 Can this run completely offline?
**Yes.** No OpenAI, no cloud APIs, no data leaving your machine. You can summarize PDFs, `.txt`, and `.docx` files locally. Web search is optional.

---

### 🧠 Does it use GPT-4 or ChatGPT?
**Nope.** It uses **open-source models** like GPT-Neo. That means no API fees, no spying, no server limits — but also less raw power than OpenAI.

---

### 🖥️ Will it work on my 2010 laptop?
If you're rocking:
- A 4th Gen Intel i7 or better  
- At least **8–16 GB of RAM**  
- A working Linux or Windows OS  

Then **yes** — even if your GPU is some crusty 1GB AMD card (*cough FirePro*).

---

### ⚙️ Does better hardware improve results?
**Absolutely.** Here's how:

| Better Hardware = | What You Get |
|-------------------|--------------|
| More RAM          | Longer input context (better summaries) |
| Faster CPU        | Lower inference time (less lag)         |
| Dedicated GPU     | Optional speed-up, especially for larger models |
| SSD/Cache space   | Faster model load and memory access     |

> GPT-Neo doesn’t "learn" in real-time, but **your hardware controls how much it can process per query**.

---

### 🐌 Why is it slow on my machine?
Probably because:
- You're on CPU-only inference  
- You're loading a large model (e.g. GPT-Neo 1.3B+)  
- You’re running multiple tools (GUI, web scraper, vector store)  

Try the CLI mode for speed, or load smaller files.

---

### 📦 Can I compile it into an `.exe` or `.AppImage`?
Yup. It supports **PyInstaller** for packaging


## 🚀 Future Improvements

Here’s what’s cooking for upcoming versions of NeuroNet:

### 🔬 Intelligence & Reasoning
- [ ] Add tool-based agent reasoning (LangChain-style)
- [ ] Question refinement + follow-up chaining
- [ ] Context blending: combine Web + PDF + Notes into one summary

### 🧠 Memory & Learning
- [ ] Vector memory support (FAISS or ChromaDB)
- [ ] User session memory for continuity
- [ ] Local topic tagging & recall system

### 🌐 Web & File Tools
- [ ] Auto-download articles from URLs
- [ ] Support for `.docx`, `.epub`, `.html`
- [ ] YouTube transcription + summarization
- [ ] Local directory indexing (like a personal research archive)

### 🎨 GUI & UX
- [ ] Chat-style interface with markdown rendering
- [ ] File drag & drop
- [ ] Dark mode / Light mode toggle
- [ ] System tray & background mode

### 📱 Mobile & Lightweight Builds
- [ ] Kivy-based Android version
- [ ] Voice input (offline STT)
- [ ] Model quantization for smaller footprints (GPT-J, GPT-2, etc.)

### ⚙️ Backend & Performance
- [ ] Model auto-downloader with resume support
- [ ] Modular agent architecture (plug in new tools easily)
- [ ] Async loading & task queuing (less blocking)
- [ ] GPU acceleration toggle

### 🧪 Experimental Ideas
- [ ] Local graph-based citation mapping
- [ ] Research trend analyzer (arxiv / Semantic Scholar)
- [ ] “Explain like I’m 5” mode
- [ ] Plugin system (custom tools, local APIs)

---

> Want to help build one of these features? [Open an issue](https://github.com/your-repo/issues) or make a pull request!
