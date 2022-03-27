# Ruuvi Gateway Client

Work in progress.

## Install

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

STATION_IP = "10.0.0.21"
USERNAME = "username"
PASSWORD = "password"


def print_data(data: ParsedDatas):
    for mac, sensor_data in data.items():
        print(f'{mac}: {sensor_data}')


async def main():
    fetch_result = await gateway.fetch_data(STATION_IP, USERNAME, PASSWORD)
    if fetch_result.is_ok():
        print_data(fetch_result.value)
    else:
        print(f'Fetch failed: {fetch_result.value}')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Execute tests

```sh
python setup.py test
```
