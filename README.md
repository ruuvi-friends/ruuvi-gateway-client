# Ruuvi Gateway Client

[![PyPI](https://img.shields.io/pypi/v/ruuvi_gateway_client.svg)](https://pypi.python.org/pypi/ruuvi_gateway_client)

Client for communicating with Ruuvi Gateway.

## Install

Install latest released version
```sh
$ python -m pip install ruuvi-gateway-client
```

Install letest development version from local sources
```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Example

```py
import asyncio
from ruuvi_gateway_client import gateway
from ruuvi_gateway_client.types import ParsedDatas

STATION_ADDR = "ruuvigateway9c2c.local"  # or IP address like 10.0.0.21
# Set either USERNAME and PASSWORD, or TOKEN (or none for access without authentication).
# Here is docs how to configure access settings from LAN using username/password or token:
# https://docs.ruuvi.com/ruuvi-gateway-firmware/gateway-html-pages/access-settings-from-lan
# Here is example how to configure polling mode using token access:
# https://docs.ruuvi.com/ruuvi-gateway-firmware/examples/polling-mode
USERNAME = "username"
PASSWORD = "password"
TOKEN = "bXRhN6p8bhedOSRayTlfOo7PAxMobAy9H9vRHtbjMww="


def print_data(data: ParsedDatas):
    for mac, sensor_data in data.items():
        print(f'{mac}: {sensor_data}')


async def main():
    print(f'Fetching data from Ruuvi Gateway "{STATION_ADDR}" without authentication')
    fetch_result = await gateway.fetch_data(STATION_ADDR)
    if fetch_result.is_ok():
        print_data(fetch_result.ok_value)
    else:
        print(f'Fetch without authentication failed: {fetch_result.err_value}')

    if USERNAME is not None and PASSWORD is not None: 
        print(f'\nFetching data from Ruuvi Gateway "{STATION_ADDR}" with username/password authentication')
        fetch_result = await gateway.fetch_data(STATION_ADDR, USERNAME, PASSWORD)
        if fetch_result.is_ok():
            print_data(fetch_result.ok_value)
        else:
            print(f'Fetch with username/password failed: {fetch_result.err_value}')

    if TOKEN is not None:
        print(f'\nFetching data from Ruuvi Gateway "{STATION_ADDR}" with token authentication')
        fetch_result = await gateway.fetch_data(STATION_ADDR, token=TOKEN)
        if fetch_result.is_ok():
            print_data(fetch_result.ok_value)
        else:
            print(f'Fetch with token failed: {fetch_result.err_value}')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Changelog

[Changelog](https://github.com/ruuvi-friends/ruuvi-gateway-client/blob/main/CHANGELOG.md)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Licensed under the [MIT](https://github.com/ruuvi-friends/ruuvi-gateway-client/blob/main/LICENSE) License.
