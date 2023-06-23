import os
import shutil
import time
import socket
from stem.control import Controller
from flask import Flask
from flask import send_file, request
from Crypto.Cipher import AES #install pycryptodome

app = Flask(__name__)

#spoofed_ip = '192.168.1.147'
spoofed_ip = '10.128.0.7'
spoofed_port_outgoing = 8005
guard_ip_3 = '35.245.92.29'
guard_port_3_incoming = 8003

r_count = 0
c_count = 0
buffer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
buffer.bind(('0.0.0.0', spoofed_port_outgoing))
reuqest_seq = 0


key = '1234567890123456'


def ConvertToFixedString(v,size):
    v_hex = hex(v)
    v_str_fixed = v_hex[:2] + (size - len(v_hex)) * '0' + v_hex[2:]
    return bytes(v_str_fixed, encoding='utf-8')


@app.route('/')
def index():
  return "<h1>this is a demo .onion for research purpose only!</h1>"

@app.route('/hello')
def hello_world():
   return "<h1>Hello world!!!</h1>"

@app.route('/spoof/<ip>/<gaurd_ip>/<gaurd_port>')
def tor_download(ip, gaurd_ip, gaurd_port):
    global spoofed_ip, guard_ip_3, guard_port_3_incoming
    spoofed_ip = ip
    guard_ip_3 = gaurd_ip
    guard_port_3_incoming = int(gaurd_port)
    print("spoofed ip = " + str(spoofed_ip))
    print("Dst IP = " + str(guard_ip_3))
    print("Dst Port = " + str(guard_port_3_incoming))
    return str(spoofed_port_outgoing)

@app.route('/startspoofing/<forwarding_port>')
def startSpoof(forwarding_port):
    global r_count, c_count 
    r_count +=1
    time.sleep(0.1)
    forwarding_port = int(forwarding_port)
    print('starting spoofing')
    print("src ip = " + spoofed_ip + " src port = " + str(spoofed_port_outgoing) + ' port type = ' + str(type(spoofed_port_outgoing)))
    print("dst ip = " + guard_ip_3 + ' dst port = ' + str(guard_port_3_incoming) + ' port type = ' + str(type(guard_port_3_incoming)))

    fp = open("example1.file", 'rb')
    input = fp.read()
    splitLen = 1024
    obj = AES.new('1234567890123456'.encode('utf8'), AES.MODE_CBC, 'This is an IV456'.encode('utf8'))
    start = time.time()
    count = 0
    #ss = conf.L3socket()
    #payload = input[0:20]
    #spoofed_packet = (IP(src=spoofed_ip, dst=guard_ip_3) / UDP(sport=spoofed_port_outgoing, dport=guard_port_3_incoming) / payload)
    #payload2 = spoofed_packet['payload']
    for lines in range(0, len(input), splitLen):
        time.sleep(0.003)
        #time.sleep(0.007)
        b = hex(count)
        #print()
        payload = obj.encrypt(bytes(b[:2] + (16-len(b)) * "0" + b[2:], encoding='utf-8') + ConvertToFixedString(forwarding_port,16) + input[lines:lines+splitLen])
        p2 = bytes(b[:2] + (16-len(b)) * "0" + b[2:], encoding='utf-8') + ConvertToFixedString(forwarding_port,16) + input[lines:lines+splitLen]
        #payload = bytes(b[:2] + (16-len(b)) * "0" + b[2:], encoding='utf-8') + input[lines:lines+splitLen]
        #print(int(p2[16:32],16))
        #return 'ok'
        elapsed1 = time.time()

        buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
        #spoofed_packet = IP(src=spoofed_ip, dst=guard_ip_3) / UDP(sport=spoofed_port_outgoing, dport=guard_port_3_incoming) / payload
        
        #ss.send(spoofed_packet)
        count += 1
        end1 = time.time()
        elapsed2 = time.time()
        payload = input[lines:lines+splitLen]
        end2 = time.time()
        #time.sleep(0.0008)
        #print("Forwarding port : " + str(forwarding_port) + " count = " + str(count) + ' elapsed1 time = ' + str(end1 - elapsed1) + 's 2 = ' + str(end2 - elapsed2) + 's')
    print("Total sent packets : " + str(count))
    payload = b'EOF'
    #spoofed_packet = IP(src=spoofed_ip, dst=guard_ip_3) / UDP(sport=spoofed_port_outgoing, dport=guard_port_3_incoming) / payload
    #ss.send(spoofed_packet)
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    payload = b'EOF'
    #spoofed_packet = IP(src=spoofed_ip, dst=guard_ip_3) / UDP(sport=spoofed_port_outgoing, dport=guard_port_3_incoming) / payload
    #ss.send(spoofed_packet)
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    payload = b'EOF'
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    payload = b'EOF'
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    payload = b'EOF'
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    payload = b'EOF'
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    payload = b'EOF'
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    payload = b'EOF'
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    payload = b'EOF'
    #spoofed_packet = IP(src=spoofed_ip, dst=guard_ip_3) / UDP(sport=spoofed_port_outgoing, dport=guard_port_3_incoming) / payload
    #ss.send(spoofed_packet)
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    print("sending done!!!" + str(time.time() - start) + 's')
    print("Request count : " + str(r_count))
    c_count += 1
    print("Completed : " + str(c_count))
    return 'ok'

@app.route('/packetRecovery/<number_of_lost_packets>')
def packetRecovery(number_of_lost_packets):
    time.sleep(1)
    print('starting recovery : ' + str(number_of_lost_packets))

    fp = open("example1.file", 'rb')
    input = fp.read()
    splitLen = 1024
    obj = AES.new('1234567890123456'.encode('utf8'), AES.MODE_CBC, 'This is an IV456'.encode('utf8'))
    start = time.time()
    count = 0
    # ss = conf.L3socket()
    # payload = input[0:20]
    # spoofed_packet = (IP(src=spoofed_ip, dst=guard_ip_3) / UDP(sport=spoofed_port_outgoing, dport=guard_port_3_incoming) / payload)
    # payload2 = spoofed_packet['payload']
    for lines in range(0, int(number_of_lost_packets)*splitLen, splitLen):
        time.sleep(0.0008)
        b = hex(count)
        # print()
        payload = obj.encrypt(
            bytes(b[:2] + (16 - len(b)) * "0" + b[2:], encoding='utf-8') + input[lines:lines + splitLen])
        # payload = bytes(b[:2] + (16-len(b)) * "0" + b[2:], encoding='utf-8') + input[lines:lines+splitLen]
        # print(payload[:16])
        elapsed1 = time.time()

        buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
        # spoofed_packet = IP(src=spoofed_ip, dst=guard_ip_3) / UDP(sport=spoofed_port_outgoing, dport=guard_port_3_incoming) / payload

        # ss.send(spoofed_packet)
        count += 1
        end1 = time.time()
        elapsed2 = time.time()
        payload = input[lines:lines + splitLen]
        end2 = time.time()
        # time.sleep(0.0008)

        #print("count = " + str(count) + ' elapsed1 time = ' + str(end1 - elapsed1) + 's 2 = ' + str(end2 - elapsed2) + 's')
    payload = b'EOF'
    # spoofed_packet = IP(src=spoofed_ip, dst=guard_ip_3) / UDP(sport=spoofed_port_outgoing, dport=guard_port_3_incoming) / payload
    # ss.send(spoofed_packet)
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    payload = b'EOF'
    # spoofed_packet = IP(src=spoofed_ip, dst=guard_ip_3) / UDP(sport=spoofed_port_outgoing, dport=guard_port_3_incoming) / payload
    # ss.send(spoofed_packet)
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    payload = b'EOF'
    # spoofed_packet = IP(src=spoofed_ip, dst=guard_ip_3) / UDP(sport=spoofed_port_outgoing, dport=guard_port_3_incoming) / payload
    # ss.send(spoofed_packet)
    buffer.sendto(payload, (guard_ip_3, guard_port_3_incoming))
    print("sending done!!!" + str(time.time() - start) + 's')
    return 'ok'


@app.route('/download', methods=['POST', 'GET'])
def download():
    return send_file('example.file', attachment_filename='example.file')

@app.route('/download1', methods=['POST', 'GET'])
def download1():
    return send_file('example1.file')

@app.route('/download2', methods=['POST', 'GET'])
def download2():
    return send_file('example2.file', attachment_filename='example2.file')

@app.route('/download3', methods=['POST', 'GET'])
def download3():
    return send_file('example3.file', attachment_filename='example3.file')

@app.route('/download4', methods=['POST', 'GET'])
def download4():
    return send_file('example4.file', attachment_filename='example4.file')

@app.route('/download5', methods=['POST', 'GET'])
def download5():
    return send_file('example5.file', attachment_filename='example5.file')
@app.route('/retransmit', methods=['POST'])
def retransmit():
  receiveddata = request.get_data()
  receiveddata = str(receiveddata, 'utf-8')
  lost_packet_seq_list = []
  receiveddata = receiveddata[1:-1] + ','
  while receiveddata != '':
    number = receiveddata[:receiveddata.index(',')]
    receiveddata = receiveddata[receiveddata.index(',') + 1:]
    lost_packet_seq_list.append(int(number))

  print(lost_packet_seq_list)
  print(len(lost_packet_seq_list))
  fp = open("example1.file", 'rb')
  input = fp.read()
  splitLen = 1024
  obj = AES.new('1234567890123456', AES.MODE_CBC, 'This is an IV456')
  resend_data = bytes()
  for packet_seq in lost_packet_seq_list:
    resend_data = resend_data + input[packet_seq*1024 : packet_seq*1024 +splitLen]
  
  payload = obj.encrypt(resend_data)
  start = time.time()
  print('Sending recovery.......')
  return payload

@app.route('/test/<forwarding_port>')
def test(forwarding_port):
    print("starting to server : " +str(forwarding_port))
    time.sleep(10)
    print("Serving is Done : " + str(forwarding_port))
    return 'ok'

app.run('0.0.0.0', 5001)

'''
print(' * Connecting to tor')

with Controller.from_port() as controller:
  controller.authenticate()

  # All hidden services have a directory on disk. Lets put ours in tor's data
  # directory.
  hidden_service_dir = os.path.join(controller.get_conf('DataDirectory', '/tmp'), 'hello_world')

  # Create a hidden service where visitors of port 80 get redirected to local
  # port 5000 (this is where Flask runs by default).

  print(" * Creating our hidden service in %s" % hidden_service_dir)
  result = controller.create_hidden_service(hidden_service_dir, 80, target_port = 5000)

  # The hostname is only available when we can read the hidden service
  # directory. This requires us to be running with the same user as tor.

  if result.hostname:
    print(" * Our service is available at %s, press ctrl+c to quit" % result.hostname)
  else:
    print(" * Unable to determine our service's hostname, probably due to being unable to read the hidden service directory")

  try:
    app.run()
  finally:
    # Shut down the hidden service and clean it off disk. Note that you *don't*
    # want to delete the hidden service directory if you'd like to have this
    # same *.onion address in the future.

    print(" * Shutting down our hidden service")
    controller.remove_hidden_service(hidden_service_dir)
    shutil.rmtree(hidden_service_dir)
    '''
