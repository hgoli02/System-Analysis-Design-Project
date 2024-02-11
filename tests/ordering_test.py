from client import PyClient as Client

client = Client()

NUM = 100
for i in range(NUM):
    client.push("key2",f"value{i}")

for i in range(NUM):
    a = client.pull()
    assert a == f"value{i}"

print("Test Passed")
