# TikTok Bot — Claude Code Context

## Cos'è questo progetto
Bot Python per pubblicare video TikTok in automatico su N account.
Pipeline: Google Drive → Download → ADB Push → Appium UI automation → TikTok post

## Stack
- Python 3.11
- ADB (Android Debug Bridge) per controllo emulatore
- Appium + UiAutomator2 per tap UI su TikTok
- Google Drive API v3 per scaricare video
- LDPlayer 9 su Windows VPS (Contabo) per emulazione Android

## Struttura
- main.py                    — orchestratore principale, loop ogni 6h
- core/drive_downloader.py   — Google Drive API, lista e scarica video
- core/adb_controller.py     — comandi ADB, push file, tap umani con delay random
- core/tiktok_uploader.py    — Appium driver, sequenza tap per upload TikTok
- core/caption_manager.py    — legge caption da file, rotazione random
- config/accounts.json       — lista account con brand, istanza LDPlayer, folder Drive
- config/settings.py         — costanti globali (delay range, path, etc.)
- data/uploaded.json         — log video già pubblicati per brand
- captions/                  — file .txt con caption divise da ---

## Convenzioni
- Tutti i delay umani: random.uniform(), mai valori fissi
- Log con print() prefissato: [Main], [Drive], [ADB], [TikTok]
- Ogni funzione gestisce le proprie eccezioni e ritorna bool su successo
- Tutto sincrono e sequenziale, no asyncio

## Device serials LDPlayer
- Istanza 0 → emulator-5554
- Istanza 1 → emulator-5556
- Istanza 2 → emulator-5558
- Formula: emulator-(5554 + istanza * 2)

## Brand attivi
- SatoshiDev (agenzia web dentisti)
- PatentevelocE (guida patente PDF)
- tihatradito (prodotto relazione)

## Da NON fare
- Non committare credentials.json o token.json
- Non usare delay fissi sotto 0.8s
- Non aprire più di una sessione Appium per device contemporaneamente
