from unittest import TestCase

from ruuvi_gateway_client import parser


class TestDataFormats(TestCase):

    def test_parse_session_cookie(self):
        header = 'x-ruuvi-interactive realm="RuuviGateway9949" challenge="ae17921390282e0495c52b6af2f365b35aebda0da2e613dfff9d6c66214856c7" session_cookie="RUUVISESSION" session_id="JYFJUDEBCDTQJOXL"'
        cookie = parser.parse_session_cookie(header)
        self.assertEqual(cookie["RUUVISESSION"], "JYFJUDEBCDTQJOXL")

    def test_parse_password(self):
        header = 'x-ruuvi-interactive realm="RuuviGateway9949" challenge="ae17921390282e0495c52b6af2f365b35aebda0da2e613dfff9d6c66214856c7" session_cookie="RUUVISESSION" session_id="JYFJUDEBCDTQJOXL"'
        username = "unit_tester"
        password = "for_unit_test"
        password_encrypted = parser.parse_password(
            header, username, password)
        self.assertEqual(
            password_encrypted, "29ea69469f7664ef7116d64108724a694fd02ce73b6464274783b238cfccb856")
