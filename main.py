
class Server:
    def __init__(self, name, ip, os, ram, cpu):
        self.name = name
        self.ip = ip
        self.os = os
        self.ram = ram
        self.cpu = cpu

server1 = Server(input('Name Server: '), input('IP: '), input('OS: '), input('RAM: '), input('CPU: '))
# server1 = Server(
#     "DNS server",
#     "127.0.0.1",
#     "Red Hat Enterprise Linux",
#     '32',
#     4
# )

print('=' * 30)
print(f'Name: {server1.name}, \nIP: {server1.ip}, \nOS: {server1.os}, \nRAM: {server1.ram}, \nCPU: {server1.cpu}')