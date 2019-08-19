
from Modules.Config.Message import Message
from Modules.Config.Connection import Connection

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65444        # The port used by the server

# CRUD Administrators, Experimenters and Designers (must change index for action)
msg = Message(action=21, information=['Lupe', 'Perez', 'jperes@local.com', '12345']) #CREATE
#msg = Message(action=12, information=[]) #READ
#msg = Message(action=13, information=[2, 'Adrian', 'Perez', 'aperez@local.com', '12345']) #UPDATE
#msg = Message(action=14, information=[2]) #DELETE
#msg = Message(action=15, information=[1]) #SELECT

# CRUD Designers Group
#msg = Message(action=26, information=['Developers group', 'Group with features of software developements', [1, 2, 3]]) #CREATE
#msg = Message(action=27, information=[]) #READ
#msg = Message(action=28, information=[2, 'Group_1', 'Group with skills of security', [1, 2, 3]]) #UPDATE
#msg = Message(action=29, information=[2]) #DELETE
#msg = Message(action=30, information=[3]) #SELECT

connection = Connection()
connection.create_connection(HOST,PORT)
connection.create_message(msg)
connection.send_message()
connection.receive_message()
print(connection.message.comment)
for i in range(0, len(connection.message.information)-1):
    print(connection.message.information[i])
for i in range(0, len(connection.message.information[2])):
    print(connection.message.information[2][i])
connection.close_connection()