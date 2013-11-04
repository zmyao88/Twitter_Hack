import socket

server = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
server.connect("/tmp/twitter_socket")
while 1:
    data = server.recv(1024)
    print data
