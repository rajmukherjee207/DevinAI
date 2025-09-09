
# tests/test_ui_iamdave.py

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.iamdave.ai"


@pytest.fixture(scope="module")
def driver():
    """Setup and teardown for Selenium WebDriver"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(5)  # global implicit wait
    yield driver
    driver.quit()


def slow_down(seconds=2):
    """Utility to make test runs human-visible"""
    time.sleep(seconds)


def test_homepage_loads_and_title(driver):
    driver.get(BASE_URL)
    slow_down()
    assert "DaveAI" in driver.title


@pytest.mark.smoke
def test_logo_presence(driver):
    driver.get(BASE_URL)
    logo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "a img"))
    )
    slow_down()
    assert logo.is_displayed()


def test_navigation_to_about_page(driver):
    driver.get(BASE_URL)

    about_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='menu-1-f7988a7']/li[1]/a"))
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", about_link)
    driver.execute_script("arguments[0].click();", about_link)

    WebDriverWait(driver, 10).until(EC.url_contains("about-us"))
    slow_down()
    assert "about-us" in driver.current_url.lower()


def test_specific_heading_on_homepage(driver):
    driver.get(BASE_URL)
    heading = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h1"))
    )
    slow_down()
    assert heading.is_displayed()


# -------------------- Helpers for Book Demo test -------------------- #

def wait_for_thankyou(driver, timeout=9):
    """Polls current_url until it contains /thank-you (max `timeout` seconds)."""
    end = time.time() + timeout
    while time.time() < end:
        if "/thank-you" in driver.current_url:
            return True
        time.sleep(0.5)
    return False


def switch_to_form_frame_if_present(driver):
    """If a form lives inside an iframe, switch into it; else stay on default."""
    driver.switch_to.default_content()
    for frm in driver.find_elements(By.TAG_NAME, "iframe"):
        driver.switch_to.frame(frm)
        # any form controls present?
        if driver.find_elements(By.CSS_SELECTOR, "form input, form textarea, form select"):
            return True
        driver.switch_to.default_content()
    return False


# -------------------- Book Demo flow (only waits after Submit) -------------------- #

def test_book_demo_form(driver):
    driver.get(BASE_URL)

    # Click "Book Demo" (use JS to avoid sticky headers/overlays)
    book_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'book-demo')]"))
    )
    driver.execute_script("arguments[0].click();", book_btn)

    # If a new tab/window opened, switch to it
    try:
        driver.switch_to.window(driver.window_handles[-1])
    except Exception:
        pass

    # Best-effort: dismiss consent if present (non-blocking)
    try:
        consent = driver.find_element(
            By.XPATH, "//button[contains(.,'Accept') or contains(.,'Agree') or contains(.,'OK') or contains(.,'Got it')]"
        )
        driver.execute_script("arguments[0].click();", consent)
    except Exception:
        pass

    # Enter the form (iframe if needed)
    in_frame = switch_to_form_frame_if_present(driver)
    if not in_frame:
        driver.switch_to.default_content()

    # Scope to the form element
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form"))
    )

    # Fields (relative to form)
    name_input    = form.find_element(By.XPATH, ".//input[contains(@id,'name')]")
    email_input   = form.find_element(By.XPATH, ".//input[@type='email']")
    company_input = form.find_element(By.XPATH, ".//input[@id='form-field-field_93bc8cc']")  # relative XPath
    service_sel   = form.find_element(By.XPATH, ".//select")
    phone_input   = form.find_element(By.XPATH, ".//input[@type='tel']")
    message_box   = form.find_element(By.XPATH, ".//textarea")

    # Fill quickly (no extra waits)
    name_input.clear();    name_input.send_keys("Test User")
    email_input.clear();   email_input.send_keys("hr@sidssol.com")  # work-like email to pass validation
    company_input.clear(); company_input.send_keys("Test Company")
    phone_input.clear();   phone_input.send_keys("1234567890")
    message_box.clear();   message_box.send_keys("This is a test automation message.")
    Select(service_sel).select_by_visible_text("AI Chatbot")

    # Submit (JS click the <button> to avoid span/overlay interception)
    submit_btn = form.find_element(By.XPATH, ".//button[@type='submit']")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
    driver.execute_script("arguments[0].click();", submit_btn)

    # ✅ Only wait here for the Thank You page (max 9s)
    assert wait_for_thankyou(driver, timeout=9), f"Did not reach thank-you. URL: {driver.current_url}"
    assert "/thank-you" in driver.current_url
