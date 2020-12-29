INSERT INTO users(id, email, username, password)
VALUES(1, 'user1@gmail.com', 'user1', 'pass1'),
(2, 'user2@gmail.com', 'user2', 'pass2'),
(3, 'user3@gmail.com', 'user3', 'pass3');

INSERT INTO events(id, name, description, event_date, organizer_id)
VALUES(1, 'Event1', 'Description1', '2020-12-11', 1),
(2, 'Event2', 'Description2', '2020-11-1', 2),
(3, 'Event3', 'Description3', '2020-10-22', 2);

INSERT INTO event_user(event_id, user_id)
VALUES(1, 2),
(1, 3),
(2, 1),
(3, 3);