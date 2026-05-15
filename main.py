'''用 Selenium 搭配 Chrome，登入 flipclass 並自動繳交作業'''
import time
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    load_dotenv()
    account = os.getenv('FLIPCLASS_ACCOUNT', '4b1g0906')
    password = os.getenv('FLIPCLASS_PASSWORD', 'raspberry')

    browser = webdriver.Chrome()

    # 1. 開啟登入頁面
    browser.get('https://flipclass.stust.edu.tw')
    time.sleep(2)

    # 2. 輸入帳號
    account_field = browser.find_element(By.NAME, 'account')
    account_field.clear()
    account_field.send_keys(account)

    # 3. 輸入密碼
    password_field = browser.find_element(By.NAME, 'password')
    password_field.clear()
    password_field.send_keys(password)

    # 4. 按下 Return 鍵
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)

    # 5. 等待 modal 出現並點擊「保持登入」
    try:
        keep_btn = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.keepLoginBtn'))
        )
        browser.execute_script("arguments[0].click();", keep_btn)
        time.sleep(3)
    except Exception:
        print('未找到「保持登入」按鈕')

    print('目前頁面標題:', browser.title)
    print('目前網址:', browser.current_url)

    # 6. 前往作業頁面
    browser.get('https://flipclass.stust.edu.tw/course/homework/149294')
    time.sleep(3)

    # 7. 點擊「交作業」按鈕
    submit_btn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-toggle="modal"][data-target="#lgIframeModalId"]'))
    )
    browser.execute_script("arguments[0].click();", submit_btn)
    time.sleep(5)

    # 8. 切換到 iframe
    iframe = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#lgIframeModalId iframe'))
    )
    browser.switch_to.frame(iframe)
    print('已切換到 iframe')

    # 9. 在 CKEditor 中輸入文字（用 JS 寫入）
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'rte-editable'))
    )
    browser.execute_script("""
        var iframe = document.querySelector('.rte-editable');
        var doc = iframe.contentDocument || iframe.contentWindow.document;
        doc.body.innerHTML = '4b1g0906盧柏均，用法是 source /Users/user/venv/bin/activate;cd /Users/user/my_python_project;python main.py';
    """)
    print('已在編輯器輸入文字')

    # 10. 點擊「上傳檔案」按鈕
    upload_btn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-default'))
    )
    browser.execute_script("arguments[0].click();", upload_btn)
    time.sleep(2)

    # 11. 點擊「瀏覽」按鈕
    browse_btn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'browse-btn'))
    )
    browser.execute_script("arguments[0].click();", browse_btn)
    time.sleep(2)

    # 12. 找到 file input 並傳入檔案路徑
    file_input = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.NAME, 'files[]'))
    )
    file_path = os.path.abspath('/Users/user/my_python_project/main.py')
    file_input.send_keys(file_path)
    print(f'已選取檔案: {file_path}')
    time.sleep(2)

    # 13. 點擊「關閉」按鈕
    close_btn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'close-btn'))
    )
    browser.execute_script("arguments[0].click();", close_btn)
    time.sleep(2)

    # 14. 點擊「繳交」按鈕
    submit_final = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-success'))
    )
    browser.execute_script("arguments[0].click();", submit_final)
    time.sleep(5)

    print('已送出作業!')
    print('目前頁面標題:', browser.title)
    print('目前網址:', browser.current_url)

    # browser.quit()

if __name__ == '__main__':
    main()
