import io
import os
import platform
import time
from urllib import request

import selenium_stealth  # avoid detection from website that selenium is used
from chromedriver_py import binary_path
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from imagescrapper.logger import logger
from imagescrapper.util import download_windows_chrome

_chrome_driver = ChromeDriverManager().install()
# firstly download all needed chrome drivers which matches current chrome version
_SYSTEM = platform.system().lower()

class imagescrapper(webdriver.Chrome):
    """_summary_
    This class is used to scrape the images from Google image and save it in the mongodb
    """

    def __init__(self, folder_path: str = "scrapped_images", teardown: bool = False):
        """ """

        try:
            self.folder_path = folder_path
            os.makedirs(self.folder_path, exist_ok=True)
            self.teardown = teardown
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("disable-dev-shm-usage")
            if _SYSTEM == "windows":
                download_windows_chrome()
                self.driver = webdriver.Chrome(executable_path=_chrome_driver, options=chrome_options)
            elif  _SYSTEM in ["linux", "darwin"]:
                service = Service(binary_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            logger.error(e)

    def __enter__(self):
        super(imagescrapper, self).__enter__()
        selenium_stealth.stealth(
            self,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        return self

    def fetch_image_urls(
        self, query: str, max_links_to_fetch: int, sleep_between_interactions: int = 2
    ):
        """function opens the google chrome and search the images for the given query
        returns the list of url of the images
        Args:
            query (str): the search query eg : query = 'kitten'
            max_links_to_fetch (int): max number of images to be fetched eg : max_links_to_fetch = 100
            sleep_between_interactions (int, optional): to create a human interaction
            . Defaults to 2.
        """

        def scroll_to_end():
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(sleep_between_interactions)

        # build the google query

        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        # load the page
        self.driver.get(search_url.format(q=query))

        self.image_urls = set()  # set the get the set of url

        # initialize the image ur no
        image_count = 0
        results_start = 0
        while image_count < max_links_to_fetch:
            scroll_to_end()

            # get all image thumbnail results
            thumbnail_results = self.driver.find_elements(
                by=By.CSS_SELECTOR, value="img.Q4LuWd"
            )
            number_results = len(thumbnail_results)

            logger.info(
                f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}"
            )

            for img in thumbnail_results[results_start:number_results]:
                # try to click every thumbnail such that we can get the real image behind it
                try:
                    img.click()
                    time.sleep(sleep_between_interactions)
                except Exception:
                    continue

                # extract image urls

                actual_images = self.driver.find_elements(
                    by=By.CSS_SELECTOR, value="img.n3VNCb"
                )
                for actual_image in actual_images:
                    if actual_image.get_attribute(
                        "src"
                    ) and "http" in actual_image.get_attribute("src"):
                        url_to_add = actual_image.get_attribute("src")

                        self.image_urls.add(url_to_add)
                        results_start += 1
                        logger.info(
                            f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}"
                        )

                image_count = len(self.image_urls)
                logger.info(f"extracted {len(self.image_urls)} image urls")

                if len(self.image_urls) >= max_links_to_fetch:
                    print(f"Found: {len(self.image_urls)} image links, done!")
                    break

            # move the result startpoint further down
            results_start = len(thumbnail_results)

        logger.info(
            f"Found: {number_results} search results. Extracting links from {len(self.image_urls)}:{number_results}"
        )
        self.driver.quit()
        return self.image_urls

    def search(self, search_term: str, number_images: int = 10):
        """start function to search and download the images from google image
        Args:
            search_term (str): eg : search_term = 'kitten'
            number_images (int, optional): number of images eg : number_images = 100
            Defaults to 10.
        """

        fetched_url = self.fetch_image_urls(
            query=search_term, max_links_to_fetch=number_images
        )
        logger.info(
            f"Found: {len(fetched_url)} image links from serach term {search_term}"
        )
        image_counter = self.download_image(
            fetched_url, folder_path=self.folder_path, search_term=search_term
        )
        return image_counter

    def download_image(
        self, fetched_url: list, folder_path: str, search_term: str = ""
    ):
        """function to download the images from the url
        Args:
            fetched_url (list): list of url of the images
            folder_path (str): path to save the images
        """
        image_counter = 0

        for i, url in enumerate(fetched_url):
            try:
                data = request.urlopen(url)
                img_content = data.read()
                img_file = io.BytesIO(img_content)
                image = Image.open(img_file)
                file_pth = os.path.join(folder_path, f"{search_term}{i}.jpg")
                with open(file_pth, "wb") as file:
                    image.save(file, "JPEG")
                    image_counter += 1
                logger.info(f"Downloaded {i} images")
            except Exception as e:
                logger.error(e)
                pass
        logger.info(f"Downloaded {image_counter} images")
        return image_counter

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            super(imagescrapper, self).__exit__()
            self.quit()
