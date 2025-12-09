import pytest
from selenium import webdriver
import os
import time
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            try:
                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_filename = f"{item.name}__{timestamp}.png"
                screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_filename)
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"Error capturing screenshot: {e}")

def pytest_configure(config):
    if hasattr(config, '_html'):
        config._html.title = "Signup Test Report"