import os

# Delay umani (secondi)
TAP_DELAY_MIN = 0.8
TAP_DELAY_MAX = 2.5
ACTION_DELAY_MIN = 1.5
ACTION_DELAY_MAX = 4.0
POST_DELAY_MIN = 3.0
POST_DELAY_MAX = 6.0
TYPING_DELAY_MIN = 0.03
TYPING_DELAY_MAX = 0.09

# Pausa tra account nello stesso ciclo (secondi)
BETWEEN_ACCOUNTS_MIN = 30
BETWEEN_ACCOUNTS_MAX = 90

# Loop principale
LOOP_INTERVAL_HOURS = 6

# Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CAPTIONS_DIR = os.path.join(BASE_DIR, 'captions')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

UPLOADED_LOG = os.path.join(DATA_DIR, 'uploaded.json')
ACCOUNTS_FILE = os.path.join(CONFIG_DIR, 'accounts.json')
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(CONFIG_DIR, 'token.json')

# Appium
APPIUM_HOST = 'http://localhost:4723'
TIKTOK_PACKAGE = 'com.zhiliaoapp.musically'
TIKTOK_ACTIVITY = 'com.ss.android.ugc.aweme.main.MainActivity'
APPIUM_WAIT_TIMEOUT = 20

# ADB
ADB_REMOTE_DIR = '/sdcard/DCIM/tiktok_upload'
