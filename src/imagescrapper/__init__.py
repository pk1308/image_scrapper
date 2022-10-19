from ensure import ensure_annotations

from imagescrapper.logger import logger
from imagescrapper.runner import imagescrapper


@ensure_annotations
def google_scrapper(folder_path: str, search_term: str, number_images: int = 10):
    """function to download the images from google image
    Args:
        folder_path (str): path to save the images
        search_term (str): search term to search in google image
        number_images (int, optional): number of images to download. Defaults to 10.
    """
    logger.info(f"searching for {search_term} images in google and downloading {number_images} images to {folder_path}")
    scrapper = imagescrapper(folder_path=folder_path)
    image_counter= scrapper.search(search_term=search_term, number_images=number_images)
    logger.info(f"Downloaded {image_counter} images from search term {search_term} to {folder_path}")
    return True
