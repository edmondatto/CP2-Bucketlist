from flask import request
from flask_restplus import Resource, fields
from .restplus import api
from app.models import Bucketlist, BucketlistItem, db

bucketlists = api.namespace('bucketlists', description='Bucketlists endpoints')

bucket_list = api.model('bucket_list', {
    'id': fields.Integer(required=True, readOnly=True),
    'name': fields.String(required=True),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.Integer,
})

bucket_list_item = api.model('bucketlist_item', {
    'id': fields.Integer(required=True, readOnly=True),
    'name': fields.String(required=True),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.Boolean,
})

bucket_input = api.model('bucket_input', {
    'name': fields.String(required=True),
})

bucketlist_item_input = api.model('bucket_list_item_input', {
    'name': fields.String(required=True)
})


@bucketlists.route('/')
class Bucketlists(Resource):
    @api.marshal_with(bucket_list)
    @api.expect(bucket_input)
    def post(self):
        """Creates a new bucketlist"""
        name = request.json['name']
        bucketlist = Bucketlist(name=name, created_by=1)
        bucketlist.save()
        return bucketlist, 201

    @api.marshal_with(bucket_list)
    def get(self):
        """Returns a bucketlist when passed its ID"""
        fetched_bucketlists = Bucketlist.get_all(self)
        return fetched_bucketlists, 200


@bucketlists.route('/<int:id>')
class BucketlistsWithId(Resource):
    @api.marshal_with(bucket_list)
    def get(self, id):
        """Returns all bucketlists belonging to a particular user"""
        queried_bucketlist = Bucketlist.query.filter_by(id=id).first()
        return queried_bucketlist, 200

    @api.marshal_with(bucket_list)
    @api.expect(bucket_input)
    def put(self, id):
        """Updates the specified bucketlist"""
        new_name = request.json['name']
        bucketlist_to_update = Bucketlist.query.filter_by(id=id).first()
        bucketlist_to_update.name = new_name
        bucketlist_to_update.save()
        return bucketlist_to_update, 200

    def delete(self, id):
        """Deletes a bucketlist when passed its ID"""
        try:
            bucketlist_to_delete = Bucketlist.query.filter_by(id=id).first()
            bucketlist_to_delete.delete()
            return 200
        except AttributeError:
            return 405


@bucketlists.route('/bucketlists/<int:id>/items')
class BucketlistItems(Resource):
    @api.marshal_with(bucketlist_item_input)
    @api.expect(bucket_input)
    def post(self, id):
        """Creates a new item in the specified bucketlist"""
        item_name = request.json['name']
        new_bucketlist_item = BucketlistItem(item_name, id)
        new_bucketlist_item.save()
        return new_bucketlist_item, 201


@bucketlists.route('/bucketlists/<int:id>/items/<item_id>')
class BucketlistItemsWithId(Resource):
    @api.expect(bucket_input)
    @api.marshal_with(bucket_list_item)
    def put(self, id, item_id):
        """Creates a new item in the specified bucketlist"""
        new_item_name = request.json['name']
        item_to_update = BucketlistItem.query.filter_by(id=item_id).first()
        if item_to_update.bucketlist_id == id:
            item_to_update.name = new_item_name
            item_to_update.save()
            return item_to_update

    # @api.expect(bucket_input)
    @api.marshal_with(bucket_list_item)
    def delete(self, id, item_id):
        """Deletes an item from the specified bucketlist"""
        item_to_delete = BucketlistItem.query.filter_by(id=item_id).first()
        if item_to_delete.bucketlist_id == id:
            item_to_delete.delete()
            return 200
