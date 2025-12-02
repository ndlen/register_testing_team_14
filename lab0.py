import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def signup(driver, first="", last="", email="", password="", confirm="", accept_terms=True):
    driver.get("https://webtestingteam14.vercel.app/signup.html")
    driver.find_element(By.ID, "firstName").clear()
    driver.find_element(By.ID, "firstName").send_keys(first)
    driver.find_element(By.ID, "lastName").clear()
    driver.find_element(By.ID, "lastName").send_keys(last)
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "confirmPassword").clear()
    driver.find_element(By.ID, "confirmPassword").send_keys(confirm)
    terms_checkbox = driver.find_element(By.ID, "terms")
    if accept_terms and not terms_checkbox.is_selected():
        terms_checkbox.click()
    elif not accept_terms and terms_checkbox.is_selected():
        terms_checkbox.click()
    driver.find_element(By.ID, "signupBtn").click()
    time.sleep(3)


# ---------- Test cases ----------

def test_tc001(driver):
    signup(driver, first="John", last="Doe", email="tc001@example.com", password="password123", confirm="password123")
    toast = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "toast"))
    )
    assert "Account created successfully! Redirecting to login..." in toast.text
    WebDriverWait(driver, 10).until(
        EC.url_contains("login.html")
    )
    assert "login.html" in driver.current_url

def test_tc002(driver):
    signup(driver, first="A", last="Doe", email="tc17@example.com",
           password="password123", confirm="password123")
    toast = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "toast"))
    )
    assert "Account created successfully! Redirecting to login..." in toast.text
    WebDriverWait(driver, 5).until(
        EC.url_contains("login.html")
    )
    assert "login.html" in driver.current_url

def test_tc003(driver):
    signup(driver, first="Join", last="Doe", email="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA@example.com", password="password123", confirm="password123")
    toast = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "toast"))
    )
    assert "Account created successfully! Redirecting to login..." in toast.text
    WebDriverWait(driver, 5).until(
        EC.url_contains("login.html")
    )
    assert "login.html" in driver.current_url

def test_tc004(driver):
    signup(driver,
           first="Join", last="Doe", email="tc026@example.com", password="password 123", confirm="password 123")
    toast = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "toast"))
    )
    assert "Account created successfully! Redirecting to login..." in toast.text
    WebDriverWait(driver, 5).until(
        EC.url_contains("login.html")
    )
    assert "login.html" in driver.current_url

def test_tc005(driver):
    signup(driver, first="Join", last="Doe", email="tc027@example.com", password="!@#$%^&*!", confirm="!@#$%^&*!")
    toast = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "toast"))
    )
    assert "Account created successfully! Redirecting to login..." in toast.text
    WebDriverWait(driver, 5).until(
        EC.url_contains("login.html")
    )
    assert "login.html" in driver.current_url

def test_tc006(driver):
    signup(driver, first="Join", last="Doe", email="TC028@GMAIL.COM", password="password123", confirm="password123")
    toast = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "toast"))
    )
    assert "Account created successfully! Redirecting to login..." in toast.text
    WebDriverWait(driver, 5).until(
        EC.url_contains("login.html")
    )
    assert "login.html" in driver.current_url

def test_tc007(driver):
    signup(driver, last="Doe", email="test11@example.com", password="password123", confirm="password123")
    assert "First name is required" in driver.find_element(By.ID, "firstNameError").text

def test_tc008(driver):
    signup(driver, first="   ", last="Doe", email="test2@example.com", password="password123", confirm="password123")
    assert "First name is required" in driver.find_element(By.ID, "firstNameError").text

def test_tc009(driver):
    signup(driver, first="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
           last="Doe", email="tc19@example.com",
           password="password123", confirm="password123")
    assert "First is too long" in driver.find_element(By.ID, "firstNameError").text

def test_tc010(driver):
    signup(driver, first="John@#$%", last="Doe", email="tc021@example.com", password="password123", confirm="password123")
    assert "First name must not contain special characters" in driver.find_element(By.ID, "firstNameError").text

def test_tc011(driver):
    signup(driver, first="John", last="Doe11", email="tc022@example.com", password="password123", confirm="password123")
    assert "Last name must not contain number characters" in driver.find_element(By.ID, "firstNameError").text

def test_tc012(driver):
    signup(driver, first="Jon", email="test2@example.com", password="password123", confirm="password123")
    assert "Last name is required" in driver.find_element(By.ID, "lastNameError").text

def test_tc013(driver):
    signup(driver, first="Jon", last="   ", email="test2@example.com", password="password123", confirm="password123")
    assert "Last name is required" in driver.find_element(By.ID, "lastNameError").text

def test_tc014(driver):
    signup(driver, first="John", last="Doe@#$%", email="tc023@example.com", password="password123", confirm="password123")
    assert "Last name must not contain special characters" in driver.find_element(By.ID, "lastNameError").text

def test_tc015(driver):
    signup(driver, first="John", last="Doe11", email="tc024@example.com", password="password123", confirm="password123")
    assert "Last name must not contain number characters" in driver.find_element(By.ID, "lastNameError").text

def test_tc016(driver):
    signup(driver, first="Jon", last="   ", password="password123", confirm="password123")
    assert "Email is required" in driver.find_element(By.ID, "emailError").text

def test_tc017(driver):
    signup(driver, first="Jon", last="Join", email="testexample.comm", password="password123", confirm="password123")
    assert "Please enter a valid email address" in driver.find_element(By.ID, "emailError").text

def test_tc018(driver):
    signup(driver, first="John", last="Doe", email="test@", password="password123", confirm="password123")
    assert "Please enter a valid email address" in driver.find_element(By.ID, "emailError").text

def test_tc019(driver):
    signup(driver, first="John", last="Doe", email="test@example", password="password123", confirm="password123")
    assert "Please enter a valid email address" in driver.find_element(By.ID, "emailError").text

def test_tc020(driver):
    signup(driver, first="John", last="Doe", email="tc001@example.com", password="password123", confirm="password123")
    assert "This email address is already registered" in driver.find_element(By.ID, "emailError").text

def test_tc021(driver):
    signup(driver, first="John", last="Doe", email="tést123@example.com", password="password123", confirm="password123")
    assert "Email must not contain unicode characters" in driver.find_element(By.ID, "emailError").text

def test_tc022(driver):
    signup(driver, first="John", last="Doe", email="test@example.com", confirm="password123")
    assert "Password is required" in driver.find_element(By.ID, "passwordError").text

def test_tc023(driver):
    signup(driver, first="John", last="Doe", email="test@example.com", password="pass", confirm="pass")
    assert "Password must be at least 6 characters" in driver.find_element(By.ID, "passwordError").text

def test_tc024(driver):
    signup(driver,first="John", last="Doe", email="tc013@example.com", password="   password123   ", confirm="password123")
    assert "Passwords do not match" in driver.find_element(By.ID, "confirmPasswordError").text

def test_tc025(driver):
    signup(driver, first="John", last="Doe", email="test@example.com", password="123456")
    assert "Please confirm your password" in driver.find_element(By.ID, "confirmPasswordError").text

def test_tc026(driver):
    signup(driver, first="John", last="Doe", email="test@example.com", password="123456", confirm="password123")
    assert "Passwords do not match" in driver.find_element(By.ID, "confirmPasswordError").text

def test_tc027(driver):
    signup(driver, first="John", last="Doe", email="test@example.com", password="password123", confirm="password123", accept_terms=False)
    signup_btn = driver.find_element(By.ID, "signupBtn")
    assert not signup_btn.is_enabled()
    driver.execute_script("arguments[0].click();", signup_btn)
    time.sleep(1)
    assert "You must agree to the Terms & Conditions" in driver.find_element(By.ID, "termsError").text

def test_tc028(driver):
    driver.get("https://webtestingteam14.vercel.app/signup.html")
    signup_btn = driver.find_element(By.ID, "signupBtn")
    terms_checkbox = driver.find_element(By.ID, "terms")
    assert not signup_btn.is_enabled()
    terms_checkbox.click()
    time.sleep(2)
    assert signup_btn.is_enabled()

def test_tc029(driver):
    driver.get("https://webtestingteam14.vercel.app/signup.html")
    signup_btn = driver.find_element(By.ID, "signupBtn")
    terms_checkbox = driver.find_element(By.ID, "terms")
    terms_checkbox.click()
    time.sleep(1)
    assert signup_btn.is_enabled()
    terms_checkbox.click()
    time.sleep(1)
    assert not signup_btn.is_enabled()

def test_tc030(driver):
    signup(driver)
    assert "First name is required" in driver.find_element(By.ID, "firstNameError").text
    assert "Last name is required" in driver.find_element(By.ID, "lastNameError").text
    assert "Email is required" in driver.find_element(By.ID, "emailError").text
    assert "Password is required" in driver.find_element(By.ID, "passwordError").text
    assert "Please confirm your password" in driver.find_element(By.ID, "confirmPasswordError").text

def test_tc031(driver):
    driver.get("https://webtestingteam14.vercel.app/signup.html")
    terms_link = driver.find_element(By.LINK_TEXT, "Terms & Conditions")
    terms_link.click()
    WebDriverWait(driver, 5).until(
        EC.url_contains("termsandcondition.html")
    )
    assert "termsandcondition.html" in driver.current_url

def test_tc032(driver):
    driver.get("https://webtestingteam14.vercel.app/signup.html")
    signin_link = driver.find_element(By.LINK_TEXT, "Sign in")
    signin_link.click()
    WebDriverWait(driver, 5).until(
        EC.url_contains("login.html")
    )
    assert "login.html" in driver.current_url

def test_tc033(driver):
    xss_payload = "<script>alert('XSS')</script>"
    signup(driver, first=xss_payload, last="Doe", email="tc33@example.com", password="password123", confirm="password123")

    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        assert False, "XSS alert triggered → Vulnerable"
    except:
        pass
    error_text = driver.find_element(By.ID, "firstNameError").text
    assert error_text != ""

def test_tc034(driver):
    xss_payload = '"><script>alert("XSS")</script>'
    signup(driver, first="John", last="Doe", email=xss_payload, password="password123", confirm="password123")
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        assert False, "XSS alert triggered in Email → Vulnerable"
    except:
        pass
    email_error = driver.find_element(By.ID, "emailError").text
    assert email_error != ""