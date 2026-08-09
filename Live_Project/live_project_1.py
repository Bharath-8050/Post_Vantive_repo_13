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

# Create evidence folder if it doesn't exist
if not os.path.exists("evidence"):
    os.makedirs("evidence")

@pytest.fixture(scope="function")
def driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Use ChromeDriverManager to automatically handle binary download
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

@pytest.mark.parametrize("username", [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
])
def test_login_combinations(driver, username):
    print(f"\n--- Starting test for user: {username} ---")
    print("Step 1: Navigating to SauceDemo website")
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)
    
    # Login
    print(f"Step 2: Entering username: {username}")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(username)
    time.sleep(0.5)
    
    print("Step 3: Entering password")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    time.sleep(0.5)
    
    print("Step 4: Clicking login button")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    
    if username == "locked_out_user":
        print("Step 5: Verifying error message for locked_out_user")
        # Expect error message
        error_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
        )
        driver.save_screenshot(f"evidence/login_failure_{username}.png")
        assert "locked out" in error_elem.text.lower()
        print("Result: Locked out user error verified successfully")
    else:
        print("Step 5: Verifying successful navigation to inventory page")
        # Expect successful navigation to inventory page
        WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
        driver.save_screenshot(f"evidence/login_success_{username}.png")
        assert "inventory.html" in driver.current_url
        
        # Check if the products are visible
        print("Step 6: Checking if products are visible")
        inventory_list = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(inventory_list) > 0
        print(f"Result: Login successful for {username}, {len(inventory_list)} items found")

def test_invalid_login(driver):
    print("\n--- Starting test: Invalid Login (Wrong Password) ---")
    print("Step 1: Navigating to SauceDemo website")
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)
    
    print("Step 2: Entering valid username 'standard_user'")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    time.sleep(0.5)
    
    print("Step 3: Entering invalid password 'wrong_password'")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    time.sleep(0.5)
    
    print("Step 4: Clicking login button")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    
    print("Step 5: Verifying error message is displayed")
    error_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )
    
    error_text = error_elem.text
    print(f"Step 6: Error message found: '{error_text}'")
    
    driver.save_screenshot("evidence/login_invalid_password.png")
    assert "Username and password do not match" in error_text
    print("Result: Invalid login test passed successfully")

def test_performance_glitch_user_timing(driver):
    print("\n--- Starting test: Performance Glitch User Timing ---")
    print("Step 1: Navigating to SauceDemo website")
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)
    
    print("Step 2: Entering performance_glitch_user credentials")
    driver.find_element(By.ID, "user-name").send_keys("performance_glitch_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    
    start_time = time.time()
    print("Step 3: Clicking login button and timing the delay")
    driver.find_element(By.ID, "login-button").click()
    
    # Wait for inventory page
    WebDriverWait(driver, 15).until(EC.url_contains("inventory.html"))
    driver.save_screenshot("evidence/performance_glitch_login.png")
    end_time = time.time()
    
    duration = end_time - start_time
    print(f"Step 4: Login took {duration:.2f} seconds")
    # Performance glitch user usually has a 5-second delay
    assert duration >= 5
    print("Result: Performance delay verified successfully")

def test_error_user_cart_add_fail(driver):
    print("\n--- Starting test: Error User Cart Add Failure ---")
    print("Step 1: Navigating to SauceDemo website")
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)
    
    print("Step 2: Logging in as error_user")
    driver.find_element(By.ID, "user-name").send_keys("error_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    
    print("Step 3: Attempting to add all items to cart")
    inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    for item in inventory_items:
        btn = item.find_element(By.CSS_SELECTOR, "button[id^='add-to-cart']")
        btn.click()
        time.sleep(0.2)
    
    # Check cart count. If it's less than total items, error_user behavior is confirmed.
    print("Step 4: Checking cart count badge")
    cart_badge = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    driver.save_screenshot("evidence/error_user_cart_fail.png")
    count = int(cart_badge[0].text) if cart_badge else 0
    print(f"Step 5: Cart count for error_user is {count} (expected < {len(inventory_items)})")
    assert count < len(inventory_items), "error_user should have failed to add some items"
    print("Result: Error user behavior in cart verified")

def test_error_user_checkout_fail(driver):
    print("\n--- Starting test: Error User Checkout Failure ---")
    print("Step 1: Navigating to SauceDemo website")
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)
    
    print("Step 2: Logging in as error_user")
    driver.find_element(By.ID, "user-name").send_keys("error_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    
    # Add an item that DOES work (e.g. Backpack)
    print("Step 3: Adding backpack to cart")
    try:
        btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
        btn.click()
    except Exception as e:
        print(f"Warning: Could not add item to cart: {e}")
    time.sleep(0.5)
    
    # Go to cart
    print("Step 4: Navigating to cart")
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(0.5)
    
    # Checkout
    print("Step 5: Clicking checkout")
    try:
        checkout_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout")))
        checkout_btn.click()
        time.sleep(0.5)
        
        # Fill info
        print("Step 6: Filling checkout information")
        driver.find_element(By.ID, "first-name").send_keys("Test")
        # error_user often fails to fill the last name or has issues here
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        time.sleep(0.5)
        
        # Continue
        print("Step 7: Clicking continue")
        driver.find_element(By.ID, "continue").click()
        time.sleep(1)
    except Exception as e:
        print(f"Step 5-7: Encountered expected or handled error: {e}")
    
    # Check for error message or that we didn't reach the final step
    print("Step 8: Verifying if checkout failed or stayed on current page")
    error_elem = driver.find_elements(By.CSS_SELECTOR, "h3[data-test='error']")
    driver.save_screenshot("evidence/error_user_checkout_fail.png")
    assert len(error_elem) > 0 or "checkout-step-two.html" not in driver.current_url
    print("Result: Error user checkout failure verified")

def test_problem_user_broken_images(driver):
    print("\n--- Starting test: Problem User Broken Images ---")
    print("Step 1: Navigating to SauceDemo website")
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)
    
    print("Step 2: Logging in as problem_user")
    driver.find_element(By.ID, "user-name").send_keys("problem_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    
    # Find all product images
    print("Step 3: Inspecting product image sources")
    images = driver.find_elements(By.CLASS_NAME, "inventory_item_img")
    # For problem_user, all images usually have the same incorrect source
    srcs = [img.get_attribute("src") for img in images if img.tag_name == 'img']
    # Sometimes it's the class name that matters, let's look for actual <img> tags
    img_tags = driver.find_elements(By.CSS_SELECTOR, ".inventory_item_img img")
    srcs = [img.get_attribute("src") for img in img_tags]
    
    print(f"Step 4: Found {len(srcs)} images. Checking for uniqueness.")
    driver.save_screenshot("evidence/problem_user_broken_images.png")
    assert len(set(srcs)) == 1, "Problem user should see broken/duplicate images"
    print("Result: Problem user broken images verified")

def test_logout(driver):
    print("\n--- Starting test: Logout ---")
    print("Step 1: Navigating to SauceDemo website")
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)
    
    print("Step 2: Logging in as standard_user")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    
    # Open menu
    print("Step 3: Opening sidebar menu")
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    
    # Small sleep for animation
    time.sleep(1)
    
    # Wait and click logout using JavaScript to avoid issues with menu animation
    print("Step 4: Clicking logout button")
    logout_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "logout_sidebar_link"))
    )
    driver.execute_script("arguments[0].click();", logout_btn)
    time.sleep(1)
    
    print("Step 5: Verifying redirection to login page")
    WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/"))
    driver.save_screenshot("evidence/logout_success.png")
    assert driver.current_url == "https://www.saucedemo.com/"
    print("Result: Logout successful")