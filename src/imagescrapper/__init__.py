from imagescrapper.runner import imagescrapper


def google_scrapper(folder_path: str, search_term: str, number_images: int = 10):
    """function to download the images from google image
    Args:
        folder_path (str): path to save the images
        search_term (str): search term to search in google image
        number_images (int, optional): number of images to download. Defaults to 10.
    """
    scrapper = imagescrapper(folder_path=folder_path)
    scrapper.search(search_term=search_term, number_images=number_images)
