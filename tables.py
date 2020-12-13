from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://lab:password@localhost:3306/pplab?charset=utf8mb4', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    event_date = Column(Date, nullable=False)
    organizer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    organizer = relationship('User', back_populates='organized_events')
    users = relationship('User', secondary='event_user')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(60), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    organized_events = relationship('Event', back_populates='')
    events = relationship('Event', secondary='event_user')


class EventUser(Base):
    __tablename__ = 'event_user'

    event_id = Column(Integer, ForeignKey('events.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

