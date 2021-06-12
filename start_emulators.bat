// arg: Name Units Place UpdateTime

//start "Emulator: DHT-1" python emulator.py DHT-1 Celsius Room_1 3  
//timeout 3 
//start "Emulator: DHT-2" python emulator.py DHT-2 Celsius Common 4
//timeout 3
//start "Emulator: Electricity&Water Meter" python emulator.py ElecWaterMeter kWh Home 7
//timeout 3
//start "Emulator: Airconditioner" python emulator.py Airconditioner Celsius air-1/sub 6
//timeout 3
start "Emulator: Freezer" python emulator.py Freezer Celsius freezer/sub 8
//timeout 3
start "Emulator: Boiler" python emulator.py Boiler Celsius boler/sub 12
//timeout 3
//start "Smart Home Manager" python manager.py
//timeout 10
//start "System GUI" python gui.py