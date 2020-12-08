import json

from flask import Flask, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)

PRODUCTS = {
    '12345': {'name': 'Maçã', 'description': 'Maçã muito boa', 'price': 2.50},
    '67890': {'name': 'Laranja', 'description': 'Laranja muito boa', 'price': 3.50}
}

USERS = {
    '12345': {'public': {'first_name': 'Abc', 'last_name': 'Def', 'email': 'abc@gmail.com'}, 'private': {'password': '123'}},
    '67890': {'public': {'first_name': 'Qwe', 'last_name': 'Lmp', 'email': 'def@gmail.com'}, 'private': {'password': '123'}},
}


def get_product(product_id):

    product = PRODUCTS.get(product_id)

    return {
        'product': product,
        'status': True if product else False
    }


def get_user(user_id):

    user = USERS.get(user_id, {})

    return {
        'user': user.get('public'),
        'status': True if user else False
    }


def update_product(product_id, product_data):
    success = False
    if product_id in PRODUCTS:
        for prop_name in product_data:
            if prop_name in PRODUCTS[product_id]:
                PRODUCTS[product_id][prop_name] = product_data[prop_name]
                success = True

    return {'status': success}


def update_user(user_id, user_data):
    success = False
    if user_id in USERS:
        for access in USERS[user_id]:
            if access in user_data:
                for prop_name in user_data[access]:
                    if prop_name in USERS[user_id][access]:
                        print(prop_name, user_id, access)
                        USERS[user_id][access][prop_name] = user_data[access][prop_name]
                        success = True

    return {'status': success}


def delete_product(product_id):
    status = False
    if product_id in PRODUCTS:
        status = True
        PRODUCTS.pop(product_id)

    return {'status': status}


def delete_user(user_id):
    status = False
    if user_id in USERS:
        status = True
        USERS.pop(user_id)

    return {'status': status}


def get_all_products():
    return {
        'status': True,
        'products': PRODUCTS
    }


def get_all_users():
    return {
        'status': True,
        'users': {user_id: USERS[user_id]['public'] for user_id in USERS}
    }


def add_product(product_data):
    success = False
    product_id = product_data.get('product_id')
    if product_id and product_id not in PRODUCTS:
        success = True
        product_data.pop('product_id')
        PRODUCTS[product_id] = product_data

    return {'status': success}


def add_user(user_data):
    success = False
    user_id = user_data.get('user_id')
    if user_id and user_id not in USERS:
        success = True
        user_data.pop('user_id')
        USERS[user_id] = user_data

    return {'status': success}


@app.route('/product/<string:product_id>', methods=['GET', 'UPDATE', 'DELETE'])
def manage_product(product_id):

    response = {}

    method = request.method
    if method == 'GET':
        response = get_product(product_id)
    elif method == 'UPDATE':
        product_data = request.get_json()
        response = update_product(product_id, product_data)
    else:
        response = delete_product(product_id)

    return json.dumps(response, ensure_ascii=False), \
            200 if response.get('status') else 400


@app.route('/product', methods=['GET', 'POST'])
def manage_products():

    method = request.method
    if method == 'GET':
        response = get_all_products()
    else:
        product_data = request.get_json()
        response = add_product(product_data)

    return json.dumps(response, ensure_ascii=False), \
            200 if response.get('status') else 400


@app.route('/user/<string:user_id>', methods=['GET', 'UPDATE', 'DELETE'])
def manage_user(user_id):

    response = {}

    method = request.method
    if method == 'GET':
        response = get_user(user_id)
    elif method == 'UPDATE':
        user_data = request.get_json()
        response = update_user(user_id, user_data)
    else:
        response = delete_user(user_id)

    return json.dumps(response, ensure_ascii=False), \
            200 if response.get('status') else 400


@app.route('/user', methods=['GET', 'POST'])
def manage_users():

    method = request.method
    if method == 'GET':
        response = get_all_users()
    else:
        user_data = request.get_json()
        response = add_user(user_data)

    return json.dumps(response, ensure_ascii=False), \
            200 if response.get('status') else 400


@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    status = False
    for user_id in USERS: 
        if (USERS[user_id]['public']['email'] == email and \
            USERS[user_id]['private']['password'] == password):
                status = True

    return json.dumps({'status': status}), 200 if status else 401


if __name__ == '__main__':
  app.run(debug=True)
