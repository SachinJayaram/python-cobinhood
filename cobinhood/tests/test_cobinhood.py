#!/usr/bin/env python
"""!
 Unit Tests for Cobinhood Api.
"""

from __future__ import print_function
from cobinhood import Cobinhood
<<<<<<< HEAD
=======
import os
>>>>>>> 651628c74b34173df01670a49b8e09fc6757c189
import json
import unittest

API_TOKEN_FILE = "./cobinhood/tests/api_token.json"

try:
    open(API_TOKEN_FILE).close()
    AUTH = True
<<<<<<< HEAD
except IOError:
    AUTH = False


def api_call_response(unit_test, response, is_success=True):
    """!
    api call response function to check for success asserts.
    """
    if is_success:
        unit_test.assertTrue(response.get("result") is not None)
    unit_test.assertEqual(response.get("success"), is_success)


=======
except Exception:
    AUTH = False


def api_call_response(unittest, response):
    """!
    api call response function to check for success asserts.
    """
    unittest.assertTrue(response.get("result") is not None)
    unittest.assertEqual(response.get("success"), True)


>>>>>>> 651628c74b34173df01670a49b8e09fc6757c189
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
<<<<<<< HEAD

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

    def test_get_order(self):
        """!
        Test the get order function.
        """
        order_history = self.cobinhood.get_order_history().get("result")
        order_id = order_history["orders"][0].get("id", "") if order_history else ""
        response = self.cobinhood.get_order(order_id)
        api_call_response(self, response)
        if not order_id:
            self.assertEqual(order_history.get("orders"),
                             response["result"].get("orders"))

    def test_get_trades_order(self):
        """!
        Test the get order function.
        """
        order_history = self.cobinhood.get_order_history().get("result")
        order_id = order_history["orders"][0].get("ids", "") if order_history else ""
        response = self.cobinhood.get_trades_order(order_id)
        if order_id:
            api_call_response(self, response)
        else:
            api_call_response(self, response, is_success=False)

    def test_get_all_orders(self):
        """!
        Test the get all current orders function.
        """
        response = self.cobinhood.get_all_orders()
        api_call_response(self, response)

    def test_get_order_history(self):
        """!
        Test the fet order history function.
        """
        response = self.cobinhood.get_order_history()
        api_call_response(self, response)

    def test_get_trade(self):
        """!
        Test the get trade function.
        """
        trade_history = self.cobinhood.get_trade_history().get("result")
        trade_id = trade_history["trades"][0].get("id") if trade_history else ""
        response = self.cobinhood.get_trade(trade_id)
        if not trade_id:
            self.assertEqual(trade_history.get("trades"),
                             response["result"].get("trades"))

    def test_get_trade_history(self):
        """!
        Test the get trade history function.
        """
        response = self.cobinhood.get_trade_history()
        api_call_response(self, response)

    def test_get_wallet_balances(self):
        """!
        Test the get wallet balances function.
        """
        response = self.cobinhood.get_wallet_balances()
        api_call_response(self, response)

=======

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

>>>>>>> 651628c74b34173df01670a49b8e09fc6757c189
    def test_get_ledger_entries(self):
        """!
        Test the get ledger entries function.
        """
        response = self.cobinhood.get_ledger_entries(currency="COB")
        api_call_response(self, response)

<<<<<<< HEAD
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

=======
>>>>>>> 651628c74b34173df01670a49b8e09fc6757c189
    def test_get_withdrawal(self):
        """!
        Test the get withdrawal function.
        """
<<<<<<< HEAD
        withdrawal_response_all = self.cobinhood.get_all_withdrawals()
        withdrawal = withdrawal_response_all["result"].get("withdrawals", "")
        withdrawal_id = withdrawal[0].get("withdrawal_id") if withdrawal else ""
        withdrawal_response = self.cobinhood.get_withdrawal(withdrawal_id)
        api_call_response(self, withdrawal_response)
        if not withdrawal_id:
            self.assertEqual(withdrawal_response_all["result"].get("withdrawals"),
                             withdrawal_response["result"].get("withdrawals"))
=======
        #response = self.cobinhood.get_withdrawal()
        #api_call_response(self, response)
>>>>>>> 651628c74b34173df01670a49b8e09fc6757c189

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
<<<<<<< HEAD
        deposit_response_all = self.cobinhood.get_all_deposits()
        deposit = deposit_response_all["result"].get("deposits", "")
        deposit_id = deposit[0].get("deposit_id") if deposit else ""
        deposit_response = self.cobinhood.get_deposit(deposit_id)
        api_call_response(self, deposit_response)
        if not deposit_id:
            self.assertEqual(deposit_response_all["result"].get("deposits"),
                             deposit_response["result"].get("deposits"))
=======
        #response = self.cobinhood.get_deposit()
        #api_call_response(self, response)
>>>>>>> 651628c74b34173df01670a49b8e09fc6757c189

    def test_get_all_deposits(self):
        """!
        Test the get all deposits function.
        """
        response = self.cobinhood.get_all_deposits()
        api_call_response(self, response)

if __name__ == "__main__":
    unittest.main()

