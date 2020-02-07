import os
from io import BytesIO
from time import sleep

from django.core.files.storage import default_storage
from django.test import LiveServerTestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.test import override_settings
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from myproject.apps.likes.models import Like
from ..models import Location


SHOW_BROWSER = getattr(settings, "TESTS_SHOW_BROWSER", False)


@override_settings(DEBUG=True)
class LiveLocationTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(LiveLocationTest, cls).setUpClass()
        driver_path = os.path.join(settings.BASE_DIR, "drivers", "chromedriver")
        chrome_options = Options()
        if not SHOW_BROWSER:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1200,800")

        cls.browser = webdriver.Chrome(
            executable_path=driver_path, options=chrome_options
        )
        cls.browser.delete_all_cookies()

        image_path = cls.save_test_image("test.jpg")
        cls.location = Location.objects.create(
            name="Park Güell",
            description="If you want to see something spectacular, come to Barcelona, Catalonia, Spain and visit Park Güell. Located on a hill, Park Güell is a public park with beautiful gardens and organic architectural elements.",
            picture=image_path,  # dummy path
        )
        cls.username = "admin"
        cls.password = "admin"
        cls.superuser = User.objects.create_superuser(
            username=cls.username, password=cls.password, email="admin@example.com"
        )

    @classmethod
    def tearDownClass(cls):
        super(LiveLocationTest, cls).tearDownClass()
        cls.browser.quit()
        cls.location.delete()
        cls.superuser.delete()

    @classmethod
    def save_test_image(cls, filename):
        from PIL import Image

        image = Image.new("RGB", (1, 1), 0)
        image_buffer = BytesIO()
        image.save(image_buffer, format="JPEG")
        path = f"tests/{filename}"
        default_storage.save(path, image_buffer)
        return path

    def wait_a_little(self):
        if SHOW_BROWSER:
            sleep(2)

    def test_login_and_like(self):
        # login
        login_path = reverse("admin:login")
        self.browser.get(
            f"{self.live_server_url}{login_path}?next={self.location.get_url_path()}"
        )
        username_field = self.browser.find_element_by_id("id_username")
        username_field.send_keys(self.username)
        password_field = self.browser.find_element_by_id("id_password")
        password_field.send_keys(self.password)
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
        WebDriverWait(self.browser, timeout=10).until(
            lambda x: self.browser.find_element_by_css_selector(".like-button")
        )
        # click on the "like" button
        like_button = self.browser.find_element_by_css_selector(".like-button")
        is_initially_active = "active" in like_button.get_attribute("class")
        initial_likes = int(
            self.browser.find_element_by_css_selector(".like-badge").text
        )

        self.assertFalse(is_initially_active)
        self.assertEqual(initial_likes, 0)

        self.wait_a_little()

        like_button.click()
        WebDriverWait(self.browser, timeout=10).until(
            lambda x: int(self.browser.find_element_by_css_selector(".like-badge").text)
            != initial_likes
        )
        likes_in_html = int(
            self.browser.find_element_by_css_selector(".like-badge").text
        )
        likes_in_db = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Location),
            object_id=self.location.pk,
        ).count()
        self.assertEqual(likes_in_html, 1)
        self.assertEqual(likes_in_html, likes_in_db)

        self.wait_a_little()

        self.assertGreater(likes_in_html, initial_likes)

        # click on the "like" button again to switch back to the previous state
        like_button.click()
        WebDriverWait(self.browser, timeout=10).until(
            lambda x: int(self.browser.find_element_by_css_selector(".like-badge").text)
            == initial_likes
        )

        self.wait_a_little()
