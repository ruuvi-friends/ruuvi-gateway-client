from typing import Dict, Tuple
from aiohttp.client import ClientSession
import aiohttp
from result import Ok, Err, Result
from ruuvi_decoders import get_decoder

from ruuvi_gateway_client.types import SensorData, SensorPayload, ParsedDatas, Payload
from ruuvi_gateway_client.parser import parse_session_cookie, parse_password


def _parse_sensor_payload(mac: str, payload: SensorPayload) -> Tuple[str, SensorData]:
    raw = payload["data"]

    try:
        companyIndex = raw.index("FF9904")
    except ValueError:
        print("Ruuvi company id not found in data")
        return [mac, None]

    rt: SensorData = {}
    rt["rssi"] = payload["rssi"]

    try:
        broadcast_data = raw[companyIndex+6:]
        data_format = broadcast_data[0:2]
        rt = get_decoder(int(data_format)).decode_data(broadcast_data)
    except ValueError:
        print("Valid data format data not found in payload")
        return [mac, None]

    return [mac, rt]


def _parse_received_data(payload: Payload) -> ParsedDatas:
    data = payload["data"]
    sensor_datas = [_parse_sensor_payload(key, value)
                    for key, value in data["tags"].items()]
    return dict(sensor_datas)


async def get_auth_info(session: ClientSession, ip: str, cookies: Dict[str, str] = {}) -> Result[str, None]:
    async with session.get(f'http://{ip}/auth', cookies=cookies) as response:
        if response.status == 401:
            auth_info = response.headers["WWW-Authenticate"]
            return Ok(auth_info)
        return Err()


async def authorize_user(session: ClientSession, ip: str, cookies, username: str, password_encrypted: str) -> Result[int, int]:
    auth_payload = '{"login":"' + username + \
        '","password":"' + password_encrypted + '"}'
    async with session.post(f'http://{ip}/auth', data=auth_payload, cookies=cookies) as response:
        return Ok(response.status) if response.status == 200 else Err(response.status)


async def get_data(session: ClientSession, ip: str, cookies: Dict[str, str] = {}) -> Result[ParsedDatas, int]:
    try:
        async with session.get(f'http://{ip}/history?time=5', cookies=cookies) as response:
            if response.status == 200:
                data = await response.json()
                parsed = _parse_received_data(data)
                return Ok(parsed)
            else:
                return Err(response.status)
    except aiohttp.ClientConnectionError as e:
        message = e.args[0]
        if hasattr(message, 'code') and message.code == 302:
            return Err(302)
        return Err(500)


async def get_authenticate_cookies(session: ClientSession, ip: str, username: str, password: str) -> Result[Dict[str, str], str]:
    auth_info_result = await get_auth_info(session, ip)
    if not auth_info_result.is_ok():
        return Err()
    cookies = parse_session_cookie(auth_info_result.value)
    password_encrypted = parse_password(
        auth_info_result.value, username, password)
    auth_result = await authorize_user(session, ip, cookies, username, password_encrypted)
    if not auth_result.is_ok():
        return Err(auth_result.value)
    return Ok(cookies)


async def fetch_data(ip: str, username: str, password: str) -> Result[ParsedDatas, str]:
    async with aiohttp.ClientSession() as session:
        get_result = await get_data(session, ip)
        if get_result.is_ok():
            return Ok(get_result.value)
        if get_result.value != 302:
            return Err(f'Fetch failed - {get_result.value}')

        cookie_result = await get_authenticate_cookies(session, ip, username, password)
        if not cookie_result.is_ok():
            return Err(f'Authentication failed - {cookie_result.value}')

        get_result = await get_data(session, ip, cookie_result.value)
        if get_result.is_ok():
            return Ok(get_result.value)
        else:
            return Err(f'Fetch failed after authentication - {get_result.value}')
