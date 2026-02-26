import sys, os
import pytest

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root not in sys.path:
    sys.path.insert(0, root)

import manager
import paho.mqtt.client as mqtt


def test_client_init():
    client = manager.client_init("test")
    assert isinstance(client, mqtt.Client)
    # callbacks should be set
    assert client.on_connect == manager.on_connect
    assert client.on_message == manager.on_message


def test_on_message_inserts(monkeypatch, tmp_path):
    # simulate insert_DB by patching it
    calls = {}
    def fake_insert(topic, m_decode):
        calls['topic'] = topic
        calls['m_decode'] = m_decode
    monkeypatch.setattr(manager, 'insert_DB', fake_insert)
    # create fake msg
    class Msg:
        topic = 'pr/Smart/device'
        payload = b'Test payload'
    manager.on_message(None, None, Msg())
    assert calls['topic'] == 'pr/Smart/device'
    assert 'Test payload' in calls['m_decode']
