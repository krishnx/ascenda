from model.data import DataModel


class DataRules:
    """
    handles the score of the data
    """

    # set of rules based on which the score is calculated
    RULES = {
        'info': {
            'score': 1,
            'keywords': ['hotels near me', 'motel', 'cheap hotels', 'cheap hotels near me', 'hotel booking',
                         'hotel deals', 'luxury', 'spa', 'deals', 'best', 'scenic', 'beauty', 'beach', 'butler service',
                         'water front', 'waterfront', 'garden', 'resort']
        },
        'amenities': {
            'count': 5,
            'score': 1
        },
        'amenities_images': {
            'count': 2,
            'score': 1
        },
        'room_images': {
            'count': 2,
            'score': 1
        },
    }

    def count_hits(self, data):
        """
        based on the field, calculate the score
        the higher the score, better the chances of getting selected
        :param data:
        :return:
        """
        score = 0
        description_lower = data['description'].lower()
        name_lower = data['name'].lower()
        for keyword in self.RULES['info']['keywords']:
            if keyword in description_lower:
                score += 1

            if keyword in name_lower:
                score += 1

        total_facilities = len(data.get('facilities', ''))
        if total_facilities >= self.RULES['amenities']['count']:
            score += total_facilities * self.RULES['amenities']['score']

        if 'images' in data:
            total_images = len(data['images'].get('rooms', ''))
            if total_images >= self.RULES['room_images']['count']:
                score += total_images * self.RULES['room_images']['score']

            if len(data['images'].get('amenities_images', '')) >= self.RULES['amenities_images']['count']:
                score += data['facilities'] * self.RULES['rooms_images']['score']
        else:
            score -= 1

        return score

    def select_data(self, source_data):
        """
        based on the calculated score, update the data selection
        :param source_data:
        :return:
        """
        for id_, data in source_data.items():
            existing_data = DataModel.get_finalized_data().get(id_)
            score = self.count_hits(data)
            if not existing_data:
                data['score'] = score
                DataModel.set_finalized_data(id_, data)
                continue

            if score < 0 or score < existing_data.get('score', 0):
                continue

            data['score'] = score
            DataModel.set_finalized_data(id_, data)

        return True
