import socket

TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPServerSocket.bind(('172.20.11.12', 65432))
TCPServerSocket.listen(1)
print('En attente de messages')

while True:

    connexion, addr = TCPServerSocket.accept()
    donnees = connexion.recv(1024).decode("UTF-8")

    # Fais une action correspondant au message recu
    if donnees == "query_logs":
        print(donnees)
        with open('mqtt_logs.log', 'r+') as f:
            lines = f.readlines()
            last_five_lines = '\n'.join(lines[-5:])
        print(last_five_lines)

        connexion.sendall((last_five_lines).encode('UTF-8'))

    # Si aucun autre alors ajouter au logs mqtt
    else:
        with open('mqtt_logs.log', 'a') as f:
            f.write(donnees)
        print(donnees)
    connexion.close()

