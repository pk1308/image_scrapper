from curses import meta
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time 
import requests
import os 
import pymongo
import logging as lg 
import gridfs


#For selenium driver implementation on heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")



class mongodb:
    '''class for mongo db operations'''
    
    def __init__(self,mongodb_client):
        """Initialize the class with the database name and collection name
        the class initialization the class with the below argument 

        Args:
            mongodb_client (pymongo.MongoClient): mongodb client
            db : database name
            
        """
        
        lg.debug('init function called')
        try :
            
            self.client = pymongo.MongoClient(mongodb_client)
            
            
            lg.info('mongodb connected')
        except Exception as e:
            lg.error('mongodb connection failed')
            lg.error(e)
            raise e
        
        
    def post_file(self,db,url ,data , counter):
        """function to post the file to the mongodb

        Args:
            db (str): database name
            url (str): url of the file
            data (str): data of the file
        """
      
        lg.info(f'post_file function called with {url}')
        try :
            db = self.client[db]
            fs = gridfs.GridFS(db)
            fs.put(data, filename=dc+str(counter) , metadata={"url":url})
            lg.info('file posted to mongodb')
        except Exception as e:
            lg.error('file posting to mongodb failed')
            lg.error(e)
            raise e
    
    def get_file(self,db):
        """function to get the file from the mongodb

        Args:
            db (str): database name
            url (str): url of the file
        """
        lg.info(f'get_file function called with {db}')
        try :
            db = self.client[db]
            fs = gridfs.GridFS(db)
            data = db.fs.files.find()
            lg.info('file fetched from mongodb')
            return data
        except Exception as e:
            lg.error('file fetching from mongodb failed')
            lg.error(e)
            raise e

class imagescrapper(mongodb):
    """_summary_
    This class is used to scrape the images from Google image and save it in the mongodb
    """
    def __init__(self,mongodb_client):
        """_summary_
        This function is used to initialize the class with the database name and collection name
        the class initialization the class with the below argument 

        Args:
             mongodb_client (pymongo.MongoClient): mongodb client
            db : database name
            
        """
        
        
        super().__init__(mongodb_client)
        
    
    def __fetch_image_urls(self,query: str, max_links_to_fetch: int,sleep_between_interactions: int = 2):
        
        
        def scroll_to_end(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_between_interactions)

            # build the google query

        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        # load the page
        wd=webdriver.Chrome(ChromeDriverManager().install()) 
        wd.get(search_url.format(q=query))

        self.image_urls = set()
        image_count = 0
        results_start = 0
        while image_count < max_links_to_fetch:
            scroll_to_end(wd)

            # get all image thumbnail results
            thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")     
            number_results = len(thumbnail_results)

            print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

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
                        self.image_urls.add(actual_image.get_attribute('src'))

                image_count = len(self.image_urls)

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

        return self.image_urls
    
    def __persist_image(self ,folder_path:str,url:str, counter):
        try:
            image_content = requests.get(url).content

        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")

        try:
            self.post_file( db=folder_path,url=url, data=image_content , counter=counter)
            
            print(f"SUCCESS - saved filename :{url} - as {self.client} ")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")


    def search_and_download(self,search_term: str , number_images=10):
        target_folder = ''.join(search_term.lower().split(' '))


        
        res =  self.__fetch_image_urls(search_term, number_images, )
        print(len(res))

        counter = 0
        for elem in res:
            self.__persist_image(target_folder, elem, counter)
            counter += 1
            
if __name__ == '__main__':
    pass 
        
        