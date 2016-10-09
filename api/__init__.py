
from flask import Flask, request
from flask_restful import Resource, Api
import redis

app = Flask(__name__)
api = Api(app)


class HealthCheckView(Resource):
    """ Used for hc on the api or another 
    service, i.e. databse access
    """
    def get(self):
        return {'status': 'OK'}


class KeyControlView(Resource):
    """ Class to manage the keys
    """
    def __init__(self):
        self.data_key = redis.Redis(host='localhost', port=6379, db=0)


    def get(self, key_id=None):
        """ Return one or all keys
        """
        if not self.data_key:
            return {'error': 'redis_error'}

        if key_id and self.data_key.get(key_id):
            return {key_id: self.data_key.get(key_id).decode()}

        return {'warning': 'key_id not found'}

    def post(self):
        """ Save the key
        """
        payload = request.json

        for key_id, key in payload.items():
            self.data_key.set(key_id, key)

        return {'success': True, 'message': 'key_saved'}


api.add_resource(HealthCheckView, "/ping/hc")
api.add_resource(
    KeyControlView,
    "/key/<string:key_id>",
    "/key"
)

if __name__ == "__main__":
    app.run(debug=True)
