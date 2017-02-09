import json

from flask import Flask
from flask import request

import pom_utils.generic_operations as pom_go

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

app = Flask(__name__)

connection = None
hostname = 'localhost'
username = 'price_o_meter'
# haha password in plain text - need to provide some sort of configuration to avoid this shit
password = 'use_FUAR-10Cl'
database = 'price_o_meter'

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            # if not attach_to_all and request.method != 'OPTIONS':
            #     return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

# product section
@app.route("/products")
@crossdomain(origin='*')
def get_products():
    query = "SELECT id,name,category,date_added,date_updated,date_removed,attributes FROM products"
    result = pom_go.select(query)
    
    return json.dumps(result, default=date_handler)

@app.route("/product", methods=['GET'])
@crossdomain(origin='*')
def get_product():
    query = "SELECT id,name,category,date_added,date_updated,date_removed,attributes FROM products WHERE id = %s" % (1)
    result = pom_go.select(query)

    return json.dumps(result, default=date_handler)

@app.route("/product_update", methods=['GET', 'POST'])
@crossdomain(origin='*')
def post_product():
    product_id = request.args.get('id')
    category = request.args.get('category')
    # attributes = request.args.get('attributes')
    
    query = "UPDATE products SET category = %s, attributes=%s WHERE id = %s"
    result = pom_go.update(query, (category, attributes, product_id))

    return "{'updated':'%s'}" % (result)

@app.route("/product_insert", methods=['GET', 'PUT', 'OPTIONS'])
@crossdomain(origin='*')
def put_product():
    name = request.args.get('name')
    category = request.args.get('category')
    attributes = request.args.get('attributes')

    query = "INSERT INTO products(name, category, date_added, attributes) VALUES(%s,%s,now(),%s)"
    result = pom_go.insert(query, (name, category, attributes))

    return "{'inserted': '%s', 'product': '%s'}" % (result, name)

@app.route("/product_delete", methods=['GET', 'DELETE'])
@crossdomain(origin='*')
def delete_product():
    product_id = request.args.get('id')
    
    query = "DELETE FROM products WHERE id = %s"
    result = pom_go.update(query, (product_id))

    return "{'deleted':'%s'}" % (result)

# product location section
@app.route("/product_locations", methods=['GET'])
@crossdomain(origin='*')
def get_product_locations():
    return "GET product locations"

@app.route("/product_location", methods=['GET'])
@crossdomain(origin='*')
def get_product_location():
    return "GET product location"

@app.route("/product_location", methods=['POST'])
@crossdomain(origin='*')
def post_product_location():
    return "POST product location"

@app.route("/product_location", methods=['PUT'])
@crossdomain(origin='*')
def put_product_location():
    return "PUT product location"

@app.route("/product_location", methods=['DELETE'])
@crossdomain(origin='*')
def delete_product_location():
    return "DELETE product location"


# product prices location
@app.route("/product_prices", methods=['GET'])
@crossdomain(origin='*')
def get_product_prices():
    return "GET product prices"

@app.route("/product_price", methods=['GET'])
@crossdomain(origin='*')
def get_product_price():
    return "GET product price"

@app.route("/product_price", methods=['PUT'])
@crossdomain(origin='*')
def put_product_price():
    return "PUT product price"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

