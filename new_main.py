from flask import Flask, request, jsonify
from http import HTTPStatus
from models import db, Car

app = Flask(__name__)

app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

'''
{
id: 1,
man: mankana,
model: modeli,
instok: yes,
price: 300
}
'''


def car_to_dict(car):
    car_dict = {
        'id': car.id,
        'manufacturer': car.manufacturer,
        'model': car.model,
        'price': car.price,
        'instock': car.instock
    }
    return car_dict


@app.route('/')
def car_list():
    cars = Car.query.all()
    return jsonify([car_to_dict(car) for car in cars])


@app.route('/car/<int:car_id>')
def get_car_by_id(car_id):
    car = Car.query.get(car_id)

    if car is None:
        return jsonify("no car"), 404
    return jsonify(car_to_dict(car))


@app.route('/create', methods=['POST'])
def create_car():
    data = request.get_json()

    man = data.get('manufacturer')
    model = data.get('model')
    instock = data.get('instock')
    price = data.get('price')

    try:
        price = float(price)
    except (ValueError, TypeError):
        return jsonify("Invalid price"), HTTPStatus.BAD_REQUEST

    car = Car(manufacturer=man, model=model, instock=instock, price=price)

    db.session.add(car)
    db.session.commit()

    return jsonify('created'), HTTPStatus.CREATED


@app.route('/update/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = Car.query.get(car_id)
    if car is None:
        return jsonify("no car"), 404

    data = request.get_json()
    if 'manufacturer' in data:
        car.manufacturer = data.get('manufacturer')
    if 'model' in data:
        car.model = data.get('model')
    if 'instock' in data:
        car.instock = data.get('instock')
    if 'price' in data:
        car.price = data.get('price')

    db.session.commit()
    return jsonify('updated'), HTTPStatus.OK


@app.route('/delete/<int:car_id>', methods=["DELETE"])
def delete_car(car_id):
    car = Car.query.get(car_id)
    db.session.delete(car)
    db.session.commit()
    return jsonify('deleted'), HTTPStatus.OK


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)
