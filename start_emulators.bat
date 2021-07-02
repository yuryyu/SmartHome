// arg: Name Units Place UpdateTime

start "Emulator: DHT-1" python emulator.py DHT-1 Celsius Room_1 24  
timeout 3 
start "Emulator: DHT-2" python emulator.py DHT-2 Celsius Common 23
timeout 3
start "Emulator: Electricity&Water Meter" python emulator.py ElecWaterMeter kWh Home 15
timeout 3
start "Emulator: Airconditioner" python emulator.py Airconditioner Celsius air-1/sub 17
timeout 3
start "Emulator: Freezer" python emulator.py Freezer Celsius freezer/sub 8
timeout 3
start "Emulator: Boiler" python emulator.py Boiler Celsius boiler/sub 12
timeout 3
start "Emulator: Refrigerator" python emulator.py Refrigerator Celsius refrigerator/sub 11
timeout 3
start "Smart Home Manager" python manager.py
timeout 10
start "System GUI" python gui.py