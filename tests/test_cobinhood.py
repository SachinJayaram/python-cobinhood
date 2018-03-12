#!/usr/bin/env python
"""!
 Unit Tests for Cobinhood Api.
"""

from __future__ import print_function
import json
import mock
import unittest
import cobinhood

API_TOKEN_FILE = "./tests/api_token.json"

try:
    open(API_TOKEN_FILE).close()
    AUTH = True
except IOError:
    AUTH = False


def api_call_response(unit_test, response, is_success=True):
    """!
    api call response function to check for success asserts.
    """
    if is_success:
        unit_test.assertTrue(response.get("result") is not None)
    unit_test.assertEqual(response.get("success"), is_success)


class TestCobinhoodPublic(unittest.TestCase):
    """!
    Unit tests for Cobinhood public api functions.
    """

    def setUp(self):
        """!
        Initial setUp function for testcases.
        """
        self.cobinhood = cobinhood.Cobinhood()

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

    # pylint: disable=I0011, W0212
    def test_query_api(self):
        """!
        Test the query api function.
        Empty fn_dict exception and incorrect url exception.
        """
        fn_dict = {}
        with self.assertRaises(cobinhood.ExceptionCobinhood) as cob_exception:
            self.cobinhood._query_api(fn_dict)
            cob_exception.assert_called_with("incorrect method call")
        fn_dict = {cobinhood.API_V1: "system/times"}
        with self.assertRaises(cobinhood.ExceptionCobinhood) as cob_exception:
            self.cobinhood._query_api(fn_dict)
            cob_exception.assert_called_with("Error: request_url is incorrect")

    @mock.patch("time.time", return_value=12345)
    def test_request_api_call(self, mock_time):
        """!
        Test the request api call function.
        """
        self.assertEqual(mock_time.return_value, 12345)
        header = {"Authorization": "", "nonce": str(mock_time.return_value*1000)}

        with mock.patch("requests.get") as request_get:
            cobinhood.request_api_call("v1/system/time", "", "get")
            request_get.assert_called_with("v1/system/time", headers=header)
        with mock.patch("requests.put") as request_put:
            cobinhood.request_api_call("v1/system/time", "", "put")
            request_put.assert_called_with("v1/system/time", headers=header)
        with mock.patch("requests.post") as request_post:
            cobinhood.request_api_call("v1/system/time", "", "post")
            request_post.assert_called_with("v1/system/time", headers=header)
        with mock.patch("requests.delete") as request_delete:
            cobinhood.request_api_call("v1/system/time", "", "delete")
            request_delete.assert_called_with("v1/system/time", headers=header)
        with self.assertRaises(cobinhood.ExceptionCobinhood) as cob_exception:
            cobinhood.request_api_call("v1/system/time", "", "abcd")
            cob_exception.assert_called_with("Error: invalid request type")

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
        self.cobinhood = cobinhood.Cobinhood(self.api_key)

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

    def test_get_ledger_entries(self):
        """!
        Test the get ledger entries function.
        """
        response = self.cobinhood.get_ledger_entries(currency="COB")
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

    def test_get_withdrawal(self):
        """!
        Test the get withdrawal function.
        """
        withdrawal_response_all = self.cobinhood.get_all_withdrawals()
        withdrawal = withdrawal_response_all["result"].get("withdrawals", "")
        withdrawal_id = withdrawal[0].get("withdrawal_id") if withdrawal else ""
        withdrawal_response = self.cobinhood.get_withdrawal(withdrawal_id)
        api_call_response(self, withdrawal_response)
        if not withdrawal_id:
            self.assertEqual(withdrawal_response_all["result"].get("withdrawals"),
                             withdrawal_response["result"].get("withdrawals"))

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
        deposit_response_all = self.cobinhood.get_all_deposits()
        deposit = deposit_response_all["result"].get("deposits", "")
        deposit_id = deposit[0].get("deposit_id") if deposit else ""
        deposit_response = self.cobinhood.get_deposit(deposit_id)
        api_call_response(self, deposit_response)
        if not deposit_id:
            self.assertEqual(deposit_response_all["result"].get("deposits"),
                             deposit_response["result"].get("deposits"))

    def test_get_all_deposits(self):
        """!
        Test the get all deposits function.
        """
        response = self.cobinhood.get_all_deposits()
        api_call_response(self, response)


class TestExceptionCobinhood(unittest.TestCase):
    """!
    Unittest test for ExceptionCobinhood class.
    """

    def setUp(self):
        """!
        Initial setUp function for testcases.
        """
        self.cause = "Error: invalid request type"
        self.exception = cobinhood.ExceptionCobinhood(self.cause)

    def test_str(self):
        """!
        Initial setUp function for testcases.
        """
        self.assertEqual(self.exception.__str__(), self.cause)

if __name__ == "__main__":
    unittest.main()

