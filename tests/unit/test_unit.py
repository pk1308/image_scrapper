

import pytest

from imagescrapper.runner import imagescrapper


class Test_scrapper_unit_test:
    
    def test_selenium(self):
        scrapper = imagescrapper()
        scrapper.driver.get("https://www.google.com")
        assert scrapper.driver.title == "Google"
    
    