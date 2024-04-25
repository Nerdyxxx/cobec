from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import random
import string


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123123123@localhost/postgres?client_encoding=utf8' 
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    # rand u p
    random_username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    

    new_user = User(username=random_username, password=random_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'username': random_username, 'password': random_password}), 200




@app.route('/register_or_login', methods=['POST'])
def register_or_login():
    data = request.json
    


    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first() # utf-8 xx

    if user:
        if user.password == password:


            return jsonify({'message': 'Успешный вход.'}), 50
        else:
            return jsonify({'message': 'Неверный пароль, попробуйте снова.'}), 50
    else:
        try:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'Регистрация завершена.'}), 50
        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': 'Имя пользователя уже занято.'}), 50
        



@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all() # utf-8 xx
    return jsonify([{'id': pizza.id, 'name': pizza.name} for pizza in pizzas]), 200


@app.route('/pizza/<int:pizza_id>', methods=['GET'])
def get_pizza(pizza_id):
    pizza = Pizza.query.get(pizza_id) # utf-8 xx
    if pizza:
        return jsonify({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}), 200
    else:
        return jsonify({'message': 'Пицца не найдена'}), 404
    

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    pizza_id = data.get('pizza_id')
    kolvo = data.get('kolvo')

    # code zakaz
    return jsonify({'message': 'Вы успешно заказали пиццу'}), 201


if __name__ == '__main__':
    app.run(debug=True)