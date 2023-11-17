import socket

# MAX_PACKET = 1024
IP = '127.0.0.1'
PORT = 1234


def protocol_send(message):
    message_len = len(message)
    final_message = str(message_len) + '!' + message
    return final_message


def protocol_receive(my_socket):
    cur_char = ''
    message_len = ''
    while cur_char != '!':
        cur_char = my_socket.recv(1).decode()
        message_len += cur_char
    message_len = message_len[:-1]
    return my_socket.recv(int(message_len)).decode()


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
        check = True
        while check:
            func = input("enter a func")
            if len(func) != 4:
                print("func must be 4 letters.")
                continue
            func = func.upper()
            my_socket.send(protocol_send(func).encode())
            if func != "EXIT":
                response = protocol_receive(my_socket)
                print(response)
            elif func == "EXIT":
                check = False

    except socket.error as err:
        print('received socket error ' + str(err))

    finally:
        print("client left the server")
        my_socket.close()


if __name__ == "__main__":
    main()