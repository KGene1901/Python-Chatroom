import socket	
import sys
from tkinter import *
from threading import Thread

def sendMsg(user_msg, chat_window):
    msg_got = user_msg.get()
    if str(msg_got) == '/quit':
    	client_socket.close()
    	chat_window.quit()
    else:
	    user_msg.set('Enter message here')
	    client_socket.sendall(str(msg_got).encode())

def receiveMsg(messages):
	while True:
		try:
			recieved_msg = client_socket.recv(1024).decode()
			messages.insert(END, recieved_msg)
		except OSError:
			break

def closeWindow(user_msg, chat_window):
	user_msg.set('/quit')
	sendMsg(user_msg, chat_window)

def startClient():

	### Initialise chat window ###
	chat_window = Tk()
	chat_window.title('Chatroom')

	frame = Frame(chat_window) 
	user_msg = StringVar()
	user_msg.set('Enter message here')
	scrollbar = Scrollbar(frame)
	messages = Listbox(frame, height = 15, width = 50, yscrollcommand = scrollbar.set)
	scrollbar.pack(side = RIGHT, fill = Y)
	messages.pack(side = LEFT, fill = BOTH)
	messages.pack()
	frame.pack()
	input_field = Entry(chat_window, text = user_msg)
	input_field.bind("<Return>", lambda event : sendMsg(user_msg, chat_window)) # allows users to press "Enter" to send message
	input_field.pack()
	send_button = Button(chat_window, text = 'SEND', command = lambda : sendMsg(user_msg, chat_window)) # create button to invoke function to send message
	send_button.pack()

	chat_window.protocol('WM_DELETE_WINDOW', lambda : closeWindow(user_msg, chat_window)) # gets invoked when user closes chat window
	##############################

	username = sys.argv[1]
	host = sys.argv[2] 
	port = sys.argv[3]	

	## need to add input check for variables##

	try:
		client_socket.connect((host, int(port)))
		client_socket.sendall(username.encode())

	except Exception as e:
		print('Server not found')
		
	rcv_thread = Thread(target=receiveMsg, args=(messages, ))
	rcv_thread.start()
	chat_window.mainloop()

if __name__ == '__main__':
	client_socket = socket.socket()
	startClient()