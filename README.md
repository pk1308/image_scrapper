# image_scrapper

step 1

pip install pymongo

pip install pymongo[srv]

pip install image-scrapper-pk1308


step 2

from imagescrapper.runner import imagescrapper

import pymong

step 3

mongourl ="mongodb+srv://`<username>`:`<password>`@`<cluster-name>`.mongodb.net/myFirstDatabase"

client = pymongo.MongoClient(mongourl)


step4

scrapper =imagescrapper(client)

scrapper.search_and_download(search_term="Virat kholi",number_images=10)

**Enjoy**

Data saved to data/Virat kholi


link to pip 


pip install image-scrapper-pk1308
