import subprocess
print("Monitoring all packets on all enabled network interfaces for 10 seconds")
# Capture to pcap file for 10 seconds
subprocess.run('/opt/homebrew/bin/timeout 10 tcpdump -i any -w output.pcap', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# Convert pcap to text
p = subprocess.Popen(['tcpdump', '-r', 'output.pcap'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
with open('output.txt', 'w') as f:
    for line in p.stdout:
        f.write(line.decode())
p.wait()
print("To view the captured packets open the file output.txt")