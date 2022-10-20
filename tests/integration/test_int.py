
import os
from pathlib import Path

import pytest
from ensure import EnsureError

from imagescrapper import google_scrapper
from imagescrapper.logger import logger

data_path = Path("tests/data")

class Test_scrapper:
    base_scrapper_input = [ ({"folder_path": "virat", "search_term": "virat", "number_images":2} , True), 
                   ({"folder_path": "sachin", "search_term": "sachin", "number_images":2} , True),] 
                   
    bad_scrapper_input = [ ({"folder_path": 1, "search_term": "dog", "number_images":2} ),
                     ({"folder_path": "cat", "search_term": 1, "number_images":"2"} )]
    

    @pytest.mark.parametrize("input, expected",  base_scrapper_input )
    def test_scrapper(self, input, expected):
        input["folder_path"] = os.path.join(data_path, input["folder_path"])
        logger.info(input["folder_path"])
        assert google_scrapper(**input) == expected
        assert os.path.exists(input["folder_path"]) == True
        assert len(os.listdir(input["folder_path"])) >= 1   
    @pytest.mark.parametrize("input",  bad_scrapper_input )
    def test_scrapper_bad_input(self, input):
        with pytest.raises(EnsureError):
            assert google_scrapper(**input)