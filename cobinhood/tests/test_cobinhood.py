#!/usr/bin/env python
"""!
 Unit Tests for Cobinhood Api.
"""

import unittest
from cobinhood.cobinhood import Cobinhood

class TestCobinhood(unittest.TestCase):
    """!
    Unit tests for Cobinhood Api functions.
    """
    def setUp(self):
        """!
        Initial setUp function for testcases.
        """
        self.cobinhood = Cobinhood()
        self.response = None

    def api_call_success_asserts(self):
        """!
        Test if the api call was successful.
        """
        self.assertTrue(self.response.get('result') is not None)
        self.assertEqual(self.response.get('success'), True)

    def test_get_system_time(self):
        """!
        Test the get system time function.
        """
        self.response = Cobinhood().get_system_time()
        self.api_call_success_asserts()

    def test_get_system_info(self):
        """!
        Test the get system info function.
        """
        self.response = Cobinhood().get_system_info()
        self.api_call_success_asserts()

    def test_get_currencies(self):
        """!
        Test the get currencies function.
        """
        self.response = Cobinhood().get_currencies()
        self.api_call_success_asserts()

    def test_get_trading_pairs(self):
        """!
        Test the get trading pairs function.
        """
        self.response = Cobinhood().get_trading_pairs()
        self.api_call_success_asserts()

    def test_get_order_book(self):
        """!
        Test the get order book function.
        """
        self.response = Cobinhood().get_order_book("COB-USDT")
        self.api_call_success_asserts()

    def test_get_trading_statistics(self):
        """!
        Test the get trading statistics function.
        """
        self.response = Cobinhood().get_trading_statistics()
        self.api_call_success_asserts()

    def test_get_ticker(self):
        """!
        Test the get ticker function.
        """
        self.response = Cobinhood().get_ticker("COB-USDT")
        self.api_call_success_asserts()

    def test_get_recent_trades(self):
        """!
        Test the get recent trades function.
        """
        self.response = Cobinhood().get_recent_trades("COB-USDT")
        self.api_call_success_asserts()

    def test_get_candles(self):
        """!
        Test the get candles function.
        """
        self.response = Cobinhood().get_candles("COB-USDT")
        self.api_call_success_asserts()

if __name__ == '__main__':
    unittest.main()
