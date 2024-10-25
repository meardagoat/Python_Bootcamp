from __future__ import annotations

import requests
from typing import List, Union


def get_request(url: str) -> tuple[int, str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        status_code = response.status_code
        json_content = response.json()
        return status_code, json_content
    except requests.exceptions.RequestException as e:
        print(f"Error in get_request: {e}")
        return 0, str(e)


def get_countries_info(country_codes: List[str], info: List[str]) -> tuple[int, str]:
    base_url = "https://restcountries.com/v3.1/alpha"
    codes = ",".join(country_codes)
    fields = ",".join(info)
    params = {
        "codes": codes,
        "fields": fields
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        status_code = response.status_code
        json_content = response.json()
        return status_code, json_content
    except requests.exceptions.RequestException as e:
        print(f"Error in get_countries_info: {e}")
        return 0, str(e)


def handle_request_status(url: str) -> Union[int, str]:
    try:
        response = requests.post(url)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error in handle_request_status: {e}")
        return str(e)


def send_query_parameters(params: dict) -> dict:
    url = "https://httpbin.org/response-headers"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return dict(response.headers)
    except requests.exceptions.RequestException as e:
        print(f"Error in send_query_parameters: {e}")
        return {}


def send_headers(headers: dict) -> str:
    url = "https://httpbin.org/headers"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('headers', '')
    except requests.exceptions.RequestException as e:
        print(f"Error in send_headers: {e}")
        return str(e)