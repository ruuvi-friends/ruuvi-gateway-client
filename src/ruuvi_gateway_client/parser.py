
import hashlib
from typing import Dict


def _parse_value_from_header(header: str, key: str) -> str:
    ch_start = header.index(key) + len(key) + 2
    ch_end = header.index("\"", ch_start + 1)
    return header[ch_start:ch_end]


def parse_password(header: str, username: str, password: str) -> str:
    challenge = _parse_value_from_header(header, "challenge")
    realm = _parse_value_from_header(header, "realm")
    password_md5 = hashlib.md5(
        f'{username}:{realm}:{password}'.encode()).hexdigest()
    password_sha256 = hashlib.sha256(
        f'{challenge}:{password_md5}'.encode()).hexdigest()
    return password_sha256


def parse_session_cookie(header: str) -> Dict[str, str]:
    session_cookie = _parse_value_from_header(header, "session_cookie")
    session_id = _parse_value_from_header(header, "session_id")
    return {session_cookie: session_id}
