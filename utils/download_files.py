import glob

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from utils.base_logger import logger

url = 'https://cricsheet.org/downloads/odis_json.zip'


def download_and_extract_json_files(path):
    """
    This function downloads zip file containing data for all ODI matches and unzips them in the provided path
    :param path: the path for storing all the json files
    :type path: str
    """
    logger.info("Downloading started from {url}".format(url=url))
    try:
        resp = urlopen(url)
        myzip = ZipFile(BytesIO(resp.read()))
        myzip.extractall(path)
    except Exception as e:
        logger.exception(e)
        raise
    else:
        counter = len(glob.glob1(path, "*.json"))
        logger.info("Downloaded {counter} files".format(counter=counter))


if __name__ == "__main__":
    path_to_files = '../data/'
    download_and_extract_json_files(path_to_files)
