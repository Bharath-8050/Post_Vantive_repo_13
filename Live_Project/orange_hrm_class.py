import time
from os import name

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class LoginPage:
    def __init__(self,driver):
        self.driver = driver
        # self.username=name
        # self.password=assword
    def Orange_HRM(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        self.driver.maximize_window()
        time.sleep(2)
        self.driver.implicitly_wait(20)
        assert driver.title == "OrangeHRM"

    def login(self,username,password):
        self.driver.find_element(By.XPATH, "//*[@name='username']").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//*[@type='submit']").click()
        self.driver.implicitly_wait(10)
        assert driver.title == "OrangeHRM"


driver = webdriver.Chrome()
login_page = LoginPage(driver)
login_page.Orange_HRM()

login_page.login("Admin","admin123")
