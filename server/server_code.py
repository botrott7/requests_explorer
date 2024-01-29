import socket
import sqlite3
import os

HOST = 'localhost'
PORT = 8080

database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database', 'server.db')
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Создание сокета TCP/IP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1) # Начинаем прослушивать входящие соединения.
    print(f'Server {HOST} : {PORT}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'New client connected: {addr[0]}:{addr[1]}')
        request_data = client_socket.recv(1024).decode('utf-8')
        print(f'Received request: \n{request_data}')

        if request_data.startswith('GET'):
            response = 'HTTP/1.1 200 OK\n\nConnection established!'

        elif request_data.startswith('POST'):
            request_lines = request_data.split('\n')
            empty_line_index = next((index for index, line in enumerate(request_lines) if line.strip() == ''),
                                    len(request_lines))

            if empty_line_index < len(request_lines):
                text = '\n'.join(request_lines[empty_line_index + 1:]).strip()
                if '==' in text:
                    name, message = text.split('==')
                    query_check = f"SELECT COUNT(*) FROM data WHERE name = '{name}'"
                    result = cursor.execute(query_check).fetchone()[0]
                    if result == 0:
                        query = f"INSERT INTO data (name, text) VALUES ('{name}', '{message}')"
                        cursor.execute(query)
                        connection.commit()
                        response = 'HTTP/1.1 200 OK\n\nData has been added!'
                    else:
                        response = 'HTTP/1.1 400 Bad Request\n\nName already exists in the database!'
                elif text == 'all':
                    query = f"SELECT name FROM data"
                    result = cursor.execute(query).fetchall()
                    response = 'HTTP/1.1 200 OK\n\n'
                    if result:
                        for row in result:
                            response += row[0] + '\n'
                    else:
                        response += 'No data found!\n'

                else:
                    query_check = f"SELECT text FROM data WHERE name = '{text}'"
                    result = cursor.execute(query_check).fetchone()
                    if result is not None:
                        response = f'HTTP/1.1 200 OK\n\n{result[0]}'
                    else:
                        response = 'HTTP/1.1 400 Bad Request\n\nName does not exist in the database!'
            else:
                response = 'HTTP/1.1 400 Bad Request\n\nEmpty line separating headers and body is missing!'

        elif request_data.startswith('PUT'):
            request_lines = request_data.split('\n')
            empty_line_index = next((index for index, line in enumerate(request_lines) if line.strip() == ''),
                                    len(request_lines))

            if empty_line_index < len(request_lines):
                text = '\n'.join(request_lines[empty_line_index + 1:]).strip()
                if '==' in text:
                    name, message = text.split('==')
                    query_check = f"SELECT COUNT(*) FROM data WHERE name = '{name}'"
                    result = cursor.execute(query_check).fetchone()[0]
                    if result != 0:
                        query = f"UPDATE data SET text = '{message}' WHERE name = '{name}'"
                        cursor.execute(query)
                        connection.commit()
                        response = 'HTTP/1.1 200 OK\n\nData has been updated!'
                    else:
                        response = 'HTTP/1.1 400 Bad Request\n\nName does not exist in the database!'
                else:
                    response = 'HTTP/1.1 400 Bad Request\n\nInvalid data format!'
            else:
                response = 'HTTP/1.1 400 Bad Request\n\nEmpty line separating headers and body is missing!'

        else:
            response = 'HTTP/1.1 400 Bad Request\n\nUnknown command!'

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()


if __name__ == '__main__':
    run_server()
