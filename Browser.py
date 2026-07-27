from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Browser:
    def __init__(self, headless: bool = False):
        self._headless = headless
        self._driver = None

    @property
    def driver(self):
        if self._driver is None:
            raise RuntimeError("Browser is not started")

        return self._driver

    def __enter__(self):
        options = Options()
        options.add_argument(r"--user-data-dir=C:\chrome_profile\chess_bot")

        if self._headless:
            options.add_argument("--headless")

        self._driver = webdriver.Chrome(options=options)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._driver:
            self._driver.quit()
            self._driver = None

    def open(self, url: str) -> None:
        self.driver.get(url)

    def login_automatically(self, username_or_email: str, password: str) -> None:
        self.open("https://www.chess.com/login")

        try:
            # 1. Ждем появления поля логина
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login-username"))
            )

            # 2. Находим поле пароля
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")

            # 3. Находим кнопку входа
            login_button = self.driver.find_element(By.ID, "login")

            # Вводим данные через JavaScript (это обходит ошибку 'invalid element state')
            self.driver.execute_script("arguments[0].value = arguments[1];", username_field, username_or_email)
            self.driver.execute_script("arguments[0].value = arguments[1];", password_field, password)

            # Триггерим событие изменения, чтобы Vue.js на сайте понял, что текст введён
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                                       username_field)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                                       password_field)

            # Кликаем "Войти"
            login_button.click()

            # Ждем, пока загрузится интерфейс авторизованного пользователя
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "nav-link-profile"))
            )
            print("[+] Автоматический вход выполнен успешно!")

        except Exception as e:
            print(f"[-] Ошибка авто-логина: {e}")
            print("[!] Скорее всего, chess.com выкатил капчу или изменил ID кнопки пароля.")
            input("Решите капчу в браузере вручную и нажмите Enter для продолжения...")

