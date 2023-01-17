from pytest import raises
from dotenv import load_dotenv
from os import getenv

from braze import Client as BrazeClient, BrazeException

load_dotenv()

client = BrazeClient(
    api_key=getenv("API_KEY"),
    api_endpoint=getenv("API_ENDPOINT"),
)


def test_track_users():
    response = client.track_users(
        {
            "attributes": [
                {
                    "external_id": "b63bef41-5ebf-4c32-9166-e0b0d3bc2853",
                    "email": "akshit@whoppah.com",
                }
            ]
        }
    )
    assert response.get("attributes_processed") == 1
    assert response.get("message") == "success"


def test_track_users_with_invalid_email():
    with raises(BrazeException):
        client.track_users(
            {
                "attributes": [
                    {
                        "external_id": "b63bef41-5ebf-4c32-9166-e0b0d3bc2853",
                        "email": "akshit @whoppah.com",
                    }
                ]
            }
        )
