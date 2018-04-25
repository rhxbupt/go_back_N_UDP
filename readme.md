# UDP Server/Client - File Transfer Protocol (FTP)
Using UDP protocol to implement the reliable transfer process between server and client. In this projcet, we implemented the Go-Back-N protocol based on UDP protocol.

# Requirements
Python 2.7+

# Usage
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

Task 1: Effect of Window size N

In this task, select a file at least 1MB, set the MSS to 500 bytes and the loss probability
p = 0.05. Run the Go-back-N protocol to transfer the file you selected, and vary the value of the window size N = 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024.

For N = 1, p = 0.05, MSS = 500 bytes:

For N = 2, p = 0.05, MSS = 500 bytes:

For N = 4, p = 0.05, MSS = 500 bytes:

For N = 8, p = 0.05, MSS = 500 bytes:

For N = 16, p = 0.05, MSS = 500 bytes:

For N = 32, p = 0.05, MSS = 500 bytes:

For N = 64, p = 0.05, MSS = 500 bytes:

For N = 128, p = 0.05, MSS = 500 bytes:

For N = 256, p = 0.05, MSS = 500 bytes:

For N = 512, p = 0.05, MSS = 500 bytes:

For N = 1024, p = 0.05, MSS = 500 bytes:


Task 2: Effect of MSS

Task 3: Effect of Loss Probability p
