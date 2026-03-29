# TikTok Bot — Multi-account Automation

Pipeline: Google Drive → Python Orchestrator → LDPlayer (ADB + Appium) → TikTok

## Setup
1. `pip install -r requirements.txt`
2. Configura `config/accounts.json` (copia da accounts.example.json)
3. Aggiungi `config/credentials.json` da Google Cloud Console
4. Avvia Appium: `appium`
5. Lancia: `python main.py`

## Workflow sviluppo
- Sviluppo su Mac con Claude Code
- Deploy su VPS Windows con `git pull`
