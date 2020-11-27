# Python-Chatroom

## Overview
Assignment for Networks and Systems module at Durham University (2nd Second Computer Science)<br><br>The application is split into two programs, **client.py** and **server.py**, and uses the idea of sockets and multithreading for multiuser real-time communications. The programs in folder **Part 1** only allows users to communicate pubicly without any extra functionalities whereas folder **Part 2** has the extended programs that gives users extra functionalities in the chatroom. 

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
`python client.py <your own username> 127.0.0.1 8080`<br>

To run server.py:<br>
`python server.py`

\*While running **client.py** from folder **Part 2**, type */help* in the chatroom GUI to display the extra commands available. 
