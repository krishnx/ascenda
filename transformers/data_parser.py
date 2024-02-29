import logging

from common.exceptions import InvalidDataException


class DataParser:
    """
    handles the logic for data parsing
    """

    # map of mandatory field in the source data. If any of the field is missing, we reject the data
    # this can be move to database for on-the-fly changes
    MANDATORY_FIELDS = {
        'id': {
            'allowed': ['id', 'Id', 'hotel_id', 'HotelId'],
            'datatype': str,
        },
        'destination': {
            'allowed': ['destination', 'DestinationId', 'destination_id'],
            'datatype': (int, str),
        },
        'name': {
            'allowed': ['name', 'Name', 'hotel_name', 'HotelName'],
            'datatype': str,
        },
        'description': {
            'allowed': ['description', 'Description', 'info', 'details'],
            'datatype': str,
        },
        'address': {
            'allowed': ['address', 'Address', 'location', 'Location'],
            'datatype': (str, dict),
        },
    }

    # optional fields
    # this can be move to database for on-the-fly changes
    OPTIONAL_FIELDS = {
        'city': {
            'allowed': ['city', 'City'],
            'datatype': str,
        },
        'latitude': {
            'allowed': ['latitude', 'Latitude', 'lat'],
            'datatype': (int, float),
        },
        'longitude': {
            'allowed': ['longitude', 'Longitude', 'lng'],
            'datatype': (int, float),
        },
        'facilities': {
            'allowed': ['facilities', 'Facilities', 'Amenities', 'amenities'],
            'datatype': (str, list),
        },
        'images': {
            'allowed': ['images', 'Images', 'Pics', 'pics'],
            'datatype': (str, dict)
        },
        'rooms': {
            'allowed': ['Rooms', 'rooms'],
            'datatype': (str, list)
        },
    }

    def __init__(self, data=None):
        self.data = data

    def sanitize_data(self, data):
        """
        strip the string, remove nulls from the list
        more cleansing can be done based on the requirement
        :param data:
        :return:
        """

        if isinstance(data, str):
            return data.strip()

        if isinstance(data, list):
            return list(filter(None, data))

        # add more sanity steps as per data type
        return data

    def _valid_field(self, field, data, field_obj):
        """
        validate the field against the datatype
        :param field:
        :param data:
        :param field_obj:
        :return:
        """
        if field in data and isinstance(data[field], field_obj['datatype']):
            return True

        return False

    def _validate_mandatory_fields(self, data):
        """
        validate the mandatory field
        raises exception for missing or invalid data
        :param data:
        :return:
        """
        for field, field_obj in self.MANDATORY_FIELDS.items():
            if self._valid_field(field, data, field_obj):
                continue

            raise InvalidDataException(f'Mandatory field "{field}" is not present or must be a {field_obj["datatype"]}')

        return True

    def _validate_optional_fields(self, data):
        """
        validate the optional field
        no exception is raised, but logged for future reference
        :param data:
        :return:
        """
        for field, field_obj in self.OPTIONAL_FIELDS.items():
            if self._valid_field(field, data, field_obj):
                continue

            logging.warning(f'Optional field {field} is not present or must be a {field_obj}')

        return True

    def validate_data(self, data):
        """
        validate the data.
        If mandatory data check fails, reject the data from the list
        :param data:
        :return:
        """
        if not isinstance(data, dict):
            raise ValueError('data needs to be in dictionary format')

        try:
            self._validate_mandatory_fields(data)
        except InvalidDataException:
            return False

        self._validate_optional_fields(data)

        return True

    def get_transformed_field_name(self, data_field):
        """
        return the name used for internal processing
        :param data_field:
        :return:
        """
        transformed_field_name = None
        for field, field_info in self.MANDATORY_FIELDS.items():
            if data_field in field_info['allowed']:
                transformed_field_name = field

        if transformed_field_name:
            return transformed_field_name

        for field, field_info in self.OPTIONAL_FIELDS.items():
            if data_field in field_info['allowed']:
                transformed_field_name = field

        return transformed_field_name

    def parse_data(self, data):
        """
        transform keys to the common format
        :return:
        """
        transformed_data = []
        for info in data:
            temp_info = {}

            for field, field_info in info.items():
                transformed_field_name = self.get_transformed_field_name(field)

                if not transformed_field_name:
                    transformed_field_name = field

                temp_info[transformed_field_name] = self.sanitize_data(field_info)

            transformed_data.append(temp_info)

        return transformed_data

    def parse(self, data=None):
        """
        validate and parse the data for internal consumption
        :param data:
        :return:
        """
        self.data = self.parse_data(self.data or data)

        validated_data = []
        for data in self.data:
            if self.validate_data(data):
                validated_data.append(data)

        self.data = validated_data

        return self.data
