import logging
import unittest
from test import BaseTestCase

class TestStocks(BaseTestCase):
    def test_get_stock(self):
        request_body = {
            "session": {
                "new": True,
                "sessionId": "amzn1.echo-api.session.5f3ec23d-5933-4620-b00b-b2e262b65182",
                "user": {
                    "userId": "amzn1.account.AHSMN72XJPRTGNUUYRUDD7EINGYQ"
                }
            },
            "version": "1.0",
            "request": {
                "intent": {
                    "slots": {
                        "Stock": {
                            "name": "Stock",
                            "value": "google"
                        }
                    },
                    "name": "price"
                },
                "type": "IntentRequest",
                "requestId": "amzn1.echo-api.request.953912c8-69d5-46ef-96e5-45bd662b845a"
            }
        }

        response = self.app.post_json('/', request_body)
        self.assertEqual(response.status, "200 OK")
        self.assertNotEqual(response.json_body, None)
        self.assertNotEqual(response.json_body["response"]["outputSpeech"]["text"], "")

