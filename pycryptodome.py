from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)

data = b"Tajne data"
ciphertext, tag = cipher.encrypt_and_digest(data)

print("Zašifrováno:", ciphertext)

cipher2 = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)
plaintext = cipher2.decrypt(ciphertext)

print("Dešifrováno:", plaintext)