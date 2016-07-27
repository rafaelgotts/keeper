
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class BaseApiView(Resource):
    """ All the implies on all views 
    will be implemented here
    """
    def post(self):

        content_type = request.headers.get('Content-type', '')
        if not content_type.lower() == 'application/json':
            return {'error': 'Content_type must be json'}, 412


class HealthCheckView(BaseApiView):
    """ Used for hc on the api or another 
    service, i.e. databse access
    """
    def get(self):
        return {'status': 'OK'}


# Simulates an database
DATA_KEY = {}

class KeyControlView(BaseApiView):
    """ Class to manage the keys
    """
    def __init__(self):
        self.data_key = DATA_KEY

    def get(self, key_id=None):
        """ Return one or all keys
        """
        if not self.data_key:
            return {'error': 'none_key_saved'}

        if key_id and self.data_key.get(key_id):
            return {key_id: self.data_key[key_id]}

        return self.data_key

    def post(self):
        """ Save the key
        """
        payload = request.json

        for key_id, key in payload.items():
            self.data_key[key_id] = key

        return {'success': True, 'message': 'key_saved'}


api.add_resource(HealthCheckView, "/ping/hc")
api.add_resource(
    KeyControlView,
    "/key/<string:key_id>",
    "/key"
)

if __name__ == "__main__":
    app.run(debug=True)
