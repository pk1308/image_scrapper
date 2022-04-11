# image_scrapper


step 1 

pip install gridfs-fuse

step 2

from src.imagescrapper import imagescrapper

step 3

mongourl ="mongodb+srv://`<username>`:`<password>`@`<cluster-name>`.mongodb.net/myFirstDatabase"

scrapper = imagescrapper.imagescrapper(mongourl)

step4

scrapper.search_and_download(search_term="Virat kholi",number_images=10)
