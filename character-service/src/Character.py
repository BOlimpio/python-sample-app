import logging
from db import db

log = logging.getLogger(__name__)


class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    anime = db.Column(db.String(128))

    def __init__(self, id, name, anime):
        self.id = id
        self.name = name
        self.anime = anime

    @classmethod
    def find_by_id(cls, _id):
        log.debug(f'Find character by id: {_id}')
        return cls.query.get(_id)

    @classmethod
    def find_all(cls):
        log.debug('Query for all characters')
        return cls.query.all()

    def save_to_db(self):
        log.debug(f'Save character to database: id= {self.id}, name={self.name}, anime={self.anime}')
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        log.debug(f'Delete character from database: id= {self.id}, name={self.name}, anime={self.anime}')
        db.session.delete(self)
        db.session.commit()

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "anime": self.anime
        }
