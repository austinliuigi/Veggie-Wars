import socket
import json
import threading


HEADER = 2048
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
print(SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        # msg_length = conn.recv(HEADER).decode(FORMAT)

        # if msg_length:
        #   msg_length = int(msg_length)
          # msg = conn.recv(msg_length).decode(FORMAT)
          msg = conn.recv(HEADER).decode(FORMAT)
          data_package = json.loads(msg)

          # Disconnect
          if data_package["DISCONNECT"] == True:
              print("[SERVER DISCONNECT] Server disconnected")
              connected = False
          
          # Movement
          player1_pos_x, player1_pos_y = data_package["player1_pos"]
          player1_vel_x, player1_vel_y = data_package["player1_vel"]
          js_movement = data_package.get("js", " ")
          if js_movement == "up":
             player1_pos_x -= player1_vel_x
          elif js_movement == "down":
             player1_pos_x += player1_vel_x
          elif js_movement == "left":
             player1_pos_y -= player1_vel_y
          elif js_movement == "right":
             player1_pos_y += player1_vel_y
          data_package["player1_pos"] = (player1_pos_x, player1_pos_y)

          
          # print(data_package["player1_pos"])

          # Encode and send back to client
          json_message = json.dumps(data_package)
          message = json_message.encode(FORMAT)
          conn.send(message)

    conn.close()
    
def start():
    server.listen()
    running = True
    print(f"[LISTENING] Server is listening on {SERVER}")

    while running:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")

def send_back(msg):
    json_message = json.dumps(msg)
    message = json_message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    server.send(send_length)
    server.send(message)

print("[STARTING] Server is starting ...")
start()