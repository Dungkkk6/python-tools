import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import multiprocessing

 
class FacebookManager:
    a = 0
    b = 1
    def __init__(self):
        self.accounts = []
        self.posts = []
        self.comments = []
        self.data_file = "facebook_data.json"

    def load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.accounts = data.get('accounts', [])
                self.posts = data.get('posts', [])
                self.comments = data.get('comments', [])
            print("Đã tải dữ liệu thành công.")
        except FileNotFoundError:
            print(f"Không tìm thấy file {self.data_file}. Tạo mới dữ liệu.")
        except json.JSONDecodeError:
            print(f"Lỗi khi đọc file {self.data_file}. Đảm bảo file có định dạng JSON hợp lệ.")

    def save_data(self):
        data = {
            'accounts': self.accounts,
            'posts': self.posts,
            'comments': self.comments
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Đã lưu dữ liệu thành công.")

    def add_account(self):
        email = input("Nhập email: ")
        password = input("Nhập mật khẩu: ")
        self.accounts.append({"email": email, "password": password})
        print("Đã thêm tài khoản thành công.")
        self.save_data()

    def add_post(self):
        post = input("Nhập nội dung bài đăng mẫu: ")
        self.posts.append(post)
        print("Đã thêm bài đăng mẫu thành công.")
        self.save_data()

    def add_comment(self):
        comment = input("Nhập nội dung bình luận mẫu: ")
        self.comments.append(comment)
        print("Đã thêm bình luận mẫu thành công.")
        self.save_data()

    def login_and_post(self, email, password, post_content, window_position):
        options = webdriver.FirefoxOptions()
    # Đặt kích thước cửa sổ cho vừa với màn hình
        options.add_argument("--width=200")
        options.add_argument("--height=500")
    
        driver = webdriver.Firefox(options=options)
        
        try:
            driver.set_window_size(200, 500)  # Kích thước cửa sổ 400x300 pixel
            driver.set_window_position(window_position[0], window_position[1])  # Vị trí cửa sổ
            driver.get('https://www.facebook.com')
            email_input = driver.find_element(By.ID, 'email')
            email_input.send_keys(email)
            password_input = driver.find_element(By.ID, 'pass')
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
            time.sleep(10)

            element = driver.find_element(By.CSS_SELECTOR, 'a.x1emribx')
            element.click()
            time.sleep(5)

            element2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.xmjcpbm:nth-child(2)'))
            )
            element2.click()
            time.sleep(5)

            post_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.xmper1u > div:nth-child(1)'))
            )
            for char in post_content:
                post_box.send_keys(char)
                time.sleep(0.1)

            time.sleep(5)
            post_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.xcud41i:nth-child(2) > div:nth-child(1) > div:nth-child(1)'))
            )
            post_button.click()

            print(f"Đã đăng bài thành công cho tài khoản {email}")
        except Exception as e:
            print(f"Đăng bài thất bại cho tài khoản {email}: {e}")
        finally:
            time.sleep(10)
            driver.quit()

    def run_multi_accounts(self): 
        if not self.accounts:
            print("Chưa có tài khoản nào. Vui lòng thêm tài khoản trước.")
            return

        if not self.posts:
            print("Chưa có bài đăng mẫu nào. Vui lòng thêm bài đăng trước.")
            return

        print("Chọn bài đăng:")
        for idx, post in enumerate(self.posts, 1):
            print(f"{idx}. {post[:50]}..." if len(post) > 50 else f"{idx}. {post}")
        
        while True:
            try:
                choice = int(input("Nhập số thứ tự bài đăng: ")) - 1
                if 0 <= choice < len(self.posts):
                    post_content = self.posts[choice]
                    break
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            except ValueError:
                print("Vui lòng nhập một số.")

        # Tính toán số lượng cột và hàng để xếp cửa sổ

        processes = []
        for idx, account in enumerate(self.accounts):
           
            window_position = (idx * 450, 0)  
            p = multiprocessing.Process(target=self.login_and_post, 
                                        args=(account['email'], account['password'], post_content, window_position))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()
    
    def run_multi_accounts_autoComent(self): 
        if not self.accounts:
            print("Chưa có tài khoản nào. Vui lòng thêm tài khoản trước.")
            return

        if not self.comments:
            print("Chưa có bình luân mẫu nào. Vui lòng thêm bình luân  trước.")
            return

        print("Chọn bình luận :")
        for idx, post in enumerate(self.comments, 1):
            print(f"{idx}. {post[:50]}..." if len(post) > 50 else f"{idx}. {post}")
        
        while True:
            try:
                choice = int(input("Nhập số thứ tự binhf luan : ")) - 1
                if 0 <= choice < len(self.comments):
                    commnet_content = self.comments[choice]
                    break
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            except ValueError:
                print("Vui lòng nhập một số.")

        # Tính toán số lượng cột và hàng để xếp cửa sổ

        processes = []
        for idx, account in enumerate(self.accounts):
           
            window_position = (idx * 450, 0)  
            p = multiprocessing.Process(target=self.login_and_comment, 
                                        args=(account['email'], account['password'], commnet_content , window_position))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()
            
    def login_and_comment(self, email, password, comment_content, window_position):
        options = webdriver.FirefoxOptions()
    # Đặt kích thước cửa sổ cho vừa với màn hình
        options.add_argument("--width=200")
        options.add_argument("--height=500")
    
        driver = webdriver.Firefox(options=options)
        
        try:
            driver.set_window_size(200, 500)  # Kích thước cửa sổ 400x300 pixel
            driver.set_window_position(window_position[0], window_position[1])  # Vị trí cửa sổ
            driver.get('https://www.facebook.com')
            email_input = driver.find_element(By.ID, 'email')
            for char in  email:
                email_input.send_keys(char)
                time.sleep(0.1)
                
            time.sleep(3)
            
            password_input = driver.find_element(By.ID, 'pass')
            for char in  password:
                password_input.send_keys(char)
                time.sleep(0.1)
            time.sleep(4)
            password_input.send_keys(Keys.ENTER)
            time.sleep(7)
            
            # đàau tiên get link bài viét 
            driver.get('https://www.facebook.com/share/v/CCSvugU48jFFEQMF/')
            
            time.sleep(3)
            # trỏ đến css bình luan selector 
            elementCommentButton = driver.find_element(By.CSS_SELECTOR, 'div.xjl7jj:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(13) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
            print("A")
            elementCommentButton.click()
            time.sleep(3)
            
            time.sleep(3)
            # trỏ tiếp tơi css selector texbox 
            elementTextBox = driver.find_element(By.CSS_SELECTOR, 'div.xjl7jj:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(13) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)')
            elementTextBox.click()
            # time.sleep(3)
            #senkey 
           
            for char in  comment_content:
                
                elementTextBox.send_keys(char)
                print("b")
                time.sleep(0.01)
            time.sleep(3)
            
            # press enter 
            elementEnter = driver.find_element(By.CSS_SELECTOR, '#focused-state-composer-submit > span:nth-child(1) > div:nth-child(1)')
            elementEnter.click()
            time.sleep(5)

           
           

           

            print(f"Đã bình luận  thành công cho tài khoản {email}")
        except Exception as e:
            print(f"bình luận thất bại cho tài khoản {email}: {e}")
        finally:
            time.sleep(10)
            driver.quit()
    
    
    
    def login_and_comment_forPersonal(self, email, password, comment_content, window_position):
        options = webdriver.FirefoxOptions()
    # Đặt kích thước cửa sổ cho vừa với màn hình
        options.add_argument("--width=200")
        options.add_argument("--height=500")
    
        driver = webdriver.Firefox(options=options)
        
        try:
            driver.set_window_size(200, 500)  # Kích thước cửa sổ 400x300 pixel
            driver.set_window_position(window_position[0], window_position[1])  # Vị trí cửa sổ
            driver.get('https://www.facebook.com')
            email_input = driver.find_element(By.ID, 'email')
            for char in  email:
                email_input.send_keys(char)
                time.sleep(0.1)
                
            time.sleep(3)
            
            password_input = driver.find_element(By.ID, 'pass')
            for char in  password:
                password_input.send_keys(char)
                time.sleep(0.1)
            time.sleep(4)
            password_input.send_keys(Keys.ENTER)
            time.sleep(7)
            
            # đàau tiên get link bài viét 
            driver.get('https://www.facebook.com/share/v/CCSvugU48jFFEQMF/')
            
            time.sleep(3)
            # trỏ đến css bình luan selector 
            elementCommentButton = driver.find_element(By.CSS_SELECTOR, '.x1sy10c2 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)')
            print("A")
            elementCommentButton.click()
            time.sleep(3)
            
            time.sleep(3)
            # trỏ tiếp tơi css selector texbox 
            elementTextBox = driver.find_element(By.CSS_SELECTOR, '.x14wi4xw')
            elementTextBox.click()
            # time.sleep(3)
            #senkey 
           
            for char in  comment_content:
                
                elementTextBox.send_keys(char)
                print("b")
                time.sleep(0.01)
            time.sleep(3)
            
            # press enter 
            elementEnter = driver.find_element(By.CSS_SELECTOR, '#focused-state-composer-submit > span:nth-child(1) > div:nth-child(1)')
            elementEnter.click()
            time.sleep(5)

           
           

           

            print(f"Đã bình luận  thành công cho tài khoản {email}")
        except Exception as e:
            print(f"bình luận thất bại cho tài khoản {email}: {e}")
        finally:
            time.sleep(10)
            driver.quit()

    def run(self):
        self.load_data()
        while True:
            print("\n--- Quản lý tài khoản Facebook ---")
            print("1. Thêm tài khoản")
            print("2. Thêm bài đăng mẫu")
            print("3. Thêm bình luận mẫu")
            print("4. Chạy đăng bài trên nhiều tài khoản")
            print("5. Chạy binh luận trên nhiều tài khoản")
            print("6. Hiển thị dữ liệu hiện tại")
            print("7. Thoát")

            choice = input("Nhập lựa chọn của bạn: ")

            if choice == '1':
                self.add_account()
            elif choice == '2':
                self.add_post()
            elif choice == '3':
                self.add_comment()
            elif choice == '4':
                self.run_multi_accounts()
            elif choice == '5':
                self.run_multi_accounts_autoComent(); 
            
            elif choice == '6':
                print("\nTài khoản:")
                for account in self.accounts:
                    print(f"Email: {account['email']}")
                print("\nBài đăng mẫu:")
                for post in self.posts:
                    print(post)
                print("\nBình luận mẫu:")
                for comment in self.comments:
                    print(comment)
            elif choice == '7':
                print("Tạm biệt!")
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    manager = FacebookManager()
    manager.run()