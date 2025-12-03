# MQTT Version Compatibility Guide

## Overview

SmartHome is now compatible with both **paho-mqtt 1.x** and **paho-mqtt 2.1.0+** (and future 2.x versions).

## Breaking Changes in paho-mqtt 2.0+

### 1. Client Constructor Signature

**paho-mqtt 1.x:**
```python
client = mqtt.Client(client_id, clean_session=True)
```

**paho-mqtt 2.0+:**
```python
client = mqtt.Client(CallbackAPIVersion.VERSION1, client_id)
# clean_session replaced with clean_start (automatic in v2)
```

### 2. CallbackAPIVersion

In paho-mqtt 2.0+, you must specify the callback API version:
- `CallbackAPIVersion.VERSION1`: For legacy applications
- `CallbackAPIVersion.VERSION2`: For new applications (not used here)

## Implementation

We use a **compatibility layer** that automatically detects the installed version:

```python
# Check paho-mqtt version for compatibility (supports both 1.x and 2.1.0+)
try:
    # paho-mqtt 2.0+
    from paho.mqtt.client import CallbackAPIVersion
    MQTT_CLIENT_INIT = lambda name: mqtt.Client(CallbackAPIVersion.VERSION1, name)
except ImportError:
    # paho-mqtt 1.x
    MQTT_CLIENT_INIT = lambda name: mqtt.Client(name, clean_session=True)
```

## Files Updated

- **mqtt_agent.py**: Base MQTT client class
  - Added version detection logic
  - Updated `connect_to()` method to use `MQTT_CLIENT_INIT()`

- **manager.py**: Manager service
  - Added version detection logic
  - Updated `client_init()` function to use `MQTT_CLIENT_INIT()`

## Testing

To verify compatibility:

```bash
# Test with current version
python3 -c "
from mqtt_agent import Mqtt_client, MQTT_CLIENT_INIT
import manager
print('✅ Compatibility verified')
"

# Install paho-mqtt 2.1.0
pip install paho-mqtt==2.1.0

# Test again (should still work)
python3 manager.py
```

## Migration Notes

### For paho-mqtt 1.x Users
No changes required. The code automatically uses the 1.x API.

### For paho-mqtt 2.1.0+ Users
The code automatically detects and uses the 2.0+ API. No manual changes needed.

### For Future Versions
This compatibility approach scales to future 2.x releases without code changes, as long as they maintain the `CallbackAPIVersion` enum.

## Best Practices

When upgrading paho-mqtt:

1. **Test in isolated environment first**
   ```bash
   python3 -m venv test_env
   source test_env/bin/activate
   pip install paho-mqtt==2.1.0
   python3 manager.py
   ```

2. **Monitor logs for deprecation warnings**
   - paho-mqtt 2.0+ may emit warnings about legacy callbacks

3. **Keep dependencies updated**
   ```bash
   pip list | grep paho
   pip install --upgrade paho-mqtt
   ```

## References

- [paho-mqtt 2.0 Migration Guide](https://github.com/eclipse/paho.mqtt.python/blob/master/MIGRATION.md)
- [paho-mqtt Documentation](https://github.com/eclipse/paho.mqtt.python)
- [MQTT Protocol Specification](https://mqtt.org/mqtt-specification/)

## Version History

- **v2.1.0**: Added paho-mqtt 2.1.0 compatibility
- **v1.6.1**: Original release with paho-mqtt 1.x
