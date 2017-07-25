from flask_restplus import reqparse

pagination_and_search_arguments = reqparse.RequestParser()
pagination_and_search_arguments.add_argument('page', type=int, required=False)
pagination_and_search_arguments.add_argument('per_page', type=int, required=False, choices=[5, 10, 20, 30, 40, 50, 60,
                                                                                            70, 80, 90, 100],
                                             default=20)
pagination_and_search_arguments.add_argument('q')
