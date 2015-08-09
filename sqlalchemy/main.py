#!/usr/bin/env python

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from sqlalchemy.ext.declarative import declarative_base

if __name__ == '__main__':
    engine = create_engine('mysql://user:pass@127.0.0.1/database')
    session = sessionmaker()
    session.configure(bind=engine)
    Base = declarative_base()
    Base.metadata.reflect(engine)

    Base.__repr__ = lambda self: '\n'.join(
        '{}: {}'.format(c.name, self.__dict__[c.name]) for c in self.__table__.columns)

    class User(Base):
        __tablename__ = 'user'
        __table_args__ = {'extend_existing': True}

        # user_profile = relationship('UserProfile', backref='user', uselist=False, lazy='joined')
        user_profile = relationship('UserProfile', backref='user', uselist=False)

    class UserProfile(Base):
        __tablename__ = 'user_profile'
        __table_args__ = {'extend_existing': True}

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    s = session()
    u = s.query(User).options(joinedload('user_profile')).first()

    print('user', u)
    print('user_profile', u.user_profile)
    print('user_profile', u.user_profile.user)

    # interactive debug
    # import IPython; IPython.embed()