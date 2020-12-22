from flask import Flask, jsonify, request, json
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from marshmallow import Schema, fields, post_load, ValidationError
from flask_jwt import JWT, jwt_required, current_identity

import os, sys

parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)
sys.path.append(".")
from tables import User, Event, EventUser, engine, Session

app = Flask(__name__)
bcrypt = Bcrypt(app)

session = Session()


@app.route('/api/v1/hello-world-26')
def welcome():
    return 'Hello world 26'


class EventUserSchema(Schema):
    event_id = fields.Integer()
    user_id = fields.Integer()
    # event_id = fields.Nested('EventSchema', many=True)
    # user_id = fields.Nested('UserSchema', many=True)

    @post_load
    def make_event(self, data, **kwargs):
        return EventUser(**data)


class EventSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    organizer_id = fields.Integer()
    event_date = fields.Date()
    users = fields.List(fields.Nested(lambda: UserSchema(only=["id"])))

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
    users = data.pop('users', None)
    try:
        res_event = EventSchema().load(data)
    except ValidationError:
        return "Validation failed", 400

    if users is not None:
        res_event.users = []
        for id in users:
            res_event.users.append(session.query(User).filter(User.id == id).first())

    session.add(res_event)
    session.commit()
    event = EventSchema().dump(res_event)

    return event, 201


@app.route('/events', methods=['PUT'])
def change_event():
    data = request.get_json()

    try:
        res_event = EventSchema(only=['id']).load({'id': data['id']})
    except ValidationError:
        return "Validation failed", 400

    try:
        event = session.query(Event).filter(Event.id == data['id']).first()
    except NameError:
        return "this name is not defined", 404

    event.name = event.name if not 'name' in data else data['name']
    event.description = event.description if not 'description' in data else data['description']
    event.event_date = event.event_date if not 'event_date' in data else data['event_date']
    event.organizer_id = event.organizer_id if not 'organizer_id' in data else data['organizer_id']

    if 'users' in data:
        event.users = []
        for id in data['users']:
            event.users.append(session.query(User).filter(User.id == id).first())

    session.commit()
    new_event = EventSchema().dump(event)

    return new_event, 201


@app.route('/events/<eventID>', methods=['DELETE'])
def delete_event(eventID):
    schema = EventSchema(only=['id'])
    try:
        schema.load({'id': eventID})
    except ValidationError as err:
        return err.messages, 404

    try:
        event = session.query(Event).filter(Event.id == eventID).first()
    except NameError:
        return "this name is not defined", 404

    session.delete(event)
    session.commit()

    return "Deleted successfully", 200


@app.route('/events/conected/<userID>', methods=['GET'])
def get_user_events(userID):
    schema = UserSchema(only=['id'])
    try:
        schema.load({'id': userID})
    except ValidationError as err:
        return err.messages, 404

    try:
        events = []
        eventusers = session.query(EventUser).filter(EventUser.user_id == userID).all()
        for eventuser in eventusers:
            events += session.query(Event).filter(Event.id == eventuser.event_id).all()

    except ValidationError:
        return "Validation failed", 400

    try:
        result = jsonify(EventSchema(many=True).dump(events))
    except ValidationError:
        return "Validation failed", 400

    return result, 200


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    data = dict(username=data['username'], email=data['email'],
                password=bcrypt.generate_password_hash(data['password']).decode('utf-8'))

    schema = UserSchema()
    if not session.query(User).filter(User.username == data['username']).first() is None:
        return "This username already exists"

    try:
        user = schema.load(data)
    except ValidationError as err:
        return err.messages, 400

    session.add(user)
    session.commit()
    return data, 201


@app.route('/users/<username>', methods=['GET'])
def get_user_by_ID(username):
    schema = UserSchema(only=['username'])
    try:
        schema.load({'username': username})
    except ValidationError as err:
        return err.messages, 404

    schema = UserSchema()
    try:
        user = session.query(User).filter(User.username == username).first()
    except NameError:
        return "this name is not defined", 404

    try:
        user_data = UserSchema().dump(user)
    except ValidationError:
        return "Validation failed", 400

    return user_data, 200


@app.route('/sign-in', methods=['GET'])
def sign_in():
    username = request.args.get('username')
    password = request.args.get('password')

    user = session.query(User).filter(User.username == username).first()
    if user is None:
        return "No such user", 404

    check_password = bcrypt.check_password_hash(user.password, password)
    if not check_password:
        return "Wrong password", 400

    data = UserSchema().dump(user)
    return data, 200


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return 'Logout successfully, 200'


if __name__ == '__main__':
    app.run(debug=True)
