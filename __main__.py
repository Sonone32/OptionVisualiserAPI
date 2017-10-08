from aiohttp import ClientSession
from aioredis import create_redis
from interest_rate import interest_rate
from sanic import Sanic
from sanic_cors import CORS
from yahoo_finance_chain import yahoo_finance
from sanic.config import LOGGING as L

# LOGGING can be found in https://github.com/channelcat/sanic/blob/master/sanic/log.py
A = {'class': 'logging.handlers.RotatingFileHandler',
        'filters': ['accessFilter'],
        'formatter': 'access',
        'filename': 'access.log',
        'maxBytes': 1024 * 1024 * 10,
        'backupCount': 5,
        }


E = {'class': 'logging.handlers.RotatingFileHandler',
        'filters': ['errorFilter'],
        'formatter': 'simple',
        'filename': 'error.log',
        'maxBytes': 1024 * 1024 * 10,
        'backupCount': 5,
        }

L['handlers']['accessStream'] = A
L['handlers']['errorStream'] = E

app = Sanic(__name__)
CORS(app)

app.blueprint(interest_rate)
app.blueprint(yahoo_finance)

@app.listener('before_server_start')
async def setup_server(app, loop):
    app.httpClient = ClientSession(loop=loop)
    app.redis = await create_redis(('localhost', 6379), loop=loop)

@app.listener('after_server_stop')
async def tear_down_server(app, loop):
    app.httpClient.close()
    app.redis.close()
    print('Server shutdown')

app.run(host="0.0.0.0", port=8000, debug=False, log_config=L)
