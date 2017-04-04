import urllib2
from multiprocessing import Process, Queue
from time import sleep

import flask_restful as restful
from db_con.sa import get_session
from flask.ext.restful import reqparse
from metadata import metadata_models as mm
from metadata import serializers


class KeyValueList(restful.Resource):
    @staticmethod
    def call_url(new_url, result_queue):
        response = urllib2.urlopen(new_url)
        html = response.read()
        result_queue.put(html)
        return html

    @staticmethod
    def get_key(session, key):
        q = session.query
        key = q(mm.Key).filter_by(key=key).scalar()
        return key

    @staticmethod
    def get_callback(session, url):
        q = session.query
        callback = q(mm.Callback).filter_by(callback=url).scalar()
        return callback

    @staticmethod
    def get_key_callbacks(session, key):
        q = session.query
        callbacks = q(mm.KeyCallbackAssociation).filter_by(key=key).all()
        result = [(i.callback.callback, "".join(["callback_", str(index)])) for index, i in
                  enumerate(callbacks)]
        return result

    def create_key_value(self, session, key_name, value):
        key = self.get_key(session, key_name)
        if not key:
            key = mm.Key()
            key.key = key_name
            key.value = value
            session.add(key)
        else:
            callbacks = self.get_key_callbacks(session, key)
            killed_processes_num = 0
            result_queue = Queue()
            processes = [Process(target=self.call_url,
                                 args=("{}?key={}".format(u[0], value),
                                       result_queue)) for u in callbacks]
            processes_num = len(processes)
            # Run processes
            for p in processes:
                p.start()

            # Exit/terminate completed processes after 5 seconds
            for p in processes:
                p.join(5)
                if p.is_alive():
                    p.terminate()
                    killed_processes_num += 1

            # Get process results from the output queue
            results = [result_queue.get() for p in range(processes_num - killed_processes_num)]
            if all([i.rstrip() == 'true' for i in results]) and not killed_processes_num:
                key.value = value
                session.add(key)
        return key

    def create_url(self, session, callback_url):
        callback = self.get_callback(session, callback_url)
        if not callback:
            callback = mm.Callback()
            callback.callback = callback_url
            session.add(callback)
        return callback

    @staticmethod
    def associate_key_url(session, key, callback):
        association = mm.KeyCallbackAssociation()
        association.key = key
        association.callback = callback
        session.add(association)

    def create_key_value_url(self, session, key_name, value, callback_url):
        key = self.create_key_value(session, key_name, value)
        if callback_url:
            callback = self.create_url(session, callback_url)
            self.associate_key_url(session, key, callback)
        session.commit()

    def get(self, key):
        session = get_session('metadata')
        parser = reqparse.RequestParser()
        args = parser.parse_args(strict=True)
        if key.endswith("/callback"):
            key = key.split("/callback")[0]
            key = self.get_key(session, key)
            return self.get_key_callbacks(session, key)
        else:
            key = self.get_key(session, key)
            return None if not key else serializers.KeyValueSerializer([key], many=True).data

    def post(self, key):
        session = get_session('metadata')
        parser = reqparse.RequestParser()
        parser.add_argument('value', type=str, required=True)
        parser.add_argument('url', type=str, required=False)
        args = parser.parse_args(strict=True)
        value = args['value']
        if key.endswith("/callback"):
            key = key.split("/callback")[0]
            callback_url = args['url']
        else:
            callback_url = None
        self.create_key_value_url(session, key, value, callback_url)


class OnlyDigitsFast(restful.Resource):
    """
    They are three examples for callback fast, medium and slow in response
    """
    def __init__(self):
        self.delay = 1

    @staticmethod
    def delay_only_digits(key, delay):
        sleep(delay)
        try:
            int(key)
            return True
        except ValueError:
            return False

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('key', type=str, required=True)
        args = parser.parse_args(strict=True)
        key = args['key']
        return self.delay_only_digits(key, self.delay)


class OnlyDigitsMedium(OnlyDigitsFast):
    def __init__(self):
        super(OnlyDigitsFast, self).__init__()
        self.delay = 3


class OnlyDigitsSlow(OnlyDigitsFast):
    def __init__(self):
        super(OnlyDigitsFast, self).__init__()
        self.delay = 6
