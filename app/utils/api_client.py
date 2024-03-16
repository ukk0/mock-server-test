from random import randint
from typing import Any, Dict, Optional, Union

from requests import Response, request

API_URL = "https://restful-booker.herokuapp.com"
API_KEY = "YWRtaW46cGFzc3dvcmQxMjM="  # Hardcoded API value, not a real secret
USER_AGENT = "Automatic-API-test"


class TestAPI:
    booking_payload = {
        "firstname": "Testy",
        "lastname": "McTester",
        "totalprice": randint(100, 999),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-01-01",
            "checkout": "2024-01-19",
        },
        "additionalneeds": "Morning coffee to bed.",
    }

    @classmethod
    def _api_request(
        cls,
        url: str,
        headers: Dict[str, Any],
        method: str = "GET",
        timeout: int = 100,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[Dict[str, Any], Response]:
        url = f"{API_URL}/{url}"
        return request(
            method=method,
            url=url,
            timeout=timeout,
            headers=headers,
            json=json,
            **kwargs,
        )

    @classmethod
    def _add_headers(cls, authenticate: bool = False) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        if authenticate:
            headers.update({"Authorization": f"Basic {API_KEY}"})
        return headers

    @classmethod
    def create_booking(cls) -> Response:
        url = "booking"
        response = cls._api_request(url=url, headers=cls._add_headers(), method="POST", json=cls.booking_payload)
        return response

    @classmethod
    def get_booking_by_id(cls, booking_id: str) -> Response:
        url = f"booking/{booking_id}"
        response = cls._api_request(url=url, headers=cls._add_headers(), method="GET")
        return response

    @classmethod
    def delete_booking(cls, booking_id: str) -> Response:
        url = f"booking/{booking_id}"
        response = cls._api_request(url=url, headers=cls._add_headers(authenticate=True), method="DELETE")
        return response
