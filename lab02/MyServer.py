import json
from flask import Flask, request, jsonify
from flask import send_file

last_id = -1

class Product:
    def __init__(self, name, description):
        global last_id
        last_id += 1
        self.id = last_id
        self.name = name
        self.description = description
        self.icon = None

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'description', self.description
        if not self.icon is None:
            yield 'icon', self.icon

    def SetField(self, name: str, value: str):
        if name == 'name':
            self.name = value
        if name == 'description':
            self.description = value
        
    def AddImage(self, path: str):
        self.icon = path

    def GetImage(self):
        return self.icon

app = Flask(__name__)

allProducts = dict()

empty_product = Product("Empty", "This object doesn't exist")

@app.route('/product', methods=['POST'])
def CreateProduct():
    data = json.loads(request.data)
    new_product = Product(data['name'], data['description'])
    allProducts[new_product.id] = new_product
    return jsonify(dict(new_product))


@app.route('/product/<product_id>', methods=['DELETE'])
def DeleteProduct(product_id):
    last_copy = jsonify(dict(allProducts[int(product_id)]))
    allProducts[int(product_id)] = empty_product
    return last_copy


@app.route('/product/<product_id>', methods=['PUT'])
def UpdateProduct(product_id):
    data = json.loads(request.data)

    ind = int(product_id)
    for field in data:
        allProducts[ind].SetField(field, data[field])

    return jsonify(dict( allProducts[int(product_id)]))


@app.route('/product/<product_id>', methods=['GET'])
def GetProduct(product_id):
    return jsonify(dict(allProducts[int(product_id)]))



@app.route('/products/', methods=['GET'])
def GetAllProducts():

    answer = dict()
    for key, value in zip(allProducts.keys(), allProducts.values()):
        if value.id == 0:
            continue
        answer[key] = json.dumps(dict(value))
    return jsonify(answer)


@app.route('/product/<product_id>/image', methods=['POST'])
def upload_product_image(product_id):
    product = allProducts[int(product_id)]
    file = request.files['icon']   
    file.save(f'{product.id}.jpg')
    return jsonify({})


@app.route('/product/<product_id>/image')
def get_product_icon(product_id):
    product = allProducts[int(product_id)]
    return send_file(f'{product.id}.jpg', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
