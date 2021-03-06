from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os
import pymongo
import logging as lg
import gridfs

# For selenium driver implementation
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")


class imagescrapper:
    """_summary_
    This class is used to scrape the images from Google image and save it in the mongodb
    """

    def __init__(self, mongodb_client):
        """_summary_
        This function is used to initialize the class with the database name and collection name
        the class initialization the class with the below argument 

        Args:
             mongodb_client (pymongo.MongoClient): mongodb client
           
            
        """

        lg.debug('init function called')
        try:

            self.client = mongodb_client

            lg.info('mongodb connected')
        except Exception as e:
            lg.error('mongodb connection failed')
            lg.error(e)
            raise e

    def __fetch_image_urls(self, query: str, max_links_to_fetch: int, done_url: list,
                           sleep_between_interactions: int = 2):
        """ function opens the google chrome and search the images for the given query 
        returns the list of url of the images 

        Args:
            query (str): the search query eg : query = 'kitten'
            max_links_to_fetch (int): max number of images to be fetched eg : max_links_to_fetch = 100
            sleep_between_interactions (int, optional): to create a human interaction
            . Defaults to 2.
        """

        def scroll_to_end(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_between_interactions)

        # build the google query

        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        wd = webdriver.Chrome(ChromeDriverManager().install())  # create the webdriver
        # load the page
        wd.get(search_url.format(q=query))

        self.image_urls = set()  # set the get the set of url

        # initialize the image ur no
        image_count = 0
        results_start = 0
        while image_count < max_links_to_fetch:
            scroll_to_end(wd)

            # get all image thumbnail results
            thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
            number_results = len(thumbnail_results)

            lg.info(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

            for img in thumbnail_results[results_start:number_results]:
                # try to click every thumbnail such that we can get the real image behind it
                try:
                    img.click()
                    time.sleep(sleep_between_interactions)
                except Exception:
                    continue

                # extract image urls

                actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        url_to_add = actual_image.get_attribute('src')
                        if url_to_add not in done_url:
                            self.image_urls.add(actual_image.get_attribute('src'))
                            results_start += 1
                            lg.info(
                                f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

                image_count = len(self.image_urls)
                lg.info(f"extracted {len(self.image_urls)} image urls")

                if len(self.image_urls) >= max_links_to_fetch:
                    print(f"Found: {len(self.image_urls)} image links, done!")
                    break
            else:
                print("Found:", len(self.image_urls), "image links, looking for more ...")
                time.sleep(30)
                return
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")

            # move the result startpoint further down
            results_start = len(thumbnail_results)

        lg.info(
            f"Found: {number_results} search results. Extracting links from {len(self.image_urls)}:{number_results}")

        return self.image_urls

    def __persist_image(self, db_name: str, url: str, counter: int, search_term: str):
        """function takes the folder path and url of the image and save it in the

        Args:
            db_name (str): database name
            url (str): url of the image
            counter (_type_): counter of the image
            search_term (str): search term
        """
        try:
            image_content = requests.get(url).content

        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")

        try:
            post_file = self.__post_file(db_name=db_name, url=url, data=image_content, counter=counter,
                                         search_term=search_term)
            if post_file:
                lg.info(f"SUCCESS -saved file_counter :{counter} -in - Mongodb db={db_name} ")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")
            return False
        return True

    def __post_file(self, db_name: str, url: str, data: str, counter: int, search_term: str):
        """function to post the file to the mongodb

        Args:
            db (str): database name
            url (str): url of the file
            data (str): data of the file
            counter (int): counter of the file
            search_term (str): search term
        """

        lg.info(f'post_file function called with {url}')
        try:
            db = self.client[db_name]
            fs = gridfs.GridFS(db)
            fs.put(data, filename=search_term + str(counter) + ".jpg", url=url, counter=counter,
                   search_term=search_term)
            lg.info('file posted to mongodb')
        except Exception as e:
            lg.error('file posting to mongodb failed')
            lg.error(e)
            raise e
        return True

    def __get_data(self, db_name: str, search_term: str):
        """function to get the data from the mongodb

        Args:
            db (str): database name
            search_term (str): search term
        """
        lg.info(f'get_data function called with {db_name}')
        try:
            db = self.client[db_name]
            fs = gridfs.GridFS(db)
            datas = db.fs.files.find({"search_term": search_term})
            lg.info('file fetched from mongodb')
            return datas
        except Exception as e:
            lg.error('file fetching from mongodb failed')
            lg.error(e)
            raise e

    def search(self, search_term: str, db_name: str, number_images: int = 10):
        """start function to search and download the images from google image

        Args:
            search_term (str): eg : search_term = 'kitten'
            number_images (int, optional): number of images eg : number_images = 100 
            Defaults to 10.
        """
        done_url = []
        done_data = self.__get_data(db_name=db_name, search_term=search_term)

        if done_data:
            done_url = [data["metadata"]["url"] for data in done_data]
            lg.info(f"{len(done_url)}data found in db {db_name}")
            number_images = number_images - len(done_url)

        res = self.__fetch_image_urls(query=search_term, max_links_to_fetch=number_images, done_url=done_url)
        lg.info(f"Found: {len(res)} image links from serach term {search_term}")

        counter = len(done_url)
        for ele in res:
            image_post = self.__persist_image(db_name=db_name, url=ele, counter=counter, search_term=search_term)
            if image_post:
                counter += 1
            else:
                lg.info(f"ERROR - Could not save {ele}")
        lg.info(f"Total images saved to mongodb db : {db_name} : {counter}")
        return True

    def download(self, search_term: str, db_name: str):
        """start function to search and download the images from google image

        Args:
            search_term (str): eg : search_term = 'kitten'
            number_images (int, optional): number of images eg : number_images = 100 
            Defaults to 10.
        """
        db = self.client[db_name]
        fs = gridfs.GridFS(db)
        datas = self.__get_data(db_name=db_name, search_term=search_term)
        dir_path = f'data/{search_term}'
        os.makedirs(dir_path, exist_ok=True)
        for data in datas:
            print(data["filename"])
            id = data['_id']
            output = fs.get(id).read()
            with open(f'{dir_path}/{data["filename"]}.jpg', 'wb') as f:
                f.write(output)

        return "Data saved to {}".format(dir_path)


if __name__ == '__main__':
    pass
