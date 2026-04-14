# 🧹 The Clean Code Bot (Automated Refactorer)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**The Clean Code Bot** is a Command Line Interface (CLI) tool designed to bridge the gap between "working" code and "maintainable" code. It leverages Large Language Models (LLMs) to automatically refactor messy, undocumented scripts into clean, production-ready code following **SOLID principles** and proper documentation standards.

---

## ✨ Key Features

* **🧠 Chain of Thought (CoT) Analysis:** Unlike standard linters, the bot performs a logical step-by-step analysis of your code's architecture before proposing changes.
* **🏗️ SOLID Enforcement:** Specifically targets Single Responsibility, Open/Closed, and other core design principles.
* **🛡️ Injection Protection:** Built-in input validation and sanitization to prevent prompt injection and malicious code execution.
* **⚡ Dual-Provider Support:** Seamlessly toggle between **OpenAI** (High reasoning) and **Groq Cloud** (Ultra-fast inference).
* **📚 Auto-Documentation:** Generates comprehensive Google-style Docstrings or JSDoc comments automatically.
