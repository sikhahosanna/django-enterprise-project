import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def call_external_api(url, timeout=5):
    retry_strategy = Retry(
        total=2,
        backoff_factor=0.5,
        status_forcelist=[502, 503, 504],
        allowed_methods=["GET"],
    )

    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return {
            "success": True,
            "data": response.json(),
            "error": None,
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "data": None,
            "error": "External service timed out.",
        }

    except requests.exceptions.RequestException:
        return {
            "success": False,
            "data": None,
            "error": "External service is temporarily unavailable.",
        }