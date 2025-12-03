# SmartHome Copilot Instructions

## Architecture Overview

SmartHome is a Python-based IoT home management system using **MQTT protocol** for device communication and **PyQt5** for GUI. The system has three main execution modes:

- **`gui.py`**: PyQt5-based dashboard with real-time MQTT message handling and data visualization
- **`emulator.py`**: IoT device simulators (DHT sensors, meters, appliances) publishing/subscribing to MQTT topics
- **`manager.py`**: Business logic layer monitoring database and controlling devices via MQTT

## Critical Data Flow Pattern

1. **Device Emulators** (`emulator.py`) → publish sensor data to MQTT topic `pr/Smart/{device_type}/{device_name}`
2. **Manager** (`manager.py`) → subscribes to all topics, parses data, stores in SQLite DB
3. **GUI** (`gui.py`) → subscribes to all topics, updates UI docks in real-time with `on_message()` callbacks
4. **Control**: GUI/Manager can publish commands back to devices via `client.publish(topic, message)`

### Message Format Convention
Messages follow pattern: `From: {name} Temperature: {value} Humidity: {value}` or device-specific formats. Parse using string split on delimiters, not regex.

## Key Components & Dependencies

- **`init.py`**: Configuration hub - broker IP (`broker_ip`), port, credentials, MQTT topic prefix (`comm_topic='pr/Smart/'`), database path (dynamically resolved relative to project root), threshold limits (`Water_max`, `Elec_max`)
- **`mqtt_agent.py`**: Base `Mqtt_client` class with setter/getter patterns; both GUI and emulators inherit via `class MC(Mqtt_client)`. Compatible with paho-mqtt 1.x and 2.1.0+
- **`data_acq.py`**: SQLite operations - two tables: `data` (sensor readings) and `iot_devices` (device metadata)
- **`speech.py`**: Google Cloud STT/TTS integration (requires credentials via environment variable or `credentials/` directory)
- **`assistant_BOT.py`**: Voice-activated bot using speech module

## Development Workflows

### Running the System
Use `start_emulators.sh` (Mac-specific with `osascript` calls, not portable). Manual equivalent:
```bash
# Terminal 1: Device emulators (run each separately)
python emulator.py DHT-1 Celsius Room_1 7
python emulator.py ElecWaterMeter kWh Home 13

# Terminal 2: Manager (control/DB logic)
python manager.py

# Terminal 3: GUI (main dashboard)
python gui.py
```

### Database Operations
- Initialize: `data_acq.init_db(db_name)` - creates `data` and `iot_devices` tables
- Insert sensor data: `data_acq.add_IOT_data(device_name, timestamp, value)`
- Query: `data_acq.fetch_data(db_name, table_name, device_name)` returns pandas DataFrame
- CSV import: `data_acq.csv_acq_data()` imports from `data/homedata.csv` if `db_init=True` in `init.py`

## Project-Specific Patterns

### MQTT Callback Pattern
All classes inherit from `Mqtt_client` and override `on_message()`:
```python
class MC(Mqtt_client):
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8","ignore"))
        # Parse and dispatch by topic substring match
        if 'Room_1' in topic:
            # update UI or DB
```
**Note**: Topic filtering uses substring matching (`'DHT' in topic`, `'alarm' in topic`), not full path comparison.

### Logging Pattern
Uses `icecream` library with prefix formatter for timestamped debug output:
```python
from icecream import ic
def time_format():
    return f'{datetime.now()}  ComponentName|> '
ic.configureOutput(prefix=time_format)
ic.configureOutput(includeContext=False)
```
Also uses Python's `logging` module for file-based logs (`logfile_gui.log`, `logfile_emulator.log`).

### PyQt5 UI Organization
GUI uses QDockWidget pattern with separate dock classes:
- `ConnectionDock`: MQTT broker connection settings
- `StatusDock`: Message log and appliance temps
- `GraphsDock`: Real-time meter visualization (pyqtgraph)
- `AirconditionDock`: AC control panel
- `TempDock`: Temperature displays
- `PlotDock`: Historical data plots

Each dock updates via `update_*()` methods called from `MC.on_message()`.

## Integration Points & Known Issues

1. **MQTT Library Compatibility**: Supports both paho-mqtt 1.x and 2.1.0+
   - paho-mqtt 1.x: Uses `mqtt.Client(client_id, clean_session=True)`
   - paho-mqtt 2.1.0+: Uses `mqtt.Client(CallbackAPIVersion.VERSION1, client_id)`
   - Automatic version detection in `mqtt_agent.py` and `manager.py`
   - See `MQTT_VERSION_COMPATIBILITY.md` for migration details

2. **Speech Module**: Requires Google Cloud credentials. 
   - Setup: Create service account in Google Cloud Console, download JSON key
   - Use environment variable: `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"` 
   - Or run: `python setup_google_credentials.py` to store locally in `credentials/`
   - Requires: `pip install google-cloud-texttospeech google-cloud-speech sounddevice scipy soundfile`

3. **Emulator Args**: `emulator.py` expects 4 CLI args: `device_type`, `unit`, `device_name`, `update_interval`

4. **Database Path**: Now uses dynamic relative path - automatically creates `data/` directory and works anywhere

5. **MQTT Broker**: Defaults to open HiveMQ broker (index `nb=1` in `init.py`), slow/unreliable for development

6. **Platform-Specific**: `start_emulators.sh` uses `osascript` (Mac Terminal automation), won't work on Windows/Linux

7. **mqtt_agent.py**: Core MQTT base class imported as `from mqtt_agent import Mqtt_client` by gui.py and emulator.py

## File-to-Purpose Quick Reference

| File | Purpose | Entry Point |
|------|---------|-------------|
| `init.py` | Global config (broker, DB, thresholds) | Import only, no CLI |
| `mqtt_agent.py` | Base MQTT client class | Inherited by GUI and emulators |
| `data_acq.py` | SQLite DB operations & pandas queries | Imported by manager, GUI, speech module |
| `gui.py` | Main PyQt5 dashboard | `python gui.py` |
| `manager.py` | MQTT-to-DB sync & device control | `python manager.py` |
| `emulator.py` | IoT device simulator | `python emulator.py {type} {unit} {name} {interval}` |
| `speech.py` | Google Cloud STT/TTS | Imported by voice modules (requires credentials) |
| `setup_google_credentials.py` | Interactive setup helper | `python setup_google_credentials.py` |
