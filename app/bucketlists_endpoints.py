from flask import request
from flask_restplus import Resource, fields

from app.models import Bucketlist
from .restplus import api

bucketlists = api.namespace('bucketlists', description='Bucketlists endpoints')

bucket_list = api.model('bucket_list', {
    'id': fields.Integer(required=True, readOnly=True),
    'name': fields.String(required=True),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
})

bucket_input = api.model('bucket_input', {
    'name': fields.String(required=True),
})


@bucketlists.route('/')
class Bucketlists(Resource):
    @api.marshal_with(bucket_list)
    @api.expect(bucket_input)
    def post(self):
        name = request.json['name']
        bucketlist = Bucketlist(name=name)
        bucketlist.save()
        return bucketlist, 201

    @api.marshal_with(bucket_list)
    def get(self):
        fetched_bucketlists = Bucketlist.get_all(self)
        return fetched_bucketlists, 200


@bucketlists.route('/<int:id>')
class BucketlistsWithId(Resource):
    @api.marshal_with(bucket_list)
    def get(self, id):
        queried_bucketlist = Bucketlist.query.filter_by(id=id).first()
        return queried_bucketlist, 200

    @api.marshal_with(bucket_list)
    @api.expect(bucket_input)
    def put(self, id):
        new_name = request.json['name']
        bucketlist_to_update = Bucketlist.query.filter_by(id=id).first()
        bucketlist_to_update.name = new_name
        bucketlist_to_update.save()
        return bucketlist_to_update, 200

    def delete(self, id):
        bucketlist_to_delete = Bucketlist.query.filter_by(id=id).first()
        bucketlist_to_delete.delete()
