from flask import Flask

import pom_utils.generic_operations as pom_go

pom_go.select("", "SELECT * FROM DUAL")

app = Flask(__name__)


# product section
@app.route("/products")
def get_products():
    return "Hello World!"

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
