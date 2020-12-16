from tables import Session, User, Event

session = Session()

user1 = User(email='test1@gmail.com', username='user1', password='E6C3DA5B206634D7F3F3586D747FFDB36B5C675757B380C6A5FE5C570C714349')
user2 = User(email='test2@gmail.com', username='user2', password='1BA3D16E9881959F8C9A9762854F72C6E6321CDD44358A10A4E939033117EAB9')
user3 = User(email='test3@gmail.com', username='user3', password='3ACB59306EF6E660CF832D1D34C4FBA3D88D616F0BB5C2A9E0F82D18EF6FC167')

event1 = Event(name='Event1', description='Description1', event_date='2020-12-11', organizer=user1, users=[user2, user3])
event2 = Event(name='Event2', description='Description2', event_date='2020-12-12', organizer=user2, users=[user1, user3])
event3 = Event(name='Event3', description='Description3', event_date='2020-12-13', organizer=user1)

session.add(event1)
session.add(event2)
session.add(event3)
session.add(user1)
session.add(user2)
session.add(user3)

session.commit()

