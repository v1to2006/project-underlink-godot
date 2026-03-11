import json
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError


class BackendHttp:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def get_json(self, path: str) -> dict:
        try:
            url = f"{self.base_url}{path}"

            with urllib.request.urlopen(url, timeout=5) as response:
                response_text = response.read().decode("utf-8")
                return json.loads(response_text)

        except HTTPError as error:
            print(f"[BackendHttp] HTTPError GET {path}: {error}")
        except URLError as error:
            print(f"[BackendHttp] URLError GET {path}: {error}")
        except Exception as error:
            print(f"[BackendHttp] Exception GET {path}: {error}")

        return {}

    def post_json(self, path: str, payload: dict) -> dict:
        try:
            url = f"{self.base_url}{path}"
            body = json.dumps(payload).encode("utf-8")

            request = urllib.request.Request(
                url,
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urllib.request.urlopen(request, timeout=5) as response:
                response_text = response.read().decode("utf-8")
                return json.loads(response_text)

        except HTTPError as error:
            print(f"[BackendHttp] HTTPError POST {path}: {error}")
        except URLError as error:
            print(f"[BackendHttp] URLError POST {path}: {error}")
        except Exception as error:
            print(f"[BackendHttp] Exception POST {path}: {error}")

        return {}