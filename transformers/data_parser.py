import copy
import logging

from common.exceptions import InvalidDataException
from model.data import DataModel


class DataParser:
    """
    handles the logic for data parsing
    """
    # template
    DATA = {
        "id": "",
        "destination_id": 0,
        "name": "",
        "location": {
            "lat": 0.0,
            "lng": 0.0,
            "address": "",
            "city": "",
            "country": ""
        },
        "description": "",
        "amenities": {
            "general": [],
            "room": []
        },
        "images": {
            "rooms": [],
            "site": [],
            "amenities": []
        },
        "booking_conditions": []
    }

    ALLOWED_HOTEL_ID = ['id', 'Id', 'hotel_id', 'HotelId']
    ALLOWED_DESTINATION_ID = ['destination', 'DestinationId', 'destination_id']
    ALLOWED_HOTEL_NAME = ['name', 'Name', 'hotel_name', 'HotelName']
    ALLOWED_DESCRIPTION = ['description', 'Description', 'info', 'details', 'caption']
    ALLOWED_LOCATION = ['location', 'Location']
    ALLOWED_ADDRESS = ['address', 'Address']
    ALLOWED_CITY = ['city', 'City']
    ALLOWED_COUNTRY = ['country', 'Country']
    ALLOWED_LAT = ['latitude', 'Latitude', 'lat']
    ALLOWED_LNG = ['longitude', 'Longitude', 'lng']
    ALLOWED_AMENITIES = ['facilities', 'Facilities', 'Amenities', 'amenities']
    ALLOWED_IMAGES = ['images', 'Images', 'Pics', 'pics']
    ALLOWED_ROOMS = ['Rooms', 'rooms', 'suite']
    ALLOWED_SITE = ['site']
    ALLOWED_AMENITIES_GENERAL = ['general', 'General']
    ALLOWED_AMENITIES_ROOMS = ['room', 'rooms', 'Room', 'Rooms']
    ALLOWED_IMAGES_AMENITIES = ['Amenities', 'amenities']
    ALLOWED_IMAGES_SITE = ['site', 'Site']
    ALLOWED_LINK = ['link', 'Link', 'url', 'URL']
    ALLOWED_BOOKING_CONDITIONS = ['booking_conditions', 'Booking conditions']

    # map of mandatory field in the source data. If any of the field is missing, we reject the data
    # this can be moved to database for on-the-fly changes
    MANDATORY_FIELDS = {
        'id': {
            'allowed': ALLOWED_HOTEL_ID,
            'datatype': str,
        },
        'destination_id': {
            'allowed': ALLOWED_DESTINATION_ID,
            'datatype': (int, str),
        },
        'name': {
            'allowed': ALLOWED_HOTEL_NAME,
            'datatype': str,
        },
        'description': {
            'allowed': ALLOWED_DESCRIPTION,
            'datatype': str,
        },
        'location': {
            'allowed': ALLOWED_LOCATION,
            'datatype': (str, dict),
        },
    }

    # optional fields
    # this can be moved to database for on-the-fly changes
    OPTIONAL_FIELDS = {
        'city': {
            'allowed': ALLOWED_CITY,
            'datatype': str,
        },
        'latitude': {
            'allowed': ALLOWED_LAT,
            'datatype': (int, float),
        },
        'longitude': {
            'allowed': ALLOWED_LNG,
            'datatype': (int, float),
        },
        'amenities': {
            'allowed': ALLOWED_AMENITIES,
            'datatype': (str, list),
        },
        'images': {
            'allowed': ALLOWED_IMAGES,
            'datatype': (str, dict)
        },
        'rooms': {
            'allowed': ALLOWED_ROOMS,
            'datatype': (str, list)
        },
        'booking_conditions': {
            'allowed': ALLOWED_BOOKING_CONDITIONS,
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

    def _update_identifiers(self, temp_info, field_name, sanitized_data):
        temp_info.update({field_name: sanitized_data})

    def _update_location_info(self, temp_info, field_name, sanitized_data):
        if not isinstance(sanitized_data, dict):
            sanitized_data = {field_name: sanitized_data}

        for field, value in sanitized_data.items():
            if field in self.ALLOWED_ADDRESS:
                temp_info['location']['address'] = sanitized_data[field]

            elif field in self.ALLOWED_LOCATION:
                temp_info['location']['location'] = sanitized_data[field]

            elif field in self.ALLOWED_LAT:
                temp_info['location']['lat'] = sanitized_data[field]

            elif field in self.ALLOWED_LNG:
                temp_info['location']['lng'] = sanitized_data[field]

            elif field in self.ALLOWED_COUNTRY:
                temp_info['location']['country'] = sanitized_data[field]

            elif field in self.ALLOWED_CITY:
                temp_info['location']['city'] = sanitized_data[field]

    def _update_amenities(self, temp_info, field_name, sanitized_data):
        if not isinstance(sanitized_data, dict):
            sanitized_data = {'general': sanitized_data}

        for field, value in sanitized_data.items():
            if field in self.ALLOWED_AMENITIES_GENERAL:
                temp_info[field_name]['general'] += sanitized_data[field]
            elif field in self.ALLOWED_AMENITIES_ROOMS:
                temp_info[field_name]['room'] += sanitized_data[field]

    def _update_images(self, temp_info, field_name, sanitized_data):
        template = {'link': '', 'description': ''}
        for field, value in sanitized_data.items():
            if field in self.ALLOWED_IMAGES_SITE:
                if 'site' not in temp_info[field_name]:
                    temp_info[field_name]['site'] = {}

                for detail in sanitized_data[field]:
                    temp = copy.deepcopy(template)
                    for k, v in detail.items():
                        if k in self.ALLOWED_LINK:
                            temp['link'] = v
                        elif k in self.ALLOWED_DESCRIPTION:
                            temp['description'] = v

                    if temp != template and temp not in temp_info[field_name]['site']:
                        temp_info[field_name]['site'].append(temp)

            elif field in self.ALLOWED_IMAGES_AMENITIES:
                if 'amenities' not in temp_info[field_name]:
                    temp_info[field_name]['amenities'] = {}

                for detail in sanitized_data[field]:
                    temp = copy.deepcopy(template)
                    for k, v in detail.items():
                        if k in self.ALLOWED_LINK:
                            temp['link'] = v
                        elif k in self.ALLOWED_DESCRIPTION:
                            temp['description'] = v

                    if temp != template and temp not in temp_info[field_name]['amenities']:
                        temp_info[field_name]['amenities'].append(temp)

            elif field in self.ALLOWED_ROOMS:
                if 'rooms' not in temp_info[field_name]:
                    temp_info[field_name]['rooms'] = []

                for detail in sanitized_data[field]:
                    temp = copy.deepcopy(template)
                    for k, v in detail.items():
                        if k in self.ALLOWED_LINK:
                            temp['link'] = v
                        elif k in self.ALLOWED_DESCRIPTION:
                            temp['description'] = v

                    if temp != template and temp not in temp_info[field_name]['rooms']:
                        temp_info[field_name]['rooms'].append(temp)

    def _update_booking_conditions(self, temp_info, field_name, sanitized_data):
        for condition in sanitized_data:
            if condition in temp_info[field_name]:
                continue

            temp_info[field_name].append(condition)

    def update_data(self, temp_info, field_name, sanitized_data):
        if not sanitized_data:
            return None

        if field_name in self.ALLOWED_HOTEL_ID + self.ALLOWED_DESTINATION_ID + \
                self.ALLOWED_HOTEL_NAME + self.ALLOWED_DESCRIPTION:
            self._update_identifiers(temp_info, field_name, sanitized_data)

        elif field_name in self.ALLOWED_LOCATION + self.ALLOWED_ADDRESS + \
                self.ALLOWED_LAT + self.ALLOWED_LNG + \
                self.ALLOWED_CITY + self.ALLOWED_COUNTRY:
            self._update_location_info(temp_info, field_name, sanitized_data)

        elif field_name in self.ALLOWED_AMENITIES:
            self._update_amenities(temp_info, field_name, sanitized_data)

        elif field_name in self.ALLOWED_IMAGES:
            self._update_images(temp_info, field_name, sanitized_data)

        elif field_name in self.ALLOWED_BOOKING_CONDITIONS:
            self._update_booking_conditions(temp_info, field_name, sanitized_data)

    def transform_data(self, data):
        """
        transform keys to the common format
        :return:
        """
        transformed_data = []
        for info in data:

            existing_id = list(filter(None, [info.get(id_field) for id_field in self.ALLOWED_HOTEL_ID]))
            if existing_id and DataModel.get_existing_data(existing_id[0]):
                temp_info = DataModel.get_existing_data(existing_id[0])
            else:
                temp_info = copy.deepcopy(self.DATA)

            for field, field_info in info.items():
                transformed_field_name = self.get_transformed_field_name(field)

                if not transformed_field_name:
                    transformed_field_name = field

                self.update_data(temp_info, transformed_field_name, self.sanitize_data(field_info))

            transformed_data.append(temp_info)

        return transformed_data

    def parse(self, data=None):
        """
        validate and parse the data for internal consumption
        :param data:
        :return:
        """
        self.data = self.transform_data(self.data or data)

        validated_data = []
        for data in self.data:
            if self.validate_data(data):
                validated_data.append(data)

        self.data = validated_data

        return self.data
