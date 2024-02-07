from pythonping import ping

ip = "localhost"  # Example IP
response = ping(ip, timeout=0.005, count=1)

if response.success():
    print(f"{ip} is alive")
else:
    print(f"{ip} is not responding")


ip = "http://system-analysis-design-project-queue-2"  # Example IP
response = ping(ip, timeout=0.005, count=1)

if response.success():
    print(f"{ip} is alive")
else:
    print(f"{ip} is not responding")


ip = "http://system-analysis-design-project-queue-1"  # Example IP
response = ping(ip, timeout=0.005, count=1)

if response.success():
    print(f"{ip} is alive")
else:
    print(f"{ip} is not responding")
