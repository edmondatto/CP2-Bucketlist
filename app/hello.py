from flask_restplus import Resource

from app import api

hello = api.namespace('hello', description='Hello world')


@hello.route('/')
class HelloWorld(Resource):
    def get(self):
        return {'Hello': "world"}
