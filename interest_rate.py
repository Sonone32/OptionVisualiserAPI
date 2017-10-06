from sanic import response
from sanic.exceptions import ServerError
from sanic import Blueprint

interest_rate = Blueprint('interest_rate')

@interest_rate.route('/interest-rate')
async def rate_grabber(request):
    storedRate = await request.app.redis.get('interest-rate')
    if storedRate:
        # Found interest rate in redis store, return it.
        return response.json({'rate': float(storedRate)})
    else:
        # Interest rate expired, scrape it from the URL
        url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'
        async with request.app.httpClient.get(url) as result:
            if result.status == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(await result.text(encoding='utf-8'), 'html.parser')
                table = soup.select('table.t-chart > tr')
                row = table[len(table) - 1]
                rate = row.select('td')[4].text
                # Put it in redis here
                await request.app.redis.setex('interest-rate', 3600 * 24, rate)
                return response.json({'rate': float(rate)})
            else:
                raise ServerError('Unable to fetch data', 400)
