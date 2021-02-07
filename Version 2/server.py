import socket
import sys
from _thread import *

## declaring server address ##
host = '127.0.0.1'
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
		chat_display = '\n'+str(client_username)+': '+str(client_msg)
		f.write(chat_display)

		if client_msg == '/help':
			helpList = '<<Available commands>>\n/listUsers => To list all current users in the chatroom\n/rename <username> => Change your own username\n/whisper <username> <message> => To privately message another user in the chatroom\n/quit => Exit chatroom'
			f.write('\n\n'+helpList+'\n\n')
			connection.sendall(helpList.encode())
			continue

		elif '/rename' in client_msg:
			split_msg = client_msg.split(' ')
			if split_msg.index('/rename') == 0:
				new_username = split_msg[1] # ensures that all usernames do not contains spaces

				if new_username in client_map: # validation check to avoid two users having the same username
					error_msg = 'This username has been taken. Please try again with /rename <username>'
					f.write('\n'+str(error_msg))
					connection.sendall(error_msg.encode())
				else:
					broadcast_msg = client_username+' has changed their username to '+new_username
					f.write('\n'+str(broadcast_msg))
					print(broadcast_msg)
					broadcast_message(broadcast_msg, client_map)
					client_map[new_username] = client_map.pop(client_username)
					client_username = new_username

				continue

		elif client_msg == '/listUsers':
			availableUsers = '<<Users>>\n'
			count = 1

			for client in client_map:
				availableUsers = availableUsers+(str(count)+'. '+str(client)+'\n')
				count+=1
			f.write('\n\n'+availableUsers+'\n')
			connection.sendall(availableUsers.encode())

			continue

		elif '/whisper' in client_msg:
			command = client_msg.split(' ')
			selected_username = command[1]

			if selected_username == client_username:
				error_msg1 = '\n[Server] Not allowed to private message your ownself!'
				f.write(error_msg1)
				print(error_msg1)
				connection.sendall(error_msg1.encode())
			elif selected_username not in client_map:
				error_msg2 = '\n[Server] This user does not exist.'
				f.write(error_msg2)
				print(error_msg2)
				connection.sendall(error_msg2.encode())
			else:
				message = ' '.join(command[2:])
				if message.strip():
					message_statement = '(private) '+client_username+': '+(' '.join(command[2:]))
					f.write('\n'+message_statement)
					print(message_statement)
					client_map[selected_username].sendall(message_statement.encode())
					client_map[client_username].sendall(message_statement.encode())
				else:
					error_msg3 = '\n[Server] Not allowed to send empty message(s).'
					f.write(error_msg3)
					print(error_msg3)
					connection.sendall(error_msg3.encode())

			continue

		print(chat_display)
		broadcast_message(chat_display, client_map)

	exit_msg = '\n'+client_username+' has left' # handling client disconnection
	f.write(exit_msg)
	print(exit_msg)
	client_map.pop(client_username)
	broadcast_message(exit_msg, client_map)
	connection.close()

def startServer():
	if len(sys.argv) == 2:
		try:
			port = int(sys.argv[1])
		except:
			print('Input type invalid')
			sys.exit(1)
	else:
		print('Port not defined \nUsing default port 8080')
		port = 8080

	## initialising important variables ##
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# allows socket to be reusable
	server_socket.bind((host, port))
	client_map = {}
	threadcount = 0
	######################################
	with open('./server.log', 'w') as f:
		try:
			
			server_socket.listen(5) 
			server_start_msg = 'Server is running and ready to recieve connection at port '+str(port)+'...\n'
			print(server_start_msg)
			f.write(server_start_msg)

			while True:
					connection, client_address = server_socket.accept()
					client_username = connection.recv(1024).decode()
					welcome_msg = '\n'+str(client_username)+' has joined'
					print(str(welcome_msg)+' from '+str(client_address))
					broadcast_message(welcome_msg, client_map)
					client_map[client_username] = connection
					welcome_msg_priv = str(client_username)+' has joined! Type /help for a list of chatroom commands.'
					connection.sendall(welcome_msg_priv.encode())
					f.write('\nRecieved connection from '+str(client_address)+' with username '+str(client_username))
					f.write(welcome_msg)
					start_new_thread(clientThreadInit, (connection, client_map, client_username, f))
					threadcount += 1
					thread_string = '\nThread: '+str(threadcount)+' initialised'
					print(thread_string)
					f.write(thread_string)

		except Exception as e:
			error_msg = '\nServer failed with error: '+str(e)+'\nServer shutting down ...'
			
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