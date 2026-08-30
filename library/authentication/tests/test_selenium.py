import time

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

CREDENTIALS = {
    "valid": ("test@gmail.com", "1234"),
    "invalid": [
        ("", "1234"),
        ("test", ""),
        ("test@gmail.com", "")
    ],
    "incorrect": [
        ("test@gmail.com", "234"),
        ("test2@gmail.com", "1234")
    ]
}

User = get_user_model()

class LoginTest(StaticLiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create_user(*CREDENTIALS["valid"])
        self.browser = webdriver.Chrome()
        self.browser.get(f"{self.live_server_url}/auth/")

    def tearDown(self):
        self.browser.quit()

    def login(self, email, password):
        self.browser.find_element(By.CLASS_NAME, "btn-auth-login").click()

        form = self.browser.find_element(By.TAG_NAME, "form")
        form.find_element(By.ID, "id_email").send_keys(email)
        form.find_element(By.ID, "id_password").send_keys(password)
        form.find_element(By.CSS_SELECTOR, "button").click()
        time.sleep(1)

        return self.edit_user_button()

    def edit_user_button(self):
        try:
            return self.browser.find_element(
                By.CSS_SELECTOR, 'a[href="/auth/edit/"]'
            )
        except NoSuchElementException:
            return None
        
    def test_valid_login_logout(self):
        print(f"Running {self._testMethodName}", flush=True)

        logged_in = self.login(*CREDENTIALS["valid"])

        self.assertIsNotNone(logged_in)
        self.assertTrue(logged_in.is_displayed())
        self.assertEqual(CREDENTIALS["valid"][0], logged_in.text)

        self.browser.find_element(
            By.CSS_SELECTOR, 'a[href="/auth/logout/"]'
        ).click()

        self.assertIsNone(
            self.edit_user_button(), "Still logged in after logout"
        )

    def test_invalid_login(self):
        print(f"Running {self._testMethodName}", flush=True)

        for credentials in CREDENTIALS["invalid"]:
            logged_in = self.login(*credentials)
            self.assertIsNone(logged_in)

    def test_incorrect_login(self):
        print(f"Running {self._testMethodName}", flush=True)

        for credentials in CREDENTIALS["incorrect"]:
            logged_in = self.login(*credentials)
            self.assertIsNone(logged_in)

            error_msg = self.browser.find_element(By.CLASS_NAME, "text-danger")
            self.assertTrue(error_msg.is_displayed())
            self.assertIn("invalid email or password", error_msg.text.lower())