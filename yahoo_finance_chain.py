from sanic import response
from sanic import Blueprint
from sanic.exceptions import ServerError
import ujson

yahoo_finance = Blueprint('yahoo_finance')

@yahoo_finance.route('/ychain')
async def ychain(request):
    # Symbol is a required parameter
    try:
        symbol = request.args['symbol'][0]
    except KeyError:
        raise ServerError('Missing ticker symbol in parameter',
                          status_code=400)
    # Expiration date is optional
    try:
        date = request.args['expiration'][0]
    except KeyError:
        date = False

    storedChain = await request.app.redis.get('{}:{}'.format(symbol, date if date else 0))
    if storedChain:
        # aioredis stores strings as bytes, so just return it raw.
        return response.raw(storedChain)
    else:
        url = 'https://query1.finance.yahoo.com/v7/finance/options/{}'.format(symbol)
        if date:
            url += '?date={}'.format(date)

        async with request.app.httpClient.get(url) as res:
            content = await res.json()
            save = ujson.dumps(content)
            if res.status == 200:
                await request.app.redis.setex('{}:{}'.format(symbol, date), 900, save)
                if not date:
                    # For the lack of a better way to access cache without expiry
                    await request.app.redis.setex('{}:0'.format(symbol), 900, save)
                return response.json(content)
            else:
                raise ServerError('Invalid Query', status_code=404)
