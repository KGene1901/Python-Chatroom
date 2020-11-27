import socket
import select
from _thread import *

## declaring server address ##
host = '127.0.0.1'
port = 8080
##############################

def broadcast_message(message, client_map): # sends message to all connected clients
	if client_map:
		for client_user in client_map:
				client_map[client_user].sendall(message.encode())

def clientThreadInit(connection, client_map, client_username, f):
	while True:
		try:
			client_msg = connection.recv(1024)
		except:
			break

		client_msg = client_msg.decode()

		if client_msg == '/help':
			helpList = '<<Available commands>>\n/listUsers => To list all current users in the chatroom\n/rename <username> => Change your own username\n/whisper <username> <message> => To privately message another user in the chatroom\n/quit => Exit chatroom'
			connection.sendall(helpList.encode())
			continue

		elif '/rename' in client_msg:
			split_msg = client_msg.split(' ')
			if split_msg.index('/rename') == 0:
				new_username = ' '.join(split_msg[1:])

				if new_username in client_map: # validation check to avoid two users having the same username
					connection.sendall('This username has been taken. Please try again with /rename <username>'.encode())
				else:
					broadcast_message('{} has changed their username to {}'.format(client_username, new_username), client_map)
					client_map[new_username] = client_map.pop(client_username)
					client_username = new_username

				continue

		elif client_msg == '/listUsers':
			availableUsers = '<<Users>>\n'
			count = 1

			for client in client_map:
				availableUsers+=f'{count}. {client}\n'
				count+=1
			connection.sendall(availableUsers.encode())

			continue

		elif '/whisper' in client_msg:
			command = client_msg.split(' ')
			selected_username = command[1]

			if selected_username == client_username:
				connection.sendall('Not allowed to private message your ownself!'.encode())
			elif selected_username not in client_map:
				connection.sendall('This user does not exist.'.encode())
			else:
				message = '(private) {}: {}'.format(client_username, ' '.join(command[2:]))
				client_map[selected_username].sendall(message.encode())
				client_map[client_username].sendall(message.encode())

			continue

		chat_display = '\n{}: {}'.format(client_username, client_msg)
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
					welcome_msg = '\n{} has joined'.format(client_username)
					print(welcome_msg + ' from {}'.format(client_address))
					broadcast_message(welcome_msg, client_map)
					client_map[client_username] = connection
					connection.sendall('Welcome to the chatroom {}! Type /help for list of chatroom commands.'.format(client_username).encode())
					f.write('\nRecieved connection from {} with username {}'.format(client_address, client_username))	# logging user connection activity 
					start_new_thread(clientThreadInit, (connection, client_map, client_username, f))
					threadcount += 1
					thread_string = '\nThread: {} initialised'.format(threadcount) 
					print(thread_string)
					f.write(thread_string)

	except Exception as e:
		error_msg = 'Connection with client failed with error: {}\nServer shutting down ...'.format(e)
		for client in client_map:
			client_map[client].close()
		f.write(error_msg)
		print(error_msg)

	f.close()
	server_socket.close()

if __name__ == '__main__':
	startServer()