import os
import random
from config.settings import CAPTIONS_DIR


def get_caption(caption_file: str) -> tuple:
    """
    Legge un file caption e ritorna (caption, hashtags) random.

    Formato file:
        Testo caption qui
        #hashtag1 #hashtag2
        ---
        Altra caption
        #altri #hashtag
    """
    path = os.path.join(CAPTIONS_DIR, os.path.basename(caption_file))
    if not os.path.exists(path):
        print(f"[Caption] File non trovato: {path}")
        return '', ''

    content = open(path, encoding='utf-8').read().strip()
    entries = [e.strip() for e in content.split('---') if e.strip()]

    if not entries:
        return '', ''

    entry = random.choice(entries)
    lines = entry.split('\n')
    caption = lines[0].strip()
    hashtags = lines[1].strip() if len(lines) > 1 else ''

    print(f"[Caption] Selezionata: {caption[:50]}...")
    return caption, hashtags
