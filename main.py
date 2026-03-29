import json
import time
import os
import random
from datetime import datetime, timedelta

from core.drive_downloader import list_videos, download_video
from core.adb_controller import push_video, is_device_online, device_serial_from_instance
from core.tiktok_uploader import upload_video
from core.caption_manager import get_caption
from config.settings import (
    UPLOADED_LOG, ACCOUNTS_FILE, DATA_DIR,
    BETWEEN_ACCOUNTS_MIN, BETWEEN_ACCOUNTS_MAX,
    LOOP_INTERVAL_HOURS
)


def load_json(path: str) -> dict:
    if os.path.exists(path):
        return json.load(open(path, encoding='utf-8'))
    return {}


def save_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)


def run_cycle():
    print(f"\n{'='*50}")
    print(f"[Main] Ciclo avviato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    accounts = json.load(open(ACCOUNTS_FILE, encoding='utf-8'))
    uploaded = load_json(UPLOADED_LOG)

    for account in accounts:
        brand = account['brand']
        folder_id = account['drive_folder_id']
        instance = account['ldplayer_instance']
        device_serial = device_serial_from_instance(instance)
        interval_hours = account.get('post_interval_hours', 24)

        print(f"\n[Main] → {brand} ({device_serial})")

        # Controlla intervallo minimo
        last_post = uploaded.get(brand, {}).get('last_post')
        if last_post:
            next_allowed = datetime.fromisoformat(last_post) + timedelta(hours=interval_hours)
            if datetime.now() < next_allowed:
                remaining = (next_allowed - datetime.now()).seconds // 60
                print(f"[Main] {brand}: prossimo post tra {remaining} minuti, skip")
                continue

        # Controlla device online
        if not is_device_online(device_serial):
            print(f"[Main] {brand}: device {device_serial} offline, skip")
            continue

        # Lista video da Drive
        videos = list_videos(folder_id)
        if not videos:
            print(f"[Main] {brand}: nessun video su Drive")
            continue

        done_ids = uploaded.get(brand, {}).get('video_ids', [])
        pending = [v for v in videos if v['id'] not in done_ids]

        if not pending:
            print(f"[Main] {brand}: tutti i video già pubblicati")
            continue

        video = pending[0]
        local_path = os.path.join(DATA_DIR, f"tmp_{brand}_{video['name']}")

        # Download
        if not download_video(video['id'], local_path):
            continue

        # Push su emulatore
        remote = push_video(device_serial, local_path)
        if not remote:
            os.remove(local_path)
            continue

        # Caption
        caption, hashtags = get_caption(account['caption_file'])

        # Upload TikTok
        success = upload_video(device_serial, caption, hashtags)

        # Aggiorna log
        if success:
            if brand not in uploaded:
                uploaded[brand] = {'video_ids': [], 'last_post': None}
            uploaded[brand]['video_ids'].append(video['id'])
            uploaded[brand]['last_post'] = datetime.now().isoformat()
            save_json(UPLOADED_LOG, uploaded)
            print(f"[Main] {brand}: log aggiornato")

        # Pulizia tmp
        if os.path.exists(local_path):
            os.remove(local_path)

        # Pausa tra account
        pause = random.uniform(BETWEEN_ACCOUNTS_MIN, BETWEEN_ACCOUNTS_MAX)
        print(f"[Main] Pausa {pause:.0f}s prima del prossimo account...")
        time.sleep(pause)

    print(f"\n[Main] Ciclo completato: {datetime.now().strftime('%H:%M:%S')}")


if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    while True:
        run_cycle()
        print(f"\n[Main] Prossimo ciclo tra {LOOP_INTERVAL_HOURS}h...")
        time.sleep(LOOP_INTERVAL_HOURS * 3600)
