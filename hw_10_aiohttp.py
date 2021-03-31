from aiohttp import web
import aiohttp
import async_timeout

api_dict = {
        'Crypto': {
            'url': 'https://api.coingecko.com/api/v3/coins/markets',
            'params': {'vs_currency': 'usd', 'order': 'market_cap_desc', 'ids': 'bitcoin'},
            'headers': {'accept': 'application/json'}
        },
        'Geo': {
            'url': 'https://freegeoip.app/json/',
            'headers': {
                'accept': "application/json",
                'content-type': "application/json"}
        },
        'Joke': {
            'url': 'https://icanhazdadjoke.com/',
            'headers': {'accept': 'application/json'}
        }
}


async def fetch_single_url(session, url_key):
    url = api_dict[url_key]['url']
    headers = api_dict[url_key]['headers'] if api_dict.get(url_key).get('headers') else None
    params = api_dict[url_key]['params'] if api_dict.get(url_key).get('params') else None

    async with async_timeout.timeout(10):
        async with session.get(url=url, headers=headers, params=params) as response:
            return await response.json()


async def main():
    res_dict = {}
    for api in api_dict.keys():
        async with aiohttp.ClientSession() as session:
            response = await fetch_single_url(session, api)
            res_dict[api] = response
    return res_dict


async def get_specific_info(response):
    crypto_keys = ['name', 'current_price']
    crypto = [dict(response['Crypto'][0]).get(key) for key in crypto_keys]
    joke = response['Joke']['joke']
    ip_keys = ['ip', 'country_name', 'city', 'latitude', 'longitude']
    ip = [response['Geo'].get(key) for key in ip_keys]
    return crypto, ip, joke

routes = web.RouteTableDef()


@routes.get('/collect_info')
async def handle(request):
    response = await main()
    crypto, ip, joke = await get_specific_info(response)
    return web.Response(
        text=f'{crypto[0]} price is {crypto[1]} USD\n\nJoke of the day: {joke}\n\nIP info: {str(ip)[1:-1]}')


app = web.Application()
app.add_routes([web.get('/collect_info', handle)])
web.run_app(app)
