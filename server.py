import time
import socket
import os
import random
import sys
from decimal import Decimal

def gen_random_number():
	while 1:
		number  = random.random()
		if Decimal(number) != Decimal(0.0):
			break
	return number	

def rdt_send(message,seq_counter):
	if message:	
		seq_no = str(int(message[0:32],2))
		send_seq_no = '{0:032b}'.format(int(seq_no))
		pad = '0' * 16
		ack_ind = '10' * 8
		return send_seq_no + pad + ack_ind
	else:
		#print "Packet loss, sequence number = " + seq_no
		return ''

def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(',')]])

# def split(string,width):
#     return [string[x:x+width] for x in range(0,len(string),width)]

def write_file(message,filename):
    print 'message'
    print message
    f = open(filename,'a')
    # temp = split(message,8)
    # # result = decode(temp)
    # print 'decode:'
    # print result
    msg = str(message[64:])
    iterations = len(msg)/8
    final_data = ''
    for i in range(0,iterations):
		bit_data = str(msg[i*8:(i+1)*8])
		char_data = chr(int(bit_data, 2))
		final_data = final_data + char_data
    f.write(final_data)
    f.close()

def cal_checksum(msg):
    if msg[48:64] == '01' * 8:
        total = 0
        data = [msg[i:i+16] for i in range(0,len(msg),16)]
        for y in data:
            total += int(y,2)
            if total >= 65535:
                total -= 65535
            if total == 0:
                return 1
            else:
                return -1
    else:
        return -1

# host = socket.gethostname()
# port = 7735
# address = (host, port)

if(len(sys.argv) == 4):
	port = int(sys.argv[1])
	filename = sys.argv[2]
	probability = float(sys.argv[3])
else:
	print "Wrong set of arguments passed"
	os._exit(0)


# if os.path.exists(filename):
# 	os.remove(filename)

hostname = ""
address = (hostname,port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
print "Listening port..."
seq_counter = 0
while 1:
	message, client_address = s.recvfrom(65535)
	random_num = gen_random_number()
	if random_num > probability:
		checksum = cal_checksum(message)
		if checksum == 1 and message[48:64] == '01' * 8:
			got_seq_no = int(message[0:32],2)
			if got_seq_no == seq_counter:
				send_msg = rdt_send(message,seq_counter)
				if send_msg:
					s.sendto(send_msg, client_address)
					# write to file
					write_file(message,filename)
					seq_counter = seq_counter + 1
			elif got_seq_no > seq_counter:
				print "Packet loss, sequence number = " + str(got_seq_no)
			elif got_seq_no < seq_counter:
				send_msg = rdt_send(message,seq_counter)
				if send_msg:
					print "Ack retransmitted:" + str(got_seq_no)
					s.sendto(send_msg, client_address)
		else:
			print "Packet Discarded"
	else:
		got_seq_no = int(message[0:32],2)
		print "Packet loss, sequence number = " + str(got_seq_no)
		
s.close()
            