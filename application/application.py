from flask import Flask, jsonify, request, json
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from marshmallow import Schema, fields, post_load, ValidationError

import os, sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)
sys.path.append(".")
from tables import User, Event, EventUser

app = Flask(__name__)

engine = create_engine('mysql+pymysql://ppuser:password@localhost:3306/pp?charset=utf8mb4')
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/api/v1/hello-world-26')
def welcome():
    return 'Hello world 26'


class EventUserSchema(Schema):
    event_id = fields.Integer()
    user_id = fields.Integer()

    @post_load
    def make_event(self, data, **kwargs):
        return EventUser(**data)


class EventSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    organizer_id = fields.Integer()
    event_date = fields.Date()
    # users = fields.List(fields.Integer)

    @post_load
    def make_event(self, data, **kwargs):
        return Event(**data)


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()
    password = fields.String()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


@app.route('/events', methods=['GET'])
def get_events():
    try:
        events = session.query(Event).all()
    except NameError:
        return "this name is not defined", 404

    try:
        result = jsonify(EventSchema(many=True).dump(events))
    except ValidationError:
        return "Validation failed", 400

    return result, 200


@app.route('/events', methods=['POST'])
def add_event():
    data = request.get_json()

    try:
        res_event = EventSchema().load(data)
    except ValidationError:
        return "Validation failed", 400

    session.add(res_event)
    session.commit()

    return data, 201

"""
@app.route('/events', methods=['PUT'])
def change_event():
    data = request.get_json()
    
    try:
        res_event = EventSchema().load(data)
    except ValidationError:
        return "Validation failed", 400

    session.add_all([res_event])
    session.commit()

    return data, 201
"""



if __name__ == '__main__':
    app.run(debug=True)


