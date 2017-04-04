from argparse import ArgumentParser

from flask import Flask
from flask_restful import Api
from metadata.metadata_api import KeyValueList, OnlyDigitsFast, OnlyDigitsMedium, OnlyDigitsSlow


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(KeyValueList, '/<path:key>')
    api.add_resource(OnlyDigitsFast, '/valuechecker/only_digits_fast')
    api.add_resource(OnlyDigitsMedium, '/valuechecker/only_digits_medium')
    api.add_resource(OnlyDigitsSlow, '/valuechecker/only_digits_slow')
    return app


def options():
    parser = ArgumentParser()
    parser.add_argument('--debug', action="store_true", default=False)
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=9000)
    return parser.parse_args()


def main():
    """Launch API server
    """
    opts = options()
    app = create_app()
    app.run(debug=opts.debug, port=opts.port, host=opts.host)


if __name__ == '__main__':
    main()
