import requests
import json


TIMEOUT = 180


class Client:
    def __init__(self, api_key: str, api_endpoint: str, timeout: int = TIMEOUT) -> None:
        self.timeout = timeout

        assert api_key, "api_key cannot be empty."
        assert api_endpoint, "api_endpoint cannot be empty."

        self.api_key = api_key
        self.api_endpoint = api_endpoint

    def request(self, path: str, method: str = "GET", params=None, **kwargs):
        try:
            response = requests.request(
                method=method,
                url=self.api_endpoint + path,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                timeout=self.timeout,
                data=json.dumps(params),
                **kwargs,
            )

            result = response.json()
            if "errors" in result:
                raise BrazeException(str(result["errors"]))
            return result

        except requests.RequestException as e:
            raise BrazeException(e)

    """ User Data Endpoints """

    def create_new_user_alias(self, params):
        return self.request("/users/alias/new", "POST", params)

    def delete_users(self, params):
        return self.request("/users/delete", "POST", params)

    def identify_users(self, params):
        return self.request("/users/identify", "POST", params)

    def track_users(self, params):
        return self.request("/users/track", "POST", params)

    def merge_users(self, params):
        return self.request("/users/merge", "POST", params)

    def rename_external_ids(self, params):
        return self.request("/users/external_ids/rename", "POST", params)

    def remove_external_ids(self, params):
        return self.request("/users/external_ids/rename", "POST", params)

    """ Export: User Data Endpoints """

    def export_users_by_ids(self, params):
        return self.request("/users/export/ids", "POST", params)

    """ Messaging: Send Messages Endpoints """

    def send_campaign_trigger(self, params):
        return self.request("/campaigns/trigger/send", "POST", params)

    def send_canvas_trigger(self, params):
        return self.request("/canvas/trigger/send", "POST", params)


class BrazeException(Exception):
    def __init__(self, result):
        self.result = result
        self.code = None
        self.message = None

        try:
            self.type = result.get("message")
            self.message = result.get("errors")
        except:
            self.type = ""
            self.message = result

        Exception.__init__(self, self.message)
