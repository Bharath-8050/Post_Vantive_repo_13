import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random
import string

# Create evidence folder if it doesn't exist
if not os.path.exists("evidence"):
    os.makedirs("evidence")

class JPetStoreActions:
    def __init__(self, driver, evidence_folder="evidence"):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.evidence_folder = evidence_folder

    def enter_store(self):
        print("Step: Entering the store")
        self.driver.get("https://petstore.octoperf.com/")
        enter_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Enter the Store")))
        enter_link.click()
        time.sleep(1)

    def navigate_to_registration(self):
        print("Step: Navigating to registration page")
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign In"))).click()
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register Now!"))).click()
        time.sleep(1)

    def register_user(self, username, password):
        print(f"Step: Registering user: {username}")
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "repeatedPassword").send_keys(password)
        
        self.driver.find_element(By.NAME, "account.firstName").send_keys("Junie")
        self.driver.find_element(By.NAME, "account.lastName").send_keys("Bot")
        self.driver.find_element(By.NAME, "account.email").send_keys(f"{username}@example.com")
        self.driver.find_element(By.NAME, "account.phone").send_keys("1234567890")
        self.driver.find_element(By.NAME, "account.address1").send_keys("123 Selenium St")
        self.driver.find_element(By.NAME, "account.city").send_keys("Automation City")
        self.driver.find_element(By.NAME, "account.state").send_keys("TestState")
        self.driver.find_element(By.NAME, "account.zip").send_keys("12345")
        self.driver.find_element(By.NAME, "account.country").send_keys("USA")
        
        # Optional preferences
        self.driver.find_element(By.NAME, "newAccount").click()
        time.sleep(1)
        self.driver.save_screenshot(f"{self.evidence_folder}/registration_{username}.png")
        print("Result: Registration form submitted")

    def login(self, username, password):
        print(f"Step: Logging in as user: {username}")
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign In"))).click()
        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").clear()
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "signon").click()
        time.sleep(1)
        self.driver.save_screenshot(f"{self.evidence_folder}/login_{username}.png")
        
        # Verify login
        welcome_msg = self.driver.find_elements(By.ID, "WelcomeContent")
        assert len(welcome_msg) > 0, "Login failed!"
        print(f"Result: Login successful for {username}")

    def add_random_item_from_category(self, category_name):
        print(f"Step: Selecting random item from {category_name}")
        # Click category from sidebar or top menu
        category_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@id='QuickLinks']//a[contains(@href, '{category_name.upper()}')]")))
        category_link.click()
        time.sleep(1)
        
        # Select a random product
        products = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table//a[contains(@href, 'productId=')]")))
        random.choice(products).click()
        time.sleep(1)
        
        # Select a random item and add to cart
        items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[text()='Add to Cart']")))
        random.choice(items).click()
        time.sleep(1)
        print(f"Result: Item from {category_name} added to cart")
        self.driver.save_screenshot(f"{self.evidence_folder}/add_to_cart_{category_name}.png")

    def checkout(self):
        print("Step: Proceeding to checkout")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Proceed to Checkout']"))).click()
        time.sleep(1)
        
        print("Step: Confirming payment and billing")
        self.wait.until(EC.element_to_be_clickable((By.NAME, "newOrder"))).click()
        time.sleep(1)
        
        print("Step: Confirming order")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Confirm']"))).click()
        time.sleep(1)
        
        self.driver.save_screenshot(f"{self.evidence_folder}/order_confirmation.png")
        
        # Verify order completion
        confirmation_msg = self.driver.find_element(By.CLASS_NAME, "messages").text
        assert "Thank you" in confirmation_msg
        print(f"Result: Order placed successfully. {confirmation_msg}")

    def logout(self):
        print("Step: Logging out")
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Out"))).click()
        time.sleep(1)
        self.driver.save_screenshot(f"{self.evidence_folder}/logout.png")
        print("Result: Logout successful")

@pytest.fixture(scope="function")
def driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_jpetstore_full_flow(driver):
    # Generate unique folder
    unique_run_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    run_folder = os.path.join("evidence", f"run_{time.strftime('%Y%m%d_%H%M%S')}_{unique_run_id}")
    os.makedirs(run_folder, exist_ok=True)
    print(f"\nStep: Created new random folder for screenshots: {run_folder}")

    actions = JPetStoreActions(driver, run_folder)
    
    # Generate unique username
    unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    username = f"user_{unique_id}"
    password = "password123"
    
    # Log user details
    log_file = os.path.join(run_folder, "user_details.log")
    with open(log_file, "w") as f:
        f.write(f"--- User Details ---\n")
        f.write(f"Username: {username}\n")
        f.write(f"Password: {password}\n")
        f.write(f"First Name: Junie\n")
        f.write(f"Last Name: Bot\n")
        f.write(f"Email: {username}@example.com\n")
        f.write(f"Timestamp: {time.ctime()}\n")
    print(f"Step: User details logged to {log_file}")
    
    actions.enter_store()
    actions.navigate_to_registration()
    actions.register_user(username, password)
    actions.login(username, password)
    
    actions.add_random_item_from_category("FISH")
    actions.add_random_item_from_category("DOGS")
    
    actions.checkout()
    actions.logout()
