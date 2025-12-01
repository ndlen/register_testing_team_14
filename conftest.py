# conftest.py
import pytest
from selenium import webdriver
import os
import time

# Thư mục lưu screenshot
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ------------------- Fixture Selenium -------------------
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# ------------------- Hook để chụp screenshot khi fail -------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    print("outcome:", outcome)
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            try:
                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_filename = f"{item.name}__{timestamp}.png"
                screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_filename)
                driver.save_screenshot(screenshot_path)
            except Exception as e:
                print(f"❌ Error capturing screenshot: {e}")



# ------------------- Hook để configure HTML report -------------------
def pytest_configure(config):
    """Configure pytest-html"""
    if hasattr(config, '_html'):
        config._html.title = "Test Report"