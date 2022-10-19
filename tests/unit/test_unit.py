

import pytest

from imagescrapper.runner import imagescrapper


class Test_scrapper_unit_test:
    scrapper_url = [ ({"folder_path": "dog", "search_term": "dog", "number_images":2} , 2), 
                   ({"folder_path": "cat", "search_term": "cat", "number_images":2} , 2)] 

    def test_selenium(self):
        scrapper = imagescrapper()
        scrapper.driver.get("https://www.google.com")
        assert scrapper.driver.title == "Google"
    
    

    @pytest.mark.parametrize("input, expected",  scrapper_url )
    def test_fectch_url(self, input, expected):
        scrapper = imagescrapper()
        urls = scrapper.fetch_image_urls(query=input["search_term"], max_links_to_fetch=input["number_images"])
        assert len(urls) >= expected
