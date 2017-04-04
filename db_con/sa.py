#!/usr/bin/env python
"""SQL Alchemy util"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_session_makers = {}
conf = {'metadata': 'mysql+pymysql://root:password@localhost:3306'}


def create_session_maker(uri, db_name, auto_flush=True):
    full_uri = '{}/{}?charset=utf8'.format(uri, db_name)
    engine = create_engine(full_uri, pool_recycle=300)
    return sessionmaker(bind=engine, autoflush=auto_flush)


def _init_session_makers():
    global _session_makers
    global conf
    for db_name, uri in conf.iteritems():
        for auto_flush in True, False:
            session_maker = create_session_maker(uri, db_name, auto_flush)
            _session_makers[(db_name, auto_flush)] = (uri, session_maker)


def get_session(db_name, auto_flush=True):
    if not _session_makers:
        _init_session_makers()

    session = _session_makers[(db_name, auto_flush)][1]()
    return session
