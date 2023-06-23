import socket
import time
from Crypto.Cipher import AES

#client_ip = '24.252.62.241'
client_ip = '35.236.226.144'
client_port_incoming = 8004
gurad_port_1_outgoing = 8011 #outgoing port
gurad_port_1_incoming = 8001
gurad_ip_2 = '34.90.151.160'
gurad_port_2_outgoing = 8022
obj_decrypt = AES.new('1234567890123456'.encode('utf8'), AES.MODE_CBC, 'This is an IV456'.encode('utf8'))
obj_encrypt = AES.new('1234567890123456'.encode('utf8'), AES.MODE_CBC, 'This is an IV456'.encode('utf8'))
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.bind(('0.0.0.0', gurad_port_1_outgoing))


buffer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
buffer.bind(('', gurad_port_1_incoming))
buffer.settimeout(30.0)
'''
These packets will create a hole on the firewall of the 2nd guard node 
so that packets from the onion server with the spoofed src IP address
can reach to the 2nd guard node. 
'''
try:
    while True:
        try:

            buffer.sendto(b'Hello server', (gurad_ip_2, gurad_port_2_outgoing))
            buffer.sendto(b'Hello server2', (gurad_ip_2, gurad_port_2_outgoing))
            buffer.sendto(b'Hello server3', (gurad_ip_2, gurad_port_2_outgoing))
            buffer_packet = ''
            start = time.time()
            count = 0

            while(buffer_packet!=b'EOF'):
                end = time.time()
                count += 1
                if end - start > 1:
                    start = time.time()
                    buffer.sendto(b'Hello server3', (gurad_ip_2, gurad_port_2_outgoing))
                    print('Receivin/Users/hasniujzahan/Downloads/Tor_script_threaded/TheClient_3.pyg......' + str(count))
                buffer_packet, _ = buffer.recvfrom(1040)
                try:
                    p2 = obj_decrypt.decrypt(buffer_packet)
                    client_port_incoming = int(p2[16:32],16)
                    #print(client_port_incoming)
                    serversocket.sendto(obj_encrypt.encrypt(p2), (client_ip, client_port_incoming))
                except Exception:
                    serversocket.sendto(buffer_packet, (client_ip, client_port_incoming))
            print("Receiving Done " + str(count))
        except socket.timeout:
            buffer.sendto(b'Hello server3', (gurad_ip_2, gurad_port_2_outgoing))
            print("Node is waiting.....")
except KeyboardInterrupt:
    print("Closing the guard node...")
buffer.close()
serversocket.close()
