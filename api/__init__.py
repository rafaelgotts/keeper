
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


api.add_resource(HealthCheckView, "/ping/hc")

if __name__ == "__main__":
    app.run(debug=True)
