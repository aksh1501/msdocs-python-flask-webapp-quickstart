import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://adminuser:anmol#2002@anmol-item-registery-server.postgres.database.azure.com:5432/'
db = SQLAlchemy(app)

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'cost': self.cost, 'description': self.description }


@app.route('/')
def index():
    return json.dumps({'name': 'anmol',
                       'email': 'alice@outlook.com'})


@app.route('/getitems', methods=['GET'])
def list_items():
    items = Items.query.all()
    return jsonify([item.to_dict() for item in items])


@app.route('/additems', methods=['POST'])
def add_items():
    data = request.json
    print(data)
    name = data.get('name')
    cost = data.get('cost')
    description = data.get('description')

    if name is None or cost is None:
        return jsonify({'error': 'Name and cost are required'}), 400

    try:
        item = Items(name=name, cost=cost, description=description)
        db.session.add(item)
        db.session.commit()
        return jsonify(item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
