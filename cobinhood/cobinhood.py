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

API_V1 = "v1"

BASE_URL_V1 = "https://api.cobinhood.com/{version}/{fn_call}?"


def request_api_call(request_url, auth_token):
    """!
    Make a request url call to get the respective response from cobinhood servers.

    @param request_url: the generated url for making the api call.
    @param signapi: signed api.
    """
    return requests.get(
        request_url,
        headers={"Authorization": auth_token}).json()


class Cobinhood(object):
    """!
    Cobinhood class definition to request information from Cobinhood exchange using api key.
    """

    def __init__(self, api_key=None, perform=request_api_call, api_version=API_V1):
        """!
        Cobinhood class initialization.

        @param perform function call to call request_api_call.
        @param api_version: default api_version set to v1
        """
        self.api_key = str(api_key) if api_key else ""
        self.perform = perform
        self.api_version = api_version

    def _query_api(self, fn_dict, extension=None):
        """!
        Function to query the cobinhood exchange.

        @param fn_dict: dict with api_version and function name.
        @return: json response from the cobinhood exchange.
        """
        if not fn_dict or self.api_version not in fn_dict:
            raise ExceptionCobinhood("incorrect method call")

        base_url = BASE_URL_V1
        request_url = base_url.format(version=self.api_version,
                                      fn_call=fn_dict[self.api_version])

        if extension:
            request_url += urlencode(extension)

        try:
            return self.perform(request_url, self.api_key)
        except:
            raise ExceptionCobinhood(
                str({
                    u"success": False,
                    u"error": {
                        u"error_code": u"resource_not_found"
                    }
                }))

    def get_system_time(self):
        """!
        Get the system time as Unix timestamp.

        V1 path-extension: /v1/system/time [GET].

        Example:
        {
            "success": true,
            "result": {
                "time": 1520288666216
            }
        }

        @return: system time as Unix timestamp in json format.
        """
        return self._query_api(
            fn_dict={API_V1: "system/time"})

    def get_system_info(self):
        """!
        Get the system information.

        V1 path-extension: /v1/system/info [GET].

        Example:
        {
            "success": true,
            "result": {
            "info": {
                "phase": "production",
                "revision": "e21f66"
                }
            }
        }

        @return: system information in json format.
        """
        return self._query_api(
            fn_dict={API_V1: "system/info"})

    def get_currencies(self):
        """!
        Get info of all currencies available for trading.

        V1 path-extension: /v1/market/currencies [GET].

        Example:
        {
            "success": true,
            "result": {
                "currencies": [
                    {
                        "currency": "BTC",
                        "name": "Bitcoin",
                        "min_unit": "0.00000011",
                        "deposit_fee": "0",
                        "withdrawal_fee": "11.9"
                        "type": "native",
                        "is_active": true,
                        "funding_frozen": false
                    },

                ]
            }
        }

        @return: info of all currencies available for trading.
        """
        return self._query_api(
            fn_dict={API_V1: "market/currencies"})

    def get_all_trading_pairs(self):
        """!
        Get info for all trading pairs available.

        V1 path-extension: /v1/market/trading_pairs [GET].

        Example:
        {
            "success": true,
            "result": {
                "trading_pairs": [
                    {
                        "id": "BTC-USD",
                        "base_currency_id": "BTC",
                        "quote_currency_id": "USD",
                        "base_min_size": "0.005",
                        "base_max_size": "10001",
                        "quote_increment": "0.1"
                    },
                    ...
                ]
            }
        }

        @return: info for all trading pairs available.
        """
        return self._query_api(
            fn_dict={API_V1: "market/trading_pairs"})

    def get_order_book(self, trading_pair_id, limit=50):
        """!
        Get order book for the trading pair containing all asks/bids.

        V1 path-extension: /v1/market/orderbooks/trading_pair_id [GET].

        Example:
        {
            "success": true,
            "result": {
                "orderbook": {
                    "sequence": 1939573,
                    "bids": [
                        [ price, count, size ],
                        ...
                    ],
                    "asks": [
                        [ price, count, size ],
                        ...
                    ]
                }
            }
        }

        @param trading_pair_id: string literal - Ex: "BTC-USDT"
        @param limit: limits number of entries of asks/bids list,
            beginning from the best price for both sides.
        @return: order book for the trading pair containing all asks/bids.
        """
        return self._query_api(
            fn_dict={API_V1: "market/orderbooks/{0}".format(trading_pair_id)},
            extension={"limit": limit})

    def get_trading_statistics(self):
        """!
        Get trading statistics.

        V1 path-extension: /v1/market/stats [GET].

        {
            "success": true,
            "result": {
                "BTC-USDT": {
                    "id": "BTC-USDT",
                    "last_price": "10006",
                    "lowest_ask": "10006",
                    "highest_bid": "15201.1",
                    "base_volume": "0.36255777",
                    "quote_volume": "4198.431917147",
                    "is_frozen": false,
                    "high_24hr": "15999.9",
                    "low_24hr": "10001",
                    "percent_changed_24hr": "-0.3417806461799594"
                }
            }
        }

        @return: trading statistics.
        """
        return self._query_api(
            fn_dict={API_V1: "market/stats"})

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

        @param trading_pair_id: string literal - Ex: "BTC-USDT"
        @return: ticker for specified trading pair.
        """
        return self._query_api(
            fn_dict={API_V1: "market/tickers/{0}".format(trading_pair_id)})

    def get_recent_trades(self, trading_pair_id, limit=20):
        """!
        Get the most recent trades for the specific trading pairs.

        V1 path-extension: /v1/market/<trading_pair_id> [GET].

        {
            "success": true,
            "result": {
                "trades": [
                    {
                        "id": "09619448e48a3bd73d493a4195f9020c",
                        "price": "11.00000000",
                        "size": "0.02000000",
                        "maker_side": "buy",
                        "timestamp": 1504459806124
                    },
                    ...
                ]
            }
        }

        @param trading_pair_id: string literal - Ex: "BTC-USDT"
        @param limit: limits number of trades beginning from the most recent.
        @return: most recent trades for the specific trading pairs.
        """
        return self._query_api(
            fn_dict={API_V1: "market/trades/{0}".format(trading_pair_id)},
            extension={"limit": limit})

    def get_candles(self, trading_pair_id):
        """!
        Get charting candles.

        V1 path-extension: /v1/chart/candles/<trading_pair_id> [GET].

        {
            "success": true,
            "result": {
                "candles": [
                    {
                        "timestamp": 1507366755,
                        "open": "4378.5",
                        "close": "4359.0",
                        "high": "4359.0",
                        "low": "4358.3",
                        "volume": "23.91465172"
                    },
                    ...
                ]
            }
        }

        @param trading_pair_id: string literal - Ex: "BTC-USDT"
        @return: charting candles.
        """
        return self._query_api(
            fn_dict={API_V1: "chart/candles/{0}".format(trading_pair_id)})

    def get_order(self, order_id):
        """!
        Get information for a single order.

        V1 path-extension: /v1/trading/orders/<order_id> [GET].

        {
            "success": true,
            "result": {
                "order": {
                    "id": "37f550a202aa6a3fe120f420637c895c",
                    "trading_pair": "BTC-USDT",
                    "state": "open",
                    "side": "bid",
                    "type": "limit",
                    "price": "5000.00",
                    "size": "1.0101",
                    "filled": "0.69",
                    "timestamp": 1604459805123
                }
            }
        }

        @param order_id: id of the order.
        @return: information for a single order.
        """
        return self._query_api(
            fn_dict={API_V1: "trading/orders/{0}".format(order_id)})

    def get_trades_order(self, order_id):
        """!
        Get all trades originating from the specific order.

        V1 path-extension: /v1/trading/orders/<order_id>/trades [GET].

        {
            "success": true,
            "result": {
                "trades": [
                    {
                        "id": "09619448e48a3bd73d493a4194f9020b",
                        "price": "10.00000000",
                        "size": "0.01000000",
                        "maker_side": "bid",
                        "timestamp": 1504459805123
                    },
                    ...
                ]
            }
        }

        @param order_id: id of the order.
        @return: trades originating from the specific order.
        """
        return self._query_api(
            fn_dict={API_V1: "trading/orders/{0}/trades".format(order_id)})

    def get_all_orders(self, limit=20):
        """!
        Get all current orders for user.

        V1 path-extension: /v1/trading/orders [GET].

        {
            "success": true,
            "result": {
                "orders": [
                    {
                        "id": "37f550a202aa6a3fe120f420637c894d",
                        "trading_pair": "BTC-USDT",
                        "state": "open",
                        "side": "bid",
                        "type": "limit",
                        "price": "5000.09",
                        "size": "1.0101",
                        "filled": "0.69",
                        "timestamp": 2504459805123,
                        "eq_price": "5000.09"
                    },
                    ...
                ]
            }
        }

        @param limit: limits number of orders per page.
        @return: all current orders for user.
        """
        return self._query_api(
            fn_dict={API_V1: "trading/orders"},
            extension={"limit": limit})

    def place_order(self):
        """!
        Place orders to ask or bid.

        V1 path-extension: /v1/trading/orders [POST].

        Payload:
        {
            "trading_pair_id": "BTC-USDT",
            "side": "bid",
            "type": "limit",
            "price": "5000.11000001",
            "size": "1.0101"
        }

        Response:
        {
            "success": true,
            "result": {
                "order": {
                    "id": "37f550a202aa6a3fe120f420637c894d",
                    "trading_pair": "BTC-USDT",
                    "state": "open",
                    "side": "bid",
                    "type": "limit",
                    "price": "5000.09",
                    "size": "1.0101",
                    "filled": "0.69",
                    "timestamp": 2504459805123,
                    "eq_price": "5000.09"
                }
            }
        }

        @return: response after the order is placed.
        """
        return self._query_api(
            fn_dict={API_V1: "trading/orders"})

    def modify_order(self, order_id):
        """!
        Modify a single order.

        V1 path-extension: /v1/trading/orders/<order_id> [PUT].

        {
            "success": true
        }

        @param order_id: id of the order.
        @return: Response after modifying an order.
        """
        return self._query_api(
            fn_dict={API_V1: "trading/orders/{0}".format(order_id)})

    def cancel_order(self, order_id):
        """!
        Cancel a single order.

        V1 path-extension: /v1/trading/orders/<order_id> [DELETE].

        {
            "success": true
        }

        @param order_id: id of the order.
        @return: Response after cancelling an order.
        """
        return self._query_api(
            fn_dict={API_V1: "trading/orders/{0}".format(order_id)})

    def get_order_history(self, limit=50):
        """!
        Get order history for the current user.

        V1 path-extension: /v1/trading/order_history [GET].

        {
            "success": true,
            "result": {
                "order_history": [
                    {
                        "id": "37f550a202aa6a3fe120f420637c894d",
                        "trading_pair": "BTC-USDT",
                        "state": "filled",
                        "side": "bid",
                        "type": "limit",
                        "price": "5000.09",
                        "size": "1.0101",
                        "filled": "0.69",
                        "timestamp": 2504459805123,
                        "eq_price": "5000.09"
                    }
                    ...
                ]
            }
        }

        @param limit: limits number of orders per page.
        @return: Order history for the current user.
        """
        return self._query_api(
            fn_dict={API_V1: "trading/order_history"},
            extension={"limit": limit})

    def get_trade(self, trade_id):
        """!
        Get trade information. A user only can get their own trade.

        V1 path-extension: /v1/trading/trades/<trade_id> [GET].

        {
            "success": true,
            "result": {
                "trade": {
                    "trading_pair_id": "BTC-USDT",
                    "id": "09619448-e48a-3bd7-3d49-3a4194f9020c",
                    "maker_side": "bid",
                    "price": "10.00000001",
                    "size": "0.01000001",
                    "timestamp": 1504459805124
                }
            }
        }

        @param trade_id: trading id.
        @return: trade information of self.
        """
        return self._query_api(
            fn_dict={API_V1: "trading/trades/{0}".format(trade_id)})

    def get_trade_history(self):
        """!
        Get trade history for the current user.

        V1 path-extension: /v1/trading/trades [GET].

        {
            "success": true,
            "result": {
                "trades": [
                    {
                        "trading_pair_id": "BTC-USDT",
                        "id": "09619448e48a3bd73d493a4194f9020c",
                        "maker_side": "ask",
                        "price": "10.00000001",
                        "size": "0.01000001",
                        "timestamp": 1504459805124
                    },
                    ...
                ]
            }
        }

        @return: trade history for the current user.
        """
        return self._query_api(
            fn_dict={API_V1: "trading/trades"})

    def get_wallet_balances(self):
        """!
        Get balances of the current user.

        V1 path-extension: /v1/wallet/balances [GET].

        {
            "success": true,
            "result": {
                "balances": [
                    {
                        "currency": "BTC",
                        "type": "exchange",
                        "total": "1",
                        "on_order": "0.5",
                        "locked": false,
                        "usd_value": "10000.1",
                        "btc_value": "1.1"
                    },
                    {
                        "currency": "ETH",
                        "type": "exchange",
                        "total": "0.0855175219863033",
                        "on_order": "0.05",
                        "locked": false,
                        "usd_value": "10000.1",
                        "btc_value": "0.009"
                    },
                    {
                        "currency": "COB",
                        "type":" exchange",
                        "total": "100",
                        "on_order": "20",
                        "locked": false,
                        "usd_value": "1000.1",
                        "btc_value": "0.11"
                    },
                    ...
                ]
            }
        }

        @return: balances of the current user.
        """
        return self._query_api(
            fn_dict={API_V1: "wallet/balances"})

    def get_ledger_entries(self, currency="", limit=20):
        """!
        Get balance history for the current user.

        V1 path-extension: /v1/wallet/ledger [GET]

        {
            "success": true,
            "result": {
                "ledger": [
                    {
                        "action": "trade",
                        "type": "exchange",
                        "trade_id": "09619448e48a3bd73d493a4194f9020c",
                        "currency": "BTC",
                        "amount": "+635.78",
                        "balance": "2930.34",
                        "timestamp": 1504685599303
                    },
                    {
                        "action": "deposit",
                        "type": "exchange",
                        "deposit_id": "09619448e48a3bd73d493a4194f9020c",
                        "currency": "BTC",
                        "amount": "+635.78",
                        "balance": "2930.34",
                        "timestamp": 1504685599303
                    },
                    {
                        "action": "withdraw",
                        "type": "exchange",
                        "withdrawal_id": "09619448e48a3bd73d493a4194f9020c",
                        "currency": "BTC",
                        "amount": "-121.02",
                        "balance": "2194.88",
                        "timestamp": 1504685599303
                    },
                    ...
                ]
            }
        }

        @param currency: currency id.
        @param limit: Limits number of balances per page.
        @return balance history for the current user.
        """
        return self._query_api(
            fn_dict={API_V1: "wallet/balances"},
            extension={"currency": currency, "limit": limit})

    def get_deposit_addresses(self, currency=""):
        """!
        Get Wallet Deposit Addresses.

        V1 path-extension: /v1/wallet/deposit_addresses [GET]

        {
            "success": true,
            "result": {
                "deposit_addresses": [
                    {
                        "currency": "BTC",
                        "address": "0xbcd7defe48a19f758a1c1a9706e809072391bc20",
                        "created_at": 1504459804123,
                        "type": "exchange"
                    },
                    ...
                ]
            }
        }

        @param currency: currency id.
        @return Wallet Deposit Addresses.
        """
        return self._query_api(
            fn_dict={API_V1: "wallet/deposit_addresses"},
            extension={"currency": currency})

    def get_withdrawal_addresses(self, currency=""):
        """!
        Get Wallet Withdrawal Addresses.

        V1 path-extension: /v1/wallet/withdrawal_addresses [GET]

        {
            "success": true,
            "result": {
                "withdrawal_addresses": [
                    {
                        "id": "09619448e48a3bd73d493a4194f9020c",
                        "currency": "BTC",
                        "name": "BTC Name",
                        "type": "exchange",
                        "address": "0xbcd7defe48a19f758a1c1a9706e808072391bc21",
                        "created_at": 1504459804123
                    },
                    ...
                ]
            }
        }

        @param currency: currency id.
        @return Wallet Withdrawal Addresses.
        """
        return self._query_api(
            fn_dict={API_V1: "wallet/withdrawal_addresses"},
            extension={"currency": currency})

    def get_withdrawal(self, withdrawal_id):
        """!
        Get Withdrawal Information.

        V1 path-extension: /v1/wallet/withdrawals/<withdrawal_id> [GET]

        {
            "success": true,
            "result": {
                "withdrawal": {
                    "withdrawal_id": "62056df2d4cf8fb9b15c7238b89a1439",
                    "user_id": "62056df2d4cf8fb9b15c7238b89a1439",
                    "status": "pending",
                    "confirmations": 29,
                    "required_confirmations": 29,
                    "created_at": 1504459805129,
                    "sent_at": 1504459805129,
                    "completed_at": 1504459914239,
                    "updated_at": 1504459914239,
                    "to_address": "0xbcd7defe48a19f758a1c1a9706e808072391bc29",
                    "txhash": "0xf6ca576fb446893432d55ec53e93b7dcfbbf75b548570b2eb8b1853de7aa7239",
                    "currency": "BTC",
                    "amount": "0.029",
                    "fee": "0.00033"
                }
            }
        }

        @param withdrawal_id: Withdrawal ID.
        @return Wallet Withdrawal Information.
        """
        return self._query_api(
            fn_dict={API_V1: "wallet/withdrawals/{0}".format(withdrawal_id)})

    def get_all_withdrawals(self):
        """!
        Get All Withdrawals.

        V1 path-extension: /v1/wallet/withdrawals [GET]

        {
            "success": true,
            "result": {
                "withdrawal": {
                    "withdrawal_id": "62056df2d4cf8fb9b15c7238b89a1439",
                    "user_id": "62056df2d4cf8fb9b15c7238b89a1439",
                    "status": "pending",
                    "confirmations": 29,
                    "required_confirmations": 29,
                    "created_at": 1504459805129,
                    "sent_at": 1504459805129,
                    "completed_at": 1504459914239,
                    "updated_at": 1504459914239,
                    "to_address": "0xbcd7defe48a19f758a1c1a9706e808072391bc29",
                    "txhash": "0xf6ca576fb446893432d55ec53e93b7dcfbbf75b548570b2eb8b1853de7aa7239",
                    "currency": "BTC",
                    "amount": "0.029",
                    "fee": "0.00033"
                }
            }
        }

        @return All Withdrawal.
        """
        return self._query_api(
            fn_dict={API_V1: "wallet/withdrawals"})

    def get_deposit(self, deposit_id):
        """!
        Get Deposit Information.

        V1 path-extension: /v1/wallet/deposits/<deposit_id> [GET]

        {
            "success": true,
            "result": {
                "deposit": {
                    "deposit_id": "62056df2d4cf8fb9b15c7238b89a1439",
                    "user_id": "62056df2d4cf8fb9b15c7238b89a1439",
                    "status": "pending",
                    "confirmations": 29,
                    "required_confirmations": 29,
                    "created_at": 1504459805129,
                    "completed_at": 1504459914239,
                    "from_address": "0xbcd7defe48a19f758a1c1a9706e808072391bc29",
                    "txhash": "0xf6ca576fb446893432d55ec53e93b7dcfbbf75b548570b2eb8b1853de7aa7239",
                    "currency": "BTC",
                    "amount": "0.029",
                    "fee": "0.0009"
                }
            }
        }

        @param deposit_id: Deposit ID.
        @return Wallet Deposit Information.
        """
        return self._query_api(
            fn_dict={API_V1: "wallet/deposits/{0}".format(deposit_id)})

    def get_all_deposits(self):
        """!
        Get All Deposits.

        V1 path-extension: /v1/wallet/deposits [GET]

        {
            "success": true,
            "result": {
                "deposits": [
                    {
                        "deposit_id": "62056df2d4cf8fb9b15c7238b89a1439",
                        "user_id": "62056df2d4cf8fb9b15c7238b89a1439",
                        "status": "pending",
                        "confirmations": 29,
                        "required_confirmations": 29,
                        "created_at": 1504459805129,
                        "completed_at": 1504459914239,
                        "from_address": "0xbcd7defe48a19f758a1c1a9706e808072391bc29",
                        "txhash": "0xf6ca576fb446893432d55ec53e93b7dcfbbf75b548570b2eb8b1853de7aa",
                        "currency": "BTC",
                        "amount": "0.029",
                        "fee": "0.0009"
                    },
                    ...
                ]
            }
        }

        @return All Deposit.
        """
        return self._query_api(
            fn_dict={API_V1: "wallet/deposits"})


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
