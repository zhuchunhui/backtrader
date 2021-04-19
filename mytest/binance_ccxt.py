import ccxt
import time

binance_exchange = ccxt.binance({
    'countries': ['CN'],
    'timeout': 15000,
    'enableRateLimit': True,
    'apiKey': "9M5drzI3MN4UmHwA1CNU5OBxV0kzkuD7cvm1nCeuzGmqP5NXv6B5PRlLZlo7xIYk",
    'secret': "CuhJcXIeUQHvmFGiVQ7fM8b6807A4L3GlriLk01VwxHPhpKARR3AKzfikaikPjAV",
    # 'proxies': {
    #     'http': 'http://106.53.38.69:3128',
    #     'https': 'https://106.53.38.69:3128',
    # },
    'urls': {
        'logo': 'https://user-images.githubusercontent.com/1294454/29604020-d5483cdc-87ee-11e7-94c7-d1a8d9169293.jpg',
        'test': {
            'dapiPublic': 'https://testnet.binancefuture.com/dapi/v1',
            'dapiPrivate': 'https://testnet.binancefuture.com/dapi/v1',
            'fapiPublic': 'https://testnet.binancefuture.com/fapi/v1',
            'fapiPrivate': 'https://testnet.binancefuture.com/fapi/v1',
            'fapiPrivateV2': 'https://testnet.binancefuture.com/fapi/v2',
            'public': 'https://testnet.binance.vision/api/v3',
            'private': 'https://testnet.binance.vision/api/v3',
            'v3': 'https://testnet.binance.vision/api/v3',
            'v1': 'https://testnet.binance.vision/api/v1',
        },
        'api': {
            'wapi': 'https://api.binance.com/wapi/v3',
            'sapi': 'https://api.binancezh.co/sapi/v1',
            'dapiPublic': 'https://dapi.binance.com/dapi/v1',
            'dapiPrivate': 'https://dapi.binance.com/dapi/v1',
            'dapiData': 'https://dapi.binance.com/futures/data',
            'fapiPublic': 'https://fapi.binance.com/fapi/v1',
            'fapiPrivate': 'https://fapi.binance.com/fapi/v1',
            'fapiData': 'https://fapi.binance.com/futures/data',
            'fapiPrivateV2': 'https://fapi.binance.com/fapi/v2',
            'public': 'https://api.binancezh.co/api/v3',
            'private': 'https://api.binancezh.co/api/v3',
            'v3': 'https://api.binancezh.co/api/v3',
            'v1': 'https://api.binancezh.co/api/v1',
        },
        'www': 'https://www.binance.com',
        'referral': 'https://www.binance.com/?ref=10205187',
        'doc': [
            'https://binance-docs.github.io/apidocs/spot/en',
        ],
        'api_management': 'https://www.binance.com/en/usercenter/settings/api-management',
        'fees': 'https://www.binance.com/en/fee/schedule',
    },
})

#载入市场清单
# markets = binance_exchange.load_markets()
# print(markets)

# print(binance_exchange.fetch_tickers(['BTC/USDT', 'ETH/USDT']))

# binance_exchange.apiKey="9M5drzI3MN4UmHwA1CNU5OBxV0kzkuD7cvm1nCeuzGmqP5NXv6B5PRlLZlo7xIYk"
# binance_exchange.secret="CuhJcXIeUQHvmFGiVQ7fM8b6807A4L3GlriLk01VwxHPhpKARR3AKzfikaikPjAV"

timestamp = binance_exchange.publicGetTime()
print(timestamp)

stamp=time.mktime(time.strptime('2021-04-01 00:00:00', '%Y-%m-%d %H:%M:%S'))

transferList = binance_exchange.sapiGetFuturesTransfer({
    'timestamp':timestamp['serverTime'],
    'asset':'USDT',
    'startTime':int(stamp),
    # 'type':1
    })

for transfer in transferList['rows']:
    if transfer['type'] == '2': #划转方向: 1( 现货向USDT本位合约), 2( USDT本位合约向现货), 3( 现货向币本位合约), and 4( 币本位合约向现货)
        timeArray = time.localtime(int(transfer['timestamp'][:-3]))
        print(time.strftime("%Y-%m-%d %H:%M:%S", timeArray),">>>>",transfer)
