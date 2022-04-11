# image_scrapper

step 1 

from src.imagescrapper import imagescrapper


step 2

mongourl ="mongodb+srv://`<username>`:`<password>`@`<cluster-name>`.mongodb.net/myFirstDatabase"

scrapper = imagescrapper.imagescrapper(mongourl)

step3

scrapper.search_and_download(search_term="Virat kholi",number_images=10)
