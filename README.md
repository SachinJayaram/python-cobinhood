# python-cobinhood
[![Build Status](https://travis-ci.org/SachinJayaram/python-cobinhood.svg?branch=master)

Python wrapper for Cobinhood. Use at your own risk. I'm not responsible for any issues.

## How to RUN Cobinhood API

```
import cobinhood

if __name__ == '__main__':
    cob_api = Cobinhood()
    result = cob_api.get_system_time()
    print(result)
```

## Testing:

To run the integration tests execute the following command:
```
"python -m unittest discover"
```

## Error Codes:

```
4000: undefined_error. Unknown error.
4001: undefined_action. Request action is not defined.
4002: cannel_not_found. Cound't found a channel according the request.
4003: subscribe_failed. Failed to subscribe a channel for specified request.
4004: unsubsribe_failed. Failed to unsubscribe a channel for specified request.
4005: invalid_payload. request is not avliable.
4006: not_authenticated. Calling a authorization required chanel, but request without authorization.
4007: invalid_snapshot. Failed to get a snapshot.
4008: place_order_failed. Failed to place a order.
4009: cancel_order_failed. Failed to cancel a order.
4010: modify_order_failed. Failed to modify a order.
```
