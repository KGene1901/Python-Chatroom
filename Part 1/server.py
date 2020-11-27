import socket
import select
from _thread import *

## declaring server address ##
host = '127.0.0.1'
port = 8080
##############################

def broadcast_message(message, client_map):
	for client_user in client_map:
			client_map[client_user].sendall(message.encode())

def clientThreadInit(connection, client_map, client_username, f):
	while True:
		try:
			client_msg = connection.recv(1024)
		except:
			break
		chat_display = '\n{}: {}'.format(client_username, client_msg.decode())
		f.write(chat_display)
		print(chat_display)
		broadcast_message(chat_display, client_map)

	exit_msg = '\n{} has disconnected'.format(client_username) # handling client disconnection
	f.write(exit_msg)
	print(exit_msg)
	client_map.pop(client_username)
	broadcast_message(exit_msg, client_map)
	connection.close()

def startServer():

	## initialising important variables ##
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# supporting TCP connection 
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# allows socket to be reusable
	server_socket.bind((host, port))
	client_map = {}
	threadcount = 0
	######################################

	try:
		with open('./server.log', 'w') as f:
			server_socket.listen(5) 
			server_start_msg = 'Server is running and ready to recieve connection at port {} ...\n'.format(port)
			print(server_start_msg)
			f.write(server_start_msg)

			while True:
					connection, client_address = server_socket.accept()	# accepting connection from client
					client_username = connection.recv(1024).decode()
					client_map[client_username] = connection
					welcome_msg = '\n{} has joined'.format(client_username)
					print(welcome_msg + ' from {}'.format(client_address))
					connection.sendall('Welcome to the chatroom {}! Type /quit to exit room.\n'.format(client_username).encode())
					broadcast_message(welcome_msg, client_map)
					f.write('\nRecieved connection from {} with username {}'.format(client_address, client_username))	# logging user connection activity 
					start_new_thread(clientThreadInit, (connection, client_map, client_username, f))
					threadcount += 1
					thread_string = '\nThread: {} initialised'.format(threadcount) 
					print(thread_string)
					f.write(thread_string)

	except Exception as e:
		error_msg = 'Connection with client failed with error: {}\nServer shutting down ...'.format(e)
		f.write(error_msg)
		print(error_msg)

	f.close()
	server_socket.close()

if __name__ == '__main__':
	startServer()