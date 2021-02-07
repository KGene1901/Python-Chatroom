# Python-Chatroom

## Overview
Assignment for Networks and Systems module at Durham University (2nd Second Computer Science)<br><br>The application is split into two programs, **client.py** and **server.py**, and uses the idea of sockets and multithreading for multiuser real-time communications. The programs in folder **Version 1** is compatible with Python 3.6 (and over) while folder **Version 2** is compatible with Python 3.5 (and over) as it does not make use of formattted strings.

## Tools Used
**Programming Language**:
- Python<br>

**To allow multiuser interaction**:
- socket library
- threading library 
- \_thread library<br>

**Chatroom GUI**:
- tkinter library

## How To Run
To run client.py:<br>
format: python client.py \<username\> \<host address\> \<port number\> <br>
example: `python client.py user1 127.0.0.1 8080`<br>

To run server.py:<br>
format: python server.py \<port number\> <br>
example: `python server.py 8080`

