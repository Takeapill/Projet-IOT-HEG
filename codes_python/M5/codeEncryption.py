from os import urandom
from Crypto.Cipher import AES

#Génération de clé
secret_key = urandom(16)
ib = urandom(16)

obj = AES.new(secret_key, AES.MODE_CBC, iv)

#Encrypter le message

message = "gngn"

message_crypted = obj.encrypt(message)

#Decrypter le message

rev_obj = AES.new(secret_key, AES.MODE_CBC, iv)

message_decrypted = rev_obj.decrypt(message_crypted)

print(message_decrypted.decode('utf-8'))