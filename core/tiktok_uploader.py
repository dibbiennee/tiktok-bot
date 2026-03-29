import time
import random
from appium import webdriver
from appium.options import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import (
    APPIUM_HOST, TIKTOK_PACKAGE, TIKTOK_ACTIVITY,
    APPIUM_WAIT_TIMEOUT, TYPING_DELAY_MIN, TYPING_DELAY_MAX,
    ACTION_DELAY_MIN, ACTION_DELAY_MAX,
    POST_DELAY_MIN, POST_DELAY_MAX
)


def get_driver(device_serial: str) -> webdriver.Remote:
    options = AppiumOptions()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.udid = device_serial
    options.app_package = TIKTOK_PACKAGE
    options.app_activity = TIKTOK_ACTIVITY
    options.no_reset = True
    return webdriver.Remote(APPIUM_HOST, options=options)


def _sleep(min_s: float = None, max_s: float = None):
    time.sleep(random.uniform(
        min_s or ACTION_DELAY_MIN,
        max_s or ACTION_DELAY_MAX
    ))


def upload_video(device_serial: str, caption: str, hashtags: str) -> bool:
    driver = None
    try:
        driver = get_driver(device_serial)
        wait = WebDriverWait(driver, APPIUM_WAIT_TIMEOUT)

        # Tap + (bottone crea)
        plus_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ACCESSIBILITY_ID, 'Create video')
        ))
        _sleep()
        plus_btn.click()

        # Tap Upload (galleria)
        _sleep(2, 3)
        upload_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, '//android.widget.TextView[@text="Upload"]')
        ))
        upload_btn.click()

        # Seleziona primo video in galleria
        _sleep(1.5, 2.5)
        first_video = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, '(//android.widget.FrameLayout[@content-desc])[1]')
        ))
        first_video.click()

        # Next
        _sleep()
        next_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, '//android.widget.TextView[@text="Next"]')
        ))
        next_btn.click()

        # Schermata post — inserisce caption con typing umano
        _sleep(2, 4)
        caption_field = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, '//android.widget.EditText')
        ))
        caption_field.clear()
        full_caption = f"{caption}\n{hashtags}"
        for char in full_caption:
            caption_field.send_keys(char)
            time.sleep(random.uniform(TYPING_DELAY_MIN, TYPING_DELAY_MAX))

        # Pubblica
        _sleep(1.5, 3)
        post_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, '//android.widget.TextView[@text="Post"]')
        ))
        post_btn.click()

        _sleep(POST_DELAY_MIN, POST_DELAY_MAX)
        print(f"[TikTok] Video pubblicato su {device_serial}")
        return True

    except Exception as e:
        print(f"[TikTok] Errore su {device_serial}: {e}")
        return False
    finally:
        if driver:
            driver.quit()
