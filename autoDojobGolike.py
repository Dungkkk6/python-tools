from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import random

# Cấu hình trình duyệt với tiện ích mở rộng
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
extension_path = r'C:\Users\dungvnzx1\Downloads\tool v2=v2.1\recaptcha'  # Đường dẫn của bạn
options.add_argument(f'--load-extension={extension_path}')

driver = webdriver.Chrome(options=options)

# Mở trang web
driver.get("https://app.golike.net")
WebDriverWait(driver, 20).until(EC.url_contains("golike"))  # Chờ trang tải xong

def wait_for_element(xpath, timeout=10):
    """Chờ cho đến khi phần tử có thể tương tác được."""
    try:
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException:
        print(f"Hết thời gian chờ phần tử: {xpath}")
        return None

def click_element(xpath):
    """Nhấp vào phần tử, chờ nếu cần."""
    element = wait_for_element(xpath)
    if element:
        element.click()
    else:
        print(f"Không thể nhấp vào phần tử: {xpath}")

def input_text(xpath, text):
    """Nhập văn bản vào trường, chờ cho đến khi trường có thể nhập."""
    element = wait_for_element(xpath)
    if element:
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
    else:
        print(f"Không thể nhập văn bản vào trường: {xpath}")

def login(username, password):
    try:
        username_xpath = '/html/body/div[1]/div/div[1]/div/form/div[1]/input'
        input_text(username_xpath, username)

        password_xpath = '/html/body/div[1]/div/div[1]/div/form/div[2]/div/input'
        input_text(password_xpath, password)

        login_button_xpath = '/html/body/div[1]/div/div[1]/div/form/div[3]/button'
        click_element(login_button_xpath)
        
        # Xử lý ô "Đã hiểu" nếu xuất hiện
        try:
            da_hieu_xpath = '/html/body/div[1]/div/div[1]/div[3]/div/div/div/div/div/button'
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, da_hieu_xpath))).click()
            print("Đã nhấp vào ô 'Đã hiểu'")
        except TimeoutException:
            print("Không tìm thấy ô 'Đã hiểu' hoặc đã đăng nhập thành công")
    except Exception as e:
        print(f"Lỗi khi đăng nhập: {e}")

# Đăng nhập
login('ngchitai28', 'ngchitai28')
print("Tool đã chạy :))")

time.sleep(3)

def toicho_nhanjosb():
    """Nhấp vào nút nhận jobs."""
    time.sleep(random.uniform(2, 4))
    xpath_toicho_nhanjosb = '/html/body/div/div/div[2]/div/div/div[2]/i'
    click_element(xpath_toicho_nhanjosb)
    time.sleep(random.uniform(1, 2))
    xpath_chuyenhuong = '/html/body/div/div/div[1]/div[2]/span/div[5]/div/div/div[2]/div[2]/div/div'
    click_element(xpath_chuyenhuong)
    time.sleep(random.uniform(2, 4))

def nhan_jobs():
    time.sleep(random.uniform(1, 3))
    """Nhấp vào nút nhận jobs."""
    xpath_jobs = '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[2]/div'
    click_element(xpath_jobs)
    time.sleep(random.uniform(1, 3))
def lam_jobs():
    time.sleep(3)

    """Nhấp vào phần tử làm jobs và quay lại tab cũ."""
    xpath_lam_jobs = '/html/body/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[2]/a' # bấm vào shoppe chuyển hướng tới shopee rồi quay lại
    click_element(xpath_lam_jobs)

    current_window = driver.current_window_handle
    time.sleep(2)

    new_windows = [window for window in driver.window_handles if window != current_window]
    if new_windows:
        driver.switch_to.window(new_windows[0])
        time.sleep(2)
        driver.close()  # Đóng tab mới nếu không cần thiết
        driver.switch_to.window(current_window)
        print("Đã thực hiện lam_jobs và quay về tab cũ.")
    else:
        print("Không có tab mới nào được mở.")
def is_captcha_visible():
    """Kiểm tra xem CAPTCHA có hiển thị hay không."""
    captcha_xpath = '/html/body/div[2]'  # Thay đổi thành XPath thực tế của CAPTCHA
    try:
        captcha_element = driver.find_element(By.XPATH, captcha_xpath)
        return captcha_element.is_displayed()
    except NoSuchElementException:
        return False

def hoanthanh_jobs():
    """Nhấp vào nút hoàn thành jobs."""
    time.sleep(5)
    
    
    try:
        xpath_hoanthanh_jobs = '/html/body/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[2]/button'
        hoanthanh_button = wait_for_element(xpath_hoanthanh_jobs)
        if hoanthanh_button:
            hoanthanh_button.click()
            print("Đã nhấp vào nút hoàn thành jobs.")
            
            nhan_jobs()
                
                # Kiểm tra xem CAPTCHA có hiển thị không
            while is_captcha_visible():
                    print("Vui lòng giải CAPTCHA trước khi tiếp tục...")
                    time.sleep(5)  # Chờ một thời gian trước khi kiểm tra lại
    except NoSuchElementException:
        print("Không tìm thấy nút hoàn thành jobs.")
try:
    toicho_nhanjosb()
    while True:  # Vòng lặp chính để thực hiện nhiều jobs
        nhan_jobs()
        lam_jobs()
        hoanthanh_jobs()
        # Thêm điều kiện để thoát khỏi vòng lặp nếu cần
        # Ví dụ: if some_condition: break
except Exception as e:
    print(f"Lỗi không mong muốn xảy ra: {e}")

