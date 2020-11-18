import json

from flask import Flask, request


app = Flask(__name__)

PRODUCTS = {
    '12345': {'name': 'Maçã', 'description': 'Maçã muito boa', 'price': 2.50},
    '67890': {'name': 'Laranja', 'description': 'Laranja muito boa', 'price': 3.50}
}


def get_product(product_id):

    product = PRODUCTS.get(product_id)

    return {
        'product': product,
        'status': True if product else False
    }


def update_product(product_id, product_data):
    success = False
    if product_id in PRODUCTS:
        success = True
        for prop_name in product_data:
            if prop_name in PRODUCTS[product_id]:
                PRODUCTS[product_id][prop_name] = product_data[prop_name]

    return {'status': success}


def delete_product(product_id):
    status = False
    if product_id in PRODUCTS:
        status = True
        PRODUCTS.pop(product_id)

    return {'status': status}


def get_all_products():
    return {
        'status': True,
        'products': PRODUCTS
    }


def add_product(product_data):
    success = False
    product_id = product_data.get('product_id')
    if product_id and product_id not in PRODUCTS:
        success = True
        product_data.pop('product_id')
        PRODUCTS[product_id] = product_data

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


if __name__ == '__main__':
  app.run(debug=True)

