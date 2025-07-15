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
