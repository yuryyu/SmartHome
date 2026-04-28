#!/bin/bash

diskutil info disk0 | grep -i smart
sleep 1
system_profiler SPHardwareDataType | grep -i Identifier
sleep 1

osascript -e 'tell app "Terminal"to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py DHT-1 Celsius Room_1 7"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py DHT-2 Celsius Room_2 5"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py DGasLeak alarm Home 13"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py DSmoke alarm Home 5"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/emulator.py DFlame alarm Home 6"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/manager.py"'
sleep 1
osascript -e 'tell app "Terminal" to do script "/Users/yuryyim/Documents/GitHub/SmartHome/venv/bin/python /Users/yuryyim/Documents/GitHub/SmartHome/gui.py"'





