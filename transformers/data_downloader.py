import json
import logging
import urllib.request
from urllib.parse import urlparse


class DataDownloader:
    """
    handles the functionality for downloading the source data from the source url
    """

    def __init__(self, source_url):
        self.source_url = source_url

    def validate_url(self):
        """
        validate the source url
        :return:
        """
        try:
            result = urlparse(self.source_url)
        except Exception as e:
            logging.exception(f'invalid url: {self.source_url}, exception: {str(e)}')
            return False

        return all([result.scheme, result.netloc])

    def download_data(self):
        """
        download the source data from the source url
        :return:
        """
        if not self.validate_url():
            return None

        with urllib.request.urlopen(self.source_url) as url:
            return json.load(url)
