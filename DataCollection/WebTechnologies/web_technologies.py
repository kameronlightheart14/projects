# web_technologies.py
"""
Kameron Lightheart
9/7/19
MATH 403
"""

import json
import socket
from matplotlib import pyplot as plt
import numpy as np

# Problem 1
def prob1(filename="nyc_traffic.json"):
    """Load the data from the specified JSON file. Look at the first few
    entries of the dataset and decide how to gather information about the
    cause(s) of each accident. Make a readable, sorted bar chart showing the
    total number of times that each of the 7 most common reasons for accidents
    are listed in the data set.
    """
    with open(filename, 'r') as infile:
        traffic_data = json.load(infile)
    cause_dict = {}
    for report in traffic_data:
        if ("contributing_factor_vehicle_1" in report.keys()):
            cause = report["contributing_factor_vehicle_1"]
            if (cause in cause_dict.keys()):
                cause_dict[cause] += 1
            else:
                cause_dict[cause] = 1

        if ("contributing_factor_vehicle_2" in report.keys()):
            cause = report["contributing_factor_vehicle_2"]
            if (cause in cause_dict.keys()):
                cause_dict[cause] += 1
            else:
                cause_dict[cause] = 1

    print(cause_dict.values())
    
    top_seven_keys = sorted(cause_dict, key=cause_dict.get, reverse=True)[:7]
    print(top_seven_keys)
    for key in top_seven_keys:
        plt.bar(key + " (" + str(cause_dict[key]) + ")", cause_dict[key],  align='center')
    plt.title("Causes of Accidents in New York")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


class TicTacToe:
    def __init__(self):
        """Initialize an empty board. The O's go first."""
        self.board = [[' ']*3 for _ in range(3)]
        self.turn, self.winner = "O", None

    def move(self, i, j):
        """Mark an O or X in the (i,j)th box and check for a winner."""
        if self.winner is not None:
            raise ValueError("the game is over!")
        elif self.board[i][j] != ' ':
            raise ValueError("space ({},{}) already taken".format(i,j))
        self.board[i][j] = self.turn

        # Determine if the game is over.
        b = self.board
        if any(sum(s == self.turn for s in r)==3 for r in b):
            self.winner = self.turn     # 3 in a row.
        elif any(sum(r[i] == self.turn for r in b)==3 for i in range(3)):
            self.winner = self.turn     # 3 in a column.
        elif b[0][0] == b[1][1] == b[2][2] == self.turn:
            self.winner = self.turn     # 3 in a diagonal.
        elif b[0][2] == b[1][1] == b[2][0] == self.turn:
            self.winner = self.turn     # 3 in a diagonal.
        else:
            self.turn = "O" if self.turn == "X" else "X"

    def empty_spaces(self):
        """Return the list of coordinates for the empty boxes."""
        return [(i,j) for i in range(3) for j in range(3)
                                        if self.board[i][j] == ' ' ]
    def __str__(self):
        return "\n---------\n".join(" | ".join(r) for r in self.board)


# Problem 2
class TicTacToeEncoder(json.JSONEncoder):
    """A custom JSON Encoder for TicTacToe objects."""
    def default(self, obj):
        if not isinstance(obj, TicTacToe):
            raise TypeError("Expected a TicTacToe data type for encoding")
        return {"dtype": "TicTacToe", "data": [obj.board, obj.turn, obj.winner]}


# Problem 2
def tic_tac_toe_decoder(obj):
    """A custom JSON decoder for TicTacToe objects."""
    if "dtype" in obj:
        if obj["dtype"] != "TicTacToe" or "data" not in obj:
            raise ValueError("Expected TicTacToe message from TicTacToeEncoder")
        game = TicTacToe()
        game.board = obj["data"][0]
        game.turn = obj["data"][1]
        game.winner = obj["data"][2]
        return game
    raise ValueError("Expected TicTacToe message from TicTacToeEncoder")

def mirror_server(server_address=("0.0.0.0", 33333)):
    """A server for reflecting strings back to clients in reverse order."""
    print("Starting mirror server on {}".format(server_address))

    # Specify the socket type, which determines how clients will connect.
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(server_address)    # Assign this socket to an address.
    server_sock.listen(1)               # Start listening for clients.

    while True:
        # Wait for a client to connect to the server.
        print("\nWaiting for a connection...")
        connection, client_address = server_sock.accept()

        try:
            # Receive data from the client.
            print("Connection accepted from {}.".format(client_address))
            in_data = connection.recv(1024).decode()    # Receive data.
            print("Received '{}' from client".format(in_data))

            # Process the received data and send something back to the client.
            out_data = in_data[::-1]
            print("Sending '{}' back to the client".format(out_data))
            connection.sendall(out_data.encode())       # Send data.

        # Make sure the connection is closed securely.
        finally:
            connection.close()
            print("Closing connection from {}".format(client_address))

def mirror_client(server_address=("0.0.0.0", 33333)):
    """A client program for mirror_server()."""
    print("Attempting to connect to server at {}...".format(server_address))

    # Set up the socket to be the same type as the server.
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(server_address)    # Attempt to connect to the server.
    print("Connected!")

    # Send some data from the client user to the server.
    out_data = input("Type a message to send: ")
    client_sock.sendall(out_data.encode())              # Send data.

    # Wait to receive a response back from the server.
    in_data = client_sock.recv(1024).decode()           # Receive data.
    print("Received '{}' from the server".format(in_data))

    # Close the client socket.
    client_sock.close()


# Problem 3
def tic_tac_toe_server(server_address=("0.0.0.0", 44444)):
    """A server for playing tic-tac-toe with random moves."""
    print("Starting TicTacToe server on {}".format(server_address))

    # Specify the socket type, which determines how clients will connect.
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(server_address)    # Assign this socket to an address.
    server_sock.listen(1)               # Start listening for clients.
    
    # Wait for a client to connect to the server.
    print("\nWaiting for a connection...")
    while True:
        connection, client_address = server_sock.accept()
        connection_open = True
        while connection_open:
            # Receive data from the client.
            #print("Connection accepted from {}.".format(client_address))
            in_data = connection.recv(1024).decode()    # Receive data.
            #print("Received '{}' from client".format(in_data))

            game = json.loads(in_data, object_hook=tic_tac_toe_decoder)
            # Process the received data and send something back to the client.
            if game.winner is "O":
                connection.sendall("WIN".encode())
                connection.close()
                connection_open = False
            elif len(game.empty_spaces()) == 0 and game.winner is None:
                connection.sendall("DRAW".encode())
                connection.close()
                connection_open = False
            else:
                i, j = game.empty_spaces()[np.random.randint(0, len(game.empty_spaces()))]
                game.move(i, j)
                if game.winner != None:
                    connection.sendall("LOSE".encode())
                    out_data = json.dumps(game, cls=TicTacToeEncoder)
                    #print("Sending", out_data, "to the client")
                    connection.sendall(out_data.encode())
                    connection.close()
                    connection_open = False
                else:
                    out_data = json.dumps(game, cls=TicTacToeEncoder)
                    #print("Sending", out_data, "to the client")
                    connection.sendall(out_data.encode())

# Problem 4
def tic_tac_toe_client(server_address=("0.0.0.0", 44444)):
    """A client program for tic_tac_toe_server()."""
    #print("Attempting to connect to server at {}...".format(server_address))

    # Set up the socket to be the same type as the server.
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(server_address)    # Attempt to connect to the server.
    #print("Connected!")

    game = TicTacToe()
    in_data = ""

    while game.winner is None and in_data != "DRAW":
        print(game)
        move = input("Please make a move in format \"0-2 0-2\": ").split(" ")
        move = [int(move[i]) for i in range(len(move))]
        while len(move) != 2 or move[0] not in [0, 1, 2]\
            or move[1] not in [0, 1, 2] or (move[0], move[1]) not in game.empty_spaces():
            try:
                move = input("Please make a move in format \"0-2 0-2\": ").split(" ")
                move = [int(move[i]) for i in range(len(move))]
            except Exception as e:
                pass

        game.move(move[0], move[1])
        out_data = json.dumps(game, cls=TicTacToeEncoder)

        client_sock.sendall(out_data.encode())              # Send data.

        # Wait to receive a response back from the server.
        in_data = client_sock.recv(1024).decode()           # Receive data.
        #print("Received '{}' from the server".format(in_data))
        
        if (len(in_data) <= 5):
            print(in_data)
        else:
            game = json.loads(in_data, object_hook = tic_tac_toe_decoder)
    print(game)

    # Close the client socket.
    client_sock.close()


def test_encoder_decoder():
    game = TicTacToe()
    tictactoe_message = json.dumps(game, cls=TicTacToeEncoder)
    print("Encoded:", tictactoe_message)
    
    game = json.loads(tictactoe_message, object_hook=tic_tac_toe_decoder)
    print("Decoded:", game.board, game.turn, game.winner)