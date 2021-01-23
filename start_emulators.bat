// arg: Name Units Place UpdateTime

start "Emulator: DHT-1" python emulator.py DHT-1 Celsius Room_1 15   
//start "Emulator DHT-2" python emulator.py DHT-2 Celsius Living_Room 1
start "Emulator: airconditioner" python emulator.py airconditioner Celsius air-1/sub 15
start "Smart Home Manager" python manager.py
