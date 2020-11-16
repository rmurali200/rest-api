from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "No store with '{}' found".format(name)}, 404

    @jwt_required()
    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "A store by the name '{}' already exists".format(name)}, 400  # Bad request error
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()
            except:
                return {"message": "An internal error occurred while creating store with name '{}'".format(name)}, 500
        return {"message": "A new store with name '{}' has been created".format(name)}, 200

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {"message": "An internal error occurred while deleting '{}' store".format(name)}, 500

        return {"message": "Store with name '{}' deleted".format(name)}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        stores = StoreModel.query.all()
        return {'stores': [store.json() for store in stores]}, 200 if stores else 404
