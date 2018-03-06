#!/usr/bin/env python
"""!
 Unit Tests for Cobinhood Api.
"""

from __future__ import print_function
from cobinhood import Cobinhood
import os
import json
import unittest

API_TOKEN_FILE = "./cobinhood/tests/api_token.json"

try:
    open(API_TOKEN_FILE).close()
    AUTH = True
except Exception:
    AUTH = False


def api_call_response(unittest, response):
    """!
    api call response function to check for success asserts.
    """
    unittest.assertTrue(response.get("result") is not None)
    unittest.assertEqual(response.get("success"), True)


class TestCobinhoodPublic(unittest.TestCase):
    """!
    Unit tests for Cobinhood public api functions.
    """

    def setUp(self):
        """!
        Initial setUp function for testcases.
        """
        self.cobinhood = Cobinhood()

    def test_get_system_time(self):
        """!
        Test the get system time function.
        """
        response = self.cobinhood.get_system_time()
        api_call_response(self, response)

    def test_get_system_info(self):
        """!
        Test the get system info function.
        """
        response = self.cobinhood.get_system_info()
        api_call_response(self, response)

    def test_get_currencies(self):
        """!
        Test the get currencies function.
        """
        response = self.cobinhood.get_currencies()
        api_call_response(self, response)

    def test_get_all_trading_pairs(self):
        """!
        Test the get all trading pairs function.
        """
        response = self.cobinhood.get_all_trading_pairs()
        api_call_response(self, response)

    def test_get_order_book(self):
        """!
        Test the get order book function.
        """
        response = self.cobinhood.get_order_book("COB-USDT")
        api_call_response(self, response)

    def test_get_trading_statistics(self):
        """!
        Test the get trading statistics function.
        """
        response = self.cobinhood.get_trading_statistics()
        api_call_response(self, response)

    def test_get_ticker(self):
        """!
        Test the get ticker function.
        """
        response = self.cobinhood.get_ticker("COB-USDT")
        api_call_response(self, response)

    def test_get_recent_trades(self):
        """!
        Test the get recent trades function.
        """
        response = self.cobinhood.get_recent_trades("COB-USDT")
        api_call_response(self, response)

    def test_get_candles(self):
        """!
        Test the get candles function.
        """
        response = self.cobinhood.get_candles("COB-USDT")
        api_call_response(self, response)


@unittest.skipUnless(AUTH, "Missing api_token.json file")
class TestCobinhoodPrivate(unittest.TestCase):
    """!
    Unit tests for Cobinhood private api functions.
    * These tests will not pass in the absence of internet connection.
    * Requires api_token.json file in the tests directory with
      valid api_key value pair structured as follows.
    {
        "api_key": "abcde123454321"
    }
    """

    def setUp(self):
        """!
        Initial setUp function for testcases.
        """
        self.api_token_file = API_TOKEN_FILE
        self.api_key = ""
        with open(self.api_token_file) as fin:
            content = json.load(fin)
            self.api_key = content.get("api_key", "")
        self.cobinhood = Cobinhood(self.api_key)
        self.order_id = ""
        self.trade_id = ""
        response = None

    def test_get_order_history(self):
        """!
        Test the fet order history function.
        """
        response = self.cobinhood.get_order_history()
        orders = response["result"]["orders"][0]
        if orders:
            self.order_id = orders.get("id", "")
        api_call_response(self, response)

    def test_get_trade_history(self):
        """!
        Test the get trade history function.
        """
        response = self.cobinhood.get_trade_history()
        trades = response["result"]["trades"][0]
        if trades:
            self.trade_id = trades.get("id", "")
        api_call_response(self, response)

    def test_get_deposit_addresses(self):
        """!
        Test the get deposit addresses function.
        """
        response = self.cobinhood.get_deposit_addresses(currency="COB")
        api_call_response(self, response)

    def test_get_withdrawal_addresses(self):
        """!
        Test the get withdrawal addresses function.
        """
        response = self.cobinhood.get_withdrawal_addresses(currency="COB")
        api_call_response(self, response)

    #@unittest.skipIf(self.order_id, "Order id unavailable")
    def test_get_order(self):
        """!
        Test the get order function.
        """
        #response = self.cobinhood.get_order(self.order_id)
        #api_call_response(self, response)

    #@unittest.skipIf(self.order_id, "Order id unavailable")
    def test_get_single_order(self):
        """!
        Test the get trades of an order function.
        """
        #response = self.cobinhood.get_trades_order(self.order_id)
        #api_call_response(self, response)

    def test_get_all_orders(self):
        """!
        Test the get all current orders function.
        """
        response = self.cobinhood.get_all_orders()
        api_call_response(self, response)

    #@unittest.skipIf(self.trade_id, "Trade id unavailable")
    def test_get_trade(self):
        """!
        Test the get trade function.
        """
        #response = self.cobinhood.get_trade(self.trade_id)
        #api_call_response(self, response)
    
    def test_get_wallet_balances(self):
        """!
        Test the get wallet balances function.
        """
        response = self.cobinhood.get_wallet_balances()
        api_call_response(self, response)

    def test_get_ledger_entries(self):
        """!
        Test the get ledger entries function.
        """
        response = self.cobinhood.get_ledger_entries(currency="COB")
        api_call_response(self, response)

    def test_get_withdrawal(self):
        """!
        Test the get withdrawal function.
        """
        #response = self.cobinhood.get_withdrawal()
        #api_call_response(self, response)

    def test_get_all_withdrawals(self):
        """!
        Test the get all withdrawals function.
        """
        response = self.cobinhood.get_all_withdrawals()
        api_call_response(self, response)

    def test_get_deposit(self):
        """!
        Test the get deposit function.
        """
        #response = self.cobinhood.get_deposit()
        #api_call_response(self, response)

    def test_get_all_deposits(self):
        """!
        Test the get all deposits function.
        """
        response = self.cobinhood.get_all_deposits()
        api_call_response(self, response)

if __name__ == "__main__":
    unittest.main()

