from flask_restplus import fields
from .restplus import api

user_input = api.model('user_input', {
    'email': fields.String(required=True, description='Email address of new or registered user'),
    'password': fields.String(required=True, description='Password of the new user'),
})

user_output = api.model('user_output', {
    'id': fields.Integer(required=True, readOnly=True, description='The user\'s unique identifier.'),
    'email': fields.String(require=True, descritpion='User\'s email address'),
    'password': fields.String(required=True, description='User\'s password'),
    'registered_on': fields.DateTime,
})

bucket_list_item = api.model('bucketlist_item', {
    'id': fields.Integer(required=True, readOnly=True),
    'name': fields.String(required=True),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.Boolean,
})

bucket_list = api.model('bucket_list', {
    'id': fields.Integer(required=True, readOnly=True),
    'name': fields.String(required=True),
    'items': fields.List(fields.Nested(bucket_list_item)),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.Integer,
})

bucket_input = api.model('bucket_input', {
    'name': fields.String(required=True),
})

bucketlist_item_input = api.model('bucket_list_item_input', {
    'name': fields.String(required=True)
})

bucketlist_item_update = api.model('bucketlist_item_update', {
    'name': fields.String(description='Name of the bucketlist item'),
    'done': fields.Boolean(description='Status of the bucketlist item')
})
