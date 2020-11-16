# import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

# query_all_items = "SELECT * FROM items"


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id"
                        )
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404  # Not Found error

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400  # Bad request

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An internal error occurred while inserting item'}, 500  # Internal server error

        return item.json(), 201  # Create successful

    @jwt_required()
    def delete(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # items.remove(item)
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete_from_db()
            except:
                return {'message': 'An error occurred while deleting the item'}, 500

        return {'message': 'Item {} deleted'.format(name)}, 200

    @jwt_required()
    def put(self, name):
        item = ItemModel.find_by_name(name)
        data = Item.parser.parse_args()

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        try:
            item.save_to_db()
        except:
            return {'message': 'An internal error occurred while adding/updating item'}, 500
        return item.json(), 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = ItemModel.query.all()
        return {'items': [item.json() for item in items]}, 200 if items else 404
