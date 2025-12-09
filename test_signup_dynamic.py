import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==================== ĐỌC FILE JSON ====================
def load_test_data(json_file="test_signup_cases.json"):
    """Đọc file JSON"""
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


# Load data
TEST_DATA = load_test_data()
CONFIG = TEST_DATA.get("config", {})
BASE_URL = CONFIG.get("base_url", "https://webtestingteam14.vercel.app/signup.html")
TIMEOUT = CONFIG.get("default_timeout", 10)
SLEEP_TIME = CONFIG.get("default_sleep", 3)


# ==================== HÀM ĐIỀN FORM ====================
def fill_signup_form(driver, input_data):
    """Điền form đăng ký"""
    driver.get(BASE_URL)
    if "first" in input_data:
        driver.find_element(By.ID, "firstName").clear()
        driver.find_element(By.ID, "firstName").send_keys(input_data["first"])

    if "last" in input_data:
        driver.find_element(By.ID, "lastName").clear()
        driver.find_element(By.ID, "lastName").send_keys(input_data["last"])

    if "email" in input_data:
        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys(input_data["email"])

    if "password" in input_data:
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(input_data["password"])

    if "confirm" in input_data:
        driver.find_element(By.ID, "confirmPassword").clear()
        driver.find_element(By.ID, "confirmPassword").send_keys(input_data["confirm"])

    terms_checkbox = driver.find_element(By.ID, "terms")
    accept_terms = input_data.get("accept_terms")

    if accept_terms is not None:
        if accept_terms and not terms_checkbox.is_selected():
            terms_checkbox.click()
        elif not accept_terms and terms_checkbox.is_selected():
            terms_checkbox.click()

    force_submit = input_data.get("force_submit", False)
    if accept_terms or force_submit:
        if force_submit and not accept_terms:
            driver.execute_script(
                """document.querySelector('#signupBtn').dispatchEvent(new MouseEvent('click'));"""
            )
        else:
            driver.find_element(By.ID, "signupBtn").click()

        time.sleep(SLEEP_TIME)


def execute_actions(driver, actions):
    driver.get(BASE_URL)

    for action in actions:
        action_type = action.get("type")
        target = action.get("target")

        if action_type == "click_link":
            element = driver.find_element(By.LINK_TEXT, target)
            element.click()

        elif action_type == "click_checkbox":
            element = driver.find_element(By.ID, target)
            element.click()

        elif action_type == "click_button":
            element = driver.find_element(By.ID, target)
            element.click()

        elif action_type == "wait":
            duration = action.get("duration", 1)
            time.sleep(duration)

        elif action_type == "check_element_state":
            element = driver.find_element(By.ID, target)
            expected = action.get("expected")

            if expected == "enabled":
                assert element.is_enabled(), f"Element {target} phải enabled"
            elif expected == "disabled":
                assert not element.is_enabled(), f"Element {target} phải disabled"
            elif expected == "checked":
                assert element.is_selected(), f"Element {target} phải checked"
            elif expected == "unchecked":
                assert not element.is_selected(), f"Element {target} phải unchecked"

def verify_output(driver, output_data):
    wait = WebDriverWait(driver, TIMEOUT)

    if "toast" in output_data and output_data["toast"]:
        toast = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "toast"))
        )
        assert output_data["toast"] in toast.text

    if "redirect" in output_data and output_data["redirect"]:
        wait.until(EC.url_contains(output_data["redirect"]))
        assert output_data["redirect"] in driver.current_url

    if "errors" in output_data:
        for error_id, error_text in output_data["errors"].items():
            if error_text:
                element = driver.find_element(By.ID, error_id)
                assert error_text in element.text

def create_test(test_case):
    def generated(driver):
        if "actions" in test_case:
            execute_actions(driver, test_case["actions"])
        else:
            fill_signup_form(driver, test_case.get("input", {}))
        verify_output(driver, test_case.get("output", {}))
    generated.__name__ = f"test_{test_case['id']}"
    generated.__doc__ = test_case.get("description", "")
    return generated

# Tạo test functions
for test_case in TEST_DATA.get("test_cases", []):
    t_func = create_test(test_case)
    globals()[t_func.__name__] = t_func
