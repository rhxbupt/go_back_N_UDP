import os
import fcntl
import re
import psutil
import sys
import time
import socket

def exist_file(send_file):
   if(os.path.exists(send_file)):
       return '1'
   else:
       return '-1'

def create_seq_file(send_file,mss,file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    f = open(file_name,'a')
    sequence = 0
    f.write(str(sequence)+',\n')        
    with open(send_file,'rb') as sed_file:
        while True:
            pos = (sequence + 1) * mss
            print 'pos'
            print pos
            sed_file.seek(pos,0)
            data = sed_file.read(1)
            if not data:
                print 'empty'
                break
            sequence = sequence + 1
            f.write(str(sequence)+',\n')    
    sed_file.close()
    f.close()


def rdt_send(file_name,sequence,mss):
    data = ''
    with open(file_name, 'rb') as f:
        pos = sequence * mss
        f.seek(pos,0)
        for i in range(1,mss+1):
            byte_data = f.read(1)
            if byte_data:
                data = data + str(byte_data)
    f.close()
    segment = combine(sequence,data)
    check_data = checksum(segment)
    return check_data

def combine(sequence,data):
    seq_no_bits = '{0:032b}'.format(sequence)
    cksum = '0' * 16
    indicator_bits = '01' * 8
    result = ''
    # byte_data = encode(data)
    # print byte_data
    for i in range(1,len(data)+1):
        data_c = data[i-1]
        data_byte = '{0:08b}'.format(ord(data_c))
        result = result + data_byte
    segment = seq_no_bits + cksum + indicator_bits + result
    return segment

def encode(s):
    return ''.join([bin(ord(c)).replace('0b', '') for c in s])

def checksum(message):
    if message:
        total = 0
        length = len(message)
        data = [message[i:i+16] for i in range(0,len(message),16)]
        for j in data:
			total += int(j,2)
			if total >= 65535:
				total -= 65535
        checksum = 65535-total
        cksum_bit = '{0:016b}'.format(checksum)
        result = message[0:32]+cksum_bit+message[48:]
        return result
    else:
        return '0'

def get_seq(window_size,filename):
    seq_no = -1
    f = open(filename, 'r')
    fcntl.flock(f.fileno(),fcntl.LOCK_EX)
    count = 0
    for line in reversed(f.readlines()):
        if re.findall('(\d+),S\n',line):
            count += 1
        elif re.findall('(\d+),\n',line):
            seq_no = str(re.findall('(\d+),\n',line)[0])
    f.close()
    if count == window_size:
        return -1
    elif count < window_size:
        return seq_no
    else:
        return -1

def set_seq(sequence,filename):
    f = open(filename, 'r+w')
    fcntl.flock(f.fileno(),fcntl.LOCK_EX)
    data = f.readlines()
    if data[int(sequence)] == sequence + ",\n":
        data[int(sequence)] = sequence + ",S\n"       
    new_data = ''.join(data)
    # print 'newdata'
    # print sequence
    # print new_data
    f.seek(0)
    f.truncate()
    f.write(new_data)
    f.close()

def recv_process(socket,filename):
    new_proc = os.fork()
    if new_proc == 0:
        print "process:" + str(os.getpid()) + " created to recv from server"
        while True:
            message,server_addr = socket.recvfrom(max_buff)
            seq_no = validate_recv_msg(message)
            print 'seq_1'
            print seq_no
            if seq_no != -1:
                ack(seq_no,filename)
                       
def ack(seq_no,seq_file):
    make_change = -1
    line_counter = 0
    f = open(seq_file,'r+w')
    fcntl.flock(f.fileno(),fcntl.LOCK_EX)
    data = f.readlines()
    #print "received " + str(seq_no)
    for line in data:
        line_counter +=1
        match = re.findall('(\d+),(\w)\n',line)
        if match:
            read_seq =match[0][0]
            status = match[0][1]
            if int(read_seq) == int(seq_no) and status == 'S' and line_counter == 1:
                make_change  = 1
                break
            elif int(read_seq) < int(seq_no) and status != 'D':
                break
            elif int(read_seq) == int(seq_no) and status == 'S' and line_counter > 1:
                make_change = 1
                break
    if make_change == 1:
        if data[int(seq_no)] == seq_no + ",S\n":
            data[int(seq_no)] = seq_no + ",D\n"
        new_data = ''.join(data)
        f.seek(0)
        f.truncate()
        f.write(new_data)
    f.close()   
 
def validate_recv_msg(message):
    seq = str(int(message[0:32],2))
    pad = message[32:48]
    ack = message[48:]
    if pad == ('0' * 16) and ack == ('10' * 8):
        return seq
    else:
        return -1
    
def timer(send_seq_no,seq_file):
    child_process =os.fork()
    if child_process == 0:
        p = psutil.Process(os.getpid())
        time.sleep(0.5)
        f = open(seq_file,'r+w')
        fcntl.flock(f.fileno(),fcntl.LOCK_EX)
        update_seq_status = -1
        data = f.readlines()
        for line in data:
            match = re.findall('(\d+),(\w)\n',line)
            if match:
                if send_seq_no ==str(match[0][0]):
                    if str(match[0][1]) == 'D':
                        break
                    if str(match[0][1]) == 'S':
                        print 'timeout, the sequence number is ' + send_seq_no
                        update_seq_status = 1
                        break
                    else:
                        break

        if update_seq_status == 1:
            if data[int(send_seq_no)] == send_seq_no + ",S\n":
                data[int(send_seq_no)] = send_seq_no + ",\n"
            new_data = ''.join(data)
            f.seek(0)
            f.truncate()    
            f.write(new_data)
        f.close()
        os._exit(0)


def check_transfer_status(seq_file):
    file_transfer = 0
    f = open(seq_file,'r')
    fcntl.flock(f.fileno(),fcntl.LOCK_EX)
    for line in f:
            if line != '\n':
                status = re.findall('\d+,([D])\n',line)
                if not status:
                    file_transfer = -1
                    break
    f.close()   
    return file_transfer      

start_time = time.time()

if(len(sys.argv) == 6):
	server_host = sys.argv[1]
	port = int(sys.argv[2])
	send_file = sys.argv[3]
	window_size = int(sys.argv[4])
	mss = int(sys.argv[5])
else:
	print "Wrong set of arguments passed"
	os._exit(0)    

seq_file = 'sequence_file.txt'
# host = socket.gethostname()
# port = 7735
# address = (host, port)


file_status = exist_file(send_file)
if file_status == '-1':
    print "file not exist, closing the program.."
    os._exit(0)

max_buff = 65535
address = (server_host,port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_process(s,seq_file)   

create_seq_file(send_file,mss,seq_file)


while 1:
    p = psutil.Process(os.getpid())
    status = check_transfer_status(seq_file)
    print 'status'
    print status
    if status == 0:
        print 'File has already transfered.'
        print 'Total time cost:' + str(time.time() - start_time)
        break
    seq_no = get_seq(window_size,seq_file)
    print 'seq_No:'
    print seq_no
    if seq_no > -1:
        set_seq(seq_no,seq_file)
        msg = rdt_send(send_file,int(seq_no),mss)
        s.sendto(msg,address)
        timer(seq_no,seq_file)

print 'Exiting from process...'
s.close()            
