from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, Car

app = Flask(__name__)

app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def Index():
    all_cars = Car.query.all()

    return render_template('index.html', cars=all_cars)


@app.route('/insert', methods=["POST", "GET"])
def insert():
    if request.method == 'POST':
        manufacturer = request.form['manufacturer']
        model = request.form['model']
        instock = request.form['instock']
        price_raw = request.form['price']
        price = float(price_raw)

        my_data = Car(manufacturer=manufacturer, model=model, instock=instock, price=price)

        db.session.add(my_data)
        db.session.commit()
        flash('Car inserted')
        return redirect(url_for('Index'))
    return redirect(url_for('Index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        car_id = request.form.get('id')
        try:
            car_id = int(car_id)
        except (TypeError, ValueError):
            flash("Invalid car id")
            return redirect(url_for('Index'))

        my_data = Car.query.get(car_id)
        if my_data is None:
            flash("Car not found")
            return redirect(url_for('Index'))

        my_data.manufacturer = request.form['manufacturer']
        my_data.model = request.form['model']
        my_data.instock = request.form['instock']
        price_raw = request.form['price']
        try:
            my_data.price = float(price_raw)
        except (TypeError, ValueError):
            flash('Invalid price')
            return redirect(url_for('Index'))
        print(my_data.instock)
        db.session.commit()
        flash("Technique Update Successfully")

        return redirect(url_for('Index'))

    return redirect(url_for('Index'))


@app.route('/delete/<id>', methods=["POST", "GET"])
def delete(id):
    my_data = Car.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Car deleted')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(debug=True)
