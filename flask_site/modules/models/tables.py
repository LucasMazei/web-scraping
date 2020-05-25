from modules.__init__ import db


class Waiter(db.Model):
    __tablename__ = "waiters"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    phone = db.Column(db.String)

    def __init__(self, username, password, name, phone):
        self.username = username
        self.password = password
        self.name = name
        self.phone = phone

    def __repr__(self):
        # return "<User %r" %self.username
        return "%r" % self.username

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def getUser(user_name=False):
        users = {}
        for waiter in Waiter.query.order_by(Waiter.id).all():
            if user_name and user_name in Waiter.query.order_by(Waiter.id).all():
                if waiter.username != user_name:
                    continue
            user_dict = {
                "password": waiter.password,
                "name": waiter.name,
                "email": waiter.phone
            }
            users[waiter.username] = user_dict
        return users


class Tables(db.Model):
    __tablename__ = "tables"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiters.id'))
    is_occupied = db.Column(db.Boolean)

    user = db.relationship('Waiter', foreign_keys=waiter_id)

    def __init__(self, number, waiter_id, is_occupied=False):
        self.number = number
        self.waiter_id = waiter_id
        self.is_occupied = is_occupied

    def __repr__(self):
        return "Table: %r" % self.number


class Dish(db.Model):
    # TODO change 'Dish' for 'Menu'
    __tablename__ = "Menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    price = db.Column(db.String)
    ingredients = db.Column(db.String)
    image = db.Column(db.String)
    serves = db.Column(db.Integer)
    number_asked = db.Column(db.Integer)

    def __init__(self, name, price, ingredients, image, serves=0, number_asked=0):
        self.name = name
        self.price = price
        self.ingredients = ingredients
        self.image = image
        self.serves = serves
        self.number_asked = number_asked

    def __repr__(self):
        return "Dish: %r" % self.name

    def getDishes():
        dishes = {}
        for dish in Dish.query.order_by(Dish.id).all():
            dish_dict = {
                'Price': dish.price,
                'Igredientes': dish.ingredients,
                'img': dish.image,
                'Serves': dish.serves,
                'number_asked': dish.number_asked
            }
            dishes[dish.name] = dish_dict
        return dishes


class Orders(db.Model):
    __tablename__ = "Orders"

    id = db.Column(db.Integer, primary_key=True)
    time_asked = db.Column(db.DateTime)
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiters.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'))
    amount = db.Column(db.Integer)

    def __init__(self, time_asked, waiter_id, dish_id, table_id, amount=1):
        self.time_asked = time_asked
        self.waiter_id = waiter_id
        self.dish_id = dish_id
        self.table_id = table_id
        self.amount = amount

    def __repr__(self):
        return "Order: %r" % self.id

    def getOrders():
        orders = {}
        for order in Orders.query.order_by(Orders.time_asked).all():
            order_dict = {
                'time_asked': order.time_asked,
                'waiter_id': order.waiter_id,
                'table_id': order.table_id,
                'amount': order.amount,
            }
            orders[order.id] = order_dict
        return orders
