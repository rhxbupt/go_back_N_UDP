# UDP Server/Client - File Transfer Protocol (FTP) #
Using UDP protocol to implement the reliable transfer process between server and client. In this projcet, we implemented the Go-Back-N protocol based on UDP protocol.

# Requirements #
Python 2.7+

# Usage #
Run server.py whitin the folder with the following commands:
```
python server.py port# file-name p
```

In details:

port# is the number of port you want to use, it should be the same as the port number client using.

file-name is the file you used to receive the data transfered from client.

p is the nunber of probability of drop packet, which used to simulate the packet lose condition in real-life condition. P should be in the duration: 0 < p < 1.


Output:
```
Listening port...
```

And if the server receiver the packet sent from client, it will display:
```
message:
0000000000000000000000000000001001111001010000110101010101010101001100010011001000110011
```
And this displayed message is in binary format.


Now run client.py on the same port
```
python client.py server-host-name server-port# file-name N MSS
```
In details:
server-host-name is the hostname of your computer, you can use command ``` hostname ``` in MacOS and Linux operation system.

server-port# is the number of port you want to use in transfer process.

file-name is the file you want to transfer. you need to specify it in absolute path if this file is not in the same folder of python file.

N is the size of window size, you need to set this window size in advance, the N can be: 1,
2, 4, 8, 16, 32, 64, 128, 256, 512, 1024.

MSS means the maximum segment size, it will form a segment that includea  header and MSS bytes of data. as a result, all segments sent, except possibly for the very last one, will have exactly MSS bytes of data.

If the transfer process work correctly, there will be a display:
```
File has already transfered.
Total time cost:0.0177121162415
Exiting from process...
```

The file will be received by the server through a socket connection. 

# Tasks #

## Task 1: Effect of Window size N ##

In this task, select a file at least 1MB, set the MSS to 500 bytes and the loss probability
p = 0.05. Run the Go-back-N protocol to transfer the file you selected, and vary the value of the window size N = 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024.

For N = 1, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/N%3D1.png)

For N = 2, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/N%20%3D2.png)

For N = 4, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/N%20%3D%204.png)

For N = 8, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/N%20%3D%208.png)

For N = 16, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/N%20%3D%2016.png)

For N = 32, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/N%20%3D%2032.png)

For N = 64, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/N%20%3D64.png)

For N = 128, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/n%20%3D128.png)

For N = 256, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/n%20%3D%20256.png)

For N = 512, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/n%20%3D%20512.png)

For N = 1024, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/n%3D1024.png)

The conclusion image is:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/window_size.png)


## Task 2: Effect of MSS ##

In this task, let the window size N = 64 and the loss probability p = 0.05. Run the Go-back-N protocol to
transfer the same file, and vary the MSS from 100 bytes to 1000 bytes in increments of 100 bytes.

For N = 64, P = 0.05, MSS = 100 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/MSS%20%3D100.png)

For N = 64, P = 0.05, MSS = 200 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/mss%20%3D%20200.png)

For N = 64, P = 0.05, MSS = 300 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/mss%20%3D%20300.png)

For N = 64, P = 0.05, MSS = 400 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/mss%20%3D%20400.png)

For N = 64, P = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/N%20%3D64.png)

For N = 64, P = 0.05, MSS = 600 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/m%20%3D600.png)

For N = 64, P = 0.05, MSS = 700 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/m%20%3D700.png)

For N = 64, P = 0.05, MSS = 800 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/m%20%3D%20800.png)

For N = 64, P = 0.05, MSS = 900 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/mss%20%3D900.png)

For N = 64, P = 0.05, MSS = 1000 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/mss%3D1000%20.png)

The conclusion image is:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/mss.png)


## Task 3: Effect of Loss Probability p ##

For this task, set the MSS to 500 bytes and the window size N = 64. Run the Go-back-N protocol to transfer the
same file, and vary the loss probability from p = 0.01 to p = 0.10 in increments of 0.01. 

For N = 64, p = 0.01, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/%20p%20%3D%200.01.png)

For N = 64, p = 0.02, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/p%20%3D%200.02.png)

For N = 64, p = 0.03, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/p%20%3D%200.03.png)


For N = 64, p = 0.04, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/p%20%3D%200.04.png)

For N = 64, p = 0.05, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/screencast/N%20%3D64.png)

For N = 64, p = 0.06, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/p%20%3D0.06.png)

For N = 64, p = 0.07, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/p%20%3D%200.07.png)

For N = 64, p = 0.08, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/p%20%3D%200.08.png)

For N = 64, p = 0.09, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/p%20%3D0.09.png)

For N = 64, p = 0.10, MSS = 500 bytes:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/p%20%3D%201.0.png)

The conclusion image is:

![image](https://github.com/rhxbupt/go_back_N_UDP/blob/master/screencast/p.png)











