from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm, Column, String, Boolean

import logging

from nl.carcharging.models.Base import Base, DbSession
from nl.carcharging.config.WebAppConfig import WebAppConfig

# generate_password_hash(password, method='sha256')

class User(Base):
    """
    """
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    password = Column(String)
    authenticated = Column(Boolean, default=False)

    def __init__(self, username=None, password=None, authenticated=None):
        self.logger = logging.getLogger('nl.carcharging.models.User')
        # If the variables are already initialized by the reconstructor, let them be
        if self.username is None and self.password is None:
            self.username = username
            self.password = password
            self.authenticated = authenticated

    # sqlalchemy calls __new__ not __init__ on reconstructing from database. Decorator to call this method
    @orm.reconstructor   
    def init_on_load(self):
        self.__init__()

    @staticmethod
    def get(username):
        db_session = DbSession()
        user = None
        try:
            # Should be only one, return last modified
            user = db_session.query(User) \
                            .filter(User.username == username) \
                            .first()
        except Exception as e:
            # Nothing to roll back
            self.logger.error("Could not query {} table in database".format(self.__tablename__ ), exc_info=True)
        return user


    def save(self) -> None:
        db_session = DbSession()
        try:
            db_session.add(self)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            self.logger.error("Could not commit to {} table in database".format(self.__tablename__ ), exc_info=True)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    # Delete this user
    def delete(self):
        db_session = DbSession()
        try:
            # Should be only one
            num_rows_deleted = db_session.query(User) \
                                         .filter(User.username == self.username) \
                                         .delete()
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            self.logger.error("Could not commit to {} table in database".format(self.__tablename__ ), exc_info=True)


    # Delete all users
    @staticmethod
    def delete_all():
        db_session = DbSession()
        try:
            # Should be only one
            num_rows_deleted = db_session.query(User) \
                                         .delete()
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            self.logger.error("Could not commit to {} table in database".format(self.__tablename__ ), exc_info=True)


