from flask_redis import FlaskRedis
from flask import Flask
from flask_restful import Resource, Api
from datetime import datetime


def create_app(config_pyfile):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile(config_pyfile)

    redis_store = FlaskRedis(app, strict=False)
    api = Api(app)

    class Pairs(Resource):
        def get(self):
            return sorted(list(set(map(lambda x: x.split(':')[0], redis_store.keys()))))

    class OnePair(Resource):
        def get(self, pair):
            keys = redis_store.keys('%s*' % pair)
            exchanges = []
            min_ = None
            max_ = None
            for k in keys:
                d = redis_store.hgetall(k)
                if 'trades_date_time' not in d:
                    continue
                ts = datetime.strptime(d['trades_date_time'], '%Y%m%d %H:%M:%S.%f')
                if (datetime.utcnow() - ts).total_seconds() >= 600:
                    # exclude if older than 10 minutes
                    continue
                price = float(d['trade_px'])
                if min_ is None or price < min_:
                    min_ = price
                if max_ is None or price > max_:
                    max_ = price
                exchanges.append(d)
            return {
                'min': min_,
                'max': max_,
                'exchanges': exchanges
            }

    api.add_resource(Pairs, '/pairs')
    api.add_resource(OnePair, '/pairs/<pair>')

    return app
