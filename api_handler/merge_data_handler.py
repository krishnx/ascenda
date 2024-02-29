import logging
from model.data import DataModel
from transformers.data_downloader import DataDownloader
from transformers.data_parser import DataParser
from transformers.data_rules import DataRules


class MergeDataHandler:
    """
    handles data merges from the source
    """

    def __init__(self, source_url):
        self.data_downloader = DataDownloader(source_url)
        self.data_parser = DataParser()
        self.data_rules = DataRules()

    def merge_data(self):
        """
        1. download the json from the source
        2. parse the data
        3. save the data
        :return:
        """
        try:
            raw_data = self.data_downloader.download_data()
            DataModel.set_data(raw_data)

            DataModel.set_parsed_data(self.data_parser.parse(raw_data))
            parsed_data = DataModel.get_parsed_data()

            self.data_rules.select_data(parsed_data)

            status = True
        except:
            logging.exception('exception occurred while merging the data')
            status = False

        return status
