from flask import request, abort
from flask_restplus import Resource
from ..restplus import api
from api.models import Bucketlist, BucketlistItem, db, User
from ..parsers import pagination_and_search_arguments
from ..serializers import bucket_list_item, bucket_list, bucket_input, bucketlist_item_input, bucketlist_item_update

bucketlists = api.namespace('bucketlists', description='Bucketlists endpoints')


@bucketlists.route('/')
@api.response(401, 'Invalid user')
@api.header('Authorization', 'JWT Token', required=True)
class Bucketlists(Resource):
    @api.marshal_with(bucket_list)
    @api.response(201, 'Bucketlist created successfully')
    @api.expect(bucket_input)
    def post(self):
        """Creates a new bucketlist"""
        data = request.get_json(force=True)
        name = data.get('name', None)
        access_token = request.headers.get('Authorization')
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist(name=name, created_by=user_id)
                bucketlist.save()
                return bucketlist, 201
        abort(401, 'Failed! You must be logged in to create a bucketlist.')

    @api.marshal_with(bucket_list)
    @api.response(200, 'Bucketlists retrieved successfully')
    @api.expect(pagination_and_search_arguments, validate=True)
    def get(self):
        """Returns all bucketlists owned by a particular user"""
        access_token = request.headers.get('Authorization')
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                arguments = pagination_and_search_arguments.parse_args(request)
                page = arguments.get('page')
                per_page = arguments.get('per_page')
                q = arguments.get('q')
                if q:
                    fetched_bucketlists = Bucketlist.get_all(user_id=user_id).filter(
                        Bucketlist.name.ilike('%' + q + '%')).paginate(page, per_page, False)
                    return fetched_bucketlists.items, 200
                else:
                    fetched_bucketlists = Bucketlist.get_all(user_id=user_id).paginate(page, per_page, False)
                    return fetched_bucketlists.items, 200
        abort(401, 'Invalid user. Please log in to view these bucketlists.')


@bucketlists.route('/<int:id>')
@api.response(401, 'User not authorized to access bucketlist')
@api.header('Authorization', 'JWT Token', required=True)
@api.response(404, 'Bucketlist does not exist')
class BucketlistsWithId(Resource):
    @api.response(200, 'Bucketlist retrieved successfully')
    @api.response(404, 'The requested bucketlist does not exist')
    @api.marshal_with(bucket_list)
    def get(self, id):
        """Returns all bucketlists belonging to a particular user"""
        access_token = request.headers.get('Authorization')
        try:
            queried_bucketlist = Bucketlist.query.filter_by(id=id).first()
            if access_token:
                user_id = User.decode_token(access_token)
                if not isinstance(user_id, str) and user_id == queried_bucketlist.created_by:
                    return queried_bucketlist, 200
            abort(401, 'Invalid user. Please log in to view a bucketlist.')
        except AttributeError:
            abort(404, 'Bucketlist {} does not exist'.format(id))

    @api.marshal_with(bucket_list)
    @api.expect(bucket_input)
    @api.response(200, 'Bucketlist updated successfully')
    def put(self, id):
        """Updates the specified bucketlist"""
        access_token = request.headers.get('Authorization')
        data = request.get_json(force=True)
        new_name = data.get('name')
        try:
            bucketlist_to_update = Bucketlist.query.filter_by(id=id).first()
            if access_token:
                user_id = User.decode_token(access_token)
                if not isinstance(user_id, str) and user_id == bucketlist_to_update.created_by:
                    bucketlist_to_update.name = new_name
                    bucketlist_to_update.save()
                    return bucketlist_to_update, 200
            abort(401, 'Invalid user. Please log in to update a bucketlist.')
        except AttributeError:
            abort(404, 'Bucketlist {} does not exist'.format(id))

    @api.response(204, 'Bucketlist deleted successfully')
    def delete(self, id):
        """Deletes a bucketlist when passed its ID"""
        access_token = request.headers.get('Authorization')
        try:
            bucketlist_to_delete = Bucketlist.query.filter_by(id=id).first()
            if access_token:
                user_id = User.decode_token(access_token)
                if not isinstance(user_id, str) and user_id == bucketlist_to_delete.created_by:
                    bucketlist_to_delete.delete()
                    response = {
                        'message': 'Bucketlist {} deleted successfully'.format(id)
                    }
                    return response, 204
            abort(401, 'Invalid user. Please log in to delete a bucketlist.')
        except AttributeError:
            abort(404, 'Bucketlist {} does not exist'.format(id))


@api.header('Authorization', 'JWT Token', required=True)
@bucketlists.route('/<int:id>/items')
@api.response(401, 'User not authorized to access bucketlist')
@api.response(404, 'Bucketlist does not exist')
class BucketlistItems(Resource):
    @api.expect(bucketlist_item_input)
    @api.marshal_with(bucket_list_item)
    @api.response(201, 'Bucketlist list item created successuflly')
    def post(self, id):
        """Creates a new item in the specified bucketlist"""
        data = request.get_json(force=True)
        item_name = data.get('name')
        access_token = request.headers.get('Authorization')
        try:
            bucketlist = Bucketlist.query.filter_by(id=id).first()
            if access_token:
                user_id = User.decode_token(access_token)
                if not isinstance(user_id, str) and user_id == bucketlist.created_by:
                    new_bucketlist_item = BucketlistItem(item_name, id)
                    new_bucketlist_item.save()
                    return new_bucketlist_item, 201
            abort(401)
        except AttributeError:
            abort(404, 'Bucketlist {} does not exist'.format(id))


@bucketlists.route('/<int:id>/items/<int:item_id>')
@api.header('Authorization', 'JWT Token', required=True)
@api.response(401, 'User not authorized to access bucketlist')
class BucketlistItemsWithId(Resource):
    @api.expect(bucketlist_item_update)
    @api.marshal_with(bucket_list_item)
    @api.response(200, 'Bucketlist item updated successfully')
    @api.response(404, 'Resource not found')
    def put(self, id, item_id):
        """Creates a new item in the specified bucketlist"""
        access_token = request.headers.get('Authorization')
        try:
            bucketlist = Bucketlist.query.filter_by(id=id).first()
            if access_token:
                user_id = User.decode_token(access_token)
                if not isinstance(user_id, str) and user_id == bucketlist.created_by:
                    try:
                        item_to_update = BucketlistItem.query.filter_by(id=item_id).first()
                        if item_to_update.bucketlist_id == id:
                            try:
                                new_item_name = request.json['name']
                                item_to_update.name = new_item_name
                            except KeyError:
                                pass
                            try:
                                new_item_status = request.json['done']
                                item_to_update.done = new_item_status
                            except KeyError:
                                pass
                            item_to_update.save()
                            return item_to_update, 200
                    except AttributeError:
                        abort(404, 'Bucketlist item {} does not exist'.format(item_id))
            abort(401)
        except AttributeError:
            abort(404, 'Bucketlist {} does not exist'.format(id))

    @api.response(200, 'Bucketlist item deleted successfully')
    @api.response(400, 'Resource not found')
    def delete(self, id, item_id):
        """Deletes an item from the specified bucketlist"""
        access_token = request.headers.get('Authorization')
        try:
            bucketlist = Bucketlist.query.filter_by(id=id).first()
            if access_token:
                user_id = User.decode_token(access_token)
                if not isinstance(user_id, str) and user_id == bucketlist.created_by:
                    try:
                        item_to_delete = BucketlistItem.query.filter_by(id=item_id).first()
                        if item_to_delete.bucketlist_id == id:
                            item_to_delete.delete()
                            response = {
                                'message': 'Bucketlist item {} deleted successfully'.format(item_id)
                            }
                            return response, 200
                    except AttributeError:
                        abort(404, 'Bucketlist item {} does not exist'.format(item_id))
            abort(401)
        except AttributeError:
            abort(404, 'Bucketlist {} does not exist'.format(id))
