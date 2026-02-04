from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

# 設定
EMAIL = "hisashi_itou001@yahoo.co.jp"  # ラッコキーワードのメールアドレス
PASSWORD = "Hisa010asiH"  # ラッコキーワードのパスワード
SEARCH_KEYWORD = "Python"  # 検索したいキーワード
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")  # ダウンロード先

# ダウンロードディレクトリを作成
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Chromeのオプション設定
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
}
chrome_options.add_experimental_option("prefs", prefs)

# ブラウザを起動
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    print("ログインページにアクセス中...")
    driver.get("https://rakkoid.com/login?service_name=rakko-keyword")
    time.sleep(3)
    
    # メールアドレスとパスワードを入力
    print("ログイン情報を入力中...")
    
    # メールアドレス入力欄(usernameフィールド)
    email_input = wait.until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    email_input.clear()
    email_input.send_keys(EMAIL)
    print(f"メールアドレスを入力: {EMAIL}")
    time.sleep(1)
    
    # パスワード入力欄
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys(PASSWORD)
    print("パスワードを入力")
    time.sleep(1)
    
    # ログインボタンをクリック
    submit_button = driver.find_element(By.ID, "form_btn")
    submit_button.click()
    
    print("ログイン処理中...")
    time.sleep(3)
    
    # 検索ボックスにキーワードを入力
    print(f"キーワード '{SEARCH_KEYWORD}' を検索中...")
    search_box = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[class='TextField_input__Dwr2Z sc-b4648576-1 wHErp']"))
    )
    search_box.clear()
    search_box.send_keys(SEARCH_KEYWORD)
    search_box.send_keys(Keys.RETURN)
    
    print("検索結果を待機中...")
    time.sleep(5)
    
    # CSVダウンロードボタンを探してクリック
    print("CSVダウンロードボタンを探索中...")
    csv_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '全キーワードコピー(重複除去)') or contains(@class, 'csv') or contains(text(), 'CSV')]"))
    )
    csv_button.click()
    
    print("CSVファイルをダウンロード中...")
    time.sleep(5)
    
    print(f"完了! ファイルは {DOWNLOAD_DIR} に保存されました。")
    
except Exception as e:
    print(f"エラーが発生しました: {e}")
    # エラー時のスクリーンショットを保存
    driver.save_screenshot("error_screenshot.png")
    print("エラーのスクリーンショットを保存しました: error_screenshot.png")
    
finally:
    print("ブラウザを閉じます...")
    time.sleep(2)
    driver.quit()

print("\n処理が完了しました。")
