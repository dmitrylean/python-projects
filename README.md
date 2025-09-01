# Telegram Bots Collection (Python)

This repository includes two practical Telegram bots written in Python. Both projects are built with real-world usage in mind and showcase automation, API integration, and user interaction via the Telegram Bot API.

---

## 🤖 `freelance-bot`

Telegram bot for collecting and organizing freelance orders

### 🔧 Features

- Accepts order requests from clients
- Captures basic details (name, description, deadline, budget, etc.)
- Sends data to a private admin chat or channel
- Optional moderation flow for reviewing orders before posting

### 🛠️ Tech Stack

- `python-telegram-bot`
- JSON / text-based data storage
- Lightweight and easily deployable

### 📸 Use Cases

- Freelancers or agencies managing incoming orders via Telegram
- Simple automated intake form for services

---

## 🧠 `news-bot`

AI-powered Telegram bot for assisting with channel management

### 🔧 Features

- Generates AI-written content (posts, ideas, or replies)
- Scheduled posting support (optional)
- Integration with GPT (OpenAI or other model)
- Can act as an assistant for writing, formatting, and planning posts

### 🛠️ Tech Stack

- `python-telegram-bot`
- `openai` (or other LLM provider)
- Optional `apscheduler` for post timing
- Config-based settings and modular design

### 📸 Use Cases

- Telegram channel admins who want help drafting content
- Bloggers or educators posting frequently
- AI-driven automation for media planning
