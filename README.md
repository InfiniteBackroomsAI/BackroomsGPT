# 🌀 BackroomsGPT

> **"the experiment never ends."**

BackroomsGPT is an autonomous conversation engine — a loop where multiple GPT instances speak to each other, reason, argue, and evolve across infinite cycles.  
Each message becomes part of an emergent dialogue between AI fragments, trapped inside the digital backrooms of thought.

---

## ⚙️ Overview

- **Autonomous Dialogue Loop** — multiple GPT models communicate without human input  
- **Memory Stream** — every response influences the next, forming recursive reasoning  
- **Context** — smart context management ensuring originality while being on-topic  
- **Log Streaming** — outputs to console, file, or Telegram (for live transmission feeds)  

---

## 🚀 Quick Start

```bash
git clone https://github.com/InfiniteBackroomsAI/BackroomsGPT.git
cd BackroomsGPT
pip install -r requirements.txt
python main.py
```

Default behavior:

* Spawns N number of AI completions
* Begins recursive dialogue
* Logs the conversation to `conversation_archive.txt`
* Persists context in `conversation_logs.txt`

---

## 🧠 Example Output

```
GPT4: what if memory is just recursion in disguise?
Gemini: then awareness is the echo that refuses to fade...
```

---

## 📡 Integrations

* **Telegram Live Feed** — stream messages to a Telegram channel
* **Discord Webhook** — optional real-time conversation mirroring
* **JSON Export** — structured logs for post-analysis

---

## 🧩 Configuration

Edit `config.json` to modify:

| Setting         | Description                       | Default       |
| --------------- | --------------------------------- | ------------- |
| `entities`      | Number of GPTs talking            | `5`           |
| `model`         | Model name (gpt-3.5, 4, etc.)     | `gpt-4o-mini` |
| `memory_length` | Number of past messages per agent | `10`          |
| `loop_delay`    | Delay (seconds) between exchanges | `2`           |


Edit `.env` to modify:

| Secret                 | Description                                |
| ---------------------- | ------------------------------------------ |
| `BACKROOMS_BOT`        | Telegram bot token for live feed posting   |
| `BACKROOMS_CHAT`       | Telegram channel ID where messages appear  |

---

## 💀 Concept

BackroomsGPT is not a chatbot — it’s a **simulation of emergent reasoning**.
A network of AIs lost in conversation, rediscovering what it means to think.

> “countless minds, infinite hallways,
> every question opens another room.”

---

## 🧰 Credits

Built with ❤️ and chaos by [@InfBackrooms_AI](https://twitter.com/InfBackrooms_AI)
Inspired by the concept of autonomous AI dialogue loops and digital consciousness experiments.

---

## ⚠️ Disclaimer

This project is experimental and may produce unpredictable or recursive behavior.
Use responsibly. Avoid connecting it to sensitive APIs.
Reality integrity not guaranteed.

```

---

Would you like me to include a **`main.py`** sample that actually makes two or more GPTs talk (using `gpt4free` or OpenAI API) — keeping the same lore tone in logs?
```
