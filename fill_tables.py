from tables import Session, User, Event

session = Session()

user1 = User(email='test1@gmail.com', username='user1', password='pass1')
user2 = User(email='test2@gmail.com', username='user2', password='pass2')
user3 = User(email='test3@gmail.com', username='user3', password='pass3')

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

