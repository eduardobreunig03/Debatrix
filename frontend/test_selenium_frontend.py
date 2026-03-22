import unittest
import time
import random
from httpcore import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


class FrontendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        #cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        #FOR SAFARI
        cls.driver = webdriver.Safari() 
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:3000"
        cls.unique_username = f"testuser_{int(time.time())}_{random.randint(1000, 9999)}"

        cls.driver.get(f"{cls.base_url}/signup")
        username_field = WebDriverWait(cls.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Username']")))
        email_field = cls.driver.find_element(By.CSS_SELECTOR, "input[aria-label='Email']")
        password_field = cls.driver.find_element(By.CSS_SELECTOR, "input[aria-label='Password']")
        submit_button = cls.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign up')]")
        
        username_field.send_keys(cls.unique_username)
        email_field.send_keys(f"{cls.unique_username}@example.com")
        password_field.send_keys("@Password123")
        submit_button.click()
        WebDriverWait(cls.driver, 5).until(EC.url_contains("login"))
        print("Initial sign-up complete, redirected to login page.")

    def setUp(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.set_page_load_timeout(30)
        
    def wait_for_element(self, by, value, timeout=5):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
        
    def test_1_login_invalid_credentials(self):
        username_field = self.wait_for_element(By.CSS_SELECTOR, "input[aria-label='Username']")
        password_field = self.wait_for_element(By.CSS_SELECTOR, "input[aria-label='Password']")
        submit_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Sign in')]")
        
        username_field.send_keys("invalid_user")
        password_field.send_keys("wrong_password")
        submit_button.click()

        error_message = self.wait_for_element(By.CLASS_NAME, "text-red-500").text
        self.assertEqual(error_message, "Invalid credentials")
        print("Invalid credentials error displayed as expected.")

    def test_2_login_process(self):
        username_field = self.wait_for_element(By.CSS_SELECTOR, "input[aria-label='Username']")
        password_field = self.wait_for_element(By.CSS_SELECTOR, "input[aria-label='Password']")
        submit_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Sign in')]")
        
        username_field.send_keys(self.unique_username)
        password_field.send_keys("@Password123")
        submit_button.click()

        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(f"{self.base_url}/home")
        )
        self.assertEqual(self.driver.current_url, f"{self.base_url}/home")
        print("Successfully logged in and redirected to home page.")
        
    def test_3_create_debate_button(self):
        self.test_2_login_process()

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Log Out']")))
            print("Login confirmed, user is on the home page.")
            
        except TimeoutException:
            self.fail("Failed to confirm login on the home page.")

        create_debate_link = self.wait_for_element(By.XPATH, "//a[@href='/createDebate']")
        self.assertTrue(create_debate_link.is_displayed(), "Create Debate link should be visible when logged in.")

        create_debate_link.click()
        
        WebDriverWait(self.driver, 10).until(EC.url_contains("createDebate"))
        self.assertEqual(self.driver.current_url, f"{self.base_url}/createDebate")
        print("Successfully navigated to the 'Create Debate' page.")

    def test_4_create_and_access_debate(self):
        self.test_2_login_process()

        create_debate_link = self.wait_for_element(By.XPATH, "//a[@href='/createDebate']")
        create_debate_link.click()
        WebDriverWait(self.driver, 20).until(EC.url_contains("createDebate"))

        title = "Selenium Test Debate Title"
        content = "This is the content of the debate created by Selenium."
        title_field = self.wait_for_element(By.CSS_SELECTOR, "input[placeholder='Enter a title...']")
        content_field = self.wait_for_element(By.CSS_SELECTOR, "textarea[placeholder='Enter the content']")
        title_field.send_keys(title)
        content_field.send_keys(content)
        
        submit_button = self.wait_for_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        WebDriverWait(self.driver, 20).until(EC.url_to_be(f"{self.base_url}/home"))
        print("Successfully created debate and navigated back to home page.")

        debate_link = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//h1[text()='{title}']"))
        )
        debate_link.click()
        
        WebDriverWait(self.driver, 20).until(EC.url_contains("/home"))
        self.assertIn("/home", self.driver.current_url)
        print("Successfully navigated to the debate detail page.")

    def test_5_comment(self):
        # Create and access a debate first
        self.test_4_create_and_access_debate()

        # Wait until the 'Comment' button is clickable
        comment_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'custom_button') and contains(text(), 'Comment')]"))
        )
        comment_button.click()

        reply_textarea = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea[placeholder='Write your reply...']"))
        )
        self.assertTrue(reply_textarea.is_displayed(), "Reply text area should be visible after clicking the Comment button.")

        reply_content = "This is a test comment."
        reply_textarea.send_keys(reply_content)

        submit_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit Reply')]"))
        )
        submit_button.click()
        print("Comment successfully added and verified.")
        
        #time.sleep(10)

    def test_6_navbar_explore_link(self):
        self.test_2_login_process()
        explore_link = self.wait_for_element(By.XPATH, "//span[text()='Explore']")
        explore_link.click()
        print("Successfully navigated to the Explore page from NavBar.")
        
        search_input = self.wait_for_element(By.CSS_SELECTOR, "input[placeholder='Search']")
        search_query = "Selenium Test Debate Title"
        search_input.send_keys(search_query)

        search_input.send_keys("\n")
            
    def test_7_navbar_trending_link(self):
        trending_link = self.wait_for_element(By.XPATH, "//span[text()='Trending']")
        trending_link.click()
        print("Successfully navigated to the Trending page from NavBar.")

    def test_8_navbar_profile_link(self):
        self.test_2_login_process()
        profile_container = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blur_background"))
        )

        profile_link = self.wait_for_element(By.XPATH, "//img[@alt='User Profile']")
        profile_link.click()
        print("Successfully navigated to the Profile page from NavBar.")
                
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()