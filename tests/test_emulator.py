import sys, os
import pytest

# adjust path to import project modules
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root not in sys.path:
    sys.path.insert(0, root)

import emulator
from mqtt_agent import Mqtt_client


def test_emulator_imports_and_classes():
    # MC should be subclass of Mqtt_client
    assert issubclass(emulator.MC, Mqtt_client)
    # ConnectionDock exists
    assert hasattr(emulator, 'ConnectionDock')
    assert hasattr(emulator, 'MainWindow')
