import os.path
import requests
import time
import socket
from Crypto.Cipher import AES
import threading

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}
#guard_ip_1 = '18.223.44.141'
guard_ip_1 = '35.240.179.39'
guard_port_1_outgoing = 8011
client_ip = '0.0.0.0'

def sendRequest(client_port, ip):
    print("Starting for Port : " + str(client_port))
    totalPackets = 10240
    start = time.time()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #client_socket.settimeout(15)
    client_socket.bind((client_ip,client_port))
    client_socket.sendto(bytes(b'Hello server'), (guard_ip_1, guard_port_1_outgoing))
    client_socket.sendto(bytes(b'Hello server2'), (guard_ip_1, guard_port_1_outgoing))
    client_socket.sendto(bytes(b'Hello server3'), (guard_ip_1, guard_port_1_outgoing))
    try:
        #timeout = requests.get('http://127.0.0.1:5000/startspoofing', proxies=proxies, timeout=0.1)
        timeout = requests.get('http://' + ip +':5001/startspoofing/'+ str(client_port), timeout=0.1)
    except Exception:
        print("Reached here!!!")

    receive = bytearray(1040)
    output = bytearray()
    count = 0

    receiving_sp_start = time.time()
    packet_received = []
    obj = AES.new('1234567890123456'.encode('utf8'), AES.MODE_CBC, 'This is an IV456'.encode('utf8'))
    start_download = time.time()
    while(receive != b'EOF'):
        try:
            receive, _ = client_socket.recvfrom(1040)

            #print(receive.decode('utf-8'))
            try:
                temp = obj.decrypt(receive)
                #packet_seq = int(temp[:16], 16)
                #packet_received.append(packet_seq)
                #blocknumber = int(packet_seq/packets_per_block)
                #blocklist[blocknumber] = blocklist[blocknumber] ^ (1 << (packet_seq % packets_per_block))
                #output.extend(temp[16:])

                count += 1
            except Exception:
                pass
            #print(count)
        except Exception:
            break


    receiving_sp_end = time.time()
    receiving_sp_time = receiving_sp_end - receiving_sp_start
    #print("count = " + str(count))
    #print("Download using spoofing = " + str(receiving_sp_time) + "s")
    #print("Total Received Packets : " + str(len(packet_received)))

    number_of_lost_packets = totalPackets - count
    receive = bytearray(1040)
    receive = ''
    start_recovery = time.time()
    lost_packets = number_of_lost_packets

    end_download = time.time()
    end_recovery = time.time()
    client_socket.close()
    print("count = " + str(count))
    print("Download using spoofing = " + str(end_download-start_download) + "s")
    print("Lost Packets : " + str(lost_packets))
    print("Recovery time : " + str(0))
    print("Done for Port : " + str(client_port))
    if not os.path.exists('results-2.csv'):
        f = open("results-2.csv", 'a')
        f.write("downloadTime,totalPackets,lostPackets,lostPacketPercentage,recoveryTime\n")
        f.close()
    f = open("results-2.csv", 'a')
    f.write(str(end_download-start_download) + ',' + str(totalPackets) + ',' + str(lost_packets) + ',' + str((lost_packets/totalPackets) * 100) + ',' + str(end_recovery - start_recovery) + '\n' )
    f.close()
    '''
    lost_packet_seq = []
    for i in range(totalPackets):
        if i not in packet_received:
            lost_packet_seq.append(i)
    #print(lost_packet_seq)
    print(len(lost_packet_seq))
    '''

IP_list = ['34.121.18.68',
           '34.23.19.137']

for i in range(9000,9500,1):
    t = threading.Thread(target=sendRequest, args=(i,IP_list[(i%2)]))
    t.start()
