// arg: Name Units Place UpdateTime

start "Emulator: DHT-1" python emulator.py DHT-1 Celsius Room_1 5   
start "Emulator: Electricity&Water Meter" python emulator.py ElecWaterMeter kWh Common 7
start "Emulator: Airconditioner" python emulator.py airconditioner Celsius air-1/sub 6
start "Smart Home Manager" python manager.py
