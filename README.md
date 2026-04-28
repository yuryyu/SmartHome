# SmartHome

SmartHome is a Python‑based Internet-of-Things home automation system that uses MQTT for device communication and PyQt5 for a desktop GUI. It includes emulators for sensors/devices, a manager service that logs data to SQLite and enforces thresholds, and a real‑time dashboard.

---

## Quick Start

```bash
# install dependencies
pip install -r requirements.txt   # if such file exists; otherwise install pyqt5 paho-mqtt pandas pyqtgraph icecream

# run manager in one terminal
python manager.py

# run emulators in additional terminals
python emulator.py DHT-1 Celsius Room_1 7
python emulator.py ElecWaterMeter kWh Home 13

# run GUI in a third terminal
python gui.py
```

> Use `start_emulators.sh` on Mac for convenience (calls multiple `python emulator.py` automatically).

---

## File Overview

| File | Purpose | Entry Point |
|------|---------|-------------|
| `init.py` | Central configuration (broker, port, db path, thresholds) | imported by all modules |
| `mqtt_agent.py` | Base MQTT client class; handles connection, callbacks | subclassed by GUI/emulators |
| `data_acq.py` | SQLite helper functions & pandas queries | used by manager & GUI |
| `manager.py` | Backend service that subscribes to topics, stores data, triggers alerts | `python manager.py` |
| `emulator.py` | IoT device simulator (DHT, meters, appliances) | `python emulator.py {type} {unit} {name} {interval}` |
| `gui.py` | PyQt5 dashboard with multiple docks | `python gui.py` |


## Testing & Development

- Use `data_acq.fetch_data()` to query the SQLite database.
- Look at log files (`logfile_manager.log`, `logfile_emulator.log`, `logfile_gui.log`) for debugging.
- **Run unit tests**: a small pytest suite is located under `tests/`.
  ```bash
  pip install pytest
  pytest tests
  ```
- Tests cover MQTT client, database operations, manager callbacks, emulator classes, and basic GUI import.



---

## License

[MIT](LICENSE)

