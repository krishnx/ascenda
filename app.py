import logging
from flask import Flask, request, jsonify, abort

from api_handler.merge_data_handler import MergeDataHandler
from model.data import DataModel

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/merge/', methods=['POST'])
def merge_data():
    request_data = request.json
    if 'source_url' not in request_data:
        return abort(403, 'source_url missing in the request')

    status = MergeDataHandler(request_data['source_url']).merge_data()

    return jsonify({'status': status})


@app.route('/get-hotel-by-id/', methods=['POST'])
def get_hotel_by_id():
    request_data = request.json
    hotel_id = request_data.get('hotel_id')
    hotel_info = DataModel.get_selected_data(hotel_id)

    return jsonify({'data': hotel_info, 'status': 'ok'})


if __name__ == "__main__":
    app.run(debug=True)
