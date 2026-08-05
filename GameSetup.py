import chess
import time
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

class GameSetup:
    def __init__(self, driver):
        self._driver = driver

    def start_as_guest(self) -> None:
        try:
            button = WebDriverWait(self._driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Start Game']]")))
            button.click()
            button = WebDriverWait(self._driver, 5).until(
                EC.presence_of_element_located((By.ID,"guest-button")))
            button.click()
        except Exception:
            raise RuntimeError("Failed to start the game as a guest")

    def enable_show_legal_moves(self) -> None:

        self._driver.get("https://www.chess.com/settings/gameplay")

        always_queen_label = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//h4[.//span[text()='Всегда превращать в ферзя']]/parent::div//label",
            ))
        )
        always_queen_label.click()

        show_moves_label = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//h4[.//span[text()='Показывать допустимые ходы']]/parent::div//label",
            ))
        )
        show_moves_label.click()

        WebDriverWait(self._driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "save-success-status-icon"))
        )
        WebDriverWait(self._driver, 5).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "save-success-status-icon"))
        )

        self._driver.get("https://www.chess.com/play/online")



    def start_game(self) -> None:


        button = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//button[.//span[text()='Начать партию']]"
            ))
        )
        button.click()
        WebDriverWait(self._driver, 60).until_not(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "[data-test-element='user-tagline-username']"),
                "Противник"
            )
        )

    def select_time_control(self, time_label: str = "3 min") -> None:
        self._driver.find_element(
            By.CSS_SELECTOR, ".cc-dropdown-button-component"
        ).click()

        # Выбираем нужное время
        WebDriverWait(self._driver, 5).until(
            EC.presence_of_element_located((
                By.XPATH, f"//button[.//span[text()='{time_label}']]"
            ))
        ).click()

    def start_new_game(self) -> None:
        try:
            button = WebDriverWait(self._driver, 30).until(
                EC.presence_of_element_located((
                    By.XPATH, "//button[.//span[text()='Новая 3 мин.']]"
                ))
            )
            self._driver.execute_script("arguments[0].click();", button)
        except TimeoutException:
            self._driver.save_screenshot("game_over_screen.png")
            raise
        self._driver.execute_script("arguments[0].click();", button)

    def wait_for_new_game(self) -> None:
        WebDriverWait(self._driver, 30).until_not(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[class*='game-over-modal']"
            ))
        )
        WebDriverWait(self._driver, 60).until_not(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "[data-test-element='user-tagline-username']"),
                "Противник"
            )
        )