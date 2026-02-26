import sys, os
import pytest

# ensure project root is importable
top = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if top not in sys.path:
    sys.path.insert(0, top)

from mqtt_agent import Mqtt_client, MQTT_CLIENT_INIT


def test_mqtt_client_init_callable():
    # constructor compatibility function should be callable
    assert callable(MQTT_CLIENT_INIT)
    client = MQTT_CLIENT_INIT("testid")
    # basic attributes exist
    assert hasattr(client, "on_connect")
    assert hasattr(client, "connect")


def test_mqtt_client_methods():
    mc = Mqtt_client()
    # setters/getters
    mc.set_broker("example")
    assert mc.get_broker() == "example"
    mc.set_port(1883)
    assert mc.get_port() == 1883
    # test that connect_to raises if broker not set or port invalid (we won't actually connect)
    with pytest.raises(Exception):
        mc.connect_to()
