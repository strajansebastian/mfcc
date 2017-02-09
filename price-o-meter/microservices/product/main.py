import json

from flask import Flask

import pom_utils.generic_operations as pom_go

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

app = Flask(__name__)

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
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

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
    result = pom_go.select("", query)
    
    return json.dumps(result, default=date_handler)

@app.route("/product", methods=['GET'])
def get_product():
    return "RETURN product"

@app.route("/product", methods=['POST'])
def post_product():
    return "UPDATE product"

@app.route("/product", methods=['PUT'])
def put_product():
    return "ADD product"

@app.route("/product", methods=['DELETE'])
def delete_product():
    return "DELETE product"


# product location section
@app.route("/product_locations", methods=['GET'])
def get_product_locations():
    return "GET product locations"

@app.route("/product_location", methods=['GET'])
def get_product_location():
    return "GET product location"

@app.route("/product_location", methods=['POST'])
def post_product_location():
    return "POST product location"

@app.route("/product_location", methods=['PUT'])
def put_product_location():
    return "PUT product location"

@app.route("/product_location", methods=['DELETE'])
def delete_product_location():
    return "DELETE product location"


# product prices location
@app.route("/product_prices", methods=['GET'])
def get_product_prices():
    return "GET product prices"

@app.route("/product_price", methods=['GET'])
def get_product_price():
    return "GET product price"

@app.route("/product_price", methods=['PUT'])
def put_product_price():
    return "PUT product price"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

