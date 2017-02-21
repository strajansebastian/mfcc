import json

from flask import Flask
from flask.json import JSONEncoder

from flask import request
from flask import jsonify
from datetime import datetime

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

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder


# product section
@app.route("/product", methods=['GET'])
@crossdomain(origin='*')
def get_product():
    product_id = request.args.get('id')
    query = "SELECT id,name,category,date_added,date_updated,date_removed,attributes FROM products"

    if product_id != None:
        query = "%s WHERE id = %s" % (query, int(product_id))

    result = pom_go.select(query)
    
    return jsonify(result)

@app.route("/product", methods=['POST'])
@crossdomain(origin='*')
def post_product():
    product_id = request.args.get('id')
    category = request.args.get('category')
    attributes = request.args.get('attributes')
    
    query = "UPDATE products SET category = %s, attributes=%s, date_updated=now() WHERE id = %s"
    (urs, urn) = pom_go.update(query, (category, attributes, product_id))

    return jsonify('{"updated_status":"%s", "updated_row_number": "%s"}' % (urs, urn))

@app.route("/product", methods=['PUT'])
@crossdomain(origin='*')
def put_product():
    name = request.args.get('name')
    category = request.args.get('category')
    attributes = request.args.get('attributes')

    query = "INSERT INTO products(name, category, date_added, attributes) VALUES(%s,%s,now(),%s)"
    (irs, irn) = pom_go.insert(query, (name, category, attributes,))

    return jsonify('{"inserted_status": "%s", "product": "%s", "inserted_row_number": "%s"}' % (irs, name, irn))

@app.route("/product", methods=['DELETE'])
@crossdomain(origin='*')
def delete_product():
    product_id = request.args.get('id')

    query = "DELETE FROM products WHERE id = %s"
    (drs, drn) = pom_go.delete(query, (product_id,))

    return jsonify('{"deleted_status":"%s", "deleted_row_number": "%s"}' % (drs, drn))

# useless crap because option is called for some methods by the browser/ng framework
@app.route("/product", methods=['OPTIONS'])
@crossdomain(origin='*')
def options_product():
    return None

@app.route("/product_location", methods=['GET'])
@crossdomain(origin='*')
def get_product_location():
    product_id = request.args.get('id')
    query = "SELECT id,product_id,date_added,date_removed,site_name,site_url FROM product_locations"

    if product_id != None:
        query = "%s WHERE product_id = %s" % (query, int(product_id))

    result = pom_go.select(query)
    
    return jsonify(result)

# @app.route("/product_location", methods=['POST'])
# @crossdomain(origin='*')
# def post_product_location():
#     return "POST product location"

# useless crap because option is called for some methods by the browser/ng framework
@app.route("/product_location", methods=['OPTIONS'])
@crossdomain(origin='*')
def options_product_location():
    return None

@app.route("/product_location", methods=['PUT'])
@crossdomain(origin='*')
def put_product_location():
    product_id = request.args.get('product_id')
    site_name = request.args.get('site_name')
    site_url = request.args.get('site_url')

    query = "INSERT INTO product_locations(product_id, site_name, site_url, date_added) VALUES(%s,%s,%s,now())"
    (irs, irn) = pom_go.insert(query, (product_id, site_name, site_url,))

    return jsonify('{"inserted_status": "%s", "product_id": "%s", "inserted_row_number": "%s"}' % (irs, product_id, irn))

@app.route("/product_location", methods=['DELETE'])
@crossdomain(origin='*')
def delete_product_location():
    product_location_id = request.args.get('id')

    query = "DELETE FROM product_locations WHERE id = %s"
    (drs, drn) = pom_go.delete(query, (product_location_id,))

    return jsonify('{"deleted_status":"%s", "deleted_row_number": "%s"}' % (drs, drn))


@app.route("/product_price", methods=['GET'])
@crossdomain(origin='*')
def get_product_price():
    product_id = request.args.get('id')
    query = "SELECT id,product_id,product_location_id,price,price_currency,date_added FROM prices"

    if product_id != None:
        query = "%s WHERE product_id = %s" % (query, int(product_id))

    result = pom_go.select(query)

    return jsonify(result)

@app.route("/product_price", methods=['PUT'])
@crossdomain(origin='*')
def put_product_price():
    product_id = request.args.get('product_id')
    product_location_id = request.args.get('product_location_id')
    price = request.args.get('price')
    price_currency = request.args.get('price_currency')

    query = "INSERT INTO prices(product_id, product_location_id, price, price_currency, date_added) VALUES(%s,%s,%s,%s,now())"
    (irs, irn) = pom_go.insert(query, (product_id, product_location_id, price, price_currency,))

    return jsonify('{"inserted_status": "%s", "product": "%s", "inserted_row_number": "%s"}' % (irs, name, irn))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

