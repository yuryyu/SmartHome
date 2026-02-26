import sys, os
import tempfile
import sqlite3
import pytest
import pandas as pd

# adjust path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root not in sys.path:
    sys.path.insert(0, root)

import data_acq as da
from init import PROJECT_ROOT


def test_init_db_and_insert_fetch(tmp_path, monkeypatch):
    # create temporary db file
    db_file = tmp_path / "test.db"
    da.init_db(str(db_file))
    # monkeypatch connection function to use the same temp file for subsequent operations
    def temp_conn(path=None):
        return sqlite3.connect(str(db_file))
    monkeypatch.setattr(da, 'create_connection', temp_conn)

    # insert a row and fetch it
    da.add_IOT_data("device1", "2025-01-01 00:00:00", 123)
    df = da.fetch_data(str(db_file), "data", "device1")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.iloc[0][0] == "device1"
