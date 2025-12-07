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
    """Create and cleanup Chrome driver"""
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()


# ------------------- Hook để chụp screenshot và thêm vào HTML report -------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure and add to HTML report"""
    outcome = yield
    report = outcome.get_result()

    # Chỉ xử lý khi test call (không phải setup/teardown)
    if report.when == "call":
        driver = item.funcargs.get("driver", None)

        # Thêm description từ docstring
        test_description = item.function.__doc__ if item.function.__doc__ else "No description"
        report.description = test_description

        # Nếu test FAIL → chụp screenshot
        if report.failed and driver:
            try:
                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_filename = f"{item.name}__{timestamp}.png"
                screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_filename)

                # Lưu screenshot
                driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot saved: {screenshot_path}")

                # Thêm screenshot vào HTML report
                if hasattr(report, 'extra'):
                    extra = getattr(report, 'extra', [])
                else:
                    # Tạo extra nếu chưa có
                    extra = []

                # Dùng pytest-html để thêm ảnh
                from pytest_html import extras
                extra.append(extras.image(screenshot_path))

                report.extra = extra

            except Exception as e:
                print(f"❌ Error capturing/adding screenshot: {e}")
                import traceback
                traceback.print_exc()


# ------------------- Hook để configure HTML report -------------------
def pytest_configure(config):
    """Configure pytest-html report"""
    if hasattr(config, '_html'):
        config._html.title = "Signup Test Report"


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Signup Form - Test Report"


# ------------------- Optional: Add test metadata -------------------
def pytest_collection_modifyitems(items):
    """Add markers and metadata to tests"""
    for item in items:
        # Add marker based on test name
        if "tc001" in item.nodeid or "tc002" in item.nodeid:
            item.add_marker(pytest.mark.smoke)

        # Add marker for validation tests
        if any(x in item.nodeid for x in ["tc007", "tc008", "tc009", "tc015", "tc016"]):
            item.add_marker(pytest.mark.validation)

        # Add marker for UI tests
        if any(x in item.nodeid for x in ["tc029", "tc030", "tc031", "tc032"]):
            item.add_marker(pytest.mark.ui)