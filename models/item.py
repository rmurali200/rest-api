from db import db

# SQL Queries defined
# query_item_by_name = "SELECT * FROM items WHERE name=?"
# insert_new_item = "INSERT INTO items VALUES (?, ?)"
# delete_item_by_name = "DELETE FROM items WHERE name=?"
# update_item_by_name = "UPDATE items SET price=? WHERE name=?"


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    stores = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, name):
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        item = cursor.execute(query_item_by_name, (name,))
        row = item.fetchone()
        connection.close()
        if row:
            return cls(*row)
        else:
            return None
        '''
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
