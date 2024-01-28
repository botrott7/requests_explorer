import socket


# def send_get_request():
#     socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     socket_client.connect(('localhost', 8080))
#     socket_client.sendall(b'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n')
#     data = socket_client.recv(1024)
#     socket_client.close()
#
#     print('Response from the server:')
#     print(data.decode('utf-8'))
#
#
# send_get_request()
