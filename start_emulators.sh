#!/bin/bash

diskutil info disk0 | grep -i smart
sleep 1
system_profiler SPHardwareDataType | grep -i Identifier
sleep 1



osascript -e 'tell app "Terminal"to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py DHT-1 Celsius Room_1 7"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py DHT-2 Celsius Room_2 5"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py ElecWaterMeter kWh Home 13"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py Airconditioner Celsius air-1 5"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py Freezer Celsius freezer 6"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py Boiler Celsius boiler 8"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py Refrigerator Celsius refrigerator 9"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/manager.py"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/gui.py"'





