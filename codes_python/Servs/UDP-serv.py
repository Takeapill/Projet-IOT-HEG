import socket

UDP_IP = "172.20.11.12"

# Status
lumiere = ""
passage = 0
visiteurs = round(passage / 2)
couleur = ""

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((UDP_IP, 12345))

while True:
    donnees, coordClient = UDPServerSocket.recvfrom(1024)
    print(donnees)

    # Status des capteurs
    if donnees == b"query_status":
        status = f"visiteurs:{visiteurs}\nlumiere:{lumiere}\ncouleur:{couleur}"
        UDPServerSocket.sendto(status.encode('UTF-8'), coordClient)

    elif donnees.startswith(b"lumiere:"):
        lumiere = donnees.split(b":")[1].decode('UTF-8')

    elif donnees.startswith(b"passage:"):
        passage = int(donnees.split(b":")[1])
        visiteurs = round(passage / 2)

    elif donnees.startswith(b"couleur:"):
        couleur = donnees.split(b":")[1].decode('UTF-8')
        
UDPServerSocket.close()



