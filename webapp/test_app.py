import os
import logging
import numpy as np

from flask import Flask
from cat import Sheet, q, compose_answer

import pytest
from injector import Injector, Module, provider, singleton, get_bindings, inject
from flask_injector import FlaskInjector
from flask_assistant import Assistant, ask

from app import init, AppModule

import json

def build_payload(
    intent, params={}, contexts=[], action="test_action", query="test query"
):

    return json.dumps(
        {
            "originalDetectIntentRequest": {
                "source": "google",
                "version": "2",
                "data": {
                    "isInSandbox": False,
                    "surface": {
                        "capabilities": [
                            {"name": "actions.capability.AUDIO_OUTPUT"},
                            {"name": "actions.capability.SCREEN_OUTPUT"},
                            {"name": "actions.capability.MEDIA_RESPONSE_AUDIO"},
                            {"name": "actions.capability.WEB_BROWSER"},
                        ]
                    },
                    "inputs": [{}],
                    "user": {
                        "lastSeen": "2018-04-23T15:10:43Z",
                        "locale": "en-US",
                        "userId": "abcdefg",
                        "accessToken": "foobar",
                    },
                    "conversation": {
                        "conversationId": "123456789",
                        "type": "ACTIVE",
                        "conversationToken": "[]",
                    },
                    "availableSurfaces": [
                        {
                            "capabilities": [
                                {"name": "actions.capability.AUDIO_OUTPUT"},
                                {"name": "actions.capability.SCREEN_OUTPUT"},
                            ]
                        }
                    ],
                },
            },
            "responseId": "8ea2d357-10c0-40d1-b1dc-e109cd714f67",
            "queryResult": {
                "action": action,
                "allRequiredParamsCollected": True,
                "outputContexts": contexts,
                "languageCode": "en",
                "fulfillment": {"messages": [], "text": ""},
                "intent": {
                    "name": "some-intent-id",
                    "displayName": intent,
                    # "webhookForSlotFillingUsed": "false",
                    "webhookState": True,
                },
                "parameters": params,
                "resolvedQuery": query,
                "intentDetectionConfidence": 1.0,
            },
            "session": "projects/test-project-id/agent/sessions/88d13aa8-2999-4f71-b233-39cbf3a824a0",
        }
    )


def get_query_response(client, payload):
    resp = client.post("/wh/", data=payload)
    assert resp.status_code == 200
    return json.loads(resp.data.decode("utf-8"))

class AppModuleTest(Module):
    @provider
    @singleton
    def provide_sheet(self) -> Sheet:
        return np.array([ 
                ['101','film'],
                ['102','CaSe'],
                ['103','film 2'],
                ['104','film 3'],
                ['105','El señor de los anillos'],
                ['106','El señor Smith'],
            ])


@pytest.fixture
def client():
    app = init(module = AppModuleTest())
    with app.test_client() as client:
        yield client

def test_root(client):
    rv = client.get('/')
    assert b'Hi!' in rv.data

def test_q_with_a_no_film(client):
    rv = client.get('/test/q/nofilm')
    assert b'No he encontrado la peli' in rv.data

def test_q_with_a_film(client):
    rv = client.get('/test/q/case')
    assert b'La peli CaSe' in rv.data

def test_q_with_a_2_words_film(client):
    rv = client.get('/test/q/señor anillos')
    assert b'La peli El se' in rv.data

def test_module_for_injector():
    module = AppModule()
    injector = Injector([module])
    sh = injector.get(Sheet)
    assert type(sh) is Sheet


def test_intent_test(client):
    payload = build_payload("Testear")
    resp = get_query_response(client, payload)
    assert "Yes you can!" in resp["fulfillmentText"]

def test_intent_search(client):
    payload = build_payload("Buscar Peli",params={"any": "case"})
    resp = get_query_response(client, payload)
    assert 'La peli CaSe' in resp["fulfillmentText"]

