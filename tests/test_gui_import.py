import pytest

try:
    import gui
except ImportError:
    gui = None


def test_gui_import():
    # GUI may depend on PyQt5; if unavailable just ensure import error makes sense
    if gui is None:
        pytest.skip("PyQt5 not installed in test environment")
    assert hasattr(gui, 'MainWindow')
    assert hasattr(gui, 'ConnectionDock')
    assert hasattr(gui, 'MC')
