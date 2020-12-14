import socket
import select
import sys
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
		chat_display = '\n{}: {}'.format(client_username, client_msg)
		f.write(client_msg)

		if client_msg == '/help':
			helpList = '<<Available commands>>\n/listUsers => To list all current users in the chatroom\n/rename <username> => Change your own username\n/whisper <username> <message> => To privately message another user in the chatroom\n/quit => Exit chatroom'
			f.write('\n'+helpList)
			connection.sendall(helpList.encode())
			continue

		elif '/rename' in client_msg:
			split_msg = client_msg.split(' ')
			if split_msg.index('/rename') == 0:
				new_username = ' '.join(split_msg[1:])

				if new_username in client_map: # validation check to avoid two users having the same username
					error_msg = 'This username has been taken. Please try again with /rename <username>'
					f.write('\n'+error_msg)
					connection.sendall(error_msg.encode())
				else:
					broadcast_msg = '{} has changed their username to {}'.format(client_username, new_username)
					f.write('\n'+broadcast_msg)
					broadcast_message(broadcast_message, client_map)
					client_map[new_username] = client_map.pop(client_username)
					print(client_map)
					client_username = new_username

				continue

		elif client_msg == '/listUsers':
			availableUsers = '<<Users>>\n'
			count = 1

			for client in client_map:
				availableUsers+=f'{count}. {client}\n'
				count+=1
			f.write('\n'+availableUsers)
			connection.sendall(availableUsers.encode())

			continue

		elif '/whisper' in client_msg:
			command = client_msg.split(' ')
			selected_username = command[1]

			if selected_username == client_username:
				error_msg1 = 'Not allowed to private message your ownself!'
				f.write(error_msg1)
				connection.sendall(error_msg1.encode())
			elif selected_username not in client_map:
				error_msg2 = 'This user does not exist.'
				f.write(error_msg2)
				connection.sendall(error_msg2.encode())
			else:
				message = '(private) {}: {}'.format(client_username, ' '.join(command[2:]))
				f.write('\n'+message)
				client_map[selected_username].sendall(message.encode())
				client_map[client_username].sendall(message.encode())

			continue

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
	with open('./server.log', 'w') as f:
		try:
			
			server_socket.listen(5) 
			server_start_msg = 'Server is running and ready to recieve connection at port {} ...\n'.format(port)
			print(server_start_msg)
			f.write(server_start_msg)

			while True:
					connection, client_address = server_socket.accept()
					client_username = connection.recv(1024).decode()
					welcome_msg = '\n{} has joined'.format(client_username)
					print(welcome_msg + ' from {}'.format(client_address))
					broadcast_message(welcome_msg, client_map)
					client_map[client_username] = connection
					connection.sendall('Welcome to the chatroom {}! Type /help for a list of chatroom commands.'.format(client_username).encode())
					f.write('\nRecieved connection from {} with username {}'.format(client_address, client_username))
					start_new_thread(clientThreadInit, (connection, client_map, client_username, f))
					threadcount += 1
					thread_string = '\nThread: {} initialised'.format(threadcount) 
					print(thread_string)
					f.write(thread_string)

		except Exception as e:
			error_msg = '\nConnection with client failed with error: {}\nServer shutting down ...'.format(e)
			
		except KeyboardInterrupt:
			error_msg = '\nKeyboardInterrupt - Force closing server'

		f.write(error_msg)
		print(error_msg)
			
	for client in client_map:
		client_map[client].close()
	f.close()
	server_socket.close()
	sys.exit(1)	

if __name__ == '__main__':
	startServer()