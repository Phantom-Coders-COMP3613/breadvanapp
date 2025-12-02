from App.database import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
       self.name = name
       self.price = price

    def get_json(self):
       return {
           'id': self.id,
           'name': self.name,
           'price': self.price,
       }
    