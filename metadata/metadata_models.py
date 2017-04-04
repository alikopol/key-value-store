# coding: utf-8
from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Key(Base):
    __tablename__ = 'key'
    id = Column(Integer, primary_key=True)
    key = Column(String(50), index=True, unique=True, nullable=False)
    value = Column(String(50), index=True, nullable=True)

    def __repr__(self):
        return '<KeyValue: id=%s, key=%s, value=%s>' % (self.id,
                                                        self.key,
                                                        self.value)


class Callback(Base):
    __tablename__ = 'callback'
    id = Column(Integer, primary_key=True)
    callback = Column(String(200), nullable=False)

    def __repr__(self):
        return '<Callback: id=%s, callback=%s>' % (self.id,
                                                   self.callback)


class KeyCallbackAssociation(Base):
    __tablename__ = 'key_callback'
    id = Column(Integer, primary_key=True)
    key_id = Column(ForeignKey('key.id'), index=True, nullable=False)
    callback_id = Column(ForeignKey('callback.id'), index=True, nullable=False)
    key = relationship('Key')
    callback = relationship('Callback')

    def __repr__(self):
        return '<KeyCallbackAssociation: id=%s, key=%s, callback=%s, ' % \
               (self.id, self.key, self.callback)
