"""!
@file       cobinhood.py

@brief      Python wrapper for accessing cobinhood api.
@author     Sachin Jayaram
@date       2/2018
@document   https://cobinhood.github.io/api-public/
"""

from __future__ import print_function
import requests

try:
    from urllib import urlencode
except ImportError:
    from urllib import urlencode

API_V1 = 'v1'

BASE_URL_V1 = 'https://api.cobinhood.com/{version}/{fn_call}?'


def request_api_call(request_url):
    """!
    Make a request url call to get the respective response from cobinhood servers.

    @param request_url: the generated url for making the api call.
    @param signapi: signed api.
    """
    return requests.get(request_url).json()


class Cobinhood(object):
    """!
    Cobinhood class definition to request information from Cobinhood exchange using api key.
    """

    def __init__(self, perform=request_api_call, api_version=API_V1):
        """!
        Cobinhood class initialization.

        @param perform function call to call request_api_call.
        @param api_version: default api_version set to v1
        """
        self.perform = perform
        self.api_version = api_version

    def _query_api(self, fn_dict, extension=None):
        """!
        Function to query the cobinhood exchange.

        @param fn_dict: dict with api_version and function name.
        @return: json response from the cobinhood exchange.
        """
        if not fn_dict or self.api_version not in fn_dict:
            raise ExceptionCobinhood('incorrect method call')

        base_url = BASE_URL_V1
        request_url = base_url.format(version=self.api_version, fn_call=fn_dict[self.api_version])

        if extension:
            request_url += urlencode(extension)

        try:
            return self.perform(request_url)
        except:
            raise ExceptionCobinhood(
                str({
                    u'success': False,
                    u'error': {
                        u'error_code': u'resource_not_found'
                    }
                }))

    def get_system_time(self):
        """!
        Get the system time as Unix timestamp.

        V1 path-extension: /v1/system/time [GET].

        Example:
        {
            'success': true,
            'result': {
                'time': 1520288666216
            }
        }

        @return: System time as Unix timestamp in json format.
        """
        return self._query_api(
            fn_dict={API_V1: 'system/time'})

    def get_system_info(self):
        """!
        Get the system information.

        V1 path-extension: /v1/system/info [GET].

        Example:
        {
            'success': true,
            'result': {
            'info': {
                'phase': 'production',
                'revision': 'e21f66'
                }
            }
        }

        @return: System information in json format.
        """
        return self._query_api(
            fn_dict={API_V1: 'system/info'})

    def get_currencies(self):
        """!
        Get info of all currencies available for trading.

        V1 path-extension: /v1/market/currencies [GET].

        Example:
        {
            'success': true,
            'result': {
                'currencies': [
                    {
                        'currency': 'BTC',
                        'name': 'Bitcoin',
                        'min_unit': '0.00000011',
                        'deposit_fee': '0',
                        'withdrawal_fee': '11.9'
                        'type': 'native',
                        'is_active': true,
                        'funding_frozen': false
                    },

                ]
            }
        }

        @return: info of all currencies available for trading.
        """
        return self._query_api(
            fn_dict={API_V1: 'market/currencies'})

    def get_trading_pairs(self):
        """!
        Get info for all trading pairs available.

        V1 path-extension: /v1/market/trading_pairs [GET].

        Example:
        {
            'success': true,
            'result': {
                'trading_pairs': [
                    {
                        'id': 'BTC-USD',
                        'base_currency_id': 'BTC',
                        'quote_currency_id': 'USD',
                        'base_min_size': '0.005',
                        'base_max_size': '10001',
                        'quote_increment': '0.1'
                    },
                    ...
                ]
            }
        }

        @return: info for all trading pairs available.
        """
        return self._query_api(
            fn_dict={API_V1: 'market/trading_pairs'})

    def get_order_book(self, trading_pair_id):
        """!
        Get order book for the trading pair containing all asks/bids.

        V1 path-extension: /v1/market/trading_pair_id [GET].

        Example:
        {
            'success': true,
            'result': {
                'orderbook': {
                    'sequence': 1939573,
                    'bids': [
                        [ price, count, size ],
                        ...
                    ],
                    'asks': [
                        [ price, count, size ],
                        ...
                    ]
                }
            }
        }

        @param trading_pair_id: string literal - Ex: 'BTC-USDT'
        @return: order book for the trading pair containing all asks/bids.
        """
        return self._query_api(
            fn_dict={API_V1: 'market/orderbooks/{0}'.format(trading_pair_id)})

    def get_trading_statistics(self):
        """!
        Get trading statistics.

        V1 path-extension: /v1/market/stats [GET].

        {
            'success': true,
            'result': {
                'BTC-USDT': {
                    'id': 'BTC-USDT',
                    'last_price': '10006',
                    'lowest_ask': '10006',
                    'highest_bid': '15201.1',
                    'base_volume': '0.36255777',
                    'quote_volume': '4198.431917147',
                    'is_frozen': false,
                    'high_24hr': '15999.9',
                    'low_24hr': '10001',
                    'percent_changed_24hr': '-0.3417806461799594'
                }
            }
        }

        @return: trading statistics.
        """
        return self._query_api(
            fn_dict={API_V1: 'market/stats'})

    def get_ticker(self, trading_pair_id):
        """!
        Get the ticker for specified trading pair.

        V1 path-extension: /v1/market/tickers/<trading_pair_id> [GET].

        {
            "success": true,
            "result": {
                "ticker": {
                    "trading_pair_id": "COB-BTC",
                    "timestamp": 1504459806123,
                    "24h_high": "23.4567",
                    "24h_low": "10.1234",
                    "24h_open": "15.7645",
                    "24h_volume": "7842.11542553",
                    "last_trade_price":"244.89",
                    "highest_bid":"244.76",
                    "lowest_ask":"244.77"
                }
            }
        }

        @return: ticker for specified trading pair.
        """
        return self._query_api(
            fn_dict={API_V1: 'market/tickers/{0}'.format(trading_pair_id)})

    def get_recent_trades(self, trading_pair_id):
        """!
        Get the most recent trades for the specific trading pairs.

        V1 path-extension: /v1/market/<trading_pair_id> [GET].

        {
            'success': true,
            'result': {
                'trades': [
                    {
                        'id': '09619448e48a3bd73d493a4195f9020c',
                        'price': '11.00000000',
                        'size': '0.02000000',
                        'maker_side': 'buy',
                        'timestamp': 1504459806124
                    },
                    ...
                ]
            }
        }

        @return: most recent trades for the specific trading pairs.
        """
        return self._query_api(
            fn_dict={API_V1: 'market/trades/{0}'.format(trading_pair_id)})

    def get_candles(self, trading_pair_id):
        """!
        Get charting candles.

        V1 path-extension: /v1/chart/candlers/<trading_pair_id> [GET].

        {
            'success': true,
            'result': {
                'candles': [
                    {
                        'timestamp': 1507366755,
                        'open': '4378.5',
                        'close': '4359.0',
                        'high': '4359.0',
                        'low': '4358.3',
                        'volume': '23.91465172'
                    },
                    ...
                ]
            }
        }

        @return: charting candles.
        """
        return self._query_api(
            fn_dict={API_V1: 'chart/candles/{0}'.format(trading_pair_id)})


class ExceptionCobinhood(Exception):
    """!
    Cobinhood api error exceptions.
    """

    def __init__(self, cause):
        """!
        class Initializer.
        """
        super(ExceptionCobinhood, self).__init__()
        self.cause = cause

    def __str__(self):
        """!
        return the cause of cobinhood exception as a string.

        @return: cause of the exception as a string.
        """
        return str(self.cause)
