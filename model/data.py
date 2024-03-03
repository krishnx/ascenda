class DataModel:
    """
    DataModel plays the role of database.
    DataModel class saves data in-memory for the demo purpose
    """

    DATA = {}
    PARSED_DATA = {}
    SELECTED_DATA = {}

    @classmethod
    def get_raw_data(cls):
        """
        return the raw data downloaded from the source using source url
        :return:
        """
        return cls.DATA

    @classmethod
    def set_data(cls, data):
        """
        save the raw data downloaded from the source using source url
        :param data:
        :return:
        """
        cls.DATA = data

    @classmethod
    def get_parsed_data(cls):
        """
        fetch the parsed data
        :return:
        """
        return cls.PARSED_DATA

    @classmethod
    def set_parsed_data(cls, data):
        """
        save the parsed data generated from raw source data
        :param data:
        :return:
        """
        cls.PARSED_DATA = {info['id']: info for info in data}

    @classmethod
    def get_finalized_data(cls, id_=None):
        """
        return the finalized data for selection.
        this data is in internal format
        :param id_: id of the hotel
        :return:
        """
        if id_:
            return cls.SELECTED_DATA.get(id_)

        return cls.SELECTED_DATA

    @classmethod
    def set_finalized_data(cls, id_, data):
        """
        save the finalized data for selection
        :param id_: hotel id
        :param data: finalized data
        :return:
        """
        cls.SELECTED_DATA[id_] = data

    @classmethod
    def get_selected_data(cls, hotel_id=None):
        """
        fetch the selected data based on hotel_id
        1. if hotel_id exists, the relevant data will be returned
        2. invalid hotel_id returns null
        3. if hotel_id is None, then return the data for all
        :param hotel_id:
        :return:
        """
        if hotel_id:
            data = cls.SELECTED_DATA.get(hotel_id)
            if data:
                data.pop('score', None)
            return data

        selected_data = []
        for id_, data in cls.SELECTED_DATA.items():
            data.pop('score', None)
            selected_data.append(data)

        return selected_data

    @classmethod
    def get_existing_data(cls, id_):
        return cls.PARSED_DATA.get(id_, {})
