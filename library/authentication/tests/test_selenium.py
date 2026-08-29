from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

CREDENTIALS = {
    "valid": ("test@gmail.com", "1234")
}

User = get_user_model()

class LoginTest(StaticLiveServerTestCase):

    def setUp(self):
        User.objects.create_user(*CREDENTIALS["valid"])
        self.browser = webdriver.Chrome()
        self.browser.get(f"{self.live_server_url}/auth/")

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        login, password = CREDENTIALS["valid"]
        browser = self.browser

        browser.find_element(By.CLASS_NAME, "btn-auth-login").click()

        form = browser.find_element(By.TAG_NAME, "form")
        form.find_element(By.ID, "id_email").send_keys(login)
        form.find_element(By.ID, "id_password").send_keys(password)
        form.find_element(By.CSS_SELECTOR, "button").click()

        logged_in = browser.find_element(
            By.CSS_SELECTOR, 'a[href="/auth/edit/"]'
        )

        self.assertTrue(logged_in.is_displayed())
        self.assertEqual(login, logged_in.text)