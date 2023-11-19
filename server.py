import socket
import datetime
import random

# MAX_PACKET = 4
IP = '0.0.0.0'
PORT = 1234
QUEUE_LEN = 1


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


def time():
    hour = datetime.datetime.now().strftime("%H:%M:%S")
    return str(hour)


def name():
    return "Eitan's Server"


def rand():
    num = random.randint(1, 10)
    return str(num)


def return_value(msg):
    if msg == "TIME":
        return time()
    elif msg == "NAME":
        return name()
    elif msg == "RAND":
        return rand()
    else:
        return "not valid func"


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        my_socket.bind((IP, PORT))
        my_socket.listen(QUEUE_LEN)

        while True:
            client_socket, client_address = my_socket.accept()

            try:
                check = True
                while check:
                    msg = protocol_receive(client_socket)

                    if msg != "EXIT":
                        client_socket.send(protocol_send(return_value(msg)).encode())
                    else:
                        check = False

            except socket.error as err:
                print('received socket error on client socket' + str(err))

            finally:
                print("client left")
                client_socket.close()

    except socket.error as err:
        print('received socket error on server socket' + str(err))

    finally:
        my_socket.close()


if __name__ == "__main__":
    assert protocol_send('eitan') == '5!eitan'
    main()
